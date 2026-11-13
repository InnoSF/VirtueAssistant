def _module_inventory():
    KEY = "inventory"; TITLE = "Inventory"
    def tile_field():
        from System import AppDomain; from System.Reflection import BindingFlags
        for a in AppDomain.CurrentDomain.GetAssemblies():
            t = a.GetType("ClassicUO.Assets.TileDataLoader")
            if t is not None: return t.GetField("_staticData", BindingFlags.Static | BindingFlags.NonPublic)
        return None
    GROUPS = ("REAGENTS", "POTIONS", "SCROLLS", "OTHER")
    ITEMS = tuple((a.lower(), "REAGENTS") + Kit.REAGENTS[a] for a in ("BP", "BM", "GA", "GI", "MR", "NS", "SS", "SA"))
    ITEMS += (("bw", "REAGENTS", "Bat Wing", 0x0F78), ("gd", "REAGENTS", "Grave Dust", 0x0F8F),
        ("db", "REAGENTS", "Daemon Blood", 0x0F7D), ("nc", "REAGENTS", "Nox Crystal", 0x0F8E),
        ("pi", "REAGENTS", "Pig Iron", 0x0F8A),
        ("p_heal", "POTIONS", "Heal", 0x0F0C), ("p_cure", "POTIONS", "Cure", 0x0F07),
        ("p_refresh", "POTIONS", "Refresh", 0x0F0B), ("p_str", "POTIONS", "Strength", 0x0F09),
        ("p_agi", "POTIONS", "Agility", 0x0F08), ("p_ns", "POTIONS", "Night Sight", 0x0F06),
        ("p_expl", "POTIONS", "Explosion", 0x0F0D), ("p_poison", "POTIONS", "Poison", 0x0F0A),
        ("s_recall", "SCROLLS", "Recall", 0x1F4C), ("s_gate", "SCROLLS", "Gate Travel", 0x1F60),
        ("s_mark", "SCROLLS", "Mark", 0x1F59), ("s_gheal", "SCROLLS", "Greater Heal", 0x1F49),
        ("s_heal", "SCROLLS", "Heal", 0x1F31), ("s_cure", "SCROLLS", "Cure", 0x1F37),
        ("s_acure", "SCROLLS", "Arch Cure", 0x1F45), ("s_mr", "SCROLLS", "Magic Reflection", 0x1F50),
        ("s_invis", "SCROLLS", "Invisibility", 0x1F58), ("s_reveal", "SCROLLS", "Reveal", 0x1F5C),
        ("s_tele", "SCROLLS", "Teleport", 0x1F42), ("s_prot", "SCROLLS", "Protection", 0x1F3B),
        ("s_bless", "SCROLLS", "Bless", 0x1F3D), ("s_res", "SCROLLS", "Resurrection", 0x1F67),
        ("o_band", "OTHER", "Bandages", 0x0E21), ("o_arrow", "OTHER", "Arrows", 0x0F3F),
        ("o_bolt", "OTHER", "Bolts", 0x1BFB))
    def item_pic(g, graphic, hue, x, y, size):
        p = G.CreateGumpItemPic(graphic, size, size); p.SetRect(x, y, size, size)
        if hue: p.Hue = hue
        p.DrawBorder = False; p.SetAcceptMouseInput(False); g.Add(p)
    def commas(n): return "{:,}".format(int(n))
    def clip(text, n): text = text[:n]; return text[:-1] if text and "\ud800" <= text[-1] <= "\udbff" else text
    def to_slot(key, g, xy):
        slot = HOST.layout_rect(key)
        if slot is None or xy is None or (xy[0], xy[1]) == (slot[0], slot[1]): return
        g.SetPos(int(slot[0]), int(slot[1])); Kit.note_rect(g, slot[0], slot[1]); Kit.moved_by_code(g)
    SORT_KINDS = (("reagents", "Reagents", (0x0F7A, 0x0F7B, 0x0F84, 0x0F85, 0x0F86, 0x0F88, 0x0F8C, 0x0F8D)
         + (0x0F78, 0x0F7D, 0x0F8A, 0x0F8E, 0x0F8F)), ("gems", "Gems", tuple(range(0x0F0F, 0x0F31))), 
        ("potions", "Potions", tuple(range(0x0F06, 0x0F0E))),
        ("scrolls", "Scrolls", tuple(range(0x1F2D, 0x1F6D)) + (0x0EF3,)),
        ("gold", "Gold", (0x0EED, 0x0EEE, 0x0EEF)), ("bandages", "Bandages", (0x0E21, 0x0EE9)),)
    PRESETS = (("reagents", "Reagents"), ("potions", "Potions"), ("bandages", "Bandages"),
               ("gold", "Gold and gems"), ("scrolls", "Scrolls"), ("maps", "Treasure maps"),
               ("ores", "Ores and ingots"), ("wood", "Wood"), ("hides", "Hides and cloth"),
               ("food", "Food"), ("weapons", "Weapons"), ("armour", "Armour"),
               ("jewellery", "Jewellery"), ("keys", "Keys and tools"))
    CAT_WORDS = {"maps": ("treasure map", "tattered map", "map"), "ores": ("ore", "ingot"), "wood": ("log", "board"),
                 "hides": ("hide", "leather", "cloth", "wool", "cotton", "flax", "yarn", "thread", "bolt of"),
                 "food": ("bread", "cake", "muffin", "pie", "apple", "pear", "peach", "grape",
                          "fish steak", "ham", "bacon", "sausage", "ribs", "cheese", "carrot",
                          "lettuce", "cabbage", "turnip", "onion", "melon", "watermelon", "squash", "gourd",
                          "lemon", "lime", "banana", "date", "coconut", "chicken", "bird",
                          "egg", "cookie", "wedge", "corn", "pumpkin", "meat", "jar of honey"),
                 "keys": ("key", "tongs", "hammer", "saw", "scissors", "pickaxe", "shovel",
                          "lockpick", "sewing", "tinker", "mortar", "fletcher", "dovetail",
                          "skillet", "rolling pin", "scorp", "plane", "inshave", "fishing pole", "hatchet", "smith")}
    CAT_SPLIT = dict((k, (frozenset(w for w in ws if " " not in w), tuple(" %s " % w for w in ws if " " in w)))
                     for k, ws in CAT_WORDS.items())
    LAYER_JEWEL = (0x06 + 2, 0x0A, 0x0E, 0x12); LAYER_HANDS = (0x01, 0x02)
    SHIELD_WORDS = frozenset(("shield", "buckler"))
    NOT_WEAPON = frozenset(("candle", "lantern", "torch", "light", "book", "spellbook", "fishing", "pickaxe", "hatchet",
                            "smith", "smyth", "sledge"))
    ARMOUR_WORDS = frozenset(("plate", "platemail", "chainmail", "ringmail", "mail", "studded", "leather", "bone",
                              "hide", "dragon", "helm", "helmet", "bascinet", "coif", "kabuto", "jingasa", "hatsuburi",
                              "gorget", "mempo", "do", "haidate", "suneate", "kote", "sode", "tonlet", "woodland",
                              "armor", "armour", "harness", "breastplate", "breastplat", "gauntlets", "solaretes",
                              "legs", "arms", "sleeves", "paldrons", "bustier"))
    cats = {"data": None, "wanted": False}
    def tile_words(name):
        toks = re.findall("[a-z]+", re.sub("%[^%]*%", "", name)); words = set(toks)
        words.update([w[:-1] for w in toks if w.endswith("s")] + [w[:-2] for w in toks if w.endswith("es")])
        return words, " " + " ".join(toks) + " "
    def build_cats(field):
        if field is None: field = safe(tile_field)
        arr = field.GetValue(None) if field is not None else None; out = dict((k, set()) for k, _c in PRESETS)
        for k, _c, gs in SORT_KINDS:
            if k == "gems": out["gold"].update(gs)
            elif k in out: out[k].update(gs)
        if arr is not None:
            for gr in range(min(int(arr.Length), 0x10000)):
                try:
                    t = arr[gr]; name = str(t.Name or "").lower()
                    if not name or bool(t.IsImpassable): continue
                    words, text = tile_words(name); worn = bool(t.IsWearable); layer = int(t.Layer)
                    if worn:
                        if layer in LAYER_HANDS:
                            kind = ("armour" if not words.isdisjoint(SHIELD_WORDS)
                                    else None if not words.isdisjoint(NOT_WEAPON) else "weapons")
                        elif not words.isdisjoint(ARMOUR_WORDS): kind = "armour"
                        else: kind = "jewellery" if layer in LAYER_JEWEL else None
                        if kind: out[kind].add(gr); continue
                    if bool(t.IsContainer): continue
                    for k, (ones, phrases) in CAT_SPLIT.items():
                        if worn and k != "keys": continue
                        if not ones.isdisjoint(words) or any(p in text for p in phrases): out[k].add(gr)
                except Exception: continue
        cats["data"] = dict((k, frozenset(v)) for k, v in out.items())
    def category_of(graphic):
        data = cats["data"] or {}
        for k, _c in PRESETS:
            if graphic in data.get(k, ()): return k
        return None
    def _part_bags():
        KEY = "bag"; TITLE = "Bags"
        try:
            import clr; from System import Array, Object, Byte, Single, UInt16, UInt32
            from System.Reflection import BindingFlags; HAVE_CLR = True
        except Exception: HAVE_CLR = False
        DEFAULT_SLOTS = 8; MIN_SLOTS, MAX_SLOTS = 1, 50; BACKPACK_INTERIOR = (142, 94); LOOSE_CELL = (150, 130)
        MAX_CELL = 600; LOOSE_GAP = 4; SHRINK_MIN = 30; CLOSED_W, CLOSED_H = 104, 64; SPLIT_KEEP = 0.10
        COLUMNS_BEAT = 0.8; SPLIT_SLOW = 0.002; DRAG_RANGE = 3; SOUND_CANT = 0x0051; PIN_CAP = 1000
        BOARDS = (0x091A, 0x092E); STACK_ON = (0x0EFA, 0x2253, 0x2252, 0x238C, 0x23A0, 0x2D50)
        LABEL_MIN_W, LABEL_MIN_H, LABEL_TWO_H = 60, 30, 46; LABEL_PITCH = 20; LABEL_LINE_H = 20; COUNT_DIGITS = "999"
        SHRINK_KEY = "UnifiedBag_shrunk"; BAR_H = 44; BAR_MIN_W = 500; SIDE_COL_W = 132; SIDE_BTN_W = 116; SIDE_RIM = 6
        SIDE_PAD = 8; SIDE_GAP = 5; SIDE_SEP_H = 9; ICON_BOX = (36, 32); DEFAULT_ICONS = (0x003C, 0x0050)
        ICON_MAGIC_TRAP = 0x1B64; ICON_MAGIC_UNTRAP = 0x1B65; ART_BARE = (2117, 2118, 2118); BARE_PAD = 4
        PANE_OVERHANG = 20; SCREEN_SLACK = 24; GRIP_OUT = 10; CATCHER_TAG = 0x7E57CA7C; FIT_STABLE_TICKS = 3; TICK = 0.1
        DRIVE_TICK = 0.05; SCAN_EVERY_FRAMES = 6; FRONT_LOOK = 8; HOOK_STALL = 0.5; FULL_GAP = 0.09
        SAVE_DELAY_TICKS = 20; OPACITY_SETTLE_POLLS = 4; DETACH_SETTLE = 0.3; GEM_BELOW = 2; NAME_CACHE_CAP = 200
        TRAP_MANA = 6; TRAP_TARGET_TIMEOUT = 5.0; TRAP_RECOVERY = 1.3; TRAP_CAST_MIN = 1.0; TRAP_RETRY_PAUSE = 1.0
        TRAP_RETRIES = 3; J_FIZZLE = ["fizzles", "concentration is disturbed"]
        J_BUSY = ["already casting", "not yet recovered"]; J_REAGENTS = ["More reagents are needed"]
        J_MANA = ["Insufficient mana", "not have enough mana"]; SEARCH_HUE = 0x0044; SEARCH_LIT = 8.0
        J_NOREACH = ["cannot be seen", "can not be seen", "that is too far away", "can't trap", "cannot trap",
                     "can only trap", "cannot place a trap", "can't disarm"]
        SEARCH_SETTLE = 0.15; SEARCH_MIN = 2; SEARCH_SCAN_CAP = 3000; SEARCH_LIT_CAP = 400; SEARCH_DEPTH = 8
        HUE_MEMORY = 2.0; TILE_NAME_CAP = 600; SORT_GAP = 0.7; SORT_CAP = 600; SORT_FAIL_STOP = 3; SORT_RECHECK = 2
        SORT_GRAPHICS_CAP = 24; BAG_MAX_ITEMS = 125; J_FULL = ["cannot hold more"]
        J_WAIT = ["must wait to perform another action"]
        SORT_KIND_KEYS = tuple(k[0] for k in SORT_KINDS); C_SEAM = "#5C544A"; C_EDGE = "#7A7066"
        HUE_OK, HUE_INFO, HUE_ERR = Kit.HUE_GOOD, Kit.HUE_INFO, Kit.HUE_BAD; LINK_CMD = "UnifiedBag_cmd"
        LINK_STATE = "UnifiedBag_state"; DOCK_KEY = KEY
        class Bag(object):
            def __init__(self, **kw): self.update(**kw)
            def update(self, **kw): self.__dict__.update(kw)
        settings = {}; DEFAULTS = dict(settings)
        st = {"cfg_bad": False, "slots": DEFAULT_SLOTS, "cols": 0, "rows": 0, "assign": {}, "frame_x": 200,
              "frame_y": 120, "saved_fx": 200, "saved_fy": 120, "cell_w": BACKPACK_INTERIOR[0],
              "cell_h": BACKPACK_INTERIOR[1], "fit_pending": True, "fit_seen": None, "trim": True, "opacity": 0.9,
              "scale_pct": 100, "scale_items": False, "driving": False, "drive_fixed": False, "drive_told": False,
              "hb_frame": -1, "hb_time": 0.0, "opacity_pending": None, "icons_used": None, "status_text": "",
              "own_cell": None, "mgr_x": 120, "mgr_y": 140, "trp_x": 200, "trp_y": 180, "mgr_min": False,
              "trp_min": False, "minimized": False, "docked": False, "bare": False, "side_hidden": False,
              "link_state": None, "attach": None, "attach_g": None, "canvas": None, "side_pw": 0, "detached_at": 0.0,
              "grid_wh": None, "names": {}, "wait_player": False, "wait_load": False, "load_wanted": False,
              "load_text": None, "trap_sel": set(), "trap_extra": [], "job": None, "queue": [], "reported": False,
              "dirty_frame": True, "dirty_mgr": False, "dirty_trp": False, "open_mgr": False, "open_trp": False,
              "want_mgr": False, "want_trp": False, "save_in": -1, "to_write": None, "shutting": False,
              "flt_pick": None, "quick_at": 0.0, "filters": [], "open_flt": False, "dirty_flt": False, "flt_min": False,
              "flt_x": 260, "flt_y": 120, "rules": {}, "sort": None, "srt_x": 240, "srt_y": 160, "srt_min": False,
              "open_srt": False, "want_srt": False, "dirty_srt": False, "layout": (), "want_flt": False,
              "geom": (1, BACKPACK_INTERIOR[0], BACKPACK_INTERIOR[1], 0), "bar_raw": None, "grid_raw": None,
              "grid_info": (None, False), "slot_raws": (), "cats_seen": None}
        win = {"g": None, "c": {}, "store": ({}, {}), "side_status": None, "bar": None, "grid": None, "mgr": None,
               "trp": None, "trap_checks": [], "srt": None, "rule_checks": [], "search_box": None, "counts": [],
               "count_state": {}}
        cleanup, queue, say = Kit.basics(st, TITLE)
        def act(kind, *args):
            def handler(*_ignored): queue.add((kind,) + args)
            return handler
        def dispose(key): Kit.dispose(win.get(key)); win[key] = None
        def box(x, y, w, h, color, alpha): b = G.CreateGumpColorBox(alpha, color); b.SetRect(x, y, w, h); return b
        def label(g, text, x, y, hue=None): return Kit.inert(Kit.add_label(g, text, x, y, hue))
        def framed_window(k, w, h, title, on_min, on_close):
            M = Kit.MARGIN; minimized = st[k + "_min"]; g = G.CreateGump(True, True)
            Kit.place(g, st[k + "_x"], st[k + "_y"], w, h)
            Kit.add_window_frame(g, w, h, corners=not minimized); Kit.add_section(g, M, M, w - 2 * M, 30)
            Kit.add_label(g, title, M + 30, M + 7, Kit.HUE_TITLE)
            Kit.title_catcher(g, M, M, w - 2 * M - 84, 30, on_min, key="bag_" + k); store = ({}, {})
            Kit.art_button(g, store, "min", Kit.ART_RESTORE if minimized else Kit.ART_MIN, w - M - 74, M + 7, None,
                           Kit.RESTORE_TIP if minimized else Kit.MIN_TIP, on_click=on_min)
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, "Close this window",
                           on_click=on_close)
            return g, store, M + 30 + Kit.GAP
        def sub_shown(k, g, moved, **more): Kit.add_front(g); Kit.on_moved(g, moved); win[k] = g; win.update(more)
        def schedule_save(): st["save_in"] = SAVE_DELAY_TICKS
        def frame_changed(): st["dirty_frame"] = True; schedule_save()
        def short(text, n): text = text or ""; return text if len(text) <= n else text[: n - 1] + "~"
        def bag_name(serial, with_serial=True):
            name = st["names"].get(serial)
            if name is None:
                it = Kit.find_item(serial)
                if not it: return "0x%08X (not loaded)" % serial
                name = it.Name or "Container"
                if len(st["names"]) >= NAME_CACHE_CAP: st["names"] = {}
                st["names"][serial] = name
            return ("%s  0x%08X" % (name, serial)) if with_serial else name
        def forget_names(): st["names"] = {}
        R = Bag(tried=False, ok=False, can_ok=False, error="", f_tiles=None)
        H = Bag(frame=0, gumps={}, managed=set(), trimmed=set(), bounds={}, scale=1.0, max_w=0, max_h=0, disabled=False,
                error="", fail_streak=0, open_count=0, catchers={}, icons=None, hook_calls=0, pre_calls=0, glist=None,
                head=None, count=-1, lay=None, want=frozenset(), placed={}, bar_at=None, full_frame=-1000, full_at=0.0,
                fulls=0, labels_for=(None, None), meas={}, opened=frozenset(), hold=None, ginfo={}, catch_ok={}, gtr={})
        CANVAS = {"ver": 0, "regions": {}, "order": [], "orient": "rows", "breaks": None,
                  "sig": None, "items": None, "kinds": {}, "size": None, "slow": False, "job": None}
        PLAN = {"done": None}
        JR = {"rd": None}; PIN = {}; PIN_ORDER = []
        CV = {"ctrl": None, "rect": None, "texts": True, "said": None, "sum_i": 0, "art": {}, "world": None,
              "tiles": None, "prof_at": 0.0, "sum_at": 0.0, "hooked": False, "poked": set(), "poke_at": 0.0}
        def init_interop():
            if not HAVE_CLR: R.error = "clr module unavailable"; return
            try:
                asm = API.GetType().Assembly; clr.AddReference(asm)
                from ClassicUO.Game.UI.Controls import Control; from ClassicUO.Game.UI.Gumps import ContainerGump
                from ClassicUO.Game.UI.Controls import ClickPriority
                inst = BindingFlags.Instance | BindingFlags.NonPublic
                stat = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
                cg = clr.GetClrType(ContainerGump); R.ContainerGump = ContainerGump
                R.f_data = cg.GetField("_data", inst); R.f_pic = cg.GetField("_gumpPicContainer", inst)
                R.f_hit = cg.GetField("_hitBox", inst); ctl = clr.GetClrType(Control)
                R.m_offset = ctl.GetMethod("SetHitTestOffset", inst); R.f_bounds = ctl.GetField("_bounds", inst)
                R.Point = clr.GetPythonType(ctl.GetProperty("Location").PropertyType)
                R.Rect = clr.GetPythonType(R.f_bounds.FieldType); uim = asm.GetType("ClassicUO.Game.Managers.UIManager")
                R.p_gumps = uim.GetProperty("Gumps", stat); R.p_cscale = uim.GetProperty("ContainerScale", stat)
                pm = asm.GetType("ClassicUO.Configuration.ProfileManager")
                R.p_profile = pm.GetProperty("CurrentProfile", stat)
                for name in ("f_data", "f_pic", "f_hit", "m_offset", "f_bounds", "p_gumps", "p_cscale", "p_profile"):
                    if getattr(R, name) is None: raise Exception("client member not found: " + name)
                class FrameHook(Control):
                    def PreDraw(self): H.pre_calls += 1; H.hook_calls += 1; guarded_tick()
                    def Draw(self, batcher, x, y):
                        if H.pre_calls == 0: H.hook_calls += 1; guarded_tick()
                        return True
                class DropCatcher(Control):
                    def Draw(self, batcher, x, y): return True
                R.Hook = FrameHook; R.Catcher = DropCatcher; R.LowPriority = ClickPriority.Low; R.ok = True
            except Exception as e: R.ok = False; R.error = str(e); return
            canvas_interop()
        def canvas_interop():
            R.can_ok = False
            try:
                from ClassicUO.Game.UI.Controls import Control, ItemGump
                class BagCanvas(Control):
                    def Draw(self, batcher, x, y):
                        try: w, h = self.va_wh
                        except Exception: return True
                        try: canvas_rehide()
                        except Exception: pass
                        if batcher.ClipBegin(int(x), int(y), int(w), int(h)):
                            try:
                                Control.Draw(self, batcher, x, y)
                                if CV["texts"]: canvas_texts(batcher, int(x), int(y))
                            finally: batcher.FlushBatch(); batcher.ClipEnd()
                        return True
                    def OnMouseUp(self, x, y, button):
                        try:
                            if canvas_mouse_up(int(x), int(y), button): return
                        except Exception as e: H.error = "canvas: %s" % e
                        Control.OnMouseUp(self, x, y, button)
                    def OnMouseDoubleClick(self, x, y, button):
                        try:
                            if canvas_double(int(x), int(y), button): return True
                        except Exception as e: H.error = "canvas: %s" % e
                        return Control.OnMouseDoubleClick(self, x, y, button)
                    def OnMouseOver(self, x, y):
                        try: canvas_hover(self, int(x), int(y))
                        except Exception: pass
                        Control.OnMouseOver(self, x, y)
                class BagLayer(Control): pass
                class CanvasItem(ItemGump):
                    def OnMouseUp(self, x, y, button): R.up_item = self; ItemGump.OnMouseUp(self, x, y, button)
                R.Canvas, R.Layer, R.CanvasItem, R.ItemGump = (BagCanvas, BagLayer, CanvasItem, ItemGump)
                R.up_item = None; R.Mouse = Tz.T("ClassicUO.Input.Mouse")
                R.Actions = Tz.T("ClassicUO.Game.GameActions"); R.f_tiles = tile_field(); R.can_ok = True
            except Exception as e: R.can_ok = False; H.error = "canvas: %s" % e
        def new_ctl(cls):
            try: return cls()
            except Exception: return cls(None)
        def add_hook(grid, tell):
            if not R.ok or H.disabled or st["drive_fixed"]: return
            try:
                hook = new_ctl(R.Hook); hook.AcceptMouseInput = False; raw = st["grid_info"][0]
                if raw is not None and Client.on_client_thread():
                    with Kit.quiet:
                        hook.Parent = raw
                        if raw.Children.Contains(hook): return
                grid.Add(hook)
            except Exception as e:
                st["driving"] = st["drive_fixed"] = True; H.error = "draw hook: %s" % e
                if tell:
                    API.SysMsg(TITLE + ": couldn't install the draw hook (%s); the script keeps the bags in place."
                               % e, HUE_INFO)
        def lay_under(grid): safe(lambda: setattr(grid, "LayerOrder", type(grid.LayerOrder).Under))
        _raw_way = {}
        def _raw_gump(w): return w.Gump
        RAW_WAYS = (_raw_gump, Kit.client_control)
        def raw_of(wrapper):
            if wrapper is None: return None
            t = type(wrapper); way = _raw_way.get(t)
            if way is not None:
                with Kit.quiet:
                    v = way(wrapper)
                    if v is not None: return v
            for fn in RAW_WAYS:
                if fn is way: continue
                try: v = fn(wrapper)
                except Exception: continue
                if v is not None: _raw_way[t] = fn; return v
            return None
        def on_main(fn): return Kit.on_client(fn, False)
        def guarded_tick():
            try: frame_tick(); H.fail_streak = 0
            except Exception as e: H.error = str(e); H.fail_streak += 1
            except: H.error = "unknown error"; H.fail_streak += 1
            if H.fail_streak > 120: H.disabled = True
        def set_offset(g, x, y):
            off = g.Offset
            if off.X != x or off.Y != y: R.m_offset.Invoke(g, Array[Object]([x, y]))
        def scan_gumps():
            found = {}; lst = R.p_gumps.GetValue(None); H.glist = lst; node = lst.First
            while node is not None:
                v = node.Value
                if isinstance(v, R.ContainerGump) and not v.IsDisposed: found[int(v.LocalSerial)] = v
                node = node.Next
            H.gumps = found
            try: H.scale = float(R.p_cscale.GetValue(None))
            except Exception: pass
        def front_check():
            lst = H.glist
            if lst is None: return
            node = lst.First; head = node.Value if node is not None else None; cnt = lst.Count
            if head is H.head and cnt == H.count: return
            H.head, H.count = head, cnt; want = H.want
            if not want: return
            gumps = H.gumps; n = 0
            while node is not None and n < FRONT_LOOK:
                v = node.Value
                if isinstance(v, R.ContainerGump) and not v.IsDisposed:
                    ser = int(v.LocalSerial)
                    if ser in want and gumps.get(ser) is not v: gumps[ser] = v
                node = node.Next; n += 1
        def interior(g):
            b = bounds_of(g); s = H.scale; left, top = int(b[0] * s), int(b[1] * s)
            return left, top, int(b[2] * s) - left, int(b[3] * s) - top
        def cell_xy(idx):
            cols, cw, ch, gap = st["geom"]; r, c = divmod(idx, cols)
            return st["frame_x"] + c * (cw + gap), st["frame_y"] + top_off() + r * (ch + gap)
        def get_pos(c): loc = c.Location; return int(loc.X), int(loc.Y)
        def move(c, x, y):
            loc = c.Location
            if loc.X != x or loc.Y != y: c.Location = R.Point(x, y)
        def get_size(c): r = R.f_bounds.GetValue(c); return int(r.Width), int(r.Height)
        def release(g):
            H.managed.discard(g); H.placed.pop(g, None); was_trimmed = g in H.trimmed; H.trimmed.discard(g)
            if g.IsDisposed: H.catchers.pop(g, None); return
            remove_catcher(g)
            if not g.IsVisible: g.IsVisible = True; Kit.stir()
            set_offset(g, 0, 0); g.AcceptMouseInput = True; g.CanMove = True; pic = R.f_pic.GetValue(g)
            if pic is not None: pic.Alpha = 1.0
            if was_trimmed and not g.IsMinimized: g.RequestUpdateContents()
        def detach(g, c):
            kids = g.Children
            while kids.Contains(c): kids.Remove(c)
        def drop_child(g, c):
            detach(g, c)
            if not c.IsDisposed: c.Dispose()
        def remove_catcher(g):
            H.catch_ok.pop(g, None); c = H.catchers.pop(g, None)
            if c is not None: drop_child(g, c)
        def purge_stray_catchers(g):
            mine = H.catchers.get(g)
            for child in list(g.Children):
                if child is not mine and int(child.LocalSerial) == CATCHER_TAG: drop_child(g, child)
        def ensure_catcher(g, left, top, iw, ih):
            c = H.catchers.get(g); kids = g.Children; n = kids.Count; ok = H.catch_ok.get(g)
            if ok is not None and c is not None and ok[0] is c and ok[1] == n \
                    and ok[2] is (kids[n - 1] if n else None) and ok[3] == (left, top, iw, ih) and not c.IsDisposed:
                return
            if c is None or c.IsDisposed or not kids.Contains(c):
                if g not in H.catchers: purge_stray_catchers(g)
                c = R.Catcher(); c.LocalSerial = CATCHER_TAG; c.AcceptMouseInput = True; c.Priority = R.LowPriority
                c.Parent = g; detach(g, c); kids.Insert(0, c); H.catchers[g] = c
            elif kids.IndexOf(c) != 0 or kids.LastIndexOf(c) != 0: detach(g, c); kids.Insert(0, c)
            r = R.f_bounds.GetValue(c)
            if (r.X, r.Y, r.Width, r.Height) != (left, top, iw, ih): R.f_bounds.SetValue(c, R.Rect(left, top, iw, ih))
            if not c.IsVisible: c.IsVisible = True
            n = kids.Count
            if len(H.catch_ok) >= GINFO_CAP: H.catch_ok.clear()
            H.catch_ok[g] = (c, n, kids[n - 1] if n else None, (left, top, iw, ih))
        GINFO_CAP = 64
        def gump_info(g):
            gi = H.ginfo.get(g)
            if gi is None:
                gi = (int(g.Graphic), bool(g.IsChessboard or g.IsBackgammonBoard))
                if len(H.ginfo) >= GINFO_CAP: H.ginfo.clear()
                H.ginfo[g] = gi
            return gi
        def place_bag(g, idx, trim):
            if g.CanMove: g.CanMove = False
            set_offset(g, 0, 0); cx, cy = cell_xy(idx); board = gump_info(g)[1]
            if g.IsMinimized or board or not trim:
                if g in H.trimmed:
                    H.trimmed.discard(g); remove_catcher(g)
                    if not g.IsMinimized: g.RequestUpdateContents()
                if not g.AcceptMouseInput and g.IsVisible: g.AcceptMouseInput = True
                pic = R.f_pic.GetValue(g)
                if pic is not None and abs(pic.Alpha - st["opacity"]) > 0.01: pic.Alpha = st["opacity"]
                move(g, cx, cy)
                if g.IsMinimized: return 0, 0, pic, False
                w, h = get_size(g); return w, h, pic, False
            left, top, iw, ih = interior(g); pic = R.f_pic.GetValue(g)
            if pic is not None and pic.IsVisible: pic.IsVisible = False
            hit = R.f_hit.GetValue(g)
            if hit is not None and hit.IsVisible: hit.IsVisible = False
            if g.AcceptMouseInput: g.AcceptMouseInput = False
            ensure_catcher(g, left, top, iw, ih); move(g, cx - left, cy - top); H.trimmed.add(g)
            ov = int(round(PANE_OVERHANG * H.scale)); return iw + ov, ih + ov, pic, True
        def frame_tick():
            if H.disabled or st["shutting"]: return
            bar = st["bar_raw"]; grid, gbare = st["grid_info"]; moved = False; att = st["attach"]
            hidden = st["minimized"]
            if att is not None:
                hidden = hidden or not att.get("shown", True); lead = attach_raw()
                if lead is not None and not lead.IsDisposed:
                    bx, by = get_pos(lead); bx, by = bx + int(att.get("dx", 0)), by + int(att.get("dy", 0))
                    moved = (bx, by) != H.bar_at; H.bar_at = (bx, by); st["frame_x"], st["frame_y"] = bx, by
                    if grid is not None and not grid.IsDisposed:
                        move(grid, bx, by)
                        if grid.IsVisible == hidden: grid.IsVisible = not hidden; Kit.stir()
            else:
                if gbare and grid is not None and not grid.IsDisposed: lead, other, dy = grid, bar, 0
                else: lead, other, dy = bar, grid, BAR_H
                if lead is not None and not lead.IsDisposed:
                    bx, by = get_pos(lead); moved = (bx, by) != H.bar_at; H.bar_at = (bx, by)
                    st["frame_x"], st["frame_y"] = bx, by
                    if other is not None and not other.IsDisposed: move(other, bx, by + dy)
            lay = st["layout"]
            if lay is not H.lay: H.lay = lay; H.want = frozenset([s for _, s in lay])
            H.frame += 1; now = time.time()
            full = H.frame - H.full_frame >= SCAN_EVERY_FRAMES and now - H.full_at >= FULL_GAP
            if full: H.full_frame, H.full_at = H.frame, now; H.fulls += 1; scan_gumps()
            else: front_check()
            rescanned = full; icons_due = full and H.fulls % 10 == 1; full = full or moved; trim = st["trim"]
            look = (trim, st["opacity"], st["geom"], top_off(), CANVAS["ver"]); active = set(); opened = set()
            mw = mh = 0
            first = None; f_pic = R.f_pic; canv = st["canvas"] is not None and not hidden
            if canv:
                cr = CV["rect"] or (0, 0, 0, 0); px, py = st["frame_x"] + cr[0], st["frame_y"] + cr[1]
                park = full or st["driving"]; seen = (CV["seen_n"], CV["seen_last"], CV["seen_min"])
            for idx, serial in lay:
                g = H.gumps.get(serial)
                if g is None: continue
                if g.IsDisposed:
                    if rescanned: continue
                    rescanned = True; scan_gumps(); g = H.gumps.get(serial)
                    if g is None or g.IsDisposed: continue
                opened.add(idx)
                if canv:
                    try:
                        if canvas_bag(g, serial, px, py, park, seen):
                            if first is None: first = g
                            active.add(g); H.managed.add(g)
                    except Exception as e: H.error = "bag 0x%08X: %s" % (serial, e)
                    continue
                if first is None: first = g
                active.add(g); H.managed.add(g)
                try:
                    if hidden:
                        if g.IsVisible: g.IsVisible = False; Kit.stir()
                        H.placed.pop(g, None); continue
                    if not g.IsVisible: g.IsVisible = True; Kit.stir()
                    mini = bool(g.IsMinimized); key = (idx, look, mini); done = H.placed.get(g); pic = f_pic.GetValue(g)
                    if not full and done is not None and done[0] == key and pic is done[2] \
                            and not (done[3] and pic is not None and pic.IsVisible):
                        w, h = done[1]
                    else:
                        w, h, pic, trimmed = place_bag(g, idx, trim); H.placed[g] = (key, (w, h), pic, trimmed)
                        if mini: iw_, ih_ = get_size(g); H.meas[idx] = (iw_, ih_, H.scale, True, None)
                        else: H.meas[idx] = (w, h, H.scale, False, int(g.Graphic) if trimmed else None)
                    mw, mh = max(mw, w), max(mh, h)
                except Exception as e: H.error = "bag 0x%08X: %s" % (serial, e)
            H.open_count = len(opened)
            if opened != H.opened:
                H.opened = frozenset(opened)
                for idx in [i for i in H.meas if i not in opened]: H.meas.pop(idx, None)
            if first is not None and icons_due:
                try:
                    iconized = int(R.f_data.GetValue(first).IconizedGraphic) or DEFAULT_ICONS[1]
                    H.icons = (int(first.Graphic), iconized)
                except Exception: pass
            if len(H.managed) > len(active):
                for g in [g for g in H.managed if g not in active]: release(g)
            H.max_w, H.max_h = mw, mh; raws = st["slot_raws"]
            if opened != H.labels_for[0] or raws is not H.labels_for[1]:
                for idx, labs in enumerate(raws):
                    show = idx not in opened
                    for lab in labs:
                        if lab is not None and lab.IsVisible != show: lab.IsVisible = show
                H.labels_for = (opened, raws)
        def canvas_bag(g, serial, px, py, park, seen):
            if gump_info(g)[1]:
                if g in H.managed: release(g)
                return False
            if g.IsVisible: g.IsVisible = False; Kit.stir()
            if g.AcceptMouseInput: g.AcceptMouseInput = False
            if park:
                if g.CanMove: g.CanMove = False
                move(g, px, py)
            kids = g.Children; n = kids.Count
            if seen[0].get(serial) != n or seen[1].get(serial) is not \
                    (kids[n - 1] if n else None) or seen[2].get(serial) != g.IsMinimized:
                if CV["built"] == CANVAS["ver"] and CV["ctrl"] is not None: canvas_resync(serial, g)
            return True
        def canvas_rehide():
            gumps = H.gumps
            for slot in CANVAS["order"]:
                info = CANVAS["kinds"].get(slot)
                if info is None or info[0] == "board" or info[0] == "closed": continue
                g = gumps.get(info[2])
                if g is not None and g.IsVisible: g.IsVisible = False; Kit.stir()
        def restore_all():
            for g in list(H.managed):
                with Kit.quiet: release(g)
        def set_minimized_all(minimize):
            serials = set(st["assign"].values())
            def run():
                scan_gumps(); n = 0
                for s in serials:
                    g = H.gumps.get(s)
                    if g is None or g.IsDisposed or g.IsChessboard or g.IsBackgammonBoard: continue
                    if bool(g.IsMinimized) != minimize: g.IsMinimized = minimize; n += 1
                return n
            return on_main(run)
        def read_scale():
            def run():
                prof = R.p_profile.GetValue(None)
                return (int(prof.ContainersScale), bool(prof.ScaleItemsInsideContainers))
            return on_main(run)
        def apply_scale(pct, items):
            def run():
                prof = R.p_profile.GetValue(None)
                changed = (int(prof.ContainersScale) != pct or bool(prof.ScaleItemsInsideContainers) != items)
                prof.ContainersScale = Byte(pct); prof.ScaleItemsInsideContainers = items
                R.p_cscale.SetValue(None, Single(pct / 100.0)); H.scale = pct / 100.0
                if changed:
                    node = R.p_gumps.GetValue(None).First
                    while node is not None:
                        v = node.Value
                        if isinstance(v, R.ContainerGump) and not v.IsDisposed: v.RequestUpdateContents()
                        node = node.Next
                return changed
            return on_main(run)
        def bag_is_open(serial):
            if R.ok and not H.disabled:
                g = H.gumps.get(serial); return g is not None and not g.IsDisposed
            it = Kit.find_item(serial); return bool(it) and Kit.is_open(safe(lambda: it.GetContainerGump()))
        def cfg_file():
            serial = safe(lambda: int(API.Player.Serial), 0); return Kit.data_path("_unified_bag_%d.cfg" % serial)
        def load_settings(): parse_cfg(read_cfg())
        def save_settings():
            st["save_in"] = -1
            if not attached() and st["canvas"] != "alone" and not HOST.layout_holds(KEY):
                st["saved_fx"], st["saved_fy"] = st["frame_x"], st["frame_y"]
            lines = ["slots=%d" % st["slots"], "cols=%d" % st["cols"], "rows=%d" % st["rows"],
                "frame_x=%d" % st["saved_fx"], "frame_y=%d" % st["saved_fy"],
                "cell_w=%d" % st["cell_w"], "cell_h=%d" % st["cell_h"],
                "trim=%d" % int(st["trim"]), "collapsed=%d" % int(st["minimized"]), "bare=%d" % int(st["bare"]),
                "side=%d" % int(st["side_hidden"]), "opacity=%d" % int(round(st["opacity"] * 100)),
                "mgr_x=%d" % st["mgr_x"], "mgr_y=%d" % st["mgr_y"], "trp_x=%d" % st["trp_x"], "trp_y=%d" % st["trp_y"],
                "mgr_open=%d" % int(st["open_mgr"]), "mgr_min=%d" % int(st["mgr_min"]),
                "trp_open=%d" % int(st["open_trp"]), "trp_min=%d" % int(st["trp_min"]),
                "trapsel=" + ",".join(str(s) for s in sorted(st["trap_sel"])),
                "trapextra=" + ",".join(str(s) for s in st["trap_extra"]),]
            for idx in sorted(st["assign"]): lines.append("slot.%d=%d" % (idx, st["assign"][idx]))
            lines += ["srt_x=%d" % st["srt_x"], "srt_y=%d" % st["srt_y"],
                      "srt_open=%d" % int(st["open_srt"]), "srt_min=%d" % int(st["srt_min"])]
            for idx in sorted(st["rules"]):
                kinds, graphics = st["rules"][idx]
                if kinds or graphics:
                    lines.append("sort.%d=%s;%s" % (idx, ",".join(sorted(kinds)), ",".join(str(g) for g in graphics)))
            lines += ["flt_x=%d" % st["flt_x"], "flt_y=%d" % st["flt_y"], "flt_min=%d" % int(st["flt_min"]),
                      "flt_open=%d" % int(st["open_flt"])]
            st["to_write"] = (cfg_file(), "\n".join(lines))
            if not safe(lambda: HOST.by_key[KEY].running, False): write_saved()
        def others_cursor(): return bool(HOST.cursor_busy(KEY))
        def write_saved():
            job = st["to_write"]
            if job is None: return
            st["to_write"] = None; path, text = job
            if st["cfg_bad"]: return
            try: Kit.write_safe(path, text)
            except Exception as e: API.SysMsg(TITLE + ": couldn't save its settings (%s)." % e, HUE_ERR)
        def parse_serials(text): return [int(p) for p in (text or "").split(",") if p.strip().isdigit()]
        def read_cfg(): return Kit.read_safe(cfg_file())
        def parse_cfg(raw):
            st["cfg_bad"] = raw is None
            if raw is None:
                API.SysMsg(TITLE + ": couldn't read its settings file, so changes aren't saved.", HUE_ERR); return
            if not raw: return
            vals, ints = {}, {}
            for line in raw.splitlines():
                if "=" in line:
                    k, v = [p.strip() for p in line.split("=", 1)]; vals[k] = v
                    try: n = int(v)
                    except ValueError: continue
                    if abs(n) <= (1000000 if k.endswith(("_x", "_y")) else 0x7FFFFFFF): ints[k] = n
            st["slots"] = max(MIN_SLOTS, min(MAX_SLOTS, ints.get("slots", st["slots"])))
            st["cols"] = max(0, min(MAX_SLOTS, ints.get("cols", 0)))
            st["rows"] = max(0, min(MAX_SLOTS, ints.get("rows", 0)))
            st["frame_x"], st["frame_y"] = Kit.adapt(ints.get("frame_x", st["frame_x"]), ints.get("frame_y",
                                                                                                  st["frame_y"]))
            st["saved_fx"], st["saved_fy"] = st["frame_x"], st["frame_y"]
            st["cell_w"] = max(20, min(MAX_CELL, ints.get("cell_w", st["cell_w"])))
            st["cell_h"] = max(20, min(MAX_CELL, ints.get("cell_h", st["cell_h"])))
            st["fit_pending"] = "cell_w" not in ints
            st["opacity"] = max(10, min(100, ints.get("opacity", ints.get("panel_a", 90)))) / 100.0
            for attr, k, dflt in (("trim", "trim", 1), ("minimized", "collapsed", 0), ("bare", "bare", 0),
                                  ("side_hidden", "side", 0), ("mgr_min", "mgr_min", 0), ("trp_min", "trp_min", 0),
                                  ("want_mgr", "mgr_open", 0), ("want_trp", "trp_open", 0), ("srt_min", "srt_min", 0),
                                  ("want_srt", "srt_open", 0), ("flt_min", "flt_min", 0), ("want_flt", "flt_open", 0)):
                st[attr] = ints.get(k, dflt) == 1
            for k in ("mgr", "trp", "srt", "flt"):
                x, y = Kit.adapt(ints.get(k + "_x", st[k + "_x"]), ints.get(k + "_y", st[k + "_y"]))
                st.update(**{k + "_x": x, k + "_y": y})
            st["trap_sel"] = set(parse_serials(vals.get("trapsel")))
            st["trap_extra"] = parse_serials(vals.get("trapextra")); st["assign"], st["rules"] = {}, {}
            for k, v in vals.items():
                pre, _, num = k.partition(".")
                try: idx = int(num)
                except ValueError: continue
                if not 0 <= idx < st["slots"]: continue
                if pre == "slot" and ints.get(k, 0) > 0: st["assign"][idx] = ints[k]
                elif pre == "sort":
                    rule = parse_rule(v)
                    if rule is not None: st["rules"][idx] = rule
        def parse_rule(text):
            kpart, _, gpart = (text or "").partition(";")
            kinds = frozenset(k for k in (p.strip() for p in kpart.split(",")) if k in SORT_KIND_KEYS); graphics = []
            for p in gpart.split(","):
                p = p.strip()
                if p.isdigit() and 0 < int(p) <= 0xFFFF and int(p) not in graphics: graphics.append(int(p))
            graphics = tuple(graphics[:SORT_GRAPHICS_CAP]); return (kinds, graphics) if (kinds or graphics) else None
        fitov = {"told": None, "cols": None, "cell": None, "area": None}
        def layout_dims(slots=None, cols=None, rows=None):
            slots = st["slots"] if slots is None else slots
            if cols is None and rows is None and fitov["cols"]:
                c = max(1, min(slots, fitov["cols"])); return c, int(math.ceil(slots / float(c)))
            cols = min(slots, st["cols"] if cols is None else cols); rows = st["rows"] if rows is None else rows
            if cols > 0 and rows > 0: return cols, rows
            if cols > 0: return cols, int(math.ceil(slots / float(cols)))
            if rows > 0: c = int(math.ceil(slots / float(rows))); return c, int(math.ceil(slots / float(c)))
            c = max(1, int(math.ceil(math.sqrt(slots)))); return c, int(math.ceil(slots / float(c)))
        def trimming(): return st["trim"] and R.ok and not H.disabled
        LAYOUT_SEEN = [None, None]
        def publish_layout():
            a = st["assign"]
            if a == LAYOUT_SEEN[0] and st["slots"] == LAYOUT_SEEN[1]: return
            lay = tuple(sorted((i, s) for i, s in a.items() if i < st["slots"]))
            if lay != st["layout"]: st["layout"] = lay
            LAYOUT_SEEN[0], LAYOUT_SEEN[1] = dict(a), st["slots"]
        def default_cell():
            s = H.scale if R.ok else 1.0
            if trimming(): return int(BACKPACK_INTERIOR[0] * s), int(BACKPACK_INTERIOR[1] * s)
            return int(LOOSE_CELL[0] * s), int(LOOSE_CELL[1] * s)
        def refit_cells(): st["cell_w"], st["cell_h"] = default_cell(); st["fit_pending"] = True; frame_changed()
        def side_columns(avail_h):
            inner = max(avail_h - 2 * (SIDE_PAD + SIDE_RIM), 0); cols, used = [[]], 0
            for item in [("bagicons", ICON_BOX[1] + 22), ("break", SIDE_SEP_H), ("spellicons", ICON_BOX[1] + 22),
                         ("stop", 22 + 4 + 18), ("quick", 4 * 24), ("tools", 24 + 26 + 24)]:
                kind, h = item; need = h + (SIDE_GAP if cols[-1] else 0)
                if cols[-1] and used + need > inner and kind != "break": cols.append([]); used, need = 0, h
                if kind == "break" and not cols[-1]: continue
                cols[-1].append(item); used += need
            for col in cols:
                while col and col[0][0] == "break": col.pop(0)
                while col and col[-1][0] == "break": col.pop()
            cols = [c for c in cols if c]; heights = [sum(i[1] for i in c) + SIDE_GAP * (len(c) - 1) for c in cols]
            return cols, heights
        def icon_pic(graphic, x, y, box_w, box_h, tip, handler):
            pic = G.CreateGumpPic(graphic); nw = pic.GetWidth() or box_w
            nh = pic.GetHeight() or box_h; k = min(box_w / float(nw), box_h / float(nh), 1.0)
            w, h = max(1, int(nw * k)), max(1, int(nh * k))
            pic.SetRect(x + (box_w - w) // 2, y + (box_h - h) // 2, w, h)
            Kit.set(pic, "ContainsByBounds", True); pic.SetTooltip(tip)
            G.AddControlOnClick(pic, handler); return pic
        def build_side_panel(grid, x0, gh, y0=0):
            tw, th = bare_btn_size(); reserve = th + BARE_PAD; cols, heights = side_columns(gh - reserve)
            pw = len(cols) * SIDE_COL_W + 2 * SIDE_RIM; ph = max(gh, max(heights) + 2 * (SIDE_PAD + SIDE_RIM) + reserve)
            Kit.add_resizepic(grid, Kit.WINDOW_BG, x0, y0, pw, ph)
            Kit.add_section(grid, x0 + SIDE_RIM, y0 + SIDE_RIM, pw - 2 * SIDE_RIM, ph - 2 * SIDE_RIM)
            art, iconized = st["icons_used"]
            for ci, col in enumerate(cols):
                cx = x0 + SIDE_RIM + ci * SIDE_COL_W
                if ci:
                    grid.Add(Kit.inert(box(cx, y0 + SIDE_RIM + SIDE_PAD, 1,
                                          ph - 2 * (SIDE_RIM + SIDE_PAD), C_SEAM, 0.8)))
                bx = cx + (SIDE_COL_W - SIDE_BTN_W) // 2; y = y0 + (ph - reserve - heights[ci]) // 2
                for kind, h in col:
                    if kind in ("bagicons", "spellicons"):
                        if kind == "bagicons":
                            pair = ((iconized, "Minimize every open slot bag", act("set_min", True), "Minimize"),
                                    (art, "Restore every minimized slot bag", act("set_min", False), "Restore"))
                        else:
                            pair = ((ICON_MAGIC_TRAP, "Cast Magic Trap on every ticked trap bag",
                                     act("start_job", "Magic Trap"), "Trap"), (ICON_MAGIC_UNTRAP,
                                     "Cast Magic Untrap on every ticked trap bag", act("start_job", "Magic Untrap"),
                                     "Untrap"))
                        half = SIDE_BTN_W // 2
                        for j, (graphic, tip, handler, cap) in enumerate(pair):
                            grid.Add(icon_pic(graphic, bx + j * half, y, half, ICON_BOX[1], tip, handler))
                            label(grid, cap, bx + j * half + max(0, (half - Kit.text_w(cap)) // 2),
                                  y + ICON_BOX[1] + 3, Kit.HUE_INFO)
                    elif kind == "stop":
                        cap = Kit.art_button(grid, win["store"], "stop", Kit.ART_CLOSE, bx, y, "Stop",
                                             "Stop the trap, untrap or sort run", on_click=act("stop_all"))
                        win["stop_ctrls"] = [win["store"][0].get("stop"), cap]
                        win["side_status"] = label(grid, st["status_text"], bx, y + 26, Kit.HUE_INFO); show_stop()
                    elif kind == "quick": build_quick(grid, bx, y)
                    elif kind == "tools": build_tools(grid, bx, y)
                    elif kind == "break": grid.Add(Kit.inert(box(bx, y + h // 2, SIDE_BTN_W, 1, C_SEAM, 0.8)))
                    y += h + SIDE_GAP
            add_bare_button(grid, x0 + pw - SIDE_RIM - BARE_PAD - tw, y0 + ph - SIDE_RIM - BARE_PAD - th, False)
            return pw, ph
        def attached(): return st["attach"] is not None
        def bare_on(): return st["bare"] and not st["minimized"] and not attached()
        def layout_gump():
            return win.get("grid") if attached() or st["canvas"] == "alone" or bare_on() else win.get("bar")
        def layout_state():
            if st["shutting"] or st["wait_player"] or not Kit.is_open(win.get("grid")): return None
            return "docked" if st["docked"] else ("minimized" if st["minimized"] else "open")
        def layout_fit(w, h, mode):
            new = (None, None); geom = st["geom"]
            if not attached():
                told = (int(w), int(h)) if (w is not None and h is not None) else None
                if (canvas_ok() and (told != fitov["told"] or (mode == "again" and told is not None))):
                    st["dirty_frame"] = True
                fitov["told"] = told
                if canvas_ok() and told is not None: return
            if w is not None and h is not None and geom is not None:
                cols_now, cw_now, ch_now, gap = geom; gw_now = cols_now * cw_now + (cols_now - 1) * gap
                gap = 0 if trimming() else LOOSE_GAP
                extra = max(0, (st["grid_wh"][0] if st["grid_wh"] else gw_now) - gw_now)
                if attached(): extra = 0 if side_off() else gap + side_width(int(h))
                aw = int(w) - extra; ah = int(h) - top_off(); cw, ch = st["cell_w"], st["cell_h"]
                n = max(1, st["slots"]); best = None
                for c in range(1, n + 1):
                    r = int(math.ceil(n / float(c))); fw = (aw - (c - 1) * gap) // c; fh = (ah - (r - 1) * gap) // r
                    if fw < cw or fh < ch: continue
                    k = min(fw / float(cw), fh / float(ch))
                    if best is None or k > best[0]: best = (k, c, fw, fh)
                if best is None:
                    c = max(1, min(n, (aw + gap) // max(1, cw + gap))); r = int(math.ceil(n / float(c)))
                    best = (0, c, max(cw, (aw - (c - 1) * gap) // c), max(ch, (ah - (r - 1) * gap) // r))
                new = (best[1], (best[2], best[3]))
            if new != (fitov["cols"], fitov["cell"]): fitov["cols"], fitov["cell"] = new; st["dirty_frame"] = True
        def bag_cell(tall=None):
            gap = 0 if trimming() else LOOSE_GAP; area = fitov.get("area")
            if tall is None and area is not None: tall = area[1]
            side = 0 if side_off() else (st["side_pw"] if tall is None else gap + side_width(int(tall)))
            cur = int(round(H.scale * 100)) if R.ok else st["scale_pct"]
            own = st["scale_pct"] if shrink["pct"] is not None else cur
            floor = SHRINK_MIN if (R.ok and not H.disabled) else own
            if shrink["pct"] is None or cur == own:
                st["own_cell"] = (st["cell_w"], st["cell_h"], st["slots"])
                cw, ch = float(st["cell_w"]), float(st["cell_h"])
            else:
                oc = st["own_cell"]
                if oc is not None and oc[2] == st["slots"]: cw, ch = float(oc[0]), float(oc[1])
                else: f = own / float(max(1, cur)); cw, ch = st["cell_w"] * f, st["cell_h"] * f
            return cw, ch, gap, st["slots"], side, own, own, min(floor, own)
        ROOM_MEMO = {}
        def side_width(h):
            k = ("sw", h); v = ROOM_MEMO.get(k)
            if v is None:
                tw, th = bare_btn_size(); cols, _h = side_columns(h - th - BARE_PAD)
                v = len(cols) * SIDE_COL_W + 2 * SIDE_RIM
                if len(ROOM_MEMO) >= 200: ROOM_MEMO.clear()
                ROOM_MEMO[k] = v
            return v
        def canvas_ok(): return R.ok and R.can_ok and not H.disabled
        def canvas_mode():
            if not canvas_ok() or st["minimized"] or st["docked"] or st["shutting"]: return None
            if attached(): return None if fitov["area"] is None or not st["attach"].get("shown", True) else "combined"
            return "alone" if fitov["told"] is not None and HOST.layout_holds(KEY) else None
        CANVAS_MIN_W = 120
        def title_buttons(): return [("Settings",), ("Trap bags",), ("Slots",)]
        def title_fits(w):
            k = ("tf", w, st["slots"]); v = ROOM_MEMO.get(k)
            if v is None:
                plan = Kit.title_plan(w, TITLE, title_buttons(), str(st["slots"]))
                v = len(plan[3]) == len(title_buttons()) and \
                    plan[4] >= Kit.MARGIN + 30 + Kit.text_w("..") + Kit.TITLE_GAP
                if len(ROOM_MEMO) >= 200: ROOM_MEMO.clear()
                ROOM_MEMO[k] = v
            return v
        def canvas_room(mode):
            if mode == "combined":
                a = fitov["area"]; side = 0 if side_off() else side_width(a[1])
                return 0, 0, max(1, a[0] - side), max(1, a[1]), side
            w, h = fitov["told"]; M = Kit.MARGIN
            if st["bare"] or not title_fits(w): return M, M, max(1, w - 2 * M), max(1, h - 2 * M), 0
            top = M + 30 + Kit.GAP; ch = max(1, h - top - M); side = side_width(ch)
            if w - 2 * M - side < CANVAS_MIN_W: side = 0
            return M, top, max(1, w - 2 * M - side), ch, side
        def bounds_of(g, graphic=None):
            if graphic is None: graphic = int(g.Graphic)
            b = H.bounds.get(graphic)
            if b is None:
                r = R.f_data.GetValue(g).Bounds; b = (int(r.X), int(r.Y), int(r.Width), int(r.Height))
                H.bounds[graphic] = b
            return b
        def is_board(g, graphic): return gump_info(g)[1] or graphic in BOARDS
        def split_input():
            out = []; seen = set()
            for idx, serial in st["layout"]:
                if serial in seen: continue
                seen.add(serial); g = H.gumps.get(serial); kind, graphic = "closed", 0
                try:
                    if g is not None and not g.IsDisposed:
                        gi = H.ginfo.get(g); graphic = gi[0] if gi is not None else int(g.Graphic)
                        if is_board(g, graphic): kind = "board"
                        elif g.IsMinimized: kind = "mini"
                        else: bounds_of(g, graphic); kind = "open"
                except Exception: kind, graphic = "closed", 0
                out.append((idx, graphic, kind, serial))
            return tuple(out)
        def split_weights(items):
            out = []
            for slot, graphic, kind, _bag in items:
                b = H.bounds.get(graphic) if kind == "open" else None
                w, h = (max(1, b[2] - b[0]), max(1, b[3] - b[1])) if b is not None else (CLOSED_W, CLOSED_H)
                out.append((slot, float(w * h), w / float(h)))
            return out
        def split_dp(ws, W, H_):
            n = len(ws); S = sum(x[1] for x in ws); pa, pal, pall, pA = [0.0], [0.0], [0.0], [0.0]
            for slot, a, r in ws:
                A = W * H_ * a / S; L = math.log(A / r); pa.append(pa[-1] + a); pal.append(pal[-1] + a * L)
                pall.append(pall[-1] + a * L * L); pA.append(pA[-1] + A)
            inf = float("inf"); best = [0.0] + [inf] * n; back = [0] * (n + 1)
            for k in range(1, n + 1):
                bk, jk = inf, 0
                for j in range(k):
                    h = (pA[k] - pA[j]) / W
                    if h <= 0: continue
                    lh = 2.0 * math.log(h)
                    c = best[j] + (pall[k] - pall[j]) - 2.0 * lh * (pal[k] - pal[j]) + lh * lh * (pa[k] - pa[j])
                    if c < bk: bk, jk = c, j
                best[k], back[k] = bk, jk
            breaks = []; k = n
            while k > 0: breaks.append(k); k = back[k]
            breaks.reverse(); return best[n], breaks
        def split_cost(ws, W, H_, breaks):
            S = sum(x[1] for x in ws); c, j = 0.0, 0
            for k in breaks:
                area = sum(W * H_ * ws[i][1] / S for i in range(j, k)); h = area / W
                if h <= 0: return float("inf")
                for i in range(j, k): w = (W * H_ * ws[i][1] / S) / h; c += ws[i][1] * math.log((w / h) / ws[i][2]) ** 2
                j = k
            return c
        def split_plan(ws, W, H_, keep=None):
            if not ws: return "rows", [], 0.0
            cr, br = split_dp(ws, W, H_); wsT = [(s, a, 1.0 / r) for s, a, r in ws]; cc, bc = split_dp(wsT, H_, W)
            best = ("columns", bc, cc) if cc < COLUMNS_BEAT * cr else ("rows", br, cr)
            if keep is not None and keep[1] and keep[1][-1] == len(ws):
                o, b = keep; kc = split_cost(ws, W, H_, b) if o == "rows" else split_cost(wsT, H_, W, b)
                if not best[2] < (1.0 - SPLIT_KEEP) * kc: return o, list(b), kc
            return best
        def split_pixels(ws, W, H_, orient, breaks):
            if not ws: return {}
            if orient == "columns":
                return dict((s, (y, x, h, w)) for s, (x, y, w, h) in split_pixels(ws, H_, W, "rows", breaks).items())
            S = sum(x[1] for x in ws); out = {}; j, cum_rows, y0 = 0, 0.0, 0; n = len(ws)
            for k in breaks:
                row = sum(W * H_ * ws[i][1] / S for i in range(j, k)); cum_rows += row
                y1 = int(round(cum_rows / W)) if k < n else H_; cum, x0 = 0.0, 0
                for i in range(j, k):
                    cum += W * H_ * ws[i][1] / S; x1 = int(round(W * cum / row)) if i < k - 1 else W
                    out[ws[i][0]] = (x0, y0, x1 - x0, y1 - y0); x0 = x1
                y0 = y1; j = k
            return out
        def client_clamp(b, aw, ah, cs, x, y):
            bw = b[2] - int(aw / cs); bh = b[3] - int(ah / cs)
            if x < b[0]: x = b[0]
            elif x > bw: x = bw
            if y < b[1]: y = b[1]
            elif y > bh: y = bh
            return x, y
        def has_line(reg): return reg[2] >= LABEL_MIN_W and reg[3] >= LABEL_MIN_H + LABEL_LINE_H
        def item_box(reg):
            if has_line(reg): rx, ry, rw, rh = reg; return rx, ry + LABEL_LINE_H, rw, rh - LABEL_LINE_H
            return reg
        def art_units(aw, ah, cs): return (float(aw), float(ah)) if CANVAS.get("si") else (aw / cs, ah / cs)
        def centre_range(box, pw, ph):
            bx_, by_, bw, bh = box; xl, xh = bx_ + pw // 2, bx_ + bw - 1 - (pw - pw // 2)
            yl, yh = by_ + ph // 2, by_ + bh - 1 - (ph - ph // 2)
            if xh < xl: xl = xh = bx_ + bw // 2
            if yh < yl: yl = yh = by_ + bh // 2
            return xl, xh, yl, yh
        def bag_to_canvas(b, box, aw, ah, cs, bx, by):
            uw, uh = art_units(aw, ah, cs); sw, sh = float(max(1, b[2] - b[0])), float(max(1, b[3] - b[1]))
            u = 0.5 if uw >= sw else (bx + uw / 2.0 - b[0]) / sw; v = 0.5 if uh >= sh else (by + uh / 2.0 - b[1]) / sh
            u = 0.0 if u < 0 else (1.0 if u > 1 else u); v = 0.0 if v < 0 else (1.0 if v > 1 else v)
            return box[0] + u * box[2], box[1] + v * box[3]
        def canvas_to_bag(b, box, aw, ah, cs, px, py):
            uw, uh = art_units(aw, ah, cs); u = (px - box[0]) / float(max(1, box[2]))
            v = (py - box[1]) / float(max(1, box[3])); u = 0.0 if u < 0 else (1.0 if u > 1 else u)
            v = 0.0 if v < 0 else (1.0 if v > 1 else v); bx = int(round(b[0] + u * (b[2] - b[0]) - uw / 2.0))
            by = int(round(b[1] + v * (b[3] - b[1]) - uh / 2.0)); return bx, by
        def pic_size(aw, ah):
            if CANVAS.get("si"): cs = H.scale or 1.0; return max(1, int(aw * cs)), max(1, int(ah * cs))
            return aw, ah
        def spot_ctx(slot):
            reg = CANVAS["regions"].get(slot); info = CANVAS["kinds"].get(slot)
            if reg is None or info is None: return None
            return info[2], item_box(reg), H.bounds.get(info[1]), H.scale or 1.0
        def item_spot(ctx, serial, aw, ah, pw, ph, bx, by):
            if ctx is None: return 0, 0
            bag, box, b, cs = ctx; pin = PIN.get(serial)
            if pin is not None and pin[0] == bag and pin[1] == bx and pin[2] == by:
                return int(pin[3]) - pw // 2, int(pin[4]) - ph // 2
            cl_x, ch_x, cl_y, ch_y = centre_range(box, pw, ph)
            if b is None: cx, cy = (cl_x + ch_x) // 2, (cl_y + ch_y) // 2
            else:
                cx, cy = bag_to_canvas(b, box, aw, ah, cs, bx, by); cx = max(cl_x, min(ch_x, cx))
                cy = max(cl_y, min(ch_y, cy))
            return int(round(cx)) - pw // 2, int(round(cy)) - ph // 2
        def pin_set(serial, bag, bx, by, cx, cy):
            if serial not in PIN:
                if len(PIN_ORDER) >= PIN_CAP:
                    for s in PIN_ORDER[:PIN_CAP // 2]: PIN.pop(s, None)
                    del PIN_ORDER[:PIN_CAP // 2]
                PIN_ORDER.append(serial)
            PIN[serial] = (bag, bx, by, cx, cy)
        def pins_drop(): PIN.clear(); del PIN_ORDER[:]
        def scale_items_now():
            now = time.time()
            if now >= CV["prof_at"]:
                CV["prof_at"] = now + 1.0
                try: st["scale_items"] = bool(R.p_profile.GetValue(None).ScaleItemsInsideContainers)
                except Exception: pass
            return st["scale_items"]
        def canvas_publish(sig, items, ws, W, H_, plan):
            orient, breaks, _cost = plan; new = split_pixels(ws, W, H_, orient, breaks); kinds, slot_of = {}, {}
            for slot, graphic, kind, bag in items: kinds[slot] = (kind, graphic, bag); slot_of[bag] = slot
            CANVAS.update({"ver": CANVAS["ver"] + 1, "regions": new, "slot_of": slot_of,
                           "order": [i[0] for i in items], "orient": orient,
                           "breaks": list(breaks), "sig": sig, "items": items, "kinds": kinds,
                           "size": (W, H_), "si": sig[4]})
            pins_drop()
        def dragging():
            try: return item_hold() is not None
            except Exception: return False
        def canvas_set(mode):
            if st["canvas"] is not None: canvas_leave()
            st["canvas"] = mode; H.placed.clear(); st["dirty_frame"] = True
        def canvas_tick():
            mode = canvas_mode()
            if mode != st["canvas"]:
                if dragging(): return
                canvas_set(mode)
            if mode is None: return
            room = canvas_room(mode); items = split_input()
            sig = (room[2], room[3], items, round(H.scale or 1.0, 4), scale_items_now()); done = PLAN["done"]
            if done is not None and len(done) > 1 and done[0] == sig and CANVAS["job"] == sig:
                if dragging(): return
                canvas_publish(*done); CANVAS["job"] = None; CANVAS["pending"] = None; return
            if sig == CANVAS["sig"]: CANVAS["job"] = None; CANVAS["pending"] = None; return
            if sig == CANVAS["job"] or dragging(): return
            W, H_ = room[2], room[3]; ws = split_weights(items); keep = None
            if CANVAS["items"] == items and CANVAS["breaks"] is not None: keep = (CANVAS["orient"], CANVAS["breaks"])
            if CANVAS["slow"]: CANVAS["job"] = sig; CANVAS["pending"] = (sig, items, ws, W, H_, keep); return
            t0 = time.time(); plan = split_plan(ws, W, H_, keep)
            if time.time() - t0 > SPLIT_SLOW and len(ws) > 8: CANVAS["slow"] = True
            canvas_publish(sig, items, ws, W, H_, plan)
        def canvas_wanted():
            job, done = CANVAS.get("pending"), PLAN["done"]
            return job is not None and (done is None or done[0] != job[0])
        def canvas_thread():
            job = CANVAS.get("pending")
            if job is None or not canvas_wanted(): return
            sig, items, ws, W, H_, keep = job
            try: PLAN["done"] = (sig, items, ws, W, H_, split_plan(ws, W, H_, keep))
            except Exception: PLAN["done"] = (sig,)
        def canvas_detach():
            c = CV["ctrl"]
            if c is None: return
            with Kit.quiet:
                p = c.Parent
                if p is not None: detach(p, c)
        def canvas_place(raw, index, x, y, w, h):
            c = CV["ctrl"]
            if c is None or c.IsDisposed:
                canvas_clear(); c = new_ctl(R.Canvas)
                c.AcceptMouseInput = True; c.Priority = R.LowPriority; CV["ctrl"] = c
            c.va_wh = (int(w), int(h)); c.Parent = raw; kids = raw.Children
            while kids.Contains(c): kids.Remove(c)
            kids.Insert(min(index, kids.Count), c); R.f_bounds.SetValue(c, R.Rect(int(x), int(y), int(w), int(h)))
            CV["rect"] = (int(x), int(y), int(w), int(h))
            for lay in CV["layers"].values(): R.f_bounds.SetValue(lay, R.Rect(0, 0, int(w), int(h)))
        def canvas_clear():
            CV.update({"built": -1, "bsize": None, "parts": [], "icons": [], "bg": None,
                       "layers": {}, "pool": {}, "owner": {}, "items": {}, "seen_n": {},
                       "seen_last": {}, "seen_min": {}, "spot": {}, "label": {}, "count": {},
                       "tip": None, "sums": {}, "say_lbl": None, "sum_part": None, "alpha_set": None,
                       "say_shown": False})
        canvas_clear()
        def canvas_leave():
            canvas_detach(); c = CV["ctrl"]; CV["ctrl"] = None
            if c is not None: safe(c.Dispose)
            canvas_clear(); CV["rect"] = None; pins_drop()
            CANVAS.update({"sig": None, "items": None, "breaks": None, "regions": {},
                           "kinds": {}, "slot_of": {}, "order": [], "job": None, "pending": None, "size": None})
            CANVAS["ver"] += 1; win["counts"] = []; win["count_state"] = {}
        def canvas_alpha():
            a = st["opacity"]; bg = CV["bg"]; want = (a, bg)
            if CV["alpha_set"] == want: return
            for ic in ([bg] if bg is not None else []) + CV["icons"]:
                with Kit.quiet:
                    if abs(float(ic.Alpha) - a) > 0.001: ic.Alpha = a
            CV["alpha_set"] = want
        def into_canvas(w):
            raw = raw_of(w) if w is not None else None
            if raw is None: return None
            raw.Parent = CV["ctrl"]; raw.AcceptMouseInput = False; return raw
        def canvas_parts():
            c = CV["ctrl"]; grid = win.get("grid")
            if c is None or grid is None: return
            for p in CV["parts"]:
                with Kit.quiet: detach(c, p); p.Dispose()
            CV["parts"], CV["icons"], CV["label"], CV["count"] = [], [], {}, {}; CV["tip"] = None
            CV["alpha_set"] = None; lbl = CV["say_lbl"]; CV["say_lbl"] = None
            if lbl is not None: safe(lbl.Dispose)
            W, H_ = CANVAS["size"] or (CV["rect"][2], CV["rect"][3])
            regions, kinds = CANVAS["regions"], CANVAS["kinds"]; made = []
            made.append((Kit.add_tiled(grid, Kit.SECTION_TILE, 0, 0, W, H_, st["opacity"]), "bg"))
            for slot in CANVAS["order"]:
                x, y, w, h = regions[slot]
                if x + w < W: made.append((box(x + w - 1, y, 1, h, C_SEAM, 0.8), "seam"))
                if y + h < H_: made.append((box(x, y + h - 1, w, 1, C_SEAM, 0.8), "seam"))
            for slot in CANVAS["order"]:
                kind, graphic, bag = kinds[slot]
                if kind != "mini": continue
                g = H.gumps.get(bag)
                try: icon = int(R.f_data.GetValue(g).IconizedGraphic) or DEFAULT_ICONS[1]
                except Exception: icon = DEFAULT_ICONS[1]
                x, y, w, h = regions[slot]; iw, ih = Kit.pic_size(icon); iw, ih = (iw or 30), (ih or 30)
                made.append((Kit.add_pic(grid, icon, x + (w - iw) // 2, y + (h - ih) // 2, mouse=False), "icon"))
            for slot in CANVAS["order"]: made.extend(region_labels(grid, slot, regions[slot], kinds[slot]))
            if not CANVAS["order"]:
                for i, line in enumerate(Kit.wrap("No bags yet. Click Slots to add some.", max(60, W - 16))[:3]):
                    made.append((Kit.add_label(grid, line, 8, 8 + 20 * i, Kit.HUE_INFO), "lbl"))
            counts = []
            for idx in range(st["slots"]):
                cnt = Kit.add_label(grid, "", 0, 0, Kit.HUE_GOOD); Kit.set(cnt, "IsVisible", False)
                r = regions.get(idx); counts.append((cnt, r[0], r[1], r[2], r[3]) if r else (cnt, 0, 0, 0, 0))
                made.append((cnt, "count"))
            Kit.flush(); layers_at = len([m for m in made if m[1] != "count"]); parts = []
            for w, kind in made:
                raw = into_canvas(w)
                if raw is None: continue
                parts.append(raw)
                if kind == "bg": CV["bg"] = raw
                elif kind == "icon": raw.Alpha = st["opacity"]; CV["icons"].append(raw)
            CV["parts"] = parts; old = CV["layers"]; keep = {}
            for slot in CANVAS["order"]:
                lay = old.pop(slot, None)
                if lay is None or lay.IsDisposed: lay = new_ctl(R.Layer); lay.AcceptMouseInput = False
                R.f_bounds.SetValue(lay, R.Rect(0, 0, int(W), int(H_))); keep[slot] = lay
            if old:
                gone = list(old.values()); pool = CV["pool"]; drop = []
                for s in CV["owner"]:
                    pc = pool.get(s)
                    if pc is not None:
                        par = pc.Parent
                        for lay in gone:
                            if par is lay: drop.append(s); break
                for s in drop: item_drop(s)
                for lay in gone: safe(lay.Dispose)
            CV["layers"] = keep; kids = c.Children
            order = parts[:layers_at] + [keep[s] for s in CANVAS["order"]] + parts[layers_at:]
            for ctl in order: ctl.Parent = c
            in_order = set(order)
            for ctl in list(kids):
                if ctl not in in_order: kids.Remove(ctl)
            win["counts"] = counts; win["count_state"] = {}; CV["built"] = CANVAS["ver"]; CV["bsize"] = (W, H_)
            CV["seen_n"], CV["seen_last"], CV["seen_min"] = {}, {}, {}
            for slot in CANVAS["order"]:
                kind, graphic, bag = kinds[slot]; g = H.gumps.get(bag)
                if g is not None and kind in ("open", "mini"): canvas_resync(bag, g)
                elif CV["items"].get(bag):
                    for s in list(CV["items"][bag]): item_drop(s)
                    CV["items"][bag] = []
            if SR["counts"]: show_counts()
        def region_labels(grid, slot, reg, info):
            kind, graphic, bag = info; x, y, w, h = reg
            if w < LABEL_MIN_W or h < LABEL_MIN_H: return []
            if kind == "open" and not has_line(reg): return []
            out = []; tag = "#%d" % (slot + 1)
            out.append((Kit.add_label(grid, tag, x + 5, y + 3, Kit.HUE_TITLE), "lbl")); nx = x + 5 + Kit.text_w(tag) + 6
            if kind == "board":
                name = Kit.fit("Game board", max(8, x + w - 4 - nx))
                out.append((Kit.add_label(grid, name, nx, y + 3, Kit.HUE_INFO), "lbl")); return out
            whole = bag_name(bag, False)
            room = x + w - nx - (6 + Kit.text_w(COUNT_DIGITS) if kind == "open" else 0) - 10
            name = Kit.fit(whole, max(8, room)); plain = whole.rsplit(" [", 1)[0]
            if name != whole and plain != whole and Kit.text_w(plain) <= max(8, room): name = plain
            out.append((Kit.add_label(grid, name, nx, y + 3, Kit.HUE_INFO), "lbl"))
            CV["label"][slot] = (whole, name != whole)
            if kind == "open":
                n = len(CV["items"].get(bag) or ())
                cnt = Kit.add_label(grid, str(n), nx + Kit.text_w(name) + 6, y + 3, Kit.HUE_INFO)
                CV["count"][bag] = cnt; out.append((cnt, "lbl"))
            elif h >= LABEL_TWO_H:
                out.append((Kit.add_label(grid, "Minimized" if kind == "mini" else "Closed",
                                          x + 5, y + 3 + LABEL_PITCH, Kit.HUE_INFO), "lbl"))
            return out
        def world_of(g):
            w = CV["world"]
            if w is None:
                try: w = CV["world"] = g.World
                except Exception: w = None
            return w
        def world_item(g, serial):
            w = world_of(g)
            try: return w.Get(UInt32(int(serial))) if w is not None else None
            except Exception: return None
        def art_of(ctl, graphic):
            r = R.f_bounds.GetValue(ctl); a = (int(r.Width), int(r.Height))
            if graphic not in CV["art"]:
                if len(CV["art"]) > 2000: CV["art"].clear()
                CV["art"][graphic] = a
            return a
        def art_size(graphic):
            a = CV["art"].get(graphic)
            if a is not None: return a
            g = st["grid_raw"]
            try: probe = R.CanvasItem(g, UInt32(0), UInt16(int(graphic)), UInt16(0), 0, 0, False)
            except Exception: return 44, 44
            try: return (1, 1) if probe.IsDisposed else art_of(probe, graphic)
            finally: safe(probe.Dispose)
        def item_drop(serial):
            c = CV["pool"].pop(serial, None); bag = CV["owner"].pop(serial, None); CV["spot"].pop(serial, None)
            if c is not None:
                try:
                    p = c.Parent
                    if p is not None: detach(p, c)
                    c.Dispose()
                except Exception: pass
            if bag is not None:
                lst = CV["items"].get(bag)
                if lst and serial in lst: lst.remove(serial)
        def canvas_resync(bag, g):
            kids = g.Children; n = kids.Count; mini = bool(g.IsMinimized); CV["seen_n"][bag] = n
            CV["seen_last"][bag] = kids[n - 1] if n else None; CV["seen_min"][bag] = mini
            slot = CANVAS["slot_of"].get(bag); lay = CV["layers"].get(slot) if slot is not None else None
            if lay is None: return
            want = []
            if not mini and CANVAS["kinds"][slot][0] == "open":
                for i in range(n):
                    ch = kids[i]
                    if isinstance(ch, R.ItemGump) and not ch.IsDisposed: want.append(ch)
            pool, owner = CV["pool"], CV["owner"]; old = CV["items"].get(bag) or []; new = []; ctrls = []
            w = world_of(g); ctx = spot_ctx(slot); si = CANVAS.get("si"); cs = H.scale or 1.0; spots = CV["spot"]
            mk, U32, U16 = R.CanvasItem, UInt32, UInt16; t = 0
            for ch in want:
                s = int(ch.LocalSerial); gr = int(ch.Graphic)
                try: it = w.Get(U32(s)) if w is not None else None
                except Exception: it = None
                hue = int(it.Hue) if it is not None else int(ch.Hue); c = pool.get(s)
                if c is not None and c.IsDisposed: item_drop(s); c = None
                if c is None:
                    try: c = mk(g, U32(s), U16(gr), U16(hue), 0, 0, False)
                    except Exception: continue
                    if c.IsDisposed: continue
                    c.va_art = art_of(c, gr); c.va_gr, c.va_hue, c.va_sz, c.va_xy = gr, hue, None, None; pool[s] = c
                elif c.va_gr != gr:
                    c.Graphic = U16(gr)
                    if c.IsDisposed: pool.pop(s, None); owner.pop(s, None); continue
                    c.va_art = art_of(c, gr); c.va_gr, c.va_sz = gr, None
                if c.va_hue != hue: c.Hue = U16(hue); c.va_hue = hue
                was = owner.get(s)
                if was is not None and was != bag:
                    lst = CV["items"].get(was)
                    if lst and s in lst: lst.remove(s)
                owner[s] = bag; aw, ah = c.va_art
                pw, ph = (max(1, int(aw * cs)), max(1, int(ah * cs))) if si else (aw, ah)
                if c.va_sz != (pw, ph):
                    r = R.f_bounds.GetValue(c)
                    if int(r.Width) != pw or int(r.Height) != ph:
                        R.f_bounds.SetValue(c, R.Rect(int(r.X), int(r.Y), pw, ph))
                    c.va_sz = (pw, ph)
                bx, by = (int(it.X), int(it.Y)) if it is not None else get_pos(ch)
                x, y = item_spot(ctx, s, aw, ah, pw, ph, bx, by)
                if c.va_xy != (x, y): move(c, x, y); c.va_xy = (x, y)
                spots[s] = (x + pw // 2, y); new.append(s); ctrls.append(c)
                if it is None: t += s
                else:
                    try: am = int(it.Amount)
                    except Exception: am = 0
                    t = (t * 31 + s * 7 + bx * 131 + by * 137 + hue * 139 + am * 149) & 0x7FFFFFFF
            if old:
                in_new = set(new)
                for s in list(old):
                    if s not in in_new and owner.get(s) == bag: item_drop(s); PIN.pop(s, None)
            CV["items"][bag] = new; lk = lay.Children; same = lk.Count == len(ctrls)
            if same:
                for i in range(len(ctrls)):
                    if lk[i] is not ctrls[i]: same = False; break
            if not same:
                for c in ctrls: c.Parent = lay
                keep = set(ctrls)
                for c in list(lk):
                    if c not in keep: lk.Remove(c)
            cnt = CV["count"].get(bag)
            if cnt is not None: Kit.set_text(cnt, str(len(new)))
            CV["sums"][bag] = t
        def bag_sum(g, serials, t=0):
            w = world_of(g); U32 = UInt32
            for s in serials:
                try: it = w.Get(U32(int(s))) if w is not None else None
                except Exception: it = None
                if it is None: t += s; continue
                t = (t * 31 + s * 7 + int(it.X) * 131 + int(it.Y) * 137 + int(it.Hue) * 139
                     + int(it.Amount) * 149) & 0x7FFFFFFF
            return t
        SAFETY_EVERY = 0.2; SAFETY_CHUNK = 30; POKE_GAP = 0.1; POKE_CAP = 40
        def on_bag_item(*args):
            pk = CV["poked"]
            if st["shutting"] or len(pk) >= POKE_CAP: return
            slots = CANVAS.get("slot_of", ())
            for a in args:
                try: s, c = int(a.Serial), int(a.Container)
                except Exception: continue
                for k in (c, s):
                    if k in slots: pk.add(k)
                return
        def canvas_safety():
            now = time.time(); pk = CV["poked"]
            if pk and now >= CV["poke_at"]:
                CV["poke_at"] = now + POKE_GAP; todo = list(pk); pk.difference_update(todo)
                for bag in todo:
                    g = H.gumps.get(bag)
                    if g is not None and not g.IsDisposed: canvas_resync(bag, g)
            order = CANVAS["order"]
            if not order: return
            if 0 <= CV["sum_at"] - now <= SAFETY_EVERY: return
            CV["sum_at"] = now + SAFETY_EVERY; part = CV["sum_part"]
            if part is not None:
                bag, g, src, n, lst, i, t = part
                if CV["items"].get(bag) is not src or len(src) != n or g.IsDisposed or H.gumps.get(bag) is not g:
                    part = None; CV["sum_part"] = None
            if part is None:
                i = CV["sum_i"] % len(order); CV["sum_i"] = i + 1; kind, graphic, bag = CANVAS["kinds"][order[i]]
                if kind != "open": return
                g = H.gumps.get(bag)
                if g is None or g.IsDisposed: return
                src = CV["items"].get(bag); lst = tuple(src) if src else ()
                n, i, t = len(src) if src is not None else -1, 0, 0
            end = i + SAFETY_CHUNK
            if end < len(lst): CV["sum_part"] = (bag, g, src, n, lst, end, bag_sum(g, lst[i:end], t)); return
            CV["sum_part"] = None
            if bag_sum(g, lst[i:], t) != CV["sums"].get(bag): canvas_resync(bag, g)
        def canvas_hue(serial, hue):
            c = CV["pool"].get(serial)
            if c is None: return
            h = int(hue) & 0xFFFF
            try:
                if not c.IsDisposed and c.va_hue != h: c.Hue = UInt16(h); c.va_hue = h
            except Exception: pass
        def region_at(x, y):
            for slot in CANVAS["order"]:
                r = CANVAS["regions"].get(slot)
                if r is not None and r[0] <= x < r[0] + r[2] and r[1] <= y < r[1] + r[3]: return slot
            return None
        def tile_of(graphic):
            arr = CV["tiles"]
            if arr is None:
                if R.f_tiles is None: return None
                arr = CV["tiles"] = R.f_tiles.GetValue(None)
            return None if arr is None or graphic < 0 or graphic >= arr.Length else arr[graphic]
        def takes_drop(it, hold):
            try: gr = int(it.Graphic)
            except Exception: return True
            if gr in STACK_ON: return True
            t = tile_of(gr)
            if t is None: return True
            try: return True if bool(t.IsContainer) else bool(t.IsStackable) and gr == int(Tz.get(hold, "Graphic"))
            except Exception: return True
        def bag_window_up(serial, button):
            bag = CV["owner"].get(serial); g = H.gumps.get(bag) if bag is not None else None
            if g is None or g.IsDisposed: return False
            g.OnMouseUp(0, 0, button); return True
        def in_reach(bag):
            g = H.gumps.get(bag); w = world_of(g) if g is not None else CV["world"]
            if w is None: return True
            try:
                it = w.Get(UInt32(int(bag)))
                if it is None: return True
                root = w.Get(it.RootContainer); return root is None or int(root.Distance) <= DRAG_RANGE
            except Exception: return True
        def cant(): API.PlaySound(SOUND_CANT)
        def canvas_mouse_up(x, y, button):
            b = str(button); up = R.up_item; R.up_item = None
            up_s = int(up.LocalSerial) if up is not None and not up.IsDisposed else None
            if b == "Left":
                hold = item_hold()
                if hold is not None:
                    if up_s is not None:
                        it = world_item(H.gumps.get(CV["owner"].get(up_s)), up_s)
                        if it is not None and takes_drop(it, hold): return bag_window_up(up_s, button)
                    slot = region_at(x, y)
                    if slot is None: return True
                    canvas_drop(slot, x, y, hold); return True
                if st["flt_pick"] is not None:
                    slot = region_at(x, y)
                    if slot is not None:
                        kinds = CANVAS["kinds"].get(slot); slots = dict((b, i) for i, b in st["layout"])
                        if kinds is not None and kinds[2] in slots:
                            act("filter_canvas_pick", slots[kinds[2]])(); return True
                if up_s is not None:
                    if not CV["texts"] and not API.HasTarget(): CV["said"] = (up_s, time.time())
                    return bag_window_up(up_s, button)
                slot = region_at(x, y)
                if slot is None: return False
                kind, graphic, bag = CANVAS["kinds"][slot]; r = CANVAS["regions"][slot]
                if kind == "open" and has_line(r) and y < r[1] + LABEL_LINE_H and not API.HasTarget():
                    act("bag_min", bag, True)(); return True
                return False
            if b == "Right":
                if up_s is not None: return True
                slot = region_at(x, y)
                if slot is not None and CANVAS["kinds"][slot][0] == "open":
                    act("bag_close", CANVAS["kinds"][slot][2])(); return True
            return False
        def canvas_drop(slot, x, y, hold):
            kind, graphic, bag = CANVAS["kinds"][slot]
            if not in_reach(bag): cant(); return
            hs = int(Tz.get(hold, "Serial"))
            if hs == bag: cant(); return
            import System; b = H.bounds.get(graphic) if kind == "open" else None
            if b is None:
                Tz.call(None, "DropItem", (System.UInt32(hs), 0xFFFF, 0xFFFF, 0,
                                           System.UInt32(int(bag)), False), R.Actions)
                return
            px, py = x, y
            with Kit.quiet:
                if bool(R.p_profile.GetValue(None).RelativeDragAndDropItems):
                    off = Tz.get(hold, "MouseOffset"); px, py = px + int(off.X), py + int(off.Y)
            aw, ah = art_size(int(Tz.get(hold, "DisplayedGraphic"))); pw, ph = pic_size(aw, ah); cs = H.scale or 1.0
            box = item_box(CANVAS["regions"][slot]); cl_x, ch_x, cl_y, ch_y = centre_range(box, pw, ph)
            cx = max(cl_x, min(ch_x, px)); cy = max(cl_y, min(ch_y, py))
            bx, by = canvas_to_bag(b, box, aw, ah, cs, cx, cy); sx, sy = client_clamp(b, aw, ah, cs, bx, by)
            Tz.call(None, "DropItem", (System.UInt32(hs), sx, sy, 0, System.UInt32(int(bag)), False), R.Actions)
            pin_set(hs, int(bag), sx, sy, cx, cy); safe(lambda: Tz.put(None, "CancelDoubleClick", True, R.Mouse))
        def canvas_double(x, y, button):
            if str(button) != "Left": return False
            slot = region_at(x, y)
            if slot is None: return False
            kind, graphic, bag = CANVAS["kinds"][slot]
            if kind in ("closed", "board"): act("bag_use", bag)(); return True
            if kind == "mini": act("bag_min", bag, False)(); return True
            return False
        TIPS = {"closed": "Double-click to open; drop an item to put it in",
                "mini": "Double-click to restore; drop an item to put it in",
                "board": "Double-click to open the board; drop an item to put it in",
                "body": "Right-click to close", "line": "Click to minimize"}
        def canvas_hover(c, x, y):
            slot = region_at(x, y); part = None
            if slot is not None:
                kind = CANVAS["kinds"][slot][0]; part = kind
                if kind == "open":
                    r = CANVAS["regions"][slot]; part = "line" if has_line(r) and y < r[1] + LABEL_LINE_H else "body"
            key = (slot, part, CANVAS["ver"])
            if key == CV["tip"]: return
            CV["tip"] = key; text = TIPS.get(part, "")
            if part == "line":
                lab = CV["label"].get(slot)
                if lab is not None and lab[1]: text = "%s. Click to minimize" % lab[0]
            c.SetTooltip(text)
        def bag_use(bag): API.UseObject(bag)
        def bag_min(bag, value):
            g = H.gumps.get(bag)
            if g is not None and not g.IsDisposed and bool(g.IsMinimized) != value: g.IsMinimized = value
        def bag_close(bag):
            g = H.gumps.get(bag)
            if g is not None and not g.IsDisposed: g.Dispose()
        def canvas_texts(batcher, sx, sy):
            try:
                spots = CV["spot"]; trs = H.gtr
                for slot in CANVAS["order"]:
                    info = CANVAS["kinds"][slot]
                    if info[0] != "open": continue
                    g = H.gumps.get(info[2])
                    if g is None: continue
                    tr = trs.get(g)
                    if tr is None:
                        tr = g.TextRenderer
                        if len(trs) >= GINFO_CAP: trs.clear()
                        trs[g] = tr
                    o = tr.DRight
                    if o is None: continue
                    while o is not None:
                        own = o.Owner
                        if not o.IsDestroyed and own is not None and o.TextBox is not None:
                            try: os_ = int(own.Serial or 0)
                            except Exception: os_ = 0
                            sp = spots.get(os_)
                            if sp is not None:
                                o.X, o.Y = sp[0], sp[1]; tw, th = get_size(o.TextBox)
                                o.RealScreenPosition = R.Point(sp[0] - (tw >> 1), sp[1] - int(o.OffsetY) - th)
                        o = o.DRight
                    tr.Draw(batcher, sx, sy, True)
            except Exception as e: CV["texts"] = False; H.error = "canvas texts: %s" % e
        SAY_SECS = 4.0; SAY_WAIT = 1.5
        def canvas_say_tick(now):
            if CV["texts"] or st["canvas"] is None: return
            lbl = CV["say_lbl"]; said = CV["said"]; rd = JR["rd"]
            if said is not None and rd is not None:
                serial, t0 = said
                for ln in rd.new():
                    if ln.at < t0 - 0.05 or ":" in ln.text[:24]: continue
                    sp = CV["spot"].get(serial); CV["said"] = None
                    if sp is None or CV["ctrl"] is None: break
                    if lbl is None:
                        grid = win.get("grid")
                        if grid is None: break
                        lbl = Kit.add_label(grid, "", 0, 0, Kit.HUE_TEXT); Kit.flush(); into_canvas(lbl)
                        CV["say_lbl"] = lbl
                    text = Kit.fit(ln.text, 200); Kit.set_text(lbl, text)
                    lbl.SetPos(max(0, sp[0] - Kit.text_w(text) // 2), max(0, sp[1] - 18)); lbl.IsVisible = True
                    CV["say_shown"] = True; CV["say_until"] = now + SAY_SECS; break
                else:
                    if now - t0 > SAY_WAIT: CV["said"] = None
            if lbl is not None and CV["say_shown"] and now >= CV.get("say_until", 0.0):
                CV["say_shown"] = False; Kit.set(lbl, "IsVisible", False)
        def item_hold():
            h = H.hold
            if h is None:
                game = Tz.get(None, "Game", Tz.T("ClassicUO.Client"))
                h = H.hold = Tz.get(Tz.get(game, "UO"), "GameCursor"); h = H.hold = Tz.get(h, "ItemHold")
            return None if not bool(Tz.get(h, "Enabled")) or bool(Tz.get(h, "IsFixedPosition")) else h
        shrink = {"pct": None}
        def scale_now():
            p = shrink["pct"]
            return (p, True) if p is not None and p < st["scale_pct"] else (st["scale_pct"], st["scale_items"])
        def note_shrunk():
            if shrink["pct"] is None: Kit.put_var(SHRINK_KEY, "")
            else: Kit.put_var(SHRINK_KEY, "%d|%d" % (st["scale_pct"], 1 if st["scale_items"] else 0))
        def bag_shrink(pct):
            if pct is not None and not (R.ok and not H.disabled and attached()): pct = None
            if pct is not None and canvas_ok(): pct = None
            if pct is not None and shrink["pct"] is None:
                got = safe(read_scale)
                if got: st["scale_pct"], st["scale_items"] = got
            if pct is not None:
                pct = max(SHRINK_MIN, int(pct))
                if pct >= st["scale_pct"]: pct = None
            if pct == shrink["pct"]: return
            was = shrink["pct"]; before = H.scale; shrink["pct"] = pct
            try: apply_scale(*scale_now())
            except Exception as e:
                shrink["pct"] = was; API.SysMsg(TITLE + ": couldn't change the bag scale (%s)." % e, HUE_ERR); return
            note_shrunk()
            if before > 0 and H.scale > 0:
                f = H.scale / before; st["cell_w"] = max(1, min(MAX_CELL, int(round(st["cell_w"] * f))))
                st["cell_h"] = max(1, min(MAX_CELL, int(round(st["cell_h"] * f))))
            st["fit_pending"] = True; frame_changed()
            if not (st["job"] or st["sort"]): set_status("Idle")
        def unshrink_left():
            raw = Kit.get_var(SHRINK_KEY)
            if not raw: return
            p = raw.split("|")
            try: pct, items = int(p[0]), (len(p) > 1 and p[1] == "1")
            except Exception: Kit.put_var(SHRINK_KEY, ""); return
            if R.ok and 50 <= pct <= 200:
                try: apply_scale(pct, items); st["scale_pct"], st["scale_items"] = pct, items
                except Exception: return
            Kit.put_var(SHRINK_KEY, "")
        def paperdoll_fit(w, h):
            area = (int(w), int(h)) if (w is not None and h is not None and attached()) else None
            if area is None:
                if fitov["area"] is not None:
                    fitov["area"] = None; layout_fit(None, None, None); st["dirty_frame"] = True
                return
            if area != fitov["area"]: fitov["area"] = area; layout_fit(area[0], area[1], "w"); st["dirty_frame"] = True
        def bag_pack(width, height):
            if not (canvas_ok() and attached()): return None
            side = 0 if side_off() else side_width(max(60, min(int(height), 1000))); aw = int(width) - side
            if aw < 40: return None
            tot = sum(a for _slot, a, _r in split_weights(split_input()))
            k = (st["scale_pct"] if shrink["pct"] is not None
                 else (int(round(H.scale * 100)) if R.ok else st["scale_pct"])) / 100.0
            need = max(80, int(math.ceil(tot * k * k / aw)))
            if int(height) < (1 << 19): need = min(need, max(1, int(height)))
            return None, need
        def side_off(): return st["side_hidden"] and not st["minimized"] and attached()
        def top_off(): return 0 if (bare_on() or attached()) else BAR_H
        def attach_raw():
            att = st["attach"]
            if att is None: return None
            raw = att.get("raw")
            if raw is None or raw.IsDisposed:
                raw = raw_of(att.get("g")) if R.ok else None; att["raw"] = raw
                if raw is not None: Kit.attach(win["grid"], att.get("g"))
            return raw
        def attach_to(info):
            if info is None and st["attach"] is not None:
                safe(lambda: bag_shrink(None))
                if fitov["area"] is not None: fitov["area"] = None; layout_fit(None, None, None)
                st["frame_x"], st["frame_y"] = st["saved_fx"], st["saved_fy"]; st["detached_at"] = time.time()
                H.bar_at = None
                for raw in (st["bar_raw"], st["grid_raw"]):
                    with Kit.quiet:
                        if raw is not None and not raw.IsDisposed: move(raw, st["frame_x"], st["frame_y"])
                for key in ("bar", "grid"):
                    g = win.get(key)
                    if Kit.is_open(g):
                        g.SetPos(st["frame_x"], st["frame_y"]); Kit.moved_by_code(g)
            elif info is not None:
                st["minimized"] = st["docked"] = False; set_dock_wish(False)
                with Kit.quiet:
                    lead = info.get("g")
                    if Kit.is_open(lead) and (info.get("dx") or info.get("dy")):
                        st["frame_x"] = int(lead.GetX()) + int(info.get("dx", 0))
                        st["frame_y"] = int(lead.GetY()) + int(info.get("dy", 0))
            st["attach"] = info; st["dirty_frame"] = True
        def bare_btn_size(): w, h = Kit.pic_size(ART_BARE[0]); return (w or 15), (h or 15)
        def add_bare_button(grid, x, y, strip=True):
            if strip: add_quick_strip(grid, x - 4, y + max(0, (bare_btn_size()[1] - QUICK_ICON) // 2))
            if attached():
                art, tip = Kit.ART_DOCK, ("Show the side panel" if st["side_hidden"] else "Hide the side panel")
            else:
                art, tip = ART_BARE, ("Show the title bar and side panel" if st["bare"]
                                      else "Bags only: hide the title bar and side panel")
            Kit.art_button(grid, win["store"], "bare", art, x, y, None, tip, on_click=act("toggle_bare"))
        def build_slots(grid, slot_raws, cols, cw, ch, gap, gw, gh, trim):
            fit = max(4, (cw - 8) // 7); area = fitov["area"] if attached() else None
            if area is not None:
                Kit.inert(Kit.add_tiled(grid, Kit.SECTION_TILE, 0, 0, area[0], area[1], Kit.SECTION_ALPHA))
            for idx in range(st["slots"]):
                r, c = divmod(idx, cols); x, y = c * (cw + gap), r * (ch + gap)
                drop = box(x, y, cw, ch, "#000000", 0.01)
                if bare_on(): Kit.set(drop, "CanMove", True)
                grid.Add(drop); Kit.add_tiled(grid, Kit.SECTION_TILE, x, y, cw, ch, st["opacity"])
                if trim:
                    if c < cols - 1: grid.Add(Kit.inert(box(x + cw - 1, y, 1, ch, C_SEAM, 0.8)))
                    if idx + cols < st["slots"]: grid.Add(Kit.inert(box(x, y + ch - 1, cw, 1, C_SEAM, 0.8)))
                else:
                    for bx, by, bw, bh in ((x, y, cw, 1), (x, y + ch - 1, cw, 1),
                                           (x, y, 1, ch), (x + cw - 1, y, 1, ch)):
                        grid.Add(Kit.inert(box(bx, by, bw, bh, C_EDGE, 0.9)))
                labs = [label(grid, "#%d" % (idx + 1), x + 5, y + 3, Kit.HUE_TITLE)]
                if idx in st["assign"]:
                    labs.append(label(grid, short(bag_name(st["assign"][idx], False), fit), x + 5, y + 21,
                                      Kit.HUE_INFO))
                    labs.append(label(grid, "Closed", x + 5, y + 39, Kit.HUE_INFO))
                else: labs.append(label(grid, short("Empty: click Slots", fit), x + 5, y + 21, Kit.HUE_INFO))
                slot_raws.append(tuple(raw_of(l) for l in labs) if R.ok else ())
                cnt = label(grid, "", x + 5, y + max(0, ch - 18), Kit.HUE_GOOD); Kit.set(cnt, "IsVisible", False)
                win["counts"].append((cnt, x, y, cw, ch))
            if area is not None:
                for idx in range(st["slots"], cols * int(math.ceil(st["slots"] / float(cols)))):
                    r, c = divmod(idx, cols)
                    Kit.inert(Kit.add_tiled(grid, Kit.SECTION_TILE, c * (cw + gap), r * (ch + gap), cw, ch,
                                           st["opacity"]))
            if trim:
                for bx, by, bw, bh in ((0, 0, gw, 1), (0, gh - 1, gw, 1), (0, 0, 1, gh), (gw - 1, 0, 1, gh)):
                    grid.Add(Kit.inert(box(bx, by, bw, bh, C_EDGE, 0.9)))
            if bare_on():
                kw, kh = Kit.pic_size(Kit.CORNER_ART); kw, kh = (kw or 30), (kh or 30); tw, th = bare_btn_size()
                kx, ky = gw - kw + GRIP_OUT, gh - kh + GRIP_OUT; Kit.inert(Kit.add_pic(grid, Kit.CORNER_ART, kx, ky))
                Kit.catcher(grid, kx, ky, kw, kh, lambda *a: None, "Drag to move the bags", movable=True)
                add_bare_button(grid, kx - tw - 3, gh + GEM_BELOW); total_w = kx + kw
                total_h = max(ky + kh, gh + GEM_BELOW + th)
                grid.SetRect(st["frame_x"], st["frame_y"], total_w, total_h)
                st["grid_wh"] = (total_w, total_h); return total_w
            if side_off():
                tw, th = bare_btn_size()
                if area is not None:
                    add_bare_button(grid, area[0] - tw - 2, area[1] - th - 2)
                    grid.SetRect(st["frame_x"], st["frame_y"], area[0], area[1]); st["grid_wh"] = area; return area[0]
                add_bare_button(grid, gw - tw, gh + GEM_BELOW); total_h = gh + GEM_BELOW + th
                grid.SetRect(st["frame_x"], st["frame_y"], gw, total_h); st["grid_wh"] = (gw, total_h); return gw
            pw, ph = build_side_panel(grid, gw + gap, gh); st["side_pw"] = gap + pw; total_w = gw + gap + pw
            if area is not None: total_w, ph = max(total_w, area[0]), max(ph, area[1])
            grid.SetRect(st["frame_x"], st["frame_y"] + top_off(), total_w, max(gh, ph))
            st["grid_wh"] = (total_w, max(gh, ph)); return total_w
        anch = {"outline": None, "told": False}
        def gump_rect(g):
            try:
                if g is None or g.IsDisposed: return None
                x, y = int(g.GetX()), int(g.GetY()); w, h = int(g.GetWidth() or 0), int(g.GetHeight() or 0)
            except Exception: return None
            return None if w <= 1 or h <= 1 else (x, y, w, h)
        def frame_outline():
            if st["minimized"] or st["docked"]: return None
            rects = []
            if not bare_on() and not attached() and st["canvas"] != "alone":
                r = gump_rect(win["bar"])
                if r is not None: rects.append(r)
            r = gump_rect(win["grid"])
            if r is not None: rects.append(r)
            if not rects: return None
            x0 = min(r[0] for r in rects); y0 = min(r[1] for r in rects); x1 = max(r[0] + r[2] for r in rects)
            y1 = max(r[1] + r[3] for r in rects); return x0, y0, x1 - x0, y1 - y0
        def anchors_capture():
            out = []; bar, grid = win["bar"], win["grid"]
            for g, leader in list(SNAP.links.items()):
                if (leader is bar or leader is grid) and leader is not None and Kit.is_open(g):
                    r = gump_rect(g)
                    if r is not None: out.append((g, r))
            return out
        def edge_pos(f0, f1, o0, o1, n0, n1):
            return n1 + (f0 - o1) if f0 >= o1 - 2 or (f1 > o0 + 2 and abs(f1 - o1) < abs(f0 - o0)) else n0 + (f0 - o0)
        def anchors_apply(followers):
            snap = SNAP; leader = win["grid"] if (bare_on() or attached() or st["canvas"] == "alone") else win["bar"]
            if leader is None: leader = win["grid"]
            Kit.flush(); new = frame_outline(); old = anch["outline"]
            if old is not None: old = (st["frame_x"] + old[0], st["frame_y"] + old[1], old[2], old[3])
            if new is not None: anch["outline"] = (new[0] - st["frame_x"], new[1] - st["frame_y"], new[2], new[3])
            moved_n = 0
            for g, (fx, fy, fw, fh) in followers:
                if leader is None or not Kit.is_open(g): continue
                snap.links[g] = leader
                if old is None or new is None or old == new: continue
                nx = edge_pos(fx, fx + fw, old[0], old[0] + old[2], new[0], new[0] + new[2])
                ny = edge_pos(fy, fy + fh, old[1], old[1] + old[3], new[1], new[1] + new[3])
                if (nx, ny) == (fx, fy): continue
                try: g.SetPos(int(nx), int(ny))
                except Exception: continue
                moved_n += 1
                with Kit.quiet:
                    if snap.last is not None: snap.last[g] = (nx, ny)
                    Kit.moved_by_code(g); snap.follow(g, nx - fx, ny - fy, set([g]))
                fn = snap.moved_cb.get(g)
                if fn is not None: safe(fn)
            if moved_n and not anch["told"]:
                anch["told"] = True
                API.SysMsg(TITLE + ": %s moved with the bags' edge." % Kit.count(moved_n, "snapped window"), HUE_INFO)
        def screen_dims(cols, rows, ch, gap):
            sh = Kit.screen()[1]
            if sh <= 0 or st["slots"] <= 1: return cols, rows
            fit_rows = max(1, (sh - top_off() - SCREEN_SLACK + gap) // (ch + gap))
            if rows <= fit_rows: return cols, rows
            c = int(math.ceil(st["slots"] / float(fit_rows))); return c, int(math.ceil(st["slots"] / float(c)))
        def build_window():
            followers = anchors_capture(); canvas_detach(); dispose("grid"); dispose("bar")
            win["quick_sig"] = quick_sig()
            if st["canvas"] is not None and canvas_mode() == st["canvas"]: build_canvas_frame(followers); return
            if fitov["area"] is not None and attached() and st["geom"] is not None:
                layout_fit(fitov["area"][0], fitov["area"][1], "w"); st["dirty_frame"] = False
            elif fitov["told"] is not None and not attached() and st["geom"] is not None:
                layout_fit(fitov["told"][0], fitov["told"][1], "w"); st["dirty_frame"] = False
            cols, rows = layout_dims(); trim = trimming(); gap = 0 if trim else LOOSE_GAP
            cw, ch = fitov["cell"] or (st["cell_w"], st["cell_h"])
            free = not attached() and st["canvas"] is None and fitov["told"] is None and not HOST.layout_locked(KEY)
            if free and not st["minimized"]: cols, rows = screen_dims(cols, rows, ch, gap)
            gw = cols * cw + (cols - 1) * gap; gh = rows * ch + (rows - 1) * gap; st["geom"] = (cols, cw, ch, gap)
            st["icons_used"] = H.icons or DEFAULT_ICONS
            win.update({"store": ({}, {}), "side_status": None, "search_box": None, "counts": [], "count_state": {}})
            bare = bare_on(); grid = G.CreateGump(bare, bare); win["grid_bare"] = bare
            st["grid_info"] = (raw_of(grid) if R.ok else None, bare); slot_raws = []
            if st["minimized"]: total_w = BAR_MIN_W; grid.SetRect(st["frame_x"], st["frame_y"] + BAR_H, 1, 1)
            else: total_w = build_slots(grid, slot_raws, cols, cw, ch, gap, gw, gh, trim)
            if free:
                pair_w = total_w if bare else max(total_w, BAR_MIN_W)
                pair_h = BAR_H if st["minimized"] else top_off() + (st["grid_wh"][1] if st["grid_wh"] else gh)
                nx, ny = Kit.clamp(st["frame_x"], st["frame_y"], pair_w, pair_h)
                if (nx, ny) != (st["frame_x"], st["frame_y"]):
                    st["frame_x"], st["frame_y"] = nx, ny
                    grid.SetPos(nx, ny + (BAR_H if st["minimized"] else top_off()))
            add_hook(grid, True); lay_under(grid); Kit.add_front(grid); win["grid"] = grid
            bar = make_bar(total_w, st["docked"] or bare or attached(), free)
            if attached(): st["attach_g"] = st["attach"].get("g"); Kit.attach(grid, st["attach_g"])
            elif bare: Kit.attach(bar, grid)
            else: Kit.attach(grid, bar)
            anchors_apply(followers); st["slot_raws"] = tuple(slot_raws)
            if SR["counts"]: show_counts()
            st["grid_raw"] = raw_of(grid) if R.ok else None; st["bar_raw"] = raw_of(bar) if R.ok else None
            if R.ok and not H.disabled and (st["grid_raw"] is None or st["bar_raw"] is None):
                H.error = "can't reach the client's own window controls"; H.disabled = True
        CLOSE_TIP = "Close " + TITLE + " (turns it off; gives every bag back)"
        SLOTS_TIP = "Open the bag manager: a bag per slot"; TRAPS_TIP = "Pick the bags Trap and Untrap cast on"
        def make_bar(total_w, hide, free=False):
            bar_w = max(total_w, BAR_MIN_W); bar = G.CreateGump(True, True)
            if free: Kit.place(bar, st["frame_x"], st["frame_y"], bar_w, BAR_H)
            else: bar.SetRect(st["frame_x"], st["frame_y"], bar_w, BAR_H)
            Kit.add_window_frame(bar, bar_w, BAR_H, corners=False); Kit.add_section(bar, 8, 8, bar_w - 16, BAR_H - 16)
            Kit.add_label(bar, TITLE.upper(), 18, 14, Kit.HUE_TITLE)
            Kit.add_label(bar, str(st["slots"]), 18 + Kit.text_w(TITLE.upper()) + 8, 14, Kit.HUE_INFO)
            store = win["store"]; x = bar_w - 12 - 30
            if Kit.zone_up(KEY): x += 20
            else:
                Kit.art_button(bar, store, "close", Kit.ART_CLOSE, x, 11, None, CLOSE_TIP, on_click=act("disable", KEY))
                x -= 20
                Kit.art_button(bar, store, "min", Kit.ART_RESTORE if st["minimized"] else Kit.ART_MIN, x, 14,
                               None, Kit.RESTORE_TIP if st["minimized"] else Kit.MIN_TIP, on_click=act("user_collapse"))
                Kit.dock_button(bar, store, x, 14, on_click=act("fold_to_bar")); x -= Kit.DOCK_DX
            for key, text, tip, fn in (("settings", "Settings", Kit.SETTINGS_TIP % TITLE,
                     act("show_settings", KEY)), ("traps", "Trap bags", TRAPS_TIP, act("open_win", "trp")),
                    ("bags", "Slots", SLOTS_TIP, act("open_win", "mgr"))):
                x -= 10 + 35 + Kit.text_w(text)
                Kit.art_button(bar, store, key, Kit.ART_PAGE, x, 11, text, tip, on_click=fn)
            Kit.title_catcher(bar, 8, 8, max(20, x - 14), BAR_H - 16, act("user_collapse"), key=KEY)
            if hide: bar.IsVisible = False
            Kit.add_front(bar); win["bar"] = bar; return bar
        wnd = None
        def refresh():
            if st["canvas"] is None or CV["ctrl"] is None or CANVAS["size"] is None: return
            if CV["built"] != CANVAS["ver"] or CV["bsize"] != CANVAS["size"]:
                if CV["rect"] is not None and (CV["rect"][2], CV["rect"][3]) != CANVAS["size"]: return
                if dragging(): return
                canvas_parts()
            canvas_alpha(); canvas_safety()
        def build_canvas_frame(followers):
            mode = st["canvas"]; alone = mode == "alone"; st["icons_used"] = H.icons or DEFAULT_ICONS
            win.update({"store": ({}, {}), "side_status": None, "search_box": None})
            x0, y0, cw, ch, side = canvas_room(mode); W, H_ = fitov["told"] if alone else fitov["area"]
            grid = G.CreateGump(alone, alone); win["grid_bare"] = alone; raw = raw_of(grid)
            if raw is None:
                Kit.dispose(grid); st["grid_raw"] = None; H.error = "can't reach the client's own window controls"
                H.disabled = True; return
            st["grid_info"] = (raw, alone)
            store = win["store"]; titled = alone and not st["bare"] and title_fits(W)
            if alone:
                Kit.add_window_frame(grid, W, H_)
                if titled:
                    Kit.title_bar(grid, store, W, TITLE, KEY, act("user_collapse"), act("fold_to_bar"),
                                  act("show_settings", KEY), close_tip=CLOSE_TIP,
                                  extra=[("traps", Kit.ART_PAGE, "Trap bags", TRAPS_TIP, act("open_win", "trp")),
                                         ("bags", Kit.ART_PAGE, "Slots", SLOTS_TIP, act("open_win", "mgr"))],
                                  after=str(st["slots"]))
                    b = store[0].get("close")
                    if b is not None: Kit.on_click(b, act("disable", KEY))
            Kit.flush(); canvas_place(raw, raw.Children.Count, x0, y0, cw, ch); tw, th = bare_btn_size()
            if alone:
                st["side_pw"] = 0
                if st["bare"] and title_fits(W): add_bare_button(grid, x0 + cw - tw - 2, y0 + ch - th - 2)
                elif titled and side: st["side_pw"] = build_side_panel(grid, x0 + cw, ch, y0)[0]
                else: add_quick_strip(grid, x0 + cw - 2, y0 + ch - QUICK_ICON - 2)
            elif side_off(): add_bare_button(grid, W - tw - 2, H_ - th - 2); st["side_pw"] = 0
            else: st["side_pw"] = build_side_panel(grid, cw, H_)[0]
            grid.SetRect(st["frame_x"], st["frame_y"], W, H_); st["grid_wh"] = (W, H_); add_hook(grid, False)
            if not alone: lay_under(grid)
            if HOST.layout_locked(KEY): grid.CanMove = False
            Kit.add_front(grid); win["grid"] = grid
            bar = make_bar(W, True)
            if attached(): st["attach_g"] = st["attach"].get("g"); Kit.attach(grid, st["attach_g"])
            anchors_apply(followers); st["slot_raws"] = (); st["grid_raw"] = raw
            st["bar_raw"] = raw_of(bar) if R.ok else None
            if st["grid_raw"] is None:
                H.error = "can't reach the client's own window controls"; H.disabled = True; return
            refresh()
        def toggle_collapsed(): st["minimized"] = not st["minimized"]; st["docked"] = False; frame_changed()
        def dock_wish(): return HOST.dock_wanted(DOCK_KEY)
        def set_dock_wish(on): HOST.dock_want_set(DOCK_KEY, on)
        def user_collapse():
            if Kit.zone_up(KEY): return
            set_dock_wish(False); toggle_collapsed()
        def fold_to_bar():
            if Kit.zone_up(KEY): return
            set_dock_wish(True); alive = HOST.bar_alive()
            if not st["minimized"] or st["docked"] != alive:
                st["minimized"], st["docked"] = True, alive; frame_changed()
            if not alive: HOST.dock_note(TITLE)
        def toggle_bare():
            if attached(): st["side_hidden"] = not st["side_hidden"]
            else: st["bare"] = not st["bare"]
            frame_changed()
        _link = {"next": 0.0}
        def link_tick():
            now = time.time()
            if now < _link["next"]: return
            _link["next"] = now + 0.1; cmd = API.GetSharedVar(LINK_CMD)
            if cmd:
                API.RemoveSharedVar(LINK_CMD); cmd = str(cmd)
                if attached():
                    fn = st["attach"].get("cmd")
                    if fn is not None: safe(lambda: fn(cmd))
                elif cmd == "show" and (st["minimized"] or st["docked"]):
                    set_dock_wish(False); st["minimized"] = st["docked"] = False; frame_changed()
                elif cmd == "dock" and not st["docked"]: fold_to_bar()
            if attached(): state = str(st["attach"].get("state") or "open")
            else:
                if st["docked"]:
                    if not HOST.bar_alive(): st["docked"] = False; st["dirty_frame"] = True
                elif st["minimized"] and now >= _link.get("wish", 0.0):
                    _link["wish"] = now + 0.25
                    if dock_wish() and HOST.bar_alive(): st["docked"] = True; st["dirty_frame"] = True
                elif not st["minimized"] and now >= _link.get("wish", 0.0):
                    _link["wish"] = now + 1.0
                    if dock_wish(): set_dock_wish(False)
                state = "docked" if st["docked"] else ("collapsed" if st["minimized"] else "open")
            if state != st["link_state"]: st["link_state"] = state; API.SetSharedVar(LINK_STATE, state)
        def set_min(value):
            if not R.ok: API.SysMsg(TITLE + ": minimizing bags needs client access (%s)." % R.error, HUE_ERR); return
            n = set_minimized_all(value) or 0
            API.SysMsg(TITLE + ": %s %s." % ("minimized" if value else "restored", Kit.count(n, "bag")), HUE_INFO)
        def fallback_tick():
            track_wrapper_frame(); grew = False
            hidden = st["minimized"] or (attached() and not st["attach"].get("shown", True))
            for idx, serial in st["layout"]:
                try:
                    it = API.FindItem(serial); g = it.GetContainerGump() if it else None
                    if not Kit.is_open(g): continue
                    try: g.IsVisible = not hidden
                    except Exception: pass
                    if hidden: continue
                    cx, cy = cell_xy(idx)
                    if g.GetX() != cx or g.GetY() != cy: g.SetPos(cx, cy)
                    w = g.GetWidth() or 0; h = g.GetHeight() or 0
                except Exception: continue
                if st["cell_w"] < w <= MAX_CELL: st["cell_w"], grew = w, True
                if st["cell_h"] < h <= MAX_CELL: st["cell_h"], grew = h, True
            if grew: frame_changed()
        def follow_lead():
            lead = st["attach"].get("g") if attached() else None
            if lead is not None and lead is not st["attach_g"] and Kit.is_open(lead) and Kit.is_open(win.get("grid")):
                st["attach_g"] = lead; Kit.attach(win["grid"], lead)
        def track_wrapper_frame():
            if attached():
                lead, att = st["attach"].get("g"), st["attach"]
                if not Kit.is_open(lead): return
                follow_lead(); x = lead.GetX() + att.get("dx", 0); y = lead.GetY() + att.get("dy", 0)
                grid = win.get("grid")
                if (x, y) != (st["frame_x"], st["frame_y"]):
                    st["frame_x"], st["frame_y"] = x, y
                    if Kit.is_open(grid): grid.SetPos(x, y); Kit.moved_by_code(grid)
                elif Kit.is_open(grid) and (int(grid.GetX()), int(grid.GetY())) != (x, y):
                    grid.SetPos(x, y); Kit.moved_by_code(grid)
                return
            lead, other, dy = (win["grid"], win["bar"], 0) if win.get("grid_bare") else (win["bar"], win["grid"], BAR_H)
            if not Kit.is_open(lead): return
            x = lead.GetX(); y = lead.GetY()
            if x != st["frame_x"] or y != st["frame_y"]:
                st["frame_x"], st["frame_y"] = x, y
                if Kit.is_open(other): other.SetPos(x, y + dy); Kit.moved_by_code(other)
        def open_win(k): st["open_" + k] = True; st["dirty_" + k] = True; schedule_save()
        CHECKS_OF = {"trp": "trap_checks", "srt": "rule_checks"}
        def sub_sync(k):
            if k == "trp": sync_trap_sel()
            elif k == "srt": sync_rules()
        def close_win(k):
            sub_sync(k); close_sub(k)
            if k in CHECKS_OF: win[CHECKS_OF[k]] = []
            st["open_" + k] = False; schedule_save()
        def toggle_win_min(k):
            sub_sync(k); st[k + "_min"] = not st[k + "_min"]; st["dirty_" + k] = True
            schedule_save()
        def sub_window_moved(): remember_window_pos(); schedule_save()
        def build_manager():
            close_sub("mgr"); M, GAP = Kit.MARGIN, Kit.GAP; w, row_h, h_act = 480, 28, 40
            list_h = min(st["slots"] * row_h + 8, 430)
            h = M + 30 + M if st["mgr_min"] else M + 30 + GAP + h_act + GAP + list_h + M
            g, store, y = framed_window("mgr", w, h, "BAG MANAGER", act("toggle_win_min", "mgr"),
                                        act("close_win", "mgr"))
            if not st["mgr_min"]:
                IW = w - 2 * M; Kit.add_section(g, M, y, IW, h_act)
                Kit.art_button(g, store, "fill", Kit.ART_OK, M + 12, y + 9, "Auto-fill",
                               "Put each open bag without a slot in an empty slot", on_click=act("auto_fill"))
                Kit.art_button(g, store, "clear", Kit.ART_CLOSE, M + 200, y + 9, "Clear all",
                               "Empty every slot", on_click=act("clear_all"))
                y += h_act + GAP; Kit.add_section(g, M, y, IW, list_h)
                sa = G.CreateGumpScrollArea(M + 4, y + 4, IW - 8, list_h - 8); inner_w = IW - 8 - 20
                for idx in range(st["slots"]):
                    ry = idx * row_h; Kit.add_label(sa, "#%d" % (idx + 1), 6, ry + 5, Kit.HUE_TITLE)
                    if idx in st["assign"]: Kit.add_label(sa, short(bag_name(st["assign"][idx]), 28), 44, ry + 5)
                    else: Kit.add_label(sa, "No bag yet: click Set...", 44, ry + 5, Kit.HUE_INFO)
                    Kit.art_button(sa, store, "set%d" % idx, Kit.ART_PLAY, inner_w - 165, ry + 3,
                                   "Set...", "Target a bag for slot #%d" % (idx + 1), on_click=act("assign_slot", idx))
                    Kit.art_button(sa, store, "clr%d" % idx, Kit.ART_CLOSE, inner_w - 80, ry + 3, "Clear",
                                   "Empty slot #%d" % (idx + 1), on_click=act("clear_slot", idx))
                g.Add(sa)
            sub_shown("mgr", g, sub_window_moved)
        def changed_bags():
            forget_names(); st["dirty_frame"] = True; st["dirty_mgr"] = True; st["dirty_trp"] = True
            st["dirty_srt"] = True
            publish_layout(); save_settings()
        def pick_then(kind, *args):
            def done(serial): queue.add((kind,) + args + (int(serial or 0),), dup=True)
            HOST.pick_target(15, done)
        def assign_slot(idx):
            API.SysMsg(TITLE + ": target a bag for slot #%d." % (idx + 1), HUE_INFO); pick_then("assign_slot_to", idx)
        def assign_slot_to(idx, target):
            if not target: API.SysMsg(TITLE + ": cancelled.", HUE_INFO); return
            it = Kit.find_item(target)
            if not it or not it.IsContainer:
                API.SysMsg(TITLE + ": that isn't a container.", HUE_ERR); return
            serial = int(target)
            for k in [k for k, v in st["assign"].items() if v == serial]: del st["assign"][k]
            st["assign"][idx] = serial; changed_bags()
            if bag_is_open(serial): API.SysMsg(TITLE + ": slot #%d set." % (idx + 1), HUE_OK)
            else: API.SysMsg(TITLE + ": slot #%d set; open the bag to snap it in." % (idx + 1), HUE_OK)
        def clear_slot(idx):
            if idx in st["assign"]: del st["assign"][idx]; changed_bags()
        def clear_all(): st["assign"] = {}; changed_bags(); API.SysMsg(TITLE + ": all slots cleared.", HUE_INFO)
        def auto_fill():
            candidates = []
            for top in (safe(lambda: int(API.Backpack), 0), safe(lambda: int(API.Bank), 0)):
                if not top: continue
                candidates.append(top)
                for it in API.ItemsInContainer(top, True) or []:
                    if it.IsContainer: candidates.append(int(it.Serial))
            used = set(st["assign"].values()); free = [i for i in range(st["slots"]) if i not in st["assign"]]
            added = 0
            for serial in candidates:
                if not free: break
                if serial in used or not bag_is_open(serial): continue
                st["assign"][free.pop(0)] = serial; used.add(serial); added += 1
            changed_bags()
            if added: API.SysMsg(TITLE + ": added %s." % Kit.count(added, "open bag"), HUE_OK)
            elif not free: API.SysMsg(TITLE + ": no empty slots left.", HUE_ERR)
            else: API.SysMsg(TITLE + ": no open bag without a slot found.", HUE_INFO)
        page = {"c": None, "store": ({}, {}), "next_status": 0.0}
        def size_line():
            if st["canvas"] is not None: return "In a zone the bags share it. Items always draw solid."
            return "Slots fit the open bags (%d x %d px). Items always draw solid." % (st["cell_w"], st["cell_h"])
        def build_config(g, x, y, w):
            if R.ok and shrink["pct"] is None:
                got = safe(read_scale)
                if got: st["scale_pct"], st["scale_items"] = got
            f = Kit.Form(g, x, y, w, {"slots": st["slots"], "cols": st["cols"], "rows": st["rows"],
                                      "scale": st["scale_pct"], "opacity": int(round(st["opacity"] * 100)),
                                      "trim": st["trim"], "items": st["scale_items"]}, page_table(w))
            page.update({"c": f.c, "store": f.store, "next_status": 0.0,
                         "seen": {"trim": st["trim"], "items": st["scale_items"]}})
        def config_closed(): page["c"] = None
        def poll_config():
            c = page["c"]
            if c is None: return
            if Kit.was_clicked(page["store"], "apply"): apply_config(); return
            for key, apply in (("trim", set_trim), ("items", set_scale_items)):
                try: ticked = bool(c[key].IsChecked)
                except Exception: ticked = None
                if ticked is not None and ticked != page["seen"][key]: page["seen"][key] = ticked; apply(ticked)
            try: v = int(c["opacity"].Value)
            except Exception: v = None
            if v is not None and 10 <= v <= 100:
                if page.get("pct_v") != (v, c["opacity_lbl"]):
                    page["pct_v"] = (v, c["opacity_lbl"]); Kit.set_text(c["opacity_lbl"], "%d%%" % v)
                value = v / 100.0
                if abs(value - st["opacity"]) > 0.001:
                    pend = st["opacity_pending"]
                    st["opacity_pending"] = (value, pend[1] + 1) if pend and pend[0] == value else (value, 0)
                    if st["opacity_pending"][1] >= OPACITY_SETTLE_POLLS:
                        st["opacity"] = value; st["opacity_pending"] = None; st["dirty_frame"] = True; canvas_alpha()
                        schedule_save()
                else: st["opacity_pending"] = None
            now = time.time()
            if now >= page["next_status"]:
                page["next_status"] = now + 1.0; Kit.set_text(c["status"], short(status_line(), 64))
                Kit.set_text(c["size"], size_line())
        def status_line():
            if not R.tried: return "Off: tick " + TITLE + " on the Modules tab"
            if not R.ok: return "No client access: " + R.error
            if H.disabled: return "Trimming stopped after errors: " + H.error
            if st["canvas"] is not None: tail = "%d open, filling the zone" % H.open_count
            else: tail = "%d open, %d trimmed" % (H.open_count, len(H.trimmed))
            if st["driving"]: return "Running (script-driven): " + tail
            return "Starting" if H.hook_calls == 0 else "Running: " + tail
        def set_trim(value):
            f = page["c"]
            if value and not (R.ok and not H.disabled):
                API.SysMsg(TITLE + ": trimming isn't available (%s)." % status_line(), HUE_ERR)
                if f: safe(lambda: f["trim"].SetIsChecked(False)); page["seen"]["trim"] = False
                value = False
            if value == st["trim"]: return
            st["trim"] = value; refit_cells(); save_settings()
            API.SysMsg(TITLE + ": trim " + ("on." if value else "off."), HUE_INFO)
        def set_scale_items(value):
            if value == st["scale_items"]: return
            if not R.ok: API.SysMsg(TITLE + ": scaling items needs client access (%s)." % R.error, HUE_ERR)
            else:
                try:
                    old = st["scale_items"]; st["scale_items"] = value
                    try: apply_scale(*scale_now())
                    except Exception: st["scale_items"] = old; raise
                    if shrink["pct"] is not None: note_shrunk()
                    refit_cells()
                    API.SysMsg(TITLE + ": items %s with the bags." % ("scale" if value else "don't scale"), HUE_INFO)
                except Exception as e: API.SysMsg(TITLE + ": couldn't change the item scaling (%s)." % e, HUE_ERR)
            f = page["c"]
            if f and st["scale_items"] != value:
                safe(lambda: f["items"].SetIsChecked(st["scale_items"])); page["seen"]["items"] = st["scale_items"]
        def read_int(field, name, lo, hi):
            raw = (safe(lambda: field.Text, "") or "").strip()
            if not raw.isdigit() or not (lo <= int(raw) <= hi):
                raise ValueError("%s must be a whole number from %d to %d." % (name, lo, hi))
            return int(raw)
        def apply_config():
            f = page["c"]
            if not f: return
            try:
                slots = read_int(f["slots"], "Slots", MIN_SLOTS, MAX_SLOTS)
                cols = read_int(f["cols"], "Columns", 0, MAX_SLOTS); rows = read_int(f["rows"], "Rows", 0, MAX_SLOTS)
                scale = read_int(f["scale"], "Bag scale", 50, 200)
            except ValueError as e: API.SysMsg(TITLE + ": " + str(e), HUE_ERR); return
            if cols > 0 and rows > 0 and cols * rows < slots:
                API.SysMsg(TITLE + ": %d columns x %d rows only fits %d slots, not %d."
                           % (cols, rows, cols * rows, slots), HUE_ERR)
                return
            dropped = [k for k in st["assign"] if k >= slots]
            for k in dropped: del st["assign"][k]
            sync_rules()
            for k in [k for k in st["rules"] if k >= slots]: del st["rules"][k]
            st["slots"], st["cols"], st["rows"] = slots, cols, rows
            if R.ok and scale != st["scale_pct"]:
                try:
                    old = st["scale_pct"]; st["scale_pct"] = scale
                    try: apply_scale(*scale_now())
                    except Exception: st["scale_pct"] = old; raise
                    if shrink["pct"] is not None:
                        if shrink["pct"] >= scale: shrink["pct"] = None
                        note_shrunk()
                    refit_cells()
                except Exception as e: API.SysMsg(TITLE + ": couldn't change the bag scale (%s)." % e, HUE_ERR)
            changed_bags(); c, r = layout_dims()
            msg = TITLE + ": %s in %d x %d." % (Kit.count(slots, "slot"), c, r)
            if dropped: msg += " Released %s from removed slots." % Kit.count(len(dropped), "bag")
            API.SysMsg(msg, HUE_OK); config_closed(); HOST.refresh_settings(KEY)
        def trap_candidates():
            out = []
            for s in [st["assign"][i] for i in sorted(st["assign"])] + st["trap_extra"]:
                if s not in out: out.append(s)
            return out
        def sync_trap_sel():
            checks = win["trap_checks"]
            if not checks or not Kit.is_open(win["trp"]): return
            for serial, chk in checks:
                if safe(lambda: chk.IsChecked, False): st["trap_sel"].add(serial)
                else: st["trap_sel"].discard(serial)
        def build_traps():
            sync_trap_sel(); close_sub("trp"); bags = trap_candidates(); M, GAP = Kit.MARGIN, Kit.GAP
            w, row_h, h_act, h_foot = 480, 28, 40, 52; list_h = min(max(1, len(bags)) * row_h + 8, 400)
            h = (M + 30 + M if st["trp_min"] else M + 30 + GAP + h_act + GAP + list_h + GAP + h_foot + M)
            g, store, y = framed_window("trp", w, h, "TRAP BAGS", act("toggle_win_min", "trp"), act("close_win", "trp"))
            checks = []
            if not st["trp_min"]:
                IW = w - 2 * M; Kit.add_section(g, M, y, IW, h_act)
                Kit.buttons(g, store, M + 12, y + 9, (
                    ("all", Kit.ART_OK, "Tick all", "Tick every bag", act("select_all_traps", True)),
                    ("none", Kit.ART_CLOSE, "Untick all", "Untick every bag", act("select_all_traps", False)),
                    ("add", Kit.ART_PLAY, "Add bag...", "Target a bag without a slot to add it",
                     act("add_trap_bag"))), 16)
                y += h_act + GAP; Kit.add_section(g, M, y, IW, list_h)
                sa = G.CreateGumpScrollArea(M + 4, y + 4, IW - 8, list_h - 8); inner_w = IW - 8 - 20
                if not bags: Kit.add_label(sa, "No bags yet. Fill the slots, or click Add bag...", 6, 6, Kit.HUE_INFO)
                for i, serial in enumerate(bags):
                    ry = i * row_h
                    chk = Kit.add_check(sa, short(bag_name(serial), 32), 6, ry + 4, serial in st["trap_sel"],
                                        "Ticked: Trap and Untrap cast on this bag")
                    checks.append((serial, chk))
                    if serial in st["trap_extra"] and serial not in st["assign"].values():
                        Kit.art_button(sa, store, "rm%d" % i, Kit.ART_CLOSE, inner_w - 110, ry + 3,
                                       "Remove", "Take this bag off", on_click=act("remove_trap_bag", serial))
                g.Add(sa); y += list_h + GAP; Kit.add_section(g, M, y, IW, h_foot)
                Kit.add_label(g, "Tick bags, then Trap or Untrap on the side panel.", M + 12, y + 8, Kit.HUE_INFO)
                Kit.add_label(g, "A trapped bag explodes on whoever opens it, you included.",
                              M + 12, y + 28, Kit.HUE_BAD)
            sub_shown("trp", g, sub_window_moved, trap_checks=checks)
        def traps_changed(): win["trap_checks"] = []; st["dirty_trp"] = True; save_settings()
        def select_all_traps(value): st["trap_sel"] = set(trap_candidates()) if value else set(); traps_changed()
        def add_trap_bag():
            sync_trap_sel(); API.SysMsg(TITLE + ": target a bag to add to the trap list.", HUE_INFO)
            pick_then("add_trap_bag_to")
        def add_trap_bag_to(target):
            if not target: return
            sync_trap_sel(); it = Kit.find_item(target)
            if not it or not it.IsContainer:
                API.SysMsg(TITLE + ": that isn't a container.", HUE_ERR); return
            serial = int(target)
            if serial not in st["trap_extra"]: st["trap_extra"].append(serial)
            st["trap_sel"].add(serial); traps_changed()
        def remove_trap_bag(serial):
            sync_trap_sel()
            if serial in st["trap_extra"]: st["trap_extra"].remove(serial)
            st["trap_sel"].discard(serial); traps_changed()
        def start_job(spell):
            sync_trap_sel(); save_settings()
            if st["job"]:
                API.SysMsg(TITLE + ": already casting %s; press Stop first." % st["job"]["spell"], HUE_ERR); return
            if st["sort"]: API.SysMsg(TITLE + ": busy sorting; press Stop first.", HUE_ERR); return
            targets = [s for s in trap_candidates() if s in st["trap_sel"]]
            if not targets:
                API.SysMsg(TITLE + ": tick bags in the Trap bags window first.", HUE_ERR)
                open_win("trp"); return
            st["job"] = {"spell": spell, "queue": targets, "i": 0, "phase": "mana", "t": 0.0,
                      "tries": 0, "done": 0, "failed": 0, "warned": False, "cast": 0.0,
                      "me": str(API.Player.Name or "")}
            st["dirty_trp"] = True; set_status("Starting")
            API.SysMsg(TITLE + ": casting %s on %s." % (spell, Kit.count(len(targets), "bag")), HUE_INFO)
        def stop_job(user=False):
            if st["job"]:
                j0 = st["job"]
                if j0.get("phase") == "target" and time.time() - j0.get("cast", 0.0) >= TRAP_CAST_MIN \
                        and HOST.cursor_ok(KEY, "neutral"):
                    API.CancelTarget()
                HOST.release_cursor(KEY)
                if user: API.SysMsg(TITLE + ": %s stopped." % st["job"]["spell"], HUE_INFO); set_status("Stopped")
            st["job"] = None; st["dirty_trp"] = True
        def show_stop():
            on = bool(st["job"] or st["sort"])
            for ctrl in win.get("stop_ctrls") or ():
                if ctrl is not None: Kit.set(ctrl, "IsVisible", on)
        def set_status(text):
            if text == "Idle":
                p = shrink["pct"]; text = ("Shown at %d%% to fit" % p) if p is not None and p < st["scale_pct"] else ""
            show_stop()
            if text == st["status_text"]: return
            st["status_text"] = text; lab = win.get("side_status")
            if lab is not None: Kit.set_text(lab, text)
        J_RESULTS = tuple((res, tuple(w.lower() for w in words))
                          for res, words in (("reagents", J_REAGENTS), ("mana", J_MANA),
                                             ("fizzle", J_FIZZLE), ("busy", J_BUSY), ("noreach", J_NOREACH)))
        def journal_result(j):
            rd = j.get("jr")
            if rd is None: return None
            texts = j["jt"]; me = j.get("me")
            for ln in rd.new():
                if ln.text and not ln.text.startswith(TITLE) and (not ln.name or ln.name in ("System", me)
                                                                  or ln.kind == "SYSTEM"):
                    texts.append(ln.low)
            if not texts: return None
            for res, words in J_RESULTS:
                if any(w in t for w in words for t in texts): return res
            return None
        def job_next(j, success):
            if success: j["done"] += 1
            else: j["failed"] += 1
            j["i"] += 1; j["tries"] = 0; j["phase"] = "mana"
        def job_retry(j, now, reason):
            j["tries"] += 1
            if j["tries"] > TRAP_RETRIES:
                API.SysMsg(TITLE + ": giving up on %s (%s)." % (bag_name(j["queue"][j["i"]], False), reason), HUE_ERR)
                job_next(j, False)
            else: j["phase"] = "pause"; j["t"] = now + TRAP_RETRY_PAUSE
        def job_step():
            j = st["job"]
            if not j: return
            now = time.time()
            if j["i"] >= len(j["queue"]):
                API.SysMsg(TITLE + ": %s finished: %d done, %d failed." % (j["spell"], j["done"], j["failed"]),
                           HUE_OK if not j["failed"] else HUE_ERR)
                set_status("Done %d/%d" % (j["done"], len(j["queue"]))); stop_job(); return
            serial = j["queue"][j["i"]]; ph = j["phase"]
            if ph == "pause":
                if now >= j["t"]: j["phase"] = "mana"
                return
            if ph == "mana":
                held = HOST.fight_hold(now) or HOST.guard_hold()
                if held:
                    if j.get("held") != held:
                        j["held"] = held; text = HOLD_TEXT.get(held, held)
                        API.SysMsg(TITLE + ": %s waits (%s)." % (j["spell"], text[:1].lower() + text[1:]), HUE_INFO)
                        set_status(text if held == "unknown" else "Paused: " + text)
                    return
                if j.get("held"): j["held"] = None; set_status("Starting")
                mana = API.Player.Mana
                if mana < TRAP_MANA:
                    if not j["warned"]:
                        API.SysMsg(TITLE + ": waiting for mana (%d/%d)." % (mana, TRAP_MANA), HUE_INFO)
                        set_status("Need mana"); j["warned"] = True
                    return
                j["warned"] = False
                if not Kit.find_item(serial):
                    API.SysMsg(TITLE + ": bag 0x%08X is out of reach; skipping it." % serial, HUE_ERR)
                    job_next(j, False); return
                if others_cursor(): set_status("Cursor busy"); return
                if API.HasTarget("any"): set_status("Cursor busy"); return
                API.SysMsg(TITLE + ": %s %d/%d: %s." % (j["spell"], j["i"] + 1, len(j["queue"]),
                                                          bag_name(serial, False)), HUE_INFO)
                set_status("%s %d/%d" % ("Untrap" if "Untrap" in j["spell"] else "Trap", j["i"] + 1, len(j["queue"])))
                j["cast"] = time.time(); j["jr"], j["jt"] = Journal.reader(), []
                HOST.claim_cursor(KEY, TRAP_TARGET_TIMEOUT + 0.5); API.CastSpell(j["spell"]); j["phase"] = "target"
                j["t"] = now; return
            if ph == "target":
                res = journal_result(j)
                if res and res != "noreach": HOST.release_cursor(KEY)
                if res == "reagents":
                    API.SysMsg(TITLE + ": out of reagents for %s." % j["spell"], HUE_ERR); stop_job(); return
                if res == "mana": j["phase"] = "mana"; return
                if res in ("fizzle", "busy"): job_retry(j, now, res); return
                if now - j["cast"] >= TRAP_CAST_MIN and HOST.cursor_ok(KEY, "neutral"):
                    API.Target(serial); HOST.release_cursor(KEY); j["phase"] = "recover"; j["t"] = now; j["jt"] = []
                elif now - j["t"] > TRAP_TARGET_TIMEOUT: HOST.release_cursor(KEY); job_retry(j, now, "no target cursor")
                return
            if ph == "recover":
                if now - j["t"] < TRAP_RECOVERY: return
                res = journal_result(j)
                if res == "reagents": API.SysMsg(TITLE + ": out of reagents for %s." % j["spell"], HUE_ERR); stop_job()
                elif res in ("fizzle", "busy", "mana"): job_retry(j, now, res)
                elif res == "noreach":
                    API.SysMsg(TITLE + ": couldn't %s %s (out of reach or refused); skipping it."
                               % ("untrap" if "Untrap" in j["spell"] else "trap", bag_name(serial, False)), HUE_ERR)
                    job_next(j, False)
                else: job_next(j, True)
        def set_hue(it, hue):
            try: it.SetHue(int(hue) & 0xFFFF); return True
            except Exception: return False
        def hue_of(it):
            try: return int(it.Hue or 0)
            except Exception: return -1
        SR = {"text": "", "typed": 0.0, "armed": False, "lit": {}, "until": 0.0, "counts": {}, "restored": {},
              "tiles": {}, "status": None, "texts": {}, "texts_at": 0.0, "objs": {}}
        def search_terms(q):
            out = []
            for part in (q or "").lower().split(","):
                p = part.strip()
                if not p: continue
                g = None
                try:
                    if p.startswith("0x") and len(p) > 2: g = int(p, 16)
                    elif p.isdigit(): g = int(p)
                except ValueError: g = None
                out.append((p, g))
            return out
        def expand_tile(raw):
            if "%" not in raw: return raw
            one, many = [], []
            for i, p in enumerate(raw.split("%")):
                if i % 2 == 0: one.append(p); many.append(p)
                else: pl, _, sg = p.partition("/"); one.append(sg); many.append(pl)
            return "".join(one) + " " + "".join(many)
        def tile_name(it, graphic):
            names = SR["tiles"]; t = names.get(graphic)
            if t is None:
                d = it.GetItemData(); raw = str(d.Name or "") if d is not None else ""
                t = expand_tile(raw).lower()
                if len(names) >= TILE_NAME_CAP: names.clear()
                names[graphic] = t
            return t
        def item_text(it, serial, graphic):
            tc = SR["texts"]; t = tc.get(serial)
            if t is not None: return t + "\n" + tile_name(it, graphic)
            t = API.ItemNameAndProps(serial) or ""
            if t:
                t = str(t).lower()
                if "\n" in t and len(tc) < SEARCH_SCAN_CAP: tc[serial] = t
                return t + "\n" + tile_name(it, graphic)
            return str(it.Name or "").lower() + "\n" + tile_name(it, graphic)
        def scan_matches(terms):
            assigned = set(s for _, s in st["layout"]); found, counts = {}, {}; objs = {}; seen = 0
            for idx, bag in st["layout"]:
                if seen >= SEARCH_SCAN_CAP: break
                items = API.ItemsInContainer(bag, True) or []; parent = {}; sers = []
                for it in items:
                    try: xs = int(it.Serial)
                    except Exception: sers.append(None); continue
                    sers.append(xs)
                    try: parent[xs] = int(it.Container)
                    except Exception: pass
                n = 0
                for j in range(len(sers)):
                    if seen >= SEARCH_SCAN_CAP: break
                    seen += 1; serial = sers[j]
                    if serial is None or serial in assigned: continue
                    top, c, depth = serial, parent.get(serial, bag), 0
                    while c != bag and depth < SEARCH_DEPTH and c not in assigned:
                        top, c = c, parent.get(c, bag); depth += 1
                    if c != bag: continue
                    it = items[j]
                    try: graphic = int(it.Graphic)
                    except Exception: continue
                    text = None; hit = False
                    for p, g in terms:
                        if g is not None:
                            if graphic == g: hit = True; break
                        else:
                            if text is None: text = item_text(it, serial, graphic)
                            if p in text: hit = True; break
                    if not hit: continue
                    n += 1
                    if len(found) < SEARCH_LIT_CAP:
                        found[serial] = idx; objs[serial] = it
                        if top != serial and len(found) < SEARCH_LIT_CAP: found[top] = idx
                if n: counts[idx] = n
            SR["objs"] = objs; return found, counts
        def scanned(serial): it = SR["objs"].get(serial); return it if it is not None else API.FindItem(serial)
        def light(serial, now):
            it = scanned(serial)
            if not it: return False
            cur = hue_of(it)
            if cur < 0: return False
            orig = cur
            if cur == SEARCH_HUE:
                rec = SR["restored"].get(serial)
                if rec is not None and now - rec[1] < HUE_MEMORY: orig = rec[0]
            if not set_hue(it, SEARCH_HUE): return False
            canvas_hue(serial, SEARCH_HUE); SR["lit"][serial] = orig; return True
        def unlight(serial, orig, now):
            it = API.FindItem(serial)
            if not it: return
            cur = hue_of(it)
            if cur == SEARCH_HUE or cur == orig:
                if set_hue(it, orig): canvas_hue(serial, orig)
                SR["restored"][serial] = (orig, now)
        def prune_restored(now):
            rs = SR["restored"]
            if rs:
                for s in [s for s, rec in rs.items() if now - rec[1] >= HUE_MEMORY]: del rs[s]
                if len(rs) > 2 * SEARCH_LIT_CAP: rs.clear()
        def run_search(q, now):
            terms = search_terms(q)
            if not terms: clear_search(now); return
            prune_restored(now)
            if not 0 <= now - SR["texts_at"] <= SEARCH_LIT: SR["texts"] = {}; SR["texts_at"] = now
            found, counts = scan_matches(terms); lit = SR["lit"]
            for serial in [s for s in lit if s not in found]: unlight(serial, lit.pop(serial), now)
            try:
                for serial in found:
                    if serial not in lit: light(serial, now)
                    else: relight(serial)
            finally: SR["objs"] = {}
            SR["counts"] = counts; SR["until"] = now + SEARCH_LIT; show_counts(); total = sum(counts.values())
            text = ("%d found" % total) if total else "None found"; SR["status"] = text; set_status(text)
        def relight(serial):
            it = scanned(serial)
            if not it: return
            cur = hue_of(it)
            if 0 <= cur != SEARCH_HUE and set_hue(it, SEARCH_HUE):
                canvas_hue(serial, SEARCH_HUE); SR["lit"][serial] = cur
        def clear_search(now):
            lit = SR["lit"]
            for serial in list(lit): unlight(serial, lit.pop(serial), now)
            SR["texts"] = {}; SR["texts_at"] = 0.0; SR["until"] = 0.0
            if SR["counts"]: SR["counts"] = {}; show_counts()
            if SR["status"] is not None:
                if st["status_text"] == SR["status"]: set_status("Idle")
                SR["status"] = None
        def show_counts():
            counts = SR["counts"]; state = win["count_state"]
            for idx, (lab, x, y, cw, ch) in enumerate(win["counts"]):
                n = counts.get(idx, 0); text = ("%d found" % n) if n else ""
                if state.get(idx) == text: continue
                state[idx] = text
                try:
                    if n:
                        lab.SetPos(x + max(5, cw - 5 - Kit.text_w(text)), y + max(0, ch - 18)); Kit.set_text(lab, text)
                    lab.IsVisible = bool(n)
                except Exception: pass
        def search_tick(now):
            box = win["search_box"]
            if box is not None and not (st["minimized"] or st["docked"]):
                try: txt = box.Text
                except Exception: txt = None
                if txt is not None:
                    txt = str(txt)
                    if txt != SR["text"]: SR["text"], SR["typed"], SR["armed"] = txt, now, True
            if SR["armed"]:
                if now - SR["typed"] >= SEARCH_SETTLE:
                    SR["armed"] = False; q = SR["text"].strip()
                    if len(q) >= SEARCH_MIN: run_search(q, now)
                    elif SR["lit"] or SR["counts"]: clear_search(now)
            elif SR["until"] and now >= SR["until"]: clear_search(now)
        def build_tools(grid, bx, y):
            lw = Kit.text_w("Find:") + 6; label(grid, "Find:", bx + 2, y + 3, Kit.HUE_TEXT)
            box = Kit.add_textbox(grid, SR["text"], bx + 2 + lw, y, SIDE_BTN_W - 4 - lw, numbers=False)
            box.SetTooltip("Item name part or graphic (0x0F7A, 3962); commas for several. Matches light up for %d s"
                           % int(SEARCH_LIT))
            win["search_box"] = box
            Kit.art_button(grid, win["store"], "rules", Kit.ART_PAGE, bx, y + 28, "Rules",
                           "Open Sort rules: what each slot's bag holds", on_click=act("open_win", "srt"))
            Kit.art_button(grid, win["store"], "filters", Kit.ART_PAGE, bx, y + 52, "Filters",
                           "Open Sort filters: items or presets and their bags", on_click=act("open_filters"))
        SORT_TIP = "Sort items into their bags once; picking up or Stop ends it"
        QUICK = (("q_restock", "Restock", Kit.ART_PLAY, 0x0E76, "restock",
                  "Top up supplies once from the Restock chest or bank", "restock.run"),
                 ("q_sort", "Sort", Kit.ART_PLAY, 0x0E79, None, SORT_TIP, None),
                 ("q_storage", "Storage", Kit.ART_PAGE, 0x0E40, "storage", "Open or raise the Storage window",
                  "storage.show"),
                 ("q_supplies", "Supplies", Kit.ART_PAGE, 0x0F7A, "supplies", "Open or raise the Supplies table",
                  "supplies.open"))
        def quick_on(part): return part is None or HOST.part_on(part, "inventory")
        def quick_tip(part, tip):
            if quick_on(part): return tip
            return ("%s is off: tick Inventory > %s on the Modules tab" % (part.title(), part.title()))
        def quick_press(key):
            for k, cap, _art, _icon, part, _tip, svc in QUICK:
                if k != key: continue
                if part is None: start_sort(); return
                fn = HOST.services.get(svc) if quick_on(part) else None
                if fn is None:
                    API.SysMsg("%s: %s is off; tick Inventory > %s on the Modules tab." % (TITLE, cap, cap), HUE_INFO)
                    return
                fn(); return
        def quick_sig(): return tuple(quick_on(q[4]) for q in QUICK)
        def build_quick(grid, bx, y):
            win["quick_sig"] = quick_sig()
            for i, (k, cap, art, _icon, part, tip, _svc) in enumerate(QUICK):
                Kit.art_button(grid, win["store"], k, art, bx, y + i * 24, cap, quick_tip(part, tip),
                               hue=None if quick_on(part) else Kit.HUE_INFO, on_click=act("quick_press", k))
        QUICK_ICON = 18; QUICK_STEP = 22
        def add_quick_strip(grid, x_right, y):
            win["quick_sig"] = quick_sig(); x = x_right - len(QUICK) * QUICK_STEP
            for i, (k, cap, _art, icon, part, tip, _svc) in enumerate(QUICK):
                with Kit.quiet:
                    pic = G.CreateGumpItemPic(icon, QUICK_ICON, QUICK_ICON)
                    pic.SetRect(x + i * QUICK_STEP, y, QUICK_ICON, QUICK_ICON)
                    if not quick_on(part): Kit.set(pic, "Hue", Kit.HUE_INFO)
                    Kit.set(pic, "DrawBorder", False); t = quick_tip(part, tip)
                    pic.SetTooltip(t if not quick_on(part) else cap + ": " + t)
                    G.AddControlOnClick(pic, act("quick_press", k)); grid.Add(pic)
        KIND_GRAPHICS = dict((k, frozenset(gs)) for k, _c, gs in SORT_KINDS); NO_RULE = (frozenset(), ())
        def rule_graphics(idx):
            kinds, extra = st["rules"].get(idx, NO_RULE); out = set(extra)
            for k in kinds: out |= KIND_GRAPHICS.get(k, frozenset())
            return out
        def in_corpse(serial):
            s = int(serial or 0)
            for _ in range(12):
                it = API.FindItem(s)
                if it is None: return False
                if int(it.Graphic or 0) == 0x2006 or it.IsCorpse: return True
                c = int(it.Container or 0)
                if not c or c == 0xFFFFFFFF or c < 0x40000000: return False
                s = c
            return False
        def sort_plan():
            flt = [f for f in st["filters"] if f["on"] and f["slot"] is not None and f["set"]]; wants = {}
            for idx, bag in st["layout"]:
                gs = rule_graphics(idx)
                if gs: wants[idx] = gs
            if not wants and not flt: return None
            by_graphic = {}
            for idx in sorted(wants):
                for g in wants[idx]:
                    if g not in by_graphic: by_graphic[g] = idx
            slot_of = dict((s, i) for i, s in st["layout"]); sources = []; pack = safe(lambda: int(API.Backpack), 0)
            if pack: sources.append(pack)
            for _, bag in st["layout"]:
                if bag not in sources and not in_corpse(bag): sources.append(bag)
            plan = []
            for src in sources:
                here = wants.get(slot_of.get(src), ())
                for it in API.ItemsInContainer(src, False) or []:
                    if len(plan) >= SORT_CAP: break
                    try: serial, graphic = int(it.Serial), int(it.Graphic)
                    except Exception: continue
                    if serial in slot_of: continue
                    idx = None
                    if flt:
                        hue = int(SR["lit"].get(serial, it.Hue or 0)) & 0x3FFF
                        for f in flt:
                            if graphic in f["set"] and (f["hue"] is None or f["hue"] == hue): idx = f["slot"]; break
                    if idx is None:
                        idx = by_graphic.get(graphic)
                        if idx is None or graphic in here: continue
                    if it.IsContainer: continue
                    dest = st["assign"].get(idx)
                    if dest and dest != src: plan.append((serial, src, dest, idx))
            return plan
        def start_sort():
            sync_rules()
            if st["sort"]: API.SysMsg(TITLE + ": already sorting; press Stop first.", HUE_ERR); return
            if st["job"]: API.SysMsg(TITLE + ": busy with %s; press Stop first." % st["job"]["spell"], HUE_ERR); return
            plan = sort_plan()
            if plan is None:
                API.SysMsg(TITLE + ": no sort rules yet; tick what each bag holds in Sort rules.", HUE_ERR)
                open_win("srt"); return
            if not plan:
                API.SysMsg(TITLE + ": nothing to sort; every ruled item is in its bag.", HUE_INFO)
                set_status("Nothing to sort"); return
            st["sort"] = {"plan": plan, "i": 0, "move": None, "check": None, "at": 0.0, "hold": 0.0,
                       "moved": 0, "refused": 0, "streak": 0, "rechecks": 0, "waits": 0,
                       "why": None, "last": 0, "sent_at": 0.0}
            set_status("Sort 0/%d" % len(plan))
            API.SysMsg(TITLE + ": sorting %s." % Kit.count(len(plan), "item"), HUE_INFO)
        def check_move(s, now):
            serial, src, dest, idx = s["check"]; t0 = s["sent_at"]
            if Journal.find(t0, J_FULL) is not None:
                stop_sort("bag #%d (%s) is full" % (idx + 1, bag_name(dest, False))); return False
            it = API.FindItem(serial); where = int(it.Container) if it else None
            if where is None and s["rechecks"] < SORT_RECHECK and not stacked(s, dest):
                s["rechecks"] += 1; s["at"] = now + SORT_GAP * 0.5; return False
            if where is None or where == dest:
                s["moved"] += 1
                s["streak"] = s["rechecks"] = s["waits"] = 0; s["check"] = None; return True
            if (where == src and Journal.find(t0, J_WAIT) is not None and s["waits"] < SORT_FAIL_STOP):
                s["waits"] += 1; s["i"] -= 1
                s["check"] = None; s["rechecks"] = 0; s["hold"] = now + SORT_GAP; return False
            if s["rechecks"] < SORT_RECHECK:
                s["rechecks"] += 1; s["at"] = now + SORT_GAP * 0.5; return False
            s["check"] = None; s["rechecks"] = 0; s["refused"] += 1
            s["streak"] += 1
            if s["streak"] >= SORT_FAIL_STOP: stop_sort("%d moves in a row were refused" % s["streak"]); return False
            return True
        def stack_total(bag, graphic, deep=None):
            n = 0
            try:
                if deep is None:
                    for x in (API.ItemsInContainer(bag, False) or []):
                        if int(x.Graphic) == graphic: n += int(x.Amount or 1)
                else:
                    for x in deep:
                        if int(x.Graphic) == graphic and int(x.Container) == bag: n += int(x.Amount or 1)
            except Exception: pass
            return n
        def stacked(s, bag):
            pre = s.get("pre"); return True if not pre or not pre[0] else stack_total(bag, pre[0]) >= pre[2] + pre[1]
        def sort_tick(now):
            s = st["sort"]
            if s is None: return
            if s["move"] is not None: return
            if s["why"]: stop_sort(s["why"]); return
            if s["check"] is not None:
                if now < s["at"] or not check_move(s, now): return
            if now < s["hold"]: return
            if others_cursor(): stop_sort("another target cursor is in use"); return
            h = Kit.held_item()
            if h and not (h == s["last"] and now - s["sent_at"] < 2 * SORT_GAP):
                stop_sort("you picked something up"); return
            plan = s["plan"]
            while s["i"] < len(plan):
                serial, src, dest, idx = plan[s["i"]]; s["i"] += 1
                it = API.FindItem(serial); where = int(it.Container) if it else 0
                if where != src: continue
                if st["assign"].get(idx) != dest: continue
                if not Kit.find_item(dest): stop_sort("slot #%d's bag is out of reach" % (idx + 1)); return
                deep = API.ItemsInContainer(dest, True) or []; inside = len(deep)
                if inside >= BAG_MAX_ITEMS: stop_sort("bag #%d (%s) is full" % (idx + 1, bag_name(dest, False))); return
                s["move"] = (serial, src, dest, idx); gr = int(it.Graphic or 0)
                s["pre"] = (gr, int(it.Amount or 1), stack_total(dest, gr, deep))
                set_status("Sort %d/%d" % (s["i"], len(plan))); return
            finish_sort()
        def sort_send():
            s = st["sort"]
            if s is None or s["move"] is None: return
            mv = s["move"]; s["move"] = None
            if st["shutting"]: return
            if others_cursor(): s["why"] = "another target cursor is in use"; return
            if Kit.held_item(): s["why"] = "you picked something up"; return
            try: API.MoveItem(mv[0], mv[2])
            except Exception as e: s["why"] = "a move failed (%s)" % e; return
            HOST.pack_dirty(); s["check"] = mv; s["last"] = mv[0]; s["sent_at"] = time.time()
            s["at"] = s["sent_at"] + SORT_GAP
        def finish_sort():
            s, st["sort"] = st["sort"], None
            if s is None: return
            msg = "%d moved" % s["moved"]
            if s["refused"]: msg += ", %d refused" % s["refused"]
            API.SysMsg(TITLE + ": sort done: %s." % msg, HUE_ERR if s["refused"] else HUE_OK)
            set_status("Sorted %d" % s["moved"])
        def stop_sort(why=None, user=False):
            s, st["sort"] = st["sort"], None
            if s is None: return
            if user: API.SysMsg(TITLE + ": sort stopped (%d moved)." % s["moved"], HUE_INFO); set_status("Stopped")
            elif why:
                API.SysMsg(TITLE + ": sort stopped: %s (%d moved)." % (why, s["moved"]), HUE_ERR)
                set_status("Sort stopped")
        def stop_all(): stop_job(True); stop_sort(user=True)
        FILTERS_KEY = "UnifiedBag_filters"; FILTERS_CAP = 40; BROAD = ("exact", "kind", "category")
        BROAD_CAP = {"exact": "this exact item", "kind": "this kind", "category": "its category"}
        def load_filters():
            st["filters"] = []
            for part in str(Kit.get_var(FILTERS_KEY, "") or "").split(";"):
                p = part.split("~")
                if len(p) < 5 or len(st["filters"]) >= FILTERS_CAP: continue
                try:
                    slot = int(p[3]) if p[3] != "" else None; hue = int(p[2]) if p[2] != "" else None
                    gs = tuple(int(x, 16) for x in p[1].split(",") if x and not x.startswith("@"))
                except ValueError: continue
                if not (0 <= (slot or 0) < MAX_SLOTS and 0 <= (hue or 0) <= 0xFFFF
                        and all(0 <= g <= 0xFFFF for g in gs)): continue
                cat = p[1][1:] if p[1].startswith("@") else None; base = None
                if len(p) >= 7 and ":" in p[5]:
                    try: base = (int(p[5].split(":", 1)[0], 16), int(p[5].split(":", 1)[1]))
                    except ValueError: base = None
                    if base is not None and not (0 <= base[0] <= 0xFFFF and 0 <= base[1] <= 0xFFFF): base = None
                st["filters"].append({"name": p[0], "gr": gs, "cat": cat, "hue": hue, "slot": slot,
                                   "on": p[4] == "1", "set": frozenset(gs), "base": base,
                                   "broad": p[6] if len(p) >= 7 and p[6] in BROAD else None})
            cats["wanted"] = cats["wanted"] or any(f["cat"] for f in st["filters"])
        def save_filters():
            Kit.put_var(FILTERS_KEY, ";".join("~".join((f["name"].replace(";", " ").replace("~", " "),
                "@" + f["cat"] if f["cat"] else ",".join("%X" % g for g in f["gr"]),
                "" if f["hue"] is None else str(f["hue"]), "" if f["slot"] is None else str(f["slot"]),
                "1" if f["on"] else "0", "%X:%d" % f["base"] if f.get("base") else "", f.get("broad") or ""))
                for f in st["filters"]))
            st["dirty_flt"] = st["open_flt"]
        def filter_sets():
            data = cats["data"]
            if data is None: return
            for f in st["filters"]:
                if f["cat"]: f["set"] = data.get(f["cat"], frozenset())
        def open_filters(): cats["wanted"] = True; st["open_flt"] = True; st["dirty_flt"] = True; schedule_save()
        def close_filters():
            remember_filter_pos(); dispose("flt"); st["open_flt"] = False; win["flt_checks"] = []; schedule_save()
        def remember_filter_pos():
            g = win.get("flt")
            if Kit.is_open(g): st["flt_x"], st["flt_y"] = int(g.GetX()), int(g.GetY())
        def toggle_flt_min():
            remember_filter_pos(); st["flt_min"] = not st["flt_min"]; st["dirty_flt"] = True; schedule_save()
        def filter_add(name, gr, hue, cat=None, broad=None):
            if len(st["filters"]) >= FILTERS_CAP:
                API.SysMsg(TITLE + ": %d filters is the most; remove one first." % FILTERS_CAP, HUE_ERR); return None
            f = {"name": name, "gr": tuple(gr), "cat": cat, "hue": hue, "slot": None, "on": True,
                 "set": frozenset(gr), "broad": broad}
            st["filters"].append(f); filter_sets(); save_filters(); return f
        def filter_preset(key):
            if safe(item_hold) is not None: filter_dropped(); return
            for k, cap in PRESETS:
                if k == key:
                    for f in st["filters"]:
                        if f["cat"] == key: API.SysMsg(TITLE + ": %s is already on the list." % cap, HUE_INFO); return
                    filter_add(cap, (), None, key)
        def filter_by_target():
            API.SysMsg(TITLE + ": target an item for the new filter.", HUE_INFO); pick_then("filter_targeted")
        def target_item(target):
            if not target: API.SysMsg(TITLE + ": cancelled.", HUE_INFO); return None
            it = Kit.find_item(target)
            if not it: API.SysMsg(TITLE + ": that isn't an item.", HUE_ERR); return None
            if it.IsContainer:
                API.SysMsg(TITLE + ": bags aren't sorted; target an item.", HUE_ERR); return None
            return it
        def filter_targeted(target):
            it = target_item(target)
            if it:
                filter_from(int(it.Graphic), int(SR["lit"].get(int(target), it.Hue or 0)) & 0x3FFF, str(it.Name or ""))
        def filter_from(graphic, hue, name):
            if not name: t = tile_of(graphic); name = str(t.Name or "") if t is not None else ""
            filter_add(clip(name or "0x%04X" % graphic, 30), (graphic,), hue, None, "exact")
        def filter_dropped():
            hold = safe(item_hold)
            if hold is None: return
            try:
                hs = int(Tz.get(hold, "Serial")); gr = int(Tz.get(hold, "Graphic"))
                hue = int(SR["lit"].get(hs, Tz.get(hold, "Hue"))) & 0x3FFF; home = int(Tz.get(hold, "Container"))
            except Exception: return
            if safe(lambda: bool(tile_of(gr).IsContainer), False):
                API.SysMsg(TITLE + ": bags aren't sorted; drop an item.", HUE_ERR); return
            filter_from(gr, hue, "")
            if home and home != 0xFFFFFFFF:
                import System
                Tz.call(None, "DropItem", (System.UInt32(hs), 0xFFFF, 0xFFFF, 0, System.UInt32(home), False), R.Actions)
        def filter_broader(i):
            if not 0 <= i < len(st["filters"]): return
            f = st["filters"][i]
            if f.get("base") is None and f["gr"]: f["base"] = (f["gr"][0], f["hue"] or 0)
            base = f.get("base")
            if base is None: return
            now = (f.get("broad") or ("category" if f["cat"] else ("exact" if f["hue"] is not None else "kind")))
            nxt = BROAD[(BROAD.index(now) + 1) % len(BROAD)]
            if nxt == "category":
                cat = category_of(base[0])
                if cat is None: nxt = "exact"
                else: f.update({"cat": cat, "hue": None, "gr": (base[0],)})
            if nxt != "category":
                f.update({"cat": None, "hue": base[1] if nxt == "exact" else None, "gr": (base[0],),
                          "set": frozenset((base[0],))})
            f["broad"] = nxt; filter_sets(); save_filters()
        def filter_move(i, d):
            j = i + d
            if 0 <= i < len(st["filters"]) and 0 <= j < len(st["filters"]):
                st["filters"][i], st["filters"][j] = st["filters"][j], st["filters"][i]; save_filters()
        def filter_remove(i):
            if 0 <= i < len(st["filters"]): del st["filters"][i]; save_filters()
        def filter_pick_bag(i):
            if not 0 <= i < len(st["filters"]): return
            st["flt_pick"] = st["filters"][i]
            API.SysMsg(TITLE + ": click a bag on the bags display, or target a bag in a slot.", HUE_INFO)
            pick_then("filter_bag_targeted", st["flt_pick"])
        def filter_bag_targeted(f, target):
            if st["flt_pick"] is not f: return
            st["flt_pick"] = None
            if not target: return
            slots = dict((b, i) for i, b in st["layout"]); s = int(target)
            for _ in range(8):
                if s in slots: f["slot"] = slots[s]; save_filters(); return
                it = Kit.find_item(s); s = int(it.Container or 0) if it else 0
                if not s: break
            API.SysMsg(TITLE + ": that isn't in a bag slot; put the bag in a slot first (Slots).", HUE_ERR)
        def filter_canvas_pick(slot_index):
            f, st["flt_pick"] = st["flt_pick"], None
            if f is None: return False
            f["slot"] = slot_index; save_filters(); API.CancelTarget(); return True
        def filter_poll():
            for i, chk in win.get("flt_checks") or ():
                if i < len(st["filters"]):
                    on = bool(safe(lambda: chk.IsChecked, st["filters"][i]["on"]))
                    if on == st["filters"][i]["on"]: continue
                    if safe(item_hold) is not None: Kit.set(chk, "IsChecked", not on); filter_dropped(); return
                    st["filters"][i]["on"] = on; save_filters(); return
        def drop_first(fn):
            def run(*args):
                if safe(item_hold) is None: fn(*args)
                else: filter_dropped()
            return run
        def build_filters():
            remember_filter_pos(); dispose("flt"); filter_sets(); M, GAP = Kit.MARGIN, Kit.GAP; n = len(st["filters"])
            row_h, h_add, h_prev = 28, 30 + 3 * 26 + 8, 40; list_h = max(row_h * 2, min(n, 12) * row_h + 8); w = 640
            h = (M + 30 + M if st["flt_min"] else M + 30 + GAP + h_prev + GAP + h_add + GAP + list_h + M)
            g, store, y = framed_window("flt", w, h, "SORT FILTERS", act("toggle_flt_min"), act("close_filters"))
            checks = []
            if not st["flt_min"]:
                IW = w - 2 * M; Kit.add_section(g, M, y, IW, h_prev)
                Kit.art_button(g, store, "sort", Kit.ART_PLAY, M + 12, y + 9, "Sort", SORT_TIP,
                               on_click=act("start_sort"))
                plan = safe(sort_plan); k = len(plan) if plan else 0
                Kit.add_label(g, "%s would move" % Kit.count(k, "item"), M + 100, y + 12, Kit.HUE_INFO)
                y += h_prev + GAP; Kit.add_section(g, M, y, IW, h_add, "ADD A FILTER"); bx = M + 12
                Kit.art_button(g, store, "add", Kit.ART_PLAY, bx, y + 28, "Add by target...",
                               "Target an item: the filter fills in from it", on_click=act("filter_by_target"))
                cols = 5; cw = (IW - 24) // cols
                for pi, (key, cap) in enumerate(PRESETS):
                    col, row = (pi + 1) % cols, (pi + 1) // cols
                    Kit.art_button(g, store, "pre_" + key, Kit.ART_OK, M + 12 + col * cw, y + 28 + row * 26,
                                   Kit.fit(cap, cw - 40), "Add the %s preset" % cap.lower(),
                                   on_click=act("filter_preset", key))
                y += h_add + GAP; Kit.add_section(g, M, y, IW, list_h)
                Kit.catcher(g, M, y, IW, list_h, act("filter_dropped"), "Drop an item here to add a filter")
                if not n:
                    Kit.add_label(g, "No filters yet. Press a preset, or Add by target.", M + 12, y + 8, Kit.HUE_INFO)
                else:
                    sa = G.CreateGumpScrollArea(M + 4, y + 4, IW - 8, list_h - 8)
                    Kit.catcher(sa, 0, 0, IW - 28, max(n * row_h, list_h - 8), act("filter_dropped"),
                                "Drop an item here to add a filter")
                    for i, f in enumerate(st["filters"]):
                        ry = i * row_h
                        chk = Kit.add_check(sa, "", 4, ry + 3, f["on"],
                                            "Use this filter (unticked: kept, moves nothing)")
                        checks.append((i, chk)); Kit.add_label(sa, Kit.fit(f["name"], 150), 30, ry + 5)
                        broad = f.get("broad") or ("category" if f["cat"] else
                                                   ("exact" if f["hue"] is not None else "kind"))
                        if f["cat"] and not f.get("base"): Kit.add_label(sa, "A preset", 186, ry + 5, Kit.HUE_INFO)
                        else:
                            Kit.art_button(sa, store, "m%d" % i, Kit.ART_PAGE, 186, ry + 2, "Match: " + broad,
                                           "Matches %s; click for the next" % BROAD_CAP[broad],
                                           on_click=act("filter_broader", i))
                        if f["slot"] is None or f["slot"] not in st["assign"]: cap, hue = "No bag", Kit.HUE_BAD
                        else: cap, hue = (short(bag_name(st["assign"][f["slot"]], False), 14), Kit.HUE_TEXT)
                        Kit.add_label(sa, cap, 330, ry + 5, hue)
                        Kit.art_button(sa, store, "b%d" % i, Kit.ART_PLAY, 424, ry + 2, "Bag...",
                                       "Click a bag on the bags display, or target a bag in a slot",
                                       on_click=act("filter_pick_bag", i))
                        Kit.art_button(sa, store, "u%d" % i, Kit.ART_PAGE, 508, ry + 2, None,
                                       "Move up (the first match wins)",
                                       on_click=Kit.once(act("filter_move", i, -1), (KEY, "flt_u", i)))
                        Kit.art_button(sa, store, "d%d" % i, Kit.ART_PAGE, 536, ry + 2, None,
                                       "Move down (the first match wins)",
                                       on_click=Kit.once(act("filter_move", i, 1), (KEY, "flt_d", i)))
                        Kit.art_button(sa, store, "x%d" % i, Kit.ART_CLOSE, 564, ry + 2, None, "Remove this filter",
                                       on_click=Kit.once(act("filter_remove", i), (KEY, "flt_x", i)))
                    g.Add(sa)
            sub_shown("flt", g, sub_window_moved); win["flt_checks"] = checks
        _srt = {"sync_at": 0.0}
        def sync_rules():
            checks = win["rule_checks"]
            if not checks or not Kit.is_open(win["srt"]): return False
            ticked, rows = {}, set()
            for idx, kind, chk in checks:
                if idx >= st["slots"]: continue
                rows.add(idx)
                try: on = bool(chk.IsChecked)
                except Exception: on = kind in st["rules"].get(idx, NO_RULE)[0]
                if on: ticked.setdefault(idx, set()).add(kind)
            changed = False
            for idx in rows:
                old = st["rules"].get(idx); graphics = old[1] if old is not None else ()
                kinds = frozenset(ticked.get(idx, ())); new = (kinds, graphics) if (kinds or graphics) else None
                if new != old:
                    changed = True; schedule_save()
                    if new is None: del st["rules"][idx]
                    else: st["rules"][idx] = new
            return changed
        def build_rules():
            sync_rules(); close_sub("srt"); M, GAP = Kit.MARGIN, Kit.GAP; w, row_h, h_act, h_foot = 580, 52, 40, 52
            list_h = min(st["slots"] * row_h + 8, 430)
            h = (M + 30 + M if st["srt_min"] else M + 30 + GAP + h_act + GAP + list_h + GAP + h_foot + M)
            g, store, y = framed_window("srt", w, h, "SORT RULES", act("toggle_win_min", "srt"),
                                        act("close_win", "srt"))
            checks = []
            if not st["srt_min"]:
                IW = w - 2 * M; Kit.add_section(g, M, y, IW, h_act)
                Kit.art_button(g, store, "sort", Kit.ART_PLAY, M + 12, y + 9, "Sort",
                               "Move matching items from your backpack and other slot bags into their bag, one at a "
                               "time", on_click=act("start_sort"))
                Kit.art_button(g, store, "stop", Kit.ART_CLOSE, M + 150, y + 9, "Stop", "Stop sorting",
                               on_click=act("stop_sort", None, True))
                Kit.add_label(g, "Tick what each slot's bag holds.", M + 250, y + 12, Kit.HUE_INFO); y += h_act + GAP
                Kit.add_section(g, M, y, IW, list_h); sa = G.CreateGumpScrollArea(M + 4, y + 4, IW - 8, list_h - 8)
                inner_w = IW - 8 - 20; gx = inner_w - 171 - Kit.text_w("+%d graphics" % SORT_GRAPHICS_CAP)
                for idx in range(st["slots"]):
                    ry = idx * row_h; kinds, graphics = st["rules"].get(idx, NO_RULE)
                    Kit.add_label(sa, "#%d" % (idx + 1), 6, ry + 5, Kit.HUE_TITLE)
                    if idx in st["assign"]: Kit.add_label(sa, short(bag_name(st["assign"][idx], False), 24), 44, ry + 5)
                    else: Kit.add_label(sa, "No bag in this slot", 44, ry + 5, Kit.HUE_INFO)
                    gl = Kit.add_label(sa, ("+%s" % Kit.count(len(graphics), "graphic"))
                                       if graphics else "", gx, ry + 5, Kit.HUE_INFO)
                    if graphics: gl.SetTooltip(", ".join("0x%04X" % v for v in graphics))
                    Kit.art_button(sa, store, "add%d" % idx, Kit.ART_PLAY, inner_w - 165, ry + 3,
                                   "Add...", "Target an item; slot #%d's bag holds its graphic too"
                                   % (idx + 1), on_click=act("add_rule_graphic", idx))
                    Kit.art_button(sa, store, "clr%d" % idx, Kit.ART_CLOSE, inner_w - 80, ry + 3,
                                   "Clear", "Forget the graphics added to slot #%d" % (idx + 1),
                                   on_click=act("clear_rule_graphics", idx))
                    x = 24
                    for key, cap, _gs in SORT_KINDS:
                        chk = Kit.add_check(sa, cap, x, ry + 27, key in kinds,
                                            "Slot #%d's bag holds %s" % (idx + 1, cap.lower()))
                        checks.append((idx, key, chk)); x += 36 + Kit.text_w(cap)
                g.Add(sa); y += list_h + GAP; Kit.add_section(g, M, y, IW, h_foot)
                Kit.add_label(g, "Sort moves one item every %.1f s from your backpack and other bags." % SORT_GAP,
                              M + 12, y + 8, Kit.HUE_INFO)
                Kit.add_label(g, "It stops when you pick something up or a bag is full.", M + 12, y + 28, Kit.HUE_INFO)
            sub_shown("srt", g, sub_window_moved, rule_checks=checks); _srt["sync_at"] = time.time() + 1.0
        def add_rule_graphic(idx):
            API.SysMsg(TITLE + ": target an item; slot #%d's bag will hold its graphic." % (idx + 1), HUE_INFO)
            pick_then("add_rule_graphic_to", idx)
        def add_rule_graphic_to(idx, target):
            if target:
                sync_rules()
                if idx >= st["slots"]: return
            it = target_item(target)
            if not it: return
            graphic = int(it.Graphic); kinds, graphics = st["rules"].get(idx, NO_RULE)
            if not graphic or graphic in graphics:
                API.SysMsg(TITLE + ": slot #%d's bag already holds that." % (idx + 1), HUE_INFO); return
            if len(graphics) >= SORT_GRAPHICS_CAP:
                API.SysMsg(TITLE + ": slot #%d already holds %d graphics; click Clear first."
                           % (idx + 1, SORT_GRAPHICS_CAP), HUE_ERR)
                return
            st["rules"][idx] = (kinds, graphics + (graphic,)); st["dirty_srt"] = True; save_settings()
            API.SysMsg(TITLE + ": slot #%d's bag holds graphic 0x%04X too." % (idx + 1, graphic), HUE_OK)
        def clear_rule_graphics(idx):
            sync_rules(); kinds, graphics = st["rules"].get(idx, NO_RULE)
            if not graphics: return
            if kinds: st["rules"][idx] = (kinds, ())
            else: st["rules"].pop(idx, None)
            st["dirty_srt"] = True; save_settings()
        def close_sub(k): remember_window_pos(); dispose(k)
        def remember_window_pos():
            for key, ax, ay in (("mgr", "mgr_x", "mgr_y"), ("trp", "trp_x", "trp_y"), ("srt", "srt_x", "srt_y"),
                                ("flt", "flt_x", "flt_y")):
                g = win.get(key)
                if Kit.is_open(g):
                    st[ax] = g.GetX(); st[ay] = g.GetY()
        def upkeep_windows():
            if cats["data"] is not st["cats_seen"]:
                st["cats_seen"] = cats["data"]; filter_sets(); st["dirty_flt"] = st["open_flt"]
            if st["open_flt"]:
                if st["dirty_flt"]: st["dirty_flt"] = False; build_filters()
                elif not Kit.is_open(win.get("flt")): st["open_flt"] = False; win["flt_checks"] = []
                else: filter_poll()
            for k, build in (("mgr", build_manager), ("trp", build_traps), ("srt", build_rules)):
                if not st["open_" + k]: st["dirty_" + k] = False
                elif st["dirty_" + k]: st["dirty_" + k] = False; build()
                elif not Kit.is_open(win[k]):
                    st["open_" + k] = False
                    if k in CHECKS_OF: win[CHECKS_OF[k]] = []
                elif k == "srt" and win["rule_checks"]:
                    now = time.time()
                    if now >= _srt["sync_at"]:
                        _srt["sync_at"] = now + 1.0
                        if sync_rules(): schedule_save()
        def grow_cells():
            mw, mh = H.max_w, H.max_h
            if mw <= 0 or mh <= 0: st["fit_seen"] = None; return
            want = (min(mw, MAX_CELL), min(mh, MAX_CELL))
            if want == (st["cell_w"], st["cell_h"]): st["fit_seen"] = None; return
            seen = st["fit_seen"]; st["fit_seen"] = (want, seen[1] + 1 if seen and seen[0] == want else 1)
            if st["fit_seen"][1] >= FIT_STABLE_TICKS or st["fit_pending"]:
                st["fit_pending"] = False; st["fit_seen"] = None; st["cell_w"], st["cell_h"] = want; frame_changed()
        def check_hook():
            if st["drive_fixed"] or not Kit.is_open(win["grid"]): return
            now = time.time()
            if H.hook_calls != st["hb_frame"]:
                st["hb_frame"] = H.hook_calls; st["hb_time"] = now
                if st["driving"]: st["driving"] = False
                return
            if not st["driving"] and now - st["hb_time"] > HOOK_STALL:
                st["driving"] = True
                if H.hook_calls == 0 and not st["drive_told"]:
                    st["drive_told"] = True
                    API.SysMsg(TITLE + ": draw hook isn't called; the script keeps the bags in place (they may "
                               "flicker when items move).", HUE_INFO)
        ACTIONS = {"add_rule_graphic": add_rule_graphic, "add_rule_graphic_to": add_rule_graphic_to,
                   "add_trap_bag": add_trap_bag, "add_trap_bag_to": add_trap_bag_to, "assign_slot": assign_slot,
                   "assign_slot_to": assign_slot_to, "auto_fill": auto_fill, "bag_close": bag_close,
                   "bag_min": bag_min, "bag_use": bag_use, "clear_all": clear_all,
                   "clear_rule_graphics": clear_rule_graphics, "clear_slot": clear_slot,
                   "close_filters": close_filters, "close_win": close_win, "disable": HOST.disable,
                   "filter_bag_targeted": filter_bag_targeted, "filter_broader": drop_first(filter_broader),
                   "filter_by_target": drop_first(filter_by_target), "filter_canvas_pick": filter_canvas_pick,
                   "filter_dropped": filter_dropped, "filter_move": drop_first(filter_move),
                   "filter_pick_bag": drop_first(filter_pick_bag), "filter_preset": filter_preset,
                   "filter_remove": drop_first(filter_remove), "filter_targeted": filter_targeted,
                   "fold_to_bar": fold_to_bar, "open_filters": open_filters, "open_win": open_win,
                   "quick_press": quick_press, "remove_trap_bag": remove_trap_bag,
                   "select_all_traps": select_all_traps, "set_min": set_min, "show_settings": HOST.show_settings,
                   "start_job": start_job, "start_sort": start_sort, "stop_all": stop_all, "stop_sort": stop_sort,
                   "toggle_bare": toggle_bare, "toggle_flt_min": toggle_flt_min, "toggle_win_min": toggle_win_min,
                   "user_collapse": user_collapse}
        def page_table(w):
            return (("LAYOUT  (Apply to use)", (
                        ("num", "slots", "Slots:", "Bag slots (%d-%d)" % (MIN_SLOTS, MAX_SLOTS), "", MIN_SLOTS,
                         MAX_SLOTS), ("num", "cols", "Columns:", "Slots per row outside a zone (0-%d, 0 = near-square)"
                         % MAX_SLOTS, "", 0, MAX_SLOTS),
                        ("num", "rows", "Rows:", "Rows of slots outside a zone (0-%d, 0 = near-square)"
                         % MAX_SLOTS, "", 0, MAX_SLOTS),
                        ("num", "scale", "Bag scale:", "The client's Container Scale, for every container (50-200)",
                         "%", 50, 200),
                        ("buttons", (("apply", Kit.ART_OK, "Apply", "Use the slots, columns, rows and scale above"),),
                         {"bdy": 4})), {"top": 32, "sh": 182, "ldy": 2, "fw": 60, "ugap": 6, "lw": w - 122}),
                    ("LOOK", (("slider", "opacity", "Bag opacity:", "How solid bag panels and art are (10-100%); "
                               "items stay solid", 10, 100,
                               {"lw": 158, "sdy": 6, "sw": 200, "ugap": 20, "vfmt": "%d%%", "h": 30}),
                              ("check", "trim", "Trim bags to their item area", "Hide bag art and butt the item areas "
                               "together (needs client access; zones always fill)"),
                              ("check", "items", "Scale items with the bags", "The client's option to draw items at "
                               "bag scale")), {"top": 32, "sh": 116, "ldy": 2}),
                    ("STATUS", (("note", short(status_line(), 64), {"key": "status", "h": 24}),
                                ("note", size_line(), {"key": "size"})), {"top": 32, "sh": 86}))
        cfg = Kit.Page(settings, page_table, save_settings)
        def _start():
            st["shutting"] = False
            if not API.Player: st["wait_player"] = True; return
            st["wait_player"] = False; pre = st["load_text"]; st["load_text"] = None
            if pre is None and Client.on_client_thread():
                st["wait_load"] = st["load_wanted"] = True; st["to_write"] = None; return
            st.update(wait_load=False, load_wanted=False, driving=False, drive_fixed=False, drive_told=False, job=None,
                      to_write=None, queue=[], reported=False, detached_at=0.0, flt_pick=None)
            anch["told"] = False; forget_names(); st["docked"], st["link_state"] = False, None
            API.RemoveSharedVar(LINK_CMD); _link["wish"] = 0.0
            fitov["cols"], fitov["cell"], fitov["area"], fitov["told"] = None, None, None, None; shrink["pct"] = None
            canvas_leave(); load_filters(); filter_sets(); st["canvas"] = None; JR["rd"] = Journal.reader()
            H.meas.clear(); H.opened = frozenset()
            if not R.tried: R.tried = True; init_interop()
            hooks = {"fit": layout_fit, "riding": attached}
            if canvas_ok(): hooks.update({"exact": True, "verify": True, "state": layout_state})
            HOST.layout_add(KEY, layout_gump, TITLE, hooks)
            if R.ok: unshrink_left()
            st["sort"] = None; SR.update({"armed": False, "lit": {}, "until": 0.0, "counts": {}, "status": None})
            if pre is not None: parse_cfg(pre[0])
            else: load_settings()
            st["open_mgr"] = st["dirty_mgr"] = st["want_mgr"]; st["open_trp"] = st["dirty_trp"] = st["want_trp"]
            st["open_srt"] = st["dirty_srt"] = st["want_srt"]
            if st["want_flt"]: cats["wanted"] = st["open_flt"] = st["dirty_flt"] = True
            if dock_wish() and not Kit.zone_up(KEY): st["minimized"] = True
            link_tick(); H.disabled, H.fail_streak, H.error = False, 0, ""
            if R.ok:
                try: on_main(scan_gumps)
                except Exception as e: H.error = "client thread: %s" % e
            else:
                HOST.refresh_settings(KEY)
                API.SysMsg(TITLE + ": no client access (%s); using basic pinning." % R.error, HUE_ERR)
            publish_layout(); st["dirty_frame"] = True; st["hb_frame"], st["hb_time"] = -1, time.time()
            for name, fn in (("bag.attach", attach_to), ("bag.grid_size", lambda: st["grid_wh"]),
                             ("bag.fit", paperdoll_fit), ("bag.cell", bag_cell), ("bag.shrink", bag_shrink),
                             ("bag.pack", bag_pack), ("bag.open_manager", act("open_win", "mgr")),
                             ("bag.open_traps", act("open_win", "trp")),
                             ("look.bags", lambda: st.update(dirty_frame=True, dirty_mgr=True, dirty_trp=True,
                                                             dirty_srt=True, dirty_flt=True))):
                cleanup.service(name, fn)
            Kit.hook_once(CV, "hooked", ("OnItemUpdated", on_bag_item))
        def _tick():
            if st["wait_player"]:
                if API.Player: _start()
                return
            if st["wait_load"]:
                if st["load_text"] is not None: _start()
                return
            while st["queue"]:
                action = st["queue"].pop(0); fn = ACTIONS[action[0]]
                try: fn(*action[1:])
                except Exception as e: API.SysMsg(TITLE + ": couldn't do that (%s)." % e, HUE_ERR)
            if st["shutting"]: return
            link_tick(); publish_layout()
            if R.ok and H.disabled and not st["reported"]:
                st["reported"] = True
                API.SysMsg(TITLE + ": draw hook stopped (%s); using basic pinning." % H.error, HUE_ERR)
                safe(lambda: on_main(restore_all)); st["dirty_frame"] = True
            if not Kit.is_open(win["bar"]) or not Kit.is_open(win["grid"]): st["dirty_frame"] = True
            if (H.icons or DEFAULT_ICONS) != st["icons_used"]: st["dirty_frame"] = True
            if R.ok and not H.disabled:
                check_hook()
                if st["driving"]:
                    try: on_main(guarded_tick)
                    except Exception as e: H.error = "client thread: %s" % e
                grow_cells(); canvas_tick()
            else:
                if st["canvas"] is not None: canvas_set(None)
                fallback_tick()
            if st["dirty_frame"] and not dragging(): st["dirty_frame"] = False; build_window()
            else:
                if attached(): follow_lead()
                refresh()
            upkeep_windows(); job_step(); now = time.time()
            if not 0 <= st["quick_at"] - now <= 1.0:
                st["quick_at"] = now + 1.0
                if win.get("quick_sig") is not None and win["quick_sig"] != quick_sig(): st["dirty_frame"] = True
            search_tick(now); sort_tick(now); sort_send(); canvas_say_tick(now)
            if (st["frame_x"], st["frame_y"]) != (st["saved_fx"], st["saved_fy"]) and st["save_in"] < 0 \
                    and not attached() and st["canvas"] != "alone" and now - st["detached_at"] >= DETACH_SETTLE \
                    and not HOST.layout_holds(KEY):
                schedule_save()
            if st["save_in"] > 0: st["save_in"] -= 1
            elif st["save_in"] == 0: remember_window_pos(); save_settings()
        def _thread_tick():
            if st["load_wanted"]:
                st["load_wanted"] = False; text = read_cfg()
                if st["wait_load"] and not st["shutting"]: st["load_text"] = (text,)
            canvas_thread()
            if cats["wanted"] and cats["data"] is None:
                cats["wanted"] = False
                try: build_cats(R.f_tiles)
                except Exception: cats["data"] = {}
            write_saved()
        def _interval(): return DRIVE_TICK if st["driving"] else TICK
        def _thread_wanted():
            return bool(st["load_wanted"] or st["to_write"] is not None or canvas_wanted()
                        or (cats["wanted"] and cats["data"] is None))
        load_settings()
        def _stop():
            st["shutting"] = True
            if st["wait_player"] or st["wait_load"]:
                st["wait_player"] = st["wait_load"] = st["load_wanted"] = False; st["load_text"] = None; return
            safe(stop_job); st.update(job=None, queue=[], sort=None); safe(lambda: clear_search(time.time()))
            sync_rules(); sync_trap_sel(); cleanup.close()
            held = HOST.layout_holds(KEY); HOST.layout_remove(KEY)
            if shrink["pct"] is not None: safe(lambda: bag_shrink(None))
            if st["attach"] is not None or held:
                st["attach"] = None; st["frame_x"], st["frame_y"] = st["saved_fx"], st["saved_fy"]
            st["grid_wh"] = None; st["docked"], st["link_state"] = False, None; API.SetSharedVar(LINK_STATE, "off")
            safe(canvas_leave); st["canvas"] = None
            if R.ok: safe(lambda: on_main(restore_all))
            remember_window_pos(); save_settings(); write_saved()
            for key in ("grid", "bar", "mgr", "trp", "srt", "flt"): dispose(key)
            st["open_mgr"] = st["open_trp"] = st["open_srt"] = st["open_flt"] = False; st["flt_pick"] = None
            win.update({"side_status": None, "trap_checks": [], "rule_checks": [], "search_box": None, "counts": [],
                        "flt_checks": []})
            st.update(bar_raw=None, grid_raw=None, grid_info=(None, False), slot_raws=())
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True,
                "config_height": cfg.height, "build_config": build_config, "poll_config": poll_config,
                "config_closed": config_closed, "interval": _interval, "thread_tick": _thread_tick,
                "thread_wanted": _thread_wanted}
    def _part_paperdoll():
        KEY = "character"; TITLE = "Paperdoll"; SETTINGS_KEY = "Character_settings"; POS_KEY = "Character_pos"
        MIN_KEY = "Character_min"; MINI_W, MINI_H = 240, 46; TRAY_ICON = 0x1F03; SLOT = 48; SLOT_GAP = 6
        CAPTION_UP = 16; DOLL_W, DOLL_H = 260, 237; STATS_H = 80; STATS_EVERY = 0.2
        WEIGHT_REARM = 0.92; WEIGHT_RED = 0.95; WEIGHT_BAR_W = 90; WEIGHT_BAR_MIN = 30
        WEIGHT_ALERT_SOUND = 0x04A
        WEIGHT_MAX_BASE, WEIGHT_MAX_PER_STR = 40, 3.5; DOLL_EVERY = 0.1; COMBINE_HOLE_GAP = Kit.GAP; PAIR_EVERY = 0.5
        SHRINK_STEP = 5; MALE_GUMP_OFFSET, FEMALE_GUMP_OFFSET = 50000, 60000; BAGS_WAIT = 2.0
        SHROUD_ANIM, GARGOYLE_SHROUD = 0x03CA, 0x0223; GARGOYLE_BODIES = (0x02B6, 0x02B7)
        try:
            import clr; from System import Array, Object, UInt32, UInt16, Int32, Double, Enum
            from System.Reflection import BindingFlags; HAVE_CLR = True
        except Exception: HAVE_CLR = False
        LAYERS = ((0x06, "helmet", "Helm", "Head"), (0x0D, "torso", "Chest", "Chest armour"),
            (0x13, "arms", "Arms", "Arms"), (0x07, "gloves", "Gloves", "Gloves"), (0x18, "legs", "Legs", "Leg armour"),
            (0x12, "earrings", "Ears", "Earrings"), (0x0A, "neck", "Neck", "Necklace / gorget"),
            (0x11, "tunic", "Tunic", "Tunic / surcoat (over the chest)"), (0x0C, "waist", "Belt", "Belt / half apron"),
            (0x03, "shoes", "Feet", "Shoes / boots"), (0x05, "shirt", "Shirt", "Shirt"), (0x16, "robe", "Robe", "Robe"),
            (0x14, "cloak", "Cloak", "Cloak / quiver"), (0x17, "skirt", "Kilt", "Skirt / kilt"),
            (0x04, "pants", "Pants", "Pants"), (0x01, "onehanded", "Main", "Main hand (one-handed weapon)"),
            (0x02, "twohanded", "Off", "Off hand (shield, two-handed weapon)"), (0x08, "ring", "Ring", "Ring"),
            (0x0E, "bracelet", "Brace", "Bracelet"), (0x09, "talisman", "Talis", "Talisman"),)
        ROWS = 5; LAYER_SET = set(l[0] for l in LAYERS); SLOT_LAYERS = tuple(l[0] for l in LAYERS)
        LAYER_ALT = {"neck": ("Necklace",), "onehanded": ("OneHanded",),
                     "twohanded": ("TwoHanded",), "earrings": ("Earrings",),
                     "bracelet": ("Bracelet",), "talisman": ("Talisman",)}
        L_ONE, L_TWO, L_SHOES, L_PANTS, L_SHIRT, L_HELMET, L_GLOVES, L_RING = (1, 2, 3, 4, 5, 6, 7, 8)
        L_TALIS, L_NECK, L_HAIR, L_WAIST, L_TORSO, L_BRACE, L_FACE, L_BEARD = (9, 10, 11, 12, 13, 14, 15, 16)
        L_TUNIC, L_EARS, L_ARMS, L_CLOAK, L_ROBE, L_SKIRT, L_LEGS = 17, 18, 19, 20, 22, 23, 24
        API_LAYER_NAME = dict((l[0], l[1]) for l in LAYERS)
        API_LAYER_NAME.update({L_HAIR: "hair", L_BEARD: "beard", L_FACE: "face"})
        ORDER_NORMAL = (L_CLOAK, L_SHIRT, L_PANTS, L_SHOES, L_LEGS, L_ARMS, L_TORSO, L_TUNIC, L_RING,
                        L_BRACE, L_FACE, L_GLOVES, L_SKIRT, L_ROBE, L_WAIST, L_NECK, L_HAIR, L_BEARD,
                        L_EARS, L_HELMET, L_ONE, L_TWO, L_TALIS)
        ORDER_QUIVER = (L_SHIRT, L_PANTS, L_SHOES, L_LEGS, L_ARMS, L_TORSO, L_TUNIC, L_RING, L_BRACE,
                        L_FACE, L_GLOVES, L_SKIRT, L_ROBE, L_CLOAK, L_WAIST, L_NECK, L_HAIR, L_BEARD,
                        L_EARS, L_HELMET, L_ONE, L_TWO, L_TALIS)
        ORDER_PARROT = (L_SHIRT, L_PANTS, L_SHOES, L_LEGS, L_ARMS, L_TORSO, L_TUNIC, L_CLOAK, L_RING,
                        L_BRACE, L_FACE, L_GLOVES, L_SKIRT, L_WAIST, L_NECK, L_HAIR, L_BEARD, L_EARS,
                        L_HELMET, L_ONE, L_TWO, L_TALIS, L_ROBE)
        DOLL_LAYERS = tuple(sorted(set(ORDER_NORMAL))); ROBES_OPEN = (0x9985, 0x9986, 0xA412, 0xA2CB, 0xA2CA)
        PAPERDOLL_BODY = {0x0190: 0x000C, 0x0192: 0x000C, 0x0191: 0x000D, 0x0193: 0x000D,
                          0x025D: 0x000E, 0x025F: 0x000E, 0x025E: 0x000F, 0x0260: 0x000F,
                          0x029A: 0x029A, 0x02B6: 0x029A, 0x029B: 0x0299, 0x02B7: 0x0299,
                          0x04E5: 0xC835, 0x03DB: 0x000C}
        FEMALE_BODIES = (0x0191, 0x0193, 0x025E, 0x0260, 0x029B, 0x02B7)
        GM_BODY, GM_BODY_HUE, GM_EXTRA = 0x03DB, 0x03EA, 0xC72B; M = Kit.MARGIN; PANEL_PAD = 8
        COL_PITCH = SLOT + SLOT_GAP; DOLL_AREA_H = ROWS * COL_PITCH - SLOT_GAP
        PANEL_W = PANEL_PAD * 2 + 2 * (2 * SLOT + SLOT_GAP) + 2 * PANEL_PAD + DOLL_W
        PANEL_H = PANEL_PAD * 2 + DOLL_AREA_H; SIDE_OWN = 4 * PANEL_PAD + 2 * (2 * SLOT + SLOT_GAP); DOLL_MIN_OWN = 100
        PANEL_W_MIN = SIDE_OWN + DOLL_MIN_OWN; DOLL_FIG = (150, 235); DOLL_INSET = 2; BOUNDS_CAP = 300
        W = PANEL_W + 2 * M; Y_BODY = M + 30 + Kit.GAP
        settings = {"stats": True, "combine": True, "beside": False, "left": False}; DEFAULTS = dict(settings)
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [], "sig": None, "doll_sig": None,
              "stats_at": 0.0, "doll_at": 0.0, "px": M, "attached": None, "beside_said": False, "layer_name": {},
              "wait_player": False, "wait_bags": None, "saved_min": False, "w_armed": True, "w_at": 0.0, "wbar": None,
              "fit": None, "k": 1.0, "py": None, "strip_w": None, "pw": PANEL_W, "col": None, "ph": PANEL_H,
              "rp": COL_PITCH, "pair": None, "pair_at": 0.0, "room": None, "room_fs": None, "told_shrink": None,
              "grew": False, "paired": False, "redraw_due": False}
        win = {"g": None, "c": {}, "store": ({}, {}), "slots": [], "raw": None, "doll": []}
        cleanup, queue, say = Kit.basics(st, TITLE)
        def load_settings():
            p = Kit.get_var(SETTINGS_KEY).split("|")
            if len(p) >= 2: settings["stats"] = p[0] == "1"; settings["combine"] = p[1] == "1"
            if len(p) >= 3: settings["beside"] = p[2] == "1"
            if len(p) >= 4: settings["left"] = p[3] == "1"
            st["saved_min"] = bool(Kit.load_min(MIN_KEY))
        def save_settings():
            Kit.put_var(SETTINGS_KEY, "|".join(["1" if settings[k] else "0"
                                                for k in ("stats", "combine", "beside", "left")] + ["0"]))
        def save_state():
            if not st.get("wait_player"): Kit.save_min(MIN_KEY, st["minimized"] and not st["docked"])
        def save_place(): Kit.save_pos(POS_KEY, win["g"])
        class Box(object): pass
        R = Box(); R.tried = R.ok = False; R.error, R.pixel_n = "", 0
        for k in ("m_animid", "m_covered", "MobileType", "cursor", "SlotItem", "DollPiece", "m_pixel", "gumps",
                  "f_tiles", "tiles"):
            setattr(R, k, None)
        def init_interop():
            if not HAVE_CLR: R.error = "clr module unavailable"; return
            try:
                asm = API.GetType().Assembly; clr.AddReference(asm)
                from ClassicUO.Game.UI.Controls import ItemGump, Control
                stat = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
                inst = BindingFlags.Instance | BindingFlags.NonPublic
                anyi = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
                cli = asm.GetType("ClassicUO.Client")
                R.p_game = cli.GetProperty("Game", stat) if cli is not None else None
                gct = asm.GetType("ClassicUO.GameController")
                R.p_uo = gct.GetProperty("UO", anyi) if gct is not None else None
                uot = asm.GetType("ClassicUO.UltimaOnline")
                R.p_cursor = uot.GetProperty("GameCursor", anyi) if uot is not None else None; R.ItemGump = ItemGump
                try:
                    class SlotItem(ItemGump):
                        def Contains(self, x, y): return True
                    R.SlotItem = SlotItem
                except Exception: R.SlotItem = None
                try:
                    class DollPiece(ItemGump):
                        def Contains(self, x, y):
                            try:
                                k = self.va_k
                                if R.pixel_n == 4: a = [UInt32(self.va_gid), Int32(int(x)), Int32(int(y)), Double(k)]
                                else: a = [UInt32(self.va_gid), Int32(int(x / k)), Int32(int(y / k))]
                                return bool(R.m_pixel.Invoke(R.gumps, Array[Object](a)))
                            except Exception: return True
                        def OnMouseDown(self, x, y, button):
                            self.va_down = True; ItemGump.OnMouseDown(self, x, y, button)
                        def OnMouseUp(self, x, y, button): self.va_down = False; ItemGump.OnMouseUp(self, x, y, button)
                        def Update(self):
                            ItemGump.Update(self)
                            if self.va_down: doll_lifted(self)
                    R.DollPiece = DollPiece
                except Exception: R.DollPiece = None
                ga = asm.GetType("ClassicUO.Game.GameActions"); R.m_equip = ga.GetMethod("Equip", stat)
                R.m_swap = ga.GetMethod("QueueEquipSwap", stat); R.LayerType = asm.GetType("ClassicUO.Game.Data.Layer")
                ctl = clr.GetClrType(Control); R.f_bounds = ctl.GetField("_bounds", inst)
                R.Point = clr.GetPythonType(ctl.GetProperty("Location").PropertyType)
                for name in ("m_equip", "m_swap", "LayerType", "f_bounds", "p_game", "p_uo", "p_cursor"):
                    if getattr(R, name) is None: raise Exception("client member not found: " + name)
                R.ok = True
            except Exception as e: R.ok = False; R.error = str(e); return
            try:
                game = R.p_game.GetValue(None, None); uo = R.p_uo.GetValue(game, None) if game is not None else None
                gp = uo.GetType().GetProperty("Gumps") if uo is not None else None
                R.gumps = gp.GetValue(uo, None) if gp is not None else None; R.m_pixel, R.pixel_n = None, 0
                if R.gumps is not None:
                    for m in R.gumps.GetType().GetMethods():
                        n = len(m.GetParameters())
                        if m.Name == "PixelCheck" and n in (3, 4) and n > R.pixel_n: R.m_pixel, R.pixel_n = m, n
            except Exception: R.gumps = R.m_pixel = None
            if R.m_pixel is None: R.DollPiece = None
            R.f_tiles = safe(tile_field)
            try:
                pdi = asm.GetType("ClassicUO.Game.UI.Controls.PaperDollInteractable")
                R.m_animid = pdi.GetMethod("GetAnimID", stat) if pdi is not None else None
                R.animid_n = (int(R.m_animid.GetParameters().Length) if R.m_animid is not None else 0)
            except Exception: R.m_animid = None
            try:
                R.MobileType = asm.GetType("ClassicUO.Game.GameObjects.Mobile")
                R.m_covered = (R.MobileType.GetMethod("IsCovered", stat) if R.MobileType is not None else None)
            except Exception: R.m_covered = None
        LAYER_ENUMS = {}
        def layer_enum(layer):
            e = LAYER_ENUMS.get(layer)
            if e is None: e = LAYER_ENUMS[layer] = Enum.ToObject(R.LayerType, layer)
            return e
        WORN_DATA = {}; WORN_DATA_CAP = 256
        def world(): raw = win["raw"]; return None if raw is None else raw.World
        def player_raw(): w = world(); return None if w is None else w.Player
        def held():
            try:
                cur = R.cursor
                if cur is None:
                    game = R.p_game.GetValue(None, None); uo = R.p_uo.GetValue(game, None) if game is not None else None
                    cur = R.cursor = R.p_cursor.GetValue(uo, None) if uo is not None else None
                h = cur.ItemHold
                if h.Enabled and not h.IsFixedPosition:
                    layer = tile_layer(int(h.Graphic))
                    if layer not in LAYER_SET:
                        try: layer = int(h.Layer)
                        except Exception: layer = 0
                    return int(h.Serial), bool(h.IsWearable), layer
            except Exception: pass
            return None
        def doll_lifted(piece):
            try:
                cur = R.cursor
                if cur is None:
                    game = R.p_game.GetValue(None, None); uo = R.p_uo.GetValue(game, None) if game is not None else None
                    cur = R.cursor = R.p_cursor.GetValue(uo, None) if uo is not None else None
                h = cur.ItemHold
                if h.Enabled and int(h.Serial) == int(piece.LocalSerial):
                    piece.va_down = False; h.IsGumpTexture = False; h.MouseOffset = R.Point(0, 0)
            except Exception: piece.va_down = False
        def tile_layer(graphic):
            try:
                arr = R.tiles
                if arr is None:
                    if R.f_tiles is None: return 0
                    arr = R.tiles = R.f_tiles.GetValue(None)
                return 0 if arr is None or graphic < 0 or graphic >= arr.Length else int(arr[graphic].Layer)
            except Exception: return 0
        def set_pos(c, x, y): c.Location = R.Point(x, y)
        on_disposed = Kit.disposer(KEY, st, win); BLOCK_W = 2 * SLOT + SLOT_GAP
        def slot_xy(i):
            col, row = divmod(i, ROWS)
            if col < 2: x = st["px"] + PANEL_PAD + col * COL_PITCH
            else: x = st["px"] + st["pw"] - PANEL_PAD - BLOCK_W + (col - 2) * COL_PITCH
            return x, panel_y() + PANEL_PAD + int(round(row * st["rp"]))
        def zoned_lock(): return bool(HOST.layout_locked(KEY))
        def mid_rect():
            x = st["px"] + 2 * PANEL_PAD + BLOCK_W
            return (x, panel_y() + PANEL_PAD, max(1, st["pw"] - SIDE_OWN), max(1, st["ph"] - 2 * PANEL_PAD))
        def panel_y(): py = st["py"]; return Y_BODY if py is None else py
        FIT_K_MIN, FIT_K_MAX = 0.4, 2.0; STRIP_MIN_W = 300
        def layout_fit(w, h, mode):
            new = (int(w), int(h)) if (w is not None and h is not None) else None
            if new != st["fit"] or (mode == "again" and new is not None and not st["paired"]):
                st["fit"] = new; st["pair"] = pair_rects() if new is not None else None; st["pair_at"] = time.time()
                queue("redraw")()
        def pair_rects():
            if st["attached"] is None: return None
            try: pr = HOST.layout_pair(KEY, "bag")
            except Exception: return None
            if not pr or pr[0] is None or pr[1] is None: return None
            return (tuple(int(v) for v in pr[0]), tuple(int(v) for v in pr[1]))
        def pair_hole(x, y, fw, fh, pr):
            (tx, ty, tw, th), (bx, by, bw, bh) = pr
            if abs((y + fh) - by) > 2 * SNAP_DIST: return None
            hx0, hx1 = max(0, bx - x), min(fw, bx + bw - x); hw = hx1 - hx0 - 2 * M
            if hw < 40: return None
            half = COMBINE_HOLE_GAP // 2; hy = fh + half; hh = (by + bh - y) - hy - M
            if hh < 20: return None
            st["room"] = (hw, hh); fs = fit_scale(hw, hh); st["room_fs"] = fs
            need = fs[1] if fs is not None else grid_need(hw, hh); st["grew"] = need > hh
            if need > hh:
                sh = int(Kit.screen()[1]); cap = (sh - y - M - hy) if sh > 0 else need
                hh = max(hh, min(need, cap))
            return (hx0 + M, hy, hw, hh)
        def scale_ctrl(c, raw=False, flushed=False):
            k = st["k"]
            if abs(k - 1.0) < 0.001 or c is None: return
            with Kit.quiet:
                if not raw and not flushed: Kit.flush()
                rc = c if raw else Kit.client_control(c)
                if rc is None: return
                if str(rc.GetType().Name) == "GumpPicTiled": rc.ScaleTiledTexture = True
                rc.ApplyScale(k, True, True, False)
        def cell_info(tall=None):
            fn = bag_service("bag.cell")
            if fn is None: return None
            try:
                v = fn() if tall is None else fn(tall); cw, ch, gap, n, side = v[0], v[1], v[2], v[3], v[4]
                cur, own, floor = (v[5], v[6], v[7]) if len(v) >= 8 else (100, 100, 100)
            except Exception: return None
            if n <= 0 or cw <= 0 or ch <= 0 or cur <= 0 or own <= 0: return None
            if cur != own: cw, ch = cw * own / float(cur), ch * own / float(cur)
            return cw, ch, gap, n, side, own, min(floor, own)
        def need_at(ci, f, width):
            cw0, ch0, gap, n, side = ci[0], ci[1], ci[2], ci[3], ci[4]; cw = int(math.ceil(cw0 * f - 0.01))
            ch = int(math.ceil(ch0 * f - 0.01)); aw = max(cw, width - side)
            cols = max(1, min(n, (aw + gap) // (cw + gap))); rows = int(math.ceil(n / float(cols)))
            return rows, rows * ch + (rows - 1) * gap, cw + side
        def grid_need(width, tall=1 << 20):
            fn = bag_service("bag.pack")
            if fn is not None:
                try: got = fn(width, 1 << 20)
                except Exception: got = None
                if got is not None: return got[1]
            ci = cell_info(tall); return 120 if ci is None else need_at(ci, 1.0, width)[1]
        def fit_scale(hw, hh):
            fn = bag_service("bag.pack")
            if fn is not None:
                try: got = fn(hw, hh)
                except Exception: got = None
                if got is not None: return got
            ci = cell_info(hh)
            if ci is None: return None
            own, floor = ci[5], ci[6]; told = st["told_shrink"]; p = own
            for _ in range(int(own - floor) // SHRINK_STEP + 2):
                rows, need, wneed = need_at(ci, p / float(own), hw)
                spare = 3 * rows if (told is not None and p > told) else 0
                if (need + spare <= hh and wneed <= hw) or p <= floor: return (None if p >= own else p), need
                p = max(floor, p - SHRINK_STEP)
        COL_ROWS = 10; COL_PITCH_MIN, COL_PITCH_MAX = 20, 26; COL_BAR_H = 14
        COL_NEED_H = 2 * 8 + COL_ROWS * COL_PITCH_MIN + COL_BAR_H
        def col_w():
            if geo["col_w"] is None:
                widest = max(Kit.text_w(t) for t in ("Stamina 999/999", "Followers 99/99", "Gold 9,999,999",
                                                     "Weight 0000/0000", "Mana 999/999", "HP 999/999"))
                geo["col_w"] = max(WEIGHT_BAR_MIN, widest) + 2 * STATS_IN + 4
            return geo["col_w"]
        def choose_fit(bw, room):
            fig = DOLL_FIG; cands = []
            if settings["stats"]:
                if bw >= STRIP_MIN_W: cands.append(("strip", bw, room - STATS_H - Kit.GAP))
                cands.append(("col", bw - col_w() - Kit.GAP, room))
            else: cands.append(("none", bw, room))
            fw_, fh_ = float(max(1, fig[0])), float(max(1, fig[1])); best = None
            for mode, aw, ah in cands:
                if mode == "col" and ah < COL_NEED_H: continue
                k = min(aw / float(PANEL_W_MIN), ah / float(PANEL_H), FIT_K_MAX)
                if k < FIT_K_MIN: continue
                f = min((aw - 2 * PANEL_PAD * k) / fw_, (ah - 2 * PANEL_PAD * k) / fh_)
                if best is None or f > best[0] + 0.001 or (f > best[0] - 0.001 and k > best[4]):
                    best = (f, mode, aw, ah, k)
            if best is None:
                k = min(bw / float(PANEL_W_MIN), room / float(PANEL_H), FIT_K_MAX)
                return "none", bw, room, max(FIT_K_MIN, k)
            return best[1], best[2], best[3], best[4]
        def doll_room(bw):
            doll = int(math.ceil(FIT_K_MIN * PANEL_H)) + 1
            if not settings["stats"]: return doll
            return doll + STATS_H + Kit.GAP if bw >= STRIP_MIN_W else max(doll, COL_NEED_H)
        def fitted_geom(fw, fh, combined):
            bx, by = M, Y_BODY; bw, bh = max(1, fw - 2 * M), max(1, fh - Y_BODY - M); gap = COMBINE_HOLE_GAP
            room = bh
            if combined:
                least = min(bh, max(doll_room(bw), (bh - gap) // 2)); room = max(bh - grid_need(bw) - gap, least)
                room = max(bh - grid_need(bw, max(1, bh - room - gap)) - gap, least)
            mode, aw, ah, k = choose_fit(bw, room)
            pw = max(PANEL_W_MIN, int(round(aw / k))); ph = max(PANEL_H, int(round(ah / k))); pph = int(round(ph * k))
            sh = (STATS_H + Kit.GAP) if mode == "strip" else 0; top, left = by, bx
            if combined: used = max(room, pph + sh); hole = (bx, by + used + gap, bw, max(1, bh - used - gap))
            else: hole = None
            ys = (top + pph + Kit.GAP) if mode == "strip" else None; strip_w = bw if mode == "strip" else None
            col = (bx + bw - col_w(), top, col_w(), pph) if mode == "col" else None
            return (k, int(round(left / k)), int(round(top / k)), ys, strip_w, hole, (bx, top + pph), pw, col, ph)
        def body_h(): return PANEL_H + (Kit.GAP + STATS_H if settings["stats"] else 0)
        def stacked_geom(gw, gh):
            iw = max(PANEL_W, gw); w = iw + 2 * M; px = M + (iw - PANEL_W) // 2
            yh = Y_BODY + body_h() + COMBINE_HOLE_GAP; hole = (M + (iw - gw) // 2, yh, gw, gh)
            return w, yh + gh + M, px, hole
        def beside_geom(gw, gh):
            w = M + PANEL_W + COMBINE_HOLE_GAP + gw + M
            hx, px = (M, M + gw + COMBINE_HOLE_GAP) if settings["left"] else (M + PANEL_W + COMBINE_HOLE_GAP, M)
            return w, Y_BODY + max(body_h(), gh) + M, px, (hx, Y_BODY, gw, gh)
        def combined_geom(gw, gh):
            if not settings["beside"]:
                w, h, px, hole = stacked_geom(gw, gh); sh = int(Kit.screen()[1])
                if sh <= 0 or h <= sh: return w, h, px, hole
                if not st["beside_said"]:
                    st["beside_said"] = True
                    API.SysMsg(TITLE + ": bag grid too tall to stack; bags go beside the doll.", Kit.HUE_INFO)
            return beside_geom(gw, gh)
        def hole_guess():
            if settings["beside"]:
                return ((M, Y_BODY) if settings["left"] else (M + PANEL_W + COMBINE_HOLE_GAP, Y_BODY))
            return M, Y_BODY + body_h() + COMBINE_HOLE_GAP
        def frame_with_hole(g, w, h, hole):
            hx, hy, hw, hh = hole; base = Kit.WINDOW_BG; s = [Kit.pic_size(base + i) for i in range(9)]
            tl, t, tr, l, c, r, bl, b, br = s; parts = []
            for rx, ry, rw, rh in ((0, 0, w, hy), (0, hy, hx, h - hy), (hx + hw, hy, w - hx - hw, h - hy),
                                   (hx, hy + hh, hw, h - hy - hh)):
                if rw > 0 and rh > 0: parts.append(Kit.add_tiled(g, base + 4, rx, ry, rw, rh))
            if all(p[0] > 0 and p[1] > 0 for p in s):
                parts += [Kit.add_tiled(g, base + 1, tl[0], 0, w - tl[0] - tr[0], t[1]),
                          Kit.add_tiled(g, base + 7, bl[0], h - b[1], w - bl[0] - br[0], b[1]),
                          Kit.add_tiled(g, base + 3, 0, tl[1], l[0], h - tl[1] - bl[1]),
                          Kit.add_tiled(g, base + 5, w - r[0], tr[1], r[0], h - tr[1] - br[1]),
                          Kit.add_pic(g, base + 0, 0, 0), Kit.add_pic(g, base + 2, w - tr[0], 0),
                          Kit.add_pic(g, base + 6, 0, h - bl[1]), Kit.add_pic(g, base + 8, w - br[0], h - br[1])]
            cw, ch = Kit.pic_size(Kit.CORNER_ART)
            if cw and ch and Kit.CORNER_ART:
                for cx, cy in ((0, 0), (w - cw, 0), (0, h - ch), (w - cw, h - ch)):
                    if cx < hx + hw and cx + cw > hx and cy < hy + hh and cy + ch > hy: continue
                    parts.append(Kit.add_pic(g, Kit.CORNER_ART, cx, cy))
            with Kit.quiet: Kit._frame_parts[g] = [p for p in parts if p is not None]
        def build_window():
            old, win["g"] = win["g"], None; clear_slots(); store = ({}, {}); c = {}; slots = []; att = st["attached"]
            hole = None
            st.update({"px": M, "k": 1.0, "py": None, "strip_w": None, "pw": PANEL_W, "col": None, "ph": PANEL_H,
                       "rp": COL_PITCH})
            fit = st["fit"] if not st["minimized"] else None; spx = M
            if Kit.is_open(old): x, y = old.GetX(), old.GetY()
            else: x, y = Kit.load_pos(POS_KEY, (200, 120), (W, Y_BODY + body_h() + M))
            spot = HOST.layout_rect(KEY); st["paired"] = False
            if spot is not None: x, y = spot[0], spot[1]
            if st["minimized"]:
                w, h = MINI_W, MINI_H; g = G.CreateGump(True, True)
                c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
                Kit.set_text(c["status"], TITLE + " & bags" if att is not None else TITLE)
            else:
                w, h = W, Y_BODY + body_h() + M; g = G.CreateGump(False, True)
                if fit is not None:
                    w, h = fit; hole2 = pair_hole(x, y, w, h, st["pair"]) if (att is not None and st["pair"]) else None
                    if hole2 is not None:
                        half = COMBINE_HOLE_GAP // 2; st["paired"] = True
                        (k, st["px"], st["py"], ys_fit, st["strip_w"], _h, sxy, st["pw"],
                         st["col"], st["ph"]) = fitted_geom(w, h - half + M, False)
                        hole = hole2; h = hole[1] + hole[3] + M
                    else:
                        (k, st["px"], st["py"], ys_fit, st["strip_w"], hole, sxy, st["pw"],
                         st["col"], st["ph"]) = fitted_geom(w, h, att is not None)
                    st["k"] = k; st["rp"] = (st["ph"] - 2 * PANEL_PAD - SLOT) / float(ROWS - 1); spx = sxy[0]
                    if hole is not None:
                        frame_with_hole(g, w, h, hole); att["dx"], att["dy"] = hole[0], hole[1]
                        if hole2 is None:
                            st["room"] = (hole[2], hole[3]); st["room_fs"] = fit_scale(hole[2], hole[3])
                            st["grew"] = (st["room_fs"] is not None and st["room_fs"][1] > hole[3])
                        tell_bags((hole[2], hole[3])); fs = st["room_fs"]
                        tell_shrink(fs[0] if fs is not None else None)
                    else: Kit.add_window_frame(g, w, h); tell_bags(None)
                elif att is not None and att.get("grid_wh"):
                    gw, gh = att["grid_wh"]; w, h, st["px"], hole = combined_geom(int(gw), int(gh))
                    frame_with_hole(g, w, h, hole); att["dx"], att["dy"] = hole[0], hole[1]
                else: Kit.add_window_frame(g, w, h)
                if fit is None: tell_bags(None)
                px = st["px"]; extra = None
                if att is not None:
                    extra = [("traps", Kit.ART_PAGE, "Traps", "Pick the bags Trap and Untrap cast on",
                              queue("bag_traps")),
                             ("bags", Kit.ART_PAGE, "Slots", "Put a bag in each slot", queue("bag_mgr"))]
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"), extra=extra)
                body = []; py = panel_y(); pw, ph = st["pw"], st["ph"]; body.append(Kit.add_section(g, px, py, pw, ph))
                body.append(Kit.catcher(g, px, py, pw, ph, lambda *a: None, None, movable=not zoned_lock()))
                mx, my, mw, mh = mid_rect(); c["doll_bg"] = Kit.add_tiled(g, 0x243A, mx, my, mw, mh, 0.35)
                body.append(c["doll_bg"])
                c["doll_drop"] = Kit.catcher(g, mx, my, mw, mh, queue(("drop", 0)),
                                             "Drop an item here to wear it", movable=True)
                body.append(c["doll_drop"])
                for i, (layer, name, cap, tip) in enumerate(LAYERS):
                    sx, sy = slot_xy(i); body.extend(Kit.gold_box(g, sx, sy, SLOT, SLOT))
                    drop = G.CreateGumpColorBox(0.01, "#000000"); drop.SetRect(sx, sy, SLOT, SLOT)
                    Kit.on_click(drop, queue(("drop", layer))); stip = tip + ": drop an item to wear it"
                    drop.SetTooltip(stip); g.Add(drop)
                    lbl = Kit.add_label(g, cap, sx + (SLOT - Kit.text_w(cap)) // 2,
                                        sy + SLOT - CAPTION_UP, Kit.HUE_TEXT)
                    lbl.SetAcceptMouseInput(False); body.append(drop); body.append(lbl)
                    slots.append({"layer": layer, "name": name, "x": sx, "y": sy, "drop": drop,
                                  "label": lbl, "serial": 0, "ctrl": None, "raw": None, "tip": stip})
                scale_body(body)
                if fit is not None: ys, spw, sx0 = ys_fit, st["strip_w"], spx
                else: ys = (Y_BODY + PANEL_H + Kit.GAP) if settings["stats"] else None; spw, sx0 = PANEL_W, px
                if ys is not None:
                    Kit.add_section(g, sx0, ys, spw, STATS_H)
                    Kit.catcher(g, sx0, ys, spw, STATS_H, lambda *a: None, None, movable=not zoned_lock())
                    for i in range(3):
                        c["stats%d" % (i + 1)] = Kit.add_label(g, "", sx0 + 10, ys + 8 + 24 * i, Kit.HUE_TEXT)
                    build_weight_bar(g, c, sx0, ys + 56)
                elif st["col"] is not None: build_stats_col(g, c, st["col"])
            xy = Kit.show_window(g, x, y, w, h, KEY, st["minimized"] and st["docked"], on_disposed(g), save_place,
                                 win, {"g": g, "c": c, "store": store, "slots": slots})
            to_slot(KEY, g, xy); hooks = geo["hooks"]
            if hooks is not None: hooks["verify"] = not st["paired"]
            win["raw"] = Kit._raw_gump(g) if R.ok else None
            if att is not None: att["g"], att["raw"] = g, None
            sync_attached()
            st.update({"sig": None, "doll_sig": None, "stats_at": 0.0, "stats_key": None, "doll_at": 0.0, "wbar": None})
            Kit.dispose(old)
        wnd = None; geo = {"col_w": None, "bounds": {}, "need": [], "redo": False, "order": [], "hooks": None}
        def tell_bags(room):
            if room is None: st["room"] = None; tell_shrink(None)
            if room == st.get("told_bags"): return
            st["told_bags"] = room; fn = bag_service("bag.fit")
            if fn is not None: safe(lambda: fn(*(room or (None, None))))
        def tell_shrink(pct):
            if pct == st["told_shrink"]: return
            st["told_shrink"] = pct; fn = bag_service("bag.shrink")
            if fn is not None: safe(lambda: fn(pct))
        def scale_body(ctrls):
            if abs(st["k"] - 1.0) < 0.001: return
            Kit.flush()
            for ctl in ctrls:
                if ctl is not None: scale_ctrl(ctl, flushed=True)
        def clear_slots():
            for s in win["slots"]:
                if s["ctrl"] is not None: Kit.dispose(s["ctrl"]); s["ctrl"] = None
            win["slots"] = []; clear_doll()
        def clear_doll():
            for p in win["doll"]: Kit.dispose(p)
            win["doll"] = []
        def dock_state(): return "docked" if st["docked"] else ("collapsed" if st["minimized"] else "open")
        def find_layer(name):
            known = st["layer_name"].get(name)
            if known is not None:
                try: return API.FindLayer(known)
                except Exception: return None
            for spelling in (name,) + LAYER_ALT.get(name, ()):
                try: it = API.FindLayer(spelling)
                except Exception: it = None
                if it: st["layer_name"][name] = spelling; return it
            return None
        def worn(p, keep=None):
            out = {}
            if R.ok and p is not None:
                try:
                    wd = WORN_DATA
                    for layer in DOLL_LAYERS:
                        it = p.FindItemByLayer(layer_enum(layer))
                        if it is None: continue
                        serial, graphic, hue = int(it.Serial), int(it.Graphic), int(it.Hue)
                        if keep is not None: keep[layer] = it
                        k = (serial, graphic); dat = wd.get(k)
                        if dat is not None: out[layer] = (serial, graphic, hue) + dat; continue
                        try: d = it.ItemData; dat = (int(d.AnimID), bool(d.IsPartialHue), bool(d.IsContainer))
                        except Exception:
                            try: d = API.FindItem(serial).GetItemData()
                            except Exception: d = None
                            if d is not None: dat = (int(d.AnimID or 0), bool(d.IsPartialHue), bool(d.IsContainer))
                            else: out[layer] = (serial, graphic, hue, 0, False, False); continue
                        if len(wd) >= WORN_DATA_CAP: wd.clear()
                        wd[k] = dat; out[layer] = (serial, graphic, hue) + dat
                    who = (int(p.Graphic), int(p.Hue), bool(p.IsFemale)); return out, who
                except Exception:
                    out = {}
                    if keep is not None: keep.clear()
            try: ap = API.Player
            except Exception: ap = None
            if not ap: return out, None
            for layer in DOLL_LAYERS:
                it = find_layer(API_LAYER_NAME[layer])
                if not it: continue
                try: serial, graphic, hue = (int(it.Serial or 0), int(it.Graphic or 0), int(it.Hue or 0))
                except Exception: continue
                anim, partial, cont = 0, False, False
                try:
                    d = it.GetItemData()
                    if d is not None:
                        anim, partial, cont = (int(d.AnimID or 0), bool(d.IsPartialHue), bool(d.IsContainer))
                except Exception: pass
                out[layer] = (serial, graphic, hue, anim, partial, cont)
            try: graphic = int(ap.Graphic or 0x0190)
            except Exception: graphic = 0x0190
            try: phue = int(ap.Hue or 0)
            except Exception: phue = 0
            who = (graphic, phue, graphic in FEMALE_BODIES); return out, who
        def body_gump(graphic, hue, female):
            if graphic == GM_BODY: return PAPERDOLL_BODY[GM_BODY], GM_BODY_HUE, GM_EXTRA
            body = PAPERDOLL_BODY.get(graphic)
            if body is None: body = 0x000D if female else 0x000C
            return body, hue, 0
        def anim_gump(mob_graphic, item_graphic, anim, female):
            if R.m_animid is not None:
                try:
                    if R.animid_n == 4: args = [UInt16(mob_graphic), UInt16(item_graphic), UInt16(anim), bool(female)]
                    else: args = [UInt16(mob_graphic), UInt16(anim), bool(female)]
                    v = int(R.m_animid.Invoke(None, Array[Object](args)))
                    if v > 0: return v
                except Exception: R.m_animid = None
            if anim == SHROUD_ANIM and mob_graphic in GARGOYLE_BODIES: anim = GARGOYLE_SHROUD
            first, second = (FEMALE_GUMP_OFFSET, MALE_GUMP_OFFSET) if female else (MALE_GUMP_OFFSET, FEMALE_GUMP_OFFSET)
            gid = anim + first
            if Kit.pic_size(gid) == (0, 0):
                alt = anim + second
                if Kit.pic_size(alt) != (0, 0): return alt
            return gid
        def covered(layer, gfx, p=None):
            if R.m_covered is not None and R.ok and p is not None:
                with Kit.quiet: return bool(R.m_covered.Invoke(None, Array[Object]([p, layer_enum(layer)])))
            robe = gfx.get(L_ROBE); pants = gfx.get(L_PANTS)
            if layer == L_SHOES:
                if gfx.get(L_LEGS) is not None or pants == 0x1411: return True
                if pants in (0x0513, 0x0514) or robe == 0x0504: return True
            elif layer == L_PANTS:
                if gfx.get(L_LEGS) is not None or robe == 0x0504: return True
                if pants in (0x01EB, 0x03E5, 0x03EB):
                    skirt = gfx.get(L_SKIRT)
                    if skirt is not None and skirt not in (0x01C7, 0x01E4): return True
                    if robe is not None and robe != 0x0229 and (robe <= 0x04E7 or robe > 0x04EB): return True
            elif layer == L_TUNIC:
                if robe is not None: return robe != 0 and robe not in ROBES_OPEN
            elif layer == L_TORSO:
                if robe is not None and robe != 0 and robe not in ROBES_OPEN: return True
                tunic = gfx.get(L_TUNIC)
                if tunic is not None and tunic not in (0x1541, 0x1542):
                    if gfx.get(L_TORSO) in (0x782A, 0x782B): return True
            elif layer == L_ARMS: return robe is not None and robe != 0 and robe not in ROBES_OPEN
            elif layer in (L_HELMET, L_HAIR):
                if robe is not None:
                    if robe > 0x3173:
                        if robe in (0x4B9D, 0x7816): return True
                    elif robe <= 0x2687:
                        if robe < 0x2683: return 0x204E <= robe <= 0x204F
                        return True
                    elif robe in (0x2FB9, 0x3173): return True
            return False
        def layer_order(items):
            gfx = dict((k, v[1]) for k, v in items.items()); cloak = items.get(L_CLOAK); order = ORDER_NORMAL
            if cloak is not None:
                if gfx.get(L_ROBE) in (0xA2CA, 0xA2CB): order = ORDER_PARROT
                elif cloak[5]: order = ORDER_QUIVER
            order = list(order); torso = gfx.get(L_TORSO)
            if torso in (0x1C06, 0x1C02, 0x1C04):
                pi, ti = order.index(L_PANTS), order.index(L_TORSO)
                if pi < ti: order.pop(ti); order.insert(pi, L_TORSO)
            arms = gfx.get(L_ARMS)
            if arms in (0x13CD, 0x13DC, 0x13EE):
                ai, ti = order.index(L_ARMS), order.index(L_TORSO)
                if ai < ti: order.pop(ai); order.insert(ti, L_ARMS)
            if arms in (0x1410, 0x1417):
                order = [L_TORSO if l == L_ARMS else (L_ARMS if l == L_TORSO else l) for l in order]
            return order, gfx
        def keep_bounds(gid, b):
            cache, order = geo["bounds"], geo["order"]
            if gid not in cache: order.append(gid)
            cache[gid] = b
            while len(order) > BOUNDS_CAP: cache.pop(order.pop(0), None)
            return b
        def art_bounds(gid):
            b = "pic"
            try: got = Kit.on_client(lambda: Tex.gump_pixels(gid) if Tex.find() else None)
            except Exception: got = None
            if got is not None:
                b = None
                px, w, h = got; T = 0x01000000
                def solid(part): return bool(part) and (max(part) >= T or min(part) < 0)
                top = 0
                while top < h and not solid(px[top * w:(top + 1) * w]): top += 1
                if top < h:
                    bot = h - 1
                    while bot > top and not solid(px[bot * w:(bot + 1) * w]): bot -= 1
                    lo, hi = top * w, (bot + 1) * w; x0 = 0
                    while x0 < w - 1 and not solid(px[lo + x0:hi:w]): x0 += 1
                    x1 = w - 1
                    while x1 > x0 and not solid(px[lo + x1:hi:w]): x1 -= 1
                    b = (x0, top, x1 + 1, bot + 1)
            return keep_bounds(gid, b)
        def cached_bounds(gid):
            b = geo["bounds"].get(gid, "need")
            if b == "need":
                if gid not in geo["need"]: geo["need"].append(gid)
                b = "pic"
            if b != "pic": return b
            pw_, ph_ = Kit.pic_size(gid); return (0, 0, pw_, ph_) if pw_ > 0 and ph_ > 0 else None
        def _thread_wanted(): return bool(geo["need"])
        def draw_doll(items, who, praw=None):
            g = win["g"]; clear_doll()
            if g is None or who is None: return
            graphic, hue, female = who; pics = []; win["doll"] = pics; draw = []
            body, bhue, extra = body_gump(graphic, hue, female); draw.append((body, bhue, True, 0, 0))
            if extra: draw.append((extra, hue, True, 0, 0))
            order, gfx = layer_order(items)
            for layer in order:
                it = items.get(layer)
                if it is None: continue
                serial, igraphic, ihue, anim, partial, _c = it
                if covered(layer, gfx, praw): continue
                if anim == 0 and R.m_animid is None: continue
                gid = anim_gump(graphic, igraphic, anim, female)
                if gid <= 0 or Kit.pic_size(gid) == (0, 0): continue
                draw.append((gid, ihue & 0x3FFF, partial, 0 if layer in (L_HAIR, L_BEARD, L_FACE) else serial, layer))
            fx0 = fy0 = 1 << 20; fx1 = fy1 = -(1 << 20)
            for d in draw:
                b = cached_bounds(d[0])
                if b is not None: fx0, fy0 = min(fx0, b[0]), min(fy0, b[1]); fx1, fy1 = max(fx1, b[2]), max(fy1, b[3])
            if fx1 <= fx0 or fy1 <= fy0: fx0, fy0, fx1, fy1 = 0, 0, DOLL_W, DOLL_H
            fig = (fx1 - fx0, fy1 - fy0); k = st["k"]; mx, my, mw, mh = mid_rect()
            MX, MY = mx * k + DOLL_INSET, my * k + DOLL_INSET
            MW, MH = max(1.0, mw * k - 2 * DOLL_INSET), max(1.0, mh * k - 2 * DOLL_INSET)
            PW = max(1.0, (st["pw"] - 2 * PANEL_PAD) * k - 2 * DOLL_INSET); S = min(MH / fig[1], PW / fig[0])
            ox = int(round(MX + MW / 2.0 - S * (fx0 + fx1) / 2.0))
            oy = int(round(MY + MH / 2.0 - S * (fy0 + fy1) / 2.0))
            ux = int(round((MX + MW / 2.0) / k - (fx0 + fx1) / 2.0))
            uy = int(round((MY + MH / 2.0) / k - (fy0 + fy1) / 2.0)); scaled = abs(S - 1.0) > 0.001; raw_g = win["raw"]
            at = [-1]
            if R.ok and raw_g is not None:
                try:
                    Kit.flush(); anchor = Kit.client_control(win["c"].get("doll_drop"))
                    if anchor is not None: at[0] = raw_g.Children.IndexOf(anchor) + 1
                except Exception: at[0] = -1
            def place(rc):
                if at[0] <= 0: return False
                ch = raw_g.Children; rc.Parent = raw_g
                while ch.Remove(rc): pass
                ch.Insert(min(at[0], ch.Count), rc); at[0] += 1; return True
            def doll_piece(gid, phue, partial, serial):
                if R.DollPiece is None or raw_g is None or at[0] <= 0: return None
                try: rc = R.DollPiece(raw_g, UInt32(int(serial)), UInt16(int(gid)), UInt16(int(phue)), 0, 0, True)
                except Exception: R.DollPiece = None; return None
                try:
                    rc.va_gid, rc.va_k, rc.va_down = int(gid), float(S), False; rc.HighlightOnMouseOver = False
                    rc.IsPartialHue = bool(partial); set_pos(rc, ox, oy)
                    if scaled: rc.ApplyScale(S, False, True, False)
                    G.AddControlOnClick(rc, queue(("drop", 0)))
                    if not place(rc): raise Exception("no place")
                except Exception: safe(rc.Dispose); return None
                return rc
            def pic(gid, phue, partial, serial=0):
                if serial:
                    rc = doll_piece(gid, phue, partial, serial)
                    if rc is not None: pics.append(rc); return
                p = G.CreateGumpPic(gid, ux, uy, phue) if phue else G.CreateGumpPic(gid, ux, uy); p.SetPos(ux, uy)
                rc = None
                try:
                    Kit.flush(); rc = Kit.client_control(p); set_pos(rc, ox, oy)
                    if scaled: rc.ApplyScale(S, False, True, False)
                except Exception: rc = None; scale_ctrl(p)
                if partial: raw = Kit.client_control(p); Kit.set(raw if raw is not None else p, "IsPartialHue", True)
                if serial:
                    p.SetEntityTooltip(serial); G.AddControlOnClick(p, queue(("drop", 0)))
                    Kit.hook_double(p, queue(("use", serial)))
                else: p.SetAcceptMouseInput(False)
                placed = False
                if rc is not None:
                    try: placed = place(rc)
                    except Exception: placed = False
                if not placed: g.Add(p)
                pics.append(p)
            for gid, phue, partial, serial, _layer in draw: pic(gid, phue, partial, serial)
        def look_worn(force=False):
            if st["minimized"] or win["g"] is None: return
            if geo["redo"] and not geo["need"]: geo["redo"] = False; st["doll_sig"] = None
            now = time.time()
            if not force and st["sig"] is not None and st["doll_sig"] is not None \
                    and 0 <= now - st["doll_at"] < DOLL_EVERY:
                return
            st["doll_at"] = now; p = player_raw() if R.ok else None; got = {}; items, who = worn(p, got)
            sig = tuple([items[l][:3] if l in items else 0 for l in SLOT_LAYERS])
            if sig != st["sig"]: refresh(sig, p, got)
            dsig = (who, tuple(sorted((k, v[0], v[1], v[2]) for k, v in items.items())))
            if dsig != st["doll_sig"]: st["doll_sig"] = dsig; draw_doll(items, who, p)
        def show_item(s, item, api_item):
            g = win["g"]
            if s["ctrl"] is not None: Kit.dispose(s["ctrl"]); s["ctrl"] = None
            if item is None and api_item is None:
                Kit.set(s["label"], "IsVisible", True); Kit.with_tip(s["drop"], s["tip"]); return
            Kit.set(s["label"], "IsVisible", False); s["drop"].SetTooltip("")
            if R.ok and item is not None and win["raw"] is not None:
                try:
                    args = (win["raw"], UInt32(int(item.Serial)), UInt16(int(item.DisplayedGraphic)),
                            UInt16(int(item.Hue)), 0, 0)
                    ig = None
                    if R.SlotItem is not None:
                        try: ig = R.SlotItem(*args)
                        except Exception: R.SlotItem = None
                    if ig is None: ig = R.ItemGump(*args)
                    r = R.f_bounds.GetValue(ig); iw, ih = int(r.Width), int(r.Height)
                    f = min(1.0, (SLOT - 6) / float(max(1, iw)), (SLOT - 6) / float(max(1, ih))); k = st["k"]
                    set_pos(ig, int(round((s["x"] + (SLOT - iw * f) / 2.0) * k)),
                            int(round((s["y"] + (SLOT - ih * f) / 2.0) * k)))
                    if abs(k * f - 1.0) > 0.001:
                        try: ig.ApplyScale(k * f, False, True, False)
                        except Exception: scale_ctrl(ig, True)
                    try: G.AddControlOnClick(ig, queue(("drop", s["layer"])))
                    except Exception as e: safe(ig.Dispose); raise e
                    g.Add(ig); s["ctrl"] = ig; return
                except Exception as e: R.error = "item control: %s" % e
            serial = int(api_item.Serial) if api_item is not None else int(item.Serial)
            graphic = int(api_item.Graphic) if api_item is not None else int(item.DisplayedGraphic)
            hue = int((api_item if api_item is not None else item).Hue or 0) & 0x3FFF
            pic = G.CreateGumpItemPic(graphic, SLOT - 6, SLOT - 6)
            if hue: pic.Hue = hue
            pic.SetRect(s["x"] + 3, s["y"] + 3, SLOT - 6, SLOT - 6); scale_ctrl(pic)
            pic.SetEntityTooltip(serial); G.AddControlOnClick(pic, queue(("drop", s["layer"])))
            Kit.hook_double(pic, queue(("use", serial))); g.Add(pic); s["ctrl"] = pic
        def refresh(sig, p, got=None):
            slots = win["slots"]
            if len(slots) != len(sig): return
            old = st["sig"] or (None,) * len(slots)
            for i, s in enumerate(slots):
                if sig[i] == old[i]: continue
                s["serial"] = sig[i][0] if sig[i] else 0; item = api_item = None
                if sig[i]:
                    if R.ok and p is not None:
                        item = got.get(s["layer"]) if got else None
                        if item is None:
                            try: item = p.FindItemByLayer(layer_enum(s["layer"]))
                            except Exception: item = None
                    if item is None: api_item = find_layer(s["name"])
                show_item(s, item, api_item)
            st["sig"] = sig
        def on_drop(layer):
            if R.ok:
                h = held()
                if h is None: return
                serial, wearable, item_layer = h
                if not wearable: API.SysMsg(TITLE + ": that can't be worn.", Kit.HUE_BAD); return
                if item_layer not in LAYER_SET and item_layer > 0:
                    API.SysMsg(TITLE + ": that doesn't go in an equipment slot.", Kit.HUE_BAD); return
                try:
                    w = world(); p = w.Player
                    worn_it = p.FindItemByLayer(layer_enum(item_layer)) if item_layer else None
                    if worn_it is not None and int(worn_it.Serial) == serial: worn_it = None
                    if worn_it is None: R.m_equip.Invoke(None, Array[Object]([w, UInt32(int(p.Serial))]))
                    else:
                        R.m_swap.Invoke(None, Array[Object]([w, UInt32(int(p.Serial)), layer_enum(item_layer),
                                                             UInt32(int(worn_it.Serial))]))
                    st["sig"] = None
                except Exception as e: API.SysMsg(TITLE + ": couldn't equip that (%s)." % e, Kit.HUE_BAD)
                return
            serial = Kit.held_item()
            if serial: API.EquipItem(serial); st["sig"] = None
        STAT_KEYS = ("Strength", "Dexterity", "Intelligence", "Hits", "HitsMax", "Mana", "ManaMax",
                     "Stamina", "StaminaMax", "Weight", "WeightMax", "Gold", "Followers",
                     "FollowersMax", "PhysicalResistance")
        STATS_IN = 10
        def build_weight_bar(g, c, px, y):
            wslot = Kit.text_w("Weight 0000/0000"); rest_w = Kit.text_w("Gold 9,999,999   Followers 99/99")
            bx = px + 10 + wslot + 6; sw = st["strip_w"] or PANEL_W; room = sw - (bx - px) - 10 - rest_w - 14
            bw = max(WEIGHT_BAR_MIN, min(WEIGHT_BAR_W, room)); Kit.weight_bar(g, c, bx, y, bw, 16)
            c["stats4"] = Kit.add_label(g, "", bx + bw + 10, y, Kit.HUE_TEXT); c["room"] = sw - 2 * STATS_IN
            c["room3"] = wslot; c["room4"] = max(0, sw - (bx + bw + 10 - px) - STATS_IN)
        def build_stats_col(g, c, col):
            x, y, w, h = col; Kit.add_section(g, x, y, w, h)
            Kit.catcher(g, x, y, w, h, lambda *a: None, None, movable=not zoned_lock())
            pitch = max(COL_PITCH_MIN, min(COL_PITCH_MAX, (h - 16 - COL_BAR_H) // COL_ROWS))
            ty = y + max(8, (h - COL_ROWS * pitch - COL_BAR_H) // 2)
            c["scol"] = [Kit.add_label(g, "", x + STATS_IN, ty + i * pitch + (COL_BAR_H if i >= 7 else 0), Kit.HUE_TEXT)
                         for i in range(COL_ROWS)]
            c["room"] = w - 2 * STATS_IN; Kit.weight_bar(g, c, x + STATS_IN, ty + 7 * pitch - 1, w - 2 * STATS_IN, 16)
        def weight_update(wt, wmax, strength):
            if wmax <= 0 and strength > 0: wmax = int(WEIGHT_MAX_BASE + WEIGHT_MAX_PER_STR * strength)
            frac = (float(wt) / wmax) if wmax > 0 else -1.0
            if frac >= WEIGHT_RED:
                if st["w_armed"] and HOST.alert("character.weight", "Weight %d/%d (%d%%): nearly overloaded"
                                                % (wt, wmax, int(frac * 100)), level="warn", who="weight") is not False:
                    st["w_armed"] = False
            elif 0 <= frac < WEIGHT_REARM: st["w_armed"] = True
            fills = win["c"].get("wfills")
            if not fills or st["minimized"]: return
            lv = Kit.weight_level(frac, win["c"]["wbar_w"])
            if lv == st["wbar"]: return
            st["wbar"] = lv; Kit.weight_show(fills, lv[0], lv[1])
        def weight_tick():
            now = time.time()
            if 0 <= now - st["w_at"] < STATS_EVERY: return
            st["w_at"] = now
            try: p = API.Player
            except Exception: p = None
            if not p: return
            try: wt, wmax, strength = int(p.Weight), int(p.WeightMax), int(p.Strength)
            except Exception: return
            weight_update(wt, wmax, strength)
        def refresh_stats():
            c = win["c"]
            if st["minimized"] or ("stats1" not in c and "scol" not in c): return False
            now = time.time()
            if 0 <= now - st["stats_at"] < STATS_EVERY: return True
            st["stats_at"] = now; p = HOST.me()
            if not p: return True
            v = {}; vals = []
            for k in STAT_KEYS:
                try: x = int(getattr(p, k))
                except Exception: x = 0
                v[k] = x; vals.append(x)
            room = c["room"]; col = c.get("scol"); s1 = c.get("stats1"); old = st.get("stats_key")
            if old is None or old[0] != vals or old[1] is not col or old[2] is not s1 \
                    or old[3] != (room, c.get("room3"), c.get("room4")):
                st["stats_key"] = (vals, col, s1, (room, c.get("room3"), c.get("room4")))
                if col is not None:
                    for lbl, text in zip(col, ("Str %d" % v["Strength"], "Dex %d" % v["Dexterity"],
                            "Int %d" % v["Intelligence"], "HP %d/%d" % (v["Hits"], v["HitsMax"]),
                            "Mana %d/%d" % (v["Mana"], v["ManaMax"]), "Stamina %d/%d" % (v["Stamina"], v["StaminaMax"]),
                            "Weight %d/%d" % (v["Weight"], v["WeightMax"]), "Gold %s" % commas(v["Gold"]),
                            "Followers %d/%d" % (v["Followers"], v["FollowersMax"]),
                            "AR %d" % v["PhysicalResistance"])):
                        Kit.set_text(lbl, Kit.fit(text, room))
                else:
                    Kit.set_text(c["stats1"], Kit.fit("Str %d   Dex %d   Int %d   AR %d" % (
                        v["Strength"], v["Dexterity"], v["Intelligence"], v["PhysicalResistance"]), room))
                    Kit.set_text(c["stats2"], Kit.fit("HP %d/%d   Mana %d/%d   Stamina %d/%d" % (
                        v["Hits"], v["HitsMax"], v["Mana"], v["ManaMax"], v["Stamina"], v["StaminaMax"]), room))
                    Kit.set_text(c["stats3"], Kit.fit("Weight %d/%d" % (v["Weight"], v["WeightMax"]), c["room3"]))
                    Kit.set_text(c["stats4"], Kit.fit("Gold %s   Followers %d/%d" % (
                        commas(v["Gold"]), v["Followers"], v["FollowersMax"]), c["room4"]))
            weight_update(v["Weight"], v["WeightMax"], v["Strength"]); return True
        def bag_service(name): return HOST.services.get(name)
        def bag_cmd(cmd):
            if cmd == "show": queue("show")()
            elif cmd == "dock": queue("to_bar")()
        def attach_bags():
            attach, size = bag_service("bag.attach"), bag_service("bag.grid_size")
            hx, hy = hole_guess(); wh = safe(size)
            att = {"g": win["g"], "raw": None, "dx": hx, "dy": hy, "shown": not st["minimized"],
                   "state": dock_state(), "grid_wh": tuple(wh) if wh else None, "cmd": bag_cmd}
            st["attached"] = att
            try: attach(att)
            except Exception as e:
                st["attached"] = None; API.SysMsg(TITLE + ": couldn't combine with Bags (%s)." % e, Kit.HUE_BAD)
                return False
            return True
        def combine_tick():
            attach = bag_service("bag.attach"); size = bag_service("bag.grid_size"); att = st["attached"]
            want = settings["combine"] and attach is not None and size is not None
            if att is None:
                if want and attach_bags(): build_window()
                return
            if not want: detach(); return
            wh = safe(size); wh = tuple(wh) if wh else None
            if wh != att["grid_wh"]:
                att["grid_wh"] = wh
                if st["fit"] is None and not st["minimized"]:
                    if held() is not None: st["redraw_due"] = True
                    else: build_window()
        def detach():
            att, st["attached"] = st["attached"], None; tell_bags(None); st["told_shrink"] = None
            if att is not None:
                attach = bag_service("bag.attach")
                if attach is not None: safe(lambda: attach(None))
            if win["g"] is not None and not st["shutting"]: build_window()
        def sync_attached():
            att = st["attached"]
            if att is not None: att["shown"] = not st["minimized"]; att["state"] = dock_state()
        ACTIONS = {"drop": on_drop, "use": lambda serial: API.UseObject(serial),
                   "follow": lambda serial: Follow.toggle(serial, TITLE)}
        def page_table(w):
            return (("WINDOW", (("check", "stats", "Show your stats", "Str / Dex / Int, HP, mana, stamina, weight, "
                                 "gold, followers: under the doll, or beside it in a zone"),
                                ("check", "combine", "Combine with Bags in one window", "The Bags grid inside this "
                                 "window (unticked: two windows)"),
                                ("check", "beside", "Bags beside the doll (not under)", "Combined: the grid beside "
                                 "the doll; one too tall to stack goes beside anyway"),
                                ("check", "left", "Bags on the left", "Beside the doll: on its left (unticked: right)"),
                                ("note", "Drop an item on a slot to wear it; drag it out to take it off.",
                                 {"ndy": 4})), {"top": 32, "sh": 170}),)
        def on_change(old, new):
            if win["g"] is not None: queue("redraw")(); HOST.poke()
        cfg = Kit.Page(settings, page_table, save_settings, on_change); load_settings()
        def _start():
            load_settings()
            if not safe(lambda: API.Player): st["wait_player"] = True; return
            st["wait_player"] = False
            if not R.tried: R.tried = True; init_interop()
            st.update({"shutting": False, "docked": HOST.dock_soon(KEY), "queue": [], "sig": None, "doll_sig": None,
                       "attached": None, "beside_said": False, "fit": None, "k": 1.0, "py": None,
                       "strip_w": None, "pw": PANEL_W, "col": None, "ph": PANEL_H, "rp": COL_PITCH,
                       "told_bags": None, "pair": None, "pair_at": 0.0,
                       "room": None, "room_fs": None, "told_shrink": None, "grew": False, "paired": False,
                       "w_armed": True, "w_at": 0.0, "wbar": None, "wait_bags": None, "redraw_due": False,
                       "minimized": bool(st["saved_min"] or HOST.dock_wanted(KEY))})
            HOST.alert_kind("character.weight", "Weight near the limit", WEIGHT_ALERT_SOUND)
            if settings["combine"] and not bags_ready() and HOST.part_on("bags", "inventory"):
                st["wait_bags"] = time.time(); return
            open_doll()
        def bags_ready():
            size = bag_service("bag.grid_size")
            return bag_service("bag.attach") is not None and size is not None and bool(safe(size))
        def open_doll():
            st["wait_bags"] = None; attach, size = bag_service("bag.attach"), bag_service("bag.grid_size")
            if settings["combine"] and attach is not None and size is not None: attach_bags()
            slot = HOST.layout_slot(KEY)
            if slot is not None and slot[0] is not None and slot[1] is not None:
                st["fit"] = (int(slot[0]), int(slot[1])); st["pair"] = pair_rects(); st["pair_at"] = time.time()
            build_window(); look_worn(); refresh_stats()
            hooks = Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"))
            hooks.update({"fit": layout_fit, "exact": True, "pieces_out": True, "verify": not st["paired"]})
            geo["hooks"] = hooks; HOST.dock_add(KEY, hooks)
            if not R.ok:
                API.SysMsg(TITLE + ": no client access (%s); slots show pictures and equip without swapping."
                           % R.error, Kit.HUE_INFO)
        def _tick():
            if st["wait_player"]:
                if safe(lambda: API.Player): _start()
                return
            if st["wait_bags"] is not None:
                if bags_ready() or not 0 <= time.time() - st["wait_bags"] < BAGS_WAIT: open_doll()
                return
            if win["g"] is None: return
            if Kit.was_clicked(win["store"], "close"): save_place(); Kit.dispose(win["g"]); return
            while st["queue"]:
                action = st["queue"].pop(0); kind = action[0] if isinstance(action, tuple) else action
                if action == "show": st["minimized"], action = True, "toggle_min"
                if action == "redraw" and held() is not None: st["redraw_due"] = True
                elif Kit.win_action(action, st, KEY, TITLE, build_window, MIN_KEY): continue
                elif action in ("bag_mgr", "bag_traps"):
                    fn = bag_service("bag.open_manager" if action == "bag_mgr" else "bag.open_traps")
                    if fn is not None: fn()
                elif kind in ACTIONS: ACTIONS[kind](action[1])
            sync_attached(); combine_tick()
            if win["g"] is None: return
            drag = held() is not None
            if st.get("redraw_due") and not drag: st["redraw_due"] = False; build_window(); return
            if st["attached"] is not None and not drag:
                now = time.time()
                if now - st["pair_at"] >= PAIR_EVERY or now < st["pair_at"]:
                    st["pair_at"] = now; pr = pair_rects()
                    if pr != st["pair"]:
                        st["pair"] = pr
                        if st["fit"] is not None: build_window(); return
                    room = st["room"]
                    if room is not None and st["fit"] is not None and not st["minimized"]:
                        ci = cell_info(room[1])
                        sig = (room, None if ci is None else (round(ci[0], 1), round(ci[1], 1),
                                                              ci[2], ci[3], ci[4], ci[5]))
                        if sig != st.get("room_sig"):
                            st["room_sig"] = sig; fs = fit_scale(room[0], room[1])
                            if fs is not None and (fs[0] != st["told_shrink"] or (fs[1] > room[1]) != st["grew"]):
                                build_window(); return
            look_worn()
            if not refresh_stats(): weight_tick()
        def _thread_tick():
            need = geo["need"]
            if not need: return
            gid = need[0]
            try: art_bounds(gid)
            except Exception: keep_bounds(gid, "pic")
            need.pop(0); geo["redo"] = True
        def _stop():
            st["shutting"] = True; HOST.dock_remove(KEY); Kit.save_pos(POS_KEY, win["g"]); save_state(); save_settings()
            att, st["attached"] = st["attached"], None
            if att is not None:
                attach = bag_service("bag.attach")
                if attach is not None: safe(lambda: attach(None))
            clear_slots(); g, win["g"] = win["g"], None; win["raw"] = None; Kit.dispose(g)
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                  "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed,
                  "thread_tick": _thread_tick, "thread_wanted": _thread_wanted}
    def _part_storage():
        KEY = "storage"; TITLE = "Storage"; SETTINGS_KEY = "StorageIndex_settings"; POS_KEY = "StorageIndex_pos"
        MIN_KEY = "StorageIndex_min"; MAX_CONTAINERS = 300; MAX_ITEMS = 20000; STALE_DAYS = 60
        READ_DELAYS = (0.6, 2.0); REREAD_SECS = 15.0; OPEN_CHECK = 1.0; WATCH_MAX = 600.0; WATCH_CAP = 20
        CHANGE_DELAY = 0.5; CHANGE_CAP = 40; SEEN_CAP = 6000; ROOTS_CAP = 80
        READ_MAX = 1500; SAVE_DELAY = 5.0; MERGE_CHECK = 10.0; TOMB_DAYS = 30; SEARCH_WAIT = 0.4; LIVE_EVERY = 3.0
        ROWS = 14; MAX_RESULT_ROWS = ROWS * 30; MAX_FAVS = 12; NAME_MAX = 40
        PACK_BODIES = {0x0123: "Pack horse", 0x0124: "Pack llama", 0x0317: "Giant beetle"}
        SKIP_GRAPHICS = (0x2006, 0x1E5E); FILE_FMT = "_storage_index_%s.txt"; GROUND = 0xFFFFFFFF; SEEN_SAVE = 3600.0
        FILE_HEAD = "# Virtue Assistant Storage Index 1"
        FAVS_KEY = "StorageIndex_favs"; ACCOUNT_KEY = "StorageIndex_account"
        W = 420; MINI_W, MINI_H = 260, 46; ROW_H = 20; TRAY_ICON = 0x0E7C
        FOLLOW_TIP = "Alt+click: auto-follow (again to stop)"; M = Kit.MARGIN; IW = W - 2 * M; Y_FIND = M + 30 + Kit.GAP
        H_FIND = 64; Y_LIST = Y_FIND + H_FIND + Kit.GAP; H_LIST = 12 + ROWS * ROW_H + 8
        Y_STAT = Y_LIST + H_LIST + Kit.GAP; H_STAT = 30; H = Y_STAT + H_STAT + M
        STORAGE_AGO = ((60, 1, "just now"), (3600, 60, "%dm ago"), (86400, 3600, "%dh ago"),
                       (172800, 86400, "%d day ago"), (0, 86400, "%d days ago"))
        settings = {"bank": True, "ground": True, "pack": True, "days": STALE_DAYS}; favs = []
        DEFAULTS = dict(settings)
        st = {"shutting": True, "minimized": False, "docked": False, "queue": [], "active": False, "hooked": False}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}; page = {"wipe_at": 0.0}
        cleanup, queue, say = Kit.basics(st, TITLE)
        idx = {"recs": {}, "tombs": {}, "ver": 0, "dirty": False, "dirty_at": 0.0,
               "loaded": False, "path": None, "mtime": None, "err": "", "unread": False}
        summ = {"ver": -1, "keys": {}, "places": {}, "items": 0, "chars": 0, "veil": False}
        view = {"query": "", "seen_text": None, "changed_at": 0.0, "page": 0, "rows": [],
                "sel": None, "naming": None, "forget_arm": (None, 0.0), "status": "",
                "status_hue": Kit.HUE_INFO, "status_at": 0.0, "dirty": True, "built_for": None,
                "live": {}, "live_at": 0.0, "live_ver": 0, "live_sig": None, "data": [], "prev": [],
                "last_read": ("", 0.0, ""), "iw": IW}
        watching = {}; feed = {"q": [], "n": 0}; took = {"n": 0}; opens = []; tile_names = {}; quick = {}
        changed = set(); seen_in = {}
        seen_roots = []
        fcache = {"key": None, "stats": []}; scache = {"key": None, "by": {}}; NAME_JUNK = re.compile(r"%[^%]*%|%s")
        def clean_text(s): return str(s or "").replace("|", "/").replace("\r", " ").replace("\n", " ").strip()
        def fnv(text):
            h = 0x811C9DC5
            for ch in text: h = ((h ^ ord(ch)) * 0x01000193) & 0xFFFFFFFF
            return "%08x" % h
        def tile_name(it, graphic):
            n = tile_names.get(graphic)
            if n is None:
                try: d = it.GetItemData(); n = NAME_JUNK.sub("", str(d.Name or "")).strip() if d is not None else ""
                except Exception: n = ""
                if len(tile_names) > 3000: tile_names.clear()
                tile_names[graphic] = n
            return n
        def item_name(it, graphic, amount):
            try: n = str(it.Name or "")
            except Exception: n = ""
            if "%" in n: n = NAME_JUNK.sub("", n)
            n = n.strip()
            if amount > 1:
                a = str(amount)
                if n.startswith(a + " "): n = n[len(a) + 1:].strip()
            if not n: n = tile_name(it, graphic) or ("item 0x%04X" % graphic)
            n = clean_text(n); return n[:1].upper() + n[1:]
        def parse_terms(text):
            out = []
            for t in str(text or "").split(","):
                t = t.strip().lower()
                if not t: continue
                g = None
                try:
                    if t.startswith("0x") and len(t) > 2: g = int(t, 16)
                    elif t.isdigit() and len(t) >= 3: g = int(t)
                except ValueError: g = None
                out.append(("g", g) if g is not None else ("n", t))
            return out
        def matches(terms, key):
            g, ln = key[0], key[2]
            for kind, v in terms:
                if kind == "g":
                    if g == v: return True
                elif v in ln: return True
            return False
        DAYS = {"days": (1, 3650)}
        def load_settings(): Kit.kv_load(SETTINGS_KEY, ";", settings, DAYS)
        def save_settings(): Kit.kv_save(SETTINGS_KEY, ";", settings, ("bank", "ground", "pack", "days"), DAYS)
        def load_favs():
            raw = Kit.get_var(FAVS_KEY, ""); del favs[:]
            if not raw:
                favs.extend([[name, "0x%04X" % gfx] for name, gfx in sorted(Kit.REAGENTS.values())]
                            + [["Bandages", "0x0E21"]])
                return
            if raw == "-": return
            for part in raw.split(";"):
                if "=" not in part: continue
                label, term = part.split("=", 1); label, term = label.strip(), term.strip()
                if term and len(favs) < MAX_FAVS: favs.append([label or term, term])
        def save_favs():
            if not favs: Kit.put_var(FAVS_KEY, "-"); return
            Kit.put_var(FAVS_KEY, ";".join("%s=%s" % (l.replace(";", ",").replace("=", "-"),
                                                      t.replace(";", ",")) for l, t in favs))
        def account_id():
            with Kit.quiet:
                Typing._find(); prof = Typing.prof
                cur = Typing._get(None, "CurrentProfile", prof) if prof is not None else None
                user = Typing._get(cur, "Username") if cur is not None else None
                if user: server = Typing._get(cur, "ServerName") or ""; return fnv(("%s|%s" % (server, user)).lower())
            try:
                scope = API.PersistentVar.Account; v = str(API.GetPersistentVar(ACCOUNT_KEY, "", scope) or "")
                if not v:
                    import random; v = "a%07x" % random.randint(0, 0xFFFFFFF)
                    API.SavePersistentVar(ACCOUNT_KEY, v, scope)
                return "".join(ch for ch in v if ch.isalnum())[:16] or "account"
            except Exception: return "account"
        def new_rec(serial):
            return {"s": serial, "parent": 0, "root": serial, "kind": "bag", "cs": 0, "cname": "",
                    "label": "", "custom": "", "facet": 0, "x": 0, "y": 0, "seen": 0.0, "mob": 0,
                    "plabel": "", "stub": False, "items": {}, "nat": 0.0}
        def when(text):
            t = float(text)
            if not 0 <= t < 4e9: raise ValueError(text)
            return t
        def parse_file(text):
            recs, tombs = {}, {}
            for line in text.split("\n"):
                line = line.rstrip("\r")
                if not line or line.startswith("#"): continue
                p = line.split("|")
                try:
                    if p[0] == "C" and len(p) >= 15:
                        s = int(p[1]); r = new_rec(s)
                        r.update({"parent": int(p[2]), "root": int(p[3]), "kind": p[4],
                                  "cs": int(p[5]), "cname": p[6], "label": p[7], "custom": p[8],
                                  "facet": int(p[9]), "x": int(p[10]), "y": int(p[11]),
                                  "seen": when(p[12]), "mob": int(p[13]), "plabel": p[14],
                                  "stub": len(p) > 15 and p[15] == "1", "nat": when(p[16]) if len(p) > 16 else 0.0})
                        if all(0 <= r[k] <= 0xFFFFFFFF for k in ("s", "parent", "root", "cs", "facet", "x", "y",
                                                                 "mob")): recs[s] = r
                    elif p[0] == "I" and len(p) >= 6:
                        r = recs.get(int(p[1])); a = int(p[4])
                        if r is not None and a > 0:
                            name = p[5]; key = (int(p[2]), int(p[3]), name.lower()); e = r["items"].get(key)
                            if e is None: r["items"][key] = [name, a]
                            else: e[1] += a
                    elif p[0] == "D" and len(p) >= 3: tombs[int(p[1])] = when(p[2])
                except (ValueError, IndexError): continue
            return recs, tombs
        def file_text():
            out = [FILE_HEAD]
            for s, r in idx["recs"].items():
                out.append("C|%d|%d|%d|%s|%d|%s|%s|%s|%d|%d|%d|%d|%d|%s|%d|%d" % (
                    s, r["parent"], r["root"], r["kind"], r["cs"], clean_text(r["cname"]),
                    clean_text(r["label"]), clean_text(r["custom"]), r["facet"], r["x"], r["y"],
                    int(r["seen"]), r["mob"], clean_text(r["plabel"]), 1 if r["stub"] else 0, int(r.get("nat", 0))))
                for key, e in r["items"].items():
                    out.append("I|%d|%d|%d|%d|%s" % (s, key[0], key[1], e[1], clean_text(e[0])))
            for s, t in idx["tombs"].items(): out.append("D|%d|%d" % (s, int(t)))
            return "\n".join(out) + "\n"
        def read_file(path): return Kit.read_merge(path)
        def write_file(path, text):
            try: return Kit.write_safe(path, text)
            except Exception as ex: idx["err"] = str(ex)[:60]; return False
        def mtime(path): return safe(lambda: os.path.getmtime(path))
        def newer_name(a, b):
            at, bt = a.get("nat", 0.0), b.get("nat", 0.0)
            return at > bt or bool(a["custom"] and not b["custom"] and not bt)
        def merge(recs, tombs):
            changed = False; mine = idx["recs"]; cut = time.time() - settings["days"] * 86400.0
            for s, t in tombs.items():
                if t > idx["tombs"].get(s, 0.0): idx["tombs"][s] = t
            for s, r in recs.items():
                if r["seen"] < cut: continue
                cur = mine.get(s)
                if cur is None or r["seen"] > cur["seen"]:
                    if cur is not None and newer_name(cur, r):
                        r["custom"], r["nat"] = cur["custom"], cur.get("nat", 0.0)
                    mine[s] = r; quick.pop(s, None); changed = True
                elif newer_name(r, cur): cur["custom"], cur["nat"] = r["custom"], r.get("nat", 0.0); changed = True
            for s in [s for s in mine if s in idx["tombs"] and mine[s]["seen"] <= idx["tombs"][s]]:
                del mine[s]; changed = True
            return changed
        def prune():
            now = time.time(); recs = idx["recs"]; cut = now - settings["days"] * 86400.0
            tcut = now - TOMB_DAYS * 86400.0
            for s in [s for s, t in idx["tombs"].items() if t < tcut]: del idx["tombs"][s]
            if len(idx["tombs"]) > 4 * MAX_CONTAINERS:
                for s, _ in sorted(idx["tombs"].items(), key=lambda kv: kv[1])[:len(idx["tombs"]) - 4 * MAX_CONTAINERS]:
                    del idx["tombs"][s]
            groups = {}
            for s, r in recs.items():
                g = groups.get(r["root"])
                if g is None: g = groups[r["root"]] = [0.0, [], 0]
                g[0] = max(g[0], r["seen"]); g[1].append(s); g[2] += len(r["items"])
            dropped = False
            for root in [k for k, g in groups.items() if g[0] < cut]:
                for s in groups.pop(root)[1]: recs.pop(s, None)
                dropped = True
            n_recs = len(recs); n_items = sum(g[2] for g in groups.values())
            if n_recs > MAX_CONTAINERS or n_items > MAX_ITEMS:
                for root, g in sorted(groups.items(), key=lambda kv: kv[1][0]):
                    if n_recs <= MAX_CONTAINERS and n_items <= MAX_ITEMS: break
                    for s in g[1]: recs.pop(s, None)
                    n_recs -= len(g[1]); n_items -= g[2]; dropped = True
            return dropped
        def load_index():
            path = idx["path"]
            if not path: return
            text = read_file(path); idx["mtime"] = mtime(path); idx["unread"] = text is None
            if text: merge(*parse_file(text))
            prune(); idx["loaded"] = True; idx["ver"] += 1
        def save_index():
            path = idx["path"]
            if not path: return
            mt = mtime(path)
            if idx["unread"] or (mt is not None and mt != idx["mtime"]):
                text = read_file(path)
                if text is None: idx["err"] = "couldn't read the index file"; idx["dirty_at"] = time.time(); return
                idx["unread"] = False; idx["mtime"] = mt
                if text and merge(*parse_file(text)): idx["ver"] += 1
            if prune(): idx["ver"] += 1
            if write_file(path, file_text()): idx["mtime"] = mtime(path); idx["dirty"] = False; idx["err"] = ""
            else: idx["dirty_at"] = time.time()
        def check_others():
            path = idx["path"]; mt = mtime(path)
            if mt is None or mt == idx["mtime"]: return
            text = read_file(path)
            if text is None: return
            idx["mtime"] = mt; idx["unread"] = False
            if text and merge(*parse_file(text)) | prune(): idx["ver"] += 1
        def mark_dirty():
            idx["ver"] += 1
            if not idx["dirty"]: idx["dirty"] = True; idx["dirty_at"] = time.time()
        def post(res): feed["n"] += 1; res["n"] = feed["n"]; feed["q"] = feed["q"] + [res]
        def unread():
            n = took["n"]; return [r for r in feed["q"] if r["n"] > n]
        def has_unread():
            q = feed["q"]; return bool(q) and q[-1]["n"] > took["n"]
        def take_reads():
            for res in unread(): took["n"] = res["n"]; integrate(res)
        def place_of(it):
            cur, depth = it, 0
            while depth < 12:
                c = int(cur.Container or 0)
                if c < 0x40000000 or c == GROUND: break
                nxt = API.FindItem(c)
                if nxt is None: return None
                cur, depth = nxt, depth + 1
            else: return None
            owner = int(cur.Container or 0); owner = 0 if owner == GROUND else owner; top = int(cur.Serial)
            if int(cur.Graphic) in SKIP_GRAPHICS or int(it.Graphic) in SKIP_GRAPHICS: return None
            if owner == 0:
                if cur.IsCorpse: return None
                return ("chest", cur, None) if settings["ground"] else None
            me = API.Player
            if me is None: return None
            if owner == int(me.Serial):
                bank = int(API.Bank or 0)
                return ("bank", cur, None) if bank and top == bank and settings["bank"] else None
            m = API.FindMobile(owner)
            return ("pack", cur, m) if m is not None and bool(m.IsRenamable) and settings["pack"] else None
        def read_container(serial, final):
            it = API.FindItem(serial)
            if it is None: return None
            place = place_of(it)
            if place is None: return None
            kind, top, mob = place; me = API.Player
            if me is None: return None
            items = API.ItemsInContainer(serial, True) or []; q, n = 0, 0; first = []
            for x in items:
                n += 1
                if n > READ_MAX: break
                try:
                    xs, am, xc = int(x.Serial), x.Amount, int(x.Container)
                    q = (q * 31 + xs + 7 * int(am or 0) + 13 * xc) & 0xFFFFFFFFFFFF
                except Exception: first.append(None); continue
                first.append((xs, am, xc))
            sig = (q, n); keep_seen(serial, first)
            if quick.get(serial) == sig and serial in idx["recs"]:
                if len(feed["q"]) < 40: post({"serial": serial, "same": True, "at": time.time()})
                return True
            cs, cname = int(me.Serial), str(me.Name or ""); facet = int(API.GetMap() or 0)
            by = {serial: []}; parents, names = {}, {}; n = 0; capped = False
            for x in items:
                n += 1
                if n > READ_MAX: capped = True; break
                try:
                    f = first[n - 1]
                    if f is not None: xs, am, c = f; a = max(1, int(am or 1))
                    else: xs = int(x.Serial); c = int(x.Container); a = None
                    g = int(x.Graphic); h = int(x.Hue)
                    if a is None: a = max(1, int(x.Amount or 1))
                    name = item_name(x, g, a)
                    if bool(x.IsContainer): parents[xs] = c; names[xs] = name
                except Exception: continue
                lst = by.get(c)
                if lst is None: lst = by[c] = []
                lst.append((g, h, a, name))
            if not by[serial] and not final and len(by) == 1: return False
            top_serial = int(top.Serial); top_name = item_name(top, int(top.Graphic), 1)
            if kind == "bank": label = ("Bank box (%s)" % cname) if cname else "Bank box"
            elif kind == "chest": label = "%s at %d, %d" % (top_name or "Chest", int(top.X), int(top.Y))
            else:
                body = int(mob.Graphic or 0)
                label = ("%s %s" % (PACK_BODIES.get(body, "Pack animal"), str(mob.Name or ""))).strip()
            res = {"serial": serial, "parent": int(it.Container or 0), "kind": kind,
                   "root": top_serial, "label": label, "top_name": top_name,
                   "own_name": item_name(it, int(it.Graphic), 1), "cs": cs, "cname": cname,
                   "facet": facet, "x": int(top.X), "y": int(top.Y),
                   "mob": int(mob.Serial) if mob is not None else 0, "by": by,
                   "parents": parents, "names": names, "capped": capped, "at": time.time()}
            if len(feed["q"]) < 40:
                post(res)
                if len(quick) > 200: quick.clear()
                quick[serial] = sig
            return True
        def under(recs, s, anc):
            depth = 0
            while s and depth < 14:
                if s == anc: return True
                r = recs.get(s)
                if r is None: return False
                s, depth = r["parent"], depth + 1
            return False
        def integrate(res):
            recs = idx["recs"]; op = res.get("op")
            if op == "forget": forget_place(res["root"]); return
            if op == "name":
                r = recs.get(res["root"])
                if r is not None: r["custom"] = res["text"]; r["nat"] = time.time(); mark_dirty()
                return
            if op == "wipe":
                now = time.time()
                for s in list(recs): idx["tombs"][s] = now
                recs.clear(); mark_dirty(); return
            if res.get("same"):
                serial, now, root, stale = res["serial"], res["at"], None, False
                for s, r in recs.items():
                    if not under(recs, s, serial): continue
                    stale = stale or now - r["seen"] > SEEN_SAVE; r["seen"] = now; root = r["root"]
                if stale and not idx["dirty"]: idx["dirty"] = True; idx["dirty_at"] = time.time()
                p = summ["places"].get(root) if root is not None else None
                if p is not None: p["seen"] = now; view["dirty"] = True
                return
            serial, root, now = res["serial"], res["root"], res["at"]
            if serial == root: old = [s for s, r in recs.items() if r["root"] == root or s == root]
            else: old = [s for s in recs if under(recs, s, serial)]
            place = {"kind": res["kind"], "root": root, "cs": res["cs"], "cname": res["cname"],
                     "facet": res["facet"], "x": res["x"], "y": res["y"], "mob": res["mob"], "plabel": res["label"]}
            parents = res["parents"]; keep = set()
            for s in old:
                if s not in res["by"] and s != root and (s in parents or res["capped"]): keep.add(s)
            more = True
            while more:
                more = False
                for s in old:
                    if s not in keep and s not in res["by"] and s != root and recs[s]["parent"] in keep:
                        keep.add(s); more = True
            customs = {}; gone = []
            for s in old:
                r = recs[s]
                if s in keep:
                    r.update(place); r["kind"] = "bag"
                    if s in parents: r["parent"] = parents[s]
                    continue
                if s in res["by"] and (r["custom"] or r.get("nat")): customs[s] = (r["custom"], r.get("nat", 0.0))
                elif s not in res["by"]: gone.append(s)
                del recs[s]
            for s in gone: idx["tombs"][s] = now
            if serial != root:
                rr = recs.get(root)
                if rr is None: rr = recs[root] = new_rec(root); rr["stub"] = True
                rr.update(place); rr["parent"] = 0; rr["label"] = res["label"]
                if rr["stub"]: rr["seen"] = max(rr["seen"], now)
            for cont, lst in res["by"].items():
                r = new_rec(cont); r.update(place); r["seen"] = now
                r["custom"], r["nat"] = customs.get(cont, ("", 0.0))
                if cont == root: r["parent"], r["label"] = 0, res["label"]
                elif cont == serial: r["kind"], r["parent"], r["label"] = "bag", res["parent"], res["own_name"]
                else:
                    r["kind"], r["parent"] = "bag", res["parents"].get(cont, 0)
                    r["label"] = res["names"].get(cont, "Bag")
                items = r["items"]
                for g, h, a, name in lst:
                    k = (g, h, name.lower()); e = items.get(k)
                    if e is None: items[k] = [name, a]
                    else: e[1] += a
                recs[cont] = r; idx["tombs"].pop(cont, None)
            idx["tombs"].pop(root, None); prune(); mark_dirty(); view["last_read"] = (res["label"], now, res["kind"])
        def on_open(*args):
            if not st["active"]: return
            for a in reversed(args):
                s = None
                try: s = int(a)
                except Exception:
                    try: s = int(a.Serial)
                    except Exception: s = None
                if s and s >= 0x40000000:
                    if len(opens) < 40: opens.append(s)
                    return
        def keep_seen(root, first):
            if len(seen_in) > SEEN_CAP or len(seen_roots) > ROOTS_CAP:
                drop = set(k for k in seen_roots if k not in watching) or set(seen_roots[:max(1, len(seen_roots) // 2)])
                for k in [k for k, v in seen_in.items() if v in drop]: del seen_in[k]
                seen_roots[:] = [k for k in seen_roots if k not in drop]
            if root in seen_roots: seen_roots.remove(root)
            seen_roots.append(root)
            for f in first:
                if f is not None: seen_in[f[0]] = root
        def on_item_change(*args):
            if not st["active"] or not watching or len(changed) >= CHANGE_CAP: return
            for a in args:
                try: s, c = int(a.Serial), int(a.Container)
                except Exception: continue
                for k in (c, s):
                    root = k if k in watching else seen_in.get(k)
                    if root is not None: changed.add(root)
                return
        def hook_events():
            Kit.hook_once(st, "hooked", ("OnOpenContainer", on_open), ("OnItemCreated", on_item_change),
                          ("OnItemUpdated", on_item_change))
        def note_open(serial):
            now = time.time(); w = watching.get(serial)
            if w is None and len(watching) >= WATCH_CAP:
                oldest = min(watching, key=lambda k: watching[k][0]); watching.pop(oldest, None)
            watching[serial] = [now, now + READ_DELAYS[0], 0]
        def watch_tick(now):
            if not watching:
                if changed: changed.clear()
                return
            if changed:
                todo = list(changed); changed.difference_update(todo); soon = now + CHANGE_DELAY
                for s in todo:
                    w = watching.get(s)
                    if w is not None and w[2] >= len(READ_DELAYS) and w[1] > soon: w[1] = soon
            check = now >= st.get("check_at", 0.0) or st.get("check_at", 0.0) - now > OPEN_CHECK
            if check: st["check_at"] = now + OPEN_CHECK
            for serial in list(watching):
                w = watching[serial]; closed = False
                if check and w[2] >= len(READ_DELAYS):
                    it = API.FindItem(serial); closed = it is None or not bool(it.Opened)
                    if it is None: watching.pop(serial, None); continue
                if closed or now - w[0] > WATCH_MAX: read_container(serial, True); watching.pop(serial, None); continue
                if now < w[1] and w[1] - now <= REREAD_SECS + 1.0: continue
                done = read_container(serial, w[2] >= len(READ_DELAYS) - 1)
                if done is None: watching.pop(serial, None); continue
                w[2] += 1; w[1] = w[0] + READ_DELAYS[w[2]] if w[2] < len(READ_DELAYS) else now + REREAD_SECS
        def build_summary():
            keys, places = {}, {}; recs = idx["recs"]; chars = set(); n = 0
            for s, r in recs.items():
                root = r["root"]; p = places.get(root)
                if p is None:
                    rr = recs.get(root); src = rr if rr is not None else r
                    label = src["custom"] or src["label"] or r["plabel"] or "A container"
                    p = places[root] = {"label": label, "seen": 0.0, "kind": src["kind"],
                                        "mob": src["mob"], "cname": src["cname"], "raw": label,
                                        "cs": src["cs"], "custom": bool(src["custom"]),
                                        "facet": src["facet"], "x": src["x"], "y": src["y"]}
                if r["seen"] > p["seen"]: p["seen"] = r["seen"]
                if r["cname"]: chars.add(r["cname"])
                for key, e in r["items"].items():
                    n += 1; k = keys.get(key)
                    if k is None: k = keys[key] = [e[0], {}]
                    k[1][root] = k[1].get(root, 0) + e[1]
            summ.update({"ver": idx["ver"], "keys": keys, "places": places, "items": n, "chars": len(chars)})
            veil_places(places, sorted(set(r["cs"] for r in recs.values() if r["cname"]))); view["dirty"] = True
        def chest_label(label): return re.sub(r" at \d+, \d+$", " at " + Kit.veil("xy", ""), label)
        def veil_places(places, css):
            summ["veil"] = Kit.streamer
            if not Kit.streamer: return
            me = HOST.me(); mine = int(me.Serial) if me is not None else 0; others = [cs for cs in css if cs != mine]
            for p in places.values():
                cs, cname = p["cs"], p["cname"]
                if cname: p["cname"] = Kit.veil("me", cname) if cs == mine else "Character %d" % (
                    others.index(cs) + 2 if cs in others else len(others) + 2)
                if p["custom"]: continue
                if p["kind"] == "bank": p["label"] = ("Bank box (%s)" % p["cname"]) if cname else "Bank box"
                elif p["kind"] == "chest": p["label"] = chest_label(p["label"])
        def fav_stored():
            key = (summ["ver"], tuple(t for _, t in favs))
            if fcache["key"] != key:
                stats = []; keys = summ["keys"]
                for label, term in favs:
                    terms = parse_terms(term); total, per = 0, {}
                    for k, e in keys.items():
                        if matches(terms, k):
                            for root, a in e[1].items(): per[root] = per.get(root, 0) + a; total += a
                    stats.append((total, per))
                fcache["key"], fcache["stats"] = key, stats
            return fcache["stats"]
        def search_stored(q):
            key = (summ["ver"], q.lower())
            if scache["key"] != key:
                terms = parse_terms(q); by = {}
                for k, e in summ["keys"].items():
                    if matches(terms, k):
                        for root, a in e[1].items():
                            d = by.get(root)
                            if d is None: d = by[root] = {}
                            d[k] = (e[0], a)
                scache["key"], scache["by"] = key, by
            return scache["by"]
        def row_click(i):
            def handler(*args): alt = Follow.alt_held(); queue.add(("row", i, alt, time.time()), dup=True, cap=20)
            return handler
        def build_window():
            told = wnd.slot if HOST.layout_holds(KEY) else None; w, h = told or (W, H)
            n = wnd.rows(ROW_H, H - ROWS * ROW_H, ROWS, 4)
            iw, h_list = w - 2 * M, h - (H - H_LIST); y_stat = Y_LIST + h_list + Kit.GAP; view["iw"] = iw
            g, store, c = wnd.begin(MINI_W if st["minimized"] else w, MINI_H if st["minimized"] else h); rows = []
            if not st["minimized"]:
                wnd.frame(g); Kit.add_section(g, M, Y_FIND, iw, H_FIND); fav_w = 35 + Kit.text_w("Add favourite")
                Kit.add_label(g, "Find:", M + 10, Y_FIND + 12, Kit.HUE_TEXT); bx = M + 16 + Kit.text_w("Find:")
                bw = iw - (bx - M) - fav_w - 22
                c["box"] = Kit.with_tip(Kit.add_textbox(g, view["query"], bx, Y_FIND + 9, bw, numbers=False),
                                        "Part of a name, or a graphic (0x0F88); commas for several; empty: favourites")
                Kit.art_button(g, store, "fav", Kit.ART_OK, M + iw - fav_w - 6, Y_FIND + 8,
                               "Add favourite", "Add the Find box text to your favourites", on_click=queue("fav"))
                yb = Y_FIND + 36; xb = M + 10
                Kit.art_button(g, store, "name", Kit.ART_OK, xb, yb, "Name", "Name the picked place: type it in "
                               "the Find box, then click Name again", on_click=queue("name"))
                xb += 35 + Kit.text_w("Name") + 12
                Kit.art_button(g, store, "forget", Kit.ART_CLOSE, xb, yb, "Forget",
                               "Drop the picked place and its bags from the index (click twice)",
                               on_click=queue("forget"))
                nx_w = 35 + Kit.text_w("Next"); xn = M + iw - nx_w - 6
                Kit.art_button(g, store, "next", Kit.ART_PAGE, xn, yb, "Next", "Next page", on_click=queue("next"))
                xp = xn - 12 - (35 + Kit.text_w("Prev"))
                Kit.art_button(g, store, "prev", Kit.ART_PAGE, xp, yb, "Prev", "Previous page", on_click=queue("prev"))
                c["page"] = Kit.add_label(g, "", xp - 50, yb + 3, Kit.HUE_INFO)
                Kit.add_section(g, M, Y_LIST, iw, h_list)
                for i in range(n):
                    ry = Y_LIST + 8 + i * ROW_H
                    r = {"l": Kit.add_label(g, "", M + 10, ry, Kit.HUE_TEXT),
                         "r": Kit.add_label(g, "", M + iw - 60, ry, Kit.HUE_INFO),
                         "lx": M + 10, "rx": M + iw - 60, "tip": "", "y": ry}
                    r["c"] = Kit.catcher(g, M + 4, ry - 2, iw - 8, ROW_H, row_click(i)); rows.append(r)
                Kit.add_section(g, M, y_stat, iw, H_STAT)
                c["status"] = Kit.add_label(g, "", M + 10, y_stat + 7, Kit.HUE_INFO)
            view.update({"data": [None] * len(rows), "prev": [(None, 0.0)] * len(rows), "seen_text": None,
                         "built_for": None, "dirty": True})
            wnd.end(g, {"rows": rows}); refresh(time.time())
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, (240, 160), icon=TRAY_ICON,
                         cleanup=cleanup, clear={"rows": []})
        def full_shown(): return win["g"] is not None and not st["minimized"] and not st["docked"]
        def set_status(text, hue=None):
            view["status"] = text; view["status_hue"] = Kit.HUE_INFO if hue is None else hue
            view["status_at"] = time.time()
        def idle_status():
            n = len(summ["places"])
            if not idx["loaded"]: return "Reading the index"
            if idx["err"]: return "Index file: %s" % idx["err"]
            label, t, kind = view["last_read"]; s = "%s noted" % Kit.count(n, "place")
            if Kit.streamer and kind == "bank": label = "Bank box (%s)" % Kit.veil("me", "")
            elif Kit.streamer and kind == "chest": label = chest_label(label)
            if summ["chars"] > 1: s += " on %d characters" % summ["chars"]
            if label: s += "; last read %s" % label
            return s
        def place_tip(p, root):
            where = ""
            if p["kind"] == "chest" and not Kit.streamer: where = " (facet %d, %d, %d)" % (p["facet"], p["x"], p["y"])
            who = (" by %s" % p["cname"]) if p["cname"] else ""
            tip = "%s\nSeen%s %s%s\nClick to pick it (then Name or Forget)" % (
                p["label"], who, Kit.ago(time.time() - p["seen"], STORAGE_AGO), where)
            if p["mob"]: tip += "\n" + FOLLOW_TIP
            return tip
        def results(now):
            rows = []; live = view["live"]; places = summ["places"]; q = view["query"]
            if not q:
                if not favs:
                    return [("No favourites yet: type a name, then click Add favourite.",
                             "", Kit.HUE_INFO, 0, "", None)]
                rows.append(("FAVOURITES  (click one to see where)", "", Kit.HUE_TITLE, 0,
                             "Totals across the account: every place noted, and your backpack now", None))
                stats = fav_stored()
                for i, (label, term) in enumerate(favs):
                    terms = parse_terms(term); total, per = stats[i] if i < len(stats) else (0, {})
                    mine = sum(e[1] for key, e in live.items() if matches(terms, key)); total += mine
                    n = len(per) + (1 if mine else 0); lines = []
                    if mine: lines.append("On you now: %s" % commas(mine))
                    for root, a in sorted(per.items(), key=lambda kv: -kv[1])[:10]:
                        p = places.get(root); lines.append("%s: %s" % (p["label"] if p else "?", commas(a)))
                    tip = "%s (%s)\n%s\nClick to see where" % (label, term, "\n".join(lines) if lines else "None noted")
                    rows.append((label, ("%s in %s" % (commas(total), Kit.count(n, "place")))
                                 if total else "none", Kit.HUE_TEXT, 0, tip, ("fav", term)))
                return rows
            terms = parse_terms(q); by_place = search_stored(q)
            mine = dict((key, (e[0], e[1])) for key, e in live.items() if matches(terms, key))
            n = len(by_place) + (1 if mine else 0)
            if not n:
                return [("Nothing noted holds \"%s\"." % q, "", Kit.HUE_INFO, 0,
                         "Open the container it is in once (bank box, chest, pack animal) and it is noted", None)]
            sums, names = {}, {}
            for root, d in by_place.items():
                t = 0
                for k, v in d.items(): t += v[1]; names[k] = v[0]
                sums[root] = t
            total = sum(sums.values()) + sum(a for _, a in mine.values())
            for k, v in mine.items(): names[k] = v[0]
            name = list(names.values())[0] if len(names) == 1 else "%d kinds" % len(names)
            rows.append((name, "%s in %s" % (commas(total), Kit.count(n, "place")),
                         Kit.HUE_TITLE, 0, "Everything noted that matches \"%s\"" % q, None))
            left = 0
            if mine:
                me_name = Kit.veil("me", str(safe(lambda: API.Player.Name, "") or ""))
                rows.append(("Backpack%s" % ((" (%s)" % me_name) if me_name else ""), "on you now",
                             Kit.HUE_TITLE, 0, "Your backpack and the bags in it, right now", None))
                lst = sorted(mine.items(), key=lambda kv: -kv[1][1]); room = max(0, MAX_RESULT_ROWS - len(rows))
                left += max(0, len(lst) - room)
                for key, (nm, a) in lst[:room]:
                    rows.append((nm, commas(a), Kit.HUE_TEXT, 14, "%s x%s on you (graphic 0x%04X, hue %d)"
                                 % (nm, commas(a), key[0], key[1]), None))
            order = sorted(by_place.items(), key=lambda kv: -sums[kv[0]])
            for root, d in order:
                p = places.get(root)
                if p is None: continue
                if len(rows) >= MAX_RESULT_ROWS: left += 1 + len(d); continue
                hue = Kit.HUE_GOOD if view["sel"] == root else Kit.HUE_TITLE
                rows.append((p["label"], "seen %s" % Kit.ago(now - p["seen"], STORAGE_AGO), hue, 0,
                             place_tip(p, root), ("place", root, p["mob"], True)))
                data = ("place", root, p["mob"], False); lst = sorted(d.items(), key=lambda kv: -kv[1][1])
                room = max(0, MAX_RESULT_ROWS - len(rows)); left += max(0, len(lst) - room)
                for key, (nm, a) in lst[:room]:
                    tip = "%s x%s in %s (graphic 0x%04X, hue %d)\nClick to pick this place" % (
                        nm, commas(a), p["label"], key[0], key[1])
                    if p["mob"]: tip += "\n" + FOLLOW_TIP
                    rows.append((nm, commas(a), Kit.HUE_TEXT, 14, tip, data))
            if left:
                rows.append(("%s more line%s: type more of the name" % (
                    commas(left), "" if left == 1 else "s"), "", Kit.HUE_INFO, 0,
                    "A search lists %d lines at most; the total above counts them all" % MAX_RESULT_ROWS, None))
            return rows
        def refresh(now):
            g = win["g"]
            if g is None or st["docked"]: return
            c = win["c"]
            if st["minimized"]:
                n = len(summ["places"]); view["status_key"] = None
                Kit.set_text(c.get("status"), TITLE + ": " + ("%s noted" % Kit.count(n, "place")
                                                              if idx["loaded"] else "reading the index"), Kit.HUE_INFO)
                return
            key = (view["query"], summ["ver"], view["live_ver"], view["sel"], view["page"], int(now // 30))
            if view["dirty"] or key != view["built_for"]:
                view["dirty"] = False; view["built_for"] = key; view["rows"] = results(now)
                pages = page_count()
                if view["page"] >= pages:
                    view["page"] = pages - 1; view["built_for"] = (key[0], key[1], key[2], key[3], view["page"], key[5])
                draw_rows(now, pages)
            if (view["status"] and view["naming"] is None and not 0 <= now - view["status_at"] <= 8.0):
                view["status"] = ""
            lbl = c.get("status")
            skey = (lbl, view["status"], view["status_hue"], idx["loaded"], idx["err"],
                    len(summ["places"]), summ["chars"], view["last_read"])
            old = view.get("status_key")
            if old is not None and old[0] is lbl and old[1:] == skey[1:]: return
            view["status_key"] = skey
            Kit.set_text(lbl, Kit.fit(view["status"] or idle_status(), view["iw"] - 20),
                         view["status_hue"] if view["status"] else Kit.HUE_INFO)
        def draw_rows(now, pages):
            rows = win["rows"]; off = view["page"] * len(rows); data, prev = view["data"], view["prev"]
            right_edge = M + view["iw"] - 10
            for i, r in enumerate(rows):
                j = off + i
                if j < len(view["rows"]): lt, rt, hue, indent, tip, d = view["rows"][j]
                else: lt, rt, hue, indent, tip, d = "", "", Kit.HUE_TEXT, 0, "", None
                rw = Kit.text_px(rt) if rt else 0; lx = M + 10 + indent; room = right_edge - lx - (rw + 8 if rt else 0)
                Kit.set_text(r["l"], Kit.fit(lt, room) if lt else "", hue); Kit.set_text(r["r"], rt, Kit.HUE_INFO)
                if lx != r["lx"]: r["lx"] = lx; Kit.ui_pos(r["l"], lx, r["y"])
                rx = right_edge - rw
                if rt and rx != r["rx"]: r["rx"] = rx; Kit.ui_pos(r["r"], rx, r["y"])
                if tip != r["tip"]: r["tip"] = tip; r["c"].SetTooltip(tip)
                if d != data[i]: prev[i] = (data[i], now); data[i] = d
            c = win["c"]
            Kit.set_text(c.get("page"), "%d / %d" % (view["page"] + 1, pages) if pages > 1 else "", Kit.HUE_INFO)
        def poll_box(now):
            box = win["c"].get("box")
            if box is None: return
            t = str(box.Text or "")
            if t != view["seen_text"]:
                if view["seen_text"] is not None: view["changed_at"] = now
                view["seen_text"] = t; return
            if view["changed_at"] and (now - view["changed_at"] >= SEARCH_WAIT or now < view["changed_at"]):
                view["changed_at"] = 0.0
                if view["naming"] is not None: return
                q = t.strip()
                if q.lower() != view["query"].lower(): view["query"] = q; view["page"] = 0; view["dirty"] = True
        def set_box(text):
            box = win["c"].get("box"); view["seen_text"] = text; view["changed_at"] = 0.0
            if box is not None: box.SetText(text)
        def live_tick(now):
            if not full_shown(): return
            if now < view["live_at"] and view["live_at"] - now <= LIVE_EVERY: return
            view["live_at"] = now + LIVE_EVERY; live = {}; items = HOST.pack_items(True, 1.0); q, n = 0, 0
            for x in items:
                n += 1
                if n > READ_MAX: break
                try: q = (q * 31 + int(x.Serial) + 7 * int(x.Amount or 0) + 13 * int(x.Container)) & 0xFFFFFFFFFFFF
                except Exception: continue
            if (q, n) == view["live_sig"]: return
            view["live_sig"] = (q, n)
            if items:
                n = 0
                for x in items:
                    n += 1
                    if n > READ_MAX: break
                    try: g, h = int(x.Graphic), int(x.Hue); a = max(1, int(x.Amount or 1)); name = item_name(x, g, a)
                    except Exception: continue
                    k = (g, h, name.lower()); e = live.get(k)
                    if e is None: live[k] = [name, a]
                    else: e[1] += a
            if live != view["live"]: view["live"] = live; view["live_ver"] += 1
        def resolve_row(i, t):
            if i >= len(view["data"]): return None
            old, changed = view["prev"][i]
            return old if changed and (changed >= t or t - changed < 0.15) else view["data"][i]
        def end_naming():
            if view["naming"] is not None: view["naming"] = None; set_box(view["query"])
        def show_window(action, now):
            if st["minimized"] or st["docked"]:
                st["minimized"] = st["docked"] = False; HOST.dock_forget(KEY); Kit.save_min(MIN_KEY, False)
                build_window()
            safe(lambda: Kit.client_control(win["g"]).BringOnTop())
        def follow_action(action, now): Follow.toggle(action[1], TITLE)
        def row_action(action, now):
            _, i, alt, t = action; d = resolve_row(i, t)
            if d is None: return
            if alt:
                if len(d) > 2 and d[2]: Follow.toggle(d[2], TITLE)
                return
            end_naming()
            if d[0] == "fav": view["query"] = d[1]; view["page"] = 0; set_box(d[1]); set_status("")
            elif d[0] == "place":
                view["sel"] = None if (d[3] and view["sel"] == d[1]) else d[1]
                p = summ["places"].get(view["sel"]) if view["sel"] else None
                set_status(("Picked: %s" % p["label"]) if p else "")
            view["dirty"] = True
        def add_fav(action, now):
            end_naming(); q = view["query"] or (view["seen_text"] or "").strip()
            if not q: set_status("Type what to look for first (a name, or a graphic like 0x0F88)", Kit.HUE_BAD)
            elif any(t.lower() == q.lower() for _, t in favs): set_status("\"%s\" is already a favourite" % q)
            elif len(favs) >= MAX_FAVS:
                set_status("%d favourites at most: take one off on the settings page" % MAX_FAVS, Kit.HUE_BAD)
            else:
                favs.append([clip(clean_text(q), NAME_MAX), clean_text(q)]); save_favs(); HOST.refresh_settings(KEY)
                set_status("Added \"%s\" to the favourites" % q, Kit.HUE_GOOD)
            view["dirty"] = True
        def name_action(action, now):
            sel = view["sel"]; p = summ["places"].get(sel) if sel else None
            if view["naming"] is not None:
                root = view["naming"]; text = clip(clean_text(view["seen_text"] or ""), NAME_MAX)
                r = idx["recs"].get(root); view["naming"] = None
                if r is not None:
                    post({"op": "name", "root": root, "text": text})
                    set_status(("Named it \"%s\"" % text) if text else "Its own name is back", Kit.HUE_GOOD)
                set_box(view["query"])
            elif p is None or sel not in idx["recs"]:
                set_status("Click a place in the list first, then Name", Kit.HUE_BAD)
            else:
                view["naming"] = sel; set_box("" if Kit.streamer and not p["custom"] else p.get("raw", p["label"]))
                set_status("Type its new name in the Find box, then click Name again "
                           "(empty: its own name)", Kit.HUE_TITLE)
        def forget_action(action, now):
            end_naming(); sel = view["sel"]; p = summ["places"].get(sel) if sel else None
            arm, at = view["forget_arm"]
            if p is None: set_status("Click a place in the list first, then Forget", Kit.HUE_BAD)
            elif arm == sel and 0 <= now - at <= 4.0:
                view["forget_arm"] = (None, 0.0); post({"op": "forget", "root": sel}); view["sel"] = None
                set_status("Forgot %s" % p["label"], Kit.HUE_GOOD)
            else:
                view["forget_arm"] = (sel, now)
                set_status("Click Forget again to forget %s (and the bags in it)" % p["label"], Kit.HUE_TITLE)
        def page_count(): per = max(1, len(win["rows"])); return max(1, (len(view["rows"]) + per - 1) // per)
        def page_step(action, now):
            pages = page_count()
            view["page"] = max(0, min(pages - 1, view["page"] + (1 if action == "next" else -1))); view["dirty"] = True
        ACTIONS = {"show": show_window, "follow": follow_action, "row": row_action, "fav": add_fav,
                   "name": name_action, "forget": forget_action, "next": page_step, "prev": page_step}
        def forget_place(root):
            recs = idx["recs"]; now = time.time()
            for s in [s for s, r in recs.items() if r["root"] == root or s == root]: del recs[s]; idx["tombs"][s] = now
            mark_dirty()
        def fav_h(): return 32 + max(1, len(favs)) * 24 + 8
        def draw_favs(f, x, y):
            if not favs:
                Kit.add_label(f.g, "No favourites yet: type a name in the Find box, then click Add favourite.",
                              x + 12, y + 2, Kit.HUE_INFO)
            for i, (label, term) in enumerate(favs):
                ry = y + i * 24
                Kit.art_button(f.g, f.store, "rm%d" % i, Kit.ART_CLOSE, x + 12, ry, None,
                               "Take %s off the favourites" % label)
                Kit.add_label(f.g, Kit.fit(label, 170), x + 48, ry + 3, Kit.HUE_TEXT)
                Kit.add_label(f.g, Kit.fit(term, f.w - 240), x + 226, ry + 3, Kit.HUE_INFO)
        def draw_wipe(f, x, y):
            page["wipe_at"] = 0.0
            f.c["wipe_lbl"] = Kit.art_button(f.g, f.store, "wipe", Kit.ART_CLOSE, x + 12, y, "Forget everything",
                                             "Empty the whole index, every character (click twice)")
        def page_table(w):
            n, nr = len(summ["places"]), len(idx["recs"])
            fname = os.path.basename(idx["path"]) if idx["path"] else "(not known yet)"
            return (("WHAT IT NOTES  (when you open a container)", (
                        ("check", "bank", "Bank boxes (and the bags in them)", "Note your bank box and its bags"),
                        ("check", "ground", "Chests and containers on the ground (in houses too)",
                         "Note chests and containers on the ground"),
                        ("check", "pack", "Your pack animals' packs", "Note your pack horse, llama or beetle",
                         {"h": 23}),
                        ("num", "days", "Forget places not seen for:", "Days a place stays after it was last opened "
                         "(1-3650)", "days", 1, 3650, {"lgap": 6, "fw": 44})), {"ch": 24, "sh": 134}),
                    ("FAVOURITES  (shown when the Find box is empty)", (("custom", 0, draw_favs),), {"sh": fav_h()}),
                    ("THE INDEX  (every character of the account)", (("note", Kit.fit("%s, %s, %s, %s" % (
                            Kit.count(n, "place"), Kit.count(nr, "container"), Kit.count(summ["items"], "item line"),
                            Kit.count(summ["chars"], "character")), w - 24), {"hue": Kit.HUE_TEXT}),
                        ("note", Kit.fit("File: %s, in VirtueAssistantSettings" % fname, w - 24), {"h": 14}),
                        ("custom", 0, draw_wipe)), {"sh": 92}))
        def read_days(f, new):
            d = Kit.read_int(f.c["days"], 0); new["days"] = min(3650, d) if d >= 1 else settings["days"]
        def page_clicks(f):
            store, c = f.store, f.c
            for i in range(len(favs)):
                if Kit.was_clicked(store, "rm%d" % i):
                    del favs[i]; save_favs(); view["dirty"] = True; HOST.refresh_settings(KEY); return
            at = page["wipe_at"]
            if at and not 0 <= time.time() - at <= 4.0:
                page["wipe_at"] = 0.0; Kit.set_text(c.get("wipe_lbl"), "Forget everything", Kit.HUE_TEXT)
            if Kit.was_clicked(store, "wipe"):
                now = time.time()
                if 0 <= now - page["wipe_at"] <= 4.0:
                    page["wipe_at"] = 0.0
                    post({"op": "wipe"}); quick.clear(); view["sel"] = None
                    API.SysMsg("%s: the index is empty." % TITLE, Kit.HUE_GOOD); HOST.refresh_settings(KEY)
                else: page["wipe_at"] = now; Kit.set_text(c.get("wipe_lbl"), "Click again to empty it", Kit.HUE_BAD)
        cfg = Kit.Page(settings, page_table, save_settings, adjust=read_days, clicks=page_clicks)
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "active": True, "check_at": 0.0,
                       "merge_at": 0.0, "minimized": wnd.start_min()})
            load_settings(); load_favs(); watching.clear(); feed["q"] = unread(); del opens[:]
            view.update({"sel": None, "naming": None, "status": "", "page": 0, "dirty": True})
            idx["path"] = Kit.data_path(FILE_FMT % account_id()); hook_events(); build_window()
            wnd.dock(fit=True, min=(W, H - (ROWS - 4) * ROW_H)); cleanup.service("storage.show", queue("show"))
        def _tick():
            if win["g"] is None: return
            if Kit.closed(win): return
            now = time.time()
            if feed["q"] and feed["q"][0]["n"] <= took["n"]: feed["q"] = unread()
            while opens: note_open(opens.pop(0))
            watch_tick(now)
            while st["queue"]:
                action = st["queue"].pop(0)
                if not wnd.action(action):
                    fn = ACTIONS.get(action[0] if isinstance(action, tuple) else action)
                    if fn is not None: fn(action, now)
                if win["g"] is None: return
            if full_shown(): poll_box(now); live_tick(now)
            refresh(now)
        def _thread_tick():
            if st["shutting"]: return
            if not idx["loaded"]:
                try: load_index()
                except Exception as ex: idx["loaded"], idx["err"] = True, str(ex)[:60]
            take_reads(); now = time.time()
            if idx["dirty"] and (now - idx["dirty_at"] >= SAVE_DELAY or now < idx["dirty_at"]):
                save_index(); st["merge_at"] = now + MERGE_CHECK
            elif now >= st["merge_at"] or st["merge_at"] - now > MERGE_CHECK:
                st["merge_at"] = now + MERGE_CHECK; check_others()
            if summ["ver"] != idx["ver"] or summ["veil"] != Kit.streamer:
                build_summary(); fav_stored()
                if view["query"]: search_stored(view["query"])
        def _thread_wanted():
            if st["shutting"]: return False
            if not idx["loaded"] or has_unread() or summ["ver"] != idx["ver"] or summ["veil"] != Kit.streamer:
                return True
            now = time.time()
            if idx["dirty"] and (now - idx["dirty_at"] >= SAVE_DELAY or now < idx["dirty_at"]): return True
            return now >= st["merge_at"] or st["merge_at"] - now > MERGE_CHECK
        load_settings()
        def _stop():
            st["shutting"] = True; st["active"] = False
            if has_unread() or idx["dirty"]:
                with Kit.quiet:
                    if not idx["loaded"]: load_index()
                    take_reads(); save_index()
            watching.clear(); del opens[:]; cleanup.close()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed,
                "thread_tick": _thread_tick, "thread_wanted": _thread_wanted}
    def _part_restock():
        KEY = "restock"; TITLE = "Restock"; SETTINGS_KEY = "Restock_settings"; POS_KEY = "Restock_pos"
        MIN_KEY = "Restock_min"; TARGETS_KEY = "Restock_targets"; W = 400; MINI_W, MINI_H = 240, 46; TRAY_ICON = 0x0E79
        ROW_H = 22; ICON = 20; PAGE_ROWS = 12; ART_BACK = (4014, 4016, 4015); MOVE_GAP = 0.7; NOCHANGE_WAIT = 3.0
        ANSWER_WAIT = 10.0; FAIL_STOP = 3; WAIT_RETRY = 3; LIMBO_WAIT = ANSWER_WAIT; OPEN_WAIT = 3.0; REACH = 2
        WEIGHT_SPARE = 0; TARGET_MAX = 60000; COUNT_EVERY = 1.0; POLL_EVERY = 0.25; PICK_TIMEOUT = 20.0
        J_FULL = ("cannot hold more",); J_WAIT = ("must wait to perform another action",)
        J_DENY = ("can not pick that up", "cannot pick that up", "that is too far away",
                  "that is out of sight", "does not belong to you", "already holding an item")
        UNIT_WEIGHT = {"REAGENTS": 0.1, "POTIONS": 1.0, "SCROLLS": 1.0, "OTHER": 0.1}; WEIGHT_FALLBACK = (40.0, 3.5)
        ALERT_STOP = "restock.stopped"; ALERT_STOP_SOUND = 0x04A; CORPSE = 0x2006; ORDER = tuple(r[0] for r in ITEMS)
        BY_KEY = dict((r[0], r) for r in ITEMS); KEY_OF = dict((r[3], r[0]) for r in ITEMS)
        KIND_WORD = {"POTIONS": " potion", "SCROLLS": " scroll"}; SRC_MODES = ("last", "bank", "pick")
        SRC_BUTTONS = (("last", "Last opened", "Take from the container you opened last"),
                       ("bank", "Bank box", "Take from your bank box (say \"bank\" near a banker to open it)"),
                       ("pick", "Pick...", "Target a chest to take from; remembered, opened once if closed"))
        DEST_BUTTONS = (("pack", "Backpack", "Restock into your backpack"),
                        ("bag", "Pick bag...", "Target a bag in your backpack to restock into"))
        settings = {"deep": True, "src_deep": True, "src": "last", "src_serial": 0, "dest": 0}; targets = {}
        DEFAULTS = dict(settings)
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [], "run": None,
              "halt": False, "status": ("Idle", Kit.HUE_INFO), "last_open": 0, "opened": [],
              "page": 0, "count_at": 0.0, "short": {}, "layout": None,
              "hooked": False, "active": False, "redraw": False, "shown_moved": 0, "sent_at": 0.0, "flight": []}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": [], "tips": {}}
        cleanup, queue, say = Kit.basics(st, TITLE)
        def noop(): pass
        def load_settings():
            settings.update({"deep": True, "src_deep": True, "src": "last", "src_serial": 0, "dest": 0})
            for part in Kit.get_var(SETTINGS_KEY).split(";"):
                if "=" not in part: continue
                k, v = [s.strip() for s in part.split("=", 1)]
                if k in ("deep", "src_deep"): settings[k] = v == "1"
                elif k == "src" and v in SRC_MODES: settings["src"] = v
                elif k in ("src_serial", "dest"):
                    try: n = int(v)
                    except ValueError: continue
                    if 0 <= n <= 0xFFFFFFFF: settings[k] = n
            targets.clear()
            for part in Kit.get_var(TARGETS_KEY).split(","):
                if "=" not in part: continue
                k, v = [s.strip() for s in part.split("=", 1)]
                if k in BY_KEY and v.isdigit():
                    n = min(TARGET_MAX, int(v))
                    if n > 0: targets[k] = n
        def save_settings():
            Kit.put_var(SETTINGS_KEY, "deep=%d;src_deep=%d;src=%s;src_serial=%d;dest=%d" % (
                settings["deep"], settings["src_deep"], settings["src"], settings["src_serial"], settings["dest"]))
        def num(obj, attr, default=0):
            try: v = getattr(obj, attr); return default if v is None else int(v)
            except Exception: return default
        def no_container(c): return not c or c == 0xFFFFFFFF
        def row_name(k): return BY_KEY[k][2] + KIND_WORD.get(BY_KEY[k][1], "")
        top_of = Kit.top_of; in_pack = Kit.in_pack
        def backpack(): return int(API.Backpack or 0)
        def bank_box(): return int(API.Bank or 0)
        def item_name(it, fallback="container"):
            try: n = str(it.Name or "").strip()
            except Exception: n = ""
            return n or fallback
        def contents(serial, deep):
            try: return list(API.ItemsInContainer(int(serial), bool(deep)) or [])
            except Exception: return []
        held_item = Kit.held_item
        def cursor_up(): return bool(HOST.cursor_busy(KEY) or API.HasTarget())
        def dest_serial(): d = settings["dest"]; return d if d else backpack()
        def pack_counts(dest, deep=None, max_age=0.0):
            pack = backpack()
            if not pack: return {}
            if settings["deep"] if deep is None else deep: items = HOST.pack_items(True, max_age)
            else:
                items = HOST.pack_items(False, max_age)
                if dest and dest != pack: items = items + contents(dest, False)
            out = {}
            for it in items:
                try:
                    k = KEY_OF.get(int(it.Graphic))
                    if k is None: continue
                    out[k] = out.get(k, 0) + max(1, int(it.Amount or 1))
                except Exception: continue
            return out
        def source_stacks(src, deep):
            out = {}
            for it in contents(src, deep):
                try:
                    k = KEY_OF.get(int(it.Graphic))
                    if k is None: continue
                    out.setdefault(k, []).append((max(1, int(it.Amount or 1)), int(it.Serial)))
                except Exception: continue
            return out
        def weight_room():
            try:
                p = API.Player; w = float(p.Weight or 0); mx = float(p.WeightMax or 0)
                if mx <= 0: mx = WEIGHT_FALLBACK[0] + WEIGHT_FALLBACK[1] * float(p.Strength or 0)
                return None if mx <= 0 else mx - WEIGHT_SPARE - w
            except Exception: return None
        def source_info():
            mode = settings["src"]
            if mode == "bank":
                b = bank_box()
                if not b:
                    return (0, "Your bank box (not open)", "open your bank box first (say \"bank\" near a banker)")
                try: open_ = len(API.ItemsInContainer(b, False) or ()) > 0
                except Exception: open_ = False
                return b, "Your bank box" + ("" if open_ else " (not open)"), None
            if mode == "pick":
                s = settings["src_serial"]
                if not s: return 0, "Nothing picked yet", "pick the chest first (Pick...)"
                it = API.FindItem(s)
                if it is None: return (0, "The picked chest (out of view)", "the chest you picked is out of view")
                return s, where_text(it), None
            s = st["last_open"]; it = API.FindItem(s) if s else None
            if it is None: return 0, "Last opened: none yet", "open a chest or your bank box first"
            return s, "Last opened: " + where_text(it), None
        def where_text(it):
            if int(it.Serial) == bank_box(): return "your bank box"
            name = item_name(it)
            if num(it, "OnGround") or no_container(num(it, "Container")):
                return "%s at %s" % (name, Kit.veil("xy", "%d, %d" % (num(it, "X"), num(it, "Y"))))
            return name
        def dest_info():
            d = settings["dest"]
            if not d: return "Your backpack", None
            it = API.FindItem(d)
            if it is None or not in_pack(d):
                return "The picked bag (not in your backpack)", \
                    "the bag you picked isn't in your backpack: pick it again or choose Backpack"
            return item_name(it, "bag") + " in your backpack", None
        def source_ok(serial):
            if not serial: return "nothing was targeted"
            it = API.FindItem(serial)
            if it is None: return "that isn't an item"
            top, _on = top_of(serial); t = API.FindItem(top) if top != int(serial) else it
            for x in (it, t):
                if x is not None and (num(x, "Graphic") == CORPSE or num(x, "IsCorpse")):
                    return "a corpse (or a bag in one) isn't a source"
            if in_pack(serial): return "that is in your backpack"
            return "that isn't a container" if not (num(it, "IsContainer") or contents(serial, False)) else None
        def out_of_reach(src):
            it = API.FindItem(src)
            if it is None: return "the source is out of view"
            top, on = top_of(src)
            if on:
                p = API.Player
                if on == num(p, "Serial"): return None
                m = API.FindMobile(on)
                if m is None or not num(m, "IsRenamable"): return "the source is on someone else"
                d = max(abs(num(m, "X") - num(p, "X")), abs(num(m, "Y") - num(p, "Y")))
                return "your pack animal is out of reach (step next to it)" if d > REACH else None
            t = API.FindItem(top)
            if t is None: return None
            try: p = API.Player; d = max(abs(num(t, "X") - num(p, "X")), abs(num(t, "Y") - num(p, "Y")))
            except Exception: return None
            return "the source is out of reach (step next to it)" if d > REACH else None
        def on_open(*args):
            if not st["active"]: return
            for a in args:
                try: s = int(a.Serial or 0)
                except AttributeError:
                    try: s = int(a or 0)
                    except Exception: s = 0
                except Exception: s = 0
                if s: st["opened"].append(s); del st["opened"][:-8]; return
        def hook_events(): Kit.hook_once(st, "hooked", ("OnOpenContainer", on_open))
        def take_opened():
            while st["opened"]:
                s = st["opened"].pop(0)
                if source_ok(s) is None: st["last_open"] = s
        def set_status(text, hue=None):
            st["status"] = (text, Kit.HUE_INFO if hue is None else hue); lbl = win["c"].get("status")
            if lbl is not None:
                if st["minimized"]: text = TITLE + ": " + text[:1].lower() + text[1:]
                Kit.set_text(lbl, Kit.fit(text, win["c"].get("status_w", 200)), st["status"][1])
        def start_run():
            if st["run"] is not None: say("already restocking; press Stop first.", Kit.HUE_BAD); return
            rows = [k for k in ORDER if targets.get(k, 0) > 0]
            if not rows:
                say("the list is empty: set how many of each item to carry on the settings page.", Kit.HUE_BAD)
                HOST.show_settings(KEY); return
            src, _lbl, why = source_info()
            if why is None: why = source_ok(src) or out_of_reach(src)
            if why is None:
                dest = dest_serial(); why = None if dest else "you have no backpack"
                if why is None: why = dest_info()[1]
            if why is None and cursor_up(): why = "a target cursor is up"
            if why is None and held_item(): why = "you are holding an item"
            if why is None and num(API.Player, "IsDead"): why = "you are dead"
            if why is not None:
                say("can't restock: %s." % why, Kit.HUE_BAD); set_status("Can't: " + why, Kit.HUE_BAD); return
            now = time.time()
            r = {"src": src, "dest": dest, "deep": settings["deep"], "src_deep": settings["src_deep"],
                 "phase": "go", "open_until": 0.0, "move": None,
                 "check": None, "at": now, "hold": 0.0, "sent_at": 0.0, "last": 0, "left": False, "c0": 0,
                 "moved": 0, "moves": 0, "refused": 0, "streak": 0, "waits": 0,
                 "why": None, "bad": set(), "limbo": [e for e in st["flight"] if 0 <= e[2] - now <= LIMBO_WAIT]}
            if 0 <= now - st["sent_at"] < MOVE_GAP: r["at"] = st["sent_at"] + MOVE_GAP
            st.update({"flight": [], "short": {}, "halt": False})
            if not contents(src, False):
                if src == bank_box():
                    say("your bank box isn't open: say \"bank\" near a banker first.", Kit.HUE_BAD)
                    set_status("Bank box not open", Kit.HUE_BAD); return
                API.UseObject(src); r.update({"phase": "open", "open_until": now + OPEN_WAIT})
                set_status("Opening the chest")
            else: set_status("Restocking")
            st["run"] = r; say("restocking %s." % Kit.count(len(rows), "item")); refresh_buttons()
        def limbo_of(r, key, now):
            n = 0; keep = []
            for e in r["limbo"]:
                if 0 <= e[2] - now <= LIMBO_WAIT:
                    keep.append(e)
                    if e[0] == key: n += e[1]
            r["limbo"] = keep; return n
        def run_step(now):
            r = st["run"]
            if r is None or r["move"] is not None: return
            if r["check"] is not None and not r["left"]:
                it = API.FindItem(r["check"][1])
                if it is None or num(it, "Container") != r["c0"]: r["left"] = True
            if r["why"]: stop_run(r["why"]); return
            if r["phase"] == "open":
                if contents(r["src"], False): r["phase"] = "go"; set_status("Restocking")
                elif not 0 <= r["open_until"] - now <= OPEN_WAIT: stop_run("the chest didn't open (or it is empty)")
                return
            if r["check"] is not None:
                if 0 < r["at"] - now <= MOVE_GAP or not check_move(r, now): return
            if 0 < r["hold"] - now <= MOVE_GAP or 0 < r["at"] - now <= MOVE_GAP: return
            if cursor_up(): stop_run("a target cursor is up"); return
            h = held_item()
            if h and not (h == r["last"] and 0 <= now - r["sent_at"] < 2 * MOVE_GAP):
                stop_run("you picked something up"); return
            if num(HOST.me(), "IsDead"): stop_run("you died"); return
            why = out_of_reach(r["src"])
            if why: stop_run(why); return
            next_move(r, now)
        def next_move(r, now):
            have = pack_counts(r["dest"], r["deep"]); stacks = source_stacks(r["src"], r["src_deep"]); waiting = False
            for key in ORDER:
                t = targets.get(key, 0)
                if t <= 0: continue
                held_back = limbo_of(r, key, now); need = t - have.get(key, 0) - held_back
                if need <= 0:
                    if held_back: waiting = True
                    st["short"].pop(key, None); continue
                mine = [s for s in stacks.get(key, ()) if s[1] not in r["bad"]]
                if not mine: st["short"][key] = need; continue
                amount, serial = max(mine); take = min(amount, need); room = weight_room()
                if room is not None:
                    fit = int(room / UNIT_WEIGHT.get(BY_KEY[key][1], 1.0) + 1e-6)
                    if fit < 1: stop_run("you are at your weight limit"); return
                    take = min(take, fit)
                st["short"].pop(key, None); it = API.FindItem(serial)
                r["c0"] = num(it, "Container") if it is not None else 0
                r["move"] = (key, serial, take, have.get(key, 0))
                set_status("Moving %s: %d (%d moved)" % (row_name(key), take, r["moved"])); return
            if waiting: set_status("Waiting for the server"); r["hold"] = now + MOVE_GAP; return
            finish_run()
        def check_move(r, now):
            key, serial, amt, have0 = r["check"]; t0 = r["sent_at"]
            if Journal.find(t0, J_FULL) is not None:
                stop_run("your %s can't hold more" % ("backpack" if r["dest"] == backpack() else "bag")); return False
            have1 = pack_counts(r["dest"], r["deep"]).get(key, 0); age = now - t0; it = API.FindItem(serial)
            where = num(it, "Container") if it is not None else 0; landed = have1 > have0
            if not landed and it is not None and not no_container(where) and where != r["c0"]:
                landed = in_pack(serial)
                if landed: have1 = have0 + amt
            if landed:
                got = min(have1 - have0, amt); r["moved"] += got
                if got < amt: r["limbo"].append([key, amt - got, now + LIMBO_WAIT])
                r.update({"check": None, "left": False, "streak": 0, "waits": 0}); return True
            back = it is not None and where == r["c0"]
            if not back or held_item() == serial:
                r["left"] = True
                if not 0 <= age < ANSWER_WAIT:
                    stop_run("the server hasn't answered a move for %d s" % int(ANSWER_WAIT)); return False
                if age >= 2 * MOVE_GAP: set_status("Waiting for the server")
                r["at"] = now + MOVE_GAP * 0.5; return False
            if Journal.find(t0, J_WAIT) is not None and r["waits"] < WAIT_RETRY:
                r["waits"] += 1
                if not r["left"]: r["limbo"].append([key, amt, now + LIMBO_WAIT])
                r.update({"check": None, "left": False, "hold": now + MOVE_GAP}); return False
            said = Journal.find(t0, J_DENY) is not None
            if not (said or r["left"]) and 0 <= age < NOCHANGE_WAIT: r["at"] = now + MOVE_GAP * 0.5; return False
            if not r["left"]: r["limbo"].append([key, amt, now + LIMBO_WAIT])
            r.update({"check": None, "left": False, "waits": 0}); r["refused"] += 1; r["streak"] += 1
            r["bad"].add(serial)
            if r["streak"] >= FAIL_STOP: stop_run("%d moves in a row were refused" % r["streak"]); return False
            return True
        def send_move():
            r = st["run"]
            if r is None or r["move"] is None: return
            mv = r["move"]; r["move"] = None
            if st["halt"] or st["shutting"]: return
            try: API.MoveItem(mv[1], r["dest"], mv[2])
            except Exception as ex: r["why"] = "a move failed (%s)" % ex; return
            HOST.pack_dirty(); r.update({"check": mv, "left": False, "last": mv[1]})
            r["sent_at"] = st["sent_at"] = time.time(); r["at"] = r["sent_at"] + MOVE_GAP; r["moves"] += 1
        def short_text():
            if not st["short"]: return ""
            parts = ["%s %d" % (row_name(k), n) for k, n in
                     sorted(st["short"].items(), key=lambda kv: ORDER.index(kv[0]))]
            return "; short (none left in the source): " + ", ".join(parts[:6]) + \
                (" and %d more" % (len(parts) - 6) if len(parts) > 6 else "")
        def keep_flight(r):
            if r is None: return
            out = [list(e) for e in r["limbo"]]
            if r["check"] is not None:
                key, _serial, amt, _h0 = r["check"]; out.append([key, amt, r["sent_at"] + ANSWER_WAIT])
            if out: st["flight"] = (st["flight"] + out)[-20:]
        def finish_run():
            r, st["run"] = st["run"], None
            if r is None: return
            keep_flight(r); msg = ("done: %d moved in %s" % (r["moved"], Kit.count(r["moves"], "move")))
            if r["refused"]: msg += ", %d refused" % r["refused"]
            say(msg + short_text() + ".", Kit.HUE_BAD if st["short"] or r["refused"] else Kit.HUE_GOOD)
            set_status("Done: %d moved%s" % (r["moved"], ", some short" if st["short"] else ""),
                       Kit.HUE_TITLE if st["short"] else Kit.HUE_GOOD)
            st["count_at"] = 0.0; refresh_buttons()
        def stop_run(why=None, user=False):
            r, st["run"] = st["run"], None; st["halt"] = True
            if r is None: return
            keep_flight(r)
            if user: say("stopped (%d moved)." % r["moved"]); set_status("Stopped (%d moved)" % r["moved"])
            else:
                text = "%s (%d moved)" % (why or "stopped", r["moved"])
                if not HOST.alert(ALERT_STOP, "Stopped: " + text, "warn"): say("stopped: " + text + ".", Kit.HUE_BAD)
                set_status("Stopped: " + (why or ""), Kit.HUE_BAD)
            st["count_at"] = 0.0; refresh_buttons()
        def halt_click(): st["halt"] = True; queue("stop")()
        def list_keys(): return [k for k in ORDER if targets.get(k, 0) > 0]
        FIXED_H = 2 * Kit.MARGIN + 30 + 3 * Kit.GAP + 136 + 64
        def layout_now():
            keys = list_keys(); per = wnd.rows(ROW_H, FIXED_H + list_h(0) - 2 * ROW_H, PAGE_ROWS, 2)
            pages = max(1, (len(keys) + per - 1) // per); pg = min(st["page"], pages - 1)
            return (st["minimized"], st["docked"], pg, pages, tuple(keys[pg * per:(pg + 1) * per]))
        def build_window():
            lay = layout_now(); st["page"] = lay[2]; st["layout"] = lay; mini = st["minimized"]
            told = wnd.slot if HOST.layout_holds(KEY) else None
            w, h = (MINI_W, MINI_H) if mini else (told or (W, FIXED_H + list_h(len(lay[4]))))
            g, store, c = wnd.begin(w, h); M = Kit.MARGIN; rows = []
            if mini: c["status_w"] = w - 90
            else:
                IW = w - 2 * M; wnd.frame(g); ya = M + 30 + Kit.GAP; Kit.add_section(g, M, ya, IW, 136, "FROM AND TO")
                Kit.add_label(g, "From:", M + 12, ya + 30, Kit.HUE_INFO)
                lx = M + 12 + max(Kit.text_w("From:"), Kit.text_w("Into:")) + 10
                c["src"] = Kit.add_label(g, "", lx, ya + 30); c["src_w"] = IW - (lx - M) - 8; bx = M + 12
                for mode, cap, tip in SRC_BUTTONS:
                    c["m_" + mode] = Kit.art_button(g, store, "m_" + mode, Kit.ART_PAGE, bx, ya + 52, cap, tip,
                        Kit.HUE_TITLE if settings["src"] == mode else Kit.HUE_TEXT, on_click=queue(("src", mode)))
                    bx += 35 + Kit.text_w(cap) + 14
                Kit.add_label(g, "Into:", M + 12, ya + 84, Kit.HUE_INFO); c["dest"] = Kit.add_label(g, "", lx, ya + 84)
                bx = M + 12
                for mode, cap, tip in DEST_BUTTONS:
                    c["d_" + mode] = Kit.art_button(g, store, "d_" + mode, Kit.ART_PAGE, bx, ya + 106, cap, tip,
                        Kit.HUE_TITLE if (mode == "bag") == bool(settings["dest"]) else Kit.HUE_TEXT,
                        on_click=queue(("dest", mode)))
                    bx += 35 + Kit.text_w(cap) + 14
                yb = ya + 136 + Kit.GAP; hb = h - FIXED_H if told else list_h(len(lay[4]))
                Kit.add_section(g, M, yb, IW, hb, "LIST  (carried / to carry)")
                if lay[3] > 1:
                    px = M + IW - 12 - 21
                    Kit.art_button(g, store, "next", Kit.ART_PLAY, px, yb + 4, None, "Next page",
                                   on_click=queue(("page", 1)))
                    Kit.add_label(g, "%d/%d" % (lay[2] + 1, lay[3]), px - 8 - Kit.text_w("%d/%d" % (lay[3], lay[3])),
                                  yb + 6, Kit.HUE_INFO)
                    Kit.art_button(g, store, "prev", ART_BACK,
                                   px - 16 - Kit.text_w("%d/%d" % (lay[3], lay[3])) - 21, yb + 4,
                                   None, "Previous page", on_click=queue(("page", -1)))
                if not lay[4]:
                    Kit.add_label(g, "The list is empty: set how many to carry", M + 12, yb + 30, Kit.HUE_INFO)
                    Kit.add_label(g, "on the " + TITLE + " settings page.", M + 12, yb + 50, Kit.HUE_INFO)
                cx = M + IW - 100
                for i, k in enumerate(lay[4]):
                    ry = yb + 28 + i * ROW_H; _key, _grp, name, graphic = BY_KEY[k]
                    item_pic(g, graphic, 0, M + 12, ry, ICON)
                    Kit.add_label(g, Kit.fit(name, cx - (M + 12 + ICON + 6) - 8), M + 12 + ICON + 6, ry + 2)
                    lbl = Kit.add_label(g, "", cx, ry + 2); tip = Kit.catcher(g, M + 8, ry, IW - 16, ROW_H, noop, name)
                    rows.append({"key": k, "count": lbl, "tip": tip})
                yc = yb + hb + Kit.GAP; Kit.add_section(g, M, yc, IW, 64)
                Kit.art_button(g, store, "go", Kit.ART_PLAY, M + 12, yc + 8, "Restock",
                               "Top each item up to its target from the source (one move every %.1f s)" % MOVE_GAP,
                               on_click=queue("go"))
                sx = M + 12 + 35 + Kit.text_w("Restock") + 18
                Kit.art_button(g, store, "stop", Kit.ART_CLOSE, sx, yc + 8, "Stop", "Stop moving items",
                               on_click=halt_click)
                c["status"] = Kit.add_label(g, "", M + 12, yc + 40, st["status"][1]); c["status_w"] = IW - 24
            wnd.end(g, {"rows": rows, "tips": {}}); set_status(*st["status"]); st["count_at"] = 0.0
            refresh(time.time())
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, (240, 220), icon=TRAY_ICON,
                         cleanup=cleanup, clear={"c": {}, "rows": []})
        def list_h(n): return 30 + max(2, n) * ROW_H + 6
        def refresh_buttons():
            c = win["c"]
            for mode, cap, _tip in SRC_BUTTONS:
                lbl = c.get("m_" + mode)
                if lbl is not None: Kit.set_text(lbl, cap, Kit.HUE_TITLE if settings["src"] == mode else Kit.HUE_TEXT)
            for mode, cap, _tip in DEST_BUTTONS:
                lbl = c.get("d_" + mode)
                if lbl is not None:
                    Kit.set_text(lbl, cap, Kit.HUE_TITLE if (mode == "bag") == bool(settings["dest"]) else Kit.HUE_TEXT)
        def refresh(now):
            g = win["g"]
            if g is None or st["minimized"]: return
            if 0 <= now - st["count_at"] < COUNT_EVERY: return
            st["count_at"] = now; c = win["c"]; _s, slbl, _why = source_info()
            Kit.set_text(c["src"], Kit.fit(slbl, c["src_w"])); dlbl, dwhy = dest_info()
            Kit.set_text(c["dest"], Kit.fit(dlbl, c["src_w"]), Kit.HUE_BAD if dwhy else Kit.HUE_TEXT)
            if not win["rows"]: return
            have = pack_counts(dest_serial(), None, 0.0 if st["run"] is not None else 0.5); tips = win["tips"]
            for row in win["rows"]:
                k = row["key"]; n, t = have.get(k, 0), targets.get(k, 0)
                hue = Kit.HUE_GOOD if n >= t else (Kit.HUE_BAD if n == 0 else Kit.HUE_TITLE)
                Kit.set_text(row["count"], "%d / %d" % (n, t), hue); tkey = (n, t, st["short"].get(k))
                if tips.get(k) == tkey: continue
                tip = "%s: %d in your pack, target %d" % (row_name(k), n, t)
                if k in st["short"]: tip += " (short by %d: none left in the source)" % st["short"][k]
                tips[k] = tkey; row["tip"].SetTooltip(tip)
        def ask_pick(what):
            if st["run"] is not None: say("press Stop first.", Kit.HUE_BAD); return
            say("target the chest to take from." if what == "src" else "target a bag in your backpack.")
            def done(serial): queue(("picked", what, int(serial or 0)))()
            HOST.pick_target(PICK_TIMEOUT, done, KEY)
        def picked(what, serial):
            if not serial: return
            if what == "src":
                why = source_ok(serial)
                if why: say("not a source: %s." % why, Kit.HUE_BAD); return
                settings["src"], settings["src_serial"] = "pick", serial; save_settings(); it = API.FindItem(serial)
                say("taking from %s." % (where_text(it) if it is not None else "it"), Kit.HUE_GOOD)
            else:
                pack = backpack()
                if serial == pack: settings["dest"] = 0
                else:
                    it = API.FindItem(serial)
                    if it is None or not in_pack(serial) or not (num(it, "IsContainer") or contents(serial, False)):
                        say("pick a bag that is in your backpack.", Kit.HUE_BAD); return
                    settings["dest"] = serial
                save_settings()
            st["count_at"] = 0.0; refresh_buttons()
        def group_rows(grp): return [r for r in ITEMS if r[1] == grp]
        def group_h(grp): n = len(group_rows(grp)); return 30 + ((n + 1) // 2) * 26 + 6
        def stop_action(action):
            if st["run"] is not None: stop_run(user=True)
        def pick_place(action):
            kind = action[0]
            if st["run"] is not None: say("press Stop first.", Kit.HUE_BAD)
            elif action[1] == ("pick" if kind == "src" else "bag"): ask_pick(kind)
            else:
                settings[kind] = action[1] if kind == "src" else 0; save_settings(); st["count_at"] = 0.0
                refresh_buttons()
        def turn_page(action): pages = layout_now()[3]; st["page"] = (st["page"] + action[1]) % pages; build_window()
        ACTIONS = {"go": lambda action: start_run(), "stop": stop_action, "src": pick_place, "dest": pick_place,
                   "picked": lambda action: picked(action[1], action[2]), "page": turn_page}
        OPT_H = 30 + 2 * 28 + 24 + 8
        def page_table(w):
            half = (w - 24) // 2
            return [("%s  (%s)" % (gp, "how many to carry, 0 = leave alone" if gp == "REAGENTS"
                                   else "how many to carry"),
                     [("num", k, Kit.fit(name, half - 76), "%s: how many to carry (0-%d, 0 = leave it alone)"
                       % (row_name(k), TARGET_MAX), None, 0, TARGET_MAX,
                       {"dx": 12 + (i % 2) * half, "stay": i % 2 == 0})
                      for i, (k, _grp, name, _gr) in enumerate(group_rows(gp))],
                     {"sh": group_h(gp), "lw": half - 78, "fw": 52, "fh": 26}) for gp in GROUPS] + [
                    ("OPTIONS", (("check", "deep", "Count inside bags in your pack", "Bags inside your backpack count "
                                  "too (as Inventory > Supplies and Grimoire)", {"h": 28}),
                                 ("check", "src_deep", "Take from bags inside the source too", "Bags inside the "
                                  "chest or bank box too (only those whose contents you have seen)", {"h": 30}),
                                 ("note", "One move every %.1f s; it stops when you pick something up." % MOVE_GAP)),
                     {"sh": OPT_H})]
        def page_change(old, new):
            if (new["deep"], new["src_deep"]) != (old["deep"], old["src_deep"]):
                settings.update(deep=new["deep"], src_deep=new["src_deep"]); save_settings(); st["count_at"] = 0.0
            if any(new[k] != old[k] for k in ORDER):
                targets.clear(); targets.update((k, new[k]) for k in ORDER if new[k] > 0)
                Kit.put_var(TARGETS_KEY, ",".join("%s=%d" % (k, targets[k]) for k in ORDER if targets.get(k, 0) > 0))
                st["count_at"] = 0.0
                if layout_now() != st["layout"]: st["redraw"] = True
        cfg = Kit.Page(settings, page_table, None, page_change, every=POLL_EVERY)
        def build_config(g, x, y, w):
            cfg.vals = dict(settings); cfg.vals.update((k, targets.get(k, 0)) for k in ORDER); cfg.build(g, x, y, w)
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "run": None, "halt": False,
                       "status": ("Idle", Kit.HUE_INFO), "opened": [], "page": 0,
                       "count_at": 0.0, "short": {}, "layout": None,
                       "active": True, "redraw": False, "shown_moved": 0, "minimized": wnd.start_min()})
            load_settings(); HOST.alert_kind(ALERT_STOP, "Restock stopped early", ALERT_STOP_SOUND)
            hook_events(); build_window(); cleanup.service("restock.run", queue("go"))
            wnd.dock(fit=True, min=(W, FIXED_H + list_h(2)))
        def _tick():
            if win["g"] is None: return
            if Kit.closed(win): return
            if st["opened"]: take_opened()
            while st["queue"]:
                action = st["queue"].pop(0)
                if wnd.action(action): continue
                fn = ACTIONS.get(action[0] if isinstance(action, tuple) else action)
                if fn is not None: fn(action)
            if st["redraw"]:
                st["redraw"] = False
                if layout_now() != st["layout"]: build_window()
            now = time.time(); r = st["run"]
            if r is not None:
                run_step(now); send_move()
                if r["moved"] != st["shown_moved"]: st["shown_moved"] = r["moved"]; st["count_at"] = 0.0
            refresh(now)
        def _interval(): return 0.05 if st["run"] is not None else 0.1
        load_settings()
        def _stop():
            st.update({"shutting": True, "halt": True, "active": False}); r, st["run"] = st["run"], None; keep_flight(r)
            save_settings(); cleanup.close()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True,
                "config_height": cfg.height, "build_config": build_config, "poll_config": cfg.poll,
                "config_closed": cfg.closed, "interval": _interval}
    def _part_supplies():
        KEY = "supplies"; TITLE = "Supplies"; OLD_SETTINGS_KEY = "UnitFrames_settings"; SET_KEY = "UnitFrames_supset"
        SAVE_EVERY = 10.0; PACK_AGE = 0.5; SUPPLY_EVERY = 1.0; SUPPLY_W = 220; SUPPLY_ROW = 22; SUPPLY_ICON = 20
        SUPPLY_ROW_MIN = 20
        SUPPOS_KEY = "UnitFrames_suppos"; SUPPLY_SIDES = ("Below the frame", "Left of the frame", "Right of the frame")
        SUPPLY_LOW_DEFAULT = 10; SUPPLY_SOON = 0.1; ROWS_POLL = 0.25; SUPPLY_ITEMS = tuple(r + (None,) for r in ITEMS)
        SUPPLY_DEFAULT = ("bp", "bm", "ga", "gi", "mr", "ns", "ss", "sa",
                          "p_heal", "p_cure", "p_refresh", "s_recall", "s_gate", "o_band")
        SUPPLIES_KEY = "UnitFrames_supplies"; SUPWARN_KEY = "UnitFrames_supwarn"; HUE_LOW = Kit.HUE_TITLE
        WARN_READ_EVERY = 0.25; WARN_MAX = 9999; ANCHOR = "frames.player_anchor"
        settings = {"sup_open": False, "sup_deep": True, "sup_hide0": False, "sup_follow": True,
                    "sup_low": SUPPLY_LOW_DEFAULT, "sup_side": 0}
        DEFAULTS = dict(settings); NUMBERS = {"sup_low": (0, 9999), "sup_side": (0, 2)}
        st = {"minimized": False, "shutting": False, "docked": False, "next_supply": 0.0, "counts": {},
              "next_save": 0.0, "queue": []}
        win = {"g": None, "c": {}, "store": ({}, {})}; supplies = set(SUPPLY_DEFAULT)
        sup = {"g": None, "c": {}, "rows": (), "at": None, "slot": None, "drawn": None}; warn = {}
        page = {"next_warn": 0.0}; _get, _put = Kit.get_var, Kit.put_var
        cleanup, queue, say = Kit.basics(st, TITLE)
        def read_pairs(key): Kit.kv_load(key, ",", settings, NUMBERS)
        def load_settings(): read_pairs(SET_KEY if _get(SET_KEY, "") else OLD_SETTINGS_KEY)
        def save_settings(): Kit.kv_save(SET_KEY, ",", settings, sorted(settings), NUMBERS)
        def load_supplies():
            raw = _get(SUPPLIES_KEY, "-")
            if raw == "-": return
            known = set(r[0] for r in SUPPLY_ITEMS); supplies.clear()
            supplies.update(k for k in raw.split(",") if k in known)
        def save_supplies(): _put(SUPPLIES_KEY, ",".join(r[0] for r in SUPPLY_ITEMS if r[0] in supplies) or "none")
        def load_warn():
            warn.clear(); known = set(r[0] for r in SUPPLY_ITEMS)
            for part in _get(SUPWARN_KEY, "").split(","):
                if "=" not in part: continue
                k, v = part.split("=", 1)
                if k not in known: continue
                vals = []
                for txt in (v.split("/") + ["", ""])[:2]:
                    try: vals.append(max(0, min(WARN_MAX, int(txt))))
                    except ValueError: vals.append(None)
                if vals[0] is not None or vals[1] is not None: warn[k] = vals
        def save_warn():
            parts = []
            for r in SUPPLY_ITEMS:
                lw = warn.get(r[0])
                if lw: parts.append("%s=%s/%s" % (r[0], "" if lw[0] is None else lw[0], "" if lw[1] is None else lw[1]))
            _put(SUPWARN_KEY, ",".join(parts))
        def count_supplies():
            wanted = {}
            for key, _grp, _cap, graphic, hue in SUPPLY_ITEMS:
                if key in supplies: wanted.setdefault(graphic, []).append((key, hue))
            counts = dict((r[0], 0) for r in SUPPLY_ITEMS if r[0] in supplies)
            if not wanted: return counts
            for it in HOST.pack_items(bool(settings["sup_deep"]), PACK_AGE):
                try:
                    rows = wanted.get(int(it.Graphic or 0))
                    if not rows: continue
                    hue = int(it.Hue or 0) & 0x3FFF; amount = max(1, int(it.Amount or 1))
                except Exception: continue
                for key, want_hue in rows:
                    if want_hue is None or want_hue == hue: counts[key] += amount
            return counts
        def supply_rows():
            return tuple((key, grp, cap) for key, grp, cap, _gr, _h in SUPPLY_ITEMS
                         if key in supplies and not (settings["sup_hide0"] and not st["counts"].get(key, 0)))
        def supply_text(key):
            n = st["counts"].get(key, 0); lw = warn.get(key)
            crit = lw[1] if lw is not None and lw[1] is not None else settings["sup_low"]
            if n <= crit: hue = Kit.HUE_BAD
            else: hue = HUE_LOW if lw is not None and lw[0] is not None and n <= lw[0] else Kit.HUE_TEXT
            return "{:,}".format(int(n)), hue
        def follows(): return bool(settings["sup_follow"]) and ANCHOR in HOST.services and not HOST.layout_holds(KEY)
        def table_slot(): return sup["slot"] if HOST.layout_holds(KEY) else None
        def table_plan(rows, pitch):
            groups = [(grp, [r for r in rows if r[1] == grp]) for grp in GROUPS if any(r[1] == grp for r in rows)]
            heights = [26 + len(grows) * pitch + 4 for _grp, grows in groups] or [26 + 2 * pitch + 4]
            return groups, heights, 16 + sum(heights) + Kit.GAP * (len(heights) - 1)
        def table_fit(w, h, mode):
            new = (int(w), int(h)) if (w is not None and h is not None) else None
            if new != sup["slot"] or mode == "again": sup["slot"] = new; sup["drawn"] = False
        def table_min(): return SUPPLY_W, table_plan(supply_rows(), SUPPLY_ROW_MIN)[2]
        def build_supplies(rows):
            old = sup["g"]; slot = table_slot(); held = HOST.layout_holds(KEY); follow = follows()
            pitch = Kit.pitch(SUPPLY_ROW)
            groups, heights, h = table_plan(rows, pitch); w = SUPPLY_W if slot is None else slot[0]
            if slot is not None:
                n = sum(len(grows) for _grp, grows in groups) or 2
                pitch = max(SUPPLY_ROW_MIN, min(2 * SUPPLY_ROW, pitch + (slot[1] - h) // n))
                groups, heights, h = table_plan(rows, pitch)
                if h < slot[1]: heights[-1] += slot[1] - h; h = slot[1]
            g = G.CreateGump(True, not follow and not HOST.layout_locked(KEY))
            Kit.add_window_frame(g, w, h, corners=False); c = {}; y = 8
            art = dict((key, (graphic, hue)) for key, _g, _c, graphic, hue in SUPPLY_ITEMS)
            if not groups:
                Kit.add_section(g, 8, y, w - 16, heights[0], "SUPPLIES")
                hint = "None of these in your pack." if supplies else "No rows ticked yet."
                Kit.add_label(g, hint, 18, y + 26, Kit.HUE_INFO)
                Kit.add_label(g, "Pick rows: its settings page.", 18, y + 26 + pitch, Kit.HUE_INFO)
            for (grp, grows), sh in zip(groups, heights):
                Kit.add_section(g, 8, y, w - 16, sh, grp)
                for i, (key, _grp, cap) in enumerate(grows):
                    ry = y + 26 + i * pitch
                    item_pic(g, art[key][0], art[key][1], 16, ry + (pitch - SUPPLY_ICON) // 2 - 1, SUPPLY_ICON)
                    text, hue = supply_text(key); ry += (pitch - SUPPLY_ROW) // 2
                    c[key] = Kit.add_label(g, text, w - 18 - Kit.text_w(text), ry + 2, hue)
                    Kit.add_label(g, Kit.fit(cap, w - 18 - SUPPLY_ICON - 4 - 18 - 6 - 44), 18 + SUPPLY_ICON + 4, ry + 2)
                y += sh + Kit.GAP
            at = None
            if held: spot = HOST.layout_rect(KEY); x, y0 = (spot[0], spot[1]) if spot is not None else sup_pos()
            elif not follow:
                Kit.catcher(g, 0, 0, w, h, lambda: None, "Drag to move the supplies table", movable=True)
                x, y0 = sup_pos()
                if Kit.is_open(old): x, y0 = old.GetX(), old.GetY()
                Kit.place(g, x, y0, w, h)
            else: a = frame_anchor(w, h); at = a[1] if a is not None else sup_pos(); Kit.place(g, at[0], at[1], w, h)
            if not Kit.zone_up(KEY):
                Kit.art_button(g, ({}, {}), "close", Kit.ART_CLOSE, w - 8 - 30, 10, None, "Close the supplies list",
                               on_click=queue("close"))
            sup.update({"g": g, "c": c, "rows": rows, "at": at, "w": w, "h": h, "follow": follow, "leader": None,
                        "drawn": slot})
            if held: to_slot(KEY, g, Kit.show_window(g, x, y0, w, h, KEY, False, None, None))
            else: Kit.add_front(g)
            if not follow and not held: Kit.on_moved(g, save_sup_pos)
            Kit.dispose(old); place_supplies()
        SUP_DEFAULT_POS = (60, 620)
        def sup_pos():
            raw = _get(SUPPOS_KEY, ""); sup["saved"] = raw
            try: x, y = (int(v) for v in raw.split(",")); return Kit.adapt(x, y, sup.get("w", 0), sup.get("h", 0))
            except ValueError:
                a = frame_anchor(sup.get("w", SUPPLY_W), sup.get("h", 0))
                return a[1] if a is not None else SUP_DEFAULT_POS
        def save_sup_pos():
            g = sup["g"]
            if Kit.is_open(g) and not sup.get("follow", True) and not HOST.layout_holds(KEY):
                try: data = "%d,%d" % (int(g.GetX()), int(g.GetY()))
                except Exception: return
                if data != sup.get("saved"): sup["saved"] = data; _put(SUPPOS_KEY, data)
        def frame_anchor(w, h):
            fn = HOST.services.get(ANCHOR)
            if fn is None: return None
            try: return fn(w, h, settings["sup_side"])
            except Exception: return None
        def place_supplies():
            g = sup["g"]
            if not Kit.is_open(g) or not sup.get("follow", True): return
            a = frame_anchor(sup["w"], sup["h"])
            if a is None: return
            leader, at = a
            if sup.get("leader") is not leader: sup["leader"] = leader; Kit.attach(g, leader)
            if at != sup["at"]:
                sup["at"] = at
                try: Kit.place(g, at[0], at[1], sup["w"], sup["h"]); Kit.moved_by_code(g)
                except Exception: pass
        ROWS_W = 620; ROWS_POS_KEY = "UnitFrames_rowspos"; ROWS_KEY = "supplies_rows"
        def build_window():
            M, GAP = Kit.MARGIN, Kit.GAP; w = ROWS_W; IW = w - 2 * M
            longest = max(sum(1 for r in SUPPLY_ITEMS if r[1] == grp) for grp in GROUPS)
            h_list = 52 + longest * SUP_ROW + 4; h = M + 30 + GAP + h_list + M
            g, store, c = wnd.begin(w, h); Kit.add_window_frame(g, w, h)
            Kit.add_section(g, M, M, IW, 30); Kit.add_label(g, "SUPPLIES ROWS", M + 30, M + 7, Kit.HUE_TITLE)
            bx = w - M - 54 - 20 - 35 - Kit.text_w("Untick all")
            Kit.art_button(g, store, "none", Kit.ART_CLOSE, bx, M + 4, "Untick all", "Empty the table")
            bx -= 14 + 35 + Kit.text_w("Tick all")
            Kit.art_button(g, store, "all", Kit.ART_OK, bx, M + 4, "Tick all", "Show every row")
            Kit.catcher(g, M, M, bx - M - 6, 30, lambda: None, "Drag to move", movable=not HOST.layout_locked(ROWS_KEY))
            if not Kit.zone_up(ROWS_KEY):
                Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, "Close the rows list")
            yl = M + 30 + GAP; Kit.add_section(g, M, yl, IW, h_list, "ROWS  (ticked rows show in the table)")
            cw = (IW - 16) // len(GROUPS)
            for col, grp in enumerate(GROUPS):
                cx = M + 10 + col * cw; Kit.add_label(g, grp, cx, yl + 30, Kit.HUE_TITLE)
                for i, (key, _grp, cap, _gr, _h) in enumerate(r for r in SUPPLY_ITEMS if r[1] == grp):
                    c[key] = Kit.add_check(g, Kit.fit(cap, cw - 34), cx, yl + 52 + i * SUP_ROW, key in supplies)
            wnd.end(g, {"next_poll": 0.0})
        wnd = Kit.Window(ROWS_KEY, "Supplies Rows", st, win, build_window, ROWS_POS_KEY, default=(260, 160),
                         cleanup=cleanup, owner=False, clear={"c": {}})
        def refresh(now):
            if not settings["sup_open"]:
                if sup["g"] is not None: save_sup_pos(); g, sup["g"] = sup["g"], None; Kit.dispose(g)
                return
            recount = now >= st["next_supply"] or not st["counts"] or (now >= st.get("sup_min", 0.0)
                                                                         and HOST.pack_ver() != st.get("pack_v"))
            if recount:
                st.update({"next_supply": now + SUPPLY_EVERY, "sup_min": now + SUPPLY_SOON, "pack_v": HOST.pack_ver()})
                st["counts"] = count_supplies()
            if not Kit.is_open(sup["g"]) or sup.get("follow") != follows() or sup["drawn"] != table_slot():
                save_sup_pos(); build_supplies(supply_rows())
            elif recount:
                rows = supply_rows()
                if rows != sup["rows"]: save_sup_pos(); build_supplies(rows)
                else:
                    for key, _grp, _cap in rows:
                        text, hue = supply_text(key); lbl = sup["c"].get(key)
                        if lbl is not None and Kit.set_text(lbl, text, hue):
                            lbl.SetPos(sup["w"] - 18 - Kit.text_px(text), lbl.GetY())
                    place_supplies()
            else: place_supplies()
        def poll_rows_window(now):
            g = win["g"]
            if g is None: return
            if not Kit.is_open(g): win.update({"g": None, "c": {}}); return
            store, c = win["store"], win["c"]
            if Kit.was_clicked(store, "close"): wnd.close(); return
            poked = False
            for name, on in (("all", True), ("none", False)):
                if Kit.was_clicked(store, name):
                    poked = True
                    for cb in c.values(): cb.SetIsChecked(on)
            if not poked and not HOST.pass_poked and now < win.get("next_poll", 0.0): return
            win["next_poll"] = now + ROWS_POLL; ticked = set()
            for key, cb in c.items():
                try: on = bool(cb.IsChecked)
                except Exception: on = key in supplies
                if on: ticked.add(key)
            if ticked != supplies:
                supplies.clear(); supplies.update(ticked); save_supplies(); st["next_supply"] = 0.0
                HOST.refresh_settings(KEY)
        def open_now(now):
            if not settings["sup_open"]: settings["sup_open"] = True; save_settings(); st["next_supply"] = 0.0
            refresh(now); g = sup["g"]
            if Kit.is_open(g): safe(lambda: Kit.client_control(g).BringOnTop())
        def close_now(now): settings["sup_open"] = False; save_settings()
        ACTIONS = {"open": open_now, "close": close_now, "sup_rows": lambda now: build_window()}
        SUP_CHECKS = (("sup_follow", "The table sticks to the player frame", "Untick to drag it anywhere"),
                      ("sup_deep", "Count inside bags in your backpack", "Bags and pouches in your backpack count too"),
                      ("sup_hide0", "Hide rows you have none of", "Leave out rows at 0"))
        SUP_LOW_TIP = "A row at or below this shows red, unless it has its own Red below (0-%d)" % NUMBERS["sup_low"][1]
        SUP_ROW = 24; CFG_H = 118; WARN_LINE = 26; WARN_BOX = 44
        def warn_rows(): return [r for r in SUPPLY_ITEMS if r[0] in supplies]
        def warn_height(): return 30 + 20 + max(1, (len(warn_rows()) + 1) // 2) * WARN_LINE + 4
        def draw_warn(f, x, y):
            g, rows = f.g, warn_rows(); cw = (f.w - 36) // 2; boxes = []
            if not rows: Kit.add_label(g, "No rows ticked yet: click Choose rows above.", x + 12, y + 2, Kit.HUE_INFO)
            for col in range(2 if len(rows) > 1 else (1 if rows else 0)):
                bx = x + 12 + col * (cw + 12) + cw - 2 * WARN_BOX - 8
                Kit.add_label(g, "Yellow", bx, y - 2, Kit.HUE_TITLE)
                Kit.add_label(g, "Red", bx + WARN_BOX + 8, y - 2, Kit.HUE_BAD)
            for i, (key, _grp, cap, _gr, _h) in enumerate(rows):
                cx = x + 12 + (i % 2) * (cw + 12); ry = y + 20 + (i // 2) * WARN_LINE; bx = cx + cw - 2 * WARN_BOX - 8
                Kit.add_label(g, Kit.fit(cap, bx - cx - 8), cx, ry + 3); lw = warn.get(key) or (None, None)
                lb = Kit.with_tip(Kit.add_textbox(g, "" if lw[0] is None else str(lw[0]), bx, ry, WARN_BOX),
                                  "Yellow at or below this many %s (empty: never)" % cap)
                cb = Kit.with_tip(Kit.add_textbox(g, "" if lw[1] is None else str(lw[1]), bx + WARN_BOX + 8, ry,
                                                  WARN_BOX), "Red at or below this many %s (empty: Red at or below "
                                  "above)" % cap)
                boxes.append((key, lb, cb))
            f.c["warn"] = boxes
        def page_table(w):
            return (("TABLE", (("check",) + SUP_CHECKS[0] + ({"stay": True},),
                               ("check",) + SUP_CHECKS[1] + ({"dx": 12 + w // 2},), ("check",) + SUP_CHECKS[2],
                               ("num", "sup_low", "Red at or below:", SUP_LOW_TIP, None) + NUMBERS["sup_low"]
                               + ({"ldy": 4, "lgap": 12, "fw": 60, "stay": True},),
                               ("note", "Opens:", {"dx": 12 + w // 2, "ndy": 4, "hue": None, "stay": True}),
                               ("buttons", (("sup_rows", Kit.ART_PAGE, "Choose rows", "Pick the rows the table shows "
                                             "(%d of %d ticked)" % (len(supplies), len(SUPPLY_ITEMS))),),
                                {"dx": w - 45 - Kit.text_w("Choose rows"), "bdy": -78})),
                     {"sh": CFG_H, "top": 30, "ch": 26}),
                    ("SUPPLY WARNINGS  (yellow and red counts, per row)", (("custom", 0, draw_warn),),
                     {"sh": warn_height()}))
        def page_clicks(f):
            if Kit.was_clicked(f.store, "sup_rows"): queue("sup_rows")()
            if f.c.get("warn") and time.time() >= page["next_warn"]:
                page["next_warn"] = time.time() + WARN_READ_EVERY
                if read_warn_boxes(f.c): st["next_supply"] = 0.0
        def read_side(f, new):
            dd = f.c.get("sup_side")
            if dd is None: return
            side = Kit.dd_index(dd, -1)
            if 0 <= side < len(SUPPLY_SIDES): new["sup_side"] = side
        def on_change(old, new): st["next_supply"] = 0.0; sup["at"] = None
        cfg = Kit.Page(settings, page_table, save_settings, on_change, adjust=read_side, clicks=page_clicks)
        def build_config(g, x, y, w):
            f = cfg.build(g, x, y, w); dx = x + 24 + (w // 2) + Kit.text_w("Opens:"); page["next_warn"] = 0.0
            try:
                dd = G.CreateDropDown(150, list(SUPPLY_SIDES), int(settings["sup_side"])); dd.SetPos(dx, y + 82)
                g.Add(dd)
                f.c["sup_side"] = Kit.with_tip(dd, "Side of the player frame the table opens on (flips when there "
                                               "is no room)")
            except Exception:
                f.c["sup_side"] = None; Kit.add_label(g, SUPPLY_SIDES[settings["sup_side"]], dx, y + 86, Kit.HUE_INFO)
        def read_warn_boxes(c):
            changed = False
            for key, lb, cb in c.get("warn") or ():
                old = warn.get(key) or [None, None]; new = list(old)
                for i, box in ((0, lb), (1, cb)):
                    try:
                        if box.IsDisposed: continue
                        txt = str(box.Text or "").strip()
                    except Exception: continue
                    if not txt: new[i] = None
                    else:
                        try: new[i] = max(0, min(WARN_MAX, int(txt)))
                        except ValueError: pass
                if new != list(old):
                    if new[0] is None and new[1] is None: warn.pop(key, None)
                    else: warn[key] = new
                    changed = True
            if changed: save_warn()
            return changed
        def config_closed():
            f = cfg.f
            if f is not None and f.c.get("warn") and read_warn_boxes(f.c): st["next_supply"] = 0.0
            cfg.closed()
        def open_table(): queue("open")()
        def _start():
            st.update({"next_supply": 0.0, "counts": {}, "next_save": 0.0, "queue": []}); sup["saved"] = None
            load_settings(); load_supplies(); load_warn(); cleanup.service("supplies.open", open_table); wnd.dock()
            HOST.dock_add(KEY, {"title": TITLE, "state": lambda: "open" if Kit.is_open(sup["g"]) else None,
                                "show": open_table, "gump": lambda: sup["g"], "fit": table_fit, "min": table_min,
                                "untitled": True, "redraw": lambda: sup.update(drawn=False)})
            cleanup.add(HOST.dock_remove, KEY)
        def _tick():
            now = time.time()
            while st["queue"]:
                action = st["queue"].pop(0)
                if wnd.action(action): continue
                fn = ACTIONS.get(action)
                if fn is not None: fn(now)
            poll_rows_window(now); refresh(now)
            if now >= st["next_save"]: st["next_save"] = now + SAVE_EVERY; save_sup_pos()
        load_settings(); load_supplies(); load_warn()
        def _stop():
            save_settings(); save_supplies(); save_sup_pos(); g, sup["g"] = sup["g"], None; Kit.dispose(g)
            cleanup.close()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                  "build_config": build_config, "poll_config": cfg.poll, "config_closed": config_closed}
    def _part_sections():
        KEY = "inventory.sections"; TITLE = "Bag Sections"; SETTINGS_KEY = "UnifiedBag_sections"
        POS_KEY = "UnifiedBag_sections_pos"; MIN_KEY = "UnifiedBag_sections_min"; W = 330; MINI = (260, 46)
        TRAY_ICON = 0x0E75; CELL_W = 46; CELL_H = 54; PIC = 36; HEAD = 30; SEC_PAD = 6; EVERY = 2.0; AFTER_USE = 0.5
        MIN_GAP = 0.25; REBUILD_GAP = 1.0
        MAX_SECTIONS = 12; CELL_CAP = 240; NAME_MAX = 24; PICK_TIMEOUT = 15
        DEFAULT_ON = ("reagents", "potions", "bandages", "gold", "scrolls", "maps"); settings = {"other": True}
        settings.update(("p_" + k, k in DEFAULT_ON) for k, _c in PRESETS); DEFAULTS = dict(settings)
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "groups": [], "sig": None,
              "ver": -1, "at": 0.0, "kinds": 0, "loaded": False, "built": 0.0, "due": 0.0}
        win = {"g": None, "c": {}, "store": ({}, {}), "cells": []}; cleanup, queue, say = Kit.basics(st, TITLE)
        customs = []
        def ticked(vals): return sum(1 for k, _c in PRESETS if vals["p_" + k])
        def load_settings():
            raw = str(Kit.get_var(SETTINGS_KEY, "") or ""); settings.update(DEFAULTS); del customs[:]
            st["loaded"] = True
            if not raw: return
            for k, _c in PRESETS: settings["p_" + k] = False
            for tok in raw.split(";"):
                if tok in ("other", "-other"): settings["other"] = tok == "other"
                elif tok.startswith("c~"):
                    p = tok.split("~", 2)
                    try: gr = int(p[1], 16)
                    except (IndexError, ValueError): continue
                    if (len(p) > 2 and 0 < gr <= 0xFFFF and len(customs) < MAX_SECTIONS
                            and all(cu[0] != gr for cu in customs)):
                        customs.append((gr, clip(p[2], NAME_MAX) or "Item"))
                elif ("p_" + tok) in settings: settings["p_" + tok] = True
            for k, _c in reversed(PRESETS):
                if len(customs) + ticked(settings) <= MAX_SECTIONS: break
                settings["p_" + k] = False
        def save_settings():
            toks = ["c~%04X~%s" % cu for cu in customs] + [k for k, _c in PRESETS if settings["p_" + k]]
            Kit.put_var(SETTINGS_KEY, ";".join(toks + ["other" if settings["other"] else "-other"]))
        def item_label(it, gr):
            try: name = re.sub(r"^[\d,]+\s+", "", str(it.Name or "").strip())
            except Exception: name = ""
            name = re.sub(r"[;~|]", " ", name).strip()
            return name[:1].upper() + name[1:] if name else "Item 0x%04X" % gr
        def amount_text(n): return commas(n) if n < 10000 else "%dk" % (n // 1000)
        def cols_for(w): return max(1, (w - 2 * Kit.MARGIN - 16) // CELL_W)
        def group_h(n, cols): return HEAD + max(1, (n + cols - 1) // cols) * CELL_H + SEC_PAD
        def fixed_h(): return 2 * Kit.MARGIN + 30 + Kit.GAP
        def min_size(): return 2 * Kit.MARGIN + 16 + 3 * CELL_W, fixed_h() + HEAD + CELL_H + SEC_PAD
        def empty_text(): return "Reading item kinds." if cats["data"] is None else "Nothing to show."
        def use_cell(i):
            def handler(*args):
                cells = win["cells"]
                if i < len(cells) and cells[i]["serial"]: queue(("use", cells[i]["serial"]))()
            return handler
        def build_window():
            z = wnd.zone_slot(*min_size()); w = z[0] if z else W; cols = cols_for(w); groups = st["groups"]
            body = sum(group_h(len(cl), cols) + Kit.GAP for _t, cl in groups) - Kit.GAP if groups else HEAD + 20
            h = z[1] if z else fixed_h() + body
            g, store, c = wnd.begin(w, h); cells = []
            if not st["minimized"]:
                wnd.frame(g); M = Kit.MARGIN; IW = w - 2 * M; y = M + 30 + Kit.GAP; bottom = h - M
                if not groups:
                    Kit.add_section(g, M, y, IW, bottom - y)
                    c["empty"] = Kit.add_label(g, empty_text(), M + 12, y + 10, Kit.HUE_INFO)
                for gi, (title, cl) in enumerate(groups):
                    rows = max(1, (len(cl) + cols - 1) // cols)
                    if z: rows = min(rows, (bottom - y - HEAD - SEC_PAD) // CELL_H)
                    if rows < 1: break
                    gh = HEAD + rows * CELL_H + SEC_PAD
                    Kit.add_section(g, M, y, IW, gh, "%s  (%d)" % (title.upper(), len(cl)))
                    for ci, (key, v) in enumerate(cl[:rows * cols]):
                        cx = M + 8 + (ci % cols) * CELL_W; cy = y + HEAD + (ci // cols) * CELL_H
                        pic = G.CreateGumpItemPic(key[0], PIC, PIC); pic.SetRect(cx + (CELL_W - PIC) // 2, cy, PIC, PIC)
                        if key[1]: pic.Hue = key[1]
                        pic.DrawBorder = False; Kit.with_tip(pic, v[0] + ": double-click to use one")
                        Kit.hook_double(pic, use_cell(len(cells)))
                        g.Add(pic); text = amount_text(v[1]); ty = cy + PIC + 1
                        amt = Kit.add_label(g, text, cx + (CELL_W - Kit.text_w(text)) // 2, ty, Kit.HUE_TEXT)
                        cells.append({"gi": gi, "ci": ci, "serial": v[2], "amt": amt, "x": cx, "y": ty})
                    y += gh + Kit.GAP
            wnd.end(g, {"cells": cells}); refresh()
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, (W, 300), MINI, TRAY_ICON, cleanup,
                         clear={"cells": []})
        def refresh():
            c = win["c"]; groups = st["groups"]
            if "status" in c: Kit.set_text(c["status"], "%s: %s" % (TITLE, Kit.count(st["kinds"], "kind"))); return
            if "empty" in c: Kit.set_text(c["empty"], empty_text())
            for cell in win["cells"]:
                try: v = groups[cell["gi"]][1][cell["ci"]][1]
                except IndexError: continue
                cell["serial"] = v[2]; text = amount_text(v[1])
                if Kit.set_text(cell["amt"], text):
                    cell["amt"].SetPos(cell["x"] + (CELL_W - Kit.text_w(text)) // 2, cell["y"])
        def rules():
            data = cats["data"] or {}; out = [(nm, frozenset((gr,))) for gr, nm in customs]
            return out + [(cap, data.get(k, frozenset())) for k, cap in PRESETS if settings["p_" + k]]
        def by_name(kv): return kv[1][0].lower(), kv[0]
        def gather():
            rs = rules(); n_rs = len(rs); found = [{} for _i in range(n_rs + 1)]; n = 0; other = settings["other"]
            for it in HOST.pack_items():
                try: gr, hue, amt, serial = int(it.Graphic), int(it.Hue), max(1, int(it.Amount or 1)), int(it.Serial)
                except Exception: continue
                at = n_rs
                for i, (_nm, gs) in enumerate(rs):
                    if gr in gs: at = i; break
                if at == n_rs and not other: continue
                cell = found[at].get((gr, hue))
                if cell is not None: cell[1] += amt
                elif n < CELL_CAP: n += 1; found[at][(gr, hue)] = [item_label(it, gr), amt, serial]
            names = [nm for nm, _gs in rs] + ["Other"]
            return [(names[i], sorted(f.items(), key=by_name)) for i, f in enumerate(found) if f]
        def walk(now, burst=False):
            st["ver"], st["at"], st["due"] = HOST.pack_ver(), now, 0.0; groups = gather()
            sig = tuple((t, tuple(k for k, _v in cl)) for t, cl in groups)
            if burst and sig != st["sig"] and 0.0 <= now - st["built"] < REBUILD_GAP:
                st["due"] = st["built"] + REBUILD_GAP; return
            st["groups"] = groups; st["kinds"] = sum(len(cl) for _t, cl in groups)
            if st["minimized"]: st["sig"] = sig; refresh()
            elif sig != st["sig"]: st["sig"], st["built"] = sig, now; build_window()
            else: refresh()
        def use_item(action):
            serial = action[1]
            if not Kit.in_pack(serial): say("that is no longer in your backpack.", Kit.HUE_BAD); return
            Kit.once(lambda: API.UseObject(serial), (KEY, serial))(); st["at"] = time.time() - EVERY + AFTER_USE
        def full():
            if len(customs) + ticked(settings) < MAX_SECTIONS: return False
            say("%d sections at most." % MAX_SECTIONS, Kit.HUE_BAD); return True
        def ask_add(action):
            if full(): return
            say("target an item for its own section.")
            def done(serial): queue(("picked", int(serial or 0)))()
            HOST.pick_target(PICK_TIMEOUT, done, KEY)
        def picked(action):
            serial = action[1]; it = API.FindItem(serial) if serial else None
            if it is None: return
            gr = int(it.Graphic); name = clip(item_label(it, gr), NAME_MAX)
            if any(cu[0] == gr for cu in customs): say("%s already has a section." % name, Kit.HUE_BAD); return
            if full(): return
            customs.append((gr, name)); save_settings(); st["at"] = 0.0; HOST.refresh_settings(KEY)
            say("added a section for %s." % name, Kit.HUE_GOOD)
        def remove(action):
            if 0 <= action[1] < len(customs):
                customs.pop(action[1]); save_settings(); st["at"] = 0.0; HOST.refresh_settings(KEY)
        ACTIONS = {"use": use_item, "add": ask_add, "picked": picked, "remove": remove}
        def page_table(w):
            half = (w - 24) // 2
            ticks = [("check", "p_" + k, cap, "A section for %s" % cap.lower(),
                      {"dx": 12 + (i % 2) * half, "stay": i % 2 == 0}) for i, (k, cap) in enumerate(PRESETS)]
            mine = []
            for i, (_gr, nm) in enumerate(customs):
                mine += [("note", Kit.fit(nm, w - 80 - Kit.text_w("Remove")),
                          {"stay": True, "ndy": 4, "hue": Kit.HUE_TEXT}),
                         ("buttons", (("rm%d" % i, Kit.ART_CLOSE, "Remove", "Remove the %s section" % nm),),
                          {"dx": w - 48 - Kit.text_w("Remove")})]
            if not mine: mine = [("note", "None yet: add one from a target.")]
            return (("SECTIONS  (%d at most, in this order)" % MAX_SECTIONS,
                     ticks + [("check", "other", "Show Other", "Everything the sections leave, in a last section")]),
                    ("YOUR SECTIONS  (checked first)", mine + [("buttons", (("add", Kit.ART_PLAY, "Add from target...",
                                      "Target an item for a section of its own"),))]))
        def on_change(old, new): st["at"] = 0.0
        def cap_ticks(f, new):
            over = len(customs) + ticked(new) - MAX_SECTIONS; cut = False
            for k, _c in reversed(PRESETS):
                if over <= 0: break
                if new["p_" + k] and not settings["p_" + k]:
                    new["p_" + k] = False; over -= 1; cut = True; Kit.set(f.c["p_" + k], "IsChecked", False)
            if cut: say("%d sections at most." % MAX_SECTIONS, Kit.HUE_BAD)
        def page_clicks(f):
            if Kit.was_clicked(f.store, "add"): queue("add")()
            for i in range(len(customs)):
                if Kit.was_clicked(f.store, "rm%d" % i): queue(("remove", i))(); break
        cfg = Kit.Page(settings, page_table, save_settings, on_change, adjust=cap_ticks, clicks=page_clicks)
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "groups": [], "sig": None, "ver": -1, "at": 0.0,
                       "kinds": 0, "loaded": False, "minimized": wnd.start_min(), "built": 0.0, "due": 0.0})
            load_settings(); build_window(); wnd.dock(fit=True, min=min_size)
        def _tick():
            q = st["queue"]
            while q:
                action = q.pop(0)
                if not wnd.action(action): ACTIONS[action[0] if isinstance(action, tuple) else action](action)
            if win["g"] is None or Kit.closed(win) or st["docked"] or cats["data"] is None: return
            now = time.time(); age = now - st["at"]
            if not 0.0 <= age < EVERY or 0.0 < st["due"] <= now: walk(now)
            elif age >= MIN_GAP and HOST.pack_ver() != st["ver"]: walk(now, True)
        def _thread_tick():
            if cats["data"] is not None: return
            try: field = tile_field()
            except Exception: field = None
            try: build_cats(field)
            except Exception: cats["data"] = {}
        def _thread_wanted(): return cats["data"] is None and not st["shutting"]
        def _stop():
            st["shutting"] = True
            if st["loaded"]: save_settings()
            cleanup.close()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed,
                "thread_tick": _thread_tick, "thread_wanted": _thread_wanted}
    PARTS = (("bags", _part_bags, 0.1, "bag"), ("paperdoll", _part_paperdoll, 0.1, "character"),
        ("storage", _part_storage, 0.1, "storage"), ("restock", _part_restock, 0.1, "restock"),
        ("supplies", _part_supplies, 0.1, "supplies"), ("sections", _part_sections, 0.1))
    return PartSet(KEY, TITLE, PARTS).hooks()


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("inventory", "Inventory", "Bags, paperdoll, storage, restock, supplies",
         _module_inventory, 0.1, category="Your things", parts=(("bags", "Bags",
              "All your bags in one grid", True, ("bag",)), ("paperdoll", "Paperdoll",
              "What you wear, and your stats", True, ("character",)),
             ("storage", "Storage", "What the containers you opened hold", False, ("storage",)), ("restock", "Restock",
              "Refills from a chest or bank, on a press", False, ("restock",)),
             ("supplies", "Supplies", "Pack supplies, low counts marked", True, (), True),
             ("sections", "Bag Sections", "What you carry, grouped by kind", False, (), True),),
         aliases=('Character', 'Unified Bag', 'Storage Index', 'Restock', 'paperdoll', 'bank',
                  'chest', 'find', 'sort', 'supplies', 'supplies table', 'sections'))
