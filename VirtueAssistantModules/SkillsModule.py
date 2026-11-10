def _module_skills():
	ai=Client._type;aj=HOST.claim_cursor;ak=HOST.cursor_busy;al=HOST.mobiles;D=HOST.refresh_settings;O=HOST.release_cursor;am=HOST.show_settings;X=Journal.reader;M=Kit.ART_CLOSE;J=Kit.ART_OK;U=Kit.ART_PAGE;P=Kit.ART_PLAY;F=Kit.GAP;u=Kit.HUE_BAD;o=Kit.HUE_GOOD;b=Kit.HUE_INFO;B=Kit.HUE_TEXT;Q=Kit.HUE_TITLE;E=Kit.MARGIN;an=Kit.add_box;Y=Kit.add_check;l=Kit.add_label;V=Kit.add_pic;H=Kit.add_section;N=Kit.add_textbox;ad=Kit.add_tiled;ae=Kit.add_window_frame;A=Kit.art_button;af=Kit.basics;K=Kit.catcher;ao=Kit.closed;aa=Kit.count;ap=Kit.data_path;ab=Kit.dispose;C=Kit.fit;R=Kit.get_var;ag=Kit.in_pack;T=Kit.is_open;W=Kit.on_click;I=Kit.pic_size;S=Kit.put_var;aq=Kit.scale_window;n=Kit.set_text;e=Kit.text_w;ar=Kit.title_bar;ah=Kit.ui_pos;at=Kit.was_clicked;z=Kit.with_tip;ac=Kit.zone_up;av="skills";aw="Skills"
	def au(q,title,what):
		while q:
			a,b=q.pop(0)
			try:
				with open(a,"w")as c:c.write(b)
				API.SysMsg("%s: %s written to %s."%(title,what,a),o)
			except Exception as d:API.SysMsg("%s: couldn't write %s (%s)."%(title,a,d),u)
	def ax():
		aw="skills";aE="Skills";bs="Skills_settings";bt="Skills_pos";bu="Skills_marks";bv="Skills_locksets";bw="Skills_session";cj=6;ck=7000;cl=("StandardSkillsGump","SkillGumpAdvanced");cm=5091;ax=22;a7=110;bx=56;cn=120;co=.35;cp=380;a8=60;by=("bar","gain","cap","real");bz=80;bA=2;bB=2;aR="Real values added up, against the total cap (settings page)";bC=(("all_up","All up","Set every listed skill to go up"),("all_down","All down","Set every listed skill to go down (click twice)"),("all_locked","All locked","Lock every listed skill"),("lock_capped","Lock capped","Lock every skill at its cap"));bD,cq=280,46;cr={"use":(P,"Use","Use this skill","use"),"button":(U,"Make button","Make its floating client button (or double-click it in the list)","mkbutton"),"pin":(J,"Pin","Keep it at the top of the list (again to unpin)","pin"),"nextgrp":(U,"Next group","Move it to the next skill group","nextgrp")};aS=200;bE=10;aX=(2103,2104,2104);ay=(2435,2437,2092);a9,ba=2086,2087;cs=2056;ct=946;bF=946;cu,cv="#D8B048",.16;cw,cx="#FFFFFF",.07;cy=4.;bG=1.;bH=["Alchemy","Anatomy","Animal Lore","Item Identification","Arms Lore","Parrying","Begging","Blacksmithy","Bowcraft/Fletching","Peacemaking","Camping","Carpentry","Cartography","Cooking","Detecting Hidden","Discordance","Evaluating Intelligence","Healing","Fishing","Forensic Evaluation","Herding","Hiding","Provocation","Inscription","Lockpicking","Magery","Resisting Spells","Tactics","Snooping","Musicianship","Poisoning","Archery","Spirit Speak","Stealing","Tailoring","Animal Taming","Taste Identification","Tinkering","Tracking","Veterinary","Swordsmanship","Mace Fighting","Fencing","Wrestling","Lumberjacking","Mining","Meditation","Stealth","Remove Trap","Necromancy","Focus","Chivalry","Bushido","Ninjitsu","Spellweaving","Mysticism","Imbuing","Throwing"];cz={"Alchemy":[(30,"NPC alchemists teach the first points for gold"),(50,"Heal and Agility potions"),(70,"Cure and Greater Agility potions"),(90,"Greater Strength and Greater Heal potions"),(100,"Greater Cure and Greater Explosion potions")],"Anatomy":[(100,"Use it on any creature or player; bandaging checks it too")],"Animal Lore":[(100,"Use it on tamed or tameable animals")],"Item Identification":[(100,"Use it on any item")],"Arms Lore":[(100,"Use it on weapons and armour")],"Parrying":[(100,"Fight with a shield on (only shields parry pre-AoS)")],"Begging":[(100,"Beg from town NPCs")],"Blacksmithy":[(30,"NPC blacksmiths teach the first points for gold"),(50,"Maces, then cutlasses"),(65,"Scimitars, then broadswords and kryss"),(80,"Katanas, then short spears and spears"),(100,"Plate gorgets and gloves, then plate legs and tunics")],"Bowcraft/Fletching":[(40,"Shafts and arrows"),(65,"Bows"),(85,"Crossbows"),(100,"Heavy crossbows")],"Peacemaking":[(100,"Use it near creatures; tougher ones as it rises")],"Camping":[(100,"Light kindling over and over (a blade on a tree gives some)")],"Carpentry":[(30,"NPC carpenters teach the first points for gold"),(50,"Medium crates"),(65,"Large crates, then wooden shields"),(85,"Fishing poles and quarter staves"),(100,"Gnarled and black staves")],"Cartography":[(30,"NPC mapmakers teach the first points for gold"),(50,"Local maps"),(65,"City maps"),(100,"Sea charts, then world maps")],"Cooking":[(30,"NPC cooks teach the first points for gold"),(100,"Cook over and over (fish steaks and ribs are cheap)")],"Detecting Hidden":[(100,"Use it often, best near someone hidden")],"Discordance":[(100,"Use it on creatures; tougher ones as it rises")],"Evaluating Intelligence":[(100,"Use it on any player or creature")],"Healing":[(30,"NPC healers teach the first points; bandage yourself when hurt"),(60,"Bandage yourself or friends while hurt"),(80,"Keep bandaging; curing poison needs 60 Healing and 60 Anatomy"),(100,"Keep bandaging; resurrecting needs 80 Healing and 80 Anatomy")],"Fishing":[(100,"Fish over and over, in any water")],"Forensic Evaluation":[(100,"Use it on corpses")],"Herding":[(100,"Herd animals with a shepherd's crook")],"Hiding":[(100,"Use it over and over")],"Provocation":[(100,"Make creatures fight each other; tougher ones as it rises")],"Inscription":[(30,"NPC scribes teach the first points for gold"),(100,"Scribe scrolls of a circle you sometimes fail (spell in your book)")],"Lockpicking":[(30,"NPC thieves and tinkers teach the first points"),(100,"Pick locked boxes just above your level")],"Magery":[(30,"NPC mages teach the first points; then 2nd circle spells"),(45,"3rd circle: Bless, Teleport"),(55,"4th circle: Greater Heal, Mana Drain"),(65,"5th circle: Paralyze, Mind Blast"),(75,"6th circle: Invisibility, Mark"),(90,"7th circle: Flamestrike, Mana Vampire"),(100,"8th circle: Earthquake, summons")],"Resisting Spells":[(100,"Rises when spells hit you: a friend's low curses work")],"Tactics":[(100,"Rises as you fight with any weapon")],"Snooping":[(100,"Look into others' packs (a friend's pack animal is safe)")],"Musicianship":[(100,"Play an instrument; the other bard skills train it too")],"Poisoning":[(30,"Lesser poison on a weapon or food"),(60,"Regular poison"),(100,"Greater, then deadly poison")],"Archery":[(30,"An archery butte or an NPC trainer for the first points"),(100,"Shoot creatures a little tougher than you as it rises")],"Spirit Speak":[(100,"Use it over and over")],"Stealing":[(100,"Steal light items from a friend's pack; heavier is harder")],"Tailoring":[(30,"NPC tailors teach the first points for gold"),(45,"Short pants and fancy shirts"),(55,"Cloaks"),(70,"Robes, then leather gorgets and sleeves"),(85,"Leather leggings and tunics"),(100,"Studded gloves, then studded sleeves and leggings")],"Animal Taming":[(30,"NPC animal trainers teach the first points for gold"),(50,"Horses, ostards, llamas, black and polar bears"),(70,"Panthers, grey wolves, grizzly bears, great harts"),(85,"White wolves, bulls, frenzied ostards"),(100,"Drakes and hell hounds, then dragons")],"Taste Identification":[(100,"Use it on food and potions")],"Tinkering":[(30,"NPC tinkers teach the first points for gold"),(60,"Tools and clock parts"),(80,"Lockpicks"),(100,"Spyglasses or jewellery")],"Tracking":[(100,"Use it over and over")],"Veterinary":[(30,"NPC veterinarians teach the first points"),(60,"Bandage hurt animals and pets"),(80,"Keep bandaging; curing needs 60 Veterinary, 60 Animal Lore"),(100,"Keep bandaging; resurrecting needs 80 and 80")],"Swordsmanship":[(30,"NPC trainers or a training dummy for the first points"),(100,"Fight creatures a little tougher than you as it rises")],"Mace Fighting":[(30,"NPC trainers or a training dummy for the first points"),(100,"Fight creatures a little tougher than you as it rises")],"Fencing":[(30,"NPC trainers or a training dummy for the first points"),(100,"Fight creatures a little tougher than you as it rises")],"Wrestling":[(30,"NPC trainers or a training dummy, empty-handed"),(100,"Fight empty-handed; tougher creatures as it rises")],"Lumberjacking":[(100,"Chop trees with an axe over and over")],"Mining":[(30,"NPC miners teach the first points for gold"),(65,"Mine iron ore in mountains and caves"),(100,"Keep mining: the coloured ores come from 65 up")],"Meditation":[(100,"Spend mana, then meditate; metal armour blocks it")],"Stealth":[(100,"Needs 80 Hiding: hide, then move with Stealth (light armour)")],"Remove Trap":[(100,"Use it on trapped boxes (tinkers can trap some to practise on)")],};bI="Skills_stat_targets";bb=250;aT=("up","down","locked");bJ=("Going up","Going down","Locked");cA=("Set it to go up","Set it to go down","Lock it");aD=[("all","All skills"),("trained","Trained (above 0)"),("gaining","Gaining now"),("session","Gained this session"),("up","Set to go up"),("down","Set to go down"),("locked","Locked"),("below","Below cap"),("pinned","Pinned")];cB=("name","real","value","cap","gain","lock");p={"replace":True,"x_hides":True,"bars":True,"col_cap":True,"col_gain":True,"journal":False,"lock_at_cap":False,"lock_at_target":True,"cap_warn":True,"rows":12,"total_cap":ck,"hl_secs":30,"rate_min":30,"sec_summary":True,"sec_stats":True,"sec_locks":True,"sec_detail":True,"sec_log":False,"log_lines":5,"sort":"name","asc":True,"filter":0,"groups":False,"minimized":False,"width":0,"tips":True,"lock_stat_target":True};cC=dict(p);aJ={"rows":(4,40),"total_cap":(100,72000),"hl_secs":(0,600),"rate_min":(5,240),"log_lines":(2,15),"filter":(0,len(aD)-1),"width":(0,4000)};cD=("bars","col_cap","col_gain","rows","sec_summary","sec_stats","sec_locks","sec_detail","sec_log","log_lines","tips","x_hides","replace");cE=1.;aP=("Strength","Dexterity","Intelligence")
		def cF():
			b={}
			for e,f in cz.items():
				c,d=[],0
				for a,g in f:c.append((a*10,"%g-%g"%(d/10.,a),g));d=a*10
				b[e.lower()]=c
			return b
		cG=cF();ao={"pins":set(),"targets":{}};aA=[];aB=[0,0,0];j={"minimized":False,"shutting":False,"docked":False,"queue":[],"sel":None,"last_click":(None,0.),"arm":{},"search":"","pc":{},"save_at":0.,"to_write":[],"ver":0,"preview":False};t={"g":None,"c":{},"store":({},{}),"rows":[],"rowmap":{}};aN={"sync":False,"skip":False};cH,ak,ac=af(j,aE);aU={};aF={"world":None,"player":None,"how":""};q={"objs":[],"names":[],"click":[],"collide":[],"n":0,"cur":[],"low":[],"full":True,"rr":0};X={"cur":[0,0,0],"locks":[0,0,0],"cap":0,"prev":[0,0,0]};O={"list":[],"ok":False,"ver":0,"sig":None,"of":{}};VG={"gumps":None,"sig":None,"full_at":0.}
		def aK():j["ver"]+=1;j["dirty"]=True
		cI=.5;cJ=1.;cK=5.
		def cL():
			j["dirty"]=True
			if(p["sort"]!="name"or aD[p["filter"]][0]not in("all","pinned")):j["ver"]+=1
		al={"width":None,"rows":None,"slot":None,"k":1.,"full":None}
		def bK():return al["width"]if al["width"]is not None else p["width"]
		def cM(w,h,mode):
			a=(int(w),int(h))if(w and h)else None
			if a==al["slot"]and not(mode=="again"and a is not None):return
			al["slot"]=a;al["width"]=a[0]if a is not None else None;al["rows"]=None;j["m"]=None;j["rebuild"]="window";aK()
		def cN():return al["k"],al["full"]
		ag={"start":0.,"base":{},"stats":None,"seen":0.}
		def bL():
			Kit.kv_load(bs,";",p,aJ,("sort",))
			if p["sort"]not in cB:p["sort"]="name"
		def aH():Kit.kv_save(bs,";",p,cC,aJ,("sort",))
		def cO():
			ao["pins"],ao["targets"]=set(),{}
			for b in R(bu).split(";"):
				p=b.split(":")
				if len(p)!=3:continue
				try:i,c,a=int(p[0]),p[1]=="1",int(p[2])
				except ValueError:continue
				if c:ao["pins"].add(i)
				if a>0:ao["targets"][i]=a
		def bM():a=sorted(ao["pins"]|set(ao["targets"]));S(bu,";".join("%d:%s:%d"%(c,"1"if c in ao["pins"]else "0",ao["targets"].get(c,0))for c in a))
		def cP():
			del aA[:]
			for a in R(bv).split("|"):
				if "="in a:
					b,c=a.split("=",1)
					if b and c:aA.append((b,c))
		def bN():S(bv,"|".join("%s=%s"%(a,d)for a,d in aA))
		def bO():
			p=R(bI).split(",")
			for k in range(3):
				try:aB[k]=max(0,min(bb,int(p[k])))
				except(IndexError,ValueError):aB[k]=0
		def cQ():
			p=R(bw).split("|");a=time.time();ag.update({"start":a,"base":{},"stats":None,"seen":a})
			if len(p)<4:return
			try:b,f=float(p[0]),float(p[3])
			except ValueError:return
			if a-f>cj*3600 or b>a:return
			c={}
			for d in p[1].split(","):
				if ":"in d:
					try:k,v=d.split(":");c[int(k)]=int(v)
					except ValueError:pass
			e=None
			try:s=[int(g)for g in p[2].split(",")];e=s if len(s)==3 else None
			except ValueError:pass
			ag.update({"start":b,"base":c,"stats":e,"seen":a})
		def aY():ag["seen"]=time.time();b=",".join("%d:%d"%(a,c)for a,c in sorted(ag["base"].items()));s=",".join(str(d)for d in ag["stats"])if ag["stats"]else "";S(bw,"%d|%s|%s|%d"%(ag["start"],b,s,ag["seen"]))
		def cR():
			ag.update({"start":time.time(),"base":{},"stats":None})
			for i in range(q["n"]):ag["base"][i]=q["cur"][i][0]
			if any(X["cur"]):ag["stats"]=list(X["cur"])
			j["gains"],j["log"]={},[];aY()
		def bc():Kit.save_pos(bt,t["g"])
		def aZ():return Typing._get(None,"Instance",ai("ClassicUO.Game.World"))
		def bP(objs,how):
			b=[str(safe(lambda s=f:s.Name,"")or "?")for f in objs];c=[bool(safe(lambda s=g:s.IsClickable,False))for g in objs];a=[h.lower()for h in b];d=[any(a[k]in a[i]for i in range(k))for k in range(len(a))];q.update({"objs":objs,"names":b,"click":c,"collide":d,"n":len(objs),"low":a,"full":True})
			if len(q["cur"])!=len(objs):q["cur"]=[[0,0,0,0]for m in objs]
			aF["how"]=how;j["m"]=None
		def bQ(force=False):
			d=time.time()
			if not force and d<j["ref_at"]:return q["n"]>0
			j["ref_at"]=d+3.;b=aZ();c=Typing._get(b,"Player")if b is not None else None
			if c is not None:
				e=Typing._get(c,"Skills");a=list(e)if e is not None else None
				if a:
					f=aF["player"]is not None and aF["player"]is c and len(a)==q["n"];h=aF["player"]is not None and not f;aF.update({"world":b,"player":c})
					if not f:
						if h:q["cur"]=[];j["ready"]=False;j["rebuild"]="window"
						bP(a,"client")
					return True
			aF.update({"world":b,"player":None})
			if q["n"]==0 or aF["how"]!="api":
				a=[]
				for g in bH:
					s=API.GetSkill(g)
					if s is not None and str(s.Name)==g:a.append(s)
				if a:bP(a,"api")
			return q["n"]>0
		bR=15
		def bS(full=False):
			b={};d=q["cur"];f=q["objs"];n=len(f)
			if n==0 or len(d)!=n:return b
			if q["full"]:q["full"]=False;full=True
			g=q["rr"]%n;q["rr"]=g+bR;a=int
			for i in range(n):
				s=f[i]
				try:e,v=a(s.BaseFixed),a(s.ValueFixed)
				except Exception:continue
				c=d[i]
				if full or e!=c[0]or v!=c[1]or(i-g)%n<bR:
					try:h=a(s.CapFixed);j=a(s.Lock)
					except Exception:continue
					if e!=c[0]or v!=c[1]or h!=c[2]or j!=c[3]:b[i]=c;d[i]=[e,v,h,j]
			return b
		def bT():
			b,a,c=X["cur"],X["locks"],X["cap"];p=aF["player"]
			if p is None:p=API.Player
			if p is not None:
				try:b=[int(p.Strength),int(p.Dexterity),int(p.Intelligence)];a=[int(p.StrLock),int(p.DexLock),int(p.IntLock)];c=int(p.StatsCap)
				except Exception:pass
			if j["stat_pending"]:
				d=time.time();a=list(a)
				for k,(e,f)in list(j["stat_pending"].items()):
					if d<f:a[k]=e
					else:j["stat_pending"].pop(k,None)
			if b==X["cur"]and a==X["locks"]and c==X["cap"]:return False
			X["prev"]=X["cur"];X["cur"],X["locks"],X["cap"]=b,a,c;return True
		def bU():return any(a[2]>0 for a in q["cur"])
		def aV():w=aF["world"]or aZ();return Typing._get(w,"SkillsGroupManager")if w is not None else None
		def cS():
			if aM.f is not None:return True
			if t["g"]is None or not t["c"]or j["minimized"]or j["docked"]:return False
			return p["groups"]or(j["sel"]is not None and p["sec_detail"])
		def aI(force=False):
			c=time.time()
			if not force and(c<j["grp_at"]or not cS()):return
			j["grp_at"]=c+(1. if aM.f is not None or p["groups"]else cT);d=aV();b=Typing._get(d,"Groups")if d is not None else None;a=[]
			if b is not None:
				for g in list(b):
					try:n=int(g.Count);i=[int(g.GetSkill(r))for r in range(n)];a.append({"obj":g,"name":str(g.Name or ""),"members":[s for s in i if s<q["n"]],"max":bool(g.IsMaximized)})
					except Exception:continue
			e=(b is not None,tuple((m["name"],tuple(m["members"]),m["max"])for m in a))
			if e!=O["sig"]:O["sig"]=e;O["ver"]+=1
			f={}
			for h in range(len(a)-1,-1,-1):
				for k in a[h]["members"]:f[k]=h
			O["list"],O["ok"],O["of"]=a,b is not None,f
		cT=3.
		def bd(i):return O["of"].get(i)
		def aO():
			a=aV()
			if a is not None:safe(lambda:a.Save())
			aI(True)
		def be(name,a):return Tz.call(None,name,a,Tz.T("ClassicUO.Game.GameActions"))
		def aW(i,v):
			if i is None or i>=q["n"]or q["cur"][i][3]==v:return
			if not q["collide"][i]:API.SetSkillLock(q["names"][i],aT[v])
			else:
				with Kit.quiet:import System;be("ChangeSkillLockStatus",[System.UInt16(i),System.Byte(v)]);a=Tz.T("ClassicUO.Game.Data.Lock");Tz.put(q["objs"][i],"Lock",System.Enum.ToObject(a,v))
			q["cur"][i][3]=v
		def cU(i):
			if i is None or i>=q["n"]:return
			if not q["click"][i]:ac("%s can't be used directly."%q["names"][i],b);return
			if not q["collide"][i]:API.UseSkill(q["names"][i]);return
			try:be("UseSkill",[i])
			except Exception as a:ac("couldn't use %s (%s)."%(q["names"][i],Tz.why(a)),u)
		def bV(i):
			if i is None or i>=q["n"]or not q["click"][i]:ac("only a usable skill gets a button.",b);return
			try:
				import System
				for a in Tz.windows(["SkillButtonGump"]):
					if int(Tz.get(a,"SkillID"))==i:a.Dispose()
				c=Tz.T("ClassicUO.Game.UI.Gumps.SkillButtonGump");d=aF["world"]or aZ();g=t["g"];x,y=(g.GetX()+g.GetWidth()+10,g.GetY())if T(g)else(200,200);e=System.Activator.CreateInstance(c,System.Array[object]([d,q["objs"][i],x,y]));Tz.call(None,"Add",[e,True],Tz.T("ClassicUO.Game.Managers.UIManager"));ac("%s button placed beside the window."%q["names"][i],o)
			except Exception as f:ac("couldn't make the button (%s)."%Tz.why(f),u)
		def bW():
			a=aF["world"]or aZ();j["swallow_until"]=time.time()+6.;j["asked"]=time.time()
			try:be("OpenSkills",[a]);return True
			except Exception:return False
		def bf(k,v):API.SetStatLock(("str","dex","int")[k],aT[v]);X["locks"][k]=v;j["stat_pending"][k]=(v,time.time()+2.5)
		def f1(a):return "%.1f"%(a/10.)
		def aG(i):b=ag["base"].get(i);return 0 if b is None else q["cur"][i][0]-b
		def bg():return sum(aG(a)for a in range(q["n"]))
		bX=600.
		def bh():return max(bX,time.time()-ag["start"])/3600.
		def bY(i,now):a=p["rate_min"]*60;return sum(f for c,f in j["gains"].get(i,[])if now-c<=a)
		def bZ(i,now):a=aG(i)/bh();b=max(bX,min(p["rate_min"]*60.,now-max(ag["start"],j["started"])));c=bY(i,now)/(b/3600.);return a,c
		def bi(secs):
			secs=int(max(0,secs))
			if secs>=3600:return "%dh %02dm"%(secs//3600,(secs%3600)//60)
			if secs>=60:return "%dm"%(secs//60)
			return "%ds"%secs
		def cV(i,now,a=None):
			b,e,c,e=q["cur"][i]
			if b>=c:return "at cap"
			f,d=a if a is not None else bZ(i,now);r=d if d>0 else f
			if r<=0:return "--"
			return "~"+bi((c-b)/r*3600)
		def cW(changed,now):
			g=False
			for i,e in changed.items():
				a=q["cur"][i];d=a[0]-e[0]
				if d==0:continue
				g=True;b=q["names"][i]
				if i not in ag["base"]:ag["base"][i]=e[0]
				if d>0:
					j["gains"].setdefault(i,[]).append((now,d))
					if len(j["gains"][i])>aS:j["gains"][i]=j["gains"][i][-aS:]
					if p["hl_secs"]>0:j["hl"][i]=now+p["hl_secs"]
				j["log"].append((now,b,d,a[0]))
				if len(j["log"])>aS:j["log"]=j["log"][-aS:]
				if p["journal"]:ac("%s %s%s (%s, session %+.1f)."%(b,"+"if d>0 else "-",f1(abs(d)),f1(a[0]),aG(i)/10.),o if d>0 else u)
				for f,h,c in((a[2],"lock_at_cap","its cap (%s)"),(ao["targets"].get(i),"lock_at_target","its target %s")):
					if d>0 and f is not None and e[0]<f<=a[0]:
						c=c%f1(f)
						if p[h]and a[3]==0:aW(i,2);ac("%s reached %s and was locked."%(b,c),o)
						else:ac("%s reached %s."%(b,c),o)
			if g and time.time()>=j["save_at"]:j["save_at"]=time.time()+15.;aY()
		def bj():return sum(a[0]for a in q["cur"])
		def cX():
			if bj()<p["total_cap"]:return False
			a=any(d[3]==0 and d[0]<d[2]for d in q["cur"]);b=any(f[3]==1 and f[0]>0 for f in q["cur"]);return a and not b
		def cY():
			if not p["cap_warn"]:j["warned_cap"]=False;return
			a=cX()
			if a and not j["warned_cap"]:ac("at the total skill cap (%s) and no skill set to go down: nothing can rise."%f1(p["total_cap"]),u)
			j["warned_cap"]=a
		def a_(k):a=ag["stats"];return X["cur"][k]-a[k]if a else 0
		def cZ():
			a,b=X["prev"],X["cur"]
			for k in range(3):
				t=aB[k]
				if not t or not a[k]or b[k]!=t:continue
				c={1:0,-1:1}.get(b[k]-a[k])
				if c is None:continue
				if p["lock_stat_target"]and X["locks"][k]==c:bf(k,2);ac("%s reached its target %d and was locked."%(aP[k],t),o)
				else:ac("%s reached its target %d."%(aP[k],t),o)
		def c_(k):
			t,v=aB[k],X["cur"][k]
			if t and v==t and p["lock_stat_target"]and X["locks"][k]!=2:bf(k,2);ac("%s is at its target %d and was locked."%(aP[k],t),o)
		def c0(k,b):
			v=X["cur"][k];a=["%s %d"%(aP[k],v)]
			if ag["stats"]:d=a_(k);a[0]+=": %+d this session (%.1f / hour)"%(d,d/b)
			t=aB[k]
			if not t:a.append("No target (click: set one in settings)")
			elif v==t:a.append("Target %d: reached"%t)
			else:a.append("Target %d: %d to go %s%s"%(t,abs(t-v),"up"if t>v else "down",", then it locks"if p["lock_stat_target"]else ""))
			return "\n".join(a)
		def b_(i):
			if i is None or i>=q["n"]:return
			a=cG.get(q["names"][i].lower())
			if a:
				b=q["cur"][i][0]
				for c,d,e in a:
					if b<c:return d,e
			return
		def c1(i,now):
			f=aD[p["filter"]][0];a,e,c,d=q["cur"][i];b=j["search"]
			if b and b not in q["low"][i]:return False
			if f=="trained":return a>0
			if f=="gaining":return bY(i,now)>0
			if f=="session":return aG(i)>0
			if f in aT:return d==aT.index(f)
			if f=="below":return a<c
			if f=="pinned":return i in ao["pins"]
			return True
		def aQ(idx):
			s=p["sort"];b=q["low"].__getitem__
			if s=="name":a=sorted(idx,key=b)
			else:c={"real":0,"value":1,"cap":2,"lock":3}.get(s);d=aG if c is None else(lambda i:q["cur"][i][c]);a=sorted(sorted(idx,key=b),key=d)
			if not p["asc"]:a.reverse()
			return a
		def c2(now):
			b=[r for r in range(q["n"])if c1(r,now)];i=set(b);d=[s for s in b if s in ao["pins"]];k=bool(j["search"])or p["filter"]!=0;a=[]
			if not p["groups"]or not O["ok"]:
				if aD[p["filter"]][0]=="pinned":return[("s",v)for v in aQ(b)]
				l=[w for w in b if w not in ao["pins"]];return[("s",x)for x in aQ(d)+aQ(l)]
			if d and aD[p["filter"]][0]!="pinned":
				c=j["pc"].get("pin",False);a.append(("g","pin",c))
				if not c:a+=[("s",y)for y in aQ(d)]
			e=set()
			for m,g in enumerate(O["list"]):
				f=[G for G in g["members"]if G in i];e.update(g["members"])
				if not f and k:continue
				a.append(("g",m,not g["max"]))
				if g["max"]:a+=[("s",L)for L in aQ(f)]
			h=[Z for Z in b if Z not in e]
			if h:
				c=j["pc"].get("other",False);a.append(("g","other",c))
				if not c:a+=[("s",dy)for dy in aQ(h)]
			return a
		def c3(i):
			def a(*c):
				a=time.time();b,t=j["last_click"]
				if b==i and a-t<=.6:j["last_click"]=(None,0.);ak.add(("button",i),dup=True)
				else:j["last_click"]=(i,a);ak.add(("pick",i),dup=True)
			return a
		c4=Kit.disposer("skills.window",j,t)
		def c5():j["rebuild"]="window"
		def av(ctrl,b,value):
			if ctrl is None:return
			k=(ctrl,b)
			if aU.get(k)==value:return
			aU[k]=value
			try:
				a=al["k"]
				if b=="Width":Kit.ui_w(ctrl,value if a==1. else int(round(value*a)))
				elif b=="Pos":
					if a==1.:ah(ctrl,value[0],value[1])
					else:ctrl.SetPos(int(round(value[0]*a)),int(round(value[1]*a)))
				else:setattr(ctrl,b,value)
			except Exception:pass
		def b0(ctrl,a,value):aU[(ctrl,a)]=value
		def aj(a):return 35+e(a)
		def aL(IW=None,zone=False):
			m=j["m"]
			if m is not None and(IW is None or(m["IW"]==IW and m.get("zone",False)==zone)):return m
			m=a0()
			if zone and IW:
				c=[]
				for a in by:
					if m["sa_w"]+16<=IW:break
					c.append(a);m=a0(c)
				e=(m["sa_w"]+16)-IW
				if e>0:
					f=min(e,m["name_w"]-a8)
					if f>0:b1(m,-f);m["cut"]=True
				m["drop"]=tuple(c)
			m["zone"]=zone;d=max(0,IW-(m["sa_w"]+16))if IW else 0
			if d:
				b=min(cn,d*2//5)if m["bar_x"]is not None else 0
				if b:
					m["bar_w"]+=b
					for a in("gain_x","lock_x"):
						if m[a]is not None and m[a]>m["bar_x"]:m[a]+=b
				b1(m,d-b)
			m["IW"]=IW;j["m"]=m;return m
		def b1(m,d):
			m["name_w"]+=d
			for a in("real_x","val_x","cap_x","bar_x","gain_x","lock_x"):
				if m[a]is not None:m[a]+=d
			m["row_w"]=m["lock_x"]+m["lock_w"]+6;m["sa_w"]=m["row_w"]+16
		def a0(drop=()):
			m={"cut":False,"drop":()};d=q["names"]or bH;a=I(ay[0])[0]or 10;m["arrow_w"]=a;m["lock_w"]=max(a,I(ay[2])[0]or 12);f=I(aX[0])[0]or 11;m["name_x"]=4+f+6;m["name_w"]=(max([e(k)for k in d]+[e("Skill")+a+4])+10);b=max(e("120.0"),e("Value")+a+3)+10;g=max(e("+120.0"),e("Gain")+a+3)+8
			if "real"in drop:m["real_x"]=None;m["val_x"]=x=m["name_x"]+m["name_w"]
			else:m["real_x"]=m["name_x"]+m["name_w"];m["val_x"]=x=m["real_x"]+b
			x+=b;m["bar_h"]=max(4,min(11,I(Kit.LINE_BLUE)[1]or 9));m["bar_w"]=bx
			for h,c,i in(("cap_x",p["col_cap"]and "cap"not in drop,b),("bar_x",p["bars"]and "bar"not in drop,bx+10),("gain_x",p["col_gain"]and "gain"not in drop,g)):
				m[h]=x if c else None
				if c:x+=i
			m["lock_x"]=x;m["row_w"]=x+m["lock_w"]+6;m["sa_w"]=m["row_w"]+16;return m
		def b2():return 6 if p["tips"]else 5
		def c6():
			M,d=E,F;m=a0();k,f=Kit.screen();o=12+e("Find:")+6+a7+14+aj(max((v[1]for v in aD),key=e))+12+24+e("Groups")+12;q=12+sum(aj(w)for w in a1)+3*10+12;r=12+aj("Use")+12+aj("Make button")+12+aj("Next group")+12;s=I(ay[2])[0]or 12;t=12+3*(e("Int 125 (+25)")+8+s+14)+e("Stats 225 / 225")+12 if p["sec_stats"]else 0;a=max(m["sa_w"]+16,o,q,r,t,cp);g=a+2*M
			if bK()>g:a=bK()-2*M
			if k:a=max(g-2*M,min(a,k-2*M-10))
			m=aL(a);L={"IW":a,"W":a+2*M,"min_w":g};y=M+30+d;l=(2 if p["sec_summary"]else 0)+(1 if p["sec_stats"]else 0);b=p["rows"]if al["rows"]is None else al["rows"]
			for c,u,n in(("sum",l,6+24*l+4),("tool",True,36),("list",True,26+b*ax+6),("locks",p["sec_locks"],36),("detail",p["sec_detail"],6+24*b2()+4),("log",p["sec_log"],26+20*p["log_lines"]+4)):
				if u:L[c]=(y,n);y+=n+d
			L["H"]=y-d+M;L["fixed_h"]=L["H"]-b*ax;h=aJ["rows"][0];L["min_h"]=L["fixed_h"]+h*ax
			if f and L["H"]>f-10 and b>h:
				i=max(h,(f-10-L["fixed_h"])//ax)
				if i<b:
					j=(b-i)*ax;L["list"]=(L["list"][0],L["list"][1]-j)
					for c in("locks","detail","log"):
						if c in L:L[c]=(L[c][0]-j,L[c][1])
					L["H"]-=j;L["rows"]=i;return L
			L["rows"]=b;return L
		a1=tuple(dW[1]for dW in bC)
		def bk(widths,gap,IW):
			b,x,a=[],12,0
			for c in widths:
				if x>12 and x+c>IW-12:x,a=12,a+1
				b.append((x,a));x+=c+gap
			return b,a+1
		def b3():
			b=a0(by);a=[b["sa_w"]-max(0,b["name_w"]-a8)+16,12+e("Find:")+6+bz+2+12,12+aj(max((d[1]for d in aD),key=e))+12,12+24+e("Groups")+12]
			if p["sec_summary"]:a+=[12+e("Session +99.9")+12,12+aj("Reset")+12]
			if p["sec_stats"]:a.append(12+e("Int 125 (+25)")+8+(I(ay[2])[0]or 12)+4)
			if p["sec_locks"]:a.append(12+max(aj(f)for f in a1)+12)
			if p["sec_detail"]:c=max(I(g)[0]for g in ay)or 12;a+=[12+a8+8+3*(c+10)+12,12+e("Target:")+8+56+12+e("none set")+4,12+max(aj("Make button"),aj("Next group"))+12]
			return max(a)+2*E
		def b4(w,h):
			M,j=E,F;a=w-2*M;Z={"IW":a,"W":w,"H":h};c=[];l=0
			if p["sec_summary"]:m=f1(p["total_cap"]);G="Total %s / %s   (%s free)   with bonuses %s"%(m,m,m,m);Z["total2"]=e(G)>a-24;H=a-12-aj("Reset");Z["sess_own"]=H-12-6<e("Session +99.9");l+=(2 if Z["total2"]else 1)+(2 if Z["sess_own"]else 1)
			if p["sec_stats"]:
				z=e("Int 125 (+25)")+8;A=I(ay[2])[0]or 12;k,b,f=[],12,0
				for N in range(3):
					if b>12 and b+z+A>a-4:b,f=12,f+1
					k.append((b,f));b+=z+A+14
				if b>12 and b+e("Stats 225 / 225")>a-4:b,f=12,f+1
				Z["stats"]=(k,(b,f));l+=f+1
			if l:c.append(("sum",6+24*l+4))
			B=aj(max((dy[1]for dy in aD),key=e));o=24+e("Groups");g=12+e("Find:")+6;s=a-g-14-B-12-o-12
			if s>=bz:T={"field":s,"filter":(g+s+14,0),"groups":(a-12-o,0)};n=1
			else:
				T={"field":max(20,a-g-2-12),"filter":(12,1)}
				if 12+B+12+o+12<=a:T["groups"],n=(a-12-o,1),2
				else:T["groups"],n=(12,2),3
			T["tx"]=g;Z["T"]=T;c.append(("tool",36+28*(n-1)));c.append(("list",None))
			if p["sec_locks"]:Z["locks_p"],n=bk([aj(dW)for dW in a1],10,a);c.append(("locks",36+26*(n-1)))
			if p["sec_detail"]:
				g=12+e("Target:")+8;t=g+56+12;u=a-12-aj("Unpin");v=u-t-6>=e("none set");C=["use","button"]+([]if v else["pin"])+["nextgrp"];J={"use":"Use","button":"Make button","pin":"Unpin","nextgrp":"Next group"};k,D=bk([aj(J[dX])for dX in C],12,a)
				if D==1:k[-1]=(a-12-aj("Next group"),0)
				Z["D"]={"tx":g,"tgt_x":t,"pin_here":v,"pin_x":u,"tgt_w":(u-6 if v else a-4)-t,"btns":list(zip(C,k))};c.append(("detail",6+24*(b2()+D)+4))
			d=p["log_lines"]if p["sec_log"]else 0
			if p["sec_log"]:c.append(("log",None))
			def q(rows,d):
				y=M+30+j
				for b,a in c:
					if b=="list":a=26+rows*ax+6
					elif b=="log":a=26+20*d+4
					y+=a+j
				return y-j+M
			K=aJ["rows"][0];i=(h-q(0,d))//ax
			while i<K and d>bB:d-=1;i=(h-q(0,d))//ax
			Z["need"]=q(bA,min(d,bB)if p["sec_log"]else 0);Z["short"]=i<bA;i=max(1,i);Z["rows"],Z["log_n"]=i,d;L=max(26+i*ax+6,h-q(0,d)+32);y=M+30+j
			for x,r in c:
				if x=="list":r=L
				elif x=="log":r=26+20*d+4
				Z[x]=(y,r);y+=r+j
			Z["H"]=y-j+M;return Z
		def c7(w,h):
			a=b3();k=1. if w>=a else w/float(a);b,c,Z=w,h,None
			for d in range(4):
				b=w if k==1. else max(a,int(round(w/k)));c=h if k==1. else int(round(h/k));Z=b4(b,c)
				if not Z["short"]:break
				k=min(k,h/float(Z["need"])*.999)
			return b,c,k,Z
		def aC(c,key,txt,room,hue=None,base=None,lbl=None):
			if lbl is None:lbl=c.get(key)
			if lbl is None:return
			b=(txt,room,hue,base);d=key+"_src"
			if c.get(d)==b:return
			c[d]=b;e=C(txt,room);n(lbl,e,hue);f=c.get(key+"_cat")
			if f is None:return
			a=base or ""if e==txt else(("%s. %s"%(txt,base))if base else txt)
			if a!=c.get(key+"_tip"):c[key+"_tip"]=a;safe(lambda:f.SetTooltip(a))
		def c8(L):b=L["IW"];Z=dict(L,total2=False,sess_own=False,log_n=p["log_lines"]);c=e("Int 125 (+25)")+8+(I(ay[2])[0]or 12)+14;Z["stats"]=([(12+f*c,0)for f in range(3)],(12+3*c,0));a=12+e("Find:")+6;Z["T"]={"tx":a,"field":a7,"filter":(a+a7+14,0),"groups":(b-12-24-e("Groups"),0)};Z["locks_p"]=bk([aj(g)for g in a1],10,b)[0];a=12+e("Target:")+8;d=b-12-aj("Unpin");Z["D"]={"tx":a,"tgt_x":a+68,"pin_here":True,"pin_x":d,"tgt_w":d-6-(a+68),"btns":[("use",(12,0)),("button",(24+aj("Use"),0)),("nextgrp",(b-12-aj("Next group"),0))]};return Z
		def b5(g,store,c,Z,k,zone=True):
			aa=E;i=Z["IW"];a=aa;aL(i,zone=zone)
			def n(key,x,y,w,hue=None,h=22,dy=0):
				a=l(g,"",x,y,hue)
				if zone:c[key+"_cat"]=K(g,x-2,y+dy-3,max(8,w+4),h,lambda:None);c[key+"_tip"]=""
				return a
			if "sum"in Z:
				f,m=Z["sum"];H(g,a,f,i,m);d=f+6
				if p["sec_summary"]:
					nl=2 if Z["total2"]else 1;c["total"]=l(g,"",a+12,d+3);ab=K(g,a+8,d,i-16,24*nl-2,lambda:None,aR)
					if zone:c["total_cat"],c["total_tip"]=ab,aR
					d+=24
					if Z["total2"]:c["total2"]=l(g,"",a+12,d+3);d+=24
					O=a+i-12-aj("Reset");c["session_w"]=i-28 if Z["sess_own"]else O-a-12-6;c["session"]=n("session",a+12,d+3,c["session_w"])
					if Z["sess_own"]:d+=24
					A(g,store,"newsess",M,O,d-1,"Reset","New session: gains count from now",on_click=ak("newsess"));d+=24
				if p["sec_stats"]:
					P=e("Int 125 (+25)")+8;ac,(R,tl)=Z["stats"];c["stats"]=[];c["stat_cats"],c["stat_tips"]=[],[None,None,None]
					for o,nm in enumerate(("Str","Dex","Int")):
						u,r=ac[o];C=d+24*r;ad=l(g,"",a+u,C+3);c["stat_cats"].append(K(g,a+u-2,C,P-4,22,ak("settings"),aP[o]));s=V(g,ay[0],a+u+P,C+5)
						if s is not None:W(s,ak(("stat",o),dup=True));z(s,"Click: %s up, down or locked"%nm)
						c["stats"].append((ad,s))
					c["stat_total_w"]=i-4-R;c["stat_total"]=n("stat_total",a+R,d+24*tl+3,c["stat_total_w"],b)
			f,m=Z["tool"];T=Z["T"];H(g,a,f,i,m);l(g,"Find:",a+12,f+10);c["search"]=z(N(g,j["search"],a+T["tx"],f+7,T["field"],numbers=False,font=max(8,int(round(16*k)))),"Type part of a skill name");c["search"].SetPlaceholder("search");fx,fl=T["filter"];c["filter"]=A(g,store,"filter",U,a+fx,f+7+28*fl,aD[p["filter"]][1],"Which skills to list (click: next)",on_click=ak("filter"));gx,gl=T["groups"];c["groups"]=Y(g,"Groups",a+gx,f+9+28*gl,p["groups"],"Show the client's skill groups (click one to fold it)");dc(g,c,a,Z["list"][0],i,Z["list"][1],Z["rows"])
			if "locks"in Z:
				f,m=Z["locks"];H(g,a,f,i,m)
				for(q,F,G),(L,r)in zip(bC,Z["locks_p"]):A(g,store,q,J,a+L,f+7+26*r,F,G,on_click=ak(q))
			if "detail"in Z:
				f,m=Z["detail"];D=Z["D"];H(g,a,f,i,m);d=f+6;S=max(I(dW)[0]for dW in ay)or 12;X=a+i-12-3*(S+10);c["d_name_w"]=X-a-12-8;c["d_locks"]=[];c["d_name"]=n("d_name",a+12,d+3,c["d_name_w"],Q)
				for v in range(3):
					t=V(g,ay[v],X+v*(S+10),d+5)
					if t is not None:W(t,ak(("dlock",v),dup=True));z(t,cA[v])
					c["d_locks"].append(t)
				d+=24;c["d_lw"]=i-28;c["d_l1"]=n("d_l1",a+12,d+3,c["d_lw"]);d+=24;c["d_l2"]=n("d_l2",a+12,d+3,c["d_lw"],b);d+=24
				if p["tips"]:c["d_tip"]=l(g,"",a+12,d+3,B);c["d_tip_cat"]=K(g,a+8,d,i-16,22,lambda:None,"Training tip for this skill's range");c["d_tip_full"]=None;d+=24
				l(g,"Target:",a+12,d+3);c["target"]=z(N(g,"",a+D["tx"],d,56,numbers=False,font=max(8,int(round(16*k)))),"Real value to stop at (empty = none)");c["target"].SetPlaceholder("none");c["d_tgt_w"]=D["tgt_w"];c["d_tgt"]=n("d_tgt",a+D["tgt_x"],d+3,D["tgt_w"],b);d+=24
				for q,(L,r)in([("pin",(D["pin_x"],-1))]if D["pin_here"]else[])+D["btns"]:
					ae,F,G,af=cr[q];ag=A(g,store,q,ae,a+L,d-1+24*r,F,G,on_click=ak(af))
					if q=="pin":c["pin"]=ag
			if "log"in Z:
				f,m=Z["log"];H(g,a,f,i,m,"RECENT GAINS");c["log"]=[];c["log_w"]=i-28
				for o in range(Z["log_n"]):c["log"].append(n("log%d"%o,a+12,f+26+20*o,c["log_w"],B,20,1))
		def bl():
			if p["x_hides"]:return "Hide %s (%s brings it back)"%(aE,"the client's Skills button"if p["replace"]else "the Action Bar's Skills button")
			return Kit.CLOSE_TIP%aE
		def a2():
			c,t["g"]=t["g"],None;aU.clear();j["desc"]=None;j["rebuild"]=None
			if j["hidden"]:t.update({"c":{},"rows":[],"rowmap":{},"store":({},{})});ab(c);return
			a=({},{});d={};j["resize_at"],j["preview"]=0.,False;t["L"]=None;L,Z=None,None;al["k"],al["full"]=1.,None
			if j["minimized"]or j["docked"]:w,h=bD,cq
			elif al["slot"]is not None:w,h=al["slot"];e,l,k,Z=c7(w,h)
			else:L=c6();w,h=L["W"],L["H"];t["L"]=L
			x,y=Kit.load_pos(bt,(160,120),(w,h))
			if T(c):x,y=c.GetX(),c.GetY()
			b=LAYOUT.placed.get(aw)if HOST.layout_holds(aw)else None
			if b is not None:x,y=int(b[0]),int(b[1])
			if Z is not None:
				g=G.CreateGump(True,True);ae(g,e,l);ar(g,a,e,aE,aw,ak("toggle_min"),ak("to_bar"),ak("settings"),close_tip=bl());b5(g,a,d,Z,k)
				if k!=1.:f=max(b3(),w);al["k"],al["full"]=k,(int(f),int(b4(f,0)["need"]));aq(g,k)
			elif L is None:g=G.CreateGump(True,True);d["mini"]=Kit.mini_bar(g,a,w,h,aE,aw,ak("toggle_min"),close_tip=bl())
			else:
				if b is None:x,y=Kit.clamp(x,y,w,h)
				g=G.CreateModernGump(x,y,w,h,True,L["min_w"],L["min_h"],da);g.SetAlpha(0);ae(g,w,h,mouse=False);ar(g,a,w,aE,aw,ak("toggle_min"),ak("to_bar"),ak("settings"),close_tip=bl());b5(g,a,d,c8(L),1.,False)
			i=Kit.show_window(g,x,y,w,h,aw,j["docked"],c4(g),bc,t,{"g":g,"c":d,"store":a,"rows":[],"rowmap":{},"w":e if Z is not None else w})
			if b is not None and i is not None and tuple(i)!=(x,y):g.SetPos(x,y);Kit.note_rect(g,x,y);Kit.moved_by_code(g)
			if b is not None:LAYOUT.fit_now(aw,g)
			if p["minimized"]!=j["minimized"]:p["minimized"]=j["minimized"];aH()
			bp();aI();bm(time.time());bo(time.time());ab(c)
		dV=None;c9=Kit.dock_hooks(aE,cm,j,t,c5)
		def da(*a):
			j["resize_at"]=time.time();g=t["g"];L=t.get("L")
			if j["preview"]or L is None or not T(g)or j["minimized"]or j["docked"]:return
			if al["width"]is None and(int(g.GetWidth()),int(g.GetHeight()))!=(L["W"],L["H"]):j["preview"]=True;g.SetAlpha(.55)
		def db():
			g=t["g"];L=t.get("L");j["preview"]=False
			if L is None or not T(g)or j["minimized"]or j["docked"]:return
			if al["width"]is not None:g.SetAlpha(0);return
			w,h=int(g.GetWidth()),int(g.GetHeight());c,d=aJ["rows"];a=max(c,min(d,(h-L["fixed_h"]+ax//2)//ax));b=w if w>L["min_w"]else 0
			if a==L["rows"]and b==p["width"]and(w,h)==(L["W"],L["H"]):g.SetAlpha(0);return
			if a!=p["rows"]or b!=p["width"]:p["rows"],p["width"]=a,b;aH();aN["sync"]=True
			j["m"]=None;j["rebuild"]="window";aK()
		def dc(g,c,j,a,IW,h,rows):
			m=aL();H(g,j,a,IW,h);d=j+8;c["hdr"]={};k=[("name","Skill",m["name_x"],"Sort by name"),("real","Real",m["real_x"],"Sort by real value without item bonuses"),("value","Value",m["val_x"],"Sort by value with bonuses"),("cap","Cap",m["cap_x"],"Sort by cap"),("gain","Gain",m["gain_x"],"Sort by gain this session")];n={"name":m["real_x"]or m["val_x"],"real":m["val_x"],"value":m["cap_x"]or m["bar_x"]or m["gain_x"]or m["lock_x"],"cap":m["bar_x"]or m["gain_x"]or m["lock_x"],"gain":m["lock_x"]}
			for i,o,e,p in k:
				if e is None:continue
				c["hdr"][i]=l(g,o,d+e,a+6,b);K(g,d+e-2,a+3,(n[i]or e+40)-e-2,20,ak(("sort",i),dup=True),p+" (again to reverse)")
			f=V(g,ay[2],d+m["lock_x"],a+7)
			if f is not None:W(f,ak(("sort","lock"),dup=True));z(f,"Sort by lock (again to reverse)")
			c["hdr"]["lock_pic"]=f;c["arrow"]=V(g,ay[1],d,a+8,mouse=False);c["sa"]=G.CreateGumpScrollArea(d,a+26,m["sa_w"],rows*ax);g.Add(c["sa"]);c["sa_xy"]=(d,a+26)
		def b6(r,y):
			if r["y"]==y:return
			r["y"]=y;a=al["k"]
			for b,x,c in r["parts"]:
				try:
					if a==1.:ah(b,x,y+c)
					else:b.SetPos(int(round(x*a)),int(round((y+c)*a)))
				except Exception:pass
		def b7(r,on):
			if r["hidden"]==(not on):return
			r["hidden"]=not on
			for a,b,b in r["parts"]:
				if a is r.get("bar"):
					if not on:av(a,"IsVisible",False)
				else:av(a,"IsVisible",on)
			if on:r["sig"]=None
		def bm(now):
			c=t["c"]
			if "sa_xy"not in c:return
			i=(j["ver"],O["ver"],int(now)if aD[p["filter"]][0]=="gaining"else 0)
			if j["desc"]is not None and i==j["desc_key"]:return
			j["desc_key"]=i;a=c2(now)
			if a==j["desc"]:return
			j["desc"]=a;m=aL();e=c["sa"];v=len(t["rowmap"])+(0 if "selbox"in c else 1)+(0 if c.get("empty")else 1)
			if "selbox"not in c:c["selbox"]=an(e,0,0,m["row_w"],ax-1,cv,cu);av(c["selbox"],"IsVisible",False)
			f=""if a else("No skill matches; change the search or the filter."if q["n"]else "Waiting for the server to send your skills.")
			if c.get("empty")is None and f:c["empty"]=l(e,f,m["name_x"],3,b)
			if c.get("empty")is not None:n(c["empty"],f);av(c["empty"],"IsVisible",bool(f))
			g=t["rowmap"];o,s,u=[],set(),{}
			for w,d in enumerate(a):
				h=w*ax;k=(d[0],d[1]);u[k]=x=u.get(k,-1)+1;k=(d[0],d[1],x);r=g.get(k)
				if r is None:r=dd(e,h,d,m)if d[0]=="g"else de(e,h,d[1],m);g[k]=r
				else:b6(r,h);b7(r,True)
				if d[0]=="g":av(r["arrow"],"Graphic",ba if d[2]else a9)
				s.add(k);o.append(r)
			for k,r in g.items():
				if k not in s and not r["hidden"]:b7(r,False);b6(r,0)
			t["rows"]=o
			if al["k"]!=1. and v!=len(g)+(0 if "selbox"in c else 1)+(0 if c.get("empty")else 1):aq(t["g"],al["k"])
			bn()
		def az(r,a,x,dy):
			if a is not None:r["parts"].append((a,x,dy))
			return a
		def dd(tgt,a,d,m):c,e=d[1],d[2];r={"kind":"g","key":c,"y":a,"hidden":False,"parts":[],"sig":None};az(r,an(tgt,0,a+1,m["row_w"],ax-2,cx,cw),0,1);r["arrow"]=az(r,V(tgt,ba if e else a9,4,a+5,mouse=False),4,5);b0(r["arrow"],"Graphic",ba if e else a9);r["lbl"]=az(r,l(tgt,"",m["name_x"],a+3,Q),m["name_x"],3);r["real"]=az(r,l(tgt,"",m["real_x"],a+3,b),m["real_x"],3)if m["real_x"]is not None else None;r["val"]=az(r,l(tgt,"",m["val_x"],a+3,b),m["val_x"],3);r["gain"]=az(r,l(tgt,"",m["gain_x"],a+3,b),m["gain_x"],3)if m["gain_x"]is not None else None;az(r,K(tgt,0,a,m["row_w"],ax-1,ak(("fold",c),dup=True),"Fold or unfold this group"),0,0);return r
		def de(tgt,a,i,m):
			r={"kind":"s","i":i,"y":a,"hidden":False,"parts":[],"sig":None};r["name"]=az(r,l(tgt,b8(i,m),m["name_x"],a+3),m["name_x"],3);r["real"]=az(r,l(tgt,"",m["real_x"],a+3),m["real_x"],3)if m["real_x"]is not None else None;r["val"]=az(r,l(tgt,"",m["val_x"],a+3),m["val_x"],3);r["cap"]=az(r,l(tgt,"",m["cap_x"],a+3,b),m["cap_x"],3)if m["cap_x"]is not None else None;r["gain"]=az(r,l(tgt,"",m["gain_x"],a+3,o),m["gain_x"],3)if m["gain_x"]is not None else None;r["bar"]=None
			if m["bar_x"]is not None:
				d=(ax-m["bar_h"])//2;e=a+d
				if I(Kit.LINE_RED)[0]>0:az(r,ad(tgt,Kit.LINE_RED,m["bar_x"],e,m["bar_w"],m["bar_h"],hue=ct),m["bar_x"],d)
				else:az(r,ad(tgt,Kit.SECTION_TILE,m["bar_x"],e,m["bar_w"],m["bar_h"],1.),m["bar_x"],d)
				r["bar"]=az(r,ad(tgt,Kit.LINE_BLUE,m["bar_x"],e,1,m["bar_h"]),m["bar_x"],d)
			f="Click: pick it (details below); double-click: its floating button"if q["click"][i]else "Click: pick it (details below)";r["cat"]=az(r,K(tgt,m["name_x"]-2,a,m["lock_x"]-m["name_x"]-2,ax-1,c3(i),f),m["name_x"]-2,0);r["tip0"]=r["cat_tip"]=f;r["use"]=None
			if q["click"][i]:c=G.CreateGumpButton("",B,aX[0],aX[1],aX[2]);c.SetPos(4,a+6);tgt.Add(c);W(c,ak(("use",i),dup=True));z(c,"Use "+q["names"][i]);r["use"]=az(r,c,4,6)
			r["lock"]=az(r,V(tgt,ay[0],m["lock_x"],a+4),m["lock_x"],4);r["tip"]=None
			if r["lock"]is not None:W(r["lock"],ak(("lock",i),dup=True));b0(r["lock"],"Graphic",ay[0])
			return r
		def b8(i,m=None):
			a=q["names"][i]if i<q["n"]else "?";m=m or aL()
			if m.get("cut"):return C(a,m["name_w"]-10)
			return a
		def bn():
			a=t["c"].get("selbox")
			if a is None:return
			y=None;b=j["sel"]
			if b is not None:
				for r in t["rows"]:
					if r["kind"]=="s"and r["i"]==b:y=r["y"];break
			if y is None:av(a,"IsVisible",False)
			else:av(a,"Pos",(0,y));av(a,"IsVisible",True)
		def df(i,now):
			if j["hl"].get(i,0)>now:return o
			if i in ao["pins"]:return Q
			return B
		def dg(now):
			s=q["cur"];v=q["n"];w=p["col_gain"];x=p["tips"];y=aL()["bar_w"]
			for r in t["rows"]:
				if r["kind"]=="g":di(r);continue
				i=r["i"]
				if i>=v:continue
				b,c,a,d=s[i];j=df(i,now);k=(b,c,a,d,aG(i)if w else 0,j)
				if k==r["sig"]:continue
				r["sig"]=k;n(r["name"],b8(i),j)
				if r["real"]is not None:n(r["real"],f1(b),o if a and b>=a else B)
				l=c-b;n(r["val"],f1(c),o if l>0 else(u if l<0 else B))
				if r["cap"]is not None:n(r["cap"],f1(a))
				if r["gain"]is not None:e=aG(i);n(r["gain"],("%+.1f"%(e/10.))if e else "",o if e>0 else u)
				if r["lock"]is not None:
					av(r["lock"],"Graphic",ay[d]);f="%s (click: %s)"%(bJ[d],bJ[(d+1)%3].lower())
					if r.get("tip")!=f:r["tip"]=f;z(r["lock"],f)
				if x:
					g=b_(i);h=r["tip0"]if g is None else "%s\n%s %s: %s"%(r["tip0"],q["names"][i],g[0],g[1])
					if h!=r["cat_tip"]:r["cat_tip"]=h;z(r["cat"],h)
				if r["bar"]is not None:m=int(y*min(1.,float(c)/a))if a>0 else 0;av(r["bar"],"Width",max(1,m));av(r["bar"],"IsVisible",m>0);av(r["bar"],"Graphic",cs if a and b>=a else Kit.LINE_BLUE)
		a3={"list":None,"n":-1,"mem":[]}
		def dh(key):
			if key=="pin":return "Pinned",[c for c in range(q["n"])if c in ao["pins"]]
			if key=="other":
				if a3["list"]is not O["list"]or a3["n"]!=q["n"]:a=O["of"];a3.update({"list":O["list"],"n":q["n"],"mem":[d for d in range(q["n"])if d not in a]})
				return "Other",a3["mem"]
			if isinstance(key,int)and key<len(O["list"]):g=O["list"][key];return g["name"]or "(no name)",g["members"]
			return "?",[]
		def di(r):
			e,b=dh(r["key"]);m=aL();j=q["n"];k=q["cur"];c=d=a=0
			for i in b:
				if i<j:
					f=k[i];c+=f[0];d+=f[1]
					if r["gain"]is not None:a+=aG(i)
			g=(m["real_x"]or m["val_x"])-m["name_x"]-6;h=(e,len(b),g,c,d,a)
			if r.get("gsig")==h:return
			r["gsig"]=h;n(r["lbl"],C("%s (%d)"%(e,len(b)),g))
			if r["real"]is not None:n(r["real"],f1(c))
			n(r["val"],f1(d))
			if r["gain"]is not None:n(r["gain"],("%+.1f"%(a/10.))if a else "")
		def dj():
			c=t["c"];h=c.get("hdr")
			if not h:return
			m=aL();s=p["sort"];i=(s,p["asc"],m);d=c.get("hdr_k")
			if d is not None and d[0]==s and d[1]==i[1]and d[2]is m:return
			c["hdr_k"]=i;f={"name":("Skill",m["name_x"]),"real":("Real",m["real_x"]),"value":("Value",m["val_x"]),"cap":("Cap",m["cap_x"]),"gain":("Gain",m["gain_x"])}
			for g,l in h.items():
				if g!="lock_pic":n(l,f[g][0],Q if g==s else b)
			a=c.get("arrow")
			if a is None:return
			j=c["sa_xy"][0]
			if s=="lock":k=j+m["lock_x"]-m["arrow_w"]-3
			elif f.get(s,(None,None))[1]is not None:o,q=f[s];k=j+q+e(o)+3
			else:av(a,"IsVisible",False);return
			r=c["sa_xy"][1]-26;av(a,"Pos",(k,r+8));av(a,"Graphic",ay[0]if p["asc"]else ay[1]);av(a,"IsVisible",True)
		a4={}
		def bo(now):
			c=t["c"]
			if not c:return
			g=bj()
			if c.get("mini")is not None:
				if j["docked"]:return
				a="%s: %s / %s %+.1f"%(aE,f1(g),f1(p["total_cap"]),bg()/10.)
				if not j["ready"]:a="%s: waiting for your skills"%aE
				n(c["mini"],C(a,bD-90),u if p["cap_warn"]and j["warned_cap"]else b);return
			dj();dg(now);bn();w=t.get("w",400)-2*E-24
			if c.get("total")is not None:
				K=sum(Z[1]for Z in q["cur"]);L=p["total_cap"]-g
				if j["warned_cap"]:h="Total %s / %s: at the cap"%(f1(g),f1(p["total_cap"]));i,A="set a skill to go down",", ";l=u
				else:h="Total %s / %s   (%s free)"%(f1(g),f1(p["total_cap"]),f1(max(0,L)));i,A="with bonuses %s"%f1(K),"   ";l=B
				a=h+A+i
				if c.get("total2")is not None:
					D,F=C(h,w),C(i,w);n(c["total"],D,l);n(c["total2"],F,l);d=aR if(D,F)==(h,i)else "%s. %s"%(a,aR)
					if d!=c.get("total_tip"):c["total_tip"]=d;z(c["total_cat"],d)
				else:aC(c,"total",a,w,l,aR)
			if c.get("session")is not None:e=bg();m=bh();a="Session %+.1f in %s   (%.1f / hour)"%(e/10.,bi(now-ag["start"]),e/10./m);aC(c,"session",a,c["session_w"],o if e>0 else b)
			if c.get("stats"):
				M=ag["stats"]or X["cur"];m=bh();G,H=c.get("stat_cats")or(),c.get("stat_tips")
				for k,(r,N)in enumerate(c["stats"]):
					I=X["cur"][k];f=I-M[k]if ag["stats"]else 0;n(r,"%s %d%s"%(("Str","Dex","Int")[k],I,(" (%+d)"%f)if f else ""),o if f>0 else B);av(N,"Graphic",ay[X["locks"][k]])
					if k<len(G):
						d=c0(k,m)
						if d!=H[k]:H[k]=d;z(G[k],d)
				x=sum(X["cur"]);s=X["cap"];a=("Stats %d / %d"%(x,s))if s else("Stats %d"%x);e=(a_(0)+a_(1)+a_(2))if ag["stats"]else 0
				if e:
					J="%s   %+d (%.1f / hour)"%(a,e,e/m)
					if Kit.text_px(J)<=c["stat_total_w"]:a=J
				aC(c,"stat_total",a,c["stat_total_w"],o if s and x>=s else b)
			dk(now)
			if c.get("log")is not None:
				y=j["log"][-len(c["log"]):][::-1]
				for k,r in enumerate(c["log"]):
					if k<len(y):
						v=y[k];f=v[2];a=a4.get(v)
						if a is None:
							O,P,R,Q=v;a="%s  %s %s%s  (%s)"%(time.strftime("%H:%M",time.localtime(O)),P,"+"if f>0 else "-",f1(abs(f)),f1(Q))
							if len(a4)>=2*aS:a4.clear()
							a4[v]=a
						aC(c,"log%d"%k,a,c["log_w"],o if f>0 else u,lbl=r)
					else:aC(c,"log%d"%k,"No gains yet this session."if k==0 and not y else "",c["log_w"],b,lbl=r)
		def dk(now):
			c=t["c"]
			if c.get("d_name")is None:return
			i=j["sel"]
			if i is None or i>=q["n"]:
				aC(c,"d_name","No skill picked",c["d_name_w"]);aC(c,"d_l1","Click a skill in the list to see it here.",c["d_lw"],b);aC(c,"d_l2","",c["d_lw"]);aC(c,"d_tgt","",c["d_tgt_w"])
				if c.get("d_tip")is not None:
					n(c["d_tip"],"")
					if c["d_tip_full"]is not None:c["d_tip_full"]=None;z(c["d_tip_cat"],"Training tip for this skill's range")
				for f in c["d_locks"]:av(f,"Hue",bF)
				return
			a,l,g,w=q["cur"][i];m=bd(i);r=O["list"][m]["name"]if m is not None else "";aC(c,"d_name",q["names"][i]+("   (%s)"%r if r else ""),c["d_name_w"],Q)
			for x,f in enumerate(c["d_locks"]):av(f,"Hue",0 if x==w else bF)
			s=l-a;y="Real %s   Value %s%s   Cap %s   %s"%(f1(a),f1(l),(" (%+.1f)"%(s/10.))if s else "",f1(g),("To cap %s"%f1(g-a))if a<g else "At cap");aC(c,"d_l1",y,c["d_lw"],B);u=bZ(i,now);A,D=u;E="Session %+.1f   %.1f / hour   last %d min %.1f / hour   cap %s"%(aG(i)/10.,A/10.,p["rate_min"],D/10.,cV(i,now,u));aC(c,"d_l2",E,c["d_lw"],b)
			if c.get("d_tip")is not None:
				v=b_(i)
				if v is not None:e,d="Tip %s: %s"%v,B
				else:e,d="No tip for this range",b
				n(c["d_tip"],C(e,c["d_lw"]),d)
				if e!=c["d_tip_full"]:c["d_tip_full"]=e;z(c["d_tip_cat"],e)
			h=ao["targets"].get(i)
			if h:
				if a>=h:k,d="reached",o
				else:k="%s to go%s"%(f1(h-a),", then locks"if p["lock_at_target"]else "");d=b
			else:k,d="none set",b
			aC(c,"d_tgt",k,c["d_tgt_w"],d)
			if c.get("pin")is not None:n(c["pin"],"Unpin"if i in ao["pins"]else "Pin")
		def bp():
			c=t["c"];a=c.get("target")
			if a is None:j["tgt_shown"]=None;return
			i=j["sel"];b=f1(ao["targets"][i])if i is not None and i in ao["targets"]else "";a.SetText(b);j["tgt_shown"]=(i,b)
		def dl(now):
			d=t["c"];b=False;e=d.get("search")
			if e is not None:
				try:q=str(e.Text or "").strip().lower()
				except Exception:q=j["search"]
				if q!=j["search"]:j["search"],b=q,True
			f=d.get("target")
			if f is not None and j["tgt_shown"]is not None:
				i,g=j["tgt_shown"]
				try:a=str(f.Text or "").strip()
				except Exception:a=g
				if a!=g and i is not None and i==j["sel"]:
					j["tgt_shown"]=(i,a)
					try:v=int(round(float(a.replace(",","."))*10))if a else 0
					except(ValueError,OverflowError):v=None
					if v is not None:
						v=max(0,min(2000,v))
						if v:ao["targets"][i]=v
						else:ao["targets"].pop(i,None)
						bM();b=True
			h=d.get("groups")
			if h is not None:
				try:c=bool(h.IsChecked)
				except Exception:c=p["groups"]
				if c!=p["groups"]:
					p["groups"]=c;aH()
					if c:aI(True)
					b=True
			return b
		def dm():
			try:
				a=VG["gumps"]
				if a is None:a=VG["gumps"]=Tz.get(None,"Gumps",Tz.T("ClassicUO.Game.Managers.UIManager"))
				return(int(a.Count),a.First)
			except Exception:VG["gumps"]=None;return
		dn=3.
		def bq():
			if not p["replace"]and time.time()>j["swallow_until"]:return
			b=time.time();a=dm()
			if a is not None and a==VG["sig"]and b<VG["full_at"]:return
			VG["sig"],VG["full_at"]=a,b+dn;VG["gumps"]=None;c=safe(lambda:Tz.windows(cl),[])or[]
			if not c:return
			VG["sig"]=None
			for d in c:d.Dispose()
			if time.time()<=j["swallow_until"]:j["swallow_until"]=0.;return
			br()
		def br():
			if j["hidden"]or j["minimized"]or j["docked"]or not T(t["g"]):j["hidden"]=j["minimized"]=j["docked"]=False;p["minimized"]=False;aH();a2()
			else:
				a=Kit.client_control(t["g"])
				if a is not None:Tz.call(None,"MakeTopMostGump",[a],Tz.T("ClassicUO.Game.Managers.UIManager"))
		def b9(key,text):
			a=time.time()
			if a-j["arm"].get(key,0.)<=cy:j["arm"].pop(key,None);return True
			j["arm"][key]=a;ac(text,b);return False
		def a5(v,a=False):
			n=0
			for i in(range(q["n"])if a else[g[1]for g in(j["desc"]or[])if g[0]=="s"]):
				d,f,c,e=q["cur"][i]
				if a and not(c and d>=c):continue
				if e!=v:aW(i,v);n+=1
			ac("%s %s."%(aa(n,"skill"),("set to go up","set to go down","locked")[v]),o if n else b)
		def do(k):
			if k>=len(aA):return
			a,b=aA[k];n=0
			for i,c in enumerate(b[:q["n"]]):
				v="udl".find(c)
				if v>=0 and q["cur"][i][3]!=v:aW(i,v);n+=1
			ac("lock set \"%s\" put on (%d change%s)."%(a,n,""if n==1 else "s"),o)
		def dp(name):
			name=re.sub(r"[|=;]","",name or "").strip()[:24]
			if not name:name="Set %d"%(len(aA)+1)
			a="".join("udl"[d[3]]for d in q["cur"])
			for k,(n,b)in enumerate(aA):
				if n.lower()==name.lower():aA[k]=(name,a);break
			else:
				if len(aA)>=bE:ac("at most %d lock sets: delete one first."%bE,u);return
				aA.append((name,a))
			bN();ac("lock set \"%s\" saved."%name,o)
		def dq(i):
			aI(True)
			if i is None or not O["list"]:ac("couldn't move the skill (the client's skill groups can't be read).",u);return
			a=bd(i);b=0 if a is None else(a+1)%len(O["list"])
			try:
				import System
				if a is not None:O["list"][a]["obj"].Remove(System.Byte(i))
				O["list"][b]["obj"].Add(System.Byte(i));aO();ac("%s moved to %s."%(q["names"][i],O["list"][bd(i)or 0]["name"]),o)
			except Exception as c:ac("couldn't move it (%s)."%Tz.why(c),u)
		def dr():
			a=aV()
			try:import System;g=System.Activator.CreateInstance(Tz.T("ClassicUO.Game.Managers.SkillsGroup"));g.Name="New group";g.IsMaximized=True;a.Add(g);aO()
			except Exception as b:ac("couldn't add a group (%s)."%Tz.why(b),u)
		def ds(gi):
			aI(True)
			if gi<=0 or gi>=len(O["list"]):return
			a=aV();b=O["list"][gi]["name"]
			if safe(lambda:a.Remove(O["list"][gi]["obj"]),False):aO();ac("group \"%s\" deleted; its skills went to \"%s\"."%(b,O["list"][0]["name"]if O["list"]else "the first group"),o)
		def dt():
			a=aV()
			try:a.MakeDefault();aO();ac("skill groups reset to the default ones.",o)
			except Exception as b:ac("couldn't reset the groups (%s)."%Tz.why(b),u)
		def du():
			b=API.Player;f=ap("Skills_%08X.txt"%int(b.Serial));c=time.time();d=["Skill sheet - %s - %s"%(b.Name or "",time.strftime("%Y-%m-%d %H:%M",time.localtime(c))),"Total %s / %s   (with bonuses %s)"%(f1(bj()),f1(p["total_cap"]),f1(sum(m[1]for m in q["cur"]))),"Str %d  Dex %d  Int %d   (stat cap %d)"%(X["cur"][0],X["cur"][1],X["cur"][2],X["cap"]),"Session %+.1f in %s"%(bg()/10.,bi(c-ag["start"])),"","%-26s %7s %7s %7s %8s  %s"%("Skill","Real","Value","Cap","Session","Lock")]
			for a in sorted(range(q["n"]),key=lambda i:q["names"][i].lower()):g,v,h,k=q["cur"][a];e=aG(a);d.append("%-26s %7s %7s %7s %8s  %s"%(q["names"][a],f1(g),f1(v),f1(h),("%+.1f"%(e/10.))if e else "",aT[k]))
			j["to_write"].append((f,"\n".join(d)+"\n"))
		def ca():au(j["to_write"],aE,"skill sheet")
		def dv():return bool(j["to_write"])
		def cb(i):
			if j["sel"]!=i:
				j["sel"]=i;bp()
				if p["sec_detail"]:aI(O["sig"]is None)
			bn()
		def a6(i):
			if i is None:ac("pick a skill first.",b)
			return i is not None
		def cc(a):
			if not isinstance(a,tuple):return a,None
			return a[0],a[1]if len(a)>1 else None
		def dw(a):j["minimized"]=not(j["minimized"]or j["docked"]);j["docked"]=False;safe(lambda:HOST.dock_forget(aw));p["minimized"]=j["minimized"];aH();j["rebuild"]="window"
		def dx(b):
			p["filter"]=(p["filter"]+1)%len(aD);aH();a=t["c"].get("filter")
			if a is not None:n(a,aD[p["filter"]][1])
		def dz(a):
			if p["sort"]==a:p["asc"]=not p["asc"]
			else:p["sort"]=a;p["asc"]=a=="name"
			aH()
		def dA(a):
			i=a if a is not None else j["sel"]
			if a6(i):cU(i)
		def dB(a):
			if not isinstance(a,int):j["pc"][a]=not j["pc"].get(a,False)
			elif a<len(O["list"]):g=O["list"][a];g["obj"].IsMaximized=g["max"]=not g["max"]
		def dC(b):
			a=j["sel"]
			if a6(a):ao["pins"]^={a};bM()
		def dD(a):
			if bW():ac("asked the server for your skills.",b)
			else:ac("couldn't ask the server (the client's skills call failed).",u)
		def dE(a):
			if a<len(aA):n=aA.pop(a)[0];bN();ac("lock set \"%s\" deleted."%n,b)
			D(aw)
		def dF(a):
			if b9("grp_reset","click Reset groups again for the default groups."):dt();D(aw)
		cd={"settings":lambda a:am(aw),"to_bar":lambda a:HOST.dock_to_bar(aw,aE),"pick":cb,"stat":lambda a:bf(a,(X["locks"][a]+1)%3),"all_up":lambda a:a5(0),"all_locked":lambda a:a5(2),"lock_capped":lambda a:a5(2,True),"export":lambda a:du(),"ls_save":lambda a:(dp(a),D(aw)),"ls_apply":do,"grp_new":lambda a:(dr(),D(aw)),"grp_del":lambda a:(ds(a),D(aw)),"grp_save":lambda a:aO(),"toggle_min":dw,"filter":dx,"sort":dz,"button":lambda a:(cb(a),bV(a)),"mkbutton":lambda a:a6(j["sel"])and bV(j["sel"]),"use":dA,"lock":lambda a:a is not None and a<q["n"]and aW(a,(q["cur"][a][3]+1)%3),"dlock":lambda a:j["sel"]is not None and aW(j["sel"],a),"fold":dB,"pin":dC,"nextgrp":lambda a:a6(j["sel"])and dq(j["sel"]),"all_down":lambda a:b9("all_down","click All down again to set every listed skill to go down.")and a5(1),"newsess":lambda a:(cR(),ac("new session; gains count from now.",o)),"ask":dD,"ls_del":dE,"grp_reset":dF};dG=[("replace","Replace the client's skills window","The paperdoll's Skills button, the Skills macro and the Action Bar open this one"),("x_hides","Close only hides it","Off: Close turns Skills off"),("bars","Progress bar per skill (value / cap)","Filled to value / cap; green at the cap"),("col_cap","Cap column","Each skill's cap"),("col_gain","Session gain column","What each skill gained this session"),("journal","Journal line for each gain or loss","The client may print its own line too (its Options)"),("lock_at_cap","Lock a skill when it reaches its cap","A rising skill locks the moment it hits its cap"),("lock_at_target","Lock a skill when it reaches its target","Set targets in the window's details"),("cap_warn","Warn at the total cap when no skill is set to go down","Journal warning and a red total when nothing can rise"),("tips","Training tips in the details and row tooltips","Classic-era advice for the skill's range")];ce=[("rows","Rows in the list:",False,"Skills shown at once (or drag a window corner)"),("total_cap","Total skill cap:",True,"The shard's total skill cap (check it in game)"),("hl_secs","Green name after a gain (s):",False,"Seconds a name stays green after a gain (0 = never)"),("rate_min","Recent pace over (minutes):",False,"Minutes the recent rate and time to cap look back")];dH=[("sec_summary","Totals and session","Total skill points and the session line"),("sec_stats","Str / Dex / Int","Stats, lock arrows and the stat cap"),("sec_locks","Lock buttons","All up, All down, All locked and Lock capped"),("sec_detail","Picked skill details","Rates, target, pin and the Use button"),("sec_log","Recent gains","The last gains, newest first")];dI="Export writes a text file to the VirtueAssistantSettings folder.";dJ="Drag a window corner: height sets the rows, width spreads the columns.";dK=("A stat set to go up locks when it rises to its target, one set to go down when it falls to it. The window's stat tooltips show gains per hour.")
		def dL(w):
			aI(O["sig"]is None);h=len(O["list"])if O["ok"]else 1;i=(w-24)//2
			def c(text,dy):return[("note",f,{"ndy":dy,"h":18})for f in Kit.wrap(text,w-24)]
			def j(k,text,dec,tip):
				def a(f,x,a):
					g=f.g;h=f.c;c=x+12+max(e(s)for r,s,r,r in ce)+10;l(g,text,x+12,a+3);n=f1(p[k])if dec else str(p[k]);h.setdefault("num",{})[k]=z(N(g,n,c,a,70,numbers=not dec),tip);i,j=aJ[k];m=("(%s-%s)"%(f1(i),f1(j)))if dec else("(%d-%d)"%(i,j));l(g,C(m,x+w-4-(c+84)),c+84,a+3,b)
					if k=="rows":d=c+84+e(m)+16;h["width_v"]=l(g,C(cf(),x+w-4-d),d,a+3,b);K(g,d-2,a,x+w-4-d,22,lambda:None,"Window width, set by dragging a corner (natural: as wide as the columns need)")
				return("custom",28,a)
			def m(f,x,c):
				a=x+12;d=f.c;d["stat_tgt"]=[]
				for k,g in enumerate(("Str","Dex","Int")):l(f.g,g+":",a,c+3);h=a+e(g+":")+8;b=str(aB[k])if aB[k]else "";i=z(N(f.g,b,h,c,44,numbers=True),"%s target (1-%d, empty = none)"%(aP[k],bb));d["stat_tgt"].append([i,b,b,0.]);a=h+44+24
			def n(f,x,a):
				g,c=f.g,f.store;l(g,"Name:",x+12,a+3);d=x+12+e("Name:")+8;h=x+w-12-aj("Save current");f.c["ls_name"]=z(N(g,"",d,a,max(60,h-d-14),numbers=False),"Name for Save current (empty = Set 1, Set 2 and so on)");A(g,c,"ls_save",J,h,a-1,"Save current","Save every skill's lock as a set (same name replaces it)");a+=28
				if not aA:l(g,"No lock sets yet. Type a name and click Save current.",x+12,a+3,b)
				i=x+w-12-aj("Delete");j=i-12-aj("Apply")
				for k,(n,m)in enumerate(aA):o,p=m.count("u"),m.count("d");l(g,C("%s  (%d up, %d down)"%(n,o,p),j-x-24),x+12,a+3);A(g,c,"ls_apply_%d"%k,J,j,a-1,"Apply","Put this set's locks on your skills");A(g,c,"ls_del_%d"%k,M,i,a-1,"Delete","Delete this lock set");a+=26
			def o(f,x,a):
				g,c=f.g,f.store;h=x+w-12-aj("Delete");f.c["grp"]=[]
				if not O["ok"]:l(g,"The client's skill groups can't be read.",x+12,a+3,u);a+=28
				for d,e in enumerate(O["list"]):
					i=z(N(g,e["name"],x+12,a,200,numbers=False),"Group name (type to rename)");l(g,aa(len(e["members"]),"skill"),x+226,a+3,b)
					if d>0:A(g,c,"grp_del_%d"%d,M,h,a-1,"Delete","Delete this group (its skills go to the first one)")
					else:l(g,"first group",h+35,a+3,b)
					f.c["grp"].append((i,d,e["name"]));a+=28
				if O["ok"]and not O["list"]:a+=28
				A(g,c,"grp_new",J,x+12,a-1,"New group","Add an empty group (Next group in the window moves skills in)");A(g,c,"grp_reset",M,x+12+aj("New group")+16,a-1,"Reset groups","Put back the client's default groups (click twice)")
			d,g=aJ["log_lines"];a={"ch":24,"pad":6};return(("WINDOW",[("check",)+v for v in dG]+[j(*y)for y in ce]+c(dJ,2),a),("SECTIONS  (what the window shows)",[("check",)+L+({"stay":G%2==0 and G<4,"dx":12+(G%2)*i},)for G,L in enumerate(dH)]+[("num","log_lines","Recent gains lines:","Lines the Recent gains part shows (%d-%d)"%(d,g),None,d,g)],a),("STAT TARGETS",[("custom",28,m),("check","lock_stat_target","Lock a stat when it reaches its target","Off: only a journal line when it gets there")]+c(dK,2),a),("LOCK SETS  (saved locks)",(("custom",28+max(1,len(aA))*26,n),),a),("GROUPS  (the client's skill groups)",(("custom",max(1,h)*28+28,o),),a),("TOOLS",[("buttons",(("export",P,"Export sheet","Write every skill's values to a file in the VirtueAssistantSettings folder"),("ask",P,"Ask server","Ask the server for fresh skill values"),("newsess",P,"New session","Start a new session: gains count from now")))]+c(dI,0),dict(a,bdy=-1,bgap=16)))
		def cf():
			if p["width"]:return "Width: %d px (drag a corner)"%p["width"]
			return "Width: natural (drag a corner)"
		def dM(ctrl,default,lo,hi,dec):
			try:a=str(ctrl.Text or "").strip()
			except Exception:a=""
			try:v=int(round(float(a.replace(",","."))*10))if dec else int(a);return max(lo,min(hi,v))
			except(ValueError,OverflowError):return default
		def dN(f):
			c=f.c;aN["skip"]=aN["sync"]
			if aN["sync"]:
				aN["sync"]=False;b=c["num"].get("rows")
				if b is not None:b.SetText(str(p["rows"]))
				if c.get("width_v")is not None:n(c["width_v"],cf())
				return
			cg(c,False)
			for b,d,g in list(c.get("grp",())):
				try:e=str(b.Text or "")
				except Exception:e=str(g or "")
				if e!=g and d<len(O["list"]):O["list"][d]["obj"].Name=O["list"][d]["name"]=e;aK();c["grp"]=[(r,m,e if m==d else v)for r,m,v in c["grp"]];j["grp_dirty_at"]=time.time()
			h=f.store
			for a in list(h[0].keys()):
				if not at(h,a):continue
				if a=="ls_save":ak.add(("ls_save",str(c["ls_name"].Text or "")),dup=True)
				elif a.startswith(("ls_apply_","ls_del_","grp_del_")):i,l,k=a.rpartition("_");ak.add((i,int(k)),dup=True)
				else:ak.add((a,),dup=True)
				HOST.poke()
		def dO(f,new):
			if aN["skip"]:new.update(p);return
			for k,a in f.c["num"].items():b,c=aJ[k];new[k]=dM(a,p[k],b,c,k=="total_cap")
		def dP(a,new):
			aK()
			if any(new[c]!=a[c]for c in cD):j["m"]=None;j["rebuild"]="window"
			j["warned_cap"]=False;j["cap_at"]=0.
		aM=Kit.Page(p,dL,aH,dP,adjust=dO,clicks=dN);dQ=.8
		def cg(c,final):
			b=time.time()
			for k,e in enumerate(c.get("stat_tgt")or()):
				if final:a=e[2]
				else:
					try:a=str(e[0].Text or "").strip()
					except Exception:continue
					if a!=e[2]:e[2],e[3]=a,b;continue
				if a==e[1]or(not final and b-e[3]<dQ):continue
				e[1]=a
				if a and not a.isdigit():continue
				v=max(0,min(bb,int(a)))if a else 0
				if v!=aB[k]:aB[k]=v;S(bI,",".join(str(d)for d in aB));aK();c_(k)
		def dR():
			if aM.f is not None:cg(aM.f.c,True)
			aM.closed();aN["sync"]=False
			if j.get("grp_dirty_at"):j["grp_dirty_at"]=0.;ak.add(("grp_save",),dup=True)
		def ch():
			j["ready"]=True
			for i in range(q["n"]):ag["base"].setdefault(i,q["cur"][i][0])
			if ag["stats"]is None and any(X["cur"]):ag["stats"]=list(X["cur"])
		def ci():g,t["g"]=t["g"],None;t.update({"c":{},"rows":[],"rowmap":{}});aU.clear();ab(g)
		bL();bO()
		def dS():
			j.update({"shutting":False,"docked":False,"hidden":False,"queue":[],"rebuild":None,"desc":None,"m":None,"ready":False,"asked":0.,"swallow_until":0.,"warned_cap":False,"hl":{},"log":[],"gains":{},"started":time.time(),"ref_at":0.,"grp_at":0.,"tgt_shown":None,"stat_pending":{},"dirty":True,"redraw_at":0.,"desc_key":None,"cap_at":0.,"resize_at":0.,"grp_dirty_at":0.,"read_at":0.,"stats_at":0.});VG.update({"gumps":None,"sig":None,"full_at":0.});bL();cO();cP();bO();cQ();j["minimized"]=p["minimized"]or HOST.dock_wanted(aw);bQ(True);bS();bT();aI(True)
			if bU():ch()
			al.update({"width":None,"rows":None,"slot":None,"k":1.,"full":None});a2();bp();HOST.dock_add(aw,dict(c9,on=br,show=br,fit=cM,exact=True,verify=True,drawn_at=cN))
			if p["replace"]:bq()
		def dT():
			a=time.time()
			if t["g"]is not None and at(t["store"],"close"):
				if p["x_hides"]:j["hidden"]=True;bc();ci();ac("hidden; %s brings it back."%("the client's or the Action Bar's Skills button"if p["replace"]else "the Action Bar's Skills button (or Skills off and on in the Modules tab)"),b)
				else:ab(t["g"]);return
			if j["resize_at"]and a-j["resize_at"]>=co and not safe(lambda:SNAP.pressed(),False):j["resize_at"]=0.;db()
			if j["grp_dirty_at"]and a-j["grp_dirty_at"]>=cE:j["grp_dirty_at"]=0.;aO()
			i=q["n"]
			if not bQ():
				while j["queue"]:
					e,f=cc(j["queue"].pop(0));c=cd.get(e)
					if c is not None:c(f)
				bq()
				if j["rebuild"]=="window":a2()
				elif t["g"]is not None and t["c"]and j["desc"]is None:bm(a)
				return
			if q["n"]!=i:j["rebuild"]="window"
			d,g={},False
			if not(j["ready"]and(t["g"]is None or not t["c"]or j["minimized"]or j["docked"])and a<j["read_at"]):
				j["read_at"]=a+cI;d=bS(not j["ready"])
				if j["stat_pending"]or a>=j["stats_at"]or not j["ready"]:j["stats_at"]=a+cJ;g=bT()
			if d:cL()
			elif g:j["dirty"]=True
			if not j["ready"]:
				if bU():ch();aY();j["rebuild"]=j["rebuild"]or "rows"
				elif a-j["started"]>3. and not j["asked"]:bW()
			elif d:cW(d,a)
			if g and j["ready"]and(aB[0]or aB[1]or aB[2]):cZ()
			if j["ready"]and ag["stats"]is None and any(X["cur"]):ag["stats"]=list(X["cur"])
			aI();h=bool(j["queue"])
			if h:aK()
			while j["queue"]:
				e,f=cc(j["queue"].pop(0));c=cd.get(e)
				if c is not None:c(f)
			if d or h or a>=j["cap_at"]:
				j["cap_at"]=a+cK;k=j["warned_cap"];cY()
				if k!=j["warned_cap"]:aK()
			bq()
			if j["rebuild"]=="window":a2();j["dirty"],j["redraw_at"]=False,a+bG;return
			if t["g"]is None or not t["c"]:return
			if not(j["minimized"]or j["docked"])and dl(a):aK()
			if not j["dirty"]and a<j["redraw_at"]:return
			j["dirty"],j["redraw_at"]=False,a+bG
			if j["minimized"]or j["docked"]:bo(a);return
			bm(a);bo(a)
		def dU():
			j["shutting"]=True
			if j.get("grp_dirty_at"):j["grp_dirty_at"]=0.;safe(lambda:Kit.on_client(aO))
			ca();bc();aH()
			if j["ready"]:aY()
			HOST.dock_remove(aw);ci();cH.close()
		return{"start":dS,"tick":dT,"stop":dU,"client_tick":True,"config_height":aM.height,"build_config":aM.build,"poll_config":aM.poll,"config_closed":dR,"thread_tick":ca,"thread_wanted":dv}
	def ay():
		W="attention";m="Training Alarm";Y="Attention_settings";aB="Attention_pos";aC="Attention_min";Z=400;x,aa=300,46;aD=7186;ab=.25;ac=1.;y=18;aE=2.;ad=60.;ae=.25;z=1.5;aF=5.;aG=60.;aH=("GM, Counselor, Seer, Admin, Administrator, Developer, Staff, Game Master");aI="";ag=("whisper","8");aJ,G=5,120;aK,q=0,600;ah=8;aj=60;ak=.5;aL=500;am=60;aM=30;aN=5.;an=(("gump","attention.gump","Gump nobody asked for",775),("staff","attention.staff","Staff in view",775),("name","attention.name","Someone says your name",824),("whisper","attention.whisper","A whisper to you",824),("hit","attention.hit","Hit while not fighting",497),("test","attention.test","Training Alarm test",775));ap=dict((bg,bh)for bg,bh,bi,bi in an);aq=("gump","staff","name","words","whisper","hit");c={"gump":True,"staff":True,"name":True,"words":True,"whisper":True,"hit":False,"markers":aH,"ignore":aI,"repeat":aJ,"hold":aK,"anyalarm":True};bf=dict(c);a={"minimized":False,"shutting":False,"docked":False,"queue":[],"open_ids":{},"last_gid":0,"me":0,"my_name":"","name_re":None,"words_re":None,"seq":0};h={"g":None,"c":{},"store":({},{})};I={"skip":False};aO={"done":False};L,r,N=af(a,m);s={"looked":False,"get":None};d={"markers":None,"text":None,"ignore":frozenset(),"ignore_text":None}
		def t(text):return str(text or "").replace(";",",").replace("="," ").strip()
		def ar():
			for k,v in Kit.codec_load(R(Y)).items():
				if k in aq or k=="anyalarm":c[k]=v=="1"
				elif k in("repeat","hold"):
					try:c[k]=max(0,min(G if k=="repeat"else q,int(v)))
					except ValueError:continue
				elif k in("markers","ignore"):c[k]=v
		def O():a=["%s=%d"%(f,1 if c[f]else 0)for f in aq+("anyalarm",)];a+=["repeat=%d"%c["repeat"],"hold=%d"%c["hold"],"markers=%s"%t(c["markers"]),"ignore=%s"%t(c["ignore"])];S(Y,";".join(a))
		def aP():
			a=c["markers"]
			if d["text"]!=a:b=[f.strip()for f in str(a or "").split(",")if f.strip()];b.sort(key=len,reverse=True);d["markers"]=re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])"%"|".join(re.escape(g)for g in b),re.IGNORECASE)if b else None;d["text"]=a
			return d["markers"]
		def at():
			a=c["ignore"]
			if d["ignore_text"]!=a:
				b=set()
				for w in str(a or "").replace(" ",",").split(","):
					w=w.strip().lower()
					if not w:continue
					try:b.add(int(w,16)if w.startswith("0x")else int(w))
					except ValueError:continue
				d["ignore"]=frozenset(b);d["ignore_text"]=a
			return d["ignore"]
		def aQ(kind):
			if ALERTS.mute:return 0
			a,b=ALERTS.setting(ap[kind]);return b if a else 0
		def au():return bool(ALERTS.shown and ALERTS.alarm)
		def av():
			if a["alarm"]:return True
			b=a["resume_at"]
			if b and 0<b-time.time()<=q+1:return True
			return bool(c["anyalarm"]and HOST.alarm_up())
		def i(kind,text,who=None,serial=0,gid=0,said=None):
			b=not a["alarm"];d=False
			for r in a["alarm"]:
				if r["who"]==who:
					if r["text"]==text or(said is not None and r["said"]==said):return False
					d=True
			e=time.time()
			if b:a["seq"]+=1
			a["alarm"].append({"kind":kind,"text":text,"who":who,"serial":int(serial or 0),"gid":int(gid or 0),"at":e,"said":said})
			if len(a["alarm"])>ah:del a["alarm"][:-ah]
			a["resume_at"]=0.
			if b:a["banner_seen"]=False;f=c["repeat"];a["next_sound"]=e+f if f>0 else 0.
			if d:k();return True
			HOST.alert(ap[kind],text,"alarm",who="%s#%d"%(who or text,a["seq"]));k();return True
		def Q(how):
			if not a["alarm"]:return
			d=a["alarm"][-1];a["alarm"]=[];b=c["hold"];a["resume_at"]=time.time()+b if b>0 else 0.
			if how!="banner"and au()and d["text"]and str(ALERTS.line).endswith(d["text"]):ALERTS.dismiss()
			N("answered; %s"%(("skill loops go on in %d s."%b)if b else "skill loops go on."),o);a["last_answered"]=d;k()
		def aR(now):
			if not a["alarm"]:return
			if au():a["banner_seen"]=True
			elif a["banner_seen"]:Q("banner");return
			b=c["repeat"]
			if b>0 and not a["next_sound"]:a["next_sound"]=now+b
			if b>0 and not 0<a["next_sound"]-now<=b:
				a["next_sound"]=now+b;d=aQ(a["alarm"][-1]["kind"])
				if d:API.PlaySound(d)
			if not 0<a["flash_at"]-now<=ak:a["flash_at"]=now+ak;a["flash_on"]=not a["flash_on"];k()
		def aS(now,p):
			if a["my_name"]and 0<=now-a["name_at"]<aN:return
			a["name_at"]=now;b=str(p.Name or "").strip();a["me"]=int(p.Serial)
			if b and b!=a["my_name"]:
				a["my_name"]=b;a["name_re"]=re.compile(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])"%re.escape(b),re.IGNORECASE);c=[f for f in re.split(r"[^A-Za-z0-9']+",b)if f];d=[g for g in c if len(g)>=4]
				if len(c)>1 and d:a["words_re"]=re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])"%"|".join(re.escape(bg)for bg in d),re.IGNORECASE)
				else:a["words_re"]=None
		def aT(g):
			if g is None:return
			try:a=g.Gump
			except Exception:return g
			return a if a is not None else g
		def T(g):
			try:return bool(g.IsDisposed)
			except Exception:return True
		def aU():
			if not s["looked"]:
				s["looked"]=True;a=[];t=ai("ClassicUO.Input.Mouse")
				if t is not None:
					for b in("Position","LastLeftButtonClickTime","LastRightButtonClickTime"):
						m=Client._member(t,b)
						if m is not None:a.append((m[0],b=="Position"))
				s["get"]=a or None
			return s["get"]
		def aV(now):
			c=aU()
			if not c:return
			b=[]
			for e,f in c:v=e();b.append((int(v.X),int(v.Y))if f else int(v))
			b=tuple(b);d,a["input"]=a["input"],b
			if d is not None and b!=d:a["asked_at"]=now
			return True
		def aW(now):
			t=bool(HOST.typing());b,a["typing"]=a["typing"],t
			if b is not None and t!=b:a["typed_at"]=a["asked_at"]=now
		def aX(now):
			aW(now)
			if aV(now)is None:
				f=bool(API.HasTarget("any"))
				if a["cursor_up"]and not f:a["asked_at"]=now
				a["cursor_up"]=f
				if 0<=now-a["used_at"]<=z:a["asked_at"]=max(a["asked_at"],a["used_at"])
			b=int(API.HasGump()or 0);d=a["gump_obj"]
			if b and d is not None and b==a["gump_gid"]and not T(d):a["open_ids"][b]=now;return
			g=aT(API.GetGump(b))if b else None
			if g is d or(g is not None and d is not None and b==a["gump_gid"]and not T(d)):
				a["gump_obj"]=g
				if b:a["open_ids"][b]=now
				return
			if d is not None and a["gump_vis"]and T(d):a["asked_at"]=now
			a["gump_obj"],a["gump_gid"]=g,b
			if g is None:a["gump_vis"]=False;return
			h=bool(g.IsVisible);a["gump_vis"]=h;a["last_gid"]=b;e=a["open_ids"];j=e.get(b);e[b]=now
			if len(e)>am:
				for k in sorted(e,key=e.get)[:len(e)-am]:del e[k]
			if HOST.gump_expected(b,now):return
			if not a["primed"]or not h or b in at():return
			if j is not None and 0<=now-j<=aG:return
			if 0<=now-a["asked_at"]<=z:return
			if c["gump"]:i("gump","A gump opened by itself (id 0x%X)"%b,"gump 0x%X"%b,gid=b)
		def aY(now):
			d=aP()
			if d is None:return
			k=al(y);e,c,l=a["checked"],a["staff_seen"],a["me"]
			if len(e)>aL or d is not a["checked_pat"]:e.clear();a["checked_pat"]=d
			for m in k:
				try:s=int(m.Serial)
				except Exception:continue
				if s==l:continue
				b=e.get(s)
				if b is None or(not b[0]and b[2]<2 and now-b[1]>=aE):
					try:
						f=str(m.Name or "");g=f
						try:
							h=m.raw.NameAndProps(False)
							if h:g=f+"\n"+str(h).split("\n")[0]
						except Exception:pass
					except Exception:continue
					b=(bool(d.search(g)),now,(b[2]if b else 0)+1,f);e[s]=b
				if not b[0]:continue
				j=c.get(s);c[s]=now
				if j is None or not 0<=now-j<=ad:i("staff","Staff in view: %s"%(b[3]or "someone"),"staff %X"%s,serial=s)
			if len(c)>50:
				for n in[p for p,w in c.items()if not 0<=now-w<=ad]:del c[n]
		def aw(name):
			a=name.lower()
			try:
				for m in al(y):
					if str(m.Name or "").lower()==a:return int(m.Serial)
			except Exception:pass
			return 0
		def ax(text):text=" ".join(str(text).split());return text if len(text)<=aj else text[:aj-2]+".."
		def aZ(now):
			e=a["rd"]
			if e is None:return
			f=e.new()
			if not f:return
			g=a["my_name"].lower();h=a["name_re"];j=a["words_re"]if c["words"]else None
			for k in f:
				b=(k.name or "").strip();d=k.text
				if not b and ": "in d:b,d=[p.strip()for p in d.split(": ",1)]
				if not b or b.lower()=="system":continue
				l=b.lower()
				if g and l==g:
					if 0<=now-a["typed_at"]<=aF:a["asked_at"]=now
					continue
				if not c["name"]or h is None:continue
				if h.search(d)or(j is not None and j.search(d)):i("name",'%s said your name: "%s"'%(b,ax(d)),b,serial=aw(b),said=d)
		def a_():
			q=a["heard"]
			if not q:return
			a["heard"]=[];d=a["my_name"].lower()
			for e,b,f in q:
				if not b or b.lower()=="system"or(d and b.lower()==d):continue
				if f in ag and c["whisper"]:i("whisper",'%s whispers to you: "%s"'%(b,ax(e)),b,serial=aw(b),said=e)
		def a0(*b):
			if a["active"]:a["used_at"]=time.time()
		U={}
		def a1(*d):
			if not a["active"]:return
			for b in d:
				try:
					c=b.MessageType;m=U.get(c)
					if m is None:
						m=str(c).lower()
						if len(U)<64:U[c]=m
				except Exception:continue
				if m in ag:
					try:e=str(b.Text or "");f=str(b.Name or "")
					except Exception:continue
					q=a["heard"]
					if len(q)<aM:q.append((e,f,m))
				return
		def a2(*b):
			if c["hit"]and not a.get("hit_poke"):a["hit_poke"]=True;HOST.poke("skills.alarm",False)
		def a3():Kit.hook_once(aO,"done",("ObjectUsed",a0),("JournalEntryAdded",a1),("OnPlayerHitsChanged",a2))
		def a4(p):
			if not c["hit"]:a["hp"]=None;return
			b=int(p.Hits);d=a["hp"];a["hp"]=b
			if d is None or p.IsDead or p.InWarMode or b>=d:return
			i("hit","You took %d damage while not fighting"%(d-b),"hit")
		def ay():
			if Follow.alt_held():
				b=a["alarm"][-1]if a["alarm"]else a.get("last_answered")
				if b is not None and b.get("serial"):r(("follow",b["serial"]))()
				return
			if a["alarm"]:r("answer")();return
			if a["minimized"]:
				c=time.time()
				if 0<=c-a.get("mini_click",0.)<=.6:a["mini_click"]=0.;r("toggle_min")()
				else:a["mini_click"]=c
		def az():
			g,n,c=j.begin(Z,E+30+F+96+E);d=E
			if a["minimized"]:c["line_w"]=x-90;c["alarm_hit"]=K(g,14,12,x-90,aa-24,ay,"Click: answer the alarm. Double-click: restore. Alt+click: auto-follow (again to stop)",movable=True)
			else:
				h=Z-2*d;j.frame(g);f=d+30+F;H(g,d,f,h,96);c["status"]=l(g,"",d+12,f+10,b);c["line2"]=l(g,"",d+12,f+32,b);c["line_w"]=h-28;c["alarm_hit"]=K(g,d+6,f+6,h-12,46,ay,"Click: answer the alarm. Alt+click: auto-follow (again to stop)",movable=True);i=d+12
				for o,p,m,q,s in(("here",J,"I'm here","Answer the alarm: skill loops go on (after the set pause)","answer"),("test",P,"Test","Raise a test alarm until you answer","test"),("ignore",M,"Ignore this gump","Answer and ignore this gump from now on","ignore_gump")):t=A(g,n,o,p,i,f+62,m,q,on_click=r(s));i+=35+e(m)+14
				c["ignore"]=t
			j.end(g);a["drawn"]=None;k()
		j=Kit.Window(W,m,a,h,az,aB,aC,(240,160),(x,aa),aD,L,lock=True)
		def a5():
			b=[g for f,g in(("gump","gumps"),("staff","staff"),("name","your name"),("whisper","whispers"),("hit","hits"))if c[f]]
			if a["minimized"]:return "%s: %s"%(m,("watching "+", ".join(b))if b else "nothing ticked in settings")
			return("Watching: "+", ".join(b))if b else "Nothing ticked in settings"
		def k():
			r=h["g"]
			if r is None or(a["minimized"]and a["docked"]):return
			c=h["c"];g=c.get("line_w",200);d=a["alarm"]
			if d:s=d[-1];e=("%s: "%m if a["minimized"]else "ALARM: ")+s["text"];i=u if a["flash_on"]else B;j=("+%d more. "%(len(d)-1)if len(d)>1 else "")+"Skill loops paused: click here or I'm here"
			else:k=a["resume_at"]-time.time()if a["resume_at"]else 0;e,i=a5(),b;j=("Skill loops go on in %d s"%int(k+.99))if 0<k<=q+1 else "All quiet"
			l=(e,i,j,g)
			if l==a["drawn"]:return
			a["drawn"]=l;e=C(e,g);n(c["status"],e,i)
			if "line2"in c:n(c["line2"],C(j,g),b)
			o=c.get("ignore")
			if o is not None:
				f=bool(d)and d[-1]["kind"]=="gump"
				if c.get("ignore_on")!=f:
					c["ignore_on"]=f;o.IsVisible=f;p=h["store"][0].get("ignore")
					if p is not None:p.IsVisible=f
		def V(f):
			d=0
			if f:
				for r in reversed(a["alarm"]):
					if r["kind"]=="gump"and r["gid"]:d=r["gid"];break
			if not d:d=a["last_gid"]
			if not d:N("no server gump seen yet.",b);return
			if d not in at():e=c["ignore"].strip().strip(",");c["ignore"]=(e+", "if e else "")+"0x%X"%d;O();D(W);N("gump 0x%X ignored."%d,b)
		def a6(action):V(True);Q("click")
		a7={"follow":lambda action:Follow.toggle(action[1],m),"answer":lambda action:Q("click"),"test":lambda action:i("test","Test alarm: answer it to go on","test"),"ignore_gump":a6,"ignore_last":lambda action:V(False)}
		def a8(w):a={"top":32,"ldy":4,"fh":30,"align":True,"sh":126};return(("TRIGGERS  (each pauses skill loops too)",(("check","gump","A server gump nobody asked for","Not within %.1f s of your mouse, typing or a gump closing; not a page of an open window or an ignored id"%z),("check","staff","Staff in view (a staff word in name or title)","Within %d tiles, a name or title holding a staff word (list below)"%y),("check","name","Someone says your name","Read from the game (whole words, any case)"),("check","words","Or any word of it with 4 letters or more","For a name of two words or more: \"Wolf\" in \"Grey Wolf\"",{"dx":34}),("check","whisper","Someone whispers to you","Lines the client marks as whispered"),("check","hit","You take damage while not in war mode","Something hurts you while you train (off at first)")),{"top":32,"sh":194}),("STAFF AND GUMPS",(("text","markers","Staff words:","Words marking a staff name or title, commas between (whole words, any case; empty: no check)"),("text","ignore","Gump ids to ignore:","Gump ids that never raise the alarm: hex (0x1A2B) or decimal, commas between"),("buttons",(("ignore_last",J,"Ignore last gump","Ignore the last server gump seen",r("ignore_last")),),{"bdy":0,"stay":True}),("note",aA(),{"dx":12+35+e("Ignore last gump")+14,"ndy":3,"key":"last"})),a),("ALARM  (sound: Settings > Alerts)",(("num","repeat","Repeat the sound every:","Seconds between sounds until you answer (0-%d, 0 = once)"%G,"s",0,G),("num","hold","Loops stay paused after you answer:","Seconds loops stay paused after you answer (0-%d, 0 = none)"%q,"s",0,q),("check","anyalarm","Any alarm pauses skill loops","While any module's alarm banner waits for a click (Ultima Tracker > Lookout, a red in your house)")),dict(a,fw=40,ugap=12)))
		def aA():return("Last server gump: 0x%X"%a["last_gid"])if a["last_gid"]else "No server gump seen yet"
		def a9(f):
			I["skip"]="ignore_last"in a["queue"]
			if I["skip"]:a["queue"].remove("ignore_last");V(False)
		def ba(f,new):
			if I["skip"]:new.update(c);return
			for k in("markers","ignore"):v=t(new[k]);new[k]=v if v!=t(c[k])else c[k]
			n(f.c["last"],aA(),b)
		def bb(b,new):a["drawn"]=None
		v=Kit.Page(c,a8,O,bb,adjust=ba,clicks=a9);ar()
		def bc():
			a.update({"shutting":False,"docked":False,"active":True,"alarm":[],"queue":[f for f in a["queue"]if f=="ignore_last"],"resume_at":0.,"next_gump":0.,"gump_obj":None,"gump_gid":0,"gump_vis":False,"primed":False,"input":None,"asked_at":0.,"used_at":0.,"cursor_up":False,"typing":None,"typed_at":0.,"next_staff":0.,"checked":{},"staff_seen":{},"name_at":0.,"next_hit":0.,"hp":None,"heard":[],"next_sound":0.,"banner_seen":False,"flash_at":0.,"flash_on":False,"drawn":None,"last_answered":None,"rd":X(),"checked_pat":None,"minimized":j.start_min()});ar();a3()
			for k,b,c,d in an:HOST.alert_kind(b,c,d)
			L.service("attention.up",av);az();j.dock()
		def bd():
			if h["g"]is None:return
			if ao(h):return
			b=time.time()
			while a["queue"]:
				d=a["queue"].pop(0)
				if j.action(d):continue
				e=a7.get(d[0]if isinstance(d,tuple)else d)
				if e is not None:e(d)
			p=HOST.me()
			if p is None:return
			aS(b,p)
			if not 0<a["next_gump"]-b<=ab:a["next_gump"]=b+ab;aX(b);a["primed"]=True
			if c["staff"]and not 0<a["next_staff"]-b<=ac:a["next_staff"]=b+ac;aY(b)
			aZ(b);a_()
			if a.pop("hit_poke",False)or not 0<a["next_hit"]-b<=ae:a["next_hit"]=b+ae;a4(p)
			aR(b)
			if not a["alarm"]and a["resume_at"]:
				if not av():a["resume_at"]=0.
				k()
		def be():a["shutting"]=True;a["active"]=False;a["alarm"]=[];a["resume_at"]=0.;O();a["rd"]=None;a["gump_obj"]=None;L.close()
		return{"start":bc,"tick":bd,"stop":be,"client_tick":True,"config_height":v.height,"build_config":v.build,"poll_config":v.poll,"config_closed":v.closed}
	def az():
		p="skillbags";Z="Skill Bags";aW="SkillBags_settings";bo="SkillBags_pos";bp="SkillBags_min";aX="SkillBags_rules";aY="SkillBags_done";bq=740;aZ,br=240,46;bs=3702;a_=42;aJ=8;ax=300;bt=6;bu=5.;bv=2.;aK=3.;bw=2.5;bx=6.;by=1.5;bz=4;bA=10.;bB={"item identification":3.,"arms lore":3.,"detect hidden":3.};ay,aL=.5,60.;a0=1;aM=.25;az=.5;bC=5372;bD=("must wait","too far away","cannot reach","can't reach","can't see that","cannot see that","already casting","you are busy");bE="Paused: guard zone";bF=HOLD_TEXT["unknown"];bG="SkillBags_results_pos";a1=200;a2=16;bH=680;aA=18;aB="skillbags.results";a3="Skill Bags Results";bI=500;aN=2*E+30+F+30+24+8;bJ="No results shown. Click a rule's Results.";bK=160;bL="SkillBags_%08X_rule%d.txt";bM=("durable","substantial","massive","fortified","indestructable","indestructible","defense","guarding","hardening","fortification","invulnerability","accurate","ruin","might","force","power","vanquishing","silver","slaying","slaughter","thrashing","repond","terathan","bane","reptilian death","dismissal","gargoyle's foe","damnation","exorcism","ophidian","spider's death","arachnid doom","dousing","dissipation","vacuum","elemental health","earth shatter","blood drinking","summer wind","elemental ban","slayer","magic");bN="unidentified";bO={"itemid":{2:"not certain"},"armslore":{2:"not certain",4:"read"},"tasteid":{2:"not certain",4:"read"},"removetrap":{1:"disarmed",2:"trap, not disarmed",3:"no trap"},"lockpick":{1:"unlocked",2:"still locked",3:"not locked"},"cartography":{1:"decoded",2:"not decoded",3:"can't decode"}};bP=re.compile(r"\b("+"|".join(bM)+r")\b");bQ=re.compile(r"\[[^\]]*:\s*\d+\s*\]");bR=re.compile(r"\bmagic\b");ab=[("itemid","Item Identification","skill","Item Identification",3.2,0,(),("not certain","no idea how much","tell much about it"),()),("armslore","Arms Lore","skill","Arms Lore",3.2,0,(),("not certain","tell much about it"),()),("tasteid","Taste Identification","skill","Taste Identification",10.2,0,(),("not certain","tell much about it","can't tell"),()),("removetrap","Remove Trap","skill","Remove Trap",10.2,1,("render the trap harmless","successfully"),("fail to disarm",),("doesn't appear to be trapped","isn't trapped","not trapped")),("lockpick","Lockpicking (uses lockpicks)","tool",bC,1.5,1,("lock quickly yields",),("unable to pick the lock",),("does not appear to be locked","cannot be picked by normal means","did not need to be unlocked")),("cartography","Cartography (decode maps)","use",None,1.,3,("successfully decode",),("fail to make anything of the map",),("too difficult to attempt to decode","not a map")),("use","Double-click each item","use",None,1.,0,(),(),()),("cskill","Custom skill (name in Custom)","cskill",None,10.2,0,(),(),()),("ctool","Custom tool (graphic in Custom)","ctool",None,1.5,0,(),(),()),];bS=[cz[1]for cz in ab];aq=[("all","Every item"),("containers","Containers only"),("graphics","Graphics in Text (hex)"),("name","Name contains Text")];bT=[cA[1]for cA in aq];bU={1:"OK",2:"failed",3:"skipped",4:"done"};q={"hidden":True,"war":True,"open":True,"retries":a0,"guard":True};cy=dict(q);h=[];c={"minimized":False,"shutting":False,"docked":False,"queue":[]};K={"g":None,"c":{},"store":({},{}),"rows":[]};aO,W,m=af(c,Z);L={"f":None,"rows":[],"next_read":0.};k={"g":None,"rule":None,"c":{},"rows":[],"page":0,"dirty":False,"minimized":False,"shutting":False,"docked":False,"queue":[]}
		def a4(s):return str(s or "").replace("|","/").replace("~","-")
		def a5(v,default):
			try:v=float(v)
			except Exception:return default
			return max(ay,min(aL,v))
		def a6(action=0):a=ab[action];return{"action":action,"bag":0,"filt":a[5],"text":"","custom":"","delay":a[4],"deep":False,"auto":False,"done":{},"order":[]}
		def V(r):return ab[r["action"]]
		def aP(r):a=ab[r["action"]];b=a[3]if a[2]=="skill"else r["custom"].strip()if a[2]=="cskill"else "";return bB.get(b.lower(),bA)if b else 0.
		def a7(text):
			b=[]
			for a in str(text or "").replace(";",",").split(","):
				a=a.strip()
				if not a:continue
				try:b.append(int(a,16)if a.lower().startswith("0x")else int(a,0))
				except Exception:
					with Kit.quiet:b.append(int(a,16))
			return b
		def a8():
			p=R(aW).split("|")
			if len(p)>=4:
				for n,k in enumerate(("hidden","war","open")):q[k]=p[n]=="1"
				try:q["retries"]=max(0,min(9,int(p[3])))
				except Exception:q["retries"]=a0
			q["guard"]=(p[5]=="1")if len(p)>=6 else True;del h[:];a=R(aX)
			if a:
				for e in a.split("|"):
					f=e.split("~")
					if len(f)<8:continue
					try:r=a6(max(0,min(len(ab)-1,int(f[0]))));r.update({"bag":int(f[1])if f[1]else 0,"filt":max(0,min(len(aq)-1,int(f[2]))),"text":f[3],"custom":f[4]});r.update({"delay":max(a5(f[5],V(r)[4]),aP(r)),"deep":f[6]=="1","auto":f[7]=="1"});h.append(r)
					except Exception:continue
					if len(h)>=aJ:break
			a=R(aY)
			if a:
				b=a.split("|")
				for i,r in enumerate(h):
					if i>=len(b):break
					for d in b[i].split(","):
						if ":"not in d:continue
						s,c=d.split(":",1)
						try:s,c=int(s),int(c)
						except Exception:continue
						r["done"][s]=c;r["order"].append(s)
		def ad():S(aW,"|".join(["1"if q["hidden"]else "0","1"if q["war"]else "0","1"if q["open"]else "0",str(q["retries"]),"0","1"if q["guard"]else "0"]));S(aX,"|".join("~".join([str(a["action"]),str(a["bag"]),str(a["filt"]),a4(a["text"]),a4(a["custom"]),"%.2f"%a["delay"],"1"if a["deep"]else "0","1"if a["auto"]else "0"])for a in h));aQ()
		def aQ():S(aY,"|".join(",".join("%d:%d"%(d,a["done"][d])for d in a["order"]if d in a["done"])for a in h))
		def aC(r,serial,code):
			if serial not in r["done"]:r["order"].append(serial)
			r["done"][serial]=code;a=r["order"]
			if len(a)>ax:
				k=len(a)-ax;b=r["done"]
				for d in a[:k]:b.pop(d,None)
				del a[:k]
			c["save_done"]=True
		def bV(a,code,answer):
			if a[0]=="itemid"and code in(1,4):
				b=(answer or "").lower()
				if not b:return "no answer"
				if bN in b:return "unidentified"
				if bQ.search(b):return "magic"
				k=b.find("[")
				if k>=0:return "magic"if bP.search(b,k)else "plain"
				return "magic"if bR.search(b)else "plain"
			c=bO.get(a[0])
			if c is not None and code in c:return c[code]
			return bU.get(code,"done")
		def aR(j):
			if j.get("match_raw"):return j["match_raw"]
			a=j.get("raw")
			if not a:return ""
			b=(j.get("name")or "").lower();c=None
			for k in range(len(a)-1,-1,-1):
				d,e=a[k];f=e.lower()
				if((b and(f==b or(len(b)>=3 and b in d.lower())))or d.lstrip().startswith("[")):return d
				if c is None and(not e or f=="system"):c=d
			return c if c is not None else a[-1][0]
		def aD(r,serial,code,name,answer,tag=None):
			a=r.get("_res")
			if a is None:a=r["_res"]=[]
			for b in range(len(a)-1,-1,-1):
				if a[b][1]==serial:del a[b];break
			answer=str(answer or "").replace("\n"," ").strip()[:bK];a.append((time.time(),serial,name or("0x%08X"%serial),code,tag or bV(V(r),code,answer),answer))
			if len(a)>a1:del a[:-a1]
			r.pop("_rescount",None)
			if k["rule"]is r:k["dirty"]=True
		def aS(r):
			r.pop("_res",None);r.pop("_rescount",None)
			if k["rule"]is r:k["dirty"]=True
		def a9(r):
			a=r.get("_rescount")
			if a is None:
				b=r.get("_res")or[]
				if not b:a="No results yet."
				else:
					c={}
					for e in b:c[e[4]]=c.get(e[4],0)+1
					a="%s: %s"%(aa(len(b),"item"),", ".join(["%d %s"%(f,d)for d,f in sorted(c.items(),key=lambda a:(-a[1],a[0]))]))
				r["_rescount"]=a
			return a
		ar=Kit.find_item
		def ai(r,short=True):
			if not r["bag"]:return "no bag yet"
			c=time.time();b=r.get("_bagname")
			if b is not None and b[0]==r["bag"]and c<b[1]:a=b[2]
			else:
				d=ar(r["bag"])
				if d is None:a="bag not found"
				else:a=safe(lambda:str(d.Name or ""),"")or "0x%08X"%r["bag"]
				r["_bagname"]=(r["bag"],c+bv,a)
			return a if short else "%s  0x%08X"%(a,r["bag"])
		def aE(r=None):
			for a in([r]if r is not None else h):a.pop("_cache",None);a.pop("_bagname",None)
		def ba(r,it):
			f=aq[r["filt"]][0]
			if f=="all":return True
			if f=="containers":
				try:return bool(it.IsContainer)
				except Exception:return False
			if f=="graphics":
				try:return int(it.Graphic)in r["_gfx"]
				except Exception:return False
			if f=="name":
				b=r["text"].strip().lower()
				if not b:return True
				a=""
				try:a=str(it.Name or "")
				except Exception:pass
				if not a:
					try:a=str(API.ItemNameAndProps(it.Serial,False)or "").split("\n")[0]
					except Exception:a=""
				if not a:return
				return b in a.lower()
			return True
		def bW(serial):
			try:return int(API.Contents(serial)or 0)
			except Exception:return-1
		def bX(r,i,now,q=True):
			s=ar(r["bag"])if r["bag"]else None
			if s is None:r.pop("_cache",None);return[],0,False
			a=r.get("_cache");j=bW(r["bag"]);g=False
			if(a is None or a["count"]!=j or now>=a["relist"]or a["bag"]!=r["bag"]):
				if not q:
					if a is None:return
					g=None
				else:g=True
			if g:
				try:k=list(API.ItemsInContainer(r["bag"],bool(r["deep"]))or[])
				except Exception:k=[]
				if aq[r["filt"]][0]=="graphics":r["_gfx"]=set(a7(r["text"]))
				e=a["scans"]if a is not None else{};l,n=[],[]
				for d in k:
					try:c=int(d.Serial)
					except Exception:continue
					if c==r["bag"]:continue
					f=ba(r,d)
					if f is None and c in r["done"]:f=True
					if f is None:n.append((c,d))
					elif f:l.append((c,d));e.pop(c,None)
				a={"bag":r["bag"],"count":j,"relist":now+bu,"items":l,"pending":n,"scans":e};r["_cache"]=a
			elif a["pending"]:
				o=[]
				for c,d in a["pending"]:
					f=ba(r,d)
					if f is None:o.append((c,d))
					elif f:a["items"].append((c,d))
				a["pending"]=o
			e=a["scans"];h=[]
			for c,d in a["pending"]:
				p=e.get(c,0)+1;e[c]=p
				if p>=bt:e.pop(c,None);h.append((c,d));a["items"].append((c,d));aC(r,c,3);aD(r,c,3,"","its name never came","skipped (no name)");m("0x%08X skipped, its name never came (rule %d)."%(c,i+1),b)
			if h:t=set(v for v,w in h);a["pending"]=[x for x in a["pending"]if x[0]not in t]
			if len(e)>ax:e.clear()
			return a["items"],len(a["pending"]),g
		def bY(serial):
			a=ar(serial)
			if a is None:return False
			try:
				if a.Opened:return True
			except Exception:pass
			try:return int(API.Contents(serial)or 0)>0
			except Exception:return False
		def at(t,now):return not 0<t-now<=aL
		def bZ(r,now,b=True):
			a=r["bag"]
			if not a or not ag(a):return False
			if bY(a):c["opening"].pop(a,None);r["_closed"]=False;return True
			r["_closed"]=True
			if not q["open"]or not b:return False
			o=c["opening"].get(a)
			if o is None or at(o+bw+bx,now):c["opening"][a]=now;API.UseObject(a)
			return False
		def bb(now):
			if c["paused"]:return "Paused"
			b=HOST.me()
			if b is None:return "No player"
			a=HOST.fight_hold(now)
			if a=="dead":return "Dead"
			if q["hidden"]and b.IsHidden:return "Hidden"
			if a=="war":return "War mode"
			d=c["guard_paused"]
			if d=="unknown":return bF
			if d:return bE
			if a:return "Paused: "+HOLD_TEXT.get(a,a)
			if ak(p):return "Cursor busy"
			if API.HasTarget("any"):return "Cursor up"
			return
		def b_(now):
			n=len(h)
			if not n:return
			p=c["rr"]%n;f=False
			for s in range(n):
				i=(p+s)%n;r=h[i]
				if not(r["auto"]or i in c["run"])or not r["bag"]:r.pop("_closed",None);continue
				if V(r)[2]=="ctool"and i not in c["run"]:
					if r["auto"]:aF(i,r);m("rule %d: a custom tool runs only on Run."%(i+1),u)
					continue
				if not ag(r["bag"]):
					c["run"].discard(i);c["budget"].pop(i,None);m("rule %d: its bag isn't in your backpack."%(i+1),u)
					if r["auto"]:aF(i,r)
					continue
				if not bZ(r,now,i in c["run"]):continue
				g=bX(r,i,now,not f)
				if g is None:continue
				d,j,k=g
				if k:f=True;c["rr"]=i+1
				r["_count"]=(sum(1 for v,w in d if v in r["done"]),len(d));l=False;a=c["budget"]
				if i in c["run"]and V(r)[2]=="ctool"and i not in a:a[i]=(r["_count"][1]-r["_count"][0]+j)*(1+q["retries"])
				for e,t in d:
					if e in r["done"]:continue
					if not at(c["later"].get((i,e),0.),now):l=True;continue
					if i in a:
						if a[i]<=0:c["run"].discard(i);a.pop(i,None);m("rule %d stopped at its count (%s)."%(i+1,ai(r)),b);break
						a[i]-=1
					return i,r,e,t
				if i in c["run"]and not j and not l and k is not None:c["run"].discard(i);c["budget"].pop(i,None);m("%s on %s, %d of %d handled."%(V(r)[1],ai(r),r["_count"][0],r["_count"][1]),o)
			return
		def aF(i,r):
			c["run"].discard(i);r["auto"]=False;ad()
			if i<len(K["rows"]):K["rows"][i]["auto"].IsChecked=False
			if L["f"]is not None:D(p)
		def b0(i,r,serial,it,now):
			d=V(r);a=d[2];j={"rule":i,"serial":serial,"t":now,"phase":"target","reader":None,"lines":[],"raw":[],"name":safe(lambda:str(it.Name or ""),"")}
			if a in("skill","cskill"):
				e=d[3]if a=="skill"else r["custom"].strip()
				if not e:m("rule %d needs a skill name in its Custom box."%(i+1),u);aF(i,r);return False
				aj(p,aK+.5);j["reader"]=X();API.UseSkill(e)
			elif a in("tool","ctool"):
				b=d[3]
				if a=="ctool":
					f=a7(r["custom"]);b=f[0]if f else 0
					if not b:m("rule %d needs a tool graphic in its Custom box."%(i+1),u);aF(i,r);return False
				g=API.FindType(int(b),API.Backpack)
				if not g:
					if at(c["no_tool"].get(i,0.),now):c["no_tool"][i]=now+10.;m("no tool 0x%04X in your backpack for rule %d."%(int(b),i+1),u)
					c["later"][(i,serial)]=now+10.;c["run"].discard(i);return False
				aj(p,aK+.5);j["reader"]=X();API.UseObject(g.Serial)
			else:j["reader"]=X();API.UseObject(serial);j["phase"]="recover"
			c["job"]=j;return True
		bc={"t":None}
		def b1():
			t=bc["t"]
			if t is None:
				a=set([APP_NAME.lower()+":"])
				for b in HOST.slots:
					a.add(str(b.title).lower()+":")
					for c in(b.parts or()):
						if len(c)>1:a.add(str(c[1]).lower()+":")
				t=bc["t"]=tuple(a)
			return t
		def b2(j,a):
			c=(a.kind or "").upper()
			if c=="CLIENT"or a.low.startswith(b1()):return False
			b=(a.name or "").strip().lower()
			if not b or b=="system":return True
			if c!="OBJECT":return False
			if not j["name"]and not j.get("named"):j["named"]=True;d=ar(j["serial"]);j["name"]=safe(lambda:str(d.Name or "")if d is not None else "","")
			return b==j["name"].strip().lower()or a.text.startswith("[")
		def aT(j,a):
			f=j["reader"]
			if f is None:return
			b,e=j["lines"],j["raw"];g=False
			for c in f.new():
				if c.text and not c.text.startswith(Z):
					if not b2(j,c):continue
					b.append(c.low);g=True;e.append((c.text,c.name or ""))
					if len(b)>40:del b[:-40];del e[:-40]
			if not b:return
			if not g:return j.get("res")
			d=next(((r,i)for r,s in(("busy",bD),("skip",a[8]),("ok",a[6]),("fail",a[7]))for t in s for i in range(len(b))if t in b[i]),None)
			if d is not None:j["match"]=b[d[1]];j["match_raw"]=e[d[1]][0]
			h=j["res"]=d[0]if d is not None else None;return h
		def av(j,r,res,now):
			i,a=j["rule"],j["serial"];b=(i,a);d=None;e=aP(r)if res=="busy"else 0.
			if e>0 and "must wait"in(j.get("match")or ""):c["later"][b]=now+e;d=now+min(r["delay"],e)
			elif res=="busy":
				n=c["busy_n"].get(b,0)+1
				if n>=bz:c["busy_n"].pop(b,None);aC(r,a,2);aD(r,a,2,j["name"],aR(j)or "no answer from the shard","no answer");m("giving up on 0x%08X (no answer from %s)."%(a,V(r)[1]),u)
				else:c["busy_n"][b]=n;c["later"][b]=now+by
			elif res=="fail":
				c["busy_n"].pop(b,None);f=r.setdefault("_tries",{});n=f.get(a,0)+1
				if n<=q["retries"]:f[a]=n;c["later"][b]=now+max(r["delay"],1.)
				else:f.pop(a,None);aC(r,a,2);aD(r,a,2,j["name"],aR(j))
			else:c["busy_n"].pop(b,None);g={"ok":1,"skip":3}.get(res,4);aC(r,a,g);aD(r,a,g,j["name"],aR(j))
			c["job"]=None;h=max(0.,now-j.get("t",now));c["next_scan"]=d if d is not None else now+(r["delay"]if res=="busy"else max(ay,r["delay"]-h));c["status"]="%s: %s"%(V(r)[1],res or "done")
			if j.get("match"):r["_last"]="%s: %s"%(res,j["match"])
			elif j["lines"]:r["_last"]="%s, no phrase matched; the shard said: %s"%(res or "no answer",j["lines"][-1])
			else:r["_last"]="%s, no journal line in %.1f s"%(res or "no answer",max(0.,now-j.get("t",now)))
			if len(c["later"])>400:
				for k in[s for s,v in c["later"].items()if at(v,now)]:c["later"].pop(k,None)
			if len(c["busy_n"])>400:c["busy_n"].clear()
			if len(r.get("_tries",{}))>ax:r["_tries"].clear()
		def b3(now):
			j=c["job"];r=h[j["rule"]]if j["rule"]<len(h)else None
			if r is None:O(p);c["job"]=None;return
			b=V(r)
			if j["phase"]=="target":
				a=aT(j,b)
				if a:O(p);av(j,r,a,now);return
				if HOST.cursor_ok(p,"neutral"):API.Target(j["serial"]);O(p);j["phase"],j["t"]="recover",now
				elif ak(p)is None and API.HasTarget("any"):O(p);av(j,r,"busy",now)
				elif now-j["t"]>aK:O(p);av(j,r,"busy",now)
				return
			if now-j["t"]<max(r["delay"],ay):
				a=aT(j,b)
				if a in("busy","skip","fail"):av(j,r,a,now)
				return
			av(j,r,aT(j,b),now)
		def b4():
			e=not c["paused"]and(bool(c["run"])or any(f["auto"]and f["bag"]for f in h));a=None
			if e and(q["guard"]or "attention.up"not in HOST.services):a=HOST.guard_hold()
			if a!=c["guard_paused"]:
				c["guard_paused"]=a
				if e:
					if a=="guard":d="%s: paused in a guard zone; it goes on when you leave."%Z
					elif a=="unknown":d=("%s: paused until the guard zone is known; cross a town's guard line once."%Z)
					else:d="%s: out of the guard zone; going on."%Z
					API.SysMsg(d,b)
		b5=1.5
		def b6(now):
			if c["job"]is not None:b3(now);return
			if not at(c["next_scan"],now):return
			b4()
			if not c["run"]and not any(f["auto"]and f["bag"]for f in h):
				c["next_scan"]=now+az
				if now>=c["idle_at"]:c["idle_at"]=now+b5;c["status"]=bb(now)or "Idle"
				return
			c["idle_at"]=0.;a=bb(now)
			if a:c["status"]=a;c["next_scan"]=now+az;return
			b=b_(now)
			if b is None:c["status"]="Watching"if any(g["auto"]and g["bag"]for g in h)else "Idle";c["next_scan"]=now+az;return
			i,r,d,e=b
			if b0(i,r,d,e,now):c["status"]="%s %d/%d"%(V(r)[1],r["_count"][0]+1,r["_count"][1])
			else:c["next_scan"]=now+az
		def b7(i):
			if c["pick"]is not None:m("already targeting a bag.",b);return
			c["pick"]=i;m("target the bag for rule %d."%(i+1),b)
			def a(serial):W.add(("picked",i,int(serial or 0)),dup=True)
			HOST.pick_target(20,a)
		def b8(i,serial):
			c["pick"]=None
			if i>=len(h):return
			if not serial:m("cancelled.",b);return
			a=ar(serial)
			if a is None or not a.IsContainer:m("that isn't a container.",u);return
			if not ag(serial):m("that bag isn't in your backpack.",u);return
			r=h[i]
			if r["bag"]!=serial:r["bag"]=serial;r["done"].clear();del r["order"][:];c["later"].clear();aE(r);aS(r)
			ad();m("rule %d uses %s."%(i+1,ai(r,False)),o);c["redraw"]=True;D(p)
		def bd():return bq,2*E+30+F+40+F+30+max(1,len(h))*a_+8
		def aw():
			r,s=bd();k=al.slot if ac(p)and not c["minimized"]else None;w,t=k if k is not None and k[0]>=r and k[1]>=s else(r,s);g,n,m=al.begin(w,t);a=E;u=[]
			if not c["minimized"]:
				i=w-2*a;al.frame(g);j=a+30+F;H(g,a,j,i,40);m["pause"]=A(g,n,"pause",P,a+12,j+9,"Resume"if c["paused"]else "Pause","Stop or restart every rule",on_click=W("pause"));v=a+12+35+e("Resume")+14;A(g,n,"add",J,v,j+9,"Add rule","Add a rule (set it up on the settings page)",on_click=W("add"));x=v+35+e("Add rule")+14;m["status"]=l(g,"",x,j+12,b);m["status_w"]=a+i-4-x;c["full_txt"]=None;o=j+40+F;H(g,a,o,i,t-o-a,"RULES  (a bag and an action each)");y=o+30;C=a+i-12-35-e("Reset");D=C-35-e("Run")-6;G=D-35-e("Bag...")-6;I=G-35-e("Results")-6;m["last_w"]=i-36-16
				if not h:l(g,"No rules yet. Click Add rule, then set its bag and action.",a+12,y+5,b)
				for q,K in enumerate(h):
					f=y+q*a_;d={};d["auto"]=Y(g,"",a+10,f+2,K["auto"],"Handle every new item that lands in this bag");d["bag"]=l(g,"",a+36,f+3,B);d["act"]=l(g,"",a+172,f+3,Q);d["prog"]=l(g,"",a+298,f+3,b);d["last"]=z(l(g,"",a+36,f+22,b),"The shard's last answer to this rule and how it was read (ok, fail, skip or busy)")
					for L,N,O,R,S,T in(("res",U,I,"Results","Show the shard's answer per item (again: close)","results"),("bag",P,G,"Bag...","Target the bag this rule works on","bag"),("run",P,D,"Run","One pass over the items not done yet","run"),("reset",M,C,"Reset","Forget what was done, so every item is handled again","reset")):A(g,n,"%s%d"%(L,q),N,O,f+1,R,S,on_click=W((T,q)))
					d["text"]=(None,None,None,None);u.append(d)
			al.end(g,{"rows":u});c["redraw"]=False;be()
		al=Kit.Window(p,Z,c,K,aw,bo,bp,mini=(aZ,br),icon=bs,cleanup=aO,lock=True);I=C
		def be():
			if c["minimized"]and c["docked"]:return
			g=K["c"].get("status")
			if g is not None:
				m=(u if c["paused"]else(o if c["job"]else b));j="mini_txt"if c["minimized"]else "full_txt";d=c.get(j)
				if d is None or d[0]!=c["status"]:d=c[j]=(c["status"],I("%s: %s"%(Z,c["status"]),aZ-90)if c["minimized"]else I(c["status"],K["c"].get("status_w",400)))
				n(g,d[1],m)
			if c["minimized"]:return
			k=time.time()
			if k<c["next_rows"]:return
			c["next_rows"]=k+aM
			for i,a in enumerate(K["rows"]):
				if i>=len(h):break
				r=h[i];l=r.get("_count");e="closed"if r.get("_closed")else "%d/%d"%l if l else ""
				if c["job"]and c["job"]["rule"]==i:e+="  working"
				elif i in c["run"]:e+="  pass"
				f=r.get("_last")or "";t=(ai(r),V(r)[1],e,f)
				if t!=a["text"]:a["text"]=t;n(a["bag"],I(t[0],130));n(a["act"],I(t[1],120));n(a["prog"],I(t[2],96));n(a["last"],I("Last: "+f if f else "Last: no answer read yet",K["c"].get("last_w",500)))
		def b9():
			a=False
			for i,b in enumerate(K["rows"]):
				if i>=len(h):break
				try:v=bool(b["auto"].IsChecked)
				except Exception:continue
				if v!=h[i]["auto"]:h[i]["auto"]=v;a=True
			if a:ad();D(p)
		aG,aU=230,120
		def aV(r):return next((a for a in range(len(h))if h[a]is r),-1)
		def ca(i):
			if i>=len(h):return
			r=h[i]
			if k["rule"]is r and T(k["g"]):aH();return
			k["rule"],k["page"]=r,0
			if T(k["g"]):k["dirty"]=True
			else:aI()
		def bf():return bI,aN+4*aA
		def aH():
			k["rule"]=None
			if ac(aB):aI()
			else:an.close()
		def cb():
			if ac(aB)or k["rule"]is not None and k["g"]is not None:aI()
			elif k["g"]is not None:an.close()
		def aI():
			a=E;i=ac(aB);z=an.slot if i else None;s,t=bf()
			if z is not None and(z[0]<s or z[1]<t):z=None
			w=z[0]if z is not None else bH;n=an.rows(aA,aN,a2)if z else a2;j=z[1]if z is not None else aN+n*aA;h=w-2*a;u=j-a-30-F-a;g,f,c=an.begin(w,j);ae(g,w,j);H(g,a,a,h,30)
			if not i:A(g,f,"close",M,w-a-54,a+4,None,"Close the results",on_click=W("res_close"))
			o=w-a-(10 if i else 66)-35-e("Export");A(g,f,"export",J,o,a+4,"Export","Write the results to a file in the VirtueAssistantSettings folder",on_click=W("res_export"));p=o-12-35-e("Clear");A(g,f,"clear",M,p,a+4,"Clear","Forget these results (items stay done; Reset handles them again)",on_click=W("res_clear"));c["title"]=l(g,"",a+30,a+7,Q);c["title_w"]=p-(a+30)-8;d=a+30+F;H(g,a,d,h,u,"RESULTS  (newest first)");q=a+h-12-35-e("Next");A(g,f,"older",U,q,d+24,"Next","Older results",on_click=W("res_older"));k=q-10-35-e("Prev");A(g,f,"newer",U,k,d+24,"Prev","Newer results",on_click=W("res_newer"));c["page_x"],c["page_y"]=k-8,d+28;c["page"]=l(g,"",c["page_x"],d+28,b);c["counts"]=l(g,"",a+12,d+28,B);c["counts_w"]=k-(a+12)-16-e("page 99 of 99");c["ans_w"]=h-12-aG-aU-8;r=[];v=d+30+24
			for x in range(n):m=v+x*aA;r.append({"name":l(g,"",a+12,m,B),"tag":l(g,"",a+12+aG,m,b),"ans":l(g,"",a+12+aG+aU,m,b),"tip":None})
			an.end(g,{"rows":r});bg()
		an=Kit.Window(aB,a3,k,k,aI,bG,default=(260,220),cleanup=aO,lock=True,owner=False,clear={"rows":[],"rule":None,"c":{}});cc={1:o,2:u,3:b,4:B}
		def bg():
			k["dirty"]=False;r,f,c=k["rule"],k["rows"],k["c"]
			if not f:return
			if r is None:n(c["title"],I(a3.upper(),c["title_w"]));n(c["counts"],I(bJ,c["counts_w"]));return
			j=aV(r)
			if j<0:aH();return
			g=len(f);l=r.get("_res")or[];m=len(l);h=max(1,(m+g-1)//g);o=k["page"]=max(0,min(k["page"],h-1));n(c["title"],I("RULE %d RESULTS: %s"%(j+1,V(r)[1]),c["title_w"]));n(c["counts"],I(a9(r),c["counts_w"]));i="page %d of %d"%(o+1,h)if h>1 else ""
			if n(c["page"],i)and i:ah(c["page"],c["page_x"]-e(i),c["page_y"])
			t=m-1-o*g;u=time.localtime()[:3]
			for v,a in enumerate(f):
				p=t-v
				if p>=0:
					w,C,x,y,q,d=l[p];s=time.localtime(w);z=time.strftime("%H:%M"if s[:3]==u else "%b %d %H:%M",s);n(a["name"],I("%s  %s"%(z,x),aG-8));A=Q if q=="magic"else cc.get(y,b);n(a["tag"],I(q,aU-8),A);n(a["ans"],I(d or "no answer",c["ans_w"]))
					if a["tip"]!=d:a["tip"]=d;a["ans"].SetTooltip(d or "")
				else:
					for B in("name","tag","ans"):n(a[B],"")
		def cd():
			r=k["rule"];i=aV(r)if r is not None else-1
			if i<0:return
			a=r.get("_res")or[]
			if not a:m("rule %d has no results to export yet."%(i+1),b);return
			e=ap(bL%(int(API.Player.Serial),i+1));d=["Skill Bags results - rule %d: %s on %s"%(i+1,V(r)[1],ai(r,False)),"Exported %s - %s"%(time.strftime("%Y-%m-%d %H:%M"),a9(r)),"","%-19s  %-10s  %-32s  %-18s  %s"%("Time","Serial","Item","Result","The shard's answer")]
			for t,s,f,j,g,h in a:d.append("%-19s  0x%08X  %-32s  %-18s  %s"%(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(t)),s,f,g,h))
			c["writes"].append((e,"\n".join(d)+"\n"))
		def bh():au(c["writes"],Z,"results")
		def ce():return bool(c["writes"])
		def cf(action):
			c["paused"]=not c["paused"];c["idle_at"]=0.
			if c["paused"]and c["job"]is not None:O(p);c["job"]=None
			a=K["c"].get("pause")
			if a is not None:n(a,"Resume"if c["paused"]else "Pause")
			m("%s."%("paused"if c["paused"]else "resumed"),b)
		def cg(action):
			if len(h)>=aJ:m("at most %d rules."%aJ,b);return
			h.append(a6());ad();aw();D(p)
			if L["f"]is None:am(p)
		def ch(action):
			i=action[1]
			if c["job"]is not None and c["job"]["rule"]==i:O(p);c["job"]=None
			elif c["job"]is not None and c["job"]["rule"]>i:c["job"]["rule"]-=1
			a=h.pop(i)
			if k["rule"]is a:aH()
			elif k["rule"]is not None:k["dirty"]=True
			c["rr"]=0;c["run"]=set(d-1 if d>i else d for d in c["run"]if d!=i);c["budget"].clear();c["later"].clear();c["busy_n"].clear();c["no_tool"].clear();ad();aw();D(p)
		def ci(action):
			i=action[1]
			if not h[i]["bag"]:m("set the bag for rule %d first (Bag button)."%(i+1),u);return
			c["run"].add(i);c["budget"].pop(i,None);c["later"].clear();aE(h[i]);c["next_scan"]=0.
		def cj(action):i=action[1];h[i]["done"].clear();del h[i]["order"][:];h[i].pop("_tries",None);h[i].pop("_last",None);aE(h[i]);c["later"].clear();aQ();m("rule %d will handle every item again (%s)."%(i+1,ai(h[i])),b)
		def ck(action):
			if k["rule"]is not None:aS(k["rule"]);k["page"]=0
		def bi(action):k["page"]+=1 if action=="res_older"else-1;k["dirty"]=True
		cl={"pause":cf,"add":cg,"remove":ch,"run":ci,"reset":cj,"bag":lambda action:b7(action[1]),"picked":lambda action:b8(action[1],action[2]),"results":lambda action:ca(action[1]),"res_close":lambda action:aH(),"res_export":lambda action:cd(),"res_clear":ck,"res_older":bi,"res_newer":bi};cm=5.;cn=118;bj=("The OK / FAIL / SKIP phrases that read the shard's answers are RunUO defaults, not checked on this shard; the window's Last line shows each rule's last answer.");bk="Hex graphics with commas (0x14FC, 0x0E76), or part of a name (treasure map)";bl="The skill's client name (Item Identification), or the tool's hex graphic (0x14FC: lockpicks)";bm=("Seconds between items (%g-%g; a skill rule waits at least its 3 or 10 s timer)"%(ay,aL));co="Also handle items in bags inside it";cp="Handle every new item that lands in the bag (the window's box too)"
		def bn(w,a=None,dds=None):
			def b(i,r):
				def b(f,x,y):g,b,c=f.g,y-30,{};l(g,"Action:",x+12,b+34);dds.append(("action",i,x+70,b+30,210,bS,r["action"]));z(l(g,"Custom:",x+296,b+34),bl);c["custom"]=z(N(g,r["custom"],x+356,b+30,130,numbers=False),bl);A(g,f.store,"rm%d"%i,M,x+f.w-12-35-e("Remove"),b+28,"Remove","Remove this rule",on_click=W(("remove",i)));l(g,"Items:",x+12,b+62);dds.append(("filt",i,x+70,b+58,210,bT,r["filt"]));z(l(g,"Text:",x+296,b+62),bk);c["text"]=z(N(g,r["text"],x+356,b+58,f.w-356-16,numbers=False),bk);z(l(g,"Delay (s):",x+12,b+90),bm);c["delay"]=z(N(g,"%g"%r["delay"],x+90,b+86,50,numbers=False),bm);c["deep"]=Y(g,"Look inside bags within the bag",x+160,b+88,r["deep"],co);c["auto"]=Y(g,"Auto (watch the bag)",x+420,b+88,r["auto"],cp);a.append(c)
				return("RULE %d  (%s)"%(i+1,I(ai(r,False),300)),(("custom",0,b),),{"sh":cn})
			return([("OPTIONS",[("check","hidden","Pause while hidden","Using a skill would reveal you"),("check","open","Open bags the client hasn't looked in","On Run, double-clicks the bag once so its contents are known",{"stay":True}),("buttons",(("add",J,"Add rule","Add a rule (a bag and an action)",W("add")),),{"dx":400}),("num","retries","Extra tries after a failure:","Retries after a FAIL phrase (0-9)",None,0,9,{"lw":268,"fw":40,"ldy":4,"ltip":True,"h":2,"clamp":False}),("check","guard","Pause in guard zones","No skill use in towns or an unknown zone; unticked counts only while Skills > Training Alarm is on",{"dx":380})]+[("note",d,{"h":18})for d in Kit.wrap(bj,w-24)or[bj]],{"pad":6})]+[b(j,s)for j,s in enumerate(h)])
		cq=Kit.Page(q,bn)
		def cr(g,x,y,w):
			a,c=[],[];f=Kit.Form(g,x,y,w,q,bn(w,a,c))
			for e,i,h,j,k,l,m in sorted(c,key=lambda d:-d[3]):b=G.CreateDropDown(k,list(l),int(m));b.SetPos(h,j);g.Add(b);a[i][e]=b
			L.update({"f":f,"rows":a,"next_read":0.})
		def cs():
			j=L["f"]
			if j is None:return
			l=time.time()
			if l<L["next_read"]:return
			L["next_read"]=l+aM;d=[];n=[]
			try:
				o=j.read(True);a=o!=q;q.update(o)
				for i,e in enumerate(L["rows"]):
					if i>=len(h):break
					r=h[i];s=False
					for f,t in(("action",ab),("filt",aq)):
						b=int(e[f].GetSelectedIndex())
						if 0<=b<len(t)and b!=r[f]:
							r[f]=b;a=True;d.append(r)
							if f=="action":s=True;r["filt"]=ab[b][5];r["delay"]=ab[b][4];r["done"].clear();del r["order"][:];aS(r);L["dirty"]=True;break
					for k in("custom","text"):
						v=str(e[k].Text or "").strip()
						if v!=r[k]:r[k]=v;a=True;d.append(r)
					if not s:
						g=a5(str(e["delay"].Text or "").strip(),r["delay"]);g=max(g,aP(r))
						if abs(g-r["delay"])>.001:r["delay"]=g;a=True
					for k in("deep","auto"):
						v=bool(e[k].IsChecked)
						if v!=r[k]:r[k]=v;a=True;(d if k=="deep"else n).append(r)
			except Exception as w:L["f"]=None;m("settings page error: %s (reopen the page)."%w,u);return
			if a:
				ad()
				for r in d:aE(r)
				for r in n:
					i=aV(r)
					if 0<=i<len(K["rows"]):
						try:K["rows"][i]["auto"].IsChecked=r["auto"]
						except Exception:c["redraw"]=True
				if L.get("dirty"):L["dirty"]=False;D(p)
		def ct():L["f"]=None;L["rows"]=[]
		a8()
		def cu():c.update({"shutting":False,"docked":False,"queue":[],"paused":False,"job":None,"next_scan":0.,"next_check":0.,"status":"Idle","run":set(),"budget":{},"opening":{},"later":{},"pick":None,"redraw":False,"save_done":False,"no_tool":{},"busy_n":{},"next_rows":0.,"rr":0,"guard_paused":None,"writes":[],"idle_at":0.,"done_at":0.,"minimized":al.start_min()});k.update({"g":None,"rule":None,"c":{},"rows":[],"page":0,"dirty":False,"minimized":False,"shutting":False,"docked":False,"queue":[]});a8();aw();al.dock(fit=True,min=bd);an.dock(fit=True,min=bf);n=sum(1 for a in h if a["auto"]and a["bag"]);m("on, %s, %d watching."%(aa(len(h),"rule"),n),o)
		def cv():
			if K["g"]is None:return
			if ao(K):return
			b=time.time()
			while c["queue"]:
				a=c["queue"].pop(0);d=a[0]if isinstance(a,tuple)else a
				if al.action(a)or(d in("remove","bag","run","reset")and a[1]>=len(h)):continue
				e=cl.get(d)
				if e is not None:e(a)
			if c.get("redraw"):aw()
			if k["queue"]:del k["queue"][:];cb()
			if k["dirty"]and k["g"]is not None:bg()
			if not c["minimized"]and b>=c["next_check"]:c["next_check"]=b+aM;b9()
			b6(b)
			if c.get("save_done")and b>=c["done_at"]:c["save_done"]=False;c["done_at"]=b+cm;aQ()
			be()
		def cw():j=c["job"];return.05 if j is not None and j["phase"]=="target"else.1
		def cx():
			c["shutting"]=k["shutting"]=True
			if c["job"]is not None:O(p);c["job"]=None
			ad();aO.close()
			if c["writes"]:
				if Client.on_client_thread():m("the export wasn't written (the module stopped); export again.",b);del c["writes"][:]
				else:bh()
		return{"start":cu,"tick":cv,"stop":cx,"client_tick":True,"config_height":cq.height,"build_config":cr,"poll_config":cs,"config_closed":ct,"thread_tick":bh,"thread_wanted":ce,"interval":cw}
	aA=(("window",ax,.25,"skills"),("alarm",ay,.1,"attention"),("bags",az,.1,"skillbags"),);return PartSet(av,aw,aA).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("skills","Skills","Skills, training and AFK alarms",_module_skills,.1,category="Skills and home",parts=(("window","Skills Window","Skills with locks, groups and gains",True,("skills",)),("alarm","Training Alarm","Alarm when staff or a gump needs you",False,("attention",)),("bags","Skill Bags","A skill on each item in a bag, once",False,("skillbags",)),),aliases=('Skill Bags','Attention','GM check','training','locks','gains','Item ID'))
