def _module_prices():
	P=Client.flags;ap=Follow.current;aq=HOST.hotkey_off;ar=HOST.pack_ver;at=HOST.refresh_settings;v="prices";z="Reagent Prices";au="ReagentPrices_settings";bc="ReagentPrices_pos";bd="ReagentPrices_min";av=420;u=22;be=(340,46);bf=3962;ab={"dist":(5,60),"old":(1,60)};bg=.5;bh=10.;bi=3.;ac=5.;bj=10;bk=400;ad=24;j=("SS","NS","BP","GA","SA","BM","GI","MR");aw=dict((Kit.REAGENTS[cJ][1],cJ)for cJ in j);ax=("Castle British","Delucia","East Britain","Jhelom","Magincia","Moonglow","Moonglow 2","Moonglow/Papua","Ocllo","Serpent's Hold","Skara Brae","Trinsic","Upper W Britain","Vesper","West Britain","Yew Abbey");Q="ReagentPrices_data.txt";bl=("P","V","R","H");bm="New shop";bn=30.;ay="ClassicUO.Game.Managers.UIManager";bo=(("ClassicUO.Game.UI.Gumps.ShopGump","IsBuyGump"),("ClassicUO.Game.UI.Gumps.ModernShopGump","isPurchaseGump"));bp=(26,27);ae=((60,1,"just now"),(3600,60,"%d min ago"),(86400,3600,"%d h ago"),(0,86400,"%d d ago"));I=36;af=28;R=34;az=36;aA="ReagentPrices_book";bq="ClassicUO.Game.UI.Gumps.ModernBookGump";aB="Reagent Prices";br=1;aC=147;C=18;F=8;bs=4;bt=1.;bu=1;bv=3000;bw=15;S=86400;bx=3;aD={"SS":"Silk","NS":"Shade","BP":"Pearl","GA":"Garlic","SA":"Ash","BM":"Moss","GI":"Ginseng","MR":"Mandrake"};by=(("SS","NS"),("BP","GA"),("SA","BM"),("GI","MR"));bz=("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");ag=8;bA=("mage","alchemist","herbalist");bB="Buy";bC=3;bD=1;bE=.6;bF=.5;aE="ReagentPrices_keep";ah=9999;A=tuple("keep_"+cK for cK in j);aF=("hk",);ai=3;aj=30+(ai+1)*u+6;ab.update((cL,(0,ah))for cL in A);aG=30;bG="Upper W Britain";bH="99^ (999)";aH=28;bI="ALL SHOPS  (price, stock; ^ up, v down)";bJ="Switch between the cheapest list and every shop";aI="ReagentPrices_log.csv";ak=5000;bK="time,shop,reagent,price,stock";bL=("Open the nearest reagent vendor's buy list (within %d tiles). Alt+click: auto-follow (again to stop)"%ag);e={"say":True,"dist":20,"book_open":True,"book_head":True,"old":7,"hk":"","skip_old":False,"grid":False,"keep_SS":0,"keep_NS":0,"keep_BP":0,"keep_GA":0,"keep_SA":0,"keep_BM":0,"keep_GI":0,"keep_MR":0};bM=dict(e);b={"minimized":False,"shutting":False,"docked":False,"queue":[],"loaded":False,"seen":None,"check_at":0.,"aged_at":0.,"save_at":0.,"ask":None,"warned":set(),"load_fails":0,"book":None,"book_serial":0,"bookver":0,"foreign":None,"ok_books":set(),"picking":None,"jobs":[],"have":None,"here":None,"hooked":None,"menu":False,"followed":None,"hk_at":0.,"pv":None,"logq":[],"log_at":0.,"log_fails":0};J={"g":None,"c":{},"store":({},{})};d={"shops":{},"vendors":{},"reads":{},"hist":{},"dirty":{},"marks":0};h={};T={};o={"tb":{},"typed":{},"n":0};aJ,p,i=Kit.basics(b,z);aK={"text":Kit.read_merge(Kit.data_path(Q)),"at":time.time()}
	def bN():
		Kit.kv_load(au,"|",e,ab,aF)
		try:b["book_serial"]=int(Kit.get_var(aA,"")or "0",16)
		except ValueError:b["book_serial"]=0
		e.update((f,0)for f in A)
		for c in Kit.get_var(aE,"").split(","):
			a,d,n=c.partition(":")
			if a not in j:continue
			try:e["keep_"+a]=max(0,min(ah,int(n)))
			except ValueError:continue
	def al():Kit.kv_save(au,"|",e,[a for a in sorted(bM)if a not in A],ab,aF);Kit.put_var(aE,",".join("%s:%d"%(c,e["keep_"+c])for c in j if e["keep_"+c]))
	def D(what):
		if what not in b["warned"]:b["warned"].add(what);i("couldn't reach the client's %s (TazUO changed)."%what,Kit.HUE_BAD)
	def aL(t):
		if "gg"not in h:h["gg"]=[a for a in Tz.T(ay).GetMethods(P(static=True))if a.Name=="GetGump"and a.IsGenericMethodDefinition][0]
		return h["gg"].MakeGenericMethod(t)
	def bO():
		if h.get("shop")is None:
			if "shop"in h:return
			h["shop"]=None
			try:
				import System;b=[]
				for c,a in bo:
					t=Tz.T(c)
					if not Tz.has(t,a,P()):raise Exception("no %s"%a)
					b.append((aL(t),a))
				h["none"]=System.Array[object]([None]);h["shop"]=b
			except Exception:D("shop list");return
		try:
			for d,a in h["shop"]:
				g=d.Invoke(None,h["none"])
				if g is not None and not g.IsDisposed and Tz.get(g,a):return g,int(g.LocalSerial)
		except Exception:pass
		return
	def bP(serial):
		if h.get("mobs")is None:
			if "mobs"in h:return
			h["mobs"]=None
			try:
				import System;b=Typing._get(API,"World")
				if b is None:b=Tz.get(Tz.get(Tz.get(None,"Game",Tz.T("ClassicUO.Client")),"UO"),"World")
				g=Tz.T("ClassicUO.Game.Data.Layer");h["layers"]=[System.Enum.ToObject(g,m)for m in bp];h["u32"]=System.UInt32;h["mobs"]=Tz.get(b,"Mobiles")
			except Exception:D("shop list");return
		try:
			c=h["mobs"];d=h["u32"](serial)
			if not c.ContainsKey(d):return
			i=c[d];e=[]
			for j in h["layers"]:
				f=i.FindItemByLayer(j);a=f.Items if f is not None else None
				for k in range(bk):
					if a is None:break
					e.append((int(a.Graphic),int(a.Price),int(a.Amount)));a=a.Next
			return e
		except Exception:return
	def aM():
		if h.get("book")is None:
			if "book"in h:return
			h["book"]=None
			try:
				import System;a=Tz.T(bq);b=P();c=P(static=True);d=Tz.T("ClassicUO.Network.NetClientExt");f=Tz.T("ClassicUO.Network.AsyncNetClient");g=Tz.get(Tz.get(None,"Game",Tz.T("ClassicUO.Client")),"UO");e={"get":aL(a),"lines":a.GetProperty("BookLines",b),"redraw":a.GetMethod("ServerSetBookText",b),"title":a.GetField("_titleTextBox",b),"author":a.GetField("_authorTextBox",b),"page":d.GetMethod("Send_BookPageData",c),"head":d.GetMethod("Send_BookHeaderChanged",c),"head_old":d.GetMethod("Send_BookHeaderChanged_Old",c),"socket":f.GetProperty("Socket",c),"focus":Tz.T(ay).GetProperty("KeyboardFocusControl",c),"ctl":Tz.T("ClassicUO.Game.UI.Controls.Control"),"root":Tz.T("ClassicUO.Game.UI.Controls.Control").GetProperty("RootParent",b),"fonts":Tz.get(Tz.get(g,"FileManager"),"Fonts"),"u32":System.UInt32,"objs":System.Array[object],"strs":System.Array[System.String]}
				if any(m is None for m in e.values()):raise Exception("no book member")
				h["book"]=e
			except Exception:D("book");return
		return h["book"]
	def bQ(serial):
		b=aM()
		if b is None:return
		try:g=b["get"].Invoke(None,b["objs"]([b["u32"](serial)]))
		except Exception:
			h["fails"]=h.get("fails",0)+1
			if h["fails"]>=bx:h["book"]=None;D("book")
			return
		h["fails"]=0;return g if g is not None and not g.IsDisposed else None
	def bR(g):
		b=h["book"]
		try:a=b["focus"].GetValue(None);return{"pages":int(g.BookPageCount),"known":set(int(c)for c in g.KnownPages),"edit":bool(g.IsEditable),"lines":[str(f or "").rstrip("\n")for f in b["lines"].GetValue(g)],"new":bool(g.UseNewHeader),"title":str(b["title"].GetValue(g).Text or ""),"author":str(b["author"].GetValue(g).Text or ""),"typing":a is not None and(a is g or b["ctl"].IsInstanceOfType(a)and b["root"].GetValue(a)is g)}
		except Exception:D("book");return
	def bS(g,serial,pages,head):
		b=h["book"]
		try:
			a=b["socket"].GetValue(None);e=b["lines"].GetValue(g);u=b["u32"](serial)
			if head is not None:b["head"if head[2]else "head_old"].Invoke(None,b["objs"]([a,u,head[0],head[1]]));g.SetTile(head[0],True);g.SetAuthor(head[1],True)
			for c,d in pages:
				b["page"].Invoke(None,b["objs"]([a,u,b["strs"](d),c]))
				for i,f in enumerate(d):e[(c-1)*F+i]=f
			if pages:b["redraw"].Invoke(g,None)
			return True
		except Exception:D("book");return False
	def bT(text):
		b=aM()
		try:return int(b["fonts"].GetWidthUnicode(br,text))
		except Exception:D("book");raise
	def bU(items):
		b={}
		for f,a,e in items:
			c=aw.get(f)
			if c is None or a<=0 or e<=0:continue
			d=b.get(c)
			if d is None or a<d[0]:b[c]=(a,e)
			elif a==d[0]:b[c]=(a,d[1]+e)
		return b
	def aN(fields):
		try:return tuple(int(a)for a in fields)if len(fields)==3 else None
		except ValueError:return
	def aO(spot):return[str(a)for a in spot]if spot else["","",""]
	def aP(text):
		a={"shops":{},"vendors":{},"reads":{},"hist":{}}
		for c in(text or "").split("\n"):
			f=c.rstrip("\r").split("|")
			try:
				if f[0]=="P":a["shops"][int(f[1])]={"name":f[2],"order":int(f[3]),"spot":aN(f[4:7]),"tail":f[7:]}
				elif f[0]=="V":a["vendors"][int(f[1],16)]={"shop":int(f[2]),"spot":aN(f[3:6]),"tail":f[6:]}
				elif f[0]=="R":
					p={}
					for b in f[3].split(","):
						if b:d,e,g=b.split(":")[:3];p[d]=(int(e),int(g))
					a["reads"][int(f[1],16)]={"t":int(f[2]),"p":p,"tail":f[4:]}
				elif f[0]=="H":h=[tuple(int(n)for n in m.split(":")[:3])for m in f[3].split(";")if m];a["hist"][(int(f[1]),f[2])]={"rows":[t for t in h if len(t)==3],"tail":f[4:]}
			except(IndexError,ValueError):continue
		return a
	def bV(key):
		f=key.split("|");b=f[0]
		if b=="P":e=d["shops"].get(int(f[1]));a=e and[e["name"],str(e["order"])]+aO(e["spot"])
		elif b=="V":e=d["vendors"].get(int(f[1],16));a=e and[str(e["shop"])]+aO(e["spot"])
		elif b=="R":e=d["reads"].get(int(f[1],16));a=e and[str(e["t"]),",".join("%s:%d:%d"%(g,c[0],c[1])for g,c in sorted(e["p"].items()))]
		else:e=d["hist"].get((int(f[1]),f[2]));a=e and[";".join("%d:%d:%d"%m for m in e["rows"])]
		return None if e is None else "|".join([key]+a+e["tail"])
	def bW(line):f=line.split("|");n=3 if f[0]=="H"else 2;return "|".join(f[:n])if f[0]in bl and len(f)>n else None
	def q(key):d["dirty"][key]=True;d["marks"]+=1
	def aQ(a):d.update(a);p.add("show")
	def aR(text=None):
		if text is None:text=Kit.read_merge(Kit.data_path(Q))
		if text is None:
			b["save_at"]=time.time()+ac;b["load_fails"]+=1
			if b["load_fails"]==2:i("couldn't read %s (trying again)."%Q,Kit.HUE_BAD)
			return
		c=aP(text)
		if not text.strip():
			for a,d in enumerate(ax):c["shops"][a+1]={"name":d,"order":a+1,"spot":None,"tail":[]};q("P|%d"%(a+1))
		b["loaded"]=True;b["bookver"]+=1;aQ(c)
	def aS():
		c=list(d["dirty"]);e=dict((g,bV(g))for g in c);f=d["marks"]
		try:a=Kit.merge_save(Kit.data_path(Q),e,bW)
		except Exception:a=None
		if a is None:b["save_at"]=time.time()+ac;return
		if d["marks"]!=f:return
		for k in c:d["dirty"].pop(k,None)
		aQ(aP("\n".join(a)))
	def H():return sorted(d["shops"],key=lambda sid:(d["shops"][sid]["order"],sid))
	def l(sid):return d["shops"][sid]["name"]if sid in d["shops"]else "?"
	def s(serial):v=d["vendors"].get(serial);return v["shop"]if v is not None and v["shop"]in d["shops"]else None
	def K(now=None):
		f={};g=e["old"]*S if now is not None and e["skip_old"]else None
		for j,a in d["reads"].items():
			h=s(j)
			if h is None or g is not None and now-a["t"]>g:continue
			b=f.setdefault(h,{})
			for c,(i,k)in a["p"].items():
				if c not in b or i<b[c][0]:b[c]=(i,k,a["t"])
		return f
	def E(prices):
		c=d["shops"];a={}
		for e,h in prices.items():
			for f,g in h.items():
				b=a.get(f)
				if b is None or(g[0],c[e]["order"])<(b[1][0],c[b[0]]["order"]):a[f]=(e,g)
		return a
	def U(n):return "{:,}".format(int(n))
	def bX():
		a,c=b["here"],b["ask"]
		if a is None:return
		if c is not None and c["mode"]=="read"and c["serial"]==a:return None,c["pend"]["p"]
		e=d["reads"].get(a);return s(a),(e["p"]if e else{})
	def aT(prices):
		g=dict((r,e["keep_"+r])for r in j if e["keep_"+r]>0);m=b["have"]or{};f=dict((t,max(0,w-m.get(t,0)))for t,w in g.items())if g else dict((x,1)for x in j);c=[y for y in j if f.get(y)];h=[]
		for i,a in(prices.items()if c else()):k=[G for G in c if G not in a];l=[M for M in c if M in a and a[M][1]<f[M]];n=sum(a[cJ][0]*min(f[cJ],a[cJ][1])for cJ in c if cJ in a);h.append((len(k)+len(l),n,d["shops"][i]["order"],i,k,l))
		h.sort();return f,bool(g),c,h[:ai]
	def aU(r):return "; ".join((["no "+", ".join(r[4])]if r[4]else[])+(["short "+", ".join(r[5])]if r[5]else[]))
	def bY(prices,hv,want,f,need):
		if not f:return "For 1 of each reagent; set a shopping list in Settings"
		if not need:return "Your list: nothing to buy"
		b=E(prices);d=[m for m in need if m not in b];c="%s at the cheapest"%U(sum(want[n]*b[n][1][0]for n in need if n in b))
		if hv is not None:a=hv[1];e=[r for r in need if r not in a or a[r][1]<want[r]];g=U(sum(min(want[t],a[t][1])*a[t][0]for t in need if t in a));c="%s here%s, %s"%(g," (short %s)"%", ".join(e)if e else "",c)
		return "Your list: "+c+("; no price for %s"%", ".join(d)if d else "")
	def L():
		a=None
		for b,c in d["reads"].items():
			if s(b)is not None and(a is None or c["t"]>d["reads"][a]["t"]):a=b
		return a
	def bZ():a=set(s(c)for c in d["reads"]);b=H();return next((f for f,g in enumerate(b)if g not in a),0)
	def aV():a=b["ask"];return(a and a["mode"],bool(a and a["new"]),L()is not None,b["foreign"]is not None,any(e[c]for c in A),e["grid"],len(d["shops"]))
	def aW():a=b["ask"];c=Kit.GAP+az if b["foreign"]is not None else 0;return(c+((Kit.GAP+I+(af if a["new"]else 0))if a else 0)+(0 if e["grid"]else Kit.GAP+aj))
	def V(n=1):a=u+n*u if e["grid"]else len(j)*u;return 2*Kit.MARGIN+30+Kit.GAP+30+a+6+Kit.GAP+R+aW()
	def aX():return Kit.text_w(bG)+8,Kit.text_w(bH)+8
	def aY():
		if not e["grid"]:return av,V()
		a,b=aX();return max(av,2*Kit.MARGIN+16+a+len(j)*b),V(1)
	def b_(sid,code,row):
		h=d["hist"].get((sid,code));a=[c for c in h["rows"]if c[0]<row[2]]if h else[]
		if not a:return ""
		return "^"if row[0]>a[-1][1]else "v"if row[0]<a[-1][1]else ""
	def b0(g,store,c,M,y,IW,a):
		Kit.add_section(g,M,y,IW,I+(af if a["new"]else 0));x=M+IW-8;i=("Skip","Drop this read")if a["mode"]=="read"else("Cancel","Keep this vendor's shop")
		for e,j,f,k in(("ask_skip",Kit.ART_CLOSE)+i,("ask_ok",Kit.ART_OK,"OK","Link this vendor to the picked shop")):x-=35+Kit.text_w(f);Kit.art_button(g,store,e,j,x,y+6,f,k,on_click=p(e));x-=10
		Kit.add_label(g,"Which shop?",M+8,y+10);b=M+16+Kit.text_w("Which shop?");h=c["ask_ids"]=H();m=[l(r)for r in h]+[bm]
		if a["new"]:Kit.add_label(g,"Name:",M+8,y+I+2);n=Kit.add_textbox(g,"",b,y+I,x-b,numbers=False);c["ask_name"]=Kit.with_tip(n,"Name of the new shop (up to %d letters)"%ad)
		d=G.CreateDropDown(x-b,m,max(0,min(a["pick"],len(h))));d.SetPos(b,y+6);g.Add(d);c["ask_dd"]=Kit.with_tip(d,"Shop this vendor is in")
	def b1(g,store,M,y,IW):Kit.add_section(g,M,y,IW,az);x=M+IW-8-35-Kit.text_w("Overwrite");Kit.art_button(g,store,"overwrite",Kit.ART_OK,x,y+6,"Overwrite","Write the prices over this book's text (this book only)",on_click=p("overwrite"));Kit.add_label(g,Kit.fit("The book holds other writing",x-M-18),M+8,y+10,Kit.HUE_BAD)
	def b2(g,c,M,y,IW,sh,n):
		Kit.add_section(g,M,y,IW,sh,bI);b,a=aX();a=max(a,(IW-16-b)//len(j));d=M+8+b;c["name_w"]=b-8;c["cell_w"]=a-4
		for i,e in enumerate(j):Kit.add_label(g,e,d+i*a,y+30,Kit.HUE_TITLE)
		c["grid"]=[(Kit.add_label(g,"",M+8,y+30+(f+1)*u),[Kit.add_label(g,"",d+m*a,y+30+(f+1)*u)for m in range(len(j))])for f in range(n)]
	def W():
		t,n=aY();z=B.zone_slot(t,n);k=e["grid"];o=0
		if k:v=max(1,min(aG,len(d["shops"])));o=min(aG,B.rows(u,V(0),v))if z else v;n=V(o)
		w,l=z if z else(t,n);g,q,c=B.begin(w,l);c["shape"]=aV()
		if not b["minimized"]:
			B.frame(g,extra=[("buy",Kit.ART_PLAY,"Buy list",bL,cy),("view",Kit.ART_PAGE,"View: grid"if k else "View: cheapest",bJ,p("view"))]);M=Kit.MARGIN;a=w-2*M;y=M+30+Kit.GAP;m=b["ask"];x=c["shape"][4];r=Kit.GAP+R+aW()
			if k:b2(g,c,M,y,a,l-M-r-y,o)
			else:
				Kit.add_section(g,M,y,a,l-M-r-y,"CHEAPEST");A=M+34;C=A+max(Kit.text_w(Kit.REAGENTS[cJ][0])for cJ in j)+10;i=C+Kit.text_w("9999")+10;D=i+(Kit.text_w("buy 9999")+10 if x else 0);E=M+a-8-Kit.text_w("59 min ago");c["shop_w"]=E-8-D;c["rows"]=[]
				for H,F in enumerate(j):h=y+30+H*u;J,K=Kit.REAGENTS[F];s=G.CreateGumpItemPic(K,20,20);s.SetPos(M+8,h-2);Kit.inert(s);g.Add(s);Kit.add_label(g,J,A,h);c["rows"].append((F,Kit.add_label(g,"",C,h),Kit.add_label(g,"",D,h),Kit.add_label(g,"",E,h,Kit.HUE_INFO),Kit.add_label(g,"",i,h,Kit.HUE_INFO)if x else None))
			f=l-M-r+Kit.GAP;Kit.add_section(g,M,f,a,R);c["line_w"]=a-16
			if m is None and L()is not None:i=M+a-8-35-Kit.text_w("Change");c["line_w"]=i-6-M-8;Kit.art_button(g,q,"change",Kit.ART_PAGE,i,f+4,"Change","Pick another shop for the last vendor read",on_click=p("change"))
			c["line"]=Kit.add_label(g,"",M+8,f+9,Kit.HUE_INFO);f+=R+Kit.GAP
			if m is not None:b0(g,q,c,M,f,a,m);f+=I+(af if m["new"]else 0)+Kit.GAP
			if not k:Kit.add_section(g,M,f,a,aj,"BEST STOPS");c["stops_w"]=a-16;c["stops"]=[Kit.add_label(g,"",M+8,f+30+cK*u,Kit.HUE_INFO)for cK in range(ai+1)];f+=aj+Kit.GAP
			if b["foreign"]is not None:b1(g,q,M,f,a)
		B.end(g);am()
	B=Kit.Window(v,z,b,J,W,bc,bd,mini=be,icon=bf,cleanup=aJ)
	def b3(c,prices,pool,hv,want,now):
		m=E(dict((r,t)for r,t in pool.items()if r!=hv[0])if hv else pool);n=E(prices);o=e["old"]*S
		for b,f,g,h,j in c["rows"]:
			a=m.get(b)
			if j is not None:Kit.set_text(j,"buy %d"%want[b]if b in want else "",Kit.HUE_TEXT if want.get(b)else Kit.HUE_INFO)
			if hv is not None:d=hv[1].get(b);p=d is not None and(a is None or d[0]<=a[1][0]);Kit.set_text(f,"out"if d is None else str(d[0]),Kit.HUE_GOOD if p else Kit.HUE_INFO if d is None else Kit.HUE_TEXT);Kit.set_text(g,Kit.fit("best %d %s"%(a[1][0],l(a[0]))if a else "no other shop",c["shop_w"]),Kit.HUE_INFO);Kit.set_text(h,Kit.ago(now-a[1][2],ae)if a else "",Kit.HUE_INFO);continue
			if a is None:Kit.set_text(f,"-",Kit.HUE_INFO);Kit.set_text(g,"Only old prices"if b in n else "No price yet",Kit.HUE_INFO);Kit.set_text(h,"");continue
			q,i=a;k=Kit.HUE_INFO if now-i[2]>o else Kit.HUE_TEXT;Kit.set_text(f,str(i[0]),k);Kit.set_text(g,Kit.fit(l(q),c["shop_w"]),k);Kit.set_text(h,Kit.ago(now-i[2],ae),Kit.HUE_INFO)
	def b4(c,prices,pool,now):
		k=E(pool);b=H();i=c["grid"];m=len(b)-len(i)+1;p=e["old"]*S
		for d,(n,q)in enumerate(i):
			f=b[d]if d<len(b)and(m<=1 or d<len(i)-1)else None;g=prices.get(f)
			if f is None:Kit.set_text(n,"+%d more shops"%m if d<len(b)else "",Kit.HUE_INFO)
			else:Kit.set_text(n,Kit.fit(l(f),c["name_w"]),Kit.HUE_INFO if g is None else Kit.HUE_TEXT)
			for h,o in zip(j,q):
				a=g.get(h)if g else None
				if a is None:Kit.set_text(o,"-"if g is not None else "",Kit.HUE_INFO);continue
				r=now-a[2]>p;s=h in k and a[0]<=k[h][1][0];Kit.set_text(o,Kit.fit("%d%s (%d)"%(a[0],b_(f,h,a),a[1]),c["cell_w"]),Kit.HUE_INFO if r else Kit.HUE_GOOD if s else Kit.HUE_TEXT)
	def am():
		c=J["c"];e=time.time();f=L()
		if f is None:a="no reads yet"
		else:a="read %s %s"%(l(s(f)),Kit.ago(e-d["reads"][f]["t"],ae))
		if b["foreign"]is not None:a="book holds other writing; Restore to overwrite"
		if b["ask"]is not None:a="which shop? Restore to pick"
		if "status"in c:Kit.set_text(c["status"],"%s: %s"%(z,a))
		elif "line"in c:
			m=K();g=K(e);n=bX();o,q,p,h=aT(g)
			if "grid"in c:b4(c,m,g,e)
			else:b3(c,m,g,n,o,e)
			if b["ask"]is not None:j="Which shop is this vendor in? Pick it below"
			elif f is None:j="No reads yet: open a reagent vendor's buy list"
			else:j="Last %s"%a
			Kit.set_text(c["line"],Kit.fit(j,c["line_w"]),Kit.HUE_INFO)
			if "stops"not in c:return
			k=[bY(g,n,o,q,p)]+["%d %s %s%s"%(x+1,l(w[3]),U(w[1]),": "+aU(w)if w[0]else "")for x,w in enumerate(h)]
			if p and not h:k.append("No prices yet")
			for i,t in enumerate(c["stops"]):r=h[i-1]if 0<i<=len(h)else None;Kit.set_text(t,Kit.fit(k[i]if i<len(k)else "",c["stops_w"]),Kit.HUE_TEXT if r is not None and not r[0]else Kit.HUE_INFO)
	def k():
		if o["tb"]and o["n"]!=len(d["shops"]):ao();o["n"]=len(d["shops"]);at(v)
		if not b["minimized"]and J["c"].get("shape")!=aV():W()
		else:am()
	def aZ(mode,serial,pend,pick):
		b["ask"]={"mode":mode,"serial":serial,"pend":pend,"pick":pick,"new":False};k()
		if b["minimized"]:i("which shop is this vendor in? Restore the window to pick.")
	def a_(sid,code,row):h=d["hist"].setdefault((sid,code),{"rows":[],"tail":[]});h["rows"].append(row);h["rows"].sort();del h["rows"][:-bj];q("H|%d|%s"%(sid,code))
	def a0(serial,sid,spot,picked=False):
		a=d["vendors"].get(serial)or{"spot":None,"tail":[]};d["vendors"][serial]={"shop":sid,"spot":spot or a["spot"],"tail":a["tail"]};q("V|%X"%serial)
		if picked and(spot or a["spot"]):d["shops"][sid]["spot"]=spot or a["spot"];q("P|%d"%sid)
	def b5(spot):
		b,c=None,e["dist"]+1;f=[(n,m["spot"])for n,m in d["shops"].items()if m["spot"]];f+=[(r["shop"],r["spot"])for r in d["vendors"].values()if r["spot"]and r["shop"]in d["shops"]]
		for h,a in(f if spot else()):
			g=max(abs(a[1]-spot[1]),abs(a[2]-spot[2]))
			if a[0]==spot[0]and g<c:b,c=h,g
		return b
	def a1(pend,sid,picked=False):
		a,t=pend["serial"],pend["t"];a0(a,sid,pend["spot"],picked);h=d["reads"].get(a)or{"tail":[]};d["reads"][a]={"t":t,"p":dict(pend["p"]),"tail":h["tail"]};q("R|%X"%a)
		for m,(n,o)in pend["p"].items():a_(sid,m,(t,n,o))
		b6(pend,sid)
		if e["say"]:c=K(time.time());p=E(c);f=c.get(sid,{});g=[r for r in j if r in f and f[r][0]==p[r][1][0]];i("%s read%s."%(l(sid),"; cheapest for "+", ".join(g)if g else ""),Kit.HUE_GOOD)
		b["bookver"]+=1;k()
	def b6(pend,sid):
		a=l(sid);c=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(pend["t"]));q=b["logq"]
		if ","in a or '"'in a:a='"%s"'%a.replace('"','""')
		q.extend("%s,%s,%s,%s,%d"%(c,a,Kit.REAGENTS[f][0],pend["p"][f][0]if f in pend["p"]else "",pend["p"][f][1]if f in pend["p"]else 0)for f in j)
		if len(q)>ak:del q[:-ak]
	def a2():
		a=b["log_lock"]
		if not a.acquire(False):return
		try:c=b7()
		finally:a.release()
		if not c:
			b["log_at"]=time.time()+ac;b["log_fails"]+=1
			if b["log_fails"]==2:i("couldn't write %s (trying again)."%aI,Kit.HUE_BAD)
			return
		b["log_fails"]=0
	def b7():
		q=b["logq"];n=len(q);c=Kit.data_path(aI);d=Kit.read_safe(c)
		if d is None:return False
		a=[f for f in d.replace("\r","").split("\n")if f.strip()];a=(a[1:]if a and a[0].lower().startswith("time,")else a)+q[:n]
		try:Kit.write_safe(c,"\n".join([bK]+a[-ak:])+"\n")
		except Exception:return False
		del q[:n];return True
	def b8(serial,now,got):
		b=d["reads"].get(serial)
		if b is not None and now-b["t"]<bi and b["p"]==got:return
		c=API.FindMobile(serial);e=(int(API.GetMap()),int(c.X),int(c.Y))if c else None;f={"serial":serial,"t":int(now),"p":got,"spot":e};a=s(serial)
		if a is None:a=b5(e)
		if a is None:aZ("read",serial,f,bZ())
		else:a1(f,a)
	def b9(now):
		d=b["ask"];a=bO()
		if d is not None and d["mode"]=="read"and(a is None or a[1]==d["serial"]):return
		if a is None:
			b["seen"]=None
			if b["here"]is not None:b["here"]=None;O();k()
			return
		if b["seen"]is a[0]:
			e=ar()
			if b["here"]is not None and e!=b["pv"]:b["pv"]=e;O()
			return
		c=bP(a[1])
		if c is not None and max([g[1]for g in c]or[0])<=0:return
		b["seen"]=a[0]
		if c is None:return
		f=bU(c)
		if f or s(a[1])is not None:b["here"],b["pv"]=a[1],ar();O();b8(a[1],now,f);k()
		elif b["here"]is not None:b["here"]=None;k()
	def a3(text):
		w=T.get(text)
		if w is None:
			if len(T)>=bv:T.clear()
			w=T[text]=bT(text)
		return w
	def N(head,tail="",end=""):
		a=head+tail+end
		while a3(a)>aC:
			if tail:tail=tail[:-1].rstrip();a=head+tail+".."+end
			elif end:end=end[:-1];a=head+end
			else:head=head[:-1];a=head
		return a
	def a4(t):a=time.localtime(t);return "%d %s %02d:%02d"%(a.tm_mday,bz[a.tm_mon-1],a.tm_hour,a.tm_min)
	def ca(now):
		m=K();n=K(now);g=E(n);u=E(m);v=e["old"]*S;c={}
		for w,x in d["reads"].items():
			a=s(w)
			if a is not None:c[a]=max(c.get(a,0),x["t"])
		def o(row):return "%d%s"%(row[0],"*"if now-row[2]>v else "")
		b=[[N("%s %s "%(G,o(g[G][1])),l(g[G][0]))if G in g else "%s - (old)"%G if G in u else "%s - (no read)"%G for G in j]];B,y,A,h=aT(n);i=["Best stops","For: your list"if y else "For: 1 of each"]
		if not h:i.append("No prices yet"if A else "Nothing to buy")
		i+=[N("%d "%(cJ+1),l(M[3])," "+U(M[1]))for cJ,M in enumerate(h)];b.append(i+[N("",l(cK[3]),": "+aU(cK))for cK in h if cK[0]])
		for a in H()[:C-2]:
			p=m.get(a,{});f=[N("",l(a))]
			if a not in c:f.append("Not read yet")
			else:
				f.append("Read "+a4(c[a]))
				for k,z in by:q,r=[o(p[cL])if cL in p else "out"for cL in(k,z)];t="%s %s  %s %s"%(aD[k],q,aD[z],r);f.append(N("",t if a3(t)<=aC else "%s %s  %s %s"%(k,q,z,r)))
			b.append(f)
		b+=[[]for cM in range(C-len(b))];return[(cN+[""]*F)[:F]for cN in b]
	def cb(view):a,b=view["lines"],view["known"];c=(0 in b and len(a)>=F and all(a[f].startswith(g+" ")for f,g in enumerate(j)));d=all(m in b for m in range(view["pages"]))and not any(n.strip()for n in a);return view["title"].strip()==aB or c or d
	def cc(view,now):
		if not e["book_head"]:return
		a=L();c=d["reads"][a]["t"]if a is not None else now;b=(aB,"Updated "+a4(c),view["new"]);return b if(view["title"],view["author"])!=b[:2]else None
	def a5(serial):
		b,c=Kit.top_of(serial)
		if c and b==int(API.Bank or 0):a=Kit.find_item(b);return a is not None and bool(a.Opened)
		if c:return b==int(API.Backpack or 0)
		a=Kit.find_item(b)
		try:return a is not None and int(a.Distance)<=bu
		except Exception:return False
	def X(a,text):
		if text not in a["said"]:a["said"].add(text);i(text,Kit.HUE_BAD)
	def Y():
		if b["foreign"]is not None:b["foreign"]=None;k()
	def cd(a,serial,view,now):
		if not view["edit"]:X(a,"couldn't write the book (can't be written).");return False
		if not a5(serial):X(a,"couldn't write the book (too far away).");return False
		if serial not in b["ok_books"]and not cb(view):
			if b["foreign"]!=serial:b["foreign"]=serial;k();i("the book holds other writing: press Overwrite to write over it.")
			return False
		try:e=ca(now)
		except Exception:a["ver"]=b["bookver"];return False
		b["ok_books"].discard(serial);Y();n=min(view["pages"],C)
		if n<C:X(a,"book has %d pages; %d needed."%(n,C))
		c=len(d["shops"])-(C-2)
		if c>0:X(a,"the book holds %d shops; %d left out."%(C-2,c))
		a.update({"ver":b["bookver"],"todo":e[:n],"sent":set(),"head":cc(view,now)});return True
	def ce(now):
		d=b["book_serial"];g=bQ(d)if d else None;a=b["book"]
		if g is None:
			if a is not None:b["book"]=None;Y()
			return
		if a is None or a["g"]is not g:a=b["book"]={"g":g,"at":now,"ver":None if e["book_open"]else b["bookver"],"said":set(),"todo":None,"sent":set(),"head":None}
		if a["todo"]is None and a["ver"]==b["bookver"]:return
		c=bR(g)
		if c is None or c["typing"]or not c["known"]and now-a["at"]<bt:return
		if a["todo"]is None:
			if not cd(a,d,c,now):return
		elif not c["edit"]or not a5(d):a["todo"],a["ver"]=None,None;return
		i=c["lines"];f=[(m+1,n)for m,n in enumerate(a["todo"])if m+1 not in a["sent"]and i[m*F:(m+1)*F]!=n][:bs];h,a["head"]=a["head"],None
		if not f and h is None:a["todo"]=None;return
		if bS(g,d,f,h):a["sent"].update(r for r,t in f)
		else:a["todo"]=None
	def cf():
		if b["picking"]is not None:return
		a=b["picking"]=object();i("target the book for the prices.",Kit.HUE_INFO)
		def c(serial):
			if b["picking"]is not a:return
			b["picking"]=None;p.add(("book_picked",int(serial or 0)),dup=True,front=True)
		HOST.pick_target(bw,c,v)
	def cg(serial):
		if not serial:i("no book picked.",Kit.HUE_INFO);return
		if Kit.find_item(serial)is None:i("that isn't an item.",Kit.HUE_BAD);return
		b.update({"book_serial":serial,"book":None,"ok_books":set()});Y();Z();Kit.put_var(aA,"%X"%serial);i("book picked; open it to write the prices.",Kit.HUE_GOOD);at(v)
	def ch():
		if b["foreign"]is not None:b["ok_books"].add(b["foreign"]);Y()
	def an(text):return " ".join(str(text or "").replace("|"," ").split())[:ad]
	def a6(name):
		for a,s in d["shops"].items():
			if s["name"].lower()==name.lower():return a
		a=max(list(d["shops"])+[len(ax)])+1;b=max([c["order"]for c in d["shops"].values()]+[0])+1;d["shops"][a]={"name":name,"order":b,"spot":None,"tail":[]};q("P|%d"%a);return a
	def ci(sid):
		Z()
		if sid not in d["shops"]:return
		if len(d["shops"])==1:i("keep at least one shop.",Kit.HUE_BAD);return
		f=l(sid);del d["shops"][sid];q("P|%d"%sid)
		for a in[g for g,m in d["vendors"].items()if m["shop"]==sid]:
			del d["vendors"][a];q("V|%X"%a)
			if d["reads"].pop(a,None)is not None:q("R|%X"%a)
		for e in[n for n in d["hist"]if n[0]==sid]:del d["hist"][e];q("H|%d|%s"%e)
		c=b["ask"]
		if c is not None and c["mode"]=="change"and s(c["serial"])is None:b["ask"]=None
		b["seen"]=None;b["bookver"]+=1;i("removed %s."%f,Kit.HUE_INFO);k()
	def a7(name,sid=None):return any(c["name"].lower()==name.lower()and a!=sid for a,c in d["shops"].items())
	def ao(*c):
		for a,b in list(o["tb"].items()):
			try:o["typed"][a]=str(b.Text or "")
			except Exception:continue
	def Z():
		ao();e=o["typed"];f=False
		for a in[g for g in e if g!="add"]:
			c=an(e.pop(a))
			if a not in d["shops"]or not c or c==d["shops"][a]["name"]:continue
			if a7(c,a):i("%s is already a shop."%c,Kit.HUE_BAD);continue
			d["shops"][a]["name"]=c;q("P|%d"%a);f=True
		if f:b["bookver"]+=1;k()
	def cj():
		Z();a=an(o["typed"].get("add",""))
		if not a:i("type a name for the new shop.",Kit.HUE_BAD);return
		if a7(a):i("%s is already a shop."%a,Kit.HUE_BAD);return
		o["typed"].pop("add",None);a6(a);b["bookver"]+=1;i("added %s."%a,Kit.HUE_GOOD);k()
	def ck():e["grid"]=not e["grid"];al();W()
	def cl(serial,sid):
		v,c=d["vendors"].get(serial),d["reads"].get(serial)
		if v is None or v["shop"]==sid:return
		for a,(f,g)in(c["p"].items()if c else()):
			h,e=d["hist"].get((v["shop"],a)),(c["t"],f,g)
			if h is None or e not in h["rows"]:continue
			h["rows"].remove(e);q("H|%d|%s"%(v["shop"],a));a_(sid,a,e)
			if not h["rows"]:del d["hist"][(v["shop"],a)]
		a0(serial,sid,v["spot"],True);b["bookver"]+=1
	def cm():
		a,c=b["ask"],J["c"]
		if a is None or "ask_dd"not in c:return
		try:d=int(c["ask_dd"].GetSelectedIndex())
		except Exception:return
		if d==a["pick"]:return
		a["pick"]=d;e=d>=len(c["ask_ids"])
		if e!=a["new"]:a["new"]=e;k()
	def cn():
		a,c=b["ask"],J["c"]
		if a is None or "ask_dd"not in c:return
		d=c["ask_ids"];f=int(c["ask_dd"].GetSelectedIndex())
		if 0<=f<len(d):e=d[f]
		else:
			g=an(c["ask_name"].Text)if "ask_name"in c else ""
			if not g:
				if a["new"]:i("type a name for the new shop.",Kit.HUE_BAD)
				a["new"],a["pick"]=True,len(d);k();return
			e=a6(g)
		b["ask"]=None
		if a["mode"]=="read":a1(a["pend"],e,True)
		else:cl(a["serial"],e);k()
	def co():
		a=L()
		if a is not None and b["ask"]is None:aZ("change",a,None,H().index(s(a)))
	def cp():b["ask"]=None;k()
	def O():
		if any(e[a]for a in A)and("count",)not in b["jobs"]:b["jobs"].append(("count",))
	def cq():
		a=dict((f,0)for f in j)
		try:d=HOST.pack_items(True,bF)
		except Exception:return
		for b in d:
			try:
				c=aw.get(int(b.Graphic))
				if c is not None:a[c]+=max(1,int(b.Amount or 1))
			except Exception:continue
		p.add(("counted",a),dup=True)
	def cr(got):
		if got!=b["have"]:b["have"]=got;b["bookver"]+=1;k()
	def cs(serial):
		try:a=API.ContextMenu(serial,bB,bC)
		except Exception:a=False
		b["menu"]=False
		if not a and not b["shutting"]:i("couldn't open that vendor's buy list.",Kit.HUE_BAD)
	ct={"count":cq,"menu":cs}
	def cu(m,me):
		a=int(m.Serial)
		if a==me:return False
		if s(a)is not None:return True
		if int(m.Notoriety)!=bD:return False
		b=("%s %s"%(m.Name or "",m.raw.NameAndProps(False)or "")).lower().split();return any(c in b for c in bA)
	def a8():
		a,b=None,ag+1
		try:c=int(API.Player.Serial)
		except Exception:c=0
		for m in HOST.mobiles(ag):
			try:
				d=int(m.Distance)
				if d<b and cu(m,c):a,b=int(m.Serial),d
			except Exception:continue
		return a
	def cv():
		if b["menu"]:return
		a=a8()
		if a is None:i("no reagent vendor in reach.",Kit.HUE_INFO);return
		b["menu"]=True;b["jobs"].append(("menu",a))
	def cw():
		a=b["followed"];c=a if a is not None and ap()==a else a8()
		if c is None:i("no reagent vendor in reach.",Kit.HUE_INFO);return
		b["followed"]=c if Follow.toggle(c,z)else None
	a9=Kit.once(lambda:p.add("buy",key=v),(v,"buy"));cx=Kit.once(lambda:p.add("follow",key=v),(v,"follow"))
	def cy(*a):
		if Follow.alt_held():cx();return
		a9()
	def cz(*d):
		a=time.time();c=a-b["hk_at"]<bE;b["hk_at"]=a
		if not c and not HOST.typing():a9()
	def ba():
		a=_norm_key(e["hk"])if e["hk"]else ""
		if a==(b["hooked"]or ""):return
		if b["hooked"]:aq(b["hooked"],z)
		b["hooked"]=None
		if not a:return
		if HOST.hotkey_on(a,z,cz,"open a reagent vendor's buy list")is False:i("%s isn't a key."%e["hk"],Kit.HUE_BAD);return
		b["hooked"]=a
	bb={"show":k,"ask_ok":cn,"ask_skip":cp,"change":co,"pick_book":cf,"book_picked":cg,"overwrite":ch,"counted":cr,"buy":cv,"follow":cw,"view":ck,"rm_shop":ci,"add_shop":cj}
	def cA(f,x,y):
		g=o["tb"];g.clear();o["n"]=len(d["shops"]);b=x+f.w-12-35-Kit.text_w("Remove")
		for i,a in enumerate(H()+["add"]):
			c=y+i*aH;e=a=="add";h=""if e else l(a);g[a]=Kit.with_tip(Kit.add_textbox(f.g,o["typed"].get(a,h),x+12,c,b-20-x,numbers=False),("Name of a new shop"if e else "Type a new name to rename this shop")+" (up to %d letters)"%ad)
			if e:Kit.art_button(f.g,f.store,"add_shop",Kit.ART_PLAY,b,c-2,"Add","Add a shop with this name",on_click=p("add_shop"))
			else:Kit.art_button(f.g,f.store,"rm_%d"%a,Kit.ART_CLOSE,b,c-2,"Remove","Remove %s and its prices"%h,on_click=p(("rm_shop",a)))
	def cB(w):return(("BOOK",(("buttons",(("pick_book",Kit.ART_PLAY,"Pick book...","Target the book the prices go in",p("pick_book")),)),("note","Book picked: open it to write"if b["book_serial"]else "No book picked yet"),("check","book_open","Write when opened","Write the prices each time you open the book"),("check","book_head","Set title and date","Title the book Reagent Prices, with the last read's date as its author"))),("SHOPPING LIST",tuple(("num",a,Kit.REAGENTS[a[5:]][0]+":","How many to keep in your backpack, bags included; 0 = not on the list","",0,ah)for a in A),{"align":True}),("SHOPS",(("custom",aH*(len(d["shops"])+1),cA),)),("OPTIONS",(("check","say","Journal line after each read","Say the shop and what it's cheapest for"),("check","skip_old","Skip old prices for the cheapest","Leave prices past Old after out of the cheapest and best stops"))),("NUMBERS",(("num","dist","Shop distance:","A vendor this close to a known shop belongs to it","tiles",5,60),("num","old","Old after:","A price this old shows grey, with * in the book","days",1,60)),{"align":True}),("HOTKEYS",(("text","hk","Buy list:","Key for the Buy list button (F5, CTRL+Q, SHIFT+F2; blank = none)",{"tw":100}),)))
	def cC(old,new):
		if any(old[a]!=new[a]for a in A):O()
		if any(old[c]!=new[c]for c in A+("old","skip_old")):b["bookver"]+=1;p.add("show")
	aa=Kit.Page(e,cB,al,cC,final=True,adjust=ao)
	def cD():aa.closed();Z();o["tb"].clear();o["typed"].clear();ba()
	def cE():
		import _thread;b.update({"shutting":False,"docked":False,"queue":[],"loaded":False,"seen":None,"check_at":0.,"aged_at":0.,"save_at":0.,"ask":None,"load_fails":0,"book":None,"foreign":None,"ok_books":set(),"picking":None,"minimized":B.start_min(),"jobs":[],"have":None,"here":None,"hooked":None,"menu":False,"followed":None,"hk_at":0.,"pv":None,"logq":[],"log_at":0.,"log_fails":0,"log_lock":_thread.allocate_lock()});d.update({"shops":{},"vendors":{},"reads":{},"hist":{},"dirty":{},"marks":0});a,c=aK.pop("text",None),aK.pop("at",0.)
		if a is not None and time.time()-c<bn:aR(a)
		bN();ba();O();W();B.dock(fit=True,min=aY)
	def cF():
		q=b["queue"]
		while q:
			c=q.pop(0)
			if B.action(c):continue
			if type(c)is tuple:bb[c[0]](*c[1:])
			else:bb[c]()
		a=time.time();cm()
		if b["loaded"]and a>=b["check_at"]:b["check_at"]=a+bg;b9(a);ce(a)
		if a>=b["aged_at"]:b["aged_at"]=a+bh;am()
	def cG():
		a=b["jobs"]
		while a and not b["shutting"]:c=a.pop(0);ct[c[0]](*c[1:])
		e=time.time()
		if b["logq"]and e>=b["log_at"]:a2()
		if e<b["save_at"]:return
		if not b["loaded"]:aR()
		elif d["dirty"]:aS()
	def cH():a=time.time();return bool(b["jobs"])or bool(b["logq"])and a>=b["log_at"]or(not b["loaded"]or bool(d["dirty"]))and a>=b["save_at"]
	def cI():
		b["shutting"]=True;al()
		if b["hooked"]:aq(b["hooked"],z);b["hooked"]=None
		if b["followed"]is not None and ap()==b["followed"]:Follow.stop(z)
		b["followed"]=None
		if b["loaded"]and d["dirty"]:aS()
		if b["logq"]:a2()
		aJ.close()
	return{"start":cE,"tick":cF,"stop":cI,"client_tick":True,"config_height":aa.height,"build_config":aa.build,"poll_config":aa.poll,"config_closed":cD,"thread_tick":cG,"thread_wanted":cH}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("prices","Reagent Prices","Reagent prices and a price book",_module_prices,.25,category="The world")
