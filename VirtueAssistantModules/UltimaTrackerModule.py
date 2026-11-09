def _module_ultima():
    KEY = "ultima"; TITLE = "Ultima Tracker"; NPC_TITLE_RE = re.compile(r"\bthe\s+[a-z]", re.IGNORECASE)
    NOTO_WORD = {"murderer": "red", "criminal": "grey", "gray": "grey", "enemy": "orange",
                 "innocent": "blue", "ally": "green", "invulnerable": "yellow"}
    NOTO_HUE = {"murderer": 0x0022, "criminal": 0x03B2, "gray": 0x03B2, "enemy": 0x0090,
                "innocent": 0x0059, "ally": 0x003F, "invulnerable": 0x0035}
    def _part_tracker():
        KEY = "ultima"; TITLE = "Ultima Tracker"; OWN_PREFIX = TITLE + ":"
        TICK_SECONDS             = 0.25; COMBAT_TICK_SECONDS      = 0.15; HP_EVERY = 0.05
        DOUBLE_CLICK_SECONDS     = 0.45
        NPC_RECHECK_SECONDS      = 3.0; DEFAULT_SCALE   = 100; DEFAULT_OPACITY = 85; DEFAULT_RANGE   = 18
        DEFAULT_SYNC    = False; SCALE_MIN, SCALE_MAX = 50, 200; RANGE_MIN, RANGE_MAX = 1, 24; ROW_H      = 32
        MIN_W      = 210; MIN_H      = 90; POP_W      = 200; POP_BTN_W  = 18; NPC_BTN_W  = 12; SCROLLBAR  = 14
        SAVE_EVERY = 8; BASE_WIDTH     = 220; BASE_ROW_H     = 16; BASE_FONT      = 11; CB_MIN_WIDTH   = 170
        CB_MAX_WIDTH   = 600; CB_ROW_GAP     = 1; CB_FOOTER_H    = 10; SPELL_POISON   = "Poison"
        SPELL_PARALYZE = "Paralyze"; SPELL_HEAL, SPELL_GREATER_HEAL = "Heal", "Greater Heal"
        SPELL_CURE, SPELL_ARCH_CURE    = "Cure", "Arch Cure"; CAST_TIMEOUT   = 5.0; COMBAT_RANGE   = 12
        MAX_RANGE      = 18; IDLE_TIMEOUT   = 20.0; MAX_BARS       = 12; DEFAULT_COMBAT_ONLY       = True
        MELEE_RANGE               = 2; NEVER_SHOW_NOTO           = ("invulnerable",)
        FRIENDLY_NOTO             = ("innocent", "ally")
        HOSTILE_NOTO = [API.Notoriety.Gray, API.Notoriety.Criminal, API.Notoriety.Enemy, API.Notoriety.Murderer]
        ALERT_KEY        = "ultima.foe"; ALERT_SOUND      = 0x2E7; DEFAULT_ALERT_MINUTES = 5
        ALERT_MIN, ALERT_MAX = 1, 60; SIGHT_CAP        = 2000; SIGHT_SLACK      = 200; SIGHT_GONE       = 60.0
        SIGHT_SAVE_SECONDS = 30.0; SIGHT_ROWS       = 12; SIGHT_REFRESH    = 30.0; SIGHT_TRAY_ICON  = 0x14F5
        KILLER_BACK      = 60.0; KILLER_SHOW      = 60.0; KILLER_ROWS      = 6; ATTACKERS_CAP    = 40
        SEEN_REFRESH     = 30.0; NOTE_MAX         = 160
        FACETS = {0: "Fel", 1: "Tram", 2: "Ilsh", 3: "Malas", 4: "Tok", 5: "TerM"}
        SIGHT_NOTO_FILTERS = (("All players", None), ("Red only", ("murderer",)),
                              ("Grey only", ("gray", "criminal")), ("Orange only", ("enemy",)),
                              ("Blue only", ("innocent",)), ("Foe list", "foe"))
        SIGHT_TIME_FILTERS = (("Last hour", 3600.0), ("Today", "today"), ("All time", None))
        SIGHT_POS_KEY    = "UltimaTracker_sight_pos"; SIGHT_MIN_KEY    = "UltimaTracker_sight_min"
        SIGHT_OPEN_KEY   = "UltimaTracker_sight_open"; KILLER_POS_KEY   = "UltimaTracker_killer_pos"
        KILLER_MIN_KEY   = "UltimaTracker_killer_min"; TITLE_DBL_SECONDS = 0.5; TITLE_JITTER   = 6
        FIXED_WINDOWS  = ("friend", "foe", "neutral", "combat", "panel"); ANCHOR_SETTLE_POLLS = 4
        ANCHOR_LINGER_POLLS = 10; CACHE_CAP      = 2000; PLAYER_NAMES_CAP  = 5000; PLAYER_NAMES_KEEP = 4000
        LABELS_CAP     = 4000; PAGE_SAVE_DELAY = 1.0
        BORDER       = 6; TITLE_H      = 24; TITLE_FONT   = 13; OPACITY_ROW_H = 20
        BTN_FACE     = "#3A3A3A"; BTN_FACE_ON  = "#5E4E24"; ICON_COLOR   = "#DDDDDD"; LOCK_ON      = "#F0C850"
        LOCK_OFF     = "#A8A8A8"; TEXT_COLOR   = "#DDDDDD"; DIM_TEXT     = "#999999"; GRIP_COLOR   = "#7D6E52"
        TITLES = {"friend": "Friends", "foe": "Foes", "neutral": "Neutral", "combat": "Combat"}
        TITLE_COLOR = {"friend": "#5CE65C", "foe": "#FF5050", "neutral": "#9EC8FF",
                       "combat": "#FFB050", "panel": "#FFD966"}
        BAR_FG = {"friend": "#3AA0D4", "foe": "#D93030", "neutral": "#B8B8B8", "combat": "#B32D2D"}
        COL_POISON = "#2E9E3A"; GLOW_COLOR = "#FF2020"; GLOW_HP_PCT = 50; GLOW_PERIOD = 1.2
        GLOW_MIN, GLOW_MAX = 0.10, 0.55; GLOW_STEPS = 32; GLOW_EVERY = 0.1; COL_HEAL   = "#B8902A"
        COL_CURE   = "#2A8C9E"; COL_BANDAGE = "#D8CCB0"; BANDAGE_GRAPHIC   = 0x0E21; BANDAGE_RANGE     = 1
        BANDAGE_CURSOR_WAIT = 3.0; BANDAGE_CLAIM     = 3.5; COL_PARA   = "#3A6FD8"; COL_BOTH   = "#21A39A"
        COL_DEAD   = "#555555"
        NOTO_COLOR = {"innocent": "#4FA3FF", "ally": "#40E040", "gray": "#B0B0B0",
            "criminal": "#B0B0B0", "enemy": "#FF9A2E", "murderer": "#FF4040",
            "invulnerable": "#FFE14D", "unknown": "#DDDDDD",}
        UO_FONT_MIN, UO_FONT_MAX = 10, 18; FRAME_GUMP    = Kit.WINDOW_BG
        SECTION_GUMP  = Kit.SECTION_TILE; HEADER_GUMP   = Kit.SECTION_TILE; DIVIDER_H     = 3
        BUTTON_GUMP   = Kit.STONE_TILE; LOCK_GUMP     = 0x082C; LOCK_OFF_ALPHA = 0.6
        MIN_GUMPS     = (Kit.ART_MIN[0], Kit.ART_RESTORE[0]); OPACITY_GUMPS = (0x0837, 0x0838)
        HUE_TEXT     = 0x0481; HUE_LOCKED   = 34
        HUE_PARA_BAR = 0x0480
        FACE_HUE = {BTN_FACE: 0, BTN_FACE_ON: 0x0035, COL_HEAL: 0x0035, COL_CURE: 0x0059,
                    COL_BANDAGE: 0, COL_POISON: 0x003F, COL_PARA: HUE_PARA_BAR}
        HUE_PALETTE = [((235, 235, 235), 0x0481), ((150, 150, 150), 0x03B2),
                       ((225, 55, 55), 0x0022), ((70, 220, 70), 0x003F),
                       ((90, 150, 255), 0x0059), ((255, 155, 45), 0x0090), ((255, 220, 80), 0x0035), ((25, 25, 25), 0)]
        DATA_FILE = Kit.data_path("_ultima_tracker_data.txt")
        OLD_DATA_FILE = os.path.join(Kit.script_dir(), "_player_tracker_data.txt"); CATS = ["friend", "foe", "neutral"]
        INT_SETTINGS = {"scale": (SCALE_MIN, SCALE_MAX), "opacity": (0, 100), "range": (RANGE_MIN, RANGE_MAX),
                        "alert_minutes": (ALERT_MIN, ALERT_MAX)}
        INT_ORDER = ("scale", "opacity", "range", "alert_minutes")
        BOOL_SETTINGS = ("sync", "magery", "combat_shown", "combat_only", "healing", "borders",
                         "alert_red", "alert_foes", "alert_orange", "alert_gray", "sightings", "killer")
        DEFAULT_LAYOUT = {"friend":  [40, 140, 240, 220, False, False, DEFAULT_OPACITY],
            "foe":     [290, 140, 240, 220, False, False, DEFAULT_OPACITY],
            "neutral": [540, 140, 240, 220, False, False, DEFAULT_OPACITY],
            "combat":  [300, 200, BASE_WIDTH, 0, False, False, DEFAULT_OPACITY],
            "panel":   [40, 380, 0, 0, False, False, DEFAULT_OPACITY],}
        FOES = {}; IGNORE = {}; LAYOUT = {k: list(v) for k, v in DEFAULT_LAYOUT.items()}
        settings = {"scale": DEFAULT_SCALE, "opacity": DEFAULT_OPACITY, "range": DEFAULT_RANGE,
                       "sync": DEFAULT_SYNC, "magery": False, "combat_shown": True,
                       "combat_only": DEFAULT_COMBAT_ONLY, "healing": False, "borders": True,
                       "alert_red": True, "alert_foes": True, "alert_orange": False,
                       "alert_gray": False, "alert_minutes": DEFAULT_ALERT_MINUTES, "sightings": True, "killer": True}
        DEFAULTS = dict(settings)
        STATE_DEFAULTS = {"dirty_save": False, "foe_ver": 0, "combat_loaded": False, "shutting": False,
                          "started": False, "loaded": False}
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "dirty_save": False, "foe_ver": 0,
              "combat_loaded": False, "started": False, "loaded": False, "party": set()}
        win = {"g": None, "c": {}, "store": ({}, {})}
        cleanup = Kit.Cleanup(); queue = Kit.queuer(st); say = Kit.sayer(TITLE)
        POPS = {}; DOCK_REQ = []; SETTINGS_REQ = []
        KIT_HEAD = Kit.MARGIN + 30 + Kit.GAP; KIT_MINI_H = 2 * Kit.MARGIN + 30
        def settings_click(*args): SETTINGS_REQ.append(True)
        LAST_CLICK = {}; NATIVE = {}; SIGHTS = []; LAST_SEEN = {}; ALT_OF = {}
        SIGHT = {"ver": 0, "seen_ver": 0, "dirty": False, "save_at": 0.0}; PRESENT = {}; ALERTED = {}; FOE_SERIALS = {}
        ALERT_PREV = set(); ATTACKERS = {}; LINK_PICK = [None]
        def sc(v, scale=None):
            s = settings["scale"] if scale is None else scale; return max(1, int(round(v * s / 100.0)))
        TEXT_FIT_MAX = 13; EMPTY_PITCH = 20
        def text_scale(s): return s if s > 1.0 else 1.0
        def tsc(v): return sc(v) if settings["scale"] > 100 else int(v)
        def empty_lines(text, width):
            width = max(20, int(width)); return [Kit.fit(ln, width) for ln in Kit.wrap(text, width)]
        def add_empty(parent, lines, x, y):
            hue = hue_of(DIM_TEXT)
            return [inert(Kit.add_label(parent, ln, x, y + i * EMPTY_PITCH, hue)) for i, ln in enumerate(lines)]
        FIT = {"req": False, "size": {}, "own_size": {}, "force": set(), "made": {}}; FIT_TRIES = 3
        def reset_layout():
            for k, v in DEFAULT_LAYOUT.items(): LAYOUT[k] = list(v)
        def reset_settings():
            ANCHORS.clear(); settings.update(DEFAULTS); FIT["req"] = False; BANDAGE["serial"] = None; reset_layout()
        def clamp(v, lo, hi): return max(lo, min(hi, v))
        def stopping(): return API.StopRequested
        TITLE_PREFIXES = ("lord ", "lady ")
        def name_key(name):
            n = (name or "").strip().lower()
            for p in TITLE_PREFIXES:
                if n.startswith(p): n = n[len(p):]
            return n
        def short(text, n): return text if len(text) <= n else text[:max(1, n - 2)] + ".."
        def inert(c): c.SetAcceptMouseInput(False); return c
        def ttf(text, size, color, **kw): return inert(API.Gumps.CreateGumpTTFLabel(text, size, color, **kw))
        def box(opacity, color): return inert(API.Gumps.CreateGumpColorBox(opacity, color))
        def set_box_alpha(b, a):
            try: b.SetAlpha(a)
            except Exception: pass
        def drop(c): LABELS.pop(id(c), None); Kit.dispose(c)
        CLICK_Q = []; CLICK_GRACE = 0.15; CLICK_MODS = {}
        class RowClick(object):
            __slots__ = ("row", "make")
            def __init__(self, row, make): self.row, self.make = row, make
            def bind(self):
                r = self.row; serial, name = r.serial, r.name; prev = r.prev
                if prev is not None and time.time() - prev[2] < CLICK_GRACE: serial, name = prev[0], prev[1]
                if serial is None: return None
                return self.make(serial, name)
        def mods_now(): return {"alt": Follow.alt_held(), "shift": bool(Client.key_held("shift"))}
        def queue_click(fn):
            def queued(*args):
                f = fn.bind() if type(fn) is RowClick else fn
                if f is not None: CLICK_Q.append((f, mods_now()))
            return queued
        def on_click(c, fn): Kit.on_click(c, queue_click(fn))
        def run_clicks():
            while CLICK_Q:
                fn, mods = CLICK_Q.pop(0); CLICK_MODS.clear(); CLICK_MODS.update(mods)
                try: fn()
                except Exception as ex:
                    if HOST.stopping(): return
                    report_error(ex)
                finally: CLICK_MODS.clear()
        def report_error(ex):
            msg = str(ex)
            if msg not in M["errors"]:
                M["errors"].add(msg); say("error (still running): " + msg, Kit.HUE_BAD)
        SAVE_REQ = [False]; THREAD_JOBS = []; TICK_JOBS = []
        def run_jobs(q):
            while q:
                fn = q.pop(0)
                try: fn()
                except Exception as ex:
                    if HOST.stopping(): return True
                    report_error(ex)
        def catcher(x, y, w, h, fn, tip=None):
            c = API.Gumps.CreateGumpColorBox(0.01, "#000000"); c.SetRect(x, y, w, h); on_click(c, fn)
            return Kit.with_tip(c, tip)
        def pic(graphic, x=0, y=0, hue=0):
            return inert(API.Gumps.CreateGumpPic(graphic, x, y, Kit.look_hue(graphic, hue)))
        def tiled(graphic, w, h, hue=0):
            return inert(API.Gumps.CreateTiledGumpPic(graphic, max(0, w), max(0, h), Kit.look_hue(graphic, hue)))
        def init_native_art():
            NATIVE.clear(); icons = NATIVE["icons"] = {}
            for kind, graphics in (("lock", (LOCK_GUMP, LOCK_GUMP)), ("min", MIN_GUMPS), ("opacity", OPACITY_GUMPS)):
                sizes = [Kit.pic_size(g) for g in graphics]
                if all(w and h for w, h in sizes): icons[kind] = list(zip(graphics, sizes))
            sample = "Name the 75% PSN 12y Foes (3)"; lb = API.Gumps.CreateGumpLabel(sample, HUE_TEXT)
            w, h = int(lb.GetWidth()), int(lb.GetHeight()); lb.Dispose()
            if w > 0 and h > 0: NATIVE["char_w"] = w / float(len(sample)); NATIVE["font_h"] = h
        HUES = {}
        def hue_of(color):
            h = HUES.get(color)
            if h is not None: return h
            c = color.lstrip("#"); r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
            best, bd = HUE_TEXT, None
            for (pr, pg, pb), hue in HUE_PALETTE:
                d = (pr - r) ** 2 + (pg - g) ** 2 + (pb - b) ** 2
                if bd is None or d < bd: best, bd = hue, d
            if len(HUES) < 256: HUES[color] = best
            return best
        RGBS = {}
        def rgb_of(color):
            v = RGBS.get(color)
            if v is None: c = color.lstrip("#"); v = RGBS[color] = (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))
            return v
        def uo_font_for(size): return "char_w" in NATIVE and UO_FONT_MIN <= size <= UO_FONT_MAX
        def char_w(size): return NATIVE["char_w"] if uo_font_for(size) else size * 0.58
        LABELS = {}; LABELS_SWEEP = [LABELS_CAP]
        def label(text, size, color, aligned="left", maxWidth=0, applyStroke=False):
            if applyStroke or not uo_font_for(size):
                lb = ttf(text, size, color, aligned=aligned, maxWidth=maxWidth, applyStroke=applyStroke)
                LABELS.pop(id(lb), None); return lb
            if len(LABELS) > LABELS_SWEEP[0]:
                for k, v in list(LABELS.items()):
                    if v[0].IsDisposed: del LABELS[k]
                LABELS_SWEEP[0] = max(LABELS_CAP, 2 * len(LABELS))
            text = fit_text(text, maxWidth); lb = inert(API.Gumps.CreateGumpLabel(text, hue_of(color)))
            LABELS[id(lb)] = [lb, aligned, maxWidth, size, 0, 0, text]; return lb
        def _uo_meta(lb): m = LABELS.get(id(lb)); return m if m is not None and m[0] is lb else None
        def fit_text(text, maxw):
            if maxw and len(text) * NATIVE.get("char_w", 7) > maxw:
                return short(text, max(2, int(maxw / NATIVE.get("char_w", 7))))
            return text
        def place(lb, x, y, text=None):
            m = _uo_meta(lb)
            if m is None: lb.SetPos(x, y); return
            m[4], m[5] = x, y; aligned, maxw, size = m[1], m[2], m[3]
            if text is None: text = m[6]
            tw = int(len(text) * NATIVE["char_w"]); dx = 0
            if maxw and aligned == "right": dx = max(0, maxw - tw)
            elif maxw and aligned == "center": dx = max(0, (maxw - tw) // 2)
            dy = int(round((size * 1.35 - NATIVE["font_h"]) / 2.0)); lb.SetPos(int(x + dx), int(y + dy))
        def set_text(lb, text):
            m = _uo_meta(lb)
            if m is None: lb.SetText(text); return
            text = fit_text(text, m[2])
            if text == m[6]: return
            m[6] = text; lb.Text = text
            if m[1] != "left" and m[2]: place(lb, m[4], m[5], text)
        def set_hue(lb, color):
            if _uo_meta(lb) is None: return False
            lb.Hue = hue_of(color); return True
        def shift_held(): return bool(CLICK_MODS.get("shift") or Client.key_held("shift"))
        def alt_held(): return CLICK_MODS.get("alt") or Follow.alt_held()
        def layout_held_keys():
            return [c for c in CATS + ["combat",
                "panel"] if HOST.layout_holds("hub" if c == "panel" else "ultima." + c)]
        def drag_on(): return bool(SNAP.drag) or SNAP.pressed() is True
        CUT_CACHE = {}; CUT_CACHE_CAP = 2000
        def cut_text(text, px, size, smooth=False):
            if size > TEXT_FIT_MAX and (smooth or not uo_font_for(size)):
                cw = size * 0.6 if smooth else char_w(size); return short(text, max(4, int(px / cw)))
            k = (text, px); out = CUT_CACHE.get(k)
            if out is None:
                if len(CUT_CACHE) > CUT_CACHE_CAP: CUT_CACHE.clear()
                out = CUT_CACHE[k] = Kit.fit(text, max(10, int(px)))
            return out
        def text_y(top, h, font): return top + max(0, int((h - font * 1.35) / 2))
        def flat_button(parent, x, y, w, h, text, fn, tip=None, face=BTN_FACE, color=TEXT_COLOR, font=12, store=None):
            f = tiled(BUTTON_GUMP, w, h, FACE_HUE.get(face, hue_of(face))); f.SetPos(x, y); color = "#141414"
            parent.Add(f); lb = label(text, font, color, aligned="center", maxWidth=w); place(lb, x, text_y(y, h, font))
            parent.Add(lb); c = catcher(x, y, w, h, fn, tip); parent.Add(c)
            if store is not None: store.extend([f, lb, c])
            return lb
        def friend_button_count(): return (2 if settings["magery"] else 0) + (1 if settings["healing"] else 0)
        ALT_FOLLOW_TIP = "Alt+click: auto-follow (again to stop)"
        TIP_HEAL = ("Cast Heal on %s (Shift+click: Greater Heal). Alt+click: auto-follow (again to stop)")
        TIP_CURE = ("Cast Cure on %s (Shift+click: Arch Cure). Alt+click: auto-follow (again to stop)")
        TIP_BANDAGE = "Bandage %s when adjacent; farther away, follow them (again to stop). " + ALT_FOLLOW_TIP
        def friend_buttons(parent, x, y, w, h, serial, name, store=None, row=None):
            fs = max(7, int(h * 0.7 / min(1.0, settings["scale"] / 100.0)))
            tips, specs, parts = [], [], [] if store is None else store
            if settings["magery"]:
                for text, spell, stronger, tip, face in (("H", SPELL_HEAL, SPELL_GREATER_HEAL, TIP_HEAL, COL_HEAL),
                        ("C", SPELL_CURE, SPELL_ARCH_CURE, TIP_CURE, COL_CURE)):
                    specs.append((text, make_heal_click(serial, spell, stronger) if row is None else RowClick(row, (
                        lambda sp, st: lambda s, n: make_heal_click(s, sp, st))(spell, stronger)), tip, face,
                        "#FFFFFF"))
            if settings["healing"]:
                specs.append(("B", make_bandage_click(serial, name) if row is None else
                              RowClick(row, make_bandage_click), TIP_BANDAGE, COL_BANDAGE, "#202020"))
            for text, fn, tip, face, color in specs:
                flat_button(parent, x, y, w, h, text, fn, tip % name, face=face, color=color, font=fs, store=parts)
                tips.append((parts[-1], tip)); x += w + 2
            return tips
        def title_h(s): return max(16, int(round(TITLE_H * s)))
        def orow_h(s): return max(16, int(round(OPACITY_ROW_H * s)))
        def start_follow(serial):
            if safe(Follow.current) == serial: return True
            return Follow.start(serial, TITLE)
        def toggle_follow(serial): Follow.toggle(serial, TITLE)
        def follow_or(serial, fn):
            def _clicked(*args):
                if alt_held(): toggle_follow(serial)
                else: fn()
            return _clicked
        BANDAGE = {"serial": None, "name": "", "state": None, "until": 0.0, "follow": None}
        def end_follow(serial):
            if serial is None or BANDAGE["follow"] != serial: return
            BANDAGE["follow"] = None
            if safe(Follow.current) == serial: Follow.stop(TITLE)
        def make_bandage_click(serial, name):
            def _cb(*args):
                if BANDAGE["serial"] == serial:
                    BANDAGE["serial"] = None; release_cursor("bandage"); end_follow(serial)
                    say("stopped bandaging %s; cursor released." % name, Kit.HUE_GOOD); return
                try:
                    mob = API.FindMobile(serial)
                    if mob is None or bool(mob.IsDead): mob = None
                    else: me = API.Player; dist = max(abs(int(mob.X) - int(me.X)), abs(int(mob.Y) - int(me.Y)))
                except Exception: mob = None
                if mob is None:
                    say("can't bandage %s (out of sight or dead)." % name, Kit.HUE_BAD); return
                if dist > BANDAGE_RANGE:
                    if BANDAGE["follow"] == serial and safe(Follow.current) == serial:
                        end_follow(serial); say("stopped following %s." % name, Kit.HUE_GOOD); return
                    started = safe(Follow.current) != serial
                    if not start_follow(serial): return
                    if started: BANDAGE["follow"] = serial
                    say("following %s; press B again when adjacent." % name, Kit.HUE_INFO); return
                band = API.FindType(BANDAGE_GRAPHIC, API.Backpack) or API.FindType(BANDAGE_GRAPHIC)
                if not band: say("no bandages in your backpack.", Kit.HUE_BAD); return
                if BANDAGE["serial"] is not None or cursor_owner() is not None or API.HasTarget("any"):
                    say("a target cursor is up; clear it, then press B.", Kit.HUE_BAD); return
                API.UseObject(band)
                BANDAGE.update(serial=serial, name=name, state="cursor", until=time.time() + BANDAGE_CURSOR_WAIT)
                claim_cursor("bandage", BANDAGE_CLAIM)
            return Kit.once(follow_or(serial, _cb), ("ultima.bandage", serial), Kit.TWICE)
        CURSOR_KEY = "ultima"; CURSOR_OWN = {"bandage": False, "spell": False}
        def claim_cursor(what, seconds): CURSOR_OWN[what] = True; HOST.claim_cursor(CURSOR_KEY, seconds)
        def release_cursor(what):
            if not CURSOR_OWN.get(what): return
            CURSOR_OWN[what] = False
            if not any(CURSOR_OWN.values()): HOST.release_cursor(CURSOR_KEY)
        def cursor_owner(): return HOST.cursor_busy(CURSOR_KEY)
        def click_can_aim():
            owner = cursor_owner()
            if owner is not None and owner != "pick": return False
            return bool(API.HasTarget("any"))
        def handle_bandage():
            s = BANDAGE["serial"]
            if s is None: release_cursor("bandage"); return
            name = BANDAGE["name"]
            try: mob = API.FindMobile(s); gone = mob is None or bool(mob.IsDead)
            except Exception: gone = True
            if gone or time.time() > BANDAGE["until"]:
                BANDAGE["serial"] = None; end_follow(s)
                say(("can't bandage %s (out of sight or dead)." if gone else "no target cursor for bandaging %s.")
                    % name, Kit.HUE_BAD); return
            if BANDAGE["state"] == "cursor" and CURSOR_OWN["bandage"] and HOST.cursor_ok(CURSOR_KEY, "beneficial"):
                API.Target(s); BANDAGE["serial"] = None; release_cursor("bandage"); end_follow(s)
        def check_follow():
            safe(Follow.current); s = Follow.serial
            if s is not None and HOST.mobile(s) is None: Follow.serial = None
            if BANDAGE["follow"] is not None and Follow.serial != BANDAGE["follow"]: BANDAGE["follow"] = None
        OPACITY_ICON = ((3, 4, 3, 8, "#FFFFFF"), (6, 4, 3, 8, "#A0A0A0"), (9, 4, 3, 8, "#5A5A5A"))
        ICON_RECTS = {("lock", True): ((3, 8, 10, 6, None), (7, 10, 2, 2, BTN_FACE_ON), (4, 2, 8, 2, None),
                                       (4, 2, 2, 6, None), (10, 2, 2, 6, None)),
                      ("lock", False): ((3, 8, 10, 6, None), (7, 10, 2, 2, BTN_FACE), (4, 0, 8, 2, None),
                                        (4, 0, 2, 8, None), (10, 0, 2, 3, None)),
                      ("min", True): ((4, 4, 8, 2, None), (4, 4, 1, 8, None), (11, 4, 1, 8, None), (4, 11, 8, 1, None)),
                      ("min", False): ((4, 10, 8, 2, None),), ("opacity", True): OPACITY_ICON,
                      ("opacity", False): OPACITY_ICON}
        def draw_icon(add, add_ctrl, x, y, sz, kind, on):
            u = sz / 16.0
            def R(v): return int(round(v * u))
            def S(v): return max(1, int(round(v * u)))
            col = (LOCK_ON if on else LOCK_OFF) if kind == "lock" else ICON_COLOR
            for rx, ry, rw, rh, c in ICON_RECTS.get((kind, bool(on)), ()):
                add(x + R(rx), y + R(ry), S(rw), S(rh), c or col)
            if kind == "close":
                fs = max(8, int(sz * 0.8)); lb = ttf("x", fs, ICON_COLOR, aligned="center", maxWidth=sz)
                lb.SetPos(x, y + max(0, int((sz - fs * 1.35) / 2))); add_ctrl(lb)
        TITLE_CLICKS = {}; CHROMES = []
        def apply_borders_all():
            for c in list(CHROMES):
                if c.gump.IsDisposed: CHROMES.remove(c)
                else: c.frame.apply_borders()
        class Frame(object):
            def __init__(self, gump):
                self.size = (0, 0); self.center = tiled(SECTION_GUMP, 1, 1); gump.Add(self.center)
                self.edges = [tiled(FRAME_GUMP + (1 if i in (0, 1) else 3), 1, 1) for i in range(4)]
                for b in self.edges: gump.Add(b)
            def layout(self, w, h):
                self.size = (w, h)
                rects = [(0, 0, w, BORDER), (0, h - BORDER, w, BORDER), (0, 0, BORDER, h), (w - BORDER, 0, BORDER, h)]
                for b, r in zip(self.edges, rects): b.SetRect(*r)
                self.apply_borders()
            def apply_borders(self):
                on = settings["borders"]
                for p in self.edges: set_box_alpha(p, 1.0 if on else 0.0)
                w, h = self.size
                if on: self.center.SetRect(BORDER, BORDER, max(0, w - 2 * BORDER), max(0, h - 2 * BORDER))
                else: self.center.SetRect(0, 0, w, h)
            def set_alpha(self, a): set_box_alpha(self.center, a)
        class KitFrame(object):
            def __init__(self, gump, key=None):
                self.gump, self.key = gump, key; self.top = 0; base = Kit.WINDOW_BG
                self.s = [Kit.pic_size(base + i) for i in range(9)]; self.kw, self.kh = Kit.pic_size(Kit.CORNER_ART)
                self.fill = tiled(base + 4, 1, 1); self.center = tiled(Kit.SECTION_TILE, 1, 1)
                self.edges = [tiled(base + i, 1, 1) for i in (1, 7, 3, 5)]
                self.corners = [pic(base + i, 0, 0) for i in (0, 2, 6, 8)]
                self.knots = [pic(Kit.CORNER_ART, 0, 0) for _ in range(4)]
                self.parts = [self.fill] + self.edges + self.corners + self.knots
                for c in [self.fill, self.center] + self.parts[1:]: gump.Add(c)
                Kit._frame_parts[gump] = self.parts
            def layout(self, w, h, top=None):
                if top is not None: self.top = top
                M = Kit.MARGIN; tl, t, tr, l, c, r, bl, b, br = self.s
                self.fill.SetRect(l[0], t[1], max(0, w - l[0] - r[0]), max(0, h - t[1] - b[1]))
                for e, rc in zip(self.edges, ((tl[0], 0, w - tl[0] - tr[0], t[1]),
                        (bl[0], h - b[1], w - bl[0] - br[0], b[1]), (0, tl[1], l[0], h - tl[1] - bl[1]),
                        (w - r[0], tr[1], r[0], h - tr[1] - br[1]))):
                    e.SetRect(rc[0], rc[1], max(0, rc[2]), max(0, rc[3]))
                for cp, xy in zip(self.corners, ((0, 0), (w - tr[0], 0), (0, h - bl[1]), (w - br[0], h - br[1]))):
                    cp.SetPos(*xy)
                for k, xy in zip(self.knots, ((0, 0), (w - self.kw, 0), (0, h - self.kh), (w - self.kw, h - self.kh))):
                    k.SetPos(*xy)
                ch = h - self.top - M; self.center.SetRect(M, self.top, max(0, w - 2 * M), max(0, ch))
                Kit.set(self.center, "IsVisible", ch > 4)
            def apply_borders(self): pass
            def set_alpha(self, a): set_box_alpha(self.center, a)
            def drop_all(self):
                for c in [self.center] + self.parts: drop(c)
                if Kit._frame_parts.get(self.gump) is self.parts: Kit._frame_parts.pop(self.gump, None)
        class Chrome(object):
            def __init__(self, gump, kit=False, key=None):
                self.gump = gump; self.kit, self.key = kit, key
                self.frame = KitFrame(gump, key) if kit else Frame(gump)
                CHROMES[:] = [c for c in CHROMES if c.gump is not gump and not c.gump.IsDisposed]
                CHROMES.append(self); self.strip = []
                self.title_bg = self.title_lbl = self.slider = self.pct_lbl = None
                self.title_text = self.title_color = self.title_raw = self.status_x = None
                self.status_lbl = self.status_text = None
                self.title_max, self.title_pos, self.font = 40, (0, 0), TITLE_FONT
                self.opacity, self.content_top = DEFAULT_OPACITY, BORDER; self.on_title_alt, self.alt_key = None, None
            def _add(self, ctrl): self.gump.Add(ctrl); self.strip.append(ctrl); return ctrl
            def _clear_strip(self):
                for c in self.strip: drop(c)
                self.strip = []; self.title_bg = self.title_lbl = self.slider = self.pct_lbl = None
                self.status_lbl, self.status_text = None, None
            def dispose(self):
                self._clear_strip(); self.frame.drop_all()
                if self in CHROMES: CHROMES.remove(self)
            def layout(self, w, h, s, opacity, title, color, buttons, opacity_open, on_dbl, on_title_alt, alt_key):
                self.opacity = opacity; a = opacity / 100.0; self.frame.layout(w, h); self.frame.set_alpha(a)
                self._clear_strip(); th = title_h(s)
                self.title_bg = self._add(tiled(HEADER_GUMP, w - 2 * BORDER, th))
                self.title_bg.SetPos(BORDER, BORDER); set_box_alpha(self.title_bg, a)
                d = self._add(tiled(Kit.STONE_TILE, w - 2 * BORDER, DIVIDER_H))
                d.SetPos(BORDER, BORDER + th - DIVIDER_H)
                bsz = max(12, th - 6 - DIVIDER_H); gap = max(2, int(round(2 * s))); n = len(buttons)
                bx = w - BORDER - 4 - n * bsz - max(0, n - 1) * gap; left = bx; self.on_title_dbl = on_dbl
                self.on_title_alt, self.alt_key = on_title_alt, alt_key
                self._title_catch(BORDER, max(10, left - BORDER - 2), th, Kit.DOUBLE_TIP + ". " + ALT_FOLLOW_TIP)
                by = BORDER + (th - DIVIDER_H - bsz) // 2
                for kind, on, fn, tip in buttons: self._button(bx, by, bsz, kind, on, fn, tip); bx += bsz + gap
                self.font = max(9, int(round(TITLE_FONT * text_scale(s)))); self.title_max = max(20, left - BORDER - 10)
                self.title_pos = (BORDER + 5, text_y(BORDER, th - DIVIDER_H, self.font)); self.title_color = color
                self.title_text = None; self.set_title(title); y = BORDER + th
                if opacity_open:
                    rh = orow_h(s); fs = max(8, int(round(11 * text_scale(s))))
                    lb = self._add(label("Opacity", fs, DIM_TEXT)); place(lb, BORDER + 5, text_y(y, rh, fs))
                    pw = int(round(34 * s)); sx = BORDER + int(round(54 * s)); sw = max(40, w - BORDER - 8 - pw - sx)
                    self.slider = API.Gumps.CreateSlider(sw, 0, 100, opacity, sx, y + max(2, (rh - 10) // 2), True)
                    self._add(self.slider)
                    self.pct_lbl = self._add(label("%d%%" % opacity, fs, TEXT_COLOR, aligned="right", maxWidth=pw))
                    place(self.pct_lbl, w - BORDER - 4 - pw, text_y(y, rh, fs)); y += rh
                self.content_top = y
            def _title_catch(self, xy, w, h, tip):
                tc = catcher(xy, xy, w, h, self._title_clicked, tip); Kit.set(tc, "CanMove", True)
                if Client.mouse is None: Kit.hook_double(tc, self._dbl_once())
                self._add(tc)
            def _dbl_once(self): return Kit.once(lambda: self.on_title_dbl(), ("utitle", id(self)))
            def layout_kit(self, w, h, opacity, title, color, mini, on_min, on_dock):
                M = Kit.MARGIN; self._clear_strip(); self.content_top = KIT_HEAD; self.frame.layout(w, h, KIT_HEAD)
                self.frame.set_alpha(opacity / 100.0); sec = self._add(tiled(Kit.SECTION_TILE, w - 2 * M, 30))
                sec.SetPos(M, M); set_box_alpha(sec, Kit.SECTION_ALPHA)
                if not mini: self._add(box(1.0, color)).SetRect(M, M + 30, w - 2 * M, 3)
                bx = w - M - 54
                if not Kit.zone_up(self.key):
                    self._art((Kit.ART_RESTORE if mini else Kit.ART_MIN)[0], bx, M + 7, on_min,
                              Kit.RESTORE_TIP if mini else Kit.MIN_TIP)
                    bx -= Kit.DOCK_DX
                    if not mini: self._art(Kit.ART_DOCK[0], bx, M + 7 + Kit.DOCK_DY, on_dock, Kit.DOCK_TIP); bx -= 10
                left = bx
                if not mini:
                    cap = "Settings"; sx = bx - 35 - Kit.text_w(cap)
                    if sx > M + 30 + Kit.text_w("COMBAT") + 40:
                        self._art(Kit.ART_PAGE[0], sx, M + 4, settings_click, Kit.SETTINGS_TIP % TITLE, cap); left = sx
                zoned = Kit.zone_up(self.key); self.on_title_dbl = (lambda: None) if zoned else on_min
                self._title_catch(M, max(10, left - M - 6), 30, None if zoned else Kit.DOUBLE_TIP)
                self.title_max = max(20, left - M - 30 - 10); self.title_pos = (M + 30, M + 7); self.title_color = color
                self.title_text = None; self.set_title(title)
            def _art(self, graphic, x, y, fn, tip, cap=None):
                p = self._add(pic(graphic, x, y)); bw, bh = Kit.pic_size(graphic); bw, bh = bw or 20, bh or 20
                if cap:
                    lb = Kit.add_label(self.gump, cap, x + bw + 5, y + 3, Kit.HUE_TEXT); self.strip.append(lb)
                    bw += 5 + Kit.text_w(cap)
                self._add(catcher(x, y, bw, bh, fn, tip)); return p
            def set_status(self, text):
                if not self.kit or self.title_lbl is None: return
                text = text or ""
                if text == self.status_text: return
                self.status_text = text; x = self.title_pos[0] + Kit.text_w(self.title_text or "") + 12
                room = self.title_pos[0] + self.title_max - x; shown = Kit.fit(text, room) if room > 20 else ""
                at = (x, self.title_pos[1])
                if self.status_lbl is None:
                    self.status_lbl = Kit.add_label(self.gump, shown, x, self.title_pos[1], Kit.HUE_INFO)
                    self.strip.append(self.status_lbl); self.status_x = at
                else:
                    if at != self.status_x: self.status_x = at; self.status_lbl.SetPos(x, self.title_pos[1])
                    Kit.set_text(self.status_lbl, shown)
            def _title_clicked(self, *args):
                now = time.time(); key = id(self.gump)
                pos = (self.gump.GetX(), self.gump.GetY())
                if self.on_title_alt is not None and alt_held():
                    ak = self.alt_key; ref = ANCHORS.pos.get(ak) if ak is not None else None
                    moved = (ak is not None and ANCHORS.moving == ak) or SNAP.drag \
                        or (ref is not None and (abs(pos[0] - ref[0]) > TITLE_JITTER
                                                 or abs(pos[1] - ref[1]) > TITLE_JITTER))
                    if not moved: self.on_title_alt()
                    return
                last = TITLE_CLICKS.get(key)
                if last and now - last[0] <= TITLE_DBL_SECONDS and abs(pos[0] - last[1][0]) <= TITLE_JITTER \
                        and abs(pos[1] - last[1][1]) <= TITLE_JITTER:
                    TITLE_CLICKS.pop(key, None); self._dbl_once()()
                else:
                    if len(TITLE_CLICKS) > CACHE_CAP: TITLE_CLICKS.clear()
                    TITLE_CLICKS[key] = (now, pos)
            def _button(self, x, y, sz, kind, on, fn, tip):
                icon = NATIVE.get("icons", {}).get(kind)
                if icon:
                    graphic, (iw, ih) = icon[1 if on else 0]
                    if iw <= sz + 6 and ih <= sz + 6:
                        hue = HUE_LOCKED if kind == "lock" and on else 0
                        p = self._add(pic(graphic, x + (sz - iw) // 2, y + (sz - ih) // 2, hue))
                        if kind == "lock" and not on: set_box_alpha(p, LOCK_OFF_ALPHA)
                        self._add(catcher(x, y, sz, sz, fn, tip)); return
                if kind == "close" and "char_w" in NATIVE:
                    lb = inert(self._add(API.Gumps.CreateGumpLabel("x", HUE_TEXT)))
                    lb.SetPos(x + max(0, (sz - int(NATIVE["char_w"])) // 2), y + (sz - NATIVE["font_h"]) // 2)
                    self._add(catcher(x, y, sz, sz, fn, tip)); return
                lit = on and kind in ("lock", "opacity"); face = self._add(box(1.0, BTN_FACE_ON if lit else BTN_FACE))
                face.SetRect(x, y, sz, sz)
                def add(bx, by, bw, bh, col): p = self._add(box(1.0, col)); p.SetRect(bx, by, bw, bh)
                draw_icon(add, self._add, x, y, sz, kind, on); self._add(catcher(x, y, sz, sz, fn, tip))
            def set_title(self, text, color=None):
                if self.kit:
                    rk = (text, self.title_max)
                    if self.title_lbl is not None and rk == self.title_raw: return
                    self.title_raw = rk; text = Kit.fit(str(text).upper(), self.title_max)
                    if self.title_lbl is None:
                        self.title_lbl = Kit.add_label(self.gump, text, self.title_pos[0],
                                                       self.title_pos[1], Kit.HUE_TITLE)
                        self.strip.append(self.title_lbl); self.title_text = text
                    elif text != self.title_text:
                        self.title_text = text; Kit.set_text(self.title_lbl, text)
                        if self.status_text is not None:
                            sv, self.status_text = self.status_text, None; self.set_status(sv)
                    return
                if color is not None and color != self.title_color:
                    self.title_color = color; old = self.title_lbl
                    if old is not None and not set_hue(old, color):
                        self.title_text = None
                        if old in self.strip: self.strip.remove(old)
                        drop(old); self.title_lbl = None
                text = cut_text(text, self.title_max, self.font)
                if self.title_lbl is None:
                    self.title_lbl = self._add(label(text, self.font, self.title_color or TEXT_COLOR))
                    place(self.title_lbl, *self.title_pos); self.title_text = text
                elif text != self.title_text: self.title_text = text; set_text(self.title_lbl, text)
            def set_opacity(self, v):
                self.opacity = v; a = v / 100.0; self.frame.set_alpha(a)
                if self.kit: return
                if self.title_bg is not None: set_box_alpha(self.title_bg, a)
                if self.pct_lbl is not None: set_text(self.pct_lbl, "%d%%" % v)
            def poll(self):
                if self.slider is None: return None
                v = clamp(int(self.slider.Value), 0, 100)
                if v != self.opacity: self.set_opacity(v); return v
                return None
        class Anchors(object):
            def __init__(self):
                self.gid, self.next_gid, self.pos, self.dims = {}, 1, {}, {}
                self.moving, self.still, self.linger, self.saved = None, 0, 0, []
                self.pending = self.alt_used = self.touched = False
            def placed(self, key, x=None, y=None, w=None, h=None):
                if x is None: self.pos.pop(key, None)
                else: self.pos[key] = (int(x), int(y))
                if w is None: self.dims.pop(key, None)
                else: self.dims[key] = (int(w), int(h))
                self.pending = True
            def sized(self, key, w, h): self.dims[key] = (int(w), int(h))
            @staticmethod
            def host_follows(g):
                out = set()
                if not SNAP.enabled or g in SNAP.no_snap: return out
                links, members = SNAP.links, SNAP.members; todo = [g]
                while todo:
                    lead = todo.pop()
                    for f, l in list(links.items()):
                        if l is lead and f is not g and f not in out and f in members: out.add(f); todo.append(f)
                return out
            def add_group(self, keys):
                g = self.next_gid; self.next_gid += 1
                for k in keys: self.gid[k] = g
            def members(self, key):
                g = self.gid.get(key)
                if g is None: return [key]
                return [k for k, v in self.gid.items() if v == g]
            def join(self, a, b):
                ga, gb = self.gid.get(a), self.gid.get(b)
                if ga is None and gb is None: self.add_group([a, b])
                elif ga is None: self.gid[a] = gb
                elif gb is None: self.gid[b] = ga
                elif ga != gb:
                    for k, v in list(self.gid.items()):
                        if v == gb: self.gid[k] = ga
                self.touched = True
            def detach(self, key):
                g = self.gid.pop(key, None)
                if g is not None:
                    self.touched = True; rest = [k for k, v in self.gid.items() if v == g]
                    if len(rest) == 1: self.gid.pop(rest[0], None)
            def clear(self): self.gid = {}; self.touched = True
            def saved_groups(self):
                groups = {}
                for k, g in self.gid.items():
                    if k in FIXED_WINDOWS: groups.setdefault(g, []).append(k)
                return [sorted(v) for v in groups.values() if len(v) > 1]
            def groups_changed(self):
                if not self.touched: return False
                self.touched = False; now = self.saved_groups()
                if now == self.saved: return False
                self.saved = now; return True
            @staticmethod
            def shift(m, dx, dy, rects, wins):
                x, y, w, h = rects[m]
                g = wins[m][0]; nx, ny = Kit.place(g, x + dx, y + dy, w, h); Kit.moved_by_code(g)
                rects[m] = (nx, ny, w, h)
            def tick(self, get_wins):
                if self.moving is None and not self.pending and self.linger <= 0 and not SNAP.drag:
                    for k in list(self.gid):
                        if k not in FIXED_WINDOWS and not pop_listed(k): self.detach(k)
                    return
                self.pending = False
                if self.linger > 0: self.linger -= 1
                wins = get_wins()
                for k in list(self.gid):
                    if k not in wins and k not in FIXED_WINDOWS: self.detach(k)
                rects = {k: (int(g.GetX()), int(g.GetY()), int(g.GetWidth()) or size[0], int(g.GetHeight()) or size[1])
                         for k, (g, size) in wins.items() if Kit.is_open(g)}
                held = layout_held_keys(); arranging = HOST.layout_arranging()
                moved = [k for k, r in rects.items() if k in self.pos and (r[0], r[1]) != self.pos[k] and k not in held]
                if moved:
                    k = self.moving if self.moving in moved else None
                    if k is None:
                        for m in moved:
                            if wins[m][0] in SNAP.drag: k = m; break
                    if k is None: k = moved[0]
                    dx = rects[k][0] - self.pos[k][0]; dy = rects[k][1] - self.pos[k][1]
                    resized = self.dims.get(k, rects[k][2:]) != rects[k][2:]
                    if resized: moved = []
                    elif k in self.gid and alt_held():
                        self.detach(k)
                        if not self.alt_used:
                            self.alt_used = True; say("window unanchored.", Kit.HUE_GOOD)
                    host_moved = self.host_follows(wins[k][0]) if moved and not arranging else ()
                    for m in (self.members(k) if moved and not arranging else []):
                        if m != k and m not in moved and m in rects and m not in held and wins[m][0] not in host_moved:
                            self.shift(m, dx, dy, rects, wins)
                    if not resized: self.moving = k; self.still = 0
                elif self.moving is not None:
                    if not SNAP.drag: self.still += 1
                    if self.still >= ANCHOR_SETTLE_POLLS:
                        k, self.moving = self.moving, None
                        if k in rects and k not in held and not arranging: self.snap(k, rects, wins, held)
                        self.linger = ANCHOR_LINGER_POLLS
                self.pos = {k: r[:2] for k, r in rects.items()}; self.dims = {k: r[2:] for k, r in rects.items()}
            def snap(self, k, rects, wins, held):
                kx, ky, kw, kh = rects[k]; group = set(self.members(k))
                if any(m in held for m in group): return
                best = None
                for o, (ox, oy, ow, oh) in rects.items():
                    if o in group or o in held: continue
                    cands = []
                    if ky < oy + oh and oy < ky + kh:
                        cands += [(abs(kx - (ox + ow)), ox + ow - kx, 0), (abs(kx + kw - ox), ox - kw - kx, 0)]
                    if kx < ox + ow and ox < kx + kw:
                        cands += [(abs(ky - (oy + oh)), 0, oy + oh - ky), (abs(ky + kh - oy), 0, oy - kh - ky)]
                    for d, dx, dy in cands:
                        if d <= SNAP_DIST and (best is None or d < best[0]):
                            if dx and abs(ky - oy) <= SNAP_DIST: dy = oy - ky
                            if dy and abs(kx - ox) <= SNAP_DIST: dx = ox - kx
                            best = (d, dx, dy, o)
                if best is None: return
                _, dx, dy, o = best
                for m in group:
                    if m in rects: self.shift(m, dx, dy, rects, wins)
                self.join(k, o)
        ANCHORS = Anchors()
        def pop_listed(k): return k.startswith("pop:") and int(k[4:]) in POPS
        import threading; FILE_LOCK = threading.Lock(); SAVE_SEQ = [0]; SAVE_ERR = [None]; DATA_READY = [False]
        FOE_CHG = {}; FILE_MT = [None]; MERGE_WAIT = [0.0]; PEND = [0]; GONE = [0.0]
        def in_background(fn):
            t = threading.Thread(target=fn); t.daemon = True; t.start()
        def read_save_lines():
            path = DATA_FILE if os.path.exists(DATA_FILE) else stranded_tmp() or OLD_DATA_FILE
            if not os.path.exists(path): return None, []
            with FILE_LOCK:
                with open(path, "r") as f: lines = f.readlines()
                if path == DATA_FILE: FILE_MT[0] = file_stamp()
            return path, lines
        def load_settings():
            try: path, lines = read_save_lines()
            except Exception as ex:
                say("couldn't read the save file (%s); saving is off this session." % ex, Kit.HUE_BAD); return
            parse_save_lines(path, lines)
        def save_settings():
            if views["windows"] is not None and not st.get("shutting"): SAVE_REQ[0] = True
            else: save_data(background=True)
        def parse_save_lines(path, lines):
            if path is None: DATA_READY[0] = True; return
            section = None; links = []
            try:
                for raw in lines:
                    try:
                        line = raw.strip()
                        if not line or line.startswith("#"): continue
                        if line.startswith("[") and line.endswith("]"): section = line[1:-1].strip().lower(); continue
                        if section == "foes": FOES[name_key(line)] = line
                        elif section == "ignore": IGNORE[line.lower()] = line
                        elif section == "players": PLAYER_NAMES[line.lower()] = line; PLAYER_VER[0] += 1
                        elif section == "settings" and "=" in line:
                            key, val = [p.strip().lower() for p in line.split("=", 1)]
                            if key in INT_SETTINGS: settings[key] = clamp(int(val), *INT_SETTINGS[key])
                            elif key in BOOL_SETTINGS: settings[key] = val == "true"
                        elif section == "anchors" and "=" in line:
                            keys = [k.strip().lower() for k in line.split("=", 1)[1].split(",")]
                            keys = [k for k in keys if k in FIXED_WINDOWS]
                            if len(keys) > 1: ANCHORS.add_group(keys)
                        elif section == "layout" and "=" in line:
                            key, val = line.split("=", 1); key = key.strip().lower()
                            parts = [p.strip() for p in val.split(",")]
                            if key in LAYOUT and len(parts) >= 5:
                                LAYOUT[key] = [int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]),
                                               parts[4].lower() == "true",
                                               len(parts) > 5 and parts[5].lower() == "true",
                                               clamp(int(parts[6]), 0, 100) if len(parts) > 6 else settings["opacity"]]
                                if key == "combat": st["combat_loaded"] = True
                        elif section == "sightings":
                            e = parse_sight(line)
                            if e is not None: SIGHTS.append(e); note_seen(e)
                        elif section == "links" and "|" in line:
                            alt, main = line.split("|", 1); links.append((name_key(alt), name_key(main)))
                        elif section == "foe_seen" and "|" in line:
                            p = line.split("|", 5)
                            seen = (float(p[0]), int(p[1]), int(p[2]), int(p[3]), {"1": True, "0": False}.get(p[4]))
                            k = name_key(p[5]); old = LAST_SEEN.get(k)
                            if k and (old is None or old[0] < seen[0]): LAST_SEEN[k] = seen
                    except Exception: continue
                trim_sights(); trim_players()
                for alt, main in links:
                    if alt != main and alt in FOES and main in FOES: ALT_OF[alt] = main
                flatten_links()
                for key in LAYOUT: L = LAYOUT[key]; L[0], L[1] = Kit.adapt(L[0], L[1], L[2], L[3])
                DATA_READY[0] = True
            except Exception as ex:
                say("couldn't read the save file (%s); saving is off this session." % ex, Kit.HUE_BAD)
            if path == OLD_DATA_FILE:
                for k in ("friend", "foe", "neutral"): LAYOUT[k][6] = settings["opacity"]
        def load_old_combat_settings():
            if st["combat_loaded"]: return
            def get(key, default):
                try: return int(API.GetPersistentVar(key, str(default), API.PersistentVar.Char))
                except Exception: return default
            L = LAYOUT["combat"]; L[0], L[1] = get("CombatBars_X", L[0]), get("CombatBars_Y", L[1])
            L[2] = clamp(get("CombatBars_W", L[2]), CB_MIN_WIDTH, CB_MAX_WIDTH)
            L[6] = clamp(get("CombatBars_Opacity", L[6]), 0, 100); L[4] = get("CombatBars_Locked", 0) == 1
            L[5] = get("CombatBars_Minimized", 0) == 1; settings["magery"] = get("CombatBars_Magery", 0) == 1
            st["dirty_save"] = True
        def stranded_tmp():
            try:
                d = os.path.dirname(DATA_FILE) or "."; base = os.path.basename(DATA_FILE) + "."
                tmps = [os.path.join(d, n) for n in os.listdir(d) if n.startswith(base) and n.endswith(".tmp")]
            except Exception: return None
            best, best_t = None, None
            for t in tmps:
                try: m = os.path.getmtime(t)
                except Exception: continue
                if best_t is None or m > best_t: best, best_t = t, m
            return best
        def write_save_file(text): Kit.write_safe(DATA_FILE, text, None)
        def file_stamp(): return safe(lambda: (os.path.getmtime(DATA_FILE), os.path.getsize(DATA_FILE)))
        def merge_foes():
            mt = file_stamp(); now = time.time()
            if mt is None:
                if FILE_MT[0] is None: return True
                if not GONE[0]: GONE[0] = now
                if now - GONE[0] < 5.0: return False
                FILE_MT[0] = None; GONE[0] = 0.0; return True
            GONE[0] = 0.0
            if mt == FILE_MT[0]: return True
            oc = Client.on_client_thread()
            if (PEND[0] and not oc) or now < MERGE_WAIT[0]: return False
            try:
                with FILE_LOCK:
                    with open(DATA_FILE, "r") as f: lines = f.readlines()
            except Exception as ex:
                MERGE_WAIT[0] = now + 30.0
                say("couldn't read the save file to merge it (%s); saving waits." % ex, Kit.HUE_BAD); return False
            sect, got = None, []
            for raw in lines:
                line = raw.strip()
                if line.startswith("[") and line.endswith("]"): sect = line[1:-1].strip().lower()
                elif sect == "foes" and line and not line.startswith("#"): got.append(line)
            if oc: apply_foes(got, mt, 0); return True
            tok = PEND[0] = id(got); TICK_JOBS.append(lambda: apply_foes(got, mt, tok)); return False
        def apply_foes(got, mt, tok):
            if tok and tok != PEND[0]: return
            PEND[0] = 0; out = Kit.merge_text("\n".join(got), dict(FOE_CHG), name_key)[1]
            new = dict((name_key(n), n) for n in out)
            for k in [k for k in FOES if k not in new]: del FOES[k]
            FOES.update(new); FILE_MT[0] = mt; st["foe_ver"] += 1
            if tok: save_settings()
        def report_save_error():
            err, SAVE_ERR[0] = SAVE_ERR[0], None
            if err: say("couldn't save (%s)." % err, Kit.HUE_BAD)
        def save_text():
            if not DATA_READY[0] or not merge_foes(): return None
            def tf(b): return "true" if b else "false"
            try:
                out = ["# UltimaTracker save file - one name per line"]
                for sect, names in (("foes", FOES), ("ignore", IGNORE)):
                    out += ["[%s]" % sect] + sorted(names.values(), key=lambda s: s.lower()) + [""]
                ver = PLAYER_VER[0]
                if PLAYER_TEXT[0] != ver or PLAYER_TEXT[1] is None:
                    PLAYER_TEXT[1] = sorted(PLAYER_NAMES.values(), key=lambda s: s.lower()); PLAYER_TEXT[0] = ver
                out += ["[players]"] + PLAYER_TEXT[1] + [""]
                out += ["[settings]"] + ["%s=%d" % (k, settings[k]) for k in INT_ORDER]
                out += ["%s=%s" % (k, tf(settings[k])) for k in BOOL_SETTINGS] + ["", "[anchors]"]
                out += ["group=%s" % ",".join(keys) for keys in ANCHORS.saved_groups()]
                out += ["", "[layout]"] + ["%s=%d,%d,%d,%d,%s,%s,%d" % (
                    k, v[0], v[1], v[2], v[3], tf(v[4]), tf(v[5]), v[6]) for k, v in LAYOUT.items()]
                out += ["", "[links]"] + ["%s|%s" % (FOES[a], FOES[m]) for a, m in sorted(ALT_OF.items())
                                          if a in FOES and m in FOES and "|" not in FOES[a] + FOES[m]]
                out += ["", "[foe_seen]"] + [seen_line(k) for k in sorted(FOES) if k in LAST_SEEN]
                out += ["", "[sightings]"] + [e[S_LINE] for e in SIGHTS]; return "\n".join(out) + "\n"
            except Exception as ex: say("couldn't save (%s)." % ex, Kit.HUE_BAD); return None
        def write_text(text, seq=None):
            with FILE_LOCK:
                if seq is not None and seq != SAVE_SEQ[0]: return
                try: write_save_file(text); FILE_MT[0] = file_stamp(); return True
                except Exception as ex: SAVE_ERR[0] = str(ex)
        def save_data(background=False):
            text = save_text()
            if text is None: return
            st["dirty_save"] = False; SIGHT["dirty"] = False; SAVE_SEQ[0] += 1; seq = SAVE_SEQ[0]
            chg = dict(FOE_CHG)
            def write():
                if write_text(text, seq):
                    for k, v in chg.items():
                        if FOE_CHG.get(k, 0) == v: FOE_CHG.pop(k, None)
            if background: in_background(write)
            else: write(); report_save_error()
        def build_window():
            windows = {c: CategoryGump(c) for c in CATS}; combat = CombatWindow()
            views.update({"windows": windows, "combat": combat})
            if settings["combat_shown"]: combat.show()
            views["panel"] = ControlPanel(windows, combat); register_docks(windows, combat); st["foe_ver"] += 1
            n = len(FOES); say("on, %s." % Kit.count(n, "saved foe"), Kit.HUE_GOOD)
            M.update({"last_layout": layout_signature(), "tick": 0,
                      "next_scan": 0.0, "next_combat": 0.0, "next_glow": 0.0})
            if Kit.get_var(SIGHT_OPEN_KEY) == "1": SIGHT_WIN.show()
        wnd = None; views = {"windows": None, "combat": None, "panel": None}
        S_T, S_SERIAL, S_NOTO, S_FACET, S_X, S_Y, S_GUARD, S_NAME, S_KEY, S_LINE = range(10)
        GUARD_CH = {True: "1", False: "0", None: "-"}; GUARD_OF = {"1": True, "0": False}
        def sight_line(t, serial, noto, facet, x, y, guard, name):
            return "%d|%d|%s|%d|%d|%d|%s|%s" % (int(t), int(serial), noto, int(facet), int(x),
                                                int(y), GUARD_CH.get(guard, "-"), name)
        def parse_sight(line):
            p = line.split("|", 7)
            if len(p) < 8 or not p[7]: return None
            return [float(p[0]), int(p[1]), p[2] or "unknown", int(p[3]), int(p[4]), int(p[5]),
                    GUARD_OF.get(p[6]), p[7], name_key(p[7]), line]
        def note_seen(e):
            k = e[S_KEY]; old = LAST_SEEN.get(k)
            if old is not None and old[0] > e[S_T]: return False
            LAST_SEEN[k] = (e[S_T], e[S_FACET], e[S_X], e[S_Y], e[S_GUARD]); return k in FOES
        def seen_line(k):
            t, facet, x, y, guard = LAST_SEEN[k]
            return "%d|%d|%d|%d|%s|%s" % (int(t), facet, x, y, GUARD_CH.get(guard, "-"), FOES[k])
        def trim_sights():
            n = len(SIGHTS)
            if n > SIGHT_CAP + SIGHT_SLACK: del SIGHTS[:n - SIGHT_CAP]
            if len(LAST_SEEN) > 2 * SIGHT_CAP:
                keep = dict((k, v) for k, v in LAST_SEEN.items() if k in FOES); LAST_SEEN.clear()
                LAST_SEEN.update(keep)
                for e in SIGHTS: note_seen(e)
        def log_sighting(t, serial, name, noto, facet, x, y, guard):
            line = sight_line(t, serial, noto, facet, x, y, guard, name)
            e = [float(int(t)), serial, noto, facet, x, y, guard, name, name_key(name), line]; SIGHTS.append(e)
            trim_sights()
            if note_seen(e): SIGHT["seen_ver"] += 1
            SIGHT["ver"] += 1
            if not SIGHT["dirty"]: SIGHT["dirty"] = True; SIGHT["save_at"] = t + SIGHT_SAVE_SECONDS
        def noto_word(noto): return NOTO_WORD.get(noto, noto or "unknown")
        def place_text(facet, x, y):
            f = FACETS.get(facet)
            if f is None: f = "map %d" % facet if facet >= 0 else "?"
            return "%s %d,%d" % (f, x, y)
        def today_start(now): lt = time.localtime(now); return now - (lt.tm_hour * 3600 + lt.tm_min * 60 + lt.tm_sec)
        def stamp(t, today0):
            try: return time.strftime("%H:%M" if t >= today0 else "%m/%d %H:%M", time.localtime(t))
            except Exception: return "?"
        def seen_text(k, now):
            s = LAST_SEEN.get(k)
            if s is None: return "not seen yet"
            t, facet, x, y, guard = s
            return "seen %s, %s%s" % (Kit.ago(now - t, Kit.AGO_WORDS), place_text(facet, x, y),
                " (guarded)" if guard else "")
        def flatten_links():
            for alt in list(ALT_OF):
                m, n = ALT_OF.get(alt), 0
                while m in ALT_OF and n < 10: m, n = ALT_OF[m], n + 1
                if m is None or m == alt or m in ALT_OF: ALT_OF.pop(alt, None)
                else: ALT_OF[alt] = m
        def alts_of(main): return sorted(a for a, m in ALT_OF.items() if m == main)
        def link_text(k):
            m = ALT_OF.get(k)
            if m is not None: return "alt of " + FOES.get(m, m)
            alts = alts_of(k)
            if alts: return "alts: " + ", ".join(FOES.get(a, a) for a in alts)
            return ""
        def link_foes(a, b):
            main = ALT_OF.get(a, a)
            if b == main or ALT_OF.get(b) == main:
                return "%s and %s are already linked." % (FOES.get(a, a), FOES.get(b, b))
            old = ALT_OF.get(b, b)
            for k in list(ALT_OF):
                if ALT_OF[k] == old: ALT_OF[k] = main
            if old != main: ALT_OF[old] = main
            ALT_OF[b] = main; ALT_OF.pop(main, None); flatten_links()
            return "linked %s as an alt of %s." % (FOES.get(b, b), FOES.get(main, main))
        def unlink_foe(k):
            if k in ALT_OF: del ALT_OF[k]; return True
            alts = alts_of(k)
            if not alts: return False
            new = alts[0]; del ALT_OF[new]
            for a in alts[1:]: ALT_OF[a] = new
            return True
        NOTE_CACHE = {}; NOTE_TTL = 10.0
        def social_note(name):
            fn = HOST.services.get("social.note")
            if fn is None or not name: return ""
            now = time.time(); hit = NOTE_CACHE.get(name)
            if hit is not None and 0.0 <= now - hit[0] < NOTE_TTL: return hit[1]
            try: n = str(fn(name) or "").strip()
            except Exception: return ""
            n = n if len(n) <= NOTE_MAX else n[:NOTE_MAX - 2] + ".."
            if len(NOTE_CACHE) > 500: NOTE_CACHE.clear()
            NOTE_CACHE[name] = (now, n); return n
        def tip_for(tip, name, extra=""):
            lines = [tip]
            if extra: lines.insert(0, extra)
            lk = link_text(name_key(name)) if name else ""
            if lk: lines.insert(0, lk[0].upper() + lk[1:])
            n = social_note(name)
            if n: lines.append("Note: " + n)
            return "\n".join(lines)
        def add_foe(name): FOES[name_key(name)] = FOE_CHG[name_key(name)] = name; st["foe_ver"] += 1; save_settings()
        def drop_foe(key): FOE_CHG[key] = None; st["foe_ver"] += 1; save_settings(); return FOES.pop(key)
        def is_foe(serial=None, name=None):
            if name:
                k = name_key(str(name))
                if k and k in FOES: return True
            if serial is None: return False
            try: s = int(serial)
            except Exception: return False
            k = FOE_SERIALS.get(s)
            if k is not None and k in FOES: return True
            if not name:
                try: m = API.FindMobile(s); k = name_key(str(m.Name or "")) if m is not None else ""
                except Exception: k = ""
                return bool(k) and k in FOES
            return False
        NPC_CACHE = {}; SEEN_PLAYER = set(); PLAYER_NAMES = {}; PLAYER_VER = [0]; PLAYER_TEXT = [None, None]
        TITLED_NPCS = set(); TITLE_CACHE = {}; KARMA_TAG_RE = re.compile(r"^\s*\[[^\]]+\]\s*$")
        def trim_players(limit=None):
            if len(PLAYER_NAMES) <= (PLAYER_NAMES_CAP if limit is None else limit): return
            drop = len(PLAYER_NAMES) - PLAYER_NAMES_KEEP; later = []
            for low, name in list(PLAYER_NAMES.items()):
                if drop <= 0: break
                if low in IGNORE or name_key(name) in FOES: later.append(low); continue
                del PLAYER_NAMES[low]; drop -= 1
            for low in later:
                if drop <= 0: break
                del PLAYER_NAMES[low]; drop -= 1
            PLAYER_VER[0] += 1; NPC_CACHE.clear(); st["dirty_save"] = True
        def capped(cache):
            if len(cache) > CACHE_CAP: cache.clear()
        JOURNAL_NEXT = [0.0]; JREAD = {"learn": None, "attack": None, "killer": None}
        def learn_from_journal():
            now = time.time()
            if now < JOURNAL_NEXT[0]: return
            JOURNAL_NEXT[0] = now + 1.0; rd = JREAD["learn"]
            if rd is None: rd = JREAD["learn"] = Journal.reader()
            for ln in rd.new():
                name = ln.name.strip(); text = ln.text.strip()
                if not name and ": " in text: name, text = [s.strip() for s in text.split(": ", 1)]
                if not name or not text: continue
                low = name.lower()
                if KARMA_TAG_RE.match(text):
                    if low not in PLAYER_NAMES:
                        if len(PLAYER_NAMES) >= PLAYER_NAMES_CAP: trim_players(PLAYER_NAMES_CAP - 1)
                        PLAYER_NAMES[low] = name; PLAYER_VER[0] += 1; st["dirty_save"] = True; NPC_CACHE.clear()
                elif text.lower().startswith(low + " the "): capped(TITLED_NPCS); TITLED_NPCS.add(low)
        FRIEND_Q = {}; FRIEND_Q_SECONDS = 1.0; FRIEND_Q_AT = [0.0]
        def is_friend(serial):
            v = FRIEND_Q.get(serial)
            if v is None:
                v = bool(API.IsFriend(serial))
                if len(FRIEND_Q) > 500: FRIEND_Q.clear()
                FRIEND_Q[serial] = v
            return v
        def mflag(m, attr):
            try: return bool(getattr(m, attr))
            except Exception: return False
        def acts_like_player(mob, serial, name, low):
            if low.startswith(TITLE_PREFIXES) or name_key(name) in FOES or low in PLAYER_NAMES or serial in st["party"]:
                return True
            if mflag(mob, "IsRunning") or mflag(mob, "IsMounted") or mflag(mob, "InWarMode"): return True
            return is_friend(serial)
        def is_npc(mob, serial, name):
            if serial in SEEN_PLAYER: return False
            low = name.strip().lower()
            if acts_like_player(mob, serial, name, low):
                capped(SEEN_PLAYER); SEEN_PLAYER.add(serial); NPC_CACHE.pop(serial, None); return False
            if low in npc_names() or low in TITLED_NPCS: return True
            now = time.time(); hit = NPC_CACHE.get(serial)
            if hit is not None and (hit[0] or now - hit[1] < NPC_RECHECK_SECONDS): return hit[0]
            text = name_props(mob); npc = bool(NPC_TITLE_RE.search(text.split("\n")[0] + " " + name))
            capped(NPC_CACHE); NPC_CACHE[serial] = (npc, now); return npc
        def name_props(mob):
            try: return str(mob.NameAndProps(False) or "")
            except Exception: return ""
        def titled_npc(mob, serial, name):
            if serial in SEEN_PLAYER: return False
            low = name.strip().lower()
            if not low: return False
            npc = low in TITLED_NPCS
            if not npc:
                now = time.time(); hit = TITLE_CACHE.get(serial)
                if hit is not None and (hit[0] or now - hit[1] < NPC_RECHECK_SECONDS): npc = hit[0]
                else:
                    first = name_props(mob).split("\n")[0].strip().lower()
                    npc = first.startswith(low + " the "); capped(TITLE_CACHE); TITLE_CACHE[serial] = (npc, now)
            if not npc: return False
            if low in PLAYER_NAMES or name_key(name) in FOES or serial in st["party"] or is_friend(serial): return False
            return True
        def looks_like_player(mob, serial):
            dead = mflag(mob, "IsDead")
            if not dead and not (mflag(mob, "IsHuman") or mflag(mob, "IsGargoyle")): return None
            if mflag(mob, "IsRenamable"): return None
            noto = Kit.noto_name(mob)
            if noto == "invulnerable": return None
            try: name = str(mob.Name or "")
            except Exception: return None
            if noto == "innocent":
                if is_npc(mob, serial, name): return None
            elif not dead and titled_npc(mob, serial, name): return None
            return (noto, dead, name)
        def classify(serial, name, noto, party):
            key = name_key(name)
            if key and key in FOES: return "foe", "L"
            if serial in party: return "friend", "P"
            if is_friend(serial): return "friend", "F"
            if noto == "ally": return "friend", "G"
            if noto == "murderer": return "foe", ""
            if noto == "enemy": return "foe", "W"
            return "neutral", ""
        def classify_service(mob, party):
            try:
                serial = mob.Serial; seen = looks_like_player(mob, serial)
                if seen is None: return None
                noto, dead, name = seen
                if name and name.lower() in IGNORE: return None
                return classify(serial, name, noto, party) + (noto, dead)
            except Exception: return None
        def mobiles_near(): return HOST.mobiles(max(settings["range"], MAX_RANGE))
        def mnum(m, attr):
            try: return getattr(m, attr) or 0
            except Exception: return 0
        def _by_name(e): return e["name"].lower()
        SCANNED = {}; SCANNED_PASS = [None]
        def scanned(serial):
            if SCANNED_PASS[0] is None or not HOST.in_hop or HOST.pass_id != SCANNED_PASS[0]: return None
            return SCANNED.get(serial)
        def scan():
            out = {c: [] for c in CATS}; SCANNED.clear(); SCANNED_PASS[0] = HOST.pass_id if HOST.in_hop else None
            now = time.time()
            if not 0.0 < FRIEND_Q_AT[0] - now <= FRIEND_Q_SECONDS:
                FRIEND_Q.clear(); FRIEND_Q_AT[0] = now + FRIEND_Q_SECONDS
            me = HOST.me(); WATCH["me"] = me
            if me is None: return out
            rng = settings["range"]; mobs = mobiles_near()
            party = set(API.GetPartyMemberSerials() or []); st["party"] = party; learn_from_journal()
            my_serial = me.Serial; mx, my = int(me.X), int(me.Y)
            alert_on = (settings["alert_red"] or settings["alert_foes"] or settings["alert_orange"]
                        or settings["alert_gray"])
            cands = fresh = appeared = foes_here = None; log_on = settings["sightings"]; wins = views["windows"] or {}
            need_hp = {}
            for c in CATS: w = wins.get(c); need_hp[c] = w is None or not (w.minimized and LAYOUT[c][5])
            for m in mobs:
                try:
                    if m is None: continue
                    serial = m.Serial
                    if serial == my_serial: continue
                    ox, oy = int(m.X), int(m.Y); dist = max(abs(ox - mx), abs(oy - my))
                    if dist > rng: continue
                    seen = looks_like_player(m, serial)
                    if seen is None: continue
                    noto, dead, name = seen
                    if name and name.lower() in IGNORE: continue
                    cat, tag = classify(serial, name, noto, party)
                    if cat != "friend" and name:
                        if tag == "L":
                            k = name_key(name)
                            if FOE_SERIALS.get(serial) != k: capped(FOE_SERIALS); FOE_SERIALS[serial] = k
                            if foes_here is None: foes_here = []
                            foes_here.append((k, ox, oy))
                        if log_on:
                            t0 = PRESENT.get(serial)
                            if t0 is None or now - t0 > SIGHT_GONE:
                                if appeared is None: appeared = []
                                appeared.append((serial, name, noto, ox, oy))
                            PRESENT[serial] = now
                        if alert_on and not dead and alert_why(tag, noto) is not None:
                            if cands is None: cands = set()
                            cands.add(serial)
                            if serial not in ALERT_PREV:
                                if fresh is None: fresh = []
                                fresh.append((serial, name, noto, tag, dist, ox - mx, oy - my))
                    if need_hp[cat]:
                        hits, hmax = m.Hits or 0, m.HitsMax or 0; psn, par = bool(m.IsPoisoned), bool(m.IsParalyzed)
                        if len(SCANNED) < CACHE_CAP:
                            SCANNED[serial] = (name, noto, cat, dead, psn, par, hits, hmax, dist)
                    else: hits = hmax = 0; psn = par = False
                    out[cat].append({"serial": serial, "name": name or "(unknown)", "tag": tag, "noto": noto,
                        "hits": hits, "hmax": hmax, "dist": dist, "poisoned": psn, "paralyzed": par, "dead": dead,
                        "mob": m.raw})
                except Exception: continue
            for c in CATS: out[c].sort(key=_by_name)
            ALERT_PREV.clear()
            if cands is not None: ALERT_PREV.update(cands)
            try:
                if foes_here is not None: foes_seen(foes_here, now)
                if fresh is not None: foe_alerts(fresh, now)
                if appeared is not None: log_appeared(appeared, now)
            except Exception as ex: report_error(ex)
            return out
        def alert_why(tag, noto):
            if tag == "L" and settings["alert_foes"]: return "foe"
            if noto == "murderer" and settings["alert_red"]: return "red"
            if noto == "enemy" and settings["alert_orange"]: return "orange"
            if (noto == "gray" or noto == "criminal") and settings["alert_gray"]: return "gray"
            return None
        def foe_alerts(fresh, now):
            gap = settings["alert_minutes"] * 60.0
            for serial, name, noto, tag, dist, dx, dy in fresh:
                t = ALERTED.get(serial)
                if t is not None and now - t < gap: continue
                ALERTED[serial] = now
                HOST.alert(ALERT_KEY, foe_alert_text(name, noto, tag, dist, dx, dy), level="warn", who=serial)
        def foe_alert_text(name, noto, tag, dist, dx, dy):
            lk = link_text(name_key(name)) if tag == "L" else ""; who = "%s (%s)" % (name, lk) if lk else name
            what = noto_word(noto) + (", on your Foe list" if tag == "L" else "")
            return "%s: %s, %s" % (who, what, Kit.where_text(dx, dy, "right here"))
        def map_now(): return int(API.GetMap())
        def guard_now(): return safe(HOST.guarded)
        def held_back(key, serial, again, now=None): return not HOST.harm_ok(serial, key, TITLE, True, again, now=now)
        def log_appeared(appeared, now):
            facet, guard = map_now(), guard_now()
            for serial, name, noto, x, y in appeared: log_sighting(now, serial, name, noto, facet, x, y, guard)
        FOE_WHERE = [-10.0, -1, None]
        def foes_seen(here, now):
            facet = guard = None
            for k, x, y in here:
                old = LAST_SEEN.get(k)
                if facet is None:
                    fg = FOE_WHERE; f = map_now()
                    if f != fg[1] or not 0.0 <= now - fg[0] < 1.0: fg[0], fg[1], fg[2] = now, f, guard_now()
                    facet, guard = fg[1], fg[2]
                LAST_SEEN[k] = (now, facet, x, y, guard)
                if old is None or now - old[0] > SIGHT_GONE:
                    SIGHT["seen_ver"] += 1
                    if not SIGHT["dirty"]: SIGHT["dirty"] = True; SIGHT["save_at"] = now + SIGHT_SAVE_SECONDS
        WATCH = {"dead": None, "prune_at": 0.0, "me": None, "att_at": 0.0, "died_at": 0.0}
        def watch_tick(now):
            if now >= WATCH["prune_at"]: WATCH["prune_at"] = now + 10.0; prune_session(now)
            me = WATCH["me"]; dead = mflag(me, "IsDead") if me is not None else WATCH["dead"]
            was, WATCH["dead"] = WATCH["dead"], dead
            if settings["killer"] and (now >= WATCH["att_at"] or (dead and was is False)):
                WATCH["att_at"] = now + 1.0; note_attackers(now)
            if was is None or dead is None or dead == was: return
            if dead: on_death(now)
            else: KILLER_WIN.end()
        def note_attackers(now):
            rd = JREAD["killer"]
            if rd is None: JREAD["killer"] = Journal.reader(); return
            todo, lows = [], set()
            for ln in rd.new():
                if ln.text.startswith(OWN_PREFIX) or "is attacking you" not in ln.low: continue
                mt = ATTACK_RE.search(ln.text); name = mt.group(1).strip().strip("*").strip() if mt is not None else ""
                if name: todo.append((ln, name)); lows.add(name.lower())
            found = named_mobiles(lows) if lows else None
            for ln, name in todo:
                serial, player = find_named(name, found)
                if player is not False: note_attacker(name, ln.at, serial)
            for s, e in cb_engaged.items():
                m = cb_snap.get(s)
                if m is None: continue
                who = e.get("player")
                if who is None:
                    who = e["player"] = not mflag(m, "IsRenamable") and (mflag(m, "IsHuman") or mflag(m, "IsGargoyle"))
                if who:
                    try: name = str(m.Name or "")
                    except Exception: name = ""
                    if name: note_attacker(name, e["last"], s)
        def named_mobiles(lows):
            out = {}
            for m in mobiles_near():
                try:
                    n = m.Name
                    if not n: continue
                    low = n.strip().lower()
                    if low not in lows or low in out: continue
                    if mflag(m, "IsRenamable"): out[low] = (m.Serial, False)
                    else: out[low] = (m.Serial, mflag(m, "IsHuman") or mflag(m, "IsGargoyle"))
                    if len(out) >= len(lows): break
                except Exception: continue
            return out
        def find_named(name, found=None):
            low = name.lower()
            if found is None: found = named_mobiles((low,))
            hit = found.get(low)
            if hit is not None: return hit
            if low.startswith("a ") or low.startswith("an "): return None, False
            return None, None
        def note_attacker(name, t, serial):
            if t <= WATCH["died_at"]: return False
            if serial is not None and (serial in st["party"] or is_friend(serial)): return False
            low = name.lower(); a = ATTACKERS.get(low)
            if a is None:
                if len(ATTACKERS) >= ATTACKERS_CAP:
                    oldest = None
                    for k, v in ATTACKERS.items():
                        if oldest is None or v[1] < ATTACKERS[oldest][1]: oldest = k
                    ATTACKERS.pop(oldest, None)
                ATTACKERS[low] = [name, t, serial]; return True
            if t > a[1]: a[1] = t
            if serial is not None: a[2] = serial
            return False
        def _newest_first(a): return -a[1]
        def on_death(now):
            WATCH["died_at"] = now
            if not settings["killer"]: ATTACKERS.clear(); return
            cut = now - KILLER_BACK; got = sorted([a for a in ATTACKERS.values() if a[1] >= cut], key=_newest_first)
            ATTACKERS.clear()
            if got: KILLER_WIN.open(got[:KILLER_ROWS], now, len(got))
        def prune_session(now):
            cut = now - SIGHT_GONE
            for s in [s for s, t in PRESENT.items() if t < cut]: del PRESENT[s]
            if ALERTED:
                cut = now - settings["alert_minutes"] * 60.0
                for s in [s for s, t in ALERTED.items() if t < cut]: del ALERTED[s]
            if ATTACKERS:
                cut = now - KILLER_BACK
                for k in [k for k, a in ATTACKERS.items() if a[1] < cut]: del ATTACKERS[k]
        def make_bar_click(serial, name, origin=None):
            def _clicked(*args):
                now = time.time(); prev = LAST_CLICK.get(serial, 0); capped(LAST_CLICK); LAST_CLICK[serial] = now
                if alt_held(): LAST_CLICK[serial] = 0; toggle_follow(serial); return
                if click_can_aim():
                    LAST_CLICK[serial] = 0
                    if HOST.harm_ok(serial, "ultima.aim", TITLE): API.Target(serial)
                    return
                if origin is not None and shift_held(): pop_out(serial, name, origin); LAST_CLICK[serial] = 0; return
                double = now - prev <= DOUBLE_CLICK_SECONDS
                if double: LAST_CLICK[serial] = 0
                API.SetLastTarget(serial=serial)
                if double:
                    if held_back("ultima.attack", serial, "double-click again to attack"): return
                    API.Attack(serial); API.HeadMsg("* attacking *", serial, 0x22)
                else: API.HeadMsg("* last target *", serial, 0x35)
            return _clicked
        def bar_color(cat, poisoned, dead, paralyzed=False):
            if dead: return COL_DEAD
            if cat in ("friend", "combat"):
                if poisoned and paralyzed: return COL_BOTH
                if paralyzed: return COL_PARA
            if poisoned: return COL_POISON
            return BAR_FG[cat]
        def needs_heal(dead, hits, hmax): return not dead and hmax > 0 and hits * 100.0 / hmax <= GLOW_HP_PCT
        def glow_alpha():
            a = GLOW_MIN + (GLOW_MAX - GLOW_MIN) * (0.5 + 0.5 * math.sin(2 * math.pi * time.time() / GLOW_PERIOD))
            return int(a * GLOW_STEPS + 0.5) / float(GLOW_STEPS)
        GLOW_SET = {}
        def pulse_glow(glow, low, a=None):
            if glow is None: return
            if not low: a = 0.0
            elif a is None: a = glow_alpha()
            k = id(glow)
            if GLOW_SET.get(k) == a: return
            if len(GLOW_SET) > 400: GLOW_SET.clear()
            GLOW_SET[k] = a; set_box_alpha(glow, a)
        def hp_text(dead, hits, hmax, poisoned, paralyzed, dist):
            if dead: return "DEAD  %dy" % dist, 0, 1
            if hmax > 0:
                flags = (" PSN" if poisoned else "") + (" PAR" if paralyzed else "")
                return "%d%%%s  %dy" % (int(round(100.0 * hits / hmax)), flags, dist), hits, hmax
            return "--  %dy" % dist, 0, 1
        BAR_PAINT = {BAR_FG["friend"]:  ("#3A86BF", "#13283A"), BAR_FG["neutral"]: ("#7E868F", "#26292C"),
                     BAR_FG["foe"]:     ("#B23C3C", "#3A1616"), BAR_FG["combat"]:  ("#B23C3C", "#3A1616"),
                     COL_POISON:        ("#4A9A55", "#16301A"), COL_PARA:          ("#5A7FCC", "#1A2640"),
                     COL_BOTH:          ("#2E9A90", "#0F302D"), COL_DEAD:          ("#4C4C4C", "#1C1C1C")}
        BAR_EDGE_ALPHA  = 0.85; BAR_TRACK_ALPHA = 0.90; BAR_FILL_ALPHA  = 0.95; BAR_SHEEN_ALPHA = 0.16
        BAR_SHADE_ALPHA = 0.30
        def bar_paint(color): return BAR_PAINT.get(color, (color, "#202020"))
        class HealthBar(object):
            def __init__(self, parent, x, y, w, h, color, cur=0, mx=1):
                self.fw = None; self.parts = []; self.color = color; fill_col, track_col = bar_paint(color)
                edge = 1 if h >= 5 and w >= 8 else 0; self.ix, self.iy = x + edge, y + edge
                self.iw, self.ih = max(1, w - 2 * edge), max(1, h - 2 * edge)
                if edge: self._add(parent, BAR_EDGE_ALPHA, "#000000", x, y, w, h)
                self.track = self._add(parent, BAR_TRACK_ALPHA, track_col, self.ix, self.iy, self.iw, self.ih)
                self.fill = self._add(parent, BAR_FILL_ALPHA, fill_col, self.ix, self.iy, 0, self.ih)
                self.sheen = self.shade = None
                if self.ih >= 6:
                    self.sheen = self._add(parent, BAR_SHEEN_ALPHA, "#FFFFFF", self.ix, self.iy,
                                           0, max(1, self.ih * 2 // 5))
                    sh = max(1, self.ih // 5)
                    self.shade = self._add(parent, BAR_SHADE_ALPHA, "#000000", self.ix, self.iy + self.ih - sh, 0, sh)
                self.SetProgress(cur, mx)
            def _add(self, parent, alpha, color, x, y, w, h):
                b = box(alpha, color); b.SetRect(x, y, w, h); parent.Add(b); self.parts.append(b); return b
            def SetProgress(self, cur, mx):
                fw = int(round(self.iw * clamp(float(cur) / mx, 0.0, 1.0))) if mx > 0 else 0
                if fw == self.fw: return
                self.fw = fw
                for b in (self.fill, self.sheen, self.shade):
                    if b is not None: b.SetWidth(fw)
            def set_color(self, color):
                if color == self.color: return
                fill_col, track_col = bar_paint(color)
                for b, col in ((self.fill, fill_col), (self.track, track_col)):
                    r, g, bl = rgb_of(col); b.SetBaseColor(r, g, bl, 255)
                self.color = color
            def set_visible(self, on):
                for c in self.parts: Kit.set(c, "IsVisible", on)
            def Dispose(self):
                for c in self.parts: drop(c)
                self.parts = []
        class PopBar(object):
            def __init__(self, serial, name, x, y):
                self.serial, self.name, self.x, self.y = serial, name, x, y; self.gump = None
                self.locked = self.minimized = self.opacity_open = False
                self.opacity, self.name_color = settings["opacity"], TEXT_COLOR; self.create()
            def create(self):
                s = settings["scale"] / 100.0; w = sc(POP_W); self.row_h = max(10, sc(16)); self.pad = max(2, sc(5))
                h = 2 * BORDER + title_h(s)
                if self.opacity_open: h += orow_h(s)
                if not self.minimized: h += self.row_h + 2 * self.pad
                self.size = (w, h); self.x, self.y = Kit.clamp(self.x, self.y, w, h)
                g = API.Gumps.CreateModernGump(self.x, self.y, w, h, False, w, h); self.gump = g
                g.SetAlpha(0.0); self.chrome = Chrome(g)
                self.bar = self.info = self.hit = self.glow = None
                self.low, self.spell_ctrls, self.bar_key, self.last = False, [], None, None; self.layout_chrome()
                G.AddGump(g); Kit.on_moved(g, self.moved); ANCHORS.placed(self.anchor_key)
                Kit.set(g, "CanMove", not self.locked)
            @property
            def anchor_key(self): return "pop:%d" % self.serial
            def moved(self): ANCHORS.pending = True
            def layout_chrome(self):
                w, h = self.size; mini, oo = self.minimized, self.opacity_open
                b = [("lock", self.locked, self.toggle_lock, "Unlock (move and resize again)"
                      if self.locked else "Lock in place (no moving or resizing)"),
                     ("min", mini, self.toggle_minimize, "Restore" if mini else Kit.MIN_TIP)]
                if not mini:
                    b.append(("opacity", oo, self.toggle_opacity, "Hide the opacity slider" if oo
                              else "Show the opacity slider (frame and bars stay solid)"))
                b.append(("close", False, self.close, "Close this bar"))
                self.chrome.layout(w, h, settings["scale"] / 100.0, self.opacity, self.name, self.name_color, b,
                                   oo and not mini, self.toggle_minimize, lambda: toggle_follow(self.serial),
                                   self.anchor_key)
            def destroy(self): g, self.gump = self.gump, None; Kit.dispose(g)
            def close(self, *args): POPS.pop(self.serial, None); self.destroy()
            def snapshot(self):
                if Kit.is_open(self.gump): self.x, self.y = self.gump.GetX(), self.gump.GetY()
            def rebuild(self): self.snapshot(); self.destroy(); self.create()
            def set_locked(self, locked):
                self.locked = locked
                if self.gump is not None: Kit.set(self.gump, "CanMove", not locked); self.layout_chrome()
            def toggle_lock(self, *args): self.set_locked(not self.locked)
            def toggle_minimize(self, *args):
                self.minimized = not self.minimized; self.opacity_open = False; self.rebuild()
            def toggle_opacity(self, *args): self.opacity_open = not self.opacity_open; self.rebuild()
            def apply_opacity(self, v):
                self.opacity = v
                if self.gump is not None: self.chrome.set_opacity(v)
            def update(self):
                if not Kit.is_open(self.gump): POPS.pop(self.serial, None); return
                try:
                    v = self.chrome.poll()
                    if v is not None: self.opacity = v
                    self._refresh()
                except Exception as ex:
                    say("closed the health bar for %s (%s)." % (self.name, ex), Kit.HUE_BAD); self.close()
            def _draw_row(self, key):
                color, _, friend = key
                if self.bar is not None: self.bar.Dispose()
                for c in [self.info, self.hit, self.glow] + self.spell_ctrls: drop(c)
                self.spell_ctrls = []; w = self.size[0]; s = settings["scale"] / 100.0
                y = self.chrome.content_top + self.pad
                bw = w - 2 * BORDER - 2 * self.pad; x = BORDER + self.pad
                if friend and friend_button_count():
                    sw = self.row_h; bw -= friend_button_count() * (sw + 2)
                    friend_buttons(self.gump, x + bw + 2, y, sw, self.row_h, self.serial, self.name, self.spell_ctrls)
                self.glow = None
                if friend:
                    gp = max(2, self.pad - 1); self.glow = box(0.0, GLOW_COLOR)
                    self.glow.SetRect(x - gp, y - gp, bw + 2 * gp, self.row_h + 2 * gp); self.gump.Add(self.glow)
                self.bar = HealthBar(self.gump, x, y, bw, self.row_h, color)
                fs = max(8, int(round(12 * text_scale(s))))
                self.info = ttf("", fs, "#FFFFFF", aligned="right", maxWidth=bw - 6, applyStroke=True)
                self.info.SetPos(x + 3, text_y(y, self.row_h, fs)); self.gump.Add(self.info)
                self.hit = catcher(x, y, bw, self.row_h, make_bar_click(self.serial, self.name),
                                   tip_for(TIP_BAR_ROW, self.name))
                self.gump.Add(self.hit); self.bar_key = key; self.last = None
            def pulse(self, a=None):
                if self.gump is not None and not self.minimized: pulse_glow(self.glow, self.low, a)
            def _refresh(self):
                me = HOST.me(); hit = scanned(self.serial) if me is not None else None
                if hit is not None and hit[0]: mob = True
                else:
                    hit = None; mob = HOST.mobile(self.serial)
                if mob is None or me is None:
                    text, cur, mx, key, ncol = ("out of range", 0, 1, (COL_DEAD, False, False), "#888888")
                    self.low = False
                else:
                    if hit is not None: name, noto, cat, dead, poisoned, paralyzed, hits, hmax, dist = hit
                    else:
                        try: name = mob.Name or self.name
                        except Exception: name = self.name
                        noto = Kit.noto_name(mob); cat, _ = classify(self.serial, name, noto, st["party"])
                        dead, poisoned = mflag(mob, "IsDead"), mflag(mob, "IsPoisoned")
                        paralyzed, hits, hmax = mflag(mob, "IsParalyzed"), mnum(mob, "Hits"), mnum(mob, "HitsMax")
                        try: dist = max(abs(int(mob.X) - int(me.X)), abs(int(mob.Y) - int(me.Y)))
                        except Exception: dist = 0
                    key = (bar_color(cat, poisoned, dead, paralyzed), (settings["magery"], settings["healing"]),
                           cat == "friend")
                    self.low = cat == "friend" and needs_heal(dead, hits, hmax); ncol = NOTO_COLOR.get(noto, "#DDDDDD")
                    text, cur, mx = hp_text(dead, hits, hmax, poisoned, paralyzed, dist)
                if Follow.serial == self.serial: text = "FOL " + text
                self.name_color = ncol
                if self.minimized: self.chrome.set_title("%s  %s" % (self.name, text.split("  ")[0]), ncol); return
                self.chrome.set_title(self.name, ncol)
                if key != self.bar_key:
                    old = self.bar_key
                    if old is not None and old[1:] == key[1:] and self.bar is not None:
                        self.bar.set_color(key[0]); self.bar_key = key
                    else: self._draw_row(key)
                if self.last != (text, cur, mx):
                    self.last = (text, cur, mx); set_text(self.info, text); self.bar.SetProgress(float(cur), float(mx))
        def make_npc_click(serial, name):
            def _clicked(*args):
                if not name or name == "(unknown)":
                    say("no name yet; try again in a moment.", Kit.HUE_BAD); return
                IGNORE[name.lower()] = name; save_settings(); pb = POPS.get(serial)
                if pb is not None: pb.close()
                say("%s marked as an NPC and hidden; Unignore the name to undo." % name, Kit.HUE_GOOD)
            return follow_or(serial, _clicked)
        def make_pop_click(serial, name, origin): return follow_or(serial, lambda: pop_out(serial, name, origin))
        def enable_unit_frames(serial, name, origin):
            HOST.enable("unitframes"); TICK_JOBS.append(lambda: pop_out(serial, name, origin, False))
        def pop_out(serial, name, origin, may_enable=True):
            add_frame = HOST.services.get("unitframes.add")
            if add_frame is None and may_enable and "unitframes" in HOST.by_key:
                THREAD_JOBS.append(lambda: enable_unit_frames(serial, name, origin)); return
            if add_frame is not None:
                add_frame(serial)
                say("%s gets a frame in Character HUD > Frames." % name, Kit.HUE_GOOD); return
            existing = POPS.get(serial)
            if existing is not None and Kit.is_open(existing.gump):
                say("a health bar for %s is already open." % name, Kit.HUE_BAD); return
            gx = safe(lambda: origin.gump.GetX(), 300); gy = safe(lambda: origin.gump.GetY(), 300)
            x = gx + origin.size[0] + 6
            y = gy + len(POPS) * (sc(52) + 4); pb = POPS[serial] = PopBar(serial, name, x, y)
            pb.update(); say("popped out a health bar for %s." % name, Kit.HUE_GOOD)
        TIP_BAR_ROW = ("Click: target; double-click: attack (blue or green in guards: twice). "
                       "Alt+click: auto-follow (again to stop)")
        TIP_FOE_ROW = "Click: put the name in the box. Alt+click: auto-follow (again to stop)"
        TIP_SIGHT = ("Click: show only this player (again for everyone). Alt+click: auto-follow (again to stop)")
        class PoolRow(object):
            glow = None; e = None; prev = None
            def parts(self): return self.ctrls
            def set_shown(self, on):
                for c in self.parts(): Kit.set(c, "IsVisible", on)
                self.bar.set_visible(on); self.shown = on
            def hide(self):
                if self.serial is not None: self.prev = (self.serial, self.name, time.time())
                self.serial, self.name = None, ""; self.low = False; self.last = None
                if self.glow is not None: pulse_glow(self.glow, False)
                self.set_shown(False)
        class TrackerRow(PoolRow):
            def __init__(self, view, i, geo, e):
                self.win = view; self.serial, self.name = e["serial"], e["name"]; self.y = y = i * geo["row_h"]
                self.shown, self.low, self.ctrls = True, False, []; self.last = self.raw = self.name_raw = None
                sa, rw = view.sa, geo["rw"]; bg = API.Gumps.CreateGumpColorBox(0.35, "#000000")
                bg.SetRect(0, y, rw, geo["row_h"] - 2)
                on_click(bg, RowClick(self, lambda s, n: make_bar_click(s, n, view)))
                Kit.with_tip(bg, tip_for(TIP_BAR_ROW, self.name)); self.bg = bg; self.glow = None
                if view.cat == "friend": self.glow = box(0.0, GLOW_COLOR); self.glow.SetRect(0, y, rw, geo["row_h"] - 2)
                text, color = row_name(e, geo); self.name_lbl = label(text, geo["name_fs"], color)
                place(self.name_lbl, 4, y + geo["name_dy"]); self.name_key = (text, color)
                pbw, nbw = geo["pbw"], geo["nbw"]
                self.info = label("", geo["info_fs"], "#DDDDDD", aligned="right", maxWidth=rw - 16 - pbw - nbw)
                place(self.info, 4, y + geo["info_dy"])
                for c in (bg, self.glow, self.name_lbl, self.info):
                    if c is not None: sa.Add(c); self.ctrls.append(c)
                flat_button(sa, rw - 8 - pbw - nbw, y + geo["npc_dy"], nbw, nbw, "N", RowClick(self, make_npc_click),
                            "Mark as an NPC and hide (Unignore the name to undo). " + ALT_FOLLOW_TIP,
                            font=geo["npc_fs"], store=self.ctrls)
                flat_button(sa, rw - 4 - pbw, y + geo["pop_dy"], pbw, geo["pop_h"], ">",
                            RowClick(self, lambda s, n: make_pop_click(s, n, view)),
                            "Pop out a health bar (or Shift+click the row). " + ALT_FOLLOW_TIP, font=geo["pop_fs"],
                                store=self.ctrls)
                self.tips = []
                if geo["fbtn"]:
                    self.tips = friend_buttons(sa, 4 + geo["bar_w"] + 2, y + geo["fbtn_dy"],
                                               geo["sb"], geo["sb"], self.serial, self.name, store=self.ctrls, row=self)
                self.bar = HealthBar(sa, 4, y + geo["bar_dy"], geo["bar_w"], geo["bar_h"], row_color(view.cat, e))
            def assign(self, e, geo):
                serial, name = e["serial"], e["name"]
                if serial != self.serial or name != self.name:
                    if serial != self.serial: self.prev = (self.serial, self.name, time.time())
                    self.serial, self.name = serial, name; self.last = None
                    for c, tip in self.tips: Kit.with_tip(c, tip % name)
                    Kit.with_tip(self.bg, tip_for(TIP_BAR_ROW, name))
                if not self.shown: self.set_shown(True)
                nr = (e["name"], e["tag"], e["noto"], geo["name_px"], geo["name_fs"])
                if nr != self.name_raw:
                    text, color = row_name(e, geo)
                    if (text, color) != self.name_key: self.set_name(text, color, geo)
                    self.name_raw = nr
                self.bar.set_color(row_color(self.win.cat, e))
            def set_name(self, text, color, geo):
                lb = self.name_lbl
                if color == self.name_key[1] or set_hue(lb, color): set_text(lb, text)
                else:
                    at = self.ctrls.index(lb); drop(lb); lb = label(text, geo["name_fs"], color)
                    place(lb, 4, self.y + geo["name_dy"]); self.win.sa.Add(lb); self.ctrls[at] = lb; self.name_lbl = lb
                self.name_key = (text, color)
            def values(self, e):
                self.e = e; fol = Follow.serial == e["serial"]
                raw = (e["dead"], e["hits"], e["hmax"], e["poisoned"], e["paralyzed"], e["dist"], fol)
                if self.last is not None and raw == self.raw: return
                self.raw = raw
                text, cur, mx = hp_text(e["dead"], e["hits"], e["hmax"], e["poisoned"], e["paralyzed"], e["dist"])
                if fol: text = "FOL " + text
                self.low = needs_heal(e["dead"], e["hits"], e["hmax"])
                if self.last != (text, cur, mx):
                    self.last = (text, cur, mx); set_text(self.info, text); self.bar.SetProgress(float(cur), float(mx))
            def forget(self):
                for c in self.ctrls: LABELS.pop(id(c), None)
                self.ctrls = []; self.serial = None
        def row_name(e, geo):
            text = cut_text(e["name"], geo["name_px"], geo["name_fs"])
            if e["tag"]: text += "  [" + e["tag"] + "]"
            return text, NOTO_COLOR.get(e["noto"], "#DDDDDD")
        def row_color(cat, e): return bar_color(cat, e["poisoned"], e["dead"], e["paralyzed"])
        class PoolWin(object):
            def show_empty(self, on):
                if on and self.empty is None: self.empty = self.make_empty(); self.empty_shown = True
                elif self.empty is not None and on != self.empty_shown:
                    for lb in self.empty: Kit.set(lb, "IsVisible", on)
                    self.empty_shown = on
            def fill(self, data):
                rows, geo, n = self.rows, self.geo, len(data)
                for i, e in enumerate(data):
                    if i < len(rows): rows[i].assign(e, geo)
                    else: rows.append(self.Row(self, i, geo, e))
                for r in rows[n:]:
                    if r.shown: r.hide()
                self.show_empty(n == 0)
                for r, e in zip(rows, data): r.values(e)
            def destroy(self): g, self.gump = self.gump, None; Kit.dispose(g)
            def moved(self): ANCHORS.pending = True; self.snapshot(); save_settings()
            @property
            def dock_key(self): return "ultima." + self.cat
            def user_minimize(self, *args): HOST.dock_forget(self.dock_key); self.toggle_minimize()
            def apply_opacity(self, v):
                LAYOUT[self.cat][6] = v
                if Kit.is_open(self.gump) and self.chrome is not None: self.chrome.set_opacity(v)
        class CategoryGump(PoolWin):
            Row = TrackerRow
            def __init__(self, cat):
                self.cat, self.rows = cat, []; self.gump = self.chrome = self.sa = self.made_min = None
                self.locked = self.minimized = self.docked = False; self.create()
            def create(self):
                x, y, w, h, locked, mini, _ = LAYOUT[self.cat]; self.minimized = mini; lo_w, lo_h = sc(MIN_W), sc(MIN_H)
                slot = FIT["size"].get(self.cat); held = HOST.layout_holds(self.dock_key)
                if slot is not None:
                    lo_w = min(lo_w, slot[0]); lo_h = min(lo_h, slot[1]); w = slot[0]
                    if not mini: h = slot[1]
                w = max(w, lo_w)
                if mini: gh = KIT_MINI_H; min_h, resizable = gh, False
                else: gh = max(h, lo_h); min_h, resizable = lo_h, slot is None
                self.made_min = (lo_w, lo_h); self.resized_flag = self.user_resize_pending = False
                self.sync_target, self.user_resize_ticks = None, 0
                if not held: x, y = Kit.clamp(x, y, w, gh); LAYOUT[self.cat][0], LAYOUT[self.cat][1] = x, y
                self.gump = API.Gumps.CreateModernGump(x, y, w, gh, resizable, lo_w, min_h, self._on_resized)
                self.gump.SetAlpha(0.0); self.chrome = Chrome(self.gump, kit=True, key=self.dock_key)
                self._forget_body(); self.size = (w, gh); self.count_n = 0; self.locked = locked; self.layout_chrome()
                G.AddGump(self.gump); Kit.on_moved(self.gump, self.moved); ANCHORS.placed(self.cat)
                self._apply_lock()
                if self.docked and mini: Kit.set(self.gump, "IsVisible", False)
            def layout_fit(self, w, h, mode):
                cat = self.cat
                if w is None or h is None:
                    if cat in FIT["size"]: FIT["size"][cat] = None
                    FIT["force"].discard(cat)
                else:
                    FIT["size"][cat] = (int(w), int(h))
                    if mode == "again": FIT["force"].add(cat)
                FIT["req"] = True
            def _forget_body(self):
                for r in self.rows: r.forget()
                self.rows = []; self.sa = self.empty = self.geo = self.body_key = None
            def layout_chrome(self):
                w, h = self.size; c = self.cat
                self.chrome.layout_kit(w, h, LAYOUT[c][6], TITLES[c], TITLE_COLOR[c], self.minimized,
                                       self.user_minimize, lambda *a: DOCK_REQ.append(self.dock_key))
                self.chrome.set_status(str(max(0, self.count_n)))
            def zone_chrome(self):
                if Kit.is_open(self.gump) and self.chrome is not None: self.layout_chrome()
            def _on_resized(self, *args): self.resized_flag = True
            def set_count(self, n):
                if n == self.count_n: return
                self.count_n = n; self.chrome.set_status(str(max(0, n)))
            def _apply_lock(self):
                locked = self.locked; zoned = FIT["size"].get(self.cat) is not None
                held = HOST.layout_holds(self.dock_key)
                if not held: Kit.set(self.gump, "CanMove", not locked)
                self.gump.SetResizable(not locked and not self.minimized and not zoned)
                LAYOUT[self.cat][4] = locked; st["dirty_save"] = True
            def set_locked(self, locked): self.locked = locked; self._apply_lock()
            def toggle_minimize(self, *args):
                self.snapshot(); LAYOUT[self.cat][5] = not self.minimized
                if not LAYOUT[self.cat][5]: self.docked = False
                self.destroy(); self.create(); st["dirty_save"] = True
            def geometry(self):
                w, h = self.size; ix = Kit.MARGIN + 4; sa_w = max(40, w - 2 * ix); rw = max(60, sa_w - SCROLLBAR)
                name_fs = tsc(13)
                g = {"sa": (ix, self.chrome.content_top + sc(4), sa_w,
                            max(20, h - self.chrome.content_top - sc(4) - ix)),
                     "rw": rw, "row_h": sc(ROW_H), "name_fs": name_fs, "info_fs": tsc(12),
                     "name_px": max(30, int(rw / 1.2)), "name_dy": sc(1), "info_dy": sc(2),
                     "pbw": sc(POP_BTN_W), "nbw": sc(NPC_BTN_W), "npc_dy": sc(3), "npc_fs": tsc(10),
                     "pop_dy": sc(1), "pop_h": sc(16), "pop_fs": tsc(12),
                     "fbtn": self.cat == "friend" and friend_button_count() > 0, "sb": sc(13), "fbtn_dy": sc(16)}
                bar_w = rw - 8
                if g["fbtn"]: bar_w -= friend_button_count() * (g["sb"] + 2)
                g["bar_w"], g["bar_dy"], g["bar_h"] = bar_w, sc(18), max(3, sc(10)); return g
            def build_body(self):
                Kit.dispose(self.sa)
                self._forget_body(); self.geo = geo = self.geometry(); x, y, w, h = geo["sa"]
                self.sa = API.Gumps.CreateGumpScrollArea(x, y, w, h); self.gump.Add(self.sa)
            def make_empty(self):
                lines = empty_lines("No players in range.", self.geo["rw"] - 8); return add_empty(self.sa, lines, 4, 4)
            def update(self, entries):
                if not Kit.is_open(self.gump): self.create()
                if not self.minimized:
                    w, h = int(self.gump.GetWidth()), int(self.gump.GetHeight())
                    if (w <= 0 or h <= 0) and self.size: w, h = self.size
                    if (w, h) != self.size or self.resized_flag:
                        self.resized_flag = False; self.size = (w, h)
                        ANCHORS.placed(self.cat, self.gump.GetX(), self.gump.GetY(), w, h)
                        self.layout_chrome(); self.body_key = None
                        if self.sync_target == (w, h) or FIT["size"].get(self.cat) is not None: self.sync_target = None
                        else: self.user_resize_pending = True; self.user_resize_ticks = 0
                    elif self.user_resize_pending: self.user_resize_ticks += 1
                    slot = FIT["size"].get(self.cat)
                    if slot is not None and (w, h) != slot: FIT["req"] = True
                self.set_count(len(entries))
                if self.minimized: return
                key = (self.size, self.chrome.content_top, settings["scale"], settings["magery"], settings["healing"])
                if key != self.body_key: self.build_body(); self.body_key = key
                self.fill(entries)
            def pulse(self, a=None):
                if self.cat != "friend" or self.minimized: return
                for row in self.rows:
                    if row.shown: pulse_glow(row.glow, row.low, a)
            def resize_to(self, w, h):
                if not self.minimized:
                    if self.size == (w, h): return
                    self.sync_target = (w, h); self.gump.SetWidth(w); self.gump.SetHeight(h)
                    if (self.gump.GetWidth(), self.gump.GetHeight()) == (w, h): return
                self.snapshot(); LAYOUT[self.cat][2], LAYOUT[self.cat][3] = w, h; self.destroy(); self.create()
            def snapshot(self):
                if not Kit.is_open(self.gump): return
                L = LAYOUT[self.cat]; L[0], L[1], L[2] = self.gump.GetX(), self.gump.GetY(), self.size[0]
                if not self.minimized: L[3] = self.size[1]
        def refresh(windows):
            for w in windows.values(): w.destroy()
            for w in windows.values(): w.create()
            for p in list(POPS.values()): p.rebuild()
        def redo_look():
            if views["windows"] is not None:
                for w in views["windows"].values(): w.snapshot()
                refresh(views["windows"])
            if views["combat"] is not None: views["combat"].relayout = True
        def sync_sizes(windows, source):
            if source.minimized: w, h = LAYOUT[source.cat][2], LAYOUT[source.cat][3]
            else: w, h = source.size
            for t in windows.values():
                if t is source or t.locked or FIT["size"].get(t.cat) is not None: continue
                t.resize_to(w, h)
            st["dirty_save"] = True
        def process_size_sync(windows):
            for w in windows.values():
                if not settings["sync"]: w.user_resize_pending = False
                elif w.user_resize_pending and w.user_resize_ticks >= 2:
                    if drag_on(): return
                    w.user_resize_pending = False; sync_sizes(windows, w); return
        def apply_scale(new_scale, windows):
            old = settings["scale"]
            if new_scale == old: return
            ratio = float(new_scale) / old
            for w in windows.values():
                w.snapshot(); L = LAYOUT[w.cat]; L[2] = max(sc(MIN_W, new_scale), int(round(L[2] * ratio)))
                L[3] = max(sc(MIN_H, new_scale), int(round(L[3] * ratio)))
            settings["scale"] = new_scale; refresh(windows); st["dirty_save"] = True
        def fit_tick(windows):
            if not FIT["req"]: return
            FIT["req"] = False; busy = drag_on()
            for cat, want in list(FIT["size"].items()):
                view = windows.get(cat)
                if view is None or view.gump is None: continue
                if want is None:
                    if busy: FIT["req"] = True; continue
                    FIT["size"].pop(cat, None); own = FIT["own_size"].pop(cat, None)
                    if view.made_min is not None and view.made_min != (sc(MIN_W), sc(MIN_H)):
                        view.snapshot()
                        if own is not None: LAYOUT[cat][2], LAYOUT[cat][3] = own
                        view.destroy(); view.create()
                    elif own is not None and own != (LAYOUT[cat][2], LAYOUT[cat][3]): view.resize_to(own[0], own[1])
                    FIT["made"].pop(cat, None)
                    if view.gump is not None: view._apply_lock()
                    continue
                if cat not in FIT["own_size"]: FIT["own_size"][cat] = (LAYOUT[cat][2], LAYOUT[cat][3])
                w, h = want; force = cat in FIT["force"]
                if view.minimized:
                    if LAYOUT[cat][2] != w or (view.size and view.size[0] != w):
                        if busy: FIT["req"] = True; continue
                        view.resize_to(w, LAYOUT[cat][3])
                    FIT["force"].discard(cat); continue
                real = (int(view.gump.GetWidth()), int(view.gump.GetHeight()))
                if real[0] <= 0 or real[1] <= 0: FIT["force"].discard(cat); continue
                made = FIT["made"].get(cat); tries = made[1] if made is not None and made[0] == (w, h) else 0
                if real == (w, h) and view.size == (w, h): tries = 0; FIT["made"].pop(cat, None)
                if (force or view.size != (w, h) or real != (w, h) or view.made_min[0] > w or view.made_min[1] > h) \
                        and (force or tries < FIT_TRIES):
                    if busy: FIT["req"] = True; continue
                    FIT["force"].discard(cat); FIT["made"][cat] = ((w, h), tries + 1); view.snapshot()
                    LAYOUT[cat][2], LAYOUT[cat][3] = w, h; view.destroy(); view.create()
                else: FIT["force"].discard(cat)
        ATTACK_RE = Journal.ATTACK_RE
        HOSTILE_INTS = [int(n) for n in HOSTILE_NOTO]; cb_engaged = {}; cb_order_counter = [0]; cb_pending_click = []
        cb_snap = {}; cb_pending_spell = []
        cb_casting = {"serial": None, "until": 0.0, "harmful": True, "stale": False}
        def cb_mob_ok(m):
            try: return m is not None and not m.IsDead
            except Exception: return False
        def cb_dist(m):
            try: return int(m.Distance)
            except Exception: return 0
        def cb_attackable(m, attacked_me=False):
            if mflag(m, "IsRenamable"): return False
            noto = Kit.noto_name(m); return noto not in NEVER_SHOW_NOTO and (attacked_me or noto not in FRIENDLY_NOTO)
        def cb_engage(serial, t=None):
            e = cb_engaged.get(serial)
            if not e:
                me = HOST.me()
                if me is None or serial == me.Serial: return
            if serial in st["party"] or is_friend(serial): return
            t = t or time.time()
            if e: e["last"] = t
            elif len(cb_engaged) < MAX_BARS:
                cb_order_counter[0] += 1; cb_engaged[serial] = {"last": t, "hits": None, "order": cb_order_counter[0]}
        ATTACK_BACK = 5.0
        def cb_scan_journal():
            rd = JREAD["attack"]
            if rd is None: JREAD["attack"] = Journal.reader(); return
            cut, names = time.time() - ATTACK_BACK, set()
            for ln in rd.new():
                if ln.at >= cut and "is attacking you" in ln.low:
                    m = ATTACK_RE.search(ln.text)
                    if m: names.add(m.group(1).strip().lower())
            if not names: return
            found = {}
            for m in mobiles_near():
                try:
                    n = m.Name
                    if n:
                        low = n.strip().lower()
                        if low in names and cb_attackable(m, attacked_me=True): found.setdefault(low, []).append(m)
                except Exception: pass
            for mobs in found.values():
                if len(mobs) == 1: cb_engage(mobs[0].Serial); continue
                picked = [m for m in mobs if cb_attackable(m) or mflag(m, "InWarMode")] or [min(mobs, key=cb_dist)]
                for m in picked: cb_engage(m.Serial)
        LT_SKIP_SECONDS = 0.5; LT_SKIP = {"serial": None, "until": 0.0}
        def cb_scan_last_target():
            s = API.LastTargetSerial; me = HOST.me()
            if not s or me is None or s == me.Serial or s in cb_engaged: return
            if settings["combat_only"] and not me.InWarMode: return
            now = time.time(); sk = LT_SKIP
            if sk["serial"] == s and 0.0 <= sk["until"] - now <= LT_SKIP_SECONDS: return
            m = API.FindMobile(s)
            if cb_mob_ok(m) and cb_dist(m) <= COMBAT_RANGE and cb_attackable(m): sk["serial"] = None; cb_engage(s)
            else: sk["serial"], sk["until"] = s, now + LT_SKIP_SECONDS
        def cb_scan_warmode_hostiles():
            rng = MELEE_RANGE if settings["combat_only"] else COMBAT_RANGE
            for m in HOST.mobiles(rng):
                try:
                    if int(m.Notoriety) in HOSTILE_INTS and m.InWarMode \
                            and not m.IsDead and not mflag(m, "IsRenamable"):
                        cb_engage(m.Serial)
                except Exception: pass
        def cb_prune_and_refresh():
            t = time.time(); cb_snap.clear(); rows = []
            for s in list(cb_engaged.keys()):
                e = cb_engaged[s]; m = API.FindMobile(s)
                if not cb_mob_ok(m): del cb_engaged[s]; continue
                d = cb_dist(m)
                if d > MAX_RANGE: del cb_engaged[s]; continue
                try: h = m.Hits
                except Exception: del cb_engaged[s]; continue
                if e["hits"] is not None and h < e["hits"]: e["last"] = t
                e["hits"] = h; n = None
                try:
                    if d <= COMBAT_RANGE and m.InWarMode:
                        n = m.Notoriety
                        if int(n) in HOSTILE_INTS: e["last"] = t
                except Exception: pass
                if t - e["last"] > IDLE_TIMEOUT: del cb_engaged[s]; continue
                cb_snap[s] = m
                try:
                    name, hm = m.Name or "???", m.HitsMax; psn, par = bool(m.IsPoisoned), bool(m.IsParalyzed)
                    rows.append((e["order"], s, name, Kit.noto_name(m) if n is None else Kit.noto_of(n), h, hm, psn,
                        par))
                except Exception: continue
            rows.sort(); return [r[1:] for r in rows]
        def cb_make_click(serial):
            def _cb(*args): cb_pending_click.append((serial, alt_held(), time.time()))
            return _cb
        def cb_handle_clicks():
            while cb_pending_click:
                s, alt, at = cb_pending_click.pop(0); m = API.FindMobile(s)
                if not m: continue
                if alt: toggle_follow(s); continue
                if click_can_aim():
                    if not HOST.harm_ok(s, "ultima.aim", TITLE, now=at): continue
                    API.Target(s)
                else:
                    if held_back("ultima.attack", s, "click the bar again to attack", at): continue
                    API.Attack(s)
                cb_engage(s)
        def cb_make_spell_click(spell, serial):
            def _cb(*args):
                if alt_held(): cb_pending_click.append((serial, True, time.time())); return
                cb_pending_spell.append((spell, serial, True, time.time()))
            return _cb
        def make_heal_click(serial, spell, stronger):
            return follow_or(serial, lambda: cb_pending_spell.append((stronger if shift_held() else spell, serial,
                                                                      False, time.time())))
        def handle_spells():
            if cb_pending_spell:
                spell, s, harmful, t0 = cb_pending_spell[-1]
                if cursor_owner() is not None:
                    if time.time() - t0 > CAST_TIMEOUT:
                        del cb_pending_spell[:]; say("target cursor busy; %s not cast." % spell, Kit.HUE_BAD)
                else:
                    del cb_pending_spell[:]; m = API.FindMobile(s)
                    if m and harmful and held_back("ultima.cast", s, "click the button again to cast", t0): m = None
                    if m:
                        stale = bool(API.HasTarget("any"))
                        if stale and cb_casting["serial"] is not None and not cb_casting["stale"] \
                                and API.HasTarget("harmful" if cb_casting["harmful"] else "beneficial"):
                            API.CancelTarget(); stale = False
                        API.CastSpell(spell)
                        cb_casting.update(serial=s, harmful=harmful, stale=stale, until=time.time() + CAST_TIMEOUT)
                        claim_cursor("spell", CAST_TIMEOUT)
                        if harmful: cb_engage(s)
            if cb_casting["serial"] is None: release_cursor("spell"); return
            if time.time() > cb_casting["until"]: cb_casting["serial"] = None; release_cursor("spell"); return
            if cb_casting["stale"]:
                if not API.HasTarget("any"): cb_casting["stale"] = False
                return
            if cursor_owner() is not None: return
            if API.HasTarget("harmful" if cb_casting["harmful"] else "beneficial"):
                s = cb_casting["serial"]; cb_casting["serial"] = None; release_cursor("spell")
                if API.FindMobile(s): API.Target(s)
                else: API.CancelTarget()
        def cb_info_text(serial, hits, hm, psn, par):
            pct = "?" if not hm or hm <= 1 else str(int(round(hits * 100.0 / hm))) + "%"
            tags = "FOL " if Follow.serial == serial else ""
            if psn: tags += "PSN "
            if par: tags += "PAR "
            return tags + pct
        TIP_CB = "Attack or aim at %s (blue or green in guards: twice). " + ALT_FOLLOW_TIP
        CB_SPELLS = ((SPELL_POISON, "P", COL_POISON, "Cast Poison on %s. Alt+click: auto-follow (again to stop)"),
                     (SPELL_PARALYZE, "Z", COL_PARA, "Cast Paralyze on %s. Alt+click: auto-follow (again to stop)"))
        CB_X = Kit.MARGIN + 4
        class CombatSlot(PoolRow):
            def __init__(self, view, i, geo, d):
                self.win = view; g = view.gump; serial, name, noto, hits, hmr, psn, par = d
                self.serial, self.name = serial, name; self.y = ry = geo["y"] + i * (geo["rh"] + CB_ROW_GAP)
                self.shown, self.ctrls, self.tips = True, [], []
                self.bar = HealthBar(g, CB_X, ry, geo["bar_w"], geo["rh"],
                                     bar_color("combat", psn, False, par), hits, hmr if hmr else 1)
                self.name_lbl = self.info = self.name_key = self.info_text = self.name_raw = self.info_raw = None
                self._texts(d, geo)
                c = catcher(CB_X, ry, geo["bar_w"], geo["rh"], RowClick(self, lambda s, n: cb_make_click(s)),
                            tip_for(TIP_CB % name, name))
                g.Add(c); self.ctrls.append(c); self.tips.append((c, TIP_CB))
                if settings["magery"]:
                    bx = CB_X + geo["bar_w"] + 1
                    for spell, txt, col, tip in CB_SPELLS:
                        parts = []
                        flat_button(g, bx, ry, geo["spell_w"], geo["rh"], txt,
                                    RowClick(self, (lambda sp: lambda s, n: cb_make_spell_click(sp, s))(spell)),
                                    tip % name, face=col, color="#FFFFFF", font=max(7.0, geo["font"] - 1), store=parts)
                        self.ctrls.extend(parts); self.tips.append((parts[-1], tip)); bx += geo["spell_w"] + 1
            def _texts(self, d, geo):
                g = self.win.gump; serial, name, noto, hits, hmr, psn, par = d; font = geo["font"]
                ty = text_y(self.y, geo["rh"], font)
                if self.name_lbl is None:
                    text = cut_text(name, geo["name_w"], font, True); color = NOTO_COLOR.get(noto, "#FFFFFF")
                    nl = ttf(text, font, color, applyStroke=True); nl.SetPos(CB_X + 3, ty); g.Add(nl)
                    self.name_lbl, self.name_key = nl, (text, color); self.name_raw = (name, noto, geo["name_w"], font)
                if self.info is None:
                    text = cb_info_text(serial, hits, hmr if hmr else 1, psn, par)
                    info = ttf(text, font, "#FFFFFF", aligned="right", maxWidth=geo["info_w"], applyStroke=True)
                    info.SetPos(CB_X + geo["bar_w"] - geo["info_w"] - 3, ty); g.Add(info)
                    self.info, self.info_text = info, text
            def assign(self, d, geo):
                serial, name, noto, hits, hmr, psn, par = d
                if serial != self.serial or name != self.name:
                    if serial != self.serial: self.prev = (self.serial, self.name, time.time())
                    self.serial, self.name = serial, name
                    for i, (c, tip) in enumerate(self.tips):
                        Kit.with_tip(c, tip_for(tip % name, name) if i == 0 else tip % name)
                if not self.shown: self.set_shown(True)
                self.bar.set_color(bar_color("combat", psn, False, par))
                font = geo["font"]; nr = (name, noto, geo["name_w"], font)
                if self.name_lbl is not None and nr != self.name_raw:
                    nk = (cut_text(name, geo["name_w"], font, True), NOTO_COLOR.get(noto, "#FFFFFF"))
                    if nk != self.name_key:
                        if nk[1] == self.name_key[1]: set_text(self.name_lbl, nk[0]); self.name_key = nk
                        else: drop(self.name_lbl); self.name_lbl = None
                    self.name_raw = nr
                self._texts(d, geo)
            def values(self, d):
                self.e = d
                serial, name, noto, hits, hmr, psn, par = d; hm = hmr if hmr else 1; self.bar.SetProgress(hits, hm)
                rk = (serial, hits, hm, psn, par, Follow.serial == serial)
                if rk != self.info_raw:
                    self.info_raw = rk; text = cb_info_text(serial, hits, hm, psn, par)
                    if text != self.info_text: self.info_text = text; set_text(self.info, text)
            def parts(self): return [self.name_lbl, self.info] + self.ctrls
            def dispose(self):
                for c in self.parts(): drop(c)
                self.bar.Dispose()
        class CombatWindow(PoolWin):
            Row = CombatSlot
            def __init__(self):
                self.gump = self.chrome = self.slot = None; self.relayout = self.zone_redraw = self.docked = False
                self.made_min = CB_MIN_WIDTH; self.cat = "combat"; self._forget()
            def layout_fit(self, w, h, mode):
                slot = (int(w), int(h)) if w and h else None
                if slot != self.slot or mode == "again": self.slot = slot; self.relayout = self.zone_redraw = True
            def width(self): return self.slot[0] if self.slot is not None else LAYOUT["combat"][2]
            def zone_chrome(self): self.relayout = True
            def _forget(self):
                self.rows, self.grip, self.empty_lines = [], [], []
                self.empty = self.frame_key = self.geo = self.fit_n = None; self.empty_shown = False
            @property
            def minimized(self): return bool(LAYOUT["combat"][5])
            def is_open(self): return Kit.is_open(self.gump)
            def show(self):
                if self.is_open(): return
                L = LAYOUT["combat"]; L[2] = clamp(L[2], CB_MIN_WIDTH, CB_MAX_WIDTH)
                held = HOST.layout_holds(self.dock_key)
                if not held: L[0], L[1] = Kit.clamp(L[0], L[1], self.width(), self.height(0))
                self.made_min = min(CB_MIN_WIDTH, self.width())
                g = API.Gumps.CreateModernGump(L[0], L[1], self.width(), self.height(0), True,
                                               self.made_min, 16, self._on_resized)
                g.SetAlpha(0.0); self.gump = g; self._forget(); G.AddGump(g)
                Kit.on_moved(g, self.moved); ANCHORS.placed("combat")
                if not held: settings["combat_shown"] = True; st["dirty_save"] = True
                self.apply_lock(); self.draw(cb_prune_and_refresh())
            def hide(self):
                self.snapshot(); Kit.dispose(self.gump)
                self.gump = None; self._drop_notes(); settings["combat_shown"] = False; st["dirty_save"] = True
                if self.docked: self.docked = False; HOST.dock_forget(self.dock_key)
            def _drop_notes(self):
                for sl in self.rows: LABELS.pop(id(sl.name_lbl), None); LABELS.pop(id(sl.info), None)
                self._forget()
            def snapshot(self):
                if self.is_open():
                    L = LAYOUT["combat"]; L[0], L[1] = self.gump.GetX(), self.gump.GetY()
            def reset(self):
                LAYOUT["combat"] = list(DEFAULT_LAYOUT["combat"])
                if self.is_open():
                    L = LAYOUT["combat"]; g = self.gump; g.SetPos(L[0], L[1]); Kit.moved_by_code(g)
                    ANCHORS.placed("combat"); self.apply_lock(); self.relayout = True
                else: self.show()
            def metrics(self):
                s = clamp(self.width(), CB_MIN_WIDTH, CB_MAX_WIDTH) / float(BASE_WIDTH)
                return s, max(10, int(round(BASE_ROW_H * s))), BASE_FONT * text_scale(s)
            def height(self, n):
                if self.slot is not None and not LAYOUT["combat"][5]: return self.slot[1]
                _, rh, _ = self.metrics()
                if LAYOUT["combat"][5]: return KIT_MINI_H
                h = KIT_HEAD + Kit.MARGIN
                if n <= 0 and self.empty_lines:
                    return h + max(rh + CB_ROW_GAP, 2 + EMPTY_PITCH * len(self.empty_lines)) + CB_FOOTER_H
                return h + max(n, 1) * (rh + CB_ROW_GAP) + CB_FOOTER_H
            def _empty_text(self, W):
                width = max(20, W - 2 * CB_X - 4); lines = empty_lines("No one is fighting you.", width)
                if self.slot is not None:
                    cap = max(1, (self.slot[1] - Kit.MARGIN - KIT_HEAD - 2) // EMPTY_PITCH)
                    if len(lines) > cap: lines = lines[:cap - 1] + [Kit.fit(" ".join(lines[cap - 1:]), width)]
                return lines
            def _on_resized(self, *args):
                if not self.is_open() or self.slot is not None: return
                w = clamp(int(self.gump.GetWidth()), CB_MIN_WIDTH, CB_MAX_WIDTH)
                if w == LAYOUT["combat"][2]: return
                LAYOUT["combat"][2] = w; self.relayout = True
            def apply_lock(self):
                if not self.is_open(): return
                g, locked = self.gump, LAYOUT["combat"][4]; held = HOST.layout_holds(self.dock_key)
                if not held: Kit.set(g, "CanMove", not locked)
                g.SetResizable(not locked and not held)
            def set_locked(self, locked):
                if LAYOUT["combat"][4] != locked:
                    LAYOUT["combat"][4] = locked; self.apply_lock(); self.relayout = True; st["dirty_save"] = True
            def toggle_minimize(self, *args):
                LAYOUT["combat"][5] = not LAYOUT["combat"][5]
                if not LAYOUT["combat"][5]: self.docked = False
                self.relayout = True; st["dirty_save"] = True
            def status_text(self, data):
                n = len(data)
                if not LAYOUT["combat"][5] or n == 0: return "%d" % n
                low, psn_n, par_n = None, 0, 0
                for serial, name, noto, h, hm, psn, par in data:
                    psn_n += psn; par_n += par
                    if hm: pct = int(round(h * 100.0 / hm)); low = pct if low is None else min(low, pct)
                parts = ["%d" % n]
                if low is not None: parts.append("low %d%%" % low)
                if psn_n: parts.append("PSN %d" % psn_n)
                if par_n: parts.append("PAR %d" % par_n)
                return "  ".join(parts)
            def build_frame(self, data):
                g = self.gump
                if self.chrome is not None and self.chrome.gump is g: self.chrome.dispose()
                for sl in self.rows: sl.dispose()
                for c in self.grip: drop(c)
                for c in self.empty or (): drop(c)
                g.Clear(); self._forget(); L = LAYOUT["combat"]; mini = L[5]; s, rh, font = self.metrics()
                W = self.width(); n = len(data)
                if not mini: self.empty_lines = self._empty_text(W)
                H = self.height(n); g.SetWidth(W); g.SetHeight(H); self.fit_n = n; ANCHORS.sized("combat", W, H)
                self.chrome = Chrome(g, kit=True, key="ultima.combat")
                self.chrome.layout_kit(W, H, L[6], "Combat", TITLE_COLOR["combat"], mini, self.user_minimize,
                                       lambda *a: DOCK_REQ.append("ultima.combat"))
                self.chrome.set_status(self.status_text(data))
                if mini: return
                inner_w = W - 2 * CB_X; info_w = int(round(80 * s)); spell_w = max(14, rh) if settings["magery"] else 0
                bar_w = inner_w - (2 * (spell_w + 1) if settings["magery"] else 0)
                self.geo = {"y": self.chrome.content_top, "rh": rh, "font": font,
                            "info_w": info_w, "spell_w": spell_w, "bar_w": bar_w, "name_w": bar_w - info_w - 6, "W": W}
                if L[4]: return
                gx, gy = W - Kit.MARGIN - 9, H - Kit.MARGIN - 9
                for dx, dy in GRIP_DOTS:
                    d = box(1.0, GRIP_COLOR); d.SetRect(gx + dx, gy + dy, 2, 2); g.Add(d); self.grip.append(d)
            def fit(self, n):
                n = max(n, 0)
                if n == self.fit_n: return
                self.fit_n = n; W, H = self.geo["W"], self.height(n); self.gump.SetHeight(H)
                ANCHORS.sized("combat", W, H); self.chrome.frame.layout(W, H)
                gx, gy = W - Kit.MARGIN - 9, H - Kit.MARGIN - 9
                for (dx, dy), d in zip(GRIP_DOTS, self.grip): d.SetRect(gx + dx, gy + dy, 2, 2)
            def make_empty(self): return add_empty(self.gump, self.empty_lines or [""], CB_X + 4, self.geo["y"] + 2)
            def fill(self, data):
                if self.slot is not None:
                    geo = self.geo; room = self.slot[1] - geo["y"] - Kit.MARGIN - CB_FOOTER_H
                    cap = max(1, room // max(1, geo["rh"] + CB_ROW_GAP))
                    if len(data) > cap: data = data[:cap]
                self.fit(len(data)); PoolWin.fill(self, data)
            def draw(self, data):
                L = LAYOUT["combat"]; key = (L[2], L[5], L[4], settings["magery"], self.slot)
                if self.zone_redraw and self.frame_key is not None and drag_on():
                    if self.chrome is not None: self.chrome.set_status(self.status_text(data))
                    if key == self.frame_key and not L[5] and self.geo is not None: self.fill(data)
                    return
                if self.relayout or key != self.frame_key:
                    self.relayout = self.zone_redraw = False; self.build_frame(data); self.frame_key = key
                elif self.chrome is not None:
                    self.chrome.set_title("Combat"); self.chrome.set_status(self.status_text(data))
                if not L[5]: self.fill(data)
            def tick(self):
                g = self.gump
                if g is None: del cb_pending_click[:]; return
                if stopping(): return
                if not Kit.is_open(g):
                    self.gump = None; self._drop_notes()
                    if HOST.layout_holds(self.dock_key): return
                    settings["combat_shown"] = False; st["dirty_save"] = True
                    say("combat bars hidden; Show combat in the %s window brings them back." % TITLE, Kit.HUE_INFO)
                    return
                if ((self.made_min > self.slot[0]) if self.slot is not None
                        else (self.made_min < CB_MIN_WIDTH)) and not drag_on():
                    self.snapshot(); self.gump = None; self._drop_notes(); Kit.dispose(g); self.show()
                    if self.docked: Kit.set(self.gump, "IsVisible", False)
                    return
                cb_handle_clicks(); cb_scan_journal(); cb_scan_last_target(); cb_scan_warmode_hostiles()
                self.draw(cb_prune_and_refresh())
        GRIP_DOTS = ((6, 6), (6, 3), (3, 6), (6, 0), (0, 6), (3, 3))
        class ControlPanel(object):
            BODY_H = 420; FOE_ROW_H = 32
            def __init__(self, windows, combat):
                self.windows, self.combat = windows, combat
                self.g = self.list_sa = self.input = self.lock_all_lbl = self.combat_lbl = self.foe_title = None
                self.store, self.x0, self.w = ({}, {}), 0, 0; self.foe_ver = self.seen_ver = -1
                self.foe_rows, self.seen_at = [], 0.0; self.lock_all_text = self.combat_text = ""
                self.list_top = self.list_h = 0; self.list_lbls = (); hub = HOST.hub
                if hub is not None:
                    hub.add("ultima", TITLE, {"height": self.height, "build": self.build_section,
                             "closed": self.section_closed})
                else: say("couldn't show the Foe list panel (no shared window).", Kit.HUE_BAD)
            @property
            def gump(self): return self.g if Kit.is_open(self.g) else None
            @property
            def size(self): hub = HOST.hub; return (hub.W, hub.H) if hub is not None else (0, 0)
            def height(self, w): return self.BODY_H + 16
            def build_section(self, g, x, y, w, store):
                self.g, self.store = g, store; self.x0, self.w = x + 8, w - 16; self.list_sa, self.foe_ver = None, -1
                Kit.add_section(g, x, y, w, self.height(w)); self.build_body(y + 8); ANCHORS.pending = True
            def section_closed(self): self.g = self.list_sa = self.input = None; self.foe_rows = []
            def _heading(self, text, y):
                lb = label(text, 13, "#FFD966"); place(lb, self.x0 + 2, y); self.g.Add(lb); return lb
            def _divider(self, y):
                d = tiled(Kit.STONE_TILE, self.w, 4); d.SetPos(self.x0, y); self.g.Add(d)
            def build_body(self, y0):
                g, X, W = self.g, self.x0, self.w; cw = int(W / 3); self._heading("FOES & IGNORE LIST", y0)
                f = tiled(Kit.FIELD_TILE, W, 24); f.SetPos(X, y0 + 21); g.Add(f)
                self.input = API.Gumps.CreateGumpTextBox("", W - 4, 22, False, 16); self.input.SetPos(X + 2, y0 + 22)
                self.input.SetPlaceholder("Player name"); Kit.with_tip(self.input, "Player name for the buttons below")
                g.Add(self.input); self.combat_text = "Hide combat" if self.combat.is_open() else "Show combat"
                rows = (("Add foe", 0, 52, self.add_foe, Kit.ART_OK, "Put the typed name on your Foe list"),
                        ("Remove foe", 1, 52, self.remove_foe, Kit.ART_CLOSE, "Take the typed name off your Foe list"),
                        ("Target...", 2, 52, self.target_foe, Kit.ART_PLAY,
                            "Target a player to put them on your Foe list"),
                        ("Ignore", 0, 80, self.ignore_name, Kit.ART_CLOSE,
                         "Hide the typed name from the trackers (an NPC)"),
                        ("Unignore", 1, 80, self.unignore_name, Kit.ART_OK,
                            "Show the typed name in the trackers again"),
                        ("Lock all", 2, 80, self.lock_all, Kit.ART_PLAY,
                         "Lock or unlock every tracker, the combat bars and pop-outs"),
                        (self.combat_text, 0, 144, self.toggle_combat, Kit.ART_PLAY, "Show or hide the combat bars"),
                        ("Settings", 1, 144, lambda *a: HOST.show_settings("ultima"), Kit.ART_PAGE,
                         Kit.SETTINGS_TIP % TITLE), ("Sightings", 2, 144, lambda *a: SIGHT_WIN.toggle(), Kit.ART_PAGE,
                         "Open or close the Sightings window"))
                lbls = [self._button(t, X + col * cw, y0 + dy, cw, fn, art, tip) for t, col, dy, fn, art, tip in rows]
                self.lock_all_lbl, self.combat_lbl, self.lock_all_text = lbls[5], lbls[6], "Lock all"
                self._divider(y0 + 110); self._heading("WINDOWS", y0 + 120)
                self._divider(y0 + 176); self.foe_title = self._heading("SAVED FOES (0)", y0 + 186)
                self.list_top = y0 + 210; bottom = y0 + self.BODY_H
                step = max(16, NATIVE.get("font_h", 0) if uo_font_for(11) else 0)
                self.list_h = bottom - step - 14 - self.list_top
                lb = label("Alt+click any bar: auto-follow (again to stop).", 11, DIM_TEXT)
                place(lb, X + 2, bottom - step - 6); g.Add(lb); self.foe_ver = st["foe_ver"]; self.rebuild_foe_list()
            def _button(self, text, x, y, w, fn, art, tip=None):
                bw = Kit.pic_size(art[0])[0] or 30; key = "ut:" + text.lower().replace(" ", "_").rstrip(".")
                return Kit.art_button(self.g, self.store, key, art, x, y, Kit.fit(text, max(10, w - bw - 6)), tip,
                                      on_click=queue_click(fn))
            def _typed(self): return (safe(lambda: self.input.Text, "") or "").strip()
            def _clear_input(self): safe(lambda: self.input.SetText(""))
            def add_foe(self, *args):
                n = self._typed()
                if not n: say("type a name first.", Kit.HUE_BAD); return
                add_foe(n); self._clear_input(); say("added %s to the Foe list." % n, Kit.HUE_GOOD)
            def remove_foe(self, *args):
                n = self._typed()
                if n: self._remove(name_key(n)); self._clear_input()
            def _remove(self, key):
                if key in FOES:
                    unlink_foe(key)
                    if LINK_PICK[0] == key: LINK_PICK[0] = None
                    name = drop_foe(key); say("removed %s from the Foe list." % name, Kit.HUE_GOOD)
                else: say("%s isn't on the Foe list." % key, Kit.HUE_BAD)
            def target_foe(self, *args):
                say("target a player for your Foe list.", Kit.HUE_INFO); HOST.pick_target(10, self._foe_targeted)
            def _foe_targeted(self, serial):
                mob = API.FindMobile(serial) if serial else None
                if not mob or not mob.Name: say("no player targeted.", Kit.HUE_BAD); return
                add_foe(mob.Name); say("added %s to the Foe list." % mob.Name, Kit.HUE_GOOD)
            def ignore_name(self, *args):
                n = self._typed()
                if n:
                    IGNORE[n.lower()] = n; save_settings(); self._clear_input()
                    say("ignoring %s from now on." % n, Kit.HUE_GOOD)
            def unignore_name(self, *args):
                n = self._typed()
                if n and n.lower() in IGNORE:
                    IGNORE.pop(n.lower()); save_settings(); self._clear_input()
                    say("no longer ignoring %s." % n, Kit.HUE_GOOD)
            def _all_locked(self):
                locks = [w.locked for w in self.windows.values()]
                if self.combat.is_open(): locks.append(LAYOUT["combat"][4])
                locks.extend(p.locked for p in POPS.values()); return all(locks)
            def lock_all(self, *args):
                target = not self._all_locked()
                for w in self.windows.values(): w.set_locked(target)
                self.combat.set_locked(target)
                for p in list(POPS.values()): p.set_locked(target)
                self.refresh_labels()
            def toggle_combat(self, *args):
                cw = self.combat
                if cw.is_open() and HOST.layout_holds(cw.dock_key): return
                (cw.hide if cw.is_open() else cw.show)(); self.refresh_labels()
            def refresh_labels(self):
                if self.gump is None or self.lock_all_lbl is None: return
                text = "Unlock all" if self._all_locked() else "Lock all"
                if text != self.lock_all_text: self.lock_all_text = text; Kit.set_text(self.lock_all_lbl, text)
                text = "Hide combat" if self.combat.is_open() else "Show combat"
                if text != self.combat_text: self.combat_text = text; Kit.set_text(self.combat_lbl, text)
            def reset_defaults(self, *args):
                reset_settings()
                for p in POPS.values(): p.opacity, p.locked = DEFAULT_OPACITY, False
                for w in self.windows.values():
                    if w.docked: w.docked = False; HOST.dock_forget(w.dock_key)
                cb_was_docked = self.combat.docked
                if cb_was_docked: self.combat.docked = False; HOST.dock_forget(self.combat.dock_key)
                refresh(self.windows); self.combat.reset()
                if cb_was_docked and self.combat.is_open(): Kit.set(self.combat.gump, "IsVisible", True)
                if HOST.hub is not None: HOST.hub.refresh()
                apply_borders_all(); save_settings()
                say("settings and windows reset to the defaults.", Kit.HUE_GOOD)
            def set_all_opacity(self, v):
                settings["opacity"] = v
                for w in self.windows.values(): w.apply_opacity(v)
                for pb in POPS.values(): pb.apply_opacity(v)
                self.combat.apply_opacity(v); LAYOUT["panel"][6] = v; st["dirty_save"] = True
            def rebuild_foe_list(self):
                if self.gump is None: return
                Kit.dispose(self.list_sa)
                for lb in self.list_lbls: LABELS.pop(id(lb), None)
                self.list_lbls = lbls = []
                self.list_sa = API.Gumps.CreateGumpScrollArea(self.x0, self.list_top, self.w, self.list_h)
                self.g.Add(self.list_sa); self.foe_rows = []; names = sorted(FOES.items(), key=lambda kv: kv[1].lower())
                set_text(self.foe_title, "SAVED FOES (%d)" % len(names))
                if not names:
                    lb = label("No foes yet. Type a name and press Add foe.", 12, "#888888"); lbls.append(lb)
                    place(lb, 2, 2); self.list_sa.Add(lb); return
                now = time.time(); rw = self.w - SCROLLBAR; mains = set(ALT_OF.values()); sa = self.list_sa
                for i, (key, name) in enumerate(names):
                    y = i * self.FOE_ROW_H; lb = label(short(name, 24), 13, "#FF9090"); lbls.append(lb)
                    place(lb, 2, y + 2); sa.Add(lb); bx = rw - 22
                    flat_button(sa, bx, y, 18, 18, "x", self._foe_btn(key, name, self._remove),
                                "Take %s off your Foe list. %s" % (name, ALT_FOLLOW_TIP))
                    bx -= 22; picked = LINK_PICK[0] == key
                    flat_button(sa, bx, y, 18, 18, "L*" if picked else "L", self._foe_btn(key, name, self.link_click),
                                ("Press L on the other entry (L here again: cancel). " if picked else
                                 "Link as one person: L here, then L on the other entry. ") + ALT_FOLLOW_TIP,
                                face=BTN_FACE_ON if picked else BTN_FACE)
                    if key in ALT_OF or key in mains:
                        bx -= 22
                        flat_button(sa, bx, y, 18, 18, "U", self._foe_btn(key, name, self.unlink_click),
                                    "Unlink from its group. " + ALT_FOLLOW_TIP)
                    sa.Add(catcher(0, y, max(20, bx - 6), 18, (lambda k, n: (lambda *a: self.foe_name_click(k, n)))(key,
                                           name), tip_for(TIP_FOE_ROW, name)))
                    info = label(self.foe_info(key, now), 11, DIM_TEXT, maxWidth=rw - 6); lbls.append(info)
                    place(info, 2, y + 17); sa.Add(info); self.foe_rows.append((key, info))
                self.seen_ver = SIGHT["seen_ver"]; self.seen_at = now + SEEN_REFRESH
            def _foe_btn(self, k, n, fn): return lambda *a: self.foe_name_click(k, n) if alt_held() else fn(k)
            @staticmethod
            def foe_info(key, now):
                lk = link_text(key); seen = seen_text(key, now); return lk + "; " + seen if lk else seen
            def link_click(self, key):
                if key not in FOES: return
                pick = LINK_PICK[0]
                if pick is None or pick not in FOES:
                    LINK_PICK[0] = key; say("press L on the entry to link with %s." % FOES[key], Kit.HUE_INFO)
                elif pick == key: LINK_PICK[0] = None; say("linking cancelled.", Kit.HUE_INFO)
                else: LINK_PICK[0] = None; say(link_foes(pick, key), Kit.HUE_GOOD); save_settings()
                st["foe_ver"] += 1
            def unlink_click(self, key):
                if key in FOES and unlink_foe(key):
                    say("%s is no longer linked." % FOES[key], Kit.HUE_GOOD); save_settings()
                    st["foe_ver"] += 1
            def foe_name_click(self, key, name):
                if alt_held():
                    best, bt = None, -1.0
                    for s, k in FOE_SERIALS.items():
                        if k == key and API.FindMobile(s) is not None:
                            t = PRESENT.get(s, 0.0)
                            if t > bt: best, bt = s, t
                    if best is not None: toggle_follow(best)
                    else: say("%s isn't in range." % name, Kit.HUE_BAD)
                    return
                safe(lambda: self.input.SetText(name))
            def update(self):
                if self.gump is None: return
                if self.foe_ver != st["foe_ver"]: self.foe_ver = st["foe_ver"]; self.rebuild_foe_list()
                elif self.foe_rows:
                    now = time.time()
                    if self.seen_ver != SIGHT["seen_ver"] or now >= self.seen_at:
                        self.seen_ver = SIGHT["seen_ver"]; self.seen_at = now + SEEN_REFRESH
                        for key, info in self.foe_rows: set_text(info, self.foe_info(key, now))
                self.refresh_labels()
        class SightRow(object):
            __slots__ = ("serial", "name", "prev", "e", "c", "nm", "here")
            def __init__(self):
                self.serial, self.name, self.prev, self.e = None, "", None, None
                self.c, self.nm, self.here = {}, "", None
        def make_sight_click(serial, name): return follow_or(serial, lambda: SIGHT_WIN.filter_name(name))
        SIGHT_LIST_H = 26 + SIGHT_ROWS * 22 + 6; SIGHT_H = 2 * Kit.MARGIN + 30 + 36 + SIGHT_LIST_H + 36 + 3 * Kit.GAP
        SIGHT_MIN_H = SIGHT_H - (SIGHT_ROWS - 1) * 22
        def zone_fit(obj, w, h, mode):
            new = (int(w), int(h)) if (w is not None and h is not None) else None
            if new != obj.slot or (mode == "again" and new is not None): obj.slot = new; obj.redraw = True
        def zone_told(obj, mw, mh):
            z = obj.slot
            if z is None or obj.st["minimized"] or not HOST.layout_holds(obj.KEY) or z[0] < mw or z[1] < mh: return None
            return z
        class SightingsWindow(object):
            KEY = "ultima.sightings"; TITLE = "Sightings"; W = 480; MINI_W, MINI_H = 300, 46
            COLS = (8, 92, 230, 278, 404)
            def __init__(self):
                self.st = {"minimized": False, "docked": False, "shutting": True}; self.win = {"g": None}
                self.slot, self.want, self.n, self.w = None, False, SIGHT_ROWS, self.W
                self.hooks = Kit.dock_hooks(self.TITLE, SIGHT_TRAY_ICON, self.st, self.win, self.ask_redraw, self.fit)
                self.hooks.update(show=self.zone_show, min=(self.W, SIGHT_MIN_H))
                self.flt = {"text": "", "noto": 0, "time": 0}; self.forget()
            def fit(self, w, h, mode): zone_fit(self, w, h, mode)
            def zone_show(self): self.want = True
            def forget(self):
                self.c, self.store, self.rows = {}, ({}, {}), []; self.page, self.matches, self.counts = 0, [], {}
                self.ver, self.ver_at, self.dirty, self.redraw = None, 0.0, True, False
                self.full_at = self.here_at = self.poll_at = 0.0
            def is_open(self): return self.win["g"] is not None
            def ask_redraw(self): self.redraw = True
            def toggle(self):
                if not self.is_open(): self.show()
                elif self.st["minimized"] or self.st["docked"]: self.bring()
                elif not HOST.layout_holds(self.KEY): self.close()
            def bring(self):
                if not self.is_open(): self.show()
                if self.st["minimized"] or self.st["docked"]:
                    HOST.dock_forget(self.KEY); self.st["minimized"] = self.st["docked"] = False
                    Kit.save_min(SIGHT_MIN_KEY, False); self.build()
            def show(self):
                if self.is_open(): return
                held = HOST.layout_holds(self.KEY)
                self.st.update(shutting=False, docked=False, minimized=not held and bool(
                    Kit.load_min(SIGHT_MIN_KEY) or HOST.dock_wanted(self.KEY)))
                self.build(); Kit.put_var(SIGHT_OPEN_KEY, "1")
            def save_pos(self):
                if not HOST.layout_holds(self.KEY): Kit.save_pos(SIGHT_POS_KEY, self.win["g"])
            def close(self, stopping=False):
                g = self.win["g"]
                if g is None: return
                self.st["shutting"] = True
                if not stopping: HOST.dock_forget(self.KEY); Kit.put_var(SIGHT_OPEN_KEY, "0")
                if not HOST.layout_holds(self.KEY):
                    Kit.save_pos(SIGHT_POS_KEY, g); Kit.save_min(SIGHT_MIN_KEY, self.st["minimized"])
                self.win["g"] = None; self.forget(); Kit.dispose(g)
            def lost(self):
                self.win["g"] = None; self.st["shutting"] = True; Kit.put_var(SIGHT_OPEN_KEY, "0"); self.forget()
            def build(self):
                self.redraw = False; old = self.win["g"]
                x, y = Kit.load_pos(SIGHT_POS_KEY, (320, 160), (self.W, SIGHT_H))
                if Kit.is_open(old): x, y = old.GetX(), old.GetY()
                self.win["g"] = None; self.forget(); store, c, rows = self.store, self.c, self.rows
                M, GAP = Kit.MARGIN, Kit.GAP; g = G.CreateGump(True, True); self.n, self.w = SIGHT_ROWS, self.W
                if self.st["minimized"]:
                    w, h = self.MINI_W, self.MINI_H
                    c["status"] = Kit.mini_bar(g, store, w, h, self.TITLE, self.KEY,
                                               queue_click(self.toggle_min), close_tip="Close Sightings")
                else:
                    z = zone_told(self, self.W, SIGHT_MIN_H); w, h = z if z else (self.W, SIGHT_H)
                    list_h = h - SIGHT_H + SIGHT_LIST_H; self.n = max(1, (list_h - 32) // 22); self.w = w
                    IW = w - 2 * M; Kit.add_window_frame(g, w, h)
                    Kit.title_bar(g, store, w, self.TITLE, self.KEY, queue_click(self.toggle_min),
                                  queue_click(lambda: HOST.dock_to_bar(self.KEY, self.TITLE)),
                                  queue_click(lambda: HOST.show_settings("ultima")), close_tip="Close Sightings")
                    yf = M + 30 + GAP; Kit.add_section(g, M, yf, IW, 36); Kit.add_label(g, "Find:", M + 10, yf + 9)
                    c["find"] = Kit.with_tip(Kit.add_textbox(g, self.flt["text"], M + 52, yf + 7, 128, numbers=False),
                                             "Part of a name: list only that player")
                    c["noto"] = Kit.art_button(g, store, "noto", Kit.ART_PAGE, M + 196, yf + 7,
                                               SIGHT_NOTO_FILTERS[self.flt["noto"]][0],
                                               "Which players to list (click to cycle)",
                                               on_click=queue_click(lambda: self.cycle("noto", SIGHT_NOTO_FILTERS)))
                    c["time"] = Kit.art_button(g, store, "time", Kit.ART_PAGE, M + 326, yf + 7,
                                               SIGHT_TIME_FILTERS[self.flt["time"]][0],
                                               "How far back to list (click to cycle)",
                                               on_click=queue_click(lambda: self.cycle("time", SIGHT_TIME_FILTERS)))
                    yl = yf + 36 + GAP; Kit.add_section(g, M, yl, IW, list_h)
                    for x0, head in zip(self.COLS, ("Time", "Player", "Colour", "Where", "Count")):
                        Kit.add_label(g, head, M + x0, yl + 6, Kit.HUE_TITLE)
                    for i in range(self.n):
                        ry = yl + 26 + i * 22; r = SightRow()
                        for k, x0, hue in (("t", 0, Kit.HUE_INFO), ("n", 1, Kit.HUE_TEXT),
                                           ("o", 2, Kit.HUE_TEXT), ("p", 3, Kit.HUE_INFO), ("k", 4, Kit.HUE_INFO)):
                            r.c[k] = Kit.add_label(g, "", M + self.COLS[x0], ry + 2, hue)
                        r.c["hit"] = Kit.catcher(g, M + 4, ry, IW - 8, 22, queue_click(RowClick(r, make_sight_click)),
                                                 TIP_SIGHT)
                        rows.append(r)
                    yb = yl + list_h + GAP; Kit.add_section(g, M, yb, IW, 36)
                    Kit.art_button(g, store, "newer", Kit.ART_PAGE, M + 10, yb + 7, "Prev",
                                   "Newer sightings", on_click=queue_click(self.newer))
                    Kit.art_button(g, store, "older", Kit.ART_PAGE, M + 120, yb + 7, "Next",
                                   "Older sightings", on_click=queue_click(self.older))
                    c["status"] = Kit.add_label(g, "", M + 230, yb + 10, Kit.HUE_INFO)
                Kit.show_window(g, x, y, w, h, self.KEY, self.st["minimized"] and self.st["docked"], None,
                                self.save_pos, self.win, {"g": g})
                Kit.dispose(old); self.refresh(time.time(), True)
            def toggle_min(self, *args):
                Kit.win_action("toggle_min", self.st, self.KEY, self.TITLE, self.build, SIGHT_MIN_KEY)
            def cycle(self, k, table):
                self.flt[k] = (self.flt[k] + 1) % len(table)
                if k in self.c: Kit.set_text(self.c[k], table[self.flt[k]][0])
                self.page, self.dirty = 0, True
            def newer(self, *args):
                if self.page > 0: self.page -= 1; self.dirty = True
            def older(self, *args):
                if (self.page + 1) * self.n < len(self.matches): self.page += 1; self.dirty = True
            def filter_name(self, name):
                new = "" if self.flt["text"].lower() == name.lower() else name; tb = self.c.get("find")
                if tb is not None: safe(lambda: tb.SetText(new))
                self.flt["text"] = new; self.page, self.dirty = 0, True
            def tick(self, now):
                if self.want:
                    self.want = False
                    if HOST.layout_holds(self.KEY):
                        if not self.is_open(): self.show()
                        elif self.st["minimized"] or self.st["docked"]:
                            self.st["minimized"] = self.st["docked"] = False; self.build()
                if self.win["g"] is None: return
                if Kit.was_clicked(self.store, "close"): self.close(); return
                if self.redraw: self.build(); return
                if now < self.poll_at <= now + TICK_SECONDS: return
                self.poll_at = now + TICK_SECONDS
                if not Kit.is_open(self.win["g"]): self.lost(); return
                if self.st["minimized"] and self.st["docked"]: return
                self.refresh(now)
            def refresh(self, now, force=False):
                c = self.c
                if self.st["minimized"]:
                    if force or SIGHT["ver"] != self.ver or now >= self.full_at:
                        self.ver, self.full_at = SIGHT["ver"], now + SIGHT_REFRESH; n = len(SIGHTS)
                        text = "%s: %d" % (self.TITLE, n)
                        if n: e = SIGHTS[-1]; text += ", last %s %s" % (e[S_NAME], stamp(e[S_T], today_start(now)))
                        else: text = "%s: none yet" % self.TITLE
                        Kit.set_text(c["status"], Kit.fit(text, self.MINI_W - 90))
                    return
                tb = c.get("find")
                if tb is not None:
                    txt = str(tb.Text or "").strip()
                    if txt != self.flt["text"]: self.flt["text"] = txt; self.page, self.dirty = 0, True
                if force or self.dirty or now >= self.full_at or \
                        (SIGHT["ver"] != self.ver and not 0.0 <= self.ver_at - now <= 1.0):
                    self.ver_at = now + 1.0; self.work_out(now); self.fill(now)
                elif now >= self.here_at: self.mark_here(now)
            def work_out(self, now):
                self.dirty = False; self.ver, self.full_at = SIGHT["ver"], now + SIGHT_REFRESH
                tf = SIGHT_TIME_FILTERS[self.flt["time"]][1]
                cut = None if tf is None else (today_start(now) if tf == "today" else now - tf)
                nf = SIGHT_NOTO_FILTERS[self.flt["noto"]][1]; find = name_key(self.flt["text"]); out, counts = [], {}
                for i in range(len(SIGHTS) - 1, -1, -1):
                    e = SIGHTS[i]
                    if cut is not None and e[S_T] < cut: break
                    if find and find not in e[S_KEY]: continue
                    if nf is not None and (e[S_KEY] not in FOES if nf == "foe" else e[S_NOTO] not in nf): continue
                    out.append(e); counts[e[S_KEY]] = counts.get(e[S_KEY], 0) + 1
                self.matches, self.counts = out, counts; last = max(0, (len(out) - 1) // self.n)
                if self.page > last: self.page = last
            def fill(self, now):
                today0 = today_start(now); start = self.page * self.n; m = self.matches
                for i, r in enumerate(self.rows): j = start + i; self.assign(r, m[j] if j < len(m) else None, today0)
                self.mark_here(now); n = len(m)
                if n:
                    text = "%d-%d of %d, %s" % (start + 1, min(n, start + self.n), n,
                                                    Kit.count(len(self.counts), "name"))
                elif SIGHTS: text = "No sightings match the filters"
                else: text = "No sightings yet" if settings["sightings"] else "Logging is off (settings page)"
                Kit.set_text(self.c["status"], Kit.fit(text, self.w - 2 * Kit.MARGIN - 236))
            def assign(self, r, e, today0):
                c = r.c
                if e is None:
                    if r.e is not None:
                        r.prev = (r.serial, r.name, time.time())
                        r.e, r.serial, r.name, r.nm, r.here = None, None, "", "", None
                        for k in ("t", "n", "o", "p", "k"): Kit.set_text(c[k], "")
                    return
                if e is not r.e:
                    if r.serial is not None and r.serial != e[S_SERIAL]: r.prev = (r.serial, r.name, time.time())
                    r.e, r.serial, r.name = e, e[S_SERIAL], e[S_NAME]; r.nm, r.here = Kit.fit(e[S_NAME], 124), None
                    Kit.set_text(c["o"], noto_word(e[S_NOTO]), NOTO_HUE.get(e[S_NOTO], Kit.HUE_TEXT))
                    where = place_text(e[S_FACET], e[S_X], e[S_Y])
                    Kit.set_text(c["p"], Kit.fit(where + (" G" if e[S_GUARD] else ""), 118)); g = e[S_GUARD]
                    extra = "Seen %s at %s%s" % (stamp(e[S_T], today0), where, ", in a guard zone (G)" if g else
                                                 (", outside the guards" if g is False else ""))
                    Kit.with_tip(c["hit"], tip_for(TIP_SIGHT, e[S_NAME], extra))
                Kit.set_text(c["t"], stamp(e[S_T], today0)); Kit.set_text(c["k"], "x%d" % self.counts.get(e[S_KEY], 1))
            def mark_here(self, now):
                self.here_at = now + 1.0
                for r in self.rows:
                    if r.e is None: continue
                    t = PRESENT.get(r.serial); here = t is not None and now - t <= 2 * TICK_SECONDS + 0.05
                    if here != r.here:
                        r.here = here; Kit.set_text(r.c["n"], r.nm, Kit.HUE_GOOD if here else Kit.HUE_TEXT)
        class KillerWindow(object):
            KEY = "ultima.killer"; TITLE = "Add my killer"; W = 340; MINI_W, MINI_H = 260, 46; ROW_H = 26
            def __init__(self):
                self.st = {"minimized": False, "docked": False, "shutting": True}; self.win = {"g": None}
                self.store, self.c, self.cands = ({}, {}), {}, []; self.until, self.slot = 0.0, None
                self.redraw = self.want = False
                self.hooks = Kit.dock_hooks(self.TITLE, 0, self.st, self.win, self.ask_redraw, self.fit)
                self.hooks.update(show=self.zone_show, min=(self.W, self.height(1)))
            def ask_redraw(self): self.redraw = True
            def zone_show(self): self.want = True
            def fit(self, w, h, mode): zone_fit(self, w, h, mode)
            def held(self): return HOST.layout_holds(self.KEY)
            def height(self, n): return 2 * Kit.MARGIN + 30 + Kit.GAP + 8 + n * self.ROW_H + 26
            def open(self, got, now, total=None):
                self.cands = [{"name": a[0], "serial": a[2]} for a in got]; self.until = now + KILLER_SHOW
                self.st.update(shutting=False, docked=False, minimized=not self.held() and Kit.load_min(KILLER_MIN_KEY))
                self.build(); n = len(got) if total is None else total
                say("you died; %s attacked you (see %s)." % (Kit.count(n, "player"), self.TITLE), Kit.HUE_BAD)
            def save_pos(self):
                if not self.held(): Kit.save_pos(KILLER_POS_KEY, self.win["g"])
            def close(self):
                g = self.win["g"]
                if g is None: return
                if not self.held(): Kit.save_pos(KILLER_POS_KEY, g); Kit.save_min(KILLER_MIN_KEY, self.st["minimized"])
                self.st["shutting"] = True; self.win["g"], self.c, self.cands = None, {}, []; Kit.dispose(g)
            def end(self):
                if not self.held(): self.close()
                elif self.cands: self.cands = []; self.build()
            def build(self):
                old = self.win["g"]; mini = self.st["minimized"]; z = zone_told(self, self.W, self.height(1))
                W, H = z if z else (self.W, self.height(max(1, len(self.cands)))); sw, sh = Kit.screen()
                shown = self.cands[:max(1, (H - self.height(0)) // self.ROW_H)] if z else self.cands
                x, y = Kit.load_pos(KILLER_POS_KEY, (max(0, ((sw or 1024) - W) // 2),
                                                     max(0, ((sh or 768) - H) // 3)), (W, H))
                if Kit.is_open(old): x, y = old.GetX(), old.GetY()
                self.win["g"] = None; store, c = ({}, {}), {}; M = Kit.MARGIN; g = G.CreateGump(True, True)
                if mini:
                    W, H = self.MINI_W, self.MINI_H; n = len(self.cands)
                    c["status"] = Kit.mini_bar(g, store, W, H, self.TITLE, self.KEY, queue_click(self.toggle_min),
                                               "%s: %s" % (self.TITLE, Kit.count(n, "attacker")),
                                               close_tip="Close the attacker list")
                else:
                    IW = W - 2 * M; Kit.add_window_frame(g, W, H); Kit.add_section(g, M, M, IW, 30)
                    Kit.add_label(g, self.TITLE.upper(), M + 30, M + 7, Kit.HUE_TITLE)
                    if Kit.zone_up(self.KEY): Kit.catcher(g, M, M, IW, 30, lambda *a: None, None, movable=True)
                    else:
                        Kit.title_catcher(g, M, M, W - M - 80 - M, 30, queue_click(self.toggle_min), key=self.KEY)
                        Kit.art_button(g, store, "min", Kit.ART_MIN, W - M - 74, M + 7, None,
                                       Kit.MIN_TIP, on_click=queue_click(self.toggle_min))
                        Kit.art_button(g, store, "close", Kit.ART_CLOSE, W - M - 54, M + 4, None,
                                       "Close the attacker list")
                    yb = M + 30 + Kit.GAP; Kit.add_section(g, M, yb, IW, H - yb - M); cap = "Add to foes"
                    bx = W - M - 10 - (35 + Kit.text_w(cap))
                    for i, a in enumerate(shown):
                        ry = yb + 8 + i * self.ROW_H; on = name_key(a["name"]) in FOES
                        Kit.add_label(g, Kit.fit(a["name"], bx - M - 30), M + 10, ry + 3, Kit.HUE_BAD)
                        Kit.catcher(g, M + 6, ry, bx - M - 14, 22, queue_click(self.make_follow(i)),
                                    tip_for("Alt+click: auto-follow (again to stop)", a["name"]))
                        c["add%d" % i] = Kit.art_button(g, store, "add%d" % i, Kit.ART_OK, bx, ry, "On Foe list" if on
                            else cap, "Put %s on your Foe list. Alt+click: auto-follow (again to stop)"
                            % a["name"], on_click=queue_click(self.make_add(i)))
                    text = "Closes on resurrection." if shown else Kit.fit(
                        "Lists your attackers when you die." if settings["killer"] else "Off (settings page)", IW - 20)
                    Kit.add_label(g, text, M + 10, yb + 8 + len(shown) * self.ROW_H + 2, Kit.HUE_INFO)
                Kit.show_window(g, x, y, W, H, self.KEY, mini and self.st["docked"], None, self.save_pos)
                self.win["g"], self.store, self.c = g, store, c; self.redraw = False; Kit.dispose(old)
            def make_add(self, i):
                def _add(*args):
                    if i >= len(self.cands): return
                    if alt_held(): self.make_follow(i)(); return
                    a = self.cands[i]
                    if name_key(a["name"]) in FOES: say("%s is already on the Foe list." % a["name"], Kit.HUE_INFO)
                    else: add_foe(a["name"]); say("added %s to the Foe list." % a["name"], Kit.HUE_GOOD)
                    lbl = self.c.get("add%d" % i)
                    if lbl is not None: Kit.set_text(lbl, "On Foe list")
                return _add
            def make_follow(self, i):
                def _follow(*args):
                    if i >= len(self.cands) or not alt_held(): return
                    a = self.cands[i]; s = a["serial"]
                    if s is None: s, _ = find_named(a["name"])
                    if s is None: say("%s isn't in sight." % a["name"], Kit.HUE_BAD)
                    else: toggle_follow(s)
                return _follow
            def toggle_min(self, *args):
                ks = self.st; ks["minimized"] = not ks["minimized"]; Kit.save_min(KILLER_MIN_KEY, ks["minimized"])
                self.build()
            def tick(self, now):
                if self.want:
                    self.want = False; ks = self.st
                    if self.held() and (self.win["g"] is None or ks["minimized"] or ks["docked"]):
                        ks.update(shutting=False, minimized=False, docked=False); self.build()
                g = self.win["g"]
                if g is None: return
                if Kit.was_clicked(self.store, "close"): self.close()
                elif not Kit.is_open(g): self.win["g"], self.c, self.cands = None, {}, []; self.st["shutting"] = True
                elif not self.cands and not self.held(): self.close()
                elif self.redraw: self.build()
                elif self.cands and now >= self.until: self.end()
        SIGHT_WIN = SightingsWindow(); KILLER_WIN = KillerWindow()
        NPC_NAMES_DATA = ("0aaron2sin1ba2bott3y2del3iel2el4la3y2igail3jah3na3ona3ra2ner2ra4h5am4n2sinthe1cacia3nit4tha"
            "2calia2e3lin2hen3illes2kerley1da3ir3lia3m3ra2di4son2eben3laide4e4ia5ne4le3m3na3res3sina2ie3mina3ran3va2la"
            "i3er4y2mon2olph3n4cia4ia5s3ra2rian4el5nne1elina2neas1fina2ra3ika2ton1gate4ha2nes2ustin1hara3ve2earn2imsa2"
            "mik2ren1ida4n2ella2ken3o2la3een3sa2mee4ry2n3a3hoa3sley3tzane2rlia2sling6n2tan3hne2yana1jara3y4i2inora1kak"
            "o3la3ndo4ke3sma2baar2ela4lo2il4ah4i5na3na2shay1laina3ke3la3manada3n4a4d4i4na4o3qua3ric3stair3vda3zne2ben4"
            "rt6a3inka2cander3ina3ott2dea4n4r5cy3rick2ec3k4a4sy3nne3ron3ser4ia4sa3thea3x4a5nder7ra8ia9na4is2fred2ger2i"
            "3a3ce4ia3da3ke3m4a3na3son4tair3ta3x3z4a2laard4n4rd3ele4n3igra4nora4son3yn2ma2odie3nzo3ysia2phonse7o2ston2"
            "tair3hea3on2ula3mit2vin5a4ta2ysa4sa6nd2zena1ma3bel3deo4i5ka5s4o3ia3la4ia3nda5ine3ra5nde6te4is3ta2bar3er3i"
            "ka4s3rose2eerah3lia5na3thyst2ie4l5la3na4ta3ssa3ta4y2mon2oke3s2sden2y1nanda3stasia2celin2ders3i3ra5ianna5s"
            "4e5a5us5w5y4ies4omeda2eida3lla3mone3zka2gela5ica6ne6que5o4ni3us2i3ca3eli3sa3ta2ke4r2n3a4bel7le4marie3e4tt"
            "e3ikka3ora2oki3rah3ush2sel5me3ley3on3reana2teia3hea4ony3je3oinette4nia6o2war1olani1para2irka2olline5oina3"
            "ni2ril5le1qua3ene1ra3bella7e3celi3minta3xie2cadia3her4ibald2dath3elia4n3is4th3on2eiela3lla3n3s3tha4ina2gu"
            "s2i3adne4na3cia5n3el4ne3on3sta5o6tle2kin2len5e4y3in5da3o2man3en3ina5da3on3strong2ne3old4n2on2piar2sen5io2"
            "temisia3hur2una2ziki1saria2enka2h3a3by3er3ford3lan4eigh5y4in3on3ur2ia3sa2linda2pasia2ta3er5a3ra4ea4id1tal"
            "anta3ra2enne3ri2halia4n3ena4ron3la2ifa2man2ta1ubrey2da3ny3rey4ianna5c3un2gustin8a6us2ra3e4k4lia3ilia4na3k"
            "ene3ora2stin2tumn1va3na3sa2ella3na3rill4y2ie3s3va1xel4la1ya3luna3me3na3sha2dee2ela2iana3la3sha3ta2la2nora"
            "2una1zaleah4ia3rael2era2ha2ilea3na3ze2ora2ura0babette2cia2e2iley3ngana2ka4ri5ne2layna3bo3der4win3e4a4ndin"
            "3i4a4n5t2mbi2nan3croft3dele3e4lla3ning2ra4n3bara3clay3den4o5n3ika3nabas6y4ett5y3on3rett4y3se3t4h5olomew4o"
            "n2sha3ia4l4mah3tiaan2takah3hsheba3ya2ul2vol2xter2y3ana5i4rd3lor3o3ta2zyli1ea3can3gan3man3trice6x3u4ina4mo"
            "nt4regard2cca3k4y2delia2l3ana3don3en3ina5da4ta3lanca4e3ora2m3an2n3edict4n3jamin3nett3son3t4e4ley4on2radin"
            "e3enger3gren3illa4t3k4eley3nadette5rd4ice3sh3t4hold4on4ram3yl2ss4ine2ta3h4ana6y3ony3ty2ulah2val4n3erly3in"
            "1ialy3n4ca2lal3lie2na3dy3ti2rdie3kita2shop2talo2xenta1jorn1lade3ine4r4se3ke3nche4da3z2enda2iss2orn2y3the1"
            "o2den2gart2hdan6a2lton2namy3d3ita3nie4y2oker3ne2rden3gny3is2tan2wie3man2yce3d4en1rad4en4ford4ney4y3ina3m3"
            "n4d5eis5i5on5y4t3xton3y3z4il2en4cis4da6n5on4na6n4t5an3t4t5a3wster2iac4n5d3ce3dget3e4g4r4tta3git6te3na4ley"
            "3ona5y3shen3tes4ta6ny2ock3derick4ny4y3nson4t4wyn3oke2uce3no3tus2yan5t3ce3nn3son1ucia3k2d3o2rgess3han3ian3"
            "ke3l3r3ton1yran3on0cadence4o3or2edmon2ilan3mile3n4e3tlin4rin2la4ndia6ra3der4well3eb4ndonia4y3ida4sta3la5n"
            "4ia5dora5e3tha3vin3ypso2m3den3elia4ron3ilia5le2nace3dace5n4ida6e4ra3tara4on3ute2oimhe2pri5ce2ra4doc3den3e"
            "sse4y3i4na5e4ssa4ta3l4a4een5n4in6g4o5s5ta4ton4y3ma4el6ina5n3na4elian3ol5ina7e5yn4n3r4ick5e4ocio5ll3son3te"
            "r3ver3yn2sey3ilda3per3sandra4ia5dy5us3ta5lia4el2talina4va3erina3herine4leen4y3o4n3riona2van2yla1eara3sar2"
            "cania3il5ia2dric2landine3este3ia4na3lia2mal2relia1had4wick3im4tra3l4e4mers3nah4da5er5i5ler5ra4e5l5y4na5in"
            "g4tal3pin4man3ris6sa5ty4les5otte5ton4maine3se4tity3tha3uncy3va4iva3y4a4ton2elsea3n4ey4oa3rica6e5e4yl3sna4"
            "ter3t3valier2iara3ka4e3lali3mlis3n3po2loe4ris2o2rista7ble6ian7na8e6oph9er7s6y2uck2you1ia3nnait3r2cely4ron"
            "2ndy2ro1laire3ra4ence4inda5ssa4k3ude6tte5ia6ne3y4ton2ement7ina9e3veland2iantha3fford4ton3nt5on3ve2orinda3"
            "ver2yde1ochiti2dy2lby3e4ene4man4tte3in3lin3on3ton2man2ndon3nie4or3rad3stance7za4uela3way2ra4lie4zon3bett5"
            "y4in3coran3deali5ll3etta4y3i4nna4s3liss3nelius3rine3t4ney2ty2urtland1raig3ndall2eighton3scent4sida2ispin2"
            "osby2ystal1ullen4in3ver2rran3tis1ybele3il2nric3thia2prien2rano3ene3il5la3us2theria0dabria2cey3ia4e4o2e2g3"
            "an3mar3na2i3ly3sel4y2karai3ota2le3ila5ia3lin3ton3y2mara3ek4n3ian4en4on4tri3on2na3e4tt3ia4el6la4or3nik3te3"
            "yelle2phene4ne5ie2r3a4lis3by3en3ia4en4o3la4ene3nell3rel6l5n3yl2sha2vene3id4n5e4s4ta2wn2ya3na1eacon3n4a4dr"
            "a2b3ra2cker2de2e3dee2ianira3ene3rdre2lana5ey5o3bert4in3ia4cia4lia3la5n3more3phina3sin2man3be3i4tria3psey5"
            "ter2na3by3ice3nis4ys3ton3ver2r3ek3rick4y2va4ki4l3erell3i4n3lin3net3on2wey1iamanta3ne4the2ederik4re3go3lla"
            "3ter2llian4on4y3ys2mitri2nah2onne2rk2sa2ta3i2xie1obry2die2lores2minic7k6que2na4ld4ta5ien5o3ielle3nelley7y"
            "5r3ovan2oriya2phina2ra3een3inda4s4thy3on3y2ugie4las7s2v2yle1rake2ew2ina2ucilla1uane2gan3las2lcie5nea2ncan"
            "3stan2rand3riken2san3tin4y2tch1wayne2ight1yami3n4i3stro2lan2mas3phna2na0eamon2rl4e3tha2ster2ton1bony1cho1"
            "dan4a2gan4r2ie3son3th2lyn2mund2na2olie2ria4n2ward3in5a1fia1gan1ileen2nar2rene1lad3ine3na2den3roth2ek3ora2"
            "i3anor4s3jah3na3sa4e4ka4sa3ta3za5beeth2kan3e2la3e4n4ry3iot6t4s3sworth3y2mer3o2odie3ise2sa3ie3ton2ton2wood"
            "2ynor3se4ia1ma3jane3lia3nuel2ber2elie4yne2il4io4y2ma3ett2o1ndora2gracia2id2och3la2rico4que2ye1phraim1rasm"
            "a2ek2ianthe3c4a3k3n2lina2nest2ol2rol2skine2wand3in2yx1skarne2merelda2peranza2sien2ta3eban4lle3her3u1tain5"
            "a3nthe2han2ta1udocia2gene5ia2lalia2stacia1va3csa3dine4ne3n4der4geline4the2e3lyn3rett2ita2onne2zen1yota1ze"
            "kial2ra0fabienne4o2ifuza3nche3rfax3th3zah2llon2ntine2rha3ima3ley3rah4ell2tin2wne2xon2y3e3ina3me1elcia3ici"
            "te7y4x2mi2nn3ton2rgus3idwyn3n3onia3ran4is1ielding2lbert3inda3more2na3lay4ey3n4igan3ola2ona3renza2sk2tzger"
            "ald1lavia2eta4cher2indo4t2ora4ence3yd2ynn1orbes3rest3sythe2ster1rances7ca5ine6s7ca4ek4k5lin3sier3zer4ier2"
            "ed4a4erica8k3mont3ya2ida3eda3tz1uller3ton2scienne0gabe3riel7la8e2ge2ia3l2latea3en5o3i4na3vin3ya2mble2na3e"
            "sa3non2reth3field3gan3ner3rett4ick5dan5son5tt3th3vin3y2spar3ton2uri2vin3rie2ye3le4ord3nor1elasia2mma2nevi"
            "eve2off5rey6y3gia3rge6anne6tta8e5iana2radline4ldine4rd3da3ik3main3ri4y3trude2va1hislaine1iacinta3nina2deo"
            "n2gi2lana3berto3da3en4s3lian2n3a3ger3ton2selle2tana3ha2von2zane1leda3n4n5a5o5ys1odfrey2lda4ie2rdon4y3man2"
            "tzone1race4ie3dy3ham3inne3m3nger4t4ville3yson3zia2ear3g4er4or6y3sham3ta4chen4te2iffen5ith1uilhem2nnar3the"
            "r2s3tave2thrie2y1wen4dolyn4eth2ynne1ytha0hackett2dara4ssa3den3i4ya3ley3rian2gan2idee3ley3mi2l3den4is3e4y3"
            "i4an4ma3le4ie3sey2milton3lin2na4n3k3nah4e3s2rden4y3ith3lan3man4oni3old3per3riet5son4y3t4ley3vey2sna3san3t"
            "in6gs2va2ya3den3es3lee3nes2zel1ea3th5er2ctor2i3di2laku3degarde3en5a5e3ki2nka3ning3rietta4y2rbert3man3sche"
            "l2sper3ter1ilary3da3liard3ton2nda2roshi2sa1obart2gan2lden3ly3t2mes2pe2race3ton2shi2uston2ward3rence2yt1ug"
            "h3o2mphrey2nter4ley1yacinth2e2man2patia0iain1da2ola3nia1lene2ias2ona1man2ogene1ndia4ra3ra2es3z2ga3mar3ram"
            "4id1olana5the2na1ra3tze2ena4e2is2ma2vin5g2win1saac3beau5l6la3dora3iah3ura2is2leta2obel3ke2rael2tas1tzak1v"
            "an4a3r2ory2y0jabari3ir2celyn3inda5the3k3ob5e3ques3son3y2da2el3n2far2gger2imie3one2ke3inda2l3a3eel2mal3es3"
            "ie4la6h4son2n3a3e4lle4t3ice4s3na4elle2rdena3ed4k3man3on3rod3via5nia5s2smine3on3per2van3ier2y3a3ne1ean4ett"
            "e4ine2bidiah2d3idiah3rek2ff4rey2lani3ena2na4y3dayi4yose3ica3nettia4ifer3sine2remiah5y3olin4me5y3rilyn3zy2"
            "sse5e4ica2thro2wel2zebel1ibril2han2llian2n3a3ny3x2ro2vin1oakima3n4ne2bey3ihna2casa3elyn2di3y2el4le5iane2h"
            "ann6a3n2ia2lan5ta3ene3ie4ne3on2nah4than6on3ina2ra3dan6e4on3gen3vin2seph6ine3hua3ie2tha2y3ce3e1uanita2dd3e"
            "3ith6a2lia5n6a6e4e5tta4nka4us2ma3oke2n3e3g2stin6e0kaatje2chine3lyn2din2ede3the2i3a3e3kara3li3mi3ros3ya2kr"
            "a2la4din4ma4nit4re3b3e4a3i4ka4l5a4nda3kin3le4i3man3onice3yca2ma4l5a5i4ria3bo3eko3ilah5ia2nda3e4ne3iel4ka3"
            "tha3ya2pera2ra4n4yan3dal3el4n3ida4mah4sa3ka3l4a4enne4i4yn3mina3ol3sten3ylin4n2sa3ch3en3ia4nda3par3sia2te4"
            "b3herine4leen3ja3oka3rien5na2ula2veri3indra2y3a3e3in3la3sa2zia1eane3ra4ney2dar2efe3lan4in4y3nan2fira2gan2"
            "hinde2i3ko3r3sha3th2lby3da3eman3ia3l4en5y4i5e4y3sey3vin2n3an3dall4ra5ick3elm3ley3nard4edy5th4is3t4on3yang"
            "i4on2ona2pa2r3ani3by3ensa3n3ry3s4en4tan3win2sare3i4a3sie3ter2turah3zia2vin1halida5l2oury1ichi2efer3le3ran"
            "4nan2llian2m3berly3mie4y2n3eta3nel3sey3tan2ona2p2ra4n3by3ima3k3sten3ti2sa3ka3met3sa2ta2yoshi1liftin2og1oh"
            "ana2lina2mor2ntar2ren4ssa1rischan4ten6r1urt1yle4r3y2na3thia2oko0lacey3ie2ethan2ila4ie3rd2keisha2la4sa2mar"
            "3ont2n3a3ce3der4on4ra3e3g3i2ra4ine4lee3i4ssa3k3ry3s2tika3onia2ura5na4el4ie5nda4yn2veda4rn6e3inia2wler3ren"
            "ce2zarus1ea3h3la3ndra3r2ba2dah2e2if3gh5ton3ko3la5na2land2n3a3e3non5r5x3or5a5e3sar2o3n4a5rd3ra2ron4y2slie3"
            "ter2tha3itia2v3ana3i2wis2xine1i2a3dan3m3n4a4e2bby2en2ke2la3ith3lian5e3y2mber2na3coln3da4say5ey3ette3nae4e"
            "a2onel2sa3ette2tsa2v2za1lewellyn2oyd1ogan2is2kelani2la2ni2ra3e4lei5le4n5zo4tta3i3ne3raine2tus2uis5e2well1"
            "ucas3ian4lle4ne3retia3y2dia2ela2is4a2ke4ne3ina3yan2lu2na3t2ther1ydia2le2nda4on3elle3n4da4ette2ris2sander3"
            "el3nadra0mabel2c3aria3er3hi3k4enzie2ddy3elaine5ina7e5on5yn3y2e2gan4ra3dalen8a6ine3ena5ta3gie3nus2hala5ia2"
            "i3a3da3sie3tane3zah2j2laya3colm3ik4la4na5da3ka3lory3u2mie2nco3da5ra4ek5r4isa4y3fred3gena3ning3on3si4ur3ue"
            "l3ya2ra3c4ella4ia4os4us4y3den3ek4n3garet6ita4o5t4uirte3ia5h5m6a5n6a6na7e4bel4e5l5tta4ly6n4na4o4s5a5ha5sa3"
            "jani4eta4orie3k4ham4os3lene4in4o5n3mara3nie5na3sha6l7l4ten3ta4ha4i5n6a6go3vin3y4ann4beth4lou3zia2son2tai4"
            "na3eo3hea5r3ilda3rika3thew5ias2ud3ra4een4ice5ta2vis2x3ine3well2y3a3nard3on1ead3ra2da3ea2g3an4ra3han2i3ra2"
            "ka2la4nie5tha3ba3ia5n4na5da4senda5sa3linio3odie5y4sa3va2rcedes5r3edith4le3ill3le3rick5k2sha2ta2yer1ia3kod"
            "a2cael3hael7a4ele6le2dori2gina3non3on3uel2ka3e3kel3os2les3licent5e3o3ton2n3a3da4el4y3er5va3ka3na4ie2ra4nd"
            "a3em5ba4ya3iam4elle2ssy3ty2tchell3ena4xi3zi1oira2llie4y2na3ique3roe3te2on2rena3gan6a6ce3ia5h3ley3ris3time"
            "r4on3ven3z2tega1ukasa2rdoch6k3iel3phy1yles2ra3on0nada3ia4ne3ya2eem2ia3lah3mah2lini3ren2mazzi3i2n3a3cy3ett"
            "e3tale5n2omi2pea2ra3da3mada2siche3tassia2talie4ne4sha3esa3han6iel2ysa2zirqah1eal4a4e2ci2diva2ely2il2kane2"
            "lek3l3son2ola3ma3na2ria4ne4ssa3on2stor2tti2va4da4n3ille4n2ysa1icanor3holas3ia3ola5e6tte2gel2ka3ki3olos2ls"
            "2mah2na2obe3la2ra3velli2ssa2ta4ra2xie1oah2din2e3l4ani4la2lan3ita2na2ra4h3bert3een3i4ko3ma5n3ris3ton1uri1y"
            "dia2le2rna2ssa0oakes3ley1belia1chen2tavia6us1delia4l3ra3ssa3tta5e2ile3n3on2on1gden1hanna1kelani1laf3the3y"
            "inka2esia2ga2iana3n4da3ver5tte4ia1mar1na2ida1pal2helia1ralie3ne2dano2en4da2iana5na3el3ole4n2lantha2man5d2"
            "nidaa2rin2son2ville1scar2good2mond1tis2to1wen0paco2ige2kuna2lmer4iera3oma2mela2ndita4ora3thea4zike3ya4in2"
            "olo2ris3ker3nell2scal6e2tamon3ia4ence3ricia6k3sy3terson4on2ul4a4ette4in6e2vel3la2xton2yton2zia1earce4l2de"
            "r2g3gy2lagia2mba4roke2nda3elope3inna3n4y3thea2ony2rcival3dita3ouze3ry3sis2ter3ra2yton1haedra2earcy3dra2il"
            "ip4lip7pe4omena2oebe4nix2ylis4lis1ia2er4ce4re4son2la4n2per1laton1olly3oma2rche3ter4ia1rentice3scot7t4ton2"
            "iscilla2udence4y1yrena2thia0qamra1ueena3lla3nby4tin5on2illan3ncy4lan4n4tina3terie0rachel2d3cliffe3ella3in"
            "ka3man2e2fael3ferty2gnar2i3don3zel2leigh3ph2miro3la3on5a3say4ey3ya2nard3ce3dall4ie4olph3e4e4n3ger3i3kin2o"
            "ul2phael2quel2shida3ine2tri2ul2ven3i4d2wnie2y3mond3na4ell4or2ziya1eade2ba3ecca2dford3mond2ed3se3ve2gan3in"
            "a6ld4s2idun2mington3y2na4ldo4ta3dor3e4e3fry3ny2uben2x2yhan1hea3tt2iamon4nne6on2oda5nthe3nda4na2ys4sa1ia3n"
            "e2ca4rdo3hard4ter3o2der3gley2gby2hana2kki2ley2mon2ngo2o3dan3rdan2sa2ta2va1oanna3rke2bert6a6o3i4n3yn2chell"
            "e3kwell2d3erick3man3ney3rigo2ger2hanna2i2land3dan3f2na4ld4n2oney2rie3y2sa4lind8a8e7e4nne3coe3e4anne4marie"
            "7y3s2th2wan3ena3land2xana5ne2y3ce1uben3y2dd3i3yard2fus2mer2nako2skin3s4ell3ty2th4ann4erford3ledge1yan4n5e"
            "2ba2der2lan2ssa0saba3ina5y4rah3ra4ina2cha4i2de3ira2ffi3iya2gara2hale3en2idah2kari3inah3ti3ura2lihah4m5ah4"
            "na3ly3oman5e2m3antha4ra3ien4rah3mon3son3uel2ncia3ders4ia4on5r4ra5ine4ya3ford2ra4h4i5d3ee4na3gent3i4sha3ng"
            "in3ojin2sha4enka2tinka2ul3nders2vanna2wyer2xon1chuyler2otia4t1ean3rlait3son2basten6ian7en2ema2if2la3by3en"
            "a3ina3ma2mele2non3ta2rafina3gio3ilda2sha2th2ung2verin3ilin2ward2ymour1haine3kira4o3mmara3na5ta4dra5y4e4i4"
            "ley4na5on4tay5ha3rman4on4ri3shi3wn3yndel2ea3ba3ena3ffield3ila3la4by4don4ley5y3n3ridan4man4ri4win5ood2ika3"
            "n4a4g3ra4ley2obi3shana2unnar1ibley3ongile3yl2dney3onia3ra2egfried3rra2gourney2ham2las3eas3va4ia2mba3on5e2"
            "ne4ad2obhan2ran3ena3oun2tara3embile2v3an3e1kip2yler1lade2evin1mith1ofi2lana5ge3edad3ita3omon2ndra3ia3ja3y"
            "a2phia5e4ronia2rgan2terios1palding2encer4ser2ica1tacey4ia4y3ndford4ley4ton3sio2efan6ia3lla3phan7i8e5en3r4"
            "ling3sha3van4e5n3wart2ockard3ke3rm3yan2rom2uart1ubrey2katai3i2laiman3lican2mi3mer3ner2n2san5na2therland3t"
            "on2zanne1ven3tlana1ybil2delle3ney2eira2lvester4ia2na3ia0tab3ari3itha2ci4ta2d3i2ffy2hirah2i3ma3nn3pa3te2jo"
            "2ka4ra3iyah3oda2lasi3bart4ot3e3ia4tha3lulah3man3os2m3a4ra5y3ma4y2naka3ek3i3ner3o3sy3ya2o2ra3o2te3yana2uri"
            "n2wnie4y2yce3lor1eague2hya2kla2m3ina2rence5tia4se3rence4ill6yn4y3tia3yn2sia3s4a1haddeus4ea3i4s3lassa4ia3m"
            "an3n4a4e4os3ra2ea3kla3lma3obald4dore6sia4ne3ra4on2ierry3rza2omas3ra4pe2urston2yra1ia3ra2balt2enette3rnan5"
            "ey4ra2ffany2lda2mandra3othy2na2ponya2rza2tus2vona1obey3ias3y2d3d2la2mas2ng2r3a3i4n3rance3y2sia2ve2wnsend1"
            "racey4y3vers4is2easa3main7e3nt3sa3va4or3y2ianon3cia3lby3na4d3sh5a4tan2oy2udy2yne3on3phena1ucker2lly1yee2l"
            "er2mon2ne2rone0ula3ni2tima1ma1na2dine1pton1rania2iah4n5a2sula1ta0vala3entina4ria6e4ska3onia4ra2n3ce3da3es"
            "sa3ora3ya2shti2ughn1eda2lika3ma2nesssa2ra3ena3ity3n4on3onica2sta2vila1ictor6ia2donia2ncent3son2olet6ta2rg"
            "il5nia3idis2to2veka3ian1lad4imir1okes2leta3f1rinda0wade2gner2kanda2lden4o3ker3lace4y3ter2nda3eta2rd3ner3r"
            "en2tson2ylan6d4on3ne1ebb3ster2ndell4y2sley3ton2ylin1hilhelmina3taker4ney1ijdan2lfen3l4ard4em4iam4ow3ma3on"
            "a3son2nda3ema3ifred3na3ona3ston3throp1lby1oody1yatt2nee3n3ona0xanthe2veria3ier6a1ena3ia3os2rxes1imen5a1yl"
            "ia3ona0yachne2kecan2le2ncey3ice2rdley3in3milla2smeen4in1elinda2nene2rik3o3vant2smina2tta2va1okiko2landa3i"
            "e2nina2rk2vela1usuf1vella3s3tte2onne0zachariah6y3kery2da2hara3irah3ra2id4e2kia2lea3ika3tana2ndra3e3iel3n2"
            "ra4h3ed4k2za1ehava2ke2lda3enka3ia3la2na4ide3ia3on2rlinda2va3ida1ia3zan2gana2la2na3nia2on2ta2ven1oe2la2na2"
            "ra4h3da3n2sia1uleika4ma2za4nny")
        NPC_NAMES = [None]
        def npc_names():
            names = NPC_NAMES[0]
            if names is None:
                names, prev = set(), ""
                for d, rest in re.findall(r"(\d)([a-z]*)", NPC_NAMES_DATA): prev = prev[:int(d)] + rest; names.add(prev)
                NPC_NAMES[0] = names
            return names
        def layout_signature(): return tuple(tuple(v) for _, v in sorted(LAYOUT.items()))
        page = {"f": None, "seen": None, "stable": 0, "loaded": False, "lines": None, "save_at": 0.0}
        def page_ensure_loaded():
            if st["started"] or page["loaded"]: return
            reset_globals(); page["loaded"] = True
            def read():
                try: page["lines"] = read_save_lines()
                except Exception as ex: SAVE_ERR[0] = "could not read the save file: " + str(ex); page["lines"] = ()
            in_background(read)
        def page_apply_loaded():
            got = page["lines"]
            if got is None: return False
            page["lines"] = None
            if st["started"] or not got: return False
            parse_save_lines(got[0], got[1]); return True
        def page_save():
            if st["started"]: st["dirty_save"] = True
            else: page["save_at"] = time.time() + PAGE_SAVE_DELAY
        def page_flush_save(background):
            if page["save_at"]: page["save_at"] = 0.0; save_data(background=background)
        def all_locked(): return all(bool(LAYOUT[k][4]) for k in CATS + ["combat"])
        ACTIONS = {}; PAGE_OPTS = {"top": 32, "pad": 6, "ldy": 0, "sdy": 4, "fh": 26, "lw": 110, "ugap": 6}
        def page_table(w):
            right = {"dx": 320, "bdy": 0, "h": 26}
            return (("WINDOWS", (("slider", "scale", "Scale:", "Size of the trackers and pop-out bars (%d-%d)"
                         % (SCALE_MIN, SCALE_MAX), SCALE_MIN, SCALE_MAX, {"unit": "%"}),
                        ("slider", "opacity", "Opacity:", "Background opacity of every window (0-100)",
                         0, 100, {"unit": "%"}), ("slider", "range", "Range:", "Tracker range in tiles (%d-%d)"
                         % (RANGE_MIN, RANGE_MAX), RANGE_MIN, RANGE_MAX, {"unit": "tiles"}), ("gap", -78),
                        ("check", "sync", "Sync tracker sizes", "Resizing one tracker resizes the others",
                         right), ("buttons", (("unanchor", Kit.ART_CLOSE, "Unanchor all",
                                      "Undo every anchor between windows"),), right),
                        ("buttons", (("reset", Kit.ART_CLOSE, "Reset to defaults",
                                      "Reset scale, opacity, range, options and window places"),), right),
                        ("check", "lock", "Lock the windows in place",
                            "Free windows can't be moved or resized (zoned windows stay put anyway)"))), ("OPTIONS", (
                        ("check", "combat_only", "Combat bars: only once fighting", "Only add a mobile once it attacks "
                         "you, you attack it in war mode, or it fights you up close", {"stay": True}),
                        ("check", "borders", "Show a border on the pop-out bars",
                            "Stone border round the pop-out bars (the other windows always have one)",
                         {"dx": 320, "h": 28}),
                        ("check", "magery", "Magery buttons", "P (Poison) and Z (Paralyze) on the combat bars; H "
                         "(Heal) and C (Cure) on friends, Shift+click for the greater spell", {"stay": True}),
                        ("check", "healing", "Bandage button",
                            "B on friends' bars: bandage when adjacent, else follow them", {"dx": 320}))),
                                ("SIGHTINGS AND DEATHS", (("check", "sightings", "Log players who come into range",
                            "Each non-friend player goes in the Sightings log once per visit (last %d kept)"
                            % SIGHT_CAP, {"stay": True}),
                        ("buttons", (("sightings", Kit.ART_PAGE, "Open Sightings", "Open the Sightings window"),),
                         {"dx": 320}), ("check", "killer", "On death: list your attackers",
                            "A window lists players who attacked you in the last %d s, each with Add to foes"
                            % int(KILLER_BACK)))), ("FOE ALERT  (sound: Settings > Alerts)", (
                        ("check", "alert_red", "Red", "Alert on a red (murderer) in range", {"stay": True}),
                        ("check", "alert_foes", "Foe list", "Alert on a Foe list player in range (linked alts too)",
                            {"stay": True, "dx": 110}),
                        ("check", "alert_orange", "Orange", "Alert on an orange (enemy) in range",
                         {"stay": True, "dx": 230}),
                        ("check", "alert_gray", "Grey", "Alert on a grey (criminal) in range", {"dx": 340, "h": 28}),
                        ("slider", "alert_minutes", "Same player again after:",
                            "Minutes before the same player alerts again (%d-%d)" % (ALERT_MIN, ALERT_MAX), ALERT_MIN,
                                ALERT_MAX,
                         {"lw": 178, "sw": 150, "ugap": 12, "unit": "%d min" % settings["alert_minutes"]}))))
        cfg = Kit.Page(settings, page_table, opts=PAGE_OPTS)
        def build_config(g, x, y, w):
            page_ensure_loaded()
            page.update({"f": Kit.Form(g, x, y, w, dict(settings, lock=all_locked()), page_table(w), **PAGE_OPTS),
                         "stable": 0, "seen": {k: settings[k] for k in INT_ORDER}})
        def poll_config():
            f = page["f"]
            if f is None: return
            if page_apply_loaded(): page["f"] = None; HOST.refresh_settings("ultima"); return
            report_save_error(); now = time.time()
            if page["save_at"] and now >= page["save_at"]: page_flush_save(True)
            store, seen = f.store, page["seen"]; windows = views["windows"]
            if Kit.was_clicked(store, "unanchor"):
                ANCHORS.clear(); page_save(); say("every window unanchored.", Kit.HUE_GOOD)
            if Kit.was_clicked(store, "reset"):
                if views["panel"] is not None: views["panel"].reset_defaults()
                else:
                    reset_settings(); page_save()
                    say("settings and windows reset to the defaults.", Kit.HUE_GOOD)
                HOST.refresh_settings("ultima"); return
            f.vals = dict(settings, **seen); new = f.read(); sv = new["scale"]
            if sv != seen["scale"]: seen["scale"] = sv; page["stable"] = 0
            elif sv != settings["scale"]:
                page["stable"] += 1
                if page["stable"] >= 2:
                    if windows is not None: apply_scale(sv, windows)
                    else: settings["scale"] = sv; page_save()
            ov = new["opacity"]
            if ov != seen["opacity"]:
                seen["opacity"] = ov
                if views["panel"] is not None: views["panel"].set_all_opacity(ov)
                else: settings["opacity"] = ov; page_save()
            for k in ("range", "alert_minutes"):
                if new[k] == seen[k]: continue
                seen[k] = settings[k] = new[k]; page_save()
                if k == "alert_minutes": Kit.set_text(f.c["alert_minutes_lbl"], "%d min" % new[k])
            if Kit.was_clicked(store, "sightings"):
                if views["windows"] is not None: M["sight_req"] = True
                else: say("the trackers aren't up yet; try again in a moment.", Kit.HUE_INFO)
            lv = bool(new.get("lock"))
            if seen.get("lock") is None: seen["lock"] = lv
            elif lv != seen["lock"]:
                seen["lock"] = lv
                if windows is not None:
                    for k in CATS: windows[k].set_locked(lv)
                if views["panel"] is not None: views["panel"].combat.set_locked(lv)
                else:
                    for k in CATS + ["combat"]: LAYOUT[k][4] = lv
                save_settings()
            for key in ("borders", "healing", "magery", "combat_only", "sync", "alert_red",
                        "alert_foes", "alert_orange", "alert_gray", "sightings", "killer"):
                v = new[key]
                if v == settings[key]: continue
                settings[key] = v; page_save()
                if key == "borders": apply_borders_all()
                elif key == "healing" and not v: BANDAGE["serial"] = None
                elif key == "sync" and v and windows is not None:
                    ref = [windows[k] for k in CATS if not windows[k].minimized]
                    sync_sizes(windows, ref[0] if ref else windows[CATS[0]]); say("tracker sizes synced.", Kit.HUE_GOOD)
        def config_closed(): page["f"] = None; page_flush_save(True)
        M = {"last_layout": None, "tick": 0, "errors": set(),
             "next_scan": 0.0, "next_combat": 0.0, "next_glow": 0.0, "sight_req": False, "next_hp": 0.0}
        def due(key, step, now):
            t = M[key]
            if now < t <= now + step: return False
            M[key] = t + step if 0 <= now - t < step else now + step; return True
        def open_windows():
            windows, combat, panel = views["windows"], views["combat"], views["panel"]
            wins = {c: (windows[c].gump, windows[c].size) for c in CATS}
            if combat.is_open(): wins["combat"] = (combat.gump, (LAYOUT["combat"][2], 0))
            if panel.gump is not None: wins["panel"] = (panel.gump, panel.size)
            for s, pb in POPS.items(): wins["pop:%d" % s] = (pb.gump, pb.size)
            return wins
        def snapshot_all():
            for w in (views["windows"] or {}).values(): w.snapshot()
            if views["combat"] is not None: views["combat"].snapshot()
        def dock_hooks(view, title, fit):
            def state():
                if view.gump is None or st.get("shutting"): return None
                return "docked" if view.docked else ("minimized" if view.minimized else "open")
            def visible(on): Kit.set(view.gump, "IsVisible", on)
            def to(docked, mini):
                def f():
                    if view.minimized != mini: view.toggle_minimize()
                    view.docked = docked; visible(not docked)
                return f
            def undock(): view.docked = False; visible(True)
            def show():
                if view.gump is None and view is views["combat"]: TICK_JOBS.append(view.show)
                else: to(False, False)()
            return {"title": title, "icon": 0, "state": state, "show": show, "dock": to(True, True),
                    "undock": undock, "minimize": to(False, True), "gump": lambda: view.gump, "fit": fit, "exact": True,
                    "verify": True, "redraw": view.zone_chrome}
        def register_docks(windows, combat):
            for c, w in list(windows.items()) + [("combat", combat)]:
                HOST.dock_add("ultima." + c, dock_hooks(w, TITLES[c], w.layout_fit))
                cleanup.add(HOST.dock_remove, "ultima." + c)
            for key, hooks in (("ultima.sightings", SIGHT_WIN.hooks), (KILLER_WIN.KEY, KILLER_WIN.hooks)):
                HOST.dock_add(key, hooks); cleanup.add(HOST.dock_remove, key)
        def reset_globals():
            for d in (FOES, IGNORE, PLAYER_NAMES, POPS, LAST_CLICK, cb_engaged, CLICK_MODS, FRIEND_Q, NOTE_CACHE,
                      LAST_SEEN, ALT_OF, ALERT_PREV, ATTACKERS, FOE_CHG): d.clear()
            FILE_MT[0] = None; MERGE_WAIT[0] = GONE[0] = 0.0; PEND[0] = 0
            for q in (DOCK_REQ, cb_pending_click, cb_pending_spell, CHROMES, CLICK_Q, THREAD_JOBS, TICK_JOBS, SIGHTS):
                del q[:]
            PLAYER_VER[0] += 1; reset_layout(); settings.update(DEFAULTS)
            FIT.update(req=False, size={}, own_size={}, force=set(), made={}); st.update(STATE_DEFAULTS, party=set())
            BANDAGE.update(serial=None, follow=None); ANCHORS.__init__(); cb_casting.update(serial=None, stale=False)
            SAVE_REQ[0] = DATA_READY[0] = False; page.update({"loaded": False, "lines": None, "save_at": 0.0})
            JREAD["learn"] = JREAD["attack"] = JREAD["killer"] = None; LT_SKIP.update(serial=None, until=0.0)
            FOE_WHERE[0] = -10.0
            for what in list(CURSOR_OWN): release_cursor(what)
            SIGHT.update(dirty=False, save_at=0.0); SIGHT["ver"] += 1; SIGHT["seen_ver"] += 1; LINK_PICK[0] = None
            WATCH["dead"] = WATCH["me"] = None
        def _start():
            pending = None
            if page["save_at"]: page["save_at"] = 0.0; pending = save_text()
            reset_globals(); st["started"] = True
            for k in JREAD: JREAD[k] = Journal.reader()
            init_native_art(); M["errors"] = set(); HOST.alert_kind(ALERT_KEY, "Foe in range", ALERT_SOUND)
            cleanup.service("ultima.is_foe", is_foe); cleanup.service("ultima.classify", classify_service)
            cleanup.service("look.ultima", lambda: TICK_JOBS.append(redo_look))
            THREAD_JOBS.append(lambda: load_job(pending))
        def load_job(pending_text=None):
            if st["shutting"]: return
            if pending_text is not None: SAVE_SEQ[0] += 1; write_text(pending_text, SAVE_SEQ[0]); report_save_error()
            load_settings(); ANCHORS.saved = ANCHORS.saved_groups(); load_old_combat_settings(); st["loaded"] = True
        def _tick():
            if views["windows"] is None:
                if st["loaded"] and not st["shutting"]: build_window()
                return
            report_save_error(); run_clicks(); run_jobs(TICK_JOBS)
            while DOCK_REQ: HOST.dock_to_bar(DOCK_REQ.pop(0))
            if SETTINGS_REQ: del SETTINGS_REQ[:]; HOST.show_settings(KEY)
            windows, combat, panel = views["windows"], views["combat"], views["panel"]
            if windows is None: return
            fit_tick(windows); now = time.time()
            try:
                try:
                    if M["sight_req"]: M["sight_req"] = False; SIGHT_WIN.bring()
                    SIGHT_WIN.tick(now); KILLER_WIN.tick(now)
                except Exception as ex:
                    if HOST.stopping(): return
                    report_error(ex)
                handle_spells(); handle_bandage(); ANCHORS.tick(open_windows)
                if ANCHORS.groups_changed(): st["dirty_save"] = True
                if due("next_glow", GLOW_EVERY, now):
                    a = glow_alpha(); windows["friend"].pulse(a)
                    for pb in list(POPS.values()): pb.pulse(a)
                if due("next_scan", TICK_SECONDS, now):
                    buckets = scan()
                    try: watch_tick(now)
                    except Exception as ex: report_error(ex)
                    if stopping(): return
                    for c in CATS: windows[c].update(buckets[c])
                    for pb in list(POPS.values()): pb.update()
                    if stopping(): return
                    process_size_sync(windows); panel.update(); check_follow(); M["tick"] += 1
                    if M["tick"] % SAVE_EVERY == 0:
                        snapshot_all(); sig = layout_signature()
                        if sig != M["last_layout"] or st["dirty_save"] or (SIGHT["dirty"] and now >= SIGHT["save_at"]):
                            M["last_layout"] = sig; save_settings()
                if due("next_combat", TICK_SECONDS if combat.docked else COMBAT_TICK_SECONDS, now) and not stopping():
                    combat.tick()
                if due("next_hp", HP_EVERY, now) and not stopping(): hp_tick(windows, combat)
            except Exception as ex:
                if HOST.stopping(): return
                report_error(ex)
        def hp_tick(windows, combat):
            for w in windows.values():
                if w.minimized or w.docked or not Kit.is_open(w.gump): continue
                for r in w.rows:
                    e = r.e
                    if not r.shown or not e or not e["hmax"] or e.get("mob") is None: continue
                    try: hits, hmax = e["mob"].Hits or 0, e["mob"].HitsMax or 0
                    except Exception: continue
                    if hmax > 0: e["hits"], e["hmax"] = hits, hmax; r.values(e)
            if combat is None or combat.docked or combat.minimized or not Kit.is_open(combat.gump): return
            for r in combat.rows:
                d = r.e
                if not r.shown or d is None: continue
                m = cb_snap.get(d[0])
                if m is None: continue
                try: hp = (m.Hits or 0, m.HitsMax or 0)
                except Exception: continue
                if hp[1] > 0 and hp != d[3:5]: r.values(d[:3] + hp + d[5:])
        def _thread_tick():
            if run_jobs(THREAD_JOBS): return
            if SAVE_REQ[0]: SAVE_REQ[0] = False; save_data(background=True)
        def _thread_wanted(): return bool(THREAD_JOBS) or bool(SAVE_REQ[0])
        def _stop():
            st["shutting"] = True; st["started"] = False; SIGHT_WIN.close(stopping=True); KILLER_WIN.close()
            cleanup.close()
            for what in list(CURSOR_OWN): release_cursor(what)
            if views["windows"] is None: return
            safe(lambda: Kit.on_client(snapshot_all)); SAVE_REQ[0] = False; save_data(); gumps = []
            for w in views["windows"].values(): gumps.append(w.gump); w.gump = None
            if views["combat"] is not None: gumps.append(views["combat"].gump); views["combat"].gump = None
            if HOST.hub is not None: HOST.hub.remove("ultima")
            for pb in list(POPS.values()): gumps.append(pb.gump); pb.gump = None
            POPS.clear()
            for g in gumps: Kit.dispose(g)
            end_follow(BANDAGE["follow"]); views.update({"windows": None, "combat": None, "panel": None})
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": build_config, "poll_config": poll_config, "config_closed": config_closed,
                "thread_tick": _thread_tick, "thread_wanted": _thread_wanted}
    def _part_lookout():
        KEY = "lookout"; TITLE = "Lookout"; SETTINGS_KEY = "Lookout_settings"; POS_KEY = "Lookout_pos"
        MIN_KEY = "Lookout_min"; FEED_NAME = "_lookout_feed.txt"; W = 370; MINI_W, MINI_H = 280, 46; TRAY_ICON = 0x0A25
        ROWS = 5; RECENT_CAP = 30; ROW_H = 22; DEFAULT_RANGE = 18; RANGE_MIN, RANGE_MAX = 3, 24; SCAN_EVERY = 0.25
        GONE_SECONDS = 30.0
        HEARTBEAT = 5.0; LOST_SECONDS = 20.0; LISTEN_EVERY = 0.1; FEED_MAX_AGE = 15.0; FEED_MAX_BYTES = 32768
        FEED_KEEP = 60; READ_MAX = 65536; ANNOUNCE_EVERY = 30.0; LISTENER_TTL = 120.0; LISTENERS_EVERY = 10.0
        OUTBOX_CAP = 200; WRITE_RETRY = 1.0; SEEN_CAP = 400; PRESENT_CAP = 1000; WATCHERS_CAP = 8; PING_GIVE_UP = 10.0
        PING_RETRY = 0.25; ALERT_ALARM = "lookout.alarm"; ALERT_ALARM_SOUND = 0x338; ALERT_LOST = "lookout.lost"
        ALERT_LOST_SOUND = 0x04A; OWN_ALARM_HOLD = 60.0; ARROW_ID = 0x4C4F4F4B
        ROW_TIP = ("Click: tracking arrow to where they were seen (again to clear). "
                   "Alt+click: auto-follow (again to stop)")
        settings = {"watch": False, "listen": True, "range": DEFAULT_RANGE, "ping": True, "lost": True}
        DEFAULTS = dict(settings)
        def fresh():
            return {"shutting": False, "minimized": False, "docked": False, "queue": [], "me": 0, "path": None,
                    "facet": -1, "next_scan": 0.0, "present": {}, "in_range": 0, "hb_next": 0.0, "outbox": [],
                    "write_next": 0.0, "pings": [], "ping_next": 0.0, "listeners": {}, "listeners_next": 0.0,
                    "offset": 0, "listen_next": 0.0, "announce_next": 0.0, "seen": {}, "inbox": [], "watchers": {},
                    "file": "none", "recent": [], "arrow": None, "own_alarm": None, "dirty": True, "refresh_at": 0.0}
        st = {"minimized": False, "shutting": False, "docked": False, "queue": []}; st.update(fresh())
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}
        cleanup = Kit.Cleanup(); queue = Kit.queuer(st); say = Kit.sayer(TITLE)
        NUMS, ORDER = {"range": (RANGE_MIN, RANGE_MAX)}, ("watch", "listen", "range", "ping", "lost")
        def load_settings(): Kit.kv_load(SETTINGS_KEY, ";", settings, NUMS)
        def save_settings(): Kit.kv_save(SETTINGS_KEY, ";", settings, ORDER, NUMS)
        def feed_path():
            p = st["path"]
            if p is None: p = st["path"] = Kit.data_path(FEED_NAME)
            return p
        def due(now, key, step):
            t = st[key]
            if now >= t or t - now > step: st[key] = now + step; return True
            return False
        def clean(text): return str(text or "").replace("|", "/").replace("\n", " ").replace("\r", " ").strip()
        def where_text(ev, short=False):
            lx, ly = ev["lx"], ev["ly"]
            if not (lx or ly): return "at %d,%d" % (ev["x"], ev["y"])
            dx, dy = ev["x"] - lx, ev["y"] - ly; d = max(abs(dx), abs(dy))
            if d == 0: return "at the lookout"
            if short: return "%d %s" % (d, Kit.compass(dx, dy))
            return Kit.where_text(dx, dy) + " of the lookout"
        def line(serial, name, noto, x, y, facet, count, lx, ly, pinged=False):
            s = "%.2f|%d|%s|%s|%d|%d|%d|%d|%d|%d|%d|%d\n" % (
                time.time(), serial, clean(name), clean(noto), x, y, facet, count, lx, ly, st["me"], 1 if pinged else 0)
            return s.encode("utf-8")
        def post(data):
            ob = st["outbox"]; ob.append(data)
            if len(ob) > OUTBOX_CAP: del ob[:-OUTBOX_CAP]
        def parse(raw):
            try:
                s = raw.decode("utf-8", "replace").strip()
                if not s: return None
                p = s.split("|")
                if len(p) < 8: return None
                ev = {"t": float(p[0]), "key": p[0], "serial": int(p[1]), "name": p[2],
                      "noto": p[3], "x": int(p[4]), "y": int(p[5]), "facet": int(p[6]), "count": int(p[7]),
                      "lx": int(p[8]) if len(p) > 8 else 0, "ly": int(p[9]) if len(p) > 9 else 0,
                      "from": int(p[10]) if len(p) > 10 else 0, "pinged": len(p) > 11 and p[11] == "1"}
                if not 0.0 < ev["t"] < 1e11: return None
                return ev
            except Exception: return None
        def write_outbox():
            ob = st["outbox"]; n = len(ob); path = feed_path()
            try:
                with open(path, "ab") as f: f.write(b"".join(ob[:n]))
            except Exception: st["write_next"] = time.time() + WRITE_RETRY; return
            del ob[:n]
            try: size = os.path.getsize(path)
            except Exception: return
            if size > (FEED_MAX_BYTES if settings["watch"] else 4 * FEED_MAX_BYTES): trim(path)
        def trim(path):
            try:
                with open(path, "rb") as f: data = f.read()
                cut = data.rfind(b"\n") + 1; data = data[:cut]
                lines = [ln for ln in data.split(b"\n") if ln.strip()]; keep = lines[-FEED_KEEP:]; heard = set()
                for ln in reversed(lines[:-FEED_KEEP]):
                    if b"|listen|" in ln and len(heard) < WATCHERS_CAP:
                        ev = parse(ln)
                        if ev is not None and ev["from"] not in heard: heard.add(ev["from"]); keep.insert(0, ln)
                def since():
                    with open(path, "rb") as f: f.seek(cut); return f.read()
                Kit.write_safe(path, b"\n".join(keep) + (b"\n" if keep else b""), tail=since)
            except Exception: pass
        def read_new(path):
            try: size = os.path.getsize(path)
            except Exception: st["file"] = "none"; return None
            off = st["offset"]
            if size < off: off = 0
            if size - off > READ_MAX: off = size - READ_MAX; skip_first = True
            else: skip_first = off > 0 and off != st["offset"]
            if size == off: st["offset"] = off; st["file"] = "ok"; return None
            try:
                with open(path, "rb") as f: f.seek(off); data = f.read(min(size - off, READ_MAX))
            except Exception: st["file"] = "busy"; return None
            st["file"] = "ok"; cut = data.rfind(b"\n")
            if cut < 0: st["offset"] = off + len(data) if len(data) >= READ_MAX else off; return None
            st["offset"] = off + cut + 1; lines = data[:cut].split(b"\n")
            if skip_first and lines: lines = lines[1:]
            return lines
        def read_feed(now):
            lines = read_new(feed_path())
            if not lines: return
            me = st["me"]; seen = st["seen"]; inbox = st["inbox"]
            for raw in lines:
                ev = parse(raw)
                if ev is None or ev["from"] == me or ev["noto"] == "listen": continue
                k = (ev["key"], ev["serial"], ev["from"])
                if k in seen: continue
                age = now - ev["t"]
                if age < -5.0 or (ev["serial"] and age > FEED_MAX_AGE): continue
                seen[k] = ev["t"]; inbox.append(ev)
            if len(seen) > SEEN_CAP:
                cut = now - 4 * FEED_MAX_AGE
                for k in [k for k, t in seen.items() if t < cut]: del seen[k]
                if len(seen) > SEEN_CAP:
                    newest = sorted(seen.items(), key=lambda kv: kv[1])[-(SEEN_CAP // 2):]; seen.clear()
                    seen.update(newest)
            if len(inbox) > 100: del inbox[:-100]
        def read_listeners(now):
            path = feed_path()
            try:
                size = os.path.getsize(path)
                with open(path, "rb") as f:
                    if size > READ_MAX: f.seek(size - READ_MAX)
                    data = f.read(READ_MAX)
            except Exception: return
            out = {}
            for raw in data.split(b"\n"):
                if b"|listen|" not in raw: continue
                ev = parse(raw)
                if ev is not None and ev["noto"] == "listen" and ev["from"] and -5.0 <= now - ev["t"] <= LISTENER_TTL:
                    out[ev["from"]] = ev["t"]
            st["listeners"] = out
        def own_check(m, serial):
            if m.IsRenamable: return None
            noto = Kit.noto_name(m)
            if noto in ("invulnerable", "ally"): return None
            if not (m.IsHuman or m.IsGargoyle): return None
            if API.IsFriend(serial): return None
            if NPC_TITLE_RE.search(str(m.Name or "")): return None
            return noto
        def watch_scan(now):
            p = HOST.me()
            if p is None: return
            me = int(p.Serial)
            mx, my = int(p.X), int(p.Y); facet = int(API.GetMap()); st["me"], st["facet"] = me, facet
            mobs = HOST.mobiles(settings["range"]); party = set(int(s) for s in (API.GetPartyMemberSerials() or ()))
            svc = HOST.services.get("ultima.classify"); listeners = st["listeners"]; counted = []
            for m in mobs:
                try:
                    if m is None: continue
                    serial = int(m.Serial)
                    if serial == me or serial in party or serial in listeners: continue
                    if svc is not None:
                        r = svc(m, party)
                        if r is None or r[0] == "friend" or r[3]: continue
                        noto = r[2]
                    else:
                        if m.IsDead: continue
                        noto = own_check(m, serial)
                        if noto is None: continue
                    if API.OnIgnoreList(serial): continue
                    counted.append((serial, m, noto))
                except Exception: continue
            present = st["present"]; fresh = []
            for serial, m, noto in counted:
                t = present.get(serial)
                if t is None or now - t > GONE_SECONDS: fresh.append((serial, m, noto))
                present[serial] = now
            if len(present) > len(counted):
                for s in [s for s, t in present.items() if not 0 <= now - t <= GONE_SECONDS]: del present[s]
                if len(present) > PRESENT_CAP: present.clear()
            n = len(counted)
            if n != st["in_range"]: st["in_range"] = n; st["dirty"] = True
            ping_on = settings["ping"] and HOST.services.get("pings.send") is not None; said = []
            for serial, m, noto in fresh:
                try: name, x, y = str(m.Name or "") or "(unknown)", int(m.X), int(m.Y)
                except Exception: continue
                will_ping = ping_on and len(st["pings"]) < 8
                post(line(serial, name, noto, x, y, facet, n, mx, my, will_ping))
                if will_ping: st["pings"].append([x, y, facet, "Lookout: " + name, now + PING_GIVE_UP])
                ev = {"t": now, "serial": serial, "name": name, "noto": noto, "x": x, "y": y,
                      "facet": facet, "count": n, "lx": mx, "ly": my, "src": "here"}
                remember(ev); said.append("%s (%s)" % (name, NOTO_WORD.get(noto, noto)))
            if said:
                say("spotted %s, %s in range." % (", ".join(said[:4]) + (" and %d more" % (len(said) - 4) if
                                                                len(said) > 4 else ""), Kit.count(n, "player")))
            if fresh or due(now, "hb_next", HEARTBEAT):
                st["hb_next"] = now + HEARTBEAT; post(line(0, "", "watch", mx, my, facet, n, mx, my))
        def send_pings(now):
            jobs = st["pings"]
            if not jobs or (now < st["ping_next"] and st["ping_next"] - now <= PING_RETRY): return
            fn = HOST.services.get("pings.send")
            if fn is None or not settings["ping"]: del jobs[:]; return
            x, y, m, who, until = jobs[0]
            if not 0 <= until - now <= PING_GIVE_UP: jobs.pop(0); return
            try: ok = fn(x, y, m, "danger", who)
            except Exception: ok = True
            if ok: jobs.pop(0)
            else: st["ping_next"] = now + PING_RETRY
        def watch_off():
            st["present"].clear(); st["in_range"] = 0; del st["pings"][:]
            if st["me"]: post(line(0, "", "off", 0, 0, st["facet"], 0, 0, 0))
            st["dirty"] = True
        def remember(ev): rec = st["recent"]; rec.insert(0, ev); del rec[RECENT_CAP:]; st["dirty"] = True
        def heard(ev, now):
            ws = st["watchers"]; w = ws.get(ev["from"])
            if w is None:
                if len(ws) >= WATCHERS_CAP: del ws[min(ws, key=lambda k: ws[k]["t"])]
                w = ws[ev["from"]] = {"t": 0.0, "told": False}
            if ev["t"] < w["t"]: return
            w.update({"t": ev["t"], "state": ev["noto"], "x": ev["x"], "y": ev["y"],
                      "facet": ev["facet"], "count": ev["count"]})
            w["told"] = ev["noto"] != "watch" or not -5.0 <= now - ev["t"] <= LOST_SECONDS; st["dirty"] = True
        def raise_alarm(ev):
            noto = ev["noto"]
            text = "%s (%s)%s, %s" % (ev["name"], NOTO_WORD.get(noto, noto),
                                       (", %d players" % ev["count"]) if ev["count"] > 1 else "", where_text(ev))
            if ev["facet"] != st["facet"] and st["facet"] >= 0: text += " in " + Kit.facet_name(ev["facet"])
            ping = None
            if settings["ping"] and not ev["pinged"] and ev["facet"] == st["facet"] and \
                    HOST.services.get("pings.send") is not None:
                ping = (ev["x"], ev["y"])
            HOST.alert(ALERT_ALARM, text, level="alarm", ping=ping, who=ev["serial"])
            st["own_alarm"] = (text, time.time()); ev["src"] = "lookout"; remember(ev)
        def listen_tick(now):
            inbox = st["inbox"]
            if inbox:
                items, st["inbox"] = inbox, []
                for ev in items:
                    if ev["serial"]: raise_alarm(ev)
                    else: heard(ev, now)
            if not settings["lost"]: return
            for frm, w in st["watchers"].items():
                if w["told"] or w.get("state") != "watch": continue
                age = now - w["t"]
                if age > LOST_SECONDS:
                    w["told"] = True; st["dirty"] = True
                    HOST.alert(ALERT_LOST, "Lookout quiet for %d s" % int(age), level="warn", who=frm)
        def row_handler(i):
            def handler():
                rows = win["rows"]
                if i >= len(rows): return
                r = rows[i]; ev = r["ev"]
                if r["prev"] is not None and time.time() - r["at"] <= 0.15: ev = r["prev"]
                if ev is None: return
                if Follow.alt_held(): queue(("follow", ev["serial"]))(); return
                queue(("arrow", ev["x"], ev["y"], ev["facet"]))()
            return handler
        def body_y(): return Kit.MARGIN + 30 + Kit.GAP
        SEC_A = 58
        def full_h(n=ROWS): return body_y() + SEC_A + Kit.GAP + 30 + n * ROW_H + 6 + Kit.MARGIN
        def build_window():
            z = wnd.slot if Kit.zone_up(KEY) and not st["minimized"] else None
            if z is not None and (z[0] < W or z[1] < full_h(1)): z = None
            w, h = z if z else (W, full_h()); n = wnd.rows(ROW_H, full_h(0), ROWS) if z else ROWS
            g, store, c = wnd.begin(w, h); M = Kit.MARGIN; rows = []
            if not st["minimized"]:
                IW = w - 2 * M; wnd.frame(g); c["info_w"] = IW - 196
                ya = body_y(); Kit.add_section(g, M, ya, IW, SEC_A); xc = w - M - 12 - 35 - Kit.text_w("Clear")
                Kit.art_button(g, store, "clear", Kit.ART_CLOSE, xc, ya + 28, "Clear",
                               "Clear the list, alarm line and tracking arrow", on_click=queue("clear"))
                c["watch"] = Kit.add_label(g, "", M + 12, ya + 9, Kit.HUE_INFO)
                c["listen"] = Kit.add_label(g, "", M + 12, ya + 32, Kit.HUE_INFO)
                c["tw"] = (IW - 24, xc - 8 - (M + 12)); yb = ya + SEC_A + Kit.GAP
                Kit.add_section(g, M, yb, IW, h - yb - M, "SPOTTED  (newest first)")
                for i in range(n):
                    yr = yb + 28 + i * ROW_H
                    r = {"name": Kit.add_label(g, "", M + 12, yr + 2, Kit.HUE_TEXT),
                         "info": Kit.add_label(g, "", M + 12 + 180, yr + 2, Kit.HUE_INFO),
                         "ev": None, "prev": None, "at": 0.0, "tip": None, "shown": True}
                    r["hit"] = Kit.catcher(g, M + 6, yr, IW - 12, ROW_H, row_handler(i), ""); rows.append(r)
            wnd.end(g, {"rows": rows}); st["dirty"] = True; refresh(time.time())
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, (220, 220), (MINI_W, MINI_H), TRAY_ICON,
                         cleanup, lock=True, clear={"rows": []})
        def watch_text():
            if not settings["watch"]: return "off", Kit.HUE_INFO
            n = st["in_range"]
            if n: return "%d tiles, %s in range" % (settings["range"], Kit.count(n, "player")), Kit.HUE_BAD
            return "%d tiles, all clear" % settings["range"], Kit.HUE_GOOD
        def listen_text(now):
            if not settings["listen"]: return "off", Kit.HUE_INFO
            best = None
            for w in st["watchers"].values():
                if best is None or w["t"] > best["t"]: best = w
            if best is None:
                if st["file"] == "busy": return "the feed is busy, trying again", Kit.HUE_INFO
                return "no lookout heard yet", Kit.HUE_INFO
            age = Kit.ago(now - best["t"], Kit.AGO_SHORT)
            if best.get("state") == "off": return "the lookout stopped %s ago" % age, Kit.HUE_INFO
            if not -5.0 <= now - best["t"] <= LOST_SECONDS:
                return "the lookout has been quiet for %s" % age, Kit.HUE_BAD
            n = best.get("count", 0); where = "%d,%d" % (best.get("x", 0), best.get("y", 0))
            if n: return "the lookout at %s sees %s" % (where, Kit.count(n, "player")), Kit.HUE_BAD
            return "the lookout at %s, all clear" % where, Kit.HUE_GOOD
        def mini_text(now):
            a = st["own_alarm"]
            if a is not None and 0 <= now - a[1] <= OWN_ALARM_HOLD: text, hue = a[0], Kit.HUE_BAD
            elif settings["listen"]: text, hue = listen_text(now)
            else: text, hue = watch_text()
            return "%s: %s" % (TITLE, text), hue
        def show_row(r, ev, now):
            if ev is not r["ev"]: r["prev"], r["ev"], r["at"] = r["ev"], ev, now
            if ev is None:
                if r["shown"]:
                    Kit.set_text(r["name"], ""); Kit.set_text(r["info"], ""); Kit.set(r["hit"], "IsVisible", False)
                    r["shown"] = False
                return
            if not r["shown"]: Kit.set(r["hit"], "IsVisible", True); r["shown"] = True
            noto = ev["noto"]
            Kit.set_text(r["name"], Kit.fit("%s (%s)" % (ev["name"], NOTO_WORD.get(noto, noto)), 172),
                         NOTO_HUE.get(noto, Kit.HUE_TEXT))
            src = "lookout" if ev.get("src") == "lookout" else "here"
            where = where_text(ev, True) if src == "lookout" else "%d,%d" % (ev["x"], ev["y"])
            Kit.set_text(r["info"], Kit.fit("%s, %s ago (%s)" % (where, Kit.ago(now - ev["t"], Kit.AGO_SHORT), src),
                                            win["c"]["info_w"]))
            tip = "%s (%s), seen %s at %d,%d%s. %s" % (
                ev["name"], NOTO_WORD.get(noto, noto), "by the lookout" if src == "lookout" else "here",
                ev["x"], ev["y"], "" if ev["facet"] == st["facet"] else " in " + Kit.facet_name(ev["facet"]), ROW_TIP)
            if tip != r["tip"]: r["tip"] = tip; Kit.with_tip(r["hit"], tip)
        def refresh(now):
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]): return
            c = win["c"]
            if st["minimized"]:
                text, hue = mini_text(now); Kit.set_text(c["status"], Kit.fit(text, MINI_W - 90), hue); return
            tw = c["tw"]; text, hue = watch_text(); Kit.set_text(c["watch"], Kit.fit("Watch: " + text, tw[0]), hue)
            text, hue = listen_text(now); a = st["own_alarm"]
            if a is not None and 0 <= now - a[1] <= OWN_ALARM_HOLD: text, hue = a[0], Kit.HUE_BAD
            else: text = "Listen: " + text
            Kit.set_text(c["listen"], Kit.fit(text, tw[1]), hue); rec = st["recent"]; rows = win["rows"]
            for i, r in enumerate(rows): show_row(r, rec[i] if i < len(rec) else None, now)
            if not rec and rows: Kit.set_text(rows[0]["name"], "No one spotted yet.", Kit.HUE_INFO)
        def toggle_arrow(x, y, m):
            here = st["facet"]; cur = st["arrow"]; API.TrackingArrow(-1, -1, ARROW_ID); st["arrow"] = None
            if cur == (x, y, m): return
            if here >= 0 and m != here:
                say("that spot is in %s." % Kit.facet_name(m)); return
            API.TrackingArrow(x, y, ARROW_ID); st["arrow"] = (x, y, m)
        def clear_arrow():
            if st["arrow"] is not None: st["arrow"] = None; API.TrackingArrow(-1, -1, ARROW_ID)
        def clear_recent(action): st["recent"] = []; st["own_alarm"] = None; clear_arrow(); st["dirty"] = True
        ACTIONS = {"clear": clear_recent, "follow": lambda action: Follow.toggle(action[1], TITLE),
                   "arrow": lambda action: toggle_arrow(action[1], action[2], action[3])}
        def page_table(w):
            return (("WATCH AND LISTEN  (two clients, one TazUO folder)", (
                        ("check", "watch", "Watch: this client is the lookout",
                            "Park it hidden and still; it reports every player in range to the other client "
                         "(not party, friends or guild)"), ("check", "listen", "Listen: this client gets the alarms",
                            "Alarm for each player a lookout reports (sound: Settings > Alerts)"),
                        ("slider", "range", "Watch range:", "Watch range in tiles (%d-%d)"
                         % (RANGE_MIN, RANGE_MAX), RANGE_MIN, RANGE_MAX,
                         {"ldy": 6, "sdy": 4, "lw": 98, "sw": 160, "ugap": 10, "vfmt": "%d tiles", "h": 32}),
                        ("check", "ping", "Danger ping on the map where a player is spotted",
                            "Needs World Map > Map Pings; guildmates see it too"),
                        ("check", "lost", "Warn when the lookout is quiet for %d s" % int(LOST_SECONDS),
                         "Its client closed, crashed or lost the connection")), {"top": 32, "pad": 4}),)
        def on_change(old, new):
            for k in ("watch", "listen", "ping", "lost"):
                if new[k] != old[k]: apply_toggle(k, new[k])
            st["dirty"] = True
        def apply_toggle(k, on):
            if k == "watch":
                if on: st["next_scan"] = st["hb_next"] = st["listeners_next"] = 0.0
                else: watch_off()
            elif k == "listen":
                if on: st["listen_next"] = st["announce_next"] = 0.0
                else: st["inbox"] = []
            elif k == "ping" and not on: del st["pings"][:]
            st["refresh_at"] = time.time()
        cfg = Kit.Page(settings, page_table, save_settings, on_change); load_settings()
        def _start():
            st.update(fresh(), minimized=wnd.start_min()); load_settings()
            p = API.Player; st["me"] = int(p.Serial) if p is not None else 0; st["facet"] = int(API.GetMap())
            feed_path(); HOST.alert_kind(ALERT_ALARM, "Lookout spotted a player", ALERT_ALARM_SOUND)
            HOST.alert_kind(ALERT_LOST, "Lookout went quiet", ALERT_LOST_SOUND); build_window()
            wnd.dock(fit=True, min=(W, full_h(1)))
        def _tick():
            if win["g"] is None: return
            if Kit.closed(win): return
            while st["queue"]:
                action = st["queue"].pop(0)
                if wnd.action(action): continue
                fn = ACTIONS.get(action[0] if isinstance(action, tuple) else action)
                if fn is not None: fn(action)
            now = time.time()
            if settings["watch"]:
                if due(now, "next_scan", SCAN_EVERY): watch_scan(now)
                send_pings(now)
            elif settings["listen"] and due(now, "next_scan", 1.0):
                p = API.Player
                if p is not None: st["me"] = int(p.Serial); st["facet"] = int(API.GetMap())
            if settings["listen"]: listen_tick(now)
            if st["dirty"] or due(now, "refresh_at", 1.0): st["dirty"] = False; refresh(now)
        def _thread_tick():
            if st["shutting"]: return
            now = time.time()
            if settings["listen"] and st["me"] and due(now, "announce_next", ANNOUNCE_EVERY):
                post(line(0, "", "listen", 0, 0, st["facet"], 0, 0, 0))
            if st["outbox"] and (now >= st["write_next"] or st["write_next"] - now > WRITE_RETRY): write_outbox()
            if settings["watch"] and due(now, "listeners_next", LISTENERS_EVERY): read_listeners(now)
            if settings["listen"] and st["me"] and due(now, "listen_next", LISTEN_EVERY): read_feed(now)
        def _thread_wanted():
            if st["shutting"]: return False
            now = time.time()
            if settings["listen"] and st["me"]: return True
            if st["outbox"] and not 0 < st["write_next"] - now <= WRITE_RETRY: return True
            return bool(settings["watch"]) and not 0 < st["listeners_next"] - now <= LISTENERS_EVERY
        def _stop():
            st["shutting"] = True
            if settings["watch"] and st["me"]: post(line(0, "", "off", 0, 0, st["facet"], 0, 0, 0)); write_outbox()
            clear_arrow(); save_settings(); cleanup.close()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed,
                "thread_tick": _thread_tick, "thread_wanted": _thread_wanted}
    PARTS = (("tracker", _part_tracker, 0.05, "ultima"), ("lookout", _part_lookout, 0.1, "lookout"),)
    return PartSet(KEY, TITLE, PARTS).hooks()


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("ultima", "Ultima Tracker", "Friends, foes and neutrals near you",
         _module_ultima, 0.05, category="The world", parts=(("tracker", "Tracker",
              "Trackers and combat bars", True, ("ultima",)), ("lookout", "Lookout",
              "A second client keeps watch", False, ("lookout",)),),
         aliases=('Combat Bars', 'Lookout', 'foe', 'sightings', 'trackers', 'second client'))
