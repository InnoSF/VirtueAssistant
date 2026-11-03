# =============================================================================
#  Property Butler  -  a Virtue Assistant module (TazUO Legion Script, Python)
#  Shard: In Mani Ylem
#
#  This file is NOT a script to run on its own. It is one module of Virtue
#  Assistant, loaded by Virtue Assistant from LegionScripts/VirtueAssistantModules.
#  Virtue Assistant provides everything this file uses (API, G, safe, Client,
#  Kit, Follow, Journal, HOST, the main loop and the settings window), so run
#  that instead and tick Property Butler on its Modules tab.
#
#  To leave this module out, take this file out of the folder.
#  Module key: "butler"
#
#  2.6.82: speed pass: the sweep's holds every 0.5 s until the skill is
#  nearly ready (always fresh right before it is used), fewer client reads
#  and text cuts per tick (same actions, messages, saved values and window).
# =============================================================================


def _module_butler():
    """Builds the module in its own namespace and returns its hooks."""
    # =============================================================================
    #  MODULE: Property Butler  -  looks after your house while you stand in it
    #
    #  - Sweep: uses the Detect Hidden skill on your own spot every time the
    #    skill is off its cooldown, so anyone hiding on the property is revealed.
    #    Revealed people are called out over their head and counted.
    #  - Visitors: every player near you, with a Friend, an Eject and a Ban
    #    button on each row. The house commands are said out loud ("Remove
    #    thyself", "I ban thee", ...) and the cursor the house raises is aimed
    #    at that player.
    #  - Eject... / Ban... / Friend...: a target cursor to pick anyone by hand.
    #  - Lock down... / Release...: a target cursor for an item in the house.
    #  - A short log of what was done (kept per character); "Show log" opens a
    #    window with every kept line.
    #  - Visitor log (2.6.05): while you stand in a house, every player who
    #    steps into one within the visitor range is logged with the times they
    #    came in and left (kept per character, capped); the log window's
    #    Visitors view lists them.
    #  - Red or Foe alarm (a setting, off by default): while you stand in your
    #    house, a red player or one on Ultima Tracker's Foe list who steps in
    #    raises an alarm; the Eject button on their row ejects them, on your press.
    #  - Settings, DEBUG: "Print the shard's replies in the journal" repeats
    #    every journal line seen while a house command or a sweep waits for
    #    the shard, so the match lists on the settings page can be fixed to
    #    the shard's actual texts.
    #
    #  Only the house owner, co-owners and friends can eject and lock down;
    #  only the owner and co-owners can ban and release; only the owner adds
    #  friends; all of it only while standing in the house (the shard answers
    #  in the journal; the log shows what it said).
    # =============================================================================
    KEY = "butler"
    TITLE = "Property Butler"

    # ------------------------------- CONFIG --------------------------------------
    SETTINGS_KEY = "PropertyButler_settings"     # per character
    POS_KEY = "PropertyButler_pos"
    VIEW_KEY = "PropertyButler_view"             # sweep on/off, kept for the next start
    MIN_KEY = "PropertyButler_min"               # minimized when last seen (Kit.load_min / save_min)
    LOG_KEY = "PropertyButler_log"               # the last actions, kept per character
    LOG_POS_KEY = "PropertyButler_log_pos"       # where the "Show log" window sits
    W = 520                                      # full window width
    MINI_W, MINI_H = 300, 46                     # minimized bar ("Property Butler: sweep on, 2 near")
    TRAY_ICON = 0x0BD2                           # house sign art on the Action Bar's tray
    MAX_ROWS = 8                                 # visitor rows drawn (more are counted only)
    ROW_H = 22
    LOG_LINES = 3                                # log lines shown in the window
    LOG_KEEP = 30                                # log lines remembered
    LOG_W = 520                                  # the "Show log" window: width and line height
    LOG_ROW_H = 18
    LOG_SAVE_EVERY = 1.0                         # seconds: log lines are saved in one write per second
    NAME_CACHE_SECS = 2.5                        # a visitor's name / notoriety is re-read this often
    NAME_CACHE_MAX = 200                         # entries kept in that cache
    CLICK_GRACE = 0.15                           # seconds: a click right after a row changed acts on what was shown
    PICK_WAIT = 15.0                             # seconds a hand pick's target cursor stays up
    # 2.6.05: the visitor log and the red or Foe alarm. "In a house" means a house
    # tile under you (API.GetMultisAt: the client's houses; RunUO counts a
    # player as inside a house when one of its tiles is under them).
    VISITS_KEY = "PropertyButler_visits"         # the visitor log, kept per character
    LOG_VIEW_KEY = "PropertyButler_log_view"     # the log window's view: actions or visitors
    VISIT_KEEP = 30                              # visits remembered (the oldest dropped)
    VISIT_MERGE = 60.0                           # seconds: back in this soon after leaving = the same visit
    VISIT_SAVE_EVERY = 5.0                       # seconds: the visitor log is saved at most this often (and on stop)
    HOUSE_EVERY = 2.0                            # seconds between looks for a house under you while you stand still
    HOUSE_CHECKS = 6                             # visitors' tiles looked up per scan at most (only those who moved)
    EJECT_FOE_EVERY = 10.0                       # eject on sight: seconds between two tries on the same player
    EJECT_FOE_FAIL = 300.0                       # seconds a player is left alone after the house refused to eject them
    FOE_SERVICE = "ultima.is_foe"                # Ultima Tracker's Foe list: fn(serial, name) -> bool (optional)

    # Shard rules (In Mani Ylem, RunUO-style house speech). VERIFY IN GAME; both
    # phrases can be changed on the settings page without touching this file.
    DEFAULT_EJECT_CMD = "Remove thyself"         # house command: eject (owner, co-owner, friend)
    DEFAULT_BAN_CMD = "I ban thee"               # house command: ban (owner, co-owner)
    DEFAULT_FRIEND_CMD = "I wish to make this a friend"   # house command: add a friend (owner); on
    #                                              shards without a spoken form, use the house sign
    DEFAULT_LOCK_CMD = "I wish to lock this down"  # house command: lock down an item
    DEFAULT_RELEASE_CMD = "I wish to release this" # house command: release a locked-down item
    DETECT_SKILL = "Detect Hidden"               # API.UseSkill name (first skill containing it)
    DEFAULT_COOLDOWN = 10.0                      # seconds between skill uses (the shard's skill delay)
    COOLDOWN_MIN, COOLDOWN_MAX = 3.0, 120.0
    DEFAULT_RANGE = 12                           # tiles: visitors listed
    RANGE_MIN, RANGE_MAX = 1, 18
    CURSOR_WAIT = 3.0                            # seconds to wait for a cursor from the skill / house
    REPLY_WAIT = 3.0                             # seconds the shard's journal reply is waited for
    REVEAL_WINDOW = 1.0                          # someone appearing this soon after the aim was revealed by it
    RETRY_SOON = 1.5                             # seconds before trying again after "you must wait"
    CONFIRM_SECS = 3.0                           # second click on Ban within this long confirms it
    STILL_SECS = 1.0                             # "standing still" means not moved this long
    SCAN_EVERY = 0.3                             # seconds between visitor scans
    HELD_EVERY = 0.5                             # 2.6.82: s between looks at the sweep's holds while cooling down
    REVEAL_SOUND = 0x01F1                        # default sound of the "revealed" alert (Settings > Alerts)
    ALERT_REVEAL = "butler.revealed"             # alert kinds (2.6.5; Settings > Alerts: sound, on / off)
    ALERT_FOE = "butler.foe"                     # a red or Foe stepped into your house: Eject?
    ALERT_FOE_SOUND = 0x338                      # yell
    #  The sweep is a skill loop (Detect Hidden every cooldown by itself): under
    #  the shard's rules it waits while you are dead, under the town guards'
    #  protection (no macroing in guarded regions) or while that isn't known yet,
    #  in war mode, hurt, with a hostile near, moving an item, while an alarm of
    #  any module waits for you (HOST.alarm_up, the training alarm's attention.up)
    #  and while a house command runs. 2.6.81: one test with every other loop
    #  (HOST.fight_hold, HOST.guard_hold; the words are the mother's HOLD_TEXT).
    #  The wait reasons, in the order tested:
    HELD_DEAD = HOLD_TEXT["dead"]
    HELD_GUARD = HOLD_TEXT["guard"]
    HELD_UNKNOWN = HOLD_TEXT["unknown"]          # (2.6.81) shown as it is: a sentence of its own
    HELD_WAR = HOLD_TEXT["war"]
    HELD_HURT = HOLD_TEXT["hurt"]
    HELD_FOE = HOLD_TEXT["foe"]
    HELD_ITEM = HOLD_TEXT["item"]
    HELD_ALARM = HOLD_TEXT["alarm"]
    HELD_FIGHT = {"dead": HELD_DEAD, "war": HELD_WAR, "hurt": HELD_HURT, "foe": HELD_FOE,
                  "item": HELD_ITEM, "alarm": HELD_ALARM}   # HOST.fight_hold's reasons
    # Journal lines the shard sends (Cliloc.enu), lower case, matched with "in":
    J_WAIT = ("must wait a few moments to use another skill", "must wait to perform another action")
    J_NOTHING = ("you can see nothing hidden there",)
    J_REVEAL = ("reveal one other person", "reveal several people", "you carefully check the house")
    J_DONE = {"eject": ("has been ejected from this house",),
              "ban": ("has been banned from this house",),
              "friend": ("is now a friend of this house", "made a friend of this house"),
              "lock": ("locked down!",),
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
    # kind -> (settings key, what the log says, "mobile" or "item")
    CMDS = {"eject": ("eject_cmd", "ejected", "mobile"), "ban": ("ban_cmd", "banned", "mobile"),
            "friend": ("friend_cmd", "befriended", "mobile"), "lock": ("lock_cmd", "locked down", "item"),
            "release": ("release_cmd", "released", "item")}
    # kind -> the verb as the status line and the log say it ("Lock down Chest: waiting...")
    VERBS = {"eject": "Eject", "ban": "Ban", "friend": "Befriend", "lock": "Lock down", "release": "Release"}
    EMPTY_ROWS = "Nobody near you. Players within range appear here."     # the VISITORS list, empty
    EMPTY_LOG = "No actions yet: ejects, bans and reveals go here."       # the action log, empty
    EMPTY_VISITS = "No visits yet: players who step into your house go here."
    # -----------------------------------------------------------------------------

    settings = {"cooldown": DEFAULT_COOLDOWN, "range": DEFAULT_RANGE, "still": False,
                "sound": True, "friends": True, "confirm": True,
                "eject_cmd": DEFAULT_EJECT_CMD, "ban_cmd": DEFAULT_BAN_CMD,
                "friend_cmd": DEFAULT_FRIEND_CMD, "lock_cmd": DEFAULT_LOCK_CMD,
                "release_cmd": DEFAULT_RELEASE_CMD,
                "say_replies": False,       # debug: print every journal line seen while waiting for the shard
                "eject_foes": False}        # the red or Foe alarm (off by default; 2.6.05's key)
    st = {"shutting": False, "minimized": False, "docked": False, "queue": [],
          "sweep": False,                 # auto-sweep on
          "held": None,                   # 2.6.5: why the sweep waits (a HELD_* text), or None
          "phase": "idle",                # idle / cursor / cast  (the Detect Hidden flow)
          "next_at": 0.0,                 # when the skill may be used again
          "deadline": 0.0,                # give up waiting for its cursor
          "cast_at": 0.0,                 # when it was aimed (reveals are watched after it)
          "seen": set(),                  # mobiles in view when the sweep was aimed
          "sweeps": 0, "revealed": 0, "empty": 0,
          "house": None,                  # {"kind","serial","name","deadline","said"} while a house command runs
          "house_wait": None,             # a house command waiting for the sweep's cursor to pass
          "confirm": None,                # (serial, until) a Ban waiting for its second click
          "scan_at": 0.0, "visitors": [], "near": 0,
          "ncache": {},                   # serial -> (until, name, notoriety): re-read every NAME_CACHE_SECS
          "pos": None, "moved_at": 0.0,   # your tile and when it last changed
          "rd": None,                     # Journal reader
          "log_dirty": False, "log_save_at": 0.0,   # the log is saved once a second, not per line
          "status": None, "note": "", "note_until": 0.0,
          # 2.6.05: the visitor log and the red or Foe alarm
          "in_house": None,               # a house tile under you? (None: not known / can't tell)
          "house_pos": None, "house_at": 0.0,   # where that was looked up, and when to look again
          "inside": {},                   # serial -> (x, y, in a house?) for the visitors, looked up when they move
          "open_visits": {},              # serial -> its visit entry while that player is in the house
          "visits_dirty": False, "visits_save_at": 0.0,   # saved at most every VISIT_SAVE_EVERY s
          "visits_redraw": False,         # the log window's visitor view is redrawn at the end of the tick
          "eject_at": {},                 # serial -> no automatic eject of that player before this time
          "foe": {},                      # serial -> (until, on the Foe list?): Ultima Tracker's answer, cached
          "auto_no_rights": False,        # (2.6.06's eject on sight; kept so older saves' state keys still read)
          "no_multi_said": False}
    win = {"g": None, "c": {}, "rows": [], "store": ({}, {}),
           "log_g": None, "log_rows": [], "log_store": ({}, {}),   # the "Show log" window
           "log_view": "log"}             # what it shows: "log" (actions) or "visits" (2.6.05)
    page = {"c": None}
    log = []                              # [(time, text, hue)] newest last
    visits = []                           # [t_in, t_out (0: inside now / not known), serial, name,
    #                                       notoriety, times in, 1 ejected / 2 banned / 0] newest last
    NOTO_HUE = {"innocent": 90, "ally": 68, "gray": 946, "criminal": 946, "murderer": 33,
                "enemy": 43, "invulnerable": 53}
    NOTO_NAMES = {}
    OWN_PREFIX = TITLE.lower() + ":"      # this module's own journal lines (lower case)
    OWN_REPLY_PREFIX = TITLE.lower() + ": reply:"


    # ---------- saved settings ----------
    def load_settings():
        p = Kit.get_var(SETTINGS_KEY).split("|")
        if len(p) >= 8:
            try:
                settings["cooldown"] = max(COOLDOWN_MIN, min(COOLDOWN_MAX, float(p[0])))
            except Exception:
                pass
            try:
                settings["range"] = max(RANGE_MIN, min(RANGE_MAX, int(p[1])))
            except Exception:
                pass
            settings["still"] = p[2] == "1"
            settings["sound"] = p[3] == "1"
            settings["friends"] = p[4] == "1"
            settings["confirm"] = p[5] == "1"
            settings["eject_cmd"] = p[6] or DEFAULT_EJECT_CMD
            settings["ban_cmd"] = p[7] or DEFAULT_BAN_CMD
            p = p + [""] * (13 - len(p))              # saves from before the extra commands
            settings["friend_cmd"] = p[8] or DEFAULT_FRIEND_CMD
            settings["lock_cmd"] = p[9] or DEFAULT_LOCK_CMD
            settings["release_cmd"] = p[10] or DEFAULT_RELEASE_CMD
            settings["say_replies"] = p[11] == "1"    # 2.6.01 (missing in older saves: off)
            settings["eject_foes"] = p[12] == "1"     # 2.6.05 (missing in older saves: off)
        st["sweep"] = Kit.get_var(VIEW_KEY) == "1"
        del log[:]
        for line in Kit.get_var(LOG_KEY).split("\n"):
            q = line.split("\t")
            if len(q) >= 3:
                try:
                    log.append((float(q[0]), q[2], int(q[1])))
                except Exception:
                    pass
        del log[:-LOG_KEEP]
        # 2.6.05: the visitor log ("t_in, t_out, serial, notoriety, times, flag, name" per line)
        del visits[:]
        for line in Kit.get_var(VISITS_KEY).split("\n"):
            q = line.split("\t", 6)
            if len(q) >= 7:
                try:
                    visits.append([float(q[0]), float(q[1]), int(q[2]), q[6], q[3] or "unknown",
                                   max(1, int(q[4])), int(q[5])])
                except Exception:
                    pass
        del visits[:-VISIT_KEEP]
        win["log_view"] = "visits" if Kit.get_var(LOG_VIEW_KEY) == "visits" else "log"


    def save_settings():
        data = "|".join(["%.1f" % settings["cooldown"], str(settings["range"]),
                         "1" if settings["still"] else "0", "1" if settings["sound"] else "0",
                         "1" if settings["friends"] else "0", "1" if settings["confirm"] else "0",
                         settings["eject_cmd"].replace("|", "/"), settings["ban_cmd"].replace("|", "/"),
                         settings["friend_cmd"].replace("|", "/"), settings["lock_cmd"].replace("|", "/"),
                         settings["release_cmd"].replace("|", "/"),
                         "1" if settings["say_replies"] else "0",
                         "1" if settings["eject_foes"] else "0"])     # 2.6.05: a 13th field
        Kit.put_var(SETTINGS_KEY, data)
        Kit.put_var(VIEW_KEY, "1" if st["sweep"] else "0")


    def save_log():
        st["log_dirty"] = False
        Kit.put_var(LOG_KEY, "\n".join(["%d\t%d\t%s" % (t, hue, text.replace("\t", " ").replace("\n", " "))
                                         for (t, text, hue) in log[-LOG_KEEP:]]))


    def save_log_soon():
        """Marks the log for saving: the tick writes it at most once a second
        (a reveal burst used to write the per-character var several times in
        one tick, on the client thread)."""
        st["log_dirty"] = True


    def save_visits():
        st["visits_dirty"] = False
        Kit.put_var(VISITS_KEY, "\n".join(["%d\t%d\t%d\t%s\t%d\t%d\t%s" % (
            e[0], e[1], e[2], str(e[4]).replace("\t", " "), e[5], e[6],
            str(e[3]).replace("\t", " ").replace("\n", " ")) for e in visits[-VISIT_KEEP:]]))


    def visits_changed():
        """A visit opened, closed or was marked: saved within VISIT_SAVE_EVERY
        seconds, and the log window's visitor view redrawn once on the next
        tick when it shows them (a burst of changes in one scan is one redraw)."""
        st["visits_dirty"] = True
        if win["log_view"] == "visits" and win["log_g"] is not None:
            st["visits_redraw"] = True


    def add_log(text, hue=None):
        """A log line (kept bare: "ejected Bob") and the same in the journal,
        as "<Title>: ejected Bob." (the journal form ends with a full stop)."""
        log.append((time.time(), text, Kit.HUE_INFO if hue is None else hue))
        del log[:-LOG_KEEP]
        save_log_soon()
        API.SysMsg("%s: %s%s" % (TITLE, text, "" if text.endswith((".", "!", "?")) else "."),
                   Kit.HUE_INFO if hue is None else hue)
        refresh_log()


    def note(text, secs=4.0):
        """A short status line under the sweep row."""
        st["note"], st["note_until"] = text, time.time() + secs


    # ---------- small helpers ----------
    def noto_name(mob):
        try:
            v = mob.Notoriety
        except Exception:
            return "unknown"
        try:
            return NOTO_NAMES[v]
        except KeyError:
            pass
        except Exception:
            return str(v).split(".")[-1].lower()
        n = NOTO_NAMES[v] = str(v).split(".")[-1].lower()
        return n


    def has_target(kind="any"):
        """Is a target cursor (of kind: "any", "neutral", ...) up? (a plain try:
        this runs every tick while something waits)"""
        try:
            return bool(API.HasTarget(kind))
        except Exception:
            return False


    def cursor_free():
        """No cursor up and nobody else has one spoken for."""
        if HOST.cursor_busy(KEY) is not None:        # cannot raise: called plainly
            return False
        return not has_target()


    def short(name, width):
        """name cut to fit width px (Kit.fit: letter widths, no label per letter cut)."""
        return Kit.fit(name or "(unknown)", width)


    # ---------- window ----------
    queue = Kit.queuer(st)
    on_disposed = Kit.disposer(KEY, st, win)

    SWEEP_H = 82
    NAME_W = 150                                 # px a visitor's name may take
    LOG_PITCH = 20                               # (2.6.78) px between log lines (ui-text: 20 at least)
    VIS_H = 30 + MAX_ROWS * ROW_H + 8
    ACT_H = 30 + 26 + 26 + LOG_LINES * LOG_PITCH + 8   # two rows of buttons, then the log
    H = Kit.MARGIN + 30 + Kit.GAP + SWEEP_H + Kit.GAP + VIS_H + Kit.GAP + ACT_H + Kit.MARGIN
    MIN_ROWS = 2                                 # (2.6.78) visitor rows kept in a short zone
    NAME_MIN = 60                                # a visitor's name gets at least this much on its line
    def row_click(row):
        """Click on a visitor row: Alt+click follows (standing rule), a plain
        click sets Last Target. The row is pooled, so the serial is read now;
        a click within 0.15 s of the row changing acts on what was shown."""
        def handler(*args):
            serial, name = row["serial"], row["name"]
            if time.time() - row["changed"] < CLICK_GRACE and row["prev"]:
                serial, name = row["prev"]
            if not serial:
                return
            if Follow.alt_held():
                queue(("follow", serial))()
                return
            queue(("last", serial, name))()
        return handler


    def row_action(row, kind):
        def handler(*args):
            serial, name = row["serial"], row["name"]
            if time.time() - row["changed"] < CLICK_GRACE and row["prev"]:
                serial, name = row["prev"]
            if serial:
                if Follow.alt_held():                    # Alt+click: auto-follow (standing rule)
                    queue(("follow", serial))()
                    return
                queue((kind, serial, name))()
        return handler


    def save_pos():
        Kit.save_pos(POS_KEY, win["g"])


    fit = {"slot": None, "k": 1.0, "full": None}   # (2.6.78) the zone's slot, and the scale drawn at

    def layout_fit(w, h, mode):
        """(2.6.78) The layout's "fit" hook: the window's slot in a zone is w x h
        (None: freed). Client thread, the keeper's pass: records and asks for a
        rebuild; mode "again" draws it again even for a size it was told."""
        new = (int(w), int(h)) if (w is not None and h is not None) else None
        if new != fit["slot"] or (mode == "again" and new is not None):
            fit["slot"] = new
            queue("redraw")()

    def drawn_at():
        return fit["k"], fit["full"]

    def at_k(ctrl, x, y):
        """A control moved after the window was built, in the layout's pixels: at
        the window's scale when it is drawn smaller (2.6.78)."""
        k = fit["k"]
        if k != 1.0:
            ctrl.SetPos(int(round(x * k)), int(round(y * k)))
        else:
            Kit.ui_pos(ctrl, x, y)

    def cap_w(text):
        return 35 + Kit.text_w(text)

    # the action buttons, in two groups (each starts its own row; a group wraps
    # when the width needs): (key, art, caption, tooltip, queue)
    ACTIONS = ((("pick_ej", Kit.ART_PLAY, "Eject...", "Target a player to eject from the house",
                 "pick_eject"),
                ("pick_ban", Kit.ART_CLOSE, "Ban...", "Target a player to ban from the house",
                 "pick_ban"),
                ("pick_fr", Kit.ART_OK, "Friend...", "Target a player to make a friend of the house",
                 "pick_friend")),
               (("pick_lock", Kit.ART_OK, "Lock down...", "Target an item in the house to lock down",
                 "pick_lock"),
                ("pick_rel", Kit.ART_CLOSE, "Release...", "Target a locked-down item to release it",
                 "pick_release"),
                ("clear", Kit.ART_CLOSE, "Clear log",
                 "Forget the actions listed below (the visitor log stays)", "clear_log"),
                ("showlog", Kit.ART_PAGE, "Show log",
                 "Open the log window: the last %d actions and the visitor log (again to close it)"
                 % LOG_KEEP, "show_log")))

    def flow(items, x0, right):
        """[(x, row)] of captioned buttons laid out left to right from x0, 16 px
        apart, wrapping before right (each at least on a row of its own)."""
        out, x, row = [], x0, 0
        for cap in items:
            w = cap_w(cap)
            if x > x0 and x + w > right:
                x, row = x0, row + 1
            out.append((x, row))
            x += w + 16
        return out

    def btn_line_w():
        return cap_w("Friend") + 12 + cap_w("Eject") + 12 + cap_w("Ban")

    def min_w():
        """(2.6.78) The narrowest width laid out: a visitor's name line, with its
        three captioned buttons on the line under it."""
        return 2 * Kit.MARGIN + 12 + max(btn_line_w(), NAME_MIN + 6 + Kit.text_w("18 tiles")) + 10

    def layout(w, h):
        """(2.6.78) Every place of the full window for w x h (h None: its own
        height at w). Returns the plan; its "h" is the height it comes out."""
        M = Kit.MARGIN
        IW = w - 2 * M
        P = {"w": w, "IW": IW}
        ys = M + 30 + Kit.GAP
        P["ys"] = ys
        # SWEEP: Sweep: off / Sweep now on one row when both fit, else two; then the status
        sw_w = max(cap_w("Sweep: off"), cap_w("Sweep: on"))
        one = 10 + sw_w + 16 + cap_w("Sweep now") <= IW - 4
        P["sweep_xy"] = (M + 10, ys + 26)
        P["now_xy"] = (M + 10 + sw_w + 16, ys + 26) if one else (M + 10, ys + 52)
        st_y = ys + 58 if one else ys + 84
        P["status_y"] = st_y
        sweep_h = SWEEP_H if one else SWEEP_H + 26
        P["sweep_h"] = sweep_h
        cnt_w = Kit.text_w("999 sweeps, 999 revealed")
        P["count_room"] = min(cnt_w, max(40, IW - 20 - 80))
        P["status_room"] = max(40, IW - 20 - P["count_room"] - 10)
        # VISITORS: rows on one line when the row holds them, else two
        yv = ys + sweep_h + Kit.GAP
        P["yv"] = yv
        dist_w = Kit.text_w("18 tiles")
        single = 12 + NAME_MIN + 6 + dist_w + 10 + btn_line_w() + 10 <= IW
        P["single"] = single
        row_h = ROW_H if single else 2 * ROW_H
        P["row_h"] = row_h
        if single:
            x_ban = M + IW - 10 - cap_w("Ban")
            x_ej = x_ban - 12 - cap_w("Eject")
            x_fr = x_ej - 12 - cap_w("Friend")
            x_dist = x_fr - 10 - dist_w
            P["btn_dy"] = 0
        else:
            x_fr = M + 12
            x_ej = x_fr + cap_w("Friend") + 12
            x_ban = x_ej + cap_w("Eject") + 12
            x_dist = M + IW - 10 - dist_w
            P["btn_dy"] = ROW_H
        P["x"] = (x_fr, x_ej, x_ban, x_dist)
        P["name_w"] = max(20, min(NAME_W, x_dist - 6 - (M + 12)))
        P["empty"] = Kit.wrap(EMPTY_ROWS, max(60, IW - 24))
        # ACTIONS: the two groups flowed, then the log
        right = M + IW - 4
        groups = []
        rows_used = 0
        for grp in ACTIONS:
            fl = flow([b[2] for b in grp], M + 10, right)
            groups.append([(x, rows_used + r) for x, r in fl])
            rows_used += fl[-1][1] + 1
        P["act_rows"] = rows_used
        P["groups"] = groups
        # heights: the visitors and the log share what is left
        fixed = M + 30 + Kit.GAP + sweep_h + Kit.GAP + 30 + 8 + Kit.GAP + 30 + 26 * rows_used + 8 + M
        vis_hint = 30 + 8
        if h is None:
            rows_n, log_n = MAX_ROWS, LOG_LINES
        else:
            room = h - fixed
            log_n, rows_n = LOG_LINES, MAX_ROWS
            while log_n > 1 and rows_n * row_h + log_n * LOG_PITCH > room:
                log_n -= 1                       # the log gives way first ...
            while rows_n > MIN_ROWS and rows_n * row_h + log_n * LOG_PITCH > room:
                rows_n -= 1                      # ... then the visitors, to MIN_ROWS
            while rows_n == MAX_ROWS and log_n < LOG_KEEP and \
                    rows_n * row_h + (log_n + 1) * LOG_PITCH <= room:
                log_n += 1                       # spare room (every row shown): more of the log
        P["rows_n"], P["log_n"] = rows_n, log_n
        vis_h = vis_hint - 8 + rows_n * row_h + 8
        act_h = 30 + 26 * rows_used + log_n * LOG_PITCH + 8
        nat = fixed - (30 + 8) - (30 + 26 * rows_used + 8) + vis_h + act_h
        if h is not None and h > nat:
            vis_h += h - nat                     # what is left over: the visitors' section
        P["vis_h"], P["act_h"] = vis_h, act_h
        P["ya"] = yv + vis_h + Kit.GAP
        P["h"] = P["ya"] + act_h + M
        return P

    def section_title(title, hint, room):
        """'TITLE  (hint)', or the title alone when the two don't fit room px."""
        full = "%s  (%s)" % (title, hint)
        return full if Kit.text_w(full) <= room else title

    def build_window():
        slot = fit["slot"]
        if st["minimized"]:
            w, h = (max(MINI_W, slot[0]) if slot else MINI_W), MINI_H
        elif slot is None:
            w, h = W, H
        else:
            w, h = slot
        x, y = Kit.load_pos(POS_KEY, (200, 200), (w, h))
        if Kit.is_open(win["g"]):
            x, y = win["g"].GetX(), win["g"].GetY()
        old, win["g"] = win["g"], None
        M = Kit.MARGIN
        store = ({}, {})
        c = {}
        rows = []
        g = G.CreateGump(True, True)
        k = 1.0
        fit["k"], fit["full"] = 1.0, None
        if st["minimized"]:
            c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
            c["mini_w"] = w
        else:
            lw, lh, body = w, h, None
            if slot is None:
                P = layout(lw, None)
                lh = P["h"]
            elif w < min_w():
                # (2.6.78) too narrow: laid out at its narrowest and drawn smaller; a
                # zone too short for that too is drawn smaller still (laid out wider)
                k = w / float(min_w())
                P = layout(min_w(), int(h / k))
                if P["h"] > int(h / k) + 1:
                    k = min(k, h / float(P["h"]))
                lw, lh = int(round(w / k)), int(round(h / k))
                P = layout(lw, lh)
            else:
                P = layout(lw, lh)
                if P["h"] > lh + 1:              # too short at the fewest rows: its body scrolls
                    lw = w - Kit.SCROLL_BAND
                    P = layout(lw, lh)
                    body = P["h"]
            win["P"] = P
            IW = P["IW"]
            Kit.add_window_frame(g, lw, lh)
            Kit.title_bar(g, store, lw, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                          queue("settings"))
            # ---- SWEEP ----
            ys = P["ys"]
            Kit.add_section(g, M, ys, IW, P["sweep_h"],
                            section_title("SWEEP", "Detect Hidden on your own spot", IW - 12))
            c["sweep_lbl"] = Kit.art_button(g, store, "sweep", Kit.ART_PAGE, P["sweep_xy"][0],
                                            P["sweep_xy"][1], "Sweep: off",
                                            "Click to switch the automatic sweep on or off; on, Detect Hidden "
                                            "is used on your spot whenever it is ready",
                                            on_click=queue("sweep"))
            Kit.art_button(g, store, "now", Kit.ART_PLAY, P["now_xy"][0], P["now_xy"][1], "Sweep now",
                           "Use Detect Hidden once now, if the skill is ready",
                           on_click=queue("now"))
            c["status"] = Kit.add_label(g, "", M + 10, P["status_y"], Kit.HUE_INFO)
            c["count"] = Kit.add_label(g, "", M + IW - 10, P["status_y"], Kit.HUE_INFO)
            c["count_y"] = P["status_y"]         # (2.6.78) its own y: never read back (3e)
            # ---- VISITORS ----
            yv = P["yv"]
            near_w = Kit.text_w("99 near (%d shown)" % MAX_ROWS)
            Kit.add_section(g, M, yv, IW, P["vis_h"],
                            section_title("VISITORS", "players near you", IW - 12 - near_w - 16))
            c["near"] = Kit.add_label(g, "", M + IW - 10, yv + 6, Kit.HUE_INFO)
            c["near_y"] = yv + 6
            x_fr, x_ej, x_ban, x_dist = P["x"]
            dist_w = Kit.text_w("18 tiles")
            c["name_w"] = P["name_w"]            # a name stops short of the distance
            c["hidden_w"] = Kit.text_w(" (hidden)")
            ban_tip = ("Say the house's ban command and aim it at them%s. Alt+click: auto-follow (again to stop)"
                       % ("; a second click within %d s confirms" % int(CONFIRM_SECS) if settings["confirm"] else ""))
            row_h, bdy = P["row_h"], P["btn_dy"]
            for i in range(P["rows_n"]):
                ry = yv + 30 + i * row_h
                row = {"serial": 0, "name": "", "prev": None, "changed": 0.0, "vis": True,
                       "hue": None, "dist": None}
                row["name_lbl"] = Kit.add_label(g, "", M + 12, ry + 3, Kit.HUE_TEXT)
                row["dist_lbl"] = Kit.add_label(g, "", x_dist, ry + 3, Kit.HUE_INFO)
                row["catch"] = Kit.catcher(g, M + 10, ry, x_dist - M - 10 + dist_w, ROW_H,
                                           row_click(row),
                                           "Set them as your last target. Alt+click: auto-follow (again to stop)")
                row["fr"] = Kit.art_button(g, store, "fr%d" % i, Kit.ART_OK, x_fr, ry + bdy, "Friend",
                                           "Say the house's friend command and aim it at them. "
                                           "Alt+click: auto-follow (again to stop)",
                                           on_click=row_action(row, "friend"))
                row["fr_btn"] = store[0]["fr%d" % i]
                row["ej"] = Kit.art_button(g, store, "ej%d" % i, Kit.ART_PLAY, x_ej, ry + bdy, "Eject",
                                           "Say the house's eject command and aim it at them. "
                                           "Alt+click: auto-follow (again to stop)",
                                           on_click=row_action(row, "eject"))
                row["ej_btn"] = store[0]["ej%d" % i]
                row["ban"] = Kit.art_button(g, store, "ban%d" % i, Kit.ART_CLOSE, x_ban, ry + bdy, "Ban",
                                            ban_tip, on_click=row_action(row, "ban"))
                row["ban_btn"] = store[0]["ban%d" % i]
                rows.append(row)
            c["empty"] = []                      # the empty-state sentence, wrapped
            for i, line in enumerate(P["empty"][:max(1, (P["vis_h"] - 33) // 20)]):
                c["empty"].append(Kit.add_label(g, line, M + 12, yv + 33 + 20 * i, Kit.HUE_INFO))
            # ---- ACTIONS / LOG ----
            ya = P["ya"]
            Kit.add_section(g, M, ya, IW, P["act_h"],
                            section_title("ACTIONS", "pick with a target cursor", IW - 12))
            for grp, places in zip(ACTIONS, P["groups"]):
                for (key, art, cap, tip, act_), (bx, brow) in zip(grp, places):
                    Kit.art_button(g, store, key, art, bx, ya + 26 + 26 * brow, cap, tip,
                                   on_click=queue(act_))
            c["log"] = []
            ly = ya + 30 + 26 * P["act_rows"]
            for i in range(P["log_n"]):
                c["log"].append(Kit.add_label(g, "", M + 12, ly + i * LOG_PITCH, Kit.HUE_INFO))
            c["log_w"] = IW - 70
            c["log_full"] = IW - 24
            if k != 1.0:
                fit["k"], fit["full"] = k, (int(min_w()), int(round(layout(min_w(), None)["h"])))
                Kit.scale_window(g, k)           # the whole window drawn smaller
            elif body is not None:
                w, h = lw, body                  # (Kit.place: slot-high, scrolling, band added)
            else:
                w, h = lw, lh
        Kit.place(g, x, y, w, h, None, slot[1] if (slot is not None and not st["minimized"]) else None)
        if safe(lambda: HOST.layout_locked(KEY), False):
            safe(lambda: setattr(g, "CanMove", False))   # held in its zone
        win.update({"g": g, "c": c, "rows": rows, "store": store})
        G.AddControlOnDisposed(g, on_disposed(g))
        G.AddGump(g)
        safe(lambda: Kit.on_moved(g, save_pos))      # saved the moment you let go of it
        if st["minimized"] and st["docked"]:
            safe(lambda: setattr(g, "IsVisible", False))
        st["status"] = None
        refresh_log()
        refresh_rows(True)
        refresh_status()
        Kit.dispose(old)


    EMPTY_ROWS_L = (EMPTY_ROWS,)                 # 2.6.82: one object (refresh_rows' change test)
    ROW_CTRLS = ("name_lbl", "dist_lbl", "catch", "fr", "fr_btn", "ej", "ej_btn", "ban", "ban_btn")


    def set_vis(ctrl, on, row, key):
        if row.get(key + "_vis") != on:
            row[key + "_vis"] = on
            try:
                ctrl.IsVisible = on
            except Exception:
                pass


    def refresh_rows(force=False):
        rows = win["rows"]
        if not rows or (st["minimized"] and not force):
            return
        c = win["c"]
        vis = st["visitors"]
        now = time.time()
        name_w, hidden_w = c.get("name_w", NAME_W), c.get("hidden_w", 0)
        for i, row in enumerate(rows):
            if i < len(vis):
                v = vis[i]
                if v["serial"] != row["serial"]:
                    row["prev"] = (row["serial"], row["name"]) if row["serial"] else None
                    row["changed"] = now
                    row["serial"], row["name"] = v["serial"], v["name"]
                sig = (v["serial"], v["name"], v["noto"], v["hidden"], v["dist"], name_w, hidden_w)
                if row.get("sig") == sig:                 # 2.6.82: the row shows this already
                    continue
                row["sig"] = sig
                hue = NOTO_HUE.get(v["noto"], Kit.HUE_TEXT)
                if v["hidden"]:       # the name gives way to its " (hidden)" tag: the row stays inside its column
                    hue = Kit.HUE_TITLE
                    Kit.set_text(row["name_lbl"], short(v["name"], name_w - hidden_w) + " (hidden)", hue)
                else:
                    Kit.set_text(row["name_lbl"], short(v["name"], name_w), hue)
                Kit.set_text(row["dist_lbl"], "%d tile%s" % (v["dist"], "" if v["dist"] == 1 else "s"))
                for k in ROW_CTRLS:
                    set_vis(row[k], True, row, k)
            else:
                if row["serial"]:
                    row["prev"], row["changed"] = (row["serial"], row["name"]), now
                    row["serial"], row["name"] = 0, ""
                row["sig"] = None
                for k in ROW_CTRLS:
                    set_vis(row[k], False, row, k)
        lines = (win.get("P") or {}).get("empty") or EMPTY_ROWS_L
        ek = c.get("empty_k")                             # 2.6.82: set only when it changes
        if ek is None or ek[0] != (not vis) or ek[1] is not lines:
            c["empty_k"] = (not vis, lines)
            for i, lbl in enumerate(c.get("empty") or ()):    # (2.6.78) the sentence, wrapped
                Kit.set_text(lbl, lines[i] if (not vis and i < len(lines)) else "")
        near = c.get("near")
        nk = (st["near"], len(vis) > len(rows), len(rows))
        if near is not None and c.get("near_k") != nk:    # 2.6.82: only when its numbers change
            c["near_k"] = nk
            txt = "%d near" % st["near"] if st["near"] else ""
            if len(vis) > len(rows):
                txt = "%d near (%d shown)" % (st["near"], len(rows))
            Kit.set_text(near, txt)
            # right-aligned at its own y (2.6.78: never read back): moved when its width changes
            tw = Kit.text_w(txt)
            if c.get("near_w") != tw:
                c["near_w"] = tw
                IW = (win.get("P") or {}).get("IW", W - 2 * Kit.MARGIN)
                safe(lambda: at_k(near, Kit.MARGIN + IW - 10 - tw, c["near_y"]))


    def log_line(entry, width):
        t, text, hue = entry
        return "%s  %s" % (time.strftime("%H:%M", time.localtime(t)), short(text, width)), hue


    def refresh_log():
        c = win["c"]
        lbls = c.get("log")
        if lbls:
            tail = log[-len(lbls):]
            for i, lbl in enumerate(lbls):
                if i < len(tail):
                    text, hue = log_line(tail[len(tail) - 1 - i], c.get("log_w", W - 2 * Kit.MARGIN - 70))
                    Kit.set_text(lbl, text, hue)
                elif i == 0:                              # empty state: the first line says so
                    Kit.set_text(lbl, Kit.fit(EMPTY_LOG, c.get("log_full", 480)), Kit.HUE_INFO)
                else:
                    Kit.set_text(lbl, "")
        refresh_logwin()


    # ---------- the "Show log" window: every kept line, newest first ----------
    #  2.6.05: two views, switched from its title row: the action log, and the
    #  visitor log (players who came into the house while you were in it).
    def save_log_pos():
        Kit.save_pos(LOG_POS_KEY, win["log_g"])


    def on_log_disposed(g):
        def handler(*args):
            if win["log_g"] is g:
                win["log_g"], win["log_rows"] = None, []
        return handler


    def visit_click(row):
        """Click on a visitor-log row: Alt+click follows that player (standing
        rule), a plain click sets Last Target, like the VISITORS rows. A click
        within 0.15 s of the row changing acts on what was shown."""
        def handler(*args):
            serial, name = row["serial"], row["name"]
            if time.time() - row["changed"] < CLICK_GRACE and row["prev"]:
                serial, name = row["prev"]
            if not serial:
                return
            if Follow.alt_held():
                queue(("follow", serial))()
                return
            queue(("last", serial, name))()
        return handler


    def build_logwin():
        """Built with a row per kept line of the view shown (at least
        LOG_LINES), newest first; refresh_logwin rewrites the rows and rebuilds
        only when lines were added."""
        M = Kit.MARGIN
        visits_view = win["log_view"] == "visits"
        if visits_view:              # rows in steps of 10: at most two rebuilds on the way to VISIT_KEEP
            n = min(VISIT_KEEP, max(10, (len(visits) + 9) // 10 * 10))
        else:
            n = max(LOG_LINES, len(log))
        sh = 30 + n * LOG_ROW_H + 8
        w, h = LOG_W, M + 30 + Kit.GAP + sh + M
        x, y = Kit.load_pos(LOG_POS_KEY, (240, 240), (w, h))       # saved place, on today's screen
        old = win["log_g"]
        if Kit.is_open(old):
            x, y = old.GetX(), old.GetY()
        win["log_g"] = None
        store = ({}, {})
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, w, h)
        Kit.add_section(g, M, M, w - 2 * M, 30)
        Kit.add_label(g, "%s LOG" % TITLE.upper(), M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, "Close",
                       on_click=queue("show_log"))
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
        Kit.add_section(g, M, ys, w - 2 * M, sh,
                        "VISITORS  (while you stood in the house)" if visits_view
                        else "ACTIONS  (newest first; %d are kept)" % LOG_KEEP)
        rows = []
        for i in range(n):
            ry = ys + 30 + i * LOG_ROW_H
            row = {"lbl": Kit.add_label(g, "", M + 12, ry, Kit.HUE_INFO), "catch": None,
                   "serial": 0, "name": "", "prev": None, "changed": 0.0}
            if visits_view:                                   # a past visitor: Alt+click follows
                row["catch"] = Kit.catcher(g, M + 10, ry - 1, w - 2 * M - 20, LOG_ROW_H, visit_click(row),
                                           "Set them as your last target. Alt+click: auto-follow (again to stop)")
            rows.append(row)
        Kit.place(g, x, y, w, h)                              # wholly on screen (the window rules)
        win.update({"log_g": g, "log_rows": rows, "log_store": store})
        G.AddControlOnDisposed(g, on_log_disposed(g))
        G.AddGump(g)
        safe(lambda: Kit.on_moved(g, save_log_pos))           # saved the moment you let go of it
        refresh_logwin()
        Kit.dispose(old)


    def visit_line(e, width, now):
        """A visit as one line: when, who (notoriety), how often, ejected."""
        t_in, t_out, serial, name, noto, times, flag = e
        lt = time.localtime(t_in)
        when = time.strftime("%H:%M" if lt[:3] == time.localtime(now)[:3] else "%b %d %H:%M", lt)
        if st["open_visits"].get(serial) is e:
            when += ", inside now"
        elif t_out:
            when += "-" + time.strftime("%H:%M", time.localtime(t_out))
        else:
            when += "-?"                                      # the module stopped while they were in
        tail = " (%s)" % noto
        if times > 1:
            tail += "  in %d times" % times
        if flag:
            tail += "  banned" if flag == 2 else "  ejected"
        name_w = max(60, width - Kit.text_px(when + "  " + tail))
        return "%s  %s%s" % (when, short(name, name_w), tail), NOTO_HUE.get(noto, Kit.HUE_TEXT)


    def refresh_logwin():
        g = win["log_g"]
        if not Kit.is_open(g):
            return
        rows = win["log_rows"]
        visits_view = win["log_view"] == "visits"
        lines = visits if visits_view else log
        if len(lines) > len(rows):                            # more lines than rows: rebuild
            build_logwin()
            return
        n = len(lines)
        now = time.time()
        for i, row in enumerate(rows):
            if i < n:
                e = lines[n - 1 - i]
                if visits_view:
                    key = (e[0], e[2], e[1], e[5], e[6], st["open_visits"].get(e[2]) is e)
                    if row.get("key") != key:                 # only a visit that changed is redrawn
                        row["key"] = key
                        text, hue = visit_line(e, LOG_W - 2 * Kit.MARGIN - 28, now)
                        Kit.set_text(row["lbl"], text, hue)
                    if e[2] != row["serial"]:                 # the row moves to another visitor
                        row["prev"] = (row["serial"], row["name"]) if row["serial"] else None
                        row["changed"] = now
                        row["serial"], row["name"] = e[2], e[3]
                else:
                    text, hue = log_line(e, LOG_W - 2 * Kit.MARGIN - 70)
                    Kit.set_text(row["lbl"], text, hue)
            else:
                if i == 0:                                    # empty state: the first row says so
                    Kit.set_text(row["lbl"], EMPTY_VISITS if visits_view else EMPTY_LOG, Kit.HUE_INFO)
                else:
                    Kit.set_text(row["lbl"], "")
                row["key"] = None
                if row["serial"]:
                    row["prev"], row["changed"] = (row["serial"], row["name"]), now
                    row["serial"], row["name"] = 0, ""
            if row["catch"] is not None:
                set_vis(row["catch"], i < n, row, "catch")


    def toggle_logwin():
        if Kit.is_open(win["log_g"]):
            save_log_pos()
            g, win["log_g"] = win["log_g"], None
            win["log_rows"] = []
            Kit.dispose(g)
        else:
            build_logwin()


    def status_text(now):
        if st["house"] is not None:
            h = st["house"]
            return ("%s %s%s: waiting for the house's cursor" % (VERBS[h["kind"]], h["name"] or "the target",
                                                                 " on sight" if h.get("auto") else ""),
                    Kit.HUE_TITLE)
        hw = st["house_wait"]
        if hw is not None:
            return ("%s %s: waiting for the sweep's cursor to pass" % (VERBS[hw["kind"]],
                                                                       hw["name"] or "the target"),
                    Kit.HUE_TITLE)
        if st["note"] and now < st["note_until"]:
            return st["note"], Kit.HUE_INFO
        if st["phase"] == "cursor":
            return "Detect Hidden: waiting for its cursor", Kit.HUE_TITLE
        if st["phase"] == "cast":
            return "Detect Hidden: sweeping", Kit.HUE_GOOD
        if not st["sweep"]:
            rem = st["next_at"] - now
            if rem > 0:
                return "Sweep off; Detect Hidden ready in %d s" % int(rem + 0.99), Kit.HUE_INFO
            return "Sweep off; Detect Hidden ready", Kit.HUE_INFO
        if st["held"] == HELD_UNKNOWN:           # 2.6.81: a sentence of its own
            return HELD_UNKNOWN, Kit.HUE_INFO
        if st["held"]:
            return "Sweep on, waiting: %s" % st["held"], Kit.HUE_INFO
        rem = st["next_at"] - now
        if rem > 0:
            return "Sweep on: next in %d s" % int(rem + 0.99), Kit.HUE_GOOD
        if settings["still"] and now - st["moved_at"] < STILL_SECS:
            return "Sweep on: waiting until you stand still", Kit.HUE_INFO
        return "Sweep on: ready", Kit.HUE_GOOD


    def mini_text():
        """The minimized bar: "<Title>: sweep on, 2 near" (what the sweep is
        doing, then who is near)."""
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
        """2.6.82: short(text, room), cut again only when text or room changed
        (one entry per label, kept in the window's controls)."""
        e = c.get(key)
        if e is not None and e[0] == text and e[1] == room:
            return e[2]
        cut = short(text, room)
        c[key] = (text, room, cut)
        return cut


    def refresh_status():
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
            # cut to its part of the row: the sweep count sits at the right (a long
            # player name in "Eject <name>: waiting..." used to run under it)
            cut = cut_once(c, "status_k", text, P.get("status_room", W - 2 * Kit.MARGIN - 160))
            if Kit.set_text(lbl, cut, hue):
                safe(lambda: lbl.SetTooltip(text if cut != text else ""))   # (its whole text)
        sl = c.get("sweep_lbl")
        if sl is not None:
            Kit.set_text(sl, "Sweep: on" if st["sweep"] else "Sweep: off",
                         Kit.HUE_GOOD if st["sweep"] else Kit.HUE_TEXT)
        cnt = c.get("count")
        ck = (st["sweeps"], st["revealed"], P.get("count_room", 400))
        if cnt is not None and c.get("count_k") != ck:   # 2.6.82: only when a number changed
            c["count_k"] = ck
            txt = "%d sweep%s, %d revealed" % (st["sweeps"], "" if st["sweeps"] == 1 else "s", st["revealed"])
            txt = Kit.fit(txt, P.get("count_room", 400))     # (2.6.78) cut last
            if Kit.set_text(cnt, txt) or c.get("count_w") is None:
                tw = Kit.text_w(txt)
                if c.get("count_w") != tw:
                    c["count_w"] = tw
                    IW = P.get("IW", W - 2 * Kit.MARGIN)
                    # right-aligned at its own y: (2.6.78) Kit.ui_y read Y back before the
                    # queued SetPos had landed (0) and put it on the stone above the row
                    safe(lambda: at_k(cnt, Kit.MARGIN + IW - 10 - tw, c["count_y"]))


    # ---------- visitors ----------
    def scan_visitors(now, me):
        """Players within range, nearest first (every SCAN_EVERY seconds).
        True when a scan was made."""
        if now - st["scan_at"] < SCAN_EVERY:
            return False
        st["scan_at"] = now
        try:
            mx, my = int(me.X), int(me.Y)
            my_serial = me.Serial
        except Exception:
            return False
        if st["pos"] != (mx, my):
            st["pos"], st["moved_at"] = (mx, my), now
        rng = settings["range"]
        try:
            # the client's own filter keeps the humans (no IsHuman read per mobile:
            # cheaper here than the pass's shared scan)
            mobs = API.GetAllMobiles(distance=rng, isHuman=True) or []
        except Exception:
            mobs = []
        # a visitor's name and notoriety change rarely: read every NAME_CACHE_SECS
        # per serial, not per scan (the position and hidden flag are read every scan)
        cache = st["ncache"]
        if len(cache) > NAME_CACHE_MAX:
            for k in [k for k, e in cache.items() if now >= e[0]]:
                del cache[k]
            if len(cache) > NAME_CACHE_MAX:
                cache.clear()
        out = []
        for m in mobs:
            try:
                if m is None:
                    continue
                serial = m.Serial
                if serial == my_serial:
                    continue
                e = cache.get(serial)
                if e is not None and now < e[0]:
                    name, noto = e[1], e[2]
                else:
                    try:                                  # 2.6.82: read plainly (no getattr by name)
                        pet = bool(m.IsRenamable)
                    except Exception:
                        pet = False
                    if pet:                               # a pet: never a visitor
                        cache[serial] = (now + NAME_CACHE_SECS, None, "pet")
                        continue
                    noto = noto_name(m)
                    name = str(m.Name or "")
                    cache[serial] = (now + NAME_CACHE_SECS, name, noto)
                if name is None:                          # a pet, cached
                    continue
                if noto == "invulnerable":          # vendors, healers
                    continue
                if not settings["friends"] and noto == "ally":
                    continue
                vx, vy = int(m.X), int(m.Y)
                dist = max(abs(vx - mx), abs(vy - my))
                if dist > rng:
                    continue
                try:
                    hid = bool(m.IsHidden)
                except Exception:
                    hid = False
                out.append({"serial": serial, "name": name, "noto": noto,
                            "dist": dist, "hidden": hid,
                            "x": vx, "y": vy, "inside": False})
            except Exception:
                continue
        out.sort(key=_by_dist)
        st["near"] = len(out)
        st["visitors"] = out
        track_house(now, mx, my, out)
        refresh_rows()
        return True


    def _by_dist(v):
        return (v["dist"], v["name"].lower())


    # ---------- 2.6.05: in a house? the visitor log ----------
    def multi_at(x, y):
        """A house tile at x, y (the client's houses)? None when this TazUO
        can't say (no API.GetMultisAt). One call; on the client thread it
        doesn't wait."""
        try:
            ms = API.GetMultisAt(x, y)
        except AttributeError:                       # an older TazUO without it
            return None
        except Exception:                            # a passing hiccup: not a house this time
            return False
        if ms is None:
            return False
        try:
            return len(ms) > 0
        except Exception:
            try:
                return int(ms.Count) > 0
            except Exception:
                return False


    def track_house(now, mx, my, out):
        """After a scan: are you in a house (looked up when you move, else
        every HOUSE_EVERY s), and which visitors stand in one (looked up only
        for those who moved, HOUSE_CHECKS a scan at most). Opens a visit when
        a player steps in and closes it when they step out or leave."""
        if st["house_pos"] != (mx, my) or now >= st["house_at"]:
            st["house_pos"], st["house_at"] = (mx, my), now + HOUSE_EVERY
            st["in_house"] = multi_at(mx, my)
            if st["in_house"] is None and not st["no_multi_said"]:
                st["no_multi_said"] = True
                API.SysMsg("%s: this TazUO can't tell where houses are (no API.GetMultisAt), so the "
                           "visitor log and the red or Foe alarm stay off." % TITLE, Kit.HUE_INFO)
        opened = st["open_visits"]
        if not st["in_house"]:
            st["auto_no_rights"] = False             # out of the house: an auto eject may try again
            if st["inside"]:
                st["inside"] = {}
            if opened:
                close_visits(now)
            return
        old = st["inside"]
        new = {}
        budget = HOUSE_CHECKS
        for v in out:
            s = v["serial"]
            e = old.get(s)
            if e is None or e[0] != v["x"] or e[1] != v["y"]:
                if budget > 0:                       # moved (or new): look again
                    budget -= 1
                    e = (v["x"], v["y"], bool(multi_at(v["x"], v["y"])))
                elif e is None:
                    continue                         # new and over this scan's budget: next scan
            new[s] = e
            inside = e[2]
            v["inside"] = inside
            if inside:
                if s not in opened:
                    open_visit(v, now)
            elif s in opened:
                close_visit(s, now)
        st["inside"] = new
        if opened:
            for s in list(opened):
                if s not in new:                     # out of range or gone: the visit ends
                    close_visit(s, now)


    def open_visit(v, now):
        s = v["serial"]
        e = None
        for k in range(len(visits) - 1, -1, -1):     # their last visit, if it just ended: the same one
            if visits[k][2] == s:
                e = visits[k]
                break
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
        e = st["open_visits"].pop(s, None)
        if e is not None:
            e[1] = now
            visits_changed()


    def close_visits(now):
        for s in list(st["open_visits"]):
            close_visit(s, now)


    def mark_visit(serial, flag):
        """An eject or ban of this player worked: their last visit says so."""
        for k in range(len(visits) - 1, -1, -1):
            if visits[k][2] == serial:
                visits[k][6] = flag
                visits_changed()
                return


    # ---------- 2.6.05: eject on sight (reds and Ultima Tracker's Foes) ----------
    def is_foe(serial, name, now):
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


    def own_people():
        """Serials of your party and of TazUO's friends list (eject on sight
        leaves them alone, whatever their notoriety)."""
        out = set()
        try:
            out.update(int(x) for x in (API.GetPartyMemberSerials() or []))
        except Exception:
            pass
        try:
            for f in (API.GetAllFriends() or []):
                try:
                    out.add(int(getattr(f, "Serial", f)))
                except Exception:
                    continue
        except Exception:
            pass
        return out

    def eject_on_sight(now, me):
        """After a scan, with the setting on and you in a house: a red (or
        Foe-list) player standing in the house raises one alert (once per
        player every EJECT_FOE_EVERY s) that asks whether to eject them; the
        Eject button on their visitor row does it, on your press. (2.6.5: the
        2.6.06 eject-on-sight acted on a player with no press, which the shard's
        rules don't allow; this is the prompt it became.)"""
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
            if mates is None:                        # your party and friends list: never
                mates = own_people()
            if s in mates:
                continue
            if len(eject_at) > NAME_CACHE_MAX:
                for k in [k for k, t in eject_at.items() if t <= now]:
                    del eject_at[k]
            eject_at[s] = now + EJECT_FOE_EVERY
            what = "red" if v["noto"] == "murderer" else "Foe"
            if not HOST.alert(ALERT_FOE, "%s (%s) is in your house: Eject from their row?"
                              % (v["name"] or "Someone", what), "alarm", who=s):
                add_log("%s (%s) stepped in" % (v["name"] or "someone", what), Kit.HUE_BAD)
            return


    # ---------- Detect Hidden sweep ----------
    def sweep_held(me, now=None):
        """Why the sweep may not use the skill now (the shard's rules: no skill
        loop in a guarded region or while the zone isn't known yet, nothing in a
        fight, nothing while an alarm needs you), or None. Read every tick while
        the sweep is on, on the client thread. 2.6.81: the shared tests, so every
        loop agrees: HOST.fight_hold (dead, war mode, hurt, a hostile near, an
        item on the cursor, the attention alarm) and HOST.guard_hold (the strict
        reading: an unknown zone holds, the "Sweep now" press too)."""
        try:
            fight = HOST.fight_hold(now)             # asked every time: it keeps the HP watch
        except Exception:
            fight = None
        if fight == "dead":
            return HELD_DEAD
        try:
            g = HOST.guard_hold()
        except Exception:
            g = "unknown"                            # can't tell: the strict reading holds
        if g == "guard":
            return HELD_GUARD
        if g is not None:
            return HELD_UNKNOWN
        if fight:
            return HELD_FIGHT.get(fight, HOLD_TEXT.get(fight, fight))
        try:
            if HOST.alarm_up():                      # any module's alarm banner
                return HELD_ALARM
        except Exception:
            pass
        return None


    def start_sweep(now, forced=False):
        if st["house"] is not None or st["phase"] != "idle":
            return False
        held = st["held"]
        if held:
            if forced:
                note(held if held == HELD_UNKNOWN else "The sweep waits: %s" % held)
            return False
        if now < st["next_at"]:
            if forced:
                note("Detect Hidden is ready in %d s" % int(st["next_at"] - now + 0.99))
            return False
        if not forced and settings["still"] and now - st["moved_at"] < STILL_SECS:
            return False
        if not cursor_free():
            if forced:
                note("A target cursor is up: the sweep waits for it")
            return False
        me = HOST.me()
        if me is not None:
            st["scan_at"] = 0.0                  # a fresh look at who is in view now
            scan_visitors(now, me)
        try:
            st["seen"] = set([v["serial"] for v in st["visitors"] if not v["hidden"]])
        except Exception:
            st["seen"] = set()
        API.UseSkill(DETECT_SKILL)
        HOST.claim_cursor(KEY, CURSOR_WAIT)
        st["phase"], st["deadline"] = "cursor", now + CURSOR_WAIT
        return True


    def sweep_tick(now):
        if st["phase"] == "cursor":
            # 2.6.81: aim only Detect Hidden's own (neutral) cursor. The deadline
            # first (another claim must not keep the sweep waiting past it), then
            # step aside for anyone else's claim or pick; a harmful or beneficial
            # cursor is someone's spell: never aimed and never cancelled.
            if now > st["deadline"]:
                HOST.release_cursor(KEY)
                st["phase"] = "idle"
                st["next_at"] = now + RETRY_SOON
                note("Detect Hidden gave no cursor; trying again shortly")
            elif HOST.cursor_busy(KEY) is not None:
                return                               # another claim or a hand pick: wait for ours
            elif HOST.cursor_ok(KEY, "neutral"):
                API.TargetSelf()                     # your own spot: the area round you
                HOST.release_cursor(KEY)
                st["phase"], st["cast_at"] = "cast", now
                st["next_at"] = now + settings["cooldown"]
                st["sweeps"] += 1
            elif has_target():
                HOST.release_cursor(KEY)
                st["phase"] = "idle"
                st["next_at"] = now + RETRY_SOON
                add_log("a spell cursor came up, so that sweep was dropped", Kit.HUE_INFO)
            return
        if st["phase"] == "cast":
            # the shard reveals at once: anyone in view within REVEAL_WINDOW of
            # the aim who wasn't before was revealed by it (later arrivals just
            # walked in)
            if now - st["cast_at"] <= REVEAL_WINDOW:
                for v in st["visitors"]:
                    if v["serial"] not in st["seen"] and not v["hidden"]:
                        st["seen"].add(v["serial"])
                        st["revealed"] += 1
                        safe(lambda: API.HeadMsg("* revealed *", v["serial"], Kit.HUE_BAD))
                        add_log("revealed %s" % (v["name"] or "someone"), Kit.HUE_BAD)
                        if settings["sound"]:
                            HOST.alert(ALERT_REVEAL, "Revealed %s" % (v["name"] or "someone"),
                                       "warn", who=v["serial"])
            if now - st["cast_at"] > REPLY_WAIT:
                st["phase"] = "idle"


    def on_journal(ln):
        """Lines from the shard about the sweep or a house command."""
        now = time.time()                            # 2.6.82: one clock read per line
        if (st["house"] is None and st["house_wait"] is None and st["phase"] not in ("cursor", "cast")
                and now - st["cast_at"] >= REPLY_WAIT):
            return                                   # nothing waits for the shard: not ours
        low = ln.low
        waiting = (st["house"] is not None or st["house_wait"] is not None
                   or st["phase"] in ("cursor", "cast") or now - st["cast_at"] < REPLY_WAIT)
        if (settings["say_replies"] and waiting and not low.startswith(OWN_PREFIX)
                and not low.startswith(OWN_REPLY_PREFIX)):
            # debug: the shard's actual texts, to fix the match lists on the settings page
            API.SysMsg("%s: reply: %s" % (TITLE, ln.text.strip()), Kit.HUE_INFO)
        if st["phase"] in ("cursor", "cast") or now - st["cast_at"] < REPLY_WAIT:
            for t in J_WAIT:
                if t in low:
                    if st["phase"] == "cursor":
                        HOST.release_cursor(KEY)
                    elif st["phase"] == "cast":
                        st["sweeps"] = max(0, st["sweeps"] - 1)   # counted on aim; it didn't happen
                    st["phase"] = "idle"
                    st["next_at"] = time.time() + RETRY_SOON
                    note("Skill delay: trying again shortly")
                    return
            for t in J_NOTHING:
                if t in low:
                    st["empty"] += 1
                    return
            for t in J_REVEAL:
                if t in low:
                    note("Someone was revealed", 6.0)
                    if settings["sound"]:
                        HOST.alert(ALERT_REVEAL, "Someone was revealed", "warn")
                    return
        h = st["house"]
        if h is None:
            return
        for t in J_DONE[h["kind"]]:
            if t in low:
                add_log("%s %s%s" % (CMDS[h["kind"]][1], h["name"] or "the target",
                                     " (on sight)" if h.get("auto") else ""), Kit.HUE_GOOD)
                if h["kind"] in ("eject", "ban"):            # the visitor log says so (2.6.05)
                    mark_visit(h["serial"], 2 if h["kind"] == "ban" else 1)
                finish_house()
                return
        for t in J_HOUSE_NO:
            if t in low:
                add_log("%s %s failed: %s" % (VERBS[h["kind"]].lower(), h["name"] or "the target",
                                              ln.text.strip()), Kit.HUE_BAD)
                if h.get("auto"):                    # refused for this player: leave them be a while
                    st["eject_at"][h["serial"]] = time.time() + EJECT_FOE_FAIL
                finish_house()
                return


    # ---------- house commands (eject / ban) ----------
    def start_house(kind, serial, name, now, waited=False, auto=False):
        """auto (2.6.05): an eject on sight; it never clears a Ban waiting for
        its second click, and when it can't be said it is dropped quietly (the
        player is tried again on a later scan)."""
        if st["house"] is not None or (st["house_wait"] is not None and not waited):
            note("A house command is still running: wait for it")
            return
        if st["phase"] == "cursor":
            # Detect Hidden was just used and its cursor is still to come: saying
            # the house command now would let that cursor arrive first and be aimed
            # at you, with the house's own cursor then left up unclaimed. Wait for
            # the sweep's cursor to resolve (sweep_tick aims it or gives up at its
            # deadline, at most CURSOR_WAIT = 3 s), then say the command (house_wait_tick).
            st["house_wait"] = {"kind": kind, "serial": serial, "name": name,
                                "until": now + CURSOR_WAIT, "auto": auto}
            if not auto:
                st["confirm"] = None
            return
        if not cursor_free():
            if auto:
                st["eject_at"].pop(serial, None)
            else:
                note("A target cursor is up: press Esc or use it first")
            return
        key, verb, what = CMDS[kind]
        if not name:
            if what == "mobile":
                m = safe(lambda: API.FindMobile(serial))
            else:
                m = safe(lambda: API.FindItem(serial))
            name = str(safe(lambda: m.Name, "") or "") if m is not None else ""
        API.Msg(settings[key])
        HOST.claim_cursor(KEY, CURSOR_WAIT)
        st["house"] = {"kind": kind, "serial": serial, "name": name, "deadline": now + CURSOR_WAIT,
                       "said": now, "aimed": 0.0, "auto": auto}
        if not auto:
            st["confirm"] = None


    def finish_house():
        st["house"] = None
        HOST.release_cursor(KEY)


    def house_wait_tick(now):
        """A house command held back while the sweep's cursor was pending: say
        it once that cursor has been aimed (or given up) and no cursor is up."""
        hw = st["house_wait"]
        if hw is None:
            return
        auto = hw.get("auto", False)
        if st["phase"] != "cursor" and cursor_free():
            st["house_wait"] = None
            start_house(hw["kind"], hw["serial"], hw["name"], now, waited=True, auto=auto)
        elif now > hw["until"]:
            st["house_wait"] = None
            if st["phase"] == "cursor":              # the skill never gave a cursor: let it go
                HOST.release_cursor(KEY)
                st["phase"] = "idle"
                st["next_at"] = now + RETRY_SOON
            if cursor_free():
                start_house(hw["kind"], hw["serial"], hw["name"], now, waited=True, auto=auto)
            elif auto:                               # eject on sight: dropped, tried again later
                st["eject_at"].pop(hw["serial"], None)
            else:
                note("A target cursor is up: press Esc or use it first")


    def house_tick(now):
        h = st["house"]
        if h is None:
            return
        if not h["aimed"]:
            # 2.6.81: the deadline first, then step aside for anyone else's claim
            # or pick; aim only the house's own (neutral) cursor. A harmful or
            # beneficial cursor is someone's spell: drop the command, never aim
            # it at the player or item and never cancel it.
            if now <= h["deadline"]:
                if HOST.cursor_busy(KEY) is not None:
                    return
                if not HOST.cursor_ok(KEY, "neutral"):
                    if has_target():
                        add_log("%s %s: a spell cursor came up, so the command was dropped"
                                % (VERBS[h["kind"]].lower(), h["name"] or "the target"), Kit.HUE_BAD)
                        finish_house()
                    return
                if CMDS[h["kind"]][2] == "mobile":
                    there = safe(lambda: API.FindMobile(h["serial"]))
                else:
                    there = safe(lambda: API.FindItem(h["serial"]))
                if there is None:
                    API.CancelTarget()
                    add_log("%s %s: out of sight" % (VERBS[h["kind"]].lower(), h["name"] or "the target"),
                            Kit.HUE_BAD)
                    finish_house()
                    return
                API.Target(h["serial"])
                HOST.release_cursor(KEY)
                h["aimed"] = now
            else:                                    # past the deadline: give up
                if h.get("auto"):
                    # not your house (or no right to eject here): no more tries
                    # until you step out of the house and back in (2.6.05)
                    st["auto_no_rights"] = True
                    add_log("eject on sight: the house gave no cursor for %s (your house, with the right "
                            "to eject?); it waits until you step out and back in" % (h["name"] or "the target"),
                            Kit.HUE_BAD)
                else:
                    add_log("%s %s: the house gave no cursor (are you in your house, with the right to? "
                            "If the shard has no spoken form of this, use the house sign)"
                            % (VERBS[h["kind"]].lower(), h["name"] or "the target"), Kit.HUE_BAD)
                finish_house()
            return
        if now - h["aimed"] > REPLY_WAIT:          # no journal reply seen: say what was done
            add_log("%s aimed at %s (no reply seen)" % (VERBS[h["kind"]].lower(), h["name"] or "the target"))
            finish_house()


    def want_ban(serial, name, now):
        if settings["confirm"]:
            c = st["confirm"]
            if not (c and c[0] == serial and now < c[1]):
                st["confirm"] = (serial, now + CONFIRM_SECS)
                note("Ban %s? Click Ban (or pick them) again to confirm." % (name or "them"), CONFIRM_SECS)
                return
        start_house("ban", serial, name, now)


    # ---------- settings page (drawn inside the Virtue Assistant window) ----------
    # SWEEP: a field row and two check rows; VISITORS: a field row and three check
    # rows; HOUSE COMMANDS: three field rows (30 apart) and a grey line; DEBUG: one
    # check row. Each: a 30 px title row, then the rows, then 10 px.
    SEC1_H, SEC2_H, SEC3_H, SEC4_H = 122, 148, 154, 66
    EJECT_TIP = ("A red, or one on Ultima Tracker's Foe list, who steps into your house raises an alarm "
                 "(once per player every %d s); their row's Eject button ejects them" % int(EJECT_FOE_EVERY))
    CMD_TIPS = {"eject_cmd": "Said out loud to eject a player (owner, co-owner or friend)",
                "ban_cmd": "Said out loud to ban a player (owner or co-owner)",
                "friend_cmd": "Said out loud to make a player a friend of the house (owner)",
                "lock_cmd": "Said out loud to lock an item down (owner, co-owner or friend)",
                "release_cmd": "Said out loud to release a locked-down item (owner or co-owner)"}


    def config_height(w):
        return SEC1_H + Kit.GAP + SEC2_H + Kit.GAP + SEC3_H + Kit.GAP + SEC4_H


    def build_config(g, x, y, w):
        c = {}
        Kit.add_section(g, x, y, w, SEC1_H, "SWEEP  (Detect Hidden on your own spot)")
        Kit.add_label(g, "Seconds between uses:", x + 12, y + 34)
        c["cooldown"] = Kit.add_textbox(g, "%d" % int(settings["cooldown"]),
                                        x + 12 + Kit.text_w("Seconds between uses:") + 10, y + 30, 50)
        safe(lambda: c["cooldown"].SetTooltip("Seconds Detect Hidden waits after a use before the next, the "
                                              "shard's skill delay (%d-%d)" % (COOLDOWN_MIN, COOLDOWN_MAX)))
        c["still"] = Kit.add_check(g, "Sweep only while you stand still", x + 12, y + 60, settings["still"],
                                   "Hold the sweep while you walk; it goes on once you have stood still a second")
        c["sound"] = Kit.add_check(g, "Alert when a sweep reveals someone", x + 12, y + 86, settings["sound"],
                                   "Raise the Someone revealed in the house alert (sound: Settings > Alerts)")
        y2 = y + SEC1_H + Kit.GAP
        Kit.add_section(g, x, y2, w, SEC2_H, "VISITORS  (the list in the window)")
        Kit.add_label(g, "List players within:", x + 12, y2 + 34)
        xr = x + 12 + Kit.text_w("List players within:") + 10
        c["range"] = Kit.add_textbox(g, str(settings["range"]), xr, y2 + 30, 50)
        Kit.add_label(g, "tiles", xr + 50 + 6, y2 + 34, Kit.HUE_INFO)
        safe(lambda: c["range"].SetTooltip("Players this many tiles from you are listed (%d-%d)"
                                           % (RANGE_MIN, RANGE_MAX)))
        c["friends"] = Kit.add_check(g, "List guild and alliance members too", x + 12, y2 + 60, settings["friends"],
                                     "Unticked, players shown green (your guild and its allies) are left out")
        c["confirm"] = Kit.add_check(g, "Ban needs a second click within %d s" % int(CONFIRM_SECS), x + 12, y2 + 86,
                                     settings["confirm"],
                                     "A Ban button or a Ban... pick asks for a second click, so the wrong person "
                                     "isn't banned")
        c["eject_foes"] = Kit.add_check(g, "Alarm when a red or Foe steps into the house",
                                        x + 12, y2 + 112, settings["eject_foes"], EJECT_TIP)
        y3 = y2 + SEC2_H + Kit.GAP
        Kit.add_section(g, x, y3, w, SEC3_H, "HOUSE COMMANDS  (said out loud; verify on the shard)")
        col = (w - 24) // 2
        left = (("Eject:", "eject_cmd"), ("Ban:", "ban_cmd"), ("Friend:", "friend_cmd"))
        right = (("Lock down:", "lock_cmd"), ("Release:", "release_cmd"))
        for cx, items in ((x + 12, left), (x + 12 + col, right)):
            lw = max([Kit.text_w(t) for t, _ in items]) + 10
            tw = col - lw - 16
            for i, (t, k) in enumerate(items):
                Kit.add_label(g, t, cx, y3 + 34 + i * 30)
                tb = c[k] = Kit.add_textbox(g, settings[k], cx + lw, y3 + 30 + i * 30, tw, numbers=False)
                safe(lambda: tb.SetTooltip(CMD_TIPS[k]))
        lines = Kit.wrap("Owner adds friends; owner and co-owners ban and release; friends eject and "
                         "lock down.", w - 28)
        for i, line in enumerate(lines[:1]):             # under both columns, inside the section
            Kit.add_label(g, line, x + 12, y3 + 124 + i * 16, Kit.HUE_INFO)
        y4 = y3 + SEC3_H + Kit.GAP
        Kit.add_section(g, x, y4, w, SEC4_H, "DEBUG  (for checking the shard's texts)")
        # the shard's replies in the journal, to fix the lists above (2.6.01)
        c["say_replies"] = Kit.add_check(g, "Print the shard's replies in the journal",
                                         x + 12, y4 + 30, settings["say_replies"],
                                         "Every journal line seen while a house command or a sweep waits for the "
                                         "shard is printed as \"%s: reply: ...\", to fix the lists above" % TITLE)
        page["c"] = c


    def poll_config():
        c = page["c"]
        if c is None:
            return
        changed = False
        confirm_was = settings["confirm"]
        try:
            txt = str(c["cooldown"].Text).strip()
            if txt.isdigit():
                v = float(max(COOLDOWN_MIN, min(COOLDOWN_MAX, int(txt))))
                if v != settings["cooldown"]:
                    settings["cooldown"], changed = v, True
            txt = str(c["range"].Text).strip()
            if txt.isdigit():
                v = max(RANGE_MIN, min(RANGE_MAX, int(txt)))
                if v != settings["range"]:
                    settings["range"], changed = v, True
            for k in ("still", "sound", "friends", "confirm", "say_replies", "eject_foes"):
                v = bool(c[k].IsChecked)
                if v != settings[k]:
                    settings[k], changed = v, True
                    if k == "eject_foes":            # switched on or off: a fresh start
                        st["auto_no_rights"] = False
                        st["eject_at"].clear()
            for k, d in (("eject_cmd", DEFAULT_EJECT_CMD), ("ban_cmd", DEFAULT_BAN_CMD),
                         ("friend_cmd", DEFAULT_FRIEND_CMD), ("lock_cmd", DEFAULT_LOCK_CMD),
                         ("release_cmd", DEFAULT_RELEASE_CMD)):
                v = str(c[k].Text or "").strip() or d
                if v != settings[k]:
                    settings[k], changed = v, True
        except Exception:
            page["c"] = None
            return
        if changed:
            save_settings()
            if settings["confirm"] != confirm_was and not st["minimized"]:
                queue("redraw")()           # the Ban tooltips say "a second click ... confirms" or not


    def config_closed():
        page["c"] = None


    # ---------- module hooks ----------
    def _start():
        st.update({"shutting": False, "docked": False, "queue": [], "phase": "idle",
                   "house": None, "house_wait": None, "confirm": None, "visitors": [], "near": 0,
                   "scan_at": 0.0, "ncache": {}, "log_dirty": False, "log_save_at": 0.0,
                   "pos": None, "moved_at": 0.0, "note": "", "note_until": 0.0,
                   "in_house": None, "house_pos": None, "house_at": 0.0, "inside": {},
                   "open_visits": {}, "visits_dirty": False, "visits_save_at": 0.0, "visits_redraw": False,
                   "eject_at": {}, "foe": {},
                   "auto_no_rights": False,
                   "minimized": bool(safe(lambda: HOST.dock_wanted(KEY), False))
                   or Kit.load_min(MIN_KEY)})
        fit.update({"slot": None, "k": 1.0, "full": None})   # (2.6.78) told again by the layout
        load_settings()
        st["rd"] = Journal.reader()
        st["held"] = None
        st["held_at"] = 0.0                          # 2.6.82: the next look at the sweep's holds
        safe(lambda: HOST.alert_kind(ALERT_REVEAL, "Someone revealed", REVEAL_SOUND))
        safe(lambda: HOST.alert_kind(ALERT_FOE, "Red or Foe in the house", ALERT_FOE_SOUND))
        build_window()
        hooks = Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"), fit=layout_fit)
        hooks.update({"exact": True, "verify": True, "drawn_at": drawn_at})   # (2.6.78) its slot exactly
        HOST.dock_add(KEY, hooks)
        API.SysMsg("%s: on; sweep %s (held in guard zones, in a fight and while an alarm waits), "
                   "visitors within %d tiles%s." % (
                       TITLE, "on" if st["sweep"] else "off", settings["range"],
                       ", red or Foe alarm on" if settings["eject_foes"] else ""), Kit.HUE_GOOD)


    def _tick():
        if win["g"] is None:
            return
        if Kit.was_clicked(win["store"], "close"):
            Kit.dispose(win["g"])
            return
        now = time.time()
        me = HOST.me()                               # 2.6.82: the pass's player (reads kept for the pass)
        while st["queue"]:
            action = st["queue"].pop(0)
            kind = action[0] if isinstance(action, tuple) else action
            if action == "settings":
                HOST.show_settings(KEY)
            elif action == "toggle_min":
                st["minimized"] = not st["minimized"]
                st["docked"] = False
                HOST.dock_forget(KEY)
                Kit.save_min(MIN_KEY, st["minimized"])
                build_window()
            elif action == "to_bar":
                HOST.dock_to_bar(KEY, TITLE)
            elif action == "redraw":
                build_window()
            elif action == "sweep":
                st["sweep"] = not st["sweep"]
                Kit.put_var(VIEW_KEY, "1" if st["sweep"] else "0")
                API.SysMsg("%s: sweep %s." % (TITLE, "on" if st["sweep"] else "off"),
                           Kit.HUE_GOOD if st["sweep"] else Kit.HUE_INFO)
            elif action == "now":
                if me is not None and st["phase"] == "idle":
                    st["held"] = sweep_held(me, now)   # (2.6.71) as of now, sweep on or off
                if me is not None and not start_sweep(now, forced=True) and st["phase"] != "idle":
                    note("A sweep is already running")
            elif action == "clear_log":
                del log[:]
                save_log_soon()
                refresh_log()
            elif action == "show_log":
                toggle_logwin()
            elif action == "log_view":                   # the log window: actions <-> visitors
                win["log_view"] = "log" if win["log_view"] == "visits" else "visits"
                Kit.put_var(LOG_VIEW_KEY, win["log_view"])
                if Kit.is_open(win["log_g"]):
                    build_logwin()
            elif action == "log_clear":                  # the log window's Clear: the view shown
                if win["log_view"] == "visits":
                    del visits[:]
                    st["open_visits"] = {}               # whoever is inside now is logged afresh
                    st["inside"] = {}
                    visits_changed()
                else:
                    del log[:]
                    save_log_soon()
                    refresh_log()
            elif kind in PICKS:
                which = PICKS[kind]
                if st["house"] is not None or st["house_wait"] is not None:
                    note("A house command is still running: wait for it")
                else:
                    note("Target the %s to %s (Esc cancels)" % (
                        "player" if CMDS[which][2] == "mobile" else "item", VERBS[which].lower()), PICK_WAIT)
                    HOST.pick_target(PICK_WAIT, picked(which))
            elif kind == "follow":
                Follow.toggle(action[1], TITLE)
            elif kind == "last":
                API.SetLastTarget(serial=action[1])
                safe(lambda: API.HeadMsg("* last target *", action[1], 0x35))
            elif kind == "ban":
                want_ban(action[1], action[2], now)
            elif kind in CMDS:
                start_house(kind, action[1], action[2], now)
        if st["log_dirty"] and now >= st["log_save_at"]:     # one write a second at most
            st["log_save_at"] = now + LOG_SAVE_EVERY
            save_log()
        if st["visits_dirty"] and now >= st["visits_save_at"]:   # 2.6.05: one write per 5 s at most
            st["visits_save_at"] = now + VISIT_SAVE_EVERY
            save_visits()
        if st["visits_redraw"]:                  # 2.6.05: the visitor view, one redraw a tick at most
            st["visits_redraw"] = False          # (changes seen in this tick's scan: on the next one)
            refresh_logwin()
        if me is None:
            return
        rd = st["rd"]
        if rd is not None:
            for ln in rd.new():
                try:
                    on_journal(ln)
                except Exception:
                    pass
        if scan_visitors(now, me):
            eject_on_sight(now, me)
        house_tick(now)
        if st["house"] is None:
            # 2.6.82: the holds every HELD_EVERY s while Detect Hidden is still
            # cooling down, every tick from HELD_EVERY s before it is ready; the
            # sweep starts only when now >= next_at, so the test start_sweep
            # goes by was always made in this same tick (fresh)
            fresh = False
            if st["sweep"] and st["phase"] == "idle" and (
                    now >= st["next_at"] - HELD_EVERY or now >= st["held_at"]):
                st["held_at"] = now + HELD_EVERY
                fresh = True
                held = sweep_held(me, now)
                if held != st["held"]:
                    was, st["held"] = st["held"], held
                    if held and not was:             # (2.6.81) once per wait, not per new reason
                        add_log("sweep waits: %s" % (held[:1].lower() + held[1:]), Kit.HUE_INFO)
            # 2.6.81: death is one of sweep_held's holds now (the status line says so)
            if st["house_wait"] is None and st["phase"] == "idle" and st["sweep"] \
                    and not st["held"] and fresh:
                start_sweep(now)                     # (2.6.82: the holds were looked at this tick)
            sweep_tick(now)
            house_wait_tick(now)
        if st["confirm"] and now >= st["confirm"][1]:
            st["confirm"] = None
        refresh_status()


    PICKS = {"pick_eject": "eject", "pick_ban": "ban", "pick_friend": "friend",
             "pick_lock": "lock", "pick_release": "release"}


    def picked(which):
        def done(serial):
            serial = int(serial or 0)
            if not serial:
                note("Nothing picked")
                return
            st["queue"].append((which, serial, None))
        return done


    def _stop():
        st["shutting"] = True
        st["house_wait"] = None
        safe(lambda: HOST.release_cursor(KEY))
        HOST.dock_remove(KEY)
        save_pos()
        save_log_pos()
        Kit.save_min(MIN_KEY, st["minimized"])
        save_settings()
        if st["log_dirty"]:
            save_log()
        if st["open_visits"]:                    # whoever is still inside: their visit ends now
            close_visits(time.time())
        if st["visits_dirty"]:
            save_visits()
        g, win["g"] = win["g"], None
        win["rows"] = []
        Kit.dispose(g)
        lg, win["log_g"] = win["log_g"], None
        win["log_rows"] = []
        Kit.dispose(lg)


    load_settings()
    MODULE = {"start": _start, "tick": _tick, "stop": _stop,
              "client_tick": True,
              "config_height": config_height, "build_config": build_config,
              "poll_config": poll_config, "config_closed": config_closed}
    # ============================= MODULE END ====================================
    return MODULE


# ------------------------- registration with Virtue Assistant ----------------
if "HOST" in globals() and hasattr(globals()["HOST"], "add"):
    HOST.add("butler", "Property Butler",
             "Keeps your house: Detect Hidden sweeps, visitors, eject, ban",
             _module_butler, 0.1,
             category="Skills and home")
else:
    import API
    API.SysMsg("Property Butler is a Virtue Assistant module and can't run on its own. "
               "Run Virtue Assistant instead; it loads this file.", 33)
