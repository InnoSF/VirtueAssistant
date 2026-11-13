def _module_interface():
    KEY = "interface"; TITLE = "Interface"; SETUP_KEY = "interface.setup"; SETUP_POS = "Interface_setup_pos"
    SEEN_KEY = "Interface_setup_seen"; EDITOR_POS = "VirtueAssistant_layout_editor_pos"
    SETUP_W, SETUP_MINI = 600, (260, 46); CARD_W, CARD_H, CARD_GAP = 100, 64, 12; DD_W = 170; BACK_EVERY = 0.25
    RING, RING_GOLD, RING_DARK = 3, "#D4AF37", "#3A2A08"
    PRESETS = (("Sides", "Bags and paperdoll left; map and trackers right"),
               ("Mirrored", "Map and trackers left; bags and paperdoll right"),
               ("Bottom bar", "Game on top; every window in one band below"),
               ("Right column", "Game left; windows stacked on the right"),
               ("Compact", "Windows stacked on the left; game on the right"))
    ROLES = (("unitframes.", "frames"), ("actionbar", "bar"), ("character", "gear"), ("bag", "bag"),
             ("ultima.", "watch"), ("hub", "watch"), ("meters", "watch"), ("worldmap", "map"))
    LOOK_ROWS = (("seam", "Join windows in zones into one panel",
                  "One frame round every zone, gold round the game view; hover a window's top for its title"),
                 ("fit_view", "Fit the game view to the game area", "Borderless, sized and locked to the game area"),
                 ("game", "Give an empty zone's room to the game area", "Widens the game area beside an empty zone"))
    settings = {"seam": False, "fit_view": True, "game": True, "snap": True, "grid_on": False, "grid": GRID_DEFAULT,
                "compact": False, "cblind": False, "streamer": False, "code": "", "situ_on": False, "fade": False,
                "fade_to": 40, "fade_after": 6, "fade_all": False}
    DEFAULTS = dict(settings)
    st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "editor": None, "back_sig": None,
          "back_at": 0.0, "jobs": []}
    win = {"g": None, "c": {}, "store": ({}, {})}
    back = {"g": None}; ring = {"g": None}; preview = {"g": None}
    sinker = {"gumps": None, "ver": None, "same": None, "off": False, "seen": None, "raw": None}
    page = {"zones": None, "windows": None, "zone_dd": [], "frame_names": [], "layout_names": [], "situ_dd": [],
            "situ_names": []}
    SITU_ROWS = (("war", "War mode:", "The window layout while you are in war mode"),
                 ("bank", "Bank:", "The window layout near your bank for 5 minutes after you open it"),
                 ("dungeon", "Dungeon:", "The window layout in a dungeon"),
                 ("town", "Town:", "The window layout in a guard zone"))
    setup = {"open": False, "step": 0, "preset": 0, "zs": None, "fname": LAYOUT_DEFAULT, "assign": {}, "look": {},
             "cards": {}}
    cleanup, queue, say = Kit.basics(st, TITLE)
    def load_settings():
        L = LAYOUT
        settings.update({"seam": L.seamless, "fit_view": L.fit_view, "game": L.game_grows, "snap": SNAP.enabled,
                         "grid_on": HOST.grid_shown(), "grid": HOST.grid_size(), "compact": Kit.compact,
                         "cblind": Kit.cblind, "streamer": Kit.streamer, "situ_on": L.situ["on"],
                         "fade": FADE.on, "fade_to": int(round(FADE.to * 100)), "fade_after": int(FADE.after),
                         "fade_all": FADE.all})
    def save_settings(): pass
    def touch(a, b):
        ax, ay, aw, ah = a; bx, by, bw, bh = b; D = SNAP_DIST
        for lo, hi in ((ax + aw, bx), (bx + bw, ax)):
            y0, y1 = max(ay, by), min(ay + ah, by + bh)
            if abs(hi - lo) <= D and y1 > y0: return "v", min(lo, hi), max(lo, hi), y0, y1
        for lo, hi in ((ay + ah, by), (by + bh, ay)):
            x0, x1 = max(ax, bx), min(ax + aw, bx + bw)
            if abs(hi - lo) <= D and x1 > x0: return "h", min(lo, hi), max(lo, hi), x0, x1
        return None
    def gaps_of(s0, s1, cov):
        out, at = [], s0
        for a, b in sorted(cov):
            if a > at: out.append((at, min(a, s1)))
            at = max(at, b)
        if at < s1: out.append((at, s1))
        return [(a, b) for a, b in out if b > a]
    class LayoutEditor(object):
        BAR_W = 720; SETTLE = 0.3; FIELD_W = 52; ROW = 28
        KEYS = {"up": ("UP",), "down": ("DOWN",), "left": ("LEFT",), "right": ("RIGHT",),
                "delete": ("DELETE",), "z": ("Z",), "y": ("Y",), "enter": ("RETURN", "KP_ENTER"), "esc": ("ESCAPE",)}
        FIELDS = ("col", "row", "w", "h")
        def __init__(self, layout, zs, on_close):
            self.layout = layout; self.zs = zs; self.on_close = on_close; self.frames = {}; self.bar = None
            self.store = ({}, {}); self.c = {}
            self.renames = {}; self.sel = zs.zones[0].id if zs.zones else None; self.multi = set(); self.grid_was = None
            self.fields = None; self.saveas_text = ""; self.bar_pos = None; self.rebuild = False; self.closed = False
            self.others = None
            self.W, self.H = Kit.screen(); self.px_mode = False; self.undo, self.redo = [], []; self.keys_was = {}
            self.focus_was = None; self.raws = {}; self.said = None; self.del_armed = None; self.marks = None
            self.marks_sig = None; self.counts = (0, 0); self.handles = []; self.handles_sig = None; self.edge = None
            self.edge_g = None; self.edge_at = 0.0; self.pressed_was = False; self.pick = 0; self.pick_keys = []
            self.preview = ""; self.raws_ok = False; self._pick_next = 0.0
            self.start_px = dict((z.id, tuple(z.px)) for z in zs.zones if z.px is not None)
        def open(self):
            self.grid_was = HOST.grid_shown()
            if not self.grid_was: safe(HOST.grid_toggle)
            for z in self.zs.zones: self.build_zone(z)
            self.build_bar(); self.draw_marks()
        def close(self, keep, quiet=False):
            if self.closed: return
            self.closed = True
            for zid, fr in list(self.frames.items()): Kit.dispose(fr.get("g"))
            self.frames = {}; self._drop_handles()
            for a in ("bar", "marks", "edge_g"): Kit.dispose(getattr(self, a)); setattr(self, a, None)
            if self.grid_was is not None and HOST.grid_shown() != self.grid_was: safe(HOST.grid_toggle)
            self.on_close(); self.layout.dirty = True; self.layout.page_refresh = True
            if not keep and not quiet: Kit.say("the saved zones are back.", Kit.HUE_INFO)
        def _snap(self): return ([z.copy() for z in self.zs.zones], self.sel, dict(self.renames))
        def push(self):
            self.undo.append(self._snap())
            if len(self.undo) > 50: del self.undo[0]
            self.redo = []
        def _restore(self, snap):
            zones, sel, renames = snap
            for zid in list(self.frames): Kit.dispose(self.frames[zid].get("g"))
            self.frames = {}; self.zs.zones = [z.copy() for z in zones]; self.renames = dict(renames)
            self.sel = (sel if self.zs.by_id(sel) is not None else (self.zs.zones[0].id if self.zs.zones else None))
            self.multi = set(); self.pick = 0; self.preview = ""
            for z in self.zs.zones: self.build_zone(z)
            self.rebuild = True
        def _hist(self, a, b, word):
            if not a: self.say("nothing to %s." % word, Kit.HUE_INFO); return
            b.append(self._snap()); self._restore(a.pop())
        def do_undo(self): self._hist(self.undo, self.redo, "undo")
        def do_redo(self): self._hist(self.redo, self.undo, "redo")
        def say(self, text, hue=None):
            now = time.time()
            if self.said is not None and self.said[0] == text and now - self.said[1] < 2.0: return
            self.said = (text, now); Kit.say(text, Kit.HUE_BAD if hue is None else hue)
        def _windows_in(self, z):
            L = self.layout; zid = self.orig_id(z.id); return [L.title_of(k) for k in L.assign.get(zid, [])]
        def orig_id(self, zid):
            for was, now in self.renames.items():
                if now == zid: return was
            return zid
        def new_id(self):
            L = self.layout; taken = set(self.renames) | set(L.assign); n = len(self.zs.zones) + 1
            if L.frames is not None and self.zs.name == L.frames_name: taken |= set(L.frames.ids())
            for nm in L.layout_names():
                f, a = L.parse_windows(Kit.get_var(LAYOUT_NAMED % nm, ""))
                if f == self.zs.name: taken |= set(a)
            b = L.situ_back
            if b is not None and b[1] == self.zs.name: taken |= set(b[2])
            while "Zone %d" % n in taken or self.zs.by_id("Zone %d" % n) is not None: n += 1
            return "Zone %d" % n
        def build_zone(self, z):
            old = self.frames.get(z.id, {}).get("g"); x, y, w, h = z.px; M = Kit.MARGIN
            fr = {"g": None, "resize_at": 0.0, "size": (w, h), "pv": z.id == self.sel and self.pick > 0}
            g = G.CreateModernGump(x, y, w, h, not z.lock, ZONE_MIN_W, ZONE_MIN_H, self._resized(z.id)); g.SetAlpha(0)
            if z.lock: g.CanMove = False
            Kit.add_window_frame(g, w, h, corners=False, mouse=False)
            Kit.add_box(g, M, M, w - 2 * M, h - 2 * M, 0.25, ZONE_COLORS.get(z.kind, "#FFFFFF"))
            if z.kind == "w" and z.stack == "t": Kit.add_box(g, M, M + 31, w - 2 * M, 4, 0.9, "#E8C15A")
            self._draw_overlaps(g, z)
            if z.kind == "k": self._draw_game(g, z)
            if fr["pv"]: self._draw_preview(g, z)
            Kit.add_section(g, M, M, w - 2 * M, 30); sel = z.id == self.sel or z.id in self.multi
            fr["lbl"] = Kit.add_label(g, Kit.fit(z.id + ("  (locked)" if z.lock else ""), w - 2 * M - 24),
                                      M + 12, M + 7, Kit.HUE_TITLE if sel else Kit.HUE_TEXT)
            wins = self._windows_in(z) if z.kind == "w" else []
            fr["wins"] = Kit.add_label(g, Kit.fit(", ".join(wins), w - 2 * M - 24) if wins else "",
                                       M + 12, M + 30 + 6, Kit.HUE_TEXT)
            fr["sum"] = Kit.add_label(g, "", M + 12, M + 30 + 6 + (20 if wins else 0), Kit.HUE_INFO)
            Kit.catcher(g, M, M, w - 2 * M, 30, self._select(z.id), "Select the zone (Shift+click: pick more)" + (
                "; locked" if z.lock else "; drag to move it on the grid"), movable=not z.lock)
            Kit.place(g, x, y, w, h); Kit.add_front(g); Kit.no_snap(g); Kit.on_moved(g, self._moved(z.id))
            fr["g"] = g; self.frames[z.id] = fr; self.update_zone(z); Kit.dispose(old)
        def _draw_overlaps(self, g, z):
            x, y, w, h = z.px
            for o in self.zs.zones:
                if o is z or o.px is None or not (z.overlap or o.overlap): continue
                ox, oy, ow, oh = o.px; ax, ay = max(x, ox), max(y, oy)
                bx, by = min(x + w, ox + ow), min(y + h, oy + oh)
                if bx - ax < 4 or by - ay < 4: continue
                for sx in range(ax, bx, 12): Kit.add_box(g, sx - x, ay - y, min(4, bx - sx), by - ay, 0.45, "#E8C15A")
        def _draw_game(self, g, z):
            zs = self.zs.copy(); Layout._overlap_shape(zs); kx, ky, kw, kh = zs.by_id(z.id).px; kx -= z.px[0]
            ky -= z.px[1]
            for r in ((kx, ky + kh - 2, kw, 2), (kx, ky, 2, kh), (kx + kw - 2, ky, 2, kh), (kx, ky, kw, 2)):
                Kit.add_box(g, r[0], r[1], r[2], r[3], 0.9, "#E8C15A")
        def _draw_preview(self, g, z):
            key = self.pick_keys[self.pick] if 0 < self.pick < len(self.pick_keys) else None
            if key is None or z.kind != "w": return
            L = self.layout; keys = [k for k in L.assign.get(self.orig_id(z.id), []) if k != key] + [key]
            x, y = z.px[0], z.px[1]
            for k, (sx, sy, sw, sh) in L.slots_for(z, keys):
                Kit.add_box(g, sx - x, sy - y, max(1, sw), max(1, sh), 0.55, "#E8C15A" if k == key else "#202020")
                Kit.add_label(g, Kit.fit(L.title_of(k), max(20, sw - 16)), sx - x + 8, sy - y + sh - 26, Kit.HUE_TEXT)
        def update_zone(self, z):
            fr = self.frames.get(z.id)
            if fr is None: return
            if fr["pv"] != (z.id == self.sel and self.pick > 0): self.build_zone(z); return
            step = HOST.grid_size(); x, y, w, h = z.px
            text = "%s, %d x %d squares" % (z.kind_name(), max(1, int(round(float(w) / step))),
                                            max(1, int(round(float(h) / step))))
            if z.overlap: text += ", overlaps"
            Kit.set_text(fr["sum"], Kit.fit(text, w - 2 * Kit.MARGIN - 24))
            Kit.set_text(fr["lbl"], Kit.fit(z.id + ("  (locked)" if z.lock else ""), w - 2 * Kit.MARGIN - 24),
                         Kit.HUE_TITLE if (z.id == self.sel or z.id in self.multi) else Kit.HUE_TEXT)
        def _select(self, zid):
            def hit():
                shift = bool(Client.key_held("shift"))
                if shift and self.sel is not None and zid != self.sel:
                    if zid in self.multi: self.multi.discard(zid)
                    else: self.multi.add(zid); self.multi.add(self.sel)
                    self.rebuild = True; HOST.poke(); return
                if zid != self.sel or self.multi:
                    self.multi = set(); self.sel = zid; self.pick = 0; self.preview = ""; self.rebuild = True
                    HOST.poke()
            return hit
        def _resized(self, zid):
            def hit(*args):
                fr = self.frames.get(zid)
                if fr is not None: fr["resize_at"] = time.time()
            return hit
        def _moved(self, zid):
            def hit():
                z = self.zs.by_id(zid); fr = self.frames.get(zid)
                if z is None or fr is None or not Kit.is_open(fr["g"]): return
                r = Snap.rect(fr["g"])
                if r is None: return
                if (r[0], r[1]) == (z.px[0], z.px[1]): return
                if z.lock:
                    self.place_zone(z); self.say('zone "%s" is locked; click Lock to move it.' % z.id, Kit.HUE_INFO)
                    return
                self.landed(z, r[0], r[1], z.px[2], z.px[3], resized=False)
            return hit
        def _blocker(self, z): hits = self.zs.overlaps(z); return hits[0] if hits else None
        def landed(self, z, x, y, w, h, resized=True):
            W, H = self.W, self.H; step = HOST.grid_size()
            if resized:
                sn = 1 if z.free else step; w = max(ZONE_MIN_W, int(round(float(w) / sn)) * sn)
                h = max(ZONE_MIN_H, int(round(float(h) / sn)) * sn)
            w, h = min(w, W), min(h, H); best = (0, int(x), int(y)) if z.free else Snap.near_anchor(x, y, w, h)
            if best is not None: nx, ny = best[1], best[2]
            else:
                nx = ny = None
                for tx in (0, max(0, W - w)):
                    if abs(tx - x) <= SNAP_DIST: nx = tx
                for ty in (0, max(0, H - h)):
                    if abs(ty - y) <= SNAP_DIST: ny = ty
                for o in self.zs.zones:
                    if o is z or o.px is None: continue
                    ox, oy, ow, oh = o.px
                    if nx is None and oy < y + h + SNAP_DIST and y < oy + oh + SNAP_DIST:
                        for tx in (ox + ow, ox - w, ox, ox + ow - w):
                            if abs(tx - x) <= SNAP_DIST: nx = tx
                    if ny is None and ox < x + w + SNAP_DIST and x < ox + ow + SNAP_DIST:
                        for ty in (oy + oh, oy - h, oy, oy + oh - h):
                            if abs(ty - y) <= SNAP_DIST: ny = ty
                if nx is None: nx = int(round(float(x) / step)) * step
                if ny is None: ny = int(round(float(y) / step)) * step
            was = z.px; self.push(); z.set_px(nx, ny, w, h, W, H)
            if not self.zs.push_clear(z, W, H, None if z.free else step):
                z.set_px(was[0], was[1], was[2], was[3], W, H); self.undo.pop(); o = self._blocker(z)
                self.say('no room for zone "%s" there%s; it stays where it was.' % (
                    z.id, (' (it would cover "%s")' % o.id) if o is not None else ""))
            z.note_pins(W, H); self.place_zone(z); self.changed()
        def _refields(self): self.fields = None; self.show_fields()
        def changed(self): self._refields(); self.draw_marks()
        def place_zone(self, z):
            fr = self.frames.get(z.id)
            if fr is None: return
            x, y, w, h = z.px
            if ((w, h) != fr["size"] or z.overlap or z.kind == "k" or any(o.overlap for o in self.zs.zones)):
                self.build_zone(z); return
            with Kit.quiet: Kit.place(fr["g"], x, y, w, h); Kit.moved_by_code(fr["g"])
            self.update_zone(z)
        def keep(self, W, H):
            if (W, H) != (self.W, self.H):
                self.W, self.H = W, H; self.zs.reflow(W, H, HOST.grid_size()); self.undo, self.redo = [], []
                for z in self.zs.zones: self.place_zone(z)
                self.draw_marks(); self.rebuild = True
        def gaps(self):
            W, H = self.W, self.H; zs = [z.px for z in self.zs.zones if z.px is not None]
            xs = [v for v in sorted(set([0, W] + [p[0] for p in zs] + [p[0] + p[2] for p in zs])) if 0 <= v <= W]
            ys = [v for v in sorted(set([0, H] + [p[1] for p in zs] + [p[1] + p[3] for p in zs])) if 0 <= v <= H]
            nx, ny = len(xs) - 1, len(ys) - 1; free = {}
            for j in range(ny):
                cy = (ys[j] + ys[j + 1]) / 2.0
                for i in range(nx):
                    cx = (xs[i] + xs[i + 1]) / 2.0
                    if not any(p[0] <= cx < p[0] + p[2] and p[1] <= cy < p[1] + p[3] for p in zs): free[(i, j)] = True
            seen, n = set(), 0
            for cell in free:
                if cell in seen: continue
                n += 1; stack = [cell]; seen.add(cell)
                while stack:
                    i, j = stack.pop()
                    for nb in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                        if nb in free and nb not in seen: seen.add(nb); stack.append(nb)
            rects = []
            for j in range(ny):
                i = 0
                while i < nx:
                    if (i, j) in free:
                        i0 = i
                        while i < nx and (i, j) in free: i += 1
                        rects.append((xs[i0], ys[j], xs[i] - xs[i0], ys[j + 1] - ys[j]))
                    else: i += 1
            merged = []
            for r in rects:
                for k, m in enumerate(merged):
                    if m[0] == r[0] and m[2] == r[2] and m[1] + m[3] == r[1]:
                        merged[k] = (m[0], m[1], m[2], m[3] + r[3]); break
                else: merged.append(r)
            return merged, n
        def bad_overlaps(self):
            out = []; zones = self.zs.zones
            for i, a in enumerate(zones):
                for b in zones[i + 1:]:
                    if a.px is None or b.px is None or b not in self.zs.overlaps(a): continue
                    if a in self.zs.overlaps(b) or not b.overlap:
                        x0, y0 = max(a.px[0], b.px[0]), max(a.px[1], b.px[1])
                        x1 = min(a.px[0] + a.px[2], b.px[0] + b.px[2]); y1 = min(a.px[1] + a.px[3], b.px[1] + b.px[3])
                        if x1 > x0 and y1 > y0: out.append((a, b, (x0, y0, x1 - x0, y1 - y0)))
            return out
        def draw_marks(self):
            sig = (self.W, self.H, tuple((z.id, z.kind, z.overlap, z.solo, tuple(z.px or ())) for z in self.zs.zones))
            if sig == self.marks_sig and (self.marks is None or Kit.is_open(self.marks)): return
            self.marks_sig = sig; gaps, n = self.gaps(); bad = self.bad_overlaps(); counts = (n, len(bad))
            old, self.marks = self.marks, None; Kit.dispose(old)
            wz = [z for z in self.zs.zones if z.kind == "w" and z.px is not None and not z.solo]
            joins = [s for i, a in enumerate(wz) for b in wz[i + 1:] for s in (touch(a.px, b.px),) if s is not None]
            if gaps or bad or joins:
                g = G.CreateGump(False, False)
                for (x, y, w, h) in gaps: Kit.add_box(g, x, y, w, h, 0.45, "#C83030")
                for a, b, (x, y, w, h) in bad: Kit.add_box(g, x, y, w, h, 0.55, "#C83030")
                for o, lo, hi, a, b in joins:
                    c = (lo + hi) // 2
                    Kit.add_box(g, *(((c - 2, a, 4, b - a) if o == "v" else (a, c - 2, b - a, 4)) + (0.9, "#E8C15A")))
                Grid.show_overlay(g, 0, 0, self.W, self.H); self.marks = g
            if counts != self.counts: self.counts = counts; self.rebuild = True
        def _drop_handles(self):
            for g, side, r in self.handles: Kit.dispose(g)
            self.handles = []; self.handles_sig = None
        def _sync_handles(self):
            z = self.zs.by_id(self.sel) if self.sel else None; fr = self.frames.get(z.id) if z is not None else None
            sig = (z.id, tuple(z.px), z.lock,
                   fr.get("g") if fr else None) if z is not None and z.px is not None else None
            if sig == self.handles_sig: return
            self._drop_handles(); self.handles_sig = sig
            if z is None or z.lock: return
            x, y, w, h = z.px; T = 10; L_ = max(24, min(80, w // 3)); V_ = max(24, min(80, h // 3))
            for side, r in (("l", (x, y + (h - V_) // 2, T, V_)), ("r", (x + w - T, y + (h - V_) // 2, T, V_)),
                            ("t", (x + (w - L_) // 2, y + Kit.MARGIN + 30, L_, T)),
                            ("b", (x + (w - L_) // 2, y + h - T, L_, T))):
                g = G.CreateGump(True, False); Kit.add_box(g, 0, 0, r[2], r[3], 0.9, "#E8C15A")
                Kit.catcher(g, 0, 0, r[2], r[3], lambda: None, "Drag to move this edge on the grid")
                g.SetRect(r[0], r[1], r[2], r[3]); Kit.add_front(g); SNAP.skip_gump(g)
                self.handles.append((g, side, r))
        def _edge_tick(self, pressed):
            now = time.time()
            if self.edge is None:
                if pressed and not self.pressed_was and self.handles:
                    m = Kit.mouse_pos()
                    if m is not None:
                        for g, side, r in self.handles:
                            if r[0] <= m[0] < r[0] + r[2] and r[1] <= m[1] < r[1] + r[3]:
                                z = self.zs.by_id(self.sel)
                                if z is not None: self.edge = (z.id, side, m, tuple(z.px))
                                break
                return
            zid, side, m0, p0 = self.edge; z = self.zs.by_id(zid); m = Kit.mouse_pos()
            if z is None or m is None: self.edge = None; Kit.dispose(self.edge_g); self.edge_g = None; return
            x, y, w, h = p0; dx, dy = m[0] - m0[0], m[1] - m0[1]
            if side == "l": nx = min(x + w - ZONE_MIN_W, max(0, x + dx)); x, w = nx, w + (x - nx)
            elif side == "r": w = max(ZONE_MIN_W, min(self.W - x, w + dx))
            elif side == "t": ny = min(y + h - ZONE_MIN_H, max(0, y + dy)); y, h = ny, h + (y - ny)
            else: h = max(ZONE_MIN_H, min(self.H - y, h + dy))
            if pressed:
                if now - self.edge_at >= 0.05:
                    self.edge_at = now; step = HOST.grid_size(); old, self.edge_g = self.edge_g, None; Kit.dispose(old)
                    g = G.CreateGump(False, False)
                    for bx, by, bw_, bh in ((0, 0, w, 2), (0, h - 2, w, 2), (0, 0, 2, h), (w - 2, 0, 2, h)):
                        Kit.add_box(g, bx, by, bw_, bh, 0.95, "#E8C15A")
                    t = "%d x %d squares (%d x %d)" % (max(1, int(round(float(w) / step))),
                                                        max(1, int(round(float(h) / step))), w, h)
                    Kit.add_box(g, 6, 6, Kit.text_w(t) + 12, 22, 0.85, "#000000")
                    Kit.add_label(g, t, 12, 8, Kit.HUE_TITLE)
                    Grid.show_overlay(g, x, y, w, h); self.edge_g = g
                return
            self.edge = None; Kit.dispose(self.edge_g); self.edge_g = None
            if (x, y, w, h) != p0: self.landed_rect(z, x, y, w, h)
        def landed_rect(self, z, x, y, w, h):
            step = 1 if z.free else HOST.grid_size()
            x0, y0, x1, y1 = [int(round(float(v) / step)) * step for v in (x, y, x + w, y + h)]
            x1, y1 = min(x1, self.W), min(y1, self.H)
            if not z.free and x + w >= self.W - SNAP_DIST: x1 = self.W
            if not z.free and y + h >= self.H - SNAP_DIST: y1 = self.H
            self.apply_rect(z, x0, y0, max(ZONE_MIN_W, x1 - x0), max(ZONE_MIN_H, y1 - y0))
        def apply_rect(self, z, x, y, w, h, typed=None):
            W, H = self.W, self.H
            if w > W or h > H or x < 0 or y < 0 or x + w > W or y + h > H:
                self.say('zone "%s" can\'t be %s there: it would run off the screen; make it '
                         'smaller or move it.' % (z.id, typed or "that size"))
                return False
            was = z.px; z.set_px(x, y, w, h, W, H); o = self._blocker(z)
            if o is not None:
                z.set_px(was[0], was[1], was[2], was[3], W, H)
                self.say('zone "%s" can\'t be %s there: it would cover "%s"; make it %s or move ' 'it.' % (
                    z.id, typed or "that size", o.id,
                    "shorter" if (h > was[3] and w <= was[2]) else "narrower" if w > was[2] else "smaller"))
                return False
            nw = z.px; z.set_px(was[0], was[1], was[2], was[3], W, H); self.push()
            z.set_px(nw[0], nw[1], nw[2], nw[3], W, H); z.note_pins(W, H); self.said = None; self.place_zone(z)
            self.changed(); return True
        @staticmethod
        def _cap_w(cap): return 35 + Kit.text_w(cap)
        def _flow(self, g, store, items, x0, y, x_max):
            x = x0
            for key, art, cap, tip in items:
                cw = self._cap_w(cap)
                if x > x0 and x + cw > x_max: x = x0; y += self.ROW
                if g is not None: Kit.art_button(g, store, key, art, x, y - 2, cap, tip)
                x += cw + 16
            return y
        def build_bar(self): Binds.scoped("interface.editor", self.draw_bar)
        def draw_bar(self):
            old = self.bar; W = self.BAR_W; M, GAP = Kit.MARGIN, Kit.GAP; store = ({}, {}); c = {}
            g = G.CreateGump(True, True); IW = W - 2 * M; x_max = M + IW - 12
            z = self.zs.by_id(self.sel) if self.sel else None; L = self.layout; step = HOST.grid_size(); ops = []
            y1 = M + 30 + GAP; ry = y1 + 32; body = []
            if z is None:
                body.append(("label", "Click Add zone, then drag it into place.", M + 12, ry + 3, Kit.HUE_INFO))
                ry += self.ROW
            else:
                nx = M + 12 + Kit.text_w("Name:") + 8; body.append(("label", "Name:", M + 12, ry + 3, None))
                body.append(("box", "name", z.id, nx, ry, 130, False,
                             "Zone name, unique in this frame layout; Enter uses it"))
                items = [("kind", Kit.ART_PAGE, "Kind: " + z.kind_name(), "Switch kind: window, keep clear, reserved"),
                         ("stack", Kit.ART_PAGE, "Stack: " + z.stack_name(),
                          "Switch the way windows stack in this zone"),
                         ("prio", Kit.ART_PAGE, "Shrinks: " + _ordinal(z.prio),
                          "Change when this zone shrinks to minimized bars on a small screen"),
                         ("overlap", Kit.ART_PAGE, "Overlap: " + ("on" if z.overlap else "off"),
                          "Let this zone lie over others (on) or keep clear of them (off)"),
                         ("lock", Kit.ART_PAGE, "Lock: " + ("on" if z.lock else "off"),
                          "Lock the zone against moving and resizing, or unlock it"),
                         ("split", Kit.ART_PLAY, "Split", "Cut this zone in two along its long side"),
                         ("join", Kit.ART_OK, "Join", "Merge with a zone flush beside it of the same height or width"),
                         ("solo", Kit.ART_PAGE, "Apart: " + ("on" if z.solo else "off"),
                          "Keep this zone's panel apart from zones it touches (on) or join them (off)"),
                         ("free", Kit.ART_PAGE, "Snap: " + ("off" if z.free else "on"),
                          "Snap this zone to the grid and its neighbours (on) or place it to the pixel (off)"),
                         ("dup", Kit.ART_OK, "Duplicate", "Add a copy of this zone beside it"),
                         ("remove", Kit.ART_CLOSE, "Remove",
                          "Remove this zone (or Delete twice); its windows become free")]
                ops.append(("flow", items, nx + 130 + 16, ry))
                ry = self._flow(None, None, items, nx + 130 + 16, ry, x_max) + self.ROW; fx = M + 12
                unit = "px" if self.px_mode else "squares"
                for key, label, tip in (("col", "X:" if self.px_mode else "Col:",
                                         "Left edge in %s from the screen's left"),
                                        ("row", "Y:" if self.px_mode else "Row:",
                                         "Top edge in %s from the screen's top"),
                                        ("w", "W:", "Width in %s"), ("h", "H:", "Height in %s")):
                    hi = (self.W if key in ("col", "w") else self.H)
                    if key in ("col", "row"):
                        hi = (hi - (ZONE_MIN_W if key == "col" else ZONE_MIN_H)) // (1 if self.px_mode else step)
                    elif not self.px_mode: hi = (hi + step - 1) // step
                    body.append(("label", label, fx, ry + 3, None)); fx += Kit.text_w(label) + 6
                    body.append(("box", key, "", fx, ry, self.FIELD_W, True,
                                 (tip % unit) + " (%d-%d); Enter or Apply uses it, "
                                 "Esc puts it back" % (0 if key in ("col", "row") else 1, hi)))
                    fx += self.FIELD_W + 14
                items = [("apply", Kit.ART_OK, "Apply", "Use the typed values (Enter does too)"),
                         ("units", Kit.ART_PAGE, "Units: " + unit, "Switch between grid squares and pixels")]
                ops.append(("flow", items, fx + 4, ry))
                ry = self._flow(None, None, items, fx + 4, ry, x_max) + self.ROW
                c["px_y"] = ry + 3; body.append(("px", M + 12, ry + 3)); ry += 20
                pins = ", ".join(n for p, n in (("L", "left"), ("T", "top"), ("R", "right"), ("B", "bottom"),
                                                ("X", "centre"), ("Y", "middle")) if p in z.pins)
                body.append(("pins", "Pinned: " + (pins or "none"), M + 12, ry + 3)); ry += 28
                items = [("even", Kit.ART_PLAY, "Even out", "Give this zone and those flush beside it in its row (or "
                          "column) equal sizes")]
                if len(self.multi) >= 2:
                    items += [("al_" + e[0], Kit.ART_PLAY, "Align " + e,
                               "Line the picked zones' %s edges up with this zone's" % e)
                              for e in ("left", "top", "right", "bottom")]
                    items.append(("same", Kit.ART_PLAY, "Same size", "Make the picked zones this zone's size"))
                ops.append(("flow", items, M + 12, ry))
                ry = self._flow(None, None, items, M + 12, ry, x_max) + self.ROW
                if len(self.multi) >= 2:
                    body.append(("label", Kit.fit("%d zones picked (Shift+click picks more or fewer)"
                                                  % len(self.multi), IW - 24), M + 12, ry + 3, Kit.HUE_INFO))
                    ry += 20
            ZH = ry - y1 + 6; y2 = y1 + ZH + GAP; wins_rows = []; WH = 0
            if z is not None and z.kind == "w":
                wins_rows = list(L.assign.get(self.orig_id(z.id), []))
                was = self.pick_keys[self.pick] if 0 < self.pick < len(self.pick_keys) else None
                wl = L.all_windows(); self.pick_keys = [None] + [k for k, t in wl]
                self.pick = self.pick_keys.index(was) if was in self.pick_keys else 0
                if not self.pick: self.preview = ""; self.update_zone(z)
                WH = 30 + 28 + 26 * len(wins_rows) + (20 if self.preview else 0) + 14
                if not wins_rows: WH += 20
            y3 = y2 + (WH + GAP if WH else 0); cls = ratio_class(self.W, self.H)
            others = [k for k in ("narrow", "wide", "ultrawide") if k != cls]
            presets = [("undo", Kit.ART_PAGE, "Undo", "Undo the last change (Ctrl+Z)"),
                       ("redo", Kit.ART_PAGE, "Redo", "Redo the last undo (Ctrl+Y)"),
                       ("from_default", Kit.ART_PLAY, "New from Default", "Start again from the Default layout"),
                       ("mirror", Kit.ART_PLAY, "Mirror", "Swap the zones left and right"),
                       ("copyto", Kit.ART_OK, "Copy to others",
                        "Use these zones on %s and %s screens too (save them first)" % tuple(others))]
            if self.others is None or self.others[0] != (self.zs.name, cls):
                named = FRAMES_NAMED % self.zs.name
                self.others = ((self.zs.name, cls), [k for k in others if Kit.get_var(named + "@" + k, "")])
            saved_other = self.others[1]
            if saved_other:
                presets.append(("reflow", Kit.ART_PLAY, "Reflow from: " + saved_other[0],
                                "Rebuild from this layout's %s-screen version" % saved_other[0]))
                c["reflow_from"] = saved_other[0]
            prow = self._flow(None, None, presets, M + 12, 0, x_max); FH = 30 + 28 * 2 + prow + 20 * 3 + 10
            H = y3 + FH + M
            Kit.add_window_frame(g, W, H); Kit.add_section(g, M, M, IW, 30)
            Kit.add_label(g, "ZONES", M + 30, M + 7, Kit.HUE_TITLE)
            Kit.add_label(g, Kit.fit('frame layout "%s"' % self.zs.name, IW - 250),
                          M + 30 + Kit.text_w("ZONES") + 12, M + 7, Kit.HUE_INFO)
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, W - M - 54, M + 4, None,
                           "Close the editor and bring back the saved zones")
            Kit.add_section(g, M, y1, IW, ZH, "ZONE  (selected)"); boxes = []
            for item in body:
                if item[0] == "label": Kit.add_label(g, item[1], item[2], item[3], item[4])
                elif item[0] == "box":
                    key, text, bx, by, bw_, num, tip = item[1:]
                    c[key] = Kit.with_tip(Kit.add_textbox(g, text, bx, by, bw_, numbers=num), tip); boxes.append(key)
                elif item[0] == "px":
                    c["px"] = Kit.add_label(g, "", item[1], item[2], Kit.HUE_INFO); c["px_x"] = item[1]
                elif item[0] == "pins":
                    Kit.with_tip(Kit.add_label(g, item[1], item[2], item[3], Kit.HUE_INFO),
                                 "Edges kept on the screen's edge (or centre line) on other screen sizes")
            for op in ops: self._flow(g, store, op[1], op[2], op[3], x_max)
            if WH:
                Kit.add_section(g, M, y2, IW, WH, "WINDOWS  (in this zone, top to bottom)"); ry = y2 + 32
                Kit.add_label(g, "Window:", M + 12, ry + 3); dd_x = M + 12 + Kit.text_w("Window:") + 8; dd_w = 300
                bx = dd_x + dd_w + 16
                Kit.art_button(g, store, "w_add", Kit.ART_OK, bx, ry - 2, "Put it here",
                               "Put the picked window in this zone (no Arrange mode needed)")
                ry += 28
                if not wins_rows:
                    Kit.add_label(g, "Pick a window above, then click Put it here.", M + 12, ry + 3, Kit.HUE_INFO)
                    ry += 20
                for i, k in enumerate(wins_rows):
                    Kit.add_label(g, Kit.fit(L.title_of(k), 300), M + 12, ry + 3)
                    self._flow(g, store, [("w_%s_%d" % (w_, i), art, cap, tip % L.title_of(k))
                                          for w_, art, cap, tip in (
                        ("up", Kit.ART_PAGE, "Up", "Move %s up the zone's stack"),
                        ("down", Kit.ART_PAGE, "Down", "Move %s down the zone's stack"),
                        ("out", Kit.ART_CLOSE, "Take out", "Free %s from the zone (it stays where it is)"))],
                        M + 12 + 310, ry, 1 << 30)
                    ry += 26
                c["wins_rows"] = wins_rows
                if self.preview:
                    Kit.add_label(g, Kit.fit(self.preview.lstrip("!"), IW - 24), M + 12, ry + 3,
                                  Kit.HUE_BAD if self.preview.startswith("!") else Kit.HUE_INFO)
            Kit.add_section(g, M, y3, IW, FH, "FRAME LAYOUT"); ry = y3 + 32; x = M + 12
            for key, art, cap, tip in (("add", Kit.ART_OK, "Add zone", "Add a zone mid-screen to drag into place"),
                                       ("fill", Kit.ART_PLAY, "Fill the gaps",
                                        "Grow every zone into empty room beside it"), ("save", Kit.ART_OK, "Save",
                                        "Save as the frame layout in use (Default saves as Default (mine))"),
                                       ("saveas", Kit.ART_OK, "Save as", "Save under the name in the box")):
                Kit.art_button(g, store, key, art, x, ry - 2, cap, tip); x += self._cap_w(cap) + 16
            c["saveas"] = Kit.with_tip(Kit.add_textbox(g, self.saveas_text, x, ry, max(
                60, W - M - 12 - self._cap_w("Discard") - 16 - x), numbers=False),
                "A name for Save as (letters, digits, spaces)")
            cap = "Discard"
            Kit.art_button(g, store, "discard", Kit.ART_CLOSE, W - M - 12 - self._cap_w(cap), ry - 2,
                           cap, "Close the editor and bring back the saved zones")
            ry += 28; ry = self._flow(g, store, presets, M + 12, ry, x_max) + 28; n = len(self.zs.zones)
            nk = sum(1 for zz in self.zs.zones if zz.kind == "k"); nr = sum(1 for zz in self.zs.zones if zz.kind == "r")
            gaps, over = self.counts
            status = "%s, %d keep clear, %d reserved; %s, %s; %d x %d, %s" % (
                Kit.count(n, "zone"), nk, nr, Kit.count(gaps, "gap"), Kit.count(over, "overlap"), self.W, self.H, cls)
            Kit.add_label(g, Kit.fit(status, IW - 24), M + 12, ry + 3, Kit.HUE_BAD if (gaps or over) else Kit.HUE_INFO)
            ry += 20; lx = M + 12
            for col, name in ((ZONE_COLORS["w"], "window"), (ZONE_COLORS["k"], "keep clear"),
                              (ZONE_COLORS["r"], "reserved"), ("#C83030", "gap or overlap"),
                              ("#E8C15A", "overlap allowed")):
                Kit.add_box(g, lx, ry + 6, 12, 12, 0.9, col); Kit.add_label(g, name, lx + 16, ry + 3, Kit.HUE_INFO)
                lx += 16 + Kit.text_w(name) + 14
            ry += 20
            Kit.add_label(g, Kit.fit("Mouse on the zone: arrows nudge it a square; Shift+arrows resize "
                                     "it; Delete twice removes it.", IW - 24), M + 12, ry + 3, Kit.HUE_INFO)
            if WH:
                names = ["(pick a window)"]
                for k, t in wl:
                    zid = L.zone_of(k); names.append(Kit.fit(t + (' (in "%s")' % zid if zid else ""), 290))
                dd = G.CreateDropDown(dd_w, names, self.pick); dd.SetPos(dd_x, y2 + 32); g.Add(dd)
                c["w_pick"] = Kit.with_tip(dd, "A window for this zone; the zone shows where it would sit")
            ax, ay = Kit.anchor_pos("B", W, H)
            if Kit.is_open(old): x, y = old.GetX(), old.GetY()
            else: x, y = self.bar_pos or Kit.load_pos(EDITOR_POS, (ax or 200, ay or 200), (W, H))
            Kit.place(g, x, y, W, H); Kit.add_front(g); Kit.on_moved(g, self._bar_moved)
            self.bar, self.store, self.c = g, store, c; self.raws = {}
            for key in boxes + ["saveas"]:
                raw = Kit.client_control(c[key]) if key in c else None
                if raw is not None: self.raws[key] = raw
            self.fields = None; self.focus_was = None; self.show_fields(); Kit.dispose(old)
        def _bar_moved(self): Kit.save_pos(EDITOR_POS, self.bar); self.bar_pos = Snap.pos(self.bar)
        def _values(self, z):
            x, y, w, h = z.px
            if self.px_mode: return tuple(str(v) for v in (x, y, w, h))
            step = HOST.grid_size()
            return tuple(str(v) for v in (int(round(float(x) / step)), int(round(float(y) / step)),
                                          max(1, int(round(float(w) / step))), max(1, int(round(float(h) / step)))))
        def show_fields(self):
            c = self.c; z = self.zs.by_id(self.sel) if self.sel else None
            if z is None or "col" not in c: return
            texts = self._values(z)
            if texts != self.fields:
                self.fields = texts
                for key, t in zip(self.FIELDS, texts): c[key].SetText(t)
            x, y, w, h = z.px
            if self.px_mode:
                step = HOST.grid_size()
                text = "%d x %d squares at square %d, %d" % (
                    max(1, int(round(float(w) / step))), max(1, int(round(float(h) / step))),
                    int(round(float(x) / step)), int(round(float(y) / step)))
            else: text = "%d x %d px at %d, %d" % (w, h, x, y)
            Kit.set_text(c["px"], Kit.fit(text, self.BAR_W - Kit.MARGIN - 12 - c["px_x"]))
        def _over(self, z):
            m = Kit.mouse_pos()
            if m is None: return True
            for r in (Snap.rect(self.bar), tuple(z.px)):
                if r is not None and r[0] <= m[0] < r[0] + r[2] and r[1] <= m[1] < r[1] + r[3]: return True
            return False
        def _key(self, name):
            down = False
            for k in self.KEYS[name]:
                if API.IsKeyPressed(k): down = True; break
            was = self.keys_was.get(name, False); self.keys_was[name] = down; return down and not was
        def _focus(self):
            if not self.raws: return None
            try:
                Typing._find()
                f = (Typing._get(None, "KeyboardFocusControl", Typing.uim) if Typing.uim is not None else None)
            except Exception: f = None
            self.raws_ok = Typing.uim is not None; n = 0
            while f is not None and n < 4:
                for key, raw in self.raws.items():
                    if Typing._same(f, raw): return key
                f = Typing._get(f, "Parent"); n += 1
            return None
        def _box_texts(self):
            c = self.c
            try: return tuple(str(c[k].Text or "").strip() for k in self.FIELDS)
            except Exception: return None
        def poll(self):
            if self.closed: return
            if not Kit.is_open(self.bar): self.close(keep=False); return
            now = time.time()
            for zid, fr in list(self.frames.items()):
                z = self.zs.by_id(zid); g = fr.get("g")
                if z is None or not Kit.is_open(g): continue
                if fr["resize_at"]:
                    r = Snap.rect(g)
                    if r is not None and (r[2], r[3]) != fr["size"]:
                        step = HOST.grid_size()
                        Kit.set_text(fr["sum"], Kit.fit("%d x %d squares" % (max(1, int(round(float(r[2]) / step))),
                                                                             max(1, int(round(float(r[3]) / step)))),
                                                        max(40, r[2] - 2 * Kit.MARGIN - 24)), Kit.HUE_TITLE)
                    if now - fr["resize_at"] >= self.SETTLE:
                        fr["resize_at"] = 0.0
                        if r is not None and (r[2], r[3]) != fr["size"]:
                            if z.lock: self.build_zone(z)
                            else: self.landed(z, r[0], r[1], r[2], r[3], resized=True)
            pressed = SNAP.pressed() is True; self._sync_handles(); self._edge_tick(pressed); self.pressed_was = pressed
            store, c = self.store, self.c; z = self.zs.by_id(self.sel) if self.sel else None
            if Kit.was_clicked(store, "close") or Kit.was_clicked(store, "discard"): self.close(keep=False); return
            focus = self._focus(); typing = Client.typing(); enter = self._key("enter")
            esc = self._key("esc")
            if not typing and not self.edge:
                ctrl = bool(Client.key_held("ctrl")); shift = bool(Client.key_held("shift"))
                if self._key("z") and ctrl: self.do_undo()
                elif self._key("y") and ctrl: self.do_redo()
                elif z is not None:
                    for name, d in (("left", (-1, 0)), ("right", (1, 0)), ("up", (0, -1)), ("down", (0, 1))):
                        if self._key(name) and self._over(z): self.nudge(z, d, shift)
                    if self._key("delete") and self._over(z): self.delete_pressed(z)
            if Kit.was_clicked(store, "add"):
                self.push(); zid = self.new_id(); nz = Zone(zid, "w", (0, 0, 1, 1), "", (0, 0), "d", 0)
                nz.set_px((self.W - 320) // 2, (self.H - 240) // 2, 320, 240, self.W, self.H)
                if not self._add_zone(nz, True, "no room for another zone; remove one or make one smaller."): return
            elif Kit.was_clicked(store, "undo"): self.do_undo()
            elif Kit.was_clicked(store, "redo"): self.do_redo()
            elif Kit.was_clicked(store, "even") and z is not None:
                was = [(zz, zz.px, zz.rect, zz.exact) for zz in self.zs.zones]; self.push()
                n = self.zs.even_out(z, self.W, self.H, HOST.grid_size())
                hit = [zz for zz, p, r, e in was if zz.lock and zz.px != p]
                if n < 2 or hit:
                    self.undo.pop()
                    for zz, p, r, e in was: zz.px, zz.rect, zz.exact = p, r, e
                    if hit: self.say('zone "%s" is locked; click Lock to change it.' % hit[0].id, Kit.HUE_INFO)
                    else: self.say("no zone sits flush beside this one in its row or column.")
                else: self._all_moved()
            elif Kit.was_clicked(store, "fill"):
                self.push(); self.zs.fill_gaps(self.W, self.H, HOST.grid_size()); self._all_moved()
            elif Kit.was_clicked(store, "save"):
                self.save(self.zs.name if self.zs.name != LAYOUT_DEFAULT else LAYOUT_MINE); return
            elif Kit.was_clicked(store, "saveas"):
                name = Layout.clean_name(safe(lambda: c["saveas"].Text, ""), "")
                if not name: self.say("type a name in the box, then click Save as.")
                else: self.save(name if name != LAYOUT_DEFAULT else LAYOUT_MINE); return
            elif Kit.was_clicked(store, "reflow") and c.get("reflow_from"):
                other = ZoneSet.parse(self.zs.name,
                                      Kit.get_var((FRAMES_NAMED % self.zs.name) + "@" + c["reflow_from"], ""))
                if other is not None:
                    other.reflow(self.W, self.H, HOST.grid_size()); self.push()
                    self._restore(([zz.copy() for zz in other.zones], self.sel, {})); self.changed()
            elif Kit.was_clicked(store, "from_default"):
                self.push(); d = ZoneSet.default(self.W, self.H, (), False)
                self._restore(([zz.copy() for zz in d.zones], self.sel, {})); self.changed()
            elif Kit.was_clicked(store, "mirror"):
                self.push()
                for zz in self.zs.zones:
                    x, y, w, h = zz.px; zz.set_px(self.W - x - w, y, w, h, self.W, self.H)
                self._all_moved()
            elif Kit.was_clicked(store, "copyto"): self.copy_to()
            elif Kit.was_clicked(store, "units"):
                self.commit_rect(z, quiet=True) if z is not None else None; self.px_mode = not self.px_mode
                self.rebuild = True
            if z is not None and not self.rebuild: self.poll_zone(z, store)
            if z is not None and z.kind == "w" and not self.rebuild: self.poll_windows(z, store, c)
            if not self.rebuild: self.poll_fields(z, focus, enter, esc, Kit.was_clicked(store, "apply"))
            self.focus_was = focus; self.draw_marks()
            if self.rebuild:
                self.rebuild = False; self.saveas_text = str(safe(lambda: c["saveas"].Text, self.saveas_text) or "")
                for zz in self.zs.zones: self.update_zone(zz)
                self.build_bar()
        def _all_moved(self):
            for zz in self.zs.zones: zz.note_pins(self.W, self.H); self.place_zone(zz)
            self.changed()
        def poll_zone(self, z, store):
            if Kit.was_clicked(store, "kind"):
                self.push(); kinds = [k for k, n in ZONE_KINDS]; z.kind = kinds[(kinds.index(z.kind) + 1) % len(kinds)]
                z.hug = z.hug and z.kind == "w"; self.build_zone(z); self.changed()
                self.rebuild = True
            elif Kit.was_clicked(store, "stack"):
                self.push(); stacks = [k for k, n in ZONE_STACKS]
                z.stack = stacks[(stacks.index(z.stack) + 1) % len(stacks)]; self.build_zone(z); self.rebuild = True
            elif Kit.was_clicked(store, "prio"):
                self.push(); z.prio = (z.prio + 1) % (SHRINK_MAX + 1); self.rebuild = True
            elif Kit.was_clicked(store, "overlap"):
                self.push(); z.overlap = not z.overlap
                if not z.overlap:
                    if not self.zs.push_clear(z, self.W, self.H, HOST.grid_size()):
                        o = self._blocker(z)
                        self.say('zone "%s" still lies over "%s"; move it or make it smaller.'
                                 % (z.id, o.id if o is not None else "a zone"), Kit.HUE_INFO)
                    z.note_pins(self.W, self.H)
                for zz in self.zs.zones: self.build_zone(zz)
                self.changed(); self.rebuild = True
            elif Kit.was_clicked(store, "lock"):
                self.push(); z.lock = not z.lock; self.build_zone(z); self.rebuild = True
            elif Kit.was_clicked(store, "split"): self.split(z)
            elif Kit.was_clicked(store, "join"): self.join(z)
            elif Kit.was_clicked(store, "solo"): self.push(); z.solo = not z.solo; self.changed(); self.rebuild = True
            elif Kit.was_clicked(store, "free"):
                self.push(); z.free = not z.free; self.px_mode = self.px_mode or z.free; z.note_pins(self.W, self.H)
                self.changed(); self.rebuild = True
            elif Kit.was_clicked(store, "dup"): self.duplicate(z)
            elif Kit.was_clicked(store, "remove"): self.remove(z)
            else:
                for key, edge in (("al_l", "l"), ("al_t", "t"), ("al_r", "r"), ("al_b", "b"), ("same", "s")):
                    if Kit.was_clicked(store, key): self.align(z, edge); break
        def poll_windows(self, z, store, c):
            L = self.layout; dd = c.get("w_pick"); now = time.time(); add = Kit.was_clicked(store, "w_add")
            if dd is not None and (now >= self._pick_next or now - HOST.input_at <= HOST.INPUT_FAST):
                self._pick_next = now + 0.2; i = Kit.dd_index(dd, self.pick)
                if i != self.pick:
                    self.pick = i; key = self.pick_keys[i] if 0 < i < len(self.pick_keys) else None
                    self.preview = self.preview_text(key, z) if key else ""; self.build_zone(z); self.rebuild = True
                    if not add: return
            zid = self.orig_id(z.id)
            if add:
                key = self.pick_keys[self.pick] if 0 < self.pick < len(self.pick_keys) else None
                if key is None:
                    self.say("pick a window in the list first, then click Put it here.", Kit.HUE_INFO); return
                sz = L.frames.by_id(zid) if L.frames is not None and self.zs.name == L.frames_name else None
                if sz is None:
                    self.say('zone "%s" isn\'t saved yet; click Save, then put the window in it.' % z.id); return
                if L.zone_of(key) == zid:
                    self.say("%s already sits in this zone." % L.title_of(key), Kit.HUE_INFO); return
                mz = L._map_zone()
                if (key != "worldmap" and zid == mz) or (key == "worldmap" and L.assign.get(zid)):
                    self.say("TazUO's World Map keeps its zone to itself; pick another zone for %s."
                             % (L.title_of(key) if key != "worldmap" else "it"))
                    return
                if L._too_small(key, z): return
                if L._too_small(key, sz, say=False):
                    if tuple(self.start_px.get(zid, (0, 0, 0, 0))[2:]) == tuple(z.px[2:]): L._too_small(key, sz); return
                    self.say('zone "%s" isn\'t saved at this size yet; click Save, then put the window in it.' % z.id)
                    return
                old = L.zone_of(key); L.assign_to(key, zid); self.pick, self.preview = 0, ""; self.build_zone(z)
                for zz in self.zs.zones:
                    if zz is not z and self.orig_id(zz.id) == old: self.build_zone(zz)
                self.rebuild = True; return
            rows = c.get("wins_rows") or []
            for i, k in enumerate(rows):
                for what in ("up", "down", "out"):
                    if not Kit.was_clicked(store, "w_%s_%d" % (what, i)): continue
                    keys = L.assign.get(zid, [])
                    if k not in keys: break
                    if what == "out": L.assign_to(k, None)
                    else:
                        j = keys.index(k); t = j - 1 if what == "up" else j + 1
                        if 0 <= t < len(keys):
                            keys[j], keys[t] = keys[t], keys[j]
                            for kk in keys: L._refit(kk)
                            L.save_assign(); L.dirty = L.fresh = True; HOST.poke()
                    self.build_zone(z); self.rebuild = True; return
        def preview_text(self, key, z):
            return self.layout.preview_text(key, z, self.layout.assign.get(self.orig_id(z.id), []))
        def poll_fields(self, z, focus, enter, esc, apply):
            c = self.c
            if z is None or "name" not in c: return
            left = self.focus_was if (self.focus_was is not None and focus != self.focus_was) else None
            if esc and (focus is not None or self._edited(z)): self._refields(); c["name"].SetText(z.id); return
            if (enter and focus == "name") or left == "name" or apply:
                name = str(safe(lambda: c["name"].Text, z.id) or "").strip()
                if name != z.id: self.rename(z, name); return
            if focus is None and left is None and enter and not self.raws_ok:
                name = str(safe(lambda: c["name"].Text, z.id) or "").strip()
                if name != z.id: self.rename(z, name); return
                self.commit_rect(z); return
            if ((enter and focus in self.FIELDS) or (left in self.FIELDS and focus not in self.FIELDS) or apply):
                self.commit_rect(z)
        def _edited(self, z):
            texts = self._box_texts(); name = str(safe(lambda: self.c["name"].Text, z.id) or "").strip()
            return (texts is not None and texts != self._values(z)) or name != z.id
        def commit_rect(self, z, quiet=False):
            texts = self._box_texts(); vals = self._values(z)
            if texts is None or texts == vals: return
            try: nums = [int(t) for t in texts]
            except Exception:
                if not quiet: self.say("type whole numbers in Col, Row, W and H.")
                self._refields(); return
            step = 1 if self.px_mode else HOST.grid_size(); W, H = self.W, self.H
            raw = tuple(z.px[i] if texts[i] == vals[i] else max(1 if i > 1 else 0, nums[i]) * step for i in range(4))
            x, y, w, h = raw
            if not self.px_mode and not z.free:
                if W - SNAP_DIST <= x + w < W + step: w = W - x
                if H - SNAP_DIST <= y + h < H + step: h = H - y
                if (x, y, w, h) == tuple(z.px): x, y, w, h = raw
            typed = "%d x %d %s" % (max(1, int(texts[2])), max(1, int(texts[3])), "px" if self.px_mode else "squares")
            if w < ZONE_MIN_W or h < ZONE_MIN_H:
                if not quiet:
                    self.say('zone "%s" can\'t be %s: the smallest zone is %d x %d px.' % (
                        z.id, typed, ZONE_MIN_W, ZONE_MIN_H))
                self._refields(); return
            if z.lock:
                self.say('zone "%s" is locked; click Lock to change it.' % z.id, Kit.HUE_INFO); self._refields(); return
            if not self.apply_rect(z, x, y, w, h, typed): self._refields()
        def rename(self, z, name):
            name = Layout.clean_name(name, "")
            if not name or name.lower() == "frames" or self.zs.by_id(name) is not None:
                self.say('zone "%s" can\'t be called "%s": %s.' % (
                    z.id, name, "a name needs letters or digits" if not name else
                    "the name is taken" if self.zs.by_id(name) is not None else "that name is kept"))
                self.c["name"].SetText(z.id); return
            self.push(); old = z.id; z.id = name
            for k, v in self.renames.items():
                if v == old: self.renames[k] = name; break
            else: self.renames[old] = name
            fr = self.frames.pop(old, None)
            if fr is not None: self.frames[name] = fr
            self.sel = name; self.multi = set(name if m == old else m for m in self.multi); self.said = None
            self.build_zone(z); self.rebuild = True
        def nudge(self, z, d, resize):
            if z.lock: self.say('zone "%s" is locked; click Lock to change it.' % z.id, Kit.HUE_INFO); return
            step = 1 if z.free else HOST.grid_size(); x, y, w, h = z.px
            if resize: self.apply_rect(z, x, y, max(ZONE_MIN_W, w + d[0] * step), max(ZONE_MIN_H, h + d[1] * step))
            else: self.apply_rect(z, x + d[0] * step, y + d[1] * step, w, h)
        def delete_pressed(self, z):
            now = time.time()
            if (self.del_armed is not None and self.del_armed[0] == z.id and now - self.del_armed[1] <= 3.0):
                self.del_armed = None; self.remove(z); return
            self.del_armed = (z.id, now); Kit.say('press Delete again to remove zone "%s".' % z.id, Kit.HUE_INFO)
        def remove(self, z):
            if z.lock: self.say('zone "%s" is locked; click Lock to remove it.' % z.id, Kit.HUE_INFO); return
            self.push(); self.zs.zones = [zz for zz in self.zs.zones if zz is not z]; fr = self.frames.pop(z.id, None)
            if fr is not None: Kit.dispose(fr.get("g"))
            self.multi.discard(z.id); self.sel = self.zs.zones[0].id if self.zs.zones else None; self.pick = 0
            self.preview = ""; self.changed(); self.rebuild = True
        def split(self, z):
            if z.lock: self.say('zone "%s" is locked; click Lock to change it.' % z.id, Kit.HUE_INFO); return
            x, y, w, h = z.px; wide = w >= h; size = w if wide else h; least = ZONE_MIN_W if wide else ZONE_MIN_H
            step = HOST.grid_size(); half = int(round(size / 2.0 / step)) * step
            if not least <= half <= size - least: half = size // 2
            if half < least or size - half < least: self.say('zone "%s" is too small to split.' % z.id); return
            self.push(); nz = z.copy(); nz.id = self.new_id(); W, H = self.W, self.H
            if wide: z.set_px(x, y, half, h, W, H); nz.set_px(x + half, y, w - half, h, W, H)
            else: z.set_px(x, y, w, half, W, H); nz.set_px(x, y + half, w, h - half, W, H)
            z.note_pins(W, H); nz.note_pins(W, H); self.zs.zones.append(nz); self.build_zone(z); self.build_zone(nz)
            self.changed(); self.rebuild = True
        def join(self, z):
            if z.lock: self.say('zone "%s" is locked; click Lock to change it.' % z.id, Kit.HUE_INFO); return
            x, y, w, h = z.px; D = SNAP_DIST; mate = None
            for o in self.zs.zones:
                if o is z or o.px is None or o.lock or o.kind != z.kind: continue
                ox, oy, ow, oh = o.px
                if abs(oy - y) <= D and abs(oh - h) <= D and (abs(ox - (x + w)) <= D or abs(x - (ox + ow)) <= D):
                    mate = o
                elif abs(ox - x) <= D and abs(ow - w) <= D and (abs(oy - (y + h)) <= D or abs(y - (oy + oh)) <= D):
                    mate = o
                if mate is not None: break
            if mate is None: self.say('no zone of the same height or width sits flush beside "%s".' % z.id); return
            self.push(); ox, oy, ow, oh = mate.px; x0, y0 = min(x, ox), min(y, oy)
            z.set_px(x0, y0, max(x + w, ox + ow) - x0, max(y + h, oy + oh) - y0, self.W, self.H)
            z.note_pins(self.W, self.H)
            self.zs.zones = [zz for zz in self.zs.zones if zz is not mate]; fr = self.frames.pop(mate.id, None)
            if fr is not None: Kit.dispose(fr.get("g"))
            self.multi.discard(mate.id); self.build_zone(z); self.changed(); self.rebuild = True
            self.say('zone "%s" joined into "%s"; its windows become free when saved.' % (mate.id, z.id), Kit.HUE_INFO)
        def _add_zone(self, nz, check, text):
            self.zs.zones.append(nz)
            if check and not self.zs.push_clear(nz, self.W, self.H, HOST.grid_size()):
                self.zs.zones.remove(nz); self.undo.pop(); self.say(text); return False
            nz.note_pins(self.W, self.H); self.sel, self.multi, self.pick, self.preview = nz.id, set(), 0, ""
            self.build_zone(nz); self.changed()
            self.rebuild = True; return True
        def duplicate(self, z):
            self.push(); nz = z.copy(); nz.id = self.new_id(); nz.lock = False; step = HOST.grid_size()
            x, y, w, h = z.px; nz.set_px(x + step, y + step, w, h, self.W, self.H)
            self._add_zone(nz, not nz.overlap, "no room for a copy of zone \"%s\"; make room first." % z.id)
        def align(self, z, edge):
            picked = [p for p in [self.zs.by_id(i) for i in self.multi if i != z.id] if p is not None and not p.lock]
            if not picked: return
            self.push(); x, y, w, h = z.px; refused = []
            for p in picked:
                px, py, pw, ph = p.px
                r = {"l": (x, py, pw, ph), "t": (px, y, pw, ph), "r": (x + w - pw, py, pw, ph),
                     "b": (px, y + h - ph, pw, ph)}.get(edge, (px, py, w, h))
                was = p.px; p.set_px(r[0], r[1], r[2], r[3], self.W, self.H)
                if self._blocker(p) is not None:
                    p.set_px(was[0], was[1], was[2], was[3], self.W, self.H); refused.append(p.id)
                p.note_pins(self.W, self.H)
            if refused:
                self.say("%s would cover another zone, so %s stayed where %s %s." % (
                    ", ".join('"%s"' % r for r in refused), "it" if len(refused) == 1 else "they",
                    "it" if len(refused) == 1 else "they", "was" if len(refused) == 1 else "were"), Kit.HUE_INFO)
            self._all_moved()
        def copy_to(self):
            name = self.zs.name; self.others = None
            if self.zs.generated or name == LAYOUT_DEFAULT or name not in self.layout.frame_names():
                self.say("save these zones first (Save or Save as), then click Copy to.", Kit.HUE_INFO); return
            cls = ratio_class(self.W, self.H); zs = self.zs.copy(name); zs.screen = (self.W, self.H)
            zs.grid = HOST.grid_size()
            for zz in zs.zones: zz.note_pins(self.W, self.H)
            text = zs.save_text(); others = [k for k in ("narrow", "wide", "ultrawide") if k != cls]
            for k in others: Kit.put_var((FRAMES_NAMED % name) + "@" + k, text)
            Kit.say('frame layout "%s" copied to %s screens.' % (name, " and ".join(others)), Kit.HUE_GOOD)
        def warnings(self):
            out = []; L = self.layout
            for z in self.zs.zones:
                if z.kind != "w" or z.px is None: continue
                b = Layout._body(z)
                for k in L.assign.get(self.orig_id(z.id), []):
                    mn = L._min_at(k, b[2], b[3])
                    if mn and (b[2] < mn[0] or b[3] < mn[1]):
                        out.append('zone "%s" has room for %d x %d; %s needs %d x %d' % (
                            z.id, b[2], b[3], L.title_of(k), mn[0], mn[1]))
            gaps, over = self.counts
            if gaps: out.append("the zones leave %s (Fill the gaps closes them)" % Kit.count(gaps, "gap"))
            if over: out.append("%s of zones without Overlap on" % Kit.count(over, "overlap"))
            if not any(z.kind == "k" for z in self.zs.zones):
                out.append("no keep-clear zone: nothing marks the game view")
            return out
        def save(self, name):
            self.others = None
            for w in self.warnings(): Kit.say("note: %s." % w, Kit.HUE_INFO)
            zs = self.zs.copy(name); zs.generated = False; zs.ver = 2; self.layout.save_frames(zs, name, self.W, self.H)
            L = self.layout; old = dict(L.assign); moves = [(a, b) for a, b in self.renames.items() if a != b]
            def moved(a):
                out = dict(a)
                for was, now in moves: out.pop(was, None)
                for was, now in moves:
                    if was in a: out[now] = a[was]
                    else: out.pop(now, None)
                return out
            L.assign.clear(); L.assign.update(moved(old))
            if L.assign != old: L.save_assign()
            tabs = moved(L.tabs)
            if tabs != L.tabs: L.tabs = tabs; L._tabs_save()
            if moves and name == self.zs.name:
                for n in L.layout_names():
                    f, a = L.parse_windows(Kit.get_var(LAYOUT_NAMED % n, ""))
                    if f == name and moved(a) != a: Kit.put_var(LAYOUT_NAMED % n, L.windows_text(f, moved(a)))
                b = L.situ_back
                if b is not None and b[1] == name: L.situ_back = b[:2] + (moved(b[2]),) + tuple(b[3:])
            Kit.say('frame layout "%s" saved.' % name, Kit.HUE_GOOD); self.close(keep=True)
            self.layout.use_frames(name, tell=False)
    def editor_closed(): st["editor"] = None
    def edit(fresh=False):
        L = LAYOUT; W, H = Kit.screen()
        if st["editor"] is not None or W <= 0 or H <= 0 or not L.enabled: return
        if fresh:
            names = L.frame_names(); n, name = 2, "Mine"
            while name in names or name == LAYOUT_DEFAULT: name = "Mine %d" % n; n += 1
            zs = ZoneSet(name, [], HOST.grid_size(), (W, H)); z = Zone("Zone 1", "w", (0, 0, 1, 1), "", (0, 0), "d", 0)
            z.set_px((W - 320) // 2, (H - 240) // 2, 320, 240, W, H); zs.zones.append(z)
        elif L.frames_name == LAYOUT_DEFAULT: zs = ZoneSet.default(W, H, L.occupied(), False); zs.generated = False
        else: zs = L.load_frames(L.frames_name, W, H) or L.frames_in_use(W, H).copy()
        st["editor"] = LayoutEditor(L, zs, editor_closed); st["editor"].open()
    def backdrop_items():
        L = LAYOUT; zs = L.frames
        if zs is None or not (L.seamless and L.enabled) or st["editor"] is not None: return (), None
        gp = Layout._game_px(zs)
        def clear(r): return gp is None or not (r[0] < gp[0] + gp[2] and gp[0] < r[0] + r[2] and r[1] < gp[1] + gp[3]
                                                 and gp[1] < r[1] + r[3])
        items = tuple((tuple(z.px), z.solo) for z in zs.zones if z.kind != "k" and z.px is not None and clear(z.px))
        return items, gp if L.fit_view else None
    def draw_backdrop(items, gp, W, H):
        g = G.CreateGump(False, False); base = Kit.WINDOW_BG; P = [Kit.pic_size(base + i) for i in range(9)]
        rects = [it[0] for it in items]; cover = [{"T": [], "B": [], "L": [], "R": []} for _ in rects]
        def solid(x, y, w, h):
            Kit.add_tiled(g, base + 4, x, y, w, h); b = Kit.add_box(g, x, y, w, h, 0.01, "#000000")
            if b is not None: b.SetAcceptMouseInput(True)
        for x, y, w, h in rects: solid(x, y, w, h)
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                s = None if items[i][1] or items[j][1] else touch(rects[i], rects[j])
                if s is None: continue
                o, lo, hi, a, b = s; k = 0 if o == "v" else 1
                near, far = (i, j) if rects[i][k] < rects[j][k] else (j, i)
                cover[near]["R" if o == "v" else "B"].append((a, b))
                cover[far]["L" if o == "v" else "T"].append((a, b))
                if hi > lo: solid(*((lo, a, hi - lo, b - a) if o == "v" else (a, lo, b - a, hi - lo)))
        for i, (x, y, w, h) in enumerate(rects):
            for sd, art, s0, s1, fx in (("T", 1, x, x + w, lambda a, b: (a, y, b - a, P[1][1])),
                                        ("B", 7, x, x + w, lambda a, b: (a, y + h - P[7][1], b - a, P[7][1])),
                                        ("L", 3, y, y + h, lambda a, b: (x, a, P[3][0], b - a)),
                                        ("R", 5, y, y + h, lambda a, b: (x + w - P[5][0], a, P[5][0], b - a))):
                for a, b in gaps_of(s0, s1, cover[i][sd]): Kit.add_tiled(g, base + art, *fx(a, b))
        Grid.show_overlay(g, 0, 0, W, H, True); back["g"] = g
        if gp is None or gp[2] <= 2 * RING or gp[3] <= 2 * RING: return
        r = G.CreateGump(False, False); x, y, w, h = gp
        for bx, by, bw, bh, col in ((0, 0, w, RING, RING_GOLD), (0, h - RING, w, RING, RING_GOLD),
                                    (0, 0, RING, h, RING_GOLD), (w - RING, 0, RING, h, RING_GOLD),
                                    (RING, RING, w - 2 * RING, 1, RING_DARK),
                                    (RING, h - RING - 1, w - 2 * RING, 1, RING_DARK),
                                    (RING, RING, 1, h - 2 * RING, RING_DARK),
                                    (w - RING - 1, RING, 1, h - 2 * RING, RING_DARK)):
            Kit.add_box(r, bx, by, bw, bh, 1.0, col)
        Grid.show_overlay(r, x, y, w, h); ring["g"] = r
    def sink():
        raw = Kit._raw_gump(back["g"]) if back["g"] is not None and not sinker["off"] else None
        if raw is None or not Client.on_client_thread(): return
        try:
            gumps = sinker["gumps"]
            if gumps is None:
                import System; t = Tz.T("ClassicUO.Game.Managers.UIManager")
                sinker["same"] = System.Object.ReferenceEquals
                sinker["ver"] = t.GetField("_gumpsStructureVersion", Client.flags(static=True, public=False))
                gumps = sinker["gumps"] = Tz.get(None, "Gumps", t)
            ver = sinker["ver"]; cur = int(ver.GetValue(None)) if ver is not None else None
            if cur is not None and cur == sinker["seen"] and raw is sinker["raw"]: return
            sinker["seen"], sinker["raw"] = cur, raw; last = gumps.Last; same = sinker["same"]
            if last is None or same(last.Value, raw) or (last.Previous is not None and same(last.Previous.Value, raw)):
                return
            node = gumps.Find(raw)
            if node is None: return
            gumps.Remove(node); gumps.AddBefore(gumps.Last, node)
            if ver is not None: ver.SetValue(None, cur + 1); sinker["seen"] = cur + 1
        except Exception: sinker["off"] = True
    def backdrop_tick(now):
        if now < st["back_at"]: return
        st["back_at"] = now + BACK_EVERY; W, H = Kit.screen(); items, gp = backdrop_items()
        sig = (W, H, items, gp, Kit.look())
        if sig == st["back_sig"] and (not items or (Kit.is_open(back["g"]) and (gp is None or Kit.is_open(ring["g"])))):
            return
        st["back_sig"] = sig; old, back["g"] = back["g"], None; old_r, ring["g"] = ring["g"], None
        if items and W > 0 and H > 0: draw_backdrop(items, gp, W, H)
        Kit.dispose(old); Kit.dispose(old_r)
    def role_of(key):
        for pre, role in ROLES:
            if key == pre or (pre.endswith(".") and key.startswith(pre)): return role
        return None
    def cut(total, shares):
        out, at = [], 0
        for i, sh in enumerate(shares):
            n = total - at if i == len(shares) - 1 else int(round(total * sh)); out.append((at, n)); at += n
        return out
    def custom_zones(i, W, H):
        t = int(_clampv(STRIP_SHARE * H, TOP_MIN, TOP_MAX)); b = int(_clampv(STRIP_SHARE * H, BOT_MIN, BOT_MAX))
        if i == 2:
            band = int(_clampv(0.30 * H, 200, 340))
            spec = [("Frames", "w", 0, 0, W, t, "r", "frames"), ("Game", "k", 0, t, W, H - t - band, "d", None)]
            names = (("Paperdoll", "gear"), ("Bags", "bag"), ("Action bar", "bar"), ("Trackers", "watch"),
                     ("Map", "map"))
            spec += [(nm, "w", x, H - band, w, band, "d", role)
                     for (x, w), (nm, role) in zip(cut(W, (0.18, 0.18, 0.28, 0.18, 0.18)), names)]
        else:
            col = int(_clampv(0.24 * W, 260, 460)) if i == 3 else int(_clampv(SIDE_SHARE * W, SIDE_MIN, SIDE_MAX))
            cx, gx = (W - col, 0) if i == 3 else (0, col)
            spec = [("Game", "k", gx, 0, W - col, H - b, "d", None),
                    ("Action bar", "w", gx, H - b, W - col, b, "r", "bar")]
            names = (("Frames", "frames"), ("Paperdoll", "gear"), ("Bags", "bag"), ("Trackers", "watch"))
            spec += [(nm, "w", cx, y, col, h, "d", role)
                     for (y, h), (nm, role) in zip(cut(H, (0.22, 0.26, 0.26, 0.26)), names)]
        zs = ZoneSet(PRESETS[i][0], [], HOST.grid_size(), (W, H)); roles = {}
        for zid, kind, x, y, w, h, stack, role in spec:
            z = Zone(zid, kind, (0, 0, 1, 1), "", (0, 0), stack, 0); z.set_px(x, y, w, h, W, H); z.note_pins(W, H)
            zs.zones.append(z)
            if role: roles[role] = zid
        return zs, roles
    def plan_of(i, W, H):
        L = LAYOUT; std = L.parse_windows(WINDOWS_DEFAULT)[1]
        if i < 2:
            assign = std if i == 0 else L.parse_windows(WINDOWS_MIRRORED)[1]
            occ = set(zid for zid, ks in assign.items() if any(L.gump_of(k) is not None for k in ks))
            return ZoneSet.default(W, H, occ, setup["look"].get("game", True)), LAYOUT_DEFAULT, assign
        zs, roles = custom_zones(i, W, H); assign = {}
        for k in sorted(set(L.wins) | set(k for ks in std.values() for k in ks)):
            zid = roles.get(role_of(k))
            if zid: assign.setdefault(zid, []).append(k)
        return zs, PRESETS[i][0], assign
    def card_zones(i, W, H):
        ck = (i, W, H, setup["look"].get("game", True)); zs = setup["cards"].get(ck)
        if zs is None: zs = setup["cards"][ck] = plan_of(i, W, H)[0]
        return zs
    def zone_in(key):
        for zid, ks in setup["assign"].items():
            if key in ks: return zid
        return None
    def draw_preview():
        old = preview["g"]; zs = setup["zs"]; W, H = Kit.screen(); L = LAYOUT
        if zs is None or W <= 0 or H <= 0: preview["g"] = None; Kit.dispose(old); return
        g = G.CreateGump(False, False)
        for z in zs.zones:
            if z.px is None or z.kind == "r": continue
            x, y, w, h = z.px; col = ZONE_COLORS.get(z.kind, "#3A78C8"); Kit.add_box(g, x, y, w, h, 0.22, col)
            for bx, by, bw, bh in ((x, y, w, 2), (x, y + h - 2, w, 2), (x, y, 2, h), (x + w - 2, y, 2, h)):
                Kit.add_box(g, bx, by, bw, bh, 0.9, col)
            if z.kind == "k": lines = ["Game area"]
            else:
                lines = [z.id] + ([L.title_of(k) for k in setup["assign"].get(z.id, []) if k in L.wins] or ["(empty)"])
            lines = [Kit.fit(t, max(20, w - 28)) for t in lines[:max(1, (h - 16) // 20)]]
            Kit.add_box(g, x + 6, y + 6, max(Kit.text_w(t) for t in lines) + 12, 20 * len(lines) + 6, 0.85, "#000000")
            for n, t in enumerate(lines):
                Kit.add_label(g, t, x + 12, y + 9 + 20 * n, Kit.HUE_TITLE if n == 0 else Kit.HUE_TEXT)
        g.SetRect(0, 0, W, H); g.SetAcceptMouseInput(False); g.CanMove = False; Kit.replace_gump(old, g)
        SNAP.skip_gump(g); preview["g"] = g; Kit.dispose(old)
    def preset_plan(i):
        W, H = Kit.screen(); zs, fname, assign = plan_of(i, W, H)
        setup.update({"preset": i, "zs": zs, "fname": fname, "assign": dict((z, list(v)) for z, v in assign.items())})
    def read_look():
        c, look = win["c"], setup["look"]
        for k in look:
            if k in c: look[k] = bool(c[k].IsChecked)
    def draw_setup():
        s = setup; step = s["step"]; M, GAP = Kit.MARGIN, Kit.GAP; W = SETUP_W; IW = W - 2 * M; L = LAYOUT
        wins = L.all_windows() if step == 1 else []
        body_h = (30 + CARD_H + 56 + 10, 32 + 26 * max(1, len(wins)) + 8, 32 + 26 * len(LOOK_ROWS) + 30)[step]
        h = M + 30 + GAP + body_h + GAP + 44 + M; g, store, c = wnd.begin(W, h)
        if not st["minimized"]:
            wnd.frame(g, settings=False, after="Step %d of 3" % (step + 1)); y = M + 30 + GAP
            if step == 0:
                Kit.add_section(g, M, y, IW, body_h, "LAYOUT  (click one; the screen shows it)"); SW, SH = Kit.screen()
                cy = y + 32; cx0 = M + (IW - 5 * CARD_W - 4 * CARD_GAP) // 2
                for i, (name, desc) in enumerate(PRESETS):
                    cx = cx0 + i * (CARD_W + CARD_GAP); sel = i == s["preset"]
                    if sel: Kit.add_box(g, cx - 2, cy - 2, CARD_W + 4, CARD_H + 4, 0.95, "#E8C15A")
                    Kit.add_box(g, cx, cy, CARD_W, CARD_H, 1.0, "#101010")
                    if SW > 0 and SH > 0:
                        kx, ky = CARD_W / float(SW), CARD_H / float(SH)
                        for z in card_zones(i, SW, SH).zones:
                            if z.px is None or z.kind == "r": continue
                            zx, zy, zw, zh = z.px
                            Kit.add_box(g, cx + int(zx * kx) + 1, cy + int(zy * ky) + 1, max(1, int(zw * kx) - 2),
                                        max(1, int(zh * ky) - 2), 0.85 if sel else 0.5,
                                        ZONE_COLORS.get(z.kind, "#3A78C8"))
                    t = Kit.fit(name, CARD_W)
                    Kit.add_label(g, t, cx + (CARD_W - Kit.text_w(t)) // 2, cy + CARD_H + 6,
                                  Kit.HUE_TITLE if sel else Kit.HUE_TEXT)
                    Kit.catcher(g, cx, cy, CARD_W, CARD_H + 26, queue(("preset", i)),
                                "Use %s: %s" % (name, desc[:1].lower() + desc[1:]))
                Kit.add_label(g, Kit.fit(PRESETS[s["preset"]][1], IW - 24), M + 12, cy + CARD_H + 32, Kit.HUE_INFO)
            elif step == 1:
                Kit.add_section(g, M, y, IW, body_h, "WINDOWS  (click to change a zone)"); ry = y + 32
                if not wins:
                    Kit.add_label(g, "No windows yet; turn modules on, then come back.", M + 12, ry + 3, Kit.HUE_INFO)
                for key, title in wins:
                    zid = zone_in(key); Kit.add_label(g, Kit.fit(title, 300), M + 12, ry + 3)
                    zcap = "Zone: " + ((zid[5:] if zid.startswith("Zone ") else zid) if zid else "free")
                    Kit.art_button(g, store, "z_" + key, Kit.ART_PAGE, M + 330, ry - 2, zcap,
                                   "Click: next zone (free: stays where it is)", on_click=queue(("cycle", key)))
                    ry += 26
            else:
                Kit.add_section(g, M, y, IW, body_h, "LOOK"); ry = y + 32
                for k, cap, tip in LOOK_ROWS: c[k] = Kit.add_check(g, cap, M + 12, ry, s["look"][k], tip); ry += 26
                Kit.add_label(g, "Change any of this later in Settings > Interface.", M + 12, ry + 5, Kit.HUE_INFO)
            ny = y + body_h + GAP; Kit.add_section(g, M, ny, IW, 44)
            Kit.art_button(g, store, "cancel", Kit.ART_CLOSE, M + 12, ny + 10, "Cancel",
                           "Close without changing anything", on_click=queue("cancel"))
            nxt = ("done", Kit.ART_OK, "Done", "Use this layout") if step == 2 else ("next", Kit.ART_PLAY, "Next",
                                                                                     "Go to the next step")
            x = W - M - 12 - 35 - Kit.text_w(nxt[2])
            Kit.art_button(g, store, nxt[0], nxt[1], x, ny + 10, nxt[2], nxt[3], on_click=queue(nxt[0]))
            if step:
                x -= 55 + Kit.text_w("Back")
                Kit.art_button(g, store, "back", Kit.ART_PAGE, x, ny + 10, "Back", "Go back a step",
                               on_click=queue("back"))
        wnd.end(g); refresh()
    def build_window(): Binds.scoped("interface.setup", draw_setup)
    wnd = Kit.Window(SETUP_KEY, "Interface Setup", st, win, build_window, SETUP_POS, default=(200, 120),
                     mini=SETUP_MINI, owner=False, lock=False, close_tip="Close without changing anything")
    def refresh():
        c = win["c"]
        if "status" in c: Kit.set_text(c["status"], "%s: step %d of 3" % ("Interface Setup", setup["step"] + 1))
    def open_setup():
        L = LAYOUT
        if not L.enabled: return
        if not setup["open"]:
            Kit.put_var(SEEN_KEY, "1"); setup.update({"open": True, "step": 0, "cards": {},
                          "look": {"seam": True, "fit_view": L.fit_view, "game": L.game_grows}})
            preset_plan(setup["preset"])
        st["minimized"] = False; draw_preview(); build_window()
    def close_setup():
        setup["open"] = False; old, preview["g"] = preview["g"], None; Kit.dispose(old); wnd.close()
    def act_preset(i): preset_plan(i); draw_preview(); build_window()
    def act_cycle(key):
        s = setup; ids = [None] + [z.id for z in s["zs"].zones if z.kind == "w"]; cur = zone_in(key)
        mapz = zone_in("worldmap"); i = ids.index(cur) if cur in ids else 0
        for _ in ids:
            i = (i + 1) % len(ids); zid = ids[i]
            if zid is None: break
            others = [k for k in s["assign"].get(zid, []) if k != key]
            if not ((key == "worldmap" and others) or (key != "worldmap" and zid == mapz)): break
        if cur is not None: s["assign"][cur] = [k for k in s["assign"][cur] if k != key]
        if zid is not None: s["assign"].setdefault(zid, []).append(key)
        draw_preview(); build_window()
    def act_step(d): read_look(); setup["step"] = max(0, min(2, setup["step"] + d)); build_window()
    def act_done():
        read_look(); s = setup; L = LAYOUT; W, H = Kit.screen(); zs, fname, look = s["zs"], s["fname"], s["look"]
        L.seamless, L.fit_view, L.game_grows = look["seam"], look["fit_view"], look["game"]; L.save_opts()
        if fname != LAYOUT_DEFAULT: zs.generated = False; L.save_frames(zs.copy(fname), fname, W, H)
        L.use_frames(fname, tell=False); L.assign = dict((z, list(v)) for z, v in s["assign"].items() if v)
        L.unfree(None); L.save_assign(); name = PRESETS[s["preset"]][0]
        name = name + " (mine)" if name in (LAYOUT_DEFAULT, LAYOUT_MIRRORED) else name
        Kit.put_var(LAYOUT_NAMED % name, L.windows_text()); names = L.layout_names()
        if name not in names: names.append(name); Kit.put_var(LAYOUT_LIST, ",".join(names))
        L.use_windows(name, tell=False); L.refit_all(); HOST.poke(); close_setup(); load_settings()
        n = sum(1 for ks in L.assign.values() for k in ks if L.gump_of(k) is not None)
        say('"%s" in use: %s placed.' % (name, Kit.count(n, "window")), Kit.HUE_GOOD)
    def act_cancel(): close_setup(); say("setup closed; nothing changed.", Kit.HUE_INFO)
    ACTIONS = {"setup": open_setup, "preset": act_preset, "cycle": act_cycle, "next": lambda: act_step(1),
               "back": lambda: act_step(-1), "done": act_done, "cancel": act_cancel}
    def windows_line():
        L = LAYOUT; n = sum(len(ks) for ks in L.assign.values()); zs = L.frames
        if not n: return "No window in a zone yet: click Set up, or Arrange windows"
        gp = Layout._game_px(zs) if zs is not None else None
        return "%s in %s%s" % (Kit.count(n, "window"), Kit.count(len(L.assign), "zone"),
                               "; game area %d x %d" % gp[2:] if gp else "")
    def drop(g, names, i, x, y, tip):
        dd = G.CreateDropDown(DD_W, names, i); dd.SetPos(x, y); g.Add(dd); return Kit.with_tip(dd, tip)
    def draw_drops(f, x, y):
        L = LAYOUT; names = page["frame_names"] = [LAYOUT_DEFAULT] + L.frame_names()
        fi = names.index(L.frames_name) if L.frames_name in names else 0
        lnames = page["layout_names"] = ["(none)", LAYOUT_DEFAULT, LAYOUT_MIRRORED] + L.layout_names()
        cur = L.layout_name or "(none)"; li = lnames.index(cur) if cur in lnames else 0
        Kit.add_label(f.g, "Zones:", x + 12, y + 3, Kit.HUE_TEXT)
        Kit.add_label(f.g, "Windows:", x + 12, y + 31, Kit.HUE_TEXT)
        page["zones"] = (drop(f.g, names, fi, x + 92, y, "The frame layout in use (its zones)"), fi)
        page["windows"] = (drop(f.g, lnames, li, x + 92, y + 28,
                                "The window layout in use; pick one to place every window"), li)
    def zone_drops(f, x, y):
        L = LAYOUT; wins = L.all_windows(); pv = L.page_preview; ry = y - 26 * len(wins) - (20 if pv else 0)
        zones = ["free"] + [z for z in L.zone_choices() if z]; page["zone_dd"] = []
        for key, title in wins:
            zid = L.zone_of(key); ids = labels = zones
            if zid is not None and zid not in zones:
                ids, labels = zones + [zid], zones + [Kit.fit("%s (missing)" % zid, DD_W - 30)]
            zi = ids.index(zid) if zid in ids else 0
            dd = drop(f.g, labels, zi, x + 302, ry, "The zone it sits in (free: stays where you put it)")
            page["zone_dd"].append((key, dd, zi, ids)); ry += 26
    def situ_drops(f, x, y):
        L = LAYOUT; names = page["situ_names"] = ["(none)", LAYOUT_DEFAULT, LAYOUT_MIRRORED] + L.layout_names()
        page["situ_dd"] = []
        for n, (kind, cap, tip) in enumerate(SITU_ROWS):
            cur = L.situ.get(kind, ""); i = names.index(cur) if cur in names else 0
            Kit.add_label(f.g, cap, x + 12, y + 3 + 28 * n, Kit.HUE_TEXT)
            page["situ_dd"].append((kind, drop(f.g, names, i, x + 92, y + 28 * n, tip), i))
    def share_code():
        code = LAYOUT.share_code()
        if not code: say("no zones to share yet.", Kit.HUE_BAD); return
        settings["code"] = code; f = cfg.f
        if f is not None and "code" in f.c: f.c["code"].SetText(code)
        st["jobs"].append(lambda: write_code(code))
        say("layout code ready; Ctrl+A then Ctrl+C in the field copies it.", Kit.HUE_GOOD)
    def write_code(code):
        try: Kit.write_safe(Kit.data_path(Layout.CODE_FILE), code + "\n")
        except Exception as ex: say("couldn't write %s (%s)." % (Layout.CODE_FILE, ex), Kit.HUE_BAD)
    def load_code():
        f = cfg.f; c = f.c.get("code") if f is not None else None
        LAYOUT.load_code(str(c.Text or "") if c is not None else settings["code"])
    def page_table(w):
        load_settings(); L = LAYOUT; wins = L.all_windows(); pv = L.page_preview
        snap = ("check", "snap", "Snap windows together", "Windows dropped near each other line up")
        look = (("buttons", (("look", Kit.ART_PAGE, "Look: %s" % Kit.LOOK_NAMES[Kit.look()],
                              "Next look: Classic, Dark, Parchment or High contrast"),
                             ("tsize", Kit.ART_PAGE, "Text size: %d%%" % int(round(Kit.tscale * 100)),
                              "Text in lists and bars (TazUO's own UI scale sizes every window)"))),
                ("check", "compact", "Compact rows", "Tighter rows in lists and settings; smaller frames"),
                ("check", "fade", "Fade windows when idle", "Dim windows until the mouse is over them or they change"),
                ("num", "fade_to", "Faded:", "How solid an idle window stays (20-90)", "%", 20, 90),
                ("num", "fade_after", "After:", "Seconds without the mouse or a change before it fades (2-30)", "s",
                 2, 30), ("check", "fade_all", "Fade the Action Bar and Character HUD > Frames too",
                 "Off: they stay solid while other windows fade"))
        access = ("ACCESSIBILITY", (("check", "cblind", "Colour-blind marks",
                                     "Letters beside notoriety and HP colours; colour-blind palette"),
                                    ("check", "streamer", "Streamer mode",
                                     "Hide names, guild and coordinates in Virtue Assistant windows")))
        grid = (snap, ("check", "grid_on", "Show the grid", "Show the snapping grid over the screen"),
                ("num", "grid", "Grid:", "Grid spacing for snapping", "px", 8, 512))
        if VA_ALONE: return (("ZONES", (("note", "Zones, layout and snapping are set in the full"),
                                        ("note", "Virtue Assistant."))),)
        if not L.enabled: return (("ZONES", (("note", "Interface is off, so zones are off."),
                                             ("note", "Tick Interface on the Modules tab to use them."))),
                                  ("LOOK", look), access, ("SNAPPING", grid))
        arr = (("arrange", Kit.ART_OK, "Done", "Lock every window in its zone") if L.arrange else
               ("arrange", Kit.ART_PLAY, "Arrange windows",
                "Unlock windows to drag them between zones (Esc or Done locks them)"))
        undo = ((("reclaim_undo", Kit.ART_CLOSE, "Undo", "Put the zones back as before Reclaim space"),)
                if L._undo_load() is not None else ())
        out = (("SCREEN", (("note", Kit.fit(windows_line(), w - 24)), ("note", Kit.fit(L.status_text(), w - 24)),
                           ("buttons", (("setup", Kit.ART_PLAY, "Set up", "Pick a ready-made layout in three steps"),
                                        arr)),
                           ("buttons", (("edit", Kit.ART_PAGE, "Edit zones", "Drag, resize, split or join zones"),
                                        ("new", Kit.ART_OK, "New zones", "Start a new frame layout with one zone"))))),
               ("LOOK", tuple(("check", k, cap, tip) for k, cap, tip in LOOK_ROWS) + look), access, ("SNAPPING", grid),
               ("LAYOUTS  (saved)", (("buttons", (("save", Kit.ART_OK, "Save windows",
                                 "Save where every window sits as the window layout in use"),
                                ("reset", Kit.ART_CLOSE, "Reset", "Go back to the Default window layout"),
                                ("free", Kit.ART_CLOSE, "Free all", "Take every window out of its zone"))),
                   ("buttons", (("remove", Kit.ART_CLOSE, "Remove zones",
                                 "Delete the frame layout in use (not Default)"), ("check", Kit.ART_PLAY, "Check fit",
                                 "Print where each window in a zone sits and if it fills it"))),
                   ("buttons", (("reclaim", Kit.ART_PLAY, "Reclaim space",
                                 "Give the game area every gap beside it; windows keep their size"),) + undo),
                   ("custom", 60, draw_drops), ("buttons", (("share", Kit.ART_PAGE, "Share code",
                                 "Put a code for the layouts in use in the field below"),
                                ("load_code", Kit.ART_OK, "Load code", "Load the layout code in the field below"))),
                   ("text", "code", "Code:", "Layout code: Ctrl+A then Ctrl+C copies it, Ctrl+V pastes one"))),
               ("LAYOUTS BY SITUATION", (("check", "situ_on", "Switch layouts by situation",
                                          "Use the layouts below in war mode, at the bank, in dungeons and in town"),
                                         ("custom", 28 * len(SITU_ROWS), situ_drops),
                                         ("note", "War mode first, then bank, dungeon, town"))))
        if not wins: return out
        rows = [("note", Kit.fit(t, 270), {"hue": Kit.HUE_TEXT, "ndy": 3, "h": 26}) for k, t in wins]
        if pv: rows.append(("note", Kit.fit(pv.lstrip("!"), w - 24), {"ndy": 3, "hue": Kit.HUE_BAD if pv.startswith("!")
                                                                       else Kit.HUE_INFO}))
        return out + (("WINDOWS  (the zone each sits in)", rows + [("custom", 0, zone_drops)]),)
    def on_change(old, new):
        L = LAYOUT; ch = set(k for k in new if new[k] != old.get(k))
        if ch & set(("seam", "fit_view", "game")):
            L.seamless, L.fit_view, L.game_grows = new["seam"], new["fit_view"], new["game"]; L.save_opts()
            L.dirty = True
            if ch & set(("seam", "fit_view")): L.fresh = True; L.seam_skip = {}; L.seam_wait = {}
        if "snap" in ch:
            SNAP.enabled = new["snap"]
            if not SNAP.enabled: SNAP.links.clear()
            HOST.save_prefs()
        if "grid" in ch:
            HOST.prefs["grid"] = str(new["grid"]); HOST.save_prefs()
            if HOST.grid is not None: HOST.grid.redraw()
        if "grid_on" in ch and new["grid_on"] != HOST.grid_shown(): HOST.grid_toggle()
        if "situ_on" in ch: L.situ_set(new["situ_on"])
        for k in ("compact", "cblind", "streamer"):
            if k in ch: HOST.set_switch(k, new[k])
        if ch & set(Fade.KEYS): FADE.set(new)
    def next_look():
        o = Kit.LOOK_ORDER; HOST.set_look(o[(o.index(Kit.look()) + 1) % len(o)])
    def next_tsize():
        o, cur = Kit.TEXT_SIZES, int(round(Kit.tscale * 100))
        HOST.set_switch("tsize", o[(o.index(cur) + 1) % len(o)] if cur in o else o[0])
    def remove_frames():
        if not LAYOUT.remove_frames(LAYOUT.frames_name):
            say("Default can't be deleted; pick another frame layout first.", Kit.HUE_BAD)
    PAGE_ACTIONS = (("setup", open_setup), ("arrange", lambda: LAYOUT.set_arrange(not LAYOUT.arrange)),
                    ("edit", lambda: edit(False)), ("new", lambda: edit(True)), ("remove", remove_frames),
                    ("save", lambda: LAYOUT.save_windows()), ("reset", lambda: LAYOUT.use_windows(LAYOUT_DEFAULT)),
                    ("free", lambda: LAYOUT.use_windows("")), ("reclaim", lambda: LAYOUT.reclaim_space()),
                    ("reclaim_undo", lambda: LAYOUT.reclaim_back()), ("check", lambda: LAYOUT.report_fit()),
                    ("look", next_look), ("tsize", next_tsize), ("share", share_code), ("load_code", load_code))
    def page_clicks(f):
        L = LAYOUT
        if L.page_refresh: L.page_refresh = False; cfg.f = None; HOST.refresh_settings(KEY); return
        for n, (key, dd, zi, ids) in enumerate(page["zone_dd"]):
            i = Kit.dd_index(dd, zi)
            if i != zi and 0 <= i < len(ids):
                page["zone_dd"][n] = (key, dd, i, ids); zid = None if i == 0 else ids[i]; L.page_preview = ""
                if zid:
                    W, H = Kit.screen(); zs = L.frames_in_use(W, H) if W > 0 and H > 0 else None
                    L.page_preview = L.preview_text(key, zs.by_id(zid) if zs is not None else None)
                L.assign_to(key, zid); L.page_refresh = True; return
        if page["zones"] is not None:
            dd, fi = page["zones"]; i = Kit.dd_index(dd, fi)
            if i != fi and 0 <= i < len(page["frame_names"]):
                page["zones"] = (dd, i); L.use_frames(page["frame_names"][i]); return
            dd, li = page["windows"]; i = Kit.dd_index(dd, li)
            if i != li and 0 <= i < len(page["layout_names"]):
                page["windows"] = (dd, i); L.use_windows("" if i == 0 else page["layout_names"][i]); return
        for n, (kind, dd, si) in enumerate(page["situ_dd"]):
            i = Kit.dd_index(dd, si)
            if i != si and 0 <= i < len(page["situ_names"]):
                page["situ_dd"][n] = (kind, dd, i); L.situ_pick(kind, "" if i == 0 else page["situ_names"][i]); return
        for k, fn in PAGE_ACTIONS:
            if Kit.was_clicked(f.store, k): fn(); return
    cfg = Kit.Page(settings, page_table, save_settings, on_change, clicks=page_clicks)
    def page_closed(): page.update({"zones": None, "windows": None, "zone_dd": [], "situ_dd": []}); cfg.closed()
    def _start():
        st.update({"shutting": False, "docked": False, "queue": [], "minimized": False, "editor": None,
                   "back_sig": None, "back_at": 0.0, "alone_up": False, "jobs": []}); setup["open"] = False
        if VA_ALONE: load_settings(); HOST.show_settings(KEY); return
        LAYOUT.set_enabled(True); load_settings(); cleanup.service("interface.page", lambda: HOST.show_settings(KEY))
        if not Kit.get_var(SEEN_KEY, "") and not LAYOUT.assign and not Kit.get_var(LAYOUT_ACTIVE, ""): queue("setup")()
    def _tick():
        if VA_ALONE:
            up = HOST.config.win["g"] is not None
            if st["alone_up"] and not up: HOST.disable(KEY)
            st["alone_up"] = st["alone_up"] or up; return
        q = st["queue"]
        while q:
            action = q.pop(0); action = "toggle_min" if action == "to_bar" else action
            if isinstance(action, tuple): ACTIONS[action[0]](*action[1:])
            elif not wnd.action(action): ACTIONS[action]()
        if setup["open"] and Kit.was_clicked(win["store"], "close"): act_cancel()
        elif setup["open"] and not Kit.is_open(win["g"]): close_setup()
        ed = st["editor"]
        if ed is not None:
            W, H = Kit.screen()
            if W > 0 and H > 0: ed.keep(W, H)
            ed.poll()
        now = time.time(); LAYOUT.situ_tick(now, ed is not None or setup["open"])
        Seam.hover(LAYOUT.arrange); backdrop_tick(now); sink()
    def _thread_tick():
        while st["jobs"] and not st["shutting"]: st["jobs"].pop(0)()
    def _interval():
        idle = not (st["queue"] or setup["open"] or Seam.recs or Seam.bare or VA_ALONE)
        return 0.25 if idle and st["editor"] is None and back["g"] is None else 0.05
    def _stop():
        st["shutting"] = True; ed = st["editor"]
        if ed is not None: ed.close(keep=False, quiet=True)
        if setup["open"]: close_setup()
        for hold in (back, ring, preview): old, hold["g"] = hold["g"], None; Kit.dispose(old)
        if not VA_ALONE: LAYOUT.set_enabled(False)
        cleanup.close()
    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
            "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": page_closed, "interval": _interval,
            "thread_tick": _thread_tick, "thread_wanted": lambda: bool(st["jobs"])}


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("interface", "Interface", "Zones, layouts and the one-panel look", _module_interface, 0.05, default_on=True,
         category="On screen")
