def _module_actionbar():
	a5=Client._type;aO=Client.on_client_thread;cp=HOST.aborting;cq=HOST.cursor_busy;cr=HOST.dock_forget;cs=HOST.dock_to_bar;bB=HOST.enable;bC=HOST.layout_arranging;ct=HOST.layout_in_use;cu=HOST.layout_locked;cv=HOST.layout_need;cw=HOST.pack_ver;aA=HOST.refresh_settings;a6=HOST.show_settings;cx=HOST.typing;cy=Kit.ART_CLOSE;aP=Kit.ART_MIN;cz=Kit.ART_OK;a7=Kit.ART_PAGE;cA=Kit.ART_PLAY;bD=Kit.ART_RESTORE;r=Kit.HUE_BAD;Q=Kit.HUE_GOOD;D=Kit.HUE_INFO;S=Kit.HUE_TEXT;aa=Kit.HUE_TITLE;cB=Kit.STONE_TILE;E=Kit.add_label;cC=Kit.add_section;bE=Kit.add_textbox;V=Kit.add_tiled;bF=Kit.add_window_frame;cD=Kit.anchor_pos;ab=Kit.art_button;aB=Kit.catcher;bG=Kit.dd_index;T=Kit.dispose;bH=Kit.find_item;bI=Kit.fit;a8=Kit.get_var;aQ=Kit.gold_box;H=Kit.is_open;cE=Kit.load_pos;cF=Kit.mouse_pos;cG=Kit.moved_by_code;cH=Kit.on_client;aC=Kit.pic_size;aR=Kit.pos;bJ=Kit.put_var;cI=Kit.save_min;bK=Kit.screen;aD=Kit.set_text;bL=Kit.spell_info;cJ=Kit.text_px;I=Kit.text_w;bM=Kit.ui_pos;a9=Kit.was_clicked;am=Kit.with_tip;bN=Kit.wrap;ac=Kit.zone_up;q="actionbar";aS="Action Bar";cK="ActionBar_settings";bO="ActionBar_pos";bP="ActionBar_min";u=24;W=12;F=11;J=5;X=u+W;ad=12;d4=22;ba,bb=36,64;an,aE=50,150;d5=8;d6=44;cL=.65;d7=4;d8=3;d9=30;aj=4;ao=2624;ap=.92;bQ=.75;cM=2.;cN=5;ea=.1;cO=set(("clumsy|feeblemind|magic arrow|weaken|harm|fireball|poison|curse|lightning|mana drain|mind blast|paralyze|dispel|energy bolt|explosion|mass curse|chain lightning|flamestrike|mana vampire|meteor swarm|earthquake|mass dispel|paralyze field").split("|"));eb=[("recall","Recall (spell)"),("gate","Gate Travel (spell)"),("charge","Recall (a book charge)"),("recall_scroll","Recall scroll"),("gate_scroll","Gate Travel scroll"),("sacred","Sacred Journey (spell)")];ec={"recall":"Recall","gate":"Gate","charge":"Recall (charge)","recall_scroll":"Recall scroll","gate_scroll":"Gate scroll","sacred":"Sacred Journey"};bc={"recall_scroll":8012,"gate_scroll":8032};cP={"charge":8901,"recall_scroll":8012,"gate_scroll":8032};cQ={"recall":"Recall","gate":"Gate Travel","sacred":"Sacred Journey"};aF="bag";cR="ActionBar_alive";cS="grimoire";ed="Grimoire_cmd";ee="VirtueAssistant_cmd";cT="ActionBar_cells";cU="ActionBar_pages";cV="ActionBar_extra";bd=4;bR=bd*u;cW,cX=240,46;bS=[("paperdoll","Paperdoll",7939,"paperdoll"),("status","Status",3852,"ga:OpenStatusBar"),("journal","Journal",4080,"ga:OpenJournal:ResizableJournal"),("skills","Skills",5091,"ga:OpenSkills"),("spellbook","Grimoire",3834,"grimoire"),("worldmap","World map",5355,"ga:OpenWorldMap"),("minimap","Mini map",5365,"ga:OpenMiniMap"),("quests","Quest log",3636,"quests"),("guild","Guild",7030,"ga:OpenGuildGump"),("party","Party",7956,"macro:PartyManifest"),("chat","Chat",3639,"ga:OpenChat"),("options","Options",7864,"ga:OpenSettings"),("help","Help",4079,"help"),("war","War / peace",5119,"war"),("barsettings","Bar settings",4031,"barsettings"),("virtue","Virtue Assistant",4179,"virtue"),("lock","Lock / unlock bar",4111,"lock"),("minimize","Minimize bar",0,"minimize"),];cY=(3834,8787,8786,9100,9120,11600,11677);ef={"paperdoll":"Open your paperdoll","status":"Open the status bar","journal":"Open the journal","skills":"Open the skills window","worldmap":"Open TazUO's World Map","minimap":"Open the mini map","quests":"Open the quest log","guild":"Open the guild window","party":"Open the party window","chat":"Open the chat window","options":"Open the client's options","help":"Open the help menu","war":"Switch war and peace mode","barsettings":"Open the Action Bar settings page","lock":"Lock or unlock the bar","minimize":"Minimize the bar"};bT="paperdoll status skills spellbook guild chat minimap worldmap options barsettings virtue".split();eg=["paperdoll","status","journal","skills","spellbook","worldmap","minimap","quests","options","barsettings","virtue"];be=16;M=2;eh=("Anatomy|Animal Lore|Animal Taming|Arms Lore|Begging|Cartography|Detect Hidden|Discordance|Evaluate Intelligence|Forensic Evaluation|Hiding|Inscription|Item Identification|Meditation|Peacemaking|Poisoning|Provocation|Remove Trap|Spirit Speak|Stealing|Stealth|Taste Identification|Tracking").split("|");ei=["Magery","Necromancy","Chivalry","Bushido","Ninjitsu","Spellweaving","Mysticism"];bf=16;bU=4;bg=20;bV=[("","Empty"),("item","Item + counter"),("spell","Spell"),("skill","Skill"),("macro","TazUO macro"),("ability","Weapon ability"),("script","Legion script"),("dress","Dress outfit"),("undress","Undress outfit"),("say","Say text"),("ui","Client window"),("travel","Travel (runebook)")];bW=("rb","ri","rm");cZ=[("","None"),("self","Self"),("last","Last target")];bh=["Bags' slots","Bags I pick","Backpack + sub-bags"];c_=((2240,"|".join(f4 for f4,f5 in Kit.MAGERY)),(20480,"Animate Dead|Blood Oath|Corpse Skin|Curse Weapon|Evil Omen|Horrific Beast|Lich Form|Mind Rot|Pain Spike|Poison Strike|Strangle|Summon Familiar|Vampiric Embrace|Vengeful Spirit|Wither|Wraith Form|Exorcism"),(20736,"Cleanse by Fire|Close Wounds|Consecrate Weapon|Dispel Evil|Divine Fury|Enemy of One|Holy Light|Noble Sacrifice|Remove Curse|Sacred Journey"),(21536,"Honorable Execution|Confidence|Evasion|Counter Attack|Lightning Strike|Momentum Strike"),(21280,"Focus Attack|Death Strike|Animal Form|Ki Attack|Surprise Attack|Backstab|Shadowjump|Mirror Image"),(23000,"Arcane Circle|Gift of Renewal|Immolating Weapon|Attune Weapon|Thunderstorm|Nature's Fury|Summon Fey|Summon Fiend|Reaper Form|Wildfire|Essence of Wind|Dryad Allure|Ethereal Voyage|Word of Death|Gift of Life|Arcane Empowerment"),(24000,"Nether Bolt|Healing Stone|Purge Magic|Enchant|Sleep|Eagle Strike|Animated Weapon|Stone Form|Spell Trigger|Mass Sleep|Cleansing Winds|Bombard|Spell Plague|Hail Storm|Nether Cyclone|Rising Colossus"),);ej=["Click a cell to use it; right-click it (Shift+click when right-clicks don't reach the bar) to choose what it holds: an item (counted in your pack), spell, skill, weapon ability, TazUO macro, Legion script, outfit, text to say, window or runebook destination, plus its hotkey and target.","Click an empty cell to target an item for it.","The 12 bottom-left cells have 12 pages, each with its own cells and hotkeys: the tiny arrows and the number switch pages.","Keys (far right) starts keybind mode: hover a cell, window button or bag slot and press a key; Esc ends it, Backspace clears a key. Lock locks the bar (with zones, toggles Arrange mode); Grid shows the snap grid.","Drag the bar by its stone edge; drop it near a corner, edge middle or the centre to anchor it there (upright on the left or right edge).","Bag slots show the bags of Inventory > Bags: click to show the Bags window, again to fold it into the bar; right-click for its settings. With Bags I pick, click an empty slot to target a bag.","The Grimoire and Virtue Assistant buttons show their window (turning Grimoire on); click again to fold it into the bar.","A Module windows button (page 2 of the Client window list) turns that module on and shows its window; click again to fold it into the tray beside the bar. The bar's numbered button hides or shows the tray.","A Travel (runebook) cell goes to a runebook destination by Recall, Gate Travel, a book charge, a scroll or Sacred Journey, through Grimoire (must be on); its counter shows charges or scrolls.","A used skill or spell darkens the cells of that kind while they count down; a spell cell greys out while a reagent it needs is at 0. Red at: when an item's counter turns red."];b={"slot":44,"top":True,"keys":True,"lock":False,"short":True,"hue":False,"bagmode":0,"bags":"","page":0,"scale":100,"tray_open":True,"bagkeys":"","extra":0,"anchor":"","vertical":False};f2=dict(b);C={"a":[],"u":[],"x":[],"pages":[]}
	def c0():return{"shutting":False,"queue":[],"want_target":None,"next_count":0.,"next_scan":0.,"rebuild_at":0.,"bag_sig":None,"ability_sig":None,"bind":None,"jobs":[],"redraw":set(),"ub_job":False,"cool":{"skill":0.,"spell":0.},"cool_next":0.}
	a={"minimized":False,"shutting":False,"docked":False,"queue":[],"em":False,"ub_pending":False,"cnt":{},"cnt_g":{},"first":{},"first_g":{},"bags":[None]*J,"ub_found":None,"ub_cache":None,"ub_state":None,"grim_state":None,"va_state":None,"pending_on":None,"right_ok":None,"dock_sig":None,"watch_next":0.,"script_check":None,"ub_last":None};a.update(c0());e={"g":None,"c":{},"store":({},{}),"cells":{},"bags":{}};bi,B,l=Kit.basics(a,aS);Y={"g":None,"at":None};j={"g":None,"ref":None,"level":"cats","cat":None,"page":0,"c":{},"bag":None,"items":[],"anchor":None,"moved":None,"placed":None};K={"sel":X-W,"dds":[]};bX=dict((f9.lower(),f6+f8)for f6,f7 in c_ for f8,f9 in enumerate(f7.split("|")))
	def ae(fn):a["jobs"].append(fn)
	def c1(name):
		n=(name or "").strip().lower()
		if not n:return 0
		a=bX.get(n)
		if a is None:a=next((d for c,d in bX.items()if c.startswith(n)),None)
		return a if a and aC(a)[0]>0 else 0
	def ek(f):
		d=[str(g)for g in(API.CurrentAbilityNames()or[])];i=1 if f=="secondary"else 0
		if len(d)<=i:return 0,""
		a=d[i];b=[str(h)for h in(API.KnownAbilityNames()or[])]
		if a not in b:return 0,a
		c=b.index(a)
		if b and b[0].lower()in("none","invalid"):c-=1
		e=20992+c;return(e if c>=0 and aC(e)[0]>0 else 0),a
	def aT(uid):
		if uid.startswith("mod:"):return c2(uid[4:])
		return next((c for c in bS if c[0]==uid),None)
	def c2(key,a=None):
		s=HOST.by_key.get(key)
		if s is None or key==q:return
		d=(a if a is not None else dict(HOST.docks)).get(key);b=int(d.get("icon")or 0)if d else 0;return("mod:"+key,s.title,b,"mod:"+key)
	def c3():
		b=[];c=dict(HOST.docks)
		for a in HOST.slots:
			e=[g[4][0]if len(g)>4 and g[4]else "%s.%s"%(a.key,g[0])for g in a.parts]
			for f in e or[a.key]:
				d=c2(f,c)
				if d is not None:b.append(d)
		return b
	def c4():return bS+c3()
	def el(key):
		s=HOST.by_key.get(key)
		if s is None:return "Module '%s' (not loaded)"%key
		d=dict(HOST.docks).get(key)
		if not s.running:return "Turn %s on"%s.title
		if d is None:return "Turn %s off"%s.title
		if safe(d.get("state"))=="open":return "Fold %s into the bar"%s.title
		return "Show %s"%s.title
	def em(key):
		s=HOST.by_key.get(key)
		if s is None:l("no module '%s'."%key,r);return False
		d=dict(HOST.docks).get(key)
		if not s.running:
			cr(key)
			def a(k=key,title=s.title):
				bB(k)
				if not HOST.by_key[k].running:l("%s couldn't be turned on."%title,r)
			ae(a);return True
		if d is None:HOST.disable(key);return True
		if safe(d.get("state"))=="open":cs(key,s.title)
		else:safe(d.get("show"));cr(key)
		return True
	def aq(k):return HOST.hotkeys_owned.get(_norm_key(k))
	def en():return set(_norm_key(d["k"])for f,d in ar()if d["k"]and d["t"])|set(c for c in af()if c)
	def ak(text,width):return bI(str(text),width,".")
	def c5(k):return(k.upper().replace("CTRL+","C").replace("SHIFT+","S").replace("ALT+","A").replace("NUMPAD","N").replace("KP_","N"))
	def c6(n):
		if b["short"]:
			if n>=10000:return "%dk"%(n//1000)
			if n>=1000:return "%.1fk"%(n/1000.)
		return str(n)
	def eo(text):
		t=(text or "").strip()
		if not t:return
		a,b=[c.strip()for c in(t.split(",",1)+[""])[:2]]
		try:return(int(a,16)if a.lower().startswith("0x")else int(a),(int(b,16)if b.lower().startswith("0x")else int(b))if b else 0)
		except Exception:return
	def Z():return{"t":"","v":"","g":0,"h":0,"tg":"","k":"","lo":cN,"n":""}
	def A(ref):return C[ref[0]][ref[1]]
	def af():a=[_norm_key(c)for c in b["bagkeys"].split(",")];return(a+[""]*J)[:J]
	def bY(ref,k):
		if ref[0]=="b":a=af();a[ref[1]]=k;b["bagkeys"]=",".join(a);ag()
		else:A(ref)["k"]=k;aW()
	def N(ref):
		a,i=ref
		if a=="b":return "bag slot %d"%(i+1)
		if a=="u":return "button %d"%(i+1)
		if a=="x":return "row %d cell %d"%(i//u+2,i%u+1)
		if i<u:return "top cell %d"%(i+1)
		return "page %d cell %d"%(b["page"]+1,i-u+1)
	def aU(idx):
		if idx<X:return("a",idx)
		if idx<X+F:return("u",idx-X)
		return("x",idx-X-F)
	def ep(ref):
		if ref[0]=="a":return ref[1]
		if ref[0]=="u":return X+ref[1]
		return X+F+ref[1]
	def eq():return(["Top %d"%(c+1)for c in range(u)]+["Bottom %d"%(d+1)for d in range(W)]+["Button %d"%(f+1)for f in range(F)]+["Row %d-%d"%(g//u+2,g%u+1)for g in range(bR)])
	def c7(ref):
		a,i=ref
		if a=="x":return i<b["extra"]*u
		if a=="a":return b["top"]or i>=u
		return True
	def ar():return[((d,f),g)for d in "aux"for f,g in enumerate(C[d])]
	def er():
		a=[Z()for g in range(X)];c=[(3617,"Bandages","self"),(3852,"Heal potion",""),(3847,"Cure potion",""),(3851,"Refresh potion","")]
		for i,(d,n,e)in enumerate(c):a[u+i].update({"t":"item","g":d,"n":n,"tg":e})
		b=[Z()for h in range(F)]
		for i,f in enumerate(bT[:F]):b[i].update({"t":"ui","v":f})
		return a,b
	def au(c):
		t,v=c["t"],c["v"]
		if t=="item":return c["n"]or("0x%04X"%c["g"])
		if t=="ui":d=aT(v);return d[1]if d else v
		if t=="ability":return "Secondary"if v=="secondary"else "Primary"
		if t=="script":return v.replace("\\","/").split("/")[-1].rsplit(".",1)[0]
		return v
	def bj(c):return "%s to %s%s"%(ec.get(c.get("rm"),"Travel"),c["v"]or "?",(" (%s)"%c["n"])if c["n"]else "")
	def aV(ref):
		c=A(ref);t=c["t"]
		if not t:
			if ref[0]in("a","x"):return "Empty: click to target an item; right-click for a spell, skill or more"
			return "Empty: right-click to choose what it does"
		if t=="travel":
			b=bj(c)
			if HOST.services.get("grimoire.travel")is None:b="Grimoire is off: turn it on to use this cell\n"+b
			if c["k"]:b+="  [%s]"%c["k"]
			return b+"\nRight-click to change"
		d=au(c)
		if t=="ui"and c["v"]=="spellbook":d={"open":"Fold Grimoire into the bar","minimized":"Show Grimoire","docked":"Show Grimoire"}.get(a["grim_state"],"Open Grimoire (turns it on)")
		elif t=="ui"and c["v"]=="virtue":d={"open":"Fold Virtue Assistant into the bar","gear":"Open the Virtue Assistant window","docked":"Open the Virtue Assistant window"}.get(a["va_state"],"Virtue Assistant (not running)")
		elif t=="ui"and c["v"].startswith("mod:"):d=el(c["v"][4:])
		elif t=="ui":d=ef.get(c["v"],d)
		b={"item":"Use %s","spell":"Cast %s","skill":"Use %s","macro":"Run macro %s","ability":"Use the %s ability","script":"Start or stop script %s","dress":"Dress %s","undress":"Undress %s","say":"Say \"%s\"","ui":"%s"}.get(t,"%s")%d
		if c["tg"]:b+=", then target %s"%("yourself"if c["tg"]=="self"else "last target")
		if c["k"]:b+="  [%s]"%c["k"]
		if t=="spell":
			e=dn(c["v"])
			if e is not None:b+="\nOut of %s"%e[1]
		return b+"\nRight-click to change"
	def es(s):return(str(s).replace("%","%25").replace("&","%26").replace("=","%3D").replace(";","%3B").replace("|","%7C"))
	def et(s):return(s.replace("%7C","|").replace("%3B",";").replace("%3D","=").replace("%26","&").replace("%25","%"))
	def c8(d):return "&".join("%s=%s"%(c,es(f))for c,f in d.items())
	def c9(s):return dict((c,et(d))for c,d in(f.split("=",1)for f in s.split("&")if "="in f))
	def da():
		d=c9(a8(cK))
		for k in("top","keys","lock","short","hue","tray_open","vertical"):
			if k in d:b[k]=d[k]=="1"
		for k,c,e in(("slot",ba,bb),("bagmode",0,len(bh)-1),("page",0,ad-1),("scale",an,aE),("extra",0,bd)):
			with Kit.quiet:b[k]=int(d[k])
			b[k]=max(c,min(e,b[k]))
		a=d.get("anchor","");b["anchor"]=a if a in Kit.ANCHORS else ""
		for k in("bags","bagkeys"):b[k]=d.get(k,b[k])
	def ag():bJ(cK,c8(dict((d,("1"if c else "0")if isinstance(c,bool)else c)for d,c in b.items())))
	def eu(d):
		c=Z()
		for k in("t","v","tg","k","n"):c[k]=d.get(k,c[k])
		for k in("g","h","lo"):
			with Kit.quiet:c[k]=int(d.get(k,c[k]))
		if c["t"]=="travel":
			for k in bW:c[k]=d.get(k,"")
		return c
	def bk(raw,n,a=True):b=[eu(c9(c))for c in raw.split(";")if c or not a];return(b+[Z()for d in range(n)])[:n]
	def db():
		bZ.clear();d,a=er();f=a8(cT)
		if "|"in f:
			i,j=f.split("|",1);d=bk(i,X,False);a=bk(j,F,False);k=set(p["v"]for p in a if p["t"]=="ui");g=[s for s in bT if s not in k]
			for c in a:
				if c["t"]=="ui"and aT(c["v"])is None and not c["v"].startswith("mod:"):
					c.update(Z())
					if g:c.update({"t":"ui","v":g.pop(0)})
			if[t["v"]if t["t"]=="ui"else None for t in a]==eg[:F]:
				for l,m in enumerate(bT[:F]):a[l].update({"t":"ui","v":m})
		e=[[Z()for w in range(W)]for v in range(ad)];h=a8(cU)
		if h:
			for n,o in enumerate(h.split("|")[:ad]):e[n]=bk(o,W)
		else:e[0]=d[u:];b["page"]=0
		d[u:]=e[b["page"]];C["x"]=bk(a8(cV),bR);C["a"],C["u"],C["pages"]=d,a,e;b3()
	def dc():
		if C["pages"]:C["pages"][b["page"]]=list(C["a"][u:])
	bZ={}
	def aW():
		dc();b3()
		def a(a):return ";".join(c8(d)for d in a)
		for b,c in((cT,a(C["a"])+"|"+a(C["u"])),(cU,"|".join(a(f)for f in C["pages"])),(cV,a(C["x"]))):
			if bZ.get(b)!=c:bJ(b,c);bZ[b]=c
	def ev(p):
		p=p%ad
		if p==b["page"]:return
		dc();b["page"]=p;C["a"][u:]=C["pages"][p];b3();ag();az();a["next_count"]=0.;aM([("a",u+c)for c in range(W)]);e_();aA(q);r=j.get("ref")
		if j.get("g")is not None and r and r[0]=="a"and r[1]>=u:ay()
	def de():
		a=[0]*J
		for i,p in enumerate(b["bags"].split(",")[:J]):
			try:a[i]=int(p,16)if p.strip()else 0
			except Exception:a[i]=0
		return a
	def df(i,serial):a=de();a[i]=serial;b["bags"]=",".join(("%X"%c)if c else ""for c in a);ag()
	def aX():
		if ac(q):return
		p=aR(e["g"])if H(e["g"])else None
		if p is not None and p!=a.get("pos_saved"):a["pos_saved"]=p;bJ(bO,"%d,%d"%p)
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
			ClientUI.looked=True;a=ClientUI.world=safe(lambda:ClientUI._get(API,"World"));ClientUI.GA=a5("ClassicUO.Game.GameActions");ClientUI.UIM=a5("ClassicUO.Game.Managers.UIManager")
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
	def dg():return Kit.data_path("_unified_bag_%d.cfg"%int(safe(lambda:API.Player.Serial,0)or 0))
	def dh(path):
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
	def ew():
		if not aO():a["ub_last"],a["ub_pending"]=dh(dg()),False
		elif not a["ub_job"]:
			a["ub_job"]=True;b=dg()
			def c():
				a["ub_job"]=False;c=dh(b)
				if c!=a["ub_last"]or a["ub_pending"]:a["ub_last"],a["ub_pending"]=c,False;a["next_scan"]=0.
			ae(c)
		return None if a["ub_last"]is None else list(a["ub_last"])
	def b_(a,b):s=API.GetSharedVar(a);return str(s)if s is not None and str(s)in b else None
	def aG():return b_("UnifiedBag_state",("open","collapsed","docked"))
	def bl():return b_("Grimoire_state",("open","minimized","docked"))
	def b0():return b_("VirtueAssistant_state",("open","gear","docked"))
	def b1(cmd):API.SetSharedVar("UnifiedBag_cmd",cmd)
	def b2():return list(HOST.docks)
	def bm():return[(f,c)for f,c in b2()if c.get("always")or safe(c.get("state"))=="docked"]
	def di():return tuple([(c,safe(f.get("state")))for c,f in b2()])
	def dj():return tuple([(f,c.get("icon"),safe(c.get("state"))if c.get("always")else None)for f,c in bm()])
	def ah(on=True):
		if on and not a["em"]:API.SetSharedVar(cR,time.time())
		else:API.RemoveSharedVar(cR)
	def ex():
		f=time.time()
		if f<a["watch_next"]:return
		a["watch_next"]=f+.25;c=False
		for k,s,i in(("ub_state",aG(),b["bagmode"]==0),("grim_state",bl(),True),("va_state",b0(),True)):
			if s!=a[k]:a[k]=s;c=c or i
		if c:dy()
		d=di()
		if d!=a["dock_sig"]:
			j=set(o for o,t in(a["dock_sig"]or()));a["dock_sig"]=d;g=dj()
			if g!=a.get("tray_sig"):a["tray_sig"]=g;dA()
			h=[w for w,v in ar()if v["t"]=="ui"and v["v"].startswith("mod:")]
			if h:
				if set(x for x,y in d)!=j:aM(h)
				else:dy()
		e=frozenset(HOST.hotkeys_owned)
		if e!=a.get("owned_sig"):
			m=e^(a.get("owned_sig")or frozenset());a["owned_sig"]=e
			if m&en():az()
		p=a["pending_on"]
		if p and time.time()>p[2]:
			a["pending_on"]=None;n=aG()if p[0]==aF else bl()
			if n is None:
				l("%s didn't start; is Virtue Assistant running?"%p[1],r)
				if p[3]is not None:p[3]()
	def bn(key,title,fallback=None):
		if key in HOST.by_key:ae(lambda:bB(key))
		else:API.SetSharedVar("VirtueAssistant_enable",key)
		l("turning %s on."%title);a["pending_on"]=(key,title,time.time()+4.,fallback)
	def ey():
		a=bl();ah()
		if a in("minimized","docked","open"):API.SetSharedVar(ed,"dock"if a=="open"else "show")
		else:bn(cS,"Grimoire",fa)
		return True
	def ez():
		a=b0();ah()
		if a not in("open","gear","docked"):l("Virtue Assistant isn't running.",r);return False
		API.SetSharedVar(ee,"dock"if a=="open"else "show");return True
	def dk():
		a=[];b=int(API.Backpack or 0)
		if b:a.append(b)
		for c in(API.ItemsInContainer(b,False)or[]):
			if len(a)>=J:break
			with Kit.quiet:
				if c.IsContainer:a.append(int(c.Serial))
		return a
	def dl():
		h=b["bagmode"]
		if h==0:
			c=ew()
			if c is None and a["ub_pending"]:c=[]
			else:
				a["ub_found"]=c is not None
				if c is None:c=dk()
		elif h==1:c=de()
		else:c=dk()
		d,g=[],[]
		for s in(list(c)+[0]*J)[:J]:
			if not s:d.append(None);g.append(None);continue
			e=bH(s);g.append(e)
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
			a["bags"],a["bag_sig"]=d,k;aM([("b",n)for n in range(J)])
	def aH(i):return a["bags"][i]if i<len(a["bags"])else None
	av={"types":None}
	def b3():av["types"]=None
	def aY():
		if av["types"]is None:
			b=C["a"]+C["u"]+C["x"];av["types"]=set(g["t"]for g in b);av["items"]=set(h["g"]for h in b if h["t"]=="item");d,e=set(),set();a={"skill":[],"spell":[]}
			for f,c in ar():
				if c["t"]=="spell":d.update(i[1]for i in dm(c["v"]));a["spell"].append(f)
				elif c["t"]=="skill":a["skill"].append(f)
				elif c["t"]=="travel"and c.get("rm")in bc:e.add(bc[c["rm"]])
			av["extra"],av["refs"]=frozenset(d|e),a
		return av
	def eA():
		if "ability"not in aY()["types"]:return
		b=tuple([str(d)for d in(API.CurrentAbilityNames()or[])])
		if b!=a["ability_sig"]:a["ability_sig"]=b;aM([f for f,g in ar()if g["t"]=="ability"])
	def aZ(extra=(),max_age=0.):
		o=cw()
		try:p=HOST.pack_items(deep=True,max_age=max_age);q=int(API.Backpack or 0)
		except Exception:return
		k=aY();d=k["items"]
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
	def b4(info,lbl,text,hue):
		if info.get("txt")!=text:
			info["txt"]=text
			try:lbl.Text=text;bM(lbl,info["x"]+info["w"]-cJ(text)-3,info["y"]+info["h"]-16)
			except Exception:pass
		if info.get("hue")!=hue:info["hue"]=hue;Kit.set(lbl,"Hue",hue)
	def eB():
		if a["em"]:return
		k=aY()
		if "item"in k["types"]or k["extra"]:aZ(max_age=.5)
		else:a["pack_v"]=None
		a0()
	a_=[None]
	def a0():
		l=time.time();s=a["cool"];m=False;i=a_[0]
		if i is None:i=[(x,w,w["count"])for x,w in e["cells"].items()if w.get("count")is not None];a_[0]=i
		for p,g,j in i:
			c=A(p);t,v=c["t"],c["v"];d,f="",S;h=s.get(t)
			if h and l<h:d,f=do(h-l),aa
			elif t=="item":n=a["cnt"].get((c["g"],c["h"]),0)if b["hue"]else a["cnt_g"].get(c["g"],0);d=c6(n);f=r if n<=max(0,c["lo"])else S
			elif t in("spell","ability","script"):
				try:
					if t=="spell":k=bool(API.IsSpellActive(v))
					elif t=="ability":k=bool(API.SecondaryAbilityActive()if v=="secondary"else API.PrimaryAbilityActive())
					else:k=bx(v)
				except Exception:k=False
				d,f=("ON"if k else ""),Q
			elif t=="travel":
				if m is False:m=eD()
				d,f=eE(c,m)
			if t=="spell":
				o=dn(v);eC(p,g,o is not None)
				if o is not None and not(h and l<h):d,f=o[0],r
			b4(g,j,d,f)
		for u,g in list(e["bags"].items()):
			j=g.get("count");q=aH(u)
			if j is None or not q:continue
			try:n=int(API.Contents(q["s"])or 0)
			except Exception:n=0
			b4(g,j,str(n),S)
	bo={}
	def dm(name):
		a=bo.get(name)
		if a is None:
			c=bL(name);b=Kit.REAGENTS;a=tuple((d,b[d][1],b[d][0])for d in(c[1]if c else())if d in b)
			if len(bo)>200:bo.clear()
			bo[name]=a
		return a
	def dn(name):
		b,c=a["cnt_g"],a.get("counted")or()
		for d,g,n in dm(name):
			if b.get(g,0)<=0 and g in c:return(d,n)
		return
	def eC(ref,info,grey):
		if info.get("grey",False)==grey:return
		info["grey"]=grey;a=info.get("icon")
		if a is not None:a.SetAlpha(.35 if grey else 1.)
		bt(info,aV(ref))
	def eD():
		a=HOST.services.get("grimoire.book_charges")
		if a is not None:return safe(a)
		a=HOST.services.get("grimoire.destinations")
		if a is None:return
		try:return dict((c["book"],c["charges"])for c in a()or())
		except Exception:return
	def eE(c,charges):
		if charges is None:return "off",D
		m=c.get("rm");b=max(0,c["lo"])
		if m in bc:n=a["cnt_g"].get(bc[m],0);return c6(n),r if n<=b else S
		try:n=charges.get(int(c.get("rb")or "0",16))
		except ValueError:n=None
		if n is None:return "",S
		if m=="charge":return str(n),r if n<=b else S
		return str(n),D
	def eF(c):
		a=HOST.services.get("grimoire.travel")
		if a is None:l("Grimoire is off; turn it on to use Travel cells.",r);return False
		try:b,d=int(c.get("rb")or "",16),int(c.get("ri")or "")
		except ValueError:l("this Travel cell has no destination; right-click it to pick one.",r);return False
		return bool(a(b,d,c.get("rm")or "recall",c["v"]or None))
	def eG(ref,d,method):a=A(ref);b=dict(Z(),t="travel",v=str(d["name"]),n=str(d["book_name"]),k=a["k"],tg="",lo=a["lo"]if a["t"]=="travel"else 2,rb="%X"%int(d["book"]),ri=str(int(d["index"])),rm=method);C[ref[0]][ref[1]]=b;aw(recount=True,refs=[ref]);l("%s set on %s."%(bj(b),N(ref)),Q)
	eH={"arms lore":3.,"item identification":3.,"detect hidden":3.}
	def do(a):return("%d"%int(math.ceil(a)))if a>=3. else("%.1f"%max(0.,a))
	def eI(t,v):
		if t=="skill":b=eH.get(str(v).strip().lower(),10.)
		else:c=bL(v);b=c[3]if c else 0.
		if b and b>0:a["cool"][t]=time.time()+b;a["cool_next"]=0.
	def eJ(now):
		c=a["cool"]
		if not(c["skill"]or c["spell"])or now<a["cool_next"]:return
		a["cool_next"]=now+.1;k=aY()["refs"];i=False
		for f in("skill","spell"):
			g=c[f]
			if not g:continue
			d=now>=g
			if d:c[f]=0.;i=True
			l=""if d else do(g-now)
			for m in k[f]:
				b=e["cells"].get(m)
				if b is None:continue
				h=not d
				if b.get("dark",False)!=h:b["dark"]=h;b["catcher"].SetAlpha(.55 if h else.01)
				j=b.get("count")
				if j is not None and not d:b4(b,j,l,aa)
		if i:a0()
	def eK(ref):
		c=A(ref)
		if c["t"]=="travel":return bj(c)
		a=aV(ref).split("\n")[0];return a.replace("  [%s]"%c["k"],"")if c["k"]else a
	def eL():a=[(_norm_key(f["k"]),"%s: %s"%(N(d),eK(d)))for d,f in ar()if _norm_key(f["k"])and f["t"]and c7(d)];a+=[(c,"bag slot %d"%(g+1))for g,c in enumerate(af())if c];return[(h,i+((" (left to %s)"%aq(h))if aq(h)else ""))for h,i in a]
	eM=Kit.disposer(q,a,e)
	def al(delay=0.):a["rebuild_at"]=time.time()+delay
	def aw(recount=False,refresh=True,refs=None):
		aW();az()
		if recount:a["next_count"]=0.
		if refs is None:al()
		else:aM(refs)
		if refresh:aA(q)
	def dp(ref):C[ref[0]][ref[1]]=Z();aw(refs=[ref])
	z={"scale":None,"vertical":None,"slot":None,"off":(0,0),"sig":None}
	def bp():v=z["scale"];return int(b["scale"])if v is None else v
	def aI():v=z["vertical"];return bool(b["vertical"])if v is None else v
	def b5():return z["slot"]if z["scale"]is not None else None
	def dq():return(b["slot"],b["top"],b["extra"])
	def b6(b,c):
		f=z["scale"]
		try:
			z["scale"]=100;d=aJ();a=max(an,min(aE,int(min(b*100./max(1.,d["W"]),c*100./max(1.,d["H"])))))
			def e(p):z["scale"]=p;a=aJ();return a["W"]<=b and a["H"]<=c
			for g in range(8):
				if a<=an or e(a):break
				a-=1
			for g in range(8):
				if a>=aE or not e(a+1):break
				a+=1
			return a
		finally:z["scale"]=f
	def dr():
		a=HOST.layout_base(q)
		if not b["extra"]or a is None:cv(q);return
		c=a[1]>a[0];f,g=(a[1],a[0])if c else a;d,h,i=b["extra"],z["scale"],P.get("vtmp");P["vtmp"]=c
		try:b["extra"]=0;p=b6(int(f),int(g));b["extra"]=d;z["scale"]=p;e=aJ()["H"]
		finally:b["extra"]=d;z["scale"]=h;P["vtmp"]=i
		cv(q,e if c else None,None if c else e)
	def eN(w,h,mode):
		if w is None or h is None or not w or not h:c=(None,None);d=e=None
		else:
			d=(int(w),int(h));b=h>w;f,g=(h,w)if b else(w,h);e=dq();dr();P["vtmp"]=b
			try:c=(b6(int(f),int(g)),b)
			finally:P["vtmp"]=None
		i=(bp(),aI(),z["slot"]);z["scale"],z["vertical"]=c;z["slot"],z["sig"]=d,e
		if(bp(),aI(),z["slot"])!=i and not a["shutting"]:al()
	def eO():
		a=b5();b=dq()
		if a is None or b==z["sig"]:return
		c,d=(a[1],a[0])if z["vertical"]else a;z["scale"]=b6(c,d);z["sig"]=b;dr()
	def eP():
		if e["g"]is None or a["shutting"]:return
		return "minimized"if a["em"]else "open"
	def eQ():
		c,d=z["scale"],P["vtmp"];a=[]
		try:
			z["scale"]=an
			for v in(False,True):P["vtmp"]=v;b=aJ();a.append((b["H"],b["W"])if v else(b["W"],b["H"]))
		finally:z["scale"],P["vtmp"]=c,d
		return min(a[0][0],a[1][0]),min(a[0][1],a[1][1])
	eR={"fit":eN,"state":eP,"min":eQ,"exact":True,"untitled":True}
	def sc(v,lo=1):k=max(an,min(aE,bp()))/100.;return max(lo,int(round(v*k)))
	a1={"key":None,"L":None}
	def b7():
		a=b5();c=(b["slot"],bp(),b["top"],b["extra"],a,aI())
		if a1["key"]!=c:
			if a is None:a1["L"]=aJ()
			else:d,e=(a[1],a[0])if aI()else a;a1["L"]=eU(aJ(),d,e)
			a1["key"]=c
		return a1["L"]
	P={"capw":None,"vtmp":None}
	def ds():
		if P["capw"]is None:P["capw"]=max(I(d)for d in("Keys","Lock","Grid"))+6
		return P["capw"]
	def dt(a):return(4,2,1)if a else(1,2,4)
	def eS(c,b,d):a=(4+c-1)//c;e=(b-2*M-(c-1)*M)//c;f=min(24,(d-2*M-(a-1)*M)//a);return a,e,f
	def eT(b,a):
		d=ds()
		for c in dt(a):
			e=(4+c-1)//c;f=e*be+(e-1)*M+2*M;g=c*d+(c-1)*M+2*M
			if a and g<=b:return f
			if not a and f<=b:return g
		return(4*be+5*M)if a else(4*d+5*M)
	def aJ():S=sc(max(ba,min(bb,int(b["slot"]))),18);k,c,a=sc(d5,4),sc(6,3),sc(4,2);m=k;t,l,n=sc(4,2),sc(d7,2),sc(d8,2);h,g,o=sc(d4,16),sc(d6,34),sc(d9,18);f=S+t;e=S+2*a;i=h+u*f+a;p=W*f+a;q=o+2*a;r=i-h-p-2*c-q-c;j=int(r*cL);s=r-j;v=(j-2*a-(F-1)*l)//F;w=(s-2*a-(J-1)*n)//J;d=(2 if b["top"]else 1)+b["extra"];g=max(g,eT(d*e+(d-1)*c,aI()if P["vtmp"]is None else P["vtmp"]));return{"S":S,"pitch":f,"ph":e,"inner":i,"left_w":p,"rows":d,"ui_w":j,"bag_w":s,"bw":v,"bh":e-3*a,"tray_w":q,"tb":o,"bgw":w,"bgh":e-2*a,"m":m,"sg":c,"p4":a,"ug":l,"bg":n,"pw":h,"cw":g,"tm":k,"colx":tuple(a+x*f for x in range(u)),"colw":(S,)*u,"top_w":u*f+a,"sgx":c,"sgc":c,"rowy":tuple(y*(e+c)for y in range(d)),"rowh":(e,)*d,"celly":(a,)*d,"cellh":(S,)*d,"W":m+i+c+g+m,"H":m+d*e+(d-1)*c+m}
	def aK(total,n):
		if n<=0:return[]
		if total<=0:return[0]*n
		return[(total*(c+1))//n-(total*c)//n for c in range(n)]
	def eU(L,O,P):
		L=dict(L);S,e,d,c=L["S"],L["p4"],L["sg"],L["rows"];o=L["pitch"]-S;n=u;p=max(0,int(S*1.6)-S);a=O-L["W"]
		if a>0:
			h=n*o+d;b=min(a,h);t=float(b)/h if h>0 else 0.;q=min(b,int(round(d*t)));i=[o+at for at in aK(b-q,n)];f=min(a-b,n*p);s=[S+by for by in aK(f,n)];j=a-b-f;v=0
			if j>0:
				if c>1:i=[dd+fn for dd,fn in zip(i,aK(j,n))]
				else:v=j
			k,x=[],e
			for w in range(n):k.append(x);x+=s[w]+i[w]
			z=d+int(round(d*t));A=L["ug"]+int(round(L["ug"]*t));B=L["bg"]+int(round(L["bg"]*t));C,Q=L["pw"],L["tray_w"];l=C+x+v;D=k[W];E=l-C-D-3*z-Q;m=int(E*cL);G=E-m;L.update({"colx":tuple(k),"colw":tuple(s),"top_w":x,"sgx":z,"sgc":d+q,"ug":A,"bg":B,"inner":l,"left_w":D,"ui_w":m,"bag_w":G,"bw":(m-2*e-(F-1)*A)//F,"bgw":(G-2*e-(J-1)*B)//J});L["W"]=L["m"]+l+L["sgc"]+L["cw"]+L["m"]
		a=P-L["H"]
		if a>0:
			b=min(a,(c-1)*d);R=[d+f4 for f4 in aK(b,c-1)];f=min(a-b,c*p);g=[S+f5 for f5 in aK(f,c)];H=aK(a-b-f,c);I,K,M,y=[],[],[],0
			for r in range(c):I.append(y);N=g[r]+2*e+H[r];K.append(N);M.append(e+H[r]//2);y+=N+(R[r]if r<c-1 else 0)
			L.update({"rowy":tuple(I),"rowh":tuple(K),"celly":tuple(M),"cellh":tuple(g),"bh":g[-1]-e,"bgh":g[-1]});L["H"]=L["m"]+y+L["m"]
		return L
	def aL():return not aI()
	def bq():
		if a["em"]:return cW,cX
		L=b7();return(L["W"],L["H"])if aL()else(L["H"],L["W"])
	def R(x,y,w,h):a,b=z["off"];return(x+a,y+b,w,h)if aL()else(y+a,x+b,h,w)
	def a2(g,graphic,hue,x,y,w,h):
		try:p=G.CreateGumpItemPic(int(graphic),int(w),int(h))
		except Exception:return
		if hue:p.Hue=max(0,min(65535,int(hue)))
		p.SetPos(x,y);p.SetAcceptMouseInput(False);g.Add(p);return p
	def du(text):t=str(text).replace("_"," ");return "".join(" "+c if d and c.isupper()and t[d-1].islower()else c for d,c in enumerate(t))
	def a3(g,text,x,y,w,h,hue=None):
		b=max(1,min(3,(h-2)//14));a=[bI(d,w-4)for d in bN(du(text),w-4)]
		if len(a)>b:a=a[:b];a[-1]=bI(a[-1]+"..",w-4)if not a[-1].endswith("..")else a[-1]
		c=y+(h-14*len(a))//2-1;return[E(g,f,x+(w-I(f))//2,c+k*14,S if hue is None else hue)for k,f in enumerate(a)]
	def eV(kind,c,b):
		def d():
			if a["right_ok"]is False and Client.key_held("shift"):B.add((c,b),dup=True)
			else:B.add((kind,b),dup=True)
		return Kit.once(d,(q,kind,b),Kit.TWICE)
	def eW(b,fn):
		if b is None or a["right_ok"]is False:return False
		if Kit.hook_mouse(b,fn,event="MouseUp",button="Right"):a["right_ok"]=True;return True
		if a["right_ok"]is None:a["right_ok"]=False;l("no right-click events from this client; Shift+click a cell for its menu instead.")
		return False
	def br(g,icon,x,y,w,h):
		a=min(w,h)-4;p=Kit.add_pic(g,icon,x+(w-a)//2,y+(h-a)//2)
		if p is not None:p.SetWidth(a);p.SetHeight(a);p.SetAcceptMouseInput(False)
		return p
	def bs(g,a,d,y,h):
		e=Kit.GOLD_V if aL()else Kit.GOLD_H
		for b,f,w in zip(a,a[1:],d):c=f-b-w;s=min(c,Kit.GOLD_T);V(g,e,*R(b+w+(c-s)//2,y,s,h))
	def b8(g,ref,x,y,w,h):
		if not A(ref)["t"]:
			V(g,ao,x,y,w,h,ap*.3)
			for a,b,c,d in((x,y,w,1),(x,y+h-1,w,1),(x,y,1,h),(x+w-1,y,1,h)):V(g,ao,a,b,c,d,ap)
		else:V(g,ao,x,y,w,h,ap)
		dv(g,ref,x,y,w,h)
	def b9(ref,x,y,w,h,pad):
		if w==h or ref[0]=="u":return x+pad,y+pad,w-2*pad,h-2*pad
		a=min(w,h)-2*pad;return x+(w-a)//2,y+(h-a)//2,a,a
	def dv(g,ref,x,y,w,h):
		c=A(ref);t=c["t"];l={"x":x,"y":y,"w":w,"h":h,"count":None};f=[];j=False;d=14 if(b["keys"]and c["k"]and t)else 0;p=None
		if t=="item"and c["g"]:p=a2(g,c["g"],c["h"],*b9(ref,x,y,w,h,3))
		elif t=="spell":
			a=c1(c["v"])
			if a:p=l["icon"]=br(g,a,x,y,w,h)
		elif t=="travel":
			m=c.get("rm")
			if m in cQ:
				a=c1(cQ[m])
				if a:p=br(g,a,x,y,w,h)
			elif m in cP:p=a2(g,cP[m],0,*b9(ref,x,y,w,h,3))
			if p is not None:p.SetAlpha(.5)
			i=ak(c["v"]or "?",w-4);f.append(E(g,i,x+(w-I(i))//2,y+d+(h-d-14)//2-1));j=True
		elif t=="ability":
			a,i=ek(c["v"])
			if a:p=br(g,a,x,y,w,h)
			elif i:f.extend(a3(g,i,x,y+d,w,h-d));j=True
		elif t=="ui":
			k=aT(c["v"])
			if k and k[2]:p=a2(g,k[2],0,*b9(ref,x,y,w,h,2))
		elif t=="script":
			n=du(au(c)).strip().lower();a=bX.get(n)if n else None
			if a and aC(a)[0]>0:p=br(g,a,x,y,w,h)
		if p is not None:j=True;f.append(p)
		if t and not j:f.extend(a3(g,au(c),x,y+d,w,h-d))
		e["cells"][ref]=dw(g,l,f,t in("item","spell","ability","script","skill","travel"),c["k"]if b["keys"]and t else "",aV(ref),("click","menu",ref));a_[0]=None
	def dw(g,info,parts,counted,k,tip,click):
		x,y,w,h=info["x"],info["y"],info["w"],info["h"]
		if counted:info["count"]=E(g,"",x+w-6,y+h-16);info["txt"],info["hue"]="",S;parts.append(info["count"])
		if k:a=ak(c5(k),w-4);info["key"]=E(g,a,x+w-2-I(a),y+1,D);parts.append(info["key"])
		info["tip"]=tip;info["catcher"]=aB(g,x,y,w,h,eV(*click),tip);parts.append(info["catcher"]);eW(info["catcher"],B(click[1:]));info["parts"]=parts;return info
	def ca(i):
		c,e=aH(i),b["bagmode"];f=(e==0 and a["ub_state"])and("Show the Bags window"if a["ub_state"]!="open"else "Fold the Bags window into the bar")
		if e==1:d=("Open %s\nRight-click: pick another bag, or clear the slot"%c["n"]if c else "Empty: click, then target a bag for it")
		elif f:d=f+"\n%sRight-click: the Bags settings"%(c["n"]+"   "if c else "")
		else:d="Open %s"%c["n"]if c else "No bag here"
		g=af()[i]
		if g:d+="  [%s]"%g
		return d
	def eX(g,i,x,y,w,h):V(g,ao,x,y,w,h,ap);dx(g,i,x,y,w,h)
	def dx(g,i,x,y,w,h):a=aH(i);c={"x":x,"y":y,"w":w,"h":h,"count":None};d=[a2(g,a["g"],a["h"],x+3,y+3,w-6,h-6)]if a and a["g"]else[];e["bags"][i]=dw(g,c,d,a,af()[i]if b["keys"]else "",ca(i),("bag","bagmenu",i))
	def aM(refs):a["redraw"].update(refs)
	def eY(ref):
		g=e["g"];f=ref[0]=="b";a,k=(e["bags"].get(ref[1]),af()[ref[1]])if f else(e["cells"].get(ref),A(ref)["k"])
		if a is None or not H(g):return
		d=ak(c5(k),a["w"]-4)if(b["keys"]and k and(f or A(ref)["t"]))else "";c=a.get("key")
		if d and c is None:c=E(g,d,a["x"]+a["w"]-2-I(d),a["y"]+1,D);c.SetAcceptMouseInput(False);a["key"]=c;a.setdefault("parts",[]).append(c)
		elif c is not None:c.Text=d
		bt(a,ca(ref[1])if f else aV(ref))
	def bt(info,tip):
		c=info.get("catcher")
		if c is not None and info.get("tip")!=tip:info["tip"]=tip;am(c,tip)
	def dy():
		if not H(e["g"]):return
		for b,a in list(e["cells"].items()):
			c=A(b)
			if(c["t"]=="ui"and(c["v"]in("spellbook","virtue")or c["v"].startswith("mod:"))or c["t"]=="travel"):bt(a,aV(b))
		for i,a in list(e["bags"].items()):bt(a,ca(i))
	def bu(a,hue,tip):
		for b in a["text"]:b.Hue=hue
		am(a.get("catcher"),tip)
	def dz():
		a=e.get("keybtn")
		if a and H(e["g"]):bu(a,*dB())
	def dA():
		if not H(e["g"]):return
		a=e.get("traybtn")
		if a:
			n=len(bm());c=aa if n else D
			for b in a.get("text",[]):aD(b,str(n),c);bM(b,a["x"]+(a["w"]-cJ(str(n)))//2,a["ly"])
			am(a.get("catcher"),dC(n))
		dJ()
	bv=(("up","Next page of the bottom-left cells (page %d of %d showing)"),("dn","Previous page of the bottom-left cells (page %d of %d showing)"),("catcher","Page %d of %d of the bottom-left cells; click for the next page"))
	def eZ(g,store,x,d,ph,m):p=b["page"];c,a=aC(bD[0]);c,a=c or 16,a or 16;n=x+(m-c)//2;f,h=R(n,d+1,c,a)[:2];q=ab(g,store,"pgup",bD,f,h,None,bv[0][1]%(p+1,ad),on_click=B(("page",1)));f,h=R(n,d+ph-a-1,c,a)[:2];r=ab(g,store,"pgdn",aP,f,h,None,bv[1][1]%(p+1,ad),on_click=B(("page",-1)));o=str(p+1);i,j,k,l=R(x,d+a+1,m,max(1,ph-2*a-2));s=E(g,o,i+(k-I(o))//2,j+(l-14)//2,aa);t=aB(g,i,j,k,l,B(("page",1)),bv[2][1]%(p+1,ad));e["pagecol"]={"up":q,"dn":r,"num":s,"catcher":t,"rect":(i,j,k,l),"page":p}
	def e_():
		a=e.get("pagecol");p=b["page"]
		if not a or a["page"]==p or not H(e["g"]):return
		a["page"]=p;c=str(p+1);f,g,h,i=a["rect"];d=a["num"];aD(d,c);bM(d,f+(h-I(c))//2,g+(i-14)//2)
		for k,j in bv:am(a[k],j%(p+1,ad))
	def e0(g,key,d,x,y,w,h):
		V(g,ao,x,y,w,h,ap);a=safe(d.get("state"));b=d.get("title")or key;e=0 if a=="open"else D;c=d.get("icon")or 0;f=c and a2(g,c,e,x+2,y+2,w-4,h-4)is not None
		if not f:a3(g,b[:3].upper(),x,y,w,h,S if a=="open"else D)
		i=("%s is off; click to turn it on"if a is None else "Fold %s into the bar"if a=="open"else "Show %s")%b;aB(g,x,y,w,h,B(("dock",key)),i)
	def e1(g,box,a,fn,hue,tip):x,y,w,h=box;V(g,ao,x,y,w,h,ap);return{"text":a3(g,a,x,y,w,max(16,h),hue),"catcher":aB(g,x,y,w,h,fn,tip)}
	def dB():
		if a["bind"]is not None:return aa,"Keybind mode on: hover a cell, press a key; Esc or a click here ends it"
		return S,"Start keybind mode: hover a cell and press a key to bind it"
	def dC(n):return "%s folded into the bar; click to %s the tray"%(Kit.count(n,"window"),"hide"if b["tray_open"]else "show")
	def e2(g,store,L):
		c,h=L["m"],L["cw"];x=c+L["inner"]+L["sgc"];l=L["rowy"][-1]+L["rowh"][-1];d,f=aC(aP[0]);d,f=d or 16,f or 16;m=c+2+f+4;n=c+l-m;j=ds();z=(("Keys",B(("bind",)),dB()),("Lock",B(("lockbar",)),cb()),("Grid",B(("grid",)),dD()))
		if aL()and n>=66 and h-4>=j:p,r=R(x+(h-d)//2,c+2,d,f)[:2];A,s=h-4,min(28,(n-8)//3);t=[R(x+2,m+at*(s+4),A,s)for at in range(3)]
		else:C,D,u,v=R(x,c,h,l);w=[(by,)+eS(by,u,v)for by in dt(not aL())];i,y,a,b=(next((dd for dd in w if dd[2]>=j and dd[3]>=be),None)or max(w,key=lambda o:min(o[2]-j,o[3]-be)));a,b=max(1,a),max(1,b);E=i*a+(i-1)*M;F=y*b+(y-1)*M;G=C+max(M,(u-E)//2);H=D+max(M,(v-F)//2);k=[(G+(f4%i)*(a+M),H+(f4//i)*(b+M),a,b)for f4 in range(4)];p,r=k[0][0]+(a-d)//2,k[0][1]+(b-f)//2;t=k[1:]
		if not ac(q):ab(g,store,"min",aP,p,r,None,"Minimize the bar",on_click=B(("toggle_min",)))
		e["keybtn"],e["lockbtn"],e["gridbtn"]=[e1(g,f8,f5,f6,*f7)for(f5,f6,f7),f8 in zip(z,t)]
	def dD():
		if HOST.grid_shown():return aa,"Hide the screen grid windows snap to"
		return D,"Show the screen grid; windows you let go snap to it, the corners, edge middles and centre"
	def e3():
		b=bool(HOST.grid_toggle());a=e.get("gridbtn")
		if a and H(e["g"]):bu(a,*dD())
		l("screen grid %s."%("shown"if b else "hidden"))
	def cb():
		if ct():
			if bC():return aa,"Lock every window in its zone"
			return D,"Unlock the layout to move windows between zones"
		if b["lock"]:return r,"Locked; click to unlock the bar"
		return D,"Lock the bar in place"
	def dE():
		g,a=e["g"],e.get("lockbtn")
		if not a or not H(g):return False
		g.CanMove=not b["lock"]and not cu(q);bu(a,*cb());e["arranging"]=bC();return True
	dF=("g","store","cells","bags","keybtn","lockbtn","gridbtn","traybtn","pagecol")
	def dG():
		b=dict((f,e.get(f))for f in dF);a=b["g"];x,y=(a.GetX(),a.GetY())if H(a)else(None,None);e.setdefault("stale",[]).append(a);e.update(dict.fromkeys(dF[4:]),g=None,cells={},bags={});d=({},{});a_[0]=None;c={"g":None}
		try:e4(x,y,d,c)
		except Exception:
			if e["g"]is None:T(c["g"]);e.update(b);a_[0]=None;e["stale"]=[g for g in e.get("stale",[])if g is not a]
			else:
				for s in e.pop("stale",[]):T(s)
			raise
	def e4(x,y,store,built):
		H=cu(q);I=a["em"]=bool(a["minimized"])and not ac(q)
		if I:
			w,h=cW,cX
			if x is None:x,y=cE(bO,(200,600),(w,h))
			g=built["g"]=G.CreateGump(True,not H);Kit.mini_bar(g,store,w,h,aS,q,B(("toggle_min",)),"%s: page %d"%(aS,b["page"]+1))
		else:
			eO();L=b7();w,h=bq();z["off"]=(0,0);k=b5()
			if k is not None:z["off"]=(max(0,(k[0]-w)//2),max(0,(k[1]-h)//2));w,h=max(w,k[0]),max(h,k[1])
			if x is None:x,y=cE(bO,(200,600),(w,h))
			o,K,l=L["m"],L["pw"],L["p4"];v,A,X=L["ug"],L["bg"],L["tb"];C,p,s=L["sgx"],L["colx"],L["colw"];M,N,O,P=L["rowy"],L["rowh"],L["celly"],L["cellh"];j=o+K;g=built["g"]=G.CreateGump(True,not b["lock"]and not H);bF(g,w,h,corners=False);r=0
			for Y,Z in([("x",at*u)for at in range(b["extra"]-1,-1,-1)]+([("a",0)]if b["top"]else[])):
				c=o+M[r];aQ(g,*R(j,c,L["top_w"],N[r]));d,m=c+O[r],P[r]
				for i in range(u):b8(g,(Y,Z+i),*R(j+p[i],d,s[i],m))
				bs(g,[j+by for by in p],s,d,m);r+=1
			c,f=o+M[r],N[r];d,m=c+O[r],P[r];eZ(g,store,o,c,f,K);aQ(g,*R(j,c,L["left_w"],f))
			for i in range(W):b8(g,("a",u+i),*R(j+p[i],d,s[i],m))
			bs(g,[j+dd for dd in p[:W]],s,d,m);t=j+L["left_w"]+C;aQ(g,*R(t,c,L["ui_w"],f));V(g,cB,*R(t+l,c+l,L["ui_w"]-2*l,f-2*l),alpha=.55);D=F*L["bw"]+(F-1)*v;n=t+(L["ui_w"]-D)//2
			for i in range(F):b8(g,("u",i),*R(n+i*(L["bw"]+v),c+(f-L["bh"])//2,L["bw"],L["bh"]))
			bs(g,[n+fn*(L["bw"]+v)for fn in range(F)],(L["bw"],)*F,c+(f-L["bh"])//2,L["bh"]);E=t+L["ui_w"]+C;aQ(g,*R(E,c,L["bag_w"],f));D=J*L["bgw"]+(J-1)*A;n=E+(L["bag_w"]-D)//2
			for i in range(J):eX(g,i,*R(n+i*(L["bgw"]+A),d,L["bgw"],L["bgh"]))
			bs(g,[n+f4*(L["bgw"]+A)for f4 in range(J)],(L["bgw"],)*J,d,L["bgh"]);Q=E+L["bag_w"]+C;aQ(g,*R(Q,c,L["tray_w"],f));e5(g,*R(Q+l,d,X,L["bgh"]));e2(g,store,L)
		if b["anchor"]and not ac(q):
			S,ay=cD(b["anchor"],w,h)
			if S is not None:x,y=S,ay
		a["last_pos"]=Kit.show_window(g,x,y,w,h,None,False,eM(g),aX,e,{"g":g,"store":store});a["moved_at"]=None
		for aa in e.pop("stale",[]):T(aa)
		if not I and time.time()-a.get("counted_at",0.)>bQ:
			U=aY()
			if "item"in U["types"]or U["extra"]:aZ()
		a0();dJ()
	def e5(g,x,y,w,h):n=len(bm());V(g,ao,x,y,w,h,ap);a=a3(g,str(n),x,y,w,h,aa if n else D);e["traybtn"]={"text":a,"x":x,"w":w,"ly":y+(h-14)//2-1,"catcher":aB(g,x,y,w,h,B(("traywin",)),dC(n))}
	def dH(w,h,at=None,rect=False):
		if rect is False:
			g=e["g"]
			if not H(g):return 300,300
			rect=Kit.rect(g)
			if at is None:at=aR(g)or(0,0)
		a,b=at;f,d=(rect[2],rect[3])if rect is not None and rect[2]>0 else bq();W,c=bK()
		if aL():
			x,y=a+f+aj,b+d-h
			if W and x+w>W:
				x=a-aj-w
				if x<0:
					x,y=a,b+d+aj
					if c and y+h>c:y=b-aj-h
		else:
			x,y=a,b+d+aj
			if c and y+h>c:
				y=b-aj-h
				if y<0:
					x,y=a+f+aj,b
					if W and x+w>W:x=a-aj-w
		return x,y
	def e6():return e["g"]
	f3=None
	def e7():
		d,a["redraw"]=a["redraw"],set();g=e["g"]
		if not d or a["em"]or not H(g):return
		for c in sorted(d):
			f=c[0]=="b";b=e["bags"].get(c[1])if f else e["cells"].get(c)
			if b is None:continue
			for p in b.get("parts")or():T(p)
			if f:dx(g,c[1],b["x"],b["y"],b["w"],b["h"])
			else:dv(g,c,b["x"],b["y"],b["w"],b["h"])
		a0()
	def dI():
		g=e["g"]
		if not b["anchor"]or not H(g)or ac(q):return
		w,h=bq();x,y=cD(b["anchor"],w,h)
		if x is None:return
		if(x,y)!=a.get("last_pos"):g.SetPos(x,y);Kit.note_rect(g,x,y);cG(g);a["last_pos"]=(x,y);dK()
	def e8(x,y):
		if a["em"]:return
		if ac(q):return
		w,h=bq();c=Kit.anchor_at(x,y,w,h,SNAP_ANCHOR);d=True if c in("L","R")else False if c in("T","B")else None;e=d is not None and d!=b["vertical"]
		if c!=b["anchor"]or e:
			b["anchor"]=c
			if e:b["vertical"]=d;ag();al();l("standing %s along the %s edge."%("upright"if d else "flat",{"L":"left","R":"right","T":"top","B":"bottom"}[c]));return
			ag()
		dI();aX()
	def e9(now):
		g=e["g"]
		if not H(g):return
		d=Kit.rect(g);c=(d[0],d[1])if d else(0,0)
		if c!=a.get("last_pos"):a["last_pos"],a["moved_at"]=c,now
		elif a.get("moved_at")is not None and now-a["moved_at"]>=.3 and SNAP.pressed()is not True:a["moved_at"]=None;e8(c[0],c[1])
		dK(c,d)
		if b["anchor"]and now>=a.get("screen_next",0.):
			a["screen_next"]=now+2.;f=bK()
			if f!=a.get("screen_wh"):
				a["screen_wh"]=f
				if not ac(q):dI()
	def dJ():
		k,Y["g"]=Y["g"],None;d=bm()
		if a["em"]or not b["tray_open"]or not d:T(k);return
		L=b7();f,l,m=L["tb"],L["bg"],max(4,L["tm"]//2);c,i=aC(aP[0]);c,i=c or 16,i or 16;j=L["bgh"];w=m+len(d)*(f+l)+c+m;h=m+j+m;g=G.CreateGump(True,False);bF(g,w,h,corners=False)
		for n,(o,p)in enumerate(d):e0(g,o,p,m+n*(f+l),m,f,j)
		q=({},{});ab(g,q,"fold",aP,w-m-c,m+(j-i)//2,None,"Hide the tray (the bar's numbered button brings it back)",on_click=B(("traywin",)));x,y=dH(w,h);Kit.place(g,x,y,w,h);Y.update({"g":g,"at":(x,y),"w":w,"h":h});G.AddGump(g);Kit.attach(g,e["g"]);T(k)
	def dK(at=None,rect=False):
		g=Y["g"]
		if not H(g):return
		w,h=Y.get("w",0),Y.get("h",0);x,y=dH(w,h,at,rect)
		if(x,y)!=Y["at"]:Y["at"]=(x,y);g.SetPos(*Kit.clamp(x,y,w,h));cG(g)
	def fa():
		aZ(cY);b=(next((c for c in(a["first_g"].get(d)for d in cY)if c),None)or API.FindLayer("Spellbook"))
		if b:API.UseObject(b);return True
		l("no spellbook in your pack.",r);return False
	def dL():
		if ct():HOST.layout_arrange();dE();return
		b["lock"]=not b["lock"];ag()
		if not dE():al()
		if U.f is not None:U.f.c["lock"].IsChecked=b["lock"]
		else:aA(q)
		l("%s."%("locked"if b["lock"]else "unlocked"),Q)
	def fb():
		g=e["g"];b=cF();c=aR(g)if H(g)else None
		if b is None or c is None:return
		d,f=b[0]-c[0],b[1]-c[1]
		for h,a in(list(e["cells"].items())+[(("b",k),m)for k,m in e["bags"].items()]):
			if a["x"]<=d<a["x"]+a["w"]and a["y"]<=f<a["y"]+a["h"]:return h
		return
	def cc(ref=None):HOST.release_typing();a["bind"]={"sel":ref};dz();l("keybind mode on: %s (Esc ends it, Backspace clears a key)."%("click a cell, then press a key"if cF()is None else "hover a cell and press a key"))
	def dM():
		if a["bind"]is None:return
		a["bind"]=None;dz();l("keybind mode off.")
	def cd(ref,k):
		c=aq(k)
		if c:l("%s belongs to %s; pick another."%(k,c),r);return
		a=[ref]
		for b,d in ar():
			if b!=ref and _norm_key(d["k"])==k:d["k"]="";a.append(b);l("%s taken off %s."%(k,N(b)))
		for i,e in enumerate(af()):
			if("b",i)!=ref and e==k:bY(("b",i),"");a.append(("b",i));l("%s taken off bag slot %d."%(k,i+1))
		bY(ref,k)
		if ref[0]=="b":aW()
		az();dN(a);f=ref[0]!="b"and not A(ref)["t"];l("%s bound to %s%s."%(k,N(ref)," (empty; fill it to use it)"if f else ""),Q)
	def fc(d):
		c=a["bind"]
		if not c:return
		k=d.rsplit("+",1)[-1]
		if k=="ESCAPE":dM();return
		b=fb()or c["sel"]
		if b is None:l("hover a cell on the bar (or click one) first.");return
		c["sel"]=b
		if k in("BACKSPACE","DELETE"):bY(b,"");az();dN([b]);l("%s has no hotkey now."%N(b),Q);return
		cd(b,d)
	def dN(refs):
		for r in refs:eY(r)
		a=aU(K["sel"])
		if U.f is not None and a in refs:U.f.c["key"].SetText(A(a)["k"])
	dO={"barsettings":lambda:a6(q),"lock":lambda:dL(),"minimize":lambda:B(("toggle_min",))(),"war":lambda:API.SetWarMode(not bool(API.Player.InWarMode)),"help":lambda:API.OpenHelp(),"quests":lambda:API.OpenQuestLog()}
	def ce(uid):
		d=aT(uid)
		if d is None:l("unknown window button '%s'."%uid,r);return False
		a=d[3];b=True
		if a in dO:dO[a]()
		elif a=="grimoire":return ey()
		elif a=="virtue":return ez()
		elif a=="paperdoll":
			import System
			if not ClientUI.game_action("OpenPaperdoll",[System.UInt32(int(API.Player.Serial))]):
				if aO():ae(lambda:ce("paperdoll"))
				else:b=safe(lambda:API.ContextMenu(API.Player,"Open Paperdoll",2),None)is not False
		elif a.startswith("mod:"):return em(a[4:])
		elif a.startswith("ga:"):c=a.split(":");b=ClientUI.game_action(c[1],reuse=c[2]if len(c)>2 else None)
		elif a.startswith("macro:"):b=ClientUI.open_macro(a[6:])
		if not b:l("couldn't open %s (%s)."%(d[1],ClientUI.error or "unknown"),r)
		return b
	ax={"looked":False,"type":None}
	def cf():
		if not ax["looked"]and aO():
			if not ax.get("asked"):ax["asked"]=True;ae(cf)
			return[]
		if not ax["looked"]:ax["looked"]=True;ax["type"]=a5("ClassicUO.LegionScripting.LegionScripting")
		t=ax["type"]
		if t is None:return[]
		c=[]
		def a(a,n):return str(safe(lambda:ClientUI._get(a,n),"")or "")
		with Kit.quiet:
			for b in(ClientUI._get(None,"LoadedScripts",t)or[]):
				d,e=a(b,"RelativePath")or a(b,"FileName"),a(b,"FullPath")
				if d or e:c.append((d,e))
		return c
	dP={};cg=set()
	def ch(v):
		v=str(v or "").strip().replace("\\","/");b=dP.get(v)
		if b is not None and time.time()<b[0]:return list(b[1])
		f=v.split("/")[-1];k,l=v.lower(),f.lower();d=[]
		def a(c):
			if c and c not in d:d.append(c)
		m=not aO()
		if not m:
			if v not in cg:
				cg.add(v)
				def n():cg.discard(v);ch(v)
				ae(n)
			if b is not None:return list(b[1])
		if "/"in v:a(v)
		for e,q in cf():
			r=e.replace("\\","/");g=r.lower()
			if g==k or g.endswith("/"+k)or g.split("/")[-1]==l:a(r)
		if not m:a(v);a(f);return list(d)
		h=dW()
		if h:
			with Kit.quiet:
				for o,i,p in os.walk(h):
					e=o.replace("\\","/")[len(h):].strip("/")
					if e.count("/")>=2:i[:]=[]
					i[:]=[s for s in i if not s.startswith(".")and s.lower()not in ck]
					for j in p:
						if j.lower()==l:a((e+"/"+j)if e else j)
		a(v);a(f);dP[v]=(time.time()+60.,d);return list(d)
	bw={}
	def bx(v):
		b=ch(v);a=bw.get(v)
		if a is not None and a in b:
			try:
				if API.IsScriptRunning(a):return True
			except Exception:pass
		for c in b:
			if c==a:continue
			try:
				if API.IsScriptRunning(c):
					if len(bw)>200:bw.clear()
					bw[v]=c;return True
			except Exception:pass
		return False
	def fd(v):
		e=ch(v);b=bx(v);f=API.StopScript if b else API.PlayScript;d=False
		for g in e:
			if not safe(lambda c=g:(f(c),True)[1],False):continue
			d=True
			if not HOST.idle(.1)or bx(v)!=b:break
		a["script_check"]=(v,b,time.time()+.5);return d
	def fe(now):
		b=a.get("script_check")
		if not b or now<b[2]:return
		a["script_check"]=None;v,c,f=b;e=bx(v);d=v.replace("\\","/").split("/")[-1]
		if c and not e:l("stopped %s."%d)
		elif not c and e:l("started %s."%d,Q)
		elif not c:l("%s didn't start; is it in the Legion Script Manager's list (refresh it)?"%d,r)
		a0()
	def ff(c):
		def e():return a["first"].get((c["g"],c["h"]))or(None if b["hue"]else a["first_g"].get(c["g"]))
		f=time.time()-a.get("counted_at",0.)>bQ
		if f:aZ()
		d=e()
		if not d and not f:aZ();d=e()
		if not d:l("no %s left."%au(c),r);return False
		API.UseObject(d);a["next_count"]=time.time()+.4;HOST.pack_dirty();return True
	dQ={"spell":API.CastSpell,"skill":API.UseSkill,"dress":API.Dress,"undress":API.Undress,"say":API.Msg};fg=("stealing","snooping","discordance","provocation")
	def dR(c,t,v):
		if t=="skill":n=v.lower();return bool(n)and any(n in d for d in fg)
		if t=="spell":n=v.lower();return bool(n)and(n in cO or any(f.startswith(n)for f in cO))
		return t=="item"and int(c.get("g")or 0)==3853
	def fh(a,c,t,v):
		if c["tg"]!="last"or not dR(c,t,v):return False
		return not HOST.harm_ok(int(API.LastTargetSerial or 0),("actionbar",)+a,aS,True,"press again to confirm",t=="skill")
	def dS(ref):
		c=A(ref);t,v=c["t"],c["v"].strip()
		if not t:l("%s is empty."%N(ref));return
		m=time.time();e=(ref,b["page"])
		if fh(e,c,t,v):return
		h=c["tg"]in("self","last")and t not in("travel","say","ui","dress","undress","ability");w=a["want_target"]
		if w and m>w[1]:w=None
		i=bool(w)and w[2]==e;j=False
		if w and not i:a4();j=h
		d=True;n=bool(API.HasTarget("any"))
		try:
			if t in dQ:dQ[t](v)
			elif t=="item":d=ff(c)
			elif t=="macro":
				f=ClientUI.run_macro(v);d=bool(f)
				if f is None:l("no TazUO macro named '%s'."%v,r)
				elif not f:l("couldn't run macro '%s' (%s)."%(v,ClientUI.error or "unknown"),r)
			elif t=="ability":API.ToggleAbility(v or "primary")
			elif t=="script":
				def o():
					try:fd(v)
					except Exception as a:l("couldn't use %s (%s)."%(au(c),a),r)
				ae(o)
			elif t=="ui":d=ce(v)
			elif t=="travel":d=eF(c)
		except Exception as p:l("couldn't use %s (%s)."%(au(c),p),r);d=False
		if d and t in("skill","spell"):eI(t,v)
		if d and h and not i:
			if j:l("a target was still pending; target by hand.")
			elif n:l("a target cursor was already up; target by hand.")
			elif cq(q):l("another module is using the target cursor; target by hand.")
			else:
				g=2.5
				if t=="spell":k=bL(v);g+=k[3]if k else 0.
				HOST.claim_cursor(q,g);a["want_target"]=(c["tg"],time.time()+g,e,dR(c,t,v),int(API.LastTargetSerial or 0))
	def fi(now):
		w=a["want_target"]
		if not w:return
		c,d=w[0],w[1]
		if now>d:a4();return
		if not API.HasTarget("any"):return
		a4()
		if cq(q):return
		if API.HasTarget("beneficial"if w[3]else "harmful"):l("that cursor isn't this cell's; target by hand.");return
		if c=="self":API.TargetSelf()
		else:
			b=w[4]if w[3]else int(API.LastTargetSerial or 0)
			if b:API.Target(b)
			else:l("no last target yet; target by hand.")
	def a4():a["want_target"]=None;HOST.release_cursor(q)
	def dT(action):
		a4()
		def a(serial):B.add(tuple(action)+(int(serial or 0),),dup=True)
		HOST.pick_target(15,a)
	def ci(ref):l("target an item for %s (Esc to cancel)."%N(ref));dT(("picked_item",ref,b["page"]))
	def fj(ref,pg,serial):
		if a["shutting"]or cp():return
		c=bH(serial)
		if c is None:l("no item picked.");return
		e,i=int(c.Graphic or 0),int(c.Hue or 0);f=str(c.Name or "")or("0x%04X"%e);g=N(ref);h=[ref]
		if ref[0]=="a"and ref[1]>=u and pg!=b["page"]and C["pages"]:d=C["pages"][pg][ref[1]-u];g="page %d cell %d"%(pg+1,ref[1]-u+1);h=[]
		else:d=A(ref)
		d.update({"t":"item","v":"","g":e,"h":i,"n":f})
		for k in bW:d.pop(k,None)
		aw(recount=True,refs=h);l("%s set on %s."%(f,g),Q)
	def dU(i):l("target a bag for bag slot %d (Esc to cancel)."%(i+1));dT(("picked_bag",i))
	def fk(i,serial):
		if a["shutting"]or cp():return
		b=bH(serial)
		if b is None or not b.IsContainer:l("that isn't a bag.",r);return
		df(i,serial);a["next_scan"]=0.
	def fl(ref):
		if a["bind"]is not None:a["bind"]["sel"]=ref;l("%s; now press a key or combination for it."%N(ref))
		elif A(ref)["t"]:dS(ref)
		elif ref[0]in("a","x"):ci(ref)
		else:cm(ref)
	def cj(i):
		if a["bind"]is not None:a["bind"]["sel"]=("b",i);l("bag slot %d; now press a key or combination for it."%(i+1));return
		c=aH(i)
		if b["bagmode"]==1 and c is None:dU(i);return
		if b["bagmode"]==0:
			d=aG()
			if d in("collapsed","docked"):b1("show");ah()
			elif d=="open":ah();b1("dock")
			else:e=c["s"]if c else None;bn(aF,"Bags",(lambda:API.UseObject(e))if e else None)
		elif c is None:l("no bag in that slot (see Bag slots on the Action Bar settings page).")
		else:API.UseObject(c["s"])
	dV=[("item","Item...")]+[(ga,dict(bV)[ga])for ga in "spell skill ability ui macro script dress undress say travel".split()];fm=dict(dV+[("hotkey","Hotkey"),("lo","Red at")]);bz={"macro":"TazUO macros","script":"Legion scripts","dress":"Dress outfits","undress":"Dress outfits"}
	def dW():a=Kit.script_dir().replace("\\","/").rstrip("/");b=os.path.dirname(a);return b if b and b!=a else a
	ck=("iplib","lib","libs","library","site-packages","dlls","stubs","__pycache__","api","docs","examples","virtueassistantmodules")
	def fo():
		b=dW();h=b.lower();c=[]
		for i,j in cf():
			p=j.replace("\\","/");a=(p[len(b):].strip("/")if b and p.lower().startswith(h)else(p or i));g=a.lower().split("/")
			if any(m in ck for m in g[:-1])or g[-1].startswith("_"):continue
			if a and a not in c:c.append(a)
		if c or not b:return sorted(c,key=lambda s:s.lower())
		with Kit.quiet:
			for k,d,e in os.walk(b):
				a=k.replace("\\","/")[len(b):].strip("/")
				if a.count("/")>=2 or "__init__.py"in e:
					d[:]=[]
					if "__init__.py"in e:continue
				d[:]=[n for n in d if not n.startswith(".")and n.lower()not in ck]
				for f in e:
					if f.lower().endswith(".py")and not f.startswith("_"):c.append((a+"/"+f)if a else f)
		return sorted(c,key=lambda s:s.lower())
	def dX(cat):
		if cat=="macro":return ClientUI.macro_names()
		if cat=="script":return fo()
		return list(API.GetAvailableDressOutfits()or[])
	cl={"macro":"The name of a macro from TazUO's macro window","script":"The script's file name (heal.py, or Spells/Bless.py)","dress":"An outfit name from TazUO's dress agent","undress":"An outfit name from TazUO's dress agent","say":"The text to say in game","hotkey":"A key or combination (F5, CTRL+Q, SHIFT+F2; blank = none)","lo":"The counter turns red at this many or fewer (0 = only when none)"}
	def fp(info):a=aR(e["g"])if H(e["g"])and info is not None else None;return None if a is None else(a[0]+info["x"],a[1]+info["y"],info["w"],info["h"])
	def fq(w,h):
		a=j.get("anchor")
		if j.get("moved")is not None:x,y=j["moved"]
		elif a is None:x,y=300,300
		else:c,b,e,d=a;x,y=c,b+d+2
		W,H=bK()
		if W and H:
			if a is not None and j.get("moved")is None and y+h>H:y=b-2-h
			x,y=max(0,min(x,W-w)),max(0,min(y,H-h))
		return int(x),int(y)
	def ay():g,j["g"]=j["g"],None;j["c"]={};T(g)
	def fr(g):
		def a(*a):
			if j["g"]is g:j["g"]=None;j["c"]={}
		return a
	def cm(ref,bag=None):j.update({"ref":ref,"bag":bag,"level":"cats"if ref else "bag","cat":None,"page":0,"moved":None,"placed":None,"anchor":fp(e["cells"].get(ref)if ref else e["bags"].get(bag))});cn()
	def dY(rows):return[rows[c:c+bf*bU]for c in range(0,len(rows),bf*bU)]
	def fs():
		f,d=j["level"],j["cat"]
		if f=="bag":
			i=j["bag"];a=[]
			if b["bagmode"]==1:a+=[("Pick a bag...",("pickbag",i)),("Clear this slot",("clearbag",i))]
			elif b["bagmode"]==0:
				s=aG()
				if s in("collapsed","docked"):a.append(("Show the Bags window",("ub","show")))
				elif s=="open":a.append(("Fold the Bags window into the bar",("ub","dock")))
				else:a.append(("Turn Bags on",("ub","on")))
				if aF in HOST.by_key:a.append(("Bags settings",("ub","settings")))
			else:h=aH(i);a.append(("Open %s"%h["n"]if h else "No bag here",("bag",i)))
			a.append(("Hotkey: %s"%(af()[i]or "none"),("bagbind",i)));a.append(("Bag slots: "+bh[b["bagmode"]],("bagmode",None)));return a,None
		if f=="cats":
			g=A(j["ref"]);a=[(t,("cat",o))for o,t in dV];l={"self":"self","last":"last target"}.get(g["tg"],"none");a+=[("-",None),("Hotkey: %s"%(g["k"]or "none"),("cat","hotkey")),("Press a key for it",("bindsel",None)),("Then target: %s"%l,("target",None))]
			if g["t"]in("item","travel"):a.append(("Red at: %d or fewer"%max(0,g["lo"]),("cat","lo")))
			a+=[("Clear cell",("clear",None)),("More on the settings page",("settings",None))];return a,None
		if f=="method":return[(w,("tset",v))for v,w in eb],None
		if f=="list":
			if d=="spell":c=[[(y,("set",("spell",y)))for y in m.split("|")]for x,m in c_];e=ei
			elif d=="skill":c,e=[[(G,("set",("skill",G)))for G in eh]],["Skills"]
			elif d=="ability":c,e=[[("Primary ability",("set",("ability","primary"))),("Secondary ability",("set",("ability","secondary")))]],["Weapon ability"]
			elif d=="travel":
				if HOST.services.get("grimoire.destinations")is None:a=[("Grimoire is off: click to turn it on",("grimon",None))]
				elif not j["items"]:a=[("No runebook read yet: open Grimoire's runebook tabs",("none",None))]
				else:a=[(ak("%s  (%s)"%(L["name"],L["book_name"]),260),("tdest",at))for at,L in enumerate(j["items"])]
				c=dY(a);e=["Runebook destinations"]*len(c)
			elif d in bz:
				a=[(ak(by,220),("set",(d,by)))for by in j["items"]]
				if not a:a=[("Nothing saved in TazUO yet",("none",None))]
				a.append(("Type a name",("typed",d)));c=dY(a);e=[bz[d]]*len(c)
			else:
				c=[[(n[1],("set",("ui",n[0])))for n in bS]];e=["Client windows"];k=[(dd[1],("set",("ui",dd[0])))for dd in c3()]
				if k:c.append(k);e.append("Module windows")
			p=max(0,min(len(c)-1,j["page"]));j["page"]=p;return c[p],(e[p],p,len(c))
		return[],None
	def cn():cH(ft)
	def ft():
		n=j["g"];o=aR(n)if H(n)else None
		if o is not None and j.get("placed")is not None and o!=j["placed"]:j["moved"]=o
		j["g"],j["stale"]=None,n;e,p=({},{}),{};M,v=Kit.MARGIN,Kit.GAP;f,q=fs();b,c=j["level"],j["ref"]
		if b=="bag":h="BAG SLOT %d"%(j["bag"]+1)
		elif b=="method":h="TRAVEL TO %s"%str((j.get("dest")or{}).get("name","?")).upper()
		elif b in("list","text"):i=fm.get(j["cat"],"Hotkey");h="%s: %s"%(N(c).upper(),i.replace("...","").upper())
		else:h="SET "+N(c).upper()
		z=I(h)+60
		if b=="text":w=max(z,340);k=92
		else:r=max(1,min(bU,(len(f)+bf-1)//bf));C=(len(f)+r-1)//r if f else 1;l=max([I(at[0])for at in f]+[100])+24;w=max(z,2*M+16+r*l);k=10+C*bg+(34 if q else 10)
		s=w-2*M;t=M+30+v+k+M;g=G.CreateGump(True,True);bF(g,w,t,corners=False);cC(g,M,M,s,30);E(g,h,M+10,M+7,aa);ab(g,e,"close",cy,w-M-34,M+4,None,"Close the menu",on_click=B(("mpick","close",None)))
		if b not in("cats","bag"):ab(g,e,"back",bD,w-M-54,M+7,None,"Back to the previous menu",on_click=B(("mpick","back",None)))
		a=M+30+v;cC(g,M,a,s,k)
		if b=="text":
			m=A(c)
			if j["cat"]=="lo":F=str(max(0,m["lo"]))
			else:F=m["k"]if j["cat"]=="hotkey"else(m["v"]if m["t"]==j["cat"]else "")
			E(g,cl.get(j["cat"],""),M+10,a+8,D);p["text"]=bE(g,F,M+10,a+32,s-20,numbers=False);ab(g,e,"ok",cz,M+10,a+62,"Apply","Save this value on the cell",on_click=B(("mpick","text",None)));p["status"]=E(g,"",M+10+35+I("Apply")+12,a+65,D)
		else:
			for K,(i,d)in enumerate(f):
				L,O=divmod(K,C);x=M+8+L*l;y=a+6+O*bg
				if d is None:V(g,cB,x,y+bg//2,l-16,1);continue
				P=d[0]=="set"and(A(c)["t"],A(c)["v"])==d[1]or d[0]in("tdest","tset")and fu(c,d);E(g,i,x+4,y+2,Q if P else S);aB(g,x,y,l-8,bg,B(("mpick",)+tuple(d)),i)
			if q:
				R,U,J=q;u=a+k-28;E(g,"%s  (%d of %d)"%(R,U+1,J),M+10,u+4,D)
				if J>1:ab(g,e,"next",a7,w-M-44,u,None,"Next page",on_click=B(("mpick","page",1)));ab(g,e,"prev",a7,w-M-84,u,None,"Previous page",on_click=B(("mpick","page",-1)))
		x,y=fq(w,t);x,y=Kit.place(g,x,y,w,t);j.update({"g":g,"c":p,"placed":(x,y)});G.AddControlOnDisposed(g,fr(g));G.AddGump(g);g.SetInScreen();T(j.pop("stale",None))
	def dZ(ref,t,v):a=A(ref);b=dict(Z(),t=t,v=v,k=a["k"],tg=a["tg"],lo=a["lo"]);C[ref[0]][ref[1]]=b;aw(recount=True,refs=[ref]);l("%s set on %s."%(au(b),N(ref)),Q)
	def fu(ref,action):
		c=A(ref)
		if c["t"]!="travel":return False
		if action[0]=="tdest":a=j["items"];d=a[action[1]]if 0<=action[1]<len(a)else None
		else:
			d=j.get("dest")
			if c.get("rm")!=action[1]:return False
		if not d:return False
		try:return(int(c.get("rb")or "0",16)==int(d["book"])and c.get("ri")==str(int(d["index"])))
		except(ValueError,TypeError,KeyError):return False
	def ai(**a):j.update(a);cn()
	def fv(what,a):
		b=j["ref"]
		if what in("close","bindsel","bagbind","set","settings","pickbag","clearbag","ub","bag","bagmode","tset","grimon")or(what,a)==("cat","item"):ay()
		if what in d_:d_[what](b,a)
	def fw(ref,a):
		if j["level"]=="method":ai(level="list",cat="travel")
		else:ai(level="cats",cat=None,page=0)
	def fx(ref,a):
		if a=="travel":b=HOST.services.get("grimoire.destinations");ai(items=list(safe(b,[])or[])if b is not None else[],level="list",cat="travel",page=0);return
		if a=="item":ci(ref);return
		if a in bz and aO():
			def c():
				b=dX(a)
				if j["ref"]==ref and j["level"]=="cats"and H(j["g"]):ai(items=b,level="list",cat=a,page=0)
			ae(c);return
		if a in("spell","skill","ability","ui","macro","script","dress","undress"):ai(items=dX(a)if a in bz else[],level="list",cat=a,page=0);return
		ai(level="text",cat=a)
	def fy(ref,a):
		if j["level"]=="list"and j["cat"]=="travel"and 0<=a<len(j["items"]):ai(level="method",dest=j["items"][a])
	def fz(ref,a):
		if j.get("dest")and ref is not None:eG(ref,j["dest"],a)
	def fA(ref,c):
		v=str(j["c"]["text"].Text or "").strip()
		if j["cat"]=="hotkey":
			k=_norm_key(v);a=aq(k)
			if a:aD(j["c"]["status"],"%s belongs to %s"%(k,a),r);return
			if k:cd(ref,k)
			else:A(ref)["k"]="";aw(refs=[ref])
			ay();return
		if j["cat"]=="lo":
			try:b=int(v)
			except ValueError:aD(j["c"]["status"],"Type a number",r);return
			A(ref)["lo"]=max(0,b);aw(refs=[ref]);ay();return
		if not v:aD(j["c"]["status"],"Type a value first",r)
		else:ay();dZ(ref,j["cat"],v)
	def fB(ref,a):c=A(ref);c["tg"]={"":"self","self":"last","last":""}.get(c["tg"],"");aW();aM([ref]);aA(q);cn()
	def fC(ref,a):dp(ref);ay()
	def fD(ref,a):K["sel"]=ep(ref);a6(q);aA(q)
	def fE(ref,b):df(b,0);a["next_scan"]=0.
	def fF(ref,a):
		if a=="settings":
			if aF in HOST.by_key:a6(aF)
		elif a=="on":bn(aF,"Bags")
		else:ah();b1(a)
	d_={"bindsel":lambda ref,a:cc(ref),"bagbind":lambda ref,a:cc(("b",a)),"set":lambda ref,a:dZ(ref,a[0],a[1]),"pickbag":lambda ref,a:dU(a),"bag":lambda ref,a:cj(a),"bagmode":lambda ref,a:a6(q),"grimon":lambda ref,a:bn(cS,"Grimoire"),"page":lambda ref,a:ai(page=j["page"]+a),"back":fw,"cat":fx,"tdest":fy,"tset":fz,"typed":lambda ref,a:ai(level="text",cat=a),"text":fA,"target":fB,"clear":fC,"settings":fD,"clearbag":fE,"ub":fF}
	def d0(ref):
		if ref[0]=="b":cj(ref[1])
		else:dS(ref)
	def fG(ref):
		try:d0(ref)
		except Exception as a:l("couldn't use %s (%s)."%(N(ref),a),r)
	O={"ok":None,"held":{},"map":{},"hooks":None}
	def fH(k):
		b,a=_norm_key(k).split("+"),None
		for p in b:
			if p and p not in("CTRL","SHIFT","ALT"):a=p if p.startswith("SDLK_")else "SDLK_"+p
		c=[d for d in("CTRL","SHIFT","ALT")if d in b];return "+".join(c+([a]if a else[]))
	def fI(a):return "+".join(c[5:]if c.startswith("SDLK_")else c for c in str(a).upper().split("+"))
	def fJ(ref):
		if ref[0]=="b":return(a["bind"]is None and aH(ref[1])is not None and(b["bagmode"]!=0 or a["ub_state"]is not None))
		c=A(ref)
		if c["t"]=="ui":d=aT(c["v"]);e=d[3]if d else "";return(e in("war","help","quests","paperdoll","lock","minimize")or e.startswith(("ga:","macro:")))
		return c["t"]in("item","spell","skill","ability","macro","say","dress","undress","travel")
	def fK(b):
		try:
			if not O["ok"]:return
			b=str(b);g=b.rsplit("+",1)[-1];f,c=time.time(),O["held"];h=c.get(g);c[g]=f
			if h is not None and f-h<cM:return
			if len(c)>32:
				for k in[i for i,m in c.items()if f-m>=cM]:del c[k]
			if a["shutting"]or e["g"]is None:return
			if a["bind"]is not None:
				if not cx():B.add(("bindkey",fI(b)),dup=True);HOST.poke()
				return
			d=O["map"].get(b)
			if d is None or cx():return
			if fJ(d):fG(d)
			else:B.add(("use",d),dup=True);HOST.poke()
		except Exception:pass
	def fL(a):
		try:O["held"].pop(str(a).rsplit("+",1)[-1],None)
		except Exception:pass
	def fM():
		if O["ok"]is not None:return
		O["ok"]=False
		try:
			import clr;import System;from System.Reflection import BindingFlags;d=BindingFlags.Static|BindingFlags.Public|BindingFlags.NonPublic;e=a5("ClassicUO.Input.Keyboard");a,b=e.GetEvent("KeyDownEvent",d),e.GetEvent("KeyUpEvent",d);c=clr.GetPythonType(a.EventHandlerType)(fK);f=clr.GetPythonType(b.EventHandlerType)(fL);a.GetAddMethod(True).Invoke(None,System.Array[object]([c]))
			try:b.GetAddMethod(True).Invoke(None,System.Array[object]([f]))
			except Exception:a.GetRemoveMethod(True).Invoke(None,System.Array[object]([c]));raise
			O.update({"hooks":(a,c,b,f),"ok":True,"held":{}})
		except Exception as g:l("couldn't read the keyboard, so cell hotkeys are off (%s)."%g,r)
	def fN():
		a,O["hooks"]=O["hooks"],None;O["ok"]=None if a else O["ok"];O["map"]={}
		if not a:return
		import System;b,c,d,e=a;safe(lambda:b.GetRemoveMethod(True).Invoke(None,System.Array[object]([c])));safe(lambda:d.GetRemoveMethod(True).Invoke(None,System.Array[object]([e])))
	co=set()
	def d1(what,text):
		if what not in co:co.add(what);l(text,r)
	def az():
		a={}
		for r,c in ar():
			k=_norm_key(c["k"])
			if not k or not c["t"]or not c7(r):continue
			b=aq(k)
			if b:d1((k,b),"%s belongs to %s; %s has no hotkey."%(k,b,N(r)));continue
			if k in a:d1((k,"two cells"),"%s is on two cells; %s gets it."%(k,N(r)))
			a[k]=r
		for i,k in enumerate(af()):
			if k and not aq(k):a[k]=("b",i)
		O["map"]=dict((fH(d),f)for d,f in a.items())if O["ok"]else{}
	d2={"click":fl,"use":d0,"bag":cj,"ui":ce,"pick":ci,"menu":cm,"mpick":fv,"picked_item":fj,"picked_bag":fk,"bindkey":fc,"lockbar":dL,"grid":e3,"bagmenu":lambda i:cm(None,i),"page":lambda step:ev(b["page"]+step),"bind":lambda:cc()if a["bind"]is None else dM()}
	def fO(w):a=(w-24)//3;b=bN("Value: a spell, skill, macro or outfit name, primary or secondary, a script file, text to say, or an item graphic (0x0E21, or 0x0E21,1153 with a hue).",w-24)[:3];return(("BAR",(("check","lock","Lock in place","Keep the bar where it is (unlocked: drag its stone edge)",{"stay":True}),("check","top","Show the top row","Show the 24-cell row above the bottom row",{"stay":True,"dx":12+a}),("check","keys","Show hotkeys","Show each cell's hotkey in its corner",{"dx":12+2*a}),("check","short","Short counts","Show 1200 as 1.2k on the counters",{"stay":True}),("check","hue","Count same hue only","Count only items of the cell's hue",{"stay":True,"dx":12+a}),("custom",28,fP),("slider","slot","Cell size:","Cell side in pixels (%d-%d)"%(ba,bb),ba,bb,{"sw":120,"vfmt":"%d px","stay":True}),("custom",26,fQ),("custom",26,fR),("slider","scale","Scale:","Size of the whole bar (%d-%d%%); text keeps its size"%(an,aE),an,aE,{"sw":160,"vfmt":"%d%%"}),("slider","extra","Extra rows:","Rows of %d cells above the top row (0-%d); hidden rows' hotkeys are off"%(u,bd),0,bd,{"sw":100,"vfmt":"%d","stay":True}),("custom",26,fS)),{"ldy":2,"sdy":6,"lgap":8,"ugap":10,"fh":26,"pad":6}),("EDIT A CELL",[("custom",128,fT)]+[("note",c)for c in b]),("HOW TO USE",[("note",f)for d in ej for f in bN(d,w-24)]))
	def d3(f,by,a):return Kit.buttons(f.g,f.store,f.x+12,by,a,16)
	def bA(f,lx,a,label,key,b,c,value,tooltip):E(f.g,label,lx,a+2);d=[g[0]for g in c];K["dds"].append((key,lx+I(label)+8,a,b,[h[1]for h in c],d.index(value)if value in d else 0,tooltip));return lx+I(label)+8+b+16
	def fP(f,x,y):b=a["ub_found"];c=aG();e=({"open":"Bags: shown","collapsed":"Bags: folded","docked":"Bags: in the bar"}.get(c)if c else "Bags: off"if b else "Bags: not found"if b is False else "Bags: not in use");b=b or c is not None;d=(f.w-24)//3;E(f.g,ak(e,d-6),x+12+2*d,y+2,Q if b else D)
	def fQ(f,x,y):bA(f,x+f.w-12-170-8-I("Bag slots:"),y,"Bag slots:","bagmode",170,list(enumerate(bh)),b["bagmode"],"Where the bag slots get bags: Inventory > Bags, bags you target, or your backpack and its bags")
	def fR(f,x,y):a=d3(f,y,(("pgprev",a7,"Prev","Show the previous bottom-left page"),("pgnext",a7,"Next","Show the next bottom-left page"),("bind",cA,"Keybind mode","Start keybind mode: hover a cell and press a key")));E(f.g,ak("Bar page %d of %d"%(b["page"]+1,ad),x+f.w-16-a),a,y+3,D)
	def fS(f,x,y):c=x+12+I("Extra rows:")+8;a=b["anchor"];d={"":"none (drop near a corner or edge middle)","L":"left edge, upright","R":"right edge, upright","T":"top edge","B":"bottom edge","C":"screen centre"}.get(a,{"TL":"top-left","TR":"top-right","BL":"bottom-left","BR":"bottom-right"}.get(a,a)+" corner");E(f.g,ak("Anchor: %s"%d,x+f.w-16-(c+130)),c+130,y+2,D)
	def fT(f,x,y):
		g,e,w=f.g,f.c,f.w;i=K["sel"];a=A(aU(i));b=bA(f,x+12,y,"Cell:","sel",120,list(enumerate(eq())),i,"The cell to edit (right-clicking a cell on the bar does the same)");b=bA(f,b,y,"Does:","does",150,bV,a["t"],"What a click or the hotkey does");bA(f,b,y,"Target:","target",100,cZ,a["tg"],"Answer the cell's target cursor with yourself or your last target (when no other module holds it)");E(g,"Value:",x+12,y+34)
		if a["t"]=="item":c=("0x%04X"%a["g"])+((",%d"%a["h"])if a["h"]else "")
		elif a["t"]=="ui":c=""
		elif a["t"]=="travel":c=bj(a)
		else:c=a["v"]
		d=x+12+max(I("Value:"),I("Window:"))+8;e["value"]=am(bE(g,c,d,y+32,x+w-16-d,numbers=False),"The cell's value (see below; a Client window cell uses Window)");E(g,"Window:",x+12,y+66);j=c4();k=[s[0]for s in j];K["dds"].append(("window",d,y+64,140,[t[1]for t in j],k.index(a["v"])if a["t"]=="ui"and a["v"]in k else 0,"The client or module window a Client window cell opens"));b=d+140+16
		for m,h,n,l,o,p in(("key","Hotkey:",a["k"],100,False,cl["hotkey"]+"; or use Keybind mode"),("lo","Red at:",str(a["lo"]),40,True,cl["lo"])):E(g,h,b,y+66);e[m]=am(bE(g,n,b+I(h)+8,y+64,l,numbers=o),p);b+=I(h)+8+l+16
		q=d3(f,y+96,(("apply",cz,"Apply","Save this cell"),("pick",cA,"Pick item...","Target an item for this cell"),("clear",cy,"Clear","Empty this cell")));e["status"]=E(g,"",q,y+99,D)
	def fU(g,x,y,w):
		if not C["a"]:db()
		K["dds"]=[];f=U.build(g,x,y,w)
		for c,e,h,i,j,k,l in sorted(K["dds"],key=lambda d:-d[2]):a=G.CreateDropDown(i,j,k);a.SetPos(e,h);g.Add(a);f.c[c]=am(a,l)
		K.update({"seen_sel":K["sel"],"seen_bag":b["bagmode"]})
	def aN(text,hue=None):
		if U.f is not None:aD(U.f.c["status"],text,D if hue is None else hue)
	def fV():
		d=U.f.c;e=aU(K["sel"]);a=A(e)
		def f(a,dd):return a[max(0,min(len(a)-1,bG(dd,0)))][0]
		t=f(bV,d["does"]);v=str(d["value"].Text or "").strip();i=f(cZ,d["target"]);k=_norm_key(d["key"].Text);g=aq(k)
		if g:aN("%s belongs to %s"%(k,g),r);return
		try:h=int(str(d["lo"].Text or "0"))
		except Exception:h=cN
		b=dict(Z(),t=t,tg=i,k=k,lo=h)
		if t=="item":
			c=eo(v)
			if c is None and a["t"]=="item"and a["g"]:c=(a["g"],a["h"])
			if c is None:aN("Pick an item, or type its graphic",r);return
			b.update({"g":c[0],"h":c[1],"n":a["n"]if(a["g"],a["h"])==c else "0x%04X"%c[0]})
		elif t=="ui":b["v"]=f(c4(),d["window"])
		elif t=="ability":b["v"]="secondary"if v.lower().startswith("s")else "primary"
		elif t=="travel":
			if a["t"]!="travel":aN("Pick its destination: right-click the cell, then Travel (runebook)",r);return
			b["tg"]=""
			for k in("v","n")+bW:b[k]=a.get(k,"")
		elif t:
			if not v:aN("Type a value first",r);return
			b["v"]=v
		C[e[0]][e[1]]=b
		if b["k"]and b["k"]!=_norm_key(a["k"]):cd(e,b["k"])
		aw(recount=True,refresh=False,refs=[e]);aN("Saved %s"%N(e),Q)
	def fW(f):
		for a,b in(("pgprev",("page",-1)),("pgnext",("page",1)),("bind",("bind",))):
			if a9(f.store,a):B(b)()
		if a9(f.store,"apply"):fV()
		if a9(f.store,"pick"):B(("pick",aU(K["sel"])))();aN("Target the item")
		if a9(f.store,"clear"):dp(aU(K["sel"]))
	def fX(f,new):
		a=bG(f.c["bagmode"],b["bagmode"])
		if a!=K["seen_bag"]and 0<=a<len(bh):K["seen_bag"]=new["bagmode"]=a
		c=bG(f.c["sel"],K["sel"])
		if c!=K["seen_sel"]and 0<=c<X+F+bR:K["sel"]=c;aA(q)
	def fY(b,new):
		if new["bagmode"]!=b["bagmode"]:a["bag_sig"],a["next_scan"]=None,0.
		az();al(.4)
	U=Kit.Page(b,fO,ag,fY,adjust=fX,clicks=fW,every=.2);da()
	def fZ():a.update(c0(),minimized=Kit.load_min(bP),em=False,ub_last=None,ub_pending=True,counted_at=0.);co.clear();O["held"]={};z.update(scale=None,vertical=None,slot=None,sig=None);da();db();dl();a["ub_state"],a["grim_state"],a["va_state"]=aG(),bl(),b0();ah();HOST.layout_add(q,e6,aS,eR);bi.add(HOST.layout_remove,q);a.update(dock_sig=di(),tray_sig=dj(),watch_next=0.,owned_sig=frozenset(HOST.hotkeys_owned));dG();a.update(rebuild_at=0.,redraw=set());fM();az();bi.service("actionbar.hotkeys",eL);bi.service("look.actionbar",al)
	def f_():
		if a["shutting"]or e["g"]is None:return
		if Kit.closed(e):return
		c=time.time();fi(c);fe(c);ex()
		if a["minimized"]and a["em"]==ac(q)and not a["rebuild_at"]:al()
		h=bC()
		if h!=e.get("arranging",False):
			e["arranging"]=h
			if e.get("lockbtn"):bu(e["lockbtn"],*cb())
		while a["queue"]:
			d=a["queue"].pop(0);f=d[0]
			if f in d2:d2[f](*d[1:])
			elif f=="dock":
				g=dict(b2()).get(d[1])
				if g is not None:
					s=safe(g.get("state"))
					if s is None:
						if g.get("on"):safe(g["on"])
						else:ae(lambda k=d[1]:safe(lambda:bB(k)))
					elif s=="open":cs(d[1])
					else:safe(g.get("show"))
					a["dock_sig"],a["watch_next"]=None,0.
			elif f=="traywin":b["tray_open"]=not b["tray_open"];ag();dA()
			elif f=="toggle_min":
				if ac(q)and not a["minimized"]:continue
				aX();a["minimized"]=not a["minimized"];cI(bP,a["minimized"]);ah();al()
			if a["shutting"]or e["g"]is None:return
		c=time.time()
		if c>=a["next_scan"]:
			a["next_scan"]=c+2.;dl();eA();ah()
			if a.get("last_pos")!=a.get("pos_saved"):aX()
		if a["rebuild_at"]and c>=a["rebuild_at"]:a["rebuild_at"]=0.;a["redraw"]=set();dG()
		elif a["redraw"]:e7()
		if c>=a["next_count"]or(a.get("pack_v")is not None and c-a.get("counted_at",0.)>=ea and cw()!=a["pack_v"]):a["next_count"]=c+bQ;eB()
		eJ(c)
		if c>=a.get("tray_next",0.):a["tray_next"]=c+.1;e9(c)
	def f0():
		while a["jobs"]and not a["shutting"]:a["jobs"].pop(0)()
	def f1():
		a["shutting"]=True;bi.close();a4();g,Y["g"]=Y["g"],None;T(g);a["bind"]=None;ay();ah(False);fN()
		with Kit.quiet:cH(aX)
		cI(bP,a["minimized"]);ag();aW();g,e["g"]=e["g"],None;T(g)
		for s in e.pop("stale",[]):T(s)
	return{"start":fZ,"tick":f_,"stop":f1,"client_tick":True,"config_height":U.height,"build_config":fU,"poll_config":U.poll,"config_closed":U.closed,"thread_tick":f0,"thread_wanted":lambda:bool(a["jobs"])}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("actionbar","Action Bar","Cells for items, spells, skills and windows",_module_actionbar,.05,category="On screen")
