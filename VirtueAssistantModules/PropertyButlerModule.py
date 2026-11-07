def _module_butler():
    KEY = "butler"; TITLE = "Property Butler"; SETTINGS_KEY = "PropertyButler_settings"; POS_KEY = "PropertyButler_pos"
    VIEW_KEY = "PropertyButler_view"; MIN_KEY = "PropertyButler_min"; LOG_KEY = "PropertyButler_log"
    LOG_POS_KEY = "PropertyButler_log_pos"; W = 520; MINI_W, MINI_H = 300, 46; TRAY_ICON = 0x0BD2; MAX_ROWS = 8
    ROW_H = 22; LOG_LINES = 3; LOG_KEEP = 30; LOG_W = 520; LOG_ROW_H = 18; LOG_SAVE_EVERY = 1.0; NAME_CACHE_SECS = 2.5
    NAME_CACHE_MAX = 200; PICK_WAIT = 15.0; VISITS_KEY = "PropertyButler_visits"
    LOG_VIEW_KEY = "PropertyButler_log_view"; VISIT_KEEP = 30; VISIT_MERGE = 60.0; VISIT_SAVE_EVERY = 5.0
    HOUSE_EVERY = 2.0; HOUSE_CHECKS = 6; EJECT_FOE_EVERY = 10.0; FOE_SERVICE = "ultima.is_foe"
    DETECT_SKILL = "Detect Hidden"; DEFAULT_COOLDOWN = 10.0; COOLDOWN_MIN, COOLDOWN_MAX = 3.0, 120.0; DEFAULT_RANGE = 12
    RANGE_MIN, RANGE_MAX = 1, 18; CURSOR_WAIT = 3.0; REPLY_WAIT = 3.0; REVEAL_WINDOW = 1.0; RETRY_SOON = 1.5
    CONFIRM_SECS = 3.0; STILL_SECS = 1.0; SCAN_EVERY = 0.3; HELD_EVERY = 0.5; REVEAL_SOUND = 0x01F1
    ALERT_REVEAL = "butler.revealed"; ALERT_FOE = "butler.foe"; ALERT_FOE_SOUND = 0x338
    HELD_UNKNOWN = HOLD_TEXT["unknown"]
    J_WAIT = ("must wait a few moments to use another skill", "must wait to perform another action")
    J_NOTHING = ("you can see nothing hidden there",)
    J_REVEAL = ("reveal one other person", "reveal several people", "you carefully check the house")
    J_DONE = {"eject": ("has been ejected from this house",), "ban": ("has been banned from this house",),
              "friend": ("is now a friend of this house", "made a friend of this house"), "lock": ("locked down!",),
              "release": ("no longer locked down",)}
    J_HOUSE_NO = ("you are not around your house", "not a co-owner of this house",
                  "only the house owner", "this person is already banned",
                  "is already the house owner", "already a house owner",
                  "cannot eject a friend", "not in your house", "already a friend",
                  "cannot be a friend of the house", "can't be a friend of the house",
                  "is already locked down", "isn't locked down", "is not locked down",
                  "cannot lock", "cannot be locked down", "refuse to lock this down",
                  "did not lock this down", "may not release this", "locked down items would be exceeded",
                  "place it on the ground first", "when the front door is open")
    CMDS = {"eject": ("eject_cmd", "ejected", "mobile"), "ban": ("ban_cmd", "banned", "mobile"),
            "friend": ("friend_cmd", "befriended", "mobile"), "lock": ("lock_cmd", "locked down", "item"),
            "release": ("release_cmd", "released", "item")}
    VERBS = {"eject": "Eject", "ban": "Ban", "friend": "Befriend", "lock": "Lock down", "release": "Release"}
    EMPTY_ROWS = "Nobody near you. Players within range appear here."
    EMPTY_LOG = "No actions yet: ejects, bans and reveals go here."
    EMPTY_VISITS = "No visits yet: players who step into your house go here."
    settings = {"cooldown": DEFAULT_COOLDOWN, "range": DEFAULT_RANGE, "still": False, "sound": True, "friends": True,
                "confirm": True, "eject_cmd": "Remove thyself", "ban_cmd": "I ban thee",
                "friend_cmd": "I wish to make this a friend", "lock_cmd": "I wish to lock this down",
                "release_cmd": "I wish to release this", "say_replies": False, "eject_foes": False}
    DEFAULTS = dict(settings)
    FIELDS = ("still", "sound", "friends", "confirm", "eject_cmd", "ban_cmd", "friend_cmd", "lock_cmd",
              "release_cmd", "say_replies", "eject_foes")
    st = {"minimized": False, "queue": [], "sweep": False, "next_at": 0.0, "deadline": 0.0, "cast_at": 0.0,
          "seen": set(), "sweeps": 0, "revealed": 0, "eject_at": {}, "no_multi_said": False}
    win = {"g": None, "c": {}, "rows": [], "store": ({}, {}), "log_g": None, "log_rows": [], "log_view": "log"}
    page = {"f": None}; log = []; visits = []
    NOTO_HUE = {"innocent": 90, "ally": 68, "gray": 946, "criminal": 946, "murderer": 33,
                "enemy": 43, "invulnerable": 53}
    NOTO_NAMES = {}; OWN_PREFIX = TITLE.lower() + ":"; OWN_REPLY_PREFIX = TITLE.lower() + ": reply:"
    def load_settings():
        p = Kit.get_var(SETTINGS_KEY).split("|")
        if len(p) >= 8:
            for i, k, lo, hi, cast in ((0, "cooldown", COOLDOWN_MIN, COOLDOWN_MAX, float),
                                       (1, "range", RANGE_MIN, RANGE_MAX, int)):
                try: settings[k] = max(lo, min(hi, cast(p[i])))
                except Exception: pass
            p = p + [""] * (13 - len(p))
            for i, k in enumerate(FIELDS, 2):
                settings[k] = p[i] == "1" if isinstance(DEFAULTS[k], bool) else p[i] or DEFAULTS[k]
        st["sweep"] = Kit.get_var(VIEW_KEY) == "1"; del log[:]
        for line in Kit.get_var(LOG_KEY).split("\n"):
            q = line.split("\t")
            if len(q) >= 3:
                try: log.append((float(q[0]), q[2], int(q[1])))
                except Exception: pass
        del log[:-LOG_KEEP]; del visits[:]
        for line in Kit.get_var(VISITS_KEY).split("\n"):
            q = line.split("\t", 6)
            if len(q) >= 7:
                try:
                    visits.append([float(q[0]), float(q[1]), int(q[2]), q[6], q[3] or "unknown",
                                   max(1, int(q[4])), int(q[5])])
                except Exception: pass
        del visits[:-VISIT_KEEP]; win["log_view"] = "visits" if Kit.get_var(LOG_VIEW_KEY) == "visits" else "log"
    def save_settings():
        Kit.put_var(SETTINGS_KEY, "|".join(["%.1f" % settings["cooldown"], str(settings["range"])] + [
            ("1" if settings[k] else "0") if isinstance(DEFAULTS[k], bool) else settings[k].replace("|", "/")
            for k in FIELDS]))
        Kit.put_var(VIEW_KEY, "1" if st["sweep"] else "0")
    def save_log():
        st["log_dirty"] = False
        Kit.put_var(LOG_KEY, "\n".join(["%d\t%d\t%s" % (t, hue, text.replace("\t", " ").replace("\n", " "))
                                         for (t, text, hue) in log[-LOG_KEEP:]]))
    def save_log_soon(): st["log_dirty"] = True
    def save_visits():
        st["visits_dirty"] = False
        Kit.put_var(VISITS_KEY, "\n".join(["%d\t%d\t%d\t%s\t%d\t%d\t%s" % (
            e[0], e[1], e[2], str(e[4]).replace("\t", " "), e[5], e[6],
            str(e[3]).replace("\t", " ").replace("\n", " ")) for e in visits[-VISIT_KEEP:]]))
    def visits_changed():
        st["visits_dirty"] = True
        if win["log_view"] == "visits" and win["log_g"] is not None: st["visits_redraw"] = True
    def add_log(text, hue=None):
        hue = Kit.HUE_INFO if hue is None else hue; log.append((time.time(), text, hue)); del log[:-LOG_KEEP]
        save_log_soon(); say(text + ("" if text.endswith((".", "!", "?")) else "."), hue); refresh_log()
    say = Kit.sayer(TITLE)
    def note(text, secs=4.0): st["note"], st["note_until"] = text, time.time() + secs
    def noto_name(mob):
        try: v = mob.Notoriety
        except Exception: return "unknown"
        try: return NOTO_NAMES[v]
        except KeyError: pass
        except Exception: return str(v).split(".")[-1].lower()
        n = NOTO_NAMES[v] = str(v).split(".")[-1].lower(); return n
    def has_target():
        try: return bool(API.HasTarget("any"))
        except Exception: return False
    def cursor_free(): return HOST.cursor_busy(KEY) is None and not has_target()
    def short(name, width): return Kit.fit(name or "(unknown)", width)
    def find_t(kind, serial):
        return safe(lambda: (API.FindMobile if CMDS[kind][2] == "mobile" else API.FindItem)(serial))
    def who(h): return VERBS[h["kind"]].lower(), h["name"] or "the target"
    queue = Kit.queuer(st); on_disposed = Kit.disposer(KEY, st, win); SWEEP_H = 82; NAME_W = 150; LOG_PITCH = 20
    VIS_H = 30 + MAX_ROWS * ROW_H + 8; ACT_H = 30 + 26 + 26 + LOG_LINES * LOG_PITCH + 8
    H = Kit.MARGIN + 30 + Kit.GAP + SWEEP_H + Kit.GAP + VIS_H + Kit.GAP + ACT_H + Kit.MARGIN; MIN_ROWS = 2
    NAME_MIN = 60; RUNNING = "A house command is still running: wait for it"
    NO_CURSOR = "A target cursor is up: press Esc or use it first"; ALT = ". Alt+click: auto-follow (again to stop)"
    LAST_TIP = "Set them as your last target" + ALT
    def save_pos(): Kit.save_pos(POS_KEY, win["g"])
    fit = {"slot": None, "k": 1.0, "full": None}
    def layout_fit(w, h, mode):
        new = (int(w), int(h)) if (w is not None and h is not None) else None
        if new != fit["slot"] or (mode == "again" and new is not None): fit["slot"] = new; queue("redraw")()
    def drawn_at(): return fit["k"], fit["full"]
    def at_k(ctrl, x, y):
        k = fit["k"]
        if k != 1.0: ctrl.SetPos(int(round(x * k)), int(round(y * k)))
        else: Kit.ui_pos(ctrl, x, y)
    def cap_w(text): return 35 + Kit.text_w(text)
    ACTIONS = ((("pick_ej", Kit.ART_PLAY, "Eject...", "Target a player to eject from the house", "pick_eject"),
                ("pick_ban", Kit.ART_CLOSE, "Ban...", "Target a player to ban from the house", "pick_ban"),
                ("pick_fr", Kit.ART_OK, "Friend...", "Target a player to make a friend of the house", "pick_friend")),
               (("pick_lock", Kit.ART_OK, "Lock down...", "Target an item in the house to lock " "down", "pick_lock"),
                ("pick_rel", Kit.ART_CLOSE, "Release...", "Target a locked-down item to release it", "pick_release"),
                ("clear", Kit.ART_CLOSE, "Clear log",
                 "Forget the actions listed below (the visitor log stays)", "clear_log"),
                ("showlog", Kit.ART_PAGE, "Show log",
                 "Open the log window: the last %d actions and the visitor log (again to close it)"
                 % LOG_KEEP, "show_log")))
    def flow(items, x0, right):
        out, x, row = [], x0, 0
        for cap in items:
            w = cap_w(cap)
            if x > x0 and x + w > right: x, row = x0, row + 1
            out.append((x, row)); x += w + 16
        return out
    def btn_line_w(): return cap_w("Friend") + 12 + cap_w("Eject") + 12 + cap_w("Ban")
    def min_w(): return 2 * Kit.MARGIN + 12 + max(btn_line_w(), NAME_MIN + 6 + Kit.text_w("18 tiles")) + 10
    def layout(w, h):
        M = Kit.MARGIN; IW = w - 2 * M; ys = M + 30 + Kit.GAP; sw_w = max(cap_w("Sweep: off"), cap_w("Sweep: on"))
        one = 10 + sw_w + 16 + cap_w("Sweep now") <= IW - 4; sweep_h = SWEEP_H if one else SWEEP_H + 26
        count_room = min(Kit.text_w("999 sweeps, 999 revealed"), max(40, IW - 20 - 80)); yv = ys + sweep_h + Kit.GAP
        dist_w = Kit.text_w("18 tiles"); single = 12 + NAME_MIN + 6 + dist_w + 10 + btn_line_w() + 10 <= IW
        row_h = ROW_H if single else 2 * ROW_H
        if single:
            x_ban = M + IW - 10 - cap_w("Ban"); x_ej = x_ban - 12 - cap_w("Eject"); x_fr = x_ej - 12 - cap_w("Friend")
            x_dist = x_fr - 10 - dist_w
        else:
            x_fr = M + 12; x_ej = x_fr + cap_w("Friend") + 12; x_ban = x_ej + cap_w("Eject") + 12
            x_dist = M + IW - 10 - dist_w
        groups, rows_used = [], 0
        for grp in ACTIONS:
            fl = flow([b[2] for b in grp], M + 10, M + IW - 4); groups.append([(x, rows_used + r) for x, r in fl])
            rows_used += fl[-1][1] + 1
        fixed = (M + 30 + Kit.GAP + sweep_h + Kit.GAP + 30 + 8 + Kit.GAP + 30 + 26 * rows_used + 8 + M)
        if h is None: rows_n, log_n = MAX_ROWS, LOG_LINES
        else:
            room = h - fixed; log_n, rows_n = LOG_LINES, MAX_ROWS
            while log_n > 1 and rows_n * row_h + log_n * LOG_PITCH > room: log_n -= 1
            while rows_n > MIN_ROWS and rows_n * row_h + log_n * LOG_PITCH > room: rows_n -= 1
            while rows_n == MAX_ROWS and log_n < LOG_KEEP and rows_n * row_h + (log_n + 1) * LOG_PITCH <= room:
                log_n += 1
        vis_h = 30 + rows_n * row_h + 8; act_h = 30 + 26 * rows_used + log_n * LOG_PITCH + 8
        nat = fixed - (30 + 8) - (30 + 26 * rows_used + 8) + vis_h + act_h
        if h is not None and h > nat: vis_h += h - nat
        ya = yv + vis_h + Kit.GAP
        return {"IW": IW, "ys": ys, "sweep_xy": (M + 10, ys + 26), "sweep_h": sweep_h, "yv": yv, "row_h": row_h,
                "now_xy": (M + 10 + sw_w + 16, ys + 26) if one else (M + 10, ys + 52),
                "status_y": ys + 58 if one else ys + 84, "count_room": count_room,
                "status_room": max(40, IW - 20 - count_room - 10), "btn_dy": 0 if single else ROW_H,
                "x": (x_fr, x_ej, x_ban, x_dist), "dist_w": dist_w,
                "name_w": max(20, min(NAME_W, x_dist - 6 - (M + 12))),
                "empty": Kit.wrap(EMPTY_ROWS, max(60, IW - 24)), "act_rows": rows_used, "groups": groups,
                "rows_n": rows_n, "log_n": log_n, "vis_h": vis_h, "act_h": act_h, "ya": ya, "h": ya + act_h + M}
    def section_title(title, hint, room):
        full = "%s  (%s)" % (title, hint); return full if Kit.text_w(full) <= room else title
    def build_window():
        slot = fit["slot"]
        if st["minimized"]: w, h = (max(MINI_W, slot[0]) if slot else MINI_W), MINI_H
        elif slot is None: w, h = W, H
        else: w, h = slot
        x, y = Kit.load_pos(POS_KEY, (200, 200), (w, h))
        if Kit.is_open(win["g"]): x, y = win["g"].GetX(), win["g"].GetY()
        old, win["g"] = win["g"], None; M = Kit.MARGIN; store, c, rows = ({}, {}), {}, []; g = G.CreateGump(True, True)
        k = 1.0; fit["k"], fit["full"] = 1.0, None
        if st["minimized"]: c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min")); c["mini_w"] = w
        else:
            lw, lh, body = w, h, None
            if slot is None: P = layout(lw, None); lh = P["h"]
            elif w < min_w():
                k = w / float(min_w()); P = layout(min_w(), int(h / k))
                if P["h"] > int(h / k) + 1: k = min(k, h / float(P["h"]))
                lw, lh = int(round(w / k)), int(round(h / k)); P = layout(lw, lh)
            else:
                P = layout(lw, lh)
                if P["h"] > lh + 1: lw = w - Kit.SCROLL_BAND; P = layout(lw, lh); body = P["h"]
            win["P"] = P; IW = P["IW"]; Kit.add_window_frame(g, lw, lh)
            Kit.title_bar(g, store, lw, TITLE, KEY, queue("toggle_min"), queue("to_bar"), queue("settings"))
            ys = P["ys"]
            Kit.add_section(g, M, ys, IW, P["sweep_h"],
                            section_title("SWEEP", "Detect Hidden on your own spot", IW - 12))
            c["sweep_lbl"] = Kit.art_button(g, store, "sweep", Kit.ART_PAGE, P["sweep_xy"][0],
                                            P["sweep_xy"][1], "Sweep: off",
                                            "Click to switch the automatic sweep on or off; on, "
                                            "Detect Hidden is used on your spot whenever it is ready",
                                            on_click=queue("sweep"))
            Kit.art_button(g, store, "now", Kit.ART_PLAY, P["now_xy"][0], P["now_xy"][1], "Sweep now",
                           "Use Detect Hidden once now, if the skill is ready", on_click=queue("now"))
            c["status"] = Kit.add_label(g, "", M + 10, P["status_y"], Kit.HUE_INFO)
            c["count"] = Kit.add_label(g, "", M + IW - 10, P["status_y"], Kit.HUE_INFO); c["count_y"] = P["status_y"]
            yv = P["yv"]; near_w = Kit.text_w("99 near (%d shown)" % MAX_ROWS)
            Kit.add_section(g, M, yv, IW, P["vis_h"],
                            section_title("VISITORS", "players near you", IW - 12 - near_w - 16))
            c["near"] = Kit.add_label(g, "", M + IW - 10, yv + 6, Kit.HUE_INFO); c["near_y"] = yv + 6
            x_fr, x_ej, x_ban, x_dist = P["x"]; c["name_w"], c["hidden_w"] = P["name_w"], Kit.text_w(" (hidden)")
            say = "Say the house's %s command and aim it at them"
            btns = (("fr", Kit.ART_OK, x_fr, "Friend", say % "friend" + ALT, "friend"),
                    ("ej", Kit.ART_PLAY, x_ej, "Eject", say % "eject" + ALT, "eject"),
                    ("ban", Kit.ART_CLOSE, x_ban, "Ban", say % "ban" + ("; a second click within %d s confirms"
                     % int(CONFIRM_SECS) if settings["confirm"] else "") + ALT, "ban"))
            row_h, bdy = P["row_h"], P["btn_dy"]
            for i in range(P["rows_n"]):
                ry = yv + 30 + i * row_h; row = {"val": None, "prev": None, "changed": 0.0}
                row["name_lbl"] = Kit.add_label(g, "", M + 12, ry + 3, Kit.HUE_TEXT)
                row["dist_lbl"] = Kit.add_label(g, "", x_dist, ry + 3, Kit.HUE_INFO)
                row["catch"] = Kit.catcher(g, M + 10, ry, x_dist - M - 10 + P["dist_w"], ROW_H,
                                           Kit.row_clicker(row, queue, "last"), LAST_TIP)
                for bk, art, bx, cap, tip, act in btns:
                    row[bk] = Kit.art_button(g, store, "%s%d" % (bk, i), art, bx, ry + bdy, cap, tip,
                                             on_click=Kit.row_clicker(row, queue, act))
                    row[bk + "_btn"] = store[0]["%s%d" % (bk, i)]
                rows.append(row)
            c["empty"] = [Kit.add_label(g, line, M + 12, yv + 33 + 20 * i, Kit.HUE_INFO)
                          for i, line in enumerate(P["empty"][:max(1, (P["vis_h"] - 33) // 20)])]
            ya = P["ya"]
            Kit.add_section(g, M, ya, IW, P["act_h"], section_title("ACTIONS", "pick with a target cursor", IW - 12))
            for grp, places in zip(ACTIONS, P["groups"]):
                for (key, art, cap, tip, act_), (bx, brow) in zip(grp, places):
                    Kit.art_button(g, store, key, art, bx, ya + 26 + 26 * brow, cap, tip, on_click=queue(act_))
            ly = ya + 30 + 26 * P["act_rows"]
            c["log"] = [Kit.add_label(g, "", M + 12, ly + i * LOG_PITCH, Kit.HUE_INFO) for i in range(P["log_n"])]
            c["log_w"], c["log_full"] = IW - 70, IW - 24
            if k != 1.0:
                fit["k"], fit["full"] = k, (int(min_w()), int(round(layout(min_w(), None)["h"])))
                Kit.scale_window(g, k)
            elif body is not None: w, h = lw, body
            else: w, h = lw, lh
        Kit.show_window(g, x, y, w, h, KEY, st["minimized"] and st["docked"], on_disposed(g), save_pos, win,
                        {"g": g, "c": c, "rows": rows, "store": store},
                        slot[1] if (slot is not None and not st["minimized"]) else None)
        refresh_log(); refresh_rows(); refresh_status(); Kit.dispose(old)
    ROW_CTRLS = ("name_lbl", "dist_lbl", "catch", "fr", "fr_btn", "ej", "ej_btn", "ban", "ban_btn")
    def set_vis(ctrl, on, row, key):
        if row.get(key + "_vis") != on:
            row[key + "_vis"] = on
            try: ctrl.IsVisible = on
            except Exception: pass
    def refresh_rows():
        rows = win["rows"]
        if not rows or st["minimized"]: return
        c = win["c"]; vis = st["visitors"]; now = time.time(); name_w, hidden_w = c["name_w"], c["hidden_w"]
        for i, row in enumerate(rows):
            if i < len(vis):
                v = vis[i]; Kit.row_set(row, (v["serial"], v["name"]), now)
                sig = (v["serial"], v["name"], v["noto"], v["hidden"], v["dist"], name_w, hidden_w)
                if row.get("sig") == sig: continue
                row["sig"] = sig; hue = NOTO_HUE.get(v["noto"], Kit.HUE_TEXT)
                if v["hidden"]:
                    hue = Kit.HUE_TITLE
                    Kit.set_text(row["name_lbl"], short(v["name"], name_w - hidden_w) + " (hidden)", hue)
                else: Kit.set_text(row["name_lbl"], short(v["name"], name_w), hue)
                Kit.set_text(row["dist_lbl"], "%d tile%s" % (v["dist"], "" if v["dist"] == 1 else "s"))
                for k in ROW_CTRLS: set_vis(row[k], True, row, k)
            else:
                Kit.row_set(row, None, now); row["sig"] = None
                for k in ROW_CTRLS: set_vis(row[k], False, row, k)
        lines = win["P"]["empty"]; ek = c.get("empty_k")
        if ek is None or ek[0] != (not vis) or ek[1] is not lines:
            c["empty_k"] = (not vis, lines)
            for i, lbl in enumerate(c["empty"]): Kit.set_text(lbl, lines[i] if (not vis and i < len(lines)) else "")
        near = c["near"]; nk = (st["near"], len(vis) > len(rows), len(rows))
        if c.get("near_k") != nk:
            c["near_k"] = nk; txt = "%d near" % st["near"] if st["near"] else ""
            if len(vis) > len(rows): txt = "%d near (%d shown)" % (st["near"], len(rows))
            Kit.set_text(near, txt); tw = Kit.text_w(txt)
            if c.get("near_w") != tw:
                c["near_w"] = tw; IW = win["P"]["IW"]; safe(lambda: at_k(near, Kit.MARGIN + IW - 10 - tw, c["near_y"]))
    def log_line(entry, width):
        t, text, hue = entry; return "%s  %s" % (time.strftime("%H:%M", time.localtime(t)), short(text, width)), hue
    def refresh_log():
        c = win["c"]; lbls = c.get("log")
        if lbls:
            tail = log[-len(lbls):]
            for i, lbl in enumerate(lbls):
                if i < len(tail):
                    text, hue = log_line(tail[len(tail) - 1 - i], c["log_w"]); Kit.set_text(lbl, text, hue)
                elif i == 0: Kit.set_text(lbl, Kit.fit(EMPTY_LOG, c["log_full"]), Kit.HUE_INFO)
                else: Kit.set_text(lbl, "")
        refresh_logwin()
    def save_log_pos(): Kit.save_pos(LOG_POS_KEY, win["log_g"])
    def on_log_disposed(g):
        def handler(*args):
            if win["log_g"] is g: win["log_g"], win["log_rows"] = None, []
        return handler
    def build_logwin():
        M = Kit.MARGIN; visits_view = win["log_view"] == "visits"
        lines, keep = (visits, VISIT_KEEP) if visits_view else (log, LOG_KEEP)
        n = min(keep, max(10, (len(lines) + 9) // 10 * 10)); sh = 30 + n * LOG_ROW_H + 8
        w, h = LOG_W, M + 30 + Kit.GAP + sh + M; x, y = Kit.load_pos(LOG_POS_KEY, (240, 240), (w, h))
        old = win["log_g"]
        if Kit.is_open(old): x, y = old.GetX(), old.GetY()
        win["log_g"] = None; store = ({}, {}); g = G.CreateGump(True, True); Kit.add_window_frame(g, w, h)
        Kit.add_section(g, M, M, w - 2 * M, 30)
        Kit.add_label(g, "%s LOG" % TITLE.upper(), M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, "Close", on_click=queue("show_log"))
        x_clr = w - M - 54 - 12 - 35 - Kit.text_w("Clear")
        Kit.art_button(g, store, "clear", Kit.ART_CLOSE, x_clr, M + 4, "Clear",
                       "Forget every visit in this list" if visits_view else "Forget every action in this list",
                       on_click=queue("log_clear"))
        cap = "Actions" if visits_view else "Visitors"
        Kit.art_button(g, store, "view", Kit.ART_PAGE, x_clr - 12 - 35 - Kit.text_w(cap), M + 4, cap,
                       "Show the action log: what the butler did, newest first" if visits_view else
                       "Show the visitor log: who came into the house while you stood in it",
                       on_click=queue("log_view"))
        ys = M + 30 + Kit.GAP
        Kit.add_section(g, M, ys, w - 2 * M, sh, "VISITORS  (while you stood in the house)" if visits_view
                        else "ACTIONS  (newest first; %d are kept)" % LOG_KEEP)
        rows = []
        for i in range(n):
            ry = ys + 30 + i * LOG_ROW_H
            row = {"lbl": Kit.add_label(g, "", M + 12, ry, Kit.HUE_INFO), "catch": None,
                   "val": None, "prev": None, "changed": 0.0}
            if visits_view:
                row["catch"] = Kit.catcher(g, M + 10, ry - 1, w - 2 * M - 20, LOG_ROW_H,
                                           Kit.row_clicker(row, queue, "last"), LAST_TIP)
            rows.append(row)
        Kit.show_window(g, x, y, w, h, None, False, on_log_disposed(g), save_log_pos, win,
                        {"log_g": g, "log_rows": rows})
        refresh_logwin(); Kit.dispose(old)
    def visit_line(e, width, now):
        t_in, t_out, serial, name, noto, times, flag = e; lt = time.localtime(t_in)
        when = time.strftime("%H:%M" if lt[:3] == time.localtime(now)[:3] else "%b %d %H:%M", lt)
        if st["open_visits"].get(serial) is e: when += ", inside now"
        elif t_out: when += "-" + time.strftime("%H:%M", time.localtime(t_out))
        else: when += "-?"
        tail = " (%s)" % noto
        if times > 1: tail += "  in %d times" % times
        if flag: tail += "  banned" if flag == 2 else "  ejected"
        name_w = max(60, width - Kit.text_px(when + "  " + tail))
        return "%s  %s%s" % (when, short(name, name_w), tail), NOTO_HUE.get(noto, Kit.HUE_TEXT)
    def refresh_logwin():
        g = win["log_g"]
        if not Kit.is_open(g): return
        rows = win["log_rows"]; visits_view = win["log_view"] == "visits"; lines = visits if visits_view else log
        if len(lines) > len(rows): build_logwin(); return
        n = len(lines); now = time.time()
        for i, row in enumerate(rows):
            if i < n:
                e = lines[n - 1 - i]
                if visits_view:
                    key = (e[0], e[2], e[1], e[5], e[6], st["open_visits"].get(e[2]) is e)
                    if row.get("key") != key:
                        row["key"] = key; text, hue = visit_line(e, LOG_W - 2 * Kit.MARGIN - 28, now)
                        Kit.set_text(row["lbl"], text, hue)
                    Kit.row_set(row, (e[2], e[3]), now)
                else: text, hue = log_line(e, LOG_W - 2 * Kit.MARGIN - 70); Kit.set_text(row["lbl"], text, hue)
            else:
                if i == 0: Kit.set_text(row["lbl"], EMPTY_VISITS if visits_view else EMPTY_LOG, Kit.HUE_INFO)
                else: Kit.set_text(row["lbl"], "")
                row["key"] = None; Kit.row_set(row, None, now)
            if row["catch"] is not None: set_vis(row["catch"], i < n, row, "catch")
    def status_text(now):
        if st["house"] is not None:
            h = st["house"]
            return ("%s %s: waiting for the house's cursor" % (VERBS[h["kind"]], h["name"] or "the target"),
                    Kit.HUE_TITLE)
        hw = st["house_wait"]
        if hw is not None:
            return ("%s %s: waiting for the sweep's cursor to pass" % (VERBS[hw["kind"]], hw["name"] or "the target"),
                    Kit.HUE_TITLE)
        if st["note"] and now < st["note_until"]: return st["note"], Kit.HUE_INFO
        if st["phase"] == "cursor": return "Detect Hidden: waiting for its cursor", Kit.HUE_TITLE
        if st["phase"] == "cast": return "Detect Hidden: sweeping", Kit.HUE_GOOD
        if not st["sweep"]:
            rem = st["next_at"] - now
            if rem > 0: return "Sweep off; Detect Hidden ready in %d s" % int(rem + 0.99), Kit.HUE_INFO
            return "Sweep off; Detect Hidden ready", Kit.HUE_INFO
        if st["held"] == HELD_UNKNOWN: return HELD_UNKNOWN, Kit.HUE_INFO
        if st["held"]: return "Sweep on, waiting: %s" % st["held"], Kit.HUE_INFO
        rem = st["next_at"] - now
        if rem > 0: return "Sweep on: next in %d s" % int(rem + 0.99), Kit.HUE_GOOD
        if settings["still"] and now - st["moved_at"] < STILL_SECS:
            return "Sweep on: waiting until you stand still", Kit.HUE_INFO
        return "Sweep on: ready", Kit.HUE_GOOD
    def mini_text():
        if st["house"] is not None or st["house_wait"] is not None: s = "house command"
        elif st["phase"] != "idle": s = "sweeping"
        elif st["sweep"]: s = "sweep on, waiting" if st["held"] else "sweep on"
        else: s = "sweep off"
        if st["near"]: s += ", %d near" % st["near"]
        return "%s: %s" % (TITLE, s)
    def cut_once(c, key, text, room):
        e = c.get(key)
        if e is not None and e[0] == text and e[1] == room: return e[2]
        cut = short(text, room); c[key] = (text, room, cut); return cut
    def refresh_status():
        c = win["c"]
        if win["g"] is None or (st["minimized"] and st["docked"]): return
        now = time.time(); text, hue = status_text(now)
        if st["minimized"]:
            lbl = c.get("status")
            if lbl is not None: Kit.set_text(lbl, cut_once(c, "mini_k", mini_text(), c.get("mini_w", MINI_W) - 90), hue)
            return
        P = win.get("P") or {}; lbl = c.get("status")
        if lbl is not None:
            cut = cut_once(c, "status_k", text, P.get("status_room", W - 2 * Kit.MARGIN - 160))
            if Kit.set_text(lbl, cut, hue): safe(lambda: lbl.SetTooltip(text if cut != text else ""))
        sl = c.get("sweep_lbl")
        if sl is not None:
            Kit.set_text(sl, "Sweep: on" if st["sweep"] else "Sweep: off",
                         Kit.HUE_GOOD if st["sweep"] else Kit.HUE_TEXT)
        cnt = c.get("count"); ck = (st["sweeps"], st["revealed"], P.get("count_room", 400))
        if cnt is not None and c.get("count_k") != ck:
            c["count_k"] = ck
            txt = ("%d sweep%s, %d revealed" % (st["sweeps"], "" if st["sweeps"] == 1 else "s", st["revealed"]))
            txt = Kit.fit(txt, P.get("count_room", 400))
            if Kit.set_text(cnt, txt) or c.get("count_w") is None:
                tw = Kit.text_w(txt)
                if c.get("count_w") != tw:
                    c["count_w"] = tw; IW = P.get("IW", W - 2 * Kit.MARGIN)
                    safe(lambda: at_k(cnt, Kit.MARGIN + IW - 10 - tw, c["count_y"]))
    def scan_visitors(now, me):
        if now - st["scan_at"] < SCAN_EVERY: return False
        st["scan_at"] = now
        try: mx, my = int(me.X), int(me.Y); my_serial = me.Serial
        except Exception: return False
        if st["pos"] != (mx, my): st["pos"], st["moved_at"] = (mx, my), now
        rng = settings["range"]
        try: mobs = API.GetAllMobiles(distance=rng, isHuman=True) or []
        except Exception: mobs = []
        cache = st["ncache"]
        if len(cache) > NAME_CACHE_MAX:
            for k in [k for k, e in cache.items() if now >= e[0]]: del cache[k]
            if len(cache) > NAME_CACHE_MAX: cache.clear()
        out = []
        for m in mobs:
            try:
                if m is None: continue
                serial = m.Serial
                if serial == my_serial: continue
                e = cache.get(serial)
                if e is not None and now < e[0]: name, noto = e[1], e[2]
                else:
                    try: pet = bool(m.IsRenamable)
                    except Exception: pet = False
                    if pet: cache[serial] = (now + NAME_CACHE_SECS, None, "pet"); continue
                    noto = noto_name(m); name = str(m.Name or ""); cache[serial] = (now + NAME_CACHE_SECS, name, noto)
                if name is None: continue
                if noto == "invulnerable": continue
                if not settings["friends"] and noto == "ally": continue
                vx, vy = int(m.X), int(m.Y); dist = max(abs(vx - mx), abs(vy - my))
                if dist > rng: continue
                try: hid = bool(m.IsHidden)
                except Exception: hid = False
                out.append({"serial": serial, "name": name, "noto": noto, "dist": dist, "hidden": hid,
                            "x": vx, "y": vy, "inside": False})
            except Exception: continue
        out.sort(key=_by_dist); st["near"] = len(out); st["visitors"] = out; track_house(now, mx, my, out)
        refresh_rows(); return True
    def _by_dist(v): return (v["dist"], v["name"].lower())
    def multi_at(x, y):
        try: ms = API.GetMultisAt(x, y)
        except AttributeError: return None
        except Exception: return False
        if ms is None: return False
        try: return len(ms) > 0
        except Exception:
            try: return int(ms.Count) > 0
            except Exception: return False
    def track_house(now, mx, my, out):
        if st["house_pos"] != (mx, my) or now >= st["house_at"]:
            st["house_pos"], st["house_at"] = (mx, my), now + HOUSE_EVERY; st["in_house"] = multi_at(mx, my)
            if st["in_house"] is None and not st["no_multi_said"]:
                st["no_multi_said"] = True
                say("this TazUO can't tell where houses are (no API.GetMultisAt), so the visitor log and the red "
                    "or Foe alarm stay off.")
        opened = st["open_visits"]
        if not st["in_house"]:
            if st["inside"]: st["inside"] = {}
            if opened: close_visits(now)
            return
        old = st["inside"]; new = {}; budget = HOUSE_CHECKS
        for v in out:
            s = v["serial"]; e = old.get(s)
            if e is None or e[0] != v["x"] or e[1] != v["y"]:
                if budget > 0: budget -= 1; e = (v["x"], v["y"], bool(multi_at(v["x"], v["y"])))
                elif e is None: continue
            new[s] = e; inside = e[2]; v["inside"] = inside
            if inside:
                if s not in opened: open_visit(v, now)
            elif s in opened: close_visit(s, now)
        st["inside"] = new
        if opened:
            for s in list(opened):
                if s not in new: close_visit(s, now)
    def open_visit(v, now):
        s = v["serial"]; e = next((r for r in reversed(visits) if r[2] == s), None)
        if e is not None and e[1] and now - e[1] <= VISIT_MERGE: e[1] = 0.0; e[5] += 1
        else: e = [now, 0.0, s, v["name"] or "someone", v["noto"], 1, 0]; visits.append(e); del visits[:-VISIT_KEEP]
        st["open_visits"][s] = e; visits_changed()
    def close_visit(s, now):
        e = st["open_visits"].pop(s, None)
        if e is not None: e[1] = now; visits_changed()
    def close_visits(now):
        for s in list(st["open_visits"]): close_visit(s, now)
    def mark_visit(serial, flag):
        e = next((r for r in reversed(visits) if r[2] == serial), None)
        if e is not None: e[6] = flag; visits_changed()
    def is_foe(serial, name, now):
        fn = HOST.services.get(FOE_SERVICE)
        if fn is None: return False
        c = st["foe"].get(serial)
        if c is not None and now < c[0]: return c[1]
        try: r = bool(fn(serial, name))
        except Exception: r = False
        if len(st["foe"]) > NAME_CACHE_MAX: st["foe"].clear()
        st["foe"][serial] = (now + NAME_CACHE_SECS, r); return r
    def own_people():
        out = set()
        try: out.update(int(x) for x in (API.GetPartyMemberSerials() or []))
        except Exception: pass
        try:
            for f in (API.GetAllFriends() or []):
                try: out.add(int(getattr(f, "Serial", f)))
                except Exception: continue
        except Exception: pass
        return out
    def eject_on_sight(now):
        if not settings["eject_foes"] or not st["in_house"]: return
        eject_at = st["eject_at"]; mates = None
        for v in st["visitors"]:
            if not v["inside"] or v["hidden"]: continue
            s = v["serial"]
            if eject_at.get(s, 0.0) > now: continue
            if v["noto"] != "murderer" and not is_foe(s, v["name"], now): continue
            if mates is None: mates = own_people()
            if s in mates: continue
            if len(eject_at) > NAME_CACHE_MAX:
                for k in [k for k, t in eject_at.items() if t <= now]: del eject_at[k]
            eject_at[s] = now + EJECT_FOE_EVERY; what = "red" if v["noto"] == "murderer" else "Foe"
            if not HOST.alert(ALERT_FOE, "%s (%s) is in your house: Eject from their row?"
                              % (v["name"] or "Someone", what), "alarm", who=s):
                add_log("%s (%s) stepped in" % (v["name"] or "someone", what), Kit.HUE_BAD)
            return
    def sweep_held(now):
        try: fight = HOST.fight_hold(now)
        except Exception: fight = None
        if fight == "dead": return HOLD_TEXT["dead"]
        try: g = HOST.guard_hold()
        except Exception: g = "unknown"
        if g == "guard": return HOLD_TEXT["guard"]
        if g is not None: return HELD_UNKNOWN
        if fight: return HOLD_TEXT.get(fight, fight)
        try:
            if HOST.alarm_up(): return HOLD_TEXT["alarm"]
        except Exception: pass
        return None
    def start_sweep(now, forced=False):
        if st["house"] is not None:
            if forced: note(RUNNING)
            return False
        if st["phase"] != "idle": return False
        held = st["held"]
        if held:
            if forced: note(held if held == HELD_UNKNOWN else "The sweep waits: %s" % held)
            return False
        if now < st["next_at"]:
            if forced: note("Detect Hidden is ready in %d s" % int(st["next_at"] - now + 0.99))
            return False
        if not forced and settings["still"] and now - st["moved_at"] < STILL_SECS: return False
        if not cursor_free():
            if forced: note("A target cursor is up: the sweep waits for it")
            return False
        me = HOST.me()
        if me is not None: st["scan_at"] = 0.0; scan_visitors(now, me)
        try: st["seen"] = {v["serial"] for v in st["visitors"] if not v["hidden"]}
        except Exception: st["seen"] = set()
        API.UseSkill(DETECT_SKILL); HOST.claim_cursor(KEY, CURSOR_WAIT)
        st["phase"], st["deadline"] = "cursor", now + CURSOR_WAIT; return True
    def sweep_tick(now):
        if st["phase"] == "cursor":
            if now > st["deadline"]:
                HOST.release_cursor(KEY); st["phase"], st["next_at"] = "idle", now + RETRY_SOON
                note("Detect Hidden gave no cursor; trying again shortly")
            elif HOST.cursor_busy(KEY) is not None: return
            elif HOST.cursor_ok(KEY, "neutral"):
                API.TargetSelf(); HOST.release_cursor(KEY); st["phase"], st["cast_at"] = "cast", now
                st["next_at"] = now + settings["cooldown"]; st["sweeps"] += 1
            elif has_target():
                HOST.release_cursor(KEY); st["phase"], st["next_at"] = "idle", now + RETRY_SOON
                add_log("a spell cursor came up, so that sweep was dropped", Kit.HUE_INFO)
            return
        if st["phase"] == "cast":
            if now - st["cast_at"] <= REVEAL_WINDOW:
                for v in st["visitors"]:
                    if v["serial"] not in st["seen"] and not v["hidden"]:
                        st["seen"].add(v["serial"]); st["revealed"] += 1
                        safe(lambda: API.HeadMsg("* revealed *", v["serial"], Kit.HUE_BAD))
                        add_log("revealed %s" % (v["name"] or "someone"), Kit.HUE_BAD)
                        if settings["sound"]:
                            HOST.alert(ALERT_REVEAL, "Revealed %s" % (v["name"] or "someone"), "warn", who=v["serial"])
            if now - st["cast_at"] > REPLY_WAIT: st["phase"] = "idle"
    def on_journal(ln):
        now = time.time(); sw = st["phase"] in ("cursor", "cast") or now - st["cast_at"] < REPLY_WAIT
        if not sw and st["house"] is None and st["house_wait"] is None: return
        low = ln.low
        if settings["say_replies"] and not low.startswith(OWN_PREFIX) and not low.startswith(OWN_REPLY_PREFIX):
            say("reply: %s" % ln.text.strip())
        if sw:
            for t in J_WAIT:
                if t in low:
                    if st["phase"] == "cursor": HOST.release_cursor(KEY)
                    elif st["phase"] == "cast": st["sweeps"] = max(0, st["sweeps"] - 1)
                    st["phase"], st["next_at"] = "idle", time.time() + RETRY_SOON
                    note("Skill delay: trying again shortly"); return
            for t in J_NOTHING:
                if t in low: return
            for t in J_REVEAL:
                if t in low:
                    note("Someone was revealed", 6.0)
                    if settings["sound"]: HOST.alert(ALERT_REVEAL, "Someone was revealed", "warn")
                    return
        h = st["house"]
        if h is None: return
        for t in J_DONE[h["kind"]]:
            if t in low:
                add_log("%s %s" % (CMDS[h["kind"]][1], h["name"] or "the target"), Kit.HUE_GOOD)
                if h["kind"] in ("eject", "ban"): mark_visit(h["serial"], 2 if h["kind"] == "ban" else 1)
                finish_house(); return
        for t in J_HOUSE_NO:
            if t in low:
                add_log("%s %s failed: %s" % (who(h) + (ln.text.strip(),)), Kit.HUE_BAD); finish_house(); return
    def start_house(kind, serial, name, now, waited=False):
        if st["house"] is not None or (st["house_wait"] is not None and not waited): note(RUNNING); return
        if st["phase"] == "cursor":
            st["house_wait"] = {"kind": kind, "serial": serial, "name": name, "until": now + CURSOR_WAIT}
            st["confirm"] = None; return
        if not cursor_free(): note(NO_CURSOR); return
        if not name: name = str(safe(lambda: find_t(kind, serial).Name, "") or "")
        API.Msg(settings[CMDS[kind][0]]); HOST.claim_cursor(KEY, CURSOR_WAIT)
        st["house"] = {"kind": kind, "serial": serial, "name": name, "deadline": now + CURSOR_WAIT, "aimed": 0.0}
        st["confirm"] = None
    def finish_house(): st["house"] = None; HOST.release_cursor(KEY)
    def house_wait_tick(now):
        hw = st["house_wait"]
        if hw is None: return
        if st["phase"] != "cursor" and cursor_free():
            st["house_wait"] = None; start_house(hw["kind"], hw["serial"], hw["name"], now, waited=True)
        elif now > hw["until"]:
            st["house_wait"] = None
            if st["phase"] == "cursor": HOST.release_cursor(KEY); st["phase"], st["next_at"] = "idle", now + RETRY_SOON
            if cursor_free(): start_house(hw["kind"], hw["serial"], hw["name"], now, waited=True)
            else: note(NO_CURSOR)
    def house_tick(now):
        h = st["house"]
        if h is None: return
        if not h["aimed"]:
            if now <= h["deadline"]:
                if HOST.cursor_busy(KEY) is not None: return
                if not HOST.cursor_ok(KEY, "neutral"):
                    if has_target():
                        add_log("%s %s: a spell cursor came up, so the command was dropped" % who(h), Kit.HUE_BAD)
                        finish_house()
                    return
                if find_t(h["kind"], h["serial"]) is None:
                    API.CancelTarget(); add_log("%s %s: out of sight" % who(h), Kit.HUE_BAD); finish_house(); return
                API.Target(h["serial"]); HOST.release_cursor(KEY); h["aimed"] = now
            else:
                add_log("%s %s: the house gave no cursor (are you in your house, with the right to? If the shard "
                        "has no spoken form of this, use the house sign)" % who(h), Kit.HUE_BAD)
                finish_house()
            return
        if now - h["aimed"] > REPLY_WAIT: add_log("%s aimed at %s (no reply seen)" % who(h)); finish_house()
    def want_ban(serial, name, now):
        if settings["confirm"]:
            c = st["confirm"]
            if not (c and c[0] == serial and now < c[1]):
                st["confirm"] = (serial, now + CONFIRM_SECS)
                note("Ban %s? Click Ban (or pick them) again to confirm" % (name or "them"), CONFIRM_SECS); return
        start_house("ban", serial, name, now)
    EJECT_TIP = ("A red, or one on Ultima Tracker's Foe list, who steps into your house raises an "
                 "alarm (once per player every %d s); their row's Eject button ejects them" % int(EJECT_FOE_EVERY))
    PAGE_OPTS = {"ldy": 4, "fh": 30, "ugap": 6}
    def page_table(w):
        col = (w - 24) // 2; lw1 = max(Kit.text_w(t) for t in ("Eject:", "Ban:", "Friend:"))
        lw2 = max(Kit.text_w(t) for t in ("Lock down:", "Release:"))
        left, right = {"lw": lw1, "tw": col - lw1 - 26}, {"dx": 12 + col, "lw": lw2, "tw": col - lw2 - 26}
        return (("SWEEP  (Detect Hidden on your own spot)", (
                    ("num", "cooldown", "Seconds between uses:", "Seconds Detect Hidden waits after a use before the "
                     "next, the shard's skill delay", None, COOLDOWN_MIN, COOLDOWN_MAX, {"cast": float}),
                    ("check", "still", "Sweep only while you stand still",
                     "Hold the sweep while you walk; it goes on once you have stood still a second"),
                    ("check", "sound", "Alert when a sweep reveals someone",
                     "Raise the Someone revealed in the house alert (sound: Settings > Alerts)"))),
                ("VISITORS  (the list in the window)", (
                    ("num", "range", "List players within:", "Players this many tiles from you are listed", "tiles",
                     RANGE_MIN, RANGE_MAX), ("check", "friends", "List guild and alliance members too",
                     "Unticked, players shown green (your guild and its allies) are left out"),
                    ("check", "confirm", "Ban needs a second click within %d s" % int(CONFIRM_SECS),
                     "A Ban button or a Ban... pick asks for a second click, so the wrong person isn't banned"),
                    ("check", "eject_foes", "Alarm when a red or Foe steps into the house", EJECT_TIP))),
                ("HOUSE COMMANDS  (said out loud; verify on the shard)", (
                    ("text", "eject_cmd", "Eject:", "Said out loud to eject a player (owner, co-owner or friend)",
                     left), ("text", "ban_cmd", "Ban:", "Said out loud to ban a player (owner or co-owner)", left),
                    ("text", "friend_cmd", "Friend:", "Said out loud to make a player a friend of the house (owner)",
                     left), ("gap", -90),
                    ("text", "lock_cmd", "Lock down:", "Said out loud to lock an item down (owner, co-owner or friend)",
                     right), ("text", "release_cmd", "Release:",
                     "Said out loud to release a locked-down item (owner or co-owner)", right), ("gap", 30),
                    ("note", Kit.wrap("Owner adds friends; owner and co-owners ban and release; friends eject "
                                      "and lock down.", w - 28)[0], {"ndy": 4, "h": 24}))),
                ("DEBUG  (for checking the shard's texts)", (
                    ("check", "say_replies", "Print the shard's replies in the journal",
                     "Every journal line seen while a house command or a sweep waits for the shard is printed as "
                     "\"%s: reply: ...\", to fix the lists above" % TITLE),)))
    def config_height(w): return Kit.Form.height(page_table(w), w, **PAGE_OPTS)
    def build_config(g, x, y, w): page["f"] = Kit.Form(g, x, y, w, settings, page_table(w), **PAGE_OPTS)
    def poll_config():
        f = page["f"]
        if f is None: return
        old = dict(settings)
        try: settings.update(f.read(True, DEFAULTS))
        except Exception: page["f"] = None; return
        if settings["eject_foes"] != old["eject_foes"]: st["eject_at"].clear()
        if settings != old:
            save_settings()
            if settings["confirm"] != old["confirm"] and not st["minimized"]: queue("redraw")()
    def config_closed(): page["f"] = None
    def _start():
        st.update({"shutting": False, "docked": False, "queue": [], "phase": "idle",
                   "house": None, "house_wait": None, "confirm": None, "visitors": [], "near": 0,
                   "scan_at": 0.0, "ncache": {}, "log_dirty": False, "log_save_at": 0.0,
                   "pos": None, "moved_at": 0.0, "note": "", "note_until": 0.0,
                   "in_house": None, "house_pos": None, "house_at": 0.0, "inside": {},
                   "open_visits": {}, "visits_dirty": False, "visits_save_at": 0.0, "visits_redraw": False,
                   "eject_at": {}, "foe": {}, "held": None, "held_at": 0.0,
                   "minimized": bool(safe(lambda: HOST.dock_wanted(KEY), False)) or Kit.load_min(MIN_KEY)})
        fit.update({"slot": None, "k": 1.0, "full": None}); load_settings(); st["rd"] = Journal.reader()
        safe(lambda: HOST.alert_kind(ALERT_REVEAL, "Someone revealed", REVEAL_SOUND))
        safe(lambda: HOST.alert_kind(ALERT_FOE, "Red or Foe in the house", ALERT_FOE_SOUND)); build_window()
        hooks = Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"), fit=layout_fit)
        hooks.update({"exact": True, "verify": True, "drawn_at": drawn_at}); HOST.dock_add(KEY, hooks)
        say("on; sweep %s (held in guard zones, in a fight and while an alarm waits), visitors within %d tiles%s."
            % ("on" if st["sweep"] else "off", settings["range"], ", red or Foe alarm on" if settings["eject_foes"]
               else ""), Kit.HUE_GOOD)
    def _tick():
        if win["g"] is None: return
        if Kit.was_clicked(win["store"], "close"): Kit.dispose(win["g"]); return
        now = time.time(); me = HOST.me()
        while st["queue"]:
            action = st["queue"].pop(0); kind = action[0] if isinstance(action, tuple) else action
            if Kit.win_action(action, st, KEY, TITLE, build_window, MIN_KEY): continue
            if action == "sweep":
                st["sweep"] = not st["sweep"]; Kit.put_var(VIEW_KEY, "1" if st["sweep"] else "0")
                say("sweep %s." % ("on" if st["sweep"] else "off"), Kit.HUE_GOOD if st["sweep"] else Kit.HUE_INFO)
            elif action == "now":
                if me is not None and st["phase"] == "idle": st["held"] = sweep_held(now)
                if me is not None and not start_sweep(now, forced=True) and st["phase"] != "idle":
                    note("A sweep is already running")
            elif action == "show_log":
                if Kit.is_open(win["log_g"]):
                    save_log_pos(); g, win["log_g"], win["log_rows"] = win["log_g"], None, []; Kit.dispose(g)
                else: build_logwin()
            elif action == "log_view":
                win["log_view"] = "log" if win["log_view"] == "visits" else "visits"
                Kit.put_var(LOG_VIEW_KEY, win["log_view"])
                if Kit.is_open(win["log_g"]): build_logwin()
            elif action == "log_clear" and win["log_view"] == "visits":
                del visits[:]; st["open_visits"], st["inside"] = {}, {}; visits_changed()
            elif action in ("clear_log", "log_clear"): del log[:]; save_log_soon(); refresh_log()
            elif kind[:5] == "pick_":
                which = kind[5:]
                if st["house"] is not None or st["house_wait"] is not None: note(RUNNING)
                else:
                    note("Target the %s to %s (Esc cancels)" % (
                        "player" if CMDS[which][2] == "mobile" else "item", VERBS[which].lower()), PICK_WAIT)
                    HOST.pick_target(PICK_WAIT, picked(which))
            elif kind == "follow": Follow.toggle(action[1], TITLE)
            elif kind == "last":
                API.SetLastTarget(serial=action[1]); safe(lambda: API.HeadMsg("* last target *", action[1], 0x35))
            elif kind == "ban": want_ban(action[1], action[2], now)
            elif kind in CMDS: start_house(kind, action[1], action[2], now)
        if st["log_dirty"] and now >= st["log_save_at"]: st["log_save_at"] = now + LOG_SAVE_EVERY; save_log()
        if st["visits_dirty"] and now >= st["visits_save_at"]:
            st["visits_save_at"] = now + VISIT_SAVE_EVERY; save_visits()
        if st["visits_redraw"]: st["visits_redraw"] = False; refresh_logwin()
        if me is None: return
        rd = st["rd"]
        if rd is not None:
            for ln in rd.new():
                try: on_journal(ln)
                except Exception: pass
        if scan_visitors(now, me): eject_on_sight(now)
        house_tick(now)
        if st["house"] is None:
            if st["sweep"] and st["phase"] == "idle" and (now >= st["next_at"] - HELD_EVERY or now >= st["held_at"]):
                st["held_at"] = now + HELD_EVERY; held = sweep_held(now)
                if held != st["held"]:
                    was, st["held"] = st["held"], held
                    if held and not was: add_log("sweep waits: %s" % (held[:1].lower() + held[1:]), Kit.HUE_INFO)
                if st["house_wait"] is None and not st["held"]: start_sweep(now)
            sweep_tick(now); house_wait_tick(now)
        if st["confirm"] and now >= st["confirm"][1]: st["confirm"] = None
        refresh_status()
    def picked(which):
        def done(serial):
            serial = int(serial or 0)
            if not serial: note("Nothing picked"); return
            st["queue"].append((which, serial, None))
        return done
    def _stop():
        st["shutting"] = True; st["house_wait"] = None; safe(lambda: HOST.release_cursor(KEY)); HOST.dock_remove(KEY)
        save_pos(); save_log_pos(); Kit.save_min(MIN_KEY, st["minimized"]); save_settings()
        if st["log_dirty"]: save_log()
        if st["open_visits"]: close_visits(time.time())
        if st["visits_dirty"]: save_visits()
        g, win["g"], win["rows"] = win["g"], None, []; Kit.dispose(g)
        lg, win["log_g"], win["log_rows"] = win["log_g"], None, []; Kit.dispose(lg)
    load_settings()
    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": config_height,
            "build_config": build_config, "poll_config": poll_config, "config_closed": config_closed}


if "HOST" in globals() and hasattr(globals()["HOST"], "add"):
    HOST.add("butler", "Property Butler", "Keeps your house: Detect Hidden sweeps, visitors, eject, ban",
             _module_butler, 0.1, category="Skills and home")
else:
    import API
    API.SysMsg("Property Butler is a Virtue Assistant module and can't run on its own. "
               "Run Virtue Assistant instead; it loads this file.", 33)
