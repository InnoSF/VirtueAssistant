def _module_social():
	G=Client._type;Y=Follow.alt_held;aM=HOST.mobile;aN=HOST.mobiles;L="social";C="Social";aO="Social_settings";bN="Social_pos";bO="Social_min";aP="Social_names";aQ="Social_guild";aR="Social_roster";bP=7956;bQ=460;bR=600;aS,bS=240,46;bT=24;aT,aU=4,16;aV=8;aW=[("friends","Friends"),("party","Party"),("guild","Guild"),("profile","Profile")];aX={"friends":"Show TazUO's friends list and their health","party":"Show your party: members, invites, loot and chat","guild":"Show your guild: info, roster and chat","profile":"Show your character and the client's windows"};bU=((60,1,"just now"),(3600,60,"%d min ago"),(86400,3600,"%d h ago"),(172800,86400,"%d day ago"),(0,86400,"%d days ago"));aY=.25;bV=2.;bW=1.;bX=15;aZ=4.;Z="Diplomacy";ap=3;aq=9999;ar=150;aa=90;bY=64;a_=120;bZ=200;N,ab="My Guild","Guild Roster";at,b_=1,2;a0=7;b0=40;b1=300;a1=5;au=120;a2=60;b2=600;b3=(1062939,1062940,1063035);b4=("not a member of any guild","abbreviation:");a3={1062954:"Guild Name",1063025:"Alliance",1063084:"Guild Faction",1062955:"Name",1062956:"Rank",1062952:"Last On",1062953:"Guild Title",1063015:"Online",1062959:"Leader",1062960:"Warlord",1062961:"Emissary",1062962:"Member",1062963:"Ronin",1062974:ab,1063014:N,1062978:Z,1062992:"Invite Player",3006115:"Resign"};av=(1063014,1062974,1062978);b5=("1063014","1062974","1062978");b6=(N.lower(),ab.lower(),Z.lower());b7=("Unknown","Innocent","Ally","Gray","Criminal","Enemy","Murderer","Invulnerable");O,RS="\x1f","\x1e";A,I,D="|",";","~";aw="Social_notes";ax=500;a4=200;b8="Social_note_pos";b9=440;P=[("online","Sort: online","Online"),("laston","Sort: last on","Last on"),("rank","Sort: rank","Rank"),("name","Sort: name","Name")];H=[dc[0]for dc in P];a5=(("leader","guild leader"),("warlord",),("emissary",),("member",),("ronin",));ca=re.compile(r"(\d{1,4})\s*([-/.])\s*(\d{1,2})\s*[-/.]\s*(\d{1,4})");d={"tab":"friends","rows":aV,"bars":True,"announce":True,"gevery":a1,"ghide":True,"dbutton":ap,"left":False,"gsort":"online"};db=dict(d);a={"shutting":False,"minimized":False,"docked":False,"queue":[],"friends":[],"names_dirty":False,"party":None,"profile":None,"msg":{},"gids":{},"me_s":0,"fserials":[],"notos":{}};j={"g":None,"c":{},"store":({},{})};ac,k,f=Kit.basics(a,C);B=[];q={};o={"dirty":False,"ver":0,"chg":{}};J={"g":None,"c":{},"store":({},{}),"name":""};M=Kit.MARGIN
	def a6():
		p=Kit.get_var(aO).split("|")
		def b(i,lo,hi,a):
			try:return max(lo,min(hi,int(p[i])))
			except Exception:return a
		if len(p)>=4:
			if p[0]in aX:d["tab"]=p[0]
			d.update({"rows":b(1,aT,aU,aV),"bars":p[2]=="1","announce":p[3]=="1"})
		if len(p)>=6:d.update({"gevery":b(4,0,au,a1),"ghide":p[5]=="1"})
		if len(p)>=8:d.update({"dbutton":b(6,0,aq,ap),"left":p[7]=="1"})
		if len(p)>=9 and p[8]in H:d["gsort"]=p[8]
		c={}
		for e in Kit.get_var(aP).split("|"):
			if "="in e:
				s,n=e.split("=",1)
				with Kit.quiet:c[int(s)]=n
		a["names"]=c;cb();cd()
	def ad():Kit.put_var(aO,"|".join([str(int(d[b]))if isinstance(d[b],bool)else str(d[b])for b in("tab","rows","bars","announce","gevery","ghide","dbutton","left","gsort")]))
	def ay():
		if not a["names_dirty"]:return
		a["names_dirty"]=False;b=sorted(a["names"].items())[-200:];Kit.put_var(aP,"|".join("%d=%s"%(c,e.replace("|","/").replace("=","-"))for c,e in b))
	def E():return{"ok":False,"in_guild":True,"name":"","alliance":"","faction":"","charter":"","website":"","members":[],"at":0.,"note":""}
	def ae(s):s=str(s or "").replace(O," ").replace(RS," ").replace("\n"," ").strip();return s.replace(D,D+"t").replace(A,D+"p").replace(I,D+"s")
	def az(s):return str(s or "").replace(D+"p",A).replace(D+"s",I).replace(D+"t",D)
	def a7(raw,a,b):
		if O in raw or RS in raw:return raw.split(a)
		return[az(c)for c in raw.split(b)]
	def cb():
		b=E();c=a7(Kit.get_var(aQ),O,A)
		if len(c)>=7:
			b["name"],b["alliance"],b["faction"],b["charter"],b["website"]=c[:5]
			try:b["at"]=float(c[5])
			except Exception:b["at"]=0.
			b["in_guild"]=c[6]!="0";b["ok"]=b["at"]>0
		e=[];d=Kit.get_var(aR)
		for g in d.split(RS if O in d or RS in d else I):
			f=a7(g,O,A)
			if len(f)>=5 and f[0]:e.append({"name":f[0],"rank":f[1],"laston":f[2],"title":f[3],"online":f[4]=="1","me":False})
		b["members"]=e;a["guild"]=b
	def cc():b=a["guild"]or E();Kit.put_var(aQ,A.join([ae(b[c])for c in("name","alliance","faction","charter","website")]+["%d"%int(b["at"]or 0),"1"if b["in_guild"]else "0"]));Kit.put_var(aR,I.join(A.join([ae(e[g])for g in("name","rank","laston","title")]+["1"if e["online"]else "0"])for e in b["members"][:b1]))
	def cd():
		try:a=str(API.GetPersistentVar(aw,"",API.PersistentVar.Account)or "")
		except Exception:a=""
		a8(a)
	def a8(raw):
		a={}
		for b in raw.split(I):
			f=[az(c).strip()for c in b.split(A)]
			if len(f)>=2 and f[0]and f[1]and len(a)<ax:a[f[0].lower()]=(f[0],f[1])
		for k,v in list(o["chg"].items()):
			if v is None:a.pop(k,None)
			else:a[k]=v
		for k in[e for e in q if e not in a]:del q[k]
		q.update(a);o["ver"]+=1
	def a9():
		if not o["dirty"]:return
		o["dirty"]=False;a=dict(o["chg"]);c=dict((h,None if g is None else A.join([ae(g[0]),ae(g[1])]))for h,g in a.items())
		try:d=str(API.GetPersistentVar(aw,"",API.PersistentVar.Account)or "");b=Kit.merge_text(d,c,lambda rec:az(rec.split(A)[0]).strip().lower(),I)[0];API.SavePersistentVar(aw,b,API.PersistentVar.Account)
		except Exception as e:o["dirty"]=True;f("couldn't save the notes (%s); they're saved with the next change."%e,Kit.HUE_BAD);return
		for k,v in a.items():
			if o["chg"].get(k,0)==v:o["chg"].pop(k,None)
		a8(b)
	def ce(a):e=q.get(str(a or "").strip().lower());return e[1]if e else ""
	def ba():o["dirty"]=True;o["ver"]+=1;B.append(a9)
	def cf(name,text):
		name=" ".join(str(name or "").split());text=" ".join(str(text or "").split())[:a4]
		if not name:f("type a name first.");return False
		k=name.lower()
		if not text:
			if q.pop(k,None)is not None:o["chg"][k]=None;f("note on %s deleted."%name);ba()
			return True
		if k not in q and len(q)>=ax:f("at most %d notes; delete one first."%ax,Kit.HUE_BAD);return False
		q[k]=o["chg"][k]=(name,text);ba();f("note on %s saved."%name,Kit.HUE_GOOD);return True
	l=Kit.fit
	def af(name,serial=0,me=False):
		if me:return Kit.veil("me",name)
		b=Kit.noto_mark(a["notos"].get(serial,0))if Kit.cblind and serial else ""
		if Kit.streamer:name=Kit.veil("name",name,serial or Kit.checksum(name.lower().encode("utf-8")))
		return b+" "+name if b else name
	def ag():return Kit.pitch(bT)
	def bb():return bool(Client.key_held("shift"))
	def Q(part,on):
		if part[0]is not None and part[1]!=on:part[1]=on;Kit.set(part[0],"IsVisible",on)
	def cg(n):
		if n is None:return ""
		try:i=int(n)
		except Exception:i=-1
		return b7[i]if 0<=i<8 else str(n).split(".")[-1]
	def u():
		s=a["me_s"]
		if not s:
			try:s=int(API.Player.Serial or 0)
			except Exception:s=0
			a["me_s"]=s
		return s
	def ci():
		b=a["profile"]
		if b and b[0]:return b[0]
		try:return str(API.Player.Name or "")
		except Exception:return ""
	def bc(t):return "never"if not t else Kit.ago(time.time()-t,bU)
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
			if a is None:c=Typing._get(None,"Game",G("ClassicUO.Client"));a=Typing._get(Typing._get(c,"UO"),"World")
			CL.world=a;CL.GA=G("ClassicUO.Game.GameActions");CL.UIM=G("ClassicUO.Game.Managers.UIManager");CL.FLM=G("ClassicUO.Game.Managers.FriendsListManager")
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
				t=G("ClassicUO.Game.UI.Gumps.IgnoreManagerGump")
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
	def bd(serial):
		m=aM(serial)
		if m is None:return
		try:return(str(m.Name or ""),int(m.Hits or 0),int(m.HitsMax or 0),int(m.Distance),bool(m.IsDead),True)
		except Exception:return
	def be(serial):
		b=a["mobs"];d=b.get(serial)
		if d is not None and d[5]is None:
			d=bd(serial)
			if d is None:b.pop(serial,None)
			else:b[serial]=d
		return d
	def cj():
		i=time.time()
		if i<a["next_friends"]:return
		a["next_friends"]=i+bV;d=CL.friends();l=d is not None
		if d is None:d=[(int(m),a["names"].get(int(m),""))for m in API.GetAllFriends()or()]
		j=u();g=(j,d)if l else None
		if g is not None and g==a["friends_raw"]:
			if a["names_dirty"]:B.append(ay)
			return
		f=[];k=False
		for b,c in d:
			if b==j or not b:continue
			if not c:k=True;h=a["mobs"].get(b);c=(h[0]if h and h[0]else "")or a["names"].get(b,"")
			if c and a["names"].get(b)!=c:a["names"][b]=c;a["names_dirty"]=True
			f.append((b,c or("0x%08X"%b)))
		f.sort(key=lambda e:(e[1].startswith("0x"),e[1].lower()));a["friends"]=f;a["fserials"]=[n for n,p in f];a["friends_raw"]=None if k else g
		if a["names_dirty"]:B.append(ay)
	def bf():
		p=CL.party()
		if p is None:b=int(API.GetPartyLeader()or 0);p=(b,0,False,[int(c)for c in API.GetPartyMemberSerials()or()])if b else None
		a["party"]=p
	def aA(p):return bool(p)and bool(p[0]or p[3])
	def bg(full=True):
		b=time.time()
		if b<a["next_profile"]and not(full and a["prof_part"]):return
		a["next_profile"]=b+bW;p=HOST.me()
		if p is None:a["profile"]=None;a["prof_part"]=False;return
		try:
			c=str(p.Name or "")
			try:d=p.raw.NameAndProps(False)
			except Exception:d=""
			e=[i.strip()for i in str(d or "").replace("\r","").split("\n")if i.strip()]
			if not full:f=a["profile"];h=f[2:]if f else("",0,0,0,0,0,False,False);a["profile"]=(c,e)+tuple(h);a["prof_part"]=True;return
			g=(c,e,cg(p.Notoriety),int(p.Gold or 0),int(p.Followers or 0),int(p.FollowersMax or 0),int(p.Weight or 0),int(p.WeightMax or 0),bool(p.InWarMode),bool(p.IsHidden))
		except Exception:g=None
		a["profile"]=g;a["prof_part"]=False
	def ck():
		i=u();d,e,f,g,h={},[],set(),{},{}
		for m in aN():
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
	def cl(c):
		b=a["view_serials"]
		if b is None and len(c)>cm:
			try:b={int(e.Serial)for e in aN()}
			except Exception:b=None
		if b is not None:return b.intersection(c)
		return{g for g in c if g and aM(g)is not None}
	cm=10
	def bh(fn):
		a=[None,None]
		def b(raw):
			for e in a:
				if e is not None and(e[0]is raw or e[0]==raw):return e[1]
			b=fn(raw);a[1]=a[0];a[0]=(raw,b);return b
		return b
	@bh
	def aB(raw):return Kit.gump_cells(raw,a3)
	@bh
	def z(raw):
		c=aB(raw)[0]
		if not c:return
		a=[e["text"].lower()for e in c];b=[g["cliloc"]for g in c]
		if any(h in av for h in b)or ab.lower()in a:
			if(1062955 in b and 1062956 in b)or("rank"in a and("last on"in a or "name"in a)):return "roster"
			return "guild"
		d="\x00".join(a)
		if any(i in b3 for i in b)or any(m in d for m in b4):return "noguild"
	def cn(raw):return any(b in raw for b in b5)or "roster"in raw.lower()
	def co(cells,d=6):
		a=[]
		for b in sorted(cells,key=lambda c:(c["y"],c["x"])):
			if a and abs(b["y"]-a[-1][0])<=d:a[-1][1].append(b)
			else:a.append([b["y"],[b]])
		return[sorted(e,key=lambda c:c["x"])for g,e in a]
	def bi(raw):
		a,f=aB(raw);a=[g for g in a if g["cliloc"]not in av]
		def e(cliloc):
			e=a3[cliloc].lower();b=next((g for g in a if g["cliloc"]==cliloc or g["text"].lower()==e),None)
			if b is None:return ""
			d=[h for h in a if abs(h["y"]-b["y"])<=6 and h["x"]>b["x"]];return min(d,key=lambda c:c["x"])["text"]if d else ""
		b={"name":e(1062954),"alliance":e(1063025),"faction":e(1063084),"charter":"","website":""};d=sorted([i for i in a if i["w"]>=300 and i["bg"]],key=lambda c:c["y"])
		if d:b["charter"]=d[0]["text"]
		if len(d)>1:b["website"]=d[1]["text"]
		for k in("charter","website"):
			if "not yet set"in b[k].lower():b[k]=""
		return b
	def cp(raw):
		g,r=aB(raw);g=[ch for ch in g if ch["cliloc"]not in av and ch["text"].lower()not in b6];m=co(g);e=None
		for c in m:
			h=[dc["text"].lower()for dc in c]
			if len(c)>=3 and("name"in h or "rank"in h or "last on"in h or any(dd["cliloc"]in(1062955,1062956,1062952,1062953)for dd in c)):e=c;break
		if e is None:return[],False
		s=[de["x"]for de in e];t=[df["text"].lower()for df in e];b={}
		for u,v in(("name",("name",)),("rank",("rank",)),("laston",("last on","online")),("title",("title",))):
			for i,w in enumerate(t):
				if any(dg in w for dg in v)and i not in b.values():b[u]=i;break
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
			l=q["raw"].lower();f=[d[b[dh]]["text"]if dh in b and b[dh]in d else ""for dh in("rank","laston","title")];z=f[1].lower()=="online"or "#000066"in l or "#006600"in l;n.append({"name":a,"rank":f[0],"laston":f[1],"title":f[2],"online":z,"me":"#006600"in l})
		A=any(di[2]==a0 for di in r);return n,A
	def cq():
		a=int(API.HasGump()or 0)
		if not a:return 0,""
		try:return a,str(API.GetGump(a).PacketGumpText or "")
		except Exception:return a,""
	def ah():return safe(lambda:Kit.on_client(cq))or(0,"")
	def bj(raw):return cn(raw)and z(raw)in("guild","roster")
	def ai(gid=0):
		a=HOST.services.get("gump.expect")
		if a is not None and gid:a(gid,aZ+1.)
		if d["ghide"]and gid:API.ConfigNextGump(serial=gid,isVisible=False)
	def cr():API.ConfigNextGump()
	def cs(c):
		a,b=ah()
		if not a or a==c:return "the guild window didn't come"
		d=" ".join(b.split())[:bZ]if b else "(empty layout)";f("gump 0x%08X came instead of the guild window (left open); it begins: %s."%(a,d));return "the guild window didn't come (another gump did)"
	def K(check):
		d=time.time()+aZ
		while time.time()<d and not a["shutting"]:
			c,b=ah();r=c and b and check(b)
			if r:return c,b,r
			if not HOST.idle(.15):break
		return 0,"",None
	def R(gid,label,button):
		a=safe(lambda:API.GetGump(gid))
		if a is not None and CL.press_labelled(Kit.client_control(a)or a,label):return True
		return bool(button)and bool(API.ReplyGump(button,gid))
	def ct():
		a["guild_busy"]=True;a["guild_pages"]=0;c=a["guild"]or E();b=c
		try:b=cu(c)
		except Exception as i:b=E();b["note"]="couldn't read the guild window (%s)"%i
		finally:
			with Kit.quiet:cr()
			g=a.get("ghid",0);a["ghid"]=0
			if g:
				with Kit.quiet:API.CloseGump(g)
			e=not b["ok"]
			if e:j,b=b["note"],dict(c);b["note"]=j;a["guild_fails"]=min(a["guild_fails"]+1,10);a["guild_next"]=time.time()+min(b2,a2*(2**(a["guild_fails"]-1)))
			else:a["guild_fails"]=0;a["guild_said"]=""
			a["guild"]=b;a["guild_busy"]=False;a["guild_dirty"]=True
			if b["ok"]and not e:cc()
		if b["note"]:
			if not e:f("%s."%b["note"])
			elif b["note"]!=a["guild_said"]:
				a["guild_said"]=b["note"];h=""
				if d["gevery"]and d["tab"]=="guild":h=" (retry in %d min)"%max(1,int((a["guild_next"]-time.time())/60+.5))
				f("%s%s."%(b["note"],h),Kit.HUE_BAD)
	def cu(old):
		c=E();c["members"]=list(old["members"]);f=a["gids"]
		def g(note,a=False):
			c["note"]=note
			if a:c.update({"ok":True,"at":time.time()})
			return c
		o,j=ah();p=z(j)if j else None;d=p in("guild","roster")
		if not d:
			u,v=CL.find_server_gump(bj)
			if u:o,j,p,d=u,v,z(v),True
		if d:b,e,h=o,j,p
		else:
			ai(f.get("info",0)if old.get("in_guild",True)else 0)
			if not CL.game_action("OpenGuildGump"):return g("couldn't ask for the guild window (%s)"%CL.error)
			b,e,h=K(z)
			if not b:return g(cs(o))
			a["ghid"]=b
		if h=="noguild":API.CloseGump(b);a["ghid"]=0;c.update({"ok":True,"in_guild":False,"members":[],"at":time.time()});return c
		if h=="roster":
			f["roster"]=b
			if not d:ai(f.get("info",0))
			R(b,N,at);b,e,h=K(lambda r:z(r)=="guild"and "guild")
			if not b:return g("the My Guild page didn't come")
			if not d:a["ghid"]=b
		q=bi(e)
		if d and not q.get("name"):
			s=e;R(b,N,at);b,e,h=K(lambda a:z(a)=="guild"and a!=s and "guild")
			if not b:return g("the My Guild page didn't come")
			q=bi(e)
		f["info"]=b;c.update(q)
		if not d:ai(f.get("roster",0))
		if not R(b,ab,b_):return g("couldn't open the Guild Roster page",True)
		b,e,h=K(lambda r:z(r)=="roster"and "roster")
		if not b:return g("the Guild Roster page didn't come",True)
		if not d:a["ghid"]=b
		f["roster"]=b;l,n,i,t=[],{},0,False
		while not a["shutting"]:
			y,A=cp(e);i+=1;a["guild_pages"]=i
			for m in y:
				k=m["name"].lower()
				if k not in n:n[k]=True;l.append(m)
			if not A or i>=b0:t=True;break
			if not d:ai(b)
			if not API.ReplyGump(a0,b):break
			s=e;w,B,C=K(lambda a:z(a)=="roster"and a!=s and "ok")
			if not w:break
			b,e=w,B
			if not d:a["ghid"]=b
		if not t or not l:
			for m in old["members"]:
				k=m["name"].lower()
				if k not in n:n[k]=True;x=dict((ch,dc)for ch,dc in m.items()if not ch.startswith("_"));x["online"]=False;l.append(x)
			if not t and i:c["note"]="read %s only; rest as before"%Kit.count(i,"roster page")
		c["members"]=l;c.update({"ok":True,"at":time.time()})
		if d:R(b,N,at)
		else:API.CloseGump(b);a["ghid"]=0
		return c
	def bk(tab):return bR if tab=="guild"else bQ
	def cv(fw,fh,mode):
		b=(int(fw),int(fh))if(fw is not None and fh is not None)else None
		if b!=a.get("fit"):a["fit"]=b;k("redraw")()
		elif mode=="again"and b is not None:
			c=(b,d["tab"],a["minimized"],d["rows"],d["bars"]);e=time.time()
			if c!=a["again_for"]or not 0<=e-a.get("again_at",0.)<5.:a.update({"again_for":c,"again_at":e,"again_build":True});k("redraw")()
	def bl():return max(160,M+30+Kit.text_w(C.upper())+6+94+M)
	def cw():return(M+30+Kit.text_w(C.upper())+16+(0 if Kit.zone_up(L)else 84+Kit.DOCK_DX)+35+Kit.text_w("Settings")+M)
	def cx(iw):
		c,a,b=[],10,0
		for f,d in aW:
			e=35+Kit.text_w(d)
			if a>10 and a+e>iw-4:a,b=10,b+1
			c.append((f,d,a,b));a+=e+14
		return c,b+1
	def aC(tab):a,b={"friends":(1,1),"party":(2,3),"guild":(6,2)}.get(tab,(7,2));return a,b,d["rows"]if a<7 else 0
	def bm(tab):a,c,b=aC(tab);d=(8+a*22+(8 if a else 0)+c*30+b*ag()+(8 if b else 0)+4);return M+30+Kit.GAP+30+Kit.GAP+d+M
	def bn():return(bl(),max(bm(b)-max(0,aC(b)[2]-1)*ag()for b,c in aW)+30)
	def aD():
		c=d["tab"];g,n,o=F.begin(bk(c),bm(c));w,h=F.w,F.h;p=[];j["info_tips"],j["info_in"]={},{}
		if a["again_build"]:a["again_build"]=False
		else:a["again_for"]=None
		if not a["minimized"]:
			b=a.get("fit")
			if b is not None and b[1]<bn()[1]:b=None
			if b is not None:w,h=max(bl(),b[0]),b[1]
			e=w-2*M;o["iw"]=e;F.frame(g,w,h,settings=w>=cw());i=M+30+Kit.GAP;r,l=cx(e);Kit.add_section(g,M,i,e,30*l)
			for f,s,t,u in r:Kit.art_button(g,n,"tab_"+f,Kit.ART_PAGE,M+t,i+4+30*u,s,aX[f],hue=Kit.HUE_TITLE if f==c else Kit.HUE_TEXT,on_click=k(("tab",f)))
			m=i+30*l+Kit.GAP
			if b is None:h+=30*(l-1)
			q=h-m-M;Kit.add_section(g,M,m,e,q);cy(g,n,o,p,c,M,m,e,q,b is not None)
		F.end(g,{"rows":p,"tab":c,"info":{}},w,h);a["rebuild"]=False;aK()
	F=Kit.Window(L,C,a,j,aD,bN,bO,mini=(aS,bS),icon=bP,cleanup=ac,docked_min=True)
	def cy(g,store,c,rows,tab,x,y,w,h,fit=False):
		b,l,j=aC(tab);ak[0]=x+w-6;k=ag()
		def f(a):return max(1,(y+h-12-a)//k)if fit else j
		e=max(1,min(b,(h-16-l*30-(k+12 if j else 4))//22))if fit and b else b;c["info"]=[Kit.add_label(g,"",x+10,y+8+22*min(n,e-1),Kit.HUE_INFO)for n in range(b)]
		for m in c["info"][e:]:m.IsVisible=False
		a=y+8+22*e+(8 if e else 0)
		if tab=="friends":i=[("add",Kit.ART_PLAY,["Add friend...",None],"Target someone to add to TazUO's friends list"),("add_last",Kit.ART_OK,["Add last target",None],"Add your last target to TazUO's friends list")];a=bq(g,store,c,x,y,a,w,i,None);aH(g,store,c,rows,f(a),x,a,w,aE%"set as last target (or answer a target cursor)",True,rm_tip="Remove from TazUO's friends list")
		elif tab=="party":a+=30*S(g,store,c,x,a,x+w-6,[("invite",Kit.ART_PLAY,["Invite...",None],"Target someone to invite to your party"),("leave",Kit.ART_CLOSE,["Leave",None],"Leave the party"),("loot",Kit.ART_OK,["Loot",None],"Allow or forbid party looting of your corpse (the line above shows which)"),("pwin",Kit.ART_PAGE,["Party window",None],"Open the client's party window")]);ak[0]=x+w-6-aj-6;c["accept"]=aF(g,store,x+10,a,"accept",Kit.ART_OK,"Accept","Join the party. Alt+click: auto-follow the inviter (again to stop)",on_click=br("accept"));c["decline"]=aF(g,store,c["accept"][1],a,"decline",Kit.ART_CLOSE,"Decline","Turn the invitation down. Alt+click: auto-follow the inviter (again to stop)",on_click=br("decline"));ak[0]=x+w-6;aG(g,store,c,x+w,a);a+=30;bs(g,store,c,x,a,w,[("psend","Send","Say it in party chat")],"Message for party chat");a+=30;aH(g,store,c,rows,f(a),x,a,w,aE%"set as last target (or answer a target cursor)",True,rm_tip="Remove from the party (leader only)")
		elif tab=="guild":i=[("grefresh",Kit.ART_PLAY,["Refresh",None],"Read the guild window again (info and roster); "+("it opens hidden"if d["ghide"]else "it shows while read; Social settings can hide it")),("gwin",Kit.ART_PAGE,["Guild window",None],"Open the server's guild menu"),("diplo",Kit.ART_PAGE,["Diplomacy",None],"Open the guild window's Diplomacy page"),("gsort",Kit.ART_PAGE,["long","short",None],None)];a=bq(g,store,c,x,y,a,w,i,[3,2,1,0,3]);bs(g,store,c,x,a,w,[("gsend","Guild","Say it in guild chat"),("asend","Alliance","Say it in alliance chat")],"Message for guild or alliance chat");a+=30;aH(g,store,c,rows,f(a),x,a,w,aE%"set as last target when in view",False,before=[("rank",bY)],after=[("title",0)])
		else:a+=30*S(g,store,c,x,a,x+w-6,[("edit",Kit.ART_PAGE,["Edit profile",None],"Open your profile (the server's scroll; closing saves)"),("paperdoll",Kit.ART_PAGE,["Paperdoll",None],"Open the client's paperdoll"),("status",Kit.ART_PAGE,["Status",None],"Open the client's status window")]);S(g,store,c,x,a,x+w-6,[("ignore",Kit.ART_PAGE,["Ignore list",None],"Open TazUO's ignore list (speech you hide)"),("war",Kit.ART_PLAY,["War / peace",None],"Switch war mode and peace (the last line above shows which)")])
	aE="Click: %s. Shift+click: write a note. Alt+click: auto-follow (again to stop)";aj=100
	def bo(c):
		a="Next roster order: online (in view first), last on, rank or name"
		if c.get("gsort_bare"):e=P[H.index(d["gsort"])];a="Roster order: %s. %s"%(e[2].lower(),a)
		return a
	def cz(key,cap):
		if key=="gsort":
			if cap=="long":return max(Kit.text_w(b[1])for b in P)
			return max(Kit.text_w(c[2])for c in P)
		return Kit.text_w(cap)
	def bp(items,x,right,order):
		b=[0]*len(items)
		if order is None:order=list(range(len(items)-1,-1,-1))
		h=[None]+list(order)
		for c in h:
			if c is not None:b[c]=min(b[c]+1,len(items[c][2])-1)
			a,d=x+10,x+10
			for i,e in enumerate(items):
				f=e[2][b[i]]
				if f is None:d,a=a+30,a+30
				else:g=cz(e[0],f);d,a=a+35+g,a+35+g+12
			if d<=right:return list(b)
		return
	def S(g,store,c,x,y,right,items,order=None,plan=None):
		h=plan or bp(items,x,right,order);j=h is None
		if j:h=[len(p[2])-1 for p in items]
		b,e=x+10,0
		for m,(d,n,i,f)in enumerate(items):
			a=i[h[m]]
			if d=="gsort":c["gsort_long"]=a=="long";c["gsort_bare"]=a is None;f=bo(c);a=None if a is None else bw(c)
			elif a is None and i[0]:f=Kit.caption_tip(i[0],f)
			l=30 if a is None else 35+Kit.text_w(a)
			if j and b>x+10 and b+l>right:b,e=x+10,e+1
			o=Kit.art_button(g,store,d,n,b,y+30*e,a,f,on_click=k(d));b+=30 if a is None else l+12
			if d=="gsort":c["gsort"]=o if a is not None else None;c["gsort_btn"]=store[0].get(d)
		return e+1
	def bq(g,store,c,x,y,a,w,items,order):
		b=bp(items,x,x+w-6-aj-6,order);e=b is not None and all(h[2][i]is not None and(i==0 or h[0]=="gsort")for h,i in zip(items,b))
		if e:d=S(g,store,c,x,a,x+w-6-aj-6,items,order,b);aG(g,store,c,x+w,a)
		else:d=S(g,store,c,x,a,x+w-6,items,order);aG(g,store,c,x+w,y+8-6);c["info_cut"]=aj+6
		return a+30*d
	ak=[100000]
	def aF(g,store,x,y,key,art,cap,tip,on_click=None):a=x+35+Kit.text_w(cap)>ak[0];b=Kit.art_button(g,store,key,art,x,y,None if a else cap,Kit.caption_tip(cap,tip)if a else tip,on_click=on_click or k(key));return store[0].get(key),(x+30 if a else x+35+Kit.text_w(cap)+12),b
	def br(key):
		def b(*c):
			p=a["party"];b=p[1]if p else 0
			if b and Y():k(("follow",b))()
			else:k(key)()
		return b
	def aG(g,store,c,right,y):c["pg"]=Kit.add_label(g,"",right-100,y+6,Kit.HUE_INFO);Kit.art_button(g,store,"pg_up",Kit.ART_RESTORE,right-56,y+4,None,"Previous page",on_click=k(("page",-1)));Kit.art_button(g,store,"pg_dn",Kit.ART_MIN,right-34,y+4,None,"Next page",on_click=k(("page",1)))
	def bs(g,store,c,x,y,w,buttons,i):
		j=sum(35+Kit.text_w(p)+12 for n,p,n in buttons);b=w-20-j-8
		if b<a_:b=max(40,w-20-30*len(buttons)-8)
		e=x+10;f=Kit.text_w("Say:")+8
		if b-f>=a_:Kit.add_label(g,"Say:",e,y+6,Kit.HUE_INFO);e+=f;b-=f
		c["msg"]=Kit.with_tip(Kit.add_textbox(g,a["msg"].get(d["tab"],""),e,y+3,b,numbers=False),i);h=e+b+12
		for k,l,m in buttons:h=aF(g,store,h,y,k,Kit.ART_PLAY,l,m)[1]
	def aH(g,store,c,rows,n,x,y,w,tip,o,before=None,after=None,rm_tip="Remove"):
		b,p=Kit.pic_size(Kit.LINE_RED);b,p=b or 109,p or 9;A,u=Kit.pic_size(Kit.LINE_BLUE);q=x+w-4-(40 if o else 0);before,after=list(before or[]),list(after or[]);s=[];f=d["bars"]
		def v():return sum(ch+8 for dc,ch in before)+sum((dd or 40)+8 for de,dd in after)
		while q-(x+10)<v()+8+40+8+(30+8 if f else 0)+44 and(after or before or f):
			if after:s.append(after.pop()[0])
			elif before:s.append(before.pop()[0])
			else:f=False
		t,k=ar,aa;l=q-(x+10)-v()-8;B=ar+8+(b+8 if f else 0)+aa
		if l<B:
			k=max(44,min(aa,int(l*.24)))
			if f:b=max(30,min(b,int(l*.3)))
			t=max(40,l-k-8-(b+8 if f else 0))
		c["bar_w"],c["name_w"],c["status_w"]=b,t,k;z=ag()
		for m in range(n):
			e=y+m*z;r={"serial":0,"prev":(0,0.),"parts":[],"name":None,"status":None,"fill":None,"fill_w":-1,"x":None,"red":None,"extra":{},"who":"","prev_who":("",0.),"tip0":tip,"tip":tip};a=x+10;r["name"]=Kit.add_label(g,"",a,e+3);r["parts"].append([r["name"],True]);a+=t+8
			for i in s:r["extra"][i]=(None,0)
			for i,h in before:j=Kit.add_label(g,"",a,e+3,Kit.HUE_INFO);r["extra"][i]=(j,h);r["parts"].append([j,True]);a+=h+8
			if f:
				r["red"]=[Kit.add_tiled(g,Kit.LINE_RED,a,e+7,b,p),True];r["parts"].append(r["red"])
				if A and u:r["fill"]=Kit.add_tiled(g,Kit.LINE_BLUE,a,e+7,1,u);r["fill"].SetWidth(0);r["parts"].append([r["fill"],True])
				a+=b+8
			r["status"]=Kit.add_label(g,"",a,e+3,Kit.HUE_INFO);r["parts"].append([r["status"],True]);a+=k+8
			for i,h in after:h=h or max(40,q-a);j=Kit.add_label(g,"",a,e+3,Kit.HUE_INFO);r["extra"][i]=(j,h);r["parts"].append([j,True]);a+=h+8
			r["catch"]=Kit.catcher(g,x+4,e,w-8-(40 if o else 0),z,cB(rows,m),tip);r["parts"].append([r["catch"],True])
			if o:r["x"]=Kit.art_button(g,store,"rm%d"%m,Kit.ART_CLOSE,x+w-42,e+1,None,rm_tip+". Alt+click: auto-follow (again to stop)",on_click=cA(rows,m));r["parts"].append([r["x"],True])
			rows.append(r)
	def aI(r,cur,prev,now):p,a=r[prev];return p if p and now-a<.15 else r[cur]
	def cA(rows,i):
		def a(*b):
			a=aI(rows[i],"serial","prev",time.time())
			if a and Y():k(("follow",a))()
			elif a:k(("rm",a))()
		return a
	def cB(rows,i):
		def a(*d):
			r,c=rows[i],time.time();b,a=aI(r,"serial","prev",c),aI(r,"who","prev_who",c)
			if not b:
				if a and not Y()and bb():k(("note",a))()
				elif a:k(("noview",a))()
				return
			if Y():k(("follow",b))()
			elif a and bb():k(("note",a))()
			else:k(("click",b))()
		return a
	cC={}
	def al(r,key,prev,v):
		if r[key]!=v:r[prev],r[key]=(r[key],time.time()),v
	def bt(r,serial,name,status,hue,d,extra=None,name_hue=None,bar=True,show_x=True,me=False):
		e=extra or cC;c=af(name,serial,me);a=(serial,name,status,hue,d,e.get("rank"),e.get("title"),name_hue,bar,show_x,o["ver"],c)
		if a==r.get("last"):return
		r["last"]=a;al(r,"serial","prev",serial);al(r,"who","prev_who",name)
		if name_hue is None:name_hue=Kit.HUE_TEXT if d is not None else Kit.HUE_INFO
		h=j["c"];i,k=l(c,h.get("name_w",ar)),l(status,h.get("status_w",aa));Kit.set_text(r["name"],i,name_hue);Kit.set_text(r["status"],k,hue);m=(["Name: %s"%c]if i!=c else[])+(["Status: %s"%status]if k!=status else[])
		for a,(n,t)in r["extra"].items():
			f=str(e.get(a,"")or "");g=""
			if n is not None:g=l(f,t);Kit.set_text(n,g,Kit.HUE_INFO)
			if g!=f:m.append("%s: %s"%(a.capitalize(),f))
		b="\n".join([r["tip0"]]+m)
		if q:
			s=q.get(name.lower())
			if s is not None:b=b+"\nNote: "+s[1]
		if b!=r["tip"]and r.get("catch")is not None:r["tip"]=b;Kit.with_tip(r["catch"],b)
		w=int(j["c"].get("bar_w",109)*max(0.,min(1.,d or 0.)))
		if r["fill"]is not None and w!=r["fill_w"]:r["fill_w"]=w;Kit.ui_w(r["fill"],max(1,w))
		u=r["parts"][-1]if r["x"]is not None else None
		for p in r["parts"]:
			if r["fill"]is not None and p[0]is r["fill"]:Q(p,bar and w>0)
			elif r["red"]is not None and p is r["red"]:Q(p,bar)
			elif p is u:Q(p,show_x)
			else:Q(p,True)
	def bu(r):
		r["last"]=None;al(r,"serial","prev",0);al(r,"who","prev_who","")
		for p in r["parts"]:Q(p,False)
	def bv(serial):
		d=be(serial)
		if d is None:return "away",Kit.HUE_INFO,None
		h,c,b,e,f,i=d
		if f:return "dead",Kit.HUE_BAD,0.
		a=c/float(b)if b>0 else None;g=(Kit.HUE_GOOD if a is None or a>.5 else(Kit.HUE_TITLE if a>.25 else Kit.HUE_BAD));return(Kit.count(e,"tile")),g,a
	def T(items):n=max(1,len(j["rows"]));b=max(1,(len(items)+n-1)//n);p=max(0,min(b-1,a["page"].get(d["tab"],0)));a["page"][d["tab"]]=p;return items[p*n:(p+1)*n],("%d/%d"%(p+1,b))if b>1 else ""
	cD=dict((dl,dj)for dj,dk in enumerate(a5)for dl in dk)
	def cE(m):
		v=m.get("_lo")
		if v is None:
			v=-1;e=ca.search(m["laston"]or "")
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
	def bw(c):e=P[H.index(d["gsort"])];return e[1]if c.get("gsort_long")else e[2]
	cF={"src":None,"how":None,"order":[],"names":{},"online":0}
	def aJ(m):
		k=m.get("_k")
		if k is None:k=m["_k"]=m["name"].lower()
		return k
	def bx(e):return e[0]
	def cG(how):
		a=len(a5)
		if how=="online":return lambda m:((0 if m["online"]else 1),m["_k"])
		if how=="name":return lambda m:m["_k"]
		if how=="rank":return lambda m:(cD.get((m["rank"]or "").strip().lower(),a),m["_k"])
		return lambda m:((0 if m["online"]else 1),-cE(m),m["_k"])
	def by(gd,how):
		a=gd["members"];b=cF
		if b["src"]is not a or b["how"]!=how:
			c,d={},0
			for m in a:
				c[aJ(m)]=True
				if m["online"]:d+=1
			b.update({"src":a,"how":how,"order":sorted(a,key=cG(how)),"names":c,"online":d})
		return b
	def cH(me):
		p=a["guild"]or E();h,i=a["view"],a["mobs"];q=d["gsort"];j=by(p,q);c=[];n=0
		if q=="online":
			e=[]
			for m in p["members"]:
				b=h.get(m["_k"],0)
				if b:
					f=i.get(b)
					if f:e.append(((f[3],(0 if m["online"]else 1),m["_k"]),b,m))
			if e:
				e.sort(key=bx);n=len(e)
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
			k.sort(key=bx)
			for g in k:c.append((g[1],g[2]))
		return c,n
	def aK():
		G,d=j["g"],j["c"]
		if G is None or(a["minimized"]and a["docked"])or("status"in d)!=bool(a["minimized"]):return
		if a["minimized"]:
			H,h=len(a["friends"]),len(a["inview"]);b=a["party"];x="%s: %s, %d in view"%(C,Kit.count(H,"friend"),h)
			if aA(b):x+=", party of %d"%(len(b[3])+1)
			Kit.set_text(d["status"],l(x,aS-18-66));return
		i=j["tab"];c=d.get("info",[]);e=d.get("iw",bk(i)-2*Kit.MARGIN)-20;y=e-d.get("info_cut",0)
		if i=="friends":
			f=a["friends"];o,p=T(f);h=len(a["inview"]);z=(len(f),h,y)
			if j["info"].get("friends")!=z:j["info"]["friends"]=z;Kit.set_text(c[0],l("%s, %d in view"%(Kit.count(len(f),"friend"),h)if f else "No friends yet: Add friend... targets one",y))
			bz(d,[(ch,U(ch,dc))for ch,dc in o],p)
		elif i=="party":
			b=a["party"];k=u()
			if not aA(b):Kit.set_text(c[0],l("Not in a party: Invite... asks someone to join",e),Kit.HUE_INFO);Kit.set_text(c[1],"",Kit.HUE_INFO);f=[]
			else:m,g,I,q=b;J="you"if m==k else af(U(m),m);Kit.set_text(c[0],l(("Party of %d, led by %s"%(len(q)+1,J))if m else "Party of %d"%(len(q)+1),e),Kit.HUE_TEXT);Kit.set_text(c[1],l("Party may loot your corpse: %s"%("yes"if I else "no"),e),Kit.HUE_INFO);f=[dd for dd in q if dd!=k]
			g=b[1]if b else 0;n=bool(g)and not(b and b[0])
			for r in("accept","decline"):
				s=d.get(r)
				if s is not None and j["info"].get("vis_"+r)!=n:
					j["info"]["vis_"+r]=n
					for K in(s[0],s[2]):Kit.set(K,"IsVisible",n)
			if n:t=a["mobs"].get(g);Kit.set_text(c[0],l("Party invite from %s: Accept or Decline"%(af(t[0],g)if t and t[0]else "0x%08X"%g),e),Kit.HUE_TITLE)
			o,p=T(f);bz(d,[(de,U(de))for de in o],p,bool(b)and b[0]==k and bool(k))
		elif i=="guild":cI(c,d,e)
		else:
			if a["prof_part"]:bg(True)
			v=a["profile"]
			if not v:
				j["info"].pop("prof",None)
				for w in c:Kit.set_text(w,"")
				Kit.set_text(c[0],l("No character logged in",e),Kit.HUE_INFO);return
			A=(v,e)
			if j["info"].get("prof")==A:return
			j["info"]["prof"]=A;B,L,D,M,N,O,P,Q,E,R=v;F=[df for df in L if df!=B];S=[(Kit.veil("me",B),Kit.HUE_TITLE),(Kit.veil("guild"," / ".join(F))if F else "No titles read yet: hover yourself once",Kit.HUE_INFO),("Notoriety: %s"%(D or "unknown"),Kit.cb_hue(D.lower(),Kit.HUE_TEXT)),("Gold: %d"%M,Kit.HUE_TEXT),("Followers: %d / %d"%(N,O),Kit.HUE_TEXT),("Weight: %d / %d"%(P,Q),Kit.HUE_TEXT),("%s%s"%("War mode"if E else "Peace",", hidden"if R else ""),Kit.HUE_BAD if E else Kit.HUE_GOOD)]
			for w,(V,W)in zip(c,S):Kit.set_text(w,l(V,e),W)
	def U(s,other=None):d=a["mobs"].get(s);return(d[0]if d and d[0]else "")or a["names"].get(s,"")or other or "0x%08X"%s
	def bz(c,shown,pg,show_x=True):
		Kit.set_text(c["pg"],pg);a=j["rows"]
		for r,(b,d)in zip(a,shown):e,f,g=bv(b);bt(r,b,d,e,f,g,show_x=show_x)
		for r in a[len(shown):]:bu(r)
	def V(lbl,full,width,hue):
		a=j["info_in"];k=(full,width,hue)
		if a.get(lbl)==k:return
		d=l(full,width);Kit.set_text(lbl,d,hue);b=full if d!=full else "";c=j["info_tips"]
		if len(c)>64:c.clear()
		if c.get(lbl)!=b:c[lbl]=b;lbl.SetAcceptMouseInput(bool(b));lbl.SetTooltip(b)
		if len(a)>64:a.clear()
		a[lbl]=k
	def aL(lbl,text,hue=None):Kit.set_text(lbl,text,hue);j["info_in"].pop(lbl,None)
	def cI(info,c,tw):
		k=tw-c.get("info_cut",0);b=a["guild"]or E();n=a["profile"];o=[ch for ch in n[1][1:]if ch and ch!=n[0]]if n else[]
		if not b["ok"]:aL(info[0],l("Guild window not read yet",k),Kit.HUE_INFO)
		elif not b["in_guild"]:aL(info[0],l("Not in a guild",k),Kit.HUE_INFO)
		else:y=Kit.veil("guild",b["name"])if b["name"]else "Guild name not shown";V(info[0],y,k,Kit.HUE_TITLE)
		V(info[1],("You: "+Kit.veil("guild"," / ".join(o)))if o else "Your guild line isn't read yet: hover yourself once",tw,Kit.HUE_TEXT if o else Kit.HUE_INFO)
		if b["ok"]and b["in_guild"]:
			V(info[2],"Alliance: %s     Faction: %s"%(Kit.veil("guild",b["alliance"])if b["alliance"]else "none",b["faction"]or "none"),tw,Kit.HUE_TEXT)
			for z,A,u in((info[3],"Charter","charter"),(info[4],"Website","website")):V(z,"%s: %s"%(A,Kit.veil("guild",b[u])if b[u]else "not set"),tw,Kit.HUE_INFO)
		else:
			for B in info[2:5]:aL(B,"")
		p=str(ci()or "").lower();C,D=cH(p);F=by(b,d["gsort"])["online"]
		if a["guild_busy"]:v=a["guild_pages"];f="Reading the guild window"+(" (page %d)"%v if v else "");e=Kit.HUE_TITLE
		elif not b["ok"]:h=b["note"];f=((h[:1].upper()+h[1:])if h else("Click Refresh to read the guild window"if not d["gevery"]else "Read when this tab shows"));e=Kit.HUE_BAD if h else Kit.HUE_INFO
		elif not b["in_guild"]:f,e="Read %s; allies in view below"%bc(b["at"]),Kit.HUE_INFO
		else:
			G=len(b["members"]);f="%s, %d online, %d in view; read %s"%(Kit.count(G,"member"),F,D,bc(b["at"]))
			if b["note"]:f+="  (%s)"%b["note"]
			e=Kit.HUE_INFO
		V(info[5],f,tw,e);w,H=T(C);Kit.set_text(c["pg"],H)
		for r,(i,m)in zip(j["rows"],w):
			g=be(i)if i else None
			if g is not None:q,e,s=bv(i)
			elif m["online"]:q,e,s="Online",Kit.HUE_GOOD,None
			else:q,e,s=(m["laston"]or "offline"),Kit.HUE_INFO,None
			x=bool(m["me"]or(p and aJ(m)==p))
			if x:t=Kit.HUE_TITLE
			elif g is not None or m["online"]:t=Kit.HUE_GOOD if g is None else Kit.HUE_TEXT
			else:t=Kit.HUE_INFO
			I=Kit.veil("guild",m["title"])if m["title"]and not m.get("ally")else m["title"];bt(r,i if g is not None else 0,m["name"],q,e,s,extra={"rank":m["rank"],"title":I},name_hue=t,bar=g is not None,me=x)
		for r in j["rows"][len(w):]:bu(r)
	bA=104;cJ=Kit.MARGIN+30+Kit.GAP+bA+Kit.MARGIN
	def bB(name):
		W.close();w,h=b9,cJ;i,l=240,180
		if Kit.is_open(j["g"]):i,l=j["g"].GetX()+40,j["g"].GetY()+60
		g,c,m=W.begin(w,h,(i,l));Kit.add_window_frame(g,w,h);Kit.add_section(g,M,M,w-2*M,30);Kit.add_label(g,"PLAYER NOTE",M+30,M+7,Kit.HUE_TITLE);Kit.art_button(g,c,"close",Kit.ART_CLOSE,w-M-54,M+4,None,"Close without saving",on_click=k("note_close"));d=w-2*M;a=M+30+Kit.GAP;Kit.add_section(g,M,a,d,bA);b=M+12;e=b+max(Kit.text_w("Player:"),Kit.text_w("Note:"))+10;Kit.add_label(g,"Player:",b,a+13);n=af(name)if name else name;m["name"]=Kit.with_tip(Kit.add_textbox(g,n,e,a+10,200,numbers=False),"Player name as shown over their head (any case)");Kit.add_label(g,"Note:",b,a+43);m["text"]=Kit.with_tip(Kit.add_textbox(g,q.get(name.lower(),("",""))[1],e,a+40,M+d-12-e,numbers=False),"Your note (up to %d letters); saving it empty deletes it"%a4);f=a+72;Kit.art_button(g,c,"save",Kit.ART_OK,b,f,"Save","Save the note for every character of this account",on_click=k("note_save"));Kit.art_button(g,c,"delete",Kit.ART_CLOSE,b+35+Kit.text_w("Save")+16,f,"Delete","Delete this note",on_click=k("note_delete"));o="Kept per account";Kit.add_label(g,o,M+d-12-Kit.text_w(o),f+3,Kit.HUE_INFO);W.end(g,{"name":name,"shown":n})
	W=Kit.Window(L,C,None,J,bB,b8,cleanup=ac,lock=False,owner=False,clear={"c":{},"store":({},{})})
	def cK():
		c=J["c"]
		try:a=str(c["name"].Text or "")
		except Exception:a=J["name"]
		if a and a==J.get("shown"):a=J["name"]
		try:b=str(c["text"].Text or "")
		except Exception:b=""
		return a,b
	def am():a=j["c"].get("msg");return ""if a is None else str(a.Text or "").strip()
	def cL():
		b=j["c"].get("msg")
		if b is not None:b.SetText("")
		a["msg"].pop(d["tab"],None)
	bC={"psend":"PartyMsg","gsend":"GuildMsg","asend":"AllyMsg"}
	def cM(fn,txt):
		if not txt:f("type something first.");return
		getattr(API,fn)(txt);cL()
	def bD(serial):
		serial=int(serial or 0)
		if not serial:f("nothing targeted.");return
		if serial==u():f("that's you.");return
		m=API.FindMobile(serial)
		if m is None:f("target a player or creature in view.",Kit.HUE_BAD);return
		b=str(m.Name or "");c=b or "0x%08X"%serial
		if serial in[int(e)for e in API.GetAllFriends()or()]or any(g==serial for g,h in a["friends"]):f("%s is already a friend."%c)
		elif API.AddFriend(serial):
			if b:a["names"][serial]=b;a["names_dirty"]=True
			f("%s added to friends."%c,Kit.HUE_GOOD)
			if a["seen"]is not None:a["seen"]=a["seen"]|{serial}
		else:f("couldn't add %s to friends (the client refused)."%c,Kit.HUE_BAD)
		a["next_friends"]=0.
	def cN(serial):
		b=a["names"].get(serial,"")or "0x%08X"%serial
		if API.RemoveFriend(serial):f("%s removed from friends."%b)
		else:f("couldn't remove %s from friends (the client refused)."%b,Kit.HUE_BAD)
		if a["seen"]:a["seen"].discard(serial)
		a["next_friends"]=0.
	def cO(serial):
		if not serial:return
		if j["tab"]=="friends":cN(serial)
		elif j["tab"]=="party":
			b=a["party"]
			if b and b[0]and b[0]==u():
				if not CL.game_action("RequestPartyRemoveMember",[X(serial)],False):f("couldn't remove them (%s)."%CL.error,Kit.HUE_BAD)
			else:f("only the leader can remove members.")
	def bE():
		with Kit.quiet:
			import System;b=Typing._get(CL.world,"Party")if CL.world is not None else None
			if b is not None:Tz.put(b,"Inviter",System.UInt32(0))
		p=a["party"]
		if p:a["party"]=(p[0],0,p[2],p[3])
	def X(serial):
		try:import System;return System.UInt32(int(serial))
		except Exception:return serial
	bF={"paperdoll":("OpenPaperdoll",True,True),"status":("OpenStatusBar",False,True),"gwin":("OpenGuildGump",False,True),"invite":("RequestPartyInviteByTarget",False,False),"edit":("RequestProfile",True,False),"ignore":None}
	def cP(what):
		e=bF[what]
		if e is None:a=CL.open_ignore_list()
		else:a=CL.game_action(e[0],[X(u())]if e[1]else(),e[2])
		if not a:f("couldn't open that (%s)."%(CL.error or "no client access"),Kit.HUE_BAD)
		return a
	def cQ():
		a=CL.world
		if a is None:f("couldn't open the party window (no client access: %s)."%CL.error,Kit.HUE_BAD);return
		def b():import System;b=Typing._get(a,"Macros");c=b.GetType().Assembly;d,e,f=[c.GetType("ClassicUO."+h)for h in("Game.Managers.MacroObject","Common.Enums.MacroType","Common.Enums.MacroSubType")];g=System.Activator.CreateInstance(d,System.Array[object]([System.Enum.Parse(e,"Open",True),System.Enum.Parse(f,"PartyManifest",True)]));CL.call(b,"SetMacroToExecute",[g]);CL.call(b,"Update");return True
		if not CL.on_main(b):f("couldn't open the party window (%s)."%CL.error,Kit.HUE_BAD)
	def cR():
		a,b=ah()
		if not(a and z(b)in("guild","roster")):a=CL.find_server_gump(bj)[0]
		if not a:
			if not CL.game_action("OpenGuildGump"):f("couldn't ask for the guild window (%s)."%CL.error,Kit.HUE_BAD);return
			a,c,e=K(lambda a:z(a)in("guild","roster")and "ok")
		if not a:f("the guild window didn't come (are you in a guild?).",Kit.HUE_BAD);return
		if not R(a,Z,d["dbutton"]):f("no %s button found; press it in the guild window (or set its id in Social settings)."%Z)
	def cS(serial):
		if API.HasTarget("any")and not HOST.cursor_busy(L):
			if HOST.harm_ok(serial,"social.row",C):API.Target(serial)
			return
		API.SetLastTarget(X(serial));m=API.FindMobile(serial)
		if m is None:f("%s isn't in view."%(a["names"].get(serial,"")or "they"))
		else:f("%s is your last target."%(str(m.Name or "")or "that"))
	def bG():
		if a["guild_busy"]:return False
		a["guild_busy"]=True;a["guild_next"]=time.time()+a2;B.append(ct);return True
	def cT():
		b=a["inview"]
		if not(d["announce"]or d["left"])or a["seen"]is None:a["seen"]=b;return
		if d["announce"]:
			for s in b-a["seen"]:f("%s is in view."%U(s,"a friend"),Kit.HUE_GOOD)
		if d["left"]:
			for s in a["seen"]-b:f("%s left view."%U(s,"a friend"))
		a["seen"]=b
	def bH(action):
		b=a["party"]
		if not aA(b):f("not in a party.")
		elif action=="leave":
			if not CL.game_action("RequestPartyRemoveMember",[X(u())],False):f("couldn't leave (%s)."%CL.error,Kit.HUE_BAD)
		elif CL.game_action("RequestPartyLootState",[not b[2]],False):f("party %s loot your corpse."%("may not"if b[2]else "may"))
		else:f("couldn't change looting (%s)."%CL.error,Kit.HUE_BAD)
	def cU(action):
		b=X(a["party"][1])
		if action=="accept":
			def e():
				if not CL.game_action("RequestPartyAccept",[b],False):return
				bE();return True
			if CL.on_main(e)is None:f("couldn't accept (%s)."%CL.error,Kit.HUE_BAD)
			return
		c=G("ClassicUO.Network.AsyncNetClient");d=G("ClassicUO.Network.NetClientExt")
		def g():CL.call(None,"Send_PartyDecline",[Typing._get(None,"Socket",c),b],d);bE();return True
		if c is None or d is None or CL.on_main(g)is None:f("couldn't decline (%s)."%CL.error,Kit.HUE_BAD)
	def cV():
		i=H.index(d["gsort"])if d["gsort"]in H else 0;d["gsort"]=H[(i+1)%len(H)];ad();c=j["c"];b=c.get("gsort")
		if b is not None:Kit.set_text(b,bw(c))
		e=c.get("gsort_btn")
		if e is not None and c.get("gsort_bare"):Kit.with_tip(e,bo(c))
		a["page"]["guild"]=0;a["next_list"]=0.
	def cW():
		a["guild_said"]=""
		if bG():aK()
		else:f("already reading the guild window.")
	def cX(tab):
		if tab!=d["tab"]:a["msg"][d["tab"]]=am();d["tab"]=tab;ad();a["rebuild"]=True
	def cY(step):a["page"][d["tab"]]=max(0,a["page"].get(d["tab"],0)+step);a["next_list"]=0.
	def cZ(name):
		if str(name).startswith("0x"):f("name not known yet.")
		else:bB(name)
	def c_():f("target the friend to add.");HOST.pick_target(bX,lambda serial:k.add(("picked",int(serial or 0)),dup=True))
	def bI(action):
		if a["party"]and a["party"][1]:cU(action)
	def bJ(keep):
		if J["g"]is None:return
		a,b=cK()
		if cf(a,b if keep else ""):W.close()
	def c0(wanted,now,a):
		if not a:bf()
	def c1(wanted,now,c):b,d=T(a["friends"]);wanted.update(e for e,g in b)
	def c2(wanted,now,e):
		bf();b=a["party"]
		if not b:return
		c=u();d,f=T([g for g in b[3]if g!=c]);wanted.update(d);wanted.add(b[0]);wanted.add(b[1])
	def c3(wanted,now,e):
		ck()
		for s,f in a["allies"]:wanted.add(s)
		b=a["guild"]or E();c=a["view"]
		for m in b["members"]:
			s=c.get(aJ(m),0)
			if s:wanted.add(s)
		if(d["gevery"]and not a["guild_busy"]and now>=a["guild_next"]and now-b["at"]>=d["gevery"]*60):bG()
	bK={"mini":c0,"friends":c1,"party":c2,"guild":c3};bL={"click":cS,"rm":cO,"follow":lambda serial:Follow.toggle(serial,C),"noview":lambda name:f("%s isn't in view."%name),"picked":lambda serial:serial and bD(serial),"tab":cX,"page":cY,"note":cZ};bM={"pwin":cQ,"note_close":W.close,"gsort":cV,"grefresh":cW,"leave":lambda:bH("leave"),"loot":lambda:bH("loot"),"add_last":lambda:bD(int(API.LastTargetSerial or 0)),"add":c_,"accept":lambda:bI("accept"),"decline":lambda:bI("decline"),"diplo":lambda:B.append(cR),"war":lambda:API.SetWarMode(not API.Player.InWarMode),"note_save":lambda:bJ(True),"note_delete":lambda:bJ(False)};c4={"ldy":4,"fw":40,"ltip":True,"clamp":False}
	def c5(w):return(("WINDOW",(("note",l("Shift+click a row to note that player; %d saved for this account."%len(q),w-28)),("note",l("Action Bar cells can show this window (Client window, page 2).",w-28)),("check","bars","Show health bars","A bar for everyone in view; off, rows show name, status and distance"),("num","rows","Rows per page:","Rows on the Friends, Party and Guild tabs; the window grows to fit",None,aT,aU))),("FRIENDS  (journal lines)",(("check","announce","Say when a friend comes into view","One line when a friend comes into view (not those in view at start)"),("check","left","Say when a friend leaves view","One line when a friend in view is gone"))),("GUILD WINDOW  (for the Guild tab)",(("check","ghide","Read the guild window hidden","It opens invisible for the read; off, it shows for a few seconds",{"h":28}),("num","gevery","Read it again every:","Minutes between reads while the Guild tab shows (0-%d, 0 = only on Refresh)"%au,"min",0,au),("num","dbutton","Diplomacy button id:","Pressed when the Diplomacy caption isn't found; ServUO uses %d (0-%d, 0 = caption only)"%(ap,aq),None,0,aq)),{"pad":8}))
	def c6(old,new):
		if(new["bars"],new["rows"])!=(old["bars"],old["rows"])or(new["ghide"]!=old["ghide"]and old["tab"]=="guild"):a["rebuild"]=True
		if(new["announce"]or new["left"])and not(old["announce"]or old["left"]):a["seen"]=None
	an=Kit.Page(d,c5,ad,c6,c4);ao=[0];a6();ao[0]=u()
	def c7():
		a.update({"shutting":False,"docked":False,"queue":[],"page":{},"mobs":{},"inview":set(),"seen":None,"next_list":0.,"next_friends":0.,"next_profile":0.,"guild_busy":False,"guild_dirty":False,"guild_next":0.,"guild_fails":0,"guild_said":"","guild_pages":0,"ghid":0,"view":{},"view_serials":None,"allies":[],"fit":None,"me_s":0,"friends_raw":None,"kept":{},"prof_part":False,"again_for":None,"again_build":False,"minimized":F.start_min()});del B[:]
		if not(ao[0]and ao[0]==u()):a6()
		ao[0]=0;CL.find();b=HOST.layout_slot(L)if HOST.booting()else None
		if b and b[0]and b[1]:a["fit"]=(int(b[0]),int(b[1]))
		aD();F.dock(cv,exact=True,verify=True,min=bn);ac.service("social.note",ce)
	def c8():
		if j["g"]is None:return
		if Kit.closed(j):return
		q=a["queue"]
		while q:
			b=q.pop(0);l=b[0]if isinstance(b,tuple)else b
			if b=="to_bar"or(b=="toggle_min"and not a["minimized"]):a["msg"][d["tab"]]=am()
			if b=="redraw":a["rebuild"]=True;continue
			if F.action(b):continue
			if l in bL:bL[l](b[1]);continue
			if b in bM:bM[b]();continue
			if b in bC:cM(bC[b],am());continue
			if b in bF and cP(b)and b=="invite":f("target who to invite.")
		if a["rebuild"]:
			if not a["minimized"]:a["msg"][d["tab"]]=am()
			aD();return
		if a["guild_dirty"]:a["guild_dirty"]=False;a["next_list"]=0.
		e=time.time()
		if e<a["next_list"]<=e+aY:return
		h=a["minimized"]and a["docked"]
		if h and not(d["announce"]or d["left"]):a["seen"]=None;return
		a["next_list"]=e+aY;cj();c="mini"if a["minimized"]else j["tab"];m=set();a["view_serials"]=None
		if c in bK:bK[c](m,e,h)
		if c in("guild","profile"):bg(c=="profile")
		g={};n=a["kept"]if c=="guild"else None
		for s in m:
			if not s:continue
			i=n.get(s)if n else None
			if i is not None:g[s]=(i[0],0,0,i[1],False,None);continue
			o=bd(s)
			if o is not None:g[s]=o
		a["mobs"]=g;k=set();p=[]
		for s in a["fserials"]:
			if s in g:k.add(s)
			else:p.append(s)
		if c=="friends"or(c=="mini"and not h)or d["announce"]or d["left"]:k|=cl(p)
		a["inview"]=k;cT();aK()
	def c9():
		while B and not a["shutting"]:B.pop(0)()
	def da():a["shutting"]=True;ad();a["names_dirty"]=True;ay();a9();ac.close()
	return{"start":c7,"tick":c8,"stop":da,"client_tick":True,"config_height":an.height,"build_config":an.build,"poll_config":an.poll,"config_closed":an.closed,"thread_tick":c9,"thread_wanted":lambda:bool(B)}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("social","Social","Friends, party, guild and profile",_module_social,.1,category="The world")
