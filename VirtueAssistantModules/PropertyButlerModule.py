def _module_butler():
	ar=HOST.alert;aW=HOST.alert_kind;aX=HOST.claim_cursor;at=HOST.cursor_busy;aY=HOST.cursor_ok;A=HOST.release_cursor;I=Kit.ART_CLOSE;au=Kit.ART_OK;av=Kit.ART_PAGE;aw=Kit.ART_PLAY;n=Kit.GAP;D=Kit.HUE_BAD;E=Kit.HUE_GOOD;f=Kit.HUE_INFO;aa=Kit.HUE_TEXT;ab=Kit.HUE_TITLE;l=Kit.MARGIN;u=Kit.add_label;P=Kit.add_section;F=Kit.art_button;aZ=Kit.catcher;a_=Kit.cb_hue;ax=Kit.fit;Q=Kit.get_var;ay=Kit.is_open;J=Kit.put_var;az=Kit.row_clicker;ac=Kit.row_set;j=Kit.set_text;m=Kit.text_w;ad=Kit.zone_up;g="butler";ae="Property Butler";a0="PropertyButler_settings";bG="PropertyButler_pos";bH="PropertyButler_min";aA="PropertyButler_view";a1="PropertyButler_log";bI="PropertyButler_log_pos";aB=520;aC,bJ=300,46;bK=3026;R=8;a2=22;aD=3;G=30;aE=520;S=18;bL=1.;aF=2.5;af=200;a3=15.;a4="PropertyButler_visits";a5="PropertyButler_log_view";T="butler.log";a6="Property Butler Log";bM=4;aG=2*l+30+n+30+8;ag=30;bN=60.;bO=5.;bP=2.;bQ=6;a7=10.;bR="ultima.is_foe";bS="Detect Hidden";bT=10.;a8,aH=3.,120.;bU=12;a9,ba=1,18;U=3.;aI=3.;bV=1.;ah=1.5;ai=3.;bb=1.;bW=.3;bX=.1;bc=.5;bY=497;aJ="butler.revealed";bd="butler.foe";bZ=824;aj=HOLD_TEXT["unknown"];b_=("must wait a few moments to use another skill","must wait to perform another action");b0=("you can see nothing hidden there",);b1=("reveal one other person","reveal several people","you carefully check the house");b2={"eject":("has been ejected from this house",),"ban":("has been banned from this house",),"friend":("is now a friend of this house","made a friend of this house"),"lock":("locked down!",),"release":("no longer locked down",)};b3=("you are not around your house","not a co-owner of this house","only the house owner","this person is already banned","is already the house owner","already a house owner","cannot eject a friend","not in your house","already a friend","cannot be a friend of the house","can't be a friend of the house","is already locked down","isn't locked down","is not locked down","cannot lock","cannot be locked down","refuse to lock this down","did not lock this down","may not release this","locked down items would be exceeded","place it on the ground first","when the front door is open");K={"eject":("eject_cmd","ejected","mobile"),"ban":("ban_cmd","banned","mobile"),"friend":("friend_cmd","befriended","mobile"),"lock":("lock_cmd","locked down","item"),"release":("release_cmd","released","item")};ak={"eject":"Eject","ban":"Ban","friend":"Befriend","lock":"Lock down","release":"Release"};b4="No players in range.";be="No actions yet.";b5="No visits yet.";b={"cooldown":bT,"range":bU,"still":False,"sound":True,"friends":True,"confirm":True,"eject_cmd":"Remove thyself","ban_cmd":"I ban thee","friend_cmd":"I wish to make this a friend","lock_cmd":"I wish to lock this down","release_cmd":"I wish to release this","eject_foes":False};aK=dict(b);bf=("still","sound","friends","confirm","eject_cmd","ban_cmd","friend_cmd","lock_cmd","release_cmd",None,"eject_foes");a={"minimized":False,"shutting":False,"docked":False,"queue":[],"sweep":False,"next_at":0.,"deadline":0.,"cast_at":0.,"seen":set(),"sweeps":0,"revealed":0,"eject_at":{},"first_d":{},"reveal_line":False,"hooked":False,"scan_poke":False};d={"g":None,"c":{},"store":({},{}),"rows":[],"log_view":"log"};k={"g":None,"c":{},"store":({},{}),"rows":[],"minimized":False,"shutting":False,"docked":False,"w":aE,"queue":[]};aL,p,aM=Kit.basics(a,ae);r=[];q=[];bg={"innocent":90,"ally":68,"gray":946,"criminal":946,"murderer":33,"enemy":43,"invulnerable":53}
	def bh():
		p=Q(a0).split("|")
		if len(p)>=8:
			for i,k,f,g,h in((0,"cooldown",a8,aH,float),(1,"range",a9,ba,int)):
				with Kit.quiet:b[k]=max(f,min(g,h(p[i])))
			n=len(p);p=p+[""]*(13-len(p))
			for i,k in enumerate(bf,2):
				if k:b[k]=p[i]=="1"if isinstance(aK[k],bool)else(p[i]if i<n else aK[k])
		a["sweep"]=Q(aA)=="1";del r[:]
		for e in Q(a1).split("\n"):
			c=e.split("\t")
			if len(c)>=3:
				with Kit.quiet:r.append((float(c[0]),c[2],int(c[1]),c[3]if len(c)>4 else "",int(c[4])if len(c)>4 else 0))
		del r[:-G];del q[:]
		for e in Q(a4).split("\n"):
			c=e.split("\t",6)
			if len(c)>=7:
				with Kit.quiet:q.append([float(c[0]),float(c[1]),int(c[2]),c[6],c[3]or "unknown",max(1,int(c[4])),int(c[5])])
		del q[:-ag];d["log_view"]="visits"if Q(a5)=="visits"else "log"
	def bi():J(a0,"|".join(["%.1f"%b["cooldown"],str(b["range"])]+["0"if c is None else("1"if b[c]else "0")if isinstance(aK[c],bool)else b[c].replace("|","/")for c in bf]));J(aA,"1"if a["sweep"]else "0")
	def bj():a["log_dirty"]=False;J(a1,"\n".join(["%d\t%d\t%s\t%s\t%d"%(c[0],c[2],c[1].replace("\t"," ").replace("\n"," "),c[3].replace("\t"," ").replace("\n"," "),c[4])for c in r[-G:]]))
	def bk():a["visits_dirty"]=False;J(a4,"\n".join(["%d\t%d\t%d\t%s\t%d\t%d\t%s"%(c[0],c[1],c[2],str(c[4]).replace("\t"," "),c[5],c[6],str(c[3]).replace("\t"," ").replace("\n"," "))for c in q[-ag:]]))
	def al():
		a["visits_dirty"]=True
		if d["log_view"]=="visits"and k["g"]is not None:a["visits_redraw"]=True
	def t(text,hue=None,name="",serial=0):hue=f if hue is None else hue;r.append((time.time(),text,hue,name or "",serial));del r[:-G];a["log_dirty"]=True;aM(text+(""if text.endswith((".","!","?"))else "."),hue);aS()
	def i(text,secs=4.):a["note"],a["note_until"]=text,time.time()+secs
	def aN():return bool(API.HasTarget("any"))
	def am():return at(g)is None and not aN()
	def V(name,width):return ax(name or "(unknown)",width)
	def bl(kind,serial):return(API.FindMobile if K[kind][2]=="mobile"else API.FindItem)(serial)
	def W(h):return ak[h["kind"]].lower(),h["name"]or "the target"
	def H(h):return(h["name"],h["serial"])if h["name"]and K[h["kind"]][2]=="mobile"else("",0)
	def X(name,serial,noto=None):a=Kit.noto_mark(noto)if noto else "";return(a+" "if a else "")+Kit.veil("name",name,serial)
	aO=82;b6=150;L=20;b7=30+R*a2+8;b8=30+26+26+aD*L+8;b9=l+30+n+aO+n+b7+n+b8+l;ca=2;bm=60;aP="A house command is still running";bn="A target cursor is up: use it or press Esc";an=". Alt+click: auto-follow (again to stop)";bo="Set as last target"+an;B={"k":1.,"full":None}
	def cb():return B["k"],B["full"]
	def bp(ctrl,x,y):
		k=B["k"]
		if k!=1.:ctrl.SetPos(int(round(x*k)),int(round(y*k)))
		else:Kit.ui_pos(ctrl,x,y)
	def o(text):return 35+m(text)
	bq=((("pick_ej",aw,"Eject...","Pick a player to eject","pick_eject"),("pick_ban",I,"Ban...","Pick a player to ban","pick_ban"),("pick_fr",au,"Friend...","Pick a player to befriend","pick_friend")),(("pick_lock",au,"Lock down...","Pick a house item to lock down","pick_lock"),("pick_rel",I,"Release...","Pick a locked-down item to release","pick_release"),("clear",I,"Clear log","Forget the actions below (visits stay)","clear_log"),("showlog",av,"Show log","Open or close the log window (last %d actions and visits)"%G,"show_log")))
	def cc(items,a,right):
		c,x,b=[],a,0
		for d in items:
			w=o(d)
			if x>a and x+w>right:x,b=a,b+1
			c.append((x,b));x+=w+16
		return c
	def br():return o("Friend")+12+o("Eject")+12+o("Ban")
	def Y():return 2*l+12+max(br(),bm+6+m("18 tiles"))+10
	def M(w,h):
		M=l;b=w-2*M;d=M+30+n;y=max(o("Sweep: off"),o("Sweep: on"));q=10+y+16+o("Sweep now")<=b-4;r=aO if q else aO+26;z=min(m("999 sweeps, 999 revealed"),max(40,b-20-80));A=d+r+n;g=m("18 tiles");s=12+bm+6+g+10+br()+10<=b;i=Kit.pitch(a2);f=i if s else 2*i
		if s:t=M+b-10-o("Ban");j=t-12-o("Eject");k=j-12-o("Friend");u=k-10-g
		else:k=M+12;j=k+o("Friend")+12;t=j+o("Eject")+12;u=M+b-10-g
		B,e=[],0
		for H in bq:C=cc([cH[2]for cH in H],M+10,M+b-4);B.append([(cI,e+cJ)for cI,cJ in C]);e+=C[-1][1]+1
		D=(M+30+n+r+n+30+8+n+30+26*e+8+M)
		if h is None:c,a=R,aD
		else:
			v=h-D;a,c=aD,R
			while a>1 and c*f+a*L>v:a-=1
			while c>ca and c*f+a*L>v:c-=1
			while c==R and a<G and c*f+(a+1)*L<=v:a+=1
		p=30+c*f+8;x=30+26*e+a*L+8;E=D-(30+8)-(30+26*e+8)+p+x
		if h is not None and h>E:p+=h-E
		F=A+p+n;return{"IW":b,"ys":d,"sweep_xy":(M+10,d+26),"sweep_h":r,"yv":A,"row_h":f,"now_xy":(M+10+y+16,d+26)if q else(M+10,d+52),"status_y":d+58 if q else d+84,"count_room":z,"status_room":max(40,b-20-z-10),"btn_dy":0 if s else i,"rh":i,"x":(k,j,t,u),"dist_w":g,"name_w":max(20,min(b6,u-6-(M+12))),"empty":Kit.wrap(b4,max(60,b-24)),"act_rows":e,"groups":B,"rows_n":c,"log_n":a,"vis_h":p,"act_h":x,"ya":F,"h":F+x+M}
	def aQ(title,hint,room):a="%s  (%s)"%(title,hint);return a if m(a)<=room else title
	def bs():
		r=C.slot
		if a["minimized"]:w,h=(max(aC,r[0])if r else aC),bJ
		elif r is None:w,h=aB,b9
		else:w,h=r
		g,s,e=C.begin(w,h);i=l;K=[];k=1.;B["k"],B["full"]=1.,None
		if a["minimized"]:e["mini_w"]=w
		else:
			n,o,y=w,h,None
			if r is None:c=M(n,None);o=c["h"]
			elif w<Y():
				k=w/float(Y());c=M(Y(),int(h/k))
				if c["h"]>int(h/k)+1:k=min(k,h/float(c["h"]))
				n,o=int(round(w/k)),int(round(h/k));c=M(n,o)
			else:
				c=M(n,o)
				if c["h"]>o+1:n=w-Kit.SCROLL_BAND;c=M(n,o);y=c["h"]
			d["P"]=c;j=c["IW"];C.frame(g,n,o);O=c["ys"];P(g,i,O,j,c["sweep_h"],aQ("SWEEP","Detect Hidden on your spot",j-12));e["sweep_lbl"]=F(g,s,"sweep",av,c["sweep_xy"][0],c["sweep_xy"][1],"Sweep: off","Switch the automatic sweep: Detect Hidden on your spot whenever ready",on_click=p("sweep"));F(g,s,"now",aw,c["now_xy"][0],c["now_xy"][1],"Sweep now","Use Detect Hidden once, if ready",on_click=p("now"));e["status"]=u(g,"",i+10,c["status_y"],f);e["count"]=u(g,"",i+j-10,c["status_y"],f);e["count_y"]=c["status_y"];t=c["yv"];Q=m("99 near (%d shown)"%R);P(g,i,t,j,c["vis_h"],aQ("VISITORS","players near you",j-12-Q-16));e["near"]=u(g,"",i+j-10,t+6,f);e["near_y"]=t+6;S,T,U,N=c["x"];e["name_w"],e["hidden_w"]=c["name_w"],m(" (hidden)");z="Say the %s command at them";V=(("fr",au,S,"Friend",z%"friend"+an,"friend"),("ej",aw,T,"Eject",z%"eject"+an,"eject"),("ban",I,U,"Ban",z%"ban"+("; click again within %d s to confirm"%int(ai)if b["confirm"]else "")+an,"ban"));W,X=c["row_h"],c["btn_dy"]
			for A in range(c["rows_n"]):
				v=t+30+A*W;q={"val":None,"prev":None,"changed":0.};q["name_lbl"]=u(g,"",i+12,v+3,aa);q["dist_lbl"]=u(g,"",N,v+3,f);q["catch"]=aZ(g,i+10,v,N-i-10+c["dist_w"],c["rh"],az(q,p,"last"),bo)
				for x,D,E,G,H,Z in V:q[x]=F(g,s,"%s%d"%(x,A),D,E,v+X,G,H,on_click=az(q,p,Z));q[x+"_btn"]=s[0]["%s%d"%(x,A)]
				K.append(q)
			e["empty"]=[u(g,cI,i+12,t+33+20*cH,f)for cH,cI in enumerate(c["empty"][:max(1,(c["vis_h"]-33)//20)])];J=c["ya"];P(g,i,J,j,c["act_h"],aQ("ACTIONS","pick with a cursor",j-12))
			for ab,ac in zip(bq,c["groups"]):
				for(ad,D,G,H,ae),(E,af)in zip(ab,ac):F(g,s,ad,D,E,J+26+26*af,G,H,on_click=p(ae))
			ly=J+30+26*c["act_rows"];e["log"]=[u(g,"",i+12,ly+cJ*L,f)for cJ in range(c["log_n"])];e["log_w"],e["log_full"]=j-70,j-24
			if k!=1.:B["k"],B["full"]=k,(int(Y()),int(round(M(Y(),None)["h"])));Kit.scale_window(g,k)
			elif y is not None:w,h=n,y
			else:w,h=n,o
		C.end(g,{"rows":K},w,h,r[1]if(r is not None and not a["minimized"])else None);cd()
	C=Kit.Window(g,ae,a,d,bs,bG,bH,icon=bK,cleanup=aL,clear={"rows":[]})
	def cd():aS();bu();by()
	bt=("name_lbl","dist_lbl","catch","fr","fr_btn","ej","ej_btn","ban","ban_btn")
	def aR(ctrl,on,row,key):
		if row.get(key+"_vis")!=on:row[key+"_vis"]=on;ctrl.IsVisible=on
	def bu():
		f=d["rows"]
		if not f or a["minimized"]:return
		c=d["c"];e=a["visitors"];r=time.time();h,s=c["name_w"],c["hidden_w"]
		for i,b in enumerate(f):
			if i<len(e):
				v=e[i];ac(b,(v["serial"],v["name"]),r);t=(v["serial"],v["name"],v["noto"],v["hidden"],v["dist"],h,s)
				if b.get("sig")==t:continue
				b["sig"]=t;n=a_(v["noto"],bg.get(v["noto"],aa));u=X(v["name"],v["serial"],v["noto"])
				if v["hidden"]:n=ab;j(b["name_lbl"],V(u,h-s)+" (hidden)",n)
				else:j(b["name_lbl"],V(u,h),n)
				j(b["dist_lbl"],Kit.count(v["dist"],"tile"))
				for k in bt:aR(b[k],True,b,k)
			else:
				ac(b,None,r);b["sig"]=None
				for k in bt:aR(b[k],False,b,k)
		g=d["P"]["empty"];o=c.get("empty_k")
		if o is None or o[0]!=(not e)or o[1]is not g:
			c["empty_k"]=(not e,g)
			for i,y in enumerate(c["empty"]):j(y,g[i]if(not e and i<len(g))else "")
		w=c["near"];x=(a["near"],len(e)>len(f),len(f))
		if c.get("near_k")!=x:
			c["near_k"]=x;p="%d near"%a["near"]if a["near"]else ""
			if len(e)>len(f):p="%d near (%d shown)"%(a["near"],len(f))
			j(w,p);q=m(p)
			if c.get("near_w")!=q:c["near_w"]=q;z=d["P"]["IW"];bp(w,l+z-10-q,c["near_y"])
	def bv(c,width):
		t,a,d,b,e=c
		if b and Kit.streamer:a=a.replace(b,X(b,e))
		return "%s  %s"%(time.strftime("%H:%M",time.localtime(t)),V(a,width)),d
	def aS():
		c=d["c"];a=c.get("log")
		if a:
			b=r[-len(a):]
			for i,e in enumerate(a):
				if i<len(b):g,h=bv(b[len(b)-1-i],c["log_w"]);j(e,g,h)
				else:j(e,ax(be,c["log_full"])if i==0 else "",f)
		aT()
	def bw():return aE,aG+bM*S
	def ce():
		if ad(T):N()
		else:z.close()
	def N():
		M=l;a=d["log_view"]=="visits";b=ad(T);x,y=(q,ag)if a else(r,G);A,B=bw();c=z.slot if b and z.slot is not None and z.slot[0]>=A and z.slot[1]>=B else None;j=z.rows(S,aG,0)if c else min(y,max(10,(len(x)+9)//10*10));w,h=c if c else(aE,aG+j*S);C=h-M-30-n-M;g,e,E=z.begin(w,h);Kit.add_window_frame(g,w,h);P(g,M,M,w-2*M,30);u(g,a6.upper(),M+30,M+7,ab)
		if not b:F(g,e,"close",I,w-M-54,M+4,None,"Close the log",on_click=p("show_log"))
		k=w-M-(10 if b else 66)-35-m("Clear");F(g,e,"clear",I,k,M+4,"Clear","Forget these visits"if a else "Forget these actions",on_click=p("log_clear"));o="Actions"if a else "Visitors";F(g,e,"view",av,k-12-35-m(o),M+4,o,"Show what the butler did"if a else "Show who came into the house",on_click=p("log_view"));s=M+30+n;P(g,M,s,w-2*M,C,"VISITORS  (while you were inside)"if a else "ACTIONS  (newest first, %d kept)"%G);t=[]
		for D in range(j):
			v=s+30+D*S;i={"lbl":u(g,"",M+12,v,f),"catch":None,"val":None,"prev":None,"changed":0.}
			if a:i["catch"]=aZ(g,M+10,v-1,w-2*M-20,S,az(i,p,"last"),bo)
			t.append(i)
		z.end(g,{"rows":t,"w":w});aT()
	z=Kit.Window(T,a6,k,k,N,bI,default=(240,240),cleanup=aL,lock=True,owner=False,clear={"rows":[]})
	def cf(e,width,now):
		k,f,g,l,c,h,i=e;j=time.localtime(k);b=time.strftime("%H:%M"if j[:3]==time.localtime(now)[:3]else "%b %d %H:%M",j)
		if a["open_visits"].get(g)is e:b+=", inside"
		elif f:b+="-"+time.strftime("%H:%M",time.localtime(f))
		else:b+="-?"
		d=" (%s)"%c
		if h>1:d+="  %d times"%h
		if i:d+="  banned"if i==2 else "  ejected"
		m=max(60,width-Kit.text_px(b+"  "+d));return("%s  %s%s"%(b,V(X(l,g,c),m),d),a_(c,bg.get(c,aa)))
	def aT():
		t=k["g"]
		if not ay(t):return
		p=k["rows"];c=d["log_view"]=="visits";g=q if c else r
		if len(g)>len(p)and not ad(T):N();return
		n=len(g);h=time.time()
		for i,b in enumerate(p):
			if i<n:
				e=g[n-1-i]
				if c:
					s=(e[0],e[2],e[1],e[5],e[6],a["open_visits"].get(e[2])is e)
					if b.get("key")!=s:b["key"]=s;m,o=cf(e,k["w"]-2*l-28,h);j(b["lbl"],m,o)
					ac(b,(e[2],e[3]),h)
				else:m,o=bv(e,k["w"]-2*l-70);j(b["lbl"],m,o)
			else:j(b["lbl"],(b5 if c else be)if i==0 else "",f);b["key"]=None;ac(b,None,h)
			if b["catch"]is not None:aR(b["catch"],i<n,b,"catch")
	def cg(now):
		h=a["house"]or a["house_wait"]
		if h is not None:d,e=H(h);return("%s %s: waiting for the %s cursor"%(ak[h["kind"]],X(d,e)if d else(h["name"]or "the target"),"house"if a["house"]is not None else "sweep"),ab)
		if a["note"]and now<a["note_until"]:return a["note"],f
		if a["phase"]=="cursor":return "Detect Hidden: waiting for cursor",ab
		if a["phase"]=="cast":return "Detect Hidden: sweeping",E
		c=aV(now)
		if not a["sweep"]:return("Sweep off; ready in %d s"%int(c+.99)if c>0 else "Sweep off; ready"),f
		if a["held"]==aj:return aj,f
		if a["held"]:return "Sweep on, waiting: %s"%a["held"],f
		if c>0:return "Sweep on: next in %d s"%int(c+.99),E
		if b["still"]and now-a["moved_at"]<bb:return "Sweep on: stand still",f
		return "Sweep on: ready",E
	def ch():
		if a["house"]is not None or a["house_wait"]is not None:s="house command"
		elif a["phase"]!="idle":s="sweeping"
		elif a["sweep"]:s="sweep on, waiting"if a["held"]else "sweep on"
		else:s="sweep off"
		if a["near"]:s+=", %d near"%a["near"]
		return "%s: %s"%(ae,s)
	def bx(c,key,text,room):
		e=c.get(key)
		if e is not None and e[0]==text and e[1]==room:return e[2]
		a=V(text,room);c[key]=(text,room,a);return a
	def by():
		c=d["c"]
		if d["g"]is None or(a["minimized"]and a["docked"]):return
		p=time.time();f,i=cg(p)
		if a["minimized"]:
			b=c.get("status")
			if b is not None:j(b,bx(c,"mini_k",ch(),c.get("mini_w",aC)-90),i)
			return
		P=d.get("P")or{};b=c.get("status")
		if b is not None:
			k=bx(c,"status_k",f,P.get("status_room",aB-2*l-160))
			if j(b,k,i):b.SetTooltip(f if k!=f else "")
		n=c.get("sweep_lbl")
		if n is not None:j(n,"Sweep: on"if a["sweep"]else "Sweep: off",E if a["sweep"]else aa)
		g=c.get("count");o=(a["sweeps"],a["revealed"],P.get("count_room",400))
		if g is not None and c.get("count_k")!=o:
			c["count_k"]=o;e=("%s, %d revealed"%(Kit.count(a["sweeps"],"sweep"),a["revealed"]));e=ax(e,P.get("count_room",400))
			if j(g,e)or c.get("count_w")is None:
				h=m(e)
				if c.get("count_w")!=h:c["count_w"]=h;q=P.get("IW",aB-2*l);bp(g,l+q-10-h,c["count_y"])
	def bz(now,me):
		if 0<=now-a["scan_at"]<(bX if a["scan_poke"]else bW):return False
		a["scan_at"]=now;a["scan_poke"]=False;g,h=int(me.X),int(me.Y);p=me.Serial
		if a["pos"]!=(g,h):a["pos"],a["moved_at"]=(g,h),now
		k=b["range"];q=API.GetAllMobiles(distance=k,isHuman=True)or[];c=a["ncache"]
		if len(c)>af:
			for r in[s for s,v in c.items()if now>=v[0]]:del c[r]
			if len(c)>af:c.clear()
		d=[]
		for m in q:
			try:
				e=m.Serial
				if e==p:continue
				i=c.get(e)
				if i is not None and now<i[0]:j,f=i[1],i[2]
				elif m.IsRenamable:c[e]=(now+aF,None,"pet");continue
				else:f=Kit.noto_name(m);j=str(m.Name or "");c[e]=(now+aF,j,f)
				if j is None or f=="invulnerable"or(f=="ally"and not b["friends"]):continue
				l,n=int(m.X),int(m.Y);o=max(abs(l-g),abs(n-h))
				if o>k:continue
				d.append({"serial":e,"name":j,"noto":f,"dist":o,"hidden":bool(m.IsHidden),"x":l,"y":n,"inside":False})
			except Exception:continue
		d.sort(key=ci);a["near"]=len(d);a["visitors"]=d;cj(now,g,h,d);bu();return True
	def ci(v):return(v["dist"],v["name"].lower())
	def bA(x,y):return len(API.GetMultisAt(x,y)or())>0
	def cj(now,mx,b,out):
		if a["house_pos"]!=(mx,b)or now>=a["house_at"]:a["house_pos"],a["house_at"]=(mx,b),now+bP;a["in_house"]=bA(mx,b)
		c=a["open_visits"]
		if not a["in_house"]:a["inside"]={};bB(now);return
		h=a["inside"];d={};f=bQ
		for v in out:
			s=v["serial"];e=h.get(s)
			if e is None or e[0]!=v["x"]or e[1]!=v["y"]:
				if f>0:f-=1;e=(v["x"],v["y"],bA(v["x"],v["y"]))
				elif e is None:continue
			d[s]=e;g=e[2];v["inside"]=g
			if g:
				if s not in c:ck(v,now)
			elif s in c:aU(s,now)
		a["inside"]=d
		for s in[w for w in c if w not in d]:aU(s,now)
	def ck(v,now):
		s=v["serial"];e=next((c for c in reversed(q)if c[2]==s),None)
		if e is not None and e[1]and now-e[1]<=bN:e[1]=0.;e[5]+=1
		else:e=[now,0.,s,v["name"]or "someone",v["noto"],1,0];q.append(e);del q[:-ag]
		a["open_visits"][s]=e;al()
	def aU(s,now):
		e=a["open_visits"].pop(s,None)
		if e is not None:e[1]=now;al()
	def bB(now):
		for s in list(a["open_visits"]):aU(s,now)
	def cl(serial,flag):
		e=next((c for c in reversed(q)if c[2]==serial),None)
		if e is not None:e[6]=flag;al()
	def cm(serial,name,now):
		b=HOST.services.get(bR)
		if b is None:return False
		c=a["foe"].get(serial)
		if c is not None and now<c[0]:return c[1]
		try:r=bool(b(serial,name))
		except Exception:r=False
		if len(a["foe"])>af:a["foe"].clear()
		a["foe"][serial]=(now+aF,r);return r
	def cn(now):
		if not b["eject_foes"]or not a["in_house"]:return
		c=a["eject_at"];d=None
		for v in a["visitors"]:
			if not v["inside"]or v["hidden"]:continue
			s=v["serial"]
			if c.get(s,0.)>now:continue
			if v["noto"]!="murderer"and not cm(s,v["name"],now):continue
			if d is None:d={int(h)for h in list(API.GetPartyMemberSerials()or[])+list(API.GetAllFriends()or[])}
			if s in d:continue
			if len(c)>af:
				for k in[w for w,x in c.items()if x<=now]:del c[k]
			c[s]=now+a7;e="red"if v["noto"]=="murderer"else "Foe"
			if not ar(bd,"%s (%s) in your house: Eject from their row?"%(v["name"]or "Someone",e),"alarm",who=s,name=v["name"]):t("%s (%s) stepped in"%(v["name"]or "someone",e),D,v["name"],s)
			return
	def bC(now):
		a=HOST.fight_hold(now)
		if a=="dead":return HOLD_TEXT["dead"]
		g=HOST.guard_hold()
		if g=="guard":return HOLD_TEXT["guard"]
		if g is not None:return aj
		if a:return HOLD_TEXT.get(a,a)
		return HOLD_TEXT["alarm"]if HOST.alarm_up()else None
	def aV(now):b=a["next_at"]-now;return b if 0<b<=aH else 0.
	def bD(now,forced=False):
		if a["house"]is not None:
			if forced:i(aP)
			return False
		if a["phase"]!="idle":return False
		c=a["held"]
		if c:
			if forced:i(c if c==aj else "The sweep waits: %s"%c)
			return False
		d=aV(now)
		if d>0:
			if forced:i("Ready in %d s"%int(d+.99))
			return False
		if not forced and b["still"]and now-a["moved_at"]<bb:return False
		if not am():
			if forced:i("A target cursor is up: the sweep waits")
			return False
		e=HOST.me()
		if e is not None:a["scan_at"]=0.;bz(now,e)
		a["seen"]={h["serial"]for h in a["visitors"]if not h["hidden"]};a["first_d"]={};a["reveal_line"]=False;API.UseSkill(bS);aX(g,U);a["phase"],a["deadline"]="cursor",now+U;return True
	def co(now):
		if a["phase"]=="cursor":
			if now>a["deadline"]:A(g);a["phase"],a["next_at"]="idle",now+ah;i("No Detect Hidden cursor; retrying")
			elif at(g)is not None:return
			elif aY(g,"neutral"):API.TargetSelf();A(g);a["phase"],a["cast_at"]="cast",now;a["next_at"]=now+b["cooldown"];a["sweeps"]+=1
			elif aN():A(g);a["phase"],a["next_at"]="idle",now+ah;t("sweep dropped: a spell cursor came up",f)
			return
		if a["phase"]=="cast":
			if now-a["cast_at"]<=bV:
				c=a["first_d"];d=max(1,b["range"]-2)
				for v in a["visitors"]:
					if v["serial"]not in a["seen"]and not v["hidden"]:
						if c.setdefault(v["serial"],v["dist"])>d and not a["reveal_line"]:continue
						a["seen"].add(v["serial"]);a["revealed"]+=1;API.HeadMsg("* revealed *",v["serial"],D);t("revealed %s"%(v["name"]or "someone"),D,v["name"],v["serial"])
						if b["sound"]:ar(aJ,"Revealed %s"%(v["name"]or "someone"),"warn",who=v["serial"],name=v["name"])
			if now-a["cast_at"]>aI:a["phase"]="idle"
	def cp(d):
		f=time.time();e=a["phase"]in("cursor","cast")or f-a["cast_at"]<aI
		if not e and a["house"]is None and a["house_wait"]is None:return
		c=d.low
		if e:
			if any(s in c for s in b_):
				if a["phase"]=="cursor":A(g)
				elif a["phase"]=="cast":a["sweeps"]=max(0,a["sweeps"]-1)
				a["phase"],a["next_at"]="idle",time.time()+ah;i("Skill delay: retrying");return
			if any(v in c for v in b0):return
			if any(w in c for w in b1):
				a["reveal_line"]=True;i("Someone was revealed",6.)
				if b["sound"]:ar(aJ,"Someone was revealed","warn")
				return
		h=a["house"]
		if h is None:return
		if any(x in c for x in b2[h["kind"]]):
			t("%s %s"%(K[h["kind"]][1],h["name"]or "the target"),E,*H(h))
			if h["kind"]in("eject","ban"):cl(h["serial"],2 if h["kind"]=="ban"else 1)
			O();return
		if any(y in c for y in b3):t("%s %s failed: %s"%(W(h)+(d.text.strip(),)),D,*H(h));O();return
	def ao(kind,serial,name,now,waited=False):
		if a["house"]is not None or(a["house_wait"]is not None and not waited):i(aP);return
		if a["phase"]=="cursor":a["house_wait"]={"kind":kind,"serial":serial,"name":name,"until":now+U};a["confirm"]=None;return
		if not b[K[kind][0]]:i("Type the words for %s on the settings page"%ak[kind]);return
		if not am():i(bn);return
		if not name:name=str(safe(lambda:bl(kind,serial).Name,"")or "")
		API.Msg(b[K[kind][0]]);aX(g,U);a["house"]={"kind":kind,"serial":serial,"name":name,"deadline":now+U,"aimed":0.};a["confirm"]=None
	def O():a["house"]=None;A(g)
	def cq(now):
		b=a["house_wait"]
		if b is None:return
		if a["phase"]!="cursor"and am():a["house_wait"]=None;ao(b["kind"],b["serial"],b["name"],now,waited=True)
		elif now>b["until"]:
			a["house_wait"]=None
			if a["phase"]=="cursor":A(g);a["phase"],a["next_at"]="idle",now+ah
			if am():ao(b["kind"],b["serial"],b["name"],now,waited=True)
			else:i(bn)
	def cr(now):
		h=a["house"]
		if h is None:return
		if not h["aimed"]:
			if now<=h["deadline"]:
				if at(g)is not None:return
				if not aY(g,"neutral"):
					if aN():t("%s %s: dropped, a spell cursor came up"%W(h),D,*H(h));O()
					return
				if bl(h["kind"],h["serial"])is None:API.CancelTarget();t("%s %s: out of sight"%W(h),D,*H(h));O();return
				API.Target(h["serial"]);A(g);h["aimed"]=now
			else:t("%s %s: no house cursor (in your house, with the right? Else use the house sign)"%W(h),D,*H(h));O()
			return
		if now-h["aimed"]>aI:t("%s aimed at %s (no reply seen)"%W(h),None,*H(h));O()
	def cs(serial,name,now):
		if b["confirm"]:
			c=a["confirm"]
			if not(c and c[0]==serial and now<c[1]):a["confirm"]=(serial,now+ai,now);i("Ban %s? Click Ban again to confirm"%(X(name,serial)if name else "them"),ai);return
			if len(c)>2 and now-c[2]<.3:return
		ao("ban",serial,name,now)
	def ct(action,now,me):a["sweep"]=not a["sweep"];J(aA,"1"if a["sweep"]else "0");aM("sweep %s."%("on"if a["sweep"]else "off"),E if a["sweep"]else f)
	def cu(action,now,me):
		if me is not None and a["phase"]=="idle":a["held"]=bC(now)
		if me is not None and not bD(now,forced=True)and a["phase"]!="idle":i("A sweep is already running")
	def cv(action,now,me):
		if ay(k["g"]):ce()
		else:N()
	def cw(action,now,me):
		d["log_view"]="log"if d["log_view"]=="visits"else "visits";J(a5,d["log_view"])
		if ay(k["g"]):N()
	def bE(action,now,me):
		if action=="log_clear"and d["log_view"]=="visits":del q[:];a["open_visits"],a["inside"]={},{};al()
		else:del r[:];a["log_dirty"]=True;aS()
	def cx(a):
		def b(serial):
			serial=int(serial or 0)
			if not serial:i("Nothing picked");return
			p.add((a,serial,None),dup=True)
		return b
	def Z(action,now,me):
		b=action[5:]
		if a["house"]is not None or a["house_wait"]is not None:i(aP)
		else:i("Target the %s to %s (Esc cancels)"%("player"if K[b][2]=="mobile"else "item",ak[b].lower()),a3);HOST.pick_target(a3,cx(b))
	def cy(action,now,me):API.SetLastTarget(serial=action[1]);API.HeadMsg("* last target *",action[1],53)
	def ap(action,now,me):ao(action[0],action[1],action[2],now)
	bF={"sweep":ct,"now":cu,"show_log":cv,"log_view":cw,"log_clear":bE,"clear_log":bE,"pick_eject":Z,"pick_ban":Z,"pick_friend":Z,"pick_lock":Z,"pick_release":Z,"follow":lambda action,now,me:Follow.toggle(action[1],ae),"last":cy,"ban":lambda action,now,me:cs(action[1],action[2],now),"eject":ap,"friend":ap,"lock":ap,"release":ap};cz=("Foe: on Ultima Tracker's Foe list; once per player every %d s; Eject on their row ejects them"%int(a7));cA={"ldy":4,"fh":30,"ugap":6}
	def cB(w):a=(w-24)//2;c=max(m(h)for h in("Eject:","Ban:","Friend:"));d=max(m(s)for s in("Lock down:","Release:"));b,e={"lw":c,"tw":a-c-26},{"dx":12+a,"lw":d,"tw":a-d-26};return(("SWEEP  (Detect Hidden on your spot)",(("num","cooldown","Seconds between uses:","Wait after each use, the shard's skill delay",None,a8,aH,{"cast":float}),("check","still","Sweep only when standing still","Waits until you have stood still 1 s"),("check","sound","Alert when a sweep reveals someone","Sound: Settings > Alerts"))),("VISITORS",(("num","range","List players within:","Players this close are listed","tiles",a9,ba),("check","friends","List guild and alliance members too","Unticked, green players are left out"),("check","confirm","Ban needs a second click within %d s"%int(ai),"So the wrong person isn't banned"),("check","eject_foes","Alarm when a red or Foe enters the house",cz))),("HOUSE COMMANDS  (said out loud)",(("text","eject_cmd","Eject:","Ejects a player (owner, co-owner or friend)",b),("text","ban_cmd","Ban:","Bans a player (owner or co-owner)",b),("text","friend_cmd","Friend:","Makes a player a house friend (owner)",b),("gap",-90),("text","lock_cmd","Lock down:","Locks an item down (owner, co-owner or friend)",e),("text","release_cmd","Release:","Releases a locked-down item (owner or co-owner)",e),("gap",30),("note",Kit.wrap("Owner adds friends; owner and co-owners ban and release; friends eject and lock down.",w-28)[0],{"ndy":4,"h":24}))))
	def cC(b,new):
		if new["eject_foes"]!=b["eject_foes"]:a["eject_at"].clear()
		if new["confirm"]!=b["confirm"]and not a["minimized"]:p("redraw")()
	aq=Kit.Page(b,cB,bi,cC,cA,strict=True);bh()
	def cD(*b):
		if not a["shutting"]and a["phase"]!="idle":a["scan_poke"]=True
	def cE():a.update({"shutting":False,"docked":False,"queue":[],"phase":"idle","house":None,"house_wait":None,"confirm":None,"visitors":[],"near":0,"scan_at":0.,"ncache":{},"log_dirty":False,"log_save_at":0.,"pos":None,"moved_at":0.,"note":"","note_until":0.,"in_house":None,"house_pos":None,"house_at":0.,"inside":{},"open_visits":{},"visits_dirty":False,"visits_save_at":0.,"visits_redraw":False,"eject_at":{},"foe":{},"held":None,"held_at":0.,"minimized":C.start_min()});C.slot=None;B.update({"k":1.,"full":None});bh();a["rd"]=Journal.reader();aW(aJ,"Someone revealed",bY);aW(bd,"Red or Foe in your house",bZ);bs();Kit.hook_once(a,"hooked",("ApiMobileCreated",cD));C.dock(fit=True,exact=True,verify=True,drawn_at=cb);k.update({"shutting":False,"queue":[]});z.dock(fit=True,min=bw);aM("on; sweep %s, visitors within %d tiles%s."%("on"if a["sweep"]else "off",b["range"],", red or Foe alarm on"if b["eject_foes"]else ""),E)
	def cF():
		if d["g"]is None:return
		if Kit.closed(d):return
		b=time.time();g=HOST.me()
		while a["queue"]:
			c=a["queue"].pop(0);h=c[0]if isinstance(c,tuple)else c
			if not C.action(c)and h in bF:bF[h](c,b,g)
		if a["log_dirty"]and b>=a["log_save_at"]:a["log_save_at"]=b+bL;bj()
		if a["visits_dirty"]and b>=a["visits_save_at"]:a["visits_save_at"]=b+bO;bk()
		if a["visits_redraw"]:a["visits_redraw"]=False;aT()
		if k["queue"]:
			del k["queue"][:]
			if ad(T)or k["g"]is not None:N()
		if g is None:return
		for i in a["rd"].new():cp(i)
		if bz(b,g):cn(b)
		cr(b)
		if a["house"]is None:
			if a["sweep"]and a["phase"]=="idle"and(aV(b)<=bc or b>=a["held_at"]):
				a["held_at"]=b+bc;e=bC(b)
				if e!=a["held"]:
					j,a["held"]=a["held"],e
					if e and not j:t("sweep waits: %s"%(e[:1].lower()+e[1:]),f)
				if a["house_wait"]is None and not a["held"]:bD(b)
			co(b);cq(b)
		if a["confirm"]and b>=a["confirm"][1]:a["confirm"]=None
		by()
	def cG():
		a["shutting"]=k["shutting"]=True;a["house_wait"]=None;A(g);bi()
		if a["log_dirty"]:bj()
		if a["open_visits"]:bB(time.time())
		if a["visits_dirty"]:bk()
		aL.close()
	return{"start":cE,"tick":cF,"stop":cG,"client_tick":True,"config_height":aq.height,"build_config":aq.build,"poll_config":aq.poll,"config_closed":aq.closed}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("butler","Property Butler","House sweeps, visitors, eject and ban",_module_butler,.1,category="Skills and home")
