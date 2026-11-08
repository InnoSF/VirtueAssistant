def _module_social():
    KEY = "social"; TITLE = "Social"; SETTINGS_KEY = "Social_settings"; POS_KEY = "Social_pos"; MIN_KEY = "Social_min"
    NAMES_KEY = "Social_names"; GUILD_KEY = "Social_guild"; ROSTER_KEY = "Social_roster"; TRAY_ICON = 0x1F14; W = 460
    GUILD_W = 600; MINI_W, MINI_H = 240, 46; ROW_H = 24; ROWS_MIN, ROWS_MAX = 4, 16; DEFAULT_ROWS = 8
    TABS = [("friends", "Friends"), ("party", "Party"), ("guild", "Guild"), ("profile", "Profile")]
    TAB_TIPS = {"friends": "Show TazUO's friends list and their health",
                "party": "Show your party: members, invites, loot and chat",
                "guild": "Show your guild: info, roster and chat",
                "profile": "Show your character and the client's windows"}
    SOCIAL_AGO = ((60, 1, "just now"), (3600, 60, "%d min ago"), (86400, 3600, "%d h ago"),
                  (172800, 86400, "%d day ago"), (0, 86400, "%d days ago"))
    LIST_EVERY = 0.25; FRIENDS_EVERY = 2.0; PROFILE_EVERY = 1.0; PICK_TIMEOUT = 15; GUMP_WAIT = 4.0
    DIPLOMACY_LABEL = "Diplomacy"; DIPLOMACY_BUTTON = 3; DIPLOMACY_BUTTON_MAX = 9999; NAME_W = 150; STATUS_W = 90
    RANK_W = 64; MSG_W_MIN = 120; DUMP_CHARS = 200; INFO_TAB, ROSTER_TAB = "My Guild", "Guild Roster"
    INFO_BUTTON, ROSTER_BUTTON = 1, 2; FORWARD_BUTTON = 7; ROSTER_PAGES_MAX = 40; ROSTER_KEEP = 300; GUILD_EVERY_MIN = 5
    GUILD_EVERY_MAX = 120; GUILD_RETRY = 60; GUILD_RETRY_MAX = 600; NOT_GUILDED_CLILOCS = (1062939, 1062940, 1063035)
    NOT_GUILDED = ("not a member of any guild", "abbreviation:")
    CLILOCS = {1062954: "Guild Name", 1063025: "Alliance", 1063084: "Guild Faction",
               1062955: "Name", 1062956: "Rank", 1062952: "Last On",
               1062953: "Guild Title", 1063015: "Online", 1062959: "Leader",
               1062960: "Warlord", 1062961: "Emissary", 1062962: "Member",
               1062963: "Ronin", 1062974: ROSTER_TAB, 1063014: INFO_TAB,
               1062978: DIPLOMACY_LABEL, 1062992: "Invite Player", 3006115: "Resign"}
    TAB_CLILOCS = (1063014, 1062974, 1062978); TAB_MARKS = ("1063014", "1062974", "1062978")
    TAB_CAPS_LOW = (INFO_TAB.lower(), ROSTER_TAB.lower(), DIPLOMACY_LABEL.lower())
    NOTO_NAMES = ("Unknown", "Innocent", "Ally", "Gray", "Criminal", "Enemy", "Murderer", "Invulnerable")
    FS, RS = "\x1f", "\x1e"; PF, PR, ESC = "|", ";", "~"; NOTES_KEY = "Social_notes"; NOTES_MAX = 500; NOTE_CHARS = 200
    NOTE_POS_KEY = "Social_note_pos"; NOTE_W = 440
    SORTS = [("online", "Sort: online", "Online"), ("laston", "Sort: last on", "Last on"),
             ("rank", "Sort: rank", "Rank"), ("name", "Sort: name", "Name")]
    SORT_CODES = [x[0] for x in SORTS]
    RANK_ORDER = (("leader", "guild leader"), ("warlord",), ("emissary",), ("member",), ("ronin",))
    DATE_RE = re.compile(r"(\d{1,4})\s*([-/.])\s*(\d{1,2})\s*[-/.]\s*(\d{1,4})")
    settings = {"tab": "friends", "rows": DEFAULT_ROWS, "bars": True, "announce": True,
                "gevery": GUILD_EVERY_MIN, "ghide": True, "dbutton": DIPLOMACY_BUTTON, "left": False, "gsort": "online"}
    st = {"shutting": False, "minimized": False, "docked": False, "friends": [], "names_dirty": False, "party": None,
          "profile": None, "msg": {}, "gids": {}, "me_s": 0, "fserials": []}
    win = {"g": None}; cleanup = Kit.Cleanup(); jobs = []; NOTES = {}; notes_st = {"dirty": False, "ver": 0}
    ed = {"g": None, "c": {}, "store": ({}, {}), "name": ""}; M = Kit.MARGIN; tell = Kit.sayer(TITLE)
    def load_settings():
        p = Kit.get_var(SETTINGS_KEY).split("|")
        def num(i, lo, hi, dflt):
            try: return max(lo, min(hi, int(p[i])))
            except Exception: return dflt
        if len(p) >= 4:
            if p[0] in TAB_TIPS: settings["tab"] = p[0]
            settings.update({"rows": num(1, ROWS_MIN, ROWS_MAX, DEFAULT_ROWS), "bars": p[2] == "1",
                             "announce": p[3] == "1"})
        if len(p) >= 6: settings.update({"gevery": num(4, 0, GUILD_EVERY_MAX, GUILD_EVERY_MIN), "ghide": p[5] == "1"})
        if len(p) >= 8:
            settings.update({"dbutton": num(6, 0, DIPLOMACY_BUTTON_MAX, DIPLOMACY_BUTTON), "left": p[7] == "1"})
        if len(p) >= 9 and p[8] in SORT_CODES: settings["gsort"] = p[8]
        names = {}
        for part in Kit.get_var(NAMES_KEY).split("|"):
            if "=" in part:
                s, n = part.split("=", 1)
                try: names[int(s)] = n
                except Exception: pass
        st["names"] = names; load_guild(); load_notes()
    def save_settings():
        Kit.put_var(SETTINGS_KEY, "|".join([str(int(settings[k])) if isinstance(settings[k], bool) else str(settings[k])
                                            for k in ("tab", "rows", "bars", "announce", "gevery", "ghide", "dbutton",
                                                      "left", "gsort")]))
    def save_names():
        if not st["names_dirty"]: return
        st["names_dirty"] = False; items = sorted(st["names"].items())[-200:]
        Kit.put_var(NAMES_KEY, "|".join("%d=%s" % (s, n.replace("|", "/").replace("=", "-")) for s, n in items))
    def empty_guild():
        return {"ok": False, "in_guild": True, "name": "", "alliance": "", "faction": "",
                "charter": "", "website": "", "members": [], "at": 0.0, "note": ""}
    def clean(s):
        s = str(s or "").replace(FS, " ").replace(RS, " ").replace("\n", " ").strip()
        return s.replace(ESC, ESC + "t").replace(PF, ESC + "p").replace(PR, ESC + "s")
    def unclean(s): return str(s or "").replace(ESC + "p", PF).replace(ESC + "s", PR).replace(ESC + "t", ESC)
    def split_saved(raw, old_sep, new_sep):
        if FS in raw or RS in raw: return raw.split(old_sep)
        return [unclean(p) for p in raw.split(new_sep)]
    def load_guild():
        gd = empty_guild(); head = split_saved(Kit.get_var(GUILD_KEY), FS, PF)
        if len(head) >= 7:
            gd["name"], gd["alliance"], gd["faction"], gd["charter"], gd["website"] = head[:5]
            try: gd["at"] = float(head[5])
            except Exception: gd["at"] = 0.0
            gd["in_guild"] = head[6] != "0"; gd["ok"] = gd["at"] > 0
        members = []; raw = Kit.get_var(ROSTER_KEY)
        for rec in raw.split(RS if FS in raw or RS in raw else PR):
            f = split_saved(rec, FS, PF)
            if len(f) >= 5 and f[0]:
                members.append({"name": f[0], "rank": f[1], "laston": f[2], "title": f[3],
                                "online": f[4] == "1", "me": False})
        gd["members"] = members; st["guild"] = gd
    def save_guild():
        gd = st["guild"] or empty_guild()
        Kit.put_var(GUILD_KEY, PF.join([clean(gd[k]) for k in ("name", "alliance", "faction", "charter", "website")]
                                       + ["%d" % int(gd["at"] or 0), "1" if gd["in_guild"] else "0"]))
        Kit.put_var(ROSTER_KEY, PR.join(PF.join([clean(m[k]) for k in ("name", "rank", "laston", "title")]
                                                + ["1" if m["online"] else "0"]) for m in gd["members"][:ROSTER_KEEP]))
    def load_notes():
        try: raw = str(API.GetPersistentVar(NOTES_KEY, "", API.PersistentVar.Account) or "")
        except Exception: raw = ""
        NOTES.clear(); notes_st["ver"] += 1
        for rec in raw.split(PR):
            f = [unclean(x).strip() for x in rec.split(PF)]
            if len(f) >= 2 and f[0] and f[1] and len(NOTES) < NOTES_MAX: NOTES[f[0].lower()] = (f[0], f[1])
    def save_notes():
        if not notes_st["dirty"]: return
        notes_st["dirty"] = False
        data = PR.join(PF.join([clean(n), clean(t)]) for n, t in sorted(NOTES.values(), key=lambda e: e[0].lower()))
        try: API.SavePersistentVar(NOTES_KEY, data, API.PersistentVar.Account)
        except Exception: pass
    def note_of(player_name): e = NOTES.get(str(player_name or "").strip().lower()); return e[1] if e else ""
    def notes_changed(): notes_st["dirty"] = True; notes_st["ver"] += 1; jobs.append(save_notes)
    def set_note(name, text):
        name = " ".join(str(name or "").split()); text = " ".join(str(text or "").split())[:NOTE_CHARS]
        if not name: tell("type a name first."); return False
        k = name.lower()
        if not text:
            if NOTES.pop(k, None) is not None: tell("note on %s deleted." % name); notes_changed()
            return True
        if k not in NOTES and len(NOTES) >= NOTES_MAX:
            tell("at most %d notes; delete one first." % NOTES_MAX, Kit.HUE_BAD); return False
        NOTES[k] = (name, text); notes_changed(); tell("note on %s saved." % name, Kit.HUE_GOOD); return True
    fit = Kit.fit
    def shift_held(): return bool(Client.key_held("shift"))
    def set_vis(part, on):
        if part[0] is not None and part[1] != on: part[1] = on; Kit.set(part[0], "IsVisible", on)
    def noto_name(n):
        if n is None: return ""
        try: i = int(n)
        except Exception: i = -1
        return NOTO_NAMES[i] if 0 <= i < 8 else str(n).split(".")[-1]
    def player_serial():
        s = st["me_s"]
        if not s:
            try: s = int(API.Player.Serial or 0)
            except Exception: s = 0
            st["me_s"] = s
        return s
    def player_name():
        prof = st["profile"]
        if prof and prof[0]: return prof[0]
        try: return str(API.Player.Name or "")
        except Exception: return ""
    def ago(t): return "never" if not t else Kit.ago(time.time() - t, SOCIAL_AGO)
    class CL(object):
        looked = False; error = ""; world = None; GA = None; UIM = None; FLM = None
        @staticmethod
        def _flags(static):
            from System.Reflection import BindingFlags
            return (BindingFlags.Public | BindingFlags.NonPublic |
                    (BindingFlags.Static if static else BindingFlags.Instance))
        _methods = {}
        @staticmethod
        def call(obj, name, args=(), t=None):
            t = t if t is not None else obj.GetType(); args = list(args); key = (t, name, len(args), obj is None)
            e = CL._methods.get(key, False)
            if e is False:
                m = None; flags = CL._flags(obj is None); tt = t
                while tt is not None and m is None:
                    for mm in tt.GetMethods(flags):
                        if mm.Name != name or mm.IsGenericMethodDefinition: continue
                        ps = mm.GetParameters()
                        if len(ps) >= len(args) and all(p.IsOptional for p in ps[len(args):]): m = mm; break
                    tt = tt.BaseType
                e = (None if m is None else (m, [p.DefaultValue for p in m.GetParameters()[len(args):]]))
                CL._methods[key] = e
            if e is None: raise Exception("can't call %s.%s" % (t.Name, name))
            import System; return e[0].Invoke(obj, System.Array[object](args + e[1]))
        @staticmethod
        def find():
            if CL.looked: return
            CL.looked = True
            try: asm = API.GetType().Assembly
            except Exception as ex: CL.error = "no client access (%s)" % ex; return
            world = Typing._get(API, "World")
            if world is None:
                game = Typing._get(None, "Game", Client._type("ClassicUO.Client"))
                world = Typing._get(Typing._get(game, "UO"), "World")
            CL.world = world; CL.GA = Client._type("ClassicUO.Game.GameActions")
            CL.UIM = Client._type("ClassicUO.Game.Managers.UIManager")
            CL.FLM = Client._type("ClassicUO.Game.Managers.FriendsListManager")
            if world is None: CL.error = "client World not found"
            elif CL.GA is None: CL.error = "GameActions not found"
        @staticmethod
        def on_main(fn):
            how, value = Client.on_main_ex(fn)
            if how == "ok": return value
            CL.error = Client.error or "can't run on the client thread"; return None
        @staticmethod
        def game_action(name, args=(), with_world=True):
            if CL.GA is None: return False
            full = ([CL.world] if with_world else []) + list(args)
            def run(): CL.call(None, name, full, CL.GA); return True
            return bool(CL.on_main(run))
        @staticmethod
        def friends():
            if CL.FLM is None: return None
            def run():
                inst = Typing._get(None, "Instance", CL.FLM)
                if inst is None: return None
                out = []
                for f in (CL.call(inst, "GetFriends") or []):
                    ft = f.GetType()
                    out.append((int(Typing._get(f, "Serial", ft) or 0), str(Typing._get(f, "Name", ft) or "")))
                return out
            return CL.on_main(run)
        @staticmethod
        def party():
            world = CL.world
            if world is None: return None
            def run():
                party = Typing._get(world, "Party")
                if party is None: return None
                leader = int(Typing._get(party, "Leader") or 0); inviter = int(Typing._get(party, "Inviter") or 0)
                loot = bool(Typing._get(party, "CanLoot") or False); pl = Typing._get(world, "Player")
                me = int(Typing._get(pl, "Serial") or 0) if pl is not None else 0; members = []
                for m in (Typing._get(party, "Members") or []):
                    if m is not None:
                        s = int(Typing._get(m, "Serial") or 0)
                        if s and s != me: members.append(s)
                return (leader, inviter, loot, members)
            return CL.on_main(run)
        @staticmethod
        def open_ignore_list():
            if CL.world is None or CL.UIM is None: return False
            def run():
                import System
                if CL.bring_to_front("IgnoreManagerGump"): return True
                t = Client._type("ClassicUO.Game.UI.Gumps.IgnoreManagerGump")
                if t is None: raise Exception("IgnoreManagerGump not found")
                g = System.Activator.CreateInstance(t, System.Array[object]([CL.world]))
                CL.call(None, "Add", [g], CL.UIM); return True
            return bool(CL.on_main(run))
        @staticmethod
        def bring_to_front(type_name):
            for g in Typing._get(None, "Gumps", CL.UIM) or ():
                if g is not None and g.GetType().Name == type_name and not g.IsDisposed:
                    CL.call(g, "BringOnTop"); return True
            return False
        @staticmethod
        def find_server_gump(test):
            if CL.UIM is None: return 0, ""
            def run():
                for g in Typing._get(None, "Gumps", CL.UIM) or ():
                    if g is None or g.IsDisposed: continue
                    try:
                        raw = Typing._get(g, "PacketGumpText")
                        if not raw: continue
                        raw = str(raw)
                        if test(raw): return int(Typing._get(g, "ServerSerial") or 0), raw
                    except Exception: continue
                return 0, ""
            r = CL.on_main(run); return r if r else (0, "")
        @staticmethod
        def press_labelled(gump, label):
            inner = safe(lambda: gump.Gump); gump = inner if inner is not None else gump; want = label.lower().strip()
            def run():
                import System; exact, texts, buttons = [], [], []
                def at(ch):
                    x = int(Typing._get(ch, "ScreenCoordinateX") or 0)
                    return x, int(Typing._get(ch, "ScreenCoordinateY") or 0)
                def walk(ctrl):
                    for ch in list(Typing._get(ctrl, "Children") or []):
                        if ch is None: continue
                        tn = ch.GetType().Name
                        if tn == "Button": buttons.append(at(ch) + (int(Typing._get(ch, "ButtonID") or 0),))
                        else:
                            txt = Typing._get(ch, "Text"); low = Kit.strip_html(txt).lower() if txt else ""
                            if low and want in low: (exact if low == want else texts).append(at(ch))
                        walk(ch)
                walk(gump); texts = exact or texts
                if not texts or not buttons: return False
                tx, ty = texts[0]
                def off(b): return abs(b[0] - tx) + abs(b[1] - ty)
                best = min(buttons, key=off)
                if off(best) > 80: return False
                CL.call(gump, "OnButtonClick", [System.Int32(best[2])]); return True
            return bool(CL.on_main(run))
    def read_mobile(serial):
        m = HOST.mobile(serial)
        if m is None: return None
        try: return (str(m.Name or ""), int(m.Hits or 0), int(m.HitsMax or 0), int(m.Distance), bool(m.IsDead), True)
        except Exception: return None
    def full_mob(serial):
        mobs = st["mobs"]; d = mobs.get(serial)
        if d is not None and d[5] is None:
            d = read_mobile(serial)
            if d is None: mobs.pop(serial, None)
            else: mobs[serial] = d
        return d
    def read_friends():
        now = time.time()
        if now < st["next_friends"]: return
        st["next_friends"] = now + FRIENDS_EVERY; lst = CL.friends(); named = lst is not None
        if lst is None: lst = [(int(s), st["names"].get(int(s), "")) for s in API.GetAllFriends() or ()]
        me = player_serial(); raw_key = (me, lst) if named else None
        if raw_key is not None and raw_key == st["friends_raw"]:
            if st["names_dirty"]: jobs.append(save_names)
            return
        out = []; unnamed = False
        for serial, name in lst:
            if serial == me or not serial: continue
            if not name:
                unnamed = True; d = st["mobs"].get(serial)
                name = (d[0] if d and d[0] else "") or st["names"].get(serial, "")
            if name and st["names"].get(serial) != name: st["names"][serial] = name; st["names_dirty"] = True
            out.append((serial, name or ("0x%08X" % serial)))
        out.sort(key=lambda e: (e[1].startswith("0x"), e[1].lower())); st["friends"] = out
        st["fserials"] = [s for s, _n in out]; st["friends_raw"] = None if unnamed else raw_key
        if st["names_dirty"]: jobs.append(save_names)
    def read_party():
        p = CL.party()
        if p is None:
            leader = int(API.GetPartyLeader() or 0)
            p = (leader, 0, False, [int(s) for s in API.GetPartyMemberSerials() or ()]) if leader else None
        st["party"] = p
    def in_party(p): return bool(p) and bool(p[0] or p[3])
    def read_profile(full=True):
        now = time.time()
        if now < st["next_profile"] and not (full and st["prof_part"]): return
        st["next_profile"] = now + PROFILE_EVERY; p = HOST.me()
        if p is None: st["profile"] = None; st["prof_part"] = False; return
        try:
            name = str(p.Name or "")
            try: nap = p.raw.NameAndProps(False)
            except Exception: nap = ""
            lines = [l.strip() for l in str(nap or "").replace("\r", "").split("\n") if l.strip()]
            if not full:
                old = st["profile"]; rest = old[2:] if old else ("", 0, 0, 0, 0, 0, False, False)
                st["profile"] = (name, lines) + tuple(rest); st["prof_part"] = True; return
            prof = (name, lines, noto_name(p.Notoriety), int(p.Gold or 0), int(p.Followers or 0),
                    int(p.FollowersMax or 0), int(p.Weight or 0), int(p.WeightMax or 0), bool(p.InWarMode),
                    bool(p.IsHidden))
        except Exception: prof = None
        st["profile"] = prof; st["prof_part"] = False
    def scan_view():
        me = player_serial(); view, allies, serials, kept = {}, [], set(), {}
        for m in HOST.mobiles():
            try:
                s = int(m.Serial)
                if not s or s == me: continue
                serials.add(s)
                if not (m.IsHuman or m.IsGargoyle): continue
                n = m.Notoriety; ni = int(n) if n is not None else -1
                if ni == 7: continue
                name = str(m.Name or "")
                if name: view[name.lower()] = s
                if ni == 2: allies.append((s, name))
                kept[s] = (name, int(m.Distance))
            except Exception: continue
        st["view"], st["allies"], st["view_serials"], st["kept"] = view, allies, serials, kept
    def friends_in_view(serials):
        known = st["view_serials"]
        if known is None and len(serials) > FRIENDS_SCAN:
            try: known = {int(m.Serial) for m in HOST.mobiles()}
            except Exception: known = None
        if known is not None: return known.intersection(serials)
        return {s for s in serials if s and HOST.mobile(s) is not None}
    FRIENDS_SCAN = 10
    def last_two(fn):
        slots = [None, None]
        def run(raw):
            for e in slots:
                if e is not None and (e[0] is raw or e[0] == raw): return e[1]
            out = fn(raw); slots[1] = slots[0]; slots[0] = (raw, out); return out
        return run
    @last_two
    def gump_cells(raw): return Kit.gump_cells(raw, CLILOCS)
    @last_two
    def classify(raw):
        cells = gump_cells(raw)[0]
        if not cells: return None
        texts = [c["text"].lower() for c in cells]; clilocs = [c["cliloc"] for c in cells]
        if any(cl in TAB_CLILOCS for cl in clilocs) or ROSTER_TAB.lower() in texts:
            if (1062955 in clilocs and 1062956 in clilocs) or ("rank" in texts and (
                    "last on" in texts or "name" in texts)):
                return "roster"
            return "guild"
        joined = "\x00".join(texts)
        if any(cl in NOT_GUILDED_CLILOCS for cl in clilocs) or any(w in joined for w in NOT_GUILDED): return "noguild"
    def may_be_guild(raw): return any(t in raw for t in TAB_MARKS) or "roster" in raw.lower()
    def bands(cells, tol=6):
        out = []
        for c in sorted(cells, key=lambda c: (c["y"], c["x"])):
            if out and abs(c["y"] - out[-1][0]) <= tol: out[-1][1].append(c)
            else: out.append([c["y"], [c]])
        return [sorted(row, key=lambda c: c["x"]) for _, row in out]
    def parse_info(raw):
        cells, _ = gump_cells(raw); cells = [c for c in cells if c["cliloc"] not in TAB_CLILOCS]
        def right_of(cliloc):
            label = CLILOCS[cliloc].lower()
            lab = next((c for c in cells if c["cliloc"] == cliloc or c["text"].lower() == label), None)
            if lab is None: return ""
            near = [c for c in cells if abs(c["y"] - lab["y"]) <= 6 and c["x"] > lab["x"]]
            return min(near, key=lambda c: c["x"])["text"] if near else ""
        out = {"name": right_of(1062954), "alliance": right_of(1063025), "faction": right_of(1063084),
               "charter": "", "website": ""}
        wide = sorted([c for c in cells if c["w"] >= 300 and c["bg"]], key=lambda c: c["y"])
        if wide: out["charter"] = wide[0]["text"]
        if len(wide) > 1: out["website"] = wide[1]["text"]
        for k in ("charter", "website"):
            if "not yet set" in out[k].lower(): out[k] = ""
        return out
    def parse_roster(raw):
        cells, buttons = gump_cells(raw)
        cells = [c for c in cells if c["cliloc"] not in TAB_CLILOCS and c["text"].lower() not in TAB_CAPS_LOW]
        rows = bands(cells); header = None
        for row in rows:
            texts = [c["text"].lower() for c in row]
            if len(row) >= 3 and ("name" in texts or "rank" in texts or "last on" in texts
                                  or any(c["cliloc"] in (1062955, 1062956, 1062952, 1062953) for c in row)):
                header = row; break
        if header is None: return [], False
        cols = [c["x"] for c in header]; names = [c["text"].lower() for c in header]; idx = {}
        for want, keys in (("name", ("name",)), ("rank", ("rank",)),
                           ("laston", ("last on", "online")), ("title", ("title",))):
            for i, n in enumerate(names):
                if any(k in n for k in keys) and i not in idx.values(): idx[want] = i; break
        if "name" not in idx: idx["name"] = 0
        members = []; hy = header[0]["y"]
        for row in rows:
            if row[0]["y"] <= hy + 10: continue
            got = {}
            for c in row:
                best, bd = -1, 1e9
                for i, cx in enumerate(cols):
                    d = abs(c["x"] - cx)
                    if d < bd: best, bd = i, d
                if bd <= 30 and best not in got: got[best] = c
            if len(got) < 2 or idx["name"] not in got: continue
            nc = got[idx["name"]]; name = nc["text"]
            if name.endswith(" *"): name = name[:-2]
            name = name.strip()
            if name.endswith(" VvV"): name = name[:-4].strip()
            if not name: continue
            raw_name = nc["raw"].lower()
            col = [got[idx[k]]["text"] if k in idx and idx[k] in got else "" for k in ("rank", "laston", "title")]
            online = col[1].lower() == "online" or "#000066" in raw_name or "#006600" in raw_name
            members.append({"name": name, "rank": col[0], "laston": col[1], "title": col[2], "online": online,
                            "me": "#006600" in raw_name})
        more = any(b[2] == FORWARD_BUTTON for b in buttons); return members, more
    def _last_gump_run():
        gid = int(API.HasGump() or 0)
        if not gid: return 0, ""
        try: return gid, str(API.GetGump(gid).PacketGumpText or "")
        except Exception: return gid, ""
    def last_gump(): return safe(lambda: Kit.on_client(_last_gump_run)) or (0, "")
    def guild_test(raw): return may_be_guild(raw) and classify(raw) in ("guild", "roster")
    def hide_next(gid=0):
        if not settings["ghide"]: return
        if gid: API.ConfigNextGump(serial=gid, isVisible=False)
        else: st["hid_any"] = True; API.ConfigNextGump(isVisible=False)
    def reset_hide(): st["hid_any"] = False; API.ConfigNextGump()
    def unknown_gump(had):
        gid, raw = last_gump()
        if not gid or gid == had: return "the guild window didn't come"
        dump = " ".join(raw.split())[:DUMP_CHARS] if raw else "(empty layout)"
        if st["hid_any"]: API.CloseGump(gid); st["hid_any"] = False; what = "closed again"
        else: what = "left open"
        tell("gump 0x%08X came instead of the guild window (%s); it begins: %s." % (gid, what, dump))
        return "the guild window didn't come (another gump did)"
    def wait_gump(check):
        deadline = time.time() + GUMP_WAIT
        while time.time() < deadline and not st["shutting"]:
            gid, raw = last_gump(); r = gid and raw and check(raw)
            if r: return gid, raw, r
            if not HOST.idle(0.15): break
        return 0, "", None
    def press(gid, label, button):
        gump = safe(lambda: API.GetGump(gid))
        if gump is not None and CL.press_labelled(Kit.client_control(gump) or gump, label): return True
        return bool(button) and bool(API.ReplyGump(button, gid))
    def guild_job():
        st["guild_busy"] = True; st["guild_pages"] = 0; old = st["guild"] or empty_guild(); gd = old
        try: gd = read_guild_window(old)
        except Exception as ex: gd = empty_guild(); gd["note"] = "couldn't read the guild window (%s)" % ex
        finally:
            with Kit.quiet: reset_hide()
            hid = st.get("ghid", 0); st["ghid"] = 0
            if hid:
                with Kit.quiet: API.CloseGump(hid)
            failed = not gd["ok"]
            if failed:
                note, gd = gd["note"], dict(old); gd["note"] = note; st["guild_fails"] = min(st["guild_fails"] + 1, 10)
                st["guild_next"] = time.time() + min(GUILD_RETRY_MAX, GUILD_RETRY * (2 ** (st["guild_fails"] - 1)))
            else: st["guild_fails"] = 0; st["guild_said"] = ""
            st["guild"] = gd; st["guild_busy"] = False; st["guild_dirty"] = True
            if gd["ok"] and not failed: save_guild()
        if gd["note"]:
            if not failed: tell("%s." % gd["note"])
            elif gd["note"] != st["guild_said"]:
                st["guild_said"] = gd["note"]; again = ""
                if settings["gevery"] and settings["tab"] == "guild":
                    again = " (retry in %d min)" % max(1, int((st["guild_next"] - time.time()) / 60 + 0.5))
                tell("%s%s." % (gd["note"], again), Kit.HUE_BAD)
    def read_guild_window(old):
        gd = empty_guild(); gd["members"] = list(old["members"]); gids = st["gids"]
        def fail(note, stamp=False):
            gd["note"] = note
            if stamp: gd.update({"ok": True, "at": time.time()})
            return gd
        had, had_raw = last_gump(); had_kind = classify(had_raw) if had_raw else None
        had_open = had_kind in ("guild", "roster")
        if not had_open:
            og, oraw = CL.find_server_gump(guild_test)
            if og: had, had_raw, had_kind, had_open = og, oraw, classify(oraw), True
        if had_open: gid, raw, kind = had, had_raw, had_kind
        else:
            hide_next(gids.get("info", 0) if old.get("in_guild", True) else 0)
            if not CL.game_action("OpenGuildGump"): return fail("couldn't ask for the guild window (%s)" % CL.error)
            gid, raw, kind = wait_gump(classify)
            if not gid: return fail(unknown_gump(had))
            st["ghid"] = gid
        if kind == "noguild":
            API.CloseGump(gid); st["ghid"] = 0
            gd.update({"ok": True, "in_guild": False, "members": [], "at": time.time()}); return gd
        if kind == "roster":
            gids["roster"] = gid
            if not had_open: hide_next(gids.get("info", 0))
            press(gid, INFO_TAB, INFO_BUTTON); gid, raw, kind = wait_gump(lambda r: classify(r) == "guild" and "guild")
            if not gid: return fail("the My Guild page didn't come")
            if not had_open: st["ghid"] = gid
        info = parse_info(raw)
        if had_open and not info.get("name"):
            prev = raw; press(gid, INFO_TAB, INFO_BUTTON)
            gid, raw, kind = wait_gump(lambda r2: classify(r2) == "guild" and r2 != prev and "guild")
            if not gid: return fail("the My Guild page didn't come")
            info = parse_info(raw)
        gids["info"] = gid; gd.update(info)
        if not had_open: hide_next(gids.get("roster", 0))
        if not press(gid, ROSTER_TAB, ROSTER_BUTTON): return fail("couldn't open the Guild Roster page", True)
        gid, raw, kind = wait_gump(lambda r: classify(r) == "roster" and "roster")
        if not gid: return fail("the Guild Roster page didn't come", True)
        if not had_open: st["ghid"] = gid
        gids["roster"] = gid; members, seen, pages, whole = [], {}, 0, False
        while not st["shutting"]:
            got, more = parse_roster(raw); pages += 1; st["guild_pages"] = pages
            for m in got:
                k = m["name"].lower()
                if k not in seen: seen[k] = True; members.append(m)
            if not more or pages >= ROSTER_PAGES_MAX: whole = True; break
            if not had_open: hide_next(gid)
            if not API.ReplyGump(FORWARD_BUTTON, gid): break
            prev = raw; gid2, raw2, _ = wait_gump(lambda r2: classify(r2) == "roster" and r2 != prev and "ok")
            if not gid2: break
            gid, raw = gid2, raw2
            if not had_open: st["ghid"] = gid
        if not whole or not members:
            for m in old["members"]:
                k = m["name"].lower()
                if k not in seen:
                    seen[k] = True; c = dict((k2, v2) for k2, v2 in m.items() if not k2.startswith("_"))
                    c["online"] = False; members.append(c)
            if not whole and pages: gd["note"] = "read %s only; rest as before" % Kit.count(pages, "roster page")
        gd["members"] = members; gd.update({"ok": True, "at": time.time()})
        if had_open: press(gid, INFO_TAB, INFO_BUTTON)
        else: API.CloseGump(gid); st["ghid"] = 0
        return gd
    queue = Kit.queuer(st)
    def win_w(tab): return GUILD_W if tab == "guild" else W
    def layout_fit(fw, fh, mode):
        new = (int(fw), int(fh)) if (fw is not None and fh is not None) else None
        if new != st.get("fit"): st["fit"] = new; queue("redraw")()
        elif mode == "again" and new is not None:
            sig = (new, settings["tab"], st["minimized"], settings["rows"], settings["bars"]); now = time.time()
            if sig != st["again_for"] or not 0 <= now - st.get("again_at", 0.0) < 5.0:
                st.update({"again_for": sig, "again_at": now, "again_build": True}); queue("redraw")()
    def min_title_w(): return max(160, M + 30 + Kit.text_w(TITLE.upper()) + 6 + 94 + M)
    def min_w(): return (M + 30 + Kit.text_w(TITLE.upper()) + 16 + 84 + Kit.DOCK_DX + 35 + Kit.text_w("Settings") + M)
    def tab_lines(iw):
        out, tx, line = [], 10, 0
        for key, cap in TABS:
            bw = 35 + Kit.text_w(cap)
            if tx > 10 and tx + bw > iw - 4: tx, line = 10, line + 1
            out.append((key, cap, tx, line)); tx += bw + 14
        return out, line + 1
    def tab_layout(tab):
        info, bars = {"friends": (1, 1), "party": (2, 3), "guild": (6, 2)}.get(tab, (7, 2))
        return info, bars, settings["rows"] if info < 7 else 0
    def window_h(tab):
        info, bars, rows = tab_layout(tab)
        body = (8 + info * 22 + (8 if info else 0) + bars * 30 + rows * ROW_H + (8 if rows else 0) + 4)
        return M + 30 + Kit.GAP + 30 + Kit.GAP + body + M
    def min_size():
        return (min_title_w(), max(window_h(t) - max(0, tab_layout(t)[2] - 1) * ROW_H for t, _c in TABS) + 30)
    def build_window():
        tab = settings["tab"]; g, store, c = wnd.begin(win_w(tab), window_h(tab)); w, h = wnd.w, wnd.h; rows = []
        win["info_tips"], win["info_in"] = {}, {}
        if st["again_build"]: st["again_build"] = False
        else: st["again_for"] = None
        if not st["minimized"]:
            fit = st.get("fit")
            if fit is not None: w, h = max(min_title_w(), fit[0]), fit[1]
            IW = w - 2 * M; c["iw"] = IW; wnd.frame(g, w, h, settings=w >= min_w())
            yt = M + 30 + Kit.GAP; places, nlines = tab_lines(IW); Kit.add_section(g, M, yt, IW, 30 * nlines)
            for key, cap, tx, line in places:
                Kit.art_button(g, store, "tab_" + key, Kit.ART_PAGE, M + tx, yt + 4 + 30 * line, cap, TAB_TIPS[key],
                               hue=Kit.HUE_TITLE if key == tab else Kit.HUE_TEXT, on_click=queue(("tab", key)))
            yb = yt + 30 * nlines + Kit.GAP
            if fit is None: h += 30 * (nlines - 1)
            bh = h - yb - M; Kit.add_section(g, M, yb, IW, bh)
            build_tab(g, store, c, rows, tab, M, yb, IW, bh, fit is not None)
        wnd.end(g, {"rows": rows, "tab": tab, "info": {}}, w, h); st["rebuild"] = False; refresh()
    wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, mini=(MINI_W, MINI_H), icon=TRAY_ICON,
                     cleanup=cleanup, docked_min=True)
    def build_tab(g, store, c, rows, tab, x, y, w, h, fit=False):
        info, bars, nrows = tab_layout(tab); TOOL_RIGHT[0] = x + w - 6
        def list_rows(yy): return max(1, (y + h - 12 - yy) // ROW_H) if fit else nrows
        c["info"] = [Kit.add_label(g, "", x + 10, y + 8 + 22 * i, Kit.HUE_INFO) for i in range(info)]
        yy = y + 8 + 22 * info + (8 if info else 0)
        if tab == "friends":
            items = [("add", Kit.ART_PLAY, ["Add friend...", None], "Target someone to add to TazUO's friends list"),
                     ("add_last", Kit.ART_OK, ["Add last target", None],
                      "Add your last target to TazUO's friends list")]
            yy = toolbar_paged(g, store, c, x, y, yy, w, items, None)
            add_rows(g, store, c, rows, list_rows(yy), x, yy, w,
                     ROW_TIP % "set as last target (or answer a target cursor)",
                     True, rm_tip="Remove from TazUO's friends list")
        elif tab == "party":
            yy += 30 * toolbar(g, store, c, x, yy, x + w - 6, [
                ("invite", Kit.ART_PLAY, ["Invite...", None], "Target someone to invite to your party"),
                ("leave", Kit.ART_CLOSE, ["Leave", None], "Leave the party"), ("loot", Kit.ART_OK, ["Loot", None],
                 "Allow or forbid party looting of your corpse (the line above shows which)"),
                ("pwin", Kit.ART_PAGE, ["Party window", None], "Open the client's party window")])
            TOOL_RIGHT[0] = x + w - 6 - PAGER_W - 6
            c["accept"] = tool(g, store, x + 10, yy, "accept", Kit.ART_OK, "Accept",
                               "Join the party. Alt+click: auto-follow the inviter (again to stop)",
                               on_click=invite_click("accept"))
            c["decline"] = tool(g, store, c["accept"][1], yy, "decline", Kit.ART_CLOSE, "Decline",
                                "Turn the invitation down. Alt+click: auto-follow the inviter (again to stop)",
                                on_click=invite_click("decline"))
            TOOL_RIGHT[0] = x + w - 6; pager(g, store, c, x + w, yy); yy += 30
            chat(g, store, c, x, yy, w, [("psend", "Send", "Say it in party chat")], "Message for party chat"); yy += 30
            add_rows(g, store, c, rows, list_rows(yy), x, yy, w,
                     ROW_TIP % "set as last target (or answer a target cursor)",
                     True, rm_tip="Remove from the party (leader only)")
        elif tab == "guild":
            items = [("grefresh", Kit.ART_PLAY, ["Refresh", None], "Read the guild window again (info and roster); "
                      + ("it opens hidden" if settings["ghide"] else
                         "it shows while read; Social settings can hide it")),
                     ("gwin", Kit.ART_PAGE, ["Guild window", None], "Open the server's guild menu"),
                     ("diplo", Kit.ART_PAGE, ["Diplomacy", None], "Open the guild window's Diplomacy page"),
                     ("gsort", Kit.ART_PAGE, ["long", "short", None], None)]
            yy = toolbar_paged(g, store, c, x, y, yy, w, items, [3, 2, 1, 0, 3])
            chat(g, store, c, x, yy, w, [("gsend", "Guild", "Say it in guild chat"),
                                         ("asend", "Alliance", "Say it in alliance chat")],
                 "Message for guild or alliance chat")
            yy += 30
            add_rows(g, store, c, rows, list_rows(yy), x, yy, w, ROW_TIP % "set as last target when in view",
                     False, before=[("rank", RANK_W)], after=[("title", 0)])
        else:
            yy += 30 * toolbar(g, store, c, x, yy, x + w - 6, [("edit", Kit.ART_PAGE, ["Edit profile", None],
                 "Open your profile (the server's scroll; closing saves)"),
                ("paperdoll", Kit.ART_PAGE, ["Paperdoll", None], "Open the client's paperdoll"),
                ("status", Kit.ART_PAGE, ["Status", None], "Open the client's status window")])
            toolbar(g, store, c, x, yy, x + w - 6, [
                ("ignore", Kit.ART_PAGE, ["Ignore list", None], "Open TazUO's ignore list (speech you hide)"),
                ("war", Kit.ART_PLAY, ["War / peace", None],
                 "Switch war mode and peace (the last line above shows which)")])
    ROW_TIP = "Click: %s. Shift+click: write a note. Alt+click: auto-follow (again to stop)"; PAGER_W = 100
    def sort_tip(c):
        tip = "Next roster order: online (in view first), last on, rank or name"
        if c.get("gsort_bare"):
            e = SORTS[SORT_CODES.index(settings["gsort"])]; tip = "Roster order: %s. %s" % (e[2].lower(), tip)
        return tip
    def cap_w(key, cap):
        if key == "gsort":
            if cap == "long": return max(Kit.text_w(e[1]) for e in SORTS)
            return max(Kit.text_w(e[2]) for e in SORTS)
        return Kit.text_w(cap)
    def toolbar_plan(items, x, right, order):
        lv = [0] * len(items)
        if order is None: order = list(range(len(items) - 1, -1, -1))
        steps = [None] + list(order)
        for st_i in steps:
            if st_i is not None: lv[st_i] = min(lv[st_i] + 1, len(items[st_i][2]) - 1)
            bx, end = x + 10, x + 10
            for i, it in enumerate(items):
                cap = it[2][lv[i]]
                if cap is None: end, bx = bx + 30, bx + 30
                else: cw = cap_w(it[0], cap); end, bx = bx + 35 + cw, bx + 35 + cw + 12
            if end <= right: return list(lv)
        return None
    def toolbar(g, store, c, x, y, right, items, order=None, plan=None):
        lv = plan or toolbar_plan(items, x, right, order); wrap = lv is None
        if wrap: lv = [len(it[2]) - 1 for it in items]
        bx, line = x + 10, 0
        for i, (key, art, caps, tip) in enumerate(items):
            cap = caps[lv[i]]
            if key == "gsort":
                c["gsort_long"] = cap == "long"; c["gsort_bare"] = cap is None; tip = sort_tip(c)
                cap = None if cap is None else sort_caption(c)
            elif cap is None and caps[0]: tip = Kit.caption_tip(caps[0], tip)
            need = 30 if cap is None else 35 + Kit.text_w(cap)
            if wrap and bx > x + 10 and bx + need > right: bx, line = x + 10, line + 1
            ctrl = Kit.art_button(g, store, key, art, bx, y + 30 * line, cap, tip, on_click=queue(key))
            bx += 30 if cap is None else need + 12
            if key == "gsort": c["gsort"] = ctrl if cap is not None else None; c["gsort_btn"] = store[0].get(key)
        return line + 1
    def toolbar_paged(g, store, c, x, y, yy, w, items, order):
        plan = toolbar_plan(items, x, x + w - 6 - PAGER_W - 6, order)
        full = plan is not None and all(
            it[2][l] is not None and (l == 0 or it[0] == "gsort") for it, l in zip(items, plan))
        if full:
            lines = toolbar(g, store, c, x, yy, x + w - 6 - PAGER_W - 6, items, order, plan)
            pager(g, store, c, x + w, yy)
        else:
            lines = toolbar(g, store, c, x, yy, x + w - 6, items, order); pager(g, store, c, x + w, y + 8 - 6)
            c["info_cut"] = PAGER_W + 6
        return yy + 30 * lines
    TOOL_RIGHT = [100000]
    def tool(g, store, x, y, key, art, cap, tip, on_click=None):
        bare = x + 35 + Kit.text_w(cap) > TOOL_RIGHT[0]
        ctrl = Kit.art_button(g, store, key, art, x, y, None if bare else cap,
                              Kit.caption_tip(cap, tip) if bare else tip, on_click=on_click or queue(key))
        return store[0].get(key), (x + 30 if bare else x + 35 + Kit.text_w(cap) + 12), ctrl
    def invite_click(key):
        def handler(*args):
            p = st["party"]; inv = p[1] if p else 0
            if inv and Follow.alt_held(): queue(("follow", inv))()
            else: queue(key)()
        return handler
    def pager(g, store, c, right, y):
        c["pg"] = Kit.add_label(g, "", right - 100, y + 6, Kit.HUE_INFO)
        Kit.art_button(g, store, "pg_up", Kit.ART_RESTORE, right - 56, y + 4, None, "Previous page",
                       on_click=queue(("page", -1)))
        Kit.art_button(g, store, "pg_dn", Kit.ART_MIN, right - 34, y + 4, None, "Next page",
                       on_click=queue(("page", 1)))
    def chat(g, store, c, x, y, w, buttons, field_tip):
        bw = sum(35 + Kit.text_w(cap) + 12 for _, cap, _ in buttons); fw = w - 20 - bw - 8
        if fw < MSG_W_MIN: fw = max(40, w - 20 - 30 * len(buttons) - 8)
        c["msg"] = Kit.with_tip(Kit.add_textbox(g, st["msg"].get(settings["tab"], ""), x + 10, y + 3, fw,
                                                numbers=False), field_tip)
        bx = x + 10 + fw + 12
        for key, cap, tip in buttons: bx = tool(g, store, bx, y, key, Kit.ART_PLAY, cap, tip)[1]
    def add_rows(g, store, c, rows, n, x, y, w, tip, removable, before=None, after=None, rm_tip="Remove"):
        bw, bh = Kit.pic_size(Kit.LINE_RED); bw, bh = bw or 109, bh or 9; fw, fh = Kit.pic_size(Kit.LINE_BLUE)
        right = x + w - 4 - (40 if removable else 0); before, after = list(before or []), list(after or [])
        dropped = []; bars = settings["bars"]
        def fixed(): return sum(wd + 8 for _k, wd in before) + sum((wd or 40) + 8 for _k, wd in after)
        while right - (x + 10) < fixed() + 8 + 40 + 8 + (30 + 8 if bars else 0) + 44 and (after or before or bars):
            if after: dropped.append(after.pop()[0])
            elif before: dropped.append(before.pop()[0])
            else: bars = False
        name_w, status_w = NAME_W, STATUS_W; room = right - (x + 10) - fixed() - 8
        need = NAME_W + 8 + (bw + 8 if bars else 0) + STATUS_W
        if room < need:
            status_w = max(44, min(STATUS_W, int(room * 0.24)))
            if bars: bw = max(30, min(bw, int(room * 0.30)))
            name_w = max(40, room - status_w - 8 - (bw + 8 if bars else 0))
        c["bar_w"], c["name_w"], c["status_w"] = bw, name_w, status_w
        for i in range(n):
            ry = y + i * ROW_H
            r = {"serial": 0, "prev": (0, 0.0), "parts": [], "name": None, "status": None,
                 "fill": None, "fill_w": -1, "x": None, "red": None, "extra": {}, "who": "", "prev_who": ("", 0.0),
                 "tip0": tip, "tip": tip}
            cx = x + 10; r["name"] = Kit.add_label(g, "", cx, ry + 3); r["parts"].append([r["name"], True])
            cx += name_w + 8
            for key in dropped: r["extra"][key] = (None, 0)
            for key, wd in before:
                lbl = Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO); r["extra"][key] = (lbl, wd)
                r["parts"].append([lbl, True]); cx += wd + 8
            if bars:
                r["red"] = [Kit.add_tiled(g, Kit.LINE_RED, cx, ry + 7, bw, bh), True]; r["parts"].append(r["red"])
                if fw and fh:
                    r["fill"] = Kit.add_tiled(g, Kit.LINE_BLUE, cx, ry + 7, 1, fh); r["fill"].SetWidth(0)
                    r["parts"].append([r["fill"], True])
                cx += bw + 8
            r["status"] = Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO); r["parts"].append([r["status"], True])
            cx += status_w + 8
            for key, wd in after:
                wd = wd or max(40, right - cx); lbl = Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO)
                r["extra"][key] = (lbl, wd); r["parts"].append([lbl, True]); cx += wd + 8
            r["catch"] = Kit.catcher(g, x + 4, ry, w - 8 - (40 if removable else 0), ROW_H, row_click(rows, i), tip)
            r["parts"].append([r["catch"], True])
            if removable:
                r["x"] = Kit.art_button(g, store, "rm%d" % i, Kit.ART_CLOSE, x + w - 42, ry + 1,
                                        None, rm_tip + ". Alt+click: auto-follow (again to stop)",
                                        on_click=rm_click(rows, i))
                r["parts"].append([r["x"], True])
            rows.append(r)
    def recent(r, cur, prev, now): p, at = r[prev]; return p if p and now - at < 0.15 else r[cur]
    def rm_click(rows, i):
        def handler(*args):
            serial = recent(rows[i], "serial", "prev", time.time())
            if serial and Follow.alt_held(): queue(("follow", serial))()
            elif serial: queue(("rm", serial))()
        return handler
    def row_click(rows, i):
        def handler(*args):
            r, now = rows[i], time.time()
            serial, who = recent(r, "serial", "prev", now), recent(r, "who", "prev_who", now)
            if not serial:
                if who and not Follow.alt_held() and shift_held(): queue(("note", who))()
                elif who: queue(("noview", who))()
                return
            if Follow.alt_held(): queue(("follow", serial))()
            elif who and shift_held(): queue(("note", who))()
            else: queue(("click", serial))()
        return handler
    NO_EXTRA = {}
    def shift(r, key, prev, v):
        if r[key] != v: r[prev], r[key] = (r[key], time.time()), v
    def set_row(r, serial, name, status, hue, frac, extra=None, name_hue=None, bar=True, show_x=True):
        ex = extra or NO_EXTRA
        key = (serial, name, status, hue, frac, ex.get("rank"), ex.get("title"), name_hue, bar, show_x, notes_st["ver"])
        if key == r.get("last"): return
        r["last"] = key
        shift(r, "serial", "prev", serial); shift(r, "who", "prev_who", name)
        if name_hue is None: name_hue = Kit.HUE_TEXT if frac is not None else Kit.HUE_INFO
        c = win["c"]; Kit.set_text(r["name"], fit(name, c.get("name_w", NAME_W)), name_hue)
        Kit.set_text(r["status"], fit(status, c.get("status_w", STATUS_W)), hue); cut = []
        for key, (lbl, wd) in r["extra"].items():
            full = str(ex.get(key, "") or ""); short = ""
            if lbl is not None: short = fit(full, wd); Kit.set_text(lbl, short, Kit.HUE_INFO)
            if short != full: cut.append("%s: %s" % (key.capitalize(), full))
        tip = "\n".join([r["tip0"]] + cut)
        if NOTES:
            e = NOTES.get(name.lower())
            if e is not None: tip = tip + "\nNote: " + e[1]
        if tip != r["tip"] and r.get("catch") is not None: r["tip"] = tip; Kit.with_tip(r["catch"], tip)
        w = int(win["c"].get("bar_w", 109) * max(0.0, min(1.0, frac or 0.0)))
        if r["fill"] is not None and w != r["fill_w"]: r["fill_w"] = w; Kit.ui_w(r["fill"], max(1, w))
        xp = r["parts"][-1] if r["x"] is not None else None
        for p in r["parts"]:
            if r["fill"] is not None and p[0] is r["fill"]: set_vis(p, bar and w > 0)
            elif r["red"] is not None and p is r["red"]: set_vis(p, bar)
            elif p is xp: set_vis(p, show_x)
            else: set_vis(p, True)
    def hide_row(r):
        r["last"] = None
        shift(r, "serial", "prev", 0); shift(r, "who", "prev_who", "")
        for p in r["parts"]: set_vis(p, False)
    def mobile_status(serial):
        d = full_mob(serial)
        if d is None: return "away", Kit.HUE_INFO, None
        name, hits, hmax, dist, dead, noto = d
        if dead: return "dead", Kit.HUE_BAD, 0.0
        frac = hits / float(hmax) if hmax > 0 else None
        hue = (Kit.HUE_GOOD if frac is None or frac > 0.5 else (Kit.HUE_TITLE if frac > 0.25 else Kit.HUE_BAD))
        return (Kit.count(dist, "tile")), hue, frac
    def page_of(items):
        n = max(1, len(win["rows"])); pages = max(1, (len(items) + n - 1) // n)
        p = max(0, min(pages - 1, st["page"].get(settings["tab"], 0))); st["page"][settings["tab"]] = p
        return items[p * n:(p + 1) * n], ("%d/%d" % (p + 1, pages)) if pages > 1 else ""
    RANK_INDEX = dict((name, i) for i, names in enumerate(RANK_ORDER) for name in names)
    def laston_key(m):
        v = m.get("_lo")
        if v is None:
            v = -1; hit = DATE_RE.search(m["laston"] or "")
            if hit is not None:
                a, sep, b, c = hit.group(1), hit.group(2), int(hit.group(3)), hit.group(4); ia, ic = int(a), int(c)
                if len(a) == 4 or ia > 31: y, mo, d = ia, b, ic
                else:
                    y = ic + (2000 if ic < 100 else 0)
                    if ia > 12: d, mo = ia, b
                    elif b > 12: mo, d = ia, b
                    elif sep == ".": d, mo = ia, b
                    else: mo, d = ia, b
                if 1 <= mo <= 12 and 1 <= d <= 31: v = y * 10000 + mo * 100 + d
            m["_lo"] = v
        return v
    def sort_caption(c): e = SORTS[SORT_CODES.index(settings["gsort"])]; return e[1] if c.get("gsort_long") else e[2]
    gcache = {"src": None, "how": None, "order": [], "names": {}, "online": 0}
    def mkey(m):
        k = m.get("_k")
        if k is None: k = m["_k"] = m["name"].lower()
        return k
    def first(e): return e[0]
    def static_key(how):
        nranks = len(RANK_ORDER)
        if how == "online": return lambda m: ((0 if m["online"] else 1), m["_k"])
        if how == "name": return lambda m: m["_k"]
        if how == "rank": return lambda m: (RANK_INDEX.get((m["rank"] or "").strip().lower(), nranks), m["_k"])
        return lambda m: ((0 if m["online"] else 1), -laston_key(m), m["_k"])
    def guild_order(gd, how):
        mem = gd["members"]; gc = gcache
        if gc["src"] is not mem or gc["how"] != how:
            names, online = {}, 0
            for m in mem:
                names[mkey(m)] = True
                if m["online"]: online += 1
            gc.update({"src": mem, "how": how, "order": sorted(mem, key=static_key(how)),
                       "names": names, "online": online})
        return gc
    def guild_items(me):
        gd = st["guild"] or empty_guild(); view, mobs = st["view"], st["mobs"]; how = settings["gsort"]
        gc = guild_order(gd, how); items = []; inview = 0
        if how == "online":
            near = []
            for m in gd["members"]:
                serial = view.get(m["_k"], 0)
                if serial:
                    d = mobs.get(serial)
                    if d: near.append(((d[3], (0 if m["online"] else 1), m["_k"]), serial, m))
            if near:
                near.sort(key=first); inview = len(near)
                for e in near: items.append((e[1], e[2]))
                for m in gc["order"]:
                    serial = view.get(m["_k"], 0)
                    if not (serial and mobs.get(serial)): items.append((serial, m))
            else:
                for m in gc["order"]: items.append((view.get(m["_k"], 0), m))
        else:
            for m in gc["order"]:
                serial = view.get(m["_k"], 0)
                if serial and serial in mobs: inview += 1
                items.append((serial, m))
        names = gc["names"]; allies = []
        for serial, name in st["allies"]:
            k = name.lower()
            if k in names or k == me or not name: continue
            d = mobs.get(serial)
            allies.append(((d[3] if d else 999, k), serial,
                           {"name": name, "rank": "ally", "laston": "", "title": "ally in view",
                            "online": True, "me": False, "_k": k, "ally": True}))
        if allies:
            allies.sort(key=first)
            for e in allies: items.append((e[1], e[2]))
        return items, inview
    def refresh():
        g, c = win["g"], win["c"]
        if g is None or (st["minimized"] and st["docked"]) or ("status" in c) != bool(st["minimized"]): return
        if st["minimized"]:
            n, inview = len(st["friends"]), len(st["inview"]); party = st["party"]
            txt = "%s: %s, %d in view" % (TITLE, Kit.count(n, "friend"), inview)
            if in_party(party): txt += ", party of %d" % (len(party[3]) + 1)
            Kit.set_text(c["status"], fit(txt, MINI_W - 18 - 66)); return
        tab = win["tab"]; info = c.get("info", []); tw = c.get("iw", win_w(tab) - 2 * Kit.MARGIN) - 20
        tw0 = tw - c.get("info_cut", 0)
        if tab == "friends":
            items = st["friends"]; shown, pg = page_of(items); inview = len(st["inview"])
            fk = (len(items), inview, tw0)
            if win["info"].get("friends") != fk:
                win["info"]["friends"] = fk
                Kit.set_text(info[0], fit("%s, %d in view" % (Kit.count(len(items), "friend"), inview) if items else
                                          "No friends yet: Add friend... targets one", tw0))
            show_rows(c, [(s, mob_name(s, n)) for s, n in shown], pg)
        elif tab == "party":
            party = st["party"]; me = player_serial()
            if not in_party(party):
                Kit.set_text(info[0], fit("Not in a party: Invite... asks someone to join", tw), Kit.HUE_INFO)
                Kit.set_text(info[1], "", Kit.HUE_INFO); items = []
            else:
                leader, inviter, loot, members = party; lname = "you" if leader == me else mob_name(leader)
                Kit.set_text(info[0], fit(("Party of %d, led by %s" % (len(members) + 1, lname))
                                          if leader else "Party of %d" % (len(members) + 1), tw), Kit.HUE_TEXT)
                Kit.set_text(info[1], fit("Party may loot your corpse: %s" % ("yes" if loot else "no"), tw),
                             Kit.HUE_INFO)
                items = [s for s in members if s != me]
            inviter = party[1] if party else 0; invite = bool(inviter) and not (party and party[0])
            for k in ("accept", "decline"):
                ctrl = c.get(k)
                if ctrl is not None and win["info"].get("vis_" + k) != invite:
                    win["info"]["vis_" + k] = invite
                    for part in (ctrl[0], ctrl[2]): Kit.set(part, "IsVisible", invite)
            if invite:
                nm = st["mobs"].get(inviter)
                Kit.set_text(info[0], fit("Party invite from %s: Accept or Decline" % (
                    nm[0] if nm and nm[0] else "0x%08X" % inviter), tw), Kit.HUE_TITLE)
            shown, pg = page_of(items)
            show_rows(c, [(s, mob_name(s)) for s in shown], pg, bool(party) and party[0] == me and bool(me))
        elif tab == "guild": refresh_guild(info, c, tw)
        else:
            if st["prof_part"]: read_profile(True)
            prof = st["profile"]
            if not prof:
                win["info"].pop("prof", None)
                for l in info: Kit.set_text(l, "")
                Kit.set_text(info[0], fit("No character logged in", tw), Kit.HUE_INFO); return
            pk = (prof, tw)
            if win["info"].get("prof") == pk: return
            win["info"]["prof"] = pk; name, lines, noto, gold, fol, fmax, wt, wmax, war, hidden = prof
            titles = [l for l in lines if l != name]
            texts = [(name, Kit.HUE_TITLE), (" / ".join(titles) if titles else
                      "No titles read yet: hover yourself once", Kit.HUE_INFO),
                     ("Notoriety: %s" % (noto or "unknown"), Kit.HUE_TEXT), ("Gold: %d" % gold, Kit.HUE_TEXT),
                     ("Followers: %d / %d" % (fol, fmax), Kit.HUE_TEXT), ("Weight: %d / %d" % (wt, wmax), Kit.HUE_TEXT),
                     ("%s%s" % ("War mode" if war else "Peace", ", hidden" if hidden else ""),
                      Kit.HUE_BAD if war else Kit.HUE_GOOD)]
            for l, (t, hue) in zip(info, texts): Kit.set_text(l, fit(t, tw), hue)
    def mob_name(s, other=None):
        d = st["mobs"].get(s); return (d[0] if d and d[0] else "") or st["names"].get(s, "") or other or "0x%08X" % s
    def show_rows(c, shown, pg, show_x=True):
        Kit.set_text(c["pg"], pg); rows = win["rows"]
        for r, (serial, name) in zip(rows, shown):
            status, hue, frac = mobile_status(serial); set_row(r, serial, name, status, hue, frac, show_x=show_x)
        for r in rows[len(shown):]: hide_row(r)
    def set_info(lbl, full, width, hue):
        done = win["info_in"]; k = (full, width, hue)
        if done.get(lbl) == k: return
        shown = fit(full, width); Kit.set_text(lbl, shown, hue); tip = full if shown != full else ""
        tips = win["info_tips"]
        if len(tips) > 64: tips.clear()
        if tips.get(lbl) != tip:
            tips[lbl] = tip; lbl.SetAcceptMouseInput(bool(tip)); lbl.SetTooltip(tip)
        if len(done) > 64: done.clear()
        done[lbl] = k
    def plain_info(lbl, text, hue=None): Kit.set_text(lbl, text, hue); win["info_in"].pop(lbl, None)
    def refresh_guild(info, c, tw):
        tw0 = tw - c.get("info_cut", 0); gd = st["guild"] or empty_guild(); prof = st["profile"]
        lines = [l for l in prof[1][1:] if l and l != prof[0]] if prof else []
        if not gd["ok"]: plain_info(info[0], fit("Guild window not read yet", tw0), Kit.HUE_INFO)
        elif not gd["in_guild"]: plain_info(info[0], fit("Not in a guild", tw0), Kit.HUE_INFO)
        else: set_info(info[0], gd["name"] or "Guild name not shown", tw0, Kit.HUE_TITLE)
        set_info(info[1], ("You: " + " / ".join(lines)) if lines else
                 "Your guild line isn't read yet: hover yourself once", tw, Kit.HUE_TEXT if lines else Kit.HUE_INFO)
        if gd["ok"] and gd["in_guild"]:
            set_info(info[2], "Alliance: %s     Faction: %s" % (
                gd["alliance"] or "none", gd["faction"] or "none"), tw, Kit.HUE_TEXT)
            set_info(info[3], "Charter: %s" % (gd["charter"] or "not set"), tw, Kit.HUE_INFO)
            set_info(info[4], "Website: %s" % (gd["website"] or "not set"), tw, Kit.HUE_INFO)
        else:
            for l in info[2:5]: plain_info(l, "")
        me_name = str(player_name() or "").lower(); items, inview = guild_items(me_name)
        online = guild_order(gd, settings["gsort"])["online"]
        if st["guild_busy"]:
            pages = st["guild_pages"]
            status = "Reading the guild window" + (" (page %d)" % pages if pages else ""); hue = Kit.HUE_TITLE
        elif not gd["ok"]:
            note = gd["note"]
            status = ((note[:1].upper() + note[1:]) if note else
                      ("Click Refresh to read the guild window" if not settings["gevery"]
                       else "Read when this tab shows"))
            hue = Kit.HUE_BAD if note else Kit.HUE_INFO
        elif not gd["in_guild"]: status, hue = "Read %s; allies in view below" % ago(gd["at"]), Kit.HUE_INFO
        else:
            n = len(gd["members"])
            status = "%s, %d online, %d in view; read %s" % (Kit.count(n, "member"), online, inview, ago(gd["at"]))
            if gd["note"]: status += "  (%s)" % gd["note"]
            hue = Kit.HUE_INFO
        set_info(info[5], status, tw, hue); shown, pg = page_of(items); Kit.set_text(c["pg"], pg)
        for r, (serial, m) in zip(win["rows"], shown):
            d = full_mob(serial) if serial else None
            if d is not None: stat, hue, frac = mobile_status(serial)
            elif m["online"]: stat, hue, frac = "Online", Kit.HUE_GOOD, None
            else: stat, hue, frac = (m["laston"] or "offline"), Kit.HUE_INFO, None
            if m["me"] or (me_name and mkey(m) == me_name): nhue = Kit.HUE_TITLE
            elif d is not None or m["online"]: nhue = Kit.HUE_GOOD if d is None else Kit.HUE_TEXT
            else: nhue = Kit.HUE_INFO
            set_row(r, serial if d is not None else 0, m["name"], stat, hue, frac,
                    extra={"rank": m["rank"], "title": m["title"]}, name_hue=nhue, bar=d is not None)
        for r in win["rows"][len(shown):]: hide_row(r)
    NOTE_BODY_H = 104; NOTE_H = Kit.MARGIN + 30 + Kit.GAP + NOTE_BODY_H + Kit.MARGIN
    def open_note(name):
        notew.close(); w, h = NOTE_W, NOTE_H; dx, dy = 240, 180
        if Kit.is_open(win["g"]): dx, dy = win["g"].GetX() + 40, win["g"].GetY() + 60
        g, store, c = notew.begin(w, h, (dx, dy)); Kit.add_window_frame(g, w, h)
        Kit.add_section(g, M, M, w - 2 * M, 30); Kit.add_label(g, "NOTE ON A PLAYER", M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, "Close without saving",
                       on_click=queue("note_close"))
        IW = w - 2 * M; yb = M + 30 + Kit.GAP; Kit.add_section(g, M, yb, IW, NOTE_BODY_H); lx = M + 12
        fx = lx + max(Kit.text_w("Player:"), Kit.text_w("Note:")) + 10; Kit.add_label(g, "Player:", lx, yb + 13)
        c["name"] = Kit.with_tip(Kit.add_textbox(g, name, fx, yb + 10, 200, numbers=False),
                                 "Player name as shown over their head (any case)")
        Kit.add_label(g, "Note:", lx, yb + 43)
        c["text"] = Kit.with_tip(Kit.add_textbox(g, NOTES.get(name.lower(), ("", ""))[1], fx, yb + 40,
                                                 M + IW - 12 - fx, numbers=False),
                                 "Your note (up to %d letters); saving it empty deletes it" % NOTE_CHARS)
        by = yb + 72
        Kit.art_button(g, store, "save", Kit.ART_OK, lx, by, "Save",
                       "Save the note for every character of this account", on_click=queue("note_save"))
        Kit.art_button(g, store, "delete", Kit.ART_CLOSE, lx + 35 + Kit.text_w("Save") + 16, by,
                       "Delete", "Delete this note", on_click=queue("note_delete"))
        hint = "Kept per account"
        Kit.add_label(g, hint, M + IW - 12 - Kit.text_w(hint), by + 3, Kit.HUE_INFO); notew.end(g, {"name": name})
    notew = Kit.Window(KEY, TITLE, None, ed, open_note, NOTE_POS_KEY, cleanup=cleanup, lock=False, owner=False,
                       clear={"c": {}, "store": ({}, {})})
    def note_fields():
        c = ed["c"]
        try: name = str(c["name"].Text or "")
        except Exception: name = ed["name"]
        try: text = str(c["text"].Text or "")
        except Exception: text = ""
        return name, text
    def read_msg(): tb = win["c"].get("msg"); return "" if tb is None else str(tb.Text or "").strip()
    def clear_msg():
        tb = win["c"].get("msg")
        if tb is not None: tb.SetText("")
        st["msg"].pop(settings["tab"], None)
    SAY = {"psend": "PartyMsg", "gsend": "GuildMsg", "asend": "AllyMsg"}
    def say(fn, txt):
        if not txt: tell("type something first."); return
        getattr(API, fn)(txt); clear_msg()
    def add_friend(serial):
        serial = int(serial or 0)
        if not serial: tell("nothing targeted."); return
        if serial == player_serial(): tell("that's you."); return
        m = API.FindMobile(serial)
        if m is None: tell("target a player or creature in view.", Kit.HUE_BAD); return
        name = str(m.Name or ""); who = name or "0x%08X" % serial
        if serial in [int(s) for s in API.GetAllFriends() or ()] or any(s == serial for s, _ in st["friends"]):
            tell("%s is already a friend." % who)
        elif API.AddFriend(serial):
            if name: st["names"][serial] = name; st["names_dirty"] = True
            tell("%s added to friends." % who, Kit.HUE_GOOD)
            if st["seen"] is not None: st["seen"] = st["seen"] | {serial}
        else: tell("couldn't add %s to friends." % who, Kit.HUE_BAD)
        st["next_friends"] = 0.0
    def remove_friend(serial):
        name = st["names"].get(serial, "") or "0x%08X" % serial
        if API.RemoveFriend(serial): tell("%s removed from friends." % name)
        else: tell("couldn't remove %s." % name, Kit.HUE_BAD)
        if st["seen"]: st["seen"].discard(serial)
        st["next_friends"] = 0.0
    def row_remove(serial):
        if not serial: return
        if win["tab"] == "friends": remove_friend(serial)
        elif win["tab"] == "party":
            party = st["party"]
            if party and party[0] and party[0] == player_serial():
                if not CL.game_action("RequestPartyRemoveMember", [to_uint(serial)], False):
                    tell("couldn't remove them (%s)." % CL.error, Kit.HUE_BAD)
            else: tell("only the leader can remove members.")
    def clear_inviter():
        try:
            import System; party = Typing._get(CL.world, "Party") if CL.world is not None else None
            if party is not None: Tz.put(party, "Inviter", System.UInt32(0))
        except Exception: pass
        p = st["party"]
        if p: st["party"] = (p[0], 0, p[2], p[3])
    def to_uint(serial):
        try: import System; return System.UInt32(int(serial))
        except Exception: return serial
    WINS = {"paperdoll": ("OpenPaperdoll", True, True), "status": ("OpenStatusBar", False, True),
            "gwin": ("OpenGuildGump", False, True), "invite": ("RequestPartyInviteByTarget", False, False),
            "edit": ("RequestProfile", True, False), "ignore": None}
    def open_window(what):
        e = WINS[what]
        if e is None: ok = CL.open_ignore_list()
        else: ok = CL.game_action(e[0], [to_uint(player_serial())] if e[1] else (), e[2])
        if not ok: tell("couldn't open that (%s)." % (CL.error or "no client access"), Kit.HUE_BAD)
        return ok
    def party_window():
        world = CL.world
        if world is None: tell("couldn't open the party window (no client access: %s)." % CL.error, Kit.HUE_BAD); return
        def run():
            import System; mgr = Typing._get(world, "Macros"); asm = mgr.GetType().Assembly
            mo_t, mt_t, ms_t = [asm.GetType("ClassicUO.Game.Managers." + n)
                                for n in ("MacroObject", "MacroType", "MacroSubType")]
            mo = System.Activator.CreateInstance(mo_t, System.Array[object]([System.Enum.Parse(mt_t, "Open", True),
                 System.Enum.Parse(ms_t, "PartyManifest", True)]))
            CL.call(mgr, "SetMacroToExecute", [mo]); CL.call(mgr, "Update"); return True
        if not CL.on_main(run): tell("couldn't open the party window (%s)." % CL.error, Kit.HUE_BAD)
    def diplomacy_job():
        gid, raw = last_gump()
        if not (gid and classify(raw) in ("guild", "roster")): gid = CL.find_server_gump(guild_test)[0]
        if not gid:
            if not CL.game_action("OpenGuildGump"):
                tell("couldn't ask for the guild window (%s)." % CL.error, Kit.HUE_BAD); return
            gid, _raw, _kind = wait_gump(lambda r2: classify(r2) in ("guild", "roster") and "ok")
        if not gid:
            tell("the guild window didn't come (are you in a guild?).", Kit.HUE_BAD); return
        if not press(gid, DIPLOMACY_LABEL, settings["dbutton"]):
            tell("no %s button found; press it in the guild window (or set its id in Social settings)."
                 % DIPLOMACY_LABEL)
    def click_mobile(serial):
        if API.HasTarget("any") and not HOST.cursor_busy(KEY): API.Target(serial); return
        API.SetLastTarget(to_uint(serial)); m = API.FindMobile(serial)
        if m is None: tell("%s isn't in view." % (st["names"].get(serial, "") or "they"))
        else: tell("%s is your last target." % (str(m.Name or "") or "that"))
    def start_guild_read():
        if st["guild_busy"]: return False
        st["guild_busy"] = True; st["guild_next"] = time.time() + GUILD_RETRY; jobs.append(guild_job); return True
    def announce():
        now_in = st["inview"]
        if not (settings["announce"] or settings["left"]) or st["seen"] is None: st["seen"] = now_in; return
        if settings["announce"]:
            for s in now_in - st["seen"]: tell("%s is in view." % mob_name(s, "a friend"), Kit.HUE_GOOD)
        if settings["left"]:
            for s in st["seen"] - now_in: tell("%s left view." % mob_name(s, "a friend"))
        st["seen"] = now_in
    PAGE_OPTS = {"ldy": 4, "fw": 40, "ltip": True, "clamp": False}
    def page_table(w):
        return (("WINDOW", (("note", fit("Shift+click a row to note that player; %d saved for this account."
                                         % len(NOTES), w - 28)),
                            ("note", fit("Action Bar cells can show this window (Client window, page 2).", w - 28)),
                            ("check", "bars", "Show health bars", "A bar for everyone in view; off, rows show name, "
                             "status and distance"),
                            ("num", "rows", "Rows per page:", "Rows on the Friends, Party and Guild tabs; the window "
                             "grows to fit", None, ROWS_MIN, ROWS_MAX))), ("FRIENDS  (journal lines)", (
                    ("check", "announce", "Say when a friend comes into view",
                     "One line when a friend comes into view (not those in view at start)"),
                    ("check", "left", "Say when a friend leaves view", "One line when a friend in view is gone"))),
                ("GUILD WINDOW  (for the Guild tab)", (("check", "ghide", "Read the guild window hidden",
                     "It opens invisible for the read; off, it shows for a few seconds", {"h": 28}),
                    ("num", "gevery", "Read it again every:", "Minutes between reads while the Guild tab shows (0-%d, "
                     "0 = only on Refresh)" % GUILD_EVERY_MAX, "min", 0, GUILD_EVERY_MAX),
                    ("num", "dbutton", "Diplomacy button id:", "Pressed when the Diplomacy caption isn't found; "
                     "ServUO uses %d (0-%d, 0 = caption only)" % (DIPLOMACY_BUTTON, DIPLOMACY_BUTTON_MAX), None, 0,
                     DIPLOMACY_BUTTON_MAX)), {"pad": 8}))
    def on_change(old, new):
        if (new["bars"], new["rows"]) != (old["bars"], old["rows"]) or (new["ghide"] != old["ghide"]
                                                                        and old["tab"] == "guild"):
            st["rebuild"] = True
        if (new["announce"] or new["left"]) and not (old["announce"] or old["left"]): st["seen"] = None
    cfg = Kit.Page(settings, page_table, save_settings, on_change, PAGE_OPTS)
    def _start():
        st.update({"shutting": False, "docked": False, "queue": [], "page": {}, "mobs": {},
                   "inview": set(), "seen": None, "next_list": 0.0, "next_friends": 0.0,
                   "next_profile": 0.0, "guild_busy": False, "guild_dirty": False,
                   "guild_next": 0.0, "guild_fails": 0, "guild_said": "", "guild_pages": 0,
                   "ghid": 0, "hid_any": False, "view": {}, "view_serials": None, "allies": [], "fit": None,
                   "me_s": 0, "friends_raw": None, "kept": {}, "prof_part": False,
                   "again_for": None, "again_build": False, "minimized": wnd.start_min()})
        del jobs[:]
        if not (LOADED_FOR[0] and LOADED_FOR[0] == player_serial()): load_settings()
        LOADED_FOR[0] = 0; CL.find(); build_window()
        wnd.dock(layout_fit, exact=True, verify=True, min=min_size); cleanup.service("social.note", note_of)
    def party_action(action):
        party = st["party"]
        if not in_party(party): tell("not in a party.")
        elif action == "leave":
            if not CL.game_action("RequestPartyRemoveMember", [to_uint(player_serial())], False):
                tell("couldn't leave (%s)." % CL.error, Kit.HUE_BAD)
        elif CL.game_action("RequestPartyLootState", [not party[2]], False):
            tell("party %s loot your corpse." % ("may not" if party[2] else "may"))
        else: tell("couldn't change looting (%s)." % CL.error, Kit.HUE_BAD)
    def answer_invite(action):
        inv = to_uint(st["party"][1])
        if action == "accept":
            def accept():
                if not CL.game_action("RequestPartyAccept", [inv], False): return None
                clear_inviter(); return True
            if CL.on_main(accept) is None: tell("couldn't accept (%s)." % CL.error, Kit.HUE_BAD)
            return
        net = Client._type("ClassicUO.Network.AsyncNetClient"); ext = Client._type("ClassicUO.Network.NetClientExt")
        def decline():
            CL.call(None, "Send_PartyDecline", [Typing._get(None, "Socket", net), inv], ext)
            clear_inviter(); return True
        if net is None or ext is None or CL.on_main(decline) is None:
            tell("couldn't decline (%s)." % CL.error, Kit.HUE_BAD)
    def next_sort():
        i = SORT_CODES.index(settings["gsort"]) if settings["gsort"] in SORT_CODES else 0
        settings["gsort"] = SORT_CODES[(i + 1) % len(SORT_CODES)]; save_settings(); c = win["c"]; lbl = c.get("gsort")
        if lbl is not None: Kit.set_text(lbl, sort_caption(c))
        btn = c.get("gsort_btn")
        if btn is not None and c.get("gsort_bare"): Kit.with_tip(btn, sort_tip(c))
        st["page"]["guild"] = 0; st["next_list"] = 0.0
    def guild_refresh():
        st["guild_said"] = ""
        if start_guild_read(): refresh()
        else: tell("already reading the guild window.")
    WITH_ARG = {"click": click_mobile, "rm": row_remove}
    PLAIN = {"pwin": party_window, "note_close": notew.close, "gsort": next_sort, "grefresh": guild_refresh}
    def _tick():
        if win["g"] is None: return
        if Kit.closed(win): return
        q = st["queue"]
        while q:
            action = q.pop(0); kind = action[0] if isinstance(action, tuple) else action
            if action == "to_bar" or (action == "toggle_min" and not st["minimized"]):
                st["msg"][settings["tab"]] = read_msg()
            if action == "redraw": st["rebuild"] = True
            elif wnd.action(action): continue
            elif kind in WITH_ARG: WITH_ARG[kind](action[1])
            elif action in ("leave", "loot"): party_action(action)
            elif action in PLAIN: PLAIN[action]()
            elif kind == "tab":
                if action[1] != settings["tab"]:
                    st["msg"][settings["tab"]] = read_msg(); settings["tab"] = action[1]; save_settings()
                    st["rebuild"] = True
            elif kind == "page":
                st["page"][settings["tab"]] = max(0, st["page"].get(settings["tab"], 0) + action[1])
                st["next_list"] = 0.0
            elif kind == "follow": Follow.toggle(action[1], TITLE)
            elif kind == "noview": tell("%s isn't in view." % action[1])
            elif action == "add":
                tell("target the friend to add.")
                HOST.pick_target(PICK_TIMEOUT, lambda serial: st["queue"].append(("picked", int(serial or 0))))
            elif kind == "picked":
                if action[1]: add_friend(action[1])
            elif action == "add_last": add_friend(int(API.LastTargetSerial or 0))
            elif action in WINS:
                if open_window(action) and action == "invite": tell("target who to invite.")
            elif action in ("accept", "decline") and st["party"] and st["party"][1]: answer_invite(action)
            elif action in SAY: say(SAY[action], read_msg())
            elif action == "diplo": jobs.append(diplomacy_job)
            elif action == "war": API.SetWarMode(not API.Player.InWarMode)
            elif kind == "note":
                if str(action[1]).startswith("0x"): tell("name not known yet.")
                else: open_note(action[1])
            elif action in ("note_save", "note_delete"):
                if ed["g"] is not None:
                    name, text = note_fields()
                    if set_note(name, text if action == "note_save" else ""): notew.close()
        if st["rebuild"]:
            if not st["minimized"]: st["msg"][settings["tab"]] = read_msg()
            build_window(); return
        if st["guild_dirty"]: st["guild_dirty"] = False; st["next_list"] = 0.0
        now = time.time()
        if now < st["next_list"] <= now + LIST_EVERY: return
        folded = st["minimized"] and st["docked"]
        if folded and not (settings["announce"] or settings["left"]): st["seen"] = None; return
        st["next_list"] = now + LIST_EVERY; read_friends(); tab = "mini" if st["minimized"] else win["tab"]
        wanted = set(); st["view_serials"] = None
        if tab == "mini":
            if not folded: read_party()
        elif tab == "friends": shown, _pg = page_of(st["friends"]); wanted.update(s for s, _ in shown)
        elif tab == "party":
            read_party(); party = st["party"]
            if party:
                me = player_serial(); shown, _pg = page_of([s for s in party[3] if s != me]); wanted.update(shown)
                wanted.add(party[0]); wanted.add(party[1])
        elif tab == "guild":
            scan_view()
            for s, _n in st["allies"]: wanted.add(s)
            gd = st["guild"] or empty_guild(); view = st["view"]
            for m in gd["members"]:
                s = view.get(mkey(m), 0)
                if s: wanted.add(s)
            if (settings["gevery"] and not st["guild_busy"] and now >= st["guild_next"]
                    and now - gd["at"] >= settings["gevery"] * 60):
                start_guild_read()
        if tab in ("guild", "profile"): read_profile(tab == "profile")
        mobs = {}; kept = st["kept"] if tab == "guild" else None
        for s in wanted:
            if s:
                e = kept.get(s) if kept else None
                if e is not None: mobs[s] = (e[0], 0, 0, e[1], False, None); continue
                d = read_mobile(s)
                if d is not None: mobs[s] = d
        st["mobs"] = mobs; inview = set(); rest = []
        for s in st["fserials"]:
            if s in mobs: inview.add(s)
            else: rest.append(s)
        if tab == "friends" or (tab == "mini" and not folded) or settings["announce"] or settings["left"]:
            inview |= friends_in_view(rest)
        st["inview"] = inview; announce(); refresh()
    def _thread_tick():
        while jobs and not st["shutting"]: jobs.pop(0)()
    def _stop():
        st["shutting"] = True; save_settings(); st["names_dirty"] = True; save_names(); save_notes(); cleanup.close()
    LOADED_FOR = [0]; load_settings(); LOADED_FOR[0] = player_serial()
    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "thread_tick": _thread_tick,
            "thread_wanted": lambda: bool(jobs), "config_height": cfg.height, "build_config": cfg.build,
            "poll_config": cfg.poll, "config_closed": cfg.closed}


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("social", "Social", "Friends, party, guild and profile", _module_social, 0.1, category="The world")
