def _module_butler():
	aa=HOST.alert;ay=HOST.alert_kind;az=HOST.claim_cursor;ab=HOST.cursor_busy;aA=HOST.cursor_ok;p=HOST.release_cursor;f="butler";N="Property Butler";aB="PropertyButler_settings";bh="PropertyButler_pos";bi="PropertyButler_min";ac="PropertyButler_view";aC="PropertyButler_log";bj="PropertyButler_log_pos";ad=520;ae,bk=300,46;bl=3026;E=8;aD=22;af=3;t=30;ag=520;F=18;bm=1.;ah=2.5;O=200;aE=15.;aF="PropertyButler_visits";aG="PropertyButler_log_view";G="butler.log";aH="Property Butler Log";bn=4;ai=2*Kit.MARGIN+30+Kit.GAP+30+8;P=30;bo=60.;bp=5.;bq=2.;br=6;aI=10.;bs="ultima.is_foe";bt="Detect Hidden";bu=10.;aJ,aj=3.,120.;bv=12;aK,aL=1,18;H=3.;ak=3.;bw=1.;Q=1.5;R=3.;aM=1.;bx=.3;by=.1;aN=.5;bz=497;al="butler.revealed";aO="butler.foe";bA=824;S=HOLD_TEXT["unknown"];bB=("must wait a few moments to use another skill","must wait to perform another action");bC=("you can see nothing hidden there",);bD=("reveal one other person","reveal several people","you carefully check the house");bE={"eject":("has been ejected from this house",),"ban":("has been banned from this house",),"friend":("is now a friend of this house","made a friend of this house"),"lock":("locked down!",),"release":("no longer locked down",)};bF=("you are not around your house","not a co-owner of this house","only the house owner","this person is already banned","is already the house owner","already a house owner","cannot eject a friend","not in your house","already a friend","cannot be a friend of the house","can't be a friend of the house","is already locked down","isn't locked down","is not locked down","cannot lock","cannot be locked down","refuse to lock this down","did not lock this down","may not release this","locked down items would be exceeded","place it on the ground first","when the front door is open");z={"eject":("eject_cmd","ejected","mobile"),"ban":("ban_cmd","banned","mobile"),"friend":("friend_cmd","befriended","mobile"),"lock":("lock_cmd","locked down","item"),"release":("release_cmd","released","item")};T={"eject":"Eject","ban":"Ban","friend":"Befriend","lock":"Lock down","release":"Release"};bG="No players in range.";aP="No actions yet.";bH="No visits yet.";b={"cooldown":bu,"range":bv,"still":False,"sound":True,"friends":True,"confirm":True,"eject_cmd":"Remove thyself","ban_cmd":"I ban thee","friend_cmd":"I wish to make this a friend","lock_cmd":"I wish to lock this down","release_cmd":"I wish to release this","eject_foes":False};am=dict(b);aQ=("still","sound","friends","confirm","eject_cmd","ban_cmd","friend_cmd","lock_cmd","release_cmd",None,"eject_foes");a={"minimized":False,"shutting":False,"docked":False,"queue":[],"sweep":False,"next_at":0.,"deadline":0.,"cast_at":0.,"seen":set(),"sweeps":0,"revealed":0,"eject_at":{},"first_d":{},"reveal_line":False,"hooked":False,"scan_poke":False};d={"g":None,"c":{},"store":({},{}),"rows":[],"log_view":"log"};i={"g":None,"c":{},"store":({},{}),"rows":[],"minimized":False,"shutting":False,"docked":False,"w":ag,"queue":[]};an,k,aR=Kit.basics(a,N);m=[];l=[];aS={"innocent":90,"ally":68,"gray":946,"criminal":946,"murderer":33,"enemy":43,"invulnerable":53}
	def aT():
		p=Kit.get_var(aB).split("|")
		if len(p)>=8:
			for i,k,e,f,g in((0,"cooldown",aJ,aj,float),(1,"range",aK,aL,int)):
				with Kit.quiet:b[k]=max(e,min(f,g(p[i])))
			n=len(p);p=p+[""]*(13-len(p))
			for i,k in enumerate(aQ,2):
				if k:b[k]=p[i]=="1"if isinstance(am[k],bool)else(p[i]if i<n else am[k])
		a["sweep"]=Kit.get_var(ac)=="1";del m[:]
		for c in Kit.get_var(aC).split("\n"):
			q=c.split("\t")
			if len(q)>=3:
				with Kit.quiet:m.append((float(q[0]),q[2],int(q[1]),q[3]if len(q)>4 else "",int(q[4])if len(q)>4 else 0))
		del m[:-t];del l[:]
		for c in Kit.get_var(aF).split("\n"):
			q=c.split("\t",6)
			if len(q)>=7:
				with Kit.quiet:l.append([float(q[0]),float(q[1]),int(q[2]),q[6],q[3]or "unknown",max(1,int(q[4])),int(q[5])])
		del l[:-P];d["log_view"]="visits"if Kit.get_var(aG)=="visits"else "log"
	def aU():Kit.put_var(aB,"|".join(["%.1f"%b["cooldown"],str(b["range"])]+["0"if c is None else("1"if b[c]else "0")if isinstance(am[c],bool)else b[c].replace("|","/")for c in aQ]));Kit.put_var(ac,"1"if a["sweep"]else "0")
	def aV():a["log_dirty"]=False;Kit.put_var(aC,"\n".join(["%d\t%d\t%s\t%s\t%d"%(c[0],c[2],c[1].replace("\t"," ").replace("\n"," "),c[3].replace("\t"," ").replace("\n"," "),c[4])for c in m[-t:]]))
	def aW():a["visits_dirty"]=False;Kit.put_var(aF,"\n".join(["%d\t%d\t%d\t%s\t%d\t%d\t%s"%(c[0],c[1],c[2],str(c[4]).replace("\t"," "),c[5],c[6],str(c[3]).replace("\t"," ").replace("\n"," "))for c in l[-P:]]))
	def U():
		a["visits_dirty"]=True
		if d["log_view"]=="visits"and i["g"]is not None:a["visits_redraw"]=True
	def n(text,hue=None,name="",serial=0):hue=Kit.HUE_INFO if hue is None else hue;m.append((time.time(),text,hue,name or "",serial));del m[:-t];a["log_dirty"]=True;aR(text+(""if text.endswith((".","!","?"))else "."),hue);au()
	def g(text,secs=4.):a["note"],a["note_until"]=text,time.time()+secs
	def ao():return bool(API.HasTarget("any"))
	def V():return ab(f)is None and not ao()
	def I(name,width):return Kit.fit(name or "(unknown)",width)
	def aX(kind,serial):return(API.FindMobile if z[kind][2]=="mobile"else API.FindItem)(serial)
	def J(h):return T[h["kind"]].lower(),h["name"]or "the target"
	def u(h):return(h["name"],h["serial"])if h["name"]and z[h["kind"]][2]=="mobile"else("",0)
	def K(name,serial,noto=None):a=Kit.noto_mark(noto)if noto else "";return(a+" "if a else "")+Kit.veil("name",name,serial)
	ap=82;bI=150;A=20;bJ=30+E*aD+8;bK=30+26+26+af*A+8;bL=Kit.MARGIN+30+Kit.GAP+ap+Kit.GAP+bJ+Kit.GAP+bK+Kit.MARGIN;bM=2;aY=60;aq="A house command is still running";aZ="A target cursor is up: use it or press Esc";W=". Alt+click: auto-follow (again to stop)";a_="Set as last target"+W;q={"k":1.,"full":None}
	def bN():return q["k"],q["full"]
	def a0(ctrl,x,y):
		k=q["k"]
		if k!=1.:ctrl.SetPos(int(round(x*k)),int(round(y*k)))
		else:Kit.ui_pos(ctrl,x,y)
	def j(text):return 35+Kit.text_w(text)
	a1=((("pick_ej",Kit.ART_PLAY,"Eject...","Pick a player to eject","pick_eject"),("pick_ban",Kit.ART_CLOSE,"Ban...","Pick a player to ban","pick_ban"),("pick_fr",Kit.ART_OK,"Friend...","Pick a player to befriend","pick_friend")),(("pick_lock",Kit.ART_OK,"Lock down...","Pick a house item to lock down","pick_lock"),("pick_rel",Kit.ART_CLOSE,"Release...","Pick a locked-down item to release","pick_release"),("clear",Kit.ART_CLOSE,"Clear log","Forget the actions below (visits stay)","clear_log"),("showlog",Kit.ART_PAGE,"Show log","Open or close the log window (last %d actions and visits)"%t,"show_log")))
	def bO(items,a,right):
		c,x,b=[],a,0
		for d in items:
			w=j(d)
			if x>a and x+w>right:x,b=a,b+1
			c.append((x,b));x+=w+16
		return c
	def a2():return j("Friend")+12+j("Eject")+12+j("Ban")
	def L():return 2*Kit.MARGIN+12+max(a2(),aY+6+Kit.text_w("18 tiles"))+10
	def B(w,h):
		M=Kit.MARGIN;b=w-2*M;d=M+30+Kit.GAP;v=max(j("Sweep: off"),j("Sweep: on"));n=10+v+16+j("Sweep now")<=b-4;o=ap if n else ap+26;x=min(Kit.text_w("999 sweeps, 999 revealed"),max(40,b-20-80));y=d+o+Kit.GAP;g=Kit.text_w("18 tiles");p=12+aY+6+g+10+a2()+10<=b;i=Kit.pitch(aD);f=i if p else 2*i
		if p:q=M+b-10-j("Ban");k=q-12-j("Eject");l=k-12-j("Friend");r=l-10-g
		else:l=M+12;k=l+j("Friend")+12;q=k+j("Eject")+12;r=M+b-10-g
		z,e=[],0
		for G in a1:B=bO([ci[2]for ci in G],M+10,M+b-4);z.append([(cj,e+ck)for cj,ck in B]);e+=B[-1][1]+1
		C=(M+30+Kit.GAP+o+Kit.GAP+30+8+Kit.GAP+30+26*e+8+M)
		if h is None:c,a=E,af
		else:
			s=h-C;a,c=af,E
			while a>1 and c*f+a*A>s:a-=1
			while c>bM and c*f+a*A>s:c-=1
			while c==E and a<t and c*f+(a+1)*A<=s:a+=1
		m=30+c*f+8;u=30+26*e+a*A+8;D=C-(30+8)-(30+26*e+8)+m+u
		if h is not None and h>D:m+=h-D
		F=y+m+Kit.GAP;return{"IW":b,"ys":d,"sweep_xy":(M+10,d+26),"sweep_h":o,"yv":y,"row_h":f,"now_xy":(M+10+v+16,d+26)if n else(M+10,d+52),"status_y":d+58 if n else d+84,"count_room":x,"status_room":max(40,b-20-x-10),"btn_dy":0 if p else i,"rh":i,"x":(l,k,q,r),"dist_w":g,"name_w":max(20,min(bI,r-6-(M+12))),"empty":Kit.wrap(bG,max(60,b-24)),"act_rows":e,"groups":z,"rows_n":c,"log_n":a,"vis_h":m,"act_h":u,"ya":F,"h":F+u+M}
	def ar(title,hint,room):a="%s  (%s)"%(title,hint);return a if Kit.text_w(a)<=room else title
	def a3():
		m=r.slot
		if a["minimized"]:w,h=(max(ae,m[0])if m else ae),bk
		elif m is None:w,h=ad,bL
		else:w,h=m
		g,n,c=r.begin(w,h);M=Kit.MARGIN;F=[];e=1.;q["k"],q["full"]=1.,None
		if a["minimized"]:c["mini_w"]=w
		else:
			i,j,t=w,h,None
			if m is None:P=B(i,None);j=P["h"]
			elif w<L():
				e=w/float(L());P=B(L(),int(h/e))
				if P["h"]>int(h/e)+1:e=min(e,h/float(P["h"]))
				i,j=int(round(w/e)),int(round(h/e));P=B(i,j)
			else:
				P=B(i,j)
				if P["h"]>j+1:i=w-Kit.SCROLL_BAND;P=B(i,j);t=P["h"]
			d["P"]=P;f=P["IW"];r.frame(g,i,j);H=P["ys"];Kit.add_section(g,M,H,f,P["sweep_h"],ar("SWEEP","Detect Hidden on your spot",f-12));c["sweep_lbl"]=Kit.art_button(g,n,"sweep",Kit.ART_PAGE,P["sweep_xy"][0],P["sweep_xy"][1],"Sweep: off","Switch the automatic sweep: Detect Hidden on your spot whenever ready",on_click=k("sweep"));Kit.art_button(g,n,"now",Kit.ART_PLAY,P["now_xy"][0],P["now_xy"][1],"Sweep now","Use Detect Hidden once, if ready",on_click=k("now"));c["status"]=Kit.add_label(g,"",M+10,P["status_y"],Kit.HUE_INFO);c["count"]=Kit.add_label(g,"",M+f-10,P["status_y"],Kit.HUE_INFO);c["count_y"]=P["status_y"];o=P["yv"];I=Kit.text_w("99 near (%d shown)"%E);Kit.add_section(g,M,o,f,P["vis_h"],ar("VISITORS","players near you",f-12-I-16));c["near"]=Kit.add_label(g,"",M+f-10,o+6,Kit.HUE_INFO);c["near_y"]=o+6;J,K,N,G=P["x"];c["name_w"],c["hidden_w"]=P["name_w"],Kit.text_w(" (hidden)");u="Say the %s command at them";O=(("fr",Kit.ART_OK,J,"Friend",u%"friend"+W,"friend"),("ej",Kit.ART_PLAY,K,"Eject",u%"eject"+W,"eject"),("ban",Kit.ART_CLOSE,N,"Ban",u%"ban"+("; click again within %d s to confirm"%int(R)if b["confirm"]else "")+W,"ban"));Q,S=P["row_h"],P["btn_dy"]
			for v in range(P["rows_n"]):
				p=o+30+v*Q;l={"val":None,"prev":None,"changed":0.};l["name_lbl"]=Kit.add_label(g,"",M+12,p+3,Kit.HUE_TEXT);l["dist_lbl"]=Kit.add_label(g,"",G,p+3,Kit.HUE_INFO);l["catch"]=Kit.catcher(g,M+10,p,G-M-10+P["dist_w"],P["rh"],Kit.row_clicker(l,k,"last"),a_)
				for s,x,y,z,C,T in O:l[s]=Kit.art_button(g,n,"%s%d"%(s,v),x,y,p+S,z,C,on_click=Kit.row_clicker(l,k,T));l[s+"_btn"]=n[0]["%s%d"%(s,v)]
				F.append(l)
			c["empty"]=[Kit.add_label(g,cj,M+12,o+33+20*ci,Kit.HUE_INFO)for ci,cj in enumerate(P["empty"][:max(1,(P["vis_h"]-33)//20)])];D=P["ya"];Kit.add_section(g,M,D,f,P["act_h"],ar("ACTIONS","pick with a cursor",f-12))
			for U,V in zip(a1,P["groups"]):
				for(X,x,z,C,Y),(y,Z)in zip(U,V):Kit.art_button(g,n,X,x,y,D+26+26*Z,z,C,on_click=k(Y))
			ly=D+30+26*P["act_rows"];c["log"]=[Kit.add_label(g,"",M+12,ly+ck*A,Kit.HUE_INFO)for ck in range(P["log_n"])];c["log_w"],c["log_full"]=f-70,f-24
			if e!=1.:q["k"],q["full"]=e,(int(L()),int(round(B(L(),None)["h"])));Kit.scale_window(g,e)
			elif t is not None:w,h=i,t
			else:w,h=i,j
		r.end(g,{"rows":F},w,h,m[1]if(m is not None and not a["minimized"])else None);bP()
	r=Kit.Window(f,N,a,d,a3,bh,bi,icon=bl,cleanup=an,clear={"rows":[]})
	def bP():au();a5();a9()
	a4=("name_lbl","dist_lbl","catch","fr","fr_btn","ej","ej_btn","ban","ban_btn")
	def at(ctrl,on,row,key):
		if row.get(key+"_vis")!=on:row[key+"_vis"]=on;ctrl.IsVisible=on
	def a5():
		f=d["rows"]
		if not f or a["minimized"]:return
		c=d["c"];e=a["visitors"];o=time.time();h,p=c["name_w"],c["hidden_w"]
		for i,b in enumerate(f):
			if i<len(e):
				v=e[i];Kit.row_set(b,(v["serial"],v["name"]),o);q=(v["serial"],v["name"],v["noto"],v["hidden"],v["dist"],h,p)
				if b.get("sig")==q:continue
				b["sig"]=q;j=Kit.cb_hue(v["noto"],aS.get(v["noto"],Kit.HUE_TEXT));r=K(v["name"],v["serial"],v["noto"])
				if v["hidden"]:j=Kit.HUE_TITLE;Kit.set_text(b["name_lbl"],I(r,h-p)+" (hidden)",j)
				else:Kit.set_text(b["name_lbl"],I(r,h),j)
				Kit.set_text(b["dist_lbl"],Kit.count(v["dist"],"tile"))
				for k in a4:at(b[k],True,b,k)
			else:
				Kit.row_set(b,None,o);b["sig"]=None
				for k in a4:at(b[k],False,b,k)
		g=d["P"]["empty"];l=c.get("empty_k")
		if l is None or l[0]!=(not e)or l[1]is not g:
			c["empty_k"]=(not e,g)
			for i,u in enumerate(c["empty"]):Kit.set_text(u,g[i]if(not e and i<len(g))else "")
		s=c["near"];t=(a["near"],len(e)>len(f),len(f))
		if c.get("near_k")!=t:
			c["near_k"]=t;m="%d near"%a["near"]if a["near"]else ""
			if len(e)>len(f):m="%d near (%d shown)"%(a["near"],len(f))
			Kit.set_text(s,m);n=Kit.text_w(m)
			if c.get("near_w")!=n:c["near_w"]=n;w=d["P"]["IW"];a0(s,Kit.MARGIN+w-10-n,c["near_y"])
	def a6(c,width):
		t,a,d,b,e=c
		if b and Kit.streamer:a=a.replace(b,K(b,e))
		return "%s  %s"%(time.strftime("%H:%M",time.localtime(t)),I(a,width)),d
	def au():
		c=d["c"];a=c.get("log")
		if a:
			b=m[-len(a):]
			for i,e in enumerate(a):
				if i<len(b):f,g=a6(b[len(b)-1-i],c["log_w"]);Kit.set_text(e,f,g)
				else:Kit.set_text(e,Kit.fit(aP,c["log_full"])if i==0 else "",Kit.HUE_INFO)
		av()
	def a7():return ag,ai+bn*F
	def bQ():
		if Kit.zone_up(G):C()
		else:o.close()
	def C():
		M=Kit.MARGIN;a=d["log_view"]=="visits";b=Kit.zone_up(G);r,s=(l,P)if a else(m,t);u,v=a7();z=o.slot if b and o.slot is not None and o.slot[0]>=u and o.slot[1]>=v else None;n=o.rows(F,ai,0)if z else min(s,max(10,(len(r)+9)//10*10));w,h=z if z else(ag,ai+n*F);x=h-M-30-Kit.GAP-M;g,c,A=o.begin(w,h);Kit.add_window_frame(g,w,h);Kit.add_section(g,M,M,w-2*M,30);Kit.add_label(g,aH.upper(),M+30,M+7,Kit.HUE_TITLE)
		if not b:Kit.art_button(g,c,"close",Kit.ART_CLOSE,w-M-54,M+4,None,"Close the log",on_click=k("show_log"))
		f=w-M-(10 if b else 66)-35-Kit.text_w("Clear");Kit.art_button(g,c,"clear",Kit.ART_CLOSE,f,M+4,"Clear","Forget these visits"if a else "Forget these actions",on_click=k("log_clear"));i="Actions"if a else "Visitors";Kit.art_button(g,c,"view",Kit.ART_PAGE,f-12-35-Kit.text_w(i),M+4,i,"Show what the butler did"if a else "Show who came into the house",on_click=k("log_view"));j=M+30+Kit.GAP;Kit.add_section(g,M,j,w-2*M,x,"VISITORS  (while you were inside)"if a else "ACTIONS  (newest first, %d kept)"%t);p=[]
		for y in range(n):
			q=j+30+y*F;e={"lbl":Kit.add_label(g,"",M+12,q,Kit.HUE_INFO),"catch":None,"val":None,"prev":None,"changed":0.}
			if a:e["catch"]=Kit.catcher(g,M+10,q-1,w-2*M-20,F,Kit.row_clicker(e,k,"last"),a_)
			p.append(e)
		o.end(g,{"rows":p,"w":w});av()
	o=Kit.Window(G,aH,i,i,C,bj,default=(240,240),cleanup=an,lock=True,owner=False,clear={"rows":[]})
	def bR(e,width,now):
		k,f,g,l,c,h,i=e;j=time.localtime(k);b=time.strftime("%H:%M"if j[:3]==time.localtime(now)[:3]else "%b %d %H:%M",j)
		if a["open_visits"].get(g)is e:b+=", inside"
		elif f:b+="-"+time.strftime("%H:%M",time.localtime(f))
		else:b+="-?"
		d=" (%s)"%c
		if h>1:d+="  %d times"%h
		if i:d+="  banned"if i==2 else "  ejected"
		m=max(60,width-Kit.text_px(b+"  "+d));return("%s  %s%s"%(b,I(K(l,g,c),m),d),Kit.cb_hue(c,aS.get(c,Kit.HUE_TEXT)))
	def av():
		q=i["g"]
		if not Kit.is_open(q):return
		o=i["rows"];f=d["log_view"]=="visits";g=l if f else m
		if len(g)>len(o)and not Kit.zone_up(G):C();return
		n=len(g);h=time.time()
		for c,b in enumerate(o):
			if c<n:
				e=g[n-1-c]
				if f:
					p=(e[0],e[2],e[1],e[5],e[6],a["open_visits"].get(e[2])is e)
					if b.get("key")!=p:b["key"]=p;j,k=bR(e,i["w"]-2*Kit.MARGIN-28,h);Kit.set_text(b["lbl"],j,k)
					Kit.row_set(b,(e[2],e[3]),h)
				else:j,k=a6(e,i["w"]-2*Kit.MARGIN-70);Kit.set_text(b["lbl"],j,k)
			else:Kit.set_text(b["lbl"],(bH if f else aP)if c==0 else "",Kit.HUE_INFO);b["key"]=None;Kit.row_set(b,None,h)
			if b["catch"]is not None:at(b["catch"],c<n,b,"catch")
	def bS(now):
		h=a["house"]or a["house_wait"]
		if h is not None:d,e=u(h);return("%s %s: waiting for the %s cursor"%(T[h["kind"]],K(d,e)if d else(h["name"]or "the target"),"house"if a["house"]is not None else "sweep"),Kit.HUE_TITLE)
		if a["note"]and now<a["note_until"]:return a["note"],Kit.HUE_INFO
		if a["phase"]=="cursor":return "Detect Hidden: waiting for cursor",Kit.HUE_TITLE
		if a["phase"]=="cast":return "Detect Hidden: sweeping",Kit.HUE_GOOD
		c=ax(now)
		if not a["sweep"]:return("Sweep off; ready in %d s"%int(c+.99)if c>0 else "Sweep off; ready"),Kit.HUE_INFO
		if a["held"]==S:return S,Kit.HUE_INFO
		if a["held"]:return "Sweep on, waiting: %s"%a["held"],Kit.HUE_INFO
		if c>0:return "Sweep on: next in %d s"%int(c+.99),Kit.HUE_GOOD
		if b["still"]and now-a["moved_at"]<aM:return "Sweep on: stand still",Kit.HUE_INFO
		return "Sweep on: ready",Kit.HUE_GOOD
	def bT():
		if a["house"]is not None or a["house_wait"]is not None:s="house command"
		elif a["phase"]!="idle":s="sweeping"
		elif a["sweep"]:s="sweep on, waiting"if a["held"]else "sweep on"
		else:s="sweep off"
		if a["near"]:s+=", %d near"%a["near"]
		return "%s: %s"%(N,s)
	def a8(c,key,text,room):
		e=c.get(key)
		if e is not None and e[0]==text and e[1]==room:return e[2]
		a=I(text,room);c[key]=(text,room,a);return a
	def a9():
		c=d["c"]
		if d["g"]is None or(a["minimized"]and a["docked"]):return
		m=time.time();f,i=bS(m)
		if a["minimized"]:
			b=c.get("status")
			if b is not None:Kit.set_text(b,a8(c,"mini_k",bT(),c.get("mini_w",ae)-90),i)
			return
		P=d.get("P")or{};b=c.get("status")
		if b is not None:
			j=a8(c,"status_k",f,P.get("status_room",ad-2*Kit.MARGIN-160))
			if Kit.set_text(b,j,i):b.SetTooltip(f if j!=f else "")
		k=c.get("sweep_lbl")
		if k is not None:Kit.set_text(k,"Sweep: on"if a["sweep"]else "Sweep: off",Kit.HUE_GOOD if a["sweep"]else Kit.HUE_TEXT)
		g=c.get("count");l=(a["sweeps"],a["revealed"],P.get("count_room",400))
		if g is not None and c.get("count_k")!=l:
			c["count_k"]=l;e=("%s, %d revealed"%(Kit.count(a["sweeps"],"sweep"),a["revealed"]));e=Kit.fit(e,P.get("count_room",400))
			if Kit.set_text(g,e)or c.get("count_w")is None:
				h=Kit.text_w(e)
				if c.get("count_w")!=h:c["count_w"]=h;n=P.get("IW",ad-2*Kit.MARGIN);a0(g,Kit.MARGIN+n-10-h,c["count_y"])
	def ba(now,me):
		if 0<=now-a["scan_at"]<(by if a["scan_poke"]else bx):return False
		a["scan_at"]=now;a["scan_poke"]=False;g,h=int(me.X),int(me.Y);p=me.Serial
		if a["pos"]!=(g,h):a["pos"],a["moved_at"]=(g,h),now
		k=b["range"];q=API.GetAllMobiles(distance=k,isHuman=True)or[];c=a["ncache"]
		if len(c)>O:
			for r in[s for s,v in c.items()if now>=v[0]]:del c[r]
			if len(c)>O:c.clear()
		d=[]
		for m in q:
			try:
				e=m.Serial
				if e==p:continue
				i=c.get(e)
				if i is not None and now<i[0]:j,f=i[1],i[2]
				elif m.IsRenamable:c[e]=(now+ah,None,"pet");continue
				else:f=Kit.noto_name(m);j=str(m.Name or "");c[e]=(now+ah,j,f)
				if j is None or f=="invulnerable"or(f=="ally"and not b["friends"]):continue
				l,n=int(m.X),int(m.Y);o=max(abs(l-g),abs(n-h))
				if o>k:continue
				d.append({"serial":e,"name":j,"noto":f,"dist":o,"hidden":bool(m.IsHidden),"x":l,"y":n,"inside":False})
			except Exception:continue
		d.sort(key=bU);a["near"]=len(d);a["visitors"]=d;bV(now,g,h,d);a5();return True
	def bU(v):return(v["dist"],v["name"].lower())
	def bb(x,y):return len(API.GetMultisAt(x,y)or())>0
	def bV(now,mx,b,out):
		if a["house_pos"]!=(mx,b)or now>=a["house_at"]:a["house_pos"],a["house_at"]=(mx,b),now+bq;a["in_house"]=bb(mx,b)
		c=a["open_visits"]
		if not a["in_house"]:a["inside"]={};bc(now);return
		h=a["inside"];d={};f=br
		for v in out:
			s=v["serial"];e=h.get(s)
			if e is None or e[0]!=v["x"]or e[1]!=v["y"]:
				if f>0:f-=1;e=(v["x"],v["y"],bb(v["x"],v["y"]))
				elif e is None:continue
			d[s]=e;g=e[2];v["inside"]=g
			if g:
				if s not in c:bW(v,now)
			elif s in c:aw(s,now)
		a["inside"]=d
		for s in[w for w in c if w not in d]:aw(s,now)
	def bW(v,now):
		s=v["serial"];e=next((c for c in reversed(l)if c[2]==s),None)
		if e is not None and e[1]and now-e[1]<=bo:e[1]=0.;e[5]+=1
		else:e=[now,0.,s,v["name"]or "someone",v["noto"],1,0];l.append(e);del l[:-P]
		a["open_visits"][s]=e;U()
	def aw(s,now):
		e=a["open_visits"].pop(s,None)
		if e is not None:e[1]=now;U()
	def bc(now):
		for s in list(a["open_visits"]):aw(s,now)
	def bX(serial,flag):
		e=next((c for c in reversed(l)if c[2]==serial),None)
		if e is not None:e[6]=flag;U()
	def bY(serial,name,now):
		b=HOST.services.get(bs)
		if b is None:return False
		c=a["foe"].get(serial)
		if c is not None and now<c[0]:return c[1]
		try:r=bool(b(serial,name))
		except Exception:r=False
		if len(a["foe"])>O:a["foe"].clear()
		a["foe"][serial]=(now+ah,r);return r
	def bZ(now):
		if not b["eject_foes"]or not a["in_house"]:return
		c=a["eject_at"];d=None
		for v in a["visitors"]:
			if not v["inside"]or v["hidden"]:continue
			s=v["serial"]
			if c.get(s,0.)>now:continue
			if v["noto"]!="murderer"and not bY(s,v["name"],now):continue
			if d is None:d={int(h)for h in list(API.GetPartyMemberSerials()or[])+list(API.GetAllFriends()or[])}
			if s in d:continue
			if len(c)>O:
				for k in[w for w,x in c.items()if x<=now]:del c[k]
			c[s]=now+aI;e="red"if v["noto"]=="murderer"else "Foe"
			if not aa(aO,"%s (%s) in your house: Eject from their row?"%(v["name"]or "Someone",e),"alarm",who=s,name=v["name"]):n("%s (%s) stepped in"%(v["name"]or "someone",e),Kit.HUE_BAD,v["name"],s)
			return
	def bd(now):
		a=HOST.fight_hold(now)
		if a=="dead":return HOLD_TEXT["dead"]
		g=HOST.guard_hold()
		if g=="guard":return HOLD_TEXT["guard"]
		if g is not None:return S
		if a:return HOLD_TEXT.get(a,a)
		return HOLD_TEXT["alarm"]if HOST.alarm_up()else None
	def ax(now):b=a["next_at"]-now;return b if 0<b<=aj else 0.
	def be(now,forced=False):
		if a["house"]is not None:
			if forced:g(aq)
			return False
		if a["phase"]!="idle":return False
		c=a["held"]
		if c:
			if forced:g(c if c==S else "The sweep waits: %s"%c)
			return False
		d=ax(now)
		if d>0:
			if forced:g("Ready in %d s"%int(d+.99))
			return False
		if not forced and b["still"]and now-a["moved_at"]<aM:return False
		if not V():
			if forced:g("A target cursor is up: the sweep waits")
			return False
		e=HOST.me()
		if e is not None:a["scan_at"]=0.;ba(now,e)
		a["seen"]={h["serial"]for h in a["visitors"]if not h["hidden"]};a["first_d"]={};a["reveal_line"]=False;API.UseSkill(bt);az(f,H);a["phase"],a["deadline"]="cursor",now+H;return True
	def b_(now):
		if a["phase"]=="cursor":
			if now>a["deadline"]:p(f);a["phase"],a["next_at"]="idle",now+Q;g("No Detect Hidden cursor; retrying")
			elif ab(f)is not None:return
			elif aA(f,"neutral"):API.TargetSelf();p(f);a["phase"],a["cast_at"]="cast",now;a["next_at"]=now+b["cooldown"];a["sweeps"]+=1
			elif ao():p(f);a["phase"],a["next_at"]="idle",now+Q;n("sweep dropped: a spell cursor came up",Kit.HUE_INFO)
			return
		if a["phase"]=="cast":
			if now-a["cast_at"]<=bw:
				c=a["first_d"];d=max(1,b["range"]-2)
				for v in a["visitors"]:
					if v["serial"]not in a["seen"]and not v["hidden"]:
						if c.setdefault(v["serial"],v["dist"])>d and not a["reveal_line"]:continue
						a["seen"].add(v["serial"]);a["revealed"]+=1;API.HeadMsg("* revealed *",v["serial"],Kit.HUE_BAD);n("revealed %s"%(v["name"]or "someone"),Kit.HUE_BAD,v["name"],v["serial"])
						if b["sound"]:aa(al,"Revealed %s"%(v["name"]or "someone"),"warn",who=v["serial"],name=v["name"])
			if now-a["cast_at"]>ak:a["phase"]="idle"
	def b0(d):
		i=time.time();e=a["phase"]in("cursor","cast")or i-a["cast_at"]<ak
		if not e and a["house"]is None and a["house_wait"]is None:return
		c=d.low
		if e:
			if any(s in c for s in bB):
				if a["phase"]=="cursor":p(f)
				elif a["phase"]=="cast":a["sweeps"]=max(0,a["sweeps"]-1)
				a["phase"],a["next_at"]="idle",time.time()+Q;g("Skill delay: retrying");return
			if any(v in c for v in bC):return
			if any(w in c for w in bD):
				a["reveal_line"]=True;g("Someone was revealed",6.)
				if b["sound"]:aa(al,"Someone was revealed","warn")
				return
		h=a["house"]
		if h is None:return
		if any(x in c for x in bE[h["kind"]]):
			n("%s %s"%(z[h["kind"]][1],h["name"]or "the target"),Kit.HUE_GOOD,*u(h))
			if h["kind"]in("eject","ban"):bX(h["serial"],2 if h["kind"]=="ban"else 1)
			D();return
		if any(y in c for y in bF):n("%s %s failed: %s"%(J(h)+(d.text.strip(),)),Kit.HUE_BAD,*u(h));D();return
	def X(kind,serial,name,now,waited=False):
		if a["house"]is not None or(a["house_wait"]is not None and not waited):g(aq);return
		if a["phase"]=="cursor":a["house_wait"]={"kind":kind,"serial":serial,"name":name,"until":now+H};a["confirm"]=None;return
		if not b[z[kind][0]]:g("Type the words for %s on the settings page"%T[kind]);return
		if not V():g(aZ);return
		if not name:name=str(safe(lambda:aX(kind,serial).Name,"")or "")
		API.Msg(b[z[kind][0]]);az(f,H);a["house"]={"kind":kind,"serial":serial,"name":name,"deadline":now+H,"aimed":0.};a["confirm"]=None
	def D():a["house"]=None;p(f)
	def b1(now):
		b=a["house_wait"]
		if b is None:return
		if a["phase"]!="cursor"and V():a["house_wait"]=None;X(b["kind"],b["serial"],b["name"],now,waited=True)
		elif now>b["until"]:
			a["house_wait"]=None
			if a["phase"]=="cursor":p(f);a["phase"],a["next_at"]="idle",now+Q
			if V():X(b["kind"],b["serial"],b["name"],now,waited=True)
			else:g(aZ)
	def b2(now):
		h=a["house"]
		if h is None:return
		if not h["aimed"]:
			if now<=h["deadline"]:
				if ab(f)is not None:return
				if not aA(f,"neutral"):
					if ao():n("%s %s: dropped, a spell cursor came up"%J(h),Kit.HUE_BAD,*u(h));D()
					return
				if aX(h["kind"],h["serial"])is None:API.CancelTarget();n("%s %s: out of sight"%J(h),Kit.HUE_BAD,*u(h));D();return
				API.Target(h["serial"]);p(f);h["aimed"]=now
			else:n("%s %s: no house cursor (in your house, with the right? Else use the house sign)"%J(h),Kit.HUE_BAD,*u(h));D()
			return
		if now-h["aimed"]>ak:n("%s aimed at %s (no reply seen)"%J(h),None,*u(h));D()
	def b3(serial,name,now):
		if b["confirm"]:
			c=a["confirm"]
			if not(c and c[0]==serial and now<c[1]):a["confirm"]=(serial,now+R,now);g("Ban %s? Click Ban again to confirm"%(K(name,serial)if name else "them"),R);return
			if len(c)>2 and now-c[2]<.3:return
		X("ban",serial,name,now)
	def b4(action,now,me):a["sweep"]=not a["sweep"];Kit.put_var(ac,"1"if a["sweep"]else "0");aR("sweep %s."%("on"if a["sweep"]else "off"),Kit.HUE_GOOD if a["sweep"]else Kit.HUE_INFO)
	def b5(action,now,me):
		if me is not None and a["phase"]=="idle":a["held"]=bd(now)
		if me is not None and not be(now,forced=True)and a["phase"]!="idle":g("A sweep is already running")
	def b6(action,now,me):
		if Kit.is_open(i["g"]):bQ()
		else:C()
	def b7(action,now,me):
		d["log_view"]="log"if d["log_view"]=="visits"else "visits";Kit.put_var(aG,d["log_view"])
		if Kit.is_open(i["g"]):C()
	def bf(action,now,me):
		if action=="log_clear"and d["log_view"]=="visits":del l[:];a["open_visits"],a["inside"]={},{};U()
		else:del m[:];a["log_dirty"]=True;au()
	def b8(a):
		def b(serial):
			serial=int(serial or 0)
			if not serial:g("Nothing picked");return
			k.add((a,serial,None),dup=True)
		return b
	def M(action,now,me):
		b=action[5:]
		if a["house"]is not None or a["house_wait"]is not None:g(aq)
		else:g("Target the %s to %s (Esc cancels)"%("player"if z[b][2]=="mobile"else "item",T[b].lower()),aE);HOST.pick_target(aE,b8(b))
	def b9(action,now,me):API.SetLastTarget(serial=action[1]);API.HeadMsg("* last target *",action[1],53)
	def Y(action,now,me):X(action[0],action[1],action[2],now)
	bg={"sweep":b4,"now":b5,"show_log":b6,"log_view":b7,"log_clear":bf,"clear_log":bf,"pick_eject":M,"pick_ban":M,"pick_friend":M,"pick_lock":M,"pick_release":M,"follow":lambda action,now,me:Follow.toggle(action[1],N),"last":b9,"ban":lambda action,now,me:b3(action[1],action[2],now),"eject":Y,"friend":Y,"lock":Y,"release":Y};ca=("Foe: on Ultima Tracker's Foe list; once per player every %d s; Eject on their row ejects them"%int(aI));cb={"ldy":4,"fh":30,"ugap":6}
	def cc(w):a=(w-24)//2;c=max(Kit.text_w(h)for h in("Eject:","Ban:","Friend:"));d=max(Kit.text_w(s)for s in("Lock down:","Release:"));b,e={"lw":c,"tw":a-c-26},{"dx":12+a,"lw":d,"tw":a-d-26};return(("SWEEP  (Detect Hidden on your spot)",(("num","cooldown","Seconds between uses:","Wait after each use, the shard's skill delay",None,aJ,aj,{"cast":float}),("check","still","Sweep only when standing still","Waits until you have stood still 1 s"),("check","sound","Alert when a sweep reveals someone","Sound: Settings > Alerts"))),("VISITORS",(("num","range","List players within:","Players this close are listed","tiles",aK,aL),("check","friends","List guild and alliance members too","Unticked, green players are left out"),("check","confirm","Ban needs a second click within %d s"%int(R),"So the wrong person isn't banned"),("check","eject_foes","Alarm when a red or Foe enters the house",ca))),("HOUSE COMMANDS  (said out loud)",(("text","eject_cmd","Eject:","Ejects a player (owner, co-owner or friend)",b),("text","ban_cmd","Ban:","Bans a player (owner or co-owner)",b),("text","friend_cmd","Friend:","Makes a player a house friend (owner)",b),("gap",-90),("text","lock_cmd","Lock down:","Locks an item down (owner, co-owner or friend)",e),("text","release_cmd","Release:","Releases a locked-down item (owner or co-owner)",e),("gap",30),("note",Kit.wrap("Owner adds friends; owner and co-owners ban and release; friends eject and lock down.",w-28)[0],{"ndy":4,"h":24}))))
	def cd(old,new):
		if new["eject_foes"]!=old["eject_foes"]:a["eject_at"].clear()
		if new["confirm"]!=old["confirm"]and not a["minimized"]:k("redraw")()
	Z=Kit.Page(b,cc,aU,cd,cb,strict=True);aT()
	def ce(*b):
		if not a["shutting"]and a["phase"]!="idle":a["scan_poke"]=True
	def cf():a.update({"shutting":False,"docked":False,"queue":[],"phase":"idle","house":None,"house_wait":None,"confirm":None,"visitors":[],"near":0,"scan_at":0.,"ncache":{},"log_dirty":False,"log_save_at":0.,"pos":None,"moved_at":0.,"note":"","note_until":0.,"in_house":None,"house_pos":None,"house_at":0.,"inside":{},"open_visits":{},"visits_dirty":False,"visits_save_at":0.,"visits_redraw":False,"eject_at":{},"foe":{},"held":None,"held_at":0.,"minimized":r.start_min()});r.slot=None;q.update({"k":1.,"full":None});aT();a["rd"]=Journal.reader();ay(al,"Someone revealed",bz);ay(aO,"Red or Foe in your house",bA);a3();Kit.hook_once(a,"hooked",("ApiMobileCreated",ce));r.dock(fit=True,exact=True,verify=True,drawn_at=bN);i.update({"shutting":False,"queue":[]});o.dock(fit=True,min=a7)
	def cg():
		if d["g"]is None:return
		if Kit.closed(d):return
		b=time.time();f=HOST.me()
		while a["queue"]:
			c=a["queue"].pop(0);g=c[0]if isinstance(c,tuple)else c
			if not r.action(c)and g in bg:bg[g](c,b,f)
		if a["log_dirty"]and b>=a["log_save_at"]:a["log_save_at"]=b+bm;aV()
		if a["visits_dirty"]and b>=a["visits_save_at"]:a["visits_save_at"]=b+bp;aW()
		if a["visits_redraw"]:a["visits_redraw"]=False;av()
		if i["queue"]:
			del i["queue"][:]
			if Kit.zone_up(G)or i["g"]is not None:C()
		if f is None:return
		for h in a["rd"].new():b0(h)
		if ba(b,f):bZ(b)
		b2(b)
		if a["house"]is None:
			if a["sweep"]and a["phase"]=="idle"and(ax(b)<=aN or b>=a["held_at"]):
				a["held_at"]=b+aN;e=bd(b)
				if e!=a["held"]:
					j,a["held"]=a["held"],e
					if e and not j:n("sweep waits: %s"%(e[:1].lower()+e[1:]),Kit.HUE_INFO)
				if a["house_wait"]is None and not a["held"]:be(b)
			b_(b);b1(b)
		if a["confirm"]and b>=a["confirm"][1]:a["confirm"]=None
		a9()
	def ch():
		a["shutting"]=i["shutting"]=True;a["house_wait"]=None;p(f);aU()
		if a["log_dirty"]:aV()
		if a["open_visits"]:bc(time.time())
		if a["visits_dirty"]:aW()
		an.close()
	return{"start":cf,"tick":cg,"stop":ch,"client_tick":True,"config_height":Z.height,"build_config":Z.build,"poll_config":Z.poll,"config_closed":Z.closed}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("butler","Property Butler","House sweeps, visitors, eject and ban",_module_butler,.1,category="Skills and home")
