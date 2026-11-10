def _module_butler():
	aq=HOST.alert;aV=HOST.alert_kind;aW=HOST.claim_cursor;ar=HOST.cursor_busy;aX=HOST.cursor_ok;A=HOST.release_cursor;H=Kit.ART_CLOSE;at=Kit.ART_OK;au=Kit.ART_PAGE;av=Kit.ART_PLAY;n=Kit.GAP;D=Kit.HUE_BAD;E=Kit.HUE_GOOD;f=Kit.HUE_INFO;Z=Kit.HUE_TEXT;aa=Kit.HUE_TITLE;l=Kit.MARGIN;u=Kit.add_label;N=Kit.add_section;F=Kit.art_button;aY=Kit.catcher;aw=Kit.fit;O=Kit.get_var;ax=Kit.is_open;I=Kit.put_var;ay=Kit.row_clicker;ab=Kit.row_set;j=Kit.set_text;m=Kit.text_w;ac=Kit.zone_up;g="butler";ad="Property Butler";aZ="PropertyButler_settings";bD="PropertyButler_pos";bE="PropertyButler_min";az="PropertyButler_view";a_="PropertyButler_log";bF="PropertyButler_log_pos";aA=520;aB,bG=300,46;bH=3026;P=8;Q=22;aC=3;G=30;aD=520;R=18;bI=1.;aE=2.5;ae=200;a0=15.;a1="PropertyButler_visits";a2="PropertyButler_log_view";S="butler.log";a3="Property Butler Log";bJ=4;aF=2*l+30+n+30+8;af=30;bK=60.;bL=5.;bM=2.;bN=6;a4=10.;bO="ultima.is_foe";bP="Detect Hidden";bQ=10.;a5,aG=3.,120.;bR=12;a6,a7=1,18;T=3.;aH=3.;bS=1.;ag=1.5;ah=3.;a8=1.;bT=.3;bU=.1;a9=.5;bV=497;aI="butler.revealed";ba="butler.foe";bW=824;ai=HOLD_TEXT["unknown"];bX=("must wait a few moments to use another skill","must wait to perform another action");bY=("you can see nothing hidden there",);bZ=("reveal one other person","reveal several people","you carefully check the house");b_={"eject":("has been ejected from this house",),"ban":("has been banned from this house",),"friend":("is now a friend of this house","made a friend of this house"),"lock":("locked down!",),"release":("no longer locked down",)};b0=("you are not around your house","not a co-owner of this house","only the house owner","this person is already banned","is already the house owner","already a house owner","cannot eject a friend","not in your house","already a friend","cannot be a friend of the house","can't be a friend of the house","is already locked down","isn't locked down","is not locked down","cannot lock","cannot be locked down","refuse to lock this down","did not lock this down","may not release this","locked down items would be exceeded","place it on the ground first","when the front door is open");U={"eject":("eject_cmd","ejected","mobile"),"ban":("ban_cmd","banned","mobile"),"friend":("friend_cmd","befriended","mobile"),"lock":("lock_cmd","locked down","item"),"release":("release_cmd","released","item")};aj={"eject":"Eject","ban":"Ban","friend":"Befriend","lock":"Lock down","release":"Release"};b1="No players in range.";bb="No actions yet.";b2="No visits yet.";b={"cooldown":bQ,"range":bR,"still":False,"sound":True,"friends":True,"confirm":True,"eject_cmd":"Remove thyself","ban_cmd":"I ban thee","friend_cmd":"I wish to make this a friend","lock_cmd":"I wish to lock this down","release_cmd":"I wish to release this","eject_foes":False};aJ=dict(b);bc=("still","sound","friends","confirm","eject_cmd","ban_cmd","friend_cmd","lock_cmd","release_cmd",None,"eject_foes");a={"minimized":False,"shutting":False,"docked":False,"queue":[],"sweep":False,"next_at":0.,"deadline":0.,"cast_at":0.,"seen":set(),"sweeps":0,"revealed":0,"eject_at":{},"first_d":{},"reveal_line":False,"hooked":False,"scan_poke":False};d={"g":None,"c":{},"store":({},{}),"rows":[],"log_view":"log"};k={"g":None,"c":{},"store":({},{}),"rows":[],"minimized":False,"shutting":False,"docked":False,"w":aD,"queue":[]};aK,p,aL=Kit.basics(a,ad);r=[];q=[];bd={"innocent":90,"ally":68,"gray":946,"criminal":946,"murderer":33,"enemy":43,"invulnerable":53}
	def be():
		p=O(aZ).split("|")
		if len(p)>=8:
			for i,k,f,g,h in((0,"cooldown",a5,aG,float),(1,"range",a6,a7,int)):
				with Kit.quiet:b[k]=max(f,min(g,h(p[i])))
			n=len(p);p=p+[""]*(13-len(p))
			for i,k in enumerate(bc,2):
				if k:b[k]=p[i]=="1"if isinstance(aJ[k],bool)else(p[i]if i<n else aJ[k])
		a["sweep"]=O(az)=="1";del r[:]
		for e in O(a_).split("\n"):
			c=e.split("\t")
			if len(c)>=3:
				with Kit.quiet:r.append((float(c[0]),c[2],int(c[1])))
		del r[:-G];del q[:]
		for e in O(a1).split("\n"):
			c=e.split("\t",6)
			if len(c)>=7:
				with Kit.quiet:q.append([float(c[0]),float(c[1]),int(c[2]),c[6],c[3]or "unknown",max(1,int(c[4])),int(c[5])])
		del q[:-af];d["log_view"]="visits"if O(a2)=="visits"else "log"
	def bf():I(aZ,"|".join(["%.1f"%b["cooldown"],str(b["range"])]+["0"if c is None else("1"if b[c]else "0")if isinstance(aJ[c],bool)else b[c].replace("|","/")for c in bc]));I(az,"1"if a["sweep"]else "0")
	def bg():a["log_dirty"]=False;I(a_,"\n".join(["%d\t%d\t%s"%(c,h,e.replace("\t"," ").replace("\n"," "))for(c,e,h)in r[-G:]]))
	def bh():a["visits_dirty"]=False;I(a1,"\n".join(["%d\t%d\t%d\t%s\t%d\t%d\t%s"%(c[0],c[1],c[2],str(c[4]).replace("\t"," "),c[5],c[6],str(c[3]).replace("\t"," ").replace("\n"," "))for c in q[-af:]]))
	def ak():
		a["visits_dirty"]=True
		if d["log_view"]=="visits"and k["g"]is not None:a["visits_redraw"]=True
	def t(text,hue=None):hue=f if hue is None else hue;r.append((time.time(),text,hue));del r[:-G];a["log_dirty"]=True;aL(text+(""if text.endswith((".","!","?"))else "."),hue);aR()
	def i(text,secs=4.):a["note"],a["note_until"]=text,time.time()+secs
	def aM():return bool(API.HasTarget("any"))
	def al():return ar(g)is None and not aM()
	def V(name,width):return aw(name or "(unknown)",width)
	def bi(kind,serial):return(API.FindMobile if U[kind][2]=="mobile"else API.FindItem)(serial)
	def W(h):return aj[h["kind"]].lower(),h["name"]or "the target"
	aN=82;b3=150;J=20;b4=30+P*Q+8;b5=30+26+26+aC*J+8;b6=l+30+n+aN+n+b4+n+b5+l;b7=2;bj=60;aO="A house command is still running";bk="A target cursor is up: use it or press Esc";am=". Alt+click: auto-follow (again to stop)";bl="Set as last target"+am;B={"k":1.,"full":None}
	def b8():return B["k"],B["full"]
	def bm(ctrl,x,y):
		k=B["k"]
		if k!=1.:ctrl.SetPos(int(round(x*k)),int(round(y*k)))
		else:Kit.ui_pos(ctrl,x,y)
	def o(text):return 35+m(text)
	bn=((("pick_ej",av,"Eject...","Pick a player to eject","pick_eject"),("pick_ban",H,"Ban...","Pick a player to ban","pick_ban"),("pick_fr",at,"Friend...","Pick a player to befriend","pick_friend")),(("pick_lock",at,"Lock down...","Pick a house item to lock down","pick_lock"),("pick_rel",H,"Release...","Pick a locked-down item to release","pick_release"),("clear",H,"Clear log","Forget the actions below (visits stay)","clear_log"),("showlog",au,"Show log","Open or close the log window (last %d actions and visits)"%G,"show_log")))
	def b9(items,a,right):
		c,x,b=[],a,0
		for d in items:
			w=o(d)
			if x>a and x+w>right:x,b=a,b+1
			c.append((x,b));x+=w+16
		return c
	def bo():return o("Friend")+12+o("Eject")+12+o("Ban")
	def X():return 2*l+12+max(bo(),bj+6+m("18 tiles"))+10
	def K(w,h):
		M=l;b=w-2*M;d=M+30+n;x=max(o("Sweep: off"),o("Sweep: on"));p=10+x+16+o("Sweep now")<=b-4;q=aN if p else aN+26;y=min(m("999 sweeps, 999 revealed"),max(40,b-20-80));z=d+q+n;g=m("18 tiles");r=12+bj+6+g+10+bo()+10<=b;f=Q if r else 2*Q
		if r:s=M+b-10-o("Ban");i=s-12-o("Eject");j=i-12-o("Friend");t=j-10-g
		else:j=M+12;i=j+o("Friend")+12;s=i+o("Eject")+12;t=M+b-10-g
		A,e=[],0
		for F in bn:B=b9([cE[2]for cE in F],M+10,M+b-4);A.append([(cF,e+cG)for cF,cG in B]);e+=B[-1][1]+1
		C=(M+30+n+q+n+30+8+n+30+26*e+8+M)
		if h is None:c,a=P,aC
		else:
			u=h-C;a,c=aC,P
			while a>1 and c*f+a*J>u:a-=1
			while c>b7 and c*f+a*J>u:c-=1
			while c==P and a<G and c*f+(a+1)*J<=u:a+=1
		k=30+c*f+8;v=30+26*e+a*J+8;D=C-(30+8)-(30+26*e+8)+k+v
		if h is not None and h>D:k+=h-D
		E=z+k+n;return{"IW":b,"ys":d,"sweep_xy":(M+10,d+26),"sweep_h":q,"yv":z,"row_h":f,"now_xy":(M+10+x+16,d+26)if p else(M+10,d+52),"status_y":d+58 if p else d+84,"count_room":y,"status_room":max(40,b-20-y-10),"btn_dy":0 if r else Q,"x":(j,i,s,t),"dist_w":g,"name_w":max(20,min(b3,t-6-(M+12))),"empty":Kit.wrap(b1,max(60,b-24)),"act_rows":e,"groups":A,"rows_n":c,"log_n":a,"vis_h":k,"act_h":v,"ya":E,"h":E+v+M}
	def aP(title,hint,room):a="%s  (%s)"%(title,hint);return a if m(a)<=room else title
	def bp():
		q=C.slot
		if a["minimized"]:w,h=(max(aB,q[0])if q else aB),bG
		elif q is None:w,h=aA,b6
		else:w,h=q
		g,r,e=C.begin(w,h);M=l;L=[];k=1.;B["k"],B["full"]=1.,None
		if a["minimized"]:e["mini_w"]=w
		else:
			j,n,x=w,h,None
			if q is None:c=K(j,None);n=c["h"]
			elif w<X():
				k=w/float(X());c=K(X(),int(h/k))
				if c["h"]>int(h/k)+1:k=min(k,h/float(c["h"]))
				j,n=int(round(w/k)),int(round(h/k));c=K(j,n)
			else:
				c=K(j,n)
				if c["h"]>n+1:j=w-Kit.SCROLL_BAND;c=K(j,n);x=c["h"]
			d["P"]=c;i=c["IW"];C.frame(g,j,n);R=c["ys"];N(g,M,R,i,c["sweep_h"],aP("SWEEP","Detect Hidden on your spot",i-12));e["sweep_lbl"]=F(g,r,"sweep",au,c["sweep_xy"][0],c["sweep_xy"][1],"Sweep: off","Switch the automatic sweep: Detect Hidden on your spot whenever ready",on_click=p("sweep"));F(g,r,"now",av,c["now_xy"][0],c["now_xy"][1],"Sweep now","Use Detect Hidden once, if ready",on_click=p("now"));e["status"]=u(g,"",M+10,c["status_y"],f);e["count"]=u(g,"",M+i-10,c["status_y"],f);e["count_y"]=c["status_y"];s=c["yv"];S=m("99 near (%d shown)"%P);N(g,M,s,i,c["vis_h"],aP("VISITORS","players near you",i-12-S-16));e["near"]=u(g,"",M+i-10,s+6,f);e["near_y"]=s+6;T,U,V,O=c["x"];e["name_w"],e["hidden_w"]=c["name_w"],m(" (hidden)");y="Say the %s command at them";W=(("fr",at,T,"Friend",y%"friend"+am,"friend"),("ej",av,U,"Eject",y%"eject"+am,"eject"),("ban",H,V,"Ban",y%"ban"+("; click again within %d s to confirm"%int(ah)if b["confirm"]else "")+am,"ban"));Y,aa=c["row_h"],c["btn_dy"]
			for z in range(c["rows_n"]):
				t=s+30+z*Y;o={"val":None,"prev":None,"changed":0.};o["name_lbl"]=u(g,"",M+12,t+3,Z);o["dist_lbl"]=u(g,"",O,t+3,f);o["catch"]=aY(g,M+10,t,O-M-10+c["dist_w"],Q,ay(o,p,"last"),bl)
				for v,A,D,E,G,ab in W:o[v]=F(g,r,"%s%d"%(v,z),A,D,t+aa,E,G,on_click=ay(o,p,ab));o[v+"_btn"]=r[0]["%s%d"%(v,z)]
				L.append(o)
			e["empty"]=[u(g,cF,M+12,s+33+20*cE,f)for cE,cF in enumerate(c["empty"][:max(1,(c["vis_h"]-33)//20)])];I=c["ya"];N(g,M,I,i,c["act_h"],aP("ACTIONS","pick with a cursor",i-12))
			for ac,ad in zip(bn,c["groups"]):
				for(ae,A,E,G,af),(D,ag)in zip(ac,ad):F(g,r,ae,A,D,I+26+26*ag,E,G,on_click=p(af))
			ly=I+30+26*c["act_rows"];e["log"]=[u(g,"",M+12,ly+cG*J,f)for cG in range(c["log_n"])];e["log_w"],e["log_full"]=i-70,i-24
			if k!=1.:B["k"],B["full"]=k,(int(X()),int(round(K(X(),None)["h"])));Kit.scale_window(g,k)
			elif x is not None:w,h=j,x
			else:w,h=j,n
		C.end(g,{"rows":L},w,h,q[1]if(q is not None and not a["minimized"])else None);ca()
	C=Kit.Window(g,ad,a,d,bp,bD,bE,icon=bH,cleanup=aK,clear={"rows":[]})
	def ca():aR();br();bv()
	bq=("name_lbl","dist_lbl","catch","fr","fr_btn","ej","ej_btn","ban","ban_btn")
	def aQ(ctrl,on,row,key):
		if row.get(key+"_vis")!=on:row[key+"_vis"]=on;ctrl.IsVisible=on
	def br():
		f=d["rows"]
		if not f or a["minimized"]:return
		c=d["c"];e=a["visitors"];r=time.time();h,s=c["name_w"],c["hidden_w"]
		for i,b in enumerate(f):
			if i<len(e):
				v=e[i];ab(b,(v["serial"],v["name"]),r);t=(v["serial"],v["name"],v["noto"],v["hidden"],v["dist"],h,s)
				if b.get("sig")==t:continue
				b["sig"]=t;n=bd.get(v["noto"],Z)
				if v["hidden"]:n=aa;j(b["name_lbl"],V(v["name"],h-s)+" (hidden)",n)
				else:j(b["name_lbl"],V(v["name"],h),n)
				j(b["dist_lbl"],Kit.count(v["dist"],"tile"))
				for k in bq:aQ(b[k],True,b,k)
			else:
				ab(b,None,r);b["sig"]=None
				for k in bq:aQ(b[k],False,b,k)
		g=d["P"]["empty"];o=c.get("empty_k")
		if o is None or o[0]!=(not e)or o[1]is not g:
			c["empty_k"]=(not e,g)
			for i,x in enumerate(c["empty"]):j(x,g[i]if(not e and i<len(g))else "")
		u=c["near"];w=(a["near"],len(e)>len(f),len(f))
		if c.get("near_k")!=w:
			c["near_k"]=w;p="%d near"%a["near"]if a["near"]else ""
			if len(e)>len(f):p="%d near (%d shown)"%(a["near"],len(f))
			j(u,p);q=m(p)
			if c.get("near_w")!=q:c["near_w"]=q;y=d["P"]["IW"];bm(u,l+y-10-q,c["near_y"])
	def bs(a,width):t,b,c=a;return "%s  %s"%(time.strftime("%H:%M",time.localtime(t)),V(b,width)),c
	def aR():
		c=d["c"];a=c.get("log")
		if a:
			b=r[-len(a):]
			for i,e in enumerate(a):
				if i<len(b):g,h=bs(b[len(b)-1-i],c["log_w"]);j(e,g,h)
				else:j(e,aw(bb,c["log_full"])if i==0 else "",f)
		aS()
	def bt():return aD,aF+bJ*R
	def cb():
		if ac(S):L()
		else:z.close()
	def L():
		M=l;a=d["log_view"]=="visits";b=ac(S);x,y=(q,af)if a else(r,G);A,B=bt();c=z.slot if b and z.slot is not None and z.slot[0]>=A and z.slot[1]>=B else None;j=z.rows(R,aF,0)if c else min(y,max(10,(len(x)+9)//10*10));w,h=c if c else(aD,aF+j*R);C=h-M-30-n-M;g,e,E=z.begin(w,h);Kit.add_window_frame(g,w,h);N(g,M,M,w-2*M,30);u(g,a3.upper(),M+30,M+7,aa)
		if not b:F(g,e,"close",H,w-M-54,M+4,None,"Close the log",on_click=p("show_log"))
		k=w-M-(10 if b else 66)-35-m("Clear");F(g,e,"clear",H,k,M+4,"Clear","Forget these visits"if a else "Forget these actions",on_click=p("log_clear"));o="Actions"if a else "Visitors";F(g,e,"view",au,k-12-35-m(o),M+4,o,"Show what the butler did"if a else "Show who came into the house",on_click=p("log_view"));s=M+30+n;N(g,M,s,w-2*M,C,"VISITORS  (while you were inside)"if a else "ACTIONS  (newest first, %d kept)"%G);t=[]
		for D in range(j):
			v=s+30+D*R;i={"lbl":u(g,"",M+12,v,f),"catch":None,"val":None,"prev":None,"changed":0.}
			if a:i["catch"]=aY(g,M+10,v-1,w-2*M-20,R,ay(i,p,"last"),bl)
			t.append(i)
		z.end(g,{"rows":t,"w":w});aS()
	z=Kit.Window(S,a3,k,k,L,bF,default=(240,240),cleanup=aK,lock=True,owner=False,clear={"rows":[]})
	def cc(e,width,now):
		j,d,k,l,f,g,h=e;i=time.localtime(j);b=time.strftime("%H:%M"if i[:3]==time.localtime(now)[:3]else "%b %d %H:%M",i)
		if a["open_visits"].get(k)is e:b+=", inside"
		elif d:b+="-"+time.strftime("%H:%M",time.localtime(d))
		else:b+="-?"
		c=" (%s)"%f
		if g>1:c+="  %d times"%g
		if h:c+="  banned"if h==2 else "  ejected"
		m=max(60,width-Kit.text_px(b+"  "+c));return "%s  %s%s"%(b,V(l,m),c),bd.get(f,Z)
	def aS():
		t=k["g"]
		if not ax(t):return
		p=k["rows"];c=d["log_view"]=="visits";g=q if c else r
		if len(g)>len(p)and not ac(S):L();return
		n=len(g);h=time.time()
		for i,b in enumerate(p):
			if i<n:
				e=g[n-1-i]
				if c:
					s=(e[0],e[2],e[1],e[5],e[6],a["open_visits"].get(e[2])is e)
					if b.get("key")!=s:b["key"]=s;m,o=cc(e,k["w"]-2*l-28,h);j(b["lbl"],m,o)
					ab(b,(e[2],e[3]),h)
				else:m,o=bs(e,k["w"]-2*l-70);j(b["lbl"],m,o)
			else:j(b["lbl"],(b2 if c else bb)if i==0 else "",f);b["key"]=None;ab(b,None,h)
			if b["catch"]is not None:aQ(b["catch"],i<n,b,"catch")
	def cd(now):
		h=a["house"]or a["house_wait"]
		if h is not None:return("%s %s: waiting for the %s cursor"%(aj[h["kind"]],h["name"]or "the target","house"if a["house"]is not None else "sweep"),aa)
		if a["note"]and now<a["note_until"]:return a["note"],f
		if a["phase"]=="cursor":return "Detect Hidden: waiting for cursor",aa
		if a["phase"]=="cast":return "Detect Hidden: sweeping",E
		c=aU(now)
		if not a["sweep"]:return("Sweep off; ready in %d s"%int(c+.99)if c>0 else "Sweep off; ready"),f
		if a["held"]==ai:return ai,f
		if a["held"]:return "Sweep on, waiting: %s"%a["held"],f
		if c>0:return "Sweep on: next in %d s"%int(c+.99),E
		if b["still"]and now-a["moved_at"]<a8:return "Sweep on: stand still",f
		return "Sweep on: ready",E
	def ce():
		if a["house"]is not None or a["house_wait"]is not None:s="house command"
		elif a["phase"]!="idle":s="sweeping"
		elif a["sweep"]:s="sweep on, waiting"if a["held"]else "sweep on"
		else:s="sweep off"
		if a["near"]:s+=", %d near"%a["near"]
		return "%s: %s"%(ad,s)
	def bu(c,key,text,room):
		e=c.get(key)
		if e is not None and e[0]==text and e[1]==room:return e[2]
		a=V(text,room);c[key]=(text,room,a);return a
	def bv():
		c=d["c"]
		if d["g"]is None or(a["minimized"]and a["docked"]):return
		p=time.time();f,i=cd(p)
		if a["minimized"]:
			b=c.get("status")
			if b is not None:j(b,bu(c,"mini_k",ce(),c.get("mini_w",aB)-90),i)
			return
		P=d.get("P")or{};b=c.get("status")
		if b is not None:
			k=bu(c,"status_k",f,P.get("status_room",aA-2*l-160))
			if j(b,k,i):b.SetTooltip(f if k!=f else "")
		n=c.get("sweep_lbl")
		if n is not None:j(n,"Sweep: on"if a["sweep"]else "Sweep: off",E if a["sweep"]else Z)
		g=c.get("count");o=(a["sweeps"],a["revealed"],P.get("count_room",400))
		if g is not None and c.get("count_k")!=o:
			c["count_k"]=o;e=("%s, %d revealed"%(Kit.count(a["sweeps"],"sweep"),a["revealed"]));e=aw(e,P.get("count_room",400))
			if j(g,e)or c.get("count_w")is None:
				h=m(e)
				if c.get("count_w")!=h:c["count_w"]=h;q=P.get("IW",aA-2*l);bm(g,l+q-10-h,c["count_y"])
	def bw(now,me):
		if 0<=now-a["scan_at"]<(bU if a["scan_poke"]else bT):return False
		a["scan_at"]=now;a["scan_poke"]=False;g,h=int(me.X),int(me.Y);p=me.Serial
		if a["pos"]!=(g,h):a["pos"],a["moved_at"]=(g,h),now
		k=b["range"];q=API.GetAllMobiles(distance=k,isHuman=True)or[];c=a["ncache"]
		if len(c)>ae:
			for r in[s for s,v in c.items()if now>=v[0]]:del c[r]
			if len(c)>ae:c.clear()
		d=[]
		for m in q:
			try:
				e=m.Serial
				if e==p:continue
				i=c.get(e)
				if i is not None and now<i[0]:j,f=i[1],i[2]
				elif m.IsRenamable:c[e]=(now+aE,None,"pet");continue
				else:f=Kit.noto_name(m);j=str(m.Name or "");c[e]=(now+aE,j,f)
				if j is None or f=="invulnerable"or(f=="ally"and not b["friends"]):continue
				l,n=int(m.X),int(m.Y);o=max(abs(l-g),abs(n-h))
				if o>k:continue
				d.append({"serial":e,"name":j,"noto":f,"dist":o,"hidden":bool(m.IsHidden),"x":l,"y":n,"inside":False})
			except Exception:continue
		d.sort(key=cf);a["near"]=len(d);a["visitors"]=d;cg(now,g,h,d);br();return True
	def cf(v):return(v["dist"],v["name"].lower())
	def bx(x,y):return len(API.GetMultisAt(x,y)or())>0
	def cg(now,mx,b,out):
		if a["house_pos"]!=(mx,b)or now>=a["house_at"]:a["house_pos"],a["house_at"]=(mx,b),now+bM;a["in_house"]=bx(mx,b)
		c=a["open_visits"]
		if not a["in_house"]:a["inside"]={};by(now);return
		h=a["inside"];d={};f=bN
		for v in out:
			s=v["serial"];e=h.get(s)
			if e is None or e[0]!=v["x"]or e[1]!=v["y"]:
				if f>0:f-=1;e=(v["x"],v["y"],bx(v["x"],v["y"]))
				elif e is None:continue
			d[s]=e;g=e[2];v["inside"]=g
			if g:
				if s not in c:ch(v,now)
			elif s in c:aT(s,now)
		a["inside"]=d
		for s in[w for w in c if w not in d]:aT(s,now)
	def ch(v,now):
		s=v["serial"];e=next((c for c in reversed(q)if c[2]==s),None)
		if e is not None and e[1]and now-e[1]<=bK:e[1]=0.;e[5]+=1
		else:e=[now,0.,s,v["name"]or "someone",v["noto"],1,0];q.append(e);del q[:-af]
		a["open_visits"][s]=e;ak()
	def aT(s,now):
		e=a["open_visits"].pop(s,None)
		if e is not None:e[1]=now;ak()
	def by(now):
		for s in list(a["open_visits"]):aT(s,now)
	def ci(serial,flag):
		e=next((c for c in reversed(q)if c[2]==serial),None)
		if e is not None:e[6]=flag;ak()
	def cj(serial,name,now):
		b=HOST.services.get(bO)
		if b is None:return False
		c=a["foe"].get(serial)
		if c is not None and now<c[0]:return c[1]
		try:r=bool(b(serial,name))
		except Exception:r=False
		if len(a["foe"])>ae:a["foe"].clear()
		a["foe"][serial]=(now+aE,r);return r
	def ck(now):
		if not b["eject_foes"]or not a["in_house"]:return
		c=a["eject_at"];d=None
		for v in a["visitors"]:
			if not v["inside"]or v["hidden"]:continue
			s=v["serial"]
			if c.get(s,0.)>now:continue
			if v["noto"]!="murderer"and not cj(s,v["name"],now):continue
			if d is None:d={int(h)for h in list(API.GetPartyMemberSerials()or[])+list(API.GetAllFriends()or[])}
			if s in d:continue
			if len(c)>ae:
				for k in[w for w,x in c.items()if x<=now]:del c[k]
			c[s]=now+a4;e="red"if v["noto"]=="murderer"else "Foe"
			if not aq(ba,"%s (%s) in your house: Eject from their row?"%(v["name"]or "Someone",e),"alarm",who=s):t("%s (%s) stepped in"%(v["name"]or "someone",e),D)
			return
	def bz(now):
		a=HOST.fight_hold(now)
		if a=="dead":return HOLD_TEXT["dead"]
		g=HOST.guard_hold()
		if g=="guard":return HOLD_TEXT["guard"]
		if g is not None:return ai
		if a:return HOLD_TEXT.get(a,a)
		return HOLD_TEXT["alarm"]if HOST.alarm_up()else None
	def aU(now):b=a["next_at"]-now;return b if 0<b<=aG else 0.
	def bA(now,forced=False):
		if a["house"]is not None:
			if forced:i(aO)
			return False
		if a["phase"]!="idle":return False
		c=a["held"]
		if c:
			if forced:i(c if c==ai else "The sweep waits: %s"%c)
			return False
		d=aU(now)
		if d>0:
			if forced:i("Ready in %d s"%int(d+.99))
			return False
		if not forced and b["still"]and now-a["moved_at"]<a8:return False
		if not al():
			if forced:i("A target cursor is up: the sweep waits")
			return False
		e=HOST.me()
		if e is not None:a["scan_at"]=0.;bw(now,e)
		a["seen"]={h["serial"]for h in a["visitors"]if not h["hidden"]};a["first_d"]={};a["reveal_line"]=False;API.UseSkill(bP);aW(g,T);a["phase"],a["deadline"]="cursor",now+T;return True
	def cl(now):
		if a["phase"]=="cursor":
			if now>a["deadline"]:A(g);a["phase"],a["next_at"]="idle",now+ag;i("No Detect Hidden cursor; retrying")
			elif ar(g)is not None:return
			elif aX(g,"neutral"):API.TargetSelf();A(g);a["phase"],a["cast_at"]="cast",now;a["next_at"]=now+b["cooldown"];a["sweeps"]+=1
			elif aM():A(g);a["phase"],a["next_at"]="idle",now+ag;t("sweep dropped: a spell cursor came up",f)
			return
		if a["phase"]=="cast":
			if now-a["cast_at"]<=bS:
				c=a["first_d"];d=max(1,b["range"]-2)
				for v in a["visitors"]:
					if v["serial"]not in a["seen"]and not v["hidden"]:
						if c.setdefault(v["serial"],v["dist"])>d and not a["reveal_line"]:continue
						a["seen"].add(v["serial"]);a["revealed"]+=1;API.HeadMsg("* revealed *",v["serial"],D);t("revealed %s"%(v["name"]or "someone"),D)
						if b["sound"]:aq(aI,"Revealed %s"%(v["name"]or "someone"),"warn",who=v["serial"])
			if now-a["cast_at"]>aH:a["phase"]="idle"
	def cm(d):
		f=time.time();e=a["phase"]in("cursor","cast")or f-a["cast_at"]<aH
		if not e and a["house"]is None and a["house_wait"]is None:return
		c=d.low
		if e:
			if any(s in c for s in bX):
				if a["phase"]=="cursor":A(g)
				elif a["phase"]=="cast":a["sweeps"]=max(0,a["sweeps"]-1)
				a["phase"],a["next_at"]="idle",time.time()+ag;i("Skill delay: retrying");return
			if any(v in c for v in bY):return
			if any(w in c for w in bZ):
				a["reveal_line"]=True;i("Someone was revealed",6.)
				if b["sound"]:aq(aI,"Someone was revealed","warn")
				return
		h=a["house"]
		if h is None:return
		if any(x in c for x in b_[h["kind"]]):
			t("%s %s"%(U[h["kind"]][1],h["name"]or "the target"),E)
			if h["kind"]in("eject","ban"):ci(h["serial"],2 if h["kind"]=="ban"else 1)
			M();return
		if any(y in c for y in b0):t("%s %s failed: %s"%(W(h)+(d.text.strip(),)),D);M();return
	def an(kind,serial,name,now,waited=False):
		if a["house"]is not None or(a["house_wait"]is not None and not waited):i(aO);return
		if a["phase"]=="cursor":a["house_wait"]={"kind":kind,"serial":serial,"name":name,"until":now+T};a["confirm"]=None;return
		if not b[U[kind][0]]:i("Type the words for %s on the settings page"%aj[kind]);return
		if not al():i(bk);return
		if not name:name=str(safe(lambda:bi(kind,serial).Name,"")or "")
		API.Msg(b[U[kind][0]]);aW(g,T);a["house"]={"kind":kind,"serial":serial,"name":name,"deadline":now+T,"aimed":0.};a["confirm"]=None
	def M():a["house"]=None;A(g)
	def cn(now):
		b=a["house_wait"]
		if b is None:return
		if a["phase"]!="cursor"and al():a["house_wait"]=None;an(b["kind"],b["serial"],b["name"],now,waited=True)
		elif now>b["until"]:
			a["house_wait"]=None
			if a["phase"]=="cursor":A(g);a["phase"],a["next_at"]="idle",now+ag
			if al():an(b["kind"],b["serial"],b["name"],now,waited=True)
			else:i(bk)
	def co(now):
		h=a["house"]
		if h is None:return
		if not h["aimed"]:
			if now<=h["deadline"]:
				if ar(g)is not None:return
				if not aX(g,"neutral"):
					if aM():t("%s %s: dropped, a spell cursor came up"%W(h),D);M()
					return
				if bi(h["kind"],h["serial"])is None:API.CancelTarget();t("%s %s: out of sight"%W(h),D);M();return
				API.Target(h["serial"]);A(g);h["aimed"]=now
			else:t("%s %s: no house cursor (in your house, with the right? Else use the house sign)"%W(h),D);M()
			return
		if now-h["aimed"]>aH:t("%s aimed at %s (no reply seen)"%W(h));M()
	def cp(serial,name,now):
		if b["confirm"]:
			c=a["confirm"]
			if not(c and c[0]==serial and now<c[1]):a["confirm"]=(serial,now+ah,now);i("Ban %s? Click Ban again to confirm"%(name or "them"),ah);return
			if len(c)>2 and now-c[2]<.3:return
		an("ban",serial,name,now)
	def cq(action,now,me):a["sweep"]=not a["sweep"];I(az,"1"if a["sweep"]else "0");aL("sweep %s."%("on"if a["sweep"]else "off"),E if a["sweep"]else f)
	def cr(action,now,me):
		if me is not None and a["phase"]=="idle":a["held"]=bz(now)
		if me is not None and not bA(now,forced=True)and a["phase"]!="idle":i("A sweep is already running")
	def cs(action,now,me):
		if ax(k["g"]):cb()
		else:L()
	def ct(action,now,me):
		d["log_view"]="log"if d["log_view"]=="visits"else "visits";I(a2,d["log_view"])
		if ax(k["g"]):L()
	def bB(action,now,me):
		if action=="log_clear"and d["log_view"]=="visits":del q[:];a["open_visits"],a["inside"]={},{};ak()
		else:del r[:];a["log_dirty"]=True;aR()
	def cu(a):
		def b(serial):
			serial=int(serial or 0)
			if not serial:i("Nothing picked");return
			p.add((a,serial,None),dup=True)
		return b
	def Y(action,now,me):
		b=action[5:]
		if a["house"]is not None or a["house_wait"]is not None:i(aO)
		else:i("Target the %s to %s (Esc cancels)"%("player"if U[b][2]=="mobile"else "item",aj[b].lower()),a0);HOST.pick_target(a0,cu(b))
	def cv(action,now,me):API.SetLastTarget(serial=action[1]);API.HeadMsg("* last target *",action[1],53)
	def ao(action,now,me):an(action[0],action[1],action[2],now)
	bC={"sweep":cq,"now":cr,"show_log":cs,"log_view":ct,"log_clear":bB,"clear_log":bB,"pick_eject":Y,"pick_ban":Y,"pick_friend":Y,"pick_lock":Y,"pick_release":Y,"follow":lambda action,now,me:Follow.toggle(action[1],ad),"last":cv,"ban":lambda action,now,me:cp(action[1],action[2],now),"eject":ao,"friend":ao,"lock":ao,"release":ao};cw=("Foe: on Ultima Tracker's Foe list; once per player every %d s; Eject on their row ejects them"%int(a4));cx={"ldy":4,"fh":30,"ugap":6}
	def cy(w):a=(w-24)//2;c=max(m(h)for h in("Eject:","Ban:","Friend:"));d=max(m(s)for s in("Lock down:","Release:"));b,e={"lw":c,"tw":a-c-26},{"dx":12+a,"lw":d,"tw":a-d-26};return(("SWEEP  (Detect Hidden on your spot)",(("num","cooldown","Seconds between uses:","Wait after each use, the shard's skill delay",None,a5,aG,{"cast":float}),("check","still","Sweep only when standing still","Waits until you have stood still 1 s"),("check","sound","Alert when a sweep reveals someone","Sound: Settings > Alerts"))),("VISITORS",(("num","range","List players within:","Players this close are listed","tiles",a6,a7),("check","friends","List guild and alliance members too","Unticked, green players are left out"),("check","confirm","Ban needs a second click within %d s"%int(ah),"So the wrong person isn't banned"),("check","eject_foes","Alarm when a red or Foe enters the house",cw))),("HOUSE COMMANDS  (said out loud)",(("text","eject_cmd","Eject:","Ejects a player (owner, co-owner or friend)",b),("text","ban_cmd","Ban:","Bans a player (owner or co-owner)",b),("text","friend_cmd","Friend:","Makes a player a house friend (owner)",b),("gap",-90),("text","lock_cmd","Lock down:","Locks an item down (owner, co-owner or friend)",e),("text","release_cmd","Release:","Releases a locked-down item (owner or co-owner)",e),("gap",30),("note",Kit.wrap("Owner adds friends; owner and co-owners ban and release; friends eject and lock down.",w-28)[0],{"ndy":4,"h":24}))))
	def cz(b,new):
		if new["eject_foes"]!=b["eject_foes"]:a["eject_at"].clear()
		if new["confirm"]!=b["confirm"]and not a["minimized"]:p("redraw")()
	ap=Kit.Page(b,cy,bf,cz,cx,strict=True);be()
	def cA(*b):
		if not a["shutting"]and a["phase"]!="idle":a["scan_poke"]=True
	def cB():a.update({"shutting":False,"docked":False,"queue":[],"phase":"idle","house":None,"house_wait":None,"confirm":None,"visitors":[],"near":0,"scan_at":0.,"ncache":{},"log_dirty":False,"log_save_at":0.,"pos":None,"moved_at":0.,"note":"","note_until":0.,"in_house":None,"house_pos":None,"house_at":0.,"inside":{},"open_visits":{},"visits_dirty":False,"visits_save_at":0.,"visits_redraw":False,"eject_at":{},"foe":{},"held":None,"held_at":0.,"minimized":C.start_min()});C.slot=None;B.update({"k":1.,"full":None});be();a["rd"]=Journal.reader();aV(aI,"Someone revealed",bV);aV(ba,"Red or Foe in your house",bW);bp();Kit.hook_once(a,"hooked",("ApiMobileCreated",cA));C.dock(fit=True,exact=True,verify=True,drawn_at=b8);k.update({"shutting":False,"queue":[]});z.dock(fit=True,min=bt);aL("on; sweep %s, visitors within %d tiles%s."%("on"if a["sweep"]else "off",b["range"],", red or Foe alarm on"if b["eject_foes"]else ""),E)
	def cC():
		if d["g"]is None:return
		if Kit.closed(d):return
		b=time.time();g=HOST.me()
		while a["queue"]:
			c=a["queue"].pop(0);h=c[0]if isinstance(c,tuple)else c
			if not C.action(c)and h in bC:bC[h](c,b,g)
		if a["log_dirty"]and b>=a["log_save_at"]:a["log_save_at"]=b+bI;bg()
		if a["visits_dirty"]and b>=a["visits_save_at"]:a["visits_save_at"]=b+bL;bh()
		if a["visits_redraw"]:a["visits_redraw"]=False;aS()
		if k["queue"]:
			del k["queue"][:]
			if ac(S)or k["g"]is not None:L()
		if g is None:return
		for i in a["rd"].new():cm(i)
		if bw(b,g):ck(b)
		co(b)
		if a["house"]is None:
			if a["sweep"]and a["phase"]=="idle"and(aU(b)<=a9 or b>=a["held_at"]):
				a["held_at"]=b+a9;e=bz(b)
				if e!=a["held"]:
					j,a["held"]=a["held"],e
					if e and not j:t("sweep waits: %s"%(e[:1].lower()+e[1:]),f)
				if a["house_wait"]is None and not a["held"]:bA(b)
			cl(b);cn(b)
		if a["confirm"]and b>=a["confirm"][1]:a["confirm"]=None
		bv()
	def cD():
		a["shutting"]=k["shutting"]=True;a["house_wait"]=None;A(g);bf()
		if a["log_dirty"]:bg()
		if a["open_visits"]:by(time.time())
		if a["visits_dirty"]:bh()
		aK.close()
	return{"start":cB,"tick":cC,"stop":cD,"client_tick":True,"config_height":ap.height,"build_config":ap.build,"poll_config":ap.poll,"config_closed":ap.closed}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("butler","Property Butler","House sweeps, visitors, eject and ban",_module_butler,.1,category="Skills and home")
