def _module_skills():
    KEY = "skills"; TITLE = "Skills"
    def write_queue(q, title, what):
        while q:
            path, text = q.pop(0)
            try:
                with open(path, "w") as fh: fh.write(text)
                API.SysMsg("%s: %s written to %s." % (title, what, path), Kit.HUE_GOOD)
            except Exception as ex: API.SysMsg("%s: couldn't write %s (%s)." % (title, path, ex), Kit.HUE_BAD)
    def _part_window():
        KEY = "skills"; TITLE = "Skills"; SETTINGS_KEY = "Skills_settings"; POS_KEY = "Skills_pos"
        MARKS_KEY = "Skills_marks"
        LOCKSETS_KEY = "Skills_locksets"; SESSION_KEY = "Skills_session"; SESSION_STALE_H = 6; TOTAL_CAP_DEFAULT = 7000
        VANILLA = ("StandardSkillsGump", "SkillGumpAdvanced"); DOCK_ICON = 0x13E3; ROW_H = 22; SEARCH_W = 110
        BAR_W = 56; BAR_GROW = 120; RESIZE_SETTLE = 0.35; MIN_IW = 380; ZONE_NAME_MIN = 60
        ZONE_DROPS = ("bar", "gain", "cap", "real"); ZONE_FIELD_MIN = 80; ZONE_MIN_ROWS = 2; ZONE_LOG_MIN = 2
        TOTAL_TIP = "Real values added up, against the total cap (settings page)"
        LOCK_BTNS = (("all_up", "All up", "Set every listed skill to go up"),
                     ("all_down", "All down", "Set every listed skill to go down (click twice)"),
                     ("all_locked", "All locked", "Lock every listed skill"),
                     ("lock_capped", "Lock capped", "Lock every skill at its cap"))
        MINI_W, MINI_H = 280, 46
        DETAIL_BTNS = {"use": (Kit.ART_PLAY, "Use", "Use this skill", "use"),
                       "button": (Kit.ART_PAGE, "Make button", "Make its floating client button (or double-click "
                                  "it in the list)", "mkbutton"),
                       "pin": (Kit.ART_OK, "Pin", "Keep it at the top of the list (again to unpin)", "pin"),
                       "nextgrp": (Kit.ART_PAGE, "Next group", "Move it to the next skill group", "nextgrp")}
        LOG_KEEP = 200; MAX_LOCKSETS = 10; GEM = (0x0837, 0x0838, 0x0838); LOCK_ART = (0x0983, 0x0985, 0x082C)
        GROUP_OPEN, GROUP_SHUT = 0x0826, 0x0827; LINE_GREEN = 0x0808; BAR_BG_HUE = 946; DIM_HUE = 946
        SEL_COLOR, SEL_ALPHA = "#D8B048", 0.16; GROUP_COLOR, GROUP_ALPHA = "#FFFFFF", 0.07; ARM_SECS = 4.0
        REDRAW_EVERY = 1.0
        FALLBACK_NAMES = ["Alchemy", "Anatomy", "Animal Lore", "Item Identification", "Arms Lore", "Parrying",
            "Begging", "Blacksmithy", "Bowcraft/Fletching", "Peacemaking", "Camping",
            "Carpentry", "Cartography", "Cooking", "Detecting Hidden", "Discordance",
            "Evaluating Intelligence", "Healing", "Fishing", "Forensic Evaluation", "Herding",
            "Hiding", "Provocation", "Inscription", "Lockpicking", "Magery", "Resisting Spells",
            "Tactics", "Snooping", "Musicianship", "Poisoning", "Archery", "Spirit Speak",
            "Stealing", "Tailoring", "Animal Taming", "Taste Identification", "Tinkering",
            "Tracking", "Veterinary", "Swordsmanship", "Mace Fighting", "Fencing", "Wrestling",
            "Lumberjacking", "Mining", "Meditation", "Stealth", "Remove Trap", "Necromancy",
            "Focus", "Chivalry", "Bushido", "Ninjitsu", "Spellweaving", "Mysticism", "Imbuing", "Throwing"]
        TIPS = {"Alchemy": [(30, "NPC alchemists teach the first points for gold"), (50, "Heal and Agility potions"),
                        (70, "Cure and Greater Agility potions"), (90, "Greater Strength and Greater Heal potions"),
                        (100, "Greater Cure and Greater Explosion potions")],
            "Anatomy": [(100, "Use it on any creature or player; bandaging checks it too")],
            "Animal Lore": [(100, "Use it on tamed or tameable animals")],
            "Item Identification": [(100, "Use it on any item")], "Arms Lore": [(100, "Use it on weapons and armour")],
            "Parrying": [(100, "Fight with a shield on (only shields parry pre-AoS)")],
            "Begging": [(100, "Beg from town NPCs")],
            "Blacksmithy": [(30, "NPC blacksmiths teach the first points for gold"), (50, "Maces, then cutlasses"),
                            (65, "Scimitars, then broadswords and kryss"),
                            (80, "Katanas, then short spears and spears"),
                            (100, "Plate gorgets and gloves, then plate legs and tunics")],
            "Bowcraft/Fletching": [(40, "Shafts and arrows"), (65, "Bows"), (85, "Crossbows"),
                                   (100, "Heavy crossbows")],
            "Peacemaking": [(100, "Use it near creatures; tougher ones as it rises")],
            "Camping": [(100, "Light kindling over and over (a blade on a tree gives some)")],
            "Carpentry": [(30, "NPC carpenters teach the first points for gold"), (50, "Medium crates"),
                          (65, "Large crates, then wooden shields"), (85, "Fishing poles and quarter staves"),
                          (100, "Gnarled and black staves")],
            "Cartography": [(30, "NPC mapmakers teach the first points for gold"), (50, "Local maps"),
                            (65, "City maps"), (100, "Sea charts, then world maps")],
            "Cooking": [(30, "NPC cooks teach the first points for gold"),
                        (100, "Cook over and over (fish steaks and ribs are cheap)")],
            "Detecting Hidden": [(100, "Use it often, best near someone hidden")],
            "Discordance": [(100, "Use it on creatures; tougher ones as it rises")],
            "Evaluating Intelligence": [(100, "Use it on any player or creature")],
            "Healing": [(30, "NPC healers teach the first points; bandage yourself when hurt"),
                        (60, "Bandage yourself or friends while hurt"),
                        (80, "Keep bandaging; curing poison needs 60 Healing and 60 Anatomy"),
                        (100, "Keep bandaging; resurrecting needs 80 Healing and 80 Anatomy")],
            "Fishing": [(100, "Fish over and over, in any water")], "Forensic Evaluation": [(100, "Use it on corpses")],
            "Herding": [(100, "Herd animals with a shepherd's crook")], "Hiding": [(100, "Use it over and over")],
            "Provocation": [(100, "Make creatures fight each other; tougher ones as it rises")],
            "Inscription": [(30, "NPC scribes teach the first points for gold"),
                            (100, "Scribe scrolls of a circle you sometimes fail (spell in your book)")],
            "Lockpicking": [(30, "NPC thieves and tinkers teach the first points"),
                            (100, "Pick locked boxes just above your level")],
            "Magery": [(30, "NPC mages teach the first points; then 2nd circle spells"),
                       (45, "3rd circle: Bless, Teleport"), (55, "4th circle: Greater Heal, Mana Drain"),
                       (65, "5th circle: Paralyze, Mind Blast"), (75, "6th circle: Invisibility, Mark"),
                       (90, "7th circle: Flamestrike, Mana Vampire"), (100, "8th circle: Earthquake, summons")],
            "Resisting Spells": [(100, "Rises when spells hit you: a friend's low curses work")],
            "Tactics": [(100, "Rises as you fight with any weapon")],
            "Snooping": [(100, "Look into others' packs (a friend's pack animal is safe)")],
            "Musicianship": [(100, "Play an instrument; the other bard skills train it too")],
            "Poisoning": [(30, "Lesser poison on a weapon or food"), (60, "Regular poison"),
                          (100, "Greater, then deadly poison")],
            "Archery": [(30, "An archery butte or an NPC trainer for the first points"),
                        (100, "Shoot creatures a little tougher than you as it rises")],
            "Spirit Speak": [(100, "Use it over and over")],
            "Stealing": [(100, "Steal light items from a friend's pack; heavier is harder")],
            "Tailoring": [(30, "NPC tailors teach the first points for gold"), (45, "Short pants and fancy shirts"),
                          (55, "Cloaks"), (70, "Robes, then leather gorgets and sleeves"),
                          (85, "Leather leggings and tunics"),
                          (100, "Studded gloves, then studded sleeves and leggings")],
            "Animal Taming": [(30, "NPC animal trainers teach the first points for gold"),
                              (50, "Horses, ostards, llamas, black and polar bears"),
                              (70, "Panthers, grey wolves, grizzly bears, great harts"),
                              (85, "White wolves, bulls, frenzied ostards"),
                              (100, "Drakes and hell hounds, then dragons")],
            "Taste Identification": [(100, "Use it on food and potions")],
            "Tinkering": [(30, "NPC tinkers teach the first points for gold"), (60, "Tools and clock parts"),
                          (80, "Lockpicks"), (100, "Spyglasses or jewellery")],
            "Tracking": [(100, "Use it over and over")],
            "Veterinary": [(30, "NPC veterinarians teach the first points"), (60, "Bandage hurt animals and pets"),
                           (80, "Keep bandaging; curing needs 60 Veterinary, 60 Animal Lore"),
                           (100, "Keep bandaging; resurrecting needs 80 and 80")],
            "Swordsmanship": [(30, "NPC trainers or a training dummy for the first points"),
                              (100, "Fight creatures a little tougher than you as it rises")],
            "Mace Fighting": [(30, "NPC trainers or a training dummy for the first points"),
                              (100, "Fight creatures a little tougher than you as it rises")],
            "Fencing": [(30, "NPC trainers or a training dummy for the first points"),
                        (100, "Fight creatures a little tougher than you as it rises")],
            "Wrestling": [(30, "NPC trainers or a training dummy, empty-handed"),
                          (100, "Fight empty-handed; tougher creatures as it rises")],
            "Lumberjacking": [(100, "Chop trees with an axe over and over")],
            "Mining": [(30, "NPC miners teach the first points for gold"), (65, "Mine iron ore in mountains and caves"),
                       (100, "Keep mining: the coloured ores come from 65 up")],
            "Meditation": [(100, "Spend mana, then meditate; metal armour blocks it")],
            "Stealth": [(100, "Needs 80 Hiding: hide, then move with Stealth (light armour)")],
            "Remove Trap": [(100, "Use it on trapped boxes (tinkers can trap some to practise on)")],}
        STAT_TARGETS_KEY = "Skills_stat_targets"; STAT_TARGET_MAX = 250; LOCK_WORD = ("up", "down", "locked")
        LOCK_TEXT = ("Going up", "Going down", "Locked"); LOCK_SET = ("Set it to go up", "Set it to go down", "Lock it")
        FILTERS = [("all", "All skills"), ("trained", "Trained (above 0)"),
                   ("gaining", "Gaining now"), ("session", "Gained this session"),
                   ("up", "Set to go up"), ("down", "Set to go down"), ("locked", "Locked"),
                   ("below", "Below cap"), ("pinned", "Pinned")]
        SORTS = ("name", "real", "value", "cap", "gain", "lock")
        settings = {"replace": True, "x_hides": True, "bars": True, "col_cap": True,
                    "col_gain": True, "journal": False, "lock_at_cap": False, "lock_at_target": True, "cap_warn": True,
                    "rows": 12, "total_cap": TOTAL_CAP_DEFAULT, "hl_secs": 30, "rate_min": 30,
                    "sec_summary": True, "sec_stats": True, "sec_locks": True,
                    "sec_detail": True, "sec_log": False, "log_lines": 5,
                    "sort": "name", "asc": True, "filter": 0, "groups": False, "minimized": False, "width": 0, 
                    "tips": True, "lock_stat_target": True}
        DEFAULTS = dict(settings)
        LIMITS ={"rows": (4, 40), "total_cap": (100, 72000), "hl_secs": (0, 600),
                  "rate_min": (5, 240), "log_lines": (2, 15), "filter": (0, len(FILTERS) - 1), "width": (0, 4000)}
        LAYOUT_KEYS = ("bars", "col_cap", "col_gain", "rows", "sec_summary", "sec_stats",
                       "sec_locks", "sec_detail", "sec_log", "log_lines", "tips", "x_hides", "replace")
        GRP_SETTLE = 1.0; STAT_NAMES = ("Strength", "Dexterity", "Intelligence")
        def tip_table():
            out = {}
            for name, rows in TIPS.items():
                lst, lo = [], 0
                for hi, text in rows: lst.append((hi * 10, "%g-%g" % (lo / 10.0, hi), text)); lo = hi * 10
                out[name.lower()] = lst
            return out
        TIP_TABLE = tip_table(); marks = {"pins": set(), "targets": {}}; locksets = []
        stat_tgt = [0, 0, 0]
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "sel": None,
              "last_click": (None, 0.0), "arm": {}, "search": "", "pc": {}, "save_at": 0.0, "to_write": [], "ver": 0,
              "preview": False}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": [], "rowmap": {}}; page = {"sync": False, "skip": False}
        cleanup = Kit.Cleanup(); queue = Kit.queuer(st); say = Kit.sayer(TITLE)
        UIC = {}; REF = {"world": None, "player": None, "how": ""}
        SK = {"objs": [], "names": [], "click": [], "collide": [], "n": 0, "cur": [], "low": [], "full": True, "rr": 0}
        STATS = {"cur": [0, 0, 0], "locks": [0, 0, 0], "cap": 0, "prev": [0, 0, 0]}
        GR = {"list": [], "ok": False, "ver": 0, "sig": None, "of": {}}
        VG = {"gumps": None, "sig": None, "full_at": 0.0}
        def touch(): st["ver"] += 1; st["dirty"] = True
        HIDDEN_READ = 0.5; STATS_EVERY = 1.0; CAP_EVERY = 5.0
        def list_moved():
            st["dirty"] = True
            if (settings["sort"] != "name" or FILTERS[settings["filter"]][0] not in ("all", "pinned")): st["ver"] += 1
        fitst = {"width": None, "rows": None, "slot": None, "k": 1.0, "full": None}
        def eff_width(): return fitst["width"] if fitst["width"] is not None else settings["width"]
        def layout_fit(w, h, mode):
            new = (int(w), int(h)) if (w and h) else None
            if new == fitst["slot"] and not (mode == "again" and new is not None): return
            fitst["slot"] = new; fitst["width"] = new[0] if new is not None else None; fitst["rows"] = None
            st["m"] = None; st["rebuild"] = "window"; touch()
        def drawn_at(): return fitst["k"], fitst["full"]
        sess = {"start": 0.0, "base": {}, "stats": None, "seen": 0.0}
        def load_settings():
            Kit.kv_load(SETTINGS_KEY, ";", settings, LIMITS, ("sort",))
            if settings["sort"] not in SORTS: settings["sort"] = "name"
        def save_settings(): Kit.kv_save(SETTINGS_KEY, ";", settings, DEFAULTS, LIMITS, ("sort",))
        def load_marks():
            marks["pins"], marks["targets"] = set(), {}
            for part in Kit.get_var(MARKS_KEY).split(";"):
                p = part.split(":")
                if len(p) != 3: continue
                try: i, pin, tgt = int(p[0]), p[1] == "1", int(p[2])
                except ValueError: continue
                if pin: marks["pins"].add(i)
                if tgt > 0: marks["targets"][i] = tgt
        def save_marks():
            idx = sorted(marks["pins"] | set(marks["targets"]))
            Kit.put_var(MARKS_KEY, ";".join("%d:%s:%d" % (i, "1" if i in marks["pins"] else "0",
                                                          marks["targets"].get(i, 0)) for i in idx))
        def load_locksets():
            del locksets[:]
            for part in Kit.get_var(LOCKSETS_KEY).split("|"):
                if "=" in part:
                    name, code = part.split("=", 1)
                    if name and code: locksets.append((name, code))
        def save_locksets(): Kit.put_var(LOCKSETS_KEY, "|".join("%s=%s" % (n, c) for n, c in locksets))
        def load_stat_targets():
            p = Kit.get_var(STAT_TARGETS_KEY).split(",")
            for k in range(3):
                try: stat_tgt[k] = max(0, min(STAT_TARGET_MAX, int(p[k])))
                except (IndexError, ValueError): stat_tgt[k] = 0
        def load_session():
            p = Kit.get_var(SESSION_KEY).split("|"); now = time.time()
            sess.update({"start": now, "base": {}, "stats": None, "seen": now})
            if len(p) < 4: return
            try: start, seen = float(p[0]), float(p[3])
            except ValueError: return
            if now - seen > SESSION_STALE_H * 3600 or start > now: return
            base = {}
            for kv in p[1].split(","):
                if ":" in kv:
                    try: k, v = kv.split(":"); base[int(k)] = int(v)
                    except ValueError: pass
            stats = None
            try: s = [int(x) for x in p[2].split(",")]; stats = s if len(s) == 3 else None
            except ValueError: pass
            sess.update({"start": start, "base": base, "stats": stats, "seen": now})
        def save_session():
            sess["seen"] = time.time(); b = ",".join("%d:%d" % (k, v) for k, v in sorted(sess["base"].items()))
            s = ",".join(str(x) for x in sess["stats"]) if sess["stats"] else ""
            Kit.put_var(SESSION_KEY, "%d|%s|%s|%d" % (sess["start"], b, s, sess["seen"]))
        def new_session():
            sess.update({"start": time.time(), "base": {}, "stats": None})
            for i in range(SK["n"]): sess["base"][i] = SK["cur"][i][0]
            if any(STATS["cur"]): sess["stats"] = list(STATS["cur"])
            st["gains"], st["log"] = {}, []; save_session()
        def save_pos(): Kit.save_pos(POS_KEY, win["g"])
        def find_world(): return Typing._get(None, "Instance", Client._type("ClassicUO.Game.World"))
        def load_skill_objects(objs, how):
            names = [str(safe(lambda s=s: s.Name, "") or "?") for s in objs]
            click = [bool(safe(lambda s=s: s.IsClickable, False)) for s in objs]; low = [n.lower() for n in names]
            collide = [any(low[i] in low[j] for j in range(i)) for i in range(len(low))]
            SK.update({"objs": objs, "names": names, "click": click, "collide": collide,
                       "n": len(objs), "low": low, "full": True})
            if len(SK["cur"]) != len(objs): SK["cur"] = [[0, 0, 0, 0] for _ in objs]
            REF["how"] = how; st["m"] = None
        def refresh_refs(force=False):
            now = time.time()
            if not force and now < st["ref_at"]: return SK["n"] > 0
            st["ref_at"] = now + 3.0; world = find_world()
            player = Typing._get(world, "Player") if world is not None else None
            if player is not None:
                arr = Typing._get(player, "Skills"); objs = list(arr) if arr is not None else None
                if objs:
                    same = REF["player"] is not None and REF["player"] is player and len(objs) == SK["n"]
                    relog = REF["player"] is not None and not same; REF.update({"world": world, "player": player})
                    if not same:
                        if relog: SK["cur"] = []; st["ready"] = False; st["rebuild"] = "window"
                        load_skill_objects(objs, "client")
                    return True
            REF.update({"world": world, "player": None})
            if SK["n"] == 0 or REF["how"] != "api":
                objs = []
                for name in FALLBACK_NAMES:
                    s = API.GetSkill(name)
                    if s is not None and str(s.Name) == name: objs.append(s)
                if objs: load_skill_objects(objs, "api")
            return SK["n"] > 0
        RR_N = 15
        def read_skills(full=False):
            changed = {}; cur = SK["cur"]; objs = SK["objs"]; n = len(objs)
            if n == 0 or len(cur) != n: return changed
            if SK["full"]: SK["full"] = False; full = True
            rr = SK["rr"] % n; SK["rr"] = rr + RR_N; _int = int
            for i in range(n):
                s = objs[i]
                try: b, v = _int(s.BaseFixed), _int(s.ValueFixed)
                except Exception: continue
                c = cur[i]
                if full or b != c[0] or v != c[1] or (i - rr) % n < RR_N:
                    try: cp = _int(s.CapFixed); lk = _int(s.Lock)
                    except Exception: continue
                    if b != c[0] or v != c[1] or cp != c[2] or lk != c[3]: changed[i] = c; cur[i] = [b, v, cp, lk]
            return changed
        def read_stats():
            cur, locks, cap = STATS["cur"], STATS["locks"], STATS["cap"]; p = REF["player"]
            if p is None: p = API.Player
            if p is not None:
                try:
                    cur = [int(p.Strength), int(p.Dexterity), int(p.Intelligence)]
                    locks = [int(p.StrLock), int(p.DexLock), int(p.IntLock)]; cap = int(p.StatsCap)
                except Exception: pass
            if st["stat_pending"]:
                now = time.time(); locks = list(locks)
                for k, (lk, until) in list(st["stat_pending"].items()):
                    if now < until: locks[k] = lk
                    else: st["stat_pending"].pop(k, None)
            if cur == STATS["cur"] and locks == STATS["locks"] and cap == STATS["cap"]: return False
            STATS["prev"] = STATS["cur"]; STATS["cur"], STATS["locks"], STATS["cap"] = cur, locks, cap; return True
        def skills_loaded(): return any(c[2] > 0 for c in SK["cur"])
        def group_mgr():
            w = REF["world"] or find_world(); return Typing._get(w, "SkillsGroupManager") if w is not None else None
        def groups_wanted():
            if cfg.f is not None: return True
            if win["g"] is None or not win["c"] or st["minimized"] or st["docked"]: return False
            return settings["groups"] or (st["sel"] is not None and settings["sec_detail"])
        def read_groups(force=False):
            now = time.time()
            if not force and (now < st["grp_at"] or not groups_wanted()): return
            st["grp_at"] = now + (1.0 if cfg.f is not None or settings["groups"] else GRP_DETAIL_EVERY)
            mgr = group_mgr(); lst = Typing._get(mgr, "Groups") if mgr is not None else None; out = []
            if lst is not None:
                for g in list(lst):
                    try:
                        n = int(g.Count); members = [int(g.GetSkill(k)) for k in range(n)]
                        out.append({"obj": g, "name": str(g.Name or ""), "members": [m for m in members if m < SK["n"]],
                                    "max": bool(g.IsMaximized)})
                    except Exception: continue
            sig = (lst is not None, tuple((g["name"], tuple(g["members"]), g["max"]) for g in out))
            if sig != GR["sig"]: GR["sig"] = sig; GR["ver"] += 1
            of = {}
            for gi in range(len(out) - 1, -1, -1):
                for k in out[gi]["members"]: of[k] = gi
            GR["list"], GR["ok"], GR["of"] = out, lst is not None, of
        GRP_DETAIL_EVERY = 3.0
        def group_of(i): return GR["of"].get(i)
        def groups_save():
            mgr = group_mgr()
            if mgr is not None: safe(lambda: mgr.Save())
            read_groups(True)
        def ga_call(name, args): return Tz.call(None, name, args, Tz.T("ClassicUO.Game.GameActions"))
        def set_lock(i, v):
            if i is None or i >= SK["n"] or SK["cur"][i][3] == v: return
            if not SK["collide"][i]: API.SetSkillLock(SK["names"][i], LOCK_WORD[v])
            else:
                try:
                    import System; ga_call("ChangeSkillLockStatus", [System.UInt16(i), System.Byte(v)])
                    lt = Tz.T("ClassicUO.Game.Data.Lock"); Tz.put(SK["objs"][i], "Lock", System.Enum.ToObject(lt, v))
                except Exception: pass
            SK["cur"][i][3] = v
        def use_skill(i):
            if i is None or i >= SK["n"]: return
            if not SK["click"][i]:
                say("%s can't be used directly." % SK["names"][i], Kit.HUE_INFO); return
            if not SK["collide"][i]: API.UseSkill(SK["names"][i]); return
            try: ga_call("UseSkill", [i])
            except Exception as ex: say("couldn't use %s (%s)." % (SK["names"][i], Tz.why(ex)), Kit.HUE_BAD)
        def make_button(i):
            if i is None or i >= SK["n"] or not SK["click"][i]:
                say("only a usable skill gets a button.", Kit.HUE_INFO); return
            try:
                import System
                for b in Tz.windows(["SkillButtonGump"]):
                    if int(Tz.get(b, "SkillID")) == i: b.Dispose()
                t = Tz.T("ClassicUO.Game.UI.Gumps.SkillButtonGump"); world = REF["world"] or find_world(); g = win["g"]
                x, y = (g.GetX() + g.GetWidth() + 10, g.GetY()) if Kit.is_open(g) else (200, 200)
                btn = System.Activator.CreateInstance(t, System.Array[object]([world, SK["objs"][i], x, y]))
                Tz.call(None, "Add", [btn, True], Tz.T("ClassicUO.Game.Managers.UIManager"))
                say("%s button placed beside the window." % SK["names"][i], Kit.HUE_GOOD)
            except Exception as ex: say("couldn't make the button (%s)." % Tz.why(ex), Kit.HUE_BAD)
        def ask_server():
            world = REF["world"] or find_world(); st["swallow_until"] = time.time() + 6.0; st["asked"] = time.time()
            try: ga_call("OpenSkills", [world]); return True
            except Exception: return False
        def set_stat_lock(k, v):
            API.SetStatLock(("str", "dex", "int")[k], LOCK_WORD[v]); STATS["locks"][k] = v
            st["stat_pending"][k] = (v, time.time() + 2.5)
        def f1(tenths): return "%.1f" % (tenths / 10.0)
        def sgain(i): b = sess["base"].get(i); return 0 if b is None else SK["cur"][i][0] - b
        def total_gain(): return sum(sgain(i) for i in range(SK["n"]))
        MIN_RATE_SPAN = 600.0
        def hours_running(): return max(MIN_RATE_SPAN, time.time() - sess["start"]) / 3600.0
        def recent_gain(i, now):
            win_s = settings["rate_min"] * 60; return sum(d for t, d in st["gains"].get(i, []) if now - t <= win_s)
        def rates(i, now):
            avg = sgain(i) / hours_running()
            span = max(MIN_RATE_SPAN, min(settings["rate_min"] * 60.0, now - max(sess["start"], st["started"])))
            recent = recent_gain(i, now) / (span / 3600.0); return avg, recent
        def dur(secs):
            secs = int(max(0, secs))
            if secs >= 3600: return "%dh %02dm" % (secs // 3600, (secs % 3600) // 60)
            if secs >= 60: return "%dm" % (secs // 60)
            return "%ds" % secs
        def eta(i, now, rt=None):
            base, _, cap, _ = SK["cur"][i]
            if base >= cap: return "at cap"
            avg, recent = rt if rt is not None else rates(i, now); r = recent if recent > 0 else avg
            if r <= 0: return "--"
            return "~" + dur((cap - base) / r * 3600)
        def note_gains(changed, now):
            dirty = False
            for i, old in changed.items():
                new = SK["cur"][i]; d = new[0] - old[0]
                if d == 0: continue
                dirty = True; name = SK["names"][i]
                if i not in sess["base"]: sess["base"][i] = old[0]
                if d > 0:
                    st["gains"].setdefault(i, []).append((now, d))
                    if len(st["gains"][i]) > LOG_KEEP: st["gains"][i] = st["gains"][i][-LOG_KEEP:]
                    if settings["hl_secs"] > 0: st["hl"][i] = now + settings["hl_secs"]
                st["log"].append((now, name, d, new[0]))
                if len(st["log"]) > LOG_KEEP: st["log"] = st["log"][-LOG_KEEP:]
                if settings["journal"]:
                    say("%s %s%s (%s, session %+.1f)." % (name, "+" if d > 0 else "-", f1(abs(d)), f1(new[0]),
                        sgain(i) / 10.0), Kit.HUE_GOOD if d > 0 else Kit.HUE_BAD)
                for mark, opt, what in ((new[2], "lock_at_cap", "its cap (%s)"),
                                        (marks["targets"].get(i), "lock_at_target", "its target %s")):
                    if d > 0 and mark is not None and old[0] < mark <= new[0]:
                        what = what % f1(mark)
                        if settings[opt] and new[3] == 0:
                            set_lock(i, 2); say("%s reached %s and was locked." % (name, what), Kit.HUE_GOOD)
                        else: say("%s reached %s." % (name, what), Kit.HUE_GOOD)
            if dirty and time.time() >= st["save_at"]: st["save_at"] = time.time() + 15.0; save_session()
        def total_real(): return sum(c[0] for c in SK["cur"])
        def at_total_cap():
            if total_real() < settings["total_cap"]: return False
            up = any(c[3] == 0 and c[0] < c[2] for c in SK["cur"])
            down = any(c[3] == 1 and c[0] > 0 for c in SK["cur"]); return up and not down
        def cap_warning():
            if not settings["cap_warn"]: st["warned_cap"] = False; return
            stuck = at_total_cap()
            if stuck and not st["warned_cap"]:
                say("at the total skill cap (%s) and no skill set to go down: nothing can rise."
                    % f1(settings["total_cap"]), Kit.HUE_BAD)
            st["warned_cap"] = stuck
        def stat_gain(k): base = sess["stats"]; return STATS["cur"][k] - base[k] if base else 0
        def note_stats():
            prev, cur = STATS["prev"], STATS["cur"]
            for k in range(3):
                t = stat_tgt[k]
                if not t or not prev[k] or cur[k] != t: continue
                way = {1: 0, -1: 1}.get(cur[k] - prev[k])
                if way is None: continue
                if settings["lock_stat_target"] and STATS["locks"][k] == way:
                    set_stat_lock(k, 2)
                    say("%s reached its target %d and was locked." % (STAT_NAMES[k], t), Kit.HUE_GOOD)
                else: say("%s reached its target %d." % (STAT_NAMES[k], t), Kit.HUE_GOOD)
        def stat_at_target(k):
            t, v = stat_tgt[k], STATS["cur"][k]
            if t and v == t and settings["lock_stat_target"] and STATS["locks"][k] != 2:
                set_stat_lock(k, 2); say("%s is at its target %d and was locked." % (STAT_NAMES[k], t), Kit.HUE_GOOD)
        def stat_tip(k, hrs):
            v = STATS["cur"][k]; lines = ["%s %d" % (STAT_NAMES[k], v)]
            if sess["stats"]: d = stat_gain(k); lines[0] += ": %+d this session (%.1f / hour)" % (d, d / hrs)
            t = stat_tgt[k]
            if not t: lines.append("No target (click: set one in settings)")
            elif v == t: lines.append("Target %d: reached" % t)
            else:
                lines.append("Target %d: %d to go %s%s" % (t, abs(t - v), "up" if t > v else "down",
                    ", then it locks" if settings["lock_stat_target"] else ""))
            return "\n".join(lines)
        def tip_for(i):
            if i is None or i >= SK["n"]: return None
            rows = TIP_TABLE.get(SK["names"][i].lower())
            if rows:
                base = SK["cur"][i][0]
                for hi, rng, text in rows:
                    if base < hi: return rng, text
            return None
        def passes(i, now):
            f = FILTERS[settings["filter"]][0]; base, _, cap, lock = SK["cur"][i]; q = st["search"]
            if q and q not in SK["low"][i]: return False
            if f == "trained": return base > 0
            if f == "gaining": return recent_gain(i, now) > 0
            if f == "session": return sgain(i) > 0
            if f in LOCK_WORD: return lock == LOCK_WORD.index(f)
            if f == "below": return base < cap
            if f == "pinned": return i in marks["pins"]
            return True
        def sort_list(idx):
            s = settings["sort"]; name = SK["low"].__getitem__
            if s == "name": out = sorted(idx, key=name)
            else:
                col = {"real": 0, "value": 1, "cap": 2, "lock": 3}.get(s)
                kf = sgain if col is None else (lambda i: SK["cur"][i][col])
                out = sorted(sorted(idx, key=name), key=kf)
            if not settings["asc"]: out.reverse()
            return out
        def descriptors(now):
            vis = [i for i in range(SK["n"]) if passes(i, now)]; vset = set(vis)
            pins = [i for i in vis if i in marks["pins"]]; filt = bool(st["search"]) or settings["filter"] != 0
            out = []
            if not settings["groups"] or not GR["ok"]:
                if FILTERS[settings["filter"]][0] == "pinned": return [("s", i) for i in sort_list(vis)]
                rest = [i for i in vis if i not in marks["pins"]]
                return [("s", i) for i in sort_list(pins) + sort_list(rest)]
            if pins and FILTERS[settings["filter"]][0] != "pinned":
                shut = st["pc"].get("pin", False); out.append(("g", "pin", shut))
                if not shut: out += [("s", i) for i in sort_list(pins)]
            seen = set()
            for gi, g in enumerate(GR["list"]):
                mem = [i for i in g["members"] if i in vset]; seen.update(g["members"])
                if not mem and filt: continue
                out.append(("g", gi, not g["max"]))
                if g["max"]: out += [("s", i) for i in sort_list(mem)]
            other = [i for i in vis if i not in seen]
            if other:
                shut = st["pc"].get("other", False); out.append(("g", "other", shut))
                if not shut: out += [("s", i) for i in sort_list(other)]
            return out
        def row_click(i):
            def handler(*args):
                now = time.time(); last, t = st["last_click"]
                if last == i and now - t <= 0.6: st["last_click"] = (None, 0.0); queue.add(("button", i), dup=True)
                else: st["last_click"] = (i, now); queue.add(("pick", i), dup=True)
            return handler
        on_disposed = Kit.disposer("skills.window", st, win)
        def redraw(): st["rebuild"] = "window"
        def setp(ctrl, attr, value):
            if ctrl is None: return
            k = (ctrl, attr)
            if UIC.get(k) == value: return
            UIC[k] = value
            try:
                zk = fitst["k"]
                if attr == "Width": Kit.ui_w(ctrl, value if zk == 1.0 else int(round(value * zk)))
                elif attr == "Pos":
                    if zk == 1.0: Kit.ui_pos(ctrl, value[0], value[1])
                    else: ctrl.SetPos(int(round(value[0] * zk)), int(round(value[1] * zk)))
                else: setattr(ctrl, attr, value)
            except Exception: pass
        def remember(ctrl, attr, value): UIC[(ctrl, attr)] = value
        def cap_w(caption): return 35 + Kit.text_w(caption)
        def metrics(IW=None, zone=False):
            m = st["m"]
            if m is not None and (IW is None or (m["IW"] == IW and m.get("zone", False) == zone)): return m
            m = natural_metrics()
            if zone and IW:
                drop = []
                for key in ZONE_DROPS:
                    if m["sa_w"] + 16 <= IW: break
                    drop.append(key); m = natural_metrics(drop)
                short = (m["sa_w"] + 16) - IW
                if short > 0:
                    cut = min(short, m["name_w"] - ZONE_NAME_MIN)
                    if cut > 0: widen(m, -cut); m["cut"] = True
                m["drop"] = tuple(drop)
            m["zone"] = zone; extra = max(0, IW - (m["sa_w"] + 16)) if IW else 0
            if extra:
                bar_extra = min(BAR_GROW, extra * 2 // 5) if m["bar_x"] is not None else 0
                if bar_extra:
                    m["bar_w"] += bar_extra
                    for key in ("gain_x", "lock_x"):
                        if m[key] is not None and m[key] > m["bar_x"]: m[key] += bar_extra
                widen(m, extra - bar_extra)
            m["IW"] = IW; st["m"] = m; return m
        def widen(m, d):
            m["name_w"] += d
            for key in ("real_x", "val_x", "cap_x", "bar_x", "gain_x", "lock_x"):
                if m[key] is not None: m[key] += d
            m["row_w"] = m["lock_x"] + m["lock_w"] + 6; m["sa_w"] = m["row_w"] + 16
        def natural_metrics(drop=()):
            m = {"cut": False, "drop": ()}; names = SK["names"] or FALLBACK_NAMES
            arrow_w = Kit.pic_size(LOCK_ART[0])[0] or 10; m["arrow_w"] = arrow_w
            m["lock_w"] = max(arrow_w, Kit.pic_size(LOCK_ART[2])[0] or 12); gem_w = Kit.pic_size(GEM[0])[0] or 11
            m["name_x"] = 4 + gem_w + 6
            m["name_w"] = (max([Kit.text_w(n) for n in names] + [Kit.text_w("Skill") + arrow_w + 4]) + 10)
            num_w = max(Kit.text_w("120.0"), Kit.text_w("Value") + arrow_w + 3) + 10
            gain_w = max(Kit.text_w("+120.0"), Kit.text_w("Gain") + arrow_w + 3) + 8
            if "real" in drop: m["real_x"] = None; m["val_x"] = x = m["name_x"] + m["name_w"]
            else: m["real_x"] = m["name_x"] + m["name_w"]; m["val_x"] = x = m["real_x"] + num_w
            x += num_w; m["bar_h"] = max(4, min(11, Kit.pic_size(Kit.LINE_BLUE)[1] or 9)); m["bar_w"] = BAR_W
            for key, on, cw in (("cap_x", settings["col_cap"] and "cap" not in drop, num_w),
                                ("bar_x", settings["bars"] and "bar" not in drop, BAR_W + 10),
                                ("gain_x", settings["col_gain"] and "gain" not in drop, gain_w)):
                m[key] = x if on else None
                if on: x += cw
            m["lock_x"] = x; m["row_w"] = x + m["lock_w"] + 6; m["sa_w"] = m["row_w"] + 16; return m
        def detail_rows(): return 6 if settings["tips"] else 5
        def layout():
            M, GAP = Kit.MARGIN, Kit.GAP; m = natural_metrics(); sw, sh = Kit.screen()
            tool_need = 12 + Kit.text_w("Find:") + 6 + SEARCH_W + 14 + \
                cap_w(max((f[1] for f in FILTERS), key=Kit.text_w)) + 12 + 24 + Kit.text_w("Groups") + 12
            locks_need = 12 + sum(cap_w(c) for c in ZLOCKS) + 3 * 10 + 12
            detail_need = 12 + cap_w("Use") + 12 + cap_w("Make button") + 12 + cap_w("Next group") + 12
            aw = Kit.pic_size(LOCK_ART[2])[0] or 12
            stats_need = 12 + 3 * (Kit.text_w("Int 125 (+25)") + 8 + aw + 14) + \
                Kit.text_w("Stats 225 / 225") + 12 if settings["sec_stats"] else 0
            IW = max(m["sa_w"] + 16, tool_need, locks_need, detail_need, stats_need, MIN_IW); min_w = IW + 2 * M
            if eff_width() > min_w: IW = eff_width() - 2 * M
            if sw: IW = max(min_w - 2 * M, min(IW, sw - 2 * M - 10))
            m = metrics(IW); L = {"IW": IW, "W": IW + 2 * M, "min_w": min_w}; y = M + 30 + GAP
            n_sum = (2 if settings["sec_summary"] else 0) + (1 if settings["sec_stats"] else 0)
            rows = settings["rows"] if fitst["rows"] is None else fitst["rows"]
            for key, on, hh in (("sum", n_sum, 6 + 24 * n_sum + 4), ("tool", True, 36),
                                ("list", True, 26 + rows * ROW_H + 6), ("locks", settings["sec_locks"], 36),
                                ("detail", settings["sec_detail"], 6 + 24 * detail_rows() + 4),
                                ("log", settings["sec_log"], 26 + 20 * settings["log_lines"] + 4)):
                if on: L[key] = (y, hh); y += hh + GAP
            L["H"] = y - GAP + M; L["fixed_h"] = L["H"] - rows * ROW_H; lo = LIMITS["rows"][0]
            L["min_h"] = L["fixed_h"] + lo * ROW_H
            if sh and L["H"] > sh - 10 and rows > lo:
                fit_rows = max(lo, (sh - 10 - L["fixed_h"]) // ROW_H)
                if fit_rows < rows:
                    shrink = (rows - fit_rows) * ROW_H; L["list"] = (L["list"][0], L["list"][1] - shrink)
                    for key in ("locks", "detail", "log"):
                        if key in L: L[key] = (L[key][0] - shrink, L[key][1])
                    L["H"] -= shrink; L["rows"] = fit_rows; return L
            L["rows"] = rows; return L
        ZLOCKS = tuple(b[1] for b in LOCK_BTNS)
        def zflow(widths, gap, IW):
            out, x, line = [], 12, 0
            for cw in widths:
                if x > 12 and x + cw > IW - 12: x, line = 12, line + 1
                out.append((x, line)); x += cw + gap
            return out, line + 1
        def zone_min_w():
            nm = natural_metrics(ZONE_DROPS)
            need = [nm["sa_w"] - max(0, nm["name_w"] - ZONE_NAME_MIN) + 16,
                    12 + Kit.text_w("Find:") + 6 + ZONE_FIELD_MIN + 2 + 12,
                    12 + cap_w(max((f[1] for f in FILTERS), key=Kit.text_w)) + 12, 12 + 24 + Kit.text_w("Groups") + 12]
            if settings["sec_summary"]: need += [12 + Kit.text_w("Session +99.9") + 12, 12 + cap_w("Reset") + 12]
            if settings["sec_stats"]:
                need.append(12 + Kit.text_w("Int 125 (+25)") + 8 + (Kit.pic_size(LOCK_ART[2])[0] or 12) + 4)
            if settings["sec_locks"]: need.append(12 + max(cap_w(t) for t in ZLOCKS) + 12)
            if settings["sec_detail"]:
                aw = max(Kit.pic_size(a)[0] for a in LOCK_ART) or 12
                need += [12 + ZONE_NAME_MIN + 8 + 3 * (aw + 10) + 12,
                         12 + Kit.text_w("Target:") + 8 + 56 + 12 + Kit.text_w("none set") + 4,
                         12 + max(cap_w("Make button"), cap_w("Next group")) + 12]
            return max(need) + 2 * Kit.MARGIN
        def zone_plan(w, h):
            M, GAP = Kit.MARGIN, Kit.GAP; IW = w - 2 * M; Z = {"IW": IW, "W": w, "H": h}; secs = []; n_sum = 0
            if settings["sec_summary"]:
                cap = f1(settings["total_cap"])
                one = "Total %s / %s   (%s free)   with bonuses %s" % (cap, cap, cap, cap)
                Z["total2"] = Kit.text_w(one) > IW - 24; rx = IW - 12 - cap_w("Reset")
                Z["sess_own"] = rx - 12 - 6 < Kit.text_w("Session +99.9")
                n_sum += (2 if Z["total2"] else 1) + (2 if Z["sess_own"] else 1)
            if settings["sec_stats"]:
                slot = Kit.text_w("Int 125 (+25)") + 8; aws = Kit.pic_size(LOCK_ART[2])[0] or 12
                places, sx, line = [], 12, 0
                for j in range(3):
                    if sx > 12 and sx + slot + aws > IW - 4: sx, line = 12, line + 1
                    places.append((sx, line)); sx += slot + aws + 14
                if sx > 12 and sx + Kit.text_w("Stats 225 / 225") > IW - 4: sx, line = 12, line + 1
                Z["stats"] = (places, (sx, line)); n_sum += line + 1
            if n_sum: secs.append(("sum", 6 + 24 * n_sum + 4))
            fcap = cap_w(max((f[1] for f in FILTERS), key=Kit.text_w)); grp_w = 24 + Kit.text_w("Groups")
            tx = 12 + Kit.text_w("Find:") + 6; field = IW - tx - 14 - fcap - 12 - grp_w - 12
            if field >= ZONE_FIELD_MIN:
                T = {"field": field, "filter": (tx + field + 14, 0), "groups": (IW - 12 - grp_w, 0)}; n = 1
            else:
                T = {"field": max(20, IW - tx - 2 - 12), "filter": (12, 1)}
                if 12 + fcap + 12 + grp_w + 12 <= IW: T["groups"], n = (IW - 12 - grp_w, 1), 2
                else: T["groups"], n = (12, 2), 3
            T["tx"] = tx; Z["T"] = T; secs.append(("tool", 36 + 28 * (n - 1))); secs.append(("list", None))
            if settings["sec_locks"]:
                Z["locks_p"], n = zflow([cap_w(t) for t in ZLOCKS], 10, IW); secs.append(("locks", 36 + 26 * (n - 1)))
            if settings["sec_detail"]:
                tx = 12 + Kit.text_w("Target:") + 8; tgt_x = tx + 56 + 12; pin_x = IW - 12 - cap_w("Unpin")
                pin_here = pin_x - tgt_x - 6 >= Kit.text_w("none set")
                keys = ["use", "button"] + ([] if pin_here else ["pin"]) + ["nextgrp"]
                caps = {"use": "Use", "button": "Make button", "pin": "Unpin", "nextgrp": "Next group"}
                places, nb = zflow([cap_w(caps[kk]) for kk in keys], 12, IW)
                if nb == 1: places[-1] = (IW - 12 - cap_w("Next group"), 0)
                Z["D"] = {"tx": tx, "tgt_x": tgt_x, "pin_here": pin_here, "pin_x": pin_x,
                          "tgt_w": (pin_x - 6 if pin_here else IW - 4) - tgt_x, "btns": list(zip(keys, places))}
                secs.append(("detail", 6 + 24 * (detail_rows() + nb) + 4))
            n_log = settings["log_lines"] if settings["sec_log"] else 0
            if settings["sec_log"]: secs.append(("log", None))
            def height(rows, logn):
                y = M + 30 + GAP
                for key, hh in secs:
                    if key == "list": hh = 26 + rows * ROW_H + 6
                    elif key == "log": hh = 26 + 20 * logn + 4
                    y += hh + GAP
                return y - GAP + M
            lo = LIMITS["rows"][0]; rows = (h - height(0, n_log)) // ROW_H
            while rows < lo and n_log > ZONE_LOG_MIN: n_log -= 1; rows = (h - height(0, n_log)) // ROW_H
            Z["need"] = height(ZONE_MIN_ROWS, min(n_log, ZONE_LOG_MIN) if settings["sec_log"] else 0)
            Z["short"] = rows < ZONE_MIN_ROWS; rows = max(1, rows); Z["rows"], Z["log_n"] = rows, n_log
            list_h = max(26 + rows * ROW_H + 6, h - height(0, n_log) + 32); y = M + 30 + GAP
            for key, hh in secs:
                if key == "list": hh = list_h
                elif key == "log": hh = 26 + 20 * n_log + 4
                Z[key] = (y, hh); y += hh + GAP
            Z["H"] = y - GAP + M; return Z
        def zone_geom(w, h):
            mw = zone_min_w(); k = 1.0 if w >= mw else w / float(mw); lw, lh, Z = w, h, None
            for _ in range(4):
                lw = w if k == 1.0 else max(mw, int(round(w / k))); lh = h if k == 1.0 else int(round(h / k))
                Z = zone_plan(lw, lh)
                if not Z["short"]: break
                k = min(k, h / float(Z["need"]) * 0.999)
            return lw, lh, k, Z
        def fit_set(c, key, txt, room, hue=None, base=None, lbl=None):
            if lbl is None: lbl = c.get(key)
            if lbl is None: return
            src = (txt, room, hue, base); sk = key + "_src"
            if c.get(sk) == src: return
            c[sk] = src; shown = Kit.fit(txt, room); Kit.set_text(lbl, shown, hue); cat = c.get(key + "_cat")
            if cat is None: return
            tip = base or "" if shown == txt else (("%s. %s" % (txt, base)) if base else txt)
            if tip != c.get(key + "_tip"): c[key + "_tip"] = tip; safe(lambda: cat.SetTooltip(tip))
        def plain_plan(L):
            IW = L["IW"]; Z = dict(L, total2=False, sess_own=False, log_n=settings["log_lines"])
            step = Kit.text_w("Int 125 (+25)") + 8 + (Kit.pic_size(LOCK_ART[2])[0] or 12) + 14
            Z["stats"] = ([(12 + j * step, 0) for j in range(3)], (12 + 3 * step, 0)); tx = 12 + Kit.text_w("Find:") + 6
            Z["T"] = {"tx": tx, "field": SEARCH_W, "filter": (tx + SEARCH_W + 14, 0),
                      "groups": (IW - 12 - 24 - Kit.text_w("Groups"), 0)}
            Z["locks_p"] = zflow([cap_w(t) for t in ZLOCKS], 10, IW)[0]; tx = 12 + Kit.text_w("Target:") + 8
            pin_x = IW - 12 - cap_w("Unpin")
            Z["D"] = {"tx": tx, "tgt_x": tx + 68, "pin_here": True, "pin_x": pin_x, "tgt_w": pin_x - 6 - (tx + 68),
                      "btns": [("use", (12, 0)), ("button", (24 + cap_w("Use"), 0)),
                               ("nextgrp", (IW - 12 - cap_w("Next group"), 0))]}
            return Z
        def build_zone(g, store, c, Z, k, zone=True):
            M = Kit.MARGIN; IW = Z["IW"]; x0 = M; metrics(IW, zone=zone)
            def zlabel(key, x, y, w, hue=None, h=22, dy=0):
                lbl = Kit.add_label(g, "", x, y, hue)
                if zone:
                    c[key + "_cat"] = Kit.catcher(g, x - 2, y + dy - 3, max(8, w + 4), h, lambda: None)
                    c[key + "_tip"] = ""
                return lbl
            if "sum" in Z:
                y0, hh = Z["sum"]; Kit.add_section(g, x0, y0, IW, hh); ry = y0 + 6
                if settings["sec_summary"]:
                    nl = 2 if Z["total2"] else 1; c["total"] = Kit.add_label(g, "", x0 + 12, ry + 3)
                    cat = Kit.catcher(g, x0 + 8, ry, IW - 16, 24 * nl - 2, lambda: None, TOTAL_TIP)
                    if zone: c["total_cat"], c["total_tip"] = cat, TOTAL_TIP
                    ry += 24
                    if Z["total2"]: c["total2"] = Kit.add_label(g, "", x0 + 12, ry + 3); ry += 24
                    rx = x0 + IW - 12 - cap_w("Reset"); c["session_w"] = IW - 28 if Z["sess_own"] else rx - x0 - 12 - 6
                    c["session"] = zlabel("session", x0 + 12, ry + 3, c["session_w"])
                    if Z["sess_own"]: ry += 24
                    Kit.art_button(g, store, "newsess", Kit.ART_CLOSE, rx, ry - 1, "Reset",
                                   "New session: gains count from now", on_click=queue("newsess"))
                    ry += 24
                if settings["sec_stats"]:
                    slot = Kit.text_w("Int 125 (+25)") + 8; places, (tx, tl) = Z["stats"]; c["stats"] = []
                    c["stat_cats"], c["stat_tips"] = [], [None, None, None]
                    for j, nm in enumerate(("Str", "Dex", "Int")):
                        sx, ln = places[j]; yy = ry + 24 * ln; lbl = Kit.add_label(g, "", x0 + sx, yy + 3)
                        c["stat_cats"].append(Kit.catcher(g, x0 + sx - 2, yy, slot - 4, 22,
                                                          queue("settings"), STAT_NAMES[j]))
                        pic = Kit.add_pic(g, LOCK_ART[0], x0 + sx + slot, yy + 5)
                        if pic is not None:
                            Kit.on_click(pic, queue(("stat", j), dup=True))
                            Kit.with_tip(pic, "Click: %s up, down or locked" % nm)
                        c["stats"].append((lbl, pic))
                    c["stat_total_w"] = IW - 4 - tx
                    c["stat_total"] = zlabel("stat_total", x0 + tx, ry + 24 * tl + 3, c["stat_total_w"], Kit.HUE_INFO)
            y0, hh = Z["tool"]; T = Z["T"]; Kit.add_section(g, x0, y0, IW, hh)
            Kit.add_label(g, "Find:", x0 + 12, y0 + 10)
            c["search"] = Kit.with_tip(Kit.add_textbox(g, st["search"], x0 + T["tx"], y0 + 7, T["field"], numbers=False,
                                                       font=max(8, int(round(16 * k)))), "Type part of a skill name")
            c["search"].SetPlaceholder("search"); fx, fl = T["filter"]
            c["filter"] = Kit.art_button(g, store, "filter", Kit.ART_PAGE, x0 + fx, y0 + 7 + 28 * fl,
                                         FILTERS[settings["filter"]][1], "Which skills to list (click: next)",
                                         on_click=queue("filter"))
            gx, gl = T["groups"]
            c["groups"] = Kit.add_check(g, "Groups", x0 + gx, y0 + 9 + 28 * gl, settings["groups"],
                                        "Show the client's skill groups (click one to fold it)")
            build_list(g, c, x0, Z["list"][0], IW, Z["list"][1], Z["rows"])
            if "locks" in Z:
                y0, hh = Z["locks"]; Kit.add_section(g, x0, y0, IW, hh)
                for (key, cap, tip), (bx, ln) in zip(LOCK_BTNS, Z["locks_p"]):
                    Kit.art_button(g, store, key, Kit.ART_OK, x0 + bx, y0 + 7 + 26 * ln, cap, tip, on_click=queue(key))
            if "detail" in Z:
                y0, hh = Z["detail"]; D = Z["D"]; Kit.add_section(g, x0, y0, IW, hh); ry = y0 + 6
                aw = max(Kit.pic_size(a)[0] for a in LOCK_ART) or 12; lx = x0 + IW - 12 - 3 * (aw + 10)
                c["d_name_w"] = lx - x0 - 12 - 8; c["d_locks"] = []
                c["d_name"] = zlabel("d_name", x0 + 12, ry + 3, c["d_name_w"], Kit.HUE_TITLE)
                for v in range(3):
                    p = Kit.add_pic(g, LOCK_ART[v], lx + v * (aw + 10), ry + 5)
                    if p is not None:
                        Kit.on_click(p, queue(("dlock", v), dup=True)); Kit.with_tip(p, LOCK_SET[v])
                    c["d_locks"].append(p)
                ry += 24; c["d_lw"] = IW - 28; c["d_l1"] = zlabel("d_l1", x0 + 12, ry + 3, c["d_lw"]); ry += 24
                c["d_l2"] = zlabel("d_l2", x0 + 12, ry + 3, c["d_lw"], Kit.HUE_INFO); ry += 24
                if settings["tips"]:
                    c["d_tip"] = Kit.add_label(g, "", x0 + 12, ry + 3, Kit.HUE_TEXT)
                    c["d_tip_cat"] = Kit.catcher(g, x0 + 8, ry, IW - 16, 22, lambda: None,
                                                 "Training tip for this skill's range")
                    c["d_tip_full"] = None; ry += 24
                Kit.add_label(g, "Target:", x0 + 12, ry + 3)
                c["target"] = Kit.with_tip(Kit.add_textbox(g, "", x0 + D["tx"], ry, 56, numbers=False,
                                                           font=max(8, int(round(16 * k)))),
                                           "Real value to stop at (empty = none)")
                c["target"].SetPlaceholder("none"); c["d_tgt_w"] = D["tgt_w"]
                c["d_tgt"] = zlabel("d_tgt", x0 + D["tgt_x"], ry + 3, D["tgt_w"], Kit.HUE_INFO); ry += 24
                for key, (bx, ln) in ([("pin", (D["pin_x"], -1))] if D["pin_here"] else []) + D["btns"]:
                    art, cap, tip, act = DETAIL_BTNS[key]
                    b = Kit.art_button(g, store, key, art, x0 + bx, ry - 1 + 24 * ln, cap, tip, on_click=queue(act))
                    if key == "pin": c["pin"] = b
            if "log" in Z:
                y0, hh = Z["log"]; Kit.add_section(g, x0, y0, IW, hh, "RECENT GAINS"); c["log"] = []
                c["log_w"] = IW - 28
                for j in range(Z["log_n"]):
                    c["log"].append(zlabel("log%d" % j, x0 + 12, y0 + 26 + 20 * j, c["log_w"], Kit.HUE_TEXT, 20, 1))
        def close_tip():
            if settings["x_hides"]: return "Hide %s (%s brings it back)" % (
                TITLE, "the client's Skills button" if settings["replace"] else "the Action Bar's Skills button")
            return Kit.CLOSE_TIP % TITLE
        def build_window():
            old, win["g"] = win["g"], None; UIC.clear(); st["desc"] = None; st["rebuild"] = None
            if st["hidden"]:
                win.update({"c": {}, "rows": [], "rowmap": {}, "store": ({}, {})}); Kit.dispose(old); return
            M = Kit.MARGIN; store = ({}, {}); c = {}; st["resize_at"], st["preview"] = 0.0, False; win["L"] = None
            L, Z = None, None; fitst["k"], fitst["full"] = 1.0, None
            if st["minimized"] or st["docked"]: w, h = MINI_W, MINI_H
            elif fitst["slot"] is not None: w, h = fitst["slot"]; lw, lh, k, Z = zone_geom(w, h)
            else: L = layout(); w, h, IW = L["W"], L["H"], L["IW"]; win["L"] = L
            x, y = Kit.load_pos(POS_KEY, (160, 120), (w, h))
            if Kit.is_open(old): x, y = old.GetX(), old.GetY()
            at = LAYOUT.placed.get(KEY) if HOST.layout_holds(KEY) else None
            if at is not None: x, y = int(at[0]), int(at[1])
            if Z is not None:
                g = G.CreateGump(True, True); Kit.add_window_frame(g, lw, lh)
                Kit.title_bar(g, store, lw, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"), close_tip=close_tip())
                build_zone(g, store, c, Z, k)
                if k != 1.0:
                    wf = max(zone_min_w(), w); fitst["k"], fitst["full"] = k, (int(wf), int(zone_plan(wf, 0)["need"]))
                    Kit.scale_window(g, k)
            elif L is None:
                g = G.CreateGump(True, True)
                c["mini"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"), close_tip=close_tip())
            else:
                if at is None: x, y = Kit.clamp(x, y, w, h)
                g = G.CreateModernGump(x, y, w, h, True, L["min_w"], L["min_h"], on_resized)
                g.SetAlpha(0); Kit.add_window_frame(g, w, h, mouse=False); Kit.add_section(g, M, M, IW, 30)
                Kit.add_label(g, TITLE.upper(), M + 30, M + 7, Kit.HUE_TITLE)
                zoned = Kit.zone_up(KEY); x_set = w - M - (10 if zoned else 84 + Kit.DOCK_DX) - cap_w("Settings")
                if zoned: Kit.catcher(g, M, M, x_set - M - 6, 30, lambda *a: None, None, movable=True)
                else: Kit.title_catcher(g, M, M, x_set - M - 6, 30, queue("toggle_min"), key=KEY)
                Kit.art_button(g, store, "settings", Kit.ART_PAGE, x_set, M + 4, "Settings", Kit.SETTINGS_TIP % TITLE,
                               on_click=queue("settings"))
                if not zoned:
                    Kit.dock_button(g, store, w - M - 74, M + 7, on_click=queue("to_bar"))
                    Kit.art_button(g, store, "min", Kit.ART_MIN, w - M - 74, M + 7, None, Kit.MIN_TIP,
                                   on_click=queue("toggle_min"))
                    Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, close_tip())
                build_zone(g, store, c, plain_plan(L), 1.0, False)
            xy = Kit.show_window(g, x, y, w, h, KEY, st["docked"], on_disposed(g), save_pos, win,
                                 {"g": g, "c": c, "store": store, "rows": [], "rowmap": {},
                                  "w": lw if Z is not None else w})
            if at is not None and xy is not None and tuple(xy) != (x, y):
                g.SetPos(x, y); Kit.note_rect(g, x, y); Kit.moved_by_code(g)
            if at is not None: LAYOUT.fit_now(KEY, g)
            if settings["minimized"] != st["minimized"]: settings["minimized"] = st["minimized"]; save_settings()
            show_target_text(); read_groups(); rebuild_rows(time.time()); refresh(time.time()); Kit.dispose(old)
        wnd = None; hooks = Kit.dock_hooks(TITLE, DOCK_ICON, st, win, redraw)
        def on_resized(*args):
            st["resize_at"] = time.time(); g = win["g"]; L = win.get("L")
            if st["preview"] or L is None or not Kit.is_open(g) or st["minimized"] or st["docked"]: return
            if fitst["width"] is None and (int(g.GetWidth()), int(g.GetHeight())) != (L["W"], L["H"]):
                st["preview"] = True; g.SetAlpha(0.55)
        def apply_resize():
            g = win["g"]; L = win.get("L"); st["preview"] = False
            if L is None or not Kit.is_open(g) or st["minimized"] or st["docked"]: return
            if fitst["width"] is not None: g.SetAlpha(0); return
            w, h = int(g.GetWidth()), int(g.GetHeight()); lo, hi = LIMITS["rows"]
            rows = max(lo, min(hi, (h - L["fixed_h"] + ROW_H // 2) // ROW_H)); width = w if w > L["min_w"] else 0
            if rows == L["rows"] and width == settings["width"] and (w, h) == (L["W"], L["H"]): g.SetAlpha(0); return
            if rows != settings["rows"] or width != settings["width"]:
                settings["rows"], settings["width"] = rows, width; save_settings(); page["sync"] = True
            st["m"] = None; st["rebuild"] = "window"; touch()
        def build_list(g, c, x0, y0, IW, h, rows):
            m = metrics(); Kit.add_section(g, x0, y0, IW, h); sx = x0 + 8; c["hdr"] = {}
            heads = [("name", "Skill", m["name_x"], "Sort by name"),
                     ("real", "Real", m["real_x"], "Sort by real value without item bonuses"),
                     ("value", "Value", m["val_x"], "Sort by value with bonuses"),
                     ("cap", "Cap", m["cap_x"], "Sort by cap"),
                     ("gain", "Gain", m["gain_x"], "Sort by gain this session")]
            nxt = {"name": m["real_x"] or m["val_x"], "real": m["val_x"], "value": m["cap_x"] or m["bar_x"]
                   or m["gain_x"] or m["lock_x"], "cap": m["bar_x"] or m["gain_x"] or m["lock_x"], "gain": m["lock_x"]}
            for key, text, cx, tip in heads:
                if cx is None: continue
                c["hdr"][key] = Kit.add_label(g, text, sx + cx, y0 + 6, Kit.HUE_INFO)
                Kit.catcher(g, sx + cx - 2, y0 + 3, (nxt[key] or cx + 40) - cx - 2, 20,
                            queue(("sort", key), dup=True), tip + " (again to reverse)")
            lp = Kit.add_pic(g, LOCK_ART[2], sx + m["lock_x"], y0 + 7)
            if lp is not None:
                Kit.on_click(lp, queue(("sort", "lock"), dup=True)); Kit.with_tip(lp, "Sort by lock (again to reverse)")
            c["hdr"]["lock_pic"] = lp; c["arrow"] = Kit.add_pic(g, LOCK_ART[1], sx, y0 + 8, mouse=False)
            c["sa"] = G.CreateGumpScrollArea(sx, y0 + 26, m["sa_w"], rows * ROW_H); g.Add(c["sa"])
            c["sa_xy"] = (sx, y0 + 26)
        def move_row(r, y):
            if r["y"] == y: return
            r["y"] = y; zk = fitst["k"]
            for ctl, x, dy in r["parts"]:
                try:
                    if zk == 1.0: Kit.ui_pos(ctl, x, y + dy)
                    else: ctl.SetPos(int(round(x * zk)), int(round((y + dy) * zk)))
                except Exception: pass
        def show_row(r, on):
            if r["hidden"] == (not on): return
            r["hidden"] = not on
            for ctl, _, _ in r["parts"]:
                if ctl is r.get("bar"):
                    if not on: setp(ctl, "IsVisible", False)
                else: setp(ctl, "IsVisible", on)
            if on: r["sig"] = None
        def rebuild_rows(now):
            c = win["c"]
            if "sa_xy" not in c: return
            key = (st["ver"], GR["ver"], int(now) if FILTERS[settings["filter"]][0] == "gaining" else 0)
            if st["desc"] is not None and key == st["desc_key"]: return
            st["desc_key"] = key; desc = descriptors(now)
            if desc == st["desc"]: return
            st["desc"] = desc; m = metrics(); tgt = c["sa"]
            made = len(win["rowmap"]) + (0 if "selbox" in c else 1) + (0 if c.get("empty") else 1)
            if "selbox" not in c:
                c["selbox"] = Kit.add_box(tgt, 0, 0, m["row_w"], ROW_H - 1, SEL_ALPHA, SEL_COLOR)
                setp(c["selbox"], "IsVisible", False)
            empty = "" if desc else ("No skill matches; change the search or the filter."
                                     if SK["n"] else "Waiting for the server to send your skills.")
            if c.get("empty") is None and empty: c["empty"] = Kit.add_label(tgt, empty, m["name_x"], 3, Kit.HUE_INFO)
            if c.get("empty") is not None: Kit.set_text(c["empty"], empty); setp(c["empty"], "IsVisible", bool(empty))
            rowmap = win["rowmap"]; rows, want, nth = [], set(), {}
            for n, d in enumerate(desc):
                ry = n * ROW_H; k = (d[0], d[1]); nth[k] = c_k = nth.get(k, -1) + 1; k = (d[0], d[1], c_k)
                r = rowmap.get(k)
                if r is None:
                    r = build_group_row(tgt, ry, d, m) if d[0] == "g" else build_skill_row(tgt, ry, d[1], m)
                    rowmap[k] = r
                else: move_row(r, ry); show_row(r, True)
                if d[0] == "g": setp(r["arrow"], "Graphic", GROUP_SHUT if d[2] else GROUP_OPEN)
                want.add(k); rows.append(r)
            for k, r in rowmap.items():
                if k not in want and not r["hidden"]: show_row(r, False); move_row(r, 0)
            win["rows"] = rows
            if fitst["k"] != 1.0 and made != len(rowmap) + (0 if "selbox" in c else 1) + (0 if c.get("empty") else 1):
                Kit.scale_window(win["g"], fitst["k"])
            place_selbox()
        def put(r, ctl, x, dy):
            if ctl is not None: r["parts"].append((ctl, x, dy))
            return ctl
        def build_group_row(tgt, ry, d, m):
            key, shut = d[1], d[2]; r = {"kind": "g", "key": key, "y": ry, "hidden": False, "parts": [], "sig": None}
            put(r, Kit.add_box(tgt, 0, ry + 1, m["row_w"], ROW_H - 2, GROUP_ALPHA, GROUP_COLOR), 0, 1)
            r["arrow"] = put(r, Kit.add_pic(tgt, GROUP_SHUT if shut else GROUP_OPEN, 4, ry + 5, mouse=False), 4, 5)
            remember(r["arrow"], "Graphic", GROUP_SHUT if shut else GROUP_OPEN)
            r["lbl"] = put(r, Kit.add_label(tgt, "", m["name_x"], ry + 3, Kit.HUE_TITLE), m["name_x"], 3)
            r["real"] = put(r, Kit.add_label(tgt, "", m["real_x"], ry + 3, Kit.HUE_INFO),
                            m["real_x"], 3) if m["real_x"] is not None else None
            r["val"] = put(r, Kit.add_label(tgt, "", m["val_x"], ry + 3, Kit.HUE_INFO), m["val_x"], 3)
            r["gain"] = put(r, Kit.add_label(tgt, "", m["gain_x"], ry + 3, Kit.HUE_INFO),
                            m["gain_x"], 3) if m["gain_x"] is not None else None
            put(r, Kit.catcher(tgt, 0, ry, m["row_w"], ROW_H - 1, queue(("fold", key), dup=True),
                            "Fold or unfold this group"), 0, 0)
            return r
        def build_skill_row(tgt, ry, i, m):
            r = {"kind": "s", "i": i, "y": ry, "hidden": False, "parts": [], "sig": None}
            r["name"] = put(r, Kit.add_label(tgt, row_name(i, m), m["name_x"], ry + 3), m["name_x"], 3)
            r["real"] = put(r, Kit.add_label(tgt, "", m["real_x"], ry + 3), m["real_x"], 3) \
                if m["real_x"] is not None else None
            r["val"] = put(r, Kit.add_label(tgt, "", m["val_x"], ry + 3), m["val_x"], 3)
            r["cap"] = put(r, Kit.add_label(tgt, "", m["cap_x"], ry + 3, Kit.HUE_INFO),
                           m["cap_x"], 3) if m["cap_x"] is not None else None
            r["gain"] = put(r, Kit.add_label(tgt, "", m["gain_x"], ry + 3, Kit.HUE_GOOD),
                            m["gain_x"], 3) if m["gain_x"] is not None else None
            r["bar"] = None
            if m["bar_x"] is not None:
                bdy = (ROW_H - m["bar_h"]) // 2; by = ry + bdy
                if Kit.pic_size(Kit.LINE_RED)[0] > 0:
                    put(r, Kit.add_tiled(tgt, Kit.LINE_RED, m["bar_x"], by, m["bar_w"],
                                      m["bar_h"], hue=BAR_BG_HUE), m["bar_x"], bdy)
                else:
                    put(r, Kit.add_tiled(tgt, Kit.SECTION_TILE, m["bar_x"], by, m["bar_w"],
                                      m["bar_h"], 1.0), m["bar_x"], bdy)
                r["bar"] = put(r, Kit.add_tiled(tgt, Kit.LINE_BLUE, m["bar_x"], by, 1, m["bar_h"]), m["bar_x"], bdy)
            tip = "Click: pick it (details below); double-click: its floating button" \
                if SK["click"][i] else "Click: pick it (details below)"
            r["cat"] = put(r, Kit.catcher(tgt, m["name_x"] - 2, ry, m["lock_x"] - m["name_x"] - 2,
                                       ROW_H - 1, row_click(i), tip), m["name_x"] - 2, 0)
            r["tip0"] = r["cat_tip"] = tip; r["use"] = None
            if SK["click"][i]:
                b = G.CreateGumpButton("", Kit.HUE_TEXT, GEM[0], GEM[1], GEM[2]); b.SetPos(4, ry + 6); tgt.Add(b)
                Kit.on_click(b, queue(("use", i), dup=True)); Kit.with_tip(b, "Use " + SK["names"][i])
                r["use"] = put(r, b, 4, 6)
            r["lock"] = put(r, Kit.add_pic(tgt, LOCK_ART[0], m["lock_x"], ry + 4), m["lock_x"], 4); r["tip"] = None
            if r["lock"] is not None:
                Kit.on_click(r["lock"], queue(("lock", i), dup=True)); remember(r["lock"], "Graphic", LOCK_ART[0])
            return r
        def row_name(i, m=None):
            nm = SK["names"][i] if i < SK["n"] else "?"; m = m or metrics()
            if m.get("cut"): return Kit.fit(nm, m["name_w"] - 10)
            return nm
        def place_selbox():
            box = win["c"].get("selbox")
            if box is None: return
            y = None; sel = st["sel"]
            if sel is not None:
                for r in win["rows"]:
                    if r["kind"] == "s" and r["i"] == sel: y = r["y"]; break
            if y is None: setp(box, "IsVisible", False)
            else:
                setp(box, "Pos", (0, y)); setp(box, "IsVisible", True)
        def name_hue(i, now):
            if st["hl"].get(i, 0) > now: return Kit.HUE_GOOD
            if i in marks["pins"]: return Kit.HUE_TITLE
            return Kit.HUE_TEXT
        def refresh_rows(now):
            cur = SK["cur"]; n = SK["n"]; has_gain = settings["col_gain"]; tips_on = settings["tips"]
            bar_w = metrics()["bar_w"]
            for r in win["rows"]:
                if r["kind"] == "g": refresh_group_row(r); continue
                i = r["i"]
                if i >= n: continue
                base, val, cap, lock = cur[i]; hue = name_hue(i, now)
                sig = (base, val, cap, lock, sgain(i) if has_gain else 0, hue)
                if sig == r["sig"]: continue
                r["sig"] = sig; Kit.set_text(r["name"], row_name(i), hue)
                if r["real"] is not None:
                    Kit.set_text(r["real"], f1(base), Kit.HUE_GOOD if cap and base >= cap else Kit.HUE_TEXT)
                bonus = val - base
                Kit.set_text(r["val"], f1(val), Kit.HUE_GOOD if bonus > 0 else (
                    Kit.HUE_BAD if bonus < 0 else Kit.HUE_TEXT))
                if r["cap"] is not None: Kit.set_text(r["cap"], f1(cap))
                if r["gain"] is not None:
                    gn = sgain(i)
                    Kit.set_text(r["gain"], ("%+.1f" % (gn / 10.0)) if gn else "",
                                 Kit.HUE_GOOD if gn > 0 else Kit.HUE_BAD)
                if r["lock"] is not None:
                    setp(r["lock"], "Graphic", LOCK_ART[lock])
                    tip = "%s (click: %s)" % (LOCK_TEXT[lock], LOCK_TEXT[(lock + 1) % 3].lower())
                    if r.get("tip") != tip: r["tip"] = tip; Kit.with_tip(r["lock"], tip)
                if tips_on:
                    tp = tip_for(i)
                    ct = r["tip0"] if tp is None else "%s\n%s %s: %s" % (r["tip0"], SK["names"][i], tp[0], tp[1])
                    if ct != r["cat_tip"]: r["cat_tip"] = ct; Kit.with_tip(r["cat"], ct)
                if r["bar"] is not None:
                    fw = int(bar_w * min(1.0, float(val) / cap)) if cap > 0 else 0; setp(r["bar"], "Width", max(1, fw))
                    setp(r["bar"], "IsVisible", fw > 0)
                    setp(r["bar"], "Graphic", LINE_GREEN if cap and base >= cap else Kit.LINE_BLUE)
        GOTHER = {"list": None, "n": -1, "mem": []}
        def group_info(key):
            if key == "pin": return "Pinned", [i for i in range(SK["n"]) if i in marks["pins"]]
            if key == "other":
                if GOTHER["list"] is not GR["list"] or GOTHER["n"] != SK["n"]:
                    of = GR["of"]
                    GOTHER.update({"list": GR["list"], "n": SK["n"], "mem": [i for i in range(SK["n"]) if i not in of]})
                return "Other", GOTHER["mem"]
            if isinstance(key, int) and key < len(GR["list"]):
                g = GR["list"][key]; return g["name"] or "(no name)", g["members"]
            return "?", []
        def refresh_group_row(r):
            name, mem = group_info(r["key"]); m = metrics(); n = SK["n"]; cur = SK["cur"]; tr = tv = gn = 0
            for i in mem:
                if i < n:
                    c = cur[i]; tr += c[0]; tv += c[1]
                    if r["gain"] is not None: gn += sgain(i)
            room = (m["real_x"] or m["val_x"]) - m["name_x"] - 6; sig = (name, len(mem), room, tr, tv, gn)
            if r.get("gsig") == sig: return
            r["gsig"] = sig; Kit.set_text(r["lbl"], Kit.fit("%s (%d)" % (name, len(mem)), room))
            if r["real"] is not None: Kit.set_text(r["real"], f1(tr))
            Kit.set_text(r["val"], f1(tv))
            if r["gain"] is not None: Kit.set_text(r["gain"], ("%+.1f" % (gn / 10.0)) if gn else "")
        def refresh_header():
            c = win["c"]; hdr = c.get("hdr")
            if not hdr: return
            m = metrics(); s = settings["sort"]; hk = (s, settings["asc"], m); old = c.get("hdr_k")
            if old is not None and old[0] == s and old[1] == hk[1] and old[2] is m: return
            c["hdr_k"] = hk
            names = {"name": ("Skill", m["name_x"]), "real": ("Real", m["real_x"]),
                     "value": ("Value", m["val_x"]), "cap": ("Cap", m["cap_x"]), "gain": ("Gain", m["gain_x"])}
            for key, lbl in hdr.items():
                if key != "lock_pic": Kit.set_text(lbl, names[key][0], Kit.HUE_TITLE if key == s else Kit.HUE_INFO)
            arrow = c.get("arrow")
            if arrow is None: return
            sx = c["sa_xy"][0]
            if s == "lock": ax = sx + m["lock_x"] - m["arrow_w"] - 3
            elif names.get(s, (None, None))[1] is not None: text, cx = names[s]; ax = sx + cx + Kit.text_w(text) + 3
            else: setp(arrow, "IsVisible", False); return
            y0 = c["sa_xy"][1] - 26; setp(arrow, "Pos", (ax, y0 + 8))
            setp(arrow, "Graphic", LOCK_ART[0] if settings["asc"] else LOCK_ART[1]); setp(arrow, "IsVisible", True)
        LOGTXT = {}
        def refresh(now):
            c = win["c"]
            if not c: return
            tr = total_real()
            if c.get("mini") is not None:
                if st["docked"]: return
                txt = "%s: %s / %s %+.1f" % (TITLE, f1(tr), f1(settings["total_cap"]), total_gain() / 10.0)
                if not st["ready"]: txt = "%s: waiting for your skills" % TITLE
                Kit.set_text(c["mini"], Kit.fit(txt, MINI_W - 90),
                             Kit.HUE_BAD if settings["cap_warn"] and st["warned_cap"] else Kit.HUE_INFO)
                return
            refresh_header(); refresh_rows(now); place_selbox(); IWt = win.get("w", 400) - 2 * Kit.MARGIN - 24
            if c.get("total") is not None:
                tv = sum(x[1] for x in SK["cur"]); free = settings["total_cap"] - tr
                if st["warned_cap"]:
                    a = "Total %s / %s: at the cap" % (f1(tr), f1(settings["total_cap"]))
                    b, sep = "set a skill to go down", ", "; hue = Kit.HUE_BAD
                else:
                    a = "Total %s / %s   (%s free)" % (f1(tr), f1(settings["total_cap"]), f1(max(0, free)))
                    b, sep = "with bonuses %s" % f1(tv), "   "; hue = Kit.HUE_TEXT
                txt = a + sep + b
                if c.get("total2") is not None:
                    sa, sb = Kit.fit(a, IWt), Kit.fit(b, IWt); Kit.set_text(c["total"], sa, hue)
                    Kit.set_text(c["total2"], sb, hue)
                    tip = TOTAL_TIP if (sa, sb) == (a, b) else "%s. %s" % (txt, TOTAL_TIP)
                    if tip != c.get("total_tip"): c["total_tip"] = tip; Kit.with_tip(c["total_cat"], tip)
                else: fit_set(c, "total", txt, IWt, hue, TOTAL_TIP)
            if c.get("session") is not None:
                tg = total_gain(); hrs = hours_running()
                txt = "Session %+.1f in %s   (%.1f / hour)" % (tg / 10.0, dur(now - sess["start"]), tg / 10.0 / hrs)
                fit_set(c, "session", txt, c["session_w"], Kit.HUE_GOOD if tg > 0 else Kit.HUE_INFO)
            if c.get("stats"):
                base = sess["stats"] or STATS["cur"]; hrs = hours_running()
                cats, tips = c.get("stat_cats") or (), c.get("stat_tips")
                for k, (lbl, pic) in enumerate(c["stats"]):
                    v = STATS["cur"][k]; d = v - base[k] if sess["stats"] else 0
                    Kit.set_text(lbl, "%s %d%s" % (("Str", "Dex", "Int")[k], v, (" (%+d)" % d) if d else ""),
                                 Kit.HUE_GOOD if d > 0 else Kit.HUE_TEXT)
                    setp(pic, "Graphic", LOCK_ART[STATS["locks"][k]])
                    if k < len(cats):
                        tip = stat_tip(k, hrs)
                        if tip != tips[k]: tips[k] = tip; Kit.with_tip(cats[k], tip)
                tot = sum(STATS["cur"]); cap = STATS["cap"]
                txt = ("Stats %d / %d" % (tot, cap)) if cap else ("Stats %d" % tot)
                tg = (stat_gain(0) + stat_gain(1) + stat_gain(2)) if sess["stats"] else 0
                if tg:
                    more = "%s   %+d (%.1f / hour)" % (txt, tg, tg / hrs)
                    if Kit.text_px(more) <= c["stat_total_w"]: txt = more
                fit_set(c, "stat_total", txt, c["stat_total_w"], Kit.HUE_GOOD if cap and tot >= cap else Kit.HUE_INFO)
            refresh_detail(now)
            if c.get("log") is not None:
                lines = st["log"][-len(c["log"]):][::-1]
                for k, lbl in enumerate(c["log"]):
                    if k < len(lines):
                        e = lines[k]; d = e[2]; txt = LOGTXT.get(e)
                        if txt is None:
                            t, name, _g, nb = e
                            txt = "%s  %s %s%s  (%s)" % (time.strftime("%H:%M", time.localtime(t)),
                                                         name, "+" if d > 0 else "-", f1(abs(d)), f1(nb))
                            if len(LOGTXT) >= 2 * LOG_KEEP: LOGTXT.clear()
                            LOGTXT[e] = txt
                        fit_set(c, "log%d" % k, txt, c["log_w"], Kit.HUE_GOOD if d > 0 else Kit.HUE_BAD, lbl=lbl)
                    else:
                        fit_set(c, "log%d" % k, "No gains yet this session." if k == 0 and not lines
                                else "", c["log_w"], Kit.HUE_INFO, lbl=lbl)
        def refresh_detail(now):
            c = win["c"]
            if c.get("d_name") is None: return
            i = st["sel"]
            if i is None or i >= SK["n"]:
                fit_set(c, "d_name", "No skill picked", c["d_name_w"])
                fit_set(c, "d_l1", "Click a skill in the list to see it here.", c["d_lw"], Kit.HUE_INFO)
                fit_set(c, "d_l2", "", c["d_lw"]); fit_set(c, "d_tgt", "", c["d_tgt_w"])
                if c.get("d_tip") is not None:
                    Kit.set_text(c["d_tip"], "")
                    if c["d_tip_full"] is not None:
                        c["d_tip_full"] = None; Kit.with_tip(c["d_tip_cat"], "Training tip for this skill's range")
                for p in c["d_locks"]: setp(p, "Hue", DIM_HUE)
                return
            base, val, cap, lock = SK["cur"][i]; gi = group_of(i)
            gname = GR["list"][gi]["name"] if gi is not None else ""
            fit_set(c, "d_name", SK["names"][i] + ("   (%s)" % gname if gname else ""), c["d_name_w"], Kit.HUE_TITLE)
            for v, p in enumerate(c["d_locks"]): setp(p, "Hue", 0 if v == lock else DIM_HUE)
            bonus = val - base
            l1 = "Real %s   Value %s%s   Cap %s   %s" % (
                f1(base), f1(val), (" (%+.1f)" % (bonus / 10.0)) if bonus else "", f1(cap),
                ("To cap %s" % f1(cap - base)) if base < cap else "At cap")
            fit_set(c, "d_l1", l1, c["d_lw"], Kit.HUE_TEXT); rt = rates(i, now); avg, recent = rt
            l2 = "Session %+.1f   %.1f / hour   last %d min %.1f / hour   cap %s" % (
                sgain(i) / 10.0, avg / 10.0, settings["rate_min"], recent / 10.0, eta(i, now, rt))
            fit_set(c, "d_l2", l2, c["d_lw"], Kit.HUE_INFO)
            if c.get("d_tip") is not None:
                tp = tip_for(i)
                if tp is not None: full, hue = "Tip %s: %s" % tp, Kit.HUE_TEXT
                else: full, hue = "No tip for this range", Kit.HUE_INFO
                Kit.set_text(c["d_tip"], Kit.fit(full, c["d_lw"]), hue)
                if full != c["d_tip_full"]: c["d_tip_full"] = full; Kit.with_tip(c["d_tip_cat"], full)
            tgt = marks["targets"].get(i)
            if tgt:
                if base >= tgt: txt, hue = "reached", Kit.HUE_GOOD
                else:
                    txt = "%s to go%s" % (f1(tgt - base), ", then locks" if settings["lock_at_target"] else "")
                    hue = Kit.HUE_INFO
            else: txt, hue = "none set", Kit.HUE_INFO
            fit_set(c, "d_tgt", txt, c["d_tgt_w"], hue)
            if c.get("pin") is not None: Kit.set_text(c["pin"], "Unpin" if i in marks["pins"] else "Pin")
        def show_target_text():
            c = win["c"]; tb = c.get("target")
            if tb is None: st["tgt_shown"] = None; return
            i = st["sel"]; txt = f1(marks["targets"][i]) if i is not None and i in marks["targets"] else ""
            tb.SetText(txt); st["tgt_shown"] = (i, txt)
        def poll_fields(now):
            c = win["c"]; moved = False; sb = c.get("search")
            if sb is not None:
                try: q = str(sb.Text or "").strip().lower()
                except Exception: q = st["search"]
                if q != st["search"]: st["search"], moved = q, True
            tb = c.get("target")
            if tb is not None and st["tgt_shown"] is not None:
                i, shown = st["tgt_shown"]
                try: txt = str(tb.Text or "").strip()
                except Exception: txt = shown
                if txt != shown and i is not None and i == st["sel"]:
                    st["tgt_shown"] = (i, txt)
                    try: v = int(round(float(txt.replace(",", ".")) * 10)) if txt else 0
                    except (ValueError, OverflowError): v = None
                    if v is not None:
                        v = max(0, min(2000, v))
                        if v: marks["targets"][i] = v
                        else: marks["targets"].pop(i, None)
                        save_marks(); moved = True
            cb = c.get("groups")
            if cb is not None:
                try: on = bool(cb.IsChecked)
                except Exception: on = settings["groups"]
                if on != settings["groups"]:
                    settings["groups"] = on; save_settings()
                    if on: read_groups(True)
                    moved = True
            return moved
        def gumps_sig():
            try:
                lst = VG["gumps"]
                if lst is None: lst = VG["gumps"] = Tz.get(None, "Gumps", Tz.T("ClassicUO.Game.Managers.UIManager"))
                return (int(lst.Count), lst.First)
            except Exception: VG["gumps"] = None; return None
        VANILLA_FULL_EVERY = 3.0
        def vanilla_check():
            if not settings["replace"] and time.time() > st["swallow_until"]: return
            now = time.time(); sig = gumps_sig()
            if sig is not None and sig == VG["sig"] and now < VG["full_at"]: return
            VG["sig"], VG["full_at"] = sig, now + VANILLA_FULL_EVERY; VG["gumps"] = None
            found = safe(lambda: Tz.windows(VANILLA), []) or []
            if not found: return
            VG["sig"] = None
            for gmp in found: gmp.Dispose()
            if time.time() <= st["swallow_until"]: st["swallow_until"] = 0.0; return
            bring_up()
        def bring_up():
            if st["hidden"] or st["minimized"] or st["docked"] or not Kit.is_open(win["g"]):
                st["hidden"] = st["minimized"] = st["docked"] = False; settings["minimized"] = False; save_settings()
                build_window()
            else:
                ctl = Kit.client_control(win["g"])
                if ctl is not None: Tz.call(None, "MakeTopMostGump", [ctl], Tz.T("ClassicUO.Game.Managers.UIManager"))
        def armed(key, text):
            now = time.time()
            if now - st["arm"].get(key, 0.0) <= ARM_SECS: st["arm"].pop(key, None); return True
            st["arm"][key] = now; say(text, Kit.HUE_INFO); return False
        def bulk_lock(v, only_capped=False):
            n = 0
            for i in (range(SK["n"]) if only_capped else [d[1] for d in (st["desc"] or []) if d[0] == "s"]):
                base, _, cap, lock = SK["cur"][i]
                if only_capped and not (cap and base >= cap): continue
                if lock != v: set_lock(i, v); n += 1
            say("%s %s." % (Kit.count(n, "skill"), ("set to go up", "set to go down", "locked")[v]),
                       Kit.HUE_GOOD if n else Kit.HUE_INFO)
        def apply_lockset(k):
            if k >= len(locksets): return
            name, code = locksets[k]; n = 0
            for i, ch in enumerate(code[:SK["n"]]):
                v = "udl".find(ch)
                if v >= 0 and SK["cur"][i][3] != v: set_lock(i, v); n += 1
            say("lock set \"%s\" put on (%d change%s)." % (name, n, "" if n == 1 else "s"), Kit.HUE_GOOD)
        def save_lockset(name):
            name = re.sub(r"[|=;]", "", name or "").strip()[:24]
            if not name: name = "Set %d" % (len(locksets) + 1)
            code = "".join("udl"[c[3]] for c in SK["cur"])
            for k, (n, _) in enumerate(locksets):
                if n.lower() == name.lower(): locksets[k] = (name, code); break
            else:
                if len(locksets) >= MAX_LOCKSETS:
                    say("at most %d lock sets: delete one first." % MAX_LOCKSETS, Kit.HUE_BAD); return
                locksets.append((name, code))
            save_locksets(); say("lock set \"%s\" saved." % name, Kit.HUE_GOOD)
        def move_to_next_group(i):
            read_groups(True)
            if i is None or not GR["list"]:
                say("couldn't move the skill (the client's skill groups can't be read).", Kit.HUE_BAD); return
            gi = group_of(i); dst = 0 if gi is None else (gi + 1) % len(GR["list"])
            try:
                import System
                if gi is not None: GR["list"][gi]["obj"].Remove(System.Byte(i))
                GR["list"][dst]["obj"].Add(System.Byte(i)); groups_save()
                say("%s moved to %s." % (SK["names"][i], GR["list"][group_of(i) or 0]["name"]), Kit.HUE_GOOD)
            except Exception as ex: say("couldn't move it (%s)." % Tz.why(ex), Kit.HUE_BAD)
        def group_new():
            mgr = group_mgr()
            try:
                import System; g = System.Activator.CreateInstance(Tz.T("ClassicUO.Game.Managers.SkillsGroup"))
                g.Name = "New group"; g.IsMaximized = True; mgr.Add(g); groups_save()
            except Exception as ex: say("couldn't add a group (%s)." % Tz.why(ex), Kit.HUE_BAD)
        def group_delete(gi):
            read_groups(True)
            if gi <= 0 or gi >= len(GR["list"]): return
            mgr = group_mgr(); name = GR["list"][gi]["name"]
            if safe(lambda: mgr.Remove(GR["list"][gi]["obj"]), False):
                groups_save()
                say("group \"%s\" deleted; its skills went to \"%s\"." % (
                    name, GR["list"][0]["name"] if GR["list"] else "the first group"), Kit.HUE_GOOD)
        def group_reset():
            mgr = group_mgr()
            try:
                mgr.MakeDefault(); groups_save()
                say("skill groups reset to the default ones.", Kit.HUE_GOOD)
            except Exception as ex: say("couldn't reset the groups (%s)." % Tz.why(ex), Kit.HUE_BAD)
        def export_sheet():
            p = API.Player; path = Kit.data_path("Skills_%08X.txt" % int(p.Serial)); now = time.time()
            lines = ["Skill sheet - %s - %s" % (p.Name or "", time.strftime("%Y-%m-%d %H:%M", time.localtime(now))),
                     "Total %s / %s   (with bonuses %s)" % (f1(total_real()), f1(settings["total_cap"]),
                         f1(sum(x[1] for x in SK["cur"]))), "Str %d  Dex %d  Int %d   (stat cap %d)" % (
                         STATS["cur"][0], STATS["cur"][1], STATS["cur"][2], STATS["cap"]),
                     "Session %+.1f in %s" % (total_gain() / 10.0, dur(now - sess["start"])), "",
                     "%-26s %7s %7s %7s %8s  %s" % ("Skill", "Real", "Value", "Cap", "Session", "Lock")]
            for i in sorted(range(SK["n"]), key=lambda i: SK["names"][i].lower()):
                b, v, cp, lk = SK["cur"][i]; gn = sgain(i)
                lines.append("%-26s %7s %7s %7s %8s  %s" % (
                    SK["names"][i], f1(b), f1(v), f1(cp), ("%+.1f" % (gn / 10.0)) if gn else "", LOCK_WORD[lk]))
            st["to_write"].append((path, "\n".join(lines) + "\n"))
        def write_files(): write_queue(st["to_write"], TITLE, "skill sheet")
        def _thread_wanted(): return bool(st["to_write"])
        def pick(i):
            if st["sel"] != i:
                st["sel"] = i; show_target_text()
                if settings["sec_detail"]: read_groups(GR["sig"] is None)
            place_selbox()
        def picked(i):
            if i is None: say("pick a skill first.", Kit.HUE_INFO)
            return i is not None
        def action_parts(a):
            if not isinstance(a, tuple): return a, None
            return a[0], a[1] if len(a) > 1 else None
        def toggle_min(arg):
            st["minimized"] = not (st["minimized"] or st["docked"]); st["docked"] = False
            safe(lambda: HOST.dock_forget(KEY)); settings["minimized"] = st["minimized"]; save_settings()
            st["rebuild"] = "window"
        def cycle_filter(arg):
            settings["filter"] = (settings["filter"] + 1) % len(FILTERS); save_settings()
            lbl = win["c"].get("filter")
            if lbl is not None: Kit.set_text(lbl, FILTERS[settings["filter"]][1])
        def sort_by(arg):
            if settings["sort"] == arg: settings["asc"] = not settings["asc"]
            else: settings["sort"] = arg; settings["asc"] = arg == "name"
            save_settings()
        def use_action(arg):
            i = arg if arg is not None else st["sel"]
            if picked(i): use_skill(i)
        def fold_row(arg):
            if not isinstance(arg, int): st["pc"][arg] = not st["pc"].get(arg, False)
            elif arg < len(GR["list"]): g = GR["list"][arg]; g["obj"].IsMaximized = g["max"] = not g["max"]
        def pin_skill(arg):
            sel = st["sel"]
            if picked(sel): marks["pins"] ^= {sel}; save_marks()
        def ask_skills(arg):
            if ask_server(): say("asked the server for your skills.", Kit.HUE_INFO)
            else: say("couldn't ask the server (the client's skills call failed).", Kit.HUE_BAD)
        def lockset_delete(arg):
            if arg < len(locksets):
                n = locksets.pop(arg)[0]; save_locksets(); say("lock set \"%s\" deleted." % n, Kit.HUE_INFO)
            HOST.refresh_settings(KEY)
        def reset_groups(arg):
            if armed("grp_reset", "click Reset groups again for the default groups."):
                group_reset(); HOST.refresh_settings(KEY)
        ACTIONS = {"settings": lambda arg: HOST.show_settings(KEY), "to_bar": lambda arg: HOST.dock_to_bar(KEY, TITLE),
                   "pick": pick, "stat": lambda arg: set_stat_lock(arg, (STATS["locks"][arg] + 1) % 3),
                   "all_up": lambda arg: bulk_lock(0), "all_locked": lambda arg: bulk_lock(2),
                   "lock_capped": lambda arg: bulk_lock(2, True), "export": lambda arg: export_sheet(),
                   "ls_save": lambda arg: (save_lockset(arg), HOST.refresh_settings(KEY)), "ls_apply": apply_lockset,
                   "grp_new": lambda arg: (group_new(), HOST.refresh_settings(KEY)),
                   "grp_del": lambda arg: (group_delete(arg), HOST.refresh_settings(KEY)),
                   "grp_save": lambda arg: groups_save(), "toggle_min": toggle_min, "filter": cycle_filter,
                   "sort": sort_by, "button": lambda arg: (pick(arg), make_button(arg)),
                   "mkbutton": lambda arg: picked(st["sel"]) and make_button(st["sel"]), "use": use_action,
                   "lock": lambda arg: arg is not None and arg < SK["n"] and set_lock(arg, (SK["cur"][arg][3] + 1) % 3),
                   "dlock": lambda arg: st["sel"] is not None and set_lock(st["sel"], arg), "fold": fold_row,
                   "pin": pin_skill, "nextgrp": lambda arg: picked(st["sel"]) and move_to_next_group(st["sel"]),
                   "all_down": lambda arg: armed("all_down",
                                                 "click All down again to set every listed skill to go down.")
                   and bulk_lock(1),
                   "newsess": lambda arg: (new_session(), say("new session; gains count from now.", Kit.HUE_GOOD)),
                   "ask": ask_skills, "ls_del": lockset_delete, "grp_reset": reset_groups}
        MAIN_CHECKS = [("replace", "Replace the client's skills window",
             "The paperdoll's Skills button, the Skills macro and the Action Bar open this one"),
            ("x_hides", "Close only hides it", "Off: Close turns Skills off"),
            ("bars", "Progress bar per skill (value / cap)", "Filled to value / cap; green at the cap"),
            ("col_cap", "Cap column", "Each skill's cap"), ("col_gain", "Session gain column",
             "What each skill gained this session"),
            ("journal", "Journal line for each gain or loss", "The client may print its own line too (its Options)"),
            ("lock_at_cap", "Lock a skill when it reaches its cap", "A rising skill locks the moment it hits its cap"),
            ("lock_at_target", "Lock a skill when it reaches its target", "Set targets in the window's details"),
            ("cap_warn", "Warn at the total cap when no skill is set to go down",
             "Journal warning and a red total when nothing can rise"),
            ("tips", "Training tips in the details and row tooltips", "Classic-era advice for the skill's range")]
        NUM_FIELDS = [("rows", "Rows in the list:", False, "Skills shown at once (or drag a window corner)"),
                      ("total_cap", "Total skill cap:", True, "The shard's total skill cap (check it in game)"),
                      ("hl_secs", "Green name after a gain (s):", False,
                       "Seconds a name stays green after a gain (0 = never)"),
                      ("rate_min", "Recent pace over (minutes):", False,
                       "Minutes the recent rate and time to cap look back")]
        SEC_CHECKS = [("sec_summary", "Totals and session", "Total skill points and the session line"),
                      ("sec_stats", "Str / Dex / Int", "Stats, lock arrows and the stat cap"),
                      ("sec_locks", "Lock buttons", "All up, All down, All locked and Lock capped"),
                      ("sec_detail", "Picked skill details", "Rates, target, pin and the Use button"),
                      ("sec_log", "Recent gains", "The last gains, newest first")]
        TOOLS_HINT = "Export writes a text file to the VirtueAssistantSettings folder."
        SIZE_HINT = "Drag a window corner: height sets the rows, width spreads the columns."
        STAT_HINT = ("A stat set to go up locks when it rises to its target, one set to go down when it falls to it. "
                     "The window's stat tooltips show gains per hour.")
        def page_table(w):
            read_groups(GR["sig"] is None); ng = len(GR["list"]) if GR["ok"] else 1; half = (w - 24) // 2
            def hint(text, dy): return [("note", line, {"ndy": dy, "h": 18}) for line in Kit.wrap(text, w - 24)]
            def num_field(k, text, dec, tip):
                def draw(f, x, ry):
                    g = f.g; c = f.c; lx = x + 12 + max(Kit.text_w(t) for _, t, _, _ in NUM_FIELDS) + 10
                    Kit.add_label(g, text, x + 12, ry + 3); val = f1(settings[k]) if dec else str(settings[k])
                    c.setdefault("num", {})[k] = Kit.with_tip(Kit.add_textbox(g, val, lx, ry, 70, numbers=not dec), tip)
                    lo, hi = LIMITS[k]; rng = ("(%s-%s)" % (f1(lo), f1(hi))) if dec else ("(%d-%d)" % (lo, hi))
                    Kit.add_label(g, Kit.fit(rng, x + w - 4 - (lx + 84)), lx + 84, ry + 3, Kit.HUE_INFO)
                    if k == "rows":
                        wx = lx + 84 + Kit.text_w(rng) + 16
                        c["width_v"] = Kit.add_label(g, Kit.fit(width_text(), x + w - 4 - wx), wx, ry + 3, Kit.HUE_INFO)
                        Kit.catcher(g, wx - 2, ry, x + w - 4 - wx, 22, lambda: None,
                                    "Window width, set by dragging a corner (natural: as wide as the columns need)")
                return ("custom", 28, draw)
            def stat_targets(f, x, ry):
                sx = x + 12; c = f.c; c["stat_tgt"] = []
                for k, nm in enumerate(("Str", "Dex", "Int")):
                    Kit.add_label(f.g, nm + ":", sx, ry + 3); tx = sx + Kit.text_w(nm + ":") + 8
                    shown = str(stat_tgt[k]) if stat_tgt[k] else ""
                    tb = Kit.with_tip(Kit.add_textbox(f.g, shown, tx, ry, 44, numbers=True),
                                      "%s target (1-%d, empty = none)" % (STAT_NAMES[k], STAT_TARGET_MAX))
                    c["stat_tgt"].append([tb, shown, shown, 0.0]); sx = tx + 44 + 24
            def lock_sets(f, x, ry):
                g, store = f.g, f.store; Kit.add_label(g, "Name:", x + 12, ry + 3)
                nx = x + 12 + Kit.text_w("Name:") + 8; sx = x + w - 12 - cap_w("Save current")
                f.c["ls_name"] = Kit.with_tip(Kit.add_textbox(g, "", nx, ry, max(60, sx - nx - 14), numbers=False),
                                              "Name for Save current (empty = Set 1, Set 2 and so on)")
                Kit.art_button(g, store, "ls_save", Kit.ART_OK, sx, ry - 1, "Save current",
                               "Save every skill's lock as a set (same name replaces it)")
                ry += 28
                if not locksets:
                    Kit.add_label(g, "No lock sets yet. Type a name and click Save current.", x + 12, ry + 3,
                                  Kit.HUE_INFO)
                dx = x + w - 12 - cap_w("Delete"); ax = dx - 12 - cap_w("Apply")
                for k, (name, code) in enumerate(locksets):
                    ups, downs = code.count("u"), code.count("d")
                    Kit.add_label(g, Kit.fit("%s  (%d up, %d down)" % (name, ups, downs), ax - x - 24), x + 12, ry + 3)
                    Kit.art_button(g, store, "ls_apply_%d" % k, Kit.ART_OK, ax, ry - 1, "Apply",
                                   "Put this set's locks on your skills")
                    Kit.art_button(g, store, "ls_del_%d" % k, Kit.ART_CLOSE, dx, ry - 1, "Delete",
                                   "Delete this lock set")
                    ry += 26
            def groups(f, x, ry):
                g, store = f.g, f.store; dx = x + w - 12 - cap_w("Delete"); f.c["grp"] = []
                if not GR["ok"]:
                    Kit.add_label(g, "The client's skill groups can't be read.", x + 12, ry + 3, Kit.HUE_BAD); ry += 28
                for gi, gr in enumerate(GR["list"]):
                    tb = Kit.with_tip(Kit.add_textbox(g, gr["name"], x + 12, ry, 200, numbers=False),
                                      "Group name (type to rename)")
                    Kit.add_label(g, Kit.count(len(gr["members"]), "skill"), x + 226, ry + 3, Kit.HUE_INFO)
                    if gi > 0:
                        Kit.art_button(g, store, "grp_del_%d" % gi, Kit.ART_CLOSE, dx, ry - 1,
                                       "Delete", "Delete this group (its skills go to the first one)")
                    else: Kit.add_label(g, "first group", dx + 35, ry + 3, Kit.HUE_INFO)
                    f.c["grp"].append((tb, gi, gr["name"])); ry += 28
                if GR["ok"] and not GR["list"]: ry += 28
                Kit.art_button(g, store, "grp_new", Kit.ART_OK, x + 12, ry - 1, "New group",
                               "Add an empty group (Next group in the window moves skills in)")
                Kit.art_button(g, store, "grp_reset", Kit.ART_CLOSE, x + 12 + cap_w("New group") + 16,
                               ry - 1, "Reset groups", "Put back the client's default groups (click twice)")
            lo, hi = LIMITS["log_lines"]; sec = {"ch": 24, "pad": 6}
            return (("WINDOW", [("check",) + r for r in MAIN_CHECKS] + [num_field(*r) for r in NUM_FIELDS] +
                     hint(SIZE_HINT, 2), sec),
                    ("SECTIONS  (what the window shows)", [("check",) + r + ({"stay": n % 2 == 0 and n < 4,
                     "dx": 12 + (n % 2) * half},) for n, r in enumerate(SEC_CHECKS)] + [("num", "log_lines",
                     "Recent gains lines:", "Lines the Recent gains part shows (%d-%d)" % (lo, hi), None, lo, hi)],
                     sec), ("STAT TARGETS", [("custom", 28, stat_targets),
                     ("check", "lock_stat_target", "Lock a stat when it reaches its target",
                      "Off: only a journal line when it gets there")] + hint(STAT_HINT, 2), sec),
                    ("LOCK SETS  (saved locks)", (("custom", 28 + max(1, len(locksets)) * 26, lock_sets),), sec),
                    ("GROUPS  (the client's skill groups)", (("custom", max(1, ng) * 28 + 28, groups),), sec),
                    ("TOOLS", [("buttons", (("export", Kit.ART_PLAY, "Export sheet", "Write every skill's values to a "
                                             "file in the VirtueAssistantSettings folder"),
                                            ("ask", Kit.ART_PLAY, "Ask server",
                                             "Ask the server for fresh skill values"),
                                            ("newsess", Kit.ART_PLAY, "New session",
                                             "Start a new session: gains count from now")))] + hint(TOOLS_HINT, 0),
                     dict(sec, bdy=-1, bgap=16)))
        def width_text():
            if settings["width"]: return "Width: %d px (drag a corner)" % settings["width"]
            return "Width: natural (drag a corner)"
        def read_num(ctrl, default, lo, hi, dec):
            try: txt = str(ctrl.Text or "").strip()
            except Exception: txt = ""
            try: v = int(round(float(txt.replace(",", ".")) * 10)) if dec else int(txt); return max(lo, min(hi, v))
            except (ValueError, OverflowError): return default
        def page_clicks(f):
            c = f.c; page["skip"] = page["sync"]
            if page["sync"]:
                page["sync"] = False; tb = c["num"].get("rows")
                if tb is not None: tb.SetText(str(settings["rows"]))
                if c.get("width_v") is not None: Kit.set_text(c["width_v"], width_text())
                return
            poll_stat_targets(c, False)
            for tb, gi, shown in list(c.get("grp", ())):
                try: txt = str(tb.Text or "")
                except Exception: txt = str(shown or "")
                if txt != shown and gi < len(GR["list"]):
                    GR["list"][gi]["obj"].Name = GR["list"][gi]["name"] = txt; touch()
                    c["grp"] = [(t, g2, txt if g2 == gi else s) for t, g2, s in c["grp"]]
                    st["grp_dirty_at"] = time.time()
            store = f.store
            for key in list(store[0].keys()):
                if not Kit.was_clicked(store, key): continue
                if key == "ls_save": queue.add(("ls_save", str(c["ls_name"].Text or "")), dup=True)
                elif key.startswith(("ls_apply_", "ls_del_", "grp_del_")):
                    kind, _, n = key.rpartition("_"); queue.add((kind, int(n)), dup=True)
                else: queue.add((key,), dup=True)
                HOST.poke()
        def page_adjust(f, new):
            if page["skip"]: new.update(settings); return
            for k, ctrl in f.c["num"].items():
                lo, hi = LIMITS[k]; new[k] = read_num(ctrl, settings[k], lo, hi, k == "total_cap")
        def page_changed(old, new):
            touch()
            if any(new[k] != old[k] for k in LAYOUT_KEYS): st["m"] = None; st["rebuild"] = "window"
            st["warned_cap"] = False; st["cap_at"] = 0.0
        cfg = Kit.Page(settings, page_table, save_settings, page_changed, adjust=page_adjust, clicks=page_clicks)
        STAT_SETTLE = 0.8
        def poll_stat_targets(c, final):
            now = time.time()
            for k, e in enumerate(c.get("stat_tgt") or ()):
                if final: txt = e[2]
                else:
                    try: txt = str(e[0].Text or "").strip()
                    except Exception: continue
                    if txt != e[2]: e[2], e[3] = txt, now; continue
                if txt == e[1] or (not final and now - e[3] < STAT_SETTLE): continue
                e[1] = txt
                if txt and not txt.isdigit(): continue
                v = max(0, min(STAT_TARGET_MAX, int(txt))) if txt else 0
                if v != stat_tgt[k]:
                    stat_tgt[k] = v; Kit.put_var(STAT_TARGETS_KEY, ",".join(str(t) for t in stat_tgt)); touch()
                    stat_at_target(k)
        def config_closed():
            if cfg.f is not None: poll_stat_targets(cfg.f.c, True)
            cfg.closed(); page["sync"] = False
            if st.get("grp_dirty_at"): st["grp_dirty_at"] = 0.0; queue.add(("grp_save",), dup=True)
        def set_ready():
            st["ready"] = True
            for i in range(SK["n"]): sess["base"].setdefault(i, SK["cur"][i][0])
            if sess["stats"] is None and any(STATS["cur"]): sess["stats"] = list(STATS["cur"])
        def drop_window():
            g, win["g"] = win["g"], None; win.update({"c": {}, "rows": [], "rowmap": {}}); UIC.clear(); Kit.dispose(g)
        load_settings(); load_stat_targets()
        def _start():
            st.update({"shutting": False, "docked": False, "hidden": False, "queue": [],
                       "rebuild": None, "desc": None, "m": None, "ready": False,
                       "asked": 0.0, "swallow_until": 0.0, "warned_cap": False, "hl": {},
                       "log": [], "gains": {}, "started": time.time(), "ref_at": 0.0,
                       "grp_at": 0.0, "tgt_shown": None, "stat_pending": {}, "dirty": True,
                       "redraw_at": 0.0, "desc_key": None, "cap_at": 0.0, "resize_at": 0.0, "grp_dirty_at": 0.0,
                       "read_at": 0.0, "stats_at": 0.0})
            VG.update({"gumps": None, "sig": None, "full_at": 0.0}); load_settings(); load_marks(); load_locksets()
            load_stat_targets(); load_session()
            st["minimized"] = settings["minimized"] or HOST.dock_wanted(KEY)
            refresh_refs(True); read_skills(); read_stats(); read_groups(True)
            if skills_loaded(): set_ready()
            fitst.update({"width": None, "rows": None, "slot": None, "k": 1.0, "full": None}); build_window()
            show_target_text()
            HOST.dock_add(KEY, dict(hooks, on=bring_up, show=bring_up, fit=layout_fit, exact=True, verify=True,
                                    drawn_at=drawn_at))
            if settings["replace"]: vanilla_check()
        def _tick():
            now = time.time()
            if win["g"] is not None and Kit.was_clicked(win["store"], "close"):
                if settings["x_hides"]:
                    st["hidden"] = True; save_pos(); drop_window()
                    say("hidden; %s brings it back."
                        % ("the client's or the Action Bar's Skills button" if settings["replace"] else
                        "the Action Bar's Skills button (or Skills off and on in the Modules tab)"), Kit.HUE_INFO)
                else: Kit.dispose(win["g"]); return
            if st["resize_at"] and now - st["resize_at"] >= RESIZE_SETTLE and not safe(lambda: SNAP.pressed(), False):
                st["resize_at"] = 0.0; apply_resize()
            if st["grp_dirty_at"] and now - st["grp_dirty_at"] >= GRP_SETTLE: st["grp_dirty_at"] = 0.0; groups_save()
            had = SK["n"]
            if not refresh_refs():
                while st["queue"]:
                    kind, arg = action_parts(st["queue"].pop(0)); fn = ACTIONS.get(kind)
                    if fn is not None: fn(arg)
                vanilla_check()
                if st["rebuild"] == "window": build_window()
                elif win["g"] is not None and win["c"] and st["desc"] is None: rebuild_rows(now)
                return
            if SK["n"] != had: st["rebuild"] = "window"
            changed, stats_moved = {}, False
            if not (st["ready"] and (win["g"] is None or not win["c"] or st["minimized"] or st["docked"])
                    and now < st["read_at"]):
                st["read_at"] = now + HIDDEN_READ; changed = read_skills(not st["ready"])
                if st["stat_pending"] or now >= st["stats_at"] or not st["ready"]:
                    st["stats_at"] = now + STATS_EVERY; stats_moved = read_stats()
            if changed: list_moved()
            elif stats_moved: st["dirty"] = True
            if not st["ready"]:
                if skills_loaded(): set_ready(); save_session(); st["rebuild"] = st["rebuild"] or "rows"
                elif now - st["started"] > 3.0 and not st["asked"]: ask_server()
            elif changed: note_gains(changed, now)
            if stats_moved and st["ready"] and (stat_tgt[0] or stat_tgt[1] or stat_tgt[2]): note_stats()
            if st["ready"] and sess["stats"] is None and any(STATS["cur"]): sess["stats"] = list(STATS["cur"])
            read_groups(); ran = bool(st["queue"])
            if ran: touch()
            while st["queue"]:
                kind, arg = action_parts(st["queue"].pop(0)); fn = ACTIONS.get(kind)
                if fn is not None: fn(arg)
            if changed or ran or now >= st["cap_at"]:
                st["cap_at"] = now + CAP_EVERY; warned = st["warned_cap"]; cap_warning()
                if warned != st["warned_cap"]: touch()
            vanilla_check()
            if st["rebuild"] == "window":
                build_window(); st["dirty"], st["redraw_at"] = False, now + REDRAW_EVERY; return
            if win["g"] is None or not win["c"]: return
            if not (st["minimized"] or st["docked"]) and poll_fields(now): touch()
            if not st["dirty"] and now < st["redraw_at"]: return
            st["dirty"], st["redraw_at"] = False, now + REDRAW_EVERY
            if st["minimized"] or st["docked"]: refresh(now); return
            rebuild_rows(now); refresh(now)
        def _stop():
            st["shutting"] = True
            if st.get("grp_dirty_at"): st["grp_dirty_at"] = 0.0; safe(lambda: Kit.on_client(groups_save))
            write_files(); save_pos(); save_settings()
            if st["ready"]: save_session()
            HOST.dock_remove(KEY); drop_window(); cleanup.close()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": config_closed,
                "thread_tick": write_files, "thread_wanted": _thread_wanted}
    def _part_alarm():
        KEY = "attention"; TITLE = "Training Alarm"; SETTINGS_KEY = "Attention_settings"; POS_KEY = "Attention_pos"
        MIN_KEY = "Attention_min"; W = 400; MINI_W, MINI_H = 300, 46; TRAY_ICON = 0x1C12; GUMP_EVERY = 0.25
        STAFF_EVERY = 1.0; STAFF_RANGE = 18; STAFF_RECHECK = 2.0; STAFF_GONE = 60.0; HIT_EVERY = 0.25; ASKED_SECS = 1.5
        TYPED_SECS = 5.0; SAME_GUMP_SECS = 60.0
        DEFAULT_MARKERS = ("GM, Counselor, Seer, Admin, Administrator, Developer, Staff, Game Master")
        DEFAULT_IGNORE = ""; WHISPER_TYPES = ("whisper", "8"); REPEAT_DEFAULT, REPEAT_MAX = 5, 120
        HOLD_DEFAULT, HOLD_MAX = 0, 600; REASONS_MAX = 8; QUOTE_MAX = 60; FLASH_SECS = 0.5; CACHE_CAP = 500
        OPEN_IDS_CAP = 60; QUEUE_CAP = 30; NAME_EVERY = 5.0
        KINDS = (("gump", "attention.gump", "Gump nobody asked for", 0x307),
                 ("staff", "attention.staff", "Staff in view", 0x307),
                 ("name", "attention.name", "Someone says your name", 0x338),
                 ("whisper", "attention.whisper", "A whisper to you", 0x338),
                 ("hit", "attention.hit", "Hit while not fighting", 0x1F1),
                 ("test", "attention.test", "Training Alarm test", 0x307))
        ALERT_KEY = dict((k, a) for k, a, _, _ in KINDS)
        TRIGGERS = ("gump", "staff", "name", "words", "whisper", "hit")
        settings = {"gump": True, "staff": True, "name": True, "words": True, "whisper": True,
                    "hit": False, "markers": DEFAULT_MARKERS, "ignore": DEFAULT_IGNORE,
                    "repeat": REPEAT_DEFAULT, "hold": HOLD_DEFAULT, "anyalarm": True}
        DEFAULTS = dict(settings)
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "open_ids": {}, "last_gid": 0,
              "me": 0, "my_name": "", "name_re": None, "words_re": None, "seq": 0}
        win = {"g": None, "c": {}, "store": ({}, {})}; page = {"skip": False}; hooks = {"done": False}
        cleanup = Kit.Cleanup(); queue = Kit.queuer(st); say = Kit.sayer(TITLE)
        mouse = {"looked": False, "get": None}
        rx = {"markers": None, "text": None, "ignore": frozenset(), "ignore_text": None}
        def _clean(text): return str(text or "").replace(";", ",").replace("=", " ").strip()
        def load_settings():
            for k, v in Kit.codec_load(Kit.get_var(SETTINGS_KEY)).items():
                if k in TRIGGERS or k == "anyalarm": settings[k] = v == "1"
                elif k in ("repeat", "hold"):
                    try: settings[k] = max(0, min(REPEAT_MAX if k == "repeat" else HOLD_MAX, int(v)))
                    except ValueError: continue
                elif k in ("markers", "ignore"): settings[k] = v
        def save_settings():
            parts = ["%s=%d" % (k, 1 if settings[k] else 0) for k in TRIGGERS + ("anyalarm",)]
            parts += ["repeat=%d" % settings["repeat"], "hold=%d" % settings["hold"],
                      "markers=%s" % _clean(settings["markers"]), "ignore=%s" % _clean(settings["ignore"])]
            Kit.put_var(SETTINGS_KEY, ";".join(parts))
        def marker_re():
            text = settings["markers"]
            if rx["text"] != text:
                words = [w.strip() for w in str(text or "").split(",") if w.strip()]; words.sort(key=len, reverse=True)
                rx["markers"] = re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])"
                                           % "|".join(re.escape(w) for w in words), re.IGNORECASE) if words else None
                rx["text"] = text
            return rx["markers"]
        def ignored_ids():
            text = settings["ignore"]
            if rx["ignore_text"] != text:
                ids = set()
                for w in str(text or "").replace(" ", ",").split(","):
                    w = w.strip().lower()
                    if not w: continue
                    try: ids.add(int(w, 16) if w.startswith("0x") else int(w))
                    except ValueError: continue
                rx["ignore"] = frozenset(ids); rx["ignore_text"] = text
            return rx["ignore"]
        def sound_of(kind):
            if ALERTS.mute: return 0
            on, sid = ALERTS.setting(ALERT_KEY[kind]); return sid if on else 0
        def banner_up(): return bool(ALERTS.shown and ALERTS.alarm)
        def is_up():
            if st["alarm"]: return True
            ra = st["resume_at"]
            if ra and 0 < ra - time.time() <= HOLD_MAX + 1: return True
            return bool(settings["anyalarm"] and HOST.alarm_up())
        def raise_alarm(kind, text, who=None, serial=0, gid=0, said=None):
            fresh = not st["alarm"]; again = False
            for r in st["alarm"]:
                if r["who"] == who:
                    if r["text"] == text or (said is not None and r["said"] == said): return False
                    again = True
            now = time.time()
            if fresh: st["seq"] += 1
            st["alarm"].append({"kind": kind, "text": text, "who": who, "serial": int(serial or 0),
                                "gid": int(gid or 0), "at": now, "said": said})
            if len(st["alarm"]) > REASONS_MAX: del st["alarm"][:-REASONS_MAX]
            st["resume_at"] = 0.0
            if fresh:
                st["banner_seen"] = False; rep = settings["repeat"]; st["next_sound"] = now + rep if rep > 0 else 0.0
            if again: refresh(); return True
            HOST.alert(ALERT_KEY[kind], text, "alarm", who="%s#%d" % (who or text, st["seq"])); refresh(); return True
        def answer(how):
            if not st["alarm"]: return
            last = st["alarm"][-1]; st["alarm"] = []; hold = settings["hold"]
            st["resume_at"] = time.time() + hold if hold > 0 else 0.0
            if how != "banner" and banner_up() and last["text"] and str(ALERTS.line).endswith(last["text"]):
                ALERTS.dismiss()
            say("answered; %s" % (("skill loops go on in %d s." % hold) if hold
                                             else "skill loops go on."), Kit.HUE_GOOD)
            st["last_answered"] = last; refresh()
        def alarm_tick(now):
            if not st["alarm"]: return
            if banner_up(): st["banner_seen"] = True
            elif st["banner_seen"]: answer("banner"); return
            rep = settings["repeat"]
            if rep > 0 and not st["next_sound"]: st["next_sound"] = now + rep
            if rep > 0 and not 0 < st["next_sound"] - now <= rep:
                st["next_sound"] = now + rep; sid = sound_of(st["alarm"][-1]["kind"])
                if sid: API.PlaySound(sid)
            if not 0 < st["flash_at"] - now <= FLASH_SECS:
                st["flash_at"] = now + FLASH_SECS; st["flash_on"] = not st["flash_on"]; refresh()
        def read_me(now, p):
            if st["my_name"] and 0 <= now - st["name_at"] < NAME_EVERY: return
            st["name_at"] = now; name = str(p.Name or "").strip(); st["me"] = int(p.Serial)
            if name and name != st["my_name"]:
                st["my_name"] = name
                st["name_re"] = re.compile(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(name), re.IGNORECASE)
                parts = [w for w in re.split(r"[^A-Za-z0-9']+", name) if w]; words = [w for w in parts if len(w) >= 4]
                if len(parts) > 1 and words:
                    st["words_re"] = re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])"
                                                % "|".join(re.escape(w) for w in words), re.IGNORECASE)
                else: st["words_re"] = None
        def real_gump(g):
            if g is None: return None
            try: inner = g.Gump
            except Exception: return g
            return inner if inner is not None else g
        def gone(g):
            try: return bool(g.IsDisposed)
            except Exception: return True
        def mouse_readers():
            if not mouse["looked"]:
                mouse["looked"] = True; got = []; t = Client._type("ClassicUO.Input.Mouse")
                if t is not None:
                    for name in ("Position", "LastLeftButtonClickTime", "LastRightButtonClickTime"):
                        m = Client._member(t, name)
                        if m is not None: got.append((m[0], name == "Position"))
                mouse["get"] = got or None
            return mouse["get"]
        def input_tick(now):
            gs = mouse_readers()
            if not gs: return None
            cur = []
            for fn, point in gs: v = fn(); cur.append((int(v.X), int(v.Y)) if point else int(v))
            cur = tuple(cur); prev, st["input"] = st["input"], cur
            if prev is not None and cur != prev: st["asked_at"] = now
            return True
        def typing_tick(now):
            t = bool(HOST.typing()); prev, st["typing"] = st["typing"], t
            if prev is not None and t != prev: st["typed_at"] = st["asked_at"] = now
        def gump_tick(now):
            typing_tick(now)
            if input_tick(now) is None:
                up = bool(API.HasTarget("any"))
                if st["cursor_up"] and not up: st["asked_at"] = now
                st["cursor_up"] = up
                if 0 <= now - st["used_at"] <= ASKED_SECS: st["asked_at"] = max(st["asked_at"], st["used_at"])
            gid = int(API.HasGump() or 0); prev = st["gump_obj"]
            if gid and prev is not None and gid == st["gump_gid"] and not gone(prev): st["open_ids"][gid] = now; return
            g = real_gump(API.GetGump(gid)) if gid else None
            if g is prev or (g is not None and prev is not None and gid == st["gump_gid"] and not gone(prev)):
                st["gump_obj"] = g
                if gid: st["open_ids"][gid] = now
                return
            if prev is not None and st["gump_vis"] and gone(prev): st["asked_at"] = now
            st["gump_obj"], st["gump_gid"] = g, gid
            if g is None: st["gump_vis"] = False; return
            visible = bool(g.IsVisible); st["gump_vis"] = visible; st["last_gid"] = gid
            opened = st["open_ids"]; seen_at = opened.get(gid); opened[gid] = now
            if len(opened) > OPEN_IDS_CAP:
                for k in sorted(opened, key=opened.get)[:len(opened) - OPEN_IDS_CAP]: del opened[k]
            if HOST.gump_expected(gid, now): return
            if not st["primed"] or not visible or gid in ignored_ids(): return
            if seen_at is not None and 0 <= now - seen_at <= SAME_GUMP_SECS: return
            if 0 <= now - st["asked_at"] <= ASKED_SECS: return
            if settings["gump"]:
                raise_alarm("gump", "A gump opened by itself (id 0x%X)" % gid, "gump 0x%X" % gid, gid=gid)
        def staff_tick(now):
            pat = marker_re()
            if pat is None: return
            mobs = HOST.mobiles(STAFF_RANGE); checked, seen, me = st["checked"], st["staff_seen"], st["me"]
            if len(checked) > CACHE_CAP or pat is not st["checked_pat"]: checked.clear(); st["checked_pat"] = pat
            for m in mobs:
                try: s = int(m.Serial)
                except Exception: continue
                if s == me: continue
                hit = checked.get(s)
                if hit is None or (not hit[0] and hit[2] < 2 and now - hit[1] >= STAFF_RECHECK):
                    try:
                        name = str(m.Name or ""); text = name
                        try:
                            props = m.raw.NameAndProps(False)
                            if props: text = name + "\n" + str(props).split("\n")[0]
                        except Exception: pass
                    except Exception: continue
                    hit = (bool(pat.search(text)), now, (hit[2] if hit else 0) + 1, name); checked[s] = hit
                if not hit[0]: continue
                last = seen.get(s); seen[s] = now
                if last is None or not 0 <= now - last <= STAFF_GONE:
                    raise_alarm("staff", "Staff in view: %s" % (hit[3] or "someone"), "staff %X" % s, serial=s)
            if len(seen) > 50:
                for k in [k for k, t in seen.items() if not 0 <= now - t <= STAFF_GONE]: del seen[k]
        def speaker_serial(name):
            low = name.lower()
            try:
                for m in HOST.mobiles(STAFF_RANGE):
                    if str(m.Name or "").lower() == low: return int(m.Serial)
            except Exception: pass
            return 0
        def quote(text):
            text = " ".join(str(text).split()); return text if len(text) <= QUOTE_MAX else text[:QUOTE_MAX - 2] + ".."
        def speech_tick(now):
            rd = st["rd"]
            if rd is None: return
            lines = rd.new()
            if not lines: return
            my_low = st["my_name"].lower(); nre = st["name_re"]; wre = st["words_re"] if settings["words"] else None
            for ln in lines:
                name = (ln.name or "").strip(); text = ln.text
                if not name and ": " in text: name, text = [x.strip() for x in text.split(": ", 1)]
                if not name or name.lower() == "system": continue
                low = name.lower()
                if my_low and low == my_low:
                    if 0 <= now - st["typed_at"] <= TYPED_SECS: st["asked_at"] = now
                    continue
                if not settings["name"] or nre is None: continue
                if nre.search(text) or (wre is not None and wre.search(text)):
                    raise_alarm("name", '%s said your name: "%s"' % (name, quote(text)), name,
                                serial=speaker_serial(name), said=text)
        def heard_tick():
            q = st["heard"]
            if not q: return
            st["heard"] = []; my_low = st["my_name"].lower()
            for text, name, mt in q:
                if not name or name.lower() == "system" or (my_low and name.lower() == my_low): continue
                if mt in WHISPER_TYPES and settings["whisper"]:
                    raise_alarm("whisper", '%s whispers to you: "%s"' % (name, quote(text)), name,
                                serial=speaker_serial(name), said=text)
        def on_used(*args):
            if st["active"]: st["used_at"] = time.time()
        MT_LOW = {}
        def on_entry(*args):
            if not st["active"]: return
            for a in args:
                try:
                    mt = a.MessageType; m = MT_LOW.get(mt)
                    if m is None:
                        m = str(mt).lower()
                        if len(MT_LOW) < 64: MT_LOW[mt] = m
                except Exception: continue
                if m in WHISPER_TYPES:
                    try: text = str(a.Text or ""); name = str(a.Name or "")
                    except Exception: continue
                    q = st["heard"]
                    if len(q) < QUEUE_CAP: q.append((text, name, m))
                return
        def on_hits(*args):
            if settings["hit"] and not st.get("hit_poke"): st["hit_poke"] = True; HOST.poke("skills.alarm", False)
        def hook_events():
            Kit.hook_once(hooks, "done", ("ObjectUsed", on_used), ("JournalEntryAdded", on_entry),
                          ("OnPlayerHitsChanged", on_hits))
        def hit_tick(p):
            if not settings["hit"]: st["hp"] = None; return
            hp = int(p.Hits); prev = st["hp"]; st["hp"] = hp
            if prev is None or p.IsDead or p.InWarMode or hp >= prev: return
            raise_alarm("hit", "You took %d damage while not fighting" % (prev - hp), "hit")
        def on_alarm_click():
            if Follow.alt_held():
                r = st["alarm"][-1] if st["alarm"] else st.get("last_answered")
                if r is not None and r.get("serial"): queue(("follow", r["serial"]))()
                return
            if st["alarm"]: queue("answer")(); return
            if st["minimized"]:
                now = time.time()
                if 0 <= now - st.get("mini_click", 0.0) <= 0.6: st["mini_click"] = 0.0; queue("toggle_min")()
                else: st["mini_click"] = now
        def build_window():
            g, store, c = wnd.begin(W, Kit.MARGIN + 30 + Kit.GAP + 96 + Kit.MARGIN); M = Kit.MARGIN
            if st["minimized"]:
                c["line_w"] = MINI_W - 90
                c["alarm_hit"] = Kit.catcher(g, 14, 12, MINI_W - 90, MINI_H - 24, on_alarm_click,
                                             "Click: answer the alarm. Double-click: restore. Alt+click: auto-follow "
                                             "(again to stop)", movable=True)
            else:
                IW = W - 2 * M; wnd.frame(g); yb = M + 30 + Kit.GAP; Kit.add_section(g, M, yb, IW, 96)
                c["status"] = Kit.add_label(g, "", M + 12, yb + 10, Kit.HUE_INFO)
                c["line2"] = Kit.add_label(g, "", M + 12, yb + 32, Kit.HUE_INFO); c["line_w"] = IW - 28
                c["alarm_hit"] = Kit.catcher(g, M + 6, yb + 6, IW - 12, 46, on_alarm_click,
                                             "Click: answer the alarm. Alt+click: auto-follow (again to stop)",
                                             movable=True)
                xb = M + 12
                for key, art, cap, tip, act in (
                        ("here", Kit.ART_OK, "I'm here", "Answer the alarm: skill loops go on (after the set pause)",
                         "answer"), ("test", Kit.ART_PLAY, "Test", "Raise a test alarm until you answer", "test"),
                        ("ignore", Kit.ART_CLOSE, "Ignore this gump", "Answer and ignore this gump from now on",
                         "ignore_gump")):
                    b = Kit.art_button(g, store, key, art, xb, yb + 62, cap, tip, on_click=queue(act))
                    xb += 35 + Kit.text_w(cap) + 14
                c["ignore"] = b
            wnd.end(g); st["drawn"] = None; refresh()
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, (240, 160), (MINI_W, MINI_H), TRAY_ICON,
                         cleanup, lock=True)
        def watching_text():
            on = [w for k, w in (("gump", "gumps"), ("staff", "staff"), ("name", "your name"), ("whisper", "whispers"),
                                 ("hit", "hits")) if settings[k]]
            if st["minimized"]:
                return "%s: %s" % (TITLE, ("watching " + ", ".join(on)) if on else "nothing ticked in settings")
            return ("Watching: " + ", ".join(on)) if on else "Nothing ticked in settings"
        def refresh():
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]): return
            c = win["c"]; lw = c.get("line_w", 200); al = st["alarm"]
            if al:
                r = al[-1]; line = ("%s: " % TITLE if st["minimized"] else "ALARM: ") + r["text"]
                hue = Kit.HUE_BAD if st["flash_on"] else Kit.HUE_TEXT
                line2 = ("+%d more. " % (len(al) - 1) if len(al) > 1 else "") + \
                    "Skill loops paused: click here or I'm here"
            else:
                left = st["resume_at"] - time.time() if st["resume_at"] else 0
                line, hue = watching_text(), Kit.HUE_INFO
                line2 = ("Skill loops go on in %d s" % int(left + 0.99)) if 0 < left <= HOLD_MAX + 1 else "All quiet"
            key = (line, hue, line2, lw)
            if key == st["drawn"]: return
            st["drawn"] = key; line = Kit.fit(line, lw); Kit.set_text(c["status"], line, hue)
            if "line2" in c: Kit.set_text(c["line2"], Kit.fit(line2, lw), Kit.HUE_INFO)
            ig = c.get("ignore")
            if ig is not None:
                want = bool(al) and al[-1]["kind"] == "gump"
                if c.get("ignore_on") != want:
                    c["ignore_on"] = want; ig.IsVisible = want; b = win["store"][0].get("ignore")
                    if b is not None: b.IsVisible = want
        def ignore_gump(from_alarm):
            gid = 0
            if from_alarm:
                for r in reversed(st["alarm"]):
                    if r["kind"] == "gump" and r["gid"]: gid = r["gid"]; break
            if not gid: gid = st["last_gid"]
            if not gid: say("no server gump seen yet.", Kit.HUE_INFO); return
            if gid not in ignored_ids():
                cur = settings["ignore"].strip().strip(",")
                settings["ignore"] = (cur + ", " if cur else "") + "0x%X" % gid; save_settings()
                HOST.refresh_settings(KEY); say("gump 0x%X ignored." % gid, Kit.HUE_INFO)
        def ignore_and_answer(action): ignore_gump(True); answer("click")
        ACTIONS = {"follow": lambda action: Follow.toggle(action[1], TITLE), "answer": lambda action: answer("click"),
                "test": lambda action: raise_alarm("test", "Test alarm: answer it to go on", "test"),
                "ignore_gump": ignore_and_answer, "ignore_last": lambda action: ignore_gump(False)}
        def page_table(w):
            fields = {"top": 32, "ldy": 4, "fh": 30, "align": True, "sh": 126}
            return (("TRIGGERS  (each pauses skill loops too)", (("check", "gump", "A server gump nobody asked for",
                         "Not within %.1f s of your mouse, typing or a gump closing; not a page of an open window "
                         "or an ignored id" % ASKED_SECS),
                        ("check", "staff", "Staff in view (a staff word in name or title)",
                         "Within %d tiles, a name or title holding a staff word (list below)" % STAFF_RANGE),
                        ("check", "name", "Someone says your name", "Read from the game (whole words, any case)"),
                        ("check", "words", "Or any word of it with 4 letters or more",
                         "For a name of two words or more: \"Wolf\" in \"Grey Wolf\"", {"dx": 34}),
                        ("check", "whisper", "Someone whispers to you", "Lines the client marks as whispered"),
                        ("check", "hit", "You take damage while not in war mode",
                         "Something hurts you while you train (off at first)")),
                     {"top": 32, "sh": 194}), ("STAFF AND GUMPS", (
                        ("text", "markers", "Staff words:", "Words marking a staff name or title, commas between "
                         "(whole words, any case; empty: no check)"), ("text", "ignore", "Gump ids to ignore:",
                         "Gump ids that never raise the alarm: hex (0x1A2B) or decimal, commas between"),
                        ("buttons", (("ignore_last", Kit.ART_OK, "Ignore last gump", "Ignore the last server gump seen",
                                      queue("ignore_last")),), {"bdy": 0, "stay": True}), ("note", last_gump_text(),
                         {"dx": 12 + 35 + Kit.text_w("Ignore last gump") + 14, "ndy": 3, "key": "last"})), fields),
                    ("ALARM  (sound: Settings > Alerts)", (("num", "repeat", "Repeat the sound every:",
                         "Seconds between sounds until you answer (0-%d, 0 = once)" % REPEAT_MAX, "s", 0, REPEAT_MAX),
                        ("num", "hold", "Loops stay paused after you answer:",
                         "Seconds loops stay paused after you answer (0-%d, 0 = none)" % HOLD_MAX, "s", 0, HOLD_MAX),
                        ("check", "anyalarm", "Any alarm pauses skill loops", "While any module's alarm banner waits "
                         "for a click (Ultima Tracker > Lookout, a red in your house)")), dict(fields, fw=40, ugap=12)))
        def last_gump_text():
            return ("Last server gump: 0x%X" % st["last_gid"]) if st["last_gid"] else "No server gump seen yet"
        def page_clicks(f):
            page["skip"] = "ignore_last" in st["queue"]
            if page["skip"]: st["queue"].remove("ignore_last"); ignore_gump(False)
        def page_adjust(f, new):
            if page["skip"]: new.update(settings); return
            for k in ("markers", "ignore"):
                v = _clean(new[k]); new[k] = v if v != _clean(settings[k]) else settings[k]
            Kit.set_text(f.c["last"], last_gump_text(), Kit.HUE_INFO)
        def page_changed(old, new): st["drawn"] = None
        cfg = Kit.Page(settings, page_table, save_settings, page_changed, adjust=page_adjust, clicks=page_clicks)
        load_settings()
        def _start():
            st.update({"shutting": False, "docked": False, "active": True, "alarm": [],
                       "queue": [a for a in st["queue"] if a == "ignore_last"],
                       "resume_at": 0.0, "next_gump": 0.0, "gump_obj": None, "gump_gid": 0,
                       "gump_vis": False, "primed": False, "input": None,
                       "asked_at": 0.0, "used_at": 0.0, "cursor_up": False, "typing": None, "typed_at": 0.0,
                       "next_staff": 0.0, "checked": {}, "staff_seen": {}, "name_at": 0.0,
                       "next_hit": 0.0, "hp": None, "heard": [], "next_sound": 0.0,
                       "banner_seen": False, "flash_at": 0.0, "flash_on": False, "drawn": None,
                       "last_answered": None, "rd": Journal.reader(), "checked_pat": None,
                       "minimized": wnd.start_min()})
            load_settings(); hook_events()
            for k, akey, label, snd in KINDS: HOST.alert_kind(akey, label, snd)
            cleanup.service("attention.up", is_up); build_window(); wnd.dock()
        def _tick():
            if win["g"] is None: return
            if Kit.closed(win): return
            now = time.time()
            while st["queue"]:
                action = st["queue"].pop(0)
                if wnd.action(action): continue
                fn = ACTIONS.get(action[0] if isinstance(action, tuple) else action)
                if fn is not None: fn(action)
            p = HOST.me()
            if p is None: return
            read_me(now, p)
            if not 0 < st["next_gump"] - now <= GUMP_EVERY:
                st["next_gump"] = now + GUMP_EVERY; gump_tick(now); st["primed"] = True
            if settings["staff"] and not 0 < st["next_staff"] - now <= STAFF_EVERY:
                st["next_staff"] = now + STAFF_EVERY; staff_tick(now)
            speech_tick(now); heard_tick()
            if st.pop("hit_poke", False) or not 0 < st["next_hit"] - now <= HIT_EVERY:
                st["next_hit"] = now + HIT_EVERY; hit_tick(p)
            alarm_tick(now)
            if not st["alarm"] and st["resume_at"]:
                if not is_up(): st["resume_at"] = 0.0
                refresh()
        def _stop():
            st["shutting"] = True; st["active"] = False; st["alarm"] = []; st["resume_at"] = 0.0; save_settings()
            st["rd"] = None; st["gump_obj"] = None; cleanup.close()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                  "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed}
    def _part_bags():
        KEY = "skillbags"; TITLE = "Skill Bags"; SETTINGS_KEY = "SkillBags_settings"; POS_KEY = "SkillBags_pos"
        MIN_KEY = "SkillBags_min"; RULES_KEY = "SkillBags_rules"; DONE_KEY = "SkillBags_done"; W = 740
        MINI_W, MINI_H = 240, 46; TRAY_ICON = 0x0E76; ROW_H = 42; MAX_RULES = 8; MAX_DONE = 300; NAME_SCANS_MAX = 6
        RELIST_EVERY = 5.0; BAG_NAME_EVERY = 2.0; TARGET_TIMEOUT = 3.0; OPEN_TIMEOUT = 2.5; OPEN_RETRY = 6.0
        BUSY_RETRY = 1.5; MAX_BUSY = 4; SKILL_TIMER = 10.0
        SKILL_TIMER_SHORT = {"item identification": 3.0, "arms lore": 3.0, "detect hidden": 3.0}
        MIN_DELAY, MAX_DELAY = 0.5, 60.0; DEFAULT_RETRIES = 1; CHECK_EVERY = 0.25; SCAN_EVERY = 0.5
        LOCKPICK_GRAPHIC = 0x14FC
        BUSY_WORDS = ("must wait", "too far away", "cannot reach", "can't reach",
                      "can't see that", "cannot see that", "already casting", "you are busy")
        GUARD_STATUS = "Paused: guard zone"; UNKNOWN_STATUS = HOLD_TEXT["unknown"]
        RES_POS_KEY = "SkillBags_results_pos"; RES_KEEP = 200; RES_ROWS = 16; RES_W = 680; RES_ROW_H = 18
        RES_KEY = "skillbags.results"; RES_TITLE = "Skill Bags Results"; RES_MIN_W = 500
        RES_FIXED = 2 * Kit.MARGIN + 30 + Kit.GAP + 30 + 24 + 8; RES_EMPTY = "No results shown. Click a rule's Results."
        RES_ANSWER_MAX = 160; EXPORT_NAME = "SkillBags_%08X_rule%d.txt"
        ITEMID_MAGIC = ("durable", "substantial", "massive", "fortified", "indestructable",
                        "indestructible", "defense", "guarding", "hardening", "fortification",
                        "invulnerability", "accurate", "ruin", "might", "force", "power", "vanquishing",
                        "silver", "slaying", "slaughter", "thrashing", "repond", "terathan", "bane",
                        "reptilian death", "dismissal", "gargoyle's foe", "damnation", "exorcism",
                        "ophidian", "spider's death", "arachnid doom", "dousing", "dissipation",
                        "vacuum", "elemental health", "earth shatter", "blood drinking", "summer wind",
                        "elemental ban", "slayer", "magic")
        ITEMID_UNKNOWN = "unidentified"
        RESULT_WORDS = {"itemid": {2: "not certain"}, "armslore": {2: "not certain", 4: "read"},
                        "tasteid": {2: "not certain", 4: "read"},
                        "removetrap": {1: "disarmed", 2: "trap, not disarmed", 3: "no trap"},
                        "lockpick": {1: "unlocked", 2: "still locked", 3: "not locked"},
                        "cartography": {1: "decoded", 2: "not decoded", 3: "can't decode"}}
        ITEMID_MAGIC_RE = re.compile(r"\b(" + "|".join(ITEMID_MAGIC) + r")\b")
        ITEMID_CHARGES_RE = re.compile(r"\[[^\]]*:\s*\d+\s*\]"); ITEMID_MAGIC_WORD = re.compile(r"\bmagic\b")
        RULE_ACTIONS = [("itemid", "Item Identification", "skill", "Item Identification", 3.2, 0,
             (), ("not certain", "no idea how much", "tell much about it"), ()),
            ("armslore", "Arms Lore", "skill", "Arms Lore", 3.2, 0, (), ("not certain", "tell much about it"), ()),
            ("tasteid", "Taste Identification", "skill", "Taste Identification", 10.2, 0,
             (), ("not certain", "tell much about it", "can't tell"), ()),
            ("removetrap", "Remove Trap", "skill", "Remove Trap", 10.2, 1,
             ("render the trap harmless", "successfully"), ("fail to disarm",),
             ("doesn't appear to be trapped", "isn't trapped", "not trapped")),
            ("lockpick", "Lockpicking (uses lockpicks)", "tool", LOCKPICK_GRAPHIC, 1.5, 1,
             ("lock quickly yields",), ("unable to pick the lock",),
             ("does not appear to be locked", "cannot be picked by normal means", "did not need to be unlocked")),
            ("cartography", "Cartography (decode maps)", "use", None, 1.0, 3,
             ("successfully decode",), ("fail to make anything of the map",),
             ("too difficult to attempt to decode", "not a map")),
            ("use", "Double-click each item", "use", None, 1.0, 0, (), (), ()),
            ("cskill", "Custom skill (name in Custom)", "cskill", None, 10.2, 0, (), (), ()),
            ("ctool", "Custom tool (graphic in Custom)", "ctool", None, 1.5, 0, (), (), ()),]
        ACTION_NAMES = [a[1] for a in RULE_ACTIONS]
        FILTERS = [("all", "Every item"), ("containers", "Containers only"),
                   ("graphics", "Graphics in Text (hex)"), ("name", "Name contains Text")]
        FILTER_NAMES = [f[1] for f in FILTERS]; CODE_TEXT = {1: "OK", 2: "failed", 3: "skipped", 4: "done"}
        settings = {"hidden": True, "war": True, "open": True, "retries": DEFAULT_RETRIES, "guard": True}
        DEFAULTS = dict(settings)
        rules = []; st = {"minimized": False, "shutting": False, "docked": False, "queue": []}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}
        cleanup = Kit.Cleanup(); queue = Kit.queuer(st); say = Kit.sayer(TITLE)
        page = {"f": None, "rows": [], "next_read": 0.0}
        resw = {"g": None, "rule": None, "c": {}, "rows": [], "page": 0, "dirty": False, "minimized": False,
                "shutting": False, "docked": False, "queue": []}
        def esc(s): return str(s or "").replace("|", "/").replace("~", "-")
        def clamp_delay(v, default):
            try: v = float(v)
            except Exception: return default
            return max(MIN_DELAY, min(MAX_DELAY, v))
        def new_rule(action=0):
            a = RULE_ACTIONS[action]
            return {"action": action, "bag": 0, "filt": a[5], "text": "", "custom": "",
                    "delay": a[4], "deep": False, "auto": False, "done": {}, "order": []}
        def rule_action(r): return RULE_ACTIONS[r["action"]]
        def skill_floor(r):
            a = RULE_ACTIONS[r["action"]]
            name = a[3] if a[2] == "skill" else r["custom"].strip() if a[2] == "cskill" else ""
            return SKILL_TIMER_SHORT.get(name.lower(), SKILL_TIMER) if name else 0.0
        def parse_graphics(text):
            out = []
            for part in str(text or "").replace(";", ",").split(","):
                part = part.strip()
                if not part: continue
                try: out.append(int(part, 16) if part.lower().startswith("0x") else int(part, 0))
                except Exception:
                    try: out.append(int(part, 16))
                    except Exception: pass
            return out
        def load_settings():
            p = Kit.get_var(SETTINGS_KEY).split("|")
            if len(p) >= 4:
                for n, k in enumerate(("hidden", "war", "open")): settings[k] = p[n] == "1"
                try: settings["retries"] = max(0, min(9, int(p[3])))
                except Exception: settings["retries"] = DEFAULT_RETRIES
            settings["guard"] = (p[5] == "1") if len(p) >= 6 else True; del rules[:]; raw = Kit.get_var(RULES_KEY)
            if raw:
                for chunk in raw.split("|"):
                    f = chunk.split("~")
                    if len(f) < 8: continue
                    try:
                        r = new_rule(max(0, min(len(RULE_ACTIONS) - 1, int(f[0]))))
                        r.update({"bag": int(f[1]) if f[1] else 0, "filt": max(0, min(len(FILTERS) - 1, int(f[2]))),
                                  "text": f[3], "custom": f[4]})
                        r.update({"delay": max(clamp_delay(f[5], rule_action(r)[4]), skill_floor(r)),
                                  "deep": f[6] == "1", "auto": f[7] == "1"})
                        rules.append(r)
                    except Exception: continue
                    if len(rules) >= MAX_RULES: break
            raw = Kit.get_var(DONE_KEY)
            if raw:
                lists = raw.split("|")
                for i, r in enumerate(rules):
                    if i >= len(lists): break
                    for part in lists[i].split(","):
                        if ":" not in part: continue
                        s, c = part.split(":", 1)
                        try: s, c = int(s), int(c)
                        except Exception: continue
                        r["done"][s] = c; r["order"].append(s)
        def save_settings():
            Kit.put_var(SETTINGS_KEY, "|".join(["1" if settings["hidden"] else "0", "1" if settings["war"] else "0",
                "1" if settings["open"] else "0", str(settings["retries"]), "0", "1" if settings["guard"] else "0"]))
            Kit.put_var(RULES_KEY, "|".join("~".join([str(r["action"]), str(r["bag"]), str(r["filt"]), esc(r["text"]),
                          esc(r["custom"]), "%.2f" % r["delay"], "1" if r["deep"] else "0",
                          "1" if r["auto"] else "0"]) for r in rules))
            save_done()
        def save_done():
            Kit.put_var(DONE_KEY, "|".join(",".join("%d:%d" % (s, r["done"][s]) for s in r["order"] if s in r["done"])
                for r in rules))
        def mark_done(r, serial, code):
            if serial not in r["done"]: r["order"].append(serial)
            r["done"][serial] = code; order = r["order"]
            if len(order) > MAX_DONE:
                k = len(order) - MAX_DONE; done = r["done"]
                for old in order[:k]: done.pop(old, None)
                del order[:k]
            st["save_done"] = True
        def result_tag(a, code, answer):
            if a[0] == "itemid" and code in (1, 4):
                low = (answer or "").lower()
                if not low: return "no answer"
                if ITEMID_UNKNOWN in low: return "unidentified"
                if ITEMID_CHARGES_RE.search(low): return "magic"
                k = low.find("[")
                if k >= 0: return "magic" if ITEMID_MAGIC_RE.search(low, k) else "plain"
                return "magic" if ITEMID_MAGIC_WORD.search(low) else "plain"
            words = RESULT_WORDS.get(a[0])
            if words is not None and code in words: return words[code]
            return CODE_TEXT.get(code, "done")
        def answer_of(j):
            if j.get("match_raw"): return j["match_raw"]
            raw = j.get("raw")
            if not raw: return ""
            nm = (j.get("name") or "").lower(); best = None
            for k in range(len(raw) - 1, -1, -1):
                text, name = raw[k]; ln = name.lower()
                if ((nm and (ln == nm or (len(nm) >= 3 and nm in text.lower()))) or text.lstrip().startswith("[")):
                    return text
                if best is None and (not name or ln == "system"): best = text
            return best if best is not None else raw[-1][0]
        def add_result(r, serial, code, name, answer, tag=None):
            res = r.get("_res")
            if res is None: res = r["_res"] = []
            for k in range(len(res) - 1, -1, -1):
                if res[k][1] == serial: del res[k]; break
            answer = str(answer or "").replace("\n", " ").strip()[:RES_ANSWER_MAX]
            res.append((time.time(), serial, name or ("0x%08X" % serial), code,
                        tag or result_tag(rule_action(r), code, answer), answer))
            if len(res) > RES_KEEP: del res[:-RES_KEEP]
            r.pop("_rescount", None)
            if resw["rule"] is r: resw["dirty"] = True
        def clear_results(r):
            r.pop("_res", None); r.pop("_rescount", None)
            if resw["rule"] is r: resw["dirty"] = True
        def counts_text(r):
            txt = r.get("_rescount")
            if txt is None:
                res = r.get("_res") or []
                if not res: txt = "No results yet."
                else:
                    cnt = {}
                    for e in res: cnt[e[4]] = cnt.get(e[4], 0) + 1
                    txt = "%s: %s" % (Kit.count(len(res), "item"), ", ".join(["%d %s" % (n, t) for t, n in
                                                        sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))]))
                r["_rescount"] = txt
            return txt
        get_item = Kit.find_item
        def bag_name(r, short=True):
            if not r["bag"]: return "no bag yet"
            now = time.time(); cached = r.get("_bagname")
            if cached is not None and cached[0] == r["bag"] and now < cached[1]: name = cached[2]
            else:
                it = get_item(r["bag"])
                if it is None: name = "bag not found"
                else: name = safe(lambda: str(it.Name or ""), "") or "0x%08X" % r["bag"]
                r["_bagname"] = (r["bag"], now + BAG_NAME_EVERY, name)
            return name if short else "%s  0x%08X" % (name, r["bag"])
        def invalidate(r=None):
            for rule in ([r] if r is not None else rules): rule.pop("_cache", None); rule.pop("_bagname", None)
        def matches(r, it):
            f = FILTERS[r["filt"]][0]
            if f == "all": return True
            if f == "containers":
                try: return bool(it.IsContainer)
                except Exception: return False
            if f == "graphics":
                try: return int(it.Graphic) in r["_gfx"]
                except Exception: return False
            if f == "name":
                want = r["text"].strip().lower()
                if not want: return True
                name = ""
                try: name = str(it.Name or "")
                except Exception: pass
                if not name:
                    try: name = str(API.ItemNameAndProps(it.Serial, False) or "").split("\n")[0]
                    except Exception: name = ""
                if not name: return None
                return want in name.lower()
            return True
        def bag_count(serial):
            try: return int(API.Contents(serial) or 0)
            except Exception: return -1
        def bag_items(r, i, now, may_list=True):
            bag = get_item(r["bag"]) if r["bag"] else None
            if bag is None: r.pop("_cache", None); return [], 0, False
            cache = r.get("_cache"); count = bag_count(r["bag"]); listed = False
            if (cache is None or cache["count"] != count or now >= cache["relist"] or cache["bag"] != r["bag"]):
                if not may_list:
                    if cache is None: return None
                    listed = None
                else: listed = True
            if listed:
                try: items = list(API.ItemsInContainer(r["bag"], bool(r["deep"])) or [])
                except Exception: items = []
                if FILTERS[r["filt"]][0] == "graphics": r["_gfx"] = set(parse_graphics(r["text"]))
                scans = cache["scans"] if cache is not None else {}; out, pending = [], []
                for it in items:
                    try: serial = int(it.Serial)
                    except Exception: continue
                    if serial == r["bag"]: continue
                    m = matches(r, it)
                    if m is None and serial in r["done"]: m = True
                    if m is None: pending.append((serial, it))
                    elif m: out.append((serial, it)); scans.pop(serial, None)
                cache = {"bag": r["bag"], "count": count, "relist": now + RELIST_EVERY,
                         "items": out, "pending": pending, "scans": scans}
                r["_cache"] = cache
            elif cache["pending"]:
                still = []
                for serial, it in cache["pending"]:
                    m = matches(r, it)
                    if m is None: still.append((serial, it))
                    elif m: cache["items"].append((serial, it))
                cache["pending"] = still
            scans = cache["scans"]; gave_up = []
            for serial, it in cache["pending"]:
                n = scans.get(serial, 0) + 1; scans[serial] = n
                if n >= NAME_SCANS_MAX:
                    scans.pop(serial, None); gave_up.append((serial, it)); cache["items"].append((serial, it))
                    mark_done(r, serial, 3); add_result(r, serial, 3, "", "its name never came", "skipped (no name)")
                    say("0x%08X skipped, its name never came (rule %d)." % (serial, i + 1), Kit.HUE_INFO)
            if gave_up:
                gone = set(s for s, _ in gave_up); cache["pending"] = [p for p in cache["pending"] if p[0] not in gone]
            if len(scans) > MAX_DONE: scans.clear()
            return cache["items"], len(cache["pending"]), listed
        def bag_opened(serial):
            it = get_item(serial)
            if it is None: return False
            try:
                if it.Opened: return True
            except Exception: pass
            try: return int(API.Contents(serial) or 0) > 0
            except Exception: return False
        def due(t, now): return not 0 < t - now <= MAX_DELAY
        def ensure_open(r, now, on_run=True):
            serial = r["bag"]
            if not serial or not Kit.in_pack(serial): return False
            if bag_opened(serial): st["opening"].pop(serial, None); r["_closed"] = False; return True
            r["_closed"] = True
            if not settings["open"] or not on_run: return False
            o = st["opening"].get(serial)
            if o is None or due(o + OPEN_TIMEOUT + OPEN_RETRY, now): st["opening"][serial] = now; API.UseObject(serial)
            return False
        def blocked(now):
            if st["paused"]: return "Paused"
            p = HOST.me()
            if p is None: return "No player"
            why = HOST.fight_hold(now)
            if why == "dead": return "Dead"
            if settings["hidden"] and p.IsHidden: return "Hidden"
            if why == "war": return "War mode"
            gp = st["guard_paused"]
            if gp == "unknown": return UNKNOWN_STATUS
            if gp: return GUARD_STATUS
            if why: return "Paused: " + HOLD_TEXT.get(why, why)
            if HOST.cursor_busy(KEY): return "Cursor busy"
            if API.HasTarget("any"): return "Cursor up"
            return None
        def pick_next(now):
            n = len(rules)
            if not n: return None
            start = st["rr"] % n; listed = False
            for k in range(n):
                i = (start + k) % n; r = rules[i]
                if not (r["auto"] or i in st["run"]) or not r["bag"]: r.pop("_closed", None); continue
                if rule_action(r)[2] == "ctool" and i not in st["run"]:
                    if r["auto"]: auto_off(i, r); say("rule %d: a custom tool runs only on Run." % (i + 1), Kit.HUE_BAD)
                    continue
                if not Kit.in_pack(r["bag"]):
                    st["run"].discard(i); st["budget"].pop(i, None)
                    say("rule %d: its bag isn't in your backpack." % (i + 1), Kit.HUE_BAD)
                    if r["auto"]: auto_off(i, r)
                    continue
                if not ensure_open(r, now, i in st["run"]): continue
                got = bag_items(r, i, now, not listed)
                if got is None: continue
                items, unknown, did = got
                if did: listed = True; st["rr"] = i + 1
                r["_count"] = (sum(1 for s, it in items if s in r["done"]), len(items)); waiting = False
                budget = st["budget"]
                if i in st["run"] and rule_action(r)[2] == "ctool" and i not in budget:
                    budget[i] = (r["_count"][1] - r["_count"][0] + unknown) * (1 + settings["retries"])
                for serial, it in items:
                    if serial in r["done"]: continue
                    if not due(st["later"].get((i, serial), 0.0), now): waiting = True; continue
                    if i in budget:
                        if budget[i] <= 0:
                            st["run"].discard(i); budget.pop(i, None)
                            say("rule %d stopped at its count (%s)." % (i + 1, bag_name(r)), Kit.HUE_INFO); break
                        budget[i] -= 1
                    return i, r, serial, it
                if i in st["run"] and not unknown and not waiting and did is not None:
                    st["run"].discard(i); st["budget"].pop(i, None)
                    say("%s on %s, %d of %d handled." % (
                        rule_action(r)[1], bag_name(r), r["_count"][0], r["_count"][1]), Kit.HUE_GOOD)
            return None
        def auto_off(i, r):
            st["run"].discard(i); r["auto"] = False; save_settings()
            if i < len(win["rows"]): win["rows"][i]["auto"].IsChecked = False
            if page["f"] is not None: HOST.refresh_settings(KEY)
        def start_job(i, r, serial, it, now):
            a = rule_action(r); kind = a[2]
            j = {"rule": i, "serial": serial, "t": now, "phase": "target", "reader": None, "lines": [], "raw": [],
                 "name": safe(lambda: str(it.Name or ""), "")}
            if kind in ("skill", "cskill"):
                name = a[3] if kind == "skill" else r["custom"].strip()
                if not name:
                    say("rule %d needs a skill name in its Custom box." % (i + 1), Kit.HUE_BAD)
                    auto_off(i, r); return False
                HOST.claim_cursor(KEY, TARGET_TIMEOUT + 0.5); j["reader"] = Journal.reader(); API.UseSkill(name)
            elif kind in ("tool", "ctool"):
                graphic = a[3]
                if kind == "ctool":
                    gl = parse_graphics(r["custom"]); graphic = gl[0] if gl else 0
                    if not graphic:
                        say("rule %d needs a tool graphic in its Custom box." % (i + 1), Kit.HUE_BAD)
                        auto_off(i, r); return False
                tool = API.FindType(int(graphic), API.Backpack)
                if not tool:
                    if due(st["no_tool"].get(i, 0.0), now):
                        st["no_tool"][i] = now + 10.0
                        say("no tool 0x%04X in your backpack for rule %d." % (int(graphic), i + 1), Kit.HUE_BAD)
                    st["later"][(i, serial)] = now + 10.0; st["run"].discard(i); return False
                HOST.claim_cursor(KEY, TARGET_TIMEOUT + 0.5); j["reader"] = Journal.reader(); API.UseObject(tool.Serial)
            else: j["reader"] = Journal.reader(); API.UseObject(serial); j["phase"] = "recover"
            st["job"] = j; return True
        va_pref = {"t": None}
        def va_prefixes():
            t = va_pref["t"]
            if t is None:
                out = set([APP_NAME.lower() + ":"])
                for sl in HOST.slots:
                    out.add(str(sl.title).lower() + ":")
                    for pt in (sl.parts or ()):
                        if len(pt) > 1: out.add(str(pt[1]).lower() + ":")
                t = va_pref["t"] = tuple(out)
            return t
        def is_answer(j, ln):
            kind = (ln.kind or "").upper()
            if kind == "CLIENT" or ln.low.startswith(va_prefixes()): return False
            who = (ln.name or "").strip().lower()
            if not who or who == "system": return True
            if kind != "OBJECT": return False
            if not j["name"] and not j.get("named"):
                j["named"] = True; it = get_item(j["serial"])
                j["name"] = safe(lambda: str(it.Name or "") if it is not None else "", "")
            return who == j["name"].strip().lower() or ln.text.startswith("[")
        def job_result(j, a):
            rd = j["reader"]
            if rd is None: return None
            lines, raw = j["lines"], j["raw"]; came = False
            for ln in rd.new():
                if ln.text and not ln.text.startswith(TITLE):
                    if not is_answer(j, ln): continue
                    lines.append(ln.low); came = True; raw.append((ln.text, ln.name or ""))
                    if len(lines) > 40: del lines[:-40]; del raw[:-40]
            if not lines: return None
            if not came: return j.get("res")
            res = None
            for rs, words in (("busy", BUSY_WORDS), ("skip", a[8]), ("ok", a[6]), ("fail", a[7])):
                for w in words:
                    for k in range(len(lines)):
                        if w in lines[k]: j["match"] = lines[k]; j["match_raw"] = raw[k][0]; res = rs; break
                    if res is not None: break
                if res is not None: break
            j["res"] = res; return res
        def finish_job(j, r, res, now):
            i, serial = j["rule"], j["serial"]; key = (i, serial); nxt = None
            floor = skill_floor(r) if res == "busy" else 0.0
            if floor > 0 and "must wait" in (j.get("match") or ""):
                st["later"][key] = now + floor; nxt = now + min(r["delay"], floor)
            elif res == "busy":
                n = st["busy_n"].get(key, 0) + 1
                if n >= MAX_BUSY:
                    st["busy_n"].pop(key, None); mark_done(r, serial, 2)
                    add_result(r, serial, 2, j["name"], answer_of(j) or "no answer from the shard", "no answer")
                    say("giving up on 0x%08X (no answer from %s)." % (serial, rule_action(r)[1]), Kit.HUE_BAD)
                else: st["busy_n"][key] = n; st["later"][key] = now + BUSY_RETRY
            elif res == "fail":
                st["busy_n"].pop(key, None); tries = r.setdefault("_tries", {}); n = tries.get(serial, 0) + 1
                if n <= settings["retries"]: tries[serial] = n; st["later"][key] = now + max(r["delay"], 1.0)
                else:
                    tries.pop(serial, None); mark_done(r, serial, 2); add_result(r, serial, 2, j["name"], answer_of(j))
            else:
                st["busy_n"].pop(key, None); code = {"ok": 1, "skip": 3}.get(res, 4); mark_done(r, serial, code)
                add_result(r, serial, code, j["name"], answer_of(j))
            st["job"] = None; waited = max(0.0, now - j.get("t", now))
            st["next_scan"] = nxt if nxt is not None else now + (
                r["delay"] if res == "busy" else max(MIN_DELAY, r["delay"] - waited))
            st["status"] = "%s: %s" % (rule_action(r)[1], res or "done")
            if j.get("match"): r["_last"] = "%s: %s" % (res, j["match"])
            elif j["lines"]:
                r["_last"] = "%s, no phrase matched; the shard said: %s" % (res or "no answer", j["lines"][-1])
            else: r["_last"] = "%s, no journal line in %.1f s" % (res or "no answer", max(0.0, now - j.get("t", now)))
            if len(st["later"]) > 400:
                for k in [k for k, t in st["later"].items() if due(t, now)]: st["later"].pop(k, None)
            if len(st["busy_n"]) > 400: st["busy_n"].clear()
            if len(r.get("_tries", {})) > MAX_DONE: r["_tries"].clear()
        def job_step(now):
            j = st["job"]; r = rules[j["rule"]] if j["rule"] < len(rules) else None
            if r is None: HOST.release_cursor(KEY); st["job"] = None; return
            a = rule_action(r)
            if j["phase"] == "target":
                res = job_result(j, a)
                if res: HOST.release_cursor(KEY); finish_job(j, r, res, now); return
                if HOST.cursor_ok(KEY, "neutral"):
                    API.Target(j["serial"]); HOST.release_cursor(KEY); j["phase"], j["t"] = "recover", now
                elif HOST.cursor_busy(KEY) is None and API.HasTarget("any"):
                    HOST.release_cursor(KEY); finish_job(j, r, "busy", now)
                elif now - j["t"] > TARGET_TIMEOUT: HOST.release_cursor(KEY); finish_job(j, r, "busy", now)
                return
            if now - j["t"] < max(r["delay"], MIN_DELAY):
                res = job_result(j, a)
                if res in ("busy", "skip", "fail"): finish_job(j, r, res, now)
                return
            finish_job(j, r, job_result(j, a), now)
        def guard_check():
            active = not st["paused"] and (bool(st["run"]) or any(r["auto"] and r["bag"] for r in rules)); hold = None
            if active and (settings["guard"] or "attention.up" not in HOST.services): hold = HOST.guard_hold()
            if hold != st["guard_paused"]:
                st["guard_paused"] = hold
                if active:
                    if hold == "guard": msg = "%s: paused in a guard zone; it goes on when you leave." % TITLE
                    elif hold == "unknown":
                        msg = ("%s: paused until the guard zone is known; cross a town's guard line once." % TITLE)
                    else: msg = "%s: out of the guard zone; going on." % TITLE
                    API.SysMsg(msg, Kit.HUE_INFO)
        IDLE_LOOK = 1.5
        def run_jobs(now):
            if st["job"] is not None: job_step(now); return
            if not due(st["next_scan"], now): return
            guard_check()
            if not st["run"] and not any(r["auto"] and r["bag"] for r in rules):
                st["next_scan"] = now + SCAN_EVERY
                if now >= st["idle_at"]: st["idle_at"] = now + IDLE_LOOK; st["status"] = blocked(now) or "Idle"
                return
            st["idle_at"] = 0.0; why = blocked(now)
            if why: st["status"] = why; st["next_scan"] = now + SCAN_EVERY; return
            nxt = pick_next(now)
            if nxt is None:
                st["status"] = "Watching" if any(r["auto"] and r["bag"] for r in rules) else "Idle"
                st["next_scan"] = now + SCAN_EVERY; return
            i, r, serial, it = nxt
            if start_job(i, r, serial, it, now):
                st["status"] = "%s %d/%d" % (rule_action(r)[1], r["_count"][0] + 1, r["_count"][1])
            else: st["next_scan"] = now + SCAN_EVERY
        def pick_bag(i):
            if st["pick"] is not None: say("already targeting a bag.", Kit.HUE_INFO); return
            st["pick"] = i; say("target the bag for rule %d." % (i + 1), Kit.HUE_INFO)
            def done(serial): queue.add(("picked", i, int(serial or 0)), dup=True)
            HOST.pick_target(20, done)
        def bag_picked(i, serial):
            st["pick"] = None
            if i >= len(rules): return
            if not serial: say("cancelled.", Kit.HUE_INFO); return
            it = get_item(serial)
            if it is None or not it.IsContainer: say("that isn't a container.", Kit.HUE_BAD); return
            if not Kit.in_pack(serial): say("that bag isn't in your backpack.", Kit.HUE_BAD); return
            r = rules[i]
            if r["bag"] != serial:
                r["bag"] = serial; r["done"].clear(); del r["order"][:]; st["later"].clear(); invalidate(r)
                clear_results(r)
            save_settings(); say("rule %d uses %s." % (i + 1, bag_name(r, False)), Kit.HUE_GOOD)
            st["redraw"] = True; HOST.refresh_settings(KEY)
        def bags_min(): return W, 2 * Kit.MARGIN + 30 + Kit.GAP + 40 + Kit.GAP + 30 + max(1, len(rules)) * ROW_H + 8
        def build_window():
            mw, mh = bags_min(); z = wnd.slot if Kit.zone_up(KEY) and not st["minimized"] else None
            w, h = z if z is not None and z[0] >= mw and z[1] >= mh else (mw, mh)
            g, store, c = wnd.begin(w, h); M = Kit.MARGIN; rows = []
            if not st["minimized"]:
                IW = w - 2 * M; wnd.frame(g); yb = M + 30 + Kit.GAP; Kit.add_section(g, M, yb, IW, 40)
                c["pause"] = Kit.art_button(g, store, "pause", Kit.ART_PLAY, M + 12, yb + 9,
                                            "Resume" if st["paused"] else "Pause", "Stop or restart every rule",
                                            on_click=queue("pause"))
                x_add = M + 12 + 35 + Kit.text_w("Resume") + 14
                Kit.art_button(g, store, "add", Kit.ART_OK, x_add, yb + 9, "Add rule",
                               "Add a rule (set it up on the settings page)", on_click=queue("add"))
                x_st = x_add + 35 + Kit.text_w("Add rule") + 14
                c["status"] = Kit.add_label(g, "", x_st, yb + 12, Kit.HUE_INFO); c["status_w"] = M + IW - 4 - x_st
                st["full_txt"] = None; yr = yb + 40 + Kit.GAP
                Kit.add_section(g, M, yr, IW, h - yr - M, "RULES  (a bag and an action each)")
                y0 = yr + 30; x_reset = M + IW - 12 - 35 - Kit.text_w("Reset")
                x_run = x_reset - 35 - Kit.text_w("Run") - 6; x_bag = x_run - 35 - Kit.text_w("Bag...") - 6
                x_res = x_bag - 35 - Kit.text_w("Results") - 6; c["last_w"] = IW - 36 - 16
                if not rules:
                    Kit.add_label(g, "No rules yet. Click Add rule, then set its bag and action.",
                                  M + 12, y0 + 5, Kit.HUE_INFO)
                for i, r in enumerate(rules):
                    ry = y0 + i * ROW_H; row = {}
                    row["auto"] = Kit.add_check(g, "", M + 10, ry + 2, r["auto"], "Handle every new item that lands "
                                                "in this bag")
                    row["bag"] = Kit.add_label(g, "", M + 36, ry + 3, Kit.HUE_TEXT)
                    row["act"] = Kit.add_label(g, "", M + 172, ry + 3, Kit.HUE_TITLE)
                    row["prog"] = Kit.add_label(g, "", M + 298, ry + 3, Kit.HUE_INFO)
                    row["last"] = Kit.with_tip(Kit.add_label(g, "", M + 36, ry + 22, Kit.HUE_INFO), "The shard's last "
                                               "answer to this rule and how it was read (ok, fail, skip or busy)")
                    for key, art, bx, cap, tip, act in (
                            ("res", Kit.ART_PAGE, x_res, "Results", "Show the shard's answer per item (again: close)",
                             "results"), ("bag", Kit.ART_PLAY, x_bag, "Bag...", "Target the bag this rule works on",
                             "bag"), ("run", Kit.ART_PLAY, x_run, "Run", "One pass over the items not done yet", "run"),
                            ("reset", Kit.ART_CLOSE, x_reset, "Reset", "Forget what was done, so every item is handled "
                             "again", "reset")):
                        Kit.art_button(g, store, "%s%d" % (key, i), art, bx, ry + 1, cap, tip, on_click=queue((act, i)))
                    row["text"] = (None, None, None, None); rows.append(row)
            wnd.end(g, {"rows": rows}); st["redraw"] = False; refresh()
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, mini=(MINI_W, MINI_H), icon=TRAY_ICON,
                         cleanup=cleanup, lock=True)
        fit = Kit.fit
        def refresh():
            if st["minimized"] and st["docked"]: return
            lbl = win["c"].get("status")
            if lbl is not None:
                hue = (Kit.HUE_BAD if st["paused"] else (Kit.HUE_GOOD if st["job"] else Kit.HUE_INFO))
                key = "mini_txt" if st["minimized"] else "full_txt"; ft = st.get(key)
                if ft is None or ft[0] != st["status"]:
                    ft = st[key] = (st["status"], fit("%s: %s" % (TITLE, st["status"]), MINI_W - 90) if st["minimized"]
                                    else fit(st["status"], win["c"].get("status_w", 400)))
                Kit.set_text(lbl, ft[1], hue)
            if st["minimized"]: return
            now = time.time()
            if now < st["next_rows"]: return
            st["next_rows"] = now + CHECK_EVERY
            for i, row in enumerate(win["rows"]):
                if i >= len(rules): break
                r = rules[i]; cnt = r.get("_count")
                prog = "closed" if r.get("_closed") else "%d/%d" % cnt if cnt else ""
                if st["job"] and st["job"]["rule"] == i: prog += "  working"
                elif i in st["run"]: prog += "  pass"
                last = r.get("_last") or ""; t = (bag_name(r), rule_action(r)[1], prog, last)
                if t != row["text"]:
                    row["text"] = t; Kit.set_text(row["bag"], fit(t[0], 130)); Kit.set_text(row["act"], fit(t[1], 120))
                    Kit.set_text(row["prog"], fit(t[2], 96))
                    Kit.set_text(row["last"], fit("Last: " + last if last else "Last: no answer read yet",
                                                  win["c"].get("last_w", 500)))
        def read_checks():
            changed = False
            for i, row in enumerate(win["rows"]):
                if i >= len(rules): break
                try: v = bool(row["auto"].IsChecked)
                except Exception: continue
                if v != rules[i]["auto"]: rules[i]["auto"] = v; changed = True
            if changed: save_settings(); HOST.refresh_settings(KEY)
        RES_NAME_W, RES_TAG_W = 230, 120
        def rule_index(r): return next((k for k in range(len(rules)) if rules[k] is r), -1)
        def show_results(i):
            if i >= len(rules): return
            r = rules[i]
            if resw["rule"] is r and Kit.is_open(resw["g"]): res_close(); return
            resw["rule"], resw["page"] = r, 0
            if Kit.is_open(resw["g"]): resw["dirty"] = True
            else: build_results()
        def res_min(): return RES_MIN_W, RES_FIXED + 4 * RES_ROW_H
        def res_close():
            resw["rule"] = None
            if Kit.zone_up(RES_KEY): build_results()
            else: resultw.close()
        def res_redraw():
            if Kit.zone_up(RES_KEY) or resw["rule"] is not None and resw["g"] is not None: build_results()
            elif resw["g"] is not None: resultw.close()
        def build_results():
            M = Kit.MARGIN; held = Kit.zone_up(RES_KEY); z = resultw.slot if held else None; mw, mh = res_min()
            if z is not None and (z[0] < mw or z[1] < mh): z = None
            w = z[0] if z is not None else RES_W; n = resultw.rows(RES_ROW_H, RES_FIXED, RES_ROWS) if z else RES_ROWS
            h = z[1] if z is not None else RES_FIXED + n * RES_ROW_H; IW = w - 2 * M; sh = h - M - 30 - Kit.GAP - M
            g, store, c = resultw.begin(w, h); Kit.add_window_frame(g, w, h); Kit.add_section(g, M, M, IW, 30)
            if not held:
                Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, "Close the results",
                               on_click=queue("res_close"))
            x_exp = w - M - (10 if held else 66) - 35 - Kit.text_w("Export")
            Kit.art_button(g, store, "export", Kit.ART_OK, x_exp, M + 4, "Export",
                           "Write the results to a file in the VirtueAssistantSettings folder",
                           on_click=queue("res_export"))
            x_clr = x_exp - 12 - 35 - Kit.text_w("Clear")
            Kit.art_button(g, store, "clear", Kit.ART_CLOSE, x_clr, M + 4, "Clear",
                           "Forget these results (items stay done; Reset handles them again)",
                           on_click=queue("res_clear"))
            c["title"] = Kit.add_label(g, "", M + 30, M + 7, Kit.HUE_TITLE); c["title_w"] = x_clr - (M + 30) - 8
            ys = M + 30 + Kit.GAP; Kit.add_section(g, M, ys, IW, sh, "RESULTS  (newest first)")
            x_old = M + IW - 12 - 35 - Kit.text_w("Next")
            Kit.art_button(g, store, "older", Kit.ART_PAGE, x_old, ys + 24, "Next", "Older results",
                           on_click=queue("res_older"))
            x_new = x_old - 10 - 35 - Kit.text_w("Prev")
            Kit.art_button(g, store, "newer", Kit.ART_PAGE, x_new, ys + 24, "Prev", "Newer results",
                           on_click=queue("res_newer"))
            c["page_x"], c["page_y"] = x_new - 8, ys + 28
            c["page"] = Kit.add_label(g, "", c["page_x"], ys + 28, Kit.HUE_INFO)
            c["counts"] = Kit.add_label(g, "", M + 12, ys + 28, Kit.HUE_TEXT)
            c["counts_w"] = x_new - (M + 12) - 16 - Kit.text_w("page 99 of 99")
            c["ans_w"] = IW - 12 - RES_NAME_W - RES_TAG_W - 8; rows = []; y0 = ys + 30 + 24
            for k in range(n):
                ry = y0 + k * RES_ROW_H
                rows.append({"name": Kit.add_label(g, "", M + 12, ry, Kit.HUE_TEXT),
                             "tag": Kit.add_label(g, "", M + 12 + RES_NAME_W, ry, Kit.HUE_INFO),
                             "ans": Kit.add_label(g, "", M + 12 + RES_NAME_W + RES_TAG_W, ry, Kit.HUE_INFO),
                             "tip": None})
            resultw.end(g, {"rows": rows}); refresh_results()
        resultw = Kit.Window(RES_KEY, RES_TITLE, resw, resw, build_results, RES_POS_KEY, default=(260, 220),
                             cleanup=cleanup, lock=True, owner=False, clear={"rows": [], "rule": None, "c": {}})
        RES_HUE = {1: Kit.HUE_GOOD, 2: Kit.HUE_BAD, 3: Kit.HUE_INFO, 4: Kit.HUE_TEXT}
        def refresh_results():
            resw["dirty"] = False; r, rows, c = resw["rule"], resw["rows"], resw["c"]
            if not rows: return
            if r is None:
                Kit.set_text(c["title"], fit(RES_TITLE.upper(), c["title_w"])); Kit.set_text(c["counts"], fit(
                    RES_EMPTY, c["counts_w"])); return
            i = rule_index(r)
            if i < 0: res_close(); return
            per = len(rows); res = r.get("_res") or []; n = len(res); pages = max(1, (n + per - 1) // per)
            pg = resw["page"] = max(0, min(resw["page"], pages - 1))
            Kit.set_text(c["title"], fit("RULE %d RESULTS: %s" % (i + 1, rule_action(r)[1]), c["title_w"]))
            Kit.set_text(c["counts"], fit(counts_text(r), c["counts_w"]))
            ptxt = "page %d of %d" % (pg + 1, pages) if pages > 1 else ""
            if Kit.set_text(c["page"], ptxt) and ptxt:
                Kit.ui_pos(c["page"], c["page_x"] - Kit.text_w(ptxt), c["page_y"])
            top = n - 1 - pg * per; today = time.localtime()[:3]
            for k, row in enumerate(rows):
                idx = top - k
                if idx >= 0:
                    t, serial, name, code, tag, answer = res[idx]; lt = time.localtime(t)
                    when = time.strftime("%H:%M" if lt[:3] == today else "%b %d %H:%M", lt)
                    Kit.set_text(row["name"], fit("%s  %s" % (when, name), RES_NAME_W - 8))
                    hue = Kit.HUE_TITLE if tag == "magic" else RES_HUE.get(code, Kit.HUE_INFO)
                    Kit.set_text(row["tag"], fit(tag, RES_TAG_W - 8), hue)
                    Kit.set_text(row["ans"], fit(answer or "no answer", c["ans_w"]))
                    if row["tip"] != answer: row["tip"] = answer; row["ans"].SetTooltip(answer or "")
                else:
                    for key in ("name", "tag", "ans"): Kit.set_text(row[key], "")
        def export_results():
            r = resw["rule"]; i = rule_index(r) if r is not None else -1
            if i < 0: return
            res = r.get("_res") or []
            if not res: say("rule %d has no results to export yet." % (i + 1), Kit.HUE_INFO); return
            path = Kit.data_path(EXPORT_NAME % (int(API.Player.Serial), i + 1))
            lines = ["Skill Bags results - rule %d: %s on %s" % (i + 1, rule_action(r)[1], bag_name(r, False)),
                     "Exported %s - %s" % (time.strftime("%Y-%m-%d %H:%M"), counts_text(r)), "",
                     "%-19s  %-10s  %-32s  %-18s  %s" % ("Time", "Serial", "Item", "Result", "The shard's answer")]
            for t, s, name, code, tag, answer in res:
                lines.append("%-19s  0x%08X  %-32s  %-18s  %s" % (
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)), s, name, tag, answer))
            st["writes"].append((path, "\n".join(lines) + "\n"))
        def write_files(): write_queue(st["writes"], TITLE, "results")
        def _thread_wanted(): return bool(st["writes"])
        def toggle_pause(action):
            st["paused"] = not st["paused"]; st["idle_at"] = 0.0
            if st["paused"] and st["job"] is not None: HOST.release_cursor(KEY); st["job"] = None
            lbl = win["c"].get("pause")
            if lbl is not None: Kit.set_text(lbl, "Resume" if st["paused"] else "Pause")
            say("%s." % ("paused" if st["paused"] else "resumed"), Kit.HUE_INFO)
        def add_rule(action):
            if len(rules) >= MAX_RULES: say("at most %d rules." % MAX_RULES, Kit.HUE_INFO); return
            rules.append(new_rule()); save_settings(); build_window(); HOST.refresh_settings(KEY)
            if page["f"] is None: HOST.show_settings(KEY)
        def remove_rule(action):
            i = action[1]
            if st["job"] is not None and st["job"]["rule"] == i: HOST.release_cursor(KEY); st["job"] = None
            elif st["job"] is not None and st["job"]["rule"] > i: st["job"]["rule"] -= 1
            gone = rules.pop(i)
            if resw["rule"] is gone: res_close()
            elif resw["rule"] is not None: resw["dirty"] = True
            st["rr"] = 0; st["run"] = set(k - 1 if k > i else k for k in st["run"] if k != i); st["budget"].clear()
            st["later"].clear(); st["busy_n"].clear(); st["no_tool"].clear(); save_settings(); build_window()
            HOST.refresh_settings(KEY)
        def run_rule(action):
            i = action[1]
            if not rules[i]["bag"]:
                say("set the bag for rule %d first (Bag button)." % (i + 1), Kit.HUE_BAD); return
            st["run"].add(i); st["budget"].pop(i, None); st["later"].clear(); invalidate(rules[i])
            st["next_scan"] = 0.0
        def reset_rule(action):
            i = action[1]; rules[i]["done"].clear(); del rules[i]["order"][:]; rules[i].pop("_tries", None)
            rules[i].pop("_last", None); invalidate(rules[i]); st["later"].clear(); save_done()
            say("rule %d will handle every item again (%s)." % (i + 1, bag_name(rules[i])), Kit.HUE_INFO)
        def clear_shown(action):
            if resw["rule"] is not None: clear_results(resw["rule"]); resw["page"] = 0
        def page_step(action): resw["page"] += 1 if action == "res_older" else -1; resw["dirty"] = True
        ACTIONS = {"pause": toggle_pause, "add": add_rule, "remove": remove_rule, "run": run_rule, "reset": reset_rule,
                "bag": lambda action: pick_bag(action[1]), "picked": lambda action: bag_picked(action[1], action[2]),
                "results": lambda action: show_results(action[1]), "res_close": lambda action: res_close(),
                "res_export": lambda action: export_results(), "res_clear": clear_shown, "res_older": page_step,
                "res_newer": page_step}
        DONE_SAVE_EVERY = 5.0; SEC_R = 118
        HINT = ("The OK / FAIL / SKIP phrases that read the shard's answers are RunUO defaults, not checked on this "
                "shard; the window's Last line shows each rule's last answer.")
        TIP_TEXT = "Hex graphics with commas (0x14FC, 0x0E76), or part of a name (treasure map)"
        TIP_CUSTOM = "The skill's client name (Item Identification), or the tool's hex graphic (0x14FC: lockpicks)"
        TIP_DELAY = ("Seconds between items (%g-%g; a skill rule waits at least its 3 or 10 s timer)"
                     % (MIN_DELAY, MAX_DELAY))
        TIP_DEEP = "Also handle items in bags inside it"
        TIP_AUTO = "Handle every new item that lands in the bag (the window's box too)"
        def page_table(w, prow=None, dds=None):
            def rule_sec(i, r):
                def draw(f, x, y):
                    g, yr, row = f.g, y - 30, {}; Kit.add_label(g, "Action:", x + 12, yr + 34)
                    dds.append(("action", i, x + 70, yr + 30, 210, ACTION_NAMES, r["action"]))
                    Kit.with_tip(Kit.add_label(g, "Custom:", x + 296, yr + 34), TIP_CUSTOM)
                    row["custom"] = Kit.with_tip(Kit.add_textbox(g, r["custom"], x + 356, yr + 30, 130, numbers=False),
                                                 TIP_CUSTOM)
                    Kit.art_button(g, f.store, "rm%d" % i, Kit.ART_CLOSE, x + f.w - 12 - 35 - Kit.text_w("Remove"),
                                   yr + 28, "Remove", "Remove this rule", on_click=queue(("remove", i)))
                    Kit.add_label(g, "Items:", x + 12, yr + 62)
                    dds.append(("filt", i, x + 70, yr + 58, 210, FILTER_NAMES, r["filt"]))
                    Kit.with_tip(Kit.add_label(g, "Text:", x + 296, yr + 62), TIP_TEXT)
                    row["text"] = Kit.with_tip(Kit.add_textbox(g, r["text"], x + 356, yr + 58, f.w - 356 - 16,
                                                               numbers=False), TIP_TEXT)
                    Kit.with_tip(Kit.add_label(g, "Delay (s):", x + 12, yr + 90), TIP_DELAY)
                    row["delay"] = Kit.with_tip(Kit.add_textbox(g, "%g" % r["delay"], x + 90, yr + 86, 50,
                                                                numbers=False), TIP_DELAY)
                    row["deep"] = Kit.add_check(g, "Look inside bags within the bag", x + 160, yr + 88, r["deep"],
                                                TIP_DEEP)
                    row["auto"] = Kit.add_check(g, "Auto (watch the bag)", x + 420, yr + 88, r["auto"], TIP_AUTO)
                    prow.append(row)
                return ("RULE %d  (%s)" % (i + 1, fit(bag_name(r, False), 300)), (("custom", 0, draw),), {"sh": SEC_R})
            return ([("OPTIONS", [("check", "hidden", "Pause while hidden", "Using a skill would reveal you"),
                        ("check", "open", "Open bags the client hasn't looked in",
                         "On Run, double-clicks the bag once so its contents are known", {"stay": True}),
                        ("buttons", (("add", Kit.ART_OK, "Add rule", "Add a rule (a bag and an action)",
                                      queue("add")),), {"dx": 400}), ("num", "retries", "Extra tries after a failure:",
                         "Retries after a FAIL phrase (0-9)", None, 0, 9,
                         {"lw": 268, "fw": 40, "ldy": 4, "ltip": True, "h": 2, "clamp": False}),
                        ("check", "guard", "Pause in guard zones", "No skill use in towns or an unknown zone; "
                         "unticked counts only while Skills > Training Alarm is on", {"dx": 380})] +
                     [("note", line, {"h": 18}) for line in Kit.wrap(HINT, w - 24) or [HINT]], {"pad": 6})] +
                    [rule_sec(i, r) for i, r in enumerate(rules)])
        cfg = Kit.Page(settings, page_table)
        def build_config(g, x, y, w):
            prow, dds = [], []; f = Kit.Form(g, x, y, w, settings, page_table(w, prow, dds))
            for kind, i, dx, dy, dw, items, idx in sorted(dds, key=lambda d: -d[3]):
                dd = G.CreateDropDown(dw, list(items), int(idx)); dd.SetPos(dx, dy); g.Add(dd); prow[i][kind] = dd
            page.update({"f": f, "rows": prow, "next_read": 0.0})
        def poll_config():
            f = page["f"]
            if f is None: return
            now = time.time()
            if now < page["next_read"]: return
            page["next_read"] = now + CHECK_EVERY; relist = []; auto_moved = []
            try:
                new = f.read(True); changed = new != settings; settings.update(new)
                for i, row in enumerate(page["rows"]):
                    if i >= len(rules): break
                    r = rules[i]; act_new = False
                    for kind, names in (("action", RULE_ACTIONS), ("filt", FILTERS)):
                        idx = int(row[kind].GetSelectedIndex())
                        if 0 <= idx < len(names) and idx != r[kind]:
                            r[kind] = idx; changed = True; relist.append(r)
                            if kind == "action":
                                act_new = True; r["filt"] = RULE_ACTIONS[idx][5]; r["delay"] = RULE_ACTIONS[idx][4]
                                r["done"].clear(); del r["order"][:]; clear_results(r); page["dirty"] = True; break
                    for k in ("custom", "text"):
                        v = str(row[k].Text or "").strip()
                        if v != r[k]: r[k] = v; changed = True; relist.append(r)
                    if not act_new:
                        d = clamp_delay(str(row["delay"].Text or "").strip(), r["delay"]); d = max(d, skill_floor(r))
                        if abs(d - r["delay"]) > 0.001: r["delay"] = d; changed = True
                    for k in ("deep", "auto"):
                        v = bool(row[k].IsChecked)
                        if v != r[k]: r[k] = v; changed = True; (relist if k == "deep" else auto_moved).append(r)
            except Exception as ex:
                page["f"] = None
                say("settings page error: %s (reopen the page)." % ex, Kit.HUE_BAD); return
            if changed:
                save_settings()
                for r in relist: invalidate(r)
                for r in auto_moved:
                    i = rule_index(r)
                    if 0 <= i < len(win["rows"]):
                        try: win["rows"][i]["auto"].IsChecked = r["auto"]
                        except Exception: st["redraw"] = True
                if page.get("dirty"): page["dirty"] = False; HOST.refresh_settings(KEY)
        def config_closed(): page["f"] = None; page["rows"] = []
        load_settings()
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "paused": False,
                       "job": None, "next_scan": 0.0, "next_check": 0.0, "status": "Idle",
                       "run": set(), "budget": {}, "opening": {}, "later": {}, "pick": None, "redraw": False,
                       "save_done": False, "no_tool": {}, "busy_n": {}, "next_rows": 0.0,
                       "rr": 0, "guard_paused": None, "writes": [], "idle_at": 0.0, "done_at": 0.0,
                       "minimized": wnd.start_min()})
            resw.update({"g": None, "rule": None, "c": {}, "rows": [], "page": 0, "dirty": False, "minimized": False,
                         "shutting": False, "docked": False, "queue": []}); load_settings()
            build_window(); wnd.dock(fit=True, min=bags_min); resultw.dock(fit=True, min=res_min)
            n = sum(1 for r in rules if r["auto"] and r["bag"])
            say("on, %s, %d watching." % (Kit.count(len(rules), "rule"), n), Kit.HUE_GOOD)
        def _tick():
            if win["g"] is None: return
            if Kit.closed(win): return
            now = time.time()
            while st["queue"]:
                action = st["queue"].pop(0); kind = action[0] if isinstance(action, tuple) else action
                if wnd.action(action) or (kind in ("remove", "bag", "run", "reset") and action[1] >= len(rules)):
                    continue
                fn = ACTIONS.get(kind)
                if fn is not None: fn(action)
            if st.get("redraw"): build_window()
            if resw["queue"]: del resw["queue"][:]; res_redraw()
            if resw["dirty"] and resw["g"] is not None: refresh_results()
            if not st["minimized"] and now >= st["next_check"]: st["next_check"] = now + CHECK_EVERY; read_checks()
            run_jobs(now)
            if st.get("save_done") and now >= st["done_at"]:
                st["save_done"] = False; st["done_at"] = now + DONE_SAVE_EVERY; save_done()
            refresh()
        def _interval(): j = st["job"]; return 0.05 if j is not None and j["phase"] == "target" else 0.1
        def _stop():
            st["shutting"] = resw["shutting"] = True
            if st["job"] is not None: HOST.release_cursor(KEY); st["job"] = None
            save_settings(); cleanup.close()
            if st["writes"]:
                if Client.on_client_thread():
                    say("the export wasn't written (the module stopped); export again.", Kit.HUE_INFO)
                    del st["writes"][:]
                else: write_files()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": build_config, "poll_config": poll_config, "config_closed": config_closed,
                "thread_tick": write_files, "thread_wanted": _thread_wanted, "interval": _interval}
    PARTS = (("window", _part_window, 0.25, "skills"), ("alarm", _part_alarm, 0.1, "attention"),
        ("bags", _part_bags, 0.1, "skillbags"),)
    return PartSet(KEY, TITLE, PARTS).hooks()


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("skills", "Skills", "Skills, training and AFK alarms", _module_skills, 0.1,
         category="Skills and home", parts=(("window", "Skills Window",
              "Skills with locks, groups and gains", True, ("skills",)),
             ("alarm", "Training Alarm", "Alarm when staff or a gump needs you", False,
              ("attention",)), ("bags", "Skill Bags", "A skill on each item in a bag, once", False, ("skillbags",)),),
         aliases=('Skill Bags', 'Attention', 'GM check', 'training', 'locks', 'gains', 'Item ID'))
