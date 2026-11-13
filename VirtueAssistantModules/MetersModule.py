def _module_meters():
    KEY = "meters"; TITLE = "Meters"; SETTINGS_KEY = "Meters_settings"; WINS_KEY = "Meters_windows"; W = 360
    SIZE_MIN_W = 240; SIZE_MAX_W = 1200; RESIZE_SETTLE = 0.35; ZONE_EVERY = 0.5; MINI_W, MINI_H = 320, 46; PICK_W = 360
    SIZE_MAX_H = 4000; POS_MAX = 100000; WIN_ID_MAX = 10000
    DETAIL_W = 300; ROW_H = 20; VAL_W = 146; MAX_WINDOWS = 6; TRAY_ICON = 0x0EEF; ART_LEFT = (4014, 4016, 4015)
    BAR_BG = "#17171a"; UI_EVERY = 1.0; UI_SOON = 0.25; FRIENDS_EVERY = 3.0; SCAN_EVERY = 2.0; WATCH_SECS = 30.0
    KILL_CREDIT_SECS = 30.0; PET_RANGE = 18; JUMP_TILES = 12; DEATH_BIT = 0x80000000; GOLD_GRAPHIC = 0x0EED
    HEAL_SPELL_SECS = 8.0; BANDAGE_SECS = 2.0; POTION_SECS = 2.5; CURE_SECS = 8.0; ORPHAN_SECS = 1.5; MANA_SECS = 4.0
    BIG_KEEP = 25; REPORT_ROWS = 5; HOOK_KEY = "VirtueMeters.DamageHook"; DAMAGE_QUEUE_MAX = 4000; PARTY_MSG_MAX = 220
    DYING_CHECK_SECS = WATCH_SECS / 2; WATCH_MAX = 40; FEED_BURST = 600; MOBS_MAX = 800; SPOTS_KEY = "Meters_spots"
    SPOTS_MAX = 20; SPOT_NAME_MAX = 24; SPOT_RADIUS = 20; SPOT_RADIUS_LIMITS = (1, 300); PLACE_EVERY = 1.0
    PLACE_ELSEWHERE = "Elsewhere"; PLACE_MIN_SECS = 60.0; GRAPH_MINUTES = 60; GRAPH_H = 40; GRAPH_COL = 4
    GRAPH_BLOCK = 18 + GRAPH_H + 4; EXPORT_FILE = "Meters_%08X.txt"; EXPORT_ROWS = 50; RECAP_SECS = 10.0
    RECAP_ROWS = 12; RECAP_COLS = 40; RECAP_W = 360; RECAP_POS_KEY = "Meters_recap_pos"
    RECAP_HINT = ("Who: spell words heard before the hit,", "else whom you fought (marked ?).")
    TAKEN_KEEP = 200; HP_KEEP = 300; CASTS_KEEP = 20; CAST_CREDIT_SECS = 4.0; CAST_EARLY = 0.5; CORPSE_SECS = 3600.0
    HARM_SET = frozenset(("Magic Arrow", "Harm", "Fireball", "Lightning", "Mind Blast",
                   "Energy Bolt", "Explosion", "Flamestrike", "Chain Lightning",
                   "Meteor Swarm", "Earthquake", "Poison", "Poison Field", "Fire Field",
                   "Holy Light", "Pain Spike", "Poison Strike", "Strangle", "Wither"))
    MSG_BANDAGE_BEGIN = "you begin applying the bandages"
    MSG_BANDAGE_HEALS = ("you finish applying the bandages", "you heal what little damage",
                         "you apply the bandages, but they barely help")
    MSG_BANDAGE_CURE = "you have cured the target of all poisons"; MSG_FIZZLE = "the spell fizzles"
    MSG_INTERRUPT = "your concentration is disturbed"; MSG_NO_MANA = "insufficient mana"
    RE_SKILL = re.compile(r"your skill in (.+?) has (increased|decreased) by " r"([0-9]+(?:\.[0-9]+)?)", re.I)
    RE_STAT = re.compile(r"your (strength|dexterity|intelligence) has (increased|decreased) by " r"([0-9]+)", re.I)
    RE_FAME = re.compile(r"you have (gained|lost) .*?\b(fame|karma)\b", re.I); SPELLS = Kit.SPELL_WORDS
    POTIONS = {0x0F0C: ("Heal", "heal"), 0x0F07: ("Cure", "cure"), 0x0F0B: ("Refresh", None),
               0x0F09: ("Strength", None), 0x0F08: ("Agility", None),
               0x0F0D: ("Explosion", None), 0x0F06: ("Night Sight", None), 0x0F0A: ("Poison", None)}
    CONSUMABLES = {0x0F7A: "Black Pearl", 0x0F7B: "Blood Moss", 0x0F84: "Garlic",
                   0x0F85: "Ginseng", 0x0F86: "Mandrake Root", 0x0F88: "Nightshade",
                   0x0F8D: "Spiders' Silk", 0x0F8C: "Sulfurous Ash", 0x0F78: "Bat Wing",
                   0x0F8F: "Grave Dust", 0x0F7D: "Daemon Blood", 0x0F8E: "Nox Crystal",
                   0x0F8A: "Pig Iron", 0x0F3F: "Arrows", 0x1BFB: "Bolts"}
    METRIC = {"dmg_done": ("Damage done", "s", "n", "#c4562a", True),
              "dmg_taken": ("Damage taken", "s", "n", "#b02a2a", True),
              "dmg_nearby": ("All damage nearby", "s", "n", "#9a5a3a", True),
              "big": ("Biggest hits", "", "n", "#d07a2a", True), "kills": ("Kills", "h", "n", "#8a6ab0", False),
              "deaths": ("Deaths", "h", "n", "#6a6a78", True), "heal_done": ("Healing done", "s", "n", "#2f9a3c", True),
              "heal_taken": ("Healing received", "s", "n", "#3fae5a", True),
              "heal_by": ("Healing by method", "s", "n", "#4aa070", False),
              "cures": ("Cures", "m", "n", "#2a9a8a", True), "poisoned": ("Poisonings", "m", "n", "#5a9a2a", True),
              "spells": ("Spells cast", "m", "n", "#2f62cc", False), "mana": ("Mana spent", "m", "n", "#3a72d8", False),
              "consum": ("Consumables", "h", "n", "#a08a2a", False),
              "buffs": ("Buffs & debuffs", "h", "n", "#8a5ab0", False), "gold": ("Gold", "h", "n", "#cfae2a", False),
              "gold_place": ("Gold by place", "h", "n", "#d8b84a", False),
              "loot": ("Items gained", "h", "n", "#a8925a", False),
              "skills": ("Skill gains", "h", "d1", "#5a8acc", False),
              "stats": ("Stat gains", "h", "n", "#cc7a5a", False), "fame": ("Fame & karma", "h", "n", "#b0a050", False),
              "travel": ("Travel", "h", "n", "#6a9aaa", False),
              "session": ("Session summary", "", "", "#4a4a58", False)}
    GROUPS = (("COMBAT", ("dmg_done", "dmg_taken", "dmg_nearby", "big", "kills", "deaths")),
              ("HEALING", ("heal_done", "heal_taken", "heal_by", "cures", "poisoned")),
              ("MAGIC & ITEMS", ("spells", "mana", "consum", "buffs")),
              ("ECONOMY & PROGRESS", ("gold", "gold_place", "loot", "skills", "stats", "fame", "travel", "session")))
    ORDER = [m for _, ms in GROUPS for m in ms]; DEFAULT_METRIC = "dmg_done"
    RATE_WORD = {"s": "per sec", "m": "per min", "h": "per hour"}
    settings = {"idle": 6, "engage": 12, "history": 10, "min_heal": 3, "rows": 8,
               "rank": True, "pct": True, "scan": True, "travel": True, "party": True, "recap": True}
    DEFAULTS = dict(settings)
    LIMITS = {"idle": (2, 60), "engage": (3, 120), "history": (1, 30), "min_heal": (1, 50), "rows": (3, 20)}
    MAX_ROWS = 5000; FOLD_TO = 4000; OTHERS = "(others)"; OWN_PREFIX = TITLE.lower() + ":"
    st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "active": False, "hooked": False,
          "jr": None, "engaged": {}, "watch": {}, "friendly": {}, "mobs": {}, "dead_seen": {}, "pack_sig": None,
          "pend": [], "orph": [], "last_spell": None, "cast_t": 0.0, "prev_lt": 0, "to_write": [], "changed": False}
    win = {"g": None, "c": {}, "store": ({}, {})}; cleanup, queue, say = Kit.basics(st, TITLE)
    spots = []; graph = {"min": None, "b": None, "hist": {}, "ver": 0, "vb": {}}
    recap = {"g": None, "c": {}, "store": ({}, {}), "rows": []}
    data = {}; wins = []; page = {}; humans = {}
    feed = {"q": None, "handler": None, "event": None, "kind": "not hooked"}
    refl = {"tried": False, "tm": None, "la": None}; jobs = []; SEGN = [0]; import heapq
    RE_COUNT = re.compile(r"^[0-9,]+\s+"); PACK_CHUNK = 60; NAME_EVERY = 1.0; find_mob = HOST.mobile
    def pets_near():
        svc = HOST.services.get("pets.list")
        if svc is not None:
            try:
                got = svc(distance=PET_RANGE)
                if got is not None: return [int(s) for s in got]
            except Exception: pass
        pets = []
        for m in HOST.mobiles(PET_RANGE):
            try:
                if m.IsRenamable: pets.append(int(m.Serial))
            except Exception: pass
        return pets
    def fmt_num(v, f="n"):
        if f == "d1": return "%.1f" % v
        a = abs(v)
        if a >= 1e6: return "%.2fM" % (v / 1e6)
        if a >= 1e4: return "%.1fk" % (v / 1e3)
        if a >= 1000: return "%.2fk" % (v / 1e3)
        if abs(v - round(v)) < 0.05: return "%d" % int(round(v))
        return "%.1f" % v
    def fmt_rate(v, f="n"):
        if f == "d1": return "%.1f" % v if abs(v) < 100 else "%d" % int(round(v))
        if abs(v) < 10: return "%.1f" % v
        if abs(v) < 1000: return "%d" % int(round(v))
        return fmt_num(v)
    def fmt_signed(v, f="n"): s = fmt_num(v, f); return s if v < 0 else "+" + s
    def fmt_time(sec):
        sec = int(max(0, sec)); h, m, s = sec // 3600, (sec // 60) % 60, sec % 60
        return "%d:%02d:%02d" % (h, m, s) if h else "%d:%02d" % (m, s)
    def is_mobile(ser): return 0 < int(ser or 0) < 0x40000000
    def pct_row(name): return name.endswith(" (%)")
    def load_settings(): Kit.kv_load(SETTINGS_KEY, "|", settings, LIMITS)
    def save_settings(): Kit.kv_save(SETTINGS_KEY, "|", settings, sorted(DEFAULTS), LIMITS)
    def new_win(wid, metric=DEFAULT_METRIC, x=200, y=200, minimized=False):
        return {"id": wid, "metric": metric if metric in METRIC else DEFAULT_METRIC,
                "seg": "current", "x": x, "y": y, "minimized": minimized, "docked": False,
                "shutting": False, "g": None, "c": {}, "store": ({}, {}), "slots": [],
                "picker": None, "segpick": None, "detail": None, "dc": {}, "detail_row": None,
                "detail_metric": None, "graph": False, "gcols": [], "gkey": None, "fit": None, "size": None,
                "drawn": None, "resize_at": 0.0, "preview": False, "home": (x, y)}
    def load_windows():
        out = []
        for part in Kit.get_var(WINS_KEY).split(";"):
            p = part.split(",")
            if len(p) < 6: continue
            try: wid, x, y = int(p[0]), int(p[3]), int(p[4])
            except ValueError: continue
            if not 0 <= wid < WIN_ID_MAX or any(w["id"] == wid for w in out): continue
            if not (TAB_X // 2 < x < POS_MAX and abs(y) < POS_MAX): x, y = 200, 200
            x, y = Kit.adapt(x, y, W, 0); w = new_win(wid, p[1], x, y, p[5] == "1")
            w["seg"] = "overall" if p[2] == "overall" else "current"; w["graph"] = len(p) > 6 and p[6] == "1"
            if len(p) > 8:
                try:
                    sw, sh = int(p[7]), int(p[8])
                    if sw > 0 and sh > 0: w["size"] = own_size(sw, sh)
                except ValueError: pass
            out.append(w)
        out.sort(key=lambda w: w["id"])
        if not out or out[0]["id"] != 0: out.insert(0, new_win(0))
        del wins[:]; wins.extend(out[:MAX_WINDOWS])
    def own_size(sw, sh):
        return max(SIZE_MIN_W, min(SIZE_MAX_W, sw)), max(60, min(SIZE_MAX_H, Kit.screen()[1] or SIZE_MAX_H, sh))
    def forget_sizes_off():
        load_windows()
        for w in wins: w["size"] = None
        save_windows()
    def save_windows():
        parts = []
        for w in wins:
            g = w["g"]
            if Kit.is_open(g):
                w["x"], w["y"] = g.GetX(), g.GetY()
                free = g not in LAYOUT.held and w["fit"] is None and not HOST.layout_holds(dock_key(w))
                if free and w["x"] > TAB_X // 2: w["home"] = (w["x"], w["y"])
            size = w.get("size") or (0, 0); hx, hy = w["home"]
            parts.append("%d,%s,%s,%d,%d,%s,%s,%d,%d" % (w["id"], w["metric"], "overall" if w["seg"] == "overall"
                                                         else "current", int(hx), int(hy),
                                                         "1" if w["minimized"] else "0", "1" if w.get("graph") else "0",
                                                         int(size[0]), int(size[1])))
        Kit.put_var(WINS_KEY, ";".join(parts))
    def load_spots():
        del spots[:]; lo, hi = SPOT_RADIUS_LIMITS
        for part in Kit.get_var(SPOTS_KEY).split(";"):
            p = part.split(",")
            if len(p) < 5 or not p[0].strip(): continue
            try: sp = [spot_name(p[0]), int(p[1]), int(p[2]), int(p[3]), max(lo, min(hi, int(p[4])))]
            except ValueError: continue
            if not sp[0] or not all(0 <= v < 65536 for v in sp[1:4]): continue
            if all(o[0] != sp[0] for o in spots) and len(spots) < SPOTS_MAX: spots.append(sp)
    def save_spots(): Kit.put_var(SPOTS_KEY, ";".join("%s,%d,%d,%d,%d" % tuple(sp) for sp in spots))
    def spot_name(text):
        for ch in ";,|": text = text.replace(ch, " ")
        return " ".join(text.split())[:SPOT_NAME_MAX]
    def new_seg(kind, n=0):
        now = time.time(); SEGN[0] += 1
        return {"kind": kind, "n": n, "name": "Fight %d" % n if n else "Overall",
                "start": now, "end": None, "combat": 0.0, "d": {}, "serial": {}, "big": [],
                "fights": 0, "uid": SEGN[0], "ver": 0, "tot": {}, "place_t": {}, "top": None}
    def reset_data():
        data.clear()
        data.update({"overall": new_seg("overall"), "cur": None, "hist": [], "n": 0, "last_combat": 0.0, "c_at": None})
        st["watch"].clear(); st["engaged"].clear(); st["pend"], st["orph"] = [], []
        graph.update({"min": None, "b": None, "ver": graph["ver"] + 1}); graph["hist"].clear(); graph["vb"].clear()
    def segs(): cur = data["cur"]; return (data["overall"], cur) if cur is not None else (data["overall"],)
    def graph_bucket(now):
        m = int(now // 60)
        if m != graph["min"]:
            hist = graph["hist"]
            for k in [k for k in hist if k <= m - GRAPH_MINUTES]: del hist[k]
            graph["min"] = m; graph["b"] = hist.setdefault(m, {})
        return graph["b"]
    def record(mid, row, amt, ser=None, side=False):
        now = time.time(); pct = side or row.endswith(" (%)")
        if not pct and (mid != "gold" or row == "Gained"):
            b = graph_bucket(now); b[mid] = b.get(mid, 0.0) + amt; vb = graph["vb"]; vb[mid] = vb.get(mid, 0) + 1
        for seg in segs():
            d = seg["d"].get(mid)
            if d is None: d = seg["d"][mid] = {}
            r = d.get(row)
            if r is None:
                if len(d) >= MAX_ROWS: fold(seg, mid, d)
                r = d[row] = [0.0, 0, amt, amt, now, now]
            r[0] += amt; r[1] += 1
            if amt > r[2]: r[2] = amt
            if amt < r[3]: r[3] = amt
            r[5] = now
            if ser: seg["serial"][(mid, row)] = ser
            if not pct: tot = seg["tot"]; tot[mid] = tot.get(mid, 0.0) + amt
            seg["ver"] += 1
        if amt and any(w["metric"] in (mid, "session") and not w["docked"] for w in wins): st["changed"] = True
    def fold(seg, mid, d):
        small = sorted((abs(r[0]), k) for k, r in d.items() if k != OTHERS and not k.endswith(" (%)"))
        o = d.get(OTHERS); sers = seg["serial"]
        for _, k in small[:max(0, len(d) - FOLD_TO)]:
            r = d.pop(k); sers.pop((mid, k), None)
            if o is None: o = d[OTHERS] = list(r)
            else:
                o[0] += r[0]; o[1] += r[1]; o[2], o[3] = max(o[2], r[2]), min(o[3], r[3])
                o[4], o[5] = min(o[4], r[4]), max(o[5], r[5])
    def record_big(amt, name, ser):
        b = graph_bucket(time.time())
        if amt > b.get("big", 0.0): b["big"] = amt; vb = graph["vb"]; vb["big"] = vb.get("big", 0) + 1
        for seg in segs():
            big = seg["big"]
            if len(big) >= BIG_KEEP and amt <= big[-1][0]: continue
            i = len(big)
            while i > 0 and big[i - 1][0] < amt: i -= 1
            big.insert(i, (amt, name, ser)); del big[BIG_KEEP:]
    def total(seg, mid): return seg["tot"].get(mid, 0)
    def enter_combat():
        now = time.time()
        if data["cur"] is None:
            data["n"] += 1; data["cur"] = new_seg("fight", data["n"]); data["overall"]["fights"] += 1
        data["last_combat"] = now; data["c_at"] = (data["cur"]["combat"], data["overall"]["combat"])
    def close_fight(now):
        cur = data["cur"]
        if cur is None: return
        ca = data.get("c_at")
        if ca is not None: cur["combat"], data["overall"]["combat"] = ca
        else:
            tail = max(0.0, now - data["last_combat"])
            for seg in (cur, data["overall"]): seg["combat"] = max(0.0, seg["combat"] - tail)
        data["c_at"] = None; cur["end"] = data["last_combat"]; d = cur["d"].get("dmg_done", {})
        if d:
            top = max(d.items(), key=lambda kv: kv[1][0])[0]
            cur["name"] = top + (" +%d" % (len(d) - 1) if len(d) > 1 else ""); cur["top"] = top
        data["hist"].insert(0, cur); del data["hist"][settings["history"]:]; data["cur"] = None
    def combat_secs(seg): return max(1.0, seg["combat"])
    def wall_secs(seg): return max(1.0, (seg["end"] or time.time()) - seg["start"])
    def rate_of(seg, rate, value):
        if rate == "s": return value / combat_secs(seg)
        if rate == "m": return value / (wall_secs(seg) / 60.0)
        return value / (max(60.0, wall_secs(seg)) / 3600.0)
    def seg_for(w):
        s = w["seg"]
        if s == "overall": return data["overall"]
        if s != "current":
            for h in data["hist"]:
                if h["n"] == s: return h
            w["seg"] = "current"
        return data["cur"] or (data["hist"][0] if data["hist"] else None)
    SEG_CAPS = {"overall": "Overall", "current": "Current"}
    def seg_caption(w): return SEG_CAPS.get(w["seg"]) or "Fight %d" % w["seg"]
    def seg_name(seg):
        top = seg["top"]
        if not top: return seg["name"]
        return shown(top, seg["serial"].get(("dmg_done", top))) + seg["name"][len(top):]
    def seg_duration_text(seg):
        if seg is None: return ""
        if seg["kind"] == "overall": return fmt_time(time.time() - seg["start"])
        return fmt_time(combat_secs(seg))
    def _row_size(kv): return abs(kv[1][0])
    def nr(seg, v, r, head=fmt_num): return "%s (%s/%s)" % (head(v), fmt_rate(rate_of(seg, r, v)), r)
    def view(mid, seg, limit=None):
        _, rate, f, _, _ = METRIC[mid]
        if seg is None: return (["No fight yet."], [])
        dur = seg_duration_text(seg)
        if mid == "session": return session_view(seg)
        if mid == "big":
            big = seg["big"] if limit is None else seg["big"][:limit]
            rows = [(name, amt, fmt_num(amt), ser, None) for amt, name, ser in big]
            head = (["Biggest %s on %s" % (fmt_num(seg["big"][0][0]), shown(seg["big"][0][1], seg["big"][0][2]))]
                    if seg["big"] else ["No hits yet."])
            return (head + [dur], rows)
        d = seg["d"].get(mid, {})
        if mid == "gold":
            gain = d.get("Gained", [0.0])[0]; spent = d.get("Spent / banked", [0.0])[0]; net = gain - spent
            rows = [("Gained", gain, nr(seg, gain, "h"), None, d.get("Gained")),
                    ("Spent / banked", spent, fmt_num(spent), None, d.get("Spent / banked")),
                    ("Net", abs(net), nr(seg, net, "h", fmt_signed), None, None)]
            return (["Net %s" % fmt_signed(net), "%s per hour" % fmt_rate(rate_of(seg, "h", net)), dur], rows)
        if mid == "gold_place": return place_view(seg, d, limit, dur)
        tot = total(seg, mid)
        if limit is None: items = sorted(d.items(), key=_row_size, reverse=True)
        elif limit <= 0: items = []
        else: items = heapq.nlargest(limit, d.items(), key=_row_size)
        rows = []
        for name, r in items:
            v = r[0]; bits = []
            if rate: bits.append(fmt_rate(rate_of(seg, rate, v), f) + ("" if rate == "s" else "/" + rate))
            if settings["pct"] and tot and not pct_row(name) and v > 0:
                bits.append("%d%%" % int(round(100.0 * v / tot)))
            vt = (fmt_signed(v, f) if mid in ("skills", "stats") else fmt_num(v, f))
            text = vt + (" (%s)" % ", ".join(bits) if bits else "")
            rows.append((name, abs(v), text, seg["serial"].get((mid, name)), r))
        if mid in ("skills", "stats"): head = ["Total %s" % fmt_signed(tot, f)]
        elif mid == "cures":
            mine = total(seg, "cures_mine"); head = ["Cures %s" % fmt_num(tot), "by you %s" % fmt_num(mine)]
        else: head = ["Total %s" % fmt_num(tot, f)]
        if rate: head.append("%s %s" % (fmt_rate(rate_of(seg, rate, tot), f), RATE_WORD[rate]))
        head.append("in combat " + fmt_time(seg["combat"]) if rate == "s" else dur); return (head, rows)
    def place_rate(seg, name, gold):
        secs = seg["place_t"].get(name, 0.0); return gold / (max(PLACE_MIN_SECS, secs) / 3600.0), secs
    def _rate_size(row): return row[1]
    def place_view(seg, d, limit, dur):
        pt = seg["place_t"]; names = list(d)
        for k, secs in pt.items():
            if secs >= PLACE_MIN_SECS and k not in d: names.append(k)
        tot = sum(r[0] for r in d.values()); rows = []
        for name in names:
            r = d.get(name); gold = r[0] if r is not None else 0.0; rate, _secs = place_rate(seg, name, gold)
            bits = [fmt_num(gold)]
            if settings["pct"] and tot and gold > 0: bits.append("%d%%" % int(round(100.0 * gold / tot)))
            rows.append((name, rate, "%s/h (%s)" % (fmt_rate(rate), ", ".join(bits)), None, r))
        rows.sort(key=_rate_size, reverse=True)
        if limit is not None: del rows[max(0, limit):]
        n = len(names); return (["Gained %s" % fmt_num(tot), Kit.count(n, "place"), dur], rows)
    def session_view(seg):
        wall = wall_secs(seg); cs = seg["combat"]
        dd, dt, hd = total(seg, "dmg_done"), total(seg, "dmg_taken"), total(seg, "heal_done")
        kills, deaths = total(seg, "kills"), total(seg, "deaths"); gd = seg["d"].get("gold", {})
        net = gd.get("Gained", [0.0])[0] - gd.get("Spent / banked", [0.0])[0]; sk = total(seg, "skills")
        lines = [("Time", fmt_time(wall)), ("In combat", "%s (%d%%)" % (fmt_time(cs), int(100 * cs / wall)))]
        if seg["kind"] == "overall": lines.append(("Fights", "%d" % seg["fights"]))
        lines += [("Damage done", nr(seg, dd, "s")), ("Damage taken", nr(seg, dt, "s")),
                  ("Healing done", nr(seg, hd, "s")), ("Kills", nr(seg, kills, "h")), ("Deaths", fmt_num(deaths)),
                  ("Gold", nr(seg, net, "h", fmt_signed)),
                  ("Skill gain", "%s (%s/h)" % (fmt_signed(sk, "d1"), fmt_rate(rate_of(seg, "h", sk), "d1"))),
                  ("Items gained", fmt_num(total(seg, "loot"))),
                  ("Spells cast", fmt_num(sum(r[1] for k, r in seg["d"].get("spells", {}).items()
                                              if k not in ("Fizzled", "Interrupted", "Out of mana"))))]
        rows = [(name, 0.0, text, None, None) for name, text in lines]
        return ([seg_name(seg) if seg["kind"] == "fight" else "Session", fmt_time(wall)], rows)
    def hook_damage():
        try:
            import clr; clr.AddReference("System.Collections.Concurrent"); clr.AddReference("System.Linq.Expressions")
            from System import Array, Int32, UInt32, Object, EventHandler, Tuple, Type, AppDomain
            from System.Reflection import BindingFlags; from System.Collections.Concurrent import ConcurrentQueue
            from System.Linq.Expressions import Expression, ParameterExpression
            stat = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static; asm = API.GetType().Assembly
            sink = asm.GetType("ClassicUO.Game.Managers.EventSink")
            ent = asm.GetType("ClassicUO.Game.GameObjects.Entity"); ev = sink.GetEvent("OnEntityDamage", stat)
            t_obj, t_int, t_uint = (clr.GetClrType(Object), clr.GetClrType(Int32), clr.GetClrType(UInt32))
            ftype = Tuple[UInt32, Int32]; q = ConcurrentQueue[ftype](); p_s = Expression.Parameter(t_obj, "sender")
            p_e = Expression.Parameter(t_int, "amount"); qc = Expression.Constant(q)
            serial = Expression.Convert(Expression.PropertyOrField(Expression.Convert(p_s, ent), "Serial"), t_uint)
            ctor = clr.GetClrType(ftype).GetConstructor(Array[Type]([t_uint, t_int]))
            enqueue = Expression.Call(qc, q.GetType().GetMethod("Enqueue"), Array[Expression]([Expression.New(ctor,
                                              Array[Expression]([serial, p_e]))]))
            room = Expression.LessThan(Expression.Property(qc, "Count"), Expression.Constant(DAMAGE_QUEUE_MAX, t_int))
            body = Expression.IfThen(Expression.AndAlso(Expression.TypeIs(p_s, ent), room), enqueue)
            handler = Expression.Lambda[EventHandler[Int32]](body, Array[ParameterExpression]([p_s, p_e])).Compile()
            dom = AppDomain.CurrentDomain; left = dom.GetData(HOOK_KEY)
            if left is not None: safe(lambda: ev.GetRemoveMethod(True).Invoke(None, Array[Object]([left])))
            ev.GetAddMethod(True).Invoke(None, Array[Object]([handler])); dom.SetData(HOOK_KEY, handler)
            feed.update({"q": q, "handler": handler, "event": ev, "kind": "exact (per mobile)"}); return True
        except Exception as ex:
            feed.update({"q": None, "handler": None, "event": None})
            feed["kind"] = "amounts only (%s)" % (str(ex)[:50] or "no hook"); return False
    def unhook_damage():
        h, ev = feed.get("handler"), feed.get("event")
        if h is None or ev is None: return
        with Kit.quiet:
            from System import Array, Object, AppDomain; ev.GetRemoveMethod(True).Invoke(None, Array[Object]([h]))
            AppDomain.CurrentDomain.SetData(HOOK_KEY, None)
        feed.update({"q": None, "handler": None, "event": None, "kind": "not hooked"})
    def on_damage_amount(*args):
        if not st["active"]: return
        if not st["poked"]: st["poked"] = True; HOST.poke(KEY, False)
        if feed.get("q") is not None: return
        for a in args:
            try: st["amtq"].append(int(a))
            except Exception: continue
            del st["amtq"][:-200]; return
    def last_attack():
        if not refl["tried"]:
            refl["tried"] = True
            try:
                from System.Reflection import BindingFlags
                fl = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
                world = API.GetType().GetField("World", fl).GetValue(API)
                tm = world.GetType().GetProperty("TargetManager", fl).GetValue(world, None)
                refl["tm"], refl["la"] = tm, tm.GetType().GetProperty("LastAttack", fl)
            except Exception: refl["tm"] = refl["la"] = None
        if refl["la"] is None: return 0
        return int(refl["la"].GetValue(refl["tm"], None) or 0)
    def on_used(*args):
        if not st["active"]: return
        for a in args:
            try: st["used"].append(int(a)); del st["used"][:-30]; return
            except Exception: continue
    def on_died(*args):
        if not st["active"]: return
        st["died"] = True
        if not st["poked"]: st["poked"] = True; HOST.poke(KEY, False)
    def on_buff(*args):
        if not st["active"]: return
        for a in args:
            t = safe(lambda: a.Title)
            if t: st["buffq"].append(str(t)); del st["buffq"][:-50]; return
    def sample():
        now = time.time()
        out = {"me": None, "dmg": [], "info": {}, "fhp": {}, "wst": {}, "used": [], "pack": None, "friends": None,
               "hum": [], "t": now, "pt": now}
        p = HOST.me()
        if p is None: return out
        ser = int(p.Serial)
        if ser != st["my_ser"] or now >= st["next_name"]:
            st["my_name"] = str(p.Name or ""); st["my_ser"], st["next_name"] = ser, now + NAME_EVERY
        me = {"ser": ser, "name": st["my_name"], "hits": int(p.Hits),
              "hmax": int(p.HitsMax), "mana": int(p.Mana), "x": int(p.X), "y": int(p.Y),
              "gold": int(p.Gold or 0), "dead": bool(p.IsDead), "war": bool(p.InWarMode), "poison": bool(p.IsPoisoned),
              "map": int(API.GetMap())}
        out["me"] = me; q = feed["q"]
        if q is not None:
            for _ in range(FEED_BURST):
                ok, item = q.TryDequeue()
                if not ok: break
                out["dmg"].append((int(item.Item1), int(item.Item2)))
        mobs = st["mobs"]; info = out["info"]
        if len(mobs) > MOBS_MAX or len(humans) > MOBS_MAX:
            keep = [(fs, mobs[fs]) for fs in st["friendly"] if fs in mobs]; mobs.clear(); mobs.update(keep)
        for ser, _ in out["dmg"]:
            if ser not in mobs and ser not in info and ser != me["ser"]:
                m = find_mob(ser); info[ser] = str(m.Name or "") if m is not None else ""
                if m is not None and m.IsHuman: out["hum"].append(ser)
        out["lt"] = int(API.LastTargetSerial or 0); out["la"] = last_attack()
        for sers in (st["engaged"], (out["lt"], out["la"])):
            for ser in sers:
                if is_mobile(ser) and ser not in mobs and ser not in info and ser != me["ser"]:
                    m = find_mob(ser)
                    if m is not None:
                        info[ser] = str(m.Name or "")
                        if m.IsHuman: out["hum"].append(ser)
        if now >= st["next_friends"]:
            st["next_friends"] = now + FRIENDS_EVERY
            party = [int(s) for s in API.GetPartyMemberSerials() or []]; pets = pets_near()
            friends = [int(s) for s in API.GetAllFriends() or []]
            out["friends"] = (party, pets, friends); pres, seen = [], set()
            for sers in (friends, pets, party):
                for fs in sers:
                    if fs != me["ser"] and fs not in seen:
                        seen.add(fs)
                        if find_mob(fs) is not None: pres.append(fs)
        else: pres = None
        names_due = out["friends"] is not None; fhp = out["fhp"]
        for ser in st["present"]:
            m = find_mob(ser)
            if m is not None:
                known = None if names_due else mobs.get(ser)
                fhp[ser] = (int(m.Hits), int(m.HitsMax), bool(m.IsPoisoned), bool(m.IsDead), known or str(m.Name or ""))
        if pres is not None: st["present"] = pres
        wst = out["wst"]
        for ser, w in st["watch"].items():
            if now - w["t"] > DYING_CHECK_SECS: continue
            if find_mob(ser) is not None: wst[ser] = "alive"
            elif API.FindMobile(ser | DEATH_BIT) is not None: wst[ser] = "dying"
            else: wst[ser] = "gone"
        if st["used"]:
            used, st["used"] = st["used"], []
            for ser in used:
                it = API.FindItem(ser)
                if it is not None: out["used"].append((int(it.Graphic), str(it.Name or "")))
        if not settings["scan"]: st["pscan"] = None
        elif st["pscan"] is None and now >= st["next_scan"]:
            st["next_scan"] = now + SCAN_EVERY
            if API.Backpack: st["pscan"] = [HOST.pack_items(True), 0, [], 0, 0, now]
        ps = st["pscan"]
        if ps is not None: out["pack"] = pack_step(ps, now); out["pt"] = ps[5]
        return out
    def pack_step(ps, now):
        items, i, pairs, ssum, asum, taken = ps; n = len(items); end = min(n, i + PACK_CHUNK)
        try:
            while i < end:
                it = items[i]; a = int(it.Amount or 1) or 1; ssum += int(it.Serial or 0); asum += a
                pairs.append((it, a)); i += 1
        except Exception:
            st["pscan"] = None
            if taken == now: raise
            st["next_scan"] = 0.0; return None
        if i < n: ps[1], ps[3], ps[4] = i, ssum, asum; return None
        st["pscan"] = None; sig = (len(pairs), ssum, asum)
        if sig == st["pack_sig"] and st["pack"] is not None:
            st["pack_cand"] = None; return st["pack"] if st["rebase"] and taken > st["rebase"] else None
        if taken != now and st.get("pack_cand") != sig: st["pack_cand"] = sig; st["next_scan"] = 0.0; return None
        st["pack_cand"] = None; st["pack_sig"] = sig; tot = {}
        for it, a in pairs:
            k = (int(it.Graphic), int(it.Hue))
            if k in tot: tot[k][0] += a
            else: tot[k] = [a, None, it]
        prev = st["pack"] or {}
        for k, v in tot.items():
            old = prev.get(k)
            if old is None or v[0] > old[0]:
                try: v[1] = str(v[2].Name or "")
                except Exception: v[1] = ""
            else: v[1] = old[1]
            v[2] = None
        return tot
    def is_friend(ser): me = st["me"]; return (me is not None and ser == me["ser"]) or ser in st["friendly"]
    def mob_name(ser):
        me = st["me"]
        if me is not None and ser == me["ser"]: return me["name"] or "You"
        return st["mobs"].get(ser) or "Unknown"
    def shown(name, ser=None, unsure=False):
        if not Kit.streamer or not name: return name
        base = name[:-4] if pct_row(name) else name; me = st["me"]
        if me is not None and base == me["name"]: return Kit.veil("me", base) + name[len(base):]
        if base.lower() not in humans and not (unsure and not is_mobile(ser)): return name
        return Kit.veil("name", base, ser if is_mobile(ser) else Kit.checksum(base.lower().encode("utf-8"))) + \
            name[len(base):]
    def engaged(ser, now): t = st["engaged"].get(ser); return t is not None and now - t <= settings["engage"]
    def add_pending(now, kind, method, secs):
        multi = kind == "cure+"; kind = "cure" if multi else kind
        for o in list(st["orph"]):
            if o[1] == kind and now - o[0] <= ORPHAN_SECS:
                st["orph"].remove(o); credit(kind, method, o[2], o[3], o[4])
                if not multi: return
        st["pend"].append([now + secs, kind, method, multi])
    def credit(kind, method, ser, name, amt):
        if kind == "heal":
            record("heal_done", name, amt, ser)
            if not pct_row(name): record("heal_by", method, amt)
        else: record("cures_mine", method, 1)
    def claim(kind, now, ser, name, amt):
        for p in st["pend"]:
            if p[1] == kind and now <= p[0]:
                if not p[3]: st["pend"].remove(p)
                credit(kind, p[2], ser, name, amt); return
        st["orph"].append((now, kind, ser, name, amt))
    def keep_humans():
        used = set()
        for seg in list(segs()) + data["hist"]:
            for d in seg["d"].values(): used.update((k[:-4] if pct_row(k) else k).lower() for k in d)
            used.update(str(b[1]).lower() for b in seg["big"])
        if st["recap"] is not None: used.update(str(r[6] or "").lower() for r in st["recap"]["rows"])
        kept = sorted((t, k) for k, t in humans.items() if k in used)[-(MOBS_MAX // 2):]; humans.clear()
        humans.update((k, t) for t, k in kept)
    def process(s, now):
        me = s["me"]
        if me is None: return
        old_me, st["me"] = st["me"], me; mobs = st["mobs"]
        if len(humans) > MOBS_MAX: keep_humans()
        for ser, name in s["info"].items():
            if name: mobs[ser] = name
        for ser in s["hum"]:
            if mobs.get(ser): humans[mobs[ser].lower()] = now
        if st["pend"]: st["pend"] = [p for p in st["pend"] if p[0] >= now]
        if st["orph"]: st["orph"] = [o for o in st["orph"] if now - o[0] <= ORPHAN_SECS]
        if s["friends"] is not None:
            party, pets, friends = s["friends"]; fr = {}
            for kind, sers in (("friend", friends), ("pet", pets), ("party", party)):
                for ser in sers: fr[ser] = kind
            for ser in friends + party:
                nm = s["fhp"][ser][4] if ser in s["fhp"] else mobs.get(ser)
                if nm: humans[nm.lower()] = now
            fr.pop(me["ser"], None); st["friendly"] = fr
        lt, la = s.get("lt", 0), s.get("la", 0)
        if la and me["war"] and is_mobile(la) and not is_friend(la): st["engaged"][la] = now
        if (is_mobile(lt) and not is_friend(lt) and (lt != st["prev_lt"] or now - st["cast_t"] <= 2.0)):
            st["engaged"][lt] = now
        st["prev_lt"] = lt
        if st["engaged"]:
            for ser in [k for k, t in st["engaged"].items() if now - t > settings["engage"]]:
                st["engaged"].pop(ser, None)
        budget = 0
        if old_me is not None and me["hits"] < old_me["hits"]: budget = old_me["hits"] - me["hits"]
        for ser, dmg in s["dmg"]: hit(ser, dmg, now)
        if st["amtq"]:
            tgt = None
            for amt in st["amtq"]:
                if budget >= amt: budget -= amt; hit(me["ser"], amt, now)
                else:
                    if tgt is None: tgt = max(st["engaged"].items(), key=lambda kv: kv[1])[0] if st["engaged"] else 0
                    hit(tgt, amt, now) if tgt else record("dmg_nearby", "Unknown", amt)
            st["amtq"] = []
        hp = s["fhp"]; hp[me["ser"]] = (me["hits"], me["hmax"], me["poison"], me["dead"], me["name"] or "You")
        for ser, (hits, hmax, poison, dead, name) in hp.items():
            if name: mobs[ser] = name
            name = mob_name(ser); prev = st["prev"].get(ser); st["prev"][ser] = (hits, hmax, poison, dead)
            if prev is None: continue
            if dead and not prev[3]:
                if now - st["dead_seen"].get(ser, 0) > 10:
                    record("deaths", name, 1, ser); st["dead_seen"][ser] = now
                    if ser == me["ser"] and settings["recap"]: make_recap(now)
                continue
            if dead or prev[3]: continue
            real = ser == me["ser"] or st["friendly"].get(ser) == "party" or hmax not in (25, 100); dh = hits - prev[0]
            if dh >= (settings["min_heal"] if real else 1) and hmax == prev[1]:
                row = name if real else name + " (%)"; amt = dh if real else dh * 100.0 / max(1, hmax)
                record("heal_taken", row, amt, ser); claim("heal", now, ser, row, amt)
            if poison and not prev[2]: record("poisoned", name, 1, ser)
            elif prev[2] and not poison: record("cures", name, 1, ser); claim("cure", now, ser, name, 1)
        if len(st["prev"]) != len(hp):
            for ser in [k for k in st["prev"] if k not in hp]: st["prev"].pop(ser, None)
        for ser, state in s["wst"].items():
            w = st["watch"].get(ser)
            if w is None: continue
            if state == "dying":
                st["watch"].pop(ser, None)
                if w["friend"]:
                    if now - st["dead_seen"].get(ser, 0) > 10:
                        record("deaths", w["name"], 1, ser); st["dead_seen"][ser] = now
                elif w["mine"] and now - w["mine"] <= KILL_CREDIT_SECS: record("kills", w["name"], 1)
        if st["watch"]:
            for ser in [k for k, w in st["watch"].items() if now - w["t"] > WATCH_SECS]: st["watch"].pop(ser, None)
        if st["dead_seen"]:
            for ser in [k for k, t in st["dead_seen"].items() if now - t > 30]: st["dead_seen"].pop(ser, None)
        hl = st["hp_log"]
        if not hl or hl[-1][1] != me["hits"] or hl[-1][2] != me["hmax"]:
            hl.append((now, me["hits"], me["hmax"]))
            if len(hl) > HP_KEEP: del hl[:len(hl) - HP_KEEP]
        if old_me is not None and me["mana"] < old_me["mana"] and not me["dead"]:
            ls = st["last_spell"]; row = ls[1] if ls is not None and now - ls[0] <= ls[2] + MANA_SECS else "Other"
            record("mana", row, old_me["mana"] - me["mana"])
        ow = st["owed"]; dead = me["dead"] or (old_me is not None and old_me["dead"])
        if ow["until"] and (now > ow["until"] or old_me is not None and old_me["ser"] != me["ser"]):
            ow.update({"gold": 0, "until": 0.0}); ow["pack"].clear()
        if old_me is not None and old_me["ser"] == me["ser"] and me["dead"] and not old_me["dead"]:
            ow["until"] = now + CORPSE_SECS; ow["gold"] += old_me["gold"]; st["rebase"] = s.get("t", now)
            for k, v in (st["pack"] or {}).items(): ow["pack"][k] = ow["pack"].get(k, 0) + v[0]
        if old_me is not None and old_me["ser"] == me["ser"] and old_me["hmax"] and not dead:
            dg = me["gold"] - old_me["gold"]
            if dg > 0 and ow["gold"]: back = min(dg, ow["gold"]); ow["gold"] -= back; dg -= back
            if dg > 0: record("gold", "Gained", dg); record("gold_place", st["place"] or PLACE_ELSEWHERE, dg)
            elif dg < 0: record("gold", "Spent / banked", -dg)
        pos = (me["x"], me["y"], me["map"])
        if settings["travel"] and st["pos"] is not None and (me["x"] or me["y"]):
            ox, oy, om = st["pos"]; dist = max(abs(me["x"] - ox), abs(me["y"] - oy))
            if om != me["map"] or dist > JUMP_TILES: record("travel", "Recalls, gates & teleports", 1)
            elif dist > 0: record("travel", "Tiles walked", dist)
        st["pos"] = pos
        for graphic, name in s["used"]:
            pot = POTIONS.get(graphic)
            if pot is None: continue
            label = pot[0] + " potion"; record("consum", label, 1)
            if pot[1]: add_pending(now, pot[1], pot[0] + " potion", POTION_SECS)
        pack = s["pack"]
        if pack is not None:
            old = st["pack"]; owp = ow["pack"]
            fresh = old is not None and len(old) == 0 and len(pack) > 0 and not any(owp.values())
            skip = me["dead"] or st["rebase"]
            if st["rebase"] and s.get("pt", now) > st["rebase"]:
                for k, v in pack.items():
                    if owp.get(k): owp[k] = max(0, owp[k] - v[0])
                st["rebase"] = False
            if old is not None and not fresh and not skip:
                for k, v in pack.items():
                    o = old.get(k); diff = v[0] - (o[0] if o else 0)
                    if diff > 0 and owp.get(k): back = min(diff, owp[k]); owp[k] -= back; diff -= back
                    if diff > 0 and k[0] != GOLD_GRAPHIC:
                        nm = RE_COUNT.sub("", (v[1] or "").strip()) or "Item 0x%04X" % k[0]
                        record("loot", nm.title(), diff)
                    elif diff < 0 and k[0] in CONSUMABLES: record("consum", CONSUMABLES[k[0]], -diff)
                for k, o in old.items():
                    if k not in pack and k[0] in CONSUMABLES: record("consum", CONSUMABLES[k[0]], o[0])
            st["pack"] = pack
        if st["buffq"]:
            for title in st["buffq"]: record("buffs", title, 1)
            st["buffq"] = []
    def hit(ser, dmg, now):
        me = st["me"]; name = mob_name(ser); record("dmg_nearby", name, dmg, ser); w = st["watch"].get(ser)
        if w is None:
            if len(st["watch"]) >= WATCH_MAX:
                oldest = min(st["watch"].items(), key=lambda kv: kv[1]["t"])[0]; st["watch"].pop(oldest, None)
            w = st["watch"][ser] = {"name": name, "t": now, "mine": 0.0, "friend": False}
        w["t"], w["name"] = now, name
        if is_friend(ser):
            w["friend"] = ser != me["ser"]; record("dmg_taken", name, dmg, ser); enter_combat()
            if ser == me["ser"]: note_taken(dmg, now)
        elif engaged(ser, now):
            st["engaged"][ser] = now; w["mine"] = now; record("dmg_done", name, dmg, ser); record_big(dmg, name, ser)
            enter_combat()
    def read_journal(now):
        me = st["me"]; my_name = me["name"] if me else None
        for ln in st["jr"].new():
            name = ln.name; low = ln.low.strip()
            if my_name and name == my_name:
                sp = SPELLS.get(low)
                if sp is not None:
                    info = Kit.spell_info(sp[0]); delay = float(info[3]) if info and info[3] else 0.0
                    record("spells", sp[0], 1); st["last_spell"] = (now, sp[0], delay); st["cast_t"] = now
                    if sp[1] == "heal": add_pending(now, "heal", sp[0], HEAL_SPELL_SECS)
                    elif sp[1] in ("cure", "cure+"): add_pending(now, sp[1], sp[0], CURE_SECS)
                    continue
                if not low.startswith((MSG_FIZZLE, MSG_NO_MANA)): continue
            elif name and name != "System":
                if my_name:
                    sp = SPELLS.get(low)
                    if sp is not None and sp[0] in HARM_SET: note_cast(now, name, sp[0])
                continue
            if low.startswith(OWN_PREFIX): continue
            if low.startswith(MSG_FIZZLE): record("spells", "Fizzled", 1, side=True)
            elif low.startswith(MSG_INTERRUPT): record("spells", "Interrupted", 1, side=True)
            elif low.startswith(MSG_NO_MANA): record("spells", "Out of mana", 1, side=True)
            elif low.startswith(MSG_BANDAGE_BEGIN): record("consum", "Bandages", 1)
            elif low.startswith(MSG_BANDAGE_CURE): add_pending(now, "cure", "Bandage", BANDAGE_SECS)
            elif low.startswith(MSG_BANDAGE_HEALS): add_pending(now, "heal", "Bandage", BANDAGE_SECS)
            else:
                if "your skill in" in low:
                    m = RE_SKILL.search(low)
                    if m:
                        v = float(m.group(3))
                        record("skills", m.group(1).strip().title(), v if m.group(2).lower() == "increased" else -v)
                        continue
                if "your " in low and " has " in low:
                    m = RE_STAT.search(low)
                    if m:
                        v = int(m.group(3))
                        record("stats", m.group(1).title(), v if m.group(2).lower() == "increased" else -v); continue
                if "you have " in low and ("fame" in low or "karma" in low):
                    m = RE_FAME.search(low)
                    if m: record("fame", "%s %s" % (m.group(2).title(), m.group(1).lower()), 1)
    def find_place(me):
        area = HOST.guard_area()
        if area: return str(area)
        best = None; x, y, m = me["x"], me["y"], me["map"]
        for sp in spots:
            if sp[3] == m:
                d = max(abs(x - sp[1]), abs(y - sp[2]))
                if d <= sp[4] and (best is None or d < best[0]): best = (d, sp[0])
        return best[1] if best is not None else PLACE_ELSEWHERE
    def track_place(now, dt):
        me = st["me"]
        if me is None: return
        if st["place"] is None or now >= st["next_place"]:
            st["next_place"] = now + PLACE_EVERY; st["place"] = find_place(me)
        place = st["place"]
        for seg in segs(): pt = seg["place_t"]; pt[place] = pt.get(place, 0.0) + dt
    def add_spot(name, radius):
        me = st["me"]
        if me is None or not (me["x"] or me["y"]):
            say("position unknown; try again.", Kit.HUE_BAD); return
        name = spot_name(name) or "Spot %d" % (len(spots) + 1); lo, hi = SPOT_RADIUS_LIMITS
        radius = max(lo, min(hi, int(radius))); old = [sp for sp in spots if sp[0].lower() == name.lower()]
        if not old and len(spots) >= SPOTS_MAX:
            say("%d spots at most; remove one first." % SPOTS_MAX, Kit.HUE_BAD); return
        for sp in old: spots.remove(sp)
        spots.append([name, me["x"], me["y"], me["map"], radius]); save_spots(); st["place"] = None
        say("spot \"%s\" named here (%d, %d), %d tiles round." % (name, me["x"], me["y"], radius), Kit.HUE_GOOD)
        HOST.refresh_settings(KEY)
    def remove_spot(name):
        n = len(spots); spots[:] = [sp for sp in spots if sp[0] != name]
        if len(spots) != n: save_spots(); st["place"] = None; HOST.refresh_settings(KEY)
    def friendly_names(now):
        fn = st["fnames"]
        if fn is not None and fn[0] == now: return fn[1]
        mobs = st["mobs"]; names = set(mobs.get(ser) for ser in st["friendly"] if mobs.get(ser))
        st["fnames"] = (now, names); return names
    def note_cast(now, name, spell):
        if name in friendly_names(now): return
        info = Kit.spell_info(spell); delay = float(info[3]) if info else 0.0; cs = st["casts"]
        cs.append([now, name, spell, False, delay])
        while cs and (len(cs) > CASTS_KEEP or now - cs[0][0] > cs[0][4] + CAST_CREDIT_SECS): cs.pop(0)
    def credit_hit(now):
        for c in st["casts"]:
            el = now - c[0]
            if not c[3] and c[4] - CAST_EARLY <= el <= c[4] + CAST_CREDIT_SECS:
                c[3] = True; return "%s: %s" % (c[1], c[2]), c[1], 0
        best = None
        for ser, t in st["engaged"].items():
            if best is None or t > best[1]: best = (ser, t)
        if best is not None and engaged(best[0], now): nm = mob_name(best[0]); return nm + "?", nm, best[0]
        me = st["me"]
        if me is not None and me["poison"]: return "Poison", None, 0
        return "Unknown", None, 0
    def note_taken(dmg, now):
        me = st["me"]; who, nm, ser = credit_hit(now); tk = st["taken"]
        tk.append((now, dmg, who, nm, ser, me["hits"], me["hmax"]))
        if len(tk) > TAKEN_KEEP: del tk[:len(tk) - TAKEN_KEEP]
    def make_recap(now):
        t0 = now - RECAP_SECS; hits = [e for e in st["taken"] if e[0] >= t0]; hp, before = [], None
        for h in st["hp_log"]:
            if h[0] < t0: before = h
            else: hp.append(h)
        if before is not None: hp.insert(0, (t0, before[1], before[2]))
        me = st["me"]
        if me is not None: hp.append((now, 0, me["hmax"]))
        want = set(e[3] for e in hits if e[3] and not e[4]); sers = {}
        if want:
            for ser, nm in st["mobs"].items():
                if nm in want: sers[nm] = ser
            for m in API.GetAllMobiles() or []:
                try:
                    nm = str(m.Name or "")
                    if nm in want:
                        sers[nm] = int(m.Serial)
                        if m.IsHuman: humans[nm.lower()] = now
                except Exception: continue
        rows = [(e[0], e[1], e[2], e[4] or sers.get(e[3], 0), e[5], e[6], e[3]) for e in hits]
        st["recap"] = {"t": now, "rows": rows, "hp": hp, "total": sum(e[1] for e in hits)}; st["recap_show"] = True
    def own_death(now):
        me = st["me"]
        if me is None or now - st["dead_seen"].get(me["ser"], 0) <= 10: return
        record("deaths", mob_name(me["ser"]), 1, me["ser"]); st["dead_seen"][me["ser"]] = now
        if settings["recap"]: make_recap(now)
    def export(w):
        seg = seg_for(w); cap = seg_caption(w)
        if seg is None: seg, cap = data["overall"], "Overall"
        me = st["me"]; serial = me["ser"] if me else int(safe(lambda: API.Player.Serial, 0) or 0)
        path = Kit.data_path(EXPORT_FILE % serial); what = seg["name"] if cap != seg["name"] else ""
        lines = ["Meters export: %s%s, %s" % (cap, " (%s)" % what if what else "", time.strftime("%Y-%m-%d %H:%M:%S",
                                                             time.localtime(time.time()))),
                 ("Session time %s, in combat %s" % (fmt_time(wall_secs(seg)), fmt_time(seg["combat"]))
                  if seg["kind"] == "overall" else "Fight time %s" % fmt_time(combat_secs(seg))), ""]
        for mid in ORDER:
            head, rows = view(mid, seg, EXPORT_ROWS); lines.append("== %s ==" % METRIC[mid][0])
            lines.append("   " + "   ".join(h for h in head if h))
            for i, r in enumerate(rows): lines.append("   %2d. %-30s %s" % (i + 1, r[0], r[2]))
            if not rows: lines.append("   (nothing)")
            lines.append("")
        st["to_write"].append((path, os.linesep.join(lines) + os.linesep, cap))
    def write_files():
        while st["to_write"] and not st["shutting"]:
            path, text, cap = st["to_write"].pop(0)
            try: Kit.write_safe(path, text); say("%s exported to %s." % (cap, path), Kit.HUE_GOOD)
            except Exception as ex: say("couldn't write %s (%s)." % (path, ex), Kit.HUE_BAD)
    M = Kit.MARGIN
    def dock_key(w): return KEY if w["id"] == 0 else "%s_%d" % (KEY, w["id"])
    def win_title(w): return TITLE if w["id"] == 0 else "%s %d" % (TITLE, w["id"] + 1)
    def on_disposed(w, g):
        def handler(*args):
            if w["g"] is g and not st["shutting"]:
                w["g"] = None
                if w["id"] == 0: HOST.disable(KEY)
                else: queue.add(("closed", w["id"]), dup=True)
        return handler
    def on_sub_disposed(w, slot, g):
        def handler(*args):
            if w.get(slot) is g: w[slot] = None
        return handler
    def row_click(w, i):
        def handler(*args):
            slots = w["slots"]
            if i >= len(slots): return
            ser = slots[i].get("ser")
            if Follow.alt_held():
                if ser: queue(("follow", ser))()
                return
            queue(("detail", w["id"], i))()
        return handler
    def foot_need(w):
        n = 8 + 35 + Kit.text_w("New") + 14 + 35 + Kit.text_w("Report") + 8
        return n + 14 + 35 + Kit.text_w("Reset") if w["id"] == 0 else n
    def build_window(w):
        x, y = w["x"], w["y"]; old = w["g"]
        if Kit.is_open(old): x, y = old.GetX(), old.GetY()
        w["g"] = None; store, c, slots, gcols = ({}, {}), {}, [], []; mid = w["metric"]
        close_tip = ("Close " + win_title(w) + (" (this window only)" if w["id"]
                      else " (turns it off; the Modules tab turns it back on)"))
        w["resize_at"], w["preview"] = 0.0, False
        if w["minimized"]:
            g = G.CreateGump(True, True); ww, hh = MINI_W, MINI_H
            c["status"] = Kit.mini_bar(g, store, ww, hh, win_title(w), dock_key(w),
                                       queue(("toggle_min", w["id"])), close_tip=close_tip)
        else:
            rows = settings["rows"]; yb = M + 30 + Kit.GAP; yr = yb + 30 + Kit.GAP
            extra_h = 56 + (GRAPH_BLOCK if w.get("graph") else 0)
            foot_w = foot_need(w); fit = w["fit"]; want = fit if fit is not None else w["size"]
            fw_room = (max(120, want[0]) if want else W) - 2 * M; two_rows = foot_w > fw_room
            if two_rows: extra_h += 26
            body_h = extra_h + rows * ROW_H; ww, hh = W, yr + body_h + M
            if want is not None:
                ww, hh = max(120, want[0]), want[1]; rows = max(1, (hh - yr - M - extra_h) // ROW_H)
                body_h = max(extra_h + rows * ROW_H, hh - yr - M)
                if fit is not None:
                    body_h = max(30, min(body_h, hh - yr - M)); rows = max(0, (body_h - extra_h) // ROW_H)
                hh = yr + body_h + M
            IW = ww - 2 * M
            if fit is None:
                x, y = Kit.clamp(x, y, ww, hh); min_h = yr + extra_h + ROW_H + M
                g = G.CreateModernGump(x, y, ww, hh, True, min(SIZE_MIN_W, ww), min(min_h, hh), on_resized(w))
                g.SetAlpha(0)
            else: g = G.CreateGump(True, True)
            Kit.add_window_frame(g, ww, hh, mouse=False); chrome = 0 if Kit.zone_up(dock_key(w)) else 84 + Kit.DOCK_DX
            title_room = (Kit.MARGIN + 30 + Kit.text_w(win_title(w).upper()) + 16 + chrome
                          + 35 + Kit.text_w("Settings") + Kit.MARGIN)
            Kit.title_bar(g, store, ww, win_title(w), dock_key(w), queue(("toggle_min", w["id"])),
                          queue(("to_bar", w["id"])),
                          queue(("settings",)) if ww >= title_room else None, close_tip=close_tip)
            Kit.add_section(g, M, yb, IW, 30); bx = M + 8
            Kit.art_button(g, store, "prev", ART_LEFT, bx, yb + 4, None,
                           "Show previous display", on_click=queue(("step", w["id"], -1)))
            Kit.art_button(g, store, "next", Kit.ART_PLAY, bx + 32, yb + 4, None,
                           "Show next display", on_click=queue(("step", w["id"], 1)))
            mt, _, _, color, mobrows = METRIC[mid]; mx = bx + 68
            room = M + IW - 6 - mx - 35 - 10 - 35 - 40
            pick_cap = mt if room >= Kit.text_w(mt) else (Kit.fit(mt, room) if room >= 40 else None)
            Kit.art_button(g, store, "pick", Kit.ART_PAGE, mx, yb + 4, pick_cap, "Pick what this window shows"
                           + ("" if pick_cap == mt else " (now: %s)" % mt), on_click=queue(("picker", w["id"])))
            sx = mx + (35 + Kit.text_w(pick_cap) if pick_cap else 30) + 10
            c["seg_room"], c["iw"] = max(20, M + IW - 6 - sx - 35), IW; seg_cap = Kit.fit(seg_caption(w), c["seg_room"])
            c["seg"] = Kit.art_button(g, store, "segs", Kit.ART_PAGE, sx, yb + 4, seg_cap,
                                      "Pick a segment: current fight, Overall or an earlier fight",
                                      on_click=queue(("segpick", w["id"])))
            Kit.add_section(g, M, yr, IW, body_h); c["head"] = Kit.add_label(g, "", M + 8, yr + 5, Kit.HUE_INFO)
            follow = "Alt+click: auto-follow (again to stop)"
            if mid in ("session", "big", "gold"): tip = follow if mobrows else None
            else: tip = "Show this row's details" + (". " + follow if mobrows else "")
            val_w = min(VAL_W, int(IW * 0.45)); name_w = IW - 12 - val_w - 10
            for i in range(rows):
                ry = yr + 26 + i * ROW_H; pb = G.CreateGumpSimpleProgressBar(IW - 12, ROW_H - 2, BAR_BG, color, 0, 100)
                pb.SetPos(M + 6, ry); pb.SetAcceptMouseInput(False); g.Add(pb)
                ln = Kit.add_label(g, "", M + 10, ry + 1, Kit.HUE_TEXT)
                lv = Kit.add_label(g, "", M + IW - 6 - val_w, ry + 1, Kit.HUE_TEXT)
                slots.append({"bar": pb, "name": ln, "val": lv, "ser": None, "key": None,
                              "prog": None, "nw": name_w, "vw": val_w})
            for i in range(rows):
                ry = yr + 26 + i * ROW_H; Kit.catcher(g, M + 6, ry, IW - 12, ROW_H - 2, row_click(w, i), tip)
            fy = yr + 26 + rows * ROW_H + 4
            if w.get("graph"):
                gy = fy - 2; c["gcap"] = Kit.add_label(g, "", M + 10, gy, Kit.HUE_INFO); base = gy + 18 + GRAPH_H
                ncol = max(1, min(GRAPH_MINUTES, (IW - 12) // (GRAPH_COL + 1)))
                gx = M + 6 + (IW - 12 - ncol * (GRAPH_COL + 1)) // 2
                for i in range(ncol):
                    box = G.CreateGumpColorBox(0.9, color)
                    box.SetRect(gx + i * (GRAPH_COL + 1), base - 1, GRAPH_COL, 1)
                    box.IsVisible = False; box.SetAcceptMouseInput(False)
                    g.Add(box); gcols.append({"box": box, "x": gx + i * (GRAPH_COL + 1), "h": 0})
                c["gbase"] = base; fy += GRAPH_BLOCK
            Kit.art_button(g, store, "new", Kit.ART_PAGE, M + 8, fy, "New",
                           "Open another window (up to %d)" % MAX_WINDOWS, on_click=queue(("new",)))
            rx = M + 8 + 35 + Kit.text_w("New") + 14
            Kit.art_button(g, store, "report", Kit.ART_PAGE, rx, fy, "Report",
                           "Post the top %d rows to party chat (if set and in a party), else the journal" % REPORT_ROWS,
                           on_click=queue(("report", w["id"])))
            if w["id"] == 0:
                ry2 = fy + 26 if two_rows else fy
                Kit.art_button(g, store, "reset", Kit.ART_CLOSE, ww - M - 8 - 35 - Kit.text_w("Reset"),
                               ry2, "Reset", "Clear all meters; new session", on_click=queue(("reset",)))
        w["x"], w["y"] = Kit.show_window(g, x, y, ww, hh, dock_key(w), w["minimized"] and w["docked"],
                                         on_disposed(w, g), save_windows, w,
                                         {"g": g, "c": c, "store": store, "slots": slots, "vkey": None,
                                          "gcols": gcols, "gkey": None, "drawn": (ww, hh)})
        for k in ("picker", "segpick", "detail"):
            sub = w.get(k)
            if Kit.is_open(sub) and not w["minimized"]:
                info = Kit.scroll_info(sub)
                if info is not None: sw, sh = int(info["w"]), int(info["h"])
                else: sw, sh = int(sub.GetWidth() or PICK_W), int(sub.GetHeight() or 200)
                sx, sy = side_pos(w, sw); Kit.place(sub, sx, sy, sw, sh); Kit.attach(sub, g)
        refresh(w); Kit.dispose(old)
    def on_resized(w):
        def fn(*args):
            w["resize_at"] = time.time(); g = w["g"]
            if w["preview"] or w["fit"] is not None or w["minimized"] or not Kit.is_open(g): return
            if (int(g.GetWidth()), int(g.GetHeight())) != w["drawn"]: w["preview"] = True; g.SetAlpha(0.55)
        return fn
    def apply_resize(w):
        g = w["g"]; w["preview"] = False
        if not Kit.is_open(g) or w["minimized"]: return
        gw, gh = int(g.GetWidth()), int(g.GetHeight())
        if w["fit"] is not None:
            g.SetAlpha(0)
            if (gw, gh) != w["drawn"]: build_window(w)
            return
        drawn = w["drawn"] or (0, 0)
        if abs(gw - drawn[0]) <= 2 and abs(gh - drawn[1]) <= 2: g.SetAlpha(0); return
        w["size"] = own_size(gw, gh); build_window(w); save_windows()
    def side_pos(w, width):
        g = w["g"]; r = Kit.rect(g) if Kit.is_open(g) else None
        x, y = (r[0], r[1]) if r is not None else (w["x"], w["y"])
        sw = Kit.screen()[0]; nx = x + ((w.get("drawn") or (W, 0))[0]) + 4
        if sw and nx + width > sw: nx = max(0, x - width - 4)
        return nx, y
    def sub_frame(width, hh, title, store, close_key, action, g=None):
        if g is None: g = G.CreateGump(True, True)
        Kit.add_window_frame(g, width, hh); Kit.add_section(g, M, M, width - 2 * M, 30)
        Kit.add_label(g, title, M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, store, close_key, Kit.ART_CLOSE, width - M - 54, M + 4, None, "Close this window",
                   on_click=queue(action))
        return g
    def drop_sub(w, slot): Kit.dispose(w[slot]); w[slot] = None
    def show_sub(w, slot, g, width, hh):
        x0, y0 = side_pos(w, width)
        Kit.show_window(g, x0, y0, width, hh, None, False, on_sub_disposed(w, slot, g), None, w, {slot: g})
        Kit.attach(g, w["g"])
    def build_picker(w):
        drop_sub(w, "picker"); IW = PICK_W - 2 * M; col = (IW - 24) // 2
        hs = [28 + ((len(ms) + 1) // 2) * 22 + 6 for _, ms in GROUPS]; h_win = 28 + 2 * 22 + 6
        hh = M + 30 + sum(h + Kit.GAP for h in hs) + h_win + Kit.GAP + M
        g = sub_frame(PICK_W, hh, "DISPLAYS", ({}, {}), "pclose", ("close_sub", w["id"], "picker"))
        y = M + 30 + Kit.GAP
        for (gname, ms), h in zip(GROUPS, hs):
            Kit.add_section(g, M, y, IW, h, gname)
            for i, mid in enumerate(ms):
                cx = M + 12 + (i % 2) * (col + 12); cy = y + 28 + (i // 2) * 22
                hue = Kit.HUE_TITLE if mid == w["metric"] else Kit.HUE_TEXT
                Kit.add_label(g, Kit.fit(METRIC[mid][0], col - 4), cx, cy, hue)
                Kit.catcher(g, cx - 2, cy - 2, col, 20, queue(("metric", w["id"], mid)),
                            "Show %s in this window" % METRIC[mid][0])
            y += h + Kit.GAP
        Kit.add_section(g, M, y, IW, h_win, "THIS WINDOW"); on = bool(w.get("graph")); state = "on" if on else "off"
        Kit.add_label(g, Kit.fit("Last-hour graph", IW - 36 - Kit.text_w(state)), M + 12, y + 28)
        Kit.add_label(g, state, M + IW - 12 - Kit.text_w(state), y + 28, Kit.HUE_GOOD if on else Kit.HUE_INFO)
        Kit.catcher(g, M + 8, y + 26, IW - 16, 20, queue(("graph", w["id"])),
                    "Show or hide the last hour under the rows, one bar per minute")
        Kit.add_label(g, Kit.fit("Export this segment", IW - 24), M + 12, y + 50)
        Kit.catcher(g, M + 8, y + 48, IW - 16, 20, queue(("export", w["id"])),
                    "Write every display to %s in the VirtueAssistantSettings folder"
                    % (EXPORT_FILE.replace("%08X", "<serial>")))
        show_sub(w, "picker", g, PICK_W, hh)
    def build_segpick(w):
        drop_sub(w, "segpick"); IW = PICK_W - 2 * M
        items = [("current", "Current fight" + (" (going on)" if data["cur"] else " (or the last)"), ""),
                 ("overall", "Overall (session)", fmt_time(time.time() - data["overall"]["start"]))]
        for h in data["hist"]:
            items.append((h["n"], "#%d  %s" % (h["n"], seg_name(h)),
                          "%s  %s" % (fmt_time(combat_secs(h)), fmt_num(total(h, "dmg_done")))))
        sh = 28 + len(items) * 22 + 6; hh = M + 30 + Kit.GAP + sh + M
        g = sub_frame(PICK_W, hh, "SEGMENTS", ({}, {}), "sclose", ("close_sub", w["id"], "segpick"))
        y = M + 30 + Kit.GAP; Kit.add_section(g, M, y, IW, sh, "WHAT TO SHOW  (fight time, damage done)"); rw = 110
        for i, (val, text, right) in enumerate(items):
            cy = y + 28 + i * 22; hue = Kit.HUE_TITLE if val == w["seg"] else Kit.HUE_TEXT
            Kit.add_label(g, Kit.fit(text, IW - 24 - rw - 6), M + 12, cy, hue)
            if right: Kit.add_label(g, right, M + IW - 12 - rw, cy, Kit.HUE_INFO)
            Kit.catcher(g, M + 8, cy - 2, IW - 16, 20, queue(("seg", w["id"], val)), "Show this segment")
        show_sub(w, "segpick", g, PICK_W, hh)
    DETAIL_LINES = ("Total", "Share", "Rate", "Times", "Average", "Biggest", "Smallest", "First", "Last")
    def build_detail(w):
        drop_sub(w, "detail"); IW = DETAIL_W - 2 * M; sh = 30 + len(DETAIL_LINES) * 20 + 6
        hh = M + 30 + Kit.GAP + sh + M
        g = sub_frame(DETAIL_W, hh, "DETAILS", ({}, {}), "dclose", ("close_sub", w["id"], "detail")); c = {}
        y = M + 30 + Kit.GAP; Kit.add_section(g, M, y, IW, sh)
        c["name"] = Kit.add_label(g, "", M + 10, y + 6, Kit.HUE_TITLE)
        lw = max(Kit.text_w(t) for t in DETAIL_LINES) + 14
        for i, t in enumerate(DETAIL_LINES):
            ly = y + 30 + i * 20; Kit.add_label(g, t, M + 10, ly, Kit.HUE_INFO)
            c[t] = Kit.add_label(g, "", M + 10 + lw, ly, Kit.HUE_TEXT)
        c["vw"] = IW - 20 - lw; w["dc"] = c; show_sub(w, "detail", g, DETAIL_W, hh); refresh_detail(w)
    def refresh_graph(w):
        mid = w["metric"]; m = int(time.time() // 60); key = (mid, m, graph["ver"], graph["vb"].get(mid, 0))
        if key == w["gkey"]: return
        w["gkey"] = key; hist = graph["hist"]; vals = []; top = 0.0
        if mid != "session":
            first = m - GRAPH_MINUTES + 1
            for i in range(GRAPH_MINUTES):
                b = hist.get(first + i); v = b.get(mid, 0.0) if b is not None else 0.0
                if v > top: top = v
                vals.append(v)
        base = w["c"]["gbase"]; skip = len(vals) - len(w["gcols"])
        for i, col in enumerate(w["gcols"]):
            v = vals[i + skip] if vals else 0.0; h = int(round(GRAPH_H * v / top)) if top > 0 and v > 0 else 0
            if v > 0 and h < 1: h = 1
            if h != col["h"]:
                box = col["box"]
                if h: Kit.ui_rect(box, col["x"], base - h, GRAPH_COL, h)
                if (h > 0) != (col["h"] > 0): box.IsVisible = h > 0
                col["h"] = h
        if mid == "session": cap = "No graph for the summary"
        elif top <= 0: cap = "Last hour, per minute: nothing yet"
        else:
            cap = "Last hour, %s per minute: peak %s" % (
                "biggest hit" if mid == "big" else "gained" if mid in ("gold", "gold_place")
                else "total", fmt_num(top, METRIC[mid][2] or "n"))
        Kit.set_text(w["c"]["gcap"], Kit.fit(cap, w["c"].get("iw", W - 2 * Kit.MARGIN) - 20))
    def fit_once(holder, k, text, width):
        f = holder.get(k)
        if f is not None and f[0] == text and f[1] == width: return f[2]
        cut = Kit.fit(text, width); holder[k] = (text, width, cut); return cut
    def recap_click(i):
        def handler(*args):
            sers = recap["rows"]
            if i < len(sers) and sers[i] and Follow.alt_held(): queue(("follow", sers[i]))()
        return handler
    def recap_hp_at(hp, t):
        cur = hp[0] if hp else (t, 0, 0)
        for h in hp:
            if h[0] > t: break
            cur = h
        return cur[1], cur[2]
    def build_recap():
        rc = st["recap"]
        if rc is None: return
        IW = RECAP_W - 2 * M; rows = rc["rows"][-RECAP_ROWS:]; strip_h = 30
        sh = 30 + 20 + strip_h + 8 + max(1, len(rows)) * 20 + 2 * 18 + 6; hh = M + 30 + Kit.GAP + sh + M
        g, store, _c = recapw.begin(RECAP_W, hh, side_pos(wins[0], RECAP_W) if wins else None)
        sub_frame(RECAP_W, hh, "DEATH RECAP", store, "close", ("recap_close",), g); y0 = M + 30 + Kit.GAP
        Kit.add_section(g, M, y0, IW, sh, "LAST %d SECONDS  (damage you took)" % int(RECAP_SECS)); n = len(rc["rows"])
        head = "Died %s: %s damage in %s" % (
            time.strftime("%H:%M:%S", time.localtime(rc["t"])), fmt_num(rc["total"]), Kit.count(n, "hit"))
        Kit.add_label(g, Kit.fit(head, IW - 20), M + 10, y0 + 26, Kit.HUE_TEXT); ys = y0 + 26 + 20
        Kit.add_label(g, "HP", M + 10, ys + (strip_h - 16) // 2, Kit.HUE_INFO); sx0 = M + 10 + Kit.text_w("HP") + 8
        cw = max(2, (M + IW - 10 - sx0) // RECAP_COLS); t0 = rc["t"] - RECAP_SECS
        for i in range(RECAP_COLS):
            hits, hmax = recap_hp_at(rc["hp"], t0 + (i + 1) * RECAP_SECS / RECAP_COLS)
            bh = int(round(strip_h * max(0, hits) / float(hmax))) if hmax > 0 else 0
            if bh > 0:
                box = G.CreateGumpColorBox(0.9, "#c22d2d")
                box.SetRect(sx0 + i * cw, ys + strip_h - bh, max(1, cw - 1), bh); g.Add(box)
        yr = ys + strip_h + 8; sers = []
        if not rows: Kit.add_label(g, "No damage seen.", M + 10, yr, Kit.HUE_INFO)
        who_x = max(M + 60, M + 16 + Kit.text_w("-10.0 s")); who_w = IW - 106 - (who_x - M)
        for i, (t, dmg, who, ser, hits, hmax, nm) in enumerate(rows):
            ry = yr + i * 20; Kit.add_label(g, "-%.1f s" % max(0.0, rc["t"] - t), M + 10, ry, Kit.HUE_INFO)
            who = shown(nm, ser, True) + who[len(nm):] if nm and who.startswith(nm) else shown(who, ser)
            Kit.add_label(g, Kit.fit(who, who_w), who_x, ry, Kit.HUE_TEXT); amt = "-%s" % fmt_num(dmg)
            Kit.add_label(g, amt, M + IW - 64 - Kit.text_w(amt), ry, Kit.HUE_BAD)
            Kit.add_label(g, "HP %d" % hits, M + IW - 58, ry, Kit.HUE_INFO); sers.append(ser if is_mobile(ser) else 0)
            if sers[-1]:
                Kit.catcher(g, who_x - 2, ry - 2, who_w + 4, 20, recap_click(i),
                            "Alt+click: auto-follow (again to stop)")
        for i, line in enumerate(RECAP_HINT):
            Kit.add_label(g, Kit.fit(line, IW - 20), M + 10, y0 + sh - 40 + i * 18, Kit.HUE_INFO)
        recapw.end(g, {"rows": sers})
    recapw = Kit.Window(KEY, TITLE, None, recap, build_recap, RECAP_POS_KEY, cleanup=cleanup, names=None, lock=False,
                        owner=False, clear={"rows": []})
    wnd = None
    def refresh(w):
        g = w["g"]
        if not Kit.is_open(g): return
        mid = w["metric"]
        if w.get("gcols") and not w["minimized"]: refresh_graph(w)
        seg = seg_for(w); me = st["me"]; my_name = me["name"] if me else None; key = None
        if seg is not None:
            if seg["end"] is not None:
                key = (mid, w["seg"], seg["uid"], seg["ver"], w["minimized"], settings["rank"],
                       settings["pct"], my_name)
            elif METRIC[mid][1] == "s":
                key = (mid, w["seg"], seg["uid"], seg["ver"], seg["combat"], w["minimized"],
                       settings["rank"], settings["pct"], my_name)
            if key is not None and key == w.get("vkey"): refresh_detail(w); return
        w["vkey"] = key; head, rows = view(mid, seg, 0 if w["minimized"] else len(w["slots"])); c = w["c"]
        if w["minimized"]:
            lbl = c.get("status")
            if lbl is not None:
                Kit.set_text(lbl, fit_once(c, "_fst", "%s: %s  %s" % (win_title(w), METRIC[mid][0],
                                                                      "  ".join(head[:2])), MINI_W - 90))
            return
        Kit.set_text(c["head"], fit_once(c, "_fhd", "   ".join(h for h in head if h),
                                         c.get("iw", W - 2 * Kit.MARGIN) - 16))
        Kit.set_text(c["seg"], fit_once(c, "_fsg", seg_caption(w), c.get("seg_room", 400)))
        top = max([r[1] for r in rows] + [0.0])
        for i, slot in enumerate(w["slots"]):
            if i < len(rows):
                name, val, text, ser, _ = rows[i]; who = shown(name, ser)
                label = ("%d. %s" % (i + 1, who)) if settings["rank"] else who
                hue = Kit.HUE_TITLE if (my_name and name == my_name) else Kit.HUE_TEXT
                Kit.set_text(slot["name"], fit_once(slot, "_fn", label, slot["nw"]), hue)
                Kit.set_text(slot["val"], fit_once(slot, "_fv", text, slot.get("vw", VAL_W)))
                prog = (float(val), float(top or 1.0))
                slot["ser"], slot["key"] = (ser if is_mobile(ser) else None), name
            else:
                Kit.set_text(slot["name"], ""); Kit.set_text(slot["val"], ""); prog = (0.0, 1.0)
                slot["ser"], slot["key"] = None, None
            if prog != slot["prog"]: slot["prog"] = prog; slot["bar"].SetProgress(prog[0], prog[1])
        refresh_detail(w)
    def refresh_detail(w):
        if not Kit.is_open(w["detail"]): return
        c = w["dc"]; mid, key = w["detail_metric"], w["detail_row"]; seg = seg_for(w)
        r = seg["d"].get(mid, {}).get(key) if (seg is not None and mid) else None
        ser = seg["serial"].get((mid, key)) if seg is not None and mid else None
        Kit.set_text(c["name"], Kit.fit("%s (%s)" % (shown(key, ser) or "", METRIC.get(mid, ("",))[0]),
                                      DETAIL_W - 2 * Kit.MARGIN - 20))
        vals = dict((t, "") for t in DETAIL_LINES)
        if r is not None:
            _, rate, f, _, _ = METRIC[mid]; now = time.time(); tot = total(seg, mid)
            if mid == "gold_place":
                pr, secs = place_rate(seg, key, r[0]); rate_txt = "%s/h (%s there)" % (fmt_rate(pr), fmt_time(secs))
            elif rate: rate_txt = "%s %s" % (fmt_rate(rate_of(seg, rate, r[0]), f), RATE_WORD[rate])
            else: rate_txt = "-"
            vals.update({"Total": fmt_num(r[0], f),
                "Share": ("%d%% of %s" % (int(round(100.0 * r[0] / tot)), fmt_num(tot, f))
                          if tot and not pct_row(key) else "-"), "Rate": rate_txt, "Times": "%d" % r[1],
                "Average": fmt_num(r[0] / max(1, r[1]), f), "Biggest": fmt_num(r[2], f), "Smallest": fmt_num(r[3], f),
                "First": "%s ago" % fmt_time(now - r[4]), "Last": "%s ago" % fmt_time(now - r[5])})
        elif key: vals["Total"] = "nothing in this segment"
        for t in DETAIL_LINES: Kit.set_text(c[t], Kit.fit(vals[t], c["vw"]))
    def drag_busy(): return bool(SNAP.drag) or SNAP.pressed() is True
    def layout_fit(w):
        def fit(fw, fh, mode):
            new = (int(fw), int(fh)) if (fw is not None and fh is not None) else None
            if new != w.get("fit") or (mode == "again" and new is not None):
                w["fit"] = new; queue(("redraw", w["id"]))()
        return fit
    def layout_min(w):
        def mn():
            extra_h = 56 + (GRAPH_BLOCK if w.get("graph") else 0) + (26 if foot_need(w) > SIZE_MIN_W - 2 * M else 0)
            return SIZE_MIN_W, M + 30 + Kit.GAP + 30 + Kit.GAP + extra_h + ROW_H + M
        return mn
    def check_zones():
        if drag_busy(): return
        for w in wins:
            g = w["g"]
            if w["minimized"] or w["docked"] or w["resize_at"] or not Kit.is_open(g): continue
            want = HOST.layout_slot(dock_key(w))
            if want is not None:
                want = (int(want[0]), int(want[1])); fit = w["fit"]
                if fit is None or abs(fit[0] - want[0]) > 4 or abs(fit[1] - want[1]) > 4:
                    w["fit"] = want; build_window(w); continue
                if w["drawn"] is None or w["drawn"][0] != max(120, fit[0]): build_window(w); continue
                real = (int(g.GetWidth()), int(g.GetHeight()))
                if abs(real[0] - w["drawn"][0]) > 2 or abs(real[1] - w["drawn"][1]) > 2:
                    w["misfit"] = w.get("misfit", 0) + 1
                    if w["misfit"] in (2, 6, 20): build_window(w)
                else: w["misfit"] = 0
            elif w["fit"] is not None and not HOST.layout_holds(dock_key(w)):
                w["fit"] = None; build_window(w)
    def dock_win(w):
        hooks = Kit.dock_hooks(win_title(w), TRAY_ICON, w, w, queue(("redraw", w["id"])), fit=layout_fit(w))
        hooks.update({"exact": True, "verify": True, "pieces_out": True, "min": layout_min(w)})
        HOST.dock_add(dock_key(w), hooks)
    def close_window(w, remove):
        w["shutting"] = True; HOST.dock_remove(dock_key(w))
        if remove: HOST.dock_forget(dock_key(w))
        for k in ("picker", "segpick", "detail", "g"): g, w[k] = w[k], None; Kit.dispose(g)
        if remove and w in wins: wins.remove(w)
    def report(w):
        mid = w["metric"]; seg = seg_for(w); head, rows = view(mid, seg, REPORT_ROWS)
        title = "%s (%s)" % (METRIC[mid][0], seg_caption(w))
        parts = ["%d. %s %s" % (i + 1, shown(r[0], r[3]), r[2]) for i, r in enumerate(rows[:REPORT_ROWS])]
        if settings["party"] and API.GetPartyMemberSerials():
            body = "; ".join(parts) or "nothing yet"; msg = "%s: %s; %s" % (title, "  ".join(head[:2]), body)
            lines = [msg] if len(msg) <= PARTY_MSG_MAX else ["%s: %s" % (title, "  ".join(head[:2])), body]
            for line in lines:
                if len(line) > PARTY_MSG_MAX: line = line[:PARTY_MSG_MAX - 2] + ".."
                API.PartyMsg(line)
        else:
            say("%s: %s." % (title, "  ".join(head)), Kit.HUE_INFO)
            for p in parts or ["nothing yet"]: say("   %s." % p, Kit.HUE_TEXT)
    def act_new(action, w):
        if len(wins) >= MAX_WINDOWS: say("%d windows at most." % MAX_WINDOWS, Kit.HUE_INFO); return
        base = wins[-1]; g = base["g"]; bx, by = (g.GetX(), g.GetY()) if Kit.is_open(g) else (base["x"], base["y"])
        nid = max(x["id"] for x in wins) + 1; used = set(x["metric"] for x in wins)
        metric = next((m for m in ORDER if m not in used), DEFAULT_METRIC)
        nw = new_win(nid, metric, bx + 30, by + 30); wins.append(nw); build_window(nw); dock_win(nw); save_windows()
    def act_own_size(action, w):
        for ow in wins:
            had = ow["size"] is not None; ow["size"] = None
            if had and ow["fit"] is None and Kit.is_open(ow["g"]): build_window(ow)
        save_windows()
    def act_reset(action, w): reset_data(); st["next_ui"] = 0.0; say("all meters cleared; new session.", Kit.HUE_GOOD)
    def act_recap(action, w):
        if st["recap"] is None: say("no death this session.", Kit.HUE_INFO)
        else: build_recap()
    def act_restyle(action, w):
        for ow in wins:
            for k, fn in (("picker", build_picker), ("segpick", build_segpick), ("detail", build_detail)):
                if Kit.is_open(ow[k]): fn(ow)
        if Kit.is_open(recap["g"]): build_recap()
    def act_graph(action, w):
        w["graph"] = not w.get("graph"); build_window(w); dock_win(w)
        if Kit.is_open(w["picker"]): build_picker(w)
        save_windows()
    def act_closed(action, w): st["redraw_wait"].discard(w["id"]); close_window(w, True); save_windows()
    def act_toggle_min(action, w):
        w["minimized"], w["docked"] = not w["minimized"], False; HOST.dock_forget(dock_key(w)); build_window(w)
        save_windows()
    def act_redraw(action, w):
        if drag_busy(): st["redraw_wait"].add(w["id"]); return
        st["redraw_wait"].discard(w["id"]); build_window(w); save_windows()
    def act_step(action, w):
        i = ORDER.index(w["metric"]) if w["metric"] in ORDER else 0
        w["metric"] = ORDER[(i + action[2]) % len(ORDER)]; build_window(w)
        if Kit.is_open(w["picker"]): build_picker(w)
        save_windows()
    def act_pick(action, w):
        kind = action[0]
        if Kit.is_open(w[kind]): Kit.dispose(w[kind])
        else: (build_picker if kind == "picker" else build_segpick)(w)
    def act_metric(action, w): w["metric"] = action[2]; Kit.dispose(w["picker"]); build_window(w); save_windows()
    def act_seg(action, w): w["seg"] = action[2]; Kit.dispose(w["segpick"]); refresh(w); save_windows()
    def act_detail(action, w):
        slots = w["slots"]; i = action[2]; key = slots[i].get("key") if i < len(slots) else None
        if key is None or w["metric"] in ("session", "big", "gold"): return
        w["detail_row"], w["detail_metric"] = key, w["metric"]
        if Kit.is_open(w["detail"]): refresh_detail(w)
        else: build_detail(w)
    ACTIONS = {"settings": lambda action, w: HOST.show_settings(KEY),
               "follow": lambda action, w: Follow.toggle(action[1], TITLE), "new": act_new, "own_size": act_own_size,
               "reset": act_reset, "spot_add": lambda action, w: add_spot(action[1], action[2]),
               "spot_rm": lambda action, w: remove_spot(action[1]), "recap": act_recap,
               "recap_close": lambda action, w: recapw.close(), "graph": act_graph,
               "export": lambda action, w: export(w), "closed": act_closed, "toggle_min": act_toggle_min,
               "to_bar": lambda action, w: HOST.dock_to_bar(dock_key(w), win_title(w)), "redraw": act_redraw,
               "step": act_step, "picker": act_pick, "segpick": act_pick, "metric": act_metric, "seg": act_seg,
               "close_sub": lambda action, w: Kit.dispose(w.get(action[2])), "detail": act_detail,
               "report": lambda action, w: report(w), "restyle": act_restyle}
    FREE_KINDS = ("settings", "follow", "new", "own_size", "reset", "spot_add", "spot_rm", "recap", "recap_close",
                  "restyle")
    FIELDS = (("idle", "A fight ends after quiet of:", "No damage for this long ends the fight", "s"),
              ("engage", "Your targets count for:", "Damage on what you attacked or targeted this recently is yours",
               "s"), ("history", "Earlier fights kept:", "Finished fights in the segment list", "fights"),
              ("min_heal", "Ignore HP rises under:", "Smaller rises count as regeneration", "HP"),
              ("rows", "Rows per window:", "For windows at their own size; undoes corner drags", "rows"))
    CHECKS = (("rank", "Number the rows", "A rank before each name"),
              ("pct", "Show each row's share (%)", "Percentage of the total after the value"),
              ("party", "Report to party chat in a party", "Unticked, Report goes to your journal"),
              ("scan", "Watch the backpack (loot, reagents, ammo)",
               "Open your backpack once after login so the client knows its contents"),
              ("travel", "Count tiles walked and recalls / gates", "Fills the Travel display"),
              ("recap", "Show a death recap when you die",
               "The last %d s of damage taken: who, how much, your HP" % int(RECAP_SECS)))
    PCT_HINT = "Pets' and strangers' healing is a \"(%)\" row outside the total."; SPOT_ROW = 24
    def page_table(w):
        return (("COUNTING  (fights, healing, rows)", [("num",) + r + LIMITS[r[0]] for r in FIELDS],
                 {"align": True, "pad": 4}), ("SHOW AND TRACK", [("check",) + r for r in CHECKS] + [
                    ("note", Kit.fit(PCT_HINT, w - 28), {"ndy": 2, "h": 18})], {"pad": 4}),
                ("GOLD BY PLACE  (per character)",
                 (("custom", 28 + max(1, len(spots)) * SPOT_ROW, draw_spots),), {"pad": 4}), ("TOOLS", (
                    ("buttons", (("new", Kit.ART_PAGE, "New meter window", "Open one more (up to %d)" % MAX_WINDOWS),
                                 ("recap", Kit.ART_PAGE, "Last death recap", "Show it again"),
                                 ("own_size", Kit.ART_CLOSE, "Reset sizes",
                                  "Give windows outside zones their own size (Rows above, %d px wide)" % W))),
                    ("buttons", (("export", Kit.ART_OK, "Export",
                                  "Write the first window's segment to %s in the VirtueAssistantSettings folder"
                                  % EXPORT_FILE.replace("%08X", "<serial>")),
                                 ("reset", Kit.ART_CLOSE, "Reset all meters", "Clear everything; new session"))),
                    ("note", Kit.fit("Damage numbers: " + feed["kind"], w - 28), {"key": "feed", "h": 26})),
                 {"pad": 4}))
    def draw_spots(f, x, y):
        g, c, w, store = f.g, f.c, f.w, f.store; Kit.add_label(g, "Name:", x + 12, y + 3)
        nx = x + 12 + Kit.text_w("Name:") + 8
        rest = 133 + Kit.text_w("Radius:") + Kit.text_w("tiles") + Kit.text_w("Name this spot")
        nbw = max(60, min(140, x + w - nx - rest))
        c["spot_name"] = Kit.with_tip(Kit.add_textbox(g, "", nx, y, nbw, numbers=False),
                                      "Spot name (up to %d letters)" % SPOT_NAME_MAX)
        rx = nx + nbw + 12; Kit.add_label(g, "Radius:", rx, y + 3); rx += Kit.text_w("Radius:") + 8
        c["spot_radius"] = Kit.with_tip(Kit.add_textbox(g, str(page.get("radius", SPOT_RADIUS)), rx, y, 44),
                                        "Tiles round you (%d-%d)" % SPOT_RADIUS_LIMITS)
        rx += 44 + 10; Kit.add_label(g, "tiles", rx, y + 3, Kit.HUE_INFO)
        Kit.art_button(g, store, "spot_add", Kit.ART_OK, rx + Kit.text_w("tiles") + 12, y - 2,
                       "Name this spot", "Gold gained within the radius counts here (a guarded town comes first)")
        if not spots:
            Kit.add_label(g, Kit.fit("No spots yet: stand where you farm, type a name, click Name this spot.",
                                   w - 28), x + 12, y + 28 + 3, Kit.HUE_INFO)
        rm_w = Kit.pic_size(Kit.ART_CLOSE[0])[0] or 30
        c["spot_rm"] = [("spot_rm%d" % i, sp[0]) for i, sp in enumerate(spots)]
        for i, sp in enumerate(spots):
            ry = y + 28 + i * SPOT_ROW; where = "facet %d at %d, %d, %d tiles round" % (sp[3], sp[1], sp[2], sp[4])
            ww_ = Kit.text_w(where); Kit.add_label(g, Kit.fit(sp[0], w - 24 - rm_w - 18 - ww_ - 12), x + 12, ry + 3)
            Kit.add_label(g, where, x + w - 12 - rm_w - 12 - ww_, ry + 3, Kit.HUE_INFO)
            Kit.art_button(g, store, "spot_rm%d" % i, Kit.ART_CLOSE, x + w - 12 - rm_w, ry, None, "Remove " + sp[0])
    CONFIG_READ_EVERY = 0.2
    def page_clicks(f):
        c, store = f.c, f.store
        if Kit.was_clicked(store, "own_size"):
            if st["active"]: queue(("own_size",))()
            else: forget_sizes_off()
        todo = [a for k, a in (("reset", ("reset",)), ("new", ("new",)), ("export", ("export", 0)),
                               ("recap", ("recap",))) if Kit.was_clicked(store, k)]
        if Kit.was_clicked(store, "spot_add"):
            page["radius"] = Kit.read_int(c["spot_radius"], SPOT_RADIUS, *SPOT_RADIUS_LIMITS)
            todo.append(("spot_add", str(c["spot_name"].Text or ""), page["radius"]))
        for action in todo:
            if st["active"]: queue(action)()
            else: say("turn Meters on first.", Kit.HUE_INFO)
        for key, name in c["spot_rm"]:
            if Kit.was_clicked(store, key):
                if st["active"]: queue(("spot_rm", name))()
                else: remove_spot(name)
    def show_feed(f, new): Kit.set_text(f.c["feed"], Kit.fit("Damage numbers: " + feed["kind"], f.w - 28))
    def on_change(old, new):
        del data["hist"][new["history"]:]
        if new["rows"] != old["rows"]:
            if st["active"]:
                for w in wins: w["size"] = None; queue(("redraw", w["id"]))()
            else: forget_sizes_off()
        st["next_ui"] = 0.0
    cfg = Kit.Page(settings, page_table, save_settings, on_change, adjust=show_feed, clicks=page_clicks,
                   every=CONFIG_READ_EVERY)
    load_settings(); load_spots(); reset_data()
    def _start():
        st.update({"shutting": False, "active": True, "queue": [], "last_tick": time.time(),
                   "next_ui": 0.0, "next_friends": 0.0, "next_scan": 0.0, "me": None,
                   "pos": None, "pack": None, "prev": {}, "used": [], "buffq": [],
                   "amtq": [], "poked": False, "place": None, "next_place": 0.0, "taken": [], "hp_log": [],
                   "casts": [], "recap": None, "recap_show": False, "to_write": [],
                   "redraw_wait": set(), "present": [], "pscan": None, "pack_cand": None, "my_ser": None,
                   "my_name": "", "next_name": 0.0, "fnames": None, "died": False,
                   "owed": {"gold": 0, "pack": {}, "until": 0.0}, "rebase": False})
        st["jr"] = Journal.reader(); load_settings(); reset_data(); load_windows(); load_spots()
        cleanup.add(unhook_damage); cleanup.service("look.meters", lambda: queue.add(("restyle",)))
        for w in wins:
            w["shutting"] = w["docked"] = False
            if HOST.dock_wanted(dock_key(w)): w["minimized"] = True; w["docked"] = HOST.dock_soon(dock_key(w))
        Kit.hook_once(st, "hooked", ("ObjectUsed", on_used), ("OnBuffAdded", on_buff),
                      ("OnEntityDamage", on_damage_amount), ("OnPlayerDeath", on_died))
        if feed["handler"] is None: del jobs[:]; jobs.append(hook_damage)
        for w in wins:
            slot = HOST.layout_slot(dock_key(w)) if HOST.booting() and w["fit"] is None else None
            if slot and slot[0] and slot[1]: w["fit"] = (int(slot[0]), int(slot[1]))
            build_window(w); dock_win(w)
    def _tick():
        st["poked"] = False
        if not wins or wins[0]["g"] is None: return
        now = time.time(); dt = max(0.0, min(1.0, now - st["last_tick"])); st["last_tick"] = now
        for w in list(wins):
            if Kit.was_clicked(w["store"], "close"):
                if w["id"] == 0: Kit.dispose(w["g"]); return
                queue.add(("closed", w["id"]), dup=True)
        while st["queue"]:
            action = st["queue"].pop(0); kind = action[0]
            w = (next((x for x in wins if x["id"] == action[1]), None)
                 if len(action) > 1 and isinstance(action[1], int) and kind != "follow" else None)
            if w is not None or kind in FREE_KINDS: ACTIONS[kind](action, w)
        if st["redraw_wait"] and not drag_busy():
            ids, st["redraw_wait"] = st["redraw_wait"], set()
            for w in list(wins):
                if w["id"] in ids: build_window(w)
            save_windows()
        for w in wins:
            if w["resize_at"] and now - w["resize_at"] >= RESIZE_SETTLE and not drag_busy():
                w["resize_at"] = 0.0; apply_resize(w)
        if now >= st.get("next_zone", 0.0): st["next_zone"] = now + ZONE_EVERY; check_zones()
        try: s = sample()
        except Exception as ex:
            s = None; msg = str(ex)[:120]
            if msg != st.get("err"): st["err"] = msg; say("couldn't read the client (%s)." % msg, Kit.HUE_BAD)
        read_journal(now)
        if s: process(s, now)
        if st["died"]: st["died"] = False; own_death(now)
        track_place(now, dt)
        if st["recap_show"]: st["recap_show"] = False; build_recap()
        if data["cur"] is not None:
            data["cur"]["combat"] += dt; data["overall"]["combat"] += dt
            if not 0.0 <= now - data["last_combat"] <= settings["idle"]: close_fight(now); st["next_ui"] = 0.0
        if now >= st["next_ui"] or (st["changed"] and st["next_ui"] - now <= UI_EVERY - UI_SOON):
            st["next_ui"] = now + UI_EVERY; st["changed"] = False
            for w in wins:
                if not w["docked"]: refresh(w)
    def _thread_tick():
        while jobs and not st["shutting"]: jobs.pop(0)()
        if st["to_write"]: write_files()
    def _thread_wanted(): return bool(jobs) or bool(st["to_write"])
    def _stop():
        st["shutting"], st["active"], st["jr"] = True, False, None; del jobs[:]; save_windows(); save_settings()
        cleanup.close()
        for w in list(wins): close_window(w, False)
    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
            "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed,
            "thread_tick": _thread_tick, "thread_wanted": _thread_wanted}


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("meters", "Meters", "Damage, healing, loot and gold meters", _module_meters, 0.25, category="Extras")
