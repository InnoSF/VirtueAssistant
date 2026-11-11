def _module_interface():
	ar=Client.key_held;ah=HOST.grid_shown;p=HOST.grid_size;at=HOST.grid_toggle;ai=HOST.poke;aC=HOST.save_prefs;aD=HOST.set_switch;aE=HOST.show_settings;E=Kit.ART_CLOSE;v=Kit.ART_OK;t=Kit.ART_PAGE;A=Kit.ART_PLAY;O=Kit.HUE_BAD;aj=Kit.HUE_GOOD;e=Kit.HUE_INFO;D=Kit.HUE_TEXT;P=Kit.HUE_TITLE;K=Kit.MARGIN;q=Kit.add_box;l=Kit.add_label;F=Kit.add_section;aF=Kit.add_textbox;aG=Kit.add_tiled;aH=Kit.add_window_frame;I=Kit.art_button;au=Kit.catcher;L=Kit.count;Y=Kit.dd_index;u=Kit.dispose;o=Kit.fit;ak=Kit.get_var;Q=Kit.is_open;av=Kit.look;aw=Kit.mouse_pos;aI=Kit.on_moved;ax=Kit.place;Z=Kit.put_var;T=Kit.say;J=Kit.screen;aa=Kit.set_text;C=Kit.text_w;j=Kit.was_clicked;ab=Kit.with_tip;al="interface";aZ="Interface";a_="interface.setup";a0="Interface_setup_pos";aJ="Interface_setup_seen";aK="VirtueAssistant_layout_editor_pos";a1,a2=600,(260,46);M,R,aL=100,64,12;aM=170;a3=.25;s,am,an=3,"#D4AF37","#3A2A08";ac=(("Sides","Bags and paperdoll left; map and trackers right"),("Mirrored","Map and trackers left; bags and paperdoll right"),("Bottom bar","Game on top; every window in one band below"),("Right column","Game left; windows stacked on the right"),("Compact","Windows stacked on the left; game on the right"));a4=(("unitframes.","frames"),("actionbar","bar"),("character","gear"),("bag","bag"),("ultima.","watch"),("hub","watch"),("meters","watch"),("worldmap","map"));ay=(("seam","Join windows in zones into one panel","One frame round every zone, gold round the game view; hover a window's top for its title"),("fit_view","Fit the game view to the game area","Borderless, sized and locked to the game area"),("game","Give an empty zone's room to the game area","Widens the game area beside an empty zone"));ad={"seam":False,"fit_view":True,"game":True,"snap":True,"grid_on":False,"grid":GRID_DEFAULT,"compact":False,"cblind":False,"streamer":False,"code":"","situ_on":False,"fade":False,"fade_to":40,"fade_after":6,"fade_all":False};bE=dict(ad);k={"minimized":False,"shutting":False,"docked":False,"queue":[],"editor":None,"back_sig":None,"back_at":0.,"jobs":[]};ao={"g":None,"c":{},"store":({},{})};N={"g":None};ae={"g":None};U={"g":None};B={"gumps":None,"ver":None,"same":None,"off":False,"seen":None,"raw":None};m={"zones":None,"windows":None,"zone_dd":[],"frame_names":[],"layout_names":[],"situ_dd":[],"situ_names":[]};aN=(("war","War mode:","The window layout while you are in war mode"),("bank","Bank:","The window layout near your bank for 5 minutes after you open it"),("dungeon","Dungeon:","The window layout in a dungeon"),("town","Town:","The window layout in a guard zone"));n={"open":False,"step":0,"preset":0,"zs":None,"fname":LAYOUT_DEFAULT,"assign":{},"look":{},"cards":{}};aO,V,X=Kit.basics(k,aZ)
	def ap():L=LAYOUT;ad.update({"seam":L.seamless,"fit_view":L.fit_view,"game":L.game_grows,"snap":SNAP.enabled,"grid_on":ah(),"grid":p(),"compact":Kit.compact,"cblind":Kit.cblind,"streamer":Kit.streamer,"situ_on":L.situ["on"],"fade":FADE.on,"fade_to":int(round(FADE.to*100)),"fade_after":int(FADE.after),"fade_all":FADE.all})
	def a5():pass
	def aP(a,b):
		e,f,i,j=a;g,h,k,l=b;D=SNAP_DIST
		for c,d in((e+i,g),(g+k,e)):
			m,n=max(f,h),min(f+j,h+l)
			if abs(d-c)<=D and n>m:return "v",min(c,d),max(c,d),m,n
		for c,d in((f+j,h),(h+l,f)):
			o,p=max(e,g),min(e+i,g+k)
			if abs(d-c)<=D and p>o:return "h",min(c,d),max(c,d),o,p
		return
	def a6(e,b,f):
		c,a=[],e
		for d,g in sorted(f):
			if d>a:c.append((a,min(d,b)))
			a=max(a,g)
		if a<b:c.append((a,b))
		return[(h,i)for h,i in c if i>h]
	class LayoutEditor(object):
		BAR_W=720;SETTLE=.3;FIELD_W=52;ROW=28;KEYS={"up":("UP",),"down":("DOWN",),"left":("LEFT",),"right":("RIGHT",),"delete":("DELETE",),"z":("Z",),"y":("Y",),"enter":("RETURN","KP_ENTER"),"esc":("ESCAPE",)};FIELDS=("col","row","w","h")
		def __init__(self,layout,zs,a):self.layout=layout;self.zs=zs;self.on_close=a;self.frames={};self.bar=None;self.store=({},{});self.c={};self.renames={};self.sel=zs.zones[0].id if zs.zones else None;self.multi=set();self.grid_was=None;self.fields=None;self.saveas_text="";self.bar_pos=None;self.rebuild=False;self.closed=False;self.others=None;self.W,self.H=J();self.px_mode=False;self.undo,self.redo=[],[];self.keys_was={};self.focus_was=None;self.raws={};self.said=None;self.del_armed=None;self.marks=None;self.marks_sig=None;self.counts=(0,0);self.handles=[];self.handles_sig=None;self.edge=None;self.edge_g=None;self.edge_at=0.;self.pressed_was=False;self.pick=0;self.pick_keys=[];self.preview="";self.raws_ok=False;self._pick_next=0.
		def open(self):
			self.grid_was=ah()
			if not self.grid_was:safe(at)
			for z in self.zs.zones:self.build_zone(z)
			self.build_bar();self.draw_marks()
		def close(self,keep,quiet=False):
			if self.closed:return
			self.closed=True
			for c,b in list(self.frames.items()):u(b.get("g"))
			self.frames={};self._drop_handles()
			for a in("bar","marks","edge_g"):u(getattr(self,a));setattr(self,a,None)
			if self.grid_was is not None and ah()!=self.grid_was:safe(at)
			self.on_close();self.layout.dirty=True;self.layout.page_refresh=True
			if not keep and not quiet:T("the saved zones are back.",e)
		def _snap(self):return([a.copy()for a in self.zs.zones],self.sel,dict(self.renames))
		def push(self):
			self.undo.append(self._snap())
			if len(self.undo)>50:del self.undo[0]
			self.redo=[]
		def _restore(self,snap):
			b,a,c=snap
			for d in list(self.frames):u(self.frames[d].get("g"))
			self.frames={};self.zs.zones=[f.copy()for f in b];self.renames=dict(c);self.sel=(a if self.zs.by_id(a)is not None else(self.zs.zones[0].id if self.zs.zones else None));self.multi=set()
			for z in self.zs.zones:self.build_zone(z)
			self.rebuild=True
		def _hist(self,a,b,word):
			if not a:self.say("nothing to %s."%word,e);return
			b.append(self._snap());self._restore(a.pop())
		def do_undo(self):self._hist(self.undo,self.redo,"undo")
		def do_redo(self):self._hist(self.redo,self.undo,"redo")
		def say(self,text,hue=None):
			if text==self.said:return
			self.said=text;T(text,O if hue is None else hue)
		def _windows_in(self,z):L=self.layout;a=self.orig_id(z.id);return[L.title_of(b)for b in L.assign.get(a,[])]
		def orig_id(self,a):
			for b,c in self.renames.items():
				if c==a:return b
			return a
		def build_zone(self,z):
			c=self.frames.get(z.id,{}).get("g");x,y,w,h=z.px;M=K;a={"g":None,"resize_at":0.,"size":(w,h)};g=G.CreateModernGump(x,y,w,h,not z.lock,ZONE_MIN_W,ZONE_MIN_H,self._resized(z.id));g.SetAlpha(0)
			if z.lock:g.CanMove=False
			aH(g,w,h,corners=False,mouse=False);q(g,M,M,w-2*M,h-2*M,.25,ZONE_COLORS.get(z.kind,"#FFFFFF"))
			if z.kind=="w"and z.stack=="t":q(g,M,M+31,w-2*M,4,.9,"#E8C15A")
			self._draw_overlaps(g,z)
			if z.kind=="k":self._draw_game(g,z)
			if z.id==self.sel and self.pick:self._draw_preview(g,z)
			F(g,M,M,w-2*M,30);d=z.id==self.sel or z.id in self.multi;a["lbl"]=l(g,o(z.id+("  (locked)"if z.lock else ""),w-2*M-24),M+12,M+7,P if d else D);b=self._windows_in(z)if z.kind=="w"else[];a["wins"]=l(g,o(", ".join(b),w-2*M-24)if b else "",M+12,M+30+6,D);a["sum"]=l(g,"",M+12,M+30+6+(20 if b else 0),e);au(g,M,M,w-2*M,30,self._select(z.id),"Select the zone (Shift+click: pick more)"+("; locked"if z.lock else "; drag to move it on the grid"),movable=not z.lock);ax(g,x,y,w,h);G.AddGump(g);Kit.no_snap(g);aI(g,self._moved(z.id));a["g"]=g;self.frames[z.id]=a;self.update_zone(z);u(c)
		def _draw_overlaps(self,g,z):
			x,y,w,i=z.px
			for o in self.zs.zones:
				if o is z or o.px is None or not(z.overlap or o.overlap):continue
				c,d,j,k=o.px;e,a=max(x,c),max(y,d);b,f=min(x+w,c+j),min(y+i,d+k)
				if b-e<4 or f-a<4:continue
				for h in range(e,b,12):q(g,h-x,a-y,min(4,b-h),f-a,.45,"#E8C15A")
		def _draw_game(self,g,z):
			e=self.zs.copy();Layout._overlap_shape(e);a,b,c,d=e.by_id(z.id).px;a-=z.px[0];b-=z.px[1]
			for r in((a,b+d-2,c,2),(a,b,2,d),(a+c-2,b,2,d),(a,b,c,2)):q(g,r[0],r[1],r[2],r[3],.9,"#E8C15A")
		def _draw_preview(self,g,z):
			a=self.pick_keys[self.pick]if 0<self.pick<len(self.pick_keys)else None
			if a is None or z.kind!="w":return
			L=self.layout;f=[h for h in L.assign.get(self.orig_id(z.id),[])if h!=a]+[a];x,y=z.px[0],z.px[1]
			for k,(b,c,d,e)in L.slots_for(z,f):q(g,b-x,c-y,max(1,d),max(1,e),.55,"#E8C15A"if k==a else "#202020");l(g,o(L.title_of(k),max(20,d-16)),b-x+8,c-y+e-26,D)
		def update_zone(self,z):
			a=self.frames.get(z.id)
			if a is None:return
			b=p();x,y,w,h=z.px;c="%s, %d x %d squares"%(z.kind_name(),max(1,int(round(float(w)/b))),max(1,int(round(float(h)/b))))
			if z.overlap:c+=", overlaps"
			aa(a["sum"],o(c,w-2*K-24));aa(a["lbl"],o(z.id+("  (locked)"if z.lock else ""),w-2*K-24),P if(z.id==self.sel or z.id in self.multi)else D)
		def _select(self,a):
			def b():
				b=bool(ar("shift"))
				if b and self.sel is not None and a!=self.sel:
					if a in self.multi:self.multi.discard(a)
					else:self.multi.add(a);self.multi.add(self.sel)
					self.rebuild=True;ai();return
				if a!=self.sel or self.multi:self.multi=set();self.sel=a;self.pick=0;self.rebuild=True;ai()
			return b
		def _resized(self,a):
			def b(*c):
				b=self.frames.get(a)
				if b is not None:b["resize_at"]=time.time()
			return b
		def _moved(self,a):
			def b():
				z=self.zs.by_id(a);b=self.frames.get(a)
				if z is None or b is None or not Q(b["g"]):return
				r=Snap.rect(b["g"])
				if r is None:return
				if(r[0],r[1])==(z.px[0],z.px[1]):return
				if z.lock:self.place_zone(z);self.say('zone "%s" is locked; click Lock to move it.'%z.id,e);return
				self.landed(z,r[0],r[1],z.px[2],z.px[3],resized=False)
			return b
		def _blocker(self,z):a=self.zs.overlaps(z);return a[0]if a else None
		def landed(self,z,x,y,w,h,resized=True):
			W,H=self.W,self.H;c=p()
			if resized:i=1 if z.free else c;w=max(ZONE_MIN_W,int(round(float(w)/i))*i);h=max(ZONE_MIN_H,int(round(float(h)/i))*i)
			w,h=min(w,W),min(h,H);k=(0,int(x),int(y))if z.free else Snap.near_anchor(x,y,w,h)
			if k is not None:a,b=k[1],k[2]
			else:
				a=b=None
				for f in(0,max(0,W-w)):
					if abs(f-x)<=SNAP_DIST:a=f
				for g in(0,max(0,H-h)):
					if abs(g-y)<=SNAP_DIST:b=g
				for o in self.zs.zones:
					if o is z or o.px is None:continue
					d,e,l,m=o.px
					if a is None and e<y+h+SNAP_DIST and y<e+m+SNAP_DIST:
						for f in(d+l,d-w,d,d+l-w):
							if abs(f-x)<=SNAP_DIST:a=f
					if b is None and d<x+w+SNAP_DIST and x<d+l+SNAP_DIST:
						for g in(e+m,e-h,e,e+m-h):
							if abs(g-y)<=SNAP_DIST:b=g
				if a is None:a=int(round(float(x)/c))*c
				if b is None:b=int(round(float(y)/c))*c
			j=z.px;self.push();z.set_px(a,b,w,h,W,H)
			if not self.zs.push_clear(z,W,H,None if z.free else c):z.set_px(j[0],j[1],j[2],j[3],W,H);self.undo.pop();o=self._blocker(z);self.say('no room for zone "%s" there%s; it stays where it was.'%(z.id,(' (it would cover "%s")'%o.id)if o is not None else ""))
			z.note_pins(W,H);self.place_zone(z);self.changed()
		def _refields(self):self.fields=None;self.show_fields()
		def changed(self):self._refields();self.draw_marks()
		def place_zone(self,z):
			a=self.frames.get(z.id)
			if a is None:return
			x,y,w,h=z.px
			if((w,h)!=a["size"]or z.overlap or z.kind=="k"or any(b.overlap for b in self.zs.zones)):self.build_zone(z);return
			with Kit.quiet:ax(a["g"],x,y,w,h);Kit.moved_by_code(a["g"])
			self.update_zone(z)
		def keep(self,W,H):
			if(W,H)!=(self.W,self.H):
				self.W,self.H=W,H;self.zs.reflow(W,H,p())
				for z in self.zs.zones:self.place_zone(z)
				self.draw_marks()
		def gaps(self):
			W,H=self.W,self.H;c=[w.px for w in self.zs.zones if w.px is not None];a=[x for x in sorted(set([0,W]+[y[0]for y in c]+[z[0]+z[2]for z in c]))if 0<=x<=W];b=[G for G in sorted(set([0,H]+[bF[1]for bF in c]+[bG[1]+bG[3]for bG in c]))if 0<=G<=H];h,n=len(a)-1,len(b)-1;d={}
			for j in range(n):
				s=(b[j]+b[j+1])/2.
				for i in range(h):
					t=(a[i]+a[i+1])/2.
					if not any(bH[0]<=t<bH[0]+bH[2]and bH[1]<=s<bH[1]+bH[3]for bH in c):d[(i,j)]=True
			e,o=set(),0
			for k in d:
				if k in e:continue
				o+=1;l=[k];e.add(k)
				while l:
					i,j=l.pop()
					for f in((i+1,j),(i-1,j),(i,j+1),(i,j-1)):
						if f in d and f not in e:e.add(f);l.append(f)
			p=[]
			for j in range(n):
				i=0
				while i<h:
					if(i,j)in d:
						q=i
						while i<h and(i,j)in d:i+=1
						p.append((a[q],b[j],a[i]-a[q],b[j+1]-b[j]))
					else:i+=1
			g=[]
			for r in p:
				for u,m in enumerate(g):
					if m[0]==r[0]and m[2]==r[2]and m[1]+m[3]==r[1]:g[u]=(m[0],m[1],m[2],m[3]+r[3]);break
				else:g.append(r)
			return g,o
		def bad_overlaps(self):
			e=[];f=self.zs.zones
			for i,a in enumerate(f):
				for b in f[i+1:]:
					if a.px is None or b.px is None or b not in self.zs.overlaps(a):continue
					if a in self.zs.overlaps(b)or not b.overlap:
						c,d=max(a.px[0],b.px[0]),max(a.px[1],b.px[1]);g=min(a.px[0]+a.px[2],b.px[0]+b.px[2]);h=min(a.px[1]+a.px[3],b.px[1]+b.px[3])
						if g>c and h>d:e.append((a,b,(c,d,g-c,h-d)))
			return e
		def draw_marks(self):
			d=(self.W,self.H,tuple((r.id,r.kind,r.overlap,r.solo,tuple(r.px or()))for r in self.zs.zones))
			if d==self.marks_sig and Q(self.marks):return
			self.marks_sig=d;e,n=self.gaps();b=self.bad_overlaps();f=(n,len(b));l,self.marks=self.marks,None;u(l);i=[H for H in self.zs.zones if H.kind=="w"and H.px is not None and not H.solo];j=[z for W,bF in enumerate(i)for bG in i[W+1:]for z in(aP(bF.px,bG.px),)if z is not None]
			if e or b or j:
				g=G.CreateGump(False,False)
				for(x,y,w,h)in e:q(g,x,y,w,h,.45,"#C83030")
				for a,c,(x,y,w,h)in b:q(g,x,y,w,h,.55,"#C83030")
				for o,m,p,a,c in j:k=(m+p)//2;q(g,*(((k-2,a,4,c-a)if o=="v"else(a,k-2,c-a,4))+(.9,"#E8C15A")))
				Grid.show_overlay(g,0,0,self.W,self.H);self.marks=g
			if f!=self.counts:self.counts=f;self.rebuild=True
		def _drop_handles(self):
			for g,a,r in self.handles:u(g)
			self.handles=[];self.handles_sig=None
		def _sync_handles(self):
			z=self.zs.by_id(self.sel)if self.sel else None;c=self.frames.get(z.id)if z is not None else None;d=(z.id,tuple(z.px),z.lock,c.get("g")if c else None)if z is not None and z.px is not None else None
			if d==self.handles_sig:return
			self._drop_handles();self.handles_sig=d
			if z is None or z.lock:return
			x,y,w,h=z.px;T=10;a=max(24,min(80,w//3));b=max(24,min(80,h//3))
			for e,r in(("l",(x,y+(h-b)//2,T,b)),("r",(x+w-T,y+(h-b)//2,T,b)),("t",(x+(w-a)//2,y+K+30,a,T)),("b",(x+(w-a)//2,y+h-T,a,T))):g=G.CreateGump(True,False);q(g,0,0,r[2],r[3],.9,"#E8C15A");au(g,0,0,r[2],r[3],lambda:None,"Drag to move this edge on the grid");g.SetRect(r[0],r[1],r[2],r[3]);G.AddGump(g);SNAP.skip_gump(g);self.handles.append((g,e,r))
		def _edge_tick(self,pressed):
			b=time.time()
			if self.edge is None:
				if pressed and not self.pressed_was and self.handles:
					m=aw()
					if m is not None:
						for g,a,r in self.handles:
							if r[0]<=m[0]<r[0]+r[2]and r[1]<=m[1]<r[1]+r[3]:
								z=self.zs.by_id(self.sel)
								if z is not None:self.edge=(z.id,a,m,tuple(z.px))
								break
				return
			n,a,c,d=self.edge;z=self.zs.by_id(n);m=aw()
			if z is None or m is None:self.edge=None;u(self.edge_g);self.edge_g=None;return
			x,y,w,h=d;e,f=m[0]-c[0],m[1]-c[1]
			if a=="l":i=min(x+w-ZONE_MIN_W,max(0,x+e));x,w=i,w+(x-i)
			elif a=="r":w=max(ZONE_MIN_W,min(self.W-x,w+e))
			elif a=="t":j=min(y+h-ZONE_MIN_H,max(0,y+f));y,h=j,h+(y-j)
			else:h=max(ZONE_MIN_H,min(self.H-y,h+f))
			if pressed:
				if b-self.edge_at>=.05:
					self.edge_at=b;k=p();o,self.edge_g=self.edge_g,None;u(o);g=G.CreateGump(False,False)
					for s,v,A,B in((0,0,w,2),(0,h-2,w,2),(0,0,2,h),(w-2,0,2,h)):q(g,s,v,A,B,.95,"#E8C15A")
					t="%d x %d squares (%d x %d)"%(max(1,int(round(float(w)/k))),max(1,int(round(float(h)/k))),w,h);q(g,6,6,C(t)+12,22,.85,"#000000");l(g,t,12,8,P);Grid.show_overlay(g,x,y,w,h);self.edge_g=g
				return
			self.edge=None;u(self.edge_g);self.edge_g=None
			if(x,y,w,h)!=d:self.landed_rect(z,x,y,w,h)
		def landed_rect(self,z,x,y,w,h):
			c=1 if z.free else p();d,e,a,b=[int(round(float(f)/c))*c for f in(x,y,x+w,y+h)];a,b=min(a,self.W),min(b,self.H)
			if not z.free and x+w>=self.W-SNAP_DIST:a=self.W
			if not z.free and y+h>=self.H-SNAP_DIST:b=self.H
			self.apply_rect(z,d,e,max(ZONE_MIN_W,a-d),max(ZONE_MIN_H,b-e))
		def apply_rect(self,z,x,y,w,h,typed=None):
			W,H=self.W,self.H
			if w>W or h>H or x<0 or y<0 or x+w>W or y+h>H:self.say('zone "%s" can\'t be %s there: it would run off the screen; make it smaller or move it.'%(z.id,typed or "that size"));return False
			a=z.px;z.set_px(x,y,w,h,W,H);o=self._blocker(z)
			if o is not None:z.set_px(a[0],a[1],a[2],a[3],W,H);self.say('zone "%s" can\'t be %s there: it would cover "%s"; make it %s or move it.'%(z.id,typed or "that size",o.id,"shorter"if(h>a[3]and w<=a[2])else "narrower"if w>a[2]else "smaller"));return False
			b=z.px;z.set_px(a[0],a[1],a[2],a[3],W,H);self.push();z.set_px(b[0],b[1],b[2],b[3],W,H);z.note_pins(W,H);self.said=None;self.place_zone(z);self.changed();return True
		@staticmethod
		def _cap_w(cap):return 35+C(cap)
		def _flow(self,g,store,items,a,y,d):
			x=a
			for e,f,b,h in items:
				c=self._cap_w(b)
				if x>a and x+c>d:x=a;y+=self.ROW
				if g is not None:I(g,store,e,f,x,y-2,b,h)
				x+=c+16
			return y
		def build_bar(self):Binds.scoped("interface.editor",self.draw_bar)
		def draw_bar(self):
			D=self.bar;W=self.BAR_W;M,U=K,Kit.GAP;j=({},{});d={};g=G.CreateGump(True,True);f=W-2*M;m=M+f-12;z=self.zs.by_id(self.sel)if self.sel else None;s=self.layout;ac=p();H=[];J=M+30+U;a=J+32;i=[]
			if z is None:i.append(("label","Click Add zone, then drag it into place.",M+12,a+3,e));a+=self.ROW
			else:
				V=M+12+C("Name:")+8;i.append(("label","Name:",M+12,a+3,None));i.append(("box","name",z.id,V,a,130,False,"Zone name, unique in this frame layout; Enter uses it"));h=[("kind",t,"Kind: "+z.kind_name(),"Switch kind: window, keep clear, reserved"),("stack",t,"Stack: "+z.stack_name(),"Switch the way windows stack in this zone"),("prio",t,"Shrinks: "+_ordinal(z.prio),"Change when this zone shrinks to minimized bars on a small screen"),("overlap",t,"Overlap: "+("on"if z.overlap else "off"),"Let this zone lie over others (on) or keep clear of them (off)"),("lock",t,"Lock: "+("on"if z.lock else "off"),"Lock the zone against moving and resizing, or unlock it"),("split",A,"Split","Cut this zone in two along its long side"),("join",v,"Join","Merge with a zone flush beside it of the same height or width"),("solo",t,"Apart: "+("on"if z.solo else "off"),"Keep this zone's panel apart from zones it touches (on) or join them (off)"),("free",t,"Snap: "+("off"if z.free else "on"),"Snap this zone to the grid and its neighbours (on) or place it to the pixel (off)"),("dup",v,"Duplicate","Add a copy of this zone beside it"),("remove",E,"Remove","Remove this zone (or Delete twice); its windows become free")];H.append(("flow",h,V+130+16,a));a=self._flow(None,None,h,V+130+16,a,m)+self.ROW;n=M+12;ad="px"if self.px_mode else "squares"
				for c,ae,w in(("col","X:"if self.px_mode else "Col:","Left edge in %s from the screen's left"),("row","Y:"if self.px_mode else "Row:","Top edge in %s from the screen's top"),("w","W:","Width in %s"),("h","H:","Height in %s")):
					X=(self.W if c in("col","w")else self.H)
					if not self.px_mode:X=(X+ac-1)//ac
					i.append(("label",ae,n,a+3,None));n+=C(ae)+6;i.append(("box",c,"",n,a,self.FIELD_W,True,(w%ad)+" (%d-%d); Enter or Apply uses it, Esc puts it back"%(0 if c in("col","row")else 1,X)));n+=self.FIELD_W+14
				h=[("apply",v,"Apply","Use the typed values (Enter does too)"),("units",t,"Units: "+ad,"Switch between grid squares and pixels")];H.append(("flow",h,n+4,a));a=self._flow(None,None,h,n+4,a,m)+self.ROW;d["px_y"]=a+3;i.append(("px",M+12,a+3));a+=20;aq=", ".join(bG for bF,bG in(("L","left"),("T","top"),("R","right"),("B","bottom"),("X","centre"),("Y","middle"))if bF in z.pins);i.append(("pins","Pinned: "+(aq or "none"),M+12,a+3));a+=28;h=[("even",A,"Even out","Give this zone and those flush beside it in its row (or column) equal sizes")]
				if len(self.multi)>=2:h+=[("al_"+bH[0],A,"Align "+bH,"Line the picked zones' %s edges up with this zone's"%bH)for bH in("left","top","right","bottom")];h.append(("same",A,"Same size","Make the picked zones this zone's size"))
				H.append(("flow",h,M+12,a));a=self._flow(None,None,h,M+12,a,m)+self.ROW
				if len(self.multi)>=2:i.append(("label",o("%d zones picked (Shift+click picks more or fewer)."%len(self.multi),f-24),M+12,a+3,e));a+=20
			ZH=a-J+6;N=J+ZH+U;r=[];k=0
			if z is not None and z.kind=="w":
				r=list(s.assign.get(self.orig_id(z.id),[]));k=30+28+26*len(r)+(20 if self.preview else 0)+14
				if not r:k+=20
			Y=N+(k+U if k else 0);R=ratio_class(self.W,self.H);af=[bI for bI in("narrow","wide","ultrawide")if bI!=R];Z=[("undo",t,"Undo","Undo the last change (Ctrl+Z)"),("redo",t,"Redo","Redo the last undo (Ctrl+Y)"),("from_default",A,"New from Default","Start again from the Default layout"),("mirror",A,"Mirror","Swap the zones left and right"),("copyto",v,"Copy to others","Use these zones on %s and %s screens too (save them first)"%tuple(af))]
			if self.others is None or self.others[0]!=(self.zs.name,R):ar=FRAMES_NAMED%self.zs.name;self.others=((self.zs.name,R),[bJ for bJ in af if ak(ar+"@"+bJ,"")])
			S=self.others[1]
			if S:Z.append(("reflow",A,"Reflow from: "+S[0],"Rebuild from this layout's %s-screen version"%S[0]));d["reflow_from"]=S[0]
			at=self._flow(None,None,Z,M+12,0,m);FH=30+28*2+at+20*3+10;T=Y+FH+M;aH(g,W,T);F(g,M,M,f,30);l(g,"ZONES",M+30,M+7,P);l(g,o('frame layout "%s"'%self.zs.name,f-250),M+30+C("ZONES")+12,M+7,e);I(g,j,"close",E,W-M-54,M+4,None,"Close the editor and bring back the saved zones");F(g,M,J,f,ZH,"ZONE  (selected)");ag=[]
			for b in i:
				if b[0]=="label":l(g,b[1],b[2],b[3],b[4])
				elif b[0]=="box":c,au,bx,by,av,aw,w=b[1:];d[c]=ab(aF(g,au,bx,by,av,numbers=aw),w);ag.append(c)
				elif b[0]=="px":d["px"]=l(g,"",b[1],b[2],e);d["px_x"]=b[1]
				elif b[0]=="pins":ab(l(g,b[1],b[2],b[3],e),"Edges kept on the screen's edge (or centre line) on other screen sizes")
			for op in H:self._flow(g,j,op[1],op[2],op[3],m)
			if k:
				F(g,M,N,f,k,"WINDOWS  (in this zone, top to bottom)");a=N+32;l(g,"Window:",M+12,a+3);ah=M+12+C("Window:")+8;ai=300;bx=ah+ai+16;I(g,j,"w_add",v,bx,a-2,"Put it here","Put the picked window in this zone (no Arrange mode needed)");a+=28
				if not r:l(g,"Pick a window above, then click Put it here.",M+12,a+3,e);a+=20
				for ay,y in enumerate(r):l(g,o(s.title_of(y),300),M+12,a+3);self._flow(g,j,[("w_%s_%d"%(bK,ay),bL,bM,bN%s.title_of(y))for bK,bL,bM,bN in(("up",t,"Up","Move %s up the zone's stack"),("down",t,"Down","Move %s down the zone's stack"),("out",E,"Take out","Free %s from the zone (it stays where it is)"))],M+12+310,a,1<<30);a+=26
				d["wins_rows"]=r
				if self.preview:l(g,o(self.preview.lstrip("!"),f-24),M+12,a+3,O if self.preview.startswith("!")else e)
			F(g,M,Y,f,FH,"FRAME LAYOUT");a=Y+32;x=M+12
			for c,az,B,w in(("add",v,"Add zone","Add a zone mid-screen to drag into place"),("fill",A,"Fill the gaps","Grow every zone into empty room beside it"),("save",v,"Save","Save as the frame layout in use (Default saves as Default (mine))"),("saveas",v,"Save as","Save under the name in the box")):I(g,j,c,az,x,a-2,B,w);x+=self._cap_w(B)+16
			d["saveas"]=ab(aF(g,self.saveas_text,x,a,max(60,W-M-12-self._cap_w("Discard")-16-x),numbers=False),"A name for Save as (letters, digits, spaces)");B="Discard";I(g,j,"discard",E,W-M-12-self._cap_w(B),a-2,B,"Close the editor and bring back the saved zones");a+=28;a=self._flow(g,j,Z,M+12,a,m)+28;aA=len(self.zs.zones);nk=sum(1 for bO in self.zs.zones if bO.kind=="k");nr=sum(1 for bP in self.zs.zones if bP.kind=="r");aj,al=self.counts;aB="%s, %d keep clear, %d reserved; %s, %s; %d x %d, %s"%(L(aA,"zone"),nk,nr,L(aj,"gap"),L(al,"overlap"),self.W,self.H,R);l(g,o(aB,f-24),M+12,a+3,O if(aj or al)else e);a+=20;lx=M+12
			for aC,am in((ZONE_COLORS["w"],"window"),(ZONE_COLORS["k"],"keep clear"),(ZONE_COLORS["r"],"reserved"),("#C83030","gap or overlap"),("#E8C15A","overlap allowed")):q(g,lx,a+6,12,12,.9,aC);l(g,am,lx+16,a+3,e);lx+=16+C(am)+14
			a+=20;l(g,o("Mouse on the zone: arrows nudge it a square; Shift+arrows resize it; Delete twice removes it.",f-24),M+12,a+3,e)
			if k:
				wl=s.all_windows();aa=["(pick a window)"];self.pick_keys=[None]
				for y,aD in wl:an=s.zone_of(y);aa.append(o(aD+(' (in "%s")'%an if an else ""),290));self.pick_keys.append(y)
				if self.pick>=len(aa):self.pick=0
				dd=G.CreateDropDown(ai,aa,self.pick);dd.SetPos(ah,N+32);g.Add(dd);d["w_pick"]=ab(dd,"A window for this zone; the zone shows where it would sit")
			aE,aG=Kit.anchor_pos("B",W,T)
			if Q(D):x,ao=D.GetX(),D.GetY()
			else:x,ao=self.bar_pos or Kit.load_pos(aK,(aE or 200,aG or 200),(W,T))
			ax(g,x,ao,W,T);G.AddGump(g);aI(g,self._bar_moved);self.bar,self.store,self.c=g,j,d;self.raws={}
			for c in ag+["saveas"]:
				ap=Kit.client_control(d[c])if c in d else None
				if ap is not None:self.raws[c]=ap
			self.fields=None;self.focus_was=None;self.show_fields();u(D)
		def _bar_moved(self):Kit.save_pos(aK,self.bar);self.bar_pos=Snap.pos(self.bar)
		def _values(self,z):
			x,y,w,h=z.px
			if self.px_mode:return tuple(str(b)for b in(x,y,w,h))
			a=p();return tuple(str(c)for c in(int(round(float(x)/a)),int(round(float(y)/a)),max(1,int(round(float(w)/a))),max(1,int(round(float(h)/a)))))
		def show_fields(self):
			c=self.c;z=self.zs.by_id(self.sel)if self.sel else None
			if z is None or "col"not in c:return
			b=self._values(z)
			if b!=self.fields:
				self.fields=b
				for e,t in zip(self.FIELDS,b):c[e].SetText(t)
			x,y,w,h=z.px
			if self.px_mode:a=p();d="%d x %d squares at square %d, %d"%(max(1,int(round(float(w)/a))),max(1,int(round(float(h)/a))),int(round(float(x)/a)),int(round(float(y)/a)))
			else:d="%d x %d px at %d, %d"%(w,h,x,y)
			aa(c["px"],o(d,self.BAR_W-K-12-c["px_x"]))
		def _over(self,z):
			m=aw()
			if m is None:return True
			for r in(Snap.rect(self.bar),tuple(z.px)):
				if r is not None and r[0]<=m[0]<r[0]+r[2]and r[1]<=m[1]<r[1]+r[3]:return True
			return False
		def _key(self,name):
			a=False
			for k in self.KEYS[name]:
				if API.IsKeyPressed(k):a=True;break
			b=self.keys_was.get(name,False);self.keys_was[name]=a;return a and not b
		def _focus(self):
			if not self.raws:return
			try:Typing._find();f=(Typing._get(None,"KeyboardFocusControl",Typing.uim)if Typing.uim is not None else None)
			except Exception:f=None
			self.raws_ok=Typing.uim is not None;n=0
			while f is not None and n<4:
				for a,b in self.raws.items():
					if Typing._same(f,b):return a
				f=Typing._get(f,"Parent");n+=1
			return
		def _box_texts(self):
			c=self.c
			try:return tuple(str(c[a].Text or "").strip()for a in self.FIELDS)
			except Exception:return
		def poll(self):
			if self.closed:return
			if not Q(self.bar):self.close(keep=False);return
			s=time.time()
			for f,b in list(self.frames.items()):
				z=self.zs.by_id(f);i=b.get("g")
				if z is None or not Q(i):continue
				if b["resize_at"]:
					r=Snap.rect(i)
					if r is not None and(r[2],r[3])!=b["size"]:k=p();aa(b["sum"],o("%d x %d squares"%(max(1,int(round(float(r[2])/k))),max(1,int(round(float(r[3])/k)))),max(40,r[2]-2*K-24)),P)
					if s-b["resize_at"]>=self.SETTLE:
						b["resize_at"]=0.
						if r is not None and(r[2],r[3])!=b["size"]:
							if z.lock:self.build_zone(z)
							else:self.landed(z,r[0],r[1],r[2],r[3],resized=True)
			l=SNAP.pressed()is True;self._sync_handles();self._edge_tick(l);self.pressed_was=l;a,c=self.store,self.c;z=self.zs.by_id(self.sel)if self.sel else None
			if j(a,"close")or j(a,"discard"):self.close(keep=False);return
			m=self._focus();t=Client.typing();u=self._key("enter");v=self._key("esc")
			if not t and not self.edge:
				n=bool(ar("ctrl"));x=bool(ar("shift"))
				if self._key("z")and n:self.do_undo()
				elif self._key("y")and n:self.do_redo()
				elif z is not None:
					for d,g in(("left",(-1,0)),("right",(1,0)),("up",(0,-1)),("down",(0,1))):
						if self._key(d)and self._over(z):self.nudge(z,g,x)
					if self._key("delete"):self.delete_pressed(z)
			if j(a,"add"):
				self.push();f=self.zs.new_id();q=Zone(f,"w",(0,0,1,1),"",(0,0),"d",0);q.set_px((self.W-320)//2,(self.H-240)//2,320,240,self.W,self.H)
				if not self._add_zone(q,True,"no room for another zone; remove one or make one smaller."):return
			elif j(a,"undo"):self.do_undo()
			elif j(a,"redo"):self.do_redo()
			elif j(a,"even")and z is not None:
				self.push();y=self.zs.even_out(z,self.W,self.H,p())
				if y<2:self.undo.pop();self.say("no zone sits flush beside this one in its row or column.")
				else:self._all_moved()
			elif j(a,"fill"):self.push();self.zs.fill_gaps(self.W,self.H,p());self._all_moved()
			elif j(a,"save"):self.save(self.zs.name if self.zs.name!=LAYOUT_DEFAULT else LAYOUT_MINE);return
			elif j(a,"saveas"):
				d=Layout.clean_name(safe(lambda:c["saveas"].Text,""),"")
				if not d:self.say("type a name in the box, then click Save as.")
				else:self.save(d if d!=LAYOUT_DEFAULT else LAYOUT_MINE);return
			elif j(a,"reflow")and c.get("reflow_from"):
				h=ZoneSet.parse(self.zs.name,ak((FRAMES_NAMED%self.zs.name)+"@"+c["reflow_from"],""))
				if h is not None:h.reflow(self.W,self.H,p());self.push();self._restore(([G.copy()for G in h.zones],self.sel,{}));self.changed()
			elif j(a,"from_default"):self.push();g=ZoneSet.default(self.W,self.H,(),False);self._restore(([H.copy()for H in g.zones],self.sel,{}));self.changed()
			elif j(a,"mirror"):
				self.push()
				for e in self.zs.zones:A,B,w,C=e.px;e.set_px(self.W-A-w,B,w,C,self.W,self.H)
				self._all_moved()
			elif j(a,"copyto"):self.copy_to()
			elif j(a,"units"):self.commit_rect(z,quiet=True)if z is not None else None;self.px_mode=not self.px_mode;self.rebuild=True
			if z is not None and not self.rebuild:self.poll_zone(z,a)
			if z is not None and z.kind=="w"and not self.rebuild:self.poll_windows(z,a,c)
			if not self.rebuild:self.poll_fields(z,m,u,v,j(a,"apply"))
			self.focus_was=m;self.draw_marks()
			if self.rebuild:
				self.rebuild=False;self.saveas_text=str(safe(lambda:c["saveas"].Text,self.saveas_text)or "")
				for e in self.zs.zones:self.update_zone(e)
				self.build_bar()
		def _all_moved(self):
			for a in self.zs.zones:a.note_pins(self.W,self.H);self.place_zone(a)
			self.changed()
		def poll_zone(self,z,store):
			if j(store,"kind"):self.push();a=[g for g,h in ZONE_KINDS];z.kind=a[(a.index(z.kind)+1)%len(a)];z.hug=z.hug and z.kind=="w";self.build_zone(z);self.changed();self.rebuild=True
			elif j(store,"stack"):self.push();b=[i for i,r in ZONE_STACKS];z.stack=b[(b.index(z.stack)+1)%len(b)];self.build_zone(z);self.rebuild=True
			elif j(store,"prio"):self.push();z.prio=(z.prio+1)%(SHRINK_MAX+1);self.rebuild=True
			elif j(store,"overlap"):
				self.push();z.overlap=not z.overlap
				if not z.overlap:
					if not self.zs.push_clear(z,self.W,self.H,p()):o=self._blocker(z);self.say('zone "%s" still lies over "%s"; move it or make it smaller.'%(z.id,o.id if o is not None else "a zone"),e)
					z.note_pins(self.W,self.H)
				for c in self.zs.zones:self.build_zone(c)
				self.changed();self.rebuild=True
			elif j(store,"lock"):self.push();z.lock=not z.lock;self.build_zone(z);self.rebuild=True
			elif j(store,"split"):self.split(z)
			elif j(store,"join"):self.join(z)
			elif j(store,"solo"):self.push();z.solo=not z.solo;self.changed();self.rebuild=True
			elif j(store,"free"):self.push();z.free=not z.free;self.px_mode=self.px_mode or z.free;z.note_pins(self.W,self.H);self.changed();self.rebuild=True
			elif j(store,"dup"):self.duplicate(z)
			elif j(store,"remove"):self.remove(z)
			else:
				for d,f in(("al_l","l"),("al_t","t"),("al_r","r"),("al_b","b"),("same","s")):
					if j(store,d):self.align(z,f);break
		def poll_windows(self,z,store,c):
			L=self.layout;l=c.get("w_pick");g=time.time();m=j(store,"w_add")
			if l is not None and(g>=self._pick_next or g-HOST.input_at<=HOST.INPUT_FAST):
				self._pick_next=g+.2;i=Y(l,self.pick)
				if i!=self.pick:
					self.pick=i;a=self.pick_keys[i]if 0<i<len(self.pick_keys)else None;self.preview=self.preview_text(a,z)if a else "";self.build_zone(z);self.rebuild=True
					if not m:return
			d=self.orig_id(z.id)
			if m:
				a=self.pick_keys[self.pick]if 0<self.pick<len(self.pick_keys)else None
				if a is None:self.say("pick a window in the list first, then click Put it here.",e);return
				if L.frames is None or L.frames.by_id(d)is None:self.say('zone "%s" isn\'t saved yet; click Save, then put the window in it.'%z.id);return
				if L.zone_of(a)==d:self.say("%s already sits in this zone."%L.title_of(a),e);return
				n=L._map_zone()
				if(a!="worldmap"and d==n)or(a=="worldmap"and L.assign.get(d)):self.say("TazUO's World Map keeps its zone to itself; pick another zone for %s."%(L.title_of(a)if a!="worldmap"else "it"));return
				if L._too_small(a,L.frames.by_id(d)):return
				L.assign_to(a,d);self.pick,self.preview=0,"";self.build_zone(z);self.rebuild=True;return
			o=c.get("wins_rows")or[]
			for i,k in enumerate(o):
				for h in("up","down","out"):
					if not j(store,"w_%s_%d"%(h,i)):continue
					b=L.assign.get(d,[])
					if k not in b:break
					if h=="out":L.assign_to(k,None)
					else:
						f=b.index(k);t=f-1 if h=="up"else f+1
						if 0<=t<len(b):
							b[f],b[t]=b[t],b[f]
							for p in b:L._refit(p)
							L.save_assign();L.dirty=L.fresh=True;ai()
					self.build_zone(z);self.rebuild=True;return
		def preview_text(self,key,z):return self.layout.preview_text(key,z,self.layout.assign.get(self.orig_id(z.id),[]))
		def poll_fields(self,z,a,enter,esc,apply):
			c=self.c
			if z is None or "name"not in c:return
			d=self.focus_was if(self.focus_was is not None and a!=self.focus_was)else None
			if esc and(a is not None or self._edited(z)):self._refields();c["name"].SetText(z.id);return
			if(enter and a=="name")or d=="name"or apply:
				b=str(safe(lambda:c["name"].Text,z.id)or "").strip()
				if b!=z.id:self.rename(z,b);return
			if a is None and d is None and enter and not self.raws_ok:
				b=str(safe(lambda:c["name"].Text,z.id)or "").strip()
				if b!=z.id:self.rename(z,b);return
				self.commit_rect(z);return
			if((enter and a in self.FIELDS)or(d in self.FIELDS and a not in self.FIELDS)or apply):self.commit_rect(z)
		def _edited(self,z):a=self._box_texts();b=str(safe(lambda:self.c["name"].Text,z.id)or "").strip();return(a is not None and a!=self._values(z))or b!=z.id
		def commit_rect(self,z,quiet=False):
			a=self._box_texts()
			if a is None or a==self._values(z):return
			try:d,f,w,h=[int(g)for g in a]
			except Exception:
				if not quiet:self.say("type whole numbers in Col, Row, W and H.")
				self._refields();return
			b=1 if self.px_mode else p();x,y=max(0,d)*b,max(0,f)*b;w,h=max(1,w)*b,max(1,h)*b;c="%d x %d %s"%(max(1,int(a[2])),max(1,int(a[3])),"px"if self.px_mode else "squares")
			if w<ZONE_MIN_W or h<ZONE_MIN_H:
				if not quiet:self.say('zone "%s" can\'t be %s: the smallest zone is %d x %d px.'%(z.id,c,ZONE_MIN_W,ZONE_MIN_H))
				self._refields();return
			if z.lock:self.say('zone "%s" is locked; click Lock to change it.'%z.id,e);self._refields();return
			if not self.apply_rect(z,x,y,w,h,c):self._refields()
		def rename(self,z,name):
			name=Layout.clean_name(name,"")
			if not name or name.lower()=="frames"or self.zs.by_id(name)is not None:self.say('zone "%s" can\'t be called "%s": %s.'%(z.id,name,"a name needs letters or digits"if not name else "the name is taken"if self.zs.by_id(name)is not None else "that name is kept"));self.c["name"].SetText(z.id);return
			self.push();a=z.id;z.id=name
			for k,v in self.renames.items():
				if v==a:self.renames[k]=name;break
			else:self.renames[a]=name
			b=self.frames.pop(a,None)
			if b is not None:self.frames[name]=b
			self.sel=name;self.multi=set(name if c==a else c for c in self.multi);self.said=None;self.build_zone(z);self.rebuild=True
		def nudge(self,z,d,b):
			if z.lock:self.say('zone "%s" is locked; click Lock to change it.'%z.id,e);return
			a=1 if z.free else p();x,y,w,h=z.px
			if b:self.apply_rect(z,x,y,max(ZONE_MIN_W,w+d[0]*a),max(ZONE_MIN_H,h+d[1]*a))
			else:self.apply_rect(z,x+d[0]*a,y+d[1]*a,w,h)
		def delete_pressed(self,z):
			a=time.time()
			if(self.del_armed is not None and self.del_armed[0]==z.id and a-self.del_armed[1]<=3.):self.del_armed=None;self.remove(z);return
			self.del_armed=(z.id,a);T('press Delete again to remove zone "%s".'%z.id,e)
		def remove(self,z):
			if z.lock:self.say('zone "%s" is locked; click Lock to remove it.'%z.id,e);return
			self.push();self.zs.zones=[b for b in self.zs.zones if b is not z];a=self.frames.pop(z.id,None)
			if a is not None:u(a.get("g"))
			self.multi.discard(z.id);self.sel=self.zs.zones[0].id if self.zs.zones else None;self.changed();self.rebuild=True
		def split(self,z):
			if z.lock:self.say('zone "%s" is locked; click Lock to change it.'%z.id,e);return
			x,y,w,h=z.px;f=w>=h;c=w if f else h;d=ZONE_MIN_W if f else ZONE_MIN_H;g=p();a=int(round(c/2./g))*g
			if not d<=a<=c-d:a=c//2
			if a<d or c-a<d:self.say('zone "%s" is too small to split.'%z.id);return
			self.push();b=z.copy();b.id=self.zs.new_id();W,H=self.W,self.H
			if f:z.set_px(x,y,a,h,W,H);b.set_px(x+a,y,w-a,h,W,H)
			else:z.set_px(x,y,w,a,W,H);b.set_px(x,y+a,w,h-a,W,H)
			z.note_pins(W,H);b.note_pins(W,H);self.zs.zones.append(b);self.build_zone(z);self.build_zone(b);self.changed();self.rebuild=True
		def join(self,z):
			if z.lock:self.say('zone "%s" is locked; click Lock to change it.'%z.id,e);return
			x,y,w,h=z.px;D=SNAP_DIST;a=None
			for o in self.zs.zones:
				if o is z or o.px is None or o.lock or o.kind!=z.kind:continue
				b,c,d,f=o.px
				if abs(c-y)<=D and abs(f-h)<=D and(abs(b-(x+w))<=D or abs(x-(b+d))<=D):a=o
				elif abs(b-x)<=D and abs(d-w)<=D and(abs(c-(y+h))<=D or abs(y-(c+f))<=D):a=o
				if a is not None:break
			if a is None:self.say('no zone of the same height or width sits flush beside "%s".'%z.id);return
			self.push();b,c,d,f=a.px;g,i=min(x,b),min(y,c);z.set_px(g,i,max(x+w,b+d)-g,max(y+h,c+f)-i,self.W,self.H);z.note_pins(self.W,self.H);self.zs.zones=[r for r in self.zs.zones if r is not a];j=self.frames.pop(a.id,None)
			if j is not None:u(j.get("g"))
			self.multi.discard(a.id);self.build_zone(z);self.changed();self.rebuild=True;self.say('zone "%s" joined into "%s"; its windows become free when saved.'%(a.id,z.id),e)
		def _add_zone(self,a,check,text):
			self.zs.zones.append(a)
			if check and not self.zs.push_clear(a,self.W,self.H,p()):self.zs.zones.remove(a);self.undo.pop();self.say(text);return False
			a.note_pins(self.W,self.H);self.sel,self.multi=a.id,set();self.build_zone(a);self.changed();self.rebuild=True;return True
		def duplicate(self,z):self.push();a=z.copy();a.id=self.zs.new_id();a.lock=False;b=p();x,y,w,h=z.px;a.set_px(x+b,y+b,w,h,self.W,self.H);self._add_zone(a,not a.overlap,"no room for a copy of zone \"%s\"; make room first."%z.id)
		def align(self,z,edge):
			h=[G for G in[self.zs.by_id(H)for H in self.multi if H!=z.id]if G is not None and not G.lock]
			if not h:return
			self.push();x,y,w,i=z.px;a=[]
			for p in h:
				f,g,b,c=p.px;r={"l":(x,g,b,c),"t":(f,y,b,c),"r":(x+w-b,g,b,c),"b":(f,y+i-c,b,c)}.get(edge,(f,g,w,i));d=p.px;p.set_px(r[0],r[1],r[2],r[3],self.W,self.H)
				if self._blocker(p)is not None:p.set_px(d[0],d[1],d[2],d[3],self.W,self.H);a.append(p.id)
				p.note_pins(self.W,self.H)
			if a:self.say("%s would cover another zone, so %s stayed where %s %s."%(", ".join('"%s"'%W for W in a),"it"if len(a)==1 else "they","it"if len(a)==1 else "they","was"if len(a)==1 else "were"),e)
			self._all_moved()
		def copy_to(self):
			a=self.zs.name;self.others=None
			if self.zs.generated or a==LAYOUT_DEFAULT or a not in self.layout.frame_names():self.say("save these zones first (Save or Save as), then click Copy to.",e);return
			d=ratio_class(self.W,self.H);b=self.zs.copy(a);b.screen=(self.W,self.H);b.grid=p()
			for f in b.zones:f.note_pins(self.W,self.H)
			g=b.save_text();c=[h for h in("narrow","wide","ultrawide")if h!=d]
			for k in c:Z((FRAMES_NAMED%a)+"@"+k,g)
			T('frame layout "%s" copied to %s screens.'%(a," and ".join(c)),aj)
		def warnings(self):
			a=[];c=self.layout
			for z in self.zs.zones:
				if z.kind!="w"or z.px is None:continue
				for k in c.assign.get(self.orig_id(z.id),[]):
					b=c._min_of(k)
					if b and(z.px[2]<b[0]or z.px[3]<b[1]):a.append('zone "%s" is %d x %d, smaller than %s can be (%d x %d)'%(z.id,z.px[2],z.px[3],c.title_of(k),b[0],b[1]))
			d,e=self.counts
			if d:a.append("the zones leave %s (Fill the gaps closes them)"%L(d,"gap"))
			if e:a.append("%s of zones without Overlap on"%L(e,"overlap"))
			if not any(f.kind=="k"for f in self.zs.zones):a.append("no keep-clear zone: nothing marks the game view")
			return a
		def save(self,name):
			self.others=None
			for w in self.warnings():T("note: %s."%w,e)
			a=self.zs.copy(name);a.generated=False;a.ver=2;self.layout.save_frames(a,name,self.W,self.H);L,d=self.layout,False
			for b,c in self.renames.items():
				if b!=c and b in L.assign and c not in L.assign:L.assign[c]=L.assign.pop(b);d=True
			if d:L.save_assign()
			T('frame layout "%s" saved.'%name,aj);self.close(keep=True);self.layout.use_frames(name,tell=False)
	def a7():k["editor"]=None
	def aQ(fresh=False):
		L=LAYOUT;W,H=J()
		if k["editor"]is not None or W<=0 or H<=0 or not L.enabled:return
		if fresh:
			c=L.frame_names();n,b=2,"Mine"
			while b in c or b==LAYOUT_DEFAULT:b="Mine %d"%n;n+=1
			a=ZoneSet(b,[],p(),(W,H));z=Zone("Zone 1","w",(0,0,1,1),"",(0,0),"d",0);z.set_px((W-320)//2,(H-240)//2,320,240,W,H);a.zones.append(z)
		elif L.frames_name==LAYOUT_DEFAULT:a=ZoneSet.default(W,H,L.occupied(),False);a.generated=False
		else:a=L.load_frames(L.frames_name,W,H)or L.frames_in_use(W,H).copy()
		k["editor"]=LayoutEditor(L,a,a7);k["editor"].open()
	def a8():
		L=LAYOUT;b=L.frames
		if b is None or not(L.seamless and L.enabled)or k["editor"]is not None:return(),None
		a=Layout._game_px(b)
		def c(r):return a is None or not(r[0]<a[0]+a[2]and a[0]<r[0]+r[2]and r[1]<a[1]+a[3]and a[1]<r[1]+r[3])
		d=tuple((tuple(f.px),f.solo)for f in b.zones if f.kind!="k"and f.px is not None and c(f.px));return d,a if L.fit_view else None
	def a9(items,o,W,H):
		l=G.CreateGump(False,False);r=Kit.WINDOW_BG;P=[Kit.pic_size(r+bF)for bF in range(9)];g=[bG[0]for bG in items];t=[{"T":[],"B":[],"L":[],"R":[]}for bH in g]
		def z(x,y,w,h):
			aG(l,r+4,x,y,w,h);b=q(l,x,y,w,h,.01,"#000000")
			if b is not None:b.SetAcceptMouseInput(True)
		for e,f,c,d in g:z(e,f,c,d)
		for i in range(len(g)):
			for m in range(i+1,len(g)):
				A=None if items[i][1]or items[m][1]else aP(g[i],g[m])
				if A is None:continue
				p,n,u,j,k=A;B=0 if p=="v"else 1;C,D=(i,m)if g[i][B]<g[m][B]else(m,i);t[C]["R"if p=="v"else "B"].append((j,k));t[D]["L"if p=="v"else "T"].append((j,k))
				if u>n:z(*((n,j,u-n,k-j)if p=="v"else(j,n,k-j,u-n)))
		for i,(e,f,c,d)in enumerate(g):
			for E,F,I,J,K in(("T",1,e,e+c,lambda a,b:(a,f,b-a,P[1][1])),("B",7,e,e+c,lambda a,b:(a,f+d-P[7][1],b-a,P[7][1])),("L",3,f,f+d,lambda a,b:(e,a,P[3][0],b-a)),("R",5,f,f+d,lambda a,b:(e+c-P[5][0],a,P[5][0],b-a))):
				for j,k in a6(I,J,t[i][E]):aG(l,r+F,*K(j,k))
		Grid.show_overlay(l,0,0,W,H,True);N["g"]=l
		if o is None or o[2]<=2*s or o[3]<=2*s:return
		v=G.CreateGump(False,False);e,f,c,d=o
		for L,M,O,Q,R in((0,0,c,s,am),(0,d-s,c,s,am),(0,0,s,d,am),(c-s,0,s,d,am),(s,s,c-2*s,1,an),(s,d-s-1,c-2*s,1,an),(s,s,1,d-2*s,an),(c-s-1,s,1,d-2*s,an)):q(v,L,M,O,Q,1.,R)
		Grid.show_overlay(v,e,f,c,d);ae["g"]=v
	def ba():
		b=Kit._raw_gump(N["g"])if N["g"]is not None and not B["off"]else None
		if b is None or not Client.on_client_thread():return
		try:
			a=B["gumps"]
			if a is None:import System;t=Tz.T("ClassicUO.Game.Managers.UIManager");B["same"]=System.Object.ReferenceEquals;B["ver"]=t.GetField("_gumpsStructureVersion",Client.flags(static=True,public=False));a=B["gumps"]=Tz.get(None,"Gumps",t)
			d=B["ver"];c=int(d.GetValue(None))if d is not None else None
			if c is not None and c==B["seen"]and b is B["raw"]:return
			B["seen"],B["raw"]=c,b;e=a.Last;g=B["same"]
			if e is None or g(e.Value,b)or(e.Previous is not None and g(e.Previous.Value,b)):return
			f=a.Find(b)
			if f is None:return
			a.Remove(f);a.AddBefore(a.Last,f)
			if d is not None:d.SetValue(None,c+1);B["seen"]=c+1
		except Exception:B["off"]=True
	def bb(now):
		if now<k["back_at"]:return
		k["back_at"]=now+a3;W,H=J();a,b=a8();c=(W,H,a,b,av())
		if c==k["back_sig"]and(not a or(Q(N["g"])and(b is None or Q(ae["g"])))):return
		k["back_sig"]=c;d,N["g"]=N["g"],None;e,ae["g"]=ae["g"],None
		if a and W>0 and H>0:a9(a,b,W,H)
		u(d);u(e)
	def bc(key):
		for a,b in a4:
			if key==a or(a.endswith(".")and key.startswith(a)):return b
		return
	def aR(total,b):
		c,a=[],0
		for i,d in enumerate(b):n=total-a if i==len(b)-1 else int(round(total*d));c.append((a,n));a+=n
		return c
	def bd(i,W,H):
		t=int(_clampv(STRIP_SHARE*H,TOP_MIN,TOP_MAX));c=int(_clampv(STRIP_SHARE*H,BOT_MIN,BOT_MAX))
		if i==2:d=int(_clampv(.3*H,200,340));b=[("Frames","w",0,0,W,t,"r","frames"),("Game","k",0,t,W,H-t-d,"d",None)];e=(("Paperdoll","gear"),("Bags","bag"),("Action bar","bar"),("Trackers","watch"),("Map","map"));b+=[(bF,"w",r,H-d,G,d,"d",bG)for(r,G),(bF,bG)in zip(aR(W,(.18,.18,.28,.18,.18)),e)]
		else:a=int(_clampv(.24*W,260,460))if i==3 else int(_clampv(SIDE_SHARE*W,SIDE_MIN,SIDE_MAX));l,f=(W-a,0)if i==3 else(0,a);b=[("Game","k",f,0,W-a,H-c,"d",None),("Action bar","w",f,H-c,W-a,c,"r","bar")];e=(("Frames","frames"),("Paperdoll","gear"),("Bags","bag"),("Trackers","watch"));b+=[(bJ,"w",l,bH,a,bI,"d",bK)for(bH,bI),(bJ,bK)in zip(aR(H,(.22,.26,.26,.26)),e)]
		g=ZoneSet(ac[i][0],[],p(),(W,H));h={}
		for j,m,x,y,w,n,o,k in b:
			z=Zone(j,m,(0,0,1,1),"",(0,0),o,0);z.set_px(x,y,w,n,W,H);z.note_pins(W,H);g.zones.append(z)
			if k:h[k]=j
		return g,h
	def aS(i,W,H):
		L=LAYOUT;b=L.parse_windows(WINDOWS_DEFAULT)[1]
		if i<2:a=b if i==0 else L.parse_windows(WINDOWS_MIRRORED)[1];d=set(g for g,h in a.items()if any(L.gump_of(r)is not None for r in h));return ZoneSet.default(W,H,d,n["look"].get("game",True)),LAYOUT_DEFAULT,a
		e,f=bd(i,W,H);a={}
		for k in sorted(set(L.wins)|set(x for w in b.values()for x in w)):
			c=f.get(bc(k))
			if c:a.setdefault(c,[]).append(k)
		return e,ac[i][0],a
	def be(i,W,H):
		b=(i,W,H,n["look"].get("game",True));a=n["cards"].get(b)
		if a is None:a=n["cards"][b]=aS(i,W,H)[0]
		return a
	def az(key):
		for a,b in n["assign"].items():
			if key in b:return a
		return
	def aA():
		e,U["g"]=U["g"],None;u(e);b=n["zs"];W,H=J();L=LAYOUT
		if b is None or W<=0 or H<=0:return
		g=G.CreateGump(False,False)
		for z in b.zones:
			if z.px is None or z.kind=="r":continue
			x,y,w,h=z.px;c=ZONE_COLORS.get(z.kind,"#3A78C8");q(g,x,y,w,h,.22,c)
			for f,i,j,k in((x,y,w,2),(x,y+h-2,w,2),(x,y,2,h),(x+w-2,y,2,h)):q(g,f,i,j,k,.9,c)
			if z.kind=="k":a=["Game area"]
			else:a=[z.id]+([L.title_of(r)for r in n["assign"].get(z.id,[])if r in L.wins]or["(empty)"])
			a=[o(bF,max(20,w-28))for bF in a[:max(1,(h-16)//20)]];q(g,x+6,y+6,max(C(bG)for bG in a)+12,20*len(a)+6,.85,"#000000")
			for d,t in enumerate(a):l(g,t,x+12,y+9+20*d,P if d==0 else D)
		Grid.show_overlay(g,0,0,W,H);U["g"]=g
	def aT(i):W,H=J();a,b,c=aS(i,W,H);n.update({"preset":i,"zs":a,"fname":b,"assign":dict((d,list(f))for d,f in c.items())})
	def aU():
		c,a=ao["c"],n["look"]
		for k in a:
			if k in c:a[k]=bool(c[k].IsChecked)
	def bf():
		s=n;c=s["step"];a,m=K,Kit.GAP;W=a1;d=W-2*a;X=LAYOUT;w=X.all_windows()if c==1 else[];i=(30+R+56+10,32+26*max(1,len(w))+8,32+26*len(ay)+30)[c];Y=a+30+m+i+m+44+a;g,p,Z=ag.begin(W,Y)
		if not k["minimized"]:
			ag.frame(g,settings=False,after="Step %d of 3"%(c+1));y=a+30+m
			if c==0:
				F(g,a,y,d,i,"LAYOUT  (click one; the screen shows it)");x,B=J();f=y+32;aa=a+(d-5*M-4*aL)//2
				for r,(N,O)in enumerate(ac):
					j=aa+r*(M+aL);G=r==s["preset"]
					if G:q(g,j-2,f-2,M+4,R+4,.95,"#E8C15A")
					q(g,j,f,M,R,1.,"#101010")
					if x>0 and B>0:
						Q,S=M/float(x),R/float(B)
						for z in be(r,x,B).zones:
							if z.px is None or z.kind=="r":continue
							zx,zy,zw,zh=z.px;q(g,j+int(zx*Q)+1,f+int(zy*S)+1,max(1,int(zw*Q)-2),max(1,int(zh*S)-2),.85 if G else.5,ZONE_COLORS.get(z.kind,"#3A78C8"))
					T=o(N,M);l(g,T,j+(M-C(T))//2,f+R+6,P if G else D);au(g,j,f,M,R+26,V(("preset",r)),"Use %s: %s"%(N,O[:1].lower()+O[1:]))
				l(g,o(ac[s["preset"]][1],d-24),a+12,f+R+32,e)
			elif c==1:
				F(g,a,y,d,i,"WINDOWS  (click to change a zone)");b=y+32
				if not w:l(g,"No windows yet; turn modules on, then come back.",a+12,b+3,e)
				for H,ab in w:ad=az(H);l(g,o(ab,300),a+12,b+3);I(g,p,"z_"+H,t,a+330,b-2,"Zone: "+(ad or "free"),"Click: next zone (free: stays where it is)",on_click=V(("cycle",H)));b+=26
			else:
				F(g,a,y,d,i,"LOOK");b=y+32
				for U,ae,af in ay:Z[U]=Kit.add_check(g,ae,a+12,b,s["look"][U],af);b+=26
				l(g,"Change any of this later in Settings > Interface.",a+12,b+5,e)
			u=y+i+m;F(g,a,u,d,44);I(g,p,"cancel",E,a+12,u+10,"Cancel","Close without changing anything",on_click=V("cancel"));h=("done",v,"Done","Use this layout")if c==2 else("next",A,"Next","Go to the next step");L=W-a-12-35-C(h[2]);I(g,p,h[0],h[1],L,u+10,h[2],h[3],on_click=V(h[0]))
			if c:L-=55+C("Back");I(g,p,"back",t,L,u+10,"Back","Go back a step",on_click=V("back"))
		ag.end(g);bg()
	def af():Binds.scoped("interface.setup",bf)
	ag=Kit.Window(a_,"Interface Setup",k,ao,af,a0,default=(200,120),mini=a2,owner=False,lock=False,close_tip="Close without changing anything")
	def bg():
		c=ao["c"]
		if "status"in c:aa(c["status"],"%s: step %d of 3"%("Interface Setup",n["step"]+1))
	def aV():
		L=LAYOUT
		if not L.enabled:return
		if not n["open"]:Z(aJ,"1");n.update({"open":True,"step":0,"cards":{},"look":{"seam":True,"fit_view":L.fit_view,"game":L.game_grows}});k["minimized"]=False;aT(n["preset"])
		aA();af()
	def aB():n["open"]=False;a,U["g"]=U["g"],None;u(a);ag.close()
	def bh(i):aT(i);aA();af()
	def bi(key):
		s=n;a=[None]+[g.id for g in s["zs"].zones if g.kind=="w"];b=az(key);d=az("worldmap");i=a.index(b)if b in a else 0
		for f in a:
			i=(i+1)%len(a);c=a[i]
			if c is None:break
			e=[h for h in s["assign"].get(c,[])if h!=key]
			if not((key=="worldmap"and e)or(key!="worldmap"and c==d)):break
		if b is not None:s["assign"][b]=[r for r in s["assign"][b]if r!=key]
		if c is not None:s["assign"].setdefault(c,[]).append(key)
		aA();af()
	def aW(d):aU();n["step"]=max(0,min(2,n["step"]+d));af()
	def bj():
		aU();s=n;a=LAYOUT;W,H=J();f,c,d=s["zs"],s["fname"],s["look"];a.seamless,a.fit_view,a.game_grows=d["seam"],d["fit_view"],d["game"];a.save_opts()
		if c!=LAYOUT_DEFAULT:f.generated=False;a.save_frames(f.copy(c),c,W,H)
		a.use_frames(c,tell=False);a.assign=dict((i,list(h))for i,h in s["assign"].items()if h);a.unfree(None);a.save_assign();b=ac[s["preset"]][0];b=b+" (mine)"if b in(LAYOUT_DEFAULT,LAYOUT_MIRRORED)else b;Z(LAYOUT_NAMED%b,a.windows_text());e=a.layout_names()
		if b not in e:e.append(b);Z(LAYOUT_LIST,",".join(e))
		a.layout_name=b;Z(LAYOUT_ACTIVE,b);a.free_scrolled();a.placed={};a.refit_all();ai();aB();ap();g=sum(1 for r in a.assign.values()for w in r if a.gump_of(w)is not None);X('"%s" in use: %s placed.'%(b,L(g,"window")),aj)
	def aX():aB();X("setup closed; nothing changed.",e)
	aY={"setup":aV,"preset":bh,"cycle":bi,"next":lambda:aW(1),"back":lambda:aW(-1),"done":bj,"cancel":aX}
	def bk():
		a=LAYOUT;n=sum(len(d)for d in a.assign.values());b=a.frames
		if not n:return "No window in a zone yet: click Set up, or Arrange windows"
		c=Layout._game_px(b)if b is not None else None;return "%s in %s%s"%(L(n,"window"),L(len(a.assign),"zone"),"; game area %d x %d"%c[2:]if c else "")
	def aq(g,names,i,x,y,tip):a=G.CreateDropDown(aM,names,i);a.SetPos(x,y);g.Add(a);return ab(a,tip)
	def bl(f,x,y):L=LAYOUT;a=m["frame_names"]=[LAYOUT_DEFAULT]+L.frame_names();c=a.index(L.frames_name)if L.frames_name in a else 0;b=m["layout_names"]=["(none)",LAYOUT_DEFAULT,LAYOUT_MIRRORED]+L.layout_names();d=L.layout_name or "(none)";e=b.index(d)if d in b else 0;l(f.g,"Zones:",x+12,y+3,D);l(f.g,"Windows:",x+12,y+31,D);m["zones"]=(aq(f.g,a,c,x+92,y,"The frame layout in use (its zones)"),c);m["windows"]=(aq(f.g,b,e,x+92,y+28,"The window layout in use; pick one to place every window"),e)
	def bm(f,x,y):
		L=LAYOUT;d=L.all_windows();j=L.page_preview;e=y-26*len(d)-(20 if j else 0);b=["free"]+[r for r in L.zone_choices()if r];m["zone_dd"]=[]
		for g,l in d:
			a=L.zone_of(g);c=h=b
			if a is not None and a not in b:c,h=b+[a],b+[o("%s (missing)"%a,aM-30)]
			i=c.index(a)if a in c else 0;k=aq(f.g,h,i,x+302,e,"The zone it sits in (free: stays where you put it)");m["zone_dd"].append((g,k,i,c));e+=26
	def bn(f,x,y):
		L=LAYOUT;a=m["situ_names"]=["(none)",LAYOUT_DEFAULT,LAYOUT_MIRRORED]+L.layout_names();m["situ_dd"]=[]
		for n,(b,d,e)in enumerate(aN):c=L.situ.get(b,"");i=a.index(c)if c in a else 0;l(f.g,d,x+12,y+3+28*n,D);m["situ_dd"].append((b,aq(f.g,a,i,x+92,y+28*n,e),i))
	def bo():
		a=LAYOUT.share_code()
		if not a:X("no zones to share yet.",O);return
		ad["code"]=a;f=S.f
		if f is not None and "code"in f.c:Kit.set(f.c["code"],"Text",a)
		k["jobs"].append(lambda:bp(a));X("layout code ready; Ctrl+A then Ctrl+C in the field copies it.",aj)
	def bp(code):
		try:Kit.write_safe(Kit.data_path(Layout.CODE_FILE),code+"\n")
		except Exception as a:X("couldn't write %s (%s)."%(Layout.CODE_FILE,a),O)
	def bq():f=S.f;c=f.c.get("code")if f is not None else None;LAYOUT.load_code(str(c.Text or "")if c is not None else ad["code"])
	def br(w):
		ap();L=LAYOUT;b=L.all_windows();a=L.page_preview;i=("check","snap","Snap windows together","Windows dropped near each other line up");c=(("buttons",(("look",t,"Look: %s"%Kit.LOOK_NAMES[av()],"Next look: Classic, Dark, Parchment or High contrast"),("tsize",t,"Text size: %d%%"%int(round(Kit.tscale*100)),"Text in lists and bars (TazUO's own UI scale sizes every window)"))),("check","compact","Compact rows","Tighter rows in lists and settings; smaller frames"),("check","fade","Fade windows when idle","Dim windows until the mouse is over them or they change"),("num","fade_to","Faded:","How solid an idle window stays (20-90)","%",20,90),("num","fade_after","After:","Seconds without the mouse or a change before it fades (2-30)","s",2,30),("check","fade_all","Fade the Action Bar and unit frames too","Off: they stay solid while other windows fade"));d=("ACCESSIBILITY",(("check","cblind","Colour-blind marks","Letters beside notoriety and HP colours; colour-blind palette"),("check","streamer","Streamer mode","Hide names, guild and coordinates in Virtue Assistant windows")));f=(i,("check","grid_on","Show the grid","Show the snapping grid over the screen"),("num","grid","Grid:","Grid spacing for snapping","px",8,512))
		if VA_ALONE:return(("ZONES",(("note","Zones, layout and snapping are set in the full"),("note","Virtue Assistant."))),)
		if not L.enabled:return(("ZONES",(("note","Interface is off, so zones are off."),("note","Tick Interface on the Modules tab to use them."))),("LOOK",c),d,("SNAPPING",f))
		j=(("arrange",v,"Done","Lock every window in its zone")if L.arrange else("arrange",A,"Arrange windows","Unlock windows to drag them between zones (Esc or Done locks them)"));k=((("reclaim_undo",E,"Undo","Put the zones back as before Reclaim space"),)if L._undo_load()is not None else());g=(("SCREEN",(("note",o(bk(),w-24)),("note",o(L.status_text(),w-24)),("buttons",(("setup",A,"Set up","Pick a ready-made layout in three steps"),j)),("buttons",(("edit",t,"Edit zones","Drag, resize, split or join zones"),("new",v,"New zones","Start a new frame layout with one zone"))))),("LOOK",tuple(("check",r,x,y)for r,x,y in ay)+c),d,("SNAPPING",f),("LAYOUTS  (saved)",(("buttons",(("save",v,"Save windows","Save where every window sits as the window layout in use"),("reset",E,"Reset","Go back to the Default window layout"),("free",E,"Free all","Take every window out of its zone"))),("buttons",(("remove",E,"Remove zones","Delete the frame layout in use (not Default)"),("check",A,"Check fit","Print where each window in a zone sits and if it fills it"))),("buttons",(("reclaim",A,"Reclaim space","Give the game area every gap beside it; windows keep their size"),)+k),("custom",60,bl),("buttons",(("share",t,"Share code","Put a code for the layouts in use in the field below"),("load_code",v,"Load code","Load the layout code in the field below"))),("text","code","Code:","Layout code: Ctrl+A then Ctrl+C copies it, Ctrl+V pastes one"))),("LAYOUTS BY SITUATION",(("check","situ_on","Switch layouts by situation","Use the layouts below in war mode, at the bank, in dungeons and in town"),("custom",28*len(aN),bn),("note","War mode first, then bank, dungeon, town"))))
		if not b:return g
		h=[("note",o(z,270),{"hue":D,"ndy":3,"h":26})for G,z in b]
		if a:h.append(("note",o(a.lstrip("!"),w-24),{"ndy":3,"hue":O if a.startswith("!")else e}))
		return g+(("WINDOWS  (the zone each sits in)",h+[("custom",0,bm)]),)
	def bs(b,new):
		L=LAYOUT;a=set(c for c in new if new[c]!=b.get(c))
		if a&set(("seam","fit_view","game")):
			L.seamless,L.fit_view,L.game_grows=new["seam"],new["fit_view"],new["game"];L.save_opts();L.dirty=True
			if a&set(("seam","fit_view")):L.fresh=True;L.seam_skip={};L.seam_wait={}
		if "snap"in a:
			SNAP.enabled=new["snap"]
			if not SNAP.enabled:SNAP.links.clear()
			aC()
		if "grid"in a:
			HOST.prefs["grid"]=str(new["grid"]);aC()
			if HOST.grid is not None:HOST.grid.redraw()
		if "grid_on"in a and new["grid_on"]!=ah():at()
		if "situ_on"in a:L.situ_set(new["situ_on"])
		for k in("compact","cblind","streamer"):
			if k in a:aD(k,new[k])
		if a&set(Fade.KEYS):FADE.set(new)
	def bt():o=Kit.LOOK_ORDER;HOST.set_look(o[(o.index(av())+1)%len(o)])
	def bu():o,a=Kit.TEXT_SIZES,int(round(Kit.tscale*100));aD("tsize",o[(o.index(a)+1)%len(o)]if a in o else o[0])
	def bv():
		if not LAYOUT.remove_frames(LAYOUT.frames_name):X("Default can't be deleted; pick another frame layout first.",O)
	bw=(("setup",aV),("arrange",lambda:LAYOUT.set_arrange(not LAYOUT.arrange)),("edit",lambda:aQ(False)),("new",lambda:aQ(True)),("remove",bv),("save",lambda:LAYOUT.save_windows()),("reset",lambda:LAYOUT.use_windows(LAYOUT_DEFAULT)),("free",lambda:LAYOUT.use_windows("")),("reclaim",lambda:LAYOUT.reclaim_space()),("reclaim_undo",lambda:LAYOUT.reclaim_back()),("check",lambda:LAYOUT.report_fit()),("look",bt),("tsize",bu),("share",bo),("load_code",bq))
	def bx(f):
		L=LAYOUT
		if L.page_refresh:L.page_refresh=False;S.f=None;HOST.refresh_settings(al);return
		for n,(b,a,e,c)in enumerate(m["zone_dd"]):
			i=Y(a,e)
			if i!=e and 0<=i<len(c):
				m["zone_dd"][n]=(b,a,i,c);d=None if i==0 else c[i];L.page_preview=""
				if d:W,H=J();g=L.frames_in_use(W,H)if W>0 and H>0 else None;L.page_preview=L.preview_text(b,g.by_id(d)if g is not None else None)
				L.assign_to(b,d);L.page_refresh=True;return
		if m["zones"]is not None:
			a,h=m["zones"];i=Y(a,h)
			if i!=h and 0<=i<len(m["frame_names"]):m["zones"]=(a,i);L.use_frames(m["frame_names"][i]);return
			a,k=m["windows"];i=Y(a,k)
			if i!=k and 0<=i<len(m["layout_names"]):m["windows"]=(a,i);L.use_windows(""if i==0 else m["layout_names"][i]);return
		for n,(l,a,o)in enumerate(m["situ_dd"]):
			i=Y(a,o)
			if i!=o and 0<=i<len(m["situ_names"]):m["situ_dd"][n]=(l,a,i);L.situ_pick(l,""if i==0 else m["situ_names"][i]);return
		for p,q in bw:
			if j(f.store,p):q();return
	S=Kit.Page(ad,br,a5,bs,clicks=bx)
	def by():m.update({"zones":None,"windows":None,"zone_dd":[],"situ_dd":[]});S.closed()
	def bz():
		k.update({"shutting":False,"docked":False,"queue":[],"minimized":False,"editor":None,"back_sig":None,"back_at":0.,"alone_up":False,"jobs":[]});n["open"]=False
		if VA_ALONE:ap();aE(al);return
		LAYOUT.set_enabled(True);ap();aO.service("interface.page",lambda:aE(al))
		if not ak(aJ,"")and not LAYOUT.assign and not ak(LAYOUT_ACTIVE,""):V("setup")()
	def bA():
		if VA_ALONE:
			c=HOST.config.win["g"]is not None
			if k["alone_up"]and not c:HOST.disable(al)
			k["alone_up"]=k["alone_up"]or c;return
		q=k["queue"]
		while q:
			a=q.pop(0);a="toggle_min"if a=="to_bar"else a
			if isinstance(a,tuple):aY[a[0]](*a[1:])
			elif not ag.action(a):aY[a]()
		if n["open"]and j(ao["store"],"close"):aX()
		b=k["editor"]
		if b is not None:
			W,H=J()
			if W>0 and H>0:b.keep(W,H)
			b.poll()
		d=time.time();LAYOUT.situ_tick(d,b is not None or n["open"]);Seam.hover(LAYOUT.arrange);bb(d);ba()
	def bB():
		while k["jobs"]and not k["shutting"]:k["jobs"].pop(0)()
	def bC():a=not(k["queue"]or n["open"]or Seam.recs or Seam.bare or VA_ALONE);return.25 if a and k["editor"]is None and N["g"]is None else.05
	def bD():
		k["shutting"]=True;a=k["editor"]
		if a is not None:a.close(keep=False,quiet=True)
		if n["open"]:aB()
		for b in(N,ae,U):c,b["g"]=b["g"],None;u(c)
		if not VA_ALONE:LAYOUT.set_enabled(False)
		aO.close()
	return{"start":bz,"tick":bA,"stop":bD,"client_tick":True,"config_height":S.height,"build_config":S.build,"poll_config":S.poll,"config_closed":by,"interval":bC,"thread_tick":bB,"thread_wanted":lambda:bool(k["jobs"])}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("interface","Interface","Zones, layout and the unified UI",_module_interface,.05,default_on=True,category="On screen")
