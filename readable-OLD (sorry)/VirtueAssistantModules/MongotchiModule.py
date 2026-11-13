# =============================================================================
#  Mongotchi: a Virtue Assistant module (TazUO Legion script, IronPython 3.4)
#  Shard: In Mani Ylem
#
#  This file is not a script to run on its own. It is one module of Virtue Assistant, loaded by
#  the mother script from the modules folder beside it. The mother provides everything used here
#  (API, Kit, HOST, safe, the main loop and the settings window), so run that and tick Mongotchi
#  on its Modules tab. To leave the module out, take this file out of the folder.
#  Module key: "mongotchi", category "Extras". Everything lives inside one function,
#  _module_mongotchi, so the module shares the mother's namespace without leaking names into it;
#  it ends by returning the MODULE hook table the mother calls (start, tick, stop, interval).
#
#  Mongbat plus Tamagotchi: raise a small pet in a window of its own.
#
#  CARE: feed it from the pantry, play with its toy, brush it, clean the pen, put it to bed
#  (Lights), cure it when sick, send it foraging when the pantry runs low, click it to pet it.
#  Its mood is shown as a UO pet loyalty text. It grows from pup to mongotchi to Greater
#  Mongotchi (only when well cared for); neglected too long it goes wild.
#
#  GREMLINS: they sneak into the pen and steal half the food. Click one before it reaches the
#  pantry to swat it. A brave pet may chase it off on its own.
#
#  SQUEAKS AND SHOP: care earns squeaks, which also trickle in at a fixed rate while the module
#  is closed (caught up at start, up to a day's worth). They are spent in the Shop.
#
#  PLAYPEN: Share posts the pet as a 64-character code in chat; other players running the module
#  pick the code up from their journal and the pet appears in their playpen. The code is posted
#  only on a player's press, never on a timer (shard rule R1); the reminder only prints a
#  journal line.
#
#  JOURNEYS: treasure hunts, meditation at virtue shrines (virtue levels change how the pet
#  behaves) and relics. Trips carry on while the module is closed.
#
#  SEASONS: the computer's calendar decides which seasonal shop items are on sale.
#
#  ACHIEVEMENTS: sixteen milestones, each paying a squeak reward once.
#
#  COMPANION: a bought charm brings the pet into the world as a client-side effect only the
#  player sees; it reacts to what happens and obeys spoken pet commands.
#
#  ANIMATION: item art cannot be flipped or faded, so every movement is done by moving, resizing
#  and re-hueing picture boxes, all of it through the View class below, which touches a control
#  only when its value changed.
#
#  Time passes for the pet only while the module is on, unless "Keep living while the module
#  is off" is ticked on its settings page.
# =============================================================================
def _module_mongotchi():
    """Build the Mongotchi module in its own namespace and return its hooks.

    Everything (settings, pet, shop, windows, companion, playpen) lives in this one function's scope,
    so the module's names never leak into the mother script. The returned MODULE table holds start,
    tick, stop and interval, which the mother calls. Code helpers shared with other modules
    (Base64 packing, checksum, streamer veils) come from Kit. Random numbers come from the module's
    own Rng, named random inside the scope, so the standard random module (which loads os) is never
    imported.
    """
    KEY = "mongotchi"
    TITLE = "Mongotchi"
    SETTINGS_KEY = "Mongotchi_settings"
    # Item art: graphic ids from the client's tiledata. The pup is the folded figurine, the adult
    # has its wings spread.
    GFX_PUP = 0x20F9
    import _random

    class Rng(_random.Random):
        """Random number source over the built-in _random generator, with the few calls the module uses.

        It stands in for the standard random module: same method names and the same kind of results, but
        nothing beyond _random is imported at start-up. _random seeds itself from the system.
        """
        def below(self, n):
            """Return a whole number from 0 up to but not including `n`, every value equally likely.

            Draws just enough random bits and tries again when the draw is too big, so there is no bias.
            """
            k = n.bit_length()
            r = self.getrandbits(k)
            while r >= n:
                r = self.getrandbits(k)
            return r

        def randint(self, a, b):
            """Return a whole number from `a` up to and including `b`.

            Raises ValueError for a non-integer or empty range, as random.randint does.
            """
            lo, hi = int(a), int(b)
            if lo != a or hi != b or hi < lo:
                raise ValueError("empty or non-integer range for randint()")
            return lo + self.below(hi - lo + 1)

        def uniform(self, a, b):
            """Return a float between `a` and `b`."""
            return a + (b - a) * self.random()

        def choice(self, seq):
            """Return one item of the non-empty sequence `seq` at random.

            Raises IndexError for an empty sequence, as random.choice does.
            """
            n = len(seq)
            if not n:
                raise IndexError("Cannot choose from an empty sequence")
            return seq[self.below(n)]

    random = Rng()
    GFX_ADULT = 0x25A6
    # Screen pixels per pixel of the gremlin line drawing, which is built from plain colour boxes
    # because no item art looks like it.
    GREM_PX = 2
    GREMLIN_COLOR = "#FFFFFF"
    GFX_MESS = 0x0F3B
    GFX_CURE = 0x0F07
    GFX_BRUSH = 0x1373
    FOODS = [(0x09D0, "an apple", 20), (0x09C9, "a ham", 35), (0x097B, "a fish steak", 30),
             (0x09D1, "some grapes", 20), (0x103B, "a loaf of bread", 25), (0x171F, "a banana", 20)]
    # Hues (Hues.mul indexes). HUE_GREATER is the Greater Mongotchi's colour when it is not dyed.
    HUE_GREATER = 1161
    HUE_SICK = 2213
    HUE_SLEEP = 1102
    HUE_WHITE = 1153
    HUE_ZZZ = 1152
    HUE_STINK = 2006
    HUE_CRUMB = 1505
    HUE_DIZZY = 1173
    HUE_HEART = 33
    HUE_HEART2 = 38
    HUE_PINK = 1201
    # Sounds, as API.PlaySound takes them (Sound.mul indexes).
    SND_HURT = 0x1A9
    SND_EAT = 0x03A
    SND_CLEAN = 0x057
    SND_CURE = 0x1E0
    SND_GROW = 0x1FE
    SND_GREMLIN = 0x42A
    SND_SWAT = 0x3B2
    SND_OOF = 0x436
    # Seconds between the smack and the gremlin's "oof".
    OOF_DELAY = 0.15
    SND_FOOD = 0x035
    SND_BUY = 0x036
    SND_TRAP = 0x02B
    # The pet's needs: points lost or gained per hour at a pace of 100%. Stats run 0 to 100.
    RATE_FOOD = 30.0
    RATE_JOY = 20.0
    RATE_JOY_NEED = 15.0
    RATE_ENERGY = 15.0
    RATE_SLEEP = 50.0
    RATE_DIRT = 6.0
    RATE_DIRT_MESS = 12.0
    # Minutes between heaps left in the pen, and the most heaps at once.
    MESS_MIN, MESS_MAX = 30, 60
    MESS_MAX_N = 3
    # One name per heap slot, for each heap's own pop-in animation.
    MESS_KINDS = tuple("mess%d" % _i for _i in range(MESS_MAX_N))
    # Sickness: chance per hour while the pen is dirty or the pet starving, and the hours of
    # untreated sickness that count as neglect.
    SICK_DIRTY = 0.5
    SICK_STARVE = 0.3
    SICK_NEGLECT = 1.0
    # Neglect timers in hours: how long before it goes wild, and when the journal first warns.
    FERAL_HOURS = 2.0
    WARN_HOURS = 0.5
    # Growth: the pup grows up at this age; a Greater Mongotchi needs the later age and an average
    # mood of at least GREATER_CARE.
    PUP_HOURS = 1.0
    GREATER_HOURS = 6.0
    GREATER_CARE = 75.0
    # Pantry sizes (food items): the starting stock, the normal limit and the Bigger Pantry limit.
    PANTRY_START = 5
    PANTRY_MAX = 12
    PANTRY_BIG = 20
    SUPPLY_MIN = 30
    # How long a forage trip takes, as a random range in seconds.
    FORAGE_SECS = (25, 45)
    MEDITATE_MIN = 20.0
    MEDITATE_XP = 60.0
    HUNT_ROLLS = (2, 4)
    HUNT_ENERGY = 20
    FORAGE_ENERGY = 15
    VIRTUE_MAX = 10
    RELIC_BONUS = 0.01
    # What one level of a virtue does. The effect texts in VIRTUES are built from these numbers,
    # so a change here changes the text as well.
    VIRTUE_FX = {"hon_price": 0.02, "com_pet": 1.0, "com_joy_loss": 0.03, "com_heal_secs": 4.0, "val_guard": 0.05,
        "val_danger": 0.06, "val_dive": 0.04, "jus_back": 0.05, "jus_squeaks": 0.1, "sac_per": 4, "sac_energy": 1,
        "sac_forage_min": 5, "sac_hunt_min": 8, "hnr_squeaks": 0.02, "spi_meditate": 0.05, "spi_relic": 0.04,
        "spi_sick": 0.05, "spi_copy": 0.03, "hum_hunger": 0.02, "hum_need": 0.04,}
    # Companion timings: seconds between its "heals" and the chance it copies a spell you cast.
    COMP_HEAL_SECS = 60.0
    COMP_COPY_CHANCE = 0.25
    # Seconds between saves of the pet. The shop is saved at least every SHOP_SAVE_MAX seconds even
    # when only passive squeaks changed.
    SAVE_EVERY = 30.0
    SHOP_SAVE_MAX = 3600.0
    PLAY_SECS = 6.0
    EAT_SECS = 2.5
    PET_COOLDOWN = 8.0
    BRUSH_COOLDOWN = 60.0
    GREMLIN_WALK = 7.0
    GREMLIN_GAP = 120.0
    GUARD_CHANCE = 0.35
    REMIND_EVERY = 900.0
    OFFLINE_MAX_H = 24
    NAME_MAX = 12
    PASSIVE_PER_H = 30.0
    # Squeaks paid for each kind of care. The passive trickle is separate (PASSIVE_PER_H).
    EARN = {"feed": 2, "treat": 2, "brush": 4, "play": 5, "clean": 3, "cure": 2, "pet": 1,
            "forage": 1, "swat": 5, "guard": 3, "trap": 10, "social": 1, "grow": 25}
    LUCK_BONUS = 1.25
    PEN_MAX = 6
    # The text before the 64-character code in chat. Never start a shared line with "[": the shard
    # reads that as a command.
    CODE_TAG = "Mongotchi code:"
    # Chat channels the code can be posted on: (label, name of the API method that sends it).
    CHANNELS = [("Say", "Msg"), ("Party", "PartyMsg"), ("Guild", "GuildMsg"),
                ("Alliance", "AllyMsg"), ("Whisper", "WhisperMsg")]
    LISTEN_EVERY = 2.0
    STATE_KEY = "Mongotchi_state"
    SHOP_KEY = "Mongotchi_shop"
    GUESTS_KEY = "Mongotchi_guests"
    QUEST_KEY = "Mongotchi_quests"
    SEASON_KEY = "Mongotchi_seasonal"
    ACH_KEY = "Mongotchi_achievements"
    # Saved window positions and their defaults, one per window, in the shared key-value store.
    POS_KEYS = {"main": "Mongotchi_pos", "shop": "Mongotchi_shop_pos",
                "pen": "Mongotchi_pen_pos", "quest": "Mongotchi_quest_pos", "ach": "Mongotchi_ach_pos"}
    POS_DEFAULTS = {"main": (200, 200), "shop": (510, 200), "pen": (200, 640), "quest": (510, 200), "ach": (540, 240)}
    WINDOWS = ("shop", "pen", "quest", "ach", "main")
    SUBS = {"shop": "Shop", "pen": "Playpen", "quest": "Journeys", "ach": "Achievements"}
    # Saved minimised state per window.
    MIN_KEYS = {"main": "Mongotchi_min", "shop": "Mongotchi_shop_min",
                "pen": "Mongotchi_pen_min", "quest": "Mongotchi_quest_min", "ach": "Mongotchi_ach_min"}
    # Main window size, then the minimised bar, shop window and playpen widths. Heights follow
    # from the rows.
    W, H = 300, 448
    TRAY_ICON = GFX_PUP
    MINI_W, MINI_H = 240, 46
    SW = 380
    SHOP_ROWS = 6
    PPW = 420
    JW = 480
    JROWS = 8
    # Seasons: (key, name, first day, last day) with days as (month, day), both included. A range
    # whose last day comes before its first runs over the New Year. Seasons may overlap.
    SEASONS = [("halloween", "Halloween", (10, 15), (11, 1)), ("winter", "Winter", (12, 1), (2, 29)),
               ("newyear", "New Year", (12, 31), (1, 2))]
    HALLOWEEN_NIGHT = (10, 31)
    HALLOWEEN_GREMLINS = 3.0
    SEASON_EVERY = 60.0
    SNOW_N = 14
    SNOW_SPEED = (12.0, 24.0)
    FIREWORK_EVERY = (2.5, 5.0)
    ACH_EVERY = 5.0
    SND_ACHIEVE = 0x1EA
    HUE_LOCKED = 1109
    ACH_W = 600
    ART_BACK = (4014, 4016, 4015)
    # Window layout, in pixels. These sections stack: pen, needs, actions. Shared margins come from
    # Kit so the windows match the other modules.
    M, GAP = Kit.MARGIN, Kit.GAP
    IW = W - 2 * M
    PX0, PY0, PW, PH = M, M + 30 + GAP, IW, 132
    SY, SH = PY0 + PH + GAP, 122
    AY, AH = SY + SH + GAP, 116
    PB_W, PB_H = 56, 48
    XMIN, XMAX = PX0 + 10, PX0 + PW - 10 - PB_W
    YMIN, YMAX = PY0 + 26, PY0 + PH - 4 - PB_H
    FLOOR_Y = PY0 + PH - 36
    GR_W, GR_H = 28 * GREM_PX, 31 * GREM_PX
    GR_Y = PY0 + PH - GR_H - 2
    GX_START, GX_PANTRY = PX0 + PW - GR_W - 4, PX0 + 60
    PANTRY_SHOW = 5
    BAR_W = 109
    # Playpen window geometry: the scene, the guest list and the paste-a-code strip.
    QX0, QY0, QW, QH = M, M + 30 + GAP, PPW - 2 * M, 180
    QXMIN, QXMAX = QX0 + 10, QX0 + QW - 10 - PB_W
    QYMIN, QYMAX = QY0 + 26, QY0 + QH - 18 - PB_H
    QGY, QGH = QY0 + QH + GAP, 84
    QAY, QAH = QGY + QGH + GAP, 40
    PPH = QAY + QAH + M
    # The four needs shown as bars: (pet key, caption).
    NEEDS = [("food", "Fullness"), ("joy", "Happiness"), ("energy", "Energy"), ("clean", "Cleanliness")]
    # Loyalty texts by mood threshold. The last entry catches any mood, so the lookup always ends.
    LOYALTY = [(95, "Wonderfully Happy"), (85, "Extremely Happy"), (75, "Very Happy"),
               (65, "Rather Happy"), (55, "Happy"), (45, "Content"), (35, "Unhappy"),
               (25, "Rather Unhappy"), (12, "Extremely Unhappy"), (-1, "Confused")]
    LINES = {"idle": ["*squeak*", "*flap flap*", "*chitters*", "Mong!", "*hangs around*",
                 "*squeak squeak*", "*sniffs the air*"],
        "hungry": ["*tummy rumbles*", "Food? FOOD?", "*eyes the pantry*"],
        "bored": ["*sighs*", "*yawns at you*", "Play?"], "dirty": ["*sniffs... ew*", "*holds its nose*"],
        "sick": ["*cough cough*", "*shivers*"], "happy": ["<3", "*happy squeak*", "*nuzzles you*"],}
    PEN_LINES = ["*boops %s*", "*tags %s!*", "*chases %s*", "*squeaks at %s*",
                 "*does a loop around %s*", "*shares a crumb with %s*", "*plays tag with %s*"]
    # Shop categories: (key, caption, equipment slot or None). Treats, upgrades and the ultimate are
    # used or owned rather than worn, so they have no slot.
    CATS = [(k, nm, None if k in ("treat", "upg", "ult") else k) for k, nm in (("treat", "Treats"), ("hat", "Hats"),
            ("neck", "Necklaces"), ("dye", "Dyes"), ("aura", "Auras"), ("toy", "Toys"), ("pers", "Personality"),
            ("decor", "Decor"), ("hang", "Hanging"), ("title", "Titles"), ("voice", "Voices"),
            ("ncol", "Name colours"), ("upg", "Upgrades"), ("ult", "Ultimate"))]
    # Slots that always hold something: their first item is free and is the default.
    DEFAULT_SLOTS = ("dye", "toy", "pers", "voice", "ncol")

    # Builds one shop item from its positional fields; extra keyword fields carry what it does.
    def I(*row, **kw):
        """Build one shop item from positional fields (id, category, name, price, graphic, hue,
        description) plus keyword fields for what the item does.
        """
        return dict(zip(("id", "cat", "name", "price", "gfx", "hue", "desc"), row), **kw)

    # The shop. Category order and item order within a category are part of the playpen code: new
    # items must go at the end of their category, never in the middle, or other players' codes
    # read back as the wrong item. Seasonal items are listed last so each is the last of its
    # category.
    ITEMS = [I("t_peach", "treat", "Sugared Peach", 15, 0x021B, 0, "+15 happy, +5 full", joy=15, food=5),
        I("t_muffin", "treat", "Muffin", 20, 0x09EA, 0, "+15 full, +10 happy", food=15, joy=10),
        I("t_cake", "treat", "Cake", 40, 0x09E9, 0, "+35 happy, +15 full, crumbs", joy=35, food=15, clean=-5),
        I("t_honey", "treat", "Jar of Honey", 30, 0x09EC, 0, "+25 energy, +10 happy", energy=25, joy=10),
        I("t_cheese", "treat", "Wheel of Cheese", 30, 0x097E, 0, "+40 full", food=40),
        I("t_sausage", "treat", "Sausage", 25, 0x09C0, 0, "+25 full, +10 happy", food=25, joy=10),
        I("t_ribs", "treat", "Cut of Ribs", 35, 0x09F2, 0, "+45 full, +5 happy", food=45, joy=5),
        I("t_melon", "treat", "Watermelon", 25, 0x0C5C, 0, "+20 full, +10 clean, +10 happy", food=20, clean=10, joy=10),
        I("t_carrot", "treat", "Carrot", 20, 0x0C77, 0, "Chases off the next gremlin", food=10, guard=True),
        I("t_pumpkin", "treat", "Pumpkin", 35, 0x0C6A, 0, "+20 happy, +20 full, spooky", joy=20, food=20, spooky=True),
        I("t_milk", "treat", "Pitcher of Milk", 25, 0x09F0, 0, "+10 happy, then bed", joy=10, energy=10, sleep=True),
        I("t_cider", "treat", "Jug of Cider", 30, 0x09C8, 0, "+20 happy, a bit dizzy", joy=20, dizzy=True),
        I("t_honeydew", "treat", "Honeydew Melon", 25, 0x0C74, 0, "+20 full, +15 happy", food=20, joy=15),
        I("t_stew", "treat", "Healing Stew", 45, 0x0970, 0, "Cures sickness, +20 full", food=20, cure=True),
        I("h_wizard", "hat", "Wizard's Hat", 120, 0x1718, 1156, "Kal Vas Flam!"),
        I("h_witch", "hat", "Witch's Hat", 130, 0x1716, 1, "For All Hallows' Eve"),
        I("h_jester", "hat", "Jester Hat", 90, 0x171C, 1157, "For the court fool"),
        I("h_tricorne", "hat", "Tricorne", 100, 0x171B, 1, "Arr, a pirate bat"),
        I("h_floppy", "hat", "Floppy Hat", 70, 0x1713, 1206, "Soft and pink"),
        I("h_straw", "hat", "Straw Hat", 60, 0x1717, 0, "Farm-fresh style"),
        I("h_feather", "hat", "Feathered Hat", 110, 0x171A, 1173, "Bard chic"),
        I("h_bonnet", "hat", "Bonnet", 70, 0x1719, 1201, "Sweet and proper"),
        I("h_skull", "hat", "Skullcap", 50, 0x1543, 1, "Rogue's choice"),
        I("h_bandana", "hat", "Bandana", 50, 0x153F, 33, "Brigand red"),
        I("h_tribal", "hat", "Tribal Mask", 140, 0x1549, 0, "Savage and proud"),
        I("h_circlet", "hat", "Royal Circlet", 220, 0x2B6F, 0, "Fit for Lord British's court"),
        I("h_gemcirc", "hat", "Gemmed Circlet", 260, 0x2B70, 0, "Sparkles in the moonlight"),
        I("h_jcap", "hat", "Jester's Cap", 90, 0x172E, 1172, "Bells not included"),
        I("h_cap", "hat", "Cap", 40, 0x1715, 1505, "Plain and orange"),
        I("h_widebrim", "hat", "Wide-Brim Hat", 100, 0x1714, 1177, "Golden and grand"),
        I("h_exec", "hat", "Executioner's Cap", 150, 0x0F83, 1, "Gremlins beware"),
        I("n_gold", "neck", "Gold Necklace", 80, 0x1088, 0, "Plain gold"),
        I("n_chain", "neck", "Gold Chain", 100, 0x1089, 0, "Bling, mongbat style"),
        I("n_silver", "neck", "Silver Chain", 90, 0x1F0A, 0, "Shiny and cool"),
        I("n_beads", "neck", "Beads", 60, 0x108B, 0, "Colourful beads"),
        I("n_jewel", "neck", "Jewelled Necklace", 160, 0x1085, 1177, "Glitters with gems"),
        I("n_leather", "neck", "Leather Gorget", 70, 0x13C7, 0, "Adventurer's guard"),
        I("n_plate", "neck", "Plate Gorget", 140, 0x1413, 0, "A tiny knight")]
    # Dyes are the adult art in a hue; the first is free (its natural colour).
    ITEMS += [I(i, "dye", nm, p, GFX_ADULT, h, d) for i, nm, p, h, d in (
        ("d_natural", "Natural", 0, 0, "Its own brown"), ("d_ice", "Ice Blue", 120, 1152, "Frosty"),
        ("d_gold", "Gold", 200, 1177, "Worth its weight"), ("d_teal", "Teal", 100, 1173, "Sea-glass green"),
        ("d_crimson", "Crimson", 120, 1157, "Blood-red"), ("d_purple", "Royal Purple", 140, 1158, "Regal"),
        ("d_verdigris", "Verdigris", 100, 2968, "Old bronze"), ("d_silver", "Silver", 160, 1150, "Gleaming"),
        ("d_sapphire", "Sapphire", 160, 1195, "Deep blue"), ("d_orchid", "Orchid", 120, 1168, "Pretty in purple"),
        ("d_violet", "Violet", 120, 1171, "Twilight"), ("d_shadow", "Shadow", 180, 1109, "Blends into the night"),
        ("d_rose", "Rose", 100, 1206, "Blushing"), ("d_midnight", "Midnight", 180, 1156, "Darkest blue"))]
    # Auras: seq is (first frame, frame count) of the client's effect art; without it the aura is a
    # still picture.
    ITEMS += [I("a_holy", "aura", "Holy Light", 250, 0x3740, 0, "Blue-white sparkles", seq=(0x373A, 16)),
        I("a_embers", "aura", "Embers", 250, 0x3750, 0, "Red sparks", seq=(0x374A, 16)),
        I("a_star", "aura", "Starlight", 300, 0x3760, 0, "Stars of blue and gold", seq=(0x375A, 16)),
        I("a_fairy", "aura", "Fairy Dust", 300, 0x3770, 0, "Twinkling motes", seq=(0x376A, 15)),
        I("a_snow", "aura", "Snowfall", 280, 0x3782, 1153, "Gentle snowflakes", seq=(0x377A, 15)),
        I("a_phoenix", "aura", "Phoenix Sparks", 350, 0x3740, 1161, "Golden fire", seq=(0x373A, 16)),
        I("a_toxic", "aura", "Toxic Glitter", 300, 0x3740, 1405, "Poisonously pretty", seq=(0x373A, 16)),
        I("a_bluegate", "aura", "Blue Moongate", 400, 0x0F6C, 0, "A halo of moonlight"),
        I("a_redgate", "aura", "Red Moongate", 400, 0x0DDA, 0, "A gate of crimson"),
        I("a_halo", "aura", "Golden Halo", 500, 0x0F6C, 1177, "Saintly"),
        I("a_void", "aura", "Void Gate", 450, 0x0F6C, 1158, "From beyond"),
        I("a_storm", "aura", "Lightning", 450, 0x3950, 0, "Crackling energy", seq=(0x3946, 31)),
        I("a_rainbow", "aura", "Rainbow", 600, 0x3740, 0, "Every colour at once", seq=(0x373A, 16), rainbow=True),
        I("y_yarn", "toy", "Ball of Yarn", 0, 0x0E1D, 0, "The classic", motion="bounce"),
        I("y_ball", "toy", "Bouncy Ball", 60, 0x0E73, 33, "Boing! +5 happy", motion="bouncy", joy=5),
        I("y_feather", "toy", "Feather", 50, 0x1BD1, 0, "Floats down; less tiring", motion="float", energy=5),
        I("y_rat", "toy", "Toy Rat", 90, 0x2123, 0, "+10 happy, tiring", motion="scurry", joy=10,
          energy=-5), I("y_dice", "toy", "Dice", 70, 0x0FA7, 0, "A gamble: 10-45 happy", motion="dice"),
        I("y_crystal", "toy", "Crystal Ball", 200, 0x0E2D, 0, "+5 squeaks a game", motion="hover", squeaks=5),
        I("y_drum", "toy", "Drum", 120, 0x0E9C, 0, "It dances along", motion="music", snd=0x038),
        I("y_tamb", "toy", "Tambourine", 100, 0x0E9D, 0, "Shake shake shake", motion="music", snd=0x052),
        I("y_lute", "toy", "Lute", 150, 0x0EB3, 0, "A bard's tune", motion="music", snd=0x04C),
        I("y_harp", "toy", "Lap Harp", 180, 0x0EB2, 0, "Soothing: +10 happy", motion="music", snd=0x045, joy=10),
        I("y_flute", "toy", "Bamboo Flute", 130, 0x2805, 0, "Toot toot", motion="music", snd=0x03D),
        I("p_cheerful", "pers", "Cheerful", 0, 0x0E3B, 0, "Sunny and easy-going"),
        I("p_playful", "pers", "Playful", 150, 0x0E3B, 1206, "Loves games; gets bored faster", play=1.5, joy_rate=1.2,
          speed=1.3, lines=["*does a loop-de-loop*", "Tag! You're it!", "*bounces off the walls*"]),
        I("p_lazy", "pers", "Lazy", 100, 0x0E3B, 1109, "Tires slowly, sleeps deeply, flies slow", energy_rate=0.6,
          sleep=1.25, speed=0.6, lines=["*yawns*", "*naps mid-flap*", "Five more minutes..."]),
        I("p_glutton", "pers", "Gluttonous", 120, 0x0E3B, 1505, "Always hungry; food cheers it", food_rate=1.3,
          feed_joy=15, lines=["Snack time?", "*drools*", "*sniffs for crumbs*"]),
        I("p_brave", "pers", "Brave", 200, 0x0E3B, 33, "Chases off gremlins more often", guard=0.75,
          lines=["*flexes*", "Gremlins fear me!", "*guards the pantry*"]),
        I("p_shy", "pers", "Shy", 120, 0x0E3B, 1152, "Quiet; loves being petted", pet=8, chat=0.4,
          lines=["*hides behind its wings*", "...squeak", "*peeks at you*"]),
        I("p_mischief", "pers", "Mischievous", 180, 0x0E3B, 1405, "More food; may steal some back from gremlins",
          forage=1, stealback=0.3, lines=["*snickers*", "*eyes the gremlins' stash*", "*hides a grape*"]),
        I("p_grumpy", "pers", "Grumpy", 100, 0x0E3B, 1157, "Hard to please, slow to sulk", joy_rate=0.85,
          lines=["*grumbles*", "Hmph.", "*glares at the gremlin hole*"]),
        I("p_scholar", "pers", "Scholarly", 250, 0x0E3B, 1156, "Earns 20% more squeaks", squeak=1.2,
          lines=["*reads a tiny spellbook*", "*mutters Kal Vas Flam*", "*adjusts its spectacles*"]),
        I("p_drama", "pers", "Dramatic", 120, 0x0E3B, 1158, "Everything is a tragedy (or triumph)", chat=1.6,
          lines=["*faints dramatically*", "Woe! WOE!", "*poses heroically*"]),
        I("o_pillow", "decor", "Straw Pillow", 120, 0x11EA, 0, "Sleeps 25% better", sleep=1.25),
        I("o_flowers", "decor", "Potted Flowers", 60, 0x11CA, 0, "A splash of colour"),
        I("o_fern", "decor", "Fern", 50, 0x0C9F, 0, "Leafy"),
        I("o_cactus", "decor", "Cactus", 50, 0x0D25, 0, "Don't hug it"),
        I("o_globe", "decor", "Globe", 90, 0x1047, 0, "Sosaria, in miniature"),
        I("o_mushroom", "decor", "Mushrooms", 40, 0x0D0C, 0, "Mysterious fungi"),
        I("o_pumpkin", "decor", "Pumpkin", 60, 0x0C6A, 0, "Happy Halloween"),
        I("o_crystal", "decor", "Crystal Ball", 150, 0x0E2D, 0, "It sees all"),
        I("o_wildflowers", "decor", "Wildflowers", 50, 0x0C83, 0, "Fresh from the meadow"),
        I("o_candles", "decor", "Candelabra", 100, 0x0B1D, 0, "Cosy candlelight"),
        I("g_lantern", "hang", "Lantern", 60, 0x0A15, 0, "A warm glow"),
        I("g_hanglamp", "hang", "Hanging Lantern", 80, 0x0A1A, 0, "Swings gently"),
        I("g_chimes", "hang", "Wind Chimes", 70, 0x2832, 0, "Tinkle tinkle"),
        I("g_fancy", "hang", "Fancy Wind Chimes", 110, 0x2833, 0, "Crystal clear"),
        I("x_brave", "title", "the Brave", 80, 0x0EF3, 0, "Fearless"),
        I("x_fluffy", "title", "the Fluffy", 60, 0x0EF3, 0, "So soft"),
        I("x_magnif", "title", "the Magnificent", 150, 0x0EF3, 0, "Behold!"),
        I("x_britain", "title", "of Britain", 100, 0x0EF3, 0, "A city bat"),
        I("x_belfry", "title", "of the Belfry", 120, 0x0EF3, 0, "Lord of the bell tower"),
        I("x_spooky", "title", "the Spooky", 90, 0x0EF3, 0, "Boo!"),
        I("x_bane", "title", "Gremlin Bane", 100, 0x0EF3, 0, "Needs 10 gremlins swatted", req="swats"),
        I("x_greater", "title", "the Greater", 100, 0x0EF3, 0, "Needs a Greater Mongotchi", req="greater"),
        I("x_elder", "title", "the Elder", 200, 0x0EF3, 0, "Needs an age of 24 hours", req="elder"),
        I("x_avatar", "title", "the Avatar", 1000, 0x0EF3, 1177, "Needs every virtue at level 5", req="avatar"),
        I("x_explorer", "title", "the Explorer", 150, 0x0EF3, 0, "Needs 8 different relics", req="relics"),
        I("x_pilgrim", "title", "the Pilgrim", 200, 0x0EF3, 0, "Needs a virtue at level 10", req="pilgrim")]
    # Voices: the sound its squeak makes.
    ITEMS += [I(i, "voice", nm, p, gfx, 0, d, snd=snd) for i, nm, p, gfx, d, snd in (
        ("v_mongbat", "Mongbat", 0, 0x20F9, "Its own squeak", 0x1A6), ("v_cat", "Cat", 60, 0x211B, "Meow?", 0x069),
        ("v_dog", "Dog", 60, 0x211C, "Woof!", 0x085), ("v_chicken", "Chicken", 50, 0x20D1, "Bawk!", 0x06E),
        ("v_bird", "Songbird", 60, 0x211A, "Tweet", 0x017), ("v_pig", "Pig", 50, 0x2101, "Oink", 0x0C4),
        ("v_cow", "Cow", 50, 0x2103, "Moo", 0x078), ("v_sheep", "Sheep", 50, 0x20E6, "Baa", 0x0D6),
        ("v_frog", "Bullfrog", 60, 0x2130, "Ribbit", 0x266), ("v_wisp", "Wisp", 120, 0x2100, "Ethereal chimes", 0x1D2),
        ("v_ghost", "Ghost", 100, 0x25C7, "Ooooo", 0x17E), ("v_dragon", "Dragon", 200, 0x20D6, "ROAR", 0x16A),
        ("v_daemon", "Daemon", 200, 0x2104, "From the abyss", 0x165),
        ("v_gazer", "Gazer", 120, 0x20F4, "Blorp", 0x179))]
    ITEMS += [I("c_gold", "ncol", "Gold", 0, 0, 53, "The usual"),
        I("c_white", "ncol", "White", 40, 0, 1153, "Clean and bright"),
        I("c_green", "ncol", "Green", 40, 0, 68, "Fresh"), I("c_red", "ncol", "Red", 40, 0, 33, "Fierce"),
        I("c_blue", "ncol", "Sky Blue", 50, 0, 1173, "Breezy"), I("c_pink", "ncol", "Pink", 50, 0, 1201, "Adorable"),
        I("c_fire", "ncol", "Fire", 80, 0, 1161, "Blazing"), I("c_ice", "ncol", "Ice", 80, 0, 1152, "Chilly"),
        I("u_pantry", "upg", "Bigger Pantry", 150, 0x0E77, 0, "Holds %d food" % PANTRY_BIG),
        I("u_trap", "upg", "Gremlin Trap", 40, 0x10F7, 0, "Catches the next gremlin (+10 sq)", uses=True),
        I("u_luck", "upg", "Lucky Black Pearl", 250, 0x0F7A, 0, "+25% squeaks, forever"),
        I("u_groom", "upg", "Grooming Kit", 100, 0x1373, 0, "Brushing does double"),
        I("u_feeder", "upg", "Auto-Feeder", 200, 0x0E7F, 0, "Feeds it from the pantry when hungry"),
        I("u_ward", "upg", "Scarecrow", 300, 0x1E34, 0, "Half as many gremlins"),
        I("u_companion", "ult", "Companion Charm", 2500, 0x0E5C, 1161,
          "Follows you in the world and joins fights", toggle=True),
        I("u_war", "ult", "War Training", 800, 0x1F4C, 33, "Dives at foes twice as often, with fireballs", req="charm"),
        I("u_shiny", "ult", "Shiny Sense", 600, 0x0EED, 0, "Finds shiny things twice as often on walks", req="charm"),
        # Seasonal items, on sale only in their season and kept all year once bought.
        I("h_orcmask", "hat", "Orc Mask", 90, 0x141B, 0, "An orc costume", season="halloween"),
        I("h_bearmask", "hat", "Bear Mask", 100, 0x1545, 0, "A bear costume: rawr!", season="halloween"),
        I("h_deermask", "hat", "Deer Mask", 100, 0x1547, 0, "Antlers and all", season="halloween"),
        I("d_ghost", "dye", "Ghost Costume", 150, GFX_ADULT, 1153, "A sheet with eye holes", season="halloween"),
        I("d_pumpkin", "dye", "Pumpkin Costume", 150, GFX_ADULT, 1505,
          "Round, orange and grinning", season="halloween"),
        I("t_pie", "treat", "Pumpkin Pie", 35, 0x1041, 0, "+25 full, +15 happy, spooky", food=25,
          joy=15, spooky=True, season="halloween"),
        I("t_pbread", "treat", "Pumpkin Bread", 30, 0x103B, 1505, "+25 full, +10 happy", food=25,
          joy=10, season="halloween"), I("h_wintercap", "hat", "Winter Cap", 70, 0x1715, 1153, "Warm and woolly",
          season="winter"), I("h_holiday", "hat", "Holiday Hat", 110, 0x1718, 33, "Red, pointy and festive",
          season="winter"), I("h_snowbonnet", "hat", "Snow Bonnet", 80, 0x1719, 1152, "Frosted lace", season="winter"),
        I("o_snowman", "decor", "Snowman", 100, 0x2328, 0, "Carrot nose included", season="winter"),
        I("o_gifts", "decor", "Gift Box", 80, 0x232A, 0, "No peeking!", season="winter"),
        I("g_mistletoe", "hang", "Mistletoe", 70, 0x2374, 0, "Who's under it?", season="winter"),
        I("g_wreath", "hang", "Holly Wreath", 90, 0x232C, 0, "Evergreen and berries", season="winter"),
        I("t_ginger", "treat", "Gingerbread Man", 25, 0x2BE1, 0, "+20 happy, +10 full", joy=20,
          food=10, season="winter"), I("t_cane", "treat", "Candy Cane", 25, 0x2BDD, 0, "+25 energy, +5 happy",
          energy=25, joy=5, season="winter"),
        I("h_partycap", "hat", "Party Cap", 90, 0x172E, 1177, "Ring in the new year", season="newyear"),
        I("a_fireworks", "aura", "Fireworks", 400, 0x3760, 0, "Bursts of every colour",
          seq=(0x375A, 16), rainbow=True, season="newyear"),
        I("t_fizz", "treat", "Sparkling Cider", 30, 0x1F7D, 0, "+20 happy, +10 energy, fizzy",
          joy=20, energy=10, dizzy=True, season="newyear"),
        I("x_festive", "title", "the Festive", 120, 0x0EF3, 0, "Toasts the new year", season="newyear"),]
    # Lookup tables built once from the item list.
    BY_ID = dict((it["id"], it) for it in ITEMS)
    BY_CAT = {}
    for _it in ITEMS:
        BY_CAT.setdefault(_it["cat"], []).append(_it)
    FREE = set(it["id"] for it in ITEMS if it["price"] == 0)
    # Seasonal items are saved under their own key, never in the shop key, so that a build which
    # drops ids it does not know cannot lose them.
    SEASON_NAME = dict((s[0], s[1]) for s in SEASONS)
    SEASONAL = [it for it in ITEMS if it.get("season")]
    SEASON_IDS = frozenset(it["id"] for it in SEASONAL)
    SEASON_CAT = ("season", "Seasonal", None)
    # The eleven worn slots, in the order the playpen code stores them.
    CODE_SLOTS = ("dye", "hat", "neck", "aura", "pers", "toy", "title", "voice", "ncol", "decor", "hang")
    # Hues the rainbow items and rainbow sparkles cycle through.
    RAINBOW = [1157, 1505, 1177, 1405, 1173, 1156, 1158, 1206]

    def vpct(k):
        """A VIRTUE_FX share as whole percent per level."""
        return int(round(VIRTUE_FX[k] * 100))

    # Virtues: (key, name, shrine's place, what a level does, number). The effect text is shown on
    # the Meditation tab with the level times the number filled in; a negative number divides
    # instead. Levels run 0 to VIRTUE_MAX and the experience a level needs grows with the level.
    VIRTUES = [("hon", "Honesty", "Dagger Isle", "Shop prices %d%% lower", vpct("hon_price")),
        ("com", "Compassion", "the Britain road", "Petting +%d happy; heals you sooner",
         int(VIRTUE_FX["com_pet"])), ("val", "Valor", "the isle south of Jhelom",
         "Guards the pantry +%d%%; hunts safer; dives sooner", vpct("val_guard")),
        ("jus", "Justice", "the Yew woods", "Wins back %d%% of stolen food", vpct("jus_back")),
        ("sac", "Sacrifice", "the Minoc desert", "Brings +%d food home; trips cost less energy", -VIRTUE_FX["sac_per"]),
        ("hnr", "Honor", "the Trinsic road", "%d%% more squeaks from everything", vpct("hnr_squeaks")),
        ("spi", "Spirituality", "the Skara Brae road",
         "Meditation +%d%%; relic luck up; sickness down", vpct("spi_meditate")),
        ("hum", "Humility", "the isle off Magincia", "Hunger %d%% slower; needs sting less", vpct("hum_hunger")),]
    VIRTUE_KEYS = [v[0] for v in VIRTUES]
    VIRTUE_BY_KEY = dict((v[0], v) for v in VIRTUES)
    # What a pet strong in a virtue says (level 5 and up).
    VIRTUE_LINES = {"hon": ["*looks you straight in the eye*", "*would never fib*"],
        "com": ["*nuzzles you gently*", "*checks that you're all right*"],
        "val": ["*puffs up bravely*", "*guards the pen*"],
        "jus": ["*weighs the crumbs fairly*", "*glares at the gremlin hole*"],
        "sac": ["*offers you a crumb*", "*saves the last bite for you*"],
        "hnr": ["*bows with dignity*", "*keeps its word*"], "spi": ["*hums an old hymn*", "*meditates on its perch*"],
        "hum": ["*bows its little head*", "*is content with a crumb*"],}
    # Relics: (id, name, graphic, hue). Two per hunting place, found nowhere else.
    RELICS = [("r_horseshoe", "a lucky horseshoe", 0x0FB6, 0), ("r_goldegg", "a golden egg", 0x09B5, 1177),
        ("r_mandrake", "a fat mandrake root", 0x0F86, 0), ("r_glowshroom", "a glowing mushroom", 0x0D0C, 1173),
        ("r_ore", "a shiny ore nugget", 0x19B9, 1150), ("r_goldingot", "a gold ingot", 0x1BF2, 1177),
        ("r_conch", "a conch shell", 0x0FC4, 0), ("r_blackpearl", "a perfect black pearl", 0x0F7A, 0),
        ("r_fang", "a silver serpent fang", 0x0F7E, 1150), ("r_eye", "a serpent's eye emerald", 0x0F10, 0),
        ("r_obsidian", "a shard of obsidian", 0x0F89, 0), ("r_phoenix", "a phoenix feather", 0x1BD1, 1161),
        ("r_scale", "a dragon scale", 0x26B4, 0), ("r_dblood", "a vial of dragon's blood", 0x0F82, 0),
        ("r_scroll", "a scroll of ancient lore", 0x0E35, 0), ("r_sextant", "a cracked sextant", 0x1057, 0),]
    RELIC_BY_ID = dict((r[0], r) for r in RELICS)

    # Builds one hunting place from its fields.
    def L(*row):
        """Build one hunting place from positional fields (id, name, minutes, danger, requirement, failure
        text, hint, loot table).
        """
        return dict(zip(("id", "name", "mins", "danger", "req", "bad", "hint", "loot"), row))

    # Places: id, name, minutes away, danger (chance the trip goes wrong, before Valor), requirement
    # (None, ("stage", n) or ("virtue", key, level)), what going wrong looks like, a short hint, and
    # the finds there as (weight, kind, a, b): "sq" squeaks (low, high), "food" pantry food (low,
    # high), "treat" (id), "trap" a Gremlin Trap, "relic" (id).
    LOCATIONS = [L("farm", "The Britain Farmlands", 8, 0.05, None, "an angry farmer's dog chased it off",
          "apples, carrots, a few squeaks", [(5, "sq", 4, 10), (5, "food", 1, 2), (2, "treat", "t_peach", 0),
           (2, "treat", "t_carrot", 0), (1, "treat", "t_milk", 0), (1.2, "relic", "r_horseshoe", 0),
           (0.4, "relic", "r_goldegg", 0)]), L("yew", "The Spiritwood, Yew", 12, 0.10, None,
          "it got lost among the trees", "honey, mushrooms, roots",
          [(5, "sq", 6, 14), (3, "food", 1, 2), (2, "treat", "t_honey", 0),
           (1, "treat", "t_honeydew", 0), (1.2, "relic", "r_mandrake", 0), (0.4, "relic", "r_glowshroom", 0)]),
        L("minoc", "The Minoc Mines", 15, 0.15, ("stage", 1), "a rockfall nearly caught it",
          "squeaks, ore, the odd gold ingot",
          [(6, "sq", 10, 25), (1, "food", 1, 1), (1, "trap", 0, 0), (1, "treat", "t_cheese", 0),
           (1.2, "relic", "r_ore", 0), (0.4, "relic", "r_goldingot", 0)]),
        L("ship", "The Sunken Ship, off Ocllo", 18, 0.20, ("stage", 1), "a sea serpent surfaced beside it",
          "fish, shells, pearls", [(4, "sq", 8, 20), (4, "food", 1, 3), (1, "treat", "t_melon", 0),
           (1, "treat", "t_ribs", 0), (1.2, "relic", "r_conch", 0), (0.4, "relic", "r_blackpearl", 0)]),
        L("terra", "Terra Sanctum", 22, 0.30, ("virtue", "val", 2), "a silver serpent bit it",
          "silver serpent fangs, silk, squeaks",
          [(5, "sq", 10, 24), (1, "food", 1, 2), (1, "trap", 0, 0), (1, "treat", "t_stew", 0),
           (1.5, "relic", "r_fang", 0), (0.4, "relic", "r_eye", 0)]),
        L("volcano", "The Volcano, Hythloth Island", 28, 0.40, ("virtue", "val", 4), "it singed its wings on the lava",
          "obsidian, sulphurous ash, phoenix feathers",
          [(5, "sq", 12, 30), (1, "trap", 0, 0), (1, "treat", "t_pumpkin", 0),
           (1, "treat", "t_cider", 0), (1.5, "relic", "r_obsidian", 0), (0.4, "relic", "r_phoenix", 0)]),
        L("destard", "Destard", 35, 0.50, ("virtue", "val", 6), "a dragon woke up", "dragon scales and hoard gold",
          [(5, "sq", 20, 45), (1, "treat", "t_cake", 0), (1, "treat", "t_sausage", 0),
           (1, "trap", 0, 0), (1.5, "relic", "r_scale", 0), (0.5, "relic", "r_dblood", 0)]),
        L("lycaeum", "The Lycaeum, Moonglow", 15, 0.05, ("virtue", "spi", 2), "a librarian shooed it out",
          "scrolls, squeaks, odd instruments", [(6, "sq", 10, 22), (1, "food", 1, 1), (1, "treat", "t_muffin", 0),
           (1.2, "relic", "r_scroll", 0), (0.4, "relic", "r_sextant", 0)]),]
    LOC_BY_ID = dict((l["id"], l) for l in LOCATIONS)
    JOURNEY_TABS = ["Treasure hunts", "Meditation", "Relics"]
    SND_MEDITATE = 0x1F6
    # Achievements: (id, name, what to do, squeak reward, picture, hue, what counts, goal). Each is
    # earned once per character. "What counts" is read from the game state as it is, so milestones
    # reached earlier are granted the first time the module runs; None means it is granted where it
    # happens. The ids are saved: never rename one, and add new ones at the end.
    ACHIEVEMENTS = [("grown", "All grown up", "Raise a pup to adulthood", 10, GFX_ADULT, 0, "stage", 1),
        ("greater", "Well raised", "Raise a Greater Mongotchi", 40, GFX_ADULT, HUE_GREATER, "stage", 2),
        ("elder", "Elder", "A mongotchi 24 hours old", 30, 0x1810, 0, "age", 24),
        ("swat1", "Swat!", "Swat a gremlin", 5, 0x1043, 0, "swats", 1),
        ("swat25", "Gremlin bane", "Swat 25 gremlins", 30, 0x0F83, 1, "swats", 25),
        ("trap", "Snap!", "Catch a gremlin in a trap", 10, 0x10F7, 0, None, 1),
        ("sq1k", "A thousand squeaks", "Earn 1,000 squeaks", 25, 0x0EED, 0, "earned", 1000),
        ("sq10k", "Squeak hoard", "Earn 10,000 squeaks", 100, 0x0EEF, 0, "earned", 10000),
        ("relic1", "First relic", "Find a relic on a hunt", 15, 0x0FB6, 0, "relics", 1),
        ("relics", "Curator", "Find all %d relics" % len(RELICS), 100, 0x09B5, 1177, "relics", len(RELICS)),
        ("places", "Seasoned traveller", "Hunt at all %d places" % len(LOCATIONS), 40, 0x14EB, 0,
         "places", len(LOCATIONS)),
        ("shrines", "Pilgrimage", "Meditate at all %d shrines" % len(VIRTUES), 40, 0x0A28, 0, "shrines", len(VIRTUES)),
        ("avatar", "Avatar", "Every virtue at level 5", 100, 0x2B6F, 1177, "virtue5", len(VIRTUES)),
        ("friend", "Playdate", "A friend's mongotchi visits", 10, 0x0E1D, 0, "guests", 1),
        ("charm", "Best friends", "Buy the Companion Charm", 50, 0x0E5C, 1161, "charm", 1),
        ("festive", "Festive", "Give a treat in its season", 20, 0x0C6A, 0, None, 1),]
    ACH_BY_ID = dict((a[0], a) for a in ACHIEVEMENTS)
    ACH_ROWS = 8
    # Most achievement ids kept from a save; newer builds' ids are kept too.
    ACH_KEEP_MAX = 200
    # Settings saved per character. share_open posts the code when the Playpen is opened (only while
    # share_min is above 0); it sits last so older saves keep sharing.
    settings = {"name": "Flapjack", "pace": 100, "grem_min": 20, "share_min": 10,
               "gremlins": True, "sounds": True, "remind": True, "offline": False,
               "listen": True, "share_ch": 0, "comp": False, "comp_talk": True, "comp_help": True, "share_open": True}
    DEFAULTS = dict(settings)
    # Allowed range of each numeric setting.
    LIMITS = {"pace": (25, 400), "grem_min": (5, 240), "share_min": (0, 60), "share_ch": (0, len(CHANNELS) - 1)}
    # A new pet's state. away_kind is 0 forage, 1 treasure hunt (away_loc) or 2 meditation
    # (away_virt), and away_total is how long the whole trip takes. These keys are the saved state.
    PET_NEW = {"food": 80.0, "joy": 80.0, "energy": 90.0, "clean": 100.0, "sick": False, "sick_t": 0.0, "asleep": False,
               "age": 0.0, "care_sum": 0.0, "care_t": 0.0, "stage": 0, "pantry": PANTRY_START, "messes": 0,
               "neglect": 0.0, "warned": False, "feral": False, "mess_in": 40 * 60.0, "supply_in": SUPPLY_MIN * 60.0,
               "away": False, "away_left": 0.0, "fed": 0, "swats": 0, "stolen": 0, "uid": 0, "guard": False,
               "last": 0.0, "away_kind": 0, "away_loc": 0, "away_virt": 0, "away_total": 0.0}
    # The live state: pet, worn and owned items, virtues and relics, and achievements. In the
    # achievements record, "new" means nothing was saved yet (its first run).
    pet = dict(PET_NEW)
    SLOTS = ["hat", "neck", "dye", "aura", "toy", "pers", "decor", "hang", "title", "voice", "ncol"]
    shop = {"sq": 0.0, "own": set(), "cnt": {}, "eq": {}, "last": 0.0}
    quest = {"xp": dict((k, 0.0) for k in VIRTUE_KEYS), "relics": {}, "visits": {}, "hunts": 0, "med": 0, "tab": 0}
    ach = {"got": set(), "earned": 0.0, "swats": 0, "new": False}
    # Session state of the module: window flags, animation tables, timers. Never saved as a whole.
    st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "last_t": 0.0, "sim_acc": 0.0,
          "saved_at": 0.0, "say": "", "say_until": 0.0, "pet_cd": 0.0, "brush_cd": 0.0, "remind": {}, "confirm": 0.0,
          "px": float(PX0 + PW // 2 - PB_W // 2), "py": float(YMIN + 10), "tx": 0.0, "ty": 0.0, "hover_until": 0.0,
          "eat_food": None, "eat_x": 0, "play_toy": None, "toy": [0.0, 0.0, 0.0, 0.0], "music_at": 0.0,
          "away_until": 0.0, "dizzy_until": 0.0, "shop_min": Kit.load_min(MIN_KEYS["shop"]), "shop_cat": 0,
          "shop_page": 0, "pen_open": False, "pen_min": Kit.load_min(MIN_KEYS["pen"]), "guests": [], "pals": {},
          "quest_min": Kit.load_min(MIN_KEYS["quest"]), "ach_min": Kit.load_min(MIN_KEYS["ach"]), "ach_saved": None,
          "hallow_night": False, "season_saved": None, "season_told": set(), "hallow_told": None, "snow": [],
          "shared_at": 0.0, "social_at": 0.0, "anims": {}, "snd_later": [], "parts": {"main": [], "pen": []},
          "sprites": {"main": [], "pen": []}, "bar_w": {}, "carry": None, "shop_dirty": False, "quest_dirty": False}
    # The main window record (the other windows get the same shape in WINDOWS later on).
    win = {"g": None, "c": {}, "store": ({}, {}), "v": None}
    # Kit.basics gives the three helpers every module needs: cleanup, queue and say.
    cleanup, queue, say = Kit.basics(st, TITLE)

    class View(object):
        """Remembers what each control shows and touches it only when that changes.

        Everything that draws (the tick, window builds, start) runs inside the client's frame, so a
        change is applied right here with no closure and no queue. Entries are keyed by id(control)
        and go away with the window's View. Pieces of the pen are drawn through a transform so the pen
        can be scaled inside a zone.
        """
        # Slots keep each View small and attribute access quick.
        __slots__ = ("cache", "pen", "xf", "made")

        def __init__(self):
            """Sets up the empty cache, the set of pen pieces, no transform and no piece list."""
            # id(control) -> its last shown values (visibility, graphic, hue, position and so on).
            self.cache = {}
            # Ids of the pen's pieces: only these are drawn through the transform.
            self.pen = set()
            # (pen x, pen y, origin x, origin y, scale), or None when the pen is drawn unscaled.
            self.xf = None
            # While the pen is built, a list that each piece made is added to.
            self.made = None

        def reg(self, ctrl, **kw):
            """Remember a new control's cache entry and, while the pen is being built, keep the control."""
            self.cache[id(ctrl)] = kw
            if self.made is not None:
                self.made.append(ctrl)

        def tr(self, x, y):
            """Where the window draws a point of the pen's scene, given in the scene's own pixels."""
            xf = self.xf
            return xf[2] + (x - xf[0]) * xf[4], xf[3] + (y - xf[1]) * xf[4]

        def _e(self, ctrl):
            """The cache entry of a control, made on first use."""
            k = id(ctrl)
            e = self.cache.get(k)
            if e is None:
                e = self.cache[k] = {}
            return e

        def _chg(self, ctrl, key, v):
            """Record a new value for a key and say whether it differs from the last one shown."""
            if ctrl is None:
                return False
            e = self._e(ctrl)
            if e.get(key) == v:
                return False
            e[key] = v
            return True

        def show(self, ctrl, on):
            """Show or hide a control, only when that changed."""
            if self._chg(ctrl, "vis", on):
                Kit.set(ctrl, "IsVisible", on)

        def look(self, ctrl, gfx, hue):
            """Set a picture's graphic and hue, each only when it changed."""
            if self._chg(ctrl, "gfx", gfx):
                Kit.set(ctrl, "Graphic", gfx)
            if self._chg(ctrl, "hue", hue):
                Kit.set(ctrl, "Hue", hue)

        def move(self, ctrl, x, y):
            """Move a control to scene or window coordinates, only when it moved."""
            if ctrl is None:
                return
            # Whole pixels only, so tiny float jitter does not count as a move.
            xi, yi = int(x), int(y)
            if not self._chg(ctrl, "pos", (xi, yi)):
                return
            try:
                xf = self.xf
                # Pen pieces go through the transform; everything else uses the window's own placement.
                if xf is not None and id(ctrl) in self.pen:
                    ctrl.SetPos(int(round(xf[2] + (xi - xf[0]) * xf[4])), int(round(xf[3] + (yi - xf[1]) * xf[4])))
                else:
                    Kit.ui_pos(ctrl, xi, yi)
            except Exception:
                pass

        def size(self, ctrl, w, h):
            """Resize a control, only when the size changed; pen pieces are scaled."""
            if ctrl is None:
                return
            wi, hi = int(w), int(h)
            if not self._chg(ctrl, "size", (wi, hi)):
                return
            try:
                if self.xf is not None and id(ctrl) in self.pen:
                    # Never below one pixel, or the client drops the control.
                    sc = self.xf[4]
                    ctrl.SetWidth(max(1, int(round(wi * sc))))
                    ctrl.SetHeight(max(1, int(round(hi * sc))))
                else:
                    Kit.ui_size(ctrl, wi, hi)
            except Exception:
                pass

        def alpha(self, ctrl, a):
            """Set a control's transparency, only when it changed (rounded to two places)."""
            if ctrl is None:
                return
            a = round(a, 2)
            if self._chg(ctrl, "alpha", a):
                try:
                    ctrl.SetAlpha(a)
                except Exception:
                    pass

        def width(self, ctrl, w):
            """Set a bar's width, only when it changed."""
            if self._chg(ctrl, "w", w):
                try:
                    Kit.ui_w(ctrl, max(0, w))
                except Exception:
                    pass

        def text(self, lbl, text, hue=None):
            """Set a label's text and optionally its hue, only when either changed."""
            if lbl is None:
                return
            e = self._e(lbl)
            if e.get("text") != text or (hue is not None and e.get("thue") != hue):
                e["text"] = text
                if hue is not None:
                    e["thue"] = hue
                Kit.set_text(lbl, text, hue)

    def clean_name(s, maxlen=NAME_MAX):
        """Make a pet name safe to store and share: printable ASCII only, none of the separator
        characters used by the saved formats, cut to maxlen, with the default name when nothing is left.
        """
        # The characters ; = | , would break the key-value formats and the playpen code.
        s = "".join(ch for ch in str(s or "") if 32 <= ord(ch) < 127 and ch not in ";=|,").strip()
        return s[:maxlen] or DEFAULTS["name"]

    def pairs(v):
        """Split a saved "a:1,b:2" string into [key, value] pairs, skipping parts without a colon."""
        return [p.split(":", 1) for p in v.split(",") if ":" in p]

    def load_settings():
        """Load the settings from the character's saved values, then tidy the name."""
        Kit.kv_load(SETTINGS_KEY, ";", settings, LIMITS, ("name",))
        settings["name"] = clean_name(settings["name"])

    def save_settings():
        """Save every setting as one key-value string, in the order of the defaults."""
        Kit.kv_save(SETTINGS_KEY, ";", settings, DEFAULTS, LIMITS, ("name",))

    def set_comp(on):
        """Set the "Follows me in the world" option from outside the settings page, save it and redraw
        the page so its tick box does not read the old value straight back.
        """
        settings["comp"] = bool(on)
        save_settings()
        HOST.refresh_settings(KEY)

    def load_pet():
        """Load the pet from its saved state; return False when nothing was saved.

        Unknown keys are ignored and each value is read as the type of its default.
        Runs once at start.
        """
        raw = Kit.get_var(STATE_KEY)
        if "=" not in raw:
            return False
        pet.update(PET_NEW)
        for k, v in Kit.codec_load(raw).items():
            if k not in PET_NEW:
                continue
            d = PET_NEW[k]
            try:
                if isinstance(d, bool):
                    pet[k] = v == "1"
                elif isinstance(d, int):
                    pet[k] = int(float(v))
                else:
                    pet[k] = float(v)
            except ValueError:
                pass
        # A pet saved without an id gets a random one; the playpen uses it to tell pets apart.
        if not pet["uid"]:
            pet["uid"] = random.randint(1, 65535)
        return True

    def save_pet(final=False):
        """Save the pet, and the shop and quest strings when they changed since their last save.

        final=True saves everything (at stop). Passive squeaks alone do not count as a change: they
        are earned again from the shop's saved time at the next start, so the shop is written for
        them at most every SHOP_SAVE_MAX seconds.
        """
        now = time.time()
        pet["last"] = now
        if pet["away"]:
            left = max(0.0, st["away_until"] - now)
            # The clock went back: never keep a trip longer than it was.
            if pet["away_total"] > 0 and left > pet["away_total"]:
                left = pet["away_total"]
                st["away_until"] = now + left
            pet["away_left"] = left
        Kit.put_var(STATE_KEY, ";".join("%s=%s" % (k, ("1" if pet[k] else "0") if isinstance(d, bool) else
                                                   "%d" % int(pet[k]) if isinstance(d, int) else "%.2f" % float(pet[k]))
                                        for k, d in PET_NEW.items()))
        if final or st["shop_dirty"] or now - shop["last"] >= SHOP_SAVE_MAX:
            save_shop()
        if final or st["quest_dirty"]:
            save_quest()
        st["saved_at"] = now

    def load_shop():
        """Load squeaks, owned items, treat counts and worn items from the saved shop string."""
        shop.update({"sq": 0.0, "own": set(), "cnt": {}, "eq": {}, "last": 0.0})
        for k, v in Kit.codec_load(Kit.get_var(SHOP_KEY)).items():
            try:
                if k == "sq":
                    shop["sq"] = max(0.0, float(v))
                elif k == "last":
                    shop["last"] = float(v)
                elif k == "own":
                    shop["own"] = set(i for i in v.split(",") if i in BY_ID)
                elif k == "cnt":
                    for i, n in pairs(v):
                        if i in BY_ID and int(n) > 0:
                            shop["cnt"][i] = int(n)
                elif k == "eq":
                    for s, i in pairs(v):
                        if s in SLOTS and (i in BY_ID or i == ""):
                            shop["eq"][s] = i
            except ValueError:
                pass
        # The free items are always owned and the default slots never empty, whatever was saved.
        shop["own"] |= FREE
        for s in DEFAULT_SLOTS:
            if not shop["eq"].get(s):
                shop["eq"][s] = default_item(s)
        load_seasonal()

    def load_seasonal():
        """Add the seasonal items from their own saved key to the shop.

        A seasonal item that was worn is put back on only if the slot still holds what save_shop wrote
        in its place, in case an older build changed it.
        """
        raw = Kit.get_var(SEASON_KEY)
        st["season_saved"] = raw
        for k, v in Kit.codec_load(raw).items():
            if k == "own":
                shop["own"] |= set(p for p in v.split(",") if p in SEASON_IDS and not stackable(BY_ID[p]))
            for a, b in pairs(v):
                if k == "cnt" and a in SEASON_IDS and stackable(BY_ID[a]):
                    if safe(lambda: int(b), 0) > 0:
                        shop["cnt"][a] = int(b)
                elif k == "eq" and b in SEASON_IDS and CAT_SLOT.get(BY_ID[b]["cat"]) == a \
                        and (shop["eq"].get(a) or "") == default_item(a):
                    shop["eq"][a] = b

    def save_shop():
        """Write the shop in its older format (seasonal items left out, a worn one leaves the slot's
        default there), the seasonal items under their own key, and the achievements with it.
        """
        shop["last"] = time.time()
        st["shop_dirty"] = False
        S = SEASON_IDS
        eq_old = ["%s:%s" % (s, default_item(s) if i in S else i) for s, i in sorted(shop["eq"].items())]
        eq_new = ["%s:%s" % (s, i) for s, i in sorted(shop["eq"].items()) if i in S]
        cnt = sorted((i, n) for i, n in shop["cnt"].items() if n > 0)
        Kit.put_var(SHOP_KEY, ";".join(["sq=%.2f" % shop["sq"], "last=%.0f" % shop["last"],
            "own=" + ",".join(sorted(i for i in shop["own"] - FREE if i not in S)),
            "cnt=" + ",".join("%s:%d" % (i, n) for i, n in cnt if i not in S), "eq=" + ",".join(eq_old)]))
        own_new = sorted(i for i in shop["own"] if i in S)
        cnt_new = ["%s:%d" % (i, n) for i, n in cnt if i in S]
        raw = ";".join(["own=" + ",".join(own_new), "cnt=" + ",".join(cnt_new),
                        "eq=" + ",".join(eq_new)]) if own_new or cnt_new or eq_new else ""
        # The seasonal key is written only when its text changed.
        if raw != st["season_saved"]:
            st["season_saved"] = raw
            Kit.put_var(SEASON_KEY, raw)
        save_ach()

    def load_ach():
        """Load the achievements. The squeaks earned in all can never be below the squeaks held plus
        what the wardrobe cost at the lowest price, which covers older saves and time spent on an
        older build.

        Needs the shop and quests loaded, and runs before catch_up adds the squeaks of the time away.
        """
        raw = Kit.get_var(ACH_KEY)
        st["ach_saved"] = raw
        ach.update({"got": set(), "earned": 0.0, "swats": 0, "new": "=" not in raw})
        for k, v in Kit.codec_load(raw).items():
            try:
                if k == "got":
                    # Ids this build does not know are kept (a newer build's).
                    ach["got"] = set(sorted(i for i in v.split(",") if i)[:ACH_KEEP_MAX])
                elif k == "earned":
                    ach["earned"] = max(0.0, float(v))
                elif k == "swats":
                    ach["swats"] = max(0, int(float(v)))
            except ValueError:
                pass
        disc = 1.0 - VIRTUE_FX["hon_price"] * vlevel("hon")
        floor = shop["sq"] + sum(int(round(it["price"] * disc)) for it in ITEMS
                                 if it["price"] and not stackable(it) and it["id"] in shop["own"])
        ach["earned"] = max(ach["earned"], floor)

    def save_ach():
        """Write the achievements. Called only with save_shop, so the earned total always matches the
        shop's saved time, from which a restart earns the passive squeaks again.
        """
        raw = "got=%s;earned=%.2f;swats=%d" % (",".join(sorted(ach["got"])), ach["earned"], ach["swats"])
        if raw != st["ach_saved"]:
            st["ach_saved"] = raw
            Kit.put_var(ACH_KEY, raw)

    def load_guests():
        """Load the guests from their saved codes, dropping bad ones; at most PEN_MAX minus yours."""
        st["guests"] = []
        for code in Kit.get_var(GUESTS_KEY).split(","):
            g = decode(code.strip())
            if g is not None and len(st["guests"]) < PEN_MAX - 1:
                st["guests"].append(g)

    def save_guests():
        """Save the guests as a comma separated list of their codes."""
        Kit.put_var(GUESTS_KEY, ",".join(g["code"] for g in st["guests"]))

    def load_quest():
        """Load virtue experience, relics found, places visited and the open tab, keeping only known ids."""
        quest.update({"xp": dict((k, 0.0) for k in VIRTUE_KEYS), "relics": {}, "visits": {},
                      "hunts": 0, "med": 0, "tab": 0})
        for k, v in Kit.codec_load(Kit.get_var(QUEST_KEY)).items():
            try:
                if k == "xp":
                    for vk, n in pairs(v):
                        if vk in quest["xp"]:
                            quest["xp"][vk] = max(0.0, min(float(n), vxp_need(VIRTUE_MAX)))
                elif k in ("relics", "visits"):
                    known = RELIC_BY_ID if k == "relics" else LOC_BY_ID
                    for i, n in pairs(v):
                        if i in known and int(n) > 0:
                            quest[k][i] = int(n)
                elif k in ("hunts", "med"):
                    quest[k] = max(0, int(float(v)))
                elif k == "tab":
                    quest["tab"] = max(0, min(len(JOURNEY_TABS) - 1, int(v)))
            except ValueError:
                pass

    def save_quest():
        """Save the quest state as one string."""
        st["quest_dirty"] = False
        Kit.put_var(QUEST_KEY, ";".join(["xp=" + ",".join("%s:%.1f" % (k, quest["xp"][k]) for k in VIRTUE_KEYS),
            "relics=" + ",".join("%s:%d" % kv for kv in sorted(quest["relics"].items())),
            "visits=" + ",".join("%s:%d" % kv for kv in sorted(quest["visits"].items())),
            "hunts=%d" % quest["hunts"], "med=%d" % quest["med"], "tab=%d" % quest["tab"]]))

    def save_pos(which):
        """Save one window's position."""
        Kit.save_pos(POS_KEYS[which], wins[which]["g"])

    def player():
        """The player's mobile, from the mother's per-pass shared read."""
        return HOST.me()

    def find_mob(ser):
        """A mobile by serial, from the mother's shared read."""
        return HOST.mobile(ser)

    def name():
        """The pet's name."""
        return settings["name"]

    def sound(idx):
        """Play a sound if sounds are on."""
        if settings["sounds"] and idx:
            API.PlaySound(idx)

    def sounds_due(t):
        """Play the delayed sounds whose time has come."""
        q = st["snd_later"]
        # Most ticks have nothing due, so scan first and rebuild the list only when something is.
        if q:
            for e in q:
                if e[0] <= t:
                    break
            else:
                return
            st["snd_later"] = [e for e in q if e[0] > t]
            for due, idx in q:
                if due <= t:
                    sound(idx)

    def squeak():
        """Play the squeak of the voice the pet wears."""
        sound(BY_ID[shop["eq"]["voice"]].get("snd", 0x1A6))

    def speak(text, secs=3.0):
        """Show a line in the pet's speech bubble for a few seconds."""
        st["say"], st["say_until"] = text, time.time() + secs

    def clamp(v, lo=0.0, hi=100.0):
        """Limit v to the range lo to hi."""
        return max(lo, min(hi, v))

    def step_to(x, y, tx, ty, step):
        """Move a point from (x, y) towards (tx, ty) by at most step, landing on the target if close."""
        dx, dy = tx - x, ty - y
        dist = math.hypot(dx, dy)
        if dist <= step or dist < 0.01:
            return tx, ty
        return x + dx / dist * step, y + dy / dist * step

    def bump(k, n):
        """Change one of the pet's needs by n, staying within 0 to 100."""
        pet[k] = clamp(pet[k] + n)

    def eq(slot):
        """The item worn or used in a slot, or None."""
        return BY_ID.get(shop["eq"].get(slot) or "")

    def default_item(slot):
        """What a slot holds when nothing is chosen: its free first item, or nothing."""
        return BY_CAT[slot][0]["id"] if slot in DEFAULT_SLOTS else ""

    def stackable(it):
        """True for treats and traps, which are bought again and again and counted, never owned."""
        return it["cat"] == "treat" or it.get("uses")

    def has(iid):
        """True when the item is owned."""
        return iid in shop["own"]

    def pers(k, default):
        """A value from the worn personality, or the default when it does not set one."""
        return eq("pers").get(k, default)

    def pantry_max():
        """How many food items the pantry holds at most."""
        return PANTRY_BIG if has("u_pantry") else PANTRY_MAX

    def vxp_need(level):
        """Total experience a virtue needs to reach a level (100, 300, 600 ... 5500)."""
        return 50.0 * level * (level + 1)

    _vl = {}

    def vlevel(key):
        """The level of a virtue, from its experience."""
        xp = quest["xp"].get(key, 0.0)
        c = _vl.get(key)
        # Remembered per virtue and recomputed only when the experience changed: the simulation asks
        # several times a tick.
        if c is not None and c[0] == xp:
            return c[1]
        lv = 0
        while lv < VIRTUE_MAX and xp >= vxp_need(lv + 1):
            lv += 1
        _vl[key] = (xp, lv)
        return lv

    def vprogress(key):
        """Experience into the current level and the experience that level needs, or (0, 0) at the top."""
        lv = vlevel(key)
        if lv >= VIRTUE_MAX:
            return 0.0, 0.0
        base = vxp_need(lv)
        return quest["xp"].get(key, 0.0) - base, vxp_need(lv + 1) - base

    def veffect(key, lv):
        """The virtue's effect text at a level."""
        v = VIRTUE_BY_KEY[key]
        # A negative number divides the level instead of multiplying it.
        n = lv // -v[4] if v[4] < 0 else lv * v[4]
        return v[3] % n if "%d" in v[3] else v[3]

    def vall_at(level):
        """True when every virtue is at least at the level."""
        return all(vlevel(k) >= level for k in VIRTUE_KEYS)

    def relic_bonus():
        """The squeak bonus from the distinct relics found, as a fraction."""
        return RELIC_BONUS * len(quest["relics"])

    def meets(req):
        """None when a place's requirement is met, else the reason it is not."""
        if req is None:
            return None
        if req[0] == "stage":
            if pet["stage"] < req[1]:
                return "needs a grown mongotchi" if req[1] == 1 else "needs a Greater Mongotchi"
        elif req[0] == "virtue":
            if vlevel(req[1]) < req[2]:
                return "needs %s at level %d" % (VIRTUE_BY_KEY[req[1]][1], req[2])
        return None

    def price_of(it):
        """What an item costs now; Honesty lowers prices."""
        return int(round(it["price"] * (1.0 - VIRTUE_FX["hon_price"] * vlevel("hon"))))

    def away_doing():
        """What the pet is doing away, as a sentence: foraging, treasure hunting or meditating."""
        k = pet["away_kind"]
        if k == 1:
            # The index is clamped in case a save came from a build with more places or shrines.
            return "treasure hunting at %s" % LOCATIONS[min(pet["away_loc"], len(LOCATIONS) - 1)]["name"]
        if k == 2:
            return "meditating at the Shrine of %s" % VIRTUES[min(pet["away_virt"], len(VIRTUES) - 1)][1]
        return "foraging"

    def away_short():
        """The short form of the away state, for the minimised bar."""
        return {1: "out hunting", 2: "meditating"}.get(pet["away_kind"], "out foraging")

    def earn(kind, n=None):
        """Pay squeaks for a kind of care (or n squeaks) and return what was paid.

        Multipliers: personality, Lucky Black Pearl, Honor and relics. Passive squeaks do not mark the
        shop for saving, since they are earned again from the saved time. The floating "+n" is skipped
        for passive and social squeaks.
        """
        n = EARN.get(kind, 0) if n is None else n
        if n <= 0:
            return 0
        # Personality, the Lucky Black Pearl.
        mult = pers("squeak", 1.0) * (LUCK_BONUS if has("u_luck") else 1.0)
        # Honor and relics.
        mult *= 1.0 + VIRTUE_FX["hnr_squeaks"] * vlevel("hnr") + relic_bonus()
        # Held and earned in all (the achievements count the second).
        shop["sq"] += n * mult
        ach["earned"] += n * mult
        if kind != "passive":
            # Passive squeaks are earned again from the saved time, so they never force a save.
            st["shop_dirty"] = True
            if kind != "social" and n * mult >= 1:
                pop_text("+%d" % int(round(n * mult)), Kit.HUE_TITLE, 12, -26.0, 1.4)
        return n * mult

    def mood():
        """The pet's mood from 0 to 100: a weighted mix of happiness, fullness, cleanliness and energy,
        lowered by sickness.
        """
        return clamp(0.45 * pet["joy"] + 0.30 * pet["food"] + 0.15 * pet["clean"]
                     + 0.10 * pet["energy"] - (15 if pet["sick"] else 0))

    def loyalty():
        """The loyalty text for the mood and its hue."""
        # Mood is 0 to 100, so the last LOYALTY entry always matches.
        m = mood()
        for lim, text in LOYALTY:
            if m >= lim:
                return text, (Kit.HUE_GOOD if m >= 55 else Kit.HUE_BAD if m < 35 else Kit.HUE_TEXT)

    def hm(secs):
        """Format seconds as "1h 05m" or "5m"."""
        secs = max(0, int(secs))
        return "%dh %02dm" % (secs // 3600, (secs % 3600) // 60) if secs >= 3600 else "%dm" % (secs // 60)

    # Kit.fit cuts text with ".." by letter widths rather than letter count.
    fit = Kit.fit

    def full_name(nm, title_id):
        """The pet's name followed by its title, if it wears one."""
        t = BY_ID.get(title_id or "")
        return nm + (" " + t["name"] if t else "")

    def new_pet():
        """Start a fresh pup: reset the pet and its timers, save, play the arrival effects and announce."""
        pet.update(PET_NEW)
        pet["uid"] = random.randint(1, 65535)
        pet["last"] = time.time()
        st.update({"grem": None, "eat_until": 0.0, "play_until": 0.0, "cure_until": 0.0,
                   "brush_until": 0.0, "leave_until": 0.0, "away_until": 0.0, "say": "",
                   "remind": {}, "px": float(PX0 + PW // 2 - PB_W // 2), "py": float(YMIN + 10),
                   "hover_until": 0.0, "dizzy_until": 0.0})
        save_pet()
        anim("arrive", 1.2)
        sprite(SPR_SPARKLE, PX0 + PW / 2.0, YMIN + 30, 1.2, 0, 64)
        say("a pup has adopted you: meet %s (rename it on the settings page)." % name(), Kit.HUE_GOOD)

    # A 64-character run with no alphabet character on either side, so a code is not cut out of
    # a longer word.
    CODE_RE = re.compile(r"(?<![A-Za-z0-9_\-])([A-Za-z0-9_\-]{64})(?![A-Za-z0-9_\-])")

    def slot_index(slot, iid):
        """The 1-based position of an item inside its category, or 0 for none. This is how a worn item is
        stored in the playpen code.
        """
        ids = [it["id"] for it in BY_CAT.get(slot, [])]
        return ids.index(iid) + 1 if iid in ids else 0

    def slot_item(slot, n):
        """The item at a 1-based position of a category, or the slot's default when out of range."""
        lst = BY_CAT.get(slot, [])
        return lst[n - 1]["id"] if 1 <= n <= len(lst) else default_item(slot)

    def text_bytes(s, n):
        """Printable ASCII of s as exactly n bytes: other characters become "?", the rest is padded
        with zeros.
        """
        b = [ord(ch) if 32 <= ord(ch) < 127 else 63 for ch in s[:n]]
        return b + [0] * (n - len(b))

    def bytes_text(b):
        """Turn bytes back into text, keeping printable ASCII only."""
        return "".join(chr(x) for x in b if 32 <= x < 127).strip()

    _owner = {"at": -99.0, "name": "Someone", "raw": None}

    def my_owner():
        """The player's name cleaned for the playpen code, re-read at most every two seconds."""
        t = time.time()
        if t - _owner["at"] >= 2.0:
            _owner["at"] = t
            # Cached against the raw name so the cleaning runs only when the character changes.
            raw = safe(lambda: player().Name, "") or "Someone"
            if raw != _owner["raw"]:
                _owner["raw"] = raw
                _owner["name"] = clean_name(raw, 16)
        return _owner["name"]

    def my_code():
        """Build the 64-character playpen code of this pet.

        Layout (48 bytes): version, stage, eleven worn slots, mood, age in hours, swats, pet id (two
        bytes), name (12), owner (16), checksum (two bytes). The bytes are packed with Kit.b64 and sealed
        with Kit.checksum, so every module that shares codes reads and writes the same format.
        """
        data = [1, pet["stage"]] + [slot_index(s, shop["eq"].get(s, "")) for s in CODE_SLOTS]
        data += [int(mood()), min(255, int(pet["age"] // 3600)), min(255, pet["swats"]),
                 (pet["uid"] >> 8) & 255, pet["uid"] & 255] + text_bytes(name(), 12) + text_bytes(my_owner(), 16)
        c = Kit.checksum(data)
        return Kit.b64(data + [(c >> 8) & 255, c & 255])

    def decode(code):
        """Read a playpen code into a guest record, or None when its length, characters, version or
        checksum are wrong. Items out of range fall back to the slot's default.

        Uses Kit.unb64 and Kit.checksum, the same routines my_code packs with. Codes arrive from other
        players' chat, so nothing in them is trusted until the checks pass.
        """
        if not code or len(code) != 64 or any(ch not in Kit.B64_REV for ch in code):
            return None
        d = Kit.unb64(code)
        if len(d) != 48 or d[0] != 1 or Kit.checksum(d[:46]) != (d[46] << 8 | d[47]):
            return None
        g = {"code": code, "stage": min(2, d[1]), "mood": d[13], "age": d[14], "swats": d[15],
             "uid": d[16] << 8 | d[17], "name": bytes_text(d[18:30]) or "Mongotchi",
             "owner": bytes_text(d[30:46]) or "Someone"}
        for n, k in enumerate(CODE_SLOTS):
            g[k] = slot_item(k, d[2 + n])
        return g

    def sim(dt, events):
        """Advance the pet's needs by dt seconds of life (one step per second), collecting events.

        Needs fall at their rates scaled by pace, personality, virtues, sleep and sickness; a pet
        away meditating loses hunger more slowly. Does nothing for a wild pet.
        """
        if pet["feral"]:
            return
        p = settings["pace"] / 100.0
        h = dt / 3600.0 * p
        asleep, sick = pet["asleep"], pet["sick"]
        # Looked up once per step: the personality alters most rates below.
        pe = eq("pers")
        # Meditating calms the pet: half the hunger.
        calm = 0.5 if (pet["away"] and pet["away_kind"] == 2) else 1.0
        FX = VIRTUE_FX
        # Fullness falls half as fast asleep and a quarter faster when sick, scaled by the personality,
        # Humility and meditation.
        pet["food"] -= RATE_FOOD * h * (0.5 if asleep else 1.0) * (1.25 if sick else 1.0) \
            * pe.get("food_rate", 1.0) * (1.0 - FX["hum_hunger"] * vlevel("hum")) * calm
        # Happiness falls at a base rate (none asleep), eased by Compassion.
        loss = 0.0 if asleep else RATE_JOY * pe.get("joy_rate", 1.0) * (1.0 - FX["com_joy_loss"] * vlevel("com"))
        # Each unmet need (hungry, dirty, sick) costs extra happiness, eased by Humility.
        loss += RATE_JOY_NEED * ((pet["food"] < 25) + (pet["clean"] < 30) + bool(sick)) \
            * (1.0 - FX["hum_need"] * vlevel("hum"))
        pet["joy"] -= loss * h * calm
        if asleep:
            deco = eq("decor")
            # Sleeping restores energy; a pillow and the personality make it better.
            pet["energy"] += (RATE_SLEEP * h * pe.get("sleep", 1.0) * (deco.get("sleep", 1.0) if deco else 1.0))
        else:
            pet["energy"] -= RATE_ENERGY * h * (1.5 if sick else 1.0) * pe.get("energy_rate", 1.0)
        # Every heap left in the pen makes the pet dirtier faster.
        pet["clean"] -= (RATE_DIRT + RATE_DIRT_MESS * pet["messes"]) * h
        for k in ("food", "joy", "energy", "clean"):
            pet[k] = clamp(pet[k])
        # Age and the care average advance with the pace, so a faster pace grows it sooner.
        pet["age"] += dt * p
        pet["care_sum"] += mood() * dt * p
        pet["care_t"] += dt * p
        pet["mess_in"] -= dt * p
        if pet["mess_in"] <= 0:
            pet["mess_in"] = random.uniform(MESS_MIN, MESS_MAX) * 60.0
            if pet["messes"] < MESS_MAX_N and not pet["away"]:
                pet["messes"] += 1
                events.append(("mess", "%s left a little heap in the pen." % name()))
        pet["supply_in"] -= dt * p
        if pet["supply_in"] <= 0:
            pet["supply_in"] = SUPPLY_MIN * 60.0
            if pet["pantry"] < pantry_max():
                pet["pantry"] += 1
                events.append(("supply", "A farmer left some food at the pen (+1)."))
        # The Auto-Feeder feeds from the pantry when the pet is hungry, awake and at home.
        if has("u_feeder") and pet["food"] < 20 and pet["pantry"] > 0 and not pet["asleep"] and not pet["away"]:
            f = random.choice(FOODS)
            pet["pantry"] -= 1
            bump("food", f[2])
            events.append(("feeder", "the Auto-Feeder gave %s %s." % (name(), f[1])))
        if not sick:
            # Sickness chance per hour, eased by Spirituality; drawn once per step against the share of
            # an hour the step covers.
            rate = ((SICK_DIRTY if pet["clean"] < 30 else 0.0) + (SICK_STARVE if pet["food"] < 10 else 0.0))
            rate *= 1.0 - FX["spi_sick"] * vlevel("spi")
            if rate and random.random() < rate * h:
                pet["sick"], pet["sick_t"] = True, 0.0
                events.append(("sick", "%s is sick: give it a Cure potion." % name()))
        else:
            pet["sick_t"] += dt * p
        # Out of energy it falls asleep (not while away); it wakes only when fully rested.
        if not pet["asleep"] and pet["energy"] <= 3 and not pet["away"]:
            pet["asleep"] = True
            events.append(("sleep", "%s fell asleep." % name()))
        elif pet["asleep"] and pet["energy"] >= 100:
            pet["asleep"] = False
            events.append(("wake", "%s woke up rested." % name()))
        # Neglect counts up while it starves, has no happiness left or has been sick too long, and heals
        # at half speed otherwise. Long enough and it goes wild.
        bad = (pet["food"] <= 0 or pet["joy"] <= 0 or (pet["sick"] and pet["sick_t"] > SICK_NEGLECT * 3600))
        if bad:
            pet["neglect"] += dt * p
        else:
            pet["neglect"] = max(0.0, pet["neglect"] - dt * p * 0.5)
            if pet["neglect"] == 0:
                pet["warned"] = False
        if pet["neglect"] >= FERAL_HOURS * 3600:
            pet["feral"], pet["away"], pet["asleep"] = True, False, False
            events.append(("feral", "%s decided it is better off without a master and flew away." % name()))
            return
        if pet["neglect"] >= WARN_HOURS * 3600 and not pet["warned"]:
            pet["warned"] = True
            events.append(("warn", "%s looks around for someone else to care for it." % name()))
        # Growth: pup to mongotchi by age; to Greater only with enough age and a good average mood.
        if pet["stage"] == 0 and pet["age"] >= PUP_HOURS * 3600:
            pet["stage"] = 1
            events.append(("grow", "%s has grown into a mongotchi." % name()))
        elif pet["stage"] == 1 and pet["age"] >= GREATER_HOURS * 3600 and pet["care_t"] > 0 \
                and pet["care_sum"] / pet["care_t"] >= GREATER_CARE:
            pet["stage"] = 2
            events.append(("grow", "%s is now a Greater Mongotchi." % name()))

    EVENT_HUE = {"sick": Kit.HUE_BAD, "feral": Kit.HUE_BAD, "warn": Kit.HUE_BAD, "grow": Kit.HUE_GOOD,
                 "feeder": Kit.HUE_INFO, "sleep": Kit.HUE_INFO, "wake": Kit.HUE_INFO}

    def handle_events(events, live=True):
        """Show and act on the events the simulation reported, each as (kind, text).

        live=False is used for events replayed after time away: the journal lines are still said
        (except sleep and wake) and growth still pays, but no sounds or animations play. Runs on the
        client tick.
        """
        for kind, text in events:
            if kind in EVENT_HUE and (live or kind not in ("sleep", "wake")):
                say(text, EVENT_HUE[kind])
            if kind == "grow":
                earn("grow")
            if not live:
                continue
            if kind == "grow":
                sound(SND_GROW)
                speak("*grows!*", 4)
                anim("grow", 2.5)
                pet_sprite(SPR_STARS, 2.0, 72)
            elif kind == "sick":
                sound(SND_HURT)
                speak("*cough cough*")
                anim("cough", 0.4)
            elif kind == "feral":
                squeak()
                anim("farewell", 2.5)
                st["redraw_at"] = time.time() + 2.6
            # Supply and feeder events are shown as a dropped food item; mess, sleep and wake have their
            # own small animations.
            elif kind in ("supply", "feeder"):
                sound(SND_FOOD)
                st["carry"] = {"who": "drop", "gfx": random.choice(FOODS)[0], "t0": time.time(),
                               "x": float(PX0 + 40 + random.randint(0, 60)), "y": float(PY0 + 20)}
            elif kind == "mess":
                anim("mess%d" % max(0, pet["messes"] - 1), 0.5)
            elif kind == "sleep":
                anim("yawn", 1.4)
            elif kind == "wake":
                anim("stretch", 0.5)

    def catch_up():
        """Catch up on the time the module was off: passive squeaks, a trip in progress, and (only when
        the setting is on) the pet's own needs.

        Squeaks always trickle in, up to OFFLINE_MAX_H hours; the pet lives through the gap only when
        "Keep living while the module is off" is ticked. Runs once at start, after the loads.
        """
        now = time.time()
        if shop["last"]:
            gap = min(max(0.0, now - shop["last"]), OFFLINE_MAX_H * 3600)
            got = earn("passive", PASSIVE_PER_H * gap / 3600.0)
            if got >= 1:
                say("%d squeaks earned while you were away." % int(got), Kit.HUE_GOOD)
        shop["last"] = now
        gap = max(0.0, now - pet["last"]) if pet["last"] else 0.0
        # A trip carries on while the module is closed: the time gone comes off it, and one that ran
        # out ends now, quietly (the journal line, but no sound or haul animation).
        if pet["away"]:
            left = pet["away_left"]
            if pet["away_total"] > 0:
                # A saved trip never grows, even if the saved value is off.
                left = min(left, pet["away_total"])
            pet["away_left"] = max(0.0, left - gap)
            st["away_until"] = now + pet["away_left"]
            if pet["away_left"] <= 0:
                st["away_until"] = now
                finish_away(quiet=True)
        if not settings["offline"] or gap < 60 or pet["feral"]:
            return
        gap = min(gap, OFFLINE_MAX_H * 3600)
        events = []
        left = gap
        # Replays the gap in steps of at most a minute, as the simulation expects small steps.
        while left > 0 and not pet["feral"]:
            step = min(60.0, left)
            sim(step, events)
            left -= step
        say("while away (%s): fullness %d, happiness %d, %s, pantry %d." % (
            hm(gap), pet["food"], pet["joy"], Kit.count(pet["messes"], "heap"), pet["pantry"]), Kit.HUE_INFO)
        handle_events([e for e in events if e[0] in ("sick", "grow", "warn", "feral")], live=False)

    def can_act(what):
        """Check whether the pet can take an action now, saying why not when it cannot.

        A wild pet cannot act, a pet away cannot, and a sleeping one only for Lights and Clean.
        """
        if pet["feral"]:
            say("%s has gone wild: adopt a new pup in the pen." % name(), Kit.HUE_INFO)
            return False
        if pet["away"]:
            say("%s is out %s." % (name(), away_doing()), Kit.HUE_INFO)
            return False
        if pet["asleep"] and what not in ("lights", "clean"):
            speak("z Z z")
            say("%s is asleep (Lights wakes it)." % name(), Kit.HUE_INFO)
            return False
        return True

    def awake_home():
        """True when the pet is neither asleep nor away."""
        return not pet["asleep"] and not pet["away"]

    def busy():
        """True while the pet is eating, playing or just leaving, so only one action runs at a time."""
        t = time.time()
        return t < st["eat_until"] or t < st["play_until"] or t < st["leave_until"]

    def do_feed(action, t):
        """Feed: take one food from the pantry and have the pet eat it.

        Refuses when the pantry is empty or the pet is nearly full.
        """
        if not can_act("feed") or busy():
            return
        if pet["pantry"] <= 0:
            speak("*eyes the empty pantry*")
            say("the pantry is empty: Forage, or wait for the farmer.", Kit.HUE_BAD)
            return
        if pet["food"] >= 95:
            speak("*turns its nose up*")
            return
        pet["pantry"] -= 1
        start_eating(random.choice(FOODS), t)

    def start_eating(food, t):
        """Put a food (graphic, name, fullness) down where the pet flies to eat it."""
        st.pop("eat_t0", None)
        st["eat_bites"] = 1.0
        st["eat_food"] = food
        st["eat_x"] = random.randint(PX0 + 70, PX0 + PW - 60)
        st["eat_until"] = t + EAT_SECS

    def finish_eat():
        """When the eating is done: pay the fullness and happiness, count it and pay squeaks."""
        _, fname, val = st["eat_food"]
        st["eat_food"] = None
        bump("food", val)
        bump("joy", pers("feed_joy", 5))
        pet["fed"] += 1
        earn("feed")
        sound(SND_EAT)
        speak("*munches %s*" % fname.split(" ", 1)[1] if " " in fname else "*munch*")

    def give_treat(it, t):
        """Give a treat from the shop stock; return True when it was given.

        Applies the treat's changes, then lets the pet eat the art with no extra fullness, since it was
        paid above. A treat of its season earns the Festive achievement.
        """
        if not can_act("treat") or busy() or shop["cnt"].get(it["id"], 0) <= 0:
            return False
        shop["cnt"][it["id"]] -= 1
        st["shop_dirty"] = True
        for k in ("food", "joy", "energy", "clean"):
            if it.get(k):
                bump(k, it[k])
        if it.get("cure") and pet["sick"]:
            pet["sick"], pet["sick_t"] = False, 0.0
        if it.get("guard"):
            pet["guard"] = True
        if it.get("dizzy"):
            st["dizzy_until"] = t + 30.0
        earn("treat")
        sound(SND_EAT)
        if it.get("spooky"):
            anim("spooky", 1.6)
        if it.get("energy", 0) >= 20:
            anim("zoom", 4.0)
        if it.get("guard"):
            pop_text("!", Kit.HUE_BAD, 0, -30.0)
        if it.get("cure"):
            pet_sprite(SPR_HEAL, 1.2)
        if it.get("sleep"):
            anim("yawn", 1.4)
        # Fullness 0: already given above.
        start_eating((it["gfx"], it["name"], 0), t)
        speak("*spooky squeak!* BOO!" if it.get("spooky") else "*gobbles the %s*" % it["name"].lower(), 3.5)
        if it.get("sleep"):
            st["sleep_after"] = t + EAT_SECS + 0.5
        say("you give %s a %s." % (name(), it["name"].lower()), Kit.HUE_GOOD)
        if it.get("season") and in_season(it):
            ach_award("festive")
        return True

    def do_play(action, t):
        """Play: start the toy's animation for PLAY_SECS, unless the pet is too sick or too tired."""
        if not can_act("play") or busy():
            return
        if pet["sick"]:
            speak("*cough*")
            say("%s is too sick to play." % name(), Kit.HUE_INFO)
            return
        if pet["energy"] < 15:
            speak("*yawns*")
            say("%s is too tired to play." % name(), Kit.HUE_INFO)
            return
        toy = eq("toy")
        st["play_toy"] = toy
        st["play_until"] = t + PLAY_SECS
        st["toy"] = [float(PX0 + 20), float(FLOOR_Y - 40), random.uniform(70, 110), -60.0]
        st["music_at"] = 0.0
        if toy.get("motion") == "music":
            st["toy"] = [float(PX0 + PW // 2 - 22), float(FLOOR_Y), 0.0, 0.0]
            speak("*dances*")
        else:
            speak("*pounces!*")

    def finish_play():
        """When the play ends: happiness by the toy and personality, energy and fullness cost, squeaks."""
        toy = st["play_toy"] or eq("toy")
        joy = random.randint(10, 45) if toy.get("motion") == "dice" else 25 + toy.get("joy", 0)
        bump("joy", joy * pers("play", 1.0))
        pet["energy"] = clamp(pet["energy"] - 10 + toy.get("energy", 0))
        bump("food", -5)
        earn("play")
        if toy.get("squeaks"):
            earn("toy", toy["squeaks"])
        squeak()
        speak(random.choice(LINES["happy"]))

    def do_brush(action, t):
        """Brush: improves happiness and cleanliness, with a cooldown; the Grooming Kit doubles the gain
        and halves the cooldown.
        """
        if not can_act("brush") or busy():
            return
        if t < st["brush_cd"]:
            speak("*already shiny*")
            return
        k = 2 if has("u_groom") else 1
        st["brush_cd"] = t + BRUSH_COOLDOWN / k
        bump("joy", 10 * k)
        bump("clean", 10 * k)
        st["brush_until"] = t + 1.8
        earn("brush", EARN["brush"] * k)
        sound(SND_CLEAN)
        speak("*purrs... er, squeaks*")

    def do_clean(action, t):
        """Clean the pen: remove every heap and restore cleanliness; pays squeaks only when it was needed."""
        if not can_act("clean"):
            return
        if pet["messes"] == 0 and pet["clean"] >= 95:
            speak("*already spotless*")
            return
        if pet["messes"] or pet["clean"] < 80:
            earn("clean")
        st["mess_was"] = pet["messes"]
        anim("clean", 0.7)
        for i in range(pet["messes"]):
            sprite(SPR_SPARKLE, PX0 + 84 + i * 44 + 22, PY0 + PH - 20, 0.9, 0, 48)
        if not pet["asleep"]:
            anim("shake", 0.6)
            speak("*shakes its wings*")
        pet["messes"], pet["clean"] = 0, 100.0
        sound(SND_CLEAN)

    def do_lights(action, t):
        """Lights: wake a sleeping pet (grumpy if it is still tired) or put a tired one to bed."""
        if not can_act("lights"):
            return
        if pet["asleep"]:
            pet["asleep"] = False
            anim("stretch", 0.5)
            if pet["energy"] < 50:
                bump("joy", -5)
                speak("*grumpy squeak*")
            else:
                speak("*stretches*")
        elif busy():
            return
        elif pet["energy"] >= 90:
            speak("*isn't sleepy*")
        else:
            pet["asleep"] = True
            anim("yawn", 1.4)
            st["say"] = ""

    def do_cure(action, t):
        """Cure: end the sickness; costs a little happiness (the medicine tastes bad)."""
        if not can_act("cure"):
            return
        if not pet["sick"]:
            speak("*isn't sick*")
            return
        pet["sick"], pet["sick_t"] = False, 0.0
        bump("joy", -5)
        st["cure_until"] = t + 1.5
        anim("flash", 1.0)
        anim("shake", 0.8)
        pet_sprite(SPR_HEAL, 1.4)
        earn("cure")
        sound(SND_CURE)
        speak("*bleh!* ...*feels better*")

    def do_forage(action, t):
        """Forage: send the pet out for food for a short time, costing energy and some fullness.

        Sacrifice lowers the energy cost, down to a floor.
        """
        if not can_act("forage") or busy():
            return
        if pet["sick"] or pet["energy"] < 20:
            speak("*too weak*" if pet["sick"] else "*too tired*")
            say("%s is too %s to forage." % (name(), "sick" if pet["sick"] else "tired"), Kit.HUE_INFO)
            return
        if pet["pantry"] >= pantry_max():
            say("the pantry is full.", Kit.HUE_INFO)
            return
        bump("energy", -max(VIRTUE_FX["sac_forage_min"], FORAGE_ENERGY - VIRTUE_FX["sac_energy"] * vlevel("sac")))
        bump("food", -5)
        leave(t, 0, random.uniform(FORAGE_SECS[0], FORAGE_SECS[1]), "*flaps off*")

    def leave(t, kind, secs, line):
        """Start a trip of the given kind: away state, its length and the return time."""
        pet["away"], pet["away_kind"], pet["away_total"] = True, kind, secs
        st["away_until"], st["leave_until"] = t + secs, t + 1.5
        speak(line, 1.5)

    def finish_forage(quiet=False, frac=1.0):
        """End a forage trip: add the food found to the pantry (never over its limit) and pay squeaks.

        quiet=True (it ended while the module was off): no sound or haul animation. Sacrifice and the
        personality add food.
        """
        found = (1 + random.randint(0, 1) + (1 if pet["energy"] > 50 and random.random() < 0.5 else 0))
        found += pers("forage", 0) + vlevel("sac") // VIRTUE_FX["sac_per"]
        found = max(0, min(found, pantry_max() - pet["pantry"]))
        pet["pantry"] += found
        if found and not quiet:
            st["carry"] = {"who": "pet", "gfx": random.choice(FOODS)[0], "t0": time.time()}
        earn("forage", EARN["forage"] * found)
        say("%s foraged %d food." % (name(), found), Kit.HUE_GOOD if found else Kit.HUE_INFO)
        if quiet:
            return
        sound(SND_FOOD)
        speak("*brings back %d food!*" % found if found else "*found nothing*")

    def finish_away(quiet=False, frac=1.0):
        """End whichever trip the pet is on (forage, treasure hunt or meditation) and put it back home.

        frac below 1 means it was called home early, with that share of the reward.
        """
        k = pet["away_kind"]
        st["ach_due"] = True
        pet["away"], pet["away_kind"] = False, 0
        st["px"], st["py"] = float(XMAX), float(YMIN + 10)
        st["tx"], st["ty"] = float(PX0 + PW // 2), float(YMIN + 20)
        {1: finish_hunt, 2: finish_meditate}.get(k, finish_forage)(quiet, frac)

    def trip_left(t):
        """Seconds left of the trip."""
        return max(0.0, st["away_until"] - t)

    def trip_frac(t):
        """How much of the trip is done, from 0 to 1."""
        total = pet["away_total"] or 1.0
        return clamp(1.0 - trip_left(t) / total, 0.0, 1.0)

    def do_hunt(n, t):
        """Treasure hunt: send the pet to a place by index, if it meets the requirement and has the
        strength; costs energy (less with Sacrifice) and fullness.
        """
        if n < 0 or n >= len(LOCATIONS):
            return
        loc = LOCATIONS[n]
        if not can_act("hunt") or busy():
            return
        why = meets(loc["req"])
        if why:
            say("%s can't go to %s yet: %s." % (name(), loc["name"], why), Kit.HUE_BAD)
            return
        if pet["sick"] or pet["energy"] < 25:
            speak("*too weak*" if pet["sick"] else "*too tired*")
            say("%s is too %s for a treasure hunt." % (name(), "sick" if pet["sick"] else "tired"), Kit.HUE_INFO)
            return
        pet["away_loc"] = n
        bump("energy", -max(VIRTUE_FX["sac_hunt_min"], HUNT_ENERGY - VIRTUE_FX["sac_energy"] * vlevel("sac")))
        bump("food", -10)
        leave(t, 1, loc["mins"] * 60.0, "*flaps off on an adventure!*")
        sound(SND_FOOD)
        say("%s flies to %s (about %d min)." % (name(), loc["name"], loc["mins"]), Kit.HUE_GOOD)
        save_pet()
        st["quest_redraw"] = True

    def roll_loot(loc, rolls):
        """Roll the finds of a hunt from the place's table.

        Returns {"sq": n, "food": n, "trap": n, "treat": [ids], "relic": [ids]}. Spirituality raises
        the weight of the relic entries.
        """
        out = {"sq": 0, "food": 0, "trap": 0, "treat": [], "relic": []}
        spi = 1.0 + VIRTUE_FX["spi_relic"] * vlevel("spi")
        table = [(w * (spi if kind == "relic" else 1.0), kind, a, b) for w, kind, a, b in loc["loot"]]
        total = sum(e[0] for e in table)
        # One weighted draw per roll: walk the table subtracting each weight until the draw runs out.
        for _ in range(rolls):
            r = random.uniform(0, total)
            for w, kind, a, b in table:
                r -= w
                if r <= 0:
                    break
            if kind in ("sq", "food"):
                out[kind] += random.randint(a, b)
            elif kind == "trap":
                out["trap"] += 1
            else:
                out[kind].append(a)
        return out

    def finish_hunt(quiet=False, frac=1.0):
        """End a treasure hunt: roll the finds, pay them and tell the player what came back.

        quiet=True (it ended while the module was off) skips sound and animation; frac below 1 is a
        trip called home early and scales danger and rolls. Valor lowers the danger and Sacrifice adds
        finds. A bad trip halves the finds, costs energy and happiness and may make the pet sick.
        """
        loc = LOCATIONS[min(pet["away_loc"], len(LOCATIONS) - 1)]
        # Valor lowers the danger.
        danger = loc["danger"] * (1.0 - VIRTUE_FX["val_danger"] * vlevel("val"))
        hurt = random.random() < danger * frac
        # Sacrifice adds finds.
        rolls = random.randint(HUNT_ROLLS[0], HUNT_ROLLS[1]) + vlevel("sac") // VIRTUE_FX["sac_per"]
        # A fractional number of rolls is rounded up or down at random, so the average is right.
        rolls = int(rolls * frac + (random.random() < (rolls * frac) % 1.0))
        if hurt:
            rolls = rolls // 2
            bump("energy", -25)
            bump("joy", -10)
            if not pet["sick"] and random.random() < 0.35:
                pet["sick"], pet["sick_t"] = True, 0.0
        got = roll_loot(loc, rolls)
        parts = []
        if got["sq"]:
            n = earn("hunt", got["sq"])
            parts.append("%d squeaks" % int(round(n)))
        if got["food"]:
            room = max(0, pantry_max() - pet["pantry"])
            n = min(got["food"], room)
            pet["pantry"] += n
            # Food over the pantry's limit is lost and said so.
            parts.append("%d food" % n if n else "food the full pantry couldn't hold")
        for tid in got["treat"]:
            shop["cnt"][tid] = shop["cnt"].get(tid, 0) + 1
            parts.append(BY_ID[tid]["name"].lower() if tid in BY_ID else tid)
        if got["trap"]:
            shop["cnt"]["u_trap"] = shop["cnt"].get("u_trap", 0) + got["trap"]
            parts.append(Kit.count(got["trap"], "Gremlin Trap"))
        st["shop_dirty"] = st["quest_dirty"] = True
        new_relic = False
        for rid in got["relic"]:
            if rid not in quest["relics"]:
                new_relic = True
            quest["relics"][rid] = quest["relics"].get(rid, 0) + 1
            parts.append(RELIC_BY_ID[rid][1])
        quest["hunts"] += 1
        quest["visits"][loc["id"]] = quest["visits"].get(loc["id"], 0) + 1
        earn("forage", 2)
        if parts:
            haul = ", ".join(parts[:-1]) + (" and " if len(parts) > 1 else "") + parts[-1]
            end = ", but %s." % loc["bad"] if hurt else "."
            say("%s is back from %s with %s%s" % (name(), loc["name"], haul, end),
                Kit.HUE_BAD if hurt else Kit.HUE_GOOD)
        else:
            say("%s is back from %s empty-handed%s" % (name(), loc["name"], ": %s." % loc["bad"] if hurt else "."),
                Kit.HUE_BAD if hurt else Kit.HUE_INFO)
        if new_relic:
            say("new relic (Journeys > Relics): relic bonus now +%d%% squeaks." % int(round(relic_bonus() * 100)),
                Kit.HUE_GOOD)
            if len(quest["relics"]) == len(RELICS):
                say("%s has found every relic in Sosaria." % name(), Kit.HUE_GOOD)
        save_pet()
        st["quest_redraw"] = True
        if quiet:
            return
        gfx = RELIC_BY_ID[got["relic"][0]][2] if got["relic"] else random.choice(FOODS)[0] if parts else None
        if gfx is not None:
            st["carry"] = {"who": "pet", "gfx": gfx, "t0": time.time()}
        if hurt:
            sound(SND_HURT)
            speak("*ouch...*", 3.0)
            anim("cough", 0.4)
        else:
            sound(SND_FOOD)
            speak("*brings back treasure!*" if parts else "*found nothing*", 3.0)
            if new_relic:
                pet_sprite(SPR_STARS, 2.0, 72)

    def do_meditate(n, t):
        """Meditation: send the pet to a virtue's shrine for MEDITATE_MIN minutes, unless it is sick or
        the virtue is already at its top level.
        """
        if n < 0 or n >= len(VIRTUES):
            return
        v = VIRTUES[n]
        if not can_act("meditate") or busy():
            return
        if pet["sick"]:
            speak("*cough*")
            say("%s is too sick to meditate." % name(), Kit.HUE_INFO)
            return
        if vlevel(v[0]) >= VIRTUE_MAX:
            say("%s has mastered %s already." % (name(), v[1]), Kit.HUE_INFO)
            return
        pet["away_virt"] = n
        bump("food", -5)
        leave(t, 2, MEDITATE_MIN * 60.0, "*flaps off serenely*")
        say("%s flies to meditate at the Shrine of %s (%s, about %d min)." % (name(), v[1], v[2], int(MEDITATE_MIN)),
            Kit.HUE_GOOD)
        save_pet()
        st["quest_redraw"] = True

    def finish_meditate(quiet=False, frac=1.0):
        """End a meditation: add virtue experience, say what changed and announce level-ups.

        frac below 1 is a trip called home early. Experience grows with Spirituality, the mood and the
        growth stage. A level-up also announces the Avatar title when every virtue reaches level 5.
        """
        v = VIRTUES[min(pet["away_virt"], len(VIRTUES) - 1)]
        k = v[0]
        before = vlevel(k)
        # Spirituality, mood and growth stage all raise the experience.
        xp = MEDITATE_XP * (1.0 + VIRTUE_FX["spi_meditate"] * vlevel("spi")) \
            * (0.7 + 0.6 * mood() / 100.0) * (0.8, 1.0, 1.25)[pet["stage"]] * frac
        xp = max(0.0, xp)
        quest["xp"][k] = min(vxp_need(VIRTUE_MAX), quest["xp"].get(k, 0.0) + xp)
        quest["med"] += 1
        st["quest_dirty"] = True
        bump("joy", 10 * frac)
        bump("energy", 10 * frac)
        earn("meditate", 3)
        after = vlevel(k)
        done, need = vprogress(k)
        prog = "level %d, %d/%d" % (after, int(done), int(need)) if after < VIRTUE_MAX else "level %d, mastered" % after
        say("%s meditated on %s: +%d experience (%s)." % (name(), v[1], int(round(xp)), prog), Kit.HUE_GOOD)
        if after > before:
            eff = veffect(k, after)
            say("%s's %s has risen to level %d: %s." % (name(), v[1], after, eff[:1].lower() + eff[1:]), Kit.HUE_GOOD)
            if vall_at(5) and not st.get("vall_told_5"):
                st["vall_told_5"] = True
                say("all eight virtues at level 5: the Avatar title is for sale (Shop > Titles).", Kit.HUE_GOOD)
            if vall_at(VIRTUE_MAX):
                say("%s embodies all eight virtues: an Avatar among mongotchis." % name(), Kit.HUE_GOOD)
        save_pet()
        st["quest_redraw"] = True
        if quiet:
            return
        if after > before:
            sound(SND_MEDITATE)
            anim("grow", 2.0)
            pet_sprite(SPR_STARS, 2.0, 72)
        else:
            sound(SND_FOOD)
            pet_sprite(SPR_SPARKLE, 1.4, 64)
        speak("*feels enlightened*" if after > before else "*feels calm*", 3.0)

    def call_home(t):
        """Call the pet home from a hunt or meditation now, with the share of the reward the time done
        earns. A forage is not called home (it is short).
        """
        if not pet["away"]:
            return
        frac = trip_frac(t)
        st["away_until"] = t
        if pet["away_kind"] == 0:
            return
        say("%s called home (%d%% of the trip done)." % (name(), int(frac * 100)), Kit.HUE_INFO)
        finish_away(False, frac)

    def do_pet(action, t):
        """Pet it: a happiness gain with a cooldown, hearts, a squeak and a line of speech.

        Compassion adds to the happiness gain.
        """
        if pet["feral"] or pet["away"]:
            return
        if pet["asleep"]:
            speak("*snore*")
            return
        if t < st["pet_cd"]:
            speak(random.choice(LINES["happy"]))
            anim("hop", 0.6)
            return
        st["pet_cd"] = t + PET_COOLDOWN
        anim("hop", 0.6)
        pop_text("<3", HUE_HEART, -10, -22.0)
        pop_text("<3", HUE_HEART2, 8, -18.0)
        # Compassion makes petting worth more.
        bump("joy", pers("pet", 4) + VIRTUE_FX["com_pet"] * vlevel("com"))
        earn("pet")
        squeak()
        if eq("pers")["id"] == "p_grumpy" and random.random() < 0.3:
            speak("*nibbles your finger*")
        elif random.random() < 0.3 and top_virtue(5) is not None:
            speak(random.choice(VIRTUE_LINES[top_virtue(5)]))
        else:
            speak(random.choice(LINES["happy"]))

    def grem_gap():
        """Seconds before the next gremlin may come; much shorter on Halloween night."""
        return GREMLIN_GAP / HALLOWEEN_GREMLINS if st["hallow_night"] else GREMLIN_GAP

    def gremlin_tick(t, dt, full):
        """Run the gremlin each tick: possibly start one, walk it to the pantry, resolve its theft, and
        move it away again.

        t is the time, dt the seconds since the last call and full says whether the pen is drawn
        (a gremlin is quicker when only simulated). A gremlin has phases: walk, flee and trapped.
        The pet may chase it off on its own (guard), a Gremlin Trap catches it, otherwise it takes half
        the pantry; Justice or a mischievous personality win some back.
        """
        gr = st["grem"]
        if gr is None:
            # The cheap tests first; the random draw and the average come only when they pass.
            if not (settings["gremlins"] and not pet["feral"] and pet["pantry"] >= 2 and t >= st["next_grem_ok"]):
                return
            # The Scarecrow doubles the average gap between gremlins.
            mean = settings["grem_min"] * 60.0 * (2.0 if has("u_ward") else 1.0)
            # On Halloween night gremlins come far more often.
            if st["hallow_night"]:
                mean /= HALLOWEEN_GREMLINS
            if random.random() < dt / mean:
                if st["hallow_night"]:
                    lt = time.localtime(t)
                    day = (lt[0], lt[1], lt[2])
                    if st["hallow_told"] != day:
                        st["hallow_told"] = day
                        say("it's Halloween night: the gremlins are out in force.", Kit.HUE_BAD)
                # Only an awake, healthy, rested pet at home can guard.
                awake = awake_home() and not pet["sick"] and pet["energy"] > 20
                # A treat can guarantee a guard, otherwise a chance by personality and Valor.
                guard = awake and (pet["guard"] or random.random() < pers("guard", GUARD_CHANCE)
                                   + VIRTUE_FX["val_guard"] * vlevel("val"))
                if guard:
                    pet["guard"] = False
                # The gremlin walks from the right of the pen to the pantry; a guard is due 1.5 seconds in.
                st["grem"] = {"phase": "walk", "x": float(GX_START), "t0": t,
                              "walk": GREMLIN_WALK * (1.0 if full else 1.5), "guard_at": t + 1.5 if guard else 0.0}
                if awake_home():
                    pop_text("!", Kit.HUE_BAD, 0, -30.0, 1.2)
                if not full:
                    say("a gremlin is sneaking into the pen.", Kit.HUE_BAD)
            return
        if gr["phase"] == "walk":
            f = (t - gr["t0"]) / gr["walk"]
            gr["x"] = GX_START + (GX_PANTRY - GX_START) * min(1.0, f)
            # The guard cancels if the pet falls asleep, leaves or goes wild before it can act.
            if gr["guard_at"] and t >= gr["guard_at"]:
                if pet["asleep"] or pet["away"] or pet["feral"]:
                    gr["guard_at"] = 0.0
                elif t >= gr["guard_at"] + 1.2:
                    gr["phase"] = "flee"
                    anim("gswat", 0.5)
                    bump("joy", 5)
                    earn("guard", EARN["guard"] * (1.0 + VIRTUE_FX["jus_squeaks"] * vlevel("jus")))
                    sound(SND_OOF)
                    speak("*chases it off!*")
                    say("%s chased the gremlin away." % name(), Kit.HUE_GOOD)
                    return
            if f >= 1.0:
                gr["phase"] = "flee"
                if shop["cnt"].get("u_trap", 0) > 0:
                    shop["cnt"]["u_trap"] -= 1
                    st["shop_dirty"] = True
                    gr["phase"], gr["trap_t"] = "trapped", t
                    anim("gtrap", 0.9)
                    sprite(SPR_STARS, gr["x"] + GR_W / 2.0, GR_Y + 30, 0.9, 0, 56)
                    particle("SNAP!", Kit.HUE_BAD, gr["x"] + GR_W / 2.0, GR_Y + 10, 0.0, -20.0, 1.2)
                    got = earn("trap")
                    sound(SND_TRAP)
                    say("your Gremlin Trap caught the gremlin (+%d squeaks)." % int(round(got)), Kit.HUE_GOOD)
                    ach_award("trap")
                    return
                before = pet["pantry"]
                # It takes half the pantry, rounded down.
                pet["pantry"] //= 2
                lost = before - pet["pantry"]
                pet["stolen"] += lost
                sound(SND_GREMLIN)
                if awake_home():
                    speak("*SQUEAK!*")
                say("a gremlin stole %d of %d food." % (lost, before), Kit.HUE_BAD)
                if lost:
                    st["carry"] = {"who": "grem", "gfx": random.choice(FOODS)[0]}
                    particle("-%d" % lost, Kit.HUE_BAD, PX0 + 30, PY0 + PH - 40, 0.0, -18.0, 1.6)
                if lost and awake_home() and random.random() < pers("stealback", 0.0):
                    back = (lost + 1) // 2
                    pet["pantry"] = min(pantry_max(), pet["pantry"] + back)
                    speak("*steals %d back!*" % back)
                    say("but %s stole %d back." % (name(), back), Kit.HUE_GOOD)
                # Justice: the pet demands part of it back.
                elif lost and awake_home() and vlevel("jus"):
                    back = int(lost * VIRTUE_FX["jus_back"] * vlevel("jus") + random.random())
                    if back:
                        pet["pantry"] = min(pantry_max(), pet["pantry"] + back)
                        speak("*demands %d back!*" % back)
                        say("but %s won %d back (Justice)." % (name(), back), Kit.HUE_GOOD)
        elif gr["phase"] == "trapped":
            if t - gr["trap_t"] >= 0.9:
                st["grem"] = None
                st["next_grem_ok"] = t + grem_gap()
        else:
            # Fleeing: run off to the right; when only simulated (not drawn) it is gone at once.
            gr["x"] += 160.0 * dt
            if gr["x"] >= GX_START + 4 or not full:
                st["grem"] = None
                st["next_grem_ok"] = t + grem_gap()
                cr = st.get("carry")
                if cr is not None and cr["who"] == "grem":
                    st["carry"] = None

    def do_swat(action, t):
        """Swat the gremlin on a click, if it is still walking: it flees and the player earns squeaks."""
        gr = st["grem"]
        if gr is None or gr["phase"] != "walk":
            return
        gr["phase"] = "flee"
        anim("gswat", 0.5)
        particle("*SWAT*", Kit.HUE_GOOD, gr["x"] + GR_W / 2.0, GR_Y + 4, 0.0, -20.0, 1.0)
        pet["swats"] += 1
        # Counted over every pet you have had (the achievements use it).
        ach["swats"] += 1
        bump("joy", 5)
        # Justice raises the squeaks of a swat.
        earn("swat", EARN["swat"] * (1.0 + VIRTUE_FX["jus_squeaks"] * vlevel("jus")))
        sound(SND_SWAT)
        # The oof comes shortly after the smack.
        st["snd_later"].append((time.time() + OOF_DELAY, SND_OOF))
        if awake_home():
            speak("*cheers*")
        say("gremlin swatted: the food is safe.", Kit.HUE_GOOD)

    ALERT_TEXT = {"sick": "%s is sick.", "hungry": "%s is hungry.", "dirty": "%s's pen needs cleaning.",
                  "bored": "%s is unhappy: play with it."}
    MINI_ALERT = {"grem": "a gremlin in the pen", "sick": "sick", "hungry": "hungry",
                  "dirty": "pen needs cleaning", "bored": "unhappy"}

    def alert_keys():
        """What the pet needs most, as keys in order of urgency (no text is built here: asked every tick)."""
        out = []
        if st["grem"] is not None and st["grem"]["phase"] == "walk":
            out.append("grem")
        if pet["sick"]:
            out.append("sick")
        if pet["food"] < 25:
            out.append("hungry")
        if pet["messes"] >= 2 or pet["clean"] < 30:
            out.append("dirty")
        if pet["joy"] < 25:
            out.append("bored")
        return out

    def remind(t):
        """Print a journal reminder for each unmet need, at most every REMIND_EVERY seconds per need.

        Only a journal line; it never posts to chat (shard rule R1).
        """
        if not settings["remind"] or pet["feral"]:
            return
        for k in alert_keys():
            if k == "grem":
                continue
            if t - st["remind"].get(k, -1e9) >= REMIND_EVERY:
                st["remind"][k] = t
                say(ALERT_TEXT[k] % name(), Kit.HUE_BAD)

    def top_virtue(least):
        """The key of the strongest virtue if it is at least the level least, else None; the first wins
        a tie.
        """
        best, best_lv = None, least - 1
        for k in VIRTUE_KEYS:
            lv = vlevel(k)
            if lv > best_lv:
                best, best_lv = k, lv
        return best

    def chatter(t):
        """Now and then say a line fitting the pet's state, with a squeak sometimes.

        Shy and dramatic personalities change how often. Silent while it is away, asleep, busy or
        already speaking.
        """
        if t < st["next_chat"]:
            return
        st["next_chat"] = t + random.uniform(25, 60) / max(0.2, pers("chat", 1.0))
        if pet["feral"] or pet["away"] or pet["asleep"] or busy() or t < st["say_until"]:
            return
        if pet["sick"]:
            lines = LINES["sick"]
        elif pet["food"] < 30:
            lines = LINES["hungry"]
        elif pet["clean"] < 35:
            lines = LINES["dirty"]
        elif pet["joy"] < 35:
            lines = LINES["bored"]
        else:
            # The personality's own lines count double.
            lines = LINES["idle"] + pers("lines", []) * 2
            tv = top_virtue(5)
            if tv is not None:
                lines = lines + VIRTUE_LINES[tv] * 2
        speak(random.choice(lines))
        if random.random() < 0.3:
            if pet["sick"]:
                sound(SND_HURT)
            else:
                squeak()

    MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December")
    SEASON_SHOP = {"halloween": "costumes and pumpkin treats are", "winter": "warm hats, a snowman and gingerbread are",
                   "newyear": "a party cap, sparkling cider and fireworks are"}

    def season_keys(t):
        """The seasons on at time t by this computer's clock, as a frozenset of keys."""
        lt = time.localtime(t)
        md = (lt[1], lt[2])
        on = []
        for key, _, a, b in SEASONS:
            # A range whose last day comes before its first runs over the New Year.
            if (a <= md <= b) if a <= b else (md >= a or md <= b):
                on.append(key)
        return frozenset(on)

    def season_tick(t, force=False):
        """Look at the calendar every SEASON_EVERY seconds (or at once when forced).

        Sets the seasons on and Halloween night. When the seasons change, the pen (snow) and the shop
        (what it sells) are redrawn, and a season that begins is announced once per run.
        """
        # A clock set back looks again at once.
        if not force and st["season_at"] - SEASON_EVERY <= t < st["season_at"]:
            return
        st["season_at"] = t + SEASON_EVERY
        on = season_keys(t)
        lt = time.localtime(t)
        st["hallow_night"] = (lt[1], lt[2]) == HALLOWEEN_NIGHT
        if on == st["seasons"]:
            return
        was, st["seasons"] = st["seasons"], on
        for key, nm, _, b in SEASONS:
            if key in on and key not in st["season_told"]:
                st["season_told"].add(key)
                until = ("the end of February" if b == (2, 29) else "%s %d" % (MONTHS[b[0] - 1], b[1]))
                say("%s: %s in the Shop (Seasonal tab) until %s." % (
                    "it's " + nm if key != "winter" else "winter is here",
                    SEASON_SHOP.get(key, "its treats and clothes are"), until), Kit.HUE_GOOD)
        # The Seasonal tab went away with its season.
        if st["shop_cat"] >= len(shop_cats()):
            st["shop_cat"], st["shop_page"] = 0, 0
        # The first look comes before the windows exist.
        if was is not None:
            st["redraw"] = st["shop_redraw"] = True

    # How to read "what counts" of each achievement from the game state.
    ACH_VALUES = {"stage": lambda: pet["stage"], "age": lambda: pet["age"] / 3600.0, "swats": lambda: ach["swats"],
                  "earned": lambda: ach["earned"], "relics": lambda: len(quest["relics"]),
                  "places": lambda: len(quest["visits"]),
                  "shrines": lambda: sum(1 for k in VIRTUE_KEYS if quest["xp"].get(k, 0.0) > 0),
                  "virtue5": lambda: sum(1 for k in VIRTUE_KEYS if vlevel(k) >= 5), "guests": lambda: len(st["guests"]),
                  "charm": lambda: 1 if has("u_companion") else 0}

    def ach_check(t):
        """Grant the achievements earned since the last look (every ACH_EVERY seconds, and right after
        anything that can earn one).

        The first run grants everything earned before in a single journal line.
        """
        st["ach_at"], st["ach_due"] = t + ACH_EVERY, False
        # Older saves and swats counted on the pet alone catch up here.
        if pet["swats"] > ach["swats"]:
            ach["swats"] = pet["swats"]
        new = [a for a in ACHIEVEMENTS if a[6] is not None and a[0] not in ach["got"] and ACH_VALUES[a[6]]() >= a[7]]
        before, ach["new"] = ach["new"], False
        if new:
            ach_grant(new, before)

    def ach_grant(lst, before=False):
        """Mark achievements earned and pay their rewards (the save follows with the shop)."""
        total = 0
        for a in lst:
            ach["got"].add(a[0])
            total += a[3]
            if not before:
                say("achievement earned: %s (%s), +%d squeaks." % (
                    a[1], a[2][0].lower() + a[2][1:], a[3]), Kit.HUE_GOOD)
        # Rewards are flat: no squeak bonus applies, and the earned total counts them too.
        shop["sq"] += total
        ach["earned"] += total
        # Achievements found on the first run are told in one line, with no sound or animation.
        if before:
            say("%s already earned: %s, +%d squeaks." % (Kit.count(len(lst), "achievement"),
                                              ", ".join(a[1] for a in lst), total), Kit.HUE_GOOD)
        else:
            sound(SND_ACHIEVE)
            pop_text("+%d" % total, Kit.HUE_TITLE, 12, -26.0, 1.6)
            pet_sprite(SPR_STARS, 1.6, 64)
        st["texts_at"] = 0.0
        save_shop()

    def ach_award(aid):
        """Grant an achievement at the place it happens (a trapped gremlin, a seasonal treat), once."""
        if aid not in ach["got"]:
            ach_grant([ACH_BY_ID[aid]])

    def requirement(it):
        """Why a title or ultimate item cannot be bought yet, or None when its requirement is met."""
        r = it.get("req")
        if r == "swats" and pet["swats"] < 10:
            return "swat %d more gremlin%s first" % (10 - pet["swats"], "" if pet["swats"] == 9 else "s")
        if r == "greater" and pet["stage"] < 2:
            return "needs a Greater Mongotchi"
        if r == "elder" and pet["age"] < 24 * 3600:
            return "needs an age of 24 hours"
        if r == "charm" and not has("u_companion"):
            return "needs the Companion Charm"
        if r == "avatar" and not vall_at(5):
            return "needs every virtue at level 5"
        if r == "relics" and len(quest["relics"]) < 8:
            return "find %d more kind%s of relic" % (8 - len(quest["relics"]), "" if len(quest["relics"]) == 7 else "s")
        if r == "pilgrim" and top_virtue(VIRTUE_MAX) is None:
            return "meditate a virtue up to level %d" % VIRTUE_MAX
        return None

    def buy(it):
        """Buy an item with squeaks: a treat or trap adds to its count, anything else is owned and, if it
        has a slot, worn at once.

        Says why when it cannot be bought; the Companion Charm turns the companion on and also earns
        its achievement through the checks. Saves the shop.
        """
        if not stackable(it) and has(it["id"]):
            return
        why = requirement(it)
        what = it["name"] if it["cat"] != "title" else "the title \"%s\"" % it["name"]
        if why:
            say("you can't buy %s yet: %s." % (what, why), Kit.HUE_BAD)
            return
        price = price_of(it)
        if shop["sq"] < price:
            say("not enough squeaks for %s (%d more needed)." % (what, price - int(shop["sq"])), Kit.HUE_BAD)
            return
        shop["sq"] -= price
        slot = CAT_SLOT.get(it["cat"])
        if stackable(it):
            shop["cnt"][it["id"]] = shop["cnt"].get(it["id"], 0) + 1
        else:
            shop["own"].add(it["id"])
            if it.get("toggle"):
                set_comp(True)
                say("%s can now follow you in the world. Say \"%s stay\", \"%s follow\", "
                    "\"%s dance\", \"%s fetch\" or \"%s go home\"." % ((name(),) * 6), Kit.HUE_GOOD)
            if slot:
                # Wear it right away.
                shop["eq"][slot] = it["id"]
        sound(SND_BUY)
        if slot or it.get("toggle"):
            poof()
        say("bought %s for %d squeaks." % (it["name"], price), Kit.HUE_GOOD)
        save_shop()

    def wear(it, on):
        """Wear or take off an item (taking off restores the slot's default) and save."""
        slot = CAT_SLOT.get(it["cat"])
        if not slot:
            return
        shop["eq"][slot] = it["id"] if on else default_item(slot)
        if slot == "voice" and on:
            squeak()
        poof()
        save_shop()

    def pet_sprite(seq, dur, size=56):
        """Show a run of sparkle art on the pet in the main pen."""
        x, y = pet_xy()
        sprite(seq, x, y + 20, dur, 0, size)

    def poof():
        """A puff of smoke and sparkles on the pet, for a change of costume."""
        x, y = pet_xy()
        sprite(SPR_POOF, x, y + 20, 0.8, 0, 60)
        for dx in (-14, 0, 14):
            particle("*", HUE_WHITE, x + dx, y + 16, dx * 0.8, -16.0, 0.8)

    # Which slot each shop category fills (None for treats, upgrades and the ultimate).
    CAT_SLOT = dict((k, s) for k, _, s in CATS)

    def row_buttons(it):
        """The buttons of an item's shop row as (key, caption, action), right to left.

        Out of season an item can only be given or worn if already held, never bought.
        """
        iid = it["id"]
        # Out of season: only what you own or hold is offered.
        sell = in_season(it)
        if it["cat"] == "treat":
            return ([("buy", "Buy", "buy")] if sell else []) + \
                ([("give", "Give", "give")] if shop["cnt"].get(iid, 0) > 0 else [])
        if it.get("uses") or not has(iid):
            return [("buy", "Buy", "buy")] if sell else []
        if it.get("toggle"):
            return [("dismiss", "Dismiss", "dismiss")] if settings["comp"] else [("summon", "Summon", "summon")]
        slot = CAT_SLOT.get(it["cat"])
        if not slot:
            return []
        if shop["eq"].get(slot) == iid:
            if slot in DEFAULT_SLOTS:
                return []
            return [("remove", "Take off" if slot in ("hat", "neck") else "Remove", "remove")]
        return [("wear", "Wear" if slot in ("hat", "neck") else "Use", "wear")]

    # The art on each row button, by action key.
    ROW_ARTS = {"buy": Kit.ART_OK, "give": Kit.ART_OK, "wear": Kit.ART_PLAY,
                "summon": Kit.ART_PLAY, "remove": Kit.ART_CLOSE, "dismiss": Kit.ART_CLOSE}
    # How a tooltip names an item whose name alone does not say what it is.
    ROW_WHAT = {"title": "the title \"%s\"", "pers": "the %s personality", "dye": "the %s dye",
                "voice": "the %s voice", "ncol": "the %s name colour", "aura": "the %s aura"}

    def row_tip(bk, it):
        """The tooltip of a shop row button, saying what the one-word caption cannot."""
        nm = ROW_WHAT.get(it["cat"], "%s") % it["name"]
        title = it["cat"] == "title"
        if bk == "buy":
            return "Buy %s for %d squeaks" % (nm, price_of(it)) if not stackable(it) else \
                "Buy one %s for %d squeaks" % (nm, price_of(it))
        if bk == "give":
            return "Give %s a %s now" % (name(), nm.lower())
        if bk == "wear":
            return "Put %s on %s" % (nm, name()) if CAT_SLOT.get(it["cat"]) in ("hat", "neck") \
                else "Give %s %s" % (name(), nm) if title else "Switch to %s" % nm
        if bk == "remove":
            return "Take %s off (you keep it)" % nm if CAT_SLOT.get(it["cat"]) in ("hat", "neck") else \
                "Drop %s (you keep it)" % nm if title else "Stop using %s (back to the free one)" % nm
        if bk == "summon":
            return "Let %s follow you in the world" % name()
        return "Send %s home to its pen" % name()

    def in_season(it):
        """True when an item can be sold now: not seasonal, or its season is on."""
        s = it.get("season")
        return s is None or s in (st["seasons"] or ())

    def shown_in_shop(it):
        """Out of season the shop sells none of a season's items but still lists the ones you own (to
        wear or take off) or hold (to give).
        """
        if "season" not in it or in_season(it):
            return True
        return shop["cnt"].get(it["id"], 0) > 0 if stackable(it) else has(it["id"])

    def shop_cats():
        """The shop's tabs: the categories, plus the Seasonal tab while a season is on."""
        return CATS + [SEASON_CAT] if st["seasons"] else CATS

    def shop_items():
        """The items of the open shop tab."""
        cats = shop_cats()
        k = cats[min(st["shop_cat"], len(cats) - 1)][0]
        if k == "season":
            return [it for it in SEASONAL if in_season(it)]
        return [it for it in BY_CAT.get(k, []) if shown_in_shop(it)]

    # Row actions by key; the lambdas defer to the functions defined above.
    SHOP_ACTS = {"buy": lambda it: buy(it), "give": lambda it: give_treat(it, time.time()),
                 "wear": lambda it: wear(it, True), "remove": lambda it: wear(it, False)}

    def shop_act(iid, act):
        """Run a shop row button.

        The row's item and action were queued when it was drawn, so a row whose buttons changed since
        (a treat count reaching zero, Wear becoming Remove) cannot fire the wrong one: an action the
        row no longer offers is dropped.
        """
        it = BY_ID.get(iid)
        # Dropped when the row no longer offers this action.
        if it is None or act not in [b[2] for b in row_buttons(it)]:
            return
        if act in SHOP_ACTS:
            SHOP_ACTS[act](it)
        elif act in ("summon", "dismiss"):
            set_comp(act == "summon")
            say("%s %s." % (name(), "flutters out to join you" if settings["comp"]
                            else "flies home to its pen"), Kit.HUE_INFO)
        st["shop_redraw"] = True

    def share():
        """Share: post the pet's code in the chosen chat channel, on the player's press only (shard rule
        R1, no timed posting).
        """
        code = my_code()
        ch = CHANNELS[settings["share_ch"]]
        getattr(API, ch[1])("%s %s" % (CODE_TAG, code))
        st["shared_at"] = time.time()
        say("%s's code posted in %s chat." % (name(), ch[0]), Kit.HUE_INFO)

    def add_guest(g):
        """Add a guest from a decoded code to the playpen; return True when it is (or already was) there.

        The player's own pet is ignored; a known pet is updated when its code changed; when the pen is
        full a guest is refused with one journal line. Saves the guests.
        """
        if g is None:
            return False
        me = my_owner()
        # That is your own pet.
        if g["uid"] == pet["uid"] and g["owner"] == me:
            return False
        for n, old in enumerate(st["guests"]):
            if old["uid"] == g["uid"] and old["owner"] == g["owner"]:
                if old["code"] != g["code"]:
                    st["guests"][n] = g
                    save_guests()
                    st["pen_redraw"] = True
                return True
        if len(st["guests"]) >= PEN_MAX - 1:
            key = (g["uid"], g["owner"])
            if key not in st["full_told"]:
                st["full_told"][key] = True
                say("%s (%s's mongotchi) wanted to play, but the playpen is full (%d): send one home with its X."
                    % (g["name"], g["owner"], PEN_MAX), Kit.HUE_INFO)
            return False
        st["guests"].append(g)
        save_guests()
        st["pen_redraw"] = st["ach_due"] = True
        say("%s, %s's mongotchi, joined your playpen." % (full_name(g["name"], g["title"]), g["owner"]), Kit.HUE_GOOD)
        if not st["pen_open"]:
            say("open the Playpen to watch them play.", Kit.HUE_INFO)
        return True

    def listen():
        """Take the playpen codes other players shared from the journal lines read_client kept.

        Each journal line comes once, so nothing needs remembering here.
        """
        if not st["jcodes_due"]:
            return
        st["jcodes_due"] = False
        entries, st["jcodes"] = st["jcodes"], []
        for text, _ in entries:
            for m in CODE_RE.finditer(text):
                add_guest(decode(m.group(1)))

    # Cache for own_look: the key the look was built for, and the look.
    _ol = {"key": None, "look": None}

    def own_look():
        """The look of the player's pet (stage, hue, hat, necklace, aura).

        The same dict is returned while nothing in it changed (asked every frame): callers read it and
        never change it, and one wanting another hue copies it.
        """
        e = shop["eq"]
        key = (pet["sick"], pet["asleep"], pet["stage"], e.get("dye", ""), e.get("hat", ""),
               e.get("neck", ""), e.get("aura", ""))
        if key == _ol["key"]:
            return _ol["look"]
        dye = BY_ID.get(e.get("dye", ""))
        # Hue order: sick, asleep, the dye, the Greater colour, none.
        hue = (HUE_SICK if pet["sick"] else HUE_SLEEP if pet["asleep"] else dye["hue"] if dye and dye["hue"] else
               HUE_GREATER if pet["stage"] == 2 else 0)
        look = {"stage": pet["stage"], "hue": hue, "hat": e.get("hat", ""),
                "neck": e.get("neck", ""), "aura": e.get("aura", "")}
        _ol["key"], _ol["look"] = key, look
        return look

    def guest_look(g):
        """The look of a guest pet, in the same form as own_look."""
        dye = BY_ID.get(g["dye"])
        hue = dye["hue"] if dye and dye["hue"] else (HUE_GREATER if g["stage"] == 2 else 0)
        return {"stage": g["stage"], "hue": hue, "hat": g["hat"], "neck": g["neck"], "aura": g["aura"]}

    # Cache for pen_members: its key, the member list, their identity keys, the fixed parts per
    # member and the guest list it was made from.
    _pm = {"key": None, "list": [], "keys": [], "der": [], "refs": None}

    def pen_members():
        """Everyone in the playpen, the player's pet first and then the guests.

        The list and its entries are shared and rebuilt only when the key changes, so callers read them
        and never change them. A wild pet is left out.
        """
        e = shop["eq"]
        gl = st["guests"]
        owner = my_owner()
        key = (pet["feral"], pet["uid"], owner, name(), e.get("title", ""), e.get("pers", ""),
               # The guests are never changed in place (replaced, added, removed), so their identities tell
               # when the list changed.
               e.get("ncol", ""), e.get("toy", ""), tuple([id(g) for g in gl]))
        if key == _pm["key"]:
            return _pm["list"]
        me = {"uid": pet["uid"], "owner": owner, "name": name(), "title": e.get("title", ""),
              "pers": e.get("pers", ""), "ncol": e.get("ncol", ""), "toy": e.get("toy", ""), "mine": True}
        out = (([] if pet["feral"] else [me]) + [dict(g, mine=False) for g in gl])[:PEN_MAX]
        _pm.update({"key": key, "list": out, "refs": list(gl),
                    "keys": [(mb["uid"], mb["owner"]) for mb in out], "der": [None] * len(out)})
        return out

    def pen_derived(n, mb):
        """The parts of pen member n that never change for it: fitted name and width, name hue, speed
        and (for a guest) its look, made once per member and kept until the members change.
        """
        der = _pm["der"]
        d = der[n] if n < len(der) else None
        if d is None:
            nm = fit(mb["name"], 80)
            ncol = BY_ID.get(mb["ncol"] or "")
            d = {"nm": nm, "nw": Kit.text_w(nm), "hue": ncol["hue"] if ncol else Kit.HUE_TITLE,
                 "spd": 40.0 * BY_ID.get(mb["pers"] or "p_cheerful", {}).get("speed", 1.0),
                 "look": None if mb["mine"] else guest_look(mb)}
            if n < len(der):
                der[n] = d
        return d

    # Companion: seconds between redraws in the world, how high it flies above your feet in z units,
    # and the height of the hat and necklace above the pet by growth stage.
    COMP_TICK = 0.5
    COMP_Z = 3
    HAT_DZ = {0: 9, 1: 6, 2: 6}
    NECK_DZ = {0: 6, 1: 2, 2: 2}
    # Client effect art: sparkles for tricks and skill gains, blue sparkles for the heal, a small
    # fireball for War Training.
    FX_SPARKLE = 0x376A
    FX_HEAL = 0x373A
    FX_BOLT = 0x36E4
    # Notoriety names the companion treats as foes.
    HOSTILE = ("Gray", "Criminal", "Murderer", "Enemy")
    # Spoken pet commands: (word, command). Several words may mean the same command.
    COMMANDS = [("follow", "follow"), ("come", "follow"), ("stay", "stay"), ("speak", "speak"), ("dance", "dance"),
                ("trick", "dance"), ("kill", "kill"), ("attack", "kill"), ("good", "good"), ("sleep", "sleep"),
                ("nap", "sleep"), ("fetch", "fetch"), ("go home", "home"), ("dismiss", "home")]

    def comp_new():
        """A fresh companion record: off, at the origin, following, with every timer at zero."""
        return {"on": False, "x": 0, "y": 0, "map": None, "mode": "follow", "stay": None, "last_p": None, "dir": (0, 1),
                "still_since": time.time(), "next": 0.0, "aura_at": 0.0, "talk_at": 0.0, "help_at": 0.0, "dive": None,
                "hp": None, "dead": False, "hidden": False, "war": False, "casting": False, "gold": None,
                "target": None, "tiles": 0, "need_at": 0.0, "chat_at": 0.0, "nap": False, "fetch_until": 0.0,
                "hover_at": 0.0, "panic_at": 0.0, "trick_at": 0.0, "bob": 0, "z": 0, "serial": 0}

    def comp_wanted():
        """True when the companion should be out in the world: switched on, charm owned, and the pet
        neither wild nor away.
        """
        return settings["comp"] and has("u_companion") and not pet["feral"] and not pet["away"]

    def comp_say(text, force=False, hue=None):
        """Make the companion say a line over its head (only the player sees it), at most one every six
        seconds unless forced.

        Uses the name colour the pet wears when no hue is given. Silent when its talk option is off.
        """
        c = st["comp"]
        t = time.time()
        if not settings["comp_talk"] or (not force and t - c["talk_at"] < 6.0):
            return
        c["talk_at"] = t
        ncol = eq("ncol")
        h = hue if hue is not None else (ncol["hue"] if ncol else Kit.HUE_TITLE)
        ser = c.get("serial")
        if ser:
            API.HeadMsg("%s: %s" % (name(), text), ser, h)

    # Journal reading: seconds between looks at the player and the journal, the most journal lines
    # kept for the next look, and the cached reader state.
    READ_EVERY = 0.5
    JBUF_MAX = 50
    jr = {"rd": None, "name": None, "re": None, "now": None}

    def journal_now():
        """The client's clock in journal ticks, so a line's age can be measured by its own time.

        Uses .NET DateTime when the host provides it, else the plain clock converted to ticks.
        """
        fn = jr["now"]
        if fn is None:
            try:
                from System import DateTime
                fn = lambda: float(DateTime.Now.Ticks)
                fn()
            except Exception:
                fn = lambda: time.time() * 1e7
            jr["now"] = fn
        return fn()

    def journal_new():
        """The journal lines that arrived since the last look.

        The first look hands over what the journal already holds; read_client keeps only the last few
        seconds of it. Returns an empty list when the journal cannot be read.
        """
        try:
            if jr["rd"] is None:
                jr["rd"] = Journal.reader()
                return Journal.recent(Journal.MAX_BACK)
            return jr["rd"].new()
        except Exception:
            return []

    def cmd_pattern():
        """The pattern of a spoken command: this pet's name or "all", at the start of a line or as a word
        (case-insensitive, matched against the lower-case text). Rebuilt only when the name changes.
        """
        nm = name()
        if jr["name"] != nm:
            jr["name"] = nm
            jr["re"] = re.compile(r"(\b%s\b|^all )" % re.escape(nm.lower()))
        return jr["re"]

    def jfresh(ent, secs, now, t):
        """True when a kept journal line is young enough (secs) to count."""
        stamp = ent[-1]
        # Journal ticks are .NET ticks (ten million a second); a stamp that is small was the time first
        # seen instead.
        age = (now - stamp) / 1e7 if stamp > 1e12 else t - stamp
        return age <= secs

    def read_client(t):
        """Every READ_EVERY seconds read what the companion and the playpen need from the client.

        Reads the player (the whole player only while the companion is out, just the name and serial
        while it is dismissed so a spoken "follow" can still summon it), and the new journal lines:
        playpen codes (looked at every LISTEN_EVERY seconds) and spoken pet commands and skill gains.
        Kept lines are dropped once older than a few seconds. Runs inside the client's frame.
        """
        if t - st["read_at"] < READ_EVERY:
            return
        st["read_at"] = t
        want_player = comp_wanted()
        want_name = not want_player and has("u_companion")
        want_codes = settings["listen"] and t - st["listen_at"] >= LISTEN_EVERY
        if not (want_player or want_name or want_codes):
            st["player"] = None
            return
        st["player"] = read_player() if want_player else read_player_lite() if want_name else None
        if want_codes:
            st["listen_at"] = t
        lines = journal_new()
        jcodes, jcmds = st["jcodes"], st["jcmds"]
        # Forget remembered command lines after ten seconds.
        if cmd_seen:
            for k in [k for k, at in cmd_seen.items() if t - at > 10]:
                del cmd_seen[k]
        if lines:
            pat = cmd_pattern()
            for ln in lines:
                text = ln.text
                # Only lines holding the code tag are kept as playpen codes.
                if CODE_TAG in text:
                    jcodes.append((text, ln.ticks or ln.at))
                # Two kinds of line: spoken commands, then skill gain messages.
                if pat.search(ln.low):
                    # Repeats are told apart by the line's time to the second: the same words from the same speaker
                    # twice within one second count once (a macro saying a command twice).
                    sec = (ln.ticks // 10000000) if ln.ticks else int(ln.at)
                    k = (sec, ln.name, text)
                    if k in cmd_seen:
                        continue
                    cmd_seen[k] = t
                    jcmds.append((text, ln.name, 0, ln.low, ln.ticks or ln.at))
                elif "Your skill in" in text:
                    jcmds.append((text, ln.name, 1, ln.low, ln.ticks or ln.at))
        if jcodes or jcmds:
            now = journal_now()
            if jcodes:
                st["jcodes"] = [e for e in jcodes if jfresh(e, LISTEN_EVERY * 3, now, t)][-JBUF_MAX:]
            if jcmds:
                st["jcmds"] = [e for e in jcmds if jfresh(e, 3.0, now, t)][-JBUF_MAX:]
        if want_codes:
            st["jcodes_due"] = True

    def read_player_lite():
        """Read only who the player is (serial and name), while the companion is dismissed."""
        try:
            P = player()
            return {"serial": int(P.Serial), "name": str(P.Name or ""), "lite": True}
        except Exception:
            return None

    # read_player's memory: the hostile notorieties (looked up once), the player's name (re-read
    # every RP_NAME_EVERY seconds) and the nearest foe in war mode (looked for at most every
    # RP_NEAR_EVERY seconds).
    _rp = {"notos": None, "name_ser": None, "name": "", "name_at": -99.0, "near_at": -99.0, "near": 0}
    RP_NAME_EVERY = 5.0
    RP_NEAR_EVERY = 1.0

    def nearest_foe(now):
        """The nearest hostile mobile within eight tiles, looked for at most once a second."""
        notos = _rp["notos"]
        if notos is None:
            notos = _rp["notos"] = [getattr(API.Notoriety, n) for n in HOSTILE]
        # Between looks the same mobile is returned, while the client still has it.
        if now - _rp["near_at"] < RP_NEAR_EVERY:
            ser = _rp["near"]
            return find_mob(ser) if ser else None
        _rp["near_at"] = now
        mob = API.NearestMobile(notos, 8)
        _rp["near"] = int(mob.Serial) if mob is not None else 0
        return mob

    def read_player():
        """Read the player for the companion, in place (the tick runs on the client thread).

        Returns a dict (serial, position, map, hidden / dead / war flags, hits, casting, gold, name and,
        in war mode, the target) or None when the player or any required read fails. The name is cached
        for a few seconds; the target is the last target if close, else the nearest foe.
        """
        P = player()
        if P is None:
            return None
        now = time.time()
        try:
            ser = int(P.Serial)
            d = {"serial": ser, "x": int(P.X), "y": int(P.Y), "z": int(P.Z),
                 "hidden": bool(P.IsHidden), "dead": bool(P.IsDead), "war": bool(P.InWarMode),
                 "hits": int(P.Hits or 0), "hmax": int(P.HitsMax or 0), "target": None, "name": "",
                 "map": int(API.GetMap()), "casting": bool(P.IsCasting), "gold": int(P.Gold or 0)}
            # The name hardly ever changes, so it is re-read only for a new serial or after RP_NAME_EVERY.
            if ser != _rp["name_ser"] or now - _rp["name_at"] >= RP_NAME_EVERY:
                _rp["name"] = str(P.Name or "")
                _rp["name_ser"], _rp["name_at"] = ser, now
            d["name"] = _rp["name"]
            # Out of war mode there is no target: the nearest-foe cache is dropped so the next war starts
            # with a fresh look.
            if not d["war"]:
                _rp["near_at"] = -99.0
                return d
            mob = None
            lser = int(API.LastTargetSerial or 0)
            if lser and lser != ser:
                mob = find_mob(lser)
                # A last target further than 10 tiles away is not the companion's business.
                if mob is not None and safe(lambda: int(mob.Distance) > 10, True):
                    mob = None
                # It just died: the companion gets its victory.
                if mob is not None and safe(lambda: bool(mob.IsDead), False):
                    d["target"] = {"serial": int(mob.Serial), "dead": True, "name": ""}
                    return d
            if mob is None:
                mob = nearest_foe(now)
            if mob is not None:
                tser, tdead = int(mob.Serial), bool(mob.IsDead)
                d["target"] = {"serial": tser, "dead": tdead, "name": str(safe(lambda: mob.Name, "") or "") or "foe"}
            return d
        except Exception:
            return None

    def comp_sparkle(dur):
        """Queue sparkles on the companion for dur seconds (sent with the tick's one client hop)."""
        c = st["comp"]
        st["hop"].append(fx_fixed(FX_SPARKLE, c["x"], c["y"], c["z"], 0, dur))

    def run_hop():
        """Run every effect and head message queued this tick, then clear the queue.

        Runs on the client thread (the tick and every window build do), so no closure or
        Kit.on_client is needed. One failing effect never stops the others.
        """
        ops = st["hop"]
        if not ops:
            return
        st["hop"] = []
        for f in ops:
            try:
                f()
            except Exception:
                pass

    def fx_fixed(graphic, x, y, z, hue=0, dur=None):
        """Return a callable that creates a fixed-position effect at x, y, z (z clamped to the client's
        signed byte range) for dur seconds, default just over one companion tick.
        """
        dur = COMP_TICK + 0.1 if dur is None else dur
        return lambda: API.CreateEffect(graphic, type=API.EffectType.FixedXYZ, hue=hue,
                                        sourceX=x, sourceY=y, sourceZ=max(-128, min(127, z)), duration=dur)

    def fx_moving(graphic, hue, src=None, dst=None, sxyz=None, txyz=None):
        """Return a callable that creates a moving effect from a source (mobile serial or x, y, z) to a
        target (serial or x, y, z). Duration 0 lets the client work the flight out.
        """
        kw = {"type": API.EffectType.Moving, "hue": hue, "duration": 0}
        if src:
            kw["source"] = src
        if dst:
            kw["target"] = dst
        if sxyz:
            kw["sourceX"], kw["sourceY"], kw["sourceZ"] = sxyz
        if txyz:
            kw["targetX"], kw["targetY"], kw["targetZ"] = txyz
        return lambda: API.CreateEffect(graphic, **kw)

    def comp_command(cmd, t):
        """Carry out one spoken command for the companion: home, follow, stay, speak, dance, kill,
        good, sleep or fetch.

        t is the tick time. A command to a companion that is not out is ignored, except follow, which
        calls it out when the Companion unlock is owned and the pet is not feral.
        """
        c = st["comp"]
        if cmd == "home":
            # The settings page follows the switch.
            set_comp(False)
            comp_say("*waves goodbye and flies home*", True)
            return
        if not c["on"]:
            if cmd == "follow" and has("u_companion") and not pet["feral"]:
                set_comp(True)
                say("%s flutters out to join you." % name(), Kit.HUE_GOOD)
            return
        c["nap"] = False
        if cmd == "follow":
            c["mode"], c["stay"] = "follow", None
            comp_say("*flaps after you*", True)
        elif cmd == "stay":
            c["mode"], c["stay"] = "stay", (c["x"], c["y"])
            comp_say("*hovers in place*", True)
        elif cmd == "speak":
            squeak()
            comp_say(random.choice(LINES["idle"] + pers("lines", [])), True)
        elif cmd == "dance":
            # Tricks have a 20 second cooldown so a spoken dance cannot be spammed for squeaks.
            if t - c["trick_at"] < 20:
                comp_say("*is dizzy from the last one*", True)
                return
            c["trick_at"] = t
            c["trick_until"] = t + 2.0
            bump("joy", 2)
            earn("pet")
            squeak()
            comp_sparkle(1.5)
            comp_say(random.choice(["*does a barrel roll*", "*loop-de-loop!*", "*spins in the air*"]), True)
        elif cmd == "kill":
            # The help timer is cleared, so the dive happens at the next look.
            c["help_at"] = 0.0
            comp_say("*SCREEEECH!*", True, Kit.HUE_BAD)
        elif cmd == "good":
            bump("joy", 3)
            comp_say("*preens proudly*", True)
        elif cmd == "sleep":
            c["nap"] = True
            comp_say("*curls up for a nap*", True)
        elif cmd == "fetch":
            c["fetch_until"] = t + 3.0
            comp_say("*zooms off*", True)

    # Compiled once: one word-bounded pattern per command word.
    CMD_RES = [(re.compile(r"\b%s\b" % _w), _c) for _w, _c in COMMANDS]
    SKILL_RE = re.compile(r"your skill in (.+?) has increased")
    cmd_seen = {}

    def comp_journal(t, me_name):
        """Handle the journal lines queued for the companion: skill gains and spoken pet commands.

        Each journal line arrives once, so nothing is remembered here. Only lines spoken by the player
        (me_name) count as commands; the first command word found wins.
        """
        c = st["comp"]
        if not st["jcmds"]:
            return
        entries, st["jcmds"] = st["jcmds"], []
        if len(entries) > 1:
            # Name lines first, then skill lines (the sort is stable).
            entries.sort(key=lambda e: e[2])
        # low is the Journal's lower case text.
        for text, who, _, low, _ in entries:
            if low.startswith("your skill in") and "increased" in low:
                m = SKILL_RE.search(low)
                got = earn("skill", 3)
                if c["on"]:
                    comp_sparkle(1.2)
                    comp_say("*cheers for your %s!* (+%d squeaks)" % (m.group(1) if m else "skill", int(got)), True)
                continue
            if who != me_name:
                continue
            for rx, cmd in CMD_RES:
                if rx.search(low):
                    comp_command(cmd, t)
                    break

    # The eight tiles around the player, used as hover and trick spots.
    COMP_RING = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    NEED_WORDS = {"sick": "*coughs pitifully*", "hungry": "*tugs your sleeve: hungry*",
                  "dirty": "*sniffs itself... needs a bath*", "bored": "*pokes you: play with me?*"}

    def comp_tick(t):
        """One companion step: follow the player, react, help in combat, chat and draw.

        Runs on the client thread, once per fresh player read and no faster than COMP_TICK. Everything
        that touches the client is queued in ops and sent through st["hop"], so a tick makes one hop.
        """
        c = st["comp"]
        # Once per fresh read: a tick with nothing new to look at costs nothing.
        if t < c["next"] or st["read_at"] <= c.get("read_seen", -1.0):
            return
        c["next"], c["read_seen"] = t + COMP_TICK, st["read_at"]
        info = st.get("player") if (comp_wanted() or has("u_companion")) else None
        if info is None:
            c["on"] = False
            return
        c["serial"] = info["serial"]
        comp_journal(t, info.get("name") or str(safe(lambda: API.Player.Name, "") or ""))
        # Dismissed or lite read: only the name was needed (for the journal).
        if not comp_wanted() or info.get("lite"):
            c["on"] = False
            return
        px, py, pz = info["x"], info["y"], info["z"]
        # First tick, a map change or a long jump (teleport, gate): appear next to the player again.
        if not c["on"] or c["map"] != info["map"] or max(abs(c["x"] - px), abs(c["y"] - py)) > 18:
            c.update({"on": True, "x": px, "y": py + 1, "map": info["map"], "last_p": (px, py),
                      "mode": "follow" if c["mode"] != "stay" or c["map"] != info["map"] else c["mode"]})
            if c["mode"] == "follow":
                c["stay"] = None
            c["hp"], c["gold"] = info["hits"], info["gold"]
            comp_say(random.choice(["*flutters onto your shoulder*", "*squeaks hello*", "*circles you happily*"]), True)
        ops = []
        # -- following --
        moved = c["last_p"] != (px, py)
        if moved:
            lx, ly = c["last_p"]
            dx, dy = (px > lx) - (px < lx), (py > ly) - (py < ly)
            if dx or dy:
                c["dir"] = (dx, dy)
            c["tiles"] += max(abs(px - lx), abs(py - ly))
            c["last_p"] = (px, py)
            c["still_since"] = t
            if c["nap"]:
                c["nap"] = False
                comp_say("*yawns and catches up*")
        if c["mode"] == "stay" and c["stay"]:
            sx, sy = c["stay"]
            if max(abs(sx - px), abs(sy - py)) > 16:
                c["mode"], c["stay"] = "follow", None
                comp_say("*got lonely and flies after you*", True)
            elif t >= c["hover_at"]:
                c["hover_at"] = t + random.uniform(2, 4)
                c["x"], c["y"] = sx + random.randint(-1, 1), sy + random.randint(-1, 1)
        RING = COMP_RING
        # A trick: it circles the player.
        if t < c.get("trick_until", 0.0):
            i = int((t - c["trick_at"]) / COMP_TICK) * 2 % 8
            c["x"], c["y"] = px + RING[i][0], py + RING[i][1]
            ops.append(fx_fixed(FX_SPARKLE, c["x"], c["y"], pz + COMP_Z, 0, 0.8))
        elif c["mode"] == "follow":
            if moved:
                c["x"], c["y"] = px - c["dir"][0], py - c["dir"][1]
            elif t - c["still_since"] > 3 and t >= c["hover_at"]:
                c["hover_at"] = t + random.uniform(3, 6)
                # A neighbouring tile.
                ox, oy = random.choice(RING)
                c["x"], c["y"] = px + ox, py + oy
        # A long stand-still and a tired (or sleeping) pet: the companion lands and dozes.
        if not c["nap"] and t - c["still_since"] > 120 and (pet["energy"] < 60 or pet["asleep"]):
            c["nap"] = True
            comp_say("*lands and dozes off*")
        # The bob alternates the height by one level each tick, so the flight looks alive.
        c["bob"] = 1 - c["bob"]
        c["z"] = z = pz + (0 if c["nap"] or pet["asleep"] else COMP_Z + c["bob"])
        # -- reactions --
        if info["dead"] != c["dead"]:
            c["dead"] = info["dead"]
            if info["dead"]:
                bump("joy", -10)
                comp_say("*wails mournfully*", True, Kit.HUE_BAD)
            else:
                comp_say("*happy flutter! You're back!*", True)
        if info["hidden"] != c["hidden"]:
            c["hidden"] = info["hidden"]
            if info["hidden"]:
                comp_say("*hides with you*", True)
        hp, hmax = info["hits"], max(1, info["hmax"])
        if c["hp"] is not None and not info["dead"]:
            if c["hp"] - hp >= hmax * 0.10:
                comp_say(random.choice(["*worried squeak*", "*hisses at your attacker*", "*flaps anxiously*"]))
            # Compassion shortens the heal cooldown.
            if hp < hmax * 0.30 and t - c["panic_at"] > COMP_HEAL_SECS - VIRTUE_FX["com_heal_secs"] * vlevel("com"):
                c["panic_at"] = t
                ops.append(fx_fixed(FX_HEAL, px, py, pz, 0, 1.5))
                comp_say("*licks your wounds* (it's the thought that counts)", True)
        c["hp"] = hp
        # Spirituality raises the chance of copying a spell.
        if info["casting"] and not c["casting"] \
                and random.random() < COMP_COPY_CHANCE + VIRTUE_FX["spi_copy"] * vlevel("spi"):
            ops.append(fx_fixed(FX_SPARKLE, c["x"], c["y"], z, 0, 1.0))
            comp_say(random.choice(["*wiggles its wings mystically*", "*squeaks along: Kal Ort*",
                                    "*copies your spell, badly*"]))
        c["casting"] = info["casting"]
        if c["gold"] is not None and info["gold"] > c["gold"] and random.random() < 0.3:
            comp_say("*eyes your gold* Shiny!")
        c["gold"] = info["gold"]
        if c["tiles"] >= 60:
            c["tiles"] -= 60
            bump("joy", 1)
            bump("energy", -1)
            earn("walk", 1)
            chance = 0.06 * (2 if has("u_shiny") else 1)
            if random.random() < chance:
                got = earn("shiny", random.randint(5, 15))
                ops.append(fx_fixed(FX_SPARKLE, c["x"], c["y"], z, 0, 1.0))
                comp_say("*found something shiny!* (+%d squeaks)" % int(got), True)
                sound(SND_FOOD)
        # -- combat --
        tgt = info["target"]
        if info["war"] != c["war"]:
            c["war"] = info["war"]
            comp_say("*bares its tiny fangs*" if info["war"] else "*settles down*")
        if c["target"] and (tgt is None or tgt["serial"] != c["target"]["serial"] or tgt["dead"]):
            if tgt is not None and tgt["serial"] == c["target"]["serial"] and tgt["dead"]:
                earn("victory", 2)
                bump("joy", 2)
                comp_say("*victory squeak!*", True)
            c["target"] = None
        if tgt is not None and not tgt["dead"] and info["war"] and settings["comp_help"] \
                and not info["dead"] and not pet["asleep"] and c["dive"] is None:
            c["target"] = tgt
            if t >= c["help_at"]:
                lo, hi = (4, 8) if has("u_war") else (8, 15)
                # Valor shortens the wait between dives.
                c["help_at"] = t + random.uniform(lo, hi) * (1.0 - VIRTUE_FX["val_dive"] * vlevel("val"))
                c["dive"] = {"t": t, "serial": tgt["serial"], "back": False}
                lk = own_look()
                # The dive is drawn as a moving effect of the pet's body to the target, and back at 0.7 seconds.
                ops.append(fx_moving(body_gfx(lk["stage"]), lk["hue"], dst=tgt["serial"], sxyz=(c["x"], c["y"], z)))
                if has("u_war") and random.random() < 0.5:
                    ops.append(fx_moving(FX_BOLT, 0, dst=tgt["serial"], sxyz=(c["x"], c["y"], z)))
                hit = random.choice(["*bonk!*", "*nibble!*", "*SCREECH*", "*wing slap!*", "*dive-bomb!*"])
                ops.append(lambda: API.HeadMsg(hit, tgt["serial"], Kit.HUE_BAD))
        dv = c["dive"]
        if dv is not None:
            if not dv["back"] and t - dv["t"] >= 0.7:
                dv["back"] = True
                lk = own_look()
                ops.append(fx_moving(body_gfx(lk["stage"]), lk["hue"], src=dv["serial"], txyz=(c["x"], c["y"], z)))
            if t - dv["t"] >= 1.4:
                c["dive"] = None
        # -- needs and chatter --
        a = [k for k in alert_keys() if k != "grem"]
        if a and t - c["need_at"] > 300:
            c["need_at"] = t
            word = NEED_WORDS.get(a[0], "*squeaks*")
            comp_say(word, True, Kit.HUE_BAD)
        elif t >= c["chat_at"]:
            c["chat_at"] = t + random.uniform(40, 90) / max(0.2, pers("chat", 1.0))
            if not c["nap"] and not pet["asleep"]:
                comp_say(random.choice(LINES["idle"] + pers("lines", []) * 2))
        # -- draw --
        fetching = t < c["fetch_until"]
        if c["fetch_until"] and not fetching:
            c["fetch_until"] = 0.0
            if random.random() < 0.25:
                got = earn("shiny", random.randint(3, 10))
                comp_say("*brings you something shiny!* (+%d squeaks)" % int(got), True)
            else:
                comp_say(random.choice(["*brings you a stick*", "*brings you a bone*",
                                        "*brings back... a gremlin's sock?*"]), True)
        # Hidden, fetching or diving: the companion is not drawn this tick, only the queued effects go.
        if info["hidden"] or fetching or c["dive"] is not None:
            st["hop"].extend(ops)
            return
        lk = own_look()
        if info["dead"]:
            # A copy, so the shared look stays as it is.
            lk = dict(lk)
            # Ghostly, like the player.
            lk["hue"] = HUE_WHITE
        cx, cy = c["x"], c["y"]
        aura = BY_ID.get(lk["aura"] or "")
        if aura:
            if aura.get("seq"):
                # A sequence aura repeats once a second; a plain aura is drawn every tick.
                if t >= c["aura_at"]:
                    c["aura_at"] = t + 1.0
                    hue = random.choice(RAINBOW) if aura.get("rainbow") else aura["hue"]
                    ops.append(fx_fixed(aura["seq"][0], cx, cy, z - 1, hue, 1.05))
            else:
                ops.append(fx_fixed(aura["gfx"], cx, cy, z - 1, aura["hue"]))
        ops.append(fx_fixed(body_gfx(lk["stage"]), cx, cy, z, lk["hue"]))
        # Neck and hat sit at stage-dependent heights over the body.
        for k, dz in (("neck", NECK_DZ), ("hat", HAT_DZ)):
            it = BY_ID.get(lk[k] or "")
            if it:
                ops.append(fx_fixed(it["gfx"], cx, cy, z + dz[lk["stage"]], it["hue"]))
        st["hop"].extend(ops)

    def want_redraw():
        """Ask the window thread to redraw the main window at its next pass."""
        st["redraw"] = True

    def on_disposed(which, g):
        """Return the handler for a gump's disposal: when the player closes the window, forget it.

        The main window going away switches the module off; a sub-window just marks itself closed.
        Nothing happens during shutdown or when the gump was already replaced.
        """
        def handler(*args):
            """Gump disposed callback (any arguments): clear the holder and the open flag."""
            w = wins[which]
            if w["g"] is g and not st["shutting"]:
                w["g"] = None
                if which == "main":
                    HOST.disable(KEY)
                else:
                    st[which + "_open"] = False

        return handler

    def item_pic(g, v, graphic, x, y, w, h, hue=0, shown=True):
        """Add a picture of an item graphic to gump g and register it with view v. The picture ignores the mouse
        so clicks fall through to what is under it.
        """
        p = G.CreateGumpItemPic(graphic, w, h)
        p.SetPos(x, y)
        if hue:
            p.Hue = hue
        if not shown:
            p.IsVisible = False
        # Plain pictures, never clickable: the pen's click areas sit over them.
        p.SetAcceptMouseInput(False)
        g.Add(p)
        v.reg(p, gfx=graphic, hue=hue, vis=shown, pos=(int(x), int(y)), size=(int(w), int(h)))
        return p

    GREM_RECTS = [(25, 0, 3, 3), (24, 2, 1, 2), (21, 3, 1, 4), (22, 3, 1, 3), (23, 3, 1, 2), (20, 4, 1, 4),
                  (18, 5, 4, 2), (15, 6, 7, 1), (14, 7, 2, 2), (19, 7, 1, 11), (12, 8, 4, 1), (10, 9, 3, 1),
                  (10, 10, 2, 1), (9, 11, 2, 1), (7, 12, 1, 4), (8, 12, 2, 1), (8, 13, 1, 1), (6, 14, 2, 2),
                  (4, 15, 16, 1), (4, 16, 2, 1), (20, 16, 1, 2), (3, 17, 1, 4), (4, 17, 1, 1), (21, 17, 1, 4),
                  (7, 18, 1, 1), (16, 18, 1, 1), (2, 19, 2, 2), (1, 20, 1, 4), (22, 20, 1, 4), (2, 22, 1, 2),
                  (3, 23, 1, 2), (7, 23, 10, 1), (21, 23, 1, 2), (4, 24, 1, 3), (19, 24, 1, 3), (20, 24, 1, 2),
                  (5, 25, 1, 2), (6, 26, 14, 1), (6, 27, 1, 3), (7, 27, 1, 1), (16, 27, 3, 1), (5, 28, 2, 2),
                  (17, 28, 2, 1), (4, 29, 1, 2), (18, 29, 2, 1), (0, 30, 5, 1), (19, 30, 6, 1)]

    def make_gremlin(g, v, c, x, y):
        """Build the gremlin: an empty holder box with one colour box per stroke inside, so moving or hiding
        the holder moves or hides the whole drawing. The strokes are kept in c["grem_kids"].
        """
        box = G.CreateGumpColorBox(0.0, "#000000")
        box.SetRect(int(x), int(y), GR_W, GR_H)
        box.SetAcceptMouseInput(False)
        box.IsVisible = False
        g.Add(box)
        kids = []
        for rx, ry, rw, rh in GREM_RECTS:
            b = G.CreateGumpColorBox(1.0, GREMLIN_COLOR)
            b.SetRect(rx * GREM_PX, ry * GREM_PX, rw * GREM_PX, rh * GREM_PX)
            box.Add(b)
            kids.append(b)
        v.reg(box, vis=False, pos=(int(x), int(y)), size=(GR_W, GR_H))
        c["grem_kids"], c["grem_k"] = kids, 1.0
        return box

    def gremlin_scale(c, k):
        """Redraw the gremlin's strokes at k times its size (the trap shrinks it).

        Moves are queued by the client, so this does not wait. Does nothing when k is unchanged.
        """
        k = round(k, 2)
        if c.get("grem_k") == k:
            return
        c["grem_k"] = k
        # The pen's own scale applies too.
        s = GREM_PX * k * c.get("pen_k", 1.0)
        for b, (rx, ry, rw, rh) in zip(c.get("grem_kids", []), GREM_RECTS):
            x0, y0 = int(round(rx * s)), int(round(ry * s))
            x1, y1 = int(round((rx + rw) * s)), int(round((ry + rh) * s))
            # Every tick of the trap animation, so a plain try rather than a lambda.
            try:
                b.SetRect(x0, y0, max(1, x1 - x0), max(1, y1 - y0))
            except Exception:
                pass

    def label(g, v, text, x, y, hue=None):
        """Add a text label to gump g and register it with view v (so a zone redraw can move it)."""
        lbl = Kit.add_label(g, text, x, y, hue)
        v.reg(lbl, text=text, thue=hue, pos=(int(x), int(y)))
        return lbl

    CLOSE_SUB = "Close"

    def title_bar(g, store, which, w, title, extra=None, dock=False, close_tip=CLOSE_SUB):
        """Build the title section: name, captioned buttons from extra, Minimize and Close, and with dock
        the gold Fold into the Action Bar arrow.

        extra holds (key, art, caption, tooltip) rows. close_tip is the Close button's tooltip.
        Clicks are queued as (which, key) for the window loop.
        """
        Kit.add_section(g, M, M, w - 2 * M, 30)
        x = w - M - 84 - (Kit.DOCK_DX if dock else 0)
        room = x - (M + 30 + Kit.text_w(title.upper()) + 6)
        need = sum(35 + Kit.text_w(cap) + 6 for _, _, cap, _ in (extra or []))
        # Too tight for captions: every button goes bare (all of them, never some).
        bare = need > room
        x_end = (x - sum((30 if bare else 35 + Kit.text_w(cap)) + 6 for _, _, cap, _ in (extra or [])))
        shown = title.upper()
        # Still too tight: the title is cut to fit.
        if Kit.text_w(shown) > x_end - 6 - (M + 30):
            shown = Kit.fit(shown, max(8, x_end - 6 - (M + 30)))
        Kit.add_label(g, shown, M + 30, M + 7, Kit.HUE_TITLE)
        for key, art, cap, tip in reversed(extra or []):
            x -= 30 if bare else 35 + Kit.text_w(cap)
            # A bare button keeps its caption as the first words of its tooltip (the UI text standard).
            Kit.art_button(g, store, key, art, x, M + 4, None if bare else cap,
                           Kit.caption_tip(cap, tip) if bare else tip, on_click=queue((which, key)))
            x -= 6
        # A window in a zone is always up: it has no buttons of its own, only a strip to drag by.
        if Kit.zone_up(dock_key(which)):
            strip = Kit.catcher(g, M, M, max(20, x - M - 6), 30, lambda *a: None, None, movable=True)
            if shown != title.upper():
                Kit.with_tip(strip, title)
            return
        strip = Kit.title_catcher(g, M, M, max(20, x - M - 6), 30, queue((which, "toggle_min")), key=KEY + which)
        if shown != title.upper():
            Kit.with_tip(strip, "%s. %s" % (title, Kit.DOUBLE_TIP))
        if dock:
            Kit.dock_button(g, store, w - M - 74, M + 7, on_click=queue((which, "to_bar")))
        Kit.art_button(g, store, "min", Kit.ART_MIN, w - M - 74, M + 7, None, Kit.MIN_TIP,
                       on_click=queue((which, "toggle_min")))
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, close_tip)

    def mini_bar(g, store, which, title, close_tip=CLOSE_SUB, w=None):
        """Build the minimized bar of a window."""
        return Kit.mini_bar(g, store, w or MINI_W, MINI_H, title, KEY + which, queue((which, "toggle_min")),
                            close_tip=close_tip)

    def dock_key(which):
        """Return the dock key of a window: the module key for the main window, a sub-key for the others."""
        return KEY if which == "main" else KEY + "." + which

    def sub_min(which):
        """Return the smallest (width, height) the sub-window needs."""
        if which == "shop":
            return SW, M + 30 + GAP + 30 + GAP + shop_layout(shop_cats())[1] + GAP + 8 + 3 * 38 + 30 + M
        return {"pen": (PPW, PPH), "quest": (JW, JH), "ach": (ACH_W, ACH_H)}[which]

    def sub_size(which, nw, nh):
        """Return the size to build a sub-window at: the zone's fitted size when it is in a zone, open and
        big enough, else the asked size (nw, nh).
        """
        z = subfit.get(which)
        mw, mh = sub_min(which)
        if z is None or not Kit.zone_up(dock_key(which)) or st[which + "_min"] or z[0] < mw or z[1] < mh:
            return nw, nh
        return z

    def sub_hooks(which):
        """Return the hooks the dock uses to drive one sub-window (title, icon, state, show, minimize,
        gump, redraw, fit, min).
        """
        holder = wins[which]

        def state():
            """Return the window state for the dock: None when closed, else minimized or open."""
            if holder["g"] is None or st["shutting"]:
                return None
            return "minimized" if st[which + "_min"] else "open"

        def show():
            """Open the sub-window (a closed playpen starts its shared-view timer) and ask for a redraw."""
            if which == "pen" and not st["pen_open"]:
                st["shared_at"] = time.time()
            st[which + "_min"] = False
            st[which + "_open"] = st[which + "_redraw"] = True

        def minimize():
            """Minimize the sub-window at the next redraw."""
            st[which + "_min"] = st[which + "_redraw"] = True

        def redraw():
            """Ask for a redraw of the sub-window."""
            st[which + "_redraw"] = True

        def fit_to(w, h, mode):
            """Fit the sub-window to a zone slot of w x h, or to its own size when w or h is None.
            Redraws when the size changed, or when mode is again with a size.
            """
            new = (int(w), int(h)) if (w is not None and h is not None) else None
            if new != subfit.get(which) or (mode == "again" and new is not None):
                subfit[which] = new
                redraw()

        return {"title": TITLE + " " + SUBS[which], "icon": TRAY_ICON, "state": state, "show": show,
                "minimize": minimize, "gump": lambda: holder["g"], "redraw": redraw, "fit": fit_to,
                "min": lambda: sub_min(which), "exact": True}

    def open_window(which, build, w, h, max_h=None, hidden=False):
        """Build and show one of the module's windows (common start and end).

        build(g, store, c, v) draws into a fresh gump; w x h is its size, max_h the zone's height (taller
        than it, the body scrolls) and hidden starts it unseen. The new gump replaces the old one, which
        is disposed last so the screen never shows a gap. The place comes from the layout manager when
        it holds the window, else from the open window or the saved position.
        """
        holder = wins[which]
        key = dock_key(which)
        # The saved place, or the live place when the window is already open.
        x, y = Kit.load_pos(POS_KEYS[which], POS_DEFAULTS[which], (w, h))
        if Kit.is_open(holder["g"]):
            x, y = holder["g"].GetX(), holder["g"].GetY()
        # The layout manager's remembered spot for this window, only while it holds this zone's windows.
        at = LAYOUT.spot(key) if HOST.layout_holds(key) else None
        if at is not None:
            x, y = int(at[0]), int(at[1])
        # The old gump is kept until the new one is up.
        old, holder["g"] = holder["g"], None
        store, c, v = ({}, {}), {}, View()
        g = G.CreateGump(True, True)
        build(g, store, c, v)
        xy = Kit.show_window(g, x, y, w, h, key, hidden, on_disposed(which, g), lambda: save_pos(which), holder,
                             {"g": g, "c": c, "store": store, "v": v}, max_h)
        # The client moved it to keep it wholly on screen: hold the zone's place and tell the layout.
        if at is not None and xy is not None and tuple(xy) != (x, y):
            g.SetPos(x, y)
            Kit.note_rect(g, x, y)
            Kit.moved_by_code(g)
        if at is not None:
            LAYOUT.fit_now(key, g)
        Kit.dispose(old)

    def open_sub(which, title, build, w, h):
        """Open a sub-window as its full build, or as its minimized bar when it was left minimized."""
        if not st[which + "_min"]:
            return open_window(which, build, w, h)

        def build_mini(g, store, c, v):
            """Build the minimized bar of the sub-window."""
            c["mini"] = mini_bar(g, store, which, title)

        open_window(which, build_mini, MINI_W, MINI_H)

    def close_window(which):
        """Close the shop, playpen or a dev window: its place is saved and st[which + "_open"] goes off."""
        holder = wins[which]
        save_pos(which)
        g, holder["g"] = holder["g"], None
        Kit.dispose(g)
        st[which + "_open"] = False

    # Pixel sizes of the item art the pet's pieces use, so a picture can be squeezed to a fraction of
    # its real size without asking the client. Unlisted art counts as 40 x 40 (see dims).
    ART_DIMS = {0x021B: (7, 7), 0x0970: (17, 11), 0x097B: (12, 8), 0x097E: (16, 17), 0x09C0: (14, 15), 0x09C8: (12, 14),
        0x09C9: (18, 14), 0x09D0: (7, 9), 0x09D1: (9, 10), 0x09E9: (23, 25), 0x09EA: (9, 9), 0x09EC: (13, 17),
        0x09F0: (13, 17), 0x09F2: (18, 16), 0x0A15: (13, 26), 0x0A1A: (13, 26), 0x0B1D: (21, 39), 0x0C5C: (17, 15),
        0x0C6A: (16, 15), 0x0C74: (10, 10), 0x0C77: (24, 25), 0x0C83: (42, 55), 0x0C9F: (60, 51), 0x0D0C: (15, 24),
        0x0D25: (36, 52), 0x0DDA: (37, 88), 0x0E1D: (14, 14), 0x0E2D: (13, 20), 0x0E73: (10, 10), 0x0E9C: (33, 32),
        0x0E9D: (16, 14), 0x0EB2: (22, 29), 0x0EB3: (22, 18), 0x0F07: (9, 17), 0x0F3B: (22, 19), 0x0F6C: (37, 88),
        0x0F83: (9, 15), 0x0FA7: (12, 17), 0x103B: (17, 15), 0x1047: (21, 39), 0x1085: (11, 11), 0x1088: (9, 10),
        0x1089: (10, 20), 0x108B: (20, 12), 0x10F7: (19, 23), 0x11CA: (38, 62), 0x11EA: (36, 34), 0x1373: (16, 17),
        0x13C7: (15, 12), 0x1413: (17, 11), 0x153F: (15, 9), 0x1543: (11, 15), 0x1549: (20, 21), 0x1713: (19, 17),
        0x1714: (17, 13), 0x1715: (12, 12), 0x1716: (21, 22), 0x1717: (20, 17), 0x1718: (18, 17), 0x1719: (12, 13),
        0x171A: (17, 16), 0x171B: (16, 17), 0x171C: (23, 11), 0x171F: (15, 13), 0x172E: (30, 26), 0x1BD1: (8, 8),
        0x1F0A: (10, 20), 0x2123: (21, 11), 0x20F9: (19, 42), 0x25A6: (51, 44), 0x2627: (38, 40), 0x2805: (24, 25),
        0x2832: (15, 45), 0x2833: (24, 42), 0x2B6F: (14, 12), 0x2B70: (12, 10), 0x1041: (21, 13), 0x2BE1: (14, 18),
        0x2BDD: (10, 22), 0x1F7D: (7, 13), 0x141B: (18, 19), 0x1545: (21, 22), 0x1547: (22, 26)}
    # Where hats and necklaces sit on the body, as a fraction of its height, per growth stage.
    HAT_FRAC = {0: -0.10, 1: 0.14, 2: 0.14}
    NECK_FRAC = {0: 0.31, 1: 0.61, 2: 0.61}
    # Effect art for the sprites: (first frame, frame count).
    SPR_SPARKLE = (0x376A, 15)
    SPR_HEAL = (0x373A, 16)
    SPR_POOF = (0x3728, 13)
    SPR_STARS = (0x375A, 16)
    SPR_MOTES = (0x377A, 15)
    PARTS_MAX, SPRITES_MAX = 8, 3

    def dims(gfx):
        """Return the art size (width, height) of a graphic."""
        return ART_DIMS.get(gfx, (40, 40))

    def body_gfx(stage):
        """Return the body art for a growth stage: the pup or the adult."""
        return GFX_PUP if stage == 0 else GFX_ADULT

    def anim(kind, dur):
        """Start (or restart) a one-shot animation of this kind for dur seconds."""
        st["anims"][kind] = {"t0": time.time(), "dur": dur}

    def anim_at(kind, t):
        """Return (animation, progress 0 to 1) while the animation runs, else (None, 0.0)."""
        a = st["anims"].get(kind)
        if a is not None and t - a["t0"] < a["dur"]:
            return a, (t - a["t0"]) / a["dur"]
        return None, 0.0

    def particle(text, hue, x, y, vx=0.0, vy=-20.0, dur=1.6, view="main"):
        """Queue a floating text for a pen view; the oldest goes when the list is full (PARTS_MAX)."""
        lst = st["parts"][view]
        if len(lst) >= PARTS_MAX:
            lst.pop(0)
        lst.append({"text": text, "hue": hue, "x": float(x), "y": float(y), "vx": vx, "vy": vy,
                    # The width is measured once here, so drawing never measures. No label is made: the pool owns them.
                    "t0": time.time(), "dur": dur, "w": Kit.text_px(text)})

    def sprite(seq, x, y, dur=1.0, hue=0, size=56, view="main"):
        """Queue an effect-art sprite run for a pen view; the oldest goes when the list is full."""
        lst = st["sprites"][view]
        if len(lst) >= SPRITES_MAX:
            lst.pop(0)
        lst.append({"seq": seq, "x": float(x), "y": float(y), "t0": time.time(), "dur": dur, "hue": hue, "size": size})

    def pet_xy():
        """Return the top centre of the pet in the main pen, where its particles start."""
        return st["px"] + PB_W / 2.0, st["py"] + 4

    def pet_particle(text, hue, dx, dy, vx, vy, dur):
        """Queue a floating text that starts at an offset from the pet."""
        x, y = pet_xy()
        particle(text, hue, x + dx, y + dy, vx, vy, dur)

    def pop_text(text, hue, dx=0, vy=-20.0, dur=1.6):
        """Pop a short floating text over the pet, with a little random sideways drift."""
        x, y = pet_xy()
        particle(text, hue, x + dx, y, random.uniform(-6, 6), vy, dur)

    def draw_pool(v, c, view, t, x0, y0, w, h):
        """Draw one pen's floating texts and sparkle runs through the pool of pre-made controls.

        Only the pool entries in use, or in use last time (to hide them), are looked at: the rest are
        hidden already. Text and sprites are clamped inside the pen rectangle x0, y0, w, h.
        """
        parts, sprs = st["parts"][view], st["sprites"][view]
        # A fresh window has no record yet: every pooled control is looked at once.
        last = c.get("pool_n", (len(c["plbl"]), len(c["spr"])))
        # Nothing live and nothing to hide: the usual case costs one comparison.
        if not parts and not sprs and last == (0, 0):
            return
        # The lists are rebuilt only when one of their entries has run out.
        if parts:
            for e in parts:
                if t - e["t0"] >= e["dur"]:
                    parts = st["parts"][view] = [p for p in parts if t - p["t0"] < p["dur"]]
                    break
        if sprs:
            for e in sprs:
                if t - e["t0"] >= e["dur"]:
                    sprs = st["sprites"][view] = [s for s in sprs if t - s["t0"] < s["dur"]]
                    break
        c["pool_n"] = (len(parts), len(sprs))
        n = max(len(parts), last[0])
        for i, lbl in enumerate(c["plbl"]):
            if i >= n:
                break
            if i < len(parts):
                p = parts[i]
                age = t - p["t0"]
                # A small sine sway makes the text wobble as it floats.
                x = clamp(p["x"] + p["vx"] * age + 2 * math.sin(age * 6 + i) - p["w"] / 2.0,
                          x0 + 4, x0 + w - 4 - p["w"])
                y = clamp(p["y"] + p["vy"] * age, y0 + 20, y0 + h - 16)
                v.text(lbl, p["text"], p["hue"])
                v.move(lbl, x, y)
                v.show(lbl, True)
            else:
                v.show(lbl, False)
        n = max(len(sprs), last[1])
        for i, pic in enumerate(c["spr"]):
            if i >= n:
                break
            if i < len(sprs):
                s = sprs[i]
                start, frames = s["seq"]
                f = min(frames - 1, int((t - s["t0"]) / s["dur"] * frames))
                sz = s["size"]
                v.look(pic, start + f, s["hue"])
                v.size(pic, sz, sz)
                v.move(pic, clamp(s["x"] - sz / 2.0, x0 + 2, x0 + w - 2 - sz),
                       clamp(s["y"] - sz / 2.0, y0 + 2, y0 + h - 2 - sz))
                v.show(pic, True)
            else:
                v.show(pic, False)

    def make_pool(g, v, x0, y0):
        """Make the pen's sparkle pictures and text labels (hidden, on top of everything); return both lists."""
        spr = [item_pic(g, v, SPR_SPARKLE[0] + 1, x0, y0, 56, 56, shown=False) for _ in range(SPRITES_MAX)]
        lbls = []
        for _ in range(PARTS_MAX):
            lbl = label(g, v, "", x0 + 8, y0 + 24, Kit.HUE_TEXT)
            lbl.IsVisible = False
            v.reg(lbl, text="", vis=False, pos=(x0 + 8, y0 + 24))
            lbls.append(lbl)
        return spr, lbls

    def scaled_box(ctrl_v, ctrl, gfx, cx, cy, k, native):
        """Draw ctrl's art centred on (cx, cy): at its native box when k is 1 or more, squeezed to k of its
        real art size when k is below 1.
        """
        if k >= 0.999:
            bw, bh = native
        else:
            dw, dh = dims(gfx)
            bw, bh = max(1, int(dw * k)), max(1, int(dh * k))
        ctrl_v.size(ctrl, bw, bh)
        ctrl_v.move(ctrl, cx - bw / 2.0, cy - bh / 2.0)

    def make_doll(g, v, x, y):
        """Make the dressed-up pet (aura, body, necklace, hat) at x, y and return its pieces in a dict.
        Used by the main pen and the playpen.
        """
        return {"aura": item_pic(g, v, 0x3740, x - 10, y - 8, PB_W + 20, PB_H + 14, shown=False),
             "pet": item_pic(g, v, GFX_ADULT, x, y, PB_W, PB_H),
             "neck": item_pic(g, v, 0x1088, x, y + 22, PB_W, 14, shown=False),
             "hat": item_pic(g, v, 0x1718, x, y - 3, PB_W, 22, shown=False)}

    def flap_pose(t, rate, phase=0.0, stage=1, depth=1.0):
        """Return the pose of beating wings: the box narrows and widens and the body bobs with it."""
        s = abs(math.cos(t * rate + phase))
        # The pup's wings are folded: it only bobs.
        if stage == 0:
            return {"sx": 1.0, "sy": 0.94 + 0.06 * s, "ox": 0.0, "oy": 2.0 - 4.0 * s}
        return {"sx": 1.0 - 0.30 * depth * (1 - s), "sy": 1.0, "ox": 0.0, "oy": 2.5 - 5.0 * s * depth}

    def sleep_pose(t, phase=0.0):
        """Return the pose of a sleeping pet: narrow and gently breathing."""
        return {"sx": 0.62, "sy": 0.93 + 0.05 * math.sin(t * 1.7 + phase), "ox": 0.0, "oy": 0.0}

    POSE_REST = {"sx": 1.0, "sy": 1.0, "ox": 0.0, "oy": 0.0}
    DOLL_PARTS = (("neck", NECK_FRAC, (PB_W, 14)), ("hat", HAT_FRAC, (PB_W, 22)))

    def place_doll(v, d, cx, cy, lk, t, pose=None, shown=True):
        """Draw the pet and its aura, necklace and hat centred on (cx, cy) for look lk at time t.

        pose scales and offsets the body (sx, sy, ox, oy, k, hue); shown False hides every piece. Moves
        go through the view v, which skips the client call when nothing changed.
        """
        if not shown:
            for k in ("aura", "pet", "neck", "hat"):
                v.show(d[k], False)
            return
        pose = pose or POSE_REST
        cx, cy = cx + pose.get("ox", 0.0), cy + pose.get("oy", 0.0)
        # Overall size: shrinking away or growing.
        k = pose.get("k", 1.0)
        sx, sy = pose["sx"] * k, pose["sy"] * k
        stage = lk["stage"]
        gfx = body_gfx(stage)
        aw, ah = dims(gfx)
        hue = pose.get("hue")
        v.look(d["pet"], gfx, lk["hue"] if hue is None else hue)
        # Full size: the control keeps its native box, so there is no scaling blur.
        if sx >= 0.999 and sy >= 0.999:
            bw, bh = PB_W, PB_H
            art_h = ah
        else:
            bw = aw if sx >= 0.999 else max(1, int(aw * sx))
            bh = ah if sy >= 0.999 else max(1, int(ah * sy))
            art_h = bh
        v.size(d["pet"], bw, bh)
        v.move(d["pet"], cx - bw / 2.0, cy - bh / 2.0)
        v.show(d["pet"], True)
        a = BY_ID.get(lk["aura"] or "")
        if a:
            if a.get("seq"):
                start, n = a["seq"]
                agfx = start + int(t * 6) % n
            else:
                agfx = a["gfx"]
            ahue = RAINBOW[int(t * 2.5) % len(RAINBOW)] if a.get("rainbow") else a["hue"]
            v.look(d["aura"], agfx, ahue)
            # The aura is a little bigger than the body and shrinks with it.
            aw2, ah2 = int((PB_W + 20) * min(1.0, k)), int((PB_H + 14) * min(1.0, k))
            v.size(d["aura"], max(1, aw2), max(1, ah2))
            v.move(d["aura"], cx - aw2 / 2.0, cy - ah2 / 2.0)
        v.show(d["aura"], a is not None)
        # Hats and necklaces hang off the top of the art as drawn, so they follow a squeeze.
        top = cy - art_h / 2.0
        for key, frac, native in DOLL_PARTS:
            it = BY_ID.get(lk[key] or "")
            if it:
                v.look(d[key], it["gfx"], it["hue"])
                scaled_box(v, d[key], it["gfx"], cx, top + frac[stage] * art_h, k, native)
            # Too small to read: the extras vanish before the body does.
            v.show(d[key], it is not None and k > 0.25)

    def pen_pieces(g, c, v):
        """Make the pen's pieces in the pen's own pixels (the pen at PX0, PY0, PW x PH).

        Decor, pantry, heaps, the night, the pet, props, the gremlin, snow, the particle pool, the speech
        label and the click areas, in drawing order. In a zone the window moves them through its View
        transform (v.xf).
        """
        c["decor"] = item_pic(g, v, 0x11CA, PX0 + PW - 50, PY0 + PH - 58, 46, 56, shown=False)
        c["hang"] = item_pic(g, v, 0x0A15, PX0 + PW - 48, PY0 + 20, 44, 40, shown=False)
        c["pantry"] = []
        for i in range(PANTRY_SHOW):
            gfx = FOODS[i % len(FOODS)][0]
            c["pantry"].append(item_pic(g, v, gfx, PX0 + 4 + i * 11, PY0 + PH - 38 + (i % 2) * 3, 44, 34,
                                        shown=i < pet["pantry"]))
        c["mess"] = [item_pic(g, v, GFX_MESS, PX0 + 84 + i * 44, PY0 + PH - 28, 44, 24,
                              shown=i < pet["messes"]) for i in range(MESS_MAX_N)]
        # The night shade is made at its current strength, so a redraw does not flash.
        na = st.get("night_a", 0.55 if pet["asleep"] else 0.0)
        c["night"] = Kit.add_box(g, PX0, PY0, PW, PH, max(0.0, na), "#000010")
        if c["night"] is not None:
            v.reg(c["night"], vis=True, alpha=round(na, 2), pos=(PX0, PY0), size=(PW, PH))
        c["doll"] = make_doll(g, v, int(st["px"]), int(st["py"]))
        c["prop"] = item_pic(g, v, 0x0E1D, PX0, FLOOR_Y, 44, 34, shown=False)
        c["grem"] = make_gremlin(g, v, c, GX_START, GR_Y)
        c["prop2"] = item_pic(g, v, 0x09D0, PX0, FLOOR_Y, 44, 34, shown=False)
        # Winter only: snow is made with the pen.
        if "winter" in (st["seasons"] or ()):
            make_snow(g, v, c)
        c["spr"], c["plbl"] = make_pool(g, v, PX0, PY0)
        c["say"] = label(g, v, "", PX0 + 8, PY0 + 24, Kit.HUE_TEXT)
        # The click areas come last so they sit on top of the pictures.
        c["pet_hit"] = Kit.catcher(g, int(st["px"]), int(st["py"]), PB_W, PB_H, queue("pet"), "Pet " + name())
        v.reg(c["pet_hit"], vis=True, pos=(int(st["px"]), int(st["py"])), size=(PB_W, PB_H))
        c["grem_hit"] = hit = Kit.catcher(g, GX_START, GR_Y, GR_W, GR_H, queue("swat"),
                                          "Swat it before it reaches the pantry (it takes half the food)")
        hit.IsVisible = False
        v.reg(hit, vis=False, pos=(GX_START, GR_Y), size=(GR_W, GR_H))

    # The pen is never drawn below half size; a shorter zone scrolls instead.
    PEN_MIN_K = 0.5
    # The pen's title strip (its name and pantry) stays at full size.
    PEN_HEAD = 26
    ACTS = [("feed", Kit.ART_PLAY, "Feed", "Give one food from the pantry"),
            ("play", Kit.ART_PLAY, "Play", "Play with its toy: happier, a bit tired"),
            ("brush", Kit.ART_PLAY, "Brush", "Brush it: happier, cleaner, a few squeaks"),
            ("clean", Kit.ART_PLAY, "Clean", "Tidy the pen and its heaps"),
            ("lights", Kit.ART_PAGE, "Lights", "Put it to bed, or wake it up"),
            ("cure", Kit.ART_PLAY, "Cure", "Give a Cure potion when it is sick"), ("forage", Kit.ART_PLAY, "Forage",
             "Send it to find food (leaves the pantry unguarded)"),
            ("shop", Kit.ART_PAGE, "Shop", "Spend squeaks on treats, clothes and more"),
            ("playpen", Kit.ART_PAGE, "Playpen", "Open the pen for other players' mongotchis"),
            ("journey", Kit.ART_PAGE, "Journeys", "Open treasure hunts and meditation"),
            ("ach", Kit.ART_PAGE, "Achievements", "Open milestones that pay squeaks once")]

    def act_col_w():
        """Return the width of one action column: the widest button plus its gap."""
        return max(35 + Kit.text_w(cap) for _, _, cap, _ in ACTS) + 12

    def zone_min_w():
        """Return the narrowest zone width laid out: two columns of actions."""
        return 2 * M + 24 - 12 + 2 * act_col_w()

    def zone_geom(w, h):
        """Work out every place of the zone layout for a w x h slot (layout pixels).

        h None asks for the height it needs (the pen at its own shape at this width). Returns a dict with
        the pen, stats and action rectangles, the pen scale k and whether the body scrolls.
        """
        IWz = w - 2 * M
        Z = {"w": w, "IW": IWz, "top": M + 30 + GAP}
        lw = max(Kit.text_w(lbl) for _, lbl in NEEDS)
        # The bar takes whatever the label and the percentage leave.
        Z["bar_w"] = max(40, IWz - 24 - lw - 10 - 8 - Kit.text_w("100%"))
        age_w = Kit.text_w("Age 99h 59m")
        # Two stat lines share a row only when both fit.
        pair1 = Kit.text_w("Wonderfully Happy  (sick)") + 6 + age_w <= IWz - 24
        pair2 = Kit.text_w("Squeaks 99999") + 6 + Kit.text_w("Mischievous") <= IWz - 24
        Z["pair1"], Z["pair2"] = pair1, pair2
        lines = (1 if pair1 else 2) + (1 if pair2 else 2)
        Z["sh"] = 8 + 4 * 18 + 2 + lines * 18 + 4
        cw = act_col_w()
        # As many action columns as fit, so captions are never dropped.
        n = max(1, min(len(ACTS), (IWz - 24 + 12) // cw))
        Z["ncols"], Z["col_w"] = n, cw
        rows = (len(ACTS) + n - 1) // n
        Z["ah"] = 8 + rows * 26 + 4
        fixed = Z["top"] + GAP + Z["sh"] + GAP + Z["ah"] + M
        # The pen's title strip keeps its PEN_HEAD px; the scene below it is scaled, so the pet never rises
        # above it.
        HD = PEN_HEAD
        if h is None:
            k = min(1.0, IWz / float(PW))
            pen_h = int(round(HD + (PH - HD) * k))
        else:
            pen_h = h - fixed
            k = min(1.0, IWz / float(PW), (pen_h - HD) / float(PH - HD))
        # Too short for the smallest pen: it stays at that size and the body scrolls.
        scroll = k < PEN_MIN_K - 0.001
        if scroll:
            k = PEN_MIN_K
            pen_h = int(round(HD + (PH - HD) * k))
        Z["pen_h"], Z["k"], Z["scroll"] = pen_h, k, scroll
        Z["sy"] = Z["top"] + pen_h + GAP
        Z["ay"] = Z["sy"] + Z["sh"] + GAP
        Z["h"] = Z["ay"] + Z["ah"] + M
        Z["ox"] = M + (IWz - PW * k) / 2.0
        Z["oy"] = Z["top"] + HD * (1.0 - k) + (pen_h - HD - (PH - HD) * k) / 2.0
        return Z

    def zone_plan(w, h):
        """Return (layout w, layout h, window scale, geometry, body height or None) for a w x h slot.

        A slot narrower than the layout's minimum is laid out at the minimum and the whole window
        scaled down. A body height is returned when the body scrolls beside its bar.
        """
        mw = zone_min_w()
        kw = 1.0
        lw, lh = w, h
        if w < mw:
            need = zone_geom(mw, None)["h"]
            kw = min(w / float(mw), h / float(need))
            lw, lh = int(round(w / kw)), int(round(h / kw))
        Z = zone_geom(lw, lh)
        # Too short: its body scrolls, so its width gives up the scroll band.
        if Z["scroll"] and kw == 1.0:
            lw = w - Kit.SCROLL_BAND
            Z = zone_geom(lw, lh)
            return lw, lh, kw, Z, Z["h"]
        return lw, lh, kw, Z, None

    def feral_block(g, store, x, y, w, h, nmax):
        """Draw the feral pet's message and the Adopt a new pup button in the pen's place."""
        lines = Kit.wrap("%s decided it is better off without a master and flew away." % name(), w - 40)
        for i, line in enumerate(lines[:nmax]):
            Kit.add_label(g, line, x + (w - Kit.text_w(line)) // 2, y + 32 + i * 18, Kit.HUE_INFO)
        cap = "Adopt a new pup"
        Kit.art_button(g, store, "adopt", Kit.ART_PLAY, x + (w - 35 - Kit.text_w(cap)) // 2, y + h - 36, cap,
                       "Start again; squeaks, wardrobe, virtues and relics stay", on_click=queue("adopt"))

    def stats_block(g, c, v, sy, iw, sh, bw, pair1=True, pair2=True):
        """Build the needs bars and the loyalty, age, squeaks and personality labels.

        Their controls are kept in c for the refresh. pair1 and pair2 put two labels on one row when the
        width allows.
        """
        Kit.add_section(g, M, sy, iw, sh)
        bx = M + 12 + max(Kit.text_w(lbl) for _, lbl in NEEDS) + 10
        c["bars"] = {}
        for i, (key, lbl) in enumerate(NEEDS):
            ry = sy + 8 + i * 18
            c["nl_" + key] = label(g, v, lbl, M + 12, ry, Kit.HUE_TEXT)
            Kit.add_tiled(g, Kit.LINE_RED, bx, ry + 3, bw, 11)
            c["bars"][key] = Kit.add_tiled(g, Kit.LINE_BLUE, bx, ry + 3, bw, 11)
            c["nv_" + key] = label(g, v, "", bx + bw + 8, ry, Kit.HUE_INFO)
        age_w = Kit.text_w("Age 99h 59m")
        y1 = sy + 82
        c["loyal"] = label(g, v, "", M + 12, y1, Kit.HUE_TEXT)
        if pair1:
            c["age"] = label(g, v, "", M + iw - 12 - age_w, y1, Kit.HUE_INFO)
            c["loyal_w"] = iw - 24 - age_w - 6
        else:
            y1 += 18
            c["age"] = label(g, v, "", M + 12, y1, Kit.HUE_INFO)
            c["loyal_w"] = iw - 24
        y2 = y1 + 18
        c["sq"] = label(g, v, "", M + 12, y2, Kit.HUE_TITLE)
        if pair2:
            c["pers"] = label(g, v, "", M + iw - 12 - Kit.text_w("Mischievous"), y2, Kit.HUE_INFO)
        else:
            c["pers"] = label(g, v, "", M + 12, y2 + 18, Kit.HUE_INFO)

    def build_zone(g, store, c, v, lw, lh, kw, Z):
        """Build the main window for its zone slot, in layout pixels (lw x lh, scaled by kw).

        Z is the geometry from zone_geom. The pen's pieces are made in the pen's own pixels and moved
        through one transform.
        """
        IWz = Z["IW"]
        Kit.add_window_frame(g, lw, Z["h"] if Z["scroll"] else lh)
        title_bar(g, store, "main", lw, TITLE, [("settings", Kit.ART_PAGE, "Settings", Kit.SETTINGS_TIP % TITLE)],
                  dock=True, close_tip=Kit.CLOSE_TIP % TITLE)
        top, pen_h, k = Z["top"], Z["pen_h"], Z["k"]
        Kit.add_section(g, M, top, IWz, pen_h)
        c["pen_w"], c["iw"], c["bar_w"] = IWz, IWz, Z["bar_w"]
        c["pen_title"] = label(g, v, "", M + 8, top + 6, Kit.HUE_TITLE)
        c["pantry_lbl"] = label(g, v, "", M + IWz - 8 - Kit.text_w("Pantry 20"), top + 6, Kit.HUE_INFO)
        if pet["feral"]:
            feral_block(g, store, M, top, IWz, pen_h, max(1, (pen_h - 70) // 18))
        else:
            v.made = []
            pen_pieces(g, c, v)
            # A control can be registered twice: each is moved once.
            made, seen = [], set()
            for ctl in v.made:
                if id(ctl) not in seen:
                    seen.add(id(ctl))
                    made.append(ctl)
            v.made = None
            v.pen = seen
            # The pen's transform: its own origin, the zone's offset and the scale.
            v.xf = (PX0, PY0, Z["ox"], Z["oy"], k)
            c["pen_ctrls"] = made
            c["pen_k"] = k
            # Every piece goes through the one transform, so the pen looks right at any size.
            for ctl in made:
                e = v.cache.get(id(ctl)) or {}
                pos, size = e.get("pos"), e.get("size")
                with Kit.quiet:
                    if pos is not None:
                        tx, ty = v.tr(pos[0], pos[1])
                        ctl.SetPos(int(round(tx)), int(round(ty)))
                    if size is not None:
                        ctl.SetWidth(max(1, int(round(size[0] * k))))
                        ctl.SetHeight(max(1, int(round(size[1] * k))))
            # The gremlin's strokes follow the pen's scale.
            c["grem_k"] = None
            gremlin_scale(c, 1.0)
        stats_block(g, c, v, Z["sy"], IWz, Z["sh"], Z["bar_w"], Z["pair1"], Z["pair2"])
        ay = Z["ay"]
        Kit.add_section(g, M, ay, IWz, Z["ah"])
        # The actions: as many columns as fit, captions never dropped.
        n, cw = Z["ncols"], Z["col_w"]
        for i, (key, art, cap, tip) in enumerate(ACTS):
            Kit.art_button(g, store, key, art, M + 12 + (i % n) * cw, ay + 8 + (i // n) * 26, cap, tip,
                           on_click=queue(key))
        # The whole window is drawn smaller than its layout.
        if kw != 1.0:
            Kit.scale_window(g, kw)
            if v.xf is not None:
                v.xf = (PX0, PY0, Z["ox"] * kw, Z["oy"] * kw, k * kw)
                c["pen_k"] = k * kw
                c["grem_k"] = None
                gremlin_scale(c, 1.0)
        # The pen's text pieces are scaled by the client at the pen's scale.
        if v.xf is not None:
            for ctl in c.get("pen_ctrls") or ():
                e = v.cache.get(id(ctl)) or {}
                if "text" in e:
                    rc = Kit.client_control(ctl)
                    if rc is not None:
                        safe(lambda rc=rc: rc.SetInternalScale(v.xf[4]))

    def zone_fit(w, h, mode):
        """The layout's fit hook: the main window's slot in a zone is w x h (None frees it).

        Runs on the client thread: it records the slot and asks for a redraw. Mode again redraws even
        for a size it was already told.
        """
        new = (int(w), int(h)) if (w is not None and h is not None) else None
        if new != st.get("fit") or (mode == "again" and new is not None):
            st["fit"] = new
            st["redraw"] = True

    def zone_drawn_at():
        """Return what the layout last drew the window at: (scale, minimum size or None)."""
        return st.get("zone_k") or (1.0, None)

    def build_window():
        """Build the main window: in a zone slot, as the minimized bar, or at its own size."""
        def build(g, store, c, v):
            """Build the main window at its own size (the normal case)."""
            if st["minimized"]:
                c["mini"] = mini_bar(g, store, "main", TITLE, Kit.CLOSE_TIP % TITLE)
                return
            Kit.add_window_frame(g, W, H)
            title_bar(g, store, "main", W, TITLE, [("settings", Kit.ART_PAGE, "Settings", Kit.SETTINGS_TIP % TITLE)],
                      dock=True, close_tip=Kit.CLOSE_TIP % TITLE)
            Kit.add_section(g, PX0, PY0, PW, PH)
            c["pen_title"] = label(g, v, "", PX0 + 8, PY0 + 6, Kit.HUE_TITLE)
            c["pantry_lbl"] = label(g, v, "", PX0 + PW - 8 - Kit.text_w("Pantry 20"), PY0 + 6, Kit.HUE_INFO)
            if pet["feral"]:
                feral_block(g, store, PX0, PY0, PW, PH, 3)
            else:
                pen_pieces(g, c, v)
            stats_block(g, c, v, SY, IW, SH, BAR_W)
            Kit.add_section(g, M, AY, IW, AH)
            nx = 0
            for i, (k, art, cap, tip) in enumerate(ACTS):
                # Three action buttons a row; a long caption pushes the next button right so none overlap.
                ax = M + 12 + (i % 3) * 88
                if i % 3 and ax < nx:
                    ax = nx
                ay = AY + 8 + (i // 3) * 26
                Kit.art_button(g, store, k, art, ax, ay, cap, tip, on_click=queue(k))
                nx = ax + 35 + Kit.text_w(cap) + 6

        # A zone slot decides the size; otherwise the window uses its own.
        slot = st.get("fit")
        st["zone_k"] = None
        if slot is not None and not st["minimized"]:
            lw, lh, kw, Z, body = zone_plan(slot[0], slot[1])
            if kw != 1.0:
                st["zone_k"] = (kw, (zone_min_w(), zone_geom(zone_min_w(), None)["h"]))

            def build_z(g, store, c, v):
                """Build the main window for its zone slot."""
                build_zone(g, store, c, v, lw, lh, kw, Z)

            if body is not None:
                open_window("main", build_z, lw, body, slot[1])
            else:
                open_window("main", build_z, slot[0], slot[1])
        elif slot is not None:
            def build_m(g, store, c, v):
                """Build the minimized bar as wide as its slot."""
                c["mini"] = mini_bar(g, store, "main", TITLE, Kit.CLOSE_TIP % TITLE, w=max(MINI_W, slot[0]))
                c["mini_w"] = max(MINI_W, slot[0])

            open_window("main", build_m, max(MINI_W, slot[0]), MINI_H, None, st["docked"])
        else:
            w, h = (MINI_W, MINI_H) if st["minimized"] else (W, H)
            open_window("main", build, w, h, None, st["minimized"] and st["docked"])
        # The new window is filled at once, so it never shows empty.
        refresh(time.time(), True)
        run_hop()

    wnd = None
    wins = dict((k, win if k == "main" else {"g": None, "c": {}, "store": ({}, {}), "v": None}) for k in WINDOWS)
    subfit = {}

    def pen_title():
        """Return the pen's title: the name (with any title worn) and the growth stage or gone wild."""
        nm = full_name(name().upper(), shop["eq"].get("title", "")).upper()
        stage = ["pup", "mongotchi", "greater"][pet["stage"]]
        # A pet with every virtue at maximum is called an avatar.
        if vall_at(VIRTUE_MAX):
            stage = "avatar"
        return "%s  (%s)" % (nm, "gone wild" if pet["feral"] else stage)

    def refresh(t, texts):
        """Update the main window's labels, bars and pen pieces for time t (client thread).

        texts True also rewrites the text labels (done about once a second); the bars, the pen pieces and
        the animation run on every call. A minimized window only shows the alert or status line.
        """
        c, v = wins["main"]["c"], wins["main"]["v"]
        if v is None:
            return
        if c.get("mini") is not None:
            if st["docked"]:
                return
            a = alert_keys()
            if texts or a:
                if pet["feral"]:
                    txt, hue = "gone wild", Kit.HUE_BAD
                elif a:
                    txt = MINI_ALERT[a[0]]
                    hue = Kit.HUE_BAD if int(t * 2) % 2 == 0 else Kit.HUE_TEXT
                elif pet["away"]:
                    txt, hue = away_short(), Kit.HUE_INFO
                elif pet["asleep"]:
                    txt, hue = "asleep", Kit.HUE_INFO
                else:
                    txt, hue = loyalty()
                raw, room = "%s: %s" % (TITLE, txt), c.get("mini_w", MINI_W) - 90
                mf = c.get("mini_fit")
                if mf is None or mf[0] != raw or mf[1] != room:
                    mf = c["mini_fit"] = (raw, room, fit(raw, room))
                v.text(c["mini"], mf[2], hue)
            return
        # The need bars glide a quarter of the way to their value each call, so they never jump.
        for k, _ in NEEDS:
            want = c.get("bar_w", BAR_W) * pet[k] / 100.0
            cur = st["bar_w"].get(k, want)
            step = max(1.0, abs(want - cur) * 0.25)
            cur = want if abs(want - cur) <= step else cur + step * (1 if want > cur else -1)
            st["bar_w"][k] = cur
            v.width(c["bars"].get(k), int(round(cur)))
        # The squeaks count rolls up or down towards its value instead of jumping.
        want = int(shop["sq"])
        shown = st.get("sq_shown", want)
        if shown != want:
            shown += max(1, abs(want - shown) // 5) * (1 if want > shown else -1)
            st["sq_shown"] = shown
            v.text(c["sq"], "Squeaks %d" % shown, Kit.HUE_GOOD if want > shown or st.get("sq_up") else Kit.HUE_TITLE)
            st["sq_up"] = want > shown
        elif texts:
            st["sq_shown"] = want
            v.text(c["sq"], "Squeaks %d" % want, Kit.HUE_TITLE)
        if texts:
            pw = Kit.text_w("Pantry 20")
            ncol = eq("ncol")
            v.text(c["pen_title"], fit(pen_title(), c.get("pen_w", PW) - 16 - pw - 6),
                   ncol["hue"] if ncol else Kit.HUE_TITLE)
            v.text(c["pantry_lbl"], "Pantry %d" % pet["pantry"], Kit.HUE_BAD if pet["pantry"] == 0 else Kit.HUE_INFO)
            for k, lbl in NEEDS:
                val = int(round(pet[k]))
                v.text(c["nv_" + k], "%d%%" % val)
                v.text(c["nl_" + k], lbl, Kit.HUE_BAD if val < 25 else Kit.HUE_TEXT)
            lt, hue = loyalty()
            extra = "  (sick)" if pet["sick"] else ""
            v.text(c["loyal"], fit(lt + extra, c.get("loyal_w", IW - 24 - Kit.text_w("Age 99h 59m") - 6)),
                   Kit.HUE_BAD if pet["sick"] else hue)
            v.text(c["age"], "Age " + hm(pet["age"]))
            v.text(c["pers"], eq("pers")["name"])
        if c.get("doll") is None:
            return
        # Finished animations are dropped here.
        anims = st["anims"]
        if anims:
            for kind in [k for k, a in anims.items() if t - a["t0"] >= a["dur"]]:
                del anims[kind]
        e = shop["eq"]
        # Decor and hanging item are redrawn only when what is worn changes.
        worn = (e.get("decor"), e.get("hang"))
        if c.get("worn") != worn:
            c["worn"] = worn
            for k in ("decor", "hang"):
                it = eq(k)
                if it:
                    v.look(c[k], it["gfx"], it["hue"])
                v.show(c[k], it is not None)
        if worn[1] and eq("hang"):
            # The hanging item sways a little.
            v.move(c["hang"], PX0 + PW - 48 + 2 * math.sin(t * 1.3), PY0 + 20)
        # The pantry is redrawn only when its count changes or an item is popping in.
        a_pop, p_pop = anim_at("pantry_pop", t) if anims else (None, 0.0)
        n_food = min(pet["pantry"], PANTRY_SHOW)
        if a_pop is not None or c.get("pantry_n") != n_food:
            c["pantry_n"] = None if a_pop is not None else n_food
            for i, p in enumerate(c["pantry"]):
                v.show(p, i < n_food)
                gfx = FOODS[i % len(FOODS)][0]
                cx, cy = PX0 + 4 + i * 11 + 22, PY0 + PH - 38 + (i % 2) * 3 + 17
                k = 1.0
                if a_pop is not None and i == n_food - 1:
                    k = 0.3 + 0.7 * p_pop
                    cy -= 6 * math.sin(p_pop * math.pi)
                scaled_box(v, p, gfx, cx, cy, k, (44, 34))
        # Heaps are redrawn only when they change or move (a clean, or a new heap dropping in).
        a_cl, p_cl = anim_at("clean", t) if anims else (None, 0.0)
        n_show = max(pet["messes"], st.get("mess_was", 0) if a_cl else 0)
        moving = a_cl is not None
        if anims and not moving:
            for k in MESS_KINDS:
                if k in anims:
                    moving = True
                    break
        if moving or c.get("mess_n") != (n_show, pet["messes"]):
            c["mess_n"] = None if moving else (n_show, pet["messes"])
            for i, p in enumerate(c["mess"]):
                on = i < n_show
                v.show(p, on)
                if not on:
                    continue
                cx, cy = PX0 + 84 + i * 44 + 22, PY0 + PH - 28 + 12
                k = 1.0
                a_m, p_m = anim_at(MESS_KINDS[i] if i < len(MESS_KINDS) else "mess%d" % i, t)
                if a_cl is not None and i >= pet["messes"]:
                    k = max(0.05, 1.0 - p_cl)
                elif a_m is not None:
                    k = 0.2 + 0.8 * p_m
                scaled_box(v, p, GFX_MESS, cx, cy + (1 - k) * 8, k, (44, 24))
        # The night shade fades in and out in steps of 0.06 per call.
        want = 0.55 if pet["asleep"] and not pet["feral"] else 0.0
        na = st.get("night_a", want)
        na = want if abs(want - na) < 0.06 else na + 0.06 * (1 if want > na else -1)
        st["night_a"] = na
        v.alpha(c["night"], na)
        animate(t, c, v)
        if c.get("snow"):
            draw_snow(t, c, v)
        # New Year: a firework now and then, unless one is already due this very call.
        if st["seasons"] and "newyear" in st["seasons"] and not st["fw_at"] - FIREWORK_EVERY[1] <= t < st["fw_at"]:
            firework(t)
        draw_pool(v, c, "main", t, PX0, PY0, PW, PH)

    def toy_motion(t, dt, toy):
        """Move the toy one step by its kind of motion and return where the pet aims for."""
        y = st["toy"]
        m = toy.get("motion", "bounce")
        lo_x, hi_x = PX0 + 6, PX0 + PW - 50
        # Toys that fall under gravity and bounce off the floor.
        if m in ("bounce", "bouncy", "dice"):
            y[3] += 320.0 * dt
            y[0] += y[2] * dt
            y[1] += y[3] * dt
            if y[1] >= FLOOR_Y:
                y[1] = float(FLOOR_Y)
                y[3] = -random.uniform(220, 300) if m == "bouncy" else \
                    -random.uniform(80, 120) if m == "dice" else -random.uniform(140, 220)
        elif m == "float":
            y[0] += y[2] * 0.5 * dt
            y[1] = FLOOR_Y - 50 + 30 * math.sin(t * 1.7)
        elif m == "scurry":
            y[1] = float(FLOOR_Y)
            y[0] += y[2] * 1.6 * dt
            if random.random() < dt * 0.8:
                y[2] = -y[2]
        elif m == "hover":
            y[0] = PX0 + PW / 2.0 - 22 + 60 * math.sin(t * 1.3)
            y[1] = PY0 + 50 + 12 * math.sin(t * 2.6)
        elif m == "music":
            if t >= st["music_at"]:
                st["music_at"] = t + 2.5
                sound(toy.get("snd"))
            cx = PX0 + PW / 2.0 - PB_W / 2.0
            return cx + 40 * math.sin(t * 3.0), YMIN + 20 + 10 * math.sin(t * 6.0)
        # Bounce off the pen's side walls.
        if y[0] <= lo_x or y[0] >= hi_x:
            y[0] = clamp(y[0], lo_x, hi_x)
            y[2] = -y[2]
        return y[0] - 6, y[1] - PB_H + 22

    def ambient(t, gone):
        """Now and then show a small particle that tells how the pet is doing."""
        if t < st.get("amb_at", 0.0) or gone or pet["feral"]:
            return
        st["amb_at"] = t + random.uniform(1.2, 2.2)
        x, y = pet_xy()
        if pet["asleep"]:
            particle(random.choice(["z", "z", "Z"]), HUE_ZZZ, x + 14, y + 4, 8.0, -14.0, 2.4)
            return
        if pet["clean"] < 35 or pet["messes"] >= 2:
            particle("~", HUE_STINK, x + random.uniform(-14, 14), y + 18, 0.0, -12.0, 1.8)
            for i in range(pet["messes"]):
                if random.random() < 0.5:
                    particle("~", HUE_STINK, PX0 + 84 + i * 44 + 22, PY0 + PH - 30, 0.0, -10.0, 1.6)
        if pet["sick"] and random.random() < 0.6:
            particle("o", HUE_SICK, x + random.uniform(-8, 8), y + 10, 0.0, -16.0, 1.6)
        elif pet["food"] < 25 and random.random() < 0.3:
            particle("?", Kit.HUE_INFO, x + 16, y, 0.0, -10.0, 1.4)
        elif pet["joy"] < 25 and random.random() < 0.3:
            particle("...", Kit.HUE_INFO, x + 16, y, 0.0, -8.0, 1.8)
        elif mood() >= 85 and random.random() < 0.15:
            sprite(SPR_MOTES, x, y + 18, 1.2, 0, 64)

    SNOW_TOP, SNOW_FLOOR = PY0 + 22, PY0 + PH - 7

    def make_snow(g, v, c):
        """Winter: make SNOW_N flakes and a strip of snow on the pen floor, with the pen.
        Their places are kept in st, so they survive a redraw.
        """
        sn = st["snow"]
        if len(sn) != SNOW_N:
            st["snow"] = sn = [[random.uniform(PX0 + 6, PX0 + PW - 9), random.uniform(SNOW_TOP, SNOW_FLOOR),
                                random.uniform(SNOW_SPEED[0], SNOW_SPEED[1]), random.uniform(0.0, 6.28),
                                random.choice((2, 2, 3))] for _ in range(SNOW_N)]
        ground = Kit.add_box(g, PX0 + 2, PY0 + PH - 5, PW - 4, 3, 0.85, "#FFFFFF")
        if ground is not None:
            v.reg(ground, pos=(PX0 + 2, PY0 + PH - 5), size=(PW - 4, 3))
        flakes = []
        for f in sn:
            b = Kit.add_box(g, int(f[0]), int(f[1]), f[4], f[4], 0.9, "#FFFFFF")
            if b is not None:
                v.reg(b, pos=(int(f[0]), int(f[1])), size=(f[4], f[4]))
                flakes.append((b, f))
        c["snow"], c["snow_ground"] = flakes, ground

    def draw_snow(t, c, v):
        """Move every snowflake: it falls and sways, and one that reaches the floor starts again at the top.
        A fixed set, so nothing is made or dropped while it snows.
        """
        # The step is capped, so a stall in the client does not make the snow jump.
        dt = max(0.0, min(0.5, t - st.get("snow_t", t)))
        st["snow_t"] = t
        for b, f in c["snow"]:
            f[1] += f[2] * dt
            if f[1] >= SNOW_FLOOR:
                f[0] = random.uniform(PX0 + 6, PX0 + PW - 9)
                f[1] = float(SNOW_TOP)
            v.move(b, f[0] + 3.0 * math.sin(t * 1.3 + f[3]), f[1])

    def firework(t):
        """New Year: a burst of colour over the pen now and then, using the pen's own sparkle and
        particle pools, so nothing new is made.
        """
        st["fw_at"] = t + random.uniform(FIREWORK_EVERY[0], FIREWORK_EVERY[1])
        hue = random.choice(RAINBOW)
        x = random.uniform(PX0 + 40, PX0 + PW - 40)
        y = random.uniform(PY0 + 36, PY0 + 60)
        sprite(SPR_STARS, x, y, 1.0, hue, 48)
        for dx in (-14, 14):
            particle("*", hue, x + dx, y, dx * 1.6, -8.0, 0.9)

    def aim(t, dt, px, py, gr, gone, eating, speed, rate):
        """Decide where the pet is heading and how fast it flaps for this frame (client thread).

        Sets the target st tx / ty from the pet's state in this order of priority: away, wild, asleep, on its
        way to guard the pantry, eating, playing with a toy, then wandering. Takes the time, the step, the
        pet's position, the gremlin, whether the pet has left, whether it is eating, and the current speed
        and wing rate. Returns (speed, rate, prop, landed): prop is (picture, x, y, hue, scale) of what is
        held in view or None, landed is True while the pet is at its food.
        """
        if pet["away"]:
            if not gone:
                st["tx"], st["ty"], speed, rate = XMAX + 30.0, float(YMIN), 140.0, 10.0
            return speed, rate, None, False
        if pet["feral"]:
            return speed, rate, None, False
        if pet["asleep"]:
            st["tx"], st["ty"] = float(PX0 + PW // 2 - PB_W // 2), float(YMAX)
            return 30.0, rate, None, False
        if gr is not None and gr["phase"] == "walk" and gr["guard_at"] and t >= gr["guard_at"]:
            st["tx"], st["ty"], speed, rate = gr["x"] - 6, float(YMAX), 170.0, 11.0
            return speed, rate, None, False
        if eating:
            fx = float(st["eat_x"] - 6)
            st["tx"], st["ty"], speed, rate = fx, float(YMAX - 4), 110.0, 7.0
            landed = abs(px - fx) < 6 and abs(py - (YMAX - 4)) < 6
            bites = 1.0
            if landed:
                st.setdefault("eat_t0", t)
                bites = max(0.0, 1.0 - int((t - st["eat_t0"]) / 0.45) * 0.25)
                if bites < st.get("eat_bites", 1.0):
                    pet_particle(".", HUE_CRUMB, random.uniform(-10, 10), 34, random.uniform(-15, 15), 10.0, 0.8)
                st["eat_bites"] = bites
            return speed, rate, (st["eat_food"][0], st["eat_x"] + 16, FLOOR_Y + 17, 0, max(0.05, bites)), landed
        if t < st["play_until"] and st["play_toy"] is not None:
            toy = st["play_toy"]
            st["tx"], st["ty"] = toy_motion(t, dt, toy)
            speed, rate = 95.0 * pers("speed", 1.0), 8.0
            prop = (toy["gfx"], st["toy"][0] + 22, st["toy"][1] + 17, toy["hue"], 1.0)
            if toy.get("motion") == "music" and random.random() < dt * 1.5:
                pet_particle(random.choice(["~", "*", "+"]), random.choice(RAINBOW), random.uniform(-20, 20), 6,
                             random.uniform(-10, 10), -18.0, 1.4)
            elif abs(st["toy"][0] + 22 - (px + PB_W / 2.0)) < 14 and random.random() < dt * 2:
                pet_particle("!", Kit.HUE_GOOD, 0, -4, 0.0, -24.0, 0.8)
            return speed, rate, prop, False
        # Hungry or tired pets move and flap slowly.
        if pet["food"] < 25 or pet["energy"] < 15:
            rate = 2.6
            speed *= 0.6
        if (abs(st["tx"] - px) < 2 and abs(st["ty"] - py) < 2 or st["tx"] == 0) and t >= st["hover_until"]:
            # Reached the target (or has none yet) and the pause is over: pick a new one, lower in the pen when
            # food or joy is low, and sometimes start a small animation that matches the mood.
            low = YMIN + 30 if (pet["food"] < 25 or pet["joy"] < 25) else YMIN
            st["tx"] = float(random.randint(XMIN, XMAX))
            st["ty"] = float(random.randint(min(low, YMAX), YMAX))
            st["hover_until"] = t + random.uniform(0.5, 2.5) / pers("speed", 1.0)
            r = random.random()
            if mood() >= 80 and r < 0.12:
                anim("loop", 1.0)
            elif pet["food"] < 25 and r < 0.25:
                anim("rumble", 0.5)
            elif pet["energy"] < 20 and r < 0.25:
                anim("yawn", 1.4)
        return speed, rate, None, False

    def carry_at(t, cr, cx, cy, hidden, gr):
        """Where the carried item is drawn: (centre x, centre y, size) or None when nothing shows.

        cr is the carry record. The pet carries it at its feet, the gremlin at its hands, and a dropped item
        arcs to the pantry; when the arc ends the carry is cleared.
        """
        if cr["who"] == "pet" and not hidden:
            return cx, cy + 20, 1.0
        if cr["who"] == "grem" and gr is not None:
            return gr["x"] + GR_W / 2.0 + 14, GR_Y + 34 + 2 * math.sin(t * 10), 1.0
        if cr["who"] != "drop":
            return None
        p = (t - cr["t0"]) / 0.8
        if p >= 1.0:
            st["carry"] = None
            anim("pantry_pop", 0.4)
            return None
        return (cr["x"] + (PX0 + 34 - cr["x"]) * p,
                cr["y"] + (PY0 + PH - 20 - cr["y"]) * p - 30 * math.sin(p * math.pi), 1.0 - 0.5 * p)

    def pose_loop(t, p, pose):
        """Pose effect of the loop animation: swing round in a circle.

        Every pose_* function takes the time t, the animation's progress p (0 to 1) and the pose dict, and
        adds to its offsets (ox, oy), scales (sx, sy), hue or size (k).
        """
        pose["ox"] += 12 * math.sin(p * 2 * math.pi)
        pose["oy"] += -12 * (1 - math.cos(p * 2 * math.pi)) / 2.0

    def pose_rumble(t, p, pose):
        """Pose effect of the rumble animation: shake sideways quickly."""
        pose["ox"] += 2 * math.sin(t * 60)

    def pose_yawn(t, p, pose):
        """Pose effect of the yawn animation: stretch tall, then settle."""
        pose["sy"] *= 1.0 - 0.12 * math.sin(p * math.pi)
        pose["oy"] += 3 * math.sin(p * math.pi)

    def pose_hop(t, p, pose):
        """Pose effect of the hop animation: squash down, then jump."""
        if p < 0.3:
            pose["sy"] *= 1.0 - 0.22 * math.sin(p / 0.3 * math.pi)
        else:
            pose["oy"] -= 9 * math.sin((p - 0.3) / 0.7 * math.pi)

    def pose_shake(t, p, pose):
        """Pose effect of the shake animation: shake sideways, fading out."""
        pose["ox"] += 3 * math.sin(t * 40) * (1 - p)

    def pose_stretch(t, p, pose):
        """Pose effect of the stretch animation: grow from squashed to full height with a small lift."""
        pose["sy"] *= 0.75 + 0.25 * p
        pose["oy"] -= 6 * math.sin(p * math.pi)

    def pose_cough(t, p, pose):
        """Pose effect of the cough animation: a small squash and bob."""
        pose["sy"] *= 1.0 - 0.15 * math.sin(p * math.pi)
        pose["oy"] += 2 * math.sin(p * math.pi)

    def pose_flash(t, p, pose):
        """Pose effect of the flash animation: flicker the sick hue on and off."""
        pose["hue"] = HUE_SICK if int(t * 10) % 2 == 0 else 0

    def pose_spooky(t, p, pose):
        """Pose effect of the spooky animation: flicker between white and the sleeping hue."""
        pose["hue"] = HUE_WHITE if int(t * 8) % 2 == 0 else HUE_SLEEP

    def pose_grow(t, p, pose):
        """Pose effect of the grow animation: flicker white while pulsing in size."""
        pose["hue"] = HUE_WHITE if int(t * 8) % 2 == 0 else None
        pose["k"] = 0.8 + 0.2 * abs(math.sin(t * 10))

    def pose_arrive(t, p, pose):
        """Pose effect of the arrive animation: drop in from above, squashing on landing."""
        pose["oy"] -= 70 * (1 - p) ** 2
        if p > 0.8:
            pose["sy"] *= 1.0 - 0.25 * math.sin((p - 0.8) / 0.2 * math.pi)

    # Poses are applied in this order, so a later hue or size wins.
    POSE_ORDER = ("loop", "rumble", "yawn", "hop", "shake", "stretch", "cough", "flash", "spooky", "grow", "arrive")
    POSE_RANK = dict((_k, _i) for _i, _k in enumerate(POSE_ORDER))
    POSE_FX = (pose_loop, pose_rumble, pose_yawn, pose_hop, pose_shake, pose_stretch, pose_cough, pose_flash,
               pose_spooky, pose_grow, pose_arrive)

    def pose_anims(t, anims, pose):
        """Apply every live animation to the pose in POSE_ORDER (client thread).

        anims is the st anims table (kind -> start time and duration). One pass collects the live kinds of
        the table that are poses, sorts them only when there are several, and calls their POSE_FX entry
        with its progress. Nothing is made when none is live.
        """
        live = None
        for kind, a in anims.items():
            o = POSE_RANK.get(kind)
            if o is None:
                continue
            el = t - a["t0"]
            if el < a["dur"]:
                if live is None:
                    live = []
                live.append((o, el / a["dur"]))
        if live is None:
            return
        if len(live) > 1:
            live.sort()
        for o, p in live:
            POSE_FX[o](t, p, pose)

    def animate(t, c, v):
        """Move and pose the pet and everything around it in the main pen for time t (client thread).

        Decides where the pet goes (wandering, eating, playing, asleep, away, guarding the pantry), poses
        it, and places the props, carried items, gremlin and speech line through the view v.
        """
        # The step is capped, so a stall in the client does not fling the pet across the pen.
        dt = max(0.0, min(0.5, t - st.get("anim_t", t)))
        st["anim_t"] = t
        px, py = st["px"], st["py"]
        stage = pet["stage"]
        speed = 35.0 * pers("speed", 1.0)
        # Wing beats per second.
        rate = 4.0
        gr = st["grem"]
        gone = pet["away"] and t >= st["leave_until"]
        a_zoom, _ = anim_at("zoom", t)
        if a_zoom:
            speed *= 2.5
            rate *= 2.0
        eating = t < st["eat_until"] and st["eat_food"] is not None
        speed, rate, prop, landed = aim(t, dt, px, py, gr, gone, eating, speed, rate)
        if t < st["cure_until"]:
            p = 1.0 - (st["cure_until"] - t) / 1.5
            prop = (GFX_CURE, px + PB_W / 2.0 + 26 * (1 - p), py + 18 + 6 * (1 - p), 0, max(0.1, 1 - p))
        elif t < st["brush_until"]:
            prop = (GFX_BRUSH, px + PB_W / 2.0 + 14 * math.sin(t * 12), py + 14 + 4 * math.cos(t * 12), 0, 1.0)
            if random.random() < dt * 4:
                pet_particle("*", HUE_WHITE, random.uniform(-18, 18), random.uniform(4, 24), 0.0, -14.0, 0.7)
        d = c["doll"]
        # -- move --
        a_far, p_far = anim_at("farewell", t)
        if not gone and not pet["feral"]:
            if t < st["dizzy_until"] and not pet["asleep"]:
                st["tx"] += 30 * math.sin(t * 4.0) * dt * 10
            st["tx"] = clamp(st["tx"], XMIN, XMAX + (40 if pet["away"] else 0))
            st["ty"] = clamp(st["ty"], YMIN, YMAX)
            px, py = st["px"], st["py"] = step_to(px, py, st["tx"], st["ty"], speed * dt)
        # -- pose --
        if pet["asleep"]:
            pose = sleep_pose(t)
        elif eating and landed:
            pose = {"sx": 0.72, "sy": 0.86 + 0.14 * abs(math.sin(t * 14)), "ox": 0.0, "oy": 2.0}
        else:
            depth = 0.6 if (pet["joy"] < 25 or pet["sick"]) else 1.0
            pose = flap_pose(t, rate, 0.0, stage, depth)
        if pet["sick"] and not pet["asleep"]:
            # Shivering.
            pose["ox"] += random.uniform(-1.0, 1.0)
        dance = st["play_toy"] is not None and t < st["play_until"] and st["play_toy"].get("motion") == "music"
        if dance:
            pose["ox"] += 6 * math.sin(t * 3.0)
            pose["oy"] += 3 * math.sin(t * 12.0)
        if t < st["dizzy_until"] and not pet["asleep"]:
            pose["ox"] += 6 * math.sin(t * 5.0)
            pose["oy"] += 4 * math.cos(t * 5.0)
            if random.random() < dt:
                pet_particle("@", HUE_DIZZY, 10, -2, 4.0, -12.0, 1.0)
        if t < st["brush_until"]:
            pose["ox"] += 2 * math.sin(t * 25)
        # One pass over the live animations, applied in POSE_ORDER (a later hue or size wins), not a
        # look-up per kind every frame.
        anims = st["anims"]
        if anims:
            pose_anims(t, anims, pose)
        # Flying off into the wild.
        if a_far:
            pose["oy"] -= 70 * p_far
            pose["ox"] += 30 * p_far
            pose["k"] = max(0.05, 1.0 - 0.9 * p_far)
        hidden = gone or (pet["away"] and px >= XMAX) or (pet["feral"] and not a_far)
        cx, cy = min(px, XMAX) + PB_W / 2.0, clamp(py, YMIN - 3, YMAX) + PB_H / 2.0
        if hidden:
            place_doll(v, d, 0, 0, None, t, shown=False)
            v.show(c["pet_hit"], False)
        else:
            place_doll(v, d, cx, cy, own_look(), t, pose)
            v.move(c["pet_hit"], cx - PB_W / 2.0, cy - PB_H / 2.0)
            v.show(c["pet_hit"], not pet["feral"])
        # -- the prop (food, toy, potion, brush) --
        if prop is not None:
            v.look(c["prop"], prop[0], prop[3])
            scaled_box(v, c["prop"], prop[0], clamp(prop[1], PX0 + 14, PX0 + PW - 14),
                       clamp(prop[2], PY0 + 30, FLOOR_Y + 17), prop[4], (44, 34))
            v.show(c["prop"], True)
        else:
            v.show(c["prop"], False)
        # -- what is carried: forage haul, the gremlin's loot, food dropped in --
        cr = st.get("carry")
        # (centre x, centre y, size k) of the carried item, or None.
        at = None
        if cr is not None:
            at = carry_at(t, cr, cx, cy, hidden, gr)
            if at is not None:
                v.look(c["prop2"], cr["gfx"], 0)
                scaled_box(v, c["prop2"], cr["gfx"], at[0], at[1], at[2], (44, 34))
            if cr["who"] == "pet" and not pet["away"] and t - cr.get("t0", t) >= 1.8:
                st["carry"] = {"who": "drop", "gfx": cr["gfx"], "t0": t, "x": cx, "y": cy + 20}
        v.show(c["prop2"], at is not None)
        # -- gremlin: waddles in, flinches when swatted, shrinks into the trap --
        if gr is not None:
            w = abs(math.sin(t * 10))
            gx = clamp(gr["x"], PX0 + 4, GX_START) + GR_W / 2.0
            # It bobs as it waddles.
            feet = GR_Y + GR_H - 2 * w
            k = 1.0
            seen = True
            a, p = anim_at("gswat", t)
            if a:
                # Flinches: flickers and hops.
                seen = int(t * 12) % 2 == 0
                feet -= 10 * math.sin(p * math.pi)
            a, p = anim_at("gtrap", t)
            if a:
                # Shrinks down into the trap.
                k = max(0.05, 1.0 - p)
            gremlin_scale(c, k)
            bw, bh = GR_W * k, GR_H * k
            v.move(c["grem"], gx - bw / 2.0, feet - bh)
            v.move(c["grem_hit"], gx - GR_W / 2.0, GR_Y)
            v.show(c["grem"], seen)
            v.show(c["grem_hit"], gr["phase"] == "walk")
        else:
            v.show(c["grem"], False)
            v.show(c["grem_hit"], False)
        # -- speech --
        # Nothing while asleep: its z's float up instead.
        txt = st["say"] if not pet["asleep"] and t < st["say_until"] and not gone else ""
        v.text(c["say"], txt)
        if txt:
            tw = Kit.text_w(txt)
            sx = clamp(cx - tw / 2.0, PX0 + 6, PX0 + PW - 6 - tw)
            # Above the pet as drawn (a hop, the wings' bob), not where it stands.
            oy = (pose or {}).get("oy", 0.0)
            sy = cy + min(0.0, oy) - PB_H / 2.0 - 22
            # No room above: the line goes below the pet.
            if sy < PY0 + 24:
                sy = cy + max(0.0, oy) + PB_H / 2.0 + 6
            v.move(c["say"], sx, clamp(sy, PY0 + 24, PY0 + PH - 18))
        ambient(t, hidden)

    def shop_layout(cats, sw=SW):
        """Flow the shop's category labels into rows.

        Returns ([(index, x, y)], section height).
        """
        x0, x, y = M + 10, M + 10, 0
        out = []
        for n, (_, lbl, _s) in enumerate(cats):
            tw = Kit.text_w(lbl)
            if x + tw > sw - M - 10 and x > x0:
                x, y = x0, y + 20
            out.append((n, x, y))
            x += tw + 14
        return out, y + 20 + 14

    def build_shop():
        """Build the shop window: balance, category tabs, the page of items and the pager.

        The page size follows the window height (st["shop_n"] rows). The window is built once per
        redraw; the squeaks label is filled by refresh_shop.
        """
        tabs = shop_cats()
        # A season's tab may be gone.
        st["shop_cat"] = min(st["shop_cat"], len(tabs) - 1)
        BY0 = M + 30 + GAP
        CY0 = BY0 + 30 + GAP
        sw, SHH = sub_size("shop", SW, CY0 + shop_layout(tabs)[1] + GAP + 8 + SHOP_ROWS * 38 + 30 + M)
        cats, cat_h = shop_layout(tabs, sw)
        LY0 = CY0 + cat_h + GAP
        LH = SHH - LY0 - M
        rows = st["shop_n"] = max(1, (LH - 38) // 38)

        def build(g, store, c, v):
            """Draw the shop's sections and the current page of items into gump g."""
            IWS = sw - 2 * M
            Kit.add_window_frame(g, sw, SHH)
            title_bar(g, store, "shop", sw, TITLE + " Shop")
            # Balance.
            Kit.add_section(g, M, BY0, IWS, 30)
            c["sq"] = label(g, v, "", M + 10, BY0 + 7, Kit.HUE_TITLE)
            hint = "+%d an hour, even when away" % int(PASSIVE_PER_H)
            Kit.add_label(g, fit(hint, IWS - 130), M + IWS - 10 - min(Kit.text_w(hint), IWS - 130),
                          BY0 + 7, Kit.HUE_INFO)
            # Categories.
            Kit.add_section(g, M, CY0, IWS, cat_h)
            for n, x, y in cats:
                lbl = tabs[n][1]
                hue = Kit.HUE_TITLE if n == st["shop_cat"] else Kit.HUE_TEXT
                Kit.add_label(g, lbl, x, CY0 + 7 + y, hue)
                Kit.catcher(g, x - 3, CY0 + 5 + y, Kit.text_w(lbl) + 6, 18,
                            queue(("shop", "cat", n)), "Show the %s tab" % lbl.lower())
            # Items.
            Kit.add_section(g, M, LY0, IWS, LH)
            items = shop_items()
            pages = max(1, (len(items) + rows - 1) // rows)
            st["shop_page"] = min(st["shop_page"], pages - 1)
            first = st["shop_page"] * rows
            for i, it in enumerate(items[first:first + rows]):
                ry = LY0 + 8 + i * 38
                if it["cat"] == "ncol":
                    Kit.add_label(g, "Abc", M + 14, ry + 9, it["hue"])
                elif it["gfx"]:
                    item_pic(g, v, it["gfx"], M + 6, ry, 44, 34, it["hue"])
                # Buttons, right to left. Each queues its own item and action, so a click can never land on a
                # button the row no longer has.
                x = M + IWS - 10
                for k, (bk, cap, act) in enumerate(row_buttons(it)):
                    x -= 35 + Kit.text_w(cap)
                    Kit.art_button(g, store, "r%d_%d" % (i, k), ROW_ARTS[bk], x, ry + 6, cap, row_tip(bk, it),
                                   on_click=queue(("shop", "act", it["id"], act)))
                    x -= 8
                owned = has(it["id"]) and not stackable(it)
                sell = in_season(it)
                nm = it["name"]
                if owned:
                    slot = CAT_SLOT.get(it["cat"])
                    ptxt = "owned" if not slot or shop["eq"].get(slot) != it["id"] else \
                        "worn" if slot in ("hat", "neck") else "in use"
                else:
                    ptxt = ("%s only" % SEASON_NAME[it["season"]]) if not sell else "%d sq" % price_of(it)
                    n = shop["cnt"].get(it["id"], 0) if stackable(it) else 0
                    nm += "  x%d" % n if n else ""
                pw = Kit.text_w(ptxt)
                x -= pw
                afford = owned or shop["sq"] >= price_of(it)
                Kit.add_label(g, ptxt, x, ry + 9, Kit.HUE_INFO if owned or not sell else
                              Kit.HUE_GOOD if afford else Kit.HUE_BAD)
                tw = x - 6 - (M + 56)
                Kit.add_label(g, fit(nm, tw), M + 56, ry + 1, Kit.HUE_TEXT)
                why = requirement(it) if not owned else None
                desc = it["desc"]
                if "season" in it:
                    desc = "%s: %s" % (SEASON_NAME[it["season"]], desc[:1].lower() + desc[1:])
                Kit.add_label(g, fit(why[:1].upper() + why[1:] if why else desc, tw), M + 56,
                              ry + 18, Kit.HUE_BAD if why else Kit.HUE_INFO)
            # Pager.
            py = LY0 + LH - 28
            Kit.art_button(g, store, "prev", ART_BACK, M + 10, py, None, "Previous page",
                           on_click=queue(("shop", "prev")))
            Kit.art_button(g, store, "next", Kit.ART_PLAY, M + IWS - 40, py, None, "Next page",
                           on_click=queue(("shop", "next")))
            ptxt = "%s: page %d of %d" % (tabs[st["shop_cat"]][1], st["shop_page"] + 1, pages)
            Kit.add_label(g, ptxt, M + (IWS - Kit.text_w(ptxt)) // 2, py + 3, Kit.HUE_INFO)

        open_sub("shop", "Shop", build, sw, SHH)
        refresh_shop(0.0, True)
        run_hop()

    def refresh_shop(t, texts):
        """Refresh the shop's squeaks balance (about once a second, when texts is True)."""
        c, v = wins["shop"]["c"], wins["shop"]["v"]
        if v is None or not texts:
            return
        if c.get("mini") is not None:
            v.text(c["mini"], "Shop: %d squeaks" % int(shop["sq"]))
        elif c.get("sq") is not None:
            v.text(c["sq"], "Squeaks %d" % int(shop["sq"]))

    def build_pen():
        """Build the playpen window: the pen scene, the member list and the paste-a-code box.

        Members come from pen_members(). Each keeps its place across redraws in st["pals"]; a newcomer
        flies in from the right.
        """
        members = pen_members()
        pw, ph = sub_size("pen", PPW, PPH)
        dh = ph - PPH

        def build(g, store, c, v):
            """Draw the playpen's sections, dolls, labels and code box into gump g."""
            IWP = pw - 2 * M
            Kit.add_window_frame(g, pw, ph)
            title_bar(g, store, "pen", pw, TITLE + " Playpen",
                      [("share", Kit.ART_PLAY, "Share", "Post %s's code in chat for friends' playpens" % name())])
            Kit.add_section(g, QX0, QY0, IWP, QH + dh)
            c["head"] = label(g, v, "", QX0 + 8, QY0 + 6, Kit.HUE_TITLE)
            c["toy"] = item_pic(g, v, 0x0E1D, QX0 + 20, QY0 + QH - 40, 44, 34, shown=False)
            c["dolls"] = []
            for n in range(PEN_MAX):
                x = QXMIN + n * (QXMAX - QXMIN) // max(1, PEN_MAX - 1)
                d = make_doll(g, v, x, QYMIN + 20)
                d["name"] = label(g, v, "", x, QY0 + QH - 18, Kit.HUE_TITLE)
                d["say"] = label(g, v, "", x, QYMIN, Kit.HUE_TEXT)
                c["dolls"].append(d)
            c["spr"], c["plbl"] = make_pool(g, v, QX0, QY0)
            if len(members) <= 1:
                tip = "Nobody else here yet. Share your code, or paste a friend's below."
                for i, line in enumerate(Kit.wrap(tip, QW - 60)[:2]):
                    Kit.add_label(g, line, QX0 + (QW - Kit.text_w(line)) // 2,
                                  QY0 + QH // 2 - 40 + i * 18, Kit.HUE_INFO)
            # Who is here.
            Kit.add_section(g, M, QGY + dh, IWP, QGH)
            colw = IWP // 2
            for n in range(PEN_MAX):
                x = M + 10 + (n % 2) * colw
                y = QGY + dh + 8 + (n // 2) * 25
                if n >= len(members):
                    Kit.add_label(g, "Free slot", x + 34, y + 3, Kit.HUE_INFO)
                    continue
                mb = members[n]
                if not mb["mine"]:
                    Kit.art_button(g, store, "rm%d" % n, Kit.ART_CLOSE, x, y, None,
                                   "Send %s home" % mb["name"], on_click=queue(("pen", "rm", n)))
                # Another player's pet carries that player's name. In streamer mode it is replaced by a stable
                # veiled label, derived from a checksum of the lower-cased name, so the same owner always looks the
                # same on stream without being named.
                own = mb["owner"]
                if Kit.streamer:
                    own = Kit.veil("name", own, Kit.checksum(own.lower().encode("utf-8")))
                txt = "%s (yours)" % mb["name"] if mb["mine"] else "%s (%s)" % (mb["name"], own)
                Kit.add_label(g, fit(txt, colw - 50), x + 34, y + 3, Kit.HUE_GOOD if mb["mine"] else Kit.HUE_TEXT)
            # Paste a code.
            ya = QAY + dh
            Kit.add_section(g, M, ya, IWP, QAH)
            Kit.add_label(g, "Code:", M + 10, ya + 12)
            cap = "Add"
            bx = M + IWP - 10 - 35 - Kit.text_w(cap)
            lx = M + 10 + Kit.text_w("Code:") + 10
            c["code"] = Kit.with_tip(Kit.add_textbox(g, "", lx, ya + 9, bx - lx - 12, numbers=False),
                                     "A friend's Mongotchi code (64 characters)")
            Kit.art_button(g, store, "add", Kit.ART_OK, bx, ya + 8, cap,
                           "Add that mongotchi to your playpen", on_click=queue(("pen", "add")))

        open_sub("pen", "Playpen", build, pw, ph)
        # Where everyone is, kept across redraws.
        pals = {}
        for mb in members:
            key = (mb["uid"], mb["owner"])
            old = st["pals"].get(key)
            # A newcomer flies in from the right, with a sparkle (not for the very first window).
            if old is None:
                y0 = float(random.randint(QYMIN, QYMAX))
                old = {"x": float(QXMAX), "y": y0, "tx": float(QXMIN + random.randint(0, QXMAX - QXMIN)),
                       "ty": y0, "until": 0.0, "say": "", "say_until": 0.0, "chase": None,
                       "chase_until": 0.0, "phase": random.uniform(0, 6.28)}
                if st["pals"]:
                    sprite(SPR_SPARKLE, QXMAX + PB_W / 2.0, y0 + PB_H / 2.0, 1.2, 0, 64, "pen")
            pals[key] = old
        st["pals"] = pals
        refresh_pen(time.time(), True)
        run_hop()

    def pal_say(p, text, t, secs=3.0):
        """Make a playpen member say a line for secs seconds."""
        p["say"], p["say_until"] = text, t + secs

    def refresh_pen(t, texts):
        """Move and draw the playpen's mongotchis, the ball game, speech and particles for time t.

        texts True also rewrites the heading (about once a second). Other players' mongotchis are drawn
        from their shared look; the owner's own follows the live look.
        """
        c, v = wins["pen"]["c"], wins["pen"]["v"]
        if v is None:
            return
        members = pen_members()
        if c.get("mini") is not None:
            if texts:
                v.text(c["mini"], "Playpen: %s" % Kit.count(len(members), "mongotchi"))
            return
        dt = max(0.0, min(0.5, t - st.get("pen_t", t)))
        st["pen_t"] = t
        if texts:
            v.text(c["head"], fit("PLAYPEN  (%d of %d)" % (len(members), PEN_MAX), QW - 16))
        # The member keys, made with the members.
        keys = _pm["keys"]
        # A ball game now and then, when there is company and the toy is not a music toy.
        game = st.get("pen_game")
        if game is None and len(members) > 1 and random.random() < dt / 25.0:
            toy = eq("toy")
            if toy.get("motion") != "music":
                st["pen_game"] = game = {"until": t + 8.0, "toy": toy, "b": [float(QX0 + 20), float(QY0 + QH - 60),
                                               random.uniform(80, 120), -80.0]}
        if game is not None and t >= game["until"]:
            st["pen_game"] = game = None
        if game is not None:
            b = game["b"]
            b[3] += 300.0 * dt
            b[0] += b[2] * dt
            b[1] += b[3] * dt
            if b[1] >= QY0 + QH - 40:
                b[1] = float(QY0 + QH - 40)
                b[3] = -random.uniform(150, 230)
            if b[0] <= QX0 + 6 or b[0] >= QX0 + QW - 50:
                b[0] = clamp(b[0], QX0 + 6, QX0 + QW - 50)
                b[2] = -b[2]
            v.look(c["toy"], game["toy"]["gfx"], game["toy"]["hue"])
            v.move(c["toy"], b[0], b[1])
        v.show(c["toy"], game is not None)
        for n, d in enumerate(c["dolls"]):
            if n >= len(members):
                place_doll(v, d, 0, 0, None, t, shown=False)
                v.show(d["name"], False)
                v.show(d["say"], False)
                continue
            mb = members[n]
            p = st["pals"].get(keys[n])
            if p is None:
                continue
            dv = pen_derived(n, mb)
            spd = dv["spd"]
            # A chase: run to the friend and boop it.
            if p["chase"] is not None and t < p["chase_until"] and p["chase"] in st["pals"]:
                q = st["pals"][p["chase"]]
                p["tx"], p["ty"], spd = q["x"], q["y"], 90.0
                if abs(q["x"] - p["x"]) < 20 and abs(q["y"] - p["y"]) < 16:
                    other = (members[keys.index(p["chase"])]["name"] if p["chase"] in keys else "a friend")
                    pal_say(p, random.choice(PEN_LINES) % other, t)
                    particle(random.choice(["<3", "!", "*boop*"]), random.choice([HUE_HEART, HUE_PINK, Kit.HUE_GOOD]),
                             q["x"] + PB_W / 2.0, q["y"], 0.0, -20.0, 1.2, "pen")
                    q["hop"] = t
                    p["chase"] = None
                    q["tx"], q["ty"] = float(random.randint(QXMIN, QXMAX)), float(QYMIN)
                    q["until"] = t + 1.5
            elif game is not None:
                p["tx"], p["ty"], spd = game["b"][0] - 6, game["b"][1] - PB_H + 22, 80.0
            else:
                p["chase"] = None
                if (abs(p["tx"] - p["x"]) < 2 and abs(p["ty"] - p["y"]) < 2) or p["tx"] == 0:
                    if t >= p["until"]:
                        if len(members) > 1 and random.random() < 0.25:
                            p["chase"] = random.choice([k for k in keys if k != keys[n]])
                            p["chase_until"] = t + 4.0
                        p["tx"] = float(random.randint(QXMIN, QXMAX))
                        p["ty"] = float(random.randint(QYMIN, QYMAX))
                        p["until"] = t + random.uniform(0.5, 3.0)
                        if random.random() < 0.08:
                            ln = BY_ID.get(mb["pers"] or "", {}).get("lines") or LINES["idle"]
                            pal_say(p, random.choice(ln), t)
            p["tx"], p["ty"] = clamp(p["tx"], QXMIN, QXMAX), clamp(p["ty"], QYMIN, QYMAX)
            p["x"], p["y"] = step_to(p["x"], p["y"], p["tx"], p["ty"], spd * dt)
            x, y = int(p["x"]), int(clamp(p["y"], QYMIN - 3, QYMAX))
            lk = own_look() if mb["mine"] else dv["look"]
            ph = p.get("phase", n * 1.3)
            if mb["mine"] and pet["asleep"]:
                # A copy, so the shared look stays as it is.
                lk = dict(lk)
                lk["hue"] = HUE_SLEEP
                pose = sleep_pose(t, ph)
            else:
                fast = (p["chase"] is not None and t < p["chase_until"]) or game is not None
                pose = flap_pose(t, 8.0 if fast else 4.0, ph, lk["stage"])
            hop = t - p.get("hop", -9.0)
            # Booped: a little hop.
            if hop < 0.5:
                pose["oy"] -= 8 * math.sin(hop / 0.5 * math.pi)
            place_doll(v, d, x + PB_W / 2.0, y + PB_H / 2.0, lk, t, pose)
            nm = dv["nm"]
            v.text(d["name"], nm, dv["hue"])
            # The name width was measured once per member.
            nw = dv["nw"]
            v.move(d["name"], clamp(x + PB_W / 2.0 - nw / 2.0, QX0 + 6, QX0 + QW - 6 - nw),
                   min(y + PB_H + 2, QY0 + QH - 18))
            v.show(d["name"], True)
            txt = p["say"] if t < p["say_until"] else ""
            v.text(d["say"], txt)
            v.show(d["say"], bool(txt))
            if txt:
                tw = Kit.text_w(txt)
                v.move(d["say"], clamp(x + PB_W / 2.0 - tw / 2.0, QX0 + 6, QX0 + QW - 6 - tw), max(QY0 + 24, y - 18))
        draw_pool(v, c, "pen", t, QX0, QY0, QW, QH)

    JBY0 = M + 30 + GAP
    JBH = 48
    JTY0 = JBY0 + JBH + GAP
    JLY0 = JTY0 + 30 + GAP
    JLH = 8 + JROWS * 38 + 8
    JH = JLY0 + JLH + M
    JBAR_W = 100

    def build_quest():
        """Build the Journeys window: status bar, tabs and the list of the chosen tab."""
        jw, jh = sub_size("quest", JW, JH)

        def build(g, store, c, v):
            """Draw the Journeys sections and the rows of the chosen tab into gump g."""
            IWJ = c["iw"] = jw - 2 * M
            Kit.add_window_frame(g, jw, jh)
            title_bar(g, store, "quest", jw, TITLE + " Journeys")
            # Status: where it is, and Call home while it is away.
            Kit.add_section(g, M, JBY0, IWJ, JBH)
            c["status"] = label(g, v, "", M + 10, JBY0 + 7, Kit.HUE_TITLE)
            c["status2"] = label(g, v, "", M + 10, JBY0 + 26, Kit.HUE_INFO)
            cap = "Call home"
            cx = M + IWJ - 10 - 35 - Kit.text_w(cap)
            c["home_x"] = cx
            c["home_lbl"] = Kit.art_button(g, store, "home", Kit.ART_CLOSE, cx, JBY0 + 12, cap,
                                           "Bring it back now with a share of the reward",
                                           on_click=queue(("quest", "home")))
            c["home_btn"] = store[0].get("home")
            # The Go and Meditate buttons follow this flag.
            c["was_away"] = pet["away"]
            # Tabs.
            Kit.add_section(g, M, JTY0, IWJ, 30)
            x = M + 12
            for n, tab in enumerate(JOURNEY_TABS):
                hue = Kit.HUE_TITLE if n == quest["tab"] else Kit.HUE_TEXT
                Kit.add_label(g, tab, x, JTY0 + 7, hue)
                Kit.catcher(g, x - 3, JTY0 + 4, Kit.text_w(tab) + 6, 22,
                            queue(("quest", "tab", n)), "Show the %s tab" % tab.lower())
                x += Kit.text_w(tab) + 24
            counts = "%s, %s" % (Kit.count(quest["hunts"], "hunt"), Kit.count(quest["med"], "meditation"))
            Kit.add_label(g, fit(counts, IWJ - (x - M) - 10), M + IWJ - 10 - min(
                Kit.text_w(counts), IWJ - (x - M) - 10), JTY0 + 7, Kit.HUE_INFO)
            # The list.
            Kit.add_section(g, M, JLY0, IWJ, jh - JLY0 - M)
            c["rows"] = []
            tab = quest["tab"]
            if tab == 0:
                build_hunt_rows(g, store, v, IWJ)
            elif tab == 1:
                build_virtue_rows(g, store, IWJ)
            else:
                build_relic_rows(g, v, IWJ)

        open_sub("quest", "Journeys", build, jw, jh)
        refresh_quest(time.time(), True)
        run_hop()

    def build_hunt_rows(g, store, v, IWJ):
        """Build the hunt rows: each location with its relic art, risk and a Go button.

        The Go button only shows when the pet is at home, not feral and meets the location's requirement.
        """
        away = pet["away"]
        for i, loc in enumerate(LOCATIONS[:JROWS]):
            ry = JLY0 + 8 + i * 38
            relic = RELIC_BY_ID[[e for e in loc["loot"] if e[1] == "relic"][0][2]]
            item_pic(g, v, relic[2], M + 6, ry, 44, 34, relic[3])
            why = meets(loc["req"])
            x = M + IWJ - 10
            if not away and not pet["feral"] and why is None:
                cap = "Go"
                x -= 35 + Kit.text_w(cap)
                Kit.art_button(g, store, "go%d" % i, Kit.ART_PLAY, x, ry + 6, cap,
                               "Send %s hunting at %s (%d min)" % (name(), loc["name"], loc["mins"]),
                               on_click=queue(("quest", "hunt", i)))
                x -= 8
            risk = "safe" if loc["danger"] <= 0.05 else "a little risky" if loc["danger"] <= 0.15 \
                else "risky" if loc["danger"] <= 0.3 else "dangerous"
            info = "%d min, %s" % (loc["mins"], risk)
            iw = Kit.text_w(info)
            x -= iw
            Kit.add_label(g, info, x, ry + 9, Kit.HUE_INFO if why is None else Kit.HUE_BAD)
            tw = x - 6 - (M + 56)
            visits = quest["visits"].get(loc["id"], 0)
            nm = loc["name"] + ("  (x%d)" % visits if visits else "")
            Kit.add_label(g, fit(nm, tw), M + 56, ry + 1, Kit.HUE_TEXT if why is None else Kit.HUE_INFO)
            Kit.add_label(g, fit(why[:1].upper() + why[1:] if why else loc["hint"], tw), M + 56,
                          ry + 18, Kit.HUE_BAD if why else Kit.HUE_INFO)

    def build_virtue_rows(g, store, IWJ):
        """Build the virtue rows: name and level, the experience bar, the effect and a Meditate button."""
        away = pet["away"]
        for i, vt in enumerate(VIRTUES[:JROWS]):
            k = vt[0]
            ry = JLY0 + 8 + i * 38
            lv = vlevel(k)
            x = M + IWJ - 10
            if not away and not pet["feral"] and lv < VIRTUE_MAX:
                cap = "Meditate"
                x -= 35 + Kit.text_w(cap)
                done, need = vprogress(k)
                Kit.art_button(g, store, "med%d" % i, Kit.ART_PLAY, x, ry + 6, cap,
                               "Meditate at the Shrine of %s for %d min (%d/%d to level %d)"
                               % (vt[1], int(MEDITATE_MIN), int(done), int(need), lv + 1),
                               on_click=queue(("quest", "med", i)))
                x -= 8
            # The experience bar shows this level's share.
            bx = x - JBAR_W
            Kit.add_tiled(g, Kit.LINE_RED, bx, ry + 12, JBAR_W, 11)
            done, need = vprogress(k)
            fill = JBAR_W if lv >= VIRTUE_MAX else int(JBAR_W * done / max(1.0, need))
            Kit.add_tiled(g, Kit.LINE_BLUE, bx, ry + 12, max(0, fill), 11)
            tw = bx - 6 - (M + 12)
            nm = "%s  Lv %d" % (vt[1], lv)
            Kit.add_label(g, fit(nm, tw), M + 12, ry + 1, Kit.HUE_TITLE if lv >= VIRTUE_MAX else Kit.HUE_TEXT)
            eff = (veffect(k, lv) if lv else "Not yet felt: " + veffect(k, 1).lower() + " at level 1")
            Kit.add_label(g, fit(eff, tw), M + 12, ry + 18, Kit.HUE_INFO)

    def build_relic_rows(g, v, IWJ):
        """Build the relic rows in two columns: found relics with their place, unknown ones as question marks."""
        colw = IWJ // 2
        for i, rel in enumerate(RELICS):
            col, row = i // JROWS, i % JROWS
            rx = M + col * colw
            ry = JLY0 + 8 + row * 38
            n = quest["relics"].get(rel[0], 0)
            loc = next((l for l in LOCATIONS if any(e[1] == "relic" and e[2] == rel[0] for e in l["loot"])), None)
            where = loc["name"] if loc else ""
            if n:
                item_pic(g, v, rel[2], rx + 6, ry, 44, 34, rel[3])
                nm = rel[1][0].upper() + rel[1][1:] + ("  x%d" % n if n > 1 else "")
                Kit.add_label(g, fit(nm, colw - 60), rx + 56, ry + 1, Kit.HUE_TEXT)
                Kit.add_label(g, fit(where, colw - 60), rx + 56, ry + 18, Kit.HUE_INFO)
            else:
                Kit.add_label(g, "?", rx + 24, ry + 9, Kit.HUE_INFO)
                Kit.add_label(g, "Not found yet", rx + 56, ry + 1, Kit.HUE_INFO)
                Kit.add_label(g, fit("Somewhere at " + where, colw - 60), rx + 56, ry + 18, Kit.HUE_INFO)

    def refresh_quest(t, texts):
        """Refresh the Journeys status lines (about once a second, when texts is True)."""
        c, v = wins["quest"]["c"], wins["quest"]["v"]
        if v is None or not texts:
            return
        if pet["feral"]:
            s1, s2 = "%s has gone wild" % name(), "Adopt a new pup in the pen first"
        elif pet["away"]:
            left = trip_left(t)
            s1 = "%s is %s" % (name(), away_doing())
            s2 = "Back in about %s (%d%% done)" % (hm(left + 59) if left >= 60 else "%d seconds" % int(left),
                                                   int(trip_frac(t) * 100))
        else:
            s1 = "%s is at home" % name()
            if quest["tab"] == 2:
                s2 = "%d of %d relics found: +%d%% squeaks" % (
                    len(quest["relics"]), len(RELICS), int(round(relic_bonus() * 100)))
            elif quest["tab"] == 1:
                s2 = "Meditation earns experience; each level adds an effect"
            else:
                s2 = "Far places are slower and riskier (Valor helps)"
        if c.get("mini") is not None:
            v.text(c["mini"], fit("Journeys: %s" % ("gone wild" if pet["feral"] else
                                                    away_short() if pet["away"] else "at home"), MINI_W - 90))
            return
        room = c.get("home_x", M + 300) - (M + 10) - 8 if pet["away"] else c["iw"] - 20
        v.text(c["status"], fit(s1, room))
        v.text(c["status2"], fit(s2, room))
        home = bool(pet["away"]) and pet["away_kind"] != 0
        v.show(c.get("home_btn"), home)
        v.show(c.get("home_lbl"), home)
        if pet["away"] != c.get("was_away"):
            c["was_away"] = pet["away"]
            st["quest_redraw"] = True

    ABY0 = M + 30 + GAP
    ALY0 = ABY0 + 30 + GAP
    ALH = 8 + ACH_ROWS * 38 + 8
    ACH_H = ALY0 + ALH + M

    def ach_line(a, done):
        """Return an achievement's second line: what to do, with how far along it is when that is known."""
        # Earned, or no counter to show: the plain text.
        if done or a[6] is None or a[6] == "stage" or a[7] <= 1:
            return a[2]
        cur = "{:,}".format(int(min(ACH_VALUES[a[6]](), a[7])))
        # Big goals show only the count; small ones show count and goal.
        return "%s (%s)" % (a[2], cur) if a[7] >= 1000 else "%s (%s/%d)" % (a[2], cur, a[7])

    def build_ach():
        """Build the Achievements window: a status bar and two columns of rows made once with the window."""
        aw, ah = sub_size("ach", ACH_W, ACH_H)

        def build(g, store, c, v):
            """Draw the Achievements sections and rows into gump g; the rows are filled by refresh_ach."""
            IWA = c["iw"] = aw - 2 * M
            Kit.add_window_frame(g, aw, ah)
            title_bar(g, store, "ach", aw, TITLE + " Achievements")
            Kit.add_section(g, M, ABY0, IWA, 30)
            c["status"] = label(g, v, "", M + 10, ABY0 + 7, Kit.HUE_TITLE)
            Kit.add_section(g, M, ALY0, IWA, ah - ALY0 - M)
            colw = IWA // 2
            rows = []
            for i, a in enumerate(ACHIEVEMENTS[:2 * ACH_ROWS]):
                rx = M + (i // ACH_ROWS) * colw
                ry = ALY0 + 8 + (i % ACH_ROWS) * 38
                done = a[0] in ach["got"]
                rtxt = "+%d" % a[3]
                rw = Kit.text_w(rtxt)
                rows.append({"a": a, "raw": None, "nw": colw - 66 - rw - 6, "hw": colw - 66,
                             "pic": item_pic(g, v, a[4], rx + 6, ry, 44, 34, a[5] if done else HUE_LOCKED),
                             "nm": label(g, v, "", rx + 56, ry + 1, Kit.HUE_TEXT),
                             "rew": label(g, v, rtxt, rx + colw - 10 - rw, ry + 1, Kit.HUE_TITLE),
                             "how": label(g, v, "", rx + 56, ry + 18, Kit.HUE_INFO)})
            c["rows"] = rows

        open_sub("ach", "Achievements", build, aw, ah)
        refresh_ach(0.0, True)
        run_hop()

    def refresh_ach(t, texts):
        """Write which achievements are earned and how far along the rest are (about once a second).

        Only the rows whose state changed are touched; the rows are made once, with the window.
        """
        c, v = wins["ach"]["c"], wins["ach"]["v"]
        if v is None or not texts:
            return
        got = ach["got"]
        n = sum(1 for a in ACHIEVEMENTS if a[0] in got)
        paid = sum(a[3] for a in ACHIEVEMENTS if a[0] in got)
        if c.get("mini") is not None:
            v.text(c["mini"], fit("Achievements: %d of %d" % (n, len(ACHIEVEMENTS)), MINI_W - 90))
            return
        v.text(c["status"], fit("%d of %d earned: +%d squeaks" % (n, len(ACHIEVEMENTS), paid), c["iw"] - 20))
        for r in c.get("rows", ()):
            a = r["a"]
            done = a[0] in got
            line = ach_line(a, done)
            if r["raw"] == (done, line):
                continue
            r["raw"] = (done, line)
            v.look(r["pic"], a[4], a[5] if done else HUE_LOCKED)
            v.text(r["nm"], fit(a[1], r["nw"]), Kit.HUE_GOOD if done else Kit.HUE_TEXT)
            v.text(r["rew"], "+%d" % a[3], Kit.HUE_INFO if done else Kit.HUE_TITLE)
            v.text(r["how"], fit(line, r["hw"]), Kit.HUE_INFO)

    def window_click(action, t):
        """Handle a click queued by a window: (window, what, extra...).

        Main window actions go to the shared window kit; Minimize flips and saves the window's state;
        the shop, Journeys and Playpen clicks change the page, start a trip or edit the member list.
        Every window that changed asks for its redraw.
        """
        which, what = action[0], action[1]
        if which == "main":
            Kit.win_action(what, st, KEY, TITLE, want_redraw, MIN_KEYS["main"])
        elif what == "toggle_min":
            k = which + "_min"
            st[k] = not st[k]
            Kit.save_min(MIN_KEYS[which], st[k])
            st[which + "_redraw"] = True
        elif which == "shop":
            if what == "cat":
                st["shop_cat"], st["shop_page"] = action[2], 0
            elif what == "prev":
                st["shop_page"] = max(0, st["shop_page"] - 1)
            elif what == "next":
                n = len(shop_items())
                st["shop_page"] = min(max(0, (n - 1) // st["shop_n"]), st["shop_page"] + 1)
            elif what == "act":
                shop_act(action[2], action[3])
            st["shop_redraw"] = True
        elif which == "quest":
            if what == "tab":
                quest["tab"] = action[2]
                st["quest_dirty"] = True
            elif what == "hunt":
                do_hunt(action[2], t)
            elif what == "med":
                do_meditate(action[2], t)
            elif what == "home":
                call_home(t)
            st["quest_redraw"] = True
        elif which == "pen":
            if what == "share":
                share()
            elif what == "rm":
                members = pen_members()
                n = action[2]
                if n < len(members) and not members[n]["mine"]:
                    mb = members[n]
                    st["guests"] = [gst for gst in st["guests"] if not (gst["uid"] == mb["uid"]
                                            and gst["owner"] == mb["owner"])]
                    save_guests()
                    say("%s went home." % mb["name"], Kit.HUE_INFO)
                    st["pen_redraw"] = True
            elif what == "add":
                # The code is pulled from the text box with a pattern, so stray spaces or text are ignored.
                m = CODE_RE.search(str(safe(lambda: wins["pen"]["c"]["code"].Text, "") or ""))
                gst = decode(m.group(1)) if m else None
                if gst is None:
                    say("that isn't a Mongotchi code (64 characters).", Kit.HUE_BAD)
                elif not add_guest(gst) and gst["uid"] == pet["uid"] and gst["owner"] == my_owner():
                    say("that's your own mongotchi's code.", Kit.HUE_INFO)

    def toggle_sub(action, t):
        """Open or close a sub-window from its action button.

        A window held in a zone cannot be closed from here. Opening the Playpen shares the code when the
        setting asks for it.
        """
        w = ACT_WIN[action]
        if st[w + "_open"]:
            if not Kit.zone_up(dock_key(w)):
                close_window(w)
        else:
            st[w + "_open"], st[w + "_redraw"] = True, True
            if w == "pen" and not pet["feral"] and settings["share_open"] and settings["share_min"] > 0:
                share()
            elif w == "pen":
                st["shared_at"] = t

    def adopt(action, t):
        """Start again with a new pup after the old one went wild."""
        if pet["feral"]:
            new_pet()
            st["redraw"] = True

    def release(action, t):
        """Release the pet: the first press asks for confirmation, a second press within 6 seconds does it."""
        if t - st["confirm"] < 6.0:
            st["confirm"] = 0.0
            say("%s released; a new pup arrives." % name(), Kit.HUE_INFO)
            new_pet()
            st["redraw"] = True
        else:
            st["confirm"] = t
        HOST.refresh_settings(KEY)

    # Button action name to its sub-window.
    ACT_WIN = {"shop": "shop", "playpen": "pen", "journey": "quest", "ach": "ach"}
    # Every queued action the tick can run, by name.
    ACTIONS = {"feed": do_feed, "play": do_play, "brush": do_brush, "cure": do_cure, "forage": do_forage, "pet": do_pet,
               "clean": do_clean, "lights": do_lights, "swat": do_swat, "window": window_click, "shop": toggle_sub,
               "playpen": toggle_sub, "journey": toggle_sub, "ach": toggle_sub, "adopt": adopt,
               "refresh_page": lambda action, t: HOST.refresh_settings(KEY), "release": release}
    # Page options: the width of the field column and the gap between rows.
    PAGE_OPTS = {"fw": 60, "ugap": 14}
    # Captions and tooltips of the settings page checkboxes.
    CHECK_TEXTS = {"gremlins": ("Gremlins raid the pantry", "A gremlin that reaches the pantry takes half the food"),
        "sounds": ("Play sounds", "Squeaks, munching, gremlins and music"),
        "remind": ("Remind me in the journal of its needs", "At most every %d min per need" % int(REMIND_EVERY / 60)),
        "offline": ("Keep living while the module is off (up to %d hours)" % OFFLINE_MAX_H,
                    "Off: time stops while the module is off (squeaks still trickle in)"),
        "listen": ("Add shared mongotchis to my playpen", "Picks up \"%s\" lines from the journal" % CODE_TAG),
        "share_open": ("Share my code when I open the Playpen",
                       "Only while re-share reminders are on; off: only Share posts it"),
        "comp": ("Follows me in the world", "Only you see it; \"<name> go home\" or \"<name> come\" work too"),
        "comp_talk": ("Talks over my head", "Head messages only you see"),
        "comp_help": ("Joins my fights (just for show)", "Dives at your war-mode target; no damage")}

    def page_table(w):
        """Return the settings page layout for width w: Pet, Playpen and Companion sections."""
        def checks(*keys):
            """Return the check box rows for the given settings keys, their captions cut to fit."""
            return [("check", k, fit(CHECK_TEXTS[k][0], w - 40), CHECK_TEXTS[k][1]) for k in keys]

        cap = "Click again to confirm" if time.time() - st["confirm"] < 6.0 else "Release %s" % name()
        return (("PET", [("text", "name", "Name:", "Up to %d letters (; = | , are dropped)" % NAME_MAX, {"tw": 130}),
                         ("num", "pace", "Pace:", "Need speed: 100 = normal, 200 = double", "%") + LIMITS["pace"],
                         ("num", "grem_min", "Gremlins every:", "Average minutes between raids (%d-%d; the Scarecrow "
                          "doubles it)" % LIMITS["grem_min"], "min") + LIMITS["grem_min"]]
                 + checks("gremlins", "sounds", "remind", "offline") + [("buttons", (("release", Kit.ART_CLOSE,
                     fit(cap, w - 70), "Start over with a new pup (squeaks, wardrobe, virtues and relics stay); "
                     "click twice within 6 s"),), {"bdy": 0})], {"align": True}),
                ("PLAYPEN", [("num", "share_min", "Remind to re-share every:", "Minutes between Share reminders while "
                              "the Playpen is open (%d-%d, 0 = never, and no post on opening)" % LIMITS["share_min"],
                              "min") + LIMITS["share_min"]]
                 + checks("listen", "share_open") + [("buttons", (("channel", Kit.ART_PAGE, "Share in: %s"
                     % CHANNELS[settings["share_ch"]][0], "Next chat for Share: Say, Party, Guild, Alliance or "
                     "Whisper"),), {"bdy": 0})]),
                ("COMPANION  (needs the Companion Charm)", checks("comp", "comp_talk", "comp_help")))

    def page_clicks(f):
        """Handle the settings page buttons: Release and the chat channel for Share."""
        if Kit.was_clicked(f.store, "release"):
            queue("release")()
        if Kit.was_clicked(f.store, "channel"):
            settings["share_ch"] = (settings["share_ch"] + 1) % len(CHANNELS)
            save_settings()
            queue("refresh_page")()

    def page_read(f, new):
        """Clean the typed name before it is stored."""
        new["name"] = clean_name(new["name"])

    def page_changed(old, new):
        """Settings page change hook: a new name redraws everything shortly after, and texts refresh."""
        if new["name"] != old["name"]:
            # A short delay lets a name being typed settle before the windows are rebuilt.
            st["redraw_at"] = time.time() + 1.5
        st["texts_at"] = 0.0

    cfg = Kit.Page(settings, page_table, save_settings, page_changed, PAGE_OPTS, empty=settings, adjust=page_read,
                   clicks=page_clicks)
    load_settings()

    def _start():
        """Start the module (client thread): reset the run state, load every save and open the windows.

        Loads the shop and guests before the pet and the achievements before catch_up, because the time
        away is added to them. Registers the main window and each sub-window with the Action Bar dock.
        The main window starts docked when the host says the bar is about to fold it in.
        """
        t = time.time()
        st.update({"shutting": False, "docked": HOST.dock_soon(KEY), "queue": [], "grem": None,
                   # The main window's minimized state is remembered, or the dock wants it folded.
                   "minimized": Kit.load_min(MIN_KEYS["main"]) or bool(HOST.dock_wanted(KEY)),
                   "redraw": False, "shop_redraw": False, "pen_redraw": False, "fit": None, "eat_until": 0.0,
                   "play_until": 0.0, "cure_until": 0.0, "brush_until": 0.0, "leave_until": 0.0,
                   "next_grem_ok": t + 60.0, "texts_at": 0.0, "next_chat": t + 10.0, "shop_open": False,
                   "pen_open": False, "quest_open": False, "quest_redraw": False, "listen_at": 0.0, "sleep_after": 0.0,
                   "pen_game": None, "comp": comp_new(), "hop": [], "read_at": 0.0, "jcodes": [], "jcmds": [],
                   "jcodes_due": False, "player": None, "close_at": 0.0, "full_told": {}, "shop_dirty": False,
                   "quest_dirty": False, "ach_open": False, "ach_redraw": False, "ach_due": False, "ach_at": 0.0,
                   "seasons": None, "season_at": 0.0, "fw_at": 0.0, "sim_acc": 0.0, "shop_n": SHOP_ROWS})
        load_settings()
        load_shop()
        load_guests()
        load_quest()
        load_ach()
        # Before the pen is drawn, so snow is there from the first frame.
        season_tick(t, force=True)
        if load_pet():
            # Live through the time the module was off (capped by the offline setting).
            catch_up()
        else:
            shop["last"] = t
            # A first save of the shop goes with the new pet.
            st["shop_dirty"] = True
            new_pet()
        # The first run grants what was earned before.
        ach_check(t)
        st["last_t"] = t
        build_window()
        # The main window folds into the Action Bar tray from its gold arrow.
        hooks = Kit.dock_hooks(TITLE, TRAY_ICON, st, wins["main"], want_redraw, fit=zone_fit)
        # In a zone it lays itself out for its slot exactly.
        hooks.update({"exact": True, "verify": True, "drawn_at": zone_drawn_at})
        HOST.dock_add(KEY, hooks)
        subfit.clear()
        for which in SUBS:
            HOST.dock_add(dock_key(which), sub_hooks(which))

    def _tick():
        """One module step (client thread, every interval): clicks, the pet's life, windows and drawing.

        Order: read the client, run queued clicks, advance the sim, finish timed things (eating, play,
        trips), the gremlin, chatter, the companion, achievements, then redraw what asked and refresh.
        Every read and client call runs in place; nothing here waits.
        """
        if win["g"] is None:
            return
        t = time.time()
        # Close and sub-window Close clicks are latched, so polling four times a second is enough.
        if t - st["close_at"] >= 0.25:
            st["close_at"] = t
            if Kit.closed(win):
                # The main window was closed: the disposed hook turns the module off.
                return
            for which in WINDOWS:
                w = wins[which]
                if which != "main" and w["g"] is not None and Kit.was_clicked(w["store"], "close"):
                    close_window(which)
        read_client(t)
        # Clicks are lived first: the time before the click passes with the pet as it was, then the click
        # shows its result at once and earns what it earned.
        if st["queue"]:
            flush_sim()
            st["texts_at"] = 0.0
            st["ach_due"] = True
        while st["queue"]:
            action = st["queue"].pop(0)
            kind = "window" if isinstance(action, tuple) else action
            if kind in ACTIONS:
                ACTIONS[kind](action, t)
        # Release confirmation ran out: the settings page shows Release and the name again.
        if st["confirm"] and not 0.0 <= t - st["confirm"] < 6.0:
            st["confirm"] = 0.0
            HOST.refresh_settings(KEY)
        # Capped, so a long stall (a client hiccup) cannot lose the pet a lot of time at once.
        dt = max(0.0, min(5.0, t - st["last_t"]))
        st["last_t"] = t
        season_tick(t)
        # The pet lives in steps of SIM_EVERY, not on every tick: its needs move about 0.01 a second and
        # catch_up already uses 60 second steps. An event (a heap, the farmer, falling asleep) comes up to
        # a second later.
        acc = st["sim_acc"] + dt
        simmed = acc >= SIM_EVERY
        if simmed:
            st["sim_acc"] = 0.0
            run_sim(acc)
        else:
            st["sim_acc"] = acc
        full = not st["minimized"]
        if st["eat_food"] is not None and t >= st["eat_until"]:
            if st["eat_food"][2]:
                finish_eat()
            else:
                st["eat_food"] = None
        if st.get("sleep_after") and t >= st["sleep_after"]:
            st["sleep_after"] = 0.0
            if awake_home():
                pet["asleep"] = True
                st["say"] = ""
        if st["play_until"] and t >= st["play_until"]:
            st["play_until"] = 0.0
            finish_play()
            st["play_toy"] = None
        if pet["away"] and t >= st["away_until"] and t >= st["leave_until"]:
            finish_away()
        gremlin_tick(t, dt, full)
        sounds_due(t)
        chatter(t)
        # Reminders are only looked at when the sim ran.
        if simmed:
            remind(t)
        listen()
        comp_tick(t)
        if st["ach_due"] or not st["ach_at"] - ACH_EVERY <= t < st["ach_at"]:
            ach_check(t)
        if st["pen_open"]:
            # Never a timed post in chat (unattended speech): only a journal reminder to press Share,
            # and only with Share my code when I open the Playpen on.
            if settings["share_open"] and settings["share_min"] \
                    and t - st["shared_at"] >= settings["share_min"] * 60 and not pet["feral"]:
                st["shared_at"] = t
                say("time to Share %s's code again." % name(), Kit.HUE_INFO)
            if len(st["guests"]) and t - st["social_at"] >= 60.0:
                st["social_at"] = t
                earn("social", min(3, len(st["guests"])))
                if not pet["asleep"] and not pet["feral"]:
                    bump("joy", 2)
        # A delayed redraw of everything (after a rename).
        if st.get("redraw_at") and t >= st["redraw_at"]:
            st["redraw_at"] = 0.0
            st["redraw"] = st["quest_redraw"] = True
        if st.get("redraw"):
            st["redraw"] = False
            build_window()
            if st["pen_open"]:
                st["pen_redraw"] = True
        # Rebuild the sub-windows that asked for it, if they are still open.
        for which, build, redo, redraw, is_open in REDRAWS:
            if st.get(redraw):
                st[redraw] = False
                if st[is_open]:
                    build()
        # Text is rewritten once a second; bars and drawing run on every tick.
        texts = t - st.get("texts_at", 0.0) >= 1.0
        if texts:
            st["texts_at"] = t
        refresh(t, texts)
        for which, build, redo, redraw, is_open in REDRAWS:
            if st[is_open]:
                redo(t, texts)
        run_hop()
        # Save at most every SAVE_EVERY seconds, with the time not lived yet lived first.
        if t - st["saved_at"] >= SAVE_EVERY:
            flush_sim()
            save_pet()

    # Seconds of pet life lived per sim step.
    SIM_EVERY = 1.0

    def run_sim(secs):
        """Let the pet live secs seconds: needs move, squeaks trickle in and what happened is told."""
        events = []
        sim(secs, events)
        earn("passive", PASSIVE_PER_H * secs / 3600.0)
        if events:
            handle_events(events)
            # It may have grown up.
            st["ach_due"] = True

    def flush_sim():
        """Live the time not lived yet, now (before a save and at stop)."""
        if st.get("sim_acc", 0.0) > 0.0:
            secs, st["sim_acc"] = st["sim_acc"], 0.0
            run_sim(secs)

    # Per sub-window: name, build, refresh, redraw flag and open flag, in one table for the tick.
    REDRAWS = tuple((w, b, r, w + "_redraw", w + "_open") for w, b, r in (("shop", build_shop, refresh_shop),
        ("pen", build_pen, refresh_pen), ("quest", build_quest, refresh_quest), ("ach", build_ach, refresh_ach)))

    def _interval():
        """Return the tick interval: fast while the pen is on view, slower when minimized."""
        return 0.1 if not st["minimized"] or (st["pen_open"] and not st["pen_min"]) else 0.5

    def _stop():
        """Stop the module (script thread): save everything and close every window.

        Marks the module as shutting down first, so a disposed window is not treated as a close click.
        """
        st["shutting"] = True
        HOST.dock_remove(KEY)
        for which in SUBS:
            HOST.dock_remove(dock_key(which))
        for which in WINDOWS:
            save_pos(which)
        for k, var in MIN_KEYS.items():
            Kit.save_min(var, st["minimized" if k == "main" else k + "_min"])
        save_settings()
        # The last second is lived too.
        flush_sim()
        # This saves the shop, quests and achievements too.
        save_pet(final=True)
        for which in WINDOWS:
            g, wins[which]["g"] = wins[which]["g"], None
            Kit.dispose(g)
        st["shop_open"] = st["pen_open"] = st["quest_open"] = st["ach_open"] = False

    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
            "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed, "interval": _interval}


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("mongotchi", "Mongotchi", "A pet mongbat to raise and dress up", _module_mongotchi, 0.1, category="Extras")
