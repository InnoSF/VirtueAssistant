def _module_prices():
	ad=Client.flags;aS=Follow.current;aT=HOST.hotkey_off;aU=HOST.layout_holds;aV=HOST.pack_ver;aW=HOST.refresh_settings;J="prices";N="Reagent Prices";aX="ReagentPrices_settings";bT="ReagentPrices_pos";bU="ReagentPrices_min";bV=420;bW=22;ax=(340,46);bX=3962;ay={"dist":(5,60),"old":(1,60)};bY=.5;bZ=10.;b_=3.;ae=5.;b0=10;az=400;aA=24;q=("SS","NS","BP","GA","SA","BM","GI","MR");aY=dict((Kit.REAGENTS[dC][1],dC)for dC in q);aZ=("Castle British","Delucia","East Britain","Jhelom","Magincia","Moonglow","Moonglow 2","Moonglow/Papua","Ocllo","Serpent's Hold","Skara Brae","Trinsic","Upper W Britain","Vesper","West Britain","Yew Abbey");af="ReagentPrices_data.txt";b1=("P","V","R","H");b2="New shop";b3=30.;a_="ClassicUO.Game.Managers.UIManager";b4=(("ClassicUO.Game.UI.Gumps.ShopGump","IsBuyGump"),("ClassicUO.Game.UI.Gumps.ModernShopGump","isPurchaseGump"));b5=(26,27);aB=((60,1,"just now"),(3600,60,"%d min ago"),(86400,3600,"%d h ago"),(0,86400,"%d d ago"));a0=36;aC=28;a1=34;a2=36;a3="ReagentPrices_book";b6="ClassicUO.Game.UI.Gumps.ModernBookGump";a4="Reagent Prices";b7=1;a5=147;P=18;T=8;b8=4;b9=1.;ca=1;cb=3000;cc=15;ag=86400;cd=3;a6={"SS":"Silk","NS":"Shade","BP":"Pearl","GA":"Garlic","SA":"Ash","BM":"Moss","GI":"Ginseng","MR":"Mandrake"};ce=(("SS","NS"),("BP","GA"),("SA","BM"),("GI","MR"));cf=("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");aD=8;cg=("mage","alchemist","herbalist");ch="Buy";ci=3;cj=1;ck=.6;cl=.5;a7="ReagentPrices_keep";aE=9999;K=tuple("keep_"+dD for dD in q);a8=("hk",);aF=3;ay.update((dE,(0,aE))for dE in K);a9=60;ba=28;cm=3600;cn=12;bb=" (here)";bc="ReagentPrices_size";bd=14;U=60;co=150;cp=.3;cq=4000;HD=27;aG=9;cr=80;cs="ALL VENDORS  (price, stock; ^ up, v down)";ct="Switch between the cheapest list and every vendor";be="ReagentPrices_log.csv";aH=5000;cu="time,shop,reagent,price,stock,vendor,serial";bf="ReagentPrices_history.txt";aI=10000;bg=400;cv=("Open the nearest reagent vendor's buy list (within %d tiles). Alt+click: auto-follow (again to stop)"%aD);l={"say":True,"dist":20,"book_open":True,"book_head":True,"old":7,"hk":"","skip_old":False,"grid":False,"keep_SS":0,"keep_NS":0,"keep_BP":0,"keep_GA":0,"keep_SA":0,"keep_BM":0,"keep_GI":0,"keep_MR":0};cw=dict(l);b={"minimized":False,"shutting":False,"docked":False,"queue":[],"loaded":False,"seen":None,"check_at":0.,"aged_at":0.,"save_at":0.,"ask":None,"warned":set(),"load_fails":0,"book":None,"book_serial":0,"bookver":0,"foreign":None,"ok_books":set(),"picking":None,"jobs":[],"have":None,"here":None,"hooked":None,"menu":False,"followed":None,"hk_at":0.,"pv":None,"logq":[],"log_at":0.,"log_fails":0,"histq":[],"drops":[],"hist_at":0.,"hist_fails":0,"obs_ok":False,"memo":{},"miss":{},"size":None,"resize_at":0.,"drawn":None,"sc":1.,"f":bd,"hd":HD};V={"g":None,"c":{},"store":({},{})};d={"shops":{},"vendors":{},"reads":{},"hist":{},"dirty":{},"marks":0,"obs":{}};o={};ai={};tw={};D={"tb":{},"typed":{},"n":0};bi,E,u=Kit.basics(b,N);bj={"text":Kit.read_merge(Kit.data_path(af)),"at":time.time()}
	def cx():
		Kit.kv_load(aX,"|",l,ay,a8)
		try:b["book_serial"]=int(Kit.get_var(a3,"")or "0",16)
		except ValueError:b["book_serial"]=0
		l.update((e,0)for e in K)
		for c in Kit.get_var(a7,"").split(","):
			a,d,n=c.partition(":")
			if a not in q:continue
			try:l["keep_"+a]=max(0,min(aE,int(n)))
			except ValueError:continue
	def aJ():Kit.kv_save(aX,"|",l,[a for a in sorted(cw)if a not in K],ay,a8);Kit.put_var(a7,",".join("%s:%d"%(c,l["keep_"+c])for c in q if l["keep_"+c]))
	def Q(what):
		if what not in b["warned"]:b["warned"].add(what);u("couldn't reach the client's %s (TazUO changed)."%what,Kit.HUE_BAD)
	def bk(t):
		if "gg"not in o:o["gg"]=[a for a in Tz.T(a_).GetMethods(ad(static=True))if a.Name=="GetGump"and a.IsGenericMethodDefinition][0]
		return o["gg"].MakeGenericMethod(t)
	def cy():
		if o.get("shop")is None:
			if "shop"in o:return
			o["shop"]=None
			try:
				import System;b=[]
				for c,a in b4:
					t=Tz.T(c)
					if not Tz.has(t,a,ad()):raise Exception("no %s"%a)
					b.append((bk(t),a))
				o["none"]=System.Array[object]([None]);o["shop"]=b
			except Exception:Q("shop list");return
		try:
			for d,a in o["shop"]:
				g=d.Invoke(None,o["none"])
				if g is not None and not g.IsDisposed and Tz.get(g,a):return g,int(g.LocalSerial)
		except Exception:pass
		return
	def cz(serial):
		if o.get("mobs")is None:
			if "mobs"in o:return
			o["mobs"]=None
			try:
				import System;b=Typing._get(API,"World")
				if b is None:b=Tz.get(Tz.get(Tz.get(None,"Game",Tz.T("ClassicUO.Client")),"UO"),"World")
				g=Tz.T("ClassicUO.Game.Data.Layer");o["layers"]=[System.Enum.ToObject(g,k)for k in b5];o["u32"]=System.UInt32;o["mobs"]=Tz.get(b,"Mobiles")
			except Exception:Q("shop list");return
		try:
			c=o["mobs"];d=o["u32"](serial)
			if not c.ContainsKey(d):return
			h=c[d];e=[]
			for i in o["layers"]:
				f=h.FindItemByLayer(i);a=f.Items if f is not None else None
				for j in range(az):
					if a is None:break
					e.append((int(a.Graphic),int(a.Price),int(a.Amount)));a=a.Next
			return e
		except Exception:return
	def bl():
		if o.get("book")is None:
			if "book"in o:return
			o["book"]=None
			try:
				import System;a=Tz.T(b6);b=ad();c=ad(static=True);d=Tz.T("ClassicUO.Network.NetClientExt");f=Tz.T("ClassicUO.Network.AsyncNetClient");g=Tz.get(Tz.get(None,"Game",Tz.T("ClassicUO.Client")),"UO");e={"get":bk(a),"lines":a.GetProperty("BookLines",b),"redraw":a.GetMethod("ServerSetBookText",b),"title":a.GetField("_titleTextBox",b),"author":a.GetField("_authorTextBox",b),"page":d.GetMethod("Send_BookPageData",c),"head":d.GetMethod("Send_BookHeaderChanged",c),"head_old":d.GetMethod("Send_BookHeaderChanged_Old",c),"socket":f.GetProperty("Socket",c),"focus":Tz.T(a_).GetProperty("KeyboardFocusControl",c),"ctl":Tz.T("ClassicUO.Game.UI.Controls.Control"),"root":Tz.T("ClassicUO.Game.UI.Controls.Control").GetProperty("RootParent",b),"fonts":Tz.get(Tz.get(g,"FileManager"),"Fonts"),"u32":System.UInt32,"objs":System.Array[object],"strs":System.Array[System.String]}
				if any(h is None for h in e.values()):raise Exception("no book member")
				o["book"]=e
			except Exception:Q("book");return
		return o["book"]
	def cA(serial):
		b=bl()
		if b is None:return
		try:g=b["get"].Invoke(None,b["objs"]([b["u32"](serial)]))
		except Exception:
			o["fails"]=o.get("fails",0)+1
			if o["fails"]>=cd:o["book"]=None;Q("book")
			return
		o["fails"]=0;return g if g is not None and not g.IsDisposed else None
	def cB(g):
		b=o["book"]
		try:a=b["focus"].GetValue(None);return{"pages":int(g.BookPageCount),"known":set(int(c)for c in g.KnownPages),"edit":bool(g.IsEditable),"lines":[str(e or "").rstrip("\n")for e in b["lines"].GetValue(g)],"new":bool(g.UseNewHeader),"title":str(b["title"].GetValue(g).Text or ""),"author":str(b["author"].GetValue(g).Text or ""),"typing":a is not None and(a is g or b["ctl"].IsInstanceOfType(a)and b["root"].GetValue(a)is g)}
		except Exception:Q("book");return
	def cC(g,serial,pages,head):
		b=o["book"]
		try:
			a=b["socket"].GetValue(None);e=b["lines"].GetValue(g);u=b["u32"](serial)
			if head is not None:b["head"if head[2]else "head_old"].Invoke(None,b["objs"]([a,u,head[0],head[1]]));g.SetTile(head[0],True);g.SetAuthor(head[1],True)
			for c,d in pages:
				b["page"].Invoke(None,b["objs"]([a,u,b["strs"](d),c]))
				for i,f in enumerate(d):e[(c-1)*T+i]=f
			if pages:b["redraw"].Invoke(g,None)
			return True
		except Exception:Q("book");return False
	def cD(text):
		b=bl()
		try:return int(b["fonts"].GetWidthUnicode(b7,text))
		except Exception:Q("book");raise
	def cE(items):
		b={}
		for f,a,e in items:
			c=aY.get(f)
			if c is None or a<=0 or e<=0:continue
			d=b.get(c)
			if d is None or a<d[0]:b[c]=(a,e)
			elif a==d[0]:b[c]=(a,d[1]+e)
		return b
	def bm(fields):
		try:return tuple(int(a)for a in fields)if len(fields)==3 else None
		except ValueError:return
	def bn(spot):return[str(a)for a in spot]if spot else["","",""]
	def bo(text):
		a={"shops":{},"vendors":{},"reads":{},"hist":{}}
		for d in(text or "").split("\n"):
			f=d.rstrip("\r").split("|")
			try:
				if f[0]=="P":a["shops"][int(f[1])]={"name":f[2],"order":int(f[3]),"spot":bm(f[4:7]),"tail":f[7:]}
				elif f[0]=="V":a["vendors"][int(f[1],16)]={"shop":int(f[2]),"spot":bm(f[3:6]),"name":Y(f[6])if len(f)>6 else "","first":aK(f,7),"last":aK(f,8),"gone":aK(f,9),"tail":f[10:]}
				elif f[0]=="R":
					p={}
					for c in f[3].split(","):
						if c:e,g,h=c.split(":")[:3];p[e]=(int(g),int(h))
					a["reads"][int(f[1],16)]={"t":int(f[2]),"p":p,"tail":f[4:]}
				elif f[0]=="H":i=[tuple(int(m)for m in k.split(":")[:3])for k in f[3].split(";")if k];a["hist"][(int(f[1]),f[2])]={"rows":[n for n in i if len(n)==3],"tail":f[4:]}
			except(IndexError,ValueError):continue
		for j,v in a["vendors"].items():
			b=a["reads"].get(j)
			if b is not None:v["first"]=v["first"]or b["t"];v["last"]=max(v["last"],b["t"])
		return a
	def aK(f,i):
		try:return int(f[i])
		except(IndexError,ValueError):return 0
	def cF(key):
		f=key.split("|");b=f[0]
		if b=="P":e=d["shops"].get(int(f[1]));a=e and[e["name"],str(e["order"])]+bn(e["spot"])
		elif b=="V":e=d["vendors"].get(int(f[1],16));a=e and[str(e["shop"])]+bn(e["spot"])+[e.get("name","")]+[str(e.get(c,0))for c in("first","last","gone")]
		elif b=="R":e=d["reads"].get(int(f[1],16));a=e and[str(e["t"]),",".join("%s:%d:%d"%(h,g[0],g[1])for h,g in sorted(e["p"].items()))]
		else:e=d["hist"].get((int(f[1]),f[2]));a=e and[";".join("%d:%d:%d"%i for i in e["rows"])]
		return None if e is None else "|".join([key]+a+e["tail"])
	def cG(line):f=line.split("|");n=3 if f[0]=="H"else 2;return "|".join(f[:n])if f[0]in b1 and len(f)>n else None
	def B(key):d["dirty"][key]=True;d["marks"]+=1
	def bp(a):d.update(a);E.add("show")
	def bq(text=None):
		if text is None:text=Kit.read_merge(Kit.data_path(af))
		if text is None:
			b["save_at"]=time.time()+ae;b["load_fails"]+=1
			if b["load_fails"]==2:u("couldn't read %s (trying again)."%af,Kit.HUE_BAD)
			return
		a=bo(text)
		if not text.strip():
			for i,c in enumerate(aZ):a["shops"][i+1]={"name":c,"order":i+1,"spot":None,"tail":[]};B("P|%d"%(i+1))
		b["loaded"]=True;b["bookver"]+=1;bp(a)
	def br():
		c=list(d["dirty"]);e=dict((g,cF(g))for g in c);f=d["marks"]
		try:a=Kit.merge_save(Kit.data_path(af),e,cG)
		except Exception:a=None
		if a is None:b["save_at"]=time.time()+ae;return
		if d["marks"]!=f:return
		for k in c:d["dirty"].pop(k,None)
		bp(bo("\n".join(a)))
	def W():return sorted(d["shops"],key=lambda sid:(d["shops"][sid]["order"],sid))
	def C(sid):return d["shops"][sid]["name"]if sid in d["shops"]else "?"
	def H(serial):v=d["vendors"].get(serial);return v["shop"]if v is not None and v["shop"]in d["shops"]else None
	def Z(serial):v=d["vendors"][serial];a=d["shops"].get(v["shop"]);return(a["order"]if a else 0,not v.get("first"),v.get("first",0),serial)
	def aj(live=False):
		a={}
		for b,v in d["vendors"].items():
			if v["shop"]in d["shops"]and not(live and v.get("gone")):a.setdefault(v["shop"],[]).append(b)
		for c in a.values():c.sort(key=Z)
		return a
	def ak():
		h={}
		for k,i in aj().items():
			b={};f=C(k)
			for l,j in enumerate(i):
				c=d["vendors"][j].get("name","");e=c.lower();b[e]=b.get(e,0)+1
				if c:a=c if b[e]==1 else "%s %d"%(c,b[e]);g=a+", "+f
				elif len(i)==1:a,g="vendor",f
				else:a="vendor %d"%(l+1);g=f+" "+a
				h[j]=(g,a)
		return h
	def al(serial,a=None):return(a or ak()).get(serial,(C(H(serial)),""))[0]
	def R(now=None):
		b={};c=l["old"]*ag if now is not None and l["skip_old"]else None
		for e,a in d["reads"].items():
			v=d["vendors"].get(e)
			if v is None or v["shop"]not in d["shops"]or v.get("gone")or c is not None and now-a["t"]>c:continue
			b[e]=dict((f,(g,h,a["t"]))for f,(g,h)in a["p"].items())
		return b
	def am(now=None,vp=None):
		f={}
		for g,p in(R(now)if vp is None else vp).items():
			c=f.setdefault(d["vendors"][g]["shop"],{})
			for e,a in p.items():
				b=c.get(e)
				if b is None or a[0]<b[0]:c[e]=a
				elif a[0]==b[0]:c[e]=(a[0],b[1]+a[1],max(b[2],a[2]))
		return f
	def S(prices,rank=None):
		rank=rank or(lambda sid:d["shops"][sid]["order"]);b={};c={}
		for e,h in prices.items():
			r=rank(e)
			for a,f in h.items():
				g=b.get(a)
				if g is None or(f[0],r)<(g[1][0],c[a]):b[a]=(e,f);c[a]=r
		return b
	def an(n):return "{:,}".format(int(n))
	def cH():
		a,c=b["here"],b["ask"]
		if a is None:return
		if c is not None and c["mode"]=="read"and c["serial"]==a:return None,c["pend"]["p"]
		e=d["reads"].get(a);return H(a),(e["p"]if e else{})
	def bs(prices,vp=None):
		f=dict((G,l["keep_"+G])for G in q if l["keep_"+G]>0);t=b["have"]or{};e=dict((M,max(0,ah-t.get(M,0)))for M,ah in f.items())if f else dict((bh,1)for bh in q);a=[dC for dC in q if e.get(dC)];g=[];i={}
		for u,v in(vp or{}).items():
			for w,x in v.items():i.setdefault((d["vendors"][u]["shop"],w),[]).append(x[:2])
		for h,j in(prices.items()if a else()):
			c={}
			for k in[dD for dD in a if dD in j]:
				m=e[k];n=0;o=sorted(i.get((h,k))or[j[k][:2]])
				for y,z in o:p=min(m,z);n+=p*y;m-=p
				c[k]=(n,sum(dE[1]for dE in o))
			r=[dF for dF in a if dF not in c];s=[dG for dG in a if dG in c and c[dG][1]<e[dG]];g.append((len(r)+len(s),sum(dH[0]for dH in c.values()),d["shops"][h]["order"],h,r,s))
		g.sort();return e,bool(f),a,g[:aF]
	def bt(r):return "; ".join((["no "+", ".join(r[4])]if r[4]else[])+(["short "+", ".join(r[5])]if r[5]else[]))
	def cI(prices,hv,want,f,need):
		if not f:return "For 1 of each reagent; set a shopping list in Settings"
		if not need:return "Your list: nothing to buy"
		b=S(prices);d=[h for h in need if h not in b];c="%s at the cheapest"%an(sum(want[i]*b[i][1][0]for i in need if i in b))
		if hv is not None:a=hv[1];e=[m for m in need if m not in a or a[m][1]<want[m]];g=an(sum(min(want[n],a[n][1])*a[n][0]for n in need if n in a));c="%s here%s, %s"%(g," (short %s)"%", ".join(e)if e else "",c)
		return "Your list: "+c+("; no price for %s"%", ".join(d)if d else "")
	def X():
		a=None
		for b,c in d["reads"].items():
			if H(b)is not None and(a is None or c["t"]>d["reads"][a]["t"]):a=b
		return a
	def cJ():a=set(H(c)for c in d["reads"]);b=W();return next((e for e,f in enumerate(b)if f not in a),0)
	def bu():a=b["ask"];return(a and a["mode"],bool(a and a["new"]),X()is not None,b["foreign"]is not None,any(l[c]for c in K),l["grid"],len(d["shops"]),bw(b["f"]))
	def j(v,s=None):return int(round(v*(b["sc"]if s is None else s)))
	def ao(s):return max(6,Kit.tsize(int(round(bd*s))))
	def aL(s):return max(j(bW,s),int(round(ao(s)*1.5)))
	def aM(s):return max(j(HD,s),int(round(ao(s)*1.9)))
	def O(bh):return max(0,(bh-int(round(b["f"]*1.3)))//2)
	def F(text,size):
		k=(text,size);w=tw.get(k)
		if w is None:
			if len(tw)>=cq:tw.clear()
			w=0
			if text:
				l=G.CreateGumpTTFLabel(text,size,"#FFFFFF");w=int(l.GetWidth()or 0);Kit.dispose(l)
				if not w:return int(.6*size*len(text))
			tw[k]=w
		return w
	def I(text,room):
		f=b["f"];text=str(text or "")
		if F(text,f)<=room:return text
		a,c=0,len(text)-1
		while a<c:
			d=(a+c+1)//2
			if F(text[:d].rstrip()+"..",f)<=room:a=d
			else:c=d-1
		return text[:a].rstrip()+".."
	def A(g,text,x,y,hue=None):l=Kit.inert(G.CreateGumpTTFLabel(text,b["f"],"#FFFFFF"));l.Hue=Kit.HUE_TEXT if hue is None else hue;l.SetPos(x,y);g.Add(l);return l
	def ap(g,x,y,w,h,title=None):
		Kit.add_section(g,x,y,w,h)
		if title:A(g,I(title,w-2*j(8)),x+j(8),y+O(b["hd"]),Kit.HUE_TITLE)
	def aN():a=aj(True);return[e for c in W()for e in[(c,f)for f in a.get(c,[])]or[(c,None)]]
	def bv(serial,code,row):return "%d%s (%d)"%(row[0],cQ(serial,code,row),row[1])
	def bw(f):
		if not l["grid"]:return(max(F(Kit.REAGENTS[m][0],f)for m in q),F("9999",f),F("buy 9999",f)if any(l[n]for n in K)else 0,F("59 min ago",f),max(F("No price yet",f),F("Only old prices",f)))
		d=aN();j=ak();k=R();e=set();g=["Shop"];h=["Vendor"];i=["-"]+list(q)
		for c,a in d[:a9]:
			if c not in e:e.add(c);g.append(C(c))
			if a is None:continue
			h.append(j[a][1]+(bb if a==b["here"]else ""));i+=[bv(a,p,s)for p,s in k.get(a,{}).items()]
		return(max(F(r,f)for r in g),max(F(t,f)for t in h),max(F(v,f)for v in i),len(d))
	def cK(f):
		c=b["ask"];a=0
		if c is None and X()is not None:a=16+35+Kit.text_w("Change")+6+60
		if c is not None:a=24+F("Which shop?",f)+cr+90+Kit.text_w("OK")+Kit.text_w("Skip"if c["mode"]=="read"else "Cancel")
		if b["foreign"]is not None:a=max(a,26+35+Kit.text_w("Overwrite")+60)
		return a
	def aq(s):
		f=ao(s);m=bw(f);p=j(8,s)
		if l["grid"]:a=j(16,s)+m[0]+m[1]+2*p+len(q)*(m[2]+p)
		else:a=(j(34,s)+m[0]+m[1]+2*j(10,s)+m[4]+2*p+m[3]+(m[2]+j(10,s)if any(l[c]for c in K)else 0))
		return 2*Kit.MARGIN+max(j(bV-2*Kit.MARGIN,s),a,cK(f))
	def bx():return 1+max(1,min(a9,len(aN())))if l["grid"]else len(q)
	def by(s):a=b["ask"];c=max(a0,j(a0,s))if a else 0;d=max(aC,j(aC,s))if a and a["new"]else 0;e=max(a2,j(a2,s))if b["foreign"]is not None else 0;f=0 if l["grid"]else aM(s)+(aF+1)*aL(s)+j(aG,s);return max(a1,j(a1,s)),c,d,f,e
	def bz(p):return sum(Kit.GAP+a for a in(p[0],p[1]+p[2],p[3],p[4])if a)
	def aO(s,k):return 2*Kit.MARGIN+30+Kit.GAP+aM(s)+k*aL(s)+j(aG,s)+bz(by(s))
	def bA():s=U/100.;return aq(s),aO(s,bx())
	def cL(w,h,k,g):
		a,b=U,co
		while a<b:
			c=(a+b+1)//2
			if aO(c/100.,k)<=h:a=c
			else:b=c-1
		d=2*Kit.MARGIN;f=w-d;s=max(U,min(a,int(U*f/max(1,g-d))))/100.;e=aq(s)
		while e>w and s>U/100.:s=max(U,min(int(round(s*100))-1,int(100.*s*f/(e-d))))/100.;e=aq(s)
		return s
	def cM(a,c,k):
		z=b["size"];d,e=Kit.screen()
		if z is None:return max(a,aq(1.)),max(c,aO(1.,k))
		return max(a,min(z[0],d)if d>0 else z[0]),max(c,min(z[1],e)if e>0 else z[1])
	def cN():
		try:w,h=[int(a)for a in Kit.get_var(bc,"").split(",")[:2]]
		except ValueError:return
		return(w,h)if w>0 and h>0 else None
	def cO(*a):b["resize_at"]=time.time()
	def cP():
		g=V["g"]
		if not Kit.is_open(g)or b["minimized"]or aU(J):return
		a,c=int(g.GetWidth()),int(g.GetHeight());d=b["drawn"]or(0,0)
		if abs(a-d[0])<=2 and abs(c-d[1])<=2:return
		b["size"]=(a,c);Kit.put_var(bc,"%d,%d"%(a,c));aa()
	def cQ(serial,code,row):
		i=q.index(code)
		for t,p,a in reversed(d["obs"].get(serial,())):
			if t<row[2]:return ""if not p[i]else "^"if row[0]>p[i]else "v"if row[0]<p[i]else ""
		return ""
	def cR(g,store,c,M,y,IW,a,ah,nh):
		Kit.add_section(g,M,y,IW,ah+nh);x=M+IW-8;f=y+(ah-24)//2;l=("Skip","Drop this read")if a["mode"]=="read"else("Cancel","Keep this vendor's shop")
		for h,m,i,n in(("ask_skip",Kit.ART_CLOSE)+l,("ask_ok",Kit.ART_OK,"OK","Link this vendor to the picked shop")):x-=35+Kit.text_w(i);Kit.art_button(g,store,h,m,x,f,i,n,on_click=E(h));x-=10
		A(g,"Which shop?",M+j(8),y+O(ah));d=M+j(8)+8+F("Which shop?",b["f"]);k=c["ask_ids"]=W();o=[C(r)for r in k]+[b2]
		if a["new"]:A(g,"Name:",M+j(8),y+ah+O(nh));p=Kit.add_textbox(g,"",d,y+ah+(nh-aC)//2,x-d,numbers=False);c["ask_name"]=Kit.with_tip(p,"Name of the new shop (up to %d letters)"%aA)
		e=G.CreateDropDown(x-d,o,max(0,min(a["pick"],len(k))));e.SetPos(d,f);g.Add(e);c["ask_dd"]=Kit.with_tip(e,"Shop this vendor is in")
	def cS(g,store,M,y,IW,a):Kit.add_section(g,M,y,IW,a);x=M+IW-8-35-Kit.text_w("Overwrite");Kit.art_button(g,store,"overwrite",Kit.ART_OK,x,y+(a-24)//2,"Overwrite","Write the prices over this book's text (this book only)",on_click=E("overwrite"));A(g,I("The book holds other writing",x-M-j(8)-10),M+j(8),y+O(a),Kit.HUE_BAD)
	def cT(g,c,M,y,IW,sh,n,m,rp):
		ap(g,M,y,IW,sh,cs);a=j(8);e,f=m[0]+a,m[1]+a;h=max(m[2]+a,(IW-j(16)-e-f)//len(q));i=M+a+e;k=i+f;c["name_w"]=e-a;c["vendor_w"]=f-a;c["cell_w"]=h-j(4);d=y+b["hd"]+O(rp)
		for x,l in[(M+a,"Shop"),(i,"Vendor")]+[(k+p*h,r)for p,r in enumerate(q)]:A(g,l,x,d,Kit.HUE_TITLE)
		c["grid"]=[(A(g,"",M+a,d+(s+1)*rp),[A(g,"",k+t*h,d+(s+1)*rp)for t in range(len(q))],A(g,"",i,d+(s+1)*rp))for s in range(n)]
	def aa():
		t=l["grid"]
		if b["minimized"]:g,i,c=L.begin(ax[0],ax[1]);L.end(g);b["drawn"]=None;ar();return
		k=bx();n,u=bA();z=L.zone_slot(n,u);w,v=z if z else cM(n,u,k);s=1. if z is None and b["size"]is None else cL(w,v,k,n);b.update(sc=s,f=ao(s),hd=aM(s),resize_at=0.);x=aL(s);B=b["hd"];I=None if aU(J)else(n,u,cO);g,i,c=L.begin(w,v,resize=I);c["shape"]=bu();L.frame(g,mouse=I is None,extra=[("buy",Kit.ART_PLAY,"Buy list",cv,dr),("view",Kit.ART_PAGE,"View: grid"if t else "View: cheapest",ct,E("view"))]);M=Kit.MARGIN;a=w-2*M;y=M+30+Kit.GAP;C=b["ask"];K=c["shape"][4];m=c["shape"][7];N=by(s);o,P,Q,R,Y=N;p=v-M-bz(N)-y;r=max(x,(p-B-j(aG))//k)
		if t:cT(g,c,M,y,a,p,k-1,m,r)
		else:
			ap(g,M,y,a,p,"CHEAPEST");D=j(8);S=M+j(34);T=S+m[0]+j(10);h=T+m[1]+j(10);U=h+(m[2]+j(10)if K else 0);V=M+a-D-m[3];c["shop_w"]=V-D-U;c["rows"]=[];F=j(20);e=O(r)
			for Z,W in enumerate(q):f=y+B+Z*r;aa,ab=Kit.REAGENTS[W];H=G.CreateGumpItemPic(ab,F,F);H.SetPos(M+D,f+(r-F)//2);Kit.inert(H);g.Add(H);A(g,aa,S,f+e);c["rows"].append((W,A(g,"",T,f+e),A(g,"",U,f+e),A(g,"",V,f+e,Kit.HUE_INFO),A(g,"",h,f+e,Kit.HUE_INFO)if K else None))
		d=y+p+Kit.GAP;ap(g,M,d,a,o);c["line_w"]=a-2*j(8)
		if C is None and X()is not None:h=M+a-8-35-Kit.text_w("Change");c["line_w"]=h-6-M-j(8);Kit.art_button(g,i,"change",Kit.ART_PAGE,h,d+(o-26)//2,"Change","Pick another shop for the last vendor read",on_click=E("change"))
		c["line"]=A(g,"",M+j(8),d+O(o),Kit.HUE_INFO);d+=o+Kit.GAP
		if C is not None:cR(g,i,c,M,d,a,C,P,Q);d+=P+Q+Kit.GAP
		if not t:ap(g,M,d,a,R,"BEST STOPS");c["stops_w"]=a-2*j(8);e=d+B+O(x);c["stops"]=[A(g,"",M+j(8),e+ah*x,Kit.HUE_INFO)for ah in range(aF+1)];d+=R+Kit.GAP
		if b["foreign"]is not None:cS(g,i,M,d,a,Y)
		L.end(g);b["drawn"]=(int(g.GetWidth()),int(g.GetHeight()));ar()
	L=Kit.Window(J,N,b,V,aa,bT,bU,mini=ax,icon=bX,cleanup=bi)
	def cU(c,q,j,hv,want,now):
		r=b["here"]if hv else None;k=ak();s=aj(True);t=S(dict((y,G)for y,G in j.items()if y!=r)if hv else j,Z);u=S(q,Z);v=l["old"]*ag
		for d,f,g,h,m in c["rows"]:
			a=t.get(d)
			if m is not None:Kit.set_text(m,"buy %d"%want[d]if d in want else "",Kit.HUE_TEXT if want.get(d)else Kit.HUE_INFO)
			if hv is not None:e=hv[1].get(d);w=e is not None and(a is None or e[0]<=a[1][0]);Kit.set_text(f,"out"if e is None else str(e[0]),Kit.HUE_GOOD if w else Kit.HUE_INFO if e is None else Kit.HUE_TEXT);Kit.set_text(g,I("best %d %s"%(a[1][0],al(a[0],k))if a else "no other shop",c["shop_w"]),Kit.HUE_INFO);Kit.set_text(h,Kit.ago(now-a[1][2],aB)if a else "",Kit.HUE_INFO);continue
			if a is None:Kit.set_text(f,"-",Kit.HUE_INFO);Kit.set_text(g,I("Only old prices"if d in u else "No price yet",c["shop_w"]),Kit.HUE_INFO);Kit.set_text(h,"");continue
			n,i=a;o=Kit.HUE_INFO if now-i[2]>v else Kit.HUE_TEXT;p=H(n);x=al(n,k)if len(s.get(p,()))>1 else C(p);Kit.set_text(f,str(i[0]),o);Kit.set_text(g,I(x,c["shop_w"]),o);Kit.set_text(h,Kit.ago(now-i[2],aB),Kit.HUE_INFO)
	def cV(c,prices,s,t,now):
		k=S(t,Z);d=aN();h=c["grid"];m=len(d)-len(h)+1;u=l["old"]*ag;v=ak();n=b["here"]
		for j,(o,w,x)in enumerate(h):
			p=d[j]if j<len(d)and(m<=1 or j<len(h)-1)else None;i,a=p or(None,None);e=s.get(a)
			if p is None:Kit.set_text(o,I("+%d more vendors"%m,c["name_w"]+c["vendor_w"])if j<len(d)else "",Kit.HUE_INFO)
			else:y=j==0 or d[j-1][0]!=i;Kit.set_text(o,I(C(i),c["name_w"])if y else "",Kit.HUE_INFO if i not in prices else Kit.HUE_TEXT)
			z=v[a][1]+(bb if a==n else "")if a is not None else "";Kit.set_text(x,I(z,c["vendor_w"]),Kit.HUE_GOOD if a is not None and a==n else Kit.HUE_INFO if e is None else Kit.HUE_TEXT)
			for f,r in zip(q,w):
				g=e.get(f)if e else None
				if g is None:Kit.set_text(r,"-"if e is not None else "",Kit.HUE_INFO);continue
				A=now-g[2]>u;B=f in k and g[0]<=k[f][1][0];Kit.set_text(r,I(bv(a,f,g),c["cell_w"]),Kit.HUE_INFO if A else Kit.HUE_GOOD if B else Kit.HUE_TEXT)
	def ar():
		c=V["c"];e=time.time();f=X()
		if f is None:a="no reads yet"
		else:a="read %s %s"%(al(f),Kit.ago(e-d["reads"][f]["t"],aB))
		if b["foreign"]is not None:a="book holds other writing; Restore to overwrite"
		if b["ask"]is not None:a="which shop? Restore to pick"
		if "status"in c:Kit.set_text(c["status"],"%s: %s"%(N,a))
		elif "line"in c:
			j=R();g=R(e);m=am(vp=g);n=cH();o,q,p,h=bs(m,g)
			if "grid"in c:cV(c,am(vp=j),j,g,e)
			else:cU(c,j,g,n,o,e)
			if b["ask"]is not None:k="Which shop is this vendor in? Pick it below"
			elif f is None:k="No reads yet: open a reagent vendor's buy list"
			else:k="Last %s"%a
			Kit.set_text(c["line"],I(k,c["line_w"]),Kit.HUE_INFO)
			if "stops"not in c:return
			l=[cI(m,n,o,q,p)]+["%d %s %s%s"%(v+1,C(t[3]),an(t[1]),": "+bt(t)if t[0]else "")for v,t in enumerate(h)]
			if p and not h:l.append("No prices yet")
			for i,s in enumerate(c["stops"]):r=h[i-1]if 0<i<=len(h)else None;Kit.set_text(s,I(l[i]if i<len(l)else "",c["stops_w"]),Kit.HUE_TEXT if r is not None and not r[0]else Kit.HUE_INFO)
	def z():
		if D["tb"]and D["n"]!=len(d["shops"]):aR();D["n"]=len(d["shops"]);aW(J)
		if not b["minimized"]and V["c"].get("shape")!=bu():aa()
		else:ar()
	def bB(mode,serial,pend,pick):
		b["ask"]={"mode":mode,"serial":serial,"pend":pend,"pick":pick,"new":False};z()
		if b["minimized"]:u("which shop is this vendor in? Restore the window to pick.")
	def bC(sid,code,row):h=d["hist"].setdefault((sid,code),{"rows":[],"tail":[]});h["rows"].append(row);h["rows"].sort();del h["rows"][:-b0];B("H|%d|%s"%(sid,code))
	def bD(serial,sid,spot,picked=False,name="",t=0):
		a=d["vendors"].get(serial)or{"spot":None,"tail":[]};d["vendors"][serial]={"shop":sid,"spot":spot or a["spot"],"name":name or a.get("name",""),"first":a.get("first")or t,"last":max(t,a.get("last",0)),"gone":0 if t else a.get("gone",0),"tail":a["tail"]};B("V|%X"%serial)
		if picked and(spot or a["spot"]):d["shops"][sid]["spot"]=spot or a["spot"];B("P|%d"%sid)
	def cW(spot):
		b,c=None,l["dist"]+1;e=[(i,h["spot"])for i,h in d["shops"].items()if h["spot"]];e+=[(k["shop"],k["spot"])for k in d["vendors"].values()if k["spot"]and k["shop"]in d["shops"]]
		for g,a in(e if spot else()):
			f=max(abs(a[1]-spot[1]),abs(a[2]-spot[2]))
			if a[0]==spot[0]and f<c:b,c=g,f
		return b
	def bE(pend,sid,picked=False):
		a,t=pend["serial"],pend["t"];bD(a,sid,pend["spot"],picked,pend.get("name",""),t);j=d["reads"].get(a)or{"tail":[]};d["reads"][a]={"t":t,"p":dict(pend["p"]),"tail":j["tail"]};B("R|%X"%a)
		for k,(m,n)in pend["p"].items():bC(sid,k,(t,m,n))
		cX(pend,sid);e=aP(t,"%X"%a,pend["p"]);r=aQ(e);c=b["histq"];f=d["obs"].setdefault(a,[]);f.append((r[0],r[2],r[3]));del f[:-bg];c.append(e)
		if len(c)>aI:del c[:-aI]
		b["miss"].pop(a,None)
		if l["say"]:g=R(time.time());o=S(g,Z);h=g.get(a,{});i=[p for p in q if p in h and h[p][0]==o[p][1][0]];u("%s read%s."%(al(a),"; cheapest for "+", ".join(i)if i else ""),Kit.HUE_GOOD)
		b["bookver"]+=1;z()
	def cX(pend,sid):
		c=bF(C(sid));e=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(pend["t"]));a=b["logq"];f="%s,%X"%(bF((d["vendors"].get(pend["serial"])or{}).get("name","")),pend["serial"]);a.extend("%s,%s,%s,%s,%d,%s"%(e,c,Kit.REAGENTS[g][0],pend["p"][g][0]if g in pend["p"]else "",pend["p"][g][1]if g in pend["p"]else 0,f)for g in q)
		if len(a)>aH:del a[:-aH]
	def bF(text):return '"%s"'%text.replace('"','""')if ","in text or '"'in text else text
	def aP(t,who,p):return "%d|%s|%s"%(t,who,",".join("%s:%d:%d"%(a,p[a][0],p[a][1])for a in q if a in p))
	def bG(line):f=line.split("|");return "|".join(f[:2])if len(f)>2 else None
	def aQ(line):
		f=line.split("|");a={}
		try:
			b=f[1].upper();e="S%d"%int(b[1:])if b[:1]=="S"else int(b,16)
			for d in f[2].split(","):
				if d:c=d.split(":");a[c[0]]=(int(c[1]),int(c[2]))
			return(int(f[0]),e,tuple(a[g][0]if g in a else 0 for g in q),tuple(a[h][1]if h in a else 0 for h in q))
		except(IndexError,ValueError):return
	def cY():
		f,b,g,h,c=dict(d["vendors"]),dict(d["reads"]),{},{},[]
		for(a,k),l in list(d["hist"].items()):
			for t,m,n in list(l["rows"]):g.setdefault((a,t),{})[k]=(m,n)
		for o,v in f.items():h.setdefault(v["shop"],[]).append(o)
		for(a,t),p in sorted(g.items()):e=h.get(a,[]);i=[r for r in e if r in b and b[r]["t"]==t];j=i[0]if len(i)==1 else e[0]if len(e)==1 else None;c.append(aP(t,"S%d"%a if j is None else "%X"%j,p))
		c.extend(aP(x["t"],"%X"%w,x["p"])for w,x in sorted(b.items())if w in f);return c
	def bH():
		a=b["log_lock"]
		if not a.acquire(False):return
		try:c=cZ()
		except Exception:c=False
		finally:a.release()
		if not c:
			b["hist_at"]=time.time()+ae;b["hist_fails"]+=1
			if b["hist_fails"]==2:u("couldn't write %s (trying again)."%bf,Kit.HUE_BAD)
			return
		b["hist_fails"]=0
	def cZ():
		q,g=b["histq"],b["drops"];n,k=len(q),len(g);l=Kit.data_path(bf);c=Kit.read_merge(l)
		if c is None:return False
		p=(cY()if not b["obs_ok"]and not c.strip()else[])+q[:n];f={}
		for m,s in g[:k]:f[m]=max(s,f.get(m,0))
		t=Kit.merge_text(c,dict((bG(v),v)for v in p),bG)[1];u=b["memo"];h=[]
		for x in t:
			r=u.get(x)or aQ(x)
			if r is not None and not(r[1]in f and r[0]<=f[r[1]]):h.append((r,x))
		h.sort(key=lambda e:e[0][0]);i={};a=[]
		for r,x in reversed(h):
			if len(a)>=aI:break
			if i.get(r[1],0)<bg:i[r[1]]=i.get(r[1],0)+1;a.append((r,x))
		a.reverse();o="\n".join(w for y,w in a)
		if o!="\n".join(G.rstrip("\r")for G in c.split("\n")if G.strip()):Kit.write_safe(l,o+"\n"if a else "")
		j={}
		for r,x in a:j.setdefault(r[1],[]).append((r[0],r[2],r[3]))
		for r in[aQ(M)for M in q[n:]]:
			if r is not None:j.setdefault(r[1],[]).append((r[0],r[2],r[3]))
		b["memo"]=dict((bh,ah)for ah,bh in a);d["obs"]=j;b["obs_ok"]=True;del q[:n];del g[:k];return True
	def bI(now):return(b["loaded"]and HOST.settled_at is not None and now>=b["hist_at"]and(not b["obs_ok"]or bool(b["histq"])or bool(b["drops"])))
	def bJ():
		a=b["log_lock"]
		if not a.acquire(False):return
		try:c=c_()
		finally:a.release()
		if not c:
			b["log_at"]=time.time()+ae;b["log_fails"]+=1
			if b["log_fails"]==2:u("couldn't write %s (trying again)."%be,Kit.HUE_BAD)
			return
		b["log_fails"]=0
	def c_():
		q=b["logq"];n=len(q);c=Kit.data_path(be);d=Kit.read_safe(c)
		if d is None:return False
		a=[e for e in d.replace("\r","").split("\n")if e.strip()];a=(a[1:]if a and a[0].lower().startswith("time,")else a)+q[:n]
		try:Kit.write_safe(c,"\n".join([cu]+a[-aH:])+"\n")
		except Exception:return False
		del q[:n];return True
	def c0(serial,now,got):
		c=d["reads"].get(serial)
		if c is not None and now-c["t"]<b_ and c["p"]==got:return
		a=API.FindMobile(serial);e=(int(API.GetMap()),int(a.X),int(a.Y))if a else None
		try:f=Y(a.Name)if a else ""
		except Exception:f=""
		g={"serial":serial,"t":int(now),"p":got,"spot":e,"name":f};b=H(serial)
		if b is None:b=cW(e)
		if b is None:bB("read",serial,g,cJ())
		else:bE(g,b)
	def c1(now):
		d=b["ask"];a=cy()
		if d is not None and d["mode"]=="read"and(a is None or a[1]==d["serial"]):return
		if a is None:
			b["seen"]=None
			if b["here"]is not None:b["here"]=None;ac();z()
			return
		if b["seen"]is a[0]:
			e=aV()
			if b["here"]is not None and e!=b["pv"]:b["pv"]=e;ac()
			return
		c=cz(a[1])
		if c is not None and max([g[1]for g in c]or[0])<=0:return
		b["seen"]=a[0]
		if c is None:return
		f=cE(c)
		if f or H(a[1])is not None:b["here"],b["pv"]=a[1],aV();ac();c0(a[1],now,f);c2(a[1],now);z()
		elif b["here"]is not None:b["here"]=None;z()
	def c2(serial,now):
		i=H(serial);a=b["miss"];e=False
		try:f=(int(API.GetMap()),int(API.Player.X),int(API.Player.Y))
		except Exception:return
		for s in aj(True).get(i,[])if i is not None else():
			v=d["vendors"][s];c=v["spot"]
			if s==serial:continue
			try:j=API.FindMobile(s)
			except Exception:continue
			if j is not None:
				a.pop(s,None)
				try:g=""if v.get("name")else Y(j.Name)
				except Exception:g=""
				if g:v["name"]=g;B("V|%X"%s);e=True
				continue
			if not c or c[0]!=f[0]or max(abs(c[1]-f[1]),abs(c[2]-f[2]))>cn:continue
			h=a.get(s)
			if h is None or h<v.get("last",0):a[s]=now
			elif now-h>=cm:v["gone"]=int(now);a.pop(s);B("V|%X"%s);e=True
		for s in sorted(a,key=a.get)[:max(0,len(a)-az)]:del a[s]
		if e:b["bookver"]+=1
	def bK(text):
		w=ai.get(text)
		if w is None:
			if len(ai)>=cb:ai.clear()
			w=ai[text]=cD(text)
		return w
	def ab(head,tail="",end=""):
		a=head+tail+end
		while bK(a)>a5:
			if tail:tail=tail[:-1].rstrip();a=head+tail+".."+end
			elif end:end=end[:-1];a=head+end
			else:head=head[:-1];a=head
		return a
	def bL(t):a=time.localtime(t);return "%d %s %02d:%02d"%(a.tm_mday,cf[a.tm_mon-1],a.tm_hour,a.tm_min)
	def c3(now):
		k=R();m=R(now);n=am(vp=k);o=am(vp=m);g=S(o);w=S(n);x=l["old"]*ag;e={};f={}
		for p,B in k.items():a=H(p);f[a]=f.get(a,0)+1;e[a]=max(e.get(a,0),d["reads"][p]["t"])
		def r(row):return "%d%s"%(row[0],"*"if now-row[2]>x else "")
		b=[[ab("%s %s "%(G,r(g[G][1])),C(g[G][0]))if G in g else "%s - (old)"%G if G in w else "%s - (no read)"%G for G in q]];D,y,A,h=bs(o,m);i=["Best stops","For: your list"if y else "For: 1 of each"]
		if not h:i.append("No prices yet"if A else "Nothing to buy")
		i+=[ab("%d "%(ah+1),C(M[3])," "+an(M[1]))for ah,M in enumerate(h)];b.append(i+[ab("",C(bh[3]),": "+bt(bh))for bh in h if bh[0]])
		for a in W()[:P-2]:
			s=n.get(a,{});c=[ab("",C(a))]
			if a not in e:c.append("Not read yet")
			else:
				c.append("Read "+bL(e[a]))
				if f[a]>1:c.append("%d vendors"%f[a])
				for j,z in ce:t,u=[r(s[dC])if dC in s else "out"for dC in(j,z)];v="%s %s  %s %s"%(a6[j],t,a6[z],u);c.append(ab("",v if bK(v)<=a5 else "%s %s  %s %s"%(j,t,z,u)))
			b.append(c)
		b+=[[]for dD in range(P-len(b))];return[(dE+[""]*T)[:T]for dE in b]
	def c4(view):a,b=view["lines"],view["known"];c=(0 in b and len(a)>=T and all(a[e].startswith(f+" ")for e,f in enumerate(q)));d=all(g in b for g in range(view["pages"]))and not any(h.strip()for h in a);return view["title"].strip()==a4 or c or d
	def c5(view,now):
		if not l["book_head"]:return
		a=X();c=d["reads"][a]["t"]if a is not None else now;b=(a4,"Updated "+bL(c),view["new"]);return b if(view["title"],view["author"])!=b[:2]else None
	def bM(serial):
		b,c=Kit.top_of(serial)
		if c and b==int(API.Bank or 0):a=Kit.find_item(b);return a is not None and bool(a.Opened)
		if c:return b==int(API.Backpack or 0)
		a=Kit.find_item(b)
		try:return a is not None and int(a.Distance)<=ca
		except Exception:return False
	def at(a,text):
		if text not in a["said"]:a["said"].add(text);u(text,Kit.HUE_BAD)
	def au():
		if b["foreign"]is not None:b["foreign"]=None;z()
	def c6(a,serial,view,now):
		if not view["edit"]:at(a,"couldn't write the book (can't be written).");return False
		if not bM(serial):at(a,"couldn't write the book (too far away).");return False
		if serial not in b["ok_books"]and not c4(view):
			if b["foreign"]!=serial:b["foreign"]=serial;z();u("the book holds other writing: press Overwrite to write over it.")
			return False
		try:e=c3(now)
		except Exception:a["ver"]=b["bookver"];return False
		b["ok_books"].discard(serial);au();n=min(view["pages"],P)
		if n<P:at(a,"book has %d pages; %d needed."%(n,P))
		c=len(d["shops"])-(P-2)
		if c>0:at(a,"the book holds %d shops; %d left out."%(P-2,c))
		a.update({"ver":b["bookver"],"todo":e[:n],"sent":set(),"head":c5(view,now)});return True
	def c7(now):
		d=b["book_serial"];g=cA(d)if d else None;a=b["book"]
		if g is None:
			if a is not None:b["book"]=None;au()
			return
		if a is None or a["g"]is not g:a=b["book"]={"g":g,"at":now,"ver":None if l["book_open"]else b["bookver"],"said":set(),"todo":None,"sent":set(),"head":None}
		if a["todo"]is None and a["ver"]==b["bookver"]:return
		c=cB(g)
		if c is None or c["typing"]or not c["known"]and now-a["at"]<b9:return
		if a["todo"]is None:
			if not c6(a,d,c,now):return
		elif not c["edit"]or not bM(d):a["todo"],a["ver"]=None,None;return
		h=c["lines"];e=[(k+1,m)for k,m in enumerate(a["todo"])if k+1 not in a["sent"]and h[k*T:(k+1)*T]!=m][:b8];f,a["head"]=a["head"],None
		if not e and f is None:a["todo"]=None;return
		if cC(g,d,e,f):a["sent"].update(i for i,n in e)
		else:a["todo"]=None
	def c8():
		if b["picking"]is not None:return
		a=b["picking"]=object();u("target the book for the prices.",Kit.HUE_INFO)
		def c(serial):
			if b["picking"]is not a:return
			b["picking"]=None;E.add(("book_picked",int(serial or 0)),dup=True,front=True)
		HOST.pick_target(cc,c,J)
	def c9(serial):
		if not serial:u("no book picked.",Kit.HUE_INFO);return
		if Kit.find_item(serial)is None:u("that isn't an item.",Kit.HUE_BAD);return
		b.update({"book_serial":serial,"book":None,"ok_books":set()});au();av();Kit.put_var(a3,"%X"%serial);u("book picked; open it to write the prices.",Kit.HUE_GOOD);aW(J)
	def da():
		if b["foreign"]is not None:b["ok_books"].add(b["foreign"]);au()
	def Y(text):return " ".join(str(text or "").replace("|"," ").split())[:aA]
	def bN(name):
		for a,s in d["shops"].items():
			if s["name"].lower()==name.lower():return a
		a=max(list(d["shops"])+[len(aZ)])+1;b=max([c["order"]for c in d["shops"].values()]+[0])+1;d["shops"][a]={"name":name,"order":b,"spot":None,"tail":[]};B("P|%d"%a);return a
	def db(sid):
		av()
		if sid not in d["shops"]:return
		if len(d["shops"])==1:u("keep at least one shop.",Kit.HUE_BAD);return
		g=C(sid);del d["shops"][sid];B("P|%d"%sid);h=int(time.time());e=b["drops"]
		for a in[i for i,m in d["vendors"].items()if m["shop"]==sid]+["S%d"%sid]:
			d["obs"].pop(a,None);e.append((a,h))
			if a not in d["vendors"]:continue
			del d["vendors"][a];B("V|%X"%a)
			if d["reads"].pop(a,None)is not None:B("R|%X"%a)
		del e[:-az]
		for f in[n for n in d["hist"]if n[0]==sid]:del d["hist"][f];B("H|%d|%s"%f)
		c=b["ask"]
		if c is not None and c["mode"]=="change"and H(c["serial"])is None:b["ask"]=None
		b["seen"]=None;b["bookver"]+=1;u("removed %s."%g,Kit.HUE_INFO);z()
	def bO(name,sid=None):return any(c["name"].lower()==name.lower()and a!=sid for a,c in d["shops"].items())
	def aR(*c):
		for a,b in list(D["tb"].items()):
			try:D["typed"][a]=str(b.Text or "")
			except Exception:continue
	def av():
		aR();e=D["typed"];f=False
		for a in[g for g in e if g!="add"]:
			c=Y(e.pop(a))
			if a not in d["shops"]or not c or c==d["shops"][a]["name"]:continue
			if bO(c,a):u("%s is already a shop."%c,Kit.HUE_BAD);continue
			d["shops"][a]["name"]=c;B("P|%d"%a);f=True
		if f:b["bookver"]+=1;z()
	def dc():
		av();a=Y(D["typed"].get("add",""))
		if not a:u("type a name for the new shop.",Kit.HUE_BAD);return
		if bO(a):u("%s is already a shop."%a,Kit.HUE_BAD);return
		D["typed"].pop("add",None);bN(a);b["bookver"]+=1;u("added %s."%a,Kit.HUE_GOOD);z()
	def dd():l["grid"]=not l["grid"];aJ();aa()
	def de(serial,sid):
		v,c=d["vendors"].get(serial),d["reads"].get(serial)
		if v is None or v["shop"]==sid:return
		for a,(f,g)in(c["p"].items()if c else()):
			h,e=d["hist"].get((v["shop"],a)),(c["t"],f,g)
			if h is None or e not in h["rows"]:continue
			h["rows"].remove(e);B("H|%d|%s"%(v["shop"],a));bC(sid,a,e)
			if not h["rows"]:del d["hist"][(v["shop"],a)]
		bD(serial,sid,v["spot"],True);b["bookver"]+=1
	def df():
		a,c=b["ask"],V["c"]
		if a is None or "ask_dd"not in c:return
		try:d=int(c["ask_dd"].GetSelectedIndex())
		except Exception:return
		if d==a["pick"]:return
		a["pick"]=d;e=d>=len(c["ask_ids"])
		if e!=a["new"]:a["new"]=e;z()
	def dg():
		a,c=b["ask"],V["c"]
		if a is None or "ask_dd"not in c:return
		d=c["ask_ids"];f=int(c["ask_dd"].GetSelectedIndex())
		if 0<=f<len(d):e=d[f]
		else:
			g=Y(c["ask_name"].Text)if "ask_name"in c else ""
			if not g:
				if a["new"]:u("type a name for the new shop.",Kit.HUE_BAD)
				a["new"],a["pick"]=True,len(d);z();return
			e=bN(g)
		b["ask"]=None
		if a["mode"]=="read":bE(a["pend"],e,True)
		else:de(a["serial"],e);z()
	def dh():
		a=X()
		if a is not None and b["ask"]is None:bB("change",a,None,W().index(H(a)))
	def di():b["ask"]=None;z()
	def ac():
		if any(l[a]for a in K)and("count",)not in b["jobs"]:b["jobs"].append(("count",))
	def dj():
		a=dict((e,0)for e in q)
		try:d=HOST.pack_items(True,cl)
		except Exception:return
		for b in d:
			try:
				c=aY.get(int(b.Graphic))
				if c is not None:a[c]+=max(1,int(b.Amount or 1))
			except Exception:continue
		E.add(("counted",a),dup=True)
	def dk(got):
		if got!=b["have"]:b["have"]=got;b["bookver"]+=1;z()
	def dl(serial):
		try:a=API.ContextMenu(serial,ch,ci)
		except Exception:a=False
		b["menu"]=False
		if not a and not b["shutting"]:u("couldn't open that vendor's buy list.",Kit.HUE_BAD)
	dm={"count":dj,"menu":dl}
	def dn(m,me):
		a=int(m.Serial)
		if a==me:return False
		if H(a)is not None:return True
		if int(m.Notoriety)!=cj:return False
		b=("%s %s"%(m.Name or "",m.raw.NameAndProps(False)or "")).lower().split();return any(c in b for c in cg)
	def bP():
		a,b=None,aD+1
		try:c=int(API.Player.Serial)
		except Exception:c=0
		for m in HOST.mobiles(aD):
			try:
				d=int(m.Distance)
				if d<b and dn(m,c):a,b=int(m.Serial),d
			except Exception:continue
		return a
	def do():
		if b["menu"]:return
		a=bP()
		if a is None:u("no reagent vendor in reach.",Kit.HUE_INFO);return
		b["menu"]=True;b["jobs"].append(("menu",a))
	def dp():
		a=b["followed"];c=a if a is not None and aS()==a else bP()
		if c is None:u("no reagent vendor in reach.",Kit.HUE_INFO);return
		b["followed"]=c if Follow.toggle(c,N)else None
	bQ=Kit.once(lambda:E.add("buy",key=J),(J,"buy"));dq=Kit.once(lambda:E.add("follow",key=J),(J,"follow"))
	def dr(*a):
		if Follow.alt_held():dq();return
		bQ()
	def ds(*d):
		a=time.time();c=a-b["hk_at"]<ck;b["hk_at"]=a
		if not c and not HOST.typing():bQ()
	def bR():
		a=_norm_key(l["hk"])if l["hk"]else ""
		if a==(b["hooked"]or ""):return
		if b["hooked"]:aT(b["hooked"],N)
		b["hooked"]=None
		if not a:return
		if HOST.hotkey_on(a,N,ds,"open a reagent vendor's buy list")is False:u("%s isn't a key."%l["hk"],Kit.HUE_BAD);return
		b["hooked"]=a
	bS={"show":z,"ask_ok":dg,"ask_skip":di,"change":dh,"pick_book":c8,"book_picked":c9,"overwrite":da,"counted":dk,"buy":do,"follow":dp,"view":dd,"rm_shop":db,"add_shop":dc}
	def dt(f,x,y):
		g=D["tb"];g.clear();D["n"]=len(d["shops"]);b=x+f.w-12-35-Kit.text_w("Remove")
		for i,a in enumerate(W()+["add"]):
			c=y+i*ba;e=a=="add";h=""if e else C(a);g[a]=Kit.with_tip(Kit.add_textbox(f.g,D["typed"].get(a,h),x+12,c,b-20-x,numbers=False),("Name of a new shop"if e else "Type a new name to rename this shop")+" (up to %d letters)"%aA)
			if e:Kit.art_button(f.g,f.store,"add_shop",Kit.ART_PLAY,b,c-2,"Add","Add a shop with this name",on_click=E("add_shop"))
			else:Kit.art_button(f.g,f.store,"rm_%d"%a,Kit.ART_CLOSE,b,c-2,"Remove","Remove %s and its prices"%h,on_click=E(("rm_shop",a)))
	def du(w):return(("BOOK",(("buttons",(("pick_book",Kit.ART_PLAY,"Pick book...","Target the book the prices go in",E("pick_book")),)),("note","Book picked: open it to write"if b["book_serial"]else "No book picked yet"),("check","book_open","Write when opened","Write the prices each time you open the book"),("check","book_head","Set title and date","Title the book Reagent Prices, with the last read's date as its author"))),("SHOPPING LIST",tuple(("num",a,Kit.REAGENTS[a[5:]][0]+":","How many to keep in your backpack, bags included; 0 = not on the list","",0,aE)for a in K),{"align":True}),("SHOPS",(("custom",ba*(len(d["shops"])+1),dt),)),("OPTIONS",(("check","say","Journal line after each read","Say the shop and what it's cheapest for"),("check","skip_old","Skip old prices for the cheapest","Leave prices past Old after out of the cheapest and best stops"))),("NUMBERS",(("num","dist","Shop distance:","A vendor this close to a known shop belongs to it","tiles",5,60),("num","old","Old after:","A price this old shows grey, with * in the book","days",1,60)),{"align":True}),("HOTKEYS",(("text","hk","Buy list:","Key for the Buy list button (F5, CTRL+Q, SHIFT+F2; blank = none)",{"tw":100}),)))
	def dv(old,new):
		if any(old[a]!=new[a]for a in K):ac()
		if any(old[c]!=new[c]for c in K+("old","skip_old")):b["bookver"]+=1;E.add("show")
	aw=Kit.Page(l,du,aJ,dv,final=True,adjust=aR)
	def dw():aw.closed();av();D["tb"].clear();D["typed"].clear();bR()
	def dx():
		import _thread;b.update({"shutting":False,"docked":False,"queue":[],"loaded":False,"seen":None,"check_at":0.,"aged_at":0.,"save_at":0.,"ask":None,"load_fails":0,"book":None,"foreign":None,"ok_books":set(),"picking":None,"minimized":L.start_min(),"jobs":[],"have":None,"here":None,"hooked":None,"menu":False,"followed":None,"hk_at":0.,"pv":None,"logq":[],"log_at":0.,"log_fails":0,"log_lock":_thread.allocate_lock(),"histq":[],"drops":[],"hist_at":0.,"hist_fails":0,"obs_ok":False,"memo":{},"miss":{},"size":cN(),"resize_at":0.,"drawn":None});d.update({"shops":{},"vendors":{},"reads":{},"hist":{},"dirty":{},"marks":0,"obs":{}});a,c=bj.pop("text",None),bj.pop("at",0.)
		if a is not None and time.time()-c<b3:bq(a)
		cx();bR();ac();aa();L.dock(fit=True,min=bA)
	def dy():
		q=b["queue"]
		while q:
			c=q.pop(0)
			if L.action(c):continue
			if type(c)is tuple:bS[c[0]](*c[1:])
			else:bS[c]()
		a=time.time();df()
		if b["loaded"]and a>=b["check_at"]:b["check_at"]=a+bY;c1(a);c7(a)
		if a>=b["aged_at"]:b["aged_at"]=a+bZ;ar()
		if b["resize_at"]and a-b["resize_at"]>=cp and not(SNAP.drag or SNAP.pressed()is True):b["resize_at"]=0.;cP()
	def dz():
		c=b["jobs"]
		while c and not b["shutting"]:e=c.pop(0);dm[e[0]](*e[1:])
		a=time.time()
		if b["logq"]and a>=b["log_at"]:bJ()
		if bI(a):bH()
		if a<b["save_at"]:return
		if not b["loaded"]:bq()
		elif d["dirty"]:br()
	def dA():a=time.time();return bool(b["jobs"])or bool(b["logq"])and a>=b["log_at"]or bI(a)or(not b["loaded"]or bool(d["dirty"]))and a>=b["save_at"]
	def dB():
		b["shutting"]=True;aJ()
		if b["hooked"]:aT(b["hooked"],N);b["hooked"]=None
		if b["followed"]is not None and aS()==b["followed"]:Follow.stop(N)
		b["followed"]=None
		if b["loaded"]and d["dirty"]:br()
		if b["logq"]:bJ()
		if b["loaded"]and(b["histq"]or b["drops"]):bH()
		bi.close()
	return{"start":dx,"tick":dy,"stop":dB,"client_tick":True,"config_height":aw.height,"build_config":aw.build,"poll_config":aw.poll,"config_closed":dw,"thread_tick":dz,"thread_wanted":dA}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("prices","Reagent Prices","Reagent prices and a price book",_module_prices,.25,category="The world")
