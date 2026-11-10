# Property Butler: a Virtue Assistant module. This file is not a script to run on its own: the
# mother script loads it from the modules folder and runs it inside its own namespace, so API, G,
# safe, Client, Kit, Follow, HOST, Journal, HOLD_TEXT and the settings window are all provided by
# the mother. Leaving the file out of the folder leaves the module out. Key "butler", category
# "Skills and home".
#
# It looks after your house while you stand in it:
#   Sweep: Detect Hidden on your own spot, once or whenever the skill is ready, so anyone hiding
#     on the property is revealed, called out over their head and counted.
#   Visitors: every player near you, with Friend, Eject and Ban buttons on each row. The house
#     command is said out loud and the cursor the house raises is aimed at that player.
#   Actions: a cursor to pick a player to eject, ban or befriend, or an item to lock down or
#     release.
#   Log window: the last actions, and the visitors who stood inside the house, kept per character.
#   Red or Foe alarm (a setting, off by default): a red player or one on Ultima Tracker's Foe
#     list who steps into your house raises an alert; the Eject button on their row acts on your
#     press, never on its own.
#
# Only the house owner, co-owners and friends can eject and lock down; only the owner and
# co-owners can ban and release; only the owner adds friends. The shard answers in the journal and
# the log shows what it said. The module runs on the client tick.
def _module_butler():
    """Build the Property Butler module in its own namespace and return its hooks.

    The returned dict holds start, tick and stop (all run on the client tick), the settings page
    hooks (config_height, build_config, poll_config, config_closed) and client_tick set to True.
    Saved keys are the PropertyButler_* names below, all kept per character.
    """
    KEY = "butler"
    TITLE = "Property Butler"
    # Saved keys, all per character: the settings line, the window place, whether it is minimised,
    # whether the sweep is on, the last actions, the log window's place and view, and the visitor log.
    SETTINGS_KEY = "PropertyButler_settings"
    POS_KEY = "PropertyButler_pos"
    MIN_KEY = "PropertyButler_min"
    VIEW_KEY = "PropertyButler_view"
    LOG_KEY = "PropertyButler_log"
    LOG_POS_KEY = "PropertyButler_log_pos"
    # Window sizes: the full width, the minimised bar and the log window.
    W = 520
    MINI_W, MINI_H = 300, 46
    # House sign art shown for this module on the Action Bar tray.
    TRAY_ICON = 0x0BD2
    # Visitor rows drawn; any more are only counted.
    MAX_ROWS = 8
    ROW_H = 22
    LOG_LINES = 3
    # Log lines remembered and saved; LOG_LINES of them show in the main window.
    LOG_KEEP = 30
    LOG_W = 520
    LOG_ROW_H = 18
    # Seconds between saves of the action log, so a burst of lines is one write.
    LOG_SAVE_EVERY = 1.0
    # A visitor's name and notoriety change rarely: they are read again only after this many seconds,
    # and the cache is capped at NAME_CACHE_MAX entries.
    NAME_CACHE_SECS = 2.5
    NAME_CACHE_MAX = 200
    # Seconds a hand-picked target cursor stays up.
    PICK_WAIT = 15.0
    VISITS_KEY = "PropertyButler_visits"
    LOG_VIEW_KEY = "PropertyButler_log_view"
    LOG_DOCK = "butler.log"
    LOG_TITLE = "Property Butler Log"
    LOG_MIN_ROWS = 4
    # Height of the log window outside its rows: margins, the title bar, the gap and the section frame.
    LOG_FIXED = 2 * Kit.MARGIN + 30 + Kit.GAP + 30 + 8
    # Visits remembered, the oldest dropped. A player back within VISIT_MERGE seconds of leaving
    # counts as the same visit, and the visitor log is saved at most every VISIT_SAVE_EVERY seconds.
    VISIT_KEEP = 30
    VISIT_MERGE = 60.0
    VISIT_SAVE_EVERY = 5.0
    # Seconds between looks for a house tile under you while you stand still. HOUSE_CHECKS caps how
    # many visitors' tiles are looked up per scan (only those who moved).
    HOUSE_EVERY = 2.0
    HOUSE_CHECKS = 6
    # Seconds before the same red or Foe player raises another alert.
    EJECT_FOE_EVERY = 10.0
    # Ultima Tracker's Foe list, offered through HOST.services as fn(serial, name) -> bool. Optional:
    # without it only reds count.
    FOE_SERVICE = "ultima.is_foe"
    # Name handed to API.UseSkill, which uses the first skill whose name contains it.
    DETECT_SKILL = "Detect Hidden"
    # Seconds between skill uses: the shard's skill delay, adjustable within COOLDOWN_MIN and
    # COOLDOWN_MAX.
    DEFAULT_COOLDOWN = 10.0
    COOLDOWN_MIN, COOLDOWN_MAX = 3.0, 120.0
    DEFAULT_RANGE = 12
    RANGE_MIN, RANGE_MAX = 1, 18
    # Seconds to wait for the cursor that Detect Hidden or a house command raises.
    CURSOR_WAIT = 3.0
    # Seconds the shard's journal reply is waited for after a cursor is aimed.
    REPLY_WAIT = 3.0
    # Someone who appears this soon after the skill was aimed counts as revealed by it; later arrivals
    # just walked in.
    REVEAL_WINDOW = 1.0
    # Seconds before trying again after a skill delay or a missed cursor.
    RETRY_SOON = 1.5
    # A second click on Ban within this long confirms it.
    CONFIRM_SECS = 3.0
    # Standing still means not having moved for this long.
    STILL_SECS = 1.0
    # Seconds between visitor scans; SCAN_POKE is the shorter gap after a mobile appears while a sweep
    # is under way, so a reveal is seen at once.
    SCAN_EVERY = 0.3
    SCAN_POKE = 0.1
    # Seconds between looks at why the sweep is held while it cools down.
    HELD_EVERY = 0.5
    # Default sound of the revealed alert; the player changes it under Settings > Alerts.
    REVEAL_SOUND = 0x01F1
    ALERT_REVEAL = "butler.revealed"
    ALERT_FOE = "butler.foe"
    ALERT_FOE_SOUND = 0x338
    # Shown as it is: the held text for a zone that is not known yet is a sentence of its own.
    HELD_UNKNOWN = HOLD_TEXT["unknown"]
    # Journal lines the shard sends, lower case and matched with "in": a skill delay, nothing hidden,
    # people revealed, and the replies to each house command (done) and its refusals (J_HOUSE_NO).
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
    # House commands by kind: (settings key of the words said, what the log says on success, whether
    # the target is a "mobile" or an "item").
    CMDS = {"eject": ("eject_cmd", "ejected", "mobile"), "ban": ("ban_cmd", "banned", "mobile"),
            "friend": ("friend_cmd", "befriended", "mobile"), "lock": ("lock_cmd", "locked down", "item"),
            "release": ("release_cmd", "released", "item")}
    # The verb as the status line and the log say it.
    VERBS = {"eject": "Eject", "ban": "Ban", "friend": "Befriend", "lock": "Lock down", "release": "Release"}
    EMPTY_ROWS = "No players in range."
    EMPTY_LOG = "No actions yet."
    EMPTY_VISITS = "No visits yet."
    # Saved settings with their defaults. The house command words are what the shard's house speech
    # expects and can be changed on the settings page.
    settings = {"cooldown": DEFAULT_COOLDOWN, "range": DEFAULT_RANGE, "still": False, "sound": True, "friends": True,
                "confirm": True, "eject_cmd": "Remove thyself", "ban_cmd": "I ban thee",
                "friend_cmd": "I wish to make this a friend", "lock_cmd": "I wish to lock this down",
                "release_cmd": "I wish to release this", "eject_foes": False}
    DEFAULTS = dict(settings)
    # Order of the settings after the first two numbers in the saved line. The None slot is a
    # reserved field, always written as 0 and never read.
    FIELDS = ("still", "sound", "friends", "confirm", "eject_cmd", "ban_cmd", "friend_cmd", "lock_cmd",
              "release_cmd", None, "eject_foes")
    # Run state, reset by _start. phase is idle, cursor or cast (the Detect Hidden flow), house and
    # house_wait hold a house command running or waiting for the sweep's cursor to pass, confirm is a
    # Ban waiting for its second click.
    st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "sweep": False, "next_at": 0.0,
          "deadline": 0.0, "cast_at": 0.0, "seen": set(), "sweeps": 0, "revealed": 0, "eject_at": {}, "first_d": {},
          "reveal_line": False, "hooked": False, "scan_poke": False}
    # win is the main window's record; logs is the log window's. Each holds its gump, controls,
    # button store and the rows it redraws.
    win = {"g": None, "c": {}, "store": ({}, {}), "rows": [], "log_view": "log"}
    logs = {"g": None, "c": {}, "store": ({}, {}), "rows": [], "minimized": False, "shutting": False, "docked": False,
            "w": LOG_W, "queue": []}
    # cleanup closes the module's windows, queue puts an action on st["queue"] for the tick to run,
    # say prints a journal line prefixed with the title.
    cleanup, queue, say = Kit.basics(st, TITLE)
    # log holds the action log as (time, text, hue), newest last. visits holds one list per visit:
    # [time in, time out (0 while inside or unknown), serial, name, notoriety, times in,
    # 0 none / 1 ejected / 2 banned].
    log = []
    visits = []
    # Hue of a notoriety name in the visitor rows and the visit lines.
    NOTO_HUE = {"innocent": 90, "ally": 68, "gray": 946, "criminal": 946, "murderer": 33,
                "enemy": 43, "invulnerable": 53}

    def load_settings():
        """Read the settings, the sweep switch, the action log and the visitor log from the saved keys.

        Settings line: cooldown|range then the FIELDS in order, split on "|"; a short line (older save)
        is padded and missing text fields take their defaults. Action log: one line per entry, tab
        separated: time, hue, text. Visitor log: tab separated time in, time out, serial, notoriety,
        times, flag, then the name last, so a name can hold anything but a tab.
        """
        p = Kit.get_var(SETTINGS_KEY).split("|")
        if len(p) >= 8:
            for i, k, lo, hi, cast in ((0, "cooldown", COOLDOWN_MIN, COOLDOWN_MAX, float),
                                       (1, "range", RANGE_MIN, RANGE_MAX, int)):
                with Kit.quiet:
                    settings[k] = max(lo, min(hi, cast(p[i])))
            n = len(p)
            # Pad to the full field count so a save with fewer fields still reads.
            p = p + [""] * (13 - len(p))
            for i, k in enumerate(FIELDS, 2):
                if k:
                    # Ticks are saved as 1 or 0; a text field missing from an older save keeps its default.
                    settings[k] = p[i] == "1" if isinstance(DEFAULTS[k], bool) else (p[i] if i < n else DEFAULTS[k])
        # Whether the sweep was on when last seen.
        st["sweep"] = Kit.get_var(VIEW_KEY) == "1"
        del log[:]
        for line in Kit.get_var(LOG_KEY).split("\n"):
            q = line.split("\t")
            if len(q) >= 3:
                with Kit.quiet:
                    log.append((float(q[0]), q[2], int(q[1])))
        # Bad lines are skipped one by one (Kit.quiet), and only the newest are kept.
        del log[:-LOG_KEEP]
        del visits[:]
        for line in Kit.get_var(VISITS_KEY).split("\n"):
            # The name is last and may hold spaces, so split at most six times.
            q = line.split("\t", 6)
            if len(q) >= 7:
                with Kit.quiet:
                    visits.append([float(q[0]), float(q[1]), int(q[2]), q[6], q[3] or "unknown",
                                   max(1, int(q[4])), int(q[5])])
        del visits[:-VISIT_KEEP]
        win["log_view"] = "visits" if Kit.get_var(LOG_VIEW_KEY) == "visits" else "log"

    def save_settings():
        """Save the settings line and the sweep switch.

        Pipes in text are turned into slashes so they cannot split the line; the reserved field is 0.
        """
        Kit.put_var(SETTINGS_KEY, "|".join(["%.1f" % settings["cooldown"], str(settings["range"])] + [
            "0" if k is None else ("1" if settings[k] else "0") if isinstance(DEFAULTS[k], bool)
            else settings[k].replace("|", "/") for k in FIELDS]))
        Kit.put_var(VIEW_KEY, "1" if st["sweep"] else "0")

    def save_log():
        """Save the action log, one tab-separated line each, and clear the dirty flag."""
        st["log_dirty"] = False
        Kit.put_var(LOG_KEY, "\n".join(["%d\t%d\t%s" % (t, hue, text.replace("\t", " ").replace("\n", " "))
                                         for (t, text, hue) in log[-LOG_KEEP:]]))

    def save_visits():
        """Save the visitor log, one tab-separated line each, and clear the dirty flag."""
        st["visits_dirty"] = False
        Kit.put_var(VISITS_KEY, "\n".join(["%d\t%d\t%d\t%s\t%d\t%d\t%s" % (
            e[0], e[1], e[2], str(e[4]).replace("\t", " "), e[5], e[6],
            str(e[3]).replace("\t", " ").replace("\n", " ")) for e in visits[-VISIT_KEEP:]]))

    def visits_changed():
        """A visit opened, closed or was marked: flag the log for saving and, when the log window shows
        visits, flag it to be redrawn once at the end of the tick.
        """
        st["visits_dirty"] = True
        if win["log_view"] == "visits" and logs["g"] is not None:
            st["visits_redraw"] = True

    def add_log(text, hue=None):
        """Add a line to the action log and say it in the journal.

        The journal form ends with a full stop; the log line itself stays bare. Saved later by _tick.
        """
        hue = Kit.HUE_INFO if hue is None else hue
        log.append((time.time(), text, hue))
        del log[:-LOG_KEEP]
        st["log_dirty"] = True
        say(text + ("" if text.endswith((".", "!", "?")) else "."), hue)
        refresh_log()

    def note(text, secs=4.0):
        """Show a short status line under the sweep row for secs seconds."""
        st["note"], st["note_until"] = text, time.time() + secs

    def has_target():
        """Is any target cursor up? A plain call, since it runs every tick while something waits."""
        return bool(API.HasTarget("any"))

    def cursor_free():
        """No cursor is up and no other module has one claimed."""
        return HOST.cursor_busy(KEY) is None and not has_target()

    def short(name, width):
        """Cut name to fit width pixels, using real letter widths."""
        return Kit.fit(name or "(unknown)", width)

    def find_t(kind, serial):
        """Look up the target of a house command by serial: a mobile or an item according to the kind.

        Returns None when it is not in view.
        """
        return (API.FindMobile if CMDS[kind][2] == "mobile" else API.FindItem)(serial)

    def who(h):
        """Return the lower-case verb and the target's name (or "the target") of a running house command,
        ready for a log line.
        """
        return VERBS[h["kind"]].lower(), h["name"] or "the target"

    # Section heights and widths in pixels. Visitor rows, the action section and the whole window are
    # worked out from them; layout() recomputes them for the width and height it is given.
    SWEEP_H = 82
    NAME_W = 150
    LOG_PITCH = 20
    VIS_H = 30 + MAX_ROWS * ROW_H + 8
    ACT_H = 30 + 26 + 26 + LOG_LINES * LOG_PITCH + 8
    H = Kit.MARGIN + 30 + Kit.GAP + SWEEP_H + Kit.GAP + VIS_H + Kit.GAP + ACT_H + Kit.MARGIN
    MIN_ROWS = 2
    NAME_MIN = 60
    RUNNING = "A house command is still running"
    NO_CURSOR = "A target cursor is up: use it or press Esc"
    # The tooltip ending shared by every control that sets the last target on a click.
    ALT = ". Alt+click: auto-follow (again to stop)"
    LAST_TIP = "Set as last target" + ALT
    # fit holds the scale the window was drawn at (1.0 unless a zone is narrower than its minimum) and
    # the size of the full layout, for the zone code to read back through drawn_at.
    fit = {"k": 1.0, "full": None}

    def drawn_at():
        """Return the scale the window is drawn at and its full size (None when drawn at full size)."""
        return fit["k"], fit["full"]

    def at_k(ctrl, x, y):
        """Place a control that was moved after the window was built.

        x and y are in the layout's pixels; the position is scaled when the window is drawn smaller.
        """
        k = fit["k"]
        if k != 1.0:
            ctrl.SetPos(int(round(x * k)), int(round(y * k)))
        else:
            Kit.ui_pos(ctrl, x, y)

    def cap_w(text):
        """Width of a captioned button: the art and gaps plus the caption's text."""
        return 35 + Kit.text_w(text)

    # The action buttons in two groups, each starting its own row and flowed to the width:
    # (key, art, caption, tooltip, queued action).
    BUTTONS = ((("pick_ej", Kit.ART_PLAY, "Eject...", "Pick a player to eject", "pick_eject"),
                ("pick_ban", Kit.ART_CLOSE, "Ban...", "Pick a player to ban", "pick_ban"),
                ("pick_fr", Kit.ART_OK, "Friend...", "Pick a player to befriend", "pick_friend")),
               (("pick_lock", Kit.ART_OK, "Lock down...", "Pick a house item to lock down", "pick_lock"),
                ("pick_rel", Kit.ART_CLOSE, "Release...", "Pick a locked-down item to release", "pick_release"),
                ("clear", Kit.ART_CLOSE, "Clear log", "Forget the actions below (visits stay)", "clear_log"),
                ("showlog", Kit.ART_PAGE, "Show log",
                 "Open or close the log window (last %d actions and visits)" % LOG_KEEP, "show_log")))

    def flow(items, x0, right):
        """Lay captioned buttons out left to right from x0, 16 pixels apart.

        Returns [(x, row)] per caption; a button that would pass right wraps to a new row.
        """
        out, x, row = [], x0, 0
        for cap in items:
            w = cap_w(cap)
            if x > x0 and x + w > right:
                x, row = x0, row + 1
            out.append((x, row))
            x += w + 16
        return out

    def btn_line_w():
        """Width of one line holding the Friend, Eject and Ban buttons."""
        return cap_w("Friend") + 12 + cap_w("Eject") + 12 + cap_w("Ban")

    def min_w():
        """The narrowest width laid out: a visitor's name and distance beside its three buttons on a line
        of their own. A narrower zone draws this layout smaller.
        """
        return 2 * Kit.MARGIN + 12 + max(btn_line_w(), NAME_MIN + 6 + Kit.text_w("18 tiles")) + 10

    def layout(w, h):
        """Work out every place in the full window for a width of w and a height of h.

        h of None means the window's own height at that width. Returns the plan as a dict; its "h" is
        the height the plan comes out at, which may exceed h when the window is too short for it.
        """
        M = Kit.MARGIN
        IW = w - 2 * M
        ys = M + 30 + Kit.GAP
        # SWEEP section: the Sweep and Sweep now buttons share one row when they fit, else two, then the
        # status line under them.
        sw_w = max(cap_w("Sweep: off"), cap_w("Sweep: on"))
        one = 10 + sw_w + 16 + cap_w("Sweep now") <= IW - 4
        sweep_h = SWEEP_H if one else SWEEP_H + 26
        count_room = min(Kit.text_w("999 sweeps, 999 revealed"), max(40, IW - 20 - 80))
        # VISITORS section: a row holds name, distance and buttons on one line when the width allows, else
        # the buttons drop to a second line.
        yv = ys + sweep_h + Kit.GAP
        dist_w = Kit.text_w("18 tiles")
        single = 12 + NAME_MIN + 6 + dist_w + 10 + btn_line_w() + 10 <= IW
        row_h = ROW_H if single else 2 * ROW_H
        if single:
            x_ban = M + IW - 10 - cap_w("Ban")
            x_ej = x_ban - 12 - cap_w("Eject")
            x_fr = x_ej - 12 - cap_w("Friend")
            x_dist = x_fr - 10 - dist_w
        else:
            x_fr = M + 12
            x_ej = x_fr + cap_w("Friend") + 12
            x_ban = x_ej + cap_w("Eject") + 12
            x_dist = M + IW - 10 - dist_w
        # ACTIONS section: the button groups are flowed to the width and the log lines go below them.
        groups, rows_used = [], 0
        for grp in BUTTONS:
            fl = flow([b[2] for b in grp], M + 10, M + IW - 4)
            groups.append([(x, rows_used + r) for x, r in fl])
            rows_used += fl[-1][1] + 1
        # Height of everything except the visitor rows and the log lines.
        fixed = (M + 30 + Kit.GAP + sweep_h + Kit.GAP + 30 + 8 + Kit.GAP + 30 + 26 * rows_used + 8 + M)
        # Rows and log lines share the room left: the log gives way first, then the visitor rows down to
        # MIN_ROWS, and spare room goes back to the log once every visitor row shows.
        if h is None:
            rows_n, log_n = MAX_ROWS, LOG_LINES
        else:
            room = h - fixed
            log_n, rows_n = LOG_LINES, MAX_ROWS
            while log_n > 1 and rows_n * row_h + log_n * LOG_PITCH > room:
                log_n -= 1
            while rows_n > MIN_ROWS and rows_n * row_h + log_n * LOG_PITCH > room:
                rows_n -= 1
            while rows_n == MAX_ROWS and log_n < LOG_KEEP and rows_n * row_h + (log_n + 1) * LOG_PITCH <= room:
                log_n += 1
        vis_h = 30 + rows_n * row_h + 8
        act_h = 30 + 26 * rows_used + log_n * LOG_PITCH + 8
        # The natural height; any height beyond it goes to the visitors section.
        nat = fixed - (30 + 8) - (30 + 26 * rows_used + 8) + vis_h + act_h
        if h is not None and h > nat:
            vis_h += h - nat
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
        """Return "TITLE  (hint)", or the title alone when both do not fit in room pixels."""
        full = "%s  (%s)" % (title, hint)
        return full if Kit.text_w(full) <= room else title

    def build_window():
        """Draw the main window, or the minimised bar, and fill it from the current state.

        Client tick. Uses the zone slot when the window sits in a zone: too narrow is laid out at its
        narrowest and drawn smaller, too short for that scrolls its body. Controls are kept in the
        window's store so refresh can rewrite them rather than rebuild.
        """
        slot = wnd.slot
        if st["minimized"]:
            w, h = (max(MINI_W, slot[0]) if slot else MINI_W), MINI_H
        elif slot is None:
            w, h = W, H
        else:
            w, h = slot
        g, store, c = wnd.begin(w, h)
        M = Kit.MARGIN
        rows = []
        k = 1.0
        fit["k"], fit["full"] = 1.0, None
        if st["minimized"]:
            c["mini_w"] = w
        else:
            lw, lh, body = w, h, None
            if slot is None:
                P = layout(lw, None)
                lh = P["h"]
            elif w < min_w():
                # Too narrow: lay out at the narrowest width and draw smaller. A zone too short for that as well
                # is drawn smaller still, laid out wider.
                k = w / float(min_w())
                P = layout(min_w(), int(h / k))
                if P["h"] > int(h / k) + 1:
                    k = min(k, h / float(P["h"]))
                lw, lh = int(round(w / k)), int(round(h / k))
                P = layout(lw, lh)
            else:
                P = layout(lw, lh)
                # Too short even at the fewest rows: the body scrolls and a scroll band is added to the width.
                if P["h"] > lh + 1:
                    lw = w - Kit.SCROLL_BAND
                    P = layout(lw, lh)
                    body = P["h"]
            win["P"] = P
            IW = P["IW"]
            wnd.frame(g, lw, lh)
            ys = P["ys"]
            Kit.add_section(g, M, ys, IW, P["sweep_h"], section_title("SWEEP", "Detect Hidden on your spot", IW - 12))
            c["sweep_lbl"] = Kit.art_button(g, store, "sweep", Kit.ART_PAGE, P["sweep_xy"][0],
                                            P["sweep_xy"][1], "Sweep: off",
                                            "Switch the automatic sweep: Detect Hidden on your spot whenever ready",
                                            on_click=queue("sweep"))
            Kit.art_button(g, store, "now", Kit.ART_PLAY, P["now_xy"][0], P["now_xy"][1], "Sweep now",
                           "Use Detect Hidden once, if ready", on_click=queue("now"))
            c["status"] = Kit.add_label(g, "", M + 10, P["status_y"], Kit.HUE_INFO)
            c["count"] = Kit.add_label(g, "", M + IW - 10, P["status_y"], Kit.HUE_INFO)
            c["count_y"] = P["status_y"]
            yv = P["yv"]
            near_w = Kit.text_w("99 near (%d shown)" % MAX_ROWS)
            Kit.add_section(g, M, yv, IW, P["vis_h"],
                            section_title("VISITORS", "players near you", IW - 12 - near_w - 16))
            c["near"] = Kit.add_label(g, "", M + IW - 10, yv + 6, Kit.HUE_INFO)
            c["near_y"] = yv + 6
            x_fr, x_ej, x_ban, x_dist = P["x"]
            c["name_w"], c["hidden_w"] = P["name_w"], Kit.text_w(" (hidden)")
            # Tooltip for a row's buttons; Ban's says a second click is needed when that setting is on.
            say_tip = "Say the %s command at them"
            btns = (("fr", Kit.ART_OK, x_fr, "Friend", say_tip % "friend" + ALT, "friend"),
                    ("ej", Kit.ART_PLAY, x_ej, "Eject", say_tip % "eject" + ALT, "eject"),
                    ("ban", Kit.ART_CLOSE, x_ban, "Ban", say_tip % "ban" + ("; click again within %d s to confirm"
                     % int(CONFIRM_SECS) if settings["confirm"] else "") + ALT, "ban"))
            row_h, bdy = P["row_h"], P["btn_dy"]
            for i in range(P["rows_n"]):
                ry = yv + 30 + i * row_h
                # Per-row state for Kit.row_set, which keeps what the row showed so a click just after a row
                # changed acts on the player the user saw.
                row = {"val": None, "prev": None, "changed": 0.0}
                row["name_lbl"] = Kit.add_label(g, "", M + 12, ry + 3, Kit.HUE_TEXT)
                row["dist_lbl"] = Kit.add_label(g, "", x_dist, ry + 3, Kit.HUE_INFO)
                row["catch"] = Kit.catcher(g, M + 10, ry, x_dist - M - 10 + P["dist_w"], ROW_H,
                                           Kit.row_clicker(row, queue, "last"), LAST_TIP)
                for bk, art, bx, cap, tip, act in btns:
                    row[bk] = Kit.art_button(g, store, "%s%d" % (bk, i), art, bx, ry + bdy, cap, tip,
                                             on_click=Kit.row_clicker(row, queue, act))
                    row[bk + "_btn"] = store[0]["%s%d" % (bk, i)]
                rows.append(row)
            # The empty-state sentence, wrapped, one label per line that fits.
            c["empty"] = [Kit.add_label(g, line, M + 12, yv + 33 + 20 * i, Kit.HUE_INFO)
                          for i, line in enumerate(P["empty"][:max(1, (P["vis_h"] - 33) // 20)])]
            ya = P["ya"]
            Kit.add_section(g, M, ya, IW, P["act_h"], section_title("ACTIONS", "pick with a cursor", IW - 12))
            for grp, places in zip(BUTTONS, P["groups"]):
                for (key, art, cap, tip, act_), (bx, brow) in zip(grp, places):
                    Kit.art_button(g, store, key, art, bx, ya + 26 + 26 * brow, cap, tip, on_click=queue(act_))
            ly = ya + 30 + 26 * P["act_rows"]
            c["log"] = [Kit.add_label(g, "", M + 12, ly + i * LOG_PITCH, Kit.HUE_INFO) for i in range(P["log_n"])]
            c["log_w"], c["log_full"] = IW - 70, IW - 24
            # Smaller than its layout: scale the whole window and remember the scale for drawn_at.
            if k != 1.0:
                fit["k"], fit["full"] = k, (int(min_w()), int(round(layout(min_w(), None)["h"])))
                Kit.scale_window(g, k)
            elif body is not None:
                w, h = lw, body
            else:
                w, h = lw, lh
        wnd.end(g, {"rows": rows}, w, h, slot[1] if (slot is not None and not st["minimized"]) else None)
        refresh()

    wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, icon=TRAY_ICON, cleanup=cleanup,
                     clear={"rows": []})

    def refresh():
        """Redraw the log lines, the visitor rows and the status line."""
        refresh_log()
        refresh_rows()
        refresh_status()

    # Every control of a visitor row, shown or hidden together.
    ROW_CTRLS = ("name_lbl", "dist_lbl", "catch", "fr", "fr_btn", "ej", "ej_btn", "ban", "ban_btn")

    def set_vis(ctrl, on, row, key):
        """Show or hide a control only when its state changes, keeping the last value on the row."""
        if row.get(key + "_vis") != on:
            row[key + "_vis"] = on
            ctrl.IsVisible = on

    def refresh_rows():
        """Rewrite the visitor rows from the last scan.

        Each row keeps a signature of what it shows and is skipped when nothing changed. Rows without a
        visitor hide their controls. The empty sentence and the "N near" count are set only when their
        inputs change; the count is right-aligned, so it is moved when its width changes.
        """
        rows = win["rows"]
        if not rows or st["minimized"]:
            return
        c = win["c"]
        vis = st["visitors"]
        now = time.time()
        name_w, hidden_w = c["name_w"], c["hidden_w"]
        for i, row in enumerate(rows):
            if i < len(vis):
                v = vis[i]
                Kit.row_set(row, (v["serial"], v["name"]), now)
                sig = (v["serial"], v["name"], v["noto"], v["hidden"], v["dist"], name_w, hidden_w)
                if row.get("sig") == sig:
                    continue
                row["sig"] = sig
                hue = NOTO_HUE.get(v["noto"], Kit.HUE_TEXT)
                # A hidden player's name gives way to a " (hidden)" tag so the row stays inside its column.
                if v["hidden"]:
                    hue = Kit.HUE_TITLE
                    Kit.set_text(row["name_lbl"], short(v["name"], name_w - hidden_w) + " (hidden)", hue)
                else:
                    Kit.set_text(row["name_lbl"], short(v["name"], name_w), hue)
                Kit.set_text(row["dist_lbl"], Kit.count(v["dist"], "tile"))
                for k in ROW_CTRLS:
                    set_vis(row[k], True, row, k)
            else:
                Kit.row_set(row, None, now)
                row["sig"] = None
                for k in ROW_CTRLS:
                    set_vis(row[k], False, row, k)
        lines = win["P"]["empty"]
        ek = c.get("empty_k")
        if ek is None or ek[0] != (not vis) or ek[1] is not lines:
            c["empty_k"] = (not vis, lines)
            for i, lbl in enumerate(c["empty"]):
                Kit.set_text(lbl, lines[i] if (not vis and i < len(lines)) else "")
        near = c["near"]
        nk = (st["near"], len(vis) > len(rows), len(rows))
        if c.get("near_k") != nk:
            c["near_k"] = nk
            txt = "%d near" % st["near"] if st["near"] else ""
            if len(vis) > len(rows):
                txt = "%d near (%d shown)" % (st["near"], len(rows))
            Kit.set_text(near, txt)
            tw = Kit.text_w(txt)
            if c.get("near_w") != tw:
                c["near_w"] = tw
                IW = win["P"]["IW"]
                at_k(near, Kit.MARGIN + IW - 10 - tw, c["near_y"])

    def log_line(entry, width):
        """Return one action log entry as "HH:MM  text" cut to width pixels, and its hue."""
        t, text, hue = entry
        return "%s  %s" % (time.strftime("%H:%M", time.localtime(t)), short(text, width)), hue

    def refresh_log():
        """Rewrite the action log lines in the main window, newest first, then the log window."""
        c = win["c"]
        lbls = c.get("log")
        if lbls:
            tail = log[-len(lbls):]
            for i, lbl in enumerate(lbls):
                if i < len(tail):
                    text, hue = log_line(tail[len(tail) - 1 - i], c["log_w"])
                    Kit.set_text(lbl, text, hue)
                else:
                    # With no entries the first line says so.
                    Kit.set_text(lbl, Kit.fit(EMPTY_LOG, c["log_full"]) if i == 0 else "", Kit.HUE_INFO)
        refresh_logwin()

    def log_min():
        """Return the smallest size the log window may take in a zone."""
        return LOG_W, LOG_FIXED + LOG_MIN_ROWS * LOG_ROW_H

    def log_close():
        """Close the log window, or redraw it in place when a zone holds it."""
        if Kit.zone_up(LOG_DOCK):
            build_logwin()
        else:
            logw.close()

    def build_logwin():
        """Draw the log window for the view shown (actions or visitors).

        Client tick. In a zone it takes the zone's size, else a row per kept line in steps of ten so
        the window is rebuilt at most a few times while the log fills. Outside a zone it has a Close
        button. Clear and the Actions / Visitors switch queue their actions.
        """
        M = Kit.MARGIN
        visits_view = win["log_view"] == "visits"
        held = Kit.zone_up(LOG_DOCK)
        lines, keep = (visits, VISIT_KEEP) if visits_view else (log, LOG_KEEP)
        mw, mh = log_min()
        z = logw.slot if held and logw.slot is not None and logw.slot[0] >= mw and logw.slot[1] >= mh else None
        # Rows: what the zone holds, else enough for every line in steps of ten.
        n = logw.rows(LOG_ROW_H, LOG_FIXED, 0) if z else min(keep, max(10, (len(lines) + 9) // 10 * 10))
        w, h = z if z else (LOG_W, LOG_FIXED + n * LOG_ROW_H)
        sh = h - M - 30 - Kit.GAP - M
        g, store, _c = logw.begin(w, h)
        Kit.add_window_frame(g, w, h)
        Kit.add_section(g, M, M, w - 2 * M, 30)
        Kit.add_label(g, LOG_TITLE.upper(), M + 30, M + 7, Kit.HUE_TITLE)
        if not held:
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, "Close the log",
                           on_click=queue("show_log"))
        x_clr = w - M - (10 if held else 66) - 35 - Kit.text_w("Clear")
        Kit.art_button(g, store, "clear", Kit.ART_CLOSE, x_clr, M + 4, "Clear",
                       "Forget these visits" if visits_view else "Forget these actions", on_click=queue("log_clear"))
        cap = "Actions" if visits_view else "Visitors"
        Kit.art_button(g, store, "view", Kit.ART_PAGE, x_clr - 12 - 35 - Kit.text_w(cap), M + 4, cap,
                       "Show what the butler did" if visits_view else "Show who came into the house",
                       on_click=queue("log_view"))
        ys = M + 30 + Kit.GAP
        Kit.add_section(g, M, ys, w - 2 * M, sh, "VISITORS  (while you were inside)" if visits_view
                        else "ACTIONS  (newest first, %d kept)" % LOG_KEEP)
        rows = []
        for i in range(n):
            ry = ys + 30 + i * LOG_ROW_H
            row = {"lbl": Kit.add_label(g, "", M + 12, ry, Kit.HUE_INFO), "catch": None,
                   "val": None, "prev": None, "changed": 0.0}
            # A visitor row is clickable: it sets the last target, and Alt+click follows.
            if visits_view:
                row["catch"] = Kit.catcher(g, M + 10, ry - 1, w - 2 * M - 20, LOG_ROW_H,
                                           Kit.row_clicker(row, queue, "last"), LAST_TIP)
            rows.append(row)
        logw.end(g, {"rows": rows, "w": w})
        refresh_logwin()

    logw = Kit.Window(LOG_DOCK, LOG_TITLE, logs, logs, build_logwin, LOG_POS_KEY, default=(240, 240), cleanup=cleanup,
                      lock=True, owner=False, clear={"rows": []})

    def visit_line(e, width, now):
        """Return one visit as a line and its hue: when, name, notoriety, how often, ejected or banned.

        The time shows the date only when it is not today. "inside" marks a visit still open; a visit
        with no leave time (the module stopped while they were in) ends in a question mark.
        """
        t_in, t_out, serial, name, noto, times, flag = e
        lt = time.localtime(t_in)
        when = time.strftime("%H:%M" if lt[:3] == time.localtime(now)[:3] else "%b %d %H:%M", lt)
        if st["open_visits"].get(serial) is e:
            when += ", inside"
        elif t_out:
            when += "-" + time.strftime("%H:%M", time.localtime(t_out))
        else:
            # No leave time was recorded: the module stopped while they were inside.
            when += "-?"
        tail = " (%s)" % noto
        if times > 1:
            tail += "  %d times" % times
        if flag:
            tail += "  banned" if flag == 2 else "  ejected"
        name_w = max(60, width - Kit.text_px(when + "  " + tail))
        return "%s  %s%s" % (when, short(name, name_w), tail), NOTO_HUE.get(noto, Kit.HUE_TEXT)

    def refresh_logwin():
        """Rewrite the log window's rows from the log or the visits.

        A window outside a zone is rebuilt when there are more lines than rows. Visitor rows redraw only
        when their key changed and follow the visit they show so a click acts on it.
        """
        g = logs["g"]
        if not Kit.is_open(g):
            return
        rows = logs["rows"]
        visits_view = win["log_view"] == "visits"
        lines = visits if visits_view else log
        if len(lines) > len(rows) and not Kit.zone_up(LOG_DOCK):
            build_logwin()
            return
        n = len(lines)
        now = time.time()
        for i, row in enumerate(rows):
            if i < n:
                e = lines[n - 1 - i]
                if visits_view:
                    key = (e[0], e[2], e[1], e[5], e[6], st["open_visits"].get(e[2]) is e)
                    if row.get("key") != key:
                        row["key"] = key
                        text, hue = visit_line(e, logs["w"] - 2 * Kit.MARGIN - 28, now)
                        Kit.set_text(row["lbl"], text, hue)
                    Kit.row_set(row, (e[2], e[3]), now)
                else:
                    text, hue = log_line(e, logs["w"] - 2 * Kit.MARGIN - 70)
                    Kit.set_text(row["lbl"], text, hue)
            else:
                Kit.set_text(row["lbl"], (EMPTY_VISITS if visits_view else EMPTY_LOG) if i == 0 else "", Kit.HUE_INFO)
                row["key"] = None
                Kit.row_set(row, None, now)
            if row["catch"] is not None:
                set_vis(row["catch"], i < n, row, "catch")

    def status_text(now):
        """Return the status line text and hue for the main window.

        In order: a house command waiting, a short note, the Detect Hidden phases, then the sweep's
        state with the seconds left or the reason it is held.
        """
        h = st["house"] or st["house_wait"]
        if h is not None:
            return ("%s %s: waiting for the %s cursor" % (VERBS[h["kind"]], h["name"] or "the target",
                    "house" if st["house"] is not None else "sweep"), Kit.HUE_TITLE)
        if st["note"] and now < st["note_until"]:
            return st["note"], Kit.HUE_INFO
        if st["phase"] == "cursor":
            return "Detect Hidden: waiting for cursor", Kit.HUE_TITLE
        if st["phase"] == "cast":
            return "Detect Hidden: sweeping", Kit.HUE_GOOD
        # Seconds left of the cooldown, rounded up when shown.
        rem = wait_left(now)
        if not st["sweep"]:
            return ("Sweep off; ready in %d s" % int(rem + 0.99) if rem > 0 else "Sweep off; ready"), Kit.HUE_INFO
        if st["held"] == HELD_UNKNOWN:
            return HELD_UNKNOWN, Kit.HUE_INFO
        if st["held"]:
            return "Sweep on, waiting: %s" % st["held"], Kit.HUE_INFO
        if rem > 0:
            return "Sweep on: next in %d s" % int(rem + 0.99), Kit.HUE_GOOD
        if settings["still"] and now - st["moved_at"] < STILL_SECS:
            return "Sweep on: stand still", Kit.HUE_INFO
        return "Sweep on: ready", Kit.HUE_GOOD

    def mini_text():
        """Return the minimised bar's text: the title, what the sweep is doing, then how many are near."""
        if st["house"] is not None or st["house_wait"] is not None:
            s = "house command"
        elif st["phase"] != "idle":
            s = "sweeping"
        elif st["sweep"]:
            s = "sweep on, waiting" if st["held"] else "sweep on"
        else:
            s = "sweep off"
        if st["near"]:
            s += ", %d near" % st["near"]
        return "%s: %s" % (TITLE, s)

    def cut_once(c, key, text, room):
        """Return text cut to room pixels, cutting again only when the text or room changed.

        One cache entry per label is kept in the window's controls dict under key.
        """
        e = c.get(key)
        if e is not None and e[0] == text and e[1] == room:
            return e[2]
        cut = short(text, room)
        c[key] = (text, room, cut)
        return cut

    def refresh_status():
        """Rewrite the status line, the Sweep switch caption and the sweeps and revealed count.

        Runs every tick; labels are set only when their text changes. A cut status line carries its
        whole text as a tooltip. The count sits at the right of the row and is moved when its width
        changes.
        """
        c = win["c"]
        if win["g"] is None or (st["minimized"] and st["docked"]):
            return
        now = time.time()
        text, hue = status_text(now)
        if st["minimized"]:
            lbl = c.get("status")
            if lbl is not None:
                Kit.set_text(lbl, cut_once(c, "mini_k", mini_text(), c.get("mini_w", MINI_W) - 90), hue)
            return
        P = win.get("P") or {}
        lbl = c.get("status")
        if lbl is not None:
            # Cut to its part of the row: the count sits at the right, so a long name in the status line
            # must not run under it.
            cut = cut_once(c, "status_k", text, P.get("status_room", W - 2 * Kit.MARGIN - 160))
            if Kit.set_text(lbl, cut, hue):
                lbl.SetTooltip(text if cut != text else "")
        sl = c.get("sweep_lbl")
        if sl is not None:
            Kit.set_text(sl, "Sweep: on" if st["sweep"] else "Sweep: off",
                         Kit.HUE_GOOD if st["sweep"] else Kit.HUE_TEXT)
        cnt = c.get("count")
        ck = (st["sweeps"], st["revealed"], P.get("count_room", 400))
        if cnt is not None and c.get("count_k") != ck:
            c["count_k"] = ck
            txt = ("%s, %d revealed" % (Kit.count(st["sweeps"], "sweep"), st["revealed"]))
            txt = Kit.fit(txt, P.get("count_room", 400))
            if Kit.set_text(cnt, txt) or c.get("count_w") is None:
                tw = Kit.text_w(txt)
                if c.get("count_w") != tw:
                    c["count_w"] = tw
                    IW = P.get("IW", W - 2 * Kit.MARGIN)
                    at_k(cnt, Kit.MARGIN + IW - 10 - tw, c["count_y"])

    def scan_visitors(now, me):
        """Read the players within range, nearest first, and update the visitor rows.

        Client tick, at most every SCAN_EVERY seconds (sooner after a poke). Returns True when a scan was
        made. Names and notorieties come from a cache, since they change rarely; position and the
        hidden flag are read every scan. Your own mobile, pets, invulnerable vendors and, when the
        setting is off, allies are left out. Also tracks which visitors stand inside a house.
        """
        if 0 <= now - st["scan_at"] < (SCAN_POKE if st["scan_poke"] else SCAN_EVERY):
            return False
        st["scan_at"] = now
        st["scan_poke"] = False
        mx, my = int(me.X), int(me.Y)
        my_serial = me.Serial
        if st["pos"] != (mx, my):
            st["pos"], st["moved_at"] = (mx, my), now
        rng = settings["range"]
        # The client's own filter keeps humans only, which is cheaper than testing each mobile.
        mobs = API.GetAllMobiles(distance=rng, isHuman=True) or []
        cache = st["ncache"]
        # Keep the cache bounded: drop expired entries first, clear it if that is not enough.
        if len(cache) > NAME_CACHE_MAX:
            for k in [k for k, e in cache.items() if now >= e[0]]:
                del cache[k]
            if len(cache) > NAME_CACHE_MAX:
                cache.clear()
        out = []
        for m in mobs:
            try:
                serial = m.Serial
                if serial == my_serial:
                    continue
                e = cache.get(serial)
                if e is not None and now < e[0]:
                    name, noto = e[1], e[2]
                # A renamable mobile is a pet: remember that for a moment and never list it.
                elif m.IsRenamable:
                    cache[serial] = (now + NAME_CACHE_SECS, None, "pet")
                    continue
                else:
                    noto = Kit.noto_name(m)
                    name = str(m.Name or "")
                    cache[serial] = (now + NAME_CACHE_SECS, name, noto)
                # Pets (cached as no name), vendors and healers are never visitors.
                if name is None or noto == "invulnerable" or (noto == "ally" and not settings["friends"]):
                    continue
                vx, vy = int(m.X), int(m.Y)
                dist = max(abs(vx - mx), abs(vy - my))
                if dist > rng:
                    continue
                out.append({"serial": serial, "name": name, "noto": noto, "dist": dist, "hidden": bool(m.IsHidden),
                            "x": vx, "y": vy, "inside": False})
            # A mobile that vanished mid-scan is skipped.
            except Exception:
                continue
        out.sort(key=_by_dist)
        st["near"] = len(out)
        st["visitors"] = out
        track_house(now, mx, my, out)
        refresh_rows()
        return True

    def _by_dist(v):
        """Sort key for visitors: distance, then name."""
        return (v["dist"], v["name"].lower())

    def multi_at(x, y):
        """Is a house tile at x, y? Uses the client's own house data; one call, no waiting."""
        return len(API.GetMultisAt(x, y) or ()) > 0

    def track_house(now, mx, my, out):
        """After a scan, work out whether you stand in a house and which visitors do.

        Your own tile is looked up when you move, else every HOUSE_EVERY seconds. A visitor's tile is
        looked up only if they moved, at most HOUSE_CHECKS per scan; the rest keep their last answer.
        Opens a visit when a player is inside, closes it when they step out, leave range or you leave.
        """
        if st["house_pos"] != (mx, my) or now >= st["house_at"]:
            st["house_pos"], st["house_at"] = (mx, my), now + HOUSE_EVERY
            st["in_house"] = multi_at(mx, my)
        opened = st["open_visits"]
        if not st["in_house"]:
            st["inside"] = {}
            close_visits(now)
            return
        old = st["inside"]
        new = {}
        # Lookups still allowed in this scan.
        budget = HOUSE_CHECKS
        for v in out:
            s = v["serial"]
            e = old.get(s)
            if e is None or e[0] != v["x"] or e[1] != v["y"]:
                # Moved or new: look again while the budget lasts.
                if budget > 0:
                    budget -= 1
                    e = (v["x"], v["y"], multi_at(v["x"], v["y"]))
                # New and over this scan's budget: leave it for the next scan.
                elif e is None:
                    continue
            new[s] = e
            inside = e[2]
            v["inside"] = inside
            if inside:
                if s not in opened:
                    open_visit(v, now)
            elif s in opened:
                close_visit(s, now)
        st["inside"] = new
        # A visit whose player is out of range or gone ends.
        for s in [s for s in opened if s not in new]:
            close_visit(s, now)

    def open_visit(v, now):
        """Start a visit for visitor v, or reopen their last one if it ended within VISIT_MERGE seconds.

        A reopened visit counts one more time in. The log is flagged for saving.
        """
        s = v["serial"]
        # Their latest visit, searched from the newest.
        e = next((r for r in reversed(visits) if r[2] == s), None)
        if e is not None and e[1] and now - e[1] <= VISIT_MERGE:
            e[1] = 0.0
            e[5] += 1
        else:
            e = [now, 0.0, s, v["name"] or "someone", v["noto"], 1, 0]
            visits.append(e)
            del visits[:-VISIT_KEEP]
        st["open_visits"][s] = e
        visits_changed()

    def close_visit(s, now):
        """End the open visit of serial s at time now. Does nothing when none is open."""
        e = st["open_visits"].pop(s, None)
        if e is not None:
            e[1] = now
            visits_changed()

    def close_visits(now):
        """End every open visit, as when you leave the house or the module stops."""
        for s in list(st["open_visits"]):
            close_visit(s, now)

    def mark_visit(serial, flag):
        """Record on the latest visit of this serial that they were ejected (1) or banned (2)."""
        e = next((r for r in reversed(visits) if r[2] == serial), None)
        if e is not None:
            e[6] = flag
            visits_changed()

    def is_foe(serial, name, now):
        """Is this player on Ultima Tracker's Foe list? False when that service is not offered.

        The answer is cached per serial for NAME_CACHE_SECS and the cache is cleared when it grows past
        NAME_CACHE_MAX; a failing service counts as no.
        """
        fn = HOST.services.get(FOE_SERVICE)
        if fn is None:
            return False
        c = st["foe"].get(serial)
        if c is not None and now < c[0]:
            return c[1]
        try:
            r = bool(fn(serial, name))
        except Exception:
            r = False
        if len(st["foe"]) > NAME_CACHE_MAX:
            st["foe"].clear()
        st["foe"][serial] = (now + NAME_CACHE_SECS, r)
        return r

    def eject_on_sight(now):
        """Raise an alert for a red or Foe player standing inside your house.

        Runs after a scan when the setting is on and you are in a house. It never ejects: the alert asks
        whether to eject, and the Eject button on the player's row does it on your press, as R8 requires
        for anything against a player. Each player alerts at most once per EJECT_FOE_EVERY seconds;
        party members and friends are never flagged. When HOST.alert does not raise the alert, the line
        goes to the action log instead.
        """
        if not settings["eject_foes"] or not st["in_house"]:
            return
        eject_at = st["eject_at"]
        mates = None
        for v in st["visitors"]:
            if not v["inside"] or v["hidden"]:
                continue
            s = v["serial"]
            if eject_at.get(s, 0.0) > now:
                continue
            if v["noto"] != "murderer" and not is_foe(s, v["name"], now):
                continue
            # Party members and friends are looked up only when a candidate turns up, and then once.
            if mates is None:
                mates = {int(x) for x in list(API.GetPartyMemberSerials() or []) + list(API.GetAllFriends() or [])}
            if s in mates:
                continue
            if len(eject_at) > NAME_CACHE_MAX:
                for k in [k for k, t in eject_at.items() if t <= now]:
                    del eject_at[k]
            eject_at[s] = now + EJECT_FOE_EVERY
            what = "red" if v["noto"] == "murderer" else "Foe"
            if not HOST.alert(ALERT_FOE, "%s (%s) in your house: Eject from their row?"
                              % (v["name"] or "Someone", what), "alarm", who=s):
                add_log("%s (%s) stepped in" % (v["name"] or "someone", what), Kit.HUE_BAD)
            return

    def sweep_held(now):
        """Return why the sweep may not use the skill, as the mother's hold text, or None.

        Client tick, called while the sweep is on. The sweep is a skill loop, so R3 applies. The tests
        are shared with every loop so they agree: HOST.fight_hold (dead, war mode, hurt, hostile near,
        item on the cursor) and HOST.guard_hold (guarded region, or a zone not known yet, which holds),
        then any module's raised alarm. Dead is checked first and the guard text before the other fight
        reasons.
        """
        # Asked every time: it also keeps the hit point watch.
        fight = HOST.fight_hold(now)
        if fight == "dead":
            return HOLD_TEXT["dead"]
        g = HOST.guard_hold()
        if g == "guard":
            return HOLD_TEXT["guard"]
        if g is not None:
            return HELD_UNKNOWN
        if fight:
            return HOLD_TEXT.get(fight, fight)
        return HOLD_TEXT["alarm"] if HOST.alarm_up() else None

    def wait_left(now):
        """Seconds left before the skill may be used again, 0 when ready or the time is implausible."""
        rem = st["next_at"] - now
        return rem if 0 < rem <= COOLDOWN_MAX else 0.0

    def start_sweep(now, forced=False):
        """Use Detect Hidden if the sweep may run, and claim the cursor it raises. Returns True when used.

        Client tick. forced is a press of Sweep now: it says why in a short note when it cannot run.
        Not used while a house command runs, a phase is under way, the sweep is held, the cooldown is
        running, a target cursor is up, or (when the setting is on) you have moved within STILL_SECS.
        """
        if st["house"] is not None:
            if forced:
                note(RUNNING)
            return False
        if st["phase"] != "idle":
            return False
        held = st["held"]
        if held:
            if forced:
                note(held if held == HELD_UNKNOWN else "The sweep waits: %s" % held)
            return False
        rem = wait_left(now)
        if rem > 0:
            if forced:
                note("Ready in %d s" % int(rem + 0.99))
            return False
        if not forced and settings["still"] and now - st["moved_at"] < STILL_SECS:
            return False
        if not cursor_free():
            if forced:
                note("A target cursor is up: the sweep waits")
            return False
        me = HOST.me()
        # A fresh look at who is in view now, so only people appearing after the aim count as revealed.
        if me is not None:
            st["scan_at"] = 0.0
            scan_visitors(now, me)
        st["seen"] = {v["serial"] for v in st["visitors"] if not v["hidden"]}
        st["first_d"] = {}
        st["reveal_line"] = False
        API.UseSkill(DETECT_SKILL)
        HOST.claim_cursor(KEY, CURSOR_WAIT)
        st["phase"], st["deadline"] = "cursor", now + CURSOR_WAIT
        return True

    def sweep_tick(now):
        """Advance the Detect Hidden flow: aim the cursor, then watch for reveals.

        Client tick. In phase "cursor" it waits for the skill's own neutral cursor and aims it at you,
        giving up at the deadline. Another claim or a hand pick means waiting; a harmful or beneficial
        cursor belongs to a spell, so it is never aimed or cancelled and the sweep drops. In phase "cast"
        anyone who was not in view before and appears within REVEAL_WINDOW is called out, logged and
        counted, then the phase ends after REPLY_WAIT.
        """
        if st["phase"] == "cursor":
            # Check the deadline first so another claim cannot keep the sweep waiting past it, then step aside
            # for anyone else's claim or pick, and aim only a neutral cursor.
            if now > st["deadline"]:
                HOST.release_cursor(KEY)
                st["phase"], st["next_at"] = "idle", now + RETRY_SOON
                note("No Detect Hidden cursor; retrying")
            elif HOST.cursor_busy(KEY) is not None:
                return
            elif HOST.cursor_ok(KEY, "neutral"):
                # Your own spot: Detect Hidden then searches the area round you.
                API.TargetSelf()
                HOST.release_cursor(KEY)
                st["phase"], st["cast_at"] = "cast", now
                st["next_at"] = now + settings["cooldown"]
                st["sweeps"] += 1
            elif has_target():
                HOST.release_cursor(KEY)
                st["phase"], st["next_at"] = "idle", now + RETRY_SOON
                add_log("sweep dropped: a spell cursor came up", Kit.HUE_INFO)
            return
        if st["phase"] == "cast":
            # The shard reveals at once, so a newcomer in this window was revealed. One first seen far out at
            # the edge of range is taken as someone walking in, unless a reveal line came from the journal.
            if now - st["cast_at"] <= REVEAL_WINDOW:
                fd = st["first_d"]
                # Distance beyond which a first sighting looks like a walker arriving.
                edge = max(1, settings["range"] - 2)
                for v in st["visitors"]:
                    if v["serial"] not in st["seen"] and not v["hidden"]:
                        if fd.setdefault(v["serial"], v["dist"]) > edge and not st["reveal_line"]:
                            continue
                        st["seen"].add(v["serial"])
                        st["revealed"] += 1
                        API.HeadMsg("* revealed *", v["serial"], Kit.HUE_BAD)
                        add_log("revealed %s" % (v["name"] or "someone"), Kit.HUE_BAD)
                        if settings["sound"]:
                            HOST.alert(ALERT_REVEAL, "Revealed %s" % (v["name"] or "someone"), "warn", who=v["serial"])
            if now - st["cast_at"] > REPLY_WAIT:
                st["phase"] = "idle"

    def on_journal(ln):
        """Read one journal line while a sweep or a house command waits for the shard.

        Ignored when nothing waits. A skill delay gives the cooldown back and retries soon. A reveal line
        sets a flag and alerts. For a house command a success line is logged (and marks the visit for an
        eject or ban) and a refusal is logged with the shard's own words; either ends the command.
        """
        now = time.time()
        # True while a sweep is waiting for the shard.
        sw = st["phase"] in ("cursor", "cast") or now - st["cast_at"] < REPLY_WAIT
        if not sw and st["house"] is None and st["house_wait"] is None:
            return
        low = ln.low
        if sw:
            if any(t in low for t in J_WAIT):
                if st["phase"] == "cursor":
                    HOST.release_cursor(KEY)
                elif st["phase"] == "cast":
                    # The sweep was counted when aimed; the delay means it did not happen.
                    st["sweeps"] = max(0, st["sweeps"] - 1)
                st["phase"], st["next_at"] = "idle", time.time() + RETRY_SOON
                note("Skill delay: retrying")
                return
            # Nothing hidden there: no reaction needed.
            if any(t in low for t in J_NOTHING):
                return
            if any(t in low for t in J_REVEAL):
                st["reveal_line"] = True
                note("Someone was revealed", 6.0)
                if settings["sound"]:
                    HOST.alert(ALERT_REVEAL, "Someone was revealed", "warn")
                return
        h = st["house"]
        if h is None:
            return
        if any(t in low for t in J_DONE[h["kind"]]):
            add_log("%s %s" % (CMDS[h["kind"]][1], h["name"] or "the target"), Kit.HUE_GOOD)
            if h["kind"] in ("eject", "ban"):
                mark_visit(h["serial"], 2 if h["kind"] == "ban" else 1)
            finish_house()
            return
        if any(t in low for t in J_HOUSE_NO):
            add_log("%s %s failed: %s" % (who(h) + (ln.text.strip(),)), Kit.HUE_BAD)
            finish_house()
            return

    def start_house(kind, serial, name, now, waited=False):
        """Say a house command and claim the cursor the house raises for it.

        kind is eject, ban, friend, lock or release; serial and name are the target. waited is set when
        this is the retry after waiting for the sweep's cursor. Refused with a short note when another
        command runs, the words are empty or a cursor is up. Client tick.
        """
        if st["house"] is not None or (st["house_wait"] is not None and not waited):
            note(RUNNING)
            return
        if st["phase"] == "cursor":
            # Detect Hidden was just used and its cursor is still to come: saying the command now would let
            # that cursor arrive first and be aimed at you, leaving the house's cursor up. Wait for the
            # sweep's cursor to resolve, at most CURSOR_WAIT seconds, then say the command.
            st["house_wait"] = {"kind": kind, "serial": serial, "name": name, "until": now + CURSOR_WAIT}
            st["confirm"] = None
            return
        if not settings[CMDS[kind][0]]:
            note("Type the words for %s on the settings page" % VERBS[kind])
            return
        if not cursor_free():
            note(NO_CURSOR)
            return
        if not name:
            # The name was not given (a pick by serial): read it from the target for the log.
            name = str(safe(lambda: find_t(kind, serial).Name, "") or "")
        # Speak the house command: this is what makes the house raise its cursor.
        API.Msg(settings[CMDS[kind][0]])
        HOST.claim_cursor(KEY, CURSOR_WAIT)
        st["house"] = {"kind": kind, "serial": serial, "name": name, "deadline": now + CURSOR_WAIT, "aimed": 0.0}
        st["confirm"] = None

    def finish_house():
        """End the running house command and give the cursor claim back."""
        st["house"] = None
        HOST.release_cursor(KEY)

    def house_wait_tick(now):
        """Say a house command that was held back for the sweep's cursor, once that cursor is aimed or
        given up and no cursor is up.

        At the deadline a sweep cursor that never came is released and the command goes ahead.
        """
        hw = st["house_wait"]
        if hw is None:
            return
        if st["phase"] != "cursor" and cursor_free():
            st["house_wait"] = None
            start_house(hw["kind"], hw["serial"], hw["name"], now, waited=True)
        elif now > hw["until"]:
            st["house_wait"] = None
            # The skill never gave a cursor: let it go.
            if st["phase"] == "cursor":
                HOST.release_cursor(KEY)
                st["phase"], st["next_at"] = "idle", now + RETRY_SOON
            if cursor_free():
                start_house(hw["kind"], hw["serial"], hw["name"], now, waited=True)
            else:
                note(NO_CURSOR)

    def house_tick(now):
        """Advance a running house command: aim the house's cursor at the target, then wait for a reply.

        Client tick. Check the deadline first, then step aside for another claim or a hand pick, and aim
        only a neutral cursor: a harmful or beneficial one is someone's spell, so the command is dropped
        and the cursor never aimed or cancelled. A target out of sight cancels. With no journal reply
        within REPLY_WAIT it logs what was done.
        """
        h = st["house"]
        if h is None:
            return
        if not h["aimed"]:
            if now <= h["deadline"]:
                if HOST.cursor_busy(KEY) is not None:
                    return
                if not HOST.cursor_ok(KEY, "neutral"):
                    if has_target():
                        add_log("%s %s: dropped, a spell cursor came up" % who(h), Kit.HUE_BAD)
                        finish_house()
                    return
                if find_t(h["kind"], h["serial"]) is None:
                    API.CancelTarget()
                    add_log("%s %s: out of sight" % who(h), Kit.HUE_BAD)
                    finish_house()
                    return
                API.Target(h["serial"])
                HOST.release_cursor(KEY)
                h["aimed"] = now
            # Past the deadline: give up.
            else:
                add_log("%s %s: no house cursor (in your house, with the right? Else use the house sign)" % who(h),
                        Kit.HUE_BAD)
                finish_house()
            return
        # No journal reply seen: say what was aimed.
        if now - h["aimed"] > REPLY_WAIT:
            add_log("%s aimed at %s (no reply seen)" % who(h))
            finish_house()

    def want_ban(serial, name, now):
        """Ban, asking for a second click within CONFIRM_SECS first when that setting is on.

        A second click within 0.3 s of the first is ignored, so a double click does not confirm.
        """
        if settings["confirm"]:
            c = st["confirm"]
            if not (c and c[0] == serial and now < c[1]):
                st["confirm"] = (serial, now + CONFIRM_SECS, now)
                note("Ban %s? Click Ban again to confirm" % (name or "them"), CONFIRM_SECS)
                return
            if len(c) > 2 and now - c[2] < 0.3:
                return
        start_house("ban", serial, name, now)

    def act_sweep(action, now, me):
        """Action: switch the automatic sweep on or off and save the choice."""
        st["sweep"] = not st["sweep"]
        Kit.put_var(VIEW_KEY, "1" if st["sweep"] else "0")
        say("sweep %s." % ("on" if st["sweep"] else "off"), Kit.HUE_GOOD if st["sweep"] else Kit.HUE_INFO)

    def act_now(action, now, me):
        """Action: Sweep now. Reads why the sweep is held, then starts it as forced."""
        if me is not None and st["phase"] == "idle":
            st["held"] = sweep_held(now)
        if me is not None and not start_sweep(now, forced=True) and st["phase"] != "idle":
            note("A sweep is already running")

    def act_show_log(action, now, me):
        """Action: open or close the log window."""
        if Kit.is_open(logs["g"]):
            log_close()
        else:
            build_logwin()

    def act_log_view(action, now, me):
        """Action: switch the log window between the actions and the visitors, and save the choice."""
        win["log_view"] = "log" if win["log_view"] == "visits" else "visits"
        Kit.put_var(LOG_VIEW_KEY, win["log_view"])
        if Kit.is_open(logs["g"]):
            build_logwin()

    def act_clear(action, now, me):
        """Action: clear the visitors (log window on Visitors) or the actions, else the actions.

        The visitors clear also forgets who is inside; the actions clear flags the log for saving.
        """
        if action == "log_clear" and win["log_view"] == "visits":
            del visits[:]
            st["open_visits"], st["inside"] = {}, {}
            visits_changed()
        else:
            del log[:]
            st["log_dirty"] = True
            refresh_log()

    def picked(which):
        """Return the callback for a hand pick of the given kind.

        The callback queues the kind and the picked serial for the tick, or says nothing was picked.
        """
        def done(serial):
            """Handle the cursor answer: a serial of 0 is a cancelled pick, anything else is queued."""
            serial = int(serial or 0)
            if not serial:
                note("Nothing picked")
                return
            # dup=True lets the same pick be queued again.
            queue.add((which, serial, None), dup=True)

        return done

    def act_pick(action, now, me):
        """Action: raise a target cursor to pick a player or an item for a house command.

        The cursor stays up for PICK_WAIT seconds; the pick is answered by picked(). Refused while a
        house command runs.
        """
        which = action[5:]
        if st["house"] is not None or st["house_wait"] is not None:
            note(RUNNING)
        else:
            note("Target the %s to %s (Esc cancels)" % (
                "player" if CMDS[which][2] == "mobile" else "item", VERBS[which].lower()), PICK_WAIT)
            HOST.pick_target(PICK_WAIT, picked(which))

    def act_last(action, now, me):
        """Action: set the row's player as the last target and call it out over their head."""
        API.SetLastTarget(serial=action[1])
        API.HeadMsg("* last target *", action[1], 0x35)

    def act_house(action, now, me):
        """Action: say the house command for the row or pick it came from."""
        start_house(action[0], action[1], action[2], now)

    # Every queued action by name. Row clicks queue a tuple of (kind, serial, name); button clicks
    # queue a plain name.
    ACTIONS = {"sweep": act_sweep, "now": act_now, "show_log": act_show_log, "log_view": act_log_view,
               "log_clear": act_clear, "clear_log": act_clear, "pick_eject": act_pick, "pick_ban": act_pick,
               "pick_friend": act_pick, "pick_lock": act_pick, "pick_release": act_pick,
               "follow": lambda action, now, me: Follow.toggle(action[1], TITLE), "last": act_last,
               "ban": lambda action, now, me: want_ban(action[1], action[2], now), "eject": act_house,
               "friend": act_house, "lock": act_house, "release": act_house}
    # Tooltip of the alarm setting.
    EJECT_TIP = ("Foe: on Ultima Tracker's Foe list; once per player every %d s; Eject on their row ejects them"
                 % int(EJECT_FOE_EVERY))
    # Layout options of the settings page.
    PAGE_OPTS = {"ldy": 4, "fh": 30, "ugap": 6}

    def page_table(w):
        """Return the settings page's rows for width w, for Kit.Page.

        Three sections: the sweep, the visitors and the house command words in two columns.
        """
        col = (w - 24) // 2
        lw1 = max(Kit.text_w(t) for t in ("Eject:", "Ban:", "Friend:"))
        lw2 = max(Kit.text_w(t) for t in ("Lock down:", "Release:"))
        left, right = {"lw": lw1, "tw": col - lw1 - 26}, {"dx": 12 + col, "lw": lw2, "tw": col - lw2 - 26}
        return (("SWEEP  (Detect Hidden on your spot)", (
                    ("num", "cooldown", "Seconds between uses:", "Wait after each use, the shard's skill delay", None,
                     COOLDOWN_MIN, COOLDOWN_MAX, {"cast": float}),
                    ("check", "still", "Sweep only when standing still", "Waits until you have stood still 1 s"),
                    ("check", "sound", "Alert when a sweep reveals someone", "Sound: Settings > Alerts"))),
                ("VISITORS", (("num", "range", "List players within:", "Players this close are listed", "tiles",
                     RANGE_MIN, RANGE_MAX), ("check", "friends", "List guild and alliance members too",
                     "Unticked, green players are left out"),
                    ("check", "confirm", "Ban needs a second click within %d s" % int(CONFIRM_SECS),
                     "So the wrong person isn't banned"),
                    ("check", "eject_foes", "Alarm when a red or Foe enters the house", EJECT_TIP))),
                ("HOUSE COMMANDS  (said out loud)", (
                    ("text", "eject_cmd", "Eject:", "Ejects a player (owner, co-owner or friend)", left),
                    ("text", "ban_cmd", "Ban:", "Bans a player (owner or co-owner)", left),
                    ("text", "friend_cmd", "Friend:", "Makes a player a house friend (owner)", left), ("gap", -90),
                    ("text", "lock_cmd", "Lock down:", "Locks an item down (owner, co-owner or friend)", right),
                    ("text", "release_cmd", "Release:", "Releases a locked-down item (owner or co-owner)", right),
                    ("gap", 30),
                    ("note", Kit.wrap("Owner adds friends; owner and co-owners ban and release; friends eject "
                                      "and lock down.", w - 28)[0], {"ndy": 4, "h": 24}))))

    def on_change(old, new):
        """Settings page hook: react to a changed setting.

        Turning the alarm on or off forgets its per-player timers; changing the Ban confirmation redraws
        the window so the Ban tooltip matches.
        """
        if new["eject_foes"] != old["eject_foes"]:
            st["eject_at"].clear()
        if new["confirm"] != old["confirm"] and not st["minimized"]:
            queue("redraw")()

    # The settings page, built from page_table.
    cfg = Kit.Page(settings, page_table, save_settings, on_change, PAGE_OPTS, strict=True)
    load_settings()

    def on_mobile(*args):
        """Event: a mobile appeared. While a sweep is under way, make the next scan come soon."""
        if not st["shutting"] and st["phase"] != "idle":
            st["scan_poke"] = True

    def _start():
        """Module start, on the client tick: reset the state, load the settings, draw and dock the windows.

        Registers the two alert kinds (revealed, red or Foe), opens a journal reader, hooks the mobile
        created event once and tells the user the state in the journal.
        """
        st.update({"shutting": False, "docked": False, "queue": [], "phase": "idle",
                   "house": None, "house_wait": None, "confirm": None, "visitors": [], "near": 0,
                   "scan_at": 0.0, "ncache": {}, "log_dirty": False, "log_save_at": 0.0,
                   "pos": None, "moved_at": 0.0, "note": "", "note_until": 0.0,
                   "in_house": None, "house_pos": None, "house_at": 0.0, "inside": {},
                   "open_visits": {}, "visits_dirty": False, "visits_save_at": 0.0, "visits_redraw": False,
                   "eject_at": {}, "foe": {}, "held": None, "held_at": 0.0, "minimized": wnd.start_min()})
        # Forget any zone slot left from the last run.
        wnd.slot = None
        fit.update({"k": 1.0, "full": None})
        load_settings()
        # The reader is polled through new() on every tick.
        st["rd"] = Journal.reader()
        HOST.alert_kind(ALERT_REVEAL, "Someone revealed", REVEAL_SOUND)
        HOST.alert_kind(ALERT_FOE, "Red or Foe in your house", ALERT_FOE_SOUND)
        build_window()
        # Hooked only once, tracked by st["hooked"].
        Kit.hook_once(st, "hooked", ("ApiMobileCreated", on_mobile))
        wnd.dock(fit=True, exact=True, verify=True, drawn_at=drawn_at)
        logs.update({"shutting": False, "queue": []})
        logw.dock(fit=True, min=log_min)
        say("on; sweep %s, visitors within %d tiles%s."
            % ("on" if st["sweep"] else "off", settings["range"], ", red or Foe alarm on" if settings["eject_foes"]
               else ""), Kit.HUE_GOOD)

    def _tick():
        """Module tick, on the client tick: act on queued actions, save, read the journal and run the work.

        Order: queued actions, delayed saves, log window redraws, then (once your mobile is known) new
        journal lines, a visitor scan with the foe alert, the house command, the sweep and a waiting
        house command, a lapsed ban confirmation and the status line.
        """
        if win["g"] is None:
            return
        # The window was closed by the player: stop here.
        if Kit.closed(win):
            return
        now = time.time()
        me = HOST.me()
        # Each queued action: the window's own buttons first, else this module's ACTIONS.
        while st["queue"]:
            action = st["queue"].pop(0)
            kind = action[0] if isinstance(action, tuple) else action
            if not wnd.action(action) and kind in ACTIONS:
                ACTIONS[kind](action, now, me)
        # Logs are saved at most once per LOG_SAVE_EVERY, the visits per VISIT_SAVE_EVERY.
        if st["log_dirty"] and now >= st["log_save_at"]:
            st["log_save_at"] = now + LOG_SAVE_EVERY
            save_log()
        if st["visits_dirty"] and now >= st["visits_save_at"]:
            st["visits_save_at"] = now + VISIT_SAVE_EVERY
            save_visits()
        if st["visits_redraw"]:
            st["visits_redraw"] = False
            refresh_logwin()
        if logs["queue"]:
            del logs["queue"][:]
            if Kit.zone_up(LOG_DOCK) or logs["g"] is not None:
                build_logwin()
        # No character yet: nothing below can run.
        if me is None:
            return
        for ln in st["rd"].new():
            on_journal(ln)
        if scan_visitors(now, me):
            eject_on_sight(now)
        house_tick(now)
        # The sweep and a held-back house command run only while no house command is running.
        if st["house"] is None:
            if st["sweep"] and st["phase"] == "idle" and (wait_left(now) <= HELD_EVERY or now >= st["held_at"]):
                st["held_at"] = now + HELD_EVERY
                # Why the sweep waits is looked at about twice a second; a change is logged once.
                held = sweep_held(now)
                if held != st["held"]:
                    was, st["held"] = st["held"], held
                    if held and not was:
                        add_log("sweep waits: %s" % (held[:1].lower() + held[1:]), Kit.HUE_INFO)
                if st["house_wait"] is None and not st["held"]:
                    start_sweep(now)
            sweep_tick(now)
            house_wait_tick(now)
        if st["confirm"] and now >= st["confirm"][1]:
            st["confirm"] = None
        refresh_status()

    def _stop():
        """Module stop: save everything unsaved, end any visit, release the cursor and close the windows."""
        st["shutting"] = logs["shutting"] = True
        st["house_wait"] = None
        HOST.release_cursor(KEY)
        save_settings()
        if st["log_dirty"]:
            save_log()
        if st["open_visits"]:
            close_visits(time.time())
        if st["visits_dirty"]:
            save_visits()
        cleanup.close()

    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
            "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed}


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("butler", "Property Butler", "House sweeps, visitors, eject and ban",
         _module_butler, 0.1, category="Skills and home")
