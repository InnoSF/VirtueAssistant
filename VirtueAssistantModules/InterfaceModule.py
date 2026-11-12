def _module_interface():
	P=Client.key_held;F=HOST.grid_shown;l=HOST.grid_size;Q=HOST.grid_toggle;I=HOST.poke;V=HOST.save_prefs;X=HOST.set_switch;Y=HOST.show_settings;J="interface";ap="Interface";aq="interface.setup";ar="Interface_setup_pos";Z="Interface_setup_seen";aa="VirtueAssistant_layout_editor_pos";at,au=600,(260,46);o,q,ab=100,64,12;ac=170;av=.25;m,K,L=3,"#D4AF37","#3A2A08";A=(("Sides","Bags and paperdoll left; map and trackers right"),("Mirrored","Map and trackers left; bags and paperdoll right"),("Bottom bar","Game on top; every window in one band below"),("Right column","Game left; windows stacked on the right"),("Compact","Windows stacked on the left; game on the right"));aw=(("unitframes.","frames"),("actionbar","bar"),("character","gear"),("bag","bag"),("ultima.","watch"),("hub","watch"),("meters","watch"),("worldmap","map"));R=(("seam","Join windows in zones into one panel","One frame round every zone, gold round the game view; hover a window's top for its title"),("fit_view","Fit the game view to the game area","Borderless, sized and locked to the game area"),("game","Give an empty zone's room to the game area","Widens the game area beside an empty zone"));B={"seam":False,"fit_view":True,"game":True,"snap":True,"grid_on":False,"grid":GRID_DEFAULT,"compact":False,"cblind":False,"streamer":False,"code":"","situ_on":False,"fade":False,"fade_to":40,"fade_after":6,"fade_all":False};a5=dict(B);e={"minimized":False,"shutting":False,"docked":False,"queue":[],"editor":None,"back_sig":None,"back_at":0.,"jobs":[]};M={"g":None,"c":{},"store":({},{})};p={"g":None};C={"g":None};t={"g":None};n={"gumps":None,"ver":None,"same":None,"off":False,"seen":None,"raw":None};j={"zones":None,"windows":None,"zone_dd":[],"frame_names":[],"layout_names":[],"situ_dd":[],"situ_names":[]};ad=(("war","War mode:","The window layout while you are in war mode"),("bank","Bank:","The window layout near your bank for 5 minutes after you open it"),("dungeon","Dungeon:","The window layout in a dungeon"),("town","Town:","The window layout in a guard zone"));k={"open":False,"step":0,"preset":0,"zs":None,"fname":LAYOUT_DEFAULT,"assign":{},"look":{},"cards":{}};ae,u,v=Kit.basics(e,ap)
	def N():L=LAYOUT;B.update({"seam":L.seamless,"fit_view":L.fit_view,"game":L.game_grows,"snap":SNAP.enabled,"grid_on":F(),"grid":l(),"compact":Kit.compact,"cblind":Kit.cblind,"streamer":Kit.streamer,"situ_on":L.situ["on"],"fade":FADE.on,"fade_to":int(round(FADE.to*100)),"fade_after":int(FADE.after),"fade_all":FADE.all})
	def ax():pass
	def af(a,b):
		e,f,i,j=a;g,h,k,l=b;D=SNAP_DIST
		for c,d in((e+i,g),(g+k,e)):
			m,n=max(f,h),min(f+j,h+l)
			if abs(d-c)<=D and n>m:return "v",min(c,d),max(c,d),m,n
		for c,d in((f+j,h),(h+l,f)):
			o,p=max(e,g),min(e+i,g+k)
			if abs(d-c)<=D and p>o:return "h",min(c,d),max(c,d),o,p
		return
	def ay(e,b,f):
		c,a=[],e
		for d,g in sorted(f):
			if d>a:c.append((a,min(d,b)))
			a=max(a,g)
		if a<b:c.append((a,b))
		return[(h,i)for h,i in c if i>h]
	class LayoutEditor(object):
		BAR_W=720;SETTLE=.3;FIELD_W=52;ROW=28;KEYS={"up":("UP",),"down":("DOWN",),"left":("LEFT",),"right":("RIGHT",),"delete":("DELETE",),"z":("Z",),"y":("Y",),"enter":("RETURN","KP_ENTER"),"esc":("ESCAPE",)};FIELDS=("col","row","w","h")
		def __init__(self,layout,zs,a):self.layout=layout;self.zs=zs;self.on_close=a;self.frames={};self.bar=None;self.store=({},{});self.c={};self.renames={};self.sel=zs.zones[0].id if zs.zones else None;self.multi=set();self.grid_was=None;self.fields=None;self.saveas_text="";self.bar_pos=None;self.rebuild=False;self.closed=False;self.others=None;self.W,self.H=Kit.screen();self.px_mode=False;self.undo,self.redo=[],[];self.keys_was={};self.focus_was=None;self.raws={};self.said=None;self.del_armed=None;self.marks=None;self.marks_sig=None;self.counts=(0,0);self.handles=[];self.handles_sig=None;self.edge=None;self.edge_g=None;self.edge_at=0.;self.pressed_was=False;self.pick=0;self.pick_keys=[];self.preview="";self.raws_ok=False;self._pick_next=0.
		def open(self):
			self.grid_was=F()
			if not self.grid_was:safe(Q)
			for z in self.zs.zones:self.build_zone(z)
			self.build_bar();self.draw_marks()
		def close(self,keep,quiet=False):
			if self.closed:return
			self.closed=True
			for c,b in list(self.frames.items()):Kit.dispose(b.get("g"))
			self.frames={};self._drop_handles()
			for a in("bar","marks","edge_g"):Kit.dispose(getattr(self,a));setattr(self,a,None)
			if self.grid_was is not None and F()!=self.grid_was:safe(Q)
			self.on_close();self.layout.dirty=True;self.layout.page_refresh=True
			if not keep and not quiet:Kit.say("the saved zones are back.",Kit.HUE_INFO)
		def _snap(self):return([a.copy()for a in self.zs.zones],self.sel,dict(self.renames))
		def push(self):
			self.undo.append(self._snap())
			if len(self.undo)>50:del self.undo[0]
			self.redo=[]
		def _restore(self,snap):
			b,a,c=snap
			for d in list(self.frames):Kit.dispose(self.frames[d].get("g"))
			self.frames={};self.zs.zones=[f.copy()for f in b];self.renames=dict(c);self.sel=(a if self.zs.by_id(a)is not None else(self.zs.zones[0].id if self.zs.zones else None));self.multi=set()
			for z in self.zs.zones:self.build_zone(z)
			self.rebuild=True
		def _hist(self,a,b,word):
			if not a:self.say("nothing to %s."%word,Kit.HUE_INFO);return
			b.append(self._snap());self._restore(a.pop())
		def do_undo(self):self._hist(self.undo,self.redo,"undo")
		def do_redo(self):self._hist(self.redo,self.undo,"redo")
		def say(self,text,hue=None):
			if text==self.said:return
			self.said=text;Kit.say(text,Kit.HUE_BAD if hue is None else hue)
		def _windows_in(self,z):L=self.layout;a=self.orig_id(z.id);return[L.title_of(b)for b in L.assign.get(a,[])]
		def orig_id(self,a):
			for b,c in self.renames.items():
				if c==a:return b
			return a
		def build_zone(self,z):
			c=self.frames.get(z.id,{}).get("g");x,y,w,h=z.px;M=Kit.MARGIN;a={"g":None,"resize_at":0.,"size":(w,h)};g=G.CreateModernGump(x,y,w,h,not z.lock,ZONE_MIN_W,ZONE_MIN_H,self._resized(z.id));g.SetAlpha(0)
			if z.lock:g.CanMove=False
			Kit.add_window_frame(g,w,h,corners=False,mouse=False);Kit.add_box(g,M,M,w-2*M,h-2*M,.25,ZONE_COLORS.get(z.kind,"#FFFFFF"))
			if z.kind=="w"and z.stack=="t":Kit.add_box(g,M,M+31,w-2*M,4,.9,"#E8C15A")
			self._draw_overlaps(g,z)
			if z.kind=="k":self._draw_game(g,z)
			if z.id==self.sel and self.pick:self._draw_preview(g,z)
			Kit.add_section(g,M,M,w-2*M,30);d=z.id==self.sel or z.id in self.multi;a["lbl"]=Kit.add_label(g,Kit.fit(z.id+("  (locked)"if z.lock else ""),w-2*M-24),M+12,M+7,Kit.HUE_TITLE if d else Kit.HUE_TEXT);b=self._windows_in(z)if z.kind=="w"else[];a["wins"]=Kit.add_label(g,Kit.fit(", ".join(b),w-2*M-24)if b else "",M+12,M+30+6,Kit.HUE_TEXT);a["sum"]=Kit.add_label(g,"",M+12,M+30+6+(20 if b else 0),Kit.HUE_INFO);Kit.catcher(g,M,M,w-2*M,30,self._select(z.id),"Select the zone (Shift+click: pick more)"+("; locked"if z.lock else "; drag to move it on the grid"),movable=not z.lock);Kit.place(g,x,y,w,h);Kit.add_front(g);Kit.no_snap(g);Kit.on_moved(g,self._moved(z.id));a["g"]=g;self.frames[z.id]=a;self.update_zone(z);Kit.dispose(c)
		def _draw_overlaps(self,g,z):
			x,y,w,i=z.px
			for o in self.zs.zones:
				if o is z or o.px is None or not(z.overlap or o.overlap):continue
				c,d,j,k=o.px;e,a=max(x,c),max(y,d);b,f=min(x+w,c+j),min(y+i,d+k)
				if b-e<4 or f-a<4:continue
				for h in range(e,b,12):Kit.add_box(g,h-x,a-y,min(4,b-h),f-a,.45,"#E8C15A")
		def _draw_game(self,g,z):
			e=self.zs.copy();Layout._overlap_shape(e);a,b,c,d=e.by_id(z.id).px;a-=z.px[0];b-=z.px[1]
			for r in((a,b+d-2,c,2),(a,b,2,d),(a+c-2,b,2,d),(a,b,c,2)):Kit.add_box(g,r[0],r[1],r[2],r[3],.9,"#E8C15A")
		def _draw_preview(self,g,z):
			a=self.pick_keys[self.pick]if 0<self.pick<len(self.pick_keys)else None
			if a is None or z.kind!="w":return
			L=self.layout;f=[h for h in L.assign.get(self.orig_id(z.id),[])if h!=a]+[a];x,y=z.px[0],z.px[1]
			for k,(b,c,d,e)in L.slots_for(z,f):Kit.add_box(g,b-x,c-y,max(1,d),max(1,e),.55,"#E8C15A"if k==a else "#202020");Kit.add_label(g,Kit.fit(L.title_of(k),max(20,d-16)),b-x+8,c-y+e-26,Kit.HUE_TEXT)
		def update_zone(self,z):
			a=self.frames.get(z.id)
			if a is None:return
			b=l();x,y,w,h=z.px;c="%s, %d x %d squares"%(z.kind_name(),max(1,int(round(float(w)/b))),max(1,int(round(float(h)/b))))
			if z.overlap:c+=", overlaps"
			Kit.set_text(a["sum"],Kit.fit(c,w-2*Kit.MARGIN-24));Kit.set_text(a["lbl"],Kit.fit(z.id+("  (locked)"if z.lock else ""),w-2*Kit.MARGIN-24),Kit.HUE_TITLE if(z.id==self.sel or z.id in self.multi)else Kit.HUE_TEXT)
		def _select(self,a):
			def b():
				b=bool(P("shift"))
				if b and self.sel is not None and a!=self.sel:
					if a in self.multi:self.multi.discard(a)
					else:self.multi.add(a);self.multi.add(self.sel)
					self.rebuild=True;I();return
				if a!=self.sel or self.multi:self.multi=set();self.sel=a;self.pick=0;self.rebuild=True;I()
			return b
		def _resized(self,a):
			def b(*c):
				b=self.frames.get(a)
				if b is not None:b["resize_at"]=time.time()
			return b
		def _moved(self,a):
			def b():
				z=self.zs.by_id(a);b=self.frames.get(a)
				if z is None or b is None or not Kit.is_open(b["g"]):return
				r=Snap.rect(b["g"])
				if r is None:return
				if(r[0],r[1])==(z.px[0],z.px[1]):return
				if z.lock:self.place_zone(z);self.say('zone "%s" is locked; click Lock to move it.'%z.id,Kit.HUE_INFO);return
				self.landed(z,r[0],r[1],z.px[2],z.px[3],resized=False)
			return b
		def _blocker(self,z):a=self.zs.overlaps(z);return a[0]if a else None
		def landed(self,z,x,y,w,h,resized=True):
			W,H=self.W,self.H;c=l()
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
					d,e,m,n=o.px
					if a is None and e<y+h+SNAP_DIST and y<e+n+SNAP_DIST:
						for f in(d+m,d-w,d,d+m-w):
							if abs(f-x)<=SNAP_DIST:a=f
					if b is None and d<x+w+SNAP_DIST and x<d+m+SNAP_DIST:
						for g in(e+n,e-h,e,e+n-h):
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
			with Kit.quiet:Kit.place(a["g"],x,y,w,h);Kit.moved_by_code(a["g"])
			self.update_zone(z)
		def keep(self,W,H):
			if(W,H)!=(self.W,self.H):
				self.W,self.H=W,H;self.zs.reflow(W,H,l())
				for z in self.zs.zones:self.place_zone(z)
				self.draw_marks()
		def gaps(self):
			W,H=self.W,self.H;c=[w.px for w in self.zs.zones if w.px is not None];a=[x for x in sorted(set([0,W]+[y[0]for y in c]+[z[0]+z[2]for z in c]))if 0<=x<=W];b=[G for G in sorted(set([0,H]+[a6[1]for a6 in c]+[a7[1]+a7[3]for a7 in c]))if 0<=G<=H];h,n=len(a)-1,len(b)-1;d={}
			for j in range(n):
				s=(b[j]+b[j+1])/2.
				for i in range(h):
					t=(a[i]+a[i+1])/2.
					if not any(a8[0]<=t<a8[0]+a8[2]and a8[1]<=s<a8[1]+a8[3]for a8 in c):d[(i,j)]=True
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
			if d==self.marks_sig and Kit.is_open(self.marks):return
			self.marks_sig=d;e,n=self.gaps();b=self.bad_overlaps();f=(n,len(b));l,self.marks=self.marks,None;Kit.dispose(l);i=[H for H in self.zs.zones if H.kind=="w"and H.px is not None and not H.solo];j=[z for W,a6 in enumerate(i)for a7 in i[W+1:]for z in(af(a6.px,a7.px),)if z is not None]
			if e or b or j:
				g=G.CreateGump(False,False)
				for(x,y,w,h)in e:Kit.add_box(g,x,y,w,h,.45,"#C83030")
				for a,c,(x,y,w,h)in b:Kit.add_box(g,x,y,w,h,.55,"#C83030")
				for o,m,p,a,c in j:k=(m+p)//2;Kit.add_box(g,*(((k-2,a,4,c-a)if o=="v"else(a,k-2,c-a,4))+(.9,"#E8C15A")))
				Grid.show_overlay(g,0,0,self.W,self.H);self.marks=g
			if f!=self.counts:self.counts=f;self.rebuild=True
		def _drop_handles(self):
			for g,a,r in self.handles:Kit.dispose(g)
			self.handles=[];self.handles_sig=None
		def _sync_handles(self):
			z=self.zs.by_id(self.sel)if self.sel else None;c=self.frames.get(z.id)if z is not None else None;d=(z.id,tuple(z.px),z.lock,c.get("g")if c else None)if z is not None and z.px is not None else None
			if d==self.handles_sig:return
			self._drop_handles();self.handles_sig=d
			if z is None or z.lock:return
			x,y,w,h=z.px;T=10;a=max(24,min(80,w//3));b=max(24,min(80,h//3))
			for e,r in(("l",(x,y+(h-b)//2,T,b)),("r",(x+w-T,y+(h-b)//2,T,b)),("t",(x+(w-a)//2,y+Kit.MARGIN+30,a,T)),("b",(x+(w-a)//2,y+h-T,a,T))):g=G.CreateGump(True,False);Kit.add_box(g,0,0,r[2],r[3],.9,"#E8C15A");Kit.catcher(g,0,0,r[2],r[3],lambda:None,"Drag to move this edge on the grid");g.SetRect(r[0],r[1],r[2],r[3]);Kit.add_front(g);SNAP.skip_gump(g);self.handles.append((g,e,r))
		def _edge_tick(self,pressed):
			b=time.time()
			if self.edge is None:
				if pressed and not self.pressed_was and self.handles:
					m=Kit.mouse_pos()
					if m is not None:
						for g,a,r in self.handles:
							if r[0]<=m[0]<r[0]+r[2]and r[1]<=m[1]<r[1]+r[3]:
								z=self.zs.by_id(self.sel)
								if z is not None:self.edge=(z.id,a,m,tuple(z.px))
								break
				return
			n,a,c,d=self.edge;z=self.zs.by_id(n);m=Kit.mouse_pos()
			if z is None or m is None:self.edge=None;Kit.dispose(self.edge_g);self.edge_g=None;return
			x,y,w,h=d;e,f=m[0]-c[0],m[1]-c[1]
			if a=="l":i=min(x+w-ZONE_MIN_W,max(0,x+e));x,w=i,w+(x-i)
			elif a=="r":w=max(ZONE_MIN_W,min(self.W-x,w+e))
			elif a=="t":j=min(y+h-ZONE_MIN_H,max(0,y+f));y,h=j,h+(y-j)
			else:h=max(ZONE_MIN_H,min(self.H-y,h+f))
			if pressed:
				if b-self.edge_at>=.05:
					self.edge_at=b;k=l();o,self.edge_g=self.edge_g,None;Kit.dispose(o);g=G.CreateGump(False,False)
					for p,q,s,u in((0,0,w,2),(0,h-2,w,2),(0,0,2,h),(w-2,0,2,h)):Kit.add_box(g,p,q,s,u,.95,"#E8C15A")
					t="%d x %d squares (%d x %d)"%(max(1,int(round(float(w)/k))),max(1,int(round(float(h)/k))),w,h);Kit.add_box(g,6,6,Kit.text_w(t)+12,22,.85,"#000000");Kit.add_label(g,t,12,8,Kit.HUE_TITLE);Grid.show_overlay(g,x,y,w,h);self.edge_g=g
				return
			self.edge=None;Kit.dispose(self.edge_g);self.edge_g=None
			if(x,y,w,h)!=d:self.landed_rect(z,x,y,w,h)
		def landed_rect(self,z,x,y,w,h):
			c=1 if z.free else l();d,e,a,b=[int(round(float(f)/c))*c for f in(x,y,x+w,y+h)];a,b=min(a,self.W),min(b,self.H)
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
		def _cap_w(cap):return 35+Kit.text_w(cap)
		def _flow(self,g,store,items,a,y,d):
			x=a
			for e,f,b,h in items:
				c=self._cap_w(b)
				if x>a and x+c>d:x=a;y+=self.ROW
				if g is not None:Kit.art_button(g,store,e,f,x,y-2,b,h)
				x+=c+16
			return y
		def build_bar(self):Binds.scoped("interface.editor",self.draw_bar)
		def draw_bar(self):
			r=self.bar;W=self.BAR_W;M,y=Kit.MARGIN,Kit.GAP;i=({},{});d={};g=G.CreateGump(True,True);e=W-2*M;k=M+e-12;z=self.zs.by_id(self.sel)if self.sel else None;L=self.layout;N=l();s=[];t=M+30+y;a=t+32;h=[]
			if z is None:h.append(("label","Click Add zone, then drag it into place.",M+12,a+3,Kit.HUE_INFO));a+=self.ROW
			else:
				A=M+12+Kit.text_w("Name:")+8;h.append(("label","Name:",M+12,a+3,None));h.append(("box","name",z.id,A,a,130,False,"Zone name, unique in this frame layout; Enter uses it"));f=[("kind",Kit.ART_PAGE,"Kind: "+z.kind_name(),"Switch kind: window, keep clear, reserved"),("stack",Kit.ART_PAGE,"Stack: "+z.stack_name(),"Switch the way windows stack in this zone"),("prio",Kit.ART_PAGE,"Shrinks: "+_ordinal(z.prio),"Change when this zone shrinks to minimized bars on a small screen"),("overlap",Kit.ART_PAGE,"Overlap: "+("on"if z.overlap else "off"),"Let this zone lie over others (on) or keep clear of them (off)"),("lock",Kit.ART_PAGE,"Lock: "+("on"if z.lock else "off"),"Lock the zone against moving and resizing, or unlock it"),("split",Kit.ART_PLAY,"Split","Cut this zone in two along its long side"),("join",Kit.ART_OK,"Join","Merge with a zone flush beside it of the same height or width"),("solo",Kit.ART_PAGE,"Apart: "+("on"if z.solo else "off"),"Keep this zone's panel apart from zones it touches (on) or join them (off)"),("free",Kit.ART_PAGE,"Snap: "+("off"if z.free else "on"),"Snap this zone to the grid and its neighbours (on) or place it to the pixel (off)"),("dup",Kit.ART_OK,"Duplicate","Add a copy of this zone beside it"),("remove",Kit.ART_CLOSE,"Remove","Remove this zone (or Delete twice); its windows become free")];s.append(("flow",f,A+130+16,a));a=self._flow(None,None,f,A+130+16,a,k)+self.ROW;m=M+12;O="px"if self.px_mode else "squares"
				for c,P,o in(("col","X:"if self.px_mode else "Col:","Left edge in %s from the screen's left"),("row","Y:"if self.px_mode else "Row:","Top edge in %s from the screen's top"),("w","W:","Width in %s"),("h","H:","Height in %s")):
					B=(self.W if c in("col","w")else self.H)
					if not self.px_mode:B=(B+N-1)//N
					h.append(("label",P,m,a+3,None));m+=Kit.text_w(P)+6;h.append(("box",c,"",m,a,self.FIELD_W,True,(o%O)+" (%d-%d); Enter or Apply uses it, Esc puts it back"%(0 if c in("col","row")else 1,B)));m+=self.FIELD_W+14
				f=[("apply",Kit.ART_OK,"Apply","Use the typed values (Enter does too)"),("units",Kit.ART_PAGE,"Units: "+O,"Switch between grid squares and pixels")];s.append(("flow",f,m+4,a));a=self._flow(None,None,f,m+4,a,k)+self.ROW;d["px_y"]=a+3;h.append(("px",M+12,a+3));a+=20;ae=", ".join(a7 for a6,a7 in(("L","left"),("T","top"),("R","right"),("B","bottom"),("X","centre"),("Y","middle"))if a6 in z.pins);h.append(("pins","Pinned: "+(ae or "none"),M+12,a+3));a+=28;f=[("even",Kit.ART_PLAY,"Even out","Give this zone and those flush beside it in its row (or column) equal sizes")]
				if len(self.multi)>=2:f+=[("al_"+a8[0],Kit.ART_PLAY,"Align "+a8,"Line the picked zones' %s edges up with this zone's"%a8)for a8 in("left","top","right","bottom")];f.append(("same",Kit.ART_PLAY,"Same size","Make the picked zones this zone's size"))
				s.append(("flow",f,M+12,a));a=self._flow(None,None,f,M+12,a,k)+self.ROW
				if len(self.multi)>=2:h.append(("label",Kit.fit("%d zones picked (Shift+click picks more or fewer)."%len(self.multi),e-24),M+12,a+3,Kit.HUE_INFO));a+=20
			Q=a-t+6;u=t+Q+y;n=[];j=0
			if z is not None and z.kind=="w":
				n=list(L.assign.get(self.orig_id(z.id),[]));j=30+28+26*len(n)+(20 if self.preview else 0)+14
				if not n:j+=20
			C=u+(j+y if j else 0);v=ratio_class(self.W,self.H);R=[a9 for a9 in("narrow","wide","ultrawide")if a9!=v];D=[("undo",Kit.ART_PAGE,"Undo","Undo the last change (Ctrl+Z)"),("redo",Kit.ART_PAGE,"Redo","Redo the last undo (Ctrl+Y)"),("from_default",Kit.ART_PLAY,"New from Default","Start again from the Default layout"),("mirror",Kit.ART_PLAY,"Mirror","Swap the zones left and right"),("copyto",Kit.ART_OK,"Copy to others","Use these zones on %s and %s screens too (save them first)"%tuple(R))]
			if self.others is None or self.others[0]!=(self.zs.name,v):af=FRAMES_NAMED%self.zs.name;self.others=((self.zs.name,v),[ba for ba in R if Kit.get_var(af+"@"+ba,"")])
			w=self.others[1]
			if w:D.append(("reflow",Kit.ART_PLAY,"Reflow from: "+w[0],"Rebuild from this layout's %s-screen version"%w[0]));d["reflow_from"]=w[0]
			ag=self._flow(None,None,D,M+12,0,k);S=30+28*2+ag+20*3+10;H=C+S+M;Kit.add_window_frame(g,W,H);Kit.add_section(g,M,M,e,30);Kit.add_label(g,"ZONES",M+30,M+7,Kit.HUE_TITLE);Kit.add_label(g,Kit.fit('frame layout "%s"'%self.zs.name,e-250),M+30+Kit.text_w("ZONES")+12,M+7,Kit.HUE_INFO);Kit.art_button(g,i,"close",Kit.ART_CLOSE,W-M-54,M+4,None,"Close the editor and bring back the saved zones");Kit.add_section(g,M,t,e,Q,"ZONE  (selected)");T=[]
			for b in h:
				if b[0]=="label":Kit.add_label(g,b[1],b[2],b[3],b[4])
				elif b[0]=="box":c,ah,E,by,ai,aj,o=b[1:];d[c]=Kit.with_tip(Kit.add_textbox(g,ah,E,by,ai,numbers=aj),o);T.append(c)
				elif b[0]=="px":d["px"]=Kit.add_label(g,"",b[1],b[2],Kit.HUE_INFO);d["px_x"]=b[1]
				elif b[0]=="pins":Kit.with_tip(Kit.add_label(g,b[1],b[2],b[3],Kit.HUE_INFO),"Edges kept on the screen's edge (or centre line) on other screen sizes")
			for F in s:self._flow(g,i,F[1],F[2],F[3],k)
			if j:
				Kit.add_section(g,M,u,e,j,"WINDOWS  (in this zone, top to bottom)");a=u+32;Kit.add_label(g,"Window:",M+12,a+3);U=M+12+Kit.text_w("Window:")+8;V=300;E=U+V+16;Kit.art_button(g,i,"w_add",Kit.ART_OK,E,a-2,"Put it here","Put the picked window in this zone (no Arrange mode needed)");a+=28
				if not n:Kit.add_label(g,"Pick a window above, then click Put it here.",M+12,a+3,Kit.HUE_INFO);a+=20
				for ak,p in enumerate(n):Kit.add_label(g,Kit.fit(L.title_of(p),300),M+12,a+3);self._flow(g,i,[("w_%s_%d"%(bb,ak),bc,bd,be%L.title_of(p))for bb,bc,bd,be in(("up",Kit.ART_PAGE,"Up","Move %s up the zone's stack"),("down",Kit.ART_PAGE,"Down","Move %s down the zone's stack"),("out",Kit.ART_CLOSE,"Take out","Free %s from the zone (it stays where it is)"))],M+12+310,a,1<<30);a+=26
				d["wins_rows"]=n
				if self.preview:Kit.add_label(g,Kit.fit(self.preview.lstrip("!"),e-24),M+12,a+3,Kit.HUE_BAD if self.preview.startswith("!")else Kit.HUE_INFO)
			Kit.add_section(g,M,C,e,S,"FRAME LAYOUT");a=C+32;x=M+12
			for c,al,q,o in(("add",Kit.ART_OK,"Add zone","Add a zone mid-screen to drag into place"),("fill",Kit.ART_PLAY,"Fill the gaps","Grow every zone into empty room beside it"),("save",Kit.ART_OK,"Save","Save as the frame layout in use (Default saves as Default (mine))"),("saveas",Kit.ART_OK,"Save as","Save under the name in the box")):Kit.art_button(g,i,c,al,x,a-2,q,o);x+=self._cap_w(q)+16
			d["saveas"]=Kit.with_tip(Kit.add_textbox(g,self.saveas_text,x,a,max(60,W-M-12-self._cap_w("Discard")-16-x),numbers=False),"A name for Save as (letters, digits, spaces)");q="Discard";Kit.art_button(g,i,"discard",Kit.ART_CLOSE,W-M-12-self._cap_w(q),a-2,q,"Close the editor and bring back the saved zones");a+=28;a=self._flow(g,i,D,M+12,a,k)+28;am=len(self.zs.zones);nk=sum(1 for bf in self.zs.zones if bf.kind=="k");nr=sum(1 for bg in self.zs.zones if bg.kind=="r");X,Y=self.counts;an="%s, %d keep clear, %d reserved; %s, %s; %d x %d, %s"%(Kit.count(am,"zone"),nk,nr,Kit.count(X,"gap"),Kit.count(Y,"overlap"),self.W,self.H,v);Kit.add_label(g,Kit.fit(an,e-24),M+12,a+3,Kit.HUE_BAD if(X or Y)else Kit.HUE_INFO);a+=20;I=M+12
			for ao,Z in((ZONE_COLORS["w"],"window"),(ZONE_COLORS["k"],"keep clear"),(ZONE_COLORS["r"],"reserved"),("#C83030","gap or overlap"),("#E8C15A","overlap allowed")):Kit.add_box(g,I,a+6,12,12,.9,ao);Kit.add_label(g,Z,I+16,a+3,Kit.HUE_INFO);I+=16+Kit.text_w(Z)+14
			a+=20;Kit.add_label(g,Kit.fit("Mouse on the zone: arrows nudge it a square; Shift+arrows resize it; Delete twice removes it.",e-24),M+12,a+3,Kit.HUE_INFO)
			if j:
				wl=L.all_windows();J=["(pick a window)"];self.pick_keys=[None]
				for p,ap in wl:ab=L.zone_of(p);J.append(Kit.fit(ap+(' (in "%s")'%ab if ab else ""),290));self.pick_keys.append(p)
				if self.pick>=len(J):self.pick=0
				K=G.CreateDropDown(V,J,self.pick);K.SetPos(U,u+32);g.Add(K);d["w_pick"]=Kit.with_tip(K,"A window for this zone; the zone shows where it would sit")
			ax,ay=Kit.anchor_pos("B",W,H)
			if Kit.is_open(r):x,ac=r.GetX(),r.GetY()
			else:x,ac=self.bar_pos or Kit.load_pos(aa,(ax or 200,ay or 200),(W,H))
			Kit.place(g,x,ac,W,H);Kit.add_front(g);Kit.on_moved(g,self._bar_moved);self.bar,self.store,self.c=g,i,d;self.raws={}
			for c in T+["saveas"]:
				ad=Kit.client_control(d[c])if c in d else None
				if ad is not None:self.raws[c]=ad
			self.fields=None;self.focus_was=None;self.show_fields();Kit.dispose(r)
		def _bar_moved(self):Kit.save_pos(aa,self.bar);self.bar_pos=Snap.pos(self.bar)
		def _values(self,z):
			x,y,w,h=z.px
			if self.px_mode:return tuple(str(b)for b in(x,y,w,h))
			a=l();return tuple(str(c)for c in(int(round(float(x)/a)),int(round(float(y)/a)),max(1,int(round(float(w)/a))),max(1,int(round(float(h)/a)))))
		def show_fields(self):
			c=self.c;z=self.zs.by_id(self.sel)if self.sel else None
			if z is None or "col"not in c:return
			b=self._values(z)
			if b!=self.fields:
				self.fields=b
				for e,t in zip(self.FIELDS,b):c[e].SetText(t)
			x,y,w,h=z.px
			if self.px_mode:a=l();d="%d x %d squares at square %d, %d"%(max(1,int(round(float(w)/a))),max(1,int(round(float(h)/a))),int(round(float(x)/a)),int(round(float(y)/a)))
			else:d="%d x %d px at %d, %d"%(w,h,x,y)
			Kit.set_text(c["px"],Kit.fit(d,self.BAR_W-Kit.MARGIN-12-c["px_x"]))
		def _over(self,z):
			m=Kit.mouse_pos()
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
			if not Kit.is_open(self.bar):self.close(keep=False);return
			p=time.time()
			for f,b in list(self.frames.items()):
				z=self.zs.by_id(f);i=b.get("g")
				if z is None or not Kit.is_open(i):continue
				if b["resize_at"]:
					r=Snap.rect(i)
					if r is not None and(r[2],r[3])!=b["size"]:j=l();Kit.set_text(b["sum"],Kit.fit("%d x %d squares"%(max(1,int(round(float(r[2])/j))),max(1,int(round(float(r[3])/j)))),max(40,r[2]-2*Kit.MARGIN-24)),Kit.HUE_TITLE)
					if p-b["resize_at"]>=self.SETTLE:
						b["resize_at"]=0.
						if r is not None and(r[2],r[3])!=b["size"]:
							if z.lock:self.build_zone(z)
							else:self.landed(z,r[0],r[1],r[2],r[3],resized=True)
			k=SNAP.pressed()is True;self._sync_handles();self._edge_tick(k);self.pressed_was=k;a,c=self.store,self.c;z=self.zs.by_id(self.sel)if self.sel else None
			if Kit.was_clicked(a,"close")or Kit.was_clicked(a,"discard"):self.close(keep=False);return
			m=self._focus();q=Client.typing();s=self._key("enter");t=self._key("esc")
			if not q and not self.edge:
				n=bool(P("ctrl"));u=bool(P("shift"))
				if self._key("z")and n:self.do_undo()
				elif self._key("y")and n:self.do_redo()
				elif z is not None:
					for d,g in(("left",(-1,0)),("right",(1,0)),("up",(0,-1)),("down",(0,1))):
						if self._key(d)and self._over(z):self.nudge(z,g,u)
					if self._key("delete"):self.delete_pressed(z)
			if Kit.was_clicked(a,"add"):
				self.push();f=self.zs.new_id();o=Zone(f,"w",(0,0,1,1),"",(0,0),"d",0);o.set_px((self.W-320)//2,(self.H-240)//2,320,240,self.W,self.H)
				if not self._add_zone(o,True,"no room for another zone; remove one or make one smaller."):return
			elif Kit.was_clicked(a,"undo"):self.do_undo()
			elif Kit.was_clicked(a,"redo"):self.do_redo()
			elif Kit.was_clicked(a,"even")and z is not None:
				self.push();v=self.zs.even_out(z,self.W,self.H,l())
				if v<2:self.undo.pop();self.say("no zone sits flush beside this one in its row or column.")
				else:self._all_moved()
			elif Kit.was_clicked(a,"fill"):self.push();self.zs.fill_gaps(self.W,self.H,l());self._all_moved()
			elif Kit.was_clicked(a,"save"):self.save(self.zs.name if self.zs.name!=LAYOUT_DEFAULT else LAYOUT_MINE);return
			elif Kit.was_clicked(a,"saveas"):
				d=Layout.clean_name(safe(lambda:c["saveas"].Text,""),"")
				if not d:self.say("type a name in the box, then click Save as.")
				else:self.save(d if d!=LAYOUT_DEFAULT else LAYOUT_MINE);return
			elif Kit.was_clicked(a,"reflow")and c.get("reflow_from"):
				h=ZoneSet.parse(self.zs.name,Kit.get_var((FRAMES_NAMED%self.zs.name)+"@"+c["reflow_from"],""))
				if h is not None:h.reflow(self.W,self.H,l());self.push();self._restore(([G.copy()for G in h.zones],self.sel,{}));self.changed()
			elif Kit.was_clicked(a,"from_default"):self.push();g=ZoneSet.default(self.W,self.H,(),False);self._restore(([H.copy()for H in g.zones],self.sel,{}));self.changed()
			elif Kit.was_clicked(a,"mirror"):
				self.push()
				for e in self.zs.zones:x,y,w,A=e.px;e.set_px(self.W-x-w,y,w,A,self.W,self.H)
				self._all_moved()
			elif Kit.was_clicked(a,"copyto"):self.copy_to()
			elif Kit.was_clicked(a,"units"):self.commit_rect(z,quiet=True)if z is not None else None;self.px_mode=not self.px_mode;self.rebuild=True
			if z is not None and not self.rebuild:self.poll_zone(z,a)
			if z is not None and z.kind=="w"and not self.rebuild:self.poll_windows(z,a,c)
			if not self.rebuild:self.poll_fields(z,m,s,t,Kit.was_clicked(a,"apply"))
			self.focus_was=m;self.draw_marks()
			if self.rebuild:
				self.rebuild=False;self.saveas_text=str(safe(lambda:c["saveas"].Text,self.saveas_text)or "")
				for e in self.zs.zones:self.update_zone(e)
				self.build_bar()
		def _all_moved(self):
			for a in self.zs.zones:a.note_pins(self.W,self.H);self.place_zone(a)
			self.changed()
		def poll_zone(self,z,store):
			if Kit.was_clicked(store,"kind"):self.push();a=[f for f,g in ZONE_KINDS];z.kind=a[(a.index(z.kind)+1)%len(a)];z.hug=z.hug and z.kind=="w";self.build_zone(z);self.changed();self.rebuild=True
			elif Kit.was_clicked(store,"stack"):self.push();b=[h for h,i in ZONE_STACKS];z.stack=b[(b.index(z.stack)+1)%len(b)];self.build_zone(z);self.rebuild=True
			elif Kit.was_clicked(store,"prio"):self.push();z.prio=(z.prio+1)%(SHRINK_MAX+1);self.rebuild=True
			elif Kit.was_clicked(store,"overlap"):
				self.push();z.overlap=not z.overlap
				if not z.overlap:
					if not self.zs.push_clear(z,self.W,self.H,l()):o=self._blocker(z);self.say('zone "%s" still lies over "%s"; move it or make it smaller.'%(z.id,o.id if o is not None else "a zone"),Kit.HUE_INFO)
					z.note_pins(self.W,self.H)
				for c in self.zs.zones:self.build_zone(c)
				self.changed();self.rebuild=True
			elif Kit.was_clicked(store,"lock"):self.push();z.lock=not z.lock;self.build_zone(z);self.rebuild=True
			elif Kit.was_clicked(store,"split"):self.split(z)
			elif Kit.was_clicked(store,"join"):self.join(z)
			elif Kit.was_clicked(store,"solo"):self.push();z.solo=not z.solo;self.changed();self.rebuild=True
			elif Kit.was_clicked(store,"free"):self.push();z.free=not z.free;self.px_mode=self.px_mode or z.free;z.note_pins(self.W,self.H);self.changed();self.rebuild=True
			elif Kit.was_clicked(store,"dup"):self.duplicate(z)
			elif Kit.was_clicked(store,"remove"):self.remove(z)
			else:
				for d,e in(("al_l","l"),("al_t","t"),("al_r","r"),("al_b","b"),("same","s")):
					if Kit.was_clicked(store,d):self.align(z,e);break
		def poll_windows(self,z,store,c):
			L=self.layout;g=c.get("w_pick");e=time.time();h=Kit.was_clicked(store,"w_add")
			if g is not None and(e>=self._pick_next or e-HOST.input_at<=HOST.INPUT_FAST):
				self._pick_next=e+.2;i=Kit.dd_index(g,self.pick)
				if i!=self.pick:
					self.pick=i;a=self.pick_keys[i]if 0<i<len(self.pick_keys)else None;self.preview=self.preview_text(a,z)if a else "";self.build_zone(z);self.rebuild=True
					if not h:return
			d=self.orig_id(z.id)
			if h:
				a=self.pick_keys[self.pick]if 0<self.pick<len(self.pick_keys)else None
				if a is None:self.say("pick a window in the list first, then click Put it here.",Kit.HUE_INFO);return
				if L.frames is None or L.frames.by_id(d)is None:self.say('zone "%s" isn\'t saved yet; click Save, then put the window in it.'%z.id);return
				if L.zone_of(a)==d:self.say("%s already sits in this zone."%L.title_of(a),Kit.HUE_INFO);return
				l=L._map_zone()
				if(a!="worldmap"and d==l)or(a=="worldmap"and L.assign.get(d)):self.say("TazUO's World Map keeps its zone to itself; pick another zone for %s."%(L.title_of(a)if a!="worldmap"else "it"));return
				if L._too_small(a,L.frames.by_id(d)):return
				L.assign_to(a,d);self.pick,self.preview=0,"";self.build_zone(z);self.rebuild=True;return
			m=c.get("wins_rows")or[]
			for i,k in enumerate(m):
				for f in("up","down","out"):
					if not Kit.was_clicked(store,"w_%s_%d"%(f,i)):continue
					b=L.assign.get(d,[])
					if k not in b:break
					if f=="out":L.assign_to(k,None)
					else:
						j=b.index(k);t=j-1 if f=="up"else j+1
						if 0<=t<len(b):
							b[j],b[t]=b[t],b[j]
							for n in b:L._refit(n)
							L.save_assign();L.dirty=L.fresh=True;I()
					self.build_zone(z);self.rebuild=True;return
		def preview_text(self,key,z):return self.layout.preview_text(key,z,self.layout.assign.get(self.orig_id(z.id),[]))
		def poll_fields(self,z,focus,enter,esc,apply):
			c=self.c
			if z is None or "name"not in c:return
			b=self.focus_was if(self.focus_was is not None and focus!=self.focus_was)else None
			if esc and(focus is not None or self._edited(z)):self._refields();c["name"].SetText(z.id);return
			if(enter and focus=="name")or b=="name"or apply:
				a=str(safe(lambda:c["name"].Text,z.id)or "").strip()
				if a!=z.id:self.rename(z,a);return
			if focus is None and b is None and enter and not self.raws_ok:
				a=str(safe(lambda:c["name"].Text,z.id)or "").strip()
				if a!=z.id:self.rename(z,a);return
				self.commit_rect(z);return
			if((enter and focus in self.FIELDS)or(b in self.FIELDS and focus not in self.FIELDS)or apply):self.commit_rect(z)
		def _edited(self,z):a=self._box_texts();b=str(safe(lambda:self.c["name"].Text,z.id)or "").strip();return(a is not None and a!=self._values(z))or b!=z.id
		def commit_rect(self,z,quiet=False):
			a=self._box_texts()
			if a is None or a==self._values(z):return
			try:d,e,w,h=[int(f)for f in a]
			except Exception:
				if not quiet:self.say("type whole numbers in Col, Row, W and H.")
				self._refields();return
			b=1 if self.px_mode else l();x,y=max(0,d)*b,max(0,e)*b;w,h=max(1,w)*b,max(1,h)*b;c="%d x %d %s"%(max(1,int(a[2])),max(1,int(a[3])),"px"if self.px_mode else "squares")
			if w<ZONE_MIN_W or h<ZONE_MIN_H:
				if not quiet:self.say('zone "%s" can\'t be %s: the smallest zone is %d x %d px.'%(z.id,c,ZONE_MIN_W,ZONE_MIN_H))
				self._refields();return
			if z.lock:self.say('zone "%s" is locked; click Lock to change it.'%z.id,Kit.HUE_INFO);self._refields();return
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
		def nudge(self,z,d,resize):
			if z.lock:self.say('zone "%s" is locked; click Lock to change it.'%z.id,Kit.HUE_INFO);return
			a=1 if z.free else l();x,y,w,h=z.px
			if resize:self.apply_rect(z,x,y,max(ZONE_MIN_W,w+d[0]*a),max(ZONE_MIN_H,h+d[1]*a))
			else:self.apply_rect(z,x+d[0]*a,y+d[1]*a,w,h)
		def delete_pressed(self,z):
			a=time.time()
			if(self.del_armed is not None and self.del_armed[0]==z.id and a-self.del_armed[1]<=3.):self.del_armed=None;self.remove(z);return
			self.del_armed=(z.id,a);Kit.say('press Delete again to remove zone "%s".'%z.id,Kit.HUE_INFO)
		def remove(self,z):
			if z.lock:self.say('zone "%s" is locked; click Lock to remove it.'%z.id,Kit.HUE_INFO);return
			self.push();self.zs.zones=[b for b in self.zs.zones if b is not z];a=self.frames.pop(z.id,None)
			if a is not None:Kit.dispose(a.get("g"))
			self.multi.discard(z.id);self.sel=self.zs.zones[0].id if self.zs.zones else None;self.changed();self.rebuild=True
		def split(self,z):
			if z.lock:self.say('zone "%s" is locked; click Lock to change it.'%z.id,Kit.HUE_INFO);return
			x,y,w,h=z.px;e=w>=h;c=w if e else h;d=ZONE_MIN_W if e else ZONE_MIN_H;f=l();a=int(round(c/2./f))*f
			if not d<=a<=c-d:a=c//2
			if a<d or c-a<d:self.say('zone "%s" is too small to split.'%z.id);return
			self.push();b=z.copy();b.id=self.zs.new_id();W,H=self.W,self.H
			if e:z.set_px(x,y,a,h,W,H);b.set_px(x+a,y,w-a,h,W,H)
			else:z.set_px(x,y,w,a,W,H);b.set_px(x,y+a,w,h-a,W,H)
			z.note_pins(W,H);b.note_pins(W,H);self.zs.zones.append(b);self.build_zone(z);self.build_zone(b);self.changed();self.rebuild=True
		def join(self,z):
			if z.lock:self.say('zone "%s" is locked; click Lock to change it.'%z.id,Kit.HUE_INFO);return
			x,y,w,h=z.px;D=SNAP_DIST;a=None
			for o in self.zs.zones:
				if o is z or o.px is None or o.lock or o.kind!=z.kind:continue
				b,c,d,e=o.px
				if abs(c-y)<=D and abs(e-h)<=D and(abs(b-(x+w))<=D or abs(x-(b+d))<=D):a=o
				elif abs(b-x)<=D and abs(d-w)<=D and(abs(c-(y+h))<=D or abs(y-(c+e))<=D):a=o
				if a is not None:break
			if a is None:self.say('no zone of the same height or width sits flush beside "%s".'%z.id);return
			self.push();b,c,d,e=a.px;f,g=min(x,b),min(y,c);z.set_px(f,g,max(x+w,b+d)-f,max(y+h,c+e)-g,self.W,self.H);z.note_pins(self.W,self.H);self.zs.zones=[r for r in self.zs.zones if r is not a];i=self.frames.pop(a.id,None)
			if i is not None:Kit.dispose(i.get("g"))
			self.multi.discard(a.id);self.build_zone(z);self.changed();self.rebuild=True;self.say('zone "%s" joined into "%s"; its windows become free when saved.'%(a.id,z.id),Kit.HUE_INFO)
		def _add_zone(self,a,check,text):
			self.zs.zones.append(a)
			if check and not self.zs.push_clear(a,self.W,self.H,l()):self.zs.zones.remove(a);self.undo.pop();self.say(text);return False
			a.note_pins(self.W,self.H);self.sel,self.multi=a.id,set();self.build_zone(a);self.changed();self.rebuild=True;return True
		def duplicate(self,z):self.push();a=z.copy();a.id=self.zs.new_id();a.lock=False;b=l();x,y,w,h=z.px;a.set_px(x+b,y+b,w,h,self.W,self.H);self._add_zone(a,not a.overlap,"no room for a copy of zone \"%s\"; make room first."%z.id)
		def align(self,z,edge):
			g=[G for G in[self.zs.by_id(H)for H in self.multi if H!=z.id]if G is not None and not G.lock]
			if not g:return
			self.push();x,y,w,h=z.px;a=[]
			for p in g:
				e,f,b,c=p.px;r={"l":(x,f,b,c),"t":(e,y,b,c),"r":(x+w-b,f,b,c),"b":(e,y+h-c,b,c)}.get(edge,(e,f,w,h));d=p.px;p.set_px(r[0],r[1],r[2],r[3],self.W,self.H)
				if self._blocker(p)is not None:p.set_px(d[0],d[1],d[2],d[3],self.W,self.H);a.append(p.id)
				p.note_pins(self.W,self.H)
			if a:self.say("%s would cover another zone, so %s stayed where %s %s."%(", ".join('"%s"'%i for i in a),"it"if len(a)==1 else "they","it"if len(a)==1 else "they","was"if len(a)==1 else "were"),Kit.HUE_INFO)
			self._all_moved()
		def copy_to(self):
			a=self.zs.name;self.others=None
			if self.zs.generated or a==LAYOUT_DEFAULT or a not in self.layout.frame_names():self.say("save these zones first (Save or Save as), then click Copy to.",Kit.HUE_INFO);return
			d=ratio_class(self.W,self.H);b=self.zs.copy(a);b.screen=(self.W,self.H);b.grid=l()
			for e in b.zones:e.note_pins(self.W,self.H)
			f=b.save_text();c=[g for g in("narrow","wide","ultrawide")if g!=d]
			for k in c:Kit.put_var((FRAMES_NAMED%a)+"@"+k,f)
			Kit.say('frame layout "%s" copied to %s screens.'%(a," and ".join(c)),Kit.HUE_GOOD)
		def warnings(self):
			a=[];L=self.layout
			for z in self.zs.zones:
				if z.kind!="w"or z.px is None:continue
				for k in L.assign.get(self.orig_id(z.id),[]):
					b=L._min_of(k)
					if b and(z.px[2]<b[0]or z.px[3]<b[1]):a.append('zone "%s" is %d x %d, smaller than %s can be (%d x %d)'%(z.id,z.px[2],z.px[3],L.title_of(k),b[0],b[1]))
			c,d=self.counts
			if c:a.append("the zones leave %s (Fill the gaps closes them)"%Kit.count(c,"gap"))
			if d:a.append("%s of zones without Overlap on"%Kit.count(d,"overlap"))
			if not any(f.kind=="k"for f in self.zs.zones):a.append("no keep-clear zone: nothing marks the game view")
			return a
		def save(self,name):
			self.others=None
			for w in self.warnings():Kit.say("note: %s."%w,Kit.HUE_INFO)
			a=self.zs.copy(name);a.generated=False;a.ver=2;self.layout.save_frames(a,name,self.W,self.H);L,d=self.layout,False
			for b,c in self.renames.items():
				if b!=c and b in L.assign and c not in L.assign:L.assign[c]=L.assign.pop(b);d=True
			if d:L.save_assign()
			Kit.say('frame layout "%s" saved.'%name,Kit.HUE_GOOD);self.close(keep=True);self.layout.use_frames(name,tell=False)
	def az():e["editor"]=None
	def ag(fresh=False):
		L=LAYOUT;W,H=Kit.screen()
		if e["editor"]is not None or W<=0 or H<=0 or not L.enabled:return
		if fresh:
			c=L.frame_names();n,b=2,"Mine"
			while b in c or b==LAYOUT_DEFAULT:b="Mine %d"%n;n+=1
			a=ZoneSet(b,[],l(),(W,H));z=Zone("Zone 1","w",(0,0,1,1),"",(0,0),"d",0);z.set_px((W-320)//2,(H-240)//2,320,240,W,H);a.zones.append(z)
		elif L.frames_name==LAYOUT_DEFAULT:a=ZoneSet.default(W,H,L.occupied(),False);a.generated=False
		else:a=L.load_frames(L.frames_name,W,H)or L.frames_in_use(W,H).copy()
		e["editor"]=LayoutEditor(L,a,az);e["editor"].open()
	def aA():
		L=LAYOUT;b=L.frames
		if b is None or not(L.seamless and L.enabled)or e["editor"]is not None:return(),None
		a=Layout._game_px(b)
		def c(r):return a is None or not(r[0]<a[0]+a[2]and a[0]<r[0]+r[2]and r[1]<a[1]+a[3]and a[1]<r[1]+r[3])
		d=tuple((tuple(f.px),f.solo)for f in b.zones if f.kind!="k"and f.px is not None and c(f.px));return d,a if L.fit_view else None
	def aB(items,q,W,H):
		l=G.CreateGump(False,False);s=Kit.WINDOW_BG;P=[Kit.pic_size(s+a6)for a6 in range(9)];g=[a7[0]for a7 in items];t=[{"T":[],"B":[],"L":[],"R":[]}for a8 in g]
		def z(x,y,w,h):
			Kit.add_tiled(l,s+4,x,y,w,h);b=Kit.add_box(l,x,y,w,h,.01,"#000000")
			if b is not None:b.SetAcceptMouseInput(True)
		for e,f,c,d in g:z(e,f,c,d)
		for i in range(len(g)):
			for n in range(i+1,len(g)):
				A=None if items[i][1]or items[n][1]else af(g[i],g[n])
				if A is None:continue
				r,o,u,j,k=A;B=0 if r=="v"else 1;D,E=(i,n)if g[i][B]<g[n][B]else(n,i);t[D]["R"if r=="v"else "B"].append((j,k));t[E]["L"if r=="v"else "T"].append((j,k))
				if u>o:z(*((o,j,u-o,k-j)if r=="v"else(j,o,k-j,u-o)))
		for i,(e,f,c,d)in enumerate(g):
			for F,I,J,M,N in(("T",1,e,e+c,lambda a,b:(a,f,b-a,P[1][1])),("B",7,e,e+c,lambda a,b:(a,f+d-P[7][1],b-a,P[7][1])),("L",3,f,f+d,lambda a,b:(e,a,P[3][0],b-a)),("R",5,f,f+d,lambda a,b:(e+c-P[5][0],a,P[5][0],b-a))):
				for j,k in ay(J,M,t[i][F]):Kit.add_tiled(l,s+I,*N(j,k))
		Grid.show_overlay(l,0,0,W,H,True);p["g"]=l
		if q is None or q[2]<=2*m or q[3]<=2*m:return
		v=G.CreateGump(False,False);e,f,c,d=q
		for O,Q,R,S,T in((0,0,c,m,K),(0,d-m,c,m,K),(0,0,m,d,K),(c-m,0,m,d,K),(m,m,c-2*m,1,L),(m,d-m-1,c-2*m,1,L),(m,m,1,d-2*m,L),(c-m-1,m,1,d-2*m,L)):Kit.add_box(v,O,Q,R,S,1.,T)
		Grid.show_overlay(v,e,f,c,d);C["g"]=v
	def aC():
		b=Kit._raw_gump(p["g"])if p["g"]is not None and not n["off"]else None
		if b is None or not Client.on_client_thread():return
		try:
			a=n["gumps"]
			if a is None:import System;t=Tz.T("ClassicUO.Game.Managers.UIManager");n["same"]=System.Object.ReferenceEquals;n["ver"]=t.GetField("_gumpsStructureVersion",Client.flags(static=True,public=False));a=n["gumps"]=Tz.get(None,"Gumps",t)
			d=n["ver"];c=int(d.GetValue(None))if d is not None else None
			if c is not None and c==n["seen"]and b is n["raw"]:return
			n["seen"],n["raw"]=c,b;e=a.Last;g=n["same"]
			if e is None or g(e.Value,b)or(e.Previous is not None and g(e.Previous.Value,b)):return
			f=a.Find(b)
			if f is None:return
			a.Remove(f);a.AddBefore(a.Last,f)
			if d is not None:d.SetValue(None,c+1);n["seen"]=c+1
		except Exception:n["off"]=True
	def aD(now):
		if now<e["back_at"]:return
		e["back_at"]=now+av;W,H=Kit.screen();a,b=aA();c=(W,H,a,b,Kit.look())
		if c==e["back_sig"]and(not a or(Kit.is_open(p["g"])and(b is None or Kit.is_open(C["g"])))):return
		e["back_sig"]=c;d,p["g"]=p["g"],None;f,C["g"]=C["g"],None
		if a and W>0 and H>0:aB(a,b,W,H)
		Kit.dispose(d);Kit.dispose(f)
	def aE(key):
		for a,b in aw:
			if key==a or(a.endswith(".")and key.startswith(a)):return b
		return
	def ah(total,b):
		c,a=[],0
		for i,d in enumerate(b):n=total-a if i==len(b)-1 else int(round(total*d));c.append((a,n));a+=n
		return c
	def aF(i,W,H):
		t=int(_clampv(STRIP_SHARE*H,TOP_MIN,TOP_MAX));c=int(_clampv(STRIP_SHARE*H,BOT_MIN,BOT_MAX))
		if i==2:d=int(_clampv(.3*H,200,340));b=[("Frames","w",0,0,W,t,"r","frames"),("Game","k",0,t,W,H-t-d,"d",None)];e=(("Paperdoll","gear"),("Bags","bag"),("Action bar","bar"),("Trackers","watch"),("Map","map"));b+=[(a6,"w",r,H-d,G,d,"d",a7)for(r,G),(a6,a7)in zip(ah(W,(.18,.18,.28,.18,.18)),e)]
		else:a=int(_clampv(.24*W,260,460))if i==3 else int(_clampv(SIDE_SHARE*W,SIDE_MIN,SIDE_MAX));m,f=(W-a,0)if i==3 else(0,a);b=[("Game","k",f,0,W-a,H-c,"d",None),("Action bar","w",f,H-c,W-a,c,"r","bar")];e=(("Frames","frames"),("Paperdoll","gear"),("Bags","bag"),("Trackers","watch"));b+=[(ba,"w",m,a8,a,a9,"d",bb)for(a8,a9),(ba,bb)in zip(ah(H,(.22,.26,.26,.26)),e)]
		g=ZoneSet(A[i][0],[],l(),(W,H));h={}
		for j,n,x,y,w,o,p,k in b:
			z=Zone(j,n,(0,0,1,1),"",(0,0),p,0);z.set_px(x,y,w,o,W,H);z.note_pins(W,H);g.zones.append(z)
			if k:h[k]=j
		return g,h
	def ai(i,W,H):
		L=LAYOUT;b=L.parse_windows(WINDOWS_DEFAULT)[1]
		if i<2:a=b if i==0 else L.parse_windows(WINDOWS_MIRRORED)[1];e=set(h for h,r in a.items()if any(L.gump_of(w)is not None for w in r));return ZoneSet.default(W,H,e,k["look"].get("game",True)),LAYOUT_DEFAULT,a
		f,g=aF(i,W,H);a={}
		for c in sorted(set(L.wins)|set(y for x in b.values()for y in x)):
			d=g.get(aE(c))
			if d:a.setdefault(d,[]).append(c)
		return f,A[i][0],a
	def aG(i,W,H):
		b=(i,W,H,k["look"].get("game",True));a=k["cards"].get(b)
		if a is None:a=k["cards"][b]=ai(i,W,H)[0]
		return a
	def S(key):
		for a,b in k["assign"].items():
			if key in b:return a
		return
	def T():
		d,t["g"]=t["g"],None;Kit.dispose(d);b=k["zs"];W,H=Kit.screen();L=LAYOUT
		if b is None or W<=0 or H<=0:return
		g=G.CreateGump(False,False)
		for z in b.zones:
			if z.px is None or z.kind=="r":continue
			x,y,w,h=z.px;c=ZONE_COLORS.get(z.kind,"#3A78C8");Kit.add_box(g,x,y,w,h,.22,c)
			for e,f,i,j in((x,y,w,2),(x,y+h-2,w,2),(x,y,2,h),(x+w-2,y,2,h)):Kit.add_box(g,e,f,i,j,.9,c)
			if z.kind=="k":a=["Game area"]
			else:a=[z.id]+([L.title_of(r)for r in k["assign"].get(z.id,[])if r in L.wins]or["(empty)"])
			a=[Kit.fit(a6,max(20,w-28))for a6 in a[:max(1,(h-16)//20)]];Kit.add_box(g,x+6,y+6,max(Kit.text_w(a7)for a7 in a)+12,20*len(a)+6,.85,"#000000")
			for n,l in enumerate(a):Kit.add_label(g,l,x+12,y+9+20*n,Kit.HUE_TITLE if n==0 else Kit.HUE_TEXT)
		Grid.show_overlay(g,0,0,W,H);t["g"]=g
	def aj(i):W,H=Kit.screen();a,b,c=ai(i,W,H);k.update({"preset":i,"zs":a,"fname":b,"assign":dict((d,list(f))for d,f in c.items())})
	def ak():
		c,b=M["c"],k["look"]
		for a in b:
			if a in c:b[a]=bool(c[a].IsChecked)
	def aH():
		s=k;b=s["step"];M,j=Kit.MARGIN,Kit.GAP;W=at;c=W-2*M;L=LAYOUT;r=L.all_windows()if b==1 else[];h=(30+q+56+10,32+26*max(1,len(r))+8,32+26*len(R)+30)[b];J=M+30+j+h+j+44+M;g,l,K=E.begin(W,J)
		if not e["minimized"]:
			E.frame(g,settings=False,after="Step %d of 3"%(b+1));y=M+30+j
			if b==0:
				Kit.add_section(g,M,y,c,h,"LAYOUT  (click one; the screen shows it)");t,v=Kit.screen();d=y+32;N=M+(c-5*o-4*ab)//2
				for m,(C,D)in enumerate(A):
					i=N+m*(o+ab);w=m==s["preset"]
					if w:Kit.add_box(g,i-2,d-2,o+4,q+4,.95,"#E8C15A")
					Kit.add_box(g,i,d,o,q,1.,"#101010")
					if t>0 and v>0:
						F,G=o/float(t),q/float(v)
						for z in aG(m,t,v).zones:
							if z.px is None or z.kind=="r":continue
							O,P,Q,T=z.px;Kit.add_box(g,i+int(O*F)+1,d+int(P*G)+1,max(1,int(Q*F)-2),max(1,int(T*G)-2),.85 if w else.5,ZONE_COLORS.get(z.kind,"#3A78C8"))
					H=Kit.fit(C,o);Kit.add_label(g,H,i+(o-Kit.text_w(H))//2,d+q+6,Kit.HUE_TITLE if w else Kit.HUE_TEXT);Kit.catcher(g,i,d,o,q+26,u(("preset",m)),"Use %s: %s"%(C,D[:1].lower()+D[1:]))
				Kit.add_label(g,Kit.fit(A[s["preset"]][1],c-24),M+12,d+q+32,Kit.HUE_INFO)
			elif b==1:
				Kit.add_section(g,M,y,c,h,"WINDOWS  (click to change a zone)");a=y+32
				if not r:Kit.add_label(g,"No windows yet; turn modules on, then come back.",M+12,a+3,Kit.HUE_INFO)
				for x,U in r:n=S(x);Kit.add_label(g,Kit.fit(U,300),M+12,a+3);V="Zone: "+((n[5:]if n.startswith("Zone ")else n)if n else "free");Kit.art_button(g,l,"z_"+x,Kit.ART_PAGE,M+330,a-2,V,"Click: next zone (free: stays where it is)",on_click=u(("cycle",x)));a+=26
			else:
				Kit.add_section(g,M,y,c,h,"LOOK");a=y+32
				for I,X,Y in R:K[I]=Kit.add_check(g,X,M+12,a,s["look"][I],Y);a+=26
				Kit.add_label(g,"Change any of this later in Settings > Interface.",M+12,a+5,Kit.HUE_INFO)
			p=y+h+j;Kit.add_section(g,M,p,c,44);Kit.art_button(g,l,"cancel",Kit.ART_CLOSE,M+12,p+10,"Cancel","Close without changing anything",on_click=u("cancel"));f=("done",Kit.ART_OK,"Done","Use this layout")if b==2 else("next",Kit.ART_PLAY,"Next","Go to the next step");B=W-M-12-35-Kit.text_w(f[2]);Kit.art_button(g,l,f[0],f[1],B,p+10,f[2],f[3],on_click=u(f[0]))
			if b:B-=55+Kit.text_w("Back");Kit.art_button(g,l,"back",Kit.ART_PAGE,B,p+10,"Back","Go back a step",on_click=u("back"))
		E.end(g);aI()
	def D():Binds.scoped("interface.setup",aH)
	E=Kit.Window(aq,"Interface Setup",e,M,D,ar,default=(200,120),mini=au,owner=False,lock=False,close_tip="Close without changing anything")
	def aI():
		c=M["c"]
		if "status"in c:Kit.set_text(c["status"],"%s: step %d of 3"%("Interface Setup",k["step"]+1))
	def al():
		L=LAYOUT
		if not L.enabled:return
		if not k["open"]:Kit.put_var(Z,"1");k.update({"open":True,"step":0,"cards":{},"look":{"seam":True,"fit_view":L.fit_view,"game":L.game_grows}});e["minimized"]=False;aj(k["preset"])
		T();D()
	def U():k["open"]=False;a,t["g"]=t["g"],None;Kit.dispose(a);E.close()
	def aJ(i):aj(i);T();D()
	def aK(key):
		s=k;a=[None]+[g.id for g in s["zs"].zones if g.kind=="w"];b=S(key);d=S("worldmap");i=a.index(b)if b in a else 0
		for f in a:
			i=(i+1)%len(a);c=a[i]
			if c is None:break
			e=[h for h in s["assign"].get(c,[])if h!=key]
			if not((key=="worldmap"and e)or(key!="worldmap"and c==d)):break
		if b is not None:s["assign"][b]=[r for r in s["assign"][b]if r!=key]
		if c is not None:s["assign"].setdefault(c,[]).append(key)
		T();D()
	def am(d):ak();k["step"]=max(0,min(2,k["step"]+d));D()
	def aL():
		ak();s=k;L=LAYOUT;W,H=Kit.screen();e,b,c=s["zs"],s["fname"],s["look"];L.seamless,L.fit_view,L.game_grows=c["seam"],c["fit_view"],c["game"];L.save_opts()
		if b!=LAYOUT_DEFAULT:e.generated=False;L.save_frames(e.copy(b),b,W,H)
		L.use_frames(b,tell=False);L.assign=dict((g,list(f))for g,f in s["assign"].items()if f);L.unfree(None);L.save_assign();a=A[s["preset"]][0];a=a+" (mine)"if a in(LAYOUT_DEFAULT,LAYOUT_MIRRORED)else a;Kit.put_var(LAYOUT_NAMED%a,L.windows_text());d=L.layout_names()
		if a not in d:d.append(a);Kit.put_var(LAYOUT_LIST,",".join(d))
		L.layout_name=a;Kit.put_var(LAYOUT_ACTIVE,a);L.free_scrolled();L.placed={};L.refit_all();I();U();N();n=sum(1 for h in L.assign.values()for i in h if L.gump_of(i)is not None);v('"%s" in use: %s placed.'%(a,Kit.count(n,"window")),Kit.HUE_GOOD)
	def an():U();v("setup closed; nothing changed.",Kit.HUE_INFO)
	ao={"setup":al,"preset":aJ,"cycle":aK,"next":lambda:am(1),"back":lambda:am(-1),"done":aL,"cancel":an}
	def aM():
		L=LAYOUT;n=sum(len(c)for c in L.assign.values());a=L.frames
		if not n:return "No window in a zone yet: click Set up, or Arrange windows"
		b=Layout._game_px(a)if a is not None else None;return "%s in %s%s"%(Kit.count(n,"window"),Kit.count(len(L.assign),"zone"),"; game area %d x %d"%b[2:]if b else "")
	def O(g,names,i,x,y,tip):a=G.CreateDropDown(ac,names,i);a.SetPos(x,y);g.Add(a);return Kit.with_tip(a,tip)
	def aN(f,x,y):L=LAYOUT;a=j["frame_names"]=[LAYOUT_DEFAULT]+L.frame_names();c=a.index(L.frames_name)if L.frames_name in a else 0;b=j["layout_names"]=["(none)",LAYOUT_DEFAULT,LAYOUT_MIRRORED]+L.layout_names();d=L.layout_name or "(none)";e=b.index(d)if d in b else 0;Kit.add_label(f.g,"Zones:",x+12,y+3,Kit.HUE_TEXT);Kit.add_label(f.g,"Windows:",x+12,y+31,Kit.HUE_TEXT);j["zones"]=(O(f.g,a,c,x+92,y,"The frame layout in use (its zones)"),c);j["windows"]=(O(f.g,b,e,x+92,y+28,"The window layout in use; pick one to place every window"),e)
	def aO(f,x,y):
		L=LAYOUT;d=L.all_windows();k=L.page_preview;e=y-26*len(d)-(20 if k else 0);b=["free"]+[r for r in L.zone_choices()if r];j["zone_dd"]=[]
		for g,m in d:
			a=L.zone_of(g);c=h=b
			if a is not None and a not in b:c,h=b+[a],b+[Kit.fit("%s (missing)"%a,ac-30)]
			i=c.index(a)if a in c else 0;l=O(f.g,h,i,x+302,e,"The zone it sits in (free: stays where you put it)");j["zone_dd"].append((g,l,i,c));e+=26
	def aP(f,x,y):
		L=LAYOUT;a=j["situ_names"]=["(none)",LAYOUT_DEFAULT,LAYOUT_MIRRORED]+L.layout_names();j["situ_dd"]=[]
		for n,(b,d,e)in enumerate(ad):c=L.situ.get(b,"");i=a.index(c)if c in a else 0;Kit.add_label(f.g,d,x+12,y+3+28*n,Kit.HUE_TEXT);j["situ_dd"].append((b,O(f.g,a,i,x+92,y+28*n,e),i))
	def aQ():
		a=LAYOUT.share_code()
		if not a:v("no zones to share yet.",Kit.HUE_BAD);return
		B["code"]=a;f=s.f
		if f is not None and "code"in f.c:Kit.set(f.c["code"],"Text",a)
		e["jobs"].append(lambda:aR(a));v("layout code ready; Ctrl+A then Ctrl+C in the field copies it.",Kit.HUE_GOOD)
	def aR(code):
		try:Kit.write_safe(Kit.data_path(Layout.CODE_FILE),code+"\n")
		except Exception as a:v("couldn't write %s (%s)."%(Layout.CODE_FILE,a),Kit.HUE_BAD)
	def aS():f=s.f;c=f.c.get("code")if f is not None else None;LAYOUT.load_code(str(c.Text or "")if c is not None else B["code"])
	def aT(w):
		N();L=LAYOUT;b=L.all_windows();a=L.page_preview;h=("check","snap","Snap windows together","Windows dropped near each other line up");c=(("buttons",(("look",Kit.ART_PAGE,"Look: %s"%Kit.LOOK_NAMES[Kit.look()],"Next look: Classic, Dark, Parchment or High contrast"),("tsize",Kit.ART_PAGE,"Text size: %d%%"%int(round(Kit.tscale*100)),"Text in lists and bars (TazUO's own UI scale sizes every window)"))),("check","compact","Compact rows","Tighter rows in lists and settings; smaller frames"),("check","fade","Fade windows when idle","Dim windows until the mouse is over them or they change"),("num","fade_to","Faded:","How solid an idle window stays (20-90)","%",20,90),("num","fade_after","After:","Seconds without the mouse or a change before it fades (2-30)","s",2,30),("check","fade_all","Fade the Action Bar and unit frames too","Off: they stay solid while other windows fade"));d=("ACCESSIBILITY",(("check","cblind","Colour-blind marks","Letters beside notoriety and HP colours; colour-blind palette"),("check","streamer","Streamer mode","Hide names, guild and coordinates in Virtue Assistant windows")));e=(h,("check","grid_on","Show the grid","Show the snapping grid over the screen"),("num","grid","Grid:","Grid spacing for snapping","px",8,512))
		if VA_ALONE:return(("ZONES",(("note","Zones, layout and snapping are set in the full"),("note","Virtue Assistant."))),)
		if not L.enabled:return(("ZONES",(("note","Interface is off, so zones are off."),("note","Tick Interface on the Modules tab to use them."))),("LOOK",c),d,("SNAPPING",e))
		i=(("arrange",Kit.ART_OK,"Done","Lock every window in its zone")if L.arrange else("arrange",Kit.ART_PLAY,"Arrange windows","Unlock windows to drag them between zones (Esc or Done locks them)"));j=((("reclaim_undo",Kit.ART_CLOSE,"Undo","Put the zones back as before Reclaim space"),)if L._undo_load()is not None else());f=(("SCREEN",(("note",Kit.fit(aM(),w-24)),("note",Kit.fit(L.status_text(),w-24)),("buttons",(("setup",Kit.ART_PLAY,"Set up","Pick a ready-made layout in three steps"),i)),("buttons",(("edit",Kit.ART_PAGE,"Edit zones","Drag, resize, split or join zones"),("new",Kit.ART_OK,"New zones","Start a new frame layout with one zone"))))),("LOOK",tuple(("check",r,x,y)for r,x,y in R)+c),d,("SNAPPING",e),("LAYOUTS  (saved)",(("buttons",(("save",Kit.ART_OK,"Save windows","Save where every window sits as the window layout in use"),("reset",Kit.ART_CLOSE,"Reset","Go back to the Default window layout"),("free",Kit.ART_CLOSE,"Free all","Take every window out of its zone"))),("buttons",(("remove",Kit.ART_CLOSE,"Remove zones","Delete the frame layout in use (not Default)"),("check",Kit.ART_PLAY,"Check fit","Print where each window in a zone sits and if it fills it"))),("buttons",(("reclaim",Kit.ART_PLAY,"Reclaim space","Give the game area every gap beside it; windows keep their size"),)+j),("custom",60,aN),("buttons",(("share",Kit.ART_PAGE,"Share code","Put a code for the layouts in use in the field below"),("load_code",Kit.ART_OK,"Load code","Load the layout code in the field below"))),("text","code","Code:","Layout code: Ctrl+A then Ctrl+C copies it, Ctrl+V pastes one"))),("LAYOUTS BY SITUATION",(("check","situ_on","Switch layouts by situation","Use the layouts below in war mode, at the bank, in dungeons and in town"),("custom",28*len(ad),aP),("note","War mode first, then bank, dungeon, town"))))
		if not b:return f
		g=[("note",Kit.fit(z,270),{"hue":Kit.HUE_TEXT,"ndy":3,"h":26})for G,z in b]
		if a:g.append(("note",Kit.fit(a.lstrip("!"),w-24),{"ndy":3,"hue":Kit.HUE_BAD if a.startswith("!")else Kit.HUE_INFO}))
		return f+(("WINDOWS  (the zone each sits in)",g+[("custom",0,aO)]),)
	def aU(old,new):
		L=LAYOUT;a=set(b for b in new if new[b]!=old.get(b))
		if a&set(("seam","fit_view","game")):
			L.seamless,L.fit_view,L.game_grows=new["seam"],new["fit_view"],new["game"];L.save_opts();L.dirty=True
			if a&set(("seam","fit_view")):L.fresh=True;L.seam_skip={};L.seam_wait={}
		if "snap"in a:
			SNAP.enabled=new["snap"]
			if not SNAP.enabled:SNAP.links.clear()
			V()
		if "grid"in a:
			HOST.prefs["grid"]=str(new["grid"]);V()
			if HOST.grid is not None:HOST.grid.redraw()
		if "grid_on"in a and new["grid_on"]!=F():Q()
		if "situ_on"in a:L.situ_set(new["situ_on"])
		for k in("compact","cblind","streamer"):
			if k in a:X(k,new[k])
		if a&set(Fade.KEYS):FADE.set(new)
	def aV():o=Kit.LOOK_ORDER;HOST.set_look(o[(o.index(Kit.look())+1)%len(o)])
	def aW():o,a=Kit.TEXT_SIZES,int(round(Kit.tscale*100));X("tsize",o[(o.index(a)+1)%len(o)]if a in o else o[0])
	def aX():
		if not LAYOUT.remove_frames(LAYOUT.frames_name):v("Default can't be deleted; pick another frame layout first.",Kit.HUE_BAD)
	aY=(("setup",al),("arrange",lambda:LAYOUT.set_arrange(not LAYOUT.arrange)),("edit",lambda:ag(False)),("new",lambda:ag(True)),("remove",aX),("save",lambda:LAYOUT.save_windows()),("reset",lambda:LAYOUT.use_windows(LAYOUT_DEFAULT)),("free",lambda:LAYOUT.use_windows("")),("reclaim",lambda:LAYOUT.reclaim_space()),("reclaim_undo",lambda:LAYOUT.reclaim_back()),("check",lambda:LAYOUT.report_fit()),("look",aV),("tsize",aW),("share",aQ),("load_code",aS))
	def aZ(f):
		L=LAYOUT
		if L.page_refresh:L.page_refresh=False;s.f=None;HOST.refresh_settings(J);return
		for n,(b,a,e,c)in enumerate(j["zone_dd"]):
			i=Kit.dd_index(a,e)
			if i!=e and 0<=i<len(c):
				j["zone_dd"][n]=(b,a,i,c);d=None if i==0 else c[i];L.page_preview=""
				if d:W,H=Kit.screen();g=L.frames_in_use(W,H)if W>0 and H>0 else None;L.page_preview=L.preview_text(b,g.by_id(d)if g is not None else None)
				L.assign_to(b,d);L.page_refresh=True;return
		if j["zones"]is not None:
			a,h=j["zones"];i=Kit.dd_index(a,h)
			if i!=h and 0<=i<len(j["frame_names"]):j["zones"]=(a,i);L.use_frames(j["frame_names"][i]);return
			a,k=j["windows"];i=Kit.dd_index(a,k)
			if i!=k and 0<=i<len(j["layout_names"]):j["windows"]=(a,i);L.use_windows(""if i==0 else j["layout_names"][i]);return
		for n,(l,a,m)in enumerate(j["situ_dd"]):
			i=Kit.dd_index(a,m)
			if i!=m and 0<=i<len(j["situ_names"]):j["situ_dd"][n]=(l,a,i);L.situ_pick(l,""if i==0 else j["situ_names"][i]);return
		for o,p in aY:
			if Kit.was_clicked(f.store,o):p();return
	s=Kit.Page(B,aT,ax,aU,clicks=aZ)
	def a_():j.update({"zones":None,"windows":None,"zone_dd":[],"situ_dd":[]});s.closed()
	def a0():
		e.update({"shutting":False,"docked":False,"queue":[],"minimized":False,"editor":None,"back_sig":None,"back_at":0.,"alone_up":False,"jobs":[]});k["open"]=False
		if VA_ALONE:N();Y(J);return
		LAYOUT.set_enabled(True);N();ae.service("interface.page",lambda:Y(J))
		if not Kit.get_var(Z,"")and not LAYOUT.assign and not Kit.get_var(LAYOUT_ACTIVE,""):u("setup")()
	def a1():
		if VA_ALONE:
			c=HOST.config.win["g"]is not None
			if e["alone_up"]and not c:HOST.disable(J)
			e["alone_up"]=e["alone_up"]or c;return
		q=e["queue"]
		while q:
			a=q.pop(0);a="toggle_min"if a=="to_bar"else a
			if isinstance(a,tuple):ao[a[0]](*a[1:])
			elif not E.action(a):ao[a]()
		if k["open"]and Kit.was_clicked(M["store"],"close"):an()
		b=e["editor"]
		if b is not None:
			W,H=Kit.screen()
			if W>0 and H>0:b.keep(W,H)
			b.poll()
		d=time.time();LAYOUT.situ_tick(d,b is not None or k["open"]);Seam.hover(LAYOUT.arrange);aD(d);aC()
	def a2():
		while e["jobs"]and not e["shutting"]:e["jobs"].pop(0)()
	def a3():a=not(e["queue"]or k["open"]or Seam.recs or Seam.bare or VA_ALONE);return.25 if a and e["editor"]is None and p["g"]is None else.05
	def a4():
		e["shutting"]=True;a=e["editor"]
		if a is not None:a.close(keep=False,quiet=True)
		if k["open"]:U()
		for b in(p,C,t):c,b["g"]=b["g"],None;Kit.dispose(c)
		if not VA_ALONE:LAYOUT.set_enabled(False)
		ae.close()
	return{"start":a0,"tick":a1,"stop":a4,"client_tick":True,"config_height":s.height,"build_config":s.build,"poll_config":s.poll,"config_closed":a_,"interval":a3,"thread_tick":a2,"thread_wanted":lambda:bool(e["jobs"])}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("interface","Interface","Zones, layout and the unified UI",_module_interface,.05,default_on=True,category="On screen")
