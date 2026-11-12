def _module_skills():
	n=Client._type;o=HOST.booting;u=HOST.claim_cursor;z=HOST.cursor_busy;A=HOST.mobiles;b=HOST.refresh_settings;e=HOST.release_cursor;B=HOST.show_settings;l=Journal.reader;D="skills";E="Skills"
	def C(q,title,what):
		while q:
			a,b=q.pop(0)
			try:
				with open(a,"w")as c:c.write(b)
				API.SysMsg("%s: %s written to %s."%(title,what,a),Kit.HUE_GOOD)
			except Exception as d:API.SysMsg("%s: couldn't write %s (%s)."%(title,a,d),Kit.HUE_BAD)
	def F():
		I="skills";S="Skills";aU="Skills_settings";aV="Skills_pos";aW="Skills_marks";aX="Skills_locksets";aY="Skills_session";bN=6;bO=7000;bP=("StandardSkillsGump","SkillGumpAdvanced");bQ=5091;bR=22;aA=110;aZ=56;bS=120;bT=.35;bU=380;aB=60;a_=("bar","gain","cap","real");a0=80;a1=2;a2=2;ah="Real values added up, against the total cap (settings page)";a3=(("all_up","All up","Set every listed skill to go up"),("all_down","All down","Set every listed skill to go down (click twice)"),("all_locked","All locked","Lock every listed skill"),("lock_capped","Lock capped","Lock every skill at its cap"));a4,bV=280,46;bW={"use":(Kit.ART_PLAY,"Use","Use this skill","use"),"button":(Kit.ART_PAGE,"Make button","Make its floating client button (or double-click it in the list)","mkbutton"),"pin":(Kit.ART_OK,"Pin","Keep it at the top of the list (again to unpin)","pin"),"nextgrp":(Kit.ART_PAGE,"Next group","Move it to the next skill group","nextgrp")};ai=200;a5=10;an=(2103,2104,2104);K=(2435,2437,2092);aC,aD=2086,2087;bX=2056;bY=946;a6=946;bZ,b_="#D8B048",.16;b0,b1="#FFFFFF",.07;b2=4.;a7=1.;a8=["Alchemy","Anatomy","Animal Lore","Item Identification","Arms Lore","Parrying","Begging","Blacksmithy","Bowcraft/Fletching","Peacemaking","Camping","Carpentry","Cartography","Cooking","Detecting Hidden","Discordance","Evaluating Intelligence","Healing","Fishing","Forensic Evaluation","Herding","Hiding","Provocation","Inscription","Lockpicking","Magery","Resisting Spells","Tactics","Snooping","Musicianship","Poisoning","Archery","Spirit Speak","Stealing","Tailoring","Animal Taming","Taste Identification","Tinkering","Tracking","Veterinary","Swordsmanship","Mace Fighting","Fencing","Wrestling","Lumberjacking","Mining","Meditation","Stealth","Remove Trap","Necromancy","Focus","Chivalry","Bushido","Ninjitsu","Spellweaving","Mysticism","Imbuing","Throwing"];b3={"Alchemy":[(30,"NPC alchemists teach the first points for gold"),(50,"Heal and Agility potions"),(70,"Cure and Greater Agility potions"),(90,"Greater Strength and Greater Heal potions"),(100,"Greater Cure and Greater Explosion potions")],"Anatomy":[(100,"Use it on any creature or player; bandaging checks it too")],"Animal Lore":[(100,"Use it on tamed or tameable animals")],"Item Identification":[(100,"Use it on any item")],"Arms Lore":[(100,"Use it on weapons and armour")],"Parrying":[(100,"Fight with a shield on (only shields parry pre-AoS)")],"Begging":[(100,"Beg from town NPCs")],"Blacksmithy":[(30,"NPC blacksmiths teach the first points for gold"),(50,"Maces, then cutlasses"),(65,"Scimitars, then broadswords and kryss"),(80,"Katanas, then short spears and spears"),(100,"Plate gorgets and gloves, then plate legs and tunics")],"Bowcraft/Fletching":[(40,"Shafts and arrows"),(65,"Bows"),(85,"Crossbows"),(100,"Heavy crossbows")],"Peacemaking":[(100,"Use it near creatures; tougher ones as it rises")],"Camping":[(100,"Light kindling over and over (a blade on a tree gives some)")],"Carpentry":[(30,"NPC carpenters teach the first points for gold"),(50,"Medium crates"),(65,"Large crates, then wooden shields"),(85,"Fishing poles and quarter staves"),(100,"Gnarled and black staves")],"Cartography":[(30,"NPC mapmakers teach the first points for gold"),(50,"Local maps"),(65,"City maps"),(100,"Sea charts, then world maps")],"Cooking":[(30,"NPC cooks teach the first points for gold"),(100,"Cook over and over (fish steaks and ribs are cheap)")],"Detecting Hidden":[(100,"Use it often, best near someone hidden")],"Discordance":[(100,"Use it on creatures; tougher ones as it rises")],"Evaluating Intelligence":[(100,"Use it on any player or creature")],"Healing":[(30,"NPC healers teach the first points; bandage yourself when hurt"),(60,"Bandage yourself or friends while hurt"),(80,"Keep bandaging; curing poison needs 60 Healing and 60 Anatomy"),(100,"Keep bandaging; resurrecting needs 80 Healing and 80 Anatomy")],"Fishing":[(100,"Fish over and over, in any water")],"Forensic Evaluation":[(100,"Use it on corpses")],"Herding":[(100,"Herd animals with a shepherd's crook")],"Hiding":[(100,"Use it over and over")],"Provocation":[(100,"Make creatures fight each other; tougher ones as it rises")],"Inscription":[(30,"NPC scribes teach the first points for gold"),(100,"Scribe scrolls of a circle you sometimes fail (spell in your book)")],"Lockpicking":[(30,"NPC thieves and tinkers teach the first points"),(100,"Pick locked boxes just above your level")],"Magery":[(30,"NPC mages teach the first points; then 2nd circle spells"),(45,"3rd circle: Bless, Teleport"),(55,"4th circle: Greater Heal, Mana Drain"),(65,"5th circle: Paralyze, Mind Blast"),(75,"6th circle: Invisibility, Mark"),(90,"7th circle: Flamestrike, Mana Vampire"),(100,"8th circle: Earthquake, summons")],"Resisting Spells":[(100,"Rises when spells hit you: a friend's low curses work")],"Tactics":[(100,"Rises as you fight with any weapon")],"Snooping":[(100,"Look into others' packs (a friend's pack animal is safe)")],"Musicianship":[(100,"Play an instrument; the other bard skills train it too")],"Poisoning":[(30,"Lesser poison on a weapon or food"),(60,"Regular poison"),(100,"Greater, then deadly poison")],"Archery":[(30,"An archery butte or an NPC trainer for the first points"),(100,"Shoot creatures a little tougher than you as it rises")],"Spirit Speak":[(100,"Use it over and over")],"Stealing":[(100,"Steal light items from a friend's pack; heavier is harder")],"Tailoring":[(30,"NPC tailors teach the first points for gold"),(45,"Short pants and fancy shirts"),(55,"Cloaks"),(70,"Robes, then leather gorgets and sleeves"),(85,"Leather leggings and tunics"),(100,"Studded gloves, then studded sleeves and leggings")],"Animal Taming":[(30,"NPC animal trainers teach the first points for gold"),(50,"Horses, ostards, llamas, black and polar bears"),(70,"Panthers, grey wolves, grizzly bears, great harts"),(85,"White wolves, bulls, frenzied ostards"),(100,"Drakes and hell hounds, then dragons")],"Taste Identification":[(100,"Use it on food and potions")],"Tinkering":[(30,"NPC tinkers teach the first points for gold"),(60,"Tools and clock parts"),(80,"Lockpicks"),(100,"Spyglasses or jewellery")],"Tracking":[(100,"Use it over and over")],"Veterinary":[(30,"NPC veterinarians teach the first points"),(60,"Bandage hurt animals and pets"),(80,"Keep bandaging; curing needs 60 Veterinary, 60 Animal Lore"),(100,"Keep bandaging; resurrecting needs 80 and 80")],"Swordsmanship":[(30,"NPC trainers or a training dummy for the first points"),(100,"Fight creatures a little tougher than you as it rises")],"Mace Fighting":[(30,"NPC trainers or a training dummy for the first points"),(100,"Fight creatures a little tougher than you as it rises")],"Fencing":[(30,"NPC trainers or a training dummy for the first points"),(100,"Fight creatures a little tougher than you as it rises")],"Wrestling":[(30,"NPC trainers or a training dummy, empty-handed"),(100,"Fight empty-handed; tougher creatures as it rises")],"Lumberjacking":[(100,"Chop trees with an axe over and over")],"Mining":[(30,"NPC miners teach the first points for gold"),(65,"Mine iron ore in mountains and caves"),(100,"Keep mining: the coloured ores come from 65 up")],"Meditation":[(100,"Spend mana, then meditate; metal armour blocks it")],"Stealth":[(100,"Needs 80 Hiding: hide, then move with Stealth (light armour)")],"Remove Trap":[(100,"Use it on trapped boxes (tinkers can trap some to practise on)")],};a9="Skills_stat_targets";aE=250;aj=("up","down","locked");ba=("Going up","Going down","Locked");b4=("Set it to go up","Set it to go down","Lock it");R=[("all","All skills"),("trained","Trained (above 0)"),("gaining","Gaining now"),("session","Gained this session"),("up","Set to go up"),("down","Set to go down"),("locked","Locked"),("below","Below cap"),("pinned","Pinned")];b5=("name","real","value","cap","gain","lock");j={"replace":True,"x_hides":True,"bars":True,"col_cap":True,"col_gain":True,"journal":False,"lock_at_cap":False,"lock_at_target":True,"cap_warn":True,"rows":12,"total_cap":bO,"hl_secs":30,"rate_min":30,"sec_summary":True,"sec_stats":True,"sec_locks":True,"sec_detail":True,"sec_log":False,"log_lines":5,"sort":"name","asc":True,"filter":0,"groups":False,"minimized":False,"width":0,"tips":True,"lock_stat_target":True};b6=dict(j);W={"rows":(4,40),"total_cap":(100,72000),"hl_secs":(0,600),"rate_min":(5,240),"log_lines":(2,15),"filter":(0,len(R)-1),"width":(0,4000)};b7=("bars","col_cap","col_gain","rows","sec_summary","sec_stats","sec_locks","sec_detail","sec_log","log_lines","tips","x_hides","replace");b8=1.;af=("Strength","Dexterity","Intelligence")
		def b9():
			b={}
			for e,f in b3.items():
				c,d=[],0
				for a,g in f:c.append((a*10,"%g-%g"%(d/10.,a),g));d=a*10
				b[e.lower()]=c
			return b
		ca=b9();H={"pins":set(),"targets":{}};O=[];P=[0,0,0];e={"minimized":False,"shutting":False,"docked":False,"queue":[],"sel":None,"last_click":(None,0.),"arm":{},"search":"","pc":{},"save_at":0.,"to_write":[],"ver":0,"preview":False};p={"g":None,"c":{},"store":({},{}),"rows":[],"rowmap":{}};ad={"sync":False,"skip":False};cb,E,z=Kit.basics(e,S);ak={};T={"world":None,"player":None,"how":""};l={"objs":[],"names":[],"click":[],"collide":[],"n":0,"cur":[],"low":[],"full":True,"rr":0};t={"cur":[0,0,0],"locks":[0,0,0],"cap":0,"prev":[0,0,0]};q={"list":[],"ok":False,"ver":0,"sig":None,"of":{}};U={"gumps":None,"sig":None,"full_at":0.}
		def aa():e["ver"]+=1;e["dirty"]=True
		cc=.5;cd=1.;ce=5.;cf=2;cg=8;ch=2.
		def ci():
			e["dirty"]=True
			if(j["sort"]!="name"or R[j["filter"]][0]not in("all","pinned")):e["ver"]+=1
		F={"width":None,"rows":None,"slot":None,"k":1.,"full":None}
		def bb():return F["width"]if F["width"]is not None else j["width"]
		def cj(w,h,mode):
			a=(int(w),int(h))if(w and h)else None
			if a==F["slot"]and not(mode=="again"and a is not None):return
			F["slot"]=a;F["width"]=a[0]if a is not None else None;F["rows"]=None;e["m"]=None;e["rebuild"]="window";aa()
		def ck():return F["k"],F["full"]
		A={"start":0.,"base":{},"stats":None,"seen":0.}
		def bc():
			Kit.kv_load(aU,";",j,W,("sort",))
			if j["sort"]not in b5:j["sort"]="name"
		def X():Kit.kv_save(aU,";",j,b6,W,("sort",))
		def cl():
			H["pins"],H["targets"]=set(),{}
			for b in Kit.get_var(aW).split(";"):
				p=b.split(":")
				if len(p)!=3:continue
				try:i,c,a=int(p[0]),p[1]=="1",int(p[2])
				except ValueError:continue
				if c:H["pins"].add(i)
				if a>0:H["targets"][i]=a
		def bd():a=sorted(H["pins"]|set(H["targets"]));Kit.put_var(aW,";".join("%d:%s:%d"%(c,"1"if c in H["pins"]else "0",H["targets"].get(c,0))for c in a))
		def cm():
			del O[:]
			for a in Kit.get_var(aX).split("|"):
				if "="in a:
					b,c=a.split("=",1)
					if b and c:O.append((b,c))
		def be():Kit.put_var(aX,"|".join("%s=%s"%(a,d)for a,d in O))
		def bf():
			p=Kit.get_var(a9).split(",")
			for k in range(3):
				try:P[k]=max(0,min(aE,int(p[k])))
				except(IndexError,ValueError):P[k]=0
		def cn():
			p=Kit.get_var(aY).split("|");a=time.time();A.update({"start":a,"base":{},"stats":None,"seen":a})
			if len(p)<4:return
			try:b,f=float(p[0]),float(p[3])
			except ValueError:return
			if a-f>bN*3600 or b>a:return
			c={}
			for d in p[1].split(","):
				if ":"in d:
					try:k,v=d.split(":");c[int(k)]=int(v)
					except ValueError:pass
			e=None
			try:s=[int(g)for g in p[2].split(",")];e=s if len(s)==3 else None
			except ValueError:pass
			A.update({"start":b,"base":c,"stats":e,"seen":a})
		def ao():A["seen"]=time.time();b=",".join("%d:%d"%(a,c)for a,c in sorted(A["base"].items()));s=",".join(str(d)for d in A["stats"])if A["stats"]else "";Kit.put_var(aY,"%d|%s|%s|%d"%(A["start"],b,s,A["seen"]))
		def co():
			A.update({"start":time.time(),"base":{},"stats":None})
			for i in range(l["n"]):A["base"][i]=l["cur"][i][0]
			if any(t["cur"]):A["stats"]=list(t["cur"])
			e["gains"],e["log"]={},[];ao()
		def aF():Kit.save_pos(aV,p["g"])
		def ap():return Typing._get(None,"Instance",n("ClassicUO.Game.World"))
		def bg(objs,how):
			b=[str(safe(lambda s=f:s.Name,"")or "?")for f in objs];c=[bool(safe(lambda s=g:s.IsClickable,False))for g in objs];a=[h.lower()for h in b];d=[any(a[k]in a[i]for i in range(k))for k in range(len(a))];l.update({"objs":objs,"names":b,"click":c,"collide":d,"n":len(objs),"low":a,"full":True})
			if len(l["cur"])!=len(objs):l["cur"]=[[0,0,0,0]for m in objs]
			T["how"]=how;e["m"]=None
		def bh(force=False):
			d=time.time()
			if not force and d<e["ref_at"]:return l["n"]>0
			e["ref_at"]=d+3.;b=ap();c=Typing._get(b,"Player")if b is not None else None
			if c is not None:
				f=Typing._get(c,"Skills");a=list(f)if f is not None else None
				if a:
					g=T["player"]is not None and T["player"]is c and len(a)==l["n"];i=T["player"]is not None and not g;T.update({"world":b,"player":c})
					if not g:
						if i:l["cur"]=[];e["ready"]=False;e["rebuild"]="window"
						bg(a,"client")
					return True
			T.update({"world":b,"player":None})
			if l["n"]==0 or T["how"]!="api":
				a=[]
				for h in a8:
					s=API.GetSkill(h)
					if s is not None and str(s.Name)==h:a.append(s)
				if a:bg(a,"api")
			return l["n"]>0
		bi=15
		def bj(full=False):
			b={};d=l["cur"];f=l["objs"];n=len(f)
			if n==0 or len(d)!=n:return b
			if l["full"]:l["full"]=False;full=True
			g=l["rr"]%n;l["rr"]=g+bi;a=int
			for i in range(n):
				s=f[i]
				try:e,v=a(s.BaseFixed),a(s.ValueFixed)
				except Exception:continue
				c=d[i]
				if full or e!=c[0]or v!=c[1]or(i-g)%n<bi:
					try:h=a(s.CapFixed);j=a(s.Lock)
					except Exception:continue
					if e!=c[0]or v!=c[1]or h!=c[2]or j!=c[3]:b[i]=c;d[i]=[e,v,h,j]
			return b
		def bk():
			b,a,c=t["cur"],t["locks"],t["cap"];p=T["player"]
			if p is None:p=API.Player
			if p is not None:
				try:b=[int(p.Strength),int(p.Dexterity),int(p.Intelligence)];a=[int(p.StrLock),int(p.DexLock),int(p.IntLock)];c=int(p.StatsCap)
				except Exception:pass
			if e["stat_pending"]:
				d=time.time();a=list(a)
				for k,(f,g)in list(e["stat_pending"].items()):
					if d<g:a[k]=f
					else:e["stat_pending"].pop(k,None)
			if b==t["cur"]and a==t["locks"]and c==t["cap"]:return False
			t["prev"]=t["cur"];t["cur"],t["locks"],t["cap"]=b,a,c;return True
		def bl():return any(a[2]>0 for a in l["cur"])
		def al():w=T["world"]or ap();return Typing._get(w,"SkillsGroupManager")if w is not None else None
		def cp():
			if ac.f is not None:return True
			if p["g"]is None or not p["c"]or e["minimized"]or e["docked"]:return False
			return j["groups"]or(e["sel"]is not None and j["sec_detail"])
		def Y(force=False):
			c=time.time()
			if not force and(c<e["grp_at"]or not cp()):return
			e["grp_at"]=c+(1. if ac.f is not None or j["groups"]else cq);d=al();b=Typing._get(d,"Groups")if d is not None else None;a=[]
			if b is not None:
				for g in list(b):
					try:n=int(g.Count);k=[int(g.GetSkill(r))for r in range(n)];a.append({"obj":g,"name":str(g.Name or ""),"members":[s for s in k if s<l["n"]],"max":bool(g.IsMaximized)})
					except Exception:continue
			f=(b is not None,tuple((v["name"],tuple(v["members"]),v["max"])for v in a))
			if f!=q["sig"]:q["sig"]=f;q["ver"]+=1
			h={}
			for i in range(len(a)-1,-1,-1):
				for m in a[i]["members"]:h[m]=i
			q["list"],q["ok"],q["of"]=a,b is not None,h
		cq=3.
		def aG(i):return q["of"].get(i)
		def ae():
			a=al()
			if a is not None:safe(lambda:a.Save())
			Y(True)
		def aH(name,a):return Tz.call(None,name,a,Tz.T("ClassicUO.Game.GameActions"))
		def am(i,v):
			if i is None or i>=l["n"]or l["cur"][i][3]==v:return
			if not l["collide"][i]:API.SetSkillLock(l["names"][i],aj[v])
			else:
				with Kit.quiet:import System;aH("ChangeSkillLockStatus",[System.UInt16(i),System.Byte(v)]);a=Tz.T("ClassicUO.Game.Data.Lock");Tz.put(l["objs"][i],"Lock",System.Enum.ToObject(a,v))
			l["cur"][i][3]=v
		def cr(i):
			if i is None or i>=l["n"]:return
			if not l["click"][i]:z("%s can't be used directly."%l["names"][i],Kit.HUE_INFO);return
			if not l["collide"][i]:API.UseSkill(l["names"][i]);return
			try:aH("UseSkill",[i])
			except Exception as a:z("couldn't use %s (%s)."%(l["names"][i],Tz.why(a)),Kit.HUE_BAD)
		def bm(i):
			if i is None or i>=l["n"]or not l["click"][i]:z("only a usable skill gets a button.",Kit.HUE_INFO);return
			try:
				import System
				for b in Tz.windows(["SkillButtonGump"]):
					if int(Tz.get(b,"SkillID"))==i:b.Dispose()
				t=Tz.T("ClassicUO.Game.UI.Gumps.SkillButtonGump");a=T["world"]or ap();g=p["g"];x,y=(g.GetX()+g.GetWidth()+10,g.GetY())if Kit.is_open(g)else(200,200);c=System.Activator.CreateInstance(t,System.Array[object]([a,l["objs"][i],x,y]));Tz.call(None,"Add",[c,True],Tz.T("ClassicUO.Game.Managers.UIManager"));z("%s button placed beside the window."%l["names"][i],Kit.HUE_GOOD)
			except Exception as d:z("couldn't make the button (%s)."%Tz.why(d),Kit.HUE_BAD)
		def bn():
			a=T["world"]or ap();e["swallow_until"]=time.time()+6.;e["asked"]=time.time()
			try:aH("OpenSkills",[a]);return True
			except Exception:return False
		def aI(k,v):API.SetStatLock(("str","dex","int")[k],aj[v]);t["locks"][k]=v;e["stat_pending"][k]=(v,time.time()+2.5)
		def u(a):return "%.1f"%(a/10.)
		def V(i):b=A["base"].get(i);return 0 if b is None else l["cur"][i][0]-b
		def aJ():return sum(V(a)for a in range(l["n"]))
		bo=600.
		def aK():return max(bo,time.time()-A["start"])/3600.
		def bp(i,now):a=j["rate_min"]*60;return sum(f for c,f in e["gains"].get(i,[])if now-c<=a)
		def bq(i,now):a=V(i)/aK();b=max(bo,min(j["rate_min"]*60.,now-max(A["start"],e["started"])));c=bp(i,now)/(b/3600.);return a,c
		def aL(secs):
			secs=int(max(0,secs))
			if secs>=3600:return "%dh %02dm"%(secs//3600,(secs%3600)//60)
			if secs>=60:return "%dm"%(secs//60)
			return "%ds"%secs
		def cs(i,now,a=None):
			b,e,c,e=l["cur"][i]
			if b>=c:return "at cap"
			f,d=a if a is not None else bq(i,now);r=d if d>0 else f
			if r<=0:return "--"
			return "~"+aL((c-b)/r*3600)
		def ct(changed,now):
			h=False
			for i,f in changed.items():
				a=l["cur"][i];d=a[0]-f[0]
				if d==0:continue
				h=True;b=l["names"][i]
				if i not in A["base"]:A["base"][i]=f[0]
				if d>0:
					e["gains"].setdefault(i,[]).append((now,d))
					if len(e["gains"][i])>ai:e["gains"][i]=e["gains"][i][-ai:]
					if j["hl_secs"]>0:e["hl"][i]=now+j["hl_secs"]
				e["log"].append((now,b,d,a[0]))
				if len(e["log"])>ai:e["log"]=e["log"][-ai:]
				if j["journal"]:z("%s %s%s (%s, session %+.1f)."%(b,"+"if d>0 else "-",u(abs(d)),u(a[0]),V(i)/10.),Kit.HUE_GOOD if d>0 else Kit.HUE_BAD)
				for g,k,c in((a[2],"lock_at_cap","its cap (%s)"),(H["targets"].get(i),"lock_at_target","its target %s")):
					if d>0 and g is not None and f[0]<g<=a[0]:
						c=c%u(g)
						if j[k]and a[3]==0:am(i,2);z("%s reached %s and was locked."%(b,c),Kit.HUE_GOOD)
						else:z("%s reached %s."%(b,c),Kit.HUE_GOOD)
			if h and time.time()>=e["save_at"]:e["save_at"]=time.time()+15.;ao()
		def aM():return sum(a[0]for a in l["cur"])
		def cu():
			if aM()<j["total_cap"]:return False
			a=any(d[3]==0 and d[0]<d[2]for d in l["cur"]);b=any(f[3]==1 and f[0]>0 for f in l["cur"]);return a and not b
		def cv():
			if not j["cap_warn"]:e["warned_cap"]=False;return
			a=cu()
			if a and not e["warned_cap"]:z("at the total skill cap (%s) and no skill set to go down: nothing can rise."%u(j["total_cap"]),Kit.HUE_BAD)
			e["warned_cap"]=a
		def aq(k):a=A["stats"];return t["cur"][k]-a[k]if a else 0
		def cw():
			b,c=t["prev"],t["cur"]
			for k in range(3):
				a=P[k]
				if not a or not b[k]or c[k]!=a:continue
				d={1:0,-1:1}.get(c[k]-b[k])
				if d is None:continue
				if j["lock_stat_target"]and t["locks"][k]==d:aI(k,2);z("%s reached its target %d and was locked."%(af[k],a),Kit.HUE_GOOD)
				else:z("%s reached its target %d."%(af[k],a),Kit.HUE_GOOD)
		def cx(k):
			a,v=P[k],t["cur"][k]
			if a and v==a and j["lock_stat_target"]and t["locks"][k]!=2:aI(k,2);z("%s is at its target %d and was locked."%(af[k],a),Kit.HUE_GOOD)
		def cy(k,c):
			v=t["cur"][k];b=["%s %d"%(af[k],v)]
			if A["stats"]:d=aq(k);b[0]+=": %+d this session (%.1f / hour)"%(d,d/c)
			a=P[k]
			if not a:b.append("No target (click: set one in settings)")
			elif v==a:b.append("Target %d: reached"%a)
			else:b.append("Target %d: %d to go %s%s"%(a,abs(a-v),"up"if a>v else "down",", then it locks"if j["lock_stat_target"]else ""))
			return "\n".join(b)
		def br(i):
			if i is None or i>=l["n"]:return
			a=ca.get(l["names"][i].lower())
			if a:
				b=l["cur"][i][0]
				for c,d,e in a:
					if b<c:return d,e
			return
		def cz(i,now):
			f=R[j["filter"]][0];a,d,b,c=l["cur"][i];q=e["search"]
			if q and q not in l["low"][i]:return False
			if f=="trained":return a>0
			if f=="gaining":return bp(i,now)>0
			if f=="session":return V(i)>0
			if f in aj:return c==aj.index(f)
			if f=="below":return a<b
			if f=="pinned":return i in H["pins"]
			return True
		def ag(idx):
			s=j["sort"];b=l["low"].__getitem__
			if s=="name":a=sorted(idx,key=b)
			else:c={"real":0,"value":1,"cap":2,"lock":3}.get(s);d=V if c is None else(lambda i:l["cur"][i][c]);a=sorted(sorted(idx,key=b),key=d)
			if not j["asc"]:a.reverse()
			return a
		def cA(now):
			b=[r for r in range(l["n"])if cz(r,now)];k=set(b);d=[s for s in b if s in H["pins"]];m=bool(e["search"])or j["filter"]!=0;a=[]
			if not j["groups"]or not q["ok"]:
				if R[j["filter"]][0]=="pinned":return[("s",v)for v in ag(b)]
				n=[w for w in b if w not in H["pins"]];return[("s",x)for x in ag(d)+ag(n)]
			if d and R[j["filter"]][0]!="pinned":
				c=e["pc"].get("pin",False);a.append(("g","pin",c))
				if not c:a+=[("s",y)for y in ag(d)]
			f=set()
			for o,g in enumerate(q["list"]):
				h=[G for G in g["members"]if G in k];f.update(g["members"])
				if not h and m:continue
				a.append(("g",o,not g["max"]))
				if g["max"]:a+=[("s",L)for L in ag(h)]
			i=[Z for Z in b if Z not in f]
			if i:
				c=e["pc"].get("other",False);a.append(("g","other",c))
				if not c:a+=[("s",ds)for ds in ag(i)]
			return a
		def cB(i):
			def a(*c):
				a=time.time();b,t=e["last_click"]
				if b==i and a-t<=.6:e["last_click"]=(None,0.);E.add(("button",i),dup=True)
				else:e["last_click"]=(i,a);E.add(("pick",i),dup=True)
			return a
		cC=Kit.disposer("skills.window",e,p)
		def cD():e["rebuild"]="window"
		def J(ctrl,b,value):
			if ctrl is None:return
			k=(ctrl,b)
			if ak.get(k)==value:return
			ak[k]=value
			try:
				a=F["k"]
				if b=="Width":Kit.ui_w(ctrl,value if a==1. else int(round(value*a)))
				elif b=="Pos":
					if a==1.:Kit.ui_pos(ctrl,value[0],value[1])
					else:ctrl.SetPos(int(round(value[0]*a)),int(round(value[1]*a)))
				else:setattr(ctrl,b,value)
			except Exception:pass
		def bs(ctrl,a,value):ak[(ctrl,a)]=value
		def D(a):return 35+Kit.text_w(a)
		def ab(IW=None,zone=False):
			m=e["m"]
			if m is not None and(IW is None or(m["IW"]==IW and m.get("zone",False)==zone)):return m
			m=ar()
			if zone and IW:
				c=[]
				for a in a_:
					if m["sa_w"]+16<=IW:break
					c.append(a);m=ar(c)
				f=(m["sa_w"]+16)-IW
				if f>0:
					g=min(f,m["name_w"]-aB)
					if g>0:bt(m,-g);m["cut"]=True
				m["drop"]=tuple(c)
			m["zone"]=zone;d=max(0,IW-(m["sa_w"]+16))if IW else 0
			if d:
				b=min(bS,d*2//5)if m["bar_x"]is not None else 0
				if b:
					m["bar_w"]+=b
					for a in("gain_x","lock_x"):
						if m[a]is not None and m[a]>m["bar_x"]:m[a]+=b
				bt(m,d-b)
			m["IW"]=IW;e["m"]=m;return m
		def bt(m,d):
			m["name_w"]+=d
			for a in("real_x","val_x","cap_x","bar_x","gain_x","lock_x"):
				if m[a]is not None:m[a]+=d
			m["row_w"]=m["lock_x"]+m["lock_w"]+6;m["sa_w"]=m["row_w"]+16
		def ar(drop=()):
			m={"cut":False,"drop":()};d=l["names"]or a8;a=Kit.pic_size(K[0])[0]or 10;m["arrow_w"]=a;m["lock_w"]=max(a,Kit.pic_size(K[2])[0]or 12);e=Kit.pic_size(an[0])[0]or 11;m["name_x"]=4+e+6;m["name_w"]=(max([Kit.text_w(i)for i in d]+[Kit.text_w("Skill")+a+4])+10);b=max(Kit.text_w("120.0"),Kit.text_w("Value")+a+3)+10;f=max(Kit.text_w("+120.0"),Kit.text_w("Gain")+a+3)+8
			if "real"in drop:m["real_x"]=None;m["val_x"]=x=m["name_x"]+m["name_w"]
			else:m["real_x"]=m["name_x"]+m["name_w"];m["val_x"]=x=m["real_x"]+b
			x+=b;m["bar_h"]=max(4,min(11,Kit.pic_size(Kit.LINE_BLUE)[1]or 9));m["bar_w"]=aZ
			for g,c,h in(("cap_x",j["col_cap"]and "cap"not in drop,b),("bar_x",j["bars"]and "bar"not in drop,aZ+10),("gain_x",j["col_gain"]and "gain"not in drop,f)):
				m[g]=x if c else None
				if c:x+=h
			m["lock_x"]=x;m["row_w"]=x+m["lock_w"]+6;m["sa_w"]=m["row_w"]+16;return m
		def M():return Kit.pitch(bR)
		def bu():return 6 if j["tips"]else 5
		def cE():
			a,e=Kit.MARGIN,Kit.GAP;m=ar();l,f=Kit.screen();p=12+Kit.text_w("Find:")+6+aA+14+D(max((v[1]for v in R),key=Kit.text_w))+12+24+Kit.text_w("Groups")+12;q=12+sum(D(w)for w in at)+3*10+12;r=12+D("Use")+12+D("Make button")+12+D("Next group")+12;s=Kit.pic_size(K[2])[0]or 12;t=12+3*(Kit.text_w("Int 125 (+25)")+8+s+14)+Kit.text_w("Stats 225 / 225")+12 if j["sec_stats"]else 0;b=max(m["sa_w"]+16,p,q,r,t,bU);g=b+2*a
			if bb()>g:b=bb()-2*a
			if l:b=max(g-2*a,min(b,l-2*a-10))
			m=ab(b);L={"IW":b,"W":b+2*a,"min_w":g};y=a+30+e;n=(2 if j["sec_summary"]else 0)+(1 if j["sec_stats"]else 0);c=j["rows"]if F["rows"]is None else F["rows"]
			for d,u,o in(("sum",n,6+24*n+4),("tool",True,36),("list",True,26+c*M()+6),("locks",j["sec_locks"],36),("detail",j["sec_detail"],6+24*bu()+4),("log",j["sec_log"],26+20*j["log_lines"]+4)):
				if u:L[d]=(y,o);y+=o+e
			L["H"]=y-e+a;L["fixed_h"]=L["H"]-c*M();h=W["rows"][0];L["min_h"]=L["fixed_h"]+h*M()
			if f and L["H"]>f-10 and c>h:
				i=max(h,(f-10-L["fixed_h"])//M())
				if i<c:
					k=(c-i)*M();L["list"]=(L["list"][0],L["list"][1]-k)
					for d in("locks","detail","log"):
						if d in L:L[d]=(L[d][0]-k,L[d][1])
					L["H"]-=k;L["rows"]=i;return L
			L["rows"]=c;return L
		at=tuple(dt[1]for dt in a3)
		def aN(widths,gap,IW):
			b,x,a=[],12,0
			for c in widths:
				if x>12 and x+c>IW-12:x,a=12,a+1
				b.append((x,a));x+=c+gap
			return b,a+1
		def bv():
			b=ar(a_);a=[b["sa_w"]-max(0,b["name_w"]-aB)+16,12+Kit.text_w("Find:")+6+a0+2+12,12+D(max((d[1]for d in R),key=Kit.text_w))+12,12+24+Kit.text_w("Groups")+12]
			if j["sec_summary"]:a+=[12+Kit.text_w("Session +99.9")+12,12+D("Reset")+12]
			if j["sec_stats"]:a.append(12+Kit.text_w("Int 125 (+25)")+8+(Kit.pic_size(K[2])[0]or 12)+4)
			if j["sec_locks"]:a.append(12+max(D(f)for f in at)+12)
			if j["sec_detail"]:c=max(Kit.pic_size(g)[0]for g in K)or 12;a+=[12+aB+8+3*(c+10)+12,12+Kit.text_w("Target:")+8+56+12+Kit.text_w("none set")+4,12+max(D("Make button"),D("Next group"))+12]
			return max(a)+2*Kit.MARGIN
		def bw(w,h):
			k,i=Kit.MARGIN,Kit.GAP;a=w-2*k;Z={"IW":a,"W":w,"H":h};c=[];m=0
			if j["sec_summary"]:o=u(j["total_cap"]);G="Total %s / %s   (%s free)   with bonuses %s"%(o,o,o,o);Z["total2"]=Kit.text_w(G)>a-24;H=a-12-D("Reset");Z["sess_own"]=H-12-6<Kit.text_w("Session +99.9");m+=(2 if Z["total2"]else 1)+(2 if Z["sess_own"]else 1)
			if j["sec_stats"]:
				A=Kit.text_w("Int 125 (+25)")+8;B=Kit.pic_size(K[2])[0]or 12;l,b,e=[],12,0
				for N in range(3):
					if b>12 and b+A+B>a-4:b,e=12,e+1
					l.append((b,e));b+=A+B+14
				if b>12 and b+Kit.text_w("Stats 225 / 225")>a-4:b,e=12,e+1
				Z["stats"]=(l,(b,e));m+=e+1
			if m:c.append(("sum",6+24*m+4))
			C=D(max((ds[1]for ds in R),key=Kit.text_w));p=24+Kit.text_w("Groups");f=12+Kit.text_w("Find:")+6;s=a-f-14-C-12-p-12
			if s>=a0:T={"field":s,"filter":(f+s+14,0),"groups":(a-12-p,0)};n=1
			else:
				T={"field":max(20,a-f-2-12),"filter":(12,1)}
				if 12+C+12+p+12<=a:T["groups"],n=(a-12-p,1),2
				else:T["groups"],n=(12,2),3
			T["tx"]=f;Z["T"]=T;c.append(("tool",36+28*(n-1)));c.append(("list",None))
			if j["sec_locks"]:Z["locks_p"],n=aN([D(dt)for dt in at],10,a);c.append(("locks",36+26*(n-1)))
			if j["sec_detail"]:
				f=12+Kit.text_w("Target:")+8;t=f+56+12;v=a-12-D("Unpin");x=v-t-6>=Kit.text_w("none set");E=["use","button"]+([]if x else["pin"])+["nextgrp"];I={"use":"Use","button":"Make button","pin":"Unpin","nextgrp":"Next group"};l,F=aN([D(I[du])for du in E],12,a)
				if F==1:l[-1]=(a-12-D("Next group"),0)
				Z["D"]={"tx":f,"tgt_x":t,"pin_here":x,"pin_x":v,"tgt_w":(v-6 if x else a-4)-t,"btns":list(zip(E,l))};c.append(("detail",6+24*(bu()+F)+4))
			d=j["log_lines"]if j["sec_log"]else 0
			if j["sec_log"]:c.append(("log",None))
			def q(rows,d):
				y=k+30+i
				for b,a in c:
					if b=="list":a=26+rows*M()+6
					elif b=="log":a=26+20*d+4
					y+=a+i
				return y-i+k
			J=W["rows"][0];g=(h-q(0,d))//M()
			while g<J and d>a2:d-=1;g=(h-q(0,d))//M()
			Z["need"]=q(a1,min(d,a2)if j["sec_log"]else 0);Z["short"]=g<a1;g=max(1,g);Z["rows"],Z["log_n"]=g,d;L=max(26+g*M()+6,h-q(0,d)+32);y=k+30+i
			for z,r in c:
				if z=="list":r=L
				elif z=="log":r=26+20*d+4
				Z[z]=(y,r);y+=r+i
			Z["H"]=y-i+k;return Z
		def cF(w,h):
			a=bv();k=1. if w>=a else w/float(a);b,c,Z=w,h,None
			for d in range(4):
				b=w if k==1. else max(a,int(round(w/k)));c=h if k==1. else int(round(h/k));Z=bw(b,c)
				if not Z["short"]:break
				k=min(k,h/float(Z["need"])*.999)
			return b,c,k,Z
		def Q(c,key,txt,room,hue=None,base=None,lbl=None):
			if lbl is None:lbl=c.get(key)
			if lbl is None:return
			b=(txt,room,hue,base);d=key+"_src"
			if c.get(d)==b:return
			c[d]=b;e=Kit.fit(txt,room);Kit.set_text(lbl,e,hue);f=c.get(key+"_cat")
			if f is None:return
			a=base or ""if e==txt else(("%s. %s"%(txt,base))if base else txt)
			if a!=c.get(key+"_tip"):c[key+"_tip"]=a;safe(lambda:f.SetTooltip(a))
		def cG(L):b=L["IW"];Z=dict(L,total2=False,sess_own=False,log_n=j["log_lines"]);c=Kit.text_w("Int 125 (+25)")+8+(Kit.pic_size(K[2])[0]or 12)+14;Z["stats"]=([(12+f*c,0)for f in range(3)],(12+3*c,0));a=12+Kit.text_w("Find:")+6;Z["T"]={"tx":a,"field":aA,"filter":(a+aA+14,0),"groups":(b-12-24-Kit.text_w("Groups"),0)};Z["locks_p"]=aN([D(g)for g in at],10,b)[0];a=12+Kit.text_w("Target:")+8;d=b-12-D("Unpin");Z["D"]={"tx":a,"tgt_x":a+68,"pin_here":True,"pin_x":d,"tgt_w":d-6-(a+68),"btns":[("use",(12,0)),("button",(24+D("Use"),0)),("nextgrp",(b-12-D("Next group"),0))]};return Z
		def bx(g,store,c,Z,k,zone=True):
			M=Kit.MARGIN;f=Z["IW"];a=M;ab(f,zone=zone)
			def l(key,x,y,w,hue=None,h=22,dy=0):
				a=Kit.add_label(g,"",x,y,hue)
				if zone:c[key+"_cat"]=Kit.catcher(g,x-2,y+dy-3,max(8,w+4),h,lambda:None);c[key+"_tip"]=""
				return a
			if "sum"in Z:
				d,i=Z["sum"];Kit.add_section(g,a,d,f,i);b=d+6
				if j["sec_summary"]:
					I=2 if Z["total2"]else 1;c["total"]=Kit.add_label(g,"",a+12,b+3);J=Kit.catcher(g,a+8,b,f-16,24*I-2,lambda:None,ah)
					if zone:c["total_cat"],c["total_tip"]=J,ah
					b+=24
					if Z["total2"]:c["total2"]=Kit.add_label(g,"",a+12,b+3);b+=24
					B=a+f-12-D("Reset");c["session_w"]=f-28 if Z["sess_own"]else B-a-12-6;c["session"]=l("session",a+12,b+3,c["session_w"])
					if Z["sess_own"]:b+=24
					Kit.art_button(g,store,"newsess",Kit.ART_CLOSE,B,b-1,"Reset","New session: gains count from now",on_click=E("newsess"));b+=24
				if j["sec_stats"]:
					C=Kit.text_w("Int 125 (+25)")+8;L,(F,N)=Z["stats"];c["stats"]=[];c["stat_cats"],c["stat_tips"]=[],[None,None,None]
					for n,O in enumerate(("Str","Dex","Int")):
						s,p=L[n];t=b+24*p;P=Kit.add_label(g,"",a+s,t+3);c["stat_cats"].append(Kit.catcher(g,a+s-2,t,C-4,22,E("settings"),af[n]));q=Kit.add_pic(g,K[0],a+s+C,t+5)
						if q is not None:Kit.on_click(q,E(("stat",n),dup=True));Kit.with_tip(q,"Click: %s up, down or locked"%O)
						c["stats"].append((P,q))
					c["stat_total_w"]=f-4-F;c["stat_total"]=l("stat_total",a+F,b+24*N+3,c["stat_total_w"],Kit.HUE_INFO)
			d,i=Z["tool"];T=Z["T"];Kit.add_section(g,a,d,f,i);Kit.add_label(g,"Find:",a+12,d+10);c["search"]=Kit.with_tip(Kit.add_textbox(g,e["search"],a+T["tx"],d+7,T["field"],numbers=False,font=max(8,int(round(16*k)))),"Type part of a skill name");c["search"].SetPlaceholder("search");Q,S=T["filter"];c["filter"]=Kit.art_button(g,store,"filter",Kit.ART_PAGE,a+Q,d+7+28*S,R[j["filter"]][1],"Which skills to list (click: next)",on_click=E("filter"));U,V=T["groups"];c["groups"]=Kit.add_check(g,"Groups",a+U,d+9+28*V,j["groups"],"Show the client's skill groups (click one to fold it)");cK(g,c,a,Z["list"][0],f,Z["list"][1],Z["rows"])
			if "locks"in Z:
				d,i=Z["locks"];Kit.add_section(g,a,d,f,i)
				for(o,u,z),(A,p)in zip(a3,Z["locks_p"]):Kit.art_button(g,store,o,Kit.ART_OK,a+A,d+7+26*p,u,z,on_click=E(o))
			if "detail"in Z:
				d,i=Z["detail"];m=Z["D"];Kit.add_section(g,a,d,f,i);b=d+6;G=max(Kit.pic_size(ds)[0]for ds in K)or 12;H=a+f-12-3*(G+10);c["d_name_w"]=H-a-12-8;c["d_locks"]=[];c["d_name"]=l("d_name",a+12,b+3,c["d_name_w"],Kit.HUE_TITLE)
				for v in range(3):
					r=Kit.add_pic(g,K[v],H+v*(G+10),b+5)
					if r is not None:Kit.on_click(r,E(("dlock",v),dup=True));Kit.with_tip(r,b4[v])
					c["d_locks"].append(r)
				b+=24;c["d_lw"]=f-28;c["d_l1"]=l("d_l1",a+12,b+3,c["d_lw"]);b+=24;c["d_l2"]=l("d_l2",a+12,b+3,c["d_lw"],Kit.HUE_INFO);b+=24
				if j["tips"]:c["d_tip"]=Kit.add_label(g,"",a+12,b+3,Kit.HUE_TEXT);c["d_tip_cat"]=Kit.catcher(g,a+8,b,f-16,22,lambda:None,"Training tip for this skill's range");c["d_tip_full"]=None;b+=24
				Kit.add_label(g,"Target:",a+12,b+3);c["target"]=Kit.with_tip(Kit.add_textbox(g,"",a+m["tx"],b,56,numbers=False,font=max(8,int(round(16*k)))),"Real value to stop at (empty = none)");c["target"].SetPlaceholder("none");c["d_tgt_w"]=m["tgt_w"];c["d_tgt"]=l("d_tgt",a+m["tgt_x"],b+3,m["tgt_w"],Kit.HUE_INFO);b+=24
				for o,(A,p)in([("pin",(m["pin_x"],-1))]if m["pin_here"]else[])+m["btns"]:
					W,u,z,X=bW[o];Y=Kit.art_button(g,store,o,W,a+A,b-1+24*p,u,z,on_click=E(X))
					if o=="pin":c["pin"]=Y
			if "log"in Z:
				d,i=Z["log"];Kit.add_section(g,a,d,f,i,"RECENT GAINS");c["log"]=[];c["log_w"]=f-28
				for n in range(Z["log_n"]):c["log"].append(l("log%d"%n,a+12,d+26+20*n,c["log_w"],Kit.HUE_TEXT,20,1))
		def by():return("the client's or the Action Bar's Skills button"if j["replace"]else "the Action Bar's Skills button")
		def aO():
			if j["x_hides"]:return "Hide %s (%s brings it back)"%(S,by())
			return Kit.CLOSE_TIP%S
		def au():
			c,p["g"]=p["g"],None;ak.clear();e["desc"]=None;e["rebuild"]=None
			if e["hidden"]:p.update({"c":{},"rows":[],"rowmap":{},"store":({},{})});Kit.dispose(c);return
			a=({},{});d={};e["resize_at"],e["preview"]=0.,False;p["L"]=None;L,Z=None,None;F["k"],F["full"]=1.,None
			if e["minimized"]or e["docked"]:w,h=a4,bV
			elif F["slot"]is not None:w,h=F["slot"];f,m,k,Z=cF(w,h)
			else:L=cE();w,h=L["W"],L["H"];p["L"]=L
			x,y=Kit.load_pos(aV,(160,120),(w,h))
			if Kit.is_open(c):x,y=c.GetX(),c.GetY()
			b=LAYOUT.spot(I)if HOST.layout_holds(I)else None
			if b is not None:x,y=int(b[0]),int(b[1])
			if Z is not None:
				g=G.CreateGump(True,True);Kit.add_window_frame(g,f,m);Kit.title_bar(g,a,f,S,I,E("toggle_min"),E("to_bar"),E("settings"),close_tip=aO());bx(g,a,d,Z,k)
				if k!=1.:i=max(bv(),w);F["k"],F["full"]=k,(int(i),int(bw(i,0)["need"]));Kit.scale_window(g,k)
			elif L is None:g=G.CreateGump(True,True);d["mini"]=Kit.mini_bar(g,a,w,h,S,I,E("toggle_min"),close_tip=aO())
			else:
				if b is None:x,y=Kit.clamp(x,y,w,h)
				g=G.CreateModernGump(x,y,w,h,True,L["min_w"],L["min_h"],cI);g.SetAlpha(0);Kit.add_window_frame(g,w,h,mouse=False);Kit.title_bar(g,a,w,S,I,E("toggle_min"),E("to_bar"),E("settings"),close_tip=aO());bx(g,a,d,cG(L),1.,False)
			l=Kit.show_window(g,x,y,w,h,I,e["docked"],cC(g),aF,p,{"g":g,"c":d,"store":a,"rows":[],"rowmap":{},"w":f if Z is not None else w})
			if b is not None and l is not None and tuple(l)!=(x,y):g.SetPos(x,y);Kit.note_rect(g,x,y);Kit.moved_by_code(g)
			if b is not None:LAYOUT.fit_now(I,g)
			if j["minimized"]!=e["minimized"]:j["minimized"]=e["minimized"];X()
			aR();Y();av(time.time());aQ(time.time());Kit.dispose(c)
		dr=None;cH=Kit.dock_hooks(S,bQ,e,p,cD)
		def cI(*a):
			e["resize_at"]=time.time();g=p["g"];L=p.get("L")
			if e["preview"]or L is None or not Kit.is_open(g)or e["minimized"]or e["docked"]:return
			if F["width"]is None and(int(g.GetWidth()),int(g.GetHeight()))!=(L["W"],L["H"]):e["preview"]=True;g.SetAlpha(.55)
		def cJ():
			g=p["g"];L=p.get("L");e["preview"]=False
			if L is None or not Kit.is_open(g)or e["minimized"]or e["docked"]:return
			if F["width"]is not None:g.SetAlpha(0);return
			w,h=int(g.GetWidth()),int(g.GetHeight());c,d=W["rows"];a=max(c,min(d,(h-L["fixed_h"]+M()//2)//M()));b=w if w>L["min_w"]else 0
			if a==L["rows"]and b==j["width"]and(w,h)==(L["W"],L["H"]):g.SetAlpha(0);return
			if a!=j["rows"]or b!=j["width"]:j["rows"],j["width"]=a,b;X();ad["sync"]=True
			e["m"]=None;e["rebuild"]="window";aa()
		def cK(g,c,i,a,IW,h,rows):
			m=ab();Kit.add_section(g,i,a,IW,h);b=i+8;c["hdr"]={};j=[("name","Skill",m["name_x"],"Sort by name"),("real","Real",m["real_x"],"Sort by real value without item bonuses"),("value","Value",m["val_x"],"Sort by value with bonuses"),("cap","Cap",m["cap_x"],"Sort by cap"),("gain","Gain",m["gain_x"],"Sort by gain this session")];k={"name":m["real_x"]or m["val_x"],"real":m["val_x"],"value":m["cap_x"]or m["bar_x"]or m["gain_x"]or m["lock_x"],"cap":m["bar_x"]or m["gain_x"]or m["lock_x"],"gain":m["lock_x"]}
			for f,l,d,n in j:
				if d is None:continue
				c["hdr"][f]=Kit.add_label(g,l,b+d,a+6,Kit.HUE_INFO);Kit.catcher(g,b+d-2,a+3,(k[f]or d+40)-d-2,20,E(("sort",f),dup=True),n+" (again to reverse)")
			e=Kit.add_pic(g,K[2],b+m["lock_x"],a+7)
			if e is not None:Kit.on_click(e,E(("sort","lock"),dup=True));Kit.with_tip(e,"Sort by lock (again to reverse)")
			c["hdr"]["lock_pic"]=e;c["arrow"]=Kit.add_pic(g,K[1],b,a+8,mouse=False);c["sa"]=G.CreateGumpScrollArea(b,a+26,m["sa_w"],rows*M());g.Add(c["sa"]);p=safe(o,False);c["sa_xy"]=(b,a+26);c["more"]=False;c["cap"]=rows+cf if p else W["rows"][1]+999;c["grow_at"]=time.time()+ch
		def bz(r,y):
			if r["y"]==y:return
			r["y"]=y;a=F["k"]
			for b,x,c in r["parts"]:
				try:
					if a==1.:Kit.ui_pos(b,x,y+c)
					else:b.SetPos(int(round(x*a)),int(round((y+c)*a)))
				except Exception:pass
		def bA(r,on):
			if r["hidden"]==(not on):return
			r["hidden"]=not on
			for a,b,b in r["parts"]:
				if a is r.get("bar"):
					if not on:J(a,"IsVisible",False)
				else:J(a,"IsVisible",on)
			if on:r["sig"]=None
		def av(now):
			c=p["c"]
			if "sa_xy"not in c:return
			i=(e["ver"],q["ver"],int(now)if R[j["filter"]][0]=="gaining"else 0)
			if e["desc"]is not None and i==e["desc_key"]:return
			e["desc_key"]=i;a=cA(now)
			if a==e["desc"]:return
			e["desc"]=a;m=ab();b=c["sa"];u=len(p["rowmap"])+(0 if "selbox"in c else 1)+(0 if c.get("empty")else 1)
			if "selbox"not in c:c["selbox"]=Kit.add_box(b,0,0,m["row_w"],M()-1,b_,bZ);J(c["selbox"],"IsVisible",False)
			f=""if a else("No skill matches; change the search or the filter."if l["n"]else "Waiting for the server to send your skills.")
			if c.get("empty")is None and f:c["empty"]=Kit.add_label(b,f,m["name_x"],3,Kit.HUE_INFO)
			if c.get("empty")is not None:Kit.set_text(c["empty"],f);J(c["empty"],"IsVisible",bool(f))
			g=p["rowmap"];n,o,s=[],set(),{};v=M();c["more"]=False
			for t,d in enumerate(a):
				h=t*v;k=(d[0],d[1]);s[k]=w=s.get(k,-1)+1;k=(d[0],d[1],w);r=g.get(k)
				if r is None and t>=c["cap"]and(d[0]=="g"or d[1]!=e["sel"]):c["more"]=True;continue
				if r is None:r=cM(b,h,d,m)if d[0]=="g"else cN(b,h,d[1],m);g[k]=r
				else:bz(r,h);bA(r,True)
				if d[0]=="g":J(r["arrow"],"Graphic",aD if d[2]else aC)
				o.add(k);n.append(r)
			for k,r in g.items():
				if k not in o and not r["hidden"]:bA(r,False);bz(r,0)
			p["rows"]=n
			if F["k"]!=1. and u!=len(g)+(0 if "selbox"in c else 1)+(0 if c.get("empty")else 1):Kit.scale_window(p["g"],F["k"])
			aP()
		def cL(now):
			c=p["c"]
			if not c.get("more")or(now<c["grow_at"]and safe(o,False)):return
			c["cap"]+=cg;e["desc"]=None;av(now);bC(now)
		def N(r,ctl,x,dy):
			if ctl is not None:r["parts"].append((ctl,x,dy))
			return ctl
		def cM(tgt,a,d,m):b,c=d[1],d[2];r={"kind":"g","key":b,"y":a,"hidden":False,"parts":[],"sig":None};N(r,Kit.add_box(tgt,0,a+1,m["row_w"],M()-2,b1,b0),0,1);r["arrow"]=N(r,Kit.add_pic(tgt,aD if c else aC,4,a+5,mouse=False),4,5);bs(r["arrow"],"Graphic",aD if c else aC);r["lbl"]=N(r,Kit.add_label(tgt,"",m["name_x"],a+3,Kit.HUE_TITLE),m["name_x"],3);r["real"]=N(r,Kit.add_label(tgt,"",m["real_x"],a+3,Kit.HUE_INFO),m["real_x"],3)if m["real_x"]is not None else None;r["val"]=N(r,Kit.add_label(tgt,"",m["val_x"],a+3,Kit.HUE_INFO),m["val_x"],3);r["gain"]=N(r,Kit.add_label(tgt,"",m["gain_x"],a+3,Kit.HUE_INFO),m["gain_x"],3)if m["gain_x"]is not None else None;N(r,Kit.catcher(tgt,0,a,m["row_w"],M()-1,E(("fold",b),dup=True),"Fold or unfold this group"),0,0);return r
		def cN(tgt,a,i,m):
			r={"kind":"s","i":i,"y":a,"hidden":False,"parts":[],"sig":None};r["name"]=N(r,Kit.add_label(tgt,bB(i,m),m["name_x"],a+3),m["name_x"],3);r["real"]=N(r,Kit.add_label(tgt,"",m["real_x"],a+3),m["real_x"],3)if m["real_x"]is not None else None;r["val"]=N(r,Kit.add_label(tgt,"",m["val_x"],a+3),m["val_x"],3);r["cap"]=N(r,Kit.add_label(tgt,"",m["cap_x"],a+3,Kit.HUE_INFO),m["cap_x"],3)if m["cap_x"]is not None else None;r["gain"]=N(r,Kit.add_label(tgt,"",m["gain_x"],a+3,Kit.HUE_GOOD),m["gain_x"],3)if m["gain_x"]is not None else None;r["bar"]=None
			if m["bar_x"]is not None:
				c=(M()-m["bar_h"])//2;d=a+c
				if Kit.pic_size(Kit.LINE_RED)[0]>0:N(r,Kit.add_tiled(tgt,Kit.LINE_RED,m["bar_x"],d,m["bar_w"],m["bar_h"],hue=bY),m["bar_x"],c)
				else:N(r,Kit.add_tiled(tgt,Kit.SECTION_TILE,m["bar_x"],d,m["bar_w"],m["bar_h"],1.),m["bar_x"],c)
				r["bar"]=N(r,Kit.add_tiled(tgt,Kit.LINE_BLUE,m["bar_x"],d,1,m["bar_h"]),m["bar_x"],c)
			e="Click: pick it (details below); double-click: its floating button"if l["click"][i]else "Click: pick it (details below)";r["cat"]=N(r,Kit.catcher(tgt,m["name_x"]-2,a,m["lock_x"]-m["name_x"]-2,M()-1,cB(i)),m["name_x"]-2,0);r["tip0"],r["cat_tip"],r["use"]=e,None,None
			if l["click"][i]:b=G.CreateGumpButton("",Kit.HUE_TEXT,an[0],an[1],an[2]);b.SetPos(4,a+6);tgt.Add(b);Kit.on_click(b,E(("use",i),dup=True));Kit.with_tip(b,"Use "+l["names"][i]);r["use"]=N(r,b,4,6)
			r["lock"]=N(r,Kit.add_pic(tgt,K[0],m["lock_x"],a+4),m["lock_x"],4);r["tip"]=None
			if r["lock"]is not None:Kit.on_click(r["lock"],E(("lock",i),dup=True));bs(r["lock"],"Graphic",K[0])
			return r
		def bB(i,m=None):
			a=l["names"][i]if i<l["n"]else "?";m=m or ab()
			if m.get("cut"):return Kit.fit(a,m["name_w"]-10)
			return a
		def aP():
			a=p["c"].get("selbox")
			if a is None:return
			y=None;b=e["sel"]
			if b is not None:
				for r in p["rows"]:
					if r["kind"]=="s"and r["i"]==b:y=r["y"];break
			if y is None:J(a,"IsVisible",False)
			else:J(a,"Pos",(0,y));J(a,"IsVisible",True)
		def cO(i,now):
			if e["hl"].get(i,0)>now:return Kit.HUE_GOOD
			if i in H["pins"]:return Kit.HUE_TITLE
			return Kit.HUE_TEXT
		def bC(now):
			q=l["cur"];s=l["n"];t=j["col_gain"];v=j["tips"];w=ab()["bar_w"]
			for r in p["rows"]:
				if r["kind"]=="g":cQ(r);continue
				i=r["i"]
				if i>=s:continue
				b,c,a,d=q[i];k=cO(i,now);m=(b,c,a,d,V(i)if t else 0,k)
				if m==r["sig"]:continue
				r["sig"]=m;Kit.set_text(r["name"],bB(i),k)
				if r["real"]is not None:Kit.set_text(r["real"],u(b),Kit.HUE_GOOD if a and b>=a else Kit.HUE_TEXT)
				n=c-b;Kit.set_text(r["val"],u(c),Kit.HUE_GOOD if n>0 else(Kit.HUE_BAD if n<0 else Kit.HUE_TEXT))
				if r["cap"]is not None:Kit.set_text(r["cap"],u(a))
				if r["gain"]is not None:e=V(i);Kit.set_text(r["gain"],("%+.1f"%(e/10.))if e else "",Kit.HUE_GOOD if e>0 else Kit.HUE_BAD)
				if r["lock"]is not None:
					J(r["lock"],"Graphic",K[d]);f="%s (click: %s)"%(ba[d],ba[(d+1)%3].lower())
					if r.get("tip")!=f:r["tip"]=f;Kit.with_tip(r["lock"],f)
				g=br(i)if v else None;h=r["tip0"]if g is None else "%s\n%s %s: %s"%(r["tip0"],l["names"][i],g[0],g[1])
				if h!=r["cat_tip"]:r["cat_tip"]=h;Kit.with_tip(r["cat"],h)
				if r["bar"]is not None:o=int(w*min(1.,float(c)/a))if a>0 else 0;J(r["bar"],"Width",max(1,o));J(r["bar"],"IsVisible",o>0);J(r["bar"],"Graphic",bX if a and b>=a else Kit.LINE_BLUE)
		aw={"list":None,"n":-1,"mem":[]}
		def cP(key):
			if key=="pin":return "Pinned",[c for c in range(l["n"])if c in H["pins"]]
			if key=="other":
				if aw["list"]is not q["list"]or aw["n"]!=l["n"]:a=q["of"];aw.update({"list":q["list"],"n":l["n"],"mem":[d for d in range(l["n"])if d not in a]})
				return "Other",aw["mem"]
			if isinstance(key,int)and key<len(q["list"]):g=q["list"][key];return g["name"]or "(no name)",g["members"]
			return "?",[]
		def cQ(r):
			e,b=cP(r["key"]);m=ab();n=l["n"];j=l["cur"];c=d=a=0
			for i in b:
				if i<n:
					f=j[i];c+=f[0];d+=f[1]
					if r["gain"]is not None:a+=V(i)
			g=(m["real_x"]or m["val_x"])-m["name_x"]-6;h=(e,len(b),g,c,d,a)
			if r.get("gsig")==h:return
			r["gsig"]=h;Kit.set_text(r["lbl"],Kit.fit("%s (%d)"%(e,len(b)),g))
			if r["real"]is not None:Kit.set_text(r["real"],u(c))
			Kit.set_text(r["val"],u(d))
			if r["gain"]is not None:Kit.set_text(r["gain"],("%+.1f"%(a/10.))if a else "")
		def cR():
			c=p["c"];f=c.get("hdr")
			if not f:return
			m=ab();s=j["sort"];g=(s,j["asc"],m);b=c.get("hdr_k")
			if b is not None and b[0]==s and b[1]==g[1]and b[2]is m:return
			c["hdr_k"]=g;d={"name":("Skill",m["name_x"]),"real":("Real",m["real_x"]),"value":("Value",m["val_x"]),"cap":("Cap",m["cap_x"]),"gain":("Gain",m["gain_x"])}
			for e,k in f.items():
				if e!="lock_pic":Kit.set_text(k,d[e][0],Kit.HUE_TITLE if e==s else Kit.HUE_INFO)
			a=c.get("arrow")
			if a is None:return
			h=c["sa_xy"][0]
			if s=="lock":i=h+m["lock_x"]-m["arrow_w"]-3
			elif d.get(s,(None,None))[1]is not None:l,n=d[s];i=h+n+Kit.text_w(l)+3
			else:J(a,"IsVisible",False);return
			o=c["sa_xy"][1]-26;J(a,"Pos",(i,o+8));J(a,"Graphic",K[0]if j["asc"]else K[1]);J(a,"IsVisible",True)
		ax={}
		def aQ(now):
			c=p["c"]
			if not c:return
			g=aM()
			if c.get("mini")is not None:
				if e["docked"]:return
				a="%s: %s / %s %+.1f"%(S,u(g),u(j["total_cap"]),aJ()/10.)
				if not e["ready"]:a="%s: waiting for your skills"%S
				Kit.set_text(c["mini"],Kit.fit(a,a4-90),Kit.HUE_BAD if j["cap_warn"]and e["warned_cap"]else Kit.HUE_INFO);return
			cR();bC(now);aP();s=p.get("w",400)-2*Kit.MARGIN-24
			if c.get("total")is not None:
				F=sum(Z[1]for Z in l["cur"]);G=j["total_cap"]-g
				if e["warned_cap"]:h="Total %s / %s: at the cap"%(u(g),u(j["total_cap"]));i,x="set a skill to go down",", ";m=Kit.HUE_BAD
				else:h="Total %s / %s   (%s free)"%(u(g),u(j["total_cap"]),u(max(0,G)));i,x="with bonuses %s"%u(F),"   ";m=Kit.HUE_TEXT
				a=h+x+i
				if c.get("total2")is not None:
					y,z=Kit.fit(h,s),Kit.fit(i,s);Kit.set_text(c["total"],y,m);Kit.set_text(c["total2"],z,m);b=ah if(y,z)==(h,i)else "%s. %s"%(a,ah)
					if b!=c.get("total_tip"):c["total_tip"]=b;Kit.with_tip(c["total_cat"],b)
				else:Q(c,"total",a,s,m,ah)
			if c.get("session")is not None:d=aJ();n=aK();a="Session %+.1f in %s   (%.1f / hour)"%(d/10.,aL(now-A["start"]),d/10./n);Q(c,"session",a,c["session_w"],Kit.HUE_GOOD if d>0 else Kit.HUE_INFO)
			if c.get("stats"):
				H=A["stats"]or t["cur"];n=aK();B,C=c.get("stat_cats")or(),c.get("stat_tips")
				for k,(o,I)in enumerate(c["stats"]):
					D=t["cur"][k];f=D-H[k]if A["stats"]else 0;Kit.set_text(o,"%s %d%s"%(("Str","Dex","Int")[k],D,(" (%+d)"%f)if f else ""),Kit.HUE_GOOD if f>0 else Kit.HUE_TEXT);J(I,"Graphic",K[t["locks"][k]])
					if k<len(B):
						b=cy(k,n)
						if b!=C[k]:C[k]=b;Kit.with_tip(B[k],b)
				v=sum(t["cur"]);q=t["cap"];a=("Stats %d / %d"%(v,q))if q else("Stats %d"%v);d=(aq(0)+aq(1)+aq(2))if A["stats"]else 0
				if d:
					E="%s   %+d (%.1f / hour)"%(a,d,d/n)
					if Kit.text_px(E)<=c["stat_total_w"]:a=E
				Q(c,"stat_total",a,c["stat_total_w"],Kit.HUE_GOOD if q and v>=q else Kit.HUE_INFO)
			cS(now)
			if c.get("log")is not None:
				w=e["log"][-len(c["log"]):][::-1]
				for k,o in enumerate(c["log"]):
					if k<len(w):
						r=w[k];f=r[2];a=ax.get(r)
						if a is None:
							L,M,O,N=r;a="%s  %s %s%s  (%s)"%(time.strftime("%H:%M",time.localtime(L)),M,"+"if f>0 else "-",u(abs(f)),u(N))
							if len(ax)>=2*ai:ax.clear()
							ax[r]=a
						Q(c,"log%d"%k,a,c["log_w"],Kit.HUE_GOOD if f>0 else Kit.HUE_BAD,lbl=o)
					else:Q(c,"log%d"%k,"No gains yet this session."if k==0 and not w else "",c["log_w"],Kit.HUE_INFO,lbl=o)
		def cS(now):
			c=p["c"]
			if c.get("d_name")is None:return
			i=e["sel"]
			if i is None or i>=l["n"]:
				Q(c,"d_name","No skill picked",c["d_name_w"]);Q(c,"d_l1","Click a skill in the list to see it here.",c["d_lw"],Kit.HUE_INFO);Q(c,"d_l2","",c["d_lw"]);Q(c,"d_tgt","",c["d_tgt_w"])
				if c.get("d_tip")is not None:
					Kit.set_text(c["d_tip"],"")
					if c["d_tip_full"]is not None:c["d_tip_full"]=None;Kit.with_tip(c["d_tip_cat"],"Training tip for this skill's range")
				for f in c["d_locks"]:J(f,"Hue",a6)
				return
			a,m,g,v=l["cur"][i];n=aG(i);o=q["list"][n]["name"]if n is not None else "";Q(c,"d_name",l["names"][i]+("   (%s)"%o if o else ""),c["d_name_w"],Kit.HUE_TITLE)
			for w,f in enumerate(c["d_locks"]):J(f,"Hue",0 if w==v else a6)
			r=m-a;x="Real %s   Value %s%s   Cap %s   %s"%(u(a),u(m),(" (%+.1f)"%(r/10.))if r else "",u(g),("To cap %s"%u(g-a))if a<g else "At cap");Q(c,"d_l1",x,c["d_lw"],Kit.HUE_TEXT);s=bq(i,now);y,z=s;A="Session %+.1f   %.1f / hour   last %d min %.1f / hour   cap %s"%(V(i)/10.,y/10.,j["rate_min"],z/10.,cs(i,now,s));Q(c,"d_l2",A,c["d_lw"],Kit.HUE_INFO)
			if c.get("d_tip")is not None:
				t=br(i)
				if t is not None:d,b="Tip %s: %s"%t,Kit.HUE_TEXT
				else:d,b="No tip for this range",Kit.HUE_INFO
				Kit.set_text(c["d_tip"],Kit.fit(d,c["d_lw"]),b)
				if d!=c["d_tip_full"]:c["d_tip_full"]=d;Kit.with_tip(c["d_tip_cat"],d)
			h=H["targets"].get(i)
			if h:
				if a>=h:k,b="reached",Kit.HUE_GOOD
				else:k="%s to go%s"%(u(h-a),", then locks"if j["lock_at_target"]else "");b=Kit.HUE_INFO
			else:k,b="none set",Kit.HUE_INFO
			Q(c,"d_tgt",k,c["d_tgt_w"],b)
			if c.get("pin")is not None:Kit.set_text(c["pin"],"Unpin"if i in H["pins"]else "Pin")
		def aR():
			c=p["c"];a=c.get("target")
			if a is None:e["tgt_shown"]=None;return
			i=e["sel"];b=u(H["targets"][i])if i is not None and i in H["targets"]else "";a.SetText(b);e["tgt_shown"]=(i,b)
		def cT(now):
			d=p["c"];b=False;f=d.get("search")
			if f is not None:
				try:q=str(f.Text or "").strip().lower()
				except Exception:q=e["search"]
				if q!=e["search"]:e["search"],b=q,True
			g=d.get("target")
			if g is not None and e["tgt_shown"]is not None:
				i,h=e["tgt_shown"]
				try:a=str(g.Text or "").strip()
				except Exception:a=h
				if a!=h and i is not None and i==e["sel"]:
					e["tgt_shown"]=(i,a)
					try:v=int(round(float(a.replace(",","."))*10))if a else 0
					except(ValueError,OverflowError):v=None
					if v is not None:
						v=max(0,min(2000,v))
						if v:H["targets"][i]=v
						else:H["targets"].pop(i,None)
						bd();b=True
			k=d.get("groups")
			if k is not None:
				try:c=bool(k.IsChecked)
				except Exception:c=j["groups"]
				if c!=j["groups"]:
					j["groups"]=c;X()
					if c:Y(True)
					b=True
			return b
		def cU():
			try:
				a=U["gumps"]
				if a is None:a=U["gumps"]=Tz.get(None,"Gumps",Tz.T("ClassicUO.Game.Managers.UIManager"))
				return(int(a.Count),a.First)
			except Exception:U["gumps"]=None;return
		cV=3.
		def aS():
			if not j["replace"]and time.time()>e["swallow_until"]:return
			b=time.time();a=cU()
			if a is not None and a==U["sig"]and b<U["full_at"]:return
			U["sig"],U["full_at"]=a,b+cV;U["gumps"]=None;c=safe(lambda:Tz.windows(bP),[])or[]
			if not c:return
			U["sig"]=None
			for d in c:d.Dispose()
			if time.time()<=e["swallow_until"]:e["swallow_until"]=0.;return
			aT()
		def aT():
			if e["hidden"]or e["minimized"]or e["docked"]or not Kit.is_open(p["g"]):e["hidden"]=e["minimized"]=e["docked"]=False;j["minimized"]=False;X();au()
			else:
				a=Kit.client_control(p["g"])
				if a is not None:Tz.call(None,"MakeTopMostGump",[a],Tz.T("ClassicUO.Game.Managers.UIManager"))
		def bD(key,text):
			a=time.time()
			if a-e["arm"].get(key,0.)<=b2:e["arm"].pop(key,None);return True
			e["arm"][key]=a;z(text,Kit.HUE_INFO);return False
		def ay(v,a=False):
			n=0
			for i in(range(l["n"])if a else[g[1]for g in(e["desc"]or[])if g[0]=="s"]):
				c,f,b,d=l["cur"][i]
				if a and not(b and c>=b):continue
				if d!=v:am(i,v);n+=1
			z("%s %s."%(Kit.count(n,"skill"),("set to go up","set to go down","locked")[v]),Kit.HUE_GOOD if n else Kit.HUE_INFO)
		def cW(k):
			if k>=len(O):return
			a,b=O[k];n=0
			for i,c in enumerate(b[:l["n"]]):
				v="udl".find(c)
				if v>=0 and l["cur"][i][3]!=v:am(i,v);n+=1
			z("lock set \"%s\" put on (%d change%s)."%(a,n,""if n==1 else "s"),Kit.HUE_GOOD)
		def cX(name):
			name=re.sub(r"[|=;]","",name or "").strip()[:24]
			if not name:name="Set %d"%(len(O)+1)
			a="".join("udl"[d[3]]for d in l["cur"])
			for k,(n,b)in enumerate(O):
				if n.lower()==name.lower():O[k]=(name,a);break
			else:
				if len(O)>=a5:z("at most %d lock sets: delete one first."%a5,Kit.HUE_BAD);return
				O.append((name,a))
			be();z("lock set \"%s\" saved."%name,Kit.HUE_GOOD)
		def cY(i):
			Y(True)
			if i is None or not q["list"]:z("couldn't move the skill (the client's skill groups can't be read).",Kit.HUE_BAD);return
			a=aG(i);b=0 if a is None else(a+1)%len(q["list"])
			try:
				import System
				if a is not None:q["list"][a]["obj"].Remove(System.Byte(i))
				q["list"][b]["obj"].Add(System.Byte(i));ae();z("%s moved to %s."%(l["names"][i],q["list"][aG(i)or 0]["name"]),Kit.HUE_GOOD)
			except Exception as c:z("couldn't move it (%s)."%Tz.why(c),Kit.HUE_BAD)
		def cZ():
			a=al()
			try:import System;g=System.Activator.CreateInstance(Tz.T("ClassicUO.Game.Managers.SkillsGroup"));g.Name="New group";g.IsMaximized=True;a.Add(g);ae()
			except Exception as b:z("couldn't add a group (%s)."%Tz.why(b),Kit.HUE_BAD)
		def c_(gi):
			Y(True)
			if gi<=0 or gi>=len(q["list"]):return
			a=al();b=q["list"][gi]["name"]
			if safe(lambda:a.Remove(q["list"][gi]["obj"]),False):ae();z("group \"%s\" deleted; its skills went to \"%s\"."%(b,q["list"][0]["name"]if q["list"]else "the first group"),Kit.HUE_GOOD)
		def c0():
			a=al()
			try:a.MakeDefault();ae();z("skill groups reset to the default ones.",Kit.HUE_GOOD)
			except Exception as b:z("couldn't reset the groups (%s)."%Tz.why(b),Kit.HUE_BAD)
		def c1():
			p=API.Player;f=Kit.data_path("Skills_%08X.txt"%int(p.Serial));b=time.time();c=["Skill sheet - %s - %s"%(p.Name or "",time.strftime("%Y-%m-%d %H:%M",time.localtime(b))),"Total %s / %s   (with bonuses %s)"%(u(aM()),u(j["total_cap"]),u(sum(m[1]for m in l["cur"]))),"Str %d  Dex %d  Int %d   (stat cap %d)"%(t["cur"][0],t["cur"][1],t["cur"][2],t["cap"]),"Session %+.1f in %s"%(aJ()/10.,aL(b-A["start"])),"","%-26s %7s %7s %7s %8s  %s"%("Skill","Real","Value","Cap","Session","Lock")]
			for a in sorted(range(l["n"]),key=lambda i:l["names"][i].lower()):g,v,h,k=l["cur"][a];d=V(a);c.append("%-26s %7s %7s %7s %8s  %s"%(l["names"][a],u(g),u(v),u(h),("%+.1f"%(d/10.))if d else "",aj[k]))
			e["to_write"].append((f,"\n".join(c)+"\n"))
		def bE():C(e["to_write"],S,"skill sheet")
		def c2():return bool(e["to_write"])
		def bF(i):
			if e["sel"]!=i:
				e["sel"]=i;aR()
				if j["sec_detail"]:Y(q["sig"]is None)
			aP()
		def az(i):
			if i is None:z("pick a skill first.",Kit.HUE_INFO)
			return i is not None
		def bG(a):
			if not isinstance(a,tuple):return a,None
			return a[0],a[1]if len(a)>1 else None
		def c3(a):e["minimized"]=not(e["minimized"]or e["docked"]);e["docked"]=False;safe(lambda:HOST.dock_forget(I));j["minimized"]=e["minimized"];X();e["rebuild"]="window"
		def c4(b):
			j["filter"]=(j["filter"]+1)%len(R);X();a=p["c"].get("filter")
			if a is not None:Kit.set_text(a,R[j["filter"]][1])
		def c5(a):
			if j["sort"]==a:j["asc"]=not j["asc"]
			else:j["sort"]=a;j["asc"]=a=="name"
			X()
		def c6(a):
			i=a if a is not None else e["sel"]
			if az(i):cr(i)
		def c7(a):
			if not isinstance(a,int):e["pc"][a]=not e["pc"].get(a,False)
			elif a<len(q["list"]):g=q["list"][a];g["obj"].IsMaximized=g["max"]=not g["max"]
		def c8(b):
			a=e["sel"]
			if az(a):H["pins"]^={a};bd()
		def c9(a):
			if bn():z("asked the server for your skills.",Kit.HUE_INFO)
			else:z("couldn't ask the server (the client's skills call failed).",Kit.HUE_BAD)
		def da(a):
			if a<len(O):n=O.pop(a)[0];be();z("lock set \"%s\" deleted."%n,Kit.HUE_INFO)
			b(I)
		def db(a):
			if bD("grp_reset","click Reset groups again for the default groups."):c0();b(I)
		bH={"settings":lambda a:B(I),"to_bar":lambda a:HOST.dock_to_bar(I,S),"pick":bF,"stat":lambda a:aI(a,(t["locks"][a]+1)%3),"all_up":lambda a:ay(0),"all_locked":lambda a:ay(2),"lock_capped":lambda a:ay(2,True),"export":lambda a:c1(),"ls_save":lambda a:(cX(a),b(I)),"ls_apply":cW,"grp_new":lambda a:(cZ(),b(I)),"grp_del":lambda a:(c_(a),b(I)),"grp_save":lambda a:ae(),"toggle_min":c3,"filter":c4,"sort":c5,"button":lambda a:(bF(a),bm(a)),"mkbutton":lambda a:az(e["sel"])and bm(e["sel"]),"use":c6,"lock":lambda a:a is not None and a<l["n"]and am(a,(l["cur"][a][3]+1)%3),"dlock":lambda a:e["sel"]is not None and am(e["sel"],a),"fold":c7,"pin":c8,"nextgrp":lambda a:az(e["sel"])and cY(e["sel"]),"all_down":lambda a:bD("all_down","click All down again to set every listed skill to go down.")and ay(1),"newsess":lambda a:(co(),z("new session; gains count from now.",Kit.HUE_GOOD)),"ask":c9,"ls_del":da,"grp_reset":db};dc=[("replace","Replace the client's skills window","The paperdoll's Skills button, the Skills macro and the Action Bar open this one"),("x_hides","Close only hides it","Off: Close turns Skills off"),("bars","Progress bar per skill (value / cap)","Filled to value / cap; green at the cap"),("col_cap","Cap column","Each skill's cap"),("col_gain","Session gain column","What each skill gained this session"),("journal","Journal line for each gain or loss","The client may print its own line too (its Options)"),("lock_at_cap","Lock a skill when it reaches its cap","A rising skill locks the moment it hits its cap"),("lock_at_target","Lock a skill when it reaches its target","Set targets in the window's details"),("cap_warn","Warn at the total cap when no skill is set to go down","Journal warning and a red total when nothing can rise"),("tips","Training tips in the details and row tooltips","Classic-era advice for the skill's range")];bI=[("rows","Rows in the list:",False,"Skills shown at once (or drag a window corner)"),("total_cap","Total skill cap:",True,"The shard's total skill cap (check it in game)"),("hl_secs","Green name after a gain (s):",False,"Seconds a name stays green after a gain (0 = never)"),("rate_min","Recent pace over (minutes):",False,"Minutes the recent rate and time to cap look back")];dd=[("sec_summary","Totals and session","Total skill points and the session line"),("sec_stats","Str / Dex / Int","Stats, lock arrows and the stat cap"),("sec_locks","Lock buttons","All up, All down, All locked and Lock capped"),("sec_detail","Picked skill details","Rates, target, pin and the Use button"),("sec_log","Recent gains","The last gains, newest first")];de="Export writes a text file to the VirtueAssistantSettings folder.";df="Drag a window corner: height sets the rows, width spreads the columns.";dg=("A stat set to go up locks when it rises to its target, one set to go down when it falls to it. The window's stat tooltips show gains per hour.")
		def dh(w):
			Y(q["sig"]is None);e=len(q["list"])if q["ok"]else 1;g=(w-24)//2
			def b(text,dy):return[("note",f,{"ndy":dy,"h":18})for f in Kit.wrap(text,w-24)]
			def h(k,text,dec,tip):
				def a(f,x,a):
					g=f.g;d=f.c;b=x+12+max(Kit.text_w(s)for r,s,r,r in bI)+10;Kit.add_label(g,text,x+12,a+3);l=u(j[k])if dec else str(j[k]);d.setdefault("num",{})[k]=Kit.with_tip(Kit.add_textbox(g,l,b,a,70,numbers=not dec),tip);e,h=W[k];i=("(%s-%s)"%(u(e),u(h)))if dec else("(%d-%d)"%(e,h));Kit.add_label(g,Kit.fit(i,x+w-4-(b+84)),b+84,a+3,Kit.HUE_INFO)
					if k=="rows":c=b+84+Kit.text_w(i)+16;d["width_v"]=Kit.add_label(g,Kit.fit(bJ(),x+w-4-c),c,a+3,Kit.HUE_INFO);Kit.catcher(g,c-2,a,x+w-4-c,22,lambda:None,"Window width, set by dragging a corner (natural: as wide as the columns need)")
				return("custom",28,a)
			def i(f,x,c):
				a=x+12;d=f.c;d["stat_tgt"]=[]
				for k,e in enumerate(("Str","Dex","Int")):Kit.add_label(f.g,e+":",a,c+3);g=a+Kit.text_w(e+":")+8;b=str(P[k])if P[k]else "";h=Kit.with_tip(Kit.add_textbox(f.g,b,g,c,44,numbers=True),"%s target (1-%d, empty = none)"%(af[k],aE));d["stat_tgt"].append([h,b,b,0.]);a=g+44+24
			def l(f,x,a):
				g,b=f.g,f.store;Kit.add_label(g,"Name:",x+12,a+3);c=x+12+Kit.text_w("Name:")+8;d=x+w-12-D("Save current");f.c["ls_name"]=Kit.with_tip(Kit.add_textbox(g,"",c,a,max(60,d-c-14),numbers=False),"Name for Save current (empty = Set 1, Set 2 and so on)");Kit.art_button(g,b,"ls_save",Kit.ART_OK,d,a-1,"Save current","Save every skill's lock as a set (same name replaces it)");a+=28
				if not O:Kit.add_label(g,"No lock sets yet. Type a name and click Save current.",x+12,a+3,Kit.HUE_INFO)
				e=x+w-12-D("Delete");h=e-12-D("Apply")
				for k,(j,i)in enumerate(O):l,m=i.count("u"),i.count("d");Kit.add_label(g,Kit.fit("%s  (%d up, %d down)"%(j,l,m),h-x-24),x+12,a+3);Kit.art_button(g,b,"ls_apply_%d"%k,Kit.ART_OK,h,a-1,"Apply","Put this set's locks on your skills");Kit.art_button(g,b,"ls_del_%d"%k,Kit.ART_CLOSE,e,a-1,"Delete","Delete this lock set");a+=26
			def m(f,x,a):
				g,b=f.g,f.store;e=x+w-12-D("Delete");f.c["grp"]=[]
				if not q["ok"]:Kit.add_label(g,"The client's skill groups can't be read.",x+12,a+3,Kit.HUE_BAD);a+=28
				for c,d in enumerate(q["list"]):
					h=Kit.with_tip(Kit.add_textbox(g,d["name"],x+12,a,200,numbers=False),"Group name (type to rename)");Kit.add_label(g,Kit.count(len(d["members"]),"skill"),x+226,a+3,Kit.HUE_INFO)
					if c>0:Kit.art_button(g,b,"grp_del_%d"%c,Kit.ART_CLOSE,e,a-1,"Delete","Delete this group (its skills go to the first one)")
					else:Kit.add_label(g,"first group",e+35,a+3,Kit.HUE_INFO)
					f.c["grp"].append((h,c,d["name"]));a+=28
				if q["ok"]and not q["list"]:a+=28
				Kit.art_button(g,b,"grp_new",Kit.ART_OK,x+12,a-1,"New group","Add an empty group (Next group in the window moves skills in)");Kit.art_button(g,b,"grp_reset",Kit.ART_CLOSE,x+12+D("New group")+16,a-1,"Reset groups","Put back the client's default groups (click twice)")
			c,d=W["log_lines"];a={"ch":24,"pad":6};return(("WINDOW",[("check",)+v for v in dc]+[h(*y)for y in bI]+b(df,2),a),("SECTIONS  (what the window shows)",[("check",)+L+({"stay":G%2==0 and G<4,"dx":12+(G%2)*g},)for G,L in enumerate(dd)]+[("num","log_lines","Recent gains lines:","Lines the Recent gains part shows (%d-%d)"%(c,d),None,c,d)],a),("STAT TARGETS",[("custom",28,i),("check","lock_stat_target","Lock a stat when it reaches its target","Off: only a journal line when it gets there")]+b(dg,2),a),("LOCK SETS  (saved locks)",(("custom",28+max(1,len(O))*26,l),),a),("GROUPS  (the client's skill groups)",(("custom",max(1,e)*28+28,m),),a),("TOOLS",[("buttons",(("export",Kit.ART_PLAY,"Export sheet","Write every skill's values to a file in the VirtueAssistantSettings folder"),("ask",Kit.ART_PLAY,"Ask server","Ask the server for fresh skill values"),("newsess",Kit.ART_PLAY,"New session","Start a new session: gains count from now")))]+b(de,0),dict(a,bdy=-1,bgap=16)))
		def bJ():
			if j["width"]:return "Width: %d px (drag a corner)"%j["width"]
			return "Width: natural (drag a corner)"
		def di(ctrl,default,lo,hi,dec):
			try:a=str(ctrl.Text or "").strip()
			except Exception:a=""
			try:v=int(round(float(a.replace(",","."))*10))if dec else int(a);return max(lo,min(hi,v))
			except(ValueError,OverflowError):return default
		def dj(f):
			c=f.c;ad["skip"]=ad["sync"]
			if ad["sync"]:
				ad["sync"]=False;b=c["num"].get("rows")
				if b is not None:b.SetText(str(j["rows"]))
				if c.get("width_v")is not None:Kit.set_text(c["width_v"],bJ())
				return
			bK(c,False)
			for b,d,h in list(c.get("grp",())):
				try:g=str(b.Text or "")
				except Exception:g=str(h or "")
				if g!=h and d<len(q["list"]):q["list"][d]["obj"].Name=q["list"][d]["name"]=g;aa();c["grp"]=[(r,m,g if m==d else v)for r,m,v in c["grp"]];e["grp_dirty_at"]=time.time()
			i=f.store
			for a in list(i[0].keys()):
				if not Kit.was_clicked(i,a):continue
				if a=="ls_save":E.add(("ls_save",str(c["ls_name"].Text or "")),dup=True)
				elif a.startswith(("ls_apply_","ls_del_","grp_del_")):k,l,n=a.rpartition("_");E.add((k,int(n)),dup=True)
				else:E.add((a,),dup=True)
				HOST.poke()
		def dk(f,new):
			if ad["skip"]:new.update(j);return
			for k,a in f.c["num"].items():b,c=W[k];new[k]=di(a,j[k],b,c,k=="total_cap")
		def dl(old,new):
			aa()
			if any(new[a]!=old[a]for a in b7):e["m"]=None;e["rebuild"]="window"
			e["warned_cap"]=False;e["cap_at"]=0.
		ac=Kit.Page(j,dh,X,dl,adjust=dk,clicks=dj);dm=.8
		def bK(c,final):
			b=time.time()
			for k,e in enumerate(c.get("stat_tgt")or()):
				if final:a=e[2]
				else:
					try:a=str(e[0].Text or "").strip()
					except Exception:continue
					if a!=e[2]:e[2],e[3]=a,b;continue
				if a==e[1]or(not final and b-e[3]<dm):continue
				e[1]=a
				if a and not a.isdigit():continue
				v=max(0,min(aE,int(a)))if a else 0
				if v!=P[k]:P[k]=v;Kit.put_var(a9,",".join(str(d)for d in P));aa();cx(k)
		def dn():
			if ac.f is not None:bK(ac.f.c,True)
			ac.closed();ad["sync"]=False
			if e.get("grp_dirty_at"):e["grp_dirty_at"]=0.;E.add(("grp_save",),dup=True)
		def bL():
			e["ready"]=True
			for i in range(l["n"]):A["base"].setdefault(i,l["cur"][i][0])
			if A["stats"]is None and any(t["cur"]):A["stats"]=list(t["cur"])
		def bM():g,p["g"]=p["g"],None;p.update({"c":{},"rows":[],"rowmap":{}});ak.clear();Kit.dispose(g)
		bc();bf()
		def do():
			e.update({"shutting":False,"docked":HOST.dock_soon(I),"hidden":False,"queue":[],"rebuild":None,"desc":None,"m":None,"ready":False,"asked":0.,"swallow_until":0.,"warned_cap":False,"hl":{},"log":[],"gains":{},"started":time.time(),"ref_at":0.,"grp_at":0.,"tgt_shown":None,"stat_pending":{},"dirty":True,"redraw_at":0.,"desc_key":None,"cap_at":0.,"resize_at":0.,"grp_dirty_at":0.,"read_at":0.,"stats_at":0.});U.update({"gumps":None,"sig":None,"full_at":0.});bc();cl();cm();bf();cn();e["minimized"]=j["minimized"]or HOST.dock_wanted(I);bh(True);bj();bk();Y(True)
			if bl():bL()
			F.update({"width":None,"rows":None,"slot":None,"k":1.,"full":None});au();aR();HOST.dock_add(I,dict(cH,on=aT,show=aT,fit=cj,exact=True,verify=True,drawn_at=ck))
			if j["replace"]:aS()
		def dp():
			a=time.time()
			if p["g"]is not None and Kit.was_clicked(p["store"],"close"):
				if j["x_hides"]:e["hidden"]=True;aF();bM();z("hidden; %s brings it back."%by(),Kit.HUE_INFO)
				else:Kit.dispose(p["g"]);return
			if e["resize_at"]and a-e["resize_at"]>=bT and not safe(lambda:SNAP.pressed(),False):e["resize_at"]=0.;cJ()
			if p["g"]is not None and p["c"].get("more")and not e["rebuild"]:cL(a)
			if e["grp_dirty_at"]and a-e["grp_dirty_at"]>=b8:e["grp_dirty_at"]=0.;ae()
			i=l["n"]
			if not bh():
				while e["queue"]:
					d,f=bG(e["queue"].pop(0));b=bH.get(d)
					if b is not None:b(f)
				aS()
				if e["rebuild"]=="window":au()
				elif p["g"]is not None and p["c"]and e["desc"]is None:av(a)
				return
			if l["n"]!=i:e["rebuild"]="window"
			c,g={},False
			if not(e["ready"]and(p["g"]is None or not p["c"]or e["minimized"]or e["docked"])and a<e["read_at"]):
				e["read_at"]=a+cc;c=bj(not e["ready"])
				if e["stat_pending"]or a>=e["stats_at"]or not e["ready"]:e["stats_at"]=a+cd;g=bk()
			if c:ci()
			elif g:e["dirty"]=True
			if not e["ready"]:
				if bl():bL();ao();e["rebuild"]=e["rebuild"]or "rows"
				elif a-e["started"]>3. and not e["asked"]:bn()
			elif c:ct(c,a)
			if g and e["ready"]and(P[0]or P[1]or P[2]):cw()
			if e["ready"]and A["stats"]is None and any(t["cur"]):A["stats"]=list(t["cur"])
			Y();h=bool(e["queue"])
			if h:aa()
			while e["queue"]:
				d,f=bG(e["queue"].pop(0));b=bH.get(d)
				if b is not None:b(f)
			if c or h or a>=e["cap_at"]:
				e["cap_at"]=a+ce;k=e["warned_cap"];cv()
				if k!=e["warned_cap"]:aa()
			aS()
			if e["rebuild"]=="window":au();e["dirty"],e["redraw_at"]=False,a+a7;return
			if p["g"]is None or not p["c"]:return
			if not(e["minimized"]or e["docked"])and cT(a):aa()
			if not e["dirty"]and a<e["redraw_at"]:return
			e["dirty"],e["redraw_at"]=False,a+a7
			if e["minimized"]or e["docked"]:aQ(a);return
			av(a);aQ(a)
		def dq():
			e["shutting"]=True
			if e.get("grp_dirty_at"):e["grp_dirty_at"]=0.;safe(lambda:Kit.on_client(ae))
			bE();aF();X()
			if e["ready"]:ao()
			HOST.dock_remove(I);bM();cb.close()
		return{"start":do,"tick":dp,"stop":dq,"client_tick":True,"config_height":ac.height,"build_config":ac.build,"poll_config":ac.poll,"config_closed":dn,"thread_tick":bE,"thread_wanted":c2}
	def H():
		H="attention";k="Training Alarm";I="Attention_settings";ag="Attention_pos";ah="Attention_min";W=400;t,J=300,46;ai=7186;K=.25;L=1.;u=18;aj=2.;M=60.;N=.25;v=1.5;ak=5.;al=60.;am=("GM, Counselor, Seer, Admin, Administrator, Developer, Staff, Game Master");an="";O=("whisper","8");ao,x=5,120;ap,m=0,600;P=8;Q=60;R=.5;aq=500;S=60;ar=30;at=5.;T=(("gump","attention.gump","Gump nobody asked for",775),("staff","attention.staff","Staff in view",775),("name","attention.name","Someone says your name",824),("whisper","attention.whisper","A whisper to you",824),("hit","attention.hit","Hit while not fighting",497),("test","attention.test","Training Alarm test",775));U=dict((aX,aY)for aX,aY,aZ,aZ in T);V=("gump","staff","name","words","whisper","hit");c={"gump":True,"staff":True,"name":True,"words":True,"whisper":True,"hit":False,"markers":am,"ignore":an,"repeat":ao,"hold":ap,"anyalarm":True};aW=dict(c);a={"minimized":False,"shutting":False,"docked":False,"queue":[],"open_ids":{},"last_gid":0,"me":0,"my_name":"","name_re":None,"words_re":None,"seq":0};e={"g":None,"c":{},"store":({},{})};y={"skip":False};au={"done":False};z,o,B=Kit.basics(a,k);q={"looked":False,"get":None};d={"markers":None,"text":None,"ignore":frozenset(),"ignore_text":None}
		def r(text):return str(text or "").replace(";",",").replace("="," ").strip()
		def X():
			for k,v in Kit.codec_load(Kit.get_var(I)).items():
				if k in V or k=="anyalarm":c[k]=v=="1"
				elif k in("repeat","hold"):
					try:c[k]=max(0,min(x if k=="repeat"else m,int(v)))
					except ValueError:continue
				elif k in("markers","ignore"):c[k]=v
		def C():a=["%s=%d"%(f,1 if c[f]else 0)for f in V+("anyalarm",)];a+=["repeat=%d"%c["repeat"],"hold=%d"%c["hold"],"markers=%s"%r(c["markers"]),"ignore=%s"%r(c["ignore"])];Kit.put_var(I,";".join(a))
		def av():
			a=c["markers"]
			if d["text"]!=a:b=[f.strip()for f in str(a or "").split(",")if f.strip()];b.sort(key=len,reverse=True);d["markers"]=re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])"%"|".join(re.escape(g)for g in b),re.IGNORECASE)if b else None;d["text"]=a
			return d["markers"]
		def Y():
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
		def aw(kind):
			if ALERTS.quiet_on()or ALERTS.mute:return 0
			a,b=ALERTS.setting(U[kind]);return b if a else 0
		def Z():return bool(ALERTS.shown and ALERTS.alarm)
		def aa():
			if a["alarm"]:return True
			b=a["resume_at"]
			if b and 0<b-time.time()<=m+1:return True
			return bool(c["anyalarm"]and HOST.alarm_up())
		def h(kind,text,who=None,serial=0,gid=0,said=None,nm=""):
			b=not a["alarm"];d=False
			for r in a["alarm"]:
				if r["who"]==who:
					if r["text"]==text or(said is not None and r["said"]==said):return False
					d=True
			e=time.time()
			if b:a["seq"]+=1
			a["alarm"].append({"kind":kind,"text":text,"who":who,"serial":int(serial or 0),"gid":int(gid or 0),"at":e,"said":said,"nm":nm})
			if len(a["alarm"])>P:del a["alarm"][:-P]
			a["resume_at"]=0.
			if b:a["banner_seen"]=False;f=c["repeat"];a["next_sound"]=e+f if f>0 else 0.
			if d:j();return True
			HOST.alert(U[kind],text,"alarm",who="%s#%d"%(who or text,a["seq"]),name=nm,serial=serial);j();return True
		def D(how):
			if not a["alarm"]:return
			d=a["alarm"][-1];a["alarm"]=[];b=c["hold"];a["resume_at"]=time.time()+b if b>0 else 0.
			if how!="banner"and Z()and d["text"]and str(ALERTS.line).endswith(d["text"]):ALERTS.dismiss()
			B("answered; %s"%(("skill loops go on in %d s."%b)if b else "skill loops go on."),Kit.HUE_GOOD);a["last_answered"]=d;j()
		def ax(now):
			if not a["alarm"]:return
			if Z():a["banner_seen"]=True
			elif a["banner_seen"]:D("banner");return
			b=c["repeat"]
			if b>0 and not a["next_sound"]:a["next_sound"]=now+b
			if b>0 and not 0<a["next_sound"]-now<=b:
				a["next_sound"]=now+b;d=aw(a["alarm"][-1]["kind"])
				if d:API.PlaySound(d)
			if not 0<a["flash_at"]-now<=R:a["flash_at"]=now+R;a["flash_on"]=not a["flash_on"];j()
		def ay(now,p):
			if a["my_name"]and 0<=now-a["name_at"]<at:return
			a["name_at"]=now;b=str(p.Name or "").strip();a["me"]=int(p.Serial)
			if b and b!=a["my_name"]:
				a["my_name"]=b;a["name_re"]=re.compile(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])"%re.escape(b),re.IGNORECASE);c=[f for f in re.split(r"[^A-Za-z0-9']+",b)if f];d=[g for g in c if len(g)>=4]
				if len(c)>1 and d:a["words_re"]=re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])"%"|".join(re.escape(aX)for aX in d),re.IGNORECASE)
				else:a["words_re"]=None
		def az(g):
			if g is None:return
			try:a=g.Gump
			except Exception:return g
			return a if a is not None else g
		def E(g):
			try:return bool(g.IsDisposed)
			except Exception:return True
		def aA():
			if not q["looked"]:
				q["looked"]=True;a=[];t=n("ClassicUO.Input.Mouse")
				if t is not None:
					for b in("Position","LastLeftButtonClickTime","LastRightButtonClickTime"):
						m=Client._member(t,b)
						if m is not None:a.append((m[0],b=="Position"))
				q["get"]=a or None
			return q["get"]
		def aB(now):
			c=aA()
			if not c:return
			b=[]
			for e,f in c:v=e();b.append((int(v.X),int(v.Y))if f else int(v))
			b=tuple(b);d,a["input"]=a["input"],b
			if d is not None and b!=d:a["asked_at"]=now
			return True
		def aC(now):
			t=bool(HOST.typing());b,a["typing"]=a["typing"],t
			if b is not None and t!=b:a["typed_at"]=a["asked_at"]=now
		def aD(now):
			aC(now)
			if aB(now)is None:
				f=bool(API.HasTarget("any"))
				if a["cursor_up"]and not f:a["asked_at"]=now
				a["cursor_up"]=f
				if 0<=now-a["used_at"]<=v:a["asked_at"]=max(a["asked_at"],a["used_at"])
			b=int(API.HasGump()or 0);d=a["gump_obj"]
			if b and d is not None and b==a["gump_gid"]and not E(d):a["open_ids"][b]=now;return
			g=az(API.GetGump(b))if b else None
			if g is d or(g is not None and d is not None and b==a["gump_gid"]and not E(d)):
				a["gump_obj"]=g
				if b:a["open_ids"][b]=now
				return
			if d is not None and a["gump_vis"]and E(d):a["asked_at"]=now
			a["gump_obj"],a["gump_gid"]=g,b
			if g is None:a["gump_vis"]=False;return
			i=bool(g.IsVisible);a["gump_vis"]=i;a["last_gid"]=b;e=a["open_ids"];j=e.get(b);e[b]=now
			if len(e)>S:
				for k in sorted(e,key=e.get)[:len(e)-S]:del e[k]
			if HOST.gump_expected(b,now):return
			if not a["primed"]or not i or b in Y():return
			if j is not None and 0<=now-j<=al:return
			if 0<=now-a["asked_at"]<=v:return
			if c["gump"]:h("gump","A gump opened by itself (id 0x%X)"%b,"gump 0x%X"%b,gid=b)
		def aE(now):
			d=av()
			if d is None:return
			k=A(u);e,c,l=a["checked"],a["staff_seen"],a["me"]
			if len(e)>aq or d is not a["checked_pat"]:e.clear();a["checked_pat"]=d
			for m in k:
				try:s=int(m.Serial)
				except Exception:continue
				if s==l:continue
				b=e.get(s)
				if b is None or(not b[0]and b[2]<2 and now-b[1]>=aj):
					try:
						f=str(m.Name or "");g=f
						try:
							i=m.raw.NameAndProps(False)
							if i:g=f+"\n"+str(i).split("\n")[0]
						except Exception:pass
					except Exception:continue
					b=(bool(d.search(g)),now,(b[2]if b else 0)+1,f);e[s]=b
				if not b[0]:continue
				j=c.get(s);c[s]=now
				if j is None or not 0<=now-j<=M:h("staff","Staff in view: %s"%(b[3]or "someone"),"staff %X"%s,serial=s,nm=b[3])
			if len(c)>50:
				for n in[p for p,w in c.items()if not 0<=now-w<=M]:del c[n]
		def ab(name):
			a=name.lower()
			try:
				for m in A(u):
					if str(m.Name or "").lower()==a:return int(m.Serial)
			except Exception:pass
			return 0
		def ac(text):text=" ".join(str(text).split());return text if len(text)<=Q else text[:Q-2]+".."
		def aF(now):
			e=a["rd"]
			if e is None:return
			f=e.new()
			if not f:return
			g=a["my_name"].lower();i=a["name_re"];j=a["words_re"]if c["words"]else None
			for k in f:
				b=(k.name or "").strip();d=k.text
				if not b and ": "in d:b,d=[p.strip()for p in d.split(": ",1)]
				if not b or b.lower()=="system":continue
				l=b.lower()
				if g and l==g:
					if 0<=now-a["typed_at"]<=ak:a["asked_at"]=now
					continue
				if not c["name"]or i is None:continue
				if i.search(d)or(j is not None and j.search(d)):h("name",'%s said your name: "%s"'%(b,ac(d)),b,serial=ab(b),said=d,nm=b)
		def aG():
			q=a["heard"]
			if not q:return
			a["heard"]=[];d=a["my_name"].lower()
			for e,b,f in q:
				if not b or b.lower()=="system"or(d and b.lower()==d):continue
				if f in O and c["whisper"]:h("whisper",'%s whispers to you: "%s"'%(b,ac(e)),b,serial=ab(b),said=e,nm=b)
		def aH(*b):
			if a["active"]:a["used_at"]=time.time()
		F={}
		def aI(*d):
			if not a["active"]:return
			for b in d:
				try:
					c=b.MessageType;m=F.get(c)
					if m is None:
						m=str(c).lower()
						if len(F)<64:F[c]=m
				except Exception:continue
				if m in O:
					try:e=str(b.Text or "");f=str(b.Name or "")
					except Exception:continue
					q=a["heard"]
					if len(q)<ar:q.append((e,f,m))
				return
		def aJ(*b):
			if c["hit"]and not a.get("hit_poke"):a["hit_poke"]=True;HOST.poke("skills.alarm",False)
		def aK():Kit.hook_once(au,"done",("ObjectUsed",aH),("JournalEntryAdded",aI),("OnPlayerHitsChanged",aJ))
		def aL(p):
			if not c["hit"]:a["hp"]=None;return
			b=int(p.Hits);d=a["hp"];a["hp"]=b
			if d is None or p.IsDead or p.InWarMode or b>=d:return
			h("hit","You took %d damage while not fighting"%(d-b),"hit")
		def ad():
			if Follow.alt_held():
				r=a["alarm"][-1]if a["alarm"]else a.get("last_answered")
				if r is not None and r.get("serial"):o(("follow",r["serial"]))()
				return
			if a["alarm"]:o("answer")();return
			if a["minimized"]:
				b=time.time()
				if 0<=b-a.get("mini_click",0.)<=.6:a["mini_click"]=0.;o("toggle_min")()
				else:a["mini_click"]=b
		def ae():
			g,h,c=i.begin(W,Kit.MARGIN+30+Kit.GAP+96+Kit.MARGIN);M=Kit.MARGIN
			if a["minimized"]:c["line_w"]=t-90;c["alarm_hit"]=Kit.catcher(g,14,12,t-90,J-24,ad,"Click: answer the alarm. Double-click: restore. Alt+click: auto-follow (again to stop)",movable=True)
			else:
				d=W-2*M;i.frame(g);b=M+30+Kit.GAP;Kit.add_section(g,M,b,d,96);c["status"]=Kit.add_label(g,"",M+12,b+10,Kit.HUE_INFO);c["line2"]=Kit.add_label(g,"",M+12,b+32,Kit.HUE_INFO);c["line_w"]=d-28;c["alarm_hit"]=Kit.catcher(g,M+6,b+6,d-12,46,ad,"Click: answer the alarm. Alt+click: auto-follow (again to stop)",movable=True);e=M+12
				for k,l,f,m,n in(("here",Kit.ART_OK,"I'm here","Answer the alarm: skill loops go on (after the set pause)","answer"),("test",Kit.ART_PLAY,"Test","Raise a test alarm until you answer","test"),("ignore",Kit.ART_CLOSE,"Ignore this gump","Answer and ignore this gump from now on","ignore_gump")):p=Kit.art_button(g,h,k,l,e,b+62,f,m,on_click=o(n));e+=35+Kit.text_w(f)+14
				c["ignore"]=p
			i.end(g);a["drawn"]=None;j()
		i=Kit.Window(H,k,a,e,ae,ag,ah,(240,160),(t,J),ai,z,lock=True)
		def aM():
			b=[g for f,g in(("gump","gumps"),("staff","staff"),("name","your name"),("whisper","whispers"),("hit","hits"))if c[f]]
			if a["minimized"]:return "%s: %s"%(k,("watching "+", ".join(b))if b else "nothing ticked in settings")
			return("Watching: "+", ".join(b))if b else "Nothing ticked in settings"
		def j():
			q=e["g"]
			if q is None or(a["minimized"]and a["docked"]):return
			c=e["c"];h=c.get("line_w",200);b=a["alarm"]
			if b:
				r=b[-1];d=r["text"]
				if Kit.streamer:
					if r["nm"]:d=d.replace(r["nm"],Kit.veil("name",r["nm"],r["serial"]))
					if a["name_re"]is not None:d=a["name_re"].sub(Kit.veil("me",""),d)
				f=("%s: "%k if a["minimized"]else "ALARM: ")+d;i=Kit.HUE_BAD if a["flash_on"]else Kit.HUE_TEXT;j=("+%d more. "%(len(b)-1)if len(b)>1 else "")+"Skill loops paused: click here or I'm here"
			else:l=a["resume_at"]-time.time()if a["resume_at"]else 0;f,i=aM(),Kit.HUE_INFO;j=("Skill loops go on in %d s"%int(l+.99))if 0<l<=m+1 else "All quiet"
			n=(f,i,j,h)
			if n==a["drawn"]:return
			a["drawn"]=n;f=Kit.fit(f,h);Kit.set_text(c["status"],f,i)
			if "line2"in c:Kit.set_text(c["line2"],Kit.fit(j,h),Kit.HUE_INFO)
			o=c.get("ignore")
			if o is not None:
				g=bool(b)and b[-1]["kind"]=="gump"
				if c.get("ignore_on")!=g:
					c["ignore_on"]=g;o.IsVisible=g;p=e["store"][0].get("ignore")
					if p is not None:p.IsVisible=g
		def G(f):
			d=0
			if f:
				for r in reversed(a["alarm"]):
					if r["kind"]=="gump"and r["gid"]:d=r["gid"];break
			if not d:d=a["last_gid"]
			if not d:B("no server gump seen yet.",Kit.HUE_INFO);return
			if d not in Y():e=c["ignore"].strip().strip(",");c["ignore"]=(e+", "if e else "")+"0x%X"%d;C();b(H);B("gump 0x%X ignored."%d,Kit.HUE_INFO)
		def aN(action):G(True);D("click")
		aO={"follow":lambda action:Follow.toggle(action[1],k),"answer":lambda action:D("click"),"test":lambda action:h("test","Test alarm: answer it to go on","test"),"ignore_gump":aN,"ignore_last":lambda action:G(False)}
		def aP(w):a={"top":32,"ldy":4,"fh":30,"align":True,"sh":126};return(("TRIGGERS  (each pauses skill loops too)",(("check","gump","A server gump nobody asked for","Not within %.1f s of your mouse, typing or a gump closing; not a page of an open window or an ignored id"%v),("check","staff","Staff in view (a staff word in name or title)","Within %d tiles, a name or title holding a staff word (list below)"%u),("check","name","Someone says your name","Read from the game (whole words, any case)"),("check","words","Or any word of it with 4 letters or more","For a name of two words or more: \"Wolf\" in \"Grey Wolf\"",{"dx":34}),("check","whisper","Someone whispers to you","Lines the client marks as whispered"),("check","hit","You take damage while not in war mode","Something hurts you while you train (off at first)")),{"top":32,"sh":194}),("STAFF AND GUMPS",(("text","markers","Staff words:","Words marking a staff name or title, commas between (whole words, any case; empty: no check)"),("text","ignore","Gump ids to ignore:","Gump ids that never raise the alarm: hex (0x1A2B) or decimal, commas between"),("buttons",(("ignore_last",Kit.ART_OK,"Ignore last gump","Ignore the last server gump seen",o("ignore_last")),),{"bdy":0,"stay":True}),("note",af(),{"dx":12+35+Kit.text_w("Ignore last gump")+14,"ndy":3,"key":"last"})),a),("ALARM  (sound: Settings > Alerts)",(("num","repeat","Repeat the sound every:","Seconds between sounds until you answer (0-%d, 0 = once)"%x,"s",0,x),("num","hold","Loops stay paused after you answer:","Seconds loops stay paused after you answer (0-%d, 0 = none)"%m,"s",0,m),("check","anyalarm","Any alarm pauses skill loops","While any module's alarm banner waits for a click (Ultima Tracker > Lookout, a red in your house)")),dict(a,fw=40,ugap=12)))
		def af():return("Last server gump: 0x%X"%a["last_gid"])if a["last_gid"]else "No server gump seen yet"
		def aQ(f):
			y["skip"]="ignore_last"in a["queue"]
			if y["skip"]:a["queue"].remove("ignore_last");G(False)
		def aR(f,new):
			if y["skip"]:new.update(c);return
			for k in("markers","ignore"):v=r(new[k]);new[k]=v if v!=r(c[k])else c[k]
			Kit.set_text(f.c["last"],af(),Kit.HUE_INFO)
		def aS(old,new):a["drawn"]=None
		s=Kit.Page(c,aP,C,aS,adjust=aR,clicks=aQ);X()
		def aT():
			a.update({"shutting":False,"docked":False,"active":True,"alarm":[],"queue":[f for f in a["queue"]if f=="ignore_last"],"resume_at":0.,"next_gump":0.,"gump_obj":None,"gump_gid":0,"gump_vis":False,"primed":False,"input":None,"asked_at":0.,"used_at":0.,"cursor_up":False,"typing":None,"typed_at":0.,"next_staff":0.,"checked":{},"staff_seen":{},"name_at":0.,"next_hit":0.,"hp":None,"heard":[],"next_sound":0.,"banner_seen":False,"flash_at":0.,"flash_on":False,"drawn":None,"last_answered":None,"rd":l(),"checked_pat":None,"minimized":i.start_min()});X();aK()
			for k,b,c,d in T:HOST.alert_kind(b,c,d)
			z.service("attention.up",aa);ae();i.dock()
		def aU():
			if e["g"]is None:return
			if Kit.closed(e):return
			b=time.time()
			while a["queue"]:
				d=a["queue"].pop(0)
				if i.action(d):continue
				f=aO.get(d[0]if isinstance(d,tuple)else d)
				if f is not None:f(d)
			p=HOST.me()
			if p is None:return
			ay(b,p)
			if not 0<a["next_gump"]-b<=K:a["next_gump"]=b+K;aD(b);a["primed"]=True
			if c["staff"]and not 0<a["next_staff"]-b<=L:a["next_staff"]=b+L;aE(b)
			aF(b);aG()
			if a.pop("hit_poke",False)or not 0<a["next_hit"]-b<=N:a["next_hit"]=b+N;aL(p)
			ax(b)
			if not a["alarm"]and a["resume_at"]:
				if not aa():a["resume_at"]=0.
				j()
		def aV():a["shutting"]=True;a["active"]=False;a["alarm"]=[];a["resume_at"]=0.;C();a["rd"]=None;a["gump_obj"]=None;z.close()
		return{"start":aT,"tick":aU,"stop":aV,"client_tick":True,"config_height":s.height,"build_config":s.build,"poll_config":s.poll,"config_closed":s.closed}
	def I():
		n="skillbags";F="Skill Bags";aq="SkillBags_settings";aU="SkillBags_pos";aV="SkillBags_min";ar="SkillBags_rules";at="SkillBags_done";aW=740;au,aX=240,46;aY=3702;av=42;ad=8;R=300;aZ=6;a_=5.;a0=2.;ae=3.;a1=2.5;a2=6.;a3=1.5;a4=4;a5=10.;a6={"item identification":3.,"arms lore":3.,"detect hidden":3.};S,af=.5,60.;aw=1;ag=.25;T=.5;a7=5372;a8=("must wait","too far away","cannot reach","can't reach","can't see that","cannot see that","already casting","you are busy");a9="Paused: guard zone";ba=HOLD_TEXT["unknown"];bb="SkillBags_results_pos";ax=200;ay=16;bc=680;U=18;V="skillbags.results";az="Skill Bags Results";bd=500;ah=2*Kit.MARGIN+30+Kit.GAP+30+24+8;be="No results shown. Click a rule's Results.";bf=160;bg="SkillBags_%08X_rule%d.txt";bh=("durable","substantial","massive","fortified","indestructable","indestructible","defense","guarding","hardening","fortification","invulnerability","accurate","ruin","might","force","power","vanquishing","silver","slaying","slaughter","thrashing","repond","terathan","bane","reptilian death","dismissal","gargoyle's foe","damnation","exorcism","ophidian","spider's death","arachnid doom","dousing","dissipation","vacuum","elemental health","earth shatter","blood drinking","summer wind","elemental ban","slayer","magic");bi="unidentified";bj={"itemid":{2:"not certain"},"armslore":{2:"not certain",4:"read"},"tasteid":{2:"not certain",4:"read"},"removetrap":{1:"disarmed",2:"trap, not disarmed",3:"no trap"},"lockpick":{1:"unlocked",2:"still locked",3:"not locked"},"cartography":{1:"decoded",2:"not decoded",3:"can't decode"}};bk=re.compile(r"\b("+"|".join(bh)+r")\b");bl=re.compile(r"\[[^\]]*:\s*\d+\s*\]");bm=re.compile(r"\bmagic\b");H=[("itemid","Item Identification","skill","Item Identification",3.2,0,(),("not certain","no idea how much","tell much about it"),()),("armslore","Arms Lore","skill","Arms Lore",3.2,0,(),("not certain","tell much about it"),()),("tasteid","Taste Identification","skill","Taste Identification",10.2,0,(),("not certain","tell much about it","can't tell"),()),("removetrap","Remove Trap","skill","Remove Trap",10.2,1,("render the trap harmless","successfully"),("fail to disarm",),("doesn't appear to be trapped","isn't trapped","not trapped")),("lockpick","Lockpicking (uses lockpicks)","tool",a7,1.5,1,("lock quickly yields",),("unable to pick the lock",),("does not appear to be locked","cannot be picked by normal means","did not need to be unlocked")),("cartography","Cartography (decode maps)","use",None,1.,3,("successfully decode",),("fail to make anything of the map",),("too difficult to attempt to decode","not a map")),("use","Double-click each item","use",None,1.,0,(),(),()),("cskill","Custom skill (name in Custom)","cskill",None,10.2,0,(),(),()),("ctool","Custom tool (graphic in Custom)","ctool",None,1.5,0,(),(),()),];bn=[b4[1]for b4 in H];M=[("all","Every item"),("containers","Containers only"),("graphics","Graphics in Text (hex)"),("name","Name contains Text")];bo=[b5[1]for b5 in M];bp={1:"OK",2:"failed",3:"skipped",4:"done"};o={"hidden":True,"war":True,"open":True,"retries":aw,"guard":True};b3=dict(o);h=[];c={"minimized":False,"shutting":False,"docked":False,"queue":[]};q={"g":None,"c":{},"store":({},{}),"rows":[]};ai,E,m=Kit.basics(c,F);A={"f":None,"rows":[],"next_read":0.};k={"g":None,"rule":None,"c":{},"rows":[],"page":0,"dirty":False,"minimized":False,"shutting":False,"docked":False,"queue":[]}
		def aA(s):return str(s or "").replace("|","/").replace("~","-")
		def aB(v,default):
			try:v=float(v)
			except Exception:return default
			return max(S,min(af,v))
		def aC(action=0):a=H[action];return{"action":action,"bag":0,"filt":a[5],"text":"","custom":"","delay":a[4],"deep":False,"auto":False,"done":{},"order":[]}
		def D(r):return H[r["action"]]
		def aj(r):a=H[r["action"]];b=a[3]if a[2]=="skill"else r["custom"].strip()if a[2]=="cskill"else "";return a6.get(b.lower(),a5)if b else 0.
		def aD(text):
			b=[]
			for a in str(text or "").replace(";",",").split(","):
				a=a.strip()
				if not a:continue
				try:b.append(int(a,16)if a.lower().startswith("0x")else int(a,0))
				except Exception:
					with Kit.quiet:b.append(int(a,16))
			return b
		def aE():
			p=Kit.get_var(aq).split("|")
			if len(p)>=4:
				for n,k in enumerate(("hidden","war","open")):o[k]=p[n]=="1"
				try:o["retries"]=max(0,min(9,int(p[3])))
				except Exception:o["retries"]=aw
			o["guard"]=(p[5]=="1")if len(p)>=6 else True;del h[:];a=Kit.get_var(ar)
			if a:
				for e in a.split("|"):
					f=e.split("~")
					if len(f)<8:continue
					try:r=aC(max(0,min(len(H)-1,int(f[0]))));r.update({"bag":int(f[1])if f[1]else 0,"filt":max(0,min(len(M)-1,int(f[2]))),"text":f[3],"custom":f[4]});r.update({"delay":max(aB(f[5],D(r)[4]),aj(r)),"deep":f[6]=="1","auto":f[7]=="1"});h.append(r)
					except Exception:continue
					if len(h)>=ad:break
			a=Kit.get_var(at)
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
		def I():Kit.put_var(aq,"|".join(["1"if o["hidden"]else "0","1"if o["war"]else "0","1"if o["open"]else "0",str(o["retries"]),"0","1"if o["guard"]else "0"]));Kit.put_var(ar,"|".join("~".join([str(a["action"]),str(a["bag"]),str(a["filt"]),aA(a["text"]),aA(a["custom"]),"%.2f"%a["delay"],"1"if a["deep"]else "0","1"if a["auto"]else "0"])for a in h));ak()
		def ak():Kit.put_var(at,"|".join(",".join("%d:%d"%(d,a["done"][d])for d in a["order"]if d in a["done"])for a in h))
		def W(r,serial,code):
			if serial not in r["done"]:r["order"].append(serial)
			r["done"][serial]=code;a=r["order"]
			if len(a)>R:
				k=len(a)-R;b=r["done"]
				for d in a[:k]:b.pop(d,None)
				del a[:k]
			c["save_done"]=True
		def bq(a,code,answer):
			if a[0]=="itemid"and code in(1,4):
				b=(answer or "").lower()
				if not b:return "no answer"
				if bi in b:return "unidentified"
				if bl.search(b):return "magic"
				k=b.find("[")
				if k>=0:return "magic"if bk.search(b,k)else "plain"
				return "magic"if bm.search(b)else "plain"
			c=bj.get(a[0])
			if c is not None and code in c:return c[code]
			return bp.get(code,"done")
		def al(j):
			if j.get("match_raw"):return j["match_raw"]
			a=j.get("raw")
			if not a:return ""
			b=(j.get("name")or "").lower();c=None
			for k in range(len(a)-1,-1,-1):
				d,e=a[k];f=e.lower()
				if((b and(f==b or(len(b)>=3 and b in d.lower())))or d.lstrip().startswith("[")):return d
				if c is None and(not e or f=="system"):c=d
			return c if c is not None else a[-1][0]
		def X(r,serial,code,name,answer,tag=None):
			a=r.get("_res")
			if a is None:a=r["_res"]=[]
			for b in range(len(a)-1,-1,-1):
				if a[b][1]==serial:del a[b];break
			answer=str(answer or "").replace("\n"," ").strip()[:bf];a.append((time.time(),serial,name or("0x%08X"%serial),code,tag or bq(D(r),code,answer),answer))
			if len(a)>ax:del a[:-ax]
			r.pop("_rescount",None)
			if k["rule"]is r:k["dirty"]=True
		def am(r):
			r.pop("_res",None);r.pop("_rescount",None)
			if k["rule"]is r:k["dirty"]=True
		def aF(r):
			a=r.get("_rescount")
			if a is None:
				b=r.get("_res")or[]
				if not b:a="No results yet."
				else:
					c={}
					for e in b:c[e[4]]=c.get(e[4],0)+1
					a="%s: %s"%(Kit.count(len(b),"item"),", ".join(["%d %s"%(f,d)for d,f in sorted(c.items(),key=lambda a:(-a[1],a[0]))]))
				r["_rescount"]=a
			return a
		N=Kit.find_item
		def J(r,short=True):
			if not r["bag"]:return "no bag yet"
			c=time.time();b=r.get("_bagname")
			if b is not None and b[0]==r["bag"]and c<b[1]:a=b[2]
			else:
				d=N(r["bag"])
				if d is None:a="bag not found"
				else:a=safe(lambda:str(d.Name or ""),"")or "0x%08X"%r["bag"]
				r["_bagname"]=(r["bag"],c+a0,a)
			return a if short else "%s  0x%08X"%(a,r["bag"])
		def Y(r=None):
			for a in([r]if r is not None else h):a.pop("_cache",None);a.pop("_bagname",None)
		def aG(r,it):
			f=M[r["filt"]][0]
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
		def br(serial):
			try:return int(API.Contents(serial)or 0)
			except Exception:return-1
		def bs(r,i,now,p=True):
			q=N(r["bag"])if r["bag"]else None
			if q is None:r.pop("_cache",None);return[],0,False
			a=r.get("_cache");h=br(r["bag"]);f=False
			if(a is None or a["count"]!=h or now>=a["relist"]or a["bag"]!=r["bag"]):
				if not p:
					if a is None:return
					f=None
				else:f=True
			if f:
				try:j=list(API.ItemsInContainer(r["bag"],bool(r["deep"]))or[])
				except Exception:j=[]
				if M[r["filt"]][0]=="graphics":r["_gfx"]=set(aD(r["text"]))
				d=a["scans"]if a is not None else{};k,l=[],[]
				for c in j:
					try:b=int(c.Serial)
					except Exception:continue
					if b==r["bag"]:continue
					e=aG(r,c)
					if e is None and b in r["done"]:e=True
					if e is None:l.append((b,c))
					elif e:k.append((b,c));d.pop(b,None)
				a={"bag":r["bag"],"count":h,"relist":now+a_,"items":k,"pending":l,"scans":d};r["_cache"]=a
			elif a["pending"]:
				n=[]
				for b,c in a["pending"]:
					e=aG(r,c)
					if e is None:n.append((b,c))
					elif e:a["items"].append((b,c))
				a["pending"]=n
			d=a["scans"];g=[]
			for b,c in a["pending"]:
				o=d.get(b,0)+1;d[b]=o
				if o>=aZ:d.pop(b,None);g.append((b,c));a["items"].append((b,c));W(r,b,3);X(r,b,3,"","its name never came","skipped (no name)");m("0x%08X skipped, its name never came (rule %d)."%(b,i+1),Kit.HUE_INFO)
			if g:s=set(t for t,v in g);a["pending"]=[w for w in a["pending"]if w[0]not in s]
			if len(d)>R:d.clear()
			return a["items"],len(a["pending"]),f
		def bt(serial):
			a=N(serial)
			if a is None:return False
			try:
				if a.Opened:return True
			except Exception:pass
			try:return int(API.Contents(serial)or 0)>0
			except Exception:return False
		def O(t,now):return not 0<t-now<=af
		def bu(r,now,d=True):
			a=r["bag"]
			if not a or not Kit.in_pack(a):return False
			if bt(a):c["opening"].pop(a,None);r["_closed"]=False;return True
			r["_closed"]=True
			if not o["open"]or not d:return False
			b=c["opening"].get(a)
			if b is None or O(b+a1+a2,now):c["opening"][a]=now;API.UseObject(a)
			return False
		def aH(now):
			if c["paused"]:return "Paused"
			p=HOST.me()
			if p is None:return "No player"
			a=HOST.fight_hold(now)
			if a=="dead":return "Dead"
			if o["hidden"]and p.IsHidden:return "Hidden"
			if a=="war":return "War mode"
			b=c["guard_paused"]
			if b=="unknown":return ba
			if b:return a9
			if a:return "Paused: "+HOLD_TEXT.get(a,a)
			if z(n):return "Cursor busy"
			if API.HasTarget("any"):return "Cursor up"
			return
		def bv(now):
			n=len(h)
			if not n:return
			l=c["rr"]%n;e=False
			for p in range(n):
				i=(l+p)%n;r=h[i]
				if not(r["auto"]or i in c["run"])or not r["bag"]:r.pop("_closed",None);continue
				if D(r)[2]=="ctool"and i not in c["run"]:
					if r["auto"]:Z(i,r);m("rule %d: a custom tool runs only on Run."%(i+1),Kit.HUE_BAD)
					continue
				if not Kit.in_pack(r["bag"]):
					c["run"].discard(i);c["budget"].pop(i,None);m("rule %d: its bag isn't in your backpack."%(i+1),Kit.HUE_BAD)
					if r["auto"]:Z(i,r)
					continue
				if not bu(r,now,i in c["run"]):continue
				f=bs(r,i,now,not e)
				if f is None:continue
				b,g,j=f
				if j:e=True;c["rr"]=i+1
				r["_count"]=(sum(1 for t,v in b if t in r["done"]),len(b));k=False;a=c["budget"]
				if i in c["run"]and D(r)[2]=="ctool"and i not in a:a[i]=(r["_count"][1]-r["_count"][0]+g)*(1+o["retries"])
				for d,q in b:
					if d in r["done"]:continue
					if not O(c["later"].get((i,d),0.),now):k=True;continue
					if i in a:
						if a[i]<=0:c["run"].discard(i);a.pop(i,None);m("rule %d stopped at its count (%s)."%(i+1,J(r)),Kit.HUE_INFO);break
						a[i]-=1
					return i,r,d,q
				if i in c["run"]and not g and not k and j is not None:c["run"].discard(i);c["budget"].pop(i,None);m("%s on %s, %d of %d handled."%(D(r)[1],J(r),r["_count"][0],r["_count"][1]),Kit.HUE_GOOD)
			return
		def Z(i,r):
			c["run"].discard(i);r["auto"]=False;I()
			if i<len(q["rows"]):q["rows"][i]["auto"].IsChecked=False
			if A["f"]is not None:b(n)
		def bw(i,r,serial,it,now):
			d=D(r);a=d[2];j={"rule":i,"serial":serial,"t":now,"phase":"target","reader":None,"lines":[],"raw":[],"name":safe(lambda:str(it.Name or ""),"")}
			if a in("skill","cskill"):
				e=d[3]if a=="skill"else r["custom"].strip()
				if not e:m("rule %d needs a skill name in its Custom box."%(i+1),Kit.HUE_BAD);Z(i,r);return False
				u(n,ae+.5);j["reader"]=l();API.UseSkill(e)
			elif a in("tool","ctool"):
				b=d[3]
				if a=="ctool":
					f=aD(r["custom"]);b=f[0]if f else 0
					if not b:m("rule %d needs a tool graphic in its Custom box."%(i+1),Kit.HUE_BAD);Z(i,r);return False
				g=API.FindType(int(b),API.Backpack)
				if not g:
					if O(c["no_tool"].get(i,0.),now):c["no_tool"][i]=now+10.;m("no tool 0x%04X in your backpack for rule %d."%(int(b),i+1),Kit.HUE_BAD)
					c["later"][(i,serial)]=now+10.;c["run"].discard(i);return False
				u(n,ae+.5);j["reader"]=l();API.UseObject(g.Serial)
			else:j["reader"]=l();API.UseObject(serial);j["phase"]="recover"
			c["job"]=j;return True
		aI={"t":None}
		def bx():
			t=aI["t"]
			if t is None:
				a=set([APP_NAME.lower()+":"])
				for b in HOST.slots:
					a.add(str(b.title).lower()+":")
					for c in(b.parts or()):
						if len(c)>1:a.add(str(c[1]).lower()+":")
				t=aI["t"]=tuple(a)
			return t
		def by(j,a):
			c=(a.kind or "").upper()
			if c=="CLIENT"or a.low.startswith(bx()):return False
			b=(a.name or "").strip().lower()
			if not b or b=="system":return True
			if c!="OBJECT":return False
			if not j["name"]and not j.get("named"):j["named"]=True;d=N(j["serial"]);j["name"]=safe(lambda:str(d.Name or "")if d is not None else "","")
			return b==j["name"].strip().lower()or a.text.startswith("[")
		def an(j,a):
			f=j["reader"]
			if f is None:return
			b,e=j["lines"],j["raw"];g=False
			for c in f.new():
				if c.text and not c.text.startswith(F):
					if not by(j,c):continue
					b.append(c.low);g=True;e.append((c.text,c.name or ""))
					if len(b)>40:del b[:-40];del e[:-40]
			if not b:return
			if not g:return j.get("res")
			d=next(((r,i)for r,s in(("busy",a8),("skip",a[8]),("ok",a[6]),("fail",a[7]))for t in s for i in range(len(b))if t in b[i]),None)
			if d is not None:j["match"]=b[d[1]];j["match_raw"]=e[d[1]][0]
			h=j["res"]=d[0]if d is not None else None;return h
		def P(j,r,res,now):
			i,a=j["rule"],j["serial"];b=(i,a);d=None;e=aj(r)if res=="busy"else 0.
			if e>0 and "must wait"in(j.get("match")or ""):c["later"][b]=now+e;d=now+min(r["delay"],e)
			elif res=="busy":
				n=c["busy_n"].get(b,0)+1
				if n>=a4:c["busy_n"].pop(b,None);W(r,a,2);X(r,a,2,j["name"],al(j)or "no answer from the shard","no answer");m("giving up on 0x%08X (no answer from %s)."%(a,D(r)[1]),Kit.HUE_BAD)
				else:c["busy_n"][b]=n;c["later"][b]=now+a3
			elif res=="fail":
				c["busy_n"].pop(b,None);f=r.setdefault("_tries",{});n=f.get(a,0)+1
				if n<=o["retries"]:f[a]=n;c["later"][b]=now+max(r["delay"],1.)
				else:f.pop(a,None);W(r,a,2);X(r,a,2,j["name"],al(j))
			else:c["busy_n"].pop(b,None);g={"ok":1,"skip":3}.get(res,4);W(r,a,g);X(r,a,g,j["name"],al(j))
			c["job"]=None;h=max(0.,now-j.get("t",now));c["next_scan"]=d if d is not None else now+(r["delay"]if res=="busy"else max(S,r["delay"]-h));c["status"]="%s: %s"%(D(r)[1],res or "done")
			if j.get("match"):r["_last"]="%s: %s"%(res,j["match"])
			elif j["lines"]:r["_last"]="%s, no phrase matched; the shard said: %s"%(res or "no answer",j["lines"][-1])
			else:r["_last"]="%s, no journal line in %.1f s"%(res or "no answer",max(0.,now-j.get("t",now)))
			if len(c["later"])>400:
				for k in[s for s,v in c["later"].items()if O(v,now)]:c["later"].pop(k,None)
			if len(c["busy_n"])>400:c["busy_n"].clear()
			if len(r.get("_tries",{}))>R:r["_tries"].clear()
		def bz(now):
			j=c["job"];r=h[j["rule"]]if j["rule"]<len(h)else None
			if r is None:e(n);c["job"]=None;return
			b=D(r)
			if j["phase"]=="target":
				a=an(j,b)
				if a:e(n);P(j,r,a,now);return
				if HOST.cursor_ok(n,"neutral"):API.Target(j["serial"]);e(n);j["phase"],j["t"]="recover",now
				elif z(n)is None and API.HasTarget("any"):e(n);P(j,r,"busy",now)
				elif now-j["t"]>ae:e(n);P(j,r,"busy",now)
				return
			if now-j["t"]<max(r["delay"],S):
				a=an(j,b)
				if a in("busy","skip","fail"):P(j,r,a,now)
				return
			P(j,r,an(j,b),now)
		def bA():
			d=not c["paused"]and(bool(c["run"])or any(f["auto"]and f["bag"]for f in h));a=None
			if d and(o["guard"]or "attention.up"not in HOST.services):a=HOST.guard_hold()
			if a!=c["guard_paused"]:
				c["guard_paused"]=a
				if d:
					if a=="guard":b="%s: paused in a guard zone; it goes on when you leave."%F
					elif a=="unknown":b=("%s: paused until the guard zone is known; cross a town's guard line once."%F)
					else:b="%s: out of the guard zone; going on."%F
					API.SysMsg(b,Kit.HUE_INFO)
		bB=1.5
		def bC(now):
			if c["job"]is not None:bz(now);return
			if not O(c["next_scan"],now):return
			bA()
			if not c["run"]and not any(f["auto"]and f["bag"]for f in h):
				c["next_scan"]=now+T
				if now>=c["idle_at"]:c["idle_at"]=now+bB;c["status"]=aH(now)or "Idle"
				return
			c["idle_at"]=0.;a=aH(now)
			if a:c["status"]=a;c["next_scan"]=now+T;return
			b=bv(now)
			if b is None:c["status"]="Watching"if any(g["auto"]and g["bag"]for g in h)else "Idle";c["next_scan"]=now+T;return
			i,r,d,e=b
			if bw(i,r,d,e,now):c["status"]="%s %d/%d"%(D(r)[1],r["_count"][0]+1,r["_count"][1])
			else:c["next_scan"]=now+T
		def bD(i):
			if c["pick"]is not None:m("already targeting a bag.",Kit.HUE_INFO);return
			c["pick"]=i;m("target the bag for rule %d."%(i+1),Kit.HUE_INFO)
			def a(serial):E.add(("picked",i,int(serial or 0)),dup=True)
			HOST.pick_target(20,a)
		def bE(i,serial):
			c["pick"]=None
			if i>=len(h):return
			if not serial:m("cancelled.",Kit.HUE_INFO);return
			a=N(serial)
			if a is None or not a.IsContainer:m("that isn't a container.",Kit.HUE_BAD);return
			if not Kit.in_pack(serial):m("that bag isn't in your backpack.",Kit.HUE_BAD);return
			r=h[i]
			if r["bag"]!=serial:r["bag"]=serial;r["done"].clear();del r["order"][:];c["later"].clear();Y(r);am(r)
			I();m("rule %d uses %s."%(i+1,J(r,False)),Kit.HUE_GOOD);c["redraw"]=True;b(n)
		def aJ():return aW,2*Kit.MARGIN+30+Kit.GAP+40+Kit.GAP+30+max(1,len(h))*av+8
		def Q():
			l,m=aJ();w,n=K.zone_slot(l,m)or(l,m);g,i,f=K.begin(w,n);M=Kit.MARGIN;o=[]
			if not c["minimized"]:
				d=w-2*M;K.frame(g);e=M+30+Kit.GAP;Kit.add_section(g,M,e,d,40);f["pause"]=Kit.art_button(g,i,"pause",Kit.ART_PLAY,M+12,e+9,"Resume"if c["paused"]else "Pause","Stop or restart every rule",on_click=E("pause"));p=M+12+35+Kit.text_w("Resume")+14;Kit.art_button(g,i,"add",Kit.ART_OK,p,e+9,"Add rule","Add a rule (set it up on the settings page)",on_click=E("add"));q=p+35+Kit.text_w("Add rule")+14;f["status"]=Kit.add_label(g,"",q,e+12,Kit.HUE_INFO);f["status_w"]=M+d-4-q;c["full_txt"]=None;j=e+40+Kit.GAP;Kit.add_section(g,M,j,d,n-j-M,"RULES  (a bag and an action each)");r=j+30;s=M+d-12-35-Kit.text_w("Reset");t=s-35-Kit.text_w("Run")-6;u=t-35-Kit.text_w("Bag...")-6;v=u-35-Kit.text_w("Results")-6;f["last_w"]=d-36-16
				if not h:Kit.add_label(g,"No rules yet. Click Add rule, then set its bag and action.",M+12,r+5,Kit.HUE_INFO)
				for k,x in enumerate(h):
					b=r+k*av;a={};a["auto"]=Kit.add_check(g,"",M+10,b+2,x["auto"],"Handle every new item that lands in this bag");a["bag"]=Kit.add_label(g,"",M+36,b+3,Kit.HUE_TEXT);a["act"]=Kit.add_label(g,"",M+172,b+3,Kit.HUE_TITLE);a["prog"]=Kit.add_label(g,"",M+298,b+3,Kit.HUE_INFO);a["last"]=Kit.with_tip(Kit.add_label(g,"",M+36,b+22,Kit.HUE_INFO),"The shard's last answer to this rule and how it was read (ok, fail, skip or busy)")
					for y,z,A,B,C,D in(("res",Kit.ART_PAGE,v,"Results","Show the shard's answer per item (again: close)","results"),("bag",Kit.ART_PLAY,u,"Bag...","Target the bag this rule works on","bag"),("run",Kit.ART_PLAY,t,"Run","One pass over the items not done yet","run"),("reset",Kit.ART_CLOSE,s,"Reset","Forget what was done, so every item is handled again","reset")):Kit.art_button(g,i,"%s%d"%(y,k),z,A,b+1,B,C,on_click=E((D,k)))
					a["text"]=(None,None,None,None);o.append(a)
			K.end(g,{"rows":o});c["redraw"]=False;aK()
		K=Kit.Window(n,F,c,q,Q,aU,aV,mini=(au,aX),icon=aY,cleanup=ai,lock=True);p=Kit.fit
		def aK():
			if c["minimized"]and c["docked"]:return
			f=q["c"].get("status")
			if f is not None:
				l=(Kit.HUE_BAD if c["paused"]else(Kit.HUE_GOOD if c["job"]else Kit.HUE_INFO));g="mini_txt"if c["minimized"]else "full_txt";b=c.get(g)
				if b is None or b[0]!=c["status"]:b=c[g]=(c["status"],p("%s: %s"%(F,c["status"]),au-90)if c["minimized"]else p(c["status"],q["c"].get("status_w",400)))
				Kit.set_text(f,b[1],l)
			if c["minimized"]:return
			j=time.time()
			if j<c["next_rows"]:return
			c["next_rows"]=j+ag
			for i,a in enumerate(q["rows"]):
				if i>=len(h):break
				r=h[i];k=r.get("_count");d="closed"if r.get("_closed")else "%d/%d"%k if k else ""
				if c["job"]and c["job"]["rule"]==i:d+="  working"
				elif i in c["run"]:d+="  pass"
				e=r.get("_last")or "";t=(J(r),D(r)[1],d,e)
				if t!=a["text"]:a["text"]=t;Kit.set_text(a["bag"],p(t[0],130));Kit.set_text(a["act"],p(t[1],120));Kit.set_text(a["prog"],p(t[2],96));Kit.set_text(a["last"],p("Last: "+e if e else "Last: no answer read yet",q["c"].get("last_w",500)))
		def bF():
			a=False
			for i,c in enumerate(q["rows"]):
				if i>=len(h):break
				try:v=bool(c["auto"].IsChecked)
				except Exception:continue
				if v!=h[i]["auto"]:h[i]["auto"]=v;a=True
			if a:I();b(n)
		aa,ao=230,120
		def ap(r):return next((a for a in range(len(h))if h[a]is r),-1)
		def bG(i):
			if i>=len(h):return
			r=h[i]
			if k["rule"]is r and Kit.is_open(k["g"]):ab();return
			k["rule"],k["page"]=r,0
			if Kit.is_open(k["g"]):k["dirty"]=True
			else:ac()
		def aL():return bd,ah+4*U
		def ab():
			k["rule"]=None
			if Kit.zone_up(V):ac()
			else:L.close()
		def bH():
			if Kit.zone_up(V)or k["rule"]is not None and k["g"]is not None:ac()
			elif k["g"]is not None:L.close()
		def ac():
			M=Kit.MARGIN;e=Kit.zone_up(V);z=L.slot if e else None;o,p=aL()
			if z is not None and(z[0]<o or z[1]<p):z=None
			w=z[0]if z is not None else bc;n=L.rows(U,ah,ay)if z else ay;h=z[1]if z is not None else ah+n*U;d=w-2*M;q=h-M-30-Kit.GAP-M;g,b,c=L.begin(w,h);Kit.add_window_frame(g,w,h);Kit.add_section(g,M,M,d,30)
			if not e:Kit.art_button(g,b,"close",Kit.ART_CLOSE,w-M-54,M+4,None,"Close the results",on_click=E("res_close"))
			j=w-M-(10 if e else 66)-35-Kit.text_w("Export");Kit.art_button(g,b,"export",Kit.ART_OK,j,M+4,"Export","Write the results to a file in the VirtueAssistantSettings folder",on_click=E("res_export"));k=j-12-35-Kit.text_w("Clear");Kit.art_button(g,b,"clear",Kit.ART_CLOSE,k,M+4,"Clear","Forget these results (items stay done; Reset handles them again)",on_click=E("res_clear"));c["title"]=Kit.add_label(g,"",M+30,M+7,Kit.HUE_TITLE);c["title_w"]=k-(M+30)-8;a=M+30+Kit.GAP;Kit.add_section(g,M,a,d,q,"RESULTS  (newest first)");l=M+d-12-35-Kit.text_w("Next");Kit.art_button(g,b,"older",Kit.ART_PAGE,l,a+24,"Next","Older results",on_click=E("res_older"));f=l-10-35-Kit.text_w("Prev");Kit.art_button(g,b,"newer",Kit.ART_PAGE,f,a+24,"Prev","Newer results",on_click=E("res_newer"));c["page_x"],c["page_y"]=f-8,a+28;c["page"]=Kit.add_label(g,"",c["page_x"],a+28,Kit.HUE_INFO);c["counts"]=Kit.add_label(g,"",M+12,a+28,Kit.HUE_TEXT);c["counts_w"]=f-(M+12)-16-Kit.text_w("page 99 of 99");c["ans_w"]=d-12-aa-ao-8;m=[];r=a+30+24
			for s in range(n):i=r+s*U;m.append({"name":Kit.add_label(g,"",M+12,i,Kit.HUE_TEXT),"tag":Kit.add_label(g,"",M+12+aa,i,Kit.HUE_INFO),"ans":Kit.add_label(g,"",M+12+aa+ao,i,Kit.HUE_INFO),"tip":None})
			L.end(g,{"rows":m});aM()
		L=Kit.Window(V,az,k,k,ac,bb,default=(260,220),cleanup=ai,lock=True,owner=False,clear={"rows":[],"rule":None,"c":{}});bI={1:Kit.HUE_GOOD,2:Kit.HUE_BAD,3:Kit.HUE_INFO,4:Kit.HUE_TEXT}
		def aM():
			k["dirty"]=False;r,d,c=k["rule"],k["rows"],k["c"]
			if not d:return
			if r is None:Kit.set_text(c["title"],p(az.upper(),c["title_w"]));Kit.set_text(c["counts"],p(be,c["counts_w"]));return
			i=ap(r)
			if i<0:ab();return
			e=len(d);h=r.get("_res")or[];n=len(h);f=max(1,(n+e-1)//e);j=k["page"]=max(0,min(k["page"],f-1));Kit.set_text(c["title"],p("RULE %d RESULTS: %s"%(i+1,D(r)[1]),c["title_w"]));Kit.set_text(c["counts"],p(aF(r),c["counts_w"]));g="page %d of %d"%(j+1,f)if f>1 else ""
			if Kit.set_text(c["page"],g)and g:Kit.ui_pos(c["page"],c["page_x"]-Kit.text_w(g),c["page_y"])
			q=n-1-j*e;s=time.localtime()[:3]
			for t,a in enumerate(d):
				l=q-t
				if l>=0:
					u,A,v,w,m,b=h[l];o=time.localtime(u);x=time.strftime("%H:%M"if o[:3]==s else "%b %d %H:%M",o);Kit.set_text(a["name"],p("%s  %s"%(x,v),aa-8));y=Kit.HUE_TITLE if m=="magic"else bI.get(w,Kit.HUE_INFO);Kit.set_text(a["tag"],p(m,ao-8),y);Kit.set_text(a["ans"],p(b or "no answer",c["ans_w"]))
					if a["tip"]!=b:a["tip"]=b;a["ans"].SetTooltip(b or "")
				else:
					for z in("name","tag","ans"):Kit.set_text(a[z],"")
		def bJ():
			r=k["rule"];i=ap(r)if r is not None else-1
			if i<0:return
			a=r.get("_res")or[]
			if not a:m("rule %d has no results to export yet."%(i+1),Kit.HUE_INFO);return
			d=Kit.data_path(bg%(int(API.Player.Serial),i+1));b=["Skill Bags results - rule %d: %s on %s"%(i+1,D(r)[1],J(r,False)),"Exported %s - %s"%(time.strftime("%Y-%m-%d %H:%M"),aF(r)),"","%-19s  %-10s  %-32s  %-18s  %s"%("Time","Serial","Item","Result","The shard's answer")]
			for t,s,e,h,f,g in a:b.append("%-19s  0x%08X  %-32s  %-18s  %s"%(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(t)),s,e,f,g))
			c["writes"].append((d,"\n".join(b)+"\n"))
		def aN():C(c["writes"],F,"results")
		def bK():return bool(c["writes"])
		def bL(action):
			c["paused"]=not c["paused"];c["idle_at"]=0.
			if c["paused"]and c["job"]is not None:e(n);c["job"]=None
			a=q["c"].get("pause")
			if a is not None:Kit.set_text(a,"Resume"if c["paused"]else "Pause")
			m("%s."%("paused"if c["paused"]else "resumed"),Kit.HUE_INFO)
		def bM(action):
			if len(h)>=ad:m("at most %d rules."%ad,Kit.HUE_INFO);return
			h.append(aC());I();Q();b(n)
			if A["f"]is None:B(n)
		def bN(action):
			i=action[1]
			if c["job"]is not None and c["job"]["rule"]==i:e(n);c["job"]=None
			elif c["job"]is not None and c["job"]["rule"]>i:c["job"]["rule"]-=1
			a=h.pop(i)
			if k["rule"]is a:ab()
			elif k["rule"]is not None:k["dirty"]=True
			c["rr"]=0;c["run"]=set(d-1 if d>i else d for d in c["run"]if d!=i);c["budget"].clear();c["later"].clear();c["busy_n"].clear();c["no_tool"].clear();I();Q();b(n)
		def bO(action):
			i=action[1]
			if not h[i]["bag"]:m("set the bag for rule %d first (Bag button)."%(i+1),Kit.HUE_BAD);return
			c["run"].add(i);c["budget"].pop(i,None);c["later"].clear();Y(h[i]);c["next_scan"]=0.
		def bP(action):i=action[1];h[i]["done"].clear();del h[i]["order"][:];h[i].pop("_tries",None);h[i].pop("_last",None);Y(h[i]);c["later"].clear();ak();m("rule %d will handle every item again (%s)."%(i+1,J(h[i])),Kit.HUE_INFO)
		def bQ(action):
			if k["rule"]is not None:am(k["rule"]);k["page"]=0
		def aO(action):k["page"]+=1 if action=="res_older"else-1;k["dirty"]=True
		bR={"pause":bL,"add":bM,"remove":bN,"run":bO,"reset":bP,"bag":lambda action:bD(action[1]),"picked":lambda action:bE(action[1],action[2]),"results":lambda action:bG(action[1]),"res_close":lambda action:ab(),"res_export":lambda action:bJ(),"res_clear":bQ,"res_older":aO,"res_newer":aO};bS=5.;bT=118;aP=("The OK / FAIL / SKIP phrases that read the shard's answers are RunUO defaults, not checked on this shard; the window's Last line shows each rule's last answer.");aQ="Hex graphics with commas (0x14FC, 0x0E76), or part of a name (treasure map)";aR="The skill's client name (Item Identification), or the tool's hex graphic (0x14FC: lockpicks)";aS=("Seconds between items (%g-%g; a skill rule waits at least its 3 or 10 s timer)"%(S,af));bU="Also handle items in bags inside it";bV="Handle every new item that lands in the bag (the window's box too)"
		def aT(w,a=None,dds=None):
			def b(i,r):
				def b(f,x,y):g,b,c=f.g,y-30,{};Kit.add_label(g,"Action:",x+12,b+34);dds.append(("action",i,x+70,b+30,210,bn,r["action"]));Kit.with_tip(Kit.add_label(g,"Custom:",x+296,b+34),aR);c["custom"]=Kit.with_tip(Kit.add_textbox(g,r["custom"],x+356,b+30,130,numbers=False),aR);Kit.art_button(g,f.store,"rm%d"%i,Kit.ART_CLOSE,x+f.w-12-35-Kit.text_w("Remove"),b+28,"Remove","Remove this rule",on_click=E(("remove",i)));Kit.add_label(g,"Items:",x+12,b+62);dds.append(("filt",i,x+70,b+58,210,bo,r["filt"]));Kit.with_tip(Kit.add_label(g,"Text:",x+296,b+62),aQ);c["text"]=Kit.with_tip(Kit.add_textbox(g,r["text"],x+356,b+58,f.w-356-16,numbers=False),aQ);Kit.with_tip(Kit.add_label(g,"Delay (s):",x+12,b+90),aS);c["delay"]=Kit.with_tip(Kit.add_textbox(g,"%g"%r["delay"],x+90,b+86,50,numbers=False),aS);c["deep"]=Kit.add_check(g,"Look inside bags within the bag",x+160,b+88,r["deep"],bU);c["auto"]=Kit.add_check(g,"Auto (watch the bag)",x+420,b+88,r["auto"],bV);a.append(c)
				return("RULE %d  (%s)"%(i+1,p(J(r,False),300)),(("custom",0,b),),{"sh":bT})
			return([("OPTIONS",[("check","hidden","Pause while hidden","Using a skill would reveal you"),("check","open","Open bags the client hasn't looked in","On Run, double-clicks the bag once so its contents are known",{"stay":True}),("buttons",(("add",Kit.ART_OK,"Add rule","Add a rule (a bag and an action)",E("add")),),{"dx":400}),("num","retries","Extra tries after a failure:","Retries after a FAIL phrase (0-9)",None,0,9,{"lw":268,"fw":40,"ldy":4,"ltip":True,"h":2,"clamp":False}),("check","guard","Pause in guard zones","No skill use in towns or an unknown zone; unticked counts only while Skills > Training Alarm is on",{"dx":380})]+[("note",d,{"h":18})for d in Kit.wrap(aP,w-24)or[aP]],{"pad":6})]+[b(j,s)for j,s in enumerate(h)])
		bW=Kit.Page(o,aT)
		def bX(g,x,y,w):
			a,c=[],[];f=Kit.Form(g,x,y,w,o,aT(w,a,c))
			for e,i,h,j,k,l,m in sorted(c,key=lambda d:-d[3]):b=G.CreateDropDown(k,list(l),int(m));b.SetPos(h,j);g.Add(b);a[i][e]=b
			A.update({"f":f,"rows":a,"next_read":0.})
		def bY():
			l=A["f"]
			if l is None:return
			p=time.time()
			if p<A["next_read"]:return
			A["next_read"]=p+ag;e=[];s=[]
			try:
				t=l.read(True);a=t!=o;o.update(t)
				for i,f in enumerate(A["rows"]):
					if i>=len(h):break
					r=h[i];u=False
					for g,w in(("action",H),("filt",M)):
						d=int(f[g].GetSelectedIndex())
						if 0<=d<len(w)and d!=r[g]:
							r[g]=d;a=True;e.append(r)
							if g=="action":u=True;r["filt"]=H[d][5];r["delay"]=H[d][4];r["done"].clear();del r["order"][:];am(r);A["dirty"]=True;break
					for k in("custom","text"):
						v=str(f[k].Text or "").strip()
						if v!=r[k]:r[k]=v;a=True;e.append(r)
					if not u:
						j=aB(str(f["delay"].Text or "").strip(),r["delay"]);j=max(j,aj(r))
						if abs(j-r["delay"])>.001:r["delay"]=j;a=True
					for k in("deep","auto"):
						v=bool(f[k].IsChecked)
						if v!=r[k]:r[k]=v;a=True;(e if k=="deep"else s).append(r)
			except Exception as x:A["f"]=None;m("settings page error: %s (reopen the page)."%x,Kit.HUE_BAD);return
			if a:
				I()
				for r in e:Y(r)
				for r in s:
					i=ap(r)
					if 0<=i<len(q["rows"]):
						try:q["rows"][i]["auto"].IsChecked=r["auto"]
						except Exception:c["redraw"]=True
				if A.get("dirty"):A["dirty"]=False;b(n)
		def bZ():A["f"]=None;A["rows"]=[]
		aE()
		def b_():c.update({"shutting":False,"docked":False,"queue":[],"paused":False,"job":None,"next_scan":0.,"next_check":0.,"status":"Idle","run":set(),"budget":{},"opening":{},"later":{},"pick":None,"redraw":False,"save_done":False,"no_tool":{},"busy_n":{},"next_rows":0.,"rr":0,"guard_paused":None,"writes":[],"idle_at":0.,"done_at":0.,"minimized":K.start_min()});k.update({"g":None,"rule":None,"c":{},"rows":[],"page":0,"dirty":False,"minimized":False,"shutting":False,"docked":False,"queue":[]});aE();Q();K.dock(fit=True,min=aJ);L.dock(fit=True,min=aL)
		def b0():
			if q["g"]is None:return
			if Kit.closed(q):return
			b=time.time()
			while c["queue"]:
				a=c["queue"].pop(0);d=a[0]if isinstance(a,tuple)else a
				if K.action(a)or(d in("remove","bag","run","reset")and a[1]>=len(h)):continue
				e=bR.get(d)
				if e is not None:e(a)
			if c.get("redraw"):Q()
			if k["queue"]:del k["queue"][:];bH()
			if k["dirty"]and k["g"]is not None:aM()
			if not c["minimized"]and b>=c["next_check"]:c["next_check"]=b+ag;bF()
			bC(b)
			if c.get("save_done")and b>=c["done_at"]:c["save_done"]=False;c["done_at"]=b+bS;ak()
			aK()
		def b1():j=c["job"];return.05 if j is not None and j["phase"]=="target"else.1
		def b2():
			c["shutting"]=k["shutting"]=True
			if c["job"]is not None:e(n);c["job"]=None
			I();ai.close()
			if c["writes"]:
				if Client.on_client_thread():m("the export wasn't written (the module stopped); export again.",Kit.HUE_INFO);del c["writes"][:]
				else:aN()
		return{"start":b_,"tick":b0,"stop":b2,"client_tick":True,"config_height":bW.height,"build_config":bX,"poll_config":bY,"config_closed":bZ,"thread_tick":aN,"thread_wanted":bK,"interval":b1}
	J=(("window",F,.25,"skills"),("alarm",H,.1,"attention"),("bags",I,.1,"skillbags"),);return PartSet(D,E,J).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("skills","Skills","Skills, training and AFK alarms",_module_skills,.1,category="Skills and home",parts=(("window","Skills Window","Skills with locks, groups and gains",True,("skills",)),("alarm","Training Alarm","Alarm when staff or a gump needs you",False,("attention",)),("bags","Skill Bags","A skill on each item in a bag, once",False,("skillbags",)),),aliases=('Skill Bags','Attention','GM check','training','locks','gains','Item ID'))
