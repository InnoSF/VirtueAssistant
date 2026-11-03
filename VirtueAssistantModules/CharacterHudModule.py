# =============================================================================
#  Character HUD  -  a Virtue Assistant module (TazUO Legion Script, Python)
#  Shard: In Mani Ylem
#
#  This file is NOT a script to run on its own. It is one module of Virtue
#  Assistant, loaded by Virtue Assistant from LegionScripts/VirtueAssistantModules.
#  Virtue Assistant provides everything this file uses (API, G, safe, Client,
#  Kit, Follow, HOST, Journal, the main loop and the settings window), so run
#  that instead and tick Character HUD on its Modules tab.
#
#  To leave this module out, take this file out of the folder.
#  Module key: "hud"
#
#  A module made of PARTS (2.6.5): each part below was a module of its own in
#  2.6.06 and keeps every saved key, window place, list and file it had. A
#  part has its own box under the module's row on the Modules tab (click the
#  arrow on the row to see them) and runs only while it is ticked; the mother
#  script's PartSet runs the ticked parts side by side. The old module keys
#  still answer (the Action Bar's mod: cells, HOST.enable, HOST.by_key).
#
#     Frames           (was Unit Frames)      Health frames for you, your target and your party, with a cast bar
#     Buffs & Timers   (was Spell Timers)     Your buffs and debuffs, and the spells you put on others, timed
#     Swing Bar        (was Swing Timer)      A bar that shows when your next melee swing lands
#     Bandages         (was Bandage Agent)    One press, one bandage: a timer bar and alerts
#     Pets             (was Pets)             Your pets' health, distance and commands
#
#  Bandages (2.6.5): redone as one press = one bandage, with alerts that prompt
#  you; nothing bandages by itself any more (the shard's rules). 2.6.56: Bandages
#  and the Swing Bar are two-row panels of the same width (the bar and its
#  seconds; then the bandage, the count, the target ring and the spiral, or the
#  hit chance and the satiety), with no smaller form and no tray button.
#  2.6.67: in a zone, Bandages and the Swing Bar sit inside their frame's zone,
#  beside the art past the end of its bars, when there is room there.
#  2.6.82: speed pass: the Swing Bar ticks fast only while its bar fills (a swing
#  pokes the pass), Frames' fast ticks while a picture is made do the drawing
#  only, the pieces are placed when something changed, slow mobile fields are
#  read twice a second, Pets reads strangers less often (and lists your pets for
#  other modules as HOST.services["pets.list"]), fewer closures on hot paths.
# =============================================================================


def _module_hud():
    """Builds the module from its parts and returns its hooks."""
    KEY = "hud"
    TITLE = "Character HUD"

    # ---------- (2.6.57) pieces that ride on the player and target frames ----------
    #  Bandages and the buff row ride on the player frame, the Swing Bar on the
    #  target frame. Each piece sits on the frame's game side: below the frame
    #  while the frame's centre is in the top half of the screen, above it in the
    #  bottom half (decided again whenever the frame moves, is slotted in a zone
    #  or the screen changes size). The nearest piece first (order 0: Bandages,
    #  the Swing Bar), then the next beyond it (order 1: the buff row), so they
    #  never overlap; each is kept on screen. (2.6.60) A piece narrower than the
    #  frame's window is flush with the end of its bars (Bandages with the player
    #  frame's right end, the Swing Bar with the mirrored target frame's left
    #  end); one as wide (the buff rows) is centred on the window. They are
    #  tied to the frame with Kit.attach (the keeper and the layout move them
    #  with it; a zone never takes them as occupants). With Frames off, or that
    #  frame hidden, every piece is its own free window again, where it stands.
    #  Frames lists the frames (pieces_anchor) and places the pieces on its tick
    #  (pieces_place, the client thread); a piece lists itself (pieces_add).
    #  (2.6.67) In a zone, a piece narrower than the frame (Bandages, the Swing
    #  Bar) goes up INTO the frame's zone when it fits there: in the free room
    #  beside the art, a GAP past the end of the bars (right of the player
    #  frame's bars, left of the mirrored target frame's), centred on the art
    #  up and down. The frame then leaves a hole in its stone and black behind
    #  the piece (PIECES["hole"], read by build_frame), so the piece still shows
    #  and takes its clicks when the frame window is brought to the front. When
    #  the room beside the art is too small, it rides outside as before.
    #  (2.6.73) Inside, the piece sits under the bars, its own stone and black
    #  hidden, the art and the piece centred in the box as one block (the art a
    #  little higher); a corner zone grows down when the frame needs the room.
    PIECES = {"anchor": {},     # frame key -> getter of the frame's window
              "piece": {},      # piece key -> (frame key, order, getter of its window)
              "tied": {},       # piece key -> (its window, the frame window) it is tied to
              "side": {},       # frame key -> True: pieces below it, False: above
              "span": {},       # frame key -> getter of (x0, x1, bars_right) (2.6.60)
              "inner": {},      # frame key -> getter of (pad, W, H, art_y, art_h) in a zone (2.6.67)
              "hole": {},       # frame key -> (x, y, w, h) a piece takes inside it, window pixels (2.6.67)
              "bg": {},         # (2.6.72) piece window -> its background controls (hidden inside)
              "bare": {},       # (2.6.72) piece window -> True while its background is hidden
              "stack": {},      # frame key -> (below, px): the pieces stacked outside it (2.6.71)
              # (2.6.82) pieces_place's change check: a full placement only when
              # something it reads cheaply changed, else every PLACE_EVERY s
              "dirty": True, "full_at": 0.0, "sig": None, "objs": None, "inside": []}
    PLACE_EVERY = 0.5           # (2.6.82) seconds between full placements with no change seen
    # (2.6.73) Riding inside its frame a piece's stone frame and black section are
    # hidden, so only its rows take room: from its section's top (Kit.MARGIN into its
    # window) to the bottom of its lowest row (Bandages' controls end 53 px down).
    PIECE_IN = 42

    def pieces_extent(fkey, below):
        """(2.6.71) Pixels the pieces stacked outside frame `fkey` take under it
        (below True) or over it (False); 0 when they are on the other side."""
        s = PIECES["stack"].get(fkey)
        if s is None or s[0] != below:
            return 0
        return max(0, int(s[1]))

    def pieces_anchor(fkey, getter, span=None, inner=None):
        """Frames lists (getter) or drops (None) frame `fkey` as an anchor.
        span (2.6.60): a getter of the frame's bar panel, (x0, x1, right) in
        the frame window's own pixels, right True when the bars end on the
        right (the player frame) and False on the left (the mirrored target
        frame); a piece narrower than the frame window lines up with that end.
        inner (2.6.67): a getter of (pad, W, H, art_y, art_h) while the frame
        fills a zone (None out of one): where a piece can sit inside it."""
        PIECES["dirty"] = True
        if getter is None:
            PIECES["anchor"].pop(fkey, None)
            PIECES["span"].pop(fkey, None)
            PIECES["inner"].pop(fkey, None)
            PIECES["hole"].pop(fkey, None)
            for pkey, (fk, _o, _g) in list(PIECES["piece"].items()):
                if fk == fkey:
                    _piece_free(pkey)
        else:
            PIECES["anchor"][fkey] = getter
            if span is not None:
                PIECES["span"][fkey] = span
            if inner is not None:
                PIECES["inner"][fkey] = inner

    def pieces_add(pkey, fkey, order, getter):
        PIECES["piece"][pkey] = (fkey, int(order), getter)
        PIECES["dirty"] = True

    def pieces_remove(pkey):
        PIECES["piece"].pop(pkey, None)
        PIECES["dirty"] = True
        _piece_free(pkey)

    def _piece_free(pkey):
        tied = PIECES["tied"].pop(pkey, None)
        g = None
        if tied is not None:
            safe(lambda: Kit.detach(tied[0]))
            g = tied[0]
        elif pkey in PIECES["piece"]:
            g = safe(PIECES["piece"][pkey][2])
        # 2.6.81: a piece let go while it rode inside its frame gets its stone and
        # black back (only pieces_place showed them again, and it stops with Frames);
        # nothing is written when its background wasn't hidden
        bare = PIECES.get("bare")
        if g is None or not bare or not bare.pop(g, False) or not Kit.is_open(g):
            return
        for ctrl in list(Kit._frame_parts.get(g) or ()) + list(PIECES["bg"].get(g) or ()):
            safe(lambda: setattr(ctrl, "IsVisible", True))

    def pieces_frame(fkey):
        """The frame window `fkey` while it is shown, else None."""
        fn = PIECES["anchor"].get(fkey)
        if fn is None:
            return None
        try:
            g = fn()
        except Exception:
            return None
        if g is None or not Kit.is_open(g):
            return None
        try:
            if not g.IsVisible:
                return None
        except Exception:
            pass
        return g

    def pieces_on(pkey):
        """Does piece `pkey` ride on its frame now (False: a free window)?"""
        p = PIECES["piece"].get(pkey)
        return p is not None and pieces_frame(p[0]) is not None

    RAISE_EVERY = 0.25          # (2.6.67) seconds between looks at a piece inside its frame's zone
    RAISE = {"at": 0.0, "uim": None, "off": False, "same": None}

    def pieces_raise(pairs):
        """(2.6.67) Keep each piece riding inside its frame's zone in front of
        the frame window: a click on the frame brings that window to the front
        (the hole keeps the piece seen; this keeps its buttons clickable).
        Walks the client's gump list from the top until it meets the piece
        (fine) or the frame (the piece is brought to the front). Client thread,
        every RAISE_EVERY s; off for good on a client that won't say."""
        if RAISE["off"]:
            return
        now = time.time()
        if now < RAISE["at"]:
            return
        RAISE["at"] = now + RAISE_EVERY
        try:
            if RAISE["uim"] is None:
                import System
                RAISE["same"] = System.Object.ReferenceEquals
                RAISE["uim"] = Tz.T("ClassicUO.Game.Managers.UIManager")
            uim, same = RAISE["uim"], RAISE["same"]
            gumps = Tz.get(None, "Gumps", uim)
            mp = _KIT_MOUSE_POS() if _KIT_MOUSE_POS is not None else None
            for pg, fg in pairs:
                if mp is not None:                   # (2.6.72) never under the mouse: the
                    fr_ = _rect_of(fg)               # frame's tooltip would go under the piece
                    if fr_ is not None and fr_[0] <= mp[0] < fr_[0] + fr_[2] \
                            and fr_[1] <= mp[1] < fr_[1] + fr_[3]:
                        continue
                rp, rf = Kit._raw_gump(pg), Kit._raw_gump(fg)
                if rp is None or rf is None:
                    continue
                node = gumps.First
                while node is not None:
                    v = node.Value
                    if same(v, rp):
                        break
                    if same(v, rf):
                        Tz.call(None, "MakeTopMostGump", [rp], uim)
                        break
                    node = node.Next
        except Exception:
            RAISE["off"] = True

    # (2.6.82) the mother's per-pass player and mobile (reads only), when it has them
    HUD_ME = getattr(HOST, "me", None)
    HUD_MOBILE = getattr(HOST, "mobile", None)
    _KIT_RECT = getattr(Kit, "rect", None)            # (2.6.82) looked up once, not per call
    _KIT_NOTE_RECT = getattr(Kit, "note_rect", None)
    _KIT_PIN_SIZE = getattr(Kit, "pin_size", None)
    _KIT_MOUSE_POS = getattr(Kit, "mouse_pos", None)

    def _rect_of(g):
        """(2.6.70) (x, y, w, h) of window g as last placed (Kit.rect: what was
        asked for, until the client has applied it), or None. A frame window
        just rebuilt reads 0, 0, 0 x 0 from the client for a frame; the pieces
        were put against that, at the screen's top-left corner, and the frame
        rebuilt again without their hole: the bandage and swing pieces
        flickered between there and their place."""
        fn = _KIT_RECT
        try:
            if fn is not None:
                r = fn(g)
            else:
                r = (int(g.GetX()), int(g.GetY()), int(g.GetWidth()), int(g.GetHeight()))
        except Exception:
            return None
        if r is None or r[2] <= 0 or r[3] <= 0:
            return None
        return r

    def _pieces_sig(sw, sh):
        """(2.6.82) What pieces_place can read cheaply: the screen, each piece's
        window (its getter: no client call) and each frame's window, place,
        bar span and zone room. (values, windows): the windows are compared by
        identity (a .NET == would be a call into the client)."""
        vals = [sw, sh]
        objs = []
        for pkey, (fk, order, getter) in PIECES["piece"].items():
            try:
                g = getter()
            except Exception:
                g = None
            vals.append((pkey, fk, order))
            objs.append(g)
        for fk, fn in PIECES["anchor"].items():
            fg = pieces_frame(fk)
            r = span = inner = None
            if fg is not None:
                r = _rect_of(fg)
                sfn = PIECES["span"].get(fk)
                if sfn is not None:
                    try:
                        span = sfn()
                    except Exception:
                        span = None
                ifn = PIECES["inner"].get(fk)
                if ifn is not None:
                    try:
                        inner = ifn()
                    except Exception:
                        inner = None
            vals.append((fk, r, span, inner))
            objs.append(fg)
        return vals, objs

    def pieces_place():
        """Place every piece on its frame (Frames' tick, the client thread). A
        piece is moved only when its place differs; nothing waits. A frame or
        a piece whose size can't be known yet is left as it is this pass.
        (2.6.82) The full placement runs when the screen, a frame (its window,
        place, span or zone room) or a piece's window changed, after
        pieces_add / pieces_remove / pieces_anchor, after a pass that had to
        leave something for later, and every PLACE_EVERY s as a safety net (a
        piece moved by something else is put back then)."""
        try:
            sw, sh = Kit.screen()
        except Exception:
            sw, sh = 0, 0
        now = time.time()
        vals, objs = _pieces_sig(sw, sh)
        if not PIECES["dirty"] and now < PIECES["full_at"] and now + 2 * PLACE_EVERY > \
                PIECES["full_at"] and vals == PIECES["sig"]:
            old = PIECES["objs"]
            same = old is not None and len(old) == len(objs)
            if same:
                for i in range(len(objs)):
                    if objs[i] is not old[i]:
                        same = False
                        break
            if same:
                if PIECES["inside"]:
                    pieces_raise(PIECES["inside"])
                return
        PIECES["sig"], PIECES["objs"] = vals, objs
        PIECES["dirty"] = False
        PIECES["full_at"] = now + PLACE_EVERY
        seen = {}                                # piece key -> its open window (one look each)
        inside = []                              # (2.6.67) (piece, frame) riding in a zone
        by_frame = {}
        for pkey, (fk, order, getter) in PIECES["piece"].items():
            by_frame.setdefault(fk, []).append((order, pkey, getter))
        for fk in [k for k in PIECES["stack"] if k not in by_frame]:
            PIECES["stack"].pop(fk, None)        # (2.6.71) no pieces on it any more
        for fk, items in by_frame.items():
            fg = pieces_frame(fk)
            if fg is None:
                for _o, pkey, _g in items:
                    _piece_free(pkey)
                PIECES["hole"].pop(fk, None)
                PIECES["stack"].pop(fk, None)
                continue
            fr_r = _rect_of(fg)
            if fr_r is None:                     # (2.6.70) just made: next pass, as it was
                PIECES["dirty"] = True
                continue
            fx, fy, fw, fh = fr_r
            below = sh <= 0 or (fy + fh / 2.0) < sh / 2.0
            PIECES["side"][fk] = below
            span = None                          # (2.6.60) where the frame's bars end
            sfn = PIECES["span"].get(fk)
            if sfn is not None:
                try:
                    span = sfn()
                except Exception:
                    span = None
            inner = None                         # (2.6.67) the frame fills a zone: room inside it
            ifn = PIECES["inner"].get(fk)
            if ifn is not None and span is not None:
                try:
                    inner = ifn()
                except Exception:
                    inner = None
            hole = None
            items.sort()
            y = fy + fh if below else fy
            for _o, pkey, getter in items:
                try:
                    g = getter()
                except Exception:
                    g = None
                if g is None or not Kit.is_open(g):
                    _piece_free(pkey)
                    continue
                seen[pkey] = g
                try:
                    if not g.IsVisible:
                        continue
                except Exception:
                    continue
                pr = _rect_of(g)
                if pr is None:                   # (2.6.70) just made: next pass
                    PIECES["dirty"] = True
                    continue
                px, py, pw, ph = pr
                ix = None
                if inner is not None and hole is None and pw < fw:
                    # (2.6.72) inside the frame's block, under its bars: Bandages' left edge
                    # in line with the player frame's bars, the Swing Bar's right edge with
                    # the mirrored target frame's, a GAP under the bar panel (2.6.67 put it
                    # beside the art, past the end of the bars). (2.6.73) Inside, the
                    # piece's stone and black are hidden, so its rows are what lines up:
                    # its window sits Kit.MARGIN further out on every side, and it fits
                    # when its rows (PIECE_IN) end inside the frame's black
                    PM = Kit.MARGIN
                    pad, iw, ih, ay, ah = inner[:5]
                    rx = (span[0] - PM) if span[2] else (span[1] - pw + PM)
                    ry = (inner[5] if len(inner) > 5 else ay + ah) + Kit.GAP - PM
                    rx = max(pad - PM, min(rx, iw - pad - pw + PM))
                    if ry + PM + PIECE_IN <= ih - pad + 2 and rx >= 0:
                        ix, hole = (fx + rx, fy + ry), (rx, ry, pw, ph)
                if ix is not None:
                    x, ny = ix                   # inside the frame: the outside stack goes on
                    inside.append((g, fg))
                elif span is not None and pw < fw:
                    # (2.6.60) flush with the end of the frame's bars: Bandages under
                    # the player frame's right end, the Swing Bar under the mirrored
                    # target frame's left end, so the two frames mirror each other
                    x = fx + (span[1] - pw if span[2] else span[0])
                    x = max(fx, min(x, fx + fw - pw))
                else:                            # as wide as the frame (the buff rows)
                    x = fx + (fw - pw) // 2
                if ix is None:
                    if sw > 0:
                        x = max(0, min(x, sw - pw))
                    if below:
                        ny, y = y, y + ph
                    else:
                        y -= ph
                        ny = y
                if (px, py) != (x, ny):
                    try:
                        g.SetPos(x, ny)
                        if _KIT_NOTE_RECT is not None:
                            _KIT_NOTE_RECT(g, x, ny)   # (2.6.70) read back as asked until it lands
                        Kit.moved_by_code(g)
                    except Exception:
                        pass
                tied = PIECES["tied"].get(pkey)
                if tied is None or tied[0] is not g or tied[1] is not fg:
                    if tied is not None and tied[0] is not g:
                        safe(lambda: Kit.detach(tied[0]))
                    safe(lambda: Kit.attach(g, fg))
                    PIECES["tied"][pkey] = (g, fg)
            PIECES["stack"][fk] = (below, (y - (fy + fh)) if below else (fy - y))   # (2.6.71)
            PIECES["hole"].pop(fk, None)         # (2.6.72) no hole: the frame keeps its black
        # (2.6.72) a piece riding inside its frame draws no background of its own (its
        # stone frame and black section hidden: the frame's black shows through); out
        # of it, its own look again. Only changes are written.
        bare = PIECES.setdefault("bare", {})
        now_in = set(g for g, _f in inside)
        for d in (bare, PIECES["bg"]):           # closed windows let go
            for g in [g for g in d if not Kit.is_open(g)]:
                d.pop(g, None)
        for pkey, (fk, order, getter) in PIECES["piece"].items():
            g = seen.get(pkey)                   # (2.6.82) the first loop's look, if it had one
            if g is None:
                g = safe(getter)
                if g is None or not Kit.is_open(g):
                    continue
            want = g in now_in
            if bare.get(g, False) != want:
                bare[g] = want
                if want:                         # (2.6.74) its size stays when its stone hides
                    if _KIT_PIN_SIZE is not None:
                        _KIT_PIN_SIZE(g)
                for ctrl in list(Kit._frame_parts.get(g) or ()) + list(PIECES.get("bg", {}).get(g) or ()):
                    try:
                        ctrl.IsVisible = not want
                    except Exception:
                        pass
        PIECES["inside"] = inside
        if inside:
            pieces_raise(inside)

    PIECES_TARGET = {"fn": None}    # Frames: fn() -> the serial its target frame shows

    # (2.6.59) The readout beside the bar of Bandages and of the Swing Bar: the
    # design reserves the width of "15.0s", but in the client's label font
    # "Ready" and "Paused" are wider (46 px to 35) and ran into the frame, so
    # the room is the widest of the readout's words, the same in both panels,
    # which still makes the two the same width and stack flush.
    READOUT_WORDS = ("Ready", "Done", "Out!", "Dead", "Paused")

    def readout_room():
        return max(Kit.text_w(w) for w in READOUT_WORDS)

    def pieces_side(fkey):
        """True when the pieces of frame fkey sit below it (top half), else False."""
        return PIECES["side"].get(fkey, True)


    def _part_frames():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  2.5.29: frames stay exactly where you drop them. They no longer take part
        #          in window snapping (no jump to a screen anchor, an edge or another
        #          window on release, and they never follow another window that is
        #          dragged); a drag is saved the moment it ends; a position is never
        #          taken from a failed read; the mirror option measures the window
        #          in gump pixels (TazUO's UI scale) and no longer moves the target
        #          frame at start-up: saved positions win. A frame dropped within
        #          FRAME_SNAP px of another frame lines up with it pixel-exact
        #          (snap_to_frames); frames snap to frames only.
        # ============================ MODULE START ===================================
        #  PART: Frames  -  player, target and tracked-player frames showing
        #  health, mana and stamina, with a snapshot picture of each character's
        #  paperdoll (head and shoulders). The rounded frame art is drawn by this
        #  code at runtime; no image files are needed.
        #
        #  Party members' frames can have their own size (FRAME SIZE on the
        #  settings page: tick "Party members" and set their slider).
        #
        #  Alt+click any frame (target or tracked) to auto-follow that character
        #  with TazUO's auto-follow; Alt+click it again to stop. Uses the shared
        #  Follow helper, so it agrees with Ultima Tracker on who you follow.
        #
        #  2.6.05: a cast bar under the player frame (your spell's name, filling
        #  through its cast delay; green when cast, red on a fizzle or a broken
        #  concentration) and a GUARDED tag on the player frame.
        # =============================================================================

        KEY = "unitframes"
        TITLE = "Frames"

        # ------------------------------- CONFIG --------------------------------------
        ROWS = ("hits", "mana", "stam")    # what each bar shows, top to bottom
        BAR_BG = "#17171a"
        BAR_COLOR = {"hits": "#c22d2d", "poison": "#2f9a3c", "yellow": "#cfae2a",
                     "mana": "#2f62cc", "stam": "#d39a1c"}
        NOTO_COLOR = {"innocent": (46, 104, 214), "ally": (40, 160, 70), "gray": (120, 120, 126),
                      "criminal": (120, 120, 126), "enemy": (222, 118, 30),
                      "murderer": (196, 38, 38), "invulnerable": (214, 178, 40)}
        NO_NOTO = (226, 226, 230)          # unknown, dead, out of range, no target (plain line)
        NOTO_NUM = {1: "innocent", 2: "ally", 3: "gray", 4: "criminal", 5: "enemy",
                    6: "murderer", 7: "invulnerable"}

        # Snapshot pictures (head and shoulders of the paperdoll)
        SNAP_BG = (0, 0, 8)                # the paperdoll's own black backdrop
        MALE_GUMP, FEMALE_GUMP = 50000, 60000
        PAPERDOLL_BODY = {0x0190: 0x000C, 0x0192: 0x000C, 0x0191: 0x000D, 0x0193: 0x000D,
                          0x025D: 0x000E, 0x025F: 0x000E, 0x025E: 0x000F, 0x0260: 0x000F,
                          0x029A: 0x029A, 0x02B6: 0x029A, 0x029B: 0x0299, 0x02B7: 0x0299,
                          0x04E5: 0xC835, 0x03DB: 0x000C}
        FEMALE_BODIES = (0x0191, 0x0193, 0x025E, 0x0260, 0x029B, 0x02B7)
        GM_BODY, GM_BODY_HUE = 0x03DB, 0x03EA
        # Layers drawn for the head and shoulders, in the client's paperdoll order
        LAYERS = ("cloak", "shirt", "arms", "torso", "tunic", "face", "robe", "neck",
                  "hair", "beard", "earrings", "helmet")
        LAYERS_QUIVER = ("shirt", "arms", "torso", "tunic", "face", "robe", "cloak", "neck",
                         "hair", "beard", "earrings", "helmet")       # quiver worn as a cloak
        LAYERS_PARROT = ("shirt", "arms", "torso", "tunic", "cloak", "face", "neck",
                         "hair", "beard", "earrings", "helmet", "robe")
        PARROT_ROBES = (0xA2CA, 0xA2CB)
        OPEN_ROBES = (0x9985, 0x9986, 0xA412, 0xA2CB, 0xA2CA)   # robes that don't hide the torso
        PLATE_ARMS = (0x1410, 0x1417)                            # drawn under the torso
        # The crop is found from the art itself: the figure's top (the head, or a
        # helmet's crest) sits HEAD_GAP art pixels below the top of the circle, the
        # figure is centred, and SNAP_DEPTH art pixels of it show at 100% zoom. The
        # PICTURE sliders on the settings page shift and zoom this for everyone.
        SNAP_DEPTH = 110                   # art pixels shown top to bottom (circle height)
        HEAD_GAP = 2                       # art pixels between the top of the circle and the head
        FIGURE_DEPTH = 120                 # rows below the top used to centre the figure
        CROP = {}                          # fallback (centre x, centre y) per body if art is empty
        CROP_DEFAULT = (98, 70)
        SNAP_RETRY = 2.0                   # seconds before retrying someone out of sight
        SNAP_BUDGET = 0.008                # seconds of picture work per slice (spread over ticks)
        THREAD_BUDGET = 0.03               # seconds of drawing per thread_tick (script's thread)
        STATUS_EVERY = 0.5                 # seconds between reads of your AR, weight and gold
        SNAP_TICK = 0.03                   # tick interval while a picture is being made
        TEX_PREFIX = "vauf_"               # names of the textures this module makes

        MAX_TRACKED = 12
        SCALE_MIN, SCALE_MAX, SCALE_DEFAULT = 50, 150, 70    # % of the art's size
        LABEL_H = 14                                         # height of the UO label font
        PARTY_EVERY = 1.0                                    # seconds between party checks
        PICK_TIMEOUT = 10                                    # seconds the "Pick" cursor waits
        PREVIEW = 100                                        # settings-page picture preview

        SETTINGS_KEY = "UnitFrames_settings"                 # per character
        TRACKED_KEY = "UnitFrames_tracked"
        FRAMEPOS_KEY = "UnitFrames_framepos"
        POS_KEY = "UnitFrames_pos"
        MIN_KEY = "UnitFrames_min"         # control window minimized when you left
        W = 350                                  # control window (room for both minimize arrows)
        TRAY_ICON = 0x1B74                                   # the bar's tray button (kite shield)
        CLOSE_ART = (0x0FB1, 0x0FB2, 0x0FB1)                 # small X at a frame's top corner
        CLOSE_INSET = 3                                      # pixels in from the corner
        MINI_W, MINI_H = 240, 46

        DRAG_SETTLE = 0.4                                    # seconds at rest that end a drag
        SAVE_EVERY = 10.0                                    # seconds between belt-and-braces saves
        CROP_SETTLE = 0.5                                    # seconds the crop sliders rest before a retake
        PREVIEW_EVERY = 0.3                                  # seconds between live preview redraws
        TICK_EVERY = 0.1                                     # the tick interval while nothing is drawn
        FRAME_SNAP = SNAP_DIST                               # a dropped frame this close to another
        #                                                      frame lines up with it exactly
        # Cast bar under the player frame (2.6.05): your spells are known from your
        # own words of power in the journal (the mother's Kit.SPELL_WORDS), their
        # cast delay from Kit.spell_info (classic per-circle delays, unchecked in game)
        CAST_H = 24                                          # the bar's stone strip
        CAST_GAP = 2                                         # pixels between the frame and it
        CAST_HOLD = 1.5                                      # seconds the green / red bar stays
        CAST_FAIL_WINDOW = 10.0                              # a fail line this soon after the words
        #                                                      still turns it red (you may take a
        #                                                      while to pick the target)
        CAST_FALLBACK = 1.0                                  # delay of a spell with none known (unchecked)
        CAST_COLOR = {"cast": "#cfae2a", "done": "#2f9a3c", "fail": "#c22d2d"}
        CAST_FAIL_TEXTS = (("the spell fizzles", "fizzled"),                  # cliloc 502632
                           ("your concentration is disturbed", "disturbed"),  # cliloc 500641
                           ("insufficient mana", "no mana"),                  # cliloc 502625
                           ("more reagents are needed", "no reagents"))       # cliloc 502630
        GUARD_EVERY = 0.5                                    # seconds between HOST.guarded() reads
        SPELLS = getattr(Kit, "SPELL_WORDS", None) or {}     # words of power -> (spell, kind)
        TEXT_PX = getattr(Kit, "text_px", None) or Kit.text_w   # a text's width, by its letters
        OWN_PREFIX = TITLE.lower() + ":"                     # this module's own journal lines

        # Frame art: geometry and colours measured from the reference frame images (502 x 194,
        # circle on the left). The target frame is the same picture mirrored.
        ART_W, ART_H = 502, 194
        RING_C = (96.5, 96.5)              # circle centre
        HOLE_R = 52.5                      # transparent hole the snapshot shows through
        RING = ((86.0, (22, 22, 24)),      # (outer radius, colour), outside in
                (81.5, (226, 226, 230)),   # light line (notoriety colour goes over it)
                (79.5, "tire"),
                (64.5, (30, 25, 10)),
                (61.5, (226, 226, 230)),
                (60.5, "gold"),
                (53.5, (14, 10, 2)))
        NOTO_RING = (78.0, 83.5)           # band recoloured by notoriety
        PANEL = (150.0, 39.5, 491.5, 154.5, 9.0)       # outer outline (x0, y0, x1, y1, radius)
        METAL = (153.0, 42.6, 488.0, 151.0, 6.5)
        INNER = (178.5, 47.5, 476.5, 146.0, 8.0)       # dark edge round the bar area
        HOLES = (183.5, 51.5, 472.5, 141.5, 6.0)       # transparent bar area
        SEPARATORS = ((77.5, 83.5), (109.5, 115.5))
        RIVETS = ((483.5, 45.8, (188, 188, 193)), (483.5, 148.6, (128, 128, 133)))
        OUTLINE_RGB, INNER_RGB = (20, 20, 22), (16, 16, 18)
        # Status strip under the player frame's bars: a tab tucked under the ring,
        # inside the art's height (art pixels, y relative to STRIP_Y)
        STRIP_Y, STRIP_H = 157, 35
        STRIP_PANEL = (122.0, 1.5, 491.5, 33.5, 8.0)
        STRIP_METAL = (125.0, 4.6, 488.0, 30.5, 6.0)
        STRIP_INNER = (134.0, 8.5, 481.0, 26.5, 5.0)
        STRIP_TEXT_X = (150, 481)                      # cells, clear of the ring
        STRIP_CELLS = (("AR", "ar", 0.22), ("Wt", "weight", 0.39), ("Gold", "gold", 0.39))
        ART_ROWS_X = (182, 474)            # bars sit behind the holes, edges under the art
        ART_ROWS_Y = ((51, 79), (83, 111), (115, 143))
        SQRT_HALF = 0.70710678
        # -----------------------------------------------------------------------------

        DEFAULTS = {"player": True, "target": True, "hide_empty": False, "numbers": True,
                    "lock": False, "click": True, "party": False, "ignore_self": True,
                    "attack": False, "status": True, "scale": SCALE_DEFAULT, "pdx": 0, "pdy": 0,
                    "pscale_on": False, "pscale": SCALE_DEFAULT,
                    "pzoom": 100, "mirror": False,
                    # (2.6.85) Inventory > Supplies reads these once: kept so the saved
                    # string stays as it was for older versions
                    "sup_open": False, "sup_deep": True, "sup_hide0": False, "sup_follow": True,
                    "sup_low": 10, "sup_side": 0,
                    # 2.6.05 (2.6.04 skips keys it doesn't know)
                    "cast": True, "guard": True, "cast_say": False,
                    # 2.6.85: TazUO's own target health bar stays away while the target frame shows
                    "hide_bar": True}
        NUMBERS = {"scale": (SCALE_MIN, SCALE_MAX), "pscale": (SCALE_MIN, SCALE_MAX),
                   "pdx": (-60, 60), "pdy": (-60, 60),
                   "pzoom": (50, 200), "sup_low": (0, 9999), "sup_side": (0, 2)}
        settings = dict(DEFAULTS)
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [],
              "target": 0, "me": 0,
              "names": {}, "pos": {}, "next_party": 0.0, "rebuild": False, "next_save": 0.0,
              "pos_dirty": False, "pos_save_at": 0.0, "mirror_sw": None,
              "crop_changed": 0.0, "art": None, "art_scales": set(),
              "snap_px": None, "party": set(),
              "snaps": {}, "stale": set(), "snap_queue": [], "snap_tries": {}, "textures": set(),
              "next_supply": 0.0, "counts": {}, "art_jobs": [], "art_failed": set(),
              "running": False, "recent": [], "next_prune": 0.0, "art_dirty": True,
              "jr": None, "guard": None, "next_guard": 0.0,
              "dismissed": set(),          # (2.6.81) party members whose frame you removed
              "removing": False,           # (2.6.81) Remove frame's cursor is up
              "full_at": 0.0}              # (2.6.82) the next full tick (_tick)
        tracked = []                       # [{"serial", "name", "auto"}]
        anchor = {"sig": None, "at": None}   # (2.6.85) where a table beside the player frame goes
        cast = {"g": None, "c": {}, "spell": None, "start": 0.0, "secs": 1.0, "state": None,
                "until": 0.0, "pct": 0, "word": "", "shown": None, "at": None, "leader": None,
                "s": None, "w": 0}         # the cast bar (its own small window under the frame)
        frames = {}                        # key -> frame dict ("player", "target", "m<serial>")
        win = {"g": None, "store": ({}, {})}
        page = {"c": None, "store": ({}, {}), "next_preview": 0.0, "layers": None}
        item_info = {}                     # item graphic -> (anim id, partial hue, is container)


        # ---------- saved settings ----------
        _get, _put = Kit.get_var, Kit.put_var


        def load_settings():
            for part in _get(SETTINGS_KEY).split(","):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                if k not in DEFAULTS:
                    continue
                if k in NUMBERS:
                    lo, hi = NUMBERS[k]
                    try:
                        settings[k] = max(lo, min(hi, int(v)))
                    except ValueError:
                        pass
                else:
                    settings[k] = v == "1"


        def save_settings():
            _put(SETTINGS_KEY, ",".join("%s=%s" % (k, settings[k] if k in NUMBERS else
                                                   ("1" if settings[k] else "0"))
                                        for k in sorted(DEFAULTS)))




        def load_tracked():
            del tracked[:]
            for part in _get(TRACKED_KEY).split(";"):
                p = part.split(",", 2)
                if len(p) < 3:
                    continue
                try:
                    tracked.append({"serial": int(p[0]), "auto": p[1] == "1", "name": p[2]})
                except ValueError:
                    pass


        def save_tracked():
            _put(TRACKED_KEY, ";".join("%d,%s,%s" % (t["serial"], "1" if t["auto"] else "0",
                                                     t["name"].replace(";", " ").replace(",", " "))
                                       for t in tracked))


        def load_positions():
            st["pos"] = {}
            for part in _get(FRAMEPOS_KEY).split(";"):
                try:
                    k, xy = part.split(":")
                    x, y = xy.split(",")
                    st["pos"][k] = Kit.adapt(int(x), int(y))   # on the screen of today
                except ValueError:
                    pass


        def save_positions():
            """Write the frame positions: "player", "target" and the m<serial> of
            every character still tracked. Entries of characters no longer tracked
            are dropped here, so the saved string stops growing with every party
            member and target ever dragged over the months."""
            remember_positions()
            keep = set("m%d" % t["serial"] for t in tracked)
            keep.update(("player", "target"))
            pos = st["pos"]
            for k in [k for k in pos if k not in keep]:
                del pos[k]
            _put(FRAMEPOS_KEY, ";".join("%s:%d,%d" % (k, p[0], p[1])
                                        for k, p in sorted(pos.items())))
            st["pos_dirty"] = False


        def remember_positions():
            for key, fr in frames.items():
                if Kit.is_open(fr.get("g")):
                    p = frame_at(fr)
                    if p is not None and st["pos"].get(key) != p:
                        st["pos"][key] = p
                        st["pos_dirty"] = True


        def save_pos():
            Kit.save_pos(POS_KEY, win["g"])


        # ---------- game data ----------
        def my_serial():
            return int(safe(lambda: API.Player.Serial, 0) or 0)


        def noto_name(n):
            if n is None:
                return ""
            try:
                return NOTO_NUM.get(int(n), "")
            except Exception:
                return str(n).split(".")[-1].lower()


        def find_mobile(serial):
            """(2.6.82) For reads only: the pass's shared player / mobile (HOST.me,
            HOST.mobile: each property read once per pass for every module)."""
            if serial == st["me"]:
                return HUD_ME() if HUD_ME is not None else API.Player
            try:
                if HUD_MOBILE is not None:
                    return HUD_MOBILE(serial)
                return API.FindMobile(serial)
            except Exception:
                return None


        # read_mobile's answer is a tuple (cheap to build and to compare every tick):
        # (name, hits, hits max, mana, mana max, stamina, stamina max, notoriety,
        #  dead, poisoned, yellow hits, paralyzed)
        M_NAME, M_HITS, M_HMAX, M_MANA, M_MMAX, M_STAM, M_SMAX, M_NOTO, M_DEAD, M_POISON, \
            M_YELLOW, M_PARA = range(12)


        def read_mobile_slow(m):
            """Field by field, each with its own default: when the one-go read failed."""
            return (str(safe(lambda: m.Name, "") or ""),
                    int(safe(lambda: m.Hits, 0) or 0), int(safe(lambda: m.HitsMax, 0) or 0),
                    int(safe(lambda: m.Mana, 0) or 0), int(safe(lambda: m.ManaMax, 0) or 0),
                    int(safe(lambda: m.Stamina, 0) or 0), int(safe(lambda: m.StaminaMax, 0) or 0),
                    noto_name(safe(lambda: m.Notoriety)),
                    bool(safe(lambda: m.IsDead, False)), bool(safe(lambda: m.IsPoisoned, False)),
                    bool(safe(lambda: m.IsYellowHits, False)), bool(safe(lambda: m.IsParalyzed, False)))


        _slow_reads = {}                   # (2.6.82) serial -> (name, maxima, noto, until, dead)
        MOBILE_SLOW_EVERY = 0.5            # seconds between reads of a mobile's slow fields
        SLOW_READS_MAX = 64                # serials kept (cleared when full)


        def read_mobile(serial):
            """Health/mana/stamina of a mobile (the tuple above), or None if the
            client can't see it. Every frame reads this every tick, so it is read
            in one go: no closure per field. A field this client's mobiles lack
            gives its default (getattr); any other error falls back to the
            field-by-field read."""
            if not serial:
                return None
            m = find_mobile(serial)
            if m is None:
                return None
            # (2.6.82) name, the maxima and notoriety almost never change: read when the
            # serial is new, every MOBILE_SLOW_EVERY and at once when IsDead flips (a
            # resurrection changes the maxima); mana / stamina only while their max is
            # not 0 (the shard sends neither for mobiles outside your party)
            try:
                dead = bool(getattr(m, "IsDead", False))
                now = time.time()
                c = _slow_reads.get(serial)
                if c is None or now >= c[5] or dead != c[6]:
                    if c is None and len(_slow_reads) >= SLOW_READS_MAX:
                        _slow_reads.clear()
                    c = _slow_reads[serial] = (
                        str(getattr(m, "Name", "") or ""), int(getattr(m, "HitsMax", 0) or 0),
                        int(getattr(m, "ManaMax", 0) or 0), int(getattr(m, "StaminaMax", 0) or 0),
                        noto_name(getattr(m, "Notoriety", None)), now + MOBILE_SLOW_EVERY, dead)
                d = (c[0], int(getattr(m, "Hits", 0) or 0), c[1],
                     int(getattr(m, "Mana", 0) or 0) if c[2] else 0, c[2],
                     int(getattr(m, "Stamina", 0) or 0) if c[3] else 0, c[3],
                     c[4], dead, bool(getattr(m, "IsPoisoned", False)),
                     bool(getattr(m, "IsYellowHits", False)), bool(getattr(m, "IsParalyzed", False)))
            except Exception:
                _slow_reads.pop(serial, None)
                d = read_mobile_slow(m)
            name = d[M_NAME]
            if name and st["names"].get(serial) != name:
                st["names"][serial] = name
            return d


        _members = {}                      # (.NET type, name) -> (PropertyInfo / FieldInfo, is property) or None


        def instance_member(obj, name):
            """A property or field of a .NET object, public or not (None if absent).
            The reflection lookup is done once per type and name (the attack-target
            chain is read every tick): after that it is one GetValue."""
            t = obj.GetType()
            key = (t, name)
            acc = _members.get(key, False)
            if acc is False:
                from System.Reflection import BindingFlags
                flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
                p = t.GetProperty(name, flags)
                if p is not None:
                    acc = (p, True)
                else:
                    f = t.GetField(name, flags)
                    acc = (f, False) if f is not None else None
                _members[key] = acc
            if acc is None:
                return None
            return acc[0].GetValue(obj, None) if acc[1] else acc[0].GetValue(obj)


        class AttackTarget(object):
            """The mobile you are attacking, read from the client's TargetManager.
            Not part of the script API, so it is looked up by name; 0 if not found."""
            getter = None
            looked = False
            HOLD_FOR = 2.0          # (2.6.82) seconds the TargetManager found is kept
            CHAINS = (("ClassicUO.Game.Managers.TargetManager", ("LastAttack",)),
                      ("ClassicUO.Game.World", ("Instance", "TargetManager", "LastAttack")),
                      ("ClassicUO.Client", ("Game", "UO", "World", "TargetManager", "LastAttack")))

            @staticmethod
            def _chain(tname, names):
                t = Client._type(tname)
                if t is None:
                    return None
                first = Client._member(t, names[0])
                if first is None:
                    return None

                if len(names) == 1:
                    def get():
                        return int(first[0]() or 0)
                    get()
                    return get
                # (2.6.82) the object holding the last link (the TargetManager) is
                # kept while the chain's first object is the same one (and for at
                # most HOLD_FOR s), so a tick makes two reflection reads, not one per link
                held = {"root": None, "obj": None, "until": 0.0}
                last = names[-1]

                def get():
                    root = first[0]()
                    if root is None:
                        held["obj"] = None
                        return 0
                    obj = held["obj"]
                    now = time.time()
                    if obj is None or root is not held["root"] or now >= held["until"] or \
                            held["until"] - now > AttackTarget.HOLD_FOR:
                        held["obj"] = None
                        obj = root
                        for n in names[1:-1]:
                            if obj is None:
                                return 0
                            obj = instance_member(obj, n)
                        if obj is None:
                            return 0
                        held["root"], held["obj"], held["until"] = root, obj, now + AttackTarget.HOLD_FOR
                    try:
                        return int(instance_member(obj, last) or 0)
                    except Exception:
                        held["obj"] = None           # looked up again on the next call
                        raise
                get()
                return get

            @staticmethod
            def serial():
                if not AttackTarget.looked:
                    AttackTarget.looked = True
                    for tname, names in AttackTarget.CHAINS:
                        g = safe(lambda: AttackTarget._chain(tname, names))
                        if g is not None:
                            AttackTarget.getter = g
                            break
                g = AttackTarget.getter
                return int(safe(g, 0) or 0) if g is not None else 0


        def update_target():
            """Your current target: last target (or attack target), mobiles only."""
            s = AttackTarget.serial() if settings["attack"] else 0
            if not s:
                try:
                    s = int(API.LastTargetSerial or 0)
                except Exception:
                    s = 0
            if not s:
                st["target"] = 0
                return
            if s == st["target"]:
                return
            if s == st["me"] and settings["ignore_self"]:
                return                                   # bandaging yourself keeps the target
            if safe(lambda: API.FindMobile(s)) is not None or s == st["me"]:
                st["target"] = s                         # items and land tiles are ignored


        def sync_party():
            party = set(int(x) for x in (safe(lambda: list(API.GetPartyMemberSerials()), []) or [])
                        if int(x) and int(x) != st["me"])
            st["party"] = party                  # frames of these use the party scale
            changed = False
            # 2.6.81: a party member whose frame you removed stays removed until they
            # leave the party (or the option is unticked); Add frame brings them back
            dismissed = st["dismissed"]
            if dismissed:
                if settings["party"]:
                    dismissed &= party
                else:
                    dismissed.clear()
            if settings["party"]:
                for s in party:
                    if s in dismissed:
                        continue
                    if not any(t["serial"] == s for t in tracked) and len(tracked) < MAX_TRACKED:
                        tracked.append({"serial": s, "auto": True,
                                        "name": st["names"].get(s) or "Party member"})
                        changed = True
            for t in list(tracked):
                if t["auto"] and (t["serial"] not in party or not settings["party"]):
                    tracked.remove(t)
                    changed = True
            if changed:
                save_tracked()
                build_window()
                HOST.refresh_settings(KEY)       # the OTHERS' FRAMES list (2.6.51)


        # ---------- the client's picture plumbing ----------
        class Bridge(object):
            """Pictures made by this module. TazUO's LegionTextureControl draws a
            texture by name from the client's named-texture table (where PNGs from
            script zips go); this puts textures drawn here into that table, and
            reads paperdoll art already hued by the client. All of it is client
            internals reached by reflection: ok is False if any piece is missing,
            and the frames are then drawn in stone instead."""
            ok = None
            parts = {}
            creatures = False

            @staticmethod
            def find():
                if Bridge.ok is not None:
                    return Bridge.ok
                try:
                    import clr
                    import System
                    from System.Reflection import BindingFlags
                    static = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
                    inst = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
                    loader_t = Client._type("ClassicUO.Assets.ExternalImageLoader")
                    loader = loader_t.GetProperty("Instance", static).GetValue(None, None)
                    p = Bridge.parts
                    p["table"] = loader_t.GetField("_zipNamedTextures", inst).GetValue(loader)
                    p["device"] = loader_t.GetProperty("GraphicsDevice", inst).GetValue(loader, None)
                    p["tex_t"] = Client._type("Microsoft.Xna.Framework.Graphics.Texture2D")
                    p["format"] = System.Enum.Parse(
                        Client._type("Microsoft.Xna.Framework.Graphics.SurfaceFormat"), "Color")
                    p["set_data"] = [m for m in p["tex_t"].GetMethods()
                                     if m.Name == "SetData" and m.IsGenericMethodDefinition
                                     and len(m.GetParameters()) == 1
                                     ][0].MakeGenericMethod(clr.GetClrType(System.UInt32))
                    game = Client._type("ClassicUO.Client").GetProperty("Game", static).GetValue(None, None)
                    p["uo"] = instance_member(game, "UO")
                    p["gumps"] = instance_member(p["uo"], "Gumps")
                    p["hued"] = p["gumps"].GetType().GetMethod("GetHuedGumpPixels")
                    # the hop to the game thread is the host's (Client.on_main_ex): one
                    # tested path for every module, nothing more to look up here
                    Bridge.ok = all(p[k] is not None for k in ("table", "device", "tex_t", "gumps",
                                                                  "hued"))
                except Exception:
                    Bridge.ok = False
                if Bridge.ok:
                    Bridge.creatures = bool(safe(Bridge.find_creatures, False))
                return Bridge.ok

            @staticmethod
            def find_creatures():
                """The pieces for creature pictures: the animation cache, the world's
                mobile list, the hue table and the texture reader. The frame lookup
                returns a Span (which scripts can't receive), so a tiny method is
                emitted that calls it and hands back one frame as a plain struct."""
                import clr
                import System
                from System.Reflection import BindingFlags
                from System.Reflection.Emit import DynamicMethod, OpCodes
                p = Bridge.parts
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
                anims_t = p["anims"].GetType()
                get_frames = anims_t.GetMethod("GetAnimationFrames")
                sprite_t = Client._type("ClassicUO.Renderer.SpriteInfo")
                span_t = get_frames.ReturnType
                obj_t, u16, u8, i32 = (clr.GetClrType(System.Object), clr.GetClrType(System.UInt16),
                                       clr.GetClrType(System.Byte), clr.GetClrType(System.Int32))
                dm = DynamicMethod("vauf_frame", obj_t, System.Array[System.Type](
                    [anims_t, u16, u8, u8, i32, clr.GetClrType(System.Array[System.UInt16])]), obj_t.Module, True)
                il = dm.GetILGenerator()
                span = il.DeclareLocal(span_t)
                hue = il.DeclareLocal(u16)
                uop = il.DeclareLocal(clr.GetClrType(System.Boolean))
                none = il.DefineLabel()
                for op in (OpCodes.Ldarg_0, OpCodes.Ldarg_1, OpCodes.Ldarg_2, OpCodes.Ldarg_3):
                    il.Emit(op)
                il.Emit(OpCodes.Ldloca_S, hue)
                il.Emit(OpCodes.Ldloca_S, uop)
                il.Emit(OpCodes.Ldc_I4_0)
                il.Emit(OpCodes.Ldc_I4_0)
                il.Emit(OpCodes.Callvirt, get_frames)
                il.Emit(OpCodes.Stloc, span)
                il.Emit(OpCodes.Ldloca_S, span)
                il.Emit(OpCodes.Call, span_t.GetProperty("Length").GetGetMethod())
                il.Emit(OpCodes.Ldarg_S, System.Byte(4))
                il.Emit(OpCodes.Ble, none)                       # no such frame -> null
                il.Emit(OpCodes.Ldarg_S, System.Byte(5))
                il.Emit(OpCodes.Ldc_I4_0)
                il.Emit(OpCodes.Ldloc, hue)
                il.Emit(OpCodes.Stelem_I2)                       # hue from the data index
                il.Emit(OpCodes.Ldloca_S, span)
                il.Emit(OpCodes.Ldarg_S, System.Byte(4))
                il.Emit(OpCodes.Call, span_t.GetMethod("get_Item"))
                il.Emit(OpCodes.Ldobj, sprite_t)
                il.Emit(OpCodes.Box, sprite_t)
                il.Emit(OpCodes.Ret)
                il.MarkLabel(none)
                il.Emit(OpCodes.Ldnull)
                il.Emit(OpCodes.Ret)
                p["frame"] = dm
                return all(p[k] is not None for k in ("anims", "hues", "hue_color", "world",
                                                       "get_entity", "group_for", "get_data"))

            @staticmethod
            def creature_pixels(serial):
                """The standing frame of a creature as it looks in the world:
                (pixels, width, height, hue ramp or None, partial hue) or None; the
                hue is put on by hue_steps, off the game thread. Call on the game
                thread."""
                import System
                p = Bridge.parts
                mob = p["get_entity"].Invoke(p["world"], System.Array[System.Object]([System.UInt32(serial)]))
                if mob is None:
                    return None
                graphic = int(mob.GetGraphicForAnimation())
                group = int(p["group_for"].Invoke(None, System.Array[System.Object]([mob, System.UInt16(0), True])))
                direction = int(mob.GetDirectionForAnimation()) & 0x7F
                hue_box = System.Array[System.UInt16]([System.UInt16(0)])
                sprite = p["frame"].Invoke(None, System.Array[System.Object](
                    [p["anims"], System.UInt16(graphic), System.Byte(group), System.Byte(direction),
                     0, hue_box]))
                if sprite is None or sprite.Texture is None:
                    return None
                uv = sprite.UV
                w, h = int(uv.Width), int(uv.Height)
                if w <= 0 or h <= 0:
                    return None
                raw = System.Array[System.UInt32](w * h)
                p["get_data"].Invoke(sprite.Texture, System.Array[System.Object]([0, uv, raw, 0, w * h]))
                hue = int(mob.Hue)
                partial = (hue & 0x8000) != 0
                hue &= 0x7FFF
                if hue == 0:
                    hue = int(hue_box[0])
                    partial = False
                ramp = None
                if hue:
                    ramp = [int(p["hue_color"].Invoke(p["hues"], System.Array[System.Object](
                        [System.UInt16(i), System.UInt16(hue)]))) & 0xFFFFFF for i in range(32)]
                return raw, w, h, ramp, partial

            @staticmethod
            def on_main(fn):
                """Run fn on the game thread (textures must be made there) and wait:
                the host's hop (Client.on_main_ex). Already there (this module's
                tick runs on it): run in place. fn's error is raised here."""
                how, value = Client.on_main_ex(fn)
                if how == "ok":
                    return value
                if how == "err" and isinstance(Client.exc, Exception):
                    raise Client.exc
                raise Exception(Client.error or "can't reach the game thread")

            @staticmethod
            def gump_pixels(ids, hue, partial):
                """Hued RGBA pixels of the first gump id the client has art for:
                (pixels, width, height) or None. Call on the game thread."""
                import System
                for gid in ids:
                    args = System.Array[System.Object]([System.UInt32(gid), System.UInt16(hue & 0xFFFF),
                                                        bool(partial), None])
                    px = Bridge.parts["hued"].Invoke(Bridge.parts["gumps"], args)
                    bounds = args[3]
                    if px is not None and len(px) and int(bounds.Width) > 0:
                        return px, int(bounds.Width), int(bounds.Height)   # converted later, off the game thread
                return None

            @staticmethod
            def put_texture(name, w, h, pixels):
                """Make a texture from RGBA pixels and file it under name (replacing,
                and freeing, any older one). Call on the game thread."""
                import System
                p = Bridge.parts
                tex = System.Activator.CreateInstance(p["tex_t"], System.Array[System.Object](
                    [p["device"], w, h, False, p["format"]]))
                p["set_data"].Invoke(tex, System.Array[System.Object](
                    [System.Array[System.UInt32](pixels)]))
                old = p["table"][name] if p["table"].ContainsKey(name) else None
                p["table"][name] = tex
                if old is not None:
                    old.Dispose()
                st["textures"].add(name)

            @staticmethod
            def drop_textures(names):
                """Remove and free this module's textures. Call on the game thread."""
                table = Bridge.parts["table"]
                for name in names:
                    if table.ContainsKey(name):
                        tex = table[name]
                        table.Remove(name)
                        safe(lambda: tex.Dispose())


        def mute(ctrl):
            """Clicks go through ctrl (to the frame's click catcher)."""
            safe(lambda: ctrl.SetAcceptMouseInput(False))
            return ctrl


        def texture_control(name, x, y, w, h):
            t = G.LegionTextureControl(name, w, h)
            t.SetRect(x, y, w, h)
            return mute(t)


        # ---------- frame art, drawn pixel by pixel ----------
        def _cov(d, s):
            """Pixel coverage for a signed distance d (art pixels, < 0 inside)."""
            v = 0.5 - d * s
            return 0.0 if v <= 0 else (1.0 if v >= 1 else v)


        def _rr(u, v, box):
            """Signed distance to a rounded rectangle (x0, y0, x1, y1, radius)."""
            x0, y0, x1, y1, r = box
            qx = abs(u - (x0 + x1) * 0.5) - ((x1 - x0) * 0.5 - r)
            qy = abs(v - (y0 + y1) * 0.5) - ((y1 - y0) * 0.5 - r)
            ox = qx if qx > 0 else 0.0
            oy = qy if qy > 0 else 0.0
            inside = qx if qx > qy else qy
            return math.sqrt(ox * ox + oy * oy) + (inside if inside < 0 else 0.0) - r


        def _smooth(a, b, x):
            t = (x - a) / (b - a)
            t = 0.0 if t < 0 else (1.0 if t > 1 else t)
            return t * t * (3 - 2 * t)


        def _metal(v):
            c = 132.0 - 62.0 * min(1.0, max(0.0, (v - 43.0) / 107.0))
            return (c, c, c + 6.0)


        def _tire(dx, dy, r):
            cosd = (dx + dy) / r * SQRT_HALF                    # towards lower right
            f = min(1.0, max(0.0, (cosd + 0.71) / 1.42))
            t = min(1.0, max(0.0, (r - 67.0) / 11.5))
            dark = 44.0 * (t ** 1.2) * f
            return (128.0 - dark, 128.0 - dark, 134.0 - dark)


        def _gold(dx, dy, r):
            cosd = -(dx + dy) / r * SQRT_HALF                   # towards upper left
            t = min(1.0, max(0.0, (r - 56.0) / 4.0))
            delta = t * (-42.0 + 57.0 * _smooth(-0.3, 0.75, cosd))
            return (min(255.0, 234.0 + delta), min(255.0, 203.0 + delta), min(255.0, 91.0 + delta * 0.65))


        def _over(acc, rgb, a):
            """Paint a colour with coverage a over a premultiplied pixel."""
            if a <= 0:
                return
            k = 1.0 - a
            acc[0] = rgb[0] * a + acc[0] * k
            acc[1] = rgb[1] * a + acc[1] * k
            acc[2] = rgb[2] * a + acc[2] * k
            acc[3] = a + acc[3] * k


        def _erase(acc, a):
            k = 1.0 - a
            acc[0] *= k
            acc[1] *= k
            acc[2] *= k
            acc[3] *= k


        def frame_pixel(u, v, s):
            """Premultiplied RGBA (0-255 colour, 0-1 alpha) of the player frame at
            art point (u, v), drawn s display pixels per art pixel."""
            acc = [0.0, 0.0, 0.0, 0.0]
            if 140 <= u and 38 <= v <= 156:                      # the bar panel
                _over(acc, OUTLINE_RGB, _cov(_rr(u, v, PANEL), s))
                if acc[3] > 0:
                    _over(acc, _metal(v), _cov(_rr(u, v, METAL), s))
                    _over(acc, INNER_RGB, _cov(_rr(u, v, INNER), s))
                    hole = _cov(_rr(u, v, HOLES), s)
                    if hole > 0:
                        _erase(acc, hole)
                        for y0, y1 in SEPARATORS:
                            band = min(v - y0, y1 - v)
                            if band > -1.5:
                                _over(acc, _metal(v), hole * _cov(-band, s))
                    for rx, ry, rgb in RIVETS:
                        if abs(u - rx) < 4 and abs(v - ry) < 4:
                            d = math.sqrt((u - rx) ** 2 + (v - ry) ** 2)
                            _over(acc, (40, 40, 44), _cov(d - 2.6, s))
                            _over(acc, rgb, _cov(d - 1.6, s))
            dx, dy = u - RING_C[0], v - RING_C[1]
            r = math.sqrt(dx * dx + dy * dy)
            if r < RING[0][0] + 2:                               # the ring, outside in
                for radius, color in RING:
                    a = _cov(r - radius, s)
                    if a <= 0:
                        continue
                    if color == "tire":
                        color = _tire(dx, dy, max(r, 0.01))
                    elif color == "gold":
                        color = _gold(dx, dy, max(r, 0.01))
                    _over(acc, color, a)
                _erase(acc, _cov(r - HOLE_R, s))
            return acc


        def pack(acc):
            """Premultiplied RGBA floats -> the RGBA8888 uint a texture takes."""
            a = acc[3]
            if a <= 0.002:
                return 0
            return (int(acc[0] + 0.5) | (int(acc[1] + 0.5) << 8) | (int(acc[2] + 0.5) << 16) |
                    (int(a * 255 + 0.5) << 24))


        def draw_frame(s):
            """A generator: None after each row, then (width, height, player
            pixels, target pixels) of the frame at scale s."""
            w, h = int(ART_W * s), int(ART_H * s)
            inv = 1.0 / s
            player = [0] * (w * h)
            for y in range(h):
                v = (y + 0.5) * inv
                row = y * w
                for x in range(w):
                    player[row + x] = pack(frame_pixel((x + 0.5) * inv, v, s))
                yield None
            target = []
            for y in range(h):
                target.extend(player[y * w:(y + 1) * w][::-1])
            yield w, h, player, target


        def draw_ring(s, rgb):
            """Notoriety-coloured band over the ring's light line. A generator:
            None now and then, then (size, pixels)."""
            outer = NOTO_RING[1] + 1
            size = int(math.ceil(2 * outer * s))
            half = size / 2.0
            pixels = [0] * (size * size)
            for y in range(size):
                if y % 4 == 3:
                    yield None
                for x in range(size):
                    r = math.sqrt((x + 0.5 - half) ** 2 + (y + 0.5 - half) ** 2) / s
                    a = min(_cov(r - NOTO_RING[1], s), _cov(NOTO_RING[0] - r, s))
                    if a > 0:
                        pixels[y * size + x] = pack([rgb[0] * a, rgb[1] * a, rgb[2] * a, a])
            yield size, pixels


        def art_names(s):
            tag = int(round(s * 100))
            return {"player": "%sframe_player_%d" % (TEX_PREFIX, tag),
                    "target": "%sframe_target_%d" % (TEX_PREFIX, tag),
                    "blank": "%ssnap_blank_%d" % (TEX_PREFIX, tag),
                    "strip": "%sframe_strip_%d" % (TEX_PREFIX, tag)}


        def art_steps(s):
            """Draw the frame art for scale s (once per size; the frames and the
            party frames may each have their own size): about a second of work in
            IronPython, only on start and size changes. A generator run by
            thread_tick, a slice at a time, on the script's own thread (never in
            the game's frame): None between slices, then the upload, a function
            to run on the game thread."""
            names = art_names(s)
            got = None
            for got in draw_frame(s):
                if got is None:
                    yield None
            w, h, player, target = got
            # (2.6.82) the status strip is no longer drawn: nothing shows it (2.6.72)
            size = snap_size(s)
            blank = [pack([SNAP_BG[0], SNAP_BG[1], SNAP_BG[2], 1.0])] * (size * size)
            for got in draw_ring(s, NO_NOTO):           # the plain ring every frame starts with
                if got is None:
                    yield None
            rsize, ring = got
            ring_name = noto_name_of(NO_NOTO, s)

            def upload():
                Bridge.put_texture(names["player"], w, h, player)
                Bridge.put_texture(names["target"], w, h, target)
                Bridge.put_texture(names["blank"], size, size, blank)
                Bridge.put_texture(ring_name, rsize, rsize, ring)
            yield upload


        def want_art(s):
            """True when the frame art for scale s is ready, False if it can't be
            made (stone frames then), None while thread_tick is drawing it."""
            if s in st["art_scales"]:
                return True
            if s in st["art_failed"]:
                return False
            if not any(j["kind"] == "art" and j["s"] == s for j in st["art_jobs"]):
                st["art_jobs"].append({"kind": "art", "s": s, "gen": art_steps(s)})
            return None


        def scales_in_use():
            """The sizes the settings ask for: every frame's, and the party's if set
            (a frame fitted to its zone counts at that size: fitst)."""
            out = set([settings["scale"] / 100.0])
            if settings["pscale_on"]:
                out.add(settings["pscale"] / 100.0)
            for v in fitst.values():
                if v is not None:
                    out.add(v / 100.0)
            return out


        def prune_art():
            """Free the art of sizes no frame uses any more (after a size change)."""
            keep = scales_in_use()
            keep.update(fr.get("s") for fr in frames.values() if fr.get("art"))
            gone = [s for s in st["art_scales"] if s not in keep]
            if not gone:
                return
            tags = set(str(int(round(s * 100))) for s in gone)
            kinds = tuple(TEX_PREFIX + k for k in ("frame_", "noto_", "snap_blank_"))
            names = [n for n in st["textures"]
                     if n.startswith(kinds) and n.rsplit("_", 1)[-1] in tags]
            for s in gone:
                st["art_scales"].discard(s)
            for n in names:
                st["textures"].discard(n)
            if names:
                safe(lambda: Bridge.on_main(lambda: Bridge.drop_textures(names)))


        def noto_name_of(rgb, s):
            return "%snoto_%d_%d_%d_%d" % (TEX_PREFIX, rgb[0], rgb[1], rgb[2], int(round(s * 100)))


        def ring_steps(rgb, s, name):
            """A notoriety ring drawn by thread_tick: None between slices, then the upload."""
            got = None
            for got in draw_ring(s, rgb):
                if got is None:
                    yield None
            size, pixels = got
            yield lambda: Bridge.put_texture(name, size, size, pixels)


        def noto_texture(rgb, s):
            """Name of the ring texture in this colour and size; None while
            thread_tick is still drawing it (the frames are updated once it's in)."""
            name = noto_name_of(rgb, s)
            if name in st["textures"]:
                return name
            if name not in st["art_failed"] and \
                    not any(j.get("name") == name for j in st["art_jobs"]):
                st["art_jobs"].append({"kind": "noto", "s": s, "name": name,
                                       "gen": ring_steps(rgb, s, name)})
            return None


        def art_work(budget):
            """thread_tick: a slice of the frame art / rings being drawn (sizes no
            longer used are dropped). True while there is more to do."""
            jobs = st["art_jobs"]
            if not jobs:
                return False
            keep = scales_in_use()
            keep.update(fr.get("s") for fr in frames.values())
            jobs[:] = [j for j in jobs if j["s"] in keep]
            deadline = time.time() + budget
            while jobs:
                j = jobs[0]
                try:
                    r = next(j["gen"])
                except Exception:
                    r = False                             # broken: give up on this one
                if r is None:
                    if time.time() >= deadline:
                        return True
                    continue
                jobs.pop(0)
                ok = r is not False and bool(safe(lambda: Bridge.on_main(r) or True, False))
                if j["kind"] == "art":
                    (st["art_scales"] if ok else st["art_failed"]).add(j["s"])
                    st["art_dirty"] = True
                elif not ok:
                    st["art_failed"].add(j["name"])
                else:
                    for fr in frames.values():            # show the new colour now
                        fr["last"] = None
                if time.time() >= deadline:
                    break
            return bool(jobs)


        # ---------- snapshot pictures ----------
        def snap_size(s):
            """Snapshot side in pixels: covers the hole, edges hidden under the ring."""
            return int(math.ceil(2 * (HOLE_R + 2) * s))


        def snap_px():
            """Side of the pictures: drawn for the biggest frame size in use; a
            smaller frame shows the same picture shrunk to fit."""
            return snap_size(max(scales_in_use()))


        def item_details(item):
            """(anim id, partial hue, is container) of a worn item, cached by graphic."""
            graphic = int(safe(lambda: item.Graphic, 0) or 0)
            info = item_info.get(graphic)
            if info is None:
                data = safe(lambda: item.GetItemData())
                info = (int(safe(lambda: data.AnimID, 0) or 0),
                        bool(safe(lambda: data.IsPartialHue, False)),
                        bool(safe(lambda: data.IsContainer, False)))
                if data is not None:          # a failed read is not kept: that layer is tried again
                    item_info[graphic] = info
            return info


        def covered(layer, worn):
            """The client's rules for robes hiding what is under them."""
            robe = worn.get("robe", (0, 0))[0]
            if layer == "tunic":
                return worn.get("tunic", (0, 0))[0] == 0x0238 and robe and robe not in OPEN_ROBES
            if layer == "arms":
                return bool(robe) and robe not in OPEN_ROBES
            if layer == "torso":
                if robe and robe not in OPEN_ROBES:
                    return True
                tunic = worn.get("tunic", (0, 0))[0]
                return bool(tunic) and tunic not in (0x1541, 0x1542) and \
                    worn.get("torso", (0, 0))[0] in (0x782A, 0x782B)
            if layer in ("helmet", "hair") and robe:       # hooded robes
                if robe > 0x3173:
                    return robe in (0x4B9D, 0x7816)
                if robe <= 0x2687:
                    return robe >= 0x2683 or 0x204E <= robe <= 0x204F
                return robe in (0x2FB9, 0x3173)
            return False


        def read_paperdoll(serial):
            """What the client's paperdoll would draw for the head and shoulders:
            {"body", "pieces": ((gump ids to try, hue, partial hue), ...)}.
            body 0 for creatures (no paperdoll); None if the client can't see them."""
            m = find_mobile(serial)
            if m is None:
                return None
            graphic = int(safe(lambda: m.Graphic, 0) or 0)
            body = PAPERDOLL_BODY.get(graphic)
            if body is None:
                return {"body": 0, "pieces": ()}
            hue = GM_BODY_HUE if graphic == GM_BODY else (int(safe(lambda: m.Hue, 0) or 0) & 0x3FFF)
            female = graphic in FEMALE_BODIES
            worn, details = {}, {}
            for layer in LAYERS:                  # (2.6.82) plain reads: no lambda per layer
                try:
                    it = API.FindLayer(layer, serial)
                except Exception:
                    it = None
                if it is not None:
                    try:
                        ig = int(it.Graphic or 0)
                    except Exception:
                        ig = 0
                    try:
                        ih = int(it.Hue or 0) & 0x3FFF
                    except Exception:
                        ih = 0
                    worn[layer] = (ig, ih)
                    details[layer] = item_details(it)
            order = LAYERS
            if "cloak" in worn:
                if worn.get("robe", (0, 0))[0] in PARROT_ROBES:
                    order = LAYERS_PARROT
                elif details["cloak"][2]:
                    order = LAYERS_QUIVER
            if worn.get("arms", (0, 0))[0] in PLATE_ARMS:
                order = tuple({"arms": "torso", "torso": "arms"}.get(l, l) for l in order)
            pieces = [((body,), hue, True)]
            for layer in order:
                if layer not in worn or covered(layer, worn):
                    continue
                anim, partial, _container = details[layer]
                if not anim:
                    continue
                if anim == 0x03CA and graphic in (0x02B6, 0x02B7):     # dead gargoyle shroud
                    anim = 0x0223
                ids = (anim + FEMALE_GUMP, anim + MALE_GUMP) if female else \
                    (anim + MALE_GUMP, anim + FEMALE_GUMP)
                pieces.append((tuple(i for i in ids if i <= 0xFFFF), worn[layer][1], partial))
            return {"body": body, "pieces": tuple(pieces)}


        def fetch_layers(doll):
            """Hued pixels of each paperdoll piece: [(pixels, w, h)], bottom first."""
            def read():
                out = []
                for ids, hue, partial in doll["pieces"]:
                    got = Bridge.gump_pixels(ids, hue, partial)
                    if got is not None:
                        out.append(got)
                return out
            return Bridge.on_main(read) or []


        def figure_bounds_steps(layers):
            """(left, top, right) of the drawn figure: the topmost opaque row and the
            widest extent of the upper part, over every layer. A generator: yields
            None now and then (slow loops in IronPython), the answer last."""
            top, left, right = None, None, None
            for px, w, h in layers:
                for y in range(h):
                    if y % 24 == 23:
                        yield None
                    if top is not None and y > top + FIGURE_DEPTH:
                        break
                    row = y * w
                    first = -1
                    for x in range(w):
                        if (px[row + x] >> 24) & 0xFF > 127:
                            first = x
                            break
                    if first < 0:
                        continue
                    last = first
                    for x in range(w - 1, first, -1):
                        if (px[row + x] >> 24) & 0xFF > 127:
                            last = x
                            break
                    if top is None or y < top:
                        top = y
                    left = first if left is None else min(left, first)
                    right = last if right is None else max(right, last)
            yield (left, top, right)


        def crop_box(body, layers, bounds):
            """Square (x0, y0, size) of the art to show. People: the head against the
            top of the circle, the figure centred, SNAP_DEPTH art pixels tall at 100%
            zoom. Creatures (body 0): the whole frame, fitted and centred."""
            if not body and layers:
                w, h = layers[0][1:]
                size = max(w, h) * 1.08 * 100.0 / settings["pzoom"]
                return (w - size) / 2.0 + settings["pdx"], (h - size) / 2.0 + settings["pdy"], size
            size = SNAP_DEPTH * 100.0 / settings["pzoom"]
            if bounds is None or bounds[1] is None:
                cx, cy = CROP.get(body, CROP_DEFAULT)[:2]
                x0, y0 = cx - size / 2.0, cy - size / 2.0
            else:
                left, top, right = bounds
                x0 = (left + right + 1) / 2.0 - size / 2.0
                y0 = top - HEAD_GAP
            return x0 + settings["pdx"], y0 + settings["pdy"], size


        def compose_steps(raw_layers, body, out):
            """Picture of the paperdoll's upper body, out x out pixels, on the black
            backdrop: the layers stacked in the crop box, then scaled down with
            2 x 2 samples per pixel. A generator: yields None between slices of
            work and the pixels last, so one picture is spread over many ticks
            instead of stalling the loop for hundreds of ms."""
            layers = []
            keep = isinstance(raw_layers, list)
            for i, (px, w, h) in enumerate(raw_layers):   # .NET arrays -> lists, one per slice
                if isinstance(px, list):
                    layers.append((px, w, h))
                else:
                    conv = (list(px), w, h)
                    layers.append(conv)
                    if keep:
                        # 2.6.81: converted once; a kept copy (the settings preview's
                        # layers) isn't converted again on every redraw
                        raw_layers[i] = conv
                yield None
            bounds = None
            if body and layers:
                for r in figure_bounds_steps(layers):
                    if r is None:
                        yield None
                    else:
                        bounds = r
            x0, y0, size = crop_box(body, layers, bounds)
            side = int(math.ceil(size)) + 1
            ix0, iy0 = int(math.floor(x0)), int(math.floor(y0))
            bg = SNAP_BG
            buf = [bg] * (side * side)                    # the crop, at the art's own size
            for px, w, h in layers:
                for y in range(side):
                    if y % 16 == 15:
                        yield None
                    sy = iy0 + y
                    if sy < 0 or sy >= h:
                        continue
                    src = sy * w
                    dst = y * side
                    for x in range(side):
                        sx = ix0 + x
                        if 0 <= sx < w:
                            p = px[src + sx]
                            if (p >> 24) & 0xFF > 127:        # gump art is on/off alpha
                                buf[dst + x] = (p & 0xFF, (p >> 8) & 0xFF, (p >> 16) & 0xFF)
            step = size / float(out)
            offs = (0.25, 0.75)
            pixels = [0] * (out * out)
            for oy in range(out):
                if oy % 8 == 7:
                    yield None
                for ox in range(out):
                    r = g = b = 0
                    for fy in offs:
                        yy = int(y0 + (oy + fy) * step) - iy0
                        yy = 0 if yy < 0 else (side - 1 if yy >= side else yy)
                        for fx in offs:
                            xx = int(x0 + (ox + fx) * step) - ix0
                            xx = 0 if xx < 0 else (side - 1 if xx >= side else xx)
                            c = buf[yy * side + xx]
                            r += c[0]
                            g += c[1]
                            b += c[2]
                    pixels[oy * out + ox] = ((r >> 2) | ((g >> 2) << 8) | ((b >> 2) << 16) |
                                             (0xFF << 24))
            yield pixels


        def compose_snapshot(layers, body, out):
            """compose_steps run in one go (the settings-page preview)."""
            for r in compose_steps(layers, body, out):
                if r is not None:
                    return r


        def snap_name(serial):
            return "%ssnap_%d" % (TEX_PREFIX, serial)


        def want_snapshot(serial):
            """Queue a picture of this character if there isn't one yet."""
            if serial and (serial not in st["snaps"] or serial in st["stale"]) and \
                    not any(q[0] == serial for q in st["snap_queue"]):
                job = st.get("snap_job")
                if job is not None and job.get("serial") == serial:
                    return                                # (2.6.81) being made right now
                st["snap_queue"].append((serial, 0.0))


        def hue_steps(got, job):
            """A creature's picture: its hue put on (the slow per-pixel part, so off
            the game thread), then compose_steps. Same yields as compose_steps."""
            raw, w, h, ramp, partial = got
            pixels = list(raw)
            yield None
            if ramp:
                for i, px in enumerate(pixels):
                    if i % 4096 == 4095:
                        yield None
                    a = px & 0xFF000000
                    if not a:
                        continue
                    r, g, b = px & 0xFF, (px >> 8) & 0xFF, (px >> 16) & 0xFF
                    if partial and (r != g or r != b):
                        continue
                    pixels[i] = ramp[r >> 3] | a
            job["layers"] = [(pixels, w, h)]
            for r in compose_steps(job["layers"], 0, job["size"]):
                yield r


        def snapshot_work(now, budget=SNAP_BUDGET):
            """A slice of the picture being made. True while one is in progress.
            Run by thread_tick, on the script's own thread (not in the game's frame)."""
            job = st.get("snap_job")
            if job is None:
                return False
            deadline = now + budget
            while st.get("snap_job") is job:             # the loop ends by clearing snap_job
                try:
                    r = next(job["gen"])
                except StopIteration:
                    st["snap_job"] = None
                    return False
                except Exception:
                    st["snap_job"] = None
                    if not any(q[0] == job["serial"] for q in st["snap_queue"]):   # (2.6.81) once
                        st["snap_queue"].append((job["serial"], now + SNAP_RETRY))
                    return False
                if r is not None:                         # the pixels: hand them to the client
                    st["snap_job"] = None
                    serial, name, size = job["serial"], snap_name(job["serial"]), job["size"]
                    if safe(lambda: Bridge.on_main(lambda: Bridge.put_texture(name, size, size, r))
                            or True, False):
                        st["snaps"][serial] = {"name": name, "creature": False}
                        if serial == st["me"] and page["c"] is not None:
                            # the settings preview re-crops these; kept only while the
                            # page is open (the art of every layer: a megabyte or two)
                            page["layers"] = (job["layers"], job["body"])
                        mark_frames(serial)
                    return False
                if time.time() >= deadline:
                    return True


        def take_next_snapshot(now):
            """Pictures are made one at a time: reading the paperdoll and its art
            happens here, in the game's frame (no waits); the rest is a job that
            snapshot_work advances from thread_tick, a slice at a time."""
            if st.get("snap_job") is not None:
                return
            for i, (serial, due) in enumerate(st["snap_queue"]):
                if due <= now:
                    del st["snap_queue"][i]
                    break
            else:
                return
            if serial in st["snaps"] and serial not in st["stale"]:
                return                                    # (2.6.81) made meanwhile: not twice
            doll = read_paperdoll(serial)
            if doll is None:                              # out of sight: try again later
                st["snap_queue"].append((serial, now + SNAP_RETRY))
                return
            st["stale"].discard(serial)
            size = snap_px()
            if not doll["body"]:                          # a creature: its standing frame
                got = safe(lambda: Bridge.on_main(lambda: Bridge.creature_pixels(serial))) \
                    if Bridge.creatures else None
                if got is None:
                    if Bridge.creatures and st["snap_tries"].get(serial, 0) < 3:
                        st["snap_tries"][serial] = st["snap_tries"].get(serial, 0) + 1
                        st["snap_queue"].append((serial, now + SNAP_RETRY))   # art may still be loading
                        return
                    st["snaps"][serial] = {"name": None, "creature": True}
                    mark_frames(serial)
                    return
                job = {"serial": serial, "size": size, "layers": None, "body": 0}
                job["gen"] = hue_steps(got, job)
                st["snap_job"] = job                      # thread_tick takes it from here
                return
            layers, body = safe(lambda: fetch_layers(doll), []), doll["body"]
            if not layers:
                st["snap_queue"].append((serial, now + SNAP_RETRY))
                return
            st["snap_job"] = {"gen": compose_steps(layers, body, size), "serial": serial,
                              "size": size, "layers": layers, "body": body}


        def mark_frames(serial):
            for key, fr in frames.items():
                if frame_serial(key) == serial:
                    fr["last"] = None


        def retake_all():
            """Take every picture again (crop, size or gear changed). The old picture
            stays up until its replacement is ready: it is swapped in by name."""
            st["stale"] = set(st["snaps"])
            for key in frames:
                want_snapshot(frame_serial(key))


        # ---------- forgetting people no frame shows ----------
        #  Every target gets a picture (a texture in the client), a name and maybe a
        #  queued retry. Without pruning, all of them stayed for the whole session:
        #  hundreds of textures after a long fight, and out-of-sight targets retried
        #  every SNAP_RETRY forever. Now only the people on a frame (and the last
        #  SNAP_KEEP shown, so a re-target is instant) are kept.
        SNAP_KEEP = 8                      # pictures kept of people no frame shows now
        PRUNE_EVERY = 5.0                  # seconds between looks


        def note_shown(serial):
            """serial was just put on a frame: the most recent of the recent list."""
            rec = st["recent"]
            if not serial or (rec and rec[-1] == serial):
                return
            if serial in rec:
                rec.remove(serial)
            rec.append(serial)
            if len(rec) > 4 * SNAP_KEEP:
                del rec[:-SNAP_KEEP]


        def prune_people():
            """Drop the pictures (and their textures), names, retry counts and
            queued pictures of everyone not on a frame, tracked, in your party or
            among the last SNAP_KEEP shown."""
            keep = set(frame_serial(k) for k in frames)
            keep.update(t["serial"] for t in tracked)
            keep.update(st["party"])
            keep.update(st["recent"][-SNAP_KEEP:])
            keep.add(st["me"])
            in_use = set(fr.get("snap") for fr in frames.values())
            snaps = st["snaps"]
            names = []
            for serial in [s for s in snaps if s not in keep]:
                name = snaps[serial].get("name")
                if name and name in in_use:              # still on a frame's picture
                    continue
                del snaps[serial]
                if name:
                    names.append(name)
                    st["textures"].discard(name)
            for d in (st["names"], st["snap_tries"]):
                for serial in [s for s in d if s not in keep]:
                    del d[serial]
            st["stale"] = set(s for s in st["stale"] if s in snaps)
            q = st["snap_queue"]
            if any(e[0] not in keep for e in q):
                q[:] = [e for e in q if e[0] in keep]
            if names and st["art"]:
                safe(lambda: Bridge.on_main(lambda: Bridge.drop_textures(names)))


        # ---------- the frames ----------
        def frame_style(key):
            return "target" if key == "target" else "player"


        def frame_serial(key):
            if key == "player":
                return st["me"]
            if key == "target":
                return st["target"]
            return int(key[1:])


        def is_party_frame(key):
            """A tracked frame of someone in your party right now."""
            return key[:1] == "m" and key[1:].isdigit() and int(key[1:]) in st["party"]


        # ---------- the zone fit (2.6.55) ----------
        #  The layout tells a frame slotted in a zone the zone's size (its "fit"
        #  hook, on the client thread): the frame's scale is overridden, in
        #  fitst, to be as wide as the zone (mode "w") or no wider than it
        #  ("s"); the saved Scale setting is never touched. sync_frames sees the
        #  change (fr["s"] differs) and rebuilds the frame on the module's tick.
        fitst = {"player": None, "target": None}      # frame key -> scale %, or None
        # (2.6.60) A frame slotted in a zone is a window the size of its slot
        # (hooks "exact": the layout leaves the size to us): the stone frame and
        # a black section fill the slot behind the art, like the other zone
        # windows, and the art sits inside at its circle's side (the player
        # frame's left edge, the mirrored target frame's right edge), so two
        # frames in zones side by side mirror each other.
        fitbox = {"player": None, "target": None}     # frame key -> its slot (w, h), or None
        ZONE_PAD = Kit.MARGIN + 2                      # stone round the black, and 2 px in it


        def frame_scale(key):
            """Scale of a frame: its zone's fit when it has one, the party scale
            for party members if it's on, the frame scale for everyone else."""
            fit = fitst.get(key)
            if fit is not None:
                return fit / 100.0
            if settings["pscale_on"] and is_party_frame(key):
                return settings["pscale"] / 100.0
            return settings["scale"] / 100.0


        def frame_fit(key):
            """The layout's "fit" hook for frame `key` (see the mother's
            Kit.dock_hooks): fn(w, h, mode), (None, None, None) when freed."""
            def fit(w, h, mode):
                want = None
                box = None
                if w and h:                       # (2.6.56) as big as fits its slot both ways,
                    box = (int(w), int(h))        # (2.6.60) inside the background's stone
                    iw, ih = box[0] - 2 * ZONE_PAD, box[1] - 2 * ZONE_PAD
                    pct = int(min(100.0 * float(iw) / ART_W, 100.0 * float(ih) / ART_H))
                    if rides_inside(key):         # (2.6.72) and its piece under the bars
                        # (2.6.73) the piece's own black and stone are hidden inside the
                        # frame: only its rows take room (PIECE_IN), not its whole window
                        pct = min(pct, int(100.0 * (ih - Kit.GAP - PIECE_IN) / PANEL[3]))
                    want = max(SCALE_MIN, min(SCALE_MAX, pct))
                fitbox[key] = box                     # sync_frames rebuilds it: fr["slot"] differs
                if want != fitst.get(key):
                    fitst[key] = want                 # sync_frames rebuilds it: fr["s"] differs
                    st["art_dirty"] = True            # a size no frame uses any more is freed
            return fit


        PIECE_H = 62                      # (2.6.72) Bandages and the Swing Bar (the taller one)
        PIECE_W = 161                     # (2.6.72) ...and their designed width
        PIECE_IN_W = PIECE_W - 2 * Kit.MARGIN   # (2.6.73) its rows' width (PIECE_IN: their height)

        def content_h(s):
            """(2.6.73) Height the art and a riding piece take at scale s: the
            piece under the bars, beside the lower part of the circle."""
            return max(ART_H * s, PANEL[3] * s + Kit.GAP + PIECE_IN)

        def frame_hug(key):
            """(2.6.72) The layout's "hug" hook: (width, height) frame `key`'s window
            wants when the layout gives it a window h px high (a corner zone of the
            centre band is made that wide): the art at the scale frame_fit gives
            for that height, or the piece under its bars when that reaches further,
            and the stone round it. (2.6.73) The height is more than h only when even
            the smallest scale can't hold the piece under the bars: the zone then
            grows down so the piece sits inside the frame's box (0: h is enough)."""
            def hug(h):
                ih = int(h) - 2 * ZONE_PAD
                pct = 100.0 * ih / ART_H
                inside = rides_inside(key)
                if inside:
                    pct = min(pct, 100.0 * (ih - Kit.GAP - PIECE_IN) / PANEL[3])
                s = max(SCALE_MIN, min(SCALE_MAX, int(pct))) / 100.0
                need = max(ART_W * s, PANEL[0] * s + PIECE_IN_W + 4) if inside else ART_W * s
                want_h = 0
                if inside:
                    hh = int(math.ceil(content_h(s))) + 2 * ZONE_PAD + 1
                    if hh > int(h):
                        want_h = hh
                return int(math.ceil(need)) + 2 * ZONE_PAD, want_h
            return hug

        def rides_inside(key):
            """(2.6.72) A piece (Bandages, the Swing Bar) rides on frame `key`, so
            the frame in a zone makes room for it under its bars."""
            for pkey, (fk, order, getter) in PIECES["piece"].items():
                if fk == key and order == 0:
                    return True
            return False


        def frame_box(key, w, h):
            """(W, H, ox, oy, zoned) of frame `key` with art w x h: its window's
            size and where the art sits in it. Slotted in a zone (2.6.60): the
            slot's size (never smaller than the art and the stone), the art at
            its circle's side and centred up and down; else the art alone."""
            box = fitbox.get(key)
            if not box:
                return w, h, 0, 0, False
            W, H = max(box[0], w + 2 * ZONE_PAD), max(box[1], h + 2 * ZONE_PAD)
            ox = ZONE_PAD if frame_style(key) == "player" else W - ZONE_PAD - w
            ch = h
            if rides_inside(key):
                # (2.6.73) the art and the piece under its bars are centred as one
                # block, so the art sits higher and the piece fits inside the box
                ch = max(h, int(math.ceil(content_h(float(h) / ART_H))))
            return W, H, ox, max(ZONE_PAD if ch > h else 0, (H - ch) // 2), True


        def frame_span(key):
            """A getter of frame `key`'s bar panel for the pieces (pieces_anchor):
            (x0, x1, right) in its window's pixels, None while it isn't built."""
            def get():
                fr = frames.get(key)
                if not fr or not fr.get("box"):
                    return None
                ox, _oy, w, _h = fr["box"]
                s = fr["s"]
                lo, hi = int(round(PANEL[0] * s)), int(round(PANEL[2] * s))
                if frame_style(key) == "player":
                    return ox + lo, ox + hi, True
                return ox + w - hi, ox + w - lo, False
            return get


        def frame_inner(key):
            """(2.6.67) A getter for the pieces (pieces_anchor): (pad, W, H, art_y,
            art_h) of frame `key` while it fills a zone, else None."""
            def get():
                fr = frames.get(key)
                if not fr or not fr.get("slot") or not fr.get("box"):
                    return None
                _ox, oy, _w, h = fr["box"]
                W, H = fr["win"]
                # (2.6.72) and the bar panel's bottom (where a piece goes under the bars)
                return ZONE_PAD, W, H, oy, h, oy + int(round(PANEL[3] * fr["s"]))
            return get


        def zone_back(g, W, H, hole):
            """(2.6.67) The zone windows' look (the stone frame and a black section
            filling it) with `hole` (x, y, w, h) left open, so the piece riding
            there (Bandages, the Swing Bar, a window of its own under this one)
            shows and takes its clicks even with this window in front. None: the
            plain look, as Kit.add_window_frame and Kit.add_section draw it."""
            M = Kit.MARGIN
            if hole is None:
                Kit.add_window_frame(g, W, H)
                Kit.add_section(g, M, M, W - 2 * M, H - 2 * M)
                return
            hx, hy, hw, hh = hole
            base = Kit.WINDOW_BG
            s = [Kit.pic_size(base + i) for i in range(9)]
            tl, _t, tr, l, _c, r, bl, _b, br = s
            if any(p[0] <= 0 or p[1] <= 0 for p in s):
                tl = tr = l = r = bl = br = (0, 0)
                cx0, cy0, cx1, cy1 = 0, 0, W, H
            else:
                cx0, cy0, cx1, cy1 = l[0], s[1][1], W - r[0], H - s[7][1]

            def around(tile, x0, y0, x1, y1, alpha=None):
                """Tile the rect (x0, y0)-(x1, y1) less the hole: four bands, no overlap."""
                a0, b0 = max(x0, hx), max(y0, hy)
                a1, b1 = min(x1, hx + hw), min(y1, hy + hh)
                if a0 >= a1 or b0 >= b1:
                    bands = ((x0, y0, x1, y1),)
                else:
                    bands = ((x0, y0, x1, b0), (x0, b1, x1, y1), (x0, b0, a0, b1), (a1, b0, x1, b1))
                for u0, v0, u1, v1 in bands:
                    if u1 > u0 and v1 > v0:
                        if alpha is None:
                            Kit.add_tiled(g, tile, u0, v0, u1 - u0, v1 - v0)
                        else:
                            Kit.add_tiled(g, tile, u0, v0, u1 - u0, v1 - v0, alpha)

            around(base + 4, cx0, cy0, cx1, cy1)
            if cx0 > 0:                          # the edges and corners, whole (the hole is inside)
                Kit.add_tiled(g, base + 1, tl[0], 0, W - tl[0] - tr[0], s[1][1])
                Kit.add_tiled(g, base + 7, bl[0], H - s[7][1], W - bl[0] - br[0], s[7][1])
                Kit.add_tiled(g, base + 3, 0, tl[1], l[0], H - tl[1] - bl[1])
                Kit.add_tiled(g, base + 5, W - r[0], tr[1], r[0], H - tr[1] - br[1])
                Kit.add_pic(g, base + 0, 0, 0)
                Kit.add_pic(g, base + 2, W - tr[0], 0)
                Kit.add_pic(g, base + 6, 0, H - bl[1])
                Kit.add_pic(g, base + 8, W - br[0], H - br[1])
            kw, kh = Kit.pic_size(Kit.CORNER_ART) if Kit.CORNER_ART else (0, 0)
            if kw and kh:
                for kx, ky in ((0, 0), (W - kw, 0), (0, H - kh), (W - kw, H - kh)):
                    if kx < hx + hw and kx + kw > hx and ky < hy + hh and ky + kh > hy:
                        continue                 # never a knot over the piece
                    Kit.add_pic(g, Kit.CORNER_ART, kx, ky)
            around(Kit.SECTION_TILE, M, M, W - M, H - M, Kit.SECTION_ALPHA)


        def _layout_add(key, getter, title, hooks):
            """HOST.layout_add with the hooks (2.6.55), or without them on an older mother."""
            fn = getattr(HOST, "layout_add", None)
            if fn is None:
                return
            try:
                fn(key, getter, title, hooks)
            except TypeError:
                fn(key, getter, title)


        def frame_size(key="player"):
            s = frame_scale(key)
            return s, int(ART_W * s), int(ART_H * s)


        def mirror_x(style, w, x0, x1):
            return (x0, x1) if style == "player" else (w - x1, w - x0)


        def default_pos(key):
            _s, w, h = frame_size(key)
            if key == "player":
                return 60, 420
            if key == "target":
                return 60 + w + 20, 420
            i = [t["serial"] for t in tracked].index(int(key[1:])) if key[1:].isdigit() else 0
            return 60 + (i // 4) * (w + 10), 40 + (i % 4) * (h + 2)


        def follow_or(serial, action):
            """(2.6.81) A button acting on someone (a frame's X, a row's X): Alt+click
            auto-follows them instead (standing rule); a plain click queues action."""
            def h(*a):
                if safe(Follow.alt_held, False):
                    queue(("follow_serial", serial))()
                    return
                queue(action)()
            return h


        def row_click(serial):
            """A row of the OTHERS' FRAMES list: Alt+click auto-follows that character."""
            def handler():
                if safe(Follow.alt_held, False):
                    queue(("follow_serial", serial))()
            return handler

        def frame_clicked(key):
            """Click on a frame: queue a target (or, with Alt held, an auto-follow),
            unless the click ended a drag. Alt is read here, at the click."""
            def handler():
                fr = frames.get(key)
                g = fr and fr.get("g")
                if not g:
                    return
                alt = bool(safe(Follow.alt_held, False))
                # 2.6.81: with "Click a frame to target it" off, a frame click still
                # answers Remove frame's own cursor (and does nothing else)
                removing = not alt and not settings["click"] and st.get("removing")
                if not alt and not settings["click"] and not removing:
                    return
                p = frame_at(fr)
                if p != fr.get("seen") or time.time() < fr.get("drag_until", 0.0):
                    fr["seen"] = p                  # it was dragged: not a click
                    return
                queue(("follow" if alt else ("remove_click" if removing else "click"), key))()
            return handler


        def frame_disposed(key, g):
            """Right-click closed a frame (our own rebuilds are ignored)."""
            def handler(*args):
                fr = frames.get(key)
                if fr is not None and fr.get("g") is g and not st["shutting"]:
                    fr["g"] = None
                    st["queue"].append(("closed", key))
            return handler


        def color_box(g, x, y, w, h, rgb, alpha=1.0):
            box = G.CreateGumpColorBox(alpha, "#%02x%02x%02x" % rgb)
            box.SetRect(x, y, w, h)
            g.Add(mute(box))
            return box


        def add_bars(g, c, rows):
            for row, (rx0, ry0, rx1, ry1) in zip(ROWS, rows):
                for v in (("hits", "poison", "yellow") if row == "hits" else (row,)):
                    pb = G.CreateGumpSimpleProgressBar(rx1 - rx0, ry1 - ry0, BAR_BG, BAR_COLOR[v], 0, 100)
                    pb.SetPos(rx0, ry0)
                    g.Add(mute(pb))
                    c["bar_" + v] = pb


        def build_frame(key):
            old = frames.get(key, {}).get("g")
            s, w, h = frame_size(key)
            style = frame_style(key)
            x, y = st["pos"].get(key) or default_pos(key)
            if Kit.is_open(old):
                x, y = old.GetX(), old.GetY()
            if key in frames:
                frames[key]["g"] = None
            sx = lambda v: int(round(v * s))
            art = bool(st["art"]) and s in st["art_scales"]     # drawn by thread_tick (want_art)
            # (2.6.72) the AR / Wt / Gold strip is gone (the Paperdoll's stats show all
            # three); its saved setting "status" is still read, and ignored
            strip = False
            sh = int(STRIP_H * s)
            W, H, ox, oy, zoned = frame_box(key, w, h)   # (2.6.60) the slot, art inside it
            g = G.CreateGump(True, not settings["lock"])
            x, y = Kit.place(g, x, y, W, H)              # wholly on screen
            c = {}
            # (2.6.72) no hole any more: the frame keeps its black under the piece riding
            # inside it, and the piece draws no background of its own there (pieces_place)
            inhole = None
            if zoned:                                    # the zone windows' look behind the art
                zone_back(g, W, H, inhole)
            cx = ox + (sx(RING_C[0]) if style == "player" else w - sx(RING_C[0]))
            cy = oy + sx(RING_C[1])
            rx0, rx1 = mirror_x(style, w, sx(ART_ROWS_X[0]), sx(ART_ROWS_X[1]))
            rows = [(ox + rx0, oy + sx(y0), ox + rx1, oy + sx(y1)) for y0, y1 in ART_ROWS_Y]
            hole = int(HOLE_R * s)
            names = art_names(s) if art else None        # kept in the frame: set_snapshot reads it
            if art:
                size = snap_size(s)
                c["snap"] = texture_control(names["blank"], cx - size // 2, cy - size // 2, size, size)
                g.Add(c["snap"])                                  # behind the frame's hole
                add_bars(g, c, rows)                              # behind the bar holes
                if strip:                                         # under the ring
                    g.Add(texture_control(names["strip"], ox, oy + sx(STRIP_Y), w, sh))
                g.Add(texture_control(names[style], ox, oy, w, h))
                ring = int(math.ceil(2 * (NOTO_RING[1] + 1) * s))
                c["noto"] = texture_control(noto_name_of(NO_NOTO, s), cx - ring // 2,
                                            cy - ring // 2, ring, ring)   # drawn with the art
                g.Add(c["noto"])
            else:                                                 # stone look
                if not zoned:                                     # (in a zone: the slot's frame)
                    Kit.add_window_frame(g, w, h, corners=False)
                side = 2 * hole
                Kit.add_section(g, cx - hole, cy - hole, side, side, alpha=0.95)
                e = max(2, int(round(3 * s)))
                c["edge"] = [color_box(g, cx - hole, cy - hole, side, e, NO_NOTO),
                             color_box(g, cx - hole, cy + hole - e, side, e, NO_NOTO),
                             color_box(g, cx - hole, cy - hole, e, side, NO_NOTO),
                             color_box(g, cx + hole - e, cy - hole, e, side, NO_NOTO)]
                Kit.add_section(g, rows[0][0] - 4, rows[0][1] - 4, rows[0][2] - rows[0][0] + 8,
                                rows[-1][3] - rows[0][1] + 8, alpha=0.9)
                add_bars(g, c, [(a, b + 1, cc, d - 1) for a, b, cc, d in rows])
                if strip:
                    Kit.add_section(g, ox + sx(STRIP_TEXT_X[0]) - 4, oy + sx(STRIP_Y + STRIP_INNER[1]),
                                    sx(STRIP_INNER[2]) - sx(STRIP_TEXT_X[0]) + 4,
                                    sx(STRIP_INNER[3]) - sx(STRIP_INNER[1]), alpha=0.9)
            c["strip"] = color_box(g, cx - 22, cy + int(hole * 0.42), 44, LABEL_H + 4, (0, 0, 0), 0.65)
            safe(lambda: setattr(c["strip"], "IsVisible", False))
            tip = None if key == "player" else \
                ("Click: set them as your target. Alt+click: auto-follow (again to stop)" if settings["click"]
                 else "Alt+click: auto-follow (again to stop)")
            # (2.6.72) the tooltip only over the name and bars (the panel); the rest of the
            # art (the ring) still clicks the same, with no tooltip of its own
            Kit.catcher(g, ox, oy, w, h, frame_clicked(key), None, movable=not settings["lock"])
            px0, px1 = mirror_x(style, w, sx(PANEL[0]), sx(PANEL[2]))
            Kit.catcher(g, ox + px0, oy + sx(PANEL[1]), px1 - px0, sx(PANEL[3]) - sx(PANEL[1]),
                        frame_clicked(key), tip, movable=not settings["lock"])
            add_close_x(g, key, w, c, ox, oy)
            for name in ("name", "hits", "mana", "stam", "status", "portrait_text"):
                c["lbl_" + name] = mute(Kit.add_label(g, "", 0, 0))
            guard_at = None
            if key == "player":                                   # the GUARDED tag (guard_tick):
                c["guard_bg"] = color_box(g, 0, 0, 1, 1, (0, 0, 0), 0.65)   # over the panel's
                safe(lambda: setattr(c["guard_bg"], "IsVisible", False))  # top right corner
                c["lbl_guard"] = mute(Kit.add_label(g, "", 0, 0))
                guard_at = (ox + sx(PANEL[2]) - 6, oy + max(1, sx(PANEL[1]) - LABEL_H - 3))
            if strip:                                             # AR / Wt / Gold cells
                ix0, ix1 = ox + sx(STRIP_TEXT_X[0]), ox + sx(STRIP_TEXT_X[1])
                ty = oy + sx(STRIP_Y) + (sx(STRIP_INNER[1]) + sx(STRIP_INNER[3]) - LABEL_H) // 2 - 1
                lx = ix0 + 2
                c["cell_w"] = {}
                for caption, k, share in STRIP_CELLS:
                    width = int((ix1 - ix0) * share)
                    Kit.add_label(g, caption, lx, ty, Kit.HUE_INFO)
                    c["cell_" + k] = mute(Kit.add_label(g, "", lx + Kit.text_w(caption) + 5, ty))
                    c["cell_w"][k] = width - Kit.text_w(caption) - 11
                    lx += width
            frames[key] = {"g": g, "c": c, "rows": rows, "centre": (cx, cy), "hole": hole, "s": s,
                           "art": art, "names": names, "last": None, "seen": (x, y), "noto": None,
                           "variant": None, "snap": None, "code_move": False,
                           # what each control shows now (update_frame touches only changes)
                           "shown": {}, "bars": {}, "serial": None,
                           # (2.6.60) the art's place in the window, the window's size, the slot
                           "box": (ox, oy, w, h), "win": (W, H), "slot": fitbox.get(key),
                           # (2.6.67) the hole left open for a piece riding inside it
                           "inhole": inhole,
                           # (2.6.73) a piece rides under its bars (the art sits higher)
                           "rides": rides_inside(key)}
            if guard_at is not None:
                frames[key]["guard_at"] = guard_at
            st["art_dirty"] = True                                # prune_art may free a size
            G.AddControlOnDisposed(g, frame_disposed(key, g))
            G.AddGump(g)
            # A frame lands exactly where it is dropped: it takes no part in window
            # snapping (no jump to an anchor, an edge or another window, it never
            # follows a window that is dragged and no window snaps on to it), but the
            # keeper still keeps it on screen. It lines up with other frames by this
            # module's own rule (snap_to_frames); watch_frames saves it when a drag ends.
            if not safe(lambda: (Kit.no_snap(g), True)[1], False):
                safe(lambda: SNAP.skip_gump(g))          # an older mother script
            safe(lambda: Kit.on_moved(g, frame_moved(key)))   # let go, or the keeper moved it
            Kit.dispose(old)


        def frame_moved(key):
            """The mother's word that frame `key` was let go after a drag, or that
            the keeper moved it (back on screen after a resolution change, or a
            frame left half off). A drag was already seen by watch_frames, tick by
            tick; a place that differs from the last one seen is the keeper's move:
            it becomes the frame's place without counting as a drag (code_move),
            and is saved."""
            def handler():
                fr = frames.get(key)
                if fr is None or not Kit.is_open(fr.get("g")):
                    return
                p = frame_at(fr)
                if p is not None and p != fr.get("seen"):
                    fr["seen"] = p
                    fr["code_move"] = True
                    if st["pos"].get(key) != p:
                        st["pos"][key] = p
                        st["pos_dirty"] = True
                save_positions()
            return handler


        def small_button(g, art, x, y, fn, tooltip, fallback):
            """A small art button; a text label on a click catcher if the art is
            missing. Returns the controls to show or hide together."""
            if Kit.pic_size(art[0])[0] > 0:
                try:
                    b = G.CreateGumpButton("", Kit.HUE_TEXT, art[0], art[1], art[2])
                    b.SetPos(x, y)
                    g.Add(b)
                    Kit.on_click(b, fn)
                    safe(lambda: b.SetTooltip(tooltip))
                    return [b]
                except Exception:
                    pass
            lbl = Kit.add_label(g, fallback, x + 2, y, Kit.HUE_TITLE)
            return [lbl, Kit.catcher(g, x, y, max(14, Kit.text_w(fallback) + 4), 16, fn, tooltip)]


        def add_close_x(g, key, w, c, ox=0, oy=0):
            """A small X at the top corner of a frame, on the circle's side: top
            left of the player and tracked frames, top right of the (mirrored)
            target frame."""
            art = CLOSE_ART if Kit.pic_size(CLOSE_ART[0])[0] > 0 else Kit.ART_CLOSE
            bw, bh = Kit.pic_size(art[0])
            bw, bh = bw or 14, bh or 14
            x = ox + (w - CLOSE_INSET - bw if frame_style(key) == "target" else CLOSE_INSET)
            if key not in ("player", "target"):
                # (2.6.57) no X on the player and target frames: they are turned off
                # on the Frames settings page (or with the part); tracked frames keep it
                # (2.6.81) Alt+click on the X follows them (key is "m<serial>" here)
                small_button(g, art, x, oy + CLOSE_INSET, follow_or(int(key[1:]), ("xclose", key)),
                             "Close this frame. Alt+click: auto-follow (again to stop)", "x")


        def close_frame(key):
            fr = frames.pop(key, None)
            if fr:
                st["art_dirty"] = True                   # its size may be unused now
                g = fr.get("g")
                if Kit.is_open(g):
                    p = frame_at(fr)
                    if p is not None and st["pos"].get(key) != p:
                        st["pos"][key] = p
                        st["pos_dirty"] = True
                fr["g"] = None
                Kit.dispose(g)


        def supplies_spot(w, h, side, p=None):
            """Where a table of w x h sits beside the player frame: the side asked
            for (0 below, 1 left, 2 right), or the other side when there is no room
            there. None when the frame's place can't be read. p: the frame's place
            when the caller has it (2.6.82)."""
            fr = frames.get("player")
            if fr is None or not Kit.is_open(fr.get("g")):
                return None
            if p is None:
                p = frame_at(fr)
            if p is None:                                # a failed read: leave the table be
                return None
            fx, fy = p
            fw, fh = fr.get("win") or frame_size("player")[1:]   # (2.6.60) the window, slot and all
            W, H = Kit.screen()
            if side == 1:                                    # left of the frame (right if no room)
                at = (fx - w - 2, fy)
                if at[0] < 0:
                    at = (fx + fw + 2, fy)
            elif side == 2:                                  # right of it (left if no room)
                at = (fx + fw + 2, fy)
                if W > 0 and at[0] + w > W:
                    at = (fx - w - 2, fy)
            else:                                            # under it (above if no room), beyond
                below, above = cast_reserve(fy, fh)          # the cast bar's strip
                # (2.6.71) and the pieces stacked under (or over) the frame
                y_below = fy + fh + 2 + below + pieces_extent("player", True)
                at = (fx, y_below)
                if H > 0 and y_below + h > H:
                    y_above = fy - h - 2 - above - pieces_extent("player", False)
                    # 2.6.81: room on neither side: the side with more room (the
                    # clamp below keeps it on screen, so the frame is never pushed)
                    if y_above >= 0 or y_above + h > H - y_below:
                        at = (fx, y_above)
            # 2.6.81: always on screen as asked (Kit.place would clamp it anyway, but
            # the spot asked for must be the one placed, or it is placed every tick)
            x, y = at
            if W > 0:
                x = max(0, min(x, W - w))
            if H > 0:
                y = max(0, min(y, H - h))
            return (x, y)


        # ---------- (2.6.85) TazUO's own target health bar ----------
        #  The client opens it when you attack (its OpenHealthBarForLastAttack option). While
        #  the target frame shows and the box is ticked the option is off and an open bar is
        #  closed. HBAR_VAR says we hold it (per character, so a stop that never ran gives it
        #  back at the next start); given back when the box is unticked, the part goes off
        #  or Virtue Assistant stops. Your own setting is never left changed.
        HBAR_VAR = "UnitFrames_hbar_held"
        HBAR_EVERY = 1.0
        hbar = {"at": 0.0, "prof": None}


        def hbar_profile():
            try:
                return Tz.get(None, "CurrentProfile", Tz.T("ClassicUO.Configuration.ProfileManager"))
            except Exception:
                return None


        def hbar_sync(want):
            """On the client thread: the option as `want` says (hidden or your own)."""
            prof = hbar_profile()
            if prof is None:
                return
            held = _get(HBAR_VAR, "") == "1"
            if want:
                if not held and not bool(Tz.get(prof, "OpenHealthBarForLastAttack")):
                    return                                   # already off by your own choice
                if not held:
                    Tz.put(prof, "OpenHealthBarForLastAttack", False)
                    _put(HBAR_VAR, "1")
                try:
                    t = Tz.T("ClassicUO.Game.UI.Gumps.BaseHealthBarGump")
                    bar = Tz.get(None, "LastAttackBar", t)
                    if bar is not None and not bar.IsDisposed:
                        bar.Dispose()
                except Exception:
                    pass
            elif held:
                Tz.put(prof, "OpenHealthBarForLastAttack", True)
                _put(HBAR_VAR, "")


        def hbar_tick(now):
            if 0 <= hbar["at"] - now <= HBAR_EVERY:
                return
            hbar["at"] = now + HBAR_EVERY
            try:
                hbar_sync(bool(settings["hide_bar"] and settings["target"]))
            except Exception:
                pass


        def player_anchor(w, h, side):
            """(2.6.85) "frames.player_anchor", for Inventory > Supplies: (the player
            frame's window, where a table of w x h goes beside it), or None with no
            frame. The spot is worked out again only when what it depends on changed:
            the frame's place as watch_frames saw it this tick, its size, the side,
            the cast bar, the pieces stacked on it and the screen."""
            fr = frames.get("player")
            if fr is None or not Kit.is_open(fr.get("g")):
                return None
            p = fr.get("seen")
            sig = None
            if p is not None:
                sig = (p, fr.get("win") or frame_size("player")[1:], side, settings["cast"],
                       PIECES["stack"].get("player"), Kit.screen(), w, h)
            if sig is None or sig != anchor["sig"] or anchor["at"] is None:
                anchor["at"] = supplies_spot(w, h, side, p)
                anchor["sig"] = sig if anchor["at"] is not None else None
            at = anchor["at"]
            return None if at is None else (fr["g"], at)




        # ---------- cast bar (2.6.05: its own small window under the player frame) ----------
        def cast_reserve(fy, fh):
            """(below, above): the pixels the cast bar's strip takes under or over
            the player frame at height fy (fh tall); it sits under the frame, or
            over it when there is no room under it. (0, 0) with the cast bar off."""
            if not settings["cast"]:
                return 0, 0
            H = (Kit.screen() or (0, 0))[1]
            if H > 0 and fy + fh + CAST_GAP + CAST_H > H:
                return 0, CAST_H + CAST_GAP
            return CAST_H + CAST_GAP, 0


        def cast_spot(fr):
            """(x, y) of the cast bar for the player frame fr, lined up under its
            bars (over the frame when there's no room under it); None when the
            frame's place isn't known."""
            p = fr.get("seen")
            if p is None:
                return None
            _ox, oy, _fw, fh = fr.get("box") or (0, 0, 0, frame_size("player")[2])
            top = p[1] + oy                              # (2.6.60) the art's top in its window
            below, _above = cast_reserve(top, fh)
            x = p[0] + fr["rows"][0][0] - 6
            # (2.6.71) clear of Bandages / the buff row stacked on that side of the frame
            wh = (fr.get("win") or frame_size("player")[1:])[1]
            if below:
                extra = pieces_extent("player", True)
                y = top + fh + CAST_GAP
                if extra:
                    y = max(y, p[1] + wh + extra + CAST_GAP)
                return x, y
            extra = pieces_extent("player", False)
            y = top - CAST_H - CAST_GAP
            if extra:
                y = min(y, p[1] - extra - CAST_H - CAST_GAP)
            return x, y


        def drop_cast():
            g, cast["g"] = cast["g"], None
            cast["leader"] = None
            cast["shown"] = None
            Kit.dispose(g)


        def build_cast(fr):
            """The cast bar's window: a stone strip as wide as the frame's bars,
            holding three bars (casting, cast, failed; one shows) and the spell's
            name. Made at the first cast; again when the frame is rebuilt."""
            drop_cast()
            rows = fr["rows"]
            w, h = rows[0][2] - rows[0][0] + 12, CAST_H
            g = G.CreateGump(False, False)               # a display: clicks go through it
            Kit.add_window_frame(g, w, h, corners=False, mouse=False)
            c = {}
            for k in ("cast", "done", "fail"):
                pb = G.CreateGumpSimpleProgressBar(w - 12, h - 10, BAR_BG, CAST_COLOR[k], 0, 100)
                pb.SetPos(6, 5)
                g.Add(mute(pb))
                c[k] = pb
            c["lbl"] = mute(Kit.add_label(g, "", 6, 4))
            at = cast_spot(fr) or (0, 0)
            Kit.place(g, at[0], at[1], w, h)             # wholly on screen
            G.AddGump(g)
            safe(lambda: setattr(g, "IsVisible", False))
            safe(lambda: Kit.attach(g, fr["g"]))         # kept on screen with the frame
            # "at": the spot asked for (moved again only when that changes, so a
            # spot the keeper had to pull on screen isn't fought over every tick)
            cast.update({"g": g, "c": c, "shown": None, "at": at, "leader": fr["g"],
                         "s": fr["s"], "w": w})


        def cast_tick(now):
            """Every tick: your own words of power start the bar (the mother's
            Kit.SPELL_WORDS), a fizzle / broken concentration / no mana / no
            reagents line turns it red; it fills through the cast delay and goes
            green, then hides after CAST_HOLD. Nothing is drawn while it is
            hidden, and only what changed is touched while it shows."""
            fr = frames.get("player")
            if not settings["cast"] or fr is None or not Kit.is_open(fr.get("g")):
                cast["state"] = None
                st["jr"] = None                          # off: the journal isn't read for it
                if cast["g"] is not None:
                    drop_cast()
                return
            lines = None
            if st["jr"] is None:                         # (back) on: the lines from now on only,
                try:                                     # so old words never start a bar
                    st["jr"] = Journal.reader()
                except Exception:
                    st["jr"] = None
            else:
                try:
                    lines = st["jr"].new()               # the lines since the last tick
                except Exception:
                    lines = None
            if lines:
                me_name = st["names"].get(st["me"]) or ""
                say = settings["cast_say"]
                for ln in lines:
                    name = ln.name or ""
                    if say and cast["spell"] is not None and \
                            now - cast["start"] <= cast["secs"] + CAST_FAIL_WINDOW and \
                            not ln.low.startswith(OWN_PREFIX):
                        # debug: the shard's own texts and speakers while a spell is cast
                        API.SysMsg("%s: line [%s]: %s" % (TITLE, name or "-", ln.text.strip()),
                                   Kit.HUE_INFO)
                    if me_name and name == me_name:
                        sp = SPELLS.get(ln.low.strip())
                        if sp is not None:               # you began a spell
                            try:
                                info = Kit.spell_info(sp[0])
                            except Exception:
                                info = None
                            secs = info[3] if info and info[3] else CAST_FALLBACK
                            cast.update({"spell": sp[0], "start": min(now, ln.at or now),
                                         "secs": max(0.1, float(secs)), "state": "cast", "pct": 0,
                                         "word": ""})
                            if say:
                                API.SysMsg("%s: cast %s (%.2f s) from [%s]: %s" % (
                                    TITLE, sp[0], cast["secs"], name, ln.text.strip()), Kit.HUE_INFO)
                            continue
                    elif name and name != "System":
                        continue                         # someone else's line
                    if cast["spell"] is None or \
                            now - cast["start"] > cast["secs"] + CAST_FAIL_WINDOW:
                        continue
                    low = ln.low
                    for text, word in CAST_FAIL_TEXTS:
                        if low.startswith(text):
                            if cast["state"] != "cast":  # after the delay: the whole bar red
                                cast["pct"] = 100
                            cast.update({"state": "fail", "word": word, "until": now + CAST_HOLD})
                            break
            state = cast["state"]
            if state == "cast":
                el = now - cast["start"]
                if el >= cast["secs"]:
                    cast.update({"state": "done", "until": now + CAST_HOLD, "pct": 100})
                else:
                    cast["pct"] = max(0, int(100 * el / cast["secs"]))
            elif state is not None and now >= cast["until"]:
                cast["state"] = None
            d = fr["last"][5] if fr.get("last") else None
            if d is not None and d[M_DEAD]:
                cast["state"] = None                     # dead: nothing to cast
            draw_cast(fr)


        def draw_cast(fr):
            state = cast["state"]
            g = cast["g"]
            if state is None:
                if g is not None and cast["shown"] is not None:
                    cast["shown"] = None
                    safe(lambda: setattr(g, "IsVisible", False))
                return
            if g is None or not Kit.is_open(g) or cast["s"] != fr["s"] or \
                    cast["leader"] is not fr["g"]:
                build_cast(fr)                           # the first cast, or a rebuilt frame
                g = cast["g"]
            at = cast_spot(fr)
            if at is not None and at != cast["at"]:      # follows the frame
                cast["at"] = at
                try:
                    g.SetRect(at[0], at[1], cast["w"], CAST_H)
                    Kit.moved_by_code(g)                 # our move, not a drag
                except Exception:
                    pass
            label = cast["spell"] if state != "fail" else "%s: %s" % (cast["spell"], cast["word"])
            want = (state, cast["pct"], label)
            old = cast["shown"]
            if want == old:
                return
            cast["shown"] = want
            c = cast["c"]
            try:                                         # every tick while casting: no lambdas
                if old is None or old[0] != state:
                    for k in ("cast", "done", "fail"):
                        c[k].IsVisible = k == state
                if old is None or old[0] != state or old[1] != want[1]:
                    c[state].SetProgress(float(want[1]), 100.0)
                if old is None or old[2] != label:
                    text = fit(label, cast["w"] - 16)
                    Kit.set_text(c["lbl"], text, Kit.HUE_TEXT)
                    # centred by letter widths (Kit.text_px): no label made to measure
                    # each new spell's caption
                    c["lbl"].SetPos(max(6, (cast["w"] - TEXT_PX(text)) // 2), 4)
                if old is None:
                    g.IsVisible = True
            except Exception:
                pass


        # ---------- GUARDED tag (2.6.05, on the player frame) ----------
        def guard_tick(now):
            """GUARDED (green) while the town guards protect you, "?" while Virtue
            Assistant doesn't know yet, blank outside: HOST.guarded() read at most
            every GUARD_EVERY, the tag written only when it changes."""
            if not settings["guard"]:
                st["guard"] = False
            elif now >= st["next_guard"]:
                st["next_guard"] = now + GUARD_EVERY
                fn = getattr(HOST, "guarded", None)
                try:
                    st["guard"] = fn() if fn is not None else False   # an older mother: blank
                except Exception:
                    st["guard"] = None
            fr = frames.get("player")
            if fr is None or "guard_at" not in fr or not Kit.is_open(fr.get("g")):
                return
            gd = st["guard"]
            if gd is None:
                text, hue = "?", Kit.HUE_INFO
            elif gd:
                text, hue = "GUARDED", Kit.HUE_GOOD
            else:
                text, hue = "", Kit.HUE_TEXT
            x1, y = fr["guard_at"]
            place(fr, "guard", text, x1, y, hue, "right")
            if fr["shown"].get("guard_bg") != text:      # the dark strip behind it
                fr["shown"]["guard_bg"] = text
                box = fr["c"]["guard_bg"]
                if text:
                    tw = Kit.text_w(text) + 8
                    safe(lambda: Kit.ui_rect(box, x1 - tw + 4, y - 1, tw, LABEL_H + 4))
                safe(lambda: setattr(box, "IsVisible", bool(text)))


        def fit(text, width):
            """Text cut short to width px: the mother's Kit.fit (letter sums, no
            label per trimmed character)."""
            return Kit.fit(text, width)


        def place(fr, name, text, x, y, hue, align="left"):
            """Label c["lbl_" + name] of frame fr showing text in hue at (x, y)
            (its right end or centre there with align). The frame remembers what
            each label shows (fr["shown"]): a label is only touched when its
            text, hue or place changes, so an update where only the hits moved
            sets one label instead of six."""
            if align == "right":                 # (2.6.82) by letters: no label per new number
                x -= TEXT_PX(text) if text else 0
            elif align == "center":
                x -= (TEXT_PX(text) if text else 0) // 2
            want = (text, hue, int(x), int(y))
            shown = fr["shown"]
            old = shown.get(name)
            if old == want:
                return
            shown[name] = want
            lbl = fr["c"]["lbl_" + name]
            Kit.set_text(lbl, text, hue)
            if old is None or old[2] != want[2] or old[3] != want[3]:
                try:
                    Kit.ui_pos(lbl, want[2], want[3])
                except Exception:
                    pass


        def set_bar(fr, variant, cur, mx):
            want = (float(max(0, cur)), float(max(1, mx)))
            if fr["bars"].get(variant) == want:
                return
            pb = fr["c"].get("bar_" + variant)
            if pb is not None:
                try:
                    pb.SetProgress(want[0], want[1])
                    fr["bars"][variant] = want
                except Exception:
                    pass


        def show_hits_variant(fr, want):
            if fr["variant"] == want:
                return
            fr["variant"] = want
            for v in ("hits", "poison", "yellow"):
                pb = fr["c"].get("bar_" + v)
                if pb is not None:
                    safe(lambda: setattr(pb, "IsVisible", v == want))
                    if v != want:
                        safe(lambda: pb.SetProgress(0.0, 1.0))
                        fr["bars"][v] = (0.0, 1.0)


        def set_noto(fr, rgb):
            if fr["noto"] == rgb:
                return
            c = fr["c"]
            if fr["art"]:
                name = noto_texture(rgb, fr["s"])
                if name is None:
                    return            # still being drawn: the frame is updated again once it's in
                safe(lambda: setattr(c["noto"], "TextureName", name))
            else:
                for box in c["edge"]:
                    safe(lambda: box.SetBaseColor(rgb[0], rgb[1], rgb[2], 255))
            fr["noto"] = rgb


        def set_snapshot(fr, serial):
            """Show this character's picture (the blank backdrop until it's taken)."""
            if not fr["art"]:
                return {}
            # (2.6.72) no one on the frame: no picture at all (the portrait control hidden,
            # the ring's black shows), never a blank or an old texture under "No target"
            empty = not serial
            if fr["shown"].get("snap_hidden") != empty:
                fr["shown"]["snap_hidden"] = empty
                safe(lambda: setattr(fr["c"]["snap"], "IsVisible", not empty))
            if empty:
                return {}
            want_snapshot(serial)
            snap = st["snaps"].get(serial) or {}
            names = fr.get("names") or art_names(fr["s"])    # cached at build (every frame, every tick)
            name = snap.get("name") or names["blank"]
            if fr["snap"] != name:
                fr["snap"] = name
                safe(lambda: setattr(fr["c"]["snap"], "TextureName", name))
            return snap


        def pct(cur, mx):
            return int(round(100.0 * cur / mx)) if mx > 0 else 0


        def update_frame(key):
            """Bring frame `key` up to date. Nothing is touched when nothing it
            shows changed (one tuple compare); otherwise only the controls whose
            value changed are set (place / set_bar / set_noto remember theirs)."""
            fr = frames.get(key)
            if fr is None or not Kit.is_open(fr.get("g")):
                return
            serial = frame_serial(key)
            if serial != fr["serial"]:                      # someone new on this frame
                fr["serial"] = serial
                note_shown(serial)
            d = read_mobile(serial)
            is_self = serial == st["me"]
            highlight = key != "target" and serial and serial == st["target"]
            snap = set_snapshot(fr, serial)
            c = fr["c"]
            cells = status_values() if "cell_ar" in c else None
            state = (serial, highlight, settings["numbers"], fr["snap"], bool(snap.get("creature")),
                     d, cells)
            if state == fr["last"]:
                return
            fr["last"] = state
            hue = Kit.HUE_TITLE if highlight else Kit.HUE_TEXT
            status, portrait_text = "", ""

            if not serial or d is None:
                noto, hue, bars, variant = NO_NOTO, Kit.HUE_INFO, ((0, 1),) * 3, "hits"
                if not serial:                               # target frame, nothing targeted
                    # (2.6.72) the placeholder: nothing in the name box or on the bars,
                    # "No target" in the dim ring
                    name, vals = "", ("", "", "")
                    portrait_text = "No target"
                else:                                        # gone off screen
                    name, vals = st["names"].get(serial) or "Unknown", ("Out of range", "", "")
            else:
                dead = d[M_DEAD]
                name = d[M_NAME] or st["names"].get(serial) or "Unknown"
                variant = "poison" if d[M_POISON] else ("yellow" if d[M_YELLOW] else "hits")
                bars = ((d[M_HITS], d[M_HMAX]), (d[M_MANA], d[M_MMAX]), (d[M_STAM], d[M_SMAX]))
                noto = NO_NOTO if dead else NOTO_COLOR.get(d[M_NOTO], NOTO_COLOR["gray"])
                status = "DEAD" if dead else ("PARA" if d[M_PARA] else "")
                if snap.get("creature"):
                    portrait_text = "No picture"
                vals = []
                for i, (cur, mx) in enumerate(bars):
                    if mx <= 0:
                        vals.append("" if i else "--")
                    elif is_self or i:                       # mana / stamina only come real
                        vals.append("%d/%d" % (cur, mx))
                    else:                                    # others' hits arrive scaled
                        vals.append("%d%%" % pct(cur, mx))
                if dead:
                    vals[0] = "Dead"
                vals = tuple(vals)
            if not settings["numbers"] and vals and vals[0] != "Out of range":
                vals = ("", "", "")

            show_hits_variant(fr, variant)
            set_bar(fr, variant, bars[0][0], bars[0][1])
            set_bar(fr, "mana", bars[1][0], bars[1][1])
            set_bar(fr, "stam", bars[2][0], bars[2][1])
            set_noto(fr, noto)
            rows = fr["rows"]
            for i, row in enumerate(ROWS):
                x0, y0, x1, y1 = rows[i]
                place(fr, row, vals[i], x1 - 8, y0 + (y1 - y0 - LABEL_H) // 2 - 1, Kit.HUE_TEXT,
                      "right")
            x0, y0, x1, y1 = rows[0]
            room = max(20, x1 - x0 - 16 - (TEXT_PX(vals[0]) + 10 if vals[0] else 0))
            fitted = fr["shown"].get("fit")                  # fit() measures: only on a change
            if fitted is None or fitted[0] != name or fitted[1] != room:
                fitted = fr["shown"]["fit"] = (name, room, fit(name, room))
            place(fr, "name", fitted[2], x0 + 8, y0 + (y1 - y0 - LABEL_H) // 2 - 1, hue)
            cx, cy = fr["centre"]
            hole = fr["hole"]
            ty = cy + int(hole * 0.42)
            place(fr, "status", status, cx, ty + 2,
                  Kit.HUE_BAD if status == "DEAD" else Kit.HUE_TITLE, "center")
            if fr["shown"].get("strip") != status:          # the dark strip behind DEAD / PARA
                fr["shown"]["strip"] = status
                if status:
                    sw = Kit.text_w(status) + 10
                    safe(lambda: Kit.ui_rect(c["strip"], cx - sw // 2, ty, sw, LABEL_H + 4))
                safe(lambda: setattr(c["strip"], "IsVisible", bool(status)))
            place(fr, "portrait_text", fit(portrait_text, 2 * hole - 6) if portrait_text else "",
                  cx, cy - LABEL_H // 2 - 1, Kit.HUE_INFO, "center")
            if cells is not None and fr["shown"].get("cells") != cells:
                fr["shown"]["cells"] = cells
                update_status_cells(fr)


        def status_values():
            """(AR, weight, max weight, gold) of the player: they change slowly, so
            they are read again at most every STATUS_EVERY seconds."""
            now = time.time()
            if st.get("status") is None or now >= st.get("status_at", 0.0):
                pl = API.Player
                try:
                    vals = (int(pl.PhysicalResistance or 0), int(pl.Weight or 0),
                            int(pl.WeightMax or 0), int(pl.Gold or 0))
                except Exception:
                    vals = (int(safe(lambda: pl.PhysicalResistance, 0) or 0),
                            int(safe(lambda: pl.Weight, 0) or 0),
                            int(safe(lambda: pl.WeightMax, 0) or 0), int(safe(lambda: pl.Gold, 0) or 0))
                st["status"], st["status_at"] = vals, now + STATUS_EVERY
            return st["status"]


        def with_commas(n):
            digits = str(abs(n))
            parts = []
            while digits:
                parts.insert(0, digits[-3:])
                digits = digits[:-3]
            return ("-" if n < 0 else "") + ",".join(parts)


        def update_status_cells(fr):
            c = fr["c"]
            ar, wt, wmax, gold = status_values()
            vals = (("ar", str(ar), Kit.HUE_TEXT),
                    ("weight", "%d/%d" % (wt, wmax) if wmax else str(wt),
                     Kit.HUE_BAD if wmax and wt > wmax else
                     (Kit.HUE_TITLE if wmax and wt >= wmax - 10 else Kit.HUE_TEXT)),
                    ("gold", with_commas(gold), Kit.HUE_TEXT))
            for k, text, hue in vals:
                Kit.set_text(c["cell_" + k], fit(text, max(20, c["cell_w"][k])), hue)


        def wanted_frames():
            keys = []
            if settings["player"]:
                keys.append("player")
            if settings["target"] and (st["target"] or not settings["hide_empty"]):
                keys.append("target")
            keys.extend("m%d" % t["serial"] for t in tracked)
            return keys


        def sync_frames():
            want = wanted_frames()
            for key in list(frames):
                if key not in want:
                    close_frame(key)
            for key in want:
                fr = frames.get(key)
                if fr is None or not Kit.is_open(fr.get("g")) or fr.get("s") != frame_scale(key) \
                        or fr.get("slot") != fitbox.get(key) \
                        or (fr.get("slot") and fr.get("inhole") != PIECES["hole"].get(key)) \
                        or (fr.get("slot") and fr.get("rides") != rides_inside(key)):
                    # new, closed, or its size changed; with pictures, once its art is drawn
                    # (thread_tick draws it; an old-size frame stays up meanwhile)
                    if not st["art"] or want_art(frame_scale(key)) is not None:
                        build_frame(key)
                update_frame(key)


        def screen_size():
            """The client window's size in gump pixels (the space frames are placed
            in; Kit.screen allows for the UI scale), or None while the client won't
            say: nothing is moved on a guess."""
            w, h = safe(Kit.screen, (0, 0)) or (0, 0)
            return (int(w), int(h)) if w > 0 and h > 0 else None


        def frame_gump(key):
            """A getter for frame `key`'s window, for the layout's registry."""
            def get():
                fr = frames.get(key)
                return fr.get("g") if fr else None
            return get


        def layout_held(key):
            """Is frame `key` slotted in a zone of the layout (2.6.54): then the
            layout places it (no line-up with other frames, no mirror)."""
            fn = getattr(HOST, "layout_holds", None)
            if fn is None:
                return False
            try:
                return bool(fn(KEY + "." + key))
            except Exception:
                return False


        def frame_at(fr):
            """Where frame fr's gump sits now, or None when it can't be read (a
            failed read is never taken for a position)."""
            g = fr.get("g")
            r = _rect_of(g) if g is not None else None   # (2.6.70) a frame just rebuilt: as
            if r is not None:                            # placed, not the 0, 0 it reads for a frame
                return r[0], r[1]
            try:                                     # every frame, every tick (drag check)
                return int(g.GetX()), int(g.GetY())
            except Exception:
                return None


        def watch_frames(now):
            """Every tick: note where each frame sits. A frame that moved was dragged
            by you, unless the move was code's (code_move: move_frame for the
            mirror option and the frame line-up, frame_moved for the keeper), which
            notes its own moves: remember the spot and save it once the drag has
            settled."""
            for key, fr in frames.items():
                if not Kit.is_open(fr.get("g")):
                    continue
                p = frame_at(fr)
                if p is None:
                    continue
                if p != fr.get("seen"):
                    fr["seen"] = p
                    if fr.get("code_move"):             # our own move landed: not a drag
                        fr["code_move"] = False
                        if st["pos"].get(key) != p:
                            st["pos"][key] = p
                            st["pos_dirty"] = True
                            st["pos_save_at"] = now + DRAG_SETTLE
                        continue
                    fr["drag_until"] = now + DRAG_SETTLE
                    if not layout_held(key):            # (slotted: the layout places it)
                        fr["moved"] = True              # for the mirror option, this tick
                        fr["dropped"] = True            # snap_to_frames once it is let go
                    if st["pos"].get(key) != p:
                        st["pos"][key] = p
                        st["pos_dirty"] = True
                        st["pos_save_at"] = now + DRAG_SETTLE
                else:
                    fr["code_move"] = False             # the move was seen where it was made
                    if fr.get("dropped") and now >= fr.get("drag_until", 0.0):
                        try:
                            pressed = SNAP.pressed()
                        except Exception:
                            pressed = None
                        if pressed is not True:
                            fr["dropped"] = False       # the drag is over: line it up
                            snap_to_frames(key)
            if st["pos_dirty"] and now >= st["pos_save_at"]:
                save_positions()


        def frame_rect(key):
            fr = frames.get(key)
            if fr is None or not Kit.is_open(fr.get("g")):
                return None
            p = fr.get("seen") or frame_at(fr)
            if p is None:
                return None
            w, h = fr.get("win") or frame_size(key)[1:]   # (2.6.60) its window, slot and all
            return p[0], p[1], w, h


        def snap_to_frames(key):
            """A frame you have just let go within FRAME_SNAP px of another frame
            moves so that it lines up with that frame exactly: a corner on a corner
            (side by side or stacked, edges flush) first, else one edge flush or in
            line. Only frames count: no screen anchors, no other windows."""
            r = frame_rect(key)
            if r is None:
                return
            x, y, w, h = r
            corner = None                             # (distance, x, y)
            ex = ey = None                            # (distance, value)
            for other in frames:
                if other == key:
                    continue
                ro = frame_rect(other)
                if ro is None:
                    continue
                ox, oy, ow, oh = ro
                for tx, ty in ((ox + ow, oy), (ox + ow, oy + oh - h), (ox - w, oy),
                               (ox - w, oy + oh - h), (ox, oy + oh), (ox + ow - w, oy + oh),
                               (ox, oy - h), (ox + ow - w, oy - h)):
                    d = max(abs(x - tx), abs(y - ty))
                    if d <= FRAME_SNAP and (corner is None or d < corner[0]):
                        corner = (d, tx, ty)
                if y < oy + oh + FRAME_SNAP and oy < y + h + FRAME_SNAP:
                    for tx in (ox + ow, ox - w, ox, ox + ow - w):
                        d = abs(x - tx)
                        if d <= FRAME_SNAP and (ex is None or d < ex[0]):
                            ex = (d, tx)
                if x < ox + ow + FRAME_SNAP and ox < x + w + FRAME_SNAP:
                    for ty in (oy + oh, oy - h, oy, oy + oh - h):
                        d = abs(y - ty)
                        if d <= FRAME_SNAP and (ey is None or d < ey[0]):
                            ey = (d, ty)
            if corner is not None:
                nx, ny = corner[1], corner[2]
            else:
                nx = ex[1] if ex else x
                ny = ey[1] if ey else y
            if (nx, ny) != (x, y):
                move_frame(key, nx, ny)
                frames[key]["moved"] = True           # the mirror option follows the lined-up spot


        def move_frame(key, x, y):
            fr = frames.get(key)
            if fr is None or not Kit.is_open(fr.get("g")):
                return
            w, h = fr.get("win") or frame_size(key)[1:]   # (2.6.60) never cut to the art
            try:
                fr["g"].SetRect(int(x), int(y), w, h)
                Kit.note_rect(fr["g"], int(x), int(y), w, h)   # (2.6.71) read back as asked until it lands
                Kit.moved_by_code(fr["g"])        # the snapping, too, knows it was no drag
            except Exception:
                pass
            fr["seen"] = (int(x), int(y))         # our own move is not a drag
            fr["code_move"] = True
            fr["moved"] = False
            st["pos"][key] = fr["seen"]
            st["pos_dirty"] = True
            st["pos_save_at"] = time.time() + DRAG_SETTLE


        def mirror_frames(force=False):
            """Keep the player and target frames at mirror-image positions, the
            same distance in from the left and right edges of the window and at
            the same height. Whichever frame was dragged leads; the other
            follows. With force, the target follows the player right now."""
            p, t = frames.get("player"), frames.get("target")
            if p is None or t is None or not Kit.is_open(p.get("g")) or not Kit.is_open(t.get("g")):
                return
            if layout_held("player") or layout_held("target"):   # the layout places them
                return
            size = screen_size()
            if size is None:                          # the window's size isn't known: no guess
                return
            sw = size[0]
            _s, w, _h = frame_size("player")
            pp, tp = p.get("seen"), t.get("seen")     # read by watch_frames this tick
            if pp is None or tp is None:
                return
            p_moved = bool(p.get("moved"))
            t_moved = bool(t.get("moved"))
            if t_moved and not p_moved and not force:
                want = (sw - tp[0] - w, tp[1])
                if want != pp:
                    move_frame("player", *want)
            elif p_moved or force:
                want = (sw - pp[0] - w, pp[1])
                if want != tp:
                    move_frame("target", *want)


        def target_from_frame(key):
            serial = frame_serial(key)
            if not serial:
                return
            if safe(lambda: API.HasTarget(), False):
                API.Target(serial)
            else:
                safe(lambda: API.SetLastTarget(serial=serial))
                if key != "target" and serial != st["me"]:
                    st["target"] = serial


        # ---------- tracked list ----------
        def add_tracked(serial, auto=False):
            if not serial:
                API.SysMsg("Frames: target someone first, then click Add frame.", Kit.HUE_BAD)
                return
            st["dismissed"].discard(serial)      # (2.6.81) asked for again: party sync may add it
            if serial == st["me"]:
                API.SysMsg("Frames: that's you; your own frame is the player frame.",
                           Kit.HUE_INFO)
                return
            for t in tracked:
                if t["serial"] == serial:
                    t["auto"] = False
                    API.SysMsg("Frames: %s already has a frame." % t["name"], Kit.HUE_INFO)
                    save_tracked()
                    return
            if len(tracked) >= MAX_TRACKED:
                API.SysMsg("Frames: %d frames is the limit." % MAX_TRACKED, Kit.HUE_BAD)
                return
            d = read_mobile(serial)
            if d is None:
                API.SysMsg("Frames: that isn't a mobile you can see.", Kit.HUE_BAD)
                return
            tracked.append({"serial": serial, "auto": auto, "name": d[M_NAME] or "Unknown"})
            save_tracked()
            API.SysMsg("Frames: added %s." % (d[M_NAME] or "a frame"), Kit.HUE_GOOD)
            build_window()
            HOST.refresh_settings(KEY)           # the OTHERS' FRAMES list (2.6.51)


        def remove_tracked(serial):
            for t in tracked:                    # (2.6.81) a party frame removed stays removed
                if t["serial"] == serial and t["auto"]:
                    st["dismissed"].add(serial)
            tracked[:] = [t for t in tracked if t["serial"] != serial]
            close_frame("m%d" % serial)
            save_tracked()
            build_window()
            HOST.refresh_settings(KEY)           # the OTHERS' FRAMES list (2.6.51)


        def is_tracked(serial):
            for t in tracked:
                if t["serial"] == serial:
                    return True
            return False


        def pick_answer(kind):
            """A pick cursor's answer, queued for the next tick as (kind, serial)."""
            def done(serial):
                st["queue"].append((kind, int(serial or 0)))
            return done


        # ---------- control window ----------
        queue = Kit.queuer(st)                 # click handler: the action runs on the next tick
        on_disposed = Kit.disposer(KEY, st, win)


        ADD_TIP = ("Give your target a frame; with no new target, a target cursor picks someone. "
                   "Alt+click a frame: auto-follow (again to stop)")
        REMOVE_TIP = ("Raise a target cursor, then click the person or their frame to remove it "
                      "(each frame has its own X too)")
        BTN_H = 40                               # the window's one section (2.6.51)


        def build_window():
            # 2.6.51: the floating window is two simple circle buttons, Add frame and
            # Remove frame; the list of frames (with Alt+click auto-follow), Add
            # target, Pick... and Clear all are on the settings page (OTHERS' FRAMES)
            if st["shutting"]:
                return
            M, GAP = Kit.MARGIN, Kit.GAP
            n = len(tracked)
            if st["minimized"]:
                w, h = MINI_W, MINI_H
            else:
                w, h = W, M + 30 + GAP + BTN_H + M
            x, y = Kit.load_pos(POS_KEY, (200, 200), (w, h))
            if Kit.is_open(win["g"]):
                x, y = win["g"].GetX(), win["g"].GetY()
            old, win["g"] = win["g"], None
            store = ({}, {})
            g = G.CreateGump(True, True)
            if st["minimized"]:
                Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"),
                             "%s: %d frame%s" % (TITLE, n, "" if n == 1 else "s"))
            else:
                IW = W - 2 * M
                Kit.add_window_frame(g, w, h)
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"))
                ya = M + 30 + GAP
                Kit.add_section(g, M, ya, IW, BTN_H)
                bx = M + 12
                Kit.art_button(g, store, "add", Kit.ART_CIRCLE, bx, ya + 12, "Add frame", ADD_TIP,
                               on_click=queue("add_frame"))
                bx += 15 + 5 + Kit.text_w("Add frame") + 24
                Kit.art_button(g, store, "remove", Kit.ART_CIRCLE, bx, ya + 12, "Remove frame",
                               REMOVE_TIP, on_click=queue("remove_frame"))
            Kit.place(g, x, y, w, h)                     # wholly on screen
            win.update({"g": g, "store": store})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))      # saved the moment you let go of it
            if st["minimized"] and st["docked"]:         # folded into the Action Bar
                safe(lambda: setattr(g, "IsVisible", False))
            if st.get("min_saved") != st["minimized"]:   # minimized / restored: kept for next start
                st["min_saved"] = st["minimized"]
                _put(MIN_KEY, "1" if st["minimized"] else "0")
            Kit.dispose(old)


        # ---------- settings page (drawn inside the Virtue Assistant window) ----------
        CHECKS_LEFT = (("player", "Show your own frame", "A frame with your HP, mana and stamina"),
                       ("target", "Show the target frame", "A frame for your current target"),
                       ("hide_empty", "Hide the target frame with no target",
                        "The target frame shows only while you have a target"),
                       ("numbers", "Show numbers on the bars",
                        "HP, mana and stamina as numbers on the bars (others' HP as a %)"),
                       ("lock", "Lock the frames in place", "Frames can't be dragged"),
                       ("cast", "Show a cast bar under your frame",
                        "Your spell's name filling through its cast delay: green when cast, red "
                        "on a fizzle, a broken concentration, no mana or no reagents"))
        CHECKS_RIGHT = (("hide_bar", "Hide TazUO's own target health bar",
                         "So there aren't two with the target frame on; unticked, your client's own "
                         "setting is back"),
                        ("click", "Click a frame to target it",
                         "With a target cursor up the click aims it; otherwise it sets your last target"),
                        ("party", "Add a frame for each party member",
                         "Party members get a frame while they are in your party"),
                        ("ignore_self", "Ignore yourself as last target",
                         "Targeting yourself (a bandage, a heal) doesn't replace your target frame"),
                        ("attack", "Prefer the attack target",
                         "Frame who you are attacking when the client exposes it, else your last target"),
                        ("mirror", "Mirror the player and target frames",
                         "Drag either frame and the other moves to the mirror-image spot "
                         "on the far side of the screen, at the same height"),
                        ("guard", "Show a GUARDED tag on your frame",
                         "GUARDED while the town guards protect you, ? while Virtue Assistant "
                         "doesn't know yet (until you enter or leave a guarded area), blank outside"))
        CHECKS_DEBUG = (("cast_say", "Print every line that arrives while you cast in the journal",
                         "While a spell of yours is cast, every journal line is repeated with its "
                         "speaker, so the shard's texts can be checked"),)
        CHECKS_ALL = CHECKS_LEFT + CHECKS_RIGHT + CHECKS_DEBUG   # (2.6.82) joined once
        PORTRAIT_SLIDERS = (("pdx", "Left / right"), ("pdy", "Up / down"), ("pzoom", "Zoom"))
        PREVIEW_TEX = TEX_PREFIX + "snap_preview"
        CHECK_W = 24                       # checkbox art and the gap before its caption


        SCALE_TIP = ("Size of the frames as a percentage of the art; pictures are redrawn to size "
                     "(%d-%d%%)" % (SCALE_MIN, SCALE_MAX))
        PSCALE_TIP = ("Size of party members' frames while 'Party members' is ticked (%d-%d%%)"
                      % (SCALE_MIN, SCALE_MAX))
        PORTRAIT_TIPS = {"pdx": "Shift everyone's picture left or right inside the circle",
                         "pdy": "Shift everyone's picture up or down inside the circle",
                         "pzoom": "Zoom everyone's picture in or out (100%% = %d art pixels tall)"
                                  % SNAP_DEPTH}
        # section heights: frames, scale, picture
        CONFIG_HS = (32 + max(len(CHECKS_LEFT), len(CHECKS_RIGHT)) * 26 + 4, 96,
                     30 + PREVIEW + 4 + 10)
        DEBUG_H = 30 + len(CHECKS_DEBUG) * 26 + 10            # the page's last section


        def with_tip(ctrl, text):
            """A settings control with its tooltip (every control on the page has one)."""
            safe(lambda: ctrl.SetTooltip(text))
            return ctrl


        def others_height():
            """OTHERS' FRAMES (2.6.51): the buttons, then one row per frame."""
            return 30 + 28 + 4 + max(1, len(tracked)) * 24 + 6


        def config_height(w):
            return others_height() + Kit.GAP + sum(CONFIG_HS) + 2 * Kit.GAP + Kit.GAP + DEBUG_H


        def build_others(g, x, y, w, store):
            """What the floating window had before 2.6.51: Add target, Pick..., Clear
            all and the list of frames (Alt+click a name: auto-follow; X: remove)."""
            n = len(tracked)
            Kit.add_section(g, x, y, w, others_height(),
                            "OTHERS' FRAMES  (%d of %d)" % (n, MAX_TRACKED))
            bx = x + 12
            Kit.art_button(g, store, "add", Kit.ART_PLAY, bx, y + 28, "Add target",
                           "Give your current target a frame", on_click=queue("add_target"))
            bx += 35 + Kit.text_w("Add target") + 14
            Kit.art_button(g, store, "pick", Kit.ART_PLAY, bx, y + 28, "Pick...",
                           "Target someone to give them a frame", on_click=queue("pick"))
            bx_clear = x + w - 12 - 35 - Kit.text_w("Clear all")
            Kit.art_button(g, store, "clear", Kit.ART_CLOSE, bx_clear, y + 28, "Clear all",
                           "Remove every frame of someone else", on_click=queue("clear"))
            yl = y + 30 + 28 + 4
            rm_w = Kit.pic_size(Kit.ART_CLOSE[0])[0] or 30
            if not tracked:
                Kit.add_label(g, "No frames yet. Target someone, then click Add target.",
                              x + 12, yl + 3, Kit.HUE_INFO)
            for i, t in enumerate(tracked):
                ry = yl + i * 24
                tag = "(party)" if t["auto"] else ""
                room = w - 24 - rm_w - 6 - (Kit.text_w(tag) + 8 if tag else 0)
                shown = fit(t["name"], room)
                Kit.add_label(g, shown, x + 12, ry + 3)
                Kit.catcher(g, x + 12, ry, room + 8, 20, row_click(t["serial"]),
                            "Alt+click: auto-follow (again to stop)")
                if tag:
                    Kit.add_label(g, tag, x + 12 + Kit.text_w(shown) + 8, ry + 3, Kit.HUE_INFO)
                Kit.art_button(g, store, "rm%d" % i, Kit.ART_CLOSE, x + w - 12 - rm_w, ry,
                               None, "Remove %s's frame. Alt+click: auto-follow (again to stop)"
                               % t["name"],
                               on_click=follow_or(t["serial"], ("rm", t["serial"])))   # (2.6.81)


        def slider_text(k, v):
            return "%d%%" % v if k == "pzoom" else ("%+d" % v)


        def build_config(g, x, y, w):
            h_frames, h_size, h_portrait = CONFIG_HS
            c = {}
            store = ({}, {})
            build_others(g, x, y, w, store)
            y = y + others_height() + Kit.GAP
            Kit.add_section(g, x, y, w, h_frames, "OPTIONS")
            for col, checks in ((0, CHECKS_LEFT), (1, CHECKS_RIGHT)):
                cx = x + 12 + col * (w // 2)
                for i, (k, text, tip) in enumerate(checks):
                    c[k] = Kit.add_check(g, text, cx, y + 30 + i * 26, settings[k], tip)
            y2 = y + h_frames + Kit.GAP
            Kit.add_section(g, x, y2, w, h_size, "FRAME SIZE")
            # row 1: every frame; row 2: party members' own size, when ticked
            sx = x + 12 + max(Kit.text_w("All frames:"), CHECK_W + Kit.text_w("Party members:")) + 14
            Kit.add_label(g, "All frames:", x + 12, y2 + 36)
            c["scale"] = with_tip(Kit.add_slider(g, sx, y2 + 38, 260, SCALE_MIN, SCALE_MAX,
                                                 settings["scale"]), SCALE_TIP)
            c["scale_lbl"] = Kit.add_label(g, "%d%%" % settings["scale"], sx + 272, y2 + 36,
                                           Kit.HUE_INFO)
            c["pscale_on"] = Kit.add_check(g, "Party members:", x + 12, y2 + 62,
                                           settings["pscale_on"],
                                           "Party members' frames get their own size (the slider "
                                           "beside this); untick and they use the size above")
            c["pscale"] = with_tip(Kit.add_slider(g, sx, y2 + 66, 260, SCALE_MIN, SCALE_MAX,
                                                  settings["pscale"]), PSCALE_TIP)
            c["pscale_lbl"] = Kit.add_label(g, "%d%%" % settings["pscale"], sx + 272, y2 + 64,
                                            Kit.HUE_INFO)
            # picture crop: a live preview of your own snapshot (only while the module
            # runs: composing it is thread_tick's work, never the settings window's build)
            y3 = y2 + h_size + Kit.GAP
            Kit.add_section(g, x, y3, w, h_portrait, "PICTURE  (in each frame's circle)")
            Kit.add_section(g, x + 12, y3 + 30, PREVIEW + 4, PREVIEW + 4, alpha=1.0)
            if st["art"] and st.get("running"):
                draw_preview()
                g.Add(texture_control(PREVIEW_TEX, x + 14, y3 + 32, PREVIEW, PREVIEW))
            else:
                lines = ("Pictures", "unavailable") if st.get("running") else \
                    ("Turn Frames", "on for a", "preview")
                top = y3 + 32 + (PREVIEW - len(lines) * 18) // 2
                for i, line in enumerate(lines):
                    Kit.add_label(g, line, x + 14 + (PREVIEW - Kit.text_w(line)) // 2,
                                  top + i * 18, Kit.HUE_INFO)
            lx = x + 12 + PREVIEW + 4 + 16
            lw = max(Kit.text_w(t) for _k, t in PORTRAIT_SLIDERS) + 12
            for i, (k, text) in enumerate(PORTRAIT_SLIDERS):
                ry = y3 + 32 + i * 26
                lo, hi = NUMBERS[k]
                Kit.add_label(g, text + ":", lx, ry)
                c[k] = with_tip(Kit.add_slider(g, lx + lw, ry + 2, 180, lo, hi, settings[k]),
                                PORTRAIT_TIPS[k])
                c[k + "_lbl"] = Kit.add_label(g, slider_text(k, settings[k]), lx + lw + 192, ry,
                                              Kit.HUE_INFO)
            ry = y3 + 32 + 3 * 26
            Kit.art_button(g, store, "retake", Kit.ART_PLAY, lx, ry, "Retake pictures",
                           "Take everyone's picture again (after a change of gear)")
            rx = lx + 35 + Kit.text_w("Retake pictures") + 18
            Kit.art_button(g, store, "reset", Kit.ART_CLOSE, rx, ry, "Reset",
                           "Put the three picture sliders back to their defaults")
            # debug (always the page's last section)
            y6 = y3 + h_portrait + Kit.GAP
            Kit.add_section(g, x, y6, w, DEBUG_H, "DEBUG  (for checking the shard's texts)")
            for i, (k, text, tip) in enumerate(CHECKS_DEBUG):
                c[k] = Kit.add_check(g, text, x + 12, y6 + 30 + i * 26, settings[k], tip)
            page.update({"c": c, "store": store})


        def draw_preview():
            """Your own picture with the current crop, drawn by thread_tick
            (composing it takes hundreds of ms: never in the game's frame, where
            the settings page is built and polled). With the module off there is
            no thread_tick, so no preview: build_config says so instead."""
            if st.get("running") and st["art"]:
                page["preview_want"] = True


        def read_own_layers():
            """(layers, body) of your own paperdoll, or None. In the game's frame."""
            doll = read_paperdoll(st["me"] or my_serial())
            if not doll or not doll["body"]:
                return None
            layers = safe(lambda: fetch_layers(doll), [])
            return (layers, doll["body"]) if layers else None


        def draw_preview_now():
            """Your own picture with the current crop, from the pixels last read."""
            got = page.get("layers")
            if got is None:
                got = safe(lambda: Kit.on_client(read_own_layers))   # one hop (in place there)
                if not got:
                    return
                page["layers"] = got
            # 2.6.81: composed a slice at a time by thread_tick (preview_work), not in
            # one go; a newer crop replaces the one being composed
            page["preview_gen"] = compose_steps(got[0], got[1], PREVIEW)


        def preview_work(budget):
            """(2.6.81) A slice of the settings preview (script thread)."""
            deadline = time.time() + budget
            while page.get("preview_gen") is not None:
                gen = page["preview_gen"]
                try:
                    r = next(gen)
                except Exception:                         # StopIteration included
                    if page.get("preview_gen") is gen:
                        page["preview_gen"] = None
                    return
                if r is not None:
                    if page.get("preview_gen") is gen:
                        page["preview_gen"] = None
                    safe(lambda: Bridge.on_main(lambda: Bridge.put_texture(PREVIEW_TEX, PREVIEW,
                                                                            PREVIEW, r)))
                    return
                if time.time() >= deadline:
                    return


        SLIDER_BY_CALL = [False]   # (2.6.82) .Value raised and GetValue() answered: use that


        def slider_value(sl, default):
            """(2.6.82) plain reads, no lambdas: the page is polled many times a second.
            .Value first, then GetValue(); once .Value raised and GetValue() answered,
            GetValue() is asked first (a raise costs more than the read)."""
            ways = ("call", "value") if SLIDER_BY_CALL[0] else ("value", "call")
            raised = False
            for way in ways:
                try:
                    v = sl.Value if way == "value" else sl.GetValue()
                except Exception:
                    if way == "value":
                        raised = True
                    continue
                if v is not None:
                    try:
                        v = int(v)
                    except Exception:
                        continue
                    if raised and way == "call":
                        SLIDER_BY_CALL[0] = True
                    return v
            return default


        def checked(c, k, default):
            """(2.6.82) c[k].IsChecked, or default when it can't be read (no lambda)."""
            try:
                return bool(c[k].IsChecked)
            except Exception:
                return bool(default)


        def poll_config():
            c = page["c"]
            if c is None:
                return
            changed = False
            for k, _t, _tip in CHECKS_ALL:
                v = checked(c, k, settings[k])
                if v != settings[k]:
                    settings[k] = v
                    changed = True
                    # (2.6.81) "click": the frames' tooltips say what a click does
                    if k in ("lock", "status", "click"):
                        st["rebuild"] = True
                    if k == "party":
                        st["next_party"] = 0.0
                    if k == "mirror" and v:
                        st["mirror_now"] = True               # line the target up right away
            for k in ("scale", "pscale"):
                sc = max(SCALE_MIN, min(SCALE_MAX, slider_value(c[k], settings[k])))
                if sc != settings[k]:
                    settings[k] = sc
                    Kit.set_text(c[k + "_lbl"], "%d%%" % sc)
                    changed = True                    # party frames resize on the next tick
            on = checked(c, "pscale_on", settings["pscale_on"])
            if on != settings["pscale_on"]:
                settings["pscale_on"] = on
                changed = True
            if changed:
                st["art_dirty"] = True                # a size no frame uses any more is freed
            crop = False
            if Kit.was_clicked(page["store"], "retake"):
                page["layers"] = None                         # your own gear may have changed too
                st["crop_changed"] = 1.0                      # retake on the next tick
            if Kit.was_clicked(page["store"], "reset"):
                for k, _t in PORTRAIT_SLIDERS:
                    settings[k] = DEFAULTS[k]
                    safe(lambda: c[k].SetValue(DEFAULTS[k]))
                    Kit.set_text(c[k + "_lbl"], slider_text(k, DEFAULTS[k]))
                crop = True
            for k, _t in PORTRAIT_SLIDERS:
                lo, hi = NUMBERS[k]
                v = max(lo, min(hi, slider_value(c[k], settings[k])))
                if v != settings[k]:
                    settings[k] = v
                    Kit.set_text(c[k + "_lbl"], slider_text(k, v))
                    crop = True
            if crop:
                changed = True
                st["crop_changed"] = time.time()
                if st["art"] and st.get("running") and time.time() >= page["next_preview"]:
                    page["next_preview"] = time.time() + PREVIEW_EVERY   # live, but not every pass
                    draw_preview()
            if changed:
                save_settings()


        def config_closed():
            page["c"] = None
            page["layers"] = None             # read again (one hop) when the page next opens
            page["preview_gen"] = None        # (2.6.81) a preview half made is dropped


        def apply_crop(now):
            """Once the crop sliders settle (or Retake is pressed), retake every picture."""
            t = st["crop_changed"]
            if not t or now - t < CROP_SETTLE:
                return
            st["crop_changed"] = 0.0
            if st["art"]:
                if page["c"] is not None:
                    draw_preview()
                retake_all()


        # ---------- module hooks ----------
        def _start():
            st.update({"shutting": False, "queue": [], "rebuild": False, "docked": False,
                       "target": 0, "next_party": 0.0, "me": my_serial(), "snaps": {},
                       "stale": set(), "snap_queue": [], "art_scales": set(), "snap_px": None,
                       "party": set(), "next_supply": 0.0, "counts": {}, "snap_job": None,
                       "art_jobs": [], "art_failed": set(), "status": None, "screen": None,
                       "running": True, "recent": [], "next_prune": 0.0, "art_dirty": True,
                       "snap_tries": {}, "guard": None, "next_guard": 0.0,
                       "jr": None,                 # the cast bar's journal reader (cast_tick)
                       "dismissed": set(), "removing": False,     # (2.6.81)
                       "full_at": 0.0})            # (2.6.82) the next full tick (_tick)
            cast.update({"spell": None, "state": None, "shown": None})
            page["preview_want"] = False
            page["preview_gen"] = None             # (2.6.81)
            load_settings()
            load_tracked()
            load_positions()
            HOST.services["frames.player_anchor"] = player_anchor   # (2.6.85)
            st["minimized"] = _get(MIN_KEY, "0") == "1" or HOST.dock_wanted(KEY)   # as you left it
            st["min_saved"] = st["minimized"]
            st["mirror_now"] = False               # saved positions win at start-up
            st["pos_save_at"] = 0.0
            st["art"] = Bridge.find()
            if not st["art"]:
                API.SysMsg("Frames: this client doesn't allow drawn pictures; using stone "
                           "frames.", Kit.HUE_INFO)
            build_window()
            # the Frames window is rebuilt whole and never moves a control after it is
            # built, so the layout may scale it to its zone (2.6.55; an older mother
            # takes the plain hooks)
            try:
                hooks = Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"), scale=True)
            except TypeError:
                hooks = Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"))
            HOST.dock_add(KEY, hooks)
            if hasattr(HOST, "services"):          # other modules (Ultima Tracker) can ask for a bar
                HOST.services["unitframes.add"] = lambda serial: queue(("add_ext", int(serial)))()
            fitst["player"] = fitst["target"] = None
            fitbox["player"] = fitbox["target"] = None
            # the layout can slot the two frames, and fits each to its zone (2.6.55)
            for fk in ("player", "target"):
                # (2.6.60) "exact": the frame draws itself at its slot's size (frame_box)
                safe(lambda k=fk: _layout_add(KEY + "." + k, frame_gump(k), TITLE + " (" + k + ")",
                                              {"fit": frame_fit(k), "fill": "frame",
                                               "exact": True, "pieces_out": True,
                                               "hug": frame_hug(k),     # (2.6.72) corner zones
                                               # (2.6.74) no title row, by design (the mock-up)
                                               "untitled": True}))
                # (2.6.57) Bandages, the buff row and the Swing Bar ride on these two
                pieces_anchor(fk, frame_gump(fk), frame_span(fk), frame_inner(fk))
            PIECES_TARGET["fn"] = lambda: st["target"]


        def _tick():
            if win["g"] is None:
                return
            if Kit.was_clicked(win["store"], "close"):
                Kit.dispose(win["g"])            # on_disposed turns the module off
                return
            # (2.6.82) while a picture is made the part ticks at SNAP_TICK for its
            # thread work only: in between, the frames themselves keep their own
            # TICK_EVERY (a light tick starts the next picture in the queue)
            now = time.time()
            if now < st["full_at"] and not st["queue"] and not st["rebuild"] \
                    and now + 1.0 > st["full_at"]:
                if st["art"]:
                    take_next_snapshot(now)
                return
            st["full_at"] = now + TICK_EVERY - 0.005
            st["me"] = st["me"] or my_serial()
            update_target()                      # first, so "Add target" sees the newest target
            while st["queue"]:
                action = st["queue"].pop(0)
                kind = action[0] if isinstance(action, tuple) else action
                if action == "settings":
                    HOST.show_settings(KEY)
                elif action == "toggle_min":
                    st["minimized"] = not st["minimized"]
                    st["docked"] = False
                    HOST.dock_forget(KEY)                # its own minimized form, not the bar
                    build_window()
                elif action == "to_bar":
                    HOST.dock_to_bar(KEY, TITLE)         # folds in now, or once the bar is up
                elif action == "redraw":
                    build_window()
                elif action == "add_target":
                    add_tracked(st["target"] or int(safe(lambda: API.LastTargetSerial, 0) or 0))
                elif action == "pick":
                    API.SysMsg("Frames: choose who gets a frame.", Kit.HUE_INFO)
                    # a cursor that holds nothing up; the answer comes back as "picked"
                    HOST.pick_target(PICK_TIMEOUT, pick_answer("picked"))
                elif kind == "picked":                   # the Pick cursor's answer (0 = none)
                    if action[1]:
                        add_tracked(action[1])
                    else:                                # Esc, a timeout or another cursor
                        API.SysMsg("Frames: pick cancelled.", Kit.HUE_INFO)
                elif action == "add_frame":              # the window's Add frame (2.6.51)
                    serial = st["target"] or int(safe(lambda: API.LastTargetSerial, 0) or 0)
                    if serial and serial != st["me"] and not is_tracked(serial):
                        add_tracked(serial)
                    elif HOST.cursor_busy(KEY):
                        API.SysMsg("Frames: a target cursor is up; try again after it.",
                                   Kit.HUE_INFO)
                    else:
                        API.SysMsg("Frames: choose who gets a frame.", Kit.HUE_INFO)
                        HOST.pick_target(PICK_TIMEOUT, pick_answer("picked"))
                elif action == "remove_frame":           # the window's Remove frame (2.6.51)
                    if not tracked:
                        API.SysMsg("Frames: nobody else has a frame to remove (your own and the "
                                   "target frame are turned off on the settings page).",
                                   Kit.HUE_INFO)
                    elif HOST.cursor_busy(KEY):
                        API.SysMsg("Frames: a target cursor is up; try again after it.",
                                   Kit.HUE_INFO)
                    else:
                        API.SysMsg("Frames: click the person, or their frame, to remove.",
                                   Kit.HUE_INFO)
                        st["removing"] = True            # (2.6.81) a frame click answers it
                        HOST.pick_target(PICK_TIMEOUT, pick_answer("unpicked"))
                elif kind == "remove_click":             # (2.6.81) a frame click for Remove frame
                    serial = frame_serial(action[1])
                    if serial and st.get("removing") and safe(lambda: API.HasTarget(), False):
                        API.Target(serial)               # Remove frame's own pick cursor
                elif kind == "unpicked":                 # Remove frame's cursor answered
                    st["removing"] = False               # (2.6.81)
                    if not action[1]:
                        API.SysMsg("Frames: remove cancelled.", Kit.HUE_INFO)
                    elif is_tracked(action[1]):
                        name = next((t["name"] for t in tracked if t["serial"] == action[1]), "")
                        remove_tracked(action[1])
                        API.SysMsg("Frames: removed %s." % (name or "the frame"), Kit.HUE_INFO)
                    else:
                        API.SysMsg("Frames: they have no frame of their own.", Kit.HUE_INFO)
                elif action == "clear":
                    for t in tracked:
                        close_frame("m%d" % t["serial"])
                    del tracked[:]
                    save_tracked()
                    HOST.refresh_settings(KEY)
                    if settings["party"]:
                        API.SysMsg("Frames: cleared. Party members come back while 'Add a "
                                   "frame for each party member' is on.", Kit.HUE_INFO)
                    build_window()
                elif kind == "rm":
                    remove_tracked(action[1])
                elif kind == "click":
                    target_from_frame(action[1])
                elif kind == "follow":                   # Alt+click: auto-follow, again to stop
                    serial = frame_serial(action[1])
                    if serial:
                        Follow.toggle(serial, TITLE)
                elif kind == "follow_serial":            # Alt+click on an OTHERS' FRAMES row
                    Follow.toggle(action[1], TITLE)
                elif kind == "add_ext":                  # a bar asked for by another module
                    add_tracked(action[1])
                elif kind in ("closed", "xclose"):
                    key = action[1]
                    if kind == "xclose":                 # the frame's own X button
                        close_frame(key)
                    frames.pop(key, None)
                    if key in ("player", "target"):
                        settings[key] = False
                        save_settings()
                        HOST.refresh_settings(KEY)
                        API.SysMsg("Frames: %s frame hidden; tick it again on the Frames "
                                   "settings page." % key, Kit.HUE_INFO)
                    elif key[1:].isdigit():
                        remove_tracked(int(key[1:]))
            if st["rebuild"]:
                st["rebuild"] = False
                remember_positions()
                for key in list(frames):
                    close_frame(key)
            if st["art"]:
                px = snap_px()
                if st["snap_px"] != px:
                    st["snap_px"] = px
                    if st["snaps"]:
                        retake_all()                          # pictures are drawn to size
            now = time.time()
            if now >= st["next_party"]:
                st["next_party"] = now + PARTY_EVERY
                sync_party()
            sync_frames()                        # a frame whose size changed is redrawn here
            if st["art"] and st["art_dirty"]:    # a frame was (re)built or closed, art came in
                st["art_dirty"] = False
                prune_art()
            if now >= st["next_prune"]:
                st["next_prune"] = now + PRUNE_EVERY
                prune_people()
            for fr in frames.values():
                fr["moved"] = False
            watch_frames(now)                    # where each frame sits now; saves a drag
            rides = (rides_inside("player"), rides_inside("target"))
            if rides != st.get("rides"):         # (2.6.73) Bandages / the Swing Bar came or went:
                st["rides"] = rides              # the corner zones are worked out again
                safe(lambda: HOST.layout_refit())
            pieces_place()                       # (2.6.57) the pieces that ride on the frames
            if settings["mirror"]:
                mirror_frames(force=st.pop("mirror_now", False))
            cast_tick(now)                       # after watch_frames: follows where the frame is
            hbar_tick(now)                       # (2.6.85) TazUO's own target bar
            guard_tick(now)
            if st["art"]:
                take_next_snapshot(now)
            apply_crop(now)
            if now >= st["next_save"]:
                st["next_save"] = now + SAVE_EVERY
                remember_positions()             # belt and braces
                if st["pos_dirty"]:
                    save_positions()


        def _stop():
            st["shutting"] = True
            st["running"] = False
            st["removing"] = False               # (2.6.81)
            st["snap_job"] = None
            st["art_jobs"] = []
            page["preview_want"] = False
            page["preview_gen"] = None             # (2.6.81)
            HOST.dock_remove(KEY)
            if hasattr(HOST, "services"):
                HOST.services.pop("unitframes.add", None)
            drop_layout = getattr(HOST, "layout_remove", None)
            if drop_layout is not None:
                safe(lambda: drop_layout(KEY + ".player"))
                safe(lambda: drop_layout(KEY + ".target"))
            pieces_anchor("player", None)        # (2.6.57) the pieces are free windows again
            pieces_anchor("target", None)
            PIECES_TARGET["fn"] = None
            save_pos()
            save_positions()
            save_settings()
            save_tracked()
            HOST.services.pop("frames.player_anchor", None)
            try:
                hbar_sync(False)                 # (2.6.85) never left changed after we stop
            except Exception:
                pass
            for key in list(frames):
                fr = frames.pop(key)
                g, fr["g"] = fr.get("g"), None
                Kit.dispose(g)
            drop_cast()
            st["jr"] = None
            g, win["g"] = win["g"], None
            Kit.dispose(g)
            if st["art"] and st["textures"]:             # free the pictures this module made
                names = list(st["textures"])
                safe(lambda: Bridge.on_main(lambda: Bridge.drop_textures(names)))
                st["textures"].clear()
                st["art_scales"] = set()
            st["art"] = None          # found again at the next start; no preview while off


        def _thread_tick():
            """On the script's own thread, after a tick: the slow drawing (frame art,
            notoriety rings, pictures, the settings preview), a slice at a time,
            so none of it runs inside the game's frame."""
            if st["shutting"]:
                return
            if st["art_jobs"]:
                art_work(THREAD_BUDGET)
            if st.get("snap_job") is not None:
                snapshot_work(time.time(), THREAD_BUDGET)
            if page.get("preview_want"):
                page["preview_want"] = False
                if page["c"] is not None:
                    draw_preview_now()
            if page.get("preview_gen") is not None:      # (2.6.81) a slice at a time
                preview_work(THREAD_BUDGET)


        def _thread_busy():
            return bool(st.get("snap_job") or st["art_jobs"] or page.get("preview_want") or
                        page.get("preview_gen") is not None)


        def _interval():
            return SNAP_TICK if _thread_busy() else TICK_EVERY


        load_settings()
        # client_tick: the tick runs inside the game's frame, batched with the other
        # modules (every read there costs no wait); it never waits itself.
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True, "thread_tick": _thread_tick,
                  "interval": _interval, "thread_wanted": _thread_busy,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        # ============================= MODULE END ====================================
        return MODULE

    def _part_timers():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Assistant, loaded by the Virtue Assistant script from
        #  this file uses (API, G, safe, Client, Kit, Follow, HOST, Journal, the main
        #  its Modules tab.
        # ============================ MODULE START ===================================
        #  PART: Buffs & Timers  -  bars that count down what is on you and on others
        #
        #  - Your buffs: Bless, Agility, Cunning, Strength, Protection, Reactive
        #    Armor and Magic Reflection (until used up), Night Sight, Incognito,
        #    Invisibility and Polymorph.
        #  - What has been done to you: paralyze, poison and its level, Curse,
        #    Clumsy, Feeblemind and Weaken.
        #  - What you put on others: paralyze, poison, the curses, and buffs you
        #    cast on a friend. Alt+click such a row to auto-follow that mobile.
        #
        #  Where the timers come from:
        #  - The shard's buff icons, when it sends them (API.Events.OnBuffAdded /
        #    OnBuffRemoved, API.ActiveBuffs). The DEBUG box on the settings page
        #    prints every icon that comes in, to see what the shard sends.
        #  - Otherwise (a classic-era shard sends none): your own casts, from your
        #    words of power in the journal (the mother's Kit.SPELL_WORDS), timed
        #    with RunUO's pre-AoS spell durations (SPELLS below, from your Magery),
        #    landing on yourself or on the mobile you target. Expiry lines end a
        #    bar early, and the client's own flags end paralyze, poison,
        #    invisibility, polymorph and incognito the moment they wear off.
        #  - Bless and its kin on you, whoever cast them: a step of 2 or more in
        #    your Strength, Dexterity or Intelligence ("Watch your stats" on the
        #    settings page); all three at once is Bless / Curse. The bar ends when
        #    the stat steps back.
        #
        #  Other modules can read the timers: HOST.services["spelltimers.list"]
        #  (see svc_list below), e.g. for small icons under a unit frame.
        # =============================================================================
        KEY = "spelltimers"
        TITLE = "Buffs & Timers"

        # ------------------------------- CONFIG --------------------------------------
        SETTINGS_KEY = "SpellTimers_settings"   # per character: "me=1;debuff=1;others=1;..."
        POS_KEY = "SpellTimers_pos"
        MIN_KEY = "SpellTimers_min"
        ACTIVE_KEY = "SpellTimers_active"       # per character: the timers on you when it stopped
        TRAY_ICON = 0x0EFA                      # a spellbook on the Action Bar's tray button
        W = 360                                 # the full window (room for the title row)
        MINI_W, MINI_H = 320, 46                # (320: room for "Buffs & Timers: <spell> <time>")
        ROW_H = 28
        ROWS_MIN, ROWS_MAX, ROWS_DEFAULT = 3, 16, 8
        TICK = 0.1                              # seconds between ticks
        SAMPLE_EVERY = 0.2                      # seconds between looks at your flags and stats
        OTHERS_EVERY = 0.25                     # ... at the flags of the mobiles you cast on
        SKILL_EVERY = 15.0                      # ... at your Magery / Eval Int (and at every cast)
        ICON_RESYNC = 5.0                       # ... at API.ActiveBuffs, once the shard sent icons
        SPELL_ICON_BASE = 0x08C0                # classic magery icons (Clumsy = 0x08C0), as Grimoire
        ICON_PX = 22                            # the icons drawn this size in a row
        #  Your casts (words of power -> landing)
        CAST_FALLBACK = 1.0                     # cast delay of a spell Kit.spell_info doesn't know
        SELF_SLACK = 0.6                        # a self spell counts as landed this long after its delay
        PRE_SLACK = 1.2                         # a target spell whose cursor was never seen (pre-target,
        #                                         a quick last-target) lands on your last target then
        TARGET_TIMEOUT = 30.0                   # a target cursor left up longer is forgotten
        MANA_WAIT = 1.5                         # (2.6.81) seconds after a spell's cursor went away for
        #                                         your mana to drop (or your last target to change):
        #                                         neither = the cursor was cancelled, no bar (RunUO takes
        #                                         the mana when the target is chosen; UNCHECKED IN GAME)
        FAIL_AFTER = 1.0                        # a fail line this soon after a landing takes the bar back
        CONFIRM = 2.0                           # paralyze / poison / invisibility must show on the
        #                                         mobile within this long, or the bar is dropped
        LAND_WINDOW = 2.5                       # a stat step this soon after your self-cast is that spell
        #  Your stats
        STAT_MIN_STEP = 2                       # a step this big or bigger is a spell (1: a skill gain)
        STAT_MAX_STEP = 30                      # a bigger one is a new start (the status arrived, a
        #                                         body change), not a spell
        STAT_GROUP = 1.0                        # Str, Dex and Int stepping together within this: Bless /
        #                                         Curse
        STAT_EFFECTS_MAX = 4                    # steps remembered per stat
        #  Rows
        END_HOLD = 1.0                          # a timed bar stays this long at 0 before it goes
        UNTIL_USED_MAX = 3600.0                 # Reactive Armor / Magic Reflection rows go after this
        LINE_ONLY_MAX = 60.0                    # a paralyze known only from a line goes after this
        AWAY_DROP = 60.0                        # a mobile out of range this long (and its time up) goes
        TRACK_MAX = 40                          # rows kept at most (the oldest of others go first)
        RESTORE_MAX = 1800.0                    # timers saved at stop come back if this young
        PREV_CLICK = 0.15                       # a click this soon after a row changed acts on the old one
        ALERT_KIND = "spelltimers.ending"       # Settings > Alerts: "Buff about to run out"
        ALERT_SOUND = 0x1EA                     # chime (pick another on the Alerts page)
        WARN_MAX = 120

        #  The spells timed from your casts. UNCHECKED IN GAME: RunUO's pre-AoS
        #  values. side: "self" (always on you) or "target" (whoever you target);
        #  kind: "buff" / "debuff"; dur: (seconds, per Magery point, per Eval Int
        #  point, at least, at most; 0 = no limit), or None = until used up / until
        #  it wears off; most: the latest a ranged duration can end (Night Sight:
        #  15 to 39 minutes); watch: what ends it early ("stat", "paralyzed",
        #  "poisoned", "hidden", "body", "name" or None).
        SPELLS = {
            "Clumsy":           ("target", "debuff", (0, 1.2, 0, 0, 0), 0, "stat"),
            "Feeblemind":       ("target", "debuff", (0, 1.2, 0, 0, 0), 0, "stat"),
            "Weaken":           ("target", "debuff", (0, 1.2, 0, 0, 0), 0, "stat"),
            "Curse":            ("target", "debuff", (0, 1.2, 0, 0, 0), 0, "stat"),
            "Agility":          ("target", "buff", (0, 1.2, 0, 0, 0), 0, "stat"),
            "Cunning":          ("target", "buff", (0, 1.2, 0, 0, 0), 0, "stat"),
            "Strength":         ("target", "buff", (0, 1.2, 0, 0, 0), 0, "stat"),
            "Bless":            ("target", "buff", (0, 1.2, 0, 0, 0), 0, "stat"),
            "Night Sight":      ("target", "buff", (900, 0, 0, 0, 0), 2340, None),
            "Invisibility":     ("target", "buff", (0, 1.2, 0, 0, 0), 0, "hidden"),
            "Paralyze":         ("target", "debuff", (7, 0.2, 0, 0, 0), 0, "paralyzed"),
            "Poison":           ("target", "debuff", None, 0, "poisoned"),
            "Protection":       ("self", "buff", (0, 2.0, 0, 15, 240), 0, None),
            "Reactive Armor":   ("self", "buff", None, 0, None),
            "Magic Reflection": ("self", "buff", None, 0, None),
            "Incognito":        ("self", "buff", (1, 1.2, 0, 0, 144), 0, "name"),
            # 2.6.81: In Mani Ylem: Polymorph lasts 2x (rules skill, section 6)
            "Polymorph":        ("self", "buff", (0, 2.0, 0, 0, 240), 0, "body"),
        }
        #  Bless and its kin on you, from your stats: (stat, up / down) -> spell
        STAT_SPELLS = {("str", 1): "Strength", ("str", -1): "Weaken", ("dex", 1): "Agility",
                       ("dex", -1): "Clumsy", ("int", 1): "Cunning", ("int", -1): "Feeblemind"}
        #  Shard lines (cliloc.enu; lower case, matched at the start of a line):
        #  a line after your words that means the spell did nothing
        FAIL_TEXTS = ("the spell fizzles",                          # 502632
                      "your concentration is disturbed",            # 500641
                      "insufficient mana",                          # 502625
                      "more reagents are needed",                   # 502630
                      "target cannot be seen",                      # 500237
                      "that is too far away",                       # 500446
                      "target is too far away",                     # 500643
                      "this spell won't work on that",              # 501857
                      "this spell is already in effect",            # 501775 / 1005417 / 1005559
                      "the spell will not adhere to you",           # 1005385 ...
                      "you currently have a re",                    # 1005384 / 1005416 ... (reflect,
                      #                                               reactive armor already up)
                      "this target already has reactive armor",     # 502349
                      "incognito cannot be cast",                   # 501604
                      "you cannot disguise yourself",               # 501698 ...
                      "you cannot polymorph",                       # 502167 ...
                      "you cannot incognito",                       # 1010445
                      "you cannot cast that spell in this form")    # 1061091
        #  a line that ends a buff on you: (text, spell)
        END_TEXTS = (("your reactive armor spell has been nullified", "Reactive Armor"),  # 1005556
                     ("your protection spell has been nullified", "Protection"))          # 1005550
        #  a line that says a buff on you is still up (keeps its row): (text, spell)
        STILL_TEXTS = (("you currently have a reflect spell", "Magic Reflection"),       # 1005416 ...
                       ("you currently have a reactive armor spell", "Reactive Armor"))   # 1005384
        PARA_ON = ("you cannot move!",)                             # 502381
        PARA_OFF = ("you can move!", "you can move again!", "you are no longer frozen")  # 502382 ...
        #  poison on you (the overhead line), by level 1-5 (cliloc 1042857 + 2 x level)
        POISON_ME = (("you feel a bit nauseous", 1), ("you feel disoriented and nauseous", 2),
                     ("you begin to feel pain throughout your body", 3),
                     ("you feel extremely weak and are in severe pain", 4),
                     ("you are in extreme pain, and require immediate aid", 5))
        #  ... and on someone else (their overhead line, with their name in it)
        POISON_THEM = (("looks extremely ill", 2), ("looks ill", 1),
                       ("stumbles around in confusion and pain", 3),
                       ("is wracked with extreme pain", 4), ("begins to spasm uncontrollably", 5))
        POISON_OFF = ("the poison seems to have worn off",          # 502136
                      "you feel cured of poison",                   # 500231
                      "you have been cured of all poisons")         # 1008072 / 1010059
        POISON_NAMES = ("", "Lesser", "Regular", "Greater", "Deadly", "Lethal")
        #  shard buff icons that are debuffs (their names, without spaces, lower case)
        ICON_DEBUFFS = frozenset(("paralyze", "paralyzed", "poison", "curse", "clumsy",
                                  "feeblemind", "weaken", "mindrot", "strangle", "corpseskin",
                                  "evilomen", "bloodoath", "masscurse", "mortalstrike"))
        # -----------------------------------------------------------------------------

        COL = {"buff": (47, 154, 60), "debuff": (194, 45, 45), "other": (207, 174, 42),
               "dim": (90, 90, 90)}
        SPELL_WORDS = getattr(Kit, "SPELL_WORDS", None) or {}
        OWN_PREFIX = TITLE.lower() + ":"
        TEXT_PX = getattr(Kit, "text_px", None) or Kit.text_w
        FIT = getattr(Kit, "fit", None)

        def norm(name):
            return str(name or "").lower().replace(" ", "").replace("-", "")

        #  icon of every Magery spell (the spellbook order, as Grimoire draws them)
        ICONS = {}
        for _i, _sp in enumerate(getattr(Kit, "MAGERY", ()) or ()):
            ICONS[norm(_sp[0])] = SPELL_ICON_BASE + _i
        ICONS["paralyzed"] = ICONS.get("paralyze", SPELL_ICON_BASE)
        SPELL_OF = {}                           # norm name -> spell name, for SPELLS and STAT_SPELLS
        for _n in SPELLS:
            SPELL_OF[norm(_n)] = _n
        SPELL_OF["paralyzed"] = "Paralyzed"
        SPELL_ORDER = {"buff": 0, "debuff": 1}
        #  the timers on you kept over a restart of the script (save_active)
        KEEP_SIDS = frozenset(norm(n) for n, v in SPELLS.items() if v[1] == "buff")

        settings = {"me": True, "debuff": True, "others": True, "stats": True, "icons": True,
                    "rows": ROWS_DEFAULT, "warn": 0, "say": False}
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [],
              "rd": None, "pend": None, "landings": [], "last_land": None,
              "me": 0, "name": "", "prev_name": ("", 0.0), "dead": False,
              "para": None, "pois": None, "hidden": None, "body": 0, "stats": None,
              "next_sample": 0.0, "next_others": 0.0, "skills": (0.0, 0.0, -1e9),
              "events": [], "icons_seen": False, "next_icons": 0.0, "hooked": False,
              "ct": None, "ct_looked": False, "ver": 0, "warned": {}, "active": False,
              "redraw": False, "rebuild": False, "restored": False}
        rows = {}                               # (who, sid) -> row; who 0 = you
        effects = {"str": [], "dex": [], "int": []}    # stat steps on you (see apply_step)
        win = {"g": None, "c": {}, "store": ({}, {}), "slots": [], "nrows": 0}
        page = {"c": None, "seen": None}
        # (2.6.57) the buff row on the player frame (see build_row)
        ROW_ICON = 24                           # an icon in the row
        ROW_PITCH = 30                          # a cell: the icon, room for "1:05" under it
        ROW_LINE = 42                           # a line of the row: the icon and its time
        ROW_PAD = 3                             # black round the cells
        ROW_MAX = 24                            # cells at most (the newest first past this)
        FORM_EVERY = 0.5                        # seconds between looks at the player frame
        rowui = {"player": {"g": None, "cells": [], "per": 1, "lines": -1, "w": 0},
                 "target": {"g": None, "cells": [], "per": 1, "lines": -1, "w": 0}}


        # ---------- saved settings ----------
        def load_settings():
            for part in Kit.get_var(SETTINGS_KEY).split(";"):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                k, v = k.strip(), v.strip()
                if k in ("me", "debuff", "others", "stats", "icons", "say"):
                    settings[k] = v == "1"
                elif k in ("rows", "warn"):
                    try:
                        n = int(v)
                    except ValueError:
                        continue
                    if k == "rows":
                        settings[k] = max(ROWS_MIN, min(ROWS_MAX, n))
                    else:
                        settings[k] = max(0, min(WARN_MAX, n))

        def save_settings():
            parts = []
            for k in ("me", "debuff", "others", "stats", "icons", "say"):
                parts.append("%s=%d" % (k, 1 if settings[k] else 0))
            parts.append("rows=%d" % settings["rows"])
            parts.append("warn=%d" % settings["warn"])
            Kit.put_var(SETTINGS_KEY, ";".join(parts))

        def save_active():
            """The timers on you (with what the stat watcher knows), so a restart
            of the script picks them up again (see restore_active)."""
            now = time.time()
            parts = ["t=%d" % int(now)]
            for stat in ("str", "dex", "int"):
                for e in effects[stat]:
                    parts.append("e:%s,%d,%d,%d,%d" % (stat, e["d"], int(e["t"]), int(e["end"] or 0),
                                                       1 if e.get("hide") else 0))
            for r in rows.values():
                if r["who"] or "cast" not in r["srcs"] or "stat" in r["srcs"] or \
                        r["sid"] not in KEEP_SIDS:
                    continue
                parts.append("r:%s,%s,%d,%d,%d" % (r["sid"], r["kind"], int(r["start"]),
                                                   int(r["end"] or 0), int(r["most"] or 0)))
            Kit.put_var(ACTIVE_KEY, ";".join(parts))

        def restore_active(now):
            parts = Kit.get_var(ACTIVE_KEY).split(";")
            try:
                saved = float(parts[0].split("=", 1)[1]) if parts[0].startswith("t=") else 0.0
            except (ValueError, IndexError):
                saved = 0.0
            if not saved or not 0 <= now - saved <= RESTORE_MAX:
                return
            for p in parts[1:]:
                try:
                    tag, rest = p.split(":", 1)
                    b = rest.split(",")
                    if tag == "e" and b[0] in effects and settings["stats"]:
                        if len(effects[b[0]]) >= STAT_EFFECTS_MAX:
                            continue                # (a damaged save: the cap, as apply_step keeps)
                        d, t0, end = int(b[1]), float(b[2]), float(b[3])
                        if (end and end > now) or not end:
                            effects[b[0]].append({"d": d, "t": t0, "end": end or None,
                                                  "hide": len(b) > 4 and b[4] == "1"})
                    elif tag == "r" and b[0] in SPELL_OF:
                        start, end, most = float(b[2]), float(b[3]), float(b[4])
                        if end and max(end, most) <= now:
                            continue
                        r = new_row(0, b[0], b[1] if b[1] in SPELL_ORDER else "buff", start)
                        r["end"], r["most"] = end or None, most or None
                        r["srcs"].add("cast")
                except Exception:
                    continue
            st["restored"] = True


        # ---------- rows ----------
        def new_row(who, sid, kind, now, name=""):
            key = (who, sid)
            r = rows.get(key)
            if r is None:
                r = {"key": key, "who": who, "sid": sid, "kind": kind, "start": now, "end": None,
                     "most": None, "srcs": set(), "watch": None, "seen": False, "confirm": 0.0,
                     "base": None, "level": 0, "delta": 0, "name": name, "away": 0.0,
                     "icon": ICONS.get(sid, SPELL_ICON_BASE), "end_src": None}
                rows[key] = r
                if len(rows) > TRACK_MAX:
                    trim_rows(key)
            else:
                r["kind"] = kind
                if name:
                    r["name"] = name
            st["ver"] += 1
            return r

        def drop_row(key):
            if rows.pop(key, None) is not None:
                st["ver"] += 1
                st["warned"].pop(key, None)

        def drop_src(key, src):
            r = rows.get(key)
            if r is None:
                return
            r["srcs"].discard(src)
            if not r["srcs"]:
                drop_row(key)
            else:
                st["ver"] += 1

        def trim_rows(keep):
            """Over TRACK_MAX: the oldest rows about others go first, then yours."""
            order = sorted(rows.values(), key=lambda r: (r["who"] == 0, r["start"]))
            for r in order:
                if len(rows) <= TRACK_MAX:
                    break
                if r["key"] != keep:
                    rows.pop(r["key"], None)

        def text_key(r):
            """(2.6.82) Every field display_name and tip_of read: their texts are
            made again only when this changes."""
            return (r["sid"], r.get("label"), r["delta"], r["level"], r["who"], r["name"],
                    r["end"] is None, "stat" in r["srcs"])

        def display_name(r):
            sid = r["sid"]
            name = SPELL_OF.get(sid) or r.get("label") or sid
            if r["delta"]:
                name = "%s %+d" % (name, r["delta"])
            if r["level"] and sid in ("poison",):
                name = "%s (%s)" % (name, POISON_NAMES[max(1, min(5, r["level"]))])
            if r["who"]:
                name = "%s: %s" % (name, r["name"] or "someone")
            return name

        def dbg(text):
            if settings["say"]:
                API.SysMsg("%s: %s" % (TITLE, text), Kit.HUE_INFO)


        # ---------- durations ----------
        def skills(now, force=False):
            """(Magery, Eval Int), read on the client thread every SKILL_EVERY."""
            s = st["skills"]
            if force or not 0 <= now - s[2] < SKILL_EVERY:
                try:
                    mag = float(API.GetSkill("Magery").Value or 0)
                except Exception:
                    mag = s[0]
                try:
                    ev = float(API.GetSkill("Evaluating Intelligence").Value or 0)
                except Exception:
                    ev = s[1]
                s = st["skills"] = (mag, ev, now)
            return s

        def duration(spell, now):
            spec = SPELLS.get(spell)
            if spec is None or spec[2] is None:
                return None
            base, per_m, per_e, lo, hi = spec[2]
            mag, ev, _ = skills(now)
            secs = base + per_m * mag + per_e * ev
            if lo:
                secs = max(lo, secs)
            if hi:
                secs = min(hi, secs)
            return max(1.0, secs)


        # ---------- your casts ----------
        def on_words(spell, at, now):
            old = st["pend"]
            if old is not None:
                due = old["at"] + old["delay"]
                st["pend"] = None
                if old["side"] == "self" and at >= due - 0.05:
                    land(old, st["me"], due, now)   # a self spell whose delay is over: it landed
                elif old["side"] == "target" and not old["cursor"] and at >= due + 0.2:
                    try:                            # pre-targeted (no cursor came): on the last target
                        tgt = int(API.LastTargetSerial or 0)
                    except Exception:
                        tgt = 0
                    if tgt:
                        land(old, tgt, due, now)
                # (a target cursor still up is taken down by the new spell: it's over)
            spec = SPELLS.get(spell)
            if spec is None:
                st["pend"] = None                   # another spell: a target still pending is over
                return
            try:
                info = Kit.spell_info(spell)
            except Exception:
                info = None
            delay = info[3] if info and info[3] else CAST_FALLBACK
            skills(now, True)
            st["pend"] = {"spell": spell, "sid": norm(spell), "at": at, "delay": float(delay),
                          "side": spec[0], "cursor": False, "body0": st["body"], "name0": st["name"]}
            dbg("cast %s (%.2f s)" % (spell, delay))

        def resolve_pending(now):
            p = st["pend"]
            if p is None:
                return
            due = p["at"] + p["delay"]
            if now < due - 0.05:
                return
            if p["side"] == "self":
                if now >= due + SELF_SLACK:
                    st["pend"] = None
                    land(p, st["me"], due, now)
                return
            try:
                up = bool(API.HasTarget())
            except Exception:
                up = False
            if up:
                # 2.6.81: what the cursor is checked against once it goes away
                if not p["cursor"]:
                    p["cursor"] = True
                    try:
                        p["lt0"] = int(API.LastTargetSerial or 0)
                    except Exception:
                        p["lt0"] = 0
                try:
                    p["mana0"] = int(API.Player.Mana)
                except Exception:
                    p["mana0"] = None
                p["gone"] = None
                if now > due + TARGET_TIMEOUT:
                    st["pend"] = None
                return
            if not p["cursor"] and now < due + PRE_SLACK:
                return
            try:
                tgt = int(API.LastTargetSerial or 0)
            except Exception:
                tgt = 0
            if p["cursor"]:
                # 2.6.81: a cursor going away isn't a landing by itself (Esc / a
                # right-click leaves your last target as it was): wait for your mana
                # to drop or your last target to change; neither in MANA_WAIT = cancelled
                if p.get("gone") is None:
                    p["gone"] = now
                try:
                    mana = int(API.Player.Mana)
                except Exception:
                    mana = None
                # (mana not readable: as before, the cursor's going away is the landing)
                spent = mana is None or p.get("mana0") is None or mana < p["mana0"]
                if not spent and tgt == p.get("lt0", 0):
                    if 0 <= now - p["gone"] < MANA_WAIT:
                        return
                    st["pend"] = None
                    dbg("%s: cursor cancelled" % p["spell"])
                    return
            st["pend"] = None
            if tgt:
                land(p, tgt, now, now)
            else:
                dbg("%s: no target known" % p["spell"])

        def land(p, who, at, now):
            """Your spell p landed on `who` (a serial; yours = on you) at time at."""
            spell, sid = p["spell"], p["sid"]
            spec = SPELLS[spell]
            me = st["me"]
            on_me = not who or who == me
            dur = duration(spell, now)
            if on_me and spec[4] == "stat" and settings["stats"]:
                # the stat watcher shows it (it may have seen the step already)
                st["landings"].append({"sid": sid, "t": at, "dur": dur or 0.0})
                del st["landings"][:-6]
                attach_landing(now)
                dbg("%s landed on you" % spell)
                return
            name = ""
            if not on_me:
                try:
                    m = API.FindMobile(who)
                    name = str(m.Name or "") if m is not None else ""
                except Exception:
                    name = ""
            r = new_row(0 if on_me else who, sid, spec[1], at, name)
            r["start"] = at
            r["srcs"].add("cast")
            if r["end_src"] != "icon":
                r["end"] = (at + dur) if dur else None
                r["most"] = (at + spec[3]) if spec[3] else None
                r["end_src"] = "cast"
            r["delta"], r["away"] = 0, 0.0
            watch = spec[4]
            if watch == "stat":
                watch = None                        # on someone else: timed only
            if watch in ("body", "name") and not on_me:
                watch = None
            if watch == "hidden" and not on_me:
                watch = None                        # a hidden mobile is gone from view
            r["watch"], r["seen"] = watch, False
            r["confirm"] = now + CONFIRM
            if watch == "body":
                r["base"] = p["body0"]
            elif watch == "name":
                r["base"] = p["name0"]
            st["last_land"] = (r["key"], now)
            st["warned"].pop(r["key"], None)
            dbg("%s landed on %s" % (spell, "you" if on_me else (name or hex(who))))

        def cast_failed(now, during=False):
            """A fail line: it is about the spell pending when its delay is (about)
            over, or when it is a broken concentration (that comes while casting);
            else about the spell that just landed (a target too far away ...)."""
            p = st["pend"]
            if p is not None and (during or now >= p["at"] + p["delay"] - 0.3):
                dbg("%s did nothing" % p["spell"])
                st["pend"] = None
                return
            ll = st["last_land"]
            if ll is not None and 0 <= now - ll[1] <= FAIL_AFTER:
                st["last_land"] = None
                r = rows.get(ll[0])
                if r is not None and r["srcs"] == set(("cast",)):
                    drop_row(ll[0])


        # ---------- your stats (Bless and its kin on you) ----------
        def attach_landing(now):
            """Give a known end to the stat steps your own self-casts made."""
            lands = [l for l in st["landings"] if 0 <= now - l["t"] <= LAND_WINDOW + 1.0]
            st["landings"] = lands
            if not lands:
                return False
            hit = False
            for stat in ("str", "dex", "int"):
                for e in effects[stat]:
                    if e["end"] is not None or e["d"] <= 0 or not 0 <= now - e["t"] <= LAND_WINDOW + 1.0:
                        continue
                    for l in reversed(lands):
                        if l["sid"] in ("bless", norm(STAT_SPELLS[(stat, 1)])) \
                                and abs(e["t"] - l["t"]) <= LAND_WINDOW and l["dur"]:
                            e["end"], e["cast"] = l["t"] + l["dur"], l["sid"]
                            hit = True
                            break
            if hit:
                sync_stat_rows(now)
            return hit

        def apply_step(stat, d, now):
            effs = effects[stat]
            total = 0
            for e in effs:
                total += e["d"]
            if effs and total + d == 0:
                del effs[:]                         # back where it started: everything on it ended
                return
            for i, e in enumerate(effs):
                if e["d"] == -d:
                    del effs[i]                     # that one ended
                    return
            effs.append({"d": d, "t": now, "end": None})
            if len(effs) > STAT_EFFECTS_MAX:
                del effs[0]

        def stat_steps(vals, now):
            old = st["stats"]
            st["stats"] = vals
            if old is None:
                return
            changed = False
            for i, stat in enumerate(("str", "dex", "int")):
                d = vals[i] - old[i]
                if abs(d) > STAT_MAX_STEP:
                    del effects[stat][:]            # not a spell: a new start for this stat
                    changed = True
                elif abs(d) >= STAT_MIN_STEP:
                    apply_step(stat, d, now)
                    changed = True
                    dbg("%s %+d" % (stat.capitalize(), d))
            if changed:
                p = st["pend"]
                # a stat buff of yours still pending: the step says it landed on you
                if p is not None and p["side"] == "target" and SPELLS[p["spell"]][4] == "stat" \
                        and now >= p["at"] + p["delay"] - 0.4 and settings["stats"]:
                    st["pend"] = None
                    land(p, st["me"], now, now)
                attach_landing(now)
                sync_stat_rows(now)

        def sync_stat_rows(now):
            """The rows the stat steps make: Bless / Curse when all three stepped
            together by the same amount, else one per stat."""
            groups = {}
            used = set()
            S, D, I = effects["str"], effects["dex"], effects["int"]
            for a in S:
                if a.get("hide"):
                    continue
                for b in D:
                    if id(b) in used or b.get("hide") or b["d"] != a["d"] or \
                            abs(b["t"] - a["t"]) > STAT_GROUP:
                        continue
                    for c in I:
                        if id(c) in used or c.get("hide") or c["d"] != a["d"] or \
                                abs(c["t"] - a["t"]) > STAT_GROUP:
                            continue
                        used.update((id(a), id(b), id(c)))
                        sid = "bless" if a["d"] > 0 else "curse"
                        end = a["end"] or b["end"] or c["end"]
                        add_group(groups, sid, a["d"], min(a["t"], b["t"], c["t"]), end)
                        break
                    if id(a) in used:
                        break
            for stat in ("str", "dex", "int"):
                for e in effects[stat]:
                    if id(e) in used or e.get("hide"):
                        continue
                    sid = norm(STAT_SPELLS[(stat, 1 if e["d"] > 0 else -1)])
                    add_group(groups, sid, e["d"], e["t"], e["end"])
            for sid, g in groups.items():
                kind = "buff" if g[0] > 0 else "debuff"
                r = new_row(0, sid, kind, g[1])
                if "stat" not in r["srcs"]:
                    r["start"] = g[1]
                r["srcs"].add("stat")
                r["delta"] = g[0]
                if r["end_src"] != "icon":
                    r["end"], r["end_src"] = g[2], "stat"
                    r["most"] = None
            for key in [k for k, r in rows.items() if not r["who"] and "stat" in r["srcs"]
                        and r["sid"] not in groups]:
                r = rows[key]
                r["delta"] = 0
                drop_src(key, "stat")
            st["ver"] += 1

        def add_group(groups, sid, d, t, end):
            g = groups.get(sid)
            if g is None:
                groups[sid] = [d, t, end]
            else:
                g[0] += d
                g[1] = min(g[1], t)
                if end is not None and (g[2] is None or end > g[2]):
                    g[2] = end

        def clear_me():
            """You died: nothing is on you any more."""
            for key in [k for k in rows if not k[0]]:
                drop_row(key)
            for stat in effects:
                del effects[stat][:]
            st["stats"] = None
            st["pend"] = None
            st["landings"] = []
            st["para"] = st["pois"] = None          # read afresh


        # ---------- the client: your flags, the mobiles you cast on ----------
        def sample(now):
            try:
                p = HUD_ME() if HUD_ME is not None else API.Player   # (2.6.82) reads only
                if p is None:
                    return
                me = int(p.Serial)
                name = str(p.Name or "")
                dead = bool(p.IsDead)
                para = bool(p.IsParalyzed)
                pois = bool(p.IsPoisoned)
                hid = bool(p.IsHidden)
                body = int(p.Graphic or 0)
                vals = (int(p.Strength or 0), int(p.Dexterity or 0), int(p.Intelligence or 0))
            except Exception:
                return
            if me != st["me"]:
                if st["me"]:
                    clear_me()                      # another character: nothing of the old one is on you
                st["me"] = me
            if name != st["name"]:
                if st["name"]:
                    st["prev_name"] = (st["name"], now)
                st["name"] = name
            if dead:
                if not st["dead"]:
                    st["dead"] = True
                    clear_me()
                    dbg("you died: timers on you cleared")
                return
            if st["dead"]:
                st["dead"] = False
                st["stats"] = None                  # resurrected: a new start for your stats
            st["body"] = body
            # paralyze and poison on you (from anyone)
            if para != st["para"]:
                if st["para"] is not None:
                    dbg("paralyzed: %s" % para)
                st["para"] = para
                if para:
                    r = new_row(0, "paralyzed", "debuff", now)
                    r["srcs"].add("flag")
                else:
                    drop_row((0, "paralyzed"))
            if pois != st["pois"]:
                if st["pois"] is not None:
                    dbg("poisoned: %s" % pois)
                st["pois"] = pois
                if pois:
                    r = new_row(0, "poison", "debuff", now)
                    r["srcs"].add("flag")
                else:
                    drop_row((0, "poison"))
            st["hidden"] = hid
            # your own spells' watches
            for r in list(rows.values()):
                if r["who"] or r["watch"] is None:
                    continue
                w = r["watch"]
                if w == "hidden":
                    cur = hid
                    on = cur
                elif w == "body":
                    on = body != r["base"]
                elif w == "name":
                    on = name != r["base"]
                else:
                    continue
                if on:
                    r["seen"] = True
                elif r["seen"]:
                    drop_row(r["key"])              # it wore off
                elif w == "hidden" and now > r["confirm"]:
                    drop_row(r["key"])              # it never took
            if settings["stats"]:
                if vals[0] and vals[1] and vals[2]:  # (0: your status hasn't come yet)
                    stat_steps(vals, now)
            elif st["stats"] is not None or effects["str"] or effects["dex"] or effects["int"]:
                st["stats"] = None
                for stat in effects:
                    del effects[stat][:]
                sync_stat_rows(now)

        def watch_others(now):
            if not rows:
                return
            found = {}                              # (2.6.82) one FindMobile per mobile, not per row
            dead_of = {}
            for r in list(rows.values()):
                who = r["who"]
                if not who:
                    continue
                if who in found:
                    m = found[who]
                else:
                    try:
                        m = API.FindMobile(who)
                    except Exception:
                        m = None
                    found[who] = m
                if m is None:
                    if not r["away"]:
                        r["away"] = now
                        st["ver"] += 1
                    if r["watch"] and not r["seen"] and now > r["confirm"]:
                        drop_row(r["key"])          # gone before it showed: never confirmed
                    continue
                if r["away"]:
                    r["away"] = 0.0
                    st["ver"] += 1
                try:
                    dead = dead_of.get(who)
                    if dead is None:
                        dead = dead_of[who] = bool(m.IsDead)
                    if dead:
                        drop_row(r["key"])
                        continue
                    w = r["watch"]
                    if w == "paralyzed":
                        on = bool(m.IsParalyzed)
                    elif w == "poisoned":
                        on = bool(m.IsPoisoned)
                    else:
                        continue
                except Exception:
                    continue
                if on:
                    if not r["seen"]:
                        r["seen"] = True
                elif r["seen"]:
                    drop_row(r["key"])              # it wore off (or was cured / broken)
                elif now > r["confirm"]:
                    drop_row(r["key"])              # it never took (resisted, immune)


        # ---------- the journal ----------
        def read_journal(now):
            rd = st["rd"]
            if rd is None:
                try:
                    st["rd"] = Journal.reader()     # from now on: old words never start a bar
                except Exception:
                    st["rd"] = None
                return
            try:
                lines = rd.new()
            except Exception:
                return
            if not lines:
                return
            me_name = st["name"]
            prev, prev_at = st["prev_name"]
            for ln in lines:
                low = ln.low
                if low.startswith(OWN_PREFIX):
                    continue
                name = ln.name or ""
                mine = bool(me_name) and name == me_name or \
                    (prev and name == prev and 0 <= now - prev_at <= 5.0)
                if mine:
                    sp = SPELL_WORDS.get(low.strip())
                    if sp is not None:
                        on_words(sp[0], min(now, ln.at or now), now)
                        continue
                if name and not mine and name != "System":
                    them_poison(ln, low, name)
                    continue
                line_me(low, now, not mine)
                if settings["say"] and st["pend"] is not None:
                    dbg("line [%s]: %s" % (name or "-", ln.text.strip()))

        def line_me(low, now, system):
            """A system line (or one of your own overhead lines) about you or your
            spell; only the shard's own lines can fail a spell or end a buff."""
            txt = low.strip(" *")
            for t, lvl in POISON_ME:
                if txt.startswith(t):
                    r = new_row(0, "poison", "debuff", now)
                    r["srcs"].add("line")
                    if lvl != r["level"]:
                        r["level"] = lvl
                        st["ver"] += 1
                    return
            if not system:
                return
            for t in FAIL_TEXTS:
                if low.startswith(t):
                    for still, spell in STILL_TEXTS:
                        if low.startswith(still):
                            r = rows.get((0, norm(spell)))
                            if r is None:
                                r = new_row(0, norm(spell), "buff", now)
                            r["srcs"].add("cast")
                    p = st["pend"]
                    if p is not None and p["sid"] in ("reactivearmor", "magicreflection") and \
                            t == "this spell is already in effect" and (0, p["sid"]) not in rows:
                        new_row(0, p["sid"], "buff", now)["srcs"].add("cast")   # so it's up
                    cast_failed(now, t == "your concentration is disturbed")
                    return
            for t, spell in END_TEXTS:
                if low.startswith(t):
                    drop_row((0, norm(spell)))
                    return
            for t in PARA_ON:
                if low.startswith(t):
                    r = new_row(0, "paralyzed", "debuff", now)
                    r["srcs"].add("line")
                    return
            for t in PARA_OFF:
                if low.startswith(t):
                    drop_row((0, "paralyzed"))
                    return
            for t in POISON_OFF:
                if txt.startswith(t):
                    drop_row((0, "poison"))
                    return

        def them_poison(ln, low, name):
            """Someone's poison level line: "* <name> looks ill. *"."""
            for r in rows.values():
                if r["who"] and r["sid"] == "poison":
                    break
            else:
                return                              # none of yours is poisoned: nothing to read
            for t, lvl in POISON_THEM:
                if t in low:
                    nl = name.lower()
                    for r in rows.values():
                        if r["who"] and r["sid"] == "poison" and r["name"] and \
                                (r["name"].lower() == nl or r["name"].lower() in low):
                            if r["level"] != lvl:
                                r["level"] = lvl
                                st["ver"] += 1
                    return


        # ---------- the shard's buff icons ----------
        def on_buff_added(*args):
            on_buff_event("add", args)

        def on_buff_removed(*args):
            on_buff_event("remove", args)

        def on_buff_event(kind, args):
            """Script thread (the callback): only noted; the tick handles it."""
            if not st["active"]:
                return
            for a in args:
                title = getattr(a, "Title", None)
                if title is None:
                    continue
                try:
                    info = (kind, str(title or ""), int(getattr(a, "Graphic", 0) or 0),
                            int(getattr(a, "Timer", 0) or 0), str(getattr(a, "Type", "") or ""))
                except Exception:
                    return
                if len(st["events"]) < 60:
                    st["events"].append(info)
                return

        def hook_events():
            if st["hooked"]:
                return
            st["hooked"] = True
            ev = safe(lambda: API.Events)
            if ev is None:
                return
            try:
                ev.OnBuffAdded(on_buff_added)
            except Exception:
                pass
            try:
                ev.OnBuffRemoved(on_buff_removed)
            except Exception:
                pass

        def client_ms():
            """The client's own millisecond clock (ClassicUO.Time.Ticks), which a
            buff icon's Timer is counted on; None when it can't be read."""
            if not st["ct_looked"]:
                st["ct_looked"] = True
                try:
                    t = Client._type("ClassicUO.Time")
                    m = Client._member(t, "Ticks") if t is not None else None
                    st["ct"] = m[0] if m else None
                except Exception:
                    st["ct"] = None
            fn = st["ct"]
            if fn is None:
                return None
            try:
                return int(fn())
            except Exception:
                return None

        def icon_row(title, graphic, timer, now):
            sid = norm(title)
            if not sid:
                return
            kind = "debuff" if sid in ICON_DEBUFFS else "buff"
            r = new_row(0, sid, kind, now)
            if "icon" not in r["srcs"]:
                r["start"] = now
            r["srcs"].add("icon")
            r["label"] = title
            if graphic:
                r["icon"] = graphic
            end = None
            if 0 < timer < 0xFFFFFFFF:
                ct = client_ms()
                if ct is not None and timer > ct:
                    end = now + (timer - ct) / 1000.0
            if end is not None:
                r["end"], r["end_src"], r["most"] = end, "icon", None

        def handle_icons(now):
            evs, st["events"] = st["events"], []
            for kind, title, graphic, timer, btype in evs:
                dbg("buff icon %s: %s (graphic 0x%X, timer %d, type %s)"
                    % ("added" if kind == "add" else "removed", title or "-", graphic, timer, btype))
                if not settings["icons"]:
                    continue
                st["icons_seen"] = True
                if kind == "add":
                    icon_row(title, graphic, timer, now)
                else:
                    drop_src((0, norm(title)), "icon")
            if settings["icons"] and now >= st["next_icons"]:
                st["next_icons"] = now + ICON_RESYNC
                if not st["icons_seen"] and st["next_icons"] - ICON_RESYNC > st["started"] + 1.0:
                    return                          # looked once at start: the shard sends none
                try:
                    buffs = list(API.ActiveBuffs() or [])
                except Exception:
                    return
                present = set()
                for b in buffs:
                    try:
                        title = str(b.Title or "")
                        graphic, timer = int(b.Graphic or 0), int(b.Timer or 0)
                    except Exception:
                        continue
                    if not title:
                        continue
                    present.add(norm(title))
                    st["icons_seen"] = True
                    r = rows.get((0, norm(title)))
                    if r is None or "icon" not in r["srcs"]:
                        icon_row(title, graphic, timer, now)
                for key in [k for k, r in rows.items() if not k[0] and "icon" in r["srcs"]
                            and k[1] not in present]:
                    drop_src(key, "icon")


        # ---------- time going by ----------
        def expire(now):
            if not rows:
                return
            for r in list(rows.values()):
                key, srcs = r["key"], r["srcs"]
                end = r["end"]
                if r["who"] and r["away"] and now - r["away"] > AWAY_DROP and \
                        (end is None or now > end):
                    drop_row(key)                   # out of range this long, and its time is up
                    continue
                if "icon" in srcs or "stat" in srcs or "flag" in srcs:
                    continue                        # the shard / your stats / the flag say when
                if r["watch"] and r["seen"]:
                    continue                        # watched: it ends when the mobile says so
                if "line" in srcs and "cast" not in srcs:
                    if now - r["start"] > LINE_ONLY_MAX:
                        drop_row(key)
                    continue
                if end is None:
                    if not r["watch"] and now - r["start"] > UNTIL_USED_MAX:
                        drop_row(key)
                    continue
                if now > max(end, r["most"] or 0) + END_HOLD:
                    drop_row(key)

        def warn(now):
            lead = settings["warn"]
            if not lead or not settings["me"]:
                return
            for r in rows.values():
                if r["who"] or r["kind"] != "buff" or r["end"] is None:
                    continue
                left = r["end"] - now
                key = r["key"]
                if 0 < left <= lead:
                    if st["warned"].get(key) != r["end"]:
                        st["warned"][key] = r["end"]
                        safe(lambda: HOST.alert(ALERT_KIND, "%s runs out in %d s" % (
                            SPELL_OF.get(r["sid"], r.get("label") or r["sid"]), int(left + 0.5)),
                            "info", who=r["sid"]))


        # ---------- the window ----------
        queue = Kit.queuer(st)
        on_disposed = Kit.disposer(KEY, st, win)

        def save_pos():
            Kit.save_pos(POS_KEY, win["g"])

        def win_h(n):
            M = Kit.MARGIN
            return M + 30 + Kit.GAP + n * ROW_H + 12 + M

        def build_window():
            n = settings["rows"]
            w, h = (MINI_W, MINI_H) if st["minimized"] else (W, win_h(n))
            x, y = Kit.load_pos(POS_KEY, (60, 260), (w, h))
            if Kit.is_open(win["g"]):
                x, y = win["g"].GetX(), win["g"].GetY()
            old, win["g"] = win["g"], None
            M = Kit.MARGIN
            store = ({}, {})
            c = {}
            slots = []
            g = G.CreateGump(True, True)
            if st["minimized"]:
                c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
            else:
                IW = w - 2 * M
                Kit.add_window_frame(g, w, h)
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"))
                yb = M + 30 + Kit.GAP
                Kit.add_section(g, M, yb, IW, n * ROW_H + 12)
                c["empty"] = Kit.add_label(g, "", M + 12, yb + 10, Kit.HUE_INFO)
                for i in range(n):
                    slots.append(make_slot(g, i, M, yb + 6 + i * ROW_H, IW))
            Kit.place(g, x, y, w, h)
            win.update({"g": g, "c": c, "store": store, "slots": slots, "nrows": n})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))
            if st["minimized"] and st["docked"]:
                safe(lambda: setattr(g, "IsVisible", False))
            st["redraw"] = True
            draw(time.time())
            Kit.dispose(old)

        def make_slot(g, i, sx, ry, IW):
            s = {"i": i, "row": None, "prev": (None, 0.0), "vis": True, "icon_g": None,
                 "tip": None, "tx": None, "fw": -1, "col": None, "x": sx, "y": ry, "iw": IW}
            pic = None
            try:
                pic = G.CreateGumpPic(SPELL_ICON_BASE, sx + 6, ry + 2)
                pic.SetPos(sx + 6, ry + 2)
                pic.SetWidth(ICON_PX)
                pic.SetHeight(ICON_PX)
                pic.SetAcceptMouseInput(False)
                g.Add(pic)
            except Exception:
                pic = None
            s["pic"] = pic
            s["name"] = Kit.add_label(g, "", sx + 34, ry + 1, Kit.HUE_TEXT)
            s["time"] = Kit.add_label(g, "", sx + IW - 50, ry + 1, Kit.HUE_INFO)
            bw = IW - 34 - 10
            s["bw"] = bw
            s["bg"] = Kit.add_box(g, sx + 34, ry + 19, bw, 5, 0.9, "#202020")
            s["fill"] = Kit.add_box(g, sx + 34, ry + 19, bw, 5, 1.0, "#2f9a3c")
            s["hit"] = Kit.catcher(g, sx, ry, IW, ROW_H - 2, slot_click(i), "")
            set_vis(s, False)
            return s

        def slot_click(i):
            def handler(*args):
                slots = win["slots"]
                if i >= len(slots):
                    return
                s = slots[i]
                r = s["row"]
                prev, at = s["prev"]
                if 0 <= time.time() - at <= PREV_CLICK:
                    r = prev                        # it changed under the pointer: the one you saw
                if r is None:
                    return
                if r[0] and Follow.alt_held():
                    queue(("follow", r[0]))()       # Alt+click: auto-follow (standing rule)
                    return
                queue(("clear", r))()
            return handler

        def set_vis(s, on):
            if s["vis"] == on:
                return
            s["vis"] = on
            for k in ("pic", "name", "time", "bg", "fill", "hit"):
                ctl = s.get(k)
                if ctl is not None:
                    try:
                        ctl.IsVisible = on
                    except Exception:
                        pass

        def shown_rows():
            out = []
            for r in rows.values():
                if r["who"]:
                    if not settings["others"]:
                        continue
                elif r["kind"] == "buff":
                    if not settings["me"]:
                        continue
                elif not settings["debuff"]:
                    continue
                out.append(r)
            out.sort(key=row_order)
            return out

        def row_order(r):
            end = r["end"]
            return (1 if r["who"] else 0, SPELL_ORDER.get(r["kind"], 2),
                    end if end is not None else 1e18, r["start"])

        def fmt_secs(s):
            s = int(s + 0.999)
            if s < 60:
                return "%ds" % s
            if s < 3600:
                return "%d:%02d" % (s // 60, s % 60)
            return "%dh %02d" % (s // 3600, (s % 3600) // 60)

        def row_time(r, now):
            """(text, fill 0..1 or None, dim) for a row's time column."""
            end = r["end"]
            if end is None:
                if r["sid"] in ("reactivearmor", "magicreflection") and not r["who"]:
                    return "on", None, False
                return "+" + fmt_secs(max(0.0, now - r["start"])), None, False
            left = end - now
            if left > 0:
                total = max(0.1, end - r["start"])
                return fmt_secs(left), max(0.0, min(1.0, left / total)), False
            if r["most"] and now < r["most"]:
                return "soon", None, True
            return "due" if ("stat" in r["srcs"] or "icon" in r["srcs"]) else "0s", 0.0, True

        def tip_of(r):
            if r["who"]:
                return ("%s on %s, cast by you. Click: clear this row. Alt+click: auto-follow "
                        "(again to stop)" % (SPELL_OF.get(r["sid"], r["sid"]), r["name"] or "them"))
            if "stat" in r["srcs"] and r["end"] is None:
                return "From a step in your stats; it ends when the stat steps back. Click: clear this row."
            if r["end"] is None and r["sid"] in ("reactivearmor", "magicreflection"):
                return "Up until it is used up (the shard doesn't say when). Click: clear this row."
            return "Click: clear this row"

        # ---------- (2.6.57) the buff rows on the frames ----------
        #  While Frames shows the player frame, Buffs & Timers is no window: each
        #  buff, debuff and timed effect on you is one icon (its buff or spell
        #  icon) in a row that rides on the player frame (pieces_add: beyond
        #  Bandages, on the frame's game side), with its time left under it
        #  ("12s", "1:05"); an effect with no timer shows the icon alone. Your
        #  spells on your target get the same row on the target frame, beyond the
        #  Swing Bar. A row wraps to its frame's width and hides while it is empty.
        #  With Frames off, or the player frame hidden, the window comes back.
        SIDES = ("player", "target")
        PIECE = {"player": KEY, "target": KEY + ".target"}   # piece keys (never saved)

        def row_mode():
            return st.get("row_mode", False)

        def form_tick(now):
            """Rows or window: looked at every FORM_EVERY s (and at start)."""
            if 0 <= st.get("form_at", 0.0) - now <= FORM_EVERY:
                return
            st["form_at"] = now + FORM_EVERY
            fg = pieces_frame("player")
            want = fg is not None
            if want != row_mode():
                set_form(want)
            elif want:
                for side in SIDES:
                    ui = rowui[side]
                    fs = pieces_frame(side)
                    fw = ui["w"]
                    if fs is not None:
                        r = _rect_of(fs)             # (2.6.71) a frame just rebuilt reads 0 wide
                        if r is None:
                            continue                 # until it lands: read again next pass
                        fw = r[2]
                    if ui["g"] is None or fw != ui["w"]:
                        build_row(side, fw, max(0, ui["lines"]))

        def set_form(row):
            st["row_mode"] = row
            if row:
                HOST.dock_remove(KEY)                # no window, no tray button, no zone
                save_pos()
                g, win["g"] = win["g"], None         # replaced by us: doesn't turn it off
                win["slots"] = []
                Kit.dispose(g)
                for side in SIDES:
                    fw = 200
                    fs = pieces_frame(side)
                    r = _rect_of(fs) if fs is not None else None   # (2.6.71) as asked, until it lands
                    if r is not None:
                        fw = r[2]
                    build_row(side, fw, 0)
                pieces_add(PIECE["player"], "player", 1, lambda: rowui["player"]["g"])
                pieces_add(PIECE["target"], "target", 1, lambda: rowui["target"]["g"])
            else:
                drop_rows()
                build_window()
                HOST.dock_add(KEY, Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw")))
            st["redraw"] = True

        def drop_rows():
            for side in SIDES:
                pieces_remove(PIECE[side])
                ui = rowui[side]
                g, ui["g"] = ui["g"], None
                ui["cells"], ui["lines"], ui["w"] = [], -1, 0
                Kit.dispose(g)

        def build_row(side, fw, lines):
            """A row's window: fw wide (its frame's width), `lines` lines of cells
            (0: hidden until there is something to show). A pool of cells, each
            reassigned as the effects come and go."""
            ui = rowui[side]
            old, ui["g"] = ui["g"], None
            fw = max(ROW_PITCH + 2 * ROW_PAD, int(fw))
            per = max(1, (fw - 2 * ROW_PAD) // ROW_PITCH)
            h = max(1, lines) * ROW_LINE + 2 * ROW_PAD
            x, y = 0, 0
            if Kit.is_open(old):
                x, y = old.GetX(), old.GetY()
            g = G.CreateGump(True, False)
            Kit.add_section(g, 0, 0, fw, h, alpha=0.6)
            cells = []
            n = min(ROW_MAX, per * max(1, lines))
            x0 = ROW_PAD + (fw - 2 * ROW_PAD - per * ROW_PITCH) // 2
            for i in range(n):
                ln, col = divmod(i, per)
                cells.append(make_cell(g, side, i, x0 + col * ROW_PITCH, ROW_PAD + ln * ROW_LINE))
            Kit.place(g, x, y, fw, h)
            G.AddGump(g)
            safe(lambda: setattr(g, "IsVisible", lines > 0))
            ui.update({"g": g, "cells": cells, "per": per, "lines": lines, "w": fw})
            Kit.dispose(old)

        def make_cell(g, side, i, cx, cy):
            c = {"i": i, "row": None, "prev": (None, 0.0), "icon_g": None, "tip": None,
                 "vis": True, "x": cx, "y": cy, "tw": None, "who": 0}
            pic = None
            try:
                ix = cx + (ROW_PITCH - ROW_ICON) // 2
                pic = G.CreateGumpPic(SPELL_ICON_BASE, ix, cy)
                pic.SetPos(ix, cy)
                pic.SetWidth(ROW_ICON)
                pic.SetHeight(ROW_ICON)
                pic.SetAcceptMouseInput(False)
                g.Add(pic)
            except Exception:
                pic = None
            c["pic"] = pic
            c["time"] = Kit.add_label(g, "", cx, cy + ROW_ICON + 1, Kit.HUE_INFO)
            safe(lambda: c["time"].SetAcceptMouseInput(False))
            c["hit"] = Kit.catcher(g, cx, cy, ROW_PITCH, ROW_LINE - 2, cell_click(side, i), "")
            return c

        def cell_click(side, i):
            def handler(*args):
                cells = rowui[side]["cells"]
                if i >= len(cells):
                    return
                c = cells[i]
                r = c["row"]
                prev, at = c["prev"]
                if 0 <= time.time() - at <= PREV_CLICK:
                    r = prev                        # it changed under the pointer: the one you saw
                if r is None:
                    return
                if r[0] and Follow.alt_held():
                    queue(("follow", r[0]))()       # Alt+click: auto-follow (standing rule)
                    return
                queue(("clear", r))()
            return handler

        def cell_vis(c, on):
            if c["vis"] == on:
                return
            c["vis"] = on
            for k in ("pic", "time", "hit"):
                ctl = c.get(k)
                if ctl is not None:
                    try:
                        ctl.IsVisible = on
                    except Exception:
                        pass

        def draw_row(side, now, mine):
            ui = rowui[side]
            mine = mine[:ROW_MAX]
            per = ui["per"]
            lines = (len(mine) + per - 1) // per if mine else 0
            if lines != ui["lines"]:
                build_row(side, ui["w"] or 200, lines)   # the row's height follows (rare)
            if ui["g"] is None:
                return
            for i, c in enumerate(ui["cells"]):
                r = mine[i] if i < len(mine) else None
                key = r["key"] if r is not None else None
                if key != c["row"]:
                    c["prev"] = (c["row"], now)
                    c["row"] = key
                if r is None:
                    cell_vis(c, False)
                    continue
                cell_vis(c, True)
                icon = r["icon"]
                if icon != c["icon_g"] and c["pic"] is not None:
                    c["icon_g"] = icon
                    try:
                        c["pic"].Graphic = icon
                        c["pic"].SetWidth(ROW_ICON)
                        c["pic"].SetHeight(ROW_ICON)
                    except Exception:
                        pass
                text, _frac, dim = row_time(r, now)
                if r["end"] is None:
                    text = ""                       # no timer: the icon alone
                tw = TEXT_PX(text) if text else 0
                if tw != c["tw"]:
                    c["tw"] = tw
                    try:
                        Kit.ui_pos(c["time"], c["x"] + max(0, (ROW_PITCH - tw) // 2),
                                   c["y"] + ROW_ICON + 1)
                    except Exception:
                        pass
                Kit.set_text(c["time"], text, Kit.HUE_BAD if (dim or r["kind"] == "debuff")
                             else Kit.HUE_TEXT)
                tk = text_key(r)                    # (2.6.82) built again only on a change
                if tk != c.get("tipk"):
                    c["tipk"] = tk
                    tip = "%s. %s" % (display_name(r), tip_of(r))
                    if tip != c["tip"]:
                        c["tip"] = tip
                        try:
                            c["hit"].SetTooltip(tip)
                        except Exception:
                            pass

        def target_serial():
            """The serial the target frame shows (0: none), for its row."""
            fn = PIECES_TARGET.get("fn")
            if fn is None:
                return 0
            try:
                return int(fn() or 0)
            except Exception:
                return 0

        def draw(now):
            if row_mode():
                if not st["redraw"] and st.get("drawn_at", 0.0) + 0.25 > now >= st.get("drawn_at", 0.0) \
                        and st.get("drawn_ver") == st["ver"]:
                    return
                st["redraw"] = False
                st["drawn_at"], st["drawn_ver"] = now, st["ver"]
                shown = shown_rows()
                # 2.6.81: no target frame shown, no target row (it would sit loose at
                # the screen's corner); it comes back on the frame with the frame
                tgt = target_serial() if pieces_frame("target") is not None else 0
                mine, theirs = [], []
                for r in shown:
                    if not r["who"]:
                        mine.append(r)
                    elif tgt and r["who"] == tgt:
                        theirs.append(r)
                if rowui["player"]["g"] is not None:
                    draw_row("player", now, mine)
                if rowui["target"]["g"] is not None:
                    draw_row("target", now, theirs)
                return
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]):
                return                              # folded: nothing to draw
            if not st["redraw"] and st.get("drawn_at", 0.0) + 0.25 > now >= st.get("drawn_at", 0.0) \
                    and st.get("drawn_ver") == st["ver"]:
                return                              # nothing changed, and the seconds can wait
            st["redraw"] = False
            st["drawn_at"], st["drawn_ver"] = now, st["ver"]
            shown = shown_rows()
            c = win["c"]
            if st["minimized"]:
                lbl = c.get("status")
                if lbl is not None:
                    if shown:
                        t = row_time(shown[0], now)[0]
                        txt = "%s: %s %s" % (TITLE, display_name(shown[0]), t)
                        if len(shown) > 1:
                            txt += "  (+%d)" % (len(shown) - 1)
                        if FIT is not None:
                            txt = FIT(txt, MINI_W - 90)
                    else:
                        txt = "%s: no timers" % TITLE
                    Kit.set_text(lbl, txt, Kit.HUE_INFO)
                return
            slots = win["slots"]
            Kit.set_text(c["empty"], "" if shown else "No timers yet. Your buffs and casts show here.",
                         Kit.HUE_INFO)
            for i, s in enumerate(slots):
                r = shown[i] if i < len(shown) else None
                key = r["key"] if r is not None else None
                if key != s["row"]:
                    s["prev"] = (s["row"], now)
                    s["row"] = key
                if r is None:
                    set_vis(s, False)
                    continue
                set_vis(s, True)
                draw_slot(s, r, now)

        def draw_slot(s, r, now):
            icon = r["icon"]
            if icon != s["icon_g"] and s["pic"] is not None:
                s["icon_g"] = icon
                try:
                    s["pic"].Graphic = icon
                    s["pic"].SetWidth(ICON_PX)
                    s["pic"].SetHeight(ICON_PX)
                except Exception:
                    pass
            if r["who"]:
                hue, colk = (Kit.HUE_INFO if r["away"] else Kit.HUE_TITLE), "other"
            elif r["kind"] == "debuff":
                hue, colk = Kit.HUE_BAD, "debuff"
            else:
                hue, colk = Kit.HUE_TEXT, "buff"
            text, frac, dim = row_time(r, now)
            if r["who"] and r["away"]:
                text = text + " (away)"
            tw = TEXT_PX(text)
            tx = s["x"] + s["iw"] - 8 - tw
            if tx != s["tx"]:
                s["tx"] = tx
                try:
                    Kit.ui_pos(s["time"], tx, s["y"] + 1)
                except Exception:
                    pass
            Kit.set_text(s["time"], text, Kit.HUE_BAD if dim else Kit.HUE_INFO)
            tk = text_key(r)                        # (2.6.82) name and tip: only on a change
            room = tx - (s["x"] + 34) - 6
            nk = (tk, room)
            if nk != s.get("namek"):
                name = display_name(r)
                if FIT is not None:
                    name = FIT(name, max(20, room))
                s["namek"], s["name_txt"] = nk, name
            Kit.set_text(s["name"], s["name_txt"], hue)
            if frac is None:
                fw, colk = s["bw"], "dim"
            else:
                fw = int(round(s["bw"] * frac))
                if dim:
                    colk = "dim"
            if fw != s["fw"]:
                s["fw"] = fw
                fill = s["fill"]
                if fill is not None:
                    try:
                        if fw <= 0:
                            fill.IsVisible = False
                        else:
                            Kit.ui_w(fill, fw)
                            fill.IsVisible = True
                    except Exception:
                        pass
            if colk != s["col"] and s["fill"] is not None:
                s["col"] = colk
                rgb = COL[colk]
                try:
                    s["fill"].SetBaseColor(rgb[0], rgb[1], rgb[2], 255)
                except Exception:
                    pass
            if tk != s.get("tipk"):
                s["tipk"] = tk
                tip = tip_of(r)
                if tip != s["tip"]:
                    s["tip"] = tip
                    try:
                        s["hit"].SetTooltip(tip)
                    except Exception:
                        pass


        # ---------- the settings page ----------
        CFG_H = (140, 90, 64, 64)       # WINDOW, HOW TIMERS ARE FOUND, ALERTS, DEBUG

        def config_height(w):
            return sum(CFG_H) + 3 * Kit.GAP

        def build_config(g, x, y, w):
            c = {}
            Kit.add_section(g, x, y, w, CFG_H[0], "WINDOW  (what it lists)")
            c["me"] = Kit.add_check(g, "Show the buffs on you", x + 12, y + 30, settings["me"],
                                    "Bless, Strength, Protection, Reactive Armor, Magic Reflection, "
                                    "Night Sight, Incognito, Invisibility, Polymorph ...")
            c["debuff"] = Kit.add_check(g, "Show what is done to you (paralyze, poison, curses)",
                                        x + 12, y + 56, settings["debuff"],
                                        "Paralyzed, Poison (with its level), Curse, Clumsy, "
                                        "Feeblemind and Weaken on you")
            c["others"] = Kit.add_check(g, "Show your spells on others", x + 12, y + 82,
                                        settings["others"],
                                        "Paralyze, Poison, the curses and the buffs you cast on "
                                        "someone else. Alt+click such a row: auto-follow (again to "
                                        "stop)")
            Kit.add_label(g, "Rows shown:", x + 12, y + 112)
            rx = x + 24 + Kit.text_w("Rows shown:")
            c["rows"] = Kit.add_textbox(g, str(settings["rows"]), rx, y + 108, 40)
            safe(lambda: c["rows"].SetTooltip("Rows the window has room for (%d-%d)"
                                              % (ROWS_MIN, ROWS_MAX)))
            y2 = y + CFG_H[0] + Kit.GAP
            Kit.add_section(g, x, y2, w, CFG_H[1], "HOW TIMERS ARE FOUND  (your casts always count)")
            c["stats"] = Kit.add_check(g, "Watch your stats for Bless, Curse and their kin", x + 12,
                                       y2 + 30, settings["stats"],
                                       "A step of %d or more in your Str, Dex or Int is a spell on "
                                       "you, whoever cast it (all three at once: Bless / Curse); the "
                                       "bar ends when the stat steps back. A potion's bonus shows "
                                       "too." % STAT_MIN_STEP)
            c["icons"] = Kit.add_check(g, "Use the shard's buff icons when it sends them", x + 12,
                                       y2 + 56, settings["icons"],
                                       "A shard that sends buff icons gives exact names and times; "
                                       "a classic shard sends none (tick the DEBUG box to see)")
            y3 = y2 + CFG_H[1] + Kit.GAP
            Kit.add_section(g, x, y3, w, CFG_H[2], "ALERTS  (sound: Settings > Alerts)")
            Kit.add_label(g, "Warn before a buff on you runs out:", x + 12, y3 + 34)
            wx = x + 24 + Kit.text_w("Warn before a buff on you runs out:")
            c["warn"] = Kit.add_textbox(g, str(settings["warn"]), wx, y3 + 30, 40)
            safe(lambda: c["warn"].SetTooltip("Seconds before a timed buff on you runs out that "
                                              "one alert comes (0-%d, 0 = never)" % WARN_MAX))
            Kit.add_label(g, "s", wx + 48, y3 + 34, Kit.HUE_INFO)
            y4 = y3 + CFG_H[2] + Kit.GAP
            Kit.add_section(g, x, y4, w, CFG_H[3], "DEBUG  (for checking the shard's texts)")
            c["say"] = Kit.add_check(g, "Print every buff icon and cast in the journal", x + 12,
                                     y4 + 30, settings["say"],
                                     "Every buff icon the shard sends, your casts and where they "
                                     "landed, stat steps, and the lines that come while a spell is "
                                     "pending, so the shard's texts can be checked")
            page["c"] = c
            page["seen"] = (str(settings["rows"]), str(settings["warn"]))

        def poll_config():
            c = page["c"]
            if c is None:
                return
            try:
                ticks = {}
                for k in ("me", "debuff", "others", "stats", "icons", "say"):
                    ticks[k] = bool(c[k].IsChecked)
                texts = (str(c["rows"].Text).strip(), str(c["warn"].Text).strip())
            except Exception:
                return
            changed = False
            for k, v in ticks.items():
                if v != settings[k]:
                    settings[k] = v
                    changed = True
                    st["redraw"] = True
                    if k == "icons" and v:
                        st["next_icons"] = 0.0
            if texts != page["seen"]:
                page["seen"] = texts
                if texts[0].isdigit():
                    n = int(texts[0])
                    if ROWS_MIN <= n <= ROWS_MAX and n != settings["rows"]:
                        settings["rows"] = n
                        st["rebuild"] = True
                        changed = True
                if texts[1].isdigit():
                    n = int(texts[1])
                    if 0 <= n <= WARN_MAX and n != settings["warn"]:
                        settings["warn"] = n
                        st["warned"] = {}
                        changed = True
            if changed:
                save_settings()

        def config_closed():
            page["c"] = None


        # ---------- the service ----------
        def svc_list(serial=None):
            """HOST.services["spelltimers.list"](serial=None): the timers now, as a
            list of dicts {"spell", "serial", "you", "kind" ("buff" / "debuff"),
            "end" (time.time() it ends, None = not known), "left" (seconds, None),
            "icon" (gump art id), "level" (poison 1-5, else 0), "delta" (a stat
            step, else 0)}. serial: only the timers on that mobile (yours: your own
            serial). Reads nothing from the client: call it from any tick."""
            now = time.time()
            me = st["me"]
            out = []
            for r in rows.values():
                who = r["who"] or me
                if serial is not None and who != serial:
                    continue
                end = r["end"]
                out.append({"spell": SPELL_OF.get(r["sid"], r.get("label") or r["sid"]),
                            "serial": who, "you": not r["who"], "kind": r["kind"], "end": end,
                            "left": (end - now) if end is not None else None, "icon": r["icon"],
                            "level": r["level"], "delta": r["delta"]})
            return out


        # ---------- module hooks ----------
        def _start():
            now = time.time()
            st.update({"shutting": False, "docked": False, "queue": [], "rd": None, "pend": None,
                       "landings": [], "last_land": None, "para": None, "pois": None,
                       "hidden": None, "stats": None, "next_sample": 0.0, "next_others": 0.0,
                       "events": [], "icons_seen": False, "next_icons": 0.0, "warned": {},
                       "active": True, "redraw": True, "rebuild": False, "dead": False,
                       "started": now, "skills": (0.0, 0.0, -1e9),
                       "minimized": Kit.load_min(MIN_KEY)
                       or bool(safe(lambda: HOST.dock_wanted(KEY), False))})
            rows.clear()
            for stat in effects:
                del effects[stat][:]
            load_settings()
            restore_active(now)
            sync_stat_rows(now)
            hook_events()
            fn = getattr(HOST, "alert_kind", None)
            if fn is not None:
                safe(lambda: fn(ALERT_KIND, "Buff about to run out", ALERT_SOUND))
            st["row_mode"], st["form_at"] = False, 0.0
            if pieces_frame("player") is not None:   # (2.6.57) rows on the frames
                set_form(True)
            else:
                build_window()
                HOST.dock_add(KEY, Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw")))
            if hasattr(HOST, "services"):
                HOST.services["spelltimers.list"] = svc_list

        def _tick():
            now = time.time()
            form_tick(now)                          # (2.6.57) a row on the frame, or the window
            if win["g"] is None and not row_mode():
                return
            if win["g"] is not None and Kit.was_clicked(win["store"], "close"):
                Kit.dispose(win["g"])               # on_disposed turns the module off
                return
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
                    if not row_mode():
                        build_window()
                elif kind == "follow":
                    Follow.toggle(action[1], TITLE)
                elif kind == "clear":
                    clear_row(action[1], now)
            if st["rebuild"]:
                st["rebuild"] = False
                if not row_mode() and not st["minimized"] and settings["rows"] != win["nrows"]:
                    build_window()
            handle_icons(now)
            if not 0 <= st["next_sample"] - now <= SAMPLE_EVERY:
                st["next_sample"] = now + SAMPLE_EVERY
                sample(now)
            read_journal(now)
            resolve_pending(now)
            if any_others() and not 0 <= st["next_others"] - now <= OTHERS_EVERY:
                st["next_others"] = now + OTHERS_EVERY
                watch_others(now)
            expire(now)
            warn(now)
            draw(now)

        def any_others():
            for k in rows:
                if k[0]:
                    return True
            return False

        def clear_row(key, now):
            r = rows.get(key)
            if r is None:
                return
            if "stat" in r["srcs"]:
                # hide the stat steps behind it: they still take the step back when
                # it wears off (else that step would look like a new curse)
                for stat in ("str", "dex", "int"):
                    for e in effects[stat]:
                        sid = norm(STAT_SPELLS[(stat, 1 if e["d"] > 0 else -1)])
                        if sid == key[1] or (key[1] in ("bless", "curse")
                                             and (e["d"] > 0) == (key[1] == "bless")):
                            e["hide"] = True
            drop_row(key)
            if "stat" in r["srcs"]:
                sync_stat_rows(now)

        def _stop():
            st["shutting"] = True
            st["active"] = False
            HOST.dock_remove(KEY)
            if hasattr(HOST, "services") and HOST.services.get("spelltimers.list") is svc_list:
                HOST.services.pop("spelltimers.list", None)
            drop_rows()
            save_pos()
            Kit.save_min(MIN_KEY, st["minimized"])
            save_settings()
            save_active()
            g, win["g"] = win["g"], None
            win["slots"] = []
            Kit.dispose(g)

        load_settings()
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True,          # tick on the client thread: no waits in it
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        # ============================= MODULE END ====================================
        return MODULE

    def _part_swing():
        """Builds the module in its own namespace and returns its hooks."""
        # =============================================================================
        #  PART: Swing Bar  (was Swing Timer, from SwingTimer v1.6)
        #  Melee swing timer + hit chance HUD. Built for In Mani Ylem (pre-AoS /
        #  T2A-era rules, RunUO-style combat).
        #
        #  DISPLAY ONLY. This module never attacks, targets, heals, or eats for you.
        #  It reads game state and draws a small window. (IMY rules forbid automating
        #  any part of combat; this does not.)
        #
        #  What it shows (2.6.56: the same two-row panel as Bandages, one form only)
        #    * A bar that fills until your next swing, the seconds left beside it.
        #    * Under it: the chance to hit your current target (your weapon skill
        #      vs. their assumed weapon skill, adjusted for weapon accuracy and
        #      food satiety) at the left, and the satiety estimate at the right.
        #    * The weapon, its speed, the swing delay and the target are in the
        #      tooltips. The background opacity is set on its settings page.
        #
        #  How it syncs: on RunUO-style servers every melee swing (hit OR miss) plays
        #  the weapon's hit/miss sound on the attacker's tile. When such a sound plays
        #  on your tile, the timer restarts using the delay computed at that instant.
        #  Wrestling (fists) plays no sound on most RunUO cores, so for fists use the
        #  manual resync hotkey or let the bar free-run.
        #
        #  How it aims: it keeps the time between each of your last 10 swings with
        #  the weapon in hand and aims the bar at their average, recomputed on every
        #  swing. Each weapon has its own list, so swapping back picks up where that
        #  weapon left off. Until a weapon's first gap is measured it uses the
        #  formula's predicted delay. A swing that takes notably longer than the
        #  average (LONG_GAP_PCT) isn't counted: a stall, a lag spike or a step out
        #  of reach would otherwise drag the aim out. Three such slow swings in a
        #  row (SLOW_STREAK) mean you really do swing slower now (low stamina), and
        #  the list starts over from them.
        #
        #  The lists are saved between sessions in the per-character saved value
        #  "SwingTimer_history" (scripts only: no data file). One record per
        #  weapon, records separated by ";":
        #      Broadsword|45|1800,1750,1820,...;Katana|58|1500,1480
        #  Older versions kept them in "_swing_timer_<serial>.txt" next to Virtue
        #  Assistant: an existing file is read once, the first time this version
        #  runs for the character with nothing saved yet, and then left alone.
        #
        #  Notices (2.6.05, display only): a short line over the bar for a few
        #  seconds when the journal says you were disarmed or dismounted (with an
        #  alert, set on Settings > Alerts), and "Slow: low stamina" when slow
        #  swings in a row make the bar relearn a slower swing (SLOW_STREAK).
        # =============================================================================

        TITLE = "Swing Bar"                 # the window title, journal prefix and hotkey owner

        # ----------------------------------------------------------------------------
        #  CONFIG - everything you might want to tune lives here
        # ----------------------------------------------------------------------------

        # Pre-AoS RunUO:  delay(sec) = 15000 / ((STAMINA + 100) * weapon_speed)
        # OSI T2A docs often describe this as a dexterity bonus because max stamina
        # comes from dex. RunUO uses CURRENT stamina. Set to "dex" if IMY uses dex.
        SPEED_STAT = "stamina"        # "stamina" or "dex"
        SWING_CONSTANT = 15000.0      # numerator of the delay formula
        MIN_SWING_MS = 0              # set a floor if the shard has one (e.g. 1250)

        # Food satiety -> hit chance multiplier, in percent, by hunger level 0..20.
        # !!! PLACEHOLDER VALUES. IMY's real numbers aren't published anywhere I could
        # !!! find - ask staff / check the IMY wiki and edit this table. The current
        # !!! satiety estimate itself is set on the settings page (or the hotkeys).
        #   (lo, hi, percent_modifier, label)
        SATIETY_TABLE = [
            (0,  4,  -10, "Starving"),
            (5,  9,   -5, "Hungry"),
            (10, 14,   0, "Fed"),
            (15, 19,   0, "Full"),
            (20, 20,   0, "Stuffed"),
        ]
        HUNGER_DECAY_SECONDS = 300    # RunUO: hunger -1 every 5 minutes while online
        DEFAULT_HUNGER = 20           # starting guess if nothing saved

        # Enemy weapon skill can't be read by the client, so it's assumed.
        # Name keyword (lowercase) -> assumed weapon/wrestling skill. First match wins.
        # Approximate - fill in what you know for IMY's monsters.
        ENEMY_SKILL_BY_NAME = [
            ("lich lord", 90), ("lich", 70), ("dragon", 90), ("daemon", 90),
            ("troll", 60), ("ogre lord", 85), ("ogre", 65), ("orc captain", 80),
            ("orc", 55), ("ettin", 55), ("skeleton", 50), ("zombie", 35),
            ("rat", 25), ("headless", 30), ("mongbat", 10),
        ]
        DEFAULT_MONSTER_SKILL = 60    # first-run value of the "Enemy skill" box on the settings page
        DEFAULT_PLAYER_SKILL = 100    # assume GM for player characters (IsHuman)
        ENEMY_SKILL_MIN, ENEMY_SKILL_MAX = 0, 120

        # Hotkeys (TazUO format). Change if they clash with your setup.
        HK_SET_TARGET   = "CTRL+SHIFT+T"   # pick the mobile you're fighting
        HK_RESYNC       = "CTRL+SHIFT+R"   # "I just swung" - restart the bar now
        HK_HUNGER_UP    = "CTRL+SHIFT+UP"     # adjust satiety estimate +1
        HK_HUNGER_DOWN  = "CTRL+SHIFT+DOWN"   # adjust satiety estimate -1
        HK_ENEMY_UP     = "CTRL+SHIFT+RIGHT"  # assumed enemy skill +5
        HK_ENEMY_DOWN   = "CTRL+SHIFT+LEFT"   # assumed enemy skill -5

        WINDOW_X, WINDOW_Y = 300, 300   # first run; after that it opens where you left it

        # Window look: the shared stone frame with a black section inside (see Kit
        # at the top of the file). The stone border stays solid; the inside follows
        # the opacity slider in the Virtue Assistant window.
        DEFAULT_BG_OPACITY = 85       # percent, 0-100 (remembered between sessions)

        BAR_H = 8                     # swing bar thickness in pixels
        # The bar is the client's own status-bar line, hued per state (hue numbers);
        # the colours are only used if that art can't be loaded.
        BAR_FILL_HUE, BAR_FILL_COLOR = 0x0035, "#b8913a"      # filling up (gold)
        BAR_READY_HUE, BAR_READY_COLOR = 0x003F, "#3fa34d"    # swing ready (green)
        BAR_PAUSED_HUE, BAR_PAUSED_COLOR = 0x03B2, "#6b6b6b"  # out of combat (grey)

        # The timer pauses while you're out of combat: not in war mode, or no living
        # target. Time spent paused doesn't count toward the swing.

        # Learned swing time: the bar aims at the average gap between your last
        # SWING_HISTORY swings with the weapon in hand, recomputed on every swing.
        # A gap more than MAX_EXTRA_MS longer than the current aim (the average, or
        # the formula before there is one) is idle time (out of range, peace mode,
        # switching targets), not a swing, and isn't counted. A gap shorter than
        # MIN_GAP_MS is a doubled sound or a resync press, and isn't counted either.
        SWING_HISTORY = 10
        MAX_EXTRA_MS = 3000
        MIN_GAP_MS = 250
        # Once there is an average, a gap more than LONG_GAP_PCT percent longer than
        # it isn't counted. SLOW_STREAK such gaps in a row (each still within
        # MAX_EXTRA_MS of the average, so not idle time) replace the list instead:
        # your real swing speed has dropped.
        LONG_GAP_PCT = 15
        SLOW_STREAK = 3
        HISTORY_KEY = "SwingTimer_history"       # per character: every weapon's last swings
        OLD_DATA_FILE = "_swing_timer_{}.txt"    # {} = character serial; read once if present (see above)
        SAVE_EVERY_MS = 5000          # learned swings are saved at most this often (and on stop)

        # Notices on the bar (2.6.05; display only). Lower-case parts of the
        # shard's journal lines (Cliloc.enu; unchecked in game: the DEBUG box on
        # the settings page prints the lines that mention disarming / mounts).
        DISARM_TEXTS = ("you have been disarmed",          # 1004007 (wrestling disarm, pre-AoS)
                        "your weapon has been disarmed")   # 1060093 (the Disarm move)
        DISMOUNT_TEXTS = ("you have been knocked off",     # 1040023, 1042043, 1042046, 1049623
                          "you fall off of your mount",    # 1060083 (the Dismount move)
                          "you fall off your mount")       # 1062315
        NOTICE_FROM = ("system", "")  # who says them: the journal line's speaker (lower case)
        NOTICE_SECS = 4.0             # how long a notice stays over the bar
        NOTICE_EVERY_MS = 100         # the lines the shared journal holds are looked at this often
        NOTICE_MAX_MS = 500           # ...and the client's journal is read for them only when
        #                               nobody has for this long (a read walks the client's whole
        #                               journal; the host's guard-zone look makes one 4x a second)
        DEBUG_WORDS = ("disarm", " mount", "dismount")   # the DEBUG box prints lines with these
        ALERT_NOTICE = "swing.notice" # disarmed / dismounted alert (Settings > Alerts)
        ALERT_NOTICE_SOUND = 0x3B2    # smack

        # Pace of the tick's slower work (ms): the game lookups (weapon, target,
        # hunger), the sound-log fallback, your skill and the eating lines, the
        # seconds beside the bar (the bar itself moves every tick).
        SLOW_EVERY_MS = 250
        SOUND_POLL_MS = 100
        SKILL_EVERY_MS = 1000
        EAT_EVERY_MS = 1000
        COUNTDOWN_EVERY_MS = 100
        FAST_TICK = 0.025             # (2.6.82) the tick while the bar fills in combat
        SLOW_TICK = 0.1               # (2.6.82) the tick otherwise (a swing pokes the pass)
        EAT_LOOKBACK_S = 30.0         # eating lines older than this (client clock) are not counted

        # Hues for classic labels
        HUE_GREEN, HUE_YELLOW, HUE_RED, HUE_GREY = 68, 53, 33, 946
        HUE_TEXT = Kit.HUE_TEXT       # classic gump text

        # ----------------------------------------------------------------------------
        #  Weapon table: graphic -> (name, pre-AoS speed, skill, hit sound, miss sound)
        #  Speeds are RunUO DefOldSpeed values. Verify on IMY and edit if they differ.
        # ----------------------------------------------------------------------------
        SW, FE, MA, WR = "Swordsmanship", "Fencing", "Mace Fighting", "Wrestling"
        AR = "Archery"                # (2.6.81) bows and crossbows

        _W = [
            # Swords
            ("Broadsword",       45, SW, (0xF5E, 0xF5F)),
            ("Cutlass",          45, SW, (0x1441, 0x1440)),
            ("Katana",           58, SW, (0x13FF, 0x13FE)),
            ("Longsword",        35, SW, (0xF61, 0xF60)),
            ("Scimitar",         30, SW, (0x13B6, 0x13B5)),
            ("Viking Sword",     30, SW, (0x13B9, 0x13BA)),
            ("Thin Longsword",   35, SW, (0x13B8, 0x13B7)),
            ("Butcher Knife",    40, SW, (0x13F6, 0x13F7)),
            ("Cleaver",          40, SW, (0xEC3, 0xEC2)),
            ("Skinning Knife",   40, SW, (0xEC4, 0xEC5)),
            # Axes (Swordsmanship)
            ("Axe",              37, SW, (0xF49, 0xF4A)),
            ("Battle Axe",       31, SW, (0xF47, 0xF48)),
            ("Double Axe",       37, SW, (0xF4B, 0xF4C)),
            ("Executioner's Axe",37, SW, (0xF45, 0xF46)),
            ("Large Battle Axe", 29, SW, (0x13FB, 0x13FA)),
            ("Two Handed Axe",   31, SW, (0x1443, 0x1442)),
            ("Pickaxe",          35, SW, (0xE86, 0xE85)),
            ("Hatchet",          41, SW, (0xF43, 0xF44)),
            # Polearms (Swordsmanship)
            ("Bardiche",         26, SW, (0xF4D, 0xF4E)),
            ("Halberd",          25, SW, (0x143E, 0x143F)),
            # Fencing
            ("Dagger",           55, FE, (0xF52, 0xF51)),
            ("Kryss",            53, FE, (0x1401, 0x1400)),
            ("Short Spear",      50, FE, (0x1403, 0x1402)),
            ("Spear",            46, FE, (0xF62, 0xF63)),
            ("War Fork",         45, FE, (0x1405, 0x1404)),
            ("Pitchfork",        45, FE, (0xE87, 0xE88)),
            # Mace Fighting
            ("Club",             40, MA, (0x13B4, 0x13B3)),
            ("Hammer Pick",      30, MA, (0x143D, 0x143C)),
            ("Mace",             30, MA, (0xF5C, 0xF5D)),
            ("Maul",             30, MA, (0x143B, 0x143A)),
            ("War Axe",          40, MA, (0x13B0, 0x13AF)),
            ("War Hammer",       31, MA, (0x1439, 0x1438)),
            ("War Mace",         26, MA, (0x1407, 0x1406)),
            ("Quarter Staff",    48, MA, (0xE89, 0xE8A)),
            ("Gnarled Staff",    33, MA, (0x13F8, 0x13F9)),
            ("Black Staff",      35, MA, (0xDF0, 0xDF1)),
            ("Shepherd's Crook", 30, MA, (0xE81, 0xE82)),
            # Archery (2.6.81; RunUO OldSpeed: verify on IMY like the rest)
            ("Bow",              20, AR, (0x13B2, 0x13B1)),
            ("Crossbow",         18, AR, (0xF50, 0xF4F)),
            ("Heavy Crossbow",   10, AR, (0x13FD, 0x13FC)),
        ]
        WEAPONS = {}
        for _name, _spd, _skill, _gfx in _W:
            for _g in _gfx:
                WEAPONS[_g] = (_name, _spd, _skill)
        FISTS = ("Fists", 30, WR)

        # Every hit/miss sound RunUO weapons use. A sound with one of these IDs
        # on YOUR tile is your own swing resolving. (2.6.81) 0x234: a bow's or
        # crossbow's hit (RunUO BaseRanged; its miss is 0x238)
        SWING_SOUNDS = {0x232, 0x233, 0x234, 0x237, 0x238, 0x239, 0x23A, 0x23B, 0x23C}

        # Pre-AoS accuracy bonuses (percent), checked longest-first
        ACCURACY = [("supremely accurate", 10), ("exceedingly accurate", 8),
                    ("eminently accurate", 6), ("surpassingly accurate", 4),
                    ("accurate", 2)]

        # ----------------------------------------------------------------------------
        #  Pure math (no game calls) - easy to check by hand
        # ----------------------------------------------------------------------------

        def swing_delay_ms(stat_value, weapon_speed):
            """RunUO pre-AoS: 15000 / ((stam + 100) * speed) seconds."""
            v = (stat_value + 100) * weapon_speed
            if v <= 0:
                v = 1
            ms = SWING_CONSTANT / v * 1000.0
            return max(ms, MIN_SWING_MS)


        def base_hit_chance(atk_skill, def_skill, accuracy_pct=0):
            """RunUO pre-AoS CheckHit: (atk+50) / ((def+50)*2), scaled by accuracy."""
            atk = max(atk_skill, -49.9)
            dfn = max(def_skill, -49.9)
            chance = (atk + 50.0) / ((dfn + 50.0) * 2.0)
            chance *= 1.0 + accuracy_pct / 100.0
            return chance


        def satiety_info(hunger):
            h = int(round(max(0, min(20, hunger))))
            for lo, hi, mod, label in SATIETY_TABLE:
                if lo <= h <= hi:
                    return mod, label
            return 0, "?"


        def final_hit_chance(atk_skill, def_skill, accuracy_pct, hunger):
            mod, _ = satiety_info(hunger)
            c = base_hit_chance(atk_skill, def_skill, accuracy_pct) * (1.0 + mod / 100.0)
            return max(0.0, min(1.0, c))


        # ----------------------------------------------------------------------------
        #  Game-state helpers (all defensive - API details vary between TazUO builds)
        # ----------------------------------------------------------------------------

        def now_ms():
            return time.time() * 1000.0


        def skill_value(name):
            try:
                s = API.GetSkill(name)
            except Exception:
                return 0.0
            if s is None:
                return 0.0
            for attr in ("Value", "Base"):
                try:
                    return float(getattr(s, attr))
                except Exception:
                    pass
            try:
                return float(s)
            except Exception:
                return 0.0


        def current_weapon():
            """Returns (name, speed, skill, accuracy_pct)."""
            for layer in ("OneHanded", "TwoHanded"):
                try:
                    item = API.FindLayer(layer)
                except Exception:
                    item = None
                if not item:
                    continue
                g = int(getattr(item, "Graphic", 0))
                if g in WEAPONS:
                    name, spd, skill = WEAPONS[g]
                    return name, spd, skill, accuracy_of(item)
            return FISTS + (0,)


        # weapon serial -> (accuracy %, good until): an accurate weapon stays so;
        # "not accurate" is asked again now and then (its properties may arrive late)
        acc_cache = {}


        def accuracy_of(item):
            try:                                  # asked four times a second: no lambdas
                serial = int(item.Serial) or 0
            except Exception:
                serial = 0
            hit = acc_cache.get(serial) if serial else None
            if hit is not None and time.time() < hit[1]:
                return hit[0]
            text = ""
            try:
                text = (getattr(item, "Name", "") or "").lower()
            except Exception:
                pass
            if "accurate" not in text:
                try:
                    text = (API.ItemNameAndProps(item.Serial, False) or "").lower()
                except Exception:
                    pass
            pct = 0
            for key, p in ACCURACY:
                if key in text:
                    pct = p
                    break
            if serial:
                if len(acc_cache) > 50:
                    acc_cache.clear()
                acc_cache[serial] = (pct, time.time() + (1e9 if pct else 2.0))
            return pct


        STAT_ATTR = "Dexterity" if SPEED_STAT == "dex" else "Stamina"


        def speed_stat(p=None):
            if p is None:
                p = API.Player
            return int(getattr(p, STAT_ATTR, 0))


        def enemy_skill(mob, override, name=None):
            """name: the mobile's Name when the caller read it already (2.6.82)."""
            if override is not None:
                return override, "set"
            if mob is None:
                return cfg["enemy_default"], "default"
            if name is None:
                name = getattr(mob, "Name", "") or ""
            name = name.lower()
            for key, val in ENEMY_SKILL_BY_NAME:
                if key in name:
                    return val, "table"
            if getattr(mob, "IsHuman", False):
                return DEFAULT_PLAYER_SKILL, "player"
            return cfg["enemy_default"], "default"


        def load_var(key, default):
            try:
                return float(Kit.get_var(key, str(default)))
            except Exception:
                return float(default)


        def save_var(key, value):
            Kit.put_var(key, str(value))


        # settings tuned on the settings page (each its own swingtimer_* saved value)
        def clamp_enemy(v):
            try:
                return int(max(ENEMY_SKILL_MIN, min(ENEMY_SKILL_MAX, int(round(float(v))))))
            except Exception:
                return DEFAULT_MONSTER_SKILL

        cfg = {"enemy_default": clamp_enemy(load_var("swingtimer_enemy_default", DEFAULT_MONSTER_SKILL))}


        # ----------------------------------------------------------------------------
        #  State
        # ----------------------------------------------------------------------------

        class State:
            last_swing = None        # ms timestamp of last detected swing
            cycle_ms = None          # aim locked in at that swing (average, or formula)
            cycle_base_ms = None     # formula delay at that swing
            gaps = []                # ms between your last SWING_HISTORY swings (this weapon)
            gaps_weapon = None       # (name, speed) those gaps were swung with
            history = {}             # (name, speed) -> its gaps list; saved to the data file
            slow = []                # slow gaps in a row, not counted (yet)
            dirty = False            # history changed since the last save
            paused_at = None         # ms timestamp when the timer was paused
            target_serial = 0
            enemy_override = None
            hunger = DEFAULT_HUNGER  # (2.6.57) read per character in start (see _start)
            hunger_clock = now_ms()
            seen_sounds = set()
            sounds = []              # swing sounds heard, for the next tick: (id, x, y, time, ms)
            keys = []                # hotkey presses, for the next tick: (what, value)
            notice = None            # (text, hue, until ms) shown over the bar (2.6.05)

        S = State()


        def average_gap():
            """Mean of the measured gaps, or None before the first one."""
            if not S.gaps:
                return None
            return sum(S.gaps) / float(len(S.gaps))


        def match_weapon(weapon):
            """A different weapon swings at a different speed: switch to its own
            list (empty the first time). Returns True when the weapon changed."""
            wkey = (weapon[0], int(weapon[1]))
            if S.gaps_weapon == wkey:
                return False
            S.gaps_weapon = wkey
            S.gaps = S.history.setdefault(wkey, [])
            S.slow = []
            return True


        # ---- learned swing times, kept between sessions -----------------------------

        # The history lives in a per-character saved value (HISTORY_KEY). The tick
        # only sets "save"; the save itself, and the one-time read of an older
        # version's data file, run in thread_tick (on the script's thread, never
        # inside the game's frame).
        files = {"saved_at": 0.0, "save": False, "import": False}


        def parse_history(text, sep):
            """{(name, speed): [gaps]} from records "Name|speed|g1,g2,..." split by sep."""
            out = {}
            for rec in text.split(sep):
                p = rec.strip().split("|")
                if len(p) != 3 or not p[0]:
                    continue
                try:
                    spd = int(p[1])
                    gaps = [float(v) for v in p[2].split(",") if v.strip()]
                except Exception:
                    continue
                gaps = [g for g in gaps if g >= MIN_GAP_MS][-SWING_HISTORY:]
                if gaps:
                    out[(p[0], spd)] = gaps
            return out


        def load_history():
            """Every weapon's last swings from the saved value (nothing saved = none;
            then an older version's data file is read once, in thread_tick)."""
            S.history = {}
            S.gaps, S.gaps_weapon, S.dirty, S.slow = [], None, False, []
            raw = Kit.get_var(HISTORY_KEY)
            if raw:
                S.history = parse_history(raw, ";")
            files["import"] = not S.history       # nothing saved yet: look for the old file


        def import_old_file():
            """One-time read of "_swing_timer_<serial>.txt" (older versions) into the
            saved value. Script thread only (disk). The file is left as it is.
            Waits for the player serial if it isn't known yet (a start at login)."""
            if now_ms() < files.get("import_next", 0.0):
                return
            files["import_next"] = now_ms() + 1000.0     # the serial read waits a frame: once a second
            try:
                serial = int(API.Player.Serial)
            except Exception:
                serial = 0
            if not serial:
                return                            # try again on a later thread tick
            files["import"] = False
            try:
                path = os.path.join(API.ScriptPath, OLD_DATA_FILE.format(serial))
                if not os.path.exists(path):
                    return
                with open(path, "r") as f:
                    text = f.read()
            except Exception:
                return
            found = parse_history(text, "\n")
            n = 0
            for wkey, gaps in found.items():
                if not S.history.get(wkey):       # swings learned since the start win
                    S.history[wkey] = gaps
                    n += 1
            if not n:
                return
            S.gaps_weapon = None                  # match the weapon to its list again
            S.dirty = True
            save_history()
            API.SysMsg("%s: learned swings of %d weapon%s brought over from the old data "
                       "file." % (TITLE, n, "" if n == 1 else "s"), Kit.HUE_GOOD)


        def save_history():
            """The whole history into the saved value (compact: one record per weapon)."""
            files["save"] = False
            recs = ["%s|%d|%s" % (name.replace("|", "/").replace(";", "/"), spd,
                                  ",".join("%.0f" % g for g in gaps))
                    for (name, spd), gaps in sorted(S.history.items()) if gaps]
            Kit.put_var(HISTORY_KEY, ";".join(recs))
            S.dirty = False
            files["saved_at"] = now_ms()


        def count_gap(gap, formula):
            """Adds one measured gap to the weapon's list, if it counts."""
            avg = average_gap()
            if gap < MIN_GAP_MS or gap > (avg or formula) + MAX_EXTRA_MS:
                S.slow = []                         # doubled sound / idle time
                return
            if avg is not None and gap > avg * (1.0 + LONG_GAP_PCT / 100.0):
                S.slow.append(gap)                  # notably slow: not counted ...
                if len(S.slow) < SLOW_STREAK:
                    return
                S.gaps[:] = S.slow                  # ... unless it keeps happening
                S.slow = []
                set_notice("Slow: low stamina", HUE_YELLOW)
            else:
                S.slow = []
                S.gaps.append(gap)                  # the weapon's own list, in place
            if len(S.gaps) > SWING_HISTORY:
                del S.gaps[:-SWING_HISTORY]
            S.dirty = True


        def mark_swing(when_ms=None):
            when = when_ms if when_ms is not None else now_ms()

            # A swing while paused: drop the paused stretch first so it isn't
            # counted as lag, and restart the pause clock from this swing.
            if S.paused_at is not None:
                if S.last_swing is not None:
                    S.last_swing += max(0.0, when - S.paused_at)
                S.paused_at = when

            weapon = current_weapon()
            formula = swing_delay_ms(speed_stat(), weapon[1])
            swapped = match_weapon(weapon)

            # The gap since the last swing joins the last SWING_HISTORY gaps, unless
            # the weapon changed in between, it's idle time / a doubled sound, or
            # it took notably longer than the average.
            if S.last_swing is not None and not swapped:
                count_gap(when - S.last_swing, formula)

            S.last_swing = when
            S.cycle_base_ms = formula
            S.cycle_ms = average_gap() or formula


        # ---- sound-based swing detection -------------------------------------------

        # System.DateTime, imported once (None: not there, e.g. outside .NET)
        _dt = {"looked": False, "DateTime": None}


        def _datetime():
            if not _dt["looked"]:
                _dt["looked"] = True
                try:
                    from System import DateTime
                    _dt["DateTime"] = DateTime
                except Exception:
                    pass
            return _dt["DateTime"]


        def journal_ticks_now():
            """The client's clock in journal-time ticks (DateTime ticks)."""
            DateTime = _datetime()
            if DateTime is not None:
                try:
                    return float(DateTime.Now.Ticks)
                except Exception:
                    pass
            return time.time() * 1e7


        def _sound_age_ms(entry):
            DateTime = _datetime()
            if DateTime is None:
                return 0.0
            try:
                return max(0.0, (DateTime.Now - entry.Time).TotalMilliseconds)
            except Exception:
                return 0.0


        def sound_of(entry):
            """(id, x, y, time text, ms it played) of a swing sound, else None.
            No game calls: safe wherever the sound event arrives. The event fires
            for every sound the client plays, so the id is checked first and
            nothing else is read for the other sounds."""
            try:
                sid = int(entry.ID)
            except Exception:
                return None
            if sid not in SWING_SOUNDS:
                return None
            try:
                sx, sy = int(entry.X), int(entry.Y)
            except Exception:
                return None
            return (sid, sx, sy, str(getattr(entry, "Time", "")), now_ms() - _sound_age_ms(entry))


        def handle_sound(snd, p=None):
            """A swing sound on your own tile restarts the bar, timed to when it played."""
            sid, sx, sy, tstamp, when = snd
            if p is None:
                p = API.Player
            if p is None or sx != int(p.X) or sy != int(p.Y):
                return
            key = (sid, sx, sy, tstamp)
            if key in S.seen_sounds:
                return
            S.seen_sounds.add(key)
            if len(S.seen_sounds) > 200:
                S.seen_sounds.clear()
            mark_swing(when)


        def on_sound_event(*args):
            """Only noted here; the tick handles it (inside the game's frame, where
            reading your tile and weapon costs no waits). 2.6.82: a swing sound pokes
            the pass, so a bar resting on Ready (slow ticks) restarts at once."""
            for a in args:
                try:
                    a.ID
                except Exception:
                    continue
                snd = sound_of(a)
                if snd is not None and len(S.sounds) < 50:
                    S.sounds.append(snd)
                    if not loop.get("fast"):
                        xy = loop.get("xy")          # (2.6.83) only a swing on your tile
                        if xy is None or (snd[1], snd[2]) == xy:
                            HOST.poke()
                return


        SOUND_EVENTS_OK = False
        SOUND_HOOKED = False


        def hook_sounds():
            """Subscribe once; the handler is ignored while the module is off."""
            nonlocal SOUND_EVENTS_OK, SOUND_HOOKED
            if SOUND_HOOKED:
                return
            SOUND_HOOKED = True
            try:
                API.Events.SoundPlayed(_sound_event_guarded)
                SOUND_EVENTS_OK = True
            except Exception:
                pass


        def _sound_event_guarded(*args):
            if win.get("active"):
                on_sound_event(*args)


        def poll_sounds(p):
            try:
                entries = API.GetSoundLog(1.0)
            except Exception:
                return
            for e in entries or ():
                snd = sound_of(e)
                if snd is not None:
                    handle_sound(snd, p)


        # ---- notices over the bar (2.6.05) -----------------------------------------

        def set_notice(text, hue):
            S.notice = (text, hue, now_ms() + NOTICE_SECS * 1000.0)


        note = {"rd": None, "clock": 0.0,
                "debug": load_var("swingtimer_notice_debug", 0) >= 1,
                "own": (TITLE.lower(),)}      # starts of Virtue Assistant's own lines (own_starts)


        def own_starts():
            """The lower-case starts of Virtue Assistant's own journal lines: every
            module's title and the app's name. In TazUO a SysMsg line is spoken by
            "System", like the shard's own lines, so a module's line quoting the
            shard's text (a debug echo, this module's included) must not count."""
            own = set([TITLE.lower()])
            try:
                for t in [APP_NAME] + [s.title for s in HOST.slots]:
                    t = str(t or "").strip().lower()
                    if t:
                        own.add(t)
            except Exception:
                pass
            return tuple(own)


        def new_lines(rd):
            """The reader's new lines. While the shared journal was read lately (by
            any module or the host), only the lines it already holds are taken (as
            Reader.new does, without its read of the client's journal); else the
            reader reads."""
            try:
                if time.time() - Journal.read_at < NOTICE_MAX_MS / 1000.0:
                    return rd.new(False)              # held lines only: no read of its own
            except (AttributeError, TypeError):       # a host whose Journal differs
                pass
            return rd.new()


        def check_notices():
            """Journal lines since the last look (the shared Journal, read once a
            pass for every module): disarmed / dismounted -> a notice and an alert.
            Lines from before the module started are never looked at."""
            rd = note["rd"]
            if rd is None:
                return
            try:
                lines = new_lines(rd)
            except Exception:
                return
            own = note["own"]
            for ln in lines:
                low = ln.low
                if low.startswith(own):
                    continue                          # Virtue Assistant's own line, not the shard's
                if note["debug"]:
                    for wd in DEBUG_WORDS:
                        if wd in low:
                            API.SysMsg("%s: line \"%s\" (from %s)"
                                       % (TITLE, ln.text, ln.name or "-"), Kit.HUE_INFO)
                            break
                if str(ln.name or "").lower() not in NOTICE_FROM:
                    continue
                what = None
                for t in DISARM_TEXTS:
                    if t in low:
                        what = ("Disarmed!", "You were disarmed")
                        break
                if what is None:
                    for t in DISMOUNT_TEXTS:
                        if t in low:
                            what = ("Dismounted!", "You were dismounted")
                            break
                if what is not None:
                    set_notice(what[0], HUE_RED)
                    fn = getattr(HOST, "alert", None)
                    if fn is not None:
                        try:
                            fn(ALERT_NOTICE, what[1])
                        except Exception:
                            pass


        # ---- satiety estimate from eating messages ---------------------------------
        # RunUO Food.FillHunger messages and the hunger bands they imply
        EAT_MSGS = [
            ("simply too full to eat any more", 20, 20),
            ("but you are stuffed", 20, 20),
            ("but are still extremely hungry", 0, 4),
            ("begin to feel more satiated", 5, 9),
            ("you feel much less hungry", 10, 14),
            ("feel quite full after consuming", 15, 19),
        ]


        # the shared journal (the mother's Journal: read once a pass for every
        # module); the reader hands each line over once, so nothing is re-scanned
        # and no "seen" list is kept here. Made on the first look; that first look
        # also counts the eating lines of the last 30 s, as the old 30 s read did.
        eat_rd = {"rd": None}


        def check_eating():
            """Eating lines since the last look, each counted once. The journal is
            shared by every module: read through Journal, never cleared."""
            rd = eat_rd["rd"]
            try:
                if rd is None:
                    rd = eat_rd["rd"] = Journal.reader()
                    lines = Journal.recent(EAT_LOOKBACK_S)
                else:
                    lines = rd.new()
            except Exception:
                return
            if not lines:
                return
            now_ticks = journal_ticks_now()
            for ln in lines:
                # older than EAT_LOOKBACK_S by the client's own clock (e.g. lines that
                # came while the module was off): the old read never looked that far back
                if ln.ticks > 1e12 and (now_ticks - ln.ticks) / 1e7 > EAT_LOOKBACK_S:
                    continue
                txt = ln.low                      # lower-cased once by the mother, for every module
                for text, lo, hi in EAT_MSGS:
                    if text in txt:
                        guess = S.hunger + 3 if lo != hi else hi
                        S.hunger = float(max(lo, min(hi, guess)))
                        S.hunger_clock = now_ms()
                        FOOD_SEEN[0] = True       # (2.6.72) a meal seen: the colours mean something
                        save_var("swingtimer_hunger", S.hunger)
                        break


        def set_hunger(value):
            """The satiety estimate (0..20), set by hand: a hotkey or the settings page."""
            FOOD_SEEN[0] = True                   # (2.6.72) set by hand: shown in its colours
            S.hunger = float(max(0, min(20, value)))
            S.hunger_clock = now_ms()
            save_var("swingtimer_hunger", S.hunger)


        def decay_hunger():
            elapsed = now_ms() - S.hunger_clock
            step = HUNGER_DECAY_SECONDS * 1000.0
            if elapsed >= step:
                ticks = int(elapsed // step)
                S.hunger = max(0.0, S.hunger - ticks)
                S.hunger_clock += ticks * step
                save_var("swingtimer_hunger", S.hunger)


        # ---- hotkeys ---------------------------------------------------------------

        # A hotkey only notes what was pressed (and when); the next tick does it,
        # inside the game's frame, where the game reads cost no waits.
        MAX_PENDING_KEYS = 50          # presses kept for the next tick (a key held down repeats)
        FOLLOW_TIP = " Alt+click: auto-follow (again to stop)."   # (2.6.81) the bar and hit chance


        def note_key(what, value):
            if len(S.keys) < MAX_PENDING_KEYS:
                S.keys.append((what, value))
                HOST.poke()                   # (2.6.82) run at once, even on slow ticks


        def hk_set_target():
            note_key("target", None)


        def hk_resync():
            note_key("resync", now_ms())            # "I just swung": timed to the key press


        def hk_hunger(delta):
            note_key("hunger", delta)


        def hk_enemy(delta):
            note_key("enemy", delta)


        def on_target_picked(serial):
            """The "pick target" cursor's answer (0 = cancelled / timed out)."""
            if serial:
                S.target_serial = int(serial)
                S.enemy_override = None


        def run_keys():
            """The hotkeys pressed since the last tick, in order."""
            while S.keys:
                what, v = S.keys.pop(0)
                if what == "target":
                    API.SysMsg("%s: target the mobile you are fighting." % TITLE, Kit.HUE_INFO)
                    HOST.pick_target(10, on_target_picked)
                elif what == "resync":
                    mark_swing(v)
                elif what == "hunger":
                    set_hunger(round(S.hunger) + v)
                elif what == "enemy":
                    mob = resolve_target()
                    base, _ = enemy_skill(mob, S.enemy_override)
                    S.enemy_override = max(ENEMY_SKILL_MIN, min(ENEMY_SKILL_MAX, base + v))
                elif what == "follow":                   # Alt+click on the target row
                    mob = loop.get("mob")
                    if mob is not None:
                        Follow.toggle(int(getattr(mob, "Serial", 0) or 0), TITLE)
                    else:                                # (2.6.81) say why nothing happens
                        API.SysMsg("%s: no target to follow." % TITLE, Kit.HUE_INFO)


        HOTKEYS = ((HK_SET_TARGET, hk_set_target, "pick the mobile you fight"),
                   (HK_RESYNC, hk_resync, "restart the bar (I just swung)"),
                   (HK_HUNGER_UP, lambda: hk_hunger(1), "satiety estimate +1"),
                   (HK_HUNGER_DOWN, lambda: hk_hunger(-1), "satiety estimate -1"),
                   (HK_ENEMY_UP, lambda: hk_enemy(5), "enemy skill +5"),
                   (HK_ENEMY_DOWN, lambda: hk_enemy(-5), "enemy skill -5"))


        def not_typing(fn):
            """The hotkey does nothing while keys go into a text field (the chat
            line, any text box anywhere on screen)."""
            def run(*args):
                if not safe(lambda: HOST.typing(), False):
                    fn()
            return run


        def register_hotkeys(on):
            """Binds (or unbinds) the six hotkeys, and tells the host which keys this
            module holds (HOST.hotkeys_owned, the same "CTRL+SHIFT+T" spelling the
            Action Bar normalises its own keys to) so a bar cell can't take one.
            Each key is also listed on Settings > Keys (HOST.hotkey_note, 2.6.05;
            left out on a host without it)."""
            owned = getattr(HOST, "hotkeys_owned", None)
            note_key_fn = getattr(HOST, "hotkey_note", None)
            drop_key_fn = getattr(HOST, "hotkey_drop", None)
            for key, fn, what in HOTKEYS:
                combo = str(key).strip().upper().replace(" ", "")
                try:
                    if on:
                        API.OnHotKey(key, not_typing(fn))
                        if owned is not None:
                            owned[combo] = TITLE
                    else:
                        API.OnHotKey(key)          # no callback = unregister
                except Exception:
                    pass
                if not on and owned is not None:
                    owned.pop(combo, None)
                try:
                    if on and note_key_fn is not None:
                        note_key_fn(combo, TITLE, what)
                    elif not on and drop_key_fn is not None:
                        drop_key_fn(combo, TITLE)
                except Exception:
                    pass


        def resolve_target():
            """Explicit pick > client last target > nearest hostile within 2 tiles."""
            for serial in (S.target_serial, getattr(API, "LastTargetSerial", 0)):
                if serial:
                    try:
                        m = API.FindMobile(serial)
                    except Exception:
                        m = None
                    if m and not getattr(m, "IsDead", False):
                        return m
            try:
                N = API.Notoriety
                return API.NearestMobile([N.Gray, N.Criminal, N.Enemy, N.Murderer], 2)
            except Exception:
                return None


        # ----------------------------------------------------------------------------
        #  Window (2.6.56)
        #  The same two-row panel as Bandages: stone frame, black section, the
        #  client's red status line with a (hued) blue line growing over it and
        #  the seconds to the next swing beside it; under it "Hit 72%" at the left
        #  and "Food 14/20" at the right. No smaller form, no fold into the Action
        #  Bar and no buttons: the hotkeys and the settings page do the rest, and
        #  turning the part off hides it.
        # ----------------------------------------------------------------------------


        set_label = Kit.set_text


        # (2.6.85) the kite marker: display only, nothing moves or attacks. Run out for half
        # the swing, turn, and arrive back as it fills. Steps are measured from your own
        # movement; until then these (ms a tile, stock RunUO), by (mounted, running)
        STEP_FALLBACK = {(False, False): 400.0, (False, True): 200.0,
                         (True, False): 200.0, (True, True): 100.0}
        STEP_MIN_MS, STEP_MAX_MS = 50.0, 800.0
        STEP_GAP_MS = 700.0            # a longer gap between tiles isn't a step: you stood still
        STEP_WEIGHT = 0.15             # how much one measured step moves the average
        KITE_VAR = "swingtimer_kite"
        KITE_COLOR = {"close": "#E8C25A", "turn": "#3CD070", "far": "#E04040", "idle": "#C8C8C8"}
        KITE_HUE = {"close": Kit.HUE_TITLE, "turn": Kit.HUE_GOOD, "far": Kit.HUE_BAD, "idle": Kit.HUE_INFO}
        KITE_WORD = {"close": "too close", "turn": "turn now", "far": "too far", "idle": ""}
        kite = {"on": bool(int(load_var("swingtimer_kite", 1) or 0)), "steps": {}, "xy": None, "at": 0.0,
                "stat0": None, "swing0": None, "px": None, "state": None, "tiles": None, "word": ""}

        WIN_H = 58
        ROW1_Y, ROW2_Y = 16, 34        # the bar's top, the text row's top (window pixels)
        PAD = 3                        # black each side of the rows
        LAYOUT_KEY = "swing"           # this window in the layout's registry

        bg_opacity = max(0.0, min(100.0, load_var("swingtimer_bg_opacity", DEFAULT_BG_OPACITY)))

        win = {"w": 0, "bar_w": 109, "x1": 0, "row1": 0, "food_w": [0] * 21,
               "fill_w": -1, "fill_state": None,
               "shown": {},            # row -> what it was last drawn from (see _tick)
               "tips": {},             # catcher -> its tooltip as last set
               "active": False, "closing": False}
        ctl = {}                               # controls of the open window
        cfgui = {"opacity": None, "seen_opacity": None}


        def is_open():
            return Kit.is_open(ctl.get("gump"))


        def make_fill(hue, color, h):
            """One state of the bar: the client's blue status line, hued."""
            if Kit.pic_size(Kit.LINE_BLUE)[0] > 0:
                t = Kit.add_tiled(ctl["gump"], Kit.LINE_BLUE, win["x1"], ROW1_Y, 1, h, hue=hue)
                if t is not None:
                    return t
            b = G.CreateGumpColorBox(1.0, color)
            b.SetRect(win["x1"] + 1, ROW1_Y + 1, 1, h)
            safe(lambda: b.SetAcceptMouseInput(False))
            ctl["gump"].Add(b)
            return b


        def window_size():
            """The fixed two-row size: row 1 (the bar, 5 px, the readout sized for
            its widest text) and PAD each side make the black section; the stone
            frame is 8 px round it."""
            # (2.6.58) row 1 is the bar, 5 px and the width of "15.0s": exactly the
            # Bandages panel's row 1, so the two panels are the same width (161 px)
            win["row1"] = win["bar_w"] + 5 + max(Kit.text_w("15.0s"), readout_room())
            return win["row1"] + 2 * PAD + 16, WIN_H


        def build_window(x=None, y=None):
            saved = x is None
            if saved:
                x = int(load_var("swingtimer_x", WINDOW_X))
                y = int(load_var("swingtimer_y", WINDOW_Y))
            old = ctl.get("gump")
            ctl.clear()
            bw = Kit.pic_size(Kit.LINE_RED)[0]
            fh = Kit.pic_size(Kit.LINE_BLUE)[1] or BAR_H
            win["bar_w"] = bw or 109
            w, h = window_size()
            win["w"] = w
            win["x1"] = x1 = 8 + PAD
            if saved:
                x, y = Kit.adapt(x, y, w, h)    # a saved place: on the screen of today
            gump = G.CreateGump(True, True)
            Kit.place(gump, x, y, w, h)         # wholly on screen
            ctl["gump"] = gump
            Kit.add_window_frame(gump, w, h, corners=False)
            ctl["section"] = Kit.add_section(gump, 8, 8, w - 16, h - 16)
            PIECES["bg"][gump] = [ctl["section"]]    # (2.6.72) hidden while it rides inside a frame
            apply_opacity()

            # row 1: the bar (red line, one fill per state on top, only one shown)
            # and the seconds to the next swing beside it
            if bw > 0:
                Kit.add_pic(gump, Kit.LINE_RED, x1, ROW1_Y)
            else:
                Kit.add_tiled(gump, Kit.SECTION_TILE, x1, ROW1_Y, 109, 9, 1.0)
            ctl["fills"] = {"fill": make_fill(BAR_FILL_HUE, BAR_FILL_COLOR, fh),
                            "ready": make_fill(BAR_READY_HUE, BAR_READY_COLOR, fh),
                            "paused": make_fill(BAR_PAUSED_HUE, BAR_PAUSED_COLOR, fh)}
            for f in ctl["fills"].values():
                safe(lambda f=f: setattr(f, "IsVisible", False))
            # (2.6.85) the kite marker: one thin box per state (only one shows), and the
            # ideal distance in tiles beside it
            ctl["kite"] = {}
            for name, colour in KITE_COLOR.items():
                b = G.CreateGumpColorBox(1.0, colour)
                b.SetRect(x1, ROW1_Y - 1, 2, fh + 2)
                safe(lambda b=b: b.SetAcceptMouseInput(False))
                safe(lambda b=b: setattr(b, "IsVisible", False))
                gump.Add(b)
                ctl["kite"][name] = b
            ctl["kite_lbl"] = Kit.add_label(gump, "", x1, ROW1_Y - 2, HUE_TEXT)
            safe(lambda: ctl["kite_lbl"].SetAcceptMouseInput(False))
            kite.update({"px": None, "state": None, "tiles": None})
            ctl["swing"] = Kit.add_label(gump, "", x1 + win["bar_w"] + 5, ROW1_Y - 2, HUE_TEXT)
            # a notice over the bar (disarmed, dismounted, slow), hidden until one comes
            ctl["notice"] = nl = Kit.add_label(gump, "", x1 + 4, ROW1_Y - 2, HUE_RED)
            safe(lambda: nl.SetAcceptMouseInput(False))
            safe(lambda: setattr(nl, "IsVisible", False))
            # row 2: hit chance at the bar's left edge, satiety right-aligned to row 1
            ctl["hit"] = Kit.add_label(gump, "", x1, ROW2_Y, HUE_GREY)
            ctl["food"] = Kit.add_label(gump, "", x1 + win["row1"] - Kit.text_w("Food 20/20"),
                                        ROW2_Y, HUE_TEXT)
            win["food_w"] = [Kit.text_px("Food %d/20" % i) for i in range(21)]   # measured once
            # the tooltips: invisible areas over each part (a drag on them moves the
            # window); their texts follow what they describe (see set_tip)
            half = win["row1"] // 2
            # 2.6.81: the bar and the hit chance are about your target: Alt+click
            # follows it (standing rule); the click only queues
            ctl["tip_bar"] = Kit.catcher(gump, x1 - 2, ROW1_Y - 4, win["row1"] + 4, 18,
                                         target_click, bar_tip(None), movable=True)
            ctl["tip_hit"] = Kit.catcher(gump, x1 - 2, ROW2_Y - 2, half, 18,
                                         target_click, hit_tip(None), movable=True)
            ctl["tip_food"] = Kit.catcher(gump, x1 + half, ROW2_Y - 2, win["row1"] - half + 2, 18,
                                          lambda *a: None, food_tip(), movable=True)
            win["fill_w"], win["fill_state"], win["shown"], win["tips"] = -1, None, {}, {}
            win["notice_shown"] = None
            G.AddControlOnDisposed(gump, on_close(gump))
            G.AddGump(gump)
            safe(lambda: Kit.on_moved(gump, save_position))   # saved the moment you let go
            if old is not None:
                Kit.dispose(old)          # its close is ignored: ctl["gump"] is the new one


        def set_tip(key, text):
            """A part's tooltip, set only when its text changed."""
            c = ctl.get(key)
            if c is None or win["tips"].get(key) == text:
                return
            win["tips"][key] = text
            try:
                c.SetTooltip(text)
            except Exception:
                pass


        def target_click(*a):
            """2.6.81: Alt+click on the bar or the hit chance: auto-follow your target."""
            if safe(Follow.alt_held, False):
                note_key("follow", None)


        def bar_tip(info):
            """The bar's tooltip: info (weapon, speed, delay ms, learned swings) or None."""
            text = ("Time to your next swing. Green: ready. Grey: paused (not in war mode "
                    "or no target).")
            if info is not None:
                name, speed, delay, n = info
                text += " %s, speed %d, swing %.1f s (%s)." % (
                    name, speed, delay / 1000.0,
                    "learned from %d swing%s" % (n, "" if n == 1 else "s") if n else "formula")
            return text + FOLLOW_TIP


        def hit_tip(info):
            """The hit chance's tooltip: info (target, skill, yours, theirs, accuracy,
            satiety %) or None (no target)."""
            if info is None:
                return "Chance to hit your target. Set the target with %s.%s" % (HK_SET_TARGET,
                                                                                FOLLOW_TIP)
            who, skill, mine, theirs, acc, sat = info
            return ("Chance to hit %s: your %s %.1f vs their assumed %d, accuracy +%d%%, "
                    "satiety %+d%%. Set the target with %s.%s" % (
                        who[:20], skill, mine, theirs, acc, sat, HK_SET_TARGET, FOLLOW_TIP))


        def food_tip(label="", mod=0):
            # (2.6.72) the estimate's basis: -1 every 5 minutes online, a meal read from the journal
            return ("Satiety estimate%s, %+d%% to hit. It drops 1 every %d minutes and rises when "
                    "the journal shows you eat%s. Adjust with %s / %s." % (
                        (": " + label.lower()) if label else "", mod, HUNGER_DECAY_SECONDS // 60,
                        "" if FOOD_SEEN[0] else " (none seen yet, so it shows grey)",
                        HK_HUNGER_UP, HK_HUNGER_DOWN))


        def apply_opacity():
            a = bg_opacity / 100.0
            safe(lambda: ctl["section"].SetAlpha(a * Kit.SECTION_ALPHA))


        def set_fill(progress, state):
            """progress 0..1000; state 'fill' | 'ready' | 'paused'. Only one fill
            shows at a time: its width is set when it changes, and visibility only
            when a different fill (or none) is to show."""
            fw = int(win["bar_w"] * max(0, min(1000, progress)) / 1000)
            old_w, old_state = win["fill_w"], win["fill_state"]
            if fw == old_w and state == old_state:
                return
            win["fill_w"], win["fill_state"] = fw, state
            fills = ctl["fills"]
            was = old_state if old_w > 0 else None      # the fill on screen (None: none)
            now = state if fw > 0 else None
            if now is not None:
                try:
                    Kit.ui_w(fills[now], fw)
                except Exception:
                    pass
            if was != now:
                for key, on in ((was, False), (now, True)):
                    f = fills.get(key) if key is not None else None
                    if f is not None:
                        try:
                            f.IsVisible = on
                        except Exception:
                            pass


        def step_note(p, t):
            """(2.6.85) ms a tile, measured from your own movement while it runs on."""
            try:
                xy = (int(p.X), int(p.Y))
            except Exception:
                return
            was, at = kite["xy"], kite["at"]
            if xy == was:
                return
            kite["xy"], kite["at"] = xy, t
            if was is None:
                return
            tiles = max(abs(xy[0] - was[0]), abs(xy[1] - was[1]))
            dt = t - at
            if not (0 < tiles <= 4 and 0 < dt <= STEP_GAP_MS * tiles):
                return
            ms = max(STEP_MIN_MS, min(STEP_MAX_MS, dt / float(tiles)))
            mode = step_mode(p)
            old = kite["steps"].get(mode)
            kite["steps"][mode] = ms if old is None else old + (ms - old) * STEP_WEIGHT


        def step_mode(p):
            return (bool(getattr(p, "IsMounted", False)), bool(getattr(p, "IsRunning", True)))


        def step_ms(p):
            mode = step_mode(p)
            v = kite["steps"].get(mode)
            return v if v is not None else STEP_FALLBACK[mode]


        def kite_tiles(swing_ms, step):
            """The ideal distance: 1 + (swing / 2) / step, rounded down."""
            return int(1 + (swing_ms / 2.0) / max(1.0, step))


        def kite_state(dist, ideal):
            if dist is None:
                return "idle"
            return "close" if dist < ideal else ("turn" if dist == ideal else "far")


        def kite_draw(p, mob, cycle, stat, w_speed):
            """(2.6.85) The marker at the turn-back point of the bar, the tile count beside
            it and its hue from your distance to the target. Display only (R1). The swing
            of now is the bar's own, moved by how far your stamina moved since it began:
            so the marker sits at 50% and slides, with the count, when stamina changes."""
            marks = ctl.get("kite")
            if not marks:
                return
            lbl = ctl.get("kite_lbl")
            if not kite["on"] or S.notice is not None:
                if kite["state"] is not None:
                    marks[kite["state"]].IsVisible = False
                    kite["state"] = None
                    kite["tiles"] = None
                    Kit.set_text(lbl, "")
                return
            swing = float(cycle)
            if kite["swing0"] != S.last_swing or kite["stat0"] is None:
                kite["swing0"], kite["stat0"] = S.last_swing, stat
            elif stat != kite["stat0"]:
                base = swing_delay_ms(kite["stat0"], w_speed)
                if base > 0:
                    swing = swing * swing_delay_ms(stat, w_speed) / float(base)
            frac = max(0.02, min(0.98, (swing / 2.0) / max(1.0, float(cycle))))
            px = win["x1"] + int(win["bar_w"] * frac)
            tiles = kite_tiles(swing, step_ms(p))
            dist = None
            if mob is not None:
                try:
                    dist = int(mob.Distance)
                except Exception:
                    dist = None
            state = kite_state(dist, tiles)
            kite["word"] = KITE_WORD[state]
            if state != kite["state"]:
                if kite["state"] is not None:
                    marks[kite["state"]].IsVisible = False
                marks[state].IsVisible = True
                kite["state"] = state
                kite["px"] = None
                kite["tiles"] = None
            if px != kite["px"]:
                kite["px"] = px
                marks[state].SetPos(px, ROW1_Y - 1)
                lbl.SetPos(px + 4, ROW1_Y - 2)
            if tiles != kite["tiles"]:
                kite["tiles"] = tiles
                Kit.set_text(lbl, str(tiles), KITE_HUE[state])


        def on_close(g):
            def handler(*args):
                if win["closing"] or ctl.get("gump") is not g:
                    return                 # stopping, or an old window being replaced
                save_position()
                ctl.clear()
                HOST.disable("swing")
            return handler


        def save_position():
            g = ctl.get("gump")
            if Kit.is_open(g) and not pieces_on(LAYOUT_KEY):   # (2.6.57) not while it rides
                save_var("swingtimer_x", safe(lambda: g.GetX(), WINDOW_X))
                save_var("swingtimer_y", safe(lambda: g.GetY(), WINDOW_Y))


        def hue_for_chance(c):
            return HUE_GREEN if c >= 0.60 else (HUE_YELLOW if c >= 0.40 else HUE_RED)


        FOOD_SEEN = [False]       # (2.6.72) a meal seen in the journal (or set by hand) this session


        def hue_for_food(hunger):
            # (2.6.72) grey until a meal has been seen this session: before that the number
            # is only the estimate counting down from the last one, and turned red after
            # about 80 minutes with nothing eaten seen
            if not FOOD_SEEN[0]:
                return Kit.HUE_INFO
            return HUE_RED if hunger < 5 else (HUE_YELLOW if hunger < 10 else HUE_TEXT)


        # ---- settings in the Virtue Assistant window ------------------------------

        PAGE_HS = (96, 68, 100, 66)   # WINDOW (2.6.85: the kite box), HIT CHANCE, HOTKEYS, DEBUG


        def config_height(w):
            return sum(PAGE_HS) + 3 * Kit.GAP


        def satiety_text():
            """'14/20 Fed' for the settings page's satiety slider."""
            return "{:.0f}/20 {}".format(S.hunger, satiety_info(S.hunger)[1])


        def build_config(g, x, y, w):
            h_win, h_hit, h_keys, h_dbg = PAGE_HS
            Kit.add_section(g, x, y, w, h_win, "WINDOW")
            cfgui["kite"] = Kit.add_check(
                g, "Show the kite marker on the bar", x + 12, y + 62, kite["on"],
                "The turn-back point of the swing and the tiles to kite out; its colour says too "
                "close, turn now or too far")
            Kit.add_label(g, "Background opacity:", x + 12, y + 34)
            cfgui["opacity"] = Kit.add_slider(g, x + 24 + Kit.text_w("Background opacity:"), y + 38,
                                              160, 0, 100, bg_opacity)
            safe(lambda: cfgui["opacity"].SetTooltip(
                "How solid the black inside of the window is; the stone edge stays solid (0-100)"))
            cfgui["seen_opacity"] = int(round(bg_opacity))
            # the two placeholder numbers, tuned here instead of in the file
            y2 = y + h_win + Kit.GAP
            Kit.add_section(g, x, y2, w, h_hit, "HIT CHANCE")
            Kit.add_label(g, "Enemy skill:", x + 12, y2 + 34)
            cfgui["enemy"] = Kit.add_textbox(g, str(cfg["enemy_default"]),
                                             x + 12 + Kit.text_w("Enemy skill:") + 8, y2 + 30, 44)
            safe(lambda: cfgui["enemy"].SetTooltip(
                "Weapon skill assumed for a monster the name table doesn't know; players count "
                "as GM (%d-%d)" % (ENEMY_SKILL_MIN, ENEMY_SKILL_MAX)))
            cfgui["seen_enemy"] = str(cfg["enemy_default"])
            Kit.add_label(g, "Satiety estimate:", x + 220, y2 + 34)
            cfgui["satiety"] = Kit.add_slider(g, x + 380, y2 + 38, 120, 0, 20, int(round(S.hunger)))
            safe(lambda: cfgui["satiety"].SetTooltip(
                "How well fed you are, 0 (starving) to 20 (stuffed); a low value lowers the hit "
                "chance. Guessed from your eating lines; set it here when you know better."))
            cfgui["seen_satiety"] = int(round(S.hunger))
            cfgui["satiety_lbl"] = Kit.add_label(g, satiety_text(), x + 508, y2 + 34, Kit.HUE_INFO)
            y3 = y2 + h_hit + Kit.GAP
            Kit.add_section(g, x, y3, w, h_keys, "HOTKEYS")
            for i, (keys, what) in enumerate((
                    (_pair(HK_SET_TARGET, HK_RESYNC), "pick the target / restart the bar"),
                    (_pair(HK_HUNGER_UP, HK_HUNGER_DOWN), "satiety estimate +1 / -1"),
                    (_pair(HK_ENEMY_UP, HK_ENEMY_DOWN), "enemy skill +5 / -5"))):
                Kit.add_label(g, keys, x + 12, y3 + 30 + i * 20, Kit.HUE_INFO)
                Kit.add_label(g, what, x + 330, y3 + 30 + i * 20, Kit.HUE_INFO)
            y4 = y3 + h_keys + Kit.GAP
            Kit.add_section(g, x, y4, w, h_dbg, "DEBUG  (for checking the shard's texts)")
            cfgui["debug"] = Kit.add_check(
                g, "Print the lines about disarming and mounts in the journal", x + 12,
                y4 + 30, note["debug"],
                "Every journal line that mentions disarming or a mount, with who said it, so the "
                "texts the Disarmed / Dismounted notices look for can be checked")


        def _pair(a, b):
            """'CTRL+SHIFT+T', 'CTRL+SHIFT+R' -> 'CTRL+SHIFT+T / R'."""
            pa, pb = a.rsplit("+", 1), b.rsplit("+", 1)
            if len(pa) == 2 and len(pb) == 2 and pa[0] == pb[0]:
                return "%s / %s" % (a, pb[1])
            return "%s / %s" % (a, b)


        def config_closed():
            for k in ("opacity", "enemy", "satiety", "satiety_lbl", "debug", "kite"):
                cfgui[k] = None


        def poll_config():
            nonlocal bg_opacity
            sl = cfgui["opacity"]
            if sl is None:
                return
            try:                                  # polled many times a second: no lambdas
                v = int(sl.Value)
            except Exception:
                v = cfgui["seen_opacity"]
            if v is not None and v != cfgui["seen_opacity"]:
                cfgui["seen_opacity"] = v
                bg_opacity = float(max(0, min(100, v)))
                save_var("swingtimer_bg_opacity", bg_opacity)
                if is_open():
                    apply_opacity()
            # the assumed enemy skill (number box): applied and saved when it changes
            try:
                txt = str(cfgui["enemy"].Text or "").strip()
            except Exception:
                txt = cfgui["seen_enemy"]
            if txt != cfgui["seen_enemy"]:
                cfgui["seen_enemy"] = txt
                if txt:
                    cfg["enemy_default"] = clamp_enemy(txt)
                    save_var("swingtimer_enemy_default", cfg["enemy_default"])
                    loop["slow_clock"] = 0.0      # the target's assumed skill follows at once
            # the satiety estimate (slider): moved by hand -> the estimate; else the
            # label beside it follows the estimate as it decays or you eat
            try:
                sat = int(cfgui["satiety"].Value)
            except Exception:
                sat = cfgui["seen_satiety"]
            if sat != cfgui["seen_satiety"]:
                cfgui["seen_satiety"] = sat
                set_hunger(sat)
            lbl = cfgui["satiety_lbl"]
            if lbl is not None:
                Kit.set_text(lbl, satiety_text())
            kc = cfgui.get("kite")
            if kc is not None:
                try:
                    on = bool(kc.IsChecked)
                except Exception:
                    on = kite["on"]
                if on != kite["on"]:
                    kite["on"] = on
                    save_var(KITE_VAR, 1 if on else 0)
            db = cfgui.get("debug")
            if db is not None:
                try:
                    on = bool(db.IsChecked)
                except Exception:
                    on = note["debug"]
                if on != note["debug"]:
                    note["debug"] = on
                    save_var("swingtimer_notice_debug", 1 if on else 0)


        # ----------------------------------------------------------------------------
        #  Module: start / one pass / stop
        # ----------------------------------------------------------------------------
        loop = {}                              # per-pass state, filled in by _start


        def _start():
            win["closing"], win["active"] = False, True
            files.update({"saved_at": now_ms(), "save": False})
            load_history()                        # learned swing times (a saved value: no disk)
            del S.sounds[:], S.keys[:]
            S.last_swing, S.cycle_ms = None, None
            S.notice = None
            note["rd"] = Journal.reader()         # notices: only lines from now on
            note["clock"] = 0.0
            note["own"] = own_starts()
            fn = getattr(HOST, "alert_kind", None)    # listed on Settings > Alerts
            if fn is not None:
                safe(lambda: fn(ALERT_NOTICE, "Disarmed or dismounted", ALERT_NOTICE_SOUND))
            # (2.6.57) the satiety estimate of this character, read now that it is
            # in the world (the part's load ran before), counting down from now
            S.hunger = max(0.0, min(20.0, load_var("swingtimer_hunger", DEFAULT_HUNGER)))
            S.hunger_clock = now_ms()
            kite["on"] = bool(int(load_var(KITE_VAR, 1) or 0))    # (2.6.85) of this character
            kite["steps"].clear()                 # (your own step times: measured afresh)
            kite["xy"], kite["stat0"], kite["swing0"] = None, None, None
            build_window()
            # (2.6.57) no zone window: it rides on the target frame (below it in the
            # top half of the screen, above it in the bottom half); (2.6.67) inside its
            # zone, left of the bars, when the frame fills a zone with room; with Frames
            # off it is a free window
            pieces_add(LAYOUT_KEY, "target", 0, lambda: ctl.get("gump"))
            hook_sounds()
            register_hotkeys(True)
            loop.update({"slow_clock": 0.0, "sound_clock": 0.0, "eat_clock": 0.0,
                         "weapon": current_weapon(), "mob": None, "my_skill": 0.0,
                         "mob_skill": enemy_skill(None, None), "mob_name": "",
                         "skill_of": None, "skill_clock": 0.0, "timer_clock": 0.0,
                         "timer_mode": None, "fast": False})
            API.SysMsg("%s: on (%s picks the target, %s restarts the bar)."
                       % (TITLE, HK_SET_TARGET, HK_RESYNC), Kit.HUE_GOOD)


        def _stop():
            win["closing"], win["active"] = True, False
            register_hotkeys(False)
            note["rd"] = None
            if S.dirty:
                save_history()      # the last save (once, as the module stops)
            save_position()
            pieces_remove(LAYOUT_KEY)
            save_var("swingtimer_bg_opacity", bg_opacity)
            g = ctl.get("gump")
            ctl.clear()
            Kit.dispose(g)


        def _tick():
            if not is_open():
                loop["fast"] = False
                return
            t = now_ms()
            # read once a tick (in the game's frame: no waits); (2.6.82) the pass's
            # shared player (reads only: X, Y, the speed stat, war mode)
            p = HUD_ME() if HUD_ME is not None else API.Player

            # swing sounds and hotkeys since the last tick, in the order they came
            while S.sounds:
                handle_sound(S.sounds.pop(0), p)
            if S.keys:
                run_keys()

            if not SOUND_EVENTS_OK and t - loop["sound_clock"] >= SOUND_POLL_MS:
                loop["sound_clock"] = t
                poll_sounds(p)                # the log looks back a second; swings are deduped

            # the game lookups (weapon, target, skill, hunger): 4x per second is plenty
            if t - note["clock"] >= NOTICE_EVERY_MS:      # disarmed / dismounted lines
                note["clock"] = t
                check_notices()

            if t - loop["slow_clock"] >= SLOW_EVERY_MS:
                loop["slow_clock"] = t
                try:
                    loop["xy"] = (int(p.X), int(p.Y))   # your tile, for the sound poke
                except Exception:
                    loop["xy"] = None
                loop["weapon"] = current_weapon()
                was = S.gaps_weapon
                if match_weapon(loop["weapon"]):       # swapped: that weapon's own aim
                    S.cycle_ms = None
                    # 2.6.81: the shard gives bows and crossbows a full swing delay on
                    # equip: the swing clock starts at the swap (not on the first
                    # weapon read at start; the gap up to the swap isn't learned)
                    if was is not None and loop["weapon"][2] == AR:
                        S.last_swing = None
                        mark_swing(t)
                if S.dirty and t - files["saved_at"] >= SAVE_EVERY_MS:
                    files["save"] = True               # saved by thread_tick, off the game's frame
                mob = loop["mob"] = resolve_target()
                # the target's name and assumed skill: read here, with the target
                # itself, not on every tick (the hotkey override is applied per tick)
                nm = (getattr(mob, "Name", "") or "") if mob is not None else ""   # (2.6.82) once
                loop["mob_skill"] = enemy_skill(mob, None, nm)
                loop["mob_name"] = (nm or "target") if mob is not None else ""
                # your weapon skill: once a second, and at once when the weapon's skill changes
                if loop["weapon"][2] != loop.get("skill_of") or \
                        t - loop.get("skill_clock", 0.0) >= SKILL_EVERY_MS:
                    loop["skill_of"], loop["skill_clock"] = loop["weapon"][2], t
                    loop["my_skill"] = skill_value(loop["weapon"][2])
                decay_hunger()
                if t - loop["eat_clock"] >= EAT_EVERY_MS:
                    loop["eat_clock"] = t
                    check_eating()

            w_name, w_speed, w_skill, w_acc = loop["weapon"]
            stat = int(getattr(p, STAT_ATTR, 0))              # = speed_stat(p), every tick
            gaps = S.gaps
            avg = sum(gaps) / float(len(gaps)) if gaps else None   # = average_gap()
            predicted = avg or swing_delay_ms(stat, w_speed)   # learned aim, else formula
            mob = loop["mob"]

            # --- combat state: pause the clock when out of combat ---
            in_combat = bool(getattr(p, "InWarMode", False)) and mob is not None
            if not in_combat:
                if S.paused_at is None:
                    S.paused_at = t
                t_eff = S.paused_at                     # frozen time
            else:
                if S.paused_at is not None:
                    if S.last_swing is not None:        # skip the paused stretch
                        S.last_swing += t - S.paused_at
                    S.paused_at = None
                t_eff = t

            nt = S.notice
            if nt is not None and t >= nt[2]:
                S.notice = nt = None                    # its few seconds are over

            # --- swing bar ---
            if S.last_swing is None:
                progress, remaining, cycle = 1000, 0.0, predicted
            else:
                cycle = S.cycle_ms or predicted
                elapsed = t_eff - S.last_swing
                remaining = cycle - elapsed
                progress = 1000 if elapsed >= cycle else int(elapsed / cycle * 1000)

            set_fill(progress, "paused" if not in_combat else      # progress tops out at 1000
                     ("ready" if progress >= 1000 else "fill"))
            step_note(p, t)                             # (2.6.85) your own ms a tile
            kite_draw(p, mob, cycle, stat, w_speed)     # (2.6.85) the turn-back point
            # (2.6.82) the fast cadence only while the bar moves (see _interval)
            loop["fast"] = in_combat and progress < 1000
            if nt is not win["notice_shown"]:           # a notice over the bar: shown / hidden
                win["notice_shown"] = nt
                nl = ctl.get("notice")
                if nl is not None:
                    if nt is not None:
                        set_label(nl, nt[0], nt[1])
                    try:
                        nl.IsVisible = nt is not None
                    except Exception:
                        pass

            # --- the seconds beside the bar ---
            # it changes every tick while the bar fills, so it is written
            # COUNTDOWN_EVERY_MS apart (and at once when its state turns)
            mode = (in_combat, progress >= 1000, mob is None)   # (2.6.72) Ready / Paused
            if mode != loop["timer_mode"] or t - loop["timer_clock"] >= COUNTDOWN_EVERY_MS:
                loop["timer_mode"], loop["timer_clock"] = mode, t
                if not in_combat:
                    # (2.6.72) no one to swing at: Ready, grey; Paused only for a target in war
                    # mode that is out of reach
                    set_label(ctl["swing"], "Paused" if mob is not None else "Ready", HUE_GREY)
                elif progress >= 1000:
                    set_label(ctl["swing"], "Ready", HUE_GREEN)
                else:
                    set_label(ctl["swing"], "%.1fs" % (max(0.0, remaining) / 1000.0), HUE_TEXT)
            # (2.6.82) keyed on the delay as the tip shows it (0.1 s), not every ms
            key = (w_name, w_speed, "%.1f" % (predicted / 1000.0), len(gaps))
            if win["shown"].get("bar_tip") != key:
                win["shown"]["bar_tip"] = key
                set_tip("tip_bar", bar_tip((w_name, w_speed, predicted, len(gaps))))

            # --- the row under the bar: hit chance left, satiety right ---
            shown = win["shown"]
            my_skill = loop["my_skill"]
            if S.enemy_override is not None:
                their_skill, src = S.enemy_override, "set"
            else:
                their_skill, src = loop["mob_skill"]
            key = (mob is not None, loop["mob_name"], their_skill, my_skill, w_skill,
                   w_acc, S.hunger)
            if shown.get("rows") != key:
                shown["rows"] = key
                chance = final_hit_chance(my_skill, their_skill, w_acc, S.hunger)
                sat_mod, sat_label = satiety_info(S.hunger)
                if mob is not None:
                    set_label(ctl["hit"], "Hit %d%%" % int(round(chance * 100)),
                              hue_for_chance(chance))
                    set_tip("tip_hit", hit_tip((loop["mob_name"], w_skill, my_skill,
                                                their_skill, w_acc, sat_mod)))
                else:
                    set_label(ctl["hit"], "Hit --%", HUE_GREY)
                    set_tip("tip_hit", hit_tip(None))
                n = max(0, min(20, int(round(S.hunger))))
                if set_label(ctl["food"], "Food %d/20" % n, hue_for_food(S.hunger)):
                    Kit.ui_pos(ctl["food"], win["x1"] + win["row1"] - win["food_w"][n], ROW2_Y)
                set_tip("tip_food", food_tip(sat_label, sat_mod))


        def _thread_tick():
            """On the script's own thread, after a tick: the save of the learned
            swings, and the one-time read of an older version's data file (a disk
            read inside the game's frame would be a hitch)."""
            if files["import"] and not win["closing"]:
                import_old_file()
                if not files["import"]:
                    loop["slow_clock"] = 0.0       # match the weapon to its list now
            if files["save"] and S.dirty:
                save_history()
            files["save"] = False


        def _interval():
            """(2.6.82) 40 a second only while the bar fills in combat (its fill must
            stay smooth); 10 a second otherwise (Ready, Paused or no target: nothing
            moves). A swing sound or a hotkey pokes the pass, so a swing still starts
            the bar at once; mark_swing times it from the sound or the key press."""
            return FAST_TICK if loop.get("fast") else SLOW_TICK


        def _thread_wanted():
            return bool(files["save"] or files["import"])


        # client_tick: the tick runs inside the game's frame, batched with the other
        # modules (every read there costs no wait); it never waits itself.
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True, "thread_tick": _thread_tick,
                  "thread_wanted": _thread_wanted, "interval": _interval,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        return MODULE

    def _part_bandage():
        """Builds the part in its own namespace and returns its hooks."""
        # =============================================================================
        #  PART: Bandages  (Character HUD; from Bandage Agent, redone in 2.6.5)
        #
        #  One press = one bandage. Nothing here bandages by itself: the shard's
        #  rules forbid automating any part of combat, healing included, so the
        #  2.6.06 agent (a bandage whenever your HP fell under a threshold, an
        #  automatic cure, bandages on party members and pets by itself) is gone.
        #  What stays, and what is new:
        #  - The bar: fills while a bandage of yours works (the shard's bandage
        #    time and a latency buffer, both on the settings page), says who it is
        #    on, and shows the bandages left in your backpack ("x87").
        #  - (2.6.56) Two rows: the bar with the time left beside it, then four
        #    controls drawn from the client's own art: the bandage (one bandage
        #    on yourself), "x87" (bandages left), the target icon (a target
        #    cursor, then one bandage on whoever you click) and the repeat arrow (one
        #    more bandage on the last one).
        #    Each press is one bandage; the cursor the bandage raises is aimed for
        #    you, and only that one (cursors other modules raise are left alone).
        #  - Separate times for a bandage on yourself and on someone else (on this
        #    shard a bandage on someone else is much faster).
        #  - Alerts (Settings > Alerts: sound, on / off): your HP under the % set
        #    here (once per drop; the old "start at HP %" setting), you are
        #    poisoned (once per poisoning, when your Healing and Anatomy could cure
        #    it with a bandage), bandages running low, and a "ready" cue when the
        #    bandage you started is done. They prompt you; they never act.
        #  - (2.6.56) No smaller form and no fold into the Action Bar: turning the
        #    part off on the Modules tab hides it.
        #  Saved keys are the 2.6.06 ones: BandageAgentStartPct (now the HP alert
        #  %), BandageAgent_timing, BandageAgent_pos, BandageAgent_extra (cure =
        #  the poison alert, low, others = the name shown on the bar; the rest of
        #  the string is kept as it was so an older version still reads it) and,
        #  new, BandageAgent_other (the time of a bandage on someone else).
        # =============================================================================

        # ---------------- CONFIG ----------------
        BANDAGE_GRAPHIC = 0x0E21    # Standard bandage
        BANDAGE_TIME    = 15.0      # seconds a bandage on yourself takes: the default of the field
        OTHER_TIME_DEF  = 7.5       # seconds a bandage on someone else takes (In Mani Ylem: much
        #                             faster than on yourself; set on the page)
        TIME_BUFFER     = 0.5       # latency padding (seconds): the default of the field
        TIME_MIN, TIME_MAX = 1.0, 60.0      # what the time fields accept
        BUFFER_MIN, BUFFER_MAX = 0.0, 5.0   # what the "buffer" field accepts
        FIELD_SETTLE    = 0.7       # seconds a typed time stands unchanged before it is applied
        TARGET_TIMEOUT  = 3.0       # seconds to wait for the bandage's target cursor
        PICK_TIMEOUT    = 15.0      # seconds the target icon's cursor waits for your click
        OTHER_RANGE     = 1         # tiles: how near they must be (RunUO's bandage range: 1
        #                             pre-AoS; unchecked in game)
        WATCH_EVERY     = 0.1       # tick while idle
        CURSOR_EVERY    = 0.03      # tick while the bandage's cursor is waited for
        HEAL_EVERY      = 0.1       # tick while a bandage runs (only the bar moves)
        # 2.6.81: the server's answers to a bandage (RunUO texts, lower case, matched
        # at the start of a journal line; UNCHECKED IN GAME). Refused: no bandage
        # runs, so the bar stops at once (no "done" cue); finished: the bar ends early
        BAND_REFUSED    = ("that being is not damaged", "you are too far away to do that",
                           "bandages can not be used on that", "you cannot heal that",
                           "bandages cannot be used on that", "that is too far away",
                           "that creature may only be healed",
                           "you did not stay close enough to heal",
                           "you were unable to finish your work")
        BAND_REFUSED_END = ("you did not stay close enough to heal",   # these come at the end
                            "you were unable to finish your work")
        REFUSE_SECS     = 2.0       # the other refusals come at once: only this soon after the aim
        #                             (the far-away text is the shard's for any far use, too)
        BAND_FINISHED   = ("you finish applying the bandages",
                           "you apply the bandages, but they barely help",
                           "you apply the bandages, but they do not seem",
                           "you heal what little damage",
                           "you are able to resurrect", "you are unable to resurrect",
                           "you have cured the target of all poisons")
        # 2.6.85: a bandage is seen starting from the shard itself, whatever started
        # it (Cliloc 500956-500960; UNCHECKED IN GAME), or from a buff icon if the
        # shard sends one for it (a name a buff's title contains)
        BAND_BEGUN      = "you begin applying the bandages"
        BAND_BUFF       = "Healing"
        PATIENT_SECS    = 4.0       # a last target this new is who a bandage we didn't aim is on

        DEFAULT_START_PCT = 50      # the HP alert: under this % (the 2.6.06 "start at" key)
        PCT_MIN, PCT_MAX  = 0, 99   # 0 = no HP alert

        BAR_WIN_X, BAR_WIN_Y = 400, 300   # the bar's position (first run)

        # the poison alert needs the skills to cure with a bandage (RunUO pre-AoS
        # needs 60 / 60; unchecked in game)
        CURE_HEALING    = 60.0
        CURE_ANATOMY    = 60.0
        SKILL_EVERY     = 5.0       # seconds between reads of those two skills (only while poisoned)

        COUNT_EVERY     = 2.0       # bandages left: counted in the backpack this often
        COUNT_AFTER_USE = 0.6       # ...and this soon after a bandage was used
        DEFAULT_LOW     = 10        # alert when fewer than this are left (0 = never)
        LOW_MIN, LOW_MAX = 0, 999
        ALERT_LOW       = "bandage.low"       # alert kinds (Settings > Alerts)
        ALERT_LOW_SOUND = 0x1EA               # chime
        ALERT_HP        = "bandage.hp"        # your HP under the %
        ALERT_HP_SOUND  = 0x1F1               # harm
        ALERT_POISON    = "bandage.poison"    # you are poisoned and a bandage could cure it
        ALERT_POISON_SOUND = 0x1E0            # cure
        ALERT_READY     = "bandage.ready"     # the bandage you started is done
        ALERT_READY_SOUND = 0x202             # heal tone
        OTHER_NAME_CHARS = 10       # longest name shown on the bar

        KEY             = "bandage"   # the 2.6.06 module key: the part's own key
        TITLE           = "Bandages"
        PERSIST_KEY     = "BandageAgentStartPct"
        TIMING_KEY      = "BandageAgent_timing"   # "<bandage time>|<buffer>"
        POS_KEY         = "BandageAgent_pos"
        EXTRA_KEY       = "BandageAgent_extra"    # "cure=0;low=10;others=0;opct=80;party=1;pets=1"
        OTHER_KEY       = "BandageAgent_other"    # "<seconds>": a bandage on someone else (2.6.5)
        TRAY_ICON       = 0x0E21    # the bandage's item art: the "bandage yourself" control
        # (2.6.57) the target reticle is drawn from the client's ring (gump 8012, a
        # 16 px circle) hued gold, with four short gold ticks across it and a dot in
        # the middle: the client has no reticle gump of its own (checked in
        # Gumpart.mul); (2.6.59) the repeat arrow is the same ring with a gap and
        # an arrowhead (no bare circular-arrow gump in the client either)
        TARGET_ICON     = 8012      # gump art: the reticle's ring
        TARGET_HUE      = 53        # ...hued gold
        TICK_COLOR      = "#E8C25A" # the reticle's ticks and dot
        REDO_RING       = 8012      # gump art: the repeat arrow's ring (hued gold, an arrowhead drawn on it)
        # ----------------------------------------

        # (2.6.56) two rows in the stone frame and black section: the bar with the
        # time left, then the four controls, both centred; no other slack
        WIN_H = 62
        ROW1_Y, ROW2_Y = 16, 35     # the bar's top, the controls' top (window pixels)
        ICON = 18                   # the three art controls are this square
        ICON_GAP = 8                # between the controls of row 2
        PAD = 3                     # black each side of the wider row
        NAME_W = 90                 # more room with "Who it is on" ticked ("Fluffy 13.9s")
        CFG_H1, CFG_H2, CFG_H3 = 120, 118, 104    # the settings page's three sections
        CFG_H = CFG_H1 + Kit.GAP + CFG_H2 + Kit.GAP + CFG_H3

        st = {
            "start_pct": DEFAULT_START_PCT,
            "band_time": BANDAGE_TIME,    # seconds a bandage on you takes
            "other_time": OTHER_TIME_DEF, # ...and on someone else
            "buffer": TIME_BUFFER,        # seconds added for latency
            "phase": "idle",          # idle / cursor / heal
            "t0": 0.0,                # bandage started
            "deadline": 0.0,          # give up waiting for the cursor
            "shutting": False,
            "queue": [],              # clicks for the next tick
            "rebuild": False,         # the bar's width changes ("Who it is on" toggled)
            "skills": (0.0, 0.0, -1e9),   # (Healing, Anatomy, when read)
            "count": None,            # bandages in the backpack (None: not counted yet)
            "count_at": 0.0,          # next count
            "low_armed": True,        # the "bandages low" alert may be raised
            "hp_armed": True,         # the HP alert may be raised (armed again above the %)
            "poison_armed": True,     # the poison alert may be raised (armed again when cured)
            "target": None,           # the bandage in hand: {"serial", "name", "short"} or None (you)
            "last": None,             # the last someone-else bandaged (the repeat arrow, Alt+click)
            "pick": False,            # a target icon cursor is up
            "rd": None,               # (2.6.81) journal reader: the server's answer to a bandage
            "begun": False,           # (2.6.85) the shard said this bandage began
            "by_buff": False,         # (2.6.85) ...or only its buff icon did
            "buff": False,            # (2.6.85) the bandage buff icon was up on the last tick
            "lt": (0, 0.0),           # (2.6.85) the client's last target, and when it changed
        }
        # saved in EXTRA_KEY (2.6.05 names kept)
        settings = {"cure": True, "low": DEFAULT_LOW, "others": False,   # (2.6.59) off: the 161 px panel
                    "other_pct": 80, "party": True, "pets": True}
        win = {"g": None, "c": {}, "store": ({}, {}), "fill": None, "fill_box": None, "label": None,
               "bar_w": 109, "fill_w": -1, "text": None, "count": None, "count_text": None,
               "wide": False, "size": None}
        cfg = {"box": None, "time": None, "other": None, "buffer": None, "typed": None, "since": 0.0}


        # ---------- persistence ----------
        def load_pct():
            try:
                v = int(Kit.get_var(PERSIST_KEY, str(DEFAULT_START_PCT)))
                st["start_pct"] = max(PCT_MIN, min(PCT_MAX, v))
            except Exception:
                st["start_pct"] = DEFAULT_START_PCT


        def save_pct():
            Kit.put_var(PERSIST_KEY, str(st["start_pct"]))


        def load_timing():
            p = Kit.get_var(TIMING_KEY, "").split("|")
            try:
                if len(p) >= 1 and p[0]:
                    st["band_time"] = max(TIME_MIN, min(TIME_MAX, float(p[0])))
                if len(p) >= 2 and p[1]:
                    st["buffer"] = max(BUFFER_MIN, min(BUFFER_MAX, float(p[1])))
            except ValueError:
                st["band_time"], st["buffer"] = BANDAGE_TIME, TIME_BUFFER
            try:
                v = Kit.get_var(OTHER_KEY, "")
                if v:
                    st["other_time"] = max(TIME_MIN, min(TIME_MAX, float(v)))
            except ValueError:
                st["other_time"] = OTHER_TIME_DEF


        def save_timing():
            Kit.put_var(TIMING_KEY, "%.2f|%.2f" % (st["band_time"], st["buffer"]))
            Kit.put_var(OTHER_KEY, "%.2f" % st["other_time"])


        def load_extra():
            v = {}
            for part in Kit.get_var(EXTRA_KEY, "").split(";"):
                if "=" in part:
                    k, val = part.split("=", 1)
                    v[k.strip()] = val.strip()
            settings["cure"] = v.get("cure", "1") != "0"
            settings["others"] = v.get("others", "0") == "1"   # (2.6.59) off unless ticked
            settings["party"] = v.get("party") != "0"
            settings["pets"] = v.get("pets") != "0"
            settings["low"] = _int_in(v.get("low"), LOW_MIN, LOW_MAX, DEFAULT_LOW)
            settings["other_pct"] = _int_in(v.get("opct"), 1, 99, 80)


        def _int_in(text, lo, hi, default):
            try:
                return max(lo, min(hi, int(text)))
            except (TypeError, ValueError):
                return default


        def save_extra():
            Kit.put_var(EXTRA_KEY, "cure=%d;low=%d;others=%d;opct=%d;party=%d;pets=%d" % (
                int(settings["cure"]), settings["low"], int(settings["others"]),
                settings["other_pct"], int(settings["party"]), int(settings["pets"])))


        def save_pos():
            if not pieces_on(KEY):               # (2.6.57) riding on the frame: not its own place
                Kit.save_pos(POS_KEY, win["g"])


        # ---------- window ----------
        queue = Kit.queuer(st)


        def layout_size():
            """(2.6.56) The panel's own size and its rows: row 1 is the bar, 5 px and
            the readout (sized for its widest text, and a name with "Who it is on"
            ticked); row 2 the bandage, "x999", the target icon and the repeat arrow, ICON_GAP
            apart. The wider row and PAD each side make the black section; the
            stone frame is 8 px round it."""
            bw = Kit.pic_size(Kit.LINE_RED)[0]
            fw = Kit.pic_size(Kit.LINE_BLUE)[0]
            bar_w = bw if bw > 0 and fw > 0 else 109
            # (2.6.58) the readout's room is the width of "15.0s" (the design), plus the
            # name's room with "Who it is on" ticked
            text_w = max(Kit.text_w("15.0s"), readout_room()) + (NAME_W if settings["others"] else 0)
            count_w = Kit.text_w("x999")
            row1 = bar_w + 5 + text_w
            row2 = ICON + ICON_GAP + count_w + ICON_GAP + ICON + ICON_GAP + ICON
            sec_w = max(row1, row2) + 2 * PAD
            return {"bar_w": bar_w, "text_w": text_w, "count_w": count_w, "row1": row1,
                    "row2": row2, "sec_w": sec_w, "W": sec_w + 16, "H": WIN_H}


        def build_window():
            L = layout_size()
            WIN_W = L["W"]
            bw = Kit.pic_size(Kit.LINE_RED)[0]
            fw, fh = Kit.pic_size(Kit.LINE_BLUE)
            wide = settings["others"]                    # room for who the bandage is on
            x, y = Kit.load_pos(POS_KEY, (BAR_WIN_X, BAR_WIN_Y), (WIN_W, WIN_H))
            old = win["g"]
            if Kit.is_open(old):                         # a rebuild: where it stands now
                x, y = old.GetX(), old.GetY()
            store = ({}, {})
            c = {}
            g = G.CreateGump(True, True)
            Kit.place(g, x, y, WIN_W, WIN_H)             # wholly on screen
            Kit.add_window_frame(g, WIN_W, WIN_H, corners=False)
            PIECES["bg"][g] = [Kit.add_section(g, 8, 8, L["sec_w"], WIN_H - 16)]   # (2.6.72)
            safe(lambda: g.SetTooltip("%s: one press = one bandage (x = bandages left in your "
                                      "backpack)" % TITLE))

            # row 1: the client's own status bar (blue line growing over the red one)
            # and the time left beside it
            x1 = 8 + (L["sec_w"] - L["row1"]) // 2
            win["fill"] = win["fill_box"] = None
            win["bar_w"] = L["bar_w"]
            if bw > 0 and fw > 0:
                Kit.add_pic(g, Kit.LINE_RED, x1, ROW1_Y)
                win["fill"] = Kit.add_tiled(g, Kit.LINE_BLUE, x1, ROW1_Y, 1, fh)
                safe(lambda: win["fill"].SetWidth(0))
            else:
                Kit.add_tiled(g, Kit.SECTION_TILE, x1, ROW1_Y, 109, 9, 1.0)
                box = G.CreateGumpColorBox(1.0, "#3A63A8")
                box.SetRect(x1 + 1, ROW1_Y + 1, 1, 7)
                g.Add(box)
                win["fill_box"] = box
            tx = x1 + L["bar_w"] + 5
            win["label"] = Kit.add_label(g, "Ready", tx, ROW1_Y - 2, Kit.HUE_INFO)
            Kit.catcher(g, x1 - 2, ROW1_Y - 4, L["row1"] + 4, 18, _bar_click,
                        "The bandage in progress and who it is on. "
                        "Alt+click: auto-follow (again to stop)", movable=True)
            # row 2: the bandage, the count, the target icon, the repeat arrow; bare art
            # with an invisible click area the size of the art over each
            x2 = 8 + (L["sec_w"] - L["row2"]) // 2
            y2 = ROW2_Y
            try:
                pic = G.CreateGumpItemPic(TRAY_ICON, ICON, ICON)
                pic.SetPos(x2, y2)
                safe(lambda: pic.SetAcceptMouseInput(False))
                g.Add(pic)
            except Exception:
                Kit.add_label(g, "B", x2 + 5, y2 + 1, Kit.HUE_TEXT)
            Kit.catcher(g, x2, y2, ICON, ICON, queue("me"), "Use one bandage on yourself")
            xc = x2 + ICON + ICON_GAP
            win["count"] = Kit.add_label(g, "", xc, y2 + 1, Kit.HUE_INFO)
            Kit.catcher(g, xc, y2, L["count_w"], ICON, lambda *a: None,
                        "Bandages left in your backpack", movable=True)
            xt = xc + L["count_w"] + ICON_GAP
            _reticle(g, xt, y2)
            Kit.catcher(g, xt, y2, ICON, ICON, _other_click,
                        "Target someone within %d tile%s for one bandage. "
                        "Alt+click: auto-follow (again to stop)"
                        % (OTHER_RANGE, "" if OTHER_RANGE == 1 else "s"))
            xr = xt + ICON + ICON_GAP
            _repeat(g, xr, y2)
            c["again"] = Kit.catcher(g, xr, y2, ICON, ICON, _again_click,
                                     "Use one more bandage on the one you last bandaged. "
                                     "Alt+click: auto-follow (again to stop)")
            win["fill_w"] = -1
            win["text"] = None
            win["count_text"] = None
            win["wide"] = wide
            win["size"] = (WIN_W, WIN_H)
            win.update({"g": g, "c": c, "store": store})
            G.AddControlOnDisposed(g, _closed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))   # saved the moment you let go of it
            if old is not None:
                Kit.dispose(old)                      # its close is ignored: win["g"] moved on
            show_count()


        def _repeat(g, x, y):
            """(2.6.59) The circular repeat arrow, ICON px square: the client's ring
            hued gold with a gap at its top right and an arrowhead there (the
            client has no bare circular-arrow gump: gump 236 is a whole stone
            button, with its own frame, which the design rules out). No mouse on
            any of it: the catcher over it takes the clicks."""
            p = Kit.add_pic(g, REDO_RING, x, y, hue=TARGET_HUE, mouse=False)
            if p is None:
                Kit.add_label(g, "@", x + 5, y + 1, Kit.HUE_TEXT)
                return
            safe(lambda: p.SetWidth(ICON))
            safe(lambda: p.SetHeight(ICON))
            Kit.add_box(g, x + 8, y, 10, 7, 1.0, "#101010")          # the gap in the ring
            for r in range(7):                                       # the head: a triangle
                Kit.add_box(g, x + 9, y + r, (3 - abs(r - 3)) * 2 + 1, 1, 1.0, TICK_COLOR)

        def _reticle(g, x, y):
            """(2.6.57) The target reticle, ICON px square: the client's ring hued
            gold, four ticks crossing it and a dot in the middle (no mouse on any
            of it: the catcher over it takes the clicks)."""
            p = Kit.add_pic(g, TARGET_ICON, x, y, hue=TARGET_HUE, mouse=False)
            if p is None:
                Kit.add_label(g, "+", x + 5, y + 1, Kit.HUE_TEXT)
                return
            safe(lambda: p.SetWidth(ICON))
            safe(lambda: p.SetHeight(ICON))
            c = ICON // 2
            for bx, by, bw, bh in ((c - 1, 0, 2, 5), (c - 1, ICON - 5, 2, 5),      # top, bottom
                                   (0, c - 1, 5, 2), (ICON - 5, c - 1, 5, 2),      # left, right
                                   (c - 1, c - 1, 2, 2)):                          # the dot
                Kit.add_box(g, x + bx, y + by, bw, bh, 1.0, TICK_COLOR)

        def _other_click(*args):
            """The target icon: a target cursor for one bandage; Alt+click follows
            the last one bandaged."""
            try:
                alt = Follow.alt_held()
            except Exception:
                alt = False
            if alt:
                o = st["last"]
                if o is not None and ("follow", o["serial"]) not in st["queue"]:
                    st["queue"].append(("follow", o["serial"]))
                return
            if "other" not in st["queue"]:
                st["queue"].append("other")


        def _bar_click(*args):
            """Alt+click on the bar or its readout: follow who the bandage is (or was
            last) on."""
            try:
                alt = Follow.alt_held()
            except Exception:
                alt = False
            if alt:
                o = st["target"] or st["last"]
                if o is not None and ("follow", o["serial"]) not in st["queue"]:
                    st["queue"].append(("follow", o["serial"]))


        def _again_click(*args):
            try:
                alt = Follow.alt_held()
            except Exception:
                alt = False
            o = st["last"]
            if alt:
                if o is not None and ("follow", o["serial"]) not in st["queue"]:
                    st["queue"].append(("follow", o["serial"]))
                return
            if "again" not in st["queue"]:
                st["queue"].append("again")


        def _closed(g):
            def handler(*args):
                if win["g"] is g and not st["shutting"]:
                    save_pos()
                    win["g"] = None
                    HOST.disable(KEY)
            return handler


        def show_count():
            """The bandages-left label: written only when the number or its hue changes."""
            lbl = win["count"]
            n = st["count"]
            if lbl is None:
                return
            if n is None:
                key = ("", Kit.HUE_INFO)
            else:
                low = settings["low"]
                key = ("x%d" % n, Kit.HUE_BAD if low > 0 and n < low else Kit.HUE_INFO)
            if key != win["count_text"]:
                win["count_text"] = key
                Kit.set_text(lbl, key[0], key[1])


        def set_bar(fraction, text, hue=None):
            fraction = max(0.0, min(1.0, fraction))
            w = int(win["bar_w"] * fraction)
            old_w = win["fill_w"]
            if w != old_w:
                win["fill_w"] = w
                # (2.6.82) every tick of a bandage: no lambdas, and the fill's
                # visibility is written only when it turns on or off
                fill = win["fill"]
                if fill is not None:
                    try:
                        Kit.ui_w(fill, w)
                    except Exception:
                        pass
                    if (w > 0) != (old_w > 0) or old_w < 0:
                        try:
                            fill.IsVisible = w > 0
                        except Exception:
                            pass
                elif win["fill_box"] is not None:
                    try:
                        Kit.ui_w(win["fill_box"], max(1, w - 2))
                    except Exception:
                        pass
            lbl = win["label"]
            if lbl is not None and (text, hue) != win["text"]:
                win["text"] = (text, hue)
                Kit.set_text(lbl, text, Kit.HUE_INFO if hue is None else hue)


        # ---------- alerts: they prompt, they never act ----------
        def alert(kind, text, level="warn"):
            fn = getattr(HOST, "alert", None)
            if fn is None:                           # an older mother: a journal line instead
                low = text[:1].lower() + text[1:]
                API.SysMsg("%s: %s%s" % (TITLE, low, "" if low[-1:] in "?!." else "."),
                           Kit.HUE_INFO)
                return
            try:
                fn(kind, text, level)
            except Exception:
                pass


        def can_cure():
            """Healing and Anatomy both at CURE_* or more (read every SKILL_EVERY s,
            only while you are poisoned)."""
            heal, anat, at = st["skills"]
            now = time.time()
            if now - at >= SKILL_EVERY:
                heal, anat = skill_value("Healing"), skill_value("Anatomy")
                st["skills"] = (heal, anat, now)
            return heal >= CURE_HEALING and anat >= CURE_ANATOMY


        def skill_value(name):
            try:
                sk = API.GetSkill(name)
                return float(sk.Value) if sk is not None else 0.0
            except Exception:
                return 0.0


        def watch_alerts(p, hits, hmax):
            """The HP and poison alerts, once per drop / poisoning."""
            pct = st["start_pct"]
            if pct > 0 and hmax > 0:
                if hits * 100.0 / hmax <= pct:
                    if st["hp_armed"]:
                        st["hp_armed"] = False
                        alert(ALERT_HP, "Your HP is at %d%%: bandage?" % int(hits * 100.0 / hmax))
                else:
                    st["hp_armed"] = True
            if settings["cure"]:
                try:
                    poisoned = bool(p.IsPoisoned)
                except Exception:
                    poisoned = False
                if poisoned:
                    if st["poison_armed"] and can_cure():
                        st["poison_armed"] = False
                        alert(ALERT_POISON, "You are poisoned: a bandage can cure it")
                else:
                    st["poison_armed"] = True


        # ---------- bandages left ----------
        def count_bandages():
            try:
                items = API.FindTypeAll(BANDAGE_GRAPHIC, API.Backpack)
            except Exception:
                return st["count"]
            n = 0
            for it in items or ():
                try:
                    n += int(it.Amount or 1)
                except Exception:
                    n += 1
            return n


        def count_tick(now):
            """Every COUNT_EVERY s: the count on the bar, and the one "bandages low"
            alert when it drops under the threshold (armed again at the threshold)."""
            if now < st["count_at"]:
                return
            st["count_at"] = now + COUNT_EVERY
            n = count_bandages()
            if n is None:
                return
            prev, st["count"] = st["count"], n
            low = settings["low"]
            if low > 0 and n < low:
                if st["low_armed"] and (n > 0 or (prev or 0) > 0):
                    st["low_armed"] = False
                    alert(ALERT_LOW, low_text(n))
            else:
                st["low_armed"] = True
            show_count()


        def low_text(n):
            if n <= 0:
                return "No bandages left"
            return "Only %d bandage%s left" % (n, "" if n == 1 else "s")


        # ---------- one bandage, on a press ----------
        def near(m, px, py, reach):
            try:
                return max(abs(int(m.X) - px), abs(int(m.Y) - py)) <= reach
            except Exception:
                return False


        def describe(m):
            try:
                name = str(m.Name or "") or "them"
                serial = int(m.Serial)
            except Exception:
                return None
            short = name if len(name) <= OTHER_NAME_CHARS else name[:OTHER_NAME_CHARS - 1] + "."
            return {"serial": serial, "name": name, "short": short}


        def start_bandage(p, now, target):
            """Use one bandage; its cursor is aimed at `target` (None: you) on the
            next ticks. One press got us here."""
            if st["phase"] != "idle":
                API.SysMsg("%s: a bandage is already running." % TITLE, Kit.HUE_INFO)
                return
            if API.HasTarget("any") or HOST.cursor_busy(KEY):
                API.SysMsg("%s: a target cursor is up (finish it or press Esc first)." % TITLE,
                           Kit.HUE_INFO)
                return
            try:
                if p.IsDead:
                    return
            except Exception:
                pass
            bandage = API.FindType(BANDAGE_GRAPHIC, API.Backpack)
            if not bandage:
                set_bar(0.0, "Out!", Kit.HUE_BAD)
                API.SysMsg("%s: out of bandages!" % TITLE, Kit.HUE_BAD)
                return
            if st.get("rd") is not None:                 # 2.6.81: lines from before the
                try:                                     # press are not its answer
                    st["rd"].new()
                except Exception:
                    pass
            API.UseObject(bandage.Serial)
            st["count_at"] = min(st["count_at"], now + COUNT_AFTER_USE)
            HOST.claim_cursor(KEY, TARGET_TIMEOUT)      # the cursor that comes is ours
            st["target"] = target
            st["begun"], st["by_buff"] = False, False
            st["phase"], st["deadline"] = "cursor", now + TARGET_TIMEOUT


        def picked(serial):
            """The target icon's cursor came down (0: cancelled)."""
            st["pick"] = False
            if serial:
                queue(("on", int(serial)))()


        def bandage_other(p, now, serial):
            try:
                m = API.FindMobile(serial)
            except Exception:
                m = None
            if m is None:
                API.SysMsg("%s: can't see them." % TITLE, Kit.HUE_BAD)
                return
            try:
                me = int(p.Serial) == int(m.Serial)
            except Exception:
                me = False
            if me:
                start_bandage(p, now, None)
                return
            try:
                if m.IsDead:
                    API.SysMsg("%s: they are dead." % TITLE, Kit.HUE_BAD)
                    return
                px, py = int(p.X), int(p.Y)
            except Exception:
                return
            if not near(m, px, py, OTHER_RANGE):
                API.SysMsg("%s: too far away (they must be within %d tile%s)." %
                           (TITLE, OTHER_RANGE, "" if OTHER_RANGE == 1 else "s"), Kit.HUE_BAD)
                return
            d = describe(m)
            if d is None:
                return
            start_bandage(p, now, d)


        def _tick():
            # Runs on the client thread (client_tick): every read below is in place,
            # with no wait. It never waits: the cursor is looked for on the next ticks.
            p = API.Player
            if p is None:
                return
            now = time.time()
            if st["queue"] or st["rebuild"]:
                _queued(p, now)
                if win["g"] is None:
                    return
            if p.IsDead:
                if st["phase"] != "idle":
                    HOST.release_cursor(KEY)
                st["phase"], st["target"] = "idle", None
                set_bar(0.0, "Dead", Kit.HUE_BAD)
                return
            count_tick(now)
            hits, hmax = p.Hits, p.HitsMax
            if hmax > 0:
                watch_alerts(p, hits, hmax)
            watch_last_target(now)
            # 2.6.81: the server's answer to the bandage (read every tick, so lines
            # from before a press are never taken for its answer)
            answer = band_answer(p, now) if st["rd"] is not None else None
            buff_answer = watch_buff(p, now)
            if answer is None:
                answer = buff_answer
            if answer is not None and answer != "done" and st["phase"] != "idle":
                if st["phase"] == "cursor":
                    HOST.release_cursor(KEY)
                st["phase"], st["target"] = "idle", None
                set_bar(0.0, "Ready")
                API.SysMsg("%s: the bandage failed (%s)." % (TITLE, answer), Kit.HUE_BAD)
                return

            if st["phase"] == "heal":
                o = st["target"]
                band_time = st["other_time"] if o is not None else st["band_time"]
                elapsed = now - st["t0"]
                if elapsed >= band_time + st["buffer"] or answer == "done":
                    st["phase"], st["target"] = "idle", None
                    set_bar(1.0, "Done", Kit.HUE_GOOD)
                    alert(ALERT_READY, "Bandage done: ready for the next", "info")
                else:
                    left = "%.1fs" % max(0.0, band_time - elapsed)
                    if o is not None and win["wide"]:        # room for the name
                        left = "%s %s" % (o["short"], left)
                    set_bar(elapsed / band_time, left, Kit.HUE_TEXT)
                return

            if st["phase"] == "cursor":
                # 2.6.81: only a beneficial cursor (the bandage's kind) is aimed, and
                # only while nobody else has the cursor spoken for (a pick_target
                # cursor included); a cursor of another kind is the player's own:
                # never aimed, never cancelled
                if HOST.cursor_ok(KEY, "beneficial"):
                    o = st["target"]
                    if o is None:
                        API.TargetSelf()
                        aimed = True
                    else:
                        aimed = aim_other(p, o)
                    HOST.release_cursor(KEY)
                    if aimed:
                        st["phase"], st["t0"] = "heal", now
                    else:
                        st["phase"], st["target"] = "idle", None
                elif now > st["deadline"]:
                    try:
                        up = bool(API.HasTarget("beneficial"))   # only for the message
                    except Exception:
                        up = False
                    if up:
                        API.SysMsg("%s: a bandage cursor is up: press Esc or aim it." % TITLE,
                                   Kit.HUE_INFO)
                    else:
                        API.SysMsg("%s: no bandage cursor appeared." % TITLE, Kit.HUE_BAD)
                    HOST.release_cursor(KEY)
                    st["phase"], st["target"] = "idle", None
                return
            t = win["text"]
            # 2.6.81: "Out!" goes back to "Ready" once bandages are counted again
            if t is None or t[0] not in ("Ready", "Done", "Out!") or \
                    (t[0] == "Out!" and (st["count"] or 0) > 0):
                set_bar(0.0, "Ready")


        def watch_last_target(now):
            """2.6.85: when the client's last target changed: a bandage this part
            didn't aim is on them if it came just after (a click on yourself never
            changes it: see TargetManager.Target)."""
            try:
                serial = int(API.LastTargetSerial)
            except Exception:
                return
            if serial != st["lt"][0]:
                st["lt"] = (serial, now)


        def guess_patient(p, now):
            """2.6.85: who a bandage this part didn't aim is on: None (you) or
            describe()'s dict. The shard doesn't say, so: a last target that has just
            changed and stands in reach; else you, unless you are unhurt (a bandage
            can't start then) and your last target stands in reach."""
            serial, when = st["lt"]
            if not serial:
                return None
            try:
                if serial == int(p.Serial):
                    return None
                m = API.FindMobile(serial)
                if m is None or not near(m, int(p.X), int(p.Y), OTHER_RANGE + 1):
                    return None
                if now - when <= PATIENT_SECS or (p.Hits >= p.HitsMax and not p.IsPoisoned):
                    return describe(m)
            except Exception:
                pass
            return None


        def band_begun(p, now, at, buff=False):
            """2.6.85: the shard says a bandage began, whatever started it. One bar
            at a time: on a bandage this part just aimed it only sets the bar's start;
            a new one over a running one starts the bar again (the server replaces
            the first), never a second bar."""
            mine = st["phase"] == "heal" and not st["begun"] and not st["by_buff"]
            if st["phase"] == "cursor":                  # aimed by hand before we could
                HOST.release_cursor(KEY)
            if buff and st["phase"] == "heal":           # the icon of the one that runs
                return
            if not mine:
                st["target"] = guess_patient(p, now)
            st["t0"] = min(now, at)
            st["phase"], st["begun"], st["by_buff"] = "heal", not buff, buff
            st["count_at"] = min(st["count_at"], now + COUNT_AFTER_USE)


        def watch_buff(p, now):
            """2.6.85: the bandage's buff icon, if the shard sends one: its coming starts
            the bar when no journal line did, and its going ends a bar only it started."""
            try:
                up = bool(API.BuffExists(BAND_BUFF))
            except Exception:
                return None
            was, st["buff"] = st["buff"], up
            if up and not was:
                band_begun(p, now, now, True)
            elif was and not up and st["phase"] == "heal" and st["by_buff"]:
                return "done"
            return None


        def band_answer(p, now):
            """2.6.81: the server's answer to a bandage in the journal lines since
            the last tick: the refusal's words (lower case, no stop), "done" for a
            finished bandage, or None. (2.6.85) A line saying one began starts the bar
            from any phase; a bandage that began can no longer be refused, only
            lose its patient or its healer."""
            try:
                lines = st["rd"].new()
            except Exception:
                return None
            if not lines:
                return None
            own = TITLE.lower() + ":"
            for ln in lines:
                low = ln.low.strip()
                if low.startswith(own):
                    continue
                if ln.name and str(ln.name).lower() != "system":
                    continue                             # someone saying it isn't the shard
                if low.startswith(BAND_BEGUN):
                    band_begun(p, now, ln.at)
                    continue
                if st["phase"] == "idle":
                    continue
                fresh = st["phase"] == "cursor" or (not st["begun"]
                                                    and now - st["t0"] <= REFUSE_SECS)
                for x in BAND_REFUSED:
                    if low.startswith(x) and (fresh or x in BAND_REFUSED_END):
                        return low.rstrip(".!")
                if st["phase"] == "heal":
                    for x in BAND_FINISHED:
                        if low.startswith(x):
                            return "done"
            return None


        def aim_other(p, o):
            """The bandage cursor is up and ours, for someone else: them, while still
            in reach and alive; else the cursor (raised by this part) is put down."""
            try:
                m = API.FindMobile(o["serial"])
                ok = m is not None and not m.IsDead and near(m, int(p.X), int(p.Y), OTHER_RANGE)
            except Exception:
                ok = False
            if not ok:
                API.CancelTarget()                       # our own cursor: nobody else's
                API.SysMsg("%s: %s is out of reach; the bandage cursor was put down." %
                           (TITLE, o["name"]), Kit.HUE_BAD)
                return False
            API.Target(o["serial"])
            st["last"] = o
            API.SysMsg("%s: bandaging %s." % (TITLE, o["name"]), Kit.HUE_INFO)
            return True


        def _queued(p, now):
            """Clicks and changes noted since the last tick (client thread)."""
            if st["rebuild"]:
                st["rebuild"] = False
                if win["g"] is not None and win["wide"] != settings["others"]:
                    build_window()
            while st["queue"]:
                action = st["queue"].pop(0)
                kind = action[0] if isinstance(action, tuple) else action
                if kind == "follow":
                    Follow.toggle(action[1], TITLE)
                elif action == "me":
                    start_bandage(p, now, None)
                elif action == "other":
                    if not st["pick"] and st["phase"] == "idle":
                        st["pick"] = True
                        HOST.pick_target(PICK_TIMEOUT, picked, KEY)
                elif action == "again":
                    o = st["last"]
                    if o is None:
                        API.SysMsg("%s: nobody bandaged yet; use the target icon first." % TITLE,
                                   Kit.HUE_INFO)
                    else:
                        bandage_other(p, now, o["serial"])
                elif kind == "on":
                    bandage_other(p, now, action[1])


        # ---------- settings in the Virtue Assistant window ----------
        def num_text(v):
            return ("%.2f" % v).rstrip("0").rstrip(".")


        def build_config(g, x, y, w):
            Kit.add_section(g, x, y, w, CFG_H1, "BANDAGE TIMES")
            # three uniform rows: label, field, the unit in grey; the range is in the tooltip
            labels = ("On yourself:", "On someone else:", "Latency buffer:")
            tx = x + 24 + max(Kit.text_w(t) for t in labels)
            for i, (key, text, value, tip) in enumerate((
                    ("time", labels[0], st["band_time"],
                     "Seconds a bandage on yourself takes on this shard; applied once you stop "
                     "typing (%d-%d)" % (int(TIME_MIN), int(TIME_MAX))),
                    ("other", labels[1], st["other_time"],
                     "Seconds a bandage on someone else takes; much faster than on yourself on "
                     "this shard (%d-%d)" % (int(TIME_MIN), int(TIME_MAX))),
                    ("buffer", labels[2], st["buffer"],
                     "Seconds added for latency before the bar says Done (%d-%d)"
                     % (int(BUFFER_MIN), int(BUFFER_MAX))))):
                ry = y + 30 + i * 28
                Kit.add_label(g, text, x + 12, ry + 4)
                cfg[key] = Kit.add_textbox(g, num_text(value), tx, ry, 50, numbers=False)
                safe(lambda box=cfg[key], t=tip: box.SetTooltip(t))
                Kit.add_label(g, "s", tx + 50 + 8, ry + 4, Kit.HUE_INFO)
            cfg["typed"], cfg["applied"] = None, None
            y2 = y + CFG_H1 + Kit.GAP
            Kit.add_section(g, x, y2, w, CFG_H2, "ALERTS  (sound: Settings > Alerts)")
            Kit.add_label(g, "Alert when your HP is at or under:", x + 12, y2 + 34)
            px = x + 24 + Kit.text_w("Alert when your HP is at or under:")
            cfg["box"] = Kit.add_textbox(g, str(st["start_pct"]), px, y2 + 30, 40)
            safe(lambda: cfg["box"].SetTooltip("One alert when your HP falls to this percentage or "
                                               "below, again once it was above (0-99, 0 = never)"))
            Kit.add_label(g, "%", px + 48, y2 + 34, Kit.HUE_INFO)
            cfg["cure"] = Kit.add_check(
                g, "Alert when you are poisoned and a bandage could cure it", x + 12, y2 + 58,
                settings["cure"],
                "One alert per poisoning, when your Healing is %d or more and your Anatomy %d or "
                "more (a bandage then tries to cure the poison)" % (int(CURE_HEALING),
                                                                     int(CURE_ANATOMY)))
            Kit.add_label(g, "Alert when bandages drop under:", x + 12, y2 + 88)
            lx = x + 24 + Kit.text_w("Alert when bandages drop under:")
            cfg["low"] = Kit.add_textbox(g, str(settings["low"]), lx, y2 + 84, 40)
            safe(lambda: cfg["low"].SetTooltip(
                "One alert when the bandages in your backpack drop under this number "
                "(%d-%d, 0 = never)" % (LOW_MIN, LOW_MAX)))
            y3 = y2 + CFG_H2 + Kit.GAP
            Kit.add_section(g, x, y3, w, CFG_H3, "WINDOW")
            cfg["others"] = Kit.add_check(
                g, "Show who the bandage is on (a wider bar)", x + 12, y3 + 30, settings["others"],
                "The bar names the one your bandage is on. Alt+click the name: auto-follow "
                "(again to stop)")
            help_text = ("The bandage: one on you. The target icon: one on whoever you click "
                         "(within %d tile%s). The repeat arrow: one more on the last one."
                         % (OTHER_RANGE, "" if OTHER_RANGE == 1 else "s"))
            for i, line in enumerate(Kit.wrap(help_text, w - 24)[:2]):
                Kit.add_label(g, line, x + 12, y3 + 58 + i * 20, Kit.HUE_INFO)
            cfg["seen"] = (str(settings["low"]),)


        def config_closed():
            for k in ("box", "time", "other", "buffer", "cure", "low", "others"):
                cfg[k] = None
            cfg["typed"], cfg["applied"] = None, None


        def parse_time(text, lo, hi):
            try:
                v = float(str(text).strip().replace(",", "."))
            except (ValueError, TypeError):
                return None
            return v if lo <= v <= hi else None


        def poll_config():
            """Read the fields; whole numbers in range at once, the times once they
            have stood unchanged for FIELD_SETTLE (so "1" on the way to "15" never
            becomes a one-second bandage)."""
            box = cfg["box"]
            if box is None:
                return
            try:
                txt = str(box.Text).strip()
                typed = (str(cfg["time"].Text).strip(), str(cfg["other"].Text).strip(),
                         str(cfg["buffer"].Text).strip())
                ticks = (bool(cfg["cure"].IsChecked), bool(cfg["others"].IsChecked))
                low_txt = str(cfg["low"].Text).strip()
            except Exception:
                config_closed()
                return
            if txt.isdigit():
                v = int(txt)
                if PCT_MIN <= v <= PCT_MAX and v != st["start_pct"]:
                    st["start_pct"] = v
                    st["hp_armed"] = True
                    save_pct()
            changed = False
            for k, v in zip(("cure", "others"), ticks):
                if v != settings[k]:
                    settings[k] = v
                    changed = True
                    if k == "others":
                        st["rebuild"] = True                 # the bar's width changes
                    if k == "cure":
                        st["poison_armed"] = True
            if (low_txt,) != cfg["seen"]:
                cfg["seen"] = (low_txt,)
                if low_txt.isdigit():
                    v = int(low_txt)
                    if LOW_MIN <= v <= LOW_MAX and v != settings["low"]:
                        settings["low"], changed = v, True
                        st["low_armed"] = True
                        st["count_at"] = 0.0
            if changed:
                save_extra()
            now = time.time()
            if typed != cfg["typed"]:
                cfg["typed"], cfg["since"] = typed, now
                return
            if cfg.get("applied") == typed or now - cfg["since"] < FIELD_SETTLE:
                return
            cfg["applied"] = typed                   # parsed once per settled text, not every pass
            bt = parse_time(typed[0], TIME_MIN, TIME_MAX)
            ot = parse_time(typed[1], TIME_MIN, TIME_MAX)
            bf = parse_time(typed[2], BUFFER_MIN, BUFFER_MAX)
            changed = False
            if bt is not None and abs(bt - st["band_time"]) > 0.001:
                st["band_time"], changed = bt, True
            if ot is not None and abs(ot - st["other_time"]) > 0.001:
                st["other_time"], changed = ot, True
            if bf is not None and abs(bf - st["buffer"]) > 0.001:
                st["buffer"], changed = bf, True
            if changed:
                save_timing()


        # ---------- module ----------
        def _start():
            st.update({"phase": "idle", "shutting": False, "queue": [], "rebuild": False,
                       "skills": (0.0, 0.0, -1e9), "count": None, "count_at": 0.0,
                       "low_armed": True, "hp_armed": True, "poison_armed": True,
                       "target": None, "last": None, "pick": False,
                       "begun": False, "by_buff": False, "buff": False, "lt": (0, 0.0),
                       "rd": safe(Journal.reader)})       # 2.6.81: the server's answer
            load_pct()
            load_timing()
            load_extra()
            fn = getattr(HOST, "alert_kind", None)      # listed on Settings > Alerts
            if fn is not None:
                safe(lambda: fn(ALERT_LOW, "Bandages running low", ALERT_LOW_SOUND))
                safe(lambda: fn(ALERT_HP, "HP low: bandage?", ALERT_HP_SOUND))
                safe(lambda: fn(ALERT_POISON, "Poisoned (a bandage cures)", ALERT_POISON_SOUND))
                safe(lambda: fn(ALERT_READY, "Bandage done", ALERT_READY_SOUND))
            build_window()
            # (2.6.57) no zone window: it rides on the player frame (below it in the
            # top half of the screen, above it in the bottom half), nearest the frame;
            # (2.6.67) inside its zone, right of the bars, when the frame fills a zone
            # with room; with Frames off it is a free window
            pieces_add(KEY, "player", 0, lambda: win["g"])
            API.SysMsg("%s: on (%s s on you, %s s on others); one press, one bandage."
                       % (TITLE, num_text(st["band_time"]), num_text(st["other_time"])),
                       Kit.HUE_GOOD)


        def _stop():
            st["shutting"] = True
            safe(lambda: HOST.release_cursor(KEY))
            save_pos()
            pieces_remove(KEY)
            save_pct()
            save_timing()
            g, win["g"] = win["g"], None
            win["label"] = win["count"] = None
            Kit.dispose(g)


        def _interval():
            if st["phase"] == "cursor":
                return CURSOR_EVERY
            return HEAL_EVERY if st["phase"] == "heal" else WATCH_EVERY


        load_pct()
        load_timing()
        load_extra()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True,
                "interval": _interval,
                "config_height": lambda w: CFG_H, "build_config": build_config,
                "poll_config": poll_config, "config_closed": config_closed}

    def _part_pets():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Kit, Follow, Journal, HOST, the main loop and the settings window), so run
        # =============================================================================
        #  PART: Pets  -  your followers in one window
        #
        #  - A row per pet: its name, a health bar (the shard sends pets' HP as a
        #    percentage), stamina when the shard sends it, and how far and which
        #    way it is. A pet seen this session that is out of view stays listed
        #    as "out of range" while your follower count says it is still yours.
        #    Click a row: the target cursor you have up goes to that pet, else the
        #    pet becomes your Last Target. Alt+click: auto-follow it (again to stop).
        #  - Commands for all your pets (Follow me, Guard me, Stay, Come) and for
        #    each pet (Follow, Guard, Stay), said out loud like typing them, one per
        #    click.
        #  - Heal on each row: one bandage (or a Heal / Greater Heal spell, a
        #    setting) on that pet per click; the cursor is aimed at the pet when it
        #    comes.
        #  - Kill buttons ("all kill", "<name> kill") only when ticked on the
        #    settings page (off at first). They are said only when you click, and
        #    the shard then gives you its own cursor to pick the enemy: nothing of
        #    the fight is done for you (the shard doesn't allow that).
        #  - An alert when a pet's HP falls to the % you pick, and when a pet dies.
        #  - Your pets are the creatures the client lets you rename (the shard says
        #    so with their status). "Add..." lists a creature you target for this
        #    session, for one the shard hasn't sent that for yet.
        #  - While you are hidden, a command or a heal (both reveal you) waits for
        #    a second click.
        # =============================================================================
        KEY = "pets"
        TITLE = "Pets"

        # ------------------------------- CONFIG --------------------------------------
        SETTINGS_KEY = "Pets_settings"        # per character: "range=18;low=30;heal=0;kill=0;hidden=1"
        POS_KEY = "Pets_pos"                  # where the window sits
        MIN_KEY = "Pets_min"                  # minimized when last seen
        W = 440                               # full window width
        MINI_W, MINI_H = 280, 46              # minimized bar ("Pets: 3 pets, 2 in view")
        TRAY_ICON = 0x0E81                    # shepherd's crook, on the Action Bar's tray button
        SCAN_EVERY = 0.25                     # seconds between looks at your pets
        FULL_EVERY = 1.0                      # (2.6.82) seconds between full looks while your pets fill your slots
        NOT_PET_FOR = 2.5                     # (2.6.82) seconds a mobile found not to be a pet is not asked again
        NOT_PET_MAX = 400                     # (2.6.82) strangers remembered (cleared when full)
        _MOBILES = getattr(HOST, "mobiles", None)   # (2.6.82) the pass's shared mobile list
        _FIND = getattr(HOST, "mobile", None)       # (2.6.82) FindMobile, memoised for the pass
        not_pet = {}                          # (2.6.82) serial -> time it may be asked again
        LOOK_EVERY = 1.0                      # seconds between looks for known pets beyond the list
        RANGE_DEFAULT, RANGE_MIN, RANGE_MAX = 18, 2, 24   # tiles: pets listed with their bars
        MAX_ROWS = 6                          # rows drawn (more are counted only)
        ROW_H = 50                            # a row: the name line, then its buttons
        NAME_W = 130                          # px a pet's name may take
        BAR_W = 110
        FORGET_AFTER = 1800.0                 # seconds: a pet out of view this long is forgotten
        MAX_KNOWN = 20                        # pets remembered at most (the longest unseen go first)
        LOW_DEFAULT = 30                      # HP % for the low-HP alert (0 = off)
        LOW_REARM = 10                        # % above that line before a pet can alert again
        BANDAGE_GRAPHIC = 0x0E21              # clean bandage
        BANDAGE_RANGE = 1                     # tiles a bandage reaches (RunUO's bandage range: 1
        #                                       pre-AoS, 2 with AoS rules, as Bandages; UNCHECKED)
        SPELL_RANGE = 10                      # tiles a heal spell reaches (UNCHECKED IN GAME)
        CURSOR_WAIT = 3.0                     # seconds the heal's target cursor is waited for
        # 2.6.81: journal lines that mean the heal raises no cursor (RunUO texts,
        # lower case, UNCHECKED IN GAME): the heal is given up at once, so a cursor
        # the player raises himself afterwards is never aimed at the pet
        HEAL_FAILED = ("the spell fizzles", "your concentration is disturbed",
                       "insufficient mana", "more reagents are needed",
                       "you must wait to perform another action")
        CMD_GAP = 0.6                         # seconds: the same command at most this often
        CONFIRM_SECS = 3.0                    # seconds to click again while hidden
        CONFIRM_MIN = 0.3                     # (a double-click isn't a second click)
        CLICK_GRACE = 0.15                    # a click this soon after a row changed acts on the old pet
        NOTE_MAX = 10.0                       # seconds a note under the buttons stays up at most
        # What is said (UNCHECKED IN GAME: the client's own speech keywords, Speech.mul
        # 0x163-0x170; RunUO's pet AI answers them). "%s" is the pet's name.
        ALL_CMDS = (("follow", "Follow me", "all follow me"), ("guard", "Guard me", "all guard me"),
                    ("stay", "Stay", "all stay"), ("come", "Come", "all come"))
        ALL_KILL = "all kill"
        PET_CMDS = (("pet_follow", "Follow", "%s follow me"), ("pet_guard", "Guard", "%s guard"),
                    ("pet_stay", "Stay", "%s stay"))
        PET_KILL = "%s kill"
        PET_SAY = dict([(k, t) for k, _, t in PET_CMDS] + [("pet_kill", PET_KILL)])
        HEAL_WAYS = (("", "Bandage"), ("Heal", "Heal (spell)"), ("Greater Heal", "Greater Heal (spell)"))
        LOW_ALERT, DEAD_ALERT = "pets.low", "pets.dead"
        BAR_BG = "#17171a"
        BAR_HITS, BAR_POISON, BAR_STAM = "#c22d2d", "#2f9a3c", "#d39a1c"
        # -----------------------------------------------------------------------------

        settings = {"range": RANGE_DEFAULT, "low": LOW_DEFAULT, "heal": 0, "kill": False,
                    "hidden": True}
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [],
              "scan_at": 0.0, "look_at": 0.0, "followers": 0, "fmax": 0, "me": 0,
              "full_at": 0.0, "heal": None, "note": "", "note_hue": Kit.HUE_INFO, "note_until": 0.0,
              "confirm": None, "cmd_at": {}, "seq": 0, "order": []}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": [], "n_rows": -1}
        page = {"c": None}
        pets = {}             # serial -> pet record (kept for the session, across off / on)


        # ---------- saved settings ----------
        def load_settings():
            for part in Kit.get_var(SETTINGS_KEY).split(";"):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                k, v = k.strip(), v.strip()
                try:
                    if k == "range":
                        settings["range"] = max(RANGE_MIN, min(RANGE_MAX, int(v)))
                    elif k == "low":
                        settings["low"] = max(0, min(99, int(v)))
                    elif k == "heal":
                        settings["heal"] = max(0, min(len(HEAL_WAYS) - 1, int(v)))
                    elif k == "kill":
                        settings["kill"] = v == "1"
                    elif k == "hidden":
                        settings["hidden"] = v != "0"
                except ValueError:
                    continue


        def save_settings():
            Kit.put_var(SETTINGS_KEY, "range=%d;low=%d;heal=%d;kill=%d;hidden=%d" % (
                settings["range"], settings["low"], settings["heal"],
                1 if settings["kill"] else 0, 1 if settings["hidden"] else 0))


        # ---------- small helpers ----------
        def note(text, hue=None, secs=4.0):
            """A line under the ALL PETS buttons (and the minimized bar) for a few seconds."""
            st["note"], st["note_hue"] = text, Kit.HUE_INFO if hue is None else hue
            st["note_until"] = time.time() + secs
            show_note()


        def note_on(now):
            """The note is still to be shown (a clock set back doesn't keep it up)."""
            return bool(st["note"]) and 0 <= st["note_until"] - now <= NOTE_MAX


        def say_line(text, hue=None):
            API.SysMsg("%s: %s" % (TITLE, text), Kit.HUE_INFO if hue is None else hue)


        def compass(dx, dy):
            """Compass direction in UO terms (+x east, +y south)."""
            if dx == 0 and dy == 0:
                return "here"
            deg = math.degrees(math.atan2(-dy, dx))
            if deg < 0:
                deg += 360.0
            return ("E", "NE", "N", "NW", "W", "SW", "S", "SE")[int(round(deg / 45.0)) % 8]


        def ago(secs):
            secs = max(0, int(secs))
            if secs < 60:
                return "%ds" % secs
            if secs < 3600:
                return "%dm" % (secs // 60)
            return "%dh" % (secs // 3600)


        def heal_way():
            return HEAL_WAYS[settings["heal"]]


        def tiles(n):
            return "%d tile%s" % (n, "" if n == 1 else "s")


        # ---------- your pets (client thread: every read is in place) ----------
        def new_pet(serial, name, manual=False):
            st["seq"] += 1
            r = {"serial": serial, "name": name, "seq": st["seq"], "seen": 0.0, "where": "gone",
                 "pct": None, "stam": None, "dist": 0, "dir": "", "dead": False, "poison": False,
                 "low": False, "manual": manual, "alive": False}
            pets[serial] = r
            st["order"] = []                         # the row order is worked out again
            return r


        def forget(serial):
            if pets.pop(serial, None) is not None:
                st["order"] = []


        def update(r, m, px, py, now, near):
            """The pet's record from the mobile m (on the client thread)."""
            if r["manual"] and r.get("own"):         # (2.6.84) released or given away since:
                try:                                 # no longer yours for Meters
                    r["own"] = bool(m.IsRenamable)
                except Exception:
                    r["own"] = False
            try:
                name = str(m.Name or "")
            except Exception:
                name = ""
            if name:
                r["name"] = name
            try:
                hits, hmax = int(m.Hits or 0), int(m.HitsMax or 0)
            except Exception:
                hits, hmax = 0, 0
            r["pct"] = max(0, min(100, int(hits * 100 // hmax))) if hmax > 0 else None
            try:
                sta, smax = int(m.Stamina or 0), int(m.StaminaMax or 0)
            except Exception:
                sta, smax = 0, 0
            r["stam"] = max(0, min(100, int(sta * 100 // smax))) if smax > 0 else None
            dead = False
            try:
                dead = bool(m.IsDead)
                r["poison"] = bool(m.IsPoisoned)
            except Exception:
                r["poison"] = False
            try:
                ox, oy = int(m.X), int(m.Y)
                r["dist"] = max(abs(ox - px), abs(oy - py))
                r["dir"] = compass(ox - px, oy - py)
            except Exception:
                pass
            r["where"] = "near" if near else "far"
            r["seen"] = now
            if dead and not r["dead"] and r["alive"]:     # seen alive, now a ghost (bonded)
                alert(DEAD_ALERT, "%s died" % (r["name"] or "A pet"), r["serial"])
            r["dead"] = dead
            if dead:
                r["low"] = True                      # no low-HP alert for a ghost
                return
            r["alive"] = True
            low = settings["low"]
            pct = r["pct"]
            if pct is not None:
                if low > 0 and pct <= low and not r["low"]:
                    r["low"] = True
                    alert(LOW_ALERT, "%s at %d%% HP (%s)" % (r["name"] or "A pet", pct,
                                                           where_text(r)), r["serial"])
                elif r["low"] and (low <= 0 or pct >= low + LOW_REARM):
                    r["low"] = False


        def where_text(r):
            if r["dist"] == 0:
                return "here"
            return "%d tile%s %s" % (r["dist"], "" if r["dist"] == 1 else "s", r["dir"])


        def alert(key, text, serial):
            try:
                HOST.alert(key, text, "warn", who=serial)
            except Exception:
                pass


        def scan(p, now):
            """One look at your pets: those in the list range from one list of the
            mobiles near you, the others you know of (beyond it, or out of view)
            once a second, by serial."""
            try:
                me = int(p.Serial)
                px, py = int(p.X), int(p.Y)
            except Exception:
                return
            st["me"] = me
            was = st["followers"]
            try:
                st["followers"], st["fmax"] = int(p.Followers or 0), int(p.FollowersMax or 0)
            except Exception:
                st["followers"], st["fmax"] = 0, 0
            seen = set()
            lost = False
            # (2.6.82) while the pets in the list already fill your follower slots,
            # nobody new can be yours: in between the full looks (FULL_EVERY) only
            # those pets are read, by serial; one gone or out of the list range
            # (or a follower count change) makes it a full look at once
            rng = settings["range"]
            full = now >= st["full_at"] or st["full_at"] - now > FULL_EVERY or \
                st["followers"] != was
            if not full:
                near = [k for k, r in pets.items() if r["where"] == "near"]
                if len(near) < st["followers"]:
                    full = True
            if not full:
                found = []
                for k in near:
                    try:
                        m = _FIND(k) if _FIND is not None else API.FindMobile(k)
                        if m is None or int(m.Distance) > rng:
                            full = True
                            break
                    except Exception:
                        full = True
                        break
                    found.append((k, m))
                if not full:
                    for k, m in found:
                        try:
                            r = pets.get(k)
                            if r is None:
                                continue
                            if not r["manual"] and not m.IsRenamable:
                                forget(k)            # released or given away: not yours now
                                continue
                            seen.add(k)
                            update(r, m, px, py, now, True)
                        except Exception:
                            continue
                    mobs = ()
            if full:
                st["full_at"] = now + FULL_EVERY
                try:
                    if _MOBILES is not None:
                        mobs = _MOBILES(rng) or []
                    else:
                        mobs = API.GetAllMobiles(distance=rng) or []
                except Exception:
                    mobs = []
                if len(not_pet) > NOT_PET_MAX:
                    not_pet.clear()
            for m in mobs:
                try:
                    if m is None:
                        continue
                    s = int(m.Serial)
                    if s == me:
                        continue
                    r = pets.get(s)
                    if r is None:
                        u = not_pet.get(s)           # (2.6.82) a stranger: asked once a while
                        if u is not None and now < u:
                            continue
                        if not m.IsRenamable:
                            not_pet[s] = now + NOT_PET_FOR
                            continue
                        not_pet.pop(s, None)
                        if len(pets) >= MAX_KNOWN:
                            prune(now, room=1)
                            if len(pets) >= MAX_KNOWN:
                                continue             # (every pet known is in view)
                        r = new_pet(s, "")
                    elif not r["manual"] and not m.IsRenamable:
                        forget(s)                    # released or given away: not yours now
                        continue
                    seen.add(s)
                    update(r, m, px, py, now, True)
                except Exception:
                    continue
            for s, r in pets.items():
                if s not in seen and r["where"] == "near":
                    lost = True                      # it just left the list: look for it now
                    r["where"] = "far"
            if lost or now >= st["look_at"] or st["look_at"] - now > LOOK_EVERY:
                st["look_at"] = now + LOOK_EVERY
                for s in [s for s in pets if s not in seen]:
                    r = pets[s]
                    try:
                        m = _FIND(s) if _FIND is not None else API.FindMobile(s)
                    except Exception:
                        m = None
                    if m is None:
                        r["where"] = "gone"
                        continue
                    try:
                        if not r["manual"] and not m.IsRenamable:
                            forget(s)
                            continue
                    except Exception:
                        pass
                    update(r, m, px, py, now, False)
            prune(now)


        def prune(now, room=0):
            """Forget pets long out of view, and out-of-view pets beyond what your
            follower count allows (each pet takes at least one slot)."""
            gone = [r for r in pets.values() if r["where"] == "gone"]
            if not gone:
                return
            for r in gone:
                if now - r["seen"] > FORGET_AFTER:
                    forget(r["serial"])
            keep = MAX_KNOWN - room
            if st["fmax"] > 0:                       # the shard sends the follower count
                in_view = len(pets) - len([r for r in pets.values() if r["where"] == "gone"])
                keep = min(keep, max(st["followers"], in_view))
            if len(pets) > keep:
                gone = sorted([r for r in pets.values() if r["where"] == "gone"],
                              key=lambda r: r["seen"])
                while gone and len(pets) > keep:
                    forget(gone.pop(0)["serial"])


        def ordered():
            """The pets in the order they were first seen (rows don't jump about)."""
            if not st["order"] or len(st["order"]) != len(pets):
                st["order"] = sorted(pets.values(), key=lambda r: r["seq"])
            return st["order"]


        # ---------- the window ----------
        queue = Kit.queuer(st)
        on_disposed = Kit.disposer(KEY, st, win)


        def save_pos():
            Kit.save_pos(POS_KEY, win["g"])


        def picked_row(row):
            """(serial, name) a click on a pooled row is for: the pet shown, or the
            one shown just before when the row changed under the click."""
            if time.time() - row["changed"] < CLICK_GRACE and row["prev"]:
                return row["prev"]
            return row["serial"], row["name"]


        def row_click(row):
            def handler(*args):
                serial, name = picked_row(row)
                if not serial:
                    return
                if Follow.alt_held():
                    queue(("follow", serial))()          # Alt+click: auto-follow (standing rule)
                    return
                queue(("target", serial))()
            return handler


        def row_action(row, kind):
            def handler(*args):
                serial, name = picked_row(row)
                if not serial:
                    return
                if Follow.alt_held():
                    queue(("follow", serial))()
                    return
                queue((kind, serial))()
            return handler


        def flow(g, store, items, x0, y0, xmax):
            """Captioned buttons left to right, onto a new line when the next one
            doesn't fit (g None: only measure). Returns the number of lines."""
            x, y, lines = x0, y0, 1
            for key, art, caption, tip, fn, hue in items:
                bw = 35 + Kit.text_w(caption)
                if x > x0 and x + bw > xmax:
                    x, y, lines = x0, y + 26, lines + 1
                if g is not None:
                    Kit.art_button(g, store, key, art, x, y, caption, tip, hue=hue, on_click=fn)
                x += bw + 12
            return lines


        def all_items():
            items = [("all_" + k, Kit.ART_CLOSE if k == "stay" else Kit.ART_PLAY, caption,
                      "Say \"%s\" (every pet of yours that hears you)" % text,
                      queue(("all", k)), None) for k, caption, text in ALL_CMDS]
            if settings["kill"]:
                items.append(("all_kill", Kit.ART_PLAY, "Kill",
                              "Say \"%s\": the shard then gives you a target cursor to pick the "
                              "enemy (a combat command: only ever said when you click)" % ALL_KILL,
                              queue(("all", "kill")), Kit.HUE_BAD))
            return items


        def build_window():
            M = Kit.MARGIN
            IW = W - 2 * M
            n_rows = min(MAX_ROWS, len(pets))
            if st["minimized"]:
                w, h = MINI_W, MINI_H
            else:
                items = all_items()
                lines = flow(None, None, items, M + 10, 0, M + IW - 10)
                all_h = 30 + lines * 26 + 22
                pets_h = 30 + max(1, n_rows) * ROW_H + 2
                w, h = W, M + 30 + Kit.GAP + all_h + Kit.GAP + pets_h + M
            x, y = Kit.load_pos(POS_KEY, (200, 200), (w, h))
            if Kit.is_open(win["g"]):
                x, y = win["g"].GetX(), win["g"].GetY()
            old, win["g"] = win["g"], None
            store = ({}, {})
            c = {}
            rows = []
            g = G.CreateGump(True, True)
            if st["minimized"]:
                c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
            else:
                Kit.add_window_frame(g, w, h)
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"))
                # ---- ALL PETS ----
                ya = M + 30 + Kit.GAP
                Kit.add_section(g, M, ya, IW, all_h, "ALL PETS  (said out loud)")
                flow(g, store, items, M + 10, ya + 26, M + IW - 10)
                c["note"] = Kit.add_label(g, "", M + 12, ya + 30 + lines * 26 - 2, Kit.HUE_INFO)
                # ---- YOUR PETS ----
                yp = ya + all_h + Kit.GAP
                ptitle = "YOUR PETS  (click to target)"      # short: the count label sits after it
                Kit.add_section(g, M, yp, IW, pets_h, ptitle)
                c["title_end"] = M + 8 + Kit.text_w(ptitle)
                x_add = M + IW - 10 - 35 - Kit.text_w("Add...")
                Kit.art_button(g, store, "add", Kit.ART_PLAY, x_add, yp + 3, "Add...",
                               "Target a creature of yours the list doesn't show yet (listed for "
                               "this session)", on_click=queue("add"))
                c["count"] = Kit.add_label(g, "", x_add - 60, yp + 6, Kit.HUE_INFO)
                c["count_right"] = x_add - 10
                x_bar = M + 12 + NAME_W + 8
                x_info = x_bar + BAR_W + 10
                buttons = [(k, art, cap) for (k, cap, _), art in
                           zip(PET_CMDS, (Kit.ART_PLAY, Kit.ART_PLAY, Kit.ART_CLOSE))]
                buttons.append(("heal", Kit.ART_PLAY, "Heal"))
                if settings["kill"]:
                    buttons.append(("pet_kill", Kit.ART_PLAY, "Kill"))
                for i in range(n_rows):
                    ry = yp + 30 + i * ROW_H
                    row = {"serial": 0, "name": "", "prev": None, "changed": 0.0,
                           "vis_hits": False, "vis_poison": False, "stam_on": False}
                    row["name_lbl"] = Kit.add_label(g, "", M + 12, ry + 3, Kit.HUE_TEXT)
                    bars = {}
                    for v, col in (("hits", BAR_HITS), ("poison", BAR_POISON)):
                        pb = G.CreateGumpSimpleProgressBar(BAR_W, 9, BAR_BG, col, 0, 100)
                        pb.SetPos(x_bar, ry + 6)
                        safe(lambda: pb.SetAcceptMouseInput(False))
                        g.Add(pb)
                        safe(lambda: setattr(pb, "IsVisible", False))
                        bars[v] = pb
                    sb = G.CreateGumpSimpleProgressBar(BAR_W, 3, BAR_BG, BAR_STAM, 0, 100)
                    sb.SetPos(x_bar, ry + 16)
                    safe(lambda: sb.SetAcceptMouseInput(False))
                    g.Add(sb)
                    safe(lambda: setattr(sb, "IsVisible", False))
                    row["bars"], row["stam_bar"] = bars, sb
                    row["info"] = Kit.add_label(g, "", x_info, ry + 3, Kit.HUE_INFO)
                    Kit.catcher(g, M + 10, ry, IW - 20, 22, row_click(row),
                                "Click: aim the target cursor you have up at this pet, or make it "
                                "your last target. Alt+click: auto-follow (again to stop)")
                    xb = M + 10
                    for kind, art, cap in buttons:
                        if kind == "heal":
                            way = heal_way()
                            tip = ("Use one bandage on this pet (within %s)"
                                   % tiles(BANDAGE_RANGE) if not way[0] else
                                   "Cast %s on this pet (within %d tiles)" % (way[0], SPELL_RANGE))
                        elif kind == "pet_kill":
                            tip = ("Say \"<name> kill\": the shard then gives you a target cursor to "
                                   "pick the enemy (a combat command: only ever said when you click)")
                        else:
                            tip = "Say \"%s\"" % (dict((k, t) for k, _, t in PET_CMDS)[kind]
                                                  % "<name>")
                        Kit.art_button(g, store, "%s%d" % (kind, i), art, xb, ry + 24, cap,
                                       tip + ". Alt+click: auto-follow (again to stop)",
                                       hue=Kit.HUE_BAD if kind == "pet_kill" else None,
                                       on_click=row_action(row, kind))
                        xb += 35 + Kit.text_w(cap) + 12
                    rows.append(row)
                c["empty"] = Kit.add_label(g, "", M + 12, yp + 33, Kit.HUE_INFO) if not n_rows else None
            Kit.place(g, x, y, w, h)                     # wholly on screen (the window rules)
            win.update({"g": g, "c": c, "rows": rows, "store": store, "n_rows": n_rows,
                        "count_w": None})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))      # saved the moment you let go of it
            if st["minimized"] and st["docked"]:         # folded into the Action Bar
                safe(lambda: setattr(g, "IsVisible", False))
            Kit.dispose(old)
            draw(time.time())


        def set_vis(row, key, ctrl, on):
            if row.get(key) != on:
                row[key] = on
                try:
                    ctrl.IsVisible = on
                except Exception:
                    pass


        def set_progress(row, key, ctrl, v):
            if row.get(key) != v:
                row[key] = v
                try:
                    ctrl.SetProgress(float(v), 100.0)
                except Exception:
                    pass


        def status_text():
            """(text, hue) for the minimized bar."""
            if note_on(time.time()):
                return st["note"], st["note_hue"]
            low = [r for r in pets.values() if r["low"] and not r["dead"] and r["where"] != "gone"
                   and r["pct"] is not None]
            if low:
                r = min(low, key=lambda r: r["pct"])
                return "%s: %s %d%% HP" % (TITLE, Kit.fit(r["name"] or "pet", 80), r["pct"]), \
                    Kit.HUE_BAD
            near = len([r for r in pets.values() if r["where"] != "gone"])
            if not pets:
                return "%s: none in view" % TITLE, Kit.HUE_INFO
            return "%s: %d pet%s, %d in view" % (TITLE, len(pets), "" if len(pets) == 1 else "s",
                                                 near), Kit.HUE_INFO


        def show_note():
            c = win["c"]
            if win["g"] is None or st["docked"]:
                return
            if st["minimized"]:
                lbl = c.get("status")
                if lbl is not None:
                    t, hue = status_text()
                    Kit.set_text(lbl, Kit.fit(t, MINI_W - 90), hue)
                return
            lbl = c.get("note")
            if lbl is not None:
                on = note_on(time.time())
                Kit.set_text(lbl, Kit.fit(st["note"], W - 2 * Kit.MARGIN - 24) if on else "",
                             st["note_hue"])


        def draw(now):
            """Bring the window up to date (client thread). Folded: nothing;
            minimized: the status line only; rows are reassigned in place."""
            if win["g"] is None or st["shutting"] or st["docked"]:
                return
            if st["minimized"]:
                show_note()
                return
            order = ordered()
            if min(MAX_ROWS, len(order)) != win["n_rows"]:
                build_window()                           # a pet more or fewer: the rows change
                return
            c = win["c"]
            for row, r in zip(win["rows"], order):
                s = r["serial"]
                if s != row["serial"]:
                    row["prev"] = (row["serial"], row["name"]) if row["serial"] else None
                    row["changed"] = now
                    row["serial"] = s
                row["name"] = r["name"]
                where, pct = r["where"], r["pct"]
                if r["dead"]:
                    hue = Kit.HUE_INFO
                elif where == "gone":
                    hue = Kit.HUE_INFO
                elif r["low"]:
                    hue = Kit.HUE_BAD
                elif r["poison"]:
                    hue = Kit.HUE_GOOD
                else:
                    hue = Kit.HUE_TEXT
                Kit.set_text(row["name_lbl"], Kit.fit(r["name"] or "(no name yet)", NAME_W), hue)
                bar = None
                if where == "near" and not r["dead"]:
                    bar = "poison" if r["poison"] else "hits"
                    info = "%s  %s" % ("%d%%" % pct if pct is not None else "?%",
                                       "here" if r["dist"] == 0 else "%d %s" % (r["dist"], r["dir"]))
                elif r["dead"] and where != "gone":
                    info = "dead  %d %s" % (r["dist"], r["dir"])
                elif where == "far":
                    info = "far: %d %s" % (r["dist"], r["dir"])
                else:
                    info = "out of range (%s)" % ago(now - r["seen"]) if r["seen"] else "out of range"
                Kit.set_text(row["info"], info, Kit.HUE_TEXT if bar else Kit.HUE_INFO)
                for v, pb in row["bars"].items():
                    set_vis(row, "vis_" + v, pb, v == bar)
                if bar:
                    set_progress(row, "p_" + bar, row["bars"][bar], pct if pct is not None else 0)
                stam = r["stam"] if bar else None
                set_vis(row, "stam_on", row["stam_bar"], stam is not None)
                if stam is not None:
                    set_progress(row, "p_stam", row["stam_bar"], stam)
            # the follower count, right-aligned before "Add..."
            lbl = c.get("count")
            if lbl is not None:
                if st["fmax"] > 0:
                    txt = "%d / %d slots" % (st["followers"], st["fmax"])
                else:
                    txt = "%d known" % len(pets) if pets else ""
                if len(order) > MAX_ROWS:
                    more = "%d more  %s" % (len(order) - MAX_ROWS, txt)
                    if c["count_right"] - Kit.text_px(more) >= c["title_end"] + 8:
                        txt = more                       # (only when it clears the title)
                Kit.set_text(lbl, txt)
                tw = Kit.text_px(txt) if txt else 0
                if win["count_w"] != tw:
                    win["count_w"] = tw
                    safe(lambda: Kit.ui_pos(lbl, c["count_right"] - tw, Kit.ui_y(lbl)))
            empty = c.get("empty")
            if empty is not None:
                if st["followers"] > 0:
                    Kit.set_text(empty, "%d slot%s used, none in view. Add... lists one."
                                 % (st["followers"], "" if st["followers"] == 1 else "s"))
                else:
                    Kit.set_text(empty, "No pets in view. Click Add... to list one.")
            show_note()


        # ---------- what a click asks for (client thread, never waiting) ----------
        def gate(action, p, now):
            """A command or a heal reveals you: while hidden it waits for a second
            click of the same button. True when it may go ahead."""
            if not settings["hidden"]:
                return True
            try:
                hidden = bool(p.IsHidden)
            except Exception:
                hidden = False
            if not hidden:
                st["confirm"] = None
                return True
            cf = st["confirm"]
            if cf is not None and cf[0] == action and cf[1] <= now <= cf[2]:
                st["confirm"] = None
                return True
            st["confirm"] = (action, now + CONFIRM_MIN, now + CONFIRM_SECS)
            note("You are hidden and that reveals you: click again to do it.", Kit.HUE_TITLE,
                 CONFIRM_SECS)
            return False


        def say(text, now):
            """Say a command out loud (one per click; a double-click is one)."""
            last = st["cmd_at"].get(text)
            if last is not None and 0 <= now - last < CMD_GAP:
                return
            if len(st["cmd_at"]) > 50:
                st["cmd_at"].clear()
            st["cmd_at"][text] = now
            API.Msg(text)
            note("Said \"%s\"." % text)


        def pet_name(serial):
            r = pets.get(serial)
            if r is None or not r["name"]:
                note("That pet has no name the client knows yet.", Kit.HUE_BAD)
                return None
            return r["name"]


        def do_target(serial):
            """A click on a row: your cursor (when you have one up) goes to the pet,
            else it becomes your Last Target. Never another module's cursor."""
            try:
                up = bool(API.HasTarget("any"))
            except Exception:
                up = False
            if up and not HOST.cursor_busy(KEY):
                API.Target(serial)
                if st["heal"] is not None:               # you aimed the heal's cursor yourself
                    st["heal"] = None
                    HOST.release_cursor(KEY)
                return
            try:
                API.SetLastTarget(serial=serial)
            except Exception:
                safe(lambda: API.SetLastTarget(serial))
            API.HeadMsg("* last target *", serial, 0x35)


        def start_heal(serial, p, now):
            """One bandage (or heal spell) for that pet: used now, its cursor aimed
            at the pet on a later tick (heal_tick)."""
            r = pets.get(serial)
            name = (r and r["name"]) or "that pet"
            if st["heal"] is not None:
                note("A heal is already on its way.", Kit.HUE_TITLE)
                return
            try:
                if p.IsDead:
                    note("You are dead.", Kit.HUE_BAD)
                    return
            except Exception:
                pass
            try:
                up = bool(API.HasTarget("any"))
            except Exception:
                up = False
            if up or HOST.cursor_busy(KEY):
                note("A target cursor is up: aim it or press Esc first.", Kit.HUE_TITLE)
                return
            spell, label = heal_way()
            reach = SPELL_RANGE if spell else BANDAGE_RANGE
            try:
                m = API.FindMobile(serial)
                d = max(abs(int(m.X) - int(p.X)), abs(int(m.Y) - int(p.Y))) if m is not None else None
            except Exception:
                m, d = None, None
            if m is None or d is None:
                note("%s is out of range." % name, Kit.HUE_BAD)
                return
            if d > reach:
                note("%s is %d tiles away (%s reaches %d)." % (name, d, label.lower(), reach),
                     Kit.HUE_BAD)
                return
            if not gate(("heal", serial), p, now):
                return
            if spell:
                API.CastSpell(spell)
                info = safe(lambda: Kit.spell_info(spell))
                wait = (info[3] if info else 1.5) + CURSOR_WAIT
            else:
                try:
                    b = API.FindType(BANDAGE_GRAPHIC, API.Backpack)
                except Exception:
                    b = None
                if not b:
                    note("Out of bandages.", Kit.HUE_BAD)
                    say_line("out of bandages!", Kit.HUE_BAD)
                    return
                API.UseObject(b.Serial)
                wait = CURSOR_WAIT
            HOST.claim_cursor(KEY, wait)             # the cursor that comes is ours
            # 2.6.81: t0 = the press, for the journal check in heal_tick
            st["heal"] = {"serial": serial, "name": name, "until": now + wait, "reach": reach,
                          "what": spell or "a bandage", "t0": now,
                          "rd": safe(Journal.reader)}     # (2.6.82) only new lines are looked at
            note("%s for %s..." % (spell or "Bandage", name))


        def heal_tick(p, now):
            """The heal's cursor came: aim it at the pet (still in reach), or put
            our own cursor down; nothing came in time: give up (client thread)."""
            j = st["heal"]
            # 2.6.81: the heal raised no cursor (fizzled, disturbed, no mana or
            # reagents, the shard's action delay): give it up now, so a cursor the
            # player raises himself in the wait is never aimed at the pet
            failed = None
            try:
                rd = j.get("rd")
                if rd is None:
                    failed = Journal.find(j.get("t0", now), HEAL_FAILED)
                else:
                    for ln in rd.new():          # (2.6.82) the lines since the last look only
                        low = ln.low
                        for x in HEAL_FAILED:
                            if x in low:
                                failed = ln
                                break
                        if failed is not None:
                            break
            except Exception:
                failed = None
            if failed is not None:
                st["heal"] = None
                HOST.release_cursor(KEY)
                note("%s for %s failed." % (j["what"][0].upper() + j["what"][1:], j["name"]),
                     Kit.HUE_BAD)
                return
            try:
                mine = HOST.cursor_claim[0] == KEY
            except Exception:
                mine = False
            # 2.6.81: only a beneficial cursor (the heal's or the bandage's) is aimed;
            # any other kind is the player's own and is neither aimed nor cancelled
            if mine and HOST.cursor_ok(KEY, "beneficial"):
                ok = False
                try:
                    m = API.FindMobile(j["serial"])
                    ok = m is not None and max(abs(int(m.X) - int(p.X)),
                                               abs(int(m.Y) - int(p.Y))) <= j["reach"]
                except Exception:
                    ok = False
                st["heal"] = None
                HOST.release_cursor(KEY)
                if ok:
                    API.Target(j["serial"])
                    note("%s on %s." % (j["what"][0].upper() + j["what"][1:], j["name"]), Kit.HUE_GOOD)
                else:
                    API.CancelTarget()                   # our own cursor: nobody else's
                    note("%s moved out of reach." % j["name"], Kit.HUE_BAD)
                return
            if not 0 <= j["until"] - now <= CURSOR_WAIT + 10.0:      # (further: the clock was set back)
                st["heal"] = None
                HOST.release_cursor(KEY)
                try:
                    up = bool(API.HasTarget("any"))      # only for the note
                except Exception:
                    up = False
                if up:
                    note("A target cursor is up: aim it or press Esc.", Kit.HUE_TITLE)
                else:
                    note("No target cursor came for %s." % j["name"], Kit.HUE_BAD)


        def picked(serial):
            """The "Add..." cursor's answer (a later pass: only queued)."""
            st["queue"].append(("added", int(serial or 0)))


        def add_pet(serial, p, now):
            if not serial:
                return
            if serial == st["me"] or serial == safe(lambda: int(p.Serial), 0):
                note("That's you.", Kit.HUE_BAD)
                return
            try:
                m = API.FindMobile(serial)
            except Exception:
                m = None
            if m is None:
                note("That isn't a creature in view.", Kit.HUE_BAD)
                return
            r = pets.get(serial)
            if r is None:
                if len(pets) >= MAX_KNOWN:
                    prune(now, room=1)
                if len(pets) >= MAX_KNOWN:
                    note("The list is full (%d)." % MAX_KNOWN, Kit.HUE_BAD)
                    return
                r = new_pet(serial, "", manual=True)
            r["manual"] = True
            try:
                r["own"] = bool(m.IsRenamable)       # (2.6.83) yours: still listed for Meters
            except Exception:
                r["own"] = False
            try:
                px, py = int(p.X), int(p.Y)
            except Exception:
                px, py = 0, 0
            update(r, m, px, py, now, True)
            if r["dist"] > settings["range"]:
                r["where"] = "far"
            note("%s is listed for this session." % (r["name"] or "It"), Kit.HUE_GOOD)


        def handle(action, p, now):
            kind = action[0] if isinstance(action, tuple) else action
            if action == "settings":
                HOST.show_settings(KEY)
            elif action == "toggle_min":
                st["minimized"] = not st["minimized"]
                st["docked"] = False
                HOST.dock_forget(KEY)                # its own minimized form, not the bar
                Kit.save_min(MIN_KEY, st["minimized"])
                build_window()
            elif action == "to_bar":
                HOST.dock_to_bar(KEY, TITLE)
            elif action == "redraw":
                build_window()
            elif action == "add":
                HOST.pick_target(10.0, picked)
                note("Target the pet to list.")
            elif kind == "added":
                if p is not None:
                    add_pet(action[1], p, now)
            elif kind == "follow":                   # Alt+click (standing rule)
                Follow.toggle(action[1], TITLE)
            elif p is None:
                return
            elif kind == "target":
                do_target(action[1])
            elif kind == "heal":
                start_heal(action[1], p, now)
            elif kind == "all":
                k = action[1]
                if k == "kill" and not settings["kill"]:
                    return                           # (a click from before the setting changed)
                text = ALL_KILL if k == "kill" else dict((a, t) for a, _, t in ALL_CMDS).get(k)
                if text and not dead_now(p) and gate(action, p, now):
                    say(text, now)
            elif kind in PET_SAY:
                if kind == "pet_kill" and not settings["kill"]:
                    return
                name = pet_name(action[1])
                if name is None or dead_now(p) or not gate(action, p, now):
                    return
                say(PET_SAY[kind] % name, now)


        def dead_now(p):
            try:
                if p.IsDead:
                    note("You are dead: your pets can't hear you.", Kit.HUE_BAD)
                    return True
            except Exception:
                pass
            return False


        # ---------- settings page (drawn inside the Virtue Assistant window) ----------
        SEC1_H = 30 + 28 + 26 + 6         # WINDOW: the range field, the hidden check
        SEC4_H = 30 + 28 + 6              # ALERTS: the low-HP field
        HEAL_INFO = ("One heal per click; its cursor is aimed at the pet when it comes (a bandage "
                     "within %s, a spell within %d)." % (tiles(BANDAGE_RANGE), SPELL_RANGE))
        KILL_INFO = ("Said only when you click; the shard then gives you its own target cursor to "
                     "pick the enemy.")


        def sec_heights(w):
            h2 = 30 + 28 + 20 * len(Kit.wrap(HEAL_INFO, w - 28)) + 6
            h3 = 30 + 28 + 20 * len(Kit.wrap(KILL_INFO, w - 28)) + 6
            return h2, h3


        def config_height(w):
            h2, h3 = sec_heights(w)
            return SEC1_H + Kit.GAP + h2 + Kit.GAP + h3 + Kit.GAP + SEC4_H


        def build_config(g, x, y, w):
            c = {}
            h2, h3 = sec_heights(w)
            Kit.add_section(g, x, y, w, SEC1_H, "WINDOW")
            t1 = "List pets within:"
            Kit.add_label(g, t1, x + 12, y + 34)
            rx = x + 24 + Kit.text_w(t1)
            c["range"] = Kit.add_textbox(g, str(settings["range"]), rx, y + 30, 44)
            safe(lambda: c["range"].SetTooltip("Tiles from you within which a pet is listed with "
                                               "its bars (%d-%d)" % (RANGE_MIN, RANGE_MAX)))
            Kit.add_label(g, "tiles", rx + 44 + 8, y + 34, Kit.HUE_INFO)
            c["hidden"] = Kit.add_check(g, "While hidden, a command or a heal needs a second click",
                                        x + 12, y + 58, settings["hidden"],
                                        "Speaking and healing reveal you: the first click only asks")
            y2 = y + SEC1_H + Kit.GAP
            Kit.add_section(g, x, y2, w, h2, "HEAL BUTTON  (on each pet's row)")
            Kit.add_label(g, "Heal with:", x + 12, y2 + 34)
            for i, line in enumerate(Kit.wrap(HEAL_INFO, w - 28)):
                Kit.add_label(g, line, x + 12, y2 + 58 + i * 20, Kit.HUE_INFO)
            y3 = y2 + h2 + Kit.GAP
            Kit.add_section(g, x, y3, w, h3, "COMBAT COMMANDS")
            c["kill"] = Kit.add_check(g, "Show Kill buttons (\"%s\" and \"<name> kill\")" % ALL_KILL,
                                      x + 12, y3 + 30, settings["kill"],
                                      "A Kill button for all your pets and one on each pet's row")
            for i, line in enumerate(Kit.wrap(KILL_INFO, w - 28)):
                Kit.add_label(g, line, x + 12, y3 + 58 + i * 20, Kit.HUE_INFO)
            y4 = y3 + h3 + Kit.GAP
            Kit.add_section(g, x, y4, w, SEC4_H, "ALERTS  (sound: Settings > Alerts)")
            t2 = "Alert when a pet's HP falls to:"
            Kit.add_label(g, t2, x + 12, y4 + 34)
            lx = x + 24 + Kit.text_w(t2)
            c["low"] = Kit.add_textbox(g, str(settings["low"]), lx, y4 + 30, 44)
            safe(lambda: c["low"].SetTooltip("One alert when a pet's HP falls to this percentage "
                                             "or below, again once it recovered (0-99, 0 = never)"))
            Kit.add_label(g, "%", lx + 44 + 8, y4 + 34, Kit.HUE_INFO)
            # the drop-down last, so its open list draws on top
            dd = G.CreateDropDown(200, [label for _, label in HEAL_WAYS], settings["heal"])
            dd.SetPos(x + 12 + Kit.text_w("Heal with:") + 10, y2 + 30)
            g.Add(dd)
            safe(lambda: dd.SetTooltip("What the Heal button on each pet's row uses: a bandage or "
                                       "a heal spell"))
            c["heal"] = dd
            page["c"] = c


        def poll_config():
            c = page["c"]
            if c is None:
                return
            changed, relayout = False, False
            try:
                txt = str(c["range"].Text or "").strip()
                if txt.isdigit():
                    v = max(RANGE_MIN, min(RANGE_MAX, int(txt)))
                    if v != settings["range"]:
                        settings["range"], changed = v, True
                txt = str(c["low"].Text or "").strip()
                if txt.isdigit():
                    v = max(0, min(99, int(txt)))
                    if v != settings["low"]:
                        settings["low"], changed = v, True
                v = bool(c["hidden"].IsChecked)
                if v != settings["hidden"]:
                    settings["hidden"], changed = v, True
                    st["confirm"] = None
                v = bool(c["kill"].IsChecked)
                if v != settings["kill"]:
                    settings["kill"], changed, relayout = v, True, True
                i = int(c["heal"].GetSelectedIndex())
                if 0 <= i < len(HEAL_WAYS) and i != settings["heal"]:
                    settings["heal"], changed, relayout = i, True, True   # (the Heal tooltips)
            except Exception:
                page["c"] = None
                return
            if changed:
                save_settings()
                if relayout and win["g"] is not None:
                    queue("redraw")()


        def config_closed():
            page["c"] = None


        # ---------- module hooks ----------
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "heal": None,
                       "confirm": None, "scan_at": 0.0, "look_at": 0.0, "note": "",
                       "full_at": 0.0,                   # (2.6.82) the next full look (scan)
                       "note_until": 0.0, "order": [],
                       "minimized": Kit.load_min(MIN_KEY)
                       or bool(safe(lambda: HOST.dock_wanted(KEY), False))})
            load_settings()
            for r in pets.values():                  # what we knew is re-read on the first scan
                r["where"] = "gone" if r["where"] == "gone" else "far"
            safe(lambda: HOST.alert_kind(LOW_ALERT, "Pet HP low", 0x335))
            safe(lambda: HOST.alert_kind(DEAD_ALERT, "Pet died", 0x1F1))
            build_window()
            HOST.dock_add(KEY, Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw")))
            if hasattr(HOST, "services"):
                HOST.services["pets.list"] = svc_pets


        def svc_pets(distance=None):
            """(2.6.82) HOST.services["pets.list"](distance=None): the serials of your
            pets (renamable mobiles, the ones added by hand left out) seen within
            `distance` tiles on Pets' last look (every SCAN_EVERY s; a new pet
            shows up to NOT_PET_FOR s later). None when Pets can't answer for that
            distance (beyond its list range, or Pets is off): look yourself then."""
            if st["shutting"]:
                return None
            rng = settings["range"]
            if distance is None:
                distance = rng
            if distance > rng:
                return None
            return [k for k, r in pets.items()
                    if r["where"] == "near" and (not r["manual"] or r.get("own"))
                    and r["dist"] <= distance]


        def _tick():
            if win["g"] is None:
                return
            if Kit.was_clicked(win["store"], "close"):
                Kit.dispose(win["g"])            # on_disposed turns the module off
                return
            now = time.time()
            p = API.Player
            while st["queue"]:
                handle(st["queue"].pop(0), p, now)
                if win["g"] is None:
                    return
            if p is None:
                return
            if st["heal"] is not None:
                heal_tick(p, now)
            if now >= st["scan_at"] or st["scan_at"] - now > SCAN_EVERY:
                st["scan_at"] = now + SCAN_EVERY
                scan(p, now)
                draw(now)
            elif st["note"] and not note_on(now):
                st["note"] = ""
                show_note()


        def _stop():
            st["shutting"] = True
            if hasattr(HOST, "services") and HOST.services.get("pets.list") is svc_pets:
                HOST.services.pop("pets.list", None)
            if st["heal"] is not None:
                st["heal"] = None
            safe(lambda: HOST.release_cursor(KEY))
            HOST.dock_remove(KEY)
            save_pos()
            Kit.save_min(MIN_KEY, st["minimized"])
            save_settings()
            g, win["g"] = win["g"], None
            win["rows"], win["c"], win["n_rows"] = [], {}, -1
            Kit.dispose(g)


        load_settings()
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True,          # tick on the client thread: no waits in it
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        # ============================= MODULE END ====================================
        return MODULE

    # ---------- the parts, run side by side by the mother's PartSet ----------
    #  (part key, builder, tick interval, the 2.6.06 module key it keeps)
    PARTS = (
        ("frames", _part_frames, 0.1, "unitframes"),
        ("timers", _part_timers, 0.1, "spelltimers"),
        ("swing", _part_swing, 0.025, "swing"),
        ("bandage", _part_bandage, 0.1, "bandage"),
        ("pets", _part_pets, 0.1, "pets"),
    )
    MODULE = PartSet(KEY, TITLE, PARTS).hooks()
    return MODULE


# ------------------------- registration with Virtue Assistant ----------------
if "HOST" in globals() and hasattr(globals()["HOST"], "add"):
    HOST.add("hud", "Character HUD",
             "Frames and bars for you, your target, your party and pets",
             _module_hud, 0.025,
             category="On screen",
             parts=(
                 ("frames", "Frames",
                  "Health frames for you, your target and your party", True,
                  ("unitframes",)),
                 ("timers", "Buffs & Timers",
                  "Your buffs and debuffs, and your spells on others, timed", True,
                  ("spelltimers",)),
                 ("swing", "Swing Bar",
                  "A bar that shows when your next melee swing lands", False, ("swing",)),
                 ("bandage", "Bandages",
                  "One press, one bandage: a timer bar and alerts", False, ("bandage",)),
                 ("pets", "Pets",
                  "Your pets' health, distance and commands", False, ("pets",)),
             ),
             aliases=('Unit Frames', 'Spell Timers', 'Swing Timer', 'Bandage Agent', 'Pets', 'cast bar', 'buffs', 'debuffs', 'party frames', 'hit chance'))
else:
    import API
    API.SysMsg("Character HUD is a Virtue Assistant module and can't run on its own. "
               "Run Virtue Assistant instead; it loads this file.", 33)
