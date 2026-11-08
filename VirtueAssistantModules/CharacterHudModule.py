def _module_hud():
    KEY = "hud"; TITLE = "Character HUD"
    PIECES = {"anchor": {}, "piece": {}, "tied": {}, "span": {}, "inner": {}, "bg": {}, "bare": {},
              "stack": {}, "dirty": True, "full_at": 0.0, "sig": None, "objs": None, "inside": []}
    PLACE_EVERY = 0.5; PIECE_IN = 42
    def pieces_extent(fkey, below):
        s = PIECES["stack"].get(fkey)
        if s is None or s[0] != below: return 0
        return max(0, int(s[1]))
    def pieces_anchor(fkey, getter, span=None, inner=None):
        PIECES["dirty"] = True
        if getter is None:
            PIECES["anchor"].pop(fkey, None); PIECES["span"].pop(fkey, None); PIECES["inner"].pop(fkey, None)
            for pkey, (fk, _o, _g) in list(PIECES["piece"].items()):
                if fk == fkey: _piece_free(pkey)
        else: PIECES["anchor"][fkey] = getter; PIECES["span"][fkey], PIECES["inner"][fkey] = span, inner
    def pieces_add(pkey, fkey, order, getter):
        PIECES["piece"][pkey] = (fkey, int(order), getter); PIECES["dirty"] = True
    def pieces_remove(pkey): PIECES["piece"].pop(pkey, None); PIECES["dirty"] = True; _piece_free(pkey)
    def _piece_free(pkey):
        tied = PIECES["tied"].pop(pkey, None); g = None
        if tied is not None: Kit.detach(tied[0]); g = tied[0]
        elif pkey in PIECES["piece"]: g = PIECES["piece"][pkey][2]()
        bare = PIECES["bare"]
        if g is None or not bare or not bare.pop(g, False) or not Kit.is_open(g): return
        for ctrl in list(Kit._frame_parts.get(g) or ()) + list(PIECES["bg"].get(g) or ()):
            Kit.set(ctrl, "IsVisible", True)
    def pieces_frame(fkey):
        fn = PIECES["anchor"].get(fkey); g = fn() if fn is not None else None
        return g if Kit.is_open(g) and g.IsVisible else None
    def pieces_on(pkey): p = PIECES["piece"].get(pkey); return p is not None and pieces_frame(p[0]) is not None
    RAISE = {"at": 0.0, "uim": None, "off": False, "same": None}
    def pieces_raise(pairs):
        if RAISE["off"]: return
        now = time.time()
        if now < RAISE["at"]: return
        RAISE["at"] = now + 0.25
        try:
            if RAISE["uim"] is None:
                import System; RAISE["same"] = System.Object.ReferenceEquals
                RAISE["uim"] = Tz.T("ClassicUO.Game.Managers.UIManager")
            uim, same = RAISE["uim"], RAISE["same"]; gumps = Tz.get(None, "Gumps", uim); mp = Kit.mouse_pos()
            for pg, fg in pairs:
                if mp is not None:
                    fr_ = _rect_of(fg)
                    if fr_ is not None and fr_[0] <= mp[0] < fr_[0] + fr_[2] and fr_[1] <= mp[1] < fr_[1] + fr_[3]:
                        continue
                rp, rf = Kit._raw_gump(pg), Kit._raw_gump(fg)
                if rp is None or rf is None: continue
                node = gumps.First
                while node is not None:
                    v = node.Value
                    if same(v, rp): break
                    if same(v, rf): Tz.call(None, "MakeTopMostGump", [rp], uim); break
                    node = node.Next
        except Exception: RAISE["off"] = True
    def _rect_of(g): r = Kit.rect(g); return r if r is not None and r[2] > 0 and r[3] > 0 else None
    def _pieces_sig(sw, sh):
        vals = [sw, sh]; objs = []
        for pkey, (fk, order, getter) in PIECES["piece"].items(): vals.append((pkey, fk, order)); objs.append(getter())
        for fk in PIECES["anchor"]:
            fg = pieces_frame(fk); r = span = inner = None
            if fg is not None:
                r = _rect_of(fg); sfn, ifn = PIECES["span"].get(fk), PIECES["inner"].get(fk)
                span = sfn() if sfn is not None else None; inner = ifn() if ifn is not None else None
            vals.append((fk, r, span, inner)); objs.append(fg)
        return vals, objs
    def pieces_place():
        sw, sh = Kit.screen(); now = time.time(); vals, objs = _pieces_sig(sw, sh)
        if not PIECES["dirty"] and now < PIECES["full_at"] and now + 2 * PLACE_EVERY > \
                PIECES["full_at"] and vals == PIECES["sig"]:
            old = PIECES["objs"]; same = old is not None and len(old) == len(objs)
            if same:
                for i in range(len(objs)):
                    if objs[i] is not old[i]: same = False; break
            if same:
                if PIECES["inside"]: pieces_raise(PIECES["inside"])
                return
        PIECES["sig"], PIECES["objs"] = vals, objs; PIECES["dirty"] = False; PIECES["full_at"] = now + PLACE_EVERY
        seen = {}; inside = []; by_frame = {}
        for pkey, (fk, order, getter) in PIECES["piece"].items():
            by_frame.setdefault(fk, []).append((order, pkey, getter))
        for fk in [k for k in PIECES["stack"] if k not in by_frame]: PIECES["stack"].pop(fk, None)
        for fk, items in by_frame.items():
            fg = pieces_frame(fk)
            if fg is None:
                for _o, pkey, _g in items: _piece_free(pkey)
                PIECES["stack"].pop(fk, None); continue
            fr_r = _rect_of(fg)
            if fr_r is None: PIECES["dirty"] = True; continue
            fx, fy, fw, fh = fr_r; below = sh <= 0 or (fy + fh / 2.0) < sh / 2.0
            sfn, ifn = PIECES["span"].get(fk), PIECES["inner"].get(fk); span = sfn() if sfn is not None else None
            inner = ifn() if ifn is not None and span is not None else None; hole = None; items.sort()
            y = fy + fh if below else fy
            for _o, pkey, getter in items:
                g = getter()
                if not Kit.is_open(g): _piece_free(pkey); continue
                seen[pkey] = g
                if not g.IsVisible: continue
                pr = _rect_of(g)
                if pr is None: PIECES["dirty"] = True; continue
                px, py, pw, ph = pr; ix = None
                if inner is not None and hole is None and pw < fw:
                    PM = Kit.MARGIN; pad, iw, ih, ay, ah = inner[:5]
                    rx = (span[0] - PM) if span[2] else (span[1] - pw + PM)
                    ry = (inner[5] if len(inner) > 5 else ay + ah) + Kit.GAP - PM
                    rx = max(pad - PM, min(rx, iw - pad - pw + PM))
                    if ry + PM + PIECE_IN <= ih - pad + 2 and rx >= 0: ix, hole = (fx + rx, fy + ry), 1
                if ix is not None: x, ny = ix; inside.append((g, fg))
                elif span is not None and pw < fw:
                    x = fx + (span[1] - pw if span[2] else span[0]); x = max(fx, min(x, fx + fw - pw))
                else: x = fx + (fw - pw) // 2
                if ix is None:
                    if sw > 0: x = max(0, min(x, sw - pw))
                    if below: ny, y = y, y + ph
                    else: y -= ph; ny = y
                if (px, py) != (x, ny): g.SetPos(x, ny); Kit.note_rect(g, x, ny); Kit.moved_by_code(g)
                tied = PIECES["tied"].get(pkey)
                if tied is None or tied[0] is not g or tied[1] is not fg:
                    if tied is not None and tied[0] is not g: Kit.detach(tied[0])
                    Kit.attach(g, fg); PIECES["tied"][pkey] = (g, fg)
            PIECES["stack"][fk] = (below, (y - (fy + fh)) if below else (fy - y))
        bare = PIECES["bare"]; now_in = set(g for g, _f in inside)
        for d in (bare, PIECES["bg"]):
            for g in [g for g in d if not Kit.is_open(g)]: d.pop(g, None)
        for pkey, (fk, order, getter) in PIECES["piece"].items():
            g = seen.get(pkey)
            if g is None: g = getter()
            if not Kit.is_open(g): continue
            want = g in now_in
            if bare.get(g, False) != want:
                bare[g] = want
                if want: Kit.pin_size(g)
                for ctrl in list(Kit._frame_parts.get(g) or ()) + list(PIECES["bg"].get(g) or ()):
                    Kit.set(ctrl, "IsVisible", not want)
        PIECES["inside"] = inside
        if inside: pieces_raise(inside)
    PIECES_TARGET = {"fn": None}; READOUT_WORDS = ("Ready", "Done", "Out!", "Dead", "Paused")
    def readout_room(): return max(Kit.text_w(w) for w in READOUT_WORDS)
    def skill_value(name, default=0.0):
        try: return float(API.GetSkill(name).Value or 0)
        except Exception: return default
    def part_dict(start, tick, stop, height, build, poll, closed, **more):
        more.update({"start": start, "tick": tick, "stop": stop, "client_tick": True, "config_height": height,
                     "build_config": build, "poll_config": poll, "config_closed": closed})
        return more
    def _part_frames():
        KEY = "unitframes"; TITLE = "Frames"; ROWS = ("hits", "mana", "stam"); BAR_BG = "#17171a"
        BAR_COLOR = {"hits": "#c22d2d", "poison": "#2f9a3c", "yellow": "#cfae2a", "mana": "#2f62cc", "stam": "#d39a1c"}
        NOTO_COLOR = {"innocent": (46, 104, 214), "ally": (40, 160, 70), "gray": (120, 120, 126),
                      "criminal": (120, 120, 126), "enemy": (222, 118, 30),
                      "murderer": (196, 38, 38), "invulnerable": (214, 178, 40)}
        NO_NOTO = (226, 226, 230)
        NOTO_NUM = {1: "innocent", 2: "ally", 3: "gray", 4: "criminal", 5: "enemy", 6: "murderer", 7: "invulnerable"}
        SNAP_BG = (0, 0, 8); MALE_GUMP, FEMALE_GUMP = 50000, 60000
        PAPERDOLL_BODY = {0x0190: 0x000C, 0x0192: 0x000C, 0x0191: 0x000D, 0x0193: 0x000D,
                          0x025D: 0x000E, 0x025F: 0x000E, 0x025E: 0x000F, 0x0260: 0x000F,
                          0x029A: 0x029A, 0x02B6: 0x029A, 0x029B: 0x0299, 0x02B7: 0x0299,
                          0x04E5: 0xC835, 0x03DB: 0x000C}
        FEMALE_BODIES = (0x0191, 0x0193, 0x025E, 0x0260, 0x029B, 0x02B7); GM_BODY, GM_BODY_HUE = 0x03DB, 0x03EA
        LAYERS = ("cloak", "shirt", "arms", "torso", "tunic", "face", "robe", "neck",
                  "hair", "beard", "earrings", "helmet")
        LAYERS_QUIVER = ("shirt", "arms", "torso", "tunic", "face", "robe", "cloak", "neck",
                         "hair", "beard", "earrings", "helmet")
        LAYERS_PARROT = ("shirt", "arms", "torso", "tunic", "cloak", "face", "neck",
                         "hair", "beard", "earrings", "helmet", "robe")
        PARROT_ROBES = (0xA2CA, 0xA2CB); OPEN_ROBES = (0x9985, 0x9986, 0xA412, 0xA2CB, 0xA2CA)
        PLATE_ARMS = (0x1410, 0x1417); SNAP_DEPTH = 110; SNAP_RETRY = 2.0; THREAD_BUDGET = 0.008; TEX_PREFIX = "vauf_"
        MAX_TRACKED = 12; SCALE_MIN, SCALE_MAX, SCALE_DEFAULT = 50, 150, 70; LABEL_H = 14; PICK_TIMEOUT = 10
        PREVIEW = 100; SETTINGS_KEY = "UnitFrames_settings"; TRACKED_KEY = "UnitFrames_tracked"
        FRAMEPOS_KEY = "UnitFrames_framepos"; POS_KEY = "UnitFrames_pos"; MIN_KEY = "UnitFrames_min"; W = 350
        CLOSE_ART = (0x0FB1, 0x0FB2, 0x0FB1); CLOSE_INSET = 3; MINI_W, MINI_H = 240, 46; DRAG_SETTLE = 0.4
        TICK_EVERY = 0.05; FRAME_SNAP = SNAP_DIST; CAST_H = 24; CAST_GAP = 2; CAST_HOLD = 1.5; CAST_FAIL_WINDOW = 10.0
        CAST_COLOR = {"cast": "#cfae2a", "done": "#2f9a3c", "fail": "#c22d2d"}
        CAST_FAIL_TEXTS = (("the spell fizzles", "fizzled"), ("your concentration is disturbed", "disturbed"),
                           ("insufficient mana", "no mana"), ("more reagents are needed", "no reagents"))
        SPELLS = Kit.SPELL_WORDS; TEXT_PX = Kit.text_px; ART_W, ART_H = 502, 194
        RING_C = (96.5, 96.5); HOLE_R = 52.5
        RING = ((86.0, (22, 22, 24)), (81.5, (226, 226, 230)), (79.5, "tire"), (64.5, (30, 25, 10)),
                (61.5, (226, 226, 230)), (60.5, "gold"), (53.5, (14, 10, 2)))
        NOTO_RING = (78.0, 83.5); PANEL = (150.0, 39.5, 491.5, 154.5, 9.0); METAL = (153.0, 42.6, 488.0, 151.0, 6.5)
        INNER = (178.5, 47.5, 476.5, 146.0, 8.0); HOLES = (183.5, 51.5, 472.5, 141.5, 6.0)
        SEPARATORS = ((77.5, 83.5), (109.5, 115.5))
        RIVETS = ((483.5, 45.8, (188, 188, 193)), (483.5, 148.6, (128, 128, 133)))
        OUTLINE_RGB, INNER_RGB = (20, 20, 22), (16, 16, 18); ART_ROWS_X = (182, 474)
        ART_ROWS_Y = ((51, 79), (83, 111), (115, 143)); SQRT_HALF = 0.70710678
        DEFAULTS = {"player": True, "target": True, "hide_empty": False, "numbers": True,
                    "lock": False, "click": True, "party": False, "ignore_self": True,
                    "attack": False, "status": True, "scale": SCALE_DEFAULT, "pdx": 0, "pdy": 0,
                    "pscale_on": False, "pscale": SCALE_DEFAULT, "pzoom": 100, "mirror": False, 
                    "sup_open": False, "sup_deep": True, "sup_hide0": False, "sup_follow": True,
                    "sup_low": 10, "sup_side": 0, "cast": True, "guard": True, "hide_bar": True}
        NUMBERS = {"scale": (SCALE_MIN, SCALE_MAX), "pscale": (SCALE_MIN, SCALE_MAX),
                   "pdx": (-60, 60), "pdy": (-60, 60), "pzoom": (50, 200), "sup_low": (0, 9999), "sup_side": (0, 2)}
        settings = dict(DEFAULTS)
        def st_reset():
            st.update({"shutting": False, "queue": [], "rebuild": False, "docked": False, "target": 0,
                       "next_party": 0.0, "snaps": {}, "stale": set(), "snap_queue": [], "art_scales": set(),
                       "snap_px": None, "party": set(), "snap_job": None, "art_jobs": [], "art_failed": set(),
                       "recent": [], "next_prune": 0.0, "art_dirty": True, "snap_tries": {}, "guard": None,
                       "next_guard": 0.0, "jr": None, "dismissed": set(), "removing": False, "full_at": 0.0,
                       "mirror_now": False, "pos_save_at": 0.0})
        st = {"minimized": False, "me": 0, "names": {}, "pos": {}, "next_save": 0.0, "pos_dirty": False,
              "crop_changed": 0.0, "art": None, "textures": set(), "running": False}
        st_reset(); tracked = []; anchor = {"sig": None, "at": None}
        cast = {"g": None, "c": {}, "spell": None, "start": 0.0, "secs": 1.0, "state": None,
                "until": 0.0, "pct": 0, "word": "", "shown": None, "at": None, "leader": None, "s": None, "w": 0}
        frames = {}; win = {"g": None, "store": ({}, {})}; cleanup = Kit.Cleanup(); say = Kit.sayer(TITLE)
        page = {"store": ({}, {}), "next_preview": 0.0, "layers": None}; item_info = {}
        _get, _put = Kit.get_var, Kit.put_var
        def load_settings(): Kit.kv_load(SETTINGS_KEY, ",", settings, NUMBERS)
        def save_settings(): Kit.kv_save(SETTINGS_KEY, ",", settings, sorted(DEFAULTS), NUMBERS)
        def load_tracked():
            del tracked[:]
            for part in _get(TRACKED_KEY).split(";"):
                p = part.split(",", 2)
                if len(p) < 3: continue
                try: tracked.append({"serial": int(p[0]), "auto": p[1] == "1", "name": p[2]})
                except ValueError: pass
        def save_tracked():
            _put(TRACKED_KEY, ";".join("%d,%s,%s" % (t["serial"], "1" if t["auto"] else "0",
                                                     t["name"].replace(";", " ").replace(",", " ")) for t in tracked))
        def load_positions():
            st["pos"] = {}
            for part in _get(FRAMEPOS_KEY).split(";"):
                try: k, xy = part.split(":"); x, y = xy.split(","); st["pos"][k] = Kit.adapt(int(x), int(y))
                except ValueError: pass
        def save_positions():
            remember_positions(); keep = set("m%d" % t["serial"] for t in tracked); keep.update(("player", "target"))
            pos = st["pos"]
            for k in [k for k in pos if k not in keep]: del pos[k]
            _put(FRAMEPOS_KEY, ";".join("%s:%d,%d" % (k, p[0], p[1]) for k, p in sorted(pos.items())))
            st["pos_dirty"] = False
        def note_pos(key, p, at=0):
            if st["pos"].get(key) != p:
                st["pos"][key] = p; st["pos_dirty"] = True
                if at: st["pos_save_at"] = at
        def remember_positions():
            for key, fr in frames.items():
                if Kit.is_open(fr.get("g")):
                    p = frame_at(fr)
                    if p is not None: note_pos(key, p)
        def my_serial(): return int(safe(lambda: API.Player.Serial, 0) or 0)
        def noto_name(n):
            if n is None: return ""
            try: return NOTO_NUM.get(int(n), "")
            except Exception: return str(n).split(".")[-1].lower()
        def find_mobile(serial): return HOST.me() if serial == st["me"] else HOST.mobile(serial)
        M_NAME, M_HITS, M_HMAX, M_MANA, M_MMAX, M_STAM, M_SMAX, M_NOTO, M_DEAD, M_POISON, M_YELLOW, M_PARA = range(12)
        _slow_reads = {}
        def read_mobile(serial):
            if not serial: return None
            m = find_mobile(serial)
            if m is None: return None
            try:
                dead = bool(m.IsDead); now = time.time(); c = _slow_reads.get(serial)
                if c is None or now >= c[5] or dead != c[6]:
                    if c is None and len(_slow_reads) >= 64: _slow_reads.clear()
                    c = _slow_reads[serial] = (str(m.Name or ""), int(m.HitsMax or 0), int(m.ManaMax or 0),
                                               int(m.StaminaMax or 0), noto_name(m.Notoriety), now + 0.5, dead)
                d = (c[0], int(m.Hits or 0), c[1], int(m.Mana or 0) if c[2] else 0, c[2],
                     int(m.Stamina or 0) if c[3] else 0, c[3], c[4], dead, bool(m.IsPoisoned), bool(m.IsYellowHits),
                     bool(m.IsParalyzed))
            except Exception: _slow_reads.pop(serial, None); return None
            name = d[M_NAME]
            if name and st["names"].get(serial) != name: st["names"][serial] = name
            return d
        _members = {}
        def instance_member(obj, name):
            t = obj.GetType(); key = (t, name); acc = _members.get(key, False)
            if acc is False:
                from System.Reflection import BindingFlags
                flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
                p = t.GetProperty(name, flags)
                if p is not None: acc = (p, True)
                else: f = t.GetField(name, flags); acc = (f, False) if f is not None else None
                _members[key] = acc
            if acc is None: return None
            return acc[0].GetValue(obj, None) if acc[1] else acc[0].GetValue(obj)
        attack = {"get": None, "looked": False, "root": None, "obj": None, "until": 0.0}; HOLD_FOR = 2.0
        def attack_chain():
            t = Client._type("ClassicUO.Game.World"); first = Client._member(t, "Instance") if t is not None else None
            if first is None: return None
            def get():
                root = first[0]()
                if root is None: attack["obj"] = None; return 0
                obj = attack["obj"]; now = time.time()
                if obj is None or root is not attack["root"] or not 0 < attack["until"] - now <= HOLD_FOR:
                    attack["obj"] = None; obj = instance_member(root, "TargetManager")
                    if obj is None: return 0
                    attack.update({"root": root, "obj": obj, "until": now + HOLD_FOR})
                try: return int(instance_member(obj, "LastAttack") or 0)
                except Exception: attack["obj"] = None; raise
            get(); return get
        def attack_serial():
            if not attack["looked"]: attack["looked"] = True; attack["get"] = safe(attack_chain)
            return int(safe(attack["get"], 0) or 0) if attack["get"] is not None else 0
        def update_target():
            s = (attack_serial() if settings["attack"] else 0) or int(API.LastTargetSerial or 0)
            if not s: st["target"] = 0; return
            if s == st["target"]: return
            if s == st["me"]:
                if not settings["ignore_self"]: st["target"] = s
            elif API.FindMobile(s) is not None: st["target"] = s
        def sync_party():
            party = set(int(x) for x in (API.GetPartyMemberSerials() or []) if int(x) and int(x) != st["me"])
            st["party"] = party; changed = False; dismissed = st["dismissed"]
            if dismissed:
                if settings["party"]: dismissed &= party
                else: dismissed.clear()
            if settings["party"]:
                for s in party:
                    if s in dismissed: continue
                    if not any(t["serial"] == s for t in tracked) and len(tracked) < MAX_TRACKED:
                        tracked.append({"serial": s, "auto": True, "name": st["names"].get(s) or "Party member"})
                        changed = True
            for t in list(tracked):
                if t["auto"] and (t["serial"] not in party or not settings["party"]): tracked.remove(t); changed = True
            if changed: save_tracked(); build_window(); HOST.refresh_settings(KEY)
        class Bridge(object):
            ok = None; parts = Tex.parts; creatures = False
            @staticmethod
            def find():
                if Bridge.ok is None:
                    Bridge.ok = Tex.find()
                    if Bridge.ok: Bridge.creatures = bool(safe(Bridge.find_creatures, False))
                return Bridge.ok
            @staticmethod
            def find_creatures():
                import clr; import System; from System.Reflection.Emit import DynamicMethod, OpCodes; p = Bridge.parts
                p["uo"] = Tz.get(Tz.get(None, "Game", Client._type("ClassicUO.Client")), "UO")
                p["anims"] = instance_member(p["uo"], "Animations")
                p["hues"] = instance_member(instance_member(p["uo"], "FileManager"), "Hues")
                p["hue_color"] = p["hues"].GetType().GetMethod("GetHueColorRgba8888")
                world_t = Client._type("ClassicUO.Game.World")
                p["world"] = world_t.GetProperty("Instance").GetValue(None, None)
                p["get_entity"] = world_t.GetMethod("Get", System.Array[System.Type]([clr.GetClrType(System.UInt32)]))
                mobile_t = Client._type("ClassicUO.Game.GameObjects.Mobile")
                p["group_for"] = mobile_t.GetMethod("GetGroupForAnimation")
                p["get_data"] = [m for m in p["tex_t"].GetMethods()
                                 if m.Name == "GetData" and m.IsGenericMethodDefinition
                                 and len(m.GetParameters()) == 5][0].MakeGenericMethod(clr.GetClrType(System.UInt32))
                anims_t = p["anims"].GetType(); get_frames = anims_t.GetMethod("GetAnimationFrames")
                sprite_t = Client._type("ClassicUO.Renderer.SpriteInfo"); span_t = get_frames.ReturnType
                obj_t, u16, u8, i32 = (clr.GetClrType(System.Object), clr.GetClrType(System.UInt16),
                                       clr.GetClrType(System.Byte), clr.GetClrType(System.Int32))
                dm = DynamicMethod("vauf_frame", obj_t, System.Array[System.Type](
                    [anims_t, u16, u8, u8, i32, clr.GetClrType(System.Array[System.UInt16])]), obj_t.Module, True)
                il = dm.GetILGenerator(); span = il.DeclareLocal(span_t); hue = il.DeclareLocal(u16)
                uop = il.DeclareLocal(clr.GetClrType(System.Boolean)); none = il.DefineLabel()
                for op in (OpCodes.Ldarg_0, OpCodes.Ldarg_1, OpCodes.Ldarg_2, OpCodes.Ldarg_3): il.Emit(op)
                il.Emit(OpCodes.Ldloca_S, hue); il.Emit(OpCodes.Ldloca_S, uop); il.Emit(OpCodes.Ldc_I4_0)
                il.Emit(OpCodes.Ldc_I4_0); il.Emit(OpCodes.Callvirt, get_frames); il.Emit(OpCodes.Stloc, span)
                il.Emit(OpCodes.Ldloca_S, span); il.Emit(OpCodes.Call, span_t.GetProperty("Length").GetGetMethod())
                il.Emit(OpCodes.Ldarg_S, System.Byte(4)); il.Emit(OpCodes.Ble, none)
                il.Emit(OpCodes.Ldarg_S, System.Byte(5)); il.Emit(OpCodes.Ldc_I4_0); il.Emit(OpCodes.Ldloc, hue)
                il.Emit(OpCodes.Stelem_I2); il.Emit(OpCodes.Ldloca_S, span); il.Emit(OpCodes.Ldarg_S, System.Byte(4))
                il.Emit(OpCodes.Call, span_t.GetMethod("get_Item")); il.Emit(OpCodes.Ldobj, sprite_t)
                il.Emit(OpCodes.Box, sprite_t); il.Emit(OpCodes.Ret); il.MarkLabel(none); il.Emit(OpCodes.Ldnull)
                il.Emit(OpCodes.Ret); p["frame"] = dm
                return all(p[k] is not None for k in ("anims", "hues", "hue_color", "world",
                                                       "get_entity", "group_for", "get_data"))
            @staticmethod
            def creature_pixels(serial):
                import System; p = Bridge.parts
                mob = p["get_entity"].Invoke(p["world"], System.Array[System.Object]([System.UInt32(serial)]))
                if mob is None: return None
                graphic = int(mob.GetGraphicForAnimation())
                group = int(p["group_for"].Invoke(None, System.Array[System.Object]([mob, System.UInt16(0), True])))
                direction = int(mob.GetDirectionForAnimation()) & 0x7F
                hue_box = System.Array[System.UInt16]([System.UInt16(0)])
                sprite = p["frame"].Invoke(None, System.Array[System.Object](
                    [p["anims"], System.UInt16(graphic), System.Byte(group), System.Byte(direction), 0, hue_box]))
                if sprite is None or sprite.Texture is None: return None
                uv = sprite.UV; w, h = int(uv.Width), int(uv.Height)
                if w <= 0 or h <= 0: return None
                raw = System.Array[System.UInt32](w * h)
                p["get_data"].Invoke(sprite.Texture, System.Array[System.Object]([0, uv, raw, 0, w * h]))
                hue = int(mob.Hue); partial = (hue & 0x8000) != 0; hue &= 0x7FFF
                if hue == 0: hue = int(hue_box[0]); partial = False
                ramp = None
                if hue:
                    ramp = [int(p["hue_color"].Invoke(p["hues"], System.Array[System.Object](
                        [System.UInt16(i), System.UInt16(hue)]))) & 0xFFFFFF for i in range(32)]
                return raw, w, h, ramp, partial
            @staticmethod
            def on_main(fn):
                how, value = Client.on_main_ex(fn)
                if how == "ok": return value
                if how == "err" and isinstance(Client.exc, Exception): raise Client.exc
                raise Exception(Client.error or "can't reach the game thread")
            @staticmethod
            def gump_pixels(ids, hue, partial):
                import System
                for gid in ids:
                    args = System.Array[System.Object]([System.UInt32(gid), System.UInt16(hue & 0xFFFF),
                                                        bool(partial), None])
                    px = Bridge.parts["hued"].Invoke(Bridge.parts["gumps"], args); bounds = args[3]
                    if px is not None and len(px) and int(bounds.Width) > 0:
                        return px, int(bounds.Width), int(bounds.Height)
                return None
            @staticmethod
            def put_texture(name, w, h, pixels): Tex.put(name, w, h, pixels); st["textures"].add(name)
        def mute(ctrl): ctrl.SetAcceptMouseInput(False); return ctrl
        def _cov(d, s): v = 0.5 - d * s; return 0.0 if v <= 0 else (1.0 if v >= 1 else v)
        def _rr(u, v, box):
            x0, y0, x1, y1, r = box; qx = abs(u - (x0 + x1) * 0.5) - ((x1 - x0) * 0.5 - r)
            qy = abs(v - (y0 + y1) * 0.5) - ((y1 - y0) * 0.5 - r); ox = qx if qx > 0 else 0.0
            oy = qy if qy > 0 else 0.0; inside = qx if qx > qy else qy
            return math.sqrt(ox * ox + oy * oy) + (inside if inside < 0 else 0.0) - r
        def _smooth(a, b, x):
            t = (x - a) / (b - a); t = 0.0 if t < 0 else (1.0 if t > 1 else t); return t * t * (3 - 2 * t)
        def _metal(v): c = 132.0 - 62.0 * min(1.0, max(0.0, (v - 43.0) / 107.0)); return (c, c, c + 6.0)
        def _tire(dx, dy, r):
            cosd = (dx + dy) / r * SQRT_HALF; f = min(1.0, max(0.0, (cosd + 0.71) / 1.42))
            t = min(1.0, max(0.0, (r - 67.0) / 11.5)); dark = 44.0 * (t ** 1.2) * f
            return (128.0 - dark, 128.0 - dark, 134.0 - dark)
        def _gold(dx, dy, r):
            cosd = -(dx + dy) / r * SQRT_HALF; t = min(1.0, max(0.0, (r - 56.0) / 4.0))
            delta = t * (-42.0 + 57.0 * _smooth(-0.3, 0.75, cosd))
            return (min(255.0, 234.0 + delta), min(255.0, 203.0 + delta), min(255.0, 91.0 + delta * 0.65))
        def _over(acc, rgb, a):
            if a <= 0: return
            k = 1.0 - a; acc[0] = rgb[0] * a + acc[0] * k; acc[1] = rgb[1] * a + acc[1] * k
            acc[2] = rgb[2] * a + acc[2] * k; acc[3] = a + acc[3] * k
        def _erase(acc, a): k = 1.0 - a; acc[0] *= k; acc[1] *= k; acc[2] *= k; acc[3] *= k
        def frame_pixel(u, v, s):
            acc = [0.0, 0.0, 0.0, 0.0]
            if 140 <= u and 38 <= v <= 156:
                _over(acc, OUTLINE_RGB, _cov(_rr(u, v, PANEL), s))
                if acc[3] > 0:
                    _over(acc, _metal(v), _cov(_rr(u, v, METAL), s)); _over(acc, INNER_RGB, _cov(_rr(u, v, INNER), s))
                    hole = _cov(_rr(u, v, HOLES), s)
                    if hole > 0:
                        _erase(acc, hole)
                        for y0, y1 in SEPARATORS:
                            band = min(v - y0, y1 - v)
                            if band > -1.5: _over(acc, _metal(v), hole * _cov(-band, s))
                    for rx, ry, rgb in RIVETS:
                        if abs(u - rx) < 4 and abs(v - ry) < 4:
                            d = math.sqrt((u - rx) ** 2 + (v - ry) ** 2); _over(acc, (40, 40, 44), _cov(d - 2.6, s))
                            _over(acc, rgb, _cov(d - 1.6, s))
            dx, dy = u - RING_C[0], v - RING_C[1]; r = math.sqrt(dx * dx + dy * dy)
            if r < RING[0][0] + 2:
                for radius, color in RING:
                    a = _cov(r - radius, s)
                    if a <= 0: continue
                    if color == "tire": color = _tire(dx, dy, max(r, 0.01))
                    elif color == "gold": color = _gold(dx, dy, max(r, 0.01))
                    _over(acc, color, a)
                _erase(acc, _cov(r - HOLE_R, s))
            return acc
        def pack(acc):
            a = acc[3]
            if a <= 0.002: return 0
            return (int(acc[0] + 0.5) | (int(acc[1] + 0.5) << 8) | (int(acc[2] + 0.5) << 16) |
                    (int(a * 255 + 0.5) << 24))
        def draw_frame(s):
            w, h = int(ART_W * s), int(ART_H * s); inv = 1.0 / s; player = [0] * (w * h)
            for y in range(h):
                v = (y + 0.5) * inv; row = y * w
                for x in range(w): player[row + x] = pack(frame_pixel((x + 0.5) * inv, v, s))
                yield None
            target = []
            for y in range(h): target.extend(player[y * w:(y + 1) * w][::-1])
            yield w, h, player, target
        def draw_ring(s, rgb):
            outer = NOTO_RING[1] + 1; size = int(math.ceil(2 * outer * s)); half = size / 2.0
            pixels = [0] * (size * size)
            for y in range(size):
                if y % 4 == 3: yield None
                for x in range(size):
                    r = math.sqrt((x + 0.5 - half) ** 2 + (y + 0.5 - half) ** 2) / s
                    a = min(_cov(r - NOTO_RING[1], s), _cov(NOTO_RING[0] - r, s))
                    if a > 0: pixels[y * size + x] = pack([rgb[0] * a, rgb[1] * a, rgb[2] * a, a])
            yield size, pixels
        def art_names(s):
            tag = int(round(s * 100))
            return {"player": "%sframe_player_%d" % (TEX_PREFIX, tag),
                    "target": "%sframe_target_%d" % (TEX_PREFIX, tag), "blank": "%ssnap_blank_%d" % (TEX_PREFIX, tag)}
        def art_steps(s):
            names = art_names(s); got = None
            for got in draw_frame(s):
                if got is None: yield None
            w, h, player, target = got; size = snap_size(s)
            blank = [pack([SNAP_BG[0], SNAP_BG[1], SNAP_BG[2], 1.0])] * (size * size)
            for got in draw_ring(s, NO_NOTO):
                if got is None: yield None
            rsize, ring = got; ring_name = noto_name_of(NO_NOTO, s)
            def upload():
                Bridge.put_texture(names["player"], w, h, player); Bridge.put_texture(names["target"], w, h, target)
                Bridge.put_texture(names["blank"], size, size, blank); Bridge.put_texture(ring_name, rsize, rsize, ring)
            yield upload
        def want_art(s):
            if s in st["art_scales"]: return True
            if s in st["art_failed"]: return False
            if not any(j["kind"] == "art" and j["s"] == s for j in st["art_jobs"]):
                st["art_jobs"].append({"kind": "art", "s": s, "gen": art_steps(s)})
            return None
        def scales_in_use():
            out = set([settings["scale"] / 100.0])
            if settings["pscale_on"]: out.add(settings["pscale"] / 100.0)
            for v in fitst.values():
                if v is not None: out.add(v / 100.0)
            return out
        def prune_art():
            keep = scales_in_use(); keep.update(fr.get("s") for fr in frames.values() if fr.get("art"))
            gone = [s for s in st["art_scales"] if s not in keep]
            if not gone: return
            tags = set(str(int(round(s * 100))) for s in gone)
            kinds = tuple(TEX_PREFIX + k for k in ("frame_", "noto_", "snap_blank_"))
            names = [n for n in st["textures"] if n.startswith(kinds) and n.rsplit("_", 1)[-1] in tags]
            for s in gone: st["art_scales"].discard(s)
            for n in names: st["textures"].discard(n)
            if names: safe(lambda: Bridge.on_main(lambda: Tex.drop(names)))
        def noto_name_of(rgb, s):
            return "%snoto_%d_%d_%d_%d" % (TEX_PREFIX, rgb[0], rgb[1], rgb[2], int(round(s * 100)))
        def ring_steps(rgb, s, name):
            got = None
            for got in draw_ring(s, rgb):
                if got is None: yield None
            size, pixels = got; yield lambda: Bridge.put_texture(name, size, size, pixels)
        def noto_texture(rgb, s):
            name = noto_name_of(rgb, s)
            if name in st["textures"]: return name
            if name not in st["art_failed"] and not any(j.get("name") == name for j in st["art_jobs"]):
                st["art_jobs"].append({"kind": "noto", "s": s, "name": name, "gen": ring_steps(rgb, s, name)})
            return None
        def art_work(budget):
            jobs = st["art_jobs"]
            if not jobs: return False
            keep = scales_in_use(); keep.update(fr.get("s") for fr in frames.values())
            jobs[:] = [j for j in jobs if j["s"] in keep]; deadline = time.time() + budget
            while jobs:
                j = jobs[0]
                try: r = next(j["gen"])
                except Exception: r = False
                if r is None:
                    if time.time() >= deadline: return True
                    continue
                jobs.pop(0); ok = r is not False and bool(safe(lambda: Bridge.on_main(r) or True, False))
                if j["kind"] == "art":
                    (st["art_scales"] if ok else st["art_failed"]).add(j["s"]); st["art_dirty"] = True
                elif not ok: st["art_failed"].add(j["name"])
                else:
                    for fr in frames.values(): fr["last"] = None
                if time.time() >= deadline: break
            return bool(jobs)
        def snap_size(s): return int(math.ceil(2 * (HOLE_R + 2) * s))
        def snap_px(): return snap_size(max(scales_in_use()))
        def item_details(graphic, item):
            info = item_info.get(graphic)
            if info is None:
                data = item.GetItemData()
                if data is None: return 0, False, False
                info = item_info[graphic] = (int(data.AnimID or 0), bool(data.IsPartialHue), bool(data.IsContainer))
            return info
        def covered(layer, worn):
            robe = worn.get("robe", (0, 0))[0]
            if layer == "tunic": return worn.get("tunic", (0, 0))[0] == 0x0238 and robe and robe not in OPEN_ROBES
            if layer == "arms": return bool(robe) and robe not in OPEN_ROBES
            if layer == "torso":
                if robe and robe not in OPEN_ROBES: return True
                tunic = worn.get("tunic", (0, 0))[0]
                return bool(tunic) and tunic not in (0x1541, 0x1542) and \
                    worn.get("torso", (0, 0))[0] in (0x782A, 0x782B)
            if layer in ("helmet", "hair") and robe:
                if robe > 0x3173: return robe in (0x4B9D, 0x7816)
                if robe <= 0x2687: return robe >= 0x2683 or 0x204E <= robe <= 0x204F
                return robe in (0x2FB9, 0x3173)
            return False
        def read_paperdoll(serial):
            m = find_mobile(serial)
            if m is None: return None
            graphic = int(m.Graphic or 0); body = PAPERDOLL_BODY.get(graphic)
            if body is None: return {"body": 0, "pieces": ()}
            hue = GM_BODY_HUE if graphic == GM_BODY else int(m.Hue or 0) & 0x3FFF
            female = graphic in FEMALE_BODIES; worn, details = {}, {}
            for layer in LAYERS:
                it = API.FindLayer(layer, serial)
                if it is None: continue
                try:
                    ig = int(it.Graphic or 0); worn[layer] = (ig, int(it.Hue or 0) & 0x3FFF)
                    details[layer] = item_details(ig, it)
                except Exception: worn.pop(layer, None)
            order = LAYERS
            if "cloak" in worn:
                if worn.get("robe", (0, 0))[0] in PARROT_ROBES: order = LAYERS_PARROT
                elif details["cloak"][2]: order = LAYERS_QUIVER
            if worn.get("arms", (0, 0))[0] in PLATE_ARMS:
                order = tuple({"arms": "torso", "torso": "arms"}.get(l, l) for l in order)
            pieces = [((body,), hue, True)]
            for layer in order:
                if layer not in worn or covered(layer, worn): continue
                anim, partial, _container = details[layer]
                if not anim: continue
                if anim == 0x03CA and graphic in (0x02B6, 0x02B7): anim = 0x0223
                ids = (anim + FEMALE_GUMP, anim + MALE_GUMP) if female else (anim + MALE_GUMP, anim + FEMALE_GUMP)
                pieces.append((tuple(i for i in ids if i <= 0xFFFF), worn[layer][1], partial))
            return {"body": body, "pieces": tuple(pieces)}
        def fetch_layers(doll):
            def read():
                out = []
                for ids, hue, partial in doll["pieces"]:
                    got = Bridge.gump_pixels(ids, hue, partial)
                    if got is not None: out.append(got)
                return out
            return Bridge.on_main(read) or []
        def figure_bounds_steps(layers):
            top, left, right = None, None, None
            for px, w, h in layers:
                for y in range(h):
                    if y % 24 == 23: yield None
                    if top is not None and y > top + 120: break
                    row = y * w; first = -1
                    for x in range(w):
                        if (px[row + x] >> 24) & 0xFF > 127: first = x; break
                    if first < 0: continue
                    last = first
                    for x in range(w - 1, first, -1):
                        if (px[row + x] >> 24) & 0xFF > 127: last = x; break
                    if top is None or y < top: top = y
                    left = first if left is None else min(left, first)
                    right = last if right is None else max(right, last)
            yield (left, top, right)
        def crop_box(body, layers, bounds):
            if not body and layers:
                w, h = layers[0][1:]; size = max(w, h) * 1.08 * 100.0 / settings["pzoom"]
                return (w - size) / 2.0 + settings["pdx"], (h - size) / 2.0 + settings["pdy"], size
            size = SNAP_DEPTH * 100.0 / settings["pzoom"]
            if bounds is None or bounds[1] is None: cx, cy = 98, 70; x0, y0 = cx - size / 2.0, cy - size / 2.0
            else: left, top, right = bounds; x0 = (left + right + 1) / 2.0 - size / 2.0; y0 = top - 2
            return x0 + settings["pdx"], y0 + settings["pdy"], size
        def compose_steps(raw_layers, body, out):
            layers = []; keep = isinstance(raw_layers, list)
            for i, (px, w, h) in enumerate(raw_layers):
                if isinstance(px, list): layers.append((px, w, h))
                else:
                    conv = (list(px), w, h); layers.append(conv)
                    if keep: raw_layers[i] = conv
                yield None
            bounds = None
            if body and layers:
                for r in figure_bounds_steps(layers):
                    if r is None: yield None
                    else: bounds = r
            x0, y0, size = crop_box(body, layers, bounds); side = int(math.ceil(size)) + 1
            ix0, iy0 = int(math.floor(x0)), int(math.floor(y0)); bg = SNAP_BG; buf = [bg] * (side * side)
            for px, w, h in layers:
                for y in range(side):
                    if y % 16 == 15: yield None
                    sy = iy0 + y
                    if sy < 0 or sy >= h: continue
                    src = sy * w; dst = y * side
                    for x in range(side):
                        sx = ix0 + x
                        if 0 <= sx < w:
                            p = px[src + sx]
                            if (p >> 24) & 0xFF > 127: buf[dst + x] = (p & 0xFF, (p >> 8) & 0xFF, (p >> 16) & 0xFF)
            step = size / float(out); offs = (0.25, 0.75); pixels = [0] * (out * out)
            for oy in range(out):
                if oy % 8 == 7: yield None
                for ox in range(out):
                    r = g = b = 0
                    for fy in offs:
                        yy = int(y0 + (oy + fy) * step) - iy0; yy = 0 if yy < 0 else (side - 1 if yy >= side else yy)
                        for fx in offs:
                            xx = int(x0 + (ox + fx) * step) - ix0
                            xx = 0 if xx < 0 else (side - 1 if xx >= side else xx); c = buf[yy * side + xx]; r += c[0]
                            g += c[1]; b += c[2]
                    pixels[oy * out + ox] = ((r >> 2) | ((g >> 2) << 8) | ((b >> 2) << 16) | (0xFF << 24))
            yield pixels
        def want_snapshot(serial):
            if serial and (serial not in st["snaps"] or serial in st["stale"]) and \
                    not any(q[0] == serial for q in st["snap_queue"]):
                job = st["snap_job"]
                if job is not None and job.get("serial") == serial: return
                st["snap_queue"].append((serial, 0.0))
        def hue_steps(got, job):
            raw, w, h, ramp, partial = got; pixels = list(raw); yield None
            if ramp:
                for i, px in enumerate(pixels):
                    if i % 4096 == 4095: yield None
                    a = px & 0xFF000000
                    if not a: continue
                    r, g, b = px & 0xFF, (px >> 8) & 0xFF, (px >> 16) & 0xFF
                    if partial and (r != g or r != b): continue
                    pixels[i] = ramp[r >> 3] | a
            job["layers"] = [(pixels, w, h)]
            for r in compose_steps(job["layers"], 0, job["size"]): yield r
        def snapshot_work(now, budget=0.008):
            job = st["snap_job"]
            if job is None: return False
            deadline = now + budget
            while st["snap_job"] is job:
                try: r = next(job["gen"])
                except StopIteration: st["snap_job"] = None; return False
                except Exception:
                    st["snap_job"] = None
                    if not any(q[0] == job["serial"] for q in st["snap_queue"]):
                        st["snap_queue"].append((job["serial"], now + SNAP_RETRY))
                    return False
                if r is not None:
                    st["snap_job"] = None
                    serial, name, size = job["serial"], "%ssnap_%d" % (TEX_PREFIX, job["serial"]), job["size"]
                    if safe(lambda: Bridge.on_main(lambda: Bridge.put_texture(name, size, size, r)) or True, False):
                        st["snaps"][serial] = {"name": name, "creature": False}
                        if serial == st["me"] and cfg.f is not None: page["layers"] = (job["layers"], job["body"])
                        mark_frames(serial)
                    return False
                if time.time() >= deadline: return True
        def take_next_snapshot(now):
            if st["snap_job"] is not None: return
            for i, (serial, due) in enumerate(st["snap_queue"]):
                if due <= now: del st["snap_queue"][i]; break
            else: return
            if serial in st["snaps"] and serial not in st["stale"]: return
            doll = read_paperdoll(serial)
            if doll is None: st["snap_queue"].append((serial, now + SNAP_RETRY)); return
            st["stale"].discard(serial); size = snap_px()
            if not doll["body"]:
                got = safe(lambda: Bridge.on_main(lambda: Bridge.creature_pixels(serial))) if Bridge.creatures else None
                if got is None:
                    if Bridge.creatures and st["snap_tries"].get(serial, 0) < 3:
                        st["snap_tries"][serial] = st["snap_tries"].get(serial, 0) + 1
                        st["snap_queue"].append((serial, now + SNAP_RETRY)); return
                    st["snaps"][serial] = {"name": None, "creature": True}; mark_frames(serial); return
                job = {"serial": serial, "size": size, "layers": None, "body": 0}; job["gen"] = hue_steps(got, job)
                st["snap_job"] = job; return
            layers, body = safe(lambda: fetch_layers(doll), []), doll["body"]
            if not layers: st["snap_queue"].append((serial, now + SNAP_RETRY)); return
            st["snap_job"] = {"gen": compose_steps(layers, body, size), "serial": serial,
                              "size": size, "layers": layers, "body": body}
        def mark_frames(serial):
            for key, fr in frames.items():
                if frame_serial(key) == serial: fr["last"] = None
        def retake_all():
            st["stale"] = set(st["snaps"])
            for key in frames: want_snapshot(frame_serial(key))
        SNAP_KEEP = 8
        def note_shown(serial):
            rec = st["recent"]
            if not serial or (rec and rec[-1] == serial): return
            if serial in rec: rec.remove(serial)
            rec.append(serial)
            if len(rec) > 4 * SNAP_KEEP: del rec[:-SNAP_KEEP]
        def prune_people():
            keep = set(frame_serial(k) for k in frames); keep.update(t["serial"] for t in tracked)
            keep.update(st["party"]); keep.update(st["recent"][-SNAP_KEEP:]); keep.add(st["me"])
            in_use = set(fr.get("snap") for fr in frames.values()); snaps = st["snaps"]; names = []
            for serial in [s for s in snaps if s not in keep]:
                name = snaps[serial].get("name")
                if name and name in in_use: continue
                del snaps[serial]
                if name: names.append(name); st["textures"].discard(name)
            for d in (st["names"], st["snap_tries"]):
                for serial in [s for s in d if s not in keep]: del d[serial]
            st["stale"] = set(s for s in st["stale"] if s in snaps); q = st["snap_queue"]
            if any(e[0] not in keep for e in q): q[:] = [e for e in q if e[0] in keep]
            if names and st["art"]: safe(lambda: Bridge.on_main(lambda: Tex.drop(names)))
        def frame_style(key): return "target" if key == "target" else "player"
        def frame_serial(key):
            if key == "player": return st["me"]
            if key == "target": return st["target"]
            return int(key[1:])
        fitst = {"player": None, "target": None}; fitbox = {"player": None, "target": None}; ZONE_PAD = Kit.MARGIN + 2
        def frame_scale(key):
            fit = fitst.get(key)
            if fit is not None: return fit / 100.0
            if settings["pscale_on"] and key[:1] == "m" and key[1:].isdigit() and int(key[1:]) in st["party"]:
                return settings["pscale"] / 100.0
            return settings["scale"] / 100.0
        def frame_fit(key):
            def fit(w, h, mode):
                want = None; box = None
                if w and h:
                    box = (int(w), int(h)); iw, ih = box[0] - 2 * ZONE_PAD, box[1] - 2 * ZONE_PAD
                    pct = int(min(100.0 * float(iw) / ART_W, 100.0 * float(ih) / ART_H))
                    if rides_inside(key): pct = min(pct, int(100.0 * (ih - Kit.GAP - PIECE_IN) / PANEL[3]))
                    want = max(SCALE_MIN, min(SCALE_MAX, pct))
                fitbox[key] = box
                if want != fitst.get(key): fitst[key] = want; st["art_dirty"] = True
            return fit
        def content_h(s): return max(ART_H * s, PANEL[3] * s + Kit.GAP + PIECE_IN)
        def frame_hug(key):
            def hug(h):
                ih = int(h) - 2 * ZONE_PAD; pct = 100.0 * ih / ART_H; inside = rides_inside(key)
                if inside: pct = min(pct, 100.0 * (ih - Kit.GAP - PIECE_IN) / PANEL[3])
                s = max(SCALE_MIN, min(SCALE_MAX, int(pct))) / 100.0
                need = max(ART_W * s, PANEL[0] * s + (161 - 2 * Kit.MARGIN) + 4) if inside else ART_W * s; want_h = 0
                if inside:
                    hh = int(math.ceil(content_h(s))) + 2 * ZONE_PAD + 1
                    if hh > int(h): want_h = hh
                return int(math.ceil(need)) + 2 * ZONE_PAD, want_h
            return hug
        def rides_inside(key):
            for pkey, (fk, order, getter) in PIECES["piece"].items():
                if fk == key and order == 0: return True
            return False
        def frame_box(key, w, h):
            box = fitbox.get(key)
            if not box: return w, h, 0, 0, False
            W, H = max(box[0], w + 2 * ZONE_PAD), max(box[1], h + 2 * ZONE_PAD)
            ox = ZONE_PAD if frame_style(key) == "player" else W - ZONE_PAD - w; ch = h
            if rides_inside(key): ch = max(h, int(math.ceil(content_h(float(h) / ART_H))))
            return W, H, ox, max(ZONE_PAD if ch > h else 0, (H - ch) // 2), True
        def frame_span(key):
            def get():
                fr = frames.get(key)
                if not fr or not fr.get("box"): return None
                ox, _oy, w, _h = fr["box"]; s = fr["s"]; lo, hi = int(round(PANEL[0] * s)), int(round(PANEL[2] * s))
                if frame_style(key) == "player": return ox + lo, ox + hi, True
                return ox + w - hi, ox + w - lo, False
            return get
        def frame_inner(key):
            def get():
                fr = frames.get(key)
                if not fr or not fr.get("slot") or not fr.get("box"): return None
                _ox, oy, _w, h = fr["box"]; W, H = fr["win"]
                return ZONE_PAD, W, H, oy, h, oy + int(round(PANEL[3] * fr["s"]))
            return get
        def frame_size(key): s = frame_scale(key); return s, int(ART_W * s), int(ART_H * s)
        def mirror_x(style, w, x0, x1): return (x0, x1) if style == "player" else (w - x1, w - x0)
        def default_pos(key):
            _s, w, h = frame_size(key)
            if key == "player": return 60, 420
            if key == "target": return 60 + w + 20, 420
            i = [t["serial"] for t in tracked].index(int(key[1:])) if key[1:].isdigit() else 0
            return 60 + (i // 4) * (w + 10), 40 + (i % 4) * (h + 2)
        def follow_or(serial, action=None):
            def h(*a):
                if Follow.alt_held(): queue(("follow_serial", serial))(); return
                if action: queue(action)()
            return h
        def frame_clicked(key):
            def handler():
                fr = frames.get(key); g = fr and fr.get("g")
                if not g: return
                alt = Follow.alt_held(); removing = not alt and not settings["click"] and st.get("removing")
                if not alt and not settings["click"] and not removing: return
                p = frame_at(fr)
                if p != fr.get("seen") or time.time() < fr.get("drag_until", 0.0): fr["seen"] = p; return
                queue(("follow" if alt else ("remove_click" if removing else "click"), key))()
            return handler
        def frame_disposed(key, g):
            def handler(*args):
                fr = frames.get(key)
                if fr is not None and fr.get("g") is g and not st["shutting"]:
                    fr["g"] = None; st["queue"].append(("closed", key))
            return handler
        def color_box(g, x, y, w, h, rgb, alpha=1.0):
            box = G.CreateGumpColorBox(alpha, "#%02x%02x%02x" % rgb); box.SetRect(x, y, w, h); g.Add(mute(box))
            return box
        def add_bars(g, c, rows):
            for row, (rx0, ry0, rx1, ry1) in zip(ROWS, rows):
                for v in (("hits", "poison", "yellow") if row == "hits" else (row,)):
                    pb = G.CreateGumpSimpleProgressBar(rx1 - rx0, ry1 - ry0, BAR_BG, BAR_COLOR[v], 0, 100)
                    pb.SetPos(rx0, ry0); g.Add(mute(pb)); c["bar_" + v] = pb
        def build_frame(key):
            old = frames.get(key, {}).get("g"); s, w, h = frame_size(key); style = frame_style(key)
            x, y = st["pos"].get(key) or default_pos(key)
            if Kit.is_open(old): x, y = old.GetX(), old.GetY()
            if key in frames: frames[key]["g"] = None
            sx = lambda v: int(round(v * s)); art = bool(st["art"]) and s in st["art_scales"]
            W, H, ox, oy, zoned = frame_box(key, w, h); g = G.CreateGump(True, not settings["lock"])
            x, y = Kit.place(g, x, y, W, H); c = {}
            if zoned: M = Kit.MARGIN; Kit.add_window_frame(g, W, H); Kit.add_section(g, M, M, W - 2 * M, H - 2 * M)
            cx = ox + (sx(RING_C[0]) if style == "player" else w - sx(RING_C[0])); cy = oy + sx(RING_C[1])
            rx0, rx1 = mirror_x(style, w, sx(ART_ROWS_X[0]), sx(ART_ROWS_X[1]))
            rows = [(ox + rx0, oy + sx(y0), ox + rx1, oy + sx(y1)) for y0, y1 in ART_ROWS_Y]; hole = int(HOLE_R * s)
            names = art_names(s) if art else None
            if art:
                size = snap_size(s)
                c["snap"] = Tex.control(g, names["blank"], cx - size // 2, cy - size // 2, size, size)
                add_bars(g, c, rows); Tex.control(g, names[style], ox, oy, w, h)
                ring = int(math.ceil(2 * (NOTO_RING[1] + 1) * s))
                c["noto"] = Tex.control(g, noto_name_of(NO_NOTO, s), cx - ring // 2, cy - ring // 2, ring, ring)
            else:
                if not zoned: Kit.add_window_frame(g, w, h, corners=False)
                side = 2 * hole; Kit.add_section(g, cx - hole, cy - hole, side, side, alpha=0.95)
                e = max(2, int(round(3 * s)))
                c["edge"] = [color_box(g, cx - hole, cy - hole, side, e, NO_NOTO),
                             color_box(g, cx - hole, cy + hole - e, side, e, NO_NOTO),
                             color_box(g, cx - hole, cy - hole, e, side, NO_NOTO),
                             color_box(g, cx + hole - e, cy - hole, e, side, NO_NOTO)]
                Kit.add_section(g, rows[0][0] - 4, rows[0][1] - 4, rows[0][2] - rows[0][0] + 8,
                                rows[-1][3] - rows[0][1] + 8, alpha=0.9)
                add_bars(g, c, [(a, b + 1, cc, d - 1) for a, b, cc, d in rows])
            c["strip"] = color_box(g, cx - 22, cy + int(hole * 0.42), 44, LABEL_H + 4, (0, 0, 0), 0.65)
            c["strip"].IsVisible = False
            tip = None if key == "player" else ("Click: make them your target. Alt+click: auto-follow (again to stop)"
                 if settings["click"] else "Alt+click: auto-follow (again to stop)")
            Kit.catcher(g, ox, oy, w, h, frame_clicked(key), None, movable=not settings["lock"])
            px0, px1 = mirror_x(style, w, sx(PANEL[0]), sx(PANEL[2]))
            Kit.catcher(g, ox + px0, oy + sx(PANEL[1]), px1 - px0, sx(PANEL[3]) - sx(PANEL[1]),
                        frame_clicked(key), tip, movable=not settings["lock"])
            add_close_x(g, key, ox, oy)
            for name in ("name", "hits", "mana", "stam", "status", "portrait_text"):
                c["lbl_" + name] = mute(Kit.add_label(g, "", 0, 0))
            guard_at = None
            if key == "player":
                c["guard_bg"] = color_box(g, 0, 0, 1, 1, (0, 0, 0), 0.65); c["guard_bg"].IsVisible = False
                c["lbl_guard"] = mute(Kit.add_label(g, "", 0, 0))
                guard_at = (ox + sx(PANEL[2]) - 6, oy + max(1, sx(PANEL[1]) - LABEL_H - 3))
            frames[key] = {"g": g, "c": c, "rows": rows, "centre": (cx, cy), "hole": hole, "s": s,
                           "art": art, "names": names, "last": None, "seen": (x, y), "noto": None,
                           "variant": None, "snap": None, "code_move": False, "shown": {}, "bars": {}, "serial": None, 
                           "box": (ox, oy, w, h), "win": (W, H), "slot": fitbox.get(key), "rides": rides_inside(key)}
            if guard_at is not None: frames[key]["guard_at"] = guard_at
            st["art_dirty"] = True; G.AddControlOnDisposed(g, frame_disposed(key, g)); G.AddGump(g)
            Kit.no_snap(g); Kit.on_moved(g, frame_moved(key)); Kit.dispose(old)
        def frame_moved(key):
            def handler():
                fr = frames.get(key)
                if fr is None or not Kit.is_open(fr.get("g")): return
                p = frame_at(fr)
                if p is not None and p != fr.get("seen"): fr["seen"] = p; fr["code_move"] = True; note_pos(key, p)
                save_positions()
            return handler
        def add_close_x(g, key, ox, oy):
            if key in ("player", "target"): return
            art = CLOSE_ART if Kit.pic_size(CLOSE_ART[0])[0] > 0 else Kit.ART_CLOSE
            x, y, fn = ox + CLOSE_INSET, oy + CLOSE_INSET, follow_or(int(key[1:]), ("xclose", key))
            tip = "Close this frame. Alt+click: auto-follow (again to stop)"
            if Kit.pic_size(art[0])[0] > 0:
                b = G.CreateGumpButton("", Kit.HUE_TEXT, art[0], art[1], art[2]); b.SetPos(x, y); g.Add(b)
                Kit.on_click(b, fn); b.SetTooltip(tip); return
            Kit.add_label(g, "x", x + 2, y, Kit.HUE_TITLE)
            Kit.catcher(g, x, y, max(14, Kit.text_w("x") + 4), 16, fn, tip)
        def close_frame(key):
            fr = frames.pop(key, None)
            if fr:
                st["art_dirty"] = True; g = fr.get("g")
                if Kit.is_open(g):
                    p = frame_at(fr)
                    if p is not None: note_pos(key, p)
                fr["g"] = None; Kit.dispose(g)
        def supplies_spot(w, h, side, p=None):
            fr = frames.get("player")
            if fr is None or not Kit.is_open(fr.get("g")): return None
            if p is None: p = frame_at(fr)
            if p is None: return None
            fx, fy = p; fw, fh = fr.get("win") or frame_size("player")[1:]; W, H = Kit.screen()
            if side == 1:
                at = (fx - w - 2, fy)
                if at[0] < 0: at = (fx + fw + 2, fy)
            elif side == 2:
                at = (fx + fw + 2, fy)
                if W > 0 and at[0] + w > W: at = (fx - w - 2, fy)
            else:
                below, above = cast_reserve(fy, fh); y_below = fy + fh + 2 + below + pieces_extent("player", True)
                at = (fx, y_below)
                if H > 0 and y_below + h > H:
                    y_above = fy - h - 2 - above - pieces_extent("player", False)
                    if y_above >= 0 or y_above + h > H - y_below: at = (fx, y_above)
            x, y = at
            if W > 0: x = max(0, min(x, W - w))
            if H > 0: y = max(0, min(y, H - h))
            return (x, y)
        HBAR_VAR = "UnitFrames_hbar_held"; HBAR_EVERY = 1.0; hbar = {"at": 0.0}
        def hbar_profile():
            try: return Tz.get(None, "CurrentProfile", Tz.T("ClassicUO.Configuration.ProfileManager"))
            except Exception: return None
        def hbar_sync(want):
            prof = hbar_profile()
            if prof is None: return
            held = _get(HBAR_VAR) == "1"
            if want:
                if not held and not bool(Tz.get(prof, "OpenHealthBarForLastAttack")): return
                if not held: Tz.put(prof, "OpenHealthBarForLastAttack", False); _put(HBAR_VAR, "1")
                try:
                    t = Tz.T("ClassicUO.Game.UI.Gumps.BaseHealthBarGump"); bar = Tz.get(None, "LastAttackBar", t)
                    if bar is not None and not bar.IsDisposed: bar.Dispose()
                except Exception: pass
            elif held: Tz.put(prof, "OpenHealthBarForLastAttack", True); _put(HBAR_VAR, "")
        def hbar_tick(now):
            if 0 <= hbar["at"] - now <= HBAR_EVERY: return
            hbar["at"] = now + HBAR_EVERY; safe(lambda: hbar_sync(bool(settings["hide_bar"] and settings["target"])))
        def player_anchor(w, h, side):
            fr = frames.get("player")
            if fr is None or not Kit.is_open(fr.get("g")): return None
            p = fr.get("seen"); sig = None
            if p is not None:
                sig = (p, fr.get("win") or frame_size("player")[1:], side, settings["cast"],
                       PIECES["stack"].get("player"), Kit.screen(), w, h)
            if sig is None or sig != anchor["sig"] or anchor["at"] is None:
                anchor["at"] = supplies_spot(w, h, side, p); anchor["sig"] = sig if anchor["at"] is not None else None
            at = anchor["at"]; return None if at is None else (fr["g"], at)
        def cast_reserve(fy, fh):
            if not settings["cast"]: return 0, 0
            H = Kit.screen()[1]
            if H > 0 and fy + fh + CAST_GAP + CAST_H > H: return 0, CAST_H + CAST_GAP
            return CAST_H + CAST_GAP, 0
        def cast_spot(fr):
            p = fr.get("seen")
            if p is None: return None
            _ox, oy, _fw, fh = fr.get("box") or (0, 0, 0, frame_size("player")[2]); top = p[1] + oy
            below, _above = cast_reserve(top, fh); x = p[0] + fr["rows"][0][0] - 6
            wh = (fr.get("win") or frame_size("player")[1:])[1]
            if below:
                extra = pieces_extent("player", True); y = top + fh + CAST_GAP
                if extra: y = max(y, p[1] + wh + extra + CAST_GAP)
                return x, y
            extra = pieces_extent("player", False); y = top - CAST_H - CAST_GAP
            if extra: y = min(y, p[1] - extra - CAST_H - CAST_GAP)
            return x, y
        def drop_cast(): g, cast["g"] = cast["g"], None; cast["leader"] = None; cast["shown"] = None; Kit.dispose(g)
        def build_cast(fr):
            drop_cast(); rows = fr["rows"]; w, h = rows[0][2] - rows[0][0] + 12, CAST_H; g = G.CreateGump(False, False)
            Kit.add_window_frame(g, w, h, corners=False, mouse=False); c = {}
            for k in ("cast", "done", "fail"):
                pb = G.CreateGumpSimpleProgressBar(w - 12, h - 10, BAR_BG, CAST_COLOR[k], 0, 100); pb.SetPos(6, 5)
                g.Add(mute(pb)); c[k] = pb
            c["lbl"] = mute(Kit.add_label(g, "", 6, 4)); at = cast_spot(fr) or (0, 0); Kit.place(g, at[0], at[1], w, h)
            G.AddGump(g); g.IsVisible = False; Kit.attach(g, fr["g"])
            cast.update({"g": g, "c": c, "shown": None, "at": at, "leader": fr["g"], "s": fr["s"], "w": w})
        def cast_tick(now):
            fr = frames.get("player")
            if not settings["cast"] or fr is None or not Kit.is_open(fr.get("g")):
                cast["state"] = None; st["jr"] = None
                if cast["g"] is not None: drop_cast()
                return
            lines = None
            if st["jr"] is None: st["jr"] = Journal.reader()
            else: lines = st["jr"].new()
            if lines:
                me_name = st["names"].get(st["me"]) or ""
                for ln in lines:
                    name = ln.name or ""
                    if me_name and name == me_name:
                        sp = SPELLS.get(ln.low.strip())
                        if sp is not None:
                            info = Kit.spell_info(sp[0]); secs = info[3] if info and info[3] else 1.0
                            cast.update({"spell": sp[0], "start": min(now, ln.at or now),
                                         "secs": max(0.1, float(secs)), "state": "cast", "pct": 0, "word": ""})
                            continue
                    elif name and name != "System": continue
                    if cast["spell"] is None or now - cast["start"] > cast["secs"] + CAST_FAIL_WINDOW: continue
                    low = ln.low
                    for text, word in CAST_FAIL_TEXTS:
                        if low.startswith(text):
                            if cast["state"] != "cast": cast["pct"] = 100
                            cast.update({"state": "fail", "word": word, "until": now + CAST_HOLD}); break
            state = cast["state"]
            if state == "cast":
                el = now - cast["start"]
                if el >= cast["secs"]: cast.update({"state": "done", "until": now + CAST_HOLD, "pct": 100})
                else: cast["pct"] = max(0, int(100 * el / cast["secs"]))
            elif state is not None and now >= cast["until"]: cast["state"] = None
            d = fr["last"][5] if fr.get("last") else None
            if d is not None and d[M_DEAD]: cast["state"] = None
            draw_cast(fr)
        def draw_cast(fr):
            state = cast["state"]; g = cast["g"]
            if state is None:
                if g is not None and cast["shown"] is not None: cast["shown"] = None; Kit.set(g, "IsVisible", False)
                return
            if g is None or not Kit.is_open(g) or cast["s"] != fr["s"] or cast["leader"] is not fr["g"]:
                build_cast(fr); g = cast["g"]
            at = cast_spot(fr)
            if at is not None and at != cast["at"]:
                cast["at"] = at; g.SetRect(at[0], at[1], cast["w"], CAST_H); Kit.moved_by_code(g)
            label = cast["spell"] if state != "fail" else "%s: %s" % (cast["spell"], cast["word"])
            want = (state, cast["pct"], label); old = cast["shown"]
            if want == old: return
            cast["shown"] = want; c = cast["c"]
            if old is None or old[0] != state:
                for k in ("cast", "done", "fail"): c[k].IsVisible = k == state
            if old is None or old[0] != state or old[1] != want[1]: c[state].SetProgress(float(want[1]), 100.0)
            if old is None or old[2] != label:
                text = Kit.fit(label, cast["w"] - 16); Kit.set_text(c["lbl"], text, Kit.HUE_TEXT)
                c["lbl"].SetPos(max(6, (cast["w"] - TEXT_PX(text)) // 2), 4)
            if old is None: g.IsVisible = True
        def guard_tick(now):
            if not settings["guard"]: st["guard"] = False
            elif now >= st["next_guard"]: st["next_guard"] = now + 0.5; st["guard"] = HOST.guarded()
            fr = frames.get("player")
            if fr is None or "guard_at" not in fr or not Kit.is_open(fr.get("g")): return
            gd = st["guard"]
            if gd is None: text, hue = "?", Kit.HUE_INFO
            elif gd: text, hue = "GUARDED", Kit.HUE_GOOD
            else: text, hue = "", Kit.HUE_TEXT
            x1, y = fr["guard_at"]; place(fr, "guard", text, x1, y, hue, "right")
            if fr["shown"].get("guard_bg") != text:
                fr["shown"]["guard_bg"] = text; box = fr["c"]["guard_bg"]
                if text: tw = Kit.text_w(text) + 8; Kit.ui_rect(box, x1 - tw + 4, y - 1, tw, LABEL_H + 4)
                box.IsVisible = bool(text)
        def place(fr, name, text, x, y, hue, align="left"):
            if align == "right": x -= TEXT_PX(text) if text else 0
            elif align == "center": x -= (TEXT_PX(text) if text else 0) // 2
            want = (text, hue, int(x), int(y)); shown = fr["shown"]; old = shown.get(name)
            if old == want: return
            shown[name] = want; lbl = fr["c"]["lbl_" + name]; Kit.set_text(lbl, text, hue)
            if old is None or old[2] != want[2] or old[3] != want[3]: Kit.ui_pos(lbl, want[2], want[3])
        def set_bar(fr, variant, cur, mx):
            want = (float(max(0, cur)), float(max(1, mx)))
            if fr["bars"].get(variant) == want: return
            pb = fr["c"].get("bar_" + variant)
            if pb is not None: pb.SetProgress(want[0], want[1]); fr["bars"][variant] = want
        def show_hits_variant(fr, want):
            if fr["variant"] == want: return
            fr["variant"] = want
            for v in ("hits", "poison", "yellow"):
                pb = fr["c"].get("bar_" + v)
                if pb is not None:
                    pb.IsVisible = v == want
                    if v != want: pb.SetProgress(0.0, 1.0); fr["bars"][v] = (0.0, 1.0)
        def set_noto(fr, rgb):
            if fr["noto"] == rgb: return
            c = fr["c"]
            if fr["art"]:
                name = noto_texture(rgb, fr["s"])
                if name is None: return
                c["noto"].TextureName = name
            else:
                for box in c["edge"]: box.SetBaseColor(rgb[0], rgb[1], rgb[2], 255)
            fr["noto"] = rgb
        def set_snapshot(fr, serial):
            if not fr["art"]: return {}
            empty = not serial
            if fr["shown"].get("snap_hidden") != empty:
                fr["shown"]["snap_hidden"] = empty; fr["c"]["snap"].IsVisible = not empty
            if empty: return {}
            want_snapshot(serial); snap = st["snaps"].get(serial) or {}; name = snap.get("name") or fr["names"]["blank"]
            if fr["snap"] != name: fr["snap"] = name; fr["c"]["snap"].TextureName = name
            return snap
        def pct(cur, mx): return int(round(100.0 * cur / mx)) if mx > 0 else 0
        def update_frame(key):
            fr = frames.get(key)
            if fr is None or not Kit.is_open(fr.get("g")): return
            serial = frame_serial(key)
            if serial != fr["serial"]: fr["serial"] = serial; note_shown(serial)
            d = read_mobile(serial); is_self = serial == st["me"]
            highlight = key != "target" and serial and serial == st["target"]; snap = set_snapshot(fr, serial)
            c = fr["c"]; state = (serial, highlight, settings["numbers"], fr["snap"], bool(snap.get("creature")), d)
            if state == fr["last"]: return
            fr["last"] = state; hue = Kit.HUE_TITLE if highlight else Kit.HUE_TEXT; status, portrait_text = "", ""
            if not serial or d is None:
                noto, hue, bars, variant = NO_NOTO, Kit.HUE_INFO, ((0, 1),) * 3, "hits"
                if not serial: name, vals = "", ("", "", ""); portrait_text = "No target"
                else: name, vals = st["names"].get(serial) or "Unknown", ("Out of range", "", "")
            else:
                dead = d[M_DEAD]; name = d[M_NAME] or st["names"].get(serial) or "Unknown"
                variant = "poison" if d[M_POISON] else ("yellow" if d[M_YELLOW] else "hits")
                bars = ((d[M_HITS], d[M_HMAX]), (d[M_MANA], d[M_MMAX]), (d[M_STAM], d[M_SMAX]))
                noto = NO_NOTO if dead else NOTO_COLOR.get(d[M_NOTO], NOTO_COLOR["gray"])
                status = "DEAD" if dead else ("PARA" if d[M_PARA] else "")
                if snap.get("creature"): portrait_text = "No picture"
                vals = []
                for i, (cur, mx) in enumerate(bars):
                    if mx <= 0: vals.append("" if i else "--")
                    elif is_self or i: vals.append("%d/%d" % (cur, mx))
                    else: vals.append("%d%%" % pct(cur, mx))
                if dead: vals[0] = "Dead"
                vals = tuple(vals)
            if not settings["numbers"] and vals and vals[0] != "Out of range": vals = ("", "", "")
            show_hits_variant(fr, variant); set_bar(fr, variant, bars[0][0], bars[0][1])
            set_bar(fr, "mana", bars[1][0], bars[1][1]); set_bar(fr, "stam", bars[2][0], bars[2][1]); set_noto(fr, noto)
            rows = fr["rows"]
            for i, row in enumerate(ROWS):
                x0, y0, x1, y1 = rows[i]
                place(fr, row, vals[i], x1 - 8, y0 + (y1 - y0 - LABEL_H) // 2 - 1, Kit.HUE_TEXT, "right")
            x0, y0, x1, y1 = rows[0]; room = max(20, x1 - x0 - 16 - (TEXT_PX(vals[0]) + 10 if vals[0] else 0))
            fitted = fr["shown"].get("fit")
            if fitted is None or fitted[0] != name or fitted[1] != room:
                fitted = fr["shown"]["fit"] = (name, room, Kit.fit(name, room))
            place(fr, "name", fitted[2], x0 + 8, y0 + (y1 - y0 - LABEL_H) // 2 - 1, hue); cx, cy = fr["centre"]
            hole = fr["hole"]; ty = cy + int(hole * 0.42)
            place(fr, "status", status, cx, ty + 2, Kit.HUE_BAD if status == "DEAD" else Kit.HUE_TITLE, "center")
            if fr["shown"].get("strip") != status:
                fr["shown"]["strip"] = status
                if status: sw = Kit.text_w(status) + 10; Kit.ui_rect(c["strip"], cx - sw // 2, ty, sw, LABEL_H + 4)
                c["strip"].IsVisible = bool(status)
            place(fr, "portrait_text", Kit.fit(portrait_text, 2 * hole - 6) if portrait_text else "",
                  cx, cy - LABEL_H // 2 - 1, Kit.HUE_INFO, "center")
        def wanted_frames():
            keys = []
            if settings["player"]: keys.append("player")
            if settings["target"] and (st["target"] or not settings["hide_empty"]): keys.append("target")
            keys.extend("m%d" % t["serial"] for t in tracked); return keys
        def sync_frames():
            want = wanted_frames()
            for key in list(frames):
                if key not in want: close_frame(key)
            for key in want:
                fr = frames.get(key)
                if (fr is None or not Kit.is_open(fr.get("g")) or fr.get("s") != frame_scale(key)
                        or fr.get("slot") != fitbox.get(key)
                        or (fr.get("slot") and fr.get("rides") != rides_inside(key))) \
                        and (not st["art"] or want_art(frame_scale(key)) is not None):
                    build_frame(key)
                update_frame(key)
        def frame_gump(key):
            def get(): fr = frames.get(key); return fr.get("g") if fr else None
            return get
        def layout_held(key): return Kit.zone_up(KEY + "." + key)
        def frame_at(fr): r = Kit.rect(fr.get("g")); return None if r is None else (r[0], r[1])
        def watch_frames(now):
            for key, fr in frames.items():
                if not Kit.is_open(fr.get("g")): continue
                p = frame_at(fr)
                if p is None: continue
                if p != fr.get("seen"):
                    fr["seen"] = p
                    if fr.get("code_move"): fr["code_move"] = False
                    else:
                        fr["drag_until"] = now + DRAG_SETTLE
                        if not layout_held(key): fr["moved"] = fr["dropped"] = True
                    note_pos(key, p, now + DRAG_SETTLE)
                else:
                    fr["code_move"] = False
                    if fr.get("dropped") and now >= fr.get("drag_until", 0.0) and SNAP.pressed() is not True:
                        fr["dropped"] = False; snap_to_frames(key)
            if st["pos_dirty"] and now >= st["pos_save_at"]: save_positions()
        def frame_rect(key):
            fr = frames.get(key)
            if fr is None or not Kit.is_open(fr.get("g")): return None
            p = fr.get("seen") or frame_at(fr)
            if p is None: return None
            w, h = fr.get("win") or frame_size(key)[1:]; return p[0], p[1], w, h
        def snap_to_frames(key):
            r = frame_rect(key)
            if r is None: return
            x, y, w, h = r; corner = None; ex = ey = None
            for other in frames:
                if other == key: continue
                ro = frame_rect(other)
                if ro is None: continue
                ox, oy, ow, oh = ro
                for tx, ty in ((ox + ow, oy), (ox + ow, oy + oh - h), (ox - w, oy),
                               (ox - w, oy + oh - h), (ox, oy + oh), (ox + ow - w, oy + oh),
                               (ox, oy - h), (ox + ow - w, oy - h)):
                    d = max(abs(x - tx), abs(y - ty))
                    if d <= FRAME_SNAP and (corner is None or d < corner[0]): corner = (d, tx, ty)
                if y < oy + oh + FRAME_SNAP and oy < y + h + FRAME_SNAP:
                    for tx in (ox + ow, ox - w, ox, ox + ow - w):
                        d = abs(x - tx)
                        if d <= FRAME_SNAP and (ex is None or d < ex[0]): ex = (d, tx)
                if x < ox + ow + FRAME_SNAP and ox < x + w + FRAME_SNAP:
                    for ty in (oy + oh, oy - h, oy, oy + oh - h):
                        d = abs(y - ty)
                        if d <= FRAME_SNAP and (ey is None or d < ey[0]): ey = (d, ty)
            if corner is not None: nx, ny = corner[1], corner[2]
            else: nx = ex[1] if ex else x; ny = ey[1] if ey else y
            if (nx, ny) != (x, y): move_frame(key, nx, ny); frames[key]["moved"] = True
        def move_frame(key, x, y):
            fr = frames.get(key)
            if fr is None or not Kit.is_open(fr.get("g")): return
            w, h = fr.get("win") or frame_size(key)[1:]; g = fr["g"]; x, y = Kit.clamp(x, y, w, h)
            g.SetRect(int(x), int(y), w, h); Kit.note_rect(g, int(x), int(y), w, h); Kit.moved_by_code(g)
            fr.update({"seen": (int(x), int(y)), "code_move": True, "moved": False}); st["pos"][key] = fr["seen"]
            st.update({"pos_dirty": True, "pos_save_at": time.time() + DRAG_SETTLE})
        def mirror_frames(force=False):
            p, t = frames.get("player"), frames.get("target")
            if (p is None or t is None or not Kit.is_open(p.get("g")) or not Kit.is_open(t.get("g"))): return
            sw, sh = Kit.screen(); _s, w, _h = frame_size("player"); pp, tp = p.get("seen"), t.get("seen")
            if layout_held("player") or layout_held("target") or sw <= 0 or sh <= 0 or pp is None or tp is None: return
            p_moved = bool(p.get("moved")); t_moved = bool(t.get("moved"))
            if t_moved and not p_moved and not force:
                want = (sw - tp[0] - w, tp[1])
                if want != pp: move_frame("player", *want)
            elif p_moved or force:
                want = (sw - pp[0] - w, pp[1])
                if want != tp: move_frame("target", *want)
        def target_from_frame(key):
            serial = frame_serial(key)
            if not serial: return
            if API.HasTarget(): API.Target(serial)
            else:
                API.SetLastTarget(serial=serial)
                if key != "target" and serial != st["me"]: st["target"] = serial
        def add_tracked(serial, auto=False):
            if not serial: say("target someone first, then click Add frame.", Kit.HUE_BAD); return
            st["dismissed"].discard(serial)
            if serial == st["me"]: say("that's you; your own frame is the player frame."); return
            for t in tracked:
                if t["serial"] == serial:
                    t["auto"] = False; say("%s already has a frame." % t["name"]); save_tracked(); return
            if len(tracked) >= MAX_TRACKED: say("%d frames is the limit." % MAX_TRACKED, Kit.HUE_BAD); return
            d = read_mobile(serial)
            if d is None: say("that isn't a mobile you can see.", Kit.HUE_BAD); return
            tracked.append({"serial": serial, "auto": auto, "name": d[M_NAME] or "Unknown"}); save_tracked()
            say("added %s." % (d[M_NAME] or "a frame"), Kit.HUE_GOOD); build_window(); HOST.refresh_settings(KEY)
        def remove_tracked(serial):
            for t in tracked:
                if t["serial"] == serial and t["auto"]: st["dismissed"].add(serial)
            tracked[:] = [t for t in tracked if t["serial"] != serial]; close_frame("m%d" % serial); save_tracked()
            build_window(); HOST.refresh_settings(KEY)
        def is_tracked(serial): return any(t["serial"] == serial for t in tracked)
        def pick_answer(kind):
            def done(serial): st["queue"].append((kind, int(serial or 0)))
            return done
        queue = Kit.queuer(st)
        ADD_TIP = ("Frame your target, or pick someone with a target cursor. Alt+click a frame: auto-follow "
                   "(again to stop)")
        REMOVE_TIP = "Click a person or their frame with a target cursor to remove it (each frame has an X too)"
        BTN_H = 40
        def build_window():
            if st["shutting"]: return
            M = Kit.MARGIN; n = len(tracked); g, store, c = wnd.begin(W, M + 30 + Kit.GAP + BTN_H + M)
            if st["minimized"]: Kit.set_text(c["status"], "%s: %s" % (TITLE, Kit.count(n, "frame")))
            else:
                wnd.frame(g); ya = M + 30 + Kit.GAP; Kit.add_section(g, M, ya, W - 2 * M, BTN_H)
                Kit.art_button(g, store, "add", Kit.ART_CIRCLE, M + 12, ya + 12, "Add frame", ADD_TIP,
                               on_click=queue("add_frame"))
                Kit.art_button(g, store, "remove", Kit.ART_CIRCLE, M + 56 + Kit.text_w("Add frame"), ya + 12,
                               "Remove frame", REMOVE_TIP, on_click=queue("remove_frame"))
            wnd.end(g)
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, mini=(MINI_W, MINI_H), icon=0x1B74,
                         cleanup=cleanup, lock=False)
        CHECKS_LEFT = (("player", "Show your own frame", "Your HP, mana and stamina"),
                       ("target", "Show the target frame", "Your current target"),
                       ("hide_empty", "Hide the target frame with no target", "Shown only while you have a target"),
                       ("numbers", "Show numbers on the bars", "HP, mana and stamina as numbers (others' HP as a %)"),
                       ("lock", "Lock the frames in place", "Frames can't be dragged"),
                       ("cast", "Show a cast bar under your frame",
                        "Your spell filling through its cast delay: green when cast, red when it fails"))
        CHECKS_RIGHT = (("hide_bar", "Hide TazUO's own target health bar",
                         "Avoids two target bars; untick to get your client's setting back"),
                        ("click", "Click a frame to target it",
                         "Aims a target cursor if one is up, else sets your last target"),
                        ("party", "Add a frame for each party member", "While they are in your party"),
                        ("ignore_self", "Ignore yourself as last target",
                         "Targeting yourself (a bandage, a heal) keeps your target frame"),
                        ("attack", "Prefer the attack target", "Frame who you attack, else your last target"),
                        ("mirror", "Mirror the player and target frames",
                         "Drag either frame and the other mirrors it across the screen"),
                        ("guard", "Show a GUARDED tag on your frame",
                         "GUARDED in guard zones, ? until known (enter or leave one), blank outside"))
        PREVIEW_TEX = TEX_PREFIX + "snap_preview"
        SCALE_TIP = "Frame size, percent of the art (%d-%d%%)" % (SCALE_MIN, SCALE_MAX)
        PSCALE_TIP = "Party members' frame size while ticked (%d-%d%%)" % (SCALE_MIN, SCALE_MAX)
        PORTRAIT_SLIDERS = (("pdx", "Left / right", "Move pictures left or right in the circle", "%+d"),
                            ("pdy", "Up / down", "Move pictures up or down in the circle", "%+d"),
                            ("pzoom", "Zoom", "Zoom pictures in or out (100%% = %d art pixels tall)" % SNAP_DEPTH,
                             "%d%%"))
        def page_table(w):
            lw = max(Kit.text_w("All frames:"), 24 + Kit.text_w("Party members:"))
            def pscale(f, x, y):
                sx = x + 26 + lw
                f.c["pscale"] = Kit.with_tip(Kit.add_slider(f.g, sx, y + 4, 260, SCALE_MIN, SCALE_MAX,
                                                            settings["pscale"]), PSCALE_TIP)
                f.c["pscale_lbl"] = Kit.add_label(f.g, "%d%%" % settings["pscale"], sx + 272, y + 2, Kit.HUE_INFO)
            pic = {"top": 32, "sh": 30 + PREVIEW + 4 + 10, "dx": 12 + PREVIEW + 4 + 16, "ldy": 0, "fh": 26, "sw": 180,
                   "ugap": 12, "lgap": 12, "lw": max(Kit.text_w(r[1]) for r in PORTRAIT_SLIDERS), "bdy": 0, "bgap": 18}
            return (("OTHERS' FRAMES  (%d of %d)" % (len(tracked), MAX_TRACKED), (("custom", 0, build_others),),
                     {"top": 0, "sh": 30 + 28 + 4 + max(1, len(tracked)) * 24 + 6}),
                    ("OPTIONS", [("check",) + r for r in CHECKS_LEFT] + [("gap", -26 * len(CHECKS_LEFT))] +
                     [("check",) + r + ({"dx": 12 + w // 2},) for r in CHECKS_RIGHT], {"pad": 6}),
                    ("FRAME SIZE", (("slider", "scale", "All frames:", SCALE_TIP, SCALE_MIN, SCALE_MAX,
                                     {"lw": lw, "lgap": 14, "ldy": 2, "sdy": 4, "sw": 260, "ugap": 12, "vfmt": "%d%%"}),
                                    ("check", "pscale_on", "Party members:", "Party members' frames use the slider "
                                     "beside this; unticked, the size above", {"stay": True}),
                                    ("custom", 0, pscale)), {"top": 34, "sh": 96}),
                    ("PICTURE  (in each frame's circle)", [("custom", 0, build_preview)] +
                     [("slider", k, text + ":", tip, NUMBERS[k][0], NUMBERS[k][1], {"vfmt": fmt})
                      for k, text, tip, fmt in PORTRAIT_SLIDERS] +
                     [("buttons", (("retake", Kit.ART_PLAY, "Retake pictures", "Take every picture again (after a gear "
                                    "change)"),
                                   ("reset", Kit.ART_CLOSE, "Reset", "Put the picture sliders back to defaults")))],
                     pic))
        def build_others(f, x, y):
            g, w, store = f.g, f.w, f.store; bx = x + 12
            Kit.art_button(g, store, "add", Kit.ART_PLAY, bx, y + 28, "Add target", "Frame your current target",
                           on_click=queue("add_target"))
            Kit.art_button(g, store, "pick", Kit.ART_PLAY, bx + 49 + Kit.text_w("Add target"), y + 28, "Pick...",
                           "Pick someone to frame", on_click=queue("pick"))
            Kit.art_button(g, store, "clear", Kit.ART_CLOSE, x + w - 47 - Kit.text_w("Clear all"), y + 28, "Clear all",
                           "Remove everyone else's frame", on_click=queue("clear"))
            yl = y + 30 + 28 + 4; rm_w = Kit.pic_size(Kit.ART_CLOSE[0])[0] or 30
            if not tracked:
                Kit.add_label(g, "No frames yet. Target someone, then click Add target.", x + 12, yl + 3, Kit.HUE_INFO)
            for i, t in enumerate(tracked):
                ry = yl + i * 24; tag = "(party)" if t["auto"] else ""
                room = w - 24 - rm_w - 6 - (Kit.text_w(tag) + 8 if tag else 0); shown = Kit.fit(t["name"], room)
                Kit.add_label(g, shown, x + 12, ry + 3)
                Kit.catcher(g, x + 12, ry, room + 8, 20, follow_or(t["serial"]),
                            "Alt+click: auto-follow (again to stop)")
                if tag: Kit.add_label(g, tag, x + 12 + Kit.text_w(shown) + 8, ry + 3, Kit.HUE_INFO)
                Kit.art_button(g, store, "rm%d" % i, Kit.ART_CLOSE, x + w - 12 - rm_w, ry,
                               None, "Remove %s's frame. Alt+click: auto-follow (again to stop)" % t["name"],
                               on_click=follow_or(t["serial"], ("rm", t["serial"])))
        def build_preview(f, x, y):
            g = f.g; Kit.add_section(g, x + 12, y - 2, PREVIEW + 4, PREVIEW + 4, alpha=1.0)
            if st["art"] and st.get("running"): draw_preview(); Tex.control(g, PREVIEW_TEX, x + 14, y, PREVIEW, PREVIEW)
            else:
                lines = ("Pictures", "unavailable") if st.get("running") else ("Turn Frames", "on for a", "preview")
                top = y + (PREVIEW - len(lines) * 18) // 2
                for i, line in enumerate(lines):
                    Kit.add_label(g, line, x + 14 + (PREVIEW - Kit.text_w(line)) // 2, top + i * 18, Kit.HUE_INFO)
        def crop_now():
            now = time.time(); st["crop_changed"] = now
            if st["art"] and st.get("running") and now >= page["next_preview"]:
                page["next_preview"] = now + 0.3; draw_preview()
        def page_clicks(f):
            if Kit.was_clicked(f.store, "retake"): page["layers"] = None; st["crop_changed"] = 1.0
            if Kit.was_clicked(f.store, "reset"):
                for k, _t, _tip, _fmt in PORTRAIT_SLIDERS: f.c[k].SetValue(DEFAULTS[k])
                crop_now()
        def read_pscale(f, new):
            try: new["pscale"] = max(SCALE_MIN, min(SCALE_MAX, int(f.c["pscale"].Value)))
            except Exception: return
            Kit.set_text(f.c["pscale_lbl"], "%d%%" % new["pscale"])
        def on_change(old, new):
            if (new["lock"], new["click"]) != (old["lock"], old["click"]): st["rebuild"] = True
            if new["party"] != old["party"]: st["next_party"] = 0.0
            if new["mirror"] and not old["mirror"]: st["mirror_now"] = True
            st["art_dirty"] = True
            for k, _t, _tip, _fmt in PORTRAIT_SLIDERS:
                if new[k] != old[k]: crop_now(); break
        cfg = Kit.Page(settings, page_table, save_settings, on_change, adjust=read_pscale, clicks=page_clicks)
        def build_config(g, x, y, w): page["store"] = cfg.build(g, x, y, w).store
        def config_closed(): cfg.closed(); page.update({"layers": None, "preview_gen": None})
        def draw_preview():
            if st.get("running") and st["art"]: page["preview_want"] = True
        def read_own_layers():
            doll = read_paperdoll(st["me"] or my_serial())
            if not doll or not doll["body"]: return None
            layers = safe(lambda: fetch_layers(doll), []); return (layers, doll["body"]) if layers else None
        def draw_preview_now():
            got = page.get("layers")
            if got is None:
                got = safe(lambda: Kit.on_client(read_own_layers))
                if not got: return
                page["layers"] = got
            page["preview_gen"] = compose_steps(got[0], got[1], PREVIEW)
        def preview_work(budget):
            deadline = time.time() + budget
            while page.get("preview_gen") is not None:
                gen = page["preview_gen"]
                try: r = next(gen)
                except Exception:
                    if page.get("preview_gen") is gen: page["preview_gen"] = None
                    return
                if r is not None:
                    if page.get("preview_gen") is gen: page["preview_gen"] = None
                    safe(lambda: Bridge.on_main(lambda: Bridge.put_texture(PREVIEW_TEX, PREVIEW, PREVIEW, r))); return
                if time.time() >= deadline: return
        def apply_crop(now):
            t = st["crop_changed"]
            if not t or now - t < 0.5: return
            st["crop_changed"] = 0.0
            if st["art"]:
                if cfg.f is not None: draw_preview()
                retake_all()
        def _start():
            st_reset(); st.update({"me": my_serial(), "running": True})
            cast.update({"spell": None, "state": None, "shown": None})
            page.update({"preview_want": False, "preview_gen": None}); load_settings(); load_tracked(); load_positions()
            cleanup.service("frames.player_anchor", player_anchor); st["minimized"] = wnd.start_min()
            st["art"] = Bridge.find()
            if not st["art"]: say("no drawn pictures on this client; using stone frames.")
            build_window(); wnd.dock(scale=True)
            cleanup.service("unitframes.add", lambda serial: queue(("add_ext", int(serial)))())
            fitst["player"] = fitst["target"] = None; fitbox["player"] = fitbox["target"] = None
            for fk in ("player", "target"):
                HOST.layout_add(KEY + "." + fk, frame_gump(fk), TITLE + " (" + fk + ")",
                                {"fit": frame_fit(fk), "fill": "frame", "exact": True, "pieces_out": True,
                                 "hug": frame_hug(fk), "untitled": True})
                pieces_anchor(fk, frame_gump(fk), frame_span(fk), frame_inner(fk))
                cleanup.add(HOST.layout_remove, KEY + "." + fk); cleanup.add(pieces_anchor, fk, None)
            PIECES_TARGET["fn"] = lambda: st["target"]
        BY_SERIAL = {"rm": remove_tracked, "click": target_from_frame, "add_ext": add_tracked,
                     "follow_serial": lambda serial: Follow.toggle(serial, TITLE)}
        def last_target(): return st["target"] or int(API.LastTargetSerial or 0)
        def _tick():
            if win["g"] is None: return
            if Kit.closed(win): return
            now = time.time()
            if now < st["full_at"] and not st["queue"] and not st["rebuild"] and now + 1.0 > st["full_at"]:
                if st["art"]: take_next_snapshot(now)
                return
            st["full_at"] = now + TICK_EVERY - 0.005; st["me"] = st["me"] or my_serial(); update_target()
            while st["queue"]:
                action = st["queue"].pop(0); kind = action[0] if isinstance(action, tuple) else action
                if wnd.action(action): continue
                if kind == "add_frame":
                    serial = last_target()
                    if serial and serial != st["me"] and not is_tracked(serial): add_tracked(serial); continue
                    kind = "busy" if HOST.cursor_busy(KEY) else "pick"
                elif kind == "remove_frame":
                    if not tracked: say("nobody else has a frame (turn off your own and the target frame in settings).")
                    elif HOST.cursor_busy(KEY): kind = "busy"
                    else:
                        say("click the person, or their frame, to remove."); st["removing"] = True
                        HOST.pick_target(PICK_TIMEOUT, pick_answer("unpicked"))
                if kind == "busy": say("a target cursor is up; try again after it.")
                elif kind == "pick":
                    say("choose who gets a frame."); HOST.pick_target(PICK_TIMEOUT, pick_answer("picked"))
                elif kind == "add_target": add_tracked(last_target())
                elif kind == "picked":
                    if action[1]: add_tracked(action[1])
                    else: say("pick cancelled.")
                elif kind == "remove_click":
                    serial = frame_serial(action[1])
                    if serial and st.get("removing") and API.HasTarget(): API.Target(serial)
                elif kind == "unpicked":
                    st["removing"] = False
                    if not action[1]: say("remove cancelled.")
                    elif is_tracked(action[1]):
                        name = next((t["name"] for t in tracked if t["serial"] == action[1]), "")
                        remove_tracked(action[1]); say("removed %s." % (name or "the frame"))
                    else: say("they have no frame of their own.")
                elif kind == "clear":
                    for t in tracked: close_frame("m%d" % t["serial"])
                    del tracked[:]; save_tracked(); HOST.refresh_settings(KEY)
                    if settings["party"]: say("cleared; party members come back while 'Add a frame for each party "
                                              "member' is ticked.")
                    build_window()
                elif kind == "follow":
                    serial = frame_serial(action[1])
                    if serial: Follow.toggle(serial, TITLE)
                elif kind in ("closed", "xclose"):
                    key = action[1]
                    if kind == "xclose": close_frame(key)
                    frames.pop(key, None)
                    if key in ("player", "target"):
                        settings[key] = False; save_settings(); HOST.refresh_settings(KEY)
                        say("%s frame hidden; tick it again in settings." % key)
                    elif key[1:].isdigit(): remove_tracked(int(key[1:]))
                elif kind in BY_SERIAL: BY_SERIAL[kind](action[1])
            if st["rebuild"]:
                st["rebuild"] = False; remember_positions()
                for key in list(frames): close_frame(key)
            if st["art"]:
                px = snap_px()
                if st["snap_px"] != px:
                    st["snap_px"] = px
                    if st["snaps"]: retake_all()
            now = time.time()
            if now >= st["next_party"]: st["next_party"] = now + 1.0; sync_party()
            sync_frames()
            if st["art"] and st["art_dirty"]: st["art_dirty"] = False; prune_art()
            if now >= st["next_prune"]: st["next_prune"] = now + 5.0; prune_people()
            for fr in frames.values(): fr["moved"] = False
            watch_frames(now); rides = (rides_inside("player"), rides_inside("target"))
            if rides != st.get("rides"): st["rides"] = rides; HOST.layout_refit()
            pieces_place()
            if settings["mirror"]: mirror_frames(force=st.pop("mirror_now", False))
            cast_tick(now); hbar_tick(now); guard_tick(now)
            if st["art"]: take_next_snapshot(now)
            apply_crop(now)
            if now >= st["next_save"]:
                st["next_save"] = now + 10.0; remember_positions()
                if st["pos_dirty"]: save_positions()
        def _stop():
            st.update({"shutting": True, "running": False, "removing": False, "snap_job": None, "art_jobs": []})
            page.update({"preview_want": False, "preview_gen": None}); PIECES_TARGET["fn"] = None; save_positions()
            save_settings(); save_tracked(); safe(lambda: hbar_sync(False))
            for key in list(frames): fr = frames.pop(key); g, fr["g"] = fr.get("g"), None; Kit.dispose(g)
            drop_cast(); st["jr"] = None
            if st["art"] and st["textures"]:
                names = list(st["textures"]); safe(lambda: Bridge.on_main(lambda: Tex.drop(names)))
                st["textures"].clear(); st["art_scales"] = set()
            st["art"] = None; cleanup.close()
        def _thread_tick():
            if st["shutting"]: return
            if st["art_jobs"]: art_work(THREAD_BUDGET)
            if st["snap_job"] is not None: snapshot_work(time.time(), THREAD_BUDGET)
            if page.get("preview_want"):
                page["preview_want"] = False
                if cfg.f is not None: draw_preview_now()
            if page.get("preview_gen") is not None: preview_work(THREAD_BUDGET)
        def _thread_busy():
            return bool(st["snap_job"] or st["art_jobs"] or page.get("preview_want") or
                        page.get("preview_gen") is not None)
        def _interval(): return 0.03 if _thread_busy() else TICK_EVERY
        load_settings()
        return part_dict(_start, _tick, _stop, cfg.height, build_config, cfg.poll, config_closed,
                         thread_tick=_thread_tick, interval=_interval, thread_wanted=_thread_busy)
    def _part_timers():
        KEY = "spelltimers"; TITLE = "Buffs & Timers"; SETTINGS_KEY = "SpellTimers_settings"
        POS_KEY = "SpellTimers_pos"; MIN_KEY = "SpellTimers_min"; ACTIVE_KEY = "SpellTimers_active"; TRAY_ICON = 0x0EFA
        MINI_W, MINI_H = 320, 46; ROW_H = 28; ROWS_MIN, ROWS_MAX, ROWS_DEFAULT = 3, 16, 8; SAMPLE_EVERY = 0.1
        OTHERS_EVERY = 0.25; ICON_RESYNC = 5.0; SPELL_ICON_BASE = 0x08C0; ICON_PX = 22; LAND_WINDOW = 2.5
        STAT_MIN_STEP = 2; STAT_GROUP = 1.0; STAT_EFFECTS_MAX = 4; TRACK_MAX = 40; ALERT_KIND = "spelltimers.ending"
        WARN_MAX = 120
        SPELLS = dict.fromkeys(("Clumsy", "Feeblemind", "Weaken", "Curse"),
                               ("target", "debuff", (0, 1.2, 0, 0, 0), 0, "stat"))
        SPELLS.update(dict.fromkeys(("Agility", "Cunning", "Strength", "Bless"),
                                    ("target", "buff", (0, 1.2, 0, 0, 0), 0, "stat")))
        SPELLS.update({"Night Sight":      ("target", "buff", (900, 0, 0, 0, 0), 2340, None),
            "Invisibility":     ("target", "buff", (0, 1.2, 0, 0, 0), 0, "hidden"),
            "Paralyze":         ("target", "debuff", (7, 0.2, 0, 0, 0), 0, "paralyzed"),
            "Poison":           ("target", "debuff", None, 0, "poisoned"),
            "Protection":       ("self", "buff", (0, 2.0, 0, 15, 240), 0, None),
            "Reactive Armor":   ("self", "buff", None, 0, None), "Magic Reflection": ("self", "buff", None, 0, None),
            "Incognito":        ("self", "buff", (1, 1.2, 0, 0, 144), 0, "name"), 
            "Polymorph":        ("self", "buff", (0, 2.0, 0, 0, 240), 0, "body"),})
        STAT_SPELLS = {("str", 1): "Strength", ("str", -1): "Weaken", ("dex", 1): "Agility",
                       ("dex", -1): "Clumsy", ("int", 1): "Cunning", ("int", -1): "Feeblemind"}
        FAIL_TEXTS = ("the spell fizzles", "your concentration is disturbed", "insufficient mana",
                      "more reagents are needed", "target cannot be seen", "that is too far away",
                      "target is too far away", "this spell won't work on that", "this spell is already in effect",
                      "the spell will not adhere to you", "you currently have a re", 
                      "this target already has reactive armor", "incognito cannot be cast",
                      "you cannot disguise yourself", "you cannot polymorph", "you cannot incognito",
                      "you cannot cast that spell in this form")
        END_TEXTS = (("your reactive armor spell has been nullified", "Reactive Armor"),
                     ("your protection spell has been nullified", "Protection"))
        STILL_TEXTS = (("you currently have a reflect spell", "Magic Reflection"),
                       ("you currently have a reactive armor spell", "Reactive Armor"))
        PARA_OFF = ("you can move!", "you can move again!", "you are no longer frozen")
        POISON_ME = (("you feel a bit nauseous", 1), ("you feel disoriented and nauseous", 2),
                     ("you begin to feel pain throughout your body", 3),
                     ("you feel extremely weak and are in severe pain", 4),
                     ("you are in extreme pain, and require immediate aid", 5))
        POISON_THEM = (("looks extremely ill", 2), ("looks ill", 1), ("stumbles around in confusion and pain", 3),
                       ("is wracked with extreme pain", 4), ("begins to spasm uncontrollably", 5))
        POISON_OFF = ("the poison seems to have worn off", "you feel cured of poison",
                      "you have been cured of all poisons")
        POISON_NAMES = ("", "Lesser", "Regular", "Greater", "Deadly", "Lethal")
        ICON_DEBUFFS = frozenset(("paralyze", "paralyzed", "poison", "curse", "clumsy",
                                  "feeblemind", "weaken", "mindrot", "strangle", "corpseskin",
                                  "evilomen", "bloodoath", "masscurse", "mortalstrike"))
        COL = {"buff": (47, 154, 60), "debuff": (194, 45, 45), "other": (207, 174, 42), "dim": (90, 90, 90)}
        OWN_PREFIX = TITLE.lower() + ":"
        def norm(name): return str(name or "").lower().replace(" ", "").replace("-", "")
        ICONS = {norm(_sp[0]): SPELL_ICON_BASE + _i for _i, _sp in enumerate(Kit.MAGERY)}
        ICONS["paralyzed"] = ICONS.get("paralyze", SPELL_ICON_BASE); SPELL_OF = {norm(_n): _n for _n in SPELLS}
        SPELL_OF["paralyzed"] = "Paralyzed"; SPELL_ORDER = {"buff": 0, "debuff": 1}
        KEEP_SIDS = frozenset(norm(n) for n, v in SPELLS.items() if v[1] == "buff")
        settings = {"me": True, "debuff": True, "others": True, "stats": True, "icons": True,
                    "rows": ROWS_DEFAULT, "warn": 0}
        def st_reset():
            st.update({"shutting": False, "docked": False, "queue": [], "rd": None, "pend": None, "landings": [],
                       "last_land": None, "para": None, "pois": None, "stats": None, "next_sample": 0.0,
                       "next_others": 0.0, "events": [], "icons_seen": False, "next_icons": 0.0, "warned": {},
                       "rebuild": False, "dead": False, "skills": (0.0, 0.0, -1e9)})
        st = {"minimized": False, "me": 0, "name": "", "prev_name": ("", 0.0), "body": 0, "hooked": False,
              "ct": None, "ct_looked": False, "ver": 0, "active": False, "redraw": False}
        st_reset(); rows = {}; effects = {"str": [], "dex": [], "int": []}
        win = {"g": None, "c": {}, "store": ({}, {}), "slots": [], "nrows": 0}
        ROW_ICON = 24; ROW_PITCH = 30; ROW_LINE = 42; ROW_PAD = 3; ROW_MAX = 24; FORM_EVERY = 0.5
        rowui = {s: {"g": None, "cells": [], "per": 1, "lines": -1, "w": 0} for s in ("player", "target")}
        NUMS = {"rows": (ROWS_MIN, ROWS_MAX), "warn": (0, WARN_MAX)}
        def load_settings(): Kit.kv_load(SETTINGS_KEY, ";", settings, NUMS)
        def save_settings():
            Kit.kv_save(SETTINGS_KEY, ";", settings, ("me", "debuff", "others", "stats", "icons", "rows", "warn"), NUMS)
        def save_active():
            now = time.time(); parts = ["t=%d" % int(now)]
            for stat in ("str", "dex", "int"):
                for e in effects[stat]:
                    parts.append("e:%s,%d,%d,%d,%d" % (stat, e["d"], int(e["t"]), int(e["end"] or 0),
                                                       1 if e.get("hide") else 0))
            for r in rows.values():
                if r["who"] or "cast" not in r["srcs"] or "stat" in r["srcs"] or r["sid"] not in KEEP_SIDS: continue
                parts.append("r:%s,%s,%d,%d,%d" % (r["sid"], r["kind"], int(r["start"]),
                                                   int(r["end"] or 0), int(r["most"] or 0)))
            Kit.put_var(ACTIVE_KEY, ";".join(parts))
        def restore_active(now):
            parts = Kit.get_var(ACTIVE_KEY).split(";")
            try: saved = float(parts[0].split("=", 1)[1]) if parts[0].startswith("t=") else 0.0
            except (ValueError, IndexError): saved = 0.0
            if not saved or not 0 <= now - saved <= 1800.0: return
            for p in parts[1:]:
                try:
                    tag, rest = p.split(":", 1); b = rest.split(",")
                    if tag == "e" and b[0] in effects and settings["stats"]:
                        if len(effects[b[0]]) >= STAT_EFFECTS_MAX: continue
                        d, t0, end = int(b[1]), float(b[2]), float(b[3])
                        if (end and end > now) or not end:
                            effects[b[0]].append({"d": d, "t": t0, "end": end or None,
                                                  "hide": len(b) > 4 and b[4] == "1"})
                    elif tag == "r" and b[0] in SPELL_OF:
                        start, end, most = float(b[2]), float(b[3]), float(b[4])
                        if end and max(end, most) <= now: continue
                        r = new_row(0, b[0], b[1] if b[1] in SPELL_ORDER else "buff", start)
                        r["end"], r["most"] = end or None, most or None; r["srcs"].add("cast")
                except Exception: continue
        def new_row(who, sid, kind, now, name=""):
            key = (who, sid); r = rows.get(key)
            if r is None:
                r = {"key": key, "who": who, "sid": sid, "kind": kind, "start": now, "end": None,
                     "most": None, "srcs": set(), "watch": None, "seen": False, "confirm": 0.0,
                     "base": None, "level": 0, "delta": 0, "name": name, "away": 0.0,
                     "icon": ICONS.get(sid, SPELL_ICON_BASE), "end_src": None}
                rows[key] = r
                if len(rows) > TRACK_MAX: trim_rows(key)
            else:
                r["kind"] = kind
                if name: r["name"] = name
            st["ver"] += 1; return r
        def drop_row(key):
            if rows.pop(key, None) is not None: st["ver"] += 1; st["warned"].pop(key, None)
        def drop_src(key, src):
            r = rows.get(key)
            if r is None: return
            r["srcs"].discard(src)
            if not r["srcs"]: drop_row(key)
            else: st["ver"] += 1
        def trim_rows(keep):
            order = sorted(rows.values(), key=lambda r: (r["who"] == 0, r["start"]))
            for r in order:
                if len(rows) <= TRACK_MAX: break
                if r["key"] != keep: rows.pop(r["key"], None)
        def text_key(r):
            return (r["sid"], r.get("label"), r["delta"], r["level"], r["who"], r["name"],
                    r["end"] is None, "stat" in r["srcs"])
        def display_name(r):
            sid = r["sid"]; name = SPELL_OF.get(sid) or r.get("label") or sid
            if r["delta"]: name = "%s %+d" % (name, r["delta"])
            if r["level"] and sid == "poison": name = "%s (%s)" % (name, POISON_NAMES[max(1, min(5, r["level"]))])
            if r["who"]: name = "%s: %s" % (name, r["name"] or "someone")
            return name
        def skills(now, force=False):
            s = st["skills"]
            if force or not 0 <= now - s[2] < 15.0:
                s = st["skills"] = (skill_value("Magery", s[0]), skill_value("Evaluating Intelligence", s[1]), now)
            return s
        def duration(spell, now):
            spec = SPELLS.get(spell)
            if spec is None or spec[2] is None: return None
            base, per_m, per_e, lo, hi = spec[2]; mag, ev, _ = skills(now); secs = base + per_m * mag + per_e * ev
            if lo: secs = max(lo, secs)
            if hi: secs = min(hi, secs)
            return max(1.0, secs)
        def on_words(spell, at, now):
            old = st["pend"]
            if old is not None:
                due = old["at"] + old["delay"]; st["pend"] = None
                if old["side"] == "self" and at >= due - 0.05: land(old, st["me"], due, now)
                elif old["side"] == "target" and not old["cursor"] and at >= due + 0.2:
                    tgt = int(API.LastTargetSerial or 0)
                    if tgt: land(old, tgt, due, now)
            spec = SPELLS.get(spell)
            if spec is None: st["pend"] = None; return
            info = Kit.spell_info(spell); delay = info[3] if info and info[3] else 1.0; skills(now, True)
            st["pend"] = {"spell": spell, "sid": norm(spell), "at": at, "delay": float(delay),
                          "side": spec[0], "cursor": False, "body0": st["body"], "name0": st["name"]}
        def resolve_pending(now):
            p = st["pend"]
            if p is None: return
            due = p["at"] + p["delay"]
            if now < due - 0.05: return
            if p["side"] == "self":
                if now >= due + 0.6: st["pend"] = None; land(p, st["me"], due, now)
                return
            if API.HasTarget():
                if not p["cursor"]: p["cursor"] = True; p["lt0"] = int(API.LastTargetSerial or 0)
                p["mana0"] = int(API.Player.Mana); p["gone"] = None
                if now > due + 30.0: st["pend"] = None
                return
            if not p["cursor"] and now < due + 1.2: return
            tgt = int(API.LastTargetSerial or 0)
            if p["cursor"]:
                if p.get("gone") is None: p["gone"] = now
                if int(API.Player.Mana) >= p["mana0"] and tgt == p.get("lt0", 0):
                    if 0 <= now - p["gone"] < 1.5: return
                    st["pend"] = None; return
            st["pend"] = None
            if tgt: land(p, tgt, now, now)
        def land(p, who, at, now):
            spell, sid = p["spell"], p["sid"]; spec = SPELLS[spell]; me = st["me"]; on_me = not who or who == me
            dur = duration(spell, now)
            if on_me and spec[4] == "stat" and settings["stats"]:
                st["landings"].append({"sid": sid, "t": at, "dur": dur or 0.0}); del st["landings"][:-6]
                attach_landing(now); return
            m = None if on_me else API.FindMobile(who); name = str(m.Name or "") if m is not None else ""
            r = new_row(0 if on_me else who, sid, spec[1], at, name); r["start"] = at; r["srcs"].add("cast")
            if r["end_src"] != "icon":
                r["end"] = (at + dur) if dur else None; r["most"] = (at + spec[3]) if spec[3] else None
                r["end_src"] = "cast"
            r["delta"], r["away"] = 0, 0.0; watch = spec[4]
            if watch == "stat" or (watch in ("body", "name", "hidden") and not on_me): watch = None
            r["watch"], r["seen"] = watch, False; r["confirm"] = now + 2.0
            if watch == "body": r["base"] = p["body0"]
            elif watch == "name": r["base"] = p["name0"]
            st["last_land"] = (r["key"], now); st["warned"].pop(r["key"], None)
        def cast_failed(now, during=False):
            p = st["pend"]
            if p is not None and (during or now >= p["at"] + p["delay"] - 0.3): st["pend"] = None; return
            ll = st["last_land"]
            if ll is not None and 0 <= now - ll[1] <= 1.0:
                st["last_land"] = None; r = rows.get(ll[0])
                if r is not None and r["srcs"] == set(("cast",)): drop_row(ll[0])
        def attach_landing(now):
            lands = [l for l in st["landings"] if 0 <= now - l["t"] <= LAND_WINDOW + 1.0]; st["landings"] = lands
            if not lands: return False
            hit = False
            for stat in ("str", "dex", "int"):
                for e in effects[stat]:
                    if (e["end"] is not None or e["d"] <= 0 or not 0 <= now - e["t"] <= LAND_WINDOW + 1.0): continue
                    for l in reversed(lands):
                        if l["sid"] in ("bless", norm(STAT_SPELLS[(stat, 1)])) \
                                and abs(e["t"] - l["t"]) <= LAND_WINDOW and l["dur"]:
                            e["end"], e["cast"] = l["t"] + l["dur"], l["sid"]; hit = True; break
            if hit: sync_stat_rows()
            return hit
        def apply_step(stat, d, now):
            effs = effects[stat]; total = 0
            for e in effs: total += e["d"]
            if effs and total + d == 0: del effs[:]; return
            for i, e in enumerate(effs):
                if e["d"] == -d: del effs[i]; return
            effs.append({"d": d, "t": now, "end": None})
            if len(effs) > STAT_EFFECTS_MAX: del effs[0]
        def stat_steps(vals, now):
            old = st["stats"]; st["stats"] = vals
            if old is None: return
            changed = False
            for i, stat in enumerate(("str", "dex", "int")):
                d = vals[i] - old[i]
                if abs(d) > 30: del effects[stat][:]; changed = True
                elif abs(d) >= STAT_MIN_STEP: apply_step(stat, d, now); changed = True
            if changed:
                p = st["pend"]
                if p is not None and p["side"] == "target" and SPELLS[p["spell"]][4] == "stat" \
                        and now >= p["at"] + p["delay"] - 0.4 and settings["stats"]:
                    st["pend"] = None; land(p, st["me"], now, now)
                attach_landing(now); sync_stat_rows()
        def sync_stat_rows():
            groups = {}; used = set(); S, D, I = effects["str"], effects["dex"], effects["int"]
            for a in S:
                if a.get("hide"): continue
                for b in D:
                    if id(b) in used or b.get("hide") or b["d"] != a["d"] or abs(b["t"] - a["t"]) > STAT_GROUP: continue
                    for c in I:
                        if id(c) in used or c.get("hide") or c["d"] != a["d"] or abs(c["t"] - a["t"]) > STAT_GROUP:
                            continue
                        used.update((id(a), id(b), id(c))); sid = "bless" if a["d"] > 0 else "curse"
                        end = a["end"] or b["end"] or c["end"]
                        add_group(groups, sid, a["d"], min(a["t"], b["t"], c["t"]), end); break
                    if id(a) in used: break
            for stat in ("str", "dex", "int"):
                for e in effects[stat]:
                    if id(e) in used or e.get("hide"): continue
                    sid = norm(STAT_SPELLS[(stat, 1 if e["d"] > 0 else -1)])
                    add_group(groups, sid, e["d"], e["t"], e["end"])
            for sid, g in groups.items():
                kind = "buff" if g[0] > 0 else "debuff"; r = new_row(0, sid, kind, g[1])
                if "stat" not in r["srcs"]: r["start"] = g[1]
                r["srcs"].add("stat"); r["delta"] = g[0]
                if r["end_src"] != "icon": r["end"], r["end_src"] = g[2], "stat"; r["most"] = None
            for key in [k for k, r in rows.items() if not r["who"] and "stat" in r["srcs"] and r["sid"] not in groups]:
                r = rows[key]; r["delta"] = 0; drop_src(key, "stat")
            st["ver"] += 1
        def add_group(groups, sid, d, t, end):
            g = groups.get(sid)
            if g is None: groups[sid] = [d, t, end]
            else:
                g[0] += d; g[1] = min(g[1], t)
                if end is not None and (g[2] is None or end > g[2]): g[2] = end
        def clear_me():
            for key in [k for k in rows if not k[0]]: drop_row(key)
            for stat in effects: del effects[stat][:]
            st.update({"stats": None, "pend": None, "landings": [], "para": None, "pois": None})
        def sample(now):
            p = HOST.me()
            if p is None: return
            me = int(p.Serial); name = str(p.Name or ""); dead = bool(p.IsDead); para = bool(p.IsParalyzed)
            pois = bool(p.IsPoisoned); hid = bool(p.IsHidden); body = int(p.Graphic or 0)
            vals = (int(p.Strength or 0), int(p.Dexterity or 0), int(p.Intelligence or 0))
            if me != st["me"]:
                if st["me"]: clear_me()
                st["me"] = me
            if name != st["name"]:
                if st["name"]: st["prev_name"] = (st["name"], now)
                st["name"] = name
            if dead:
                if not st["dead"]: st["dead"] = True; clear_me()
                return
            if st["dead"]: st["dead"] = False; st["stats"] = None
            st["body"] = body
            for k, sid, on in (("para", "paralyzed", para), ("pois", "poison", pois)):
                if on != st[k]:
                    st[k] = on
                    if on: new_row(0, sid, "debuff", now)["srcs"].add("flag")
                    else: drop_row((0, sid))
            for r in list(rows.values()):
                if r["who"] or r["watch"] is None: continue
                w = r["watch"]
                if w == "hidden": on = hid
                elif w == "body": on = body != r["base"]
                elif w == "name": on = name != r["base"]
                else: continue
                if on: r["seen"] = True
                elif r["seen"]: drop_row(r["key"])
                elif w == "hidden" and now > r["confirm"]: drop_row(r["key"])
            if settings["stats"]:
                if vals[0] and vals[1] and vals[2]: stat_steps(vals, now)
            elif st["stats"] is not None or effects["str"] or effects["dex"] or effects["int"]:
                st["stats"] = None
                for stat in effects: del effects[stat][:]
                sync_stat_rows()
        def watch_others(now):
            if not rows: return
            found = {}; dead_of = {}
            for r in list(rows.values()):
                who = r["who"]
                if not who: continue
                if who not in found: found[who] = API.FindMobile(who)
                m = found[who]
                if m is None:
                    if not r["away"]: r["away"] = now; st["ver"] += 1
                    if r["watch"] and not r["seen"] and now > r["confirm"]: drop_row(r["key"])
                    continue
                if r["away"]: r["away"] = 0.0; st["ver"] += 1
                try:
                    dead = dead_of.get(who)
                    if dead is None: dead = dead_of[who] = bool(m.IsDead)
                    if dead: drop_row(r["key"]); continue
                    w = r["watch"]
                    if w == "paralyzed": on = bool(m.IsParalyzed)
                    elif w == "poisoned": on = bool(m.IsPoisoned)
                    else: continue
                except Exception: continue
                if on:
                    if not r["seen"]: r["seen"] = True
                elif r["seen"]: drop_row(r["key"])
                elif now > r["confirm"]: drop_row(r["key"])
        def read_journal(now):
            rd = st["rd"]
            if rd is None: st["rd"] = Journal.reader(); return
            lines = rd.new()
            if not lines: return
            me_name = st["name"]; prev, prev_at = st["prev_name"]
            for ln in lines:
                low = ln.low
                if low.startswith(OWN_PREFIX): continue
                name = ln.name or ""
                mine = bool(me_name) and name == me_name or (prev and name == prev and 0 <= now - prev_at <= 5.0)
                if mine:
                    sp = Kit.SPELL_WORDS.get(low.strip())
                    if sp is not None: on_words(sp[0], min(now, ln.at or now), now); continue
                if name and not mine and name != "System": them_poison(low, name); continue
                line_me(low, now, not mine)
        def line_me(low, now, system):
            txt = low.strip(" *")
            for t, lvl in POISON_ME:
                if txt.startswith(t):
                    r = new_row(0, "poison", "debuff", now); r["srcs"].add("line")
                    if lvl != r["level"]: r["level"] = lvl; st["ver"] += 1
                    return
            if not system: return
            for t in FAIL_TEXTS:
                if low.startswith(t):
                    for still, spell in STILL_TEXTS:
                        if low.startswith(still):
                            r = rows.get((0, norm(spell)))
                            if r is None: r = new_row(0, norm(spell), "buff", now)
                            r["srcs"].add("cast")
                    p = st["pend"]
                    if p is not None and p["sid"] in ("reactivearmor", "magicreflection") and \
                            t == "this spell is already in effect" and (0, p["sid"]) not in rows:
                        new_row(0, p["sid"], "buff", now)["srcs"].add("cast")
                    cast_failed(now, t == "your concentration is disturbed"); return
            for t, spell in END_TEXTS:
                if low.startswith(t): drop_row((0, norm(spell))); return
            if low.startswith("you cannot move!"): new_row(0, "paralyzed", "debuff", now)["srcs"].add("line")
            elif low.startswith(PARA_OFF): drop_row((0, "paralyzed"))
            elif txt.startswith(POISON_OFF): drop_row((0, "poison"))
        def them_poison(low, name):
            for r in rows.values():
                if r["who"] and r["sid"] == "poison": break
            else: return
            for t, lvl in POISON_THEM:
                if t in low:
                    nl = name.lower()
                    for r in rows.values():
                        if r["who"] and r["sid"] == "poison" and r["name"] and r["level"] != lvl and \
                                (r["name"].lower() == nl or r["name"].lower() in low):
                            r["level"] = lvl; st["ver"] += 1
                    return
        def on_buff_event(kind, args):
            if not st["active"]: return
            for a in args:
                try: info = (kind, str(a.Title or ""), int(a.Graphic or 0), int(a.Timer or 0))
                except Exception: continue
                if len(st["events"]) < 60: st["events"].append(info); HOST.poked = True
                return
        def hook_events():
            Kit.hook_once(st, "hooked", ("OnBuffAdded", lambda *a: on_buff_event("add", a)),
                          ("OnBuffRemoved", lambda *a: on_buff_event("remove", a)))
        def client_ms():
            if not st["ct_looked"]:
                st["ct_looked"] = True
                try:
                    t = Client._type("ClassicUO.Time"); m = Client._member(t, "Ticks") if t is not None else None
                    st["ct"] = m[0] if m else None
                except Exception: st["ct"] = None
            fn = st["ct"]
            if fn is None: return None
            try: return int(fn())
            except Exception: return None
        def icon_row(title, graphic, timer, now):
            sid = norm(title)
            if not sid: return
            kind = "debuff" if sid in ICON_DEBUFFS else "buff"; r = new_row(0, sid, kind, now)
            if "icon" not in r["srcs"]: r["start"] = now
            r["srcs"].add("icon"); r["label"] = title
            if graphic: r["icon"] = graphic
            end = None
            if 0 < timer < 0xFFFFFFFF:
                ct = client_ms()
                if ct is not None and timer > ct: end = now + (timer - ct) / 1000.0
            if end is not None: r["end"], r["end_src"], r["most"] = end, "icon", None
        def handle_icons(now):
            evs, st["events"] = st["events"], []
            if not settings["icons"]: return
            for kind, title, graphic, timer in evs:
                st["icons_seen"] = True
                if kind == "add": icon_row(title, graphic, timer, now)
                else: drop_src((0, norm(title)), "icon")
            if now >= st["next_icons"]:
                st["next_icons"] = now + ICON_RESYNC
                if not st["icons_seen"] and st["next_icons"] - ICON_RESYNC > st["started"] + 1.0: return
                present = set()
                for b in API.ActiveBuffs() or []:
                    title = str(b.Title or "")
                    if not title: continue
                    present.add(norm(title)); st["icons_seen"] = True; r = rows.get((0, norm(title)))
                    if r is None or "icon" not in r["srcs"]:
                        icon_row(title, int(b.Graphic or 0), int(b.Timer or 0), now)
                for key in [k for k, r in rows.items() if not k[0] and "icon" in r["srcs"] and k[1] not in present]:
                    drop_src(key, "icon")
        def expire(now):
            if not rows: return
            for r in list(rows.values()):
                key, srcs = r["key"], r["srcs"]; end = r["end"]
                if r["who"] and r["away"] and now - r["away"] > 60.0 and (end is None or now > end):
                    drop_row(key); continue
                if "icon" in srcs or "stat" in srcs or "flag" in srcs: continue
                if r["watch"] and r["seen"]: continue
                if "line" in srcs and "cast" not in srcs:
                    if now - r["start"] > 60.0: drop_row(key)
                    continue
                if end is None:
                    if not r["watch"] and now - r["start"] > 3600.0: drop_row(key)
                    continue
                if now > max(end, r["most"] or 0) + 1.0: drop_row(key)
        def warn(now):
            lead = settings["warn"]
            if not lead or not settings["me"]: return
            for r in rows.values():
                if r["who"] or r["kind"] != "buff" or r["end"] is None: continue
                left = r["end"] - now; key = r["key"]
                if 0 < left <= lead and st["warned"].get(key) != r["end"]:
                    st["warned"][key] = r["end"]
                    HOST.alert(ALERT_KIND, "%s runs out in %d s" % (SPELL_OF.get(r["sid"], r.get("label") or r["sid"]),
                                                                  int(left + 0.5)), "info", who=r["sid"])
        queue = Kit.queuer(st)
        def build_window():
            n = settings["rows"]; slots = []
            g, store, c = wnd.begin(360, 2 * Kit.MARGIN + 30 + Kit.GAP + n * ROW_H + 12)
            if not st["minimized"]:
                M = Kit.MARGIN; IW = 360 - 2 * M; wnd.frame(g); yb = M + 30 + Kit.GAP
                Kit.add_section(g, M, yb, IW, n * ROW_H + 12)
                c["empty"] = Kit.add_label(g, "", M + 12, yb + 10, Kit.HUE_INFO)
                for i in range(n): slots.append(make_slot(g, i, M, yb + 6 + i * ROW_H, IW))
            wnd.end(g, {"slots": slots, "nrows": n}); st["redraw"] = True; draw(time.time())
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, default=(60, 260), mini=(MINI_W, MINI_H),
                         icon=TRAY_ICON, lock=False, clear={"slots": []})
        def row_pic(g, x, y, px):
            pic = G.CreateGumpPic(SPELL_ICON_BASE, x, y); pic.SetPos(x, y); pic.SetWidth(px); pic.SetHeight(px)
            pic.SetAcceptMouseInput(False); g.Add(pic); return pic
        def set_icon(s, icon, px):
            s["icon_g"] = icon; s["pic"].Graphic = icon; s["pic"].SetWidth(px); s["pic"].SetHeight(px)
        def make_slot(g, i, sx, ry, IW):
            s = {"row": None, "prev": (None, 0.0), "vis": True, "icon_g": None,
                 "tip": None, "tx": None, "fw": -1, "col": None, "x": sx, "y": ry, "iw": IW}
            s["pic"] = row_pic(g, sx + 6, ry + 2, ICON_PX)
            s["name"] = Kit.add_label(g, "", sx + 34, ry + 1, Kit.HUE_TEXT)
            s["time"] = Kit.add_label(g, "", sx + IW - 50, ry + 1, Kit.HUE_INFO); bw = IW - 34 - 10; s["bw"] = bw
            s["bg"] = Kit.add_box(g, sx + 34, ry + 19, bw, 5, 0.9, "#202020")
            s["fill"] = Kit.add_box(g, sx + 34, ry + 19, bw, 5, 1.0, "#2f9a3c")
            s["hit"] = Kit.catcher(g, sx, ry, IW, ROW_H - 2, row_click(lambda: win["slots"], i), ""); set_vis(s, False)
            return s
        def row_click(get, i):
            def handler(*args):
                cells = get()
                if i >= len(cells): return
                c = cells[i]; r = c["row"]; prev, at = c["prev"]
                if 0 <= time.time() - at <= 0.15: r = prev
                if r is None: return
                if r[0] and Follow.alt_held(): queue(("follow", r[0]))(); return
                queue(("clear", r))()
            return handler
        def set_vis(s, on):
            if s["vis"] == on: return
            s["vis"] = on
            for k in ("pic", "name", "time", "bg", "fill", "hit"):
                if s.get(k) is not None: s[k].IsVisible = on
        def shown_rows():
            out = []
            for r in rows.values():
                if r["who"]:
                    if not settings["others"]: continue
                elif r["kind"] == "buff":
                    if not settings["me"]: continue
                elif not settings["debuff"]: continue
                out.append(r)
            out.sort(key=row_order); return out
        def row_order(r):
            end = r["end"]
            return (1 if r["who"] else 0, SPELL_ORDER.get(r["kind"], 2), end if end is not None else 1e18, r["start"])
        def fmt_secs(s):
            s = int(s + 0.999)
            if s < 60: return "%ds" % s
            if s < 3600: return "%d:%02d" % (s // 60, s % 60)
            return "%dh %02d" % (s // 3600, (s % 3600) // 60)
        def row_time(r, now):
            end = r["end"]
            if end is None:
                if r["sid"] in ("reactivearmor", "magicreflection") and not r["who"]: return "on", None, False
                return "+" + fmt_secs(max(0.0, now - r["start"])), None, False
            left = end - now
            if left > 0:
                total = max(0.1, end - r["start"]); return fmt_secs(left), max(0.0, min(1.0, left / total)), False
            if r["most"] and now < r["most"]: return "soon", None, True
            return "due" if ("stat" in r["srcs"] or "icon" in r["srcs"]) else "0s", 0.0, True
        def tip_of(r):
            if r["who"]:
                return ("%s on %s, cast by you. Click: clear this row. Alt+click: auto-follow (again to stop)"
                        % (SPELL_OF.get(r["sid"], r["sid"]), r["name"] or "them"))
            if "stat" in r["srcs"] and r["end"] is None:
                return "From a stat step; ends when it steps back. Click: clear this row."
            if r["end"] is None and r["sid"] in ("reactivearmor", "magicreflection"):
                return "Up until used up (the shard doesn't say when). Click: clear this row."
            return "Click: clear this row"
        SIDES = ("player", "target"); PIECE = {"player": KEY, "target": KEY + ".target"}
        def row_mode(): return st.get("row_mode", False)
        def form_tick(now):
            if 0 <= st.get("form_at", 0.0) - now <= FORM_EVERY: return
            st["form_at"] = now + FORM_EVERY; fg = pieces_frame("player"); want = fg is not None
            if want != row_mode(): set_form(want)
            elif want:
                for side in SIDES:
                    ui = rowui[side]; fs = pieces_frame(side); fw = ui["w"]
                    if fs is not None:
                        r = _rect_of(fs)
                        if r is None: continue
                        fw = r[2]
                    if ui["g"] is None or fw != ui["w"]: build_row(side, fw, max(0, ui["lines"]))
        def set_form(row):
            st["row_mode"] = row
            if row:
                HOST.dock_remove(KEY); wnd.close()
                for side in SIDES:
                    fs = pieces_frame(side); r = _rect_of(fs) if fs is not None else None
                    build_row(side, r[2] if r is not None else 200, 0)
                for side in SIDES: pieces_add(PIECE[side], side, 1, lambda s=side: rowui[s]["g"])
            else: drop_rows(); build_window(); wnd.dock()
            st["redraw"] = True
        def drop_rows():
            for side in SIDES:
                pieces_remove(PIECE[side]); ui = rowui[side]; g, ui["g"] = ui["g"], None
                ui["cells"], ui["lines"], ui["w"] = [], -1, 0; Kit.dispose(g)
        def build_row(side, fw, lines):
            ui = rowui[side]; old, ui["g"] = ui["g"], None; fw = max(ROW_PITCH + 2 * ROW_PAD, int(fw))
            per = max(1, (fw - 2 * ROW_PAD) // ROW_PITCH); h = max(1, lines) * ROW_LINE + 2 * ROW_PAD; x, y = 0, 0
            if Kit.is_open(old): x, y = old.GetX(), old.GetY()
            g = G.CreateGump(True, False); Kit.add_section(g, 0, 0, fw, h, alpha=0.6); cells = []
            n = min(ROW_MAX, per * max(1, lines)); x0 = ROW_PAD + (fw - 2 * ROW_PAD - per * ROW_PITCH) // 2
            for i in range(n):
                ln, col = divmod(i, per)
                cells.append(make_cell(g, side, i, x0 + col * ROW_PITCH, ROW_PAD + ln * ROW_LINE))
            Kit.place(g, x, y, fw, h); G.AddGump(g); g.IsVisible = lines > 0
            ui.update({"g": g, "cells": cells, "per": per, "lines": lines, "w": fw}); Kit.dispose(old)
        def make_cell(g, side, i, cx, cy):
            c = {"row": None, "prev": (None, 0.0), "icon_g": None, "tip": None, "vis": True, "x": cx, "y": cy,
                 "tw": None}
            c["pic"] = row_pic(g, cx + (ROW_PITCH - ROW_ICON) // 2, cy, ROW_ICON)
            c["time"] = Kit.add_label(g, "", cx, cy + ROW_ICON + 1, Kit.HUE_INFO); c["time"].SetAcceptMouseInput(False)
            c["hit"] = Kit.catcher(g, cx, cy, ROW_PITCH, ROW_LINE - 2, row_click(lambda: rowui[side]["cells"], i), "")
            return c
        def draw_row(side, now, mine):
            ui = rowui[side]; mine = mine[:ROW_MAX]; per = ui["per"]
            lines = (len(mine) + per - 1) // per if mine else 0
            if lines != ui["lines"]: build_row(side, ui["w"] or 200, lines)
            if ui["g"] is None: return
            for i, c in enumerate(ui["cells"]):
                r = mine[i] if i < len(mine) else None; key = r["key"] if r is not None else None
                if key != c["row"]: c["prev"] = (c["row"], now); c["row"] = key
                if r is None: set_vis(c, False); continue
                set_vis(c, True); icon = r["icon"]
                if icon != c["icon_g"]: set_icon(c, icon, ROW_ICON)
                text, _frac, dim = row_time(r, now)
                if r["end"] is None: text = ""
                tw = Kit.text_px(text) if text else 0
                if tw != c["tw"]:
                    c["tw"] = tw; Kit.ui_pos(c["time"], c["x"] + max(0, (ROW_PITCH - tw) // 2), c["y"] + ROW_ICON + 1)
                Kit.set_text(c["time"], text, Kit.HUE_BAD if (dim or r["kind"] == "debuff") else Kit.HUE_TEXT)
                tk = text_key(r)
                if tk != c.get("tipk"):
                    c["tipk"] = tk; tip = "%s. %s" % (display_name(r), tip_of(r))
                    if tip != c["tip"]: c["tip"] = tip; c["hit"].SetTooltip(tip)
        def draw(now):
            rm = row_mode()
            if not rm and (win["g"] is None or (st["minimized"] and st["docked"])): return
            if not st["redraw"] and st.get("drawn_at", 0.0) + 0.25 > now >= st.get("drawn_at", 0.0) \
                    and st.get("drawn_ver") == st["ver"]:
                return
            st["redraw"] = False; st["drawn_at"], st["drawn_ver"] = now, st["ver"]; shown = shown_rows()
            if rm:
                tgt = PIECES_TARGET["fn"]() if PIECES_TARGET["fn"] is not None and pieces_frame("target") is not None \
                    else 0
                mine = [r for r in shown if not r["who"]]; theirs = [r for r in shown if tgt and r["who"] == tgt]
                if rowui["player"]["g"] is not None: draw_row("player", now, mine)
                if rowui["target"]["g"] is not None: draw_row("target", now, theirs)
                return
            c = win["c"]
            if st["minimized"]:
                lbl = c.get("status")
                if lbl is not None:
                    if shown:
                        t = row_time(shown[0], now)[0]; txt = "%s: %s %s" % (TITLE, display_name(shown[0]), t)
                        if len(shown) > 1: txt += "  (+%d)" % (len(shown) - 1)
                        txt = Kit.fit(txt, MINI_W - 90)
                    else: txt = "%s: no timers" % TITLE
                    Kit.set_text(lbl, txt, Kit.HUE_INFO)
                return
            slots = win["slots"]
            Kit.set_text(c["empty"], "" if shown else "No timers yet; your buffs and casts show here.", Kit.HUE_INFO)
            for i, s in enumerate(slots):
                r = shown[i] if i < len(shown) else None; key = r["key"] if r is not None else None
                if key != s["row"]: s["prev"] = (s["row"], now); s["row"] = key
                if r is None: set_vis(s, False); continue
                set_vis(s, True); draw_slot(s, r, now)
        def draw_slot(s, r, now):
            icon = r["icon"]
            if icon != s["icon_g"]: set_icon(s, icon, ICON_PX)
            if r["who"]: hue, colk = (Kit.HUE_INFO if r["away"] else Kit.HUE_TITLE), "other"
            elif r["kind"] == "debuff": hue, colk = Kit.HUE_BAD, "debuff"
            else: hue, colk = Kit.HUE_TEXT, "buff"
            text, frac, dim = row_time(r, now)
            if r["who"] and r["away"]: text = text + " (away)"
            tw = Kit.text_px(text); tx = s["x"] + s["iw"] - 8 - tw
            if tx != s["tx"]: s["tx"] = tx; Kit.ui_pos(s["time"], tx, s["y"] + 1)
            Kit.set_text(s["time"], text, Kit.HUE_BAD if dim else Kit.HUE_INFO); tk = text_key(r)
            room = tx - (s["x"] + 34) - 6; nk = (tk, room)
            if nk != s.get("namek"):
                name = display_name(r); s["namek"], s["name_txt"] = nk, Kit.fit(name, max(20, room))
            Kit.set_text(s["name"], s["name_txt"], hue)
            if frac is None: fw, colk = s["bw"], "dim"
            else:
                fw = int(round(s["bw"] * frac))
                if dim: colk = "dim"
            fill = s["fill"]
            if fw != s["fw"]:
                s["fw"] = fw
                if fw <= 0: fill.IsVisible = False
                else: Kit.ui_w(fill, fw); fill.IsVisible = True
            if colk != s["col"]: s["col"] = colk; rgb = COL[colk]; fill.SetBaseColor(rgb[0], rgb[1], rgb[2], 255)
            if tk != s.get("tipk"):
                s["tipk"] = tk; tip = tip_of(r)
                if tip != s["tip"]: s["tip"] = tip; s["hit"].SetTooltip(tip)
        PAGE = (("WINDOW  (what it lists)", (
                    ("check", "me", "Show the buffs on you", "Bless, Strength, Protection, Reactive Armor, Magic "
                     "Reflection, Night Sight and more"),
                    ("check", "debuff", "Show what is done to you (paralyze, poison, curses)",
                     "Paralyzed, Poison (with its level), Curse, Clumsy, Feeblemind and Weaken on you"),
                    ("check", "others", "Show your spells on others", "What you cast on someone else. Alt+click such "
                     "a row: auto-follow (again to stop)"),
                    ("num", "rows", "Rows shown:", "Rows the window has room for", None, ROWS_MIN, ROWS_MAX,
                     {"clamp": False})), {"sh": 140}), ("HOW TIMERS ARE FOUND  (your casts always count)", (
                    ("check", "stats", "Watch your stats for Bless, Curse and their kin",
                     "A Str, Dex or Int step of %d or more is a spell on you (all three: Bless / Curse); potions show "
                     "too" % STAT_MIN_STEP),
                    ("check", "icons", "Use the shard's buff icons when it sends them", "Exact names and times when "
                     "the shard sends icons (a classic shard sends none)")), {"sh": 90}),
                ("ALERTS  (sound: Settings > Alerts)", (
                    ("num", "warn", "Warn before a buff on you runs out:", "One alert this many seconds before it ends "
                     "(0-%d, 0 = never)" % WARN_MAX, "s", 0, WARN_MAX, {"clamp": False}),), {"sh": 64}))
        def on_change(old, new):
            st["redraw"] = True
            if new["icons"] and not old["icons"]: st["next_icons"] = 0.0
            if new["rows"] != old["rows"]: st["rebuild"] = True
            if new["warn"] != old["warn"]: st["warned"] = {}
        cfg = Kit.Page(settings, PAGE, save_settings, on_change, {"ldy": 4, "lgap": 12, "fw": 40})
        def svc_list(serial=None):
            now = time.time(); me = st["me"]; out = []
            for r in rows.values():
                who = r["who"] or me
                if serial is not None and who != serial: continue
                end = r["end"]
                out.append({"spell": SPELL_OF.get(r["sid"], r.get("label") or r["sid"]),
                            "serial": who, "you": not r["who"], "kind": r["kind"], "end": end,
                            "left": (end - now) if end is not None else None, "icon": r["icon"],
                            "level": r["level"], "delta": r["delta"]})
            return out
        def _start():
            now = time.time(); st_reset(); st.update({"active": True, "redraw": True, "started": now,
                                                      "minimized": wnd.start_min()})
            rows.clear()
            for stat in effects: del effects[stat][:]
            load_settings(); restore_active(now); sync_stat_rows(); hook_events()
            HOST.alert_kind(ALERT_KIND, "Buff about to run out", 0x1EA); st["row_mode"], st["form_at"] = False, 0.0
            if pieces_frame("player") is not None: set_form(True)
            else: build_window(); wnd.dock()
            HOST.services["spelltimers.list"] = svc_list
        def _tick():
            now = time.time(); form_tick(now)
            if win["g"] is None and not row_mode(): return
            if win["g"] is not None and Kit.closed(win): return
            while st["queue"]:
                action = st["queue"].pop(0); kind = action[0] if isinstance(action, tuple) else action
                if action == "redraw":
                    if not row_mode(): build_window()
                elif wnd.action(action): pass
                elif kind == "follow": Follow.toggle(action[1], TITLE)
                elif kind == "clear": clear_row(action[1])
            if st["rebuild"]:
                st["rebuild"] = False
                if not row_mode() and not st["minimized"] and settings["rows"] != win["nrows"]: build_window()
            handle_icons(now)
            if not 0 <= st["next_sample"] - now <= SAMPLE_EVERY: st["next_sample"] = now + SAMPLE_EVERY; sample(now)
            read_journal(now); resolve_pending(now)
            if any_others() and not 0 <= st["next_others"] - now <= OTHERS_EVERY:
                st["next_others"] = now + OTHERS_EVERY; watch_others(now)
            expire(now); warn(now); draw(now)
        def any_others():
            for k in rows:
                if k[0]: return True
            return False
        def clear_row(key):
            r = rows.get(key)
            if r is None: return
            if "stat" in r["srcs"]:
                for stat in ("str", "dex", "int"):
                    for e in effects[stat]:
                        sid = norm(STAT_SPELLS[(stat, 1 if e["d"] > 0 else -1)])
                        if sid == key[1] or (key[1] in ("bless", "curse") and (e["d"] > 0) == (key[1] == "bless")):
                            e["hide"] = True
            drop_row(key)
            if "stat" in r["srcs"]: sync_stat_rows()
        def _stop():
            st["shutting"] = True; st["active"] = False; HOST.dock_remove(KEY)
            if HOST.services.get("spelltimers.list") is svc_list: HOST.services.pop("spelltimers.list", None)
            drop_rows(); wnd.close(); save_settings(); save_active()
        load_settings(); return part_dict(_start, _tick, _stop, cfg.height, cfg.build, cfg.poll, cfg.closed)
    def _part_swing():
        try: from System import DateTime
        except Exception: DateTime = None
        TITLE = "Swing Bar"
        SATIETY_TABLE = [(0,  4,  -10, "Starving"), (5,  9,   -5, "Hungry"), (10, 14,   0, "Fed"),
            (15, 19,   0, "Full"), (20, 20,   0, "Stuffed"),]
        HUNGER_DECAY_SECONDS = 300; DEFAULT_HUNGER = 20
        ENEMY_SKILL_BY_NAME = [("lich lord", 90), ("lich", 70), ("dragon", 90), ("daemon", 90),
            ("troll", 60), ("ogre lord", 85), ("ogre", 65), ("orc captain", 80),
            ("orc", 55), ("ettin", 55), ("skeleton", 50), ("zombie", 35),
            ("rat", 25), ("headless", 30), ("mongbat", 10),]
        DEFAULT_MONSTER_SKILL = 60; ENEMY_SKILL_MIN, ENEMY_SKILL_MAX = 0, 120; HK_SET_TARGET   = "CTRL+SHIFT+T"
        HK_RESYNC       = "CTRL+SHIFT+R"; HK_HUNGER_UP    = "CTRL+SHIFT+UP"; HK_HUNGER_DOWN  = "CTRL+SHIFT+DOWN"
        HK_ENEMY_UP     = "CTRL+SHIFT+RIGHT"; HK_ENEMY_DOWN   = "CTRL+SHIFT+LEFT"; WINDOW_X, WINDOW_Y = 300, 300
        BAR_FILL_HUE, BAR_FILL_COLOR = 0x0035, "#b8913a"; BAR_READY_HUE, BAR_READY_COLOR = 0x003F, "#3fa34d"
        BAR_PAUSED_HUE, BAR_PAUSED_COLOR = 0x03B2, "#6b6b6b"; SWING_HISTORY = 10; MIN_GAP_MS = 250
        HISTORY_KEY = "SwingTimer_history"; DISARM_TEXTS = ("you have been disarmed", "your weapon has been disarmed")
        DISMOUNT_TEXTS = ("you have been knocked off", "you fall off of your mount", "you fall off your mount")
        NOTICE_FROM = ("system", ""); ALERT_NOTICE = "swing.notice"
        EAT_LOOKBACK_S = 30.0; HUE_GREEN, HUE_YELLOW, HUE_RED, HUE_GREY = 68, 53, 33, 946; HUE_TEXT = Kit.HUE_TEXT
        SW, FE, MA, WR = "Swordsmanship", "Fencing", "Mace Fighting", "Wrestling"; AR = "Archery"
        _W = [("Broadsword",       45, SW, (0xF5E, 0xF5F)), ("Cutlass",          45, SW, (0x1441, 0x1440)),
            ("Katana",           58, SW, (0x13FF, 0x13FE)), ("Longsword",        35, SW, (0xF61, 0xF60)),
            ("Scimitar",         30, SW, (0x13B6, 0x13B5)), ("Viking Sword",     30, SW, (0x13B9, 0x13BA)),
            ("Thin Longsword",   35, SW, (0x13B8, 0x13B7)), ("Butcher Knife",    40, SW, (0x13F6, 0x13F7)),
            ("Cleaver",          40, SW, (0xEC3, 0xEC2)), ("Skinning Knife",   40, SW, (0xEC4, 0xEC5)), 
            ("Axe",              37, SW, (0xF49, 0xF4A)), ("Battle Axe",       31, SW, (0xF47, 0xF48)),
            ("Double Axe",       37, SW, (0xF4B, 0xF4C)), ("Executioner's Axe",37, SW, (0xF45, 0xF46)),
            ("Large Battle Axe", 29, SW, (0x13FB, 0x13FA)), ("Two Handed Axe",   31, SW, (0x1443, 0x1442)),
            ("Pickaxe",          35, SW, (0xE86, 0xE85)), ("Hatchet",          41, SW, (0xF43, 0xF44)), 
            ("Bardiche",         26, SW, (0xF4D, 0xF4E)), ("Halberd",          25, SW, (0x143E, 0x143F)), 
            ("Dagger",           55, FE, (0xF52, 0xF51)), ("Kryss",            53, FE, (0x1401, 0x1400)),
            ("Short Spear",      50, FE, (0x1403, 0x1402)), ("Spear",            46, FE, (0xF62, 0xF63)),
            ("War Fork",         45, FE, (0x1405, 0x1404)), ("Pitchfork",        45, FE, (0xE87, 0xE88)), 
            ("Club",             40, MA, (0x13B4, 0x13B3)), ("Hammer Pick",      30, MA, (0x143D, 0x143C)),
            ("Mace",             30, MA, (0xF5C, 0xF5D)), ("Maul",             30, MA, (0x143B, 0x143A)),
            ("War Axe",          40, MA, (0x13B0, 0x13AF)), ("War Hammer",       31, MA, (0x1439, 0x1438)),
            ("War Mace",         26, MA, (0x1407, 0x1406)), ("Quarter Staff",    48, MA, (0xE89, 0xE8A)),
            ("Gnarled Staff",    33, MA, (0x13F8, 0x13F9)), ("Black Staff",      35, MA, (0xDF0, 0xDF1)),
            ("Shepherd's Crook", 30, MA, (0xE81, 0xE82)), ("Bow",              20, AR, (0x13B2, 0x13B1)),
            ("Crossbow",         18, AR, (0xF50, 0xF4F)), ("Heavy Crossbow",   10, AR, (0x13FD, 0x13FC)),]
        WEAPONS = {}
        for _name, _spd, _skill, _gfx in _W:
            for _g in _gfx: WEAPONS[_g] = (_name, _spd, _skill)
        FISTS = ("Fists", 30, WR); SWING_SOUNDS = {0x232, 0x233, 0x234, 0x237, 0x238, 0x239, 0x23A, 0x23B, 0x23C}
        ACCURACY = [("supremely accurate", 10), ("exceedingly accurate", 8),
                    ("eminently accurate", 6), ("surpassingly accurate", 4), ("accurate", 2)]
        def swing_delay_ms(stat_value, weapon_speed):
            v = (stat_value + 100) * weapon_speed
            if v <= 0: v = 1
            return 15000.0 / v * 1000.0
        def satiety_info(hunger):
            h = int(round(max(0, min(20, hunger))))
            for lo, hi, mod, label in SATIETY_TABLE:
                if lo <= h <= hi: return mod, label
            return 0, "?"
        def final_hit_chance(atk_skill, def_skill, accuracy_pct, hunger):
            mod, _ = satiety_info(hunger)
            chance = (max(atk_skill, -49.9) + 50.0) / ((max(def_skill, -49.9) + 50.0) * 2.0)
            chance *= 1.0 + accuracy_pct / 100.0; return max(0.0, min(1.0, chance * (1.0 + mod / 100.0)))
        def now_ms(): return time.time() * 1000.0
        def current_weapon():
            for layer in ("OneHanded", "TwoHanded"):
                item = API.FindLayer(layer)
                if item and int(item.Graphic) in WEAPONS:
                    name, spd, skill = WEAPONS[int(item.Graphic)]; return name, spd, skill, accuracy_of(item)
            return FISTS + (0,)
        acc_cache = {}
        def accuracy_of(item):
            serial = int(item.Serial); hit = acc_cache.get(serial) if serial else None
            if hit is not None and time.time() < hit[1]: return hit[0]
            text = (item.Name or "").lower()
            if "accurate" not in text: text = (API.ItemNameAndProps(serial, False) or "").lower()
            pct = 0
            for key, p in ACCURACY:
                if key in text: pct = p; break
            if serial:
                if len(acc_cache) > 50: acc_cache.clear()
                acc_cache[serial] = (pct, time.time() + (1e9 if pct else 2.0))
            return pct
        def enemy_skill(mob, override, name=None):
            if override is not None: return override
            if mob is None: return cfg["enemy_default"]
            name = (mob.Name or "" if name is None else name).lower()
            for key, val in ENEMY_SKILL_BY_NAME:
                if key in name: return val
            return 100 if mob.IsHuman else cfg["enemy_default"]
        def load_var(key, default):
            try: return float(Kit.get_var(key, str(default)))
            except Exception: return float(default)
        def save_var(key, value): Kit.put_var(key, str(value))
        def clamp_enemy(v):
            try: return int(max(ENEMY_SKILL_MIN, min(ENEMY_SKILL_MAX, int(round(float(v))))))
            except Exception: return DEFAULT_MONSTER_SKILL
        cfg = {"enemy_default": clamp_enemy(load_var("swingtimer_enemy_default", DEFAULT_MONSTER_SKILL))}
        class State:
            last_swing = None; cycle_ms = None; gaps = []; gaps_weapon = None; history = {}; slow = []; dirty = False
            paused_at = None; target_serial = 0; enemy_override = None; hunger = DEFAULT_HUNGER; hunger_clock = now_ms()
            seen_sounds = set(); sounds = []; keys = []; notice = None
        S = State(); say = Kit.sayer(TITLE)
        def average_gap():
            if not S.gaps: return None
            return sum(S.gaps) / float(len(S.gaps))
        def match_weapon(weapon):
            wkey = (weapon[0], int(weapon[1]))
            if S.gaps_weapon == wkey: return False
            S.gaps_weapon = wkey; S.gaps = S.history.setdefault(wkey, []); S.slow = []; return True
        files = {"saved_at": 0.0, "save": False, "import": False}
        def parse_history(text, sep):
            out = {}
            for rec in text.split(sep):
                p = rec.strip().split("|")
                if len(p) != 3 or not p[0]: continue
                try: spd = int(p[1]); gaps = [float(v) for v in p[2].split(",") if v.strip()]
                except Exception: continue
                gaps = [g for g in gaps if g >= MIN_GAP_MS][-SWING_HISTORY:]
                if gaps: out[(p[0], spd)] = gaps
            return out
        def load_history():
            S.history = {}; S.gaps, S.gaps_weapon, S.dirty, S.slow = [], None, False, []; raw = Kit.get_var(HISTORY_KEY)
            if raw: S.history = parse_history(raw, ";")
            files["import"] = not S.history
        def import_old_file():
            if now_ms() < files.get("import_next", 0.0): return
            files["import_next"] = now_ms() + 1000.0
            try: serial = int(API.Player.Serial)
            except Exception: serial = 0
            if not serial: return
            files["import"] = False
            try:
                path = Kit.data_path("_swing_timer_{}.txt".format(serial))
                if not os.path.exists(path): return
                with open(path, "r") as f: text = f.read()
            except Exception: return
            found = parse_history(text, "\n"); n = 0
            for wkey, gaps in found.items():
                if not S.history.get(wkey): S.history[wkey] = gaps; n += 1
            if not n: return
            S.gaps_weapon = None; S.dirty = True; save_history()
            say("brought over learned swings of %s from the old data file." % Kit.count(n, "weapon"), Kit.HUE_GOOD)
        def save_history():
            files["save"] = False
            recs = ["%s|%d|%s" % (name.replace("|", "/").replace(";", "/"), spd, ",".join("%.0f" % g for g in gaps))
                    for (name, spd), gaps in sorted(S.history.items()) if gaps]
            Kit.put_var(HISTORY_KEY, ";".join(recs)); S.dirty = False; files["saved_at"] = now_ms()
        def count_gap(gap, formula):
            avg = average_gap()
            if gap < MIN_GAP_MS or gap > (avg or formula) + 3000: S.slow = []; return
            if avg is not None and gap > avg * 1.15:
                S.slow.append(gap)
                if len(S.slow) < 3: return
                S.gaps[:] = S.slow; S.slow = []; set_notice("Slow: low stamina", HUE_YELLOW)
            else: S.slow = []; S.gaps.append(gap)
            if len(S.gaps) > SWING_HISTORY: del S.gaps[:-SWING_HISTORY]
            S.dirty = True
        def mark_swing(when):
            if S.paused_at is not None:
                if S.last_swing is not None: S.last_swing += max(0.0, when - S.paused_at)
                S.paused_at = when
            weapon = current_weapon(); formula = swing_delay_ms(int(API.Player.Stamina), weapon[1])
            swapped = match_weapon(weapon)
            if S.last_swing is not None and not swapped: count_gap(when - S.last_swing, formula)
            S.last_swing = when; S.cycle_ms = average_gap() or formula
        def _sound_age_ms(entry):
            try: return max(0.0, (DateTime.Now - entry.Time).TotalMilliseconds)
            except Exception: return 0.0
        def sound_of(entry):
            sid = int(entry.ID)
            if sid not in SWING_SOUNDS: return None
            return (sid, int(entry.X), int(entry.Y), str(entry.Time), now_ms() - _sound_age_ms(entry))
        def handle_sound(snd, p):
            sid, sx, sy, tstamp, when = snd
            if sx != int(p.X) or sy != int(p.Y): return
            key = (sid, sx, sy, tstamp)
            if key in S.seen_sounds: return
            S.seen_sounds.add(key)
            if len(S.seen_sounds) > 200: S.seen_sounds.clear()
            mark_swing(when)
        def on_sound_event(*args):
            if not win.get("active"): return
            for a in args:
                try: snd = sound_of(a)
                except Exception: continue
                if snd is not None and len(S.sounds) < 50:
                    S.sounds.append(snd)
                    if not loop.get("fast"):
                        xy = loop.get("xy")
                        if xy is None or (snd[1], snd[2]) == xy: HOST.poke()
                return
        hooked = [False]
        def set_notice(text, hue): S.notice = (text, hue, now_ms() + 4000.0)
        note = {"rd": None, "clock": 0.0, "own": (TITLE.lower(),)}
        def own_starts():
            own = set([TITLE.lower()])
            for t in [APP_NAME] + [s.title for s in HOST.slots]:
                t = str(t or "").strip().lower()
                if t: own.add(t)
            return tuple(own)
        def check_notices():
            own = note["own"]
            for ln in note["rd"].new(time.time() - Journal.read_at >= 0.5):
                low = ln.low
                if low.startswith(own) or str(ln.name or "").lower() not in NOTICE_FROM: continue
                for texts, what in ((DISARM_TEXTS, ("Disarmed!", "You were disarmed")),
                                    (DISMOUNT_TEXTS, ("Dismounted!", "You were dismounted"))):
                    if any(t in low for t in texts):
                        set_notice(what[0], HUE_RED); HOST.alert(ALERT_NOTICE, what[1]); break
        EAT_MSGS = [("simply too full to eat any more", 20, 20), ("but you are stuffed", 20, 20),
            ("but are still extremely hungry", 0, 4), ("begin to feel more satiated", 5, 9),
            ("you feel much less hungry", 10, 14), ("feel quite full after consuming", 15, 19),]
        eat_rd = {"rd": None}
        def check_eating():
            rd = eat_rd["rd"]
            if rd is None: eat_rd["rd"] = Journal.reader(); lines = Journal.recent(EAT_LOOKBACK_S)
            else: lines = rd.new()
            if not lines: return
            try: now_ticks = float(DateTime.Now.Ticks)
            except Exception: now_ticks = time.time() * 1e7
            for ln in lines:
                if ln.ticks > 1e12 and (now_ticks - ln.ticks) / 1e7 > EAT_LOOKBACK_S: continue
                txt = ln.low
                for text, lo, hi in EAT_MSGS:
                    if text in txt: set_hunger(max(lo, min(hi, S.hunger + 3 if lo != hi else hi))); break
        def set_hunger(value):
            FOOD_SEEN[0] = True; S.hunger = float(max(0, min(20, value))); S.hunger_clock = now_ms()
            save_var("swingtimer_hunger", S.hunger)
        def decay_hunger():
            elapsed = now_ms() - S.hunger_clock; step = HUNGER_DECAY_SECONDS * 1000.0
            if elapsed >= step:
                ticks = int(elapsed // step); S.hunger = max(0.0, S.hunger - ticks); S.hunger_clock += ticks * step
                save_var("swingtimer_hunger", S.hunger)
        FOLLOW_TIP = " Alt+click: auto-follow (again to stop)"
        def note_key(what, value):
            if len(S.keys) < 50: S.keys.append((what, value)); HOST.poke()
        def on_target_picked(serial):
            if serial: S.target_serial = int(serial); S.enemy_override = None
        def run_keys():
            while S.keys:
                what, v = S.keys.pop(0)
                if what == "target": say("target the mobile you are fighting."); HOST.pick_target(10, on_target_picked)
                elif what == "resync": mark_swing(v)
                elif what == "hunger": set_hunger(round(S.hunger) + v)
                elif what == "enemy":
                    mob = resolve_target(); base = enemy_skill(mob, S.enemy_override)
                    S.enemy_override = max(ENEMY_SKILL_MIN, min(ENEMY_SKILL_MAX, base + v))
                elif what == "follow":
                    mob = loop.get("mob")
                    if mob is not None: Follow.toggle(int(mob.Serial), TITLE)
                    else: say("no target to follow.")
        HOTKEYS = ((HK_SET_TARGET, lambda: note_key("target", None), "pick the mobile you fight"),
                   (HK_RESYNC, lambda: note_key("resync", now_ms()), "restart the bar (I just swung)"),
                   (HK_HUNGER_UP, lambda: note_key("hunger", 1), "satiety estimate +1"),
                   (HK_HUNGER_DOWN, lambda: note_key("hunger", -1), "satiety estimate -1"),
                   (HK_ENEMY_UP, lambda: note_key("enemy", 5), "enemy skill +5"),
                   (HK_ENEMY_DOWN, lambda: note_key("enemy", -5), "enemy skill -5"))
        def not_typing(fn):
            def run(*args):
                if not HOST.typing(): fn()
            return run
        def register_hotkeys(on):
            for key, fn, what in HOTKEYS:
                if on:
                    API.OnHotKey(key, not_typing(fn)); HOST.hotkeys_owned[key] = TITLE
                    HOST.hotkey_note(key, TITLE, what)
                else: API.OnHotKey(key); HOST.hotkeys_owned.pop(key, None); HOST.hotkey_drop(key, TITLE)
        def resolve_target():
            for serial in (S.target_serial, API.LastTargetSerial):
                if serial:
                    m = API.FindMobile(serial)
                    if m and not m.IsDead: return m
            N = API.Notoriety; return API.NearestMobile([N.Gray, N.Criminal, N.Enemy, N.Murderer], 2)
        set_label = Kit.set_text
        STEP_FALLBACK = {(False, False): 400.0, (False, True): 200.0, (True, False): 200.0, (True, True): 100.0}
        STEP_MIN_MS, STEP_MAX_MS = 50.0, 800.0; KITE_VAR = "swingtimer_kite"
        KITE_COLOR = {"close": "#E8C25A", "turn": "#3CD070", "far": "#E04040", "idle": "#C8C8C8"}
        KITE_HUE = {"close": Kit.HUE_TITLE, "turn": Kit.HUE_GOOD, "far": Kit.HUE_BAD, "idle": Kit.HUE_INFO}
        kite = {"on": bool(int(load_var(KITE_VAR, 1) or 0)), "steps": {}, "xy": None, "at": 0.0,
                "stat0": None, "swing0": None, "px": None, "state": None, "tiles": None}
        ROW1_Y, ROW2_Y = 16, 34; PAD = 3; LAYOUT_KEY = "swing"
        bg_opacity = max(0.0, min(100.0, load_var("swingtimer_bg_opacity", 85)))
        win = {"bar_w": 109, "x1": 0, "row1": 0, "food_w": [0] * 21, "fill_w": -1, "fill_state": None,
               "shown": {}, "tips": {}, "active": False, "closing": False}
        ctl = {}; cfgui = {"f": None}
        def is_open(): return Kit.is_open(ctl.get("gump"))
        def make_fill(hue, color, h):
            if Kit.pic_size(Kit.LINE_BLUE)[0] > 0:
                t = Kit.add_tiled(ctl["gump"], Kit.LINE_BLUE, win["x1"], ROW1_Y, 1, h, hue=hue)
                if t is not None: return t
            b = G.CreateGumpColorBox(1.0, color); b.SetRect(win["x1"] + 1, ROW1_Y + 1, 1, h)
            b.SetAcceptMouseInput(False); ctl["gump"].Add(b); return b
        def window_size():
            win["row1"] = win["bar_w"] + 5 + max(Kit.text_w("15.0s"), readout_room())
            return win["row1"] + 2 * PAD + 16, 58
        def build_window(x=None, y=None):
            saved = x is None
            if saved: x = int(load_var("swingtimer_x", WINDOW_X)); y = int(load_var("swingtimer_y", WINDOW_Y))
            old = ctl.get("gump"); ctl.clear(); bw = Kit.pic_size(Kit.LINE_RED)[0]
            fh = Kit.pic_size(Kit.LINE_BLUE)[1] or 8; win["bar_w"] = bw or 109; w, h = window_size()
            win["x1"] = x1 = 8 + PAD
            if saved: x, y = Kit.adapt(x, y, w, h)
            gump = G.CreateGump(True, True); Kit.place(gump, x, y, w, h); ctl["gump"] = gump
            Kit.add_window_frame(gump, w, h, corners=False)
            ctl["section"] = Kit.add_section(gump, 8, 8, w - 16, h - 16); PIECES["bg"][gump] = [ctl["section"]]
            apply_opacity()
            if bw > 0: Kit.add_pic(gump, Kit.LINE_RED, x1, ROW1_Y)
            else: Kit.add_tiled(gump, Kit.SECTION_TILE, x1, ROW1_Y, 109, 9, 1.0)
            ctl["fills"] = {"fill": make_fill(BAR_FILL_HUE, BAR_FILL_COLOR, fh),
                            "ready": make_fill(BAR_READY_HUE, BAR_READY_COLOR, fh),
                            "paused": make_fill(BAR_PAUSED_HUE, BAR_PAUSED_COLOR, fh)}
            for f in ctl["fills"].values(): f.IsVisible = False
            ctl["kite"] = {}
            for name, colour in KITE_COLOR.items():
                b = G.CreateGumpColorBox(1.0, colour); b.SetRect(x1, ROW1_Y - 1, 2, fh + 2)
                b.SetAcceptMouseInput(False)
                b.IsVisible = False; gump.Add(b); ctl["kite"][name] = b
            ctl["kite_lbl"] = Kit.add_label(gump, "", x1, ROW1_Y - 2, HUE_TEXT)
            ctl["kite_lbl"].SetAcceptMouseInput(False); kite.update({"px": None, "state": None, "tiles": None})
            ctl["swing"] = Kit.add_label(gump, "", x1 + win["bar_w"] + 5, ROW1_Y - 2, HUE_TEXT)
            ctl["notice"] = nl = Kit.add_label(gump, "", x1 + 4, ROW1_Y - 2, HUE_RED)
            nl.SetAcceptMouseInput(False); nl.IsVisible = False
            ctl["hit"] = Kit.add_label(gump, "", x1, ROW2_Y, HUE_GREY)
            ctl["food"] = Kit.add_label(gump, "", x1 + win["row1"] - Kit.text_w("Food 20/20"), ROW2_Y, HUE_TEXT)
            win["food_w"] = [Kit.text_px("Food %d/20" % i) for i in range(21)]; half = win["row1"] // 2
            ctl["tip_bar"] = Kit.catcher(gump, x1 - 2, ROW1_Y - 4, win["row1"] + 4, 18,
                                         target_click, bar_tip(None), movable=True)
            ctl["tip_hit"] = Kit.catcher(gump, x1 - 2, ROW2_Y - 2, half, 18, target_click, hit_tip(None), movable=True)
            ctl["tip_food"] = Kit.catcher(gump, x1 + half, ROW2_Y - 2, win["row1"] - half + 2, 18,
                                          lambda *a: None, food_tip(), movable=True)
            win["fill_w"], win["fill_state"], win["shown"], win["tips"] = -1, None, {}, {}; win["notice_shown"] = None
            G.AddControlOnDisposed(gump, on_close(gump)); G.AddGump(gump); Kit.on_moved(gump, save_position)
            Kit.dispose(old)
        def set_tip(key, text):
            c = ctl.get(key)
            if c is None or win["tips"].get(key) == text: return
            win["tips"][key] = text; c.SetTooltip(text)
        def target_click(*a):
            if Follow.alt_held(): note_key("follow", None)
        def bar_tip(info):
            text = "Time to your next swing. Green: ready; grey: paused (no war mode or target)."
            if info is not None:
                name, speed, delay, n = info
                text += " %s, speed %d, swing %.1f s (%s)." % (name, speed, delay / 1000.0,
                    "learned from %s" % Kit.count(n, "swing") if n else "formula")
            return text + FOLLOW_TIP
        def hit_tip(info):
            if info is None: return "Chance to hit your target; set it with %s.%s" % (HK_SET_TARGET, FOLLOW_TIP)
            who, skill, mine, theirs, acc, sat = info
            return ("Chance to hit %s: your %s %.1f vs their assumed %d, accuracy +%d%%, satiety %+d%%; set the "
                    "target with %s.%s" % (who[:20], skill, mine, theirs, acc, sat, HK_SET_TARGET, FOLLOW_TIP))
        def food_tip(label="", mod=0):
            return ("Satiety estimate%s, %+d%% to hit: drops 1 every %d min, rises when you eat%s. Adjust: %s / %s." % (
                        (": " + label.lower()) if label else "", mod, HUNGER_DECAY_SECONDS // 60,
                        "" if FOOD_SEEN[0] else " (none seen yet, so grey)", HK_HUNGER_UP, HK_HUNGER_DOWN))
        def apply_opacity(): ctl["section"].SetAlpha(bg_opacity / 100.0 * Kit.SECTION_ALPHA)
        def set_fill(progress, state):
            fw = int(win["bar_w"] * max(0, min(1000, progress)) / 1000)
            old_w, old_state = win["fill_w"], win["fill_state"]
            if fw == old_w and state == old_state: return
            win["fill_w"], win["fill_state"] = fw, state; fills = ctl["fills"]; was = old_state if old_w > 0 else None
            now = state if fw > 0 else None
            if now is not None: Kit.ui_w(fills[now], fw)
            if was != now:
                for key, on in ((was, False), (now, True)):
                    if key is not None: fills[key].IsVisible = on
        def step_note(p, t):
            xy = (int(p.X), int(p.Y)); was, at = kite["xy"], kite["at"]
            if xy == was: return
            kite["xy"], kite["at"] = xy, t
            if was is None: return
            tiles = max(abs(xy[0] - was[0]), abs(xy[1] - was[1])); dt = t - at
            if not (0 < tiles <= 4 and 0 < dt <= 700.0 * tiles): return
            ms = max(STEP_MIN_MS, min(STEP_MAX_MS, dt / float(tiles))); mode = step_mode(p)
            old = kite["steps"].get(mode); kite["steps"][mode] = ms if old is None else old + (ms - old) * 0.15
        def step_mode(p): return (bool(p.IsMounted), bool(p.IsRunning))
        def step_ms(p):
            mode = step_mode(p); v = kite["steps"].get(mode); return v if v is not None else STEP_FALLBACK[mode]
        def kite_tiles(swing_ms, step): return int(1 + (swing_ms / 2.0) / max(1.0, step))
        def kite_state(dist, ideal):
            if dist is None: return "idle"
            return "close" if dist < ideal else ("turn" if dist == ideal else "far")
        def kite_draw(p, mob, cycle, stat, w_speed):
            marks = ctl.get("kite")
            if not marks: return
            lbl = ctl.get("kite_lbl")
            if not kite["on"] or S.notice is not None:
                if kite["state"] is not None:
                    marks[kite["state"]].IsVisible = False; kite["state"] = None; kite["tiles"] = None
                    Kit.set_text(lbl, "")
                return
            swing = float(cycle)
            if kite["swing0"] != S.last_swing or kite["stat0"] is None:
                kite["swing0"], kite["stat0"] = S.last_swing, stat
            elif stat != kite["stat0"]:
                base = swing_delay_ms(kite["stat0"], w_speed)
                if base > 0: swing = swing * swing_delay_ms(stat, w_speed) / float(base)
            frac = max(0.02, min(0.98, (swing / 2.0) / max(1.0, float(cycle))))
            px = win["x1"] + int(win["bar_w"] * frac); tiles = kite_tiles(swing, step_ms(p)); dist = None
            if mob is not None:
                try: dist = int(mob.Distance)
                except Exception: dist = None
            state = kite_state(dist, tiles)
            if state != kite["state"]:
                if kite["state"] is not None: marks[kite["state"]].IsVisible = False
                marks[state].IsVisible = True; kite["state"] = state; kite["px"] = None; kite["tiles"] = None
            if px != kite["px"]: kite["px"] = px; marks[state].SetPos(px, ROW1_Y - 1); lbl.SetPos(px + 4, ROW1_Y - 2)
            if tiles != kite["tiles"]: kite["tiles"] = tiles; Kit.set_text(lbl, str(tiles), KITE_HUE[state])
        def on_close(g):
            def handler(*args):
                if win["closing"] or ctl.get("gump") is not g: return
                save_position(); ctl.clear(); HOST.disable("swing")
            return handler
        def save_position():
            g = ctl.get("gump")
            if Kit.is_open(g) and not pieces_on(LAYOUT_KEY):
                save_var("swingtimer_x", g.GetX()); save_var("swingtimer_y", g.GetY())
        FOOD_SEEN = [False]
        def satiety_text(): return "{:.0f}/20 {}".format(S.hunger, satiety_info(S.hunger)[1])
        def _pair(a, b): return "%s / %s" % (a, b.rsplit("+", 1)[1])
        def page_table():
            keys = ((_pair(HK_SET_TARGET, HK_RESYNC), "pick the target / restart the bar"),
                    (_pair(HK_HUNGER_UP, HK_HUNGER_DOWN), "satiety estimate +1 / -1"),
                    (_pair(HK_ENEMY_UP, HK_ENEMY_DOWN), "enemy skill +5 / -5"))
            return (("WINDOW", (("gap", 32), ("check", "kite", "Show the kite marker on the bar", "Turn-back point and "
                                 "tiles to kite out; colour: too close, turn now, too far", {"h": -32}),
                                ("slider", "opacity", "Background opacity:", "How solid the window's black inside is "
                                 "(0-100)", 0, 100, {"lgap": 12, "sdy": 8, "sw": 160})), {"sh": 96, "ldy": 4}),
                    ("HIT CHANCE", (("num", "enemy", "Enemy skill:", "Skill assumed for an unknown monster; players "
                                     "count as GM (%d-%d)" % (ENEMY_SKILL_MIN, ENEMY_SKILL_MAX), None, ENEMY_SKILL_MIN,
                                     ENEMY_SKILL_MAX, {"lgap": 8, "fw": 44, "stay": True}),
                                    ("slider", "satiety", "Satiety estimate:", "How well fed you are, 0 (starving) to "
                                     "20 (stuffed); low lowers the hit chance", 0, 20,
                                     {"dx": 220, "lw": 150, "sdy": 8, "sw": 120, "unit": satiety_text()})),
                     {"sh": 68, "ldy": 4}), ("HOTKEYS", [r for k, what in keys for r in (("note", k, {"stay": True}),
                                                                 ("note", what, {"dx": 330}))], {"sh": 100}))
        def config_height(w): return Kit.Form.height(page_table(), w)
        def build_config(g, x, y, w):
            cfgui["f"] = Kit.Form(g, x, y, w, {"kite": kite["on"], "opacity": int(round(bg_opacity)),
                                               "enemy": cfg["enemy_default"], "satiety": int(round(S.hunger))},
                                  page_table())
        def config_closed(): cfgui["f"] = None
        def poll_config():
            nonlocal bg_opacity; f = cfgui["f"]
            if f is None: return
            new, seen = f.read(), f.vals; f.vals = new
            if new["opacity"] != seen["opacity"]:
                bg_opacity = float(new["opacity"]); save_var("swingtimer_bg_opacity", bg_opacity)
                if is_open(): apply_opacity()
            if new["enemy"] != seen["enemy"]:
                cfg["enemy_default"] = new["enemy"]; save_var("swingtimer_enemy_default", new["enemy"])
                loop["slow_clock"] = 0.0
            if new["satiety"] != seen["satiety"]: set_hunger(new["satiety"])
            Kit.set_text(f.c["satiety_lbl"], satiety_text())
            if new["kite"] != kite["on"]: kite["on"] = new["kite"]; save_var(KITE_VAR, 1 if new["kite"] else 0)
        loop = {}
        def _start():
            win["closing"], win["active"] = False, True; files.update({"saved_at": now_ms(), "save": False})
            load_history(); del S.sounds[:], S.keys[:]; S.last_swing = S.cycle_ms = S.notice = None
            note.update({"rd": Journal.reader(), "clock": 0.0, "own": own_starts()})
            HOST.alert_kind(ALERT_NOTICE, "Disarmed or dismounted", 0x3B2)
            S.hunger = max(0.0, min(20.0, load_var("swingtimer_hunger", DEFAULT_HUNGER))); S.hunger_clock = now_ms()
            kite["on"] = bool(int(load_var(KITE_VAR, 1) or 0)); kite["steps"].clear()
            kite["xy"], kite["stat0"], kite["swing0"] = None, None, None; build_window()
            pieces_add(LAYOUT_KEY, "target", 0, lambda: ctl.get("gump")); register_hotkeys(True)
            if not hooked[0]:
                hooked[0] = True
                try: API.Events.SoundPlayed(on_sound_event)
                except Exception: pass
            loop.update({"slow_clock": 0.0, "eat_clock": 0.0, "weapon": current_weapon(), "mob": None, "my_skill": 0.0,
                         "mob_skill": enemy_skill(None, None), "mob_name": "",
                         "skill_of": None, "skill_clock": 0.0, "timer_clock": 0.0, "timer_mode": None, "fast": False})
            say("on (%s picks the target, %s restarts the bar)." % (HK_SET_TARGET, HK_RESYNC), Kit.HUE_GOOD)
        def _stop():
            win["closing"], win["active"] = True, False; register_hotkeys(False); note["rd"] = None
            if S.dirty: save_history()
            save_position(); pieces_remove(LAYOUT_KEY); save_var("swingtimer_bg_opacity", bg_opacity)
            g = ctl.get("gump"); ctl.clear(); Kit.dispose(g)
        def _tick():
            if not is_open(): loop["fast"] = False; return
            t = now_ms(); p = HOST.me()
            if p is None: return
            while S.sounds: handle_sound(S.sounds.pop(0), p)
            if S.keys: run_keys()
            if t - note["clock"] >= 100: note["clock"] = t; check_notices()
            if t - loop["slow_clock"] >= 250:
                loop["slow_clock"] = t; loop["xy"] = (int(p.X), int(p.Y)); loop["weapon"] = current_weapon()
                was = S.gaps_weapon
                if match_weapon(loop["weapon"]):
                    S.cycle_ms = None
                    if was is not None and loop["weapon"][2] == AR: S.last_swing = None; mark_swing(t)
                if S.dirty and t - files["saved_at"] >= 5000: files["save"] = True
                mob = loop["mob"] = resolve_target(); nm = (mob.Name or "") if mob is not None else ""
                loop["mob_skill"] = enemy_skill(mob, None, nm)
                loop["mob_name"] = (nm or "target") if mob is not None else ""
                if loop["weapon"][2] != loop.get("skill_of") or t - loop.get("skill_clock", 0.0) >= 1000:
                    loop["skill_of"], loop["skill_clock"] = loop["weapon"][2], t
                    loop["my_skill"] = skill_value(loop["weapon"][2])
                decay_hunger()
                if t - loop["eat_clock"] >= 1000: loop["eat_clock"] = t; check_eating()
            w_name, w_speed, w_skill, w_acc = loop["weapon"]; stat = int(p.Stamina); gaps = S.gaps
            avg = sum(gaps) / float(len(gaps)) if gaps else None; predicted = avg or swing_delay_ms(stat, w_speed)
            mob = loop["mob"]; in_combat = bool(p.InWarMode) and mob is not None
            if not in_combat:
                if S.paused_at is None: S.paused_at = t
                t_eff = S.paused_at
            else:
                if S.paused_at is not None:
                    if S.last_swing is not None: S.last_swing += t - S.paused_at
                    S.paused_at = None
                t_eff = t
            nt = S.notice
            if nt is not None and t >= nt[2]: S.notice = nt = None
            if S.last_swing is None: progress, remaining, cycle = 1000, 0.0, predicted
            else:
                cycle = S.cycle_ms or predicted; elapsed = t_eff - S.last_swing; remaining = cycle - elapsed
                progress = 1000 if elapsed >= cycle else int(elapsed / cycle * 1000)
            set_fill(progress, "paused" if not in_combat else ("ready" if progress >= 1000 else "fill"))
            step_note(p, t); kite_draw(p, mob, cycle, stat, w_speed); loop["fast"] = in_combat and progress < 1000
            if nt is not win["notice_shown"]:
                win["notice_shown"] = nt; nl = ctl["notice"]
                if nt is not None: set_label(nl, nt[0], nt[1])
                nl.IsVisible = nt is not None
            mode = (in_combat, progress >= 1000, mob is None)
            if mode != loop["timer_mode"] or t - loop["timer_clock"] >= 100:
                loop["timer_mode"], loop["timer_clock"] = mode, t
                if not in_combat: set_label(ctl["swing"], "Paused" if mob is not None else "Ready", HUE_GREY)
                elif progress >= 1000: set_label(ctl["swing"], "Ready", HUE_GREEN)
                else: set_label(ctl["swing"], "%.1fs" % (max(0.0, remaining) / 1000.0), HUE_TEXT)
            key = (w_name, w_speed, "%.1f" % (predicted / 1000.0), len(gaps))
            if win["shown"].get("bar_tip") != key:
                win["shown"]["bar_tip"] = key; set_tip("tip_bar", bar_tip((w_name, w_speed, predicted, len(gaps))))
            shown = win["shown"]; my_skill = loop["my_skill"]
            their_skill = S.enemy_override if S.enemy_override is not None else loop["mob_skill"]
            key = (mob is not None, loop["mob_name"], their_skill, my_skill, w_skill, w_acc, S.hunger)
            if shown.get("rows") != key:
                shown["rows"] = key; chance = final_hit_chance(my_skill, their_skill, w_acc, S.hunger)
                sat_mod, sat_label = satiety_info(S.hunger)
                if mob is not None:
                    set_label(ctl["hit"], "Hit %d%%" % int(round(chance * 100)),
                              HUE_GREEN if chance >= 0.60 else (HUE_YELLOW if chance >= 0.40 else HUE_RED))
                    set_tip("tip_hit", hit_tip((loop["mob_name"], w_skill, my_skill, their_skill, w_acc, sat_mod)))
                else: set_label(ctl["hit"], "Hit --%", HUE_GREY); set_tip("tip_hit", hit_tip(None))
                n = max(0, min(20, int(round(S.hunger))))
                if set_label(ctl["food"], "Food %d/20" % n, Kit.HUE_INFO if not FOOD_SEEN[0] else
                             (HUE_RED if S.hunger < 5 else (HUE_YELLOW if S.hunger < 10 else HUE_TEXT))):
                    Kit.ui_pos(ctl["food"], win["x1"] + win["row1"] - win["food_w"][n], ROW2_Y)
                set_tip("tip_food", food_tip(sat_label, sat_mod))
        def _thread_tick():
            if files["import"] and not win["closing"]:
                import_old_file()
                if not files["import"]: loop["slow_clock"] = 0.0
            if files["save"] and S.dirty: save_history()
            files["save"] = False
        def _interval(): return 0.025 if loop.get("fast") else 0.1
        def _thread_wanted(): return bool(files["save"] or files["import"])
        return part_dict(_start, _tick, _stop, config_height, build_config, poll_config, config_closed,
                         thread_tick=_thread_tick, thread_wanted=_thread_wanted, interval=_interval)
    def _part_bandage():
        BANDAGE_GRAPHIC = 0x0E21; BANDAGE_TIME    = 15.0; OTHER_TIME_DEF  = 7.5; TIME_BUFFER     = 0.5
        TIME_MIN, TIME_MAX = 1.0, 60.0; BUFFER_MIN, BUFFER_MAX = 0.0, 5.0; TARGET_TIMEOUT  = 3.0; OTHER_RANGE     = 1
        BAND_REFUSED_END = ("you did not stay close enough to heal", "you were unable to finish your work")
        BAND_REFUSED    = ("that being is not damaged", "you are too far away to do that",
                           "bandages can not be used on that", "you cannot heal that",
                           "bandages cannot be used on that", "that is too far away",
                           "that creature may only be healed") + BAND_REFUSED_END
        BAND_FINISHED   = ("you finish applying the bandages", "you apply the bandages, but they barely help",
                           "you apply the bandages, but they do not seem", "you heal what little damage",
                           "you are able to resurrect", "you are unable to resurrect",
                           "you have cured the target of all poisons")
        DEFAULT_START_PCT = 50; PCT_MIN, PCT_MAX  = 0, 99; BAR_WIN_X, BAR_WIN_Y = 400, 300; CURE_HEALING    = 60.0
        CURE_ANATOMY    = 60.0; COUNT_AFTER_USE = 0.6; DEFAULT_LOW     = 10; LOW_MIN, LOW_MAX = 0, 999
        ALERT_LOW       = "bandage.low"; ALERT_HP        = "bandage.hp"; ALERT_POISON    = "bandage.poison"
        ALERT_READY     = "bandage.ready"; OTHER_NAME_CHARS = 10; KEY             = "bandage"
        TITLE           = "Bandages"; PERSIST_KEY     = "BandageAgentStartPct"; TIMING_KEY      = "BandageAgent_timing"
        POS_KEY         = "BandageAgent_pos"; EXTRA_KEY       = "BandageAgent_extra"
        OTHER_KEY       = "BandageAgent_other"; TICK_COLOR      = "#E8C25A"; WIN_H = 62; ROW1_Y, ROW2_Y = 16, 35
        ICON = 18; ICON_GAP = 8; CFG_H1, CFG_H2, CFG_H3 = 120, 118, 104
        CFG_H = CFG_H1 + Kit.GAP + CFG_H2 + Kit.GAP + CFG_H3
        def st_reset():
            st.update({"phase": "idle", "shutting": False, "queue": [], "rebuild": False, "skills": (0.0, 0.0, -1e9),
                       "count": None, "count_at": 0.0, "low_armed": True, "hp_armed": True, "poison_armed": True,
                       "target": None, "last": None, "pick": False, "begun": False, "by_buff": False, "buff": False,
                       "lt": (0, 0.0)})
        st = {"start_pct": DEFAULT_START_PCT, "band_time": BANDAGE_TIME, "other_time": OTHER_TIME_DEF,
              "buffer": TIME_BUFFER, "t0": 0.0, "deadline": 0.0, "rd": None}
        st_reset()
        settings = {"cure": True, "low": DEFAULT_LOW, "others": False, "other_pct": 80, "party": True, "pets": True}
        win = {"g": None, "fill": None, "fill_box": None, "label": None,
               "bar_w": 109, "fill_w": -1, "text": None, "count": None, "count_text": None, "wide": False}
        cfg = {"f": None, "typed": None, "applied": None, "since": 0.0}; say = Kit.sayer(TITLE)
        def load_pct():
            try: st["start_pct"] = max(PCT_MIN, min(PCT_MAX, int(Kit.get_var(PERSIST_KEY, str(DEFAULT_START_PCT)))))
            except Exception: st["start_pct"] = DEFAULT_START_PCT
        def save_pct(): Kit.put_var(PERSIST_KEY, str(st["start_pct"]))
        def load_timing():
            p = Kit.get_var(TIMING_KEY).split("|")
            try:
                if p[0]: st["band_time"] = max(TIME_MIN, min(TIME_MAX, float(p[0])))
                if len(p) >= 2 and p[1]: st["buffer"] = max(BUFFER_MIN, min(BUFFER_MAX, float(p[1])))
            except ValueError: st["band_time"], st["buffer"] = BANDAGE_TIME, TIME_BUFFER
            try:
                v = Kit.get_var(OTHER_KEY)
                if v: st["other_time"] = max(TIME_MIN, min(TIME_MAX, float(v)))
            except ValueError: st["other_time"] = OTHER_TIME_DEF
        def save_timing():
            Kit.put_var(TIMING_KEY, "%.2f|%.2f" % (st["band_time"], st["buffer"]))
            Kit.put_var(OTHER_KEY, "%.2f" % st["other_time"])
        def load_extra():
            v = dict(part.split("=", 1) for part in Kit.get_var(EXTRA_KEY).split(";") if "=" in part)
            settings["cure"] = v.get("cure", "1") != "0"; settings["others"] = v.get("others", "0") == "1"
            settings["party"] = v.get("party") != "0"; settings["pets"] = v.get("pets") != "0"
            settings["low"] = _int_in(v.get("low"), LOW_MIN, LOW_MAX, DEFAULT_LOW)
            settings["other_pct"] = _int_in(v.get("opct"), 1, 99, 80)
        def _int_in(text, lo, hi, default):
            try: return max(lo, min(hi, int(text)))
            except (TypeError, ValueError): return default
        def save_extra():
            Kit.put_var(EXTRA_KEY, "cure=%d;low=%d;others=%d;opct=%d;party=%d;pets=%d" % (
                int(settings["cure"]), settings["low"], int(settings["others"]),
                settings["other_pct"], int(settings["party"]), int(settings["pets"])))
        def save_pos():
            if not pieces_on(KEY): Kit.save_pos(POS_KEY, win["g"])
        queue = Kit.queuer(st)
        def layout_size():
            bw = Kit.pic_size(Kit.LINE_RED)[0]; fw = Kit.pic_size(Kit.LINE_BLUE)[0]
            bar_w = bw if bw > 0 and fw > 0 else 109
            text_w = (max(Kit.text_w("15.0s"), readout_room()) + (90 if settings["others"] else 0))
            count_w = Kit.text_w("x999"); row1 = bar_w + 5 + text_w
            row2 = ICON + ICON_GAP + count_w + ICON_GAP + ICON + ICON_GAP + ICON; sec_w = max(row1, row2) + 6
            return {"bar_w": bar_w, "count_w": count_w, "row1": row1, "row2": row2, "sec_w": sec_w, "W": sec_w + 16}
        def build_window():
            L = layout_size(); WIN_W = L["W"]; bw = Kit.pic_size(Kit.LINE_RED)[0]; fw, fh = Kit.pic_size(Kit.LINE_BLUE)
            wide = settings["others"]; x, y = Kit.load_pos(POS_KEY, (BAR_WIN_X, BAR_WIN_Y), (WIN_W, WIN_H))
            old = win["g"]
            if Kit.is_open(old): x, y = old.GetX(), old.GetY()
            g = G.CreateGump(True, True); Kit.place(g, x, y, WIN_W, WIN_H)
            Kit.add_window_frame(g, WIN_W, WIN_H, corners=False)
            PIECES["bg"][g] = [Kit.add_section(g, 8, 8, L["sec_w"], WIN_H - 16)]
            g.SetTooltip("%s: one press, one bandage (x = bandages left)" % TITLE)
            x1 = 8 + (L["sec_w"] - L["row1"]) // 2; win["fill"] = win["fill_box"] = None; win["bar_w"] = L["bar_w"]
            if bw > 0 and fw > 0:
                Kit.add_pic(g, Kit.LINE_RED, x1, ROW1_Y)
                win["fill"] = Kit.add_tiled(g, Kit.LINE_BLUE, x1, ROW1_Y, 1, fh); win["fill"].SetWidth(0)
            else:
                Kit.add_tiled(g, Kit.SECTION_TILE, x1, ROW1_Y, 109, 9, 1.0); box = G.CreateGumpColorBox(1.0, "#3A63A8")
                box.SetRect(x1 + 1, ROW1_Y + 1, 1, 7); g.Add(box); win["fill_box"] = box
            tx = x1 + L["bar_w"] + 5; win["label"] = Kit.add_label(g, "Ready", tx, ROW1_Y - 2, Kit.HUE_INFO)
            Kit.catcher(g, x1 - 2, ROW1_Y - 4, L["row1"] + 4, 18, _bar_click,
                        "Bandage in progress and its patient. Alt+click: auto-follow (again to stop)", movable=True)
            x2 = 8 + (L["sec_w"] - L["row2"]) // 2; y2 = ROW2_Y
            pic = G.CreateGumpItemPic(BANDAGE_GRAPHIC, ICON, ICON); pic.SetPos(x2, y2); pic.SetAcceptMouseInput(False)
            g.Add(pic); Kit.catcher(g, x2, y2, ICON, ICON, queue("me"), "Use one bandage on yourself")
            xc = x2 + ICON + ICON_GAP; win["count"] = Kit.add_label(g, "", xc, y2 + 1, Kit.HUE_INFO)
            Kit.catcher(g, xc, y2, L["count_w"], ICON, lambda *a: None, "Bandages left in your backpack", movable=True)
            xt = xc + L["count_w"] + ICON_GAP; _reticle(g, xt, y2)
            Kit.catcher(g, xt, y2, ICON, ICON, _other_click, "Target someone within %d tile%s for one bandage. "
                        "Alt+click: auto-follow (again to stop)" % (OTHER_RANGE, "" if OTHER_RANGE == 1 else "s"))
            xr = xt + ICON + ICON_GAP; _repeat(g, xr, y2)
            Kit.catcher(g, xr, y2, ICON, ICON, _again_click,
                        "One more bandage on your last patient. Alt+click: auto-follow (again to stop)")
            win.update({"fill_w": -1, "text": None, "count_text": None, "wide": wide, "g": g})
            G.AddControlOnDisposed(g, _closed(g)); G.AddGump(g); Kit.on_moved(g, save_pos); Kit.dispose(old)
            show_count()
        def _ring(g, x, y, art, ch):
            p = Kit.add_pic(g, art, x, y, hue=53, mouse=False)
            if p is None: Kit.add_label(g, ch, x + 5, y + 1, Kit.HUE_TEXT); return False
            p.SetWidth(ICON); p.SetHeight(ICON); return True
        def _repeat(g, x, y):
            if not _ring(g, x, y, 8012, "@"): return
            Kit.add_box(g, x + 8, y, 10, 7, 1.0, "#101010")
            for r in range(7): Kit.add_box(g, x + 9, y + r, (3 - abs(r - 3)) * 2 + 1, 1, 1.0, TICK_COLOR)
        def _reticle(g, x, y):
            if not _ring(g, x, y, 8012, "+"): return
            c = ICON // 2
            for bx, by, bw, bh in ((c - 1, 0, 2, 5), (c - 1, ICON - 5, 2, 5), (0, c - 1, 5, 2), (ICON - 5, c - 1, 5, 2),
                                   (c - 1, c - 1, 2, 2)):
                Kit.add_box(g, x + bx, y + by, bw, bh, 1.0, TICK_COLOR)
        def _alt(o):
            alt = Follow.alt_held()
            if alt and o is not None: queue(("follow", o["serial"]))()
            return alt
        def _other_click(*args):
            if not _alt(st["last"]): queue("other")()
        def _bar_click(*args): _alt(st["target"] or st["last"])
        def _again_click(*args):
            if not _alt(st["last"]): queue("again")()
        def _closed(g):
            def handler(*args):
                if win["g"] is g and not st["shutting"]: save_pos(); win["g"] = None; HOST.disable(KEY)
            return handler
        def show_count():
            lbl = win["count"]; n = st["count"]
            if lbl is None: return
            if n is None: key = ("", Kit.HUE_INFO)
            else: low = settings["low"]; key = ("x%d" % n, Kit.HUE_BAD if low > 0 and n < low else Kit.HUE_INFO)
            if key != win["count_text"]: win["count_text"] = key; Kit.set_text(lbl, key[0], key[1])
        def set_bar(fraction, text, hue=None):
            fraction = max(0.0, min(1.0, fraction)); w = int(win["bar_w"] * fraction); old_w = win["fill_w"]
            if w != old_w:
                win["fill_w"] = w; fill = win["fill"]
                if fill is not None:
                    Kit.ui_w(fill, w)
                    if (w > 0) != (old_w > 0) or old_w < 0: fill.IsVisible = w > 0
                elif win["fill_box"] is not None: Kit.ui_w(win["fill_box"], max(1, w - 2))
            lbl = win["label"]
            if lbl is not None and (text, hue) != win["text"]:
                win["text"] = (text, hue); Kit.set_text(lbl, text, Kit.HUE_INFO if hue is None else hue)
        def alert(kind, text, level="warn"): HOST.alert(kind, text, level)
        def can_cure():
            heal, anat, at = st["skills"]; now = time.time()
            if now - at >= 5.0:
                heal, anat = skill_value("Healing"), skill_value("Anatomy"); st["skills"] = (heal, anat, now)
            return heal >= CURE_HEALING and anat >= CURE_ANATOMY
        def watch_alerts(p, hits, hmax):
            pct = st["start_pct"]
            if pct > 0 and hmax > 0:
                if hits * 100.0 / hmax <= pct:
                    if st["hp_armed"]:
                        st["hp_armed"] = False
                        alert(ALERT_HP, "Your HP is at %d%%: bandage?" % int(hits * 100.0 / hmax))
                else: st["hp_armed"] = True
            if settings["cure"]:
                if p.IsPoisoned:
                    if st["poison_armed"] and can_cure():
                        st["poison_armed"] = False; alert(ALERT_POISON, "Poisoned: a bandage can cure it")
                else: st["poison_armed"] = True
        def count_tick(now):
            if now < st["count_at"]: return
            st["count_at"] = now + 2.0; n = 0
            for it in API.FindTypeAll(BANDAGE_GRAPHIC, API.Backpack) or (): n += int(it.Amount or 1)
            prev, st["count"] = st["count"], n; low = settings["low"]
            if low > 0 and n < low:
                if st["low_armed"] and (n > 0 or (prev or 0) > 0):
                    st["low_armed"] = False
                    alert(ALERT_LOW, "No bandages left" if n <= 0 else "Only %s left" % Kit.count(n, "bandage"))
            else: st["low_armed"] = True
            show_count()
        def near(m, px, py, reach): return max(abs(int(m.X) - px), abs(int(m.Y) - py)) <= reach
        def describe(m):
            name = str(m.Name or "") or "them"
            short = name if len(name) <= OTHER_NAME_CHARS else name[:OTHER_NAME_CHARS - 1] + "."
            return {"serial": int(m.Serial), "name": name, "short": short}
        def start_bandage(p, now, target):
            if st["phase"] != "idle": say("a bandage is already running."); return
            if API.HasTarget("any") or HOST.cursor_busy(KEY):
                say("a target cursor is up (aim it or press Esc first)."); return
            if p.IsDead: return
            bandage = API.FindType(BANDAGE_GRAPHIC, API.Backpack)
            if not bandage: set_bar(0.0, "Out!", Kit.HUE_BAD); say("out of bandages!", Kit.HUE_BAD); return
            st["rd"].new(); API.UseObject(bandage.Serial); st["count_at"] = min(st["count_at"], now + COUNT_AFTER_USE)
            HOST.claim_cursor(KEY, TARGET_TIMEOUT); st["target"] = target; st["begun"], st["by_buff"] = False, False
            st["phase"], st["deadline"] = "cursor", now + TARGET_TIMEOUT
        def picked(serial):
            st["pick"] = False
            if serial: queue(("on", int(serial)))()
        def bandage_other(p, now, serial):
            m = API.FindMobile(serial)
            if m is None: say("can't see them.", Kit.HUE_BAD); return
            if int(p.Serial) == int(m.Serial): start_bandage(p, now, None); return
            if m.IsDead: say("they are dead.", Kit.HUE_BAD); return
            if not near(m, int(p.X), int(p.Y), OTHER_RANGE):
                say("too far away (%s at most)." % Kit.count(OTHER_RANGE, "tile"), Kit.HUE_BAD); return
            start_bandage(p, now, describe(m))
        def watch_last_target(now):
            serial = int(API.LastTargetSerial)
            if serial != st["lt"][0]: st["lt"] = (serial, now)
        def guess_patient(p, now):
            serial, when = st["lt"]
            if not serial: return None
            try:
                if serial == int(p.Serial): return None
                m = API.FindMobile(serial)
                if m is None or not near(m, int(p.X), int(p.Y), OTHER_RANGE + 1): return None
                if now - when <= 4.0 or (p.Hits >= p.HitsMax and not p.IsPoisoned): return describe(m)
            except Exception: pass
            return None
        def band_begun(p, now, at, buff=False):
            mine = st["phase"] == "heal" and not st["begun"] and not st["by_buff"]
            if st["phase"] == "cursor": HOST.release_cursor(KEY)
            if buff and st["phase"] == "heal": return
            if not mine: st["target"] = guess_patient(p, now)
            st["t0"] = min(now, at); st["phase"], st["begun"], st["by_buff"] = "heal", not buff, buff
            st["count_at"] = min(st["count_at"], now + COUNT_AFTER_USE)
        def watch_buff(p, now):
            up = bool(API.BuffExists("Healing")); was, st["buff"] = st["buff"], up
            if up and not was: band_begun(p, now, now, True)
            elif was and not up and st["phase"] == "heal" and st["by_buff"]: return "done"
            return None
        def band_answer(p, now):
            lines = st["rd"].new()
            if not lines: return None
            own = TITLE.lower() + ":"
            for ln in lines:
                low = ln.low.strip()
                if low.startswith(own): continue
                if ln.name and str(ln.name).lower() != "system": continue
                if low.startswith("you begin applying the bandages"): band_begun(p, now, ln.at); continue
                if st["phase"] == "idle": continue
                fresh = st["phase"] == "cursor" or (not st["begun"] and now - st["t0"] <= 2.0)
                for x in BAND_REFUSED:
                    if low.startswith(x) and (fresh or x in BAND_REFUSED_END): return low.rstrip(".!")
                if st["phase"] == "heal" and low.startswith(BAND_FINISHED): return "done"
            return None
        def aim_other(p, o):
            try:
                m = API.FindMobile(o["serial"])
                ok = m is not None and not m.IsDead and near(m, int(p.X), int(p.Y), OTHER_RANGE)
            except Exception: ok = False
            if not ok:
                API.CancelTarget(); say("%s is out of reach; cursor put down." % o["name"], Kit.HUE_BAD); return False
            API.Target(o["serial"]); st["last"] = o; say("bandaging %s." % o["name"])
            return True
        def _queued(p, now):
            if st["rebuild"]:
                st["rebuild"] = False
                if win["g"] is not None and win["wide"] != settings["others"]: build_window()
            while st["queue"]:
                action = st["queue"].pop(0); kind = action[0] if isinstance(action, tuple) else action
                if kind == "follow": Follow.toggle(action[1], TITLE)
                elif action == "me": start_bandage(p, now, None)
                elif action == "other":
                    if not st["pick"] and st["phase"] == "idle": st["pick"] = True; HOST.pick_target(15.0, picked, KEY)
                elif action == "again":
                    if st["last"] is None: say("nobody bandaged yet; use the target icon first.")
                    else: bandage_other(p, now, st["last"]["serial"])
                elif kind == "on": bandage_other(p, now, action[1])
        def num_text(v): return ("%.2f" % v).rstrip("0").rstrip(".")
        def build_config(g, x, y, w):
            labels = ("On yourself:", "On someone else:", "Latency buffer:"); field = {"stay": True, "tw": 50}
            unit = ("note", "s", {"dx": 82 + max(Kit.text_w(t) for t in labels), "ndy": 4, "h": 28})
            help_text = ("Bandage: one on you. Target icon: one on whoever you click (within %d tile%s). "
                         "Arrow: one more on the last one." % (OTHER_RANGE, "" if OTHER_RANGE == 1 else "s"))
            limits = (int(TIME_MIN), int(TIME_MAX))
            page = (("BANDAGE TIMES", (
                        ("text", "time", labels[0], "Seconds one on yourself takes; applied when you stop typing "
                         "(%d-%d)" % limits, field), unit,
                        ("text", "other", labels[1], "Seconds one on someone else takes, much faster on this shard "
                         "(%d-%d)" % limits, field), unit,
                        ("text", "buffer", labels[2], "Seconds added for latency before the bar says Done (%d-%d)"
                         % (int(BUFFER_MIN), int(BUFFER_MAX)), field), unit), {"sh": CFG_H1, "align": True}),
                    ("ALERTS  (sound: Settings > Alerts)", (
                        ("num", "box", "Alert when your HP is at or under:", "One alert per fall to this % or below "
                         "(0-99, 0 = never)", "%", PCT_MIN, PCT_MAX, {"clamp": False}),
                        ("check", "cure", "Alert when poisoned and a bandage can cure it", "Once per poisoning, with "
                         "Healing %d and Anatomy %d or more" % (int(CURE_HEALING), int(CURE_ANATOMY))),
                        ("num", "low", "Alert when bandages drop under:", "One alert when your bandages drop under "
                         "this (%d-%d, 0 = never)" % (LOW_MIN, LOW_MAX), None, LOW_MIN, LOW_MAX, {"clamp": False})),
                     {"sh": CFG_H2}),
                    ("WINDOW", [("check", "others", "Show who the bandage is on (a wider bar)", "The bar names your "
                                 "patient. Alt+click the name: auto-follow (again to stop)")] +
                     [("note", line, {"ndy": 2}) for line in Kit.wrap(help_text, w - 24)[:2]], {"sh": CFG_H3}))
            vals = dict(settings, time=num_text(st["band_time"]), other=num_text(st["other_time"]),
                        buffer=num_text(st["buffer"]), box=st["start_pct"])
            cfg.update({"f": Kit.Form(g, x, y, w, vals, page, ldy=4, lgap=12, fw=40), "typed": None, "applied": None})
        def config_closed(): cfg.update({"f": None, "typed": None, "applied": None})
        def parse_time(text, lo, hi):
            try: v = float(str(text).strip().replace(",", "."))
            except (ValueError, TypeError): return None
            return v if lo <= v <= hi else None
        def poll_config():
            f = cfg["f"]
            if f is None: return
            try: new = f.read(True)
            except Exception: config_closed(); return
            f.vals = new
            if new["box"] != st["start_pct"]: st["start_pct"] = new["box"]; st["hp_armed"] = True; save_pct()
            if new["low"] != settings["low"]: st["count_at"] = 0.0
            changed = False
            for k, flag in (("cure", "poison_armed"), ("others", "rebuild"), ("low", "low_armed")):
                if new[k] != settings[k]: settings[k] = new[k]; st[flag] = True; changed = True
            if changed: save_extra()
            now = time.time(); typed = (new["time"], new["other"], new["buffer"])
            if typed != cfg["typed"]: cfg["typed"], cfg["since"] = typed, now; return
            if cfg["applied"] == typed or now - cfg["since"] < 0.7: return
            cfg["applied"] = typed; changed = False
            for i, (k, lo, hi) in enumerate((("band_time", TIME_MIN, TIME_MAX), ("other_time", TIME_MIN, TIME_MAX),
                                             ("buffer", BUFFER_MIN, BUFFER_MAX))):
                v = parse_time(typed[i], lo, hi)
                if v is not None and abs(v - st[k]) > 0.001: st[k], changed = v, True
            if changed: save_timing()
        def _start():
            st_reset(); st["rd"] = Journal.reader(); load_pct(); load_timing(); load_extra()
            for k, label, sound in ((ALERT_LOW, "Bandages running low", 0x1EA), (ALERT_HP, "HP low: bandage?", 0x1F1),
                                    (ALERT_POISON, "Poisoned (a bandage cures)", 0x1E0),
                                    (ALERT_READY, "Bandage done", 0x202)):
                HOST.alert_kind(k, label, sound)
            build_window(); pieces_add(KEY, "player", 0, lambda: win["g"])
            say("on (%s s on you, %s s on others)." % (num_text(st["band_time"]), num_text(st["other_time"])),
                Kit.HUE_GOOD)
        def _tick():
            p = API.Player
            if p is None: return
            now = time.time()
            if st["queue"] or st["rebuild"]:
                _queued(p, now)
                if win["g"] is None: return
            if p.IsDead:
                if st["phase"] != "idle": HOST.release_cursor(KEY)
                st["phase"], st["target"] = "idle", None; set_bar(0.0, "Dead", Kit.HUE_BAD); return
            count_tick(now); hits, hmax = p.Hits, p.HitsMax
            if hmax > 0: watch_alerts(p, hits, hmax)
            watch_last_target(now); answer = band_answer(p, now); buff_answer = watch_buff(p, now)
            if answer is None: answer = buff_answer
            if answer is not None and answer != "done" and st["phase"] != "idle":
                if st["phase"] == "cursor": HOST.release_cursor(KEY)
                st["phase"], st["target"] = "idle", None; set_bar(0.0, "Ready")
                say("the bandage failed (%s)." % answer, Kit.HUE_BAD); return
            if st["phase"] == "heal":
                o = st["target"]; band_time = st["other_time"] if o is not None else st["band_time"]
                elapsed = now - st["t0"]
                if elapsed >= band_time + st["buffer"] or answer == "done":
                    st["phase"], st["target"] = "idle", None; set_bar(1.0, "Done", Kit.HUE_GOOD)
                    alert(ALERT_READY, "Bandage done", "info")
                else:
                    left = "%.1fs" % max(0.0, band_time - elapsed)
                    if o is not None and win["wide"]: left = "%s %s" % (o["short"], left)
                    set_bar(elapsed / band_time, left, Kit.HUE_TEXT)
                return
            if st["phase"] == "cursor":
                if HOST.cursor_ok(KEY, "beneficial"):
                    o = st["target"]
                    if o is None: API.TargetSelf(); aimed = True
                    else: aimed = aim_other(p, o)
                    HOST.release_cursor(KEY)
                    if aimed: st["phase"], st["t0"] = "heal", now
                    else: st["phase"], st["target"] = "idle", None
                elif now > st["deadline"]:
                    if API.HasTarget("beneficial"): say("a bandage cursor is up: press Esc or aim it.")
                    else: say("no bandage cursor appeared.", Kit.HUE_BAD)
                    HOST.release_cursor(KEY); st["phase"], st["target"] = "idle", None
                return
            t = win["text"]
            if t is None or t[0] not in ("Ready", "Done", "Out!") or (t[0] == "Out!" and (st["count"] or 0) > 0):
                set_bar(0.0, "Ready")
        def _stop():
            st["shutting"] = True; HOST.release_cursor(KEY); save_pos(); pieces_remove(KEY); save_pct()
            save_timing(); g, win["g"] = win["g"], None; win["label"] = win["count"] = None; Kit.dispose(g)
        def _interval():
            if st["phase"] == "cursor": return 0.01
            if st["phase"] != "heal": return 0.1
            band_time = st["other_time"] if st["target"] is not None else st["band_time"]
            return min(0.1, max(0.01, st["t0"] + band_time + st["buffer"] - time.time()))
        load_pct(); load_timing(); load_extra()
        return part_dict(_start, _tick, _stop, lambda w: CFG_H, build_config, poll_config, config_closed,
                         interval=_interval)
    def _part_pets():
        KEY = "pets"; TITLE = "Pets"; SETTINGS_KEY = "Pets_settings"; POS_KEY = "Pets_pos"; MIN_KEY = "Pets_min"
        W = 440; MINI_W, MINI_H = 280, 46; SCAN_EVERY = 0.25; FULL_EVERY = 1.0; not_pet = {}; LOOK_EVERY = 1.0
        RANGE_DEFAULT, RANGE_MIN, RANGE_MAX = 18, 2, 24; MAX_ROWS = 6; ROW_H = 50; NAME_W = 130; BAR_W = 110
        MAX_KNOWN = 20; BANDAGE_RANGE = 1; SPELL_RANGE = 10; CURSOR_WAIT = 3.0
        HEAL_FAILED = ("the spell fizzles", "your concentration is disturbed",
                       "insufficient mana", "more reagents are needed", "you must wait to perform another action")
        CONFIRM_SECS = 3.0
        ALL_CMDS = (("follow", "Follow me", "all follow me"), ("guard", "Guard me", "all guard me"),
                    ("stay", "Stay", "all stay"), ("come", "Come", "all come"))
        ALL_KILL = "all kill"; ALL_SAY = dict((a, t) for a, _, t in ALL_CMDS)
        PET_CMDS = (("pet_follow", "Follow", "%s follow me"), ("pet_guard", "Guard", "%s guard"),
                    ("pet_stay", "Stay", "%s stay"))
        PET_SAY = dict([(k, t) for k, _, t in PET_CMDS] + [("pet_kill", "%s kill")])
        HEAL_WAYS = (("", "Bandage"), ("Heal", "Heal (spell)"), ("Greater Heal", "Greater Heal (spell)"))
        LOW_ALERT, DEAD_ALERT = "pets.low", "pets.dead"; BAR_BG = "#17171a"
        BAR_HITS, BAR_POISON, BAR_STAM = "#c22d2d", "#2f9a3c", "#d39a1c"
        KILL_TIP = "then pick the enemy with the shard's cursor (only on a click)"
        settings = {"range": RANGE_DEFAULT, "low": 30, "heal": 0, "kill": False, "hidden": True}
        def st_reset():
            st.update({"shutting": False, "docked": False, "queue": [], "heal": None, "confirm": None, "scan_at": 0.0,
                       "look_at": 0.0, "note": "", "full_at": 0.0, "note_until": 0.0, "order": []})
        st = {"minimized": False, "followers": 0, "fmax": 0, "me": 0, "note_hue": Kit.HUE_INFO, "cmd_at": {}, "seq": 0}
        st_reset(); win = {"g": None, "c": {}, "store": ({}, {}), "rows": [], "n_rows": -1}; cleanup = Kit.Cleanup()
        pets = {}; NUMS = {"range": (RANGE_MIN, RANGE_MAX), "low": (0, 99), "heal": (0, len(HEAL_WAYS) - 1)}
        def load_settings(): Kit.kv_load(SETTINGS_KEY, ";", settings, NUMS)
        def save_settings(): Kit.kv_save(SETTINGS_KEY, ";", settings, ("range", "low", "heal", "kill", "hidden"), NUMS)
        def note(text, hue=None, secs=4.0):
            st["note"], st["note_hue"] = text, Kit.HUE_INFO if hue is None else hue
            st["note_until"] = time.time() + secs; show_note()
        def note_on(now): return bool(st["note"]) and 0 <= st["note_until"] - now <= 10.0
        def heal_way(): return HEAL_WAYS[settings["heal"]]
        def tiles(n): return Kit.count(n, "tile")
        def new_pet(serial, name, manual=False):
            st["seq"] += 1
            r = {"serial": serial, "name": name, "seq": st["seq"], "seen": 0.0, "where": "gone",
                 "pct": None, "stam": None, "dist": 0, "dir": "", "dead": False, "poison": False,
                 "low": False, "manual": manual, "alive": False}
            pets[serial] = r; st["order"] = []; return r
        def forget(serial):
            if pets.pop(serial, None) is not None: st["order"] = []
        def update(r, m, px, py, now, near):
            if r["manual"] and r.get("own"): r["own"] = bool(m.IsRenamable)
            name = str(m.Name or "")
            if name: r["name"] = name
            hits, hmax, sta, smax = int(m.Hits or 0), int(m.HitsMax or 0), int(m.Stamina or 0), int(m.StaminaMax or 0)
            r["pct"] = max(0, min(100, int(hits * 100 // hmax))) if hmax > 0 else None
            r["stam"] = max(0, min(100, int(sta * 100 // smax))) if smax > 0 else None
            dead = bool(m.IsDead); r["poison"] = bool(m.IsPoisoned); ox, oy = int(m.X), int(m.Y)
            r["dist"] = max(abs(ox - px), abs(oy - py)); r["dir"] = Kit.compass(ox - px, oy - py) or "here"
            r["where"] = "near" if near else "far"; r["seen"] = now
            if dead and not r["dead"] and r["alive"]: alert(DEAD_ALERT, "%s died" % (r["name"] or "A pet"), r["serial"])
            r["dead"] = dead
            if dead: r["low"] = True; return
            r["alive"] = True; low = settings["low"]; pct = r["pct"]
            if pct is not None:
                if low > 0 and pct <= low and not r["low"]:
                    r["low"] = True
                    alert(LOW_ALERT, "%s at %d%% HP (%s)" % (r["name"] or "A pet", pct, "here" if r["dist"] == 0 else
                          "%s %s" % (tiles(r["dist"]), r["dir"])), r["serial"])
                elif r["low"] and (low <= 0 or pct >= low + 10): r["low"] = False
        def alert(key, text, serial): HOST.alert(key, text, "warn", who=serial)
        def scan(p, now):
            me = int(p.Serial); px, py = int(p.X), int(p.Y); st["me"] = me; was = st["followers"]
            st["followers"], st["fmax"] = int(p.Followers or 0), int(p.FollowersMax or 0)
            seen = set(); lost = False; rng = settings["range"]
            full = now >= st["full_at"] or st["full_at"] - now > FULL_EVERY or st["followers"] != was
            if not full:
                near = [k for k, r in pets.items() if r["where"] == "near"]
                if len(near) < st["followers"]: full = True
            if not full:
                found = []
                for k in near:
                    try:
                        m = HOST.mobile(k)
                        if m is None or int(m.Distance) > rng: full = True; break
                    except Exception: full = True; break
                    found.append((k, m))
                if not full:
                    for k, m in found:
                        try:
                            r = pets.get(k)
                            if r is None: continue
                            if not r["manual"] and not m.IsRenamable: forget(k); continue
                            seen.add(k); update(r, m, px, py, now, True)
                        except Exception: continue
                    mobs = ()
            if full:
                st["full_at"] = now + FULL_EVERY; mobs = HOST.mobiles(rng) or []
                if len(not_pet) > 400: not_pet.clear()
            for m in mobs:
                try:
                    if m is None: continue
                    s = int(m.Serial)
                    if s == me: continue
                    r = pets.get(s)
                    if r is None:
                        u = not_pet.get(s)
                        if u is not None and now < u: continue
                        if not m.IsRenamable: not_pet[s] = now + 2.5; continue
                        not_pet.pop(s, None)
                        if len(pets) >= MAX_KNOWN:
                            prune(now, room=1)
                            if len(pets) >= MAX_KNOWN: continue
                        r = new_pet(s, "")
                    elif not r["manual"] and not m.IsRenamable: forget(s); continue
                    seen.add(s); update(r, m, px, py, now, True)
                except Exception: continue
            for s, r in pets.items():
                if s not in seen and r["where"] == "near": lost = True; r["where"] = "far"
            if lost or now >= st["look_at"] or st["look_at"] - now > LOOK_EVERY:
                st["look_at"] = now + LOOK_EVERY
                for s in [s for s in pets if s not in seen]:
                    r = pets[s]; m = HOST.mobile(s)
                    if m is None: r["where"] = "gone"; continue
                    try:
                        if not r["manual"] and not m.IsRenamable: forget(s); continue
                        update(r, m, px, py, now, False)
                    except Exception: continue
            prune(now)
        def prune(now, room=0):
            gone = [r for r in pets.values() if r["where"] == "gone"]
            if not gone: return
            for r in gone:
                if now - r["seen"] > 1800.0: forget(r["serial"])
            keep = MAX_KNOWN - room
            if st["fmax"] > 0:
                in_view = len(pets) - len([r for r in pets.values() if r["where"] == "gone"])
                keep = min(keep, max(st["followers"], in_view))
            if len(pets) > keep:
                gone = sorted([r for r in pets.values() if r["where"] == "gone"], key=lambda r: r["seen"])
                while gone and len(pets) > keep: forget(gone.pop(0)["serial"])
        def ordered():
            if not st["order"] or len(st["order"]) != len(pets):
                st["order"] = sorted(pets.values(), key=lambda r: r["seq"])
            return st["order"]
        queue = Kit.queuer(st)
        def flow(g, store, items, x0, y0, xmax):
            x, y, lines = x0, y0, 1
            for key, art, caption, tip, fn, hue in items:
                bw = 35 + Kit.text_w(caption)
                if x > x0 and x + bw > xmax: x, y, lines = x0, y + 26, lines + 1
                if g is not None: Kit.art_button(g, store, key, art, x, y, caption, tip, hue=hue, on_click=fn)
                x += bw + 12
            return lines
        def all_items():
            items = [("all_" + k, Kit.ART_CLOSE if k == "stay" else Kit.ART_PLAY, caption,
                      "Say \"%s\" (all your pets in earshot)" % text, queue(("all", k)), None)
                     for k, caption, text in ALL_CMDS]
            if settings["kill"]:
                items.append(("all_kill", Kit.ART_PLAY, "Kill", "Say \"%s\", %s" % (ALL_KILL, KILL_TIP),
                              queue(("all", "kill")), Kit.HUE_BAD))
            return items
        def build_window():
            M = Kit.MARGIN; IW = W - 2 * M; n_rows = min(MAX_ROWS, len(pets)); items = all_items()
            lines = flow(None, None, items, M + 10, 0, M + IW - 10); all_h = 30 + lines * 26 + 22
            pets_h = 30 + max(1, n_rows) * ROW_H + 2
            g, store, c = wnd.begin(W, M + 30 + Kit.GAP + all_h + Kit.GAP + pets_h + M); rows = []
            if not st["minimized"]:
                wnd.frame(g); ya = M + 30 + Kit.GAP
                Kit.add_section(g, M, ya, IW, all_h, "ALL PETS  (said out loud)")
                flow(g, store, items, M + 10, ya + 26, M + IW - 10)
                c["note"] = Kit.add_label(g, "", M + 12, ya + 30 + lines * 26 - 2, Kit.HUE_INFO)
                yp = ya + all_h + Kit.GAP; ptitle = "YOUR PETS  (click to target)"
                Kit.add_section(g, M, yp, IW, pets_h, ptitle); c["title_end"] = M + 8 + Kit.text_w(ptitle)
                x_add = M + IW - 10 - 35 - Kit.text_w("Add...")
                Kit.art_button(g, store, "add", Kit.ART_PLAY, x_add, yp + 3, "Add...",
                               "List a pet of yours that isn't shown (this session)", on_click=queue("add"))
                c["count"] = Kit.add_label(g, "", x_add - 60, yp + 6, Kit.HUE_INFO); c["count_right"] = x_add - 10
                x_bar = M + 12 + NAME_W + 8; x_info = x_bar + BAR_W + 10; way = heal_way()
                buttons = [(k, art, cap, "Say \"%s\"" % (PET_SAY[k] % "<name>")) for (k, cap, _), art in
                           zip(PET_CMDS, (Kit.ART_PLAY, Kit.ART_PLAY, Kit.ART_CLOSE))]
                buttons.append(("heal", Kit.ART_PLAY, "Heal",
                                "Use one bandage on this pet (within %s)" % tiles(BANDAGE_RANGE) if not way[0] else
                                "Cast %s on this pet (within %d tiles)" % (way[0], SPELL_RANGE)))
                if settings["kill"]:
                    buttons.append(("pet_kill", Kit.ART_PLAY, "Kill", "Say \"<name> kill\", " + KILL_TIP))
                for i in range(n_rows):
                    ry = yp + 30 + i * ROW_H
                    row = {"val": None, "prev": None, "changed": 0.0,
                           "vis_hits": False, "vis_poison": False, "stam_on": False}
                    row["name_lbl"] = Kit.add_label(g, "", M + 12, ry + 3, Kit.HUE_TEXT); bars = {}
                    for v, col, bh, by in (("hits", BAR_HITS, 9, 6), ("poison", BAR_POISON, 9, 6),
                                           ("stam", BAR_STAM, 3, 16)):
                        pb = G.CreateGumpSimpleProgressBar(BAR_W, bh, BAR_BG, col, 0, 100); pb.SetPos(x_bar, ry + by)
                        pb.SetAcceptMouseInput(False); g.Add(pb); pb.IsVisible = False; bars[v] = pb
                    row["bars"], row["stam_bar"] = bars, bars.pop("stam")
                    row["info"] = Kit.add_label(g, "", x_info, ry + 3, Kit.HUE_INFO)
                    Kit.catcher(g, M + 10, ry, IW - 20, 22, Kit.row_clicker(row, queue, "target"),
                                "Click: aim your cursor at this pet, or make it your last target. "
                                "Alt+click: auto-follow (again to stop)")
                    xb = M + 10
                    for kind, art, cap, tip in buttons:
                        Kit.art_button(g, store, "%s%d" % (kind, i), art, xb, ry + 24, cap,
                                       tip + ". Alt+click: auto-follow (again to stop)",
                                       hue=Kit.HUE_BAD if kind == "pet_kill" else None,
                                       on_click=Kit.row_clicker(row, queue, kind))
                        xb += 35 + Kit.text_w(cap) + 12
                    rows.append(row)
                c["empty"] = (Kit.add_label(g, "", M + 12, yp + 33, Kit.HUE_INFO) if not n_rows else None)
            wnd.end(g, {"rows": rows, "n_rows": n_rows, "count_w": None}); draw(time.time())
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, mini=(MINI_W, MINI_H), icon=0x0E81,
                         cleanup=cleanup, lock=False, clear={"rows": [], "c": {}, "n_rows": -1})
        def set_vis(row, key, ctrl, on):
            if row.get(key) != on: row[key] = on; ctrl.IsVisible = on
        def set_progress(row, key, ctrl, v):
            if row.get(key) != v: row[key] = v; ctrl.SetProgress(float(v), 100.0)
        def status_text():
            if note_on(time.time()): return st["note"], st["note_hue"]
            low = [r for r in pets.values() if r["low"] and not r["dead"] and r["where"] != "gone"
                   and r["pct"] is not None]
            if low:
                r = min(low, key=lambda r: r["pct"])
                return "%s: %s %d%% HP" % (TITLE, Kit.fit(r["name"] or "pet", 80), r["pct"]), Kit.HUE_BAD
            near = len([r for r in pets.values() if r["where"] != "gone"])
            if not pets: return "%s: none in view" % TITLE, Kit.HUE_INFO
            return "%s: %s, %d in view" % (TITLE, Kit.count(len(pets), "pet"), near), Kit.HUE_INFO
        def show_note():
            c = win["c"]
            if win["g"] is None or st["docked"]: return
            if st["minimized"]:
                lbl = c.get("status")
                if lbl is not None: t, hue = status_text(); Kit.set_text(lbl, Kit.fit(t, MINI_W - 90), hue)
                return
            lbl = c.get("note")
            if lbl is not None:
                on = note_on(time.time())
                Kit.set_text(lbl, Kit.fit(st["note"], W - 2 * Kit.MARGIN - 24) if on else "", st["note_hue"])
        def draw(now):
            if win["g"] is None or st["shutting"] or st["docked"]: return
            if st["minimized"]: show_note(); return
            order = ordered()
            if min(MAX_ROWS, len(order)) != win["n_rows"]: build_window(); return
            c = win["c"]
            for row, r in zip(win["rows"], order):
                Kit.row_set(row, (r["serial"],), now); where, pct = r["where"], r["pct"]
                if r["dead"] or where == "gone": hue = Kit.HUE_INFO
                elif r["low"]: hue = Kit.HUE_BAD
                elif r["poison"]: hue = Kit.HUE_GOOD
                else: hue = Kit.HUE_TEXT
                Kit.set_text(row["name_lbl"], Kit.fit(r["name"] or "(no name yet)", NAME_W), hue); bar = None
                if where == "near" and not r["dead"]:
                    bar = "poison" if r["poison"] else "hits"
                    info = "%s  %s" % ("%d%%" % pct if pct is not None else "?%", "here" if r["dist"] == 0 else "%d %s"
                                       % (r["dist"], r["dir"]))
                elif r["dead"] and where != "gone": info = "dead  %d %s" % (r["dist"], r["dir"])
                elif where == "far": info = "far: %d %s" % (r["dist"], r["dir"])
                else: info = ("out of range (%s)" % Kit.ago(now - r["seen"], Kit.AGO_SHORT) if r["seen"] else
                              "out of range")
                Kit.set_text(row["info"], info, Kit.HUE_TEXT if bar else Kit.HUE_INFO)
                for v, pb in row["bars"].items(): set_vis(row, "vis_" + v, pb, v == bar)
                if bar: set_progress(row, "p_" + bar, row["bars"][bar], pct if pct is not None else 0)
                stam = r["stam"] if bar else None; set_vis(row, "stam_on", row["stam_bar"], stam is not None)
                if stam is not None: set_progress(row, "p_stam", row["stam_bar"], stam)
            lbl = c.get("count")
            if lbl is not None:
                if st["fmax"] > 0: txt = "%d / %d slots" % (st["followers"], st["fmax"])
                else: txt = "%d known" % len(pets) if pets else ""
                if len(order) > MAX_ROWS:
                    more = "%d more  %s" % (len(order) - MAX_ROWS, txt)
                    if c["count_right"] - Kit.text_px(more) >= c["title_end"] + 8: txt = more
                Kit.set_text(lbl, txt); tw = Kit.text_px(txt) if txt else 0
                if win["count_w"] != tw: win["count_w"] = tw; Kit.ui_pos(lbl, c["count_right"] - tw, Kit.ui_y(lbl))
            empty = c.get("empty")
            if empty is not None:
                if st["followers"] > 0:
                    Kit.set_text(empty, "%s used, none in view. Add... lists one." % Kit.count(st["followers"], "slot"))
                else: Kit.set_text(empty, "No pets in view. Click Add... to list one.")
            show_note()
        def gate(action, p, now):
            if not settings["hidden"]: return True
            if not p.IsHidden: st["confirm"] = None; return True
            cf = st["confirm"]
            if cf is not None and cf[0] == action and cf[1] <= now <= cf[2]: st["confirm"] = None; return True
            st["confirm"] = (action, now + 0.3, now + CONFIRM_SECS)
            note("That reveals you: click again to do it.", Kit.HUE_TITLE, CONFIRM_SECS); return False
        def say(text, now):
            last = st["cmd_at"].get(text)
            if last is not None and 0 <= now - last < 0.6: return
            if len(st["cmd_at"]) > 50: st["cmd_at"].clear()
            st["cmd_at"][text] = now; API.Msg(text); note("Said \"%s\"." % text)
        def pet_name(serial):
            r = pets.get(serial)
            if r is None or not r["name"]: note("That pet has no name yet.", Kit.HUE_BAD); return None
            return r["name"]
        def do_target(serial):
            if API.HasTarget("any") and not HOST.cursor_busy(KEY):
                API.Target(serial)
                if st["heal"] is not None: st["heal"] = None; HOST.release_cursor(KEY)
                return
            API.SetLastTarget(serial=serial); API.HeadMsg("* last target *", serial, 0x35)
        def dist_to(m, p): return max(abs(int(m.X) - int(p.X)), abs(int(m.Y) - int(p.Y)))
        def start_heal(serial, p, now):
            r = pets.get(serial); name = (r and r["name"]) or "that pet"
            if st["heal"] is not None: note("A heal is already on its way.", Kit.HUE_TITLE); return
            if p.IsDead: note("You are dead.", Kit.HUE_BAD); return
            if API.HasTarget("any") or HOST.cursor_busy(KEY):
                note("A target cursor is up: aim it or press Esc first.", Kit.HUE_TITLE); return
            spell, label = heal_way(); reach = SPELL_RANGE if spell else BANDAGE_RANGE; m = API.FindMobile(serial)
            if m is None: note("%s is out of range." % name, Kit.HUE_BAD); return
            d = dist_to(m, p)
            if d > reach:
                note("%s is %d tiles away (%s reaches %d)." % (name, d, label.lower(), reach), Kit.HUE_BAD); return
            if not gate(("heal", serial), p, now): return
            if spell: API.CastSpell(spell); wait = Kit.spell_info(spell)[3] + CURSOR_WAIT
            else:
                b = API.FindType(0x0E21, API.Backpack)
                if not b:
                    note("Out of bandages.", Kit.HUE_BAD); API.SysMsg("%s: out of bandages!" % TITLE, Kit.HUE_BAD)
                    return
                API.UseObject(b.Serial); wait = CURSOR_WAIT
            HOST.claim_cursor(KEY, wait)
            st["heal"] = {"serial": serial, "name": name, "until": now + wait, "reach": reach,
                          "what": spell or "a bandage", "t0": now, "rd": Journal.reader()}
            note("%s for %s..." % (spell or "Bandage", name))
        def heal_tick(p, now):
            j = st["heal"]; failed = False; what = j["what"][0].upper() + j["what"][1:]
            for ln in j["rd"].new():
                for x in HEAL_FAILED:
                    if x in ln.low: failed = True; break
                if failed: break
            if failed:
                st["heal"] = None; HOST.release_cursor(KEY); note("%s for %s failed." % (what, j["name"]), Kit.HUE_BAD)
                return
            if HOST.cursor_claim[0] == KEY and HOST.cursor_ok(KEY, "beneficial"):
                m = API.FindMobile(j["serial"]); st["heal"] = None; HOST.release_cursor(KEY)
                if m is not None and dist_to(m, p) <= j["reach"]:
                    API.Target(j["serial"]); note("%s on %s." % (what, j["name"]), Kit.HUE_GOOD)
                else: API.CancelTarget(); note("%s moved out of reach." % j["name"], Kit.HUE_BAD)
                return
            if not 0 <= j["until"] - now <= CURSOR_WAIT + 10.0:
                st["heal"] = None; HOST.release_cursor(KEY)
                if API.HasTarget("any"): note("A target cursor is up: aim it or press Esc.", Kit.HUE_TITLE)
                else: note("No target cursor came for %s." % j["name"], Kit.HUE_BAD)
        def picked(serial): st["queue"].append(("added", int(serial or 0)))
        def add_pet(serial, p, now):
            if not serial: return
            if serial == st["me"] or serial == int(p.Serial): note("That's you.", Kit.HUE_BAD); return
            m = API.FindMobile(serial)
            if m is None: note("That isn't a creature in view.", Kit.HUE_BAD); return
            r = pets.get(serial)
            if r is None:
                if len(pets) >= MAX_KNOWN: prune(now, room=1)
                if len(pets) >= MAX_KNOWN: note("The list is full (%d)." % MAX_KNOWN, Kit.HUE_BAD); return
                r = new_pet(serial, "", manual=True)
            r["manual"] = True; r["own"] = bool(m.IsRenamable); update(r, m, int(p.X), int(p.Y), now, True)
            if r["dist"] > settings["range"]: r["where"] = "far"
            note("%s is listed for this session." % (r["name"] or "It"), Kit.HUE_GOOD)
        def handle(action, p, now):
            kind = action[0] if isinstance(action, tuple) else action
            if wnd.action(action): return
            if action == "add": HOST.pick_target(10.0, picked); note("Target the pet to list.")
            elif kind == "follow": Follow.toggle(action[1], TITLE)
            elif p is None: return
            elif kind == "added": add_pet(action[1], p, now)
            elif kind == "target": do_target(action[1])
            elif kind == "heal": start_heal(action[1], p, now)
            elif kind == "all" or kind in PET_SAY:
                if (action[1] == "kill" if kind == "all" else kind == "pet_kill") and not settings["kill"]: return
                if kind == "all": text = ALL_KILL if action[1] == "kill" else ALL_SAY.get(action[1])
                else: text = pet_name(action[1]); text = text and PET_SAY[kind] % text
                if text and not dead_now(p) and gate(action, p, now): say(text, now)
        def dead_now(p):
            if p.IsDead: note("You are dead: your pets can't hear you.", Kit.HUE_BAD); return True
            return False
        HEAL_INFO = ("One heal per click, aimed at the pet when its cursor comes (bandage within %s, spell within %d)."
                     % (tiles(BANDAGE_RANGE), SPELL_RANGE))
        KILL_INFO = "Said only on a click; the shard's cursor then picks the enemy."
        def page_table(w):
            heal, kill = ([("note", line) for line in Kit.wrap(t, w - 28)] for t in (HEAL_INFO, KILL_INFO))
            return (("WINDOW", (("num", "range", "List pets within:", "How far a pet is listed with its bars", "tiles",
                                 RANGE_MIN, RANGE_MAX),
                                ("check", "hidden", "While hidden, a command or a heal needs a second click",
                                 "Speaking and healing reveal you; the first click only asks"))),
                    ("HEAL BUTTON  (on each pet's row)",
                     [("note", "Heal with:", {"ndy": 4, "h": 28, "hue": Kit.HUE_TEXT})] + heal),
                    ("COMBAT COMMANDS", [("check", "kill", "Show Kill buttons (\"%s\" and \"<name> kill\")" % ALL_KILL,
                                          "One for all pets and one per pet row", {"h": 28})] + kill),
                    ("ALERTS  (sound: Settings > Alerts)", (("num", "low", "Alert when a pet's HP falls to:",
                        "One alert per fall to this % or below (0-99, 0 = never)", "%", 0, 99),)))
        def read_heal(f, new):
            try: i = int(f.c["heal"].GetSelectedIndex())
            except Exception: return
            if 0 <= i < len(HEAL_WAYS): new["heal"] = i
        def on_change(old, new):
            if new["hidden"] != old["hidden"]: st["confirm"] = None
            if (new["kill"], new["heal"]) != (old["kill"], old["heal"]) and win["g"] is not None: queue("redraw")()
        cfg = Kit.Page(settings, page_table, save_settings, on_change, {"ldy": 4, "lgap": 12, "fw": 44, "pad": 6},
                       strict=True, adjust=read_heal)
        def build_config(g, x, y, w):
            f = cfg.build(g, x, y, w); dd = G.CreateDropDown(200, [label for _, label in HEAL_WAYS], settings["heal"])
            dd.SetPos(x + 22 + Kit.text_w("Heal with:"), y + 90 + Kit.GAP + 30); g.Add(dd); f.c["heal"] = dd
            dd.SetTooltip("What each row's Heal button uses")
        def _start():
            st_reset(); st["minimized"] = wnd.start_min(); load_settings()
            for r in pets.values(): r["where"] = "gone" if r["where"] == "gone" else "far"
            HOST.alert_kind(LOW_ALERT, "Pet HP low", 0x335); HOST.alert_kind(DEAD_ALERT, "Pet died", 0x1F1)
            build_window(); wnd.dock(); cleanup.service("pets.list", svc_pets)
        def svc_pets(distance=None):
            if st["shutting"]: return None
            rng = settings["range"]
            if distance is None: distance = rng
            if distance > rng: return None
            return [k for k, r in pets.items() if r["where"] == "near" and (not r["manual"] or r.get("own"))
                    and r["dist"] <= distance]
        def _tick():
            if win["g"] is None: return
            if Kit.closed(win): return
            now = time.time(); p = API.Player
            while st["queue"]:
                handle(st["queue"].pop(0), p, now)
                if win["g"] is None: return
            if p is None: return
            if st["heal"] is not None: heal_tick(p, now)
            if now >= st["scan_at"] or st["scan_at"] - now > SCAN_EVERY:
                st["scan_at"] = now + SCAN_EVERY; scan(p, now); draw(now)
            elif st["note"] and not note_on(now): st["note"] = ""; show_note()
        def _stop():
            st["shutting"] = True; st["heal"] = None; HOST.release_cursor(KEY); save_settings(); cleanup.close()
        load_settings(); return part_dict(_start, _tick, _stop, cfg.height, build_config, cfg.poll, cfg.closed,
                                          interval=lambda: 0.02 if st["heal"] is not None else 0.1)
    PARTS = (("frames", _part_frames, 0.1, "unitframes"), ("timers", _part_timers, 0.1, "spelltimers"),
        ("swing", _part_swing, 0.025, "swing"), ("bandage", _part_bandage, 0.1, "bandage"),
        ("pets", _part_pets, 0.1, "pets"),)
    return PartSet(KEY, TITLE, PARTS).hooks()


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("hud", "Character HUD", "Frames, timers and bars for you and pets", _module_hud, 0.025,
         category="On screen", parts=(("frames", "Frames", "Health frames: you, target, party", True,
              ("unitframes",)), ("timers", "Buffs & Timers", "Timed buffs, debuffs and your spells", True,
              ("spelltimers",)), ("swing", "Swing Bar", "When your next melee swing lands", False, ("swing",)),
              ("bandage", "Bandages", "One-press bandage, timer and alerts", False, ("bandage",)),
              ("pets", "Pets", "Pets' health, distance and commands", False, ("pets",)),),
         aliases=('Unit Frames', 'Spell Timers', 'Swing Timer', 'Bandage Agent', 'Pets',
                  'cast bar', 'buffs', 'debuffs', 'party frames', 'hit chance'))
