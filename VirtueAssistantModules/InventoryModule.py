def _module_inventory():
	aO=Client.on_client_thread;aE=Follow.toggle;aP=HOST.alert;aQ=HOST.alert_kind;aF=HOST.bar_alive;aR=HOST.cursor_busy;aS=HOST.cursor_ok;aT=HOST.dock_add;aU=HOST.dock_remove;aV=HOST.dock_wanted;ac=HOST.layout_holds;ao=HOST.layout_locked;aG=HOST.layout_rect;aH=HOST.me;aW=HOST.pack_dirty;ap=HOST.pack_items;av=HOST.pack_ver;aI=HOST.pick_target;Y=HOST.refresh_settings;aw=HOST.release_cursor;aX=HOST.show_settings;aq=Journal.find;aY=Journal.reader;I=Kit.ART_CLOSE;aZ=Kit.ART_MIN;ad=Kit.ART_OK;J=Kit.ART_PAGE;M=Kit.ART_PLAY;a_=Kit.ART_RESTORE;ar=Kit.CORNER_ART;v=Kit.GAP;u=Kit.HUE_BAD;L=Kit.HUE_GOOD;l=Kit.HUE_INFO;D=Kit.HUE_TEXT;E=Kit.HUE_TITLE;K=Kit.MARGIN;a0=Kit.MIN_TIP;a1=Kit.REAGENTS;a2=Kit.RESTORE_TIP;ax=Kit.SECTION_TILE;a3=Kit.WINDOW_BG;aJ=Kit.adapt;ay=Kit.add_check;e=Kit.add_label;ae=Kit.add_pic;B=Kit.add_section;az=Kit.add_textbox;R=Kit.add_tiled;af=Kit.add_window_frame;m=Kit.art_button;ag=Kit.attach;ak=Kit.basics;S=Kit.catcher;ai=Kit.client_control;aK=Kit.closed;F=Kit.count;a4=Kit.data_path;T=Kit.dispose;Z=Kit.find_item;C=Kit.fit;aa=Kit.flush;ab=Kit.get_var;aA=Kit.held_item;aL=Kit.hook_once;a5=Kit.in_pack;U=Kit.inert;z=Kit.is_open;a6=Kit.kv_load;a7=Kit.kv_save;aj=Kit.moved_by_code;aB=Kit.on_click;a8=Kit.on_client;a9=Kit.on_moved;V=Kit.pic_size;at=Kit.place;N=Kit.put_var;ba=Kit.save_min;bb=Kit.save_pos;aM=Kit.screen;O=Kit.set;A=Kit.set_text;bc=Kit.show_window;bd=Kit.text_px;o=Kit.text_w;be=Kit.title_bar;bf=Kit.title_catcher;bg=Kit.ui_pos;aC=Kit.veil;X=Kit.was_clicked;bh=Kit.weight_bar;al=Kit.with_tip;bi=Kit.write_safe;am=Kit.zone_up;bm="inventory";bn="Inventory"
	def aN():
		from System import AppDomain;from System.Reflection import BindingFlags
		for a in AppDomain.CurrentDomain.GetAssemblies():
			t=a.GetType("ClassicUO.Assets.TileDataLoader")
			if t is not None:return t.GetField("_staticData",BindingFlags.Static|BindingFlags.NonPublic)
		return
	au=("REAGENTS","POTIONS","SCROLLS","OTHER");an=tuple((bB.lower(),"REAGENTS")+a1[bB]for bB in("BP","BM","GA","GI","MR","NS","SS","SA"));an+=(("bw","REAGENTS","Bat Wing",3960),("gd","REAGENTS","Grave Dust",3983),("db","REAGENTS","Daemon Blood",3965),("nc","REAGENTS","Nox Crystal",3982),("pi","REAGENTS","Pig Iron",3978),("p_heal","POTIONS","Heal",3852),("p_cure","POTIONS","Cure",3847),("p_refresh","POTIONS","Refresh",3851),("p_str","POTIONS","Strength",3849),("p_agi","POTIONS","Agility",3848),("p_ns","POTIONS","Night Sight",3846),("p_expl","POTIONS","Explosion",3853),("p_poison","POTIONS","Poison",3850),("s_recall","SCROLLS","Recall",8012),("s_gate","SCROLLS","Gate Travel",8032),("s_mark","SCROLLS","Mark",8025),("s_gheal","SCROLLS","Greater Heal",8009),("s_heal","SCROLLS","Heal",7985),("s_cure","SCROLLS","Cure",7991),("s_acure","SCROLLS","Arch Cure",8005),("s_mr","SCROLLS","Magic Reflection",8016),("s_invis","SCROLLS","Invisibility",8024),("s_reveal","SCROLLS","Reveal",8028),("s_tele","SCROLLS","Teleport",8002),("s_prot","SCROLLS","Protection",7995),("s_bless","SCROLLS","Bless",7997),("s_res","SCROLLS","Resurrection",8039),("o_band","OTHER","Bandages",3617),("o_arrow","OTHER","Arrows",3903),("o_bolt","OTHER","Bolts",7163))
	def bj(g,graphic,hue,x,y,size):
		p=G.CreateGumpItemPic(graphic,size,size);p.SetRect(x,y,size,size)
		if hue:p.Hue=hue
		p.DrawBorder=False;p.SetAcceptMouseInput(False);g.Add(p)
	def P(n):return "{:,}".format(int(n))
	def bk(key,g,xy):
		a=aG(key)
		if a is None or xy is None or(xy[0],xy[1])==(a[0],a[1]):return
		g.SetPos(int(a[0]),int(a[1]));Kit.note_rect(g,a[0],a[1]);aj(g)
	aD=(("reagents","Reagents",(3962,3963,3972,3973,3974,3976,3980,3981)+(3960,3965,3978,3982,3983)),("gems","Gems",tuple(range(3855,3889))),("potions","Potions",tuple(range(3846,3854))),("scrolls","Scrolls",tuple(range(7981,8045))+(3827,)),("gold","Gold",(3821,3822,3823)),("bandages","Bandages",(3617,3817)),);Q=(("reagents","Reagents"),("potions","Potions"),("bandages","Bandages"),("gold","Gold and gems"),("scrolls","Scrolls"),("maps","Treasure maps"),("ores","Ores and ingots"),("wood","Wood"),("hides","Hides and cloth"),("food","Food"),("weapons","Weapons"),("armour","Armour"),("jewellery","Jewellery"),("keys","Keys and tools"));bo={"maps":("treasure map","tattered map","map"),"ores":(" ore","ingot"),"wood":("log","board"),"hides":("hide","leather","cloth","wool","cotton","flax","yarn","thread","bolt of"),"food":("bread","cake","muffin","pie","apple","pear","peach","grape","fish steak","ham","bacon","sausage","ribs","cheese","carrot","lettuce","cabbage","turnip","onion","melon","squash","gourd","lemon","lime","banana","date","coconut","chicken","bird","egg","cookie","wedge","corn","pumpkin","meat","jar of honey"),"keys":("key","tongs","hammer","saw","scissors","pickaxe","shovel","lockpick","sewing","tinker","mortar","fletcher","dovetail","skillet","rolling pin","scorp","plane","inshave","fishing pole","hatchet","smith")};bp=(6+2,10,14,18);bq=134217728;H={"data":None,"wanted":False}
	def bl(field):
		c=field.GetValue(None)if field is not None else None;a=dict((j,set())for j,n in Q)
		for k,i,d in aD:
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
					if f&bq:a["armour"].add(b)
					if bool(t.IsWearable)and int(t.Layer)in bp:a["jewellery"].add(b)
					if f&2097152 or bool(t.IsContainer):continue
					g=" "+e
					for k,h in bo.items():
						for w in h:
							if w in g:a[k].add(b);break
				except Exception:continue
		H["data"]=dict((p,frozenset(q))for p,q in a.items())
	def br(graphic):
		a=H["data"]or{}
		for k,b in Q:
			if graphic in a.get(k,()):return k
		return
	def bs():
		aH="bag";an="Bags"
		try:import clr;from System import Array,Object,Byte,Single,UInt16,UInt32;from System.Reflection import BindingFlags;de=True
		except Exception:de=False
		eF=8;b1,a1=1,50;bA=(142,94);df=(150,130);bc=600;cr=4;dg=30;eG,eH=104,64;eI=.1;eJ=.8;eK=.002;eL=3;eM=81;ct=1000;eN=(2330,2350);eO=(3834,8787,8786,9100,9120,11600);dh,di,eP=60,30,46;eQ=20;bO=20;eR="999";bP="UnifiedBag_shrunk";a5=44;cu=500;bQ=132;b2=116;aT=6;b3=8;cv=5;eS=9;b4=(36,32);bB=(60,80);eT=7012;eU=7013;dj=(2117,2118,2118);bR=4;eV=20;eW=24;dk=10;dl=0x7E57CA7C;eX=3;eY=.1;eZ=.05;e_=6;e0=8;e1=.5;e2=.09;e3=20;e4=4;e5=.3;b5=2;e6=200;dm=6;dn=5.;e7=1.3;do=1.;e8=1.;e9=3;fa=["fizzles","concentration is disturbed"];fb=["already casting","not yet recovered"];fc=["More reagents are needed"];fd=["Insufficient mana","not have enough mana"];bp=68;cx=8.;fe=.15;ff=2;cy=3000;cz=400;fg=8;dp=2.;fh=600;bC=.7;fi=600;dq=3;dr=2;b6=24;fj=125;fk=["cannot hold more"];fl=["must wait to perform another action"];fm=tuple(hM[0]for hM in aD);bD="#5C544A";ds="#7A7066";bd,aK,aC=L,l,u;cA="UnifiedBag_cmd";dt="UnifiedBag_state";du=aH
		class Bag(object):
			def __init__(self,**a):self.update(**a)
			def update(self,**a):self.__dict__.update(a)
		dv={};hJ=dict(dv);p={"cfg_bad":False,"slots":eF,"cols":0,"rows":0,"assign":{},"frame_x":200,"frame_y":120,"saved_fx":200,"saved_fy":120,"cell_w":bA[0],"cell_h":bA[1],"fit_pending":True,"fit_seen":None,"trim":True,"opacity":.9,"scale_pct":100,"scale_items":False,"driving":False,"drive_fixed":False,"drive_told":False,"hb_frame":-1,"hb_time":0.,"opacity_pending":None,"icons_used":None,"status_text":"","own_cell":None,"mgr_x":120,"mgr_y":140,"trp_x":200,"trp_y":180,"mgr_min":False,"trp_min":False,"minimized":False,"docked":False,"bare":False,"side_hidden":False,"link_state":None,"attach":None,"attach_g":None,"canvas":None,"side_pw":0,"detached_at":0.,"grid_wh":None,"names":{},"wait_player":False,"wait_load":False,"load_wanted":False,"load_text":None,"trap_sel":set(),"trap_extra":[],"job":None,"queue":[],"reported":False,"dirty_frame":True,"dirty_mgr":False,"dirty_trp":False,"open_mgr":False,"open_trp":False,"want_mgr":False,"want_trp":False,"save_in":-1,"to_write":None,"shutting":False,"flt_pick":None,"quick_at":0.,"filters":[],"open_flt":False,"dirty_flt":False,"flt_min":False,"flt_x":260,"flt_y":120,"rules":{},"sort":None,"srt_x":240,"srt_y":160,"srt_min":False,"open_srt":False,"want_srt":False,"dirty_srt":False,"layout":(),"geom":(1,bA[0],bA[1],0),"bar_raw":None,"grid_raw":None,"grid_info":(None,False),"slot_raws":(),"cats_seen":None};ap={"g":None,"c":{},"store":({},{}),"side_status":None,"bar":None,"grid":None,"mgr":None,"trp":None,"trap_checks":[],"srt":None,"rule_checks":[],"search_box":None,"counts":[],"count_state":{}};dw,dx,hK=ak(p,an)
		def av(kind,*a):
			def b(*b):dx.add((kind,)+a)
			return b
		def bE(key):T(ap.get(key));ap[key]=None
		def a7(x,y,w,h,color,alpha):b=G.CreateGumpColorBox(alpha,color);b.SetRect(x,y,w,h);return b
		def bg(g,text,x,y,hue=None):return U(e(g,text,x,y,hue))
		def b7(k,w,h,title,c,d):M=K;a=p[k+"_min"];g=G.CreateGump(True,True);at(g,p[k+"_x"],p[k+"_y"],w,h);af(g,w,h,corners=not a);B(g,M,M,w-2*M,30);e(g,title,M+30,M+7,E);bf(g,M,M,w-2*M-84,30,c,key="bag_"+k);b=({},{});m(g,b,"min",a_ if a else aZ,w-M-74,M+7,None,a2 if a else a0,on_click=c);m(g,b,"close",I,w-M-54,M+4,None,"Close this window",on_click=d);return g,b,M+30+v
		def b8(k,g,moved,**more):G.AddGump(g);a9(g,moved);ap[k]=g;ap.update(more)
		def bh():p["save_in"]=e3
		def bj():p["dirty_frame"]=True;bh()
		def bk(text,n):text=text or "";return text if len(text)<=n else text[:n-1]+"~"
		def a6(serial,c=True):
			a=p["names"].get(serial)
			if a is None:
				b=Z(serial)
				if not b:return "0x%08X (not loaded)"%serial
				a=b.Name or "Container"
				if len(p["names"])>=e6:p["names"]={}
				p["names"][serial]=a
			return("%s  0x%08X"%(a,serial))if c else a
		def dy():p["names"]={}
		al=Bag(tried=False,ok=False,can_ok=False,error="",f_tiles=None);r=Bag(frame=0,gumps={},managed=set(),trimmed=set(),bounds={},scale=1.,max_w=0,max_h=0,disabled=False,error="",fail_streak=0,open_count=0,catchers={},icons=None,hook_calls=0,pre_calls=0,glist=None,head=None,count=-1,lay=None,want=frozenset(),placed={},bar_at=None,full_frame=-1000,full_at=0.,fulls=0,labels_for=(None,None),meas={},opened=frozenset(),hold=None,ginfo={},catch_ok={},gtr={});au={"ver":0,"regions":{},"order":[],"orient":"rows","breaks":None,"sig":None,"items":None,"kinds":{},"size":None,"slow":False,"job":None};b9={"done":None};JR={"rd":None};bF={};bS=[];P={"ctrl":None,"rect":None,"texts":True,"said":None,"sum_i":0,"art":{},"world":None,"tiles":None,"prof_at":0.,"sum_at":0.,"hooked":False,"poked":set(),"poke_at":0.}
		def fo():
			if not de:al.error="clr module unavailable";return
			try:
				b=API.GetType().Assembly;clr.AddReference(b);from ClassicUO.Game.UI.Controls import Control;from ClassicUO.Game.UI.Gumps import ContainerGump;from ClassicUO.Game.UI.Controls import ClickPriority;a=BindingFlags.Instance|BindingFlags.NonPublic;c=BindingFlags.Static|BindingFlags.Public|BindingFlags.NonPublic;d=clr.GetClrType(ContainerGump);al.ContainerGump=ContainerGump;al.f_data=d.GetField("_data",a);al.f_pic=d.GetField("_gumpPicContainer",a);al.f_hit=d.GetField("_hitBox",a);e=clr.GetClrType(Control);al.m_offset=e.GetMethod("SetHitTestOffset",a);al.f_bounds=e.GetField("_bounds",a);al.Point=clr.GetPythonType(e.GetProperty("Location").PropertyType);al.Rect=clr.GetPythonType(al.f_bounds.FieldType);f=b.GetType("ClassicUO.Game.Managers.UIManager");al.p_gumps=f.GetProperty("Gumps",c);al.p_cscale=f.GetProperty("ContainerScale",c);h=b.GetType("ClassicUO.Configuration.ProfileManager");al.p_profile=h.GetProperty("CurrentProfile",c)
				for g in("f_data","f_pic","f_hit","m_offset","f_bounds","p_gumps","p_cscale","p_profile"):
					if getattr(al,g)is None:raise Exception("client member not found: "+g)
				class FrameHook(Control):
					def PreDraw(self):r.pre_calls+=1;r.hook_calls+=1;cC()
					def Draw(self,a,x,y):
						if r.pre_calls==0:r.hook_calls+=1;cC()
						return True
				class DropCatcher(Control):
					def Draw(self,a,x,y):return True
				al.Hook=FrameHook;al.Catcher=DropCatcher;al.LowPriority=ClickPriority.Low;al.ok=True
			except Exception as i:al.ok=False;al.error=str(i);return
			fp()
		def fp():
			al.can_ok=False
			try:
				from ClassicUO.Game.UI.Controls import Control,ItemGump
				class BagCanvas(Control):
					def Draw(self,a,x,y):
						try:w,h=self.va_wh
						except Exception:return True
						try:fz()
						except Exception:pass
						if a.ClipBegin(int(x),int(y),int(w),int(h)):
							try:
								Control.Draw(self,a,x,y)
								if P["texts"]:gc(a,int(x),int(y))
							finally:a.FlushBatch();a.ClipEnd()
						return True
					def OnMouseUp(self,x,y,button):
						try:
							if f4(int(x),int(y),button):return
						except Exception as e:r.error="canvas: %s"%e
						Control.OnMouseUp(self,x,y,button)
					def OnMouseDoubleClick(self,x,y,button):
						try:
							if f6(int(x),int(y),button):return True
						except Exception as e:r.error="canvas: %s"%e
						return Control.OnMouseDoubleClick(self,x,y,button)
					def OnMouseOver(self,x,y):
						try:f8(self,int(x),int(y))
						except Exception:pass
						Control.OnMouseOver(self,x,y)
				class BagLayer(Control):pass
				class CanvasItem(ItemGump):
					def OnMouseUp(self,x,y,button):al.up_item=self;ItemGump.OnMouseUp(self,x,y,button)
				al.Canvas,al.Layer,al.CanvasItem,al.ItemGump=(BagCanvas,BagLayer,CanvasItem,ItemGump);al.up_item=None;al.Mouse=Tz.T("ClassicUO.Input.Mouse");al.Actions=Tz.T("ClassicUO.Game.GameActions");al.f_tiles=aN();al.can_ok=True
			except Exception as e:al.can_ok=False;r.error="canvas: %s"%e
		def cB(a):
			try:return a()
			except Exception:return a(None)
		def dz(grid,tell):
			if not al.ok or r.disabled or p["drive_fixed"]:return
			try:
				a=cB(al.Hook);a.AcceptMouseInput=False;b=p["grid_info"][0]
				if b is not None and aO():
					with Kit.quiet:
						a.Parent=b
						if b.Children.Contains(a):return
				grid.Add(a)
			except Exception as e:
				p["driving"]=p["drive_fixed"]=True;r.error="draw hook: %s"%e
				if tell:API.SysMsg(an+": couldn't install the draw hook (%s); the script keeps the bags in place."%e,aK)
		def dA(grid):safe(lambda:setattr(grid,"LayerOrder",type(grid.LayerOrder).Under))
		dB={}
		def fq(w):return w.Gump
		fr=(fq,ai)
		def bm(a):
			if a is None:return
			t=type(a);b=dB.get(t)
			if b is not None:
				with Kit.quiet:
					v=b(a)
					if v is not None:return v
			for c in fr:
				if c is b:continue
				try:v=c(a)
				except Exception:continue
				if v is not None:dB[t]=c;return v
			return
		def bq(fn):return a8(fn,False)
		def cC():
			try:fx();r.fail_streak=0
			except Exception as e:r.error=str(e);r.fail_streak+=1
			except:r.error="unknown error";r.fail_streak+=1
			if r.fail_streak>120:r.disabled=True
		def dC(g,x,y):
			a=g.Offset
			if a.X!=x or a.Y!=y:al.m_offset.Invoke(g,Array[Object]([x,y]))
		def ca():
			b={};c=al.p_gumps.GetValue(None);r.glist=c;a=c.First
			while a is not None:
				v=a.Value
				if isinstance(v,al.ContainerGump)and not v.IsDisposed:b[int(v.LocalSerial)]=v
				a=a.Next
			r.gumps=b
			try:r.scale=float(al.p_cscale.GetValue(None))
			except Exception:pass
		def fs():
			b=r.glist
			if b is None:return
			a=b.First;d=a.Value if a is not None else None;e=b.Count
			if d is r.head and e==r.count:return
			r.head,r.count=d,e;f=r.want
			if not f:return
			g=r.gumps;n=0
			while a is not None and n<e0:
				v=a.Value
				if isinstance(v,al.ContainerGump)and not v.IsDisposed:
					c=int(v.LocalSerial)
					if c in f and g.get(c)is not v:g[c]=v
				a=a.Next;n+=1
		def ft(g):b=dS(g);s=r.scale;a,c=int(b[0]*s),int(b[1]*s);return a,c,int(b[2]*s)-a,int(b[3]*s)-c
		def dD(idx):b,c,d,a=p["geom"];r,e=divmod(idx,b);return p["frame_x"]+e*(c+a),p["frame_y"]+bu()+r*(d+a)
		def cD(c):a=c.Location;return int(a.X),int(a.Y)
		def bs(c,x,y):
			a=c.Location
			if a.X!=x or a.Y!=y:c.Location=al.Point(x,y)
		def cE(c):r=al.f_bounds.GetValue(c);return int(r.Width),int(r.Height)
		def cF(g):
			r.managed.discard(g);r.placed.pop(g,None);b=g in r.trimmed;r.trimmed.discard(g)
			if g.IsDisposed:r.catchers.pop(g,None);return
			dF(g)
			if not g.IsVisible:g.IsVisible=True
			dC(g,0,0);g.AcceptMouseInput=True;g.CanMove=True;a=al.f_pic.GetValue(g)
			if a is not None:a.Alpha=1.
			if b and not g.IsMinimized:g.RequestUpdateContents()
		def bG(g,c):
			a=g.Children
			while a.Contains(c):a.Remove(c)
		def dE(g,c):
			bG(g,c)
			if not c.IsDisposed:c.Dispose()
		def dF(g):
			r.catch_ok.pop(g,None);c=r.catchers.pop(g,None)
			if c is not None:dE(g,c)
		def fu(g):
			b=r.catchers.get(g)
			for a in list(g.Children):
				if a is not b and int(a.LocalSerial)==dl:dE(g,a)
		def fv(g,left,top,iw,d):
			c=r.catchers.get(g);a=g.Children;n=a.Count;b=r.catch_ok.get(g)
			if b is not None and c is not None and b[0]is c and b[1]==n and b[2]is(a[n-1]if n else None)and b[3]==(left,top,iw,d)and not c.IsDisposed:return
			if c is None or c.IsDisposed or not a.Contains(c):
				if g not in r.catchers:fu(g)
				c=al.Catcher();c.LocalSerial=dl;c.AcceptMouseInput=True;c.Priority=al.LowPriority;c.Parent=g;bG(g,c);a.Insert(0,c);r.catchers[g]=c
			elif a.IndexOf(c)!=0 or a.LastIndexOf(c)!=0:bG(g,c);a.Insert(0,c)
			e=al.f_bounds.GetValue(c)
			if(e.X,e.Y,e.Width,e.Height)!=(left,top,iw,d):al.f_bounds.SetValue(c,al.Rect(left,top,iw,d))
			if not c.IsVisible:c.IsVisible=True
			n=a.Count
			if len(r.catch_ok)>=cG:r.catch_ok.clear()
			r.catch_ok[g]=(c,n,a[n-1]if n else None,(left,top,iw,d))
		cG=64
		def cH(g):
			a=r.ginfo.get(g)
			if a is None:
				a=(int(g.Graphic),bool(g.IsChessboard or g.IsBackgammonBoard))
				if len(r.ginfo)>=cG:r.ginfo.clear()
				r.ginfo[g]=a
			return a
		def fw(g,idx,trim):
			if g.CanMove:g.CanMove=False
			dC(g,0,0);c,d=dD(idx);k=cH(g)[1]
			if g.IsMinimized or k or not trim:
				if g in r.trimmed:
					r.trimmed.discard(g);dF(g)
					if not g.IsMinimized:g.RequestUpdateContents()
				if not g.AcceptMouseInput and g.IsVisible:g.AcceptMouseInput=True
				a=al.f_pic.GetValue(g)
				if a is not None and abs(a.Alpha-p["opacity"])>.01:a.Alpha=p["opacity"]
				bs(g,c,d)
				if g.IsMinimized:return 0,0,a,False
				w,l=cE(g);return w,l,a,False
			e,f,h,i=ft(g);a=al.f_pic.GetValue(g)
			if a is not None and a.IsVisible:a.IsVisible=False
			b=al.f_hit.GetValue(g)
			if b is not None and b.IsVisible:b.IsVisible=False
			if g.AcceptMouseInput:g.AcceptMouseInput=False
			fv(g,e,f,h,i);bs(g,c-e,d-f);r.trimmed.add(g);j=int(round(eV*r.scale));return h+j,i+j,a,True
		def fx():
			if r.disabled or p["shutting"]:return
			B=p["bar_raw"];c,M=p["grid_info"];u=False;n=p["attach"];j=p["minimized"]
			if n is not None:
				j=j or not n.get("shown",True);e=gj()
				if e is not None and not e.IsDisposed:
					a,b=cD(e);a,b=a+int(n.get("dx",0)),b+int(n.get("dy",0));u=(a,b)!=r.bar_at;r.bar_at=(a,b);p["frame_x"],p["frame_y"]=a,b
					if c is not None and not c.IsDisposed:
						bs(c,a,b)
						if c.IsVisible==j:c.IsVisible=not j
			else:
				if M and c is not None and not c.IsDisposed:e,o,C=c,B,0
				else:e,o,C=B,c,a5
				if e is not None and not e.IsDisposed:
					a,b=cD(e);u=(a,b)!=r.bar_at;r.bar_at=(a,b);p["frame_x"],p["frame_y"]=a,b
					if o is not None and not o.IsDisposed:bs(o,a,b+C)
			q=p["layout"]
			if q is not r.lay:r.lay=q;r.want=frozenset([ah for by,ah in q])
			r.frame+=1;D=time.time();h=r.frame-r.full_frame>=e_ and D-r.full_at>=e2
			if h:r.full_frame,r.full_at=r.frame,D;r.fulls+=1;ca()
			else:fs()
			E=h;N=h and r.fulls%10==1;h=h or u;F=p["trim"];O=(F,p["opacity"],p["geom"],bu(),au["ver"]);s=set();f=set();v=x=0;i=None;Q=al.f_pic;G=p["canvas"]is not None and not j
			if G:H=P["rect"]or(0,0,0,0);R,S=p["frame_x"]+H[0],p["frame_y"]+H[1];T=h or p["driving"];U=(P["seen_n"],P["seen_last"],P["seen_min"])
			for d,k in q:
				g=r.gumps.get(k)
				if g is None:continue
				if g.IsDisposed:
					if E:continue
					E=True;ca();g=r.gumps.get(k)
					if g is None or g.IsDisposed:continue
				f.add(d)
				if G:
					try:
						if fy(g,k,R,S,T,U):
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
					I=bool(g.IsMinimized);J=(d,O,I);l=r.placed.get(g);m=Q.GetValue(g)
					if not h and l is not None and l[0]==J and m is l[2]and not(l[3]and m is not None and m.IsVisible):w,t=l[1]
					else:
						w,t,m,K=fw(g,d,F);r.placed[g]=(J,(w,t),m,K)
						if I:V,W=cE(g);r.meas[d]=(V,W,r.scale,True,None)
						else:r.meas[d]=(w,t,r.scale,False,int(g.Graphic)if K else None)
					v,x=max(v,w),max(x,t)
				except Exception as y:r.error="bag 0x%08X: %s"%(k,y)
			r.open_count=len(f)
			if f!=r.opened:
				r.opened=frozenset(f)
				for d in[ch for ch in r.meas if ch not in f]:r.meas.pop(d,None)
			if i is not None and N:
				try:X=int(al.f_data.GetValue(i).IconizedGraphic)or bB[1];r.icons=(int(i.Graphic),X)
				except Exception:pass
			if len(r.managed)>len(s):
				for g in[cs for cs in r.managed if cs not in s]:cF(g)
			r.max_w,r.max_h=v,x;z=p["slot_raws"]
			if f!=r.labels_for[0]or z is not r.labels_for[1]:
				for d,Y in enumerate(z):
					L=d not in f
					for A in Y:
						if A is not None and A.IsVisible!=L:A.IsVisible=L
				r.labels_for=(f,z)
		def fy(g,serial,px,py,b,seen):
			if cH(g)[1]:
				if g in r.managed:cF(g)
				return False
			if g.IsVisible:g.IsVisible=False
			if g.AcceptMouseInput:g.AcceptMouseInput=False
			if b:
				if g.CanMove:g.CanMove=False
				bs(g,px,py)
			a=g.Children;n=a.Count
			if seen[0].get(serial)!=n or seen[1].get(serial)is not(a[n-1]if n else None)or seen[2].get(serial)!=g.IsMinimized:
				if P["built"]==au["ver"]and P["ctrl"]is not None:ci(serial,g)
			return True
		def fz():
			b=r.gumps
			for c in au["order"]:
				a=au["kinds"].get(c)
				if a is None or a[0]=="board"or a[0]=="closed":continue
				g=b.get(a[2])
				if g is not None and g.IsVisible:g.IsVisible=False
		def dG():
			for g in list(r.managed):
				with Kit.quiet:cF(g)
		def fA(minimize):
			a=set(p["assign"].values())
			def b():
				ca();n=0
				for s in a:
					g=r.gumps.get(s)
					if g is None or g.IsDisposed or g.IsChessboard or g.IsBackgammonBoard:continue
					if bool(g.IsMinimized)!=minimize:g.IsMinimized=minimize;n+=1
				return n
			return bq(b)
		def dH():
			def a():a=al.p_profile.GetValue(None);return(int(a.ContainersScale),bool(a.ScaleItemsInsideContainers))
			return bq(a)
		def cb(pct,items):
			def a():
				a=al.p_profile.GetValue(None);c=(int(a.ContainersScale)!=pct or bool(a.ScaleItemsInsideContainers)!=items);a.ContainersScale=Byte(pct);a.ScaleItemsInsideContainers=items;al.p_cscale.SetValue(None,Single(pct/100.));r.scale=pct/100.
				if c:
					b=al.p_gumps.GetValue(None).First
					while b is not None:
						v=b.Value
						if isinstance(v,al.ContainerGump)and not v.IsDisposed:v.RequestUpdateContents()
						b=b.Next
				return c
			return bq(a)
		def dI(serial):
			if al.ok and not r.disabled:g=r.gumps.get(serial);return g is not None and not g.IsDisposed
			a=Z(serial);return bool(a)and z(safe(lambda:a.GetContainerGump()))
		def dJ():a=safe(lambda:int(API.Player.Serial),0);return a4("_unified_bag_%d.cfg"%a)
		def dK():dN(dM())
		def ba():
			p["save_in"]=-1
			if not aG()and p["canvas"]!="alone":p["saved_fx"],p["saved_fy"]=p["frame_x"],p["frame_y"]
			b=["slots=%d"%p["slots"],"cols=%d"%p["cols"],"rows=%d"%p["rows"],"frame_x=%d"%p["saved_fx"],"frame_y=%d"%p["saved_fy"],"cell_w=%d"%p["cell_w"],"cell_h=%d"%p["cell_h"],"trim=%d"%int(p["trim"]),"collapsed=%d"%int(p["minimized"]),"bare=%d"%int(p["bare"]),"side=%d"%int(p["side_hidden"]),"opacity=%d"%int(round(p["opacity"]*100)),"mgr_x=%d"%p["mgr_x"],"mgr_y=%d"%p["mgr_y"],"trp_x=%d"%p["trp_x"],"trp_y=%d"%p["trp_y"],"mgr_open=%d"%int(p["open_mgr"]),"mgr_min=%d"%int(p["mgr_min"]),"trp_open=%d"%int(p["open_trp"]),"trp_min=%d"%int(p["trp_min"]),"trapsel="+",".join(str(f)for f in sorted(p["trap_sel"])),"trapextra="+",".join(str(h)for h in p["trap_extra"]),]
			for a in sorted(p["assign"]):b.append("slot.%d=%d"%(a,p["assign"][a]))
			b+=["srt_x=%d"%p["srt_x"],"srt_y=%d"%p["srt_y"],"srt_open=%d"%int(p["open_srt"]),"srt_min=%d"%int(p["srt_min"])]
			for a in sorted(p["rules"]):
				c,d=p["rules"][a]
				if c or d:b.append("sort.%d=%s;%s"%(a,",".join(sorted(c)),",".join(str(i)for i in d)))
			p["to_write"]=(dJ(),"\n".join(b))
			if not safe(lambda:HOST.by_key[aH].running,False):cJ()
		def cI():return bool(aR(aH))
		def cJ():
			a=p["to_write"]
			if a is None:return
			p["to_write"]=None;b,c=a
			if p["cfg_bad"]:return
			try:bi(b,c)
			except Exception as e:API.SysMsg(an+": couldn't save its settings (%s)."%e,aC)
		def dL(text):return[int(a)for a in(text or "").split(",")if a.strip().isdigit()]
		def dM():return Kit.read_safe(dJ())
		def dN(raw):
			p["cfg_bad"]=raw is None
			if raw is None:API.SysMsg(an+": couldn't read its settings file, so changes aren't saved.",aC);return
			if not raw:return
			b,a={},{}
			for d in raw.splitlines():
				if "="in d:
					k,v=[n.strip()for n in d.split("=",1)];b[k]=v
					try:a[k]=int(v)
					except ValueError:pass
			p["slots"]=max(b1,min(a1,a.get("slots",p["slots"])));p["cols"]=max(0,min(a1,a.get("cols",0)));p["rows"]=max(0,min(a1,a.get("rows",0)));p["frame_x"],p["frame_y"]=aJ(a.get("frame_x",p["frame_x"]),a.get("frame_y",p["frame_y"]));p["saved_fx"],p["saved_fy"]=p["frame_x"],p["frame_y"];p["cell_w"]=max(20,min(bc,a.get("cell_w",p["cell_w"])));p["cell_h"]=max(20,min(bc,a.get("cell_h",p["cell_h"])));p["fit_pending"]="cell_w"not in a;p["opacity"]=max(10,min(100,a.get("opacity",a.get("panel_a",90))))/100.
			for g,k,h in(("trim","trim",1),("minimized","collapsed",0),("bare","bare",0),("side_hidden","side",0),("mgr_min","mgr_min",0),("trp_min","trp_min",0),("want_mgr","mgr_open",0),("want_trp","trp_open",0),("srt_min","srt_min",0),("want_srt","srt_open",0)):p[g]=a.get(k,h)==1
			for k in("mgr","trp","srt"):x,y=aJ(a.get(k+"_x",p[k+"_x"]),a.get(k+"_y",p[k+"_y"]));p.update(**{k+"_x":x,k+"_y":y})
			p["trap_sel"]=set(dL(b.get("trapsel")));p["trap_extra"]=dL(b.get("trapextra"));p["assign"],p["rules"]={},{}
			for k,v in b.items():
				e,j,i=k.partition(".")
				try:c=int(i)
				except ValueError:continue
				if not 0<=c<p["slots"]:continue
				if e=="slot"and a.get(k,0)>0:p["assign"][c]=a[k]
				elif e=="sort":
					f=fB(v)
					if f is not None:p["rules"][c]=f
		def fB(text):
			c,e,d=(text or "").partition(";");b=frozenset(f for f in(g.strip()for g in c.split(","))if f in fm);a=[]
			for p in d.split(","):
				p=p.strip()
				if p.isdigit()and 0<int(p)<=65535 and int(p)not in a:a.append(int(p))
			a=tuple(a[:b6]);return(b,a)if(b or a)else None
		aE={"told":None,"cols":None,"cell":None,"area":None}
		def dO(slots=None,cols=None,rows=None):
			slots=p["slots"]if slots is None else slots
			if cols is None and rows is None and aE["cols"]:c=max(1,min(slots,aE["cols"]));return c,int(math.ceil(slots/float(c)))
			cols=p["cols"]if cols is None else cols;rows=p["rows"]if rows is None else rows
			if cols>0 and rows>0:return cols,rows
			if cols>0:return cols,int(math.ceil(slots/float(cols)))
			if rows>0:c=int(math.ceil(slots/float(rows)));return c,int(math.ceil(slots/float(c)))
			c=max(1,int(math.ceil(math.sqrt(slots))));return c,int(math.ceil(slots/float(c)))
		def cc():return p["trim"]and al.ok and not r.disabled
		cd=[None,None]
		def cK():
			a=p["assign"]
			if a==cd[0]and p["slots"]==cd[1]:return
			b=tuple(sorted((c,d)for c,d in a.items()if c<p["slots"]))
			if b!=p["layout"]:p["layout"]=b
			cd[0],cd[1]=dict(a),p["slots"]
		def fC():
			s=r.scale if al.ok else 1.
			if cc():return int(bA[0]*s),int(bA[1]*s)
			return int(df[0]*s),int(df[1]*s)
		def cL():p["cell_w"],p["cell_h"]=fC();p["fit_pending"]=True;bj()
		def cM(g):
			i=max(g-2*(b3+aT),0);a,c=[[]],0
			for e in[("bagicons",b4[1]+22),("break",eS),("spellicons",b4[1]+22),("stop",22+4+18),("quick",4*24),("tools",24+26+24)]:
				f,h=e;d=h+(cv if a[-1]else 0)
				if a[-1]and c+d>i and f!="break":a.append([]);c,d=0,h
				if f=="break"and not a[-1]:continue
				a[-1].append(e);c+=d
			for b in a:
				while b and b[0][0]=="break":b.pop(0)
				while b and b[-1][0]=="break":b.pop()
			a=[k for k in a if k];j=[sum(q[1]for q in n)+cv*(len(n)-1)for n in a];return a,j
		def fD(graphic,x,y,b,c,tip,handler):a=G.CreateGumpPic(graphic);d=a.GetWidth()or b;e=a.GetHeight()or c;k=min(b/float(d),c/float(e),1.);w,h=max(1,int(d*k)),max(1,int(e*k));a.SetRect(x+(b-w)//2,y+(c-h)//2,w,h);O(a,"ContainsByBounds",True);a.SetTooltip(tip);G.AddControlOnClick(a,handler);return a
		def cN(grid,e,k,d=0):
			w,n=bv();i=n+bR;q,r=cM(k-i);f=len(q)*bQ+2*aT;b=max(k,max(r)+2*(b3+aT)+i);Kit.add_resizepic(grid,a3,e,d,f,b);B(grid,e+aT,d+aT,f-2*aT,b-2*aT);x,z=p["icons_used"]
			for j,A in enumerate(q):
				s=e+aT+j*bQ
				if j:grid.Add(U(a7(s,d+aT+b3,1,b-2*(aT+b3),bD,.8)))
				a=s+(bQ-b2)//2;y=d+(b-i-r[j])//2
				for c,t in A:
					if c in("bagicons","spellicons"):
						if c=="bagicons":u=((z,"Minimize every open slot bag",av("set_min",True),"Minimize"),(x,"Restore every minimized slot bag",av("set_min",False),"Restore"))
						else:u=((eT,"Cast Magic Trap on every ticked trap bag",av("start_job","Magic Trap"),"Trap"),(eU,"Cast Magic Untrap on every ticked trap bag",av("start_job","Magic Untrap"),"Untrap"))
						g=b2//2
						for v,(C,D,E,h)in enumerate(u):grid.Add(fD(C,a+v*g,y,g,b4[1],D,E));bg(grid,h,a+v*g+max(0,(g-o(h))//2),y+b4[1]+3,l)
					elif c=="stop":h=m(grid,ap["store"],"stop",I,a,y,"Stop","Stop the trap, untrap or sort run",on_click=av("stop_all"));ap["stop_ctrls"]=[ap["store"][0].get("stop"),h];ap["side_status"]=bg(grid,p["status_text"],a,y+26,l);ep()
					elif c=="quick":g3(grid,a,y)
					elif c=="tools":g1(grid,a,y)
					elif c=="break":grid.Add(U(a7(a,y+t//2,b2,1,bD,.8)))
					y+=t+cv
			bL(grid,e+f-aT-bR-w,d+b-aT-bR-n,False);return f,b
		def aG():return p["attach"]is not None
		def bt():return p["bare"]and not p["minimized"]and not aG()
		def fE():return ap.get("grid")if aG()or p["canvas"]=="alone"or bt()else ap.get("bar")
		def fF():
			if p["shutting"]or p["wait_player"]or not z(ap.get("grid")):return
			return "docked"if p["docked"]else("minimized"if p["minimized"]else "open")
		def bH(w,h,mode):
			f=(None,None);l=p["geom"]
			if not aG():
				d=(int(w),int(h))if(w is not None and h is not None)else None
				if(bI()and(d!=aE["told"]or(mode=="again"and d is not None))):p["dirty_frame"]=True
				aE["told"]=d
				if bI()and d is not None:return
			if w is not None and h is not None and l is not None:
				m,u,v,a=l;o=m*u+(m-1)*a;a=0 if cc()else cr;q=max(0,(p["grid_wh"][0]if p["grid_wh"]else o)-o)
				if aG():q=0 if bK()else p["side_pw"]
				g=int(w)-q;s=int(h)-bu();e,i=p["cell_w"],p["cell_h"];n=max(1,p["slots"]);b=None
				for c in range(1,n+1):
					r=int(math.ceil(n/float(c)));j=(g-(c-1)*a)//c;k=(s-(r-1)*a)//r
					if j<e or k<i:continue
					t=min(j/float(e),k/float(i))
					if b is None or t>b[0]:b=(t,c,j,k)
				if b is None:c=max(1,min(n,(g+a)//max(1,e+a)));r=int(math.ceil(n/float(c)));b=(0,c,max(e,(g-(c-1)*a)//c),max(i,(s-(r-1)*a)//r))
				f=(b[1],(b[2],b[3]))
			if f!=(aE["cols"],aE["cell"]):aE["cols"],aE["cell"]=f;p["dirty_frame"]=True
		def fG():
			i=0 if cc()else cr;c=0 if bK()else p["side_pw"];g=aE.get("area")
			if c and g is not None:m,j=bv();k,n=cM(g[1]-j-bR);c=len(k)*bQ+2*aT
			d=int(round(r.scale*100))if al.ok else p["scale_pct"];a=p["scale_pct"]if aP["pct"]is not None else d;l=dg if(al.ok and not r.disabled)else a
			if aP["pct"]is None or d==a:p["own_cell"]=(p["cell_w"],p["cell_h"],p["slots"]);e,f=float(p["cell_w"]),float(p["cell_h"])
			else:
				b=p["own_cell"]
				if b is not None and b[2]==p["slots"]:e,f=float(b[0]),float(b[1])
				else:h=a/float(max(1,d));e,f=p["cell_w"]*h,p["cell_h"]*h
			return e,f,i,p["slots"],c,a,a,min(l,a)
		bn={}
		def cO(h):
			k=("sw",h);v=bn.get(k)
			if v is None:
				c,a=bv();b,d=cM(h-a-bR);v=len(b)*bQ+2*aT
				if len(bn)>=200:bn.clear()
				bn[k]=v
			return v
		def bI():return al.ok and al.can_ok and not r.disabled
		def dP():
			if not bI()or p["minimized"]or p["docked"]or p["shutting"]:return
			if aG():return None if aE["area"]is None or not p["attach"].get("shown",True)else "combined"
			return "alone"if aE["told"]is not None and ac(aH)else None
		fH=120
		def dQ():return[("Settings",),("Trap bags",),("Slots",)]
		def cP(w):
			k=("tf",w,p["slots"]);v=bn.get(k)
			if v is None:
				a=Kit.title_plan(w,an,dQ(),str(p["slots"]));v=len(a[3])==len(dQ())and a[4]>=K+30+o("..")+Kit.TITLE_GAP
				if len(bn)>=200:bn.clear()
				bn[k]=v
			return v
		def dR(mode):
			if mode=="combined":b=aE["area"];a=0 if bK()else cO(b[1]);return 0,0,max(1,b[0]-a),max(1,b[1]),a
			w,h=aE["told"];M=K
			if p["bare"]or not cP(w):return M,M,max(1,w-2*M),max(1,h-2*M),0
			c=M+30+v;d=max(1,h-c-M);a=cO(d)
			if w-2*M-a<fH:a=0
			return M,c,max(1,w-2*M-a),d,a
		def dS(g,graphic=None):
			if graphic is None:graphic=int(g.Graphic)
			b=r.bounds.get(graphic)
			if b is None:a=al.f_data.GetValue(g).Bounds;b=(int(a.X),int(a.Y),int(a.Width),int(a.Height));r.bounds[graphic]=b
			return b
		def fI(g,graphic):return cH(g)[1]or graphic in eN
		def dT():
			d=[];e=set()
			for h,c in p["layout"]:
				if c in e:continue
				e.add(c);g=r.gumps.get(c);a,b="closed",0
				try:
					if g is not None and not g.IsDisposed:
						f=r.ginfo.get(g);b=f[0]if f is not None else int(g.Graphic)
						if fI(g,b):a="board"
						elif g.IsMinimized:a="mini"
						else:dS(g,b);a="open"
				except Exception:a,b="closed",0
				d.append((h,b,a,c))
			return tuple(d)
		def dU(items):
			a=[]
			for c,d,e,f in items:b=r.bounds.get(d)if e=="open"else None;w,h=(max(1,b[2]-b[0]),max(1,b[3]-b[1]))if b is not None else(eG,eH);a.append((c,float(w*h),w/float(h)))
			return a
		def dV(f,W,s):
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
		def dW(a,W,b,breaks):
			S=sum(f[1]for f in a);c,j=0.,0
			for k in breaks:
				d=sum(W*b*a[g][1]/S for g in range(j,k));h=d/W
				if h<=0:return float("inf")
				for i in range(j,k):w=(W*b*a[i][1]/S)/h;c+=a[i][1]*math.log((w/h)/a[i][2])**2
				j=k
			return c
		def dX(a,W,b,keep=None):
			if not a:return "rows",[],0.
			d,i=dV(a,W,b);e=[(k,n,1./q)for k,n,q in a];f,j=dV(e,b,W);g=("columns",j,f)if f<eJ*d else("rows",i,d)
			if keep is not None and keep[1]and keep[1][-1]==len(a):
				o,c=keep;h=dW(a,W,b,c)if o=="rows"else dW(e,b,W,c)
				if not g[2]<(1.-eI)*h:return o,list(c),h
			return g
		def dY(a,W,b,orient,breaks):
			if not a:return{}
			if orient=="columns":return dict((q,(G,t,by,ah))for q,(t,G,ah,by)in dY(a,b,W,"rows",breaks).items())
			S=sum(s[1]for s in a);e={};j,f,c=0,0.,0;n=len(a)
			for k in breaks:
				g=sum(W*b*a[w][1]/S for w in range(j,k));f+=g;h=int(round(f/W))if k<n else b;l,d=0.,0
				for i in range(j,k):l+=W*b*a[i][1]/S;m=int(round(W*l/g))if i<k-1 else W;e[a[i][0]]=(d,c,m-d,h-c);d=m
				c=h;j=k
			return e
		def fJ(b,d,ah,cs,x,y):
			a=b[2]-int(d/cs);c=b[3]-int(ah/cs)
			if x<b[0]:x=b[0]
			elif x>a:x=a
			if y<b[1]:y=b[1]
			elif y>c:y=c
			return x,y
		def ce(a):return a[2]>=dh and a[3]>=di+bO
		def dZ(a):
			if ce(a):b,c,d,e=a;return b,c+bO,d,e-bO
			return a
		def d_(a,ah,cs):return(float(a),float(ah))if au.get("si")else(a/cs,ah/cs)
		def d0(box,pw,ph):
			a,b,g,h=box;c,d=a+pw//2,a+g-1-(pw-pw//2);e,f=b+ph//2,b+h-1-(ph-ph//2)
			if d<c:c=d=a+g//2
			if f<e:e=f=b+h//2
			return c,d,e,f
		def fK(b,box,f,ah,cs,g,by):a,c=d_(f,ah,cs);d,e=float(max(1,b[2]-b[0])),float(max(1,b[3]-b[1]));u=.5 if a>=d else(g+a/2.-b[0])/d;v=.5 if c>=e else(by+c/2.-b[1])/e;u=0. if u<0 else(1. if u>1 else u);v=0. if v<0 else(1. if v>1 else v);return box[0]+u*box[2],box[1]+v*box[3]
		def fL(b,box,a,ah,cs,px,py):c,d=d_(a,ah,cs);u=(px-box[0])/float(max(1,box[2]));v=(py-box[1])/float(max(1,box[3]));u=0. if u<0 else(1. if u>1 else u);v=0. if v<0 else(1. if v>1 else v);e=int(round(b[0]+u*(b[2]-b[0])-c/2.));f=int(round(b[1]+v*(b[3]-b[1])-d/2.));return e,f
		def fM(a,ah):
			if au.get("si"):b=r.scale or 1.;return max(1,int(a*b)),max(1,int(ah*b))
			return a,ah
		def fN(slot):
			b=au["regions"].get(slot);a=au["kinds"].get(slot)
			if b is None or a is None:return
			return a[2],dZ(b),r.bounds.get(a[1]),r.scale or 1.
		def fO(d,serial,l,ah,pw,ph,e,by):
			if d is None:return 0,0
			m,f,g,n=d;a=bF.get(serial)
			if a is not None and a[0]==m and a[1]==e and a[2]==by:return int(a[3])-pw//2,int(a[4])-ph//2
			h,i,j,k=d0(f,pw,ph)
			if g is None:b,c=(h+i)//2,(j+k)//2
			else:b,c=fK(g,f,l,ah,n,e,by);b=max(h,min(i,b));c=max(j,min(k,c))
			return int(round(b))-pw//2,int(round(c))-ph//2
		def fP(serial,bag,a,by,b,c):
			if serial not in bF:
				if len(bS)>=ct:
					for s in bS[:ct//2]:bF.pop(s,None)
					del bS[:ct//2]
				bS.append(serial)
			bF[serial]=(bag,a,by,b,c)
		def d1():bF.clear();del bS[:]
		def fQ():
			a=time.time()
			if a>=P["prof_at"]:
				P["prof_at"]=a+1.
				try:p["scale_items"]=bool(al.p_profile.GetValue(None).ScaleItemsInsideContainers)
				except Exception:pass
			return p["scale_items"]
		def d2(sig,items,h,W,a,plan):
			b,c,l=plan;i=dY(h,W,a,b,c);d,e={},{}
			for f,j,k,g in items:d[f]=(k,j,g);e[g]=f
			au.update({"ver":au["ver"]+1,"regions":i,"slot_of":e,"order":[n[0]for n in items],"orient":b,"breaks":list(c),"sig":sig,"items":items,"kinds":d,"size":(W,a),"si":sig[4]});d1()
		def bT():
			try:return cV()is not None
			except Exception:return False
		def d3(mode):
			if p["canvas"]is not None:cR()
			p["canvas"]=mode;r.placed.clear();p["dirty_frame"]=True
		def fR():
			c=dP()
			if c!=p["canvas"]:
				if bT():return
				d3(c)
			if c is None:return
			d=dR(c);b=dT();a=(d[2],d[3],b,round(r.scale or 1.,4),fQ());e=b9["done"]
			if e is not None and len(e)>1 and e[0]==a and au["job"]==a:
				if bT():return
				d2(*e);au["job"]=None;au["pending"]=None;return
			if a==au["sig"]:au["job"]=None;au["pending"]=None;return
			if a==au["job"]or bT():return
			W,g=d[2],d[3];f=dU(b);h=None
			if au["items"]==b and au["breaks"]is not None:h=(au["orient"],au["breaks"])
			if au["slow"]:au["job"]=a;au["pending"]=(a,b,f,W,g,h);return
			i=time.time();j=dX(f,W,g,h)
			if time.time()-i>eK and len(f)>8:au["slow"]=True
			d2(a,b,f,W,g,j)
		def d4():a,b=au.get("pending"),b9["done"];return a is not None and(b is None or b[0]!=a[0])
		def fS():
			a=au.get("pending")
			if a is None or not d4():return
			b,e,c,W,d,f=a
			try:b9["done"]=(b,e,c,W,d,dX(c,W,d,f))
			except Exception:b9["done"]=(b,)
		def d5():
			c=P["ctrl"]
			if c is None:return
			with Kit.quiet:
				p=c.Parent
				if p is not None:bG(p,c)
		def fT(raw,index,x,y,w,h):
			c=P["ctrl"]
			if c is None or c.IsDisposed:cQ();c=cB(al.Canvas);c.AcceptMouseInput=True;c.Priority=al.LowPriority;P["ctrl"]=c
			c.va_wh=(int(w),int(h));c.Parent=raw;a=raw.Children
			while a.Contains(c):a.Remove(c)
			a.Insert(min(index,a.Count),c);al.f_bounds.SetValue(c,al.Rect(int(x),int(y),int(w),int(h)));P["rect"]=(int(x),int(y),int(w),int(h))
			for b in P["layers"].values():al.f_bounds.SetValue(b,al.Rect(0,0,int(w),int(h)))
		def cQ():P.update({"built":-1,"bsize":None,"parts":[],"icons":[],"bg":None,"layers":{},"pool":{},"owner":{},"items":{},"seen_n":{},"seen_last":{},"seen_min":{},"spot":{},"label":{},"count":{},"tip":None,"sums":{},"say_lbl":None,"sum_part":None,"alpha_set":None,"say_shown":False})
		cQ()
		def cR():
			d5();c=P["ctrl"];P["ctrl"]=None
			if c is not None:safe(c.Dispose)
			cQ();P["rect"]=None;d1();au.update({"sig":None,"items":None,"breaks":None,"regions":{},"kinds":{},"slot_of":{},"order":[],"job":None,"pending":None,"size":None});au["ver"]+=1;ap["counts"]=[];ap["count_state"]={}
		def d6():
			a=p["opacity"];b=P["bg"];c=(a,b)
			if P["alpha_set"]==c:return
			for d in([b]if b is not None else[])+P["icons"]:
				with Kit.quiet:
					if abs(float(d.Alpha)-a)>.001:d.Alpha=a
			P["alpha_set"]=c
		def d7(w):
			a=bm(w)if w is not None else None
			if a is None:return
			a.Parent=P["ctrl"];a.AcceptMouseInput=False;return a
		def fU():
			k=P["ctrl"];f=ap.get("grid")
			if k is None or f is None:return
			for E in P["parts"]:
				with Kit.quiet:bG(k,E);E.Dispose()
			P["parts"],P["icons"],P["label"],P["count"]=[],[],{},{};P["tip"]=None;P["alpha_set"]=None;F=P["say_lbl"];P["say_lbl"]=None
			if F is not None:safe(F.Dispose)
			W,m=au["size"]or(P["rect"][2],P["rect"][3]);n,v=au["regions"],au["kinds"];c=[];c.append((R(f,ax,0,0,W,m,p["opacity"]),"bg"))
			for a in au["order"]:
				x,y,w,h=n[a]
				if x+w<W:c.append((a7(x+w-1,y,1,h,bD,.8),"seam"))
				if y+h<m:c.append((a7(x,y+h-1,w,1,bD,.8),"seam"))
			for a in au["order"]:
				g,Q,d=v[a]
				if g!="mini":continue
				o=r.gumps.get(d)
				try:z=int(al.f_data.GetValue(o).IconizedGraphic)or bB[1]
				except Exception:z=bB[1]
				x,y,w,h=n[a];A,B=V(z);A,B=(A or 30),(B or 30);c.append((ae(f,z,x+(w-A)//2,y+(h-B)//2,mouse=False),"icon"))
			for a in au["order"]:c.extend(fV(f,a,n[a],v[a]))
			if not au["order"]:
				for S,T in enumerate(Kit.wrap("No bags yet. Click Slots to add some.",max(60,W-16))[:3]):c.append((e(f,T,8,8+20*S,l),"lbl"))
			G=[]
			for U in range(p["slots"]):q=e(f,"",0,0,L);O(q,"IsVisible",False);i=n.get(U);G.append((q,i[0],i[1],i[2],i[3])if i else(q,0,0,0,0));c.append((q,"count"))
			aa();H=len([ah for ah in c if ah[1]!="count"]);t=[]
			for w,g in c:
				j=d7(w)
				if j is None:continue
				t.append(j)
				if g=="bg":P["bg"]=j
				elif g=="icon":j.Alpha=p["opacity"];P["icons"].append(j)
			P["parts"]=t;C=P["layers"];D={}
			for a in au["order"]:
				b=C.pop(a,None)
				if b is None or b.IsDisposed:b=cB(al.Layer);b.AcceptMouseInput=False
				al.f_bounds.SetValue(b,al.Rect(0,0,int(W),int(m)));D[a]=b
			if C:
				I=list(C.values());X=P["pool"];J=[]
				for s in P["owner"]:
					K=X.get(s)
					if K is not None:
						Y=K.Parent
						for b in I:
							if Y is b:J.append(s);break
				for s in J:cg(s)
				for b in I:safe(b.Dispose)
			P["layers"]=D;M=k.Children;N=t[:H]+[D[by]for by in au["order"]]+t[H:]
			for u in N:u.Parent=k
			Z=set(N)
			for u in list(M):
				if u not in Z:M.Remove(u)
			ap["counts"]=G;ap["count_state"]={};P["built"]=au["ver"];P["bsize"]=(W,m);P["seen_n"],P["seen_last"],P["seen_min"]={},{},{}
			for a in au["order"]:
				g,Q,d=v[a];o=r.gumps.get(d)
				if o is not None and g in("open","mini"):ci(d,o)
				elif P["items"].get(d):
					for s in list(P["items"][d]):cg(s)
					P["items"][d]=[]
			if SR["counts"]:cm()
		def fV(grid,slot,h,info):
			b,p,f=info;x,y,w,i=h
			if w<dh or i<di:return[]
			if b=="open"and not ce(h):return[]
			a=[];j="#%d"%(slot+1);a.append((e(grid,j,x+5,y+3,E),"lbl"));c=x+5+o(j)+6
			if b=="board":d=C("Game board",max(8,x+w-4-c));a.append((e(grid,d,c,y+3,l),"lbl"));return a
			g=a6(f,False);m=x+w-c-(6+o(eR)if b=="open"else 0)-10;d=C(g,max(8,m));a.append((e(grid,d,c,y+3,l),"lbl"));P["label"][slot]=(g,d!=g)
			if b=="open":n=len(P["items"].get(f)or());k=e(grid,str(n),c+o(d)+6,y+3,l);P["count"][f]=k;a.append((k,"lbl"))
			elif i>=eP:a.append((e(grid,"Minimized"if b=="mini"else "Closed",x+5,y+3+eQ,l),"lbl"))
			return a
		def cf(g):
			w=P["world"]
			if w is None:
				try:w=P["world"]=g.World
				except Exception:w=None
			return w
		def fW(g,serial):
			w=cf(g)
			try:return w.Get(UInt32(int(serial)))if w is not None else None
			except Exception:return
		def cS(b,graphic):
			r=al.f_bounds.GetValue(b);a=(int(r.Width),int(r.Height))
			if graphic not in P["art"]:
				if len(P["art"])>2000:P["art"].clear()
				P["art"][graphic]=a
			return a
		def fX(graphic):
			b=P["art"].get(graphic)
			if b is not None:return b
			g=p["grid_raw"]
			try:a=al.CanvasItem(g,UInt32(0),UInt16(int(graphic)),UInt16(0),0,0,False)
			except Exception:return 44,44
			try:return(1,1)if a.IsDisposed else cS(a,graphic)
			finally:safe(a.Dispose)
		def cg(serial):
			c=P["pool"].pop(serial,None);b=P["owner"].pop(serial,None);P["spot"].pop(serial,None)
			if c is not None:
				try:
					p=c.Parent
					if p is not None:bG(p,c)
					c.Dispose()
				except Exception:pass
			if b is not None:
				a=P["items"].get(b)
				if a and serial in a:a.remove(serial)
		def ci(bag,g):
			u=g.Children;n=u.Count;F=bool(g.IsMinimized);P["seen_n"][bag]=n;P["seen_last"][bag]=u[n-1]if n else None;P["seen_min"][bag]=F;j=au["slot_of"].get(bag);v=P["layers"].get(j)if j is not None else None
			if v is None:return
			G=[]
			if not F and au["kinds"][j][0]=="open":
				for k in range(n):
					a=u[k]
					if isinstance(a,al.ItemGump)and not a.IsDisposed:G.append(a)
			w,l=P["pool"],P["owner"];H=P["items"].get(bag)or[];m=[];e=[];I=cf(g);Q=fN(j);R=au.get("si");J=r.scale or 1.;S=P["spot"];T,K,o=al.CanvasItem,UInt32,UInt16;t=0
			for a in G:
				s=int(a.LocalSerial);d=int(a.Graphic)
				try:b=I.Get(K(s))if I is not None else None
				except Exception:b=None
				f=int(b.Hue)if b is not None else int(a.Hue);c=w.get(s)
				if c is not None and c.IsDisposed:cg(s);c=None
				if c is None:
					try:c=T(g,K(s),o(d),o(f),0,0,False)
					except Exception:continue
					if c.IsDisposed:continue
					c.va_art=cS(c,d);c.va_gr,c.va_hue,c.va_sz,c.va_xy=d,f,None,None;w[s]=c
				elif c.va_gr!=d:
					c.Graphic=o(d)
					if c.IsDisposed:w.pop(s,None);l.pop(s,None);continue
					c.va_art=cS(c,d);c.va_gr,c.va_sz=d,None
				if c.va_hue!=f:c.Hue=o(f);c.va_hue=f
				z=l.get(s)
				if z is not None and z!=bag:
					B=P["items"].get(z)
					if B and s in B:B.remove(s)
				l[s]=bag;C,D=c.va_art;h,i=(max(1,int(C*J)),max(1,int(D*J)))if R else(C,D)
				if c.va_sz!=(h,i):
					p=al.f_bounds.GetValue(c)
					if int(p.Width)!=h or int(p.Height)!=i:al.f_bounds.SetValue(c,al.Rect(int(p.X),int(p.Y),h,i))
					c.va_sz=(h,i)
				L,M=(int(b.X),int(b.Y))if b is not None else cD(a);x,y=fO(Q,s,C,D,h,i,L,M)
				if c.va_xy!=(x,y):bs(c,x,y);c.va_xy=(x,y)
				S[s]=(x+h//2,y);m.append(s);e.append(c)
				if b is None:t+=s
				else:
					try:N=int(b.Amount)
					except Exception:N=0
					t=(t*31+s*7+L*131+M*137+f*139+N*149)&0x7FFFFFFF
			if H:
				U=set(m)
				for s in H:
					if s not in U and l.get(s)==bag:cg(s);bF.pop(s,None)
			P["items"][bag]=m;q=v.Children;E=q.Count==len(e)
			if E:
				for k in range(len(e)):
					if q[k]is not e[k]:E=False;break
			if not E:
				for c in e:c.Parent=v
				V=set(e)
				for c in list(q):
					if c not in V:q.Remove(c)
			O=P["count"].get(bag)
			if O is not None:A(O,str(len(m)))
			P["sums"][bag]=t
		def d8(g,b,t=0):
			w=cf(g);c=UInt32
			for s in b:
				try:a=w.Get(c(int(s)))if w is not None else None
				except Exception:a=None
				if a is None:t+=s;continue
				t=(t*31+s*7+int(a.X)*131+int(a.Y)*137+int(a.Hue)*139+int(a.Amount)*149)&0x7FFFFFFF
			return t
		d9=.2;fY=30;fZ=.1;f_=40
		def f0(*c):
			a=P["poked"]
			if p["shutting"]or len(a)>=f_:return
			d=au.get("slot_of",())
			for b in c:
				try:s,e=int(b.Serial),int(b.Container)
				except Exception:continue
				for k in(e,s):
					if k in d:a.add(k)
				return
		def f1():
			d=time.time();f=P["poked"]
			if f and d>=P["poke_at"]:
				P["poke_at"]=d+fZ;k=list(f);f.difference_update(k)
				for a in k:
					g=r.gumps.get(a)
					if g is not None and not g.IsDisposed:ci(a,g)
			h=au["order"]
			if not h:return
			if 0<=P["sum_at"]-d<=d9:return
			P["sum_at"]=d+d9;e=P["sum_part"]
			if e is not None:
				a,g,b,n,c,i,t=e
				if P["items"].get(a)is not b or len(b)!=n or g.IsDisposed or r.gumps.get(a)is not g:e=None;P["sum_part"]=None
			if e is None:
				i=P["sum_i"]%len(h);P["sum_i"]=i+1;l,m,a=au["kinds"][h[i]]
				if l!="open":return
				g=r.gumps.get(a)
				if g is None or g.IsDisposed:return
				b=P["items"].get(a);c=tuple(b)if b else();n,i,t=len(b)if b is not None else-1,0,0
			j=i+fY
			if j<len(c):P["sum_part"]=(a,g,b,n,c,j,d8(g,c[i:j],t));return
			P["sum_part"]=None
			if d8(g,c[i:],t)!=P["sums"].get(a):ci(a,g)
		def cT(serial,hue):
			c=P["pool"].get(serial)
			if c is None:return
			h=int(hue)&65535
			try:
				if not c.IsDisposed and c.va_hue!=h:c.Hue=UInt16(h);c.va_hue=h
			except Exception:pass
		def bJ(x,y):
			for a in au["order"]:
				r=au["regions"].get(a)
				if r is not None and r[0]<=x<r[0]+r[2]and r[1]<=y<r[1]+r[3]:return a
			return
		def cU(graphic):
			a=P["tiles"]
			if a is None:
				if al.f_tiles is None:return
				a=P["tiles"]=al.f_tiles.GetValue(None)
			return None if a is None or graphic<0 or graphic>=a.Length else a[graphic]
		def f2(it,hold):
			try:a=int(it.Graphic)
			except Exception:return True
			if a in eO:return True
			t=cU(a)
			if t is None:return True
			try:return True if bool(t.IsContainer)else bool(t.IsStackable)and a==int(Tz.get(hold,"Graphic"))
			except Exception:return True
		def ea(serial,button):
			a=P["owner"].get(serial);g=r.gumps.get(a)if a is not None else None
			if g is None or g.IsDisposed:return False
			g.OnMouseUp(0,0,button);return True
		def f3(bag):
			g=r.gumps.get(bag);w=cf(g)if g is not None else P["world"]
			if w is None:return True
			try:
				a=w.Get(UInt32(int(bag)))
				if a is None:return True
				b=w.Get(a.RootContainer);return b is None or int(b.Distance)<=eL
			except Exception:return True
		def eb():API.PlaySound(eM)
		def f4(x,y,button):
			f=str(button);c=al.up_item;al.up_item=None;b=int(c.LocalSerial)if c is not None and not c.IsDisposed else None
			if f=="Left":
				d=cV()
				if d is not None:
					if b is not None:
						g=fW(r.gumps.get(P["owner"].get(b)),b)
						if g is not None and f2(g,d):return ea(b,button)
					a=bJ(x,y)
					if a is None:return True
					f5(a,x,y,d);return True
				if p["flt_pick"]is not None:
					a=bJ(x,y)
					if a is not None:
						e=au["kinds"].get(a);h=dict((q,n)for n,q in p["layout"])
						if e is not None and e[2]in h:av("filter_canvas_pick",h[e[2]])();return True
				if b is not None:
					if not P["texts"]and not API.HasTarget():P["said"]=(b,time.time())
					return ea(b,button)
				a=bJ(x,y)
				if a is None:return False
				j,l,k=au["kinds"][a];i=au["regions"][a]
				if j=="open"and ce(i)and y<i[1]+bO and not API.HasTarget():av("bag_min",k,True)();return True
				return False
			if f=="Right":
				if b is not None:return True
				a=bJ(x,y)
				if a is not None and au["kinds"][a][0]=="open":av("bag_close",au["kinds"][a][2])();return True
			return False
		def f5(slot,x,y,hold):
			o,p,a=au["kinds"][slot]
			if not f3(a):eb();return
			b=int(Tz.get(hold,"Serial"))
			if b==a:eb();return
			import System;c=r.bounds.get(p)if o=="open"else None
			if c is None:Tz.call(None,"DropItem",(System.UInt32(b),65535,65535,0,System.UInt32(int(a)),False),al.Actions);return
			d,e=x,y
			with Kit.quiet:
				if bool(al.p_profile.GetValue(None).RelativeDragAndDropItems):h=Tz.get(hold,"MouseOffset");d,e=d+int(h.X),e+int(h.Y)
			f,g=fX(int(Tz.get(hold,"DisplayedGraphic")));q,s=fM(f,g);i=r.scale or 1.;j=dZ(au["regions"][slot]);t,u,v,w=d0(j,q,s);k=max(t,min(u,d));l=max(v,min(w,e));z,A=fL(c,j,f,g,i,k,l);m,n=fJ(c,f,g,i,z,A);Tz.call(None,"DropItem",(System.UInt32(b),m,n,0,System.UInt32(int(a)),False),al.Actions);fP(b,int(a),m,n,k,l);safe(lambda:Tz.put(None,"CancelDoubleClick",True,al.Mouse))
		def f6(x,y,button):
			if str(button)!="Left":return False
			a=bJ(x,y)
			if a is None:return False
			b,d,c=au["kinds"][a]
			if b in("closed","board"):av("bag_use",c)();return True
			if b=="mini":av("bag_min",c,False)();return True
			return False
		f7={"closed":"Double-click to open; drop an item to put it in","mini":"Double-click to restore; drop an item to put it in","board":"Double-click to open the board; drop an item to put it in","body":"Right-click to close","line":"Click to minimize"}
		def f8(c,x,y):
			a=bJ(x,y);b=None
			if a is not None:
				e=au["kinds"][a][0];b=e
				if e=="open":r=au["regions"][a];b="line"if ce(r)and y<r[1]+bO else "body"
			f=(a,b,au["ver"])
			if f==P["tip"]:return
			P["tip"]=f;g=f7.get(b,"")
			if b=="line":
				d=P["label"].get(a)
				if d is not None and d[1]:g="%s. Click to minimize"%d[0]
			c.SetTooltip(g)
		def f9(bag):API.UseObject(bag)
		def ga(bag,value):
			g=r.gumps.get(bag)
			if g is not None and not g.IsDisposed and bool(g.IsMinimized)!=value:g.IsMinimized=value
		def gb(bag):
			g=r.gumps.get(bag)
			if g is not None and not g.IsDisposed:g.Dispose()
		def gc(h,sx,sy):
			try:
				i=P["spot"];c=r.gtr
				for j in au["order"]:
					d=au["kinds"][j]
					if d[0]!="open":continue
					g=r.gumps.get(d[2])
					if g is None:continue
					a=c.get(g)
					if a is None:
						a=g.TextRenderer
						if len(c)>=cG:c.clear()
						c[g]=a
					o=a.DRight
					if o is None:continue
					while o is not None:
						e=o.Owner
						if not o.IsDestroyed and e is not None and o.TextBox is not None:
							try:f=int(e.Serial or 0)
							except Exception:f=0
							b=i.get(f)
							if b is not None:o.X,o.Y=b[0],b[1];k,l=cE(o.TextBox);o.RealScreenPosition=al.Point(b[0]-(k>>1),b[1]-int(o.OffsetY)-l)
						o=o.DRight
					a.Draw(h,sx,sy,True)
			except Exception as m:P["texts"]=False;r.error="canvas texts: %s"%m
		gd=4.;ge=1.5
		def gf(now):
			if P["texts"]or p["canvas"]is None:return
			a=P["say_lbl"];d=P["said"];f=JR["rd"]
			if d is not None and f is not None:
				j,g=d
				for b in f.new():
					if b.at<g-.05 or ":"in b.text[:24]:continue
					c=P["spot"].get(j);P["said"]=None
					if c is None or P["ctrl"]is None:break
					if a is None:
						h=ap.get("grid")
						if h is None:break
						a=e(h,"",0,0,D);aa();d7(a);P["say_lbl"]=a
					i=C(b.text,200);A(a,i);a.SetPos(max(0,c[0]-o(i)//2),max(0,c[1]-18));a.IsVisible=True;P["say_shown"]=True;P["say_until"]=now+gd;break
				else:
					if now-g>ge:P["said"]=None
			if a is not None and P["say_shown"]and now>=P.get("say_until",0.):P["say_shown"]=False;O(a,"IsVisible",False)
		def cV():
			h=r.hold
			if h is None:a=Tz.get(None,"Game",Tz.T("ClassicUO.Client"));h=r.hold=Tz.get(Tz.get(a,"UO"),"GameCursor");h=r.hold=Tz.get(h,"ItemHold")
			return None if not bool(Tz.get(h,"Enabled"))or bool(Tz.get(h,"IsFixedPosition"))else h
		aP={"pct":None}
		def cW():a=aP["pct"];return(a,True)if a is not None and a<p["scale_pct"]else(p["scale_pct"],p["scale_items"])
		def cX():
			if aP["pct"]is None:N(bP,"")
			else:N(bP,"%d|%d"%(p["scale_pct"],1 if p["scale_items"]else 0))
		def cY(pct):
			if pct is not None and not(al.ok and not r.disabled and aG()):pct=None
			if pct is not None and bI():pct=None
			if pct is not None and aP["pct"]is None:
				a=safe(dH)
				if a:p["scale_pct"],p["scale_items"]=a
			if pct is not None:
				pct=max(dg,int(pct))
				if pct>=p["scale_pct"]:pct=None
			if pct==aP["pct"]:return
			c=aP["pct"];b=r.scale;aP["pct"]=pct
			try:cb(*cW())
			except Exception as e:aP["pct"]=c;API.SysMsg(an+": couldn't change the bag scale (%s)."%e,aC);return
			cX()
			if b>0 and r.scale>0:f=r.scale/b;p["cell_w"]=max(1,min(bc,int(round(p["cell_w"]*f))));p["cell_h"]=max(1,min(bc,int(round(p["cell_h"]*f))))
			p["fit_pending"]=True;bj()
			if not(p["job"]or p["sort"]):aQ("Idle")
		def gg():
			c=ab(bP)
			if not c:return
			a=c.split("|")
			try:b,d=int(a[0]),(len(a)>1 and a[1]=="1")
			except Exception:N(bP,"");return
			if al.ok and 50<=b<=200:
				try:cb(b,d);p["scale_pct"],p["scale_items"]=b,d
				except Exception:return
			N(bP,"")
		def gh(w,h):
			a=(int(w),int(h))if(w is not None and h is not None and aG())else None
			if a is None:
				if aE["area"]is not None:aE["area"]=None;bH(None,None,None);p["dirty_frame"]=True
				return
			if a!=aE["area"]:aE["area"]=a;bH(a[0],a[1],"w");p["dirty_frame"]=True
		def gi(width,height):
			if not(bI()and aG()):return
			c=0 if bK()else cO(max(60,min(int(height),1000)));b=int(width)-c
			if b<40:return
			d=sum(f for g,f,h in dU(dT()));k=(p["scale_pct"]if aP["pct"]is not None else(int(round(r.scale*100))if al.ok else p["scale_pct"]))/100.;a=max(80,int(math.ceil(d*k*k/b)))
			if int(height)<(1<<19):a=min(a,max(1,int(height)))
			return None,a
		def bK():return p["side_hidden"]and not p["minimized"]and aG()
		def bu():return 0 if(bt()or aG())else a5
		def gj():
			b=p["attach"]
			if b is None:return
			a=b.get("raw")
			if a is None or a.IsDisposed:
				a=bm(b.get("g"))if al.ok else None;b["raw"]=a
				if a is not None:ag(ap["grid"],b.get("g"))
			return a
		def gk(info):
			if info is None and p["attach"]is not None:
				safe(lambda:cY(None))
				if aE["area"]is not None:aE["area"]=None;bH(None,None,None)
				p["frame_x"],p["frame_y"]=p["saved_fx"],p["saved_fy"];p["detached_at"]=time.time();r.bar_at=None
				for a in(p["bar_raw"],p["grid_raw"]):
					with Kit.quiet:
						if a is not None and not a.IsDisposed:bs(a,p["frame_x"],p["frame_y"])
				for c in("bar","grid"):
					g=ap.get(c)
					if z(g):g.SetPos(p["frame_x"],p["frame_y"]);aj(g)
			elif info is not None:
				p["minimized"]=p["docked"]=False;bV(False)
				with Kit.quiet:
					b=info.get("g")
					if z(b)and(info.get("dx")or info.get("dy")):p["frame_x"]=int(b.GetX())+int(info.get("dx",0));p["frame_y"]=int(b.GetY())+int(info.get("dy",0))
			p["attach"]=info;p["dirty_frame"]=True
		def bv():w,h=V(dj[0]);return(w or 15),(h or 15)
		def bL(grid,x,y,strip=True):
			if strip:ew(grid,x-4,y+max(0,(bv()[1]-bN)//2))
			if aG():a,b=Kit.ART_DOCK,("Show the side panel"if p["side_hidden"]else "Hide the side panel")
			else:a,b=dj,("Show the title bar and side panel"if p["bare"]else "Bags only: hide the title bar and side panel")
			m(grid,ap["store"],"bare",a,x,y,None,b,on_click=av("toggle_bare"))
		def gl(grid,slot_raws,cols,cw,ch,gap,d,c,trim):
			z=max(4,(cw-8)//7);b=aE["area"]if aG()else None
			if b is not None:U(R(grid,ax,0,0,b[0],b[1],Kit.SECTION_ALPHA))
			for f in range(p["slots"]):
				r,j=divmod(f,cols);x,y=j*(cw+gap),r*(ch+gap);A=a7(x,y,cw,ch,"#000000",.01)
				if bt():O(A,"CanMove",True)
				grid.Add(A);R(grid,ax,x,y,cw,ch,p["opacity"])
				if trim:
					if j<cols-1:grid.Add(U(a7(x+cw-1,y,1,ch,bD,.8)))
					if f+cols<p["slots"]:grid.Add(U(a7(x,y+ch-1,cw,1,bD,.8)))
				else:
					for s,t,u,v in((x,y,cw,1),(x,y+ch-1,cw,1),(x,y,1,ch),(x+cw-1,y,1,ch)):grid.Add(U(a7(s,t,u,v,ds,.9)))
				k=[bg(grid,"#%d"%(f+1),x+5,y+3,E)]
				if f in p["assign"]:k.append(bg(grid,bk(a6(p["assign"][f],False),z),x+5,y+21,l));k.append(bg(grid,"Closed",x+5,y+39,l))
				else:k.append(bg(grid,bk("Empty: click Slots",z),x+5,y+21,l))
				slot_raws.append(tuple(bm(G)for G in k)if al.ok else());B=bg(grid,"",x+5,y+max(0,ch-18),L);O(B,"IsVisible",False);ap["counts"].append((B,x,y,cw,ch))
			if b is not None:
				for f in range(p["slots"],cols*int(math.ceil(p["slots"]/float(cols)))):r,j=divmod(f,cols);U(R(grid,ax,j*(cw+gap),r*(ch+gap),cw,ch,p["opacity"]))
			if trim:
				for s,t,u,v in((0,0,d,1),(0,c-1,d,1),(0,0,1,c),(d-1,0,1,c)):grid.Add(U(a7(s,t,u,v,ds,.9)))
			if bt():g,h=V(ar);g,h=(g or 30),(h or 30);m,n=bv();o,w=d-g+dk,c-h+dk;U(ae(grid,ar,o,w));S(grid,o,w,g,h,lambda*a:None,"Drag to move the bags",movable=True);bL(grid,o-m-3,c+b5);e=o+g;i=max(w+h,c+b5+n);grid.SetRect(p["frame_x"],p["frame_y"],e,i);p["grid_wh"]=(e,i);return e
			if bK():
				m,n=bv()
				if b is not None:bL(grid,b[0]-m-2,b[1]-n-2);grid.SetRect(p["frame_x"],p["frame_y"],b[0],b[1]);p["grid_wh"]=b;return b[0]
				bL(grid,d-m,c+b5);i=c+b5+n;grid.SetRect(p["frame_x"],p["frame_y"],d,i);p["grid_wh"]=(d,i);return d
			C,q=cN(grid,d+gap,c);p["side_pw"]=gap+C;e=d+gap+C
			if b is not None:e,q=max(e,b[0]),max(q,b[1])
			grid.SetRect(p["frame_x"],p["frame_y"]+bu(),e,max(c,q));p["grid_wh"]=(e,max(c,q));return e
		bU={"outline":None,"told":False}
		def cZ(g):
			try:
				if g is None or g.IsDisposed:return
				x,y=int(g.GetX()),int(g.GetY());w,h=int(g.GetWidth()or 0),int(g.GetHeight()or 0)
			except Exception:return
			return None if w<=1 or h<=1 else(x,y,w,h)
		def gm():
			if p["minimized"]or p["docked"]:return
			a=[]
			if not bt()and not aG()and p["canvas"]!="alone":
				r=cZ(ap["bar"])
				if r is not None:a.append(r)
			r=cZ(ap["grid"])
			if r is not None:a.append(r)
			if not a:return
			b=min(f[0]for f in a);c=min(g[1]for g in a);d=max(h[0]+h[2]for h in a);e=max(i[1]+i[3]for i in a);return b,c,d-b,e-c
		def gn():
			b=[];c,d=ap["bar"],ap["grid"]
			for g,a in list(SNAP.links.items()):
				if(a is c or a is d)and a is not None and z(g):
					r=cZ(g)
					if r is not None:b.append((g,r))
			return b
		def ec(a,d,b,c,e,f):return f+(a-c)if a>=c-2 or(d>b+2 and abs(d-c)<abs(a-b))else e+(a-b)
		def ed(followers):
			c=SNAP;d=ap["grid"]if(bt()or aG()or p["canvas"]=="alone")else ap["bar"]
			if d is None:d=ap["grid"]
			aa();b=gm();a=bU["outline"]
			if a is not None:a=(p["frame_x"]+a[0],p["frame_y"]+a[1],a[2],a[3])
			if b is not None:bU["outline"]=(b[0]-p["frame_x"],b[1]-p["frame_y"],b[2],b[3])
			j=0
			for g,(e,f,l,m)in followers:
				if d is None or not z(g):continue
				c.links[g]=d
				if a is None or b is None or a==b:continue
				h=ec(e,e+l,a[0],a[0]+a[2],b[0],b[0]+b[2]);i=ec(f,f+m,a[1],a[1]+a[3],b[1],b[1]+b[3])
				if(h,i)==(e,f):continue
				try:g.SetPos(int(h),int(i))
				except Exception:continue
				j+=1
				with Kit.quiet:
					if c.last is not None:c.last[g]=(h,i)
					aj(g);c.follow(g,h-e,i-f,set([g]))
				k=c.moved_cb.get(g)
				if k is not None:safe(k)
			if j and not bU["told"]:bU["told"]=True;API.SysMsg(an+": %s moved with the bags' edge."%F(j,"snapped window"),aK)
		def go(cols,rows,ch,gap):
			a=aM()[1]
			if a<=0 or p["slots"]<=1:return cols,rows
			b=max(1,(a-bu()-eW+gap)//(ch+gap))
			if rows<=b:return cols,rows
			c=int(math.ceil(p["slots"]/float(b)));return c,int(math.ceil(p["slots"]/float(c)))
		def gp():
			m=gn();d5();bE("grid");bE("bar")
			if p["canvas"]is not None and dP()==p["canvas"]:gq(m);return
			if aE["area"]is not None and aG()and p["geom"]is not None:bH(aE["area"][0],aE["area"][1],"w");p["dirty_frame"]=False
			elif aE["told"]is not None and not aG()and p["geom"]is not None:bH(aE["told"][0],aE["told"][1],"w");p["dirty_frame"]=False
			c,e=dO();n=cc();d=0 if n else cr;h,f=aE["cell"]or(p["cell_w"],p["cell_h"]);i=not aG()and p["canvas"]is None and aE["told"]is None and not ao(aH)
			if i and not p["minimized"]:c,e=go(c,e,f,d)
			s=c*h+(c-1)*d;o=e*f+(e-1)*d;p["geom"]=(c,h,f,d);p["icons_used"]=r.icons or bB;ap.update({"store":({},{}),"side_status":None,"search_box":None,"counts":[],"count_state":{}});b=bt();a=G.CreateGump(b,b);ap["grid_bare"]=b;p["grid_info"]=(bm(a)if al.ok else None,b);q=[]
			if p["minimized"]:g=cu;a.SetRect(p["frame_x"],p["frame_y"]+a5,1,1)
			else:g=gl(a,q,c,h,f,d,s,o,n)
			if i:
				t=g if b else max(g,cu);u=a5 if p["minimized"]else bu()+(p["grid_wh"][1]if p["grid_wh"]else o);j,k=Kit.clamp(p["frame_x"],p["frame_y"],t,u)
				if(j,k)!=(p["frame_x"],p["frame_y"]):p["frame_x"],p["frame_y"]=j,k;a.SetPos(j,k+(a5 if p["minimized"]else bu()))
			dz(a,True);dA(a);G.AddGump(a);ap["grid"]=a;l=eh(g,p["docked"]or b or aG(),i)
			if aG():p["attach_g"]=p["attach"].get("g");ag(a,p["attach_g"])
			elif b:ag(l,a)
			else:ag(a,l)
			ed(m);p["slot_raws"]=tuple(q)
			if SR["counts"]:cm()
			p["grid_raw"]=bm(a)if al.ok else None;p["bar_raw"]=bm(l)if al.ok else None
			if al.ok and not r.disabled and(p["grid_raw"]is None or p["bar_raw"]is None):r.error="can't reach the client's own window controls";r.disabled=True
		ee="Close "+an+" (turns it off; gives every bag back)";ef="Open the bag manager: a bag per slot";eg="Pick the bags Trap and Untrap cast on"
		def eh(f,hide,free=False):
			b=max(f,cu);a=G.CreateGump(True,True)
			if free:at(a,p["frame_x"],p["frame_y"],b,a5)
			else:a.SetRect(p["frame_x"],p["frame_y"],b,a5)
			af(a,b,a5,corners=False);B(a,8,8,b-16,a5-16);e(a,an.upper(),18,14,E);e(a,str(p["slots"]),18+o(an.upper())+8,14,l);c=ap["store"];x=b-12-30
			if am(aH):x+=20
			else:m(a,c,"close",I,x,11,None,ee,on_click=av("disable",aH));x-=20;m(a,c,"min",a_ if p["minimized"]else aZ,x,14,None,a2 if p["minimized"]else a0,on_click=av("user_collapse"));Kit.dock_button(a,c,x,14,on_click=av("fold_to_bar"));x-=Kit.DOCK_DX
			for g,d,h,i in(("settings","Settings",Kit.SETTINGS_TIP%an,av("show_settings",aH)),("traps","Trap bags",eg,av("open_win","trp")),("bags","Slots",ef,av("open_win","mgr"))):x-=10+35+o(d);m(a,c,g,J,x,11,d,h,on_click=i)
			bf(a,8,8,max(20,x-14),a5-16,av("user_collapse"),key=aH)
			if hide:a.IsVisible=False
			G.AddGump(a);ap["bar"]=a;return a
		hL=None
		def ei():
			if p["canvas"]is None or P["ctrl"]is None or au["size"]is None:return
			if P["built"]!=au["ver"]or P["bsize"]!=au["size"]:
				if P["rect"]is not None and(P["rect"][2],P["rect"][3])!=au["size"]:return
				if bT():return
				fU()
			d6();f1()
		def gq(followers):
			i=p["canvas"];b=i=="alone";p["icons_used"]=r.icons or bB;ap.update({"store":({},{}),"side_status":None,"search_box":None});e,f,c,g,o=dR(i);W,d=aE["told"]if b else aE["area"];a=G.CreateGump(b,b);ap["grid_bare"]=b;h=bm(a);p["grid_info"]=(h,b);j=ap["store"];k=b and not p["bare"]and cP(W)
			if b:
				af(a,W,d)
				if k:
					be(a,j,W,an,aH,av("user_collapse"),av("fold_to_bar"),av("show_settings",aH),close_tip=ee,extra=[("traps",J,"Trap bags",eg,av("open_win","trp")),("bags",J,"Slots",ef,av("open_win","mgr"))],after=str(p["slots"]));l=j[0].get("close")
					if l is not None:aB(l,av("disable",aH))
			aa();fT(h,h.Children.Count,e,f,c,g);m,n=bv()
			if b:
				p["side_pw"]=0
				if p["bare"]and cP(W):bL(a,e+c-m-2,f+g-n-2)
				elif k and o:p["side_pw"]=cN(a,e+c,g,f)[0]
				else:ew(a,e+c-2,f+g-bN-2)
			elif bK():bL(a,W-m-2,d-n-2);p["side_pw"]=0
			else:p["side_pw"]=cN(a,c,d)[0]
			a.SetRect(p["frame_x"],p["frame_y"],W,d);p["grid_wh"]=(W,d);dz(a,False)
			if not b:dA(a)
			if ao(aH):a.CanMove=False
			G.AddGump(a);ap["grid"]=a;q=eh(W,True)
			if aG():p["attach_g"]=p["attach"].get("g");ag(a,p["attach_g"])
			ed(followers);p["slot_raws"]=();p["grid_raw"]=h;p["bar_raw"]=bm(q)if al.ok else None
			if p["grid_raw"]is None:r.error="can't reach the client's own window controls";r.disabled=True;return
			ei()
		def gs():p["minimized"]=not p["minimized"];p["docked"]=False;bj()
		def c_():return aV(du)
		def bV(on):HOST.dock_want_set(du,on)
		def gt():
			if am(aH):return
			bV(False);gs()
		def ej():
			if am(aH):return
			bV(True);a=aF()
			if not p["minimized"]or p["docked"]!=a:p["minimized"],p["docked"]=True,a;bj()
			if not a:HOST.dock_note(an)
		def gu():
			if aG():p["side_hidden"]=not p["side_hidden"]
			else:p["bare"]=not p["bare"]
			bj()
		bw={"next":0.}
		def ek():
			a=time.time()
			if a<bw["next"]:return
			bw["next"]=a+.1;b=API.GetSharedVar(cA)
			if b:
				API.RemoveSharedVar(cA);b=str(b)
				if aG():
					d=p["attach"].get("cmd")
					if d is not None:safe(lambda:d(b))
				elif b=="show"and(p["minimized"]or p["docked"]):bV(False);p["minimized"]=p["docked"]=False;bj()
				elif b=="dock"and not p["docked"]:ej()
			if aG():c=str(p["attach"].get("state")or "open")
			else:
				if p["docked"]:
					if not aF():p["docked"]=False;p["dirty_frame"]=True
				elif p["minimized"]and a>=bw.get("wish",0.):
					bw["wish"]=a+.25
					if c_()and aF():p["docked"]=True;p["dirty_frame"]=True
				elif not p["minimized"]and a>=bw.get("wish",0.):
					bw["wish"]=a+1.
					if c_():bV(False)
				c="docked"if p["docked"]else("collapsed"if p["minimized"]else "open")
			if c!=p["link_state"]:p["link_state"]=c;API.SetSharedVar(dt,c)
		def gv(value):
			if not al.ok:API.SysMsg(an+": minimizing bags needs client access (%s)."%al.error,aC);return
			n=fA(value)or 0;API.SysMsg(an+": %s %s."%("minimized"if value else "restored",F(n,"bag")),aK)
		def gw():
			gx();a=False;b=p["minimized"]or(aG()and not p["attach"].get("shown",True))
			for f,i in p["layout"]:
				try:
					c=API.FindItem(i);g=c.GetContainerGump()if c else None
					if not z(g):continue
					try:g.IsVisible=not b
					except Exception:pass
					if b:continue
					d,e=dD(f)
					if g.GetX()!=d or g.GetY()!=e:g.SetPos(d,e)
					w=g.GetWidth()or 0;h=g.GetHeight()or 0
				except Exception:continue
				if p["cell_w"]<w<=bc:p["cell_w"],a=w,True
				if p["cell_h"]<h<=bc:p["cell_h"],a=h,True
			if a:bj()
		def el():
			a=p["attach"].get("g")if aG()else None
			if a is not None and a is not p["attach_g"]and z(a)and z(ap.get("grid")):p["attach_g"]=a;ag(ap["grid"],a)
		def gx():
			if aG():
				b,d=p["attach"].get("g"),p["attach"]
				if not z(b):return
				el();x=b.GetX()+d.get("dx",0);y=b.GetY()+d.get("dy",0);a=ap.get("grid")
				if(x,y)!=(p["frame_x"],p["frame_y"]):
					p["frame_x"],p["frame_y"]=x,y
					if z(a):a.SetPos(x,y);aj(a)
				elif z(a)and(int(a.GetX()),int(a.GetY()))!=(x,y):a.SetPos(x,y);aj(a)
				return
			b,c,e=(ap["grid"],ap["bar"],0)if ap.get("grid_bare")else(ap["bar"],ap["grid"],a5)
			if not z(b):return
			x=b.GetX();y=b.GetY()
			if x!=p["frame_x"]or y!=p["frame_y"]:
				p["frame_x"],p["frame_y"]=x,y
				if z(c):c.SetPos(x,y+e);aj(c)
		def c0(k):p["open_"+k]=True;p["dirty_"+k]=True;bh()
		cj={"trp":"trap_checks","srt":"rule_checks"}
		def em(k):
			if k=="trp":bx()
			elif k=="srt":bo()
		def gy(k):
			em(k);cp(k)
			if k in cj:ap[cj[k]]=[]
			p["open_"+k]=False;bh()
		def gz(k):em(k);p[k+"_min"]=not p[k+"_min"];p["dirty_"+k]=True;bh()
		def c1():cq();bh()
		def gA():
			cp("mgr");a,i=K,v;w,n,j=480,28,40;k=min(p["slots"]*n+8,430);q=a+30+a if p["mgr_min"]else a+30+i+j+i+k+a;g,f,y=b7("mgr",w,q,"BAG MANAGER",av("toggle_win_min","mgr"),av("close_win","mgr"))
			if not p["mgr_min"]:
				h=w-2*a;B(g,a,y,h,j);m(g,f,"fill",ad,a+12,y+9,"Auto-fill","Put each open bag without a slot in an empty slot",on_click=av("auto_fill"));m(g,f,"clear",I,a+200,y+9,"Clear all","Empty every slot",on_click=av("clear_all"));y+=j+i;B(g,a,y,h,k);c=G.CreateGumpScrollArea(a+4,y+4,h-8,k-8);o=h-8-20
				for b in range(p["slots"]):
					d=b*n;e(c,"#%d"%(b+1),6,d+5,E)
					if b in p["assign"]:e(c,bk(a6(p["assign"][b]),28),44,d+5)
					else:e(c,"No bag yet: click Set...",44,d+5,l)
					m(c,f,"set%d"%b,M,o-165,d+3,"Set...","Target a bag for slot #%d"%(b+1),on_click=av("assign_slot",b));m(c,f,"clr%d"%b,I,o-80,d+3,"Clear","Empty slot #%d"%(b+1),on_click=av("clear_slot",b))
				g.Add(c)
			b8("mgr",g,c1)
		def bW():dy();p["dirty_frame"]=True;p["dirty_mgr"]=True;p["dirty_trp"]=True;p["dirty_srt"]=True;cK();ba()
		def bX(kind,*a):
			def b(serial):dx.add((kind,)+a+(int(serial or 0),),dup=True)
			aI(15,b)
		def gB(idx):API.SysMsg(an+": target a bag for slot #%d."%(idx+1),aK);bX("assign_slot_to",idx)
		def gC(idx,target):
			if not target:API.SysMsg(an+": cancelled.",aK);return
			b=Z(target)
			if not b or not b.IsContainer:API.SysMsg(an+": that isn't a container.",aC);return
			a=int(target)
			for k in[c for c,d in p["assign"].items()if d==a]:del p["assign"][k]
			p["assign"][idx]=a;bW()
			if dI(a):API.SysMsg(an+": slot #%d set."%(idx+1),bd)
			else:API.SysMsg(an+": slot #%d set; open the bag to snap it in."%(idx+1),bd)
		def gD(idx):
			if idx in p["assign"]:del p["assign"][idx];bW()
		def gE():p["assign"]={};bW();API.SysMsg(an+": all slots cleared.",aK)
		def gF():
			b=[]
			for c in(safe(lambda:int(API.Backpack),0),safe(lambda:int(API.Bank),0)):
				if not c:continue
				b.append(c)
				for f in API.ItemsInContainer(c,True)or[]:
					if f.IsContainer:b.append(int(f.Serial))
			g=set(p["assign"].values());d=[h for h in range(p["slots"])if h not in p["assign"]];e=0
			for a in b:
				if not d:break
				if a in g or not dI(a):continue
				p["assign"][d.pop(0)]=a;g.add(a);e+=1
			bW()
			if e:API.SysMsg(an+": added %s."%F(e,"open bag"),bd)
			elif not d:API.SysMsg(an+": no empty slots left.",aC)
			else:API.SysMsg(an+": no open bag without a slot found.",aK)
		aU={"c":None,"store":({},{}),"next_status":0.}
		def en():
			if p["canvas"]is not None:return "In a zone the bags share it. Items always draw solid."
			return "Slots fit the open bags (%d x %d px). Items always draw solid."%(p["cell_w"],p["cell_h"])
		def gG(g,x,y,w):
			if al.ok and aP["pct"]is None:
				a=safe(dH)
				if a:p["scale_pct"],p["scale_items"]=a
			f=Kit.Form(g,x,y,w,{"slots":p["slots"],"cols":p["cols"],"rows":p["rows"],"scale":p["scale_pct"],"opacity":int(round(p["opacity"]*100)),"trim":p["trim"],"items":p["scale_items"]},eE(w));aU.update({"c":f.c,"store":f.store,"next_status":0.,"seen":{"trim":p["trim"],"items":p["scale_items"]}})
		def eo():aU["c"]=None
		def gH():
			c=aU["c"]
			if c is None:return
			if X(aU["store"],"apply"):gK();return
			for d,g in(("trim",gI),("items",gJ)):
				try:a=bool(c[d].IsChecked)
				except Exception:a=None
				if a is not None and a!=aU["seen"][d]:aU["seen"][d]=a;g(a)
			try:v=int(c["opacity"].Value)
			except Exception:v=None
			if v is not None and 10<=v<=100:
				if aU.get("pct_v")!=(v,c["opacity_lbl"]):aU["pct_v"]=(v,c["opacity_lbl"]);A(c["opacity_lbl"],"%d%%"%v)
				b=v/100.
				if abs(b-p["opacity"])>.001:
					e=p["opacity_pending"];p["opacity_pending"]=(b,e[1]+1)if e and e[0]==b else(b,0)
					if p["opacity_pending"][1]>=e4:p["opacity"]=b;p["opacity_pending"]=None;p["dirty_frame"]=True;d6();bh()
				else:p["opacity_pending"]=None
			f=time.time()
			if f>=aU["next_status"]:aU["next_status"]=f+1.;A(c["status"],bk(c2(),64));A(c["size"],en())
		def c2():
			if not al.tried:return "Off: tick "+an+" on the Modules tab"
			if not al.ok:return "No client access: "+al.error
			if r.disabled:return "Trimming stopped after errors: "+r.error
			if p["canvas"]is not None:a="%d open, filling the zone"%r.open_count
			else:a="%d open, %d trimmed"%(r.open_count,len(r.trimmed))
			if p["driving"]:return "Running (script-driven): "+a
			return "Starting"if r.hook_calls==0 else "Running: "+a
		def gI(value):
			f=aU["c"]
			if value and not(al.ok and not r.disabled):
				API.SysMsg(an+": trimming isn't available (%s)."%c2(),aC)
				if f:safe(lambda:f["trim"].SetIsChecked(False));aU["seen"]["trim"]=False
				value=False
			if value==p["trim"]:return
			p["trim"]=value;cL();ba();API.SysMsg(an+": trim "+("on."if value else "off."),aK)
		def gJ(value):
			if value==p["scale_items"]:return
			if not al.ok:API.SysMsg(an+": scaling items needs client access (%s)."%al.error,aC);return
			try:
				a=p["scale_items"];p["scale_items"]=value
				try:cb(*cW())
				except Exception:p["scale_items"]=a;raise
				if aP["pct"]is not None:cX()
				cL();API.SysMsg(an+": items %s with the bags."%("scale"if value else "don't scale"),aK)
			except Exception as e:API.SysMsg(an+": couldn't change the item scaling (%s)."%e,aC)
		def ck(field,name,lo,hi):
			a=(safe(lambda:field.Text,"")or "").strip()
			if not a.isdigit()or not(lo<=int(a)<=hi):raise ValueError("%s must be a whole number from %d to %d."%(name,lo,hi))
			return int(a)
		def gK():
			f=aU["c"]
			if not f:return
			try:a=ck(f["slots"],"Slots",b1,a1);b=ck(f["cols"],"Columns",0,a1);c=ck(f["rows"],"Rows",0,a1);d=ck(f["scale"],"Bag scale",50,200)
			except ValueError as e:API.SysMsg(an+": "+str(e),aC);return
			if b>0 and c>0 and b*c<a:API.SysMsg(an+": %d columns x %d rows only fits %d slots, not %d."%(b,c,b*c,a),aC);return
			g=[n for n in p["assign"]if n>=a]
			for k in g:del p["assign"][k]
			bo()
			for k in[q for q in p["rules"]if q>=a]:del p["rules"][k]
			p["slots"],p["cols"],p["rows"]=a,b,c
			if al.ok and d!=p["scale_pct"]:
				try:
					i=p["scale_pct"];p["scale_pct"]=d
					try:cb(*cW())
					except Exception:p["scale_pct"]=i;raise
					if aP["pct"]is not None:
						if aP["pct"]>=d:aP["pct"]=None
						cX()
					cL()
				except Exception as e:API.SysMsg(an+": couldn't change the bag scale (%s)."%e,aC)
			bW();j,r=dO();h=an+": %s in %d x %d."%(F(a,"slot"),j,r)
			if g:h+=" Released %s from removed slots."%F(len(g),"bag")
			API.SysMsg(h,bd);eo();Y(aH)
		def c3():
			a=[]
			for s in[p["assign"][b]for b in sorted(p["assign"])]+p["trap_extra"]:
				if s not in a:a.append(s)
			return a
		def bx():
			a=ap["trap_checks"]
			if not a or not z(ap["trp"]):return
			for b,c in a:
				if safe(lambda:c.IsChecked,False):p["trap_sel"].add(b)
				else:p["trap_sel"].discard(b)
		def gL():
			bx();cp("trp");i=c3();a,c=K,v;w,k,j,n=480,28,40,52;f=min(max(1,len(i))*k+8,400);t=(a+30+a if p["trp_min"]else a+30+c+j+c+f+c+n+a);g,o,y=b7("trp",w,t,"TRAP BAGS",av("toggle_win_min","trp"),av("close_win","trp"));q=[]
			if not p["trp_min"]:
				d=w-2*a;B(g,a,y,d,j);Kit.buttons(g,o,a+12,y+9,(("all",ad,"Tick all","Tick every bag",av("select_all_traps",True)),("none",I,"Untick all","Untick every bag",av("select_all_traps",False)),("add",M,"Add bag...","Target a bag without a slot to add it",av("add_trap_bag"))),16);y+=j+c;B(g,a,y,d,f);h=G.CreateGumpScrollArea(a+4,y+4,d-8,f-8);x=d-8-20
				if not i:e(h,"No bags yet. Fill the slots, or click Add bag...",6,6,l)
				for r,b in enumerate(i):
					s=r*k;z=ay(h,bk(a6(b),32),6,s+4,b in p["trap_sel"],"Ticked: Trap and Untrap cast on this bag");q.append((b,z))
					if b in p["trap_extra"]and b not in p["assign"].values():m(h,o,"rm%d"%r,I,x-110,s+3,"Remove","Take this bag off",on_click=av("remove_trap_bag",b))
				g.Add(h);y+=f+c;B(g,a,y,d,n);e(g,"Tick bags, then Trap or Untrap on the side panel.",a+12,y+8,l);e(g,"A trapped bag explodes on whoever opens it, you included.",a+12,y+28,u)
			b8("trp",g,c1,trap_checks=q)
		def c4():ap["trap_checks"]=[];p["dirty_trp"]=True;ba()
		def gM(value):p["trap_sel"]=set(c3())if value else set();c4()
		def gN():bx();API.SysMsg(an+": target a bag to add to the trap list.",aK);bX("add_trap_bag_to")
		def gO(target):
			if not target:return
			bx();b=Z(target)
			if not b or not b.IsContainer:API.SysMsg(an+": that isn't a container.",aC);return
			a=int(target)
			if a not in p["trap_extra"]:p["trap_extra"].append(a)
			p["trap_sel"].add(a);c4()
		def gP(serial):
			bx()
			if serial in p["trap_extra"]:p["trap_extra"].remove(serial)
			p["trap_sel"].discard(serial);c4()
		def gQ(spell):
			bx();ba()
			if p["job"]:API.SysMsg(an+": already casting %s; press Stop first."%p["job"]["spell"],aC);return
			if p["sort"]:API.SysMsg(an+": busy sorting; press Stop first.",aC);return
			a=[b for b in c3()if b in p["trap_sel"]]
			if not a:API.SysMsg(an+": tick bags in the Trap bags window first.",aC);c0("trp");return
			p["job"]={"spell":spell,"queue":a,"i":0,"phase":"mana","t":0.,"tries":0,"done":0,"failed":0,"warned":False,"cast":0.};p["dirty_trp"]=True;aQ("Starting");API.SysMsg(an+": casting %s on %s."%(spell,F(len(a),"bag")),aK)
		def bY(user=False):
			if p["job"]:
				a=p["job"]
				if a.get("phase")=="target"and time.time()-a.get("cast",0.)>=do and aS(aH,"neutral"):API.CancelTarget()
				aw(aH)
				if user:API.SysMsg(an+": %s stopped."%p["job"]["spell"],aK);aQ("Stopped")
			p["job"]=None;p["dirty_trp"]=True
		def ep():
			b=bool(p["job"]or p["sort"])
			for a in ap.get("stop_ctrls")or():
				if a is not None:O(a,"IsVisible",b)
		def aQ(text):
			if text=="Idle":a=aP["pct"];text=("Shown at %d%% to fit"%a)if a is not None and a<p["scale_pct"]else ""
			ep()
			if text==p["status_text"]:return
			p["status_text"]=text;b=ap.get("side_status")
			if b is not None:A(b,text)
		gR=tuple((hN,tuple(hP.lower()for hP in hO))for hN,hO in(("reagents",fc),("mana",fd),("fizzle",fa),("busy",fb)))
		def eq(j):
			c=j.get("jr")
			if c is None:return
			a=j["jt"]
			for b in c.new():
				if b.text and not b.text.startswith(an):a.append(b.low)
			if not a:return
			for d,e in gR:
				if any(f in g for f in e for g in a):return d
			return
		def c5(j,a):
			if a:j["done"]+=1
			else:j["failed"]+=1
			j["i"]+=1;j["tries"]=0;j["phase"]="mana"
		def c6(j,now,a):
			j["tries"]+=1
			if j["tries"]>e9:API.SysMsg(an+": giving up on %s (%s)."%(a6(j["queue"][j["i"]],False),a),aC);c5(j,False)
			else:j["phase"]="pause";j["t"]=now+e8
		def gS():
			j=p["job"]
			if not j:return
			a=time.time()
			if j["i"]>=len(j["queue"]):API.SysMsg(an+": %s finished: %d done, %d failed."%(j["spell"],j["done"],j["failed"]),bd if not j["failed"]else aC);aQ("Done %d/%d"%(j["done"],len(j["queue"])));bY();return
			d=j["queue"][j["i"]];e=j["phase"]
			if e=="pause":
				if a>=j["t"]:j["phase"]="mana"
				return
			if e=="mana":
				c=HOST.fight_hold(a)or HOST.guard_hold()
				if c:
					if j.get("held")!=c:j["held"]=c;f=HOLD_TEXT.get(c,c);API.SysMsg(an+": %s waits (%s)."%(j["spell"],f[:1].lower()+f[1:]),aK);aQ(f if c=="unknown"else "Paused: "+f)
					return
				if j.get("held"):j["held"]=None;aQ("Starting")
				g=API.Player.Mana
				if g<dm:
					if not j["warned"]:API.SysMsg(an+": waiting for mana (%d/%d)."%(g,dm),aK);aQ("Need mana");j["warned"]=True
					return
				j["warned"]=False
				if not Z(d):API.SysMsg(an+": bag 0x%08X is out of reach; skipping it."%d,aC);c5(j,False);return
				if cI():aQ("Cursor busy");return
				if API.HasTarget("any"):aQ("Cursor busy");return
				API.SysMsg(an+": %s %d/%d: %s."%(j["spell"],j["i"]+1,len(j["queue"]),a6(d,False)),aK);aQ("%s %d/%d"%("Untrap"if "Untrap"in j["spell"]else "Trap",j["i"]+1,len(j["queue"])));j["cast"]=time.time();j["jr"],j["jt"]=aY(),[];HOST.claim_cursor(aH,dn+.5);API.CastSpell(j["spell"]);j["phase"]="target";j["t"]=a;return
			if e=="target":
				b=eq(j)
				if b:aw(aH)
				if b=="reagents":API.SysMsg(an+": out of reagents for %s."%j["spell"],aC);bY();return
				if b=="mana":j["phase"]="mana";return
				if b in("fizzle","busy"):c6(j,a,b);return
				if a-j["cast"]>=do and aS(aH,"neutral"):API.Target(d);aw(aH);j["phase"]="recover";j["t"]=a
				elif a-j["t"]>dn:aw(aH);c6(j,a,"no target cursor")
				return
			if e=="recover":
				if a-j["t"]<e7:return
				b=eq(j)
				if b=="reagents":API.SysMsg(an+": out of reagents for %s."%j["spell"],aC);bY()
				elif b in("fizzle","busy","mana"):c6(j,a,b)
				else:c5(j,True)
		def c7(it,hue):
			try:it.SetHue(int(hue)&65535);return True
			except Exception:return False
		def c8(it):
			try:return int(it.Hue or 0)
			except Exception:return-1
		SR={"text":"","typed":0.,"armed":False,"lit":{},"until":0.,"counts":{},"restored":{},"tiles":{},"status":None,"texts":{},"texts_at":0.,"objs":{}}
		def gT(q):
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
		def gU(raw):
			if "%"not in raw:return raw
			a,b=[],[]
			for i,p in enumerate(raw.split("%")):
				if i%2==0:a.append(p);b.append(p)
				else:c,e,d=p.partition("/");a.append(d);b.append(c)
			return "".join(a)+" "+"".join(b)
		def c9(it,graphic):
			a=SR["tiles"];t=a.get(graphic)
			if t is None:
				d=it.GetItemData();b=str(d.Name or "")if d is not None else "";t=gU(b).lower()
				if len(a)>=fh:a.clear()
				a[graphic]=t
			return t
		def gV(it,serial,graphic):
			a=SR["texts"];t=a.get(serial)
			if t is not None:return t+"\n"+c9(it,graphic)
			t=API.ItemNameAndProps(serial)or ""
			if t:
				t=str(t).lower()
				if "\n"in t and len(a)<cy:a[serial]=t
				return t+"\n"+c9(it,graphic)
			return str(it.Name or "").lower()+"\n"+c9(it,graphic)
		def gW(x):
			m=set(G for W,G in p["layout"]);d,o={},{};q={};g=0
			for h,e in p["layout"]:
				if g>=cy:break
				r=API.ItemsInContainer(e,True)or[];i={};f=[]
				for b in r:
					try:s=int(b.Serial)
					except Exception:f.append(None);continue
					f.append(s)
					try:i[s]=int(b.Container)
					except Exception:pass
				n=0
				for t in range(len(f)):
					if g>=cy:break
					g+=1;a=f[t]
					if a is None or a in m:continue
					j,c,u=a,i.get(a,e),0
					while c!=e and u<fg and c not in m:j,c=c,i.get(c,e);u+=1
					if c!=e:continue
					b=r[t]
					try:v=int(b.Graphic)
					except Exception:continue
					k=None;l=False
					for y,w in x:
						if w is not None:
							if v==w:l=True;break
						else:
							if k is None:k=gV(b,a,v)
							if y in k:l=True;break
					if not l:continue
					n+=1
					if len(d)<cz:
						d[a]=h;q[a]=b
						if j!=a and len(d)<cz:d[j]=h
				if n:o[h]=n
			SR["objs"]=q;return d,o
		def er(serial):a=SR["objs"].get(serial);return a if a is not None else API.FindItem(serial)
		def gX(serial,now):
			a=er(serial)
			if not a:return False
			b=c8(a)
			if b<0:return False
			d=b
			if b==bp:
				c=SR["restored"].get(serial)
				if c is not None and now-c[1]<dp:d=c[0]
			if not c7(a,bp):return False
			cT(serial,bp);SR["lit"][serial]=d;return True
		def es(serial,orig,now):
			a=API.FindItem(serial)
			if not a:return
			b=c8(a)
			if b==bp or b==orig:
				if c7(a,orig):cT(serial,orig)
				SR["restored"][serial]=(orig,now)
		def gY(now):
			a=SR["restored"]
			if a:
				for s in[b for b,c in a.items()if now-c[1]>=dp]:del a[s]
				if len(a)>2*cz:a.clear()
		def gZ(q,now):
			c=gT(q)
			if not c:cl(now);return
			gY(now)
			if not 0<=now-SR["texts_at"]<=cx:SR["texts"]={};SR["texts_at"]=now
			d,e=gW(c);b=SR["lit"]
			for a in[h for h in b if h not in d]:es(a,b.pop(a),now)
			try:
				for a in d:
					if a not in b:gX(a,now)
					else:g_(a)
			finally:SR["objs"]={}
			SR["counts"]=e;SR["until"]=now+cx;cm();f=sum(e.values());g=("%d found"%f)if f else "None found";SR["status"]=g;aQ(g)
		def g_(serial):
			a=er(serial)
			if not a:return
			b=c8(a)
			if 0<=b!=bp and c7(a,bp):cT(serial,bp);SR["lit"][serial]=b
		def cl(now):
			a=SR["lit"]
			for b in list(a):es(b,a.pop(b),now)
			SR["texts"]={};SR["texts_at"]=0.;SR["until"]=0.
			if SR["counts"]:SR["counts"]={};cm()
			if SR["status"]is not None:
				if p["status_text"]==SR["status"]:aQ("Idle")
				SR["status"]=None
		def cm():
			e=SR["counts"];d=ap["count_state"]
			for b,(c,x,y,f,g)in enumerate(ap["counts"]):
				n=e.get(b,0);a=("%d found"%n)if n else ""
				if d.get(b)==a:continue
				d[b]=a
				try:
					if n:c.SetPos(x+max(5,f-5-o(a)),y+max(0,g-18));A(c,a)
					c.IsVisible=bool(n)
				except Exception:pass
		def g0(now):
			b=ap["search_box"]
			if b is not None and not(p["minimized"]or p["docked"]):
				try:a=b.Text
				except Exception:a=None
				if a is not None:
					a=str(a)
					if a!=SR["text"]:SR["text"],SR["typed"],SR["armed"]=a,now,True
			if SR["armed"]:
				if now-SR["typed"]>=fe:
					SR["armed"]=False;q=SR["text"].strip()
					if len(q)>=ff:gZ(q,now)
					elif SR["lit"]or SR["counts"]:cl(now)
			elif SR["until"]and now>=SR["until"]:cl(now)
		def g1(grid,a,y):b=o("Find:")+6;bg(grid,"Find:",a+2,y+3,D);c=az(grid,SR["text"],a+2+b,y,b2-4-b,numbers=False);c.SetTooltip("Item name part or graphic (0x0F7A, 3962); commas for several. Matches light up for %d s"%int(cx));ap["search_box"]=c;m(grid,ap["store"],"rules",J,a,y+28,"Rules","Open Sort rules: what each slot's bag holds",on_click=av("open_win","srt"));m(grid,ap["store"],"filters",J,a,y+52,"Filters","Open Sort filters: items or presets and their bags",on_click=av("open_filters"))
		et="Sort items into their bags once; picking up or Stop ends it";bZ=(("q_restock","Restock",M,3702,"restock","Top up supplies once from the Restock chest or bank","restock.run"),("q_sort","Sort",M,3705,None,et,None),("q_storage","Storage",J,3648,"storage","Open or raise the Storage window","storage.show"),("q_supplies","Supplies",J,3962,"supplies","Open or raise the Supplies table","supplies.open"))
		def bM(part):return part is None or HOST.part_on(part,"inventory")
		def eu(part,tip):
			if bM(part):return tip
			return("%s is off: tick Inventory > %s on the Modules tab"%(part.title(),part.title()))
		def g2(key):
			for k,a,e,f,b,g,d in bZ:
				if k!=key:continue
				if b is None:ey();return
				c=HOST.services.get(d)if bM(b)else None
				if c is None:API.SysMsg("%s: %s is off; tick Inventory > %s on the Modules tab."%(an,a,a),aK);return
				c();return
		def da():return tuple(bM(a[4])for a in bZ)
		def g3(grid,b,y):
			ap["quick_sig"]=da()
			for i,(k,c,d,f,a,e,g)in enumerate(bZ):m(grid,ap["store"],k,d,b,y+i*24,c,eu(a,e),hue=None if bM(a)else l,on_click=av("quick_press",k))
		bN=18;ev=22
		def ew(grid,c,y):
			ap["quick_sig"]=da();x=c-len(bZ)*ev
			for i,(k,d,g,e,b,f,h)in enumerate(bZ):
				with Kit.quiet:
					a=G.CreateGumpItemPic(e,bN,bN);a.SetRect(x+i*ev,y,bN,bN)
					if not bM(b):O(a,"Hue",l)
					O(a,"DrawBorder",False);t=eu(b,f);a.SetTooltip(t if not bM(b)else d+": "+t);G.AddControlOnClick(a,av("quick_press",k));grid.Add(a)
		g4=dict((hQ,frozenset(hR))for hQ,hS,hR in aD);b_=(frozenset(),())
		def g5(idx):
			b,c=p["rules"].get(idx,b_);a=set(c)
			for k in b:a|=g4.get(k,frozenset())
			return a
		def g6(serial):
			s=int(serial or 0)
			for b in range(12):
				a=API.FindItem(s)
				if a is None:return False
				if int(a.Graphic or 0)==8198 or a.IsCorpse:return True
				c=int(a.Container or 0)
				if not c or c==0xFFFFFFFF or c<0x40000000:return False
				s=c
			return False
		def ex():
			h=[w for w in p["filters"]if w["on"]and w["slot"]is not None and w["set"]];b={}
			for a,c in p["layout"]:
				m=g5(a)
				if m:b[a]=m
			if not b and not h:return
			i={}
			for a in sorted(b):
				for n in b[a]:
					if n not in i:i[n]=a
			o=dict((y,x)for x,y in p["layout"]);d=[];q=safe(lambda:int(API.Backpack),0)
			if q:d.append(q)
			for u,c in p["layout"]:
				if c not in d and not g6(c):d.append(c)
			j=[]
			for e in d:
				s=b.get(o.get(e),())
				for f in API.ItemsInContainer(e,False)or[]:
					if len(j)>=fi:break
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
		def ey():
			bo()
			if p["sort"]:API.SysMsg(an+": already sorting; press Stop first.",aC);return
			if p["job"]:API.SysMsg(an+": busy with %s; press Stop first."%p["job"]["spell"],aC);return
			a=ex()
			if a is None:API.SysMsg(an+": no sort rules yet; tick what each bag holds in Sort rules.",aC);c0("srt");return
			if not a:API.SysMsg(an+": nothing to sort; every ruled item is in its bag.",aK);aQ("Nothing to sort");return
			p["sort"]={"plan":a,"i":0,"move":None,"check":None,"at":0.,"hold":0.,"moved":0,"refused":0,"streak":0,"rechecks":0,"waits":0,"why":None,"last":0,"sent_at":0.};aQ("Sort 0/%d"%len(a));API.SysMsg(an+": sorting %s."%F(len(a),"item"),aK)
		def g7(s,now):
			e,f,b,g=s["check"];c=s["sent_at"]
			if aq(c,fk)is not None:bb("bag #%d (%s) is full"%(g+1,a6(b,False)));return False
			d=API.FindItem(e);a=int(d.Container)if d else None
			if a is None and s["rechecks"]<dr and not g8(s,b):s["rechecks"]+=1;s["at"]=now+bC*.5;return False
			if a is None or a==b:s["moved"]+=1;s["streak"]=s["rechecks"]=s["waits"]=0;s["check"]=None;return True
			if(a==f and aq(c,fl)is not None and s["waits"]<dq):s["waits"]+=1;s["i"]-=1;s["check"]=None;s["rechecks"]=0;s["hold"]=now+bC;return False
			if s["rechecks"]<dr:s["rechecks"]+=1;s["at"]=now+bC*.5;return False
			s["check"]=None;s["rechecks"]=0;s["refused"]+=1;s["streak"]+=1
			if s["streak"]>=dq:bb("%d moves in a row were refused"%s["streak"]);return False
			return True
		def ez(bag,graphic,deep=None):
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
		def g8(s,bag):a=s.get("pre");return True if not a or not a[0]else ez(bag,a[0])>=a[2]+a[1]
		def g9(now):
			s=p["sort"]
			if s is None:return
			if s["move"]is not None:return
			if s["why"]:bb(s["why"]);return
			if s["check"]is not None:
				if now<s["at"]or not g7(s,now):return
			if now<s["hold"]:return
			if cI():bb("another target cursor is in use");return
			h=aA()
			if h and not(h==s["last"]and now-s["sent_at"]<2*bC):bb("you picked something up");return
			d=s["plan"]
			while s["i"]<len(d):
				e,f,a,b=d[s["i"]];s["i"]+=1;c=API.FindItem(e);j=int(c.Container)if c else 0
				if j!=f:continue
				if p["assign"].get(b)!=a:continue
				if not Z(a):bb("slot #%d's bag is out of reach"%(b+1));return
				g=API.ItemsInContainer(a,True)or[];k=len(g)
				if k>=fj:bb("bag #%d (%s) is full"%(b+1,a6(a,False)));return
				s["move"]=(e,f,a,b);i=int(c.Graphic or 0);s["pre"]=(i,int(c.Amount or 1),ez(a,i,g));aQ("Sort %d/%d"%(s["i"],len(d)));return
			hb()
		def ha():
			s=p["sort"]
			if s is None or s["move"]is None:return
			a=s["move"];s["move"]=None
			if p["shutting"]:return
			if cI():s["why"]="another target cursor is in use";return
			if aA():s["why"]="you picked something up";return
			try:API.MoveItem(a[0],a[2])
			except Exception as e:s["why"]="a move failed (%s)"%e;return
			aW();s["check"]=a;s["last"]=a[0];s["sent_at"]=time.time();s["at"]=s["sent_at"]+bC
		def hb():
			s,p["sort"]=p["sort"],None
			if s is None:return
			a="%d moved"%s["moved"]
			if s["refused"]:a+=", %d refused"%s["refused"]
			API.SysMsg(an+": sort done: %s."%a,aC if s["refused"]else bd);aQ("Sorted %d"%s["moved"])
		def bb(why=None,user=False):
			s,p["sort"]=p["sort"],None
			if s is None:return
			if user:API.SysMsg(an+": sort stopped (%d moved)."%s["moved"],aK);aQ("Stopped")
			elif why:API.SysMsg(an+": sort stopped: %s (%d moved)."%(why,s["moved"]),aC);aQ("Sort stopped")
		def hc():bY(True);bb(user=True)
		eA="UnifiedBag_filters";db=40;cn=("exact","kind","category");hd={"exact":"this exact item","kind":"this kind","category":"its category"}
		def he():
			p["filters"]=[]
			for d in str(ab(eA,"")or "").split(";"):
				a=d.split("~")
				if len(a)<5 or len(p["filters"])>=db:continue
				try:e=int(a[3])if a[3]!=""else None;f=int(a[2])if a[2]!=""else None;c=tuple(int(h,16)for h in a[1].split(",")if h and not h.startswith("@"))
				except ValueError:continue
				g=a[1][1:]if a[1].startswith("@")else None;b=None
				if len(a)>=7 and ":"in a[5]:
					try:b=(int(a[5].split(":",1)[0],16),int(a[5].split(":",1)[1]))
					except ValueError:b=None
				p["filters"].append({"name":a[0],"gr":c,"cat":g,"hue":f,"slot":e,"on":a[4]=="1","set":frozenset(c),"base":b,"broad":a[6]if len(a)>=7 and a[6]in cn else None})
			H["wanted"]=H["wanted"]or any(i["cat"]for i in p["filters"])
		def bz():N(eA,";".join("~".join((a["name"].replace(";"," ").replace("~"," "),"@"+a["cat"]if a["cat"]else ",".join("%X"%b for b in a["gr"]),""if a["hue"]is None else str(a["hue"]),""if a["slot"]is None else str(a["slot"]),"1"if a["on"]else "0","%X:%d"%a["base"]if a.get("base")else "",a.get("broad")or ""))for a in p["filters"]));p["dirty_flt"]=p["open_flt"]
		def b0():
			a=H["data"]
			if a is None:return
			for f in p["filters"]:
				if f["cat"]:f["set"]=a.get(f["cat"],frozenset())
		def hf():H["wanted"]=True;p["open_flt"]=True;p["dirty_flt"]=True
		def hg():co();bE("flt");p["open_flt"]=False;ap["flt_checks"]=[]
		def co():
			g=ap.get("flt")
			if z(g):p["flt_x"],p["flt_y"]=int(g.GetX()),int(g.GetY())
		def hh():co();p["flt_min"]=not p["flt_min"];p["dirty_flt"]=True
		def eB(name,gr,hue,cat=None,broad=None):
			if len(p["filters"])>=db:API.SysMsg(an+": %d filters is the most; remove one first."%db,aC);return
			f={"name":name,"gr":tuple(gr),"cat":cat,"hue":hue,"slot":None,"on":True,"set":frozenset(gr),"broad":broad};p["filters"].append(f);b0();bz();return f
		def hj(key):
			for k,a in Q:
				if k==key:
					for f in p["filters"]:
						if f["cat"]==key:API.SysMsg(an+": %s is already on the list."%a,aK);return
					eB(a,(),None,key)
		def hk():API.SysMsg(an+": target an item for the new filter.",aK);bX("filter_targeted")
		def eC(target):
			if not target:API.SysMsg(an+": cancelled.",aK);return
			a=Z(target)
			if not a:API.SysMsg(an+": that isn't an item.",aC);return
			if a.IsContainer:API.SysMsg(an+": bags aren't sorted; target an item.",aC);return
			return a
		def hl(target):
			a=eC(target)
			if a:eD(int(a.Graphic),int(a.Hue or 0)&16383,str(a.Name or ""))
		def eD(graphic,hue,name):
			if not name:t=cU(graphic);name=str(t.Name or "")if t is not None else ""
			eB((name or "0x%04X"%graphic)[:30],(graphic,),hue,None,"exact")
		def hm():
			a=safe(cV)
			if a is None:return
			try:d=int(Tz.get(a,"Serial"));c=int(Tz.get(a,"Graphic"));e=int(Tz.get(a,"Hue"))&16383;b=int(Tz.get(a,"Container"))
			except Exception:return
			if safe(lambda:bool(cU(c).IsContainer),False):API.SysMsg(an+": bags aren't sorted; drop an item.",aC);return
			eD(c,e,"")
			if b and b!=0xFFFFFFFF:import System;Tz.call(None,"DropItem",(System.UInt32(d),65535,65535,0,System.UInt32(b),False),al.Actions)
		def hn(i):
			if not 0<=i<len(p["filters"]):return
			f=p["filters"][i]
			if f.get("base")is None and f["gr"]:f["base"]=(f["gr"][0],f["hue"]or 0)
			a=f.get("base")
			if a is None:return
			d=(f.get("broad")or("category"if f["cat"]else("exact"if f["hue"]is not None else "kind")));b=cn[(cn.index(d)+1)%len(cn)]
			if b=="category":
				c=br(a[0])
				if c is None:b="exact"
				else:f.update({"cat":c,"hue":None,"gr":(a[0],)})
			if b!="category":f.update({"cat":None,"hue":a[1]if b=="exact"else None,"gr":(a[0],),"set":frozenset((a[0],))})
			f["broad"]=b;b0();bz()
		def ho(i,d):
			j=i+d
			if 0<=i<len(p["filters"])and 0<=j<len(p["filters"]):p["filters"][i],p["filters"][j]=p["filters"][j],p["filters"][i];bz()
		def hp(i):
			if 0<=i<len(p["filters"]):del p["filters"][i];bz()
		def hq(i):
			if not 0<=i<len(p["filters"]):return
			p["flt_pick"]=p["filters"][i];API.SysMsg(an+": click a bag on the bags display, or target a bag in a slot.",aK);bX("filter_bag_targeted",p["flt_pick"])
		def hr(f,target):
			if p["flt_pick"]is not f:return
			p["flt_pick"]=None
			if not target:return
			a=dict((g,d)for d,g in p["layout"]);s=int(target)
			for c in range(8):
				if s in a:f["slot"]=a[s];bz();return
				b=Z(s);s=int(b.Container or 0)if b else 0
				if not s:break
			API.SysMsg(an+": that isn't in a bag slot; put the bag in a slot first (Slots).",aC)
		def hs(a):
			f,p["flt_pick"]=p["flt_pick"],None
			if f is None:return False
			f["slot"]=a;bz();API.CancelTarget();return True
		def ht():
			for i,b in ap.get("flt_checks")or():
				if i<len(p["filters"]):
					a=bool(safe(lambda:b.IsChecked,p["filters"][i]["on"]))
					if a!=p["filters"][i]["on"]:p["filters"][i]["on"]=a;bz();return
		def hu():
			co();bE("flt");b0();a,j=K,v;t=len(p["filters"]);o,q,r=28,30+3*26+8,40;n=max(o*2,min(t,12)*o+8);w=640;O=(a+30+a if p["flt_min"]else a+30+j+r+j+q+j+n+a);g,d,y=b7("flt",w,O,"SORT FILTERS",av("toggle_flt_min"),av("close_filters"));x=[]
			if not p["flt_min"]:
				h=w-2*a;B(g,a,y,h,r);m(g,d,"sort",M,a+12,y+9,"Sort",et,on_click=av("start_sort"));z=safe(ex);P=len(z)if z else 0;e(g,"%s would move"%F(P,"item"),a+100,y+12,l);y+=r+j;B(g,a,y,h,q,"ADD A FILTER");R=a+12;m(g,d,"add",M,R,y+28,"Add by target...","Target an item: the filter fills in from it",on_click=av("filter_by_target"));s=5;A=(h-24)//s
				for E,(H,k)in enumerate(Q):T,U=(E+1)%s,(E+1)//s;m(g,d,"pre_"+H,ad,a+12+T*A,y+28+U*26,C(k,A-40),"Add the %s preset"%k.lower(),on_click=av("filter_preset",H))
				y+=q+j;B(g,a,y,h,n);S(g,a,y,h,n,av("filter_dropped"),"Drop an item here to add a filter")
				if not t:e(g,"No filters yet. Press a preset, or Add by target.",a+12,y+8,l)
				else:
					b=G.CreateGumpScrollArea(a+4,y+4,h-8,n-8)
					for i,f in enumerate(p["filters"]):
						c=i*o;V=ay(b,"",4,c+3,f["on"],"Use this filter (unticked: kept, moves nothing)");x.append((i,V));e(b,C(f["name"],150),30,c+5);L=f.get("broad")or("category"if f["cat"]else("exact"if f["hue"]is not None else "kind"))
						if f["cat"]and not f.get("base"):e(b,"A preset",186,c+5,l)
						else:m(b,d,"m%d"%i,J,186,c+2,"Match: "+L,"Matches %s; click for the next"%hd[L],on_click=av("filter_broader",i))
						if f["slot"]is None or f["slot"]not in p["assign"]:k,N="No bag",u
						else:k,N=(bk(a6(p["assign"][f["slot"]],False),14),D)
						e(b,k,330,c+5,N);m(b,d,"b%d"%i,M,424,c+2,"Bag...","Click a bag on the bags display, or target a bag in a slot",on_click=av("filter_pick_bag",i));m(b,d,"u%d"%i,J,508,c+2,None,"Move up (the first match wins)",on_click=av("filter_move",i,-1));m(b,d,"d%d"%i,J,536,c+2,None,"Move down (the first match wins)",on_click=av("filter_move",i,1));m(b,d,"x%d"%i,I,564,c+2,None,"Remove this filter",on_click=av("filter_remove",i))
					g.Add(b)
			b8("flt",g,co);ap["flt_checks"]=x
		dc={"sync_at":0.}
		def bo():
			d=ap["rule_checks"]
			if not d or not z(ap["srt"]):return False
			e,f={},set()
			for a,g,l in d:
				if a>=p["slots"]:continue
				f.add(a)
				try:h=bool(l.IsChecked)
				except Exception:h=g in p["rules"].get(a,b_)[0]
				if h:e.setdefault(a,set()).add(g)
			i=False
			for a in f:
				b=p["rules"].get(a);j=b[1]if b is not None else();k=frozenset(e.get(a,()));c=(k,j)if(k or j)else None
				if c!=b:
					i=True
					if c is None:del p["rules"][a]
					else:p["rules"][a]=c
			return i
		def hv():
			bo();cp("srt");a,f=K,v;w,s,n,t=580,52,40,52;i=min(p["slots"]*s+8,430);A=(a+30+a if p["srt_min"]else a+30+f+n+f+i+f+t+a);g,j,y=b7("srt",w,A,"SORT RULES",av("toggle_win_min","srt"),av("close_win","srt"));u=[]
			if not p["srt_min"]:
				h=w-2*a;B(g,a,y,h,n);m(g,j,"sort",M,a+12,y+9,"Sort","Move matching items from your backpack and other slot bags into their bag, one at a time",on_click=av("start_sort"));m(g,j,"stop",I,a+150,y+9,"Stop","Stop sorting",on_click=av("stop_sort",None,True));e(g,"Tick what each slot's bag holds.",a+250,y+12,l);y+=n+f;B(g,a,y,h,i);c=G.CreateGumpScrollArea(a+4,y+4,h-8,i-8);q=h-8-20;C=q-171-o("+%d graphics"%b6)
				for b in range(p["slots"]):
					d=b*s;D,k=p["rules"].get(b,b_);e(c,"#%d"%(b+1),6,d+5,E)
					if b in p["assign"]:e(c,bk(a6(p["assign"][b],False),24),44,d+5)
					else:e(c,"No bag in this slot",44,d+5,l)
					H=e(c,("+%s"%F(len(k),"graphic"))if k else "",C,d+5,l)
					if k:H.SetTooltip(", ".join("0x%04X"%W for W in k))
					m(c,j,"add%d"%b,M,q-165,d+3,"Add...","Target an item; slot #%d's bag holds its graphic too"%(b+1),on_click=av("add_rule_graphic",b));m(c,j,"clr%d"%b,I,q-80,d+3,"Clear","Forget the graphics added to slot #%d"%(b+1),on_click=av("clear_rule_graphics",b));x=24
					for z,r,L in aD:J=ay(c,r,x,d+27,z in D,"Slot #%d's bag holds %s"%(b+1,r.lower()));u.append((b,z,J));x+=36+o(r)
				g.Add(c);y+=i+f;B(g,a,y,h,t);e(g,"Sort moves one item every %.1f s from your backpack and other bags."%bC,a+12,y+8,l);e(g,"It stops when you pick something up or a bag is full.",a+12,y+28,l)
			b8("srt",g,c1,rule_checks=u);dc["sync_at"]=time.time()+1.
		def hw(idx):API.SysMsg(an+": target an item; slot #%d's bag will hold its graphic."%(idx+1),aK);bX("add_rule_graphic_to",idx)
		def hx(idx,target):
			if target:
				bo()
				if idx>=p["slots"]:return
			c=eC(target)
			if not c:return
			a=int(c.Graphic);d,b=p["rules"].get(idx,b_)
			if not a or a in b:API.SysMsg(an+": slot #%d's bag already holds that."%(idx+1),aK);return
			if len(b)>=b6:API.SysMsg(an+": slot #%d already holds %d graphics; click Clear first."%(idx+1,b6),aC);return
			p["rules"][idx]=(d,b+(a,));p["dirty_srt"]=True;ba();API.SysMsg(an+": slot #%d's bag holds graphic 0x%04X too."%(idx+1,a),bd)
		def hy(idx):
			bo();a,b=p["rules"].get(idx,b_)
			if not b:return
			if a:p["rules"][idx]=(a,())
			else:p["rules"].pop(idx,None)
			p["dirty_srt"]=True;ba()
		def cp(k):cq();bE(k)
		def cq():
			for a,b,c in(("mgr","mgr_x","mgr_y"),("trp","trp_x","trp_y"),("srt","srt_x","srt_y")):
				g=ap[a]
				if z(g):p[b]=g.GetX();p[c]=g.GetY()
		def hz():
			if H["data"]is not p["cats_seen"]:p["cats_seen"]=H["data"];b0();p["dirty_flt"]=p["open_flt"]
			if p["open_flt"]:
				if p["dirty_flt"]:p["dirty_flt"]=False;hu()
				elif not z(ap.get("flt")):p["open_flt"]=False;ap["flt_checks"]=[]
				else:ht()
			for k,b in(("mgr",gA),("trp",gL),("srt",hv)):
				if not p["open_"+k]:p["dirty_"+k]=False
				elif p["dirty_"+k]:p["dirty_"+k]=False;b()
				elif not z(ap[k]):
					p["open_"+k]=False
					if k in cj:ap[cj[k]]=[]
				elif k=="srt"and ap["rule_checks"]:
					a=time.time()
					if a>=dc["sync_at"]:
						dc["sync_at"]=a+1.
						if bo():bh()
		def hA():
			c,d=r.max_w,r.max_h
			if c<=0 or d<=0:p["fit_seen"]=None;return
			a=(min(c,bc),min(d,bc))
			if a==(p["cell_w"],p["cell_h"]):p["fit_seen"]=None;return
			b=p["fit_seen"];p["fit_seen"]=(a,b[1]+1 if b and b[0]==a else 1)
			if p["fit_seen"][1]>=eX or p["fit_pending"]:p["fit_pending"]=False;p["fit_seen"]=None;p["cell_w"],p["cell_h"]=a;bj()
		def hB():
			if p["drive_fixed"]or not z(ap["grid"]):return
			a=time.time()
			if r.hook_calls!=p["hb_frame"]:
				p["hb_frame"]=r.hook_calls;p["hb_time"]=a
				if p["driving"]:p["driving"]=False
				return
			if not p["driving"]and a-p["hb_time"]>e1:
				p["driving"]=True
				if r.hook_calls==0 and not p["drive_told"]:p["drive_told"]=True;API.SysMsg(an+": draw hook isn't called; the script keeps the bags in place (they may flicker when items move).",aK)
		hC={"add_rule_graphic":hw,"add_rule_graphic_to":hx,"add_trap_bag":gN,"add_trap_bag_to":gO,"assign_slot":gB,"assign_slot_to":gC,"auto_fill":gF,"bag_close":gb,"bag_min":ga,"bag_use":f9,"clear_all":gE,"clear_rule_graphics":hy,"clear_slot":gD,"close_filters":hg,"close_win":gy,"disable":HOST.disable,"filter_bag_targeted":hr,"filter_broader":hn,"filter_by_target":hk,"filter_canvas_pick":hs,"filter_dropped":hm,"filter_move":ho,"filter_pick_bag":hq,"filter_preset":hj,"filter_remove":hp,"filter_targeted":hl,"fold_to_bar":ej,"open_filters":hf,"open_win":c0,"quick_press":g2,"remove_trap_bag":gP,"select_all_traps":gM,"set_min":gv,"show_settings":aX,"start_job":gQ,"start_sort":ey,"stop_all":hc,"stop_sort":bb,"toggle_bare":gu,"toggle_flt_min":hh,"toggle_win_min":gz,"user_collapse":gt}
		def eE(w):return(("LAYOUT  (Apply to use)",(("num","slots","Slots:","Bag slots (%d-%d)"%(b1,a1),"",b1,a1),("num","cols","Columns:","Slots per row outside a zone (0-%d, 0 = near-square)"%a1,"",0,a1),("num","rows","Rows:","Rows of slots outside a zone (0-%d, 0 = near-square)"%a1,"",0,a1),("num","scale","Bag scale:","The client's Container Scale, for every container (50-200)","%",50,200),("buttons",(("apply",ad,"Apply","Use the slots, columns, rows and scale above"),),{"bdy":4})),{"top":32,"sh":182,"ldy":2,"fw":60,"ugap":6,"lw":w-122}),("LOOK",(("slider","opacity","Bag opacity:","How solid bag panels and art are (10-100%); items stay solid",10,100,{"lw":158,"sdy":6,"sw":200,"ugap":20,"vfmt":"%d%%","h":30}),("check","trim","Trim bags to their item area","Hide bag art and butt the item areas together (needs client access; zones always fill)"),("check","items","Scale items with the bags","The client's option to draw items at bag scale")),{"top":32,"sh":116,"ldy":2}),("STATUS",(("note",bk(c2(),64),{"key":"status","h":24}),("note",en(),{"key":"size"})),{"top":32,"sh":86}))
		hD=Kit.Page(dv,eE,ba)
		def dd():
			p["shutting"]=False
			if not API.Player:p["wait_player"]=True;return
			p["wait_player"]=False;a=p["load_text"];p["load_text"]=None
			if a is None and aO():p["wait_load"]=p["load_wanted"]=True;p["to_write"]=None;return
			p.update(wait_load=False,load_wanted=False,driving=False,drive_fixed=False,drive_told=False,job=None,to_write=None,queue=[],reported=False,detached_at=0.);bU["told"]=False;dy();p["docked"],p["link_state"]=False,None;API.RemoveSharedVar(cA);bw["wish"]=0.;aE["cols"],aE["cell"],aE["area"],aE["told"]=None,None,None,None;aP["pct"]=None;cR();he();b0();p["canvas"]=None;JR["rd"]=aY();r.meas.clear();r.opened=frozenset()
			if not al.tried:al.tried=True;fo()
			b={"fit":bH,"riding":aG}
			if bI():b.update({"exact":True,"verify":True,"state":fF})
			HOST.layout_add(aH,fE,an,b)
			if al.ok:gg()
			p["sort"]=None;SR.update({"armed":False,"lit":{},"until":0.,"counts":{},"status":None})
			if a is not None:dN(a[0])
			else:dK()
			p["open_mgr"]=p["dirty_mgr"]=p["want_mgr"];p["open_trp"]=p["dirty_trp"]=p["want_trp"];p["open_srt"]=p["dirty_srt"]=p["want_srt"]
			if c_()and not am(aH):p["minimized"]=True
			ek();r.disabled,r.fail_streak,r.error=False,0,""
			if al.ok:
				try:bq(ca)
				except Exception as e:r.error="client thread: %s"%e
			else:Y(aH);API.SysMsg(an+": no client access (%s); using basic pinning."%al.error,aC)
			cK();p["dirty_frame"]=True;p["hb_frame"],p["hb_time"]=-1,time.time()
			for c,d in(("bag.attach",gk),("bag.grid_size",lambda:p["grid_wh"]),("bag.fit",gh),("bag.cell",fG),("bag.shrink",cY),("bag.pack",gi),("bag.open_manager",av("open_win","mgr")),("bag.open_traps",av("open_win","trp")),("look.bags",lambda:p.update(dirty_frame=True))):dw.service(c,d)
			aL(P,"hooked",("OnItemUpdated",f0));API.SysMsg(an+": on, %s."%F(p["slots"],"slot"),bd)
		def hE():
			if p["wait_player"]:
				if API.Player:dd()
				return
			if p["wait_load"]:
				if p["load_text"]is not None:dd()
				return
			while p["queue"]:
				b=p["queue"].pop(0);c=hC[b[0]]
				try:c(*b[1:])
				except Exception as e:API.SysMsg(an+": couldn't do that (%s)."%e,aC)
			if p["shutting"]:return
			ek();cK()
			if al.ok and r.disabled and not p["reported"]:p["reported"]=True;API.SysMsg(an+": draw hook stopped (%s); using basic pinning."%r.error,aC);safe(lambda:bq(dG));p["dirty_frame"]=True
			if not z(ap["bar"])or not z(ap["grid"]):p["dirty_frame"]=True
			if(r.icons or bB)!=p["icons_used"]:p["dirty_frame"]=True
			if al.ok and not r.disabled:
				hB()
				if p["driving"]:
					try:bq(cC)
					except Exception as e:r.error="client thread: %s"%e
				hA();fR()
			else:
				if p["canvas"]is not None:d3(None)
				gw()
			if p["dirty_frame"]and not bT():p["dirty_frame"]=False;gp()
			else:
				if aG():el()
				ei()
			hz();gS();a=time.time()
			if not 0<=p["quick_at"]-a<=1.:
				p["quick_at"]=a+1.
				if ap.get("quick_sig")is not None and ap["quick_sig"]!=da():p["dirty_frame"]=True
			g0(a);g9(a);ha();gf(a)
			if(p["frame_x"],p["frame_y"])!=(p["saved_fx"],p["saved_fy"])and p["save_in"]<0 and not aG()and p["canvas"]!="alone"and a-p["detached_at"]>=e5:bh()
			if p["save_in"]>0:p["save_in"]-=1
			elif p["save_in"]==0:cq();ba()
		def hF():
			if p["load_wanted"]:
				p["load_wanted"]=False;a=dM()
				if p["wait_load"]and not p["shutting"]:p["load_text"]=(a,)
			fS()
			if H["wanted"]and H["data"]is None:
				H["wanted"]=False
				try:bl(al.f_tiles)
				except Exception:H["data"]={}
			cJ()
		def hG():return eZ if p["driving"]else eY
		def hH():return bool(p["load_wanted"]or p["to_write"]is not None or d4()or(H["wanted"]and H["data"]is None))
		dK()
		def hI():
			p["shutting"]=True
			if p["wait_player"]or p["wait_load"]:p["wait_player"]=p["wait_load"]=p["load_wanted"]=False;p["load_text"]=None;return
			safe(bY);p.update(job=None,queue=[],sort=None);safe(lambda:cl(time.time()));bo();bx();dw.close();HOST.layout_remove(aH)
			if aP["pct"]is not None:safe(lambda:cY(None))
			if p["attach"]is not None:p["attach"]=None;p["frame_x"],p["frame_y"]=p["saved_fx"],p["saved_fy"]
			p["grid_wh"]=None;p["docked"],p["link_state"]=False,None;API.SetSharedVar(dt,"off");safe(cR);p["canvas"]=None
			if al.ok:safe(lambda:bq(dG))
			cq();ba();cJ()
			for a in("grid","bar","mgr","trp","srt"):bE(a)
			p["open_mgr"]=p["open_trp"]=p["open_srt"]=False;ap.update({"side_status":None,"trap_checks":[],"rule_checks":[],"search_box":None,"counts":[]});p.update(bar_raw=None,grid_raw=None,grid_info=(None,False),slot_raws=())
		return{"start":dd,"tick":hE,"stop":hI,"client_tick":True,"config_height":hD.height,"build_config":gG,"poll_config":gH,"config_closed":eo,"interval":hG,"thread_tick":hF,"thread_wanted":hH}
	def bt():
		F="character";t="Paperdoll";bo="Character_settings";aR="Character_pos";aS="Character_min";b4,b5=240,46;b6=7939;m=48;am=6;b7=16;bp,b8=260,237;ad=80;bq=.2;de=.85;b9=.95;ca=90;br=30;cb=74;cc,cd=40,3.5;ce=.1;U=v;cf=.5;bs=5;bt,bu=50000,60000;cg,ch=970,547;cj=(694,695)
		try:import clr;from System import Array,Object,UInt32,UInt16,Int32,Double,Enum;from System.Reflection import BindingFlags;bv=True
		except Exception:bv=False
		ay=((6,"helmet","Helm","Head"),(13,"torso","Chest","Chest armour"),(19,"arms","Arms","Arms"),(7,"gloves","Gloves","Gloves"),(24,"legs","Legs","Leg armour"),(18,"earrings","Ears","Earrings"),(10,"neck","Neck","Necklace / gorget"),(17,"tunic","Tunic","Tunic / surcoat (over the chest)"),(12,"waist","Belt","Belt / half apron"),(3,"shoes","Feet","Shoes / boots"),(5,"shirt","Shirt","Shirt"),(22,"robe","Robe","Robe"),(20,"cloak","Cloak","Cloak / quiver"),(23,"skirt","Kilt","Skirt / kilt"),(4,"pants","Pants","Pants"),(1,"onehanded","Main","Main hand (one-handed weapon)"),(2,"twohanded","Off","Off hand (shield, two-handed weapon)"),(8,"ring","Ring","Ring"),(14,"bracelet","Brace","Bracelet"),(9,"talisman","Talis","Talisman"),);aW=5;bx=set(dj[0]for dj in ay);ck=tuple(dk[0]for dk in ay);cl={"neck":("Necklace",),"onehanded":("OneHanded",),"twohanded":("TwoHanded",),"earrings":("Earrings",),"bracelet":("Bracelet",),"talisman":("Talisman",)};aX,aY,az,ag,aZ,aC,a_,a0=(1,2,3,4,5,6,7,8);a1,a2,ah,a4,I,a5,an,ap=(9,10,11,12,13,14,15,16);aq,a6,W,aD,at,aF,au=17,18,19,20,22,23,24;by=dict((dl[0],dl[1])for dl in ay);by.update({ah:"hair",ap:"beard",an:"face"});bz=(aD,aZ,ag,az,au,W,I,aq,a0,a5,an,a_,aF,at,a4,a2,ah,ap,a6,aC,aX,aY,a1);cm=(aZ,ag,az,au,W,I,aq,a0,a5,an,a_,aF,at,aD,a4,a2,ah,ap,a6,aC,aX,aY,a1);cn=(aZ,ag,az,au,W,I,aq,aD,a0,a5,an,a_,aF,a4,a2,ah,ap,a6,aC,aX,aY,a1,at);bA=tuple(sorted(set(bz)));a7=(39301,39302,42002,41675,41674);bB={400:12,402:12,401:13,403:13,605:14,607:14,606:15,608:15,666:666,694:666,667:665,695:665,1253:51253,987:12};co=(401,403,606,608,667,695);bC,cp,cq=987,1002,50987;M=K;E=8;aj=m+am;cr=aW*aj-am;L=E*2+2*(2*m+am)+2*E+bp;Y=E*2+cr;bD=4*E+2*(2*m+am);cs=100;a9=bD+cs;ct=(150,235);av=2;cu=300;bE=L+2*M;H=M+30+v;q={"stats":True,"combine":True,"beside":False,"left":False};df=dict(q);d={"shutting":False,"minimized":False,"docked":False,"queue":[],"sig":None,"doll_sig":None,"stats_at":0.,"doll_at":0.,"px":M,"attached":None,"beside_said":False,"layer_name":{},"wait_player":False,"saved_min":False,"w_armed":True,"w_at":0.,"wbar":None,"fit":None,"k":1.,"py":None,"strip_w":None,"pw":L,"col":None,"ph":Y,"rp":aj,"pair":None,"pair_at":0.,"room":None,"room_fs":None,"told_shrink":None,"grew":False,"paired":False};k={"g":None,"c":{},"store":({},{}),"slots":[],"raw":None,"doll":[]};dg,n,dh=ak(d,t)
		def bF():
			p=ab(bo).split("|")
			if len(p)>=2:q["stats"]=p[0]=="1";q["combine"]=p[1]=="1"
			if len(p)>=3:q["beside"]=p[2]=="1"
			if len(p)>=4:q["left"]=p[3]=="1"
			d["saved_min"]=bool(Kit.load_min(aS))
		def bG():N(bo,"|".join(["1"if q[a]else "0"for a in("stats","combine","beside","left")]+["0"]))
		def cv():
			if not d.get("wait_player"):ba(aS,d["minimized"]and not d["docked"])
		def bH():bb(aR,k["g"])
		class Box(object):pass
		j=Box();j.tried=j.ok=False;j.error,j.pixel_n="",0
		for cw in("m_animid","m_covered","MobileType","cursor","SlotItem","DollPiece","m_pixel","gumps","f_tiles","tiles"):setattr(j,cw,None)
		def cx():
			if not bv:j.error="clr module unavailable";return
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
							if self.va_down:cB(self)
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
			j.f_tiles=safe(aN)
			try:p=a.GetType("ClassicUO.Game.UI.Controls.PaperDollInteractable");j.m_animid=p.GetMethod("GetAnimID",b)if p is not None else None;j.animid_n=(int(j.m_animid.GetParameters().Length)if j.m_animid is not None else 0)
			except Exception:j.m_animid=None
			try:j.MobileType=a.GetType("ClassicUO.Game.GameObjects.Mobile");j.m_covered=(j.MobileType.GetMethod("IsCovered",b)if j.MobileType is not None else None)
			except Exception:j.m_covered=None
		bI={}
		def aw(layer):
			e=bI.get(layer)
			if e is None:e=bI[layer]=Enum.ToObject(j.LayerType,layer)
			return e
		cy={};cz=256
		def bJ():a=k["raw"];return None if a is None else a.World
		def cA():w=bJ();return None if w is None else w.Player
		def bd():
			try:
				b=j.cursor
				if b is None:c=j.p_game.GetValue(None,None);d=j.p_uo.GetValue(c,None)if c is not None else None;b=j.cursor=j.p_cursor.GetValue(d,None)if d is not None else None
				h=b.ItemHold
				if h.Enabled and not h.IsFixedPosition:
					a=cC(int(h.Graphic))
					if a not in bx:
						try:a=int(h.Layer)
						except Exception:a=0
					return int(h.Serial),bool(h.IsWearable),a
			except Exception:pass
			return
		def cB(piece):
			try:
				a=j.cursor
				if a is None:b=j.p_game.GetValue(None,None);c=j.p_uo.GetValue(b,None)if b is not None else None;a=j.cursor=j.p_cursor.GetValue(c,None)if c is not None else None
				h=a.ItemHold
				if h.Enabled and int(h.Serial)==int(piece.LocalSerial):piece.va_down=False;h.IsGumpTexture=False;h.MouseOffset=j.Point(0,0)
			except Exception:piece.va_down=False
		def cC(graphic):
			try:
				a=j.tiles
				if a is None:
					if j.f_tiles is None:return 0
					a=j.tiles=j.f_tiles.GetValue(None)
				return 0 if a is None or graphic<0 or graphic>=a.Length else int(a[graphic].Layer)
			except Exception:return 0
		def bf(c,x,y):c.Location=j.Point(x,y)
		cD=Kit.disposer(F,d,k);bK=2*m+am
		def cE(i):
			a,b=divmod(i,aW)
			if a<2:x=d["px"]+E+a*aj
			else:x=d["px"]+d["pw"]-E-bK+(a-2)*aj
			return x,bi()+E+int(round(b*d["rp"]))
		def bg():return bool(ao(F))
		def bL():x=d["px"]+2*E+bK;return(x,bi()+E,max(1,d["pw"]-bD),max(1,d["ph"]-2*E))
		def bi():a=d["py"];return H if a is None else a
		bj,bM=.4,2.;bN=300
		def cF(w,h,mode):
			a=(int(w),int(h))if(w is not None and h is not None)else None
			if a!=d["fit"]or(mode=="again"and a is not None and not d["paired"]):d["fit"]=a;d["pair"]=bO()if a is not None else None;d["pair_at"]=time.time();n("redraw")()
		def bO():
			if d["attached"]is None:return
			try:a=HOST.layout_pair(F,"bag")
			except Exception:return
			if not a or a[0]is None or a[1]is None:return
			return(tuple(int(b)for b in a[0]),tuple(int(c)for c in a[1]))
		def cG(x,y,fw,fh,k):
			(q,r,s,t),(g,h,l,m)=k
			if abs((y+fh)-h)>2*SNAP_DIST:return
			i,n=max(0,g-x),min(fw,g+l-x);b=n-i-2*M
			if b<40:return
			o=U//2;e=fh+o;a=(h+m-y)-e-M
			if a<20:return
			d["room"]=(b,a);f=bm(b,a);d["room_fs"]=f;c=f[1]if f is not None else bQ(b);d["grew"]=c>a
			if c>a:j=int(aM()[1]);p=(j-y-M-e)if j>0 else c;a=max(a,min(c,p))
			return(i+M,e,b,a)
		def aI(c,raw=False,flushed=False):
			k=d["k"]
			if abs(k-1.)<.001 or c is None:return
			with Kit.quiet:
				if not raw and not flushed:aa()
				a=c if raw else ai(c)
				if a is None:return
				if str(a.GetType().Name)=="GumpPicTiled":a.ScaleTiledTexture=True
				a.ApplyScale(k,True,True,False)
		def bl():
			e=Q("bag.cell")
			if e is None:return
			try:v=e();b,c,f,n,g=v[0],v[1],v[2],v[3],v[4];d,a,h=(v[5],v[6],v[7])if len(v)>=8 else(100,100,100)
			except Exception:return
			if n<=0 or b<=0 or c<=0 or d<=0 or a<=0:return
			if d!=a:b,c=b*a/float(d),c*a/float(d)
			return b,c,f,n,g,a,min(h,a)
		def bP(ci,f,width):e,g,a,n,d=ci[0],ci[1],ci[2],ci[3],ci[4];b=int(math.ceil(e*f-.01));h=int(math.ceil(g*f-.01));i=max(b,width-d);j=max(1,min(n,(i+a)//(b+a)));c=int(math.ceil(n/float(j)));return c,c*h+(c-1)*a,b+d
		def bQ(width):
			b=Q("bag.pack")
			if b is not None:
				try:a=b(width,1<<20)
				except Exception:a=None
				if a is not None:return a[1]
			c=bl();return 120 if c is None else bP(c,1.,width)[1]
		def bm(hw,f):
			g=Q("bag.pack")
			if g is not None:
				try:c=g(hw,f)
				except Exception:c=None
				if c is not None:return c
			a=bl()
			if a is None:return
			b,e=a[5],a[6];h=d["told_shrink"];p=b
			for m in range(int(b-e)//bs+2):
				j,i,k=bP(a,p/float(b),hw);l=3*j if(h is not None and p>h)else 0
				if(i+l<=f and k<=hw)or p<=e:return(None if p>=b else p),i
				p=max(e,p-bs)
		aJ=10;bR,cH=20,26;aK=14;bS=2*8+aJ*bR+aK
		def bn():
			if r["col_w"]is None:a=max(o(b)for b in("Stamina 999/999","Followers 99/99","Gold 9,999,999","Weight 0000/0000","Mana 999/999","HP 999/999"));r["col_w"]=max(br,a)+2*ac+4
			return r["col_w"]
		def cI(bw,room):
			e=ct;b=[]
			if q["stats"]:
				if bw>=bN:b.append(("strip",bw,room-ad-v))
				b.append(("col",bw-bn()-v,room))
			else:b.append(("none",bw,room))
			h,i=float(max(1,e[0])),float(max(1,e[1]));a=None
			for g,d,c in b:
				if g=="col"and c<bS:continue
				k=min(d/float(a9),c/float(Y),bM)
				if k<bj:continue
				f=min((d-2*E*k)/h,(c-2*E*k)/i)
				if a is None or f>a[0]+.001 or(f>a[0]-.001 and k>a[4]):a=(f,g,d,c,k)
			if a is None:k=min(bw/float(a9),room/float(Y),bM);return "none",bw,room,max(bj,k)
			return a[1],a[2],a[3],a[4]
		def cJ(bw):
			a=int(math.ceil(bj*Y))+1
			if not q["stats"]:return a
			return a+ad+v if bw>=bN else max(a,bS)
		def bT(fw,fh,combined):
			c,h=M,H;a,b=max(1,fw-2*M),max(1,fh-H-M);d=U;i=max(b-bQ(a)-d,min(b,max(cJ(a),(b-d)//2)))if combined else b;e,n,o,k=cI(a,i);p=max(a9,int(round(n/k)));j=max(Y,int(round(o/k)));f=int(round(j*k));q=(ad+v)if e=="strip"else 0;g,r=h,c
			if combined:l=max(i,f+q);m=(c,h+l+d,a,max(1,b-l-d))
			else:m=None
			s=(g+f+v)if e=="strip"else None;t=a if e=="strip"else None;u=(c+a-bn(),g,bn(),f)if e=="col"else None;return(k,int(round(r/k)),int(round(g/k)),s,t,m,(c,g+f),p,u,j)
		def ax():return Y+(v+ad if q["stats"]else 0)
		def cK(a,c):b=max(L,a);w=b+2*M;e=M+(b-L)//2;d=H+ax()+U;f=(M+(b-a)//2,d,a,c);return w,d+c+M,e,f
		def cL(a,b):w=M+L+U+a+M;c,d=(M,M+a+U)if q["left"]else(M+L+U,M);return w,H+max(ax(),b)+M,d,(c,H,a,b)
		def cM(a,b):
			if not q["beside"]:
				w,h,e,f=cK(a,b);c=int(aM()[1])
				if c<=0 or h<=c:return w,h,e,f
				if not d["beside_said"]:d["beside_said"]=True;API.SysMsg(t+": bag grid too tall to stack; bags go beside the doll.",l)
			return cL(a,b)
		def cN():
			if q["beside"]:return((M,H)if q["left"]else(M+L+U,H))
			return M,H+ax()+U
		def bU(g,w,h,hole):
			c,b,d,n=hole;a=a3;s=[V(a+G)for G in range(9)];e,v,f,x,A,r,i,q,j=s;k=[]
			for y,z,t,u in((0,0,w,b),(0,b,c,h-b),(c+d,b,w-c-d,h-b),(c,b+n,d,h-b-n)):
				if t>0 and u>0:k.append(R(g,a+4,y,z,t,u))
			if all(bw[0]>0 and bw[1]>0 for bw in s):k+=[R(g,a+1,e[0],0,w-e[0]-f[0],v[1]),R(g,a+7,i[0],h-q[1],w-i[0]-j[0],q[1]),R(g,a+3,0,e[1],x[0],h-e[1]-i[1]),R(g,a+5,w-r[0],f[1],r[0],h-f[1]-j[1]),ae(g,a+0,0,0),ae(g,a+2,w-f[0],0),ae(g,a+6,0,h-i[1]),ae(g,a+8,w-j[0],h-j[1])]
			l,m=V(ar)
			if l and m and ar:
				for o,p in((0,0),(w-l,0),(0,h-m),(w-l,h-m)):
					if o<c+d and o+l>c and p<b+n and p+m>b:continue
					k.append(ae(g,ar,o,p))
			with Kit.quiet:Kit._frame_parts[g]=[ci for ci in k if ci is not None]
		def Z():
			u,k["g"]=k["g"],None;bW();O=({},{});f={};Z=[];c=d["attached"];b=None;d.update({"px":M,"k":1.,"py":None,"strip_w":None,"pw":L,"col":None,"ph":Y,"rp":aj});x=d["fit"]if not d["minimized"]else None;aa=M
			if z(u):y,C=u.GetX(),u.GetY()
			else:y,C=Kit.load_pos(aR,(200,120),(bE,H+ax()+M))
			P=aG(F);d["paired"]=False
			if P is not None:y,C=P[0],P[1]
			if d["minimized"]:w,h=b4,b5;g=G.CreateGump(True,True);f["status"]=Kit.mini_bar(g,O,w,h,t,F,n("toggle_min"));A(f["status"],t+" & bags"if c is not None else t)
			else:
				w,h=bE,H+ax()+M;g=G.CreateGump(False,True)
				if x is not None:
					w,h=x;Q=cG(y,C,w,h,d["pair"])if(c is not None and d["pair"])else None
					if Q is not None:am=U//2;d["paired"]=True;(ab,d["px"],d["py"],ac,d["strip_w"],_h,ae,d["pw"],d["col"],d["ph"])=bT(w,h-am+M,False);b=Q;h=b[1]+b[3]+M
					else:(ab,d["px"],d["py"],ac,d["strip_w"],b,ae,d["pw"],d["col"],d["ph"])=bT(w,h,c is not None)
					d["k"]=ab;d["rp"]=(d["ph"]-2*E-m)/float(aW-1);aa=ae[0]
					if b is not None:
						bU(g,w,h,b);c["dx"],c["dy"]=b[0],b[1]
						if Q is None:d["room"]=(b[2],b[3]);d["room_fs"]=bm(b[2],b[3]);d["grew"]=(d["room_fs"]is not None and d["room_fs"][1]>b[3])
						aL((b[2],b[3]));fs=d["room_fs"];bV(fs[0]if fs is not None else None)
					else:af(g,w,h);aL(None)
				elif c is not None and c.get("grid_wh"):gw,gh=c["grid_wh"];w,h,d["px"],b=cM(int(gw),int(gh));bU(g,w,h,b);c["dx"],c["dy"]=b[0],b[1]
				else:af(g,w,h)
				if x is None:aL(None)
				V=d["px"];ag=None
				if c is not None:ag=[("traps",J,"Traps","Pick the bags Trap and Untrap cast on",n("bag_traps")),("bags",J,"Slots","Put a bag in each slot",n("bag_mgr"))]
				be(g,O,w,t,F,n("toggle_min"),n("to_bar"),n("settings"),extra=ag);i=[];py=bi();pw,ph=d["pw"],d["ph"];i.append(B(g,V,py,pw,ph));i.append(S(g,V,py,pw,ph,lambda*a:None,None,movable=not bg()));mx,my,mw,mh=bL();f["doll_bg"]=R(g,9274,mx,my,mw,mh,.35);i.append(f["doll_bg"]);f["doll_drop"]=S(g,mx,my,mw,mh,n(("drop",0)),"Drop an item here to wear it",movable=True);i.append(f["doll_drop"])
				for I,(ah,an,ai,ao)in enumerate(ay):K,N=cE(I);i.extend(Kit.gold_box(g,K,N,m,m));l=G.CreateGumpColorBox(.01,"#000000");l.SetRect(K,N,m,m);aB(l,n(("drop",ah)));ak=ao+": drop an item to wear it";l.SetTooltip(ak);g.Add(l);W=e(g,ai,K+(m-o(ai))//2,N+m-b7,D);W.SetAcceptMouseInput(False);i.append(l);i.append(W);Z.append({"layer":ah,"name":an,"x":K,"y":N,"drop":l,"label":W,"serial":0,"ctrl":None,"raw":None,"tip":ak})
				cO(i)
				if x is not None:p,X,s=ac,d["strip_w"],aa
				else:p=(H+Y+v)if q["stats"]else None;X,s=L,V
				if p is not None:
					B(g,s,p,X,ad);S(g,s,p,X,ad,lambda*a:None,None,movable=not bg())
					for I in range(3):f["stats%d"%(I+1)]=e(g,"",s+10,p+8+24*I,D)
					c2(g,f,s,p+56)
				elif d["col"]is not None:c3(g,f,d["col"])
			xy=bc(g,y,C,w,h,F,d["minimized"]and d["docked"],cD(g),bH,k,{"g":g,"c":f,"store":O,"slots":Z});bk(F,g,xy);al=r["hooks"]
			if al is not None:al["verify"]=not d["paired"]
			k["raw"]=Kit._raw_gump(g)if j.ok else None
			if c is not None:c["g"],c["raw"]=g,None
			b1();d.update({"sig":None,"doll_sig":None,"stats_at":0.,"stats_key":None,"doll_at":0.,"wbar":None});T(u)
		di=None;r={"col_w":None,"bounds":{},"need":[],"redo":False,"order":[],"hooks":None}
		def aL(room):
			if room is None:d["room"]=None;bV(None)
			if room==d.get("told_bags"):return
			d["told_bags"]=room;a=Q("bag.fit")
			if a is not None:safe(lambda:a(*(room or(None,None))))
		def bV(pct):
			if pct==d["told_shrink"]:return
			d["told_shrink"]=pct;a=Q("bag.shrink")
			if a is not None:safe(lambda:a(pct))
		def cO(ctrls):
			if abs(d["k"]-1.)<.001:return
			aa()
			for a in ctrls:
				if a is not None:aI(a,flushed=True)
		def bW():
			for s in k["slots"]:
				if s["ctrl"]is not None:T(s["ctrl"]);s["ctrl"]=None
			k["slots"]=[];bX()
		def bX():
			for p in k["doll"]:T(p)
			k["doll"]=[]
		def bY():return "docked"if d["docked"]else("collapsed"if d["minimized"]else "open")
		def bZ(name):
			b=d["layer_name"].get(name)
			if b is not None:
				try:return API.FindLayer(b)
				except Exception:return
			for c in(name,)+cl.get(name,()):
				try:a=API.FindLayer(c)
				except Exception:a=None
				if a:d["layer_name"][name]=c;return a
			return
		def cP(p,keep=None):
			c={}
			if j.ok and p is not None:
				try:
					i=cy
					for e in bA:
						a=p.FindItemByLayer(aw(e))
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
						if len(i)>=cz:i.clear()
						i[m]=g;c[e]=(f,b,h)+g
					l=(int(p.Graphic),int(p.Hue),bool(p.IsFemale));return c,l
				except Exception:
					c={}
					if keep is not None:keep.clear()
			try:k=API.Player
			except Exception:k=None
			if not k:return c,None
			for e in bA:
				a=bZ(by[e])
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
			l=(b,r,b in co);return c,l
		def cQ(graphic,hue,b):
			if graphic==bC:return bB[bC],cp,cq
			a=bB.get(graphic)
			if a is None:a=13 if b else 12
			return a,hue,0
		def cR(b,g,a,c):
			if j.m_animid is not None:
				try:
					if j.animid_n==4:d=[UInt16(b),UInt16(g),UInt16(a),bool(c)]
					else:d=[UInt16(b),UInt16(a),bool(c)]
					v=int(j.m_animid.Invoke(None,Array[Object](d)))
					if v>0:return v
				except Exception:j.m_animid=None
			if a==cg and b in cj:a=ch
			h,i=(bu,bt)if c else(bt,bu);e=a+h
			if V(e)==(0,0):
				f=a+i
				if V(f)!=(0,0):return f
			return e
		def cS(layer,gfx,p=None):
			if j.m_covered is not None and j.ok and p is not None:
				with Kit.quiet:return bool(j.m_covered.Invoke(None,Array[Object]([p,aw(layer)])))
			a=gfx.get(at);b=gfx.get(ag)
			if layer==az:
				if gfx.get(au)is not None or b==5137:return True
				if b in(1299,1300)or a==1284:return True
			elif layer==ag:
				if gfx.get(au)is not None or a==1284:return True
				if b in(491,997,1003):
					c=gfx.get(aF)
					if c is not None and c not in(455,484):return True
					if a is not None and a!=553 and(a<=1255 or a>1259):return True
			elif layer==aq:
				if a is not None:return a!=0 and a not in a7
			elif layer==I:
				if a is not None and a!=0 and a not in a7:return True
				d=gfx.get(aq)
				if d is not None and d not in(5441,5442):
					if gfx.get(I)in(30762,30763):return True
			elif layer==W:return a is not None and a!=0 and a not in a7
			elif layer in(aC,ah):
				if a is not None:
					if a>12659:
						if a in(19357,30742):return True
					elif a<=9863:
						if a<9859:return 8270<=a<=8271
						return True
					elif a in(12217,12659):return True
			return False
		def cT(items):
			c=dict((i,p[1])for i,p in items.items());d=items.get(aD);a=bz
			if d is not None:
				if c.get(at)in(41674,41675):a=cn
				elif d[5]:a=cm
			a=list(a);h=c.get(I)
			if h in(7174,7170,7172):
				e,b=a.index(ag),a.index(I)
				if e<b:a.pop(b);a.insert(e,I)
			f=c.get(W)
			if f in(5069,5084,5102):
				g,b=a.index(W),a.index(I)
				if g<b:a.pop(g);a.insert(b,W)
			if f in(5136,5143):a=[I if s==W else(W if s==I else s)for s in a]
			return a,c
		def b_(gid,b):
			a,c=r["bounds"],r["order"]
			if gid not in a:c.append(gid)
			a[gid]=b
			while len(c)>cu:a.pop(c.pop(0),None)
			return b
		def cU(gid):
			g="pic"
			try:h=a8(lambda:Tex.gump_pixels(gid)if Tex.find()else None)
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
			return b_(gid,g)
		def cV(gid):
			b=r["bounds"].get(gid,"need")
			if b=="need":
				if gid not in r["need"]:r["need"].append(gid)
				b="pic"
			if b!="pic":return b
			a,c=V(gid);return(0,0,a,c)if a>0 and c>0 else None
		def cW():return bool(r["need"])
		def cX(items,who,N=None):
			v=k["g"];bX()
			if v is None or who is None:return
			w,x,y=who;p=[];k["doll"]=p;i=[];P,Q,z=cQ(w,x,y);i.append((P,Q,True,0,0))
			if z:i.append((z,x,True,0,0))
			R,T=cT(items)
			for o in R:
				A=items.get(o)
				if A is None:continue
				q,U,W,B,r,_c=A
				if cS(o,T,N):continue
				if B==0 and j.m_animid is None:continue
				l=cR(w,U,B,y)
				if l<=0 or V(l)==(0,0):continue
				i.append((l,W&16383,r,0 if o in(ah,ap,an)else q,o))
			a=b=1<<20;c=e=-(1<<20)
			for X in i:
				m=cV(X[0])
				if m is not None:a,b=min(a,m[0]),min(b,m[1]);c,e=max(c,m[2]),max(e,m[3])
			if c<=a or e<=b:a,b,c,e=0,0,bp,b8
			C=(c-a,e-b);f=d["k"];Y,Z,mw,mh=bL();D,F=Y*f+av,Z*f+av;H,s=max(1.,mw*f-2*av),max(1.,mh*f-2*av);PW=max(1.,(d["pw"]-2*E)*f-2*av);S=min(s/C[1],PW/C[0]);I=int(round(D+H/2.-S*(a+c)/2.));J=int(round(F+s/2.-S*(b+e)/2.));t=int(round((D+H/2.)/f-(a+c)/2.));u=int(round((F+s/2.)/f-(b+e)/2.));K=abs(S-1.)>.001;g=k["raw"];h=[-1]
			if j.ok and g is not None:
				try:
					aa();L=ai(k["c"].get("doll_drop"))
					if L is not None:h[0]=g.Children.IndexOf(L)+1
				except Exception:h[0]=-1
			def M(a):
				if h[0]<=0:return False
				b=g.Children;a.Parent=g
				while b.Remove(a):pass
				b.Insert(min(h[0],b.Count),a);h[0]+=1;return True
			def ab(gid,b,c,serial):
				if j.DollPiece is None or g is None or h[0]<=0:return
				try:a=j.DollPiece(g,UInt32(int(serial)),UInt16(int(gid)),UInt16(int(b)),0,0,True)
				except Exception:j.DollPiece=None;return
				try:
					a.va_gid,a.va_k,a.va_down=int(gid),float(S),False;a.HighlightOnMouseOver=False;a.IsPartialHue=bool(c);bf(a,I,J)
					if K:a.ApplyScale(S,False,True,False)
					G.AddControlOnClick(a,n(("drop",0)))
					if not M(a):raise Exception("no place")
				except Exception:safe(a.Dispose);return
				return a
			def ac(gid,c,e,serial=0):
				if serial:
					b=ab(gid,c,e,serial)
					if b is not None:p.append(b);return
				a=G.CreateGumpPic(gid,t,u,c)if c else G.CreateGumpPic(gid,t,u);a.SetPos(t,u);b=None
				try:
					aa();b=ai(a);bf(b,I,J)
					if K:b.ApplyScale(S,False,True,False)
				except Exception:b=None;aI(a)
				if e:f=ai(a);O(f if f is not None else a,"IsPartialHue",True)
				if serial:a.SetEntityTooltip(serial);aB(a,n(("drop",0)));Kit.hook_double(a,n(("use",serial)))
				else:a.SetAcceptMouseInput(False)
				d=False
				if b is not None:
					try:d=M(b)
					except Exception:d=False
				if not d:v.Add(a)
				p.append(a)
			for l,ad,r,q,ae in i:ac(l,ad,r,q)
		def cY(force=False):
			if d["minimized"]or k["g"]is None:return
			if r["redo"]and not r["need"]:r["redo"]=False;d["doll_sig"]=None
			b=time.time()
			if not force and d["sig"]is not None and d["doll_sig"]is not None and 0<=b-d["doll_at"]<ce:return
			d["doll_at"]=b;p=cA()if j.ok else None;c={};a,e=cP(p,c);f=tuple([a[h][0]if h in a else 0 for h in ck])
			if f!=d["sig"]:c_(f,p,c)
			g=(e,tuple(sorted((s,i[0],i[1],i[2])for s,i in a.items())))
			if g!=d["doll_sig"]:d["doll_sig"]=g;cX(a,e,p)
		def cZ(s,item,c):
			h=k["g"]
			if s["ctrl"]is not None:T(s["ctrl"]);s["ctrl"]=None
			if item is None and c is None:O(s["label"],"IsVisible",True);al(s["drop"],s["tip"]);return
			O(s["label"],"IsVisible",False);s["drop"].SetTooltip("")
			if j.ok and item is not None and k["raw"]is not None:
				try:
					i=(k["raw"],UInt32(int(item.Serial)),UInt16(int(item.DisplayedGraphic)),UInt16(int(item.Hue)),0,0);a=None
					if j.SlotItem is not None:
						try:a=j.SlotItem(*i)
						except Exception:j.SlotItem=None
					if a is None:a=j.ItemGump(*i)
					r=j.f_bounds.GetValue(a);l,o=int(r.Width),int(r.Height);f=min(1.,(m-6)/float(max(1,l)),(m-6)/float(max(1,o)));e=d["k"];bf(a,int(round((s["x"]+(m-l*f)/2.)*e)),int(round((s["y"]+(m-o*f)/2.)*e)))
					if abs(e*f-1.)>.001:
						try:a.ApplyScale(e*f,False,True,False)
						except Exception:aI(a,True)
					try:G.AddControlOnClick(a,n(("drop",s["layer"])))
					except Exception as g:safe(a.Dispose);raise g
					h.Add(a);s["ctrl"]=a;return
				except Exception as g:j.error="item control: %s"%g
			p=int(c.Serial)if c is not None else int(item.Serial);q=int(c.Graphic)if c is not None else int(item.DisplayedGraphic);b=G.CreateGumpItemPic(q,m-6,m-6);b.SetRect(s["x"]+3,s["y"]+3,m-6,m-6);aI(b);b.SetEntityTooltip(p);aB(b,n(("drop",s["layer"])));Kit.hook_double(b,n(("use",p)));h.Add(b);s["ctrl"]=b
		def c_(sig,p,got=None):
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
							try:a=p.FindItemByLayer(aw(s["layer"]))
							except Exception:a=None
					if a is None:c=bZ(s["name"])
				cZ(s,a,c)
			d["sig"]=sig
		def c0(layer):
			if j.ok:
				h=bd()
				if h is None:return
				c,e,a=h
				if not e:API.SysMsg(t+": that can't be worn.",u);return
				if a not in bx and a>0:API.SysMsg(t+": that doesn't go in an equipment slot.",u);return
				try:
					w=bJ();p=w.Player;b=p.FindItemByLayer(aw(a))if a else None
					if b is not None and int(b.Serial)==c:b=None
					if b is None:j.m_equip.Invoke(None,Array[Object]([w,UInt32(int(p.Serial))]))
					else:j.m_swap.Invoke(None,Array[Object]([w,UInt32(int(p.Serial)),aw(a),UInt32(int(b.Serial))]))
					d["sig"]=None
				except Exception as f:API.SysMsg(t+": couldn't equip that (%s)."%f,u)
				return
			c=aA()
			if c:API.EquipItem(c);d["sig"]=None
		c1=("Strength","Dexterity","Intelligence","Hits","HitsMax","Mana","ManaMax","Stamina","StaminaMax","Weight","WeightMax","Gold","Followers","FollowersMax","PhysicalResistance");ac=10
		def c2(g,c,px,y):h=o("Weight 0000/0000");i=o("Gold 9,999,999   Followers 99/99");a=px+10+h+6;b=d["strip_w"]or L;j=b-(a-px)-10-i-14;f=max(br,min(ca,j));bh(g,c,a,y,f,16);c["stats4"]=e(g,"",a+f+10,y,D);c["room"]=b-2*ac;c["room3"]=h;c["room4"]=max(0,b-(a+f+10-px)-ac)
		def c3(g,c,col):x,y,w,h=col;B(g,x,y,w,h);S(g,x,y,w,h,lambda*a:None,None,movable=not bg());b=max(bR,min(cH,(h-16-aK)//aJ));d=y+max(8,(h-aJ*b-aK)//2);c["scol"]=[e(g,"",x+ac,d+f*b+(aK if f>=7 else 0),D)for f in range(aJ)];c["room"]=w-2*ac;bh(g,c,x+ac,d+7*b-1,w-2*ac,16)
		def b0(e,a,f):
			if a<=0 and f>0:a=int(cc+cd*f)
			b=(float(e)/a)if a>0 else-1.
			if b>=b9:
				if d["w_armed"]and aP("character.weight","Weight %d/%d (%d%%): nearly overloaded"%(e,a,int(b*100)),level="warn",who="weight")is not False:d["w_armed"]=False
			elif b>=0:d["w_armed"]=True
			g=k["c"].get("wfills")
			if not g or d["minimized"]:return
			c=Kit.weight_level(b,k["c"]["wbar_w"])
			if c==d["wbar"]:return
			d["wbar"]=c;Kit.weight_show(g,c[0],c[1])
		def c4():
			a=time.time()
			if 0<=a-d["w_at"]<bq:return
			d["w_at"]=a
			try:p=API.Player
			except Exception:p=None
			if not p:return
			try:b,c,e=int(p.Weight),int(p.WeightMax),int(p.Strength)
			except Exception:return
			b0(b,c,e)
		def c5():
			c=k["c"]
			if d["minimized"]or("stats1"not in c and "scol"not in c):return False
			g=time.time()
			if 0<=g-d["stats_at"]<bq:return True
			d["stats_at"]=g;p=aH()
			if not p:return True
			v={};f=[]
			for h in c1:
				try:x=int(getattr(p,h))
				except Exception:x=0
				v[h]=x;f.append(x)
			a=c["room"];e=c.get("scol");i=c.get("stats1");b=d.get("stats_key")
			if b is None or b[0]!=f or b[1]is not e or b[2]is not i or b[3]!=(a,c.get("room3"),c.get("room4")):
				d["stats_key"]=(f,e,i,(a,c.get("room3"),c.get("room4")))
				if e is not None:
					for j,l in zip(e,("Str %d"%v["Strength"],"Dex %d"%v["Dexterity"],"Int %d"%v["Intelligence"],"HP %d/%d"%(v["Hits"],v["HitsMax"]),"Mana %d/%d"%(v["Mana"],v["ManaMax"]),"Stamina %d/%d"%(v["Stamina"],v["StaminaMax"]),"Weight %d/%d"%(v["Weight"],v["WeightMax"]),"Gold %s"%P(v["Gold"]),"Followers %d/%d"%(v["Followers"],v["FollowersMax"]),"AR %d"%v["PhysicalResistance"])):A(j,C(l,a))
				else:A(c["stats1"],C("Str %d   Dex %d   Int %d   AR %d"%(v["Strength"],v["Dexterity"],v["Intelligence"],v["PhysicalResistance"]),a));A(c["stats2"],C("HP %d/%d   Mana %d/%d   Stamina %d/%d"%(v["Hits"],v["HitsMax"],v["Mana"],v["ManaMax"],v["Stamina"],v["StaminaMax"]),a));A(c["stats3"],C("Weight %d/%d"%(v["Weight"],v["WeightMax"]),c["room3"]));A(c["stats4"],C("Gold %s   Followers %d/%d"%(P(v["Gold"]),v["Followers"],v["FollowersMax"]),c["room4"]))
			b0(v["Weight"],v["WeightMax"],v["Strength"]);return True
		def Q(name):return HOST.services.get(name)
		def c6(cmd):
			if cmd=="show":n("show")()
			elif cmd=="dock":n("to_bar")()
		def c7():
			c=Q("bag.attach");e=Q("bag.grid_size");a=d["attached"];f=q["combine"]and c is not None and e is not None
			if a is None:
				if not f:return
				g,h=cN();a={"g":k["g"],"raw":None,"dx":g,"dy":h,"shown":not d["minimized"],"state":bY(),"grid_wh":None,"cmd":c6};d["attached"]=a
				try:c(a)
				except Exception as i:d["attached"]=None;API.SysMsg(t+": couldn't combine with Bags (%s)."%i,u);return
				Z();return
			if not f:c8();return
			b=safe(e);b=tuple(b)if b else None
			if b!=a["grid_wh"]:a["grid_wh"]=b;Z()
		def c8():
			b,d["attached"]=d["attached"],None;aL(None);d["told_shrink"]=None
			if b is not None:
				a=Q("bag.attach")
				if a is not None:safe(lambda:a(None))
			if k["g"]is not None and not d["shutting"]:Z()
		def b1():
			a=d["attached"]
			if a is not None:a["shown"]=not d["minimized"];a["state"]=bY()
		b2={"drop":c0,"use":lambda serial:API.UseObject(serial),"follow":lambda serial:aE(serial,t)}
		def c9(w):return(("WINDOW",(("check","stats","Show your stats","Str / Dex / Int, HP, mana, stamina, weight, gold, followers: under the doll, or beside it in a zone"),("check","combine","Combine with Bags in one window","The Bags grid inside this window (unticked: two windows)"),("check","beside","Bags beside the doll (not under)","Combined: the grid beside the doll; one too tall to stack goes beside anyway"),("check","left","Bags on the left","Beside the doll: on its left (unticked: right)"),("note","Drop an item on a slot to wear it; drag it out to take it off.",{"ndy":4})),{"top":32,"sh":170}),)
		def da(a,new):
			if k["g"]is not None:n("redraw")();HOST.poke()
		aO=Kit.Page(q,c9,bG,da);bF()
		def b3():
			bF()
			if not safe(lambda:API.Player):d["wait_player"]=True;return
			d["wait_player"]=False
			if not j.tried:j.tried=True;cx()
			d.update({"shutting":False,"docked":False,"queue":[],"sig":None,"doll_sig":None,"attached":None,"beside_said":False,"fit":None,"k":1.,"py":None,"strip_w":None,"pw":L,"col":None,"ph":Y,"rp":aj,"told_bags":None,"pair":None,"pair_at":0.,"room":None,"room_fs":None,"told_shrink":None,"grew":False,"paired":False,"w_armed":True,"w_at":0.,"wbar":None,"minimized":bool(d["saved_min"]or aV(F))});aQ("character.weight","Weight near the limit",cb);Z();a=Kit.dock_hooks(t,b6,d,k,n("redraw"));a.update({"fit":cF,"exact":True,"pieces_out":True,"verify":not d["paired"]});r["hooks"]=a;aT(F,a)
			if not j.ok:API.SysMsg(t+": no client access (%s); slots show pictures and equip without swapping."%j.error,l)
		def db():
			if d["wait_player"]:
				if safe(lambda:API.Player):b3()
				return
			if k["g"]is None:return
			if X(k["store"],"close"):bH();T(k["g"]);return
			while d["queue"]:
				a=d["queue"].pop(0);g=a[0]if isinstance(a,tuple)else a
				if a=="show":d["minimized"],a=True,"toggle_min"
				if a=="redraw"and bd()is not None:d["redraw_due"]=True
				elif Kit.win_action(a,d,F,t,Z,aS):continue
				elif a in("bag_mgr","bag_traps"):
					h=Q("bag.open_manager"if a=="bag_mgr"else "bag.open_traps")
					if h is not None:h()
				elif g in b2:b2[g](a[1])
			b1();c7()
			if k["g"]is None:return
			i=bd()is not None
			if d.get("redraw_due")and not i:d["redraw_due"]=False;Z();return
			if d["attached"]is not None and not i:
				e=time.time()
				if e-d["pair_at"]>=cf or e<d["pair_at"]:
					d["pair_at"]=e;j=bO()
					if j!=d["pair"]:
						d["pair"]=j
						if d["fit"]is not None:Z();return
					c=d["room"]
					if c is not None and d["fit"]is not None and not d["minimized"]:
						b=bl();l=(c,None if b is None else(round(b[0],1),round(b[1],1),b[2],b[3],b[4],b[5]))
						if l!=d.get("room_sig"):
							d["room_sig"]=l;f=bm(c[0],c[1])
							if f is not None and(f[0]!=d["told_shrink"]or(f[1]>c[1])!=d["grew"]):Z();return
			cY()
			if not c5():c4()
		def dc():
			a=r["need"]
			if not a:return
			b=a[0]
			try:cU(b)
			except Exception:b_(b,"pic")
			a.pop(0);r["redo"]=True
		def dd():
			d["shutting"]=True;aU(F);bb(aR,k["g"]);cv();bG();b,d["attached"]=d["attached"],None
			if b is not None:
				a=Q("bag.attach")
				if a is not None:safe(lambda:a(None))
			bW();g,k["g"]=k["g"],None;k["raw"]=None;T(g)
		return{"start":b3,"tick":db,"stop":dd,"client_tick":True,"config_height":aO.height,"build_config":aO.build,"poll_config":aO.poll,"config_closed":aO.closed,"thread_tick":dc,"thread_wanted":cW}
	def bu():
		T="storage";U="Storage";aX="StorageIndex_settings";bB="StorageIndex_pos";aY="StorageIndex_min";am=300;aZ=20000;bC=60;V=(.6,2.);a_=15.;a0=1.;bD=600.;bE=20;bF=.5;bG=40;bH=6000;bI=80;an=1500;a2=5.;ao=10.;bJ=30;bK=.4;a3=3.;ag=14;aq=ag*30;aM=12;a5=40;bL={291:"Pack horse",292:"Pack llama",791:"Giant beetle"};a8=(8198,7774);bM="_storage_index_%s.txt";bN="# Virtue Assistant Storage Index 1";aN="StorageIndex_favs";a9="StorageIndex_account";aO=420;bO,bP=260,46;W=20;bQ=3708;bb="Alt+click: auto-follow (again to stop)";M=K;IW=aO-2*M;Z=M+30+v;bc=64;ar=Z+bc+v;be=12+ag*W+8;bR=ar+be+v;bf=30;at=bR+bf+M;bh=((60,1,"just now"),(3600,60,"%dm ago"),(86400,3600,"%dh ago"),(172800,86400,"%d day ago"),(0,86400,"%d days ago"));z={"bank":True,"ground":True,"pack":True,"days":bC};g=[];cz=dict(z);c={"shutting":True,"minimized":False,"docked":False,"queue":[],"active":False,"hooked":False};j={"g":None,"c":{},"store":({},{}),"rows":[]};aa={"wipe_at":0.};aP,Q,cA=ak(c,U);b={"recs":{},"tombs":{},"ver":0,"dirty":False,"dirty_at":0.,"loaded":False,"path":None,"mtime":None,"err":"","unread":False};d={"ver":-1,"keys":{},"places":{},"items":0,"chars":0,"veil":False};a={"query":"","seen_text":None,"changed_at":0.,"page":0,"rows":[],"sel":None,"naming":None,"forget_arm":(None,0.),"status":"","status_hue":l,"status_at":0.,"dirty":True,"built_for":None,"live":{},"live_at":0.,"live_ver":0,"live_sig":None,"data":[],"prev":[],"last_read":("",0.,""),"iw":IW};h={};n={"q":[],"n":0};au={"n":0};ae=[];av={};af={};R=set();ah={};G=[];aw={"key":None,"stats":[]};ax={"key":None,"by":{}};bj=re.compile(r"%[^%]*%|%s")
		def H(s):return str(s or "").replace("|","/").replace("\r"," ").replace("\n"," ").strip()
		def bS(text):
			h=0x811C9DC5
			for a in text:h=((h^ord(a))*16777619)&0xFFFFFFFF
			return "%08x"%h
		def bT(it,graphic):
			n=av.get(graphic)
			if n is None:
				try:d=it.GetItemData();n=bj.sub("",str(d.Name or "")).strip()if d is not None else ""
				except Exception:n=""
				if len(av)>3000:av.clear()
				av[graphic]=n
			return n
		def ay(it,graphic,amount):
			try:n=str(it.Name or "")
			except Exception:n=""
			if "%"in n:n=bj.sub("",n)
			n=n.strip()
			if amount>1:
				a=str(amount)
				if n.startswith(a+" "):n=n[len(a)+1:].strip()
			if not n:n=bT(it,graphic)or("item 0x%04X"%graphic)
			n=H(n);return n[:1].upper()+n[1:]
		def aA(text):
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
		def aB(a,key):
			g,b=key[0],key[2]
			for c,v in a:
				if c=="g":
					if g==v:return True
				elif v in b:return True
			return False
		bk={"days":(1,3650)}
		def bl():a6(aX,";",z,bk)
		def bU():a7(aX,";",z,("bank","ground","pack","days"),bk)
		def bV():
			b=ab(aN,"");del g[:]
			if not b:g.extend([[f,"0x%04X"%i]for f,i in sorted(a1.values())]+[["Bandages","0x0E21"]]);return
			if b=="-":return
			for d in b.split(";"):
				if "="not in d:continue
				c,a=d.split("=",1);c,a=c.strip(),a.strip()
				if a and len(g)<aM:g.append([c or a,a])
		def bm():
			if not g:N(aN,"-");return
			N(aN,";".join("%s=%s"%(f.replace(";",",").replace("=","-"),i.replace(";",","))for f,i in g))
		def bW():
			with Kit.quiet:
				Typing._find();b=Typing.prof;a=Typing._get(None,"CurrentProfile",b)if b is not None else None;c=Typing._get(a,"Username")if a is not None else None
				if c:e=Typing._get(a,"ServerName")or "";return bS(("%s|%s"%(e,c)).lower())
			try:
				d=API.PersistentVar.Account;v=str(API.GetPersistentVar(a9,"",d)or "")
				if not v:import random;v="a%07x"%random.randint(0,0xFFFFFFF);API.SavePersistentVar(a9,v,d)
				return "".join(f for f in v if f.isalnum())[:16]or "account"
			except Exception:return "account"
		def aQ(serial):return{"s":serial,"parent":0,"root":serial,"kind":"bag","cs":0,"cname":"","label":"","custom":"","facet":0,"x":0,"y":0,"seen":0.,"mob":0,"plabel":"","stub":False,"items":{}}
		def aR(text):
			b,d={},{}
			for a in text.split("\n"):
				a=a.rstrip("\r")
				if not a or a.startswith("#"):continue
				p=a.split("|")
				try:
					if p[0]=="C"and len(p)>=15:s=int(p[1]);r=aQ(s);r.update({"parent":int(p[2]),"root":int(p[3]),"kind":p[4],"cs":int(p[5]),"cname":p[6],"label":p[7],"custom":p[8],"facet":int(p[9]),"x":int(p[10]),"y":int(p[11]),"seen":float(p[12]),"mob":int(p[13]),"plabel":p[14],"stub":len(p)>15 and p[15]=="1"});b[s]=r
					elif p[0]=="I"and len(p)>=6:
						r=b.get(int(p[1]));c=int(p[4])
						if r is not None and c>0:
							e=p[5];f=(int(p[2]),int(p[3]),e.lower());g=r["items"].get(f)
							if g is None:r["items"][f]=[e,c]
							else:g[1]+=c
					elif p[0]=="D"and len(p)>=3:d[int(p[1])]=float(p[2])
				except(ValueError,IndexError):continue
			return b,d
		def bX():
			a=[bN]
			for s,r in b["recs"].items():
				a.append("C|%d|%d|%d|%s|%d|%s|%s|%s|%d|%d|%d|%d|%d|%s|%d"%(s,r["parent"],r["root"],r["kind"],r["cs"],H(r["cname"]),H(r["label"]),H(r["custom"]),r["facet"],r["x"],r["y"],int(r["seen"]),r["mob"],H(r["plabel"]),1 if r["stub"]else 0))
				for c,e in r["items"].items():a.append("I|%d|%d|%d|%d|%s"%(s,c[0],c[1],e[1],H(e[0])))
			for s,t in b["tombs"].items():a.append("D|%d|%d"%(s,int(t)))
			return "\n".join(a)+"\n"
		def aS(path):return Kit.read_merge(path)
		def bY(path,text):
			try:return bi(path,text)
			except Exception as a:b["err"]=str(a)[:60];return False
		def aD(path):return safe(lambda:os.path.getmtime(path))
		def aT(recs,tombs):
			d=False;c=b["recs"];e=time.time()-z["days"]*86400.
			for s,t in tombs.items():
				if t>b["tombs"].get(s,0.):b["tombs"][s]=t
			for s,r in recs.items():
				if r["seen"]<e:continue
				a=c.get(s)
				if a is None or r["seen"]>a["seen"]:
					if a is not None and a["custom"]and not r["custom"]:r["custom"]=a["custom"]
					c[s]=r;af.pop(s,None);d=True
				elif r["custom"]and not a["custom"]:a["custom"]=r["custom"];d=True
			for s in[f for f in c if f in b["tombs"]and c[f]["seen"]<=b["tombs"][f]]:del c[s];d=True
			return d
		def aF():
			h=time.time();c=b["recs"];j=h-z["days"]*86400.;k=h-bJ*86400.
			for s in[p for p,q in b["tombs"].items()if q<k]:del b["tombs"][s]
			if len(b["tombs"])>4*am:
				for s,l in sorted(b["tombs"].items(),key=lambda a:a[1])[:len(b["tombs"])-4*am]:del b["tombs"][s]
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
			if e>am or f>aZ:
				for i,g in sorted(a.items(),key=lambda a:a[1][0]):
					if e<=am and f<=aZ:break
					for s in g[1]:c.pop(s,None)
					e-=len(g[1]);f-=g[2];d=True
			return d
		def bn():
			a=b["path"]
			if not a:return
			c=aS(a);b["mtime"]=aD(a);b["unread"]=c is None
			if c:aT(*aR(c))
			aF();b["loaded"]=True;b["ver"]+=1
		def bo():
			a=b["path"]
			if not a:return
			c=aD(a)
			if b["unread"]or(c is not None and c!=b["mtime"]):
				d=aS(a)
				if d is None:b["err"]="couldn't read the index file";return
				b["unread"]=False;b["mtime"]=c
				if d and aT(*aR(d)):b["ver"]+=1
			if aF():b["ver"]+=1
			if bY(a,bX()):b["mtime"]=aD(a);b["dirty"]=False;b["err"]=""
		def bZ():
			d=b["path"];a=aD(d)
			if a is None or a==b["mtime"]:return
			c=aS(d)
			if c is None:return
			b["mtime"]=a;b["unread"]=False
			if c and aT(*aR(c))|aF():b["ver"]+=1
		def aG():
			b["ver"]+=1
			if not b["dirty"]:b["dirty"]=True;b["dirty_at"]=time.time()
		def aj(res):n["n"]+=1;res["n"]=n["n"];n["q"]=n["q"]+[res]
		def aU():a=au["n"];return[f for f in n["q"]if f["n"]>a]
		def bp():q=n["q"];return bool(q)and q[-1]["n"]>au["n"]
		def bq():
			for a in aU():au["n"]=a["n"];b0(a)
		def b_(it):
			a,b=it,0
			while b<12:
				c=int(a.Container or 0)
				if c==0 or c<0x40000000:break
				e=API.FindItem(c)
				if e is None:return
				a,b=e,b+1
			else:return
			d=int(a.Container or 0);h=int(a.Serial)
			if int(a.Graphic)in a8 or int(it.Graphic)in a8:return
			if d==0:
				if a.IsCorpse:return
				return("chest",a,None)if z["ground"]else None
			f=API.Player
			if f is None:return
			if d==int(f.Serial):g=int(API.Bank or 0);return("bank",a,None)if g and h==g and z["bank"]else None
			m=API.FindMobile(d);return("pack",a,m)if m is not None and bool(m.IsRenamable)and z["pack"]else None
		def br(serial,final):
			e=API.FindItem(serial)
			if e is None:return
			s=b_(e)
			if s is None:return
			l,a,h=s;m=API.Player
			if m is None:return
			t=API.ItemsInContainer(serial,True)or[];q,c=0,0;i=[]
			for x in t:
				c+=1
				if c>an:break
				try:d,j,u=int(x.Serial),x.Amount,int(x.Container);q=(q*31+d+7*int(j or 0)+13*u)&0xFFFFFFFFFFFF
				except Exception:i.append(None);continue
				i.append((d,j,u))
			v=(q,c);b2(serial,i)
			if af.get(serial)==v and serial in b["recs"]:
				if len(n["q"])<40:aj({"serial":serial,"same":True,"at":time.time()})
				return True
			E,o=int(m.Serial),str(m.Name or "");F=int(API.GetMap()or 0);f={serial:[]};w,y={},{};c=0;z=False
			for x in t:
				c+=1
				if c>an:z=True;break
				try:
					A=i[c-1]
					if A is not None:d,j,k=A;g=max(1,int(j or 1))
					else:d=int(x.Serial);k=int(x.Container);g=None
					B=int(x.Graphic);G=int(x.Hue)
					if g is None:g=max(1,int(x.Amount or 1))
					C=ay(x,B,g)
					if bool(x.IsContainer):w[d]=k;y[d]=C
				except Exception:continue
				p=f.get(k)
				if p is None:p=f[k]=[]
				p.append((B,G,g,C))
			if not f[serial]and not final and len(f)==1:return False
			H=int(a.Serial);D=ay(a,int(a.Graphic),1)
			if l=="bank":r=("Bank box (%s)"%o)if o else "Bank box"
			elif l=="chest":r="%s at %d, %d"%(D or "Chest",int(a.X),int(a.Y))
			else:I=int(h.Graphic or 0);r=("%s %s"%(bL.get(I,"Pack animal"),str(h.Name or ""))).strip()
			J={"serial":serial,"parent":int(e.Container or 0),"kind":l,"root":H,"label":r,"top_name":D,"own_name":ay(e,int(e.Graphic),1),"cs":E,"cname":o,"facet":F,"x":int(a.X),"y":int(a.Y),"mob":int(h.Serial)if h is not None else 0,"by":f,"parents":w,"names":y,"capped":z,"at":time.time()}
			if len(n["q"])<40:
				aj(J)
				if len(af)>200:af.clear()
				af[serial]=v
			return True
		def bs(recs,s,b):
			a=0
			while s and a<14:
				if s==b:return True
				r=recs.get(s)
				if r is None:return False
				s,a=r["parent"],a+1
			return False
		def b0(res):
			e=b["recs"];l=res.get("op")
			if l=="forget":cn(res["root"]);return
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
					if bs(e,s,i):r["seen"]=f;c=r["root"]
				p=d["places"].get(c)if c is not None else None
				if p is not None:p["seen"]=f;a["dirty"]=True
				return
			i,c,f=res["serial"],res["root"],res["at"]
			if i==c:k=[cB for cB,cC in e.items()if cC["root"]==c or cB==c]
			else:k=[cD for cD in e if bs(e,cD,i)]
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
				if g is None:g=e[c]=aQ(c);g["stub"]=True
				g.update(m);g["parent"]=0;g["label"]=res["label"]
				if g["stub"]:g["seen"]=max(g["seen"],f)
			for h,z in res["by"].items():
				r=aQ(h);r.update(m);r["custom"]=q.get(h,"");r["seen"]=f
				if h==c:r["parent"],r["label"]=0,res["label"]
				elif h==i:r["kind"],r["parent"],r["label"]="bag",res["parent"],res["own_name"]
				else:r["kind"],r["parent"]="bag",res["parents"].get(h,0);r["label"]=res["names"].get(h,"Bag")
				u=r["items"]
				for A,B,v,w in z:
					x=(A,B,w.lower());y=u.get(x)
					if y is None:u[x]=[w,v]
					else:y[1]+=v
				e[h]=r;b["tombs"].pop(h,None)
			b["tombs"].pop(c,None);aF();aG();a["last_read"]=(res["label"],f,res["kind"])
		def b1(*b):
			if not c["active"]:return
			for a in reversed(b):
				s=None
				try:s=int(a)
				except Exception:
					try:s=int(a.Serial)
					except Exception:s=None
				if s and s>=0x40000000:
					if len(ae)<40:ae.append(s)
					return
		def b2(root,first):
			if len(ah)>bH or len(G)>bI:
				a=set(i for i in G if i not in h)or set(G[:max(1,len(G)//2)])
				for k in[p for p,q in ah.items()if q in a]:del ah[k]
				G[:]=[s for s in G if s not in a]
			if root in G:G.remove(root)
			G.append(root)
			for f in first:
				if f is not None:ah[f[0]]=root
		def bt(*d):
			if not c["active"]or not h or len(R)>=bG:return
			for a in d:
				try:s,e=int(a.Serial),int(a.Container)
				except Exception:continue
				for k in(e,s):
					b=k if k in h else ah.get(k)
					if b is not None:R.add(b)
				return
		def b3():aL(c,"hooked",("OnOpenContainer",b1),("OnItemCreated",bt),("OnItemUpdated",bt))
		def b4(serial):
			a=time.time();w=h.get(serial)
			if w is None and len(h)>=bE:b=min(h,key=lambda k:h[k][0]);h.pop(b,None)
			h[serial]=[a,a+V[0],0]
		def b5(now):
			if not h:
				if R:R.clear()
				return
			if R:
				d=list(R);R.difference_update(d);e=now+bF
				for s in d:
					w=h.get(s)
					if w is not None and w[2]>=len(V)and w[1]>e:w[1]=e
			f=now>=c.get("check_at",0.)or c.get("check_at",0.)-now>a0
			if f:c["check_at"]=now+a0
			for a in list(h):
				w=h[a];g=False
				if f and w[2]>=len(V):
					b=API.FindItem(a);g=b is None or not bool(b.Opened)
					if b is None:h.pop(a,None);continue
				if g or now-w[0]>bD:br(a,True);h.pop(a,None);continue
				if now<w[1]and w[1]-now<=a_+1.:continue
				i=br(a,w[2]>=len(V)-1)
				if i is None:h.pop(a,None);continue
				w[2]+=1;w[1]=w[0]+V[w[2]]if w[2]<len(V)else now+a_
		def b6():
			g,f={},{};h=b["recs"];i=set();n=0
			for s,r in h.items():
				e=r["root"];p=f.get(e)
				if p is None:j=h.get(e);c=j if j is not None else r;l=c["custom"]or c["label"]or r["plabel"]or "A container";p=f[e]={"label":l,"seen":0.,"kind":c["kind"],"mob":c["mob"],"cname":c["cname"],"raw":l,"cs":c["cs"],"custom":bool(c["custom"]),"facet":c["facet"],"x":c["x"],"y":c["y"]}
				if r["seen"]>p["seen"]:p["seen"]=r["seen"]
				if r["cname"]:i.add(r["cname"])
				for m,o in r["items"].items():
					n+=1;k=g.get(m)
					if k is None:k=g[m]=[o[0],{}]
					k[1][e]=k[1].get(e,0)+o[1]
			d.update({"ver":b["ver"],"keys":g,"places":f,"items":n,"chars":len(i)});b7(f,sorted(set(q["cs"]for q in h.values()if q["cname"])));a["dirty"]=True
		def bu(label):return re.sub(r" at \d+, \d+$"," at "+aC("xy",""),label)
		def b7(places,g):
			d["veil"]=Kit.streamer
			if not Kit.streamer:return
			e=aH();f=int(e.Serial)if e is not None else 0;a=[i for i in g if i!=f]
			for p in places.values():
				b,c=p["cs"],p["cname"]
				if c:p["cname"]=aC("me",c)if b==f else "Character %d"%(a.index(b)+2 if b in a else len(a)+2)
				if p["custom"]:continue
				if p["kind"]=="bank":p["label"]=("Bank box (%s)"%p["cname"])if c else "Bank box"
				elif p["kind"]=="chest":p["label"]=bu(p["label"])
		def bv():
			b=(d["ver"],tuple(p for q,p in g))
			if aw["key"]!=b:
				c=[];i=d["keys"]
				for n,j in g:
					k=aA(j);e,a=0,{}
					for l,m in i.items():
						if aB(k,l):
							for f,h in m[1].items():a[f]=a.get(f,0)+h;e+=h
					c.append((e,a))
				aw["key"],aw["stats"]=b,c
			return aw["stats"]
		def bw(q):
			c=(d["ver"],q.lower())
			if ax["key"]!=c:
				g=aA(q);a={}
				for k,e in d["keys"].items():
					if aB(g,k):
						for f,h in e[1].items():
							b=a.get(f)
							if b is None:b=a[f]={}
							b[k]=(e[0],h)
				ax["key"],ax["by"]=c,a
			return ax["by"]
		def b8(i):
			def a(*b):a=Follow.alt_held();Q.add(("row",i,a,time.time()),dup=True,cap=20)
			return a
		def aV():
			z=O.slot if ac(T)else None;w,n=z or(aO,at);A=O.rows(W,at-ag*W,ag,4);b,p=w-2*M,n-(at-be);q=ar+p+v;a["iw"]=b;g,d,j=O.begin(bO if c["minimized"]else w,bP if c["minimized"]else n);h=[]
			if not c["minimized"]:
				O.frame(g);B(g,M,Z,b,bc);r=35+o("Add favourite");e(g,"Find:",M+10,Z+12,D);s=M+16+o("Find:");C=b-(s-M)-r-22;j["box"]=al(az(g,a["query"],s,Z+9,C,numbers=False),"Part of a name, or a graphic (0x0F88); commas for several; empty: favourites");m(g,d,"fav",ad,M+b-r-6,Z+8,"Add favourite","Add the Find box text to your favourites",on_click=Q("fav"));f=Z+36;k=M+10;m(g,d,"name",ad,k,f,"Name","Name the picked place: type it in the Find box, then click Name again",on_click=Q("name"));k+=35+o("Name")+12;m(g,d,"forget",I,k,f,"Forget","Drop the picked place and its bags from the index (click twice)",on_click=Q("forget"));E=35+o("Next");t=M+b-E-6;m(g,d,"next",J,t,f,"Next","Next page",on_click=Q("next"));u=t-12-(35+o("Prev"));m(g,d,"prev",J,u,f,"Prev","Previous page",on_click=Q("prev"));j["page"]=e(g,"",u-50,f+3,l);B(g,M,ar,b,p)
				for x in range(A):i=ar+8+x*W;y={"l":e(g,"",M+10,i,D),"r":e(g,"",M+b-60,i,l),"lx":M+10,"rx":M+b-60,"tip":"","y":i};y["c"]=S(g,M+4,i-2,b-8,W,b8(x));h.append(y)
				B(g,M,q,b,bf);j["status"]=e(g,"",M+10,q+7,l)
			a.update({"data":[None]*len(h),"prev":[(None,0.)]*len(h),"seen_text":None,"built_for":None,"dirty":True});O.end(g,{"rows":h});by(time.time())
		O=Kit.Window(T,U,c,j,aV,bB,aY,(240,160),icon=bQ,cleanup=aP,clear={"rows":[]})
		def bx():return j["g"]is not None and not c["minimized"]and not c["docked"]
		def r(text,hue=None):a["status"]=text;a["status_hue"]=l if hue is None else hue;a["status_at"]=time.time()
		def b9():
			n=len(d["places"])
			if not b["loaded"]:return "Reading the index"
			if b["err"]:return "Index file: %s"%b["err"]
			c,t,e=a["last_read"];s="%s noted"%F(n,"place")
			if Kit.streamer and e=="bank":c="Bank box (%s)"%aC("me","")
			elif Kit.streamer and e=="chest":c=bu(c)
			if d["chars"]>1:s+=" on %d characters"%d["chars"]
			if c:s+="; last read %s"%c
			return s
		def ca(p,root):
			a=""
			if p["kind"]=="chest"and not Kit.streamer:a=" (facet %d, %d, %d)"%(p["facet"],p["x"],p["y"])
			c=(" by %s"%p["cname"])if p["cname"]else "";b="%s\nSeen%s %s%s\nClick to pick it (then Name or Forget)"%(p["label"],c,Kit.ago(time.time()-p["seen"],bh),a)
			if p["mob"]:b+="\n"+bb
			return b
		def cb(now):
			b=[];B=a["live"];C=d["places"];q=a["query"]
			if not q:
				if not g:return[("No favourites yet: type a name, then click Add favourite.","",l,0,"",None)]
				b.append(("FAVOURITES  (click one to see where)","",E,0,"Totals across the account: every place noted, and your backpack now",None));G=bv()
				for H,(I,w)in enumerate(g):
					x=aA(w);i,J=G[H]if H<len(G)else(0,{});c=sum(cC[1]for cB,cC in B.items()if aB(x,cB));i+=c;r=len(J)+(1 if c else 0);s=[]
					if c:s.append("On you now: %s"%P(c))
					for e,f in sorted(J.items(),key=lambda a:-a[1])[:10]:p=C.get(e);s.append("%s: %s"%(p["label"]if p else "?",P(f)))
					t="%s (%s)\n%s\nClick to see where"%(I,w,"\n".join(s)if s else "None noted");b.append((I,("%s in %s"%(P(i),F(r,"place")))if i else "none",D,0,t,("fav",w)))
				return b
			x=aA(q);y=bw(q);c=dict((cD,(cE[0],cE[1]))for cD,cE in B.items()if aB(x,cD));r=len(y)+(1 if c else 0)
			if not r:return[("Nothing noted holds \"%s\"."%q,"",l,0,"Open the container it is in once (bank box, chest, pack animal) and it is noted",None)]
			z,j={},{}
			for e,u in y.items():
				K=0
				for A,v in u.items():K+=v[1];j[A]=v[0]
				z[e]=K
			i=sum(z.values())+sum(cF for cG,cF in c.values())
			for A,v in c.items():j[A]=v[0]
			N=list(j.values())[0]if len(j)==1 else "%d kinds"%len(j);b.append((N,"%s in %s"%(P(i),F(r,"place")),E,0,"Everything noted that matches \"%s\""%q,None));h=0
			if c:
				M=aC("me",str(safe(lambda:API.Player.Name,"")or ""));b.append(("Backpack%s"%((" (%s)"%M)if M else ""),"on you now",E,0,"Your backpack and the bags in it, right now",None));k=sorted(c.items(),key=lambda a:-a[1][1]);m=max(0,aq-len(b));h+=max(0,len(k)-m)
				for n,(o,f)in k[:m]:b.append((o,P(f),D,14,"%s x%s on you (graphic 0x%04X, hue %d)"%(o,P(f),n[0],n[1]),None))
			O=sorted(y.items(),key=lambda a:-z[a[0]])
			for e,u in O:
				p=C.get(e)
				if p is None:continue
				if len(b)>=aq:h+=1+len(u);continue
				Q=L if a["sel"]==e else E;b.append((p["label"],"seen %s"%Kit.ago(now-p["seen"],bh),Q,0,ca(p,e),("place",e,p["mob"],True)));R=("place",e,p["mob"],False);k=sorted(u.items(),key=lambda a:-a[1][1]);m=max(0,aq-len(b));h+=max(0,len(k)-m)
				for n,(o,f)in k[:m]:
					t="%s x%s in %s (graphic 0x%04X, hue %d)\nClick to pick this place"%(o,P(f),p["label"],n[0],n[1])
					if p["mob"]:t+="\n"+bb
					b.append((o,P(f),D,14,t,R))
			if h:b.append(("%s more line%s: type more of the name"%(P(h),""if h==1 else "s"),"",l,0,"A search lists %d lines at most; the total above counts them all"%aq,None))
			return b
		def by(now):
			m=j["g"]
			if m is None or c["docked"]:return
			i=j["c"]
			if c["minimized"]:n=len(d["places"]);a["status_key"]=None;A(i.get("status"),U+": "+("%s noted"%F(n,"place")if b["loaded"]else "reading the index"),l);return
			e=(a["query"],d["ver"],a["live_ver"],a["sel"],a["page"],int(now//30))
			if a["dirty"]or e!=a["built_for"]:
				a["dirty"]=False;a["built_for"]=e;a["rows"]=cb(now);f=bz()
				if a["page"]>=f:a["page"]=f-1;a["built_for"]=(e[0],e[1],e[2],e[3],a["page"],e[5])
				cc(now,f)
			if(a["status"]and a["naming"]is None and not 0<=now-a["status_at"]<=8.):a["status"]=""
			g=i.get("status");k=(g,a["status"],a["status_hue"],b["loaded"],b["err"],len(d["places"]),d["chars"],a["last_read"]);h=a.get("status_key")
			if h is not None and h[0]is g and h[1:]==k[1:]:return
			a["status_key"]=k;A(g,C(a["status"]or b9(),a["iw"]-20),a["status_hue"]if a["status"]else l)
		def cc(now,pages):
			k=j["rows"];s=a["page"]*len(k);e,t=a["data"],a["prev"];m=M+a["iw"]-10
			for i,r in enumerate(k):
				n=s+i
				if n<len(a["rows"]):f,b,o,p,c,g=a["rows"][n]
				else:f,b,o,p,c,g="","",D,0,"",None
				q=bd(b)if b else 0;d=M+10+p;u=m-d-(q+8 if b else 0);A(r["l"],C(f,u)if f else "",o);A(r["r"],b,l)
				if d!=r["lx"]:r["lx"]=d;bg(r["l"],d,r["y"])
				h=m-q
				if b and h!=r["rx"]:r["rx"]=h;bg(r["r"],h,r["y"])
				if c!=r["tip"]:r["tip"]=c;r["c"].SetTooltip(c)
				if g!=e[i]:t[i]=(e[i],now);e[i]=g
			v=j["c"];A(v.get("page"),"%d / %d"%(a["page"]+1,pages)if pages>1 else "",l)
		def cd(now):
			b=j["c"].get("box")
			if b is None:return
			t=str(b.Text or "")
			if t!=a["seen_text"]:
				if a["seen_text"]is not None:a["changed_at"]=now
				a["seen_text"]=t;return
			if a["changed_at"]and(now-a["changed_at"]>=bK or now<a["changed_at"]):
				a["changed_at"]=0.
				if a["naming"]is not None:return
				q=t.strip()
				if q.lower()!=a["query"].lower():a["query"]=q;a["page"]=0;a["dirty"]=True
		def aI(text):
			b=j["c"].get("box");a["seen_text"]=text;a["changed_at"]=0.
			if b is not None:b.SetText(text)
		def ce(now):
			if not bx():return
			if now<a["live_at"]and a["live_at"]-now<=a3:return
			a["live_at"]=now+a3;b={};c=ap(True,1.);q,n=0,0
			for x in c:
				n+=1
				if n>an:break
				try:q=(q*31+int(x.Serial)+7*int(x.Amount or 0)+13*int(x.Container))&0xFFFFFFFFFFFF
				except Exception:continue
			if(q,n)==a["live_sig"]:return
			a["live_sig"]=(q,n)
			if c:
				n=0
				for x in c:
					n+=1
					if n>an:break
					try:g,h=int(x.Graphic),int(x.Hue);d=max(1,int(x.Amount or 1));e=ay(x,g,d)
					except Exception:continue
					k=(g,h,e.lower());f=b.get(k)
					if f is None:b[k]=[e,d]
					else:f[1]+=d
			if b!=a["live"]:a["live"]=b;a["live_ver"]+=1
		def cf(i,t):
			if i>=len(a["data"]):return
			c,b=a["prev"][i];return c if b and(b>=t or t-b<.15)else a["data"][i]
		def aW():
			if a["naming"]is not None:a["naming"]=None;aI(a["query"])
		def cg(action,now):
			if c["minimized"]or c["docked"]:c["minimized"]=c["docked"]=False;HOST.dock_forget(T);ba(aY,False);aV()
			safe(lambda:ai(j["g"]).BringOnTop())
		def ch(action,now):aE(action[1],U)
		def ci(action,now):
			e,i,c,t=action;b=cf(i,t)
			if b is None:return
			if c:
				if len(b)>2 and b[2]:aE(b[2],U)
				return
			aW()
			if b[0]=="fav":a["query"]=b[1];a["page"]=0;aI(b[1]);r("")
			elif b[0]=="place":a["sel"]=None if(b[3]and a["sel"]==b[1])else b[1];p=d["places"].get(a["sel"])if a["sel"]else None;r(("Picked: %s"%p["label"])if p else "")
			a["dirty"]=True
		def cj(action,now):
			aW();q=a["query"]or(a["seen_text"]or "").strip()
			if not q:r("Type what to look for first (a name, or a graphic like 0x0F88).",u)
			elif any(f.lower()==q.lower()for i,f in g):r("\"%s\" is already a favourite."%q)
			elif len(g)>=aM:r("%d favourites at most: take one off on the settings page."%aM,u)
			else:g.append([H(q)[:a5],H(q)]);bm();Y(T);r("Added \"%s\" to the favourites."%q,L)
			a["dirty"]=True
		def ck(action,now):
			c=a["sel"];p=d["places"].get(c)if c else None
			if a["naming"]is not None:
				f=a["naming"];e=H(a["seen_text"]or "")[:a5];g=b["recs"].get(f);a["naming"]=None
				if g is not None:aj({"op":"name","root":f,"text":e});r(("Named it \"%s\"."%e)if e else "Its own name is back.",L)
				aI(a["query"])
			elif p is None or c not in b["recs"]:r("Click a place in the list first, then Name.",u)
			else:a["naming"]=c;aI(p.get("raw",p["label"]));r("Type its new name in the Find box, then click Name again (empty: its own name).",E)
		def cl(action,now):
			aW();b=a["sel"];p=d["places"].get(b)if b else None;c,e=a["forget_arm"]
			if p is None:r("Click a place in the list first, then Forget.",u)
			elif c==b and 0<=now-e<=4.:a["forget_arm"]=(None,0.);aj({"op":"forget","root":b});a["sel"]=None;r("Forgot %s."%p["label"],L)
			else:a["forget_arm"]=(b,now);r("Click Forget again to forget %s (and the bags in it)."%p["label"],E)
		def bz():b=max(1,len(j["rows"]));return max(1,(len(a["rows"])+b-1)//b)
		def bA(action,now):b=bz();a["page"]=max(0,min(b-1,a["page"]+(1 if action=="next"else-1)));a["dirty"]=True
		cm={"show":cg,"follow":ch,"row":ci,"fav":cj,"name":ck,"forget":cl,"next":bA,"prev":bA}
		def cn(root):
			a=b["recs"];c=time.time()
			for s in[f for f,i in a.items()if i["root"]==root or f==root]:del a[s];b["tombs"][s]=c
			aG()
		def co():return 32+max(1,len(g))*24+8
		def cp(f,x,y):
			if not g:e(f.g,"No favourites yet: type a name in the Find box, then click Add favourite.",x+12,y+2,l)
			for i,(b,c)in enumerate(g):a=y+i*24;m(f.g,f.store,"rm%d"%i,I,x+12,a,None,"Take %s off the favourites"%b);e(f.g,C(b,170),x+48,a+3,D);e(f.g,C(c,f.w-240),x+226,a+3,l)
		def cq(f,x,y):aa["wipe_at"]=0.;f.c["wipe_lbl"]=m(f.g,f.store,"wipe",I,x+12,y,"Forget everything","Empty the whole index, every character (click twice)")
		def cr(w):n,a=len(d["places"]),len(b["recs"]);c=os.path.basename(b["path"])if b["path"]else "(not known yet)";return(("WHAT IT NOTES  (when you open a container)",(("check","bank","Bank boxes (and the bags in them)","Note your bank box and its bags"),("check","ground","Chests and containers on the ground (in houses too)","Note chests and containers on the ground"),("check","pack","Your pack animals' packs","Note your pack horse, llama or beetle",{"h":23}),("num","days","Forget places not seen for:","Days a place stays after it was last opened (1-3650)","days",1,3650,{"lgap":6,"fw":44})),{"ch":24,"sh":134}),("FAVOURITES  (shown when the Find box is empty)",(("custom",0,cp),),{"sh":co()}),("THE INDEX  (every character of the account)",(("note",C("%s, %s, %s, %s"%(F(n,"place"),F(a,"container"),F(d["items"],"item line"),F(d["chars"],"character")),w-24),{"hue":D}),("note",C("File: %s, in VirtueAssistantSettings"%c,w-24),{"h":14}),("custom",0,cq)),{"sh":92}))
		def cs(f,new):d=Kit.read_int(f.c["days"],0);new["days"]=min(3650,d)if d>=1 else z["days"]
		def ct(f):
			b,c=f.store,f.c
			for i in range(len(g)):
				if X(b,"rm%d"%i):del g[i];bm();a["dirty"]=True;Y(T);return
			d=aa["wipe_at"]
			if d and not 0<=time.time()-d<=4.:aa["wipe_at"]=0.;A(c.get("wipe_lbl"),"Forget everything",D)
			if X(b,"wipe"):
				e=time.time()
				if 0<=e-aa["wipe_at"]<=4.:aa["wipe_at"]=0.;aj({"op":"wipe"});af.clear();a["sel"]=None;API.SysMsg("%s: the index is empty."%U,L);Y(T)
				else:aa["wipe_at"]=e;A(c.get("wipe_lbl"),"Click again to empty it",u)
		aJ=Kit.Page(z,cr,bU,adjust=cs,clicks=ct)
		def cu():c.update({"shutting":False,"docked":False,"queue":[],"active":True,"check_at":0.,"merge_at":0.,"minimized":O.start_min()});bl();bV();h.clear();n["q"]=aU();del ae[:];a.update({"sel":None,"naming":None,"status":"","page":0,"dirty":True});b["path"]=a4(bM%bW());b3();aV();O.dock(fit=True,min=(aO,at-(ag-4)*W));aP.service("storage.show",Q("show"))
		def cv():
			if j["g"]is None:return
			if aK(j):return
			a=time.time()
			if n["q"]and n["q"][0]["n"]<=au["n"]:n["q"]=aU()
			while ae:b4(ae.pop(0))
			b5(a)
			while c["queue"]:
				b=c["queue"].pop(0)
				if not O.action(b):
					d=cm.get(b[0]if isinstance(b,tuple)else b)
					if d is not None:d(b,a)
				if j["g"]is None:return
			if bx():cd(a);ce(a)
			by(a)
		def cw():
			if c["shutting"]:return
			if not b["loaded"]:
				try:bn()
				except Exception as f:b["loaded"],b["err"]=True,str(f)[:60]
			bq();e=time.time()
			if b["dirty"]and(e-b["dirty_at"]>=a2 or e<b["dirty_at"]):bo();c["merge_at"]=e+ao
			elif e>=c["merge_at"]or c["merge_at"]-e>ao:c["merge_at"]=e+ao;bZ()
			if d["ver"]!=b["ver"]or d["veil"]!=Kit.streamer:
				b6();bv()
				if a["query"]:bw(a["query"])
		def cx():
			if c["shutting"]:return False
			if not b["loaded"]or bp()or d["ver"]!=b["ver"]or d["veil"]!=Kit.streamer:return True
			a=time.time()
			if b["dirty"]and(a-b["dirty_at"]>=a2 or a<b["dirty_at"]):return True
			return a>=c["merge_at"]or c["merge_at"]-a>ao
		bl()
		def cy():
			c["shutting"]=True;c["active"]=False
			if bp()or b["dirty"]:
				with Kit.quiet:
					if not b["loaded"]:bn()
					bq();bo()
			h.clear();del ae[:];aP.close()
		return{"start":cu,"tick":cv,"stop":cy,"client_tick":True,"config_height":aJ.height,"build_config":aJ.build,"poll_config":aJ.poll,"config_closed":aJ.closed,"thread_tick":cw,"thread_wanted":cx}
	def bv():
		O="restock";U="Restock";ar="Restock_settings";aZ="Restock_pos";a_="Restock_min";at="Restock_targets";av=400;a0,a1=240,46;a2=3705;P=22;ae=20;a3=12;a4=(4014,4016,4015);f=.7;a6=3.;V=10.;a7=3;a8=3;Q=V;aw=3.;ax=2;a9=0;af=60000;ba=1.;bb=.25;bc=20.;bd=("cannot hold more",);be=("must wait to perform another action",);bf=("can not pick that up","cannot pick that up","that is too far away","that is out of sight","does not belong to you","already holding an item");bg={"REAGENTS":.1,"POTIONS":1.,"SCROLLS":1.,"OTHER":.1};ay=(40.,3.5);az="restock.stopped";bh=74;bi=8198;q=tuple(bQ[0]for bQ in an);z=dict((bR[0],bR)for bR in an);aB=dict((bS[3],bS[0])for bS in an);bk=("last","bank","pick");aC=(("last","Last opened","Take from the container you opened last"),("bank","Bank box","Take from your bank box (say \"bank\" near a banker to open it)"),("pick","Pick...","Target a chest to take from; remembered, opened once if closed"));aD=(("pack","Backpack","Restock into your backpack"),("bag","Pick bag...","Target a bag in your backpack to restock into"));b={"deep":True,"src_deep":True,"src":"last","src_serial":0,"dest":0};j={};bP=dict(b);a={"shutting":False,"minimized":False,"docked":False,"queue":[],"run":None,"halt":False,"status":("Idle",l),"last_open":0,"opened":[],"page":0,"count_at":0.,"short":{},"layout":None,"hooked":False,"active":False,"redraw":False,"shown_moved":0,"sent_at":0.,"flight":[]};k={"g":None,"c":{},"store":({},{}),"rows":[],"tips":{}};ag,s,h=ak(a,U)
		def bl():pass
		def aE():
			b.update({"deep":True,"src_deep":True,"src":"last","src_serial":0,"dest":0})
			for a in ab(ar).split(";"):
				if "="not in a:continue
				k,v=[c.strip()for c in a.split("=",1)]
				if k in("deep","src_deep"):b[k]=v=="1"
				elif k=="src"and v in bk:b["src"]=v
				elif k in("src_serial","dest"):
					try:b[k]=max(0,int(v))
					except ValueError:pass
			j.clear()
			for a in ab(at).split(","):
				if "="not in a:continue
				k,v=[g.strip()for g in a.split("=",1)]
				if k in z and v.isdigit():
					n=min(af,int(v))
					if n>0:j[k]=n
		def R():N(ar,"deep=%d;src_deep=%d;src=%s;src_serial=%d;dest=%d"%(b["deep"],b["src_deep"],b["src"],b["src_serial"],b["dest"]))
		def d(obj,a,default=0):
			try:v=getattr(obj,a);return default if v is None else int(v)
			except Exception:return default
		def aF(c):return not c or c==0xFFFFFFFF
		aG=Kit.top_of;W=a5
		def X():return int(API.Backpack or 0)
		def ah():return int(API.Bank or 0)
		def aJ(it,fallback="container"):
			try:n=str(it.Name or "").strip()
			except Exception:n=""
			return n or fallback
		def G(serial,deep):
			try:return list(API.ItemsInContainer(int(serial),bool(deep))or[])
			except Exception:return[]
		ai=aA
		def aM():return bool(aR(O)or API.HasTarget())
		def aN():d=b["dest"];return d if d else X()
		def aj(dest,deep=None,max_age=0.):
			d=X()
			if not d:return{}
			if b["deep"]if deep is None else deep:a=ap(True,max_age)
			else:
				a=ap(False,max_age)
				if dest and dest!=d:a=a+G(dest,False)
			c={}
			for e in a:
				try:
					k=aB.get(int(e.Graphic))
					if k is None:continue
					c[k]=c.get(k,0)+max(1,int(e.Amount or 1))
				except Exception:continue
			return c
		def bm(src,deep):
			b={}
			for a in G(src,deep):
				try:
					k=aB.get(int(a.Graphic))
					if k is None:continue
					b.setdefault(k,[]).append((max(1,int(a.Amount or 1)),int(a.Serial)))
				except Exception:continue
			return b
		def bn():
			try:
				p=API.Player;w=float(p.Weight or 0);a=float(p.WeightMax or 0)
				if a<=0:a=ay[0]+ay[1]*float(p.Strength or 0)
				return None if a<=0 else a-a9-w
			except Exception:return
		def aO():
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
				return s,al(c),None
			s=a["last_open"];c=API.FindItem(s)if s else None
			if c is None:return 0,"Last opened: none yet","open a chest or your bank box first"
			return s,"Last opened: "+al(c),None
		def al(it):
			if int(it.Serial)==ah():return "your bank box"
			a=aJ(it)
			if d(it,"OnGround")or aF(d(it,"Container")):return "%s at %d, %d"%(a,d(it,"X"),d(it,"Y"))
			return a
		def aS():
			d=b["dest"]
			if not d:return "Your backpack",None
			a=API.FindItem(d)
			if a is None or not W(d):return "The picked bag (not in your backpack)","the bag you picked isn't in your backpack: pick it again or choose Backpack"
			return aJ(a,"bag")+" in your backpack",None
		def am(serial):
			if not serial:return "nothing was targeted"
			a=API.FindItem(serial)
			if a is None:return "that isn't an item"
			b,c=aG(serial);t=API.FindItem(b)if b!=int(serial)else a
			for x in(a,t):
				if x is not None and(d(x,"Graphic")==bi or d(x,"IsCorpse")):return "a corpse (or a bag in one) isn't a source"
			if W(serial):return "that is in your backpack"
			return "that isn't a container"if not(d(a,"IsContainer")or G(serial,False))else None
		def aT(src):
			c=API.FindItem(src)
			if c is None:return "the source is out of view"
			e,a=aG(src)
			if a:
				p=API.Player
				if a==d(p,"Serial"):return
				m=API.FindMobile(a)
				if m is None or not d(m,"IsRenamable"):return "the source is on someone else"
				b=max(abs(d(m,"X")-d(p,"X")),abs(d(m,"Y")-d(p,"Y")));return "your pack animal is out of reach (step next to it)"if b>ax else None
			t=API.FindItem(e)
			if t is None:return
			try:p=API.Player;b=max(abs(d(t,"X")-d(p,"X")),abs(d(t,"Y")-d(p,"Y")))
			except Exception:return
			return "the source is out of reach (step next to it)"if b>ax else None
		def bo(*c):
			if not a["active"]:return
			for b in c:
				try:s=int(b.Serial or 0)
				except AttributeError:
					try:s=int(b or 0)
					except Exception:s=0
				except Exception:s=0
				if s:a["opened"].append(s);del a["opened"][:-8];return
		def bp():aL(a,"hooked",("OnOpenContainer",bo))
		def bq():
			while a["opened"]:
				s=a["opened"].pop(0)
				if am(s)is None:a["last_open"]=s
		def i(text,hue=None):
			a["status"]=(text,l if hue is None else hue);b=k["c"].get("status")
			if b is not None:
				if a["minimized"]:text=U+": "+text[:1].lower()+text[1:]
				A(b,C(text,k["c"].get("status_w",200)),a["status"][1])
		def br():
			if a["run"]is not None:h("already restocking; press Stop first.",u);return
			k=[n for n in q if j.get(n,0)>0]
			if not k:h("the list is empty: set how many of each item to carry on the settings page.",u);aX(O);return
			e,m,c=aO()
			if c is None:c=am(e)or aT(e)
			if c is None:
				l=aN();c=None if l else "you have no backpack"
				if c is None:c=aS()[1]
			if c is None and aM():c="a target cursor is up"
			if c is None and ai():c="you are holding an item"
			if c is None and d(API.Player,"IsDead"):c="you are dead"
			if c is not None:h("can't restock: %s."%c,u);i("Can't: "+c,u);return
			g=time.time();r={"src":e,"dest":l,"deep":b["deep"],"src_deep":b["src_deep"],"phase":"go","open_until":0.,"move":None,"check":None,"at":g,"hold":0.,"sent_at":0.,"last":0,"left":False,"c0":0,"moved":0,"moves":0,"refused":0,"streak":0,"waits":0,"why":None,"bad":set(),"limbo":[w for w in a["flight"]if 0<=w[2]-g<=Q]}
			if 0<=g-a["sent_at"]<f:r["at"]=a["sent_at"]+f
			a.update({"flight":[],"short":{},"halt":False})
			if not G(e,False):
				if e==ah():h("your bank box isn't open: say \"bank\" near a banker first.",u);i("Bank box not open",u);return
				API.UseObject(e);r.update({"phase":"open","open_until":g+aw});i("Opening the chest")
			else:i("Restocking")
			a["run"]=r;h("restocking %s."%F(len(k),"item"));T()
		def bs(r,key,now):
			n=0;a=[]
			for e in r["limbo"]:
				if 0<=e[2]-now<=Q:
					a.append(e)
					if e[0]==key:n+=e[1]
			r["limbo"]=a;return n
		def bt(now):
			r=a["run"]
			if r is None or r["move"]is not None:return
			if r["check"]is not None and not r["left"]:
				b=API.FindItem(r["check"][1])
				if b is None or d(b,"Container")!=r["c0"]:r["left"]=True
			if r["why"]:p(r["why"]);return
			if r["phase"]=="open":
				if G(r["src"],False):r["phase"]="go";i("Restocking")
				elif not 0<=r["open_until"]-now<=aw:p("the chest didn't open (or it is empty)")
				return
			if r["check"]is not None:
				if 0<r["at"]-now<=f or not bv(r,now):return
			if 0<r["hold"]-now<=f or 0<r["at"]-now<=f:return
			if aM():p("a target cursor is up");return
			h=ai()
			if h and not(h==r["last"]and 0<=now-r["sent_at"]<2*f):p("you picked something up");return
			if d(aH(),"IsDead"):p("you died");return
			c=aT(r["src"])
			if c:p(c);return
			bu(r,now)
		def bu(r,now):
			g=aj(r["dest"],r["deep"]);u=bm(r["src"],r["src_deep"]);h=False
			for b in q:
				t=j.get(b,0)
				if t<=0:continue
				k=bs(r,b,now);e=t-g.get(b,0)-k
				if e<=0:
					if k:h=True
					a["short"].pop(b,None);continue
				l=[w for w in u.get(b,())if w[1]not in r["bad"]]
				if not l:a["short"][b]=e;continue
				v,m=max(l);c=min(v,e);n=bn()
				if n is not None:
					o=int(n/bg.get(z[b][1],1.)+1e-6)
					if o<1:p("you are at your weight limit");return
					c=min(c,o)
				a["short"].pop(b,None);s=API.FindItem(m);r["c0"]=d(s,"Container")if s is not None else 0;r["move"]=(b,m,c,g.get(b,0));i("Moving %d %s (%d moved)"%(c,z[b][2],r["moved"]));return
			if h:i("Waiting for the server");r["hold"]=now+f;return
			by()
		def bv(r,now):
			b,c,a,j=r["check"];e=r["sent_at"]
			if aq(e,bd)is not None:p("your %s can't hold more"%("backpack"if r["dest"]==X()else "bag"));return False
			k=aj(r["dest"],r["deep"]).get(b,0);l=now-e;g=API.FindItem(c);m=d(g,"Container")if g is not None else 0;h=k>j
			if not h and g is not None and not aF(m)and m!=r["c0"]:
				h=W(c)
				if h:k=j+a
			if h:
				n=min(k-j,a);r["moved"]+=n
				if n<a:r["limbo"].append([b,a-n,now+Q])
				r.update({"check":None,"left":False,"streak":0,"waits":0});return True
			o=g is not None and m==r["c0"]
			if not o or ai()==c:
				r["left"]=True
				if not 0<=l<V:p("the server hasn't answered a move for %d s"%int(V));return False
				if l>=2*f:i("Waiting for the server")
				r["at"]=now+f*.5;return False
			if aq(e,be)is not None and r["waits"]<a8:
				r["waits"]+=1
				if not r["left"]:r["limbo"].append([b,a,now+Q])
				r.update({"check":None,"left":False,"hold":now+f});return False
			q=aq(e,bf)is not None
			if not(q or r["left"])and 0<=l<a6:r["at"]=now+f*.5;return False
			if not r["left"]:r["limbo"].append([b,a,now+Q])
			r.update({"check":None,"left":False,"waits":0});r["refused"]+=1;r["streak"]+=1;r["bad"].add(c)
			if r["streak"]>=a7:p("%d moves in a row were refused"%r["streak"]);return False
			return True
		def bw():
			r=a["run"]
			if r is None or r["move"]is None:return
			b=r["move"];r["move"]=None
			if a["halt"]or a["shutting"]:return
			try:API.MoveItem(b[1],r["dest"],b[2])
			except Exception as c:r["why"]="a move failed (%s)"%c;return
			aW();r.update({"check":b,"left":False,"last":b[1]});r["sent_at"]=a["sent_at"]=time.time();r["at"]=r["sent_at"]+f;r["moves"]+=1
		def bx():
			if not a["short"]:return ""
			b=["%s %d"%(z[c][2],g)for c,g in sorted(a["short"].items(),key=lambda a:q.index(a[0]))];return "; short (none left in the source): "+", ".join(b[:6])+(" and %d more"%(len(b)-6)if len(b)>6 else "")
		def ao(r):
			if r is None:return
			b=[list(g)for g in r["limbo"]]
			if r["check"]is not None:c,e,d,f=r["check"];b.append([c,d,r["sent_at"]+V])
			if b:a["flight"]=(a["flight"]+b)[-20:]
		def by():
			r,a["run"]=a["run"],None
			if r is None:return
			ao(r);b=("done: %d moved in %s"%(r["moved"],F(r["moves"],"move")))
			if r["refused"]:b+=", %d refused"%r["refused"]
			h(b+bx()+".",u if a["short"]or r["refused"]else L);i("Done: %d moved%s"%(r["moved"],", some short"if a["short"]else ""),E if a["short"]else L);a["count_at"]=0.;T()
		def p(why=None,user=False):
			r,a["run"]=a["run"],None;a["halt"]=True
			if r is None:return
			ao(r)
			if user:h("stopped (%d moved)."%r["moved"]);i("Stopped (%d moved)"%r["moved"])
			else:
				b="%s (%d moved)"%(why or "stopped",r["moved"])
				if not aP(az,"Stopped: "+b,"warn"):h("stopped: "+b+".",u)
				i("Stopped: "+(why or ""),u)
			a["count_at"]=0.;T()
		def bz():a["halt"]=True;s("stop")()
		def bA():return[c for c in q if j.get(c,0)>0]
		Y=2*K+30+3*v+136+64
		def Z():d=bA();b=t.rows(P,Y+ad(0)-2*P,a3,2);e=max(1,(len(d)+b-1)//b);c=min(a["page"],e-1);return(a["minimized"],a["docked"],c,e,tuple(d[c*b:(c+1)*b]))
		def aa():
			d=Z();a["page"]=d[2];a["layout"]=d;H=a["minimized"];L=t.slot if ac(O)else None;A,N=(a0,a1)if H else(L or(av,Y+ad(len(d[4]))));g,q,j=t.begin(A,N);c=K;Q=[]
			if H:j["status_w"]=A-90
			else:
				k=A-2*c;t.frame(g);n=c+30+v;B(g,c,n,k,136,"FROM AND TO");e(g,"From:",c+12,n+30,l);F=c+12+max(o("From:"),o("Into:"))+10;j["src"]=e(g,"",F,n+30);j["src_w"]=k-(F-c)-8;r=c+12
				for h,u,w in aC:j["m_"+h]=m(g,q,"m_"+h,J,r,n+52,u,w,E if b["src"]==h else D,on_click=s(("src",h)));r+=35+o(u)+14
				e(g,"Into:",c+12,n+84,l);j["dest"]=e(g,"",F,n+84);r=c+12
				for h,u,w in aD:j["d_"+h]=m(g,q,"d_"+h,J,r,n+106,u,w,E if(h=="bag")==bool(b["dest"])else D,on_click=s(("dest",h)));r+=35+o(u)+14
				p=n+136+v;R=N-Y if L else ad(len(d[4]));B(g,c,p,k,R,"LIST  (carried / to carry)")
				if d[3]>1:G=c+k-12-21;m(g,q,"next",M,G,p+4,None,"Next page",on_click=s(("page",1)));e(g,"%d/%d"%(d[2]+1,d[3]),G-8-o("%d/%d"%(d[3],d[3])),p+6,l);m(g,q,"prev",a4,G-16-o("%d/%d"%(d[3],d[3]))-21,p+4,None,"Previous page",on_click=s(("page",-1)))
				if not d[4]:e(g,"The list is empty: set how many to carry",c+12,p+30,l);e(g,"on the "+U+" settings page.",c+12,p+50,l)
				T=c+k-100
				for X,V in enumerate(d[4]):x=p+28+X*P;af,ag,W,aa=z[V];bj(g,aa,0,c+12,x,ae);e(g,C(W,T-(c+12+ae+6)-8),c+12+ae+6,x+2);ab=e(g,"",T,x+2);w=S(g,c+8,x,k-16,P,bl,W);Q.append({"key":V,"count":ab,"tip":w})
				y=p+R+v;B(g,c,y,k,64);m(g,q,"go",M,c+12,y+8,"Restock","Top each item up to its target from the source (one move every %.1f s)"%f,on_click=s("go"));sx=c+12+35+o("Restock")+18;m(g,q,"stop",I,sx,y+8,"Stop","Stop moving items",on_click=bz);j["status"]=e(g,"",c+12,y+40,a["status"][1]);j["status_w"]=k-24
			t.end(g,{"rows":Q,"tips":{}});i(*a["status"]);a["count_at"]=0.;aU(time.time())
		t=Kit.Window(O,U,a,k,aa,aZ,a_,(240,220),icon=a2,cleanup=ag,clear={"c":{},"rows":[]})
		def ad(n):return 30+max(2,n)*P+6
		def T():
			e=k["c"]
			for a,d,f in aC:
				c=e.get("m_"+a)
				if c is not None:A(c,d,E if b["src"]==a else D)
			for a,d,f in aD:
				c=e.get("d_"+a)
				if c is not None:A(c,d,E if(a=="bag")==bool(b["dest"])else D)
		def aU(now):
			h=k["g"]
			if h is None or a["minimized"]:return
			if 0<=now-a["count_at"]<ba:return
			a["count_at"]=now;c=k["c"];q,i,r=aO();A(c["src"],C(i,c["src_w"]));l,m=aS();A(c["dest"],C(l,c["src_w"]),u if m else D)
			if not k["rows"]:return
			o=aj(aN(),None,0. if a["run"]is not None else.5);e=k["tips"]
			for d in k["rows"]:
				b=d["key"];n,t=o.get(b,0),j.get(b,0);p=L if n>=t else(u if n==0 else E);A(d["count"],"%d / %d"%(n,t),p);f=(n,t,a["short"].get(b))
				if e.get(b)==f:continue
				g="%s: %d in your pack, target %d"%(z[b][2],n,t)
				if b in a["short"]:g+=" (short by %d: none left in the source)"%a["short"][b]
				e[b]=f;d["tip"].SetTooltip(g)
		def bB(what):
			if a["run"]is not None:h("press Stop first.",u);return
			h("target the chest to take from."if what=="src"else "target a bag in your backpack.")
			def b(serial):s(("picked",what,int(serial or 0)))()
			aI(bc,b,O)
		def bC(what,serial):
			if not serial:return
			if what=="src":
				e=am(serial)
				if e:h("not a source: %s."%e,u);return
				b["src"],b["src_serial"]="pick",serial;R();c=API.FindItem(serial);h("taking from %s."%(al(c)if c is not None else "it"),L)
			else:
				f=X()
				if serial==f:b["dest"]=0
				else:
					c=API.FindItem(serial)
					if c is None or not W(serial)or not(d(c,"IsContainer")or G(serial,False)):h("pick a bag that is in your backpack.",u);return
					b["dest"]=serial
				R()
			a["count_at"]=0.;T()
		def aV(grp):return[c for c in an if c[1]==grp]
		def bD(grp):n=len(aV(grp));return 30+((n+1)//2)*26+6
		def bE(action):
			if a["run"]is not None:p(user=True)
		def aY(action):
			c=action[0]
			if a["run"]is not None:h("press Stop first.",u)
			elif action[1]==("pick"if c=="src"else "bag"):bB(c)
			else:b[c]=action[1]if c=="src"else 0;R();a["count_at"]=0.;T()
		def bF(action):b=Z()[3];a["page"]=(a["page"]+action[1])%b;aa()
		bG={"go":lambda action:br(),"stop":bE,"src":aY,"dest":aY,"picked":lambda action:bC(action[1],action[2]),"page":bF};bH=30+2*28+24+8
		def bI(w):a=(w-24)//2;return[("%s  (%s)"%(c,"how many to carry, 0 = leave alone"if c=="REAGENTS"else "how many to carry"),[("num",r,C(n,a-76),"How many %s to carry (0-%d, 0 = leave it alone)"%(n,af),None,0,af,{"dx":12+(g%2)*a,"stay":g%2==0})for g,(r,x,n,y)in enumerate(aV(c))],{"sh":bD(c),"lw":a-78,"fw":52,"fh":26})for c in au]+[("OPTIONS",(("check","deep","Count inside bags in your pack","Bags inside your backpack count too (as Inventory > Supplies and Grimoire)",{"h":28}),("check","src_deep","Take from bags inside the source too","Bags inside the chest or bank box too (only those whose contents you have seen)",{"h":30}),("note","One move every %.1f s; it stops when you pick something up."%f)),{"sh":bH})]
		def bJ(c,new):
			if(new["deep"],new["src_deep"])!=(c["deep"],c["src_deep"]):b.update(deep=new["deep"],src_deep=new["src_deep"]);R();a["count_at"]=0.
			if any(new[g]!=c[g]for g in q):
				j.clear();j.update((n,new[n])for n in q if new[n]>0);N(at,",".join("%s=%d"%(r,j[r])for r in q if j.get(r,0)>0));a["count_at"]=0.
				if Z()!=a["layout"]:a["redraw"]=True
		H=Kit.Page(b,bI,None,bJ,every=bb)
		def bK(g,x,y,w):H.vals=dict(b);H.vals.update((c,j.get(c,0))for c in q);H.build(g,x,y,w)
		def bL():a.update({"shutting":False,"docked":False,"queue":[],"run":None,"halt":False,"status":("Idle",l),"opened":[],"page":0,"count_at":0.,"short":{},"layout":None,"active":True,"redraw":False,"shown_moved":0,"minimized":t.start_min()});aE();aQ(az,"Restock stopped early",bh);bp();aa();ag.service("restock.run",s("go"));t.dock(fit=True,min=(av,Y+ad(2)))
		def bM():
			if k["g"]is None:return
			if aK(k):return
			if a["opened"]:bq()
			while a["queue"]:
				b=a["queue"].pop(0)
				if t.action(b):continue
				c=bG.get(b[0]if isinstance(b,tuple)else b)
				if c is not None:c(b)
			if a["redraw"]:
				a["redraw"]=False
				if Z()!=a["layout"]:aa()
			d=time.time();r=a["run"]
			if r is not None:
				bt(d);bw()
				if r["moved"]!=a["shown_moved"]:a["shown_moved"]=r["moved"];a["count_at"]=0.
			aU(d)
		def bN():return.05 if a["run"]is not None else.1
		aE()
		def bO():a.update({"shutting":True,"halt":True,"active":False});r,a["run"]=a["run"],None;ao(r);R();ag.close()
		return{"start":bL,"tick":bM,"stop":bO,"client_tick":True,"config_height":H.height,"build_config":bK,"poll_config":H.poll,"config_closed":H.closed,"interval":bN}
	def bx():
		j="supplies";aA="Supplies";aZ="UnitFrames_settings";P="UnitFrames_supset";a_=10.;a0=.5;a1=1.;Q=220;R=22;F=20;aB=20;aC="UnitFrames_suppos";U=("Below the frame","Left of the frame","Right of the frame");a2=10;a3=.1;a4=.25;k=tuple(bG+(None,)for bG in an);a5=("bp","bm","ga","gi","mr","ns","ss","sa","p_heal","p_cure","p_refresh","s_recall","s_gate","o_band");aD="UnitFrames_supplies";aE="UnitFrames_supwarn";a8=E;ba=.25;aF=9999;d={"sup_open":False,"sup_deep":True,"sup_hide0":False,"sup_follow":True,"sup_low":a2,"sup_side":0};bE=dict(d);H={"sup_low":(0,9999),"sup_side":(0,2)};b={"minimized":False,"shutting":False,"docked":False,"next_supply":0.,"counts":{},"next_save":0.,"queue":[]};p={"g":None,"c":{},"store":({},{})};i=set(a5);a={"g":None,"c":{},"rows":(),"at":None,"slot":None,"drawn":None};n={};V={"next_warn":0.};L,W=ab,N;M,Z,bF=ak(b,aA)
		def bb(key):a6(key,",",d,H)
		def aH():bb(P if L(P,"")else aZ)
		def O():a7(P,",",d,sorted(d),H)
		def aI():
			a=L(aD,"-")
			if a=="-":return
			b=set(c[0]for c in k);i.clear();i.update(f for f in a.split(",")if f in b)
		def aK():W(aD,",".join(c[0]for c in k if c[0]in i)or "none")
		def aL():
			n.clear();d=set(f[0]for f in k)
			for b in L(aE,"").split(","):
				if "="not in b:continue
				c,v=b.split("=",1)
				if c not in d:continue
				a=[]
				for e in(v.split("/")+["",""])[:2]:
					try:a.append(max(0,min(aF,int(e))))
					except ValueError:a.append(None)
				if a[0]is not None or a[1]is not None:n[c]=a
		def be():
			b=[]
			for r in k:
				a=n.get(r[0])
				if a:b.append("%s=%s/%s"%(r[0],""if a[0]is None else a[0],""if a[1]is None else a[1]))
			W(aE,",".join(b))
		def bf():
			b={}
			for a,m,n,j,c in k:
				if a in i:b.setdefault(j,[]).append((a,c))
			e=dict((w[0],0)for w in k if w[0]in i)
			if not b:return e
			for f in ap(bool(d["sup_deep"]),a0):
				try:
					g=b.get(int(f.Graphic or 0))
					if not g:continue
					c=int(f.Hue or 0)&16383;l=max(1,int(f.Amount or 1))
				except Exception:continue
				for a,h in g:
					if h is None or h==c:e[a]+=l
			return e
		def aa():return tuple((c,f,g)for c,f,g,h,w in k if c in i and not(d["sup_hide0"]and not b["counts"].get(c,0)))
		def aM(key):
			c=b["counts"].get(key,0);a=n.get(key);f=a[1]if a is not None and a[1]is not None else d["sup_low"]
			if c<=f:e=u
			else:e=a8 if a is not None and a[0]is not None and c<=a[0]else D
			return "{:,}".format(int(c)),e
		def aN():return bool(d["sup_follow"])and not ac(j)
		def aO():return a["slot"]if ac(j)else None
		def ae(rows,pitch):b=[(c,[g for g in rows if g[1]==c])for c in au if any(f[1]==c for f in rows)];a=[26+len(h)*pitch+4 for w,h in b]or[26+2*pitch+4];return b,a,16+sum(a)+v*(len(a)-1)
		def bg(w,h,mode):
			b=(int(w),int(h))if(w is not None and h is not None)else None
			if b!=a["slot"]or mode=="again":a["slot"]=b;a["drawn"]=False
		def bh():return Q,ae(aa(),aB)[2]
		def aP(rows):
			d=a["g"];b=aO();A=ac(j);f=aN();c=Kit.pitch(R);n,p,h=ae(rows,c);w=Q if b is None else b[0]
			if b is not None:
				M=sum(len(bG)for bH,bG in n)or 2;c=max(aB,min(2*R,c+(b[1]-h)//M));n,p,h=ae(rows,c)
				if h<b[1]:p[-1]+=b[1]-h;h=b[1]
			g=G.CreateGump(True,not f and not ao(j));af(g,w,h,corners=False);E={};y=8;H=dict((bI,(bJ,bK))for bI,bL,bM,bJ,bK in k)
			if not n:B(g,8,y,w-16,p[0],"SUPPLIES");N="None of these in your pack."if i else "No rows ticked yet.";e(g,N,18,y+26,l);e(g,"Pick rows: its settings page.",18,y+26+c,l)
			for(O,P),J in zip(n,p):
				B(g,8,y,w-16,J,O)
				for U,(r,X,V)in enumerate(P):s=y+26+U*c;bj(g,H[r][0],H[r][1],16,s+(c-F)//2-1,F);K,W=aM(r);s+=(c-R)//2;E[r]=e(g,K,w-18-o(K),s+2,W);e(g,C(V,w-18-F-4-18-6-44),18+F+4,s+2)
				y+=J+v
			t=None
			if A:D=aG(j);x,u=(D[0],D[1])if D is not None else ah()
			elif not f:
				S(g,0,0,w,h,lambda:None,"Drag to move the supplies table",movable=True);x,u=ah()
				if z(d):x,u=d.GetX(),d.GetY()
				at(g,x,u,w,h)
			else:L=aq(w,h);t=L[1]if L is not None else ah();at(g,t[0],t[1],w,h)
			if not am(j):m(g,({},{}),"close",I,w-8-30,10,None,"Close the supplies list",on_click=Z("close"))
			a.update({"g":g,"c":E,"rows":rows,"at":t,"w":w,"h":h,"follow":f,"leader":None,"drawn":b})
			if A:bk(j,g,bc(g,x,u,w,h,j,False,None,None))
			else:G.AddGump(g)
			if not f and not A:a9(g,q)
			T(d);ar()
		bi=(60,620)
		def ah():
			b=L(aC,"");a["saved"]=b
			try:x,y=(int(f)for f in b.split(","));return aJ(x,y,a.get("w",0),a.get("h",0))
			except ValueError:c=aq(a.get("w",Q),a.get("h",0));return c[1]if c is not None else bi
		def q():
			g=a["g"]
			if z(g)and not a.get("follow",True)and not ac(j):
				try:b="%d,%d"%(int(g.GetX()),int(g.GetY()))
				except Exception:return
				if b!=a.get("saved"):a["saved"]=b;W(aC,b)
		def aq(w,h):
			a=HOST.services.get("frames.player_anchor")
			if a is None:return
			try:return a(w,h,d["sup_side"])
			except Exception:return
		def ar():
			g=a["g"]
			if not z(g)or not a.get("follow",True):return
			d=aq(a["w"],a["h"])
			if d is None:return
			c,b=d
			if a.get("leader")is not c:a["leader"]=c;ag(g,c)
			if b!=a["at"]:
				a["at"]=b
				try:at(g,b[0],b[1],a["w"],a["h"]);aj(g)
				except Exception:pass
		bl=620;bm="UnitFrames_rowspos";aw="supplies_rows"
		def aQ():
			M,f=K,v;w=bl;b=w-2*M;r=max(sum(1 for bG in k if bG[1]==G)for G in au);h=52+r*aS+4;j=M+30+f+h+M;g,c,t=s.begin(w,j);af(g,w,j);B(g,M,M,b,30);e(g,"SUPPLIES TABLE ROWS",M+30,M+7,E);a=w-M-54-20-35-o("Untick all");m(g,c,"none",I,a,M+4,"Untick all","Empty the table");a-=14+35+o("Tick all");m(g,c,"all",ad,a,M+4,"Tick all","Show every row");S(g,M,M,a-M-6,30,lambda:None,"Drag to move",movable=not ao(aw))
			if not am(aw):m(g,c,"close",I,w-M-54,M+4,None,"Close the table")
			d=M+30+f;B(g,M,d,b,h,"ROWS  (ticked rows show in the table)");l=(b-16)//len(au)
			for u,n in enumerate(au):
				p=M+10+u*l;e(g,n,p,d+30,E)
				for x,(q,z,y,A,D)in enumerate(bH for bH in k if bH[1]==n):t[q]=ay(g,C(y,l-34),p,d+52+x*aS,q in i)
			s.end(g,{"next_poll":0.})
		s=Kit.Window(aw,"Supplies Rows",b,p,aQ,bm,default=(260,160),cleanup=M,owner=False,clear={"c":{}})
		def aR(now):
			if not d["sup_open"]:
				if a["g"]is not None:q();i,a["g"]=a["g"],None;T(i)
				return
			f=now>=b["next_supply"]or not b["counts"]or(now>=b.get("sup_min",0.)and av()!=b.get("pack_v"))
			if f:b.update({"next_supply":now+a1,"sup_min":now+a3,"pack_v":av()});b["counts"]=bf()
			if not z(a["g"])or a.get("follow")!=aN()or a["drawn"]!=aO():q();aP(aa())
			elif f:
				e=aa()
				if e!=a["rows"]:q();aP(e)
				else:
					for g,k,l in e:
						h,j=aM(g);c=a["c"].get(g)
						if c is not None and A(c,h,j):c.SetPos(a["w"]-18-bd(h),c.GetY())
					ar()
			else:ar()
		def bn(now):
			g=p["g"]
			if g is None:return
			if not z(g):p.update({"g":None,"c":{}});return
			e,f=p["store"],p["c"]
			if X(e,"close"):s.close();return
			h=False
			for l,a in(("all",True),("none",False)):
				if X(e,l):
					h=True
					for c in f.values():c.SetIsChecked(a)
			if not h and not HOST.pass_poked and now<p.get("next_poll",0.):return
			p["next_poll"]=now+a4;d=set()
			for k,c in f.items():
				try:a=bool(c.IsChecked)
				except Exception:a=k in i
				if a:d.add(k)
			if d!=i:i.clear();i.update(d);aK();b["next_supply"]=0.;Y(j)
		def bo(now):
			if not d["sup_open"]:d["sup_open"]=True;O();b["next_supply"]=0.
			aR(now);g=a["g"]
			if z(g):safe(lambda:ai(g).BringOnTop())
		def bp(now):d["sup_open"]=False;O()
		bq={"open":bo,"close":bp,"sup_rows":lambda now:aQ()};ax=(("sup_follow","The table sticks to the player frame","Untick to drag it anywhere"),("sup_deep","Count inside bags in your backpack","Bags and pouches in your backpack count too"),("sup_hide0","Hide rows you have none of","Leave out rows at 0"));br="A row at or below this shows red, unless it has its own Red below (0-%d)"%H["sup_low"][1];aS=24;bs=118;aV=26;r=44
		def aW():return[c for c in k if c[0]in i]
		def bt():return 30+20+max(1,(len(aW())+1)//2)*aV+4
		def bu(f,x,y):
			g,b=f.g,aW();c=(f.w-36)//2;k=[]
			if not b:e(g,"No rows ticked yet: click Choose rows above.",x+12,y+2,l)
			for p in range(2 if len(b)>1 else(1 if b else 0)):a=x+12+p*(c+12)+c-2*r-8;e(g,"Yellow",a,y-2,E);e(g,"Red",a+r+8,y-2,u)
			for m,(o,t,h,v,w)in enumerate(b):i=x+12+(m%2)*(c+12);j=y+20+(m//2)*aV;a=i+c-2*r-8;e(g,C(h,a-i-8),i,j+3);d=n.get(o)or(None,None);q=al(az(g,""if d[0]is None else str(d[0]),a,j,r),"Yellow at or below this many %s (empty: never)"%h);s=al(az(g,""if d[1]is None else str(d[1]),a+r+8,j,r),"Red at or below this many %s (empty: Red at or below above)"%h);k.append((o,q,s))
			f.c["warn"]=k
		def bv(w):return(("TABLE",(("check",)+ax[0]+({"stay":True},),("check",)+ax[1]+({"dx":12+w//2},),("check",)+ax[2],("num","sup_low","Red at or below:",br,None)+H["sup_low"]+({"ldy":4,"lgap":12,"fw":60,"stay":True},),("note","Opens:",{"dx":12+w//2,"ndy":4,"hue":None,"stay":True}),("buttons",(("sup_rows",J,"Choose rows","Pick the rows the table shows (%d of %d ticked)"%(len(i),len(k))),),{"dx":w-45-o("Choose rows"),"bdy":-78})),{"sh":bs}),("SUPPLY WARNINGS  (yellow and red counts, per row)",(("custom",0,bu),),{"sh":bt()}))
		def bw(f):
			if X(f.store,"sup_rows"):Z("sup_rows")()
			if f.c.get("warn")and time.time()>=V["next_warn"]:
				V["next_warn"]=time.time()+ba
				if aX(f.c):b["next_supply"]=0.
		def bx(f,new):
			a=f.c.get("sup_side")
			if a is None:return
			b=Kit.dd_index(a,-1)
			if 0<=b<len(U):new["sup_side"]=b
		def by(c,new):b["next_supply"]=0.;a["at"]=None
		t=Kit.Page(d,bv,O,by,adjust=bx,clicks=bw)
		def bz(g,x,y,w):
			f=t.build(g,x,y,w);b=x+24+(w//2)+o("Opens:");V["next_warn"]=0.
			try:a=G.CreateDropDown(150,list(U),int(d["sup_side"]));a.SetPos(b,y+82);g.Add(a);f.c["sup_side"]=al(a,"Side of the player frame the table opens on (flips when there is no room)")
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
						try:a[i]=max(0,min(aF,int(g)))
						except ValueError:pass
				if a!=list(e):
					if a[0]is None and a[1]is None:n.pop(d,None)
					else:n[d]=a
					b=True
			if b:be()
			return b
		def bA():
			f=t.f
			if f is not None and f.c.get("warn")and aX(f.c):b["next_supply"]=0.
			t.closed()
		def aY():Z("open")()
		def bB():b.update({"next_supply":0.,"counts":{},"next_save":0.,"queue":[]});a["saved"]=None;aH();aI();aL();M.service("supplies.open",aY);s.dock();aT(j,{"title":aA,"state":lambda:"open"if z(a["g"])else None,"show":aY,"gump":lambda:a["g"],"fit":bg,"min":bh,"untitled":True,"redraw":lambda:a.update(drawn=False)});M.add(aU,j)
		def bC():
			a=time.time()
			while b["queue"]:
				c=b["queue"].pop(0)
				if s.action(c):continue
				d=bq.get(c)
				if d is not None:d(a)
			bn(a);aR(a)
			if a>=b["next_save"]:b["next_save"]=a+a_;q()
		aH();aI();aL()
		def bD():O();aK();q();g,a["g"]=a["g"],None;T(g);M.close()
		return{"start":bB,"tick":bC,"stop":bD,"client_tick":True,"config_height":t.height,"build_config":bz,"poll_config":t.poll,"config_closed":bA}
	def bz():
		q="inventory.sections";z="Bag Sections";R="UnifiedBag_sections";ai="UnifiedBag_sections_pos";aj="UnifiedBag_sections_min";W=330;am=(260,46);an=3701;h=46;r=54;j=36;k=30;s=6;S=2.;ao=.5;aq=.25;T=1.;d=12;ar=240;U=24;at=15;au=("reagents","potions","bandages","gold","scrolls","maps");b={"other":True};b.update(("p_"+bw,bw in au)for bw,by in Q);aw=dict(b);a={"minimized":False,"shutting":False,"docked":False,"queue":[],"groups":[],"sig":None,"ver":-1,"at":0.,"kinds":0,"loaded":False,"built":0.,"due":0.};m={"g":None,"c":{},"store":({},{}),"cells":[]};V,t,p=ak(a,z);c=[]
		def E(vals):return sum(1 for f,i in Q if vals["p_"+f])
		def ax():
			f=str(ab(R,"")or "");b.update(aw);del c[:];a["loaded"]=True
			if not f:return
			for k,h in Q:b["p_"+k]=False
			for e in f.split(";"):
				if e in("other","-other"):b["other"]=e=="other"
				elif e.startswith("c~"):
					p=e.split("~",2)
					try:g=int(p[1],16)
					except(IndexError,ValueError):continue
					if len(p)>2 and len(c)<d and all(i[0]!=g for i in c):c.append((g,p[2][:U]or "Item"))
				elif("p_"+e)in b:b["p_"+e]=True
			for k,h in reversed(Q):
				if len(c)+E(b)<=d:break
				b["p_"+k]=False
		def x():a=["c~%04X~%s"%f for f in c]+[i for i,n in Q if b["p_"+i]];N(R,";".join(a+["other"if b["other"]else "-other"]))
		def Z(it,gr):
			try:a=re.sub(r"^[\d,]+\s+","",str(it.Name or "").strip())
			except Exception:a=""
			a=re.sub(r"[;~|]"," ",a).strip();return a[:1].upper()+a[1:]if a else "Item 0x%04X"%gr
		def aa(n):return P(n)if n<10000 else "%dk"%(n//1000)
		def ay(w):return max(1,(w-2*K-16)//h)
		def az(n,cols):return k+max(1,(n+cols-1)//cols)*r+s
		def ac():return 2*K+30+v
		def ad():return 2*K+16+3*h,ac()+k+r+s
		def ae():return "Reading item kinds."if H["data"]is None else "Nothing to show."
		def aA(i):
			def a(*b):
				a=m["cells"]
				if i<len(a)and a[i]["serial"]:t(("use",a[i]["serial"]))()
			return a
		def J():
			z=g.zone_slot(*ad());w=z[0]if z else W;c=ay(w);i=a["groups"];J=sum(az(len(bw),c)+v for by,bw in i)-v if i else k+20;x=z[1]if z else ac()+J;b,Q,L=g.begin(w,x);m=[]
			if not a["minimized"]:
				g.frame(b);M=K;A=w-2*M;y=M+30+v;C=x-M
				if not i:B(b,M,y,A,C-y);L["empty"]=e(b,ae(),M+12,y+10,l)
				for N,(O,n)in enumerate(i):
					f=max(1,(len(n)+c-1)//c)
					if z:f=min(f,(C-y-k-s)//r)
					if f<1:break
					E=k+f*r+s;B(b,M,y,A,E,"%s  (%d)"%(O.upper(),len(n)))
					for p,(q,t)in enumerate(n[:f*c]):
						u=M+8+(p%c)*h;F=y+k+(p//c)*r;d=G.CreateGumpItemPic(q[0],j,j);d.SetRect(u+(h-j)//2,F,j,j)
						if q[1]:d.Hue=q[1]
						d.DrawBorder=False;al(d,t[0]);Kit.hook_double(d,aA(len(m)));b.Add(d);H=aa(t[1]);I=F+j+1;P=e(b,H,u+(h-o(H))//2,I,D);m.append({"gi":N,"ci":p,"serial":t[2],"amt":P,"x":u,"y":I})
					y+=E+v
			g.end(b,{"cells":m});af()
		g=Kit.Window(q,z,a,m,J,ai,aj,(W,300),am,an,V,clear={"cells":[]})
		def af():
			c=m["c"];e=a["groups"]
			if "status"in c:A(c["status"],"%s: %s"%(z,F(a["kinds"],"kind")));return
			if "empty"in c:A(c["empty"],ae())
			for b in m["cells"]:
				try:v=e[b["gi"]][1][b["ci"]][1]
				except IndexError:continue
				b["serial"]=v[2];d=aa(v[1])
				if A(b["amt"],d):b["amt"].SetPos(b["x"]+(h-o(d))//2,b["y"])
		def aB():a=H["data"]or{};d=[(i,frozenset((f,)))for f,i in c];return d+[(w,a.get(n,frozenset()))for n,w in Q if b["p_"+n]]
		def aC(a):return a[1][0].lower(),a[0]
		def aD():
			e=aB();f=len(e);g=[{}for w in range(f+1)];n=0;k=b["other"]
			for a in ap():
				try:c,h,i,l=int(a.Graphic),int(a.Hue),max(1,int(a.Amount or 1)),int(a.Serial)
				except Exception:continue
				d=f
				for m,(q,o)in enumerate(e):
					if c in o:d=m;break
				if d==f and not k:continue
				j=g[d].get((c,h))
				if j is not None:j[1]+=i
				elif n<ar:n+=1;g[d][(c,h)]=[Z(a,c),i,l]
			p=[G for G,bw in e]+["Other"];return[(p[bB],sorted(by.items(),key=aC))for bB,by in enumerate(g)if by]
		def ag(now,d=False):
			a["ver"],a["at"],a["due"]=av(),now,0.;b=aD();c=tuple((f,tuple(n for n,w in i))for f,i in b)
			if d and c!=a["sig"]and 0.<=now-a["built"]<T:a["due"]=a["built"]+T;return
			a["groups"]=b;a["kinds"]=sum(len(G)for bw,G in b)
			if c!=a["sig"]:a["sig"],a["built"]=c,now;J()
			else:af()
		def aE(action):
			b=action[1]
			if not a5(b):p("that is no longer in your backpack.",u);return
			Kit.once(lambda:API.UseObject(b),(q,b))();a["at"]=time.time()-S+ao
		def ah():
			if len(c)+E(b)<d:return False
			p("%d sections at most."%d,u);return True
		def aF(action):
			if ah():return
			p("target an item for its own section.")
			def a(serial):t(("picked",int(serial or 0)))()
			aI(at,a,q)
		def aG(action):
			f=action[1];b=API.FindItem(f)if f else None
			if b is None:return
			d=int(b.Graphic);e=Z(b,d)[:U]
			if any(i[0]==d for i in c):p("%s already has a section."%e,u);return
			if ah():return
			c.append((d,e));x();a["at"]=0.;Y(q);p("added a %s section."%e,L)
		def aH(action):
			if 0<=action[1]<len(c):c.pop(action[1]);x();a["at"]=0.;Y(q)
		aJ={"use":aE,"add":aF,"picked":aG,"remove":aH}
		def aL(w):
			e=(w-24)//2;f=[("check","p_"+bw,G,"A section for %s"%G.lower(),{"dx":12+(n%2)*e,"stay":n%2==0})for n,(bw,G)in enumerate(Q)];a=[]
			for i,(g,b)in enumerate(c):a+=[("note",C(b,w-80-o("Remove")),{"stay":True,"ndy":4,"hue":D}),("buttons",(("rm%d"%i,I,"Remove","Remove the %s section"%b),),{"dx":w-48-o("Remove")})]
			if not a:a=[("note","None yet: add one from a target.")]
			return(("SECTIONS  (%d at most, in this order)"%d,f+[("check","other","Show Other","Everything the sections leave, in a last section")]),("YOUR SECTIONS  (checked first)",a+[("buttons",(("add",M,"Add from target...","Target an item for a section of its own"),))]))
		def aM(b,new):a["at"]=0.
		def aO(f,new):
			a=len(c)+E(new)-d;e=False
			for k,g in reversed(Q):
				if a<=0:break
				if new["p_"+k]and not b["p_"+k]:new["p_"+k]=False;a-=1;e=True;O(f.c["p_"+k],"IsChecked",False)
			if e:p("%d sections at most."%d,u)
		def aP(f):
			if X(f.store,"add"):t("add")()
			for i in range(len(c)):
				if X(f.store,"rm%d"%i):t(("remove",i))();break
		y=Kit.Page(b,aL,x,aM,adjust=aO,clicks=aP)
		def aQ():a.update({"shutting":False,"docked":False,"queue":[],"groups":[],"sig":None,"ver":-1,"at":0.,"kinds":0,"loaded":False,"minimized":g.start_min(),"built":0.,"due":0.});ax();J();g.dock(fit=True,min=ad)
		def aR():
			q=a["queue"]
			while q:
				b=q.pop(0)
				if not g.action(b):aJ[b[0]if isinstance(b,tuple)else b](b)
			if m["g"]is None or aK(m)or a["minimized"]or a["docked"]or H["data"]is None:return
			c=time.time();d=c-a["at"]
			if not 0.<=d<S or 0.<a["due"]<=c:ag(c)
			elif d>=aq and av()!=a["ver"]:ag(c,True)
		def aS():
			if H["data"]is not None:return
			try:a=aN()
			except Exception:a=None
			try:bl(a)
			except Exception:H["data"]={}
		def aT():return H["data"]is None and not a["shutting"]
		def aU():
			a["shutting"]=True
			if a["loaded"]:x()
			V.close()
		return{"start":aQ,"tick":aR,"stop":aU,"client_tick":True,"config_height":y.height,"build_config":y.build,"poll_config":y.poll,"config_closed":y.closed,"thread_tick":aS,"thread_wanted":aT}
	bA=(("bags",bs,.1,"bag"),("paperdoll",bt,.1,"character"),("storage",bu,.1,"storage"),("restock",bv,.1,"restock"),("supplies",bx,.1,"supplies"),("sections",bz,.1));return PartSet(bm,bn,bA).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("inventory","Inventory","Bags, paperdoll, storage, restock, supplies",_module_inventory,.1,category="Your things",parts=(("bags","Bags","All your bags in one grid",True,("bag",)),("paperdoll","Paperdoll","What you wear, and your stats",True,("character",)),("storage","Storage","What the containers you opened hold",False,("storage",)),("restock","Restock","Refills from a chest or bank, on a press",False,("restock",)),("supplies","Supplies","Pack supplies, low counts marked",True,(),True),("sections","Bag Sections","What you carry, grouped by kind",False,(),True),),aliases=('Character','Unified Bag','Storage Index','Restock','paperdoll','bank','chest','find','sort','supplies','supplies table','sections'))
