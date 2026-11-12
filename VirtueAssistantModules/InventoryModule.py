def _module_inventory():
	N=Client.on_client_thread;H=Follow.toggle;O=HOST.alert;P=HOST.alert_kind;I=HOST.bar_alive;Q=HOST.cursor_busy;R=HOST.cursor_ok;S=HOST.dock_add;T=HOST.dock_remove;U=HOST.dock_wanted;u=HOST.layout_holds;z=HOST.layout_locked;J=HOST.layout_rect;K=HOST.me;V=HOST.pack_dirty;A=HOST.pack_items;D=HOST.pack_ver;X=HOST.part_on;L=HOST.pick_target;o=HOST.refresh_settings;E=HOST.release_cursor;Y=HOST.show_settings;B=Journal.find;Z=Journal.reader;ad="inventory";ae="Inventory"
	def M():
		from System import AppDomain;from System.Reflection import BindingFlags
		for a in AppDomain.CurrentDomain.GetAssemblies():
			t=a.GetType("ClassicUO.Assets.TileDataLoader")
			if t is not None:return t.GetField("_staticData",BindingFlags.Static|BindingFlags.NonPublic)
		return
	C=("REAGENTS","POTIONS","SCROLLS","OTHER");v=tuple((ar.lower(),"REAGENTS")+Kit.REAGENTS[ar]for ar in("BP","BM","GA","GI","MR","NS","SS","SA"));v+=(("bw","REAGENTS","Bat Wing",3960),("gd","REAGENTS","Grave Dust",3983),("db","REAGENTS","Daemon Blood",3965),("nc","REAGENTS","Nox Crystal",3982),("pi","REAGENTS","Pig Iron",3978),("p_heal","POTIONS","Heal",3852),("p_cure","POTIONS","Cure",3847),("p_refresh","POTIONS","Refresh",3851),("p_str","POTIONS","Strength",3849),("p_agi","POTIONS","Agility",3848),("p_ns","POTIONS","Night Sight",3846),("p_expl","POTIONS","Explosion",3853),("p_poison","POTIONS","Poison",3850),("s_recall","SCROLLS","Recall",8012),("s_gate","SCROLLS","Gate Travel",8032),("s_mark","SCROLLS","Mark",8025),("s_gheal","SCROLLS","Greater Heal",8009),("s_heal","SCROLLS","Heal",7985),("s_cure","SCROLLS","Cure",7991),("s_acure","SCROLLS","Arch Cure",8005),("s_mr","SCROLLS","Magic Reflection",8016),("s_invis","SCROLLS","Invisibility",8024),("s_reveal","SCROLLS","Reveal",8028),("s_tele","SCROLLS","Teleport",8002),("s_prot","SCROLLS","Protection",7995),("s_bless","SCROLLS","Bless",7997),("s_res","SCROLLS","Resurrection",8039),("o_band","OTHER","Bandages",3617),("o_arrow","OTHER","Arrows",3903),("o_bolt","OTHER","Bolts",7163))
	def aa(g,graphic,hue,x,y,size):
		p=G.CreateGumpItemPic(graphic,size,size);p.SetRect(x,y,size,size)
		if hue:p.Hue=hue
		p.DrawBorder=False;p.SetAcceptMouseInput(False);g.Add(p)
	def l(n):return "{:,}".format(int(n))
	def ab(key,g,xy):
		a=J(key)
		if a is None or xy is None or(xy[0],xy[1])==(a[0],a[1]):return
		g.SetPos(int(a[0]),int(a[1]));Kit.note_rect(g,a[0],a[1]);Kit.moved_by_code(g)
	F=(("reagents","Reagents",(3962,3963,3972,3973,3974,3976,3980,3981)+(3960,3965,3978,3982,3983)),("gems","Gems",tuple(range(3855,3889))),("potions","Potions",tuple(range(3846,3854))),("scrolls","Scrolls",tuple(range(7981,8045))+(3827,)),("gold","Gold",(3821,3822,3823)),("bandages","Bandages",(3617,3817)),);m=(("reagents","Reagents"),("potions","Potions"),("bandages","Bandages"),("gold","Gold and gems"),("scrolls","Scrolls"),("maps","Treasure maps"),("ores","Ores and ingots"),("wood","Wood"),("hides","Hides and cloth"),("food","Food"),("weapons","Weapons"),("armour","Armour"),("jewellery","Jewellery"),("keys","Keys and tools"));af={"maps":("treasure map","tattered map","map"),"ores":(" ore","ingot"),"wood":("log","board"),"hides":("hide","leather","cloth","wool","cotton","flax","yarn","thread","bolt of"),"food":("bread","cake","muffin","pie","apple","pear","peach","grape","fish steak","ham","bacon","sausage","ribs","cheese","carrot","lettuce","cabbage","turnip","onion","melon","squash","gourd","lemon","lime","banana","date","coconut","chicken","bird","egg","cookie","wedge","corn","pumpkin","meat","jar of honey"),"keys":("key","tongs","hammer","saw","scissors","pickaxe","shovel","lockpick","sewing","tinker","mortar","fletcher","dovetail","skillet","rolling pin","scorp","plane","inshave","fishing pole","hatchet","smith")};ag=(6+2,10,14,18);ai=134217728;e={"data":None,"wanted":False}
	def ac(field):
		c=field.GetValue(None)if field is not None else None;a=dict((n,set())for n,p in m)
		for k,j,d in F:
			if k=="gems":a["gold"].update(d)
			elif k in a:a[k].update(d)
		if c is not None:
			for b in range(min(int(c.Length),65536)):
				try:
					t=c[b];f=str(t.Name or "").lower()
					if not f:continue
					g=int(t.Flags)
					if bool(t.IsImpassable):continue
					if bool(t.IsWeapon):a["weapons"].add(b)
					if g&ai:a["armour"].add(b)
					if bool(t.IsWearable)and int(t.Layer)in ag:a["jewellery"].add(b)
					if g&2097152 or bool(t.IsContainer):continue
					h=" "+f
					for k,i in af.items():
						for w in i:
							if w in h:a[k].add(b);break
				except Exception:continue
		e["data"]=dict((q,frozenset(r))for q,r in a.items())
	def aj(graphic):
		a=e["data"]or{}
		for k,b in m:
			if graphic in a.get(k,()):return k
		return
	def ak():
		S="bag";A="Bags"
		try:import clr;from System import Array,Object,Byte,Single,UInt16,UInt32;from System.Reflection import BindingFlags;ci=True
		except Exception:ci=False
		dM=8;a6,af=1,50;aF=(142,94);cj=(150,130);an=600;bx=4;ck=30;dN,dO=104,64;dP=.1;dQ=.8;dR=.002;dS=3;dT=81;bz=1000;dU=(2330,2350);dV=(3834,8787,8786,9100,9120,11600);cl,cm,dW=60,30,46;dX=20;aU=20;dY="999";aV="UnifiedBag_shrunk";ag=44;bA=500;a7=132;a8=116;ad=6;a9=8;bB=5;dZ=9;ba=(36,32);aG=(60,80);d_=7012;d0=7013;cn=(2117,2118,2118);bb=4;d1=20;d2=24;co=10;cp=0x7E57CA7C;d3=3;d4=.1;d5=.05;d6=6;d7=8;d8=.5;d9=.09;ea=20;eb=4;ec=.3;bc=2;ed=200;cq=6;cr=5.;ee=1.3;ct=1.;ef=1.;eg=3;eh=["fizzles","concentration is disturbed"];ei=["already casting","not yet recovered"];ej=["More reagents are needed"];ek=["Insufficient mana","not have enough mana"];aw=68;bC=8.;el=.15;em=2;bD=3000;bE=400;en=8;cu=2.;eo=600;aH=.7;ep=600;cv=3;cx=2;bd=24;eq=125;er=["cannot hold more"];es=["must wait to perform another action"];et=tuple(gS[0]for gS in F);aI="#5C544A";cy="#7A7066";ax,T,K=Kit.HUE_GOOD,Kit.HUE_INFO,Kit.HUE_BAD;bF="UnifiedBag_cmd";cz="UnifiedBag_state";cA=S
		class Bag(object):
			def __init__(self,**a):self.update(**a)
			def update(self,**a):self.__dict__.update(a)
		cB={};gP=dict(cB);l={"cfg_bad":False,"slots":dM,"cols":0,"rows":0,"assign":{},"frame_x":200,"frame_y":120,"saved_fx":200,"saved_fy":120,"cell_w":aF[0],"cell_h":aF[1],"fit_pending":True,"fit_seen":None,"trim":True,"opacity":.9,"scale_pct":100,"scale_items":False,"driving":False,"drive_fixed":False,"drive_told":False,"hb_frame":-1,"hb_time":0.,"opacity_pending":None,"icons_used":None,"status_text":"","own_cell":None,"mgr_x":120,"mgr_y":140,"trp_x":200,"trp_y":180,"mgr_min":False,"trp_min":False,"minimized":False,"docked":False,"bare":False,"side_hidden":False,"link_state":None,"attach":None,"attach_g":None,"canvas":None,"side_pw":0,"detached_at":0.,"grid_wh":None,"names":{},"wait_player":False,"wait_load":False,"load_wanted":False,"load_text":None,"trap_sel":set(),"trap_extra":[],"job":None,"queue":[],"reported":False,"dirty_frame":True,"dirty_mgr":False,"dirty_trp":False,"open_mgr":False,"open_trp":False,"want_mgr":False,"want_trp":False,"save_in":-1,"to_write":None,"shutting":False,"flt_pick":None,"quick_at":0.,"filters":[],"open_flt":False,"dirty_flt":False,"flt_min":False,"flt_x":260,"flt_y":120,"rules":{},"sort":None,"srt_x":240,"srt_y":160,"srt_min":False,"open_srt":False,"want_srt":False,"dirty_srt":False,"layout":(),"geom":(1,aF[0],aF[1],0),"bar_raw":None,"grid_raw":None,"grid_info":(None,False),"slot_raws":(),"cats_seen":None};v={"g":None,"c":{},"store":({},{}),"side_status":None,"bar":None,"grid":None,"mgr":None,"trp":None,"trap_checks":[],"srt":None,"rule_checks":[],"search_box":None,"counts":[],"count_state":{}};cC,cD,gQ=Kit.basics(l,A)
		def D(kind,*a):
			def b(*b):cD.add((kind,)+a)
			return b
		def aJ(key):Kit.dispose(v.get(key));v[key]=None
		def ak(x,y,w,h,color,alpha):b=G.CreateGumpColorBox(alpha,color);b.SetRect(x,y,w,h);return b
		def ao(g,text,x,y,hue=None):return Kit.inert(Kit.add_label(g,text,x,y,hue))
		def be(k,w,h,title,c,d):M=Kit.MARGIN;a=l[k+"_min"];g=G.CreateGump(True,True);Kit.place(g,l[k+"_x"],l[k+"_y"],w,h);Kit.add_window_frame(g,w,h,corners=not a);Kit.add_section(g,M,M,w-2*M,30);Kit.add_label(g,title,M+30,M+7,Kit.HUE_TITLE);Kit.title_catcher(g,M,M,w-2*M-84,30,c,key="bag_"+k);b=({},{});Kit.art_button(g,b,"min",Kit.ART_RESTORE if a else Kit.ART_MIN,w-M-74,M+7,None,Kit.RESTORE_TIP if a else Kit.MIN_TIP,on_click=c);Kit.art_button(g,b,"close",Kit.ART_CLOSE,w-M-54,M+4,None,"Close this window",on_click=d);return g,b,M+30+Kit.GAP
		def bf(k,g,moved,**more):Kit.add_front(g);Kit.on_moved(g,moved);v[k]=g;v.update(more)
		def ap():l["save_in"]=ea
		def aq():l["dirty_frame"]=True;ap()
		def ar(text,n):text=text or "";return text if len(text)<=n else text[:n-1]+"~"
		def ai(serial,c=True):
			a=l["names"].get(serial)
			if a is None:
				b=Kit.find_item(serial)
				if not b:return "0x%08X (not loaded)"%serial
				a=b.Name or "Container"
				if len(l["names"])>=ed:l["names"]={}
				l["names"][serial]=a
			return("%s  0x%08X"%(a,serial))if c else a
		def cE():l["names"]={}
		r=Bag(tried=False,ok=False,can_ok=False,error="",f_tiles=None);H=Bag(frame=0,gumps={},managed=set(),trimmed=set(),bounds={},scale=1.,max_w=0,max_h=0,disabled=False,error="",fail_streak=0,open_count=0,catchers={},icons=None,hook_calls=0,pre_calls=0,glist=None,head=None,count=-1,lay=None,want=frozenset(),placed={},bar_at=None,full_frame=-1000,full_at=0.,fulls=0,labels_for=(None,None),meas={},opened=frozenset(),hold=None,ginfo={},catch_ok={},gtr={});C={"ver":0,"regions":{},"order":[],"orient":"rows","breaks":None,"sig":None,"items":None,"kinds":{},"size":None,"slow":False,"job":None};bg={"done":None};JR={"rd":None};aK={};aW=[];p={"ctrl":None,"rect":None,"texts":True,"said":None,"sum_i":0,"art":{},"world":None,"tiles":None,"prof_at":0.,"sum_at":0.,"hooked":False,"poked":set(),"poke_at":0.}
		def eu():
			if not ci:r.error="clr module unavailable";return
			try:
				b=API.GetType().Assembly;clr.AddReference(b);from ClassicUO.Game.UI.Controls import Control;from ClassicUO.Game.UI.Gumps import ContainerGump;from ClassicUO.Game.UI.Controls import ClickPriority;a=BindingFlags.Instance|BindingFlags.NonPublic;c=BindingFlags.Static|BindingFlags.Public|BindingFlags.NonPublic;d=clr.GetClrType(ContainerGump);r.ContainerGump=ContainerGump;r.f_data=d.GetField("_data",a);r.f_pic=d.GetField("_gumpPicContainer",a);r.f_hit=d.GetField("_hitBox",a);e=clr.GetClrType(Control);r.m_offset=e.GetMethod("SetHitTestOffset",a);r.f_bounds=e.GetField("_bounds",a);r.Point=clr.GetPythonType(e.GetProperty("Location").PropertyType);r.Rect=clr.GetPythonType(r.f_bounds.FieldType);f=b.GetType("ClassicUO.Game.Managers.UIManager");r.p_gumps=f.GetProperty("Gumps",c);r.p_cscale=f.GetProperty("ContainerScale",c);h=b.GetType("ClassicUO.Configuration.ProfileManager");r.p_profile=h.GetProperty("CurrentProfile",c)
				for g in("f_data","f_pic","f_hit","m_offset","f_bounds","p_gumps","p_cscale","p_profile"):
					if getattr(r,g)is None:raise Exception("client member not found: "+g)
				class FrameHook(Control):
					def PreDraw(self):H.pre_calls+=1;H.hook_calls+=1;bH()
					def Draw(self,a,x,y):
						if H.pre_calls==0:H.hook_calls+=1;bH()
						return True
				class DropCatcher(Control):
					def Draw(self,a,x,y):return True
				r.Hook=FrameHook;r.Catcher=DropCatcher;r.LowPriority=ClickPriority.Low;r.ok=True
			except Exception as i:r.ok=False;r.error=str(i);return
			ev()
		def ev():
			r.can_ok=False
			try:
				from ClassicUO.Game.UI.Controls import Control,ItemGump
				class BagCanvas(Control):
					def Draw(self,a,x,y):
						try:w,h=self.va_wh
						except Exception:return True
						try:eF()
						except Exception:pass
						if a.ClipBegin(int(x),int(y),int(w),int(h)):
							try:
								Control.Draw(self,a,x,y)
								if p["texts"]:fi(a,int(x),int(y))
							finally:a.FlushBatch();a.ClipEnd()
						return True
					def OnMouseUp(self,x,y,button):
						try:
							if fa(int(x),int(y),button):return
						except Exception as e:H.error="canvas: %s"%e
						Control.OnMouseUp(self,x,y,button)
					def OnMouseDoubleClick(self,x,y,button):
						try:
							if fc(int(x),int(y),button):return True
						except Exception as e:H.error="canvas: %s"%e
						return Control.OnMouseDoubleClick(self,x,y,button)
					def OnMouseOver(self,x,y):
						try:fe(self,int(x),int(y))
						except Exception:pass
						Control.OnMouseOver(self,x,y)
				class BagLayer(Control):pass
				class CanvasItem(ItemGump):
					def OnMouseUp(self,x,y,button):r.up_item=self;ItemGump.OnMouseUp(self,x,y,button)
				r.Canvas,r.Layer,r.CanvasItem,r.ItemGump=(BagCanvas,BagLayer,CanvasItem,ItemGump);r.up_item=None;r.Mouse=Tz.T("ClassicUO.Input.Mouse");r.Actions=Tz.T("ClassicUO.Game.GameActions");r.f_tiles=M();r.can_ok=True
			except Exception as e:r.can_ok=False;H.error="canvas: %s"%e
		def bG(a):
			try:return a()
			except Exception:return a(None)
		def cF(grid,tell):
			if not r.ok or H.disabled or l["drive_fixed"]:return
			try:
				a=bG(r.Hook);a.AcceptMouseInput=False;b=l["grid_info"][0]
				if b is not None and N():
					with Kit.quiet:
						a.Parent=b
						if b.Children.Contains(a):return
				grid.Add(a)
			except Exception as e:
				l["driving"]=l["drive_fixed"]=True;H.error="draw hook: %s"%e
				if tell:API.SysMsg(A+": couldn't install the draw hook (%s); the script keeps the bags in place."%e,T)
		def cG(grid):safe(lambda:setattr(grid,"LayerOrder",type(grid.LayerOrder).Under))
		cH={}
		def ew(w):return w.Gump
		ex=(ew,Kit.client_control)
		def at(a):
			if a is None:return
			t=type(a);b=cH.get(t)
			if b is not None:
				with Kit.quiet:
					v=b(a)
					if v is not None:return v
			for c in ex:
				if c is b:continue
				try:v=c(a)
				except Exception:continue
				if v is not None:cH[t]=c;return v
			return
		def ay(fn):return Kit.on_client(fn,False)
		def bH():
			try:eD();H.fail_streak=0
			except Exception as e:H.error=str(e);H.fail_streak+=1
			except:H.error="unknown error";H.fail_streak+=1
			if H.fail_streak>120:H.disabled=True
		def cI(g,x,y):
			a=g.Offset
			if a.X!=x or a.Y!=y:r.m_offset.Invoke(g,Array[Object]([x,y]))
		def bh():
			b={};c=r.p_gumps.GetValue(None);H.glist=c;a=c.First
			while a is not None:
				v=a.Value
				if isinstance(v,r.ContainerGump)and not v.IsDisposed:b[int(v.LocalSerial)]=v
				a=a.Next
			H.gumps=b
			try:H.scale=float(r.p_cscale.GetValue(None))
			except Exception:pass
		def ey():
			b=H.glist
			if b is None:return
			a=b.First;d=a.Value if a is not None else None;e=b.Count
			if d is H.head and e==H.count:return
			H.head,H.count=d,e;f=H.want
			if not f:return
			g=H.gumps;n=0
			while a is not None and n<d7:
				v=a.Value
				if isinstance(v,r.ContainerGump)and not v.IsDisposed:
					c=int(v.LocalSerial)
					if c in f and g.get(c)is not v:g[c]=v
				a=a.Next;n+=1
		def ez(g):b=cZ(g);s=H.scale;a,c=int(b[0]*s),int(b[1]*s);return a,c,int(b[2]*s)-a,int(b[3]*s)-c
		def cJ(idx):b,c,d,a=l["geom"];r,e=divmod(idx,b);return l["frame_x"]+e*(c+a),l["frame_y"]+aB()+r*(d+a)
		def bI(c):a=c.Location;return int(a.X),int(a.Y)
		def az(c,x,y):
			a=c.Location
			if a.X!=x or a.Y!=y:c.Location=r.Point(x,y)
		def bJ(c):a=r.f_bounds.GetValue(c);return int(a.Width),int(a.Height)
		def bK(g):
			H.managed.discard(g);H.placed.pop(g,None);b=g in H.trimmed;H.trimmed.discard(g)
			if g.IsDisposed:H.catchers.pop(g,None);return
			cL(g)
			if not g.IsVisible:g.IsVisible=True;Kit.stir()
			cI(g,0,0);g.AcceptMouseInput=True;g.CanMove=True;a=r.f_pic.GetValue(g)
			if a is not None:a.Alpha=1.
			if b and not g.IsMinimized:g.RequestUpdateContents()
		def aL(g,c):
			a=g.Children
			while a.Contains(c):a.Remove(c)
		def cK(g,c):
			aL(g,c)
			if not c.IsDisposed:c.Dispose()
		def cL(g):
			H.catch_ok.pop(g,None);c=H.catchers.pop(g,None)
			if c is not None:cK(g,c)
		def eA(g):
			b=H.catchers.get(g)
			for a in list(g.Children):
				if a is not b and int(a.LocalSerial)==cp:cK(g,a)
		def eB(g,left,top,iw,d):
			c=H.catchers.get(g);a=g.Children;n=a.Count;b=H.catch_ok.get(g)
			if b is not None and c is not None and b[0]is c and b[1]==n and b[2]is(a[n-1]if n else None)and b[3]==(left,top,iw,d)and not c.IsDisposed:return
			if c is None or c.IsDisposed or not a.Contains(c):
				if g not in H.catchers:eA(g)
				c=r.Catcher();c.LocalSerial=cp;c.AcceptMouseInput=True;c.Priority=r.LowPriority;c.Parent=g;aL(g,c);a.Insert(0,c);H.catchers[g]=c
			elif a.IndexOf(c)!=0 or a.LastIndexOf(c)!=0:aL(g,c);a.Insert(0,c)
			e=r.f_bounds.GetValue(c)
			if(e.X,e.Y,e.Width,e.Height)!=(left,top,iw,d):r.f_bounds.SetValue(c,r.Rect(left,top,iw,d))
			if not c.IsVisible:c.IsVisible=True
			n=a.Count
			if len(H.catch_ok)>=bL:H.catch_ok.clear()
			H.catch_ok[g]=(c,n,a[n-1]if n else None,(left,top,iw,d))
		bL=64
		def bM(g):
			a=H.ginfo.get(g)
			if a is None:
				a=(int(g.Graphic),bool(g.IsChessboard or g.IsBackgammonBoard))
				if len(H.ginfo)>=bL:H.ginfo.clear()
				H.ginfo[g]=a
			return a
		def eC(g,idx,trim):
			if g.CanMove:g.CanMove=False
			cI(g,0,0);c,d=cJ(idx);k=bM(g)[1]
			if g.IsMinimized or k or not trim:
				if g in H.trimmed:
					H.trimmed.discard(g);cL(g)
					if not g.IsMinimized:g.RequestUpdateContents()
				if not g.AcceptMouseInput and g.IsVisible:g.AcceptMouseInput=True
				a=r.f_pic.GetValue(g)
				if a is not None and abs(a.Alpha-l["opacity"])>.01:a.Alpha=l["opacity"]
				az(g,c,d)
				if g.IsMinimized:return 0,0,a,False
				w,m=bJ(g);return w,m,a,False
			e,f,h,i=ez(g);a=r.f_pic.GetValue(g)
			if a is not None and a.IsVisible:a.IsVisible=False
			b=r.f_hit.GetValue(g)
			if b is not None and b.IsVisible:b.IsVisible=False
			if g.AcceptMouseInput:g.AcceptMouseInput=False
			eB(g,e,f,h,i);az(g,c-e,d-f);H.trimmed.add(g);j=int(round(d1*H.scale));return h+j,i+j,a,True
		def eD():
			if H.disabled or l["shutting"]:return
			D=l["bar_raw"];c,P=l["grid_info"];v=False;o=l["attach"];j=l["minimized"]
			if o is not None:
				j=j or not o.get("shown",True);e=fq()
				if e is not None and not e.IsDisposed:
					a,b=bI(e);a,b=a+int(o.get("dx",0)),b+int(o.get("dy",0));v=(a,b)!=H.bar_at;H.bar_at=(a,b);l["frame_x"],l["frame_y"]=a,b
					if c is not None and not c.IsDisposed:
						az(c,a,b)
						if c.IsVisible==j:c.IsVisible=not j
			else:
				if P and c is not None and not c.IsDisposed:e,q,E=c,D,0
				else:e,q,E=D,c,ag
				if e is not None and not e.IsDisposed:
					a,b=bI(e);v=(a,b)!=H.bar_at;H.bar_at=(a,b);l["frame_x"],l["frame_y"]=a,b
					if q is not None and not q.IsDisposed:az(q,a,b+E)
			s=l["layout"]
			if s is not H.lay:H.lay=s;H.want=frozenset([ah for by,ah in s])
			H.frame+=1;F=time.time();h=H.frame-H.full_frame>=d6 and F-H.full_at>=d9
			if h:H.full_frame,H.full_at=H.frame,F;H.fulls+=1;bh()
			else:ey()
			G=h;Q=h and H.fulls%10==1;h=h or v;I=l["trim"];R=(I,l["opacity"],l["geom"],aB(),C["ver"]);t=set();f=set();x=y=0;i=None;S=r.f_pic;J=l["canvas"]is not None and not j
			if J:K=p["rect"]or(0,0,0,0);T,U=l["frame_x"]+K[0],l["frame_y"]+K[1];V=h or l["driving"];W=(p["seen_n"],p["seen_last"],p["seen_min"])
			for d,k in s:
				g=H.gumps.get(k)
				if g is None:continue
				if g.IsDisposed:
					if G:continue
					G=True;bh();g=H.gumps.get(k)
					if g is None or g.IsDisposed:continue
				f.add(d)
				if J:
					try:
						if eE(g,k,T,U,V,W):
							if i is None:i=g
							t.add(g);H.managed.add(g)
					except Exception as z:H.error="bag 0x%08X: %s"%(k,z)
					continue
				if i is None:i=g
				t.add(g);H.managed.add(g)
				try:
					if j:
						if g.IsVisible:g.IsVisible=False;Kit.stir()
						H.placed.pop(g,None);continue
					if not g.IsVisible:g.IsVisible=True;Kit.stir()
					L=bool(g.IsMinimized);M=(d,R,L);m=H.placed.get(g);n=S.GetValue(g)
					if not h and m is not None and m[0]==M and n is m[2]and not(m[3]and n is not None and n.IsVisible):w,u=m[1]
					else:
						w,u,n,N=eC(g,d,I);H.placed[g]=(M,(w,u),n,N)
						if L:X,Y=bJ(g);H.meas[d]=(X,Y,H.scale,True,None)
						else:H.meas[d]=(w,u,H.scale,False,int(g.Graphic)if N else None)
					x,y=max(x,w),max(y,u)
				except Exception as z:H.error="bag 0x%08X: %s"%(k,z)
			H.open_count=len(f)
			if f!=H.opened:
				H.opened=frozenset(f)
				for d in[ch for ch in H.meas if ch not in f]:H.meas.pop(d,None)
			if i is not None and Q:
				try:Z=int(r.f_data.GetValue(i).IconizedGraphic)or aG[1];H.icons=(int(i.Graphic),Z)
				except Exception:pass
			if len(H.managed)>len(t):
				for g in[cs for cs in H.managed if cs not in t]:bK(g)
			H.max_w,H.max_h=x,y;A=l["slot_raws"]
			if f!=H.labels_for[0]or A is not H.labels_for[1]:
				for d,aa in enumerate(A):
					O=d not in f
					for B in aa:
						if B is not None and B.IsVisible!=O:B.IsVisible=O
				H.labels_for=(f,A)
		def eE(g,serial,px,py,b,seen):
			if bM(g)[1]:
				if g in H.managed:bK(g)
				return False
			if g.IsVisible:g.IsVisible=False;Kit.stir()
			if g.AcceptMouseInput:g.AcceptMouseInput=False
			if b:
				if g.CanMove:g.CanMove=False
				az(g,px,py)
			a=g.Children;n=a.Count
			if seen[0].get(serial)!=n or seen[1].get(serial)is not(a[n-1]if n else None)or seen[2].get(serial)!=g.IsMinimized:
				if p["built"]==C["ver"]and p["ctrl"]is not None:bo(serial,g)
			return True
		def eF():
			b=H.gumps
			for c in C["order"]:
				a=C["kinds"].get(c)
				if a is None or a[0]=="board"or a[0]=="closed":continue
				g=b.get(a[2])
				if g is not None and g.IsVisible:g.IsVisible=False;Kit.stir()
		def cM():
			for g in list(H.managed):
				with Kit.quiet:bK(g)
		def eG(minimize):
			a=set(l["assign"].values())
			def b():
				bh();n=0
				for s in a:
					g=H.gumps.get(s)
					if g is None or g.IsDisposed or g.IsChessboard or g.IsBackgammonBoard:continue
					if bool(g.IsMinimized)!=minimize:g.IsMinimized=minimize;n+=1
				return n
			return ay(b)
		def cN():
			def a():a=r.p_profile.GetValue(None);return(int(a.ContainersScale),bool(a.ScaleItemsInsideContainers))
			return ay(a)
		def bi(pct,items):
			def a():
				a=r.p_profile.GetValue(None);c=(int(a.ContainersScale)!=pct or bool(a.ScaleItemsInsideContainers)!=items);a.ContainersScale=Byte(pct);a.ScaleItemsInsideContainers=items;r.p_cscale.SetValue(None,Single(pct/100.));H.scale=pct/100.
				if c:
					b=r.p_gumps.GetValue(None).First
					while b is not None:
						v=b.Value
						if isinstance(v,r.ContainerGump)and not v.IsDisposed:v.RequestUpdateContents()
						b=b.Next
				return c
			return ay(a)
		def cO(serial):
			if r.ok and not H.disabled:g=H.gumps.get(serial);return g is not None and not g.IsDisposed
			a=Kit.find_item(serial);return bool(a)and Kit.is_open(safe(lambda:a.GetContainerGump()))
		def cP():a=safe(lambda:int(API.Player.Serial),0);return Kit.data_path("_unified_bag_%d.cfg"%a)
		def cQ():cT(cS())
		def al():
			l["save_in"]=-1
			if not P()and l["canvas"]!="alone":l["saved_fx"],l["saved_fy"]=l["frame_x"],l["frame_y"]
			b=["slots=%d"%l["slots"],"cols=%d"%l["cols"],"rows=%d"%l["rows"],"frame_x=%d"%l["saved_fx"],"frame_y=%d"%l["saved_fy"],"cell_w=%d"%l["cell_w"],"cell_h=%d"%l["cell_h"],"trim=%d"%int(l["trim"]),"collapsed=%d"%int(l["minimized"]),"bare=%d"%int(l["bare"]),"side=%d"%int(l["side_hidden"]),"opacity=%d"%int(round(l["opacity"]*100)),"mgr_x=%d"%l["mgr_x"],"mgr_y=%d"%l["mgr_y"],"trp_x=%d"%l["trp_x"],"trp_y=%d"%l["trp_y"],"mgr_open=%d"%int(l["open_mgr"]),"mgr_min=%d"%int(l["mgr_min"]),"trp_open=%d"%int(l["open_trp"]),"trp_min=%d"%int(l["trp_min"]),"trapsel="+",".join(str(f)for f in sorted(l["trap_sel"])),"trapextra="+",".join(str(h)for h in l["trap_extra"]),]
			for a in sorted(l["assign"]):b.append("slot.%d=%d"%(a,l["assign"][a]))
			b+=["srt_x=%d"%l["srt_x"],"srt_y=%d"%l["srt_y"],"srt_open=%d"%int(l["open_srt"]),"srt_min=%d"%int(l["srt_min"])]
			for a in sorted(l["rules"]):
				c,d=l["rules"][a]
				if c or d:b.append("sort.%d=%s;%s"%(a,",".join(sorted(c)),",".join(str(i)for i in d)))
			l["to_write"]=(cP(),"\n".join(b))
			if not safe(lambda:HOST.by_key[S].running,False):bO()
		def bN():return bool(Q(S))
		def bO():
			a=l["to_write"]
			if a is None:return
			l["to_write"]=None;b,c=a
			if l["cfg_bad"]:return
			try:Kit.write_safe(b,c)
			except Exception as e:API.SysMsg(A+": couldn't save its settings (%s)."%e,K)
		def cR(text):return[int(a)for a in(text or "").split(",")if a.strip().isdigit()]
		def cS():return Kit.read_safe(cP())
		def cT(raw):
			l["cfg_bad"]=raw is None
			if raw is None:API.SysMsg(A+": couldn't read its settings file, so changes aren't saved.",K);return
			if not raw:return
			b,a={},{}
			for d in raw.splitlines():
				if "="in d:
					k,v=[n.strip()for n in d.split("=",1)];b[k]=v
					try:a[k]=int(v)
					except ValueError:pass
			l["slots"]=max(a6,min(af,a.get("slots",l["slots"])));l["cols"]=max(0,min(af,a.get("cols",0)));l["rows"]=max(0,min(af,a.get("rows",0)));l["frame_x"],l["frame_y"]=Kit.adapt(a.get("frame_x",l["frame_x"]),a.get("frame_y",l["frame_y"]));l["saved_fx"],l["saved_fy"]=l["frame_x"],l["frame_y"];l["cell_w"]=max(20,min(an,a.get("cell_w",l["cell_w"])));l["cell_h"]=max(20,min(an,a.get("cell_h",l["cell_h"])));l["fit_pending"]="cell_w"not in a;l["opacity"]=max(10,min(100,a.get("opacity",a.get("panel_a",90))))/100.
			for g,k,h in(("trim","trim",1),("minimized","collapsed",0),("bare","bare",0),("side_hidden","side",0),("mgr_min","mgr_min",0),("trp_min","trp_min",0),("want_mgr","mgr_open",0),("want_trp","trp_open",0),("srt_min","srt_min",0),("want_srt","srt_open",0)):l[g]=a.get(k,h)==1
			for k in("mgr","trp","srt"):x,y=Kit.adapt(a.get(k+"_x",l[k+"_x"]),a.get(k+"_y",l[k+"_y"]));l.update(**{k+"_x":x,k+"_y":y})
			l["trap_sel"]=set(cR(b.get("trapsel")));l["trap_extra"]=cR(b.get("trapextra"));l["assign"],l["rules"]={},{}
			for k,v in b.items():
				e,j,i=k.partition(".")
				try:c=int(i)
				except ValueError:continue
				if not 0<=c<l["slots"]:continue
				if e=="slot"and a.get(k,0)>0:l["assign"][c]=a[k]
				elif e=="sort":
					f=eH(v)
					if f is not None:l["rules"][c]=f
		def eH(text):
			c,e,d=(text or "").partition(";");b=frozenset(f for f in(g.strip()for g in c.split(","))if f in et);a=[]
			for p in d.split(","):
				p=p.strip()
				if p.isdigit()and 0<int(p)<=65535 and int(p)not in a:a.append(int(p))
			a=tuple(a[:bd]);return(b,a)if(b or a)else None
		O={"told":None,"cols":None,"cell":None,"area":None}
		def cU(slots=None,cols=None,rows=None):
			slots=l["slots"]if slots is None else slots
			if cols is None and rows is None and O["cols"]:c=max(1,min(slots,O["cols"]));return c,int(math.ceil(slots/float(c)))
			cols=l["cols"]if cols is None else cols;rows=l["rows"]if rows is None else rows
			if cols>0 and rows>0:return cols,rows
			if cols>0:return cols,int(math.ceil(slots/float(cols)))
			if rows>0:c=int(math.ceil(slots/float(rows)));return c,int(math.ceil(slots/float(c)))
			c=max(1,int(math.ceil(math.sqrt(slots))));return c,int(math.ceil(slots/float(c)))
		def bj():return l["trim"]and r.ok and not H.disabled
		bk=[None,None]
		def bP():
			a=l["assign"]
			if a==bk[0]and l["slots"]==bk[1]:return
			b=tuple(sorted((c,d)for c,d in a.items()if c<l["slots"]))
			if b!=l["layout"]:l["layout"]=b
			bk[0],bk[1]=dict(a),l["slots"]
		def eI():
			s=H.scale if r.ok else 1.
			if bj():return int(aF[0]*s),int(aF[1]*s)
			return int(cj[0]*s),int(cj[1]*s)
		def bQ():l["cell_w"],l["cell_h"]=eI();l["fit_pending"]=True;aq()
		def cV(g):
			i=max(g-2*(a9+ad),0);a,c=[[]],0
			for e in[("bagicons",ba[1]+22),("break",dZ),("spellicons",ba[1]+22),("stop",22+4+18),("quick",4*24),("tools",24+26+24)]:
				f,h=e;d=h+(bB if a[-1]else 0)
				if a[-1]and c+d>i and f!="break":a.append([]);c,d=0,h
				if f=="break"and not a[-1]:continue
				a[-1].append(e);c+=d
			for b in a:
				while b and b[0][0]=="break":b.pop(0)
				while b and b[-1][0]=="break":b.pop()
			a=[k for k in a if k];j=[sum(q[1]for q in n)+bB*(len(n)-1)for n in a];return a,j
		def eJ(graphic,x,y,b,c,tip,handler):a=G.CreateGumpPic(graphic);d=a.GetWidth()or b;e=a.GetHeight()or c;k=min(b/float(d),c/float(e),1.);w,h=max(1,int(d*k)),max(1,int(e*k));a.SetRect(x+(b-w)//2,y+(c-h)//2,w,h);Kit.set(a,"ContainsByBounds",True);a.SetTooltip(tip);G.AddControlOnClick(a,handler);return a
		def bR(grid,e,k,d=0):
			t,m=aQ();i=m+bb;n,o=cV(k-i);f=len(n)*a7+2*ad;b=max(k,max(o)+2*(a9+ad)+i);Kit.add_resizepic(grid,Kit.WINDOW_BG,e,d,f,b);Kit.add_section(grid,e+ad,d+ad,f-2*ad,b-2*ad);u,w=l["icons_used"]
			for j,x in enumerate(n):
				p=e+ad+j*a7
				if j:grid.Add(Kit.inert(ak(p,d+ad+a9,1,b-2*(ad+a9),aI,.8)))
				a=p+(a7-a8)//2;y=d+(b-i-o[j])//2
				for c,q in x:
					if c in("bagicons","spellicons"):
						if c=="bagicons":r=((w,"Minimize every open slot bag",D("set_min",True),"Minimize"),(u,"Restore every minimized slot bag",D("set_min",False),"Restore"))
						else:r=((d_,"Cast Magic Trap on every ticked trap bag",D("start_job","Magic Trap"),"Trap"),(d0,"Cast Magic Untrap on every ticked trap bag",D("start_job","Magic Untrap"),"Untrap"))
						g=a8//2
						for s,(z,A,B,h)in enumerate(r):grid.Add(eJ(z,a+s*g,y,g,ba[1],A,B));ao(grid,h,a+s*g+max(0,(g-Kit.text_w(h))//2),y+ba[1]+3,Kit.HUE_INFO)
					elif c=="stop":h=Kit.art_button(grid,v["store"],"stop",Kit.ART_CLOSE,a,y,"Stop","Stop the trap, untrap or sort run",on_click=D("stop_all"));v["stop_ctrls"]=[v["store"][0].get("stop"),h];v["side_status"]=ao(grid,l["status_text"],a,y+26,Kit.HUE_INFO);dw()
					elif c=="quick":f9(grid,a,y)
					elif c=="tools":f7(grid,a,y)
					elif c=="break":grid.Add(Kit.inert(ak(a,y+q//2,a8,1,aI,.8)))
					y+=q+bB
			aR(grid,e+f-ad-bb-t,d+b-ad-bb-m,False);return f,b
		def P():return l["attach"]is not None
		def aA():return l["bare"]and not l["minimized"]and not P()
		def eK():return v.get("grid")if P()or l["canvas"]=="alone"or aA()else v.get("bar")
		def eL():
			if l["shutting"]or l["wait_player"]or not Kit.is_open(v.get("grid")):return
			return "docked"if l["docked"]else("minimized"if l["minimized"]else "open")
		def aM(w,h,mode):
			f=(None,None);m=l["geom"]
			if not P():
				d=(int(w),int(h))if(w is not None and h is not None)else None
				if(aN()and(d!=O["told"]or(mode=="again"and d is not None))):l["dirty_frame"]=True
				O["told"]=d
				if aN()and d is not None:return
			if w is not None and h is not None and m is not None:
				o,u,v,a=m;p=o*u+(o-1)*a;a=0 if bj()else bx;q=max(0,(l["grid_wh"][0]if l["grid_wh"]else p)-p)
				if P():q=0 if aP()else a+aX(int(h))
				g=int(w)-q;s=int(h)-aB();e,i=l["cell_w"],l["cell_h"];n=max(1,l["slots"]);b=None
				for c in range(1,n+1):
					r=int(math.ceil(n/float(c)));j=(g-(c-1)*a)//c;k=(s-(r-1)*a)//r
					if j<e or k<i:continue
					t=min(j/float(e),k/float(i))
					if b is None or t>b[0]:b=(t,c,j,k)
				if b is None:c=max(1,min(n,(g+a)//max(1,e+a)));r=int(math.ceil(n/float(c)));b=(0,c,max(e,(g-(c-1)*a)//c),max(i,(s-(r-1)*a)//r))
				f=(b[1],(b[2],b[3]))
			if f!=(O["cols"],O["cell"]):O["cols"],O["cell"]=f;l["dirty_frame"]=True
		def eM(b=None):
			g=0 if bj()else bx;h=O.get("area")
			if b is None and h is not None:b=h[1]
			j=0 if aP()else(l["side_pw"]if b is None else g+aX(int(b)));d=int(round(H.scale*100))if r.ok else l["scale_pct"];a=l["scale_pct"]if aa["pct"]is not None else d;k=ck if(r.ok and not H.disabled)else a
			if aa["pct"]is None or d==a:l["own_cell"]=(l["cell_w"],l["cell_h"],l["slots"]);e,f=float(l["cell_w"]),float(l["cell_h"])
			else:
				c=l["own_cell"]
				if c is not None and c[2]==l["slots"]:e,f=float(c[0]),float(c[1])
				else:i=a/float(max(1,d));e,f=l["cell_w"]*i,l["cell_h"]*i
			return e,f,g,l["slots"],j,a,a,min(k,a)
		au={}
		def aX(h):
			k=("sw",h);v=au.get(k)
			if v is None:
				c,a=aQ();b,d=cV(h-a-bb);v=len(b)*a7+2*ad
				if len(au)>=200:au.clear()
				au[k]=v
			return v
		def aN():return r.ok and r.can_ok and not H.disabled
		def cW():
			if not aN()or l["minimized"]or l["docked"]or l["shutting"]:return
			if P():return None if O["area"]is None or not l["attach"].get("shown",True)else "combined"
			return "alone"if O["told"]is not None and u(S)else None
		eN=120
		def cX():return[("Settings",),("Trap bags",),("Slots",)]
		def bS(w):
			k=("tf",w,l["slots"]);v=au.get(k)
			if v is None:
				a=Kit.title_plan(w,A,cX(),str(l["slots"]));v=len(a[3])==len(cX())and a[4]>=Kit.MARGIN+30+Kit.text_w("..")+Kit.TITLE_GAP
				if len(au)>=200:au.clear()
				au[k]=v
			return v
		def cY(mode):
			if mode=="combined":b=O["area"];a=0 if aP()else aX(b[1]);return 0,0,max(1,b[0]-a),max(1,b[1]),a
			w,h=O["told"];M=Kit.MARGIN
			if l["bare"]or not bS(w):return M,M,max(1,w-2*M),max(1,h-2*M),0
			c=M+30+Kit.GAP;d=max(1,h-c-M);a=aX(d)
			if w-2*M-a<eN:a=0
			return M,c,max(1,w-2*M-a),d,a
		def cZ(g,graphic=None):
			if graphic is None:graphic=int(g.Graphic)
			b=H.bounds.get(graphic)
			if b is None:a=r.f_data.GetValue(g).Bounds;b=(int(a.X),int(a.Y),int(a.Width),int(a.Height));H.bounds[graphic]=b
			return b
		def eO(g,graphic):return bM(g)[1]or graphic in dU
		def c_():
			d=[];e=set()
			for h,c in l["layout"]:
				if c in e:continue
				e.add(c);g=H.gumps.get(c);a,b="closed",0
				try:
					if g is not None and not g.IsDisposed:
						f=H.ginfo.get(g);b=f[0]if f is not None else int(g.Graphic)
						if eO(g,b):a="board"
						elif g.IsMinimized:a="mini"
						else:cZ(g,b);a="open"
				except Exception:a,b="closed",0
				d.append((h,b,a,c))
			return tuple(d)
		def c0(items):
			a=[]
			for c,d,e,f in items:b=H.bounds.get(d)if e=="open"else None;w,h=(max(1,b[2]-b[0]),max(1,b[3]-b[1]))if b is not None else(dN,dO);a.append((c,float(w*h),w/float(h)))
			return a
		def c1(f,W,s):
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
		def c2(a,W,b,breaks):
			S=sum(f[1]for f in a);c,j=0.,0
			for k in breaks:
				d=sum(W*b*a[g][1]/S for g in range(j,k));h=d/W
				if h<=0:return float("inf")
				for i in range(j,k):w=(W*b*a[i][1]/S)/h;c+=a[i][1]*math.log((w/h)/a[i][2])**2
				j=k
			return c
		def c3(a,W,b,keep=None):
			if not a:return "rows",[],0.
			d,i=c1(a,W,b);e=[(k,n,1./q)for k,n,q in a];f,j=c1(e,b,W);g=("columns",j,f)if f<dQ*d else("rows",i,d)
			if keep is not None and keep[1]and keep[1][-1]==len(a):
				o,c=keep;h=c2(a,W,b,c)if o=="rows"else c2(e,b,W,c)
				if not g[2]<(1.-dP)*h:return o,list(c),h
			return g
		def c4(a,W,b,orient,breaks):
			if not a:return{}
			if orient=="columns":return dict((q,(G,t,by,ah))for q,(t,G,ah,by)in c4(a,b,W,"rows",breaks).items())
			S=sum(s[1]for s in a);e={};j,f,c=0,0.,0;n=len(a)
			for k in breaks:
				g=sum(W*b*a[w][1]/S for w in range(j,k));f+=g;h=int(round(f/W))if k<n else b;l,d=0.,0
				for i in range(j,k):l+=W*b*a[i][1]/S;m=int(round(W*l/g))if i<k-1 else W;e[a[i][0]]=(d,c,m-d,h-c);d=m
				c=h;j=k
			return e
		def eP(b,d,ah,cs,x,y):
			a=b[2]-int(d/cs);c=b[3]-int(ah/cs)
			if x<b[0]:x=b[0]
			elif x>a:x=a
			if y<b[1]:y=b[1]
			elif y>c:y=c
			return x,y
		def bl(a):return a[2]>=cl and a[3]>=cm+aU
		def c5(a):
			if bl(a):b,c,d,e=a;return b,c+aU,d,e-aU
			return a
		def c6(a,ah,cs):return(float(a),float(ah))if C.get("si")else(a/cs,ah/cs)
		def c7(box,pw,ph):
			a,b,g,h=box;c,d=a+pw//2,a+g-1-(pw-pw//2);e,f=b+ph//2,b+h-1-(ph-ph//2)
			if d<c:c=d=a+g//2
			if f<e:e=f=b+h//2
			return c,d,e,f
		def eQ(b,box,f,ah,cs,g,by):a,c=c6(f,ah,cs);d,e=float(max(1,b[2]-b[0])),float(max(1,b[3]-b[1]));u=.5 if a>=d else(g+a/2.-b[0])/d;v=.5 if c>=e else(by+c/2.-b[1])/e;u=0. if u<0 else(1. if u>1 else u);v=0. if v<0 else(1. if v>1 else v);return box[0]+u*box[2],box[1]+v*box[3]
		def eR(b,box,a,ah,cs,px,py):c,d=c6(a,ah,cs);u=(px-box[0])/float(max(1,box[2]));v=(py-box[1])/float(max(1,box[3]));u=0. if u<0 else(1. if u>1 else u);v=0. if v<0 else(1. if v>1 else v);e=int(round(b[0]+u*(b[2]-b[0])-c/2.));f=int(round(b[1]+v*(b[3]-b[1])-d/2.));return e,f
		def eS(a,ah):
			if C.get("si"):b=H.scale or 1.;return max(1,int(a*b)),max(1,int(ah*b))
			return a,ah
		def eT(slot):
			b=C["regions"].get(slot);a=C["kinds"].get(slot)
			if b is None or a is None:return
			return a[2],c5(b),H.bounds.get(a[1]),H.scale or 1.
		def eU(d,serial,l,ah,pw,ph,e,by):
			if d is None:return 0,0
			m,f,g,n=d;a=aK.get(serial)
			if a is not None and a[0]==m and a[1]==e and a[2]==by:return int(a[3])-pw//2,int(a[4])-ph//2
			h,i,j,k=c7(f,pw,ph)
			if g is None:b,c=(h+i)//2,(j+k)//2
			else:b,c=eQ(g,f,l,ah,n,e,by);b=max(h,min(i,b));c=max(j,min(k,c))
			return int(round(b))-pw//2,int(round(c))-ph//2
		def eV(serial,bag,a,by,b,c):
			if serial not in aK:
				if len(aW)>=bz:
					for s in aW[:bz//2]:aK.pop(s,None)
					del aW[:bz//2]
				aW.append(serial)
			aK[serial]=(bag,a,by,b,c)
		def c8():aK.clear();del aW[:]
		def eW():
			a=time.time()
			if a>=p["prof_at"]:
				p["prof_at"]=a+1.
				try:l["scale_items"]=bool(r.p_profile.GetValue(None).ScaleItemsInsideContainers)
				except Exception:pass
			return l["scale_items"]
		def c9(sig,items,h,W,a,plan):
			b,c,l=plan;i=c4(h,W,a,b,c);d,e={},{}
			for f,j,k,g in items:d[f]=(k,j,g);e[g]=f
			C.update({"ver":C["ver"]+1,"regions":i,"slot_of":e,"order":[n[0]for n in items],"orient":b,"breaks":list(c),"sig":sig,"items":items,"kinds":d,"size":(W,a),"si":sig[4]});c8()
		def aY():
			try:return bY()is not None
			except Exception:return False
		def da(mode):
			if l["canvas"]is not None:bU()
			l["canvas"]=mode;H.placed.clear();l["dirty_frame"]=True
		def eX():
			c=cW()
			if c!=l["canvas"]:
				if aY():return
				da(c)
			if c is None:return
			d=cY(c);b=c_();a=(d[2],d[3],b,round(H.scale or 1.,4),eW());e=bg["done"]
			if e is not None and len(e)>1 and e[0]==a and C["job"]==a:
				if aY():return
				c9(*e);C["job"]=None;C["pending"]=None;return
			if a==C["sig"]:C["job"]=None;C["pending"]=None;return
			if a==C["job"]or aY():return
			W,g=d[2],d[3];f=c0(b);h=None
			if C["items"]==b and C["breaks"]is not None:h=(C["orient"],C["breaks"])
			if C["slow"]:C["job"]=a;C["pending"]=(a,b,f,W,g,h);return
			i=time.time();j=c3(f,W,g,h)
			if time.time()-i>dR and len(f)>8:C["slow"]=True
			c9(a,b,f,W,g,j)
		def db():a,b=C.get("pending"),bg["done"];return a is not None and(b is None or b[0]!=a[0])
		def eY():
			a=C.get("pending")
			if a is None or not db():return
			b,e,c,W,d,f=a
			try:bg["done"]=(b,e,c,W,d,c3(c,W,d,f))
			except Exception:bg["done"]=(b,)
		def dc():
			c=p["ctrl"]
			if c is None:return
			with Kit.quiet:
				a=c.Parent
				if a is not None:aL(a,c)
		def eZ(raw,index,x,y,w,h):
			c=p["ctrl"]
			if c is None or c.IsDisposed:bT();c=bG(r.Canvas);c.AcceptMouseInput=True;c.Priority=r.LowPriority;p["ctrl"]=c
			c.va_wh=(int(w),int(h));c.Parent=raw;a=raw.Children
			while a.Contains(c):a.Remove(c)
			a.Insert(min(index,a.Count),c);r.f_bounds.SetValue(c,r.Rect(int(x),int(y),int(w),int(h)));p["rect"]=(int(x),int(y),int(w),int(h))
			for b in p["layers"].values():r.f_bounds.SetValue(b,r.Rect(0,0,int(w),int(h)))
		def bT():p.update({"built":-1,"bsize":None,"parts":[],"icons":[],"bg":None,"layers":{},"pool":{},"owner":{},"items":{},"seen_n":{},"seen_last":{},"seen_min":{},"spot":{},"label":{},"count":{},"tip":None,"sums":{},"say_lbl":None,"sum_part":None,"alpha_set":None,"say_shown":False})
		bT()
		def bU():
			dc();c=p["ctrl"];p["ctrl"]=None
			if c is not None:safe(c.Dispose)
			bT();p["rect"]=None;c8();C.update({"sig":None,"items":None,"breaks":None,"regions":{},"kinds":{},"slot_of":{},"order":[],"job":None,"pending":None,"size":None});C["ver"]+=1;v["counts"]=[];v["count_state"]={}
		def dd():
			a=l["opacity"];b=p["bg"];c=(a,b)
			if p["alpha_set"]==c:return
			for d in([b]if b is not None else[])+p["icons"]:
				with Kit.quiet:
					if abs(float(d.Alpha)-a)>.001:d.Alpha=a
			p["alpha_set"]=c
		def de(w):
			a=at(w)if w is not None else None
			if a is None:return
			a.Parent=p["ctrl"];a.AcceptMouseInput=False;return a
		def e_():
			j=p["ctrl"];e=v.get("grid")
			if j is None or e is None:return
			for F in p["parts"]:
				with Kit.quiet:aL(j,F);F.Dispose()
			p["parts"],p["icons"],p["label"],p["count"]=[],[],{},{};p["tip"]=None;p["alpha_set"]=None;G=p["say_lbl"];p["say_lbl"]=None
			if G is not None:safe(G.Dispose)
			W,k=C["size"]or(p["rect"][2],p["rect"][3]);m,u=C["regions"],C["kinds"];c=[];c.append((Kit.add_tiled(e,Kit.SECTION_TILE,0,0,W,k,l["opacity"]),"bg"))
			for a in C["order"]:
				x,y,w,h=m[a]
				if x+w<W:c.append((ak(x+w-1,y,1,h,aI,.8),"seam"))
				if y+h<k:c.append((ak(x,y+h-1,w,1,aI,.8),"seam"))
			for a in C["order"]:
				f,Q,d=u[a]
				if f!="mini":continue
				n=H.gumps.get(d)
				try:z=int(r.f_data.GetValue(n).IconizedGraphic)or aG[1]
				except Exception:z=aG[1]
				x,y,w,h=m[a];A,B=Kit.pic_size(z);A,B=(A or 30),(B or 30);c.append((Kit.add_pic(e,z,x+(w-A)//2,y+(h-B)//2,mouse=False),"icon"))
			for a in C["order"]:c.extend(e0(e,a,m[a],u[a]))
			if not C["order"]:
				for R,S in enumerate(Kit.wrap("No bags yet. Click Slots to add some.",max(60,W-16))[:3]):c.append((Kit.add_label(e,S,8,8+20*R,Kit.HUE_INFO),"lbl"))
			I=[]
			for T in range(l["slots"]):o=Kit.add_label(e,"",0,0,Kit.HUE_GOOD);Kit.set(o,"IsVisible",False);g=m.get(T);I.append((o,g[0],g[1],g[2],g[3])if g else(o,0,0,0,0));c.append((o,"count"))
			Kit.flush();K=len([ah for ah in c if ah[1]!="count"]);q=[]
			for w,f in c:
				i=de(w)
				if i is None:continue
				q.append(i)
				if f=="bg":p["bg"]=i
				elif f=="icon":i.Alpha=l["opacity"];p["icons"].append(i)
			p["parts"]=q;D=p["layers"];E={}
			for a in C["order"]:
				b=D.pop(a,None)
				if b is None or b.IsDisposed:b=bG(r.Layer);b.AcceptMouseInput=False
				r.f_bounds.SetValue(b,r.Rect(0,0,int(W),int(k)));E[a]=b
			if D:
				L=list(D.values());U=p["pool"];M=[]
				for s in p["owner"]:
					N=U.get(s)
					if N is not None:
						V=N.Parent
						for b in L:
							if V is b:M.append(s);break
				for s in M:bn(s)
				for b in L:safe(b.Dispose)
			p["layers"]=E;O=j.Children;P=q[:K]+[E[by]for by in C["order"]]+q[K:]
			for t in P:t.Parent=j
			X=set(P)
			for t in list(O):
				if t not in X:O.Remove(t)
			v["counts"]=I;v["count_state"]={};p["built"]=C["ver"];p["bsize"]=(W,k);p["seen_n"],p["seen_last"],p["seen_min"]={},{},{}
			for a in C["order"]:
				f,Q,d=u[a];n=H.gumps.get(d)
				if n is not None and f in("open","mini"):bo(d,n)
				elif p["items"].get(d):
					for s in list(p["items"][d]):bn(s)
					p["items"][d]=[]
			if J["counts"]:bs()
		def e0(grid,slot,h,info):
			d,m,f=info;x,y,w,i=h
			if w<cl or i<cm:return[]
			if d=="open"and not bl(h):return[]
			a=[];j="#%d"%(slot+1);a.append((Kit.add_label(grid,j,x+5,y+3,Kit.HUE_TITLE),"lbl"));e=x+5+Kit.text_w(j)+6
			if d=="board":b=Kit.fit("Game board",max(8,x+w-4-e));a.append((Kit.add_label(grid,b,e,y+3,Kit.HUE_INFO),"lbl"));return a
			c=ai(f,False);k=x+w-e-(6+Kit.text_w(dY)if d=="open"else 0)-10;b=Kit.fit(c,max(8,k));g=c.rsplit(" [",1)[0]
			if b!=c and g!=c and Kit.text_w(g)<=max(8,k):b=g
			a.append((Kit.add_label(grid,b,e,y+3,Kit.HUE_INFO),"lbl"));p["label"][slot]=(c,b!=c)
			if d=="open":n=len(p["items"].get(f)or());l=Kit.add_label(grid,str(n),e+Kit.text_w(b)+6,y+3,Kit.HUE_INFO);p["count"][f]=l;a.append((l,"lbl"))
			elif i>=dW:a.append((Kit.add_label(grid,"Minimized"if d=="mini"else "Closed",x+5,y+3+dX,Kit.HUE_INFO),"lbl"))
			return a
		def bm(g):
			w=p["world"]
			if w is None:
				try:w=p["world"]=g.World
				except Exception:w=None
			return w
		def e1(g,serial):
			w=bm(g)
			try:return w.Get(UInt32(int(serial)))if w is not None else None
			except Exception:return
		def bV(ctl,graphic):
			a=r.f_bounds.GetValue(ctl);b=(int(a.Width),int(a.Height))
			if graphic not in p["art"]:
				if len(p["art"])>2000:p["art"].clear()
				p["art"][graphic]=b
			return b
		def e2(graphic):
			b=p["art"].get(graphic)
			if b is not None:return b
			g=l["grid_raw"]
			try:a=r.CanvasItem(g,UInt32(0),UInt16(int(graphic)),UInt16(0),0,0,False)
			except Exception:return 44,44
			try:return(1,1)if a.IsDisposed else bV(a,graphic)
			finally:safe(a.Dispose)
		def bn(serial):
			c=p["pool"].pop(serial,None);b=p["owner"].pop(serial,None);p["spot"].pop(serial,None)
			if c is not None:
				try:
					d=c.Parent
					if d is not None:aL(d,c)
					c.Dispose()
				except Exception:pass
			if b is not None:
				a=p["items"].get(b)
				if a and serial in a:a.remove(serial)
		def bo(bag,g):
			v=g.Children;n=v.Count;G=bool(g.IsMinimized);p["seen_n"][bag]=n;p["seen_last"][bag]=v[n-1]if n else None;p["seen_min"][bag]=G;j=C["slot_of"].get(bag);w=p["layers"].get(j)if j is not None else None
			if w is None:return
			I=[]
			if not G and C["kinds"][j][0]=="open":
				for k in range(n):
					a=v[k]
					if isinstance(a,r.ItemGump)and not a.IsDisposed:I.append(a)
			z,l=p["pool"],p["owner"];J=p["items"].get(bag)or[];m=[];e=[];K=bm(g);R=eT(j);S=C.get("si");L=H.scale or 1.;T=p["spot"];U,M,o=r.CanvasItem,UInt32,UInt16;t=0
			for a in I:
				s=int(a.LocalSerial);d=int(a.Graphic)
				try:b=K.Get(M(s))if K is not None else None
				except Exception:b=None
				f=int(b.Hue)if b is not None else int(a.Hue);c=z.get(s)
				if c is not None and c.IsDisposed:bn(s);c=None
				if c is None:
					try:c=U(g,M(s),o(d),o(f),0,0,False)
					except Exception:continue
					if c.IsDisposed:continue
					c.va_art=bV(c,d);c.va_gr,c.va_hue,c.va_sz,c.va_xy=d,f,None,None;z[s]=c
				elif c.va_gr!=d:
					c.Graphic=o(d)
					if c.IsDisposed:z.pop(s,None);l.pop(s,None);continue
					c.va_art=bV(c,d);c.va_gr,c.va_sz=d,None
				if c.va_hue!=f:c.Hue=o(f);c.va_hue=f
				A=l.get(s)
				if A is not None and A!=bag:
					B=p["items"].get(A)
					if B and s in B:B.remove(s)
				l[s]=bag;D,E=c.va_art;h,i=(max(1,int(D*L)),max(1,int(E*L)))if S else(D,E)
				if c.va_sz!=(h,i):
					q=r.f_bounds.GetValue(c)
					if int(q.Width)!=h or int(q.Height)!=i:r.f_bounds.SetValue(c,r.Rect(int(q.X),int(q.Y),h,i))
					c.va_sz=(h,i)
				N,O=(int(b.X),int(b.Y))if b is not None else bI(a);x,y=eU(R,s,D,E,h,i,N,O)
				if c.va_xy!=(x,y):az(c,x,y);c.va_xy=(x,y)
				T[s]=(x+h//2,y);m.append(s);e.append(c)
				if b is None:t+=s
				else:
					try:P=int(b.Amount)
					except Exception:P=0
					t=(t*31+s*7+N*131+O*137+f*139+P*149)&0x7FFFFFFF
			if J:
				V=set(m)
				for s in J:
					if s not in V and l.get(s)==bag:bn(s);aK.pop(s,None)
			p["items"][bag]=m;u=w.Children;F=u.Count==len(e)
			if F:
				for k in range(len(e)):
					if u[k]is not e[k]:F=False;break
			if not F:
				for c in e:c.Parent=w
				W=set(e)
				for c in list(u):
					if c not in W:u.Remove(c)
			Q=p["count"].get(bag)
			if Q is not None:Kit.set_text(Q,str(len(m)))
			p["sums"][bag]=t
		def df(g,b,t=0):
			w=bm(g);c=UInt32
			for s in b:
				try:a=w.Get(c(int(s)))if w is not None else None
				except Exception:a=None
				if a is None:t+=s;continue
				t=(t*31+s*7+int(a.X)*131+int(a.Y)*137+int(a.Hue)*139+int(a.Amount)*149)&0x7FFFFFFF
			return t
		dg=.2;e3=30;e4=.1;e5=40
		def e6(*c):
			a=p["poked"]
			if l["shutting"]or len(a)>=e5:return
			d=C.get("slot_of",())
			for b in c:
				try:s,e=int(b.Serial),int(b.Container)
				except Exception:continue
				for k in(e,s):
					if k in d:a.add(k)
				return
		def e7():
			d=time.time();f=p["poked"]
			if f and d>=p["poke_at"]:
				p["poke_at"]=d+e4;k=list(f);f.difference_update(k)
				for a in k:
					g=H.gumps.get(a)
					if g is not None and not g.IsDisposed:bo(a,g)
			h=C["order"]
			if not h:return
			if 0<=p["sum_at"]-d<=dg:return
			p["sum_at"]=d+dg;e=p["sum_part"]
			if e is not None:
				a,g,b,n,c,i,t=e
				if p["items"].get(a)is not b or len(b)!=n or g.IsDisposed or H.gumps.get(a)is not g:e=None;p["sum_part"]=None
			if e is None:
				i=p["sum_i"]%len(h);p["sum_i"]=i+1;l,m,a=C["kinds"][h[i]]
				if l!="open":return
				g=H.gumps.get(a)
				if g is None or g.IsDisposed:return
				b=p["items"].get(a);c=tuple(b)if b else();n,i,t=len(b)if b is not None else-1,0,0
			j=i+e3
			if j<len(c):p["sum_part"]=(a,g,b,n,c,j,df(g,c[i:j],t));return
			p["sum_part"]=None
			if df(g,c[i:],t)!=p["sums"].get(a):bo(a,g)
		def bW(serial,hue):
			c=p["pool"].get(serial)
			if c is None:return
			h=int(hue)&65535
			try:
				if not c.IsDisposed and c.va_hue!=h:c.Hue=UInt16(h);c.va_hue=h
			except Exception:pass
		def aO(x,y):
			for a in C["order"]:
				r=C["regions"].get(a)
				if r is not None and r[0]<=x<r[0]+r[2]and r[1]<=y<r[1]+r[3]:return a
			return
		def bX(graphic):
			a=p["tiles"]
			if a is None:
				if r.f_tiles is None:return
				a=p["tiles"]=r.f_tiles.GetValue(None)
			return None if a is None or graphic<0 or graphic>=a.Length else a[graphic]
		def e8(it,hold):
			try:a=int(it.Graphic)
			except Exception:return True
			if a in dV:return True
			t=bX(a)
			if t is None:return True
			try:return True if bool(t.IsContainer)else bool(t.IsStackable)and a==int(Tz.get(hold,"Graphic"))
			except Exception:return True
		def dh(serial,button):
			a=p["owner"].get(serial);g=H.gumps.get(a)if a is not None else None
			if g is None or g.IsDisposed:return False
			g.OnMouseUp(0,0,button);return True
		def e9(bag):
			g=H.gumps.get(bag);w=bm(g)if g is not None else p["world"]
			if w is None:return True
			try:
				a=w.Get(UInt32(int(bag)))
				if a is None:return True
				b=w.Get(a.RootContainer);return b is None or int(b.Distance)<=dS
			except Exception:return True
		def di():API.PlaySound(dT)
		def fa(x,y,button):
			f=str(button);c=r.up_item;r.up_item=None;b=int(c.LocalSerial)if c is not None and not c.IsDisposed else None
			if f=="Left":
				d=bY()
				if d is not None:
					if b is not None:
						g=e1(H.gumps.get(p["owner"].get(b)),b)
						if g is not None and e8(g,d):return dh(b,button)
					a=aO(x,y)
					if a is None:return True
					fb(a,x,y,d);return True
				if l["flt_pick"]is not None:
					a=aO(x,y)
					if a is not None:
						e=C["kinds"].get(a);h=dict((q,n)for n,q in l["layout"])
						if e is not None and e[2]in h:D("filter_canvas_pick",h[e[2]])();return True
				if b is not None:
					if not p["texts"]and not API.HasTarget():p["said"]=(b,time.time())
					return dh(b,button)
				a=aO(x,y)
				if a is None:return False
				j,m,k=C["kinds"][a];i=C["regions"][a]
				if j=="open"and bl(i)and y<i[1]+aU and not API.HasTarget():D("bag_min",k,True)();return True
				return False
			if f=="Right":
				if b is not None:return True
				a=aO(x,y)
				if a is not None and C["kinds"][a][0]=="open":D("bag_close",C["kinds"][a][2])();return True
			return False
		def fb(slot,x,y,hold):
			o,p,a=C["kinds"][slot]
			if not e9(a):di();return
			b=int(Tz.get(hold,"Serial"))
			if b==a:di();return
			import System;c=H.bounds.get(p)if o=="open"else None
			if c is None:Tz.call(None,"DropItem",(System.UInt32(b),65535,65535,0,System.UInt32(int(a)),False),r.Actions);return
			d,e=x,y
			with Kit.quiet:
				if bool(r.p_profile.GetValue(None).RelativeDragAndDropItems):h=Tz.get(hold,"MouseOffset");d,e=d+int(h.X),e+int(h.Y)
			f,g=e2(int(Tz.get(hold,"DisplayedGraphic")));q,s=eS(f,g);i=H.scale or 1.;j=c5(C["regions"][slot]);t,u,v,w=c7(j,q,s);k=max(t,min(u,d));l=max(v,min(w,e));z,A=eR(c,j,f,g,i,k,l);m,n=eP(c,f,g,i,z,A);Tz.call(None,"DropItem",(System.UInt32(b),m,n,0,System.UInt32(int(a)),False),r.Actions);eV(b,int(a),m,n,k,l);safe(lambda:Tz.put(None,"CancelDoubleClick",True,r.Mouse))
		def fc(x,y,button):
			if str(button)!="Left":return False
			a=aO(x,y)
			if a is None:return False
			b,d,c=C["kinds"][a]
			if b in("closed","board"):D("bag_use",c)();return True
			if b=="mini":D("bag_min",c,False)();return True
			return False
		fd={"closed":"Double-click to open; drop an item to put it in","mini":"Double-click to restore; drop an item to put it in","board":"Double-click to open the board; drop an item to put it in","body":"Right-click to close","line":"Click to minimize"}
		def fe(c,x,y):
			a=aO(x,y);b=None
			if a is not None:
				e=C["kinds"][a][0];b=e
				if e=="open":r=C["regions"][a];b="line"if bl(r)and y<r[1]+aU else "body"
			f=(a,b,C["ver"])
			if f==p["tip"]:return
			p["tip"]=f;g=fd.get(b,"")
			if b=="line":
				d=p["label"].get(a)
				if d is not None and d[1]:g="%s. Click to minimize"%d[0]
			c.SetTooltip(g)
		def ff(bag):API.UseObject(bag)
		def fg(bag,value):
			g=H.gumps.get(bag)
			if g is not None and not g.IsDisposed and bool(g.IsMinimized)!=value:g.IsMinimized=value
		def fh(bag):
			g=H.gumps.get(bag)
			if g is not None and not g.IsDisposed:g.Dispose()
		def fi(h,sx,sy):
			try:
				i=p["spot"];c=H.gtr
				for j in C["order"]:
					d=C["kinds"][j]
					if d[0]!="open":continue
					g=H.gumps.get(d[2])
					if g is None:continue
					a=c.get(g)
					if a is None:
						a=g.TextRenderer
						if len(c)>=bL:c.clear()
						c[g]=a
					o=a.DRight
					if o is None:continue
					while o is not None:
						e=o.Owner
						if not o.IsDestroyed and e is not None and o.TextBox is not None:
							try:f=int(e.Serial or 0)
							except Exception:f=0
							b=i.get(f)
							if b is not None:o.X,o.Y=b[0],b[1];k,l=bJ(o.TextBox);o.RealScreenPosition=r.Point(b[0]-(k>>1),b[1]-int(o.OffsetY)-l)
						o=o.DRight
					a.Draw(h,sx,sy,True)
			except Exception as m:p["texts"]=False;H.error="canvas texts: %s"%m
		fj=4.;fk=1.5
		def fl(now):
			if p["texts"]or l["canvas"]is None:return
			a=p["say_lbl"];d=p["said"];e=JR["rd"]
			if d is not None and e is not None:
				i,f=d
				for b in e.new():
					if b.at<f-.05 or ":"in b.text[:24]:continue
					c=p["spot"].get(i);p["said"]=None
					if c is None or p["ctrl"]is None:break
					if a is None:
						g=v.get("grid")
						if g is None:break
						a=Kit.add_label(g,"",0,0,Kit.HUE_TEXT);Kit.flush();de(a);p["say_lbl"]=a
					h=Kit.fit(b.text,200);Kit.set_text(a,h);a.SetPos(max(0,c[0]-Kit.text_w(h)//2),max(0,c[1]-18));a.IsVisible=True;p["say_shown"]=True;p["say_until"]=now+fj;break
				else:
					if now-f>fk:p["said"]=None
			if a is not None and p["say_shown"]and now>=p.get("say_until",0.):p["say_shown"]=False;Kit.set(a,"IsVisible",False)
		def bY():
			h=H.hold
			if h is None:a=Tz.get(None,"Game",Tz.T("ClassicUO.Client"));h=H.hold=Tz.get(Tz.get(a,"UO"),"GameCursor");h=H.hold=Tz.get(h,"ItemHold")
			return None if not bool(Tz.get(h,"Enabled"))or bool(Tz.get(h,"IsFixedPosition"))else h
		aa={"pct":None}
		def bZ():p=aa["pct"];return(p,True)if p is not None and p<l["scale_pct"]else(l["scale_pct"],l["scale_items"])
		def b_():
			if aa["pct"]is None:Kit.put_var(aV,"")
			else:Kit.put_var(aV,"%d|%d"%(l["scale_pct"],1 if l["scale_items"]else 0))
		def b0(pct):
			if pct is not None and not(r.ok and not H.disabled and P()):pct=None
			if pct is not None and aN():pct=None
			if pct is not None and aa["pct"]is None:
				a=safe(cN)
				if a:l["scale_pct"],l["scale_items"]=a
			if pct is not None:
				pct=max(ck,int(pct))
				if pct>=l["scale_pct"]:pct=None
			if pct==aa["pct"]:return
			c=aa["pct"];b=H.scale;aa["pct"]=pct
			try:bi(*bZ())
			except Exception as e:aa["pct"]=c;API.SysMsg(A+": couldn't change the bag scale (%s)."%e,K);return
			b_()
			if b>0 and H.scale>0:f=H.scale/b;l["cell_w"]=max(1,min(an,int(round(l["cell_w"]*f))));l["cell_h"]=max(1,min(an,int(round(l["cell_h"]*f))))
			l["fit_pending"]=True;aq()
			if not(l["job"]or l["sort"]):ab("Idle")
		def fm():
			b=Kit.get_var(aV)
			if not b:return
			p=b.split("|")
			try:a,c=int(p[0]),(len(p)>1 and p[1]=="1")
			except Exception:Kit.put_var(aV,"");return
			if r.ok and 50<=a<=200:
				try:bi(a,c);l["scale_pct"],l["scale_items"]=a,c
				except Exception:return
			Kit.put_var(aV,"")
		def fo(w,h):
			a=(int(w),int(h))if(w is not None and h is not None and P())else None
			if a is None:
				if O["area"]is not None:O["area"]=None;aM(None,None,None);l["dirty_frame"]=True
				return
			if a!=O["area"]:O["area"]=a;aM(a[0],a[1],"w");l["dirty_frame"]=True
		def fp(width,height):
			if not(aN()and P()):return
			c=0 if aP()else aX(max(60,min(int(height),1000)));b=int(width)-c
			if b<40:return
			d=sum(f for g,f,h in c0(c_()));k=(l["scale_pct"]if aa["pct"]is not None else(int(round(H.scale*100))if r.ok else l["scale_pct"]))/100.;a=max(80,int(math.ceil(d*k*k/b)))
			if int(height)<(1<<19):a=min(a,max(1,int(height)))
			return None,a
		def aP():return l["side_hidden"]and not l["minimized"]and P()
		def aB():return 0 if(aA()or P())else ag
		def fq():
			b=l["attach"]
			if b is None:return
			a=b.get("raw")
			if a is None or a.IsDisposed:
				a=at(b.get("g"))if r.ok else None;b["raw"]=a
				if a is not None:Kit.attach(v["grid"],b.get("g"))
			return a
		def fr(info):
			if info is None and l["attach"]is not None:
				safe(lambda:b0(None))
				if O["area"]is not None:O["area"]=None;aM(None,None,None)
				l["frame_x"],l["frame_y"]=l["saved_fx"],l["saved_fy"];l["detached_at"]=time.time();H.bar_at=None
				for a in(l["bar_raw"],l["grid_raw"]):
					with Kit.quiet:
						if a is not None and not a.IsDisposed:az(a,l["frame_x"],l["frame_y"])
				for c in("bar","grid"):
					g=v.get(c)
					if Kit.is_open(g):g.SetPos(l["frame_x"],l["frame_y"]);Kit.moved_by_code(g)
			elif info is not None:
				l["minimized"]=l["docked"]=False;a_(False)
				with Kit.quiet:
					b=info.get("g")
					if Kit.is_open(b)and(info.get("dx")or info.get("dy")):l["frame_x"]=int(b.GetX())+int(info.get("dx",0));l["frame_y"]=int(b.GetY())+int(info.get("dy",0))
			l["attach"]=info;l["dirty_frame"]=True
		def aQ():w,h=Kit.pic_size(cn[0]);return(w or 15),(h or 15)
		def aR(grid,x,y,strip=True):
			if strip:dD(grid,x-4,y+max(0,(aQ()[1]-aT)//2))
			if P():a,b=Kit.ART_DOCK,("Show the side panel"if l["side_hidden"]else "Hide the side panel")
			else:a,b=cn,("Show the title bar and side panel"if l["bare"]else "Bags only: hide the title bar and side panel")
			Kit.art_button(grid,v["store"],"bare",a,x,y,None,b,on_click=D("toggle_bare"))
		def fs(grid,slot_raws,cols,cw,ch,gap,d,c,trim):
			A=max(4,(cw-8)//7);b=O["area"]if P()else None
			if b is not None:Kit.inert(Kit.add_tiled(grid,Kit.SECTION_TILE,0,0,b[0],b[1],Kit.SECTION_ALPHA))
			for f in range(l["slots"]):
				q,j=divmod(f,cols);x,y=j*(cw+gap),q*(ch+gap);B=ak(x,y,cw,ch,"#000000",.01)
				if aA():Kit.set(B,"CanMove",True)
				grid.Add(B);Kit.add_tiled(grid,Kit.SECTION_TILE,x,y,cw,ch,l["opacity"])
				if trim:
					if j<cols-1:grid.Add(Kit.inert(ak(x+cw-1,y,1,ch,aI,.8)))
					if f+cols<l["slots"]:grid.Add(Kit.inert(ak(x,y+ch-1,cw,1,aI,.8)))
				else:
					for s,t,u,w in((x,y,cw,1),(x,y+ch-1,cw,1),(x,y,1,ch),(x+cw-1,y,1,ch)):grid.Add(Kit.inert(ak(s,t,u,w,cy,.9)))
				k=[ao(grid,"#%d"%(f+1),x+5,y+3,Kit.HUE_TITLE)]
				if f in l["assign"]:k.append(ao(grid,ar(ai(l["assign"][f],False),A),x+5,y+21,Kit.HUE_INFO));k.append(ao(grid,"Closed",x+5,y+39,Kit.HUE_INFO))
				else:k.append(ao(grid,ar("Empty: click Slots",A),x+5,y+21,Kit.HUE_INFO))
				slot_raws.append(tuple(at(G)for G in k)if r.ok else());C=ao(grid,"",x+5,y+max(0,ch-18),Kit.HUE_GOOD);Kit.set(C,"IsVisible",False);v["counts"].append((C,x,y,cw,ch))
			if b is not None:
				for f in range(l["slots"],cols*int(math.ceil(l["slots"]/float(cols)))):q,j=divmod(f,cols);Kit.inert(Kit.add_tiled(grid,Kit.SECTION_TILE,j*(cw+gap),q*(ch+gap),cw,ch,l["opacity"]))
			if trim:
				for s,t,u,w in((0,0,d,1),(0,c-1,d,1),(0,0,1,c),(d-1,0,1,c)):grid.Add(Kit.inert(ak(s,t,u,w,cy,.9)))
			if aA():g,h=Kit.pic_size(Kit.CORNER_ART);g,h=(g or 30),(h or 30);m,n=aQ();o,z=d-g+co,c-h+co;Kit.inert(Kit.add_pic(grid,Kit.CORNER_ART,o,z));Kit.catcher(grid,o,z,g,h,lambda*a:None,"Drag to move the bags",movable=True);aR(grid,o-m-3,c+bc);e=o+g;i=max(z+h,c+bc+n);grid.SetRect(l["frame_x"],l["frame_y"],e,i);l["grid_wh"]=(e,i);return e
			if aP():
				m,n=aQ()
				if b is not None:aR(grid,b[0]-m-2,b[1]-n-2);grid.SetRect(l["frame_x"],l["frame_y"],b[0],b[1]);l["grid_wh"]=b;return b[0]
				aR(grid,d-m,c+bc);i=c+bc+n;grid.SetRect(l["frame_x"],l["frame_y"],d,i);l["grid_wh"]=(d,i);return d
			D,p=bR(grid,d+gap,c);l["side_pw"]=gap+D;e=d+gap+D
			if b is not None:e,p=max(e,b[0]),max(p,b[1])
			grid.SetRect(l["frame_x"],l["frame_y"]+aB(),e,max(c,p));l["grid_wh"]=(e,max(c,p));return e
		aZ={"outline":None,"told":False}
		def b1(g):
			try:
				if g is None or g.IsDisposed:return
				x,y=int(g.GetX()),int(g.GetY());w,h=int(g.GetWidth()or 0),int(g.GetHeight()or 0)
			except Exception:return
			return None if w<=1 or h<=1 else(x,y,w,h)
		def ft():
			if l["minimized"]or l["docked"]:return
			a=[]
			if not aA()and not P()and l["canvas"]!="alone":
				r=b1(v["bar"])
				if r is not None:a.append(r)
			r=b1(v["grid"])
			if r is not None:a.append(r)
			if not a:return
			b=min(f[0]for f in a);c=min(g[1]for g in a);d=max(h[0]+h[2]for h in a);e=max(i[1]+i[3]for i in a);return b,c,d-b,e-c
		def fu():
			b=[];c,d=v["bar"],v["grid"]
			for g,a in list(SNAP.links.items()):
				if(a is c or a is d)and a is not None and Kit.is_open(g):
					r=b1(g)
					if r is not None:b.append((g,r))
			return b
		def dj(a,d,b,c,e,f):return f+(a-c)if a>=c-2 or(d>b+2 and abs(d-c)<abs(a-b))else e+(a-b)
		def dk(followers):
			c=SNAP;d=v["grid"]if(aA()or P()or l["canvas"]=="alone")else v["bar"]
			if d is None:d=v["grid"]
			Kit.flush();b=ft();a=aZ["outline"]
			if a is not None:a=(l["frame_x"]+a[0],l["frame_y"]+a[1],a[2],a[3])
			if b is not None:aZ["outline"]=(b[0]-l["frame_x"],b[1]-l["frame_y"],b[2],b[3])
			j=0
			for g,(e,f,m,n)in followers:
				if d is None or not Kit.is_open(g):continue
				c.links[g]=d
				if a is None or b is None or a==b:continue
				h=dj(e,e+m,a[0],a[0]+a[2],b[0],b[0]+b[2]);i=dj(f,f+n,a[1],a[1]+a[3],b[1],b[1]+b[3])
				if(h,i)==(e,f):continue
				try:g.SetPos(int(h),int(i))
				except Exception:continue
				j+=1
				with Kit.quiet:
					if c.last is not None:c.last[g]=(h,i)
					Kit.moved_by_code(g);c.follow(g,h-e,i-f,set([g]))
				k=c.moved_cb.get(g)
				if k is not None:safe(k)
			if j and not aZ["told"]:aZ["told"]=True;API.SysMsg(A+": %s moved with the bags' edge."%Kit.count(j,"snapped window"),T)
		def fv(cols,rows,ch,gap):
			a=Kit.screen()[1]
			if a<=0 or l["slots"]<=1:return cols,rows
			b=max(1,(a-aB()-d2+gap)//(ch+gap))
			if rows<=b:return cols,rows
			c=int(math.ceil(l["slots"]/float(b)));return c,int(math.ceil(l["slots"]/float(c)))
		def fw():
			n=fu();dc();aJ("grid");aJ("bar")
			if l["canvas"]is not None and cW()==l["canvas"]:fx(n);return
			if O["area"]is not None and P()and l["geom"]is not None:aM(O["area"][0],O["area"][1],"w");l["dirty_frame"]=False
			elif O["told"]is not None and not P()and l["geom"]is not None:aM(O["told"][0],O["told"][1],"w");l["dirty_frame"]=False
			c,e=cU();o=bj();d=0 if o else bx;h,f=O["cell"]or(l["cell_w"],l["cell_h"]);i=not P()and l["canvas"]is None and O["told"]is None and not z(S)
			if i and not l["minimized"]:c,e=fv(c,e,f,d)
			s=c*h+(c-1)*d;p=e*f+(e-1)*d;l["geom"]=(c,h,f,d);l["icons_used"]=H.icons or aG;v.update({"store":({},{}),"side_status":None,"search_box":None,"counts":[],"count_state":{}});b=aA();a=G.CreateGump(b,b);v["grid_bare"]=b;l["grid_info"]=(at(a)if r.ok else None,b);q=[]
			if l["minimized"]:g=bA;a.SetRect(l["frame_x"],l["frame_y"]+ag,1,1)
			else:g=fs(a,q,c,h,f,d,s,p,o)
			if i:
				t=g if b else max(g,bA);u=ag if l["minimized"]else aB()+(l["grid_wh"][1]if l["grid_wh"]else p);j,k=Kit.clamp(l["frame_x"],l["frame_y"],t,u)
				if(j,k)!=(l["frame_x"],l["frame_y"]):l["frame_x"],l["frame_y"]=j,k;a.SetPos(j,k+(ag if l["minimized"]else aB()))
			cF(a,True);cG(a);Kit.add_front(a);v["grid"]=a;m=do(g,l["docked"]or b or P(),i)
			if P():l["attach_g"]=l["attach"].get("g");Kit.attach(a,l["attach_g"])
			elif b:Kit.attach(m,a)
			else:Kit.attach(a,m)
			dk(n);l["slot_raws"]=tuple(q)
			if J["counts"]:bs()
			l["grid_raw"]=at(a)if r.ok else None;l["bar_raw"]=at(m)if r.ok else None
			if r.ok and not H.disabled and(l["grid_raw"]is None or l["bar_raw"]is None):H.error="can't reach the client's own window controls";H.disabled=True
		dl="Close "+A+" (turns it off; gives every bag back)";dm="Open the bag manager: a bag per slot";dn="Pick the bags Trap and Untrap cast on"
		def do(e,hide,free=False):
			b=max(e,bA);a=G.CreateGump(True,True)
			if free:Kit.place(a,l["frame_x"],l["frame_y"],b,ag)
			else:a.SetRect(l["frame_x"],l["frame_y"],b,ag)
			Kit.add_window_frame(a,b,ag,corners=False);Kit.add_section(a,8,8,b-16,ag-16);Kit.add_label(a,A.upper(),18,14,Kit.HUE_TITLE);Kit.add_label(a,str(l["slots"]),18+Kit.text_w(A.upper())+8,14,Kit.HUE_INFO);c=v["store"];x=b-12-30
			if Kit.zone_up(S):x+=20
			else:Kit.art_button(a,c,"close",Kit.ART_CLOSE,x,11,None,dl,on_click=D("disable",S));x-=20;Kit.art_button(a,c,"min",Kit.ART_RESTORE if l["minimized"]else Kit.ART_MIN,x,14,None,Kit.RESTORE_TIP if l["minimized"]else Kit.MIN_TIP,on_click=D("user_collapse"));Kit.dock_button(a,c,x,14,on_click=D("fold_to_bar"));x-=Kit.DOCK_DX
			for f,d,g,h in(("settings","Settings",Kit.SETTINGS_TIP%A,D("show_settings",S)),("traps","Trap bags",dn,D("open_win","trp")),("bags","Slots",dm,D("open_win","mgr"))):x-=10+35+Kit.text_w(d);Kit.art_button(a,c,f,Kit.ART_PAGE,x,11,d,g,on_click=h)
			Kit.title_catcher(a,8,8,max(20,x-14),ag-16,D("user_collapse"),key=S)
			if hide:a.IsVisible=False
			Kit.add_front(a);v["bar"]=a;return a
		gR=None
		def dp():
			if l["canvas"]is None or p["ctrl"]is None or C["size"]is None:return
			if p["built"]!=C["ver"]or p["bsize"]!=C["size"]:
				if p["rect"]is not None and(p["rect"][2],p["rect"][3])!=C["size"]:return
				if aY():return
				e_()
			dd();e7()
		def fx(followers):
			i=l["canvas"];b=i=="alone";l["icons_used"]=H.icons or aG;v.update({"store":({},{}),"side_status":None,"search_box":None});e,f,c,g,p=cY(i);W,d=O["told"]if b else O["area"];a=G.CreateGump(b,b);v["grid_bare"]=b;h=at(a);l["grid_info"]=(h,b);j=v["store"];k=b and not l["bare"]and bS(W)
			if b:
				Kit.add_window_frame(a,W,d)
				if k:
					Kit.title_bar(a,j,W,A,S,D("user_collapse"),D("fold_to_bar"),D("show_settings",S),close_tip=dl,extra=[("traps",Kit.ART_PAGE,"Trap bags",dn,D("open_win","trp")),("bags",Kit.ART_PAGE,"Slots",dm,D("open_win","mgr"))],after=str(l["slots"]));m=j[0].get("close")
					if m is not None:Kit.on_click(m,D("disable",S))
			Kit.flush();eZ(h,h.Children.Count,e,f,c,g);n,o=aQ()
			if b:
				l["side_pw"]=0
				if l["bare"]and bS(W):aR(a,e+c-n-2,f+g-o-2)
				elif k and p:l["side_pw"]=bR(a,e+c,g,f)[0]
				else:dD(a,e+c-2,f+g-aT-2)
			elif aP():aR(a,W-n-2,d-o-2);l["side_pw"]=0
			else:l["side_pw"]=bR(a,c,d)[0]
			a.SetRect(l["frame_x"],l["frame_y"],W,d);l["grid_wh"]=(W,d);cF(a,False)
			if not b:cG(a)
			if z(S):a.CanMove=False
			Kit.add_front(a);v["grid"]=a;q=do(W,True)
			if P():l["attach_g"]=l["attach"].get("g");Kit.attach(a,l["attach_g"])
			dk(followers);l["slot_raws"]=();l["grid_raw"]=h;l["bar_raw"]=at(q)if r.ok else None
			if l["grid_raw"]is None:H.error="can't reach the client's own window controls";H.disabled=True;return
			dp()
		def fy():l["minimized"]=not l["minimized"];l["docked"]=False;aq()
		def b2():return U(cA)
		def a_(on):HOST.dock_want_set(cA,on)
		def fz():
			if Kit.zone_up(S):return
			a_(False);fy()
		def dq():
			if Kit.zone_up(S):return
			a_(True);a=I()
			if not l["minimized"]or l["docked"]!=a:l["minimized"],l["docked"]=True,a;aq()
			if not a:HOST.dock_note(A)
		def fA():
			if P():l["side_hidden"]=not l["side_hidden"]
			else:l["bare"]=not l["bare"]
			aq()
		aC={"next":0.}
		def dr():
			a=time.time()
			if a<aC["next"]:return
			aC["next"]=a+.1;b=API.GetSharedVar(bF)
			if b:
				API.RemoveSharedVar(bF);b=str(b)
				if P():
					d=l["attach"].get("cmd")
					if d is not None:safe(lambda:d(b))
				elif b=="show"and(l["minimized"]or l["docked"]):a_(False);l["minimized"]=l["docked"]=False;aq()
				elif b=="dock"and not l["docked"]:dq()
			if P():c=str(l["attach"].get("state")or "open")
			else:
				if l["docked"]:
					if not I():l["docked"]=False;l["dirty_frame"]=True
				elif l["minimized"]and a>=aC.get("wish",0.):
					aC["wish"]=a+.25
					if b2()and I():l["docked"]=True;l["dirty_frame"]=True
				elif not l["minimized"]and a>=aC.get("wish",0.):
					aC["wish"]=a+1.
					if b2():a_(False)
				c="docked"if l["docked"]else("collapsed"if l["minimized"]else "open")
			if c!=l["link_state"]:l["link_state"]=c;API.SetSharedVar(cz,c)
		def fB(value):
			if not r.ok:API.SysMsg(A+": minimizing bags needs client access (%s)."%r.error,K);return
			n=eG(value)or 0;API.SysMsg(A+": %s %s."%("minimized"if value else "restored",Kit.count(n,"bag")),T)
		def fC():
			fD();a=False;b=l["minimized"]or(P()and not l["attach"].get("shown",True))
			for f,i in l["layout"]:
				try:
					c=API.FindItem(i);g=c.GetContainerGump()if c else None
					if not Kit.is_open(g):continue
					try:g.IsVisible=not b
					except Exception:pass
					if b:continue
					d,e=cJ(f)
					if g.GetX()!=d or g.GetY()!=e:g.SetPos(d,e)
					w=g.GetWidth()or 0;h=g.GetHeight()or 0
				except Exception:continue
				if l["cell_w"]<w<=an:l["cell_w"],a=w,True
				if l["cell_h"]<h<=an:l["cell_h"],a=h,True
			if a:aq()
		def ds():
			a=l["attach"].get("g")if P()else None
			if a is not None and a is not l["attach_g"]and Kit.is_open(a)and Kit.is_open(v.get("grid")):l["attach_g"]=a;Kit.attach(v["grid"],a)
		def fD():
			if P():
				b,d=l["attach"].get("g"),l["attach"]
				if not Kit.is_open(b):return
				ds();x=b.GetX()+d.get("dx",0);y=b.GetY()+d.get("dy",0);a=v.get("grid")
				if(x,y)!=(l["frame_x"],l["frame_y"]):
					l["frame_x"],l["frame_y"]=x,y
					if Kit.is_open(a):a.SetPos(x,y);Kit.moved_by_code(a)
				elif Kit.is_open(a)and(int(a.GetX()),int(a.GetY()))!=(x,y):a.SetPos(x,y);Kit.moved_by_code(a)
				return
			b,c,e=(v["grid"],v["bar"],0)if v.get("grid_bare")else(v["bar"],v["grid"],ag)
			if not Kit.is_open(b):return
			x=b.GetX();y=b.GetY()
			if x!=l["frame_x"]or y!=l["frame_y"]:
				l["frame_x"],l["frame_y"]=x,y
				if Kit.is_open(c):c.SetPos(x,y+e);Kit.moved_by_code(c)
		def b3(k):l["open_"+k]=True;l["dirty_"+k]=True;ap()
		bp={"trp":"trap_checks","srt":"rule_checks"}
		def dt(k):
			if k=="trp":aD()
			elif k=="srt":av()
		def fE(k):
			dt(k);bv(k)
			if k in bp:v[bp[k]]=[]
			l["open_"+k]=False;ap()
		def fF(k):dt(k);l[k+"_min"]=not l[k+"_min"];l["dirty_"+k]=True;ap()
		def b4():bw();ap()
		def fG():
			bv("mgr");M,f=Kit.MARGIN,Kit.GAP;w,j,h=480,28,40;i=min(l["slots"]*j+8,430);m=M+30+M if l["mgr_min"]else M+30+f+h+f+i+M;g,d,y=be("mgr",w,m,"BAG MANAGER",D("toggle_win_min","mgr"),D("close_win","mgr"))
			if not l["mgr_min"]:
				e=w-2*M;Kit.add_section(g,M,y,e,h);Kit.art_button(g,d,"fill",Kit.ART_OK,M+12,y+9,"Auto-fill","Put each open bag without a slot in an empty slot",on_click=D("auto_fill"));Kit.art_button(g,d,"clear",Kit.ART_CLOSE,M+200,y+9,"Clear all","Empty every slot",on_click=D("clear_all"));y+=h+f;Kit.add_section(g,M,y,e,i);b=G.CreateGumpScrollArea(M+4,y+4,e-8,i-8);k=e-8-20
				for a in range(l["slots"]):
					c=a*j;Kit.add_label(b,"#%d"%(a+1),6,c+5,Kit.HUE_TITLE)
					if a in l["assign"]:Kit.add_label(b,ar(ai(l["assign"][a]),28),44,c+5)
					else:Kit.add_label(b,"No bag yet: click Set...",44,c+5,Kit.HUE_INFO)
					Kit.art_button(b,d,"set%d"%a,Kit.ART_PLAY,k-165,c+3,"Set...","Target a bag for slot #%d"%(a+1),on_click=D("assign_slot",a));Kit.art_button(b,d,"clr%d"%a,Kit.ART_CLOSE,k-80,c+3,"Clear","Empty slot #%d"%(a+1),on_click=D("clear_slot",a))
				g.Add(b)
			bf("mgr",g,b4)
		def a0():cE();l["dirty_frame"]=True;l["dirty_mgr"]=True;l["dirty_trp"]=True;l["dirty_srt"]=True;bP();al()
		def a1(kind,*a):
			def b(serial):cD.add((kind,)+a+(int(serial or 0),),dup=True)
			L(15,b)
		def fH(idx):API.SysMsg(A+": target a bag for slot #%d."%(idx+1),T);a1("assign_slot_to",idx)
		def fI(idx,target):
			if not target:API.SysMsg(A+": cancelled.",T);return
			b=Kit.find_item(target)
			if not b or not b.IsContainer:API.SysMsg(A+": that isn't a container.",K);return
			a=int(target)
			for k in[c for c,d in l["assign"].items()if d==a]:del l["assign"][k]
			l["assign"][idx]=a;a0()
			if cO(a):API.SysMsg(A+": slot #%d set."%(idx+1),ax)
			else:API.SysMsg(A+": slot #%d set; open the bag to snap it in."%(idx+1),ax)
		def fJ(idx):
			if idx in l["assign"]:del l["assign"][idx];a0()
		def fK():l["assign"]={};a0();API.SysMsg(A+": all slots cleared.",T)
		def fL():
			b=[]
			for c in(safe(lambda:int(API.Backpack),0),safe(lambda:int(API.Bank),0)):
				if not c:continue
				b.append(c)
				for f in API.ItemsInContainer(c,True)or[]:
					if f.IsContainer:b.append(int(f.Serial))
			g=set(l["assign"].values());d=[h for h in range(l["slots"])if h not in l["assign"]];e=0
			for a in b:
				if not d:break
				if a in g or not cO(a):continue
				l["assign"][d.pop(0)]=a;g.add(a);e+=1
			a0()
			if e:API.SysMsg(A+": added %s."%Kit.count(e,"open bag"),ax)
			elif not d:API.SysMsg(A+": no empty slots left.",K)
			else:API.SysMsg(A+": no open bag without a slot found.",T)
		ae={"c":None,"store":({},{}),"next_status":0.}
		def du():
			if l["canvas"]is not None:return "In a zone the bags share it. Items always draw solid."
			return "Slots fit the open bags (%d x %d px). Items always draw solid."%(l["cell_w"],l["cell_h"])
		def fM(g,x,y,w):
			if r.ok and aa["pct"]is None:
				a=safe(cN)
				if a:l["scale_pct"],l["scale_items"]=a
			f=Kit.Form(g,x,y,w,{"slots":l["slots"],"cols":l["cols"],"rows":l["rows"],"scale":l["scale_pct"],"opacity":int(round(l["opacity"]*100)),"trim":l["trim"],"items":l["scale_items"]},dL(w));ae.update({"c":f.c,"store":f.store,"next_status":0.,"seen":{"trim":l["trim"],"items":l["scale_items"]}})
		def dv():ae["c"]=None
		def fN():
			c=ae["c"]
			if c is None:return
			if Kit.was_clicked(ae["store"],"apply"):fQ();return
			for d,g in(("trim",fO),("items",fP)):
				try:a=bool(c[d].IsChecked)
				except Exception:a=None
				if a is not None and a!=ae["seen"][d]:ae["seen"][d]=a;g(a)
			try:v=int(c["opacity"].Value)
			except Exception:v=None
			if v is not None and 10<=v<=100:
				if ae.get("pct_v")!=(v,c["opacity_lbl"]):ae["pct_v"]=(v,c["opacity_lbl"]);Kit.set_text(c["opacity_lbl"],"%d%%"%v)
				b=v/100.
				if abs(b-l["opacity"])>.001:
					e=l["opacity_pending"];l["opacity_pending"]=(b,e[1]+1)if e and e[0]==b else(b,0)
					if l["opacity_pending"][1]>=eb:l["opacity"]=b;l["opacity_pending"]=None;l["dirty_frame"]=True;dd();ap()
				else:l["opacity_pending"]=None
			f=time.time()
			if f>=ae["next_status"]:ae["next_status"]=f+1.;Kit.set_text(c["status"],ar(b5(),64));Kit.set_text(c["size"],du())
		def b5():
			if not r.tried:return "Off: tick "+A+" on the Modules tab"
			if not r.ok:return "No client access: "+r.error
			if H.disabled:return "Trimming stopped after errors: "+H.error
			if l["canvas"]is not None:a="%d open, filling the zone"%H.open_count
			else:a="%d open, %d trimmed"%(H.open_count,len(H.trimmed))
			if l["driving"]:return "Running (script-driven): "+a
			return "Starting"if H.hook_calls==0 else "Running: "+a
		def fO(value):
			f=ae["c"]
			if value and not(r.ok and not H.disabled):
				API.SysMsg(A+": trimming isn't available (%s)."%b5(),K)
				if f:safe(lambda:f["trim"].SetIsChecked(False));ae["seen"]["trim"]=False
				value=False
			if value==l["trim"]:return
			l["trim"]=value;bQ();al();API.SysMsg(A+": trim "+("on."if value else "off."),T)
		def fP(value):
			if value==l["scale_items"]:return
			if not r.ok:API.SysMsg(A+": scaling items needs client access (%s)."%r.error,K);return
			try:
				a=l["scale_items"];l["scale_items"]=value
				try:bi(*bZ())
				except Exception:l["scale_items"]=a;raise
				if aa["pct"]is not None:b_()
				bQ();API.SysMsg(A+": items %s with the bags."%("scale"if value else "don't scale"),T)
			except Exception as e:API.SysMsg(A+": couldn't change the item scaling (%s)."%e,K)
		def bq(field,name,lo,hi):
			a=(safe(lambda:field.Text,"")or "").strip()
			if not a.isdigit()or not(lo<=int(a)<=hi):raise ValueError("%s must be a whole number from %d to %d."%(name,lo,hi))
			return int(a)
		def fQ():
			f=ae["c"]
			if not f:return
			try:a=bq(f["slots"],"Slots",a6,af);b=bq(f["cols"],"Columns",0,af);c=bq(f["rows"],"Rows",0,af);d=bq(f["scale"],"Bag scale",50,200)
			except ValueError as e:API.SysMsg(A+": "+str(e),K);return
			if b>0 and c>0 and b*c<a:API.SysMsg(A+": %d columns x %d rows only fits %d slots, not %d."%(b,c,b*c,a),K);return
			g=[n for n in l["assign"]if n>=a]
			for k in g:del l["assign"][k]
			av()
			for k in[q for q in l["rules"]if q>=a]:del l["rules"][k]
			l["slots"],l["cols"],l["rows"]=a,b,c
			if r.ok and d!=l["scale_pct"]:
				try:
					i=l["scale_pct"];l["scale_pct"]=d
					try:bi(*bZ())
					except Exception:l["scale_pct"]=i;raise
					if aa["pct"]is not None:
						if aa["pct"]>=d:aa["pct"]=None
						b_()
					bQ()
				except Exception as e:API.SysMsg(A+": couldn't change the bag scale (%s)."%e,K)
			a0();j,m=cU();h=A+": %s in %d x %d."%(Kit.count(a,"slot"),j,m)
			if g:h+=" Released %s from removed slots."%Kit.count(len(g),"bag")
			API.SysMsg(h,ax);dv();o(S)
		def b6():
			a=[]
			for s in[l["assign"][b]for b in sorted(l["assign"])]+l["trap_extra"]:
				if s not in a:a.append(s)
			return a
		def aD():
			a=v["trap_checks"]
			if not a or not Kit.is_open(v["trp"]):return
			for b,c in a:
				if safe(lambda:c.IsChecked,False):l["trap_sel"].add(b)
				else:l["trap_sel"].discard(b)
		def fR():
			aD();bv("trp");f=b6();M,b=Kit.MARGIN,Kit.GAP;w,i,h,j=480,28,40,52;d=min(max(1,len(f))*i+8,400);p=(M+30+M if l["trp_min"]else M+30+b+h+b+d+b+j+M);g,k,y=be("trp",w,p,"TRAP BAGS",D("toggle_win_min","trp"),D("close_win","trp"));m=[]
			if not l["trp_min"]:
				c=w-2*M;Kit.add_section(g,M,y,c,h);Kit.buttons(g,k,M+12,y+9,(("all",Kit.ART_OK,"Tick all","Tick every bag",D("select_all_traps",True)),("none",Kit.ART_CLOSE,"Untick all","Untick every bag",D("select_all_traps",False)),("add",Kit.ART_PLAY,"Add bag...","Target a bag without a slot to add it",D("add_trap_bag"))),16);y+=h+b;Kit.add_section(g,M,y,c,d);e=G.CreateGumpScrollArea(M+4,y+4,c-8,d-8);q=c-8-20
				if not f:Kit.add_label(e,"No bags yet. Fill the slots, or click Add bag...",6,6,Kit.HUE_INFO)
				for n,a in enumerate(f):
					o=n*i;r=Kit.add_check(e,ar(ai(a),32),6,o+4,a in l["trap_sel"],"Ticked: Trap and Untrap cast on this bag");m.append((a,r))
					if a in l["trap_extra"]and a not in l["assign"].values():Kit.art_button(e,k,"rm%d"%n,Kit.ART_CLOSE,q-110,o+3,"Remove","Take this bag off",on_click=D("remove_trap_bag",a))
				g.Add(e);y+=d+b;Kit.add_section(g,M,y,c,j);Kit.add_label(g,"Tick bags, then Trap or Untrap on the side panel.",M+12,y+8,Kit.HUE_INFO);Kit.add_label(g,"A trapped bag explodes on whoever opens it, you included.",M+12,y+28,Kit.HUE_BAD)
			bf("trp",g,b4,trap_checks=m)
		def b7():v["trap_checks"]=[];l["dirty_trp"]=True;al()
		def fS(value):l["trap_sel"]=set(b6())if value else set();b7()
		def fT():aD();API.SysMsg(A+": target a bag to add to the trap list.",T);a1("add_trap_bag_to")
		def fU(target):
			if not target:return
			aD();b=Kit.find_item(target)
			if not b or not b.IsContainer:API.SysMsg(A+": that isn't a container.",K);return
			a=int(target)
			if a not in l["trap_extra"]:l["trap_extra"].append(a)
			l["trap_sel"].add(a);b7()
		def fV(serial):
			aD()
			if serial in l["trap_extra"]:l["trap_extra"].remove(serial)
			l["trap_sel"].discard(serial);b7()
		def fW(spell):
			aD();al()
			if l["job"]:API.SysMsg(A+": already casting %s; press Stop first."%l["job"]["spell"],K);return
			if l["sort"]:API.SysMsg(A+": busy sorting; press Stop first.",K);return
			a=[b for b in b6()if b in l["trap_sel"]]
			if not a:API.SysMsg(A+": tick bags in the Trap bags window first.",K);b3("trp");return
			l["job"]={"spell":spell,"queue":a,"i":0,"phase":"mana","t":0.,"tries":0,"done":0,"failed":0,"warned":False,"cast":0.};l["dirty_trp"]=True;ab("Starting");API.SysMsg(A+": casting %s on %s."%(spell,Kit.count(len(a),"bag")),T)
		def a2(user=False):
			if l["job"]:
				a=l["job"]
				if a.get("phase")=="target"and time.time()-a.get("cast",0.)>=ct and R(S,"neutral"):API.CancelTarget()
				E(S)
				if user:API.SysMsg(A+": %s stopped."%l["job"]["spell"],T);ab("Stopped")
			l["job"]=None;l["dirty_trp"]=True
		def dw():
			b=bool(l["job"]or l["sort"])
			for a in v.get("stop_ctrls")or():
				if a is not None:Kit.set(a,"IsVisible",b)
		def ab(text):
			if text=="Idle":p=aa["pct"];text=("Shown at %d%% to fit"%p)if p is not None and p<l["scale_pct"]else ""
			dw()
			if text==l["status_text"]:return
			l["status_text"]=text;a=v.get("side_status")
			if a is not None:Kit.set_text(a,text)
		fX=tuple((gT,tuple(gV.lower()for gV in gU))for gT,gU in(("reagents",ej),("mana",ek),("fizzle",eh),("busy",ei)))
		def dx(j):
			c=j.get("jr")
			if c is None:return
			a=j["jt"]
			for b in c.new():
				if b.text and not b.text.startswith(A):a.append(b.low)
			if not a:return
			for d,e in fX:
				if any(f in g for f in e for g in a):return d
			return
		def b8(j,a):
			if a:j["done"]+=1
			else:j["failed"]+=1
			j["i"]+=1;j["tries"]=0;j["phase"]="mana"
		def b9(j,now,a):
			j["tries"]+=1
			if j["tries"]>eg:API.SysMsg(A+": giving up on %s (%s)."%(ai(j["queue"][j["i"]],False),a),K);b8(j,False)
			else:j["phase"]="pause";j["t"]=now+ef
		def fY():
			j=l["job"]
			if not j:return
			a=time.time()
			if j["i"]>=len(j["queue"]):API.SysMsg(A+": %s finished: %d done, %d failed."%(j["spell"],j["done"],j["failed"]),ax if not j["failed"]else K);ab("Done %d/%d"%(j["done"],len(j["queue"])));a2();return
			d=j["queue"][j["i"]];e=j["phase"]
			if e=="pause":
				if a>=j["t"]:j["phase"]="mana"
				return
			if e=="mana":
				c=HOST.fight_hold(a)or HOST.guard_hold()
				if c:
					if j.get("held")!=c:j["held"]=c;f=HOLD_TEXT.get(c,c);API.SysMsg(A+": %s waits (%s)."%(j["spell"],f[:1].lower()+f[1:]),T);ab(f if c=="unknown"else "Paused: "+f)
					return
				if j.get("held"):j["held"]=None;ab("Starting")
				g=API.Player.Mana
				if g<cq:
					if not j["warned"]:API.SysMsg(A+": waiting for mana (%d/%d)."%(g,cq),T);ab("Need mana");j["warned"]=True
					return
				j["warned"]=False
				if not Kit.find_item(d):API.SysMsg(A+": bag 0x%08X is out of reach; skipping it."%d,K);b8(j,False);return
				if bN():ab("Cursor busy");return
				if API.HasTarget("any"):ab("Cursor busy");return
				API.SysMsg(A+": %s %d/%d: %s."%(j["spell"],j["i"]+1,len(j["queue"]),ai(d,False)),T);ab("%s %d/%d"%("Untrap"if "Untrap"in j["spell"]else "Trap",j["i"]+1,len(j["queue"])));j["cast"]=time.time();j["jr"],j["jt"]=Z(),[];HOST.claim_cursor(S,cr+.5);API.CastSpell(j["spell"]);j["phase"]="target";j["t"]=a;return
			if e=="target":
				b=dx(j)
				if b:E(S)
				if b=="reagents":API.SysMsg(A+": out of reagents for %s."%j["spell"],K);a2();return
				if b=="mana":j["phase"]="mana";return
				if b in("fizzle","busy"):b9(j,a,b);return
				if a-j["cast"]>=ct and R(S,"neutral"):API.Target(d);E(S);j["phase"]="recover";j["t"]=a
				elif a-j["t"]>cr:E(S);b9(j,a,"no target cursor")
				return
			if e=="recover":
				if a-j["t"]<ee:return
				b=dx(j)
				if b=="reagents":API.SysMsg(A+": out of reagents for %s."%j["spell"],K);a2()
				elif b in("fizzle","busy","mana"):b9(j,a,b)
				else:b8(j,True)
		def ca(it,hue):
			try:it.SetHue(int(hue)&65535);return True
			except Exception:return False
		def cb(it):
			try:return int(it.Hue or 0)
			except Exception:return-1
		J={"text":"","typed":0.,"armed":False,"lit":{},"until":0.,"counts":{},"restored":{},"tiles":{},"status":None,"texts":{},"texts_at":0.,"objs":{}}
		def fZ(q):
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
		def f_(raw):
			if "%"not in raw:return raw
			a,b=[],[]
			for i,p in enumerate(raw.split("%")):
				if i%2==0:a.append(p);b.append(p)
				else:c,e,d=p.partition("/");a.append(d);b.append(c)
			return "".join(a)+" "+"".join(b)
		def cc(it,graphic):
			a=J["tiles"];t=a.get(graphic)
			if t is None:
				d=it.GetItemData();b=str(d.Name or "")if d is not None else "";t=f_(b).lower()
				if len(a)>=eo:a.clear()
				a[graphic]=t
			return t
		def f0(it,serial,graphic):
			a=J["texts"];t=a.get(serial)
			if t is not None:return t+"\n"+cc(it,graphic)
			t=API.ItemNameAndProps(serial)or ""
			if t:
				t=str(t).lower()
				if "\n"in t and len(a)<bD:a[serial]=t
				return t+"\n"+cc(it,graphic)
			return str(it.Name or "").lower()+"\n"+cc(it,graphic)
		def f1(x):
			o=set(G for W,G in l["layout"]);d,p={},{};q={};g=0
			for h,e in l["layout"]:
				if g>=bD:break
				r=API.ItemsInContainer(e,True)or[];i={};f=[]
				for b in r:
					try:s=int(b.Serial)
					except Exception:f.append(None);continue
					f.append(s)
					try:i[s]=int(b.Container)
					except Exception:pass
				n=0
				for t in range(len(f)):
					if g>=bD:break
					g+=1;a=f[t]
					if a is None or a in o:continue
					j,c,u=a,i.get(a,e),0
					while c!=e and u<en and c not in o:j,c=c,i.get(c,e);u+=1
					if c!=e:continue
					b=r[t]
					try:v=int(b.Graphic)
					except Exception:continue
					k=None;m=False
					for y,w in x:
						if w is not None:
							if v==w:m=True;break
						else:
							if k is None:k=f0(b,a,v)
							if y in k:m=True;break
					if not m:continue
					n+=1
					if len(d)<bE:
						d[a]=h;q[a]=b
						if j!=a and len(d)<bE:d[j]=h
				if n:p[h]=n
			J["objs"]=q;return d,p
		def dy(serial):a=J["objs"].get(serial);return a if a is not None else API.FindItem(serial)
		def f2(serial,now):
			a=dy(serial)
			if not a:return False
			b=cb(a)
			if b<0:return False
			d=b
			if b==aw:
				c=J["restored"].get(serial)
				if c is not None and now-c[1]<cu:d=c[0]
			if not ca(a,aw):return False
			bW(serial,aw);J["lit"][serial]=d;return True
		def dz(serial,orig,now):
			a=API.FindItem(serial)
			if not a:return
			b=cb(a)
			if b==aw or b==orig:
				if ca(a,orig):bW(serial,orig)
				J["restored"][serial]=(orig,now)
		def f3(now):
			a=J["restored"]
			if a:
				for s in[b for b,c in a.items()if now-c[1]>=cu]:del a[s]
				if len(a)>2*bE:a.clear()
		def f4(q,now):
			c=fZ(q)
			if not c:br(now);return
			f3(now)
			if not 0<=now-J["texts_at"]<=bC:J["texts"]={};J["texts_at"]=now
			d,e=f1(c);b=J["lit"]
			for a in[h for h in b if h not in d]:dz(a,b.pop(a),now)
			try:
				for a in d:
					if a not in b:f2(a,now)
					else:f5(a)
			finally:J["objs"]={}
			J["counts"]=e;J["until"]=now+bC;bs();f=sum(e.values());g=("%d found"%f)if f else "None found";J["status"]=g;ab(g)
		def f5(serial):
			a=dy(serial)
			if not a:return
			b=cb(a)
			if 0<=b!=aw and ca(a,aw):bW(serial,aw);J["lit"][serial]=b
		def br(now):
			a=J["lit"]
			for b in list(a):dz(b,a.pop(b),now)
			J["texts"]={};J["texts_at"]=0.;J["until"]=0.
			if J["counts"]:J["counts"]={};bs()
			if J["status"]is not None:
				if l["status_text"]==J["status"]:ab("Idle")
				J["status"]=None
		def bs():
			e=J["counts"];d=v["count_state"]
			for b,(c,x,y,f,g)in enumerate(v["counts"]):
				n=e.get(b,0);a=("%d found"%n)if n else ""
				if d.get(b)==a:continue
				d[b]=a
				try:
					if n:c.SetPos(x+max(5,f-5-Kit.text_w(a)),y+max(0,g-18));Kit.set_text(c,a)
					c.IsVisible=bool(n)
				except Exception:pass
		def f6(now):
			b=v["search_box"]
			if b is not None and not(l["minimized"]or l["docked"]):
				try:a=b.Text
				except Exception:a=None
				if a is not None:
					a=str(a)
					if a!=J["text"]:J["text"],J["typed"],J["armed"]=a,now,True
			if J["armed"]:
				if now-J["typed"]>=el:
					J["armed"]=False;q=J["text"].strip()
					if len(q)>=em:f4(q,now)
					elif J["lit"]or J["counts"]:br(now)
			elif J["until"]and now>=J["until"]:br(now)
		def f7(grid,a,y):b=Kit.text_w("Find:")+6;ao(grid,"Find:",a+2,y+3,Kit.HUE_TEXT);c=Kit.add_textbox(grid,J["text"],a+2+b,y,a8-4-b,numbers=False);c.SetTooltip("Item name part or graphic (0x0F7A, 3962); commas for several. Matches light up for %d s"%int(bC));v["search_box"]=c;Kit.art_button(grid,v["store"],"rules",Kit.ART_PAGE,a,y+28,"Rules","Open Sort rules: what each slot's bag holds",on_click=D("open_win","srt"));Kit.art_button(grid,v["store"],"filters",Kit.ART_PAGE,a,y+52,"Filters","Open Sort filters: items or presets and their bags",on_click=D("open_filters"))
		dA="Sort items into their bags once; picking up or Stop ends it";a3=(("q_restock","Restock",Kit.ART_PLAY,3702,"restock","Top up supplies once from the Restock chest or bank","restock.run"),("q_sort","Sort",Kit.ART_PLAY,3705,None,dA,None),("q_storage","Storage",Kit.ART_PAGE,3648,"storage","Open or raise the Storage window","storage.show"),("q_supplies","Supplies",Kit.ART_PAGE,3962,"supplies","Open or raise the Supplies table","supplies.open"))
		def aS(part):return part is None or X(part,"inventory")
		def dB(part,tip):
			if aS(part):return tip
			return("%s is off: tick Inventory > %s on the Modules tab"%(part.title(),part.title()))
		def f8(key):
			for k,a,e,f,b,g,d in a3:
				if k!=key:continue
				if b is None:dF();return
				c=HOST.services.get(d)if aS(b)else None
				if c is None:API.SysMsg("%s: %s is off; tick Inventory > %s on the Modules tab."%(A,a,a),T);return
				c();return
		def cd():return tuple(aS(a[4])for a in a3)
		def f9(grid,b,y):
			v["quick_sig"]=cd()
			for i,(k,c,d,f,a,e,g)in enumerate(a3):Kit.art_button(grid,v["store"],k,d,b,y+i*24,c,dB(a,e),hue=None if aS(a)else Kit.HUE_INFO,on_click=D("quick_press",k))
		aT=18;dC=22
		def dD(grid,c,y):
			v["quick_sig"]=cd();x=c-len(a3)*dC
			for i,(k,d,g,e,b,f,h)in enumerate(a3):
				with Kit.quiet:
					a=G.CreateGumpItemPic(e,aT,aT);a.SetRect(x+i*dC,y,aT,aT)
					if not aS(b):Kit.set(a,"Hue",Kit.HUE_INFO)
					Kit.set(a,"DrawBorder",False);t=dB(b,f);a.SetTooltip(t if not aS(b)else d+": "+t);G.AddControlOnClick(a,D("quick_press",k));grid.Add(a)
		ga=dict((gW,frozenset(gX))for gW,gY,gX in F);a4=(frozenset(),())
		def gb(idx):
			b,c=l["rules"].get(idx,a4);a=set(c)
			for k in b:a|=ga.get(k,frozenset())
			return a
		def gc(serial):
			s=int(serial or 0)
			for b in range(12):
				a=API.FindItem(s)
				if a is None:return False
				if int(a.Graphic or 0)==8198 or a.IsCorpse:return True
				c=int(a.Container or 0)
				if not c or c==0xFFFFFFFF or c<0x40000000:return False
				s=c
			return False
		def dE():
			h=[w for w in l["filters"]if w["on"]and w["slot"]is not None and w["set"]];b={}
			for a,c in l["layout"]:
				n=gb(a)
				if n:b[a]=n
			if not b and not h:return
			i={}
			for a in sorted(b):
				for o in b[a]:
					if o not in i:i[o]=a
			p=dict((y,x)for x,y in l["layout"]);d=[];q=safe(lambda:int(API.Backpack),0)
			if q:d.append(q)
			for u,c in l["layout"]:
				if c not in d and not gc(c):d.append(c)
			j=[]
			for e in d:
				s=b.get(p.get(e),())
				for f in API.ItemsInContainer(e,False)or[]:
					if len(j)>=ep:break
					try:r,k=int(f.Serial),int(f.Graphic)
					except Exception:continue
					if r in p:continue
					a=None
					if h:
						t=int(f.Hue or 0)&16383
						for g in h:
							if k in g["set"]and(g["hue"]is None or g["hue"]==t):a=g["slot"];break
					if a is None:
						a=i.get(k)
						if a is None or k in s:continue
					if f.IsContainer:continue
					m=l["assign"].get(a)
					if m and m!=e:j.append((r,e,m,a))
			return j
		def dF():
			av()
			if l["sort"]:API.SysMsg(A+": already sorting; press Stop first.",K);return
			if l["job"]:API.SysMsg(A+": busy with %s; press Stop first."%l["job"]["spell"],K);return
			a=dE()
			if a is None:API.SysMsg(A+": no sort rules yet; tick what each bag holds in Sort rules.",K);b3("srt");return
			if not a:API.SysMsg(A+": nothing to sort; every ruled item is in its bag.",T);ab("Nothing to sort");return
			l["sort"]={"plan":a,"i":0,"move":None,"check":None,"at":0.,"hold":0.,"moved":0,"refused":0,"streak":0,"rechecks":0,"waits":0,"why":None,"last":0,"sent_at":0.};ab("Sort 0/%d"%len(a));API.SysMsg(A+": sorting %s."%Kit.count(len(a),"item"),T)
		def gd(s,now):
			e,f,b,g=s["check"];c=s["sent_at"]
			if B(c,er)is not None:am("bag #%d (%s) is full"%(g+1,ai(b,False)));return False
			d=API.FindItem(e);a=int(d.Container)if d else None
			if a is None and s["rechecks"]<cx and not ge(s,b):s["rechecks"]+=1;s["at"]=now+aH*.5;return False
			if a is None or a==b:s["moved"]+=1;s["streak"]=s["rechecks"]=s["waits"]=0;s["check"]=None;return True
			if(a==f and B(c,es)is not None and s["waits"]<cv):s["waits"]+=1;s["i"]-=1;s["check"]=None;s["rechecks"]=0;s["hold"]=now+aH;return False
			if s["rechecks"]<cx:s["rechecks"]+=1;s["at"]=now+aH*.5;return False
			s["check"]=None;s["rechecks"]=0;s["refused"]+=1;s["streak"]+=1
			if s["streak"]>=cv:am("%d moves in a row were refused"%s["streak"]);return False
			return True
		def dG(bag,graphic,deep=None):
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
		def ge(s,bag):a=s.get("pre");return True if not a or not a[0]else dG(bag,a[0])>=a[2]+a[1]
		def gf(now):
			s=l["sort"]
			if s is None:return
			if s["move"]is not None:return
			if s["why"]:am(s["why"]);return
			if s["check"]is not None:
				if now<s["at"]or not gd(s,now):return
			if now<s["hold"]:return
			if bN():am("another target cursor is in use");return
			h=Kit.held_item()
			if h and not(h==s["last"]and now-s["sent_at"]<2*aH):am("you picked something up");return
			d=s["plan"]
			while s["i"]<len(d):
				e,f,a,b=d[s["i"]];s["i"]+=1;c=API.FindItem(e);j=int(c.Container)if c else 0
				if j!=f:continue
				if l["assign"].get(b)!=a:continue
				if not Kit.find_item(a):am("slot #%d's bag is out of reach"%(b+1));return
				g=API.ItemsInContainer(a,True)or[];k=len(g)
				if k>=eq:am("bag #%d (%s) is full"%(b+1,ai(a,False)));return
				s["move"]=(e,f,a,b);i=int(c.Graphic or 0);s["pre"]=(i,int(c.Amount or 1),dG(a,i,g));ab("Sort %d/%d"%(s["i"],len(d)));return
			gh()
		def gg():
			s=l["sort"]
			if s is None or s["move"]is None:return
			a=s["move"];s["move"]=None
			if l["shutting"]:return
			if bN():s["why"]="another target cursor is in use";return
			if Kit.held_item():s["why"]="you picked something up";return
			try:API.MoveItem(a[0],a[2])
			except Exception as e:s["why"]="a move failed (%s)"%e;return
			V();s["check"]=a;s["last"]=a[0];s["sent_at"]=time.time();s["at"]=s["sent_at"]+aH
		def gh():
			s,l["sort"]=l["sort"],None
			if s is None:return
			a="%d moved"%s["moved"]
			if s["refused"]:a+=", %d refused"%s["refused"]
			API.SysMsg(A+": sort done: %s."%a,K if s["refused"]else ax);ab("Sorted %d"%s["moved"])
		def am(why=None,user=False):
			s,l["sort"]=l["sort"],None
			if s is None:return
			if user:API.SysMsg(A+": sort stopped (%d moved)."%s["moved"],T);ab("Stopped")
			elif why:API.SysMsg(A+": sort stopped: %s (%d moved)."%(why,s["moved"]),K);ab("Sort stopped")
		def gi():a2(True);am(user=True)
		dH="UnifiedBag_filters";ce=40;bt=("exact","kind","category");gj={"exact":"this exact item","kind":"this kind","category":"its category"}
		def gk():
			l["filters"]=[]
			for c in str(Kit.get_var(dH,"")or "").split(";"):
				p=c.split("~")
				if len(p)<5 or len(l["filters"])>=ce:continue
				try:d=int(p[3])if p[3]!=""else None;f=int(p[2])if p[2]!=""else None;b=tuple(int(h,16)for h in p[1].split(",")if h and not h.startswith("@"))
				except ValueError:continue
				g=p[1][1:]if p[1].startswith("@")else None;a=None
				if len(p)>=7 and ":"in p[5]:
					try:a=(int(p[5].split(":",1)[0],16),int(p[5].split(":",1)[1]))
					except ValueError:a=None
				l["filters"].append({"name":p[0],"gr":b,"cat":g,"hue":f,"slot":d,"on":p[4]=="1","set":frozenset(b),"base":a,"broad":p[6]if len(p)>=7 and p[6]in bt else None})
			e["wanted"]=e["wanted"]or any(i["cat"]for i in l["filters"])
		def aE():Kit.put_var(dH,";".join("~".join((a["name"].replace(";"," ").replace("~"," "),"@"+a["cat"]if a["cat"]else ",".join("%X"%b for b in a["gr"]),""if a["hue"]is None else str(a["hue"]),""if a["slot"]is None else str(a["slot"]),"1"if a["on"]else "0","%X:%d"%a["base"]if a.get("base")else "",a.get("broad")or ""))for a in l["filters"]));l["dirty_flt"]=l["open_flt"]
		def a5():
			a=e["data"]
			if a is None:return
			for f in l["filters"]:
				if f["cat"]:f["set"]=a.get(f["cat"],frozenset())
		def gl():e["wanted"]=True;l["open_flt"]=True;l["dirty_flt"]=True
		def gm():bu();aJ("flt");l["open_flt"]=False;v["flt_checks"]=[]
		def bu():
			g=v.get("flt")
			if Kit.is_open(g):l["flt_x"],l["flt_y"]=int(g.GetX()),int(g.GetY())
		def gn():bu();l["flt_min"]=not l["flt_min"];l["dirty_flt"]=True
		def dI(name,gr,hue,cat=None,broad=None):
			if len(l["filters"])>=ce:API.SysMsg(A+": %d filters is the most; remove one first."%ce,K);return
			f={"name":name,"gr":tuple(gr),"cat":cat,"hue":hue,"slot":None,"on":True,"set":frozenset(gr),"broad":broad};l["filters"].append(f);a5();aE();return f
		def go(key):
			for k,a in m:
				if k==key:
					for f in l["filters"]:
						if f["cat"]==key:API.SysMsg(A+": %s is already on the list."%a,T);return
					dI(a,(),None,key)
		def gp():API.SysMsg(A+": target an item for the new filter.",T);a1("filter_targeted")
		def dJ(target):
			if not target:API.SysMsg(A+": cancelled.",T);return
			a=Kit.find_item(target)
			if not a:API.SysMsg(A+": that isn't an item.",K);return
			if a.IsContainer:API.SysMsg(A+": bags aren't sorted; target an item.",K);return
			return a
		def gq(target):
			a=dJ(target)
			if a:dK(int(a.Graphic),int(a.Hue or 0)&16383,str(a.Name or ""))
		def dK(graphic,hue,name):
			if not name:t=bX(graphic);name=str(t.Name or "")if t is not None else ""
			dI((name or "0x%04X"%graphic)[:30],(graphic,),hue,None,"exact")
		def gs():
			a=safe(bY)
			if a is None:return
			try:d=int(Tz.get(a,"Serial"));c=int(Tz.get(a,"Graphic"));e=int(Tz.get(a,"Hue"))&16383;b=int(Tz.get(a,"Container"))
			except Exception:return
			if safe(lambda:bool(bX(c).IsContainer),False):API.SysMsg(A+": bags aren't sorted; drop an item.",K);return
			dK(c,e,"")
			if b and b!=0xFFFFFFFF:import System;Tz.call(None,"DropItem",(System.UInt32(d),65535,65535,0,System.UInt32(b),False),r.Actions)
		def gt(i):
			if not 0<=i<len(l["filters"]):return
			f=l["filters"][i]
			if f.get("base")is None and f["gr"]:f["base"]=(f["gr"][0],f["hue"]or 0)
			a=f.get("base")
			if a is None:return
			d=(f.get("broad")or("category"if f["cat"]else("exact"if f["hue"]is not None else "kind")));b=bt[(bt.index(d)+1)%len(bt)]
			if b=="category":
				c=aj(a[0])
				if c is None:b="exact"
				else:f.update({"cat":c,"hue":None,"gr":(a[0],)})
			if b!="category":f.update({"cat":None,"hue":a[1]if b=="exact"else None,"gr":(a[0],),"set":frozenset((a[0],))})
			f["broad"]=b;a5();aE()
		def gu(i,d):
			j=i+d
			if 0<=i<len(l["filters"])and 0<=j<len(l["filters"]):l["filters"][i],l["filters"][j]=l["filters"][j],l["filters"][i];aE()
		def gv(i):
			if 0<=i<len(l["filters"]):del l["filters"][i];aE()
		def gw(i):
			if not 0<=i<len(l["filters"]):return
			l["flt_pick"]=l["filters"][i];API.SysMsg(A+": click a bag on the bags display, or target a bag in a slot.",T);a1("filter_bag_targeted",l["flt_pick"])
		def gx(f,target):
			if l["flt_pick"]is not f:return
			l["flt_pick"]=None
			if not target:return
			a=dict((g,d)for d,g in l["layout"]);s=int(target)
			for c in range(8):
				if s in a:f["slot"]=a[s];aE();return
				b=Kit.find_item(s);s=int(b.Container or 0)if b else 0
				if not s:break
			API.SysMsg(A+": that isn't in a bag slot; put the bag in a slot first (Slots).",K)
		def gy(a):
			f,l["flt_pick"]=l["flt_pick"],None
			if f is None:return False
			f["slot"]=a;aE();API.CancelTarget();return True
		def gz():
			for i,b in v.get("flt_checks")or():
				if i<len(l["filters"]):
					a=bool(safe(lambda:b.IsChecked,l["filters"][i]["on"]))
					if a!=l["filters"][i]["on"]:l["filters"][i]["on"]=a;aE();return
		def gA():
			bu();aJ("flt");a5();M,e=Kit.MARGIN,Kit.GAP;q=len(l["filters"]);k,n,o=28,30+3*26+8,40;j=max(k*2,min(q,12)*k+8);w=640;B=(M+30+M if l["flt_min"]else M+30+e+o+e+n+e+j+M);g,c,y=be("flt",w,B,"SORT FILTERS",D("toggle_flt_min"),D("close_filters"));r=[]
			if not l["flt_min"]:
				d=w-2*M;Kit.add_section(g,M,y,d,o);Kit.art_button(g,c,"sort",Kit.ART_PLAY,M+12,y+9,"Sort",dA,on_click=D("start_sort"));s=safe(dE);C=len(s)if s else 0;Kit.add_label(g,"%s would move"%Kit.count(C,"item"),M+100,y+12,Kit.HUE_INFO);y+=o+e;Kit.add_section(g,M,y,d,n,"ADD A FILTER");E=M+12;Kit.art_button(g,c,"add",Kit.ART_PLAY,E,y+28,"Add by target...","Target an item: the filter fills in from it",on_click=D("filter_by_target"));p=5;t=(d-24)//p
				for u,(x,h)in enumerate(m):F,H=(u+1)%p,(u+1)//p;Kit.art_button(g,c,"pre_"+x,Kit.ART_OK,M+12+F*t,y+28+H*26,Kit.fit(h,t-40),"Add the %s preset"%h.lower(),on_click=D("filter_preset",x))
				y+=n+e;Kit.add_section(g,M,y,d,j);Kit.catcher(g,M,y,d,j,D("filter_dropped"),"Drop an item here to add a filter")
				if not q:Kit.add_label(g,"No filters yet. Press a preset, or Add by target.",M+12,y+8,Kit.HUE_INFO)
				else:
					a=G.CreateGumpScrollArea(M+4,y+4,d-8,j-8)
					for i,f in enumerate(l["filters"]):
						b=i*k;I=Kit.add_check(a,"",4,b+3,f["on"],"Use this filter (unticked: kept, moves nothing)");r.append((i,I));Kit.add_label(a,Kit.fit(f["name"],150),30,b+5);z=f.get("broad")or("category"if f["cat"]else("exact"if f["hue"]is not None else "kind"))
						if f["cat"]and not f.get("base"):Kit.add_label(a,"A preset",186,b+5,Kit.HUE_INFO)
						else:Kit.art_button(a,c,"m%d"%i,Kit.ART_PAGE,186,b+2,"Match: "+z,"Matches %s; click for the next"%gj[z],on_click=D("filter_broader",i))
						if f["slot"]is None or f["slot"]not in l["assign"]:h,A="No bag",Kit.HUE_BAD
						else:h,A=(ar(ai(l["assign"][f["slot"]],False),14),Kit.HUE_TEXT)
						Kit.add_label(a,h,330,b+5,A);Kit.art_button(a,c,"b%d"%i,Kit.ART_PLAY,424,b+2,"Bag...","Click a bag on the bags display, or target a bag in a slot",on_click=D("filter_pick_bag",i));Kit.art_button(a,c,"u%d"%i,Kit.ART_PAGE,508,b+2,None,"Move up (the first match wins)",on_click=D("filter_move",i,-1));Kit.art_button(a,c,"d%d"%i,Kit.ART_PAGE,536,b+2,None,"Move down (the first match wins)",on_click=D("filter_move",i,1));Kit.art_button(a,c,"x%d"%i,Kit.ART_CLOSE,564,b+2,None,"Remove this filter",on_click=D("filter_remove",i))
					g.Add(a)
			bf("flt",g,bu);v["flt_checks"]=r
		cf={"sync_at":0.}
		def av():
			d=v["rule_checks"]
			if not d or not Kit.is_open(v["srt"]):return False
			e,f={},set()
			for a,g,m in d:
				if a>=l["slots"]:continue
				f.add(a)
				try:h=bool(m.IsChecked)
				except Exception:h=g in l["rules"].get(a,a4)[0]
				if h:e.setdefault(a,set()).add(g)
			i=False
			for a in f:
				b=l["rules"].get(a);j=b[1]if b is not None else();k=frozenset(e.get(a,()));c=(k,j)if(k or j)else None
				if c!=b:
					i=True
					if c is None:del l["rules"][a]
					else:l["rules"][a]=c
			return i
		def gB():
			av();bv("srt");M,d=Kit.MARGIN,Kit.GAP;w,n,j,o=580,52,40,52;f=min(l["slots"]*n+8,430);r=(M+30+M if l["srt_min"]else M+30+d+j+d+f+d+o+M);g,h,y=be("srt",w,r,"SORT RULES",D("toggle_win_min","srt"),D("close_win","srt"));p=[]
			if not l["srt_min"]:
				e=w-2*M;Kit.add_section(g,M,y,e,j);Kit.art_button(g,h,"sort",Kit.ART_PLAY,M+12,y+9,"Sort","Move matching items from your backpack and other slot bags into their bag, one at a time",on_click=D("start_sort"));Kit.art_button(g,h,"stop",Kit.ART_CLOSE,M+150,y+9,"Stop","Stop sorting",on_click=D("stop_sort",None,True));Kit.add_label(g,"Tick what each slot's bag holds.",M+250,y+12,Kit.HUE_INFO);y+=j+d;Kit.add_section(g,M,y,e,f);b=G.CreateGumpScrollArea(M+4,y+4,e-8,f-8);k=e-8-20;s=k-171-Kit.text_w("+%d graphics"%bd)
				for a in range(l["slots"]):
					c=a*n;t,i=l["rules"].get(a,a4);Kit.add_label(b,"#%d"%(a+1),6,c+5,Kit.HUE_TITLE)
					if a in l["assign"]:Kit.add_label(b,ar(ai(l["assign"][a],False),24),44,c+5)
					else:Kit.add_label(b,"No bag in this slot",44,c+5,Kit.HUE_INFO)
					u=Kit.add_label(b,("+%s"%Kit.count(len(i),"graphic"))if i else "",s,c+5,Kit.HUE_INFO)
					if i:u.SetTooltip(", ".join("0x%04X"%W for W in i))
					Kit.art_button(b,h,"add%d"%a,Kit.ART_PLAY,k-165,c+3,"Add...","Target an item; slot #%d's bag holds its graphic too"%(a+1),on_click=D("add_rule_graphic",a));Kit.art_button(b,h,"clr%d"%a,Kit.ART_CLOSE,k-80,c+3,"Clear","Forget the graphics added to slot #%d"%(a+1),on_click=D("clear_rule_graphics",a));x=24
					for q,m,z in F:v=Kit.add_check(b,m,x,c+27,q in t,"Slot #%d's bag holds %s"%(a+1,m.lower()));p.append((a,q,v));x+=36+Kit.text_w(m)
				g.Add(b);y+=f+d;Kit.add_section(g,M,y,e,o);Kit.add_label(g,"Sort moves one item every %.1f s from your backpack and other bags."%aH,M+12,y+8,Kit.HUE_INFO);Kit.add_label(g,"It stops when you pick something up or a bag is full.",M+12,y+28,Kit.HUE_INFO)
			bf("srt",g,b4,rule_checks=p);cf["sync_at"]=time.time()+1.
		def gC(idx):API.SysMsg(A+": target an item; slot #%d's bag will hold its graphic."%(idx+1),T);a1("add_rule_graphic_to",idx)
		def gD(idx,target):
			if target:
				av()
				if idx>=l["slots"]:return
			c=dJ(target)
			if not c:return
			a=int(c.Graphic);d,b=l["rules"].get(idx,a4)
			if not a or a in b:API.SysMsg(A+": slot #%d's bag already holds that."%(idx+1),T);return
			if len(b)>=bd:API.SysMsg(A+": slot #%d already holds %d graphics; click Clear first."%(idx+1,bd),K);return
			l["rules"][idx]=(d,b+(a,));l["dirty_srt"]=True;al();API.SysMsg(A+": slot #%d's bag holds graphic 0x%04X too."%(idx+1,a),ax)
		def gE(idx):
			av();a,b=l["rules"].get(idx,a4)
			if not b:return
			if a:l["rules"][idx]=(a,())
			else:l["rules"].pop(idx,None)
			l["dirty_srt"]=True;al()
		def bv(k):bw();aJ(k)
		def bw():
			for a,b,c in(("mgr","mgr_x","mgr_y"),("trp","trp_x","trp_y"),("srt","srt_x","srt_y")):
				g=v[a]
				if Kit.is_open(g):l[b]=g.GetX();l[c]=g.GetY()
		def gF():
			if e["data"]is not l["cats_seen"]:l["cats_seen"]=e["data"];a5();l["dirty_flt"]=l["open_flt"]
			if l["open_flt"]:
				if l["dirty_flt"]:l["dirty_flt"]=False;gA()
				elif not Kit.is_open(v.get("flt")):l["open_flt"]=False;v["flt_checks"]=[]
				else:gz()
			for k,b in(("mgr",fG),("trp",fR),("srt",gB)):
				if not l["open_"+k]:l["dirty_"+k]=False
				elif l["dirty_"+k]:l["dirty_"+k]=False;b()
				elif not Kit.is_open(v[k]):
					l["open_"+k]=False
					if k in bp:v[bp[k]]=[]
				elif k=="srt"and v["rule_checks"]:
					a=time.time()
					if a>=cf["sync_at"]:
						cf["sync_at"]=a+1.
						if av():ap()
		def gG():
			c,d=H.max_w,H.max_h
			if c<=0 or d<=0:l["fit_seen"]=None;return
			a=(min(c,an),min(d,an))
			if a==(l["cell_w"],l["cell_h"]):l["fit_seen"]=None;return
			b=l["fit_seen"];l["fit_seen"]=(a,b[1]+1 if b and b[0]==a else 1)
			if l["fit_seen"][1]>=d3 or l["fit_pending"]:l["fit_pending"]=False;l["fit_seen"]=None;l["cell_w"],l["cell_h"]=a;aq()
		def gH():
			if l["drive_fixed"]or not Kit.is_open(v["grid"]):return
			a=time.time()
			if H.hook_calls!=l["hb_frame"]:
				l["hb_frame"]=H.hook_calls;l["hb_time"]=a
				if l["driving"]:l["driving"]=False
				return
			if not l["driving"]and a-l["hb_time"]>d8:
				l["driving"]=True
				if H.hook_calls==0 and not l["drive_told"]:l["drive_told"]=True;API.SysMsg(A+": draw hook isn't called; the script keeps the bags in place (they may flicker when items move).",T)
		gI={"add_rule_graphic":gC,"add_rule_graphic_to":gD,"add_trap_bag":fT,"add_trap_bag_to":fU,"assign_slot":fH,"assign_slot_to":fI,"auto_fill":fL,"bag_close":fh,"bag_min":fg,"bag_use":ff,"clear_all":fK,"clear_rule_graphics":gE,"clear_slot":fJ,"close_filters":gm,"close_win":fE,"disable":HOST.disable,"filter_bag_targeted":gx,"filter_broader":gt,"filter_by_target":gp,"filter_canvas_pick":gy,"filter_dropped":gs,"filter_move":gu,"filter_pick_bag":gw,"filter_preset":go,"filter_remove":gv,"filter_targeted":gq,"fold_to_bar":dq,"open_filters":gl,"open_win":b3,"quick_press":f8,"remove_trap_bag":fV,"select_all_traps":fS,"set_min":fB,"show_settings":Y,"start_job":fW,"start_sort":dF,"stop_all":gi,"stop_sort":am,"toggle_bare":fA,"toggle_flt_min":gn,"toggle_win_min":fF,"user_collapse":fz}
		def dL(w):return(("LAYOUT  (Apply to use)",(("num","slots","Slots:","Bag slots (%d-%d)"%(a6,af),"",a6,af),("num","cols","Columns:","Slots per row outside a zone (0-%d, 0 = near-square)"%af,"",0,af),("num","rows","Rows:","Rows of slots outside a zone (0-%d, 0 = near-square)"%af,"",0,af),("num","scale","Bag scale:","The client's Container Scale, for every container (50-200)","%",50,200),("buttons",(("apply",Kit.ART_OK,"Apply","Use the slots, columns, rows and scale above"),),{"bdy":4})),{"top":32,"sh":182,"ldy":2,"fw":60,"ugap":6,"lw":w-122}),("LOOK",(("slider","opacity","Bag opacity:","How solid bag panels and art are (10-100%); items stay solid",10,100,{"lw":158,"sdy":6,"sw":200,"ugap":20,"vfmt":"%d%%","h":30}),("check","trim","Trim bags to their item area","Hide bag art and butt the item areas together (needs client access; zones always fill)"),("check","items","Scale items with the bags","The client's option to draw items at bag scale")),{"top":32,"sh":116,"ldy":2}),("STATUS",(("note",ar(b5(),64),{"key":"status","h":24}),("note",du(),{"key":"size"})),{"top":32,"sh":86}))
		gJ=Kit.Page(cB,dL,al)
		def cg():
			l["shutting"]=False
			if not API.Player:l["wait_player"]=True;return
			l["wait_player"]=False;a=l["load_text"];l["load_text"]=None
			if a is None and N():l["wait_load"]=l["load_wanted"]=True;l["to_write"]=None;return
			l.update(wait_load=False,load_wanted=False,driving=False,drive_fixed=False,drive_told=False,job=None,to_write=None,queue=[],reported=False,detached_at=0.);aZ["told"]=False;cE();l["docked"],l["link_state"]=False,None;API.RemoveSharedVar(bF);aC["wish"]=0.;O["cols"],O["cell"],O["area"],O["told"]=None,None,None,None;aa["pct"]=None;bU();gk();a5();l["canvas"]=None;JR["rd"]=Z();H.meas.clear();H.opened=frozenset()
			if not r.tried:r.tried=True;eu()
			b={"fit":aM,"riding":P}
			if aN():b.update({"exact":True,"verify":True,"state":eL})
			HOST.layout_add(S,eK,A,b)
			if r.ok:fm()
			l["sort"]=None;J.update({"armed":False,"lit":{},"until":0.,"counts":{},"status":None})
			if a is not None:cT(a[0])
			else:cQ()
			l["open_mgr"]=l["dirty_mgr"]=l["want_mgr"];l["open_trp"]=l["dirty_trp"]=l["want_trp"];l["open_srt"]=l["dirty_srt"]=l["want_srt"]
			if b2()and not Kit.zone_up(S):l["minimized"]=True
			dr();H.disabled,H.fail_streak,H.error=False,0,""
			if r.ok:
				try:ay(bh)
				except Exception as e:H.error="client thread: %s"%e
			else:o(S);API.SysMsg(A+": no client access (%s); using basic pinning."%r.error,K)
			bP();l["dirty_frame"]=True;l["hb_frame"],l["hb_time"]=-1,time.time()
			for c,d in(("bag.attach",fr),("bag.grid_size",lambda:l["grid_wh"]),("bag.fit",fo),("bag.cell",eM),("bag.shrink",b0),("bag.pack",fp),("bag.open_manager",D("open_win","mgr")),("bag.open_traps",D("open_win","trp")),("look.bags",lambda:l.update(dirty_frame=True))):cC.service(c,d)
			Kit.hook_once(p,"hooked",("OnItemUpdated",e6))
		def gK():
			if l["wait_player"]:
				if API.Player:cg()
				return
			if l["wait_load"]:
				if l["load_text"]is not None:cg()
				return
			while l["queue"]:
				b=l["queue"].pop(0);c=gI[b[0]]
				try:c(*b[1:])
				except Exception as e:API.SysMsg(A+": couldn't do that (%s)."%e,K)
			if l["shutting"]:return
			dr();bP()
			if r.ok and H.disabled and not l["reported"]:l["reported"]=True;API.SysMsg(A+": draw hook stopped (%s); using basic pinning."%H.error,K);safe(lambda:ay(cM));l["dirty_frame"]=True
			if not Kit.is_open(v["bar"])or not Kit.is_open(v["grid"]):l["dirty_frame"]=True
			if(H.icons or aG)!=l["icons_used"]:l["dirty_frame"]=True
			if r.ok and not H.disabled:
				gH()
				if l["driving"]:
					try:ay(bH)
					except Exception as e:H.error="client thread: %s"%e
				gG();eX()
			else:
				if l["canvas"]is not None:da(None)
				fC()
			if l["dirty_frame"]and not aY():l["dirty_frame"]=False;fw()
			else:
				if P():ds()
				dp()
			gF();fY();a=time.time()
			if not 0<=l["quick_at"]-a<=1.:
				l["quick_at"]=a+1.
				if v.get("quick_sig")is not None and v["quick_sig"]!=cd():l["dirty_frame"]=True
			f6(a);gf(a);gg();fl(a)
			if(l["frame_x"],l["frame_y"])!=(l["saved_fx"],l["saved_fy"])and l["save_in"]<0 and not P()and l["canvas"]!="alone"and a-l["detached_at"]>=ec:ap()
			if l["save_in"]>0:l["save_in"]-=1
			elif l["save_in"]==0:bw();al()
		def gL():
			if l["load_wanted"]:
				l["load_wanted"]=False;a=cS()
				if l["wait_load"]and not l["shutting"]:l["load_text"]=(a,)
			eY()
			if e["wanted"]and e["data"]is None:
				e["wanted"]=False
				try:ac(r.f_tiles)
				except Exception:e["data"]={}
			bO()
		def gM():return d5 if l["driving"]else d4
		def gN():return bool(l["load_wanted"]or l["to_write"]is not None or db()or(e["wanted"]and e["data"]is None))
		cQ()
		def gO():
			l["shutting"]=True
			if l["wait_player"]or l["wait_load"]:l["wait_player"]=l["wait_load"]=l["load_wanted"]=False;l["load_text"]=None;return
			safe(a2);l.update(job=None,queue=[],sort=None);safe(lambda:br(time.time()));av();aD();cC.close();HOST.layout_remove(S)
			if aa["pct"]is not None:safe(lambda:b0(None))
			if l["attach"]is not None:l["attach"]=None;l["frame_x"],l["frame_y"]=l["saved_fx"],l["saved_fy"]
			l["grid_wh"]=None;l["docked"],l["link_state"]=False,None;API.SetSharedVar(cz,"off");safe(bU);l["canvas"]=None
			if r.ok:safe(lambda:ay(cM))
			bw();al();bO()
			for a in("grid","bar","mgr","trp","srt"):aJ(a)
			l["open_mgr"]=l["open_trp"]=l["open_srt"]=False;v.update({"side_status":None,"trap_checks":[],"rule_checks":[],"search_box":None,"counts":[]});l.update(bar_raw=None,grid_raw=None,grid_info=(None,False),slot_raws=())
		return{"start":cg,"tick":gK,"stop":gO,"client_tick":True,"config_height":gJ.height,"build_config":fM,"poll_config":fN,"config_closed":dv,"interval":gM,"thread_tick":gL,"thread_wanted":gN}
	def al():
		r="character";t="Paperdoll";aR="Character_settings";ar="Character_pos";at="Character_min";bA,bB=240,46;bC=7939;k=48;W=6;bD=16;aS,bE=260,237;L=80;aT=.2;cJ=.85;bF=.95;bG=90;aU=30;bH=74;bI,bJ=40,3.5;bK=.1;C=Kit.GAP;bL=.5;aV=5;aW,aX=50000,60000;bM=2.;bN,bO=970,547;bP=(694,695)
		try:import clr;from System import Array,Object,UInt32,UInt16,Int32,Double,Enum;from System.Reflection import BindingFlags;aY=True
		except Exception:aY=False
		ah=((6,"helmet","Helm","Head"),(13,"torso","Chest","Chest armour"),(19,"arms","Arms","Arms"),(7,"gloves","Gloves","Gloves"),(24,"legs","Legs","Leg armour"),(18,"earrings","Ears","Earrings"),(10,"neck","Neck","Necklace / gorget"),(17,"tunic","Tunic","Tunic / surcoat (over the chest)"),(12,"waist","Belt","Belt / half apron"),(3,"shoes","Feet","Shoes / boots"),(5,"shirt","Shirt","Shirt"),(22,"robe","Robe","Robe"),(20,"cloak","Cloak","Cloak / quiver"),(23,"skirt","Kilt","Skirt / kilt"),(4,"pants","Pants","Pants"),(1,"onehanded","Main","Main hand (one-handed weapon)"),(2,"twohanded","Off","Off hand (shield, two-handed weapon)"),(8,"ring","Ring","Ring"),(14,"bracelet","Brace","Bracelet"),(9,"talisman","Talis","Talisman"),);au=5;aZ=set(cO[0]for cO in ah);bQ=tuple(cP[0]for cP in ah);bR={"neck":("Necklace",),"onehanded":("OneHanded",),"twohanded":("TwoHanded",),"earrings":("Earrings",),"bracelet":("Bracelet",),"talisman":("Talisman",)};av,aw,ai,N,ax,aj,ay,az=(1,2,3,4,5,6,7,8);aA,aB,Q,aC,A,aD,Y,Z=(9,10,11,12,13,14,15,16);aa,aE,D,ak,ac,al,ad=17,18,19,20,22,23,24;a_=dict((cQ[0],cQ[1])for cQ in ah);a_.update({Q:"hair",Z:"beard",Y:"face"});a0=(ak,ax,N,ai,ad,D,A,aa,az,aD,Y,ay,al,ac,aC,aB,Q,Z,aE,aj,av,aw,aA);bS=(ax,N,ai,ad,D,A,aa,az,aD,Y,ay,al,ac,ak,aC,aB,Q,Z,aE,aj,av,aw,aA);bT=(ax,N,ai,ad,D,A,aa,ak,az,aD,Y,ay,al,aC,aB,Q,Z,aE,aj,av,aw,aA,ac);a1=tuple(sorted(set(a0)));aF=(39301,39302,42002,41675,41674);a2={400:12,402:12,401:13,403:13,605:14,607:14,606:15,608:15,666:666,694:666,667:665,695:665,1253:51253,987:12};bU=(401,403,606,608,667,695);a3,bV,bW=987,1002,50987;j=Kit.MARGIN;u=8;V=k+W;bX=au*V-W;B=u*2+2*(2*k+W)+2*u+aS;E=u*2+bX;a4=4*u+2*(2*k+W);bY=100;aG=a4+bY;bZ=(150,235);ae=2;b_=300;a5=B+2*j;v=j+30+Kit.GAP;n={"stats":True,"combine":True,"beside":False,"left":False};cK=dict(n);d={"shutting":False,"minimized":False,"docked":False,"queue":[],"sig":None,"doll_sig":None,"stats_at":0.,"doll_at":0.,"px":j,"attached":None,"beside_said":False,"layer_name":{},"wait_player":False,"wait_bags":None,"saved_min":False,"w_armed":True,"w_at":0.,"wbar":None,"fit":None,"k":1.,"py":None,"strip_w":None,"pw":B,"col":None,"ph":E,"rp":V,"pair":None,"pair_at":0.,"room":None,"room_fs":None,"told_shrink":None,"grew":False,"paired":False};e={"g":None,"c":{},"store":({},{}),"slots":[],"raw":None,"doll":[]};cL,m,cM=Kit.basics(d,t)
		def a6():
			p=Kit.get_var(aR).split("|")
			if len(p)>=2:n["stats"]=p[0]=="1";n["combine"]=p[1]=="1"
			if len(p)>=3:n["beside"]=p[2]=="1"
			if len(p)>=4:n["left"]=p[3]=="1"
			d["saved_min"]=bool(Kit.load_min(at))
		def a7():Kit.put_var(aR,"|".join(["1"if n[a]else "0"for a in("stats","combine","beside","left")]+["0"]))
		def b0():
			if not d.get("wait_player"):Kit.save_min(at,d["minimized"]and not d["docked"])
		def a8():Kit.save_pos(ar,e["g"])
		class Box(object):pass
		R=Box();R.tried=R.ok=False;R.error,R.pixel_n="",0
		for b1 in("m_animid","m_covered","MobileType","cursor","SlotItem","DollPiece","m_pixel","gumps","f_tiles","tiles"):setattr(R,b1,None)
		def b2():
			if not aY:R.error="clr module unavailable";return
			try:
				a=API.GetType().Assembly;clr.AddReference(a);from ClassicUO.Game.UI.Controls import ItemGump,Control;b=BindingFlags.Static|BindingFlags.Public|BindingFlags.NonPublic;p=BindingFlags.Instance|BindingFlags.NonPublic;d=BindingFlags.Instance|BindingFlags.Public|BindingFlags.NonPublic;e=a.GetType("ClassicUO.Client");R.p_game=e.GetProperty("Game",b)if e is not None else None;f=a.GetType("ClassicUO.GameController");R.p_uo=f.GetProperty("UO",d)if f is not None else None;g=a.GetType("ClassicUO.UltimaOnline");R.p_cursor=g.GetProperty("GameCursor",d)if g is not None else None;R.ItemGump=ItemGump
				try:
					class SlotItem(ItemGump):
						def Contains(self,x,y):return True
					R.SlotItem=SlotItem
				except Exception:R.SlotItem=None
				try:
					class DollPiece(ItemGump):
						def Contains(self,x,y):
							try:
								k=self.va_k
								if R.pixel_n==4:a=[UInt32(self.va_gid),Int32(int(x)),Int32(int(y)),Double(k)]
								else:a=[UInt32(self.va_gid),Int32(int(x/k)),Int32(int(y/k))]
								return bool(R.m_pixel.Invoke(R.gumps,Array[Object](a)))
							except Exception:return True
						def OnMouseDown(self,x,y,button):self.va_down=True;ItemGump.OnMouseDown(self,x,y,button)
						def OnMouseUp(self,x,y,button):self.va_down=False;ItemGump.OnMouseUp(self,x,y,button)
						def Update(self):
							ItemGump.Update(self)
							if self.va_down:b6(self)
					R.DollPiece=DollPiece
				except Exception:R.DollPiece=None
				h=a.GetType("ClassicUO.Game.GameActions");R.m_equip=h.GetMethod("Equip",b);R.m_swap=h.GetMethod("QueueEquipSwap",b);R.LayerType=a.GetType("ClassicUO.Game.Data.Layer");i=clr.GetClrType(Control);R.f_bounds=i.GetField("_bounds",p);R.Point=clr.GetPythonType(i.GetProperty("Location").PropertyType)
				for j in("m_equip","m_swap","LayerType","f_bounds","p_game","p_uo","p_cursor"):
					if getattr(R,j)is None:raise Exception("client member not found: "+j)
				R.ok=True
			except Exception as q:R.ok=False;R.error=str(q);return
			try:
				k=R.p_game.GetValue(None,None);c=R.p_uo.GetValue(k,None)if k is not None else None;l=c.GetType().GetProperty("Gumps")if c is not None else None;R.gumps=l.GetValue(c,None)if l is not None else None;R.m_pixel,R.pixel_n=None,0
				if R.gumps is not None:
					for m in R.gumps.GetType().GetMethods():
						n=len(m.GetParameters())
						if m.Name=="PixelCheck"and n in(3,4)and n>R.pixel_n:R.m_pixel,R.pixel_n=m,n
			except Exception:R.gumps=R.m_pixel=None
			if R.m_pixel is None:R.DollPiece=None
			R.f_tiles=safe(M)
			try:o=a.GetType("ClassicUO.Game.UI.Controls.PaperDollInteractable");R.m_animid=o.GetMethod("GetAnimID",b)if o is not None else None;R.animid_n=(int(R.m_animid.GetParameters().Length)if R.m_animid is not None else 0)
			except Exception:R.m_animid=None
			try:R.MobileType=a.GetType("ClassicUO.Game.GameObjects.Mobile");R.m_covered=(R.MobileType.GetMethod("IsCovered",b)if R.MobileType is not None else None)
			except Exception:R.m_covered=None
		a9={}
		def af(layer):
			e=a9.get(layer)
			if e is None:e=a9[layer]=Enum.ToObject(R.LayerType,layer)
			return e
		b3={};b4=256
		def ba():a=e["raw"];return None if a is None else a.World
		def b5():w=ba();return None if w is None else w.Player
		def aH():
			try:
				b=R.cursor
				if b is None:c=R.p_game.GetValue(None,None);d=R.p_uo.GetValue(c,None)if c is not None else None;b=R.cursor=R.p_cursor.GetValue(d,None)if d is not None else None
				h=b.ItemHold
				if h.Enabled and not h.IsFixedPosition:
					a=b7(int(h.Graphic))
					if a not in aZ:
						try:a=int(h.Layer)
						except Exception:a=0
					return int(h.Serial),bool(h.IsWearable),a
			except Exception:pass
			return
		def b6(piece):
			try:
				a=R.cursor
				if a is None:b=R.p_game.GetValue(None,None);c=R.p_uo.GetValue(b,None)if b is not None else None;a=R.cursor=R.p_cursor.GetValue(c,None)if c is not None else None
				h=a.ItemHold
				if h.Enabled and int(h.Serial)==int(piece.LocalSerial):piece.va_down=False;h.IsGumpTexture=False;h.MouseOffset=R.Point(0,0)
			except Exception:piece.va_down=False
		def b7(graphic):
			try:
				a=R.tiles
				if a is None:
					if R.f_tiles is None:return 0
					a=R.tiles=R.f_tiles.GetValue(None)
				return 0 if a is None or graphic<0 or graphic>=a.Length else int(a[graphic].Layer)
			except Exception:return 0
		def aI(c,x,y):c.Location=R.Point(x,y)
		b8=Kit.disposer(r,d,e);bb=2*k+W
		def b9(i):
			a,b=divmod(i,au)
			if a<2:x=d["px"]+u+a*V
			else:x=d["px"]+d["pw"]-u-bb+(a-2)*V
			return x,aK()+u+int(round(b*d["rp"]))
		def aJ():return bool(z(r))
		def bc():x=d["px"]+2*u+bb;return(x,aK()+u,max(1,d["pw"]-a4),max(1,d["ph"]-2*u))
		def aK():a=d["py"];return v if a is None else a
		aL,bd=.4,2.;be=300
		def ca(w,h,mode):
			a=(int(w),int(h))if(w is not None and h is not None)else None
			if a!=d["fit"]or(mode=="again"and a is not None and not d["paired"]):d["fit"]=a;d["pair"]=aM()if a is not None else None;d["pair_at"]=time.time();m("redraw")()
		def aM():
			if d["attached"]is None:return
			try:a=HOST.layout_pair(r,"bag")
			except Exception:return
			if not a or a[0]is None or a[1]is None:return
			return(tuple(int(b)for b in a[0]),tuple(int(c)for c in a[1]))
		def cb(x,y,fw,fh,l):
			(r,s,t,u),(g,h,m,n)=l
			if abs((y+fh)-h)>2*SNAP_DIST:return
			i,o=max(0,g-x),min(fw,g+m-x);b=o-i-2*j
			if b<40:return
			p=C//2;e=fh+p;a=(h+n-y)-e-j
			if a<20:return
			d["room"]=(b,a);f=aP(b,a);d["room_fs"]=f;c=f[1]if f is not None else aO(b,a);d["grew"]=c>a
			if c>a:k=int(Kit.screen()[1]);q=(k-y-j-e)if k>0 else c;a=max(a,min(c,q))
			return(i+j,e,b,a)
		def am(c,raw=False,flushed=False):
			k=d["k"]
			if abs(k-1.)<.001 or c is None:return
			with Kit.quiet:
				if not raw and not flushed:Kit.flush()
				a=c if raw else Kit.client_control(c)
				if a is None:return
				if str(a.GetType().Name)=="GumpPicTiled":a.ScaleTiledTexture=True
				a.ApplyScale(k,True,True,False)
		def aN(f=None):
			e=q("bag.cell")
			if e is None:return
			try:v=e()if f is None else e(f);b,c,g,n,h=v[0],v[1],v[2],v[3],v[4];d,a,i=(v[5],v[6],v[7])if len(v)>=8 else(100,100,100)
			except Exception:return
			if n<=0 or b<=0 or c<=0 or d<=0 or a<=0:return
			if d!=a:b,c=b*a/float(d),c*a/float(d)
			return b,c,g,n,h,a,min(i,a)
		def bf(ci,f,width):e,g,a,n,d=ci[0],ci[1],ci[2],ci[3],ci[4];b=int(math.ceil(e*f-.01));h=int(math.ceil(g*f-.01));i=max(b,width-d);j=max(1,min(n,(i+a)//(b+a)));c=int(math.ceil(n/float(j)));return c,c*h+(c-1)*a,b+d
		def aO(width,d=1<<20):
			b=q("bag.pack")
			if b is not None:
				try:a=b(width,1<<20)
				except Exception:a=None
				if a is not None:return a[1]
			c=aN(d);return 120 if c is None else bf(c,1.,width)[1]
		def aP(hw,c):
			g=q("bag.pack")
			if g is not None:
				try:e=g(hw,c)
				except Exception:e=None
				if e is not None:return e
			a=aN(c)
			if a is None:return
			b,f=a[5],a[6];h=d["told_shrink"];p=b
			for m in range(int(b-f)//aV+2):
				j,i,k=bf(a,p/float(b),hw);l=3*j if(h is not None and p>h)else 0
				if(i+l<=c and k<=hw)or p<=f:return(None if p>=b else p),i
				p=max(f,p-aV)
		an=10;bg,cc=20,26;ao=14;bh=2*8+an*bg+ao
		def aQ():
			if o["col_w"]is None:a=max(Kit.text_w(b)for b in("Stamina 999/999","Followers 99/99","Gold 9,999,999","Weight 0000/0000","Mana 999/999","HP 999/999"));o["col_w"]=max(aU,a)+2*I+4
			return o["col_w"]
		def cd(bw,room):
			e=bZ;b=[]
			if n["stats"]:
				if bw>=be:b.append(("strip",bw,room-L-Kit.GAP))
				b.append(("col",bw-aQ()-Kit.GAP,room))
			else:b.append(("none",bw,room))
			h,i=float(max(1,e[0])),float(max(1,e[1]));a=None
			for g,d,c in b:
				if g=="col"and c<bh:continue
				k=min(d/float(aG),c/float(E),bd)
				if k<aL:continue
				f=min((d-2*u*k)/h,(c-2*u*k)/i)
				if a is None or f>a[0]+.001 or(f>a[0]-.001 and k>a[4]):a=(f,g,d,c,k)
			if a is None:k=min(bw/float(aG),room/float(E),bd);return "none",bw,room,max(aL,k)
			return a[1],a[2],a[3],a[4]
		def ce(bw):
			a=int(math.ceil(aL*E))+1
			if not n["stats"]:return a
			return a+L+Kit.GAP if bw>=be else max(a,bh)
		def bi(fw,fh,combined):
			e,i=j,v;a,b=max(1,fw-2*j),max(1,fh-v-j);c=C;d=b
			if combined:l=min(b,max(ce(a),(b-c)//2));d=max(b-aO(a)-c,l);d=max(b-aO(a,max(1,b-d-c))-c,l)
			f,p,q,k=cd(a,d);r=max(aG,int(round(p/k)));m=max(E,int(round(q/k)));g=int(round(m*k));s=(L+Kit.GAP)if f=="strip"else 0;h,t=i,e
			if combined:n=max(d,g+s);o=(e,i+n+c,a,max(1,b-n-c))
			else:o=None
			u=(h+g+Kit.GAP)if f=="strip"else None;w=a if f=="strip"else None;x=(e+a-aQ(),h,aQ(),g)if f=="col"else None;return(k,int(round(t/k)),int(round(h/k)),u,w,o,(e,h+g),r,x,m)
		def ag():return E+(Kit.GAP+L if n["stats"]else 0)
		def cf(a,c):b=max(B,a);w=b+2*j;e=j+(b-B)//2;d=v+ag()+C;f=(j+(b-a)//2,d,a,c);return w,d+c+j,e,f
		def cg(a,b):w=j+B+C+a+j;c,d=(j,j+a+C)if n["left"]else(j+B+C,j);return w,v+max(ag(),b)+j,d,(c,v,a,b)
		def ch(a,b):
			if not n["beside"]:
				w,h,e,f=cf(a,b);c=int(Kit.screen()[1])
				if c<=0 or h<=c:return w,h,e,f
				if not d["beside_said"]:d["beside_said"]=True;API.SysMsg(t+": bag grid too tall to stack; bags go beside the doll.",Kit.HUE_INFO)
			return cg(a,b)
		def cj():
			if n["beside"]:return((j,v)if n["left"]else(j+B+C,v))
			return j,v+ag()+C
		def bj(g,w,h,hole):
			c,b,d,n=hole;a=Kit.WINDOW_BG;s=[Kit.pic_size(a+G)for G in range(9)];e,v,f,x,A,r,i,q,j=s;k=[]
			for y,z,t,u in((0,0,w,b),(0,b,c,h-b),(c+d,b,w-c-d,h-b),(c,b+n,d,h-b-n)):
				if t>0 and u>0:k.append(Kit.add_tiled(g,a+4,y,z,t,u))
			if all(bw[0]>0 and bw[1]>0 for bw in s):k+=[Kit.add_tiled(g,a+1,e[0],0,w-e[0]-f[0],v[1]),Kit.add_tiled(g,a+7,i[0],h-q[1],w-i[0]-j[0],q[1]),Kit.add_tiled(g,a+3,0,e[1],x[0],h-e[1]-i[1]),Kit.add_tiled(g,a+5,w-r[0],f[1],r[0],h-f[1]-j[1]),Kit.add_pic(g,a+0,0,0),Kit.add_pic(g,a+2,w-f[0],0),Kit.add_pic(g,a+6,0,h-i[1]),Kit.add_pic(g,a+8,w-j[0],h-j[1])]
			l,m=Kit.pic_size(Kit.CORNER_ART)
			if l and m and Kit.CORNER_ART:
				for o,p in((0,0),(w-l,0),(0,h-m),(w-l,h-m)):
					if o<c+d and o+l>c and p<b+n and p+m>b:continue
					k.append(Kit.add_pic(g,Kit.CORNER_ART,o,p))
			with Kit.quiet:Kit._frame_parts[g]=[ci for ci in k if ci is not None]
		def F():
			s,e["g"]=e["g"],None;bl();H=({},{});f={};P=[];c=d["attached"];b=None;d.update({"px":j,"k":1.,"py":None,"strip_w":None,"pw":B,"col":None,"ph":E,"rp":V});x=d["fit"]if not d["minimized"]else None;Q=j
			if Kit.is_open(s):y,z=s.GetX(),s.GetY()
			else:y,z=Kit.load_pos(ar,(200,120),(a5,v+ag()+j))
			I=J(r);d["paired"]=False
			if I is not None:y,z=I[0],I[1]
			if d["minimized"]:w,h=bA,bB;g=G.CreateGump(True,True);f["status"]=Kit.mini_bar(g,H,w,h,t,r,m("toggle_min"));Kit.set_text(f["status"],t+" & bags"if c is not None else t)
			else:
				w,h=a5,v+ag()+j;g=G.CreateGump(False,True)
				if x is not None:
					w,h=x;K=cb(y,z,w,h,d["pair"])if(c is not None and d["pair"])else None
					if K is not None:af=C//2;d["paired"]=True;(S,d["px"],d["py"],T,d["strip_w"],_h,U,d["pw"],d["col"],d["ph"])=bi(w,h-af+j,False);b=K;h=b[1]+b[3]+j
					else:(S,d["px"],d["py"],T,d["strip_w"],b,U,d["pw"],d["col"],d["ph"])=bi(w,h,c is not None)
					d["k"]=S;d["rp"]=(d["ph"]-2*u-k)/float(au-1);Q=U[0]
					if b is not None:
						bj(g,w,h,b);c["dx"],c["dy"]=b[0],b[1]
						if K is None:d["room"]=(b[2],b[3]);d["room_fs"]=aP(b[2],b[3]);d["grew"]=(d["room_fs"]is not None and d["room_fs"][1]>b[3])
						ap((b[2],b[3]));W=d["room_fs"];bk(W[0]if W is not None else None)
					else:Kit.add_window_frame(g,w,h);ap(None)
				elif c is not None and c.get("grid_wh"):gw,gh=c["grid_wh"];w,h,d["px"],b=ch(int(gw),int(gh));bj(g,w,h,b);c["dx"],c["dy"]=b[0],b[1]
				else:Kit.add_window_frame(g,w,h)
				if x is None:ap(None)
				M=d["px"];X=None
				if c is not None:X=[("traps",Kit.ART_PAGE,"Traps","Pick the bags Trap and Untrap cast on",m("bag_traps")),("bags",Kit.ART_PAGE,"Slots","Put a bag in each slot",m("bag_mgr"))]
				Kit.title_bar(g,H,w,t,r,m("toggle_min"),m("to_bar"),m("settings"),extra=X);i=[];Y=aK();Z,ph=d["pw"],d["ph"];i.append(Kit.add_section(g,M,Y,Z,ph));i.append(Kit.catcher(g,M,Y,Z,ph,lambda*a:None,None,movable=not aJ()));mx,my,mw,mh=bc();f["doll_bg"]=Kit.add_tiled(g,9274,mx,my,mw,mh,.35);i.append(f["doll_bg"]);f["doll_drop"]=Kit.catcher(g,mx,my,mw,mh,m(("drop",0)),"Drop an item here to wear it",movable=True);i.append(f["doll_drop"])
				for A,(aa,ai,ac,aj)in enumerate(ah):D,F=b9(A);i.extend(Kit.gold_box(g,D,F,k,k));l=G.CreateGumpColorBox(.01,"#000000");l.SetRect(D,F,k,k);Kit.on_click(l,m(("drop",aa)));ad=aj+": drop an item to wear it";l.SetTooltip(ad);g.Add(l);N=Kit.add_label(g,ac,D+(k-Kit.text_w(ac))//2,F+k-bD,Kit.HUE_TEXT);N.SetAcceptMouseInput(False);i.append(l);i.append(N);P.append({"layer":aa,"name":ai,"x":D,"y":F,"drop":l,"label":N,"serial":0,"ctrl":None,"raw":None,"tip":ad})
				ck(i)
				if x is not None:p,O,q=T,d["strip_w"],Q
				else:p=(v+E+Kit.GAP)if n["stats"]else None;O,q=B,M
				if p is not None:
					Kit.add_section(g,q,p,O,L);Kit.catcher(g,q,p,O,L,lambda*a:None,None,movable=not aJ())
					for A in range(3):f["stats%d"%(A+1)]=Kit.add_label(g,"",q+10,p+8+24*A,Kit.HUE_TEXT)
					cy(g,f,q,p+56)
				elif d["col"]is not None:cz(g,f,d["col"])
			xy=Kit.show_window(g,y,z,w,h,r,d["minimized"]and d["docked"],b8(g),a8,e,{"g":g,"c":f,"store":H,"slots":P});ab(r,g,xy);ae=o["hooks"]
			if ae is not None:ae["verify"]=not d["paired"]
			e["raw"]=Kit._raw_gump(g)if R.ok else None
			if c is not None:c["g"],c["raw"]=g,None
			bu();d.update({"sig":None,"doll_sig":None,"stats_at":0.,"stats_key":None,"doll_at":0.,"wbar":None});Kit.dispose(s)
		cN=None;o={"col_w":None,"bounds":{},"need":[],"redo":False,"order":[],"hooks":None}
		def ap(room):
			if room is None:d["room"]=None;bk(None)
			if room==d.get("told_bags"):return
			d["told_bags"]=room;a=q("bag.fit")
			if a is not None:safe(lambda:a(*(room or(None,None))))
		def bk(pct):
			if pct==d["told_shrink"]:return
			d["told_shrink"]=pct;a=q("bag.shrink")
			if a is not None:safe(lambda:a(pct))
		def ck(ctrls):
			if abs(d["k"]-1.)<.001:return
			Kit.flush()
			for a in ctrls:
				if a is not None:am(a,flushed=True)
		def bl():
			for s in e["slots"]:
				if s["ctrl"]is not None:Kit.dispose(s["ctrl"]);s["ctrl"]=None
			e["slots"]=[];bm()
		def bm():
			for p in e["doll"]:Kit.dispose(p)
			e["doll"]=[]
		def bn():return "docked"if d["docked"]else("collapsed"if d["minimized"]else "open")
		def bo(name):
			b=d["layer_name"].get(name)
			if b is not None:
				try:return API.FindLayer(b)
				except Exception:return
			for c in(name,)+bR.get(name,()):
				try:a=API.FindLayer(c)
				except Exception:a=None
				if a:d["layer_name"][name]=c;return a
			return
		def cl(p,keep=None):
			c={}
			if R.ok and p is not None:
				try:
					i=b3
					for e in a1:
						a=p.FindItemByLayer(af(e))
						if a is None:continue
						f,b,h=int(a.Serial),int(a.Graphic),int(a.Hue)
						if keep is not None:keep[e]=a
						l=(f,b);g=i.get(l)
						if g is not None:c[e]=(f,b,h)+g;continue
						try:d=a.ItemData;g=(int(d.AnimID),bool(d.IsPartialHue),bool(d.IsContainer))
						except Exception:
							try:d=API.FindItem(f).GetItemData()
							except Exception:d=None
							if d is not None:g=(int(d.AnimID or 0),bool(d.IsPartialHue),bool(d.IsContainer))
							else:c[e]=(f,b,h,0,False,False);continue
						if len(i)>=b4:i.clear()
						i[l]=g;c[e]=(f,b,h)+g
					k=(int(p.Graphic),int(p.Hue),bool(p.IsFemale));return c,k
				except Exception:
					c={}
					if keep is not None:keep.clear()
			try:j=API.Player
			except Exception:j=None
			if not j:return c,None
			for e in a1:
				a=bo(a_[e])
				if not a:continue
				try:f,b,h=(int(a.Serial or 0),int(a.Graphic or 0),int(a.Hue or 0))
				except Exception:continue
				m,n,o=0,False,False
				try:
					d=a.GetItemData()
					if d is not None:m,n,o=(int(d.AnimID or 0),bool(d.IsPartialHue),bool(d.IsContainer))
				except Exception:pass
				c[e]=(f,b,h,m,n,o)
			try:b=int(j.Graphic or 400)
			except Exception:b=400
			try:q=int(j.Hue or 0)
			except Exception:q=0
			k=(b,q,b in bU);return c,k
		def cm(graphic,hue,b):
			if graphic==a3:return a2[a3],bV,bW
			a=a2.get(graphic)
			if a is None:a=13 if b else 12
			return a,hue,0
		def cn(b,g,a,c):
			if R.m_animid is not None:
				try:
					if R.animid_n==4:d=[UInt16(b),UInt16(g),UInt16(a),bool(c)]
					else:d=[UInt16(b),UInt16(a),bool(c)]
					v=int(R.m_animid.Invoke(None,Array[Object](d)))
					if v>0:return v
				except Exception:R.m_animid=None
			if a==bN and b in bP:a=bO
			h,i=(aX,aW)if c else(aW,aX);e=a+h
			if Kit.pic_size(e)==(0,0):
				f=a+i
				if Kit.pic_size(f)!=(0,0):return f
			return e
		def co(layer,gfx,p=None):
			if R.m_covered is not None and R.ok and p is not None:
				with Kit.quiet:return bool(R.m_covered.Invoke(None,Array[Object]([p,af(layer)])))
			a=gfx.get(ac);b=gfx.get(N)
			if layer==ai:
				if gfx.get(ad)is not None or b==5137:return True
				if b in(1299,1300)or a==1284:return True
			elif layer==N:
				if gfx.get(ad)is not None or a==1284:return True
				if b in(491,997,1003):
					c=gfx.get(al)
					if c is not None and c not in(455,484):return True
					if a is not None and a!=553 and(a<=1255 or a>1259):return True
			elif layer==aa:
				if a is not None:return a!=0 and a not in aF
			elif layer==A:
				if a is not None and a!=0 and a not in aF:return True
				d=gfx.get(aa)
				if d is not None and d not in(5441,5442):
					if gfx.get(A)in(30762,30763):return True
			elif layer==D:return a is not None and a!=0 and a not in aF
			elif layer in(aj,Q):
				if a is not None:
					if a>12659:
						if a in(19357,30742):return True
					elif a<=9863:
						if a<9859:return 8270<=a<=8271
						return True
					elif a in(12217,12659):return True
			return False
		def cp(items):
			c=dict((i,p[1])for i,p in items.items());d=items.get(ak);a=a0
			if d is not None:
				if c.get(ac)in(41674,41675):a=bT
				elif d[5]:a=bS
			a=list(a);h=c.get(A)
			if h in(7174,7170,7172):
				e,b=a.index(N),a.index(A)
				if e<b:a.pop(b);a.insert(e,A)
			f=c.get(D)
			if f in(5069,5084,5102):
				g,b=a.index(D),a.index(A)
				if g<b:a.pop(g);a.insert(b,D)
			if f in(5136,5143):a=[A if s==D else(D if s==A else s)for s in a]
			return a,c
		def bp(gid,b):
			a,c=o["bounds"],o["order"]
			if gid not in a:c.append(gid)
			a[gid]=b
			while len(c)>b_:a.pop(c.pop(0),None)
			return b
		def cq(gid):
			g="pic"
			try:h=Kit.on_client(lambda:Tex.gump_pixels(gid)if Tex.find()else None)
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
			return bp(gid,g)
		def cr(gid):
			b=o["bounds"].get(gid,"need")
			if b=="need":
				if gid not in o["need"]:o["need"].append(gid)
				b="pic"
			if b!="pic":return b
			a,c=Kit.pic_size(gid);return(0,0,a,c)if a>0 and c>0 else None
		def cs():return bool(o["need"])
		def ct(items,who,M=None):
			v=e["g"];bm()
			if v is None or who is None:return
			w,x,y=who;o=[];e["doll"]=o;i=[];N,O,z=cm(w,x,y);i.append((N,O,True,0,0))
			if z:i.append((z,x,True,0,0))
			P,T=cp(items)
			for n in P:
				A=items.get(n)
				if A is None:continue
				p,U,V,B,q,_c=A
				if co(n,T,M):continue
				if B==0 and R.m_animid is None:continue
				j=cn(w,U,B,y)
				if j<=0 or Kit.pic_size(j)==(0,0):continue
				i.append((j,V&16383,q,0 if n in(Q,Z,Y)else p,n))
			a=b=1<<20;c=f=-(1<<20)
			for W in i:
				l=cr(W[0])
				if l is not None:a,b=min(a,l[0]),min(b,l[1]);c,f=max(c,l[2]),max(f,l[3])
			if c<=a or f<=b:a,b,c,f=0,0,aS,bE
			C=(c-a,f-b);k=d["k"];X,my,mw,mh=bc();D,E=X*k+ae,my*k+ae;F,r=max(1.,mw*k-2*ae),max(1.,mh*k-2*ae);PW=max(1.,(d["pw"]-2*u)*k-2*ae);S=min(r/C[1],PW/C[0]);H=int(round(D+F/2.-S*(a+c)/2.));I=int(round(E+r/2.-S*(b+f)/2.));s=int(round((D+F/2.)/k-(a+c)/2.));t=int(round((E+r/2.)/k-(b+f)/2.));J=abs(S-1.)>.001;g=e["raw"];h=[-1]
			if R.ok and g is not None:
				try:
					Kit.flush();K=Kit.client_control(e["c"].get("doll_drop"))
					if K is not None:h[0]=g.Children.IndexOf(K)+1
				except Exception:h[0]=-1
			def L(a):
				if h[0]<=0:return False
				b=g.Children;a.Parent=g
				while b.Remove(a):pass
				b.Insert(min(h[0],b.Count),a);h[0]+=1;return True
			def aa(gid,b,c,serial):
				if R.DollPiece is None or g is None or h[0]<=0:return
				try:a=R.DollPiece(g,UInt32(int(serial)),UInt16(int(gid)),UInt16(int(b)),0,0,True)
				except Exception:R.DollPiece=None;return
				try:
					a.va_gid,a.va_k,a.va_down=int(gid),float(S),False;a.HighlightOnMouseOver=False;a.IsPartialHue=bool(c);aI(a,H,I)
					if J:a.ApplyScale(S,False,True,False)
					G.AddControlOnClick(a,m(("drop",0)))
					if not L(a):raise Exception("no place")
				except Exception:safe(a.Dispose);return
				return a
			def ab(gid,b,d,serial=0):
				if serial:
					a=aa(gid,b,d,serial)
					if a is not None:o.append(a);return
				p=G.CreateGumpPic(gid,s,t,b)if b else G.CreateGumpPic(gid,s,t);p.SetPos(s,t);a=None
				try:
					Kit.flush();a=Kit.client_control(p);aI(a,H,I)
					if J:a.ApplyScale(S,False,True,False)
				except Exception:a=None;am(p)
				if d:e=Kit.client_control(p);Kit.set(e if e is not None else p,"IsPartialHue",True)
				if serial:p.SetEntityTooltip(serial);Kit.on_click(p,m(("drop",0)));Kit.hook_double(p,m(("use",serial)))
				else:p.SetAcceptMouseInput(False)
				c=False
				if a is not None:
					try:c=L(a)
					except Exception:c=False
				if not c:v.Add(p)
				o.append(p)
			for j,ac,q,p,ad in i:ab(j,ac,q,p)
		def bq(force=False):
			if d["minimized"]or e["g"]is None:return
			if o["redo"]and not o["need"]:o["redo"]=False;d["doll_sig"]=None
			b=time.time()
			if not force and d["sig"]is not None and d["doll_sig"]is not None and 0<=b-d["doll_at"]<bK:return
			d["doll_at"]=b;p=b5()if R.ok else None;c={};a,f=cl(p,c);g=tuple([a[i][0]if i in a else 0 for i in bQ])
			if g!=d["sig"]:cv(g,p,c)
			h=(f,tuple(sorted((w,s[0],s[1],s[2])for w,s in a.items())))
			if h!=d["doll_sig"]:d["doll_sig"]=h;ct(a,f,p)
		def cu(s,item,c):
			i=e["g"]
			if s["ctrl"]is not None:Kit.dispose(s["ctrl"]);s["ctrl"]=None
			if item is None and c is None:Kit.set(s["label"],"IsVisible",True);Kit.with_tip(s["drop"],s["tip"]);return
			Kit.set(s["label"],"IsVisible",False);s["drop"].SetTooltip("")
			if R.ok and item is not None and e["raw"]is not None:
				try:
					j=(e["raw"],UInt32(int(item.Serial)),UInt16(int(item.DisplayedGraphic)),UInt16(int(item.Hue)),0,0);a=None
					if R.SlotItem is not None:
						try:a=R.SlotItem(*j)
						except Exception:R.SlotItem=None
					if a is None:a=R.ItemGump(*j)
					r=R.f_bounds.GetValue(a);l,n=int(r.Width),int(r.Height);f=min(1.,(k-6)/float(max(1,l)),(k-6)/float(max(1,n)));g=d["k"];aI(a,int(round((s["x"]+(k-l*f)/2.)*g)),int(round((s["y"]+(k-n*f)/2.)*g)))
					if abs(g*f-1.)>.001:
						try:a.ApplyScale(g*f,False,True,False)
						except Exception:am(a,True)
					try:G.AddControlOnClick(a,m(("drop",s["layer"])))
					except Exception as h:safe(a.Dispose);raise h
					i.Add(a);s["ctrl"]=a;return
				except Exception as h:R.error="item control: %s"%h
			o=int(c.Serial)if c is not None else int(item.Serial);p=int(c.Graphic)if c is not None else int(item.DisplayedGraphic);b=G.CreateGumpItemPic(p,k-6,k-6);b.SetRect(s["x"]+3,s["y"]+3,k-6,k-6);am(b);b.SetEntityTooltip(o);Kit.on_click(b,m(("drop",s["layer"])));Kit.hook_double(b,m(("use",o)));i.Add(b);s["ctrl"]=b
		def cv(sig,p,got=None):
			b=e["slots"]
			if len(b)!=len(sig):return
			f=d["sig"]or(None,)*len(b)
			for i,s in enumerate(b):
				if sig[i]==f[i]:continue
				s["serial"]=sig[i];a=c=None
				if sig[i]:
					if R.ok and p is not None:
						a=got.get(s["layer"])if got else None
						if a is None:
							try:a=p.FindItemByLayer(af(s["layer"]))
							except Exception:a=None
					if a is None:c=bo(s["name"])
				cu(s,a,c)
			d["sig"]=sig
		def cw(layer):
			if R.ok:
				h=aH()
				if h is None:return
				c,e,a=h
				if not e:API.SysMsg(t+": that can't be worn.",Kit.HUE_BAD);return
				if a not in aZ and a>0:API.SysMsg(t+": that doesn't go in an equipment slot.",Kit.HUE_BAD);return
				try:
					w=ba();p=w.Player;b=p.FindItemByLayer(af(a))if a else None
					if b is not None and int(b.Serial)==c:b=None
					if b is None:R.m_equip.Invoke(None,Array[Object]([w,UInt32(int(p.Serial))]))
					else:R.m_swap.Invoke(None,Array[Object]([w,UInt32(int(p.Serial)),af(a),UInt32(int(b.Serial))]))
					d["sig"]=None
				except Exception as f:API.SysMsg(t+": couldn't equip that (%s)."%f,Kit.HUE_BAD)
				return
			c=Kit.held_item()
			if c:API.EquipItem(c);d["sig"]=None
		cx=("Strength","Dexterity","Intelligence","Hits","HitsMax","Mana","ManaMax","Stamina","StaminaMax","Weight","WeightMax","Gold","Followers","FollowersMax","PhysicalResistance");I=10
		def cy(g,c,px,y):f=Kit.text_w("Weight 0000/0000");h=Kit.text_w("Gold 9,999,999   Followers 99/99");a=px+10+f+6;b=d["strip_w"]or B;i=b-(a-px)-10-h-14;e=max(aU,min(bG,i));Kit.weight_bar(g,c,a,y,e,16);c["stats4"]=Kit.add_label(g,"",a+e+10,y,Kit.HUE_TEXT);c["room"]=b-2*I;c["room3"]=f;c["room4"]=max(0,b-(a+e+10-px)-I)
		def cz(g,c,col):x,y,w,h=col;Kit.add_section(g,x,y,w,h);Kit.catcher(g,x,y,w,h,lambda*a:None,None,movable=not aJ());b=max(bg,min(cc,(h-16-ao)//an));d=y+max(8,(h-an*b-ao)//2);c["scol"]=[Kit.add_label(g,"",x+I,d+f*b+(ao if f>=7 else 0),Kit.HUE_TEXT)for f in range(an)];c["room"]=w-2*I;Kit.weight_bar(g,c,x+I,d+7*b-1,w-2*I,16)
		def br(f,a,g):
			if a<=0 and g>0:a=int(bI+bJ*g)
			b=(float(f)/a)if a>0 else-1.
			if b>=bF:
				if d["w_armed"]and O("character.weight","Weight %d/%d (%d%%): nearly overloaded"%(f,a,int(b*100)),level="warn",who="weight")is not False:d["w_armed"]=False
			elif b>=0:d["w_armed"]=True
			h=e["c"].get("wfills")
			if not h or d["minimized"]:return
			c=Kit.weight_level(b,e["c"]["wbar_w"])
			if c==d["wbar"]:return
			d["wbar"]=c;Kit.weight_show(h,c[0],c[1])
		def cA():
			a=time.time()
			if 0<=a-d["w_at"]<aT:return
			d["w_at"]=a
			try:p=API.Player
			except Exception:p=None
			if not p:return
			try:b,c,e=int(p.Weight),int(p.WeightMax),int(p.Strength)
			except Exception:return
			br(b,c,e)
		def bs():
			c=e["c"]
			if d["minimized"]or("stats1"not in c and "scol"not in c):return False
			h=time.time()
			if 0<=h-d["stats_at"]<aT:return True
			d["stats_at"]=h;p=K()
			if not p:return True
			v={};g=[]
			for k in cx:
				try:x=int(getattr(p,k))
				except Exception:x=0
				v[k]=x;g.append(x)
			a=c["room"];f=c.get("scol");i=c.get("stats1");b=d.get("stats_key")
			if b is None or b[0]!=g or b[1]is not f or b[2]is not i or b[3]!=(a,c.get("room3"),c.get("room4")):
				d["stats_key"]=(g,f,i,(a,c.get("room3"),c.get("room4")))
				if f is not None:
					for j,m in zip(f,("Str %d"%v["Strength"],"Dex %d"%v["Dexterity"],"Int %d"%v["Intelligence"],"HP %d/%d"%(v["Hits"],v["HitsMax"]),"Mana %d/%d"%(v["Mana"],v["ManaMax"]),"Stamina %d/%d"%(v["Stamina"],v["StaminaMax"]),"Weight %d/%d"%(v["Weight"],v["WeightMax"]),"Gold %s"%l(v["Gold"]),"Followers %d/%d"%(v["Followers"],v["FollowersMax"]),"AR %d"%v["PhysicalResistance"])):Kit.set_text(j,Kit.fit(m,a))
				else:Kit.set_text(c["stats1"],Kit.fit("Str %d   Dex %d   Int %d   AR %d"%(v["Strength"],v["Dexterity"],v["Intelligence"],v["PhysicalResistance"]),a));Kit.set_text(c["stats2"],Kit.fit("HP %d/%d   Mana %d/%d   Stamina %d/%d"%(v["Hits"],v["HitsMax"],v["Mana"],v["ManaMax"],v["Stamina"],v["StaminaMax"]),a));Kit.set_text(c["stats3"],Kit.fit("Weight %d/%d"%(v["Weight"],v["WeightMax"]),c["room3"]));Kit.set_text(c["stats4"],Kit.fit("Gold %s   Followers %d/%d"%(l(v["Gold"]),v["Followers"],v["FollowersMax"]),c["room4"]))
			br(v["Weight"],v["WeightMax"],v["Strength"]);return True
		def q(name):return HOST.services.get(name)
		def cB(cmd):
			if cmd=="show":m("show")()
			elif cmd=="dock":m("to_bar")()
		def bt():
			c,f=q("bag.attach"),q("bag.grid_size");g,h=cj();a=safe(f);b={"g":e["g"],"raw":None,"dx":g,"dy":h,"shown":not d["minimized"],"state":bn(),"grid_wh":tuple(a)if a else None,"cmd":cB};d["attached"]=b
			try:c(b)
			except Exception as i:d["attached"]=None;API.SysMsg(t+": couldn't combine with Bags (%s)."%i,Kit.HUE_BAD);return False
			return True
		def cC():
			f=q("bag.attach");c=q("bag.grid_size");b=d["attached"];e=n["combine"]and f is not None and c is not None
			if b is None:
				if e and bt():F()
				return
			if not e:cD();return
			a=safe(c);a=tuple(a)if a else None
			if a!=b["grid_wh"]:
				b["grid_wh"]=a
				if d["fit"]is None and not d["minimized"]:F()
		def cD():
			b,d["attached"]=d["attached"],None;ap(None);d["told_shrink"]=None
			if b is not None:
				a=q("bag.attach")
				if a is not None:safe(lambda:a(None))
			if e["g"]is not None and not d["shutting"]:F()
		def bu():
			a=d["attached"]
			if a is not None:a["shown"]=not d["minimized"];a["state"]=bn()
		bv={"drop":cw,"use":lambda serial:API.UseObject(serial),"follow":lambda serial:H(serial,t)}
		def cE(w):return(("WINDOW",(("check","stats","Show your stats","Str / Dex / Int, HP, mana, stamina, weight, gold, followers: under the doll, or beside it in a zone"),("check","combine","Combine with Bags in one window","The Bags grid inside this window (unticked: two windows)"),("check","beside","Bags beside the doll (not under)","Combined: the grid beside the doll; one too tall to stack goes beside anyway"),("check","left","Bags on the left","Beside the doll: on its left (unticked: right)"),("note","Drop an item on a slot to wear it; drag it out to take it off.",{"ndy":4})),{"top":32,"sh":170}),)
		def cF(old,new):
			if e["g"]is not None:m("redraw")();HOST.poke()
		aq=Kit.Page(n,cE,a7,cF);a6()
		def bx():
			a6()
			if not safe(lambda:API.Player):d["wait_player"]=True;return
			d["wait_player"]=False
			if not R.tried:R.tried=True;b2()
			d.update({"shutting":False,"docked":HOST.dock_soon(r),"queue":[],"sig":None,"doll_sig":None,"attached":None,"beside_said":False,"fit":None,"k":1.,"py":None,"strip_w":None,"pw":B,"col":None,"ph":E,"rp":V,"told_bags":None,"pair":None,"pair_at":0.,"room":None,"room_fs":None,"told_shrink":None,"grew":False,"paired":False,"w_armed":True,"w_at":0.,"wbar":None,"wait_bags":None,"minimized":bool(d["saved_min"]or U(r))});P("character.weight","Weight near the limit",bH)
			if n["combine"]and not by()and X("bags","inventory"):d["wait_bags"]=time.time();return
			bz()
		def by():a=q("bag.grid_size");return q("bag.attach")is not None and a is not None and bool(safe(a))
		def bz():
			d["wait_bags"]=None;c,f=q("bag.attach"),q("bag.grid_size")
			if n["combine"]and c is not None and f is not None:bt()
			a=HOST.layout_slot(r)
			if a is not None and a[0]is not None and a[1]is not None:d["fit"]=(int(a[0]),int(a[1]));d["pair"]=aM();d["pair_at"]=time.time()
			F();bq();bs();b=Kit.dock_hooks(t,bC,d,e,m("redraw"));b.update({"fit":ca,"exact":True,"pieces_out":True,"verify":not d["paired"]});o["hooks"]=b;S(r,b)
			if not R.ok:API.SysMsg(t+": no client access (%s); slots show pictures and equip without swapping."%R.error,Kit.HUE_INFO)
		def cG():
			if d["wait_player"]:
				if safe(lambda:API.Player):bx()
				return
			if d["wait_bags"]is not None:
				if by()or not 0<=time.time()-d["wait_bags"]<bM:bz()
				return
			if e["g"]is None:return
			if Kit.was_clicked(e["store"],"close"):a8();Kit.dispose(e["g"]);return
			while d["queue"]:
				a=d["queue"].pop(0);h=a[0]if isinstance(a,tuple)else a
				if a=="show":d["minimized"],a=True,"toggle_min"
				if a=="redraw"and aH()is not None:d["redraw_due"]=True
				elif Kit.win_action(a,d,r,t,F,at):continue
				elif a in("bag_mgr","bag_traps"):
					i=q("bag.open_manager"if a=="bag_mgr"else "bag.open_traps")
					if i is not None:i()
				elif h in bv:bv[h](a[1])
			bu();cC()
			if e["g"]is None:return
			j=aH()is not None
			if d.get("redraw_due")and not j:d["redraw_due"]=False;F();return
			if d["attached"]is not None and not j:
				f=time.time()
				if f-d["pair_at"]>=bL or f<d["pair_at"]:
					d["pair_at"]=f;k=aM()
					if k!=d["pair"]:
						d["pair"]=k
						if d["fit"]is not None:F();return
					c=d["room"]
					if c is not None and d["fit"]is not None and not d["minimized"]:
						b=aN(c[1]);l=(c,None if b is None else(round(b[0],1),round(b[1],1),b[2],b[3],b[4],b[5]))
						if l!=d.get("room_sig"):
							d["room_sig"]=l;g=aP(c[0],c[1])
							if g is not None and(g[0]!=d["told_shrink"]or(g[1]>c[1])!=d["grew"]):F();return
			bq()
			if not bs():cA()
		def cH():
			a=o["need"]
			if not a:return
			b=a[0]
			try:cq(b)
			except Exception:bp(b,"pic")
			a.pop(0);o["redo"]=True
		def cI():
			d["shutting"]=True;T(r);Kit.save_pos(ar,e["g"]);b0();a7();b,d["attached"]=d["attached"],None
			if b is not None:
				a=q("bag.attach")
				if a is not None:safe(lambda:a(None))
			bl();g,e["g"]=e["g"],None;e["raw"]=None;Kit.dispose(g)
		return{"start":bx,"tick":cG,"stop":cI,"client_tick":True,"config_height":aq.height,"build_config":aq.build,"poll_config":aq.poll,"config_closed":aq.closed,"thread_tick":cH,"thread_wanted":cs}
	def am():
		D="storage";E="Storage";av="StorageIndex_settings";a1="StorageIndex_pos";aw="StorageIndex_min";R=300;ax=20000;a2=60;F=(.6,2.);ay=15.;az=1.;a3=600.;a4=20;a5=.5;a6=40;a7=6000;a8=80;S=1500;aA=5.;T=10.;a9=30;ba=.4;aB=3.;O=14;U=O*30;aj=12;aC=40;bb={291:"Pack horse",292:"Pack llama",791:"Giant beetle"};aD=(8198,7774);bc="_storage_index_%s.txt";bd="# Virtue Assistant Storage Index 1";ak="StorageIndex_favs";aE="StorageIndex_account";al=420;be,bf=260,46;G=20;bg=3708;aF="Alt+click: auto-follow (again to stop)";M=Kit.MARGIN;IW=al-2*M;I=M+30+Kit.GAP;aG=64;V=I+aG+Kit.GAP;aH=12+O*G+8;bh=V+aH+Kit.GAP;aI=30;W=bh+aI+M;aJ=((60,1,"just now"),(3600,60,"%dm ago"),(86400,3600,"%dh ago"),(172800,86400,"%d day ago"),(0,86400,"%d days ago"));n={"bank":True,"ground":True,"pack":True,"days":a2};e=[];b_=dict(n);c={"shutting":True,"minimized":False,"docked":False,"queue":[],"active":False,"hooked":False};h={"g":None,"c":{},"store":({},{}),"rows":[]};J={"wipe_at":0.};am,B,b0=Kit.basics(c,E);b={"recs":{},"tombs":{},"ver":0,"dirty":False,"dirty_at":0.,"loaded":False,"path":None,"mtime":None,"err":"","unread":False};d={"ver":-1,"keys":{},"places":{},"items":0,"chars":0,"veil":False};a={"query":"","seen_text":None,"changed_at":0.,"page":0,"rows":[],"sel":None,"naming":None,"forget_arm":(None,0.),"status":"","status_hue":Kit.HUE_INFO,"status_at":0.,"dirty":True,"built_for":None,"live":{},"live_at":0.,"live_ver":0,"live_sig":None,"data":[],"prev":[],"last_read":("",0.,""),"iw":IW};g={};j={"q":[],"n":0};X={"n":0};L=[];Y={};N={};C=set();P={};r=[];Z={"key":None,"stats":[]};aa={"key":None,"by":{}};aK=re.compile(r"%[^%]*%|%s")
		def v(s):return str(s or "").replace("|","/").replace("\r"," ").replace("\n"," ").strip()
		def bi(text):
			h=0x811C9DC5
			for a in text:h=((h^ord(a))*16777619)&0xFFFFFFFF
			return "%08x"%h
		def bj(it,graphic):
			n=Y.get(graphic)
			if n is None:
				try:d=it.GetItemData();n=aK.sub("",str(d.Name or "")).strip()if d is not None else ""
				except Exception:n=""
				if len(Y)>3000:Y.clear()
				Y[graphic]=n
			return n
		def ab(it,graphic,amount):
			try:n=str(it.Name or "")
			except Exception:n=""
			if "%"in n:n=aK.sub("",n)
			n=n.strip()
			if amount>1:
				a=str(amount)
				if n.startswith(a+" "):n=n[len(a)+1:].strip()
			if not n:n=bj(it,graphic)or("item 0x%04X"%graphic)
			n=v(n);return n[:1].upper()+n[1:]
		def ac(text):
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
		def ad(a,key):
			g,b=key[0],key[2]
			for c,v in a:
				if c=="g":
					if g==v:return True
				elif v in b:return True
			return False
		aL={"days":(1,3650)}
		def aM():Kit.kv_load(av,";",n,aL)
		def bk():Kit.kv_save(av,";",n,("bank","ground","pack","days"),aL)
		def bl():
			b=Kit.get_var(ak,"");del e[:]
			if not b:e.extend([[f,"0x%04X"%i]for f,i in sorted(Kit.REAGENTS.values())]+[["Bandages","0x0E21"]]);return
			if b=="-":return
			for d in b.split(";"):
				if "="not in d:continue
				c,a=d.split("=",1);c,a=c.strip(),a.strip()
				if a and len(e)<aj:e.append([c or a,a])
		def aN():
			if not e:Kit.put_var(ak,"-");return
			Kit.put_var(ak,";".join("%s=%s"%(f.replace(";",",").replace("=","-"),i.replace(";",","))for f,i in e))
		def bm():
			with Kit.quiet:
				Typing._find();b=Typing.prof;a=Typing._get(None,"CurrentProfile",b)if b is not None else None;c=Typing._get(a,"Username")if a is not None else None
				if c:e=Typing._get(a,"ServerName")or "";return bi(("%s|%s"%(e,c)).lower())
			try:
				d=API.PersistentVar.Account;v=str(API.GetPersistentVar(aE,"",d)or "")
				if not v:import random;v="a%07x"%random.randint(0,0xFFFFFFF);API.SavePersistentVar(aE,v,d)
				return "".join(f for f in v if f.isalnum())[:16]or "account"
			except Exception:return "account"
		def an(serial):return{"s":serial,"parent":0,"root":serial,"kind":"bag","cs":0,"cname":"","label":"","custom":"","facet":0,"x":0,"y":0,"seen":0.,"mob":0,"plabel":"","stub":False,"items":{}}
		def ao(text):
			b,d={},{}
			for a in text.split("\n"):
				a=a.rstrip("\r")
				if not a or a.startswith("#"):continue
				p=a.split("|")
				try:
					if p[0]=="C"and len(p)>=15:s=int(p[1]);r=an(s);r.update({"parent":int(p[2]),"root":int(p[3]),"kind":p[4],"cs":int(p[5]),"cname":p[6],"label":p[7],"custom":p[8],"facet":int(p[9]),"x":int(p[10]),"y":int(p[11]),"seen":float(p[12]),"mob":int(p[13]),"plabel":p[14],"stub":len(p)>15 and p[15]=="1"});b[s]=r
					elif p[0]=="I"and len(p)>=6:
						r=b.get(int(p[1]));c=int(p[4])
						if r is not None and c>0:
							e=p[5];f=(int(p[2]),int(p[3]),e.lower());g=r["items"].get(f)
							if g is None:r["items"][f]=[e,c]
							else:g[1]+=c
					elif p[0]=="D"and len(p)>=3:d[int(p[1])]=float(p[2])
				except(ValueError,IndexError):continue
			return b,d
		def bn():
			a=[bd]
			for s,r in b["recs"].items():
				a.append("C|%d|%d|%d|%s|%d|%s|%s|%s|%d|%d|%d|%d|%d|%s|%d"%(s,r["parent"],r["root"],r["kind"],r["cs"],v(r["cname"]),v(r["label"]),v(r["custom"]),r["facet"],r["x"],r["y"],int(r["seen"]),r["mob"],v(r["plabel"]),1 if r["stub"]else 0))
				for c,e in r["items"].items():a.append("I|%d|%d|%d|%d|%s"%(s,c[0],c[1],e[1],v(e[0])))
			for s,t in b["tombs"].items():a.append("D|%d|%d"%(s,int(t)))
			return "\n".join(a)+"\n"
		def ap(path):return Kit.read_merge(path)
		def bo(path,text):
			try:return Kit.write_safe(path,text)
			except Exception as a:b["err"]=str(a)[:60];return False
		def ae(path):return safe(lambda:os.path.getmtime(path))
		def aq(recs,tombs):
			d=False;c=b["recs"];e=time.time()-n["days"]*86400.
			for s,t in tombs.items():
				if t>b["tombs"].get(s,0.):b["tombs"][s]=t
			for s,r in recs.items():
				if r["seen"]<e:continue
				a=c.get(s)
				if a is None or r["seen"]>a["seen"]:
					if a is not None and a["custom"]and not r["custom"]:r["custom"]=a["custom"]
					c[s]=r;N.pop(s,None);d=True
				elif r["custom"]and not a["custom"]:a["custom"]=r["custom"];d=True
			for s in[f for f in c if f in b["tombs"]and c[f]["seen"]<=b["tombs"][f]]:del c[s];d=True
			return d
		def af():
			h=time.time();c=b["recs"];j=h-n["days"]*86400.;k=h-a9*86400.
			for s in[p for p,q in b["tombs"].items()if q<k]:del b["tombs"][s]
			if len(b["tombs"])>4*R:
				for s,l in sorted(b["tombs"].items(),key=lambda a:a[1])[:len(b["tombs"])-4*R]:del b["tombs"][s]
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
			if e>R or f>ax:
				for i,g in sorted(a.items(),key=lambda a:a[1][0]):
					if e<=R and f<=ax:break
					for s in g[1]:c.pop(s,None)
					e-=len(g[1]);f-=g[2];d=True
			return d
		def aO():
			a=b["path"]
			if not a:return
			c=ap(a);b["mtime"]=ae(a);b["unread"]=c is None
			if c:aq(*ao(c))
			af();b["loaded"]=True;b["ver"]+=1
		def aP():
			a=b["path"]
			if not a:return
			c=ae(a)
			if b["unread"]or(c is not None and c!=b["mtime"]):
				d=ap(a)
				if d is None:b["err"]="couldn't read the index file";return
				b["unread"]=False;b["mtime"]=c
				if d and aq(*ao(d)):b["ver"]+=1
			if af():b["ver"]+=1
			if bo(a,bn()):b["mtime"]=ae(a);b["dirty"]=False;b["err"]=""
		def bp():
			d=b["path"];a=ae(d)
			if a is None or a==b["mtime"]:return
			c=ap(d)
			if c is None:return
			b["mtime"]=a;b["unread"]=False
			if c and aq(*ao(c))|af():b["ver"]+=1
		def ag():
			b["ver"]+=1
			if not b["dirty"]:b["dirty"]=True;b["dirty_at"]=time.time()
		def Q(res):j["n"]+=1;res["n"]=j["n"];j["q"]=j["q"]+[res]
		def ar():n=X["n"];return[f for f in j["q"]if f["n"]>n]
		def aQ():q=j["q"];return bool(q)and q[-1]["n"]>X["n"]
		def aR():
			for a in ar():X["n"]=a["n"];br(a)
		def bq(it):
			a,b=it,0
			while b<12:
				c=int(a.Container or 0)
				if c==0 or c<0x40000000:break
				e=API.FindItem(c)
				if e is None:return
				a,b=e,b+1
			else:return
			d=int(a.Container or 0);h=int(a.Serial)
			if int(a.Graphic)in aD or int(it.Graphic)in aD:return
			if d==0:
				if a.IsCorpse:return
				return("chest",a,None)if n["ground"]else None
			f=API.Player
			if f is None:return
			if d==int(f.Serial):g=int(API.Bank or 0);return("bank",a,None)if g and h==g and n["bank"]else None
			m=API.FindMobile(d);return("pack",a,m)if m is not None and bool(m.IsRenamable)and n["pack"]else None
		def aS(serial,final):
			d=API.FindItem(serial)
			if d is None:return
			s=bq(d)
			if s is None:return
			l,a,g=s;m=API.Player
			if m is None:return
			t=API.ItemsInContainer(serial,True)or[];q,n=0,0;h=[]
			for x in t:
				n+=1
				if n>S:break
				try:c,i,u=int(x.Serial),x.Amount,int(x.Container);q=(q*31+c+7*int(i or 0)+13*u)&0xFFFFFFFFFFFF
				except Exception:h.append(None);continue
				h.append((c,i,u))
			v=(q,n);bt(serial,h)
			if N.get(serial)==v and serial in b["recs"]:
				if len(j["q"])<40:Q({"serial":serial,"same":True,"at":time.time()})
				return True
			E,o=int(m.Serial),str(m.Name or "");F=int(API.GetMap()or 0);e={serial:[]};w,y={},{};n=0;z=False
			for x in t:
				n+=1
				if n>S:z=True;break
				try:
					A=h[n-1]
					if A is not None:c,i,k=A;f=max(1,int(i or 1))
					else:c=int(x.Serial);k=int(x.Container);f=None
					B=int(x.Graphic);G=int(x.Hue)
					if f is None:f=max(1,int(x.Amount or 1))
					C=ab(x,B,f)
					if bool(x.IsContainer):w[c]=k;y[c]=C
				except Exception:continue
				p=e.get(k)
				if p is None:p=e[k]=[]
				p.append((B,G,f,C))
			if not e[serial]and not final and len(e)==1:return False
			H=int(a.Serial);D=ab(a,int(a.Graphic),1)
			if l=="bank":r=("Bank box (%s)"%o)if o else "Bank box"
			elif l=="chest":r="%s at %d, %d"%(D or "Chest",int(a.X),int(a.Y))
			else:I=int(g.Graphic or 0);r=("%s %s"%(bb.get(I,"Pack animal"),str(g.Name or ""))).strip()
			J={"serial":serial,"parent":int(d.Container or 0),"kind":l,"root":H,"label":r,"top_name":D,"own_name":ab(d,int(d.Graphic),1),"cs":E,"cname":o,"facet":F,"x":int(a.X),"y":int(a.Y),"mob":int(g.Serial)if g is not None else 0,"by":e,"parents":w,"names":y,"capped":z,"at":time.time()}
			if len(j["q"])<40:
				Q(J)
				if len(N)>200:N.clear()
				N[serial]=v
			return True
		def aT(recs,s,b):
			a=0
			while s and a<14:
				if s==b:return True
				r=recs.get(s)
				if r is None:return False
				s,a=r["parent"],a+1
			return False
		def br(res):
			e=b["recs"];l=res.get("op")
			if l=="forget":bO(res["root"]);return
			if l=="name":
				r=e.get(res["root"])
				if r is not None:r["custom"]=res["text"];ag()
				return
			if l=="wipe":
				f=time.time()
				for s in list(e):b["tombs"][s]=f
				e.clear();ag();return
			if res.get("same"):
				i,f,c=res["serial"],res["at"],None
				for s,r in e.items():
					if aT(e,s,i):r["seen"]=f;c=r["root"]
				p=d["places"].get(c)if c is not None else None
				if p is not None:p["seen"]=f;a["dirty"]=True
				return
			i,c,f=res["serial"],res["root"],res["at"]
			if i==c:k=[b1 for b1,b2 in e.items()if b2["root"]==c or b1==c]
			else:k=[b3 for b3 in e if aT(e,b3,i)]
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
				if g is None:g=e[c]=an(c);g["stub"]=True
				g.update(m);g["parent"]=0;g["label"]=res["label"]
				if g["stub"]:g["seen"]=max(g["seen"],f)
			for h,z in res["by"].items():
				r=an(h);r.update(m);r["custom"]=q.get(h,"");r["seen"]=f
				if h==c:r["parent"],r["label"]=0,res["label"]
				elif h==i:r["kind"],r["parent"],r["label"]="bag",res["parent"],res["own_name"]
				else:r["kind"],r["parent"]="bag",res["parents"].get(h,0);r["label"]=res["names"].get(h,"Bag")
				u=r["items"]
				for A,B,v,w in z:
					x=(A,B,w.lower());y=u.get(x)
					if y is None:u[x]=[w,v]
					else:y[1]+=v
				e[h]=r;b["tombs"].pop(h,None)
			b["tombs"].pop(c,None);af();ag();a["last_read"]=(res["label"],f,res["kind"])
		def bs(*b):
			if not c["active"]:return
			for a in reversed(b):
				s=None
				try:s=int(a)
				except Exception:
					try:s=int(a.Serial)
					except Exception:s=None
				if s and s>=0x40000000:
					if len(L)<40:L.append(s)
					return
		def bt(root,first):
			if len(P)>a7 or len(r)>a8:
				a=set(i for i in r if i not in g)or set(r[:max(1,len(r)//2)])
				for k in[p for p,q in P.items()if q in a]:del P[k]
				r[:]=[s for s in r if s not in a]
			if root in r:r.remove(root)
			r.append(root)
			for f in first:
				if f is not None:P[f[0]]=root
		def aU(*d):
			if not c["active"]or not g or len(C)>=a6:return
			for a in d:
				try:s,e=int(a.Serial),int(a.Container)
				except Exception:continue
				for k in(e,s):
					b=k if k in g else P.get(k)
					if b is not None:C.add(b)
				return
		def bu():Kit.hook_once(c,"hooked",("OnOpenContainer",bs),("OnItemCreated",aU),("OnItemUpdated",aU))
		def bv(serial):
			a=time.time();w=g.get(serial)
			if w is None and len(g)>=a4:b=min(g,key=lambda k:g[k][0]);g.pop(b,None)
			g[serial]=[a,a+F[0],0]
		def bw(now):
			if not g:
				if C:C.clear()
				return
			if C:
				d=list(C);C.difference_update(d);e=now+a5
				for s in d:
					w=g.get(s)
					if w is not None and w[2]>=len(F)and w[1]>e:w[1]=e
			f=now>=c.get("check_at",0.)or c.get("check_at",0.)-now>az
			if f:c["check_at"]=now+az
			for a in list(g):
				w=g[a];h=False
				if f and w[2]>=len(F):
					b=API.FindItem(a);h=b is None or not bool(b.Opened)
					if b is None:g.pop(a,None);continue
				if h or now-w[0]>a3:aS(a,True);g.pop(a,None);continue
				if now<w[1]and w[1]-now<=ay+1.:continue
				i=aS(a,w[2]>=len(F)-1)
				if i is None:g.pop(a,None);continue
				w[2]+=1;w[1]=w[0]+F[w[2]]if w[2]<len(F)else now+ay
		def bx():
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
			d.update({"ver":b["ver"],"keys":g,"places":f,"items":n,"chars":len(i)});by(f,sorted(set(q["cs"]for q in h.values()if q["cname"])));a["dirty"]=True
		def aV(label):return re.sub(r" at \d+, \d+$"," at "+Kit.veil("xy",""),label)
		def by(places,g):
			d["veil"]=Kit.streamer
			if not Kit.streamer:return
			e=K();f=int(e.Serial)if e is not None else 0;a=[i for i in g if i!=f]
			for p in places.values():
				b,c=p["cs"],p["cname"]
				if c:p["cname"]=Kit.veil("me",c)if b==f else "Character %d"%(a.index(b)+2 if b in a else len(a)+2)
				if p["custom"]:continue
				if p["kind"]=="bank":p["label"]=("Bank box (%s)"%p["cname"])if c else "Bank box"
				elif p["kind"]=="chest":p["label"]=aV(p["label"])
		def aW():
			b=(d["ver"],tuple(p for q,p in e))
			if Z["key"]!=b:
				c=[];i=d["keys"]
				for n,j in e:
					k=ac(j);f,a=0,{}
					for l,m in i.items():
						if ad(k,l):
							for g,h in m[1].items():a[g]=a.get(g,0)+h;f+=h
					c.append((f,a))
				Z["key"],Z["stats"]=b,c
			return Z["stats"]
		def aX(q):
			c=(d["ver"],q.lower())
			if aa["key"]!=c:
				g=ac(q);a={}
				for k,e in d["keys"].items():
					if ad(g,k):
						for f,h in e[1].items():
							b=a.get(f)
							if b is None:b=a[f]={}
							b[k]=(e[0],h)
				aa["key"],aa["by"]=c,a
			return aa["by"]
		def bz(i):
			def a(*b):a=Follow.alt_held();B.add(("row",i,a,time.time()),dup=True,cap=20)
			return a
		def at():
			t=z.slot if u(D)else None;w,k=t or(al,W);v=z.rows(G,W-O*G,O,4);b,l=w-2*M,k-(W-aH);m=V+l+Kit.GAP;a["iw"]=b;g,d,i=z.begin(be if c["minimized"]else w,bf if c["minimized"]else k);f=[]
			if not c["minimized"]:
				z.frame(g);Kit.add_section(g,M,I,b,aG);n=35+Kit.text_w("Add favourite");Kit.add_label(g,"Find:",M+10,I+12,Kit.HUE_TEXT);o=M+16+Kit.text_w("Find:");x=b-(o-M)-n-22;i["box"]=Kit.with_tip(Kit.add_textbox(g,a["query"],o,I+9,x,numbers=False),"Part of a name, or a graphic (0x0F88); commas for several; empty: favourites");Kit.art_button(g,d,"fav",Kit.ART_OK,M+b-n-6,I+8,"Add favourite","Add the Find box text to your favourites",on_click=B("fav"));e=I+36;j=M+10;Kit.art_button(g,d,"name",Kit.ART_OK,j,e,"Name","Name the picked place: type it in the Find box, then click Name again",on_click=B("name"));j+=35+Kit.text_w("Name")+12;Kit.art_button(g,d,"forget",Kit.ART_CLOSE,j,e,"Forget","Drop the picked place and its bags from the index (click twice)",on_click=B("forget"));y=35+Kit.text_w("Next");p=M+b-y-6;Kit.art_button(g,d,"next",Kit.ART_PAGE,p,e,"Next","Next page",on_click=B("next"));q=p-12-(35+Kit.text_w("Prev"));Kit.art_button(g,d,"prev",Kit.ART_PAGE,q,e,"Prev","Previous page",on_click=B("prev"));i["page"]=Kit.add_label(g,"",q-50,e+3,Kit.HUE_INFO);Kit.add_section(g,M,V,b,l)
				for r in range(v):h=V+8+r*G;s={"l":Kit.add_label(g,"",M+10,h,Kit.HUE_TEXT),"r":Kit.add_label(g,"",M+b-60,h,Kit.HUE_INFO),"lx":M+10,"rx":M+b-60,"tip":"","y":h};s["c"]=Kit.catcher(g,M+4,h-2,b-8,G,bz(r));f.append(s)
				Kit.add_section(g,M,m,b,aI);i["status"]=Kit.add_label(g,"",M+10,m+7,Kit.HUE_INFO)
			a.update({"data":[None]*len(f),"prev":[(None,0.)]*len(f),"seen_text":None,"built_for":None,"dirty":True});z.end(g,{"rows":f});aZ(time.time())
		z=Kit.Window(D,E,c,h,at,a1,aw,(240,160),icon=bg,cleanup=am,clear={"rows":[]})
		def aY():return h["g"]is not None and not c["minimized"]and not c["docked"]
		def m(text,hue=None):a["status"]=text;a["status_hue"]=Kit.HUE_INFO if hue is None else hue;a["status_at"]=time.time()
		def bA():
			n=len(d["places"])
			if not b["loaded"]:return "Reading the index"
			if b["err"]:return "Index file: %s"%b["err"]
			c,t,e=a["last_read"];s="%s noted"%Kit.count(n,"place")
			if Kit.streamer and e=="bank":c="Bank box (%s)"%Kit.veil("me","")
			elif Kit.streamer and e=="chest":c=aV(c)
			if d["chars"]>1:s+=" on %d characters"%d["chars"]
			if c:s+="; last read %s"%c
			return s
		def bB(p,root):
			a=""
			if p["kind"]=="chest"and not Kit.streamer:a=" (facet %d, %d, %d)"%(p["facet"],p["x"],p["y"])
			c=(" by %s"%p["cname"])if p["cname"]else "";b="%s\nSeen%s %s%s\nClick to pick it (then Name or Forget)"%(p["label"],c,Kit.ago(time.time()-p["seen"],aJ),a)
			if p["mob"]:b+="\n"+aF
			return b
		def bC(now):
			b=[];B=a["live"];C=d["places"];q=a["query"]
			if not q:
				if not e:return[("No favourites yet: type a name, then click Add favourite.","",Kit.HUE_INFO,0,"",None)]
				b.append(("FAVOURITES  (click one to see where)","",Kit.HUE_TITLE,0,"Totals across the account: every place noted, and your backpack now",None));D=aW()
				for E,(F,w)in enumerate(e):
					x=ac(w);i,G=D[E]if E<len(D)else(0,{});c=sum(b2[1]for b1,b2 in B.items()if ad(x,b1));i+=c;r=len(G)+(1 if c else 0);s=[]
					if c:s.append("On you now: %s"%l(c))
					for f,g in sorted(G.items(),key=lambda a:-a[1])[:10]:p=C.get(f);s.append("%s: %s"%(p["label"]if p else "?",l(g)))
					t="%s (%s)\n%s\nClick to see where"%(F,w,"\n".join(s)if s else "None noted");b.append((F,("%s in %s"%(l(i),Kit.count(r,"place")))if i else "none",Kit.HUE_TEXT,0,t,("fav",w)))
				return b
			x=ac(q);y=aX(q);c=dict((b3,(b4[0],b4[1]))for b3,b4 in B.items()if ad(x,b3));r=len(y)+(1 if c else 0)
			if not r:return[("Nothing noted holds \"%s\"."%q,"",Kit.HUE_INFO,0,"Open the container it is in once (bank box, chest, pack animal) and it is noted",None)]
			z,j={},{}
			for f,u in y.items():
				H=0
				for A,v in u.items():H+=v[1];j[A]=v[0]
				z[f]=H
			i=sum(z.values())+sum(b5 for b6,b5 in c.values())
			for A,v in c.items():j[A]=v[0]
			J=list(j.values())[0]if len(j)==1 else "%d kinds"%len(j);b.append((J,"%s in %s"%(l(i),Kit.count(r,"place")),Kit.HUE_TITLE,0,"Everything noted that matches \"%s\""%q,None));h=0
			if c:
				I=Kit.veil("me",str(safe(lambda:API.Player.Name,"")or ""));b.append(("Backpack%s"%((" (%s)"%I)if I else ""),"on you now",Kit.HUE_TITLE,0,"Your backpack and the bags in it, right now",None));k=sorted(c.items(),key=lambda a:-a[1][1]);m=max(0,U-len(b));h+=max(0,len(k)-m)
				for n,(o,g)in k[:m]:b.append((o,l(g),Kit.HUE_TEXT,14,"%s x%s on you (graphic 0x%04X, hue %d)"%(o,l(g),n[0],n[1]),None))
			K=sorted(y.items(),key=lambda a:-z[a[0]])
			for f,u in K:
				p=C.get(f)
				if p is None:continue
				if len(b)>=U:h+=1+len(u);continue
				L=Kit.HUE_GOOD if a["sel"]==f else Kit.HUE_TITLE;b.append((p["label"],"seen %s"%Kit.ago(now-p["seen"],aJ),L,0,bB(p,f),("place",f,p["mob"],True)));M=("place",f,p["mob"],False);k=sorted(u.items(),key=lambda a:-a[1][1]);m=max(0,U-len(b));h+=max(0,len(k)-m)
				for n,(o,g)in k[:m]:
					t="%s x%s in %s (graphic 0x%04X, hue %d)\nClick to pick this place"%(o,l(g),p["label"],n[0],n[1])
					if p["mob"]:t+="\n"+aF
					b.append((o,l(g),Kit.HUE_TEXT,14,t,M))
			if h:b.append(("%s more line%s: type more of the name"%(l(h),""if h==1 else "s"),"",Kit.HUE_INFO,0,"A search lists %d lines at most; the total above counts them all"%U,None))
			return b
		def aZ(now):
			l=h["g"]
			if l is None or c["docked"]:return
			j=h["c"]
			if c["minimized"]:n=len(d["places"]);a["status_key"]=None;Kit.set_text(j.get("status"),E+": "+("%s noted"%Kit.count(n,"place")if b["loaded"]else "reading the index"),Kit.HUE_INFO);return
			e=(a["query"],d["ver"],a["live_ver"],a["sel"],a["page"],int(now//30))
			if a["dirty"]or e!=a["built_for"]:
				a["dirty"]=False;a["built_for"]=e;a["rows"]=bC(now);f=a_()
				if a["page"]>=f:a["page"]=f-1;a["built_for"]=(e[0],e[1],e[2],e[3],a["page"],e[5])
				bD(now,f)
			if(a["status"]and a["naming"]is None and not 0<=now-a["status_at"]<=8.):a["status"]=""
			g=j.get("status");k=(g,a["status"],a["status_hue"],b["loaded"],b["err"],len(d["places"]),d["chars"],a["last_read"]);i=a.get("status_key")
			if i is not None and i[0]is g and i[1:]==k[1:]:return
			a["status_key"]=k;Kit.set_text(g,Kit.fit(a["status"]or bA(),a["iw"]-20),a["status_hue"]if a["status"]else Kit.HUE_INFO)
		def bD(now,pages):
			k=h["rows"];q=a["page"]*len(k);e,s=a["data"],a["prev"];l=M+a["iw"]-10
			for i,r in enumerate(k):
				m=q+i
				if m<len(a["rows"]):f,b,n,o,c,g=a["rows"][m]
				else:f,b,n,o,c,g="","",Kit.HUE_TEXT,0,"",None
				p=Kit.text_px(b)if b else 0;d=M+10+o;t=l-d-(p+8 if b else 0);Kit.set_text(r["l"],Kit.fit(f,t)if f else "",n);Kit.set_text(r["r"],b,Kit.HUE_INFO)
				if d!=r["lx"]:r["lx"]=d;Kit.ui_pos(r["l"],d,r["y"])
				j=l-p
				if b and j!=r["rx"]:r["rx"]=j;Kit.ui_pos(r["r"],j,r["y"])
				if c!=r["tip"]:r["tip"]=c;r["c"].SetTooltip(c)
				if g!=e[i]:s[i]=(e[i],now);e[i]=g
			u=h["c"];Kit.set_text(u.get("page"),"%d / %d"%(a["page"]+1,pages)if pages>1 else "",Kit.HUE_INFO)
		def bE(now):
			b=h["c"].get("box")
			if b is None:return
			t=str(b.Text or "")
			if t!=a["seen_text"]:
				if a["seen_text"]is not None:a["changed_at"]=now
				a["seen_text"]=t;return
			if a["changed_at"]and(now-a["changed_at"]>=ba or now<a["changed_at"]):
				a["changed_at"]=0.
				if a["naming"]is not None:return
				q=t.strip()
				if q.lower()!=a["query"].lower():a["query"]=q;a["page"]=0;a["dirty"]=True
		def ah(text):
			b=h["c"].get("box");a["seen_text"]=text;a["changed_at"]=0.
			if b is not None:b.SetText(text)
		def bF(now):
			if not aY():return
			if now<a["live_at"]and a["live_at"]-now<=aB:return
			a["live_at"]=now+aB;b={};c=A(True,1.);q,n=0,0
			for x in c:
				n+=1
				if n>S:break
				try:q=(q*31+int(x.Serial)+7*int(x.Amount or 0)+13*int(x.Container))&0xFFFFFFFFFFFF
				except Exception:continue
			if(q,n)==a["live_sig"]:return
			a["live_sig"]=(q,n)
			if c:
				n=0
				for x in c:
					n+=1
					if n>S:break
					try:g,h=int(x.Graphic),int(x.Hue);d=max(1,int(x.Amount or 1));e=ab(x,g,d)
					except Exception:continue
					k=(g,h,e.lower());f=b.get(k)
					if f is None:b[k]=[e,d]
					else:f[1]+=d
			if b!=a["live"]:a["live"]=b;a["live_ver"]+=1
		def bG(i,t):
			if i>=len(a["data"]):return
			c,b=a["prev"][i];return c if b and(b>=t or t-b<.15)else a["data"][i]
		def au():
			if a["naming"]is not None:a["naming"]=None;ah(a["query"])
		def bH(action,now):
			if c["minimized"]or c["docked"]:c["minimized"]=c["docked"]=False;HOST.dock_forget(D);Kit.save_min(aw,False);at()
			safe(lambda:Kit.client_control(h["g"]).BringOnTop())
		def bI(action,now):H(action[1],E)
		def bJ(action,now):
			e,i,c,t=action;b=bG(i,t)
			if b is None:return
			if c:
				if len(b)>2 and b[2]:H(b[2],E)
				return
			au()
			if b[0]=="fav":a["query"]=b[1];a["page"]=0;ah(b[1]);m("")
			elif b[0]=="place":a["sel"]=None if(b[3]and a["sel"]==b[1])else b[1];p=d["places"].get(a["sel"])if a["sel"]else None;m(("Picked: %s"%p["label"])if p else "")
			a["dirty"]=True
		def bK(action,now):
			au();q=a["query"]or(a["seen_text"]or "").strip()
			if not q:m("Type what to look for first (a name, or a graphic like 0x0F88).",Kit.HUE_BAD)
			elif any(f.lower()==q.lower()for i,f in e):m("\"%s\" is already a favourite."%q)
			elif len(e)>=aj:m("%d favourites at most: take one off on the settings page."%aj,Kit.HUE_BAD)
			else:e.append([v(q)[:aC],v(q)]);aN();o(D);m("Added \"%s\" to the favourites."%q,Kit.HUE_GOOD)
			a["dirty"]=True
		def bL(action,now):
			c=a["sel"];p=d["places"].get(c)if c else None
			if a["naming"]is not None:
				f=a["naming"];e=v(a["seen_text"]or "")[:aC];r=b["recs"].get(f);a["naming"]=None
				if r is not None:Q({"op":"name","root":f,"text":e});m(("Named it \"%s\"."%e)if e else "Its own name is back.",Kit.HUE_GOOD)
				ah(a["query"])
			elif p is None or c not in b["recs"]:m("Click a place in the list first, then Name.",Kit.HUE_BAD)
			else:a["naming"]=c;ah(p.get("raw",p["label"]));m("Type its new name in the Find box, then click Name again (empty: its own name).",Kit.HUE_TITLE)
		def bM(action,now):
			au();b=a["sel"];p=d["places"].get(b)if b else None;c,e=a["forget_arm"]
			if p is None:m("Click a place in the list first, then Forget.",Kit.HUE_BAD)
			elif c==b and 0<=now-e<=4.:a["forget_arm"]=(None,0.);Q({"op":"forget","root":b});a["sel"]=None;m("Forgot %s."%p["label"],Kit.HUE_GOOD)
			else:a["forget_arm"]=(b,now);m("Click Forget again to forget %s (and the bags in it)."%p["label"],Kit.HUE_TITLE)
		def a_():b=max(1,len(h["rows"]));return max(1,(len(a["rows"])+b-1)//b)
		def a0(action,now):b=a_();a["page"]=max(0,min(b-1,a["page"]+(1 if action=="next"else-1)));a["dirty"]=True
		bN={"show":bH,"follow":bI,"row":bJ,"fav":bK,"name":bL,"forget":bM,"next":a0,"prev":a0}
		def bO(root):
			a=b["recs"];c=time.time()
			for s in[f for f,i in a.items()if i["root"]==root or f==root]:del a[s];b["tombs"][s]=c
			ag()
		def bP():return 32+max(1,len(e))*24+8
		def bQ(f,x,y):
			if not e:Kit.add_label(f.g,"No favourites yet: type a name in the Find box, then click Add favourite.",x+12,y+2,Kit.HUE_INFO)
			for i,(b,c)in enumerate(e):a=y+i*24;Kit.art_button(f.g,f.store,"rm%d"%i,Kit.ART_CLOSE,x+12,a,None,"Take %s off the favourites"%b);Kit.add_label(f.g,Kit.fit(b,170),x+48,a+3,Kit.HUE_TEXT);Kit.add_label(f.g,Kit.fit(c,f.w-240),x+226,a+3,Kit.HUE_INFO)
		def bR(f,x,y):J["wipe_at"]=0.;f.c["wipe_lbl"]=Kit.art_button(f.g,f.store,"wipe",Kit.ART_CLOSE,x+12,y,"Forget everything","Empty the whole index, every character (click twice)")
		def bS(w):n,a=len(d["places"]),len(b["recs"]);c=os.path.basename(b["path"])if b["path"]else "(not known yet)";return(("WHAT IT NOTES  (when you open a container)",(("check","bank","Bank boxes (and the bags in them)","Note your bank box and its bags"),("check","ground","Chests and containers on the ground (in houses too)","Note chests and containers on the ground"),("check","pack","Your pack animals' packs","Note your pack horse, llama or beetle",{"h":23}),("num","days","Forget places not seen for:","Days a place stays after it was last opened (1-3650)","days",1,3650,{"lgap":6,"fw":44})),{"ch":24,"sh":134}),("FAVOURITES  (shown when the Find box is empty)",(("custom",0,bQ),),{"sh":bP()}),("THE INDEX  (every character of the account)",(("note",Kit.fit("%s, %s, %s, %s"%(Kit.count(n,"place"),Kit.count(a,"container"),Kit.count(d["items"],"item line"),Kit.count(d["chars"],"character")),w-24),{"hue":Kit.HUE_TEXT}),("note",Kit.fit("File: %s, in VirtueAssistantSettings"%c,w-24),{"h":14}),("custom",0,bR)),{"sh":92}))
		def bT(f,new):d=Kit.read_int(f.c["days"],0);new["days"]=min(3650,d)if d>=1 else n["days"]
		def bU(f):
			b,c=f.store,f.c
			for i in range(len(e)):
				if Kit.was_clicked(b,"rm%d"%i):del e[i];aN();a["dirty"]=True;o(D);return
			d=J["wipe_at"]
			if d and not 0<=time.time()-d<=4.:J["wipe_at"]=0.;Kit.set_text(c.get("wipe_lbl"),"Forget everything",Kit.HUE_TEXT)
			if Kit.was_clicked(b,"wipe"):
				g=time.time()
				if 0<=g-J["wipe_at"]<=4.:J["wipe_at"]=0.;Q({"op":"wipe"});N.clear();a["sel"]=None;API.SysMsg("%s: the index is empty."%E,Kit.HUE_GOOD);o(D)
				else:J["wipe_at"]=g;Kit.set_text(c.get("wipe_lbl"),"Click again to empty it",Kit.HUE_BAD)
		ai=Kit.Page(n,bS,bk,adjust=bT,clicks=bU)
		def bV():c.update({"shutting":False,"docked":False,"queue":[],"active":True,"check_at":0.,"merge_at":0.,"minimized":z.start_min()});aM();bl();g.clear();j["q"]=ar();del L[:];a.update({"sel":None,"naming":None,"status":"","page":0,"dirty":True});b["path"]=Kit.data_path(bc%bm());bu();at();z.dock(fit=True,min=(al,W-(O-4)*G));am.service("storage.show",B("show"))
		def bW():
			if h["g"]is None:return
			if Kit.closed(h):return
			a=time.time()
			if j["q"]and j["q"][0]["n"]<=X["n"]:j["q"]=ar()
			while L:bv(L.pop(0))
			bw(a)
			while c["queue"]:
				b=c["queue"].pop(0)
				if not z.action(b):
					d=bN.get(b[0]if isinstance(b,tuple)else b)
					if d is not None:d(b,a)
				if h["g"]is None:return
			if aY():bE(a);bF(a)
			aZ(a)
		def bX():
			if c["shutting"]:return
			if not b["loaded"]:
				try:aO()
				except Exception as f:b["loaded"],b["err"]=True,str(f)[:60]
			aR();e=time.time()
			if b["dirty"]and(e-b["dirty_at"]>=aA or e<b["dirty_at"]):aP();c["merge_at"]=e+T
			elif e>=c["merge_at"]or c["merge_at"]-e>T:c["merge_at"]=e+T;bp()
			if d["ver"]!=b["ver"]or d["veil"]!=Kit.streamer:
				bx();aW()
				if a["query"]:aX(a["query"])
		def bY():
			if c["shutting"]:return False
			if not b["loaded"]or aQ()or d["ver"]!=b["ver"]or d["veil"]!=Kit.streamer:return True
			a=time.time()
			if b["dirty"]and(a-b["dirty_at"]>=aA or a<b["dirty_at"]):return True
			return a>=c["merge_at"]or c["merge_at"]-a>T
		aM()
		def bZ():
			c["shutting"]=True;c["active"]=False
			if aQ()or b["dirty"]:
				with Kit.quiet:
					if not b["loaded"]:aO()
					aR();aP()
			g.clear();del L[:];am.close()
		return{"start":bV,"tick":bW,"stop":bZ,"client_tick":True,"config_height":ai.height,"build_config":ai.build,"poll_config":ai.poll,"config_closed":ai.closed,"thread_tick":bX,"thread_wanted":bY}
	def an():
		t="restock";G="Restock";af="Restock_settings";aC="Restock_pos";aD="Restock_min";ag="Restock_targets";ah=400;aE,aF=240,46;aG=3705;z=22;T=20;aH=12;aI=(4014,4016,4015);e=.7;aJ=3.;H=10.;aK=3;aL=3;D=H;ai=3.;aj=2;aM=0;U=60000;aN=1.;aO=.25;aP=20.;aQ=("cannot hold more",);aR=("must wait to perform another action",);aS=("can not pick that up","cannot pick that up","that is too far away","that is out of sight","does not belong to you","already holding an item");aT={"REAGENTS":.1,"POTIONS":1.,"SCROLLS":1.,"OTHER":.1};ak=(40.,3.5);al="restock.stopped";aU=74;aV=8198;l=tuple(br[0]for br in v);p=dict((bs[0],bs)for bs in v);am=dict((bt[3],bt[0])for bt in v);aW=("last","bank","pick");an=(("last","Last opened","Take from the container you opened last"),("bank","Bank box","Take from your bank box (say \"bank\" near a banker to open it)"),("pick","Pick...","Target a chest to take from; remembered, opened once if closed"));ao=(("pack","Backpack","Restock into your backpack"),("bag","Pick bag...","Target a bag in your backpack to restock into"));b={"deep":True,"src_deep":True,"src":"last","src_serial":0,"dest":0};i={};bq=dict(b);a={"shutting":False,"minimized":False,"docked":False,"queue":[],"run":None,"halt":False,"status":("Idle",Kit.HUE_INFO),"last_open":0,"opened":[],"page":0,"count_at":0.,"short":{},"layout":None,"hooked":False,"active":False,"redraw":False,"shown_moved":0,"sent_at":0.,"flight":[]};j={"g":None,"c":{},"store":({},{}),"rows":[],"tips":{}};W,m,f=Kit.basics(a,G)
		def aX():pass
		def ap():
			b.update({"deep":True,"src_deep":True,"src":"last","src_serial":0,"dest":0})
			for a in Kit.get_var(af).split(";"):
				if "="not in a:continue
				k,v=[c.strip()for c in a.split("=",1)]
				if k in("deep","src_deep"):b[k]=v=="1"
				elif k=="src"and v in aW:b["src"]=v
				elif k in("src_serial","dest"):
					try:b[k]=max(0,int(v))
					except ValueError:pass
			i.clear()
			for a in Kit.get_var(ag).split(","):
				if "="not in a:continue
				k,v=[g.strip()for g in a.split("=",1)]
				if k in p and v.isdigit():
					n=min(U,int(v))
					if n>0:i[k]=n
		def E():Kit.put_var(af,"deep=%d;src_deep=%d;src=%s;src_serial=%d;dest=%d"%(b["deep"],b["src_deep"],b["src"],b["src_serial"],b["dest"]))
		def d(obj,a,default=0):
			try:v=getattr(obj,a);return default if v is None else int(v)
			except Exception:return default
		def aq(c):return not c or c==0xFFFFFFFF
		ar=Kit.top_of;I=Kit.in_pack
		def J():return int(API.Backpack or 0)
		def X():return int(API.Bank or 0)
		def at(it,fallback="container"):
			try:n=str(it.Name or "").strip()
			except Exception:n=""
			return n or fallback
		def q(serial,deep):
			try:return list(API.ItemsInContainer(int(serial),bool(deep))or[])
			except Exception:return[]
		Z=Kit.held_item
		def au():return bool(Q(t)or API.HasTarget())
		def av():d=b["dest"];return d if d else J()
		def ab(dest,deep=None,max_age=0.):
			d=J()
			if not d:return{}
			if b["deep"]if deep is None else deep:a=A(True,max_age)
			else:
				a=A(False,max_age)
				if dest and dest!=d:a=a+q(dest,False)
			c={}
			for e in a:
				try:
					k=am.get(int(e.Graphic))
					if k is None:continue
					c[k]=c.get(k,0)+max(1,int(e.Amount or 1))
				except Exception:continue
			return c
		def aY(src,deep):
			b={}
			for a in q(src,deep):
				try:
					k=am.get(int(a.Graphic))
					if k is None:continue
					b.setdefault(k,[]).append((max(1,int(a.Amount or 1)),int(a.Serial)))
				except Exception:continue
			return b
		def aZ():
			try:
				p=API.Player;w=float(p.Weight or 0);a=float(p.WeightMax or 0)
				if a<=0:a=ak[0]+ak[1]*float(p.Strength or 0)
				return None if a<=0 else a-aM-w
			except Exception:return
		def aw():
			e=b["src"]
			if e=="bank":
				d=X()
				if not d:return(0,"Your bank box (not open)","open your bank box first (say \"bank\" near a banker)")
				try:f=len(API.ItemsInContainer(d,False)or())>0
				except Exception:f=False
				return d,"Your bank box"+(""if f else " (not open)"),None
			if e=="pick":
				s=b["src_serial"]
				if not s:return 0,"Nothing picked yet","pick the chest first (Pick...)"
				c=API.FindItem(s)
				if c is None:return(0,"The picked chest (out of view)","the chest you picked is out of view")
				return s,ac(c),None
			s=a["last_open"];c=API.FindItem(s)if s else None
			if c is None:return 0,"Last opened: none yet","open a chest or your bank box first"
			return s,"Last opened: "+ac(c),None
		def ac(it):
			if int(it.Serial)==X():return "your bank box"
			a=at(it)
			if d(it,"OnGround")or aq(d(it,"Container")):return "%s at %d, %d"%(a,d(it,"X"),d(it,"Y"))
			return a
		def ax():
			d=b["dest"]
			if not d:return "Your backpack",None
			a=API.FindItem(d)
			if a is None or not I(d):return "The picked bag (not in your backpack)","the bag you picked isn't in your backpack: pick it again or choose Backpack"
			return at(a,"bag")+" in your backpack",None
		def ad(serial):
			if not serial:return "nothing was targeted"
			a=API.FindItem(serial)
			if a is None:return "that isn't an item"
			b,c=ar(serial);t=API.FindItem(b)if b!=int(serial)else a
			for x in(a,t):
				if x is not None and(d(x,"Graphic")==aV or d(x,"IsCorpse")):return "a corpse (or a bag in one) isn't a source"
			if I(serial):return "that is in your backpack"
			return "that isn't a container"if not(d(a,"IsContainer")or q(serial,False))else None
		def ay(src):
			c=API.FindItem(src)
			if c is None:return "the source is out of view"
			e,a=ar(src)
			if a:
				p=API.Player
				if a==d(p,"Serial"):return
				m=API.FindMobile(a)
				if m is None or not d(m,"IsRenamable"):return "the source is on someone else"
				b=max(abs(d(m,"X")-d(p,"X")),abs(d(m,"Y")-d(p,"Y")));return "your pack animal is out of reach (step next to it)"if b>aj else None
			t=API.FindItem(e)
			if t is None:return
			try:p=API.Player;b=max(abs(d(t,"X")-d(p,"X")),abs(d(t,"Y")-d(p,"Y")))
			except Exception:return
			return "the source is out of reach (step next to it)"if b>aj else None
		def a_(*c):
			if not a["active"]:return
			for b in c:
				try:s=int(b.Serial or 0)
				except AttributeError:
					try:s=int(b or 0)
					except Exception:s=0
				except Exception:s=0
				if s:a["opened"].append(s);del a["opened"][:-8];return
		def a0():Kit.hook_once(a,"hooked",("OnOpenContainer",a_))
		def a1():
			while a["opened"]:
				s=a["opened"].pop(0)
				if ad(s)is None:a["last_open"]=s
		def h(text,hue=None):
			a["status"]=(text,Kit.HUE_INFO if hue is None else hue);b=j["c"].get("status")
			if b is not None:
				if a["minimized"]:text=G+": "+text[:1].lower()+text[1:]
				Kit.set_text(b,Kit.fit(text,j["c"].get("status_w",200)),a["status"][1])
		def a2():
			if a["run"]is not None:f("already restocking; press Stop first.",Kit.HUE_BAD);return
			k=[w for w in l if i.get(w,0)>0]
			if not k:f("the list is empty: set how many of each item to carry on the settings page.",Kit.HUE_BAD);Y(t);return
			g,n,c=aw()
			if c is None:c=ad(g)or ay(g)
			if c is None:
				m=av();c=None if m else "you have no backpack"
				if c is None:c=ax()[1]
			if c is None and au():c="a target cursor is up"
			if c is None and Z():c="you are holding an item"
			if c is None and d(API.Player,"IsDead"):c="you are dead"
			if c is not None:f("can't restock: %s."%c,Kit.HUE_BAD);h("Can't: "+c,Kit.HUE_BAD);return
			j=time.time();r={"src":g,"dest":m,"deep":b["deep"],"src_deep":b["src_deep"],"phase":"go","open_until":0.,"move":None,"check":None,"at":j,"hold":0.,"sent_at":0.,"last":0,"left":False,"c0":0,"moved":0,"moves":0,"refused":0,"streak":0,"waits":0,"why":None,"bad":set(),"limbo":[x for x in a["flight"]if 0<=x[2]-j<=D]}
			if 0<=j-a["sent_at"]<e:r["at"]=a["sent_at"]+e
			a.update({"flight":[],"short":{},"halt":False})
			if not q(g,False):
				if g==X():f("your bank box isn't open: say \"bank\" near a banker first.",Kit.HUE_BAD);h("Bank box not open",Kit.HUE_BAD);return
				API.UseObject(g);r.update({"phase":"open","open_until":j+ai});h("Opening the chest")
			else:h("Restocking")
			a["run"]=r;f("restocking %s."%Kit.count(len(k),"item"));F()
		def a3(r,key,now):
			n=0;a=[]
			for e in r["limbo"]:
				if 0<=e[2]-now<=D:
					a.append(e)
					if e[0]==key:n+=e[1]
			r["limbo"]=a;return n
		def a4(now):
			r=a["run"]
			if r is None or r["move"]is not None:return
			if r["check"]is not None and not r["left"]:
				b=API.FindItem(r["check"][1])
				if b is None or d(b,"Container")!=r["c0"]:r["left"]=True
			if r["why"]:k(r["why"]);return
			if r["phase"]=="open":
				if q(r["src"],False):r["phase"]="go";h("Restocking")
				elif not 0<=r["open_until"]-now<=ai:k("the chest didn't open (or it is empty)")
				return
			if r["check"]is not None:
				if 0<r["at"]-now<=e or not a6(r,now):return
			if 0<r["hold"]-now<=e or 0<r["at"]-now<=e:return
			if au():k("a target cursor is up");return
			c=Z()
			if c and not(c==r["last"]and 0<=now-r["sent_at"]<2*e):k("you picked something up");return
			if d(K(),"IsDead"):k("you died");return
			f=ay(r["src"])
			if f:k(f);return
			a5(r,now)
		def a5(r,now):
			g=ab(r["dest"],r["deep"]);v=aY(r["src"],r["src_deep"]);j=False
			for b in l:
				t=i.get(b,0)
				if t<=0:continue
				m=a3(r,b,now);f=t-g.get(b,0)-m
				if f<=0:
					if m:j=True
					a["short"].pop(b,None);continue
				n=[x for x in v.get(b,())if x[1]not in r["bad"]]
				if not n:a["short"][b]=f;continue
				w,o=max(n);c=min(w,f);q=aZ()
				if q is not None:
					s=int(q/aT.get(p[b][1],1.)+1e-6)
					if s<1:k("you are at your weight limit");return
					c=min(c,s)
				a["short"].pop(b,None);u=API.FindItem(o);r["c0"]=d(u,"Container")if u is not None else 0;r["move"]=(b,o,c,g.get(b,0));h("Moving %d %s (%d moved)"%(c,p[b][2],r["moved"]));return
			if j:h("Waiting for the server");r["hold"]=now+e;return
			a9()
		def a6(r,now):
			b,c,a,j=r["check"];f=r["sent_at"]
			if B(f,aQ)is not None:k("your %s can't hold more"%("backpack"if r["dest"]==J()else "bag"));return False
			l=ab(r["dest"],r["deep"]).get(b,0);m=now-f;g=API.FindItem(c);n=d(g,"Container")if g is not None else 0;i=l>j
			if not i and g is not None and not aq(n)and n!=r["c0"]:
				i=I(c)
				if i:l=j+a
			if i:
				o=min(l-j,a);r["moved"]+=o
				if o<a:r["limbo"].append([b,a-o,now+D])
				r.update({"check":None,"left":False,"streak":0,"waits":0});return True
			p=g is not None and n==r["c0"]
			if not p or Z()==c:
				r["left"]=True
				if not 0<=m<H:k("the server hasn't answered a move for %d s"%int(H));return False
				if m>=2*e:h("Waiting for the server")
				r["at"]=now+e*.5;return False
			if B(f,aR)is not None and r["waits"]<aL:
				r["waits"]+=1
				if not r["left"]:r["limbo"].append([b,a,now+D])
				r.update({"check":None,"left":False,"hold":now+e});return False
			q=B(f,aS)is not None
			if not(q or r["left"])and 0<=m<aJ:r["at"]=now+e*.5;return False
			if not r["left"]:r["limbo"].append([b,a,now+D])
			r.update({"check":None,"left":False,"waits":0});r["refused"]+=1;r["streak"]+=1;r["bad"].add(c)
			if r["streak"]>=aK:k("%d moves in a row were refused"%r["streak"]);return False
			return True
		def a7():
			r=a["run"]
			if r is None or r["move"]is None:return
			b=r["move"];r["move"]=None
			if a["halt"]or a["shutting"]:return
			try:API.MoveItem(b[1],r["dest"],b[2])
			except Exception as c:r["why"]="a move failed (%s)"%c;return
			V();r.update({"check":b,"left":False,"last":b[1]});r["sent_at"]=a["sent_at"]=time.time();r["at"]=r["sent_at"]+e;r["moves"]+=1
		def a8():
			if not a["short"]:return ""
			b=["%s %d"%(p[c][2],g)for c,g in sorted(a["short"].items(),key=lambda a:l.index(a[0]))];return "; short (none left in the source): "+", ".join(b[:6])+(" and %d more"%(len(b)-6)if len(b)>6 else "")
		def ae(r):
			if r is None:return
			b=[list(g)for g in r["limbo"]]
			if r["check"]is not None:c,e,d,f=r["check"];b.append([c,d,r["sent_at"]+H])
			if b:a["flight"]=(a["flight"]+b)[-20:]
		def a9():
			r,a["run"]=a["run"],None
			if r is None:return
			ae(r);b=("done: %d moved in %s"%(r["moved"],Kit.count(r["moves"],"move")))
			if r["refused"]:b+=", %d refused"%r["refused"]
			f(b+a8()+".",Kit.HUE_BAD if a["short"]or r["refused"]else Kit.HUE_GOOD);h("Done: %d moved%s"%(r["moved"],", some short"if a["short"]else ""),Kit.HUE_TITLE if a["short"]else Kit.HUE_GOOD);a["count_at"]=0.;F()
		def k(why=None,user=False):
			r,a["run"]=a["run"],None;a["halt"]=True
			if r is None:return
			ae(r)
			if user:f("stopped (%d moved)."%r["moved"]);h("Stopped (%d moved)"%r["moved"])
			else:
				b="%s (%d moved)"%(why or "stopped",r["moved"])
				if not O(al,"Stopped: "+b,"warn"):f("stopped: "+b+".",Kit.HUE_BAD)
				h("Stopped: "+(why or ""),Kit.HUE_BAD)
			a["count_at"]=0.;F()
		def ba():a["halt"]=True;m("stop")()
		def bb():return[c for c in l if i.get(c,0)>0]
		M=2*Kit.MARGIN+30+3*Kit.GAP+136+64
		def N():d=bb();b=o.rows(z,M+S(0)-2*z,aH,2);e=max(1,(len(d)+b-1)//b);c=min(a["page"],e-1);return(a["minimized"],a["docked"],c,e,tuple(d[c*b:(c+1)*b]))
		def R():
			d=N();a["page"]=d[2];a["layout"]=d;B=a["minimized"];C=o.slot if u(t)else None;x,D=(aE,aF)if B else(C or(ah,M+S(len(d[4]))));g,n,i=o.begin(x,D);c=Kit.MARGIN;E=[]
			if B:i["status_w"]=x-90
			else:
				j=x-2*c;o.frame(g);k=c+30+Kit.GAP;Kit.add_section(g,c,k,j,136,"FROM AND TO");Kit.add_label(g,"From:",c+12,k+30,Kit.HUE_INFO);y=c+12+max(Kit.text_w("From:"),Kit.text_w("Into:"))+10;i["src"]=Kit.add_label(g,"",y,k+30);i["src_w"]=j-(y-c)-8;q=c+12
				for f,r,s in an:i["m_"+f]=Kit.art_button(g,n,"m_"+f,Kit.ART_PAGE,q,k+52,r,s,Kit.HUE_TITLE if b["src"]==f else Kit.HUE_TEXT,on_click=m(("src",f)));q+=35+Kit.text_w(r)+14
				Kit.add_label(g,"Into:",c+12,k+84,Kit.HUE_INFO);i["dest"]=Kit.add_label(g,"",y,k+84);q=c+12
				for f,r,s in ao:i["d_"+f]=Kit.art_button(g,n,"d_"+f,Kit.ART_PAGE,q,k+106,r,s,Kit.HUE_TITLE if(f=="bag")==bool(b["dest"])else Kit.HUE_TEXT,on_click=m(("dest",f)));q+=35+Kit.text_w(r)+14
				l=k+136+Kit.GAP;F=D-M if C else S(len(d[4]));Kit.add_section(g,c,l,j,F,"LIST  (carried / to carry)")
				if d[3]>1:A=c+j-12-21;Kit.art_button(g,n,"next",Kit.ART_PLAY,A,l+4,None,"Next page",on_click=m(("page",1)));Kit.add_label(g,"%d/%d"%(d[2]+1,d[3]),A-8-Kit.text_w("%d/%d"%(d[3],d[3])),l+6,Kit.HUE_INFO);Kit.art_button(g,n,"prev",aI,A-16-Kit.text_w("%d/%d"%(d[3],d[3]))-21,l+4,None,"Previous page",on_click=m(("page",-1)))
				if not d[4]:Kit.add_label(g,"The list is empty: set how many to carry",c+12,l+30,Kit.HUE_INFO);Kit.add_label(g,"on the "+G+" settings page.",c+12,l+50,Kit.HUE_INFO)
				H=c+j-100
				for K,I in enumerate(d[4]):v=l+28+K*z;Q,R,J,L=p[I];aa(g,L,0,c+12,v,T);Kit.add_label(g,Kit.fit(J,H-(c+12+T+6)-8),c+12+T+6,v+2);O=Kit.add_label(g,"",H,v+2);s=Kit.catcher(g,c+8,v,j-16,z,aX,J);E.append({"key":I,"count":O,"tip":s})
				w=l+F+Kit.GAP;Kit.add_section(g,c,w,j,64);Kit.art_button(g,n,"go",Kit.ART_PLAY,c+12,w+8,"Restock","Top each item up to its target from the source (one move every %.1f s)"%e,on_click=m("go"));P=c+12+35+Kit.text_w("Restock")+18;Kit.art_button(g,n,"stop",Kit.ART_CLOSE,P,w+8,"Stop","Stop moving items",on_click=ba);i["status"]=Kit.add_label(g,"",c+12,w+40,a["status"][1]);i["status_w"]=j-24
			o.end(g,{"rows":E,"tips":{}});h(*a["status"]);a["count_at"]=0.;az(time.time())
		o=Kit.Window(t,G,a,j,R,aC,aD,(240,220),icon=aG,cleanup=W,clear={"c":{},"rows":[]})
		def S(n):return 30+max(2,n)*z+6
		def F():
			e=j["c"]
			for a,d,f in an:
				c=e.get("m_"+a)
				if c is not None:Kit.set_text(c,d,Kit.HUE_TITLE if b["src"]==a else Kit.HUE_TEXT)
			for a,d,f in ao:
				c=e.get("d_"+a)
				if c is not None:Kit.set_text(c,d,Kit.HUE_TITLE if(a=="bag")==bool(b["dest"])else Kit.HUE_TEXT)
		def az(now):
			g=j["g"]
			if g is None or a["minimized"]:return
			if 0<=now-a["count_at"]<aN:return
			a["count_at"]=now;c=j["c"];r,h,s=aw();Kit.set_text(c["src"],Kit.fit(h,c["src_w"]));l,m=ax();Kit.set_text(c["dest"],Kit.fit(l,c["src_w"]),Kit.HUE_BAD if m else Kit.HUE_TEXT)
			if not j["rows"]:return
			o=ab(av(),None,0. if a["run"]is not None else.5);d=j["tips"]
			for b in j["rows"]:
				k=b["key"];n,t=o.get(k,0),i.get(k,0);q=Kit.HUE_GOOD if n>=t else(Kit.HUE_BAD if n==0 else Kit.HUE_TITLE);Kit.set_text(b["count"],"%d / %d"%(n,t),q);e=(n,t,a["short"].get(k))
				if d.get(k)==e:continue
				f="%s: %d in your pack, target %d"%(p[k][2],n,t)
				if k in a["short"]:f+=" (short by %d: none left in the source)"%a["short"][k]
				d[k]=e;b["tip"].SetTooltip(f)
		def bc(what):
			if a["run"]is not None:f("press Stop first.",Kit.HUE_BAD);return
			f("target the chest to take from."if what=="src"else "target a bag in your backpack.")
			def b(serial):m(("picked",what,int(serial or 0)))()
			L(aP,b,t)
		def bd(what,serial):
			if not serial:return
			if what=="src":
				e=ad(serial)
				if e:f("not a source: %s."%e,Kit.HUE_BAD);return
				b["src"],b["src_serial"]="pick",serial;E();c=API.FindItem(serial);f("taking from %s."%(ac(c)if c is not None else "it"),Kit.HUE_GOOD)
			else:
				g=J()
				if serial==g:b["dest"]=0
				else:
					c=API.FindItem(serial)
					if c is None or not I(serial)or not(d(c,"IsContainer")or q(serial,False)):f("pick a bag that is in your backpack.",Kit.HUE_BAD);return
					b["dest"]=serial
				E()
			a["count_at"]=0.;F()
		def aA(grp):return[c for c in v if c[1]==grp]
		def be(grp):n=len(aA(grp));return 30+((n+1)//2)*26+6
		def bf(action):
			if a["run"]is not None:k(user=True)
		def aB(action):
			c=action[0]
			if a["run"]is not None:f("press Stop first.",Kit.HUE_BAD)
			elif action[1]==("pick"if c=="src"else "bag"):bc(c)
			else:b[c]=action[1]if c=="src"else 0;E();a["count_at"]=0.;F()
		def bg(action):b=N()[3];a["page"]=(a["page"]+action[1])%b;R()
		bh={"go":lambda action:a2(),"stop":bf,"src":aB,"dest":aB,"picked":lambda action:bd(action[1],action[2]),"page":bg};bi=30+2*28+24+8
		def bj(w):a=(w-24)//2;return[("%s  (%s)"%(c,"how many to carry, 0 = leave alone"if c=="REAGENTS"else "how many to carry"),[("num",r,Kit.fit(n,a-76),"How many %s to carry (0-%d, 0 = leave it alone)"%(n,U),None,0,U,{"dx":12+(g%2)*a,"stay":g%2==0})for g,(r,x,n,y)in enumerate(aA(c))],{"sh":be(c),"lw":a-78,"fw":52,"fh":26})for c in C]+[("OPTIONS",(("check","deep","Count inside bags in your pack","Bags inside your backpack count too (as Inventory > Supplies and Grimoire)",{"h":28}),("check","src_deep","Take from bags inside the source too","Bags inside the chest or bank box too (only those whose contents you have seen)",{"h":30}),("note","One move every %.1f s; it stops when you pick something up."%e)),{"sh":bi})]
		def bk(old,new):
			if(new["deep"],new["src_deep"])!=(old["deep"],old["src_deep"]):b.update(deep=new["deep"],src_deep=new["src_deep"]);E();a["count_at"]=0.
			if any(new[c]!=old[c]for c in l):
				i.clear();i.update((g,new[g])for g in l if new[g]>0);Kit.put_var(ag,",".join("%s=%d"%(n,i[n])for n in l if i.get(n,0)>0));a["count_at"]=0.
				if N()!=a["layout"]:a["redraw"]=True
		s=Kit.Page(b,bj,None,bk,every=aO)
		def bl(g,x,y,w):s.vals=dict(b);s.vals.update((c,i.get(c,0))for c in l);s.build(g,x,y,w)
		def bm():a.update({"shutting":False,"docked":False,"queue":[],"run":None,"halt":False,"status":("Idle",Kit.HUE_INFO),"opened":[],"page":0,"count_at":0.,"short":{},"layout":None,"active":True,"redraw":False,"shown_moved":0,"minimized":o.start_min()});ap();P(al,"Restock stopped early",aU);a0();R();W.service("restock.run",m("go"));o.dock(fit=True,min=(ah,M+S(2)))
		def bn():
			if j["g"]is None:return
			if Kit.closed(j):return
			if a["opened"]:a1()
			while a["queue"]:
				b=a["queue"].pop(0)
				if o.action(b):continue
				c=bh.get(b[0]if isinstance(b,tuple)else b)
				if c is not None:c(b)
			if a["redraw"]:
				a["redraw"]=False
				if N()!=a["layout"]:R()
			d=time.time();r=a["run"]
			if r is not None:
				a4(d);a7()
				if r["moved"]!=a["shown_moved"]:a["shown_moved"]=r["moved"];a["count_at"]=0.
			az(d)
		def bo():return.05 if a["run"]is not None else.1
		ap()
		def bp():a.update({"shutting":True,"halt":True,"active":False});r,a["run"]=a["run"],None;ae(r);E();W.close()
		return{"start":bm,"tick":bn,"stop":bp,"client_tick":True,"config_height":s.height,"build_config":bl,"poll_config":s.poll,"config_closed":s.closed,"interval":bo}
	def ao():
		i="supplies";X="Supplies";av="UnitFrames_settings";F="UnitFrames_supset";aw=10.;ax=.5;ay=1.;H=220;I=22;r=20;Y=20;Z="UnitFrames_suppos";K=("Below the frame","Left of the frame","Right of the frame");az=10;aA=.1;aB=.25;j=tuple(a5+(None,)for a5 in v);aC=("bp","bm","ga","gi","mr","ns","ss","sa","p_heal","p_cure","p_refresh","s_recall","s_gate","o_band");ac="UnitFrames_supplies";ad="UnitFrames_supwarn";aD=Kit.HUE_TITLE;aE=.25;ae=9999;d={"sup_open":False,"sup_deep":True,"sup_hide0":False,"sup_follow":True,"sup_low":az,"sup_side":0};a3=dict(d);s={"sup_low":(0,9999),"sup_side":(0,2)};b={"minimized":False,"shutting":False,"docked":False,"next_supply":0.,"counts":{},"next_save":0.,"queue":[]};l={"g":None,"c":{},"store":({},{})};e=set(aC);a={"g":None,"c":{},"rows":(),"at":None,"slot":None,"drawn":None};k={};L={"next_warn":0.};t,M=Kit.get_var,Kit.put_var;B,N,a4=Kit.basics(b,X)
		def aF(key):Kit.kv_load(key,",",d,s)
		def af():aF(F if t(F,"")else av)
		def E():Kit.kv_save(F,",",d,sorted(d),s)
		def ag():
			a=t(ac,"-")
			if a=="-":return
			b=set(c[0]for c in j);e.clear();e.update(f for f in a.split(",")if f in b)
		def ah():M(ac,",".join(c[0]for c in j if c[0]in e)or "none")
		def ai():
			k.clear();d=set(f[0]for f in j)
			for b in t(ad,"").split(","):
				if "="not in b:continue
				c,v=b.split("=",1)
				if c not in d:continue
				a=[]
				for e in(v.split("/")+["",""])[:2]:
					try:a.append(max(0,min(ae,int(e))))
					except ValueError:a.append(None)
				if a[0]is not None or a[1]is not None:k[c]=a
		def aG():
			b=[]
			for r in j:
				a=k.get(r[0])
				if a:b.append("%s=%s/%s"%(r[0],""if a[0]is None else a[0],""if a[1]is None else a[1]))
			M(ad,",".join(b))
		def aH():
			b={}
			for a,m,n,k,c in j:
				if a in e:b.setdefault(k,[]).append((a,c))
			f=dict((w[0],0)for w in j if w[0]in e)
			if not b:return f
			for g in A(bool(d["sup_deep"]),ax):
				try:
					h=b.get(int(g.Graphic or 0))
					if not h:continue
					c=int(g.Hue or 0)&16383;l=max(1,int(g.Amount or 1))
				except Exception:continue
				for a,i in h:
					if i is None or i==c:f[a]+=l
			return f
		def O():return tuple((c,f,g)for c,f,g,h,w in j if c in e and not(d["sup_hide0"]and not b["counts"].get(c,0)))
		def aj(key):
			n=b["counts"].get(key,0);a=k.get(key);e=a[1]if a is not None and a[1]is not None else d["sup_low"]
			if n<=e:c=Kit.HUE_BAD
			else:c=aD if a is not None and a[0]is not None and n<=a[0]else Kit.HUE_TEXT
			return "{:,}".format(int(n)),c
		def ak():return bool(d["sup_follow"])and not u(i)
		def al():return a["slot"]if u(i)else None
		def P(rows,pitch):b=[(c,[g for g in rows if g[1]==c])for c in C if any(f[1]==c for f in rows)];a=[26+len(h)*pitch+4 for w,h in b]or[26+2*pitch+4];return b,a,16+sum(a)+Kit.GAP*(len(a)-1)
		def aI(w,h,mode):
			b=(int(w),int(h))if(w is not None and h is not None)else None
			if b!=a["slot"]or mode=="again":a["slot"]=b;a["drawn"]=False
		def aJ():return H,P(O(),Y)[2]
		def am(rows):
			d=a["g"];b=al();s=u(i);f=ak();c=Kit.pitch(I);k,l,h=P(rows,c);w=H if b is None else b[0]
			if b is not None:
				E=sum(len(a5)for a6,a5 in k)or 2;c=max(Y,min(2*I,c+(b[1]-h)//E));k,l,h=P(rows,c)
				if h<b[1]:l[-1]+=b[1]-h;h=b[1]
			g=G.CreateGump(True,not f and not z(i));Kit.add_window_frame(g,w,h,corners=False);v={};y=8;A=dict((a7,(a8,a9))for a7,ba,bb,a8,a9 in j)
			if not k:Kit.add_section(g,8,y,w-16,l[0],"SUPPLIES");F="None of these in your pack."if e else "No rows ticked yet.";Kit.add_label(g,F,18,y+26,Kit.HUE_INFO);Kit.add_label(g,"Pick rows: its settings page.",18,y+26+c,Kit.HUE_INFO)
			for(K,L),B in zip(k,l):
				Kit.add_section(g,8,y,w-16,B,K)
				for M,(n,T,O)in enumerate(L):o=y+26+M*c;aa(g,A[n][0],A[n][1],16,o+(c-r)//2-1,r);C,S=aj(n);o+=(c-I)//2;v[n]=Kit.add_label(g,C,w-18-Kit.text_w(C),o+2,S);Kit.add_label(g,Kit.fit(O,w-18-r-4-18-6-44),18+r+4,o+2)
				y+=B+Kit.GAP
			p=None
			if s:t=J(i);x,q=(t[0],t[1])if t is not None else Q()
			elif not f:
				Kit.catcher(g,0,0,w,h,lambda:None,"Drag to move the supplies table",movable=True);x,q=Q()
				if Kit.is_open(d):x,q=d.GetX(),d.GetY()
				Kit.place(g,x,q,w,h)
			else:D=R(w,h);p=D[1]if D is not None else Q();Kit.place(g,p[0],p[1],w,h)
			if not Kit.zone_up(i):Kit.art_button(g,({},{}),"close",Kit.ART_CLOSE,w-8-30,10,None,"Close the supplies list",on_click=N("close"))
			a.update({"g":g,"c":v,"rows":rows,"at":p,"w":w,"h":h,"follow":f,"leader":None,"drawn":b})
			if s:ab(i,g,Kit.show_window(g,x,q,w,h,i,False,None,None))
			else:Kit.add_front(g)
			if not f and not s:Kit.on_moved(g,m)
			Kit.dispose(d);U()
		aK=(60,620)
		def Q():
			b=t(Z,"");a["saved"]=b
			try:x,y=(int(f)for f in b.split(","));return Kit.adapt(x,y,a.get("w",0),a.get("h",0))
			except ValueError:c=R(a.get("w",H),a.get("h",0));return c[1]if c is not None else aK
		def m():
			g=a["g"]
			if Kit.is_open(g)and not a.get("follow",True)and not u(i):
				try:b="%d,%d"%(int(g.GetX()),int(g.GetY()))
				except Exception:return
				if b!=a.get("saved"):a["saved"]=b;M(Z,b)
		def R(w,h):
			a=HOST.services.get("frames.player_anchor")
			if a is None:return
			try:return a(w,h,d["sup_side"])
			except Exception:return
		def U():
			g=a["g"]
			if not Kit.is_open(g)or not a.get("follow",True):return
			d=R(a["w"],a["h"])
			if d is None:return
			c,b=d
			if a.get("leader")is not c:a["leader"]=c;Kit.attach(g,c)
			if b!=a["at"]:
				a["at"]=b
				try:Kit.place(g,b[0],b[1],a["w"],a["h"]);Kit.moved_by_code(g)
				except Exception:pass
		aL=620;aM="UnitFrames_rowspos";V="supplies_rows"
		def an():
			M,f=Kit.MARGIN,Kit.GAP;w=aL;b=w-2*M;o=max(sum(1 for G in j if G[1]==y)for y in C);h=52+o*ap+4;i=M+30+f+h+M;g,c,q=p.begin(w,i);Kit.add_window_frame(g,w,i);Kit.add_section(g,M,M,b,30);Kit.add_label(g,"SUPPLIES TABLE ROWS",M+30,M+7,Kit.HUE_TITLE);a=w-M-54-20-35-Kit.text_w("Untick all");Kit.art_button(g,c,"none",Kit.ART_CLOSE,a,M+4,"Untick all","Empty the table");a-=14+35+Kit.text_w("Tick all");Kit.art_button(g,c,"all",Kit.ART_OK,a,M+4,"Tick all","Show every row");Kit.catcher(g,M,M,a-M-6,30,lambda:None,"Drag to move",movable=not z(V))
			if not Kit.zone_up(V):Kit.art_button(g,c,"close",Kit.ART_CLOSE,w-M-54,M+4,None,"Close the table")
			d=M+30+f;Kit.add_section(g,M,d,b,h,"ROWS  (ticked rows show in the table)");k=(b-16)//len(C)
			for r,l in enumerate(C):
				m=M+10+r*k;Kit.add_label(g,l,m,d+30,Kit.HUE_TITLE)
				for s,(n,u,t,v,x)in enumerate(a5 for a5 in j if a5[1]==l):q[n]=Kit.add_check(g,Kit.fit(t,k-34),m,d+52+s*ap,n in e)
			p.end(g,{"next_poll":0.})
		p=Kit.Window(V,"Supplies Rows",b,l,an,aM,default=(260,160),cleanup=B,owner=False,clear={"c":{}})
		def ao(now):
			if not d["sup_open"]:
				if a["g"]is not None:m();i,a["g"]=a["g"],None;Kit.dispose(i)
				return
			f=now>=b["next_supply"]or not b["counts"]or(now>=b.get("sup_min",0.)and D()!=b.get("pack_v"))
			if f:b.update({"next_supply":now+ay,"sup_min":now+aA,"pack_v":D()});b["counts"]=aH()
			if not Kit.is_open(a["g"])or a.get("follow")!=ak()or a["drawn"]!=al():m();am(O())
			elif f:
				e=O()
				if e!=a["rows"]:m();am(e)
				else:
					for g,k,l in e:
						h,j=aj(g);c=a["c"].get(g)
						if c is not None and Kit.set_text(c,h,j):c.SetPos(a["w"]-18-Kit.text_px(h),c.GetY())
					U()
			else:U()
		def aN(now):
			g=l["g"]
			if g is None:return
			if not Kit.is_open(g):l.update({"g":None,"c":{}});return
			f,h=l["store"],l["c"]
			if Kit.was_clicked(f,"close"):p.close();return
			j=False
			for m,a in(("all",True),("none",False)):
				if Kit.was_clicked(f,m):
					j=True
					for c in h.values():c.SetIsChecked(a)
			if not j and not HOST.pass_poked and now<l.get("next_poll",0.):return
			l["next_poll"]=now+aB;d=set()
			for k,c in h.items():
				try:a=bool(c.IsChecked)
				except Exception:a=k in e
				if a:d.add(k)
			if d!=e:e.clear();e.update(d);ah();b["next_supply"]=0.;o(i)
		def aO(now):
			if not d["sup_open"]:d["sup_open"]=True;E();b["next_supply"]=0.
			ao(now);g=a["g"]
			if Kit.is_open(g):safe(lambda:Kit.client_control(g).BringOnTop())
		def aP(now):d["sup_open"]=False;E()
		aQ={"open":aO,"close":aP,"sup_rows":lambda now:an()};W=(("sup_follow","The table sticks to the player frame","Untick to drag it anywhere"),("sup_deep","Count inside bags in your backpack","Bags and pouches in your backpack count too"),("sup_hide0","Hide rows you have none of","Leave out rows at 0"));aR="A row at or below this shows red, unless it has its own Red below (0-%d)"%s["sup_low"][1];ap=24;aS=118;aq=26;n=44
		def ar():return[c for c in j if c[0]in e]
		def aT():return 30+20+max(1,(len(ar())+1)//2)*aq+4
		def aU(f,x,y):
			g,b=f.g,ar();c=(f.w-36)//2;j=[]
			if not b:Kit.add_label(g,"No rows ticked yet: click Choose rows above.",x+12,y+2,Kit.HUE_INFO)
			for o in range(2 if len(b)>1 else(1 if b else 0)):a=x+12+o*(c+12)+c-2*n-8;Kit.add_label(g,"Yellow",a,y-2,Kit.HUE_TITLE);Kit.add_label(g,"Red",a+n+8,y-2,Kit.HUE_BAD)
			for l,(m,r,e,s,t)in enumerate(b):h=x+12+(l%2)*(c+12);i=y+20+(l//2)*aq;a=h+c-2*n-8;Kit.add_label(g,Kit.fit(e,a-h-8),h,i+3);d=k.get(m)or(None,None);p=Kit.with_tip(Kit.add_textbox(g,""if d[0]is None else str(d[0]),a,i,n),"Yellow at or below this many %s (empty: never)"%e);q=Kit.with_tip(Kit.add_textbox(g,""if d[1]is None else str(d[1]),a+n+8,i,n),"Red at or below this many %s (empty: Red at or below above)"%e);j.append((m,p,q))
			f.c["warn"]=j
		def aV(w):return(("TABLE",(("check",)+W[0]+({"stay":True},),("check",)+W[1]+({"dx":12+w//2},),("check",)+W[2],("num","sup_low","Red at or below:",aR,None)+s["sup_low"]+({"ldy":4,"lgap":12,"fw":60,"stay":True},),("note","Opens:",{"dx":12+w//2,"ndy":4,"hue":None,"stay":True}),("buttons",(("sup_rows",Kit.ART_PAGE,"Choose rows","Pick the rows the table shows (%d of %d ticked)"%(len(e),len(j))),),{"dx":w-45-Kit.text_w("Choose rows"),"bdy":-78})),{"sh":aS}),("SUPPLY WARNINGS  (yellow and red counts, per row)",(("custom",0,aU),),{"sh":aT()}))
		def aW(f):
			if Kit.was_clicked(f.store,"sup_rows"):N("sup_rows")()
			if f.c.get("warn")and time.time()>=L["next_warn"]:
				L["next_warn"]=time.time()+aE
				if at(f.c):b["next_supply"]=0.
		def aX(f,new):
			a=f.c.get("sup_side")
			if a is None:return
			b=Kit.dd_index(a,-1)
			if 0<=b<len(K):new["sup_side"]=b
		def aY(old,new):b["next_supply"]=0.;a["at"]=None
		q=Kit.Page(d,aV,E,aY,adjust=aX,clicks=aW)
		def aZ(g,x,y,w):
			f=q.build(g,x,y,w);b=x+24+(w//2)+Kit.text_w("Opens:");L["next_warn"]=0.
			try:a=G.CreateDropDown(150,list(K),int(d["sup_side"]));a.SetPos(b,y+82);g.Add(a);f.c["sup_side"]=Kit.with_tip(a,"Side of the player frame the table opens on (flips when there is no room)")
			except Exception:f.c["sup_side"]=None;Kit.add_label(g,K[d["sup_side"]],b,y+86,Kit.HUE_INFO)
		def at(c):
			b=False
			for d,h,j in c.get("warn")or():
				e=k.get(d)or[None,None];a=list(e)
				for i,f in((0,h),(1,j)):
					try:
						if f.IsDisposed:continue
						g=str(f.Text or "").strip()
					except Exception:continue
					if not g:a[i]=None
					else:
						try:a[i]=max(0,min(ae,int(g)))
						except ValueError:pass
				if a!=list(e):
					if a[0]is None and a[1]is None:k.pop(d,None)
					else:k[d]=a
					b=True
			if b:aG()
			return b
		def a_():
			f=q.f
			if f is not None and f.c.get("warn")and at(f.c):b["next_supply"]=0.
			q.closed()
		def au():N("open")()
		def a0():b.update({"next_supply":0.,"counts":{},"next_save":0.,"queue":[]});a["saved"]=None;af();ag();ai();B.service("supplies.open",au);p.dock();S(i,{"title":X,"state":lambda:"open"if Kit.is_open(a["g"])else None,"show":au,"gump":lambda:a["g"],"fit":aI,"min":aJ,"untitled":True,"redraw":lambda:a.update(drawn=False)});B.add(T,i)
		def a1():
			a=time.time()
			while b["queue"]:
				c=b["queue"].pop(0)
				if p.action(c):continue
				d=aQ.get(c)
				if d is not None:d(a)
			aN(a);ao(a)
			if a>=b["next_save"]:b["next_save"]=a+aw;m()
		af();ag();ai()
		def a2():E();ah();m();g,a["g"]=a["g"],None;Kit.dispose(g);B.close()
		return{"start":a0,"tick":a1,"stop":a2,"client_tick":True,"config_height":q.height,"build_config":aZ,"poll_config":q.poll,"config_closed":a_}
	def ap():
		r="inventory.sections";y="Bag Sections";C="UnifiedBag_sections";T="UnifiedBag_sections_pos";U="UnifiedBag_sections_min";W=330;V=(260,46);X=3701;h=46;s=54;j=36;k=30;t=6;E=2.;Y=.5;Z=.25;F=1.;d=12;aa=240;H=24;ab=15;ad=("reagents","potions","bandages","gold","scrolls","maps");b={"other":True};b.update(("p_"+aB,aB in ad)for aB,aC in m);ae=dict(b);a={"minimized":False,"shutting":False,"docked":False,"queue":[],"groups":[],"sig":None,"ver":-1,"at":0.,"kinds":0,"loaded":False,"built":0.,"due":0.};p={"g":None,"c":{},"store":({},{}),"cells":[]};I,u,q=Kit.basics(a,y);c=[]
		def z(vals):return sum(1 for f,i in m if vals["p_"+f])
		def af():
			f=str(Kit.get_var(C,"")or "");b.update(ae);del c[:];a["loaded"]=True
			if not f:return
			for k,h in m:b["p_"+k]=False
			for e in f.split(";"):
				if e in("other","-other"):b["other"]=e=="other"
				elif e.startswith("c~"):
					p=e.split("~",2)
					try:g=int(p[1],16)
					except(IndexError,ValueError):continue
					if len(p)>2 and len(c)<d and all(i[0]!=g for i in c):c.append((g,p[2][:H]or "Item"))
				elif("p_"+e)in b:b["p_"+e]=True
			for k,h in reversed(m):
				if len(c)+z(b)<=d:break
				b["p_"+k]=False
		def v():a=["c~%04X~%s"%f for f in c]+[i for i,n in m if b["p_"+i]];Kit.put_var(C,";".join(a+["other"if b["other"]else "-other"]))
		def J(it,gr):
			try:a=re.sub(r"^[\d,]+\s+","",str(it.Name or "").strip())
			except Exception:a=""
			a=re.sub(r"[;~|]"," ",a).strip();return a[:1].upper()+a[1:]if a else "Item 0x%04X"%gr
		def K(n):return l(n)if n<10000 else "%dk"%(n//1000)
		def ag(w):return max(1,(w-2*Kit.MARGIN-16)//h)
		def ah(n,cols):return k+max(1,(n+cols-1)//cols)*s+t
		def N():return 2*Kit.MARGIN+30+Kit.GAP
		def O():return 2*Kit.MARGIN+16+3*h,N()+k+s+t
		def P():return "Reading item kinds."if e["data"]is None else "Nothing to show."
		def ai(i):
			def a(*b):
				a=p["cells"]
				if i<len(a)and a[i]["serial"]:u(("use",a[i]["serial"]))()
			return a
		def B():
			z=g.zone_slot(*O());w=z[0]if z else W;c=ag(w);f=a["groups"];C=sum(ah(len(aB),c)+Kit.GAP for aC,aB in f)-Kit.GAP if f else k+20;p=z[1]if z else N()+C;b,I,D=g.begin(w,p);i=[]
			if not a["minimized"]:
				g.frame(b);M=Kit.MARGIN;q=w-2*M;y=M+30+Kit.GAP;r=p-M
				if not f:Kit.add_section(b,M,y,q,r-y);D["empty"]=Kit.add_label(b,P(),M+12,y+10,Kit.HUE_INFO)
				for E,(F,l)in enumerate(f):
					e=max(1,(len(l)+c-1)//c)
					if z:e=min(e,(r-y-k-t)//s)
					if e<1:break
					u=k+e*s+t;Kit.add_section(b,M,y,q,u,"%s  (%d)"%(F.upper(),len(l)))
					for m,(n,v)in enumerate(l[:e*c]):
						o=M+8+(m%c)*h;x=y+k+(m//c)*s;d=G.CreateGumpItemPic(n[0],j,j);d.SetRect(o+(h-j)//2,x,j,j)
						if n[1]:d.Hue=n[1]
						d.DrawBorder=False;Kit.with_tip(d,v[0]);Kit.hook_double(d,ai(len(i)));b.Add(d);A=K(v[1]);B=x+j+1;H=Kit.add_label(b,A,o+(h-Kit.text_w(A))//2,B,Kit.HUE_TEXT);i.append({"gi":E,"ci":m,"serial":v[2],"amt":H,"x":o,"y":B})
					y+=u+Kit.GAP
			g.end(b,{"cells":i});Q()
		g=Kit.Window(r,y,a,p,B,T,U,(W,300),V,X,I,clear={"cells":[]})
		def Q():
			c=p["c"];e=a["groups"]
			if "status"in c:Kit.set_text(c["status"],"%s: %s"%(y,Kit.count(a["kinds"],"kind")));return
			if "empty"in c:Kit.set_text(c["empty"],P())
			for b in p["cells"]:
				try:v=e[b["gi"]][1][b["ci"]][1]
				except IndexError:continue
				b["serial"]=v[2];d=K(v[1])
				if Kit.set_text(b["amt"],d):b["amt"].SetPos(b["x"]+(h-Kit.text_w(d))//2,b["y"])
		def aj():a=e["data"]or{};d=[(i,frozenset((f,)))for f,i in c];return d+[(w,a.get(n,frozenset()))for n,w in m if b["p_"+n]]
		def ak(a):return a[1][0].lower(),a[0]
		def al():
			e=aj();f=len(e);g=[{}for w in range(f+1)];n=0;k=b["other"]
			for a in A():
				try:c,h,i,l=int(a.Graphic),int(a.Hue),max(1,int(a.Amount or 1)),int(a.Serial)
				except Exception:continue
				d=f
				for m,(q,o)in enumerate(e):
					if c in o:d=m;break
				if d==f and not k:continue
				j=g[d].get((c,h))
				if j is not None:j[1]+=i
				elif n<aa:n+=1;g[d][(c,h)]=[J(a,c),i,l]
			p=[G for G,aB in e]+["Other"];return[(p[aD],sorted(aC.items(),key=ak))for aD,aC in enumerate(g)if aC]
		def R(now,d=False):
			a["ver"],a["at"],a["due"]=D(),now,0.;b=al();c=tuple((f,tuple(n for n,w in i))for f,i in b)
			if d and c!=a["sig"]and 0.<=now-a["built"]<F:a["due"]=a["built"]+F;return
			a["groups"]=b;a["kinds"]=sum(len(G)for aB,G in b)
			if c!=a["sig"]:a["sig"],a["built"]=c,now;B()
			else:Q()
		def am(action):
			b=action[1]
			if not Kit.in_pack(b):q("that is no longer in your backpack.",Kit.HUE_BAD);return
			Kit.once(lambda:API.UseObject(b),(r,b))();a["at"]=time.time()-E+Y
		def S():
			if len(c)+z(b)<d:return False
			q("%d sections at most."%d,Kit.HUE_BAD);return True
		def an(action):
			if S():return
			q("target an item for its own section.")
			def a(serial):u(("picked",int(serial or 0)))()
			L(ab,a,r)
		def ao(action):
			f=action[1];b=API.FindItem(f)if f else None
			if b is None:return
			d=int(b.Graphic);e=J(b,d)[:H]
			if any(i[0]==d for i in c):q("%s already has a section."%e,Kit.HUE_BAD);return
			if S():return
			c.append((d,e));v();a["at"]=0.;o(r);q("added a %s section."%e,Kit.HUE_GOOD)
		def ap(action):
			if 0<=action[1]<len(c):c.pop(action[1]);v();a["at"]=0.;o(r)
		aq={"use":am,"add":an,"picked":ao,"remove":ap}
		def ar(w):
			e=(w-24)//2;f=[("check","p_"+aB,G,"A section for %s"%G.lower(),{"dx":12+(n%2)*e,"stay":n%2==0})for n,(aB,G)in enumerate(m)];a=[]
			for i,(g,b)in enumerate(c):a+=[("note",Kit.fit(b,w-80-Kit.text_w("Remove")),{"stay":True,"ndy":4,"hue":Kit.HUE_TEXT}),("buttons",(("rm%d"%i,Kit.ART_CLOSE,"Remove","Remove the %s section"%b),),{"dx":w-48-Kit.text_w("Remove")})]
			if not a:a=[("note","None yet: add one from a target.")]
			return(("SECTIONS  (%d at most, in this order)"%d,f+[("check","other","Show Other","Everything the sections leave, in a last section")]),("YOUR SECTIONS  (checked first)",a+[("buttons",(("add",Kit.ART_PLAY,"Add from target...","Target an item for a section of its own"),))]))
		def at(old,new):a["at"]=0.
		def au(f,new):
			a=len(c)+z(new)-d;e=False
			for k,g in reversed(m):
				if a<=0:break
				if new["p_"+k]and not b["p_"+k]:new["p_"+k]=False;a-=1;e=True;Kit.set(f.c["p_"+k],"IsChecked",False)
			if e:q("%d sections at most."%d,Kit.HUE_BAD)
		def av(f):
			if Kit.was_clicked(f.store,"add"):u("add")()
			for i in range(len(c)):
				if Kit.was_clicked(f.store,"rm%d"%i):u(("remove",i))();break
		x=Kit.Page(b,ar,v,at,adjust=au,clicks=av)
		def aw():a.update({"shutting":False,"docked":False,"queue":[],"groups":[],"sig":None,"ver":-1,"at":0.,"kinds":0,"loaded":False,"minimized":g.start_min(),"built":0.,"due":0.});af();B();g.dock(fit=True,min=O)
		def ax():
			q=a["queue"]
			while q:
				b=q.pop(0)
				if not g.action(b):aq[b[0]if isinstance(b,tuple)else b](b)
			if p["g"]is None or Kit.closed(p)or a["minimized"]or a["docked"]or e["data"]is None:return
			c=time.time();d=c-a["at"]
			if not 0.<=d<E or 0.<a["due"]<=c:R(c)
			elif d>=Z and D()!=a["ver"]:R(c,True)
		def ay():
			if e["data"]is not None:return
			try:a=M()
			except Exception:a=None
			try:ac(a)
			except Exception:e["data"]={}
		def az():return e["data"]is None and not a["shutting"]
		def aA():
			a["shutting"]=True
			if a["loaded"]:v()
			I.close()
		return{"start":aw,"tick":ax,"stop":aA,"client_tick":True,"config_height":x.height,"build_config":x.build,"poll_config":x.poll,"config_closed":x.closed,"thread_tick":ay,"thread_wanted":az}
	aq=(("bags",ak,.1,"bag"),("paperdoll",al,.1,"character"),("storage",am,.1,"storage"),("restock",an,.1,"restock"),("supplies",ao,.1,"supplies"),("sections",ap,.1));return PartSet(ad,ae,aq).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("inventory","Inventory","Bags, paperdoll, storage, restock, supplies",_module_inventory,.1,category="Your things",parts=(("bags","Bags","All your bags in one grid",True,("bag",)),("paperdoll","Paperdoll","What you wear, and your stats",True,("character",)),("storage","Storage","What the containers you opened hold",False,("storage",)),("restock","Restock","Refills from a chest or bank, on a press",False,("restock",)),("supplies","Supplies","Pack supplies, low counts marked",True,(),True),("sections","Bag Sections","What you carry, grouped by kind",False,(),True),),aliases=('Character','Unified Bag','Storage Index','Restock','paperdoll','bank','chest','find','sort','supplies','supplies table','sections'))
