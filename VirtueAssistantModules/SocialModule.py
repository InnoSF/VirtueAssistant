def _module_social():
	R=Client._type;am=Follow.alt_held;a6=HOST.mobile;a7=HOST.mobiles;Y=Kit.ART_CLOSE;an=Kit.ART_OK;G=Kit.ART_PAGE;Z=Kit.ART_PLAY;U=Kit.GAP;l=Kit.HUE_BAD;S=Kit.HUE_GOOD;k=Kit.HUE_INFO;C=Kit.HUE_TEXT;L=Kit.HUE_TITLE;ao=Kit.MARGIN;D=Kit.add_label;ap=Kit.add_section;aK=Kit.add_textbox;a8=Kit.add_tiled;H=Kit.art_button;a9=Kit.caption_tip;aa=Kit.count;aq=Kit.get_var;ba=Kit.pic_size;ar=Kit.put_var;q=Kit.set_text;z=Kit.text_w;I=Kit.veil;ab=Kit.with_tip;at="social";N="Social";bb="Social_settings";b9="Social_pos";ca="Social_min";bc="Social_names";bd="Social_guild";be="Social_roster";cb=7956;cc=460;cd=600;bf,ce=240,46;cf=24;bg,bh=4,16;bi=8;bj=[("friends","Friends"),("party","Party"),("guild","Guild"),("profile","Profile")];bk={"friends":"Show TazUO's friends list and their health","party":"Show your party: members, invites, loot and chat","guild":"Show your guild: info, roster and chat","profile":"Show your character and the client's windows"};cg=((60,1,"just now"),(3600,60,"%d min ago"),(86400,3600,"%d h ago"),(172800,86400,"%d day ago"),(0,86400,"%d days ago"));bl=.25;ci=2.;cj=1.;ck=15;bm=4.;au="Diplomacy";aL=3;aM=9999;aN=150;av=90;cl=64;cm=120;cn=200;ac,aw="My Guild","Guild Roster";aO,co=1,2;bn=7;cp=40;cq=300;bo=5;aP=120;bp=60;cr=600;cs=(1062939,1062940,1063035);ct=("not a member of any guild","abbreviation:");bq={1062954:"Guild Name",1063025:"Alliance",1063084:"Guild Faction",1062955:"Name",1062956:"Rank",1062952:"Last On",1062953:"Guild Title",1063015:"Online",1062959:"Leader",1062960:"Warlord",1062961:"Emissary",1062962:"Member",1062963:"Ronin",1062974:aw,1063014:ac,1062978:au,1062992:"Invite Player",3006115:"Resign"};aQ=(1063014,1062974,1062978);cu=("1063014","1062974","1062978");cv=(ac.lower(),aw.lower(),au.lower());cw=("Unknown","Innocent","Ally","Gray","Criminal","Enemy","Murderer","Invulnerable");FS,RS="\x1f","\x1e";J,V,O="|",";","~";aR="Social_notes";aS=500;br=200;cx="Social_note_pos";cy=440;ad=[("online","Sort: online","Online"),("laston","Sort: last on","Last on"),("rank","Sort: rank","Rank"),("name","Sort: name","Name")];T=[dA[0]for dA in ad];bs=(("leader","guild leader"),("warlord",),("emissary",),("member",),("ronin",));cz=re.compile(r"(\d{1,4})\s*([-/.])\s*(\d{1,2})\s*[-/.]\s*(\d{1,4})");d={"tab":"friends","rows":bi,"bars":True,"announce":True,"gevery":bo,"ghide":True,"dbutton":aL,"left":False,"gsort":"online"};dz=dict(d);a={"shutting":False,"minimized":False,"docked":False,"queue":[],"friends":[],"names_dirty":False,"party":None,"profile":None,"msg":{},"gids":{},"me_s":0,"fserials":[],"notos":{}};j={"g":None,"c":{},"store":({},{})};ax,o,f=Kit.basics(a,N);K=[];B={};A={"dirty":False,"ver":0,"chg":{}};W={"g":None,"c":{},"store":({},{}),"name":""};M=ao
	def bt():
		p=aq(bb).split("|")
		def b(i,lo,hi,a):
			try:return max(lo,min(hi,int(p[i])))
			except Exception:return a
		if len(p)>=4:
			if p[0]in bk:d["tab"]=p[0]
			d.update({"rows":b(1,bg,bh,bi),"bars":p[2]=="1","announce":p[3]=="1"})
		if len(p)>=6:d.update({"gevery":b(4,0,aP,bo),"ghide":p[5]=="1"})
		if len(p)>=8:d.update({"dbutton":b(6,0,aM,aL),"left":p[7]=="1"})
		if len(p)>=9 and p[8]in T:d["gsort"]=p[8]
		c={}
		for e in aq(bc).split("|"):
			if "="in e:
				s,n=e.split("=",1)
				with Kit.quiet:c[int(s)]=n
		a["names"]=c;cA();cC()
	def ay():ar(bb,"|".join([str(int(d[b]))if isinstance(d[b],bool)else str(d[b])for b in("tab","rows","bars","announce","gevery","ghide","dbutton","left","gsort")]))
	def aT():
		if not a["names_dirty"]:return
		a["names_dirty"]=False;b=sorted(a["names"].items())[-200:];ar(bc,"|".join("%d=%s"%(c,e.replace("|","/").replace("=","-"))for c,e in b))
	def P():return{"ok":False,"in_guild":True,"name":"","alliance":"","faction":"","charter":"","website":"","members":[],"at":0.,"note":""}
	def az(s):s=str(s or "").replace(FS," ").replace(RS," ").replace("\n"," ").strip();return s.replace(O,O+"t").replace(J,O+"p").replace(V,O+"s")
	def aU(s):return str(s or "").replace(O+"p",J).replace(O+"s",V).replace(O+"t",O)
	def bu(raw,a,b):
		if FS in raw or RS in raw:return raw.split(a)
		return[aU(c)for c in raw.split(b)]
	def cA():
		b=P();c=bu(aq(bd),FS,J)
		if len(c)>=7:
			b["name"],b["alliance"],b["faction"],b["charter"],b["website"]=c[:5]
			try:b["at"]=float(c[5])
			except Exception:b["at"]=0.
			b["in_guild"]=c[6]!="0";b["ok"]=b["at"]>0
		e=[];d=aq(be)
		for g in d.split(RS if FS in d or RS in d else V):
			f=bu(g,FS,J)
			if len(f)>=5 and f[0]:e.append({"name":f[0],"rank":f[1],"laston":f[2],"title":f[3],"online":f[4]=="1","me":False})
		b["members"]=e;a["guild"]=b
	def cB():b=a["guild"]or P();ar(bd,J.join([az(b[c])for c in("name","alliance","faction","charter","website")]+["%d"%int(b["at"]or 0),"1"if b["in_guild"]else "0"]));ar(be,V.join(J.join([az(e[g])for g in("name","rank","laston","title")]+["1"if e["online"]else "0"])for e in b["members"][:cq]))
	def cC():
		try:a=str(API.GetPersistentVar(aR,"",API.PersistentVar.Account)or "")
		except Exception:a=""
		bv(a)
	def bv(raw):
		a={}
		for b in raw.split(V):
			f=[aU(c).strip()for c in b.split(J)]
			if len(f)>=2 and f[0]and f[1]and len(a)<aS:a[f[0].lower()]=(f[0],f[1])
		for k,v in list(A["chg"].items()):
			if v is None:a.pop(k,None)
			else:a[k]=v
		for k in[e for e in B if e not in a]:del B[k]
		B.update(a);A["ver"]+=1
	def bw():
		if not A["dirty"]:return
		A["dirty"]=False;a=dict(A["chg"]);c=dict((h,None if g is None else J.join([az(g[0]),az(g[1])]))for h,g in a.items())
		try:d=str(API.GetPersistentVar(aR,"",API.PersistentVar.Account)or "");b=Kit.merge_text(d,c,lambda rec:aU(rec.split(J)[0]).strip().lower(),V)[0];API.SavePersistentVar(aR,b,API.PersistentVar.Account)
		except Exception as e:A["dirty"]=True;f("couldn't save the notes (%s); they're saved with the next change."%e,l);return
		for k,v in a.items():
			if A["chg"].get(k,0)==v:A["chg"].pop(k,None)
		bv(b)
	def cD(a):e=B.get(str(a or "").strip().lower());return e[1]if e else ""
	def bx():A["dirty"]=True;A["ver"]+=1;K.append(bw)
	def cE(name,text):
		name=" ".join(str(name or "").split());text=" ".join(str(text or "").split())[:br]
		if not name:f("type a name first.");return False
		k=name.lower()
		if not text:
			if B.pop(k,None)is not None:A["chg"][k]=None;f("note on %s deleted."%name);bx()
			return True
		if k not in B and len(B)>=aS:f("at most %d notes; delete one first."%aS,l);return False
		B[k]=A["chg"][k]=(name,text);bx();f("note on %s saved."%name,S);return True
	u=Kit.fit
	def aA(name,serial=0,me=False):
		if me:return I("me",name)
		b=Kit.noto_mark(a["notos"].get(serial,0))if Kit.cblind and serial else ""
		if Kit.streamer:name=I("name",name,serial or Kit.checksum(name.lower().encode("utf-8")))
		return b+" "+name if b else name
	def aB():return Kit.pitch(cf)
	def by():return bool(Client.key_held("shift"))
	def ae(part,on):
		if part[0]is not None and part[1]!=on:part[1]=on;Kit.set(part[0],"IsVisible",on)
	def cF(n):
		if n is None:return ""
		try:i=int(n)
		except Exception:i=-1
		return cw[i]if 0<=i<8 else str(n).split(".")[-1]
	def E():
		s=a["me_s"]
		if not s:
			try:s=int(API.Player.Serial or 0)
			except Exception:s=0
			a["me_s"]=s
		return s
	def cG():
		b=a["profile"]
		if b and b[0]:return b[0]
		try:return str(API.Player.Name or "")
		except Exception:return ""
	def bz(t):return "never"if not t else Kit.ago(time.time()-t,cg)
	class CL(object):
		looked=False;error="";world=None;GA=None;UIM=None;FLM=None
		@staticmethod
		def call(obj,name,a=(),t=None):return Tz.call(obj,name,a,t,True)
		@staticmethod
		def find():
			if CL.looked:return
			CL.looked=True
			try:d=API.GetType().Assembly
			except Exception as b:CL.error="no client access (%s)"%b;return
			a=Typing._get(API,"World")
			if a is None:c=Typing._get(None,"Game",R("ClassicUO.Client"));a=Typing._get(Typing._get(c,"UO"),"World")
			CL.world=a;CL.GA=R("ClassicUO.Game.GameActions");CL.UIM=R("ClassicUO.Game.Managers.UIManager");CL.FLM=R("ClassicUO.Game.Managers.FriendsListManager")
			if a is None:CL.error="client World not found"
			elif CL.GA is None:CL.error="GameActions not found"
		@staticmethod
		def on_main(fn,need=True):
			if not need:return
			a,b=Client.on_main_ex(fn)
			if a=="ok":return b
			CL.error=Client.error or "can't run on the client thread";return
		@staticmethod
		def game_action(name,a=(),b=True):
			c=([CL.world]if b else[])+list(a)
			def d():CL.call(None,name,c,CL.GA);return True
			return bool(CL.on_main(d,CL.GA is not None))
		@staticmethod
		def friends():
			def a():
				a=Typing._get(None,"Instance",CL.FLM)
				if a is None:return
				b=[]
				for f in(CL.call(a,"GetFriends")or[]):c=f.GetType();b.append((int(Typing._get(f,"Serial",c)or 0),str(Typing._get(f,"Name",c)or "")))
				return b
			return CL.on_main(a,CL.FLM is not None)
		@staticmethod
		def party():
			a=CL.world
			def b():
				b=Typing._get(a,"Party")
				if b is None:return
				e=int(Typing._get(b,"Leader")or 0);f=int(Typing._get(b,"Inviter")or 0);g=bool(Typing._get(b,"CanLoot")or False);c=Typing._get(a,"Player");h=int(Typing._get(c,"Serial")or 0)if c is not None else 0;d=[]
				for m in(Typing._get(b,"Members")or[]):
					if m is not None:
						s=int(Typing._get(m,"Serial")or 0)
						if s and s!=h:d.append(s)
				return(e,f,g,d)
			return CL.on_main(b,a is not None)
		@staticmethod
		def open_ignore_list():
			def a():
				import System
				if CL.bring_to_front("IgnoreManagerGump"):return True
				t=R("ClassicUO.Game.UI.Gumps.IgnoreManagerGump")
				if t is None:raise Exception("IgnoreManagerGump not found")
				g=System.Activator.CreateInstance(t,System.Array[object]([CL.world]));CL.call(None,"Add",[g],CL.UIM);return True
			return bool(CL.on_main(a,CL.world is not None and CL.UIM is not None))
		@staticmethod
		def bring_to_front(a):
			for g in Typing._get(None,"Gumps",CL.UIM)or():
				if g is not None and g.GetType().Name==a and not g.IsDisposed:CL.call(g,"BringOnTop");return True
			return False
		@staticmethod
		def find_server_gump(test):
			def a():
				for g in Typing._get(None,"Gumps",CL.UIM)or():
					if g is None or g.IsDisposed:continue
					try:
						a=Typing._get(g,"PacketGumpText")
						if not a:continue
						a=str(a)
						if test(a):return int(Typing._get(g,"ServerSerial")or 0),a
					except Exception:continue
				return 0,""
			r=CL.on_main(a,CL.UIM is not None);return r if r else(0,"")
		@staticmethod
		def press_labelled(gump,label):
			a=safe(lambda:gump.Gump);gump=a if a is not None else gump;c=label.lower().strip()
			def d():
				import System;e,a,d=[],[],[]
				def f(ch):x=int(Typing._get(ch,"ScreenCoordinateX")or 0);return x,int(Typing._get(ch,"ScreenCoordinateY")or 0)
				def g(ctrl):
					for b in list(Typing._get(ctrl,"Children")or[]):
						if b is None:continue
						j=b.GetType().Name
						if j=="Button":d.append(f(b)+(int(Typing._get(b,"ButtonID")or 0),))
						else:
							i=Typing._get(b,"Text");h=Kit.strip_html(i).lower()if i else ""
							if h and c in h:(e if h==c else a).append(f(b))
						g(b)
				g(gump);a=e or a
				if not a or not d:return False
				j,k=a[0]
				def h(b):return abs(b[0]-j)+abs(b[1]-k)
				i=min(d,key=h)
				if h(i)>80:return False
				CL.call(gump,"OnButtonClick",[System.Int32(i[2])]);return True
			return bool(CL.on_main(d))
	def bA(serial):
		m=a6(serial)
		if m is None:return
		try:return(str(m.Name or ""),int(m.Hits or 0),int(m.HitsMax or 0),int(m.Distance),bool(m.IsDead),True)
		except Exception:return
	def bB(serial):
		b=a["mobs"];d=b.get(serial)
		if d is not None and d[5]is None:
			d=bA(serial)
			if d is None:b.pop(serial,None)
			else:b[serial]=d
		return d
	def cH():
		i=time.time()
		if i<a["next_friends"]:return
		a["next_friends"]=i+ci;d=CL.friends();l=d is not None
		if d is None:d=[(int(m),a["names"].get(int(m),""))for m in API.GetAllFriends()or()]
		j=E();g=(j,d)if l else None
		if g is not None and g==a["friends_raw"]:
			if a["names_dirty"]:K.append(aT)
			return
		f=[];k=False
		for b,c in d:
			if b==j or not b:continue
			if not c:k=True;h=a["mobs"].get(b);c=(h[0]if h and h[0]else "")or a["names"].get(b,"")
			if c and a["names"].get(b)!=c:a["names"][b]=c;a["names_dirty"]=True
			f.append((b,c or("0x%08X"%b)))
		f.sort(key=lambda e:(e[1].startswith("0x"),e[1].lower()));a["friends"]=f;a["fserials"]=[n for n,p in f];a["friends_raw"]=None if k else g
		if a["names_dirty"]:K.append(aT)
	def bC():
		p=CL.party()
		if p is None:b=int(API.GetPartyLeader()or 0);p=(b,0,False,[int(c)for c in API.GetPartyMemberSerials()or()])if b else None
		a["party"]=p
	def aV(p):return bool(p)and bool(p[0]or p[3])
	def bD(full=True):
		b=time.time()
		if b<a["next_profile"]and not(full and a["prof_part"]):return
		a["next_profile"]=b+cj;p=HOST.me()
		if p is None:a["profile"]=None;a["prof_part"]=False;return
		try:
			c=str(p.Name or "")
			try:d=p.raw.NameAndProps(False)
			except Exception:d=""
			e=[i.strip()for i in str(d or "").replace("\r","").split("\n")if i.strip()]
			if not full:f=a["profile"];h=f[2:]if f else("",0,0,0,0,0,False,False);a["profile"]=(c,e)+tuple(h);a["prof_part"]=True;return
			g=(c,e,cF(p.Notoriety),int(p.Gold or 0),int(p.Followers or 0),int(p.FollowersMax or 0),int(p.Weight or 0),int(p.WeightMax or 0),bool(p.InWarMode),bool(p.IsHidden))
		except Exception:g=None
		a["profile"]=g;a["prof_part"]=False
	def cI():
		i=E();d,e,f,g,h={},[],set(),{},{}
		for m in a7():
			try:
				s=int(m.Serial)
				if not s or s==i:continue
				f.add(s)
				if not(m.IsHuman or m.IsGargoyle):continue
				n=m.Notoriety;c=int(n)if n is not None else-1
				if c==7:continue
				b=str(m.Name or "")
				if b:d[b.lower()]=s
				if c==2:e.append((s,b))
				g[s]=(b,int(m.Distance))
				if Kit.cblind:h[s]=c
			except Exception:continue
		a["view"],a["allies"],a["view_serials"],a["kept"],a["notos"]=d,e,f,g,h
	def cJ(c):
		b=a["view_serials"]
		if b is None and len(c)>cK:
			try:b={int(e.Serial)for e in a7()}
			except Exception:b=None
		if b is not None:return b.intersection(c)
		return{g for g in c if g and a6(g)is not None}
	cK=10
	def bE(fn):
		a=[None,None]
		def b(raw):
			for e in a:
				if e is not None and(e[0]is raw or e[0]==raw):return e[1]
			b=fn(raw);a[1]=a[0];a[0]=(raw,b);return b
		return b
	@bE
	def aW(raw):return Kit.gump_cells(raw,bq)
	@bE
	def F(raw):
		c=aW(raw)[0]
		if not c:return
		a=[e["text"].lower()for e in c];b=[g["cliloc"]for g in c]
		if any(h in aQ for h in b)or aw.lower()in a:
			if(1062955 in b and 1062956 in b)or("rank"in a and("last on"in a or "name"in a)):return "roster"
			return "guild"
		d="\x00".join(a)
		if any(i in cs for i in b)or any(m in d for m in ct):return "noguild"
	def cL(raw):return any(b in raw for b in cu)or "roster"in raw.lower()
	def cM(cells,d=6):
		a=[]
		for b in sorted(cells,key=lambda c:(c["y"],c["x"])):
			if a and abs(b["y"]-a[-1][0])<=d:a[-1][1].append(b)
			else:a.append([b["y"],[b]])
		return[sorted(e,key=lambda c:c["x"])for g,e in a]
	def bF(raw):
		a,f=aW(raw);a=[g for g in a if g["cliloc"]not in aQ]
		def e(cliloc):
			e=bq[cliloc].lower();b=next((g for g in a if g["cliloc"]==cliloc or g["text"].lower()==e),None)
			if b is None:return ""
			d=[h for h in a if abs(h["y"]-b["y"])<=6 and h["x"]>b["x"]];return min(d,key=lambda c:c["x"])["text"]if d else ""
		b={"name":e(1062954),"alliance":e(1063025),"faction":e(1063084),"charter":"","website":""};d=sorted([i for i in a if i["w"]>=300 and i["bg"]],key=lambda c:c["y"])
		if d:b["charter"]=d[0]["text"]
		if len(d)>1:b["website"]=d[1]["text"]
		for k in("charter","website"):
			if "not yet set"in b[k].lower():b[k]=""
		return b
	def cN(raw):
		g,r=aW(raw);g=[ch for ch in g if ch["cliloc"]not in aQ and ch["text"].lower()not in cv];m=cM(g);e=None
		for c in m:
			h=[dA["text"].lower()for dA in c]
			if len(c)>=3 and("name"in h or "rank"in h or "last on"in h or any(dB["cliloc"]in(1062955,1062956,1062952,1062953)for dB in c)):e=c;break
		if e is None:return[],False
		s=[dC["x"]for dC in e];t=[dD["text"].lower()for dD in e];b={}
		for u,v in(("name",("name",)),("rank",("rank",)),("laston",("last on","online")),("title",("title",))):
			for i,w in enumerate(t):
				if any(dE in w for dE in v)and i not in b.values():b[u]=i;break
		if "name"not in b:b["name"]=0
		n=[];x=e[0]["y"]
		for c in m:
			if c[0]["y"]<=x+10:continue
			d={}
			for o in c:
				j,k=-1,1e9
				for i,y in enumerate(s):
					p=abs(o["x"]-y)
					if p<k:j,k=i,p
				if k<=30 and j not in d:d[j]=o
			if len(d)<2 or b["name"]not in d:continue
			q=d[b["name"]];a=q["text"]
			if a.endswith(" *"):a=a[:-2]
			a=a.strip()
			if a.endswith(" VvV"):a=a[:-4].strip()
			if not a:continue
			l=q["raw"].lower();f=[d[b[dF]]["text"]if dF in b and b[dF]in d else ""for dF in("rank","laston","title")];z=f[1].lower()=="online"or "#000066"in l or "#006600"in l;n.append({"name":a,"rank":f[0],"laston":f[1],"title":f[2],"online":z,"me":"#006600"in l})
		A=any(dG[2]==bn for dG in r);return n,A
	def cO():
		a=int(API.HasGump()or 0)
		if not a:return 0,""
		try:return a,str(API.GetGump(a).PacketGumpText or "")
		except Exception:return a,""
	def aC():return safe(lambda:Kit.on_client(cO))or(0,"")
	def bG(raw):return cL(raw)and F(raw)in("guild","roster")
	def aD(gid=0):
		a=HOST.services.get("gump.expect")
		if a is not None and gid:a(gid,bm+1.)
		if d["ghide"]and gid:API.ConfigNextGump(serial=gid,isVisible=False)
	def cP():API.ConfigNextGump()
	def cQ(c):
		a,b=aC()
		if not a or a==c:return "the guild window didn't come"
		d=" ".join(b.split())[:cn]if b else "(empty layout)";f("gump 0x%08X came instead of the guild window (left open); it begins: %s."%(a,d));return "the guild window didn't come (another gump did)"
	def X(check):
		d=time.time()+bm
		while time.time()<d and not a["shutting"]:
			c,b=aC();r=c and b and check(b)
			if r:return c,b,r
			if not HOST.idle(.15):break
		return 0,"",None
	def af(gid,label,button):
		a=safe(lambda:API.GetGump(gid))
		if a is not None and CL.press_labelled(Kit.client_control(a)or a,label):return True
		return bool(button)and bool(API.ReplyGump(button,gid))
	def cR():
		a["guild_busy"]=True;a["guild_pages"]=0;c=a["guild"]or P();b=c
		try:b=cS(c)
		except Exception as i:b=P();b["note"]="couldn't read the guild window (%s)"%i
		finally:
			with Kit.quiet:cP()
			g=a.get("ghid",0);a["ghid"]=0
			if g:
				with Kit.quiet:API.CloseGump(g)
			e=not b["ok"]
			if e:j,b=b["note"],dict(c);b["note"]=j;a["guild_fails"]=min(a["guild_fails"]+1,10);a["guild_next"]=time.time()+min(cr,bp*(2**(a["guild_fails"]-1)))
			else:a["guild_fails"]=0;a["guild_said"]=""
			a["guild"]=b;a["guild_busy"]=False;a["guild_dirty"]=True
			if b["ok"]and not e:cB()
		if b["note"]:
			if not e:f("%s."%b["note"])
			elif b["note"]!=a["guild_said"]:
				a["guild_said"]=b["note"];h=""
				if d["gevery"]and d["tab"]=="guild":h=" (retry in %d min)"%max(1,int((a["guild_next"]-time.time())/60+.5))
				f("%s%s."%(b["note"],h),l)
	def cS(o):
		c=P();c["members"]=list(o["members"]);f=a["gids"]
		def g(note,a=False):
			c["note"]=note
			if a:c.update({"ok":True,"at":time.time()})
			return c
		p,j=aC();q=F(j)if j else None;d=q in("guild","roster")
		if not d:
			v,w=CL.find_server_gump(bG)
			if v:p,j,q,d=v,w,F(w),True
		if d:b,e,h=p,j,q
		else:
			aD(f.get("info",0)if o.get("in_guild",True)else 0)
			if not CL.game_action("OpenGuildGump"):return g("couldn't ask for the guild window (%s)"%CL.error)
			b,e,h=X(F)
			if not b:return g(cQ(p))
			a["ghid"]=b
		if h=="noguild":API.CloseGump(b);a["ghid"]=0;c.update({"ok":True,"in_guild":False,"members":[],"at":time.time()});return c
		if h=="roster":
			f["roster"]=b
			if not d:aD(f.get("info",0))
			af(b,ac,aO);b,e,h=X(lambda r:F(r)=="guild"and "guild")
			if not b:return g("the My Guild page didn't come")
			if not d:a["ghid"]=b
		s=bF(e)
		if d and not s.get("name"):
			t=e;af(b,ac,aO);b,e,h=X(lambda a:F(a)=="guild"and a!=t and "guild")
			if not b:return g("the My Guild page didn't come")
			s=bF(e)
		f["info"]=b;c.update(s)
		if not d:aD(f.get("roster",0))
		if not af(b,aw,co):return g("couldn't open the Guild Roster page",True)
		b,e,h=X(lambda r:F(r)=="roster"and "roster")
		if not b:return g("the Guild Roster page didn't come",True)
		if not d:a["ghid"]=b
		f["roster"]=b;l,n,i,u=[],{},0,False
		while not a["shutting"]:
			z,A=cN(e);i+=1;a["guild_pages"]=i
			for m in z:
				k=m["name"].lower()
				if k not in n:n[k]=True;l.append(m)
			if not A or i>=cp:u=True;break
			if not d:aD(b)
			if not API.ReplyGump(bn,b):break
			t=e;x,B,C=X(lambda a:F(a)=="roster"and a!=t and "ok")
			if not x:break
			b,e=x,B
			if not d:a["ghid"]=b
		if not u or not l:
			for m in o["members"]:
				k=m["name"].lower()
				if k not in n:n[k]=True;y=dict((ch,dA)for ch,dA in m.items()if not ch.startswith("_"));y["online"]=False;l.append(y)
			if not u and i:c["note"]="read %s only; rest as before"%aa(i,"roster page")
		c["members"]=l;c.update({"ok":True,"at":time.time()})
		if d:af(b,ac,aO)
		else:API.CloseGump(b);a["ghid"]=0
		return c
	def bH(tab):return cd if tab=="guild"else cc
	def cT(fw,fh,mode):
		b=(int(fw),int(fh))if(fw is not None and fh is not None)else None
		if b!=a.get("fit"):a["fit"]=b;o("redraw")()
		elif mode=="again"and b is not None:
			c=(b,d["tab"],a["minimized"],d["rows"],d["bars"]);e=time.time()
			if c!=a["again_for"]or not 0<=e-a.get("again_at",0.)<5.:a.update({"again_for":c,"again_at":e,"again_build":True});o("redraw")()
	def bI():return max(160,M+30+z(N.upper())+6+94+M)
	def cU():return(M+30+z(N.upper())+16+(0 if Kit.zone_up(at)else 84+Kit.DOCK_DX)+35+z("Settings")+M)
	def cV(iw):
		c,a,b=[],10,0
		for f,d in bj:
			e=35+z(d)
			if a>10 and a+e>iw-4:a,b=10,b+1
			c.append((f,d,a,b));a+=e+14
		return c,b+1
	def aX(tab):a,b={"friends":(1,1),"party":(2,3),"guild":(6,2)}.get(tab,(7,2));return a,b,d["rows"]if a<7 else 0
	def bJ(tab):a,c,b=aX(tab);d=(8+a*22+(8 if a else 0)+c*30+b*aB()+(8 if b else 0)+4);return M+30+U+30+U+d+M
	def bK():return(bI(),max(bJ(b)-max(0,aX(b)[2]-1)*aB()for b,c in bj)+30)
	def aY():
		c=d["tab"];g,m,n=Q.begin(bH(c),bJ(c));w,h=Q.w,Q.h;p=[];j["info_tips"],j["info_in"]={},{}
		if a["again_build"]:a["again_build"]=False
		else:a["again_for"]=None
		if not a["minimized"]:
			b=a.get("fit")
			if b is not None and b[1]<bK()[1]:b=None
			if b is not None:w,h=max(bI(),b[0]),b[1]
			e=w-2*M;n["iw"]=e;Q.frame(g,w,h,settings=w>=cU());i=M+30+U;r,k=cV(e);ap(g,M,i,e,30*k)
			for f,s,t,u in r:H(g,m,"tab_"+f,G,M+t,i+4+30*u,s,bk[f],hue=L if f==c else C,on_click=o(("tab",f)))
			l=i+30*k+U
			if b is None:h+=30*(k-1)
			q=h-l-M;ap(g,M,l,e,q);cW(g,m,n,p,c,M,l,e,q,b is not None)
		Q.end(g,{"rows":p,"tab":c,"info":{}},w,h);a["rebuild"]=False;a4()
	Q=Kit.Window(at,N,a,j,aY,b9,ca,mini=(bf,ce),icon=cb,cleanup=ax,docked_min=True)
	def cW(g,store,c,rows,tab,x,y,w,h,fit=False):
		b,m,j=aX(tab);aF[0]=x+w-6;l=aB()
		def f(a):return max(1,(y+h-12-a)//l)if fit else j
		e=max(1,min(b,(h-16-m*30-(l+12 if j else 4))//22))if fit and b else b;c["info"]=[D(g,"",x+10,y+8+22*min(p,e-1),k)for p in range(b)]
		for n in c["info"][e:]:n.IsVisible=False
		a=y+8+22*e+(8 if e else 0)
		if tab=="friends":i=[("add",Z,["Add friend...",None],"Target someone to add to TazUO's friends list"),("add_last",an,["Add last target",None],"Add your last target to TazUO's friends list")];a=bN(g,store,c,x,y,a,w,i,None);a1(g,store,c,rows,f(a),x,a,w,aZ%"set as last target (or answer a target cursor)",True,rm_tip="Remove from TazUO's friends list")
		elif tab=="party":a+=30*ag(g,store,c,x,a,x+w-6,[("invite",Z,["Invite...",None],"Target someone to invite to your party"),("leave",Y,["Leave",None],"Leave the party"),("loot",an,["Loot",None],"Allow or forbid party looting of your corpse (the line above shows which)"),("pwin",G,["Party window",None],"Open the client's party window")]);aF[0]=x+w-6-aE-6;c["accept"]=a_(g,store,x+10,a,"accept",an,"Accept","Join the party. Alt+click: auto-follow the inviter (again to stop)",on_click=bO("accept"));c["decline"]=a_(g,store,c["accept"][1],a,"decline",Y,"Decline","Turn the invitation down. Alt+click: auto-follow the inviter (again to stop)",on_click=bO("decline"));aF[0]=x+w-6;a0(g,store,c,x+w,a);a+=30;bP(g,store,c,x,a,w,[("psend","Send","Say it in party chat")],"Message for party chat");a+=30;a1(g,store,c,rows,f(a),x,a,w,aZ%"set as last target (or answer a target cursor)",True,rm_tip="Remove from the party (leader only)")
		elif tab=="guild":i=[("grefresh",Z,["Refresh",None],"Read the guild window again (info and roster); "+("it opens hidden"if d["ghide"]else "it shows while read; Social settings can hide it")),("gwin",G,["Guild window",None],"Open the server's guild menu"),("diplo",G,["Diplomacy",None],"Open the guild window's Diplomacy page"),("gsort",G,["long","short",None],None)];a=bN(g,store,c,x,y,a,w,i,[3,2,1,0,3]);bP(g,store,c,x,a,w,[("gsend","Guild","Say it in guild chat"),("asend","Alliance","Say it in alliance chat")],"Message for guild or alliance chat");a+=30;a1(g,store,c,rows,f(a),x,a,w,aZ%"set as last target when in view",False,before=[("rank",cl)],after=[("title",0)])
		else:a+=30*ag(g,store,c,x,a,x+w-6,[("edit",G,["Edit profile",None],"Open your profile (the server's scroll; closing saves)"),("paperdoll",G,["Paperdoll",None],"Open the client's paperdoll"),("status",G,["Status",None],"Open the client's status window")]);ag(g,store,c,x,a,x+w-6,[("ignore",G,["Ignore list",None],"Open TazUO's ignore list (speech you hide)"),("war",Z,["War / peace",None],"Switch war mode and peace (the last line above shows which)")])
	aZ="Click: %s. Shift+click: write a note. Alt+click: auto-follow (again to stop)";aE=100
	def bL(c):
		a="Next roster order: online (in view first), last on, rank or name"
		if c.get("gsort_bare"):e=ad[T.index(d["gsort"])];a="Roster order: %s. %s"%(e[2].lower(),a)
		return a
	def cX(key,cap):
		if key=="gsort":
			if cap=="long":return max(z(b[1])for b in ad)
			return max(z(c[2])for c in ad)
		return z(cap)
	def bM(items,x,right,order):
		b=[0]*len(items)
		if order is None:order=list(range(len(items)-1,-1,-1))
		h=[None]+list(order)
		for c in h:
			if c is not None:b[c]=min(b[c]+1,len(items[c][2])-1)
			a,d=x+10,x+10
			for i,e in enumerate(items):
				f=e[2][b[i]]
				if f is None:d,a=a+30,a+30
				else:g=cX(e[0],f);d,a=a+35+g,a+35+g+12
			if d<=right:return list(b)
		return
	def ag(g,store,c,x,y,right,items,order=None,plan=None):
		h=plan or bM(items,x,right,order);j=h is None
		if j:h=[len(p[2])-1 for p in items]
		b,e=x+10,0
		for l,(d,m,i,f)in enumerate(items):
			a=i[h[l]]
			if d=="gsort":c["gsort_long"]=a=="long";c["gsort_bare"]=a is None;f=bL(c);a=None if a is None else bT(c)
			elif a is None and i[0]:f=a9(i[0],f)
			k=30 if a is None else 35+z(a)
			if j and b>x+10 and b+k>right:b,e=x+10,e+1
			n=H(g,store,d,m,b,y+30*e,a,f,on_click=o(d));b+=30 if a is None else k+12
			if d=="gsort":c["gsort"]=n if a is not None else None;c["gsort_btn"]=store[0].get(d)
		return e+1
	def bN(g,store,c,x,y,a,w,items,order):
		b=bM(items,x,x+w-6-aE-6,order);e=b is not None and all(h[2][i]is not None and(i==0 or h[0]=="gsort")for h,i in zip(items,b))
		if e:d=ag(g,store,c,x,a,x+w-6-aE-6,items,order,b);a0(g,store,c,x+w,a)
		else:d=ag(g,store,c,x,a,x+w-6,items,order);a0(g,store,c,x+w,y+8-6);c["info_cut"]=aE+6
		return a+30*d
	aF=[100000]
	def a_(g,store,x,y,key,art,cap,tip,on_click=None):a=x+35+z(cap)>aF[0];b=H(g,store,key,art,x,y,None if a else cap,a9(cap,tip)if a else tip,on_click=on_click or o(key));return store[0].get(key),(x+30 if a else x+35+z(cap)+12),b
	def bO(key):
		def b(*c):
			p=a["party"];b=p[1]if p else 0
			if b and am():o(("follow",b))()
			else:o(key)()
		return b
	def a0(g,store,c,right,y):c["pg"]=D(g,"",right-100,y+6,k);H(g,store,"pg_up",Kit.ART_RESTORE,right-56,y+4,None,"Previous page",on_click=o(("page",-1)));H(g,store,"pg_dn",Kit.ART_MIN,right-34,y+4,None,"Next page",on_click=o(("page",1)))
	def bP(g,store,c,x,y,w,buttons,f):
		h=sum(35+z(n)+12 for m,n,m in buttons);b=w-20-h-8
		if b<cm:b=max(40,w-20-30*len(buttons)-8)
		c["msg"]=ab(aK(g,a["msg"].get(d["tab"],""),x+10,y+3,b,numbers=False),f);e=x+10+b+12
		for i,j,k in buttons:e=a_(g,store,e,y,i,Z,j,k)[1]
	def a1(g,store,c,rows,n,x,y,w,tip,p,before=None,after=None,rm_tip="Remove"):
		b,q=ba(Kit.LINE_RED);b,q=b or 109,q or 9;B,v=ba(Kit.LINE_BLUE);s=x+w-4-(40 if p else 0);before,after=list(before or[]),list(after or[]);t=[];f=d["bars"]
		def z():return sum(ch+8 for dA,ch in before)+sum((dB or 40)+8 for dC,dB in after)
		while s-(x+10)<z()+8+40+8+(30+8 if f else 0)+44 and(after or before or f):
			if after:t.append(after.pop()[0])
			elif before:t.append(before.pop()[0])
			else:f=False
		u,l=aN,av;m=s-(x+10)-z()-8;C=aN+8+(b+8 if f else 0)+av
		if m<C:
			l=max(44,min(av,int(m*.24)))
			if f:b=max(30,min(b,int(m*.3)))
			u=max(40,m-l-8-(b+8 if f else 0))
		c["bar_w"],c["name_w"],c["status_w"]=b,u,l;A=aB()
		for o in range(n):
			e=y+o*A;r={"serial":0,"prev":(0,0.),"parts":[],"name":None,"status":None,"fill":None,"fill_w":-1,"x":None,"red":None,"extra":{},"who":"","prev_who":("",0.),"tip0":tip,"tip":tip};a=x+10;r["name"]=D(g,"",a,e+3);r["parts"].append([r["name"],True]);a+=u+8
			for i in t:r["extra"][i]=(None,0)
			for i,h in before:j=D(g,"",a,e+3,k);r["extra"][i]=(j,h);r["parts"].append([j,True]);a+=h+8
			if f:
				r["red"]=[a8(g,Kit.LINE_RED,a,e+7,b,q),True];r["parts"].append(r["red"])
				if B and v:r["fill"]=a8(g,Kit.LINE_BLUE,a,e+7,1,v);r["fill"].SetWidth(0);r["parts"].append([r["fill"],True])
				a+=b+8
			r["status"]=D(g,"",a,e+3,k);r["parts"].append([r["status"],True]);a+=l+8
			for i,h in after:h=h or max(40,s-a);j=D(g,"",a,e+3,k);r["extra"][i]=(j,h);r["parts"].append([j,True]);a+=h+8
			r["catch"]=Kit.catcher(g,x+4,e,w-8-(40 if p else 0),A,cZ(rows,o),tip);r["parts"].append([r["catch"],True])
			if p:r["x"]=H(g,store,"rm%d"%o,Y,x+w-42,e+1,None,rm_tip+". Alt+click: auto-follow (again to stop)",on_click=cY(rows,o));r["parts"].append([r["x"],True])
			rows.append(r)
	def a2(r,cur,prev,now):p,a=r[prev];return p if p and now-a<.15 else r[cur]
	def cY(rows,i):
		def a(*b):
			a=a2(rows[i],"serial","prev",time.time())
			if a and am():o(("follow",a))()
			elif a:o(("rm",a))()
		return a
	def cZ(rows,i):
		def a(*d):
			r,c=rows[i],time.time();b,a=a2(r,"serial","prev",c),a2(r,"who","prev_who",c)
			if not b:
				if a and not am()and by():o(("note",a))()
				elif a:o(("noview",a))()
				return
			if am():o(("follow",b))()
			elif a and by():o(("note",a))()
			else:o(("click",b))()
		return a
	c_={}
	def aG(r,key,prev,v):
		if r[key]!=v:r[prev],r[key]=(r[key],time.time()),v
	def bQ(r,serial,name,status,hue,c,extra=None,name_hue=None,bar=True,show_x=True,me=False):
		d=extra or c_;g=aA(name,serial,me);a=(serial,name,status,hue,c,d.get("rank"),d.get("title"),name_hue,bar,show_x,A["ver"],g)
		if a==r.get("last"):return
		r["last"]=a;aG(r,"serial","prev",serial);aG(r,"who","prev_who",name)
		if name_hue is None:name_hue=C if c is not None else k
		h=j["c"];q(r["name"],u(g,h.get("name_w",aN)),name_hue);q(r["status"],u(status,h.get("status_w",av)),hue);i=[]
		for a,(l,n)in r["extra"].items():
			e=str(d.get(a,"")or "");f=""
			if l is not None:f=u(e,n);q(l,f,k)
			if f!=e:i.append("%s: %s"%(a.capitalize(),e))
		b="\n".join([r["tip0"]]+i)
		if B:
			m=B.get(name.lower())
			if m is not None:b=b+"\nNote: "+m[1]
		if b!=r["tip"]and r.get("catch")is not None:r["tip"]=b;ab(r["catch"],b)
		w=int(j["c"].get("bar_w",109)*max(0.,min(1.,c or 0.)))
		if r["fill"]is not None and w!=r["fill_w"]:r["fill_w"]=w;Kit.ui_w(r["fill"],max(1,w))
		o=r["parts"][-1]if r["x"]is not None else None
		for p in r["parts"]:
			if r["fill"]is not None and p[0]is r["fill"]:ae(p,bar and w>0)
			elif r["red"]is not None and p is r["red"]:ae(p,bar)
			elif p is o:ae(p,show_x)
			else:ae(p,True)
	def bR(r):
		r["last"]=None;aG(r,"serial","prev",0);aG(r,"who","prev_who","")
		for p in r["parts"]:ae(p,False)
	def bS(serial):
		d=bB(serial)
		if d is None:return "away",k,None
		h,c,b,e,f,i=d
		if f:return "dead",l,0.
		a=c/float(b)if b>0 else None;g=(S if a is None or a>.5 else(L if a>.25 else l));return(aa(e,"tile")),g,a
	def ah(items):n=max(1,len(j["rows"]));b=max(1,(len(items)+n-1)//n);p=max(0,min(b-1,a["page"].get(d["tab"],0)));a["page"][d["tab"]]=p;return items[p*n:(p+1)*n],("%d/%d"%(p+1,b))if b>1 else ""
	c0=dict((dJ,dH)for dH,dI in enumerate(bs)for dJ in dI)
	def c1(m):
		v=m.get("_lo")
		if v is None:
			v=-1;e=cz.search(m["laston"]or "")
			if e is not None:
				g,h,b,i=e.group(1),e.group(2),int(e.group(3)),e.group(4);a,f=int(g),int(i)
				if len(g)==4 or a>31:y,c,d=a,b,f
				else:
					y=f+(2000 if f<100 else 0)
					if a>12:d,c=a,b
					elif b>12:c,d=a,b
					elif h==".":d,c=a,b
					else:c,d=a,b
				if 1<=c<=12 and 1<=d<=31:v=y*10000+c*100+d
			m["_lo"]=v
		return v
	def bT(c):e=ad[T.index(d["gsort"])];return e[1]if c.get("gsort_long")else e[2]
	c2={"src":None,"how":None,"order":[],"names":{},"online":0}
	def a3(m):
		k=m.get("_k")
		if k is None:k=m["_k"]=m["name"].lower()
		return k
	def bU(e):return e[0]
	def c3(how):
		a=len(bs)
		if how=="online":return lambda m:((0 if m["online"]else 1),m["_k"])
		if how=="name":return lambda m:m["_k"]
		if how=="rank":return lambda m:(c0.get((m["rank"]or "").strip().lower(),a),m["_k"])
		return lambda m:((0 if m["online"]else 1),-c1(m),m["_k"])
	def bV(gd,how):
		a=gd["members"];b=c2
		if b["src"]is not a or b["how"]!=how:
			c,d={},0
			for m in a:
				c[a3(m)]=True
				if m["online"]:d+=1
			b.update({"src":a,"how":how,"order":sorted(a,key=c3(how)),"names":c,"online":d})
		return b
	def c4(me):
		p=a["guild"]or P();h,i=a["view"],a["mobs"];q=d["gsort"];j=bV(p,q);c=[];n=0
		if q=="online":
			e=[]
			for m in p["members"]:
				b=h.get(m["_k"],0)
				if b:
					f=i.get(b)
					if f:e.append(((f[3],(0 if m["online"]else 1),m["_k"]),b,m))
			if e:
				e.sort(key=bU);n=len(e)
				for g in e:c.append((g[1],g[2]))
				for m in j["order"]:
					b=h.get(m["_k"],0)
					if not(b and i.get(b)):c.append((b,m))
			else:
				for m in j["order"]:c.append((h.get(m["_k"],0),m))
		else:
			for m in j["order"]:
				b=h.get(m["_k"],0)
				if b and b in i:n+=1
				c.append((b,m))
		r=j["names"];k=[]
		for b,o in a["allies"]:
			l=o.lower()
			if l in r or l==me or not o:continue
			f=i.get(b);k.append(((f[3]if f else 999,l),b,{"name":o,"rank":"ally","laston":"","title":"ally in view","online":True,"me":False,"_k":l,"ally":True}))
		if k:
			k.sort(key=bU)
			for g in k:c.append((g[1],g[2]))
		return c,n
	def a4():
		K,d=j["g"],j["c"]
		if K is None or(a["minimized"]and a["docked"])or("status"in d)!=bool(a["minimized"]):return
		if a["minimized"]:
			M,h=len(a["friends"]),len(a["inview"]);b=a["party"];z="%s: %s, %d in view"%(N,aa(M,"friend"),h)
			if aV(b):z+=", party of %d"%(len(b[3])+1)
			q(d["status"],u(z,bf-18-66));return
		i=j["tab"];c=d.get("info",[]);e=d.get("iw",bH(i)-2*ao)-20;A=e-d.get("info_cut",0)
		if i=="friends":
			f=a["friends"];p,r=ah(f);h=len(a["inview"]);B=(len(f),h,A)
			if j["info"].get("friends")!=B:j["info"]["friends"]=B;q(c[0],u("%s, %d in view"%(aa(len(f),"friend"),h)if f else "No friends yet: Add friend... targets one",A))
			bW(d,[(ch,ai(ch,dA))for ch,dA in p],r)
		elif i=="party":
			b=a["party"];m=E()
			if not aV(b):q(c[0],u("Not in a party: Invite... asks someone to join",e),k);q(c[1],"",k);f=[]
			else:n,g,O,s=b;P="you"if n==m else aA(ai(n),n);q(c[0],u(("Party of %d, led by %s"%(len(s)+1,P))if n else "Party of %d"%(len(s)+1),e),C);q(c[1],u("Party may loot your corpse: %s"%("yes"if O else "no"),e),k);f=[dB for dB in s if dB!=m]
			g=b[1]if b else 0;o=bool(g)and not(b and b[0])
			for t in("accept","decline"):
				v=d.get(t)
				if v is not None and j["info"].get("vis_"+t)!=o:
					j["info"]["vis_"+t]=o
					for Q in(v[0],v[2]):Kit.set(Q,"IsVisible",o)
			if o:w=a["mobs"].get(g);q(c[0],u("Party invite from %s: Accept or Decline"%(aA(w[0],g)if w and w[0]else "0x%08X"%g),e),L)
			p,r=ah(f);bW(d,[(dC,ai(dC))for dC in p],r,bool(b)and b[0]==m and bool(m))
		elif i=="guild":c5(c,d,e)
		else:
			if a["prof_part"]:bD(True)
			x=a["profile"]
			if not x:
				j["info"].pop("prof",None)
				for y in c:q(y,"")
				q(c[0],u("No character logged in",e),k);return
			D=(x,e)
			if j["info"].get("prof")==D:return
			j["info"]["prof"]=D;F,R,G,T,U,V,W,X,H,Y=x;J=[dD for dD in R if dD!=F];Z=[(I("me",F),L),(I("guild"," / ".join(J))if J else "No titles read yet: hover yourself once",k),("Notoriety: %s"%(G or "unknown"),Kit.cb_hue(G.lower(),C)),("Gold: %d"%T,C),("Followers: %d / %d"%(U,V),C),("Weight: %d / %d"%(W,X),C),("%s%s"%("War mode"if H else "Peace",", hidden"if Y else ""),l if H else S)]
			for y,(ab,ac)in zip(c,Z):q(y,u(ab,e),ac)
	def ai(s,other=None):d=a["mobs"].get(s);return(d[0]if d and d[0]else "")or a["names"].get(s,"")or other or "0x%08X"%s
	def bW(c,shown,pg,show_x=True):
		q(c["pg"],pg);a=j["rows"]
		for r,(b,d)in zip(a,shown):e,f,g=bS(b);bQ(r,b,d,e,f,g,show_x=show_x)
		for r in a[len(shown):]:bR(r)
	def aj(lbl,full,width,hue):
		a=j["info_in"];k=(full,width,hue)
		if a.get(lbl)==k:return
		d=u(full,width);q(lbl,d,hue);b=full if d!=full else "";c=j["info_tips"]
		if len(c)>64:c.clear()
		if c.get(lbl)!=b:c[lbl]=b;lbl.SetAcceptMouseInput(bool(b));lbl.SetTooltip(b)
		if len(a)>64:a.clear()
		a[lbl]=k
	def a5(lbl,text,hue=None):q(lbl,text,hue);j["info_in"].pop(lbl,None)
	def c5(info,c,tw):
		n=tw-c.get("info_cut",0);b=a["guild"]or P();o=a["profile"];p=[ch for ch in o[1][1:]if ch and ch!=o[0]]if o else[]
		if not b["ok"]:a5(info[0],u("Guild window not read yet",n),k)
		elif not b["in_guild"]:a5(info[0],u("Not in a guild",n),k)
		else:B=I("guild",b["name"])if b["name"]else "Guild name not shown";aj(info[0],B,n,L)
		aj(info[1],("You: "+I("guild"," / ".join(p)))if p else "Your guild line isn't read yet: hover yourself once",tw,C if p else k)
		if b["ok"]and b["in_guild"]:
			aj(info[2],"Alliance: %s     Faction: %s"%(I("guild",b["alliance"])if b["alliance"]else "none",b["faction"]or "none"),tw,C)
			for D,E,x in((info[3],"Charter","charter"),(info[4],"Website","website")):aj(D,"%s: %s"%(E,I("guild",b[x])if b[x]else "not set"),tw,k)
		else:
			for F in info[2:5]:a5(F,"")
		r=str(cG()or "").lower();G,H=c4(r);J=bV(b,d["gsort"])["online"]
		if a["guild_busy"]:y=a["guild_pages"];f="Reading the guild window"+(" (page %d)"%y if y else "");e=L
		elif not b["ok"]:h=b["note"];f=((h[:1].upper()+h[1:])if h else("Click Refresh to read the guild window"if not d["gevery"]else "Read when this tab shows"));e=l if h else k
		elif not b["in_guild"]:f,e="Read %s; allies in view below"%bz(b["at"]),k
		else:
			K=len(b["members"]);f="%s, %d online, %d in view; read %s"%(aa(K,"member"),J,H,bz(b["at"]))
			if b["note"]:f+="  (%s)"%b["note"]
			e=k
		aj(info[5],f,tw,e);z,M=ah(G);q(c["pg"],M)
		for s,(i,m)in zip(j["rows"],z):
			g=bB(i)if i else None
			if g is not None:t,e,v=bS(i)
			elif m["online"]:t,e,v="Online",S,None
			else:t,e,v=(m["laston"]or "offline"),k,None
			A=bool(m["me"]or(r and a3(m)==r))
			if A:w=L
			elif g is not None or m["online"]:w=S if g is None else C
			else:w=k
			N=I("guild",m["title"])if m["title"]and not m.get("ally")else m["title"];bQ(s,i if g is not None else 0,m["name"],t,e,v,extra={"rank":m["rank"],"title":N},name_hue=w,bar=g is not None,me=A)
		for s in j["rows"][len(z):]:bR(s)
	bX=104;c6=ao+30+U+bX+ao
	def bY(name):
		ak.close();w,h=cy,c6;i,l=240,180
		if Kit.is_open(j["g"]):i,l=j["g"].GetX()+40,j["g"].GetY()+60
		g,c,m=ak.begin(w,h,(i,l));Kit.add_window_frame(g,w,h);ap(g,M,M,w-2*M,30);D(g,"PLAYER NOTE",M+30,M+7,L);H(g,c,"close",Y,w-M-54,M+4,None,"Close without saving",on_click=o("note_close"));d=w-2*M;a=M+30+U;ap(g,M,a,d,bX);b=M+12;e=b+max(z("Player:"),z("Note:"))+10;D(g,"Player:",b,a+13);n=aA(name)if name else name;m["name"]=ab(aK(g,n,e,a+10,200,numbers=False),"Player name as shown over their head (any case)");D(g,"Note:",b,a+43);m["text"]=ab(aK(g,B.get(name.lower(),("",""))[1],e,a+40,M+d-12-e,numbers=False),"Your note (up to %d letters); saving it empty deletes it"%br);f=a+72;H(g,c,"save",an,b,f,"Save","Save the note for every character of this account",on_click=o("note_save"));H(g,c,"delete",Y,b+35+z("Save")+16,f,"Delete","Delete this note",on_click=o("note_delete"));p="Kept per account";D(g,p,M+d-12-z(p),f+3,k);ak.end(g,{"name":name,"shown":n})
	ak=Kit.Window(at,N,None,W,bY,cx,cleanup=ax,lock=False,owner=False,clear={"c":{},"store":({},{})})
	def c7():
		c=W["c"]
		try:a=str(c["name"].Text or "")
		except Exception:a=W["name"]
		if a and a==W.get("shown"):a=W["name"]
		try:b=str(c["text"].Text or "")
		except Exception:b=""
		return a,b
	def aH():a=j["c"].get("msg");return ""if a is None else str(a.Text or "").strip()
	def c8():
		b=j["c"].get("msg")
		if b is not None:b.SetText("")
		a["msg"].pop(d["tab"],None)
	bZ={"psend":"PartyMsg","gsend":"GuildMsg","asend":"AllyMsg"}
	def c9(fn,txt):
		if not txt:f("type something first.");return
		getattr(API,fn)(txt);c8()
	def b_(serial):
		serial=int(serial or 0)
		if not serial:f("nothing targeted.");return
		if serial==E():f("that's you.");return
		m=API.FindMobile(serial)
		if m is None:f("target a player or creature in view.",l);return
		b=str(m.Name or "");c=b or "0x%08X"%serial
		if serial in[int(e)for e in API.GetAllFriends()or()]or any(g==serial for g,h in a["friends"]):f("%s is already a friend."%c)
		elif API.AddFriend(serial):
			if b:a["names"][serial]=b;a["names_dirty"]=True
			f("%s added to friends."%c,S)
			if a["seen"]is not None:a["seen"]=a["seen"]|{serial}
		else:f("couldn't add %s to friends (the client refused)."%c,l)
		a["next_friends"]=0.
	def da(serial):
		b=a["names"].get(serial,"")or "0x%08X"%serial
		if API.RemoveFriend(serial):f("%s removed from friends."%b)
		else:f("couldn't remove %s from friends (the client refused)."%b,l)
		if a["seen"]:a["seen"].discard(serial)
		a["next_friends"]=0.
	def db(serial):
		if not serial:return
		if j["tab"]=="friends":da(serial)
		elif j["tab"]=="party":
			b=a["party"]
			if b and b[0]and b[0]==E():
				if not CL.game_action("RequestPartyRemoveMember",[al(serial)],False):f("couldn't remove them (%s)."%CL.error,l)
			else:f("only the leader can remove members.")
	def b0():
		with Kit.quiet:
			import System;b=Typing._get(CL.world,"Party")if CL.world is not None else None
			if b is not None:Tz.put(b,"Inviter",System.UInt32(0))
		p=a["party"]
		if p:a["party"]=(p[0],0,p[2],p[3])
	def al(serial):
		try:import System;return System.UInt32(int(serial))
		except Exception:return serial
	b1={"paperdoll":("OpenPaperdoll",True,True),"status":("OpenStatusBar",False,True),"gwin":("OpenGuildGump",False,True),"invite":("RequestPartyInviteByTarget",False,False),"edit":("RequestProfile",True,False),"ignore":None}
	def dc(what):
		e=b1[what]
		if e is None:a=CL.open_ignore_list()
		else:a=CL.game_action(e[0],[al(E())]if e[1]else(),e[2])
		if not a:f("couldn't open that (%s)."%(CL.error or "no client access"),l)
		return a
	def dd():
		a=CL.world
		if a is None:f("couldn't open the party window (no client access: %s)."%CL.error,l);return
		def b():import System;b=Typing._get(a,"Macros");c=b.GetType().Assembly;d,e,f=[c.GetType("ClassicUO."+h)for h in("Game.Managers.MacroObject","Common.Enums.MacroType","Common.Enums.MacroSubType")];g=System.Activator.CreateInstance(d,System.Array[object]([System.Enum.Parse(e,"Open",True),System.Enum.Parse(f,"PartyManifest",True)]));CL.call(b,"SetMacroToExecute",[g]);CL.call(b,"Update");return True
		if not CL.on_main(b):f("couldn't open the party window (%s)."%CL.error,l)
	def de():
		a,b=aC()
		if not(a and F(b)in("guild","roster")):a=CL.find_server_gump(bG)[0]
		if not a:
			if not CL.game_action("OpenGuildGump"):f("couldn't ask for the guild window (%s)."%CL.error,l);return
			a,c,e=X(lambda a:F(a)in("guild","roster")and "ok")
		if not a:f("the guild window didn't come (are you in a guild?).",l);return
		if not af(a,au,d["dbutton"]):f("no %s button found; press it in the guild window (or set its id in Social settings)."%au)
	def df(serial):
		if API.HasTarget("any")and not HOST.cursor_busy(at):
			if HOST.harm_ok(serial,"social.row",N):API.Target(serial)
			return
		API.SetLastTarget(al(serial));m=API.FindMobile(serial)
		if m is None:f("%s isn't in view."%(a["names"].get(serial,"")or "they"))
		else:f("%s is your last target."%(str(m.Name or "")or "that"))
	def b2():
		if a["guild_busy"]:return False
		a["guild_busy"]=True;a["guild_next"]=time.time()+bp;K.append(cR);return True
	def dg():
		b=a["inview"]
		if not(d["announce"]or d["left"])or a["seen"]is None:a["seen"]=b;return
		if d["announce"]:
			for s in b-a["seen"]:f("%s is in view."%ai(s,"a friend"),S)
		if d["left"]:
			for s in a["seen"]-b:f("%s left view."%ai(s,"a friend"))
		a["seen"]=b
	def b3(action):
		b=a["party"]
		if not aV(b):f("not in a party.")
		elif action=="leave":
			if not CL.game_action("RequestPartyRemoveMember",[al(E())],False):f("couldn't leave (%s)."%CL.error,l)
		elif CL.game_action("RequestPartyLootState",[not b[2]],False):f("party %s loot your corpse."%("may not"if b[2]else "may"))
		else:f("couldn't change looting (%s)."%CL.error,l)
	def dh(action):
		b=al(a["party"][1])
		if action=="accept":
			def e():
				if not CL.game_action("RequestPartyAccept",[b],False):return
				b0();return True
			if CL.on_main(e)is None:f("couldn't accept (%s)."%CL.error,l)
			return
		c=R("ClassicUO.Network.AsyncNetClient");d=R("ClassicUO.Network.NetClientExt")
		def g():CL.call(None,"Send_PartyDecline",[Typing._get(None,"Socket",c),b],d);b0();return True
		if c is None or d is None or CL.on_main(g)is None:f("couldn't decline (%s)."%CL.error,l)
	def di():
		i=T.index(d["gsort"])if d["gsort"]in T else 0;d["gsort"]=T[(i+1)%len(T)];ay();c=j["c"];b=c.get("gsort")
		if b is not None:q(b,bT(c))
		e=c.get("gsort_btn")
		if e is not None and c.get("gsort_bare"):ab(e,bL(c))
		a["page"]["guild"]=0;a["next_list"]=0.
	def dj():
		a["guild_said"]=""
		if b2():a4()
		else:f("already reading the guild window.")
	def dk(tab):
		if tab!=d["tab"]:a["msg"][d["tab"]]=aH();d["tab"]=tab;ay();a["rebuild"]=True
	def dl(step):a["page"][d["tab"]]=max(0,a["page"].get(d["tab"],0)+step);a["next_list"]=0.
	def dm(name):
		if str(name).startswith("0x"):f("name not known yet.")
		else:bY(name)
	def dn():f("target the friend to add.");HOST.pick_target(ck,lambda serial:o.add(("picked",int(serial or 0)),dup=True))
	def b4(action):
		if a["party"]and a["party"][1]:dh(action)
	def b5(keep):
		if W["g"]is None:return
		a,b=c7()
		if cE(a,b if keep else ""):ak.close()
	def do(wanted,now,a):
		if not a:bC()
	def dp(wanted,now,c):b,d=ah(a["friends"]);wanted.update(e for e,g in b)
	def dq(wanted,now,e):
		bC();b=a["party"]
		if not b:return
		c=E();d,f=ah([g for g in b[3]if g!=c]);wanted.update(d);wanted.add(b[0]);wanted.add(b[1])
	def dr(wanted,now,e):
		cI()
		for s,f in a["allies"]:wanted.add(s)
		b=a["guild"]or P();c=a["view"]
		for m in b["members"]:
			s=c.get(a3(m),0)
			if s:wanted.add(s)
		if(d["gevery"]and not a["guild_busy"]and now>=a["guild_next"]and now-b["at"]>=d["gevery"]*60):b2()
	b6={"mini":do,"friends":dp,"party":dq,"guild":dr};b7={"click":df,"rm":db,"follow":lambda serial:Follow.toggle(serial,N),"noview":lambda name:f("%s isn't in view."%name),"picked":lambda serial:serial and b_(serial),"tab":dk,"page":dl,"note":dm};b8={"pwin":dd,"note_close":ak.close,"gsort":di,"grefresh":dj,"leave":lambda:b3("leave"),"loot":lambda:b3("loot"),"add_last":lambda:b_(int(API.LastTargetSerial or 0)),"add":dn,"accept":lambda:b4("accept"),"decline":lambda:b4("decline"),"diplo":lambda:K.append(de),"war":lambda:API.SetWarMode(not API.Player.InWarMode),"note_save":lambda:b5(True),"note_delete":lambda:b5(False)};ds={"ldy":4,"fw":40,"ltip":True,"clamp":False}
	def dt(w):return(("WINDOW",(("note",u("Shift+click a row to note that player; %d saved for this account."%len(B),w-28)),("note",u("Action Bar cells can show this window (Client window, page 2).",w-28)),("check","bars","Show health bars","A bar for everyone in view; off, rows show name, status and distance"),("num","rows","Rows per page:","Rows on the Friends, Party and Guild tabs; the window grows to fit",None,bg,bh))),("FRIENDS  (journal lines)",(("check","announce","Say when a friend comes into view","One line when a friend comes into view (not those in view at start)"),("check","left","Say when a friend leaves view","One line when a friend in view is gone"))),("GUILD WINDOW  (for the Guild tab)",(("check","ghide","Read the guild window hidden","It opens invisible for the read; off, it shows for a few seconds",{"h":28}),("num","gevery","Read it again every:","Minutes between reads while the Guild tab shows (0-%d, 0 = only on Refresh)"%aP,"min",0,aP),("num","dbutton","Diplomacy button id:","Pressed when the Diplomacy caption isn't found; ServUO uses %d (0-%d, 0 = caption only)"%(aL,aM),None,0,aM)),{"pad":8}))
	def du(b,new):
		if(new["bars"],new["rows"])!=(b["bars"],b["rows"])or(new["ghide"]!=b["ghide"]and b["tab"]=="guild"):a["rebuild"]=True
		if(new["announce"]or new["left"])and not(b["announce"]or b["left"]):a["seen"]=None
	aI=Kit.Page(d,dt,ay,du,ds);aJ=[0];bt();aJ[0]=E()
	def dv():
		a.update({"shutting":False,"docked":False,"queue":[],"page":{},"mobs":{},"inview":set(),"seen":None,"next_list":0.,"next_friends":0.,"next_profile":0.,"guild_busy":False,"guild_dirty":False,"guild_next":0.,"guild_fails":0,"guild_said":"","guild_pages":0,"ghid":0,"view":{},"view_serials":None,"allies":[],"fit":None,"me_s":0,"friends_raw":None,"kept":{},"prof_part":False,"again_for":None,"again_build":False,"minimized":Q.start_min()});del K[:]
		if not(aJ[0]and aJ[0]==E()):bt()
		aJ[0]=0;CL.find();aY();Q.dock(cT,exact=True,verify=True,min=bK);ax.service("social.note",cD)
	def dw():
		if j["g"]is None:return
		if Kit.closed(j):return
		q=a["queue"]
		while q:
			b=q.pop(0);l=b[0]if isinstance(b,tuple)else b
			if b=="to_bar"or(b=="toggle_min"and not a["minimized"]):a["msg"][d["tab"]]=aH()
			if b=="redraw":a["rebuild"]=True;continue
			if Q.action(b):continue
			if l in b7:b7[l](b[1]);continue
			if b in b8:b8[b]();continue
			if b in bZ:c9(bZ[b],aH());continue
			if b in b1 and dc(b)and b=="invite":f("target who to invite.")
		if a["rebuild"]:
			if not a["minimized"]:a["msg"][d["tab"]]=aH()
			aY();return
		if a["guild_dirty"]:a["guild_dirty"]=False;a["next_list"]=0.
		e=time.time()
		if e<a["next_list"]<=e+bl:return
		h=a["minimized"]and a["docked"]
		if h and not(d["announce"]or d["left"]):a["seen"]=None;return
		a["next_list"]=e+bl;cH();c="mini"if a["minimized"]else j["tab"];m=set();a["view_serials"]=None
		if c in b6:b6[c](m,e,h)
		if c in("guild","profile"):bD(c=="profile")
		g={};n=a["kept"]if c=="guild"else None
		for s in m:
			if not s:continue
			i=n.get(s)if n else None
			if i is not None:g[s]=(i[0],0,0,i[1],False,None);continue
			o=bA(s)
			if o is not None:g[s]=o
		a["mobs"]=g;k=set();p=[]
		for s in a["fserials"]:
			if s in g:k.add(s)
			else:p.append(s)
		if c=="friends"or(c=="mini"and not h)or d["announce"]or d["left"]:k|=cJ(p)
		a["inview"]=k;dg();a4()
	def dx():
		while K and not a["shutting"]:K.pop(0)()
	def dy():a["shutting"]=True;ay();a["names_dirty"]=True;aT();bw();ax.close()
	return{"start":dv,"tick":dw,"stop":dy,"client_tick":True,"config_height":aI.height,"build_config":aI.build,"poll_config":aI.poll,"config_closed":aI.closed,"thread_tick":dx,"thread_wanted":lambda:bool(K)}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("social","Social","Friends, party, guild and profile",_module_social,.1,category="The world")
