def _module_mongotchi():
	cA=HOST.dock_add;cB=HOST.dock_remove;bt=HOST.refresh_settings;ag="mongotchi";Y="Mongotchi";cC="Mongotchi_settings";cD=8441;import _random
	class Rng(_random.Random):
		def below(self,n):
			k=n.bit_length();r=self.getrandbits(k)
			while r>=n:r=self.getrandbits(k)
			return r
		def randint(self,a,b):
			c,d=int(a),int(b)
			if c!=a or d!=b or d<c:raise ValueError("empty or non-integer range for randint()")
			return c+self.below(d-c+1)
		def uniform(self,a,b):return a+(b-a)*self.random()
		def choice(self,seq):
			n=len(seq)
			if not n:raise IndexError("Cannot choose from an empty sequence")
			return seq[self.below(n)]
	l=Rng();aF=9638;aG=2;ey="#FFFFFF";cE=3899;ez=3847;eA=4979;ap=[(2512,"an apple",20),(2505,"a ham",35),(2427,"a fish steak",30),(2513,"some grapes",20),(4155,"a loaf of bread",25),(5919,"a banana",20)];bW=1161;bX=2213;bY=1102;a8=1153;eB=1152;cF=2006;eC=1505;eD=1173;cG=33;eE=38;eF=1201;bZ=425;cH=58;cI=87;eG=480;eH=510;eI=1066;eJ=946;cJ=1078;eK=.15;aU=53;eL=54;eM=43;eN=30.;eO=20.;eP=15.;eQ=15.;eR=50.;eS=6.;eT=12.;eU,eV=30,60;b_=3;b0=tuple("mess%d"%hL for hL in range(b_));eW=.5;eX=.3;eY=1.;eZ=2.;e_=.5;e0=1.;e1=6.;e2=75.;e3=5;e4=12;cK=20;cL=30;cM=(25,45);b1=20.;e5=60.;cN=(2,4);e6=20;e7=15;ai=10;e8=.01;Q={"hon_price":.02,"com_pet":1.,"com_joy_loss":.03,"com_heal_secs":4.,"val_guard":.05,"val_danger":.06,"val_dive":.04,"jus_back":.05,"jus_squeaks":.1,"sac_per":4,"sac_energy":1,"sac_forage_min":5,"sac_hunt_min":8,"hnr_squeaks":.02,"spi_meditate":.05,"spi_relic":.04,"spi_sick":.05,"spi_copy":.03,"hum_hunger":.02,"hum_need":.04,};e9=60.;fa=.25;fb=30.;fc=3600.;fd=6.;cO=2.5;fe=8.;ff=60.;fg=7.;cP=120.;fh=.35;cQ=900.;b2=24;cR=12;b3=30.;a9={"feed":2,"treat":2,"brush":4,"play":5,"clean":3,"cure":2,"pet":1,"forage":1,"swat":5,"guard":3,"trap":10,"social":1,"grow":25};fi=1.25;az=6;b4="Mongotchi code:";bu=[("Say","Msg"),("Party","PartyMsg"),("Guild","GuildMsg"),("Alliance","AllyMsg"),("Whisper","WhisperMsg")];cS=2.;cT="Mongotchi_state";cU="Mongotchi_shop";cV="Mongotchi_guests";cW="Mongotchi_quests";cX="Mongotchi_seasonal";cY="Mongotchi_achievements";cZ={"main":"Mongotchi_pos","shop":"Mongotchi_shop_pos","pen":"Mongotchi_pen_pos","quest":"Mongotchi_quest_pos","ach":"Mongotchi_ach_pos"};fj={"main":(200,200),"shop":(510,200),"pen":(200,640),"quest":(510,200),"ach":(540,240)};bv=("shop","pen","quest","ach","main");b5={"shop":"Shop","pen":"Playpen","quest":"Journeys","ach":"Achievements"};aA={"main":"Mongotchi_min","shop":"Mongotchi_shop_min","pen":"Mongotchi_pen_min","quest":"Mongotchi_quest_min","ach":"Mongotchi_ach_min"};bx,c_=300,448;c0=cD;at,by=240,46;SW=380;c1=6;b6=420;JW=480;ba=8;b7=[("halloween","Halloween",(10,15),(11,1)),("winter","Winter",(12,1),(2,29)),("newyear","New Year",(12,31),(1,2))];fk=(10,31);c2=3.;c3=60.;c4=14;c5=(12.,24.);b8=(2.5,5.);c6=5.;fl=490;c7=1109;c8=600;fm=(4014,4016,4015);M,T=Kit.MARGIN,Kit.GAP;IW=bx-2*M;r,B,C,L=M,M+30+T,IW,132;SY,SH=B+L+T,122;AY,AH=SY+SH+T,116;J,ab=56,48;c9,aV=r+10,r+C-10-J;am,aB=B+26,B+L-4-ab;aq=B+L-36;ak,aH=28*aG,31*aG;au=B+L-aH-2;aC,fn=r+C-ak-4,r+60;da=5;db=109;ac,ae,QW,QH=M,M+30+T,b6-2*M,180;aI,aJ=ac+10,ac+QW-10-J;aK,bz=ae+26,ae+QH-18-ab;b9,dc=ae+QH+T,84;dd,de=b9+dc+T,40;ca=dd+de+M;bb=[("food","Fullness"),("joy","Happiness"),("energy","Energy"),("clean","Cleanliness")];fo=[(95,"Wonderfully Happy"),(85,"Extremely Happy"),(75,"Very Happy"),(65,"Rather Happy"),(55,"Happy"),(45,"Content"),(35,"Unhappy"),(25,"Rather Unhappy"),(12,"Extremely Unhappy"),(-1,"Confused")];an={"idle":["*squeak*","*flap flap*","*chitters*","Mong!","*hangs around*","*squeak squeak*","*sniffs the air*"],"hungry":["*tummy rumbles*","Food? FOOD?","*eyes the pantry*"],"bored":["*sighs*","*yawns at you*","Play?"],"dirty":["*sniffs... ew*","*holds its nose*"],"sick":["*cough cough*","*shivers*"],"happy":["<3","*happy squeak*","*nuzzles you*"],};fp=["*boops %s*","*tags %s!*","*chases %s*","*squeaks at %s*","*does a loop around %s*","*shares a crumb with %s*","*plays tag with %s*"];cb=[(hM,hN,None if hM in("treat","upg","ult")else hM)for hM,hN in(("treat","Treats"),("hat","Hats"),("neck","Necklaces"),("dye","Dyes"),("aura","Auras"),("toy","Toys"),("pers","Personality"),("decor","Decor"),("hang","Hanging"),("title","Titles"),("voice","Voices"),("ncol","Name colours"),("upg","Upgrades"),("ult","Ultimate"))];cc=("dye","toy","pers","voice","ncol")
	def I(*row,**a):return dict(zip(("id","cat","name","price","gfx","hue","desc"),row),**a)
	av=[I("t_peach","treat","Sugared Peach",15,539,0,"+15 happy, +5 full",joy=15,food=5),I("t_muffin","treat","Muffin",20,2538,0,"+15 full, +10 happy",food=15,joy=10),I("t_cake","treat","Cake",40,2537,0,"+35 happy, +15 full, crumbs",joy=35,food=15,clean=-5),I("t_honey","treat","Jar of Honey",30,2540,0,"+25 energy, +10 happy",energy=25,joy=10),I("t_cheese","treat","Wheel of Cheese",30,2430,0,"+40 full",food=40),I("t_sausage","treat","Sausage",25,2496,0,"+25 full, +10 happy",food=25,joy=10),I("t_ribs","treat","Cut of Ribs",35,2546,0,"+45 full, +5 happy",food=45,joy=5),I("t_melon","treat","Watermelon",25,3164,0,"+20 full, +10 clean, +10 happy",food=20,clean=10,joy=10),I("t_carrot","treat","Carrot",20,3191,0,"Chases off the next gremlin",food=10,guard=True),I("t_pumpkin","treat","Pumpkin",35,3178,0,"+20 happy, +20 full, spooky",joy=20,food=20,spooky=True),I("t_milk","treat","Pitcher of Milk",25,2544,0,"+10 happy, then bed",joy=10,energy=10,sleep=True),I("t_cider","treat","Jug of Cider",30,2504,0,"+20 happy, a bit dizzy",joy=20,dizzy=True),I("t_honeydew","treat","Honeydew Melon",25,3188,0,"+20 full, +15 happy",food=20,joy=15),I("t_stew","treat","Healing Stew",45,2416,0,"Cures sickness, +20 full",food=20,cure=True),I("h_wizard","hat","Wizard's Hat",120,5912,1156,"Kal Vas Flam!"),I("h_witch","hat","Witch's Hat",130,5910,1,"For All Hallows' Eve"),I("h_jester","hat","Jester Hat",90,5916,1157,"For the court fool"),I("h_tricorne","hat","Tricorne",100,5915,1,"Arr, a pirate bat"),I("h_floppy","hat","Floppy Hat",70,5907,1206,"Soft and pink"),I("h_straw","hat","Straw Hat",60,5911,0,"Farm-fresh style"),I("h_feather","hat","Feathered Hat",110,5914,1173,"Bard chic"),I("h_bonnet","hat","Bonnet",70,5913,1201,"Sweet and proper"),I("h_skull","hat","Skullcap",50,5443,1,"Rogue's choice"),I("h_bandana","hat","Bandana",50,5439,33,"Brigand red"),I("h_tribal","hat","Tribal Mask",140,5449,0,"Savage and proud"),I("h_circlet","hat","Royal Circlet",220,11119,0,"Fit for Lord British's court"),I("h_gemcirc","hat","Gemmed Circlet",260,11120,0,"Sparkles in the moonlight"),I("h_jcap","hat","Jester's Cap",90,5934,1172,"Bells not included"),I("h_cap","hat","Cap",40,5909,1505,"Plain and orange"),I("h_widebrim","hat","Wide-Brim Hat",100,5908,1177,"Golden and grand"),I("h_exec","hat","Executioner's Cap",150,3971,1,"Gremlins beware"),I("n_gold","neck","Gold Necklace",80,4232,0,"Plain gold"),I("n_chain","neck","Gold Chain",100,4233,0,"Bling, mongbat style"),I("n_silver","neck","Silver Chain",90,7946,0,"Shiny and cool"),I("n_beads","neck","Beads",60,4235,0,"Colourful beads"),I("n_jewel","neck","Jewelled Necklace",160,4229,1177,"Glitters with gems"),I("n_leather","neck","Leather Gorget",70,5063,0,"Adventurer's guard"),I("n_plate","neck","Plate Gorget",140,5139,0,"A tiny knight")];av+=[I(hO,"dye",hP,hQ,aF,hR,hS)for hO,hP,hQ,hR,hS in(("d_natural","Natural",0,0,"Its own brown"),("d_ice","Ice Blue",120,1152,"Frosty"),("d_gold","Gold",200,1177,"Worth its weight"),("d_teal","Teal",100,1173,"Sea-glass green"),("d_crimson","Crimson",120,1157,"Blood-red"),("d_purple","Royal Purple",140,1158,"Regal"),("d_verdigris","Verdigris",100,2968,"Old bronze"),("d_silver","Silver",160,1150,"Gleaming"),("d_sapphire","Sapphire",160,1195,"Deep blue"),("d_orchid","Orchid",120,1168,"Pretty in purple"),("d_violet","Violet",120,1171,"Twilight"),("d_shadow","Shadow",180,1109,"Blends into the night"),("d_rose","Rose",100,1206,"Blushing"),("d_midnight","Midnight",180,1156,"Darkest blue"))];av+=[I("a_holy","aura","Holy Light",250,14144,0,"Blue-white sparkles",seq=(14138,16)),I("a_embers","aura","Embers",250,14160,0,"Red sparks",seq=(14154,16)),I("a_star","aura","Starlight",300,14176,0,"Stars of blue and gold",seq=(14170,16)),I("a_fairy","aura","Fairy Dust",300,14192,0,"Twinkling motes",seq=(14186,15)),I("a_snow","aura","Snowfall",280,14210,1153,"Gentle snowflakes",seq=(14202,15)),I("a_phoenix","aura","Phoenix Sparks",350,14144,1161,"Golden fire",seq=(14138,16)),I("a_toxic","aura","Toxic Glitter",300,14144,1405,"Poisonously pretty",seq=(14138,16)),I("a_bluegate","aura","Blue Moongate",400,3948,0,"A halo of moonlight"),I("a_redgate","aura","Red Moongate",400,3546,0,"A gate of crimson"),I("a_halo","aura","Golden Halo",500,3948,1177,"Saintly"),I("a_void","aura","Void Gate",450,3948,1158,"From beyond"),I("a_storm","aura","Lightning",450,14672,0,"Crackling energy",seq=(14662,31)),I("a_rainbow","aura","Rainbow",600,14144,0,"Every colour at once",seq=(14138,16),rainbow=True),I("y_yarn","toy","Ball of Yarn",0,3613,0,"The classic",motion="bounce"),I("y_ball","toy","Bouncy Ball",60,3699,33,"Boing! +5 happy",motion="bouncy",joy=5),I("y_feather","toy","Feather",50,7121,0,"Floats down; less tiring",motion="float",energy=5),I("y_rat","toy","Toy Rat",90,8483,0,"+10 happy, tiring",motion="scurry",joy=10,energy=-5),I("y_dice","toy","Dice",70,4007,0,"A gamble: 10-45 happy",motion="dice"),I("y_crystal","toy","Crystal Ball",200,3629,0,"+5 squeaks a game",motion="hover",squeaks=5),I("y_drum","toy","Drum",120,3740,0,"It dances along",motion="music",snd=56),I("y_tamb","toy","Tambourine",100,3741,0,"Shake shake shake",motion="music",snd=82),I("y_lute","toy","Lute",150,3763,0,"A bard's tune",motion="music",snd=76),I("y_harp","toy","Lap Harp",180,3762,0,"Soothing: +10 happy",motion="music",snd=69,joy=10),I("y_flute","toy","Bamboo Flute",130,10245,0,"Toot toot",motion="music",snd=61),I("p_cheerful","pers","Cheerful",0,3643,0,"Sunny and easy-going"),I("p_playful","pers","Playful",150,3643,1206,"Loves games; gets bored faster",play=1.5,joy_rate=1.2,speed=1.3,lines=["*does a loop-de-loop*","Tag! You're it!","*bounces off the walls*"]),I("p_lazy","pers","Lazy",100,3643,1109,"Tires slowly, sleeps deeply, flies slow",energy_rate=.6,sleep=1.25,speed=.6,lines=["*yawns*","*naps mid-flap*","Five more minutes..."]),I("p_glutton","pers","Gluttonous",120,3643,1505,"Always hungry; food cheers it",food_rate=1.3,feed_joy=15,lines=["Snack time?","*drools*","*sniffs for crumbs*"]),I("p_brave","pers","Brave",200,3643,33,"Chases off gremlins more often",guard=.75,lines=["*flexes*","Gremlins fear me!","*guards the pantry*"]),I("p_shy","pers","Shy",120,3643,1152,"Quiet; loves being petted",pet=8,chat=.4,lines=["*hides behind its wings*","...squeak","*peeks at you*"]),I("p_mischief","pers","Mischievous",180,3643,1405,"More food; may steal some back from gremlins",forage=1,stealback=.3,lines=["*snickers*","*eyes the gremlins' stash*","*hides a grape*"]),I("p_grumpy","pers","Grumpy",100,3643,1157,"Hard to please, slow to sulk",joy_rate=.85,lines=["*grumbles*","Hmph.","*glares at the gremlin hole*"]),I("p_scholar","pers","Scholarly",250,3643,1156,"Earns 20% more squeaks",squeak=1.2,lines=["*reads a tiny spellbook*","*mutters Kal Vas Flam*","*adjusts its spectacles*"]),I("p_drama","pers","Dramatic",120,3643,1158,"Everything is a tragedy (or triumph)",chat=1.6,lines=["*faints dramatically*","Woe! WOE!","*poses heroically*"]),I("o_pillow","decor","Straw Pillow",120,4586,0,"Sleeps 25% better",sleep=1.25),I("o_flowers","decor","Potted Flowers",60,4554,0,"A splash of colour"),I("o_fern","decor","Fern",50,3231,0,"Leafy"),I("o_cactus","decor","Cactus",50,3365,0,"Don't hug it"),I("o_globe","decor","Globe",90,4167,0,"Sosaria, in miniature"),I("o_mushroom","decor","Mushrooms",40,3340,0,"Mysterious fungi"),I("o_pumpkin","decor","Pumpkin",60,3178,0,"Happy Halloween"),I("o_crystal","decor","Crystal Ball",150,3629,0,"It sees all"),I("o_wildflowers","decor","Wildflowers",50,3203,0,"Fresh from the meadow"),I("o_candles","decor","Candelabra",100,2845,0,"Cosy candlelight"),I("g_lantern","hang","Lantern",60,2581,0,"A warm glow"),I("g_hanglamp","hang","Hanging Lantern",80,2586,0,"Swings gently"),I("g_chimes","hang","Wind Chimes",70,10290,0,"Tinkle tinkle"),I("g_fancy","hang","Fancy Wind Chimes",110,10291,0,"Crystal clear"),I("x_brave","title","the Brave",80,3827,0,"Fearless"),I("x_fluffy","title","the Fluffy",60,3827,0,"So soft"),I("x_magnif","title","the Magnificent",150,3827,0,"Behold!"),I("x_britain","title","of Britain",100,3827,0,"A city bat"),I("x_belfry","title","of the Belfry",120,3827,0,"Lord of the bell tower"),I("x_spooky","title","the Spooky",90,3827,0,"Boo!"),I("x_bane","title","Gremlin Bane",100,3827,0,"Needs 10 gremlins swatted",req="swats"),I("x_greater","title","the Greater",100,3827,0,"Needs a Greater Mongotchi",req="greater"),I("x_elder","title","the Elder",200,3827,0,"Needs an age of 24 hours",req="elder"),I("x_avatar","title","the Avatar",1000,3827,1177,"Needs every virtue at level 5",req="avatar"),I("x_explorer","title","the Explorer",150,3827,0,"Needs 8 different relics",req="relics"),I("x_pilgrim","title","the Pilgrim",200,3827,0,"Needs a virtue at level 10",req="pilgrim")];av+=[I(hT,"voice",hU,hV,hW,0,hX,snd=hY)for hT,hU,hV,hW,hX,hY in(("v_mongbat","Mongbat",0,8441,"Its own squeak",422),("v_cat","Cat",60,8475,"Meow?",105),("v_dog","Dog",60,8476,"Woof!",133),("v_chicken","Chicken",50,8401,"Bawk!",110),("v_bird","Songbird",60,8474,"Tweet",23),("v_pig","Pig",50,8449,"Oink",196),("v_cow","Cow",50,8451,"Moo",120),("v_sheep","Sheep",50,8422,"Baa",214),("v_frog","Bullfrog",60,8496,"Ribbit",614),("v_wisp","Wisp",120,8448,"Ethereal chimes",466),("v_ghost","Ghost",100,9671,"Ooooo",382),("v_dragon","Dragon",200,8406,"ROAR",362),("v_daemon","Daemon",200,8452,"From the abyss",357),("v_gazer","Gazer",120,8436,"Blorp",377))];av+=[I("c_gold","ncol","Gold",0,0,53,"The usual"),I("c_white","ncol","White",40,0,1153,"Clean and bright"),I("c_green","ncol","Green",40,0,68,"Fresh"),I("c_red","ncol","Red",40,0,33,"Fierce"),I("c_blue","ncol","Sky Blue",50,0,1173,"Breezy"),I("c_pink","ncol","Pink",50,0,1201,"Adorable"),I("c_fire","ncol","Fire",80,0,1161,"Blazing"),I("c_ice","ncol","Ice",80,0,1152,"Chilly"),I("u_pantry","upg","Bigger Pantry",150,3703,0,"Holds %d food"%cK),I("u_trap","upg","Gremlin Trap",40,4343,0,"Catches the next gremlin (+10 sq)",uses=True),I("u_luck","upg","Lucky Black Pearl",250,3962,0,"+25% squeaks, forever"),I("u_groom","upg","Grooming Kit",100,4979,0,"Brushing does double"),I("u_feeder","upg","Auto-Feeder",200,3711,0,"Feeds it from the pantry when hungry"),I("u_ward","upg","Scarecrow",300,7732,0,"Half as many gremlins"),I("u_companion","ult","Companion Charm",2500,3676,1161,"Follows you in the world and joins fights",toggle=True),I("u_war","ult","War Training",800,8012,33,"Dives at foes twice as often, with fireballs",req="charm"),I("u_shiny","ult","Shiny Sense",600,3821,0,"Finds shiny things twice as often on walks",req="charm"),I("h_orcmask","hat","Orc Mask",90,5147,0,"An orc costume",season="halloween"),I("h_bearmask","hat","Bear Mask",100,5445,0,"A bear costume: rawr!",season="halloween"),I("h_deermask","hat","Deer Mask",100,5447,0,"Antlers and all",season="halloween"),I("d_ghost","dye","Ghost Costume",150,aF,1153,"A sheet with eye holes",season="halloween"),I("d_pumpkin","dye","Pumpkin Costume",150,aF,1505,"Round, orange and grinning",season="halloween"),I("t_pie","treat","Pumpkin Pie",35,4161,0,"+25 full, +15 happy, spooky",food=25,joy=15,spooky=True,season="halloween"),I("t_pbread","treat","Pumpkin Bread",30,4155,1505,"+25 full, +10 happy",food=25,joy=10,season="halloween"),I("h_wintercap","hat","Winter Cap",70,5909,1153,"Warm and woolly",season="winter"),I("h_holiday","hat","Holiday Hat",110,5912,33,"Red, pointy and festive",season="winter"),I("h_snowbonnet","hat","Snow Bonnet",80,5913,1152,"Frosted lace",season="winter"),I("o_snowman","decor","Snowman",100,9000,0,"Carrot nose included",season="winter"),I("o_gifts","decor","Gift Box",80,9002,0,"No peeking!",season="winter"),I("g_mistletoe","hang","Mistletoe",70,9076,0,"Who's under it?",season="winter"),I("g_wreath","hang","Holly Wreath",90,9004,0,"Evergreen and berries",season="winter"),I("t_ginger","treat","Gingerbread Man",25,11233,0,"+20 happy, +10 full",joy=20,food=10,season="winter"),I("t_cane","treat","Candy Cane",25,11229,0,"+25 energy, +5 happy",energy=25,joy=5,season="winter"),I("h_partycap","hat","Party Cap",90,5934,1177,"Ring in the new year",season="newyear"),I("a_fireworks","aura","Fireworks",400,14176,0,"Bursts of every colour",seq=(14170,16),rainbow=True,season="newyear"),I("t_fizz","treat","Sparkling Cider",30,8061,0,"+20 happy, +10 energy, fizzy",joy=20,energy=10,dizzy=True,season="newyear"),I("x_festive","title","the Festive",120,3827,0,"Toasts the new year",season="newyear"),];W=dict((hZ["id"],hZ)for hZ in av);bc={}
	for df in av:bc.setdefault(df["cat"],[]).append(df)
	dg=set(h_["id"]for h_ in av if h_["price"]==0);dh=dict((h0[0],h0[1])for h0 in b7);di=[h1 for h1 in av if h1.get("season")];bA=frozenset(h2["id"]for h2 in di);fq=("season","Seasonal",None);dj=("dye","hat","neck","aura","pers","toy","title","voice","ncol","decor","hang");bd=[1157,1505,1177,1405,1173,1156,1158,1206]
	def aW(k):return int(round(Q[k]*100))
	al=[("hon","Honesty","Dagger Isle","Shop prices %d%% lower",aW("hon_price")),("com","Compassion","the Britain road","Petting +%d happy; heals you sooner",int(Q["com_pet"])),("val","Valor","the isle south of Jhelom","Guards the pantry +%d%%; hunts safer; dives sooner",aW("val_guard")),("jus","Justice","the Yew woods","Wins back %d%% of stolen food",aW("jus_back")),("sac","Sacrifice","the Minoc desert","Brings +%d food home; trips cost less energy",-Q["sac_per"]),("hnr","Honor","the Trinsic road","%d%% more squeaks from everything",aW("hnr_squeaks")),("spi","Spirituality","the Skara Brae road","Meditation +%d%%; relic luck up; sickness down",aW("spi_meditate")),("hum","Humility","the isle off Magincia","Hunger %d%% slower; needs sting less",aW("hum_hunger")),];aL=[h3[0]for h3 in al];dk=dict((h4[0],h4)for h4 in al);dl={"hon":["*looks you straight in the eye*","*would never fib*"],"com":["*nuzzles you gently*","*checks that you're all right*"],"val":["*puffs up bravely*","*guards the pen*"],"jus":["*weighs the crumbs fairly*","*glares at the gremlin hole*"],"sac":["*offers you a crumb*","*saves the last bite for you*"],"hnr":["*bows with dignity*","*keeps its word*"],"spi":["*hums an old hymn*","*meditates on its perch*"],"hum":["*bows its little head*","*is content with a crumb*"],};aX=[("r_horseshoe","a lucky horseshoe",4022,0),("r_goldegg","a golden egg",2485,1177),("r_mandrake","a fat mandrake root",3974,0),("r_glowshroom","a glowing mushroom",3340,1173),("r_ore","a shiny ore nugget",6585,1150),("r_goldingot","a gold ingot",7154,1177),("r_conch","a conch shell",4036,0),("r_blackpearl","a perfect black pearl",3962,0),("r_fang","a silver serpent fang",3966,1150),("r_eye","a serpent's eye emerald",3856,0),("r_obsidian","a shard of obsidian",3977,0),("r_phoenix","a phoenix feather",7121,1161),("r_scale","a dragon scale",9908,0),("r_dblood","a vial of dragon's blood",3970,0),("r_scroll","a scroll of ancient lore",3637,0),("r_sextant","a cracked sextant",4183,0),];bB=dict((h5[0],h5)for h5 in aX)
	def aD(*row):return dict(zip(("id","name","mins","danger","req","bad","hint","loot"),row))
	ao=[aD("farm","The Britain Farmlands",8,.05,None,"an angry farmer's dog chased it off","apples, carrots, a few squeaks",[(5,"sq",4,10),(5,"food",1,2),(2,"treat","t_peach",0),(2,"treat","t_carrot",0),(1,"treat","t_milk",0),(1.2,"relic","r_horseshoe",0),(.4,"relic","r_goldegg",0)]),aD("yew","The Spiritwood, Yew",12,.1,None,"it got lost among the trees","honey, mushrooms, roots",[(5,"sq",6,14),(3,"food",1,2),(2,"treat","t_honey",0),(1,"treat","t_honeydew",0),(1.2,"relic","r_mandrake",0),(.4,"relic","r_glowshroom",0)]),aD("minoc","The Minoc Mines",15,.15,("stage",1),"a rockfall nearly caught it","squeaks, ore, the odd gold ingot",[(6,"sq",10,25),(1,"food",1,1),(1,"trap",0,0),(1,"treat","t_cheese",0),(1.2,"relic","r_ore",0),(.4,"relic","r_goldingot",0)]),aD("ship","The Sunken Ship, off Ocllo",18,.2,("stage",1),"a sea serpent surfaced beside it","fish, shells, pearls",[(4,"sq",8,20),(4,"food",1,3),(1,"treat","t_melon",0),(1,"treat","t_ribs",0),(1.2,"relic","r_conch",0),(.4,"relic","r_blackpearl",0)]),aD("terra","Terra Sanctum",22,.3,("virtue","val",2),"a silver serpent bit it","silver serpent fangs, silk, squeaks",[(5,"sq",10,24),(1,"food",1,2),(1,"trap",0,0),(1,"treat","t_stew",0),(1.5,"relic","r_fang",0),(.4,"relic","r_eye",0)]),aD("volcano","The Volcano, Hythloth Island",28,.4,("virtue","val",4),"it singed its wings on the lava","obsidian, sulphurous ash, phoenix feathers",[(5,"sq",12,30),(1,"trap",0,0),(1,"treat","t_pumpkin",0),(1,"treat","t_cider",0),(1.5,"relic","r_obsidian",0),(.4,"relic","r_phoenix",0)]),aD("destard","Destard",35,.5,("virtue","val",6),"a dragon woke up","dragon scales and hoard gold",[(5,"sq",20,45),(1,"treat","t_cake",0),(1,"treat","t_sausage",0),(1,"trap",0,0),(1.5,"relic","r_scale",0),(.5,"relic","r_dblood",0)]),aD("lycaeum","The Lycaeum, Moonglow",15,.05,("virtue","spi",2),"a librarian shooed it out","scrolls, squeaks, odd instruments",[(6,"sq",10,22),(1,"food",1,1),(1,"treat","t_muffin",0),(1.2,"relic","r_scroll",0),(.4,"relic","r_sextant",0)]),];fr=dict((h6["id"],h6)for h6 in ao);dm=["Treasure hunts","Meditation","Relics"];fs=502;aM=[("grown","All grown up","Raise a pup to adulthood",10,aF,0,"stage",1),("greater","Well raised","Raise a Greater Mongotchi",40,aF,bW,"stage",2),("elder","Elder","A mongotchi 24 hours old",30,6160,0,"age",24),("swat1","Swat!","Swat a gremlin",5,4163,0,"swats",1),("swat25","Gremlin bane","Swat 25 gremlins",30,3971,1,"swats",25),("trap","Snap!","Catch a gremlin in a trap",10,4343,0,None,1),("sq1k","A thousand squeaks","Earn 1,000 squeaks",25,3821,0,"earned",1000),("sq10k","Squeak hoard","Earn 10,000 squeaks",100,3823,0,"earned",10000),("relic1","First relic","Find a relic on a hunt",15,4022,0,"relics",1),("relics","Curator","Find all %d relics"%len(aX),100,2485,1177,"relics",len(aX)),("places","Seasoned traveller","Hunt at all %d places"%len(ao),40,5355,0,"places",len(ao)),("shrines","Pilgrimage","Meditate at all %d shrines"%len(al),40,2600,0,"shrines",len(al)),("avatar","Avatar","Every virtue at level 5",100,11119,1177,"virtue5",len(al)),("friend","Playdate","A friend's mongotchi visits",10,3613,0,"guests",1),("charm","Best friends","Buy the Companion Charm",50,3676,1161,"charm",1),("festive","Festive","Give a treat in its season",20,3178,0,None,1),];ft=dict((h7[0],h7)for h7 in aM);bC=8;fu=200;E={"name":"Flapjack","pace":100,"grem_min":20,"share_min":10,"gremlins":True,"sounds":True,"remind":True,"offline":False,"listen":True,"share_ch":0,"comp":False,"comp_talk":True,"comp_help":True,"share_open":True};dn=dict(E);aN={"pace":(25,400),"grem_min":(5,240),"share_min":(0,60),"share_ch":(0,len(bu)-1)};aY={"food":80.,"joy":80.,"energy":90.,"clean":100.,"sick":False,"sick_t":0.,"asleep":False,"age":0.,"care_sum":0.,"care_t":0.,"stage":0,"pantry":e3,"messes":0,"neglect":0.,"warned":False,"feral":False,"mess_in":40*60.,"supply_in":cL*60.,"away":False,"away_left":0.,"fed":0,"swats":0,"stolen":0,"uid":0,"guard":False,"last":0.,"away_kind":0,"away_loc":0,"away_virt":0,"away_total":0.};j=dict(aY);fv=["hat","neck","dye","aura","toy","pers","decor","hang","title","voice","ncol"];m={"sq":0.,"own":set(),"cnt":{},"eq":{},"last":0.};u={"xp":dict((h8,0.)for h8 in aL),"relics":{},"visits":{},"hunts":0,"med":0,"tab":0};U={"got":set(),"earned":0.,"swats":0,"new":False};i={"minimized":False,"shutting":False,"docked":False,"queue":[],"last_t":0.,"sim_acc":0.,"saved_at":0.,"say":"","say_until":0.,"pet_cd":0.,"brush_cd":0.,"remind":{},"confirm":0.,"px":float(r+C//2-J//2),"py":float(am+10),"tx":0.,"ty":0.,"hover_until":0.,"eat_food":None,"eat_x":0,"play_toy":None,"toy":[0.,0.,0.,0.],"music_at":0.,"away_until":0.,"dizzy_until":0.,"shop_min":Kit.load_min(aA["shop"]),"shop_cat":0,"shop_page":0,"pen_open":False,"pen_min":Kit.load_min(aA["pen"]),"guests":[],"pals":{},"quest_min":Kit.load_min(aA["quest"]),"ach_min":Kit.load_min(aA["ach"]),"ach_saved":None,"hallow_night":False,"season_saved":None,"season_told":set(),"hallow_told":None,"snow":[],"shared_at":0.,"social_at":0.,"anims":{},"snd_later":[],"parts":{"main":[],"pen":[]},"sprites":{"main":[],"pen":[]},"bar_w":{},"carry":None,"shop_dirty":False,"quest_dirty":False};cd={"g":None,"c":{},"store":({},{}),"v":None};hJ,V,q=Kit.basics(i,Y)
	class View(object):
		__slots__=("cache","pen","xf","made")
		def __init__(self):self.cache={};self.pen=set();self.xf=None;self.made=None
		def reg(self,ctrl,**a):
			self.cache[id(ctrl)]=a
			if self.made is not None:self.made.append(ctrl)
		def tr(self,x,y):a=self.xf;return a[2]+(x-a[0])*a[4],a[3]+(y-a[1])*a[4]
		def _e(self,ctrl):
			k=id(ctrl);e=self.cache.get(k)
			if e is None:e=self.cache[k]={}
			return e
		def _chg(self,ctrl,key,v):
			if ctrl is None:return False
			e=self._e(ctrl)
			if e.get(key)==v:return False
			e[key]=v;return True
		def show(self,ctrl,on):
			if self._chg(ctrl,"vis",on):Kit.set(ctrl,"IsVisible",on)
		def look(self,ctrl,gfx,hue):
			if self._chg(ctrl,"gfx",gfx):Kit.set(ctrl,"Graphic",gfx)
			if self._chg(ctrl,"hue",hue):Kit.set(ctrl,"Hue",hue)
		def move(self,ctrl,x,y):
			if ctrl is None:return
			b,c=int(x),int(y)
			if not self._chg(ctrl,"pos",(b,c)):return
			try:
				a=self.xf
				if a is not None and id(ctrl)in self.pen:ctrl.SetPos(int(round(a[2]+(b-a[0])*a[4])),int(round(a[3]+(c-a[1])*a[4])))
				else:Kit.ui_pos(ctrl,b,c)
			except Exception:pass
		def size(self,ctrl,w,h):
			if ctrl is None:return
			a,b=int(w),int(h)
			if not self._chg(ctrl,"size",(a,b)):return
			try:
				if self.xf is not None and id(ctrl)in self.pen:c=self.xf[4];ctrl.SetWidth(max(1,int(round(a*c))));ctrl.SetHeight(max(1,int(round(b*c))))
				else:Kit.ui_size(ctrl,a,b)
			except Exception:pass
		def alpha(self,ctrl,a):
			if ctrl is None:return
			a=round(a,2)
			if self._chg(ctrl,"alpha",a):
				try:ctrl.SetAlpha(a)
				except Exception:pass
		def width(self,ctrl,w):
			if self._chg(ctrl,"w",w):
				try:Kit.ui_w(ctrl,max(0,w))
				except Exception:pass
		def text(self,lbl,text,hue=None):
			if lbl is None:return
			e=self._e(lbl)
			if e.get("text")!=text or(hue is not None and e.get("thue")!=hue):
				e["text"]=text
				if hue is not None:e["thue"]=hue
				Kit.set_text(lbl,text,hue)
	def ce(s,a=cR):s="".join(b for b in str(s or "")if 32<=ord(b)<127 and b not in ";=|,").strip();return s[:a]or dn["name"]
	def be(v):return[a.split(":",1)for a in v.split(",")if ":"in a]
	def do():Kit.kv_load(cC,";",E,aN,("name",));E["name"]=ce(E["name"])
	def bD():Kit.kv_save(cC,";",E,dn,aN,("name",))
	def bE(on):E["comp"]=bool(on);bD();bt(ag)
	def fw():
		a=Kit.get_var(cT)
		if "="not in a:return False
		j.update(aY)
		for k,v in Kit.codec_load(a).items():
			if k not in aY:continue
			d=aY[k]
			try:
				if isinstance(d,bool):j[k]=v=="1"
				elif isinstance(d,int):j[k]=int(float(v))
				else:j[k]=float(v)
			except ValueError:pass
		if not j["uid"]:j["uid"]=l.randint(1,65535)
		return True
	def aO(final=False):
		a=time.time();j["last"]=a
		if j["away"]:
			b=max(0.,i["away_until"]-a)
			if j["away_total"]>0 and b>j["away_total"]:b=j["away_total"];i["away_until"]=a+b
			j["away_left"]=b
		Kit.put_var(cT,";".join("%s=%s"%(c,("1"if j[c]else "0")if isinstance(e,bool)else "%d"%int(j[c])if isinstance(e,int)else "%.2f"%float(j[c]))for c,e in aY.items()))
		if final or i["shop_dirty"]or a-m["last"]>=fc:bF()
		if final or i["quest_dirty"]:fD()
		i["saved_at"]=a
	def fx():
		m.update({"sq":0.,"own":set(),"cnt":{},"eq":{},"last":0.})
		for k,v in Kit.codec_load(Kit.get_var(cU)).items():
			try:
				if k=="sq":m["sq"]=max(0.,float(v))
				elif k=="last":m["last"]=float(v)
				elif k=="own":m["own"]=set(a for a in v.split(",")if a in W)
				elif k=="cnt":
					for i,n in be(v):
						if i in W and int(n)>0:m["cnt"][i]=int(n)
				elif k=="eq":
					for s,i in be(v):
						if s in fv and(i in W or i==""):m["eq"][s]=i
			except ValueError:pass
		m["own"]|=dg
		for s in cc:
			if not m["eq"].get(s):m["eq"][s]=bf(s)
		fy()
	def fy():
		c=Kit.get_var(cX);i["season_saved"]=c
		for k,v in Kit.codec_load(c).items():
			if k=="own":m["own"]|=set(d for d in v.split(",")if d in bA and not aw(W[d]))
			for a,b in be(v):
				if k=="cnt"and a in bA and aw(W[a]):
					if safe(lambda:int(b),0)>0:m["cnt"][a]=int(b)
				elif k=="eq"and b in bA and aS.get(W[b]["cat"])==a and(m["eq"].get(a)or "")==bf(a):m["eq"][a]=b
	def bF():
		m["last"]=time.time();i["shop_dirty"]=False;S=bA;f=["%s:%s"%(g,bf(g)if h in S else h)for g,h in sorted(m["eq"].items())];b=["%s:%s"%(p,k)for p,k in sorted(m["eq"].items())if k in S];c=sorted((t,s)for t,s in m["cnt"].items()if s>0);Kit.put_var(cU,";".join(["sq=%.2f"%m["sq"],"last=%.0f"%m["last"],"own="+",".join(sorted(v for v in m["own"]-dg if v not in S)),"cnt="+",".join("%s:%d"%(w,x)for w,x in c if w not in S),"eq="+",".join(f)]));d=sorted(y for y in m["own"]if y in S);e=["%s:%d"%(z,G)for z,G in c if z in S];a=";".join(["own="+",".join(d),"cnt="+",".join(e),"eq="+",".join(b)])if d or e or b else ""
		if a!=i["season_saved"]:i["season_saved"]=a;Kit.put_var(cX,a)
		fA()
	def fz():
		a=Kit.get_var(cY);i["ach_saved"]=a;U.update({"got":set(),"earned":0.,"swats":0,"new":"="not in a})
		for k,v in Kit.codec_load(a).items():
			try:
				if k=="got":U["got"]=set(sorted(d for d in v.split(",")if d)[:fu])
				elif k=="earned":U["earned"]=max(0.,float(v))
				elif k=="swats":U["swats"]=max(0,int(float(v)))
			except ValueError:pass
		b=1.-Q["hon_price"]*D("hon");c=m["sq"]+sum(int(round(e["price"]*b))for e in av if e["price"]and not aw(e)and e["id"]in m["own"]);U["earned"]=max(U["earned"],c)
	def fA():
		a="got=%s;earned=%.2f;swats=%d"%(",".join(sorted(U["got"])),U["earned"],U["swats"])
		if a!=i["ach_saved"]:i["ach_saved"]=a;Kit.put_var(cY,a)
	def fB():
		i["guests"]=[]
		for a in Kit.get_var(cV).split(","):
			g=cm(a.strip())
			if g is not None and len(i["guests"])<az-1:i["guests"].append(g)
	def cf():Kit.put_var(cV,",".join(a["code"]for a in i["guests"]))
	def fC():
		u.update({"xp":dict((c,0.)for c in aL),"relics":{},"visits":{},"hunts":0,"med":0,"tab":0})
		for k,v in Kit.codec_load(Kit.get_var(cW)).items():
			try:
				if k=="xp":
					for a,n in be(v):
						if a in u["xp"]:u["xp"][a]=max(0.,min(float(n),bg(ai)))
				elif k in("relics","visits"):
					b=bB if k=="relics"else fr
					for i,n in be(v):
						if i in b and int(n)>0:u[k][i]=int(n)
				elif k in("hunts","med"):u[k]=max(0,int(float(v)))
				elif k=="tab":u["tab"]=max(0,min(len(dm)-1,int(v)))
			except ValueError:pass
	def fD():i["quest_dirty"]=False;Kit.put_var(cW,";".join(["xp="+",".join("%s:%.1f"%(a,u["xp"][a])for a in aL),"relics="+",".join("%s:%d"%b for b in sorted(u["relics"].items())),"visits="+",".join("%s:%d"%c for c in sorted(u["visits"].items())),"hunts=%d"%u["hunts"],"med=%d"%u["med"],"tab=%d"%u["tab"]]))
	def cg(a):Kit.save_pos(cZ[a],X[a]["g"])
	def ch():return HOST.me()
	def dp(ser):return HOST.mobile(ser)
	def o():return E["name"]
	def O(idx):
		if E["sounds"]and idx:API.PlaySound(idx)
	def fE(t):
		q=i["snd_later"]
		if q:
			for e in q:
				if e[0]<=t:break
			else:return
			i["snd_later"]=[c for c in q if c[0]>t]
			for a,b in q:
				if a<=t:O(b)
	def aP():O(W[m["eq"]["voice"]].get("snd",422))
	def A(text,secs=3.):i["say"],i["say_until"]=text,time.time()+secs
	def R(v,lo=0.,hi=100.):return max(lo,min(hi,v))
	def dq(x,y,tx,ty,step):
		b,c=tx-x,ty-y;a=math.hypot(b,c)
		if a<=step or a<.01:return tx,ty
		return x+b/a*step,y+c/a*step
	def F(k,n):j[k]=R(j[k]+n)
	def eq(slot):return W.get(m["eq"].get(slot)or "")
	def bf(slot):return bc[slot][0]["id"]if slot in cc else ""
	def aw(it):return it["cat"]=="treat"or it.get("uses")
	def aa(a):return a in m["own"]
	def af(k,default):return eq("pers").get(k,default)
	def aZ():return cK if aa("u_pantry")else e4
	def bg(level):return 50.*level*(level+1)
	dr={}
	def D(key):
		b=u["xp"].get(key,0.);c=dr.get(key)
		if c is not None and c[0]==b:return c[1]
		a=0
		while a<ai and b>=bg(a+1):a+=1
		dr[key]=(b,a);return a
	def ci(key):
		a=D(key)
		if a>=ai:return 0.,0.
		b=bg(a);return u["xp"].get(key,0.)-b,bg(a+1)-b
	def cj(key,a):v=dk[key];n=a//-v[4]if v[4]<0 else a*v[4];return v[3]%n if "%d"in v[3]else v[3]
	def bG(level):return all(D(a)>=level for a in aL)
	def ck():return e8*len(u["relics"])
	def ds(req):
		if req is None:return
		if req[0]=="stage":
			if j["stage"]<req[1]:return "needs a grown mongotchi"if req[1]==1 else "needs a Greater Mongotchi"
		elif req[0]=="virtue":
			if D(req[1])<req[2]:return "needs %s at level %d"%(dk[req[1]][1],req[2])
		return
	def bh(it):return int(round(it["price"]*(1.-Q["hon_price"]*D("hon"))))
	def dt():
		k=j["away_kind"]
		if k==1:return "treasure hunting at %s"%ao[min(j["away_loc"],len(ao)-1)]["name"]
		if k==2:return "meditating at the Shrine of %s"%al[min(j["away_virt"],len(al)-1)][1]
		return "foraging"
	def du():return{1:"out hunting",2:"meditating"}.get(j["away_kind"],"out foraging")
	def P(kind,n=None):
		n=a9.get(kind,0)if n is None else n
		if n<=0:return 0
		a=af("squeak",1.)*(fi if aa("u_luck")else 1.);a*=1.+Q["hnr_squeaks"]*D("hnr")+ck();m["sq"]+=n*a;U["earned"]+=n*a
		if kind!="passive":
			i["shop_dirty"]=True
			if kind!="social"and n*a>=1:a6("+%d"%int(round(n*a)),Kit.HUE_TITLE,12,-26.,1.4)
		return n*a
	def a_():return R(.45*j["joy"]+.3*j["food"]+.15*j["clean"]+.1*j["energy"]-(15 if j["sick"]else 0))
	def dv():
		m=a_()
		for a,b in fo:
			if m>=a:return b,(Kit.HUE_GOOD if m>=55 else Kit.HUE_BAD if m<35 else Kit.HUE_TEXT)
	def hm(secs):secs=max(0,int(secs));return "%dh %02dm"%(secs//3600,(secs%3600)//60)if secs>=3600 else "%dm"%(secs//60)
	N=Kit.fit
	def dw(nm,a):t=W.get(a or "");return nm+(" "+t["name"]if t else "")
	def cl():j.update(aY);j["uid"]=l.randint(1,65535);j["last"]=time.time();i.update({"grem":None,"eat_until":0.,"play_until":0.,"cure_until":0.,"brush_until":0.,"leave_until":0.,"away_until":0.,"say":"","remind":{},"px":float(r+C//2-J//2),"py":float(am+10),"hover_until":0.,"dizzy_until":0.});aO();K("arrive",1.2);aE(bm,r+C/2.,am+30,1.2,0,64);q("a pup has adopted you: meet %s (rename it on the settings page)."%o(),Kit.HUE_GOOD)
	dz=re.compile(r"(?<![A-Za-z0-9_\-])([A-Za-z0-9_\-]{64})(?![A-Za-z0-9_\-])")
	def fF(slot,a):b=[c["id"]for c in bc.get(slot,[])];return b.index(a)+1 if a in b else 0
	def fG(slot,n):a=bc.get(slot,[]);return a[n-1]["id"]if 1<=n<=len(a)else bf(slot)
	def dA(s,n):b=[ord(a)if 32<=ord(a)<127 else 63 for a in s[:n]];return b+[0]*(n-len(b))
	def dB(b):return "".join(chr(a)for a in b if 32<=a<127).strip()
	a0={"at":-99.,"name":"Someone","raw":None}
	def bH():
		t=time.time()
		if t-a0["at"]>=2.:
			a0["at"]=t;a=safe(lambda:ch().Name,"")or "Someone"
			if a!=a0["raw"]:a0["raw"]=a;a0["name"]=ce(a,16)
		return a0["name"]
	def fH():a=[1,j["stage"]]+[fF(b,m["eq"].get(b,""))for b in dj];a+=[int(a_()),min(255,int(j["age"]//3600)),min(255,j["swats"]),(j["uid"]>>8)&255,j["uid"]&255]+dA(o(),12)+dA(bH(),16);c=Kit.checksum(a);return Kit.b64(a+[(c>>8)&255,c&255])
	def cm(code):
		if not code or len(code)!=64 or any(a not in Kit.B64_REV for a in code):return
		d=Kit.unb64(code)
		if len(d)!=48 or d[0]!=1 or Kit.checksum(d[:46])!=(d[46]<<8|d[47]):return
		g={"code":code,"stage":min(2,d[1]),"mood":d[13],"age":d[14],"swats":d[15],"uid":d[16]<<8|d[17],"name":dB(d[18:30])or "Mongotchi","owner":dB(d[30:46])or "Someone"}
		for n,k in enumerate(dj):g[k]=fG(k,d[2+n])
		return g
	def dC(a,events):
		if j["feral"]:return
		p=E["pace"]/100.;h=a/3600.*p;e,b=j["asleep"],j["sick"];c=eq("pers");g=.5 if(j["away"]and j["away_kind"]==2)else 1.;d=Q;j["food"]-=eN*h*(.5 if e else 1.)*(1.25 if b else 1.)*c.get("food_rate",1.)*(1.-d["hum_hunger"]*D("hum"))*g;i=0. if e else eO*c.get("joy_rate",1.)*(1.-d["com_joy_loss"]*D("com"));i+=eP*((j["food"]<25)+(j["clean"]<30)+bool(b))*(1.-d["hum_need"]*D("hum"));j["joy"]-=i*h*g
		if e:k=eq("decor");j["energy"]+=(eR*h*c.get("sleep",1.)*(k.get("sleep",1.)if k else 1.))
		else:j["energy"]-=eQ*h*(1.5 if b else 1.)*c.get("energy_rate",1.)
		j["clean"]-=(eS+eT*j["messes"])*h
		for m in("food","joy","energy","clean"):j[m]=R(j[m])
		j["age"]+=a*p;j["care_sum"]+=a_()*a*p;j["care_t"]+=a*p;j["mess_in"]-=a*p
		if j["mess_in"]<=0:
			j["mess_in"]=l.uniform(eU,eV)*60.
			if j["messes"]<b_ and not j["away"]:j["messes"]+=1;events.append(("mess","%s left a little heap in the pen."%o()))
		j["supply_in"]-=a*p
		if j["supply_in"]<=0:
			j["supply_in"]=cL*60.
			if j["pantry"]<aZ():j["pantry"]+=1;events.append(("supply","A farmer left some food at the pen (+1)."))
		if aa("u_feeder")and j["food"]<20 and j["pantry"]>0 and not j["asleep"]and not j["away"]:n=l.choice(ap);j["pantry"]-=1;F("food",n[2]);events.append(("feeder","the Auto-Feeder gave %s %s."%(o(),n[1])))
		if not b:
			f=((eW if j["clean"]<30 else 0.)+(eX if j["food"]<10 else 0.));f*=1.-d["spi_sick"]*D("spi")
			if f and l.random()<f*h:j["sick"],j["sick_t"]=True,0.;events.append(("sick","%s is sick: give it a Cure potion."%o()))
		else:j["sick_t"]+=a*p
		if not j["asleep"]and j["energy"]<=3 and not j["away"]:j["asleep"]=True;events.append(("sleep","%s fell asleep."%o()))
		elif j["asleep"]and j["energy"]>=100:j["asleep"]=False;events.append(("wake","%s woke up rested."%o()))
		q=(j["food"]<=0 or j["joy"]<=0 or(j["sick"]and j["sick_t"]>eY*3600))
		if q:j["neglect"]+=a*p
		else:
			j["neglect"]=max(0.,j["neglect"]-a*p*.5)
			if j["neglect"]==0:j["warned"]=False
		if j["neglect"]>=eZ*3600:j["feral"],j["away"],j["asleep"]=True,False,False;events.append(("feral","%s decided it is better off without a master and flew away."%o()));return
		if j["neglect"]>=e_*3600 and not j["warned"]:j["warned"]=True;events.append(("warn","%s looks around for someone else to care for it."%o()))
		if j["stage"]==0 and j["age"]>=e0*3600:j["stage"]=1;events.append(("grow","%s has grown into a mongotchi."%o()))
		elif j["stage"]==1 and j["age"]>=e1*3600 and j["care_t"]>0 and j["care_sum"]/j["care_t"]>=e2:j["stage"]=2;events.append(("grow","%s is now a Greater Mongotchi."%o()))
	dD={"sick":Kit.HUE_BAD,"feral":Kit.HUE_BAD,"warn":Kit.HUE_BAD,"grow":Kit.HUE_GOOD,"feeder":Kit.HUE_INFO,"sleep":Kit.HUE_INFO,"wake":Kit.HUE_INFO}
	def dE(events,live=True):
		for a,b in events:
			if a in dD and(live or a not in("sleep","wake")):q(b,dD[a])
			if a=="grow":P("grow")
			if not live:continue
			if a=="grow":O(eH);A("*grows!*",4);K("grow",2.5);aR(a5,2.,72)
			elif a=="sick":O(bZ);A("*cough cough*");K("cough",.4)
			elif a=="feral":aP();K("farewell",2.5);i["redraw_at"]=time.time()+2.6
			elif a in("supply","feeder"):O(aU);i["carry"]={"who":"drop","gfx":l.choice(ap)[0],"t0":time.time(),"x":float(r+40+l.randint(0,60)),"y":float(B+20)}
			elif a=="mess":K("mess%d"%max(0,j["messes"]-1),.5)
			elif a=="sleep":K("yawn",1.4)
			elif a=="wake":K("stretch",.5)
	def fI():
		c=time.time()
		if m["last"]:
			a=min(max(0.,c-m["last"]),b2*3600);d=P("passive",b3*a/3600.)
			if d>=1:q("%d squeaks earned while you were away."%int(d),Kit.HUE_GOOD)
		m["last"]=c;a=max(0.,c-j["last"])if j["last"]else 0.
		if j["away"]:
			b=j["away_left"]
			if j["away_total"]>0:b=min(b,j["away_total"])
			j["away_left"]=max(0.,b-a);i["away_until"]=c+j["away_left"]
			if j["away_left"]<=0:i["away_until"]=c;co(quiet=True)
		if not E["offline"]or a<60 or j["feral"]:return
		a=min(a,b2*3600);e=[];b=a
		while b>0 and not j["feral"]:f=min(60.,b);dC(f,e);b-=f
		q("while away (%s): fullness %d, happiness %d, %s, pantry %d."%(hm(a),j["food"],j["joy"],Kit.count(j["messes"],"heap"),j["pantry"]),Kit.HUE_INFO);dE([g for g in e if g[0]in("sick","grow","warn","feral")],live=False)
	def ar(what):
		if j["feral"]:q("%s has gone wild: adopt a new pup in the pen."%o(),Kit.HUE_INFO);return False
		if j["away"]:q("%s is out %s."%(o(),dt()),Kit.HUE_INFO);return False
		if j["asleep"]and what not in("lights","clean"):A("z Z z");q("%s is asleep (Lights wakes it)."%o(),Kit.HUE_INFO);return False
		return True
	def aQ():return not j["asleep"]and not j["away"]
	def ax():t=time.time();return t<i["eat_until"]or t<i["play_until"]or t<i["leave_until"]
	def fJ(action,t):
		if not ar("feed")or ax():return
		if j["pantry"]<=0:A("*eyes the empty pantry*");q("the pantry is empty: Forage, or wait for the farmer.",Kit.HUE_BAD);return
		if j["food"]>=95:A("*turns its nose up*");return
		j["pantry"]-=1;dF(l.choice(ap),t)
	def dF(food,t):i.pop("eat_t0",None);i["eat_bites"]=1.;i["eat_food"]=food;i["eat_x"]=l.randint(r+70,r+C-60);i["eat_until"]=t+cO
	def fK():c,a,b=i["eat_food"];i["eat_food"]=None;F("food",b);F("joy",af("feed_joy",5));j["fed"]+=1;P("feed");O(cH);A("*munches %s*"%a.split(" ",1)[1]if " "in a else "*munch*")
	def fL(it,t):
		if not ar("treat")or ax()or m["cnt"].get(it["id"],0)<=0:return False
		m["cnt"][it["id"]]-=1;i["shop_dirty"]=True
		for k in("food","joy","energy","clean"):
			if it.get(k):F(k,it[k])
		if it.get("cure")and j["sick"]:j["sick"],j["sick_t"]=False,0.
		if it.get("guard"):j["guard"]=True
		if it.get("dizzy"):i["dizzy_until"]=t+30.
		P("treat");O(cH)
		if it.get("spooky"):K("spooky",1.6)
		if it.get("energy",0)>=20:K("zoom",4.)
		if it.get("guard"):a6("!",Kit.HUE_BAD,0,-30.)
		if it.get("cure"):aR(d4,1.2)
		if it.get("sleep"):K("yawn",1.4)
		dF((it["gfx"],it["name"],0),t);A("*spooky squeak!* BOO!"if it.get("spooky")else "*gobbles the %s*"%it["name"].lower(),3.5)
		if it.get("sleep"):i["sleep_after"]=t+cO+.5
		q("you give %s a %s."%(o(),it["name"].lower()),Kit.HUE_GOOD)
		if it.get("season")and bi(it):dN("festive")
		return True
	def fM(action,t):
		if not ar("play")or ax():return
		if j["sick"]:A("*cough*");q("%s is too sick to play."%o(),Kit.HUE_INFO);return
		if j["energy"]<15:A("*yawns*");q("%s is too tired to play."%o(),Kit.HUE_INFO);return
		a=eq("toy");i["play_toy"]=a;i["play_until"]=t+fd;i["toy"]=[float(r+20),float(aq-40),l.uniform(70,110),-60.];i["music_at"]=0.
		if a.get("motion")=="music":i["toy"]=[float(r+C//2-22),float(aq),0.,0.];A("*dances*")
		else:A("*pounces!*")
	def fN():
		a=i["play_toy"]or eq("toy");b=l.randint(10,45)if a.get("motion")=="dice"else 25+a.get("joy",0);F("joy",b*af("play",1.));j["energy"]=R(j["energy"]-10+a.get("energy",0));F("food",-5);P("play")
		if a.get("squeaks"):P("toy",a["squeaks"])
		aP();A(l.choice(an["happy"]))
	def fO(action,t):
		if not ar("brush")or ax():return
		if t<i["brush_cd"]:A("*already shiny*");return
		k=2 if aa("u_groom")else 1;i["brush_cd"]=t+ff/k;F("joy",10*k);F("clean",10*k);i["brush_until"]=t+1.8;P("brush",a9["brush"]*k);O(cI);A("*purrs... er, squeaks*")
	def fP(action,t):
		if not ar("clean"):return
		if j["messes"]==0 and j["clean"]>=95:A("*already spotless*");return
		if j["messes"]or j["clean"]<80:P("clean")
		i["mess_was"]=j["messes"];K("clean",.7)
		for a in range(j["messes"]):aE(bm,r+84+a*44+22,B+L-20,.9,0,48)
		if not j["asleep"]:K("shake",.6);A("*shakes its wings*")
		j["messes"],j["clean"]=0,100.;O(cI)
	def fQ(action,t):
		if not ar("lights"):return
		if j["asleep"]:
			j["asleep"]=False;K("stretch",.5)
			if j["energy"]<50:F("joy",-5);A("*grumpy squeak*")
			else:A("*stretches*")
		elif ax():return
		elif j["energy"]>=90:A("*isn't sleepy*")
		else:j["asleep"]=True;K("yawn",1.4);i["say"]=""
	def fR(action,t):
		if not ar("cure"):return
		if not j["sick"]:A("*isn't sick*");return
		j["sick"],j["sick_t"]=False,0.;F("joy",-5);i["cure_until"]=t+1.5;K("flash",1.);K("shake",.8);aR(d4,1.4);P("cure");O(eG);A("*bleh!* ...*feels better*")
	def fS(action,t):
		if not ar("forage")or ax():return
		if j["sick"]or j["energy"]<20:A("*too weak*"if j["sick"]else "*too tired*");q("%s is too %s to forage."%(o(),"sick"if j["sick"]else "tired"),Kit.HUE_INFO);return
		if j["pantry"]>=aZ():q("the pantry is full.",Kit.HUE_INFO);return
		F("energy",-max(Q["sac_forage_min"],e7-Q["sac_energy"]*D("sac")));F("food",-5);cn(t,0,l.uniform(cM[0],cM[1]),"*flaps off*")
	def cn(t,kind,secs,line):j["away"],j["away_kind"],j["away_total"]=True,kind,secs;i["away_until"],i["leave_until"]=t+secs,t+1.5;A(line,1.5)
	def fT(quiet=False,b=1.):
		a=(1+l.randint(0,1)+(1 if j["energy"]>50 and l.random()<.5 else 0));a+=af("forage",0)+D("sac")//Q["sac_per"];a=max(0,min(a,aZ()-j["pantry"]));j["pantry"]+=a
		if a and not quiet:i["carry"]={"who":"pet","gfx":l.choice(ap)[0],"t0":time.time()}
		P("forage",a9["forage"]*a);q("%s foraged %d food."%(o(),a),Kit.HUE_GOOD if a else Kit.HUE_INFO)
		if quiet:return
		O(aU);A("*brings back %d food!*"%a if a else "*found nothing*")
	def co(quiet=False,a=1.):k=j["away_kind"];i["ach_due"]=True;j["away"],j["away_kind"]=False,0;i["px"],i["py"]=float(aV),float(am+10);i["tx"],i["ty"]=float(r+C//2),float(am+20);{1:fW,2:fY}.get(k,fT)(quiet,a)
	def dG(t):return max(0.,i["away_until"]-t)
	def dH(t):a=j["away_total"]or 1.;return R(1.-dG(t)/a,0.,1.)
	def fU(n,t):
		if n<0 or n>=len(ao):return
		a=ao[n]
		if not ar("hunt")or ax():return
		b=ds(a["req"])
		if b:q("%s can't go to %s yet: %s."%(o(),a["name"],b),Kit.HUE_BAD);return
		if j["sick"]or j["energy"]<25:A("*too weak*"if j["sick"]else "*too tired*");q("%s is too %s for a treasure hunt."%(o(),"sick"if j["sick"]else "tired"),Kit.HUE_INFO);return
		j["away_loc"]=n;F("energy",-max(Q["sac_hunt_min"],e6-Q["sac_energy"]*D("sac")));F("food",-10);cn(t,1,a["mins"]*60.,"*flaps off on an adventure!*");O(aU);q("%s flies to %s (about %d min)."%(o(),a["name"],a["mins"]),Kit.HUE_GOOD);aO();i["quest_redraw"]=True
	def fV(e,f):
		a={"sq":0,"food":0,"trap":0,"treat":[],"relic":[]};g=1.+Q["spi_relic"]*D("spi");c=[(n*(g if k=="relic"else 1.),k,p,s)for n,k,p,s in e["loot"]];h=sum(t[0]for t in c)
		for j in range(f):
			r=l.uniform(0,h)
			for w,b,d,i in c:
				r-=w
				if r<=0:break
			if b in("sq","food"):a[b]+=l.randint(d,i)
			elif b=="trap":a["trap"]+=1
			else:a[b].append(d)
		return a
	def fW(quiet=False,h=1.):
		c=ao[min(j["away_loc"],len(ao)-1)];r=c["danger"]*(1.-Q["val_danger"]*D("val"));d=l.random()<r*h;e=l.randint(cN[0],cN[1])+D("sac")//Q["sac_per"];e=int(e*h+(l.random()<(e*h)%1.))
		if d:
			e=e//2;F("energy",-25);F("joy",-10)
			if not j["sick"]and l.random()<.35:j["sick"],j["sick_t"]=True,0.
		a=fV(c,e);b=[]
		if a["sq"]:n=P("hunt",a["sq"]);b.append("%d squeaks"%int(round(n)))
		if a["food"]:s=max(0,aZ()-j["pantry"]);n=min(a["food"],s);j["pantry"]+=n;b.append("%d food"%n if n else "food the full pantry couldn't hold")
		for f in a["treat"]:m["cnt"][f]=m["cnt"].get(f,0)+1;b.append(W[f]["name"].lower()if f in W else f)
		if a["trap"]:m["cnt"]["u_trap"]=m["cnt"].get("u_trap",0)+a["trap"];b.append(Kit.count(a["trap"],"Gremlin Trap"))
		i["shop_dirty"]=i["quest_dirty"]=True;k=False
		for g in a["relic"]:
			if g not in u["relics"]:k=True
			u["relics"][g]=u["relics"].get(g,0)+1;b.append(bB[g][1])
		u["hunts"]+=1;u["visits"][c["id"]]=u["visits"].get(c["id"],0)+1;P("forage",2)
		if b:t=", ".join(b[:-1])+(" and "if len(b)>1 else "")+b[-1];v=", but %s."%c["bad"]if d else ".";q("%s is back from %s with %s%s"%(o(),c["name"],t,v),Kit.HUE_BAD if d else Kit.HUE_GOOD)
		else:q("%s is back from %s empty-handed%s"%(o(),c["name"],": %s."%c["bad"]if d else "."),Kit.HUE_BAD if d else Kit.HUE_INFO)
		if k:
			q("new relic (Journeys > Relics): relic bonus now +%d%% squeaks."%int(round(ck()*100)),Kit.HUE_GOOD)
			if len(u["relics"])==len(aX):q("%s has found every relic in Sosaria."%o(),Kit.HUE_GOOD)
		aO();i["quest_redraw"]=True
		if quiet:return
		p=bB[a["relic"][0]][2]if a["relic"]else l.choice(ap)[0]if b else None
		if p is not None:i["carry"]={"who":"pet","gfx":p,"t0":time.time()}
		if d:O(bZ);A("*ouch...*",3.);K("cough",.4)
		else:
			O(aU);A("*brings back treasure!*"if b else "*found nothing*",3.)
			if k:aR(a5,2.,72)
	def fX(n,t):
		if n<0 or n>=len(al):return
		v=al[n]
		if not ar("meditate")or ax():return
		if j["sick"]:A("*cough*");q("%s is too sick to meditate."%o(),Kit.HUE_INFO);return
		if D(v[0])>=ai:q("%s has mastered %s already."%(o(),v[1]),Kit.HUE_INFO);return
		j["away_virt"]=n;F("food",-5);cn(t,2,b1*60.,"*flaps off serenely*");q("%s flies to meditate at the Shrine of %s (%s, about %d min)."%(o(),v[1],v[2],int(b1)),Kit.HUE_GOOD);aO();i["quest_redraw"]=True
	def fY(quiet=False,c=1.):
		v=al[min(j["away_virt"],len(al)-1)];k=v[0];d=D(k);b=e5*(1.+Q["spi_meditate"]*D("spi"))*(.7+.6*a_()/100.)*(.8,1.,1.25)[j["stage"]]*c;b=max(0.,b);u["xp"][k]=min(bg(ai),u["xp"].get(k,0.)+b);u["med"]+=1;i["quest_dirty"]=True;F("joy",10*c);F("energy",10*c);P("meditate",3);a=D(k);f,g=ci(k);h="level %d, %d/%d"%(a,int(f),int(g))if a<ai else "level %d, mastered"%a;q("%s meditated on %s: +%d experience (%s)."%(o(),v[1],int(round(b)),h),Kit.HUE_GOOD)
		if a>d:
			e=cj(k,a);q("%s's %s has risen to level %d: %s."%(o(),v[1],a,e[:1].lower()+e[1:]),Kit.HUE_GOOD)
			if bG(5)and not i.get("vall_told_5"):i["vall_told_5"]=True;q("all eight virtues at level 5: the Avatar title is for sale (Shop > Titles).",Kit.HUE_GOOD)
			if bG(ai):q("%s embodies all eight virtues: an Avatar among mongotchis."%o(),Kit.HUE_GOOD)
		aO();i["quest_redraw"]=True
		if quiet:return
		if a>d:O(fs);K("grow",2.);aR(a5,2.,72)
		else:O(aU);aR(bm,1.4,64)
		A("*feels enlightened*"if a>d else "*feels calm*",3.)
	def fZ(t):
		if not j["away"]:return
		a=dH(t);i["away_until"]=t
		if j["away_kind"]==0:return
		q("%s called home (%d%% of the trip done)."%(o(),int(a*100)),Kit.HUE_INFO);co(False,a)
	def f_(action,t):
		if j["feral"]or j["away"]:return
		if j["asleep"]:A("*snore*");return
		if t<i["pet_cd"]:A(l.choice(an["happy"]));K("hop",.6);return
		i["pet_cd"]=t+fe;K("hop",.6);a6("<3",cG,-10,-22.);a6("<3",eE,8,-18.);F("joy",af("pet",4)+Q["com_pet"]*D("com"));P("pet");aP()
		if eq("pers")["id"]=="p_grumpy"and l.random()<.3:A("*nibbles your finger*")
		elif l.random()<.3 and bI(5)is not None:A(l.choice(dl[bI(5)]))
		else:A(l.choice(an["happy"]))
	def dI():return cP/c2 if i["hallow_night"]else cP
	def f0(t,e,full):
		a=i["grem"]
		if a is None:
			if not(E["gremlins"]and not j["feral"]and j["pantry"]>=2 and t>=i["next_grem_ok"]):return
			f=E["grem_min"]*60.*(2. if aa("u_ward")else 1.)
			if i["hallow_night"]:f/=c2
			if l.random()<e/f:
				if i["hallow_night"]:
					d=time.localtime(t);g=(d[0],d[1],d[2])
					if i["hallow_told"]!=g:i["hallow_told"]=g;q("it's Halloween night: the gremlins are out in force.",Kit.HUE_BAD)
				s=aQ()and not j["sick"]and j["energy"]>20;h=s and(j["guard"]or l.random()<af("guard",fh)+Q["val_guard"]*D("val"))
				if h:j["guard"]=False
				i["grem"]={"phase":"walk","x":float(aC),"t0":t,"walk":fg*(1. if full else 1.5),"guard_at":t+1.5 if h else 0.}
				if aQ():a6("!",Kit.HUE_BAD,0,-30.,1.2)
				if not full:q("a gremlin is sneaking into the pen.",Kit.HUE_BAD)
			return
		if a["phase"]=="walk":
			k=(t-a["t0"])/a["walk"];a["x"]=aC+(fn-aC)*min(1.,k)
			if a["guard_at"]and t>=a["guard_at"]:
				if j["asleep"]or j["away"]or j["feral"]:a["guard_at"]=0.
				elif t>=a["guard_at"]+1.2:a["phase"]="flee";K("gswat",.5);F("joy",5);P("guard",a9["guard"]*(1.+Q["jus_squeaks"]*D("jus")));O(cJ);A("*chases it off!*");q("%s chased the gremlin away."%o(),Kit.HUE_GOOD);return
			if k>=1.:
				a["phase"]="flee"
				if m["cnt"].get("u_trap",0)>0:m["cnt"]["u_trap"]-=1;i["shop_dirty"]=True;a["phase"],a["trap_t"]="trapped",t;K("gtrap",.9);aE(a5,a["x"]+ak/2.,au+30,.9,0,56);ah("SNAP!",Kit.HUE_BAD,a["x"]+ak/2.,au+10,0.,-20.,1.2);u=P("trap");O(eM);q("your Gremlin Trap caught the gremlin (+%d squeaks)."%int(round(u)),Kit.HUE_GOOD);dN("trap");return
				n=j["pantry"];j["pantry"]//=2;b=n-j["pantry"];j["stolen"]+=b;O(eI)
				if aQ():A("*SQUEAK!*")
				q("a gremlin stole %d of %d food."%(b,n),Kit.HUE_BAD)
				if b:i["carry"]={"who":"grem","gfx":l.choice(ap)[0]};ah("-%d"%b,Kit.HUE_BAD,r+30,B+L-40,0.,-18.,1.6)
				if b and aQ()and l.random()<af("stealback",0.):c=(b+1)//2;j["pantry"]=min(aZ(),j["pantry"]+c);A("*steals %d back!*"%c);q("but %s stole %d back."%(o(),c),Kit.HUE_GOOD)
				elif b and aQ()and D("jus"):
					c=int(b*Q["jus_back"]*D("jus")+l.random())
					if c:j["pantry"]=min(aZ(),j["pantry"]+c);A("*demands %d back!*"%c);q("but %s won %d back (Justice)."%(o(),c),Kit.HUE_GOOD)
		elif a["phase"]=="trapped":
			if t-a["trap_t"]>=.9:i["grem"]=None;i["next_grem_ok"]=t+dI()
		else:
			a["x"]+=160.*e
			if a["x"]>=aC+4 or not full:
				i["grem"]=None;i["next_grem_ok"]=t+dI();p=i.get("carry")
				if p is not None and p["who"]=="grem":i["carry"]=None
	def f1(action,t):
		a=i["grem"]
		if a is None or a["phase"]!="walk":return
		a["phase"]="flee";K("gswat",.5);ah("*SWAT*",Kit.HUE_GOOD,a["x"]+ak/2.,au+4,0.,-20.,1.);j["swats"]+=1;U["swats"]+=1;F("joy",5);P("swat",a9["swat"]*(1.+Q["jus_squeaks"]*D("jus")));O(eJ);i["snd_later"].append((time.time()+eK,cJ))
		if aQ():A("*cheers*")
		q("gremlin swatted: the food is safe.",Kit.HUE_GOOD)
	f2={"sick":"%s is sick.","hungry":"%s is hungry.","dirty":"%s's pen needs cleaning.","bored":"%s is unhappy: play with it."};f3={"grem":"a gremlin in the pen","sick":"sick","hungry":"hungry","dirty":"pen needs cleaning","bored":"unhappy"}
	def cp():
		a=[]
		if i["grem"]is not None and i["grem"]["phase"]=="walk":a.append("grem")
		if j["sick"]:a.append("sick")
		if j["food"]<25:a.append("hungry")
		if j["messes"]>=2 or j["clean"]<30:a.append("dirty")
		if j["joy"]<25:a.append("bored")
		return a
	def f4(t):
		if not E["remind"]or j["feral"]:return
		for k in cp():
			if k=="grem":continue
			if t-i["remind"].get(k,-1e9)>=cQ:i["remind"][k]=t;q(f2[k]%o(),Kit.HUE_BAD)
	def bI(d):
		a,b=None,d-1
		for k in aL:
			c=D(k)
			if c>b:a,b=k,c
		return a
	def f5(t):
		if t<i["next_chat"]:return
		i["next_chat"]=t+l.uniform(25,60)/max(.2,af("chat",1.))
		if j["feral"]or j["away"]or j["asleep"]or ax()or t<i["say_until"]:return
		if j["sick"]:a=an["sick"]
		elif j["food"]<30:a=an["hungry"]
		elif j["clean"]<35:a=an["dirty"]
		elif j["joy"]<35:a=an["bored"]
		else:
			a=an["idle"]+af("lines",[])*2;b=bI(5)
			if b is not None:a=a+dl[b]*2
		A(l.choice(a))
		if l.random()<.3:
			if j["sick"]:O(bZ)
			else:aP()
	f6=("January","February","March","April","May","June","July","August","September","October","November","December");f7={"halloween":"costumes and pumpkin treats are","winter":"warm hats, a snowman and gingerbread are","newyear":"a party cap, sparkling cider and fireworks are"}
	def f8(t):
		d=time.localtime(t);a=(d[1],d[2]);e=[]
		for f,g,b,c in b7:
			if(b<=a<=c)if b<=c else(a>=b or a<=c):e.append(f)
		return frozenset(e)
	def dJ(t,force=False):
		if not force and i["season_at"]-c3<=t<i["season_at"]:return
		i["season_at"]=t+c3;b=f8(t);d=time.localtime(t);i["hallow_night"]=(d[1],d[2])==fk
		if b==i["seasons"]:return
		e,i["seasons"]=i["seasons"],b
		for a,f,h,c in b7:
			if a in b and a not in i["season_told"]:i["season_told"].add(a);g=("the end of February"if c==(2,29)else "%s %d"%(f6[c[0]-1],c[1]));q("%s: %s in the Shop (Seasonal tab) until %s."%("it's "+f if a!="winter"else "winter is here",f7.get(a,"its treats and clothes are"),g),Kit.HUE_GOOD)
		if i["shop_cat"]>=len(bJ()):i["shop_cat"],i["shop_page"]=0,0
		if e is not None:i["redraw"]=i["shop_redraw"]=True
	dK={"stage":lambda:j["stage"],"age":lambda:j["age"]/3600.,"swats":lambda:U["swats"],"earned":lambda:U["earned"],"relics":lambda:len(u["relics"]),"places":lambda:len(u["visits"]),"shrines":lambda:sum(1 for a in aL if u["xp"].get(a,0.)>0),"virtue5":lambda:sum(1 for a in aL if D(a)>=5),"guests":lambda:len(i["guests"]),"charm":lambda:1 if aa("u_companion")else 0}
	def dL(t):
		i["ach_at"],i["ach_due"]=t+c6,False
		if j["swats"]>U["swats"]:U["swats"]=j["swats"]
		a=[c for c in aM if c[6]is not None and c[0]not in U["got"]and dK[c[6]]()>=c[7]];b,U["new"]=U["new"],False
		if a:dM(a,b)
	def dM(c,before=False):
		b=0
		for a in c:
			U["got"].add(a[0]);b+=a[3]
			if not before:q("achievement earned: %s (%s), +%d squeaks."%(a[1],a[2][0].lower()+a[2][1:],a[3]),Kit.HUE_GOOD)
		m["sq"]+=b;U["earned"]+=b
		if before:q("%s already earned: %s, +%d squeaks."%(Kit.count(len(c),"achievement"),", ".join(d[1]for d in c),b),Kit.HUE_GOOD)
		else:O(fl);a6("+%d"%b,Kit.HUE_TITLE,12,-26.,1.6);aR(a5,1.6,64)
		i["texts_at"]=0.;bF()
	def dN(a):
		if a not in U["got"]:dM([ft[a]])
	def dO(it):
		r=it.get("req")
		if r=="swats"and j["swats"]<10:return "swat %d more gremlin%s first"%(10-j["swats"],""if j["swats"]==9 else "s")
		if r=="greater"and j["stage"]<2:return "needs a Greater Mongotchi"
		if r=="elder"and j["age"]<24*3600:return "needs an age of 24 hours"
		if r=="charm"and not aa("u_companion"):return "needs the Companion Charm"
		if r=="avatar"and not bG(5):return "needs every virtue at level 5"
		if r=="relics"and len(u["relics"])<8:return "find %d more kind%s of relic"%(8-len(u["relics"]),""if len(u["relics"])==7 else "s")
		if r=="pilgrim"and bI(ai)is None:return "meditate a virtue up to level %d"%ai
		return
	def f9(it):
		if not aw(it)and aa(it["id"]):return
		c=dO(it);d=it["name"]if it["cat"]!="title"else "the title \"%s\""%it["name"]
		if c:q("you can't buy %s yet: %s."%(d,c),Kit.HUE_BAD);return
		a=bh(it)
		if m["sq"]<a:q("not enough squeaks for %s (%d more needed)."%(d,a-int(m["sq"])),Kit.HUE_BAD);return
		m["sq"]-=a;b=aS.get(it["cat"])
		if aw(it):m["cnt"][it["id"]]=m["cnt"].get(it["id"],0)+1
		else:
			m["own"].add(it["id"])
			if it.get("toggle"):bE(True);q("%s can now follow you in the world. Say \"%s stay\", \"%s follow\", \"%s dance\", \"%s fetch\" or \"%s go home\"."%((o(),)*6),Kit.HUE_GOOD)
			if b:m["eq"][b]=it["id"]
		O(eL)
		if b or it.get("toggle"):dQ()
		q("bought %s for %d squeaks."%(it["name"],a),Kit.HUE_GOOD);bF()
	def dP(it,on):
		a=aS.get(it["cat"])
		if not a:return
		m["eq"][a]=it["id"]if on else bf(a)
		if a=="voice"and on:aP()
		dQ();bF()
	def aR(seq,dur,size=56):x,y=bn();aE(seq,x,y+20,dur,0,size)
	def dQ():
		x,y=bn();aE(gN,x,y+20,.8,0,60)
		for a in(-14,0,14):ah("*",a8,x+a,y+16,a*.8,-16.,.8)
	aS=dict((h9,ia)for h9,ib,ia in cb)
	def dR(it):
		b=it["id"];c=bi(it)
		if it["cat"]=="treat":return([("buy","Buy","buy")]if c else[])+([("give","Give","give")]if m["cnt"].get(b,0)>0 else[])
		if it.get("uses")or not aa(b):return[("buy","Buy","buy")]if c else[]
		if it.get("toggle"):return[("dismiss","Dismiss","dismiss")]if E["comp"]else[("summon","Summon","summon")]
		a=aS.get(it["cat"])
		if not a:return[]
		if m["eq"].get(a)==b:
			if a in cc:return[]
			return[("remove","Take off"if a in("hat","neck")else "Remove","remove")]
		return[("wear","Wear"if a in("hat","neck")else "Use","wear")]
	ga={"buy":Kit.ART_OK,"give":Kit.ART_OK,"wear":Kit.ART_PLAY,"summon":Kit.ART_PLAY,"remove":Kit.ART_CLOSE,"dismiss":Kit.ART_CLOSE};gb={"title":"the title \"%s\"","pers":"the %s personality","dye":"the %s dye","voice":"the %s voice","ncol":"the %s name colour","aura":"the %s aura"}
	def gc(b,it):
		a=gb.get(it["cat"],"%s")%it["name"];c=it["cat"]=="title"
		if b=="buy":return "Buy %s for %d squeaks"%(a,bh(it))if not aw(it)else "Buy one %s for %d squeaks"%(a,bh(it))
		if b=="give":return "Give %s a %s now"%(o(),a.lower())
		if b=="wear":return "Put %s on %s"%(a,o())if aS.get(it["cat"])in("hat","neck")else "Give %s %s"%(o(),a)if c else "Switch to %s"%a
		if b=="remove":return "Take %s off (you keep it)"%a if aS.get(it["cat"])in("hat","neck")else "Drop %s (you keep it)"%a if c else "Stop using %s (back to the free one)"%a
		if b=="summon":return "Let %s follow you in the world"%o()
		return "Send %s home to its pen"%o()
	def bi(it):s=it.get("season");return s is None or s in(i["seasons"]or())
	def gd(it):
		if "season"not in it or bi(it):return True
		return m["cnt"].get(it["id"],0)>0 if aw(it)else aa(it["id"])
	def bJ():return cb+[fq]if i["seasons"]else cb
	def dS():
		a=bJ();k=a[min(i["shop_cat"],len(a)-1)][0]
		if k=="season":return[b for b in di if bi(b)]
		return[c for c in bc.get(k,[])if gd(c)]
	dT={"buy":lambda it:f9(it),"give":lambda it:fL(it,time.time()),"wear":lambda it:dP(it,True),"remove":lambda it:dP(it,False)}
	def ge(b,act):
		a=W.get(b)
		if a is None or act not in[c[2]for c in dR(a)]:return
		if act in dT:dT[act](a)
		elif act in("summon","dismiss"):bE(act=="summon");q("%s %s."%(o(),"flutters out to join you"if E["comp"]else "flies home to its pen"),Kit.HUE_INFO)
		i["shop_redraw"]=True
	def dU():b=fH();a=bu[E["share_ch"]];getattr(API,a[1])("%s %s"%(b4,b));i["shared_at"]=time.time();q("%s's code posted in %s chat."%(o(),a[0]),Kit.HUE_INFO)
	def dV(g):
		if g is None:return False
		c=bH()
		if g["uid"]==j["uid"]and g["owner"]==c:return False
		for n,a in enumerate(i["guests"]):
			if a["uid"]==g["uid"]and a["owner"]==g["owner"]:
				if a["code"]!=g["code"]:i["guests"][n]=g;cf();i["pen_redraw"]=True
				return True
		if len(i["guests"])>=az-1:
			b=(g["uid"],g["owner"])
			if b not in i["full_told"]:i["full_told"][b]=True;q("%s (%s's mongotchi) wanted to play, but the playpen is full (%d): send one home with its X."%(g["name"],g["owner"],az),Kit.HUE_INFO)
			return False
		i["guests"].append(g);cf();i["pen_redraw"]=i["ach_due"]=True;q("%s, %s's mongotchi, joined your playpen."%(dw(g["name"],g["title"]),g["owner"]),Kit.HUE_GOOD)
		if not i["pen_open"]:q("open the Playpen to watch them play.",Kit.HUE_INFO)
		return True
	def gf():
		if not i["jcodes_due"]:return
		i["jcodes_due"]=False;a,i["jcodes"]=i["jcodes"],[]
		for b,c in a:
			for m in dz.finditer(b):dV(cm(m.group(1)))
	bK={"key":None,"look":None}
	def bj():
		e=m["eq"];b=(j["sick"],j["asleep"],j["stage"],e.get("dye",""),e.get("hat",""),e.get("neck",""),e.get("aura",""))
		if b==bK["key"]:return bK["look"]
		a=W.get(e.get("dye",""));d=(bX if j["sick"]else bY if j["asleep"]else a["hue"]if a and a["hue"]else bW if j["stage"]==2 else 0);c={"stage":j["stage"],"hue":d,"hat":e.get("hat",""),"neck":e.get("neck",""),"aura":e.get("aura","")};bK["key"],bK["look"]=b,c;return c
	def gg(g):a=W.get(g["dye"]);b=a["hue"]if a and a["hue"]else(bW if g["stage"]==2 else 0);return{"stage":g["stage"],"hue":b,"hat":g["hat"],"neck":g["neck"],"aura":g["aura"]}
	bk={"key":None,"list":[],"keys":[],"der":[],"refs":None}
	def cq():
		e=m["eq"];b=i["guests"];c=bH();d=(j["feral"],j["uid"],c,o(),e.get("title",""),e.get("pers",""),e.get("ncol",""),e.get("toy",""),tuple([id(h)for h in b]))
		if d==bk["key"]:return bk["list"]
		f={"uid":j["uid"],"owner":c,"name":o(),"title":e.get("title",""),"pers":e.get("pers",""),"ncol":e.get("ncol",""),"toy":e.get("toy",""),"mine":True};a=(([]if j["feral"]else[f])+[dict(k,mine=False)for k in b])[:az];bk.update({"key":d,"list":a,"refs":list(b),"keys":[(g["uid"],g["owner"])for g in a],"der":[None]*len(a)});return a
	def gh(n,a):
		b=bk["der"];d=b[n]if n<len(b)else None
		if d is None:
			c=N(a["name"],80);e=W.get(a["ncol"]or "");d={"nm":c,"nw":Kit.text_w(c),"hue":e["hue"]if e else Kit.HUE_TITLE,"spd":40.*W.get(a["pers"]or "p_cheerful",{}).get("speed",1.),"look":None if a["mine"]else gg(a)}
			if n<len(b):b[n]=d
		return d
	cr=.5;dW=3;gi={0:9,1:6,2:6};gj={0:6,1:2,2:2};bL=14186;gk=14138;gl=14052;gm=("Gray","Criminal","Murderer","Enemy");gn=[("follow","follow"),("come","follow"),("stay","stay"),("speak","speak"),("dance","dance"),("trick","dance"),("kill","kill"),("attack","kill"),("good","good"),("sleep","sleep"),("nap","sleep"),("fetch","fetch"),("go home","home"),("dismiss","home")]
	def go():return{"on":False,"x":0,"y":0,"map":None,"mode":"follow","stay":None,"last_p":None,"dir":(0,1),"still_since":time.time(),"next":0.,"aura_at":0.,"talk_at":0.,"help_at":0.,"dive":None,"hp":None,"dead":False,"hidden":False,"war":False,"casting":False,"gold":None,"target":None,"tiles":0,"need_at":0.,"chat_at":0.,"nap":False,"fetch_until":0.,"hover_at":0.,"panic_at":0.,"trick_at":0.,"bob":0,"z":0,"serial":0}
	def cs():return E["comp"]and aa("u_companion")and not j["feral"]and not j["away"]
	def H(text,force=False,hue=None):
		c=i["comp"];t=time.time()
		if not E["comp_talk"]or(not force and t-c["talk_at"]<6.):return
		c["talk_at"]=t;a=eq("ncol");h=hue if hue is not None else(a["hue"]if a else Kit.HUE_TITLE);b=c.get("serial")
		if b:API.HeadMsg("%s: %s"%(o(),text),b,h)
	gp=.5;dX=50;jr={"rd":None,"name":None,"re":None,"now":None}
	def gq():
		a=jr["now"]
		if a is None:
			try:from System import DateTime;a=lambda:float(DateTime.Now.Ticks);a()
			except Exception:a=lambda:time.time()*1e7
			jr["now"]=a
		return a()
	def gs():
		try:
			if jr["rd"]is None:jr["rd"]=Journal.reader();return Journal.recent(Journal.MAX_BACK)
			return jr["rd"].new()
		except Exception:return[]
	def gt():
		a=o()
		if jr["name"]!=a:jr["name"]=a;jr["re"]=re.compile(r"(\b%s\b|^all )"%re.escape(a.lower()))
		return jr["re"]
	def dY(ent,secs,now,t):a=ent[-1];b=(now-a)/1e7 if a>1e12 else t-a;return b<=secs
	def gu(t):
		if t-i["read_at"]<gp:return
		i["read_at"]=t;e=cs();g=not e and aa("u_companion");f=E["listen"]and t-i["listen_at"]>=cS
		if not(e or g or f):i["player"]=None;return
		i["player"]=gz()if e else gv()if g else None
		if f:i["listen_at"]=t
		h=gs();d,c=i["jcodes"],i["jcmds"]
		if bl:
			for k in[n for n,p in bl.items()if t-p>10]:del bl[k]
		if h:
			l=gt()
			for a in h:
				b=a.text
				if b4 in b:d.append((b,a.ticks or a.at))
				if l.search(a.low):
					m=(a.ticks//10000000)if a.ticks else int(a.at);k=(m,a.name,b)
					if k in bl:continue
					bl[k]=t;c.append((b,a.name,0,a.low,a.ticks or a.at))
				elif "Your skill in"in b:c.append((b,a.name,1,a.low,a.ticks or a.at))
		if d or c:
			j=gq()
			if d:i["jcodes"]=[s for s in d if dY(s,cS*3,j,t)][-dX:]
			if c:i["jcmds"]=[v for v in c if dY(v,3.,j,t)][-dX:]
		if f:i["jcodes_due"]=True
	def gv():
		try:P=ch();return{"serial":int(P.Serial),"name":str(P.Name or ""),"lite":True}
		except Exception:return
	aj={"notos":None,"name_ser":None,"name":"","name_at":-99.,"near_at":-99.,"near":0};gw=5.;gx=1.
	def gy(now):
		a=aj["notos"]
		if a is None:a=aj["notos"]=[getattr(API.Notoriety,d)for d in gm]
		if now-aj["near_at"]<gx:c=aj["near"];return dp(c)if c else None
		aj["near_at"]=now;b=API.NearestMobile(a,8);aj["near"]=int(b.Serial)if b is not None else 0;return b
	def gz():
		P=ch()
		if P is None:return
		c=time.time()
		try:
			b=int(P.Serial);d={"serial":b,"x":int(P.X),"y":int(P.Y),"z":int(P.Z),"hidden":bool(P.IsHidden),"dead":bool(P.IsDead),"war":bool(P.InWarMode),"hits":int(P.Hits or 0),"hmax":int(P.HitsMax or 0),"target":None,"name":"","map":int(API.GetMap()),"casting":bool(P.IsCasting),"gold":int(P.Gold or 0)}
			if b!=aj["name_ser"]or c-aj["name_at"]>=gw:aj["name"]=str(P.Name or "");aj["name_ser"],aj["name_at"]=b,c
			d["name"]=aj["name"]
			if not d["war"]:aj["near_at"]=-99.;return d
			a=None;e=int(API.LastTargetSerial or 0)
			if e and e!=b:
				a=dp(e)
				if a is not None and safe(lambda:int(a.Distance)>10,True):a=None
				if a is not None and safe(lambda:bool(a.IsDead),False):d["target"]={"serial":int(a.Serial),"dead":True,"name":""};return d
			if a is None:a=gy(c)
			if a is not None:f,g=int(a.Serial),bool(a.IsDead);d["target"]={"serial":f,"dead":g,"name":str(safe(lambda:a.Name,"")or "")or "foe"}
			return d
		except Exception:return
	def dZ(dur):c=i["comp"];i["hop"].append(ay(bL,c["x"],c["y"],c["z"],0,dur))
	def a1():
		a=i["hop"]
		if not a:return
		i["hop"]=[]
		for f in a:
			try:f()
			except Exception:pass
	def ay(graphic,x,y,z,hue=0,dur=None):dur=cr+.1 if dur is None else dur;return lambda:API.CreateEffect(graphic,type=API.EffectType.FixedXYZ,hue=hue,sourceX=x,sourceY=y,sourceZ=max(-128,min(127,z)),duration=dur)
	def ct(graphic,hue,src=None,dst=None,sxyz=None,txyz=None):
		a={"type":API.EffectType.Moving,"hue":hue,"duration":0}
		if src:a["source"]=src
		if dst:a["target"]=dst
		if sxyz:a["sourceX"],a["sourceY"],a["sourceZ"]=sxyz
		if txyz:a["targetX"],a["targetY"],a["targetZ"]=txyz
		return lambda:API.CreateEffect(graphic,**a)
	def gA(cmd,t):
		c=i["comp"]
		if cmd=="home":bE(False);H("*waves goodbye and flies home*",True);return
		if not c["on"]:
			if cmd=="follow"and aa("u_companion")and not j["feral"]:bE(True);q("%s flutters out to join you."%o(),Kit.HUE_GOOD)
			return
		c["nap"]=False
		if cmd=="follow":c["mode"],c["stay"]="follow",None;H("*flaps after you*",True)
		elif cmd=="stay":c["mode"],c["stay"]="stay",(c["x"],c["y"]);H("*hovers in place*",True)
		elif cmd=="speak":aP();H(l.choice(an["idle"]+af("lines",[])),True)
		elif cmd=="dance":
			if t-c["trick_at"]<20:H("*is dizzy from the last one*",True);return
			c["trick_at"]=t;c["trick_until"]=t+2.;F("joy",2);P("pet");aP();dZ(1.5);H(l.choice(["*does a barrel roll*","*loop-de-loop!*","*spins in the air*"]),True)
		elif cmd=="kill":c["help_at"]=0.;H("*SCREEEECH!*",True,Kit.HUE_BAD)
		elif cmd=="good":F("joy",3);H("*preens proudly*",True)
		elif cmd=="sleep":c["nap"]=True;H("*curls up for a nap*",True)
		elif cmd=="fetch":c["fetch_until"]=t+3.;H("*zooms off*",True)
	gB=[(re.compile(r"\b%s\b"%ic),ie)for ic,ie in gn];gC=re.compile(r"your skill in (.+?) has increased");bl={}
	def gD(t,c):
		d=i["comp"]
		if not i["jcmds"]:return
		b,i["jcmds"]=i["jcmds"],[]
		if len(b)>1:b.sort(key=lambda e:e[2])
		for l,f,g,a,g in b:
			if a.startswith("your skill in")and "increased"in a:
				m=gC.search(a);h=P("skill",3)
				if d["on"]:dZ(1.2);H("*cheers for your %s!* (+%d squeaks)"%(m.group(1)if m else "skill",int(h)),True)
				continue
			if f!=c:continue
			for j,k in gB:
				if j.search(a):gA(k,t);break
	gE=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)];gF={"sick":"*coughs pitifully*","hungry":"*tugs your sleeve: hungry*","dirty":"*sniffs itself... needs a bath*","bored":"*pokes you: play with me?*"}
	def gG(t):
		c=i["comp"]
		if t<c["next"]or i["read_at"]<=c.get("read_seen",-1.):return
		c["next"],c["read_seen"]=t+cr,i["read_at"];a=i.get("player")if(cs()or aa("u_companion"))else None
		if a is None:c["on"]=False;return
		c["serial"]=a["serial"];gD(t,a.get("name")or str(safe(lambda:API.Player.Name,"")or ""))
		if not cs()or a.get("lite"):c["on"]=False;return
		e,f,o=a["x"],a["y"],a["z"]
		if not c["on"]or c["map"]!=a["map"]or max(abs(c["x"]-e),abs(c["y"]-f))>18:
			c.update({"on":True,"x":e,"y":f+1,"map":a["map"],"last_p":(e,f),"mode":"follow"if c["mode"]!="stay"or c["map"]!=a["map"]else c["mode"]})
			if c["mode"]=="follow":c["stay"]=None
			c["hp"],c["gold"]=a["hits"],a["gold"];H(l.choice(["*flutters onto your shoulder*","*squeaks hello*","*circles you happily*"]),True)
		b=[];w=c["last_p"]!=(e,f)
		if w:
			p,q=c["last_p"];x,y=(e>p)-(e<p),(f>q)-(f<q)
			if x or y:c["dir"]=(x,y)
			c["tiles"]+=max(abs(e-p),abs(f-q));c["last_p"]=(e,f);c["still_since"]=t
			if c["nap"]:c["nap"]=False;H("*yawns and catches up*")
		if c["mode"]=="stay"and c["stay"]:
			A,B=c["stay"]
			if max(abs(A-e),abs(B-f))>16:c["mode"],c["stay"]="follow",None;H("*got lonely and flies after you*",True)
			elif t>=c["hover_at"]:c["hover_at"]=t+l.uniform(2,4);c["x"],c["y"]=A+l.randint(-1,1),B+l.randint(-1,1)
		r=gE
		if t<c.get("trick_until",0.):C=int((t-c["trick_at"])/cr)*2%8;c["x"],c["y"]=e+r[C][0],f+r[C][1];b.append(ay(bL,c["x"],c["y"],o+dW,0,.8))
		elif c["mode"]=="follow":
			if w:c["x"],c["y"]=e-c["dir"][0],f-c["dir"][1]
			elif t-c["still_since"]>3 and t>=c["hover_at"]:c["hover_at"]=t+l.uniform(3,6);K,L=l.choice(r);c["x"],c["y"]=e+K,f+L
		if not c["nap"]and t-c["still_since"]>120 and(j["energy"]<60 or j["asleep"]):c["nap"]=True;H("*lands and dozes off*")
		c["bob"]=1-c["bob"];c["z"]=z=o+(0 if c["nap"]or j["asleep"]else dW+c["bob"])
		if a["dead"]!=c["dead"]:
			c["dead"]=a["dead"]
			if a["dead"]:F("joy",-10);H("*wails mournfully*",True,Kit.HUE_BAD)
			else:H("*happy flutter! You're back!*",True)
		if a["hidden"]!=c["hidden"]:
			c["hidden"]=a["hidden"]
			if a["hidden"]:H("*hides with you*",True)
		s,G=a["hits"],max(1,a["hmax"])
		if c["hp"]is not None and not a["dead"]:
			if c["hp"]-s>=G*.1:H(l.choice(["*worried squeak*","*hisses at your attacker*","*flaps anxiously*"]))
			if s<G*.3 and t-c["panic_at"]>e9-Q["com_heal_secs"]*D("com"):c["panic_at"]=t;b.append(ay(gk,e,f,o,0,1.5));H("*licks your wounds* (it's the thought that counts)",True)
		c["hp"]=s
		if a["casting"]and not c["casting"]and l.random()<fa+Q["spi_copy"]*D("spi"):b.append(ay(bL,c["x"],c["y"],z,0,1.));H(l.choice(["*wiggles its wings mystically*","*squeaks along: Kal Ort*","*copies your spell, badly*"]))
		c["casting"]=a["casting"]
		if c["gold"]is not None and a["gold"]>c["gold"]and l.random()<.3:H("*eyes your gold* Shiny!")
		c["gold"]=a["gold"]
		if c["tiles"]>=60:
			c["tiles"]-=60;F("joy",1);F("energy",-1);P("walk",1);M=.06*(2 if aa("u_shiny")else 1)
			if l.random()<M:u=P("shiny",l.randint(5,15));b.append(ay(bL,c["x"],c["y"],z,0,1.));H("*found something shiny!* (+%d squeaks)"%int(u),True);O(aU)
		g=a["target"]
		if a["war"]!=c["war"]:c["war"]=a["war"];H("*bares its tiny fangs*"if a["war"]else "*settles down*")
		if c["target"]and(g is None or g["serial"]!=c["target"]["serial"]or g["dead"]):
			if g is not None and g["serial"]==c["target"]["serial"]and g["dead"]:P("victory",2);F("joy",2);H("*victory squeak!*",True)
			c["target"]=None
		if g is not None and not g["dead"]and a["war"]and E["comp_help"]and not a["dead"]and not j["asleep"]and c["dive"]is None:
			c["target"]=g
			if t>=c["help_at"]:
				N,R=(4,8)if aa("u_war")else(8,15);c["help_at"]=t+l.uniform(N,R)*(1.-Q["val_dive"]*D("val"));c["dive"]={"t":t,"serial":g["serial"],"back":False};d=bj();b.append(ct(bO(d["stage"]),d["hue"],dst=g["serial"],sxyz=(c["x"],c["y"],z)))
				if aa("u_war")and l.random()<.5:b.append(ct(gl,0,dst=g["serial"],sxyz=(c["x"],c["y"],z)))
				S=l.choice(["*bonk!*","*nibble!*","*SCREECH*","*wing slap!*","*dive-bomb!*"]);b.append(lambda:API.HeadMsg(S,g["serial"],Kit.HUE_BAD))
		k=c["dive"]
		if k is not None:
			if not k["back"]and t-k["t"]>=.7:k["back"]=True;d=bj();b.append(ct(bO(d["stage"]),d["hue"],src=k["serial"],txyz=(c["x"],c["y"],z)))
			if t-k["t"]>=1.4:c["dive"]=None
		I=[Z for Z in cp()if Z!="grem"]
		if I and t-c["need_at"]>300:c["need_at"]=t;T=gF.get(I[0],"*squeaks*");H(T,True,Kit.HUE_BAD)
		elif t>=c["chat_at"]:
			c["chat_at"]=t+l.uniform(40,90)/max(.2,af("chat",1.))
			if not c["nap"]and not j["asleep"]:H(l.choice(an["idle"]+af("lines",[])*2))
		J=t<c["fetch_until"]
		if c["fetch_until"]and not J:
			c["fetch_until"]=0.
			if l.random()<.25:u=P("shiny",l.randint(3,10));H("*brings you something shiny!* (+%d squeaks)"%int(u),True)
			else:H(l.choice(["*brings you a stick*","*brings you a bone*","*brings back... a gremlin's sock?*"]),True)
		if a["hidden"]or J or c["dive"]is not None:i["hop"].extend(b);return
		d=bj()
		if a["dead"]:d=dict(d);d["hue"]=a8
		m,n=c["x"],c["y"];h=W.get(d["aura"]or "")
		if h:
			if h.get("seq"):
				if t>=c["aura_at"]:c["aura_at"]=t+1.;U=l.choice(bd)if h.get("rainbow")else h["hue"];b.append(ay(h["seq"][0],m,n,z-1,U,1.05))
			else:b.append(ay(h["gfx"],m,n,z-1,h["hue"]))
		b.append(ay(bO(d["stage"]),m,n,z,d["hue"]))
		for V,X in(("neck",gj),("hat",gi)):
			v=W.get(d[V]or "")
			if v:b.append(ay(v["gfx"],m,n,z+X[d["stage"]],v["hue"]))
		i["hop"].extend(b)
	def d_():i["redraw"]=True
	def gH(a,g):
		def b(*b):
			w=X[a]
			if w["g"]is g and not i["shutting"]:
				w["g"]=None
				if a=="main":HOST.disable(ag)
				else:i[a+"_open"]=False
		return b
	def ad(g,v,graphic,x,y,w,h,hue=0,shown=True):
		p=G.CreateGumpItemPic(graphic,w,h);p.SetPos(x,y)
		if hue:p.Hue=hue
		if not shown:p.IsVisible=False
		p.SetAcceptMouseInput(False);g.Add(p);v.reg(p,gfx=graphic,hue=hue,vis=shown,pos=(int(x),int(y)),size=(int(w),int(h)));return p
	d0=[(25,0,3,3),(24,2,1,2),(21,3,1,4),(22,3,1,3),(23,3,1,2),(20,4,1,4),(18,5,4,2),(15,6,7,1),(14,7,2,2),(19,7,1,11),(12,8,4,1),(10,9,3,1),(10,10,2,1),(9,11,2,1),(7,12,1,4),(8,12,2,1),(8,13,1,1),(6,14,2,2),(4,15,16,1),(4,16,2,1),(20,16,1,2),(3,17,1,4),(4,17,1,1),(21,17,1,4),(7,18,1,1),(16,18,1,1),(2,19,2,2),(1,20,1,4),(22,20,1,4),(2,22,1,2),(3,23,1,2),(7,23,10,1),(21,23,1,2),(4,24,1,3),(19,24,1,3),(20,24,1,2),(5,25,1,2),(6,26,14,1),(6,27,1,3),(7,27,1,1),(16,27,3,1),(5,28,2,2),(17,28,2,1),(4,29,1,2),(18,29,2,1),(0,30,5,1),(19,30,6,1)]
	def gI(g,v,c,x,y):
		a=G.CreateGumpColorBox(0.,"#000000");a.SetRect(int(x),int(y),ak,aH);a.SetAcceptMouseInput(False);a.IsVisible=False;g.Add(a);d=[]
		for e,f,h,i in d0:b=G.CreateGumpColorBox(1.,ey);b.SetRect(e*aG,f*aG,h*aG,i*aG);a.Add(b);d.append(b)
		v.reg(a,vis=False,pos=(int(x),int(y)),size=(ak,aH));c["grem_kids"],c["grem_k"]=d,1.;return a
	def cu(c,k):
		k=round(k,2)
		if c.get("grem_k")==k:return
		c["grem_k"]=k;s=aG*k*c.get("pen_k",1.)
		for f,(a,b,g,h)in zip(c.get("grem_kids",[]),d0):
			d,e=int(round(a*s)),int(round(b*s));i,j=int(round((a+g)*s)),int(round((b+h)*s))
			try:f.SetRect(d,e,max(1,i-d),max(1,j-e))
			except Exception:pass
	def S(g,v,text,x,y,hue=None):a=Kit.add_label(g,text,x,y,hue);v.reg(a,text=text,thue=hue,pos=(int(x),int(y)));return a
	d1="Close"
	def a2(g,store,b,w,title,extra=None,dock=False,close_tip=d1):
		Kit.add_section(g,M,M,w-2*M,30);x=w-M-84-(Kit.DOCK_DX if dock else 0);k=x-(M+30+Kit.text_w(title.upper())+6);l=sum(35+Kit.text_w(p)+6 for n,n,p,n in(extra or[]));d=l>k;h=(x-sum((30 if d else 35+Kit.text_w(t))+6 for s,s,t,s in(extra or[])));c=title.upper()
		if Kit.text_w(c)>h-6-(M+30):c=Kit.fit(c,max(8,h-6-(M+30)))
		Kit.add_label(g,c,M+30,M+7,Kit.HUE_TITLE)
		for i,m,e,j in reversed(extra or[]):x-=30 if d else 35+Kit.text_w(e);Kit.art_button(g,store,i,m,x,M+4,None if d else e,Kit.caption_tip(e,j)if d else j,on_click=V((b,i)));x-=6
		if Kit.zone_up(a3(b)):
			f=Kit.catcher(g,M,M,max(20,x-M-6),30,lambda*a:None,None,movable=True)
			if c!=title.upper():Kit.with_tip(f,title)
			return
		f=Kit.title_catcher(g,M,M,max(20,x-M-6),30,V((b,"toggle_min")),key=ag+b)
		if c!=title.upper():Kit.with_tip(f,"%s. %s"%(title,Kit.DOUBLE_TIP))
		if dock:Kit.dock_button(g,store,w-M-74,M+7,on_click=V((b,"to_bar")))
		Kit.art_button(g,store,"min",Kit.ART_MIN,w-M-74,M+7,None,Kit.MIN_TIP,on_click=V((b,"toggle_min")));Kit.art_button(g,store,"close",Kit.ART_CLOSE,w-M-54,M+4,None,close_tip)
	def cv(g,store,a,title,close_tip=d1,w=None):return Kit.mini_bar(g,store,w or at,by,title,ag+a,V((a,"toggle_min")),close_tip=close_tip)
	def a3(a):return ag if a=="main"else ag+"."+a
	def d2(a):
		if a=="shop":return SW,M+30+T+30+T+cx(bJ())[1]+T+8+3*38+30+M
		return{"pen":(b6,ca),"quest":(JW,JH),"ach":(c8,es)}[a]
	def bM(a,nw,nh):
		z=bR.get(a);b,c=d2(a)
		if z is None or not Kit.zone_up(a3(a))or i[a+"_min"]or z[0]<b or z[1]<c:return nw,nh
		return z
	def gJ(a):
		b=X[a]
		def d():
			if b["g"]is None or i["shutting"]:return
			return "minimized"if i[a+"_min"]else "open"
		def e():
			if a=="pen"and not i["pen_open"]:i["shared_at"]=time.time()
			i[a+"_min"]=False;i[a+"_open"]=i[a+"_redraw"]=True
		def f():i[a+"_min"]=i[a+"_redraw"]=True
		def c():i[a+"_redraw"]=True
		def g(w,h,mode):
			b=(int(w),int(h))if(w is not None and h is not None)else None
			if b!=bR.get(a)or(mode=="again"and b is not None):bR[a]=b;c()
		return{"title":Y+" "+b5[a],"icon":c0,"state":d,"show":e,"minimize":f,"gump":lambda:b["g"],"redraw":c,"fit":g,"min":lambda:d2(a),"exact":True}
	def a4(a,build,w,h,max_h=None,hidden=False):
		b=X[a];d=a3(a);x,y=Kit.load_pos(cZ[a],fj[a],(w,h))
		if Kit.is_open(b["g"]):x,y=b["g"].GetX(),b["g"].GetY()
		c=LAYOUT.spot(d)if HOST.layout_holds(d)else None
		if c is not None:x,y=int(c[0]),int(c[1])
		j,b["g"]=b["g"],None;e,f,v=({},{}),{},View();g=G.CreateGump(True,True);build(g,e,f,v);i=Kit.show_window(g,x,y,w,h,d,hidden,gH(a,g),lambda:cg(a),b,{"g":g,"c":f,"store":e,"v":v},max_h)
		if c is not None and i is not None and tuple(i)!=(x,y):g.SetPos(x,y);Kit.note_rect(g,x,y);Kit.moved_by_code(g)
		if c is not None:LAYOUT.fit_now(d,g)
		Kit.dispose(j)
	def bN(a,title,build,w,h):
		if not i[a+"_min"]:return a4(a,build,w,h)
		def b(g,store,c,v):c["mini"]=cv(g,store,a,title)
		a4(a,b,at,by)
	def d3(a):b=X[a];cg(a);g,b["g"]=b["g"],None;Kit.dispose(g);i[a+"_open"]=False
	gK={539:(7,7),2416:(17,11),2427:(12,8),2430:(16,17),2496:(14,15),2504:(12,14),2505:(18,14),2512:(7,9),2513:(9,10),2537:(23,25),2538:(9,9),2540:(13,17),2544:(13,17),2546:(18,16),2581:(13,26),2586:(13,26),2845:(21,39),3164:(17,15),3178:(16,15),3188:(10,10),3191:(24,25),3203:(42,55),3231:(60,51),3340:(15,24),3365:(36,52),3546:(37,88),3613:(14,14),3629:(13,20),3699:(10,10),3740:(33,32),3741:(16,14),3762:(22,29),3763:(22,18),3847:(9,17),3899:(22,19),3948:(37,88),3971:(9,15),4007:(12,17),4155:(17,15),4167:(21,39),4229:(11,11),4232:(9,10),4233:(10,20),4235:(20,12),4343:(19,23),4554:(38,62),4586:(36,34),4979:(16,17),5063:(15,12),5139:(17,11),5439:(15,9),5443:(11,15),5449:(20,21),5907:(19,17),5908:(17,13),5909:(12,12),5910:(21,22),5911:(20,17),5912:(18,17),5913:(12,13),5914:(17,16),5915:(16,17),5916:(23,11),5919:(15,13),5934:(30,26),7121:(8,8),7946:(10,20),8483:(21,11),8441:(19,42),9638:(51,44),9767:(38,40),10245:(24,25),10290:(15,45),10291:(24,42),11119:(14,12),11120:(12,10),4161:(21,13),11233:(14,18),11229:(10,22),8061:(7,13),5147:(18,19),5445:(21,22),5447:(22,26)};gL={0:-.1,1:.14,2:.14};gM={0:.31,1:.61,2:.61};bm=(14186,15);d4=(14138,16);gN=(14120,13);a5=(14170,16);gO=(14202,15);d5,d6=8,3
	def d7(gfx):return gK.get(gfx,(40,40))
	def bO(stage):return cD if stage==0 else aF
	def K(kind,dur):i["anims"][kind]={"t0":time.time(),"dur":dur}
	def aT(kind,t):
		a=i["anims"].get(kind)
		if a is not None and t-a["t0"]<a["dur"]:return a,(t-a["t0"])/a["dur"]
		return None,0.
	def ah(text,hue,x,y,vx=0.,vy=-20.,dur=1.6,view="main"):
		a=i["parts"][view]
		if len(a)>=d5:a.pop(0)
		a.append({"text":text,"hue":hue,"x":float(x),"y":float(y),"vx":vx,"vy":vy,"t0":time.time(),"dur":dur,"w":Kit.text_px(text)})
	def aE(seq,x,y,dur=1.,hue=0,size=56,view="main"):
		a=i["sprites"][view]
		if len(a)>=d6:a.pop(0)
		a.append({"seq":seq,"x":float(x),"y":float(y),"t0":time.time(),"dur":dur,"hue":hue,"size":size})
	def bn():return i["px"]+J/2.,i["py"]+4
	def bo(text,hue,dx,dy,vx,vy,dur):x,y=bn();ah(text,hue,x+dx,y+dy,vx,vy,dur)
	def a6(text,hue,dx=0,vy=-20.,dur=1.6):x,y=bn();ah(text,hue,x+dx,y,l.uniform(-6,6),vy,dur)
	def d8(v,c,view,t,j,k,w,h):
		a,b=i["parts"][view],i["sprites"][view];m=c.get("pool_n",(len(c["plbl"]),len(c["spr"])))
		if not a and not b and m==(0,0):return
		if a:
			for f in a:
				if t-f["t0"]>=f["dur"]:a=i["parts"][view]=[z for z in a if t-z["t0"]<z["dur"]];break
		if b:
			for f in b:
				if t-f["t0"]>=f["dur"]:b=i["sprites"][view]=[G for G in b if t-G["t0"]<G["dur"]];break
		c["pool_n"]=(len(a),len(b));n=max(len(a),m[0])
		for d,l in enumerate(c["plbl"]):
			if d>=n:break
			if d<len(a):p=a[d];o=t-p["t0"];x=R(p["x"]+p["vx"]*o+2*math.sin(o*6+d)-p["w"]/2.,j+4,j+w-4-p["w"]);y=R(p["y"]+p["vy"]*o,k+20,k+h-16);v.text(l,p["text"],p["hue"]);v.move(l,x,y);v.show(l,True)
			else:v.show(l,False)
		n=max(len(b),m[1])
		for d,g in enumerate(c["spr"]):
			if d>=n:break
			if d<len(b):s=b[d];r,q=s["seq"];u=min(q-1,int((t-s["t0"])/s["dur"]*q));e=s["size"];v.look(g,r+u,s["hue"]);v.size(g,e,e);v.move(g,R(s["x"]-e/2.,j+2,j+w-2-e),R(s["y"]-e/2.,k+2,k+h-2-e));v.show(g,True)
			else:v.show(g,False)
	def d9(g,v,a,b):
		e=[ad(g,v,bm[0]+1,a,b,56,56,shown=False)for h in range(d6)];d=[]
		for f in range(d5):c=S(g,v,"",a+8,b+24,Kit.HUE_TEXT);c.IsVisible=False;v.reg(c,text="",vis=False,pos=(a+8,b+24));d.append(c)
		return e,d
	def bp(c,ctrl,gfx,d,e,k,f):
		if k>=.999:a,b=f
		else:g,h=d7(gfx);a,b=max(1,int(g*k)),max(1,int(h*k))
		c.size(ctrl,a,b);c.move(ctrl,d-a/2.,e-b/2.)
	def ea(g,v,x,y):return{"aura":ad(g,v,14144,x-10,y-8,J+20,ab+14,shown=False),"pet":ad(g,v,aF,x,y,J,ab),"neck":ad(g,v,4232,x,y+22,J,14,shown=False),"hat":ad(g,v,5912,x,y-3,J,22,shown=False)}
	def eb(t,b,phase=0.,stage=1,a=1.):
		s=abs(math.cos(t*b+phase))
		if stage==0:return{"sx":1.,"sy":.94+.06*s,"ox":0.,"oy":2.-4.*s}
		return{"sx":1.-.3*a*(1-s),"sy":1.,"ox":0.,"oy":2.5-5.*s*a}
	def ec(t,phase=0.):return{"sx":.62,"sy":.93+.05*math.sin(t*1.7+phase),"ox":0.,"oy":0.}
	gP={"sx":1.,"sy":1.,"ox":0.,"oy":0.};gQ=(("neck",gM,(J,14)),("hat",gL,(J,22)))
	def bP(v,d,c,e,lk,t,a=None,shown=True):
		if not shown:
			for k in("aura","pet","neck","hat"):v.show(d[k],False)
			return
		a=a or gP;c,e=c+a.get("ox",0.),e+a.get("oy",0.);k=a.get("k",1.);i,j=a["sx"]*k,a["sy"]*k;o=lk["stage"];p=bO(o);q,l=d7(p);r=a.get("hue");v.look(d["pet"],p,lk["hue"]if r is None else r)
		if i>=.999 and j>=.999:m,g=J,ab;n=l
		else:m=q if i>=.999 else max(1,int(q*i));g=l if j>=.999 else max(1,int(l*j));n=g
		v.size(d["pet"],m,g);v.move(d["pet"],c-m/2.,e-g/2.);v.show(d["pet"],True);b=W.get(lk["aura"]or "")
		if b:
			if b.get("seq"):x,y=b["seq"];s=x+int(t*6)%y
			else:s=b["gfx"]
			z=bd[int(t*2.5)%len(bd)]if b.get("rainbow")else b["hue"];v.look(d["aura"],s,z);u,w=int((J+20)*min(1.,k)),int((ab+14)*min(1.,k));v.size(d["aura"],max(1,u),max(1,w));v.move(d["aura"],c-u/2.,e-w/2.)
		v.show(d["aura"],b is not None);A=e-n/2.
		for h,B,C in gQ:
			f=W.get(lk[h]or "")
			if f:v.look(d[h],f["gfx"],f["hue"]);bp(v,d[h],f["gfx"],c,A+B[o]*n,k,C)
			v.show(d[h],f is not None and k>.25)
	def ed(g,c,v):
		c["decor"]=ad(g,v,4554,r+C-50,B+L-58,46,56,shown=False);c["hang"]=ad(g,v,2581,r+C-48,B+20,44,40,shown=False);c["pantry"]=[]
		for a in range(da):e=ap[a%len(ap)][0];c["pantry"].append(ad(g,v,e,r+4+a*11,B+L-38+(a%2)*3,44,34,shown=a<j["pantry"]))
		c["mess"]=[ad(g,v,cE,r+84+f*44,B+L-28,44,24,shown=f<j["messes"])for f in range(b_)];b=i.get("night_a",.55 if j["asleep"]else 0.);c["night"]=Kit.add_box(g,r,B,C,L,max(0.,b),"#000010")
		if c["night"]is not None:v.reg(c["night"],vis=True,alpha=round(b,2),pos=(r,B),size=(C,L))
		c["doll"]=ea(g,v,int(i["px"]),int(i["py"]));c["prop"]=ad(g,v,3613,r,aq,44,34,shown=False);c["grem"]=gI(g,v,c,aC,au);c["prop2"]=ad(g,v,2512,r,aq,44,34,shown=False)
		if "winter"in(i["seasons"]or()):gZ(g,v,c)
		c["spr"],c["plbl"]=d9(g,v,r,B);c["say"]=S(g,v,"",r+8,B+24,Kit.HUE_TEXT);c["pet_hit"]=Kit.catcher(g,int(i["px"]),int(i["py"]),J,ab,V("pet"),"Pet "+o());v.reg(c["pet_hit"],vis=True,pos=(int(i["px"]),int(i["py"])),size=(J,ab));c["grem_hit"]=d=Kit.catcher(g,aC,au,ak,aH,V("swat"),"Swat it before it reaches the pantry (it takes half the food)");d.IsVisible=False;v.reg(d,vis=False,pos=(aC,au),size=(ak,aH))
	ee=.5;gR=26;bq=[("feed",Kit.ART_PLAY,"Feed","Give one food from the pantry"),("play",Kit.ART_PLAY,"Play","Play with its toy: happier, a bit tired"),("brush",Kit.ART_PLAY,"Brush","Brush it: happier, cleaner, a few squeaks"),("clean",Kit.ART_PLAY,"Clean","Tidy the pen and its heaps"),("lights",Kit.ART_PAGE,"Lights","Put it to bed, or wake it up"),("cure",Kit.ART_PLAY,"Cure","Give a Cure potion when it is sick"),("forage",Kit.ART_PLAY,"Forage","Send it to find food (leaves the pantry unguarded)"),("shop",Kit.ART_PAGE,"Shop","Spend squeaks on treats, clothes and more"),("playpen",Kit.ART_PAGE,"Playpen","Open the pen for other players' mongotchis"),("journey",Kit.ART_PAGE,"Journeys","Open treasure hunts and meditation"),("ach",Kit.ART_PAGE,"Achievements","Open milestones that pay squeaks once")]
	def ef():return max(35+Kit.text_w(b)for a,a,b,a in bq)+12
	def cw():return 2*M+24-12+2*ef()
	def bQ(w,h):
		b=w-2*M;Z={"w":w,"IW":b,"top":M+30+T};i=max(Kit.text_w(p)for s,p in bb);Z["bar_w"]=max(40,b-24-i-10-8-Kit.text_w("100%"));j=Kit.text_w("Age 99h 59m");d=Kit.text_w("Wonderfully Happy  (sick)")+6+j<=b-24;e=Kit.text_w("Squeaks 99999")+6+Kit.text_w("Mischievous")<=b-24;Z["pair1"],Z["pair2"]=d,e;l=(1 if d else 2)+(1 if e else 2);Z["sh"]=8+4*18+2+l*18+4;f=ef();n=max(1,min(len(bq),(b-24+12)//f));Z["ncols"],Z["col_w"]=n,f;m=(len(bq)+n-1)//n;Z["ah"]=8+m*26+4;o=Z["top"]+T+Z["sh"]+T+Z["ah"]+M;a=gR
		if h is None:k=min(1.,b/float(C));c=int(round(a+(L-a)*k))
		else:c=h-o;k=min(1.,b/float(C),(c-a)/float(L-a))
		g=k<ee-.001
		if g:k=ee;c=int(round(a+(L-a)*k))
		Z["pen_h"],Z["k"],Z["scroll"]=c,k,g;Z["sy"]=Z["top"]+c+T;Z["ay"]=Z["sy"]+Z["sh"]+T;Z["h"]=Z["ay"]+Z["ah"]+M;Z["ox"]=M+(b-C*k)/2.;Z["oy"]=Z["top"]+a*(1.-k)+(c-a-(L-a)*k)/2.;return Z
	def gS(w,h):
		d=cw();a=1.;b,c=w,h
		if w<d:e=bQ(d,None)["h"];a=min(w/float(d),h/float(e));b,c=int(round(w/a)),int(round(h/a))
		Z=bQ(b,c)
		if Z["scroll"]and a==1.:b=w-Kit.SCROLL_BAND;Z=bQ(b,c);return b,c,a,Z,Z["h"]
		return b,c,a,Z,None
	def eg(g,store,x,y,w,h,c):
		d=Kit.wrap("%s decided it is better off without a master and flew away."%o(),w-40)
		for i,a in enumerate(d[:c]):Kit.add_label(g,a,x+(w-Kit.text_w(a))//2,y+32+i*18,Kit.HUE_INFO)
		b="Adopt a new pup";Kit.art_button(g,store,"adopt",Kit.ART_PLAY,x+(w-35-Kit.text_w(b))//2,y+h-36,b,"Start again; squeaks, wardrobe, virtues and relics stay",on_click=V("adopt"))
	def eh(g,c,v,sy,iw,sh,bw,pair1=True,pair2=True):
		Kit.add_section(g,M,sy,iw,sh);d=M+12+max(Kit.text_w(k)for n,k in bb)+10;c["bars"]={}
		for i,(e,j)in enumerate(bb):b=sy+8+i*18;c["nl_"+e]=S(g,v,j,M+12,b,Kit.HUE_TEXT);Kit.add_tiled(g,Kit.LINE_RED,d,b+3,bw,11);c["bars"][e]=Kit.add_tiled(g,Kit.LINE_BLUE,d,b+3,bw,11);c["nv_"+e]=S(g,v,"",d+bw+8,b,Kit.HUE_INFO)
		h=Kit.text_w("Age 99h 59m");a=sy+82;c["loyal"]=S(g,v,"",M+12,a,Kit.HUE_TEXT)
		if pair1:c["age"]=S(g,v,"",M+iw-12-h,a,Kit.HUE_INFO);c["loyal_w"]=iw-24-h-6
		else:a+=18;c["age"]=S(g,v,"",M+12,a,Kit.HUE_INFO);c["loyal_w"]=iw-24
		f=a+18;c["sq"]=S(g,v,"",M+12,f,Kit.HUE_TITLE)
		if pair2:c["pers"]=S(g,v,"",M+iw-12-Kit.text_w("Mischievous"),f,Kit.HUE_INFO)
		else:c["pers"]=S(g,v,"",M+12,f+18,Kit.HUE_INFO)
	def gT(g,store,c,v,lw,u,d,Z):
		b=Z["IW"];Kit.add_window_frame(g,lw,Z["h"]if Z["scroll"]else u);a2(g,store,"main",lw,Y,[("settings",Kit.ART_PAGE,"Settings",Kit.SETTINGS_TIP%Y)],dock=True,close_tip=Kit.CLOSE_TIP%Y);e,h,k=Z["top"],Z["pen_h"],Z["k"];Kit.add_section(g,M,e,b,h);c["pen_w"],c["iw"],c["bar_w"]=b,b,Z["bar_w"];c["pen_title"]=S(g,v,"",M+8,e+6,Kit.HUE_TITLE);c["pantry_lbl"]=S(g,v,"",M+b-8-Kit.text_w("Pantry 20"),e+6,Kit.HUE_INFO)
		if j["feral"]:eg(g,store,M,e,b,h,max(1,(h-70)//18))
		else:
			v.made=[];ed(g,c,v);i,l=[],set()
			for a in v.made:
				if id(a)not in l:l.add(id(a));i.append(a)
			v.made=None;v.pen=l;v.xf=(r,B,Z["ox"],Z["oy"],k);c["pen_ctrls"]=i;c["pen_k"]=k
			for a in i:
				f=v.cache.get(id(a))or{};m,n=f.get("pos"),f.get("size")
				with Kit.quiet:
					if m is not None:w,x=v.tr(m[0],m[1]);a.SetPos(int(round(w)),int(round(x)))
					if n is not None:a.SetWidth(max(1,int(round(n[0]*k))));a.SetHeight(max(1,int(round(n[1]*k))))
			c["grem_k"]=None;cu(c,1.)
		eh(g,c,v,Z["sy"],b,Z["sh"],Z["bar_w"],Z["pair1"],Z["pair2"]);o=Z["ay"];Kit.add_section(g,M,o,b,Z["ah"]);p,y=Z["ncols"],Z["col_w"]
		for q,(s,z,A,C)in enumerate(bq):Kit.art_button(g,store,s,z,M+12+(q%p)*y,o+8+(q//p)*26,A,C,on_click=V(s))
		if d!=1.:
			Kit.scale_window(g,d)
			if v.xf is not None:v.xf=(r,B,Z["ox"]*d,Z["oy"]*d,k*d);c["pen_k"]=k*d;c["grem_k"]=None;cu(c,1.)
		if v.xf is not None:
			for a in c.get("pen_ctrls")or():
				f=v.cache.get(id(a))or{}
				if "text"in f:
					t=Kit.client_control(a)
					if t is not None:safe(lambda a=t:a.SetInternalScale(v.xf[4]))
	def gU(w,h,mode):
		a=(int(w),int(h))if(w is not None and h is not None)else None
		if a!=i.get("fit")or(mode=="again"and a is not None):i["fit"]=a;i["redraw"]=True
	def gV():return i.get("zone_k")or(1.,None)
	def ei():
		def h(g,store,c,v):
			if i["minimized"]:c["mini"]=cv(g,store,"main",Y,Kit.CLOSE_TIP%Y);return
			Kit.add_window_frame(g,bx,c_);a2(g,store,"main",bx,Y,[("settings",Kit.ART_PAGE,"Settings",Kit.SETTINGS_TIP%Y)],dock=True,close_tip=Kit.CLOSE_TIP%Y);Kit.add_section(g,r,B,C,L);c["pen_title"]=S(g,v,"",r+8,B+6,Kit.HUE_TITLE);c["pantry_lbl"]=S(g,v,"",r+C-8-Kit.text_w("Pantry 20"),B+6,Kit.HUE_INFO)
			if j["feral"]:eg(g,store,r,B,C,L,3)
			else:ed(g,c,v)
			eh(g,c,v,SY,IW,SH,db);Kit.add_section(g,M,AY,IW,AH);b=0
			for d,(k,f,e,h)in enumerate(bq):
				a=M+12+(d%3)*88
				if d%3 and a<b:a=b
				l=AY+8+(d//3)*26;Kit.art_button(g,store,k,f,a,l,e,h,on_click=V(k));b=a+35+Kit.text_w(e)+6
		a=i.get("fit");i["zone_k"]=None
		if a is not None and not i["minimized"]:
			d,k,b,Z,e=gS(a[0],a[1])
			if b!=1.:i["zone_k"]=(b,(cw(),bQ(cw(),None)["h"]))
			def f(g,store,c,v):gT(g,store,c,v,d,k,b,Z)
			if e is not None:a4("main",f,d,e,a[1])
			else:a4("main",f,a[0],a[1])
		elif a is not None:
			def l(g,store,c,v):c["mini"]=cv(g,store,"main",Y,Kit.CLOSE_TIP%Y,w=max(at,a[0]));c["mini_w"]=max(at,a[0])
			a4("main",l,max(at,a[0]),by,None,i["docked"])
		else:w,m=(at,by)if i["minimized"]else(bx,c_);a4("main",h,w,m,None,i["minimized"]and i["docked"])
		ej(time.time(),True);a1()
	hK=None;X=dict((ig,cd if ig=="main"else{"g":None,"c":{},"store":({},{}),"v":None})for ig in bv);bR={}
	def gW():
		b=dw(o().upper(),m["eq"].get("title","")).upper();a=["pup","mongotchi","greater"][j["stage"]]
		if bG(ai):a="avatar"
		return "%s  (%s)"%(b,"gone wild"if j["feral"]else a)
	def ej(t,texts):
		c,v=X["main"]["c"],X["main"]["v"]
		if v is None:return
		if c.get("mini")is not None:
			if i["docked"]:return
			w=cp()
			if texts or w:
				if j["feral"]:l,e="gone wild",Kit.HUE_BAD
				elif w:l=f3[w[0]];e=Kit.HUE_BAD if int(t*2)%2==0 else Kit.HUE_TEXT
				elif j["away"]:l,e=du(),Kit.HUE_INFO
				elif j["asleep"]:l,e="asleep",Kit.HUE_INFO
				else:l,e=dv()
				x,y="%s: %s"%(Y,l),c.get("mini_w",at)-90;n=c.get("mini_fit")
				if n is None or n[0]!=x or n[1]!=y:n=c["mini_fit"]=(x,y,N(x,y))
				v.text(c["mini"],n[2],e)
			return
		for k,Z in bb:a=c.get("bar_w",db)*j[k]/100.;f=i["bar_w"].get(k,a);G=max(1.,abs(a-f)*.25);f=a if abs(a-f)<=G else f+G*(1 if a>f else-1);i["bar_w"][k]=f;v.width(c["bars"].get(k),int(round(f)))
		a=int(m["sq"]);d=i.get("sq_shown",a)
		if d!=a:d+=max(1,abs(a-d)//5)*(1 if a>d else-1);i["sq_shown"]=d;v.text(c["sq"],"Squeaks %d"%d,Kit.HUE_GOOD if a>d or i.get("sq_up")else Kit.HUE_TITLE);i["sq_up"]=a>d
		elif texts:i["sq_shown"]=a;v.text(c["sq"],"Squeaks %d"%a,Kit.HUE_TITLE)
		if texts:
			O=Kit.text_w("Pantry 20");H=eq("ncol");v.text(c["pen_title"],N(gW(),c.get("pen_w",C)-16-O-6),H["hue"]if H else Kit.HUE_TITLE);v.text(c["pantry_lbl"],"Pantry %d"%j["pantry"],Kit.HUE_BAD if j["pantry"]==0 else Kit.HUE_INFO)
			for k,P in bb:I=int(round(j[k]));v.text(c["nv_"+k],"%d%%"%I);v.text(c["nl_"+k],P,Kit.HUE_BAD if I<25 else Kit.HUE_TEXT)
			Q,e=dv();R="  (sick)"if j["sick"]else "";v.text(c["loyal"],N(Q+R,c.get("loyal_w",IW-24-Kit.text_w("Age 99h 59m")-6)),Kit.HUE_BAD if j["sick"]else e);v.text(c["age"],"Age "+hm(j["age"]));v.text(c["pers"],eq("pers")["name"])
		if c.get("doll")is None:return
		g=i["anims"]
		if g:
			for S in[dx for dx,bw in g.items()if t-bw["t0"]>=bw["dur"]]:del g[S]
		J=m["eq"];z=(J.get("decor"),J.get("hang"))
		if c.get("worn")!=z:
			c["worn"]=z
			for k in("decor","hang"):
				o=eq(k)
				if o:v.look(c[k],o["gfx"],o["hue"])
				v.show(c[k],o is not None)
		if z[1]and eq("hang"):v.move(c["hang"],r+C-48+2*math.sin(t*1.3),B+20)
		A,K=aT("pantry_pop",t)if g else(None,0.);q=min(j["pantry"],da)
		if A is not None or c.get("pantry_n")!=q:
			c["pantry_n"]=None if A is not None else q
			for b,p in enumerate(c["pantry"]):
				v.show(p,b<q);T=ap[b%len(ap)][0];D,s=r+4+b*11+22,B+L-38+(b%2)*3+17;k=1.
				if A is not None and b==q-1:k=.3+.7*K;s-=6*math.sin(K*math.pi)
				bp(v,p,T,D,s,k,(44,34))
		E,U=aT("clean",t)if g else(None,0.);F=max(j["messes"],i.get("mess_was",0)if E else 0);u=E is not None
		if g and not u:
			for k in b0:
				if k in g:u=True;break
		if u or c.get("mess_n")!=(F,j["messes"]):
			c["mess_n"]=None if u else(F,j["messes"])
			for b,p in enumerate(c["mess"]):
				M=b<F;v.show(p,M)
				if not M:continue
				D,s=r+84+b*44+22,B+L-28+12;k=1.;V,W=aT(b0[b]if b<len(b0)else "mess%d"%b,t)
				if E is not None and b>=j["messes"]:k=max(.05,1.-U)
				elif V is not None:k=.2+.8*W
				bp(v,p,cE,D,s+(1-k)*8,k,(44,24))
		a=.55 if j["asleep"]and not j["feral"]else 0.;h=i.get("night_a",a);h=a if abs(a-h)<.06 else h+.06*(1 if a>h else-1);i["night_a"]=h;v.alpha(c["night"],h);hj(t,c,v)
		if c.get("snow"):g_(t,c,v)
		if i["seasons"]and "newyear"in i["seasons"]and not i["fw_at"]-b8[1]<=t<i["fw_at"]:g0(t)
		d8(v,c,"main",t,r,B,C,L)
	def gX(t,a,toy):
		y=i["toy"];m=toy.get("motion","bounce");b,c=r+6,r+C-50
		if m in("bounce","bouncy","dice"):
			y[3]+=320.*a;y[0]+=y[2]*a;y[1]+=y[3]*a
			if y[1]>=aq:y[1]=float(aq);y[3]=-l.uniform(220,300)if m=="bouncy"else-l.uniform(80,120)if m=="dice"else-l.uniform(140,220)
		elif m=="float":y[0]+=y[2]*.5*a;y[1]=aq-50+30*math.sin(t*1.7)
		elif m=="scurry":
			y[1]=float(aq);y[0]+=y[2]*1.6*a
			if l.random()<a*.8:y[2]=-y[2]
		elif m=="hover":y[0]=r+C/2.-22+60*math.sin(t*1.3);y[1]=B+50+12*math.sin(t*2.6)
		elif m=="music":
			if t>=i["music_at"]:i["music_at"]=t+2.5;O(toy.get("snd"))
			d=r+C/2.-J/2.;return d+40*math.sin(t*3.),am+20+10*math.sin(t*6.)
		if y[0]<=b or y[0]>=c:y[0]=R(y[0],b,c);y[2]=-y[2]
		return y[0]-6,y[1]-ab+22
	def gY(t,gone):
		if t<i.get("amb_at",0.)or gone or j["feral"]:return
		i["amb_at"]=t+l.uniform(1.2,2.2);x,y=bn()
		if j["asleep"]:ah(l.choice(["z","z","Z"]),eB,x+14,y+4,8.,-14.,2.4);return
		if j["clean"]<35 or j["messes"]>=2:
			ah("~",cF,x+l.uniform(-14,14),y+18,0.,-12.,1.8)
			for a in range(j["messes"]):
				if l.random()<.5:ah("~",cF,r+84+a*44+22,B+L-30,0.,-10.,1.6)
		if j["sick"]and l.random()<.6:ah("o",bX,x+l.uniform(-8,8),y+10,0.,-16.,1.6)
		elif j["food"]<25 and l.random()<.3:ah("?",Kit.HUE_INFO,x+16,y,0.,-10.,1.4)
		elif j["joy"]<25 and l.random()<.3:ah("...",Kit.HUE_INFO,x+16,y,0.,-8.,1.8)
		elif a_()>=85 and l.random()<.15:aE(gO,x,y+18,1.2,0,64)
	ek,el=B+22,B+L-7
	def gZ(g,v,c):
		a=i["snow"]
		if len(a)!=c4:i["snow"]=a=[[l.uniform(r+6,r+C-9),l.uniform(ek,el),l.uniform(c5[0],c5[1]),l.uniform(0.,6.28),l.choice((2,2,3))]for h in range(c4)]
		b=Kit.add_box(g,r+2,B+L-5,C-4,3,.85,"#FFFFFF")
		if b is not None:v.reg(b,pos=(r+2,B+L-5),size=(C-4,3))
		e=[]
		for f in a:
			d=Kit.add_box(g,int(f[0]),int(f[1]),f[4],f[4],.9,"#FFFFFF")
			if d is not None:v.reg(d,pos=(int(f[0]),int(f[1])),size=(f[4],f[4]));e.append((d,f))
		c["snow"],c["snow_ground"]=e,b
	def g_(t,c,v):
		a=max(0.,min(.5,t-i.get("snow_t",t)));i["snow_t"]=t
		for b,f in c["snow"]:
			f[1]+=f[2]*a
			if f[1]>=el:f[0]=l.uniform(r+6,r+C-9);f[1]=float(ek)
			v.move(b,f[0]+3.*math.sin(t*1.3+f[3]),f[1])
	def g0(t):
		i["fw_at"]=t+l.uniform(b8[0],b8[1]);a=l.choice(bd);x=l.uniform(r+40,r+C-40);y=l.uniform(B+36,B+60);aE(a5,x,y,1.,a,48)
		for b in(-14,14):ah("*",a,x+b,y,b*1.6,-8.,.9)
	def g1(t,d,px,py,gr,gone,h,speed,a):
		if j["away"]:
			if not gone:i["tx"],i["ty"],speed,a=aV+30.,float(am),140.,10.
			return speed,a,None,False
		if j["feral"]:return speed,a,None,False
		if j["asleep"]:i["tx"],i["ty"]=float(r+C//2-J//2),float(aB);return 30.,a,None,False
		if gr is not None and gr["phase"]=="walk"and gr["guard_at"]and t>=gr["guard_at"]:i["tx"],i["ty"],speed,a=gr["x"]-6,float(aB),170.,11.;return speed,a,None,False
		if h:
			f=float(i["eat_x"]-6);i["tx"],i["ty"],speed,a=f,float(aB-4),110.,7.;g=abs(px-f)<6 and abs(py-(aB-4))<6;b=1.
			if g:
				i.setdefault("eat_t0",t);b=max(0.,1.-int((t-i["eat_t0"])/.45)*.25)
				if b<i.get("eat_bites",1.):bo(".",eC,l.uniform(-10,10),34,l.uniform(-15,15),10.,.8)
				i["eat_bites"]=b
			return speed,a,(i["eat_food"][0],i["eat_x"]+16,aq+17,0,max(.05,b)),g
		if t<i["play_until"]and i["play_toy"]is not None:
			c=i["play_toy"];i["tx"],i["ty"]=gX(t,d,c);speed,a=95.*af("speed",1.),8.;k=(c["gfx"],i["toy"][0]+22,i["toy"][1]+17,c["hue"],1.)
			if c.get("motion")=="music"and l.random()<d*1.5:bo(l.choice(["~","*","+"]),l.choice(bd),l.uniform(-20,20),6,l.uniform(-10,10),-18.,1.4)
			elif abs(i["toy"][0]+22-(px+J/2.))<14 and l.random()<d*2:bo("!",Kit.HUE_GOOD,0,-4,0.,-24.,.8)
			return speed,a,k,False
		if j["food"]<25 or j["energy"]<15:a=2.6;speed*=.6
		if(abs(i["tx"]-px)<2 and abs(i["ty"]-py)<2 or i["tx"]==0)and t>=i["hover_until"]:
			m=am+30 if(j["food"]<25 or j["joy"]<25)else am;i["tx"]=float(l.randint(c9,aV));i["ty"]=float(l.randint(min(m,aB),aB));i["hover_until"]=t+l.uniform(.5,2.5)/af("speed",1.);e=l.random()
			if a_()>=80 and e<.12:K("loop",1.)
			elif j["food"]<25 and e<.25:K("rumble",.5)
			elif j["energy"]<20 and e<.25:K("yawn",1.4)
		return speed,a,None,False
	def g2(t,a,b,c,hidden,gr):
		if a["who"]=="pet"and not hidden:return b,c+20,1.
		if a["who"]=="grem"and gr is not None:return gr["x"]+ak/2.+14,au+34+2*math.sin(t*10),1.
		if a["who"]!="drop":return
		p=(t-a["t0"])/.8
		if p>=1.:i["carry"]=None;K("pantry_pop",.4);return
		return(a["x"]+(r+34-a["x"])*p,a["y"]+(B+L-20-a["y"])*p-30*math.sin(p*math.pi),1.-.5*p)
	def g3(t,p,a):a["ox"]+=12*math.sin(p*2*math.pi);a["oy"]+=-12*(1-math.cos(p*2*math.pi))/2.
	def g4(t,p,a):a["ox"]+=2*math.sin(t*60)
	def g5(t,p,a):a["sy"]*=1.-.12*math.sin(p*math.pi);a["oy"]+=3*math.sin(p*math.pi)
	def g6(t,p,a):
		if p<.3:a["sy"]*=1.-.22*math.sin(p/.3*math.pi)
		else:a["oy"]-=9*math.sin((p-.3)/.7*math.pi)
	def g7(t,p,a):a["ox"]+=3*math.sin(t*40)*(1-p)
	def g8(t,p,a):a["sy"]*=.75+.25*p;a["oy"]-=6*math.sin(p*math.pi)
	def g9(t,p,a):a["sy"]*=1.-.15*math.sin(p*math.pi);a["oy"]+=2*math.sin(p*math.pi)
	def ha(t,p,a):a["hue"]=bX if int(t*10)%2==0 else 0
	def hb(t,p,a):a["hue"]=a8 if int(t*8)%2==0 else bY
	def hc(t,p,a):a["hue"]=a8 if int(t*8)%2==0 else None;a["k"]=.8+.2*abs(math.sin(t*10))
	def hd(t,p,a):
		a["oy"]-=70*(1-p)**2
		if p>.8:a["sy"]*=1.-.25*math.sin((p-.8)/.2*math.pi)
	he=("loop","rumble","yawn","hop","shake","stretch","cough","flash","spooky","grow","arrive");hf=dict((ii,ih)for ih,ii in enumerate(he));hg=(g3,g4,g5,g6,g7,g8,g9,ha,hb,hc,hd)
	def hh(t,anims,d):
		a=None
		for e,b in anims.items():
			o=hf.get(e)
			if o is None:continue
			c=t-b["t0"]
			if c<b["dur"]:
				if a is None:a=[]
				a.append((o,c/b["dur"]))
		if a is None:return
		if len(a)>1:a.sort()
		for o,p in a:hg[o](t,p,d)
	def hj(t,c,v):
		k=max(0.,min(.5,t-i.get("anim_t",t)));i["anim_t"]=t;d,f=i["px"],i["py"];O=j["stage"];o=35.*af("speed",1.);q=4.;m=i["grem"];s=j["away"]and t>=i["leave_until"];P,Y=aT("zoom",t)
		if P:o*=2.5;q*=2.
		D=t<i["eat_until"]and i["eat_food"]is not None;o,q,b,Q=g1(t,k,d,f,m,s,D,o,q)
		if t<i["cure_until"]:p=1.-(i["cure_until"]-t)/1.5;b=(ez,d+J/2.+26*(1-p),f+18+6*(1-p),0,max(.1,1-p))
		elif t<i["brush_until"]:
			b=(eA,d+J/2.+14*math.sin(t*12),f+14+4*math.cos(t*12),0,1.)
			if l.random()<k*4:bo("*",a8,l.uniform(-18,18),l.uniform(4,24),0.,-14.,.7)
		E=c["doll"];F,w=aT("farewell",t)
		if not s and not j["feral"]:
			if t<i["dizzy_until"]and not j["asleep"]:i["tx"]+=30*math.sin(t*4.)*k*10
			i["tx"]=R(i["tx"],c9,aV+(40 if j["away"]else 0));i["ty"]=R(i["ty"],am,aB);d,f=i["px"],i["py"]=dq(d,f,i["tx"],i["ty"],o*k)
		if j["asleep"]:a=ec(t)
		elif D and Q:a={"sx":.72,"sy":.86+.14*abs(math.sin(t*14)),"ox":0.,"oy":2.}
		else:S=.6 if(j["joy"]<25 or j["sick"])else 1.;a=eb(t,q,0.,O,S)
		if j["sick"]and not j["asleep"]:a["ox"]+=l.uniform(-1.,1.)
		T=i["play_toy"]is not None and t<i["play_until"]and i["play_toy"].get("motion")=="music"
		if T:a["ox"]+=6*math.sin(t*3.);a["oy"]+=3*math.sin(t*12.)
		if t<i["dizzy_until"]and not j["asleep"]:
			a["ox"]+=6*math.sin(t*5.);a["oy"]+=4*math.cos(t*5.)
			if l.random()<k:bo("@",eD,10,-2,4.,-12.,1.)
		if t<i["brush_until"]:a["ox"]+=2*math.sin(t*25)
		G=i["anims"]
		if G:hh(t,G,a)
		if F:a["oy"]-=70*w;a["ox"]+=30*w;a["k"]=max(.05,1.-.9*w)
		x=s or(j["away"]and d>=aV)or(j["feral"]and not F);n,g=min(d,aV)+J/2.,R(f,am-3,aB)+ab/2.
		if x:bP(v,E,0,0,None,t,shown=False);v.show(c["pet_hit"],False)
		else:bP(v,E,n,g,bj(),t,a);v.move(c["pet_hit"],n-J/2.,g-ab/2.);v.show(c["pet_hit"],not j["feral"])
		if b is not None:v.look(c["prop"],b[0],b[3]);bp(v,c["prop"],b[0],R(b[1],r+14,r+C-14),R(b[2],B+30,aq+17),b[4],(44,34));v.show(c["prop"],True)
		else:v.show(c["prop"],False)
		e=i.get("carry");h=None
		if e is not None:
			h=g2(t,e,n,g,x,m)
			if h is not None:v.look(c["prop2"],e["gfx"],0);bp(v,c["prop2"],e["gfx"],h[0],h[1],h[2],(44,34))
			if e["who"]=="pet"and not j["away"]and t-e.get("t0",t)>=1.8:i["carry"]={"who":"drop","gfx":e["gfx"],"t0":t,"x":n,"y":g+20}
		v.show(c["prop2"],h is not None)
		if m is not None:
			U=abs(math.sin(t*10));H=R(m["x"],r+4,aC)+ak/2.;I=au+aH-2*U;u=1.;K=True;y,p=aT("gswat",t)
			if y:K=int(t*12)%2==0;I-=10*math.sin(p*math.pi)
			y,p=aT("gtrap",t)
			if y:u=max(.05,1.-p)
			cu(c,u);V,W=ak*u,aH*u;v.move(c["grem"],H-V/2.,I-W);v.move(c["grem_hit"],H-ak/2.,au);v.show(c["grem"],K);v.show(c["grem_hit"],m["phase"]=="walk")
		else:v.show(c["grem"],False);v.show(c["grem_hit"],False)
		z=i["say"]if not j["asleep"]and t<i["say_until"]and not s else "";v.text(c["say"],z)
		if z:
			M=Kit.text_w(z);X=R(n-M/2.,r+6,r+C-6-M);N=(a or{}).get("oy",0.);A=g+min(0.,N)-ab/2.-22
			if A<B+24:A=g+max(0.,N)+ab/2.+6
			v.move(c["say"],X,R(A,B+24,B+L-18))
		gY(t,x)
	def cx(cats,sw=SW):
		a,x,y=M+10,M+10,0;b=[]
		for n,(e,d,f)in enumerate(cats):
			c=Kit.text_w(d)
			if x+c>sw-M-10 and x>a:x,y=a,y+20
			b.append((n,x,y));x+=c+14
		return b,y+20+14
	def hk():
		a=bJ();i["shop_cat"]=min(i["shop_cat"],len(a)-1);e=M+30+T;b=e+30+T;d,j=bM("shop",SW,b+cx(a)[1]+T+8+c1*38+30+M);n,l=cx(a,d);f=b+l+T;k=j-f-M;h=i["shop_n"]=max(1,(k-38)//38)
		def o(g,store,c,v):
			p=d-2*M;Kit.add_window_frame(g,d,j);a2(g,store,"shop",d,Y+" Shop");Kit.add_section(g,M,e,p,30);c["sq"]=S(g,v,"",M+10,e+7,Kit.HUE_TITLE);B="+%d an hour, even when away"%int(b3);Kit.add_label(g,N(B,p-130),M+p-10-min(Kit.text_w(B),p-130),e+7,Kit.HUE_INFO);Kit.add_section(g,M,b,p,l)
			for q,x,C in n:y=a[q][1];O=Kit.HUE_TITLE if q==i["shop_cat"]else Kit.HUE_TEXT;Kit.add_label(g,y,x,b+7+C,O);Kit.catcher(g,x-3,b+5+C,Kit.text_w(y)+6,18,V(("shop","cat",q)),"Show the %s tab"%y.lower())
			Kit.add_section(g,M,f,p,k);D=dS();E=max(1,(len(D)+h-1)//h);i["shop_page"]=min(i["shop_page"],E-1);F=i["shop_page"]*h
			for G,o in enumerate(D[F:F+h]):
				r=f+8+G*38
				if o["cat"]=="ncol":Kit.add_label(g,"Abc",M+14,r+9,o["hue"])
				elif o["gfx"]:ad(g,v,o["gfx"],M+6,r,44,34,o["hue"])
				x=M+p-10
				for P,(H,I,Q)in enumerate(dR(o)):x-=35+Kit.text_w(I);Kit.art_button(g,store,"r%d_%d"%(G,P),ga[H],x,r+6,I,gc(H,o),on_click=V(("shop","act",o["id"],Q)));x-=8
				t=aa(o["id"])and not aw(o);J=bi(o);K=o["name"]
				if t:z=aS.get(o["cat"]);s="owned"if not z or m["eq"].get(z)!=o["id"]else "worn"if z in("hat","neck")else "in use"
				else:s=("%s only"%dh[o["season"]])if not J else "%d sq"%bh(o);q=m["cnt"].get(o["id"],0)if aw(o)else 0;K+="  x%d"%q if q else ""
				R=Kit.text_w(s);x-=R;T=t or m["sq"]>=bh(o);Kit.add_label(g,s,x,r+9,Kit.HUE_INFO if t or not J else Kit.HUE_GOOD if T else Kit.HUE_BAD);L=x-6-(M+56);Kit.add_label(g,N(K,L),M+56,r+1,Kit.HUE_TEXT);u=dO(o)if not t else None;w=o["desc"]
				if "season"in o:w="%s: %s"%(dh[o["season"]],w[:1].lower()+w[1:])
				Kit.add_label(g,N(u[:1].upper()+u[1:]if u else w,L),M+56,r+18,Kit.HUE_BAD if u else Kit.HUE_INFO)
			A=f+k-28;Kit.art_button(g,store,"prev",fm,M+10,A,None,"Previous page",on_click=V(("shop","prev")));Kit.art_button(g,store,"next",Kit.ART_PLAY,M+p-40,A,None,"Next page",on_click=V(("shop","next")));s="%s: page %d of %d"%(a[i["shop_cat"]][1],i["shop_page"]+1,E);Kit.add_label(g,s,M+(p-Kit.text_w(s))//2,A+3,Kit.HUE_INFO)
		bN("shop","Shop",o,d,j);em(0.,True);a1()
	def em(t,texts):
		c,v=X["shop"]["c"],X["shop"]["v"]
		if v is None or not texts:return
		if c.get("mini")is not None:v.text(c["mini"],"Shop: %d squeaks"%int(m["sq"]))
		elif c.get("sq")is not None:v.text(c["sq"],"Squeaks %d"%int(m["sq"]))
	def hl():
		a=cq();b,e=bM("pen",b6,ca);d=e-ca
		def n(g,store,c,v):
			h=b-2*M;Kit.add_window_frame(g,b,e);a2(g,store,"pen",b,Y+" Playpen",[("share",Kit.ART_PLAY,"Share","Post %s's code in chat for friends' playpens"%o())]);Kit.add_section(g,ac,ae,h,QH+d);c["head"]=S(g,v,"",ac+8,ae+6,Kit.HUE_TITLE);c["toy"]=ad(g,v,3613,ac+20,ae+QH-40,44,34,shown=False);c["dolls"]=[]
			for n in range(az):x=aI+n*(aJ-aI)//max(1,az-1);k=ea(g,v,x,aK+20);k["name"]=S(g,v,"",x,ae+QH-18,Kit.HUE_TITLE);k["say"]=S(g,v,"",x,aK,Kit.HUE_TEXT);c["dolls"].append(k)
			c["spr"],c["plbl"]=d9(g,v,ac,ae)
			if len(a)<=1:
				s="Nobody else here yet. Share your code, or paste a friend's below."
				for t,l in enumerate(Kit.wrap(s,QW-60)[:2]):Kit.add_label(g,l,ac+(QW-Kit.text_w(l))//2,ae+QH//2-40+t*18,Kit.HUE_INFO)
			Kit.add_section(g,M,b9+d,h,dc);m=h//2
			for n in range(az):
				x=M+10+(n%2)*m;y=b9+d+8+(n//2)*25
				if n>=len(a):Kit.add_label(g,"Free slot",x+34,y+3,Kit.HUE_INFO);continue
				f=a[n]
				if not f["mine"]:Kit.art_button(g,store,"rm%d"%n,Kit.ART_CLOSE,x,y,None,"Send %s home"%f["name"],on_click=V(("pen","rm",n)))
				i=f["owner"]
				if Kit.streamer:i=Kit.veil("name",i,Kit.checksum(i.lower().encode("utf-8")))
				u="%s (yours)"%f["name"]if f["mine"]else "%s (%s)"%(f["name"],i);Kit.add_label(g,N(u,m-50),x+34,y+3,Kit.HUE_GOOD if f["mine"]else Kit.HUE_TEXT)
			j=dd+d;Kit.add_section(g,M,j,h,de);Kit.add_label(g,"Code:",M+10,j+12);p="Add";q=M+h-10-35-Kit.text_w(p);r=M+10+Kit.text_w("Code:")+10;c["code"]=Kit.with_tip(Kit.add_textbox(g,"",r,j+9,q-r-12,numbers=False),"A friend's Mongotchi code (64 characters)");Kit.art_button(g,store,"add",Kit.ART_OK,q,j+8,p,"Add that mongotchi to your playpen",on_click=V(("pen","add")))
		bN("pen","Playpen",n,b,e);j={}
		for k in a:
			m=(k["uid"],k["owner"]);f=i["pals"].get(m)
			if f is None:
				h=float(l.randint(aK,bz));f={"x":float(aJ),"y":h,"tx":float(aI+l.randint(0,aJ-aI)),"ty":h,"until":0.,"say":"","say_until":0.,"chase":None,"chase_until":0.,"phase":l.uniform(0,6.28)}
				if i["pals"]:aE(bm,aJ+J/2.,h+ab/2.,1.2,0,64,"pen")
			j[m]=f
		i["pals"]=j;eo(time.time(),True);a1()
	def en(p,text,t,secs=3.):p["say"],p["say_until"]=text,t+secs
	def eo(t,texts):
		c,v=X["pen"]["c"],X["pen"]["v"]
		if v is None:return
		e=cq()
		if c.get("mini")is not None:
			if texts:v.text(c["mini"],"Playpen: %s"%Kit.count(len(e),"mongotchi"))
			return
		f=max(0.,min(.5,t-i.get("pen_t",t)));i["pen_t"]=t
		if texts:v.text(c["head"],N("PLAYPEN  (%d of %d)"%(len(e),az),QW-16))
		g=bk["keys"];a=i.get("pen_game")
		if a is None and len(e)>1 and l.random()<f/25.:
			u=eq("toy")
			if u.get("motion")!="music":i["pen_game"]=a={"until":t+8.,"toy":u,"b":[float(ac+20),float(ae+QH-60),l.uniform(80,120),-80.]}
		if a is not None and t>=a["until"]:i["pen_game"]=a=None
		if a is not None:
			b=a["b"];b[3]+=300.*f;b[0]+=b[2]*f;b[1]+=b[3]*f
			if b[1]>=ae+QH-40:b[1]=float(ae+QH-40);b[3]=-l.uniform(150,230)
			if b[0]<=ac+6 or b[0]>=ac+QW-50:b[0]=R(b[0],ac+6,ac+QW-50);b[2]=-b[2]
			v.look(c["toy"],a["toy"]["gfx"],a["toy"]["hue"]);v.move(c["toy"],b[0],b[1])
		v.show(c["toy"],a is not None)
		for n,d in enumerate(c["dolls"]):
			if n>=len(e):bP(v,d,0,0,None,t,shown=False);v.show(d["name"],False);v.show(d["say"],False);continue
			m=e[n];p=i["pals"].get(g[n])
			if p is None:continue
			h=gh(n,m);r=h["spd"]
			if p["chase"]is not None and t<p["chase_until"]and p["chase"]in i["pals"]:
				q=i["pals"][p["chase"]];p["tx"],p["ty"],r=q["x"],q["y"],90.
				if abs(q["x"]-p["x"])<20 and abs(q["y"]-p["y"])<16:C=(e[g.index(p["chase"])]["name"]if p["chase"]in g else "a friend");en(p,l.choice(fp)%C,t);ah(l.choice(["<3","!","*boop*"]),l.choice([cG,eF,Kit.HUE_GOOD]),q["x"]+J/2.,q["y"],0.,-20.,1.2,"pen");q["hop"]=t;p["chase"]=None;q["tx"],q["ty"]=float(l.randint(aI,aJ)),float(aK);q["until"]=t+1.5
			elif a is not None:p["tx"],p["ty"],r=a["b"][0]-6,a["b"][1]-ab+22,80.
			else:
				p["chase"]=None
				if(abs(p["tx"]-p["x"])<2 and abs(p["ty"]-p["y"])<2)or p["tx"]==0:
					if t>=p["until"]:
						if len(e)>1 and l.random()<.25:p["chase"]=l.choice([G for G in g if G!=g[n]]);p["chase_until"]=t+4.
						p["tx"]=float(l.randint(aI,aJ));p["ty"]=float(l.randint(aK,bz));p["until"]=t+l.uniform(.5,3.)
						if l.random()<.08:D=W.get(m["pers"]or "",{}).get("lines")or an["idle"];en(p,l.choice(D),t)
			p["tx"],p["ty"]=R(p["tx"],aI,aJ),R(p["ty"],aK,bz);p["x"],p["y"]=dq(p["x"],p["y"],p["tx"],p["ty"],r*f);x,y=int(p["x"]),int(R(p["y"],aK-3,bz));k=bj()if m["mine"]else h["look"];w=p.get("phase",n*1.3)
			if m["mine"]and j["asleep"]:k=dict(k);k["hue"]=bY;s=ec(t,w)
			else:E=(p["chase"]is not None and t<p["chase_until"])or a is not None;s=eb(t,8. if E else 4.,w,k["stage"])
			z=t-p.get("hop",-9.)
			if z<.5:s["oy"]-=8*math.sin(z/.5*math.pi)
			bP(v,d,x+J/2.,y+ab/2.,k,t,s);F=h["nm"];v.text(d["name"],F,h["hue"]);A=h["nw"];v.move(d["name"],R(x+J/2.-A/2.,ac+6,ac+QW-6-A),min(y+ab+2,ae+QH-18));v.show(d["name"],True);o=p["say"]if t<p["say_until"]else "";v.text(d["say"],o);v.show(d["say"],bool(o))
			if o:B=Kit.text_w(o);v.move(d["say"],R(x+J/2.-B/2.,ac+6,ac+QW-6-B),max(ae+24,y-18))
		d8(v,c,"pen",t,ac,ae,QW,QH)
	br=M+30+T;ep=48;bs=br+ep+T;a7=bs+30+T;hn=8+ba*38+8;JH=a7+hn+M;bS=100
	def ho():
		a,b=bM("quest",JW,JH)
		def d(g,store,c,v):
			d=c["iw"]=a-2*M;Kit.add_window_frame(g,a,b);a2(g,store,"quest",a,Y+" Journeys");Kit.add_section(g,M,br,d,ep);c["status"]=S(g,v,"",M+10,br+7,Kit.HUE_TITLE);c["status2"]=S(g,v,"",M+10,br+26,Kit.HUE_INFO);f="Call home";h=M+d-10-35-Kit.text_w(f);c["home_x"]=h;c["home_lbl"]=Kit.art_button(g,store,"home",Kit.ART_CLOSE,h,br+12,f,"Bring it back now with a share of the reward",on_click=V(("quest","home")));c["home_btn"]=store[0].get("home");c["was_away"]=j["away"];Kit.add_section(g,M,bs,d,30);x=M+12
			for n,e in enumerate(dm):k=Kit.HUE_TITLE if n==u["tab"]else Kit.HUE_TEXT;Kit.add_label(g,e,x,bs+7,k);Kit.catcher(g,x-3,bs+4,Kit.text_w(e)+6,22,V(("quest","tab",n)),"Show the %s tab"%e.lower());x+=Kit.text_w(e)+24
			i="%s, %s"%(Kit.count(u["hunts"],"hunt"),Kit.count(u["med"],"meditation"));Kit.add_label(g,N(i,d-(x-M)-10),M+d-10-min(Kit.text_w(i),d-(x-M)-10),bs+7,Kit.HUE_INFO);Kit.add_section(g,M,a7,d,b-a7-M);c["rows"]=[];e=u["tab"]
			if e==0:hp(g,store,v,d)
			elif e==1:hq(g,store,d)
			else:hr(g,v,d)
		bN("quest","Journeys",d,a,b);er(time.time(),True);a1()
	def hp(g,store,v,l):
		m=j["away"]
		for i,a in enumerate(ao[:ba]):
			c=a7+8+i*38;d=bB[[s for s in a["loot"]if s[1]=="relic"][0][2]];ad(g,v,d[2],M+6,c,44,34,d[3]);b=ds(a["req"]);x=M+l-10
			if not m and not j["feral"]and b is None:e="Go";x-=35+Kit.text_w(e);Kit.art_button(g,store,"go%d"%i,Kit.ART_PLAY,x,c+6,e,"Send %s hunting at %s (%d min)"%(o(),a["name"],a["mins"]),on_click=V(("quest","hunt",i)));x-=8
			n="safe"if a["danger"]<=.05 else "a little risky"if a["danger"]<=.15 else "risky"if a["danger"]<=.3 else "dangerous";f="%d min, %s"%(a["mins"],n);p=Kit.text_w(f);x-=p;Kit.add_label(g,f,x,c+9,Kit.HUE_INFO if b is None else Kit.HUE_BAD);h=x-6-(M+56);k=u["visits"].get(a["id"],0);q=a["name"]+("  (x%d)"%k if k else "");Kit.add_label(g,N(q,h),M+56,c+1,Kit.HUE_TEXT if b is None else Kit.HUE_INFO);Kit.add_label(g,N(b[:1].upper()+b[1:]if b else a["hint"],h),M+56,c+18,Kit.HUE_BAD if b else Kit.HUE_INFO)
	def hq(g,store,m):
		n=j["away"]
		for i,c in enumerate(al[:ba]):
			k=c[0];b=a7+8+i*38;a=D(k);x=M+m-10
			if not n and not j["feral"]and a<ai:h="Meditate";x-=35+Kit.text_w(h);d,e=ci(k);Kit.art_button(g,store,"med%d"%i,Kit.ART_PLAY,x,b+6,h,"Meditate at the Shrine of %s for %d min (%d/%d to level %d)"%(c[1],int(b1),int(d),int(e),a+1),on_click=V(("quest","med",i)));x-=8
			f=x-bS;Kit.add_tiled(g,Kit.LINE_RED,f,b+12,bS,11);d,e=ci(k);o=bS if a>=ai else int(bS*d/max(1.,e));Kit.add_tiled(g,Kit.LINE_BLUE,f,b+12,max(0,o),11);l=f-6-(M+12);p="%s  Lv %d"%(c[1],a);Kit.add_label(g,N(p,l),M+12,b+1,Kit.HUE_TITLE if a>=ai else Kit.HUE_TEXT);q=(cj(k,a)if a else "Not yet felt: "+cj(k,1).lower()+" at level 1");Kit.add_label(g,N(q,l),M+12,b+18,Kit.HUE_INFO)
	def hr(g,v,h):
		d=h//2
		for i,a in enumerate(aX):
			j,k=i//ba,i%ba;b=M+j*d;c=a7+8+k*38;n=u["relics"].get(a[0],0);e=next((p for p in ao if any(s[1]=="relic"and s[2]==a[0]for s in p["loot"])),None);f=e["name"]if e else ""
			if n:ad(g,v,a[2],b+6,c,44,34,a[3]);l=a[1][0].upper()+a[1][1:]+("  x%d"%n if n>1 else "");Kit.add_label(g,N(l,d-60),b+56,c+1,Kit.HUE_TEXT);Kit.add_label(g,N(f,d-60),b+56,c+18,Kit.HUE_INFO)
			else:Kit.add_label(g,"?",b+24,c+9,Kit.HUE_INFO);Kit.add_label(g,"Not found yet",b+56,c+1,Kit.HUE_INFO);Kit.add_label(g,N("Somewhere at "+f,d-60),b+56,c+18,Kit.HUE_INFO)
	def er(t,texts):
		c,v=X["quest"]["c"],X["quest"]["v"]
		if v is None or not texts:return
		if j["feral"]:b,a="%s has gone wild"%o(),"Adopt a new pup in the pen first"
		elif j["away"]:d=dG(t);b="%s is %s"%(o(),dt());a="Back in about %s (%d%% done)"%(hm(d+59)if d>=60 else "%d seconds"%int(d),int(dH(t)*100))
		else:
			b="%s is at home"%o()
			if u["tab"]==2:a="%d of %d relics found: +%d%% squeaks"%(len(u["relics"]),len(aX),int(round(ck()*100)))
			elif u["tab"]==1:a="Meditation earns experience; each level adds an effect"
			else:a="Far places are slower and riskier (Valor helps)"
		if c.get("mini")is not None:v.text(c["mini"],N("Journeys: %s"%("gone wild"if j["feral"]else du()if j["away"]else "at home"),at-90));return
		e=c.get("home_x",M+300)-(M+10)-8 if j["away"]else c["iw"]-20;v.text(c["status"],N(b,e));v.text(c["status2"],N(a,e));f=bool(j["away"])and j["away_kind"]!=0;v.show(c.get("home_btn"),f);v.show(c.get("home_lbl"),f)
		if j["away"]!=c.get("was_away"):c["was_away"]=j["away"];i["quest_redraw"]=True
	cy=M+30+T;bT=cy+30+T;hs=8+bC*38+8;es=bT+hs+M
	def ht(a,done):
		if done or a[6]is None or a[6]=="stage"or a[7]<=1:return a[2]
		b="{:,}".format(int(min(dK[a[6]](),a[7])));return "%s (%s)"%(a[2],b)if a[7]>=1000 else "%s (%s/%d)"%(a[2],b,a[7])
	def hu():
		a,b=bM("ach",c8,es)
		def d(g,store,c,v):
			i=c["iw"]=a-2*M;Kit.add_window_frame(g,a,b);a2(g,store,"ach",a,Y+" Achievements");Kit.add_section(g,M,cy,i,30);c["status"]=S(g,v,"",M+10,cy+7,Kit.HUE_TITLE);Kit.add_section(g,M,bT,i,b-bT-M);e=i//2;j=[]
			for k,d in enumerate(aM[:2*bC]):f=M+(k//bC)*e;h=bT+8+(k%bC)*38;n=d[0]in U["got"];l="+%d"%d[3];m=Kit.text_w(l);j.append({"a":d,"raw":None,"nw":e-66-m-6,"hw":e-66,"pic":ad(g,v,d[4],f+6,h,44,34,d[5]if n else c7),"nm":S(g,v,"",f+56,h+1,Kit.HUE_TEXT),"rew":S(g,v,l,f+e-10-m,h+1,Kit.HUE_TITLE),"how":S(g,v,"",f+56,h+18,Kit.HUE_INFO)})
			c["rows"]=j
		bN("ach","Achievements",d,a,b);et(0.,True);a1()
	def et(t,texts):
		c,v=X["ach"]["c"],X["ach"]["v"]
		if v is None or not texts:return
		d=U["got"];n=sum(1 for g in aM if g[0]in d);f=sum(h[3]for h in aM if h[0]in d)
		if c.get("mini")is not None:v.text(c["mini"],N("Achievements: %d of %d"%(n,len(aM)),at-90));return
		v.text(c["status"],N("%d of %d earned: +%d squeaks"%(n,len(aM),f),c["iw"]-20))
		for r in c.get("rows",()):
			a=r["a"];b=a[0]in d;e=ht(a,b)
			if r["raw"]==(b,e):continue
			r["raw"]=(b,e);v.look(r["pic"],a[4],a[5]if b else c7);v.text(r["nm"],N(a[1],r["nw"]),Kit.HUE_GOOD if b else Kit.HUE_TEXT);v.text(r["rew"],"+%d"%a[3],Kit.HUE_INFO if b else Kit.HUE_TITLE);v.text(r["how"],N(e,r["hw"]),Kit.HUE_INFO)
	def hv(action,t):
		b,a=action[0],action[1]
		if b=="main":Kit.win_action(a,i,ag,Y,d_,aA["main"])
		elif a=="toggle_min":k=b+"_min";i[k]=not i[k];Kit.save_min(aA[b],i[k]);i[b+"_redraw"]=True
		elif b=="shop":
			if a=="cat":i["shop_cat"],i["shop_page"]=action[2],0
			elif a=="prev":i["shop_page"]=max(0,i["shop_page"]-1)
			elif a=="next":n=len(dS());i["shop_page"]=min(max(0,(n-1)//i["shop_n"]),i["shop_page"]+1)
			elif a=="act":ge(action[2],action[3])
			i["shop_redraw"]=True
		elif b=="quest":
			if a=="tab":u["tab"]=action[2];i["quest_dirty"]=True
			elif a=="hunt":fU(action[2],t)
			elif a=="med":fX(action[2],t)
			elif a=="home":fZ(t)
			i["quest_redraw"]=True
		elif b=="pen":
			if a=="share":dU()
			elif a=="rm":
				d=cq();n=action[2]
				if n<len(d)and not d[n]["mine"]:e=d[n];i["guests"]=[f for f in i["guests"]if not(f["uid"]==e["uid"]and f["owner"]==e["owner"])];cf();q("%s went home."%e["name"],Kit.HUE_INFO);i["pen_redraw"]=True
			elif a=="add":
				m=dz.search(str(safe(lambda:X["pen"]["c"]["code"].Text,"")or ""));c=cm(m.group(1))if m else None
				if c is None:q("that isn't a Mongotchi code (64 characters).",Kit.HUE_BAD)
				elif not dV(c)and c["uid"]==j["uid"]and c["owner"]==bH():q("that's your own mongotchi's code.",Kit.HUE_INFO)
	def bU(action,t):
		w=hy[action]
		if i[w+"_open"]:
			if not Kit.zone_up(a3(w)):d3(w)
		else:
			i[w+"_open"],i[w+"_redraw"]=True,True
			if w=="pen"and not j["feral"]and E["share_open"]and E["share_min"]>0:dU()
			elif w=="pen":i["shared_at"]=t
	def hw(action,t):
		if j["feral"]:cl();i["redraw"]=True
	def hx(action,t):
		if t-i["confirm"]<6.:i["confirm"]=0.;q("%s released; a new pup arrives."%o(),Kit.HUE_INFO);cl();i["redraw"]=True
		else:i["confirm"]=t
		bt(ag)
	hy={"shop":"shop","playpen":"pen","journey":"quest","ach":"ach"};eu={"feed":fJ,"play":fM,"brush":fO,"cure":fR,"forage":fS,"pet":f_,"clean":fP,"lights":fQ,"swat":f1,"window":hv,"shop":bU,"playpen":bU,"journey":bU,"ach":bU,"adopt":hw,"refresh_page":lambda action,t:bt(ag),"release":hx};hz={"fw":60,"ugap":14};ev={"gremlins":("Gremlins raid the pantry","A gremlin that reaches the pantry takes half the food"),"sounds":("Play sounds","Squeaks, munching, gremlins and music"),"remind":("Remind me in the journal of its needs","At most every %d min per need"%int(cQ/60)),"offline":("Keep living while the module is off (up to %d hours)"%b2,"Off: time stops while the module is off (squeaks still trickle in)"),"listen":("Add shared mongotchis to my playpen","Picks up \"%s\" lines from the journal"%b4),"share_open":("Share my code when I open the Playpen","Only while re-share reminders are on; off: only Share posts it"),"comp":("Follows me in the world","Only you see it; \"<name> go home\" or \"<name> come\" work too"),"comp_talk":("Talks over my head","Head messages only you see"),"comp_help":("Joins my fights (just for show)","Dives at your war-mode target; no damage")}
	def hA(w):
		def a(*keys):return[("check",c,N(ev[c][0],w-40),ev[c][1])for c in keys]
		b="Click again to confirm"if time.time()-i["confirm"]<6. else "Release %s"%o();return(("PET",[("text","name","Name:","Up to %d letters (; = | , are dropped)"%cR,{"tw":130}),("num","pace","Pace:","Need speed: 100 = normal, 200 = double","%")+aN["pace"],("num","grem_min","Gremlins every:","Average minutes between raids (%d-%d; the Scarecrow doubles it)"%aN["grem_min"],"min")+aN["grem_min"]]+a("gremlins","sounds","remind","offline")+[("buttons",(("release",Kit.ART_CLOSE,N(b,w-70),"Start over with a new pup (squeaks, wardrobe, virtues and relics stay); click twice within 6 s"),),{"bdy":0})],{"align":True}),("PLAYPEN",[("num","share_min","Remind to re-share every:","Minutes between Share reminders while the Playpen is open (%d-%d, 0 = never, and no post on opening)"%aN["share_min"],"min")+aN["share_min"]]+a("listen","share_open")+[("buttons",(("channel",Kit.ART_PAGE,"Share in: %s"%bu[E["share_ch"]][0],"Next chat for Share: Say, Party, Guild, Alliance or Whisper"),),{"bdy":0})]),("COMPANION  (needs the Companion Charm)",a("comp","comp_talk","comp_help")))
	def hB(f):
		if Kit.was_clicked(f.store,"release"):V("release")()
		if Kit.was_clicked(f.store,"channel"):E["share_ch"]=(E["share_ch"]+1)%len(bu);bD();V("refresh_page")()
	def hC(f,new):new["name"]=ce(new["name"])
	def hD(old,new):
		if new["name"]!=old["name"]:i["redraw_at"]=time.time()+1.5
		i["texts_at"]=0.
	bV=Kit.Page(E,hA,bD,hD,hz,empty=E,adjust=hC,clicks=hB);do()
	def hE():
		t=time.time();i.update({"shutting":False,"docked":HOST.dock_soon(ag),"queue":[],"grem":None,"minimized":Kit.load_min(aA["main"])or bool(HOST.dock_wanted(ag)),"redraw":False,"shop_redraw":False,"pen_redraw":False,"fit":None,"eat_until":0.,"play_until":0.,"cure_until":0.,"brush_until":0.,"leave_until":0.,"next_grem_ok":t+60.,"texts_at":0.,"next_chat":t+10.,"shop_open":False,"pen_open":False,"quest_open":False,"quest_redraw":False,"listen_at":0.,"sleep_after":0.,"pen_game":None,"comp":go(),"hop":[],"read_at":0.,"jcodes":[],"jcmds":[],"jcodes_due":False,"player":None,"close_at":0.,"full_told":{},"shop_dirty":False,"quest_dirty":False,"ach_open":False,"ach_redraw":False,"ach_due":False,"ach_at":0.,"seasons":None,"season_at":0.,"fw_at":0.,"sim_acc":0.,"shop_n":c1});do();fx();fB();fC();fz();dJ(t,force=True)
		if fw():fI()
		else:m["last"]=t;i["shop_dirty"]=True;cl()
		dL(t);i["last_t"]=t;ei();a=Kit.dock_hooks(Y,c0,i,X["main"],d_,fit=gU);a.update({"exact":True,"verify":True,"drawn_at":gV});cA(ag,a);bR.clear()
		for b in b5:cA(a3(b),gJ(b))
	def hF():
		if cd["g"]is None:return
		t=time.time()
		if t-i["close_at"]>=.25:
			i["close_at"]=t
			if Kit.closed(cd):return
			for a in bv:
				w=X[a]
				if a!="main"and w["g"]is not None and Kit.was_clicked(w["store"],"close"):d3(a)
		gu(t)
		if i["queue"]:cz();i["texts_at"]=0.;i["ach_due"]=True
		while i["queue"]:
			b=i["queue"].pop(0);g="window"if isinstance(b,tuple)else b
			if g in eu:eu[g](b,t)
		if i["confirm"]and not 0.<=t-i["confirm"]<6.:i["confirm"]=0.;bt(ag)
		h=max(0.,min(5.,t-i["last_t"]));i["last_t"]=t;dJ(t);c=i["sim_acc"]+h;k=c>=hG
		if k:i["sim_acc"]=0.;ew(c)
		else:i["sim_acc"]=c
		n=not i["minimized"]
		if i["eat_food"]is not None and t>=i["eat_until"]:
			if i["eat_food"][2]:fK()
			else:i["eat_food"]=None
		if i.get("sleep_after")and t>=i["sleep_after"]:
			i["sleep_after"]=0.
			if aQ():j["asleep"]=True;i["say"]=""
		if i["play_until"]and t>=i["play_until"]:i["play_until"]=0.;fN();i["play_toy"]=None
		if j["away"]and t>=i["away_until"]and t>=i["leave_until"]:co()
		f0(t,h,n);fE(t);f5(t)
		if k:f4(t)
		gf();gG(t)
		if i["ach_due"]or not i["ach_at"]-c6<=t<i["ach_at"]:dL(t)
		if i["pen_open"]:
			if E["share_open"]and E["share_min"]and t-i["shared_at"]>=E["share_min"]*60 and not j["feral"]:i["shared_at"]=t;q("time to Share %s's code again."%o(),Kit.HUE_INFO)
			if len(i["guests"])and t-i["social_at"]>=60.:
				i["social_at"]=t;P("social",min(3,len(i["guests"])))
				if not j["asleep"]and not j["feral"]:F("joy",2)
		if i.get("redraw_at")and t>=i["redraw_at"]:i["redraw_at"]=0.;i["redraw"]=i["quest_redraw"]=True
		if i.get("redraw"):
			i["redraw"]=False;ei()
			if i["pen_open"]:i["pen_redraw"]=True
		for a,l,m,d,e in ex:
			if i.get(d):
				i[d]=False
				if i[e]:l()
		f=t-i.get("texts_at",0.)>=1.
		if f:i["texts_at"]=t
		ej(t,f)
		for a,l,m,d,e in ex:
			if i[e]:m(t,f)
		a1()
		if t-i["saved_at"]>=fb:cz();aO()
	hG=1.
	def ew(secs):
		a=[];dC(secs,a);P("passive",b3*secs/3600.)
		if a:dE(a);i["ach_due"]=True
	def cz():
		if i.get("sim_acc",0.)>0.:a,i["sim_acc"]=i["sim_acc"],0.;ew(a)
	ex=tuple((ij,ik,il,ij+"_redraw",ij+"_open")for ij,ik,il in(("shop",hk,em),("pen",hl,eo),("quest",ho,er),("ach",hu,et)))
	def hH():return.1 if not i["minimized"]or(i["pen_open"]and not i["pen_min"])else.5
	def hI():
		i["shutting"]=True;cB(ag)
		for a in b5:cB(a3(a))
		for a in bv:cg(a)
		for k,b in aA.items():Kit.save_min(b,i["minimized"if k=="main"else k+"_min"])
		bD();cz();aO(final=True)
		for a in bv:g,X[a]["g"]=X[a]["g"],None;Kit.dispose(g)
		i["shop_open"]=i["pen_open"]=i["quest_open"]=i["ach_open"]=False
	return{"start":hE,"tick":hF,"stop":hI,"client_tick":True,"config_height":bV.height,"build_config":bV.build,"poll_config":bV.poll,"config_closed":bV.closed,"interval":hH}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("mongotchi","Mongotchi","A pet mongbat to raise and dress up",_module_mongotchi,.1,category="Extras")
