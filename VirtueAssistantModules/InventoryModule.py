def _module_inventory():
	aE=Client.on_client_thread;ay=Follow.toggle;aF=HOST.alert;aG=HOST.alert_kind;az=HOST.bar_alive;aH=HOST.cursor_busy;aI=HOST.cursor_ok;aJ=HOST.dock_add;aK=HOST.dock_remove;aL=HOST.dock_wanted;V=HOST.layout_holds;aj=HOST.layout_locked;aA=HOST.layout_rect;aM=HOST.pack_dirty;aq=HOST.pack_items;aN=HOST.pack_ver;aO=HOST.pick_target;af=HOST.refresh_settings;ar=HOST.release_cursor;aP=HOST.show_settings;ak=Journal.find;aQ=Journal.reader;H=Kit.ART_CLOSE;aR=Kit.ART_MIN;X=Kit.ART_OK;I=Kit.ART_PAGE;L=Kit.ART_PLAY;aS=Kit.ART_RESTORE;al=Kit.CORNER_ART;B=Kit.GAP;v=Kit.HUE_BAD;J=Kit.HUE_GOOD;l=Kit.HUE_INFO;D=Kit.HUE_TEXT;E=Kit.HUE_TITLE;K=Kit.MARGIN;aT=Kit.MIN_TIP;aU=Kit.REAGENTS;aV=Kit.RESTORE_TIP;at=Kit.SECTION_TILE;aW=Kit.WINDOW_BG;aB=Kit.adapt;au=Kit.add_check;e=Kit.add_label;Y=Kit.add_pic;z=Kit.add_section;av=Kit.add_textbox;P=Kit.add_tiled;Z=Kit.add_window_frame;m=Kit.art_button;aa=Kit.attach;am=Kit.basics;Q=Kit.catcher;ab=Kit.client_control;aX=Kit.closed;F=Kit.count;aY=Kit.data_path;R=Kit.dispose;T=Kit.find_item;C=Kit.fit;U=Kit.flush;ac=Kit.get_var;aw=Kit.held_item;aC=Kit.hook_once;u=Kit.is_open;aZ=Kit.kv_load;a_=Kit.kv_save;ad=Kit.moved_by_code;ax=Kit.on_click;a0=Kit.on_client;a1=Kit.on_moved;S=Kit.pic_size;an=Kit.place;M=Kit.put_var;a2=Kit.save_min;a3=Kit.save_pos;aD=Kit.screen;N=Kit.set;A=Kit.set_text;a4=Kit.show_window;a5=Kit.text_px;o=Kit.text_w;a6=Kit.title_bar;a7=Kit.title_catcher;a8=Kit.ui_pos;ae=Kit.was_clicked;a9=Kit.weight_bar;ao=Kit.with_tip;ba=Kit.write_safe;ag=Kit.zone_up;be="inventory";bf="Inventory"
	def bb():
		from System import AppDomain;from System.Reflection import BindingFlags
		for a in AppDomain.CurrentDomain.GetAssemblies():
			t=a.GetType("ClassicUO.Assets.TileDataLoader")
			if t is not None:return t.GetField("_staticData",BindingFlags.Static|BindingFlags.NonPublic)
		return
	ap=("REAGENTS","POTIONS","SCROLLS","OTHER");ai=tuple((bm.lower(),"REAGENTS")+aU[bm]for bm in("BP","BM","GA","GI","MR","NS","SS","SA"));ai+=(("bw","REAGENTS","Bat Wing",3960),("gd","REAGENTS","Grave Dust",3983),("db","REAGENTS","Daemon Blood",3965),("nc","REAGENTS","Nox Crystal",3982),("pi","REAGENTS","Pig Iron",3978),("p_heal","POTIONS","Heal",3852),("p_cure","POTIONS","Cure",3847),("p_refresh","POTIONS","Refresh",3851),("p_str","POTIONS","Strength",3849),("p_agi","POTIONS","Agility",3848),("p_ns","POTIONS","Night Sight",3846),("p_expl","POTIONS","Explosion",3853),("p_poison","POTIONS","Poison",3850),("s_recall","SCROLLS","Recall",8012),("s_gate","SCROLLS","Gate Travel",8032),("s_mark","SCROLLS","Mark",8025),("s_gheal","SCROLLS","Greater Heal",8009),("s_heal","SCROLLS","Heal",7985),("s_cure","SCROLLS","Cure",7991),("s_acure","SCROLLS","Arch Cure",8005),("s_mr","SCROLLS","Magic Reflection",8016),("s_invis","SCROLLS","Invisibility",8024),("s_reveal","SCROLLS","Reveal",8028),("s_tele","SCROLLS","Teleport",8002),("s_prot","SCROLLS","Protection",7995),("s_bless","SCROLLS","Bless",7997),("s_res","SCROLLS","Resurrection",8039),("o_band","OTHER","Bandages",3617),("o_arrow","OTHER","Arrows",3903),("o_bolt","OTHER","Bolts",7163))
	def bc(g,graphic,hue,x,y,size):
		p=G.CreateGumpItemPic(graphic,size,size);p.SetRect(x,y,size,size)
		if hue:p.Hue=hue
		p.DrawBorder=False;p.SetAcceptMouseInput(False);g.Add(p)
	def O(n):return "{:,}".format(int(n))
	def bd(key,g,xy):
		a=aA(key)
		if a is None or xy is None or(xy[0],xy[1])==(a[0],a[1]):return
		g.SetPos(int(a[0]),int(a[1]));Kit.note_rect(g,a[0],a[1]);ad(g)
	def bg():
		aJ="bag";ao="Bags"
		try:import clr;from System import Array,Object,Byte,Single,UInt16,UInt32;from System.Reflection import BindingFlags;dd=True
		except Exception:dd=False
		eD=8;bX,a_=1,50;bv=(142,94);de=(150,130);bd=600;co=4;df=30;eE,eF=104,64;eG=.1;eH=.8;eI=.002;eJ=3;eK=81;cp=1000;eL=(2330,2350);eM=(3834,8787,8786,9100,9120,11600);dg,dh,eN=60,30,46;eO=20;bK=20;eP="999";bL="UnifiedBag_shrunk";a3=44;cq=500;bM=132;bY=116;aX=6;bZ=8;cr=5;eQ=9;b_=(36,32);bw=(60,80);eR=7012;eS=7013;di=(2117,2118,2118);bN=4;eT=20;eU=24;dj=10;dk=0x7E57CA7C;eV=3;eW=.1;eX=.05;eY=6;eZ=8;e_=.5;e0=.09;e1=20;e2=4;e3=.3;b0=2;e4=200;dl=6;dm=5.;e5=1.3;dn=1.;e6=1.;e7=3;e8=["fizzles","concentration is disturbed"];e9=["already casting","not yet recovered"];fa=["More reagents are needed"];fb=["Insufficient mana","not have enough mana"];bm=68;ct=8.;fc=.15;fd=2;cu=3000;cv=400;fe=8;do=2.;ff=600;bx=.7;fg=600;dp=3;dq=2;b1=24;fh=125;fi=["cannot hold more"];fj=["must wait to perform another action"];b2=(("reagents","Reagents",(3962,3963,3972,3973,3974,3976,3980,3981)+(3960,3965,3978,3982,3983)),("gems","Gems",tuple(range(3855,3889))),("potions","Potions",tuple(range(3846,3854))),("scrolls","Scrolls",tuple(range(7981,8045))+(3827,)),("gold","Gold",(3821,3822,3823)),("bandages","Bandages",(3617,3817)),);fk=tuple(hQ[0]for hQ in b2);bz="#5C544A";dr="#7A7066";be,aK,aA=J,l,v;cx="UnifiedBag_cmd";ds="UnifiedBag_state";dt=aJ
		class Bag(object):
			def __init__(self,**a):self.update(**a)
			def update(self,**a):self.__dict__.update(a)
		du={};hM=dict(du);p={"cfg_bad":False,"slots":eD,"cols":0,"rows":0,"assign":{},"frame_x":200,"frame_y":120,"saved_fx":200,"saved_fy":120,"cell_w":bv[0],"cell_h":bv[1],"fit_pending":True,"fit_seen":None,"trim":True,"opacity":.9,"scale_pct":100,"scale_items":False,"driving":False,"drive_fixed":False,"drive_told":False,"hb_frame":-1,"hb_time":0.,"opacity_pending":None,"icons_used":None,"status_text":"","own_cell":None,"mgr_x":120,"mgr_y":140,"trp_x":200,"trp_y":180,"mgr_min":False,"trp_min":False,"minimized":False,"docked":False,"bare":False,"side_hidden":False,"link_state":None,"attach":None,"attach_g":None,"canvas":None,"side_pw":0,"detached_at":0.,"grid_wh":None,"names":{},"wait_player":False,"wait_load":False,"load_wanted":False,"load_text":None,"trap_sel":set(),"trap_extra":[],"job":None,"queue":[],"reported":False,"dirty_frame":True,"dirty_mgr":False,"dirty_trp":False,"open_mgr":False,"open_trp":False,"want_mgr":False,"want_trp":False,"save_in":-1,"to_write":None,"shutting":False,"flt_pick":None,"quick_at":0.,"filters":[],"open_flt":False,"dirty_flt":False,"flt_min":False,"flt_x":260,"flt_y":120,"rules":{},"sort":None,"srt_x":240,"srt_y":160,"srt_min":False,"open_srt":False,"want_srt":False,"dirty_srt":False,"layout":(),"geom":(1,bv[0],bv[1],0),"bar_raw":None,"grid_raw":None,"grid_info":(None,False),"slot_raws":()};ap={"g":None,"c":{},"store":({},{}),"side_status":None,"bar":None,"grid":None,"mgr":None,"trp":None,"trap_checks":[],"srt":None,"rule_checks":[],"search_box":None,"counts":[],"count_state":{}};dv,dw,hN=am(p,ao)
		def ay(kind,*a):
			def b(*b):dw.add((kind,)+a)
			return b
		def bA(key):R(ap.get(key));ap[key]=None
		def a4(ctrl):ctrl.SetAcceptMouseInput(False);return ctrl
		def a8(x,y,w,h,color,alpha):b=G.CreateGumpColorBox(alpha,color);b.SetRect(x,y,w,h);return b
		def bf(g,text,x,y,hue=None):return a4(e(g,text,x,y,hue))
		def b3(k,w,h,title,c,d):M=K;a=p[k+"_min"];g=G.CreateGump(True,True);an(g,p[k+"_x"],p[k+"_y"],w,h);Z(g,w,h,corners=not a);z(g,M,M,w-2*M,30);e(g,title,M+30,M+7,E);a7(g,M,M,w-2*M-84,30,c,key="bag_"+k);b=({},{});m(g,b,"min",aS if a else aR,w-M-74,M+7,None,aV if a else aT,on_click=c);m(g,b,"close",H,w-M-54,M+4,None,"Close this window",on_click=d);return g,b,M+30+B
		def b4(k,g,moved,**more):G.AddGump(g);a1(g,moved);ap[k]=g;ap.update(more)
		def bg():p["save_in"]=e1
		def bh():p["dirty_frame"]=True;bg()
		def bi(text,n):text=text or "";return text if len(text)<=n else text[:n-1]+"~"
		def a5(serial,c=True):
			a=p["names"].get(serial)
			if a is None:
				b=T(serial)
				if not b:return "0x%08X (not loaded)"%serial
				a=b.Name or "Container"
				if len(p["names"])>=e4:p["names"]={}
				p["names"][serial]=a
			return("%s  0x%08X"%(a,serial))if c else a
		def dx():p["names"]={}
		ai=Bag(tried=False,ok=False,can_ok=False,error="",f_tiles=None);r=Bag(frame=0,gumps={},managed=set(),trimmed=set(),bounds={},scale=1.,max_w=0,max_h=0,disabled=False,error="",fail_streak=0,open_count=0,catchers={},icons=None,hook_calls=0,pre_calls=0,glist=None,head=None,count=-1,lay=None,want=frozenset(),placed={},bar_at=None,full_frame=-1000,full_at=0.,fulls=0,labels_for=(None,None),meas={},opened=frozenset(),hold=None,ginfo={},catch_ok={},gtr={});aq={"ver":0,"regions":{},"order":[],"orient":"rows","breaks":None,"sig":None,"items":None,"kinds":{},"size":None,"slow":False,"job":None};b5={"done":None};JR={"rd":None};bB={};bO=[];O={"ctrl":None,"rect":None,"texts":True,"said":None,"sum_i":0,"art":{},"world":None,"tiles":None,"prof_at":0.,"sum_at":0.,"hooked":False,"poked":set(),"poke_at":0.}
		def fl():
			if not dd:ai.error="clr module unavailable";return
			try:
				b=API.GetType().Assembly;clr.AddReference(b);from ClassicUO.Game.UI.Controls import Control;from ClassicUO.Game.UI.Gumps import ContainerGump;from ClassicUO.Game.UI.Controls import ClickPriority;a=BindingFlags.Instance|BindingFlags.NonPublic;c=BindingFlags.Static|BindingFlags.Public|BindingFlags.NonPublic;d=clr.GetClrType(ContainerGump);ai.ContainerGump=ContainerGump;ai.f_data=d.GetField("_data",a);ai.f_pic=d.GetField("_gumpPicContainer",a);ai.f_hit=d.GetField("_hitBox",a);e=clr.GetClrType(Control);ai.m_offset=e.GetMethod("SetHitTestOffset",a);ai.f_bounds=e.GetField("_bounds",a);ai.Point=clr.GetPythonType(e.GetProperty("Location").PropertyType);ai.Rect=clr.GetPythonType(ai.f_bounds.FieldType);f=b.GetType("ClassicUO.Game.Managers.UIManager");ai.p_gumps=f.GetProperty("Gumps",c);ai.p_cscale=f.GetProperty("ContainerScale",c);h=b.GetType("ClassicUO.Configuration.ProfileManager");ai.p_profile=h.GetProperty("CurrentProfile",c)
				for g in("f_data","f_pic","f_hit","m_offset","f_bounds","p_gumps","p_cscale","p_profile"):
					if getattr(ai,g)is None:raise Exception("client member not found: "+g)
				class FrameHook(Control):
					def PreDraw(self):r.pre_calls+=1;r.hook_calls+=1;cz()
					def Draw(self,a,x,y):
						if r.pre_calls==0:r.hook_calls+=1;cz()
						return True
				class DropCatcher(Control):
					def Draw(self,a,x,y):return True
				ai.Hook=FrameHook;ai.Catcher=DropCatcher;ai.LowPriority=ClickPriority.Low;ai.ok=True
			except Exception as i:ai.ok=False;ai.error=str(i);return
			fm()
		def fm():
			ai.can_ok=False
			try:
				from ClassicUO.Game.UI.Controls import Control,ItemGump
				class BagCanvas(Control):
					def Draw(self,a,x,y):
						try:w,h=self.va_wh
						except Exception:return True
						try:fx()
						except Exception:pass
						if a.ClipBegin(int(x),int(y),int(w),int(h)):
							try:
								Control.Draw(self,a,x,y)
								if O["texts"]:ga(a,int(x),int(y))
							finally:a.FlushBatch();a.ClipEnd()
						return True
					def OnMouseUp(self,x,y,button):
						try:
							if f2(int(x),int(y),button):return
						except Exception as e:r.error="canvas: %s"%e
						Control.OnMouseUp(self,x,y,button)
					def OnMouseDoubleClick(self,x,y,button):
						try:
							if f4(int(x),int(y),button):return True
						except Exception as e:r.error="canvas: %s"%e
						return Control.OnMouseDoubleClick(self,x,y,button)
					def OnMouseOver(self,x,y):
						try:f6(self,int(x),int(y))
						except Exception:pass
						Control.OnMouseOver(self,x,y)
				class BagLayer(Control):pass
				class CanvasItem(ItemGump):
					def OnMouseUp(self,x,y,button):ai.up_item=self;ItemGump.OnMouseUp(self,x,y,button)
				ai.Canvas,ai.Layer,ai.CanvasItem,ai.ItemGump=(BagCanvas,BagLayer,CanvasItem,ItemGump);ai.up_item=None;ai.Mouse=Tz.T("ClassicUO.Input.Mouse");ai.Actions=Tz.T("ClassicUO.Game.GameActions");ai.f_tiles=bb();ai.can_ok=True
			except Exception as e:ai.can_ok=False;r.error="canvas: %s"%e
		def cy(a):
			try:return a()
			except Exception:return a(None)
		def dy(grid,tell):
			if not ai.ok or r.disabled or p["drive_fixed"]:return
			try:
				a=cy(ai.Hook);a.AcceptMouseInput=False;b=p["grid_info"][0]
				if b is not None and aE():
					with Kit.quiet:
						a.Parent=b
						if b.Children.Contains(a):return
				grid.Add(a)
			except Exception as e:
				p["driving"]=p["drive_fixed"]=True;r.error="draw hook: %s"%e
				if tell:API.SysMsg(ao+": couldn't install the draw hook (%s); the script keeps the bags in place."%e,aK)
		def dz(grid):safe(lambda:setattr(grid,"LayerOrder",type(grid.LayerOrder).Under))
		dA={}
		def fo(w):return w.Gump
		fp=(fo,ab)
		def bj(a):
			if a is None:return
			t=type(a);b=dA.get(t)
			if b is not None:
				with Kit.quiet:
					v=b(a)
					if v is not None:return v
			for c in fp:
				if c is b:continue
				try:v=c(a)
				except Exception:continue
				if v is not None:dA[t]=c;return v
			return
		def bn(fn):return a0(fn,False)
		def cz():
			try:fv();r.fail_streak=0
			except Exception as e:r.error=str(e);r.fail_streak+=1
			except:r.error="unknown error";r.fail_streak+=1
			if r.fail_streak>120:r.disabled=True
		def dB(g,x,y):
			a=g.Offset
			if a.X!=x or a.Y!=y:ai.m_offset.Invoke(g,Array[Object]([x,y]))
		def b6():
			b={};c=ai.p_gumps.GetValue(None);r.glist=c;a=c.First
			while a is not None:
				v=a.Value
				if isinstance(v,ai.ContainerGump)and not v.IsDisposed:b[int(v.LocalSerial)]=v
				a=a.Next
			r.gumps=b
			try:r.scale=float(ai.p_cscale.GetValue(None))
			except Exception:pass
		def fq():
			b=r.glist
			if b is None:return
			a=b.First;d=a.Value if a is not None else None;e=b.Count
			if d is r.head and e==r.count:return
			r.head,r.count=d,e;f=r.want
			if not f:return
			g=r.gumps;n=0
			while a is not None and n<eZ:
				v=a.Value
				if isinstance(v,ai.ContainerGump)and not v.IsDisposed:
					c=int(v.LocalSerial)
					if c in f and g.get(c)is not v:g[c]=v
				a=a.Next;n+=1
		def fr(g):b=dR(g);s=r.scale;a,c=int(b[0]*s),int(b[1]*s);return a,c,int(b[2]*s)-a,int(b[3]*s)-c
		def dC(idx):b,c,d,a=p["geom"];r,e=divmod(idx,b);return p["frame_x"]+e*(c+a),p["frame_y"]+bq()+r*(d+a)
		def cA(c):a=c.Location;return int(a.X),int(a.Y)
		def bo(c,x,y):
			a=c.Location
			if a.X!=x or a.Y!=y:c.Location=ai.Point(x,y)
		def cB(c):r=ai.f_bounds.GetValue(c);return int(r.Width),int(r.Height)
		def cC(g):
			r.managed.discard(g);r.placed.pop(g,None);b=g in r.trimmed;r.trimmed.discard(g)
			if g.IsDisposed:r.catchers.pop(g,None);return
			dE(g)
			if not g.IsVisible:g.IsVisible=True
			dB(g,0,0);g.AcceptMouseInput=True;g.CanMove=True;a=ai.f_pic.GetValue(g)
			if a is not None:a.Alpha=1.
			if b and not g.IsMinimized:g.RequestUpdateContents()
		def bC(g,c):
			a=g.Children
			while a.Contains(c):a.Remove(c)
		def dD(g,c):
			bC(g,c)
			if not c.IsDisposed:c.Dispose()
		def dE(g):
			r.catch_ok.pop(g,None);c=r.catchers.pop(g,None)
			if c is not None:dD(g,c)
		def fs(g):
			b=r.catchers.get(g)
			for a in list(g.Children):
				if a is not b and int(a.LocalSerial)==dk:dD(g,a)
		def ft(g,left,top,iw,d):
			c=r.catchers.get(g);a=g.Children;n=a.Count;b=r.catch_ok.get(g)
			if b is not None and c is not None and b[0]is c and b[1]==n and b[2]is(a[n-1]if n else None)and b[3]==(left,top,iw,d)and not c.IsDisposed:return
			if c is None or c.IsDisposed or not a.Contains(c):
				if g not in r.catchers:fs(g)
				c=ai.Catcher();c.LocalSerial=dk;c.AcceptMouseInput=True;c.Priority=ai.LowPriority;c.Parent=g;bC(g,c);a.Insert(0,c);r.catchers[g]=c
			elif a.IndexOf(c)!=0 or a.LastIndexOf(c)!=0:bC(g,c);a.Insert(0,c)
			e=ai.f_bounds.GetValue(c)
			if(e.X,e.Y,e.Width,e.Height)!=(left,top,iw,d):ai.f_bounds.SetValue(c,ai.Rect(left,top,iw,d))
			if not c.IsVisible:c.IsVisible=True
			n=a.Count
			if len(r.catch_ok)>=cD:r.catch_ok.clear()
			r.catch_ok[g]=(c,n,a[n-1]if n else None,(left,top,iw,d))
		cD=64
		def cE(g):
			a=r.ginfo.get(g)
			if a is None:
				a=(int(g.Graphic),bool(g.IsChessboard or g.IsBackgammonBoard))
				if len(r.ginfo)>=cD:r.ginfo.clear()
				r.ginfo[g]=a
			return a
		def fu(g,idx,trim):
			if g.CanMove:g.CanMove=False
			dB(g,0,0);c,d=dC(idx);k=cE(g)[1]
			if g.IsMinimized or k or not trim:
				if g in r.trimmed:
					r.trimmed.discard(g);dE(g)
					if not g.IsMinimized:g.RequestUpdateContents()
				if not g.AcceptMouseInput and g.IsVisible:g.AcceptMouseInput=True
				a=ai.f_pic.GetValue(g)
				if a is not None and abs(a.Alpha-p["opacity"])>.01:a.Alpha=p["opacity"]
				bo(g,c,d)
				if g.IsMinimized:return 0,0,a,False
				w,l=cB(g);return w,l,a,False
			e,f,h,i=fr(g);a=ai.f_pic.GetValue(g)
			if a is not None and a.IsVisible:a.IsVisible=False
			b=ai.f_hit.GetValue(g)
			if b is not None and b.IsVisible:b.IsVisible=False
			if g.AcceptMouseInput:g.AcceptMouseInput=False
			ft(g,e,f,h,i);bo(g,c-e,d-f);r.trimmed.add(g);j=int(round(eT*r.scale));return h+j,i+j,a,True
		def fv():
			if r.disabled or p["shutting"]:return
			B=p["bar_raw"];c,M=p["grid_info"];u=False;n=p["attach"];j=p["minimized"]
			if n is not None:
				j=j or not n.get("shown",True);e=gh()
				if e is not None and not e.IsDisposed:
					a,b=cA(e);a,b=a+int(n.get("dx",0)),b+int(n.get("dy",0));u=(a,b)!=r.bar_at;r.bar_at=(a,b);p["frame_x"],p["frame_y"]=a,b
					if c is not None and not c.IsDisposed:
						bo(c,a,b)
						if c.IsVisible==j:c.IsVisible=not j
			else:
				if M and c is not None and not c.IsDisposed:e,o,C=c,B,0
				else:e,o,C=B,c,a3
				if e is not None and not e.IsDisposed:
					a,b=cA(e);u=(a,b)!=r.bar_at;r.bar_at=(a,b);p["frame_x"],p["frame_y"]=a,b
					if o is not None and not o.IsDisposed:bo(o,a,b+C)
			q=p["layout"]
			if q is not r.lay:r.lay=q;r.want=frozenset([ah for by,ah in q])
			r.frame+=1;D=time.time();h=r.frame-r.full_frame>=eY and D-r.full_at>=e0
			if h:r.full_frame,r.full_at=r.frame,D;r.fulls+=1;b6()
			else:fq()
			E=h;N=h and r.fulls%10==1;h=h or u;F=p["trim"];P=(F,p["opacity"],p["geom"],bq(),aq["ver"]);s=set();f=set();v=x=0;i=None;Q=ai.f_pic;G=p["canvas"]is not None and not j
			if G:H=O["rect"]or(0,0,0,0);R,S=p["frame_x"]+H[0],p["frame_y"]+H[1];T=h or p["driving"];U=(O["seen_n"],O["seen_last"],O["seen_min"])
			for d,k in q:
				g=r.gumps.get(k)
				if g is None:continue
				if g.IsDisposed:
					if E:continue
					E=True;b6();g=r.gumps.get(k)
					if g is None or g.IsDisposed:continue
				f.add(d)
				if G:
					try:
						if fw(g,k,R,S,T,U):
							if i is None:i=g
							s.add(g);r.managed.add(g)
					except Exception as y:r.error="bag 0x%08X: %s"%(k,y)
					continue
				if i is None:i=g
				s.add(g);r.managed.add(g)
				try:
					if j:
						if g.IsVisible:g.IsVisible=False
						r.placed.pop(g,None);continue
					if not g.IsVisible:g.IsVisible=True
					I=bool(g.IsMinimized);J=(d,P,I);l=r.placed.get(g);m=Q.GetValue(g)
					if not h and l is not None and l[0]==J and m is l[2]and not(l[3]and m is not None and m.IsVisible):w,t=l[1]
					else:
						w,t,m,K=fu(g,d,F);r.placed[g]=(J,(w,t),m,K)
						if I:V,W=cB(g);r.meas[d]=(V,W,r.scale,True,None)
						else:r.meas[d]=(w,t,r.scale,False,int(g.Graphic)if K else None)
					v,x=max(v,w),max(x,t)
				except Exception as y:r.error="bag 0x%08X: %s"%(k,y)
			r.open_count=len(f)
			if f!=r.opened:
				r.opened=frozenset(f)
				for d in[ch for ch in r.meas if ch not in f]:r.meas.pop(d,None)
			if i is not None and N:
				try:X=int(ai.f_data.GetValue(i).IconizedGraphic)or bw[1];r.icons=(int(i.Graphic),X)
				except Exception:pass
			if len(r.managed)>len(s):
				for g in[cs for cs in r.managed if cs not in s]:cC(g)
			r.max_w,r.max_h=v,x;z=p["slot_raws"]
			if f!=r.labels_for[0]or z is not r.labels_for[1]:
				for d,Y in enumerate(z):
					L=d not in f
					for A in Y:
						if A is not None and A.IsVisible!=L:A.IsVisible=L
				r.labels_for=(f,z)
		def fw(g,serial,px,py,b,seen):
			if cE(g)[1]:
				if g in r.managed:cC(g)
				return False
			if g.IsVisible:g.IsVisible=False
			if g.AcceptMouseInput:g.AcceptMouseInput=False
			if b:
				if g.CanMove:g.CanMove=False
				bo(g,px,py)
			a=g.Children;n=a.Count
			if seen[0].get(serial)!=n or seen[1].get(serial)is not(a[n-1]if n else None)or seen[2].get(serial)!=g.IsMinimized:
				if O["built"]==aq["ver"]and O["ctrl"]is not None:cd(serial,g)
			return True
		def fx():
			b=r.gumps
			for c in aq["order"]:
				a=aq["kinds"].get(c)
				if a is None or a[0]=="board"or a[0]=="closed":continue
				g=b.get(a[2])
				if g is not None and g.IsVisible:g.IsVisible=False
		def dF():
			for g in list(r.managed):
				with Kit.quiet:cC(g)
		def fy(minimize):
			a=set(p["assign"].values())
			def b():
				b6();n=0
				for s in a:
					g=r.gumps.get(s)
					if g is None or g.IsDisposed or g.IsChessboard or g.IsBackgammonBoard:continue
					if bool(g.IsMinimized)!=minimize:g.IsMinimized=minimize;n+=1
				return n
			return bn(b)
		def dG():
			def a():a=ai.p_profile.GetValue(None);return(int(a.ContainersScale),bool(a.ScaleItemsInsideContainers))
			return bn(a)
		def b7(pct,items):
			def a():
				a=ai.p_profile.GetValue(None);c=(int(a.ContainersScale)!=pct or bool(a.ScaleItemsInsideContainers)!=items);a.ContainersScale=Byte(pct);a.ScaleItemsInsideContainers=items;ai.p_cscale.SetValue(None,Single(pct/100.));r.scale=pct/100.
				if c:
					b=ai.p_gumps.GetValue(None).First
					while b is not None:
						v=b.Value
						if isinstance(v,ai.ContainerGump)and not v.IsDisposed:v.RequestUpdateContents()
						b=b.Next
				return c
			return bn(a)
		def dH(serial):
			if ai.ok and not r.disabled:g=r.gumps.get(serial);return g is not None and not g.IsDisposed
			a=T(serial);return bool(a)and u(safe(lambda:a.GetContainerGump()))
		def dI():a=safe(lambda:int(API.Player.Serial),0);return aY("_unified_bag_%d.cfg"%a)
		def dJ():dM(dL())
		def a9():
			p["save_in"]=-1
			if not aG()and p["canvas"]!="alone":p["saved_fx"],p["saved_fy"]=p["frame_x"],p["frame_y"]
			b=["slots=%d"%p["slots"],"cols=%d"%p["cols"],"rows=%d"%p["rows"],"frame_x=%d"%p["saved_fx"],"frame_y=%d"%p["saved_fy"],"cell_w=%d"%p["cell_w"],"cell_h=%d"%p["cell_h"],"trim=%d"%int(p["trim"]),"collapsed=%d"%int(p["minimized"]),"bare=%d"%int(p["bare"]),"side=%d"%int(p["side_hidden"]),"opacity=%d"%int(round(p["opacity"]*100)),"mgr_x=%d"%p["mgr_x"],"mgr_y=%d"%p["mgr_y"],"trp_x=%d"%p["trp_x"],"trp_y=%d"%p["trp_y"],"mgr_open=%d"%int(p["open_mgr"]),"mgr_min=%d"%int(p["mgr_min"]),"trp_open=%d"%int(p["open_trp"]),"trp_min=%d"%int(p["trp_min"]),"trapsel="+",".join(str(f)for f in sorted(p["trap_sel"])),"trapextra="+",".join(str(h)for h in p["trap_extra"]),]
			for a in sorted(p["assign"]):b.append("slot.%d=%d"%(a,p["assign"][a]))
			b+=["srt_x=%d"%p["srt_x"],"srt_y=%d"%p["srt_y"],"srt_open=%d"%int(p["open_srt"]),"srt_min=%d"%int(p["srt_min"])]
			for a in sorted(p["rules"]):
				c,d=p["rules"][a]
				if c or d:b.append("sort.%d=%s;%s"%(a,",".join(sorted(c)),",".join(str(i)for i in d)))
			p["to_write"]=(dI(),"\n".join(b))
			if not safe(lambda:HOST.by_key[aJ].running,False):cG()
		def cF():return bool(aH(aJ))
		def cG():
			a=p["to_write"]
			if a is None:return
			p["to_write"]=None;b,c=a
			if p["cfg_bad"]:return
			try:ba(b,c)
			except Exception as e:API.SysMsg(ao+": couldn't save its settings (%s)."%e,aA)
		def dK(text):return[int(a)for a in(text or "").split(",")if a.strip().isdigit()]
		def dL():return Kit.read_safe(dI())
		def dM(raw):
			p["cfg_bad"]=raw is None
			if raw is None:API.SysMsg(ao+": couldn't read its settings file, so changes aren't saved.",aA);return
			if not raw:return
			b,a={},{}
			for d in raw.splitlines():
				if "="in d:
					k,v=[n.strip()for n in d.split("=",1)];b[k]=v
					try:a[k]=int(v)
					except ValueError:pass
			p["slots"]=max(bX,min(a_,a.get("slots",p["slots"])));p["cols"]=max(0,min(a_,a.get("cols",0)));p["rows"]=max(0,min(a_,a.get("rows",0)));p["frame_x"],p["frame_y"]=aB(a.get("frame_x",p["frame_x"]),a.get("frame_y",p["frame_y"]));p["saved_fx"],p["saved_fy"]=p["frame_x"],p["frame_y"];p["cell_w"]=max(20,min(bd,a.get("cell_w",p["cell_w"])));p["cell_h"]=max(20,min(bd,a.get("cell_h",p["cell_h"])));p["fit_pending"]="cell_w"not in a;p["opacity"]=max(10,min(100,a.get("opacity",a.get("panel_a",90))))/100.
			for g,k,h in(("trim","trim",1),("minimized","collapsed",0),("bare","bare",0),("side_hidden","side",0),("mgr_min","mgr_min",0),("trp_min","trp_min",0),("want_mgr","mgr_open",0),("want_trp","trp_open",0),("srt_min","srt_min",0),("want_srt","srt_open",0)):p[g]=a.get(k,h)==1
			for k in("mgr","trp","srt"):x,y=aB(a.get(k+"_x",p[k+"_x"]),a.get(k+"_y",p[k+"_y"]));p.update(**{k+"_x":x,k+"_y":y})
			p["trap_sel"]=set(dK(b.get("trapsel")));p["trap_extra"]=dK(b.get("trapextra"));p["assign"],p["rules"]={},{}
			for k,v in b.items():
				e,j,i=k.partition(".")
				try:c=int(i)
				except ValueError:continue
				if not 0<=c<p["slots"]:continue
				if e=="slot"and a.get(k,0)>0:p["assign"][c]=a[k]
				elif e=="sort":
					f=fz(v)
					if f is not None:p["rules"][c]=f
		def fz(text):
			c,e,d=(text or "").partition(";");b=frozenset(f for f in(g.strip()for g in c.split(","))if f in fk);a=[]
			for p in d.split(","):
				p=p.strip()
				if p.isdigit()and 0<int(p)<=65535 and int(p)not in a:a.append(int(p))
			a=tuple(a[:b1]);return(b,a)if(b or a)else None
		aF={"told":None,"cols":None,"cell":None,"area":None}
		def dN(slots=None,cols=None,rows=None):
			slots=p["slots"]if slots is None else slots
			if cols is None and rows is None and aF["cols"]:c=max(1,min(slots,aF["cols"]));return c,int(math.ceil(slots/float(c)))
			cols=p["cols"]if cols is None else cols;rows=p["rows"]if rows is None else rows
			if cols>0 and rows>0:return cols,rows
			if cols>0:return cols,int(math.ceil(slots/float(cols)))
			if rows>0:c=int(math.ceil(slots/float(rows)));return c,int(math.ceil(slots/float(c)))
			c=max(1,int(math.ceil(math.sqrt(slots))));return c,int(math.ceil(slots/float(c)))
		def b8():return p["trim"]and ai.ok and not r.disabled
		b9=[None,None]
		def cH():
			a=p["assign"]
			if a==b9[0]and p["slots"]==b9[1]:return
			b=tuple(sorted((c,d)for c,d in a.items()if c<p["slots"]))
			if b!=p["layout"]:p["layout"]=b
			b9[0],b9[1]=dict(a),p["slots"]
		def fA():
			s=r.scale if ai.ok else 1.
			if b8():return int(bv[0]*s),int(bv[1]*s)
			return int(de[0]*s),int(de[1]*s)
		def cI():p["cell_w"],p["cell_h"]=fA();p["fit_pending"]=True;bh()
		def cJ(g):
			i=max(g-2*(bZ+aX),0);a,c=[[]],0
			for e in[("bagicons",b_[1]+22),("break",eQ),("spellicons",b_[1]+22),("stop",22+4+18),("quick",4*24),("tools",24+26+24)]:
				f,h=e;d=h+(cr if a[-1]else 0)
				if a[-1]and c+d>i and f!="break":a.append([]);c,d=0,h
				if f=="break"and not a[-1]:continue
				a[-1].append(e);c+=d
			for b in a:
				while b and b[0][0]=="break":b.pop(0)
				while b and b[-1][0]=="break":b.pop()
			a=[k for k in a if k];j=[sum(q[1]for q in n)+cr*(len(n)-1)for n in a];return a,j
		def fB(graphic,x,y,b,c,tip,handler):a=G.CreateGumpPic(graphic);d=a.GetWidth()or b;e=a.GetHeight()or c;k=min(b/float(d),c/float(e),1.);w,h=max(1,int(d*k)),max(1,int(e*k));a.SetRect(x+(b-w)//2,y+(c-h)//2,w,h);N(a,"ContainsByBounds",True);a.SetTooltip(tip);G.AddControlOnClick(a,handler);return a
		def cK(grid,e,k,d=0):
			w,n=br();i=n+bN;q,r=cJ(k-i);f=len(q)*bM+2*aX;b=max(k,max(r)+2*(bZ+aX)+i);Kit.add_resizepic(grid,aW,e,d,f,b);z(grid,e+aX,d+aX,f-2*aX,b-2*aX);x,A=p["icons_used"]
			for j,B in enumerate(q):
				s=e+aX+j*bM
				if j:grid.Add(a4(a8(s,d+aX+bZ,1,b-2*(aX+bZ),bz,.8)))
				a=s+(bM-bY)//2;y=d+(b-i-r[j])//2
				for c,t in B:
					if c in("bagicons","spellicons"):
						if c=="bagicons":u=((A,"Minimize every open slot bag",ay("set_min",True),"Minimize"),(x,"Restore every minimized slot bag",ay("set_min",False),"Restore"))
						else:u=((eR,"Cast Magic Trap on every ticked trap bag",ay("start_job","Magic Trap"),"Trap"),(eS,"Cast Magic Untrap on every ticked trap bag",ay("start_job","Magic Untrap"),"Untrap"))
						g=bY//2
						for v,(C,D,E,h)in enumerate(u):grid.Add(fB(C,a+v*g,y,g,b_[1],D,E));bf(grid,h,a+v*g+max(0,(g-o(h))//2),y+b_[1]+3,l)
					elif c=="stop":h=m(grid,ap["store"],"stop",H,a,y,"Stop","Stop the trap, untrap or sort run",on_click=ay("stop_all"));ap["stop_ctrls"]=[ap["store"][0].get("stop"),h];ap["side_status"]=bf(grid,p["status_text"],a,y+26,l);eo()
					elif c=="quick":g2(grid,a,y)
					elif c=="tools":g0(grid,a,y)
					elif c=="break":grid.Add(a4(a8(a,y+t//2,bY,1,bz,.8)))
					y+=t+cr
			bH(grid,e+f-aX-bN-w,d+b-aX-bN-n,False);return f,b
		def aG():return p["attach"]is not None
		def bp():return p["bare"]and not p["minimized"]and not aG()
		def fC():return ap.get("grid")if aG()or p["canvas"]=="alone"or bp()else ap.get("bar")
		def fD():
			if p["shutting"]or p["wait_player"]or not u(ap.get("grid")):return
			return "docked"if p["docked"]else("minimized"if p["minimized"]else "open")
		def bD(w,h,mode):
			f=(None,None);l=p["geom"]
			if not aG():
				d=(int(w),int(h))if(w is not None and h is not None)else None
				if(bE()and(d!=aF["told"]or(mode=="again"and d is not None))):p["dirty_frame"]=True
				aF["told"]=d
				if bE()and d is not None:return
			if w is not None and h is not None and l is not None:
				m,u,v,a=l;o=m*u+(m-1)*a;a=0 if b8()else co;q=max(0,(p["grid_wh"][0]if p["grid_wh"]else o)-o)
				if aG():q=0 if bG()else p["side_pw"]
				g=int(w)-q;s=int(h)-bq();e,i=p["cell_w"],p["cell_h"];n=max(1,p["slots"]);b=None
				for c in range(1,n+1):
					r=int(math.ceil(n/float(c)));j=(g-(c-1)*a)//c;k=(s-(r-1)*a)//r
					if j<e or k<i:continue
					t=min(j/float(e),k/float(i))
					if b is None or t>b[0]:b=(t,c,j,k)
				if b is None:c=max(1,min(n,(g+a)//max(1,e+a)));r=int(math.ceil(n/float(c)));b=(0,c,max(e,(g-(c-1)*a)//c),max(i,(s-(r-1)*a)//r))
				f=(b[1],(b[2],b[3]))
			if f!=(aF["cols"],aF["cell"]):aF["cols"],aF["cell"]=f;p["dirty_frame"]=True
		def fE():
			i=0 if b8()else co;c=0 if bG()else p["side_pw"];g=aF.get("area")
			if c and g is not None:m,j=br();k,n=cJ(g[1]-j-bN);c=len(k)*bM+2*aX
			d=int(round(r.scale*100))if ai.ok else p["scale_pct"];a=p["scale_pct"]if aN["pct"]is not None else d;l=df if(ai.ok and not r.disabled)else a
			if aN["pct"]is None or d==a:p["own_cell"]=(p["cell_w"],p["cell_h"],p["slots"]);e,f=float(p["cell_w"]),float(p["cell_h"])
			else:
				b=p["own_cell"]
				if b is not None and b[2]==p["slots"]:e,f=float(b[0]),float(b[1])
				else:h=a/float(max(1,d));e,f=p["cell_w"]*h,p["cell_h"]*h
			return e,f,i,p["slots"],c,a,a,min(l,a)
		bk={}
		def cL(h):
			k=("sw",h);v=bk.get(k)
			if v is None:
				c,a=br();b,d=cJ(h-a-bN);v=len(b)*bM+2*aX
				if len(bk)>=200:bk.clear()
				bk[k]=v
			return v
		def bE():return ai.ok and ai.can_ok and not r.disabled
		def dO():
			if not bE()or p["minimized"]or p["docked"]or p["shutting"]:return
			if aG():return None if aF["area"]is None or not p["attach"].get("shown",True)else "combined"
			return "alone"if aF["told"]is not None and V(aJ)else None
		fF=120
		def dP():return[("Settings",),("Trap bags",),("Slots",)]
		def cM(w):
			k=("tf",w,p["slots"]);v=bk.get(k)
			if v is None:
				a=Kit.title_plan(w,ao,dP(),str(p["slots"]));v=len(a[3])==len(dP())and a[4]>=K+30+o("..")+Kit.TITLE_GAP
				if len(bk)>=200:bk.clear()
				bk[k]=v
			return v
		def dQ(mode):
			if mode=="combined":b=aF["area"];a=0 if bG()else cL(b[1]);return 0,0,max(1,b[0]-a),max(1,b[1]),a
			w,h=aF["told"];M=K
			if p["bare"]or not cM(w):return M,M,max(1,w-2*M),max(1,h-2*M),0
			c=M+30+B;d=max(1,h-c-M);a=cL(d)
			if w-2*M-a<fF:a=0
			return M,c,max(1,w-2*M-a),d,a
		def dR(g,graphic=None):
			if graphic is None:graphic=int(g.Graphic)
			b=r.bounds.get(graphic)
			if b is None:a=ai.f_data.GetValue(g).Bounds;b=(int(a.X),int(a.Y),int(a.Width),int(a.Height));r.bounds[graphic]=b
			return b
		def fG(g,graphic):return cE(g)[1]or graphic in eL
		def dS():
			d=[];e=set()
			for h,c in p["layout"]:
				if c in e:continue
				e.add(c);g=r.gumps.get(c);a,b="closed",0
				try:
					if g is not None and not g.IsDisposed:
						f=r.ginfo.get(g);b=f[0]if f is not None else int(g.Graphic)
						if fG(g,b):a="board"
						elif g.IsMinimized:a="mini"
						else:dR(g,b);a="open"
				except Exception:a,b="closed",0
				d.append((h,b,a,c))
			return tuple(d)
		def dT(items):
			a=[]
			for c,d,e,f in items:b=r.bounds.get(d)if e=="open"else None;w,h=(max(1,b[2]-b[0]),max(1,b[3]-b[1]))if b is not None else(eE,eF);a.append((c,float(w*h),w/float(h)))
			return a
		def dU(f,W,s):
			n=len(f);S=sum(w[1]for w in f);a,b,c,d=[0.],[0.],[0.],[0.]
			for u,e,t in f:A=W*s*e/S;L=math.log(A/t);a.append(a[-1]+e);b.append(b[-1]+e*L);c.append(c[-1]+e*L*L);d.append(d[-1]+A)
			m=float("inf");g=[0.]+[m]*n;o=[0]*(n+1)
			for k in range(1,n+1):
				h,p=m,0
				for j in range(k):
					q=(d[k]-d[j])/W
					if q<=0:continue
					i=2.*math.log(q);r=g[j]+(c[k]-c[j])-2.*i*(b[k]-b[j])+i*i*(a[k]-a[j])
					if r<h:h,p=r,j
				g[k],o[k]=h,p
			l=[];k=n
			while k>0:l.append(k);k=o[k]
			l.reverse();return g[n],l
		def dV(a,W,b,breaks):
			S=sum(f[1]for f in a);c,j=0.,0
			for k in breaks:
				d=sum(W*b*a[g][1]/S for g in range(j,k));h=d/W
				if h<=0:return float("inf")
				for i in range(j,k):w=(W*b*a[i][1]/S)/h;c+=a[i][1]*math.log((w/h)/a[i][2])**2
				j=k
			return c
		def dW(a,W,b,keep=None):
			if not a:return "rows",[],0.
			d,i=dU(a,W,b);e=[(k,n,1./q)for k,n,q in a];f,j=dU(e,b,W);g=("columns",j,f)if f<eH*d else("rows",i,d)
			if keep is not None and keep[1]and keep[1][-1]==len(a):
				o,c=keep;h=dV(a,W,b,c)if o=="rows"else dV(e,b,W,c)
				if not g[2]<(1.-eG)*h:return o,list(c),h
			return g
		def dX(a,W,b,orient,breaks):
			if not a:return{}
			if orient=="columns":return dict((q,(G,t,by,ah))for q,(t,G,ah,by)in dX(a,b,W,"rows",breaks).items())
			S=sum(s[1]for s in a);e={};j,f,c=0,0.,0;n=len(a)
			for k in breaks:
				g=sum(W*b*a[w][1]/S for w in range(j,k));f+=g;h=int(round(f/W))if k<n else b;l,d=0.,0
				for i in range(j,k):l+=W*b*a[i][1]/S;m=int(round(W*l/g))if i<k-1 else W;e[a[i][0]]=(d,c,m-d,h-c);d=m
				c=h;j=k
			return e
		def fH(b,d,ah,cs,x,y):
			a=b[2]-int(d/cs);c=b[3]-int(ah/cs)
			if x<b[0]:x=b[0]
			elif x>a:x=a
			if y<b[1]:y=b[1]
			elif y>c:y=c
			return x,y
		def ca(a):return a[2]>=dg and a[3]>=dh+bK
		def dY(a):
			if ca(a):b,c,d,e=a;return b,c+bK,d,e-bK
			return a
		def dZ(a,ah,cs):return(float(a),float(ah))if aq.get("si")else(a/cs,ah/cs)
		def d_(box,pw,ph):
			a,b,g,h=box;c,d=a+pw//2,a+g-1-(pw-pw//2);e,f=b+ph//2,b+h-1-(ph-ph//2)
			if d<c:c=d=a+g//2
			if f<e:e=f=b+h//2
			return c,d,e,f
		def fI(b,box,f,ah,cs,g,by):a,c=dZ(f,ah,cs);d,e=float(max(1,b[2]-b[0])),float(max(1,b[3]-b[1]));u=.5 if a>=d else(g+a/2.-b[0])/d;v=.5 if c>=e else(by+c/2.-b[1])/e;u=0. if u<0 else(1. if u>1 else u);v=0. if v<0 else(1. if v>1 else v);return box[0]+u*box[2],box[1]+v*box[3]
		def fJ(b,box,a,ah,cs,px,py):c,d=dZ(a,ah,cs);u=(px-box[0])/float(max(1,box[2]));v=(py-box[1])/float(max(1,box[3]));u=0. if u<0 else(1. if u>1 else u);v=0. if v<0 else(1. if v>1 else v);e=int(round(b[0]+u*(b[2]-b[0])-c/2.));f=int(round(b[1]+v*(b[3]-b[1])-d/2.));return e,f
		def fK(a,ah):
			if aq.get("si"):b=r.scale or 1.;return max(1,int(a*b)),max(1,int(ah*b))
			return a,ah
		def fL(slot):
			b=aq["regions"].get(slot);a=aq["kinds"].get(slot)
			if b is None or a is None:return
			return a[2],dY(b),r.bounds.get(a[1]),r.scale or 1.
		def fM(d,serial,l,ah,pw,ph,e,by):
			if d is None:return 0,0
			m,f,g,n=d;a=bB.get(serial)
			if a is not None and a[0]==m and a[1]==e and a[2]==by:return int(a[3])-pw//2,int(a[4])-ph//2
			h,i,j,k=d_(f,pw,ph)
			if g is None:b,c=(h+i)//2,(j+k)//2
			else:b,c=fI(g,f,l,ah,n,e,by);b=max(h,min(i,b));c=max(j,min(k,c))
			return int(round(b))-pw//2,int(round(c))-ph//2
		def fN(serial,bag,a,by,b,c):
			if serial not in bB:
				if len(bO)>=cp:
					for s in bO[:cp//2]:bB.pop(s,None)
					del bO[:cp//2]
				bO.append(serial)
			bB[serial]=(bag,a,by,b,c)
		def d0():bB.clear();del bO[:]
		def fO():
			a=time.time()
			if a>=O["prof_at"]:
				O["prof_at"]=a+1.
				try:p["scale_items"]=bool(ai.p_profile.GetValue(None).ScaleItemsInsideContainers)
				except Exception:pass
			return p["scale_items"]
		def d1(sig,items,h,W,a,plan):
			b,c,l=plan;i=dX(h,W,a,b,c);d,e={},{}
			for f,j,k,g in items:d[f]=(k,j,g);e[g]=f
			aq.update({"ver":aq["ver"]+1,"regions":i,"slot_of":e,"order":[n[0]for n in items],"orient":b,"breaks":list(c),"sig":sig,"items":items,"kinds":d,"size":(W,a),"si":sig[4]});d0()
		def bP():
			try:return cS()is not None
			except Exception:return False
		def d2(mode):
			if p["canvas"]is not None:cO()
			p["canvas"]=mode;r.placed.clear();p["dirty_frame"]=True
		def fP():
			c=dO()
			if c!=p["canvas"]:
				if bP():return
				d2(c)
			if c is None:return
			d=dQ(c);b=dS();a=(d[2],d[3],b,round(r.scale or 1.,4),fO());e=b5["done"]
			if e is not None and len(e)>1 and e[0]==a and aq["job"]==a:
				if bP():return
				d1(*e);aq["job"]=None;aq["pending"]=None;return
			if a==aq["sig"]:aq["job"]=None;aq["pending"]=None;return
			if a==aq["job"]or bP():return
			W,g=d[2],d[3];f=dT(b);h=None
			if aq["items"]==b and aq["breaks"]is not None:h=(aq["orient"],aq["breaks"])
			if aq["slow"]:aq["job"]=a;aq["pending"]=(a,b,f,W,g,h);return
			i=time.time();j=dW(f,W,g,h)
			if time.time()-i>eI and len(f)>8:aq["slow"]=True
			d1(a,b,f,W,g,j)
		def d3():a,b=aq.get("pending"),b5["done"];return a is not None and(b is None or b[0]!=a[0])
		def fQ():
			a=aq.get("pending")
			if a is None or not d3():return
			b,e,c,W,d,f=a
			try:b5["done"]=(b,e,c,W,d,dW(c,W,d,f))
			except Exception:b5["done"]=(b,)
		def d4():
			c=O["ctrl"]
			if c is None:return
			with Kit.quiet:
				p=c.Parent
				if p is not None:bC(p,c)
		def fR(raw,index,x,y,w,h):
			c=O["ctrl"]
			if c is None or c.IsDisposed:cN();c=cy(ai.Canvas);c.AcceptMouseInput=True;c.Priority=ai.LowPriority;O["ctrl"]=c
			c.va_wh=(int(w),int(h));c.Parent=raw;a=raw.Children
			while a.Contains(c):a.Remove(c)
			a.Insert(min(index,a.Count),c);ai.f_bounds.SetValue(c,ai.Rect(int(x),int(y),int(w),int(h)));O["rect"]=(int(x),int(y),int(w),int(h))
			for b in O["layers"].values():ai.f_bounds.SetValue(b,ai.Rect(0,0,int(w),int(h)))
		def cN():O.update({"built":-1,"bsize":None,"parts":[],"icons":[],"bg":None,"layers":{},"pool":{},"owner":{},"items":{},"seen_n":{},"seen_last":{},"seen_min":{},"spot":{},"label":{},"count":{},"tip":None,"sums":{},"say_lbl":None,"sum_part":None,"alpha_set":None,"say_shown":False})
		cN()
		def cO():
			d4();c=O["ctrl"];O["ctrl"]=None
			if c is not None:safe(c.Dispose)
			cN();O["rect"]=None;d0();aq.update({"sig":None,"items":None,"breaks":None,"regions":{},"kinds":{},"slot_of":{},"order":[],"job":None,"pending":None,"size":None});aq["ver"]+=1;ap["counts"]=[];ap["count_state"]={}
		def d5():
			a=p["opacity"];b=O["bg"];c=(a,b)
			if O["alpha_set"]==c:return
			for d in([b]if b is not None else[])+O["icons"]:
				with Kit.quiet:
					if abs(float(d.Alpha)-a)>.001:d.Alpha=a
			O["alpha_set"]=c
		def d6(w):
			a=bj(w)if w is not None else None
			if a is None:return
			a.Parent=O["ctrl"];a.AcceptMouseInput=False;return a
		def fS():
			k=O["ctrl"];f=ap.get("grid")
			if k is None or f is None:return
			for E in O["parts"]:
				with Kit.quiet:bC(k,E);E.Dispose()
			O["parts"],O["icons"],O["label"],O["count"]=[],[],{},{};O["tip"]=None;O["alpha_set"]=None;F=O["say_lbl"];O["say_lbl"]=None
			if F is not None:safe(F.Dispose)
			W,m=aq["size"]or(O["rect"][2],O["rect"][3]);n,v=aq["regions"],aq["kinds"];c=[];c.append((P(f,at,0,0,W,m,p["opacity"]),"bg"))
			for a in aq["order"]:
				x,y,w,h=n[a]
				if x+w<W:c.append((a8(x+w-1,y,1,h,bz,.8),"seam"))
				if y+h<m:c.append((a8(x,y+h-1,w,1,bz,.8),"seam"))
			for a in aq["order"]:
				g,R,d=v[a]
				if g!="mini":continue
				o=r.gumps.get(d)
				try:z=int(ai.f_data.GetValue(o).IconizedGraphic)or bw[1]
				except Exception:z=bw[1]
				x,y,w,h=n[a];A,B=S(z);A,B=(A or 30),(B or 30);c.append((Y(f,z,x+(w-A)//2,y+(h-B)//2,mouse=False),"icon"))
			for a in aq["order"]:c.extend(fT(f,a,n[a],v[a]))
			if not aq["order"]:
				for T,V in enumerate(Kit.wrap("No bags yet. Click Slots to add some.",max(60,W-16))[:3]):c.append((e(f,V,8,8+20*T,l),"lbl"))
			G=[]
			for X in range(p["slots"]):q=e(f,"",0,0,J);N(q,"IsVisible",False);i=n.get(X);G.append((q,i[0],i[1],i[2],i[3])if i else(q,0,0,0,0));c.append((q,"count"))
			U();H=len([ah for ah in c if ah[1]!="count"]);t=[]
			for w,g in c:
				j=d6(w)
				if j is None:continue
				t.append(j)
				if g=="bg":O["bg"]=j
				elif g=="icon":j.Alpha=p["opacity"];O["icons"].append(j)
			O["parts"]=t;C=O["layers"];D={}
			for a in aq["order"]:
				b=C.pop(a,None)
				if b is None or b.IsDisposed:b=cy(ai.Layer);b.AcceptMouseInput=False
				ai.f_bounds.SetValue(b,ai.Rect(0,0,int(W),int(m)));D[a]=b
			if C:
				I=list(C.values());Z=O["pool"];K=[]
				for s in O["owner"]:
					L=Z.get(s)
					if L is not None:
						aa=L.Parent
						for b in I:
							if aa is b:K.append(s);break
				for s in K:cc(s)
				for b in I:safe(b.Dispose)
			O["layers"]=D;M=k.Children;Q=t[:H]+[D[by]for by in aq["order"]]+t[H:]
			for u in Q:u.Parent=k
			ab=set(Q)
			for u in list(M):
				if u not in ab:M.Remove(u)
			ap["counts"]=G;ap["count_state"]={};O["built"]=aq["ver"];O["bsize"]=(W,m);O["seen_n"],O["seen_last"],O["seen_min"]={},{},{}
			for a in aq["order"]:
				g,R,d=v[a];o=r.gumps.get(d)
				if o is not None and g in("open","mini"):cd(d,o)
				elif O["items"].get(d):
					for s in list(O["items"][d]):cc(s)
					O["items"][d]=[]
			if SR["counts"]:ci()
		def fT(grid,slot,h,info):
			b,p,f=info;x,y,w,i=h
			if w<dg or i<dh:return[]
			if b=="open"and not ca(h):return[]
			a=[];j="#%d"%(slot+1);a.append((e(grid,j,x+5,y+3,E),"lbl"));c=x+5+o(j)+6
			if b=="board":d=C("Game board",max(8,x+w-4-c));a.append((e(grid,d,c,y+3,l),"lbl"));return a
			g=a5(f,False);m=x+w-c-(6+o(eP)if b=="open"else 0)-10;d=C(g,max(8,m));a.append((e(grid,d,c,y+3,l),"lbl"));O["label"][slot]=(g,d!=g)
			if b=="open":n=len(O["items"].get(f)or());k=e(grid,str(n),c+o(d)+6,y+3,l);O["count"][f]=k;a.append((k,"lbl"))
			elif i>=eN:a.append((e(grid,"Minimized"if b=="mini"else "Closed",x+5,y+3+eO,l),"lbl"))
			return a
		def cb(g):
			w=O["world"]
			if w is None:
				try:w=O["world"]=g.World
				except Exception:w=None
			return w
		def fU(g,serial):
			w=cb(g)
			try:return w.Get(UInt32(int(serial)))if w is not None else None
			except Exception:return
		def cP(b,graphic):
			r=ai.f_bounds.GetValue(b);a=(int(r.Width),int(r.Height))
			if graphic not in O["art"]:
				if len(O["art"])>2000:O["art"].clear()
				O["art"][graphic]=a
			return a
		def fV(graphic):
			b=O["art"].get(graphic)
			if b is not None:return b
			g=p["grid_raw"]
			try:a=ai.CanvasItem(g,UInt32(0),UInt16(int(graphic)),UInt16(0),0,0,False)
			except Exception:return 44,44
			try:return(1,1)if a.IsDisposed else cP(a,graphic)
			finally:safe(a.Dispose)
		def cc(serial):
			c=O["pool"].pop(serial,None);b=O["owner"].pop(serial,None);O["spot"].pop(serial,None)
			if c is not None:
				try:
					p=c.Parent
					if p is not None:bC(p,c)
					c.Dispose()
				except Exception:pass
			if b is not None:
				a=O["items"].get(b)
				if a and serial in a:a.remove(serial)
		def cd(bag,g):
			u=g.Children;n=u.Count;F=bool(g.IsMinimized);O["seen_n"][bag]=n;O["seen_last"][bag]=u[n-1]if n else None;O["seen_min"][bag]=F;j=aq["slot_of"].get(bag);v=O["layers"].get(j)if j is not None else None
			if v is None:return
			G=[]
			if not F and aq["kinds"][j][0]=="open":
				for k in range(n):
					a=u[k]
					if isinstance(a,ai.ItemGump)and not a.IsDisposed:G.append(a)
			w,l=O["pool"],O["owner"];H=O["items"].get(bag)or[];m=[];e=[];I=cb(g);Q=fL(j);R=aq.get("si");J=r.scale or 1.;S=O["spot"];T,K,o=ai.CanvasItem,UInt32,UInt16;t=0
			for a in G:
				s=int(a.LocalSerial);d=int(a.Graphic)
				try:b=I.Get(K(s))if I is not None else None
				except Exception:b=None
				f=int(b.Hue)if b is not None else int(a.Hue);c=w.get(s)
				if c is not None and c.IsDisposed:cc(s);c=None
				if c is None:
					try:c=T(g,K(s),o(d),o(f),0,0,False)
					except Exception:continue
					if c.IsDisposed:continue
					c.va_art=cP(c,d);c.va_gr,c.va_hue,c.va_sz,c.va_xy=d,f,None,None;w[s]=c
				elif c.va_gr!=d:
					c.Graphic=o(d)
					if c.IsDisposed:w.pop(s,None);l.pop(s,None);continue
					c.va_art=cP(c,d);c.va_gr,c.va_sz=d,None
				if c.va_hue!=f:c.Hue=o(f);c.va_hue=f
				z=l.get(s)
				if z is not None and z!=bag:
					B=O["items"].get(z)
					if B and s in B:B.remove(s)
				l[s]=bag;C,D=c.va_art;h,i=(max(1,int(C*J)),max(1,int(D*J)))if R else(C,D)
				if c.va_sz!=(h,i):
					p=ai.f_bounds.GetValue(c)
					if int(p.Width)!=h or int(p.Height)!=i:ai.f_bounds.SetValue(c,ai.Rect(int(p.X),int(p.Y),h,i))
					c.va_sz=(h,i)
				L,M=(int(b.X),int(b.Y))if b is not None else cA(a);x,y=fM(Q,s,C,D,h,i,L,M)
				if c.va_xy!=(x,y):bo(c,x,y);c.va_xy=(x,y)
				S[s]=(x+h//2,y);m.append(s);e.append(c)
				if b is None:t+=s
				else:
					try:N=int(b.Amount)
					except Exception:N=0
					t=(t*31+s*7+L*131+M*137+f*139+N*149)&0x7FFFFFFF
			if H:
				U=set(m)
				for s in H:
					if s not in U and l.get(s)==bag:cc(s);bB.pop(s,None)
			O["items"][bag]=m;q=v.Children;E=q.Count==len(e)
			if E:
				for k in range(len(e)):
					if q[k]is not e[k]:E=False;break
			if not E:
				for c in e:c.Parent=v
				V=set(e)
				for c in list(q):
					if c not in V:q.Remove(c)
			P=O["count"].get(bag)
			if P is not None:A(P,str(len(m)))
			O["sums"][bag]=t
		def d7(g,b,t=0):
			w=cb(g);c=UInt32
			for s in b:
				try:a=w.Get(c(int(s)))if w is not None else None
				except Exception:a=None
				if a is None:t+=s;continue
				t=(t*31+s*7+int(a.X)*131+int(a.Y)*137+int(a.Hue)*139+int(a.Amount)*149)&0x7FFFFFFF
			return t
		d8=.2;fW=30;fX=.1;fY=40
		def fZ(*c):
			a=O["poked"]
			if p["shutting"]or len(a)>=fY:return
			d=aq.get("slot_of",())
			for b in c:
				try:s,e=int(b.Serial),int(b.Container)
				except Exception:continue
				for k in(e,s):
					if k in d:a.add(k)
				return
		def f_():
			d=time.time();f=O["poked"]
			if f and d>=O["poke_at"]:
				O["poke_at"]=d+fX;k=list(f);f.difference_update(k)
				for a in k:
					g=r.gumps.get(a)
					if g is not None and not g.IsDisposed:cd(a,g)
			h=aq["order"]
			if not h:return
			if 0<=O["sum_at"]-d<=d8:return
			O["sum_at"]=d+d8;e=O["sum_part"]
			if e is not None:
				a,g,b,n,c,i,t=e
				if O["items"].get(a)is not b or len(b)!=n or g.IsDisposed or r.gumps.get(a)is not g:e=None;O["sum_part"]=None
			if e is None:
				i=O["sum_i"]%len(h);O["sum_i"]=i+1;l,m,a=aq["kinds"][h[i]]
				if l!="open":return
				g=r.gumps.get(a)
				if g is None or g.IsDisposed:return
				b=O["items"].get(a);c=tuple(b)if b else();n,i,t=len(b)if b is not None else-1,0,0
			j=i+fW
			if j<len(c):O["sum_part"]=(a,g,b,n,c,j,d7(g,c[i:j],t));return
			O["sum_part"]=None
			if d7(g,c[i:],t)!=O["sums"].get(a):cd(a,g)
		def cQ(serial,hue):
			c=O["pool"].get(serial)
			if c is None:return
			h=int(hue)&65535
			try:
				if not c.IsDisposed and c.va_hue!=h:c.Hue=UInt16(h);c.va_hue=h
			except Exception:pass
		def bF(x,y):
			for a in aq["order"]:
				r=aq["regions"].get(a)
				if r is not None and r[0]<=x<r[0]+r[2]and r[1]<=y<r[1]+r[3]:return a
			return
		def cR(graphic):
			a=O["tiles"]
			if a is None:
				if ai.f_tiles is None:return
				a=O["tiles"]=ai.f_tiles.GetValue(None)
			return None if a is None or graphic<0 or graphic>=a.Length else a[graphic]
		def f0(it,hold):
			try:a=int(it.Graphic)
			except Exception:return True
			if a in eM:return True
			t=cR(a)
			if t is None:return True
			try:return True if bool(t.IsContainer)else bool(t.IsStackable)and a==int(Tz.get(hold,"Graphic"))
			except Exception:return True
		def d9(serial,button):
			a=O["owner"].get(serial);g=r.gumps.get(a)if a is not None else None
			if g is None or g.IsDisposed:return False
			g.OnMouseUp(0,0,button);return True
		def f1(bag):
			g=r.gumps.get(bag);w=cb(g)if g is not None else O["world"]
			if w is None:return True
			try:
				a=w.Get(UInt32(int(bag)))
				if a is None:return True
				b=w.Get(a.RootContainer);return b is None or int(b.Distance)<=eJ
			except Exception:return True
		def ea():API.PlaySound(eK)
		def f2(x,y,button):
			f=str(button);c=ai.up_item;ai.up_item=None;b=int(c.LocalSerial)if c is not None and not c.IsDisposed else None
			if f=="Left":
				d=cS()
				if d is not None:
					if b is not None:
						g=fU(r.gumps.get(O["owner"].get(b)),b)
						if g is not None and f0(g,d):return d9(b,button)
					a=bF(x,y)
					if a is None:return True
					f3(a,x,y,d);return True
				if p["flt_pick"]is not None:
					a=bF(x,y)
					if a is not None:
						e=aq["kinds"].get(a);h=dict((q,n)for n,q in p["layout"])
						if e is not None and e[2]in h:ay("filter_canvas_pick",h[e[2]])();return True
				if b is not None:
					if not O["texts"]and not API.HasTarget():O["said"]=(b,time.time())
					return d9(b,button)
				a=bF(x,y)
				if a is None:return False
				j,l,k=aq["kinds"][a];i=aq["regions"][a]
				if j=="open"and ca(i)and y<i[1]+bK and not API.HasTarget():ay("bag_min",k,True)();return True
				return False
			if f=="Right":
				if b is not None:return True
				a=bF(x,y)
				if a is not None and aq["kinds"][a][0]=="open":ay("bag_close",aq["kinds"][a][2])();return True
			return False
		def f3(slot,x,y,hold):
			o,p,a=aq["kinds"][slot]
			if not f1(a):ea();return
			b=int(Tz.get(hold,"Serial"))
			if b==a:ea();return
			import System;c=r.bounds.get(p)if o=="open"else None
			if c is None:Tz.call(None,"DropItem",(System.UInt32(b),65535,65535,0,System.UInt32(int(a)),False),ai.Actions);return
			d,e=x,y
			with Kit.quiet:
				if bool(ai.p_profile.GetValue(None).RelativeDragAndDropItems):h=Tz.get(hold,"MouseOffset");d,e=d+int(h.X),e+int(h.Y)
			f,g=fV(int(Tz.get(hold,"DisplayedGraphic")));q,s=fK(f,g);i=r.scale or 1.;j=dY(aq["regions"][slot]);t,u,v,w=d_(j,q,s);k=max(t,min(u,d));l=max(v,min(w,e));z,A=fJ(c,j,f,g,i,k,l);m,n=fH(c,f,g,i,z,A);Tz.call(None,"DropItem",(System.UInt32(b),m,n,0,System.UInt32(int(a)),False),ai.Actions);fN(b,int(a),m,n,k,l);safe(lambda:Tz.put(None,"CancelDoubleClick",True,ai.Mouse))
		def f4(x,y,button):
			if str(button)!="Left":return False
			a=bF(x,y)
			if a is None:return False
			b,d,c=aq["kinds"][a]
			if b in("closed","board"):ay("bag_use",c)();return True
			if b=="mini":ay("bag_min",c,False)();return True
			return False
		f5={"closed":"Double-click to open; drop an item to put it in","mini":"Double-click to restore; drop an item to put it in","board":"Double-click to open the board; drop an item to put it in","body":"Right-click to close","line":"Click to minimize"}
		def f6(c,x,y):
			a=bF(x,y);b=None
			if a is not None:
				e=aq["kinds"][a][0];b=e
				if e=="open":r=aq["regions"][a];b="line"if ca(r)and y<r[1]+bK else "body"
			f=(a,b,aq["ver"])
			if f==O["tip"]:return
			O["tip"]=f;g=f5.get(b,"")
			if b=="line":
				d=O["label"].get(a)
				if d is not None and d[1]:g="%s. Click to minimize"%d[0]
			c.SetTooltip(g)
		def f7(bag):API.UseObject(bag)
		def f8(bag,value):
			g=r.gumps.get(bag)
			if g is not None and not g.IsDisposed and bool(g.IsMinimized)!=value:g.IsMinimized=value
		def f9(bag):
			g=r.gumps.get(bag)
			if g is not None and not g.IsDisposed:g.Dispose()
		def ga(h,sx,sy):
			try:
				i=O["spot"];c=r.gtr
				for j in aq["order"]:
					d=aq["kinds"][j]
					if d[0]!="open":continue
					g=r.gumps.get(d[2])
					if g is None:continue
					a=c.get(g)
					if a is None:
						a=g.TextRenderer
						if len(c)>=cD:c.clear()
						c[g]=a
					o=a.DRight
					if o is None:continue
					while o is not None:
						e=o.Owner
						if not o.IsDestroyed and e is not None and o.TextBox is not None:
							try:f=int(e.Serial or 0)
							except Exception:f=0
							b=i.get(f)
							if b is not None:o.X,o.Y=b[0],b[1];k,l=cB(o.TextBox);o.RealScreenPosition=ai.Point(b[0]-(k>>1),b[1]-int(o.OffsetY)-l)
						o=o.DRight
					a.Draw(h,sx,sy,True)
			except Exception as m:O["texts"]=False;r.error="canvas texts: %s"%m
		gb=4.;gc=1.5
		def gd(now):
			if O["texts"]or p["canvas"]is None:return
			a=O["say_lbl"];d=O["said"];f=JR["rd"]
			if d is not None and f is not None:
				j,g=d
				for b in f.new():
					if b.at<g-.05 or ":"in b.text[:24]:continue
					c=O["spot"].get(j);O["said"]=None
					if c is None or O["ctrl"]is None:break
					if a is None:
						h=ap.get("grid")
						if h is None:break
						a=e(h,"",0,0,D);U();d6(a);O["say_lbl"]=a
					i=C(b.text,200);A(a,i);a.SetPos(max(0,c[0]-o(i)//2),max(0,c[1]-18));a.IsVisible=True;O["say_shown"]=True;O["say_until"]=now+gb;break
				else:
					if now-g>gc:O["said"]=None
			if a is not None and O["say_shown"]and now>=O.get("say_until",0.):O["say_shown"]=False;N(a,"IsVisible",False)
		def cS():
			h=r.hold
			if h is None:a=Tz.get(None,"Game",Tz.T("ClassicUO.Client"));h=r.hold=Tz.get(Tz.get(a,"UO"),"GameCursor");h=r.hold=Tz.get(h,"ItemHold")
			return None if not bool(Tz.get(h,"Enabled"))or bool(Tz.get(h,"IsFixedPosition"))else h
		aN={"pct":None}
		def cT():a=aN["pct"];return(a,True)if a is not None and a<p["scale_pct"]else(p["scale_pct"],p["scale_items"])
		def cU():
			if aN["pct"]is None:M(bL,"")
			else:M(bL,"%d|%d"%(p["scale_pct"],1 if p["scale_items"]else 0))
		def cV(pct):
			if pct is not None and not(ai.ok and not r.disabled and aG()):pct=None
			if pct is not None and bE():pct=None
			if pct is not None and aN["pct"]is None:
				a=safe(dG)
				if a:p["scale_pct"],p["scale_items"]=a
			if pct is not None:
				pct=max(df,int(pct))
				if pct>=p["scale_pct"]:pct=None
			if pct==aN["pct"]:return
			c=aN["pct"];b=r.scale;aN["pct"]=pct
			try:b7(*cT())
			except Exception as e:aN["pct"]=c;API.SysMsg(ao+": couldn't change the bag scale (%s)."%e,aA);return
			cU()
			if b>0 and r.scale>0:f=r.scale/b;p["cell_w"]=max(1,min(bd,int(round(p["cell_w"]*f))));p["cell_h"]=max(1,min(bd,int(round(p["cell_h"]*f))))
			p["fit_pending"]=True;bh()
			if not(p["job"]or p["sort"]):aU("Idle")
		def ge():
			c=ac(bL)
			if not c:return
			a=c.split("|")
			try:b,d=int(a[0]),(len(a)>1 and a[1]=="1")
			except Exception:M(bL,"");return
			if ai.ok and 50<=b<=200:
				try:b7(b,d);p["scale_pct"],p["scale_items"]=b,d
				except Exception:return
			M(bL,"")
		def gf(w,h):
			a=(int(w),int(h))if(w is not None and h is not None and aG())else None
			if a is None:
				if aF["area"]is not None:aF["area"]=None;bD(None,None,None);p["dirty_frame"]=True
				return
			if a!=aF["area"]:aF["area"]=a;bD(a[0],a[1],"w");p["dirty_frame"]=True
		def gg(width,height):
			if not(bE()and aG()):return
			c=0 if bG()else cL(max(60,min(int(height),1000)));b=int(width)-c
			if b<40:return
			d=sum(f for g,f,h in dT(dS()));k=(p["scale_pct"]if aN["pct"]is not None else(int(round(r.scale*100))if ai.ok else p["scale_pct"]))/100.;a=max(80,int(math.ceil(d*k*k/b)))
			if int(height)<(1<<19):a=min(a,max(1,int(height)))
			return None,a
		def bG():return p["side_hidden"]and not p["minimized"]and aG()
		def bq():return 0 if(bp()or aG())else a3
		def gh():
			b=p["attach"]
			if b is None:return
			a=b.get("raw")
			if a is None or a.IsDisposed:
				a=bj(b.get("g"))if ai.ok else None;b["raw"]=a
				if a is not None:aa(ap["grid"],b.get("g"))
			return a
		def gi(info):
			if info is None and p["attach"]is not None:
				safe(lambda:cV(None))
				if aF["area"]is not None:aF["area"]=None;bD(None,None,None)
				p["frame_x"],p["frame_y"]=p["saved_fx"],p["saved_fy"];p["detached_at"]=time.time();r.bar_at=None
				for a in(p["bar_raw"],p["grid_raw"]):
					with Kit.quiet:
						if a is not None and not a.IsDisposed:bo(a,p["frame_x"],p["frame_y"])
				for c in("bar","grid"):
					g=ap.get(c)
					if u(g):g.SetPos(p["frame_x"],p["frame_y"]);ad(g)
			elif info is not None:
				p["minimized"]=p["docked"]=False;bR(False)
				with Kit.quiet:
					b=info.get("g")
					if u(b)and(info.get("dx")or info.get("dy")):p["frame_x"]=int(b.GetX())+int(info.get("dx",0));p["frame_y"]=int(b.GetY())+int(info.get("dy",0))
			p["attach"]=info;p["dirty_frame"]=True
		def br():w,h=S(di[0]);return(w or 15),(h or 15)
		def bH(grid,x,y,strip=True):
			if strip:ev(grid,x-4,y+max(0,(br()[1]-bJ)//2))
			if aG():a,b=Kit.ART_DOCK,("Show the side panel"if p["side_hidden"]else "Hide the side panel")
			else:a,b=di,("Show the title bar and side panel"if p["bare"]else "Bags only: hide the title bar and side panel")
			m(grid,ap["store"],"bare",a,x,y,None,b,on_click=ay("toggle_bare"))
		def gj(grid,slot_raws,cols,cw,ch,gap,d,c,trim):
			z=max(4,(cw-8)//7);b=aF["area"]if aG()else None
			if b is not None:a4(P(grid,at,0,0,b[0],b[1],Kit.SECTION_ALPHA))
			for f in range(p["slots"]):
				r,j=divmod(f,cols);x,y=j*(cw+gap),r*(ch+gap);A=a8(x,y,cw,ch,"#000000",.01)
				if bp():N(A,"CanMove",True)
				grid.Add(A);P(grid,at,x,y,cw,ch,p["opacity"])
				if trim:
					if j<cols-1:grid.Add(a4(a8(x+cw-1,y,1,ch,bz,.8)))
					if f+cols<p["slots"]:grid.Add(a4(a8(x,y+ch-1,cw,1,bz,.8)))
				else:
					for s,t,u,v in((x,y,cw,1),(x,y+ch-1,cw,1),(x,y,1,ch),(x+cw-1,y,1,ch)):grid.Add(a4(a8(s,t,u,v,dr,.9)))
				k=[bf(grid,"#%d"%(f+1),x+5,y+3,E)]
				if f in p["assign"]:k.append(bf(grid,bi(a5(p["assign"][f],False),z),x+5,y+21,l));k.append(bf(grid,"Closed",x+5,y+39,l))
				else:k.append(bf(grid,bi("Empty: click Slots",z),x+5,y+21,l))
				slot_raws.append(tuple(bj(G)for G in k)if ai.ok else());B=bf(grid,"",x+5,y+max(0,ch-18),J);N(B,"IsVisible",False);ap["counts"].append((B,x,y,cw,ch))
			if b is not None:
				for f in range(p["slots"],cols*int(math.ceil(p["slots"]/float(cols)))):r,j=divmod(f,cols);a4(P(grid,at,j*(cw+gap),r*(ch+gap),cw,ch,p["opacity"]))
			if trim:
				for s,t,u,v in((0,0,d,1),(0,c-1,d,1),(0,0,1,c),(d-1,0,1,c)):grid.Add(a4(a8(s,t,u,v,dr,.9)))
			if bp():g,h=S(al);g,h=(g or 30),(h or 30);m,n=br();o,w=d-g+dj,c-h+dj;a4(Y(grid,al,o,w));Q(grid,o,w,g,h,lambda*a:None,"Drag to move the bags",movable=True);bH(grid,o-m-3,c+b0);e=o+g;i=max(w+h,c+b0+n);grid.SetRect(p["frame_x"],p["frame_y"],e,i);p["grid_wh"]=(e,i);return e
			if bG():
				m,n=br()
				if b is not None:bH(grid,b[0]-m-2,b[1]-n-2);grid.SetRect(p["frame_x"],p["frame_y"],b[0],b[1]);p["grid_wh"]=b;return b[0]
				bH(grid,d-m,c+b0);i=c+b0+n;grid.SetRect(p["frame_x"],p["frame_y"],d,i);p["grid_wh"]=(d,i);return d
			C,q=cK(grid,d+gap,c);p["side_pw"]=gap+C;e=d+gap+C
			if b is not None:e,q=max(e,b[0]),max(q,b[1])
			grid.SetRect(p["frame_x"],p["frame_y"]+bq(),e,max(c,q));p["grid_wh"]=(e,max(c,q));return e
		bQ={"outline":None,"told":False}
		def cW(g):
			try:
				if g is None or g.IsDisposed:return
				x,y=int(g.GetX()),int(g.GetY());w,h=int(g.GetWidth()or 0),int(g.GetHeight()or 0)
			except Exception:return
			return None if w<=1 or h<=1 else(x,y,w,h)
		def gk():
			if p["minimized"]or p["docked"]:return
			a=[]
			if not bp()and not aG()and p["canvas"]!="alone":
				r=cW(ap["bar"])
				if r is not None:a.append(r)
			r=cW(ap["grid"])
			if r is not None:a.append(r)
			if not a:return
			b=min(f[0]for f in a);c=min(g[1]for g in a);d=max(h[0]+h[2]for h in a);e=max(i[1]+i[3]for i in a);return b,c,d-b,e-c
		def gl():
			b=[];c,d=ap["bar"],ap["grid"]
			for g,a in list(SNAP.links.items()):
				if(a is c or a is d)and a is not None and u(g):
					r=cW(g)
					if r is not None:b.append((g,r))
			return b
		def eb(a,d,b,c,e,f):return f+(a-c)if a>=c-2 or(d>b+2 and abs(d-c)<abs(a-b))else e+(a-b)
		def ec(followers):
			c=SNAP;d=ap["grid"]if(bp()or aG()or p["canvas"]=="alone")else ap["bar"]
			if d is None:d=ap["grid"]
			U();b=gk();a=bQ["outline"]
			if a is not None:a=(p["frame_x"]+a[0],p["frame_y"]+a[1],a[2],a[3])
			if b is not None:bQ["outline"]=(b[0]-p["frame_x"],b[1]-p["frame_y"],b[2],b[3])
			j=0
			for g,(e,f,l,m)in followers:
				if d is None or not u(g):continue
				c.links[g]=d
				if a is None or b is None or a==b:continue
				h=eb(e,e+l,a[0],a[0]+a[2],b[0],b[0]+b[2]);i=eb(f,f+m,a[1],a[1]+a[3],b[1],b[1]+b[3])
				if(h,i)==(e,f):continue
				try:g.SetPos(int(h),int(i))
				except Exception:continue
				j+=1
				with Kit.quiet:
					if c.last is not None:c.last[g]=(h,i)
					ad(g);c.follow(g,h-e,i-f,set([g]))
				k=c.moved_cb.get(g)
				if k is not None:safe(k)
			if j and not bQ["told"]:bQ["told"]=True;API.SysMsg(ao+": %s moved with the bags' edge."%F(j,"snapped window"),aK)
		def gm(cols,rows,ch,gap):
			a=aD()[1]
			if a<=0 or p["slots"]<=1:return cols,rows
			b=max(1,(a-bq()-eU+gap)//(ch+gap))
			if rows<=b:return cols,rows
			c=int(math.ceil(p["slots"]/float(b)));return c,int(math.ceil(p["slots"]/float(c)))
		def gn():
			m=gl();d4();bA("grid");bA("bar")
			if p["canvas"]is not None and dO()==p["canvas"]:go(m);return
			if aF["area"]is not None and aG()and p["geom"]is not None:bD(aF["area"][0],aF["area"][1],"w");p["dirty_frame"]=False
			elif aF["told"]is not None and not aG()and p["geom"]is not None:bD(aF["told"][0],aF["told"][1],"w");p["dirty_frame"]=False
			c,e=dN();n=b8();d=0 if n else co;h,f=aF["cell"]or(p["cell_w"],p["cell_h"]);i=not aG()and p["canvas"]is None and aF["told"]is None and not aj(aJ)
			if i and not p["minimized"]:c,e=gm(c,e,f,d)
			s=c*h+(c-1)*d;o=e*f+(e-1)*d;p["geom"]=(c,h,f,d);p["icons_used"]=r.icons or bw;ap.update({"store":({},{}),"side_status":None,"search_box":None,"counts":[],"count_state":{}});b=bp();a=G.CreateGump(b,b);ap["grid_bare"]=b;p["grid_info"]=(bj(a)if ai.ok else None,b);q=[]
			if p["minimized"]:g=cq;a.SetRect(p["frame_x"],p["frame_y"]+a3,1,1)
			else:g=gj(a,q,c,h,f,d,s,o,n)
			if i:
				t=g if b else max(g,cq);u=a3 if p["minimized"]else bq()+(p["grid_wh"][1]if p["grid_wh"]else o);j,k=Kit.clamp(p["frame_x"],p["frame_y"],t,u)
				if(j,k)!=(p["frame_x"],p["frame_y"]):p["frame_x"],p["frame_y"]=j,k;a.SetPos(j,k+(a3 if p["minimized"]else bq()))
			dy(a,True);dz(a);G.AddGump(a);ap["grid"]=a;l=eg(g,p["docked"]or b or aG(),i)
			if aG():p["attach_g"]=p["attach"].get("g");aa(a,p["attach_g"])
			elif b:aa(l,a)
			else:aa(a,l)
			ec(m);p["slot_raws"]=tuple(q)
			if SR["counts"]:ci()
			p["grid_raw"]=bj(a)if ai.ok else None;p["bar_raw"]=bj(l)if ai.ok else None
			if ai.ok and not r.disabled and(p["grid_raw"]is None or p["bar_raw"]is None):r.error="can't reach the client's own window controls";r.disabled=True
		ed="Close "+ao+" (turns it off; gives every bag back)";ee="Open the bag manager: a bag per slot";ef="Pick the bags Trap and Untrap cast on"
		def eg(f,hide,free=False):
			b=max(f,cq);a=G.CreateGump(True,True)
			if free:an(a,p["frame_x"],p["frame_y"],b,a3)
			else:a.SetRect(p["frame_x"],p["frame_y"],b,a3)
			Z(a,b,a3,corners=False);z(a,8,8,b-16,a3-16);e(a,ao.upper(),18,14,E);e(a,str(p["slots"]),18+o(ao.upper())+8,14,l);c=ap["store"];x=b-12-30
			if ag(aJ):x+=20
			else:m(a,c,"close",H,x,11,None,ed,on_click=ay("disable",aJ));x-=20;m(a,c,"min",aS if p["minimized"]else aR,x,14,None,aV if p["minimized"]else aT,on_click=ay("user_collapse"));Kit.dock_button(a,c,x,14,on_click=ay("fold_to_bar"));x-=Kit.DOCK_DX
			for g,d,h,i in(("settings","Settings",Kit.SETTINGS_TIP%ao,ay("show_settings",aJ)),("traps","Trap bags",ef,ay("open_win","trp")),("bags","Slots",ee,ay("open_win","mgr"))):x-=10+35+o(d);m(a,c,g,I,x,11,d,h,on_click=i)
			a7(a,8,8,max(20,x-14),a3-16,ay("user_collapse"),key=aJ)
			if hide:a.IsVisible=False
			G.AddGump(a);ap["bar"]=a;return a
		hO=None
		def eh():
			if p["canvas"]is None or O["ctrl"]is None or aq["size"]is None:return
			if O["built"]!=aq["ver"]or O["bsize"]!=aq["size"]:
				if O["rect"]is not None and(O["rect"][2],O["rect"][3])!=aq["size"]:return
				if bP():return
				fS()
			d5();f_()
		def go(followers):
			i=p["canvas"];b=i=="alone";p["icons_used"]=r.icons or bw;ap.update({"store":({},{}),"side_status":None,"search_box":None});e,f,c,g,o=dQ(i);W,d=aF["told"]if b else aF["area"];a=G.CreateGump(b,b);ap["grid_bare"]=b;h=bj(a);p["grid_info"]=(h,b);j=ap["store"];k=b and not p["bare"]and cM(W)
			if b:
				Z(a,W,d)
				if k:
					a6(a,j,W,ao,aJ,ay("user_collapse"),ay("fold_to_bar"),ay("show_settings",aJ),close_tip=ed,extra=[("traps",I,"Trap bags",ef,ay("open_win","trp")),("bags",I,"Slots",ee,ay("open_win","mgr"))],after=str(p["slots"]));l=j[0].get("close")
					if l is not None:ax(l,ay("disable",aJ))
			U();fR(h,h.Children.Count,e,f,c,g);m,n=br()
			if b:
				p["side_pw"]=0
				if p["bare"]and cM(W):bH(a,e+c-m-2,f+g-n-2)
				elif k and o:p["side_pw"]=cK(a,e+c,g,f)[0]
				else:ev(a,e+c-2,f+g-bJ-2)
			elif bG():bH(a,W-m-2,d-n-2);p["side_pw"]=0
			else:p["side_pw"]=cK(a,c,d)[0]
			a.SetRect(p["frame_x"],p["frame_y"],W,d);p["grid_wh"]=(W,d);dy(a,False)
			if not b:dz(a)
			if aj(aJ):a.CanMove=False
			G.AddGump(a);ap["grid"]=a;q=eg(W,True)
			if aG():p["attach_g"]=p["attach"].get("g");aa(a,p["attach_g"])
			ec(followers);p["slot_raws"]=();p["grid_raw"]=h;p["bar_raw"]=bj(q)if ai.ok else None
			if p["grid_raw"]is None:r.error="can't reach the client's own window controls";r.disabled=True;return
			eh()
		def gp():p["minimized"]=not p["minimized"];p["docked"]=False;bh()
		def cX():return aL(dt)
		def bR(on):HOST.dock_want_set(dt,on)
		def gq():
			if ag(aJ):return
			bR(False);gp()
		def ei():
			if ag(aJ):return
			bR(True);a=az()
			if not p["minimized"]or p["docked"]!=a:p["minimized"],p["docked"]=True,a;bh()
			if not a:HOST.dock_note(ao)
		def gs():
			if aG():p["side_hidden"]=not p["side_hidden"]
			else:p["bare"]=not p["bare"]
			bh()
		bs={"next":0.}
		def ej():
			a=time.time()
			if a<bs["next"]:return
			bs["next"]=a+.1;b=API.GetSharedVar(cx)
			if b:
				API.RemoveSharedVar(cx);b=str(b)
				if aG():
					d=p["attach"].get("cmd")
					if d is not None:safe(lambda:d(b))
				elif b=="show"and(p["minimized"]or p["docked"]):bR(False);p["minimized"]=p["docked"]=False;bh()
				elif b=="dock"and not p["docked"]:ei()
			if aG():c=str(p["attach"].get("state")or "open")
			else:
				if p["docked"]:
					if not az():p["docked"]=False;p["dirty_frame"]=True
				elif p["minimized"]and a>=bs.get("wish",0.):
					bs["wish"]=a+.25
					if cX()and az():p["docked"]=True;p["dirty_frame"]=True
				elif not p["minimized"]and a>=bs.get("wish",0.):
					bs["wish"]=a+1.
					if cX():bR(False)
				c="docked"if p["docked"]else("collapsed"if p["minimized"]else "open")
			if c!=p["link_state"]:p["link_state"]=c;API.SetSharedVar(ds,c)
		def gt(value):
			if not ai.ok:API.SysMsg(ao+": minimizing bags needs client access (%s)."%ai.error,aA);return
			n=fy(value)or 0;API.SysMsg(ao+": %s %s."%("minimized"if value else "restored",F(n,"bag")),aK)
		def gu():
			gv();a=False;b=p["minimized"]or(aG()and not p["attach"].get("shown",True))
			for f,i in p["layout"]:
				try:
					c=API.FindItem(i);g=c.GetContainerGump()if c else None
					if not u(g):continue
					try:g.IsVisible=not b
					except Exception:pass
					if b:continue
					d,e=dC(f)
					if g.GetX()!=d or g.GetY()!=e:g.SetPos(d,e)
					w=g.GetWidth()or 0;h=g.GetHeight()or 0
				except Exception:continue
				if p["cell_w"]<w<=bd:p["cell_w"],a=w,True
				if p["cell_h"]<h<=bd:p["cell_h"],a=h,True
			if a:bh()
		def ek():
			a=p["attach"].get("g")if aG()else None
			if a is not None and a is not p["attach_g"]and u(a)and u(ap.get("grid")):p["attach_g"]=a;aa(ap["grid"],a)
		def gv():
			if aG():
				b,d=p["attach"].get("g"),p["attach"]
				if not u(b):return
				ek();x=b.GetX()+d.get("dx",0);y=b.GetY()+d.get("dy",0);a=ap.get("grid")
				if(x,y)!=(p["frame_x"],p["frame_y"]):
					p["frame_x"],p["frame_y"]=x,y
					if u(a):a.SetPos(x,y);ad(a)
				elif u(a)and(int(a.GetX()),int(a.GetY()))!=(x,y):a.SetPos(x,y);ad(a)
				return
			b,c,e=(ap["grid"],ap["bar"],0)if ap.get("grid_bare")else(ap["bar"],ap["grid"],a3)
			if not u(b):return
			x=b.GetX();y=b.GetY()
			if x!=p["frame_x"]or y!=p["frame_y"]:
				p["frame_x"],p["frame_y"]=x,y
				if u(c):c.SetPos(x,y+e);ad(c)
		def cY(k):p["open_"+k]=True;p["dirty_"+k]=True;bg()
		ce={"trp":"trap_checks","srt":"rule_checks"}
		def el(k):
			if k=="trp":bt()
			elif k=="srt":bl()
		def gw(k):
			el(k);cm(k)
			if k in ce:ap[ce[k]]=[]
			p["open_"+k]=False;bg()
		def gx(k):el(k);p[k+"_min"]=not p[k+"_min"];p["dirty_"+k]=True;bg()
		def cZ():cn();bg()
		def gy():
			cm("mgr");M,h=K,B;w,k,i=480,28,40;j=min(p["slots"]*k+8,430);o=M+30+M if p["mgr_min"]else M+30+h+i+h+j+M;g,d,y=b3("mgr",w,o,"BAG MANAGER",ay("toggle_win_min","mgr"),ay("close_win","mgr"))
			if not p["mgr_min"]:
				f=w-2*M;z(g,M,y,f,i);m(g,d,"fill",X,M+12,y+9,"Auto-fill","Put each open bag without a slot in an empty slot",on_click=ay("auto_fill"));m(g,d,"clear",H,M+200,y+9,"Clear all","Empty every slot",on_click=ay("clear_all"));y+=i+h;z(g,M,y,f,j);b=G.CreateGumpScrollArea(M+4,y+4,f-8,j-8);n=f-8-20
				for a in range(p["slots"]):
					c=a*k;e(b,"#%d"%(a+1),6,c+5,E)
					if a in p["assign"]:e(b,bi(a5(p["assign"][a]),28),44,c+5)
					else:e(b,"No bag yet: click Set...",44,c+5,l)
					m(b,d,"set%d"%a,L,n-165,c+3,"Set...","Target a bag for slot #%d"%(a+1),on_click=ay("assign_slot",a));m(b,d,"clr%d"%a,H,n-80,c+3,"Clear","Empty slot #%d"%(a+1),on_click=ay("clear_slot",a))
				g.Add(b)
			b4("mgr",g,cZ)
		def bS():dx();p["dirty_frame"]=True;p["dirty_mgr"]=True;p["dirty_trp"]=True;p["dirty_srt"]=True;cH();a9()
		def bT(kind,*a):
			def b(serial):dw.add((kind,)+a+(int(serial or 0),),dup=True)
			aO(15,b)
		def gz(idx):API.SysMsg(ao+": target a bag for slot #%d."%(idx+1),aK);bT("assign_slot_to",idx)
		def gA(idx,target):
			if not target:API.SysMsg(ao+": cancelled.",aK);return
			b=T(target)
			if not b or not b.IsContainer:API.SysMsg(ao+": that isn't a container.",aA);return
			a=int(target)
			for k in[c for c,d in p["assign"].items()if d==a]:del p["assign"][k]
			p["assign"][idx]=a;bS()
			if dH(a):API.SysMsg(ao+": slot #%d set."%(idx+1),be)
			else:API.SysMsg(ao+": slot #%d set; open the bag to snap it in."%(idx+1),be)
		def gB(idx):
			if idx in p["assign"]:del p["assign"][idx];bS()
		def gC():p["assign"]={};bS();API.SysMsg(ao+": all slots cleared.",aK)
		def gD():
			b=[]
			for c in(safe(lambda:int(API.Backpack),0),safe(lambda:int(API.Bank),0)):
				if not c:continue
				b.append(c)
				for f in API.ItemsInContainer(c,True)or[]:
					if f.IsContainer:b.append(int(f.Serial))
			g=set(p["assign"].values());d=[h for h in range(p["slots"])if h not in p["assign"]];e=0
			for a in b:
				if not d:break
				if a in g or not dH(a):continue
				p["assign"][d.pop(0)]=a;g.add(a);e+=1
			bS()
			if e:API.SysMsg(ao+": added %s."%F(e,"open bag"),be)
			elif not d:API.SysMsg(ao+": no empty slots left.",aA)
			else:API.SysMsg(ao+": no open bag without a slot found.",aK)
		aZ={"c":None,"store":({},{}),"next_status":0.}
		def em():
			if p["canvas"]is not None:return "In a zone the bags share it. Items always draw solid."
			return "Slots fit the open bags (%d x %d px). Items always draw solid."%(p["cell_w"],p["cell_h"])
		def gE(w):return Kit.Form.height(db(w),w)
		def gF(g,x,y,w):
			if ai.ok and aN["pct"]is None:
				a=safe(dG)
				if a:p["scale_pct"],p["scale_items"]=a
			f=Kit.Form(g,x,y,w,{"slots":p["slots"],"cols":p["cols"],"rows":p["rows"],"scale":p["scale_pct"],"opacity":int(round(p["opacity"]*100)),"trim":p["trim"],"items":p["scale_items"]},db(w));aZ.update({"c":f.c,"store":f.store,"next_status":0.,"seen":{"trim":p["trim"],"items":p["scale_items"]}})
		def en():aZ["c"]=None
		def gG():
			c=aZ["c"]
			if c is None:return
			if ae(aZ["store"],"apply"):gJ();return
			for d,g in(("trim",gH),("items",gI)):
				try:a=bool(c[d].IsChecked)
				except Exception:a=None
				if a is not None and a!=aZ["seen"][d]:aZ["seen"][d]=a;g(a)
			try:v=int(c["opacity"].Value)
			except Exception:v=None
			if v is not None and 10<=v<=100:
				if aZ.get("pct_v")!=(v,c["opacity_lbl"]):aZ["pct_v"]=(v,c["opacity_lbl"]);A(c["opacity_lbl"],"%d%%"%v)
				b=v/100.
				if abs(b-p["opacity"])>.001:
					e=p["opacity_pending"];p["opacity_pending"]=(b,e[1]+1)if e and e[0]==b else(b,0)
					if p["opacity_pending"][1]>=e2:p["opacity"]=b;p["opacity_pending"]=None;p["dirty_frame"]=True;d5();bg()
				else:p["opacity_pending"]=None
			f=time.time()
			if f>=aZ["next_status"]:aZ["next_status"]=f+1.;A(c["status"],bi(c_(),64));A(c["size"],em())
		def c_():
			if not ai.tried:return "Off: tick "+ao+" on the Modules tab"
			if not ai.ok:return "No client access: "+ai.error
			if r.disabled:return "Trimming stopped after errors: "+r.error
			if p["canvas"]is not None:a="%d open, filling the zone"%r.open_count
			else:a="%d open, %d trimmed"%(r.open_count,len(r.trimmed))
			if p["driving"]:return "Running (script-driven): "+a
			return "Starting"if r.hook_calls==0 else "Running: "+a
		def gH(value):
			f=aZ["c"]
			if value and not(ai.ok and not r.disabled):
				API.SysMsg(ao+": trimming isn't available (%s)."%c_(),aA)
				if f:safe(lambda:f["trim"].SetIsChecked(False));aZ["seen"]["trim"]=False
				value=False
			if value==p["trim"]:return
			p["trim"]=value;cI();a9();API.SysMsg(ao+": trim "+("on."if value else "off."),aK)
		def gI(value):
			if value==p["scale_items"]:return
			if not ai.ok:API.SysMsg(ao+": scaling items needs client access (%s)."%ai.error,aA);return
			try:
				a=p["scale_items"];p["scale_items"]=value
				try:b7(*cT())
				except Exception:p["scale_items"]=a;raise
				if aN["pct"]is not None:cU()
				cI();API.SysMsg(ao+": items %s with the bags."%("scale"if value else "don't scale"),aK)
			except Exception as e:API.SysMsg(ao+": couldn't change the item scaling (%s)."%e,aA)
		def cf(field,name,lo,hi):
			a=(safe(lambda:field.Text,"")or "").strip()
			if not a.isdigit()or not(lo<=int(a)<=hi):raise ValueError("%s must be a whole number from %d to %d."%(name,lo,hi))
			return int(a)
		def gJ():
			f=aZ["c"]
			if not f:return
			try:a=cf(f["slots"],"Slots",bX,a_);b=cf(f["cols"],"Columns",0,a_);c=cf(f["rows"],"Rows",0,a_);d=cf(f["scale"],"Bag scale",50,200)
			except ValueError as e:API.SysMsg(ao+": "+str(e),aA);return
			if b>0 and c>0 and b*c<a:API.SysMsg(ao+": %d columns x %d rows only fits %d slots, not %d."%(b,c,b*c,a),aA);return
			g=[n for n in p["assign"]if n>=a]
			for k in g:del p["assign"][k]
			bl()
			for k in[q for q in p["rules"]if q>=a]:del p["rules"][k]
			p["slots"],p["cols"],p["rows"]=a,b,c
			if ai.ok and d!=p["scale_pct"]:
				try:
					i=p["scale_pct"];p["scale_pct"]=d
					try:b7(*cT())
					except Exception:p["scale_pct"]=i;raise
					if aN["pct"]is not None:
						if aN["pct"]>=d:aN["pct"]=None
						cU()
					cI()
				except Exception as e:API.SysMsg(ao+": couldn't change the bag scale (%s)."%e,aA)
			bS();j,r=dN();h=ao+": %s in %d x %d."%(F(a,"slot"),j,r)
			if g:h+=" Released %s from removed slots."%F(len(g),"bag")
			API.SysMsg(h,be);en();af(aJ)
		def c0():
			a=[]
			for s in[p["assign"][b]for b in sorted(p["assign"])]+p["trap_extra"]:
				if s not in a:a.append(s)
			return a
		def bt():
			a=ap["trap_checks"]
			if not a or not u(ap["trp"]):return
			for b,c in a:
				if safe(lambda:c.IsChecked,False):p["trap_sel"].add(b)
				else:p["trap_sel"].discard(b)
		def gK():
			bt();cm("trp");h=c0();M,b=K,B;w,j,i,k=480,28,40,52;d=min(max(1,len(h))*j+8,400);s=(M+30+M if p["trp_min"]else M+30+b+i+b+d+b+k+M);g,n,y=b3("trp",w,s,"TRAP BAGS",ay("toggle_win_min","trp"),ay("close_win","trp"));o=[]
			if not p["trp_min"]:
				c=w-2*M;z(g,M,y,c,i);Kit.buttons(g,n,M+12,y+9,(("all",X,"Tick all","Tick every bag",ay("select_all_traps",True)),("none",H,"Untick all","Untick every bag",ay("select_all_traps",False)),("add",L,"Add bag...","Target a bag without a slot to add it",ay("add_trap_bag"))),16);y+=i+b;z(g,M,y,c,d);f=G.CreateGumpScrollArea(M+4,y+4,c-8,d-8);t=c-8-20
				if not h:e(f,"No bags yet. Fill the slots, or click Add bag...",6,6,l)
				for q,a in enumerate(h):
					r=q*j;u=au(f,bi(a5(a),32),6,r+4,a in p["trap_sel"],"Ticked: Trap and Untrap cast on this bag");o.append((a,u))
					if a in p["trap_extra"]and a not in p["assign"].values():m(f,n,"rm%d"%q,H,t-110,r+3,"Remove","Take this bag off",on_click=ay("remove_trap_bag",a))
				g.Add(f);y+=d+b;z(g,M,y,c,k);e(g,"Tick bags, then Trap or Untrap on the side panel.",M+12,y+8,l);e(g,"A trapped bag explodes on whoever opens it, you included.",M+12,y+28,v)
			b4("trp",g,cZ,trap_checks=o)
		def c1():ap["trap_checks"]=[];p["dirty_trp"]=True;a9()
		def gL(value):p["trap_sel"]=set(c0())if value else set();c1()
		def gM():bt();API.SysMsg(ao+": target a bag to add to the trap list.",aK);bT("add_trap_bag_to")
		def gN(target):
			if not target:return
			bt();b=T(target)
			if not b or not b.IsContainer:API.SysMsg(ao+": that isn't a container.",aA);return
			a=int(target)
			if a not in p["trap_extra"]:p["trap_extra"].append(a)
			p["trap_sel"].add(a);c1()
		def gO(serial):
			bt()
			if serial in p["trap_extra"]:p["trap_extra"].remove(serial)
			p["trap_sel"].discard(serial);c1()
		def gP(spell):
			bt();a9()
			if p["job"]:API.SysMsg(ao+": already casting %s; press Stop first."%p["job"]["spell"],aA);return
			if p["sort"]:API.SysMsg(ao+": busy sorting; press Stop first.",aA);return
			a=[b for b in c0()if b in p["trap_sel"]]
			if not a:API.SysMsg(ao+": tick bags in the Trap bags window first.",aA);cY("trp");return
			p["job"]={"spell":spell,"queue":a,"i":0,"phase":"mana","t":0.,"tries":0,"done":0,"failed":0,"warned":False,"cast":0.};p["dirty_trp"]=True;aU("Starting");API.SysMsg(ao+": casting %s on %s."%(spell,F(len(a),"bag")),aK)
		def bU(user=False):
			if p["job"]:
				a=p["job"]
				if a.get("phase")=="target"and time.time()-a.get("cast",0.)>=dn and aI(aJ,"neutral"):API.CancelTarget()
				ar(aJ)
				if user:API.SysMsg(ao+": %s stopped."%p["job"]["spell"],aK);aU("Stopped")
			p["job"]=None;p["dirty_trp"]=True
		def eo():
			b=bool(p["job"]or p["sort"])
			for a in ap.get("stop_ctrls")or():
				if a is not None:N(a,"IsVisible",b)
		def aU(text):
			if text=="Idle":a=aN["pct"];text=("Shown at %d%% to fit"%a)if a is not None and a<p["scale_pct"]else ""
			eo()
			if text==p["status_text"]:return
			p["status_text"]=text;b=ap.get("side_status")
			if b is not None:A(b,text)
		gQ=tuple((hR,tuple(hT.lower()for hT in hS))for hR,hS in(("reagents",fa),("mana",fb),("fizzle",e8),("busy",e9)))
		def ep(j):
			c=j.get("jr")
			if c is None:return
			a=j["jt"]
			for b in c.new():
				if b.text and not b.text.startswith(ao):a.append(b.low)
			if not a:return
			for d,e in gQ:
				if any(f in g for f in e for g in a):return d
			return
		def c2(j,a):
			if a:j["done"]+=1
			else:j["failed"]+=1
			j["i"]+=1;j["tries"]=0;j["phase"]="mana"
		def c3(j,now,a):
			j["tries"]+=1
			if j["tries"]>e7:API.SysMsg(ao+": giving up on %s (%s)."%(a5(j["queue"][j["i"]],False),a),aA);c2(j,False)
			else:j["phase"]="pause";j["t"]=now+e6
		def gR():
			j=p["job"]
			if not j:return
			a=time.time()
			if j["i"]>=len(j["queue"]):API.SysMsg(ao+": %s finished: %d done, %d failed."%(j["spell"],j["done"],j["failed"]),be if not j["failed"]else aA);aU("Done %d/%d"%(j["done"],len(j["queue"])));bU();return
			d=j["queue"][j["i"]];e=j["phase"]
			if e=="pause":
				if a>=j["t"]:j["phase"]="mana"
				return
			if e=="mana":
				c=HOST.fight_hold(a)or HOST.guard_hold()
				if c:
					if j.get("held")!=c:j["held"]=c;f=HOLD_TEXT.get(c,c);API.SysMsg(ao+": %s waits (%s)."%(j["spell"],f[:1].lower()+f[1:]),aK);aU(f if c=="unknown"else "Paused: "+f)
					return
				if j.get("held"):j["held"]=None;aU("Starting")
				g=API.Player.Mana
				if g<dl:
					if not j["warned"]:API.SysMsg(ao+": waiting for mana (%d/%d)."%(g,dl),aK);aU("Need mana");j["warned"]=True
					return
				j["warned"]=False
				if not T(d):API.SysMsg(ao+": bag 0x%08X is out of reach; skipping it."%d,aA);c2(j,False);return
				if cF():aU("Cursor busy");return
				if API.HasTarget("any"):aU("Cursor busy");return
				API.SysMsg(ao+": %s %d/%d: %s."%(j["spell"],j["i"]+1,len(j["queue"]),a5(d,False)),aK);aU("%s %d/%d"%("Untrap"if "Untrap"in j["spell"]else "Trap",j["i"]+1,len(j["queue"])));j["cast"]=time.time();j["jr"],j["jt"]=aQ(),[];HOST.claim_cursor(aJ,dm+.5);API.CastSpell(j["spell"]);j["phase"]="target";j["t"]=a;return
			if e=="target":
				b=ep(j)
				if b:ar(aJ)
				if b=="reagents":API.SysMsg(ao+": out of reagents for %s."%j["spell"],aA);bU();return
				if b=="mana":j["phase"]="mana";return
				if b in("fizzle","busy"):c3(j,a,b);return
				if a-j["cast"]>=dn and aI(aJ,"neutral"):API.Target(d);ar(aJ);j["phase"]="recover";j["t"]=a
				elif a-j["t"]>dm:ar(aJ);c3(j,a,"no target cursor")
				return
			if e=="recover":
				if a-j["t"]<e5:return
				b=ep(j)
				if b=="reagents":API.SysMsg(ao+": out of reagents for %s."%j["spell"],aA);bU()
				elif b in("fizzle","busy","mana"):c3(j,a,b)
				else:c2(j,True)
		def c4(it,hue):
			try:it.SetHue(int(hue)&65535);return True
			except Exception:return False
		def c5(it):
			try:return int(it.Hue or 0)
			except Exception:return-1
		SR={"text":"","typed":0.,"armed":False,"lit":{},"until":0.,"counts":{},"restored":{},"tiles":{},"status":None,"texts":{},"texts_at":0.,"objs":{}}
		def gS(q):
			a=[]
			for b in(q or "").lower().split(","):
				p=b.strip()
				if not p:continue
				g=None
				try:
					if p.startswith("0x")and len(p)>2:g=int(p,16)
					elif p.isdigit():g=int(p)
				except ValueError:g=None
				a.append((p,g))
			return a
		def gT(raw):
			if "%"not in raw:return raw
			a,b=[],[]
			for i,p in enumerate(raw.split("%")):
				if i%2==0:a.append(p);b.append(p)
				else:c,e,d=p.partition("/");a.append(d);b.append(c)
			return "".join(a)+" "+"".join(b)
		def c6(it,graphic):
			a=SR["tiles"];t=a.get(graphic)
			if t is None:
				d=it.GetItemData();b=str(d.Name or "")if d is not None else "";t=gT(b).lower()
				if len(a)>=ff:a.clear()
				a[graphic]=t
			return t
		def gU(it,serial,graphic):
			a=SR["texts"];t=a.get(serial)
			if t is not None:return t+"\n"+c6(it,graphic)
			t=API.ItemNameAndProps(serial)or ""
			if t:
				t=str(t).lower()
				if "\n"in t and len(a)<cu:a[serial]=t
				return t+"\n"+c6(it,graphic)
			return str(it.Name or "").lower()+"\n"+c6(it,graphic)
		def gV(x):
			m=set(G for W,G in p["layout"]);d,o={},{};q={};g=0
			for h,e in p["layout"]:
				if g>=cu:break
				r=API.ItemsInContainer(e,True)or[];i={};f=[]
				for b in r:
					try:s=int(b.Serial)
					except Exception:f.append(None);continue
					f.append(s)
					try:i[s]=int(b.Container)
					except Exception:pass
				n=0
				for t in range(len(f)):
					if g>=cu:break
					g+=1;a=f[t]
					if a is None or a in m:continue
					j,c,u=a,i.get(a,e),0
					while c!=e and u<fe and c not in m:j,c=c,i.get(c,e);u+=1
					if c!=e:continue
					b=r[t]
					try:v=int(b.Graphic)
					except Exception:continue
					k=None;l=False
					for y,w in x:
						if w is not None:
							if v==w:l=True;break
						else:
							if k is None:k=gU(b,a,v)
							if y in k:l=True;break
					if not l:continue
					n+=1
					if len(d)<cv:
						d[a]=h;q[a]=b
						if j!=a and len(d)<cv:d[j]=h
				if n:o[h]=n
			SR["objs"]=q;return d,o
		def eq(serial):a=SR["objs"].get(serial);return a if a is not None else API.FindItem(serial)
		def gW(serial,now):
			a=eq(serial)
			if not a:return False
			b=c5(a)
			if b<0:return False
			d=b
			if b==bm:
				c=SR["restored"].get(serial)
				if c is not None and now-c[1]<do:d=c[0]
			if not c4(a,bm):return False
			cQ(serial,bm);SR["lit"][serial]=d;return True
		def er(serial,orig,now):
			a=API.FindItem(serial)
			if not a:return
			b=c5(a)
			if b==bm or b==orig:
				if c4(a,orig):cQ(serial,orig)
				SR["restored"][serial]=(orig,now)
		def gX(now):
			a=SR["restored"]
			if a:
				for s in[b for b,c in a.items()if now-c[1]>=do]:del a[s]
				if len(a)>2*cv:a.clear()
		def gY(q,now):
			c=gS(q)
			if not c:cg(now);return
			gX(now)
			if not 0<=now-SR["texts_at"]<=ct:SR["texts"]={};SR["texts_at"]=now
			d,e=gV(c);b=SR["lit"]
			for a in[h for h in b if h not in d]:er(a,b.pop(a),now)
			try:
				for a in d:
					if a not in b:gW(a,now)
					else:gZ(a)
			finally:SR["objs"]={}
			SR["counts"]=e;SR["until"]=now+ct;ci();f=sum(e.values());g=("%d found"%f)if f else "None found";SR["status"]=g;aU(g)
		def gZ(serial):
			a=eq(serial)
			if not a:return
			b=c5(a)
			if 0<=b!=bm and c4(a,bm):cQ(serial,bm);SR["lit"][serial]=b
		def cg(now):
			a=SR["lit"]
			for b in list(a):er(b,a.pop(b),now)
			SR["texts"]={};SR["texts_at"]=0.;SR["until"]=0.
			if SR["counts"]:SR["counts"]={};ci()
			if SR["status"]is not None:
				if p["status_text"]==SR["status"]:aU("Idle")
				SR["status"]=None
		def ci():
			e=SR["counts"];d=ap["count_state"]
			for b,(c,x,y,f,g)in enumerate(ap["counts"]):
				n=e.get(b,0);a=("%d found"%n)if n else ""
				if d.get(b)==a:continue
				d[b]=a
				try:
					if n:c.SetPos(x+max(5,f-5-o(a)),y+max(0,g-18));A(c,a)
					c.IsVisible=bool(n)
				except Exception:pass
		def g_(now):
			b=ap["search_box"]
			if b is not None and not(p["minimized"]or p["docked"]):
				try:a=b.Text
				except Exception:a=None
				if a is not None:
					a=str(a)
					if a!=SR["text"]:SR["text"],SR["typed"],SR["armed"]=a,now,True
			if SR["armed"]:
				if now-SR["typed"]>=fc:
					SR["armed"]=False;q=SR["text"].strip()
					if len(q)>=fd:gY(q,now)
					elif SR["lit"]or SR["counts"]:cg(now)
			elif SR["until"]and now>=SR["until"]:cg(now)
		def g0(grid,a,y):b=o("Find:")+6;bf(grid,"Find:",a+2,y+3,D);c=av(grid,SR["text"],a+2+b,y,bY-4-b,numbers=False);c.SetTooltip("Item name part or graphic (0x0F7A, 3962); commas for several. Matches light up for %d s"%int(ct));ap["search_box"]=c;m(grid,ap["store"],"rules",I,a,y+28,"Rules","Open Sort rules: what each slot's bag holds",on_click=ay("open_win","srt"));m(grid,ap["store"],"filters",I,a,y+52,"Filters","Open Sort filters: items or presets and their bags",on_click=ay("open_filters"))
		es="Sort items into their bags once; picking up or Stop ends it";bV=(("q_restock","Restock",L,3702,"restock","Top up supplies once from the Restock chest or bank","restock.run"),("q_sort","Sort",L,3705,None,es,None),("q_storage","Storage",I,3648,"storage","Open or raise the Storage window","storage.show"),("q_supplies","Supplies",I,3962,"supplies","Open or raise the Supplies table","supplies.open"))
		def bI(part):return part is None or HOST.part_on(part,"inventory")
		def et(part,tip):
			if bI(part):return tip
			return("%s is off: tick Inventory > %s on the Modules tab"%(part.title(),part.title()))
		def g1(key):
			for k,a,e,f,b,g,d in bV:
				if k!=key:continue
				if b is None:ex();return
				c=HOST.services.get(d)if bI(b)else None
				if c is None:API.SysMsg("%s: %s is off; tick Inventory > %s on the Modules tab."%(ao,a,a),aK);return
				c();return
		def c7():return tuple(bI(a[4])for a in bV)
		def g2(grid,b,y):
			ap["quick_sig"]=c7()
			for i,(k,c,d,f,a,e,g)in enumerate(bV):m(grid,ap["store"],k,d,b,y+i*24,c,et(a,e),hue=None if bI(a)else l,on_click=ay("quick_press",k))
		bJ=18;eu=22
		def ev(grid,c,y):
			ap["quick_sig"]=c7();x=c-len(bV)*eu
			for i,(k,d,g,e,b,f,h)in enumerate(bV):
				with Kit.quiet:
					a=G.CreateGumpItemPic(e,bJ,bJ);a.SetRect(x+i*eu,y,bJ,bJ)
					if not bI(b):N(a,"Hue",l)
					N(a,"DrawBorder",False);t=et(b,f);a.SetTooltip(t if not bI(b)else d+": "+t);G.AddControlOnClick(a,ay("quick_press",k));grid.Add(a)
		g3=dict((hU,frozenset(hV))for hU,hW,hV in b2);bW=(frozenset(),())
		def g4(idx):
			b,c=p["rules"].get(idx,bW);a=set(c)
			for k in b:a|=g3.get(k,frozenset())
			return a
		def g5(serial):
			s=int(serial or 0)
			for b in range(12):
				a=API.FindItem(s)
				if a is None:return False
				if int(a.Graphic or 0)==8198 or a.IsCorpse:return True
				c=int(a.Container or 0)
				if not c or c==0xFFFFFFFF or c<0x40000000:return False
				s=c
			return False
		def ew():
			h=[w for w in p["filters"]if w["on"]and w["slot"]is not None and w["set"]];b={}
			for a,c in p["layout"]:
				m=g4(a)
				if m:b[a]=m
			if not b and not h:return
			i={}
			for a in sorted(b):
				for n in b[a]:
					if n not in i:i[n]=a
			o=dict((y,x)for x,y in p["layout"]);d=[];q=safe(lambda:int(API.Backpack),0)
			if q:d.append(q)
			for u,c in p["layout"]:
				if c not in d and not g5(c):d.append(c)
			j=[]
			for e in d:
				s=b.get(o.get(e),())
				for f in API.ItemsInContainer(e,False)or[]:
					if len(j)>=fg:break
					try:r,k=int(f.Serial),int(f.Graphic)
					except Exception:continue
					if r in o:continue
					a=None
					if h:
						t=int(f.Hue or 0)&16383
						for g in h:
							if k in g["set"]and(g["hue"]is None or g["hue"]==t):a=g["slot"];break
					if a is None:
						a=i.get(k)
						if a is None or k in s:continue
					if f.IsContainer:continue
					l=p["assign"].get(a)
					if l and l!=e:j.append((r,e,l,a))
			return j
		def ex():
			bl()
			if p["sort"]:API.SysMsg(ao+": already sorting; press Stop first.",aA);return
			if p["job"]:API.SysMsg(ao+": busy with %s; press Stop first."%p["job"]["spell"],aA);return
			a=ew()
			if a is None:API.SysMsg(ao+": no sort rules yet; tick what each bag holds in Sort rules.",aA);cY("srt");return
			if not a:API.SysMsg(ao+": nothing to sort; every ruled item is in its bag.",aK);aU("Nothing to sort");return
			p["sort"]={"plan":a,"i":0,"move":None,"check":None,"at":0.,"hold":0.,"moved":0,"refused":0,"streak":0,"rechecks":0,"waits":0,"why":None,"last":0,"sent_at":0.};aU("Sort 0/%d"%len(a));API.SysMsg(ao+": sorting %s."%F(len(a),"item"),aK)
		def g6(s,now):
			e,f,b,g=s["check"];c=s["sent_at"]
			if ak(c,fi)is not None:bc("bag #%d (%s) is full"%(g+1,a5(b,False)));return False
			d=API.FindItem(e);a=int(d.Container)if d else None
			if a is None and s["rechecks"]<dq and not g7(s,b):s["rechecks"]+=1;s["at"]=now+bx*.5;return False
			if a is None or a==b:s["moved"]+=1;s["streak"]=s["rechecks"]=s["waits"]=0;s["check"]=None;return True
			if(a==f and ak(c,fj)is not None and s["waits"]<dp):s["waits"]+=1;s["i"]-=1;s["check"]=None;s["rechecks"]=0;s["hold"]=now+bx;return False
			if s["rechecks"]<dq:s["rechecks"]+=1;s["at"]=now+bx*.5;return False
			s["check"]=None;s["rechecks"]=0;s["refused"]+=1;s["streak"]+=1
			if s["streak"]>=dp:bc("%d moves in a row were refused"%s["streak"]);return False
			return True
		def ey(bag,graphic,deep=None):
			n=0
			try:
				if deep is None:
					for x in(API.ItemsInContainer(bag,False)or[]):
						if int(x.Graphic)==graphic:n+=int(x.Amount or 1)
				else:
					for x in deep:
						if int(x.Graphic)==graphic and int(x.Container)==bag:n+=int(x.Amount or 1)
			except Exception:pass
			return n
		def g7(s,bag):a=s.get("pre");return True if not a or not a[0]else ey(bag,a[0])>=a[2]+a[1]
		def g8(now):
			s=p["sort"]
			if s is None:return
			if s["move"]is not None:return
			if s["why"]:bc(s["why"]);return
			if s["check"]is not None:
				if now<s["at"]or not g6(s,now):return
			if now<s["hold"]:return
			if cF():bc("another target cursor is in use");return
			h=aw()
			if h and not(h==s["last"]and now-s["sent_at"]<2*bx):bc("you picked something up");return
			d=s["plan"]
			while s["i"]<len(d):
				e,f,a,b=d[s["i"]];s["i"]+=1;c=API.FindItem(e);j=int(c.Container)if c else 0
				if j!=f:continue
				if p["assign"].get(b)!=a:continue
				if not T(a):bc("slot #%d's bag is out of reach"%(b+1));return
				g=API.ItemsInContainer(a,True)or[];k=len(g)
				if k>=fh:bc("bag #%d (%s) is full"%(b+1,a5(a,False)));return
				s["move"]=(e,f,a,b);i=int(c.Graphic or 0);s["pre"]=(i,int(c.Amount or 1),ey(a,i,g));aU("Sort %d/%d"%(s["i"],len(d)));return
			ha()
		def g9():
			s=p["sort"]
			if s is None or s["move"]is None:return
			a=s["move"];s["move"]=None
			if p["shutting"]:return
			if cF():s["why"]="another target cursor is in use";return
			if aw():s["why"]="you picked something up";return
			try:API.MoveItem(a[0],a[2])
			except Exception as e:s["why"]="a move failed (%s)"%e;return
			aM();s["check"]=a;s["last"]=a[0];s["sent_at"]=time.time();s["at"]=s["sent_at"]+bx
		def ha():
			s,p["sort"]=p["sort"],None
			if s is None:return
			a="%d moved"%s["moved"]
			if s["refused"]:a+=", %d refused"%s["refused"]
			API.SysMsg(ao+": sort done: %s."%a,aA if s["refused"]else be);aU("Sorted %d"%s["moved"])
		def bc(why=None,user=False):
			s,p["sort"]=p["sort"],None
			if s is None:return
			if user:API.SysMsg(ao+": sort stopped (%d moved)."%s["moved"],aK);aU("Stopped")
			elif why:API.SysMsg(ao+": sort stopped: %s (%d moved)."%(why,s["moved"]),aA);aU("Sort stopped")
		def hb():bU(True);bc(user=True)
		ez="UnifiedBag_filters";c8=40;cj=("exact","kind","category");hc={"exact":"this exact item","kind":"this kind","category":"its category"};ck=(("reagents","Reagents"),("potions","Potions"),("bandages","Bandages"),("gold","Gold and gems"),("scrolls","Scrolls"),("maps","Treasure maps"),("ores","Ores and ingots"),("wood","Wood"),("hides","Hides and cloth"),("food","Food"),("weapons","Weapons"),("armour","Armour"),("jewellery","Jewellery"),("keys","Keys and tools"));hd={"maps":("treasure map","tattered map","map"),"ores":(" ore","ingot"),"wood":("log","board"),"hides":("hide","leather","cloth","wool","cotton","flax","yarn","thread","bolt of"),"food":("bread","cake","muffin","pie","apple","pear","peach","grape","fish steak","ham","bacon","sausage","ribs","cheese","carrot","lettuce","cabbage","turnip","onion","melon","squash","gourd","lemon","lime","banana","date","coconut","chicken","bird","egg","cookie","wedge","corn","pumpkin","meat","jar of honey"),"keys":("key","tongs","hammer","saw","scissors","pickaxe","shovel","lockpick","sewing","tinker","mortar","fletcher","dovetail","skillet","rolling pin","scorp","plane","inshave","fishing pole","hatchet","smith")};he=(6+2,10,14,18);hf=134217728;a2={"data":None,"wanted":False}
		def hg():
			c=ai.f_tiles.GetValue(None)if ai.f_tiles is not None else None;a=dict((j,set())for j,n in ck)
			for k,i,d in b2:
				if k=="gems":a["gold"].update(d)
				elif k in a:a[k].update(d)
			if c is not None:
				for b in range(min(int(c.Length),65536)):
					try:
						t=c[b];e=str(t.Name or "").lower()
						if not e:continue
						f=int(t.Flags)
						if bool(t.IsImpassable):continue
						if bool(t.IsWeapon):a["weapons"].add(b)
						if f&hf:a["armour"].add(b)
						if bool(t.IsWearable)and int(t.Layer)in he:a["jewellery"].add(b)
						if f&2097152 or bool(t.IsContainer):continue
						g=" "+e
						for k,h in hd.items():
							for w in h:
								if w in g:a[k].add(b);break
					except Exception:continue
			a2["data"]=dict((q,frozenset(s))for q,s in a.items());p["dirty_flt"]=p["open_flt"]
		def hh(graphic):
			a=a2["data"]or{}
			for k,b in ck:
				if graphic in a.get(k,()):return k
			return
		def hj():
			p["filters"]=[]
			for d in str(ac(ez,"")or "").split(";"):
				a=d.split("~")
				if len(a)<5 or len(p["filters"])>=c8:continue
				try:e=int(a[3])if a[3]!=""else None;f=int(a[2])if a[2]!=""else None;c=tuple(int(h,16)for h in a[1].split(",")if h and not h.startswith("@"))
				except ValueError:continue
				g=a[1][1:]if a[1].startswith("@")else None;b=None
				if len(a)>=7 and ":"in a[5]:
					try:b=(int(a[5].split(":",1)[0],16),int(a[5].split(":",1)[1]))
					except ValueError:b=None
				p["filters"].append({"name":a[0],"gr":c,"cat":g,"hue":f,"slot":e,"on":a[4]=="1","set":frozenset(c),"base":b,"broad":a[6]if len(a)>=7 and a[6]in cj else None})
			a2["wanted"]=a2["wanted"]or any(i["cat"]for i in p["filters"])
		def bu():M(ez,";".join("~".join((a["name"].replace(";"," ").replace("~"," "),"@"+a["cat"]if a["cat"]else ",".join("%X"%b for b in a["gr"]),""if a["hue"]is None else str(a["hue"]),""if a["slot"]is None else str(a["slot"]),"1"if a["on"]else "0","%X:%d"%a["base"]if a.get("base")else "",a.get("broad")or ""))for a in p["filters"]));p["dirty_flt"]=p["open_flt"]
		def c9():
			a=a2["data"]
			if a is None:return
			for f in p["filters"]:
				if f["cat"]:f["set"]=a.get(f["cat"],frozenset())
		def hk():a2["wanted"]=True;p["open_flt"]=True;p["dirty_flt"]=True
		def hl():cl();bA("flt");p["open_flt"]=False;ap["flt_checks"]=[]
		def cl():
			g=ap.get("flt")
			if u(g):p["flt_x"],p["flt_y"]=int(g.GetX()),int(g.GetY())
		def hm():cl();p["flt_min"]=not p["flt_min"];p["dirty_flt"]=True
		def eA(name,gr,hue,cat=None,broad=None):
			if len(p["filters"])>=c8:API.SysMsg(ao+": %d filters is the most; remove one first."%c8,aA);return
			f={"name":name,"gr":tuple(gr),"cat":cat,"hue":hue,"slot":None,"on":True,"set":frozenset(gr),"broad":broad};p["filters"].append(f);c9();bu();return f
		def hn(key):
			for k,a in ck:
				if k==key:
					for f in p["filters"]:
						if f["cat"]==key:API.SysMsg(ao+": %s is already on the list."%a,aK);return
					eA(a,(),None,key)
		def ho():API.SysMsg(ao+": target an item for the new filter.",aK);bT("filter_targeted")
		def eB(target):
			if not target:API.SysMsg(ao+": cancelled.",aK);return
			a=T(target)
			if not a:API.SysMsg(ao+": that isn't an item.",aA);return
			if a.IsContainer:API.SysMsg(ao+": bags aren't sorted; target an item.",aA);return
			return a
		def hp(target):
			a=eB(target)
			if a:eC(int(a.Graphic),int(a.Hue or 0)&16383,str(a.Name or ""))
		def eC(graphic,hue,name):
			if not name:t=cR(graphic);name=str(t.Name or "")if t is not None else ""
			eA((name or "0x%04X"%graphic)[:30],(graphic,),hue,None,"exact")
		def hq():
			a=safe(cS)
			if a is None:return
			try:d=int(Tz.get(a,"Serial"));c=int(Tz.get(a,"Graphic"));e=int(Tz.get(a,"Hue"))&16383;b=int(Tz.get(a,"Container"))
			except Exception:return
			if safe(lambda:bool(cR(c).IsContainer),False):API.SysMsg(ao+": bags aren't sorted; drop an item.",aA);return
			eC(c,e,"")
			if b and b!=0xFFFFFFFF:import System;Tz.call(None,"DropItem",(System.UInt32(d),65535,65535,0,System.UInt32(b),False),ai.Actions)
		def hr(i):
			if not 0<=i<len(p["filters"]):return
			f=p["filters"][i]
			if f.get("base")is None and f["gr"]:f["base"]=(f["gr"][0],f["hue"]or 0)
			a=f.get("base")
			if a is None:return
			d=(f.get("broad")or("category"if f["cat"]else("exact"if f["hue"]is not None else "kind")));b=cj[(cj.index(d)+1)%len(cj)]
			if b=="category":
				c=hh(a[0])
				if c is None:b="exact"
				else:f.update({"cat":c,"hue":None,"gr":(a[0],)})
			if b!="category":f.update({"cat":None,"hue":a[1]if b=="exact"else None,"gr":(a[0],),"set":frozenset((a[0],))})
			f["broad"]=b;c9();bu()
		def hs(i,d):
			j=i+d
			if 0<=i<len(p["filters"])and 0<=j<len(p["filters"]):p["filters"][i],p["filters"][j]=p["filters"][j],p["filters"][i];bu()
		def ht(i):
			if 0<=i<len(p["filters"]):del p["filters"][i];bu()
		def hu(i):
			if not 0<=i<len(p["filters"]):return
			p["flt_pick"]=p["filters"][i];API.SysMsg(ao+": click a bag on the bags display, or target a bag in a slot.",aK);bT("filter_bag_targeted",p["flt_pick"])
		def hv(f,target):
			if p["flt_pick"]is not f:return
			p["flt_pick"]=None
			if not target:return
			a=dict((g,d)for d,g in p["layout"]);s=int(target)
			for c in range(8):
				if s in a:f["slot"]=a[s];bu();return
				b=T(s);s=int(b.Container or 0)if b else 0
				if not s:break
			API.SysMsg(ao+": that isn't in a bag slot; put the bag in a slot first (Slots).",aA)
		def hw(a):
			f,p["flt_pick"]=p["flt_pick"],None
			if f is None:return False
			f["slot"]=a;bu();API.CancelTarget();return True
		def hx():
			for i,b in ap.get("flt_checks")or():
				if i<len(p["filters"]):
					a=bool(safe(lambda:b.IsChecked,p["filters"][i]["on"]))
					if a!=p["filters"][i]["on"]:p["filters"][i]["on"]=a;bu();return
		def hy():
			cl();bA("flt");c9();M,h=K,B;s=len(p["filters"]);n,o,q=28,30+3*26+8,40;k=max(n*2,min(s,12)*n+8);w=640;O=(M+30+M if p["flt_min"]else M+30+h+q+h+o+h+k+M);g,c,y=b3("flt",w,O,"SORT FILTERS",ay("toggle_flt_min"),ay("close_filters"));t=[]
			if not p["flt_min"]:
				d=w-2*M;z(g,M,y,d,q);m(g,c,"sort",L,M+12,y+9,"Sort",es,on_click=ay("start_sort"));u=safe(ew);P=len(u)if u else 0;e(g,"%s would move"%F(P,"item"),M+100,y+12,l);y+=q+h;z(g,M,y,d,o,"ADD A FILTER");R=M+12;m(g,c,"add",L,R,y+28,"Add by target...","Target an item: the filter fills in from it",on_click=ay("filter_by_target"));r=5;x=(d-24)//r
				for A,(E,j)in enumerate(ck):S,T=(A+1)%r,(A+1)//r;m(g,c,"pre_"+E,X,M+12+S*x,y+28+T*26,C(j,x-40),"Add the %s preset"%j.lower(),on_click=ay("filter_preset",E))
				y+=o+h;z(g,M,y,d,k);Q(g,M,y,d,k,ay("filter_dropped"),"Drop an item here to add a filter")
				if not s:e(g,"No filters yet. Press a preset, or Add by target.",M+12,y+8,l)
				else:
					a=G.CreateGumpScrollArea(M+4,y+4,d-8,k-8)
					for i,f in enumerate(p["filters"]):
						b=i*n;U=au(a,"",4,b+3,f["on"],"Use this filter (unticked: kept, moves nothing)");t.append((i,U));e(a,C(f["name"],150),30,b+5);J=f.get("broad")or("category"if f["cat"]else("exact"if f["hue"]is not None else "kind"))
						if f["cat"]and not f.get("base"):e(a,"A preset",186,b+5,l)
						else:m(a,c,"m%d"%i,I,186,b+2,"Match: "+J,"Matches %s; click for the next"%hc[J],on_click=ay("filter_broader",i))
						if f["slot"]is None or f["slot"]not in p["assign"]:j,N="No bag",v
						else:j,N=(bi(a5(p["assign"][f["slot"]],False),14),D)
						e(a,j,330,b+5,N);m(a,c,"b%d"%i,L,424,b+2,"Bag...","Click a bag on the bags display, or target a bag in a slot",on_click=ay("filter_pick_bag",i));m(a,c,"u%d"%i,I,508,b+2,None,"Move up (the first match wins)",on_click=ay("filter_move",i,-1));m(a,c,"d%d"%i,I,536,b+2,None,"Move down (the first match wins)",on_click=ay("filter_move",i,1));m(a,c,"x%d"%i,H,564,b+2,None,"Remove this filter",on_click=ay("filter_remove",i))
					g.Add(a)
			b4("flt",g,cl);ap["flt_checks"]=t
		da={"sync_at":0.}
		def bl():
			d=ap["rule_checks"]
			if not d or not u(ap["srt"]):return False
			e,f={},set()
			for a,g,l in d:
				if a>=p["slots"]:continue
				f.add(a)
				try:h=bool(l.IsChecked)
				except Exception:h=g in p["rules"].get(a,bW)[0]
				if h:e.setdefault(a,set()).add(g)
			i=False
			for a in f:
				b=p["rules"].get(a);j=b[1]if b is not None else();k=frozenset(e.get(a,()));c=(k,j)if(k or j)else None
				if c!=b:
					i=True
					if c is None:del p["rules"][a]
					else:p["rules"][a]=c
			return i
		def hz():
			bl();cm("srt");M,d=K,B;w,r,k,s=580,52,40,52;h=min(p["slots"]*r+8,430);v=(M+30+M if p["srt_min"]else M+30+d+k+d+h+d+s+M);g,i,y=b3("srt",w,v,"SORT RULES",ay("toggle_win_min","srt"),ay("close_win","srt"));t=[]
			if not p["srt_min"]:
				f=w-2*M;z(g,M,y,f,k);m(g,i,"sort",L,M+12,y+9,"Sort","Move matching items from your backpack and other slot bags into their bag, one at a time",on_click=ay("start_sort"));m(g,i,"stop",H,M+150,y+9,"Stop","Stop sorting",on_click=ay("stop_sort",None,True));e(g,"Tick what each slot's bag holds.",M+250,y+12,l);y+=k+d;z(g,M,y,f,h);b=G.CreateGumpScrollArea(M+4,y+4,f-8,h-8);n=f-8-20;A=n-171-o("+%d graphics"%b1)
				for a in range(p["slots"]):
					c=a*r;C,j=p["rules"].get(a,bW);e(b,"#%d"%(a+1),6,c+5,E)
					if a in p["assign"]:e(b,bi(a5(p["assign"][a],False),24),44,c+5)
					else:e(b,"No bag in this slot",44,c+5,l)
					D=e(b,("+%s"%F(len(j),"graphic"))if j else "",A,c+5,l)
					if j:D.SetTooltip(", ".join("0x%04X"%W for W in j))
					m(b,i,"add%d"%a,L,n-165,c+3,"Add...","Target an item; slot #%d's bag holds its graphic too"%(a+1),on_click=ay("add_rule_graphic",a));m(b,i,"clr%d"%a,H,n-80,c+3,"Clear","Forget the graphics added to slot #%d"%(a+1),on_click=ay("clear_rule_graphics",a));x=24
					for u,q,J in b2:I=au(b,q,x,c+27,u in C,"Slot #%d's bag holds %s"%(a+1,q.lower()));t.append((a,u,I));x+=36+o(q)
				g.Add(b);y+=h+d;z(g,M,y,f,s);e(g,"Sort moves one item every %.1f s from your backpack and other bags."%bx,M+12,y+8,l);e(g,"It stops when you pick something up or a bag is full.",M+12,y+28,l)
			b4("srt",g,cZ,rule_checks=t);da["sync_at"]=time.time()+1.
		def hA(idx):API.SysMsg(ao+": target an item; slot #%d's bag will hold its graphic."%(idx+1),aK);bT("add_rule_graphic_to",idx)
		def hB(idx,target):
			if target:
				bl()
				if idx>=p["slots"]:return
			c=eB(target)
			if not c:return
			a=int(c.Graphic);d,b=p["rules"].get(idx,bW)
			if not a or a in b:API.SysMsg(ao+": slot #%d's bag already holds that."%(idx+1),aK);return
			if len(b)>=b1:API.SysMsg(ao+": slot #%d already holds %d graphics; click Clear first."%(idx+1,b1),aA);return
			p["rules"][idx]=(d,b+(a,));p["dirty_srt"]=True;a9();API.SysMsg(ao+": slot #%d's bag holds graphic 0x%04X too."%(idx+1,a),be)
		def hC(idx):
			bl();a,b=p["rules"].get(idx,bW)
			if not b:return
			if a:p["rules"][idx]=(a,())
			else:p["rules"].pop(idx,None)
			p["dirty_srt"]=True;a9()
		def cm(k):cn();bA(k)
		def cn():
			for a,b,c in(("mgr","mgr_x","mgr_y"),("trp","trp_x","trp_y"),("srt","srt_x","srt_y")):
				g=ap[a]
				if u(g):p[b]=g.GetX();p[c]=g.GetY()
		def hD():
			if p["open_flt"]:
				if p["dirty_flt"]:p["dirty_flt"]=False;hy()
				elif not u(ap.get("flt")):p["open_flt"]=False;ap["flt_checks"]=[]
				else:hx()
			for k,b in(("mgr",gy),("trp",gK),("srt",hz)):
				if not p["open_"+k]:p["dirty_"+k]=False
				elif p["dirty_"+k]:p["dirty_"+k]=False;b()
				elif not u(ap[k]):
					p["open_"+k]=False
					if k in ce:ap[ce[k]]=[]
				elif k=="srt"and ap["rule_checks"]:
					a=time.time()
					if a>=da["sync_at"]:
						da["sync_at"]=a+1.
						if bl():bg()
		def hE():
			c,d=r.max_w,r.max_h
			if c<=0 or d<=0:p["fit_seen"]=None;return
			a=(min(c,bd),min(d,bd))
			if a==(p["cell_w"],p["cell_h"]):p["fit_seen"]=None;return
			b=p["fit_seen"];p["fit_seen"]=(a,b[1]+1 if b and b[0]==a else 1)
			if p["fit_seen"][1]>=eV or p["fit_pending"]:p["fit_pending"]=False;p["fit_seen"]=None;p["cell_w"],p["cell_h"]=a;bh()
		def hF():
			if p["drive_fixed"]or not u(ap["grid"]):return
			a=time.time()
			if r.hook_calls!=p["hb_frame"]:
				p["hb_frame"]=r.hook_calls;p["hb_time"]=a
				if p["driving"]:p["driving"]=False
				return
			if not p["driving"]and a-p["hb_time"]>e_:
				p["driving"]=True
				if r.hook_calls==0 and not p["drive_told"]:p["drive_told"]=True;API.SysMsg(ao+": draw hook isn't called; the script keeps the bags in place (they may flicker when items move).",aK)
		hG={"add_rule_graphic":hA,"add_rule_graphic_to":hB,"add_trap_bag":gM,"add_trap_bag_to":gN,"assign_slot":gz,"assign_slot_to":gA,"auto_fill":gD,"bag_close":f9,"bag_min":f8,"bag_use":f7,"clear_all":gC,"clear_rule_graphics":hC,"clear_slot":gB,"close_filters":hl,"close_win":gw,"disable":HOST.disable,"filter_bag_targeted":hv,"filter_broader":hr,"filter_by_target":ho,"filter_canvas_pick":hw,"filter_dropped":hq,"filter_move":hs,"filter_pick_bag":hu,"filter_preset":hn,"filter_remove":ht,"filter_targeted":hp,"fold_to_bar":ei,"open_filters":hk,"open_win":cY,"quick_press":g1,"remove_trap_bag":gO,"select_all_traps":gL,"set_min":gt,"show_settings":aP,"start_job":gP,"start_sort":ex,"stop_all":hb,"stop_sort":bc,"toggle_bare":gs,"toggle_flt_min":hm,"toggle_win_min":gx,"user_collapse":gq}
		def db(w):return(("LAYOUT  (Apply to use)",(("num","slots","Slots:","Bag slots (%d-%d)"%(bX,a_),"",bX,a_),("num","cols","Columns:","Slots per row outside a zone (0-%d, 0 = near-square)"%a_,"",0,a_),("num","rows","Rows:","Rows of slots outside a zone (0-%d, 0 = near-square)"%a_,"",0,a_),("num","scale","Bag scale:","The client's Container Scale, for every container (50-200)","%",50,200),("buttons",(("apply",X,"Apply","Use the slots, columns, rows and scale above"),),{"bdy":4})),{"top":32,"sh":182,"ldy":2,"fw":60,"ugap":6,"lw":w-122}),("LOOK",(("slider","opacity","Bag opacity:","How solid bag panels and art are (10-100%); items stay solid",10,100,{"lw":158,"sdy":6,"sw":200,"ugap":20,"vfmt":"%d%%","h":30}),("check","trim","Trim bags to their item area","Hide bag art and butt the item areas together (needs client access; zones always fill)"),("check","items","Scale items with the bags","The client's option to draw items at bag scale")),{"top":32,"sh":116,"ldy":2}),("STATUS",(("note",bi(c_(),64),{"key":"status","h":24}),("note",em(),{"key":"size"})),{"top":32,"sh":86}))
		hP=Kit.Page(du,db,a9)
		def dc():
			p["shutting"]=False
			if not API.Player:p["wait_player"]=True;return
			p["wait_player"]=False;a=p["load_text"];p["load_text"]=None
			if a is None and aE():p["wait_load"]=p["load_wanted"]=True;p["to_write"]=None;return
			p.update(wait_load=False,load_wanted=False,driving=False,drive_fixed=False,drive_told=False,job=None,to_write=None,queue=[],reported=False,detached_at=0.);bQ["told"]=False;dx();p["docked"],p["link_state"]=False,None;API.RemoveSharedVar(cx);bs["wish"]=0.;aF["cols"],aF["cell"],aF["area"],aF["told"]=None,None,None,None;aN["pct"]=None;cO();hj();p["canvas"]=None;JR["rd"]=aQ();r.meas.clear();r.opened=frozenset()
			if not ai.tried:ai.tried=True;fl()
			b={"fit":bD,"riding":aG}
			if bE():b.update({"exact":True,"verify":True,"state":fD})
			HOST.layout_add(aJ,fC,ao,b)
			if ai.ok:ge()
			p["sort"]=None;SR.update({"armed":False,"lit":{},"until":0.,"counts":{},"status":None})
			if a is not None:dM(a[0])
			else:dJ()
			p["open_mgr"]=p["dirty_mgr"]=p["want_mgr"];p["open_trp"]=p["dirty_trp"]=p["want_trp"];p["open_srt"]=p["dirty_srt"]=p["want_srt"]
			if cX()and not ag(aJ):p["minimized"]=True
			ej();r.disabled,r.fail_streak,r.error=False,0,""
			if ai.ok:
				try:bn(b6)
				except Exception as e:r.error="client thread: %s"%e
			else:af(aJ);API.SysMsg(ao+": no client access (%s); using basic pinning."%ai.error,aA)
			cH();p["dirty_frame"]=True;p["hb_frame"],p["hb_time"]=-1,time.time()
			for c,d in(("bag.attach",gi),("bag.grid_size",lambda:p["grid_wh"]),("bag.fit",gf),("bag.cell",fE),("bag.shrink",cV),("bag.pack",gg),("bag.open_manager",ay("open_win","mgr")),("bag.open_traps",ay("open_win","trp"))):dv.service(c,d)
			aC(O,"hooked",("OnItemUpdated",fZ));API.SysMsg(ao+": on, %s."%F(p["slots"],"slot"),be)
		def hH():
			if p["wait_player"]:
				if API.Player:dc()
				return
			if p["wait_load"]:
				if p["load_text"]is not None:dc()
				return
			while p["queue"]:
				b=p["queue"].pop(0);c=hG[b[0]]
				try:c(*b[1:])
				except Exception as e:API.SysMsg(ao+": couldn't do that (%s)."%e,aA)
			if p["shutting"]:return
			ej();cH()
			if ai.ok and r.disabled and not p["reported"]:p["reported"]=True;API.SysMsg(ao+": draw hook stopped (%s); using basic pinning."%r.error,aA);safe(lambda:bn(dF));p["dirty_frame"]=True
			if not u(ap["bar"])or not u(ap["grid"]):p["dirty_frame"]=True
			if(r.icons or bw)!=p["icons_used"]:p["dirty_frame"]=True
			if ai.ok and not r.disabled:
				hF()
				if p["driving"]:
					try:bn(cz)
					except Exception as e:r.error="client thread: %s"%e
				hE();fP()
			else:
				if p["canvas"]is not None:d2(None)
				gu()
			if p["dirty_frame"]and not bP():p["dirty_frame"]=False;gn()
			else:
				if aG():ek()
				eh()
			hD();gR();a=time.time()
			if not 0<=p["quick_at"]-a<=1.:
				p["quick_at"]=a+1.
				if ap.get("quick_sig")is not None and ap["quick_sig"]!=c7():p["dirty_frame"]=True
			g_(a);g8(a);g9();gd(a)
			if(p["frame_x"],p["frame_y"])!=(p["saved_fx"],p["saved_fy"])and p["save_in"]<0 and not aG()and p["canvas"]!="alone"and a-p["detached_at"]>=e3:bg()
			if p["save_in"]>0:p["save_in"]-=1
			elif p["save_in"]==0:cn();a9()
		def hI():
			if p["load_wanted"]:
				p["load_wanted"]=False;a=dL()
				if p["wait_load"]and not p["shutting"]:p["load_text"]=(a,)
			fQ()
			if a2["wanted"]and a2["data"]is None:
				a2["wanted"]=False
				try:hg()
				except Exception:a2["data"]={}
			cG()
		def hJ():return eX if p["driving"]else eW
		def hK():return bool(p["load_wanted"]or p["to_write"]is not None or d3()or(a2["wanted"]and a2["data"]is None))
		dJ()
		def hL():
			p["shutting"]=True
			if p["wait_player"]or p["wait_load"]:p["wait_player"]=p["wait_load"]=p["load_wanted"]=False;p["load_text"]=None;return
			safe(bU);p.update(job=None,queue=[],sort=None);safe(lambda:cg(time.time()));bl();bt();dv.close();HOST.layout_remove(aJ)
			if aN["pct"]is not None:safe(lambda:cV(None))
			if p["attach"]is not None:p["attach"]=None;p["frame_x"],p["frame_y"]=p["saved_fx"],p["saved_fy"]
			p["grid_wh"]=None;p["docked"],p["link_state"]=False,None;API.SetSharedVar(ds,"off");safe(cO);p["canvas"]=None
			if ai.ok:safe(lambda:bn(dF))
			cn();a9();cG()
			for a in("grid","bar","mgr","trp","srt"):bA(a)
			p["open_mgr"]=p["open_trp"]=p["open_srt"]=False;ap.update({"side_status":None,"trap_checks":[],"rule_checks":[],"search_box":None,"counts":[]});p.update(bar_raw=None,grid_raw=None,grid_info=(None,False),slot_raws=())
		return{"start":dc,"tick":hH,"stop":hL,"client_tick":True,"config_height":gE,"build_config":gF,"poll_config":gG,"config_closed":en,"interval":hJ,"thread_tick":hI,"thread_wanted":hK}
	def bh():
		H="character";E="Paperdoll";bn="Character_settings";aS="Character_pos";aT="Character_min";b3,b4=240,46;b5=7939;n=48;an=6;b6=16;bo,b7=260,237;ag=80;bp=.2;dc=.85;b8=.95;b9=90;bq=30;ca=74;cb,cc=40,3.5;cd=.1;W=B;ce=.5;br=5;bs,bt=50000,60000;cf,cg=970,547;ch=(694,695)
		try:import clr;from System import Array,Object,UInt32,UInt16,Int32,Double,Enum;from System.Reflection import BindingFlags;bu=True
		except Exception:bu=False
		aC=((6,"helmet","Helm","Head"),(13,"torso","Chest","Chest armour"),(19,"arms","Arms","Arms"),(7,"gloves","Gloves","Gloves"),(24,"legs","Legs","Leg armour"),(18,"earrings","Ears","Earrings"),(10,"neck","Neck","Necklace / gorget"),(17,"tunic","Tunic","Tunic / surcoat (over the chest)"),(12,"waist","Belt","Belt / half apron"),(3,"shoes","Feet","Shoes / boots"),(5,"shirt","Shirt","Shirt"),(22,"robe","Robe","Robe"),(20,"cloak","Cloak","Cloak / quiver"),(23,"skirt","Kilt","Skirt / kilt"),(4,"pants","Pants","Pants"),(1,"onehanded","Main","Main hand (one-handed weapon)"),(2,"twohanded","Off","Off hand (shield, two-handed weapon)"),(8,"ring","Ring","Ring"),(14,"bracelet","Brace","Bracelet"),(9,"talisman","Talis","Talisman"),);aU=5;bv=set(dh[0]for dh in aC);ci=tuple(di[0]for di in aC);cj={"neck":("Necklace",),"onehanded":("OneHanded",),"twohanded":("TwoHanded",),"earrings":("Earrings",),"bracelet":("Bracelet",),"talisman":("Talisman",)};aV,aX,aE,ah,aY,aH,aZ,a_=(1,2,3,4,5,6,7,8);a1,a5,ai,a7,L,a8,ap,aq=(9,10,11,12,13,14,15,16);ar,ba,X,aI,at,aM,au=17,18,19,20,22,23,24;bx=dict((dj[0],dj[1])for dj in aC);bx.update({ai:"hair",aq:"beard",ap:"face"});by=(aI,aY,ah,aE,au,X,L,ar,a_,a8,ap,aZ,aM,at,a7,a5,ai,aq,ba,aH,aV,aX,a1);ck=(aY,ah,aE,au,X,L,ar,a_,a8,ap,aZ,aM,at,aI,a7,a5,ai,aq,ba,aH,aV,aX,a1);cl=(aY,ah,aE,au,X,L,ar,aI,a_,a8,ap,aZ,aM,a7,a5,ai,aq,ba,aH,aV,aX,a1,at);bz=tuple(sorted(set(by)));bc=(39301,39302,42002,41675,41674);bA={400:12,402:12,401:13,403:13,605:14,607:14,606:15,608:15,666:666,694:666,667:665,695:665,1253:51253,987:12};cm=(401,403,606,608,667,695);bB,cn,co=987,1002,50987;m=K;F=8;ak=n+an;cp=aU*ak-an;T=F*2+2*(2*n+an)+2*F+bo;aa=F*2+cp;bC=4*F+2*(2*n+an);cq=100;be=bC+cq;cr=(150,235);av=2;cs=300;bD=T+2*m;J=m+30+B;r={"stats":True,"combine":True,"beside":False,"left":False};dd=dict(r);d={"shutting":False,"minimized":False,"docked":False,"queue":[],"sig":None,"doll_sig":None,"stats_at":0.,"doll_at":0.,"px":m,"attached":None,"beside_said":False,"layer_name":{},"wait_player":False,"saved_min":False,"w_armed":True,"w_at":0.,"wbar":None,"fit":None,"k":1.,"py":None,"strip_w":None,"pw":T,"col":None,"ph":aa,"rp":ak,"pair":None,"pair_at":0.,"room":None,"room_fs":None,"told_shrink":None,"grew":False,"paired":False};k={"g":None,"c":{},"store":({},{}),"slots":[],"raw":None,"doll":[]};de,q,df=am(d,E)
		def bE():
			p=ac(bn).split("|")
			if len(p)>=2:r["stats"]=p[0]=="1";r["combine"]=p[1]=="1"
			if len(p)>=3:r["beside"]=p[2]=="1"
			if len(p)>=4:r["left"]=p[3]=="1"
			d["saved_min"]=bool(Kit.load_min(aT))
		def bF():M(bn,"|".join(["1"if r[a]else "0"for a in("stats","combine","beside","left")]+["0"]))
		def ct():
			if not d.get("wait_player"):a2(aT,d["minimized"]and not d["docked"])
		def bG():a3(aS,k["g"])
		class Box(object):pass
		j=Box();j.tried=j.ok=False;j.error,j.pixel_n="",0
		for cu in("m_animid","m_covered","MobileType","cursor","SlotItem","DollPiece","m_pixel","gumps","f_tiles","tiles"):setattr(j,cu,None)
		def cv():
			if not bu:j.error="clr module unavailable";return
			try:
				a=API.GetType().Assembly;clr.AddReference(a);from ClassicUO.Game.UI.Controls import ItemGump,Control;b=BindingFlags.Static|BindingFlags.Public|BindingFlags.NonPublic;q=BindingFlags.Instance|BindingFlags.NonPublic;d=BindingFlags.Instance|BindingFlags.Public|BindingFlags.NonPublic;e=a.GetType("ClassicUO.Client");j.p_game=e.GetProperty("Game",b)if e is not None else None;f=a.GetType("ClassicUO.GameController");j.p_uo=f.GetProperty("UO",d)if f is not None else None;g=a.GetType("ClassicUO.UltimaOnline");j.p_cursor=g.GetProperty("GameCursor",d)if g is not None else None;j.ItemGump=ItemGump
				try:
					class SlotItem(ItemGump):
						def Contains(self,x,y):return True
					j.SlotItem=SlotItem
				except Exception:j.SlotItem=None
				try:
					class DollPiece(ItemGump):
						def Contains(self,x,y):
							try:
								k=self.va_k
								if j.pixel_n==4:a=[UInt32(self.va_gid),Int32(int(x)),Int32(int(y)),Double(k)]
								else:a=[UInt32(self.va_gid),Int32(int(x/k)),Int32(int(y/k))]
								return bool(j.m_pixel.Invoke(j.gumps,Array[Object](a)))
							except Exception:return True
						def OnMouseDown(self,x,y,button):self.va_down=True;ItemGump.OnMouseDown(self,x,y,button)
						def OnMouseUp(self,x,y,button):self.va_down=False;ItemGump.OnMouseUp(self,x,y,button)
						def Update(self):
							ItemGump.Update(self)
							if self.va_down:cz(self)
					j.DollPiece=DollPiece
				except Exception:j.DollPiece=None
				h=a.GetType("ClassicUO.Game.GameActions");j.m_equip=h.GetMethod("Equip",b);j.m_swap=h.GetMethod("QueueEquipSwap",b);j.LayerType=a.GetType("ClassicUO.Game.Data.Layer");i=clr.GetClrType(Control);j.f_bounds=i.GetField("_bounds",q);j.Point=clr.GetPythonType(i.GetProperty("Location").PropertyType)
				for k in("m_equip","m_swap","LayerType","f_bounds","p_game","p_uo","p_cursor"):
					if getattr(j,k)is None:raise Exception("client member not found: "+k)
				j.ok=True
			except Exception as r:j.ok=False;j.error=str(r);return
			try:
				l=j.p_game.GetValue(None,None);c=j.p_uo.GetValue(l,None)if l is not None else None;o=c.GetType().GetProperty("Gumps")if c is not None else None;j.gumps=o.GetValue(c,None)if o is not None else None;j.m_pixel,j.pixel_n=None,0
				if j.gumps is not None:
					for m in j.gumps.GetType().GetMethods():
						n=len(m.GetParameters())
						if m.Name=="PixelCheck"and n in(3,4)and n>j.pixel_n:j.m_pixel,j.pixel_n=m,n
			except Exception:j.gumps=j.m_pixel=None
			if j.m_pixel is None:j.DollPiece=None
			j.f_tiles=safe(bb)
			try:p=a.GetType("ClassicUO.Game.UI.Controls.PaperDollInteractable");j.m_animid=p.GetMethod("GetAnimID",b)if p is not None else None;j.animid_n=(int(j.m_animid.GetParameters().Length)if j.m_animid is not None else 0)
			except Exception:j.m_animid=None
			try:j.MobileType=a.GetType("ClassicUO.Game.GameObjects.Mobile");j.m_covered=(j.MobileType.GetMethod("IsCovered",b)if j.MobileType is not None else None)
			except Exception:j.m_covered=None
		bH={}
		def az(layer):
			e=bH.get(layer)
			if e is None:e=bH[layer]=Enum.ToObject(j.LayerType,layer)
			return e
		cw={};cx=256
		def bI():a=k["raw"];return None if a is None else a.World
		def cy():w=bI();return None if w is None else w.Player
		def bf():
			try:
				b=j.cursor
				if b is None:c=j.p_game.GetValue(None,None);d=j.p_uo.GetValue(c,None)if c is not None else None;b=j.cursor=j.p_cursor.GetValue(d,None)if d is not None else None
				h=b.ItemHold
				if h.Enabled and not h.IsFixedPosition:
					a=cA(int(h.Graphic))
					if a not in bv:
						try:a=int(h.Layer)
						except Exception:a=0
					return int(h.Serial),bool(h.IsWearable),a
			except Exception:pass
			return
		def cz(piece):
			try:
				a=j.cursor
				if a is None:b=j.p_game.GetValue(None,None);c=j.p_uo.GetValue(b,None)if b is not None else None;a=j.cursor=j.p_cursor.GetValue(c,None)if c is not None else None
				h=a.ItemHold
				if h.Enabled and int(h.Serial)==int(piece.LocalSerial):piece.va_down=False;h.IsGumpTexture=False;h.MouseOffset=j.Point(0,0)
			except Exception:piece.va_down=False
		def cA(graphic):
			try:
				a=j.tiles
				if a is None:
					if j.f_tiles is None:return 0
					a=j.tiles=j.f_tiles.GetValue(None)
				return 0 if a is None or graphic<0 or graphic>=a.Length else int(a[graphic].Layer)
			except Exception:return 0
		def bg(c,x,y):c.Location=j.Point(x,y)
		cB=Kit.disposer(H,d,k);bJ=2*n+an
		def cC(i):
			a,b=divmod(i,aU)
			if a<2:x=d["px"]+F+a*ak
			else:x=d["px"]+d["pw"]-F-bJ+(a-2)*ak
			return x,bi()+F+int(round(b*d["rp"]))
		def bh():return bool(aj(H))
		def bK():x=d["px"]+2*F+bJ;return(x,bi()+F,max(1,d["pw"]-bC),max(1,d["ph"]-2*F))
		def bi():a=d["py"];return J if a is None else a
		bj,bL=.4,2.;bM=300
		def cD(w,h,mode):
			a=(int(w),int(h))if(w is not None and h is not None)else None
			if a!=d["fit"]or(mode=="again"and a is not None and not d["paired"]):d["fit"]=a;d["pair"]=bN()if a is not None else None;d["pair_at"]=time.time();q("redraw")()
		def bN():
			if d["attached"]is None:return
			try:a=HOST.layout_pair(H,"bag")
			except Exception:return
			if not a or a[0]is None or a[1]is None:return
			return(tuple(int(b)for b in a[0]),tuple(int(c)for c in a[1]))
		def cE(x,y,fw,fh,k):
			(r,s,t,u),(g,h,l,n)=k
			if abs((y+fh)-h)>2*SNAP_DIST:return
			i,o=max(0,g-x),min(fw,g+l-x);b=o-i-2*m
			if b<40:return
			p=W//2;e=fh+p;a=(h+n-y)-e-m
			if a<20:return
			d["room"]=(b,a);f=bl(b,a);d["room_fs"]=f;c=f[1]if f is not None else bP(b);d["grew"]=c>a
			if c>a:j=int(aD()[1]);q=(j-y-m-e)if j>0 else c;a=max(a,min(c,q))
			return(i+m,e,b,a)
		def aN(c,raw=False,flushed=False):
			k=d["k"]
			if abs(k-1.)<.001 or c is None:return
			with Kit.quiet:
				if not raw and not flushed:U()
				a=c if raw else ab(c)
				if a is None:return
				if str(a.GetType().Name)=="GumpPicTiled":a.ScaleTiledTexture=True
				a.ApplyScale(k,True,True,False)
		def bk():
			e=V("bag.cell")
			if e is None:return
			try:v=e();b,c,f,n,g=v[0],v[1],v[2],v[3],v[4];d,a,h=(v[5],v[6],v[7])if len(v)>=8 else(100,100,100)
			except Exception:return
			if n<=0 or b<=0 or c<=0 or d<=0 or a<=0:return
			if d!=a:b,c=b*a/float(d),c*a/float(d)
			return b,c,f,n,g,a,min(h,a)
		def bO(a,f,width):g,h,b,n,e=a[0],a[1],a[2],a[3],a[4];c=int(math.ceil(g*f-.01));i=int(math.ceil(h*f-.01));j=max(c,width-e);k=max(1,min(n,(j+b)//(c+b)));d=int(math.ceil(n/float(k)));return d,d*i+(d-1)*b,c+e
		def bP(width):
			b=V("bag.pack")
			if b is not None:
				try:a=b(width,1<<20)
				except Exception:a=None
				if a is not None:return a[1]
			c=bk();return 120 if c is None else bO(c,1.,width)[1]
		def bl(hw,f):
			g=V("bag.pack")
			if g is not None:
				try:c=g(hw,f)
				except Exception:c=None
				if c is not None:return c
			a=bk()
			if a is None:return
			b,e=a[5],a[6];h=d["told_shrink"];p=b
			for m in range(int(b-e)//br+2):
				j,i,k=bO(a,p/float(b),hw);l=3*j if(h is not None and p>h)else 0
				if(i+l<=f and k<=hw)or p<=e:return(None if p>=b else p),i
				p=max(e,p-br)
		aO=10;bQ,cF=20,26;aP=14;bR=2*8+aO*bQ+aP
		def bm():
			if t["col_w"]is None:a=max(o(b)for b in("Stamina 999/999","Followers 99/99","Gold 9,999,999","Weight 0000/0000","Mana 999/999","HP 999/999"));t["col_w"]=max(bq,a)+2*af+4
			return t["col_w"]
		def cG(bw,room):
			e=cr;b=[]
			if r["stats"]:
				if bw>=bM:b.append(("strip",bw,room-ag-B))
				b.append(("col",bw-bm()-B,room))
			else:b.append(("none",bw,room))
			h,i=float(max(1,e[0])),float(max(1,e[1]));a=None
			for g,d,c in b:
				if g=="col"and c<bR:continue
				k=min(d/float(be),c/float(aa),bL)
				if k<bj:continue
				f=min((d-2*F*k)/h,(c-2*F*k)/i)
				if a is None or f>a[0]+.001 or(f>a[0]-.001 and k>a[4]):a=(f,g,d,c,k)
			if a is None:k=min(bw/float(be),room/float(aa),bL);return "none",bw,room,max(bj,k)
			return a[1],a[2],a[3],a[4]
		def cH(bw):
			a=int(math.ceil(bj*aa))+1
			if not r["stats"]:return a
			return a+ag+B if bw>=bM else max(a,bR)
		def bS(fw,fh,combined):
			c,h=m,J;a,b=max(1,fw-2*m),max(1,fh-J-m);d=W;i=max(b-bP(a)-d,min(b,max(cH(a),(b-d)//2)))if combined else b;e,o,p,k=cG(a,i);q=max(be,int(round(o/k)));j=max(aa,int(round(p/k)));f=int(round(j*k));r=(ag+B)if e=="strip"else 0;g,s=h,c
			if combined:l=max(i,f+r);n=(c,h+l+d,a,max(1,b-l-d))
			else:n=None
			t=(g+f+B)if e=="strip"else None;u=a if e=="strip"else None;v=(c+a-bm(),g,bm(),f)if e=="col"else None;return(k,int(round(s/k)),int(round(g/k)),t,u,n,(c,g+f),q,v,j)
		def aB():return aa+(B+ag if r["stats"]else 0)
		def cI(a,c):b=max(T,a);w=b+2*m;e=m+(b-T)//2;d=J+aB()+W;f=(m+(b-a)//2,d,a,c);return w,d+c+m,e,f
		def cJ(a,b):w=m+T+W+a+m;c,d=(m,m+a+W)if r["left"]else(m+T+W,m);return w,J+max(aB(),b)+m,d,(c,J,a,b)
		def cK(a,b):
			if not r["beside"]:
				w,h,e,f=cI(a,b);c=int(aD()[1])
				if c<=0 or h<=c:return w,h,e,f
				if not d["beside_said"]:d["beside_said"]=True;API.SysMsg(E+": bag grid too tall to stack; bags go beside the doll.",l)
			return cJ(a,b)
		def cL():
			if r["beside"]:return((m,J)if r["left"]else(m+T+W,J))
			return m,J+aB()+W
		def bT(g,w,h,hole):
			c,b,d,n=hole;a=aW;s=[S(a+G)for G in range(9)];e,v,f,x,A,r,i,q,j=s;k=[]
			for y,z,t,u in((0,0,w,b),(0,b,c,h-b),(c+d,b,w-c-d,h-b),(c,b+n,d,h-b-n)):
				if t>0 and u>0:k.append(P(g,a+4,y,z,t,u))
			if all(bw[0]>0 and bw[1]>0 for bw in s):k+=[P(g,a+1,e[0],0,w-e[0]-f[0],v[1]),P(g,a+7,i[0],h-q[1],w-i[0]-j[0],q[1]),P(g,a+3,0,e[1],x[0],h-e[1]-i[1]),P(g,a+5,w-r[0],f[1],r[0],h-f[1]-j[1]),Y(g,a+0,0,0),Y(g,a+2,w-f[0],0),Y(g,a+6,0,h-i[1]),Y(g,a+8,w-j[0],h-j[1])]
			l,m=S(al)
			if l and m and al:
				for o,p in((0,0),(w-l,0),(0,h-m),(w-l,h-m)):
					if o<c+d and o+l>c and p<b+n and p+m>b:continue
					k.append(Y(g,al,o,p))
			with Kit.quiet:Kit._frame_parts[g]=[dh for dh in k if dh is not None]
		def ad():
			v,k["g"]=k["g"],None;bV();N=({},{});f={};Y=[];c=d["attached"];b=None;d.update({"px":m,"k":1.,"py":None,"strip_w":None,"pw":T,"col":None,"ph":aa,"rp":ak});x=d["fit"]if not d["minimized"]else None;ab=m
			if u(v):y,C=v.GetX(),v.GetY()
			else:y,C=Kit.load_pos(aS,(200,120),(bD,J+aB()+m))
			O=aA(H);d["paired"]=False
			if O is not None:y,C=O[0],O[1]
			if d["minimized"]:w,h=b3,b4;g=G.CreateGump(True,True);f["status"]=Kit.mini_bar(g,N,w,h,E,H,q("toggle_min"));A(f["status"],E+" & bags"if c is not None else E)
			else:
				w,h=bD,J+aB()+m;g=G.CreateGump(False,True)
				if x is not None:
					w,h=x;S=cE(y,C,w,h,d["pair"])if(c is not None and d["pair"])else None
					if S is not None:am=W//2;d["paired"]=True;(ac,d["px"],d["py"],ad,d["strip_w"],_h,ae,d["pw"],d["col"],d["ph"])=bS(w,h-am+m,False);b=S;h=b[1]+b[3]+m
					else:(ac,d["px"],d["py"],ad,d["strip_w"],b,ae,d["pw"],d["col"],d["ph"])=bS(w,h,c is not None)
					d["k"]=ac;d["rp"]=(d["ph"]-2*F-n)/float(aU-1);ab=ae[0]
					if b is not None:
						bT(g,w,h,b);c["dx"],c["dy"]=b[0],b[1]
						if S is None:d["room"]=(b[2],b[3]);d["room_fs"]=bl(b[2],b[3]);d["grew"]=(d["room_fs"]is not None and d["room_fs"][1]>b[3])
						aQ((b[2],b[3]));fs=d["room_fs"];bU(fs[0]if fs is not None else None)
					else:Z(g,w,h);aQ(None)
				elif c is not None and c.get("grid_wh"):gw,gh=c["grid_wh"];w,h,d["px"],b=cK(int(gw),int(gh));bT(g,w,h,b);c["dx"],c["dy"]=b[0],b[1]
				else:Z(g,w,h)
				if x is None:aQ(None)
				U=d["px"];af=None
				if c is not None:af=[("traps",I,"Traps","Pick the bags Trap and Untrap cast on",q("bag_traps")),("bags",I,"Slots","Put a bag in each slot",q("bag_mgr"))]
				a6(g,N,w,E,H,q("toggle_min"),q("to_bar"),q("settings"),extra=af);i=[];py=bi();pw,ph=d["pw"],d["ph"];i.append(z(g,U,py,pw,ph));i.append(Q(g,U,py,pw,ph,lambda*a:None,None,movable=not bh()));mx,my,mw,mh=bK();f["doll_bg"]=P(g,9274,mx,my,mw,mh,.35);i.append(f["doll_bg"]);f["doll_drop"]=Q(g,mx,my,mw,mh,q(("drop",0)),"Drop an item here to wear it",movable=True);i.append(f["doll_drop"])
				for K,(ah,an,ai,ao)in enumerate(aC):L,M=cC(K);i.extend(Kit.gold_box(g,L,M,n,n));l=G.CreateGumpColorBox(.01,"#000000");l.SetRect(L,M,n,n);ax(l,q(("drop",ah)));aj=ao+": drop an item to wear it";l.SetTooltip(aj);g.Add(l);V=e(g,ai,L+(n-o(ai))//2,M+n-b6,D);V.SetAcceptMouseInput(False);i.append(l);i.append(V);Y.append({"layer":ah,"name":an,"x":L,"y":M,"drop":l,"label":V,"serial":0,"ctrl":None,"raw":None,"tip":aj})
				cM(i)
				if x is not None:p,X,s=ad,d["strip_w"],ab
				else:p=(J+aa+B)if r["stats"]else None;X,s=T,U
				if p is not None:
					z(g,s,p,X,ag);Q(g,s,p,X,ag,lambda*a:None,None,movable=not bh())
					for K in range(3):f["stats%d"%(K+1)]=e(g,"",s+10,p+8+24*K,D)
					c0(g,f,s,p+56)
				elif d["col"]is not None:c1(g,f,d["col"])
			xy=a4(g,y,C,w,h,H,d["minimized"]and d["docked"],cB(g),bG,k,{"g":g,"c":f,"store":N,"slots":Y});bd(H,g,xy);al=t["hooks"]
			if al is not None:al["verify"]=not d["paired"]
			k["raw"]=Kit._raw_gump(g)if j.ok else None
			if c is not None:c["g"],c["raw"]=g,None
			b0();d.update({"sig":None,"doll_sig":None,"stats_at":0.,"stats_key":None,"doll_at":0.,"wbar":None});R(v)
		dg=None;t={"col_w":None,"bounds":{},"need":[],"redo":False,"order":[],"hooks":None}
		def aQ(room):
			if room is None:d["room"]=None;bU(None)
			if room==d.get("told_bags"):return
			d["told_bags"]=room;a=V("bag.fit")
			if a is not None:safe(lambda:a(*(room or(None,None))))
		def bU(pct):
			if pct==d["told_shrink"]:return
			d["told_shrink"]=pct;a=V("bag.shrink")
			if a is not None:safe(lambda:a(pct))
		def cM(ctrls):
			if abs(d["k"]-1.)<.001:return
			U()
			for a in ctrls:
				if a is not None:aN(a,flushed=True)
		def bV():
			for s in k["slots"]:
				if s["ctrl"]is not None:R(s["ctrl"]);s["ctrl"]=None
			k["slots"]=[];bW()
		def bW():
			for p in k["doll"]:R(p)
			k["doll"]=[]
		def bX():return "docked"if d["docked"]else("collapsed"if d["minimized"]else "open")
		def bY(name):
			b=d["layer_name"].get(name)
			if b is not None:
				try:return API.FindLayer(b)
				except Exception:return
			for c in(name,)+cj.get(name,()):
				try:a=API.FindLayer(c)
				except Exception:a=None
				if a:d["layer_name"][name]=c;return a
			return
		def cN(p,keep=None):
			c={}
			if j.ok and p is not None:
				try:
					i=cw
					for e in bz:
						a=p.FindItemByLayer(az(e))
						if a is None:continue
						f,b,h=int(a.Serial),int(a.Graphic),int(a.Hue)
						if keep is not None:keep[e]=a
						m=(f,b);g=i.get(m)
						if g is not None:c[e]=(f,b,h)+g;continue
						try:d=a.ItemData;g=(int(d.AnimID),bool(d.IsPartialHue),bool(d.IsContainer))
						except Exception:
							try:d=API.FindItem(f).GetItemData()
							except Exception:d=None
							if d is not None:g=(int(d.AnimID or 0),bool(d.IsPartialHue),bool(d.IsContainer))
							else:c[e]=(f,b,h,0,False,False);continue
						if len(i)>=cx:i.clear()
						i[m]=g;c[e]=(f,b,h)+g
					l=(int(p.Graphic),int(p.Hue),bool(p.IsFemale));return c,l
				except Exception:
					c={}
					if keep is not None:keep.clear()
			try:k=API.Player
			except Exception:k=None
			if not k:return c,None
			for e in bz:
				a=bY(bx[e])
				if not a:continue
				try:f,b,h=(int(a.Serial or 0),int(a.Graphic or 0),int(a.Hue or 0))
				except Exception:continue
				n,o,q=0,False,False
				try:
					d=a.GetItemData()
					if d is not None:n,o,q=(int(d.AnimID or 0),bool(d.IsPartialHue),bool(d.IsContainer))
				except Exception:pass
				c[e]=(f,b,h,n,o,q)
			try:b=int(k.Graphic or 400)
			except Exception:b=400
			try:r=int(k.Hue or 0)
			except Exception:r=0
			l=(b,r,b in cm);return c,l
		def cO(graphic,hue,b):
			if graphic==bB:return bA[bB],cn,co
			a=bA.get(graphic)
			if a is None:a=13 if b else 12
			return a,hue,0
		def cP(b,g,a,c):
			if j.m_animid is not None:
				try:
					if j.animid_n==4:d=[UInt16(b),UInt16(g),UInt16(a),bool(c)]
					else:d=[UInt16(b),UInt16(a),bool(c)]
					v=int(j.m_animid.Invoke(None,Array[Object](d)))
					if v>0:return v
				except Exception:j.m_animid=None
			if a==cf and b in ch:a=cg
			h,i=(bt,bs)if c else(bs,bt);e=a+h
			if S(e)==(0,0):
				f=a+i
				if S(f)!=(0,0):return f
			return e
		def cQ(layer,gfx,p=None):
			if j.m_covered is not None and j.ok and p is not None:
				with Kit.quiet:return bool(j.m_covered.Invoke(None,Array[Object]([p,az(layer)])))
			a=gfx.get(at);b=gfx.get(ah)
			if layer==aE:
				if gfx.get(au)is not None or b==5137:return True
				if b in(1299,1300)or a==1284:return True
			elif layer==ah:
				if gfx.get(au)is not None or a==1284:return True
				if b in(491,997,1003):
					c=gfx.get(aM)
					if c is not None and c not in(455,484):return True
					if a is not None and a!=553 and(a<=1255 or a>1259):return True
			elif layer==ar:
				if a is not None:return a!=0 and a not in bc
			elif layer==L:
				if a is not None and a!=0 and a not in bc:return True
				d=gfx.get(ar)
				if d is not None and d not in(5441,5442):
					if gfx.get(L)in(30762,30763):return True
			elif layer==X:return a is not None and a!=0 and a not in bc
			elif layer in(aH,ai):
				if a is not None:
					if a>12659:
						if a in(19357,30742):return True
					elif a<=9863:
						if a<9859:return 8270<=a<=8271
						return True
					elif a in(12217,12659):return True
			return False
		def cR(items):
			c=dict((i,p[1])for i,p in items.items());d=items.get(aI);a=by
			if d is not None:
				if c.get(at)in(41674,41675):a=cl
				elif d[5]:a=ck
			a=list(a);h=c.get(L)
			if h in(7174,7170,7172):
				e,b=a.index(ah),a.index(L)
				if e<b:a.pop(b);a.insert(e,L)
			f=c.get(X)
			if f in(5069,5084,5102):
				g,b=a.index(X),a.index(L)
				if g<b:a.pop(g);a.insert(b,X)
			if f in(5136,5143):a=[L if s==X else(X if s==L else s)for s in a]
			return a,c
		def bZ(gid,b):
			a,c=t["bounds"],t["order"]
			if gid not in a:c.append(gid)
			a[gid]=b
			while len(c)>cs:a.pop(c.pop(0),None)
			return b
		def cS(gid):
			g="pic"
			try:h=a0(lambda:Tex.gump_pixels(gid)if Tex.find()else None)
			except Exception:h=None
			if h is not None:
				g=None;d,w,i=h;T=16777216
				def e(part):return bool(part)and(max(part)>=T or min(part)<0)
				a=0
				while a<i and not e(d[a*w:(a+1)*w]):a+=1
				if a<i:
					b=i-1
					while b>a and not e(d[b*w:(b+1)*w]):b-=1
					j,k=a*w,(b+1)*w;c=0
					while c<w-1 and not e(d[j+c:k:w]):c+=1
					f=w-1
					while f>c and not e(d[j+f:k:w]):f-=1
					g=(c,a,f+1,b+1)
			return bZ(gid,g)
		def cT(gid):
			b=t["bounds"].get(gid,"need")
			if b=="need":
				if gid not in t["need"]:t["need"].append(gid)
				b="pic"
			if b!="pic":return b
			a,c=S(gid);return(0,0,a,c)if a>0 and c>0 else None
		def cU():return bool(t["need"])
		def cV(items,who,P=None):
			w=k["g"];bW()
			if w is None or who is None:return
			x,y,z=who;p=[];k["doll"]=p;l=[];Q,R,A=cO(x,y,z);l.append((Q,R,True,0,0))
			if A:l.append((A,y,True,0,0))
			T,V=cR(items)
			for o in T:
				B=items.get(o)
				if B is None:continue
				r,W,X,C,s,_c=B
				if cQ(o,V,P):continue
				if C==0 and j.m_animid is None:continue
				m=cP(x,W,C,z)
				if m<=0 or S(m)==(0,0):continue
				l.append((m,X&16383,s,0 if o in(ai,aq,ap)else r,o))
			a=b=1<<20;c=e=-(1<<20)
			for Y in l:
				n=cT(Y[0])
				if n is not None:a,b=min(a,n[0]),min(b,n[1]);c,e=max(c,n[2]),max(e,n[3])
			if c<=a or e<=b:a,b,c,e=0,0,bo,b7
			D=(c-a,e-b);f=d["k"];Z,my,mw,mh=bK();E,H=Z*f+av,my*f+av;I,t=max(1.,mw*f-2*av),max(1.,mh*f-2*av);PW=max(1.,(d["pw"]-2*F)*f-2*av);g=min(t/D[1],PW/D[0]);J=int(round(E+I/2.-g*(a+c)/2.));K=int(round(H+t/2.-g*(b+e)/2.));u=int(round((E+I/2.)/f-(a+c)/2.));v=int(round((H+t/2.)/f-(b+e)/2.));L=abs(g-1.)>.001;h=k["raw"];i=[-1]
			if j.ok and h is not None:
				try:
					U();M=ab(k["c"].get("doll_drop"))
					if M is not None:i[0]=h.Children.IndexOf(M)+1
				except Exception:i[0]=-1
			def O(a):
				if i[0]<=0:return False
				b=h.Children;a.Parent=h
				while b.Remove(a):pass
				b.Insert(min(i[0],b.Count),a);i[0]+=1;return True
			def aa(gid,b,c,serial):
				if j.DollPiece is None or h is None or i[0]<=0:return
				try:a=j.DollPiece(h,UInt32(int(serial)),UInt16(int(gid)),UInt16(int(b)),0,0,True)
				except Exception:j.DollPiece=None;return
				try:
					a.va_gid,a.va_k,a.va_down=int(gid),float(g),False;a.HighlightOnMouseOver=False;a.IsPartialHue=bool(c);bg(a,J,K)
					if L:a.ApplyScale(g,False,True,False)
					G.AddControlOnClick(a,q(("drop",0)))
					if not O(a):raise Exception("no place")
				except Exception:safe(a.Dispose);return
				return a
			def ac(gid,c,e,serial=0):
				if serial:
					b=aa(gid,c,e,serial)
					if b is not None:p.append(b);return
				a=G.CreateGumpPic(gid,u,v,c)if c else G.CreateGumpPic(gid,u,v);a.SetPos(u,v);b=None
				try:
					U();b=ab(a);bg(b,J,K)
					if L:b.ApplyScale(g,False,True,False)
				except Exception:b=None;aN(a)
				if e:f=ab(a);N(f if f is not None else a,"IsPartialHue",True)
				if serial:a.SetEntityTooltip(serial);ax(a,q(("drop",0)));Kit.hook_double(a,q(("use",serial)))
				else:a.SetAcceptMouseInput(False)
				d=False
				if b is not None:
					try:d=O(b)
					except Exception:d=False
				if not d:w.Add(a)
				p.append(a)
			for m,ad,s,r,ae in l:ac(m,ad,s,r)
		def cW(force=False):
			if d["minimized"]or k["g"]is None:return
			if t["redo"]and not t["need"]:t["redo"]=False;d["doll_sig"]=None
			b=time.time()
			if not force and d["sig"]is not None and d["doll_sig"]is not None and 0<=b-d["doll_at"]<cd:return
			d["doll_at"]=b;p=cy()if j.ok else None;c={};a,e=cN(p,c);f=tuple([a[h][0]if h in a else 0 for h in ci])
			if f!=d["sig"]:cY(f,p,c)
			g=(e,tuple(sorted((s,i[0],i[1],i[2])for s,i in a.items())))
			if g!=d["doll_sig"]:d["doll_sig"]=g;cV(a,e,p)
		def cX(s,item,c):
			h=k["g"]
			if s["ctrl"]is not None:R(s["ctrl"]);s["ctrl"]=None
			if item is None and c is None:N(s["label"],"IsVisible",True);ao(s["drop"],s["tip"]);return
			N(s["label"],"IsVisible",False);s["drop"].SetTooltip("")
			if j.ok and item is not None and k["raw"]is not None:
				try:
					i=(k["raw"],UInt32(int(item.Serial)),UInt16(int(item.DisplayedGraphic)),UInt16(int(item.Hue)),0,0);a=None
					if j.SlotItem is not None:
						try:a=j.SlotItem(*i)
						except Exception:j.SlotItem=None
					if a is None:a=j.ItemGump(*i)
					r=j.f_bounds.GetValue(a);l,m=int(r.Width),int(r.Height);f=min(1.,(n-6)/float(max(1,l)),(n-6)/float(max(1,m)));e=d["k"];bg(a,int(round((s["x"]+(n-l*f)/2.)*e)),int(round((s["y"]+(n-m*f)/2.)*e)))
					if abs(e*f-1.)>.001:
						try:a.ApplyScale(e*f,False,True,False)
						except Exception:aN(a,True)
					try:G.AddControlOnClick(a,q(("drop",s["layer"])))
					except Exception as g:safe(a.Dispose);raise g
					h.Add(a);s["ctrl"]=a;return
				except Exception as g:j.error="item control: %s"%g
			o=int(c.Serial)if c is not None else int(item.Serial);p=int(c.Graphic)if c is not None else int(item.DisplayedGraphic);b=G.CreateGumpItemPic(p,n-6,n-6);b.SetRect(s["x"]+3,s["y"]+3,n-6,n-6);aN(b);b.SetEntityTooltip(o);ax(b,q(("drop",s["layer"])));Kit.hook_double(b,q(("use",o)));h.Add(b);s["ctrl"]=b
		def cY(sig,p,got=None):
			b=k["slots"]
			if len(b)!=len(sig):return
			e=d["sig"]or(None,)*len(b)
			for i,s in enumerate(b):
				if sig[i]==e[i]:continue
				s["serial"]=sig[i];a=c=None
				if sig[i]:
					if j.ok and p is not None:
						a=got.get(s["layer"])if got else None
						if a is None:
							try:a=p.FindItemByLayer(az(s["layer"]))
							except Exception:a=None
					if a is None:c=bY(s["name"])
				cX(s,a,c)
			d["sig"]=sig
		def cZ(layer):
			if j.ok:
				h=bf()
				if h is None:return
				c,e,a=h
				if not e:API.SysMsg(E+": that can't be worn.",v);return
				if a not in bv and a>0:API.SysMsg(E+": that doesn't go in an equipment slot.",v);return
				try:
					w=bI();p=w.Player;b=p.FindItemByLayer(az(a))if a else None
					if b is not None and int(b.Serial)==c:b=None
					if b is None:j.m_equip.Invoke(None,Array[Object]([w,UInt32(int(p.Serial))]))
					else:j.m_swap.Invoke(None,Array[Object]([w,UInt32(int(p.Serial)),az(a),UInt32(int(b.Serial))]))
					d["sig"]=None
				except Exception as f:API.SysMsg(E+": couldn't equip that (%s)."%f,v)
				return
			c=aw()
			if c:API.EquipItem(c);d["sig"]=None
		c_=("Strength","Dexterity","Intelligence","Hits","HitsMax","Mana","ManaMax","Stamina","StaminaMax","Weight","WeightMax","Gold","Followers","FollowersMax","PhysicalResistance");af=10
		def c0(g,c,px,y):h=o("Weight 0000/0000");i=o("Gold 9,999,999   Followers 99/99");a=px+10+h+6;b=d["strip_w"]or T;j=b-(a-px)-10-i-14;f=max(bq,min(b9,j));a9(g,c,a,y,f,16);c["stats4"]=e(g,"",a+f+10,y,D);c["room"]=b-2*af;c["room3"]=h;c["room4"]=max(0,b-(a+f+10-px)-af)
		def c1(g,c,col):x,y,w,h=col;z(g,x,y,w,h);Q(g,x,y,w,h,lambda*a:None,None,movable=not bh());b=max(bQ,min(cF,(h-16-aP)//aO));d=y+max(8,(h-aO*b-aP)//2);c["scol"]=[e(g,"",x+af,d+f*b+(aP if f>=7 else 0),D)for f in range(aO)];c["room"]=w-2*af;a9(g,c,x+af,d+7*b-1,w-2*af,16)
		def b_(e,a,f):
			if a<=0 and f>0:a=int(cb+cc*f)
			b=(float(e)/a)if a>0 else-1.
			if b>=b8:
				if d["w_armed"]and aF("character.weight","Weight %d/%d (%d%%): nearly overloaded"%(e,a,int(b*100)),level="warn",who="weight")is not False:d["w_armed"]=False
			elif b>=0:d["w_armed"]=True
			g=k["c"].get("wfills")
			if not g or d["minimized"]:return
			c=Kit.weight_level(b,k["c"]["wbar_w"])
			if c==d["wbar"]:return
			d["wbar"]=c;Kit.weight_show(g,c[0],c[1])
		def c2():
			a=time.time()
			if 0<=a-d["w_at"]<bp:return
			d["w_at"]=a
			try:p=API.Player
			except Exception:p=None
			if not p:return
			try:b,c,e=int(p.Weight),int(p.WeightMax),int(p.Strength)
			except Exception:return
			b_(b,c,e)
		def c3():
			c=k["c"]
			if d["minimized"]or("stats1"not in c and "scol"not in c):return False
			g=time.time()
			if 0<=g-d["stats_at"]<bp:return True
			d["stats_at"]=g;p=HOST.me()
			if not p:return True
			v={};f=[]
			for h in c_:
				try:x=int(getattr(p,h))
				except Exception:x=0
				v[h]=x;f.append(x)
			a=c["room"];e=c.get("scol");i=c.get("stats1");b=d.get("stats_key")
			if b is None or b[0]!=f or b[1]is not e or b[2]is not i or b[3]!=(a,c.get("room3"),c.get("room4")):
				d["stats_key"]=(f,e,i,(a,c.get("room3"),c.get("room4")))
				if e is not None:
					for j,l in zip(e,("Str %d"%v["Strength"],"Dex %d"%v["Dexterity"],"Int %d"%v["Intelligence"],"HP %d/%d"%(v["Hits"],v["HitsMax"]),"Mana %d/%d"%(v["Mana"],v["ManaMax"]),"Stamina %d/%d"%(v["Stamina"],v["StaminaMax"]),"Weight %d/%d"%(v["Weight"],v["WeightMax"]),"Gold %s"%O(v["Gold"]),"Followers %d/%d"%(v["Followers"],v["FollowersMax"]),"AR %d"%v["PhysicalResistance"])):A(j,C(l,a))
				else:A(c["stats1"],C("Str %d   Dex %d   Int %d   AR %d"%(v["Strength"],v["Dexterity"],v["Intelligence"],v["PhysicalResistance"]),a));A(c["stats2"],C("HP %d/%d   Mana %d/%d   Stamina %d/%d"%(v["Hits"],v["HitsMax"],v["Mana"],v["ManaMax"],v["Stamina"],v["StaminaMax"]),a));A(c["stats3"],C("Weight %d/%d"%(v["Weight"],v["WeightMax"]),c["room3"]));A(c["stats4"],C("Gold %s   Followers %d/%d"%(O(v["Gold"]),v["Followers"],v["FollowersMax"]),c["room4"]))
			b_(v["Weight"],v["WeightMax"],v["Strength"]);return True
		def V(name):return HOST.services.get(name)
		def c4(cmd):
			if cmd=="show":q("show")()
			elif cmd=="dock":q("to_bar")()
		def c5():
			c=V("bag.attach");e=V("bag.grid_size");a=d["attached"];f=r["combine"]and c is not None and e is not None
			if a is None:
				if not f:return
				g,h=cL();a={"g":k["g"],"raw":None,"dx":g,"dy":h,"shown":not d["minimized"],"state":bX(),"grid_wh":None,"cmd":c4};d["attached"]=a
				try:c(a)
				except Exception as i:d["attached"]=None;API.SysMsg(E+": couldn't combine with Bags (%s)."%i,v);return
				ad();return
			if not f:c6();return
			b=safe(e);b=tuple(b)if b else None
			if b!=a["grid_wh"]:a["grid_wh"]=b;ad()
		def c6():
			b,d["attached"]=d["attached"],None;aQ(None);d["told_shrink"]=None
			if b is not None:
				a=V("bag.attach")
				if a is not None:safe(lambda:a(None))
			if k["g"]is not None and not d["shutting"]:ad()
		def b0():
			a=d["attached"]
			if a is not None:a["shown"]=not d["minimized"];a["state"]=bX()
		b1={"drop":cZ,"use":lambda serial:API.UseObject(serial),"follow":lambda serial:ay(serial,E)}
		def c7(w):return(("WINDOW",(("check","stats","Show your stats","Str / Dex / Int, HP, mana, stamina, weight, gold, followers: under the doll, or beside it in a zone"),("check","combine","Combine with Bags in one window","The Bags grid inside this window (unticked: two windows)"),("check","beside","Bags beside the doll (not under)","Combined: the grid beside the doll; one too tall to stack goes beside anyway"),("check","left","Bags on the left","Beside the doll: on its left (unticked: right)"),("note","Drop an item on a slot to wear it; drag it out to take it off.",{"ndy":4})),{"top":32,"sh":170}),)
		def c8(a,new):
			if k["g"]is not None:q("redraw")();HOST.poke()
		aR=Kit.Page(r,c7,bF,c8);bE()
		def b2():
			bE()
			if not safe(lambda:API.Player):d["wait_player"]=True;return
			d["wait_player"]=False
			if not j.tried:j.tried=True;cv()
			d.update({"shutting":False,"docked":False,"queue":[],"sig":None,"doll_sig":None,"attached":None,"beside_said":False,"fit":None,"k":1.,"py":None,"strip_w":None,"pw":T,"col":None,"ph":aa,"rp":ak,"told_bags":None,"pair":None,"pair_at":0.,"room":None,"room_fs":None,"told_shrink":None,"grew":False,"paired":False,"w_armed":True,"w_at":0.,"wbar":None,"minimized":bool(d["saved_min"]or aL(H))});aG("character.weight","Weight near the limit",ca);ad();a=Kit.dock_hooks(E,b5,d,k,q("redraw"));a.update({"fit":cD,"exact":True,"pieces_out":True,"verify":not d["paired"]});t["hooks"]=a;aJ(H,a)
			if not j.ok:API.SysMsg(E+": no client access (%s); slots show pictures and equip without swapping."%j.error,l)
		def c9():
			if d["wait_player"]:
				if safe(lambda:API.Player):b2()
				return
			if k["g"]is None:return
			if ae(k["store"],"close"):bG();R(k["g"]);return
			while d["queue"]:
				a=d["queue"].pop(0);g=a[0]if isinstance(a,tuple)else a
				if a=="show":d["minimized"],a=True,"toggle_min"
				if a=="redraw"and bf()is not None:d["redraw_due"]=True
				elif Kit.win_action(a,d,H,E,ad,aT):continue
				elif a in("bag_mgr","bag_traps"):
					h=V("bag.open_manager"if a=="bag_mgr"else "bag.open_traps")
					if h is not None:h()
				elif g in b1:b1[g](a[1])
			b0();c5()
			if k["g"]is None:return
			i=bf()is not None
			if d.get("redraw_due")and not i:d["redraw_due"]=False;ad();return
			if d["attached"]is not None and not i:
				e=time.time()
				if e-d["pair_at"]>=ce or e<d["pair_at"]:
					d["pair_at"]=e;j=bN()
					if j!=d["pair"]:
						d["pair"]=j
						if d["fit"]is not None:ad();return
					c=d["room"]
					if c is not None and d["fit"]is not None and not d["minimized"]:
						b=bk();l=(c,None if b is None else(round(b[0],1),round(b[1],1),b[2],b[3],b[4],b[5]))
						if l!=d.get("room_sig"):
							d["room_sig"]=l;f=bl(c[0],c[1])
							if f is not None and(f[0]!=d["told_shrink"]or(f[1]>c[1])!=d["grew"]):ad();return
			cW()
			if not c3():c2()
		def da():
			a=t["need"]
			if not a:return
			b=a[0]
			try:cS(b)
			except Exception:bZ(b,"pic")
			a.pop(0);t["redo"]=True
		def db():
			d["shutting"]=True;aK(H);a3(aS,k["g"]);ct();bF();b,d["attached"]=d["attached"],None
			if b is not None:
				a=V("bag.attach")
				if a is not None:safe(lambda:a(None))
			bV();g,k["g"]=k["g"],None;k["raw"]=None;R(g)
		return{"start":b2,"tick":c9,"stop":db,"client_tick":True,"config_height":aR.height,"build_config":aR.build,"poll_config":aR.poll,"config_closed":aR.closed,"thread_tick":da,"thread_wanted":cU}
	def bi():
		T="storage";U="Storage";aV="StorageIndex_settings";by="StorageIndex_pos";aW="StorageIndex_min";ak=300;a0=20000;bz=60;W=(.6,2.);a1=15.;a3=1.;bA=600.;bB=20;bC=.5;bD=40;bE=6000;bF=80;al=1500;a4=5.;an=10.;bG=30;bH=.4;a6=3.;ah=14;ap=ah*30;aJ=12;a7=40;bI={291:"Pack horse",292:"Pack llama",791:"Giant beetle"};a9=(8198,7774);bJ="_storage_index_%s.txt";bK="# Virtue Assistant Storage Index 1";aK="StorageIndex_favs";bb="StorageIndex_account";aL=420;bL,bM=260,46;Y=20;bN=3708;bc="Alt+click: auto-follow (again to stop)";g=K;IW=aL-2*g;Z=g+30+B;bd=64;ar=Z+bd+B;be=12+ah*Y+8;bO=ar+be+B;bf=30;at=bO+bf+g;bg=((60,1,"just now"),(3600,60,"%dm ago"),(86400,3600,"%dh ago"),(172800,86400,"%d day ago"),(0,86400,"%d days ago"));G={"bank":True,"ground":True,"pack":True,"days":bz};h=[];cv=dict(G);c={"shutting":True,"minimized":False,"docked":False,"queue":[],"active":False,"hooked":False};n={"g":None,"c":{},"store":({},{}),"rows":[]};aa={"wipe_at":0.};aM,R,cw=am(c,U);b={"recs":{},"tombs":{},"ver":0,"dirty":False,"dirty_at":0.,"loaded":False,"path":None,"mtime":None,"err":"","unread":False};d={"ver":-1,"keys":{},"places":{},"items":0,"chars":0};a={"query":"","seen_text":None,"changed_at":0.,"page":0,"rows":[],"sel":None,"naming":None,"forget_arm":(None,0.),"status":"","status_hue":l,"status_at":0.,"dirty":True,"built_for":None,"live":{},"live_at":0.,"live_ver":0,"live_sig":None,"data":[],"prev":[],"last_read":("",0.),"iw":IW};j={};r={"q":[],"n":0};au={"n":0};ad=[];aw={};ag={};S=set();ai={};L=[];ax={"key":None,"stats":[]};az={"key":None,"by":{}};bh=re.compile(r"%[^%]*%|%s")
		def N(s):return str(s or "").replace("|","/").replace("\r"," ").replace("\n"," ").strip()
		def bP(text):
			h=0x811C9DC5
			for a in text:h=((h^ord(a))*16777619)&0xFFFFFFFF
			return "%08x"%h
		def bQ(it,graphic):
			n=aw.get(graphic)
			if n is None:
				try:d=it.GetItemData();n=bh.sub("",str(d.Name or "")).strip()if d is not None else ""
				except Exception:n=""
				if len(aw)>3000:aw.clear()
				aw[graphic]=n
			return n
		def aA(it,graphic,amount):
			try:n=str(it.Name or "")
			except Exception:n=""
			if "%"in n:n=bh.sub("",n)
			n=n.strip()
			if amount>1:
				a=str(amount)
				if n.startswith(a+" "):n=n[len(a)+1:].strip()
			if not n:n=bQ(it,graphic)or("item 0x%04X"%graphic)
			n=N(n);return n[:1].upper()+n[1:]
		def aB(text):
			a=[]
			for t in str(text or "").split(","):
				t=t.strip().lower()
				if not t:continue
				g=None
				try:
					if t.startswith("0x")and len(t)>2:g=int(t,16)
					elif t.isdigit()and len(t)>=3:g=int(t)
				except ValueError:g=None
				a.append(("g",g)if g is not None else("n",t))
			return a
		def aD(a,key):
			g,b=key[0],key[2]
			for c,v in a:
				if c=="g":
					if g==v:return True
				elif v in b:return True
			return False
		bi={"days":(1,3650)}
		def bj():aZ(aV,";",G,bi)
		def bR():a_(aV,";",G,("bank","ground","pack","days"),bi)
		def bS():
			b=ac(aK,"");del h[:]
			if not b:h.extend([[f,"0x%04X"%i]for f,i in sorted(aU.values())]+[["Bandages","0x0E21"]]);return
			if b=="-":return
			for d in b.split(";"):
				if "="not in d:continue
				c,a=d.split("=",1);c,a=c.strip(),a.strip()
				if a and len(h)<aJ:h.append([c or a,a])
		def bk():
			if not h:M(aK,"-");return
			M(aK,";".join("%s=%s"%(f.replace(";",",").replace("=","-"),i.replace(";",","))for f,i in h))
		def bT():
			with Kit.quiet:
				Typing._find();b=Typing.prof;a=Typing._get(None,"CurrentProfile",b)if b is not None else None;c=Typing._get(a,"Username")if a is not None else None
				if c:e=Typing._get(a,"ServerName")or "";return bP(("%s|%s"%(e,c)).lower())
			try:
				d=API.PersistentVar.Account;v=str(API.GetPersistentVar(bb,"",d)or "")
				if not v:import random;v="a%07x"%random.randint(0,0xFFFFFFF);API.SavePersistentVar(bb,v,d)
				return "".join(f for f in v if f.isalnum())[:16]or "account"
			except Exception:return "account"
		def aN(serial):return{"s":serial,"parent":0,"root":serial,"kind":"bag","cs":0,"cname":"","label":"","custom":"","facet":0,"x":0,"y":0,"seen":0.,"mob":0,"plabel":"","stub":False,"items":{}}
		def aO(text):
			b,d={},{}
			for a in text.split("\n"):
				a=a.rstrip("\r")
				if not a or a.startswith("#"):continue
				p=a.split("|")
				try:
					if p[0]=="C"and len(p)>=15:s=int(p[1]);r=aN(s);r.update({"parent":int(p[2]),"root":int(p[3]),"kind":p[4],"cs":int(p[5]),"cname":p[6],"label":p[7],"custom":p[8],"facet":int(p[9]),"x":int(p[10]),"y":int(p[11]),"seen":float(p[12]),"mob":int(p[13]),"plabel":p[14],"stub":len(p)>15 and p[15]=="1"});b[s]=r
					elif p[0]=="I"and len(p)>=6:
						r=b.get(int(p[1]));c=int(p[4])
						if r is not None and c>0:
							e=p[5];f=(int(p[2]),int(p[3]),e.lower());g=r["items"].get(f)
							if g is None:r["items"][f]=[e,c]
							else:g[1]+=c
					elif p[0]=="D"and len(p)>=3:d[int(p[1])]=float(p[2])
				except(ValueError,IndexError):continue
			return b,d
		def bU():
			a=[bK]
			for s,r in b["recs"].items():
				a.append("C|%d|%d|%d|%s|%d|%s|%s|%s|%d|%d|%d|%d|%d|%s|%d"%(s,r["parent"],r["root"],r["kind"],r["cs"],N(r["cname"]),N(r["label"]),N(r["custom"]),r["facet"],r["x"],r["y"],int(r["seen"]),r["mob"],N(r["plabel"]),1 if r["stub"]else 0))
				for c,e in r["items"].items():a.append("I|%d|%d|%d|%d|%s"%(s,c[0],c[1],e[1],N(e[0])))
			for s,t in b["tombs"].items():a.append("D|%d|%d"%(s,int(t)))
			return "\n".join(a)+"\n"
		def aP(path):return Kit.read_merge(path)
		def bV(path,text):
			try:return ba(path,text)
			except Exception as a:b["err"]=str(a)[:60];return False
		def aE(path):return safe(lambda:os.path.getmtime(path))
		def aQ(recs,tombs):
			d=False;c=b["recs"];e=time.time()-G["days"]*86400.
			for s,t in tombs.items():
				if t>b["tombs"].get(s,0.):b["tombs"][s]=t
			for s,r in recs.items():
				if r["seen"]<e:continue
				a=c.get(s)
				if a is None or r["seen"]>a["seen"]:
					if a is not None and a["custom"]and not r["custom"]:r["custom"]=a["custom"]
					c[s]=r;ag.pop(s,None);d=True
				elif r["custom"]and not a["custom"]:a["custom"]=r["custom"];d=True
			for s in[f for f in c if f in b["tombs"]and c[f]["seen"]<=b["tombs"][f]]:del c[s];d=True
			return d
		def aF():
			h=time.time();c=b["recs"];j=h-G["days"]*86400.;k=h-bG*86400.
			for s in[p for p,q in b["tombs"].items()if q<k]:del b["tombs"][s]
			if len(b["tombs"])>4*ak:
				for s,l in sorted(b["tombs"].items(),key=lambda a:a[1])[:len(b["tombs"])-4*ak]:del b["tombs"][s]
			a={}
			for s,r in c.items():
				g=a.get(r["root"])
				if g is None:g=a[r["root"]]=[0.,[],0]
				g[0]=max(g[0],r["seen"]);g[1].append(s);g[2]+=len(r["items"])
			d=False
			for i in[t for t,w in a.items()if w[0]<j]:
				for s in a.pop(i)[1]:c.pop(s,None)
				d=True
			e=len(c);f=sum(x[2]for x in a.values())
			if e>ak or f>a0:
				for i,g in sorted(a.items(),key=lambda a:a[1][0]):
					if e<=ak and f<=a0:break
					for s in g[1]:c.pop(s,None)
					e-=len(g[1]);f-=g[2];d=True
			return d
		def bl():
			a=b["path"]
			if not a:return
			c=aP(a);b["mtime"]=aE(a);b["unread"]=c is None
			if c:aQ(*aO(c))
			aF();b["loaded"]=True;b["ver"]+=1
		def bm():
			a=b["path"]
			if not a:return
			c=aE(a)
			if b["unread"]or(c is not None and c!=b["mtime"]):
				d=aP(a)
				if d is None:b["err"]="couldn't read the index file";return
				b["unread"]=False;b["mtime"]=c
				if d and aQ(*aO(d)):b["ver"]+=1
			if aF():b["ver"]+=1
			if bV(a,bU()):b["mtime"]=aE(a);b["dirty"]=False;b["err"]=""
		def bW():
			d=b["path"];a=aE(d)
			if a is None or a==b["mtime"]:return
			c=aP(d)
			if c is None:return
			b["mtime"]=a;b["unread"]=False
			if c and aQ(*aO(c))|aF():b["ver"]+=1
		def aG():
			b["ver"]+=1
			if not b["dirty"]:b["dirty"]=True;b["dirty_at"]=time.time()
		def aj(res):r["n"]+=1;res["n"]=r["n"];r["q"]=r["q"]+[res]
		def aR():n=au["n"];return[f for f in r["q"]if f["n"]>n]
		def bn():q=r["q"];return bool(q)and q[-1]["n"]>au["n"]
		def bo():
			for a in aR():au["n"]=a["n"];bY(a)
		def bX(it):
			a,b=it,0
			while b<12:
				c=int(a.Container or 0)
				if c==0 or c<0x40000000:break
				e=API.FindItem(c)
				if e is None:return
				a,b=e,b+1
			else:return
			d=int(a.Container or 0);h=int(a.Serial)
			if int(a.Graphic)in a9 or int(it.Graphic)in a9:return
			if d==0:
				if a.IsCorpse:return
				return("chest",a,None)if G["ground"]else None
			f=API.Player
			if f is None:return
			if d==int(f.Serial):g=int(API.Bank or 0);return("bank",a,None)if g and h==g and G["bank"]else None
			m=API.FindMobile(d);return("pack",a,m)if m is not None and bool(m.IsRenamable)and G["pack"]else None
		def bp(serial,final):
			d=API.FindItem(serial)
			if d is None:return
			s=bX(d)
			if s is None:return
			k,a,g=s;l=API.Player
			if l is None:return
			t=API.ItemsInContainer(serial,True)or[];q,n=0,0;h=[]
			for x in t:
				n+=1
				if n>al:break
				try:c,i,u=int(x.Serial),x.Amount,int(x.Container);q=(q*31+c+7*int(i or 0)+13*u)&0xFFFFFFFFFFFF
				except Exception:h.append(None);continue
				h.append((c,i,u))
			v=(q,n);b_(serial,h)
			if ag.get(serial)==v and serial in b["recs"]:
				if len(r["q"])<40:aj({"serial":serial,"same":True,"at":time.time()})
				return True
			E,m=int(l.Serial),str(l.Name or "");F=int(API.GetMap()or 0);e={serial:[]};w,y={},{};n=0;z=False
			for x in t:
				n+=1
				if n>al:z=True;break
				try:
					A=h[n-1]
					if A is not None:c,i,j=A;f=max(1,int(i or 1))
					else:c=int(x.Serial);j=int(x.Container);f=None
					B=int(x.Graphic);G=int(x.Hue)
					if f is None:f=max(1,int(x.Amount or 1))
					C=aA(x,B,f)
					if bool(x.IsContainer):w[c]=j;y[c]=C
				except Exception:continue
				o=e.get(j)
				if o is None:o=e[j]=[]
				o.append((B,G,f,C))
			if not e[serial]and not final and len(e)==1:return False
			H=int(a.Serial);D=aA(a,int(a.Graphic),1)
			if k=="bank":p=("Bank box (%s)"%m)if m else "Bank box"
			elif k=="chest":p="%s at %d, %d"%(D or "Chest",int(a.X),int(a.Y))
			else:I=int(g.Graphic or 0);p=("%s %s"%(bI.get(I,"Pack animal"),str(g.Name or ""))).strip()
			J={"serial":serial,"parent":int(d.Container or 0),"kind":k,"root":H,"label":p,"top_name":D,"own_name":aA(d,int(d.Graphic),1),"cs":E,"cname":m,"facet":F,"x":int(a.X),"y":int(a.Y),"mob":int(g.Serial)if g is not None else 0,"by":e,"parents":w,"names":y,"capped":z,"at":time.time()}
			if len(r["q"])<40:
				aj(J)
				if len(ag)>200:ag.clear()
				ag[serial]=v
			return True
		def bq(recs,s,b):
			a=0
			while s and a<14:
				if s==b:return True
				r=recs.get(s)
				if r is None:return False
				s,a=r["parent"],a+1
			return False
		def bY(res):
			e=b["recs"];l=res.get("op")
			if l=="forget":cj(res["root"]);return
			if l=="name":
				r=e.get(res["root"])
				if r is not None:r["custom"]=res["text"];aG()
				return
			if l=="wipe":
				f=time.time()
				for s in list(e):b["tombs"][s]=f
				e.clear();aG();return
			if res.get("same"):
				i,f,c=res["serial"],res["at"],None
				for s,r in e.items():
					if bq(e,s,i):r["seen"]=f;c=r["root"]
				p=d["places"].get(c)if c is not None else None
				if p is not None:p["seen"]=f;a["dirty"]=True
				return
			i,c,f=res["serial"],res["root"],res["at"]
			if i==c:k=[cx for cx,cy in e.items()if cy["root"]==c or cx==c]
			else:k=[cz for cz in e if bq(e,cz,i)]
			m={"kind":res["kind"],"root":c,"cs":res["cs"],"cname":res["cname"],"facet":res["facet"],"x":res["x"],"y":res["y"],"mob":res["mob"],"plabel":res["label"]};n=res["parents"];j=set()
			for s in k:
				if s not in res["by"]and s!=c and(s in n or res["capped"]):j.add(s)
			o=True
			while o:
				o=False
				for s in k:
					if s not in j and s not in res["by"]and s!=c and e[s]["parent"]in j:j.add(s);o=True
			q={};t=[]
			for s in k:
				r=e[s]
				if s in j:
					r.update(m);r["kind"]="bag"
					if s in n:r["parent"]=n[s]
					continue
				if s in res["by"]and r["custom"]:q[s]=r["custom"]
				elif s not in res["by"]:t.append(s)
				del e[s]
			for s in t:b["tombs"][s]=f
			if i!=c:
				g=e.get(c)
				if g is None:g=e[c]=aN(c);g["stub"]=True
				g.update(m);g["parent"]=0;g["label"]=res["label"]
				if g["stub"]:g["seen"]=max(g["seen"],f)
			for h,z in res["by"].items():
				r=aN(h);r.update(m);r["custom"]=q.get(h,"");r["seen"]=f
				if h==c:r["parent"],r["label"]=0,res["label"]
				elif h==i:r["kind"],r["parent"],r["label"]="bag",res["parent"],res["own_name"]
				else:r["kind"],r["parent"]="bag",res["parents"].get(h,0);r["label"]=res["names"].get(h,"Bag")
				u=r["items"]
				for A,B,v,w in z:
					x=(A,B,w.lower());y=u.get(x)
					if y is None:u[x]=[w,v]
					else:y[1]+=v
				e[h]=r;b["tombs"].pop(h,None)
			b["tombs"].pop(c,None);aF();aG();a["last_read"]=(res["label"],f)
		def bZ(*b):
			if not c["active"]:return
			for a in reversed(b):
				s=None
				try:s=int(a)
				except Exception:
					try:s=int(a.Serial)
					except Exception:s=None
				if s and s>=0x40000000:
					if len(ad)<40:ad.append(s)
					return
		def b_(root,first):
			if len(ai)>bE or len(L)>bF:
				a=set(i for i in L if i not in j)or set(L[:max(1,len(L)//2)])
				for k in[p for p,q in ai.items()if q in a]:del ai[k]
				L[:]=[s for s in L if s not in a]
			if root in L:L.remove(root)
			L.append(root)
			for f in first:
				if f is not None:ai[f[0]]=root
		def br(*d):
			if not c["active"]or not j or len(S)>=bD:return
			for a in d:
				try:s,e=int(a.Serial),int(a.Container)
				except Exception:continue
				for k in(e,s):
					b=k if k in j else ai.get(k)
					if b is not None:S.add(b)
				return
		def b0():aC(c,"hooked",("OnOpenContainer",bZ),("OnItemCreated",br),("OnItemUpdated",br))
		def b1(serial):
			a=time.time();w=j.get(serial)
			if w is None and len(j)>=bB:b=min(j,key=lambda k:j[k][0]);j.pop(b,None)
			j[serial]=[a,a+W[0],0]
		def b2(now):
			if not j:
				if S:S.clear()
				return
			if S:
				d=list(S);S.difference_update(d);e=now+bC
				for s in d:
					w=j.get(s)
					if w is not None and w[2]>=len(W)and w[1]>e:w[1]=e
			f=now>=c.get("check_at",0.)or c.get("check_at",0.)-now>a3
			if f:c["check_at"]=now+a3
			for a in list(j):
				w=j[a];g=False
				if f and w[2]>=len(W):
					b=API.FindItem(a);g=b is None or not bool(b.Opened)
					if b is None:j.pop(a,None);continue
				if g or now-w[0]>bA:bp(a,True);j.pop(a,None);continue
				if now<w[1]and w[1]-now<=a1+1.:continue
				h=bp(a,w[2]>=len(W)-1)
				if h is None:j.pop(a,None);continue
				w[2]+=1;w[1]=w[0]+W[w[2]]if w[2]<len(W)else now+a1
		def b3():
			f,g={},{};h=b["recs"];i=set();n=0
			for s,r in h.items():
				e=r["root"];p=g.get(e)
				if p is None:j=h.get(e);c=j if j is not None else r;o=c["custom"]or c["label"]or r["plabel"]or "A container";p=g[e]={"label":o,"seen":0.,"kind":c["kind"],"mob":c["mob"],"cname":c["cname"],"facet":c["facet"],"x":c["x"],"y":c["y"]}
				if r["seen"]>p["seen"]:p["seen"]=r["seen"]
				if r["cname"]:i.add(r["cname"])
				for l,m in r["items"].items():
					n+=1;k=f.get(l)
					if k is None:k=f[l]=[m[0],{}]
					k[1][e]=k[1].get(e,0)+m[1]
			d.update({"ver":b["ver"],"keys":f,"places":g,"items":n,"chars":len(i)});a["dirty"]=True
		def bs():
			b=(d["ver"],tuple(p for q,p in h))
			if ax["key"]!=b:
				c=[];i=d["keys"]
				for n,j in h:
					k=aB(j);e,a=0,{}
					for l,m in i.items():
						if aD(k,l):
							for f,g in m[1].items():a[f]=a.get(f,0)+g;e+=g
					c.append((e,a))
				ax["key"],ax["stats"]=b,c
			return ax["stats"]
		def bt(q):
			c=(d["ver"],q.lower())
			if az["key"]!=c:
				g=aB(q);a={}
				for k,e in d["keys"].items():
					if aD(g,k):
						for f,h in e[1].items():
							b=a.get(f)
							if b is None:b=a[f]={}
							b[k]=(e[0],h)
				az["key"],az["by"]=c,a
			return az["by"]
		def b4(i):
			def a(*b):a=Follow.alt_held();R.add(("row",i,a,time.time()),dup=True,cap=20)
			return a
		def aS():
			A=P.slot if V(T)else None;w,p=A or(aL,at);C=P.rows(Y,at-ah*Y,ah,4);d,q=w-2*g,p-(at-be);r=ar+q+B;a["iw"]=d;b,f,k=P.begin(bL if c["minimized"]else w,bM if c["minimized"]else p);i=[]
			if not c["minimized"]:
				P.frame(b);z(b,g,Z,d,bd);s=35+o("Add favourite");e(b,"Find:",g+10,Z+12,D);t=g+16+o("Find:");E=d-(t-g)-s-22;k["box"]=ao(av(b,a["query"],t,Z+9,E,numbers=False),"Part of a name, or a graphic (0x0F88); commas for several; empty: favourites");m(b,f,"fav",X,g+d-s-6,Z+8,"Add favourite","Add the Find box text to your favourites",on_click=R("fav"));h=Z+36;n=g+10;m(b,f,"name",X,n,h,"Name","Name the picked place: type it in the Find box, then click Name again",on_click=R("name"));n+=35+o("Name")+12;m(b,f,"forget",H,n,h,"Forget","Drop the picked place and its bags from the index (click twice)",on_click=R("forget"));F=35+o("Next");u=g+d-F-6;m(b,f,"next",I,u,h,"Next","Next page",on_click=R("next"));v=u-12-(35+o("Prev"));m(b,f,"prev",I,v,h,"Prev","Previous page",on_click=R("prev"));k["page"]=e(b,"",v-50,h+3,l);z(b,g,ar,d,q)
				for x in range(C):j=ar+8+x*Y;y={"l":e(b,"",g+10,j,D),"r":e(b,"",g+d-60,j,l),"lx":g+10,"rx":g+d-60,"tip":"","y":j};y["c"]=Q(b,g+4,j-2,d-8,Y,b4(x));i.append(y)
				z(b,g,r,d,bf);k["status"]=e(b,"",g+10,r+7,l)
			a.update({"data":[None]*len(i),"prev":[(None,0.)]*len(i),"seen_text":None,"built_for":None,"dirty":True});P.end(b,{"rows":i});bv(time.time())
		P=Kit.Window(T,U,c,n,aS,by,aW,(240,160),icon=bN,cleanup=aM,clear={"rows":[]})
		def bu():return n["g"]is not None and not c["minimized"]and not c["docked"]
		def u(text,hue=None):a["status"]=text;a["status_hue"]=l if hue is None else hue;a["status_at"]=time.time()
		def b5():
			n=len(d["places"])
			if not b["loaded"]:return "Reading the index"
			if b["err"]:return "Index file: %s"%b["err"]
			c,t=a["last_read"];s="%s noted"%F(n,"place")
			if d["chars"]>1:s+=" on %d characters"%d["chars"]
			if c:s+="; last read %s"%c
			return s
		def b6(p,root):
			a=""
			if p["kind"]=="chest":a=" (facet %d, %d, %d)"%(p["facet"],p["x"],p["y"])
			c=(" by %s"%p["cname"])if p["cname"]else "";b="%s\nSeen%s %s%s\nClick to pick it (then Name or Forget)"%(p["label"],c,Kit.ago(time.time()-p["seen"],bg),a)
			if p["mob"]:b+="\n"+bc
			return b
		def b7(now):
			b=[];B=a["live"];C=d["places"];q=a["query"]
			if not q:
				if not h:return[("No favourites yet: type a name, then click Add favourite.","",l,0,"",None)]
				b.append(("FAVOURITES  (click one to see where)","",E,0,"Totals across the account: every place noted, and your backpack now",None));G=bs()
				for H,(I,w)in enumerate(h):
					x=aB(w);i,K=G[H]if H<len(G)else(0,{});c=sum(cy[1]for cx,cy in B.items()if aD(x,cx));i+=c;r=len(K)+(1 if c else 0);s=[]
					if c:s.append("On you now: %s"%O(c))
					for e,f in sorted(K.items(),key=lambda a:-a[1])[:10]:p=C.get(e);s.append("%s: %s"%(p["label"]if p else "?",O(f)))
					t="%s (%s)\n%s\nClick to see where"%(I,w,"\n".join(s)if s else "None noted");b.append((I,("%s in %s"%(O(i),F(r,"place")))if i else "none",D,0,t,("fav",w)))
				return b
			x=aB(q);y=bt(q);c=dict((cz,(cA[0],cA[1]))for cz,cA in B.items()if aD(x,cz));r=len(y)+(1 if c else 0)
			if not r:return[("Nothing noted holds \"%s\"."%q,"",l,0,"Open the container it is in once (bank box, chest, pack animal) and it is noted",None)]
			z,j={},{}
			for e,u in y.items():
				L=0
				for A,v in u.items():L+=v[1];j[A]=v[0]
				z[e]=L
			i=sum(z.values())+sum(cB for cC,cB in c.values())
			for A,v in c.items():j[A]=v[0]
			N=list(j.values())[0]if len(j)==1 else "%d kinds"%len(j);b.append((N,"%s in %s"%(O(i),F(r,"place")),E,0,"Everything noted that matches \"%s\""%q,None));g=0
			if c:
				M=str(safe(lambda:API.Player.Name,"")or "");b.append(("Backpack%s"%((" (%s)"%M)if M else ""),"on you now",E,0,"Your backpack and the bags in it, right now",None));k=sorted(c.items(),key=lambda a:-a[1][1]);m=max(0,ap-len(b));g+=max(0,len(k)-m)
				for n,(o,f)in k[:m]:b.append((o,O(f),D,14,"%s x%s on you (graphic 0x%04X, hue %d)"%(o,O(f),n[0],n[1]),None))
			P=sorted(y.items(),key=lambda a:-z[a[0]])
			for e,u in P:
				p=C.get(e)
				if p is None:continue
				if len(b)>=ap:g+=1+len(u);continue
				Q=J if a["sel"]==e else E;b.append((p["label"],"seen %s"%Kit.ago(now-p["seen"],bg),Q,0,b6(p,e),("place",e,p["mob"],True)));R=("place",e,p["mob"],False);k=sorted(u.items(),key=lambda a:-a[1][1]);m=max(0,ap-len(b));g+=max(0,len(k)-m)
				for n,(o,f)in k[:m]:
					t="%s x%s in %s (graphic 0x%04X, hue %d)\nClick to pick this place"%(o,O(f),p["label"],n[0],n[1])
					if p["mob"]:t+="\n"+bc
					b.append((o,O(f),D,14,t,R))
			if g:b.append(("%s more line%s: type more of the name"%(O(g),""if g==1 else "s"),"",l,0,"A search lists %d lines at most; the total above counts them all"%ap,None))
			return b
		def bv(now):
			k=n["g"]
			if k is None or c["docked"]:return
			i=n["c"]
			if c["minimized"]:m=len(d["places"]);a["status_key"]=None;A(i.get("status"),U+": "+("%s noted"%F(m,"place")if b["loaded"]else "reading the index"),l);return
			e=(a["query"],d["ver"],a["live_ver"],a["sel"],a["page"],int(now//30))
			if a["dirty"]or e!=a["built_for"]:
				a["dirty"]=False;a["built_for"]=e;a["rows"]=b7(now);f=bw()
				if a["page"]>=f:a["page"]=f-1;a["built_for"]=(e[0],e[1],e[2],e[3],a["page"],e[5])
				b8(now,f)
			if(a["status"]and a["naming"]is None and not 0<=now-a["status_at"]<=8.):a["status"]=""
			g=i.get("status");j=(g,a["status"],a["status_hue"],b["loaded"],b["err"],len(d["places"]),d["chars"],a["last_read"]);h=a.get("status_key")
			if h is not None and h[0]is g and h[1:]==j[1:]:return
			a["status_key"]=j;A(g,C(a["status"]or b5(),a["iw"]-20),a["status_hue"]if a["status"]else l)
		def b8(now,pages):
			k=n["rows"];t=a["page"]*len(k);e,u=a["data"],a["prev"];m=g+a["iw"]-10
			for i,r in enumerate(k):
				o=t+i
				if o<len(a["rows"]):f,b,p,q,c,h=a["rows"][o]
				else:f,b,p,q,c,h="","",D,0,"",None
				s=a5(b)if b else 0;d=g+10+q;v=m-d-(s+8 if b else 0);A(r["l"],C(f,v)if f else "",p);A(r["r"],b,l)
				if d!=r["lx"]:r["lx"]=d;a8(r["l"],d,r["y"])
				j=m-s
				if b and j!=r["rx"]:r["rx"]=j;a8(r["r"],j,r["y"])
				if c!=r["tip"]:r["tip"]=c;r["c"].SetTooltip(c)
				if h!=e[i]:u[i]=(e[i],now);e[i]=h
			w=n["c"];A(w.get("page"),"%d / %d"%(a["page"]+1,pages)if pages>1 else "",l)
		def b9(now):
			b=n["c"].get("box")
			if b is None:return
			t=str(b.Text or "")
			if t!=a["seen_text"]:
				if a["seen_text"]is not None:a["changed_at"]=now
				a["seen_text"]=t;return
			if a["changed_at"]and(now-a["changed_at"]>=bH or now<a["changed_at"]):
				a["changed_at"]=0.
				if a["naming"]is not None:return
				q=t.strip()
				if q.lower()!=a["query"].lower():a["query"]=q;a["page"]=0;a["dirty"]=True
		def aH(text):
			b=n["c"].get("box");a["seen_text"]=text;a["changed_at"]=0.
			if b is not None:b.SetText(text)
		def ca(now):
			if not bu():return
			if now<a["live_at"]and a["live_at"]-now<=a6:return
			a["live_at"]=now+a6;b={};c=aq(True,1.);q,n=0,0
			for x in c:
				n+=1
				if n>al:break
				try:q=(q*31+int(x.Serial)+7*int(x.Amount or 0)+13*int(x.Container))&0xFFFFFFFFFFFF
				except Exception:continue
			if(q,n)==a["live_sig"]:return
			a["live_sig"]=(q,n)
			if c:
				n=0
				for x in c:
					n+=1
					if n>al:break
					try:g,h=int(x.Graphic),int(x.Hue);d=max(1,int(x.Amount or 1));e=aA(x,g,d)
					except Exception:continue
					k=(g,h,e.lower());f=b.get(k)
					if f is None:b[k]=[e,d]
					else:f[1]+=d
			if b!=a["live"]:a["live"]=b;a["live_ver"]+=1
		def cb(i,t):
			if i>=len(a["data"]):return
			c,b=a["prev"][i];return c if b and(b>=t or t-b<.15)else a["data"][i]
		def aT():
			if a["naming"]is not None:a["naming"]=None;aH(a["query"])
		def cc(action,now):
			if c["minimized"]or c["docked"]:c["minimized"]=c["docked"]=False;HOST.dock_forget(T);a2(aW,False);aS()
			safe(lambda:ab(n["g"]).BringOnTop())
		def cd(action,now):ay(action[1],U)
		def ce(action,now):
			e,i,c,t=action;b=cb(i,t)
			if b is None:return
			if c:
				if len(b)>2 and b[2]:ay(b[2],U)
				return
			aT()
			if b[0]=="fav":a["query"]=b[1];a["page"]=0;aH(b[1]);u("")
			elif b[0]=="place":a["sel"]=None if(b[3]and a["sel"]==b[1])else b[1];p=d["places"].get(a["sel"])if a["sel"]else None;u(("Picked: %s"%p["label"])if p else "")
			a["dirty"]=True
		def cf(action,now):
			aT();q=a["query"]or(a["seen_text"]or "").strip()
			if not q:u("Type what to look for first (a name, or a graphic like 0x0F88).",v)
			elif any(f.lower()==q.lower()for i,f in h):u("\"%s\" is already a favourite."%q)
			elif len(h)>=aJ:u("%d favourites at most: take one off on the settings page."%aJ,v)
			else:h.append([N(q)[:a7],N(q)]);bk();af(T);u("Added \"%s\" to the favourites."%q,J)
			a["dirty"]=True
		def cg(action,now):
			c=a["sel"];p=d["places"].get(c)if c else None
			if a["naming"]is not None:
				f=a["naming"];e=N(a["seen_text"]or "")[:a7];r=b["recs"].get(f);a["naming"]=None
				if r is not None:aj({"op":"name","root":f,"text":e});u(("Named it \"%s\"."%e)if e else "Its own name is back.",J)
				aH(a["query"])
			elif p is None or c not in b["recs"]:u("Click a place in the list first, then Name.",v)
			else:a["naming"]=c;aH(p["label"]);u("Type its new name in the Find box, then click Name again (empty: its own name).",E)
		def ch(action,now):
			aT();b=a["sel"];p=d["places"].get(b)if b else None;c,e=a["forget_arm"]
			if p is None:u("Click a place in the list first, then Forget.",v)
			elif c==b and 0<=now-e<=4.:a["forget_arm"]=(None,0.);aj({"op":"forget","root":b});a["sel"]=None;u("Forgot %s."%p["label"],J)
			else:a["forget_arm"]=(b,now);u("Click Forget again to forget %s (and the bags in it)."%p["label"],E)
		def bw():b=max(1,len(n["rows"]));return max(1,(len(a["rows"])+b-1)//b)
		def bx(action,now):b=bw();a["page"]=max(0,min(b-1,a["page"]+(1 if action=="next"else-1)));a["dirty"]=True
		ci={"show":cc,"follow":cd,"row":ce,"fav":cf,"name":cg,"forget":ch,"next":bx,"prev":bx}
		def cj(root):
			a=b["recs"];c=time.time()
			for s in[f for f,i in a.items()if i["root"]==root or f==root]:del a[s];b["tombs"][s]=c
			aG()
		def ck():return 32+max(1,len(h))*24+8
		def cl(f,x,y):
			if not h:e(f.g,"No favourites yet: type a name in the Find box, then click Add favourite.",x+12,y+2,l)
			for i,(b,c)in enumerate(h):a=y+i*24;m(f.g,f.store,"rm%d"%i,H,x+12,a,None,"Take %s off the favourites"%b);e(f.g,C(b,170),x+48,a+3,D);e(f.g,C(c,f.w-240),x+226,a+3,l)
		def cm(f,x,y):aa["wipe_at"]=0.;f.c["wipe_lbl"]=m(f.g,f.store,"wipe",H,x+12,y,"Forget everything","Empty the whole index, every character (click twice)")
		def cn(w):n,a=len(d["places"]),len(b["recs"]);c=os.path.basename(b["path"])if b["path"]else "(not known yet)";return(("WHAT IT NOTES  (when you open a container)",(("check","bank","Bank boxes (and the bags in them)","Note your bank box and its bags"),("check","ground","Chests and containers on the ground (in houses too)","Note chests and containers on the ground"),("check","pack","Your pack animals' packs","Note your pack horse, llama or beetle",{"h":23}),("num","days","Forget places not seen for:","Days a place stays after it was last opened (1-3650)","days",1,3650,{"lgap":6,"fw":44})),{"ch":24,"sh":134}),("FAVOURITES  (shown when the Find box is empty)",(("custom",0,cl),),{"sh":ck()}),("THE INDEX  (every character of the account)",(("note",C("%s, %s, %s, %s"%(F(n,"place"),F(a,"container"),F(d["items"],"item line"),F(d["chars"],"character")),w-24),{"hue":D}),("note",C("File: %s, in VirtueAssistantSettings"%c,w-24),{"h":14}),("custom",0,cm)),{"sh":92}))
		def co(f,new):d=Kit.read_int(f.c["days"],0);new["days"]=min(3650,d)if d>=1 else G["days"]
		def cp(f):
			b,c=f.store,f.c
			for i in range(len(h)):
				if ae(b,"rm%d"%i):del h[i];bk();a["dirty"]=True;af(T);return
			d=aa["wipe_at"]
			if d and not 0<=time.time()-d<=4.:aa["wipe_at"]=0.;A(c.get("wipe_lbl"),"Forget everything",D)
			if ae(b,"wipe"):
				e=time.time()
				if 0<=e-aa["wipe_at"]<=4.:aa["wipe_at"]=0.;aj({"op":"wipe"});ag.clear();a["sel"]=None;API.SysMsg("%s: the index is empty."%U,J);af(T)
				else:aa["wipe_at"]=e;A(c.get("wipe_lbl"),"Click again to empty it",v)
		aI=Kit.Page(G,cn,bR,adjust=co,clicks=cp)
		def cq():c.update({"shutting":False,"docked":False,"queue":[],"active":True,"check_at":0.,"merge_at":0.,"minimized":P.start_min()});bj();bS();j.clear();r["q"]=aR();del ad[:];a.update({"sel":None,"naming":None,"status":"","page":0,"dirty":True});b["path"]=aY(bJ%bT());b0();aS();P.dock(fit=True,min=(aL,at-(ah-4)*Y));aM.service("storage.show",R("show"))
		def cr():
			if n["g"]is None:return
			if aX(n):return
			a=time.time()
			if r["q"]and r["q"][0]["n"]<=au["n"]:r["q"]=aR()
			while ad:b1(ad.pop(0))
			b2(a)
			while c["queue"]:
				b=c["queue"].pop(0)
				if not P.action(b):
					d=ci.get(b[0]if isinstance(b,tuple)else b)
					if d is not None:d(b,a)
				if n["g"]is None:return
			if bu():b9(a);ca(a)
			bv(a)
		def cs():
			if c["shutting"]:return
			if not b["loaded"]:
				try:bl()
				except Exception as f:b["loaded"],b["err"]=True,str(f)[:60]
			bo();e=time.time()
			if b["dirty"]and(e-b["dirty_at"]>=a4 or e<b["dirty_at"]):bm();c["merge_at"]=e+an
			elif e>=c["merge_at"]or c["merge_at"]-e>an:c["merge_at"]=e+an;bW()
			if d["ver"]!=b["ver"]:
				b3();bs()
				if a["query"]:bt(a["query"])
		def ct():
			if c["shutting"]:return False
			if not b["loaded"]or bn()or d["ver"]!=b["ver"]:return True
			a=time.time()
			if b["dirty"]and(a-b["dirty_at"]>=a4 or a<b["dirty_at"]):return True
			return a>=c["merge_at"]or c["merge_at"]-a>an
		bj()
		def cu():
			c["shutting"]=True;c["active"]=False
			if bn()or b["dirty"]:
				with Kit.quiet:
					if not b["loaded"]:bl()
					bo();bm()
			j.clear();del ad[:];aM.close()
		return{"start":cq,"tick":cr,"stop":cu,"client_tick":True,"config_height":aI.height,"build_config":aI.build,"poll_config":aI.poll,"config_closed":aI.closed,"thread_tick":cs,"thread_wanted":ct}
	def bj():
		O="restock";U="Restock";at="Restock_settings";aY="Restock_pos";aZ="Restock_min";au="Restock_targets";av=400;a_,a0=240,46;a1=3705;P=22;ae=20;a2=12;a3=(4014,4016,4015);f=.7;a4=3.;W=10.;a5=3;a6=3;R=W;ax=3.;ay=2;a7=0;af=60000;a8=1.;a9=.25;ba=20.;bb=("cannot hold more",);bd=("must wait to perform another action",);be=("can not pick that up","cannot pick that up","that is too far away","that is out of sight","does not belong to you","already holding an item");bf={"REAGENTS":.1,"POTIONS":1.,"SCROLLS":1.,"OTHER":.1};az=(40.,3.5);aA="restock.stopped";bg=74;bh=8198;q=tuple(bO[0]for bO in ai);u=dict((bP[0],bP)for bP in ai);aB=dict((bQ[3],bQ[0])for bQ in ai);bi=("last","bank","pick");aD=(("last","Last opened","Take from the container you opened last"),("bank","Bank box","Take from your bank box (say \"bank\" near a banker to open it)"),("pick","Pick...","Target a chest to take from; remembered, opened once if closed"));aE=(("pack","Backpack","Restock into your backpack"),("bag","Pick bag...","Target a bag in your backpack to restock into"));b={"deep":True,"src_deep":True,"src":"last","src_serial":0,"dest":0};j={};bN=dict(b);a={"shutting":False,"minimized":False,"docked":False,"queue":[],"run":None,"halt":False,"status":("Idle",l),"last_open":0,"opened":[],"page":0,"count_at":0.,"short":{},"layout":None,"hooked":False,"active":False,"redraw":False,"shown_moved":0,"sent_at":0.,"flight":[]};k={"g":None,"c":{},"store":({},{}),"rows":[],"tips":{}};ag,s,h=am(a,U)
		def bj():pass
		def aI():
			b.update({"deep":True,"src_deep":True,"src":"last","src_serial":0,"dest":0})
			for a in ac(at).split(";"):
				if "="not in a:continue
				k,v=[c.strip()for c in a.split("=",1)]
				if k in("deep","src_deep"):b[k]=v=="1"
				elif k=="src"and v in bi:b["src"]=v
				elif k in("src_serial","dest"):
					try:b[k]=max(0,int(v))
					except ValueError:pass
			j.clear()
			for a in ac(au).split(","):
				if "="not in a:continue
				k,v=[g.strip()for g in a.split("=",1)]
				if k in u and v.isdigit():
					n=min(af,int(v))
					if n>0:j[k]=n
		def S():M(at,"deep=%d;src_deep=%d;src=%s;src_serial=%d;dest=%d"%(b["deep"],b["src_deep"],b["src"],b["src_serial"],b["dest"]))
		def d(obj,a,default=0):
			try:v=getattr(obj,a);return default if v is None else int(v)
			except Exception:return default
		def aJ(c):return not c or c==0xFFFFFFFF
		aK=Kit.top_of;X=Kit.in_pack
		def Y():return int(API.Backpack or 0)
		def ah():return int(API.Bank or 0)
		def aL(it,fallback="container"):
			try:n=str(it.Name or "").strip()
			except Exception:n=""
			return n or fallback
		def G(serial,deep):
			try:return list(API.ItemsInContainer(int(serial),bool(deep))or[])
			except Exception:return[]
		aj=aw
		def aN():return bool(aH(O)or API.HasTarget())
		def aQ():d=b["dest"];return d if d else Y()
		def al(dest,deep=None,max_age=0.):
			d=Y()
			if not d:return{}
			if b["deep"]if deep is None else deep:a=aq(True,max_age)
			else:
				a=aq(False,max_age)
				if dest and dest!=d:a=a+G(dest,False)
			c={}
			for e in a:
				try:
					k=aB.get(int(e.Graphic))
					if k is None:continue
					c[k]=c.get(k,0)+max(1,int(e.Amount or 1))
				except Exception:continue
			return c
		def bk(src,deep):
			b={}
			for a in G(src,deep):
				try:
					k=aB.get(int(a.Graphic))
					if k is None:continue
					b.setdefault(k,[]).append((max(1,int(a.Amount or 1)),int(a.Serial)))
				except Exception:continue
			return b
		def bl():
			try:
				p=API.Player;w=float(p.Weight or 0);a=float(p.WeightMax or 0)
				if a<=0:a=az[0]+az[1]*float(p.Strength or 0)
				return None if a<=0 else a-a7-w
			except Exception:return
		def aR():
			e=b["src"]
			if e=="bank":
				d=ah()
				if not d:return(0,"Your bank box (not open)","open your bank box first (say \"bank\" near a banker)")
				try:f=len(API.ItemsInContainer(d,False)or())>0
				except Exception:f=False
				return d,"Your bank box"+(""if f else " (not open)"),None
			if e=="pick":
				s=b["src_serial"]
				if not s:return 0,"Nothing picked yet","pick the chest first (Pick...)"
				c=API.FindItem(s)
				if c is None:return(0,"The picked chest (out of view)","the chest you picked is out of view")
				return s,an(c),None
			s=a["last_open"];c=API.FindItem(s)if s else None
			if c is None:return 0,"Last opened: none yet","open a chest or your bank box first"
			return s,"Last opened: "+an(c),None
		def an(it):
			if int(it.Serial)==ah():return "your bank box"
			a=aL(it)
			if d(it,"OnGround")or aJ(d(it,"Container")):return "%s at %d, %d"%(a,d(it,"X"),d(it,"Y"))
			return a
		def aS():
			d=b["dest"]
			if not d:return "Your backpack",None
			a=API.FindItem(d)
			if a is None or not X(d):return "The picked bag (not in your backpack)","the bag you picked isn't in your backpack: pick it again or choose Backpack"
			return aL(a,"bag")+" in your backpack",None
		def ao(serial):
			if not serial:return "nothing was targeted"
			a=API.FindItem(serial)
			if a is None:return "that isn't an item"
			b,c=aK(serial);t=API.FindItem(b)if b!=int(serial)else a
			for x in(a,t):
				if x is not None and(d(x,"Graphic")==bh or d(x,"IsCorpse")):return "a corpse (or a bag in one) isn't a source"
			if X(serial):return "that is in your backpack"
			return "that isn't a container"if not(d(a,"IsContainer")or G(serial,False))else None
		def aT(src):
			c=API.FindItem(src)
			if c is None:return "the source is out of view"
			e,a=aK(src)
			if a:
				p=API.Player
				if a==d(p,"Serial"):return
				m=API.FindMobile(a)
				if m is None or not d(m,"IsRenamable"):return "the source is on someone else"
				b=max(abs(d(m,"X")-d(p,"X")),abs(d(m,"Y")-d(p,"Y")));return "your pack animal is out of reach (step next to it)"if b>ay else None
			t=API.FindItem(e)
			if t is None:return
			try:p=API.Player;b=max(abs(d(t,"X")-d(p,"X")),abs(d(t,"Y")-d(p,"Y")))
			except Exception:return
			return "the source is out of reach (step next to it)"if b>ay else None
		def bm(*c):
			if not a["active"]:return
			for b in c:
				try:s=int(b.Serial or 0)
				except AttributeError:
					try:s=int(b or 0)
					except Exception:s=0
				except Exception:s=0
				if s:a["opened"].append(s);del a["opened"][:-8];return
		def bn():aC(a,"hooked",("OnOpenContainer",bm))
		def bo():
			while a["opened"]:
				s=a["opened"].pop(0)
				if ao(s)is None:a["last_open"]=s
		def i(text,hue=None):
			a["status"]=(text,l if hue is None else hue);b=k["c"].get("status")
			if b is not None:
				if a["minimized"]:text=U+": "+text[:1].lower()+text[1:]
				A(b,C(text,k["c"].get("status_w",200)),a["status"][1])
		def bp():
			if a["run"]is not None:h("already restocking; press Stop first.",v);return
			k=[n for n in q if j.get(n,0)>0]
			if not k:h("the list is empty: set how many of each item to carry on the settings page.",v);aP(O);return
			e,m,c=aR()
			if c is None:c=ao(e)or aT(e)
			if c is None:
				l=aQ();c=None if l else "you have no backpack"
				if c is None:c=aS()[1]
			if c is None and aN():c="a target cursor is up"
			if c is None and aj():c="you are holding an item"
			if c is None and d(API.Player,"IsDead"):c="you are dead"
			if c is not None:h("can't restock: %s."%c,v);i("Can't: "+c,v);return
			g=time.time();r={"src":e,"dest":l,"deep":b["deep"],"src_deep":b["src_deep"],"phase":"go","open_until":0.,"move":None,"check":None,"at":g,"hold":0.,"sent_at":0.,"last":0,"left":False,"c0":0,"moved":0,"moves":0,"refused":0,"streak":0,"waits":0,"why":None,"bad":set(),"limbo":[w for w in a["flight"]if 0<=w[2]-g<=R]}
			if 0<=g-a["sent_at"]<f:r["at"]=a["sent_at"]+f
			a.update({"flight":[],"short":{},"halt":False})
			if not G(e,False):
				if e==ah():h("your bank box isn't open: say \"bank\" near a banker first.",v);i("Bank box not open",v);return
				API.UseObject(e);r.update({"phase":"open","open_until":g+ax});i("Opening the chest")
			else:i("Restocking")
			a["run"]=r;h("restocking %s."%F(len(k),"item"));T()
		def bq(r,key,now):
			n=0;a=[]
			for e in r["limbo"]:
				if 0<=e[2]-now<=R:
					a.append(e)
					if e[0]==key:n+=e[1]
			r["limbo"]=a;return n
		def br(now):
			r=a["run"]
			if r is None or r["move"]is not None:return
			if r["check"]is not None and not r["left"]:
				b=API.FindItem(r["check"][1])
				if b is None or d(b,"Container")!=r["c0"]:r["left"]=True
			if r["why"]:p(r["why"]);return
			if r["phase"]=="open":
				if G(r["src"],False):r["phase"]="go";i("Restocking")
				elif not 0<=r["open_until"]-now<=ax:p("the chest didn't open (or it is empty)")
				return
			if r["check"]is not None:
				if 0<r["at"]-now<=f or not bt(r,now):return
			if 0<r["hold"]-now<=f or 0<r["at"]-now<=f:return
			if aN():p("a target cursor is up");return
			h=aj()
			if h and not(h==r["last"]and 0<=now-r["sent_at"]<2*f):p("you picked something up");return
			if d(HOST.me(),"IsDead"):p("you died");return
			c=aT(r["src"])
			if c:p(c);return
			bs(r,now)
		def bs(r,now):
			g=al(r["dest"],r["deep"]);v=bk(r["src"],r["src_deep"]);h=False
			for b in q:
				t=j.get(b,0)
				if t<=0:continue
				k=bq(r,b,now);e=t-g.get(b,0)-k
				if e<=0:
					if k:h=True
					a["short"].pop(b,None);continue
				l=[x for x in v.get(b,())if x[1]not in r["bad"]]
				if not l:a["short"][b]=e;continue
				w,m=max(l);c=min(w,e);n=bl()
				if n is not None:
					o=int(n/bf.get(u[b][1],1.)+1e-6)
					if o<1:p("you are at your weight limit");return
					c=min(c,o)
				a["short"].pop(b,None);s=API.FindItem(m);r["c0"]=d(s,"Container")if s is not None else 0;r["move"]=(b,m,c,g.get(b,0));i("Moving %d %s (%d moved)"%(c,u[b][2],r["moved"]));return
			if h:i("Waiting for the server");r["hold"]=now+f;return
			bw()
		def bt(r,now):
			b,c,a,j=r["check"];e=r["sent_at"]
			if ak(e,bb)is not None:p("your %s can't hold more"%("backpack"if r["dest"]==Y()else "bag"));return False
			k=al(r["dest"],r["deep"]).get(b,0);l=now-e;g=API.FindItem(c);m=d(g,"Container")if g is not None else 0;h=k>j
			if not h and g is not None and not aJ(m)and m!=r["c0"]:
				h=X(c)
				if h:k=j+a
			if h:
				n=min(k-j,a);r["moved"]+=n
				if n<a:r["limbo"].append([b,a-n,now+R])
				r.update({"check":None,"left":False,"streak":0,"waits":0});return True
			o=g is not None and m==r["c0"]
			if not o or aj()==c:
				r["left"]=True
				if not 0<=l<W:p("the server hasn't answered a move for %d s"%int(W));return False
				if l>=2*f:i("Waiting for the server")
				r["at"]=now+f*.5;return False
			if ak(e,bd)is not None and r["waits"]<a6:
				r["waits"]+=1
				if not r["left"]:r["limbo"].append([b,a,now+R])
				r.update({"check":None,"left":False,"hold":now+f});return False
			q=ak(e,be)is not None
			if not(q or r["left"])and 0<=l<a4:r["at"]=now+f*.5;return False
			if not r["left"]:r["limbo"].append([b,a,now+R])
			r.update({"check":None,"left":False,"waits":0});r["refused"]+=1;r["streak"]+=1;r["bad"].add(c)
			if r["streak"]>=a5:p("%d moves in a row were refused"%r["streak"]);return False
			return True
		def bu():
			r=a["run"]
			if r is None or r["move"]is None:return
			b=r["move"];r["move"]=None
			if a["halt"]or a["shutting"]:return
			try:API.MoveItem(b[1],r["dest"],b[2])
			except Exception as c:r["why"]="a move failed (%s)"%c;return
			aM();r.update({"check":b,"left":False,"last":b[1]});r["sent_at"]=a["sent_at"]=time.time();r["at"]=r["sent_at"]+f;r["moves"]+=1
		def bv():
			if not a["short"]:return ""
			b=["%s %d"%(u[c][2],g)for c,g in sorted(a["short"].items(),key=lambda a:q.index(a[0]))];return "; short (none left in the source): "+", ".join(b[:6])+(" and %d more"%(len(b)-6)if len(b)>6 else "")
		def ar(r):
			if r is None:return
			b=[list(g)for g in r["limbo"]]
			if r["check"]is not None:c,e,d,f=r["check"];b.append([c,d,r["sent_at"]+W])
			if b:a["flight"]=(a["flight"]+b)[-20:]
		def bw():
			r,a["run"]=a["run"],None
			if r is None:return
			ar(r);b=("done: %d moved in %s"%(r["moved"],F(r["moves"],"move")))
			if r["refused"]:b+=", %d refused"%r["refused"]
			h(b+bv()+".",v if a["short"]or r["refused"]else J);i("Done: %d moved%s"%(r["moved"],", some short"if a["short"]else ""),E if a["short"]else J);a["count_at"]=0.;T()
		def p(why=None,user=False):
			r,a["run"]=a["run"],None;a["halt"]=True
			if r is None:return
			ar(r)
			if user:h("stopped (%d moved)."%r["moved"]);i("Stopped (%d moved)"%r["moved"])
			else:
				b="%s (%d moved)"%(why or "stopped",r["moved"])
				if not aF(aA,"Stopped: "+b,"warn"):h("stopped: "+b+".",v)
				i("Stopped: "+(why or ""),v)
			a["count_at"]=0.;T()
		def bx():a["halt"]=True;s("stop")()
		def by():return[c for c in q if j.get(c,0)>0]
		Z=2*K+30+3*B+136+64
		def aa():d=by();b=t.rows(P,Z+ad(0)-2*P,a2,2);e=max(1,(len(d)+b-1)//b);c=min(a["page"],e-1);return(a["minimized"],a["docked"],c,e,tuple(d[c*b:(c+1)*b]))
		def ab():
			c=aa();a["page"]=c[2];a["layout"]=c;G=a["minimized"];J=t.slot if V(O)else None;y,N=(a_,a0)if G else(J or(av,Z+ad(len(c[4]))));g,p,h=t.begin(y,N);M=K;R=[]
			if G:h["status_w"]=y-90
			else:
				j=y-2*M;t.frame(g);k=M+30+B;z(g,M,k,j,136,"FROM AND TO");e(g,"From:",M+12,k+30,l);A=M+12+max(o("From:"),o("Into:"))+10;h["src"]=e(g,"",A,k+30);h["src_w"]=j-(A-M)-8;q=M+12
				for d,r,v in aD:h["m_"+d]=m(g,p,"m_"+d,I,q,k+52,r,v,E if b["src"]==d else D,on_click=s(("src",d)));q+=35+o(r)+14
				e(g,"Into:",M+12,k+84,l);h["dest"]=e(g,"",A,k+84);q=M+12
				for d,r,v in aE:h["d_"+d]=m(g,p,"d_"+d,I,q,k+106,r,v,E if(d=="bag")==bool(b["dest"])else D,on_click=s(("dest",d)));q+=35+o(r)+14
				n=k+136+B;S=N-Z if J else ad(len(c[4]));z(g,M,n,j,S,"LIST  (carried / to carry)")
				if c[3]>1:F=M+j-12-21;m(g,p,"next",L,F,n+4,None,"Next page",on_click=s(("page",1)));e(g,"%d/%d"%(c[2]+1,c[3]),F-8-o("%d/%d"%(c[3],c[3])),n+6,l);m(g,p,"prev",a3,F-16-o("%d/%d"%(c[3],c[3]))-21,n+4,None,"Previous page",on_click=s(("page",-1)))
				if not c[4]:e(g,"The list is empty: set how many to carry",M+12,n+30,l);e(g,"on the "+U+" settings page.",M+12,n+50,l)
				T=M+j-100
				for Y,W in enumerate(c[4]):w=n+28+Y*P;af,ag,X,ab=u[W];bc(g,ab,0,M+12,w,ae);e(g,C(X,T-(M+12+ae+6)-8),M+12+ae+6,w+2);ac=e(g,"",T,w+2);v=Q(g,M+8,w,j-16,P,bj,X);R.append({"key":W,"count":ac,"tip":v})
				x=n+S+B;z(g,M,x,j,64);m(g,p,"go",L,M+12,x+8,"Restock","Top each item up to its target from the source (one move every %.1f s)"%f,on_click=s("go"));sx=M+12+35+o("Restock")+18;m(g,p,"stop",H,sx,x+8,"Stop","Stop moving items",on_click=bx);h["status"]=e(g,"",M+12,x+40,a["status"][1]);h["status_w"]=j-24
			t.end(g,{"rows":R,"tips":{}});i(*a["status"]);a["count_at"]=0.;aU(time.time())
		t=Kit.Window(O,U,a,k,ab,aY,aZ,(240,220),icon=a1,cleanup=ag,clear={"c":{},"rows":[]})
		def ad(n):return 30+max(2,n)*P+6
		def T():
			e=k["c"]
			for a,d,f in aD:
				c=e.get("m_"+a)
				if c is not None:A(c,d,E if b["src"]==a else D)
			for a,d,f in aE:
				c=e.get("d_"+a)
				if c is not None:A(c,d,E if(a=="bag")==bool(b["dest"])else D)
		def aU(now):
			h=k["g"]
			if h is None or a["minimized"]:return
			if 0<=now-a["count_at"]<a8:return
			a["count_at"]=now;c=k["c"];q,i,r=aR();A(c["src"],C(i,c["src_w"]));l,m=aS();A(c["dest"],C(l,c["src_w"]),v if m else D)
			if not k["rows"]:return
			o=al(aQ(),None,0. if a["run"]is not None else.5);e=k["tips"]
			for d in k["rows"]:
				b=d["key"];n,t=o.get(b,0),j.get(b,0);p=J if n>=t else(v if n==0 else E);A(d["count"],"%d / %d"%(n,t),p);f=(n,t,a["short"].get(b))
				if e.get(b)==f:continue
				g="%s: %d in your pack, target %d"%(u[b][2],n,t)
				if b in a["short"]:g+=" (short by %d: none left in the source)"%a["short"][b]
				e[b]=f;d["tip"].SetTooltip(g)
		def bz(what):
			if a["run"]is not None:h("press Stop first.",v);return
			h("target the chest to take from."if what=="src"else "target a bag in your backpack.")
			def b(serial):s(("picked",what,int(serial or 0)))()
			aO(ba,b,O)
		def bA(what,serial):
			if not serial:return
			if what=="src":
				e=ao(serial)
				if e:h("not a source: %s."%e,v);return
				b["src"],b["src_serial"]="pick",serial;S();c=API.FindItem(serial);h("taking from %s."%(an(c)if c is not None else "it"),J)
			else:
				f=Y()
				if serial==f:b["dest"]=0
				else:
					c=API.FindItem(serial)
					if c is None or not X(serial)or not(d(c,"IsContainer")or G(serial,False)):h("pick a bag that is in your backpack.",v);return
					b["dest"]=serial
				S()
			a["count_at"]=0.;T()
		def aV(grp):return[c for c in ai if c[1]==grp]
		def bB(grp):n=len(aV(grp));return 30+((n+1)//2)*26+6
		def bC(action):
			if a["run"]is not None:p(user=True)
		def aW(action):
			c=action[0]
			if a["run"]is not None:h("press Stop first.",v)
			elif action[1]==("pick"if c=="src"else "bag"):bz(c)
			else:b[c]=action[1]if c=="src"else 0;S();a["count_at"]=0.;T()
		def bD(action):b=aa()[3];a["page"]=(a["page"]+action[1])%b;ab()
		bE={"go":lambda action:bp(),"stop":bC,"src":aW,"dest":aW,"picked":lambda action:bA(action[1],action[2]),"page":bD};bF=30+2*28+24+8
		def bG(w):a=(w-24)//2;return[("%s  (%s)"%(c,"how many to carry, 0 = leave alone"if c=="REAGENTS"else "how many to carry"),[("num",r,C(n,a-76),"How many %s to carry (0-%d, 0 = leave it alone)"%(n,af),None,0,af,{"dx":12+(g%2)*a,"stay":g%2==0})for g,(r,x,n,y)in enumerate(aV(c))],{"sh":bB(c),"lw":a-78,"fw":52,"fh":26})for c in ap]+[("OPTIONS",(("check","deep","Count inside bags in your pack","Bags inside your backpack count too (as Inventory > Supplies and Grimoire)",{"h":28}),("check","src_deep","Take from bags inside the source too","Bags inside the chest or bank box too (only those whose contents you have seen)",{"h":30}),("note","One move every %.1f s; it stops when you pick something up."%f)),{"sh":bF})]
		def bH(c,new):
			if(new["deep"],new["src_deep"])!=(c["deep"],c["src_deep"]):b.update(deep=new["deep"],src_deep=new["src_deep"]);S();a["count_at"]=0.
			if any(new[g]!=c[g]for g in q):
				j.clear();j.update((n,new[n])for n in q if new[n]>0);M(au,",".join("%s=%d"%(r,j[r])for r in q if j.get(r,0)>0));a["count_at"]=0.
				if aa()!=a["layout"]:a["redraw"]=True
		N=Kit.Page(b,bG,None,bH,every=a9)
		def bI(g,x,y,w):N.vals=dict(b);N.vals.update((c,j.get(c,0))for c in q);N.build(g,x,y,w)
		def bJ():a.update({"shutting":False,"docked":False,"queue":[],"run":None,"halt":False,"status":("Idle",l),"opened":[],"page":0,"count_at":0.,"short":{},"layout":None,"active":True,"redraw":False,"shown_moved":0,"minimized":t.start_min()});aI();aG(aA,"Restock stopped early",bg);bn();ab();ag.service("restock.run",s("go"));t.dock(fit=True,min=(av,Z+ad(2)))
		def bK():
			if k["g"]is None:return
			if aX(k):return
			if a["opened"]:bo()
			while a["queue"]:
				b=a["queue"].pop(0)
				if t.action(b):continue
				c=bE.get(b[0]if isinstance(b,tuple)else b)
				if c is not None:c(b)
			if a["redraw"]:
				a["redraw"]=False
				if aa()!=a["layout"]:ab()
			d=time.time();r=a["run"]
			if r is not None:
				br(d);bu()
				if r["moved"]!=a["shown_moved"]:a["shown_moved"]=r["moved"];a["count_at"]=0.
			aU(d)
		def bL():return.05 if a["run"]is not None else.1
		aI()
		def bM():a.update({"shutting":True,"halt":True,"active":False});r,a["run"]=a["run"],None;ar(r);S();ag.close()
		return{"start":bJ,"tick":bK,"stop":bM,"client_tick":True,"config_height":N.height,"build_config":bI,"poll_config":N.poll,"config_closed":N.closed,"interval":bL}
	def bk():
		j="supplies";az="Supplies";a0="UnitFrames_settings";S="UnitFrames_supset";a2=10.;a3=.5;a6=1.;T=220;F=22;J=20;aC=20;aD="UnitFrames_suppos";U=("Below the frame","Left of the frame","Right of the frame");a7=10;a8=.1;a9=.25;k=tuple(bG+(None,)for bG in ai);ba=("bp","bm","ga","gi","mr","ns","ss","sa","p_heal","p_cure","p_refresh","s_recall","s_gate","o_band");aE="UnitFrames_supplies";aF="UnitFrames_supwarn";bb=E;be=.25;aG=9999;d={"sup_open":False,"sup_deep":True,"sup_hide0":False,"sup_follow":True,"sup_low":a7,"sup_side":0};bE=dict(d);L={"sup_low":(0,9999),"sup_side":(0,2)};b={"minimized":False,"shutting":False,"docked":False,"next_supply":0.,"counts":{},"next_save":0.,"queue":[]};p={"g":None,"c":{},"store":({},{})};i=set(ba);a={"g":None,"c":{},"rows":(),"at":None,"slot":None,"drawn":None};n={};W={"next_warn":0.};N,Y=ac,M;O,ah,bF=am(b,az)
		def bf(key):aZ(key,",",d,L)
		def aH():bf(S if N(S,"")else a0)
		def P():a_(S,",",d,sorted(d),L)
		def aI():
			a=N(aE,"-")
			if a=="-":return
			b=set(c[0]for c in k);i.clear();i.update(f for f in a.split(",")if f in b)
		def aL():Y(aE,",".join(c[0]for c in k if c[0]in i)or "none")
		def aM():
			n.clear();d=set(f[0]for f in k)
			for b in N(aF,"").split(","):
				if "="not in b:continue
				c,v=b.split("=",1)
				if c not in d:continue
				a=[]
				for e in(v.split("/")+["",""])[:2]:
					try:a.append(max(0,min(aG,int(e))))
					except ValueError:a.append(None)
				if a[0]is not None or a[1]is not None:n[c]=a
		def bg():
			b=[]
			for r in k:
				a=n.get(r[0])
				if a:b.append("%s=%s/%s"%(r[0],""if a[0]is None else a[0],""if a[1]is None else a[1]))
			Y(aF,",".join(b))
		def bh():
			b={}
			for a,m,n,j,c in k:
				if a in i:b.setdefault(j,[]).append((a,c))
			e=dict((w[0],0)for w in k if w[0]in i)
			if not b:return e
			for f in aq(bool(d["sup_deep"]),a3):
				try:
					g=b.get(int(f.Graphic or 0))
					if not g:continue
					c=int(f.Hue or 0)&16383;l=max(1,int(f.Amount or 1))
				except Exception:continue
				for a,h in g:
					if h is None or h==c:e[a]+=l
			return e
		def ak():return tuple((c,f,g)for c,f,g,h,w in k if c in i and not(d["sup_hide0"]and not b["counts"].get(c,0)))
		def aO(key):
			c=b["counts"].get(key,0);a=n.get(key);f=a[1]if a is not None and a[1]is not None else d["sup_low"]
			if c<=f:e=v
			else:e=bb if a is not None and a[0]is not None and c<=a[0]else D
			return "{:,}".format(int(c)),e
		def aP():return bool(d["sup_follow"])and not V(j)
		def aQ():return a["slot"]if V(j)else None
		def al(rows,pitch):b=[(c,[g for g in rows if g[1]==c])for c in ap if any(f[1]==c for f in rows)];a=[26+len(h)*pitch+4 for w,h in b]or[26+2*pitch+4];return b,a,16+sum(a)+B*(len(a)-1)
		def bi(w,h,mode):
			b=(int(w),int(h))if(w is not None and h is not None)else None
			if b!=a["slot"]or mode=="again":a["slot"]=b;a["drawn"]=False
		def bj():return T,al(ak(),aC)[2]
		def aR(rows):
			d=a["g"];b=aQ();A=V(j);f=aP();c=F;n,p,h=al(rows,c);w=T if b is None else b[0]
			if b is not None:
				N=sum(len(bG)for bH,bG in n)or 2;c=max(aC,min(2*F,F+(b[1]-h)//N));n,p,h=al(rows,c)
				if h<b[1]:p[-1]+=b[1]-h;h=b[1]
			g=G.CreateGump(True,not f and not aj(j));Z(g,w,h,corners=False);E={};y=8;I=dict((bI,(bJ,bK))for bI,bL,bM,bJ,bK in k)
			if not n:z(g,8,y,w-16,p[0],"SUPPLIES");O="None of these in your pack."if i else "No rows ticked yet.";e(g,O,18,y+26,l);e(g,"Pick rows: its settings page.",18,y+26+c,l)
			for(P,S),K in zip(n,p):
				z(g,8,y,w-16,K,P)
				for U,(r,Y,W)in enumerate(S):s=y+26+U*c;bc(g,I[r][0],I[r][1],16,s+(c-J)//2-1,J);L,X=aO(r);s+=(c-F)//2;E[r]=e(g,L,w-18-o(L),s+2,X);e(g,C(W,w-18-J-4-18-6-44),18+J+4,s+2)
				y+=K+B
			t=None
			if A:D=aA(j);x,v=(D[0],D[1])if D is not None else ar()
			elif not f:
				Q(g,0,0,w,h,lambda:None,"Drag to move the supplies table",movable=True);x,v=ar()
				if u(d):x,v=d.GetX(),d.GetY()
				an(g,x,v,w,h)
			else:M=at(w,h);t=M[1]if M is not None else ar();an(g,t[0],t[1],w,h)
			if not ag(j):m(g,({},{}),"close",H,w-8-30,10,None,"Close the supplies list",on_click=ah("close"))
			a.update({"g":g,"c":E,"rows":rows,"at":t,"w":w,"h":h,"follow":f,"leader":None,"drawn":b})
			if A:bd(j,g,a4(g,x,v,w,h,j,False,None,None))
			else:G.AddGump(g)
			if not f and not A:a1(g,q)
			R(d);aw()
		bk=(60,620)
		def ar():
			b=N(aD,"");a["saved"]=b
			try:x,y=(int(f)for f in b.split(","));return aB(x,y,a.get("w",0),a.get("h",0))
			except ValueError:c=at(a.get("w",T),a.get("h",0));return c[1]if c is not None else bk
		def q():
			g=a["g"]
			if u(g)and not a.get("follow",True)and not V(j):
				try:b="%d,%d"%(int(g.GetX()),int(g.GetY()))
				except Exception:return
				if b!=a.get("saved"):a["saved"]=b;Y(aD,b)
		def at(w,h):
			a=HOST.services.get("frames.player_anchor")
			if a is None:return
			try:return a(w,h,d["sup_side"])
			except Exception:return
		def aw():
			g=a["g"]
			if not u(g)or not a.get("follow",True):return
			d=at(a["w"],a["h"])
			if d is None:return
			c,b=d
			if a.get("leader")is not c:a["leader"]=c;aa(g,c)
			if b!=a["at"]:
				a["at"]=b
				try:an(g,b[0],b[1],a["w"],a["h"]);ad(g)
				except Exception:pass
		bl=620;bm="UnitFrames_rowspos";ax="supplies_rows"
		def aS():
			M,f=K,B;w=bl;b=w-2*M;r=max(sum(1 for bG in k if bG[1]==G)for G in ap);h=52+r*aU+4;j=M+30+f+h+M;g,c,t=s.begin(w,j);Z(g,w,j);z(g,M,M,b,30);e(g,"SUPPLIES TABLE ROWS",M+30,M+7,E);a=w-M-54-20-35-o("Untick all");m(g,c,"none",H,a,M+4,"Untick all","Empty the table");a-=14+35+o("Tick all");m(g,c,"all",X,a,M+4,"Tick all","Show every row");Q(g,M,M,a-M-6,30,lambda:None,"Drag to move",movable=not aj(ax))
			if not ag(ax):m(g,c,"close",H,w-M-54,M+4,None,"Close the table")
			d=M+30+f;z(g,M,d,b,h,"ROWS  (ticked rows show in the table)");l=(b-16)//len(ap)
			for u,n in enumerate(ap):
				p=M+10+u*l;e(g,n,p,d+30,E)
				for v,(q,y,x,A,D)in enumerate(bH for bH in k if bH[1]==n):t[q]=au(g,C(x,l-34),p,d+52+v*aU,q in i)
			s.end(g,{"next_poll":0.})
		s=Kit.Window(ax,"Supplies Rows",b,p,aS,bm,default=(260,160),cleanup=O,owner=False,clear={"c":{}})
		def aT(now):
			if not d["sup_open"]:
				if a["g"]is not None:q();i,a["g"]=a["g"],None;R(i)
				return
			f=now>=b["next_supply"]or not b["counts"]or(now>=b.get("sup_min",0.)and aN()!=b.get("pack_v"))
			if f:b.update({"next_supply":now+a6,"sup_min":now+a8,"pack_v":aN()});b["counts"]=bh()
			if not u(a["g"])or a.get("follow")!=aP()or a["drawn"]!=aQ():q();aR(ak())
			elif f:
				e=ak()
				if e!=a["rows"]:q();aR(e)
				else:
					for g,k,l in e:
						h,j=aO(g);c=a["c"].get(g)
						if c is not None and A(c,h,j):c.SetPos(a["w"]-18-a5(h),c.GetY())
					aw()
			else:aw()
		def bn(now):
			g=p["g"]
			if g is None:return
			if not u(g):p.update({"g":None,"c":{}});return
			e,f=p["store"],p["c"]
			if ae(e,"close"):s.close();return
			h=False
			for l,a in(("all",True),("none",False)):
				if ae(e,l):
					h=True
					for c in f.values():c.SetIsChecked(a)
			if not h and not HOST.pass_poked and now<p.get("next_poll",0.):return
			p["next_poll"]=now+a9;d=set()
			for k,c in f.items():
				try:a=bool(c.IsChecked)
				except Exception:a=k in i
				if a:d.add(k)
			if d!=i:i.clear();i.update(d);aL();b["next_supply"]=0.;af(j)
		def bo(now):
			if not d["sup_open"]:d["sup_open"]=True;P();b["next_supply"]=0.
			aT(now);g=a["g"]
			if u(g):safe(lambda:ab(g).BringOnTop())
		def bp(now):d["sup_open"]=False;P()
		bq={"open":bo,"close":bp,"sup_rows":lambda now:aS()};ay=(("sup_follow","The table sticks to the player frame","Untick to drag it anywhere"),("sup_deep","Count inside bags in your backpack","Bags and pouches in your backpack count too"),("sup_hide0","Hide rows you have none of","Leave out rows at 0"));br="A row at or below this shows red, unless it has its own Red below (0-%d)"%L["sup_low"][1];aU=24;bs=118;aV=26;r=44
		def aW():return[c for c in k if c[0]in i]
		def bt():return 30+20+max(1,(len(aW())+1)//2)*aV+4
		def bu(f,x,y):
			g,b=f.g,aW();c=(f.w-36)//2;k=[]
			if not b:e(g,"No rows ticked yet: click Choose rows above.",x+12,y+2,l)
			for p in range(2 if len(b)>1 else(1 if b else 0)):a=x+12+p*(c+12)+c-2*r-8;e(g,"Yellow",a,y-2,E);e(g,"Red",a+r+8,y-2,v)
			for m,(o,t,h,u,w)in enumerate(b):i=x+12+(m%2)*(c+12);j=y+20+(m//2)*aV;a=i+c-2*r-8;e(g,C(h,a-i-8),i,j+3);d=n.get(o)or(None,None);q=ao(av(g,""if d[0]is None else str(d[0]),a,j,r),"Yellow at or below this many %s (empty: never)"%h);s=ao(av(g,""if d[1]is None else str(d[1]),a+r+8,j,r),"Red at or below this many %s (empty: Red at or below above)"%h);k.append((o,q,s))
			f.c["warn"]=k
		def bv(w):return(("TABLE",(("check",)+ay[0]+({"stay":True},),("check",)+ay[1]+({"dx":12+w//2},),("check",)+ay[2],("num","sup_low","Red at or below:",br,None)+L["sup_low"]+({"ldy":4,"lgap":12,"fw":60,"stay":True},),("note","Opens:",{"dx":12+w//2,"ndy":4,"hue":None,"stay":True}),("buttons",(("sup_rows",I,"Choose rows","Pick the rows the table shows (%d of %d ticked)"%(len(i),len(k))),),{"dx":w-45-o("Choose rows"),"bdy":-78})),{"sh":bs}),("SUPPLY WARNINGS  (yellow and red counts, per row)",(("custom",0,bu),),{"sh":bt()}))
		def bw(f):
			if ae(f.store,"sup_rows"):ah("sup_rows")()
			if f.c.get("warn")and time.time()>=W["next_warn"]:
				W["next_warn"]=time.time()+be
				if aX(f.c):b["next_supply"]=0.
		def bx(f,new):
			a=f.c.get("sup_side")
			if a is None:return
			b=Kit.dd_index(a,-1)
			if 0<=b<len(U):new["sup_side"]=b
		def by(c,new):b["next_supply"]=0.;a["at"]=None
		t=Kit.Page(d,bv,P,by,adjust=bx,clicks=bw)
		def bz(g,x,y,w):
			f=t.build(g,x,y,w);b=x+24+(w//2)+o("Opens:");W["next_warn"]=0.
			try:a=G.CreateDropDown(150,list(U),int(d["sup_side"]));a.SetPos(b,y+82);g.Add(a);f.c["sup_side"]=ao(a,"Side of the player frame the table opens on (flips when there is no room)")
			except Exception:f.c["sup_side"]=None;e(g,U[d["sup_side"]],b,y+86,l)
		def aX(c):
			b=False
			for d,h,j in c.get("warn")or():
				e=n.get(d)or[None,None];a=list(e)
				for i,f in((0,h),(1,j)):
					try:
						if f.IsDisposed:continue
						g=str(f.Text or "").strip()
					except Exception:continue
					if not g:a[i]=None
					else:
						try:a[i]=max(0,min(aG,int(g)))
						except ValueError:pass
				if a!=list(e):
					if a[0]is None and a[1]is None:n.pop(d,None)
					else:n[d]=a
					b=True
			if b:bg()
			return b
		def bA():
			f=t.f
			if f is not None and f.c.get("warn")and aX(f.c):b["next_supply"]=0.
			t.closed()
		def aY():ah("open")()
		def bB():b.update({"next_supply":0.,"counts":{},"next_save":0.,"queue":[]});a["saved"]=None;aH();aI();aM();O.service("supplies.open",aY);s.dock();aJ(j,{"title":az,"state":lambda:"open"if u(a["g"])else None,"show":aY,"gump":lambda:a["g"],"fit":bi,"min":bj,"untitled":True});O.add(aK,j)
		def bC():
			a=time.time()
			while b["queue"]:
				c=b["queue"].pop(0)
				if s.action(c):continue
				d=bq.get(c)
				if d is not None:d(a)
			bn(a);aT(a)
			if a>=b["next_save"]:b["next_save"]=a+a2;q()
		aH();aI();aM()
		def bD():P();aL();q();g,a["g"]=a["g"],None;R(g);O.close()
		return{"start":bB,"tick":bC,"stop":bD,"client_tick":True,"config_height":t.height,"build_config":bz,"poll_config":t.poll,"config_closed":bA}
	bl=(("bags",bg,.1,"bag"),("paperdoll",bh,.1,"character"),("storage",bi,.1,"storage"),("restock",bj,.1,"restock"),("supplies",bk,.1,"supplies"),);return PartSet(be,bf,bl).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("inventory","Inventory","Bags, paperdoll, storage, restock, supplies",_module_inventory,.1,category="Your things",parts=(("bags","Bags","All your bags in one grid",True,("bag",)),("paperdoll","Paperdoll","What you wear, and your stats",True,("character",)),("storage","Storage","What the containers you opened hold",False,("storage",)),("restock","Restock","Refills from a chest or bank, on a press",False,("restock",)),("supplies","Supplies","Pack supplies, low counts marked",True,(),True),),aliases=('Character','Unified Bag','Storage Index','Restock','paperdoll','bank','chest','find','sort','supplies','supplies table'))
