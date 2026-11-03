# =============================================================================
#  Ultima Tracker  -  a Virtue Assistant module (TazUO Legion Script, Python)
#  Shard: In Mani Ylem
#
#  This file is NOT a script to run on its own. It is one module of Virtue
#  Assistant, loaded by Virtue Assistant from LegionScripts/VirtueAssistantModules.
#  Virtue Assistant provides everything this file uses (API, G, safe, Client,
#  Kit, Follow, HOST, Journal, the main loop and the settings window), so run
#  that instead and tick Ultima Tracker on its Modules tab.
#
#  To leave this module out, take this file out of the folder.
#  Module key: "ultima"
#
#  A module made of PARTS (2.6.5): each part below was a module of its own in
#  2.6.06 and keeps every saved key, window place, list and file it had. A
#  part has its own box under the module's row on the Modules tab (click the
#  arrow on the row to see them) and runs only while it is ticked; the mother
#  script's PartSet runs the ticked parts side by side. The old module keys
#  still answer (the Action Bar's mod: cells, HOST.enable, HOST.by_key).
#
#     Tracker          (was UltimaTracker)    Trackers and combat bars for the players around you
#     Lookout          (was Lookout)          A second client watches a spot and raises the alarm here
#
#  On the lookout client tick only Lookout: the trackers, combat bars and the
#  sightings file then cost nothing there.
#
#  2.6.82: speed pass: fewer client reads per mobile, per bar and per pass (the
#  cheap tests first, each value read once, shared per-pass reads); same results.
# =============================================================================


def _module_ultima():
    """Builds the module from its parts and returns its hooks."""
    KEY = "ultima"
    TITLE = "Ultima Tracker"


    def _part_tracker():
        # ---- notes carried over from the 2.6.06 module file ----
        #  Assistant, loaded by the mother script from its VirtueAssistantModules folder.
        # =============================================================================
        #  MODULE: Ultima Tracker  (from UltimaTracker v1.5)
        #  Ultima Online: The Second Age  -  In Mani Ylem shard
        #
        #  Combines PlayerTracker (v2-1) and CombatBars (MobTracker v5).
        #
        #  Every window is drawn with the shared native look (Kit): the stone frame
        #  of the crafting gump around a black section, the UO font in notoriety
        #  hues, smooth soft-coloured health bars (outlined, with a dark track for
        #  the missing HP; see BAR_PAINT) and stone buttons. If your client can't
        #  load a piece of that art, that part falls back to a flat style (see
        #  NATIVE_STYLE).
        #  The title strip has the same buttons on the right of every window:
        #
        #    [padlock]  lock the window in place (no moving / resizing). The client's
        #               own padlock: red while locked, plain and dim while unlocked.
        #    [arrow]    minimize the window to its title strip / restore it
        #    [gem]      folds out a 0-100 background-opacity slider for that window.
        #               The frame and bars always stay solid.
        #    [x]        pop-out health bars only: close the bar
        #
        #  Double-click any window's title strip to minimize / restore it.
        #
        #  Anchoring: drag any window (trackers, combat bars, panel, pop-outs) so an
        #  edge lands next to another window's edge and let go: it snaps flush and
        #  the two are anchored, so dragging either one moves the whole group.
        #  Alt+drag pulls a single window out of its group; "Unanchor all" on the
        #  Settings tab breaks every group. Groups are saved (pop-outs aren't).
        #
        #  PLAYER TRACKERS - three resizable windows that automatically show a health
        #  bar for every player near you:
        #
        #    FRIENDS  - party members, TazUO friends-list, guild/alliance (green names)
        #    FOES     - red names (murderers/PKers), your saved Foe list, and
        #               optionally orange (war enemies) and gray (criminals)
        #    NEUTRAL  - every other player
        #
        #  Not players and never listed: your pets, yellow (invulnerable) vendors and
        #  healers, and blue town NPCs - recognized by a job title in the name ("Bob
        #  the guard") or by a plain first name from the server's NPC name lists
        #  ("Candra", "Thierry"). A blue player who happens to share one of those
        #  names shows up as soon as they run, ride, go to war mode, are on your
        #  party / friends / Foe list, or you single-click them and the journal shows
        #  their karma tag ("Draxt: [Dubious]") - that last one is remembered for
        #  good. NPCs that announce a title on a click ("Melia the town crier") are
        #  hidden too. Red and grey human NPCs (brigands, grey wandering healers) are
        #  hidden only by a title: once a single-click shows "<name> the <job>", or
        #  when the client's name line carries that title (never by a plain first
        #  name, so a red player is never hidden). One that never shows a title
        #  stays listed until you press "N" on its row. Anything else that slips
        #  through: press "N" on its row.
        #
        #  FRIENDS bars and their pop-outs show status colors (green = poisoned,
        #  pale = paralyzed, teal = both, gray = dead) and pulse red at
        #  GLOW_HP_PCT (50%) HP or lower. With "Magery buttons" on (Settings page)
        #  they get an H (Heal) and C (Cure) button; Shift+click casts Greater Heal /
        #  Arch Cure. With "Bandage button" on, the B button bandages that friend when
        #  you're within BANDAGE_RANGE (one press, one bandage); farther away it only
        #  auto-follows them, and B again stops that follow. Press B again once you
        #  reach them to bandage.
        #
        #  COMBAT BARS - one window that stacks a condensed health bar for every
        #  hostile (monster or player) you're in combat with:
        #
        #   * Bar colour:  red = normal, green = poisoned, pale = paralyzed,
        #                  teal = poisoned AND paralyzed  (flat style: blue = paralyzed)
        #   * Tag text :   PSN / PAR (and FOL while you auto-follow it) next to HP %
        #   * Name hue :   matches the mobile's notoriety
        #   * Resize / scale: drag any corner (the strip along the bottom edge is the
        #     easiest grab). The width sets the scale; the height snaps to fit.
        #   * Minimized, the title strip keeps showing how many hostiles you're
        #     fighting, the lowest HP among them and PSN/PAR counts.
        #   * "Magery buttons" (on the Settings tab): adds a green P (Poison) and pale
        #     Z (Paralyze) button next to every bar; the spell is aimed at that
        #     hostile as soon as the target cursor appears (gives up after
        #     CAST_TIMEOUT seconds if it fizzles).
        #   How "in combat with" is decided (the client has no aggressor list):
        #     1. "<name> is attacking you" journal messages
        #     2. Anything you target or attack (API.LastTargetSerial)
        #     3. Hostile-notoriety mobiles (gray/criminal/enemy/murderer) in war mode
        #        within COMBAT_RANGE
        #     4. Anything already on the list stays while it keeps losing hit points
        #   With "Combat bars: only once fighting" on (the default, Settings tab),
        #   #2 only counts while you're in war mode and #3 only within MELEE_RANGE,
        #   so a mobile shows up only once you're actually fighting it.
        #   Never shown: friends, party members, your pets, vendors / player vendors /
        #   healers (yellow), and blue or green NPCs and players unless they attack you.
        #   A mobile is dropped when it dies, leaves MAX_RANGE, or shows no combat
        #   activity for IDLE_TIMEOUT seconds.
        #
        #  CONTROL PANEL (Ultima Tracker's section of the shared Ultima Tracker window) lets you:
        #    - add/remove players on your permanent Foe list by name or by targeting
        #    - ignore NPCs that slip through
        #    - lock/unlock every tracker, the combat bars and pop-outs at once
        #    - show or hide the combat bars window
        #  and its Settings button opens Ultima Tracker's page of the Virtue
        #  Assistant Settings tab, where you can:
        #    - scale the player trackers and pop-outs (50% - 200%)
        #    - set every window's background opacity at once
        #    - set the tracking range in tiles
        #    - keep all three trackers the same size (resize one, the others follow)
        #    - unanchor every window
        #    - Magery buttons / Bandage button, a border on every window
        #    - choose whether combat bars only appear once you're actually fighting
        #    - reset everything to the defaults
        #
        #  Mouse
        #    - Click a bar while a spell/skill target cursor is up to target them.
        #    - Player bars: click = Last Target, double-click = attack.
        #    - Combat bars: click = attack.
        #    - A blue or green mobile while you are (or may be) in a guard zone: the
        #      attack waits for the same press again, later than a double-click's
        #      second click and within ATTACK_CONFIRM_SECONDS (the shard's R6).
        #    - Alt+click any bar (combat bars, player trackers or pop-outs) to
        #      auto-follow that mobile with TazUO's auto-follow. Alt+click the same
        #      one again to stop following.
        #    - Press ">" on a player row (or Shift+click the row) to pop that player
        #      out as their own small health bar window.
        #    - Press the tiny "N" on a player row to mark that person as an NPC: they
        #      go on the ignore list. Type the name and press "Unignore" to undo.
        #    - Closing the combat bars window just hides it; reopen it from the panel.
        #    - Untick Ultima Tracker on the Virtue Assistant Modules tab to turn it off.
        #
        #  FOE ALERT (2.6.05) - when a red player or one on your Foe list (and, by
        #  setting, orange or grey) comes into range, Virtue Assistant's alert banner
        #  shows the name, notoriety, distance and direction ("Killer: red, 7 tiles
        #  NE") with a sound you pick on Settings > Alerts ("Foe in range"; war drum
        #  at first). Once per player per N minutes (Settings page). A linked Foe
        #  entry is named with its group ("Bob (alt of Killer)").
        #
        #  SIGHTINGS (2.6.05) - every player who isn't a friend is logged once each
        #  time they turn up: name, notoriety, time, facet, where they stood and
        #  whether you were in a guard zone (the last SIGHT_CAP are kept, in the save
        #  file). The panel's "Sightings" button opens the log, newest first, with a
        #  name filter, a notoriety and a time filter and a count per name; a click
        #  on a row shows only that player, Alt+click follows them while in range.
        #  Each saved foe shows when and where it was last seen.
        #
        #  LINKED FOES (2.6.05) - one person, several characters: press "L" on one
        #  saved foe, then "L" on the other; the rows say "alt of <name>" and "U"
        #  unlinks.
        #
        #  ADD MY KILLER (2.6.05) - when you die, a small window lists the players who
        #  attacked you in the last KILLER_BACK seconds ("<name> is attacking you"
        #  lines and the combat bars), each with "Add to foes". It closes when you
        #  are resurrected or after KILLER_SHOW seconds.
        #
        #  Social's note on a player (when Social is on) shows in the rows' tooltips,
        #  and other modules can ask HOST.services["ultima.is_foe"](serial, name).
        #  (2.6.06) HOST.services["ultima.classify"](mobile or serial[, party]) tells
        #  them how the trackers see a mobile: None (not a player, or ignored) or
        #  (category, tag, notoriety), e.g. ("friend", "G", "ally") - Lookout uses it.
        #
        #  Everything is saved to "_ultima_tracker_data.txt" next to this script.
        #  On first run your Foe list, ignore list and layout are read from
        #  PlayerTracker's "_player_tracker_data.txt", and the Combat Bars window
        #  picks up the position/size CombatBars saved for this character.
        # =============================================================================

        # The part's name as the player reads it: the journal prefix of every line
        # here and the hub window's title (the module's own name: this part is its
        # heart). OWN_PREFIX: the attack reader skips the part's own lines by it.
        TITLE = "Ultima Tracker"
        OWN_PREFIX = TITLE + ":"

        # ------------------------------- SETTINGS ------------------------------------
        TICK_SECONDS             = 0.25   # how often player bars/lists refresh
        COMBAT_TICK_SECONDS      = 0.15   # how often the combat bars refresh
        POLL_SECONDS             = 0.05   # how often clicks are handled (keep small)
        DOUBLE_CLICK_SECONDS     = 0.45   # max gap between clicks of a double-click
        DOUBLE_CLICK_ACTION      = "attack"   # "attack" or "lasttarget"
        # (2.6.81) UT1-2, the shard's R6: an attack on a blue or green mobile while you are
        # (or may be) in a guard zone waits for a confirming press: the same press again
        # later than ATTACK_CONFIRM_MIN (so one habitual double-click doesn't confirm it)
        # and within ATTACK_CONFIRM_SECONDS of the first
        ATTACK_CONFIRM_SECONDS   = 3.0
        ATTACK_CONFIRM_MIN       = 0.6
        FOE_INCLUDE_WAR_ENEMIES  = True   # orange names (guild war / faction enemies)
        FOE_INCLUDE_CRIMINALS    = False  # gray names (criminals / attackable)
        SHOW_GHOSTS              = True   # keep dead players listed (shown as DEAD)
        AUTO_HIDE_NPCS           = True   # hide blue town NPCs (see is_npc)
        NPC_TITLE_RE = re.compile(r"\bthe\s+[a-z]", re.IGNORECASE)   # " the <job>" in the name
        NPC_RECHECK_SECONDS      = 3.0    # re-read names whose title hadn't arrived yet

        DEFAULT_SCALE   = 100   # percent
        DEFAULT_OPACITY = 85    # percent, window backgrounds
        DEFAULT_RANGE   = 18    # tiles
        DEFAULT_SYNC    = False # keep all three trackers the same size
        SCALE_MIN, SCALE_MAX = 50, 200
        RANGE_MIN, RANGE_MAX = 1, 24      # the client only knows mobiles it can see

        # Base (100%) sizes - multiplied by the Scale setting
        ROW_H      = 32    # height of one player row
        MIN_W      = 210
        MIN_H      = 90
        POP_W      = 200   # pop-out health bar width
        POP_BTN_W  = 18    # the ">" pop-out button on each row
        NPC_BTN_W  = 12    # the tiny "N" (mark as NPC / ignore) button on each row

        PAD        = 8     # inner padding
        SCROLLBAR  = 14    # room reserved for the scroll bar
        SAVE_EVERY = 8     # ticks between layout-change checks (8 * 0.25s = 2s)

        # ---------------------------- COMBAT BARS SETTINGS ---------------------------
        BASE_WIDTH     = 220     # combat window width that equals 100% scale
        BASE_ROW_H     = 16      # combat bar height at 100% scale
        BASE_FONT      = 11      # combat bar text size at 100% scale
        CB_MIN_WIDTH   = 170     # smallest combat window width (about 77% scale)
        CB_MAX_WIDTH   = 600     # largest combat window width (about 270% scale)
        CB_ROW_GAP     = 1       # gap between combat bars (0 = fully joined)
        CB_FOOTER_H    = 10      # bottom strip kept clear so the corners can be grabbed

        # Magery buttons: spell names passed to API.CastSpell (exact names match first)
        SPELL_POISON   = "Poison"
        SPELL_PARALYZE = "Paralyze"
        SPELL_HEAL, SPELL_GREATER_HEAL = "Heal", "Greater Heal"     # Friends: H button
        SPELL_CURE, SPELL_ARCH_CURE    = "Cure", "Arch Cure"        # Friends: C button
        CAST_TIMEOUT   = 5.0     # seconds to wait for the spell's target cursor

        COMBAT_RANGE   = 12      # war-mode hostiles inside this range get picked up
        MAX_RANGE      = 18      # anything farther than this is removed
        IDLE_TIMEOUT   = 20.0    # seconds without combat activity before removal
        MAX_BARS       = 12
        SORT_BY_DISTANCE = False # True = nearest at top (re-sorts often), False = order engaged

        AUTO_ADD_WARMODE_HOSTILES = True   # signal #3 above
        AUTO_ADD_LAST_TARGET      = True   # signal #2 above
        COMBAT_IGNORE_FRIENDS     = True   # never show TazUO friends-list or party members
        DEFAULT_COMBAT_ONLY       = True   # only add mobiles you're actually fighting
                                           # (toggle "Combat bars: only once fighting" on the Settings page)
        MELEE_RANGE               = 2      # a war-mode hostile this close counts as fighting you
        # Never shown: your pets, and blue/green/yellow notoriety (vendors, player
        # vendors, healers, town NPCs, guildmates). Only an "is attacking you" message
        # can add a blue or green mobile.
        NEVER_SHOW_NOTO           = ("invulnerable",)
        FRIENDLY_NOTO             = ("innocent", "ally")

        HOSTILE_NOTO = [API.Notoriety.Gray, API.Notoriety.Criminal,
                        API.Notoriety.Enemy, API.Notoriety.Murderer]

        # ---------------------- FOE ALERT, SIGHTINGS, DEATHS -------------------------
        ALERT_KEY        = "ultima.foe"    # the alert kind (Settings > Alerts: its sound, on / off)
        ALERT_SOUND      = 0x2E7           # default sound: the war drum (drum_battle.wav)
        ALERT_LEVEL      = "warn"          # "warn": the banner hides after a while; "alarm": it
        #                                    flashes until clicked
        DEFAULT_ALERT_MINUTES = 5          # the same player is alerted again after this long
        ALERT_MIN, ALERT_MAX = 1, 60       # minutes (the Settings page slider)
        SIGHT_CAP        = 2000            # sightings kept in the log (the oldest go first)
        SIGHT_SLACK      = 200             # the log is cut back to SIGHT_CAP past CAP + SLACK lines
        SIGHT_GONE       = 60.0            # s out of range before a player's return is a new sighting
        SIGHT_SAVE_SECONDS = 30.0          # a new sighting reaches the save file within this long
        SIGHT_ROWS       = 12              # rows on one page of the Sightings window
        SIGHT_REFRESH    = 30.0            # s between redraws of an unchanged list (times, cut-offs)
        SIGHT_TRAY_ICON  = 0x14F5          # spyglass: the Sightings window's Action Bar tray icon
        KILLER_BACK      = 60.0            # s: who attacked you this recently is listed when you die
        KILLER_SHOW      = 60.0            # s the death window stays up (it closes on resurrection too)
        KILLER_ROWS      = 6               # most attackers listed in it
        ATTACKERS_CAP    = 40              # attackers remembered (older than KILLER_BACK are dropped)
        SEEN_REFRESH     = 30.0            # s between updates of the Foe list's "seen ... ago" lines
        NOTE_MAX         = 160             # characters of a Social note shown in a tooltip
        FACETS = {0: "Fel", 1: "Tram", 2: "Ilsh", 3: "Malas", 4: "Tok", 5: "TerM"}
        NOTO_WORD = {"murderer": "red", "criminal": "grey", "gray": "grey", "enemy": "orange",
                     "innocent": "blue", "ally": "green", "invulnerable": "yellow"}
        NOTO_HUE = {"murderer": 0x0022, "criminal": 0x03B2, "gray": 0x03B2, "enemy": 0x0090,
                    "innocent": 0x0059, "ally": 0x003F, "invulnerable": 0x0035}
        # the Sightings window's filters: (caption, notoriety names; "foe" = on your Foe list)
        SIGHT_NOTO_FILTERS = (("All players", None), ("Red only", ("murderer",)),
                              ("Grey only", ("gray", "criminal")), ("Orange only", ("enemy",)),
                              ("Blue only", ("innocent",)), ("Foe list", "foe"))
        SIGHT_TIME_FILTERS = (("Last hour", 3600.0), ("Today", "today"), ("All time", None))
        SIGHT_POS_KEY    = "UltimaTracker_sight_pos"    # where the Sightings window sits
        SIGHT_MIN_KEY    = "UltimaTracker_sight_min"    # it was minimized
        SIGHT_OPEN_KEY   = "UltimaTracker_sight_open"   # it was open when the module stopped
        KILLER_POS_KEY   = "UltimaTracker_killer_pos"   # the death window
        KILLER_MIN_KEY   = "UltimaTracker_killer_min"

        TITLE_DBL_SECONDS = 0.5   # max gap between the two clicks of a title double-click
        TITLE_JITTER   = 6       # px the window may shift between those clicks (a click
                                 # on the draggable title strip can nudge it a little)
        # px: drop a window this close to another to anchor them (the host's SNAP_DIST, the
        # same distance every window of every module snaps at)
        SNAP_DISTANCE  = globals().get("SNAP_DIST", 16)
        FIXED_WINDOWS  = ("friend", "foe", "neutral", "combat", "panel")   # saved groups
        ANCHOR_SETTLE_POLLS = 4   # polls a dragged window must stand still before it snaps
        ANCHOR_LINGER  = 0.5      # seconds the windows are still watched after a drag ended
                                  # (the host's own snap may still nudge the dropped window)
        ANCHOR_LINGER_POLLS = max(1, int(round(ANCHOR_LINGER / POLL_SECONDS)))

        # Caches of things seen this session (one entry per mobile clicked / seen / per
        # window): emptied past this many entries, like every other cache here.
        CACHE_CAP      = 2000
        # (2.6.81) UT1-5: the saved confirmed players (one name per player ever single-
        # clicked) fold to PLAYER_NAMES_KEEP past PLAYER_NAMES_CAP; a dropped name is
        # learned again on the next single-click of that player
        PLAYER_NAMES_CAP  = 5000
        PLAYER_NAMES_KEEP = 4000
        LABELS_CAP     = 4000     # UO-font label notes kept before disposed ones are swept
        MOBS_EVERY     = 0.1      # seconds between reads of the mobiles around you
        PAGE_SAVE_DELAY = 1.0     # seconds a Settings-page change waits before the file is
                                  # written (with the module off; one write per burst of changes)

        # ------------------------------- STYLE ---------------------------------------
        # One look for every window.
        BG_COLOR     = "#141414"   # window background (faded by the opacity setting)
        BORDER_COLOR = "#7D6E52"   # window border (always solid)
        BORDER       = 2           # border thickness in pixels
        TITLE_BG     = "#2B2B2B"   # title strip (fades with the background)
        TITLE_H      = 24          # title strip height at 100% scale (stone divider included)
        TITLE_FONT   = 13          # title text size at 100% scale
        OPACITY_ROW_H = 20         # fold-out opacity slider row at 100% scale
        BTN_FACE     = "#3A3A3A"   # button face
        BTN_FACE_ON  = "#5E4E24"   # button face while switched on (locked / slider open)
        ICON_COLOR   = "#DDDDDD"
        LOCK_ON      = "#F0C850"   # closed padlock
        LOCK_OFF     = "#A8A8A8"   # open padlock
        TEXT_COLOR   = "#DDDDDD"
        DIM_TEXT     = "#999999"
        GRIP_COLOR   = "#7D6E52"

        TITLES = {"friend": "Friends", "foe": "Foes", "neutral": "Neutral"}
        TITLE_COLOR = {"friend": "#5CE65C", "foe": "#FF5050", "neutral": "#9EC8FF",
                       "combat": "#FFB050", "panel": "#FFD966"}

        BAR_FG = {"friend": "#3AA0D4", "foe": "#D93030", "neutral": "#B8B8B8",
                  "combat": "#B32D2D"}
        COL_POISON = "#2E9E3A"
        GLOW_COLOR = "#FF2020"   # Friends: pulsing glow when they need healing
        GLOW_HP_PCT = 50         # glow at or below this HP %
        GLOW_PERIOD = 1.2        # seconds per pulse
        GLOW_MIN, GLOW_MAX = 0.10, 0.55
        GLOW_STEPS = 32          # the glow's alpha moves in steps of 1/32: a handful of
                                 # alpha writes a second per row instead of one every poll
        GLOW_EVERY = 0.1         # (2.6.82) seconds between glow updates (10 steps a second)
        COL_HEAL   = "#B8902A"   # H (Heal / Greater Heal) button
        COL_CURE   = "#2A8C9E"   # C (Cure / Arch Cure) button
        COL_BANDAGE = "#D8CCB0"  # B (bandage) button

        # Friends: B button = bandage them when in reach; farther away it only follows them
        # (2.6.81: one press = one action, the shard's R1; no walk-then-bandage, no speech)
        BANDAGE_GRAPHIC   = 0x0E21   # clean bandages
        BANDAGE_RANGE     = 1        # tiles; raise to 2 if the shard allows it
        BANDAGE_CURSOR_WAIT = 3.0    # seconds the bandage's target cursor may take to show
        BANDAGE_CLAIM     = 3.5      # seconds the shared cursor is claimed for that bandage
        COL_PARA   = "#3A6FD8"
        COL_BOTH   = "#21A39A"
        COL_DEAD   = "#555555"

        # Name colors follow UO notoriety hues
        NOTO_COLOR = {
            "innocent": "#4FA3FF", "ally": "#40E040", "gray": "#B0B0B0",
            "criminal": "#B0B0B0", "enemy": "#FF9A2E", "murderer": "#FF4040",
            "invulnerable": "#FFE14D", "unknown": "#DDDDDD",
        }

        # ----------------------------- NATIVE UO LOOK --------------------------------
        # Windows are drawn with the client's own gump art and the UO font. If a piece
        # of art can't be loaded, that part falls back to the flat style above.
        NATIVE_STYLE  = True       # False = the flat style above everywhere
        UO_FONT       = True       # UO font for text; text drawn over a bar keeps an
                                   # outlined font so it stays readable
        UO_FONT_MIN, UO_FONT_MAX = 10, 18   # text sizes (after Scale) that use the UO font;
                                            # smaller / larger text falls back to the smooth font
        FRAME_GUMP    = Kit.WINDOW_BG   # 9-piece window background: the stone frame of the
                                   # crafting gump (shared with every module)
        FRAME_RIM     = 6          # px of the frame art's outer stone rim to draw
        SECTION_GUMP  = Kit.SECTION_TILE   # black inside of every window (fades with opacity)
        HEADER_GUMP   = Kit.SECTION_TILE   # title strip tile; 0 = plain dark strip
        DIVIDER_H     = 3          # stone strip under the title
        BUTTON_GUMP   = Kit.STONE_TILE     # button face tile (stone, hued for coloured buttons)
        LOCK_GUMP     = 0x082C     # the client's padlock: red while locked, as when you
                                   # Alt-lock one of the client's own bars
        LOCK_OFF_ALPHA = 0.6       # the unlocked padlock is drawn this dim
        MIN_GUMPS     = (Kit.ART_MIN[0], Kit.ART_RESTORE[0])   # minimize / restore arrows
        OPACITY_GUMPS = (0x0837, 0x0838)   # opacity slider closed / open (small gem button)
        LINE_RED, LINE_BLUE    = 0x0805, 0x0806   # the classic health bar lines
        LINE_POISON = 0x0808

        # UO hues (the same numbers the client uses)
        HUE_TEXT     = 0x0481      # white text
        HUE_LOCKED   = 34          # red padlock
        HUE_PARA_BAR = 0x0480      # paralyzed: pale / frozen
        FACE_HUE = {BTN_FACE: 0, BTN_FACE_ON: 0x0035, COL_HEAL: 0x0035, COL_CURE: 0x0059,
                    COL_BANDAGE: 0, COL_POISON: 0x003F, COL_PARA: HUE_PARA_BAR}
        # closest UO hue for a color used in the flat style: (r, g, b) -> hue
        HUE_PALETTE = [((235, 235, 235), 0x0481), ((150, 150, 150), 0x03B2),
                       ((225, 55, 55), 0x0022), ((70, 220, 70), 0x003F),
                       ((90, 150, 255), 0x0059), ((255, 155, 45), 0x0090),
                       ((255, 220, 80), 0x0035), ((25, 25, 25), 0)]

        DATA_FILE = os.path.join(API.ScriptPath, "_ultima_tracker_data.txt")
        OLD_DATA_FILE = os.path.join(API.ScriptPath, "_player_tracker_data.txt")

        CATS = ["friend", "foe", "neutral"]
        # saved settings: numbers -> (min, max), and the on / off ones (in save-file order)
        INT_SETTINGS = {"scale": (SCALE_MIN, SCALE_MAX), "opacity": (0, 100),
                        "range": (RANGE_MIN, RANGE_MAX),
                        "alert_minutes": (ALERT_MIN, ALERT_MAX)}           # (2.6.05)
        INT_ORDER = ("scale", "opacity", "range", "alert_minutes")         # in save-file order
        #  (2.6.05 added the ones after "borders": 2.6.04 skips keys it doesn't know)
        BOOL_SETTINGS = ("sync", "magery", "combat_shown", "combat_only", "healing", "borders",
                         "alert_red", "alert_foes", "alert_orange", "alert_gray", "sightings",
                         "killer", "say_attackers")

        # x, y, w, h, locked, minimized, opacity
        #   panel uses x, y, locked, minimized, opacity
        #   combat uses x, y, w (= scale), locked, minimized, opacity
        DEFAULT_LAYOUT = {
            "friend":  [40, 140, 240, 220, False, False, DEFAULT_OPACITY],
            "foe":     [290, 140, 240, 220, False, False, DEFAULT_OPACITY],
            "neutral": [540, 140, 240, 220, False, False, DEFAULT_OPACITY],
            "combat":  [300, 200, BASE_WIDTH, 0, False, False, DEFAULT_OPACITY],
            "panel":   [40, 380, 0, 0, False, False, DEFAULT_OPACITY],
        }

        # ------------------------------- STATE ---------------------------------------
        FOES = {}      # name key -> name as typed
        IGNORE = {}    # lowercase name -> name as typed
        LAYOUT = {k: list(v) for k, v in DEFAULT_LAYOUT.items()}
        UI_DEFAULTS = {"scale": DEFAULT_SCALE, "opacity": DEFAULT_OPACITY, "range": DEFAULT_RANGE,
                       "sync": DEFAULT_SYNC, "magery": False, "combat_shown": True,
                       "combat_only": DEFAULT_COMBAT_ONLY, "healing": False, "borders": True,
                       # foe alert: which notorieties count, and how often the same player
                       "alert_red": True, "alert_foes": True, "alert_orange": False,
                       "alert_gray": False, "alert_minutes": DEFAULT_ALERT_MINUTES,
                       "sightings": True,          # log players who come into range
                       "killer": True,             # on death: list who attacked you
                       "say_attackers": False}     # debug: the attack lines seen, in the journal
        UI = dict(UI_DEFAULTS)
        STATE_DEFAULTS = {"dirty_save": False, "foe_ver": 0, "combat_loaded": False,
                          "shutting": False,
                          "started": False,    # the module is on (its windows may still be on their way)
                          "loaded": False}     # the save file was read (by the load job): build the windows
        STATE = dict(STATE_DEFAULTS, party=set())
        POPS = {}        # serial -> PopBar (pop-out health bars)
        DOCK_REQ = []    # dock keys whose gold Fold into the Action Bar arrow was clicked
        SETTINGS_REQ = []   # (2.6.72) a window's Settings button was clicked
        KIT_HEAD = Kit.MARGIN + 30 + Kit.GAP   # (2.6.72) a Kit-look window's content starts here
        KIT_MINI_H = 2 * Kit.MARGIN + 30       # (2.6.72) its minimized height


        def settings_click(*args):
            SETTINGS_REQ.append(True)
        #                  (handled on the next tick: a click only records)
        LAST_CLICK = {}  # serial -> time of last single click (double-click detection)
        NATIVE = {}      # gump art / UO font that loaded (see init_native_art)
        # (2.6.05) saved with the lists (new sections of the save file, which 2.6.04 skips):
        SIGHTS = []      # the sightings log, oldest first (see log_sighting): SIGHT_CAP at most
        LAST_SEEN = {}   # name key -> (time, facet, x, y, guarded): the last sighting of that name
        ALT_OF = {}      # Foe list name key -> the name key of the entry it's an alt of (links)
        SIGHT = {"ver": 0,           # bumped for every sighting logged (windows redraw)
                 "seen_ver": 0,      # bumped when a Foe list name's last sighting changed
                 "dirty": False,     # sightings not written to the file yet
                 "save_at": 0.0}     # ... and when they are due to be
        # this session only; the first three are kept while the module is off and on
        # again, so a restart neither alerts again nor logs again the players around:
        PRESENT = {}     # serial -> time last seen in range (players who aren't friends)
        ALERTED = {}     # serial -> time of the last foe alert about them
        FOE_SERIALS = {}     # serial -> the Foe list name key it was seen under
        ALERT_PREV = set()   # serials that counted for the alert in the last scan
        ATTACKERS = {}       # lower-case name -> [name, time, serial or None]: who attacked you
        LINK_PICK = [None]   # Foe list name key whose "L" was pressed first (Link, step 1)


        def sc(v, scale=None):
            """Scale a base pixel/font size by the current (or given) Scale %."""
            s = UI["scale"] if scale is None else scale
            return max(1, int(round(v * s / 100.0)))


        # (2.6.74) E12: text is never drawn under the font's own size. Below 100%
        # the rows (heights, bar widths, spacing) still scale, but a label keeps
        # its size at 100% (sizes under it fell out of the UO font into a tiny smooth
        # font, unreadable in a small zone); text that doesn't fit is cut instead.
        TEXT_FIT_MAX = 13            # a smooth font up to this size is cut as the UO font
        EMPTY_PITCH = 20             # px from one line of an empty-state text to the next


        def text_scale(s):
            """(2.6.74) The scale (1.0 = 100%) text is drawn at: s, never under 1.0."""
            return s if s > 1.0 else 1.0


        def tsc(v):
            """(2.6.74) sc() for a font size: scaled up with the Scale %, never down."""
            return sc(v) if UI["scale"] > 100 else int(v)


        def empty_lines(text, width):
            """(2.6.74) E12: an empty-state sentence as lines no wider than width px
            in the label font (Kit.wrap; a word longer than a line is cut). Only
            when a window is built."""
            width = max(20, int(width))
            return [Kit.fit(ln, width) for ln in Kit.wrap(text, width)]


        def add_empty(parent, lines, x, y):
            """(2.6.74) The empty-state lines as grey label-font text, EMPTY_PITCH px
            apart, from (x, y) in parent. Returns the labels (they let clicks
            through)."""
            out = []
            hue = hue_of(DIM_TEXT)
            for i, ln in enumerate(lines):
                lb = inert(Kit.add_label(parent, ln, x, y + i * EMPTY_PITCH, hue))
                out.append(lb)
            return out


        # (2.6.55) the zone fit: while a group window sits in a zone of the layout
        # whose fit is on, UI["scale"] is overridden so the window fills the zone;
        # the player's own Scale % is kept in FIT["own"] (saved, shown on the slider)
        # and put back when every fitted group is freed. "want": group -> the
        # scale its zone asks for; the smallest wins, so every group fits its zone.
        FIT = {"own": None, "want": {}, "req": False, "size": {}, "own_size": {},
               "force": set(),           # (2.6.69) groups the layout says aren't their slot's size
               "made": {}}               # (2.6.69) cat -> (slot, rebuilds for it in a row)
        FIT_TRIES = 3                     # (2.6.69) rebuilds for one slot before the layout's word
        FIT_MIN, FIT_MAX = 50, 150            # how far the fit may scale, percent


        def own_scale():
            """The player's own Scale % (UI["scale"] unless the zone fit overrides it)."""
            return UI["scale"] if FIT["own"] is None else FIT["own"]


        def reset_layout():
            for k, v in DEFAULT_LAYOUT.items():
                LAYOUT[k] = list(v)


        def reset_settings():
            """Reset to defaults: anchors, every value of the Settings page (the
            options too: Magery, Healing, Combat Bars shown) and the layout."""
            ANCHORS.clear()
            UI.update(UI_DEFAULTS)
            FIT["own"] = None                     # (the zone fit starts again from the default)
            FIT["req"] = bool(FIT["want"])
            BANDAGE["serial"] = None              # (Healing is off again)
            reset_layout()


        def clamp(v, lo, hi):
            return max(lo, min(hi, v))


        def stopping():
            try:
                return bool(API.StopRequested)
            except Exception:
                return True


        # ------------------------------- HELPERS -------------------------------------
        TITLE_PREFIXES = ("lord ", "lady ")


        def name_key(name):
            n = (name or "").strip().lower()
            for p in TITLE_PREFIXES:
                if n.startswith(p):
                    n = n[len(p):]
            return n


        NOTO_NAMES = {}      # the client's Notoriety value -> "innocent", "murderer", ...


        def noto_name(mob):
            try:
                v = mob.Notoriety
            except Exception:
                return "unknown"
            return noto_of(v)


        def noto_of(v):
            """(2.6.82) noto_name for a Notoriety value already read."""
            try:
                return NOTO_NAMES[v]
            except KeyError:
                pass
            except Exception:                    # not hashable: work it out every time
                return str(v).split(".")[-1].lower()
            n = NOTO_NAMES[v] = str(v).split(".")[-1].lower()
            return n


        def short(text, n):
            return text if len(text) <= n else text[:max(1, n - 2)] + ".."


        def inert(c):
            """A control that lets clicks through to what's under it."""
            try:
                c.SetAcceptMouseInput(False)
            except Exception:
                pass
            return c


        def ttf(text, size, color, **kw):
            return inert(API.Gumps.CreateGumpTTFLabel(text, size, color, **kw))


        def box(opacity, color):
            return inert(API.Gumps.CreateGumpColorBox(opacity, color))


        ALPHA_OK = [True]    # (2.6.82) colour boxes take .Alpha on this client (else SetAlpha)


        def set_box_alpha(b, a):
            if ALPHA_OK[0]:
                try:
                    b.Alpha = a
                    return
                except AttributeError:            # no .Alpha on this build: SetAlpha from now on
                    if b is not None:
                        ALPHA_OK[0] = False
                except Exception:
                    pass
            try:
                b.SetAlpha(a)
            except Exception:
                pass


        VIS_OK = [True]      # child controls can be hidden (IsVisible) on this client


        def set_vis(c, on):
            """Show / hide one control of a pooled row. False when this client
            can't hide child controls (the row is then disposed instead)."""
            if not VIS_OK[0]:
                return False
            try:
                c.IsVisible = bool(on)
                return True
            except Exception:
                VIS_OK[0] = False
                return False


        def drop(c):
            """Dispose a control (and forget the UO-font bookkeeping of a label)."""
            if c is None:
                return
            LABELS.pop(id(c), None)
            try:
                c.Dispose()
            except Exception:
                pass


        CLICK_Q = []       # clicks waiting for the next tick: (handler, modifiers held at the click)
        CLICK_GRACE = 0.15 # s: a pooled row that changed hands this recently still acts for the old one
        CLICK_MODS = {}    # "alt" / "shift": True when held at the click being handled now


        class RowClick(object):
            """The click handler of a pooled row (its controls are reused for
            whoever is listed at its place): who the click is for is read at the
            moment of the click, make(serial, name) gives the handler."""
            __slots__ = ("row", "make")

            def __init__(self, row, make):
                self.row, self.make = row, make

            def bind(self):
                # A click handler runs a pass after the click, and the tick in
                # between may have given the row to someone else (a mob died, the
                # list moved up): a change that recent is newer than the click, so
                # the click is for whoever the row showed before it.
                r = self.row
                serial, name = r.serial, r.name
                prev = getattr(r, "prev", None)
                if prev is not None and time.time() - prev[2] < CLICK_GRACE:
                    serial, name = prev[0], prev[1]
                if serial is None:
                    return None
                return self.make(serial, name)


        def mods_now():
            mods = {}
            for which in ("alt", "shift"):
                for r in MOD_READERS[which]:
                    try:
                        if r():
                            mods[which] = True
                            break
                    except Exception:
                        pass
            return mods


        def queue_click(fn):
            """A click handler that only records the click (with the modifiers held
            at that moment); fn itself runs on the next tick. CLICK_Q is written
            from click handlers only (see TICK_JOBS for the other way in)."""
            def queued(*args):
                f = fn.bind() if type(fn) is RowClick else fn
                if f is not None:
                    CLICK_Q.append((f, mods_now()))
            return queued


        def on_click(c, fn):
            """Kit.on_click (gets the second click of a double-click too), but the
            work is done by the next tick: that runs on the client thread, where
            the handler's calls (new windows, mobile lookups, targets) don't wait,
            while a click handler runs on the script's thread, where every one
            waits a frame. Alt / Shift are read at click time (and so is the
            player a pooled row shows, see RowClick)."""
            Kit.on_click(c, queue_click(fn))


        def run_clicks():
            """The clicks since the last tick, in order (on the client thread)."""
            while CLICK_Q:
                fn, mods = CLICK_Q.pop(0)
                CLICK_MODS.clear()
                CLICK_MODS.update(mods)
                try:
                    fn()
                except Exception as ex:
                    if stopping() or HOST.stopping():
                        return
                    report_error(ex)
                finally:
                    CLICK_MODS.clear()


        def report_error(ex):
            """Report each distinct error once and keep running."""
            msg = str(ex)
            if msg not in M["errors"]:
                M["errors"].add(msg)
                safe(lambda: API.SysMsg(TITLE + ": error (still running): " + msg, Kit.HUE_BAD))


        # ------------------------- work off the client thread -------------------------
        # The tick runs on the client thread, where nothing may wait and a file
        # write is a frame hitch. Such work is queued here and done by
        # thread_tick, on the script's own thread, right after the tick.
        SAVE_REQ = [False]   # the save file should be written
        THREAD_JOBS = []     # functions to run on the script's thread
        TICK_JOBS = []       # functions a thread job hands back to the next tick (they run on
        #                      the client thread like a click, but are not clicks: CLICK_Q
        #                      stays the clicks' own list)


        def run_tick_jobs():
            while TICK_JOBS:
                fn = TICK_JOBS.pop(0)
                try:
                    fn()
                except Exception as ex:
                    if stopping() or HOST.stopping():
                        return
                    report_error(ex)


        def request_save():
            """Write the save file off the client thread: by thread_tick while the
            module runs, else (the Settings page with the module off) on a short
            thread of its own."""
            if M["windows"] is not None and not STATE.get("shutting"):
                SAVE_REQ[0] = True
            else:
                save_data(background=True)


        def catcher(x, y, w, h, fn, tip=None):
            """Invisible click target."""
            c = API.Gumps.CreateGumpColorBox(0.01, "#000000")
            c.SetRect(x, y, w, h)
            on_click(c, fn)
            if tip:
                safe(lambda: c.SetTooltip(tip))
            return c


        # ------------------------------- NATIVE ART ----------------------------------
        ART_SIZES = {}   # gump graphic -> (w, h), or None when the client lacks it


        def art_size(graphic):
            """Size of a gump art piece, or None if it can't be loaded."""
            if graphic not in ART_SIZES:
                size = None
                if graphic:
                    try:
                        p = API.Gumps.CreateGumpPic(graphic)
                        w, h = int(p.GetWidth()), int(p.GetHeight())
                        safe(lambda: p.Dispose())
                        if w > 0 and h > 0:
                            size = (w, h)
                    except Exception:
                        pass
                ART_SIZES[graphic] = size
            return ART_SIZES[graphic]


        def pic(graphic, x=0, y=0, hue=0):
            return inert(API.Gumps.CreateGumpPic(graphic, x, y, hue))


        def tiled(graphic, w, h, hue=0):
            return inert(API.Gumps.CreateTiledGumpPic(graphic, max(0, w), max(0, h), hue))


        def init_native_art():
            """Work out which pieces of the client's art can be used. Anything that
            fails to load keeps the flat style. Run once, before any window opens."""
            nonlocal BORDER
            NATIVE.clear()
            if not NATIVE_STYLE:
                return
            try:
                t = tiled(FRAME_GUMP + 4, 4, 4)       # older TazUO builds lack tiled pics
                safe(lambda: t.Dispose())
                can_tile = True
            except Exception:
                can_tile = False
            parts = [art_size(FRAME_GUMP + i) for i in range(9)]
            if can_tile and all(parts):
                NATIVE["frame"] = parts
                # content starts inside the frame's edge
                BORDER = int(clamp(min(FRAME_RIM, parts[3][0], parts[1][1]), 2, 12))
            if can_tile and HEADER_GUMP and art_size(HEADER_GUMP):
                NATIVE["header"] = HEADER_GUMP
            if can_tile and art_size(BUTTON_GUMP):
                NATIVE["button"] = BUTTON_GUMP
            lines = [art_size(g) for g in (LINE_RED, LINE_BLUE, LINE_POISON)]
            if can_tile and all(lines):
                NATIVE["bar_h"] = min(l[1] for l in lines)
            icons = {}
            for kind, graphics in (("lock", (LOCK_GUMP, LOCK_GUMP)), ("min", MIN_GUMPS),
                                   ("dock", (Kit.ART_DOCK[0], Kit.ART_DOCK[0])),
                                   ("opacity", OPACITY_GUMPS)):
                sizes = [art_size(g) for g in graphics]
                if all(sizes):
                    icons[kind] = list(zip(graphics, sizes))
            NATIVE["icons"] = icons
            if UO_FONT:
                try:
                    sample = "Name the 75% PSN 12y Foes (3)"
                    lb = API.Gumps.CreateGumpLabel(sample, HUE_TEXT)
                    w, h = int(lb.GetWidth()), int(lb.GetHeight())
                    safe(lambda: lb.Dispose())
                    if w > 0 and h > 0:
                        NATIVE["char_w"] = w / float(len(sample))
                        NATIVE["font_h"] = h
                except Exception:
                    pass


        HUES = {}            # #RRGGBB -> closest UO hue (worked out once per color)


        def hue_of(color):
            """Closest UO hue to a #RRGGBB color."""
            h = HUES.get(color)
            if h is not None:
                return h
            try:
                c = color.lstrip("#")
                r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
            except Exception:
                return HUE_TEXT
            best, bd = HUE_TEXT, None
            for (pr, pg, pb), hue in HUE_PALETTE:
                d = (pr - r) ** 2 + (pg - g) ** 2 + (pb - b) ** 2
                if bd is None or d < bd:
                    best, bd = hue, d
            if len(HUES) < 256:
                HUES[color] = best
            return best


        RGBS = {}            # #RRGGBB -> (r, g, b)


        def rgb_of(color):
            v = RGBS.get(color)
            if v is None:
                c = color.lstrip("#")
                v = RGBS[color] = (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))
            return v


        def uo_font_for(size):
            return "char_w" in NATIVE and UO_FONT_MIN <= size <= UO_FONT_MAX


        def char_w(size):
            """Average character width of text at this size (for trimming names)."""
            return NATIVE["char_w"] if uo_font_for(size) else size * 0.58


        LABELS = {}      # id(label) -> [label, aligned, maxWidth, size, x, y, text] (UO font)
        LABELS_SWEEP = [LABELS_CAP]   # (2.6.82) LABELS is swept past this many entries


        def label(text, size, color, aligned="left", maxWidth=0, applyStroke=False):
            """Text in the UO font with a UO hue (or the smooth font when the size is
            out of the UO font's range, or the text sits on top of a bar). Position
            it with place() and change it with set_text() / set_hue()."""
            if applyStroke or not uo_font_for(size):
                lb = ttf(text, size, color, aligned=aligned, maxWidth=maxWidth,
                         applyStroke=applyStroke)
                LABELS.pop(id(lb), None)
                return lb
            if len(LABELS) > LABELS_SWEEP[0]:        # forget labels that were disposed
                for k, v in list(LABELS.items()):
                    try:
                        gone = v[0].IsDisposed
                    except Exception:
                        gone = True
                    if gone:
                        del LABELS[k]
                # (2.6.82) the next sweep only once as many again have been made
                LABELS_SWEEP[0] = max(LABELS_CAP, 2 * len(LABELS))
            text = fit_text(text, maxWidth)
            lb = inert(API.Gumps.CreateGumpLabel(text, hue_of(color)))
            LABELS[id(lb)] = [lb, aligned, maxWidth, size, 0, 0, text]
            return lb


        def _uo_meta(lb):
            m = LABELS.get(id(lb))
            return m if m is not None and m[0] is lb else None


        def fit_text(text, maxw):
            if maxw and len(text) * NATIVE.get("char_w", 7) > maxw:
                return short(text, max(2, int(maxw / NATIVE.get("char_w", 7))))
            return text


        def place(lb, x, y, text=None):
            """SetPos for any label. `y` is worked out for the smooth font of the
            label's size (text_y); UO font labels are re-centered on that line and
            right / center aligned inside their maxWidth (their text is known
            here, nothing is read back from the client)."""
            m = _uo_meta(lb)
            if m is None:
                lb.SetPos(x, y)
                return
            m[4], m[5] = x, y
            aligned, maxw, size = m[1], m[2], m[3]
            if text is None:
                text = m[6]
            tw = int(len(text) * NATIVE["char_w"])
            dx = 0
            if maxw and aligned == "right":
                dx = max(0, maxw - tw)
            elif maxw and aligned == "center":
                dx = max(0, (maxw - tw) // 2)
            dy = int(round((size * 1.35 - NATIVE["font_h"]) / 2.0))
            lb.SetPos(int(x + dx), int(y + dy))


        def set_text(lb, text):
            m = _uo_meta(lb)
            if m is None:
                try:
                    lb.SetText(text)
                except Exception:
                    pass
                return
            text = fit_text(text, m[2])
            if text == m[6]:
                return
            m[6] = text
            try:
                lb.Text = text
            except Exception:
                pass
            if m[1] != "left" and m[2]:
                place(lb, m[4], m[5], text)


        def set_hue(lb, color):
            """Recolor a UO-font label in place. False for a smooth-font label (its
            color is fixed when it's made: the caller makes a new one)."""
            if _uo_meta(lb) is None:
                return False
            try:
                lb.Hue = hue_of(color)
                return True
            except Exception:
                return False


        SHIFT_NAMES = ["SHIFT", "LSHIFT", "RSHIFT", "LEFTSHIFT", "RIGHTSHIFT"]
        ALT_NAMES = ["ALT", "LALT", "RALT", "LEFTALT", "RIGHTALT", "MENU", "LMENU", "RMENU"]


        def key_held(names):
            return any(safe(lambda: API.IsKeyPressed(k), False) for k in names)


        MOD_READERS = {"alt": [], "shift": []}   # read modifiers straight from the client
        MOD_MASKS = {"alt": 0x0300, "shift": 0x0003}   # SDL KMOD_ALT / KMOD_SHIFT


        def find_mod_readers():
            """API.IsKeyPressed wants a key combination ("CTRL+F1"), so a bare Alt or
            Shift can't be asked for reliably. Read the modifier state from the
            client instead: ClassicUO's Keyboard.Alt/Shift, or SDL's modifier flags."""
            try:
                import clr
                for asm in ("ClassicUO", "ClassicUO.Client", "TazUO", "FNA", "SDL2-CS", "SDL3-CS"):
                    safe(lambda: clr.AddReference(asm))
            except Exception:
                pass
            Client.find()                     # the client's own Alt / Shift, by reflection
            for which in ("alt", "shift"):
                if which in Client.keys:
                    MOD_READERS[which].append((lambda w: lambda: Client.key_held(w))(which))
            try:
                from ClassicUO.Input import Keyboard
                bool(Keyboard.Alt)
                bool(Keyboard.Shift)
                MOD_READERS["alt"].append(lambda: bool(Keyboard.Alt))
                MOD_READERS["shift"].append(lambda: bool(Keyboard.Shift))
            except Exception:
                pass
            for modname in ("SDL2", "SDL3"):
                try:
                    sdl = __import__(modname).SDL
                    int(sdl.SDL_GetModState())
                    for which, mask in MOD_MASKS.items():
                        MOD_READERS[which].append(
                            lambda sdl=sdl, mask=mask: (int(sdl.SDL_GetModState()) & mask) != 0)
                except Exception:
                    pass
            return len(MOD_READERS["alt"])


        def mod_held(which, names):
            if CLICK_MODS.get(which):                  # held at the click being handled
                return True
            readers = MOD_READERS[which]
            if readers:
                # (2.6.82) a reader exists and says up: believe it (as the mother's
                # Follow.alt_held does); IsKeyPressed only on builds with no reader
                for r in readers:
                    try:
                        if r():
                            return True
                    except Exception:
                        pass
                return False
            return key_held(names)


        def shift_held():
            return mod_held("shift", SHIFT_NAMES)


        def alt_held():
            return mod_held("alt", ALT_NAMES)


        def layout_rect(key):
            """(2.6.69) (x, y, w, h) of window `key`'s slot in its zone, or None
            (free, not placed yet, or an older Virtue Assistant)."""
            fn = getattr(HOST, "layout_rect", None)
            if fn is None:
                return None
            try:
                return fn(key)
            except Exception:
                return None


        def layout_held_keys():
            """The group windows slotted in a zone of the layout (2.6.54): the
            layout places them, so a move of one is never a drag of its group."""
            fn = getattr(HOST, "layout_holds", None)
            if fn is None:
                return ()
            out = []
            for c in CATS + ["combat"]:          # (2.6.58) the Combat window too: it was
                try:                             # left out, so each zone move of it read as a
                    if fn("ultima." + c):        # drag that shifted its group, which the zone
                        out.append(c)            # moved back: the windows see-sawed, then
                except Exception:                # bunched up
                    pass
            try:                                 # (2.6.74) the shared hub window too (its
                if fn("hub"):                    # layout key is the hub's own)
                    out.append("panel")
            except Exception:
                pass
            return out


        def layout_arranging():
            """(2.6.74) Is the layout's Arrange mode on? (False on an older mother.)
            While it is, the anchors stand down: the drop decides where a window goes."""
            fn = getattr(HOST, "layout_arranging", None)
            if fn is None:
                return False
            try:
                return bool(fn())
            except Exception:
                return False


        def drag_on():
            """(2.6.74) A window is being dragged, or the left button is held: no
            window of ours is rebuilt or put on a new place now (a window made anew
            under the mouse is a new gump, so the drop of the old one is lost).
            The work is kept and done on a tick after the drag. Ask it only when
            there is work waiting (SNAP.pressed() asks the client)."""
            try:
                if SNAP.drag:
                    return True
            except Exception:
                pass
            try:
                return SNAP.pressed() is True
            except Exception:
                return False


        CUT_CACHE = {}       # (2.6.74) (text, px) -> the text cut to px (cut_text)
        CUT_CACHE_CAP = 2000


        def cut_text(text, px, size, smooth=False):
            """(2.6.74) E12: text of font size `size` that would not fit in px
            pixels is cut (Kit.fit, in the client's label font), never drawn
            smaller. smooth: the label is the smooth font whatever its size (text
            on a bar). A smooth font larger than the UO font (a big Scale %) keeps
            the old letter-count estimate. The cut of a text is worked out once
            (a row's name is asked every scan)."""
            if size > TEXT_FIT_MAX and (smooth or not uo_font_for(size)):
                cw = size * 0.6 if smooth else char_w(size)
                return short(text, max(4, int(px / cw)))
            k = (text, px)
            out = CUT_CACHE.get(k)
            if out is None:
                if len(CUT_CACHE) > CUT_CACHE_CAP:
                    CUT_CACHE.clear()
                out = CUT_CACHE[k] = Kit.fit(text, max(10, int(px)))
            return out


        def text_y(top, h, font):
            return top + max(0, int((h - font * 1.35) / 2))


        def flat_button(parent, x, y, w, h, text, fn, tip=None, face=BTN_FACE,
                        color=TEXT_COLOR, font=12, store=None):
            """The one button style used everywhere (rows, panel, magery): a light
            stone tile (hued for the colored buttons) with black UO text."""
            if "button" in NATIVE:
                f = tiled(NATIVE["button"], w, h, FACE_HUE.get(face, hue_of(face)))
                f.SetPos(x, y)
                color = "#141414"
            else:
                f = box(1.0, face)
                f.SetRect(x, y, w, h)
            parent.Add(f)
            lb = label(text, font, color, aligned="center", maxWidth=w)
            place(lb, x, text_y(y, h, font))
            parent.Add(lb)
            c = catcher(x, y, w, h, fn, tip)
            parent.Add(c)
            if store is not None:
                store.extend([f, lb, c])
            return lb


        def friend_button_count():
            return (2 if UI["magery"] else 0) + (1 if UI["healing"] else 0)


        TIP_HEAL = "Cast Heal on %s (Shift+click: Greater Heal). Alt+click: auto-follow (again to stop)"
        TIP_CURE = "Cast Cure on %s (Shift+click: Arch Cure). Alt+click: auto-follow (again to stop)"
        # (2.6.81) UT1-3: B is one action: a bandage in reach, else a follow (again stops it)
        TIP_BANDAGE = ("Bandage %s when next to them; farther away it follows them (again to stop). "
                       "Alt+click: auto-follow (again to stop)")


        def friend_buttons(parent, x, y, w, h, serial, name, store=None, row=None):
            """Friends: [H] Heal and [C] Cure (Magery on; Shift+click for Greater
            Heal / Arch Cure) and [B] bandage (Healing on), left to right from x.
            With `row` (a pooled tracker row) the buttons act for whoever the row
            shows when clicked; returns [(click target, tooltip with %s)] so the
            tooltips can follow the row's name."""
            # (2.6.74) E12: the letter keeps its 100% size when the Scale % shrinks h
            fs = max(7, int(h * 0.7 / min(1.0, UI["scale"] / 100.0)))
            tips = []
            if UI["magery"]:
                for text, spell, stronger, tip, face in (
                        ("H", SPELL_HEAL, SPELL_GREATER_HEAL, TIP_HEAL, COL_HEAL),
                        ("C", SPELL_CURE, SPELL_ARCH_CURE, TIP_CURE, COL_CURE)):
                    if row is None:
                        fn = make_heal_click(serial, spell, stronger)
                    else:
                        fn = RowClick(row, (lambda sp, st: lambda s, n: make_heal_click(s, sp, st))(
                            spell, stronger))
                    parts = []
                    flat_button(parent, x, y, w, h, text, fn, tip % name, face=face,
                                color="#FFFFFF", font=fs, store=parts)
                    if store is not None:
                        store.extend(parts)
                    tips.append((parts[-1], tip))
                    x += w + 2
            if UI["healing"]:
                fn = make_bandage_click(serial, name) if row is None else \
                    RowClick(row, make_bandage_click)
                parts = []
                flat_button(parent, x, y, w, h, "B", fn, TIP_BANDAGE % name,
                            face=COL_BANDAGE, color="#202020", font=fs, store=parts)
                if store is not None:
                    store.extend(parts)
                tips.append((parts[-1], TIP_BANDAGE))
            return tips


        def title_h(s):
            return max(16, int(round(TITLE_H * s)))


        def orow_h(s):
            return max(16, int(round(OPACITY_ROW_H * s)))


        # ------------------------------- FOLLOW --------------------------------------
        # Follow.serial is Virtue Assistant's shared follow, so Character HUD > Frames agrees.
        def start_follow(serial):
            if safe(Follow.current) == serial:
                return True
            return Follow.start(serial, TITLE)   # the shared helper: its refusals too


        def toggle_follow(serial):
            """Alt+click: auto-follow a mobile with TazUO's follow; again to stop."""
            Follow.toggle(serial, TITLE)


        # ------------------------------- BANDAGE -------------------------------------
        # B button (2.6.81, UT1-3: one press = one action, the shard's R1): within
        # BANDAGE_RANGE the press uses a bandage and handle_bandage aims only the
        # cursor that bandage raises (part of the pressed action); farther away the
        # press only starts the auto-follow, and B again (out of reach) stops it.
        # "follow" (UT1-X1) is the serial whose auto-follow a B press started, so the
        # bandage landing, a give-up or the press that stops it ends that follow too.
        BANDAGE = {"serial": None, "name": "", "state": None, "until": 0.0, "follow": None}


        def end_follow(serial):
            """(2.6.81) UT1-X1: stop the auto-follow a B press started for serial
            (never one the player started with Alt+click or another module's)."""
            if serial is None or BANDAGE["follow"] != serial:
                return
            BANDAGE["follow"] = None
            if safe(Follow.current) == serial:
                Follow.stop(TITLE)


        def make_bandage_click(serial, name):
            def _cb(*args):
                if alt_held():                    # Alt+click: auto-follow (the standing rule)
                    toggle_follow(serial)
                    return
                if BANDAGE["serial"] == serial:   # its cursor is still on its way: let it be
                    BANDAGE["serial"] = None
                    release_cursor("bandage")
                    end_follow(serial)
                    API.SysMsg(TITLE + (": stopped bandaging %s; the cursor is yours." % name),
                               Kit.HUE_GOOD)
                    return
                try:
                    mob = API.FindMobile(serial)
                    if mob is None or bool(mob.IsDead):
                        mob = None
                    else:
                        me = API.Player
                        dist = max(abs(int(mob.X) - int(me.X)), abs(int(mob.Y) - int(me.Y)))
                except Exception:
                    mob = None
                if mob is None:
                    API.SysMsg(TITLE + (": can't bandage %s (out of sight or dead)." % name),
                               Kit.HUE_BAD)
                    return
                if dist > BANDAGE_RANGE:          # out of reach: this press only follows
                    if BANDAGE["follow"] == serial and safe(Follow.current) == serial:
                        end_follow(serial)        # B again while out of reach: stop
                        API.SysMsg(TITLE + (": stopped following %s." % name), Kit.HUE_GOOD)
                        return
                    started = safe(Follow.current) != serial
                    if not start_follow(serial):
                        return
                    if started:
                        BANDAGE["follow"] = serial
                    API.SysMsg(TITLE + (": following %s; press B again once you reach them."
                                        % name), Kit.HUE_INFO)
                    return
                band = find_bandage()
                if not band:
                    API.SysMsg(TITLE + ": no bandages in your backpack.", Kit.HUE_BAD)
                    return
                if BANDAGE["serial"] is not None or cursor_owner() is not None \
                        or API.HasTarget("any"):
                    API.SysMsg(TITLE + ": a target cursor is up; answer or cancel it, then press B.",
                               Kit.HUE_BAD)
                    return                        # never steal a cursor that's up
                API.UseObject(band)
                BANDAGE.update(serial=serial, name=name, state="cursor",
                               until=time.time() + BANDAGE_CURSOR_WAIT)
                claim_cursor("bandage", BANDAGE_CLAIM)   # the cursor that comes is ours to aim
            return _cb


        def find_bandage():
            for get in (lambda: API.FindType(BANDAGE_GRAPHIC, API.Backpack),
                        lambda: API.FindType(BANDAGE_GRAPHIC)):
                item = safe(get)
                if item:
                    return item


        # ----------------------------- the shared cursor -----------------------------
        # One target cursor for every module (HOST.claim_cursor / cursor_busy): while
        # Ultima Tracker's own bandage or spell cursor is on its way it claims the
        # cursor, and its automatic steps leave a cursor someone else has spoken for
        # alone (no aiming, no cancelling).
        CURSOR_KEY = "ultima"
        CURSOR_OWN = {"bandage": False, "spell": False}   # which of our flows holds the claim


        def claim_cursor(what, seconds):
            CURSOR_OWN[what] = True
            safe(lambda: HOST.claim_cursor(CURSOR_KEY, seconds))


        def release_cursor(what):
            if not CURSOR_OWN.get(what):
                return
            CURSOR_OWN[what] = False
            if not any(CURSOR_OWN.values()):
                safe(lambda: HOST.release_cursor(CURSOR_KEY))


        def cursor_owner():
            """Who else has the cursor spoken for (a module key, "pick"), or None."""
            return safe(lambda: HOST.cursor_busy(CURSOR_KEY), None)


        def click_can_aim():
            """A click on a bar answers the cursor that's up: your own, ours, or a
            module asking you to pick something; never one another module is
            answering by itself (then the click does what it does without a cursor)."""
            owner = cursor_owner()
            if owner is not None and owner != "pick":
                return False
            return bool(API.HasTarget("any"))


        def handle_bandage():
            s = BANDAGE["serial"]
            if s is None:
                release_cursor("bandage")         # ended (cancelled, done, gave up)
                return
            name = BANDAGE["name"]
            try:                                  # (every poll while a bandage is on its way)
                mob = API.FindMobile(s)
                gone = mob is None or bool(mob.IsDead)
            except Exception:
                gone = True
            if gone:
                BANDAGE["serial"] = None
                end_follow(s)                     # (2.6.81) UT1-X1
                API.SysMsg(TITLE + (": can't bandage %s (out of sight or dead)." % name),
                           Kit.HUE_BAD)
                return
            if time.time() > BANDAGE["until"]:
                BANDAGE["serial"] = None
                end_follow(s)
                API.SysMsg(TITLE + (": the bandage gave no target cursor for %s." % name),
                           Kit.HUE_BAD)
                return
            # (2.6.81) UT1-3: the press already used the bandage ("cursor" is the only
            # state now); aim only the beneficial cursor it raised, while our claim holds
            # and nobody else has the cursor spoken for (HOST.cursor_ok)
            if BANDAGE["state"] == "cursor" and CURSOR_OWN["bandage"] \
                    and HOST.cursor_ok(CURSOR_KEY, "beneficial"):
                API.Target(s)
                BANDAGE["serial"] = None
                release_cursor("bandage")
                end_follow(s)                     # the bandage landed: the B follow ends


        def check_follow():
            safe(Follow.current)                 # catch up with the client (stopped, other module)
            s = Follow.serial
            if s is not None and not mobile_seen(s):   # (2.6.82) HOST.mobile: no second lookup
                Follow.serial = None             # gone from view; the client stops too
            if BANDAGE["follow"] is not None and Follow.serial != BANDAGE["follow"]:
                BANDAGE["follow"] = None         # (2.6.81) the B follow ended some other way


        # ------------------------------- WINDOW CHROME -------------------------------
        def draw_icon(add, add_ctrl, x, y, sz, kind, on):
            u = sz / 16.0

            def R(v):
                return int(round(v * u))

            def S(v):
                return max(1, int(round(v * u)))

            if kind == "lock":
                col = LOCK_ON if on else LOCK_OFF
                add(x + R(3), y + R(8), S(10), S(6), col)                    # body
                add(x + R(7), y + R(10), S(2), S(2), BTN_FACE_ON if on else BTN_FACE)
                if on:                                                       # closed shackle
                    add(x + R(4), y + R(2), S(8), S(2), col)
                    add(x + R(4), y + R(2), S(2), S(6), col)
                    add(x + R(10), y + R(2), S(2), S(6), col)
                else:                                                        # raised, open shackle
                    add(x + R(4), y + R(0), S(8), S(2), col)
                    add(x + R(4), y + R(0), S(2), S(8), col)
                    add(x + R(10), y + R(0), S(2), S(3), col)
            elif kind == "min":
                if on:                                                       # restore: a window
                    add(x + R(4), y + R(4), S(8), S(2), ICON_COLOR)
                    add(x + R(4), y + R(4), S(1), S(8), ICON_COLOR)
                    add(x + R(11), y + R(4), S(1), S(8), ICON_COLOR)
                    add(x + R(4), y + R(11), S(8), S(1), ICON_COLOR)
                else:                                                        # minimize: a bar
                    add(x + R(4), y + R(10), S(8), S(2), ICON_COLOR)
            elif kind == "dock":                                             # down into the bar
                for i in range(4):
                    add(x + R(4 + i), y + R(3 + i), S(8 - 2 * i), S(1), ICON_COLOR)
                add(x + R(3), y + R(11), S(10), S(2), ICON_COLOR)
            elif kind == "opacity":                                          # fading bars
                add(x + R(3), y + R(4), S(3), S(8), "#FFFFFF")
                add(x + R(6), y + R(4), S(3), S(8), "#A0A0A0")
                add(x + R(9), y + R(4), S(3), S(8), "#5A5A5A")
            elif kind == "close":
                fs = max(8, int(sz * 0.8))
                lb = ttf("x", fs, ICON_COLOR, aligned="center", maxWidth=sz)
                lb.SetPos(x, y + max(0, int((sz - fs * 1.35) / 2)))
                add_ctrl(lb)


        TITLE_CLICKS = {}   # id(gump) -> (time, (x, y)) of the last title-strip click
        CHROMES = []        # every live window's Chrome (for the Borders? toggle)


        def apply_borders_all():
            for c in list(CHROMES):
                if safe(lambda: c.gump.IsDisposed, True):
                    CHROMES.remove(c)                 # window was closed or rebuilt
                else:
                    c.frame.apply_borders()


        class Frame(object):
            """Window background. Native: only the outer stone rim of the client's
            frame art (FRAME_GUMP); the dark band the art has inside that rim is
            cropped off, and the middle fades with the opacity setting. The rim
            stays solid. Flat: a faded box and four border boxes."""

            def __init__(self, gump):
                self.art = NATIVE.get("frame")
                self.size = (0, 0)
                if self.art:
                    self.center = tiled(SECTION_GUMP, 1, 1)
                    gump.Add(self.center)
                    # top / bottom: rows cut from the top edge piece; left / right:
                    # columns cut from the left edge piece (its stone side is outermost)
                    self.edges = [(i, tiled(FRAME_GUMP + (1 if i in (0, 1) else 3), 1, 1))
                                  for i in range(4)]
                else:
                    self.center = box(1.0, BG_COLOR)
                    gump.Add(self.center)
                    self.edges = [(i, box(1.0, BORDER_COLOR)) for i in range(4)]
                for _, b in self.edges:
                    gump.Add(b)

            def layout(self, w, h):
                self.size = (w, h)
                rects = [(0, 0, w, BORDER), (0, h - BORDER, w, BORDER),
                         (0, 0, BORDER, h), (w - BORDER, 0, BORDER, h)]
                for (_, b), r in zip(self.edges, rects):
                    b.SetRect(*r)
                self.apply_borders()

            def apply_borders(self):
                on = UI["borders"]
                for _, p in self.edges:
                    set_box_alpha(p, 1.0 if on else 0.0)
                w, h = self.size
                if self.art and on:              # the middle stops at the rim
                    self.center.SetRect(BORDER, BORDER, max(0, w - 2 * BORDER),
                                        max(0, h - 2 * BORDER))
                else:
                    self.center.SetRect(0, 0, w, h)

            def set_alpha(self, a):
                set_box_alpha(self.center, a)


        class KitFrame(object):
            """(2.6.72) The standard Virtue Assistant frame for the tracker groups and
            the Combat window: the stone 9-piece (Kit.WINDOW_BG) with its corner
            knots, its stone inside, and one black panel (Kit.SECTION_TILE) behind
            the content. Made once and moved with SetRect, so a change of size never
            puts a piece over the rows. Its stone pieces are noted as the window's
            frame (Kit._frame_parts), so "Join zone windows in one frame" hides them
            like any Kit window's; the black panel then keeps Kit.SECTION_ALPHA
            whatever the opacity setting says."""
            M = Kit.MARGIN

            def __init__(self, gump, key=None):
                self.gump, self.key = gump, key
                self.size, self.top, self.alpha = (0, 0), 0, 1.0
                base = Kit.WINDOW_BG
                self.s = [Kit.pic_size(base + i) for i in range(9)]
                self.ok = all(p[0] > 0 and p[1] > 0 for p in self.s)
                parts = []
                self.fill = tiled(base + 4, 1, 1)
                gump.Add(self.fill)
                parts.append(self.fill)
                self.center = tiled(Kit.SECTION_TILE, 1, 1)
                gump.Add(self.center)
                self.edges, self.corners, self.knots = [], [], []
                if self.ok:
                    for i in (1, 7, 3, 5):                    # top, bottom, left, right
                        t = tiled(base + i, 1, 1)
                        gump.Add(t)
                        self.edges.append(t)
                    for i in (0, 2, 6, 8):                    # the four corner pieces
                        c = pic(base + i, 0, 0)
                        gump.Add(c)
                        self.corners.append(c)
                    if Kit.CORNER_ART:
                        self.kw, self.kh = Kit.pic_size(Kit.CORNER_ART)
                        if self.kw and self.kh:
                            for _ in range(4):
                                k = pic(Kit.CORNER_ART, 0, 0)
                                gump.Add(k)
                                self.knots.append(k)
                parts += self.edges + self.corners + self.knots
                self.parts = parts
                try:
                    Kit._frame_parts[gump] = parts       # the one frame hides these
                except Exception:
                    pass
                if key is not None and safe(lambda: HOST.layout_unified(key), False):
                    safe(lambda: Kit.hide_zone_frame(gump))   # zoned with one frame on: hidden now

            def layout(self, w, h, top=None):
                if top is not None:
                    self.top = top
                self.size = (w, h)
                M = self.M
                if self.ok:
                    tl, t, tr, l, c, r, bl, b, br = self.s
                    self.fill.SetRect(l[0], t[1], max(0, w - l[0] - r[0]), max(0, h - t[1] - b[1]))
                    for e, rc in zip(self.edges, (
                            (tl[0], 0, w - tl[0] - tr[0], t[1]),
                            (bl[0], h - b[1], w - bl[0] - br[0], b[1]),
                            (0, tl[1], l[0], h - tl[1] - bl[1]),
                            (w - r[0], tr[1], r[0], h - tr[1] - br[1]))):
                        e.SetRect(rc[0], rc[1], max(0, rc[2]), max(0, rc[3]))
                    for cp, xy in zip(self.corners, ((0, 0), (w - tr[0], 0), (0, h - bl[1]),
                                                     (w - br[0], h - br[1]))):
                        cp.SetPos(*xy)
                    for k, xy in zip(self.knots, ((0, 0), (w - self.kw, 0), (0, h - self.kh),
                                                  (w - self.kw, h - self.kh))):
                        k.SetPos(*xy)
                else:
                    self.fill.SetRect(0, 0, w, h)
                ch = h - self.top - M
                self.center.SetRect(M, self.top, max(0, w - 2 * M), max(0, ch))
                set_vis(self.center, ch > 4)

            def apply_borders(self):
                pass                                     # (the pop-out bars' option only)

            def set_alpha(self, a):
                if self.key is not None and safe(lambda: HOST.layout_unified(self.key), False):
                    a = Kit.SECTION_ALPHA                # (2.6.72) one frame: no opacity of its own
                self.alpha = a
                set_box_alpha(self.center, a)

            def drop_all(self):
                for c in [self.fill, self.center] + self.edges + self.corners + self.knots:
                    drop(c)
                self.edges, self.corners, self.knots = [], [], []
                try:
                    if Kit._frame_parts.get(self.gump) is self.parts:
                        Kit._frame_parts.pop(self.gump, None)
                except Exception:
                    pass


        class Chrome(object):
            """Shared look for every window: faded background, solid border, a title
            strip with [padlock] ([fold into the Action Bar]) [minimize] [opacity] ([x])
            buttons and a fold-out opacity slider row. Content goes below
            `content_top`."""

            def __init__(self, gump, kit=False, key=None):
                self.gump = gump
                self.kit, self.key = kit, key    # (2.6.72) the standard Kit look (groups, Combat)
                self.frame = KitFrame(gump, key) if kit else Frame(gump)
                self.status_lbl, self.status_text = None, None
                self.store = ({}, {})
                # one entry per window: drop this gump's old Chrome (Combat Bars
                # redraws in place) and any closed windows
                CHROMES[:] = [c for c in CHROMES
                              if c.gump is not gump and not safe(lambda: c.gump.IsDisposed, True)]
                CHROMES.append(self)
                self.strip = []
                self.title_bg = self.title_lbl = self.slider = self.pct_lbl = None
                self.title_text = self.title_color = None
                self.title_raw = self.status_x = None   # (2.6.82) set_title / set_status caches
                self.title_max, self.title_pos, self.font = 40, (0, 0), TITLE_FONT
                self.opacity, self.content_top = DEFAULT_OPACITY, BORDER
                self.on_title_alt, self.alt_key = None, None   # (2.6.81) UT1-4

            def _add(self, ctrl):
                self.gump.Add(ctrl)
                self.strip.append(ctrl)
                return ctrl

            def _clear_strip(self):
                for c in self.strip:
                    drop(c)
                self.strip = []
                self.title_bg = self.title_lbl = self.slider = self.pct_lbl = None
                self.status_lbl, self.status_text = None, None

            def dispose(self):
                """Take every control of this window's look away (it's redrawn)."""
                self._clear_strip()
                f = self.frame
                if self.kit:
                    f.drop_all()
                else:
                    drop(f.center)
                    for _, b in f.edges:
                        drop(b)
                    f.edges = []
                if self in CHROMES:
                    CHROMES.remove(self)

            def layout(self, w, h, s, opacity, title, color, buttons,
                       opacity_open=False, reserve=0, on_title_dbl=None,
                       on_title_alt=None, alt_key=None):
                """buttons: [(kind, on, fn, tooltip), ...] left to right.
                Returns the x where `reserve` pixels were kept free for extras.
                on_title_alt (2.6.81): an Alt+click on the title strip (not an
                Alt+drag of the window, whose anchor key is alt_key) calls it."""
                if self.kit:
                    return self._layout_kit(w, h, opacity, title, color, buttons, on_title_dbl)
                self.opacity = opacity
                a = opacity / 100.0
                self.frame.layout(w, h)
                self.frame.set_alpha(a)

                self._clear_strip()
                th = title_h(s)
                if "header" in NATIVE:
                    self.title_bg = self._add(tiled(NATIVE["header"], w - 2 * BORDER, th))
                    self.title_bg.SetPos(BORDER, BORDER)
                    set_box_alpha(self.title_bg, a)
                else:
                    self.title_bg = self._add(box(a, TITLE_BG))
                    self.title_bg.SetRect(BORDER, BORDER, w - 2 * BORDER, th)
                if "frame" in NATIVE and DIVIDER_H:      # stone between title and content
                    d = self._add(tiled(Kit.STONE_TILE, w - 2 * BORDER, DIVIDER_H))
                    d.SetPos(BORDER, BORDER + th - DIVIDER_H)

                bsz = max(12, th - 6 - DIVIDER_H)
                gap = max(2, int(round(2 * s)))
                n = len(buttons)
                bx = w - BORDER - 4 - n * bsz - max(0, n - 1) * gap
                left = bx

                # double-click the title strip to minimize / restore; the strip stays
                # draggable because the click target is allowed to move the window
                self.on_title_dbl = on_title_dbl
                self.on_title_alt, self.alt_key = on_title_alt, alt_key
                if on_title_dbl is not None:
                    tip = "Double-click: minimize or restore"
                    if on_title_alt is not None:
                        tip += ". Alt+click: auto-follow (again to stop)"
                    tc = catcher(BORDER, BORDER, max(10, left - reserve - BORDER - 2), th,
                                 self._title_clicked, tip)
                    safe(lambda: setattr(tc, "CanMove", True))
                    if Client.mouse is None:
                        Kit.hook_double(tc, Kit.once(lambda: self.on_title_dbl(), ("utitle", id(self))))
                    self._add(tc)
                by = BORDER + (th - DIVIDER_H - bsz) // 2
                for kind, on, fn, tip in buttons:
                    self._button(bx, by, bsz, kind, on, fn, tip)
                    bx += bsz + gap

                self.font = max(9, int(round(TITLE_FONT * text_scale(s))))   # (2.6.74) E12
                self.title_max = max(20, left - reserve - BORDER - 10)
                self.title_pos = (BORDER + 5, text_y(BORDER, th - DIVIDER_H, self.font))
                self.title_color = color
                self.title_text = None
                self.set_title(title)

                y = BORDER + th
                if opacity_open:
                    rh = orow_h(s)
                    fs = max(8, int(round(11 * text_scale(s))))   # (2.6.74) E12
                    lb = self._add(label("Opacity", fs, DIM_TEXT))
                    place(lb, BORDER + 5, text_y(y, rh, fs))
                    pw = int(round(34 * s))
                    sx = BORDER + int(round(54 * s))
                    sw = max(40, w - BORDER - 8 - pw - sx)
                    self.slider = API.Gumps.CreateSlider(sw, 0, 100, opacity, sx,
                                                         y + max(2, (rh - 10) // 2), True)
                    self._add(self.slider)
                    self.pct_lbl = self._add(label("%d%%" % opacity, fs, TEXT_COLOR,
                                                   aligned="right", maxWidth=pw))
                    place(self.pct_lbl, w - BORDER - 4 - pw, text_y(y, rh, fs))
                    y += rh
                self.content_top = y
                return left - reserve

            def _layout_kit(self, w, h, opacity, title, color, buttons, on_title_dbl):
                """(2.6.72) The standard title row (virtue-assistant-ui-text-rules 2.1):
                a 30 px black section at (MARGIN, MARGIN), the title gold UPPER CASE at
                (MARGIN + 30, MARGIN + 7), a grey status after it (the count), and at the
                right, right to left: Close (when the window has one), Minimize or
                Restore, the gold Fold arrow and Settings. The tracker's own padlock
                and opacity buttons are gone from it (the zone lock and the settings
                page do those). A 3 px stripe in the group's colour runs under the
                title row; the content starts a GAP under it."""
                M = Kit.MARGIN
                self.opacity = opacity
                self._clear_strip()
                mini = any(k == "min" and on for k, on, fn, tip in buttons)
                top = M + 30 + Kit.GAP
                self.content_top = top
                self.frame.layout(w, h, top)
                self.frame.set_alpha(opacity / 100.0)
                sec = self._add(tiled(Kit.SECTION_TILE, w - 2 * M, 30))
                sec.SetPos(M, M)
                set_box_alpha(sec, Kit.SECTION_ALPHA)
                if not mini and color:
                    st = self._add(box(1.0, color))
                    st.SetRect(M, M + 30, w - 2 * M, 3)
                kinds = dict((k, (on, fn, tip)) for k, on, fn, tip in buttons)
                # (2.6.85) a window in a zone is always up: no Close, Minimize or fold
                if self.key is not None and Kit.zone_up(self.key):
                    for k in ("close", "min", "dock"):
                        kinds.pop(k, None)
                bx = w - M - 54                          # the Close slot
                if "close" in kinds:
                    self._art(Kit.ART_CLOSE[0], bx, M + 4, kinds["close"][1], kinds["close"][2])
                    bx -= 20
                if "min" in kinds:
                    on, fn, tip = kinds["min"]
                    self._art((Kit.ART_RESTORE if on else Kit.ART_MIN)[0], bx, M + 7, fn,
                              Kit.RESTORE_TIP if on else Kit.MIN_TIP)
                    bx -= Kit.DOCK_DX
                if "dock" in kinds:
                    self._art(Kit.ART_DOCK[0], bx, M + 7 + Kit.DOCK_DY, kinds["dock"][1], Kit.DOCK_TIP)
                    bx -= 10
                left = bx
                if not mini:
                    cap = "Settings"
                    sx = bx - 35 - Kit.text_w(cap)
                    if sx > M + 30 + Kit.text_w("COMBAT") + 40:
                        self._art(Kit.ART_PAGE[0], sx, M + 4, settings_click,
                                  Kit.SETTINGS_TIP % TITLE, cap)
                        left = sx
                Kit.note_title(self.gump, M)
                self.on_title_dbl = on_title_dbl
                if on_title_dbl is not None:
                    tc = catcher(M, M, max(10, left - M - 6), 30, self._title_clicked, Kit.DOUBLE_TIP)
                    safe(lambda: setattr(tc, "CanMove", True))
                    if Client.mouse is None:
                        Kit.hook_double(tc, Kit.once(lambda: self.on_title_dbl(), ("utitle", id(self))))
                    self._add(tc)
                self.title_max = max(20, left - M - 30 - 10)
                self.title_pos = (M + 30, M + 7)
                self.title_color = color
                self.title_text = None
                self.set_title(title)
                return left

            def _art(self, graphic, x, y, fn, tip, cap=None):
                """A Kit button's art (normal face) with a click area and tooltip."""
                p = self._add(pic(graphic, x, y))
                bw, bh = Kit.pic_size(graphic)
                bw, bh = bw or 20, bh or 20
                if cap:
                    lb = Kit.add_label(self.gump, cap, x + bw + 5, y + 3, Kit.HUE_TEXT)
                    self.strip.append(lb)
                    bw += 5 + Kit.text_w(cap)
                self._add(catcher(x, y, bw, bh, fn, tip))
                return p

            def set_status(self, text):
                """(2.6.72) The grey status after the title (the count, Combat's
                low / PSN / PAR); kit look only."""
                if not self.kit or self.title_lbl is None:
                    return
                text = text or ""
                if text == self.status_text:
                    return
                self.status_text = text
                x = self.title_pos[0] + Kit.text_w(self.title_text or "") + 12
                room = self.title_pos[0] + self.title_max - x
                shown = Kit.fit(text, room) if room > 20 else ""
                at = (x, self.title_pos[1])
                if self.status_lbl is None:
                    self.status_lbl = Kit.add_label(self.gump, shown, x, self.title_pos[1],
                                                    Kit.HUE_INFO)
                    self.strip.append(self.status_lbl)
                    self.status_x = at
                else:
                    if at != self.status_x:           # (2.6.82) moved only when the title did
                        self.status_x = at
                        try:
                            self.status_lbl.SetPos(x, self.title_pos[1])
                        except Exception:
                            pass
                    Kit.set_text(self.status_lbl, shown)

            def _title_clicked(self, *args):
                now = time.time()
                key = id(self.gump)          # survives redraws of the same window
                pos = (safe(lambda: self.gump.GetX(), 0), safe(lambda: self.gump.GetY(), 0))
                if self.on_title_alt is not None and alt_held():
                    # (2.6.81) UT1-4: Alt+click follows (a minimized pop-out's only
                    # control for its player), but an Alt+drag also ends in a click:
                    # follow only when the window didn't move (the anchors aren't
                    # following a drag of it, and it stands where they last saw it)
                    ak = self.alt_key
                    ref = (ANCHORS.pos or {}).get(ak) if ak is not None else None
                    moved = (ak is not None and ANCHORS.moving == ak) or ANCHORS.in_drag() \
                        or (ref is not None and (abs(pos[0] - ref[0]) > TITLE_JITTER
                                                 or abs(pos[1] - ref[1]) > TITLE_JITTER))
                    if not moved:
                        self.on_title_alt()
                    return                   # never counted toward a double-click
                last = TITLE_CLICKS.get(key)
                # a drag also ends in a click, so the window must not have moved far
                if last and now - last[0] <= TITLE_DBL_SECONDS \
                        and abs(pos[0] - last[1][0]) <= TITLE_JITTER \
                        and abs(pos[1] - last[1][1]) <= TITLE_JITTER:
                    TITLE_CLICKS.pop(key, None)
                    Kit.once(lambda: self.on_title_dbl(), ("utitle", id(self)))()
                else:
                    if len(TITLE_CLICKS) > CACHE_CAP:    # one entry per window ever drawn
                        TITLE_CLICKS.clear()
                    TITLE_CLICKS[key] = (now, pos)

            def _button(self, x, y, sz, kind, on, fn, tip):
                icon = NATIVE.get("icons", {}).get(kind)
                if icon:
                    graphic, (iw, ih) = icon[1 if on else 0]
                    if iw <= sz + 6 and ih <= sz + 6:    # client art, centered in the cell
                        hue = HUE_LOCKED if kind == "lock" and on else 0
                        p = self._add(pic(graphic, x + (sz - iw) // 2, y + (sz - ih) // 2, hue))
                        if kind == "lock" and not on:
                            set_box_alpha(p, LOCK_OFF_ALPHA)   # unlocked: the plain, dimmer padlock
                        self._add(catcher(x, y, sz, sz, fn, tip))
                        return
                if kind == "close" and "char_w" in NATIVE:
                    lb = inert(self._add(API.Gumps.CreateGumpLabel("x", HUE_TEXT)))
                    lb.SetPos(x + max(0, (sz - int(NATIVE["char_w"])) // 2),
                              y + (sz - NATIVE["font_h"]) // 2)
                    self._add(catcher(x, y, sz, sz, fn, tip))
                    return
                lit = on and kind in ("lock", "opacity")
                face = self._add(box(1.0, BTN_FACE_ON if lit else BTN_FACE))
                face.SetRect(x, y, sz, sz)

                def add(bx, by, bw, bh, col):
                    p = self._add(box(1.0, col))
                    p.SetRect(bx, by, bw, bh)

                draw_icon(add, self._add, x, y, sz, kind, on)
                self._add(catcher(x, y, sz, sz, fn, tip))

            def set_title(self, text, color=None):
                if self.kit:
                    rk = (text, self.title_max)       # (2.6.82) the same title: nothing to fit
                    if self.title_lbl is not None and rk == self.title_raw:
                        return
                    self.title_raw = rk
                    text = Kit.fit(str(text).upper(), self.title_max)
                    if self.title_lbl is None:
                        self.title_lbl = Kit.add_label(self.gump, text, self.title_pos[0],
                                                       self.title_pos[1], Kit.HUE_TITLE)
                        self.strip.append(self.title_lbl)
                        self.title_text = text
                    elif text != self.title_text:
                        self.title_text = text
                        Kit.set_text(self.title_lbl, text)
                        if self.status_text is not None:
                            st, self.status_text = self.status_text, None
                            self.set_status(st)          # it starts after the title
                    return
                if color is not None and color != self.title_color:
                    self.title_color = color
                    old = self.title_lbl
                    if old is not None and not set_hue(old, color):
                        # a smooth-font title: its color is fixed, so a new label
                        self.title_text = None
                        if old in self.strip:
                            self.strip.remove(old)
                        drop(old)
                        self.title_lbl = None
                text = cut_text(text, self.title_max, self.font)   # (2.6.74) E12: cut, not shrunk
                if self.title_lbl is None:
                    self.title_lbl = self._add(label(text, self.font,
                                                     self.title_color or TEXT_COLOR))
                    place(self.title_lbl, *self.title_pos)
                    self.title_text = text
                elif text != self.title_text:
                    self.title_text = text
                    set_text(self.title_lbl, text)

            def set_opacity(self, v):
                self.opacity = v
                a = v / 100.0
                self.frame.set_alpha(a)
                if self.kit:
                    return
                if self.title_bg is not None:
                    set_box_alpha(self.title_bg, a)
                if self.pct_lbl is not None:
                    set_text(self.pct_lbl, "%d%%" % v)

            def poll(self):
                """Read the opacity slider; returns the new value when it moved."""
                if self.slider is None:
                    return None
                v = clamp(safe(lambda: int(self.slider.Value), self.opacity), 0, 100)
                if v != self.opacity:
                    self.set_opacity(v)
                    return v
                return None


        def std_buttons(locked, minimized, opacity_open, on_lock, on_min, on_opacity,
                        on_close=None, on_dock=None):
            b = [("lock", locked, on_lock, "Unlock the window (it can be moved and resized again)"
                  if locked else "Lock the window in place (no moving or resizing)")]
            if on_dock is not None and not minimized:     # gold arrow, left of Minimize
                b.append(("dock", False, on_dock, Kit.DOCK_TIP))
            b.append(("min", minimized, on_min,
                      "Restore" if minimized else "Minimize (double-click the title does too)"))
            if not minimized:
                b.append(("opacity", opacity_open, on_opacity,
                          "Hide the background opacity slider" if opacity_open
                          else "Show the background opacity slider (the frame and bars stay solid)"))
            if on_close is not None:
                b.append(("close", False, on_close, "Close"))
            return b


        # ------------------------------- ANCHORING -----------------------------------
        def move_gump(g, x, y):
            try:
                g.SetPos(x, y)
            except Exception:
                safe(lambda: setattr(g, "X", x))
                safe(lambda: setattr(g, "Y", y))


        class Anchors(object):
            """Drop a window next to another one (within SNAP_DISTANCE of an edge)
            and it snaps flush and anchors to it; anchored windows then move as one
            group when any of them is dragged. Alt+drag pulls a single window out of
            its group, and the Settings page's "Unanchor all" breaks every group.

            The windows' places are only read while something moves: the host's
            snapping already watches every window each pass and says which one is
            being dragged (dragging()), and each window's Kit.on_moved callback
            reports it let go (note_moved). Then a window that moved without us
            moving it is being dragged, so the rest of its group gets the same
            offset; once it has been still for a moment, it's checked for a snap.
            A quiet poll costs no client call at all."""

            def __init__(self):
                self.gid = {}          # window key -> group id
                self.next_gid = 1
                self.pos = {}          # window key -> (x, y) we last saw / set; None = measure again
                self.dims = {}         # window key -> (w, h) last seen
                self.moving = None
                self.still = 0
                self.pending = False   # a window's on_moved callback fired since the last look
                self.linger = 0        # polls still to look after the last move ended
                self.alt_used = False
                self.touched = False   # a group changed since groups_changed() last looked
                self.saved = []        # the groups as last saved

            # ----- what the windows and the host tell us -----
            def note_moved(self, key):
                """A window's Kit.on_moved callback: it was dragged (or shifted by
                the host's snapping or keeper) and let go. The next poll looks."""
                self.pending = True

            def placed(self, key, x=None, y=None, w=None, h=None):
                """Window `key` was (re)built, put at (x, y) or resized to (w, h) by
                this module or the player: that is where it stands now, not a move
                (the place and size a drag of it later starts from; unknown:
                measured at the next look)."""
                if self.pos is None:
                    self.pos = {}
                if x is None:
                    self.pos.pop(key, None)
                else:
                    self.pos[key] = (int(x), int(y))
                if w is None:
                    self.dims.pop(key, None)
                else:
                    self.dims[key] = (int(w), int(h))
                self.pending = True                 # one look: its size, the other windows

            def sized(self, key, w, h):
                """Window `key` is (w, h) now (its height followed its rows): kept so
                the next drag of it is not taken for a resize."""
                self.dims[key] = (int(w), int(h))

            @staticmethod
            def dragging():
                """Is a window being dragged right now? The host's snapping keeps a
                list of the windows in a drag (no client call to read it); on a
                build without it, the mouse button decides (None = can't tell:
                look)."""
                try:
                    return bool(SNAP.drag)
                except Exception:
                    pass
                try:
                    return SNAP.pressed() is not False
                except Exception:
                    return True

            @staticmethod
            def in_drag():
                """(2.6.74) Does the host see a window in a drag now (its list, no
                client call)? False when it can't tell: a drop is never waited for
                for good."""
                try:
                    return bool(SNAP.drag)
                except Exception:
                    return False

            @staticmethod
            def dragged_gump(g):
                """Is this gump one the host sees being dragged?"""
                try:
                    return g in SNAP.drag
                except Exception:
                    return False

            @staticmethod
            def host_follows(g):
                """The windows the host's own snapping moves along with g while g
                is dragged (the ones snapped on to it, and theirs): shifting them
                here as well would move them twice (the host looks every other
                poll, so they would race ahead of the group)."""
                out = set()
                try:
                    if not SNAP.enabled or g in SNAP.no_snap:
                        return out
                    links, members = SNAP.links, SNAP.members
                    todo = [g]
                    while todo:
                        lead = todo.pop()
                        for f, l in list(links.items()):
                            if l is lead and f is not g and f not in out and f in members:
                                out.add(f)
                                todo.append(f)
                except Exception:
                    return set()
                return out

            # ----- groups -----
            def add_group(self, keys):
                g = self.next_gid
                self.next_gid += 1
                for k in keys:
                    self.gid[k] = g

            def members(self, key):
                g = self.gid.get(key)
                if g is None:
                    return [key]
                return [k for k, v in self.gid.items() if v == g]

            def join(self, a, b):
                ga, gb = self.gid.get(a), self.gid.get(b)
                if ga is None and gb is None:
                    self.add_group([a, b])
                elif ga is None:
                    self.gid[a] = gb
                elif gb is None:
                    self.gid[b] = ga
                elif ga != gb:
                    for k, v in list(self.gid.items()):
                        if v == gb:
                            self.gid[k] = ga
                self.touched = True

            def detach(self, key):
                g = self.gid.pop(key, None)
                if g is not None:
                    self.touched = True
                    rest = [k for k, v in self.gid.items() if v == g]
                    if len(rest) == 1:                 # a group of one isn't a group
                        self.gid.pop(rest[0], None)

            def clear(self):
                self.gid = {}
                self.touched = True

            def saved_groups(self):
                groups = {}
                for k, g in self.gid.items():
                    if k in FIXED_WINDOWS:
                        groups.setdefault(g, []).append(k)
                return [sorted(v) for v in groups.values() if len(v) > 1]

            def groups_changed(self):
                """True once after the saved groups changed (worked out only when
                a group was touched, not every pass)."""
                if not self.touched:
                    return False
                self.touched = False
                now = self.saved_groups()
                if now == self.saved:
                    return False
                self.saved = now
                return True

            # ----- per poll -----
            @staticmethod
            def shift(m, dx, dy, rects, wins):
                x, y, w, h = rects[m]
                g = wins[m][0]
                move_gump(g, x + dx, y + dy)
                Kit.moved_by_code(g)                    # a group shift, not a drag of m
                rects[m] = (x + dx, y + dy, w, h)

            @staticmethod
            def rect(g, size):
                try:
                    x, y = int(g.GetX()), int(g.GetY())
                except Exception:
                    return None
                try:
                    w = int(g.GetWidth()) or size[0]
                except Exception:
                    w = size[0]
                try:
                    h = int(g.GetHeight()) or size[1]
                except Exception:
                    h = size[1]
                return x, y, w, h

            def tick(self, get_wins):
                """get_wins() -> {key: (gump, (w, h))} for every open window. The
                windows are only looked at while something moves: a drag the host
                sees, a window we saw move and are waiting to see dropped, a window
                whose on_moved callback just fired, or the moment after a drop (the
                host's own snap may still nudge the dropped window). A quiet poll
                makes no client call."""
                if self.moving is None and not self.pending and self.linger <= 0 \
                        and not self.dragging():
                    for k in list(self.gid):            # closed pop-outs leave their group
                        if k not in FIXED_WINDOWS and not pop_listed(k):
                            self.detach(k)
                    return
                self.pending = False
                if self.linger > 0:
                    self.linger -= 1
                wins = get_wins()
                for k in list(self.gid):                # closed pop-outs leave their group
                    if k not in wins and k not in FIXED_WINDOWS:
                        self.detach(k)
                rects = {}
                for k, (g, size) in wins.items():
                    if g is None:
                        continue
                    try:
                        if g.IsDisposed:
                            continue
                    except Exception:
                        continue
                    r = self.rect(g, size)
                    if r is not None:
                        rects[k] = r
                held = layout_held_keys()               # slotted in the layout: it places them
                # (2.6.74) Arrange mode: the anchors stand down (no group shift, no snap):
                # a dragged window towed its free group mates along, and the snap after
                # the drop pulled it back out of the zone the layout had just given it
                arranging = layout_arranging()
                if self.pos is None:                    # first look ever: nothing to compare
                    moved = []
                else:
                    moved = [k for k, r in rects.items()
                             if k in self.pos and (r[0], r[1]) != self.pos[k] and k not in held]
                if moved:
                    # the dragged one: the window we already follow, else the one
                    # the host sees in a drag, else the first that moved (the others
                    # that moved on their own were placed by code: only noted)
                    k = self.moving if self.moving in moved else None
                    if k is None:
                        for m in moved:
                            if self.dragged_gump(wins[m][0]):
                                k = m
                                break
                    if k is None:
                        k = moved[0]
                    dx = rects[k][0] - self.pos[k][0]
                    dy = rects[k][1] - self.pos[k][1]
                    resized = self.dims.get(k, rects[k][2:]) != rects[k][2:]
                    if resized:                         # dragged a top/left edge: not a move
                        moved = []
                    elif k in self.gid and alt_held():
                        self.detach(k)                  # Alt+drag: move this one alone
                        if not self.alt_used:
                            self.alt_used = True
                            API.SysMsg(TITLE + ": window unanchored.", Kit.HUE_GOOD)
                    host_moved = self.host_follows(wins[k][0]) if moved and not arranging else ()
                    for m in (self.members(k) if moved and not arranging else []):
                        if m != k and m not in moved and m in rects and m not in held \
                                and wins[m][0] not in host_moved:    # (the host moves those;
                            self.shift(m, dx, dy, rects, wins)       #  the layout its own)
                    if not resized:
                        self.moving = k
                        self.still = 0
                elif self.moving is not None:
                    # (2.6.74) still under the mouse: not dropped yet. The settle count
                    # starts once the drag is over, so the snap below comes after the
                    # drop was handled (the host's _tell_moved: the layout's drop, our
                    # on_moved), never before it
                    if not self.in_drag():
                        self.still += 1
                    if self.still >= ANCHOR_SETTLE_POLLS:   # dropped: try to snap
                        k, self.moving = self.moving, None
                        if k in rects and k not in held and not arranging:
                            self.snap(k, rects, wins)       # (2.6.74) it reads the held keys now
                        self.linger = ANCHOR_LINGER_POLLS   # the host may still nudge it
                self.pos = {k: r[:2] for k, r in rects.items()}
                self.dims = {k: r[2:] for k, r in rects.items()}

            def snap(self, k, rects, wins, held=None):
                # (2.6.74) the held keys as they are now, after the drop was handled (the
                # layout may have just slotted k or a group mate), unless the caller
                # has just read them; and never in Arrange mode
                if held is None:
                    held = layout_held_keys()
                if layout_arranging():
                    return
                kx, ky, kw, kh = rects[k]
                group = set(self.members(k))
                if any(m in held for m in group):       # (2.6.58) a zone places its windows
                    return
                best = None                              # (distance, dx, dy, other)
                for o, (ox, oy, ow, oh) in rects.items():
                    if o in group or o in held:
                        continue
                    v_overlap = ky < oy + oh and oy < ky + kh
                    h_overlap = kx < ox + ow and ox < kx + kw
                    cands = []
                    if v_overlap:
                        cands.append((abs(kx - (ox + ow)), ox + ow - kx, 0))   # right of it
                        cands.append((abs(kx + kw - ox), ox - kw - kx, 0))     # left of it
                    if h_overlap:
                        cands.append((abs(ky - (oy + oh)), 0, oy + oh - ky))   # below it
                        cands.append((abs(ky + kh - oy), 0, oy - kh - ky))     # above it
                    for d, dx, dy in cands:
                        if d <= SNAP_DISTANCE and (best is None or d < best[0]):
                            # line up the other edge too when it's close
                            if dx and abs(ky - oy) <= SNAP_DISTANCE:
                                dy = oy - ky
                            if dy and abs(kx - ox) <= SNAP_DISTANCE:
                                dx = ox - kx
                            best = (d, dx, dy, o)
                if best is None:
                    return
                _, dx, dy, o = best
                for m in group:                          # the whole group snaps
                    if m in rects:
                        self.shift(m, dx, dy, rects, wins)
                self.join(k, o)


        ANCHORS = Anchors()


        def pop_listed(k):
            """A "pop:<serial>" window key whose pop-out is still listed (as
            open_windows() would list it)."""
            try:
                return k.startswith("pop:") and int(k[4:]) in POPS
            except Exception:
                return False


        # ------------------------------- STORAGE -------------------------------------
        # The file is never touched on the client thread: while the module runs the
        # load job and the saves run in thread_tick (the script's thread); with the
        # module off (its Settings page) the read and the writes go to a short
        # thread of their own, since no thread_tick runs then. _stop is the one
        # exception (see there). A save is written whole to DATA_FILE + ".tmp" and
        # swapped in, so a crash or a stop mid-write leaves the old file intact
        # instead of an empty one.
        import threading
        FILE_LOCK = threading.Lock()   # one file operation at a time, whichever thread
        SAVE_SEQ = [0]                 # number of the latest save asked for (older ones are skipped)
        SAVE_ERR = [None]              # a failure on the background thread, reported on the next pass
        DATA_READY = [False]           # the save file was read: only then may it be written over
        #                                (a save before that would put an empty foe list over it)


        def in_background(fn):
            """fn() on a short-lived thread of its own: file work with the module off
            (no thread_tick runs then). fn runs here when no thread can be started.
            fn must not call the API (only the tick threads may)."""
            try:
                t = threading.Thread(target=fn)
                t.daemon = True
                t.start()
            except Exception:
                fn()


        def read_save_lines():
            """(path, lines) of the save file (or PlayerTracker's old one); (None, [])
            when there is none. Only the read: parse_save_lines does the rest, so
            this may run on any thread."""
            path = DATA_FILE if os.path.exists(DATA_FILE) else stranded_tmp() or OLD_DATA_FILE
            if not os.path.exists(path):
                return None, []
            with FILE_LOCK:                        # (a save may be swapping the file in)
                with open(path, "r") as f:
                    lines = f.readlines()
            return path, lines


        def load_data():
            """Read and apply the save file (on the script's thread, from the load job)."""
            try:
                path, lines = read_save_lines()
            except Exception as ex:
                API.SysMsg(TITLE + (": couldn't read the save file (%s); nothing is saved "
                                    "this session, so the file is kept as it is." % ex),
                           Kit.HUE_BAD)
                return
            parse_save_lines(path, lines)


        def parse_save_lines(path, lines):
            """Apply the lines of the save file at `path` (None: no file yet)."""
            DATA_READY[0] = True
            if path is None:
                return
            section = None
            links = []                             # (alt, main) as read: checked once FOES is in
            try:
                for raw in lines:
                    try:
                        line = raw.strip()
                        if not line or line.startswith("#"):
                            continue
                        if line.startswith("[") and line.endswith("]"):
                            section = line[1:-1].strip().lower()
                            continue
                        if section == "foes":
                            FOES[name_key(line)] = line
                        elif section == "ignore":
                            IGNORE[line.lower()] = line
                        elif section == "players":
                            PLAYER_NAMES[line.lower()] = line
                            PLAYER_VER[0] += 1
                        elif section == "settings" and "=" in line:
                            key, val = [p.strip().lower() for p in line.split("=", 1)]
                            if key in INT_SETTINGS:
                                UI[key] = clamp(int(val), *INT_SETTINGS[key])
                            elif key in BOOL_SETTINGS:
                                UI[key] = val == "true"
                        elif section == "anchors" and "=" in line:
                            keys = [k.strip().lower() for k in line.split("=", 1)[1].split(",")]
                            keys = [k for k in keys if k in FIXED_WINDOWS]
                            if len(keys) > 1:
                                ANCHORS.add_group(keys)
                        elif section == "layout" and "=" in line:
                            key, val = line.split("=", 1)
                            key = key.strip().lower()
                            parts = [p.strip() for p in val.split(",")]
                            if key in LAYOUT and len(parts) >= 5:
                                LAYOUT[key] = [int(parts[0]), int(parts[1]),
                                               int(parts[2]), int(parts[3]),
                                               parts[4].lower() == "true",
                                               len(parts) > 5 and parts[5].lower() == "true",
                                               clamp(int(parts[6]), 0, 100) if len(parts) > 6
                                               else UI["opacity"]]
                                if key == "combat":
                                    STATE["combat_loaded"] = True
                        # (2.6.05) sections 2.6.04 skips: it doesn't know their names
                        elif section == "sightings":
                            e = parse_sight(line)
                            if e is not None:
                                SIGHTS.append(e)
                                note_seen(e)
                        elif section == "links" and "|" in line:
                            alt, main = line.split("|", 1)
                            links.append((name_key(alt), name_key(main)))
                        elif section == "foe_seen" and "|" in line:
                            p = line.split("|", 5)
                            seen = (float(p[0]), int(p[1]), int(p[2]), int(p[3]),
                                    {"1": True, "0": False}.get(p[4]))
                            k = name_key(p[5])
                            old = LAST_SEEN.get(k)
                            if k and (old is None or old[0] < seen[0]):
                                LAST_SEEN[k] = seen
                    except Exception:
                        continue           # a damaged line: skip it, keep the rest

                trim_sights()
                trim_players()                         # (2.6.81) UT1-5
                for alt, main in links:                # links between entries still on the list
                    if alt != main and alt in FOES and main in FOES:
                        ALT_OF[alt] = main
                flatten_links()
                for key in LAYOUT:                     # saved places: on the screen of today
                    L = LAYOUT[key]
                    L[0], L[1] = Kit.adapt(L[0], L[1], L[2], L[3])
            except Exception as ex:
                API.SysMsg(TITLE + (": couldn't read the save file (%s)." % ex), Kit.HUE_BAD)
            if path == OLD_DATA_FILE:
                for k in ("friend", "foe", "neutral"):     # PlayerTracker had one opacity
                    LAYOUT[k][6] = UI["opacity"]


        def load_old_combat_settings():
            """First run: pick up what CombatBars saved for this character."""
            if STATE["combat_loaded"]:
                return

            def get(key, default):
                try:
                    return int(API.GetPersistentVar(key, str(default), API.PersistentVar.Char))
                except Exception:
                    return default
            L = LAYOUT["combat"]
            L[0], L[1] = get("CombatBars_X", L[0]), get("CombatBars_Y", L[1])
            L[2] = clamp(get("CombatBars_W", L[2]), CB_MIN_WIDTH, CB_MAX_WIDTH)
            L[6] = clamp(get("CombatBars_Opacity", L[6]), 0, 100)
            L[4] = get("CombatBars_Locked", 0) == 1
            L[5] = get("CombatBars_Minimized", 0) == 1
            UI["magery"] = get("CombatBars_Magery", 0) == 1
            STATE["dirty_save"] = True


        def stranded_tmp():
            """(2.6.84) A whole save left as its temporary copy (a swap that failed
            after the old file went), newest first, or None: read instead of
            starting with empty lists (which the first save would write over)."""
            try:
                d = os.path.dirname(DATA_FILE) or "."
                base = os.path.basename(DATA_FILE) + "."
                tmps = [os.path.join(d, n) for n in os.listdir(d)
                        if n.startswith(base) and n.endswith(".tmp")]
            except Exception:
                return None
            best, best_t = None, None
            for t in tmps:
                try:
                    m = os.path.getmtime(t)
                except Exception:
                    continue
                if best_t is None or m > best_t:
                    best, best_t = t, m
            return best


        def write_save_file(text):
            """The file write itself (any thread): whole into a temporary copy, then
            swapped over the old file in one step. (2.6.84) The copy is named per
            process: two clients sharing the folder never write the same one."""
            try:
                tmp = DATA_FILE + ".%d.tmp" % os.getpid()
            except Exception:
                tmp = DATA_FILE + ".tmp"
            with open(tmp, "w") as f:
                f.write(text)
            try:
                os.replace(tmp, DATA_FILE)
            except Exception:                      # no os.replace on this build, or it won't
                try:                               # go over an existing file: the two-step way
                    if os.path.exists(DATA_FILE):
                        os.remove(DATA_FILE)
                    os.rename(tmp, DATA_FILE)
                except Exception:
                    if os.path.exists(DATA_FILE):  # the old file is still there: no half-way
                        try:                       # copy left beside it
                            os.remove(tmp)
                        except Exception:
                            pass
                    raise


        def report_save_error():
            """A failed background write is reported here, on a tick thread."""
            err, SAVE_ERR[0] = SAVE_ERR[0], None
            if err:
                API.SysMsg(TITLE + (": couldn't save (%s)." % err), Kit.HUE_BAD)


        def save_text():
            """The save file's text (lists, settings, anchors, layout), or None when
            the file was never read (a save then would put empty lists over it)."""
            if not DATA_READY[0]:
                return None

            def tf(b):
                return "true" if b else "false"
            try:
                out = ["# UltimaTracker save file - one name per line"]
                # [players]: confirmed players (karma tag seen)
                for sect, names in (("foes", FOES), ("ignore", IGNORE)):
                    out += ["[%s]" % sect] + sorted(names.values(), key=lambda s: s.lower()) + [""]
                # (2.6.82) the confirmed players (up to 5000) are sorted again only
                # after a change (the version is taken before the sort: a change
                # made meanwhile sorts again at the next save)
                ver = PLAYER_VER[0]
                if PLAYER_TEXT[0] != ver or PLAYER_TEXT[1] is None:
                    PLAYER_TEXT[1] = sorted(PLAYER_NAMES.values(), key=lambda s: s.lower())
                    PLAYER_TEXT[0] = ver
                out += ["[players]"] + PLAYER_TEXT[1] + [""]
                out += ["[settings]"] + ["%s=%d" % (k, own_scale() if k == "scale" else UI[k])
                                         for k in INT_ORDER]
                out += ["%s=%s" % (k, tf(UI[k])) for k in BOOL_SETTINGS] + ["", "[anchors]"]
                out += ["group=%s" % ",".join(keys) for keys in ANCHORS.saved_groups()]
                out += ["", "[layout]"] + ["%s=%d,%d,%d,%d,%s,%s,%d" % (
                    k, v[0], v[1], v[2], v[3], tf(v[4]), tf(v[5]), v[6]) for k, v in LAYOUT.items()]
                # (2.6.05) new sections, after the old ones: 2.6.04 skips sections it doesn't
                # know. [links]: "alt|main" (Foe list entries linked as one person);
                # [foe_seen]: "time|facet|x|y|guarded|name" for Foe list names (their last
                # sighting outlives the log); [sightings]: see sight_line
                out += ["", "[links]"] + ["%s|%s" % (FOES[a], FOES[m])
                                          for a, m in sorted(ALT_OF.items())
                                          if a in FOES and m in FOES
                                          and "|" not in FOES[a] + FOES[m]]
                out += ["", "[foe_seen]"] + [seen_line(k) for k in sorted(FOES) if k in LAST_SEEN]
                out += ["", "[sightings]"] + [e[S_LINE] for e in SIGHTS]
                return "\n".join(out) + "\n"
            except Exception as ex:
                API.SysMsg(TITLE + (": couldn't save (%s)." % ex), Kit.HUE_BAD)
                return None


        def write_text(text, seq=None):
            """Write `text` as the save file (any thread; failures are kept for
            report_save_error). With `seq`, skipped when a newer save followed."""
            with FILE_LOCK:
                if seq is not None and seq != SAVE_SEQ[0]:
                    return                         # a newer save is on its way: this one is stale
                try:
                    write_save_file(text)
                except Exception as ex:
                    SAVE_ERR[0] = str(ex)


        def save_data(background=False):
            """Write the save file: here (thread_tick / _stop), or with `background`
            on a thread of its own (the Settings page with the module off). The
            text is made here, on the calling thread; only the write moves."""
            text = save_text()
            if text is None:
                return
            STATE["dirty_save"] = False
            SIGHT["dirty"] = False                 # (the sightings went with this text)
            SAVE_SEQ[0] += 1
            seq = SAVE_SEQ[0]

            def write():
                write_text(text, seq)
            if background:
                in_background(write)
            else:
                write()
                report_save_error()


        # --------------------- SIGHTINGS, LINKS, NOTES (2.6.05) ----------------------
        #  A sighting: [time, serial, notoriety, facet, x, y, guarded (True / False /
        #  None), name, name key, its save-file line]. The line is made once, when the
        #  sighting is logged (or read), so a save only joins the lines.
        S_T, S_SERIAL, S_NOTO, S_FACET, S_X, S_Y, S_GUARD, S_NAME, S_KEY, S_LINE = range(10)
        GUARD_CH = {True: "1", False: "0", None: "-"}
        GUARD_OF = {"1": True, "0": False}
        COMPASS = ("E", "SE", "S", "SW", "W", "NW", "N", "NE")   # clockwise from east (y grows south)


        def sight_line(t, serial, noto, facet, x, y, guard, name):
            """"time|serial|notoriety|facet|x|y|guarded|name" (guarded: 1, 0 or -)."""
            return "%d|%d|%s|%d|%d|%d|%s|%s" % (int(t), int(serial), noto, int(facet), int(x),
                                                int(y), GUARD_CH.get(guard, "-"), name)


        def parse_sight(line):
            p = line.split("|", 7)
            if len(p) < 8 or not p[7]:
                return None
            return [float(p[0]), int(p[1]), p[2] or "unknown", int(p[3]), int(p[4]), int(p[5]),
                    GUARD_OF.get(p[6]), p[7], name_key(p[7]), line]


        def note_seen(e):
            """A sighting is the newest of its name: LAST_SEEN follows (True when
            that name is on the Foe list, whose rows show it)."""
            k = e[S_KEY]
            old = LAST_SEEN.get(k)
            if old is not None and old[0] > e[S_T]:
                return False
            LAST_SEEN[k] = (e[S_T], e[S_FACET], e[S_X], e[S_Y], e[S_GUARD])
            return k in FOES


        def seen_line(k):
            t, facet, x, y, guard = LAST_SEEN[k]
            return "%d|%d|%d|%d|%s|%s" % (int(t), facet, x, y, GUARD_CH.get(guard, "-"), FOES[k])


        def trim_sights():
            """The cap: past SIGHT_CAP + SIGHT_SLACK sightings the oldest go (in one
            cut, not one per new line). LAST_SEEN is rebuilt from what's left (and
            the Foe list's own entries) when it has grown well past the log."""
            n = len(SIGHTS)
            if n > SIGHT_CAP + SIGHT_SLACK:
                del SIGHTS[:n - SIGHT_CAP]
            if len(LAST_SEEN) > 2 * SIGHT_CAP:
                keep = dict((k, v) for k, v in LAST_SEEN.items() if k in FOES)
                LAST_SEEN.clear()
                LAST_SEEN.update(keep)
                for e in SIGHTS:
                    note_seen(e)


        def log_sighting(t, serial, name, noto, facet, x, y, guard):
            line = sight_line(t, serial, noto, facet, x, y, guard, name)
            e = [float(int(t)), serial, noto, facet, x, y, guard, name, name_key(name), line]
            SIGHTS.append(e)
            trim_sights()
            if note_seen(e):
                SIGHT["seen_ver"] += 1
            SIGHT["ver"] += 1
            if not SIGHT["dirty"]:
                SIGHT["dirty"] = True
                SIGHT["save_at"] = t + SIGHT_SAVE_SECONDS


        def noto_word(noto):
            return NOTO_WORD.get(noto, noto or "unknown")


        def compass(dx, dy):
            if not dx and not dy:
                return ""
            return COMPASS[int(round(math.atan2(dy, dx) / (math.pi / 4))) % 8]


        def ago(t, now):
            d = max(0, int(now - t))
            if d < 60:
                return "just now"
            if d < 3600:
                return "%dm ago" % (d // 60)
            if d < 86400:
                return "%dh ago" % (d // 3600)
            return "%dd ago" % (d // 86400)


        def place_text(facet, x, y):
            f = FACETS.get(facet)
            if f is None:
                f = "map %d" % facet if facet >= 0 else "?"
            return "%s %d,%d" % (f, x, y)


        def today_start(now):
            lt = time.localtime(now)
            return now - (lt.tm_hour * 3600 + lt.tm_min * 60 + lt.tm_sec)


        def stamp(t, today0):
            """Clock time of a sighting; the date too when it wasn't today."""
            try:
                return time.strftime("%H:%M" if t >= today0 else "%m/%d %H:%M", time.localtime(t))
            except Exception:
                return "?"


        def seen_text(k, now):
            """'seen 5m ago, Fel 1432,1690 (guarded)' for a Foe list name."""
            s = LAST_SEEN.get(k)
            if s is None:
                return "not seen yet"
            t, facet, x, y, guard = s
            return "seen %s, %s%s" % (ago(t, now), place_text(facet, x, y),
                                      " (guarded)" if guard else "")


        # ----- Foe list links: one person, several characters -----
        def flatten_links():
            """Every alt points straight at its group's main entry (which is no
            one's alt); a loop in a damaged file is broken."""
            for alt in list(ALT_OF):
                m, n = ALT_OF.get(alt), 0
                while m in ALT_OF and n < 10:
                    m, n = ALT_OF[m], n + 1
                if m is None or m == alt or m in ALT_OF:
                    ALT_OF.pop(alt, None)
                else:
                    ALT_OF[alt] = m


        def alts_of(main):
            return sorted(a for a, m in ALT_OF.items() if m == main)


        def link_text(k):
            """'alt of Main', 'alts: A, B' or '' for a Foe list name key."""
            m = ALT_OF.get(k)
            if m is not None:
                return "alt of " + FOES.get(m, m)
            alts = alts_of(k)
            if alts:
                return "alts: " + ", ".join(FOES.get(a, a) for a in alts)
            return ""


        def link_foes(a, b):
            """b (and its alts) become alts of a's person. Returns a journal line."""
            main = ALT_OF.get(a, a)
            if b == main or ALT_OF.get(b) == main:
                return "%s and %s are already linked." % (FOES.get(a, a), FOES.get(b, b))
            old = ALT_OF.get(b, b)              # b's own person: all of it joins
            for k in list(ALT_OF):
                if ALT_OF[k] == old:
                    ALT_OF[k] = main
            if old != main:
                ALT_OF[old] = main
            ALT_OF[b] = main
            ALT_OF.pop(main, None)
            flatten_links()
            return "linked %s as an alt of %s." % (FOES.get(b, b), FOES.get(main, main))


        def unlink_foe(k):
            """Take k out of its group (a main hands the group to its first alt)."""
            if k in ALT_OF:
                del ALT_OF[k]
                return True
            alts = alts_of(k)
            if not alts:
                return False
            new = alts[0]
            del ALT_OF[new]
            for a in alts[1:]:
                ALT_OF[a] = new
            return True


        # ----- Social's notes on players (optional; one call per tooltip) -----
        NOTE_CACHE = {}      # (2.6.82) name -> (asked at, note): rows changing hands in a crowd
        NOTE_TTL = 10.0      # ask Social again after this long (an edited note shows by then)


        def social_note(name):
            fn = HOST.services.get("social.note")
            if fn is None or not name:
                return ""
            now = time.time()
            hit = NOTE_CACHE.get(name)
            if hit is not None and 0.0 <= now - hit[0] < NOTE_TTL:
                return hit[1]
            try:
                n = str(fn(name) or "").strip()
            except Exception:
                return ""
            n = n if len(n) <= NOTE_MAX else n[:NOTE_MAX - 2] + ".."
            if len(NOTE_CACHE) > 500:
                NOTE_CACHE.clear()
            NOTE_CACHE[name] = (now, n)
            return n


        def tip_for(tip, name, extra=""):
            """A row's tooltip: the base text, then what's known of that player
            (Foe list link, Social's note). Built when the row changes hands."""
            lines = [tip]
            if extra:
                lines.insert(0, extra)
            lk = link_text(name_key(name)) if name else ""
            if lk:
                lines.insert(0, lk[0].upper() + lk[1:])
            n = social_note(name)
            if n:
                lines.append("Note: " + n)
            return "\n".join(lines)


        # ----- the Foe list, from every place that adds to it -----
        def add_foe(name):
            """Put a name on the Foe list (the panel, Target Foe, the death window)."""
            FOES[name_key(name)] = name
            STATE["foe_ver"] += 1
            request_save()


        def is_foe(serial=None, name=None):
            """HOST.services["ultima.is_foe"](serial, name): True when that player
            is on your Foe list, by name (case-insensitive, Lord / Lady dropped) or
            by serial (a player seen under a Foe list name, or the mobile's name)."""
            if name:
                k = name_key(str(name))
                if k and k in FOES:
                    return True
            if serial is None:
                return False
            try:
                s = int(serial)
            except Exception:
                return False
            k = FOE_SERIALS.get(s)
            if k is not None and k in FOES:
                return True
            if not name:
                try:
                    m = API.FindMobile(s)
                    k = name_key(str(m.Name or "")) if m is not None else ""
                except Exception:
                    k = ""
                return bool(k) and k in FOES
            return False


        # ------------------------------- SCANNING ------------------------------------
        # (NPC_CACHE, SEEN_PLAYER and TITLED_NPCS are emptied past CACHE_CAP entries)
        NPC_CACHE = {}     # serial -> (is_npc, last checked)
        SEEN_PLAYER = set()  # serials that have acted like players
        PLAYER_NAMES = {}    # lowercase name -> name: confirmed players (saved)
        PLAYER_VER = [0]     # (2.6.82) bumped on every change of PLAYER_NAMES (save_text's cache)
        PLAYER_TEXT = [None, None]   # (version, its sorted [players] lines)
        TITLED_NPCS = set()  # lowercase names that announced an NPC title
        TITLE_CACHE = {}     # (2.6.81) serial -> (name line shows a title, last checked)
        KARMA_TAG_RE = re.compile(r"^\s*\[[^\]]+\]\s*$")   # "[Dubious]" on a single-click


        def trim_players(limit=None):
            """(2.6.81) UT1-5: past `limit` (PLAYER_NAMES_CAP) names, fold PLAYER_NAMES
            to PLAYER_NAMES_KEEP; names on the Foe list or the ignore list go last
            (the save keeps no order, so any other name may go)."""
            if len(PLAYER_NAMES) <= (PLAYER_NAMES_CAP if limit is None else limit):
                return
            drop = len(PLAYER_NAMES) - PLAYER_NAMES_KEEP
            later = []
            for low, name in list(PLAYER_NAMES.items()):
                if drop <= 0:
                    break
                if low in IGNORE or name_key(name) in FOES:
                    later.append(low)
                    continue
                del PLAYER_NAMES[low]
                drop -= 1
            for low in later:
                if drop <= 0:
                    break
                del PLAYER_NAMES[low]
                drop -= 1
            PLAYER_VER[0] += 1
            NPC_CACHE.clear()
            STATE["dirty_save"] = True


        def capped(cache):
            """Empty a per-mobile cache once it has grown past CACHE_CAP entries."""
            if len(cache) > CACHE_CAP:
                cache.clear()


        JOURNAL_NEXT = [0.0]
        JREAD = {"learn": None, "attack": None, "killer": None}   # our readers of the shared Journal


        def learn_from_journal():
            """Single-clicking someone prints their name label in the journal:
            players show a karma/fame tag ("Draxt: [Dubious]"), titled NPCs their
            job ("Melia: Melia the town crier"). Remember both. (Looked at once a
            second: the lines the shared Journal got since the last look.)"""
            now = time.time()
            if now < JOURNAL_NEXT[0]:
                return
            JOURNAL_NEXT[0] = now + 1.0
            rd = JREAD["learn"]
            if rd is None:
                rd = JREAD["learn"] = Journal.reader()
            for ln in rd.new():
                name = ln.name.strip()
                text = ln.text.strip()
                if not name and ": " in text:                  # "Name: text" in one string
                    name, text = [s.strip() for s in text.split(": ", 1)]
                if not name or not text:
                    continue
                low = name.lower()
                if KARMA_TAG_RE.match(text):
                    if low not in PLAYER_NAMES:
                        if len(PLAYER_NAMES) >= PLAYER_NAMES_CAP:
                            trim_players(PLAYER_NAMES_CAP - 1)   # (2.6.81) UT1-5
                        PLAYER_NAMES[low] = name
                        PLAYER_VER[0] += 1
                        STATE["dirty_save"] = True
                        NPC_CACHE.clear()
                elif text.lower().startswith(low + " the "):
                    capped(TITLED_NPCS)
                    TITLED_NPCS.add(low)


        FRIEND_Q = {}        # serial -> API.IsFriend's answer (kept FRIEND_Q_SECONDS)
        FRIEND_Q_SECONDS = 1.0   # (2.6.82) the friends-list answers are asked again after this
        FRIEND_Q_AT = [0.0]      # when FRIEND_Q is next emptied (by the scan)


        def is_friend(serial):
            v = FRIEND_Q.get(serial)
            if v is None:
                try:
                    v = bool(API.IsFriend(serial))
                except Exception:
                    v = False
                if len(FRIEND_Q) > 500:
                    FRIEND_Q.clear()
                FRIEND_Q[serial] = v
            return v


        def mflag(m, attr):
            """A mobile's on / off property, False when it can't be read."""
            try:
                return bool(getattr(m, attr))
            except Exception:
                return False


        def acts_like_player(mob, serial, name, low):
            """Things town NPCs don't do: run, ride, go to war mode, carry a
            Lord/Lady title, or be on your party / friends / Foe list.
            (2.6.82) low = name.strip().lower(); the pure-Python tests first, then
            the client's flags, the friends list last (the same OR of the same tests)."""
            if low.startswith(TITLE_PREFIXES) or name_key(name) in FOES or low in PLAYER_NAMES \
                    or serial in STATE["party"]:
                return True
            if mflag(mob, "IsRunning") or mflag(mob, "IsMounted") or mflag(mob, "InWarMode"):
                return True
            return is_friend(serial)


        def is_npc(mob, serial, name):
            """Blue town NPCs: either a job title in the name line ("Bob the guard",
            when the shard sends titles) or a plain first name from the server's NPC
            name lists ("Candra", "Thierry"). Anything seen acting like a player is
            remembered as a player for the rest of the session.
            (2.6.82) serial and name (str) as the caller read them."""
            if serial in SEEN_PLAYER:
                return False
            low = name.strip().lower()
            if acts_like_player(mob, serial, name, low):
                capped(SEEN_PLAYER)
                SEEN_PLAYER.add(serial)
                NPC_CACHE.pop(serial, None)
                return False
            if low in npc_names() or low in TITLED_NPCS:
                return True
            now = time.time()
            hit = NPC_CACHE.get(serial)
            if hit is not None and (hit[0] or now - hit[1] < NPC_RECHECK_SECONDS):
                return hit[0]
            # the title (when sent) can arrive a moment after the mobile; re-check
            text = name_props(mob, serial)
            npc = bool(NPC_TITLE_RE.search(text.split("\n")[0] + " " + name))
            capped(NPC_CACHE)
            NPC_CACHE[serial] = (npc, now)
            return npc


        NAME_PROPS_HOW = [None]   # how a mobile's name line is read on this build (see name_props)


        def name_props(mob, serial):
            """The mobile's name-and-title line ("Bob the guard") as the client has
            it now, "" when it can't be read; never waits for the server. Reads
            mob.NameAndProps(False) when the build's mobiles have it, else the
            documented API.ItemNameAndProps(serial, False) (the first time one of
            them is missing is remembered, so it isn't tried again per mobile)."""
            how = NAME_PROPS_HOW[0]
            if how != "api":
                try:
                    raw = mob.raw                       # (2.6.82) a shared per-pass mobile
                except Exception:
                    raw = mob
                try:
                    text = raw.NameAndProps(False)
                    NAME_PROPS_HOW[0] = "mob"
                    return str(text or "")
                except AttributeError:
                    NAME_PROPS_HOW[0] = "api"          # not on this build: the API call instead
                except Exception:
                    return ""
            try:
                return str(API.ItemNameAndProps(serial, False) or "")
            except Exception:
                return ""


        def titled_npc(mob, serial, name):
            """(2.6.81) UT1-1: a red / grey / orange human that is an NPC by its
            title (brigands, executioners, the shard's grey wandering healers):
            its name announced "<name> the <job>" on a single-click (TITLED_NPCS),
            or the client's name line already shows such a title after the name.
            Never by a plain first name (NPC_NAMES), war mode or running: a real
            red player must never be hidden from the Foes tracker and its alert,
            and a known player (Foe list, party, friends, a karma tag seen, acted
            like a player) never is. (2.6.82) serial and name (str) as the caller
            read them."""
            if serial in SEEN_PLAYER:
                return False
            low = name.strip().lower()
            if not low:
                return False
            npc = low in TITLED_NPCS
            if not npc:
                now = time.time()
                hit = TITLE_CACHE.get(serial)
                if hit is not None and (hit[0] or now - hit[1] < NPC_RECHECK_SECONDS):
                    npc = hit[0]
                else:
                    # the title must come after the mobile's own name, so a player
                    # whose name itself holds " the " is never taken for an NPC
                    first = name_props(mob, serial).split("\n")[0].strip().lower()
                    npc = first.startswith(low + " the ")
                    capped(TITLE_CACHE)
                    TITLE_CACHE[serial] = (npc, now)
            if not npc:
                return False
            if low in PLAYER_NAMES or name_key(name) in FOES or serial in STATE["party"] \
                    or is_friend(serial):
                return False
            return True


        def looks_like_player(mob, serial):
            """(notoriety, dead, name) when mob looks like a player, else None (read
            once here and reused by the caller; name is str(mob.Name or "")).
            (2.6.82) the cheap body test first: a monster or an animal costs three
            reads, and only a human / gargoyle / ghost reaches the NPC tests (the
            same answer for every mobile as before)."""
            dead = mflag(mob, "IsDead")
            if not dead and not (mflag(mob, "IsHuman") or mflag(mob, "IsGargoyle")):
                return None
            if dead and not SHOW_GHOSTS:
                return None
            if mflag(mob, "IsRenamable"):                         # your pets/hirelings
                return None
            noto = noto_name(mob)
            if noto == "invulnerable":                            # vendors/healers
                return None
            try:
                name = str(mob.Name or "")
            except Exception:
                return None                                       # (unreadable: never listed)
            if AUTO_HIDE_NPCS:
                if noto == "innocent":
                    if is_npc(mob, serial, name):
                        return None                               # guards, criers, escorts...
                # (2.6.81) UT1-1: red / grey human NPCs by their title (the innocent
                # ones went through is_npc above); a ghost is always a player
                elif not dead and titled_npc(mob, serial, name):
                    return None
            return (noto, dead, name)


        def classify(serial, name, noto, party):
            key = name_key(name)
            if key and key in FOES:
                return "foe", "L"                                 # saved Foe list
            if serial in party:
                return "friend", "P"
            if is_friend(serial):
                return "friend", "F"
            if noto == "ally":
                return "friend", "G"                              # guild / alliance
            if noto == "murderer":
                return "foe", ""
            if noto == "enemy" and FOE_INCLUDE_WAR_ENEMIES:
                return "foe", "W"
            if noto in ("criminal", "gray") and FOE_INCLUDE_CRIMINALS:
                return "foe", "C"
            return "neutral", ""


        def classify_service(mob, party=None, with_dead=False):
            """HOST.services["ultima.classify"](mob, party=None) (2.6.06): how the
            trackers see a mobile. None when it isn't a player they would list (an
            NPC, a pet, a vendor, an empty serial) or is on the ignore list; else
            (category, tag, notoriety): category "friend" / "foe" / "neutral", tag
            as on the rows ("P" party, "F" friends list, "G" guild or alliance, "L"
            Foe list, "W" war enemy, "C" criminal, "" none), notoriety the client's
            word for it ("innocent", "murderer", ...). mob may be a serial. party:
            the party serials if the caller has them (else the trackers' last scan).
            with_dead (2.6.82, Lookout): a fourth item, the mobile is a ghost.
            Reads only what the client already has: no waits on the client thread."""
            try:
                if mob is None:
                    return None
                try:
                    serial = mob.Serial
                except AttributeError:                            # a serial
                    mob = API.FindMobile(int(mob))
                    if mob is None:
                        return None
                    serial = mob.Serial
                seen = looks_like_player(mob, serial)
                if seen is None:
                    return None
                noto, dead, name = seen
                if name and name.lower() in IGNORE:
                    return None
                cat, tag = classify(serial, name, noto, STATE["party"] if party is None else party)
                if with_dead:
                    return cat, tag, noto, dead
                return cat, tag, noto
            except Exception:
                return None


        # (2.6.82) the mother's shared per-pass reads (one read per pass for every
        # module, on the client thread); on an older mother the API itself
        HOST_ME = getattr(HOST, "me", None)
        HOST_MOBILES = getattr(HOST, "mobiles", None)
        HOST_MOBILE = getattr(HOST, "mobile", None)


        def player():
            """The player (HOST.me(): read once per pass), None when not in game."""
            if HOST_ME is not None:
                try:
                    return HOST_ME()
                except Exception:
                    pass
            return API.Player


        def mobiles_within(d):
            """Every mobile within d tiles, nearest first (HOST.mobiles: one list
            per pass shared by every module), [] when it can't be read."""
            if HOST_MOBILES is not None:
                try:
                    return HOST_MOBILES(distance=d)
                except Exception:
                    pass
            try:
                return list(API.GetAllMobiles(distance=d) or [])
            except Exception:
                return []


        def mobile_seen(serial):
            """The client still knows that mobile (HOST.mobile: per-pass memo);
            False when it can't be asked (as before)."""
            if HOST_MOBILE is not None:
                try:
                    return HOST_MOBILE(serial) is not None
                except Exception:
                    pass
            try:
                return API.FindMobile(serial) is not None
            except Exception:
                return False


        def find_mobile(serial):
            """API.FindMobile(serial) (HOST.mobile: per-pass memo, for reads only)."""
            if HOST_MOBILE is not None:
                try:
                    return HOST_MOBILE(serial)
                except Exception:
                    pass
            return API.FindMobile(serial)


        MOBS = {"t": 0.0, "list": []}


        def mobiles_near():
            """Every mobile the client knows within the larger of the tracking and
            combat ranges; callers filter by distance. (2.6.82) the mother's
            per-pass list when it has one (shared by the scan, the attack lines and
            every other module that pass), else fetched at most ten times a second."""
            rng = max(UI["range"], MAX_RANGE)
            if HOST_MOBILES is not None:
                return mobiles_within(rng)
            now = time.time()
            if now - MOBS["t"] > MOBS_EVERY:
                MOBS["list"] = mobiles_within(rng)
                MOBS["t"] = now
            return MOBS["list"]


        def mnum(m, attr):
            """A mobile's number (hits...), 0 when it can't be read."""
            try:
                return getattr(m, attr) or 0
            except Exception:
                return 0


        def _by_name(e):
            return e["name"].lower()


        SCANNED = {}         # (2.6.82) serial -> what this scan read of a listed player (PopBar)
        SCANNED_PASS = [None]   # the mother's pass it was read in (None: not in the client hop)


        def scanned(serial):
            """(2.6.82) What this pass's scan read of a listed player, else None."""
            if SCANNED_PASS[0] is None or not getattr(HOST, "in_hop", False) \
                    or HOST.pass_id != SCANNED_PASS[0]:
                return None
            return SCANNED.get(serial)


        def scan():
            out = {c: [] for c in CATS}
            SCANNED.clear()
            SCANNED_PASS[0] = HOST.pass_id if getattr(HOST, "in_hop", False) else None
            now = time.time()
            if not 0.0 < FRIEND_Q_AT[0] - now <= FRIEND_Q_SECONDS:   # (2.6.82) answers: kept 1 s
                FRIEND_Q.clear()
                FRIEND_Q_AT[0] = now + FRIEND_Q_SECONDS
            me = player()
            WATCH["me"] = me                       # (for watch_tick, right after: read once)
            if me is None:
                return out
            rng = UI["range"]
            mobs = mobiles_near()
            try:
                party = set(API.GetPartyMemberSerials() or [])
            except Exception:
                party = set()
            STATE["party"] = party
            learn_from_journal()
            my_serial = me.Serial
            try:
                mx, my = int(me.X), int(me.Y)          # read once, not once per mobile
            except Exception:
                return out
            # (2.6.05) who counts for the foe alert, and players appearing (sightings)
            alert_on = UI["alert_red"] or UI["alert_foes"] or UI["alert_orange"] or UI["alert_gray"]
            cands = None                           # serials that count for the alert this scan
            fresh = None                           # (serial, name, noto, tag, dist, x, y) new to it
            appeared = None                        # (serial, name, noto, x, y) new in range
            foes_here = None                       # (name key, x, y) of Foe list players here
            log_on = UI["sightings"]
            # (2.6.82) HP and status only for the trackers that show rows: a
            # minimized (or folded) tracker shows only its count
            wins = M["windows"] or {}
            need_hp = {}
            for c in CATS:
                w = wins.get(c)
                need_hp[c] = w is None or not (w.minimized and LAYOUT[c][5])
            for m in mobs:
                try:
                    if m is None:
                        continue
                    serial = m.Serial
                    if serial == my_serial:
                        continue
                    ox, oy = int(m.X), int(m.Y)
                    dist = max(abs(ox - mx), abs(oy - my))
                    if dist > rng:
                        continue
                    seen = looks_like_player(m, serial)
                    if seen is None:
                        continue
                    noto, dead, name = seen
                    if name and name.lower() in IGNORE:
                        continue
                    cat, tag = classify(serial, name, noto, party)
                    if cat != "friend" and name:
                        if tag == "L":
                            k = name_key(name)
                            if FOE_SERIALS.get(serial) != k:
                                capped(FOE_SERIALS)
                                FOE_SERIALS[serial] = k
                            if foes_here is None:
                                foes_here = []
                            foes_here.append((k, ox, oy))
                        if log_on:
                            t0 = PRESENT.get(serial)
                            if t0 is None or now - t0 > SIGHT_GONE:
                                if appeared is None:
                                    appeared = []
                                appeared.append((serial, name, noto, ox, oy))
                            PRESENT[serial] = now
                        if alert_on and not dead and alert_why(tag, noto) is not None:
                            if cands is None:
                                cands = set()
                            cands.add(serial)
                            if serial not in ALERT_PREV:
                                if fresh is None:
                                    fresh = []
                                fresh.append((serial, name, noto, tag, dist, ox - mx, oy - my))
                    if need_hp[cat]:
                        try:                               # one go; each on its own if one fails
                            hits, hmax = m.Hits or 0, m.HitsMax or 0
                            psn, par = bool(m.IsPoisoned), bool(m.IsParalyzed)
                        except Exception:
                            hits, hmax = mnum(m, "Hits"), mnum(m, "HitsMax")
                            psn, par = mflag(m, "IsPoisoned"), mflag(m, "IsParalyzed")
                        if len(SCANNED) < CACHE_CAP:
                            SCANNED[serial] = (name, noto, cat, dead, psn, par, hits, hmax, dist)
                    else:
                        hits = hmax = 0
                        psn = par = False
                    out[cat].append({
                        "serial": serial,
                        "name": name or "(unknown)",
                        "tag": tag,
                        "noto": noto,
                        "hits": hits,
                        "hmax": hmax,
                        "dist": dist,
                        "poisoned": psn,
                        "paralyzed": par,
                        "dead": dead,
                    })
                except Exception:
                    continue
            for c in CATS:
                out[c].sort(key=_by_name)
            # (2.6.05) nothing to do here unless someone new turned up; a failure
            # here is reported and never stops the trackers' own update
            try:
                if cands is None:
                    if ALERT_PREV:
                        ALERT_PREV.clear()
                else:
                    ALERT_PREV.clear()
                    ALERT_PREV.update(cands)
                if foes_here is not None:
                    foes_seen(foes_here, now)
                if fresh is not None:
                    foe_alerts(fresh, now)
                if appeared is not None:
                    log_appeared(appeared, now)
            except Exception as ex:
                report_error(ex)
            return out


        # ------------------------- FOE ALERT (2.6.05) ---------------------------------
        def alert_why(tag, noto):
            """Why a player counts for the foe alert ("foe", "red", "orange", "gray"),
            or None, by the choices on the Settings page."""
            if tag == "L" and UI["alert_foes"]:
                return "foe"
            if noto == "murderer" and UI["alert_red"]:
                return "red"
            if noto == "enemy" and UI["alert_orange"]:
                return "orange"
            if (noto == "gray" or noto == "criminal") and UI["alert_gray"]:
                return "gray"
            return None


        def foe_alerts(fresh, now):
            """Players who just started to count for the alert (came into range, or
            turned red...): one alert each, once per player per alert_minutes."""
            gap = UI["alert_minutes"] * 60.0
            for serial, name, noto, tag, dist, dx, dy in fresh:
                t = ALERTED.get(serial)
                if t is not None and now - t < gap:
                    continue
                ALERTED[serial] = now
                raise_foe_alert(name, noto, tag, dist, dx, dy, serial)


        def foe_alert_text(name, noto, tag, dist, dx, dy):
            """'Killer: red, 7 tiles NE'; a Foe list entry also says so, and names
            its linked characters ('Bob (alt of Killer): blue, on your Foe list, ...')."""
            lk = link_text(name_key(name)) if tag == "L" else ""
            who = "%s (%s)" % (name, lk) if lk else name
            what = noto_word(noto) + (", on your Foe list" if tag == "L" else "")
            if dist <= 0:
                where = "right here"
            else:
                where = "%d tile%s %s" % (dist, "" if dist == 1 else "s", compass(dx, dy))
            return "%s: %s, %s" % (who, what, where.rstrip())


        def raise_foe_alert(name, noto, tag, dist, dx, dy, serial):
            text = foe_alert_text(name, noto, tag, dist, dx, dy)
            fn = getattr(HOST, "alert", None)
            if fn is not None:                     # banner, the chosen sound, a journal line
                fn(ALERT_KEY, text, level=ALERT_LEVEL, who=serial)
            else:                                  # a Virtue Assistant without alerts
                API.SysMsg(TITLE + ": " + text + ".", Kit.HUE_BAD)
                safe(lambda: API.PlaySound(ALERT_SOUND))


        # ------------------------- SIGHTINGS (2.6.05) ---------------------------------
        def map_now():
            try:
                return int(API.GetMap())
            except Exception:
                return -1


        def guard_now():
            """HOST.guarded(): True / False / None (None also on a host without it)."""
            g = getattr(HOST, "guarded", None)
            if g is None:
                return None
            try:
                return g()
            except Exception:
                return None


        # (2.6.81) UT1-2: the pending attack confirm, shared by the player bars'
        # double-click and the combat bars' click
        ATTACK_CONFIRM = {"serial": None, "t": 0.0}


        def attack_hold(serial, mob, now):
            """Before a pressed attack (R6): None = attack now; "warn" = hold it and
            tell the player to press again (the first press, stored); "quiet" = hold
            it and say nothing (the replayed second click of a double-click, within
            ATTACK_CONFIRM_MIN of the first). Only a blue / green mobile while the
            guard zone is True or unknown is held."""
            c = ATTACK_CONFIRM
            noto = noto_name(mob) if mob is not None else "unknown"
            if noto not in FRIENDLY_NOTO or guard_now() is False:
                c["serial"] = None
                return None
            if c["serial"] == serial:
                age = now - c["t"]
                if 0.0 <= age <= ATTACK_CONFIRM_MIN:
                    return "quiet"                 # (keep the time of the first press)
                if age <= ATTACK_CONFIRM_SECONDS:
                    c["serial"] = None             # confirmed
                    return None
            c["serial"], c["t"] = serial, now
            return "warn"


        def attack_warn_text(mob, name, again, verb="attack"):
            """The journal line of a held attack: "<name> is blue and you are (may be)
            in a guard zone: <again> to attack."."""
            colour = "green" if noto_name(mob) == "ally" else "blue"
            where = "are" if guard_now() is True else "may be"
            return TITLE + (": %s is %s and you %s in a guard zone: %s to %s."
                            % (name, colour, where, again, verb))


        def log_appeared(appeared, now):
            """Players (not friends) who came into range: one line each in the log,
            with the facet, where they stood and whether you are in a guard zone."""
            facet, guard = map_now(), guard_now()
            for serial, name, noto, x, y in appeared:
                log_sighting(now, serial, name, noto, facet, x, y, guard)


        FOE_WHERE = [-10.0, -1, None]   # (2.6.82) (when, facet, guard zone) for foes_seen


        def foes_seen(here, now):
            """Foe list players in range: their "last seen" is now, where they stand
            (kept with the Foe list, the log on or off). The panel's rows are told
            when one turns up, not on every scan."""
            facet = guard = None
            for k, x, y in here:
                old = LAST_SEEN.get(k)
                if facet is None:
                    # (2.6.82) the facet and guard zone: looked at once a second here
                    fg = FOE_WHERE
                    f = map_now()                # (2.6.83) a facet change is never kept
                    if f != fg[1] or not 0.0 <= now - fg[0] < 1.0:
                        fg[0], fg[1], fg[2] = now, f, guard_now()
                    facet, guard = fg[1], fg[2]
                LAST_SEEN[k] = (now, facet, x, y, guard)
                if old is None or now - old[0] > SIGHT_GONE:
                    SIGHT["seen_ver"] += 1
                    if not SIGHT["dirty"]:
                        SIGHT["dirty"] = True
                        SIGHT["save_at"] = now + SIGHT_SAVE_SECONDS


        # ----------------------- DEATHS: "Add my killer" (2.6.05) ---------------------
        WATCH = {"dead": None, "prune_at": 0.0,
                 "me": None,            # the player as the scan just read it
                 "att_at": 0.0,         # the attack lines are read once a second (and on a death)
                 "died_at": 0.0}        # attacks before your last death don't count for the next


        def watch_tick(now):
            """After each scan (client thread): who is attacking you, your death and
            resurrection (the death window), and the session lists' pruning."""
            if now >= WATCH["prune_at"]:
                WATCH["prune_at"] = now + 10.0
                prune_session(now)
            me = WATCH["me"]
            dead = mflag(me, "IsDead") if me is not None else WATCH["dead"]
            was, WATCH["dead"] = WATCH["dead"], dead
            if UI["killer"] and (now >= WATCH["att_at"] or (dead and was is False)):
                WATCH["att_at"] = now + 1.0
                note_attackers(now)
            if was is None or dead is None or dead == was:
                return
            if dead:
                on_death(now)
            else:
                KILLER_WIN.close()                 # resurrected


        def note_attackers(now):
            """The "<name> is attacking you" lines since the last look, and the
            players on the combat bars."""
            rd = JREAD["killer"]
            if rd is None:
                JREAD["killer"] = Journal.reader()
                return
            dbg = UI["say_attackers"]
            todo = None                            # (line, name: None = not an attack line)
            lows = None                            # the names in them: one look at the mobiles
            for ln in rd.new():
                if ln.text.startswith(OWN_PREFIX):
                    continue                       # (our own lines, the debug ones too)
                if "is attacking you" not in ln.low:
                    if dbg and "attack" in ln.low:
                        if todo is None:
                            todo = []
                        todo.append((ln, None))
                    continue
                mt = ATTACK_RE.search(ln.text)
                name = mt.group(1).strip().strip("*").strip() if mt is not None else ""
                if todo is None:
                    todo = []
                todo.append((ln, name))
                if name:
                    if lows is None:
                        lows = set()
                    lows.add(name.lower())
            found = named_mobiles(lows) if lows else None
            for ln, name in (todo or ()):
                if name is None:
                    API.SysMsg(TITLE + (": (debug) not an attack line: \"%s\"." % ln.text),
                               Kit.HUE_INFO)
                    continue
                if not name:
                    if dbg:
                        API.SysMsg(TITLE + (": (debug) no name in \"%s\"." % ln.text),
                                   Kit.HUE_INFO)
                    continue
                serial, player = find_named(name, found)
                if player is not False:
                    note_attacker(name, ln.at, serial)
                if dbg:
                    API.SysMsg(TITLE + (": (debug) attack line \"%s\" names %s%s."
                                        % (ln.text, name, " (not a player: left out)"
                                           if player is False else "")), Kit.HUE_INFO)
            if cb_engaged:
                for s, e in cb_engaged.items():
                    m = cb_snap.get(s)
                    if m is None:
                        continue
                    who = e.get("player")           # (2.6.82) its body, once per bar
                    if who is None:
                        who = e["player"] = not mflag(m, "IsRenamable") and \
                            (mflag(m, "IsHuman") or mflag(m, "IsGargoyle"))
                    if who:
                        try:
                            name = str(m.Name or "")
                        except Exception:
                            name = ""
                        if name and note_attacker(name, e["last"], s) and dbg:
                            API.SysMsg(TITLE + (": (debug) on the combat bars: %s." % name),
                                       Kit.HUE_INFO)


        def named_mobiles(lows):
            """{lower-case name: (serial, looks like a player)} of the first mobile
            in sight with each of the names in `lows`: one pass over the mobiles
            however many names are asked for."""
            out = {}
            for m in mobiles_near():
                try:
                    n = m.Name
                    if not n:
                        continue
                    low = n.strip().lower()
                    if low not in lows or low in out:
                        continue
                    if mflag(m, "IsRenamable"):
                        out[low] = (m.Serial, False)
                    else:
                        out[low] = (m.Serial, mflag(m, "IsHuman") or mflag(m, "IsGargoyle"))
                    if len(out) >= len(lows):
                        break
                except Exception:
                    continue
            return out


        def find_named(name, found=None):
            """(serial, looks like a player) of the mobile in sight with that name;
            (None, None) when none is (a name like "a lich" counts as no player).
            found: named_mobiles() already worked out for this name."""
            low = name.lower()
            if found is None:
                found = named_mobiles((low,))
            hit = found.get(low)
            if hit is not None:
                return hit
            if low.startswith("a ") or low.startswith("an "):
                return None, False
            return None, None


        def note_attacker(name, t, serial):
            """Remember who attacked you (True when they weren't listed yet)."""
            if t <= WATCH["died_at"]:
                return False                       # (a fight from before your last death)
            if serial is not None and (serial in STATE["party"] or is_friend(serial)):
                return False
            low = name.lower()
            a = ATTACKERS.get(low)
            if a is None:
                if len(ATTACKERS) >= ATTACKERS_CAP:            # the cap: the oldest goes
                    oldest = None
                    for k, v in ATTACKERS.items():
                        if oldest is None or v[1] < ATTACKERS[oldest][1]:
                            oldest = k
                    ATTACKERS.pop(oldest, None)
                ATTACKERS[low] = [name, t, serial]
                return True
            if t > a[1]:
                a[1] = t
            if serial is not None:
                a[2] = serial
            return False


        def _newest_first(a):
            return -a[1]


        def on_death(now):
            WATCH["died_at"] = now
            if not UI["killer"]:
                ATTACKERS.clear()
                return
            cut = now - KILLER_BACK
            got = sorted([a for a in ATTACKERS.values() if a[1] >= cut], key=_newest_first)
            ATTACKERS.clear()                      # the next death lists its own attackers
            if UI["say_attackers"]:
                API.SysMsg(TITLE + (": (debug) you died; attackers in the last %d s: %s."
                                    % (int(KILLER_BACK), ", ".join(a[0] for a in got) or "none")),
                           Kit.HUE_INFO)
            if got:
                KILLER_WIN.open(got[:KILLER_ROWS], now, len(got))


        def prune_session(now):
            """Every 10 s: forget who left long ago, alerts past their cooldown and
            attackers too old to list."""
            cut = now - SIGHT_GONE
            for s in [s for s, t in PRESENT.items() if t < cut]:
                del PRESENT[s]
            if ALERTED:
                cut = now - UI["alert_minutes"] * 60.0
                for s in [s for s, t in ALERTED.items() if t < cut]:
                    del ALERTED[s]
            if ATTACKERS:
                cut = now - KILLER_BACK
                for k in [k for k, a in ATTACKERS.items() if a[1] < cut]:
                    del ATTACKERS[k]


        def make_bar_click(serial, name, origin=None):
            """Click handler for a player health bar.

            alt+click        -> auto-follow (again to stop)
            target cursor up -> target the player (spells, bandages, skills)
            shift+click      -> pop out a standalone health bar (tracker rows only)
            double-click     -> attack (or set last target, see DOUBLE_CLICK_ACTION)
            single click     -> set Last Target
            """
            def _clicked(*args):
                try:
                    now = time.time()
                    prev = LAST_CLICK.get(serial, 0)
                    capped(LAST_CLICK)
                    LAST_CLICK[serial] = now

                    if alt_held():
                        LAST_CLICK[serial] = 0
                        toggle_follow(serial)
                        return
                    if click_can_aim():
                        API.Target(serial)
                        LAST_CLICK[serial] = 0
                        return
                    if origin is not None and shift_held():
                        pop_out(serial, name, origin)
                        LAST_CLICK[serial] = 0
                        return
                    double = now - prev <= DOUBLE_CLICK_SECONDS
                    if double:
                        LAST_CLICK[serial] = 0
                    API.SetLastTarget(serial=serial)
                    if double and DOUBLE_CLICK_ACTION == "attack":
                        # (2.6.81) UT1-2: a blue / green player in (maybe) a guard zone
                        # needs a second double-click (the shard's R6)
                        mob = API.FindMobile(serial)
                        hold = attack_hold(serial, mob, now)
                        if hold is not None:
                            if hold == "warn":
                                API.HeadMsg("* double-click again to attack *", serial, 0x22)
                                API.SysMsg(attack_warn_text(mob, name, "double-click again"),
                                           Kit.HUE_BAD)
                            return
                        API.Attack(serial)
                        API.HeadMsg("* attacking *", serial, 0x22)
                    else:
                        API.HeadMsg("* last target *", serial, 0x35)
                except Exception as ex:
                    API.SysMsg(TITLE + (": couldn't handle that click (%s)." % ex), Kit.HUE_BAD)
            return _clicked


        def bar_color(cat, poisoned, dead, paralyzed=False):
            """Friends show every status: green = poisoned, blue = paralyzed,
            teal = both, gray = dead. Other trackers color poison only."""
            if dead:
                return COL_DEAD
            if cat == "friend":
                if poisoned and paralyzed:
                    return COL_BOTH
                if paralyzed:
                    return COL_PARA
            if poisoned:
                return COL_POISON
            return BAR_FG[cat]


        def needs_heal(dead, hits, hmax):
            return not dead and hmax > 0 and hits * 100.0 / hmax <= GLOW_HP_PCT


        def glow_alpha():
            """The pulse's alpha now, in steps of 1/GLOW_STEPS: pulse_glow writes an
            alpha only when it changed, so a row gets a few writes a second, not one
            every poll (a new float every call did that)."""
            a = GLOW_MIN + (GLOW_MAX - GLOW_MIN) * \
                (0.5 + 0.5 * math.sin(2 * math.pi * time.time() / GLOW_PERIOD))
            return int(a * GLOW_STEPS + 0.5) / float(GLOW_STEPS)


        GLOW_SET = {}            # id(glow box) -> the alpha it was last given


        def pulse_glow(glow, low, a=None):
            """Fade a glow box in and out while `low`; hide it otherwise (set once,
            not every pass). a: (2.6.82) glow_alpha() worked out once for the pass."""
            if glow is None:
                return
            if not low:
                a = 0.0
            elif a is None:
                a = glow_alpha()
            k = id(glow)
            if GLOW_SET.get(k) == a:
                return
            if len(GLOW_SET) > 400:
                GLOW_SET.clear()
            GLOW_SET[k] = a
            set_box_alpha(glow, a)


        def hp_text(dead, hits, hmax, poisoned, paralyzed, dist):
            if dead:
                return "DEAD  %dy" % dist, 0, 1
            if hmax > 0:
                flags = (" PSN" if poisoned else "") + (" PAR" if paralyzed else "")
                return "%d%%%s  %dy" % (int(round(100.0 * hits / hmax)), flags, dist), hits, hmax
            return "--  %dy" % dist, 0, 1


        # ------------------------------- HEALTH BARS ---------------------------------
        # Smooth bars drawn from plain color boxes (no art files, no line art, so no
        # stripes and no seam where the line art repeats). Each status color gets a
        # soft fill and a dark track of the same tint for the missing HP:
        #     flat color -> (fill, track)
        BAR_PAINT = {BAR_FG["friend"]:  ("#3A86BF", "#13283A"),
                     BAR_FG["neutral"]: ("#7E868F", "#26292C"),
                     BAR_FG["foe"]:     ("#B23C3C", "#3A1616"),
                     BAR_FG["combat"]:  ("#B23C3C", "#3A1616"),
                     COL_POISON:        ("#4A9A55", "#16301A"),
                     COL_PARA:          ("#5A7FCC", "#1A2640"),
                     COL_BOTH:          ("#2E9A90", "#0F302D"),
                     COL_DEAD:          ("#4C4C4C", "#1C1C1C")}
        BAR_EDGE_ALPHA  = 0.85     # thin black outline round each bar
        BAR_TRACK_ALPHA = 0.90     # the missing-HP part
        BAR_FILL_ALPHA  = 0.95
        BAR_SHEEN_ALPHA = 0.16     # soft light along the top of the fill
        BAR_SHADE_ALPHA = 0.30     # soft shadow along the bottom of the fill


        def bar_paint(color):
            """(fill, track) for a flat bar color; unknown colors get a dark track."""
            return BAR_PAINT.get(color, (color, "#202020"))


        class HealthBar(object):
            """A health bar: a thin black outline, a dark track of the bar's own
            tint for the missing HP, and a soft solid fill with a faint light
            along its top and shadow along its bottom. Built from color boxes only.
            Adds itself to `parent`."""

            RECOLOR = [True]      # color boxes take SetBaseColor on this client

            def __init__(self, parent, x, y, w, h, color, cur=0, mx=1):
                self.fw = None
                self.parts = []
                self.color = color
                fill_col, track_col = bar_paint(color)
                edge = 1 if h >= 5 and w >= 8 else 0
                self.ix, self.iy = x + edge, y + edge
                self.iw, self.ih = max(1, w - 2 * edge), max(1, h - 2 * edge)
                if edge:
                    self._add(parent, BAR_EDGE_ALPHA, "#000000", x, y, w, h)
                self.track = self._add(parent, BAR_TRACK_ALPHA, track_col, self.ix, self.iy,
                                       self.iw, self.ih)
                self.fill = self._add(parent, BAR_FILL_ALPHA, fill_col,
                                      self.ix, self.iy, 0, self.ih)
                self.sheen = self.shade = None
                if self.ih >= 6:
                    self.sheen = self._add(parent, BAR_SHEEN_ALPHA, "#FFFFFF", self.ix, self.iy,
                                           0, max(1, self.ih * 2 // 5))
                    sh = max(1, self.ih // 5)
                    self.shade = self._add(parent, BAR_SHADE_ALPHA, "#000000",
                                           self.ix, self.iy + self.ih - sh, 0, sh)
                self.SetProgress(cur, mx)

            def _add(self, parent, alpha, color, x, y, w, h):
                b = box(alpha, color)
                b.SetRect(x, y, w, h)
                parent.Add(b)
                self.parts.append(b)
                return b

            def SetProgress(self, cur, mx):
                fw = int(round(self.iw * clamp(float(cur) / mx, 0.0, 1.0))) if mx > 0 else 0
                if fw == self.fw:
                    return
                self.fw = fw
                for b in (self.fill, self.sheen, self.shade):
                    if b is not None:
                        try:
                            b.SetWidth(fw)
                        except Exception:
                            pass

            def set_color(self, color):
                """Repaint the bar in another status color, in place (the fill and
                its track are the only tinted parts). False when this client's
                color boxes can't be repainted: the caller builds a new bar."""
                if color == self.color:
                    return True
                if not HealthBar.RECOLOR[0]:
                    return False
                fill_col, track_col = bar_paint(color)
                try:
                    for b, col in ((self.fill, fill_col), (self.track, track_col)):
                        r, g, bl = rgb_of(col)
                        b.SetBaseColor(r, g, bl, 255)
                except Exception:
                    HealthBar.RECOLOR[0] = False
                    return False
                self.color = color
                return True

            def set_visible(self, on):
                ok = True
                for c in self.parts:
                    ok = set_vis(c, on) and ok
                return ok

            def Dispose(self):
                for c in self.parts:
                    drop(c)
                self.parts = []


        # ---------------------------- POP-OUT HEALTH BAR -----------------------------
        class PopBar(object):
            """A small standalone health bar for one player."""

            def __init__(self, serial, name, x, y):
                self.serial = serial
                self.name = name
                self.x, self.y = x, y
                self.gump = None
                self.locked = False
                self.minimized = False
                self.opacity_open = False
                self.opacity = UI["opacity"]
                self.name_color = TEXT_COLOR
                self.create()

            def create(self):
                s = UI["scale"] / 100.0
                w = sc(POP_W)
                self.row_h = max(10, sc(16))
                self.pad = max(2, sc(5))
                h = 2 * BORDER + title_h(s)
                if self.opacity_open:
                    h += orow_h(s)
                if not self.minimized:
                    h += self.row_h + 2 * self.pad
                self.size = (w, h)
                self.x, self.y = Kit.clamp(self.x, self.y, w, h)    # wholly on screen
                g = API.Gumps.CreateModernGump(self.x, self.y, w, h, False, w, h)
                self.gump = g
                safe(lambda: setattr(g, "CanCloseWithRightClick", False))
                safe(lambda: g.SetAlpha(0.0))
                self.chrome = Chrome(g)
                self.bar = self.info = self.hit = self.glow = None
                self.low = False
                self.spell_ctrls = []
                self.bar_key = None
                self.last = None
                self.layout_chrome()
                G.AddGump(g)
                safe(lambda: Kit.on_moved(g, self.moved))   # dragged and let go: the anchors look
                ANCHORS.placed(self.anchor_key)             # (its place is measured next poll)
                safe(lambda: g.SetInScreen())       # never open off the edge of the screen
                safe(lambda: setattr(g, "CanMove", not self.locked))

            @property
            def anchor_key(self):
                return "pop:%d" % self.serial

            def moved(self):
                """Dragged and let go (pop-outs aren't saved; the anchors are told)."""
                ANCHORS.note_moved(self.anchor_key)

            def layout_chrome(self):
                w, h = self.size
                self.chrome.layout(w, h, UI["scale"] / 100.0, self.opacity, self.name,
                                   self.name_color,
                                   std_buttons(self.locked, self.minimized, self.opacity_open,
                                               self.toggle_lock, self.toggle_minimize,
                                               self.toggle_opacity, self.close),
                                   self.opacity_open and not self.minimized,
                                   on_title_dbl=self.toggle_minimize,
                                   on_title_alt=lambda: toggle_follow(self.serial),
                                   alt_key=self.anchor_key)   # (2.6.81) UT1-4

            def destroy(self):
                g, self.gump = self.gump, None
                if g is not None:
                    safe(lambda: g.Dispose())

            def close(self, *args):
                POPS.pop(self.serial, None)
                self.destroy()

            def snapshot(self):
                if self.gump is not None and not safe(lambda: self.gump.IsDisposed, True):
                    self.x = safe(lambda: self.gump.GetX(), self.x)
                    self.y = safe(lambda: self.gump.GetY(), self.y)

            def rebuild(self):
                self.snapshot()
                self.destroy()
                self.create()

            def set_locked(self, locked):
                self.locked = locked
                if self.gump is not None:
                    safe(lambda: setattr(self.gump, "CanMove", not locked))
                    self.layout_chrome()

            def toggle_lock(self, *args):
                self.set_locked(not self.locked)

            def toggle_minimize(self, *args):
                self.minimized = not self.minimized
                self.opacity_open = False
                self.rebuild()

            def toggle_opacity(self, *args):
                self.opacity_open = not self.opacity_open
                self.rebuild()

            def apply_opacity(self, v):
                self.opacity = v
                if self.gump is not None:
                    self.chrome.set_opacity(v)

            def update(self):
                if not Kit.is_open(self.gump):       # (every scan: no lambda here)
                    POPS.pop(self.serial, None)       # closed with right-click
                    return
                try:
                    v = self.chrome.poll()
                    if v is not None:
                        self.opacity = v
                    self._refresh()
                except Exception as ex:
                    API.SysMsg(TITLE + (": closed the health bar for %s (%s)." % (self.name, ex)),
                               Kit.HUE_BAD)
                    self.close()

            def _draw_row(self, key):
                color, _, friend = key
                if self.bar is not None:
                    self.bar.Dispose()
                for c in [self.info, self.hit, self.glow] + self.spell_ctrls:
                    drop(c)
                self.spell_ctrls = []
                w = self.size[0]
                s = UI["scale"] / 100.0
                y = self.chrome.content_top + self.pad
                bw = w - 2 * BORDER - 2 * self.pad
                x = BORDER + self.pad
                if friend and friend_button_count():   # [H] [C] [B] right of the bar
                    sw = self.row_h
                    bw -= friend_button_count() * (sw + 2)
                    friend_buttons(self.gump, x + bw + 2, y, sw, self.row_h, self.serial,
                                   self.name, self.spell_ctrls)
                self.glow = None
                if friend:                        # pulses red at low HP (see pulse())
                    gp = max(2, self.pad - 1)
                    self.glow = box(0.0, GLOW_COLOR)
                    self.glow.SetRect(x - gp, y - gp, bw + 2 * gp, self.row_h + 2 * gp)
                    self.gump.Add(self.glow)
                self.bar = HealthBar(self.gump, x, y, bw, self.row_h, color)
                fs = max(8, int(round(12 * text_scale(s))))   # (2.6.74) E12
                self.info = ttf("", fs, "#FFFFFF", aligned="right", maxWidth=bw - 6,
                                applyStroke=True)
                self.info.SetPos(x + 3, text_y(y, self.row_h, fs))
                self.gump.Add(self.info)
                self.hit = catcher(x, y, bw, self.row_h, make_bar_click(self.serial, self.name),
                                   tip_for(TIP_BAR_ROW, self.name))
                self.gump.Add(self.hit)
                self.bar_key = key
                self.last = None

            def pulse(self, a=None):
                if self.gump is not None and not self.minimized:
                    pulse_glow(self.glow, self.low, a)

            def _refresh(self):
                # (every scan, per pop-out: plain try/except, no lambdas)
                me = player()
                # (2.6.82) a player the scan just listed: what it read this pass
                hit = scanned(self.serial) if me is not None else None
                if hit is not None and hit[0]:
                    mob = True
                else:
                    hit = None
                    try:
                        mob = find_mobile(self.serial)
                    except Exception:
                        mob = None
                if mob is None or me is None:
                    text, cur, mx, key, ncol = "out of range", 0, 1, (COL_DEAD, False, False), "#888888"
                    self.low = False
                else:
                    if hit is not None:
                        name, noto, cat, dead, poisoned, paralyzed, hits, hmax, dist = hit
                    else:
                        try:
                            name = mob.Name or self.name
                        except Exception:
                            name = self.name
                        noto = noto_name(mob)
                        cat, _ = classify(self.serial, name, noto, STATE["party"])
                        dead = mflag(mob, "IsDead")
                        poisoned = mflag(mob, "IsPoisoned")
                        paralyzed = mflag(mob, "IsParalyzed")
                        hits = mnum(mob, "Hits")
                        hmax = mnum(mob, "HitsMax")
                        try:
                            dist = max(abs(int(mob.X) - int(me.X)), abs(int(mob.Y) - int(me.Y)))
                        except Exception:
                            dist = 0
                    key = (bar_color(cat, poisoned, dead, paralyzed),
                           (UI["magery"], UI["healing"]), cat == "friend")
                    self.low = cat == "friend" and needs_heal(dead, hits, hmax)
                    ncol = NOTO_COLOR.get(noto, "#DDDDDD")
                    text, cur, mx = hp_text(dead, hits, hmax, poisoned, paralyzed, dist)
                if Follow.serial == self.serial:
                    text = "FOL " + text

                self.name_color = ncol
                if self.minimized:                      # the title strip carries the HP
                    self.chrome.set_title("%s  %s" % (self.name, text.split("  ")[0]), ncol)
                    return
                self.chrome.set_title(self.name, ncol)

                if key != self.bar_key:
                    old = self.bar_key
                    if old is not None and old[1:] == key[1:] and self.bar is not None \
                            and self.bar.set_color(key[0]):
                        self.bar_key = key            # only the status color changed: repainted
                    else:
                        self._draw_row(key)
                if self.last != (text, cur, mx):
                    self.last = (text, cur, mx)
                    set_text(self.info, text)
                    self.bar.SetProgress(float(cur), float(mx))


        def make_npc_click(serial, name):
            def _clicked(*args):
                if alt_held():                    # Alt+click: auto-follow (the standing rule)
                    toggle_follow(serial)
                    return
                if not name or name == "(unknown)":
                    API.SysMsg(TITLE + ": this person has no name yet; try again in a moment.",
                               Kit.HUE_BAD)
                    return
                IGNORE[name.lower()] = name
                request_save()
                pb = POPS.get(serial)
                if pb is not None:
                    pb.close()
                API.SysMsg(TITLE + (": marked %s as an NPC (hidden from now on). Type the name "
                                    "and press Unignore to undo." % name), Kit.HUE_GOOD)
            return _clicked


        def make_pop_click(serial, name, origin):
            def _clicked(*args):
                if alt_held():                    # Alt+click: auto-follow (the standing rule)
                    toggle_follow(serial)
                    return
                pop_out(serial, name, origin)
            return _clicked


        def enable_unit_frames(serial, name, origin):
            """On the script's thread (thread_tick): turning Character HUD > Frames
            on may load its file, a hitch on the client thread. The pop-out then
            goes on with the next tick (TICK_JOBS: handed back to the tick, not a
            click)."""
            HOST.enable("unitframes")
            TICK_JOBS.append(lambda: pop_out(serial, name, origin, False))


        def pop_out(serial, name, origin, may_enable=True):
            """Character HUD > Frames' "give this mobile a bar" call (turning the
            part on if it's off), or our own pop-out bar when there is no Frames
            part about."""
            add_frame = HOST.services.get("unitframes.add")
            if add_frame is None and may_enable and "unitframes" in HOST.by_key:
                THREAD_JOBS.append(lambda: enable_unit_frames(serial, name, origin))
                return
            if add_frame is not None:                 # a Frames frame, not our own bar
                add_frame(serial)
                API.SysMsg(TITLE + (": %s gets a frame in Character HUD > Frames." % name),
                           Kit.HUE_GOOD)
                return
            existing = POPS.get(serial)
            if existing is not None and existing.gump is not None \
                    and not safe(lambda: existing.gump.IsDisposed, True):
                API.SysMsg(TITLE + (": a health bar for %s is already open." % name), Kit.HUE_BAD)
                return
            try:
                gx = safe(lambda: origin.gump.GetX(), 300)
                gy = safe(lambda: origin.gump.GetY(), 300)
                x = gx + origin.size[0] + 6
                y = gy + len(POPS) * (sc(52) + 4)
                pb = PopBar(serial, name, x, y)
                POPS[serial] = pb
                pb.update()
                API.SysMsg(TITLE + (": popped out a health bar for %s." % name), Kit.HUE_GOOD)
            except Exception as ex:
                POPS.pop(serial, None)
                API.SysMsg(TITLE + (": couldn't pop out a bar for %s (%s)." % (name, ex)),
                           Kit.HUE_BAD)


        # --------------------------- CATEGORY WINDOW ---------------------------------
        #  A tracker window keeps ONE scroll area and a pool of rows. Row i always
        #  sits at the same place and shows the i-th player of the (name-sorted)
        #  list, so when players come and go only the rows' texts, hues, tooltips
        #  and bars change: no controls are made or thrown away. A row is only
        #  made when the list grows past the pool (a surplus row is hidden, not
        #  disposed), and the window's body is drawn again only when its layout
        #  really changes (size, scale, the opacity row, Magery / Healing buttons).
        TIP_BAR_ROW = ("Click: your last target, or aim a target cursor. Double-click: attack "
                       "(blue or green in a guard zone: twice). Alt+click: auto-follow (again to stop)")
        TIP_FOE_ROW = "Click: put the name in the box. Alt+click: auto-follow (again to stop)"
        ALT_FOLLOW_TIP = "Alt+click: auto-follow (again to stop)"   # (2.6.81) UT2-4
        TIP_SIGHT = ("Click: show only this player (again for everyone). "
                     "Alt+click: auto-follow (again to stop)")


        class TrackerRow(object):
            """One reusable row of a tracker window. Its click targets act for
            whoever the row shows at the moment of the click (RowClick)."""

            def __init__(self, win, i, geo, e):
                self.win = win
                self.serial, self.name = e["serial"], e["name"]
                self.y = y = i * geo["row_h"]
                self.shown = True
                self.low = False
                self.last = None                  # (text, cur, mx) the info line / bar show
                self.raw = None                   # (2.6.82) what values() last worked from
                self.name_raw = None              # (2.6.82) what row_name() last worked from
                self.ctrls = []                   # every control but the bar
                sa, rw = win.sa, geo["rw"]
                bg = API.Gumps.CreateGumpColorBox(0.35, "#000000")
                bg.SetRect(0, y, rw, geo["row_h"] - 2)
                on_click(bg, RowClick(self, lambda s, n: make_bar_click(s, n, win)))
                safe(lambda: bg.SetTooltip(tip_for(TIP_BAR_ROW, self.name)))
                sa.Add(bg)
                self.ctrls.append(bg)
                self.bg = bg                      # its tooltip follows the player shown
                self.glow = None
                if win.cat == "friend":           # pulses red at low HP (see pulse())
                    self.glow = box(0.0, GLOW_COLOR)
                    self.glow.SetRect(0, y, rw, geo["row_h"] - 2)
                    sa.Add(self.glow)
                    self.ctrls.append(self.glow)

                text, color = row_name(e, geo)
                self.name_lbl = label(text, geo["name_fs"], color)
                place(self.name_lbl, 4, y + geo["name_dy"])
                sa.Add(self.name_lbl)
                self.ctrls.append(self.name_lbl)
                self.name_key = (text, color)

                pbw, nbw = geo["pbw"], geo["nbw"]
                self.info = label("", geo["info_fs"], "#DDDDDD", aligned="right",
                                  maxWidth=rw - 16 - pbw - nbw)
                place(self.info, 4, y + geo["info_dy"])
                sa.Add(self.info)
                self.ctrls.append(self.info)

                flat_button(sa, rw - 8 - pbw - nbw, y + geo["npc_dy"], nbw, nbw, "N",
                            RowClick(self, make_npc_click),
                            "Mark them as an NPC: hidden from now on (type the name and press "
                            "Unignore to undo). Alt+click: auto-follow (again to stop)",
                            font=geo["npc_fs"], store=self.ctrls)
                flat_button(sa, rw - 4 - pbw, y + geo["pop_dy"], pbw, geo["pop_h"], ">",
                            RowClick(self, lambda s, n: make_pop_click(s, n, win)),
                            "Pop out a health bar for them (Shift+click the row does too). "
                            "Alt+click: auto-follow (again to stop)",
                            font=geo["pop_fs"], store=self.ctrls)
                self.tips = []
                if geo["fbtn"]:                   # Friends: [H] [C] [B]
                    self.tips = friend_buttons(sa, 4 + geo["bar_w"] + 2, y + geo["fbtn_dy"],
                                               geo["sb"], geo["sb"], self.serial, self.name,
                                               store=self.ctrls, row=self)
                self.bar_at = (4, y + geo["bar_dy"], geo["bar_w"], geo["bar_h"])
                x0, y0, bw, bh = self.bar_at
                self.bar = HealthBar(sa, x0, y0, bw, bh, row_color(win.cat, e))

            def assign(self, e, geo):
                """Show player e in this row (only what differs is changed). False
                when the row couldn't be shown again on this client."""
                serial, name = e["serial"], e["name"]
                if serial != self.serial or name != self.name:
                    if serial != self.serial:
                        self.prev = (self.serial, self.name, time.time())
                    self.serial, self.name = serial, name
                    self.last = None
                    for c, tip in self.tips:
                        try:
                            c.SetTooltip(tip % name)
                        except Exception:
                            pass
                    try:                          # (the player's link and note: once per change)
                        self.bg.SetTooltip(tip_for(TIP_BAR_ROW, name))
                    except Exception:
                        pass
                if not self.shown and not self.set_shown(True):
                    return False
                nr = (e["name"], e["tag"], e["noto"], geo["name_px"], geo["name_fs"])
                if nr != self.name_raw:           # (2.6.82) the name line made only on a change
                    text, color = row_name(e, geo)
                    if (text, color) != self.name_key:
                        self.set_name(text, color, geo)
                    self.name_raw = nr
                fg = row_color(self.win.cat, e)
                if fg != self.bar.color and not self.bar.set_color(fg):
                    self.bar.Dispose()            # this client can't repaint: a new bar
                    x0, y0, bw, bh = self.bar_at
                    self.bar = HealthBar(self.win.sa, x0, y0, bw, bh, fg)
                    self.last = None
                return True

            def set_name(self, text, color, geo):
                lb = self.name_lbl
                if color == self.name_key[1] or set_hue(lb, color):
                    set_text(lb, text)
                else:                             # a smooth-font name: its color is fixed
                    at = self.ctrls.index(lb)
                    drop(lb)
                    lb = label(text, geo["name_fs"], color)
                    place(lb, 4, self.y + geo["name_dy"])
                    self.win.sa.Add(lb)
                    self.ctrls[at] = lb
                    self.name_lbl = lb
                self.name_key = (text, color)

            def values(self, e):
                """HP, distance and status of the player shown (every scan)."""
                fol = Follow.serial == e["serial"]
                # (2.6.82) nothing changed since the last scan: no text made
                raw = (e["dead"], e["hits"], e["hmax"], e["poisoned"], e["paralyzed"],
                       e["dist"], fol)
                if self.last is not None and raw == self.raw:
                    return
                self.raw = raw
                text, cur, mx = hp_text(e["dead"], e["hits"], e["hmax"],
                                        e["poisoned"], e["paralyzed"], e["dist"])
                if fol:
                    text = "FOL " + text
                self.low = needs_heal(e["dead"], e["hits"], e["hmax"])
                if self.last != (text, cur, mx):
                    self.last = (text, cur, mx)
                    set_text(self.info, text)
                    self.bar.SetProgress(float(cur), float(mx))

            def set_shown(self, on):
                """Show / hide the whole row; False when this client can't."""
                ok = True
                for c in self.ctrls:
                    if not set_vis(c, on):
                        ok = False
                        break
                ok = ok and self.bar.set_visible(on)
                if ok:
                    self.shown = on
                return ok

            def hide(self):
                if self.serial is not None:
                    self.prev = (self.serial, self.name, time.time())
                self.serial, self.name = None, ""
                self.low = False
                self.last = None
                if self.glow is not None:
                    pulse_glow(self.glow, False)
                return self.set_shown(False)

            def dispose(self):
                for c in self.ctrls:
                    drop(c)
                self.ctrls = []
                self.bar.Dispose()
                self.serial = None

            def forget(self):
                """The row's controls went with their scroll area: drop the notes."""
                for c in self.ctrls:
                    LABELS.pop(id(c), None)
                self.ctrls = []
                self.serial = None


        def row_name(e, geo):
            """(text, color) of a tracker row's name line."""
            text = cut_text(e["name"], geo["name_px"], geo["name_fs"])   # (2.6.74) E12: cut, not shrunk
            if e["tag"]:
                text += "  [" + e["tag"] + "]"
            return text, NOTO_COLOR.get(e["noto"], "#DDDDDD")


        def row_color(cat, e):
            return bar_color(cat, e["poisoned"], e["dead"], e["paralyzed"])


        class CategoryGump(object):
            def __init__(self, cat):
                self.cat = cat
                self.gump = None
                self.chrome = None
                self.locked = False
                self.minimized = False
                self.docked = False               # folded into the Action Bar (hidden)
                self.opacity_open = False
                self.sa = None
                self.rows = []
                self.made_min = None
                self.create()

            # ----- lifecycle -----
            def create(self):
                x, y, w, h, locked, mini, _ = LAYOUT[self.cat]
                self.minimized = mini
                if mini:
                    self.opacity_open = False
                s = UI["scale"] / 100.0
                lo_w, lo_h = sc(MIN_W), sc(MIN_H)
                slot = FIT["size"].get(self.cat)
                if slot is not None:              # (2.6.60) in a zone: exactly its slot, even
                    lo_w = min(lo_w, slot[0])     # one smaller than the tracker's own smallest
                    lo_h = min(lo_h, slot[1])     # size (it ran over the window beside it), and
                    w = slot[0]                   # after any rebuild (a new scale) too
                    if not mini:
                        h = slot[1]
                    # (2.6.69) made where its slot is (not where it was last saved, which
                    # the keeper would first pull on screen over its neighbour)
                    at = layout_rect(self.dock_key)
                    if at is not None:
                        x, y = at[0], at[1]
                w = max(w, lo_w)
                if mini:
                    gh = KIT_MINI_H               # (2.6.72) the Kit look's minimized height
                    min_h, resizable = gh, False
                else:
                    gh = max(h, lo_h)
                    # (2.6.69) in a zone the zone has the size: no corner drag
                    min_h, resizable = lo_h, slot is None
                self.made_min = (lo_w, lo_h)      # the smallest the client lets it be
                self.resized_flag = False
                self.sync_target = None           # size we set via sync (not a user drag)
                self.user_resize_pending = False
                self.user_resize_ticks = 0
                x, y = Kit.clamp(x, y, w, gh)     # wholly on screen
                LAYOUT[self.cat][0], LAYOUT[self.cat][1] = x, y
                self.gump = API.Gumps.CreateModernGump(x, y, w, gh, resizable, lo_w,
                                                       min_h, self._on_resized)
                safe(lambda: setattr(self.gump, "CanCloseWithRightClick", False))
                # Hide the built-in frame; Chrome draws the shared background + border.
                safe(lambda: self.gump.SetAlpha(0.0))
                self.chrome = Chrome(self.gump, kit=True, key=self.dock_key)   # (2.6.72) Kit look

                self._forget_body()
                self.size = (w, gh)
                self.count_n = 0
                self.locked = locked
                self.layout_chrome()
                G.AddGump(self.gump)
                safe(lambda: Kit.on_moved(self.gump, self.moved))   # saved when you let go
                ANCHORS.placed(self.cat)          # built here, not dragged here (measured next poll)
                self._apply_lock()                # (the padlock was drawn by layout_chrome)
                if self.docked and mini:
                    safe(lambda: setattr(self.gump, "IsVisible", False))

            def _forget_body(self):
                """The scroll area and its rows went (window rebuilt / disposed)."""
                for r in self.rows:
                    r.forget()
                self.rows = []
                self.sa = None
                self.empty = None                 # (2.6.74) its lines went with the scroll area
                self.geo = None
                self.body_key = None

            def layout_chrome(self):
                w, h = self.size
                self.chrome.layout(w, h, UI["scale"] / 100.0, LAYOUT[self.cat][6],
                                   self.title_text(), TITLE_COLOR[self.cat],
                                   std_buttons(self.locked, self.minimized, self.opacity_open,
                                               self.toggle_lock, self.user_minimize,
                                               self.toggle_opacity,
                                               on_dock=lambda *a: DOCK_REQ.append(self.dock_key)),
                                   self.opacity_open and not self.minimized,
                                   on_title_dbl=self.user_minimize)
                self.chrome.set_status(str(max(0, self.count_n)))   # (2.6.72) the count

            def destroy(self):
                g, self.gump = self.gump, None
                if g is not None:
                    safe(lambda: g.Dispose())

            def _on_resized(self, *args):
                self.resized_flag = True          # handled on the script loop

            def apply_opacity(self, v):
                LAYOUT[self.cat][6] = v
                if self.gump is not None:
                    self.chrome.set_opacity(v)

            def title_text(self):
                return TITLES[self.cat]           # (2.6.72) the count is the grey status after it

            def set_count(self, n, force=False):
                if n == self.count_n and not force:
                    return
                self.count_n = n
                self.chrome.set_status(str(max(0, n)))

            # ----- lock / minimize / opacity -----
            def _apply_lock(self):
                locked = self.locked
                zoned = FIT["size"].get(self.cat) is not None     # (2.6.69) the zone sizes it
                # (2.6.72) a window in a zone is the layout's to hold (Arrange mode moves it)
                held = safe(lambda: HOST.layout_holds(self.dock_key), False)
                if not held:
                    safe(lambda: setattr(self.gump, "CanMove", not locked))
                safe(lambda: self.gump.SetResizable(not locked and not self.minimized
                                                    and not zoned))
                LAYOUT[self.cat][4] = locked
                STATE["dirty_save"] = True

            def set_locked(self, locked):
                self.locked = locked
                self._apply_lock()
                if not self.chrome.kit:
                    self.layout_chrome()          # redraw the padlock

            def toggle_lock(self, *args):
                self.set_locked(not self.locked)

            @property
            def dock_key(self):
                return "ultima." + self.cat

            def user_minimize(self, *args):
                """Minimize / Restore from the window itself: its own title strip,
                never the Action Bar (the gold arrow is for that)."""
                safe(lambda: HOST.dock_forget(self.dock_key))
                self.toggle_minimize()

            def toggle_minimize(self, *args):
                self.snapshot()
                LAYOUT[self.cat][5] = not self.minimized
                if not LAYOUT[self.cat][5]:
                    self.docked = False
                self.destroy()
                self.create()
                STATE["dirty_save"] = True

            def toggle_opacity(self, *args):
                self.opacity_open = not self.opacity_open
                self.layout_chrome()
                self.body_key = None              # rows move down / up

            # ----- rows -----
            def geometry(self):
                """Where everything of a row goes (worked out once per layout)."""
                w, h = self.size
                sa_w = max(40, w - 2 * PAD)
                rw = max(60, sa_w - SCROLLBAR)
                name_fs = tsc(13)                 # (2.6.74) E12: never under its own size
                # (2.6.72) inside the Kit body panel: MARGIN + 4 in from the window's edge
                ix = Kit.MARGIN + 4 if self.chrome.kit else PAD
                if self.chrome.kit:
                    sa_w = max(40, w - 2 * ix)
                    rw = max(60, sa_w - SCROLLBAR)
                g = {"sa": (ix, self.chrome.content_top + sc(4), sa_w,
                            max(20, h - self.chrome.content_top - sc(4) - ix)),
                     "rw": rw, "row_h": sc(ROW_H), "name_fs": name_fs, "info_fs": tsc(12),
                     "name_px": max(30, int(rw / 1.2)),   # (2.6.74) cut_text's room
                     "name_dy": sc(1), "info_dy": sc(2),
                     "pbw": sc(POP_BTN_W), "nbw": sc(NPC_BTN_W),
                     "npc_dy": sc(3), "npc_fs": tsc(10),
                     "pop_dy": sc(1), "pop_h": sc(16), "pop_fs": tsc(12),
                     "fbtn": self.cat == "friend" and friend_button_count() > 0,
                     "sb": sc(13), "fbtn_dy": sc(16)}
                bar_w = rw - 8
                if g["fbtn"]:
                    bar_w -= friend_button_count() * (g["sb"] + 2)
                g["bar_w"] = bar_w
                # a little taller when the line art loaded
                by, bh = (sc(18), sc(10)) if "bar_h" in NATIVE else (sc(19), sc(8))
                g["bar_dy"], g["bar_h"] = by, max(3, bh)
                return g

            def build_body(self):
                """A new scroll area with no rows yet (they're made as needed)."""
                if self.sa is not None:
                    old = self.sa
                    safe(lambda: old.Dispose())   # its rows go with it
                self._forget_body()
                self.geo = geo = self.geometry()
                x, y, w, h = geo["sa"]
                self.sa = API.Gumps.CreateGumpScrollArea(x, y, w, h)
                self.gump.Add(self.sa)

            def show_empty(self, on):
                """The "No players in range." line."""
                if on and self.empty is None:
                    # (2.6.72) the standard empty state: grey, a full sentence that says what to do
                    # (2.6.74) E12: in the label font at its own size, wrapped inside the
                    # rows' width (4 px in from either side), one line each EMPTY_PITCH px
                    lines = empty_lines("No players in range. The list fills as players "
                                        "come near.", self.geo["rw"] - 8)
                    self.empty = add_empty(self.sa, lines, 4, 4)
                    self.empty_shown = True
                elif self.empty is not None and on != self.empty_shown:
                    if all(set_vis(lb, on) for lb in self.empty):
                        self.empty_shown = on
                    else:
                        for lb in self.empty:
                            drop(lb)
                        self.empty = None

            def fill(self, entries):
                """Row i shows entries[i]: rows are reused, hidden or added."""
                rows, geo, n = self.rows, self.geo, len(entries)
                for i in range(n):
                    e = entries[i]
                    if i < len(rows) and not rows[i].assign(e, geo):
                        for r2 in rows[i:]:       # can't be shown again: made anew
                            r2.dispose()
                        del rows[i:]
                    if i >= len(rows):
                        rows.append(TrackerRow(self, i, geo, e))
                for i in range(n, len(rows)):
                    r = rows[i]
                    if r.shown and not r.hide():  # this client can't hide: dispose instead
                        for r2 in rows[i:]:
                            r2.dispose()
                        del rows[i:]
                        break
                self.show_empty(n == 0)
                for i in range(n):
                    rows[i].values(entries[i])

            def update(self, entries):
                if not Kit.is_open(self.gump):
                    self.create()

                if not self.minimized:
                    # follow live resizes (every scan: plain try/except)
                    try:
                        w, h = int(self.gump.GetWidth()), int(self.gump.GetHeight())
                    except Exception:
                        w, h = self.size
                    if (w <= 0 or h <= 0) and self.size:  # (2.6.71) made this pass: not landed yet
                        w, h = self.size
                    if (w, h) != self.size or self.resized_flag:
                        self.resized_flag = False
                        self.size = (w, h)
                        try:                      # the anchors: a new size, not a move
                            ANCHORS.placed(self.cat, self.gump.GetX(), self.gump.GetY(), w, h)
                        except Exception:
                            pass
                        self.layout_chrome()
                        self.body_key = None
                        if self.sync_target == (w, h):
                            self.sync_target = None      # our own sync, not a user drag
                        elif FIT["size"].get(self.cat) is not None:
                            # (2.6.57) in a zone the layout sizes it: never a drag of
                            # the player's, so never synced on to the other trackers
                            self.sync_target = None
                        else:
                            self.user_resize_pending = True
                            self.user_resize_ticks = 0
                    elif self.user_resize_pending:
                        self.user_resize_ticks += 1
                    slot = FIT["size"].get(self.cat)
                    if slot is not None and (w, h) != slot:
                        FIT["req"] = True         # (2.6.69) not its slot's size: fit_tick puts it right

                v = self.chrome.poll()
                if v is not None:
                    LAYOUT[self.cat][6] = v
                    STATE["dirty_save"] = True

                self.set_count(len(entries))
                if self.minimized:
                    return

                key = (self.size, self.chrome.content_top, UI["scale"], UI["magery"],
                       UI["healing"])
                if key != self.body_key:
                    self.build_body()
                    self.body_key = key
                self.fill(entries)

            def pulse(self, a=None):
                if self.cat != "friend" or self.minimized:
                    return
                for row in self.rows:
                    if row.shown:
                        pulse_glow(row.glow, row.low, a)

            def resize_to(self, w, h):
                """Match another tracker's size (used by Sync tracker sizes)."""
                if not self.minimized:
                    if self.size == (w, h):
                        return
                    self.sync_target = (w, h)
                    safe(lambda: self.gump.SetWidth(w))
                    safe(lambda: self.gump.SetHeight(h))
                    if (safe(lambda: self.gump.GetWidth(), 0),
                            safe(lambda: self.gump.GetHeight(), 0)) == (w, h):
                        return
                # minimized, or the client refused a live resize: rebuild
                self.snapshot()
                LAYOUT[self.cat][2], LAYOUT[self.cat][3] = w, h
                self.destroy()
                self.create()

            def moved(self):
                """Dragged and let go: the layout is saved right away, and the
                anchors look at the windows (its group may need to follow / snap)."""
                ANCHORS.note_moved(self.cat)
                self.snapshot()
                request_save()

            def snapshot(self):
                if self.gump is None or safe(lambda: self.gump.IsDisposed, True):
                    return
                L = LAYOUT[self.cat]
                L[0] = safe(lambda: self.gump.GetX(), L[0])
                L[1] = safe(lambda: self.gump.GetY(), L[1])
                L[2] = self.size[0]
                if not self.minimized:            # keep the restore height while minimized
                    L[3] = self.size[1]


        def rebuild_windows(windows):
            for w in windows.values():
                w.destroy()
            for w in windows.values():
                w.create()
            for p in list(POPS.values()):
                p.rebuild()


        def sync_sizes(windows, source):
            """Give every other unlocked tracker the source tracker's size."""
            if source.minimized:
                w, h = LAYOUT[source.cat][2], LAYOUT[source.cat][3]
            else:
                w, h = source.size
            for t in windows.values():
                if t is source or t.locked or FIT["size"].get(t.cat) is not None:
                    continue                      # (2.6.57) a window in a zone keeps its slot
                t.resize_to(w, h)
            STATE["dirty_save"] = True


        def process_size_sync(windows):
            for w in windows.values():
                if not UI["sync"]:
                    w.user_resize_pending = False
                elif w.user_resize_pending and w.user_resize_ticks >= 2:
                    if drag_on():                         # (2.6.74) a resize may rebuild a
                        return                            # window: after the drag (kept)
                    w.user_resize_pending = False         # drag finished
                    sync_sizes(windows, w)
                    return


        def apply_scale(new_scale, windows):
            old = UI["scale"]
            if new_scale == old:
                return
            ratio = float(new_scale) / old
            for w in windows.values():
                w.snapshot()
                L = LAYOUT[w.cat]
                L[2] = max(sc(MIN_W, new_scale), int(round(L[2] * ratio)))
                L[3] = max(sc(MIN_H, new_scale), int(round(L[3] * ratio)))
            UI["scale"] = new_scale
            rebuild_windows(windows)
            STATE["dirty_save"] = True


        def fit_hook(cat):
            """The layout's "fit" hook for group window `cat` (2.6.56: "exact"):
            its slot in a zone is w x h px and the window is made exactly that
            size (the tracker's own resize: the rows lay out for it), or it is
            freed (None) and gets back the size the player gave it. Runs in the
            keeper's pass: it only records; fit_tick applies."""
            def fit(w, h, mode):
                if w is None or h is None:
                    if cat in FIT["size"]:
                        FIT["size"][cat] = None   # freed: the player's own size back
                    FIT["force"].discard(cat)
                else:
                    FIT["size"][cat] = (int(w), int(h))
                    if mode == "again":           # (2.6.69) the layout measured it: not its
                        FIT["force"].add(cat)     # slot's size, so made anew at that size
                FIT["req"] = True
            return fit


        def fit_tick(windows):
            """Apply the slots told since the last tick: each fitted group window
            made its slot's size, a freed one its own size again. (2.6.74) Never
            under a drag (drag_on, asked once and only when a window is to be made
            anew or resized): that window's fit is kept (FIT["req"] set again, its
            "again" kept) and done on a tick after the drag."""
            if not FIT["req"]:
                return
            FIT["req"] = False
            busy = None                           # (2.6.74) drag_on(), asked when needed
            for cat, want in list(FIT["size"].items()):
                win = windows.get(cat)
                if win is None or win.gump is None:
                    continue
                if want is None:                  # freed
                    if busy is None:
                        busy = drag_on()
                    if busy:                      # (2.6.74) kept for a tick after the drag
                        FIT["req"] = True
                        continue
                    FIT["size"].pop(cat, None)
                    own = FIT["own_size"].pop(cat, None)
                    if win.made_min is not None and win.made_min != (sc(MIN_W), sc(MIN_H)):
                        # (2.6.60) made smaller than its own smallest for a zone: made
                        # anew, so the player's drags stop at the smallest size again
                        win.snapshot()
                        if own is not None:
                            LAYOUT[cat][2], LAYOUT[cat][3] = own
                        win.destroy()
                        win.create()
                    elif own is not None and own != (LAYOUT[cat][2], LAYOUT[cat][3]):
                        win.resize_to(own[0], own[1])
                    FIT["made"].pop(cat, None)
                    if win.gump is not None:
                        win._apply_lock()         # (2.6.69) free: its corners drag again
                    continue
                if cat not in FIT["own_size"]:
                    FIT["own_size"][cat] = (LAYOUT[cat][2], LAYOUT[cat][3])
                w, h = want
                force = cat in FIT["force"]
                if win.minimized:                 # a minimized group: its bar, the slot's width
                    if LAYOUT[cat][2] != w or (win.size and win.size[0] != w):
                        if busy is None:
                            busy = drag_on()
                        if busy:                  # (2.6.74) kept for a tick after the drag
                            FIT["req"] = True
                            continue
                        win.resize_to(w, LAYOUT[cat][3])
                    FIT["force"].discard(cat)
                    continue
                # (2.6.69) the window as it really is, not as it was last asked to be: a
                # live resize is queued by the client and read back before it lands, and a
                # window made smaller than the client lets it be, or dragged by a corner,
                # stayed off its slot. Made anew at exactly the slot (where the slot is):
                # the client makes a new window that size at once.
                try:
                    real = (int(win.gump.GetWidth()), int(win.gump.GetHeight()))
                except Exception:
                    real = None
                if real is not None and (real[0] <= 0 or real[1] <= 0):
                    FIT["force"].discard(cat)
                    continue                      # (2.6.71) just made: read it once it has landed
                made = FIT["made"].get(cat)
                tries = made[1] if made is not None and made[0] == (w, h) else 0
                if real == (w, h) and win.size == (w, h):
                    tries = 0
                    FIT["made"].pop(cat, None)    # (2.6.71) landed: the count is "in a row"
                if (force or win.size != (w, h) or real != (w, h)
                        or win.made_min[0] > w or win.made_min[1] > h) \
                        and (force or tries < FIT_TRIES):  # (never a rebuild every tick)
                    if busy is None:
                        busy = drag_on()
                    if busy:                      # (2.6.74) kept (its "again" too) for a
                        FIT["req"] = True         # tick after the drag
                        continue
                    FIT["force"].discard(cat)
                    FIT["made"][cat] = ((w, h), tries + 1)
                    win.snapshot()
                    LAYOUT[cat][2], LAYOUT[cat][3] = w, h
                    win.destroy()
                    win.create()                  # its next update lays the rows out for it
                else:
                    FIT["force"].discard(cat)


        # =============================================================================
        #  COMBAT BARS
        # =============================================================================
        ATTACK_RE = re.compile(r"\*?\s*(.+?)\s+is attacking you", re.IGNORECASE)
        HOSTILE_INTS = [int(n) for n in HOSTILE_NOTO]

        cb_engaged = {}        # serial -> {"last": t, "hits": int, "order": n}
        cb_order_counter = [0]
        cb_pending_click = []  # (serial, alt held) clicked (handled in the loop)
        cb_snap = {}           # serial -> mobile, refreshed once per pass
        cb_pending_spell = []  # (spell name, serial, harmful, click time) clicked (handled in the loop)
        cb_casting = {"serial": None, "until": 0.0, "harmful": True, "stale": False}


        def cb_mob_ok(m):
            try:
                return m is not None and not m.IsDead
            except Exception:
                return False


        def cb_dist(m):
            try:
                return int(m.Distance)
            except Exception:
                return 0


        def cb_attackable(m, attacked_me=False):
            """False entries never get a bar: your pets, vendors / player vendors /
            healers (yellow), and blue/green NPCs or players unless they attacked you."""
            if mflag(m, "IsRenamable"):
                return False
            noto = noto_name(m)
            return noto not in NEVER_SHOW_NOTO and (attacked_me or noto not in FRIENDLY_NOTO)


        def cb_engage(serial, t=None):
            e = cb_engaged.get(serial)
            if not e:                       # (2.6.82) a bar's mobile already passed "not you"
                me = player()
                if me is None or serial == me.Serial:
                    return
            if COMBAT_IGNORE_FRIENDS and (serial in STATE["party"] or is_friend(serial)):
                return
            t = t or time.time()
            if e:
                e["last"] = t
            elif len(cb_engaged) < MAX_BARS:
                cb_order_counter[0] += 1
                cb_engaged[serial] = {"last": t, "hits": None, "order": cb_order_counter[0]}


        # ----------------------------- detection -------------------------------------
        ATTACK_BACK = 5.0      # an "is attacking you" line counts this long after it came in


        def cb_new_attack_lines():
            """The "is attacking you" lines that came in since the last look (from
            the shared Journal: read once per pass for every module, never
            cleared). Lines older than ATTACK_BACK seconds (the window was hidden
            meanwhile) no longer count, as before."""
            rd = JREAD["attack"]
            if rd is None:
                JREAD["attack"] = Journal.reader()
                return []
            cut = time.time() - ATTACK_BACK
            out = []
            for ln in rd.new():
                if ln.at >= cut and "is attacking you" in ln.low:
                    out.append(ln.text)
            return out


        def cb_scan_journal():
            entries = cb_new_attack_lines()
            if not entries:
                return
            names = set()
            for text in entries:
                try:
                    m = ATTACK_RE.search(text)
                    if m:
                        names.add(m.group(1).strip().lower())
                except Exception:
                    pass
            if not names:
                return
            # (2.6.81) UT2-1: names aren't unique. A name with one mobile in sight
            # brings it in (blue / green too: it attacked you); with several, only
            # those that are attackable anyway (not blue / green) or in war mode, and
            # if none of them is, only the nearest: a blue bystander who merely
            # shares the attacker's name never gets a bar
            found = {}
            for m in mobiles_near():
                try:
                    n = m.Name
                    if n:
                        low = n.strip().lower()
                        if low in names and cb_attackable(m, attacked_me=True):
                            found.setdefault(low, []).append(m)
                except Exception:
                    pass
            for mobs in found.values():
                try:
                    if len(mobs) == 1:
                        cb_engage(mobs[0].Serial)
                        continue
                    picked = [m for m in mobs if cb_attackable(m) or mflag(m, "InWarMode")]
                    if not picked:
                        picked = [min(mobs, key=cb_dist)]
                    for m in picked:
                        cb_engage(m.Serial)
                except Exception:
                    pass


        LT_SKIP_SECONDS = 0.5   # (2.6.82) a last target that got no bar is looked at again after this
        LT_SKIP = {"serial": None, "until": 0.0}


        def cb_scan_last_target():
            if not AUTO_ADD_LAST_TARGET:
                return
            s = API.LastTargetSerial
            me = player()
            if not s or me is None or s == me.Serial or s in cb_engaged:
                return
            if UI["combat_only"]:
                try:
                    war = me.InWarMode
                except Exception:
                    war = False
                if not war:
                    return                  # just targeted (heal, look, buy...), not fighting
            # (2.6.82) one that wasn't attackable / in range is looked at again twice a second
            now = time.time()
            sk = LT_SKIP
            if sk["serial"] == s and 0.0 <= sk["until"] - now <= LT_SKIP_SECONDS:
                return
            m = API.FindMobile(s)
            if cb_mob_ok(m) and cb_dist(m) <= COMBAT_RANGE and cb_attackable(m):
                sk["serial"] = None
                cb_engage(s)
            else:
                sk["serial"], sk["until"] = s, now + LT_SKIP_SECONDS


        def cb_scan_warmode_hostiles():
            if not AUTO_ADD_WARMODE_HOSTILES:
                return
            rng = MELEE_RANGE if UI["combat_only"] else COMBAT_RANGE
            # (2.6.82) only the mobiles within rng (the list is cut by distance: no
            # Distance read per mobile here); a hostile notoriety is never yellow,
            # blue or green, so of cb_attackable only the pet test is left
            for m in mobiles_within(rng):
                try:
                    if int(m.Notoriety) in HOSTILE_INTS and m.InWarMode \
                            and not m.IsDead and not mflag(m, "IsRenamable"):
                        cb_engage(m.Serial)
                except Exception:
                    pass


        def _first(r):
            return r[0]


        def cb_prune_and_refresh():
            """Drop what's no longer being fought, and read everything the bars
            show ONCE per pass for the rest: a mobile can vanish from the client
            between two lookups, so the drawing works from what is read here.
            Returns the bars to show, in order, as
            (serial, name, notoriety, hits, hits max as read, poisoned, paralyzed)."""
            t = time.time()
            cb_snap.clear()
            rows = []
            for s in list(cb_engaged.keys()):
                e = cb_engaged[s]
                m = API.FindMobile(s)
                if not cb_mob_ok(m):
                    del cb_engaged[s]
                    continue
                d = cb_dist(m)
                if d > MAX_RANGE:
                    del cb_engaged[s]
                    continue
                # losing hit points or still in war mode near us = still fighting
                try:
                    h = m.Hits
                except Exception:
                    del cb_engaged[s]
                    continue
                if e["hits"] is not None and h < e["hits"]:
                    e["last"] = t
                e["hits"] = h
                n = None                    # (2.6.82) Notoriety read once (also for the row)
                try:
                    if d <= COMBAT_RANGE and m.InWarMode:
                        n = m.Notoriety
                        if int(n) in HOSTILE_INTS:
                            e["last"] = t
                except Exception:
                    pass
                if t - e["last"] > IDLE_TIMEOUT:
                    del cb_engaged[s]
                    continue
                cb_snap[s] = m
                try:
                    name, hm = m.Name or "???", m.HitsMax
                    try:
                        psn, par = bool(m.IsPoisoned), bool(m.IsParalyzed)
                    except AttributeError:          # (a build without them: as before)
                        psn = bool(getattr(m, "IsPoisoned", False))
                        par = bool(getattr(m, "IsParalyzed", False))
                    rows.append((d if SORT_BY_DISTANCE else e["order"], s, name,
                                 noto_name(m) if n is None else noto_of(n), h, hm, psn, par))
                except Exception:
                    continue           # vanished mid-pass; no bar for it this pass
            rows.sort(key=_first)
            return [r[1:] for r in rows]


        # ----------------------------- clicks / spells -------------------------------
        def cb_make_click(serial):
            def _cb(*args):
                cb_pending_click.append((serial, alt_held()))   # read Alt at click time
            return _cb


        def cb_handle_clicks():
            while cb_pending_click:
                s, alt = cb_pending_click.pop(0)
                m = API.FindMobile(s)
                if not m:
                    continue
                if alt:
                    toggle_follow(s)
                    continue
                if click_can_aim():
                    API.Target(s)
                else:
                    # (2.6.81) UT1-2 (audit): a blue / green mobile in (maybe) a guard
                    # zone needs a second click, later than a double-click's (R6)
                    hold = attack_hold(s, m, time.time())
                    if hold is not None:
                        if hold == "warn":
                            API.HeadMsg("* click again to attack *", s, 0x22)
                            nm = safe(lambda: m.Name, "") or "they"
                            API.SysMsg(attack_warn_text(m, nm, "click the bar again"),
                                       Kit.HUE_BAD)
                        continue
                    API.Attack(s)
                cb_engage(s)


        def cb_make_spell_click(spell, serial):
            def _cb(*args):
                if alt_held():                    # Alt+click: auto-follow (the standing rule)
                    cb_pending_click.append((serial, True))
                    return
                cb_pending_spell.append((spell, serial, True, time.time()))
            return _cb


        def make_heal_click(serial, spell, stronger):
            """Friends H / C buttons: Shift+click casts the stronger spell."""
            def _cb(*args):
                if alt_held():                    # Alt+click: auto-follow (the standing rule)
                    toggle_follow(serial)
                    return
                cb_pending_spell.append((stronger if shift_held() else spell, serial, False,
                                         time.time()))
            return _cb


        def handle_spells():
            """Cast queued spells and aim each at its mobile once the cursor shows."""
            # a new spell click replaces whatever was waiting
            if cb_pending_spell:
                spell, s, harmful, t0 = cb_pending_spell[-1]
                if cursor_owner() is not None:
                    # another module (or a pick) has the cursor spoken for: casting
                    # now would knock its cursor away, so wait a moment for it
                    if time.time() - t0 > CAST_TIMEOUT:
                        del cb_pending_spell[:]
                        API.SysMsg(TITLE + (": the target cursor stayed in use; %s was not cast."
                                            % spell), Kit.HUE_BAD)
                else:
                    del cb_pending_spell[:]
                    m = API.FindMobile(s)
                    if m and harmful:
                        # (2.6.84) R6: a harmful spell on a blue / green in (maybe) a
                        # guard zone needs a second press too, as the bar's attack does
                        # its own confirm (never the bar's attack warning), timed
                        # from the press
                        hold = attack_hold(("cast", s), m, t0)
                        if hold is not None:
                            if hold == "warn":
                                API.HeadMsg("* click again to cast *", s, 0x22)
                                nm = safe(lambda: m.Name, "") or "they"
                                API.SysMsg(attack_warn_text(m, nm, "click the button again",
                                                            "cast"), Kit.HUE_BAD)
                            m = None
                    if m:
                        stale = bool(API.HasTarget("any"))
                        # cancel only our own last spell's cursor: it came after the
                        # older cursor went away and is of that spell's kind (a
                        # neutral one, e.g. a Map Pings aim or yours, is never ours)
                        if stale and cb_casting["serial"] is not None and not cb_casting["stale"] \
                                and API.HasTarget("harmful" if cb_casting["harmful"] else "beneficial"):
                            API.CancelTarget()
                            stale = False
                        API.CastSpell(spell)
                        # a cursor that was already up (yours) is never aimed: only one
                        # that comes after it went away
                        cb_casting.update(serial=s, harmful=harmful, stale=stale,
                                          until=time.time() + CAST_TIMEOUT)
                        claim_cursor("spell", CAST_TIMEOUT)
                        if harmful:
                            cb_engage(s)

            # once the spell's cursor shows up, aim it at the chosen mobile
            if cb_casting["serial"] is None:
                release_cursor("spell")
                return
            if time.time() > cb_casting["until"]:
                cb_casting["serial"] = None        # fizzled / interrupted / no reagents
                release_cursor("spell")
                return
            if cb_casting["stale"]:
                if not API.HasTarget("any"):
                    cb_casting["stale"] = False    # the old cursor is gone: the next one is ours
                return
            if cursor_owner() is not None:
                return                             # a pick is up: not our spell's cursor
            # Poison/Paralyze cursors are harmful, Heal/Cure cursors beneficial;
            # a bandage cursor is neither, so it's never hijacked
            if API.HasTarget("harmful" if cb_casting["harmful"] else "beneficial"):
                s = cb_casting["serial"]
                cb_casting["serial"] = None
                release_cursor("spell")
                if API.FindMobile(s):
                    API.Target(s)
                else:
                    API.CancelTarget()             # our spell's cursor; its mobile is gone


        # ----------------------------- drawing helpers -------------------------------
        def cb_bar_color(psn, par):
            if psn and par:
                return COL_BOTH
            if psn:
                return COL_POISON
            if par:
                return COL_PARA
            return BAR_FG["combat"]


        def cb_info_text(serial, hits, hm, psn, par):
            pct = "?" if not hm or hm <= 1 else str(int(round(hits * 100.0 / hm))) + "%"
            tags = "FOL " if Follow.serial == serial else ""
            if psn:
                tags += "PSN "
            if par:
                tags += "PAR "
            return tags + pct


        # ----------------------------- window ----------------------------------------
        #  Like the trackers: the window's frame is drawn once per layout (width =
        #  scale, opacity row, minimized, locked, Magery), and a pool of bars sits
        #  under it. Slot i always shows the i-th mobile fought; when mobiles come
        #  and go only the slots' texts, colors and tooltips change, extra slots
        #  are hidden, and the window's height follows the number of bars.
        TIP_CB = ("Click: attack %s (blue or green in a guard zone: click twice), or aim a "
                  "target cursor. Alt+click: auto-follow (again to stop)")
        CB_SPELLS = ((SPELL_POISON, "P", COL_POISON,
                      "Cast Poison on %s. Alt+click: auto-follow (again to stop)"),
                     (SPELL_PARALYZE, "Z", COL_PARA,
                      "Cast Paralyze on %s. Alt+click: auto-follow (again to stop)"))


        CB_X = Kit.MARGIN + 4      # (2.6.72) bars start inside the Kit body panel


        class CombatSlot(object):
            """One reusable bar of the Combat Bars window: the bar, the name and
            HP text on it, its click target and the Magery [P] [Z] buttons."""

            def __init__(self, win, i, geo, d):
                self.win = win
                g = win.gump
                serial, name, noto, hits, hmr, psn, par = d
                self.serial, self.name = serial, name
                self.y = ry = geo["y"] + i * (geo["rh"] + CB_ROW_GAP)
                self.shown = True
                self.ctrls = []               # click targets and buttons (not the bar or texts)
                self.tips = []                # [(click target, tooltip with %s)]
                self.bar = HealthBar(g, CB_X, ry, geo["bar_w"], geo["rh"],
                                     cb_bar_color(psn, par), hits, hmr if hmr else 1)
                self.name_lbl = self.info = None
                self.name_key = self.info_text = None
                self.name_raw = self.info_raw = None   # (2.6.82) see assign / values
                self._texts(d, geo)
                c = catcher(CB_X, ry, geo["bar_w"], geo["rh"],
                            RowClick(self, lambda s, n: cb_make_click(s)),
                            tip_for(TIP_CB % name, name))
                g.Add(c)
                self.ctrls.append(c)
                self.tips.append((c, TIP_CB))
                # Magery: tiny [P] poison and [Z] paralyze buttons to the right of the bar
                if UI["magery"]:
                    bx = CB_X + geo["bar_w"] + 1
                    for spell, txt, col, tip in CB_SPELLS:
                        parts = []
                        flat_button(g, bx, ry, geo["spell_w"], geo["rh"], txt,
                                    RowClick(self, (lambda sp: lambda s, n: cb_make_spell_click(
                                        sp, s))(spell)),
                                    tip % name, face=col, color="#FFFFFF",
                                    font=max(7.0, geo["font"] - 1), store=parts)
                        self.ctrls.extend(parts)
                        self.tips.append((parts[-1], tip))
                        bx += geo["spell_w"] + 1

            def _texts(self, d, geo):
                """The name and HP text over the bar (made anew when needed, so they
                stay on top of it)."""
                g = self.win.gump
                serial, name, noto, hits, hmr, psn, par = d
                font = geo["font"]
                ty = text_y(self.y, geo["rh"], font)
                if self.name_lbl is None:
                    text = cut_text(name, geo["name_w"], font, True)   # (2.6.74) E12: cut, not shrunk
                    color = NOTO_COLOR.get(noto, "#FFFFFF")
                    nl = ttf(text, font, color, applyStroke=True)
                    nl.SetPos(CB_X + 3, ty)
                    g.Add(nl)
                    self.name_lbl, self.name_key = nl, (text, color)
                    self.name_raw = (name, noto, geo["name_w"], font)
                if self.info is None:
                    text = cb_info_text(serial, hits, hmr if hmr else 1, psn, par)
                    info = ttf(text, font, "#FFFFFF", aligned="right", maxWidth=geo["info_w"],
                               applyStroke=True)
                    info.SetPos(CB_X + geo["bar_w"] - geo["info_w"] - 3, ty)
                    g.Add(info)
                    self.info, self.info_text = info, text

            def assign(self, d, geo):
                """Show mobile d here (only what differs changes). False when the
                slot couldn't be shown again on this client."""
                serial, name, noto, hits, hmr, psn, par = d
                if serial != self.serial or name != self.name:
                    if serial != self.serial:
                        self.prev = (self.serial, self.name, time.time())
                    self.serial, self.name = serial, name
                    for i, (c, tip) in enumerate(self.tips):
                        try:                      # (the bar itself: with the link and note)
                            c.SetTooltip(tip_for(tip % name, name) if i == 0 else tip % name)
                        except Exception:
                            pass
                if not self.shown and not self.set_shown(True):
                    return False
                color = cb_bar_color(psn, par)
                if color != self.bar.color and not self.bar.set_color(color):
                    # this client can't repaint: a new bar, its texts again on top of it
                    self.bar.Dispose()
                    drop(self.name_lbl)
                    drop(self.info)
                    self.name_lbl = self.info = None
                    self.bar = HealthBar(self.win.gump, CB_X, self.y, geo["bar_w"], geo["rh"],
                                         color, hits, hmr if hmr else 1)
                font = geo["font"]
                nr = (name, noto, geo["name_w"], font)
                if self.name_lbl is not None and nr != self.name_raw:   # (2.6.82) on a change only
                    nk = (cut_text(name, geo["name_w"], font, True),   # (2.6.74) E12
                          NOTO_COLOR.get(noto, "#FFFFFF"))
                    if nk != self.name_key:
                        if nk[1] == self.name_key[1]:
                            set_text(self.name_lbl, nk[0])
                            self.name_key = nk
                        else:                     # the smooth font's color is fixed: a new label
                            drop(self.name_lbl)
                            self.name_lbl = None
                    self.name_raw = nr
                self._texts(d, geo)
                return True

            def values(self, d):
                serial, name, noto, hits, hmr, psn, par = d
                hm = hmr if hmr else 1
                self.bar.SetProgress(hits, hm)
                rk = (serial, hits, hm, psn, par, Follow.serial == serial)
                if rk != self.info_raw:           # (2.6.82) the text made only on a change
                    self.info_raw = rk
                    text = cb_info_text(serial, hits, hm, psn, par)
                    if text != self.info_text:
                        self.info_text = text
                        set_text(self.info, text)

            def set_shown(self, on):
                ok = True
                for c in [self.name_lbl, self.info] + self.ctrls:
                    if c is not None and not set_vis(c, on):
                        ok = False
                        break
                ok = ok and self.bar.set_visible(on)
                if ok:
                    self.shown = on
                return ok

            def hide(self):
                if self.serial is not None:
                    self.prev = (self.serial, self.name, time.time())
                self.serial, self.name = None, ""
                return self.set_shown(False)

            def dispose(self):
                for c in [self.name_lbl, self.info] + self.ctrls:
                    drop(c)
                self.bar.Dispose()
                self.ctrls = []
                self.name_lbl = self.info = None
                self.serial = None


        class CombatWindow(object):
            """The combat bars window. LAYOUT["combat"] holds x, y, width (= scale),
            -, locked, minimized, opacity."""

            def __init__(self):
                self.gump = None
                self.chrome = None
                self.opacity_open = False
                self.relayout = False
                self.zone_redraw = False          # (2.6.74) the relayout is the layout's (its fit)
                self.docked = False               # folded into the Action Bar (hidden)
                self.slot = None                  # (2.6.56) its slot in a zone (w, h), or None
                self.made_min = CB_MIN_WIDTH      # (2.6.60) the width it can't go under
                self._forget()

            def layout_fit(self, w, h, mode):
                """The layout's "fit" hook (2.6.56, "exact"): the window is made its
                slot's size, the bars as wide as it and as many as fit in it; freed
                (None), its own width and the height its bars need again."""
                slot = (int(w), int(h)) if w and h else None
                if slot != self.slot or mode == "again":   # (2.6.69) "again": not its slot's size
                    self.slot = slot
                    self.relayout = True
                    self.zone_redraw = True       # (2.6.74) never drawn under a drag (see draw)

            def width(self):
                """Its width: the slot's, else the player's (which sets the scale)."""
                return self.slot[0] if self.slot is not None else LAYOUT["combat"][2]

            def _forget(self):
                """Nothing drawn yet (a new window, or the old one went)."""
                self.slots = []
                self.grip = []
                self.empty = None
                self.empty_shown = False
                self.empty_lines = []             # (2.6.74) the empty-state text, wrapped
                self.frame_key = None
                self.geo = None
                self.fit_n = None

            @property
            def minimized(self):
                return bool(LAYOUT["combat"][5])

            # ----- open / close -----
            def is_open(self):
                return Kit.is_open(self.gump)     # (asked every combat tick: no lambda)

            def show(self):
                if self.is_open():
                    return
                L = LAYOUT["combat"]
                L[2] = clamp(L[2], CB_MIN_WIDTH, CB_MAX_WIDTH)
                L[0], L[1] = Kit.clamp(L[0], L[1], self.width(), self.height(0))   # wholly on screen
                self.made_min = min(CB_MIN_WIDTH, self.width())   # the smallest the client lets it be
                g = API.Gumps.CreateModernGump(L[0], L[1], self.width(), self.height(0), True,
                                               self.made_min, 16, self._on_resized)
                safe(lambda: g.SetAlpha(0.0))   # Chrome draws the shared look
                self.gump = g
                self._forget()
                G.AddGump(g)
                safe(lambda: Kit.on_moved(g, self.moved))         # saved when you let go
                ANCHORS.placed("combat")
                UI["combat_shown"] = True
                STATE["dirty_save"] = True
                self.apply_lock()
                self.draw(cb_prune_and_refresh())

            def hide(self):
                self.snapshot()
                if self.is_open():
                    g = self.gump
                    safe(lambda: g.Dispose())
                self.gump = None
                self._drop_notes()
                UI["combat_shown"] = False
                STATE["dirty_save"] = True
                # (2.6.81) UT2-2: hidden by the panel's button is no longer folded (a
                # later Show would be on screen while the dock still read "docked");
                # only toggle_visible calls this, module stop keeps the fold
                if self.docked:
                    self.docked = False
                    safe(lambda: HOST.dock_forget("ultima.combat"))

            def _drop_notes(self):
                """The window's controls went with it: forget the label notes."""
                for sl in self.slots:
                    LABELS.pop(id(sl.name_lbl), None)
                    LABELS.pop(id(sl.info), None)
                self._forget()                    # (2.6.74) the empty lines: no label notes

            def toggle_visible(self):
                if self.is_open():
                    self.hide()
                else:
                    self.show()

            def moved(self):
                """Dragged and let go: the layout is saved right away, and the
                anchors look at the windows."""
                ANCHORS.note_moved("combat")
                self.snapshot()
                request_save()

            def snapshot(self):
                if self.is_open():
                    L = LAYOUT["combat"]
                    L[0] = safe(lambda: self.gump.GetX(), L[0])
                    L[1] = safe(lambda: self.gump.GetY(), L[1])

            def reset(self):
                LAYOUT["combat"] = list(DEFAULT_LAYOUT["combat"])
                self.opacity_open = False
                if self.is_open():
                    L = LAYOUT["combat"]
                    g = self.gump
                    safe(lambda: g.SetPos(L[0], L[1]))
                    Kit.moved_by_code(g)              # placed by us, not dragged
                    ANCHORS.placed("combat")
                    self.apply_lock()
                    self.relayout = True
                else:
                    self.show()

            # ----- sizes -----
            def metrics(self):
                s = clamp(self.width(), CB_MIN_WIDTH, CB_MAX_WIDTH) / float(BASE_WIDTH)
                # (2.6.74) E12: the bars scale with the width, the text never under its
                # 100% size (a 192 px zone drew it in a tiny smooth font)
                return s, max(10, int(round(BASE_ROW_H * s))), BASE_FONT * text_scale(s)

            def height(self, n):
                if self.slot is not None and not LAYOUT["combat"][5]:
                    return self.slot[1]           # in a zone: its slot's height, always
                s, rh, _ = self.metrics()
                if LAYOUT["combat"][5]:
                    return KIT_MINI_H             # (2.6.72) the Kit look's minimized height
                h = KIT_HEAD + Kit.MARGIN
                if self.opacity_open:
                    h += orow_h(s)
                if n <= 0 and self.empty_lines:   # (2.6.74) E12: room for the wrapped empty text
                    return h + max(rh + CB_ROW_GAP, 2 + EMPTY_PITCH * len(self.empty_lines)) \
                        + CB_FOOTER_H
                return h + max(n, 1) * (rh + CB_ROW_GAP) + CB_FOOTER_H

            def _empty_text(self, W):
                """(2.6.74) E12: the empty-state sentence wrapped to the window, W px
                wide (from CB_X + 4 to 4 px in from the body section's right edge);
                in a zone only the lines its slot's height holds, the last one cut.
                Worked out when the frame is built, never per tick."""
                width = max(20, W - 2 * CB_X - 4)
                lines = empty_lines("No one is fighting you. Bars show here when a fight "
                                    "starts.", width)
                if self.slot is not None:
                    cap = max(1, (self.slot[1] - Kit.MARGIN - KIT_HEAD - 2) // EMPTY_PITCH)
                    if len(lines) > cap:
                        lines = lines[:cap - 1] + [Kit.fit(" ".join(lines[cap - 1:]), width)]
                return lines

            # ----- buttons -----
            def _on_resized(self, *args):
                if not self.is_open():
                    return
                if self.slot is not None:
                    return                       # in a zone: the layout sizes it
                try:
                    w = clamp(int(self.gump.GetWidth()), CB_MIN_WIDTH, CB_MAX_WIDTH)
                except Exception:
                    return
                if w == LAYOUT["combat"][2]:
                    return                       # only the height moved: fit() owns the height
                LAYOUT["combat"][2] = w
                self.relayout = True

            def apply_lock(self):
                if not self.is_open():
                    return
                g, locked = self.gump, LAYOUT["combat"][4]
                # (2.6.72) in a zone the layout holds it: no drag, no corner resize
                held = safe(lambda: HOST.layout_holds("ultima.combat"), False)
                if not held:
                    safe(lambda: setattr(g, "CanMove", not locked))
                safe(lambda: g.SetResizable(not locked and not held))

            def set_locked(self, locked):
                if LAYOUT["combat"][4] != locked:
                    LAYOUT["combat"][4] = locked
                    self.apply_lock()
                    self.relayout = True
                    STATE["dirty_save"] = True

            def toggle_lock(self, *args):
                self.set_locked(not LAYOUT["combat"][4])

            def user_minimize(self, *args):
                """Minimize / Restore from the window itself (not the Action Bar)."""
                safe(lambda: HOST.dock_forget("ultima.combat"))
                self.toggle_minimize()

            def toggle_minimize(self, *args):
                LAYOUT["combat"][5] = not LAYOUT["combat"][5]
                if not LAYOUT["combat"][5]:
                    self.docked = False
                self.opacity_open = False
                self.relayout = True
                STATE["dirty_save"] = True

            def toggle_opacity(self, *args):
                self.opacity_open = not self.opacity_open
                self.relayout = True

            def apply_opacity(self, v):
                LAYOUT["combat"][6] = v
                if self.is_open() and self.chrome is not None:
                    self.chrome.set_opacity(v)

            # ----- drawing -----
            def title_text(self, data):
                return "Combat"                   # (2.6.72) the rest is the grey status

            def status_text(self, data):
                """(2.6.72) The grey status after the title: the count, and while
                minimized the lowest HP and the poisoned / paralyzed counts."""
                n = len(data)
                if not LAYOUT["combat"][5] or n == 0:
                    return "%d" % n
                low, psn_n, par_n = None, 0, 0
                for serial, name, noto, h, hm, psn, par in data:
                    psn_n += psn
                    par_n += par
                    if hm:
                        pct = int(round(h * 100.0 / hm))
                        low = pct if low is None else min(low, pct)
                parts = ["%d" % n]
                if low is not None:
                    parts.append("low %d%%" % low)
                if psn_n:
                    parts.append("PSN %d" % psn_n)
                if par_n:
                    parts.append("PAR %d" % par_n)
                return "  ".join(parts)

            def build_frame(self, data):
                """The window itself: frame, title strip, grip. Bars are added by
                fill() as needed."""
                g = self.gump
                if self.chrome is not None and self.chrome.gump is g:
                    self.chrome.dispose()
                for sl in self.slots:
                    sl.dispose()
                for c in self.grip:
                    drop(c)
                for c in self.empty or ():        # (2.6.74) its wrapped lines
                    drop(c)
                g.Clear()                         # (anything else still in it)
                self._forget()
                L = LAYOUT["combat"]
                mini = L[5]
                s, rh, font = self.metrics()
                W = self.width()
                n = len(data)
                if not mini:
                    self.empty_lines = self._empty_text(W)   # (2.6.74) before the height
                H = self.height(n)
                g.SetWidth(W)
                g.SetHeight(H)
                self.fit_n = n                    # (2.6.74) 0 and 1 differ: the empty text
                ANCHORS.sized("combat", W, H)     # a new size (scale, minimized), not a move

                self.chrome = Chrome(g, kit=True, key="ultima.combat")   # (2.6.72) Kit look
                self.chrome.layout(W, H, s, L[6], self.title_text(data),
                                   TITLE_COLOR["combat"],
                                   std_buttons(L[4], mini, self.opacity_open,
                                               self.toggle_lock, self.user_minimize,
                                               self.toggle_opacity,
                                               on_dock=lambda *a: DOCK_REQ.append(
                                                   "ultima.combat")),
                                   self.opacity_open and not mini,
                                   on_title_dbl=self.user_minimize)
                self.chrome.set_status(self.status_text(data))
                if mini:
                    return
                inner_w = W - 2 * CB_X
                info_w = int(round(80 * s))
                spell_w = max(14, rh) if UI["magery"] else 0        # one tiny square button each
                bar_w = inner_w - (2 * (spell_w + 1) if UI["magery"] else 0)
                self.geo = {"y": self.chrome.content_top, "rh": rh, "font": font, "s": s,
                            "info_w": info_w, "spell_w": spell_w, "bar_w": bar_w,
                            "name_w": bar_w - info_w - 6, "W": W}
                if L[4]:
                    return
                # resize grip marks in the bottom-right corner (purely visual)
                gx, gy = W - Kit.MARGIN - 9, H - Kit.MARGIN - 9
                for dx, dy in GRIP_DOTS:
                    d = box(1.0, GRIP_COLOR)
                    d.SetRect(gx + dx, gy + dy, 2, 2)
                    g.Add(d)
                    self.grip.append(d)

            def fit(self, n):
                """The window's height for n bars (the frame and grip follow)."""
                n = max(n, 0)                     # (2.6.74) none: the empty text's height
                if n == self.fit_n:
                    return
                self.fit_n = n
                W, H = self.geo["W"], self.height(n)
                try:
                    self.gump.SetHeight(H)
                except Exception:
                    pass
                ANCHORS.sized("combat", W, H)     # the height followed the bars: not a resize by hand
                self.chrome.frame.layout(W, H)
                gx, gy = W - Kit.MARGIN - 9, H - Kit.MARGIN - 9
                for (dx, dy), d in zip(GRIP_DOTS, self.grip):
                    try:
                        d.SetRect(gx + dx, gy + dy, 2, 2)
                    except Exception:
                        pass

            def show_empty(self, on):
                """The "No one is fighting you." line."""
                if on and self.empty is None:
                    # (2.6.72) the standard empty state: a full sentence that says what to expect
                    # (2.6.74) E12: in the label font at its own size, wrapped (see _empty_text)
                    self.empty = add_empty(self.gump, self.empty_lines or [""], CB_X + 4,
                                           self.geo["y"] + 2)
                    self.empty_shown = True
                elif self.empty is not None and on != self.empty_shown:
                    if all(set_vis(lb, on) for lb in self.empty):
                        self.empty_shown = on
                    else:
                        for lb in self.empty:
                            drop(lb)
                        self.empty = None

            def fill(self, data):
                if self.slot is not None:         # in a zone: as many bars as fit its slot
                    geo = self.geo
                    room = self.slot[1] - geo["y"] - Kit.MARGIN - CB_FOOTER_H
                    cap = max(1, room // max(1, geo["rh"] + CB_ROW_GAP))
                    if len(data) > cap:
                        data = data[:cap]
                slots, geo, n = self.slots, self.geo, len(data)
                self.fit(n)
                for i in range(n):
                    d = data[i]
                    if i < len(slots) and not slots[i].assign(d, geo):
                        for sl in slots[i:]:
                            sl.dispose()
                        del slots[i:]
                    if i >= len(slots):
                        slots.append(CombatSlot(self, i, geo, d))
                for i in range(n, len(slots)):
                    sl = slots[i]
                    if sl.shown and not sl.hide():    # this client can't hide: dispose instead
                        for sl2 in slots[i:]:
                            sl2.dispose()
                        del slots[i:]
                        break
                self.show_empty(n == 0)
                for i in range(n):
                    slots[i].values(data[i])

            def draw(self, data):
                L = LAYOUT["combat"]
                key = (L[2], self.opacity_open, L[5], L[4], UI["magery"], self.slot)
                if self.zone_redraw and self.frame_key is not None and drag_on():
                    # (2.6.74) never redrawn for the layout's fit ("again" too) under a drag:
                    # kept (relayout / the key still differ) and done on a tick after it
                    if self.chrome is not None:
                        self.chrome.set_status(self.status_text(data))
                    if key == self.frame_key and not L[5] and self.geo is not None:
                        self.fill(data)           # (the frame as it is: only the bars' values)
                    return
                if self.relayout or key != self.frame_key:
                    self.relayout = self.zone_redraw = False
                    self.build_frame(data)
                    self.frame_key = key
                elif self.chrome is not None:
                    self.chrome.set_title(self.title_text(data))
                    self.chrome.set_status(self.status_text(data))
                if not L[5]:
                    self.fill(data)

            # ----- one pass -----
            def tick(self):
                g = self.gump
                if g is None:
                    del cb_pending_click[:]
                    return
                if stopping():
                    return
                if not Kit.is_open(g):
                    # closed with a right-click: hide it until it's reopened from the panel
                    self.gump = None
                    self._drop_notes()
                    UI["combat_shown"] = False
                    STATE["dirty_save"] = True
                    API.SysMsg(TITLE + ": the combat bars are hidden; Show combat in the "
                               + TITLE + " window brings them back.", Kit.HUE_INFO)
                    return

                if self.chrome is not None:
                    v = self.chrome.poll()
                    if v is not None:
                        LAYOUT["combat"][6] = v
                        STATE["dirty_save"] = True

                if ((self.made_min > self.slot[0]) if self.slot is not None
                        else (self.made_min < CB_MIN_WIDTH)) and not drag_on():
                    # (2.6.74) never made anew under a drag (a new gump loses the drop)
                    # (2.6.60) its slot is narrower than the client lets this window be
                    # (or it was freed from one): made anew with the minimum that fits
                    # (show() draws it)
                    self.snapshot()
                    self.gump = None
                    self._drop_notes()
                    safe(lambda: g.Dispose())
                    self.show()
                    if self.docked:               # (2.6.81) UT2-2: still folded: stays hidden
                        g2 = self.gump
                        safe(lambda: setattr(g2, "IsVisible", False))
                    return

                cb_handle_clicks()
                cb_scan_journal()
                cb_scan_last_target()
                cb_scan_warmode_hostiles()
                self.draw(cb_prune_and_refresh())


        GRIP_DOTS = ((6, 6), (6, 3), (3, 6), (6, 0), (0, 6), (3, 3))


        # ----------------------------- CONTROL PANEL ---------------------------------
        class ControlPanel(object):
            """The tracker's controls (foe list, lock all, combat window): a
            section of the shared Ultima Tracker window (HOST.hub) rather than a
            window of its own. The hub draws the title strip, minimize and close;
            this draws the body into the gump it is handed."""
            BODY_H = 420                      # (kept: the shared window must still fit 768 px)
            FOE_ROW_H = 32                    # (2.6.05) a saved foe: name and buttons, then its
            #                                   link / last seen (the list scrolls past 4)

            def __init__(self, windows, combat):
                self.windows = windows
                self.combat = combat
                self.g = None                 # the hub's gump while our section is drawn
                self.store = ({}, {})         # the hub's click registry for our buttons
                self.x0, self.w = 0, 0
                self.list_sa = None
                self.input = None
                self.foe_ver = -1
                self.foe_rows = []            # (name key, its link / last seen label) of the list
                self.seen_ver = -1            # SIGHT["seen_ver"] those labels were written for
                self.seen_at = 0.0            # their "... ago" is written again after this
                self.lock_all_lbl = self.combat_lbl = self.foe_title = None
                self.lock_all_text = self.combat_text = ""
                self.list_top = self.list_h = 0
                hub = getattr(HOST, "hub", None)
                if hub is not None:
                    hub.add("ultima", TITLE,
                            {"height": self.height, "build": self.build_section,
                             "closed": self.section_closed})
                else:
                    API.SysMsg(TITLE + ": this Virtue Assistant has no shared window, so the "
                               "Foe list panel can't be shown.", Kit.HUE_BAD)

            # ----- our section of the shared window -----
            @property
            def gump(self):
                return self.g if Kit.is_open(self.g) else None

            @property
            def size(self):
                hub = getattr(HOST, "hub", None)
                return (hub.W, hub.H) if hub is not None else (0, 0)

            def height(self, w):
                return self.BODY_H + 16

            def build_section(self, g, x, y, w, store):
                self.g = g
                self.store = store                # the hub's (buttons, clicks) registry for us
                self.x0, self.w = x + 8, w - 16
                self.list_sa = None
                self.foe_ver = -1
                Kit.add_section(g, x, y, w, self.height(w))
                self.build_body(y + 8)
                ANCHORS.note_moved("panel")       # the hub's window was (re)drawn: one look at it

            def section_closed(self):
                self.g = None
                self.list_sa = None
                self.input = None
                self.foe_rows = []

            def build(self):
                """Redraw our section (the hub rebuilds on its next pass)."""
                hub = getattr(HOST, "hub", None)
                if hub is not None:
                    hub.refresh()

            def _heading(self, text, y):
                lb = label(text, 13, "#FFD966")           # gold, like BOD Fisher's headings
                place(lb, self.x0 + 2, y)
                self.g.Add(lb)
                return lb

            def _divider(self, y):
                if "frame" in NATIVE:
                    d = tiled(Kit.STONE_TILE, self.w, 4)
                    d.SetPos(self.x0, y)
                    self.g.Add(d)

            def build_body(self, y0):
                g, X, W = self.g, self.x0, self.w
                cw = int(W / 3)                           # three buttons to a row

                # --- foe / ignore list ---
                self._heading("FOES & IGNORE LIST", y0)
                if "frame" in NATIVE:
                    f = tiled(Kit.FIELD_TILE, W, 24)
                    f.SetPos(X, y0 + 21)
                    g.Add(f)
                self.input = API.Gumps.CreateGumpTextBox("", W - 4, 22, False, 16)
                self.input.SetPos(X + 2, y0 + 22)
                safe(lambda: self.input.SetPlaceholder("Player name"))
                safe(lambda: self.input.SetTooltip(
                    "Type a player name for Add foe, Remove foe, Ignore and Unignore"))
                g.Add(self.input)

                self._button("Add foe", X, y0 + 52, cw, self.add_foe, Kit.ART_OK,
                             "Put the typed name on your Foe list")
                self._button("Remove foe", X + cw, y0 + 52, cw, self.remove_foe, Kit.ART_CLOSE,
                             "Take the typed name off your Foe list")
                self._button("Target...", X + 2 * cw, y0 + 52, cw, self.target_foe,
                             Kit.ART_PLAY, "Target a player to put them on your Foe list")
                self._button("Ignore", X, y0 + 80, cw, self.ignore_name, Kit.ART_CLOSE,
                             "Hide the typed name from the trackers (an NPC that slipped through)")
                self._button("Unignore", X + cw, y0 + 80, cw, self.unignore_name, Kit.ART_OK,
                             "Show the typed name in the trackers again")
                self.lock_all_lbl = self._button("Lock all", X + 2 * cw, y0 + 80, cw,
                                                 self.lock_all, Kit.ART_PLAY,
                                                 "Lock or unlock every tracker, the combat bars "
                                                 "and the pop-outs in place at once")
                self.lock_all_text = "Lock all"
                self._divider(y0 + 110)

                # --- windows ---
                self._heading("WINDOWS", y0 + 120)
                self.combat_text = "Hide combat" if self.combat.is_open() else "Show combat"
                self.combat_lbl = self._button(self.combat_text, X, y0 + 144, cw,
                                               self.toggle_combat, Kit.ART_PLAY,
                                               "Show or hide the combat bars window")
                self._button("Settings", X + cw, y0 + 144, cw,
                             lambda *a: HOST.show_settings("ultima"), Kit.ART_PAGE,
                             "Open the " + TITLE + " settings page")
                self._button("Sightings", X + 2 * cw, y0 + 144, cw,
                             lambda *a: SIGHT_WIN.toggle(), Kit.ART_PAGE,
                             "Open the Sightings window (again to close it)")
                self._divider(y0 + 176)

                # --- saved foes ---
                self.foe_title = label("SAVED FOES (0)", 13, "#FFD966")
                place(self.foe_title, X + 2, y0 + 186)
                g.Add(self.foe_title)
                self.list_top = y0 + 210
                bottom = y0 + self.BODY_H
                step = max(16, NATIVE.get("font_h", 0) if uo_font_for(11) else 0)   # the help line
                self.list_h = bottom - step - 14 - self.list_top
                lb = label("Alt+click any bar: auto-follow (again to stop).", 11, DIM_TEXT)
                place(lb, X + 2, bottom - step - 6)
                g.Add(lb)
                self.foe_ver = STATE["foe_ver"]
                self.rebuild_foe_list()

            def _button(self, text, x, y, w, fn, art, tip=None):
                """A standard gump button with its clickable caption beside it:
                Kit.art_button, the same look as the other sections of the shared
                window. The click is only queued (fn runs on the next tick);
                returns the caption label (Kit.set_text changes it)."""
                bw = Kit.pic_size(art[0])[0] or 30
                key = "ut:" + text.lower().replace(" ", "_").rstrip(".")
                try:
                    return Kit.art_button(self.g, self.store, key, art, x, y,
                                          Kit.fit(text, max(10, w - bw - 6)), tip,
                                          on_click=queue_click(fn))
                except Exception:
                    return flat_button(self.g, x, y, w - 4, 20, text, fn, tip)

            def apply_opacity(self, v):
                LAYOUT["panel"][6] = v                    # the hub keeps the shared stone look

            def _typed(self):
                return (safe(lambda: self.input.Text, "") or "").strip()

            def _clear_input(self):
                safe(lambda: self.input.SetText(""))

            # ----- foe / ignore actions -----
            def _set_foe(self, name):
                add_foe(name)

            def add_foe(self, *args):
                n = self._typed()
                if not n:
                    API.SysMsg(TITLE + ": type a player name in the box first.", Kit.HUE_BAD)
                    return
                self._set_foe(n)
                self._clear_input()
                API.SysMsg(TITLE + (": added %s to the Foe list." % n), Kit.HUE_GOOD)

            def remove_foe(self, *args):
                n = self._typed()
                if n:
                    self._remove(name_key(n))
                    self._clear_input()

            def _remove(self, key):
                if key in FOES:
                    unlink_foe(key)               # (a main hands its alts to the next one)
                    if LINK_PICK[0] == key:
                        LINK_PICK[0] = None
                    name = FOES.pop(key)
                    STATE["foe_ver"] += 1
                    request_save()
                    API.SysMsg(TITLE + (": removed %s from the Foe list." % name), Kit.HUE_GOOD)
                else:
                    API.SysMsg(TITLE + (": %s isn't on the Foe list." % key), Kit.HUE_BAD)

            def target_foe(self, *args):
                API.SysMsg(TITLE + ": target a player to add to your Foe list.", Kit.HUE_INFO)
                # a cursor that holds nothing up: the answer comes on a later pass
                HOST.pick_target(10, self._foe_targeted)

            def _foe_targeted(self, serial):
                mob = safe(lambda: API.FindMobile(serial)) if serial else None
                if not mob or not mob.Name:
                    API.SysMsg(TITLE + ": no player targeted.", Kit.HUE_BAD)
                    return
                self._set_foe(mob.Name)
                API.SysMsg(TITLE + (": added %s to the Foe list." % mob.Name), Kit.HUE_GOOD)

            def ignore_name(self, *args):
                n = self._typed()
                if n:
                    IGNORE[n.lower()] = n
                    request_save()
                    self._clear_input()
                    API.SysMsg(TITLE + (": ignoring %s from now on." % n), Kit.HUE_GOOD)

            def unignore_name(self, *args):
                n = self._typed()
                if n and n.lower() in IGNORE:
                    IGNORE.pop(n.lower())
                    request_save()
                    self._clear_input()
                    API.SysMsg(TITLE + (": no longer ignoring %s." % n), Kit.HUE_GOOD)

            # ----- lock all / combat bars -----
            def _all_locked(self):
                locks = [w.locked for w in self.windows.values()]
                if self.combat.is_open():
                    locks.append(LAYOUT["combat"][4])
                locks.extend(p.locked for p in POPS.values())
                return all(locks)

            def lock_all(self, *args):
                target = not self._all_locked()
                for w in self.windows.values():
                    w.set_locked(target)
                self.combat.set_locked(target)
                for p in list(POPS.values()):
                    p.set_locked(target)
                self.refresh_labels()

            def toggle_combat(self, *args):
                self.combat.toggle_visible()
                self.refresh_labels()

            def refresh_labels(self):
                if self.gump is None or self.lock_all_lbl is None:
                    return
                text = "Unlock all" if self._all_locked() else "Lock all"
                if text != self.lock_all_text:
                    self.lock_all_text = text
                    Kit.set_text(self.lock_all_lbl, text)
                text = "Hide combat" if self.combat.is_open() else "Show combat"
                if text != self.combat_text:
                    self.combat_text = text
                    Kit.set_text(self.combat_lbl, text)

            # ----- appearance actions -----
            def reset_defaults(self, *args):
                reset_settings()
                for p in POPS.values():
                    p.opacity, p.locked = DEFAULT_OPACITY, False
                # (2.6.81) UT2-2: the reset brings every window back shown, so none
                # stays marked folded (its dock state would read "docked" on screen)
                for w in self.windows.values():
                    if w.docked:
                        w.docked = False
                        safe(lambda: HOST.dock_forget(w.dock_key))
                cb_was_docked = self.combat.docked
                if cb_was_docked:
                    self.combat.docked = False
                    safe(lambda: HOST.dock_forget("ultima.combat"))
                rebuild_windows(self.windows)
                self.combat.reset()
                if cb_was_docked and self.combat.is_open():   # (reset keeps the hidden gump)
                    cg = self.combat.gump
                    safe(lambda: setattr(cg, "IsVisible", True))
                self.build()
                apply_borders_all()
                request_save()
                API.SysMsg(TITLE + ": settings and windows reset to the defaults.", Kit.HUE_GOOD)

            def set_all_opacity(self, v):
                UI["opacity"] = v
                for w in self.windows.values():
                    w.apply_opacity(v)
                for pb in POPS.values():
                    pb.apply_opacity(v)
                self.combat.apply_opacity(v)
                self.apply_opacity(v)
                STATE["dirty_save"] = True

            # ----- saved foe list -----
            def rebuild_foe_list(self):
                if self.gump is None:
                    return
                if self.list_sa is not None:
                    old = self.list_sa
                    safe(lambda: old.Dispose())
                # (2.6.82) the old rows' label notes go with their scroll area
                for lb in getattr(self, "list_lbls", ()):
                    LABELS.pop(id(lb), None)
                self.list_lbls = lbls = []
                self.list_sa = API.Gumps.CreateGumpScrollArea(self.x0, self.list_top,
                                                              self.w, self.list_h)
                self.g.Add(self.list_sa)
                self.foe_rows = []
                names = sorted(FOES.items(), key=lambda kv: kv[1].lower())
                set_text(self.foe_title, "SAVED FOES (%d)" % len(names))
                if not names:
                    lb = label("No foes yet. Type a name and press Add foe.", 12, "#888888")
                    lbls.append(lb)
                    place(lb, 2, 2)
                    self.list_sa.Add(lb)
                    return
                # (2.6.05) two lines a foe: the name with its buttons ([U]nlink when
                # linked, [L]ink, [x] remove), then "alt of ..." and where it was last seen
                now = time.time()
                rw = self.w - SCROLLBAR
                mains = set(ALT_OF.values())
                sa = self.list_sa
                for i, (key, name) in enumerate(names):
                    y = i * self.FOE_ROW_H
                    lb = label(short(name, 24), 13, "#FF9090")
                    lbls.append(lb)
                    place(lb, 2, y + 2)
                    sa.Add(lb)
                    bx = rw - 22
                    # (2.6.81) UT2-4: the row's buttons Alt+click follow that player too
                    # (foe_name_click reads Alt again and follows; never called without Alt,
                    # its plain click fills the box)
                    flat_button(sa, bx, y, 18, 18, "x",
                                (lambda k, n: (lambda *a: self.foe_name_click(k, n) if alt_held()
                                               else self._remove(k)))(key, name),
                                "Take %s off your Foe list. %s" % (name, ALT_FOLLOW_TIP))
                    bx -= 22
                    picked = LINK_PICK[0] == key
                    flat_button(sa, bx, y, 18, 18, "L*" if picked else "L",
                                (lambda k, n: (lambda *a: self.foe_name_click(k, n) if alt_held()
                                               else self.link_click(k)))(key, name),
                                ("Linking: press L on the other entry (L here again to cancel). "
                                 if picked else
                                 "Link with another entry as one person (several characters): "
                                 "press L here, then L on the other. ") + ALT_FOLLOW_TIP,
                                face=BTN_FACE_ON if picked else BTN_FACE)
                    if key in ALT_OF or key in mains:
                        bx -= 22
                        flat_button(sa, bx, y, 18, 18, "U",
                                    (lambda k, n: (lambda *a: self.foe_name_click(k, n)
                                                   if alt_held() else self.unlink_click(k)))(key, name),
                                    "Unlink: take this entry out of its group of characters. "
                                    + ALT_FOLLOW_TIP)
                    sa.Add(catcher(0, y, max(20, bx - 6), 18,
                                   (lambda k, n: (lambda *a: self.foe_name_click(k, n)))(key, name),
                                   tip_for(TIP_FOE_ROW, name)))
                    info = label(self.foe_info(key, now), 11, DIM_TEXT, maxWidth=rw - 6)
                    lbls.append(info)
                    place(info, 2, y + 17)
                    sa.Add(info)
                    self.foe_rows.append((key, info))
                self.seen_ver = SIGHT["seen_ver"]
                self.seen_at = now + SEEN_REFRESH

            @staticmethod
            def foe_info(key, now):
                lk = link_text(key)
                seen = seen_text(key, now)
                return lk + "; " + seen if lk else seen

            def link_click(self, key):
                """[L]: the first press picks the entry, the second (on another)
                links the two as one person; again on the same one cancels."""
                if key not in FOES:
                    return
                pick = LINK_PICK[0]
                if pick is None or pick not in FOES:
                    LINK_PICK[0] = key
                    API.SysMsg(TITLE + (": now press L on the entry to link with %s "
                                        "(L on it again to cancel)." % FOES[key]), Kit.HUE_INFO)
                elif pick == key:
                    LINK_PICK[0] = None
                    API.SysMsg(TITLE + ": linking cancelled.", Kit.HUE_INFO)
                else:
                    LINK_PICK[0] = None
                    API.SysMsg(TITLE + ": " + link_foes(pick, key), Kit.HUE_GOOD)
                    request_save()
                STATE["foe_ver"] += 1             # the list is drawn again

            def unlink_click(self, key):
                if key in FOES and unlink_foe(key):
                    API.SysMsg(TITLE + (": %s is no longer linked." % FOES[key]), Kit.HUE_GOOD)
                    request_save()
                    STATE["foe_ver"] += 1

            def foe_name_click(self, key, name):
                """Alt+click a saved foe: auto-follow that player while one in range
                goes by that name; a plain click puts the name in the box."""
                if alt_held():
                    best, bt = None, -1.0
                    for s, k in FOE_SERIALS.items():          # (on a click only)
                        if k == key and API.FindMobile(s) is not None:
                            t = PRESENT.get(s, 0.0)           # the one seen last, if several
                            if t > bt:
                                best, bt = s, t
                    if best is not None:
                        toggle_follow(best)
                    else:
                        API.SysMsg(TITLE + (": %s isn't in range." % name), Kit.HUE_BAD)
                    return
                safe(lambda: self.input.SetText(name))

            def update(self):
                if self.gump is None:
                    return
                if self.foe_ver != STATE["foe_ver"]:
                    self.foe_ver = STATE["foe_ver"]
                    self.rebuild_foe_list()
                elif self.foe_rows:
                    now = time.time()             # "seen ... ago": on a new sighting, or now and then
                    if self.seen_ver != SIGHT["seen_ver"] or now >= self.seen_at:
                        self.seen_ver = SIGHT["seen_ver"]
                        self.seen_at = now + SEEN_REFRESH
                        for key, info in self.foe_rows:
                            set_text(info, self.foe_info(key, now))
                self.refresh_labels()


        # ----------------------------- SIGHTINGS WINDOW (2.6.05) ---------------------
        #  The log, newest first, a page of SIGHT_ROWS at a time: a pool of rows made
        #  with the window and only relabelled. Opened from the panel's "Sightings"
        #  button (or the Settings page); its X closes it (the module stays on).
        #  Minimize gives its own small bar; the gold arrow folds it into the Action
        #  Bar. Hidden (folded) it draws nothing; minimized, only its status line.
        class SightRow(object):
            """One reusable row: RowClick reads serial / name / prev at the click."""
            __slots__ = ("serial", "name", "prev", "e", "c", "nm", "here")

            def __init__(self):
                self.serial, self.name, self.prev, self.e = None, "", None, None
                self.c, self.nm, self.here = {}, "", None


        def make_sight_click(serial, name):
            def _clicked(*args):
                if alt_held():
                    toggle_follow(serial)          # (refuses, with a journal line, out of sight)
                    return
                SIGHT_WIN.filter_name(name)
            return _clicked


        SIGHT_LIST_H = 26 + SIGHT_ROWS * 22 + 6                       # the list section
        SIGHT_H = 2 * Kit.MARGIN + 30 + 36 + SIGHT_LIST_H + 36 + 3 * Kit.GAP


        def dock_hooks_scaled(*args):
            """(2.6.55) Kit.dock_hooks with scale=True: the layout may scale the
            window itself (it is rebuilt whole; its rows only change text). An
            older mother knows no scale= and gets the plain call."""
            try:
                return Kit.dock_hooks(*args, scale=True)
            except TypeError:
                return Kit.dock_hooks(*args)


        class SightingsWindow(object):
            KEY = "ultima.sightings"              # its dock key (Fold into the Action Bar)
            TITLE = "Sightings"
            W = 480
            MINI_W, MINI_H = 300, 46
            COLS = (8, 92, 230, 278, 404)         # time, player, notoriety, where, count

            def __init__(self):
                self.st = {"minimized": False, "docked": False, "shutting": True}
                self.win = {"g": None}
                self.hooks = dock_hooks_scaled(self.TITLE, SIGHT_TRAY_ICON, self.st, self.win,
                                               self.ask_redraw)
                self.flt = {"text": "", "noto": 0, "time": 0}
                self.forget()

            def forget(self):
                self.c, self.store, self.rows = {}, ({}, {}), []
                self.page, self.matches, self.counts = 0, [], {}
                self.ver = None                   # SIGHT["ver"] the list was worked out for
                self.ver_at = 0.0                 # (2.6.82) the list's last redraw + 1 s
                self.dirty = True                 # a filter or the page changed
                self.full_at = self.here_at = self.poll_at = 0.0
                self.redraw = False

            def is_open(self):
                return self.win["g"] is not None

            def ask_redraw(self):
                self.redraw = True                # (dock hooks: rebuilt on the next tick)

            def toggle(self):
                """The panel's button: open it; shown, close it; folded or
                minimized, bring it back."""
                if not self.is_open():
                    self.show()
                elif self.st["minimized"] or self.st["docked"]:
                    self.bring()
                else:
                    self.close()

            def bring(self):
                """Open, shown in full (not folded, not minimized)."""
                if not self.is_open():
                    self.show()
                if self.st["minimized"] or self.st["docked"]:
                    safe(lambda: HOST.dock_forget(self.KEY))
                    self.st["minimized"] = self.st["docked"] = False
                    Kit.save_min(SIGHT_MIN_KEY, False)
                    self.build()

            def show(self):
                if self.is_open():
                    return
                self.st.update(shutting=False, docked=False,
                               minimized=Kit.load_min(SIGHT_MIN_KEY)
                               or bool(safe(lambda: HOST.dock_wanted(self.KEY), False)))
                self.build()
                HOST.dock_add(self.KEY, self.hooks)
                Kit.put_var(SIGHT_OPEN_KEY, "1")

            def save_pos(self):
                Kit.save_pos(SIGHT_POS_KEY, self.win["g"])

            def close(self, stopping=False):
                """Its X (or the panel's button): closed, and closed next time too.
                stopping: the module stops; it opens again with the module."""
                g = self.win["g"]
                if g is None:
                    return
                self.st["shutting"] = True
                HOST.dock_remove(self.KEY)
                if not stopping:
                    safe(lambda: HOST.dock_forget(self.KEY))
                    Kit.put_var(SIGHT_OPEN_KEY, "0")
                Kit.save_pos(SIGHT_POS_KEY, g)
                Kit.save_min(SIGHT_MIN_KEY, self.st["minimized"])
                self.win["g"] = None
                self.forget()
                Kit.dispose(g)

            def lost(self):
                """Closed by the client (not by us): as if closed by its X."""
                self.win["g"] = None
                self.st["shutting"] = True
                HOST.dock_remove(self.KEY)
                Kit.put_var(SIGHT_OPEN_KEY, "0")
                self.forget()

            # ----- drawing -----
            def build(self):
                self.redraw = False
                old = self.win["g"]
                x, y = Kit.load_pos(SIGHT_POS_KEY, (320, 160), (self.W, SIGHT_H))
                if Kit.is_open(old):
                    x, y = old.GetX(), old.GetY()
                self.win["g"] = None
                self.forget()
                store, c, rows = self.store, self.c, self.rows
                M, GAP = Kit.MARGIN, Kit.GAP
                g = G.CreateGump(True, True)
                if self.st["minimized"]:
                    w, h = self.MINI_W, self.MINI_H
                    c["status"] = Kit.mini_bar(g, store, w, h, self.TITLE, self.KEY,
                                               queue_click(self.toggle_min), close_tip="Close")
                else:
                    w, h = self.W, SIGHT_H
                    IW = w - 2 * M
                    Kit.add_window_frame(g, w, h)
                    Kit.title_bar(g, store, w, self.TITLE, self.KEY, queue_click(self.toggle_min),
                                  queue_click(self.to_bar), queue_click(self.settings),
                                  close_tip="Close")
                    yf = M + 30 + GAP                                  # filters
                    Kit.add_section(g, M, yf, IW, 36)
                    Kit.add_label(g, "Find:", M + 10, yf + 9)
                    c["find"] = Kit.add_textbox(g, self.flt["text"], M + 52, yf + 7, 128,
                                                numbers=False)
                    safe(lambda: c["find"].SetTooltip(
                        "Type part of a name to list only that player's sightings"))
                    c["noto"] = Kit.art_button(g, store, "noto", Kit.ART_PAGE, M + 196, yf + 7,
                                               SIGHT_NOTO_FILTERS[self.flt["noto"]][0],
                                               "Which players to list; click for the next choice",
                                               on_click=queue_click(self.next_noto))
                    c["time"] = Kit.art_button(g, store, "time", Kit.ART_PAGE, M + 326, yf + 7,
                                               SIGHT_TIME_FILTERS[self.flt["time"]][0],
                                               "How far back to list; click for the next choice",
                                               on_click=queue_click(self.next_time))
                    yl = yf + 36 + GAP                                 # the list
                    Kit.add_section(g, M, yl, IW, SIGHT_LIST_H)
                    for x0, head in zip(self.COLS, ("Time", "Player", "Colour", "Where", "Count")):
                        Kit.add_label(g, head, M + x0, yl + 6, Kit.HUE_TITLE)
                    for i in range(SIGHT_ROWS):
                        ry = yl + 26 + i * 22
                        r = SightRow()
                        for k, x0, hue in (("t", 0, Kit.HUE_INFO), ("n", 1, Kit.HUE_TEXT),
                                           ("o", 2, Kit.HUE_TEXT), ("p", 3, Kit.HUE_INFO),
                                           ("k", 4, Kit.HUE_INFO)):
                            r.c[k] = Kit.add_label(g, "", M + self.COLS[x0], ry + 2, hue)
                        r.c["hit"] = Kit.catcher(g, M + 4, ry, IW - 8, 22,
                                                 queue_click(RowClick(r, make_sight_click)),
                                                 TIP_SIGHT)
                        rows.append(r)
                    yb = yl + SIGHT_LIST_H + GAP                       # pages and status
                    Kit.add_section(g, M, yb, IW, 36)
                    Kit.art_button(g, store, "newer", Kit.ART_PAGE, M + 10, yb + 7, "Prev",
                                   "Previous page (newer sightings)", on_click=queue_click(self.newer))
                    Kit.art_button(g, store, "older", Kit.ART_PAGE, M + 120, yb + 7, "Next",
                                   "Next page (older sightings)", on_click=queue_click(self.older))
                    c["status"] = Kit.add_label(g, "", M + 230, yb + 10, Kit.HUE_INFO)
                Kit.place(g, x, y, w, h)
                self.win["g"] = g
                G.AddGump(g)
                safe(lambda: Kit.on_moved(g, self.save_pos))
                if self.st["minimized"] and self.st["docked"]:      # folded into the Action Bar
                    safe(lambda: setattr(g, "IsVisible", False))
                Kit.dispose(old)
                self.refresh(time.time(), True)

            # ----- clicks (they run on the module's tick) -----
            def toggle_min(self, *args):
                self.st["minimized"] = not self.st["minimized"]
                self.st["docked"] = False
                safe(lambda: HOST.dock_forget(self.KEY))
                Kit.save_min(SIGHT_MIN_KEY, self.st["minimized"])
                self.build()

            def to_bar(self, *args):
                HOST.dock_to_bar(self.KEY, self.TITLE)

            def settings(self, *args):
                HOST.show_settings("ultima")

            def next_noto(self, *args):
                self.flt["noto"] = (self.flt["noto"] + 1) % len(SIGHT_NOTO_FILTERS)
                if "noto" in self.c:
                    Kit.set_text(self.c["noto"], SIGHT_NOTO_FILTERS[self.flt["noto"]][0])
                self.page, self.dirty = 0, True

            def next_time(self, *args):
                self.flt["time"] = (self.flt["time"] + 1) % len(SIGHT_TIME_FILTERS)
                if "time" in self.c:
                    Kit.set_text(self.c["time"], SIGHT_TIME_FILTERS[self.flt["time"]][0])
                self.page, self.dirty = 0, True

            def newer(self, *args):
                if self.page > 0:
                    self.page -= 1
                    self.dirty = True

            def older(self, *args):
                if (self.page + 1) * SIGHT_ROWS < len(self.matches):
                    self.page += 1
                    self.dirty = True

            def filter_name(self, name):
                """A row's click: only that player (again: everyone)."""
                new = "" if self.flt["text"].lower() == name.lower() else name
                tb = self.c.get("find")
                if tb is not None:
                    safe(lambda: tb.SetText(new))
                self.flt["text"] = new
                self.page, self.dirty = 0, True

            # ----- every tick -----
            def tick(self, now):
                if self.win["g"] is None:
                    return
                if Kit.was_clicked(self.store, "close"):
                    self.close()
                    return
                if self.redraw:
                    self.build()
                    return
                if now < self.poll_at:
                    return
                self.poll_at = now + TICK_SECONDS
                if not Kit.is_open(self.win["g"]):
                    self.lost()
                    return
                if self.st["minimized"] and self.st["docked"]:
                    return                            # folded: nothing drawn
                self.refresh(now)

            def refresh(self, now, force=False):
                c = self.c
                if self.st["minimized"]:              # the status line only
                    if force or SIGHT["ver"] != self.ver or now >= self.full_at:
                        self.ver, self.full_at = SIGHT["ver"], now + SIGHT_REFRESH
                        n = len(SIGHTS)
                        text = "%s: %d" % (self.TITLE, n)     # "Sightings: 12, last Bob 12:30"
                        if n:
                            e = SIGHTS[-1]
                            text += ", last %s %s" % (e[S_NAME], stamp(e[S_T], today_start(now)))
                        else:
                            text = "%s: none yet" % self.TITLE
                        Kit.set_text(c["status"], Kit.fit(text, self.MINI_W - 90))
                    return
                tb = c.get("find")
                if tb is not None:
                    try:
                        txt = str(tb.Text or "").strip()
                    except Exception:
                        txt = self.flt["text"]
                    if txt != self.flt["text"]:
                        self.flt["text"] = txt
                        self.page, self.dirty = 0, True
                # (2.6.82) new sightings redraw the list at most once a second
                if force or self.dirty or now >= self.full_at or \
                        (SIGHT["ver"] != self.ver and not 0.0 <= self.ver_at - now <= 1.0):
                    self.ver_at = now + 1.0
                    self.work_out(now)
                    self.fill(now)
                elif now >= self.here_at:
                    self.mark_here(now)

            def work_out(self, now):
                """The sightings that pass the filters, newest first, and how many
                of them each name has."""
                self.dirty = False
                self.ver, self.full_at = SIGHT["ver"], now + SIGHT_REFRESH
                tf = SIGHT_TIME_FILTERS[self.flt["time"]][1]
                cut = None if tf is None else (today_start(now) if tf == "today" else now - tf)
                nf = SIGHT_NOTO_FILTERS[self.flt["noto"]][1]
                find = name_key(self.flt["text"])
                out, counts = [], {}
                for i in range(len(SIGHTS) - 1, -1, -1):
                    e = SIGHTS[i]
                    if cut is not None and e[S_T] < cut:
                        break                         # (the log is in time order)
                    if find and find not in e[S_KEY]:
                        continue
                    if nf is not None and (e[S_KEY] not in FOES if nf == "foe"
                                           else e[S_NOTO] not in nf):
                        continue
                    out.append(e)
                    counts[e[S_KEY]] = counts.get(e[S_KEY], 0) + 1
                self.matches, self.counts = out, counts
                last = max(0, (len(out) - 1) // SIGHT_ROWS)
                if self.page > last:
                    self.page = last

            def fill(self, now):
                today0 = today_start(now)
                start = self.page * SIGHT_ROWS
                m = self.matches
                for i, r in enumerate(self.rows):
                    j = start + i
                    self.assign(r, m[j] if j < len(m) else None, today0)
                self.mark_here(now)
                n = len(m)
                if n:
                    text = "%d-%d of %d, %d name%s" % (start + 1, min(n, start + SIGHT_ROWS), n,
                                                       len(self.counts),
                                                       "" if len(self.counts) == 1 else "s")
                elif SIGHTS:
                    text = "No sightings match the filters"
                else:
                    text = "No sightings yet" if UI["sightings"] else \
                        "Logging is off (settings page)"
                Kit.set_text(self.c["status"], Kit.fit(text, self.W - 2 * Kit.MARGIN - 236))

            def assign(self, r, e, today0):
                c = r.c
                if e is None:
                    if r.e is not None:
                        r.prev = (r.serial, r.name, time.time())
                        r.e, r.serial, r.name, r.nm, r.here = None, None, "", "", None
                        for k in ("t", "n", "o", "p", "k"):
                            Kit.set_text(c[k], "")
                    return
                if e is not r.e:
                    if r.serial is not None and r.serial != e[S_SERIAL]:
                        r.prev = (r.serial, r.name, time.time())
                    r.e, r.serial, r.name = e, e[S_SERIAL], e[S_NAME]
                    r.nm, r.here = Kit.fit(e[S_NAME], 124), None
                    Kit.set_text(c["o"], noto_word(e[S_NOTO]), NOTO_HUE.get(e[S_NOTO], Kit.HUE_TEXT))
                    where = place_text(e[S_FACET], e[S_X], e[S_Y])
                    Kit.set_text(c["p"], Kit.fit(where + (" G" if e[S_GUARD] else ""), 118))
                    g = e[S_GUARD]
                    extra = "Seen %s at %s%s" % (stamp(e[S_T], today0), where,
                                                 ", in a guard zone (G)" if g else
                                                 (", outside the guards" if g is False else ""))
                    try:
                        c["hit"].SetTooltip(tip_for(TIP_SIGHT, e[S_NAME], extra))
                    except Exception:
                        pass
                Kit.set_text(c["t"], stamp(e[S_T], today0))
                Kit.set_text(c["k"], "x%d" % self.counts.get(e[S_KEY], 1))

            def mark_here(self, now):
                """Names of players still in range are green (a look a second)."""
                self.here_at = now + 1.0
                for r in self.rows:
                    if r.e is None:
                        continue
                    t = PRESENT.get(r.serial)
                    here = t is not None and now - t <= 2 * TICK_SECONDS + 0.05
                    if here != r.here:
                        r.here = here
                        Kit.set_text(r.c["n"], r.nm, Kit.HUE_GOOD if here else Kit.HUE_TEXT)


        # ------------------------- DEATH WINDOW (2.6.05) -----------------------------
        #  "Add my killer": opened when you die, listing who attacked you in the
        #  last KILLER_BACK seconds, each with "Add to foes". It closes when you are
        #  resurrected, after KILLER_SHOW seconds, or with its X. Built once per death.
        class KillerWindow(object):
            TITLE = "Add my killer"
            W = 340
            MINI_W, MINI_H = 260, 46
            ROW_H = 26

            def __init__(self):
                self.g = None
                self.store = ({}, {})
                self.c = {}
                self.cands = []
                self.until = 0.0
                self.minimized = False

            def height(self):
                return 2 * Kit.MARGIN + 30 + Kit.GAP + 8 + len(self.cands) * self.ROW_H + 26

            def open(self, got, now, total=None):
                """got: [name, time, serial or None], newest first (the ones listed);
                total: how many attacked you (more than are listed past KILLER_ROWS)."""
                self.cands = [{"name": a[0], "serial": a[2]} for a in got]
                self.until = now + KILLER_SHOW
                self.minimized = Kit.load_min(KILLER_MIN_KEY)
                self.build()
                n = len(got) if total is None else total
                which = "them" if n == len(got) else "the last %d" % len(got)
                API.SysMsg(TITLE + (": you died; %d player%s attacked you. Add %s to your Foe "
                                    "list in the %s window." % (n, "" if n == 1 else "s", which,
                                                                 self.TITLE)), Kit.HUE_BAD)

            def save_pos(self):
                Kit.save_pos(KILLER_POS_KEY, self.g)

            def close(self):
                g = self.g
                if g is None:
                    return
                Kit.save_pos(KILLER_POS_KEY, g)
                Kit.save_min(KILLER_MIN_KEY, self.minimized)
                self.g, self.c, self.cands = None, {}, []
                Kit.dispose(g)

            def build(self):
                old = self.g
                W, H = self.W, self.height()
                sw, sh = Kit.screen()
                x, y = Kit.load_pos(KILLER_POS_KEY, (max(0, ((sw or 1024) - W) // 2),
                                                     max(0, ((sh or 768) - H) // 3)), (W, H))
                if Kit.is_open(old):
                    x, y = old.GetX(), old.GetY()
                self.g = None
                store, c = ({}, {}), {}
                M = Kit.MARGIN
                g = G.CreateGump(True, True)
                if self.minimized:
                    W, H = self.MINI_W, self.MINI_H
                    n = len(self.cands)
                    c["status"] = Kit.mini_bar(g, store, W, H, self.TITLE, "ultima.killer",
                                               queue_click(self.toggle_min),
                                               "%s: %d attacker%s" % (self.TITLE, n,
                                                                      "" if n == 1 else "s"),
                                               close_tip="Close")
                else:
                    IW = W - 2 * M
                    Kit.add_window_frame(g, W, H)
                    Kit.add_section(g, M, M, IW, 30)
                    Kit.add_label(g, self.TITLE.upper(), M + 30, M + 7, Kit.HUE_TITLE)
                    Kit.title_catcher(g, M, M, W - M - 80 - M, 30, queue_click(self.toggle_min),
                                      key="ultima.killer")
                    Kit.art_button(g, store, "min", Kit.ART_MIN, W - M - 74, M + 7, None,
                                   "Minimize (double-click the title does too)",
                                   on_click=queue_click(self.toggle_min))
                    Kit.art_button(g, store, "close", Kit.ART_CLOSE, W - M - 54, M + 4, None,
                                   "Close")
                    yb = M + 30 + Kit.GAP
                    Kit.add_section(g, M, yb, IW, H - yb - M)
                    cap = "Add to foes"
                    bx = W - M - 10 - (35 + Kit.text_w(cap))
                    for i, a in enumerate(self.cands):
                        ry = yb + 8 + i * self.ROW_H
                        on = name_key(a["name"]) in FOES
                        Kit.add_label(g, Kit.fit(a["name"], bx - M - 30), M + 10, ry + 3,
                                      Kit.HUE_BAD)
                        Kit.catcher(g, M + 6, ry, bx - M - 14, 22,
                                    queue_click(self.make_follow(i)),
                                    tip_for("Alt+click: auto-follow (again to stop)", a["name"]))
                        c["add%d" % i] = Kit.art_button(
                            g, store, "add%d" % i, Kit.ART_OK, bx, ry, "On Foe list" if on else cap,
                            "Put %s on your Foe list. Alt+click: auto-follow (again to stop)"
                            % a["name"], on_click=queue_click(self.make_add(i)))
                    Kit.add_label(g, "Closes when you are resurrected.", M + 10,
                                  yb + 8 + len(self.cands) * self.ROW_H + 2, Kit.HUE_INFO)
                Kit.place(g, x, y, W, H)
                self.g, self.store, self.c = g, store, c
                G.AddGump(g)
                safe(lambda: Kit.on_moved(g, self.save_pos))
                Kit.dispose(old)

            def make_add(self, i):
                def _add(*args):
                    if i >= len(self.cands):
                        return
                    if alt_held():                 # (Alt+click: follow, as on the name)
                        self.make_follow(i)()
                        return
                    a = self.cands[i]
                    if name_key(a["name"]) in FOES:
                        API.SysMsg(TITLE + (": %s is already on the Foe list." % a["name"]),
                                   Kit.HUE_INFO)
                    else:
                        add_foe(a["name"])
                        API.SysMsg(TITLE + (": added %s to the Foe list." % a["name"]),
                                   Kit.HUE_GOOD)
                    lbl = self.c.get("add%d" % i)
                    if lbl is not None:
                        Kit.set_text(lbl, "On Foe list")
                return _add

            def make_follow(self, i):
                def _follow(*args):
                    if i >= len(self.cands) or not alt_held():
                        return
                    a = self.cands[i]
                    s = a["serial"]
                    if s is None:
                        s, _ = find_named(a["name"])
                    if s is None:
                        API.SysMsg(TITLE + (": %s isn't in sight." % a["name"]), Kit.HUE_BAD)
                    else:
                        toggle_follow(s)
                return _follow

            def toggle_min(self, *args):
                self.minimized = not self.minimized
                Kit.save_min(KILLER_MIN_KEY, self.minimized)
                self.build()

            def tick(self, now):
                if self.g is None:
                    return
                if Kit.was_clicked(self.store, "close") or now >= self.until:
                    self.close()
                elif not Kit.is_open(self.g):
                    self.g, self.c, self.cands = None, {}, []      # closed by the client


        SIGHT_WIN = SightingsWindow()
        KILLER_WIN = KillerWindow()


        # ------------------------------- NPC NAMES -----------------------------------
        # Town NPCs on this kind of server get a random first name from fixed lists
        # (RunUO/ServUO Data/names.xml, "male" + "female"). A blue human with one of
        # these names is treated as an NPC unless it has acted like a player.
        NPC_NAMES_DATA = (
            "Aaron,Aasin,Aba,Abbott,Abby,Abdel,Abdiel,Abel,Abella,Abey,Abigail,Abijah,"
            "Abina,Abiona,Abira,Abner,Abra,Abrah,Abraham,Abran,Absinthe,Acacia,Acanit,"
            "Acantha,Accalia,Ace,Acelin,Achen,Achilles,Ackerley,Ada,Adair,Adalia,Adam,"
            "Adara,Addi,Addison,Adeben,Adelaide,Adele,Adelia,Adeline,Adelle,Adem,Adena,"
            "Aderes,Adesina,Adie,Adimina,Adiran,Adiva,Adlai,Adler,Adley,Admon,Adolph,"
            "Adon,Adoncia,Adonia,Adonis,Adora,Adrian,Adriel,Adrienne,Aelina,Aeneas,"
            "Afina,Afra,Afrika,Afton,Agate,Agatha,Agnes,Agustin,Ahara,Ahave,Ahearn,"
            "Ahimsa,Ahmik,Ahren,Aida,Aidan,Aiella,Aiken,Aiko,Aila,Aileen,Ailsa,Aimee,"
            "Aimery,Ain,Aina,Ainhoa,Ainsley,Aintzane,Airlia,Aisling,Aislinn,Aitan,"
            "Aithne,Aiyana,Ajara,Ajay,Ajayi,Ajinora,Akako,Akala,Akando,Akanke,Akasma,"
            "Akbaar,Akela,Akello,Akil,Akilah,Akili,Akilina,Akina,Akshay,Alaina,Alake,"
            "Alala,Alamanada,Alan,Alana,Aland,Alani,Alanna,Alano,Alaqua,Alaric,"
            "Alastair,Alavda,Alazne,Alben,Albert,Alberta,Albinka,Alcander,Alcina,"
            "Alcott,Aldea,Alden,Alder,Aldercy,Aldrick,Alec,Alek,Aleka,Aleksy,Alenne,"
            "Aleron,Aleser,Alesia,Alessa,Alethea,Alex,Alexa,Alexander,Alexandra,"
            "Alexandria,Alexandrina,Alexis,Alfred,Alger,Ali,Alia,Alice,Alicia,Alida,"
            "Alike,Alim,Alima,Alina,Alison,Alistair,Alita,Alix,Aliz,Aliza,Allaard,"
            "Allan,Allard,Allele,Allen,Alligra,Allinora,Allison,Allyn,Alma,Alodie,"
            "Alonzo,Aloysia,Alphonse,Alphonso,Alston,Altair,Althea,Alton,Alula,Alumit,"
            "Alvin,Alvina,Alvita,Alysa,Alyssa,Alyssand,Alzena,Ama,Amabel,Amadeo,Amadi,"
            "Amadika,Amadis,Amado,Amaia,Amala,Amalia,Amanda,Amandine,Amara,Amarande,"
            "Amarante,Amaris,Amata,Ambar,Amber,Ambika,Ambis,Ambrose,Ameerah,Amelia,"
            "Amelina,Amethyst,Amie,Amiel,Amiella,Amina,Aminta,Amissa,Amita,Amity,Ammon,"
            "Amoke,Amos,Amsden,Amy,Ananda,Anastasia,Ancelin,Anders,Andi,Andra,"
            "Andraianna,Andras,Andre,Andrea,Andreus,Andrew,Andrey,Andries,Andromeda,"
            "Aneida,Anella,Anemone,Anezka,Angela,Angelica,Angeline,Angelique,Angelo,"
            "Angeni,Angus,Ani,Anica,Anieli,Anisa,Anita,Anke,Anker,Ann,Anna,Annabel,"
            "Annabelle,Annamarie,Anne,Annette,Annikka,Annora,Anoki,Anorah,Anoush,Ansel,"
            "Anselme,Ansley,Anson,Ansreana,Anteia,Anthea,Anthony,Antje,Antoinette,"
            "Antonia,Antonio,Anwar,Aolani,Apara,Apirka,Apolline,Apolloina,Aponi,April,"
            "Aprille,Aqua,Aquene,Ara,Arabella,Arabelle,Araceli,Araminta,Araxie,Arcadia,"
            "Archer,Archibald,Ardath,Ardelia,Arden,Ardis,Ardith,Ardon,Areiela,Arella,"
            "Aren,Ares,Aretha,Aretina,Argus,Ari,Ariadne,Ariana,Aricia,Aricin,Ariel,"
            "Ariene,Arion,Arista,Aristo,Aristotle,Arkin,Arlen,Arlene,Arley,Arlin,"
            "Arlinda,Arlo,Arman,Armen,Armina,Arminda,Armon,Armstrong,Arne,Arnold,Arnon,"
            "Aron,Arpiar,Arsen,Arsenio,Artemisia,Arthur,Aruna,Arziki,Asaria,Asenka,Ash,"
            "Asha,Ashby,Asher,Ashford,Ashlan,Ashleigh,Ashley,Ashlin,Ashon,Ashur,Asia,"
            "Asisa,Aslinda,Aspasia,Asta,Aster,Astera,Astra,Astrea,Astrid,Atalanta,"
            "Atara,Atenne,Ateri,Athalia,Athan,Athena,Atheron,Athla,Atifa,Atman,Atta,"
            "Aubrey,Auda,Audny,Audrey,Audrianna,Audric,Audun,Augustin,Augustina,"
            "Augustus,Aura,Aure,Aurek,Aurelia,Aurilia,Aurina,Aurkene,Aurora,Austin,"
            "Autumn,Ava,Avana,Avasa,Avella,Avena,Averill,Avery,Avie,Avis,Aviva,Axel,"
            "Axella,Aya,Ayaluna,Ayame,Ayana,Ayasha,Aydee,Ayela,Ayiana,Ayila,Ayisha,"
            "Ayita,Ayla,Aynora,Ayuna,Azaleah,Azalia,Azarael,Azera,Azha,Azilea,Azina,"
            "Azize,Azora,Azura,Babette,Bacia,Bae,Bailey,Baingana,Baka,Bakari,Bakarne,"
            "Balayna,Balbo,Balder,Baldwin,Bale,Balea,Balendin,Bali,Balia,Balin,Balint,"
            "Bambi,Banan,Bancroft,Bandele,Bane,Banella,Banning,Bara,Baran,Barbara,"
            "Barclay,Barden,Bardo,Bardon,Barika,Barnabas,Barnaby,Barnett,Barney,Baron,"
            "Barrett,Barry,Barse,Bart,Barth,Bartholomew,Barton,Basha,Basia,Basil,"
            "Basimah,Bastiaan,Batakah,Bathsheba,Batya,Baul,Bavol,Baxter,Bay,Bayana,"
            "Bayani,Bayard,Baylor,Bayo,Bayta,Bazyli,Bea,Beacan,Beagan,Beaman,Beatrice,"
            "Beatrix,Beau,Beauina,Beaumont,Beauregard,Becca,Beck,Becky,Bedelia,Bel,"
            "Belana,Beldon,Belen,Belina,Belinda,Belita,Bellanca,Belle,Belora,Bem,Beman,"
            "Ben,Benedict,Benen,Benjamin,Bennett,Benson,Bent,Bente,Bentley,Benton,"
            "Beradine,Berenger,Bergren,Berilla,Berit,Berk,Berkeley,Bernadette,Bernard,"
            "Bernice,Bersh,Bert,Berthold,Berton,Bertram,Beryl,Bess,Bessine,Beta,Beth,"
            "Bethana,Bethany,Betony,Betty,Beulah,Beval,Bevan,Beverly,Bevin,Bialy,Bian,"
            "Bianca,Bilal,Billie,Bina,Bindy,Binti,Birdie,Birkita,Bishop,Bitalo,Bixenta,"
            "Bjorn,Blade,Blaine,Blair,Blaise,Blake,Blanche,Blanda,Blaz,Blenda,Bliss,"
            "Blorn,Bly,Blythe,Bo,Boden,Bogart,Bohdan,Bohdana,Bolton,Bonamy,Bond,Bonita,"
            "Bonnie,Bonny,Booker,Boone,Borden,Borgny,Boris,Botan,Bowie,Bowman,Boyce,"
            "Boyd,Boyden,Brad,Braden,Bradford,Bradney,Brady,Braina,Bram,Bran,Brand,"
            "Brandeis,Brandi,Brandon,Brandy,Brant,Braxton,Bray,Braz,Brazil,Bren,"
            "Brencis,Brenda,Brendan,Brendon,Brenna,Brennan,Brent,Brentan,Bret,Brett,"
            "Bretta,Brewster,Briac,Brian,Briand,Brice,Bridget,Brie,Brieg,Brier,Brietta,"
            "Brigit,Brigitte,Brina,Brinley,Briona,Briony,Brishen,Brites,Britta,"
            "Brittany,Brock,Broderick,Brodny,Brody,Bronson,Bront,Bronwyn,Brooke,Bruce,"
            "Bruno,Brutus,Bryan,Bryant,Bryce,Brynn,Bryson,Bucia,Buck,Bud,Budo,Burgess,"
            "Burhan,Burian,Burke,Burl,Burr,Burton,Byran,Byron,Cadence,Cadeo,Cador,"
            "Caedmon,Cailan,Caimile,Cain,Caine,Caitlin,Caitrin,Cala,Calandia,Calandra,"
            "Calder,Caldwell,Caleb,Calendonia,Caley,Calida,Calista,Calla,Callan,Callia,"
            "Callidora,Callie,Caltha,Calvin,Calypso,Cam,Camden,Camelia,Cameron,Camilia,"
            "Camille,Canace,Candace,Candan,Candida,Candide,Candra,Cantara,Canton,"
            "Canute,Caoimhe,Capri,Caprice,Cara,Caradoc,Carden,Caresse,Carey,Cari,"
            "Carina,Carine,Carissa,Carita,Carl,Carla,Carleen,Carlen,Carlin,Carling,"
            "Carlo,Carlos,Carlota,Carlton,Carly,Carma,Carmel,Carmelina,Carmen,Carna,"
            "Carnelian,Carol,Carolina,Caroline,Carolyn,Caron,Carr,Carrick,Carrie,"
            "Carrocio,Carroll,Carson,Carter,Carver,Caryn,Casey,Casilda,Casper,"
            "Cassandra,Cassia,Cassidy,Cassius,Casta,Castalia,Castel,Catalina,Catava,"
            "Caterina,Catherine,Cathleen,Cathy,Cato,Caton,Catriona,Cavan,Cayla,Ceara,"
            "Ceasar,Cecania,Cecil,Cecilia,Cedric,Celandine,Celeste,Celia,Celina,Cellia,"
            "Cemal,Cerelia,Chad,Chadwick,Chaim,Chaitra,Chal,Chale,Chalmers,Chanah,"
            "Chanda,Chander,Chandi,Chandler,Chandra,Chane,Chanel,Chaney,Channa,"
            "Channing,Chantal,Chapin,Chapman,Charis,Charissa,Charity,Charles,Charlotte,"
            "Charlton,Charmaine,Chase,Chastity,Chatha,Chauncy,Chava,Chaviva,Chay,Chaya,"
            "Chayton,Chelsea,Chen,Cheney,Chenoa,Cherica,Cherice,Cherie,Cheryl,Chesna,"
            "Chester,Chet,Chevalier,Chiara,Chika,Chike,Chilali,Chimlis,Chin,Chipo,"
            "Chloe,Chloris,Cho,Christa,Christable,Christian,Christina,Christine,"
            "Christoph,Christopher,Christos,Christy,Chuck,Chyou,Cia,Ciannait,Ciar,"
            "Cicely,Ciceron,Cindy,Ciro,Claire,Clara,Clarence,Clarinda,Clarissa,Clark,"
            "Claude,Claudette,Claudia,Claudine,Clay,Clayton,Clement,Clementina,"
            "Clementine,Cleveland,Cliantha,Clifford,Clifton,Clint,Clinton,Clive,"
            "Clorinda,Clover,Clyde,Cochiti,Cody,Colby,Cole,Coleene,Coleman,Colette,"
            "Colin,Collin,Colon,Colton,Coman,Condon,Connie,Connor,Conrad,Constance,"
            "Constanza,Consuela,Conway,Cora,Coralie,Corazon,Corbett,Corbey,Corbin,"
            "Corcoran,Cordeali,Cordell,Coretta,Corey,Cori,Corinna,Coris,Corliss,"
            "Cornelius,Corrine,Cort,Cortney,Coty,Courtland,Craig,Crandall,Creighton,"
            "Crescent,Cressida,Crispin,Crosby,Crystal,Cullen,Cullin,Culver,Curran,"
            "Curtis,Cybele,Cybil,Cynric,Cynthia,Cyprien,Cyrano,Cyrene,Cyril,Cyrilla,"
            "Cyrus,Cytheria,Dabria,Dacey,Dacia,Dacie,Dacio,Dae,Dag,Dagan,Dagmar,Dagna,"
            "Dai,Daily,Daisel,Daisy,Dakarai,Dakota,Dale,Dalila,Dalilia,Dallin,Dalton,"
            "Daly,Damara,Damek,Damen,Damian,Damien,Damion,Damitri,Damon,Dana,Dane,"
            "Danett,Dania,Daniel,Daniella,Danior,Dannik,Dante,Danyelle,Daphene,Daphne,"
            "Daphnie,Dar,Dara,Daralis,Darby,Daren,Daria,Darien,Dario,Darla,Darlene,"
            "Darnell,Darrel,Darrell,Darren,Daryl,Dasha,Davene,David,Davin,Davine,Davis,"
            "Davita,Dawn,Daya,Dayna,Deacon,Dean,Deana,Deandra,Deb,Debra,Decker,Dede,"
            "Dee,Deedee,Deianira,Deiene,Deirdre,Delana,Delaney,Delano,Delbert,Delbin,"
            "Delia,Delicia,Delilia,Della,Dellan,Delmore,Delphina,Delsin,Deman,Dembe,"
            "Demi,Demitria,Dempsey,Dempster,Dena,Denby,Denice,Dennis,Dennys,Denton,"
            "Denver,Der,Derek,Derrick,Derry,Deva,Devaki,Deval,Deverell,Devi,Devin,"
            "Devlin,Devnet,Devon,Dewey,Diamanta,Diane,Dianthe,Diederik,Diedre,Diego,"
            "Diella,Dieter,Dillian,Dillon,Dilly,Dilys,Dimitri,Dinah,Dionne,Dirk,Disa,"
            "Dita,diti,Dixie,Dobry,Dodie,Dolores,Dominic,Dominick,Dominique,Dona,"
            "Donald,Donata,Donatien,Donato,Donielle,Donnelley,Donnelly,Donner,Donovan,"
            "Dooriya,Dophina,Dora,Doreen,Dorinda,Doris,Dorithy,Doron,Dory,Dougie,"
            "Douglas,Douglass,Dov,Doyle,Drake,Drew,Drina,Drucilla,Duane,Dugan,Duglas,"
            "Dulcie,Dulcinea,Duncan,Dunstan,Durand,Durriken,Dusan,Dustin,Dusty,Dutch,"
            "Dwayne,Dwight,Dyami,Dyan,Dyani,Dyastro,Dylan,Dymas,Dymphna,Dyna,Eamon,"
            "Earl,Earle,Eartha,Easter,Eaton,Ebony,Echo,Edan,Edana,Edgan,Edgar,Edie,"
            "Edison,Edith,Edlyn,Edmund,Edna,Edolie,Edria,Edrin,Edward,Edwin,Edwina,"
            "Efia,Egan,Eileen,Einar,Eirene,Elad,Elaine,Elana,Elden,Eldroth,Elek,Eleora,"
            "Eli,Elianor,Elias,Elijah,Elina,Elisa,Elise,Eliska,Elissa,Elita,Eliza,"
            "Elizabeeth,Elkan,Elke,Ella,Elle,Ellen,Ellery,Elliot,Elliott,Ellis,"
            "Ellsworth,Elly,Elmer,Elmo,Elodie,Eloise,Elsa,Elsie,Elston,Elton,Elwood,"
            "Elynor,Elyse,Elysia,Ema,Emajane,Emalia,Emanuel,Ember,Emelie,Emelyne,Emil,"
            "Emilio,Emily,Emma,Emmett,Emo,Endora,Engracia,Enid,Enoch,Enola,Enrico,"
            "Enrique,Enye,Ephraim,Erasma,Erek,Erianthe,Eric,Erica,Erik,Erin,Erlina,"
            "Ernest,Erol,Errol,Erskine,Erwand,Erwin,Eryx,Eskarne,Esmerelda,Esperanza,"
            "Essien,Esta,Esteban,Estelle,Esther,Estu,Etain,Etaina,Etanthe,Ethan,Etta,"
            "Eudocia,Eugene,Eugenia,Eulalia,Eustacia,Eva,Evacsa,Evadine,Evadne,Evan,"
            "Evander,Evangeline,Evanthe,Eve,Evelyn,Everett,Evita,Evonne,Evzen,Eyota,"
            "Ezekial,Ezra,Fabienne,Fabio,Faifuza,Fainche,Fairfax,Faith,Faizah,Fallon,"
            "Fantine,Farha,Farima,Farley,Farrah,Farrell,Fatin,Fawne,Faxon,Fay,Faye,"
            "Fayina,Fayme,Felcia,Felicite,Felicity,Felix,Femi,Fenn,Fenton,Fergus,"
            "Feridwyn,Fern,Feronia,Ferran,Ferris,Fielding,Filbert,Filinda,Filmore,Fina,"
            "Finlay,Finley,Finn,Finnigan,Finola,Fiona,Fiorenza,Fisk,Fitzgerald,Flavia,"
            "Fleta,Fletcher,Flindo,Flint,Flora,Florence,Floyd,Flynn,Forbes,Forrest,"
            "Forsythe,Foster,Frances,Francesca,Francine,Francis,Francisca,Franek,Frank,"
            "Franklin,Frasier,Frazer,Frazier,Fred,Freda,Frederica,Frederick,Fremont,"
            "Freya,Frida,Frieda,Fritz,Fuller,Fulton,Fuscienne,Gabe,Gabriel,Gabriella,"
            "Gabrielle,Gage,Gaia,Gail,Galatea,Galen,Galeno,Gali,Galina,Galvin,Galya,"
            "Gamble,Gana,Ganesa,Gannon,Gareth,Garfield,Gargan,Garner,Garrett,Garrick,"
            "Garridan,Garrison,Garritt,Garth,Garvin,Gary,Gaspar,Gaston,Gauri,Gavin,"
            "Gavrie,Gaye,Gayle,Gaylord,Gaynor,Gelasia,Gemma,Genevieve,Geoff,Geoffrey,"
            "Geoffry,Geogia,George,Georgeanne,Georgetta,Georgette,Georgiana,Geradline,"
            "Geraldine,Gerard,Gerda,Gerik,Germain,Gerri,Gerry,Gertrude,Geva,Ghislaine,"
            "Giacinta,Gianina,Gideon,Gigi,Gilana,Gilberto,Gilda,Gilen,Giles,Gillian,"
            "Gin,Gina,Ginger,Ginton,Giselle,Gitana,Githa,Givon,Gizane,Gleda,Glen,Glenn,"
            "Glenna,Glenno,Glennys,Godfrey,Golda,Goldie,Gordon,Gordy,Gorman,Gotzone,"
            "Grace,Gracie,Grady,Graham,Grainne,Gram,Granger,Grant,Granville,Grayson,"
            "Grazia,Grear,Greg,Greger,Gregor,Gregory,Gresham,Greta,Gretchen,Grette,"
            "Griffen,Griffith,Guilhem,Gunnar,Gunther,Gus,Gustave,Guthrie,Guy,Gwen,"
            "Gwendolyn,Gweneth,Gwynne,Gytha,Hackett,Hadara,Hadassa,Hadden,Hadi,Hadiya,"
            "Hadley,Hadrian,Hagan,Haidee,Hailey,Haimi,Hal,Halden,Haldis,Hale,Haley,"
            "Hali,Halian,Halima,Halle,Hallie,Halsey,Hamilton,Hamlin,Hana,Hanan,Hank,"
            "Hannah,Hanne,Hans,Harden,Hardy,Harith,Harlan,Harman,Harmoni,Harold,Harper,"
            "Harriet,Harrison,Harry,Hart,Hartley,Harvey,Hasna,Hassan,Hastin,Hastings,"
            "Hava,Haya,Hayden,Hayes,Haylee,Haynes,Hazel,Hea,Heath,Heather,Hector,Hei,"
            "Heidi,Helaku,Heldegarde,Helen,Helena,Helene,Helki,Henka,Henning,Henrietta,"
            "Henry,Herbert,Herman,Herschel,Hesper,Hester,Hilary,Hilda,Hilliard,Hilton,"
            "Hinda,Hiroshi,Hisa,Hobart,Hogan,Holden,Holly,Holt,Homes,Hope,Horace,"
            "Horton,Hoshi,Houston,Howard,Howrence,Hoyt,Hugh,Hugo,Humphrey,Hunter,"
            "Huntley,Hyacinth,Hye,Hyman,Hypatia,Iain,Ida,Idola,Idonia,Ilene,"
            "Ilias,Ilona,Iman,Imogene,India,Indira,Indra,Ines,Inez,Inga,Ingmar,Ingram,"
            "Ingrid,Iolana,Iolanthe,Iona,Ira,Iratze,Irena,Irene,Iris,Irma,Irvin,Irving,"
            "Irwin,Isaac,Isabeau,Isabel,Isabella,Isadora,Isaiah,Isaura,Isis,Isleta,"
            "Isobel,Isoke,Israel,Istas,Itzak,Ivan,Ivana,Ivar,Ivory,Ivy,Jabari,Jabir,"
            "Jacelyn,Jacinda,Jacinthe,Jack,Jacob,Jacobe,Jacques,Jacson,Jacy,Jada,Jael,"
            "Jaen,Jafar,Jagger,Jaimie,Jaione,Jake,Jakinda,Jal,Jala,Jaleel,Jamal,James,"
            "Jamie,Jamila,Jamilah,Jamison,Jan,Jana,Jane,Janelle,Janet,Janice,Janis,"
            "Janna,Jannelle,Jardena,Jared,Jarek,Jarman,Jaron,Jarrod,Jarvia,Jarvinia,"
            "Jarvis,Jasmine,Jason,Jasper,Javan,Javier,Jay,Jaya,Jayne,Jean,Jeanette,"
            "Jeanine,Jebidiah,Jed,Jedidiah,Jedrek,Jeff,Jeffrey,Jelani,Jelena,Jena,"
            "Jenay,Jendayi,Jendyose,Jenica,Jennettia,Jennifer,Jensine,Jeremiah,Jeremy,"
            "Jerolin,Jerome,Jeromy,Jerrilyn,Jerzy,Jesse,Jessee,Jessica,Jethro,Jewel,"
            "Jezebel,Jibril,Jihan,Jillian,Jin,Jina,Jinny,Jinx,Jiro,Jivin,Joakima,Joan,"
            "Joanne,Jobey,Jobihna,Jocasa,Jocelyn,Jodi,Jody,Joel,Joelle,Joelliane,"
            "Johann,Johanna,John,Joia,Jolan,Jolanta,Jolene,Jolie,Joline,Jolon,Jonah,"
            "Jonathan,Jonathon,Jonina,Jora,Jordan,Jordane,Jordon,Jorgen,Jorvin,Joseph,"
            "Josephine,Joshua,Josie,Jotha,Joy,Joyce,Joye,Juanita,Judd,Jude,Judith,"
            "Juditha,Julia,Julian,Juliana,Juliane,Julie,Julietta,Julinka,Julius,Juma,"
            "Jumoke,Jun,June,Jung,Justin,Justine,Kaatje,Kachine,Kaclyn,Kadin,Kaede,"
            "Kaethe,Kai,Kaia,Kaie,Kaikara,Kaili,Kaimi,Kairos,Kaiya,Kakra,Kala,Kaladin,"
            "Kalama,Kalanit,Kalare,Kalb,Kale,Kalea,Kali,Kalika,Kalil,Kalila,Kalinda,"
            "Kalkin,Kalle,Kalli,Kalman,Kalonice,Kalyca,Kama,Kamal,Kamala,Kamali,"
            "Kamaria,Kambo,Kameko,Kamilah,Kamilia,Kanda,Kane,Kanene,Kaniel,Kanika,"
            "Kantha,Kanya,Kapera,Kara,Karan,Karayan,Kardal,Karel,Karen,Karida,Karimah,"
            "Karisa,Karka,Karl,Karla,Karlenne,Karli,Karlyn,Karmina,Karol,Karsten,"
            "Karylin,Karyn,Kasa,Kasch,Kasen,Kasia,Kasinda,Kaspar,Kassia,Kate,Kateb,"
            "Katherine,Kathleen,Katja,Katoka,Katrien,Katrina,Kaula,Kaveri,Kavindra,Kay,"
            "Kaya,Kaye,Kayin,Kayla,Kaysa,Kazia,Keane,Keara,Kearney,Kedar,Keefe,Keelan,"
            "Keelin,Keely,Keenan,Kefira,Kegan,Kehinde,Kei,Keiko,Keir,Keisha,Keith,"
            "Kelby,Kelda,Keleman,Kelia,Kell,Kellen,Kelley,Kelli,Kellie,Kelly,Kelsey,"
            "Kelvin,Ken,Kenan,Kendall,Kendra,Kendrick,Kenelm,Kenley,Kennard,Kennedy,"
            "Kenneth,Kennis,Kent,Kenton,Kenyangi,Kenyon,Keona,Kepa,Ker,Kerani,Kerby,"
            "Kerensa,Kern,Kerry,Kers,Kersen,Kerstan,Kerwin,Kesare,Kesi,Kesia,Kessie,"
            "Kester,Keturah,Ketzia,Kevin,Khalida,Khalil,Khoury,Kichi,Kiefer,Kiele,"
            "Kieran,Kiernan,Killian,Kim,Kimberly,Kimmie,Kimmy,Kin,Kineta,Kinnel,Kinsey,"
            "Kintan,Kiona,Kip,Kira,Kiran,Kirby,Kirima,Kirk,Kirsten,Kirti,Kisa,Kiska,"
            "Kismet,Kissa,Kita,Kiyoshi,Kliftin,Klog,Kohana,Kolina,Komor,Kontar,Koren,"
            "Koressa,Krischan,Kristen,Krister,Kurt,Kyle,Kyler,Kyly,Kyna,Kynthia,Kyoko,"
            "Lacey,Lacie,Laethan,Laila,Lailie,Laird,Lakeisha,Lala,Lalasa,Lamar,Lamont,"
            "Lan,Lana,Lance,Lander,Landon,Landra,Lane,Lang,Lani,Lara,Laraine,Laralee,"
            "Lari,Larissa,Lark,Larry,Lars,Latika,Latonia,Laura,Laurana,Laurel,Laurie,"
            "Laurinda,Lauryn,Laveda,Lavern,Laverne,Lavinia,Lawler,Lawrence,Lazarus,Lea,"
            "Leah,Leala,Leandra,Lear,Leba,Ledah,Lee,Leif,Leigh,Leighton,Leiko,Leila,"
            "Leilana,Leland,Len,Lena,Lene,Lennon,Lennor,Lennox,Lenor,Lenora,Lenore,"
            "Lensar,Leo,Leon,Leona,Leonard,Leora,Leron,Leroy,Leslie,Lester,Letha,"
            "Letitia,Lev,Levana,Levi,Lewis,Lexine,Li,Lia,Liadan,Liam,Lian,Liana,Liane,"
            "Libby,Lien,Like,Lila,Lilith,Lillian,Lillie,Lily,Limber,Lina,Lincoln,Linda,"
            "Lindsay,Lindsey,Linette,Linnae,Linnea,Lionel,Lisa,Lisette,Litsa,Liv,Liza,"
            "Llewellyn,Lloyd,Logan,Lois,Lokelani,Lola,Loni,Lora,Lore,Lorelei,Lorelle,"
            "Loren,Lorenzo,Loretta,Lori,Lorne,Lorraine,Lotus,Louis,Louise,Lowell,Lucas,"
            "Lucian,Lucille,Lucine,Lucretia,Lucy,Ludia,Luela,Luis,Luisa,Luke,Lukene,"
            "Lukina,Lukyan,Lulu,Luna,Lunt,Luther,Lydia,Lyle,Lynda,Lyndon,Lynelle,Lynn,"
            "Lynnda,Lynnette,Lyris,Lysander,Lysel,Lysnadra,Mabel,Mac,Macaria,Macer,"
            "Machi,Mack,Mackenzie,Maddy,Madelaine,Madelina,Madeline,Madelon,Madelyn,"
            "Mady,Mae,Magan,Magara,Magdalen,Magdalena,Magdaline,Magena,Magenta,Maggie,"
            "Magnus,Mahala,Mahalia,Mai,Maia,Maida,Maisie,Maitane,Maizah,Maj,Malaya,"
            "Malcolm,Malik,Malila,Malina,Malinda,Malka,Mallory,Malu,Mamie,Manco,Manda,"
            "Mandara,Mandek,Mander,Mandisa,Mandy,Manfred,Mangena,Manning,Manon,Mansi,"
            "Mansur,Manuel,Manya,Mara,Marc,Marcella,Marcia,Marcos,Marcus,Marcy,Marden,"
            "Marek,Maren,Margaret,Margarita,Margo,Margot,Marguirte,Maria,Mariah,Mariam,"
            "Mariama,Marian,Mariana,Marianna,Marianne,Maribel,Marie,Mariel,Marietta,"
            "Marily,Marilyn,Marina,Mario,Maris,Marisa,Marisha,Marissa,Marjani,Marjeta,"
            "Marjorie,Mark,Markham,Markos,Marlene,Marlin,Marlo,Marlon,Marmara,Marnie,"
            "Marnina,Marsha,Marshal,Marshall,Marsten,Marta,Martha,Marti,Martin,Martina,"
            "Martingo,Marvin,Mary,Maryann,Marybeth,Marylou,Marzia,Mason,Matai,Matana,"
            "Mateo,Mathea,Mather,Matilda,Matrika,Matthew,Matthias,Maud,Maura,Maureen,"
            "Maurice,Maurita,Mavis,Max,Maxine,Maxwell,May,Maya,Maynard,Mayon,Mead,"
            "Meara,Meda,Medea,Meg,Megan,Megara,Meghan,Mei,Meira,Meka,Mela,Melanie,"
            "Melantha,Melba,Melia,Melian,Melina,Melinda,Melisenda,Melissa,Mellinio,"
            "Melodie,Melody,Melosa,Melva,Mercedes,Mercer,Meredith,Merele,Merill,Merle,"
            "Merrick,Merrik,Mesha,Meta,Meyer,Mia,Miakoda,Micael,Michael,Michaela,"
            "Michele,Michelle,Midori,Migina,Mignon,Migon,Miguel,Mika,Mike,Mikkel,Mikos,"
            "Miles,Millicent,Millie,Milo,Milton,Min,Mina,Minda,Mindel,Mindy,Miner,"
            "Minerva,Minka,Minna,Minnie,Mira,Miranda,Mirem,Miremba,Mireya,Miriam,"
            "Mirielle,Missy,Misty,Mitchell,Mitena,Mitexi,Mitzi,Moira,Mollie,Molly,Mona,"
            "Monique,Monroe,Monte,Moon,Morena,Morgan,Morgana,Morgance,Moria,Moriah,"
            "Morley,Morris,Mortimer,Morton,Morven,Morz,Motega,Mukasa,Murdoch,Murdock,"
            "Muriel,Murphy,Myles,Myra,Myron,Nada,Nadia,Nadine,Nadya,Naeem,Naia,Nailah,"
            "Naimah,Nalini,Nalren,Namazzi,Nami,Nan,Nana,Nancy,Nanette,Nantale,Nantan,"
            "Naomi,Napea,Nara,Narda,Narmada,Nasiche,Nastassia,Natalie,Natane,Natasha,"
            "Natesa,Nathan,Nathaniel,Naysa,Nazirqah,Neal,Neala,Neale,Neci,Nediva,Neely,"
            "Neil,Nekane,Nelek,Nell,Nelson,Neola,Neoma,Neona,Neria,Nerine,Nerissa,"
            "Neron,Nestor,Netti,Neva,Nevada,Nevan,Neville,Nevin,Neysa,Nicanor,Nicholas,"
            "Nicia,Nicola,Nicole,Nicolette,Nigel,Nika,Nikki,Nikolos,Nils,Nimah,Nina,"
            "Niobe,Niola,Nira,Nirvelli,Nissa,Nita,Nitara,Nixie,Noah,Nodin,Noe,Noel,"
            "Noelani,Noella,Nolan,Nolita,Nona,Nora,Norah,Norbert,Noreen,Nori,Noriko,"
            "Norma,Norman,Norris,Norton,Nuri,Nydia,Nyle,Nyrna,Nyssa,Oakes,Oakley,"
            "Obelia,Ochen,Octavia,Octavius,Odelia,Odell,Odera,Odessa,Odetta,Odette,"
            "Odile,Odin,Odion,Odon,Ogden,Ohanna,Okelani,Olaf,Olathe,Olayinka,Olesia,"
            "Olga,Oliana,Olin,Olinda,Oliver,Olivette,Olivia,Omar,Ona,Onida,Opal,"
            "Ophelia,Oralie,Orane,Ordano,Oren,Orenda,Oriana,Orianna,Oriel,Oriole,Orion,"
            "Orlantha,Orman,Ormand,Ornidaa,Orrin,Orson,Orville,Oscar,Osgood,Osmond,"
            "Otis,Otto,Owen,Paco,Paige,Pakuna,Palmer,Palmiera,Paloma,Pamela,Pandita,"
            "Pandora,Panthea,Pantzike,Panya,Panyin,Paolo,Paris,Parker,Parnell,Pascal,"
            "Pascale,Patamon,Patia,Patience,Patricia,Patrick,Patsy,Patterson,Patton,"
            "Paul,Paula,Paulette,Paulin,Pauline,Pavel,Pavla,Paxton,Payton,Pazia,Pearce,"
            "Pearl,Peder,Peg,Peggy,Pelagia,Pemba,Pembroke,Penda,Penelope,Peninna,Penn,"
            "Penny,Penthea,Peony,Percival,Perdita,Perouze,Perry,Persis,Peter,Petra,"
            "Peyton,Phaedra,Phearcy,Phedra,Philip,Phillip,Phillippe,Philomena,Phoebe,"
            "Phoenix,Phylis,Phyllis,Pia,Pier,Pierce,Pierre,Pierson,Pila,Pilan,Piper,"
            "Platon,Polly,Poloma,Porche,Porter,Portia,Prentice,Prescot,Prescott,"
            "Preston,Priscilla,Prudence,Prudy,Pyrena,Pythia,Qamra,Queena,Quella,Quenby,"
            "Quentin,Quenton,Quillan,Quincy,Quinlan,Quinn,Quintina,Quiterie,Rachel,Rad,"
            "Radcliffe,Radella,Radinka,Radman,Rae,Rafael,Rafferty,Ragnar,Rai,Raidon,"
            "Raizel,Raleigh,Ralph,Ramiro,Ramla,Ramon,Ramona,Ramsay,Ramsey,Ramya,Ranard,"
            "Rance,Randall,Randie,Randolph,Rane,Ranee,Ranen,Ranger,Rani,Rankin,Raoul,"
            "Raphael,Raquel,Rashida,Rasine,Ratri,Raul,Raven,Ravi,Ravid,Rawnie,Ray,"
            "Raymond,Rayna,Raynell,Raynor,Raziya,Reade,Reba,Rebecca,Redford,Redmond,"
            "Reed,Reese,Reeve,Regan,Regina,Reginald,Regis,Reidun,Remington,Remy,Rena,"
            "Renaldo,Renata,Rendor,Rene,Renee,Renfry,Renny,Reuben,Rex,Reyhan,Rhea,"
            "Rhett,Rhiamon,Rhianne,Rhiannon,Rhoda,Rhodanthe,Rhonda,Rhonna,Rhys,Rhyssa,"
            "Ria,Riane,Rica,Ricardo,Richard,Richter,Rico,Rider,Ridgley,Rigby,Rihana,"
            "Rikki,Riley,Rimon,Ringo,Rio,Riodan,Riordan,Risa,Rita,Riva,Roanna,Roarke,"
            "Robert,Roberta,Roberto,Robi,Robin,Robyn,Rochelle,Rockwell,Rod,Roderick,"
            "Rodman,Rodney,Rodrigo,Roger,Rohanna,Roi,Roland,Roldan,Rolf,Rona,Ronald,"
            "Ronan,Rooney,Rorie,Rory,Rosa,Rosalind,Rosalinda,Rosalinde,Rosaline,"
            "Rosanne,Roscoe,Rose,Roseanne,Rosemarie,Rosemary,Ross,Roth,Rowan,Rowena,"
            "Rowland,Roxana,Roxanne,Roy,Royce,Ruben,Ruby,Rudd,Rudi,Rudyard,Rufus,Rumer,"
            "Runako,Ruskin,Russ,Russell,Rusty,Ruth,Ruthann,Rutherford,Rutledge,Ryan,"
            "Ryann,Ryanne,Ryba,Ryder,Rylan,Ryssa,Saba,Sabina,Sabiny,Sabirah,Sabra,"
            "Sabrina,Sacha,Sachi,Sade,Sadira,Saffi,Safiya,Sagara,Sahale,Sahen,Saidah,"
            "Sakari,Sakinah,Sakti,Sakura,Salihah,Salim,Salimah,Salina,Sally,Saloman,"
            "Salome,Sam,Samantha,Samara,Samien,Samirah,Sammon,Samson,Samuel,Sancia,"
            "Sanders,Sandia,Sandon,Sandor,Sandra,Sandrine,Sandya,Sanford,Sara,Sarah,"
            "Sarai,Saraid,Saree,Sarena,Sargent,Sari,Sarisha,Sarngin,Sarojin,Sasha,"
            "Sashenka,Satinka,Saul,Saunders,Savanna,Sawyer,Saxon,Schuyler,Scotia,Scott,"
            "Sean,Searlait,Season,Sebasten,Sebastian,Sebastien,Seema,Seif,Sela,Selby,"
            "Selena,Selina,Selma,Semele,Senon,Senta,Serafina,Sergio,Serilda,Sesha,Seth,"
            "Seung,Severin,Sevilin,Seward,Seymour,Shaine,Shakira,Shako,Shammara,Shana,"
            "Shanata,Shandra,Shandy,Shane,Shani,Shanley,Shanna,Shannon,Shantay,Shantha,"
            "Sharman,Sharon,Sharri,Shashi,Shawn,Shayndel,Shea,Sheba,Sheena,Sheffield,"
            "Sheila,Shela,Shelby,Sheldon,Shelley,Shelly,Shen,Sheridan,Sherman,Sherri,"
            "Sherwin,Sherwood,Shika,Shin,Shina,Shing,Shira,Shirley,Shobi,Shoshana,"
            "Shunnar,Sibley,Sibongile,Sibyl,Sidney,Sidonia,Sidra,Siegfried,Sierra,"
            "Sigourney,Siham,Silas,Sileas,Silva,Silvia,Simba,Simon,Simone,Sine,Sinead,"
            "Siobhan,Siran,Sirena,Siroun,Sitara,Sitembile,Siv,Sivan,Sive,Skip,Skyler,"
            "Slade,Slevin,Smith,Sofi,Solana,Solange,Soledad,Solita,Solomon,Sondra,"
            "Sonia,Sonja,Sonya,Sophia,Sophie,Sophronia,Sorgan,Soterios,Spalding,"
            "Spencer,Spenser,Spica,Stacey,Stacia,Stacy,Standford,Stanley,Stanton,"
            "Stasio,Stefan,Stefania,Stella,Stephan,Stephani,Stephanie,Stephen,Ster,"
            "Sterling,Stesha,Stevan,Steve,Steven,Stewart,Stockard,Stoke,Storm,Stoyan,"
            "Strom,Stuart,Subrey,Sukatai,Suki,Sulaiman,Sullican,Sumi,Summer,Sumner,Sun,"
            "Susan,Susanna,Sutherland,Sutton,Suzanne,Sven,Svetlana,Sybil,Sydelle,"
            "Sydney,Syeira,Sylvester,Sylvia,Syna,Synia,Tab,Tabari,Tabitha,Taci,Tacita,"
            "Tad,Tadi,Taffy,Tahirah,Tai,Taima,Tainn,Taipa,Taite,Tajo,Taka,Takara,"
            "Takiyah,Takoda,Talasi,Talbart,Talbot,Tale,Talia,Talitha,Tallulah,Talman,"
            "Talos,Tam,Tama,Tamara,Tamary,Tamma,Tammy,Tanaka,Tanek,Tani,Tanner,Tano,"
            "Tansy,Tanya,Tao,Tara,Taro,Tate,Tatyana,Taurin,Tawnie,Tawny,Tayce,Taylor,"
            "Teague,Tehya,Tekla,Tem,Temina,Terence,Terentia,Terese,Terrence,Terrill,"
            "Terrilyn,Terry,Tertia,Teryn,Tesia,Tess,Tessa,Thaddeus,Thadea,Thai,Thais,"
            "Thalassa,Thalia,Thaman,Than,Thana,Thane,Thanos,Thara,Thea,Thekla,Thelma,"
            "Theobald,Theodore,Theodosia,Theone,Thera,Theron,Thierry,Thirza,Thomas,"
            "Thora,Thorpe,Thurston,Thyra,Tia,Tiara,Tibalt,Tienette,Tiernan,Tierney,"
            "Tierra,Tiffany,Tilda,Timandra,Timothy,Tina,Tiponya,Tirza,Titus,Tivona,"
            "Tobey,Tobias,Toby,Tod,Todd,Tola,Tomas,Tong,Tor,Tora,Tori,Torin,Torrance,"
            "Tory,Tosia,Tove,Townsend,Tracey,Tracy,Travers,Travis,Treasa,Tremain,"
            "Tremaine,Trent,Tresa,Treva,Trevor,Trey,Trianon,Tricia,Trilby,Trina,Trind,"
            "Trish,Trisha,Tristan,Troy,Trudy,Tryne,Tryon,Tryphena,Tucker,Tully,Tyee,"
            "Tyler,Tymon,Tyne,Tyrone,Ula,Ulani,Ultima,Uma,Una,Undine,Upton,Urania,"
            "Uriah,Urian,Uriana,Ursula,Uta,Vala,Valentina,Valeria,Valerie,Valeska,"
            "Valonia,Valora,Van,Vance,Vanda,Vanessa,Vanora,Vanya,Vashti,Vaughn,Veda,"
            "Velika,Velma,Venesssa,Vera,Verena,Verity,Vern,Vernon,Veronica,Vesta,"
            "Vevila,Victor,Victoria,Vidonia,Vincent,Vinson,Violet,Violetta,Virgil,"
            "Virginia,Viridis,Vito,Viveka,Vivian,Vlad,Vladimir,Vokes,Voleta,Volf,"
            "Vrinda,Wade,Wagner,Wakanda,Walden,Waldo,Walker,Wallace,Wally,Walter,Wanda,"
            "Waneta,Ward,Warner,Warren,Watson,Waylan,Wayland,Waylon,Wayne,Webb,Webster,"
            "Wendell,Wendy,Wesley,Weston,Weylin,Whilhelmina,Whitaker,Whitney,Wijdan,"
            "Wilfen,Will,Willard,Willem,William,Willow,Wilma,Wilona,Wilson,Winda,"
            "Winema,Winifred,Winna,Winona,Winston,Winthrop,Wlby,Woody,Wyatt,Wynee,Wynn,"
            "Wynona,Xanthe,Xaveria,Xavier,Xaviera,Xena,Xenia,Xenos,Xerxes,Ximen,Ximena,"
            "Xylia,Xylona,Yachne,Yakecan,Yale,Yancey,Yanice,Yardley,Yarin,Yarmilla,"
            "Yasmeen,Yasmin,Yelinda,Yenene,Yerik,Yero,Yervant,Yesmina,Yetta,Yeva,"
            "Yokiko,Yolanda,Yolie,Yonina,York,Yovela,Yusuf,Yvella,Yves,Yvette,Yvonne,"
            "Zachariah,Zachary,Zackery,Zada,Zahara,Zahirah,Zahra,Zaid,Zaide,Zakia,"
            "Zalea,Zalika,Zaltana,Zandra,Zane,Zaniel,Zann,Zara,Zarah,Zared,Zarek,Zaza,"
            "Zehava,Zeke,Zelda,Zelenka,Zelia,Zella,Zena,Zenaide,Zenia,Zenon,Zerlinda,"
            "Zeva,Zevida,Zia,Ziazan,Zigana,Zila,Zina,Zinnia,Zion,Zita,Ziven,Zoe,Zola,"
            "Zona,Zora,Zorah,Zorda,Zorn,Zosia,Zuleika,Zulema,Zuza,Zuzanny,"
        )
        NPC_NAMES = [None]   # (2.6.82) the set of NPC_NAMES_DATA, made at its first use (is_npc)


        def npc_names():
            names = NPC_NAMES[0]
            if names is None:
                names = NPC_NAMES[0] = set(n.lower() for n in NPC_NAMES_DATA.split(",") if n)
            return names


        # --------------------------------- MAIN --------------------------------------
        def layout_signature():
            return tuple(tuple(v) for _, v in sorted(LAYOUT.items()))


        # ------------------------------- MODULE --------------------------------------
        M = {"windows": None, "combat": None, "panel": None, "last_layout": None,
             "tick": 0, "poll": 0, "errors": set(), "readers": False,
             "next_scan": 0.0, "next_combat": 0.0, "next_glow": 0.0,
             "sight_req": False}     # the Settings page asked for the Sightings window


        def due(key, step, now):
            """True once every `step` seconds (kept on that rate on average, however
            the passes fall); M[key] is when it is next due."""
            t = M[key]
            if now < t:
                return False
            M[key] = t + step if now - t < step else now + step
            return True


        def open_windows():
            windows, combat, panel = M["windows"], M["combat"], M["panel"]
            wins = {c: (windows[c].gump, windows[c].size) for c in CATS}
            if combat.is_open():
                wins["combat"] = (combat.gump, (LAYOUT["combat"][2], 0))
            if panel.gump is not None:                 # the shared Ultima Tracker window
                wins["panel"] = (panel.gump, panel.size)
            for s, pb in POPS.items():
                wins["pop:%d" % s] = (pb.gump, pb.size)
            return wins


        def snapshot_all():
            for w in (M["windows"] or {}).values():
                safe(w.snapshot)
            if M["combat"] is not None:
                safe(M["combat"].snapshot)       # (the hub saves the panel's position)


        def dock_hooks(win, title, cat=None):
            """Dock-registry hooks for one tracker window (fold into the Action Bar);
            a group window (cat) fits its zone by the shared scale (fit_hook)."""
            def state():
                if win.gump is None or STATE.get("shutting"):
                    return None
                return "docked" if win.docked else ("minimized" if win.minimized else "open")

            def visible(on):
                safe(lambda: setattr(win.gump, "IsVisible", bool(on)))

            def dock():
                if not win.minimized:
                    win.toggle_minimize()
                win.docked = True
                visible(False)

            def show():
                win.docked = False
                if win.minimized:
                    win.toggle_minimize()
                visible(True)

            def undock():
                win.docked = False
                visible(True)

            def minimize():
                win.docked = False
                if not win.minimized:
                    win.toggle_minimize()
                visible(True)
            hooks = {"title": title, "icon": 0, "state": state, "show": show, "dock": dock,
                     "undock": undock, "minimize": minimize, "gump": lambda: win.gump}
            if cat is not None:
                hooks["fit"] = fit_hook(cat)
                hooks["exact"] = True             # (2.6.56) it is made exactly its slot's size
                hooks["verify"] = True            # (2.6.69) measured by the layout every pass
            return hooks


        def register_docks(windows, combat):
            for c in CATS:
                HOST.dock_add("ultima." + c, dock_hooks(windows[c], TITLES[c], c))
            hooks = dock_hooks(combat, "Combat")
            hooks["fit"] = combat.layout_fit      # (2.6.56) made exactly its slot's size
            hooks["exact"] = True
            hooks["verify"] = True                # (2.6.69) measured by the layout every pass
            HOST.dock_add("ultima.combat", hooks)


        def unregister_docks():
            for c in CATS:
                HOST.dock_remove("ultima." + c)
            HOST.dock_remove("ultima.combat")


        def reset_globals():
            FOES.clear()
            IGNORE.clear()
            PLAYER_NAMES.clear()
            PLAYER_VER[0] += 1
            reset_layout()
            UI.update(UI_DEFAULTS)
            FIT.update(own=None, want={}, req=False, size={}, own_size={},   # told again when slotted
                       force=set(), made={})      # (2.6.71) no spent rebuilds from the last run
            STATE.update(STATE_DEFAULTS, party=set())
            POPS.clear()
            LAST_CLICK.clear()
            del DOCK_REQ[:]
            # (Follow.serial is shared with every module and is left alone here: this also
            #  runs when the Settings page opens with the module off; _stop ends the follow)
            BANDAGE.update(serial=None, follow=None)
            ANCHORS.__init__()
            cb_engaged.clear()
            del cb_pending_click[:]
            del cb_pending_spell[:]
            cb_casting.update(serial=None, stale=False)
            del CHROMES[:]
            del CLICK_Q[:]
            CLICK_MODS.clear()
            del THREAD_JOBS[:]
            del TICK_JOBS[:]
            SAVE_REQ[0] = False
            DATA_READY[0] = False
            page.update({"loaded": False, "lines": None, "save_at": 0.0})
            JREAD["learn"] = JREAD["attack"] = JREAD["killer"] = None
            FRIEND_Q.clear()
            LT_SKIP.update(serial=None, until=0.0)    # (2.6.83) the 2.6.82 caches too
            FOE_WHERE[0] = -10.0
            NOTE_CACHE.clear()
            for what in list(CURSOR_OWN):
                release_cursor(what)
            # (2.6.05) what the save file holds is read again; the session's lists of
            # who is around (PRESENT, ALERTED) stay, so a restart doesn't alert or log
            # again the players still there
            del SIGHTS[:]
            LAST_SEEN.clear()
            ALT_OF.clear()
            SIGHT.update(dirty=False, save_at=0.0)
            SIGHT["ver"] += 1
            SIGHT["seen_ver"] += 1
            LINK_PICK[0] = None
            ALERT_PREV.clear()
            ATTACKERS.clear()
            WATCH["dead"] = WATCH["me"] = None


        def _start():
            """On the client thread (Kit.on_client): no file here. The save file is
            read by load_job on the script's thread (the first thread_tick), and
            the windows are built by the first tick after it landed."""
            pending = None
            if page["save_at"]:                  # a Settings-page change not written yet
                page["save_at"] = 0.0
                pending = save_text()            # (its text, before the lists are reset)
            reset_globals()
            STATE["started"] = True
            # our readers of the shared Journal start now: older lines aren't reacted to
            JREAD["learn"] = safe(Journal.reader)
            JREAD["attack"] = safe(Journal.reader)
            JREAD["killer"] = safe(Journal.reader)
            safe(init_native_art)                # which of the client's gump art loads
            M.update({"last_layout": None, "tick": 0, "poll": 0, "errors": set(),
                      "next_scan": 0.0, "next_combat": 0.0, "next_glow": 0.0})
            # (2.6.05) the foe alert's kind on Settings > Alerts, and "is this player
            # on my Foe list?" for other modules
            fn = getattr(HOST, "alert_kind", None)
            if fn is not None:
                safe(lambda: fn(ALERT_KEY, "Foe in range", ALERT_SOUND))
            HOST.services["ultima.is_foe"] = is_foe
            HOST.services["ultima.classify"] = classify_service     # (2.6.06) e.g. Lookout
            THREAD_JOBS.append(lambda: load_job(pending))


        def load_job(pending_text=None):
            """Script thread (thread_tick): read the save file; the next tick builds
            the windows from it. A Settings-page change still unwritten goes to the
            file first, so the read sees it."""
            if STATE["shutting"]:
                return
            if pending_text is not None:
                SAVE_SEQ[0] += 1                 # (newer than any page write still on its thread)
                write_text(pending_text, SAVE_SEQ[0])
                report_save_error()
            load_data()
            ANCHORS.saved = ANCHORS.saved_groups()
            load_old_combat_settings()           # persistent vars: no client call
            STATE["loaded"] = True


        def build_windows():
            """Client thread (the first tick after the save file was read)."""
            windows = {c: CategoryGump(c) for c in CATS}
            combat = CombatWindow()
            M.update({"windows": windows, "combat": combat})
            if UI["combat_shown"]:
                combat.show()
            M["panel"] = ControlPanel(windows, combat)
            register_docks(windows, combat)
            STATE["foe_ver"] += 1

            n = len(FOES)
            API.SysMsg(TITLE + (": on, %d saved foe%s." % (n, "" if n == 1 else "s")), Kit.HUE_GOOD)
            if not M["readers"]:
                M["readers"] = True
                if not find_mod_readers():
                    API.SysMsg(TITLE + ": couldn't read the client's Alt and Shift keys directly; "
                               "Alt+click and Shift+click may be less reliable.", Kit.HUE_INFO)
            M.update({"last_layout": layout_signature(), "tick": 0, "poll": 0,
                      "next_scan": 0.0, "next_combat": 0.0, "next_glow": 0.0})
            if Kit.get_var(SIGHT_OPEN_KEY) == "1":   # (2.6.05) open when the module stopped
                SIGHT_WIN.show()


        def _tick():
            """On the client thread (client_tick): nothing here waits, and every
            call runs in place. Saves and Frames' start go to _thread_tick."""
            if M["windows"] is None:
                if STATE["loaded"] and not STATE["shutting"]:
                    build_windows()              # the save file has landed (load_job)
                return
            report_save_error()                    # (a failed background write, if any)
            run_clicks()                           # clicks since the last tick
            run_tick_jobs()                        # work handed back by thread jobs
            while DOCK_REQ:                        # gold arrows clicked since the last tick
                HOST.dock_to_bar(DOCK_REQ.pop(0))  # folds in now, or once the bar is up
            if SETTINGS_REQ:                       # (2.6.72) a window's Settings button
                del SETTINGS_REQ[:]
                HOST.show_settings(KEY)
            windows, combat, panel = M["windows"], M["combat"], M["panel"]
            if windows is None:
                return
            fit_tick(windows)                      # (2.6.55) a zone asked for another scale
            now = time.time()
            try:
                try:                               # (2.6.05; on their own: a failure there
                    if M["sight_req"]:             # never stops the trackers)
                        M["sight_req"] = False     # the Settings page's "Open Sightings"
                        SIGHT_WIN.bring()
                    SIGHT_WIN.tick(now)            # its close / redraws / list
                    KILLER_WIN.tick(now)
                except Exception as ex:
                    if stopping() or HOST.stopping():
                        return
                    report_error(ex)
                handle_spells()
                handle_bandage()
                ANCHORS.tick(open_windows)
                if ANCHORS.groups_changed():
                    STATE["dirty_save"] = True
                if due("next_glow", GLOW_EVERY, now):   # (2.6.82) the low-HP glow: 10 a second
                    a = glow_alpha()
                    windows["friend"].pulse(a)    # low-HP glow on Friends
                    for pb in list(POPS.values()):
                        pb.pulse(a)
                if due("next_scan", TICK_SECONDS, now):
                    buckets = scan()
                    try:
                        watch_tick(now)            # (2.6.05) attackers, death, resurrection
                    except Exception as ex:
                        report_error(ex)
                    # (2.6.82) StopRequested read once here (was once per window)
                    if stopping():
                        return
                    for c in CATS:
                        windows[c].update(buckets[c])
                    for pb in list(POPS.values()):
                        try:
                            pb.update()
                        except Exception as ex:
                            if stopping():
                                return
                            POPS.pop(pb.serial, None)
                            API.SysMsg(TITLE + (": closed a broken health bar (%s)." % ex),
                                       Kit.HUE_BAD)
                    if stopping():
                        return
                    process_size_sync(windows)
                    panel.update()
                    check_follow()

                    M["tick"] += 1
                    if M["tick"] % SAVE_EVERY == 0:
                        snapshot_all()
                        sig = layout_signature()
                        if sig != M["last_layout"] or STATE["dirty_save"] or \
                                (SIGHT["dirty"] and now >= SIGHT["save_at"]):
                            M["last_layout"] = sig
                            request_save()

                # (2.6.82) folded into the Action Bar (nothing drawn): at the scan's pace
                if due("next_combat", TICK_SECONDS if combat.docked else COMBAT_TICK_SECONDS,
                       now) and not stopping():
                    combat.tick()
            except Exception as ex:
                # While the module is being stopped TazUO refuses to create new gump
                # controls (they come back as None). That is expected, so just leave
                # quietly instead of showing an error.
                if stopping() or HOST.stopping():
                    return
                # A real problem: report each distinct error once and keep running.
                report_error(ex)


        def _thread_tick():
            """On the script's own thread, right after each tick: the work that
            mustn't run on the client thread. Returns at once when there is none."""
            while THREAD_JOBS:
                job = THREAD_JOBS.pop(0)
                try:
                    job()
                except Exception as ex:
                    if stopping() or HOST.stopping():
                        return
                    report_error(ex)
            if SAVE_REQ[0]:
                SAVE_REQ[0] = False
                # the text is made here; the write (the sightings make the file bigger)
                # goes to a short thread of its own, so this thread doesn't wait on it
                save_data(background=True)


        def _stop():
            STATE["shutting"] = True
            STATE["started"] = False
            unregister_docks()
            for what in list(CURSOR_OWN):
                release_cursor(what)
            if HOST.services.get("ultima.is_foe") is is_foe:
                HOST.services.pop("ultima.is_foe", None)
            if HOST.services.get("ultima.classify") is classify_service:
                HOST.services.pop("ultima.classify", None)
            if M["windows"] is None:
                return                               # (never built: nothing changed, nothing to save)
            safe(lambda: Kit.on_client(snapshot_all))   # one hop for every window's position
            SAVE_REQ[0] = False
            # The one synchronous file write: no thread_tick of ours runs after stop, and a
            # background thread could be cut off by the script ending, so the layout and the
            # lists are written here, on whichever thread stop runs on (a one-off hitch when
            # that is the client thread: the Modules tab).
            save_data()
            gumps = []
            for w in M["windows"].values():
                gumps.append(w.gump)
                w.gump = None
            if M["combat"] is not None:
                gumps.append(M["combat"].gump)
                M["combat"].gump = None
            hub = getattr(HOST, "hub", None)
            if hub is not None:
                hub.remove("ultima")               # our section of the shared window
            for pb in list(POPS.values()):
                gumps.append(pb.gump)
                pb.gump = None
            POPS.clear()
            for g in gumps:
                Kit.dispose(g)
            SIGHT_WIN.close(stopping=True)           # (it opens again with the module)
            KILLER_WIN.close()
            if Follow.serial is not None:
                safe(lambda: API.CancelAutoFollow())
                Follow.serial = None
            M.update({"windows": None, "combat": None, "panel": None})


        # =============================================================================
        #  Ultima Tracker's page of the Virtue Assistant Settings tab
        # =============================================================================
        page = {"c": None, "seen": None, "stable": 0, "loaded": False, "store": ({}, {}),
                "lines": None,       # (path, lines) read in the background, for poll_config to apply
                "save_at": 0.0}      # when a change made with the module off is written (0: none)


        def page_ensure_loaded():
            """With the module off, read the save file so the page shows (and keeps)
            what's saved. The read runs on a thread of its own (the page is built
            on the client thread); poll_config applies it and redraws the page."""
            if STATE["started"] or page["loaded"]:
                return
            reset_globals()
            page["loaded"] = True

            def read():
                try:
                    page["lines"] = read_save_lines()
                except Exception as ex:
                    SAVE_ERR[0] = "could not read the save file: " + str(ex)
                    page["lines"] = ()           # failed: nothing to apply, and (DATA_READY stays
                    #                              off) nothing may be written over the file
            in_background(read)


        def page_apply_loaded():
            """poll_config: the save file read for the page has landed."""
            got = page["lines"]
            if got is None:
                return False
            page["lines"] = None
            if STATE["started"] or not got:
                return False                         # the module's own load owns the data now,
                #                                      or the read failed (reported; no save)
            parse_save_lines(got[0], got[1])
            return True


        def page_save():
            """A change made on the Settings page: written by thread_tick while the
            module runs, else PAGE_SAVE_DELAY after the last change (one write per
            burst, off the client thread)."""
            if STATE["started"]:
                STATE["dirty_save"] = True
            else:
                page["save_at"] = time.time() + PAGE_SAVE_DELAY


        def page_flush_save(background):
            """Write a pending Settings-page change now (the page closed, or the
            module is starting and about to read the file)."""
            if page["save_at"]:
                page["save_at"] = 0.0
                save_data(background=background)


        # the page's sections, top to bottom: WINDOWS, OPTIONS, SIGHTINGS AND DEATHS,
        # FOE ALERT, DEBUG (their heights; config_height is their sum)
        CFG_H = (142, 92, 92, 92, 64)      # (2.6.72) WINDOWS: one row more (the lock)


        def all_locked():
            """(2.6.72) Every tracker window (groups and Combat) is locked."""
            return all(bool(LAYOUT[k][4]) for k in list(CATS) + ["combat"] if k in LAYOUT)


        def config_height(w):
            return sum(CFG_H) + Kit.GAP * (len(CFG_H) - 1)


        def build_config(g, x, y, w):
            page_ensure_loaded()
            store = ({}, {})
            c = {}
            Kit.add_section(g, x, y, w, CFG_H[0], "WINDOWS")

            def slider_row(text, sx, sy, lo, hi, val, unit, tip):
                Kit.add_label(g, text, sx, sy)
                s = Kit.add_slider(g, sx + 120, sy + 4, 140, lo, hi, val)
                safe(lambda: s.SetTooltip(tip))
                Kit.add_label(g, unit, sx + 266, sy, Kit.HUE_INFO)   # (ends before x + 320)
                return s

            c["scale"] = slider_row("Scale:", x + 12, y + 32, SCALE_MIN, SCALE_MAX, own_scale(), "%",
                                    "Size of the trackers and the pop-out bars (%d-%d)"
                                    % (SCALE_MIN, SCALE_MAX))
            c["opacity"] = slider_row("Opacity:", x + 12, y + 58, 0, 100, UI["opacity"], "%",
                                      "Background opacity of every window at once (0-100)")
            c["range"] = slider_row("Range:", x + 12, y + 84, RANGE_MIN, RANGE_MAX, UI["range"],
                                    "tiles", "Tiles round you the trackers list players in (%d-%d)"
                                    % (RANGE_MIN, RANGE_MAX))
            c["sync"] = Kit.add_check(g, "Sync tracker sizes", x + 320, y + 32, UI["sync"],
                                      "Resizing one tracker resizes the other two to match")
            Kit.art_button(g, store, "unanchor", Kit.ART_CLOSE, x + 320, y + 58, "Unanchor all",
                           "Undo every anchor between windows (they move on their own again)")
            Kit.art_button(g, store, "reset", Kit.ART_CLOSE, x + 320, y + 84, "Reset to defaults",
                           "Reset scale, opacity, range, the options and every window's place")
            # (2.6.72) the lock left the windows' title rows: one box for them all (a window
            # in a zone is held by the layout whatever it says)
            c["lock"] = Kit.add_check(g, "Lock the windows in place", x + 12, y + 110, all_locked(),
                                      "Free windows can't be moved or resized while ticked "
                                      "(windows in zones stay in their zones either way)")

            yo = y + CFG_H[0] + Kit.GAP
            Kit.add_section(g, x, yo, w, CFG_H[1], "OPTIONS")
            c["combat_only"] = Kit.add_check(
                g, "Combat bars: only once fighting", x + 12, yo + 32, UI["combat_only"],
                "Only add a mobile once it attacks you, you attack it in war mode, "
                "or it fights you up close")
            c["borders"] = Kit.add_check(g, "Show a border on the pop-out bars", x + 320, yo + 32,
                                         UI["borders"],
                                         "A stone border round the pop-out bars (the trackers and "
                                         "the Combat window always have the standard frame)")
            c["magery"] = Kit.add_check(
                g, "Magery buttons", x + 12, yo + 60, UI["magery"],
                "P (Poison) and Z (Paralyze) on the combat bars; H (Heal) and C (Cure) on "
                "friends, Shift+click for the greater spell")
            c["healing"] = Kit.add_check(g, "Bandage button", x + 320, yo + 60, UI["healing"],
                                         "B on friends' bars: bandage them when next to them; "
                                         "farther away it follows them")

            # (2.6.05) the sightings log and the death window
            ys = yo + CFG_H[1] + Kit.GAP
            Kit.add_section(g, x, ys, w, CFG_H[2], "SIGHTINGS AND DEATHS")
            c["sightings"] = Kit.add_check(
                g, "Log players who come into range", x + 12, ys + 32, UI["sightings"],
                "Every player who isn't a friend goes in the Sightings log once each time "
                "they turn up (the last %d are kept)" % SIGHT_CAP)
            Kit.art_button(g, store, "sightings", Kit.ART_PAGE, x + 320, ys + 30,
                           "Open Sightings", "Open the Sightings window")
            c["killer"] = Kit.add_check(
                g, "On death: list your attackers", x + 12, ys + 60, UI["killer"],
                "A small window lists the players who attacked you in the last %d seconds, "
                "each with Add to foes" % int(KILLER_BACK))

            # (2.6.05) the foe alert: who counts, and how often the same player
            ya = ys + CFG_H[2] + Kit.GAP
            Kit.add_section(g, x, ya, w, CFG_H[3], "FOE ALERT  (sound: Settings > Alerts)")
            for key, text, cx, tip in (
                    ("alert_red", "Red", 12, "Alert when a red (murderer) player comes into range"),
                    ("alert_foes", "Foe list", 110,
                     "Alert when a player on your Foe list comes into range (linked alts too)"),
                    ("alert_orange", "Orange", 230, "Alert when an orange (enemy) player comes "
                                                    "into range"),
                    ("alert_gray", "Grey", 340, "Alert when a grey (criminal) player comes "
                                                "into range")):
                c[key] = Kit.add_check(g, text, x + cx, ya + 32, UI[key], tip)
            Kit.add_label(g, "Same player again after:", x + 12, ya + 60)
            c["alert_minutes"] = Kit.add_slider(g, x + 200, ya + 64, 150, ALERT_MIN, ALERT_MAX,
                                                UI["alert_minutes"])
            safe(lambda: c["alert_minutes"].SetTooltip(
                "Minutes before the same player raises the alert again (%d-%d)"
                % (ALERT_MIN, ALERT_MAX)))
            c["alert_minutes_lbl"] = Kit.add_label(g, "%d min" % UI["alert_minutes"], x + 362,
                                                   ya + 60, Kit.HUE_INFO)

            yd = ya + CFG_H[3] + Kit.GAP
            Kit.add_section(g, x, yd, w, CFG_H[4], "DEBUG  (for checking the shard's texts)")
            c["say_attackers"] = Kit.add_check(
                g, "Print the attack lines seen in the journal", x + 12, yd + 32,
                UI["say_attackers"],
                "Repeats every line taken as \"<name> is attacking you\" (and lines about "
                "attacks that weren't), to check the shard's texts")
            page.update({"c": c, "store": store, "stable": 0,
                         "seen": {"scale": own_scale(), "opacity": UI["opacity"],
                                  "range": UI["range"], "alert_minutes": UI["alert_minutes"]}})


        def ctl_int(c, key, dflt):
            """(2.6.82) A page slider's value (no lambda per read), dflt when unreadable."""
            try:
                return int(c[key].Value)
            except Exception:
                return dflt


        def ctl_checked(c, key, dflt):
            """(2.6.82) A page checkbox's state, dflt when unreadable."""
            try:
                return c[key].IsChecked
            except Exception:
                return dflt


        def poll_config():
            c = page["c"]
            if c is None:
                return
            if page_apply_loaded():                # the save file read for the page landed:
                # (2.6.05) the controls still show what was there before the file came:
                # forget them, or the last look the page gets before it is drawn again
                # (Virtue Assistant polls a page as it leaves it) would put those back
                # over what was just read, and save them
                page["c"] = None
                HOST.refresh_settings("ultima")    # draw the page again with what it says
                return
            report_save_error()
            now = time.time()
            if page["save_at"] and now >= page["save_at"]:
                page_flush_save(True)              # a change made with the module off
            store, seen = page["store"], page["seen"]
            windows = M["windows"]
            if Kit.was_clicked(store, "unanchor"):
                ANCHORS.clear()
                page_save()
                API.SysMsg(TITLE + ": every window unanchored.", Kit.HUE_GOOD)
            if Kit.was_clicked(store, "reset"):
                if M["panel"] is not None:
                    M["panel"].reset_defaults()
                else:
                    reset_settings()
                    page_save()
                    API.SysMsg(TITLE + ": settings and windows reset to the defaults.",
                               Kit.HUE_GOOD)
                HOST.refresh_settings("ultima")
                return

            # Scale: wait until the slider has stopped moving before rebuilding
            sv = clamp(ctl_int(c, "scale", seen["scale"]), SCALE_MIN, SCALE_MAX)
            if sv != seen["scale"]:
                seen["scale"] = sv
                page["stable"] = 0
            elif sv != own_scale():
                page["stable"] += 1
                if page["stable"] >= 2:
                    if FIT["own"] is not None:     # fitted to a zone: the own scale is kept
                        FIT["own"] = sv            # for when the windows are freed
                        FIT["req"] = True          # (a shrink-only zone follows it)
                        STATE["dirty_save"] = True
                    elif windows is not None:
                        apply_scale(sv, windows)
                    else:
                        UI["scale"] = sv
                        page_save()

            # Opacity (all): cheap, apply immediately
            ov = clamp(ctl_int(c, "opacity", seen["opacity"]), 0, 100)
            if ov != seen["opacity"]:
                seen["opacity"] = ov
                if M["panel"] is not None:
                    M["panel"].set_all_opacity(ov)
                else:
                    UI["opacity"] = ov
                    page_save()

            # Range: used by the next scan
            rv = clamp(ctl_int(c, "range", seen["range"]), RANGE_MIN, RANGE_MAX)
            if rv != seen["range"]:
                seen["range"] = rv
                UI["range"] = rv
                page_save()

            # (2.6.05) foe alert: minutes before the same player alerts again
            av = clamp(ctl_int(c, "alert_minutes", seen["alert_minutes"]),
                       ALERT_MIN, ALERT_MAX)
            if av != seen["alert_minutes"]:
                seen["alert_minutes"] = av
                UI["alert_minutes"] = av
                Kit.set_text(c["alert_minutes_lbl"], "%d min" % av)
                page_save()
            if Kit.was_clicked(store, "sightings"):
                if M["windows"] is not None:
                    M["sight_req"] = True              # opened by the module's next tick
                else:                                  # (the save file is still being read)
                    API.SysMsg(TITLE + ": the Sightings window opens once the trackers are up; "
                               "try again in a moment.", Kit.HUE_INFO)

            lv = bool(ctl_checked(c, "lock", page["seen"].get("lock")))
            if page["seen"].get("lock") is None:
                page["seen"]["lock"] = lv
            elif lv != page["seen"]["lock"]:             # (2.6.72) lock every window at once
                page["seen"]["lock"] = lv
                if windows is not None:
                    for k in CATS:
                        safe(lambda: windows[k].set_locked(lv))
                if M["panel"] is not None:
                    safe(lambda: M["panel"].combat.set_locked(lv))
                else:
                    for k in list(CATS) + ["combat"]:
                        if k in LAYOUT:
                            LAYOUT[k][4] = lv
                request_save()
            for key in ("borders", "healing", "magery", "combat_only", "sync", "alert_red",
                        "alert_foes", "alert_orange", "alert_gray", "sightings", "killer",
                        "say_attackers"):
                v = bool(ctl_checked(c, key, UI[key]))
                if v == UI[key]:
                    continue
                UI[key] = v
                page_save()
                if key == "borders":
                    apply_borders_all()
                elif key == "healing" and not v:
                    BANDAGE["serial"] = None
                elif key == "sync" and v and windows is not None:
                    ref = [windows[k] for k in CATS if not windows[k].minimized]
                    sync_sizes(windows, ref[0] if ref else windows[CATS[0]])
                    API.SysMsg(TITLE + ": tracker sizes synced.", Kit.HUE_GOOD)


        def config_closed():
            page["c"] = None
            page_flush_save(True)                  # a change still waiting: written now


        def _thread_wanted():
            """(2.6.82) The script-thread pass only when it has work: a job, a save."""
            return bool(THREAD_JOBS) or bool(SAVE_REQ[0])


        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True, "thread_tick": _thread_tick,
                  "thread_wanted": _thread_wanted,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        return MODULE

    def _part_lookout():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Assistant, loaded by the Virtue Assistant script from
        #  this file uses (API, G, safe, Client, Kit, Follow, HOST, Journal, the main
        #  Modules tab.
        # ============================ MODULE START ===================================
        #  MODULE: Lookout  -  a second client keeps watch for you (2.6.06)
        #
        #  The shard allows a second client. Park a character of the second client
        #  (hidden, standing still) on the approach to where your main character
        #  farms, and run Virtue Assistant with Lookout on in both clients:
        #    - Watch (the lookout's client): twice a second it looks at the players
        #      in range. Anyone who isn't you, your party, your friends list, your
        #      guild or alliance (green) or ignored counts. Each one is reported
        #      once per appearance: not again until they have been out of range
        #      for GONE_SECONDS. With World Map > Map Pings on, a danger map ping
        #      goes on the spot too, so your guildmates see it on their maps.
        #    - Listen (your main client): each report raises an alarm at once (the
        #      alert banner, a client sound, a journal line): "Killer (red),
        #      2 players, 25 tiles NE of the lookout". The window lists the last
        #      few; click a row for a tracking arrow to the spot, Alt+click to
        #      auto-follow a player who is in your own view. Lookout also warns
        #      when the lookout goes quiet (its client closed or lost).
        #  Both can be ticked on one client: it then hears the other clients'
        #  lookouts, never its own.
        #
        #  The link: both clients run from the same TazUO folder, so they share
        #  LegionScripts. The lookout appends a line per report (and a heartbeat
        #  every few seconds) to FEED_NAME, a small file this module makes itself
        #  next to Virtue Assistant; the listener reads only what is new, off the
        #  game's thread. The file is trimmed when it passes FEED_MAX_BYTES. If the
        #  two clients don't share a folder, the Map Pings ping is the fallback.
        #
        #  With Ultima Tracker on, Lookout sees players exactly as the trackers do
        #  (HOST.services["ultima.classify"]: town NPCs, pets and its ignore list
        #  left out); without it, a simpler check of its own.
        #
        #  The lookout never moves, attacks or casts: display and alert only.
        # =============================================================================
        KEY = "lookout"
        TITLE = "Lookout"

        # ------------------------------- CONFIG --------------------------------------
        SETTINGS_KEY = "Lookout_settings"      # per character: "watch=0;listen=1;range=18;ping=1;lost=1"
        POS_KEY = "Lookout_pos"
        MIN_KEY = "Lookout_min"
        FEED_NAME = "_lookout_feed.txt"        # made by this module next to Virtue Assistant (runtime data)
        W = 370                                # full window width
        MINI_W, MINI_H = 280, 46               # minimized bar
        TRAY_ICON = 0x0A25                     # a lantern, on the Action Bar's tray button
        ROWS = 5                               # sightings listed in the window
        ROW_H = 22
        DEFAULT_RANGE = 18                     # tiles the lookout watches (the client's view range)
        RANGE_MIN, RANGE_MAX = 3, 24
        SCAN_EVERY = 0.5                       # seconds between looks at the players in range
        GONE_SECONDS = 30.0                    # out of range this long = the next sighting is a new one
        HEARTBEAT = 5.0                        # seconds between the lookout's "still here" lines
        LOST_SECONDS = 20.0                    # no line from the lookout for this long: it went quiet
        LISTEN_EVERY = 0.25                    # seconds between looks at the feed (listener)
        FEED_MAX_AGE = 15.0                    # a report older than this when read is not raised
        FEED_MAX_BYTES = 32768                 # the feed is trimmed past this size...
        FEED_KEEP = 60                         # ...to its last this many lines
        READ_MAX = 65536                       # bytes read from the feed at most at once
        ANNOUNCE_EVERY = 30.0                  # a listener says "this is me" this often...
        LISTENER_TTL = 120.0                   # ...and the lookout leaves it alone this long after
        LISTENERS_EVERY = 10.0                 # how often the lookout reads who is listening
        OUTBOX_CAP = 200                       # lines kept for the file while it can't be written
        WRITE_RETRY = 1.0                      # seconds before trying again after a failed write
        SEEN_CAP = 400                         # report keys remembered (no report raised twice)
        PRESENT_CAP = 1000                     # players remembered as in range
        WATCHERS_CAP = 8                       # lookouts told apart by the listener
        PING_GIVE_UP = 10.0                    # seconds a map ping keeps waiting for Map Pings' pace
        PING_RETRY = 0.25                      # seconds between asks while Map Pings is paced
        ALERT_ALARM = "lookout.alarm"          # Settings > Alerts: "Lookout spotted a player"
        ALERT_ALARM_SOUND = 0x338              # yell
        ALERT_LOST = "lookout.lost"            # Settings > Alerts: "Lookout went quiet"
        ALERT_LOST_SOUND = 0x04A               # lever
        OWN_ALARM_HOLD = 60.0                  # seconds the window's own line keeps a report red
        ARROW_ID = 0x4C4F4F4B                  # "LOOK": Lookout's own tracking arrow
        NPC_TITLE_RE = re.compile(r"\bthe\s+[a-z]", re.IGNORECASE)   # "Bob the guard" (own check)
        FACETS = ("Felucca", "Trammel", "Ilshenar", "Malas", "Tokuno", "Ter Mur")
        NOTO_WORD = {"murderer": "red", "criminal": "grey", "gray": "grey", "enemy": "orange",
                     "innocent": "blue", "ally": "green", "invulnerable": "yellow"}
        NOTO_HUE = {"murderer": 0x0022, "criminal": 0x03B2, "gray": 0x03B2, "enemy": 0x0090,
                    "innocent": 0x0059, "ally": 0x003F, "invulnerable": 0x0035}
        COMPASS = ("E", "SE", "S", "SW", "W", "NW", "N", "NE")   # clockwise from east (y grows south)
        ROW_TIP = ("Click: a tracking arrow to where they were seen (again to clear it). "
                   "Alt+click: auto-follow (again to stop)")
        # -----------------------------------------------------------------------------

        settings = {"watch": False, "listen": True, "range": DEFAULT_RANGE, "ping": True,
                    "lost": True}
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [],
              "me": 0, "path": None, "facet": -1,
              # watch
              "next_scan": 0.0, "present": {}, "in_range": 0, "hb_next": 0.0, "outbox": [],
              "write_next": 0.0, "pings": [], "ping_next": 0.0, "listeners": {}, "listeners_next": 0.0,
              # listen
              "offset": 0, "listen_next": 0.0, "announce_next": 0.0, "seen": {}, "inbox": [],
              "watchers": {}, "file": "none",
              # both
              "recent": [], "arrow": None, "own_alarm": None, "dirty": True, "refresh_at": 0.0}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}
        page = {"c": None}


        # ---------- saved settings ----------
        def load_settings():
            for part in Kit.get_var(SETTINGS_KEY).split(";"):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                k, v = k.strip(), v.strip()
                if k in ("watch", "listen", "ping", "lost"):
                    settings[k] = v == "1"
                elif k == "range":
                    try:
                        settings["range"] = max(RANGE_MIN, min(RANGE_MAX, int(v)))
                    except ValueError:
                        pass


        def save_settings():
            Kit.put_var(SETTINGS_KEY, "watch=%d;listen=%d;range=%d;ping=%d;lost=%d" % (
                1 if settings["watch"] else 0, 1 if settings["listen"] else 0, settings["range"],
                1 if settings["ping"] else 0, 1 if settings["lost"] else 0))


        def save_pos():
            Kit.save_pos(POS_KEY, win["g"])


        # ---------- small helpers ----------
        def feed_path():
            """The feed beside Virtue Assistant (worked out once per start)."""
            p = st["path"]
            if p is None:
                base = str(safe(lambda: API.ScriptPath, "") or "").rstrip("/\\")
                if base and safe(lambda: os.path.isfile(base), False):
                    base = os.path.dirname(base)
                p = st["path"] = os.path.join(base, FEED_NAME) if base else FEED_NAME
            return p


        def due(now, key, step):
            """True once every `step` seconds (a time far ahead: the clock was set back)."""
            t = st[key]
            if now >= t or t - now > step:
                st[key] = now + step
                return True
            return False


        def noto_name(mob):
            try:
                return str(mob.Notoriety).split(".")[-1].lower()
            except Exception:
                return "unknown"


        def compass(dx, dy):
            if not dx and not dy:
                return ""
            return COMPASS[int(round(math.atan2(dy, dx) / (math.pi / 4))) % 8]


        def clean(text):
            return str(text or "").replace("|", "/").replace("\n", " ").replace("\r", " ").strip()


        def facet_name(m):
            return FACETS[m] if 0 <= m < len(FACETS) else "facet %d" % m


        def ago(t, now):
            d = int(now - t)
            if d < 0:
                d = 0
            if d < 60:
                return "%ds" % d
            if d < 3600:
                return "%dm" % (d // 60)
            return "%dh" % (d // 3600)


        def where_text(ev, short=False):
            """'25 tiles NE of the lookout' ('25 NE' short), or the spot."""
            lx, ly = ev["lx"], ev["ly"]
            if not (lx or ly):
                return "at %d,%d" % (ev["x"], ev["y"])
            dx, dy = ev["x"] - lx, ev["y"] - ly
            d = max(abs(dx), abs(dy))
            if d == 0:
                return "at the lookout"
            if short:
                return "%d %s" % (d, compass(dx, dy))
            return "%d tile%s %s of the lookout" % (d, "" if d == 1 else "s", compass(dx, dy))


        # ---------- the feed: lines ----------
        #  t|serial|name|notoriety|x|y|facet|count|lx|ly|from|pinged
        #  serial 0: not a sighting: notoriety "watch" (heartbeat: x, y = the
        #  lookout, count = players in range now), "off" (the lookout stopped) or
        #  "listen" (a listener saying who it is, so the lookouts leave it alone).
        def line(serial, name, noto, x, y, facet, count, lx, ly, pinged=False):
            s = "%.2f|%d|%s|%s|%d|%d|%d|%d|%d|%d|%d|%d\n" % (
                time.time(), serial, clean(name), clean(noto), x, y, facet, count, lx, ly,
                st["me"], 1 if pinged else 0)
            try:
                return s.encode("utf-8")
            except Exception:
                return s.encode("ascii", "replace")


        def post(data):
            ob = st["outbox"]
            ob.append(data)
            if len(ob) > OUTBOX_CAP:
                del ob[:-OUTBOX_CAP]


        def parse(raw):
            try:
                s = raw.decode("utf-8", "replace").strip()
                if not s:
                    return None
                p = s.split("|")
                if len(p) < 8:
                    return None
                ev = {"t": float(p[0]), "key": p[0], "serial": int(p[1]), "name": p[2],
                      "noto": p[3], "x": int(p[4]), "y": int(p[5]), "facet": int(p[6]),
                      "count": int(p[7]),
                      "lx": int(p[8]) if len(p) > 8 else 0, "ly": int(p[9]) if len(p) > 9 else 0,
                      "from": int(p[10]) if len(p) > 10 else 0,
                      "pinged": len(p) > 11 and p[11] == "1"}
                if not 0.0 < ev["t"] < 1e11:                 # NaN, inf, nonsense
                    return None
                return ev
            except Exception:
                return None


        # ---------- thread_tick: the file (never on the client thread) ----------
        def write_outbox():
            ob = st["outbox"]
            n = len(ob)
            path = feed_path()
            try:
                f = open(path, "ab")
                try:
                    f.write(b"".join(ob[:n]))
                finally:
                    f.close()
            except Exception:
                st["write_next"] = time.time() + WRITE_RETRY  # locked / no folder: a bit later
                return
            del ob[:n]
            try:
                size = os.path.getsize(path)
            except Exception:
                return
            # the lookout keeps the file small; a listener alone only trims a runaway file
            if size > (FEED_MAX_BYTES if settings["watch"] else 4 * FEED_MAX_BYTES):
                trim(path)


        def trim(path):
            try:
                f = open(path, "rb")
                try:
                    data = f.read()
                finally:
                    f.close()
                lines = [ln for ln in data.split(b"\n") if ln.strip()]
                keep = lines[-FEED_KEEP:]
                # a listener's "this is me" line is kept however old the rest is, or the
                # lookout would report your own character walking past it after a trim
                heard = set()
                for ln in reversed(lines[:-FEED_KEEP]):
                    if b"|listen|" in ln and len(heard) < WATCHERS_CAP:
                        ev = parse(ln)
                        if ev is not None and ev["from"] not in heard:
                            heard.add(ev["from"])
                            keep.insert(0, ln)
                f = open(path, "wb")
                try:
                    f.write(b"\n".join(keep) + (b"\n" if keep else b""))
                finally:
                    f.close()
            except Exception:
                pass


        def read_new(path):
            """The complete lines added since the last read (bytes), or None."""
            try:
                size = os.path.getsize(path)
            except Exception:
                st["file"] = "none"
                return None
            off = st["offset"]
            if size < off:                                   # trimmed or made anew
                off = 0
            if size - off > READ_MAX:                        # a big file: only its end matters
                off = size - READ_MAX
                skip_first = True
            else:
                skip_first = off > 0 and off != st["offset"]
            if size == off:
                st["offset"] = off
                st["file"] = "ok"
                return None
            try:
                f = open(path, "rb")
                try:
                    f.seek(off)
                    data = f.read(min(size - off, READ_MAX))
                finally:
                    f.close()
            except Exception:
                st["file"] = "busy"
                return None
            st["file"] = "ok"
            cut = data.rfind(b"\n")
            if cut < 0:
                if len(data) >= READ_MAX:                    # no line at all in it: garbage
                    st["offset"] = off + len(data)
                else:
                    st["offset"] = off                       # a line still being written
                return None
            st["offset"] = off + cut + 1
            lines = data[:cut].split(b"\n")
            if skip_first and lines:
                lines = lines[1:]                            # it started mid-line
            return lines


        def read_feed(now):
            lines = read_new(feed_path())
            if not lines:
                return
            me = st["me"]
            seen = st["seen"]
            inbox = st["inbox"]
            for raw in lines:
                ev = parse(raw)
                if ev is None or ev["from"] == me or ev["noto"] == "listen":
                    continue
                k = (ev["key"], ev["serial"], ev["from"])
                if k in seen:
                    continue
                age = now - ev["t"]
                if age < -5.0 or (ev["serial"] and age > FEED_MAX_AGE):
                    continue                                 # from the future, or a stale report
                seen[k] = ev["t"]
                inbox.append(ev)
            if len(seen) > SEEN_CAP:
                cut = now - 4 * FEED_MAX_AGE
                for k in [k for k, t in seen.items() if t < cut]:
                    del seen[k]
                if len(seen) > SEEN_CAP:                     # a flood: keep the newest half
                    newest = sorted(seen.items(), key=lambda kv: kv[1])[-(SEEN_CAP // 2):]
                    seen.clear()
                    seen.update(newest)
            if len(inbox) > 100:
                del inbox[:-100]


        def read_listeners(now):
            """Lookout: who is listening (their characters are never reported)."""
            path = feed_path()
            try:
                size = os.path.getsize(path)
                f = open(path, "rb")
                try:
                    if size > READ_MAX:
                        f.seek(size - READ_MAX)
                    data = f.read(READ_MAX)
                finally:
                    f.close()
            except Exception:
                return
            out = {}
            for raw in data.split(b"\n"):
                if b"|listen|" not in raw:
                    continue
                ev = parse(raw)
                if ev is not None and ev["noto"] == "listen" and ev["from"] and \
                        -5.0 <= now - ev["t"] <= LISTENER_TTL:
                    out[ev["from"]] = ev["t"]
            st["listeners"] = out


        def _thread_tick():
            """Script thread, right after the client tick: the feed file."""
            if st["shutting"]:
                return
            now = time.time()
            if settings["listen"] and st["me"] and due(now, "announce_next", ANNOUNCE_EVERY):
                post(line(0, "", "listen", 0, 0, st["facet"], 0, 0, 0))
            if st["outbox"] and (now >= st["write_next"] or st["write_next"] - now > WRITE_RETRY):
                write_outbox()
            if settings["watch"] and due(now, "listeners_next", LISTENERS_EVERY):
                read_listeners(now)
            if settings["listen"] and st["me"] and due(now, "listen_next", LISTEN_EVERY):
                read_feed(now)


        # ---------- Watch (client thread) ----------
        def own_check(m, serial):
            """Without Ultima Tracker: the notoriety of a player who counts, or None."""
            if m.IsRenamable:                                # your pets and hirelings
                return None
            noto = noto_name(m)
            if noto in ("invulnerable", "ally"):             # vendors / guards; your guild or alliance
                return None
            if not (m.IsHuman or m.IsGargoyle):              # a creature
                return None
            if API.IsFriend(serial):
                return None
            if NPC_TITLE_RE.search(str(m.Name or "")):       # "Bob the guard"
                return None
            return noto


        def watch_scan(now):
            # (2.6.82) the mother's per-pass player and mobile list when it has them
            # (client thread: the same values a fresh read gives this pass)
            fn = getattr(HOST, "me", None)
            p = fn() if fn is not None else API.Player
            if p is None:
                return
            me = int(p.Serial)
            mx, my = int(p.X), int(p.Y)
            try:
                facet = int(API.GetMap())
            except Exception:
                facet = 0
            st["me"], st["facet"] = me, facet
            try:
                fn = getattr(HOST, "mobiles", None)
                if fn is not None:
                    mobs = fn(distance=settings["range"])
                else:
                    mobs = API.GetAllMobiles(distance=settings["range"]) or []
            except Exception:
                mobs = []
            try:
                party = set(int(s) for s in (API.GetPartyMemberSerials() or ()))
            except Exception:
                party = set()
            svc = HOST.services.get("ultima.classify")
            listeners = st["listeners"]
            counted = []
            for m in mobs:
                try:
                    if m is None:
                        continue
                    serial = int(m.Serial)
                    if serial == me or serial in party or serial in listeners:
                        continue
                    if svc is not None:
                        # (2.6.82) the trackers' answer says whether it is a ghost (IsDead
                        # read once, there); the dead are skipped as before
                        r = svc(m, party, with_dead=True)
                        if r is None or r[0] == "friend" or (len(r) > 3 and r[3]):
                            continue
                        noto = r[2]
                    else:
                        if m.IsDead:
                            continue
                        noto = own_check(m, serial)
                        if noto is None:
                            continue
                    try:
                        if API.OnIgnoreList(serial):         # TazUO's own ignore list
                            continue
                    except Exception:
                        pass
                    counted.append((serial, m, noto))
                except Exception:
                    continue
            present = st["present"]
            fresh = []
            for serial, m, noto in counted:
                t = present.get(serial)
                if t is None or now - t > GONE_SECONDS:
                    fresh.append((serial, m, noto))
                present[serial] = now
            if len(present) > len(counted):
                for s in [s for s, t in present.items() if not 0 <= now - t <= GONE_SECONDS]:
                    del present[s]
                if len(present) > PRESENT_CAP:
                    present.clear()
            n = len(counted)
            if n != st["in_range"]:
                st["in_range"] = n
                st["dirty"] = True
            ping_on = settings["ping"] and HOST.services.get("pings.send") is not None
            said = []
            for serial, m, noto in fresh:
                try:
                    name, x, y = str(m.Name or "") or "(unknown)", int(m.X), int(m.Y)
                except Exception:
                    continue
                # (2.6.81) UT2-3: "pinged" in the feed only when a ping is really
                # queued (the queue holds 8), so the listener pings the rest itself
                will_ping = ping_on and len(st["pings"]) < 8
                post(line(serial, name, noto, x, y, facet, n, mx, my, will_ping))
                if will_ping:
                    st["pings"].append([x, y, facet, "Lookout: " + name, now + PING_GIVE_UP])
                ev = {"t": now, "serial": serial, "name": name, "noto": noto, "x": x, "y": y,
                      "facet": facet, "count": n, "lx": mx, "ly": my, "src": "here"}
                remember(ev)
                said.append("%s (%s)" % (name, NOTO_WORD.get(noto, noto)))
            if said:                                         # one journal line, however many came
                API.SysMsg("%s: spotted %s, %d player%s in range." % (
                    TITLE, ", ".join(said[:4]) + (" and %d more" % (len(said) - 4) if len(said) > 4
                                                  else ""), n, "" if n == 1 else "s"), Kit.HUE_INFO)
            if fresh or due(now, "hb_next", HEARTBEAT):
                st["hb_next"] = now + HEARTBEAT
                post(line(0, "", "watch", mx, my, facet, n, mx, my))


        def send_pings(now):
            jobs = st["pings"]
            if not jobs or (now < st["ping_next"] and st["ping_next"] - now <= PING_RETRY):
                return
            fn = HOST.services.get("pings.send")
            if fn is None or not settings["ping"]:
                del jobs[:]
                return
            x, y, m, who, until = jobs[0]
            if not 0 <= until - now <= PING_GIVE_UP:
                jobs.pop(0)
                return
            try:
                ok = fn(x, y, m, "danger", who)
            except Exception:
                ok = True                                    # it failed outright: don't retry
            if ok:
                jobs.pop(0)
            else:
                st["ping_next"] = now + PING_RETRY           # Map Pings' pace: ask again soon


        def watch_off():
            """The lookout stops: listeners hear it stopped (no "went quiet" alarm)."""
            st["present"].clear()
            st["in_range"] = 0
            del st["pings"][:]
            if st["me"]:
                post(line(0, "", "off", 0, 0, st["facet"], 0, 0, 0))
            st["dirty"] = True


        # ---------- Listen (client thread) ----------
        def remember(ev):
            rec = st["recent"]
            rec.insert(0, ev)
            del rec[ROWS:]
            st["dirty"] = True


        def heard(ev, now):
            """A heartbeat / stop line from a lookout."""
            ws = st["watchers"]
            w = ws.get(ev["from"])
            if w is None:
                if len(ws) >= WATCHERS_CAP:
                    oldest = min(ws, key=lambda k: ws[k]["t"])
                    del ws[oldest]
                w = ws[ev["from"]] = {"t": 0.0, "told": False}
            if ev["t"] < w["t"]:
                return                                       # an older line read late
            w.update({"t": ev["t"], "state": ev["noto"], "x": ev["x"], "y": ev["y"],
                      "facet": ev["facet"], "count": ev["count"]})
            # a line too old to be live counts as already told (no alarm for it)
            w["told"] = ev["noto"] != "watch" or not -5.0 <= now - ev["t"] <= LOST_SECONDS
            st["dirty"] = True


        def raise_alarm(ev):
            noto = ev["noto"]
            text = "%s (%s)%s, %s" % (ev["name"], NOTO_WORD.get(noto, noto),
                                       (", %d players" % ev["count"]) if ev["count"] > 1 else "",
                                       where_text(ev))
            if ev["facet"] != st["facet"] and st["facet"] >= 0:
                text += " in " + facet_name(ev["facet"])
            ping = None
            if settings["ping"] and not ev["pinged"] and ev["facet"] == st["facet"] and \
                    HOST.services.get("pings.send") is not None:
                ping = (ev["x"], ev["y"])                    # the lookout couldn't ping: we do
            fn = getattr(HOST, "alert", None)
            done = False
            if fn is not None:
                try:
                    fn(ALERT_ALARM, text, level="alarm", ping=ping, who=ev["serial"])
                    done = True
                except Exception:
                    done = False
            if not done:                                     # a Virtue Assistant without alerts
                API.SysMsg("%s: %s." % (TITLE, text), Kit.HUE_BAD)
                safe(lambda: API.PlaySound(ALERT_ALARM_SOUND))
            st["own_alarm"] = (text, time.time())
            ev["src"] = "lookout"
            remember(ev)


        def listen_tick(now):
            inbox = st["inbox"]
            if inbox:
                items, st["inbox"] = inbox, []
                for ev in items:
                    if ev["serial"]:
                        raise_alarm(ev)
                    else:
                        heard(ev, now)
            if not settings["lost"]:
                return
            for frm, w in st["watchers"].items():
                if w["told"] or w.get("state") != "watch":
                    continue
                age = now - w["t"]
                if age > LOST_SECONDS:
                    w["told"] = True
                    st["dirty"] = True
                    text = "no word from the lookout for %d s" % int(age)
                    fn = getattr(HOST, "alert", None)
                    if fn is not None:
                        safe(lambda: fn(ALERT_LOST, "The lookout has gone quiet: " + text,
                                        level="warn", who=frm))
                    else:
                        API.SysMsg("%s: the lookout has gone quiet; %s." % (TITLE, text),
                                   Kit.HUE_BAD)


        # ---------- the window ----------
        queue = Kit.queuer(st)
        on_disposed = Kit.disposer(KEY, st, win)


        def row_handler(i):
            """Row i's click: Alt+click follows, a click toggles the tracking arrow.
            A click within 0.15 s of the row changing acts on what was shown before."""
            def handler():
                rows = win["rows"]
                if i >= len(rows):
                    return
                r = rows[i]
                ev = r["ev"]
                if r["prev"] is not None and time.time() - r["at"] <= 0.15:
                    ev = r["prev"]
                if ev is None:
                    return
                if Follow.alt_held():
                    queue(("follow", ev["serial"]))()
                    return
                queue(("arrow", ev["x"], ev["y"], ev["facet"]))()
            return handler


        def body_y():
            return Kit.MARGIN + 30 + Kit.GAP


        SEC_A = 58


        def full_h():
            return body_y() + SEC_A + Kit.GAP + 30 + ROWS * ROW_H + 6 + Kit.MARGIN


        def build_window():
            w, h = (MINI_W, MINI_H) if st["minimized"] else (W, full_h())
            x, y = Kit.load_pos(POS_KEY, (220, 220), (w, h))
            if Kit.is_open(win["g"]):
                x, y = win["g"].GetX(), win["g"].GetY()
            old, win["g"] = win["g"], None
            M = Kit.MARGIN
            store = ({}, {})
            c = {}
            rows = []
            g = G.CreateGump(True, True)
            if st["minimized"]:
                c["mini"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
            else:
                IW = w - 2 * M
                Kit.add_window_frame(g, w, h)
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"))
                ya = body_y()
                Kit.add_section(g, M, ya, IW, SEC_A)
                xc = w - M - 12 - 35 - Kit.text_w("Clear")
                Kit.art_button(g, store, "clear", Kit.ART_CLOSE, xc, ya + 28, "Clear",
                               "Clear the list, the window's alarm line and the tracking arrow",
                               on_click=queue("clear"))
                c["watch"] = Kit.add_label(g, "", M + 12, ya + 9, Kit.HUE_INFO)
                c["listen"] = Kit.add_label(g, "", M + 12, ya + 32, Kit.HUE_INFO)
                c["tw"] = (IW - 24, xc - 8 - (M + 12))       # room for the two lines
                yb = ya + SEC_A + Kit.GAP
                Kit.add_section(g, M, yb, IW, 30 + ROWS * ROW_H + 6, "SPOTTED  (newest first)")
                for i in range(ROWS):
                    yr = yb + 28 + i * ROW_H
                    r = {"name": Kit.add_label(g, "", M + 12, yr + 2, Kit.HUE_TEXT),
                         "info": Kit.add_label(g, "", M + 12 + 180, yr + 2, Kit.HUE_INFO),
                         "ev": None, "prev": None, "at": 0.0, "tip": None, "shown": True}
                    r["hit"] = Kit.catcher(g, M + 6, yr, IW - 12, ROW_H, row_handler(i), "")
                    rows.append(r)
            Kit.place(g, x, y, w, h)
            win.update({"g": g, "c": c, "store": store, "rows": rows})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))
            if st["minimized"] and st["docked"]:              # folded into the Action Bar
                safe(lambda: setattr(g, "IsVisible", False))
            st["dirty"] = True
            refresh(time.time())
            Kit.dispose(old)


        def watch_text():
            """The Watch line's status (without its "Watch: " prefix) and hue."""
            if not settings["watch"]:
                return "off", Kit.HUE_INFO
            n = st["in_range"]
            if n:
                return "%d tiles, %d player%s in range" % (
                    settings["range"], n, "" if n == 1 else "s"), Kit.HUE_BAD
            return "%d tiles, all clear" % settings["range"], Kit.HUE_GOOD


        def listen_text(now):
            """The Listen line's status (without its "Listen: " prefix) and hue."""
            if not settings["listen"]:
                return "off", Kit.HUE_INFO
            best = None
            for w in st["watchers"].values():
                if best is None or w["t"] > best["t"]:
                    best = w
            if best is None:
                if st["file"] == "busy":
                    return "the feed is busy, trying again", Kit.HUE_INFO
                return "no lookout heard yet", Kit.HUE_INFO
            age = ago(best["t"], now)
            if best.get("state") == "off":
                return "the lookout stopped %s ago" % age, Kit.HUE_INFO
            if not -5.0 <= now - best["t"] <= LOST_SECONDS:
                return "the lookout has been quiet for %s" % age, Kit.HUE_BAD
            n = best.get("count", 0)
            where = "%d,%d" % (best.get("x", 0), best.get("y", 0))
            if n:
                return "the lookout at %s sees %d player%s" % (where, n, "" if n == 1 else "s"), \
                    Kit.HUE_BAD
            return "the lookout at %s, all clear" % where, Kit.HUE_GOOD


        def mini_text(now):
            """The minimized bar: "Lookout: <status>"."""
            a = st["own_alarm"]
            if a is not None and 0 <= now - a[1] <= OWN_ALARM_HOLD:
                text, hue = a[0], Kit.HUE_BAD
            elif settings["listen"]:
                text, hue = listen_text(now)
            else:
                text, hue = watch_text()
            return "%s: %s" % (TITLE, text), hue


        def show_row(r, ev, now):
            if ev is not r["ev"]:
                r["prev"], r["ev"], r["at"] = r["ev"], ev, now
            if ev is None:
                if r["shown"]:
                    Kit.set_text(r["name"], "")
                    Kit.set_text(r["info"], "")
                    safe(lambda: setattr(r["hit"], "IsVisible", False))
                    r["shown"] = False
                return
            if not r["shown"]:
                safe(lambda: setattr(r["hit"], "IsVisible", True))
                r["shown"] = True
            noto = ev["noto"]
            Kit.set_text(r["name"], Kit.fit("%s (%s)" % (ev["name"], NOTO_WORD.get(noto, noto)), 172),
                         NOTO_HUE.get(noto, Kit.HUE_TEXT))
            src = "lookout" if ev.get("src") == "lookout" else "here"
            where = where_text(ev, True) if src == "lookout" else "%d,%d" % (ev["x"], ev["y"])
            Kit.set_text(r["info"], Kit.fit("%s, %s ago (%s)" % (where, ago(ev["t"], now), src),
                                            W - 2 * Kit.MARGIN - 196))
            tip = "%s (%s), seen %s at %d,%d%s. %s" % (
                ev["name"], NOTO_WORD.get(noto, noto), "by the lookout" if src == "lookout" else "here",
                ev["x"], ev["y"], "" if ev["facet"] == st["facet"] else " in " + facet_name(ev["facet"]),
                ROW_TIP)
            if tip != r["tip"]:
                r["tip"] = tip
                safe(lambda: r["hit"].SetTooltip(tip))


        def refresh(now):
            """Draw what changed (only what is on screen)."""
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]):
                return
            c = win["c"]
            if st["minimized"]:
                text, hue = mini_text(now)
                Kit.set_text(c["mini"], Kit.fit(text, MINI_W - 90), hue)
                return
            tw = c["tw"]
            text, hue = watch_text()
            Kit.set_text(c["watch"], Kit.fit("Watch: " + text, tw[0]), hue)
            text, hue = listen_text(now)
            a = st["own_alarm"]
            if a is not None and 0 <= now - a[1] <= OWN_ALARM_HOLD:
                text, hue = a[0], Kit.HUE_BAD                # the last report, red for a minute
            else:
                text = "Listen: " + text
            Kit.set_text(c["listen"], Kit.fit(text, tw[1]), hue)
            rec = st["recent"]
            rows = win["rows"]
            for i, r in enumerate(rows):
                show_row(r, rec[i] if i < len(rec) else None, now)
            if not rec and rows:                             # the empty state, in the first row
                Kit.set_text(rows[0]["name"], "No one spotted yet.", Kit.HUE_INFO)


        def toggle_arrow(x, y, m):
            here = st["facet"]
            cur = st["arrow"]
            safe(lambda: API.TrackingArrow(-1, -1, ARROW_ID))
            st["arrow"] = None
            if cur == (x, y, m):
                return                                       # the same spot again: off
            if here >= 0 and m != here:
                API.SysMsg("%s: that spot is in %s." % (TITLE, facet_name(m)), Kit.HUE_INFO)
                return
            API.TrackingArrow(x, y, ARROW_ID)
            st["arrow"] = (x, y, m)


        def clear_arrow():
            if st["arrow"] is not None:
                st["arrow"] = None
                safe(lambda: API.TrackingArrow(-1, -1, ARROW_ID))


        # ---------- settings page ----------
        SEC_H = 172


        def config_height(w):
            return SEC_H


        def build_config(g, x, y, w):
            Kit.add_section(g, x, y, w, SEC_H, "WATCH AND LISTEN  (two clients, one TazUO folder)")
            c = {"watch": Kit.add_check(g, "Watch: this client is the lookout", x + 12, y + 32,
                                        settings["watch"],
                                        "Park it hidden and standing still; it reports every "
                                        "player who comes into range to the other client (not "
                                        "your party, friends or guild)"),
                 "listen": Kit.add_check(g, "Listen: this client gets the alarms", x + 12, y + 58,
                                         settings["listen"],
                                         "Raise an alarm for each player a lookout reports "
                                         "(sound: Settings > Alerts)")}
            Kit.add_label(g, "Watch range:", x + 12, y + 90)
            c["range"] = Kit.add_slider(g, x + 120, y + 88, 160, RANGE_MIN, RANGE_MAX,
                                        settings["range"])
            safe(lambda: c["range"].SetTooltip("Tiles round the lookout it watches (%d-%d)"
                                               % (RANGE_MIN, RANGE_MAX)))
            c["range_v"] = Kit.add_label(g, "%d tiles" % settings["range"], x + 290, y + 90,
                                         Kit.HUE_INFO)
            c["ping"] = Kit.add_check(g, "Danger ping on the map where a player is spotted",
                                      x + 12, y + 116, settings["ping"],
                                      "Needs World Map > Map Pings on; your guildmates see the "
                                      "ping on their maps too")
            c["lost"] = Kit.add_check(g, "Warn when the lookout goes quiet (%d s without a word)"
                                      % int(LOST_SECONDS), x + 12, y + 142, settings["lost"],
                                      "An alarm when no word comes from the lookout: its client "
                                      "closed, crashed or lost the connection")
            page["c"] = c


        def _slider_value(s, default):
            try:
                v = s.Value
            except Exception:
                v = safe(lambda: s.GetValue(), default)
            try:
                return int(v)
            except Exception:
                return default


        def poll_config():
            c = page["c"]
            if c is None:
                return
            changed = False
            for k in ("watch", "listen", "ping", "lost"):
                try:
                    on = bool(c[k].IsChecked)
                except Exception:
                    on = settings[k]
                if on != settings[k]:
                    settings[k] = on
                    changed = True
                    apply_toggle(k, on)
            rng = max(RANGE_MIN, min(RANGE_MAX, _slider_value(c["range"], settings["range"])))
            if rng != settings["range"]:
                settings["range"] = rng
                Kit.set_text(c["range_v"], "%d tiles" % rng)
                changed = True
            if changed:
                save_settings()
                st["dirty"] = True


        def apply_toggle(k, on):
            now = time.time()
            if k == "watch":
                if on:
                    st["next_scan"] = st["hb_next"] = st["listeners_next"] = 0.0
                else:
                    watch_off()
            elif k == "listen":
                if on:
                    st["listen_next"] = st["announce_next"] = 0.0
                else:
                    st["inbox"] = []
            elif k == "ping" and not on:
                del st["pings"][:]
            st["refresh_at"] = now


        def config_closed():
            page["c"] = None


        # ---------- module hooks ----------
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "me": 0, "path": None,
                       "facet": -1, "next_scan": 0.0, "present": {}, "in_range": 0, "hb_next": 0.0,
                       "outbox": [], "write_next": 0.0, "pings": [], "ping_next": 0.0, "listeners": {},
                       "listeners_next": 0.0, "offset": 0, "listen_next": 0.0,
                       "announce_next": 0.0, "seen": {}, "inbox": [], "watchers": {},
                       "file": "none", "recent": [], "arrow": None, "own_alarm": None,
                       "dirty": True, "refresh_at": 0.0,
                       "minimized": Kit.load_min(MIN_KEY) or
                       bool(safe(lambda: HOST.dock_wanted(KEY), False))})
            load_settings()
            try:
                p = API.Player
                st["me"] = int(p.Serial) if p is not None else 0
                st["facet"] = int(API.GetMap())
            except Exception:
                pass
            feed_path()
            fn = getattr(HOST, "alert_kind", None)           # listed on Settings > Alerts
            if fn is not None:
                safe(lambda: fn(ALERT_ALARM, "Lookout spotted a player", ALERT_ALARM_SOUND))
                safe(lambda: fn(ALERT_LOST, "Lookout went quiet", ALERT_LOST_SOUND))
            build_window()
            try:                                   # (2.6.55) the layout may scale the window
                hooks = Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"), scale=True)
            except TypeError:                      # an older mother: the plain call
                hooks = Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"))
            HOST.dock_add(KEY, hooks)


        def _tick():
            if win["g"] is None:
                return
            if Kit.was_clicked(win["store"], "close"):
                Kit.dispose(win["g"])                        # on_disposed turns the module off
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
                    build_window()
                elif action == "clear":
                    st["recent"] = []
                    st["own_alarm"] = None
                    clear_arrow()
                    st["dirty"] = True
                elif kind == "follow":
                    Follow.toggle(action[1], TITLE)
                elif kind == "arrow":
                    toggle_arrow(action[1], action[2], action[3])
            now = time.time()
            if settings["watch"]:
                if due(now, "next_scan", SCAN_EVERY):
                    watch_scan(now)
                send_pings(now)
            elif settings["listen"] and due(now, "next_scan", 1.0):
                # who am I and where: own lines are skipped, a report on another facet says so
                try:
                    p = API.Player
                    if p is not None:
                        st["me"] = int(p.Serial)
                        st["facet"] = int(API.GetMap())
                except Exception:
                    pass
            if settings["listen"]:
                listen_tick(now)
            if st["dirty"] or due(now, "refresh_at", 1.0):
                st["dirty"] = False
                refresh(now)


        def _stop():
            st["shutting"] = True
            HOST.dock_remove(KEY)
            if settings["watch"] and st["me"]:
                # the one write outside thread_tick: none runs after stop, and without
                # it a listener would take the stop for a lookout gone quiet
                post(line(0, "", "off", 0, 0, st["facet"], 0, 0, 0))
                write_outbox()
            clear_arrow()
            save_pos()
            Kit.save_min(MIN_KEY, st["minimized"])
            save_settings()
            g, win["g"] = win["g"], None
            win["rows"] = []
            Kit.dispose(g)


        load_settings()
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True,          # tick on the client thread: no waits in it
                  "thread_tick": _thread_tick,  # the feed file, on the script's thread
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        # ============================= MODULE END ====================================
        return MODULE

    # ---------- the parts, run side by side by the mother's PartSet ----------
    #  (part key, builder, tick interval, the 2.6.06 module key it keeps)
    PARTS = (
        ("tracker", _part_tracker, 0.05, "ultima"),
        ("lookout", _part_lookout, 0.1, "lookout"),
    )
    MODULE = PartSet(KEY, TITLE, PARTS).hooks()
    return MODULE


# ------------------------- registration with Virtue Assistant ----------------
if "HOST" in globals() and hasattr(globals()["HOST"], "add"):
    HOST.add("ultima", "Ultima Tracker",
             "Who is around you: friends, foes and neutrals, with bars",
             _module_ultima, 0.05,
             category="The world",
             parts=(
                 ("tracker", "Tracker",
                  "Trackers and combat bars for the players around you", True, ("ultima",)),
                 ("lookout", "Lookout",
                  "A second client watches a spot and raises the alarm here", False, ("lookout",)),
             ),
             aliases=('Combat Bars', 'Lookout', 'foe', 'sightings', 'trackers', 'second client'))
else:
    import API
    API.SysMsg("Ultima Tracker is a Virtue Assistant module and can't run on its own. "
               "Run Virtue Assistant instead; it loads this file.", 33)
