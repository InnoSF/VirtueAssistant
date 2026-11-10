def _module_mongotchi():
	c1=HOST.dock_add;c2=HOST.dock_remove;bN=HOST.refresh_settings;a3=Kit.ART_CLOSE;cg=Kit.ART_OK;aI=Kit.ART_PAGE;ap=Kit.ART_PLAY;bO=Kit.CLOSE_TIP;E=Kit.HUE_BAD;D=Kit.HUE_GOOD;o=Kit.HUE_INFO;ag=Kit.HUE_TEXT;ab=Kit.HUE_TITLE;c3=Kit.SETTINGS_TIP;ch=Kit.add_box;P=Kit.add_label;ah=Kit.add_section;bP=Kit.add_tiled;a4=Kit.add_window_frame;an=Kit.art_button;bn=Kit.catcher;bo=Kit.codec_load;a5=Kit.count;ci=Kit.dispose;a6=Kit.get_var;bp=Kit.load_min;a7=Kit.put_var;c4=Kit.save_min;cj=Kit.set;u=Kit.text_w;ck=Kit.was_clicked;cl=Kit.with_tip;cm=Kit.zone_up;aq="mongotchi";ae="Mongotchi";c5="Mongotchi_settings";import random;c6=8441;aP=9638;aQ=2;e3="#FFFFFF";c7=3899;e4=3847;e5=4979;az=[(2512,"an apple",20),(2505,"a ham",35),(2427,"a fish steak",30),(2513,"some grapes",20),(4155,"a loaf of bread",25),(5919,"a banana",20)];cn=1161;co=2213;cp=1102;bq=1153;e6=1152;c8=2006;e7=1505;e8=1173;c9=33;e9=38;fa=1201;cq=425;da=58;db=87;fb=480;fc=510;fd=1066;fe=946;dc=1078;ff=.15;a8=53;fg=54;fh=43;fi=30.;fj=20.;fk=15.;fl=15.;fm=50.;fn=6.;fo=12.;fp,fq=30,60;cr=3;cs=tuple("mess%d"%h2 for h2 in range(cr));fr=.5;fs=.3;ft=1.;fu=2.;fv=.5;fw=1.;fx=6.;fy=75.;fz=5;fA=12;dd=20;de=30;df=(25,45);ct=20.;fB=60.;dg=(2,4);fC=20;fD=15;ar=10;fE=.01;U={"hon_price":.02,"com_pet":1.,"com_joy_loss":.03,"com_heal_secs":4.,"val_guard":.05,"val_danger":.06,"val_dive":.04,"jus_back":.05,"jus_squeaks":.1,"sac_per":4,"sac_energy":1,"sac_forage_min":5,"sac_hunt_min":8,"hnr_squeaks":.02,"spi_meditate":.05,"spi_relic":.04,"spi_sick":.05,"spi_copy":.03,"hum_hunger":.02,"hum_need":.04,};fF=60.;fG=.25;fH=30.;fI=3600.;fJ=6.;dh=2.5;fK=8.;fL=60.;fM=7.;di=120.;fN=.35;dj=900.;cu=24;dk=12;cv=30.;br={"feed":2,"treat":2,"brush":4,"play":5,"clean":3,"cure":2,"pet":1,"forage":1,"swat":5,"guard":3,"trap":10,"social":1,"grow":25};fO=1.25;aJ=6;cw="Mongotchi code:";bQ=[("Say","Msg"),("Party","PartyMsg"),("Guild","GuildMsg"),("Alliance","AllyMsg"),("Whisper","WhisperMsg")];dl=2.;dm="Mongotchi_state";dn="Mongotchi_shop";do="Mongotchi_guests";dp="Mongotchi_quests";dq="Mongotchi_seasonal";dr="Mongotchi_achievements";ds={"main":"Mongotchi_pos","shop":"Mongotchi_shop_pos","pen":"Mongotchi_pen_pos","quest":"Mongotchi_quest_pos","ach":"Mongotchi_ach_pos"};fP={"main":(200,200),"shop":(510,200),"pen":(200,640),"quest":(510,200),"ach":(540,240)};bR=("shop","pen","quest","ach","main");cx={"shop":"Shop","pen":"Playpen","quest":"Journeys","ach":"Achievements"};aK={"main":"Mongotchi_min","shop":"Mongotchi_shop_min","pen":"Mongotchi_pen_min","quest":"Mongotchi_quest_min","ach":"Mongotchi_ach_min"};bS,dt=300,448;du=c6;aC,bT=240,46;SW=380;dv=6;cy=420;JW=480;bs=8;cz=[("halloween","Halloween",(10,15),(11,1)),("winter","Winter",(12,1),(2,29)),("newyear","New Year",(12,31),(1,2))];fQ=(10,31);dw=3.;dz=60.;dA=14;dB=(12.,24.);cA=(2.5,5.);dC=5.;fR=490;dD=1109;dE=600;fS=(4014,4016,4015);M,X=Kit.MARGIN,Kit.GAP;IW=bS-2*M;r,C,F,Q=M,M+30+X,IW,132;SY,SH=C+Q+X,122;AY,AH=SY+SH+X,116;N,ai=56,48;dF,a9=r+10,r+F-10-N;aw,aL=C+26,C+Q-4-ai;aA=C+Q-36;au,aR=28*aQ,31*aQ;aD=C+Q-aR-2;aM,fT=r+F-au-4,r+60;dG=5;dH=109;aj,al,QW,QH=M,M+30+X,cy-2*M,180;aS,aT=aj+10,aj+QW-10-N;aU,bU=al+26,al+QH-18-ai;cB,dI=al+QH+X,84;dJ,dK=cB+dI+X,40;cC=dJ+dK+M;bt=[("food","Fullness"),("joy","Happiness"),("energy","Energy"),("clean","Cleanliness")];fU=[(95,"Wonderfully Happy"),(85,"Extremely Happy"),(75,"Very Happy"),(65,"Rather Happy"),(55,"Happy"),(45,"Content"),(35,"Unhappy"),(25,"Rather Unhappy"),(12,"Extremely Unhappy"),(-1,"Confused")];ax={"idle":["*squeak*","*flap flap*","*chitters*","Mong!","*hangs around*","*squeak squeak*","*sniffs the air*"],"hungry":["*tummy rumbles*","Food? FOOD?","*eyes the pantry*"],"bored":["*sighs*","*yawns at you*","Play?"],"dirty":["*sniffs... ew*","*holds its nose*"],"sick":["*cough cough*","*shivers*"],"happy":["<3","*happy squeak*","*nuzzles you*"],};fV=["*boops %s*","*tags %s!*","*chases %s*","*squeaks at %s*","*does a loop around %s*","*shares a crumb with %s*","*plays tag with %s*"];cD=[(h3,h4,None if h3 in("treat","upg","ult")else h3)for h3,h4 in(("treat","Treats"),("hat","Hats"),("neck","Necklaces"),("dye","Dyes"),("aura","Auras"),("toy","Toys"),("pers","Personality"),("decor","Decor"),("hang","Hanging"),("title","Titles"),("voice","Voices"),("ncol","Name colours"),("upg","Upgrades"),("ult","Ultimate"))];cE=("dye","toy","pers","voice","ncol")
	def I(*row,**a):return dict(zip(("id","cat","name","price","gfx","hue","desc"),row),**a)
	aE=[I("t_peach","treat","Sugared Peach",15,539,0,"+15 happy, +5 full",joy=15,food=5),I("t_muffin","treat","Muffin",20,2538,0,"+15 full, +10 happy",food=15,joy=10),I("t_cake","treat","Cake",40,2537,0,"+35 happy, +15 full, crumbs",joy=35,food=15,clean=-5),I("t_honey","treat","Jar of Honey",30,2540,0,"+25 energy, +10 happy",energy=25,joy=10),I("t_cheese","treat","Wheel of Cheese",30,2430,0,"+40 full",food=40),I("t_sausage","treat","Sausage",25,2496,0,"+25 full, +10 happy",food=25,joy=10),I("t_ribs","treat","Cut of Ribs",35,2546,0,"+45 full, +5 happy",food=45,joy=5),I("t_melon","treat","Watermelon",25,3164,0,"+20 full, +10 clean, +10 happy",food=20,clean=10,joy=10),I("t_carrot","treat","Carrot",20,3191,0,"Chases off the next gremlin",food=10,guard=True),I("t_pumpkin","treat","Pumpkin",35,3178,0,"+20 happy, +20 full, spooky",joy=20,food=20,spooky=True),I("t_milk","treat","Pitcher of Milk",25,2544,0,"+10 happy, then bed",joy=10,energy=10,sleep=True),I("t_cider","treat","Jug of Cider",30,2504,0,"+20 happy, a bit dizzy",joy=20,dizzy=True),I("t_honeydew","treat","Honeydew Melon",25,3188,0,"+20 full, +15 happy",food=20,joy=15),I("t_stew","treat","Healing Stew",45,2416,0,"Cures sickness, +20 full",food=20,cure=True),I("h_wizard","hat","Wizard's Hat",120,5912,1156,"Kal Vas Flam!"),I("h_witch","hat","Witch's Hat",130,5910,1,"For All Hallows' Eve"),I("h_jester","hat","Jester Hat",90,5916,1157,"For the court fool"),I("h_tricorne","hat","Tricorne",100,5915,1,"Arr, a pirate bat"),I("h_floppy","hat","Floppy Hat",70,5907,1206,"Soft and pink"),I("h_straw","hat","Straw Hat",60,5911,0,"Farm-fresh style"),I("h_feather","hat","Feathered Hat",110,5914,1173,"Bard chic"),I("h_bonnet","hat","Bonnet",70,5913,1201,"Sweet and proper"),I("h_skull","hat","Skullcap",50,5443,1,"Rogue's choice"),I("h_bandana","hat","Bandana",50,5439,33,"Brigand red"),I("h_tribal","hat","Tribal Mask",140,5449,0,"Savage and proud"),I("h_circlet","hat","Royal Circlet",220,11119,0,"Fit for Lord British's court"),I("h_gemcirc","hat","Gemmed Circlet",260,11120,0,"Sparkles in the moonlight"),I("h_jcap","hat","Jester's Cap",90,5934,1172,"Bells not included"),I("h_cap","hat","Cap",40,5909,1505,"Plain and orange"),I("h_widebrim","hat","Wide-Brim Hat",100,5908,1177,"Golden and grand"),I("h_exec","hat","Executioner's Cap",150,3971,1,"Gremlins beware"),I("n_gold","neck","Gold Necklace",80,4232,0,"Plain gold"),I("n_chain","neck","Gold Chain",100,4233,0,"Bling, mongbat style"),I("n_silver","neck","Silver Chain",90,7946,0,"Shiny and cool"),I("n_beads","neck","Beads",60,4235,0,"Colourful beads"),I("n_jewel","neck","Jewelled Necklace",160,4229,1177,"Glitters with gems"),I("n_leather","neck","Leather Gorget",70,5063,0,"Adventurer's guard"),I("n_plate","neck","Plate Gorget",140,5139,0,"A tiny knight")];aE+=[I(h5,"dye",h6,h7,aP,h8,h9)for h5,h6,h7,h8,h9 in(("d_natural","Natural",0,0,"Its own brown"),("d_ice","Ice Blue",120,1152,"Frosty"),("d_gold","Gold",200,1177,"Worth its weight"),("d_teal","Teal",100,1173,"Sea-glass green"),("d_crimson","Crimson",120,1157,"Blood-red"),("d_purple","Royal Purple",140,1158,"Regal"),("d_verdigris","Verdigris",100,2968,"Old bronze"),("d_silver","Silver",160,1150,"Gleaming"),("d_sapphire","Sapphire",160,1195,"Deep blue"),("d_orchid","Orchid",120,1168,"Pretty in purple"),("d_violet","Violet",120,1171,"Twilight"),("d_shadow","Shadow",180,1109,"Blends into the night"),("d_rose","Rose",100,1206,"Blushing"),("d_midnight","Midnight",180,1156,"Darkest blue"))];aE+=[I("a_holy","aura","Holy Light",250,14144,0,"Blue-white sparkles",seq=(14138,16)),I("a_embers","aura","Embers",250,14160,0,"Red sparks",seq=(14154,16)),I("a_star","aura","Starlight",300,14176,0,"Stars of blue and gold",seq=(14170,16)),I("a_fairy","aura","Fairy Dust",300,14192,0,"Twinkling motes",seq=(14186,15)),I("a_snow","aura","Snowfall",280,14210,1153,"Gentle snowflakes",seq=(14202,15)),I("a_phoenix","aura","Phoenix Sparks",350,14144,1161,"Golden fire",seq=(14138,16)),I("a_toxic","aura","Toxic Glitter",300,14144,1405,"Poisonously pretty",seq=(14138,16)),I("a_bluegate","aura","Blue Moongate",400,3948,0,"A halo of moonlight"),I("a_redgate","aura","Red Moongate",400,3546,0,"A gate of crimson"),I("a_halo","aura","Golden Halo",500,3948,1177,"Saintly"),I("a_void","aura","Void Gate",450,3948,1158,"From beyond"),I("a_storm","aura","Lightning",450,14672,0,"Crackling energy",seq=(14662,31)),I("a_rainbow","aura","Rainbow",600,14144,0,"Every colour at once",seq=(14138,16),rainbow=True),I("y_yarn","toy","Ball of Yarn",0,3613,0,"The classic",motion="bounce"),I("y_ball","toy","Bouncy Ball",60,3699,33,"Boing! +5 happy",motion="bouncy",joy=5),I("y_feather","toy","Feather",50,7121,0,"Floats down; less tiring",motion="float",energy=5),I("y_rat","toy","Toy Rat",90,8483,0,"+10 happy, tiring",motion="scurry",joy=10,energy=-5),I("y_dice","toy","Dice",70,4007,0,"A gamble: 10-45 happy",motion="dice"),I("y_crystal","toy","Crystal Ball",200,3629,0,"+5 squeaks a game",motion="hover",squeaks=5),I("y_drum","toy","Drum",120,3740,0,"It dances along",motion="music",snd=56),I("y_tamb","toy","Tambourine",100,3741,0,"Shake shake shake",motion="music",snd=82),I("y_lute","toy","Lute",150,3763,0,"A bard's tune",motion="music",snd=76),I("y_harp","toy","Lap Harp",180,3762,0,"Soothing: +10 happy",motion="music",snd=69,joy=10),I("y_flute","toy","Bamboo Flute",130,10245,0,"Toot toot",motion="music",snd=61),I("p_cheerful","pers","Cheerful",0,3643,0,"Sunny and easy-going"),I("p_playful","pers","Playful",150,3643,1206,"Loves games; gets bored faster",play=1.5,joy_rate=1.2,speed=1.3,lines=["*does a loop-de-loop*","Tag! You're it!","*bounces off the walls*"]),I("p_lazy","pers","Lazy",100,3643,1109,"Tires slowly, sleeps deeply, flies slow",energy_rate=.6,sleep=1.25,speed=.6,lines=["*yawns*","*naps mid-flap*","Five more minutes..."]),I("p_glutton","pers","Gluttonous",120,3643,1505,"Always hungry; food cheers it",food_rate=1.3,feed_joy=15,lines=["Snack time?","*drools*","*sniffs for crumbs*"]),I("p_brave","pers","Brave",200,3643,33,"Chases off gremlins more often",guard=.75,lines=["*flexes*","Gremlins fear me!","*guards the pantry*"]),I("p_shy","pers","Shy",120,3643,1152,"Quiet; loves being petted",pet=8,chat=.4,lines=["*hides behind its wings*","...squeak","*peeks at you*"]),I("p_mischief","pers","Mischievous",180,3643,1405,"More food; may steal some back from gremlins",forage=1,stealback=.3,lines=["*snickers*","*eyes the gremlins' stash*","*hides a grape*"]),I("p_grumpy","pers","Grumpy",100,3643,1157,"Hard to please, slow to sulk",joy_rate=.85,lines=["*grumbles*","Hmph.","*glares at the gremlin hole*"]),I("p_scholar","pers","Scholarly",250,3643,1156,"Earns 20% more squeaks",squeak=1.2,lines=["*reads a tiny spellbook*","*mutters Kal Vas Flam*","*adjusts its spectacles*"]),I("p_drama","pers","Dramatic",120,3643,1158,"Everything is a tragedy (or triumph)",chat=1.6,lines=["*faints dramatically*","Woe! WOE!","*poses heroically*"]),I("o_pillow","decor","Straw Pillow",120,4586,0,"Sleeps 25% better",sleep=1.25),I("o_flowers","decor","Potted Flowers",60,4554,0,"A splash of colour"),I("o_fern","decor","Fern",50,3231,0,"Leafy"),I("o_cactus","decor","Cactus",50,3365,0,"Don't hug it"),I("o_globe","decor","Globe",90,4167,0,"Sosaria, in miniature"),I("o_mushroom","decor","Mushrooms",40,3340,0,"Mysterious fungi"),I("o_pumpkin","decor","Pumpkin",60,3178,0,"Happy Halloween"),I("o_crystal","decor","Crystal Ball",150,3629,0,"It sees all"),I("o_wildflowers","decor","Wildflowers",50,3203,0,"Fresh from the meadow"),I("o_candles","decor","Candelabra",100,2845,0,"Cosy candlelight"),I("g_lantern","hang","Lantern",60,2581,0,"A warm glow"),I("g_hanglamp","hang","Hanging Lantern",80,2586,0,"Swings gently"),I("g_chimes","hang","Wind Chimes",70,10290,0,"Tinkle tinkle"),I("g_fancy","hang","Fancy Wind Chimes",110,10291,0,"Crystal clear"),I("x_brave","title","the Brave",80,3827,0,"Fearless"),I("x_fluffy","title","the Fluffy",60,3827,0,"So soft"),I("x_magnif","title","the Magnificent",150,3827,0,"Behold!"),I("x_britain","title","of Britain",100,3827,0,"A city bat"),I("x_belfry","title","of the Belfry",120,3827,0,"Lord of the bell tower"),I("x_spooky","title","the Spooky",90,3827,0,"Boo!"),I("x_bane","title","Gremlin Bane",100,3827,0,"Needs 10 gremlins swatted",req="swats"),I("x_greater","title","the Greater",100,3827,0,"Needs a Greater Mongotchi",req="greater"),I("x_elder","title","the Elder",200,3827,0,"Needs an age of 24 hours",req="elder"),I("x_avatar","title","the Avatar",1000,3827,1177,"Needs every virtue at level 5",req="avatar"),I("x_explorer","title","the Explorer",150,3827,0,"Needs 8 different relics",req="relics"),I("x_pilgrim","title","the Pilgrim",200,3827,0,"Needs a virtue at level 10",req="pilgrim")];aE+=[I(ia,"voice",ib,ic,ie,0,ig,snd=ih)for ia,ib,ic,ie,ig,ih in(("v_mongbat","Mongbat",0,8441,"Its own squeak",422),("v_cat","Cat",60,8475,"Meow?",105),("v_dog","Dog",60,8476,"Woof!",133),("v_chicken","Chicken",50,8401,"Bawk!",110),("v_bird","Songbird",60,8474,"Tweet",23),("v_pig","Pig",50,8449,"Oink",196),("v_cow","Cow",50,8451,"Moo",120),("v_sheep","Sheep",50,8422,"Baa",214),("v_frog","Bullfrog",60,8496,"Ribbit",614),("v_wisp","Wisp",120,8448,"Ethereal chimes",466),("v_ghost","Ghost",100,9671,"Ooooo",382),("v_dragon","Dragon",200,8406,"ROAR",362),("v_daemon","Daemon",200,8452,"From the abyss",357),("v_gazer","Gazer",120,8436,"Blorp",377))];aE+=[I("c_gold","ncol","Gold",0,0,53,"The usual"),I("c_white","ncol","White",40,0,1153,"Clean and bright"),I("c_green","ncol","Green",40,0,68,"Fresh"),I("c_red","ncol","Red",40,0,33,"Fierce"),I("c_blue","ncol","Sky Blue",50,0,1173,"Breezy"),I("c_pink","ncol","Pink",50,0,1201,"Adorable"),I("c_fire","ncol","Fire",80,0,1161,"Blazing"),I("c_ice","ncol","Ice",80,0,1152,"Chilly"),I("u_pantry","upg","Bigger Pantry",150,3703,0,"Holds %d food"%dd),I("u_trap","upg","Gremlin Trap",40,4343,0,"Catches the next gremlin (+10 sq)",uses=True),I("u_luck","upg","Lucky Black Pearl",250,3962,0,"+25% squeaks, forever"),I("u_groom","upg","Grooming Kit",100,4979,0,"Brushing does double"),I("u_feeder","upg","Auto-Feeder",200,3711,0,"Feeds it from the pantry when hungry"),I("u_ward","upg","Scarecrow",300,7732,0,"Half as many gremlins"),I("u_companion","ult","Companion Charm",2500,3676,1161,"Follows you in the world and joins fights",toggle=True),I("u_war","ult","War Training",800,8012,33,"Dives at foes twice as often, with fireballs",req="charm"),I("u_shiny","ult","Shiny Sense",600,3821,0,"Finds shiny things twice as often on walks",req="charm"),I("h_orcmask","hat","Orc Mask",90,5147,0,"An orc costume",season="halloween"),I("h_bearmask","hat","Bear Mask",100,5445,0,"A bear costume: rawr!",season="halloween"),I("h_deermask","hat","Deer Mask",100,5447,0,"Antlers and all",season="halloween"),I("d_ghost","dye","Ghost Costume",150,aP,1153,"A sheet with eye holes",season="halloween"),I("d_pumpkin","dye","Pumpkin Costume",150,aP,1505,"Round, orange and grinning",season="halloween"),I("t_pie","treat","Pumpkin Pie",35,4161,0,"+25 full, +15 happy, spooky",food=25,joy=15,spooky=True,season="halloween"),I("t_pbread","treat","Pumpkin Bread",30,4155,1505,"+25 full, +10 happy",food=25,joy=10,season="halloween"),I("h_wintercap","hat","Winter Cap",70,5909,1153,"Warm and woolly",season="winter"),I("h_holiday","hat","Holiday Hat",110,5912,33,"Red, pointy and festive",season="winter"),I("h_snowbonnet","hat","Snow Bonnet",80,5913,1152,"Frosted lace",season="winter"),I("o_snowman","decor","Snowman",100,9000,0,"Carrot nose included",season="winter"),I("o_gifts","decor","Gift Box",80,9002,0,"No peeking!",season="winter"),I("g_mistletoe","hang","Mistletoe",70,9076,0,"Who's under it?",season="winter"),I("g_wreath","hang","Holly Wreath",90,9004,0,"Evergreen and berries",season="winter"),I("t_ginger","treat","Gingerbread Man",25,11233,0,"+20 happy, +10 full",joy=20,food=10,season="winter"),I("t_cane","treat","Candy Cane",25,11229,0,"+25 energy, +5 happy",energy=25,joy=5,season="winter"),I("h_partycap","hat","Party Cap",90,5934,1177,"Ring in the new year",season="newyear"),I("a_fireworks","aura","Fireworks",400,14176,0,"Bursts of every colour",seq=(14170,16),rainbow=True,season="newyear"),I("t_fizz","treat","Sparkling Cider",30,8061,0,"+20 happy, +10 energy, fizzy",joy=20,energy=10,dizzy=True,season="newyear"),I("x_festive","title","the Festive",120,3827,0,"Toasts the new year",season="newyear"),];ac=dict((ii["id"],ii)for ii in aE);bu={}
	for dL in aE:bu.setdefault(dL["cat"],[]).append(dL)
	dM=set(ij["id"]for ij in aE if ij["price"]==0);dN=dict((ik[0],ik[1])for ik in cz);dO=[il for il in aE if il.get("season")];bV=frozenset(im["id"]for im in dO);fW=("season","Seasonal",None);dP=("dye","hat","neck","aura","pers","toy","title","voice","ncol","decor","hang");bv=[1157,1505,1177,1405,1173,1156,1158,1206]
	def ba(k):return int(round(U[k]*100))
	av=[("hon","Honesty","Dagger Isle","Shop prices %d%% lower",ba("hon_price")),("com","Compassion","the Britain road","Petting +%d happy; heals you sooner",int(U["com_pet"])),("val","Valor","the isle south of Jhelom","Guards the pantry +%d%%; hunts safer; dives sooner",ba("val_guard")),("jus","Justice","the Yew woods","Wins back %d%% of stolen food",ba("jus_back")),("sac","Sacrifice","the Minoc desert","Brings +%d food home; trips cost less energy",-U["sac_per"]),("hnr","Honor","the Trinsic road","%d%% more squeaks from everything",ba("hnr_squeaks")),("spi","Spirituality","the Skara Brae road","Meditation +%d%%; relic luck up; sickness down",ba("spi_meditate")),("hum","Humility","the isle off Magincia","Hunger %d%% slower; needs sting less",ba("hum_hunger")),];aV=[io[0]for io in av];dQ=dict((ip[0],ip)for ip in av);dR={"hon":["*looks you straight in the eye*","*would never fib*"],"com":["*nuzzles you gently*","*checks that you're all right*"],"val":["*puffs up bravely*","*guards the pen*"],"jus":["*weighs the crumbs fairly*","*glares at the gremlin hole*"],"sac":["*offers you a crumb*","*saves the last bite for you*"],"hnr":["*bows with dignity*","*keeps its word*"],"spi":["*hums an old hymn*","*meditates on its perch*"],"hum":["*bows its little head*","*is content with a crumb*"],};bb=[("r_horseshoe","a lucky horseshoe",4022,0),("r_goldegg","a golden egg",2485,1177),("r_mandrake","a fat mandrake root",3974,0),("r_glowshroom","a glowing mushroom",3340,1173),("r_ore","a shiny ore nugget",6585,1150),("r_goldingot","a gold ingot",7154,1177),("r_conch","a conch shell",4036,0),("r_blackpearl","a perfect black pearl",3962,0),("r_fang","a silver serpent fang",3966,1150),("r_eye","a serpent's eye emerald",3856,0),("r_obsidian","a shard of obsidian",3977,0),("r_phoenix","a phoenix feather",7121,1161),("r_scale","a dragon scale",9908,0),("r_dblood","a vial of dragon's blood",3970,0),("r_scroll","a scroll of ancient lore",3637,0),("r_sextant","a cracked sextant",4183,0),];bW=dict((iq[0],iq)for iq in bb)
	def aN(*row):return dict(zip(("id","name","mins","danger","req","bad","hint","loot"),row))
	ay=[aN("farm","The Britain Farmlands",8,.05,None,"an angry farmer's dog chased it off","apples, carrots, a few squeaks",[(5,"sq",4,10),(5,"food",1,2),(2,"treat","t_peach",0),(2,"treat","t_carrot",0),(1,"treat","t_milk",0),(1.2,"relic","r_horseshoe",0),(.4,"relic","r_goldegg",0)]),aN("yew","The Spiritwood, Yew",12,.1,None,"it got lost among the trees","honey, mushrooms, roots",[(5,"sq",6,14),(3,"food",1,2),(2,"treat","t_honey",0),(1,"treat","t_honeydew",0),(1.2,"relic","r_mandrake",0),(.4,"relic","r_glowshroom",0)]),aN("minoc","The Minoc Mines",15,.15,("stage",1),"a rockfall nearly caught it","squeaks, ore, the odd gold ingot",[(6,"sq",10,25),(1,"food",1,1),(1,"trap",0,0),(1,"treat","t_cheese",0),(1.2,"relic","r_ore",0),(.4,"relic","r_goldingot",0)]),aN("ship","The Sunken Ship, off Ocllo",18,.2,("stage",1),"a sea serpent surfaced beside it","fish, shells, pearls",[(4,"sq",8,20),(4,"food",1,3),(1,"treat","t_melon",0),(1,"treat","t_ribs",0),(1.2,"relic","r_conch",0),(.4,"relic","r_blackpearl",0)]),aN("terra","Terra Sanctum",22,.3,("virtue","val",2),"a silver serpent bit it","silver serpent fangs, silk, squeaks",[(5,"sq",10,24),(1,"food",1,2),(1,"trap",0,0),(1,"treat","t_stew",0),(1.5,"relic","r_fang",0),(.4,"relic","r_eye",0)]),aN("volcano","The Volcano, Hythloth Island",28,.4,("virtue","val",4),"it singed its wings on the lava","obsidian, sulphurous ash, phoenix feathers",[(5,"sq",12,30),(1,"trap",0,0),(1,"treat","t_pumpkin",0),(1,"treat","t_cider",0),(1.5,"relic","r_obsidian",0),(.4,"relic","r_phoenix",0)]),aN("destard","Destard",35,.5,("virtue","val",6),"a dragon woke up","dragon scales and hoard gold",[(5,"sq",20,45),(1,"treat","t_cake",0),(1,"treat","t_sausage",0),(1,"trap",0,0),(1.5,"relic","r_scale",0),(.5,"relic","r_dblood",0)]),aN("lycaeum","The Lycaeum, Moonglow",15,.05,("virtue","spi",2),"a librarian shooed it out","scrolls, squeaks, odd instruments",[(6,"sq",10,22),(1,"food",1,1),(1,"treat","t_muffin",0),(1.2,"relic","r_scroll",0),(.4,"relic","r_sextant",0)]),];fX=dict((ir["id"],ir)for ir in ay);dS=["Treasure hunts","Meditation","Relics"];fY=502;aW=[("grown","All grown up","Raise a pup to adulthood",10,aP,0,"stage",1),("greater","Well raised","Raise a Greater Mongotchi",40,aP,cn,"stage",2),("elder","Elder","A mongotchi 24 hours old",30,6160,0,"age",24),("swat1","Swat!","Swat a gremlin",5,4163,0,"swats",1),("swat25","Gremlin bane","Swat 25 gremlins",30,3971,1,"swats",25),("trap","Snap!","Catch a gremlin in a trap",10,4343,0,None,1),("sq1k","A thousand squeaks","Earn 1,000 squeaks",25,3821,0,"earned",1000),("sq10k","Squeak hoard","Earn 10,000 squeaks",100,3823,0,"earned",10000),("relic1","First relic","Find a relic on a hunt",15,4022,0,"relics",1),("relics","Curator","Find all %d relics"%len(bb),100,2485,1177,"relics",len(bb)),("places","Seasoned traveller","Hunt at all %d places"%len(ay),40,5355,0,"places",len(ay)),("shrines","Pilgrimage","Meditate at all %d shrines"%len(av),40,2600,0,"shrines",len(av)),("avatar","Avatar","Every virtue at level 5",100,11119,1177,"virtue5",len(av)),("friend","Playdate","A friend's mongotchi visits",10,3613,0,"guests",1),("charm","Best friends","Buy the Companion Charm",50,3676,1161,"charm",1),("festive","Festive","Give a treat in its season",20,3178,0,None,1),];fZ=dict((iu[0],iu)for iu in aW);bX=8;f_=200;J={"name":"Flapjack","pace":100,"grem_min":20,"share_min":10,"gremlins":True,"sounds":True,"remind":True,"offline":False,"listen":True,"share_ch":0,"comp":False,"comp_talk":True,"comp_help":True,"share_open":True};dT=dict(J);aX={"pace":(25,400),"grem_min":(5,240),"share_min":(0,60),"share_ch":(0,len(bQ)-1)};bc={"food":80.,"joy":80.,"energy":90.,"clean":100.,"sick":False,"sick_t":0.,"asleep":False,"age":0.,"care_sum":0.,"care_t":0.,"stage":0,"pantry":fz,"messes":0,"neglect":0.,"warned":False,"feral":False,"mess_in":40*60.,"supply_in":de*60.,"away":False,"away_left":0.,"fed":0,"swats":0,"stolen":0,"uid":0,"guard":False,"last":0.,"away_kind":0,"away_loc":0,"away_virt":0,"away_total":0.};j=dict(bc);f0=["hat","neck","dye","aura","toy","pers","decor","hang","title","voice","ncol"];l={"sq":0.,"own":set(),"cnt":{},"eq":{},"last":0.};A={"xp":dict((iv,0.)for iv in aV),"relics":{},"visits":{},"hunts":0,"med":0,"tab":0};Y={"got":set(),"earned":0.,"swats":0,"new":False};i={"minimized":False,"shutting":False,"docked":False,"queue":[],"last_t":0.,"sim_acc":0.,"saved_at":0.,"say":"","say_until":0.,"pet_cd":0.,"brush_cd":0.,"remind":{},"confirm":0.,"px":float(r+F//2-N//2),"py":float(aw+10),"tx":0.,"ty":0.,"hover_until":0.,"eat_food":None,"eat_x":0,"play_toy":None,"toy":[0.,0.,0.,0.],"music_at":0.,"away_until":0.,"dizzy_until":0.,"shop_min":bp(aK["shop"]),"shop_cat":0,"shop_page":0,"pen_open":False,"pen_min":bp(aK["pen"]),"guests":[],"pals":{},"quest_min":bp(aK["quest"]),"ach_min":bp(aK["ach"]),"ach_saved":None,"hallow_night":False,"season_saved":None,"season_told":set(),"hallow_told":None,"snow":[],"shared_at":0.,"social_at":0.,"anims":{},"snd_later":[],"parts":{"main":[],"pen":[]},"sprites":{"main":[],"pen":[]},"bar_w":{},"carry":None,"shop_dirty":False,"quest_dirty":False};cF={"g":None,"c":{},"store":({},{}),"v":None};h0,aa,q=Kit.basics(i,ae)
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
			if self._chg(ctrl,"vis",on):cj(ctrl,"IsVisible",on)
		def look(self,ctrl,gfx,hue):
			if self._chg(ctrl,"gfx",gfx):cj(ctrl,"Graphic",gfx)
			if self._chg(ctrl,"hue",hue):cj(ctrl,"Hue",hue)
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
	def cG(s,a=dk):s="".join(b for b in str(s or "")if 32<=ord(b)<127 and b not in ";=|,").strip();return s[:a]or dT["name"]
	def bx(v):return[a.split(":",1)for a in v.split(",")if ":"in a]
	def dU():Kit.kv_load(c5,";",J,aX,("name",));J["name"]=cG(J["name"])
	def bY():Kit.kv_save(c5,";",J,dT,aX,("name",))
	def bZ(on):J["comp"]=bool(on);bY();bN(aq)
	def f1():
		a=a6(dm)
		if "="not in a:return False
		j.update(bc)
		for k,v in bo(a).items():
			if k not in bc:continue
			d=bc[k]
			try:
				if isinstance(d,bool):j[k]=v=="1"
				elif isinstance(d,int):j[k]=int(float(v))
				else:j[k]=float(v)
			except ValueError:pass
		if not j["uid"]:j["uid"]=random.randint(1,65535)
		return True
	def aY(final=False):
		a=time.time();j["last"]=a
		if j["away"]:
			b=max(0.,i["away_until"]-a)
			if j["away_total"]>0 and b>j["away_total"]:b=j["away_total"];i["away_until"]=a+b
			j["away_left"]=b
		a7(dm,";".join("%s=%s"%(c,("1"if j[c]else "0")if isinstance(e,bool)else "%d"%int(j[c])if isinstance(e,int)else "%.2f"%float(j[c]))for c,e in bc.items()))
		if final or i["shop_dirty"]or a-l["last"]>=fI:b_()
		if final or i["quest_dirty"]:f8()
		i["saved_at"]=a
	def f2():
		l.update({"sq":0.,"own":set(),"cnt":{},"eq":{},"last":0.})
		for k,v in bo(a6(dn)).items():
			try:
				if k=="sq":l["sq"]=max(0.,float(v))
				elif k=="last":l["last"]=float(v)
				elif k=="own":l["own"]=set(a for a in v.split(",")if a in ac)
				elif k=="cnt":
					for i,n in bx(v):
						if i in ac and int(n)>0:l["cnt"][i]=int(n)
				elif k=="eq":
					for s,i in bx(v):
						if s in f0 and(i in ac or i==""):l["eq"][s]=i
			except ValueError:pass
		l["own"]|=dM
		for s in cE:
			if not l["eq"].get(s):l["eq"][s]=by(s)
		f3()
	def f3():
		c=a6(dq);i["season_saved"]=c
		for k,v in bo(c).items():
			if k=="own":l["own"]|=set(d for d in v.split(",")if d in bV and not aF(ac[d]))
			for a,b in bx(v):
				if k=="cnt"and a in bV and aF(ac[a]):
					if safe(lambda:int(b),0)>0:l["cnt"][a]=int(b)
				elif k=="eq"and b in bV and a1.get(ac[b]["cat"])==a and(l["eq"].get(a)or "")==by(a):l["eq"][a]=b
	def b_():
		l["last"]=time.time();i["shop_dirty"]=False;S=bV;f=["%s:%s"%(g,by(g)if h in S else h)for g,h in sorted(l["eq"].items())];b=["%s:%s"%(p,k)for p,k in sorted(l["eq"].items())if k in S];c=sorted((t,s)for t,s in l["cnt"].items()if s>0);a7(dn,";".join(["sq=%.2f"%l["sq"],"last=%.0f"%l["last"],"own="+",".join(sorted(v for v in l["own"]-dM if v not in S)),"cnt="+",".join("%s:%d"%(w,x)for w,x in c if w not in S),"eq="+",".join(f)]));d=sorted(y for y in l["own"]if y in S);e=["%s:%d"%(z,G)for z,G in c if z in S];a=";".join(["own="+",".join(d),"cnt="+",".join(e),"eq="+",".join(b)])if d or e or b else ""
		if a!=i["season_saved"]:i["season_saved"]=a;a7(dq,a)
		f5()
	def f4():
		a=a6(dr);i["ach_saved"]=a;Y.update({"got":set(),"earned":0.,"swats":0,"new":"="not in a})
		for k,v in bo(a).items():
			try:
				if k=="got":Y["got"]=set(sorted(d for d in v.split(",")if d)[:f_])
				elif k=="earned":Y["earned"]=max(0.,float(v))
				elif k=="swats":Y["swats"]=max(0,int(float(v)))
			except ValueError:pass
		b=1.-U["hon_price"]*H("hon");c=l["sq"]+sum(int(round(e["price"]*b))for e in aE if e["price"]and not aF(e)and e["id"]in l["own"]);Y["earned"]=max(Y["earned"],c)
	def f5():
		a="got=%s;earned=%.2f;swats=%d"%(",".join(sorted(Y["got"])),Y["earned"],Y["swats"])
		if a!=i["ach_saved"]:i["ach_saved"]=a;a7(dr,a)
	def f6():
		i["guests"]=[]
		for a in a6(do).split(","):
			g=cO(a.strip())
			if g is not None and len(i["guests"])<aJ-1:i["guests"].append(g)
	def cH():a7(do,",".join(a["code"]for a in i["guests"]))
	def f7():
		A.update({"xp":dict((c,0.)for c in aV),"relics":{},"visits":{},"hunts":0,"med":0,"tab":0})
		for k,v in bo(a6(dp)).items():
			try:
				if k=="xp":
					for a,n in bx(v):
						if a in A["xp"]:A["xp"][a]=max(0.,min(float(n),bz(ar)))
				elif k in("relics","visits"):
					b=bW if k=="relics"else fX
					for i,n in bx(v):
						if i in b and int(n)>0:A[k][i]=int(n)
				elif k in("hunts","med"):A[k]=max(0,int(float(v)))
				elif k=="tab":A["tab"]=max(0,min(len(dS)-1,int(v)))
			except ValueError:pass
	def f8():i["quest_dirty"]=False;a7(dp,";".join(["xp="+",".join("%s:%.1f"%(a,A["xp"][a])for a in aV),"relics="+",".join("%s:%d"%b for b in sorted(A["relics"].items())),"visits="+",".join("%s:%d"%c for c in sorted(A["visits"].items())),"hunts=%d"%A["hunts"],"med=%d"%A["med"],"tab=%d"%A["tab"]]))
	def cI(a):Kit.save_pos(ds[a],ad[a]["g"])
	def cJ():return HOST.me()
	def dV(ser):return HOST.mobile(ser)
	def m():return J["name"]
	def S(idx):
		if J["sounds"]and idx:API.PlaySound(idx)
	def f9(t):
		q=i["snd_later"]
		if q:
			for e in q:
				if e[0]<=t:break
			else:return
			i["snd_later"]=[c for c in q if c[0]>t]
			for a,b in q:
				if a<=t:S(b)
	def aZ():S(ac[l["eq"]["voice"]].get("snd",422))
	def B(text,secs=3.):i["say"],i["say_until"]=text,time.time()+secs
	def V(v,lo=0.,hi=100.):return max(lo,min(hi,v))
	def dW(x,y,tx,ty,step):
		b,c=tx-x,ty-y;a=math.hypot(b,c)
		if a<=step or a<.01:return tx,ty
		return x+b/a*step,y+c/a*step
	def K(k,n):j[k]=V(j[k]+n)
	def eq(slot):return ac.get(l["eq"].get(slot)or "")
	def by(slot):return bu[slot][0]["id"]if slot in cE else ""
	def aF(it):return it["cat"]=="treat"or it.get("uses")
	def af(a):return a in l["own"]
	def am(k,default):return eq("pers").get(k,default)
	def bd():return dd if af("u_pantry")else fA
	def bz(level):return 50.*level*(level+1)
	dX={}
	def H(key):
		b=A["xp"].get(key,0.);c=dX.get(key)
		if c is not None and c[0]==b:return c[1]
		a=0
		while a<ar and b>=bz(a+1):a+=1
		dX[key]=(b,a);return a
	def cK(key):
		a=H(key)
		if a>=ar:return 0.,0.
		b=bz(a);return A["xp"].get(key,0.)-b,bz(a+1)-b
	def cL(key,a):v=dQ[key];n=a//-v[4]if v[4]<0 else a*v[4];return v[3]%n if "%d"in v[3]else v[3]
	def b0(level):return all(H(a)>=level for a in aV)
	def cM():return fE*len(A["relics"])
	def dY(req):
		if req is None:return
		if req[0]=="stage":
			if j["stage"]<req[1]:return "needs a grown mongotchi"if req[1]==1 else "needs a Greater Mongotchi"
		elif req[0]=="virtue":
			if H(req[1])<req[2]:return "needs %s at level %d"%(dQ[req[1]][1],req[2])
		return
	def bA(it):return int(round(it["price"]*(1.-U["hon_price"]*H("hon"))))
	def dZ():
		k=j["away_kind"]
		if k==1:return "treasure hunting at %s"%ay[min(j["away_loc"],len(ay)-1)]["name"]
		if k==2:return "meditating at the Shrine of %s"%av[min(j["away_virt"],len(av)-1)][1]
		return "foraging"
	def d_():return{1:"out hunting",2:"meditating"}.get(j["away_kind"],"out foraging")
	def T(kind,n=None):
		n=br.get(kind,0)if n is None else n
		if n<=0:return 0
		a=am("squeak",1.)*(fO if af("u_luck")else 1.);a*=1.+U["hnr_squeaks"]*H("hnr")+cM();l["sq"]+=n*a;Y["earned"]+=n*a
		if kind!="passive":
			i["shop_dirty"]=True
			if kind!="social"and n*a>=1:bl("+%d"%int(round(n*a)),ab,12,-26.,1.4)
		return n*a
	def be():return V(.45*j["joy"]+.3*j["food"]+.15*j["clean"]+.1*j["energy"]-(15 if j["sick"]else 0))
	def d0():
		m=be()
		for a,b in fU:
			if m>=a:return b,(D if m>=55 else E if m<35 else ag)
	def hm(secs):secs=max(0,int(secs));return "%dh %02dm"%(secs//3600,(secs%3600)//60)if secs>=3600 else "%dm"%(secs//60)
	R=Kit.fit
	def d1(nm,a):t=ac.get(a or "");return nm+(" "+t["name"]if t else "")
	def cN():j.update(bc);j["uid"]=random.randint(1,65535);j["last"]=time.time();i.update({"grem":None,"eat_until":0.,"play_until":0.,"cure_until":0.,"brush_until":0.,"leave_until":0.,"away_until":0.,"say":"","remind":{},"px":float(r+F//2-N//2),"py":float(aw+10),"hover_until":0.,"dizzy_until":0.});aY();O("arrive",1.2);aO(bG,r+F/2.,aw+30,1.2,0,64);q("a pup has adopted you: meet %s (rename it on the settings page)."%m(),D)
	bB="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";d2=dict((iy,ix)for ix,iy in enumerate(bB));d3=re.compile(r"(?<![A-Za-z0-9_\-])([A-Za-z0-9_\-]{64})(?![A-Za-z0-9_\-])")
	def ga(data):
		a=[]
		for i in range(0,len(data),3):n=(data[i]<<16)|(data[i+1]<<8)|data[i+2];a+=[bB[(n>>18)&63],bB[(n>>12)&63],bB[(n>>6)&63],bB[n&63]]
		return "".join(a)
	def gb(s):
		a=[]
		for i in range(0,len(s),4):
			n=0
			for b in s[i:i+4]:n=(n<<6)|d2[b]
			a+=[(n>>16)&255,(n>>8)&255,n&255]
		return a
	def d4(data):
		s=7
		for i,b in enumerate(data):s=(s*31+b+i)&65535
		return s
	def gc(slot,a):b=[c["id"]for c in bu.get(slot,[])];return b.index(a)+1 if a in b else 0
	def gd(slot,n):a=bu.get(slot,[]);return a[n-1]["id"]if 1<=n<=len(a)else by(slot)
	def d5(s,n):b=[ord(a)if 32<=ord(a)<127 else 63 for a in s[:n]];return b+[0]*(n-len(b))
	def d6(b):return "".join(chr(a)for a in b if 32<=a<127).strip()
	bf={"at":-99.,"name":"Someone","raw":None}
	def b1():
		t=time.time()
		if t-bf["at"]>=2.:
			bf["at"]=t;a=safe(lambda:cJ().Name,"")or "Someone"
			if a!=bf["raw"]:bf["raw"]=a;bf["name"]=cG(a,16)
		return bf["name"]
	def ge():a=[1,j["stage"]]+[gc(b,l["eq"].get(b,""))for b in dP];a+=[int(be()),min(255,int(j["age"]//3600)),min(255,j["swats"]),(j["uid"]>>8)&255,j["uid"]&255]+d5(m(),12)+d5(b1(),16);c=d4(a);return ga(a+[(c>>8)&255,c&255])
	def cO(code):
		if not code or len(code)!=64 or any(a not in d2 for a in code):return
		d=gb(code)
		if len(d)!=48 or d[0]!=1 or d4(d[:46])!=(d[46]<<8|d[47]):return
		g={"code":code,"stage":min(2,d[1]),"mood":d[13],"age":d[14],"swats":d[15],"uid":d[16]<<8|d[17],"name":d6(d[18:30])or "Mongotchi","owner":d6(d[30:46])or "Someone"}
		for n,k in enumerate(dP):g[k]=gd(k,d[2+n])
		return g
	def d7(a,events):
		if j["feral"]:return
		p=J["pace"]/100.;h=a/3600.*p;e,b=j["asleep"],j["sick"];c=eq("pers");g=.5 if(j["away"]and j["away_kind"]==2)else 1.;d=U;j["food"]-=fi*h*(.5 if e else 1.)*(1.25 if b else 1.)*c.get("food_rate",1.)*(1.-d["hum_hunger"]*H("hum"))*g;i=0. if e else fj*c.get("joy_rate",1.)*(1.-d["com_joy_loss"]*H("com"));i+=fk*((j["food"]<25)+(j["clean"]<30)+bool(b))*(1.-d["hum_need"]*H("hum"));j["joy"]-=i*h*g
		if e:k=eq("decor");j["energy"]+=(fm*h*c.get("sleep",1.)*(k.get("sleep",1.)if k else 1.))
		else:j["energy"]-=fl*h*(1.5 if b else 1.)*c.get("energy_rate",1.)
		j["clean"]-=(fn+fo*j["messes"])*h
		for l in("food","joy","energy","clean"):j[l]=V(j[l])
		j["age"]+=a*p;j["care_sum"]+=be()*a*p;j["care_t"]+=a*p;j["mess_in"]-=a*p
		if j["mess_in"]<=0:
			j["mess_in"]=random.uniform(fp,fq)*60.
			if j["messes"]<cr and not j["away"]:j["messes"]+=1;events.append(("mess","%s left a little heap in the pen."%m()))
		j["supply_in"]-=a*p
		if j["supply_in"]<=0:
			j["supply_in"]=de*60.
			if j["pantry"]<bd():j["pantry"]+=1;events.append(("supply","A farmer left some food at the pen (+1)."))
		if af("u_feeder")and j["food"]<20 and j["pantry"]>0 and not j["asleep"]and not j["away"]:n=random.choice(az);j["pantry"]-=1;K("food",n[2]);events.append(("feeder","the Auto-Feeder gave %s %s."%(m(),n[1])))
		if not b:
			f=((fr if j["clean"]<30 else 0.)+(fs if j["food"]<10 else 0.));f*=1.-d["spi_sick"]*H("spi")
			if f and random.random()<f*h:j["sick"],j["sick_t"]=True,0.;events.append(("sick","%s is sick: give it a Cure potion."%m()))
		else:j["sick_t"]+=a*p
		if not j["asleep"]and j["energy"]<=3 and not j["away"]:j["asleep"]=True;events.append(("sleep","%s fell asleep."%m()))
		elif j["asleep"]and j["energy"]>=100:j["asleep"]=False;events.append(("wake","%s woke up rested."%m()))
		o=(j["food"]<=0 or j["joy"]<=0 or(j["sick"]and j["sick_t"]>ft*3600))
		if o:j["neglect"]+=a*p
		else:
			j["neglect"]=max(0.,j["neglect"]-a*p*.5)
			if j["neglect"]==0:j["warned"]=False
		if j["neglect"]>=fu*3600:j["feral"],j["away"],j["asleep"]=True,False,False;events.append(("feral","%s decided it is better off without a master and flew away."%m()));return
		if j["neglect"]>=fv*3600 and not j["warned"]:j["warned"]=True;events.append(("warn","%s looks around for someone else to care for it."%m()))
		if j["stage"]==0 and j["age"]>=fw*3600:j["stage"]=1;events.append(("grow","%s has grown into a mongotchi."%m()))
		elif j["stage"]==1 and j["age"]>=fx*3600 and j["care_t"]>0 and j["care_sum"]/j["care_t"]>=fy:j["stage"]=2;events.append(("grow","%s is now a Greater Mongotchi."%m()))
	d8={"sick":E,"feral":E,"warn":E,"grow":D,"feeder":o,"sleep":o,"wake":o}
	def d9(events,live=True):
		for a,b in events:
			if a in d8 and(live or a not in("sleep","wake")):q(b,d8[a])
			if a=="grow":T("grow")
			if not live:continue
			if a=="grow":S(fc);B("*grows!*",4);O("grow",2.5);a0(bk,2.,72)
			elif a=="sick":S(cq);B("*cough cough*");O("cough",.4)
			elif a=="feral":aZ();O("farewell",2.5);i["redraw_at"]=time.time()+2.6
			elif a in("supply","feeder"):S(a8);i["carry"]={"who":"drop","gfx":random.choice(az)[0],"t0":time.time(),"x":float(r+40+random.randint(0,60)),"y":float(C+20)}
			elif a=="mess":O("mess%d"%max(0,j["messes"]-1),.5)
			elif a=="sleep":O("yawn",1.4)
			elif a=="wake":O("stretch",.5)
	def gf():
		c=time.time()
		if l["last"]:
			a=min(max(0.,c-l["last"]),cu*3600);d=T("passive",cv*a/3600.)
			if d>=1:q("%d squeaks earned while you were away."%int(d),D)
		l["last"]=c;a=max(0.,c-j["last"])if j["last"]else 0.
		if j["away"]:
			b=j["away_left"]
			if j["away_total"]>0:b=min(b,j["away_total"])
			j["away_left"]=max(0.,b-a);i["away_until"]=c+j["away_left"]
			if j["away_left"]<=0:i["away_until"]=c;cQ(quiet=True)
		if not J["offline"]or a<60 or j["feral"]:return
		a=min(a,cu*3600);e=[];b=a
		while b>0 and not j["feral"]:f=min(60.,b);d7(f,e);b-=f
		q("while away (%s): fullness %d, happiness %d, %s, pantry %d."%(hm(a),j["food"],j["joy"],a5(j["messes"],"heap"),j["pantry"]),o);d9([g for g in e if g[0]in("sick","grow","warn","feral")],live=False)
	def aB(what):
		if j["feral"]:q("%s has gone wild: adopt a new pup in the pen."%m(),o);return False
		if j["away"]:q("%s is out %s."%(m(),dZ()),o);return False
		if j["asleep"]and what not in("lights","clean"):B("z Z z");q("%s is asleep (Lights wakes it)."%m(),o);return False
		return True
	def a_():return not j["asleep"]and not j["away"]
	def aG():t=time.time();return t<i["eat_until"]or t<i["play_until"]or t<i["leave_until"]
	def gg(action,t):
		if not aB("feed")or aG():return
		if j["pantry"]<=0:B("*eyes the empty pantry*");q("the pantry is empty: Forage, or wait for the farmer.",E);return
		if j["food"]>=95:B("*turns its nose up*");return
		j["pantry"]-=1;ea(random.choice(az),t)
	def ea(food,t):i.pop("eat_t0",None);i["eat_bites"]=1.;i["eat_food"]=food;i["eat_x"]=random.randint(r+70,r+F-60);i["eat_until"]=t+dh
	def gh():c,a,b=i["eat_food"];i["eat_food"]=None;K("food",b);K("joy",am("feed_joy",5));j["fed"]+=1;T("feed");S(da);B("*munches %s*"%a.split(" ",1)[1]if " "in a else "*munch*")
	def gi(it,t):
		if not aB("treat")or aG()or l["cnt"].get(it["id"],0)<=0:return False
		l["cnt"][it["id"]]-=1;i["shop_dirty"]=True
		for k in("food","joy","energy","clean"):
			if it.get(k):K(k,it[k])
		if it.get("cure")and j["sick"]:j["sick"],j["sick_t"]=False,0.
		if it.get("guard"):j["guard"]=True
		if it.get("dizzy"):i["dizzy_until"]=t+30.
		T("treat");S(da)
		if it.get("spooky"):O("spooky",1.6)
		if it.get("energy",0)>=20:O("zoom",4.)
		if it.get("guard"):bl("!",E,0,-30.)
		if it.get("cure"):a0(eB,1.2)
		if it.get("sleep"):O("yawn",1.4)
		ea((it["gfx"],it["name"],0),t);B("*spooky squeak!* BOO!"if it.get("spooky")else "*gobbles the %s*"%it["name"].lower(),3.5)
		if it.get("sleep"):i["sleep_after"]=t+dh+.5
		q("you give %s a %s."%(m(),it["name"].lower()),D)
		if it.get("season")and bC(it):ei("festive")
		return True
	def gj(action,t):
		if not aB("play")or aG():return
		if j["sick"]:B("*cough*");q("%s is too sick to play."%m(),o);return
		if j["energy"]<15:B("*yawns*");q("%s is too tired to play."%m(),o);return
		a=eq("toy");i["play_toy"]=a;i["play_until"]=t+fJ;i["toy"]=[float(r+20),float(aA-40),random.uniform(70,110),-60.];i["music_at"]=0.
		if a.get("motion")=="music":i["toy"]=[float(r+F//2-22),float(aA),0.,0.];B("*dances*")
		else:B("*pounces!*")
	def gk():
		a=i["play_toy"]or eq("toy");b=random.randint(10,45)if a.get("motion")=="dice"else 25+a.get("joy",0);K("joy",b*am("play",1.));j["energy"]=V(j["energy"]-10+a.get("energy",0));K("food",-5);T("play")
		if a.get("squeaks"):T("toy",a["squeaks"])
		aZ();B(random.choice(ax["happy"]))
	def gl(action,t):
		if not aB("brush")or aG():return
		if t<i["brush_cd"]:B("*already shiny*");return
		k=2 if af("u_groom")else 1;i["brush_cd"]=t+fL/k;K("joy",10*k);K("clean",10*k);i["brush_until"]=t+1.8;T("brush",br["brush"]*k);S(db);B("*purrs... er, squeaks*")
	def gm(action,t):
		if not aB("clean"):return
		if j["messes"]==0 and j["clean"]>=95:B("*already spotless*");return
		if j["messes"]or j["clean"]<80:T("clean")
		i["mess_was"]=j["messes"];O("clean",.7)
		for a in range(j["messes"]):aO(bG,r+84+a*44+22,C+Q-20,.9,0,48)
		if not j["asleep"]:O("shake",.6);B("*shakes its wings*")
		j["messes"],j["clean"]=0,100.;S(db)
	def gn(action,t):
		if not aB("lights"):return
		if j["asleep"]:
			j["asleep"]=False;O("stretch",.5)
			if j["energy"]<50:K("joy",-5);B("*grumpy squeak*")
			else:B("*stretches*")
		elif aG():return
		elif j["energy"]>=90:B("*isn't sleepy*")
		else:j["asleep"]=True;O("yawn",1.4);i["say"]=""
	def go(action,t):
		if not aB("cure"):return
		if not j["sick"]:B("*isn't sick*");return
		j["sick"],j["sick_t"]=False,0.;K("joy",-5);i["cure_until"]=t+1.5;O("flash",1.);O("shake",.8);a0(eB,1.4);T("cure");S(fb);B("*bleh!* ...*feels better*")
	def gp(action,t):
		if not aB("forage")or aG():return
		if j["sick"]or j["energy"]<20:B("*too weak*"if j["sick"]else "*too tired*");q("%s is too %s to forage."%(m(),"sick"if j["sick"]else "tired"),o);return
		if j["pantry"]>=bd():q("the pantry is full.",o);return
		K("energy",-max(U["sac_forage_min"],fD-U["sac_energy"]*H("sac")));K("food",-5);cP(t,0,random.uniform(df[0],df[1]),"*flaps off*")
	def cP(t,kind,secs,line):j["away"],j["away_kind"],j["away_total"]=True,kind,secs;i["away_until"],i["leave_until"]=t+secs,t+1.5;B(line,1.5)
	def gq(quiet=False,b=1.):
		a=(1+random.randint(0,1)+(1 if j["energy"]>50 and random.random()<.5 else 0));a+=am("forage",0)+H("sac")//U["sac_per"];a=max(0,min(a,bd()-j["pantry"]));j["pantry"]+=a
		if a and not quiet:i["carry"]={"who":"pet","gfx":random.choice(az)[0],"t0":time.time()}
		T("forage",br["forage"]*a);q("%s foraged %d food."%(m(),a),D if a else o)
		if quiet:return
		S(a8);B("*brings back %d food!*"%a if a else "*found nothing*")
	def cQ(quiet=False,a=1.):k=j["away_kind"];i["ach_due"]=True;j["away"],j["away_kind"]=False,0;i["px"],i["py"]=float(a9),float(aw+10);i["tx"],i["ty"]=float(r+F//2),float(aw+20);{1:gt,2:gv}.get(k,gq)(quiet,a)
	def eb(t):return max(0.,i["away_until"]-t)
	def ec(t):a=j["away_total"]or 1.;return V(1.-eb(t)/a,0.,1.)
	def gr(n,t):
		if n<0 or n>=len(ay):return
		a=ay[n]
		if not aB("hunt")or aG():return
		b=dY(a["req"])
		if b:q("%s can't go to %s yet: %s."%(m(),a["name"],b),E);return
		if j["sick"]or j["energy"]<25:B("*too weak*"if j["sick"]else "*too tired*");q("%s is too %s for a treasure hunt."%(m(),"sick"if j["sick"]else "tired"),o);return
		j["away_loc"]=n;K("energy",-max(U["sac_hunt_min"],fC-U["sac_energy"]*H("sac")));K("food",-10);cP(t,1,a["mins"]*60.,"*flaps off on an adventure!*");S(a8);q("%s flies to %s (about %d min)."%(m(),a["name"],a["mins"]),D);aY();i["quest_redraw"]=True
	def gs(e,f):
		a={"sq":0,"food":0,"trap":0,"treat":[],"relic":[]};g=1.+U["spi_relic"]*H("spi");c=[(n*(g if k=="relic"else 1.),k,p,s)for n,k,p,s in e["loot"]];h=sum(t[0]for t in c)
		for j in range(f):
			r=random.uniform(0,h)
			for w,b,d,i in c:
				r-=w
				if r<=0:break
			if b in("sq","food"):a[b]+=random.randint(d,i)
			elif b=="trap":a["trap"]+=1
			else:a[b].append(d)
		return a
	def gt(quiet=False,h=1.):
		c=ay[min(j["away_loc"],len(ay)-1)];r=c["danger"]*(1.-U["val_danger"]*H("val"));d=random.random()<r*h;e=random.randint(dg[0],dg[1])+H("sac")//U["sac_per"];e=int(e*h+(random.random()<(e*h)%1.))
		if d:
			e=e//2;K("energy",-25);K("joy",-10)
			if not j["sick"]and random.random()<.35:j["sick"],j["sick_t"]=True,0.
		a=gs(c,e);b=[]
		if a["sq"]:n=T("hunt",a["sq"]);b.append("%d squeaks"%int(round(n)))
		if a["food"]:s=max(0,bd()-j["pantry"]);n=min(a["food"],s);j["pantry"]+=n;b.append("%d food"%n if n else "food the full pantry couldn't hold")
		for f in a["treat"]:l["cnt"][f]=l["cnt"].get(f,0)+1;b.append(ac[f]["name"].lower()if f in ac else f)
		if a["trap"]:l["cnt"]["u_trap"]=l["cnt"].get("u_trap",0)+a["trap"];b.append(a5(a["trap"],"Gremlin Trap"))
		i["shop_dirty"]=i["quest_dirty"]=True;k=False
		for g in a["relic"]:
			if g not in A["relics"]:k=True
			A["relics"][g]=A["relics"].get(g,0)+1;b.append(bW[g][1])
		A["hunts"]+=1;A["visits"][c["id"]]=A["visits"].get(c["id"],0)+1;T("forage",2)
		if b:t=", ".join(b[:-1])+(" and "if len(b)>1 else "")+b[-1];u=", but %s."%c["bad"]if d else ".";q("%s is back from %s with %s%s"%(m(),c["name"],t,u),E if d else D)
		else:q("%s is back from %s empty-handed%s"%(m(),c["name"],": %s."%c["bad"]if d else "."),E if d else o)
		if k:
			q("new relic (Journeys > Relics): relic bonus now +%d%% squeaks."%int(round(cM()*100)),D)
			if len(A["relics"])==len(bb):q("%s has found every relic in Sosaria."%m(),D)
		aY();i["quest_redraw"]=True
		if quiet:return
		p=bW[a["relic"][0]][2]if a["relic"]else random.choice(az)[0]if b else None
		if p is not None:i["carry"]={"who":"pet","gfx":p,"t0":time.time()}
		if d:S(cq);B("*ouch...*",3.);O("cough",.4)
		else:
			S(a8);B("*brings back treasure!*"if b else "*found nothing*",3.)
			if k:a0(bk,2.,72)
	def gu(n,t):
		if n<0 or n>=len(av):return
		v=av[n]
		if not aB("meditate")or aG():return
		if j["sick"]:B("*cough*");q("%s is too sick to meditate."%m(),o);return
		if H(v[0])>=ar:q("%s has mastered %s already."%(m(),v[1]),o);return
		j["away_virt"]=n;K("food",-5);cP(t,2,ct*60.,"*flaps off serenely*");q("%s flies to meditate at the Shrine of %s (%s, about %d min)."%(m(),v[1],v[2],int(ct)),D);aY();i["quest_redraw"]=True
	def gv(quiet=False,c=1.):
		v=av[min(j["away_virt"],len(av)-1)];k=v[0];d=H(k);b=fB*(1.+U["spi_meditate"]*H("spi"))*(.7+.6*be()/100.)*(.8,1.,1.25)[j["stage"]]*c;b=max(0.,b);A["xp"][k]=min(bz(ar),A["xp"].get(k,0.)+b);A["med"]+=1;i["quest_dirty"]=True;K("joy",10*c);K("energy",10*c);T("meditate",3);a=H(k);f,g=cK(k);h="level %d, %d/%d"%(a,int(f),int(g))if a<ar else "level %d, mastered"%a;q("%s meditated on %s: +%d experience (%s)."%(m(),v[1],int(round(b)),h),D)
		if a>d:
			e=cL(k,a);q("%s's %s has risen to level %d: %s."%(m(),v[1],a,e[:1].lower()+e[1:]),D)
			if b0(5)and not i.get("vall_told_5"):i["vall_told_5"]=True;q("all eight virtues at level 5: the Avatar title is for sale (Shop > Titles).",D)
			if b0(ar):q("%s embodies all eight virtues: an Avatar among mongotchis."%m(),D)
		aY();i["quest_redraw"]=True
		if quiet:return
		if a>d:S(fY);O("grow",2.);a0(bk,2.,72)
		else:S(a8);a0(bG,1.4,64)
		B("*feels enlightened*"if a>d else "*feels calm*",3.)
	def gw(t):
		if not j["away"]:return
		a=ec(t);i["away_until"]=t
		if j["away_kind"]==0:return
		q("%s called home (%d%% of the trip done)."%(m(),int(a*100)),o);cQ(False,a)
	def gx(action,t):
		if j["feral"]or j["away"]:return
		if j["asleep"]:B("*snore*");return
		if t<i["pet_cd"]:B(random.choice(ax["happy"]));O("hop",.6);return
		i["pet_cd"]=t+fK;O("hop",.6);bl("<3",c9,-10,-22.);bl("<3",e9,8,-18.);K("joy",am("pet",4)+U["com_pet"]*H("com"));T("pet");aZ()
		if eq("pers")["id"]=="p_grumpy"and random.random()<.3:B("*nibbles your finger*")
		elif random.random()<.3 and b2(5)is not None:B(random.choice(dR[b2(5)]))
		else:B(random.choice(ax["happy"]))
	def ed():return di/dw if i["hallow_night"]else di
	def gy(t,e,full):
		a=i["grem"]
		if a is None:
			if not(J["gremlins"]and not j["feral"]and j["pantry"]>=2 and t>=i["next_grem_ok"]):return
			f=J["grem_min"]*60.*(2. if af("u_ward")else 1.)
			if i["hallow_night"]:f/=dw
			if random.random()<e/f:
				if i["hallow_night"]:
					d=time.localtime(t);g=(d[0],d[1],d[2])
					if i["hallow_told"]!=g:i["hallow_told"]=g;q("it's Halloween night: the gremlins are out in force.",E)
				p=a_()and not j["sick"]and j["energy"]>20;h=p and(j["guard"]or random.random()<am("guard",fN)+U["val_guard"]*H("val"))
				if h:j["guard"]=False
				i["grem"]={"phase":"walk","x":float(aM),"t0":t,"walk":fM*(1. if full else 1.5),"guard_at":t+1.5 if h else 0.}
				if a_():bl("!",E,0,-30.,1.2)
				if not full:q("a gremlin is sneaking into the pen.",E)
			return
		if a["phase"]=="walk":
			k=(t-a["t0"])/a["walk"];a["x"]=aM+(fT-aM)*min(1.,k)
			if a["guard_at"]and t>=a["guard_at"]:
				if j["asleep"]or j["away"]or j["feral"]:a["guard_at"]=0.
				elif t>=a["guard_at"]+1.2:a["phase"]="flee";O("gswat",.5);K("joy",5);T("guard",br["guard"]*(1.+U["jus_squeaks"]*H("jus")));S(dc);B("*chases it off!*");q("%s chased the gremlin away."%m(),D);return
			if k>=1.:
				a["phase"]="flee"
				if l["cnt"].get("u_trap",0)>0:l["cnt"]["u_trap"]-=1;i["shop_dirty"]=True;a["phase"],a["trap_t"]="trapped",t;O("gtrap",.9);aO(bk,a["x"]+au/2.,aD+30,.9,0,56);ao("SNAP!",E,a["x"]+au/2.,aD+10,0.,-20.,1.2);s=T("trap");S(fh);q("your Gremlin Trap caught the gremlin (+%d squeaks)."%int(round(s)),D);ei("trap");return
				n=j["pantry"];j["pantry"]//=2;b=n-j["pantry"];j["stolen"]+=b;S(fd)
				if a_():B("*SQUEAK!*")
				q("a gremlin stole %d of %d food."%(b,n),E)
				if b:i["carry"]={"who":"grem","gfx":random.choice(az)[0]};ao("-%d"%b,E,r+30,C+Q-40,0.,-18.,1.6)
				if b and a_()and random.random()<am("stealback",0.):c=(b+1)//2;j["pantry"]=min(bd(),j["pantry"]+c);B("*steals %d back!*"%c);q("but %s stole %d back."%(m(),c),D)
				elif b and a_()and H("jus"):
					c=int(b*U["jus_back"]*H("jus")+random.random())
					if c:j["pantry"]=min(bd(),j["pantry"]+c);B("*demands %d back!*"%c);q("but %s won %d back (Justice)."%(m(),c),D)
		elif a["phase"]=="trapped":
			if t-a["trap_t"]>=.9:i["grem"]=None;i["next_grem_ok"]=t+ed()
		else:
			a["x"]+=160.*e
			if a["x"]>=aM+4 or not full:
				i["grem"]=None;i["next_grem_ok"]=t+ed();o=i.get("carry")
				if o is not None and o["who"]=="grem":i["carry"]=None
	def gz(action,t):
		a=i["grem"]
		if a is None or a["phase"]!="walk":return
		a["phase"]="flee";O("gswat",.5);ao("*SWAT*",D,a["x"]+au/2.,aD+4,0.,-20.,1.);j["swats"]+=1;Y["swats"]+=1;K("joy",5);T("swat",br["swat"]*(1.+U["jus_squeaks"]*H("jus")));S(fe);i["snd_later"].append((time.time()+ff,dc))
		if a_():B("*cheers*")
		q("gremlin swatted: the food is safe.",D)
	gA={"sick":"%s is sick.","hungry":"%s is hungry.","dirty":"%s's pen needs cleaning.","bored":"%s is unhappy: play with it."};gB={"grem":"a gremlin in the pen","sick":"sick","hungry":"hungry","dirty":"pen needs cleaning","bored":"unhappy"}
	def cR():
		a=[]
		if i["grem"]is not None and i["grem"]["phase"]=="walk":a.append("grem")
		if j["sick"]:a.append("sick")
		if j["food"]<25:a.append("hungry")
		if j["messes"]>=2 or j["clean"]<30:a.append("dirty")
		if j["joy"]<25:a.append("bored")
		return a
	def gC(t):
		if not J["remind"]or j["feral"]:return
		for k in cR():
			if k=="grem":continue
			if t-i["remind"].get(k,-1e9)>=dj:i["remind"][k]=t;q(gA[k]%m(),E)
	def b2(d):
		a,b=None,d-1
		for k in aV:
			c=H(k)
			if c>b:a,b=k,c
		return a
	def gD(t):
		if t<i["next_chat"]:return
		i["next_chat"]=t+random.uniform(25,60)/max(.2,am("chat",1.))
		if j["feral"]or j["away"]or j["asleep"]or aG()or t<i["say_until"]:return
		if j["sick"]:a=ax["sick"]
		elif j["food"]<30:a=ax["hungry"]
		elif j["clean"]<35:a=ax["dirty"]
		elif j["joy"]<35:a=ax["bored"]
		else:
			a=ax["idle"]+am("lines",[])*2;b=b2(5)
			if b is not None:a=a+dR[b]*2
		B(random.choice(a))
		if random.random()<.3:
			if j["sick"]:S(cq)
			else:aZ()
	gE=("January","February","March","April","May","June","July","August","September","October","November","December");gF={"halloween":"costumes and pumpkin treats are","winter":"warm hats, a snowman and gingerbread are","newyear":"a party cap, sparkling cider and fireworks are"}
	def gG(t):
		d=time.localtime(t);a=(d[1],d[2]);e=[]
		for f,g,b,c in cz:
			if(b<=a<=c)if b<=c else(a>=b or a<=c):e.append(f)
		return frozenset(e)
	def ee(t,force=False):
		if not force and i["season_at"]-dz<=t<i["season_at"]:return
		i["season_at"]=t+dz;b=gG(t);d=time.localtime(t);i["hallow_night"]=(d[1],d[2])==fQ
		if b==i["seasons"]:return
		e,i["seasons"]=i["seasons"],b
		for a,f,h,c in cz:
			if a in b and a not in i["season_told"]:i["season_told"].add(a);g=("the end of February"if c==(2,29)else "%s %d"%(gE[c[0]-1],c[1]));q("%s: %s in the Shop (Seasonal tab) until %s."%("it's "+f if a!="winter"else "winter is here",gF.get(a,"its treats and clothes are"),g),D)
		if i["shop_cat"]>=len(b3()):i["shop_cat"],i["shop_page"]=0,0
		if e is not None:i["redraw"]=i["shop_redraw"]=True
	ef={"stage":lambda:j["stage"],"age":lambda:j["age"]/3600.,"swats":lambda:Y["swats"],"earned":lambda:Y["earned"],"relics":lambda:len(A["relics"]),"places":lambda:len(A["visits"]),"shrines":lambda:sum(1 for a in aV if A["xp"].get(a,0.)>0),"virtue5":lambda:sum(1 for a in aV if H(a)>=5),"guests":lambda:len(i["guests"]),"charm":lambda:1 if af("u_companion")else 0}
	def eg(t):
		i["ach_at"],i["ach_due"]=t+dC,False
		if j["swats"]>Y["swats"]:Y["swats"]=j["swats"]
		a=[c for c in aW if c[6]is not None and c[0]not in Y["got"]and ef[c[6]]()>=c[7]];b,Y["new"]=Y["new"],False
		if a:eh(a,b)
	def eh(c,before=False):
		b=0
		for a in c:
			Y["got"].add(a[0]);b+=a[3]
			if not before:q("achievement earned: %s (%s), +%d squeaks."%(a[1],a[2][0].lower()+a[2][1:],a[3]),D)
		l["sq"]+=b;Y["earned"]+=b
		if before:q("%s already earned: %s, +%d squeaks."%(a5(len(c),"achievement"),", ".join(d[1]for d in c),b),D)
		else:S(fR);bl("+%d"%b,ab,12,-26.,1.6);a0(bk,1.6,64)
		i["texts_at"]=0.;b_()
	def ei(a):
		if a not in Y["got"]:eh([fZ[a]])
	def ej(it):
		r=it.get("req")
		if r=="swats"and j["swats"]<10:return "swat %d more gremlin%s first"%(10-j["swats"],""if j["swats"]==9 else "s")
		if r=="greater"and j["stage"]<2:return "needs a Greater Mongotchi"
		if r=="elder"and j["age"]<24*3600:return "needs an age of 24 hours"
		if r=="charm"and not af("u_companion"):return "needs the Companion Charm"
		if r=="avatar"and not b0(5):return "needs every virtue at level 5"
		if r=="relics"and len(A["relics"])<8:return "find %d more kind%s of relic"%(8-len(A["relics"]),""if len(A["relics"])==7 else "s")
		if r=="pilgrim"and b2(ar)is None:return "meditate a virtue up to level %d"%ar
		return
	def gH(it):
		if not aF(it)and af(it["id"]):return
		c=ej(it);d=it["name"]if it["cat"]!="title"else "the title \"%s\""%it["name"]
		if c:q("you can't buy %s yet: %s."%(d,c),E);return
		a=bA(it)
		if l["sq"]<a:q("not enough squeaks for %s (%d more needed)."%(d,a-int(l["sq"])),E);return
		l["sq"]-=a;b=a1.get(it["cat"])
		if aF(it):l["cnt"][it["id"]]=l["cnt"].get(it["id"],0)+1
		else:
			l["own"].add(it["id"])
			if it.get("toggle"):bZ(True);q("%s can now follow you in the world. Say \"%s stay\", \"%s follow\", \"%s dance\", \"%s fetch\" or \"%s go home\"."%((m(),)*6),D)
			if b:l["eq"][b]=it["id"]
		S(fg)
		if b or it.get("toggle"):el()
		q("bought %s for %d squeaks."%(it["name"],a),D);b_()
	def ek(it,on):
		a=a1.get(it["cat"])
		if not a:return
		l["eq"][a]=it["id"]if on else by(a)
		if a=="voice"and on:aZ()
		el();b_()
	def a0(seq,dur,size=56):x,y=bH();aO(seq,x,y+20,dur,0,size)
	def el():
		x,y=bH();aO(hk,x,y+20,.8,0,60)
		for a in(-14,0,14):ao("*",bq,x+a,y+16,a*.8,-16.,.8)
	a1=dict((iz,iA)for iz,iB,iA in cD)
	def em(it):
		b=it["id"];c=bC(it)
		if it["cat"]=="treat":return([("buy","Buy","buy")]if c else[])+([("give","Give","give")]if l["cnt"].get(b,0)>0 else[])
		if it.get("uses")or not af(b):return[("buy","Buy","buy")]if c else[]
		if it.get("toggle"):return[("dismiss","Dismiss","dismiss")]if J["comp"]else[("summon","Summon","summon")]
		a=a1.get(it["cat"])
		if not a:return[]
		if l["eq"].get(a)==b:
			if a in cE:return[]
			return[("remove","Take off"if a in("hat","neck")else "Remove","remove")]
		return[("wear","Wear"if a in("hat","neck")else "Use","wear")]
	gI={"buy":cg,"give":cg,"wear":ap,"summon":ap,"remove":a3,"dismiss":a3};gJ={"title":"the title \"%s\"","pers":"the %s personality","dye":"the %s dye","voice":"the %s voice","ncol":"the %s name colour","aura":"the %s aura"}
	def gK(b,it):
		a=gJ.get(it["cat"],"%s")%it["name"];c=it["cat"]=="title"
		if b=="buy":return "Buy %s for %d squeaks"%(a,bA(it))if not aF(it)else "Buy one %s for %d squeaks"%(a,bA(it))
		if b=="give":return "Give %s a %s now"%(m(),a.lower())
		if b=="wear":return "Put %s on %s"%(a,m())if a1.get(it["cat"])in("hat","neck")else "Give %s %s"%(m(),a)if c else "Switch to %s"%a
		if b=="remove":return "Take %s off (you keep it)"%a if a1.get(it["cat"])in("hat","neck")else "Drop %s (you keep it)"%a if c else "Stop using %s (back to the free one)"%a
		if b=="summon":return "Let %s follow you in the world"%m()
		return "Send %s home to its pen"%m()
	def bC(it):s=it.get("season");return s is None or s in(i["seasons"]or())
	def gL(it):
		if "season"not in it or bC(it):return True
		return l["cnt"].get(it["id"],0)>0 if aF(it)else af(it["id"])
	def b3():return cD+[fW]if i["seasons"]else cD
	def en():
		a=b3();k=a[min(i["shop_cat"],len(a)-1)][0]
		if k=="season":return[b for b in dO if bC(b)]
		return[c for c in bu.get(k,[])if gL(c)]
	eo={"buy":lambda it:gH(it),"give":lambda it:gi(it,time.time()),"wear":lambda it:ek(it,True),"remove":lambda it:ek(it,False)}
	def gM(b,act):
		a=ac.get(b)
		if a is None or act not in[c[2]for c in em(a)]:return
		if act in eo:eo[act](a)
		elif act in("summon","dismiss"):bZ(act=="summon");q("%s %s."%(m(),"flutters out to join you"if J["comp"]else "flies home to its pen"),o)
		i["shop_redraw"]=True
	def ep():b=ge();a=bQ[J["share_ch"]];getattr(API,a[1])("%s %s"%(cw,b));i["shared_at"]=time.time();q("%s's code posted in %s chat."%(m(),a[0]),o)
	def er(g):
		if g is None:return False
		c=b1()
		if g["uid"]==j["uid"]and g["owner"]==c:return False
		for n,a in enumerate(i["guests"]):
			if a["uid"]==g["uid"]and a["owner"]==g["owner"]:
				if a["code"]!=g["code"]:i["guests"][n]=g;cH();i["pen_redraw"]=True
				return True
		if len(i["guests"])>=aJ-1:
			b=(g["uid"],g["owner"])
			if b not in i["full_told"]:i["full_told"][b]=True;q("%s (%s's mongotchi) wanted to play, but the playpen is full (%d): send one home with its X."%(g["name"],g["owner"],aJ),o)
			return False
		i["guests"].append(g);cH();i["pen_redraw"]=i["ach_due"]=True;q("%s, %s's mongotchi, joined your playpen."%(d1(g["name"],g["title"]),g["owner"]),D)
		if not i["pen_open"]:q("open the Playpen to watch them play.",o)
		return True
	def gN():
		if not i["jcodes_due"]:return
		i["jcodes_due"]=False;a,i["jcodes"]=i["jcodes"],[]
		for b,c in a:
			for m in d3.finditer(b):er(cO(m.group(1)))
	b4={"key":None,"look":None}
	def bD():
		e=l["eq"];b=(j["sick"],j["asleep"],j["stage"],e.get("dye",""),e.get("hat",""),e.get("neck",""),e.get("aura",""))
		if b==b4["key"]:return b4["look"]
		a=ac.get(e.get("dye",""));d=(co if j["sick"]else cp if j["asleep"]else a["hue"]if a and a["hue"]else cn if j["stage"]==2 else 0);c={"stage":j["stage"],"hue":d,"hat":e.get("hat",""),"neck":e.get("neck",""),"aura":e.get("aura","")};b4["key"],b4["look"]=b,c;return c
	def gO(g):a=ac.get(g["dye"]);b=a["hue"]if a and a["hue"]else(cn if g["stage"]==2 else 0);return{"stage":g["stage"],"hue":b,"hat":g["hat"],"neck":g["neck"],"aura":g["aura"]}
	bE={"key":None,"list":[],"keys":[],"der":[],"refs":None}
	def cS():
		e=l["eq"];b=i["guests"];c=b1();d=(j["feral"],j["uid"],c,m(),e.get("title",""),e.get("pers",""),e.get("ncol",""),e.get("toy",""),tuple([id(h)for h in b]))
		if d==bE["key"]:return bE["list"]
		f={"uid":j["uid"],"owner":c,"name":m(),"title":e.get("title",""),"pers":e.get("pers",""),"ncol":e.get("ncol",""),"toy":e.get("toy",""),"mine":True};a=(([]if j["feral"]else[f])+[dict(k,mine=False)for k in b])[:aJ];bE.update({"key":d,"list":a,"refs":list(b),"keys":[(g["uid"],g["owner"])for g in a],"der":[None]*len(a)});return a
	def gP(n,a):
		b=bE["der"];d=b[n]if n<len(b)else None
		if d is None:
			c=R(a["name"],80);e=ac.get(a["ncol"]or "");d={"nm":c,"nw":u(c),"hue":e["hue"]if e else ab,"spd":40.*ac.get(a["pers"]or "p_cheerful",{}).get("speed",1.),"look":None if a["mine"]else gO(a)}
			if n<len(b):b[n]=d
		return d
	cT=.5;es=3;gQ={0:9,1:6,2:6};gR={0:6,1:2,2:2};b5=14186;gS=14138;gT=14052;gU=("Gray","Criminal","Murderer","Enemy");gV=[("follow","follow"),("come","follow"),("stay","stay"),("speak","speak"),("dance","dance"),("trick","dance"),("kill","kill"),("attack","kill"),("good","good"),("sleep","sleep"),("nap","sleep"),("fetch","fetch"),("go home","home"),("dismiss","home")]
	def gW():return{"on":False,"x":0,"y":0,"map":None,"mode":"follow","stay":None,"last_p":None,"dir":(0,1),"still_since":time.time(),"next":0.,"aura_at":0.,"talk_at":0.,"help_at":0.,"dive":None,"hp":None,"dead":False,"hidden":False,"war":False,"casting":False,"gold":None,"target":None,"tiles":0,"need_at":0.,"chat_at":0.,"nap":False,"fetch_until":0.,"hover_at":0.,"panic_at":0.,"trick_at":0.,"bob":0,"z":0,"serial":0}
	def cU():return J["comp"]and af("u_companion")and not j["feral"]and not j["away"]
	def L(text,force=False,hue=None):
		c=i["comp"];t=time.time()
		if not J["comp_talk"]or(not force and t-c["talk_at"]<6.):return
		c["talk_at"]=t;a=eq("ncol");h=hue if hue is not None else(a["hue"]if a else ab);b=c.get("serial")
		if b:API.HeadMsg("%s: %s"%(m(),text),b,h)
	gX=.5;et=50;jr={"rd":None,"name":None,"re":None,"now":None}
	def gY():
		a=jr["now"]
		if a is None:
			try:from System import DateTime;a=lambda:float(DateTime.Now.Ticks);a()
			except Exception:a=lambda:time.time()*1e7
			jr["now"]=a
		return a()
	def gZ():
		try:
			if jr["rd"]is None:jr["rd"]=Journal.reader();return Journal.recent(Journal.MAX_BACK)
			return jr["rd"].new()
		except Exception:return[]
	def g_():
		a=m()
		if jr["name"]!=a:jr["name"]=a;jr["re"]=re.compile(r"(\b%s\b|^all )"%re.escape(a.lower()))
		return jr["re"]
	def eu(ent,secs,now,t):a=ent[-1];b=(now-a)/1e7 if a>1e12 else t-a;return b<=secs
	def g0(t):
		if t-i["read_at"]<gX:return
		i["read_at"]=t;e=cU();g=not e and af("u_companion");f=J["listen"]and t-i["listen_at"]>=dl
		if not(e or g or f):i["player"]=None;return
		i["player"]=g5()if e else g1()if g else None
		if f:i["listen_at"]=t
		h=gZ();d,c=i["jcodes"],i["jcmds"]
		if bF:
			for k in[n for n,p in bF.items()if t-p>10]:del bF[k]
		if h:
			l=g_()
			for a in h:
				b=a.text
				if cw in b:d.append((b,a.ticks or a.at))
				if l.search(a.low):
					m=(a.ticks//10000000)if a.ticks else int(a.at);k=(m,a.name,b)
					if k in bF:continue
					bF[k]=t;c.append((b,a.name,0,a.low,a.ticks or a.at))
				elif "Your skill in"in b:c.append((b,a.name,1,a.low,a.ticks or a.at))
		if d or c:
			j=gY()
			if d:i["jcodes"]=[s for s in d if eu(s,dl*3,j,t)][-et:]
			if c:i["jcmds"]=[v for v in c if eu(v,3.,j,t)][-et:]
		if f:i["jcodes_due"]=True
	def g1():
		try:P=cJ();return{"serial":int(P.Serial),"name":str(P.Name or ""),"lite":True}
		except Exception:return
	at={"notos":None,"name_ser":None,"name":"","name_at":-99.,"near_at":-99.,"near":0};g2=5.;g3=1.
	def g4(now):
		a=at["notos"]
		if a is None:a=at["notos"]=[getattr(API.Notoriety,d)for d in gU]
		if now-at["near_at"]<g3:c=at["near"];return dV(c)if c else None
		at["near_at"]=now;b=API.NearestMobile(a,8);at["near"]=int(b.Serial)if b is not None else 0;return b
	def g5():
		P=cJ()
		if P is None:return
		c=time.time()
		try:
			b=int(P.Serial);d={"serial":b,"x":int(P.X),"y":int(P.Y),"z":int(P.Z),"hidden":bool(P.IsHidden),"dead":bool(P.IsDead),"war":bool(P.InWarMode),"hits":int(P.Hits or 0),"hmax":int(P.HitsMax or 0),"target":None,"name":"","map":int(API.GetMap()),"casting":bool(P.IsCasting),"gold":int(P.Gold or 0)}
			if b!=at["name_ser"]or c-at["name_at"]>=g2:at["name"]=str(P.Name or "");at["name_ser"],at["name_at"]=b,c
			d["name"]=at["name"]
			if not d["war"]:at["near_at"]=-99.;return d
			a=None;e=int(API.LastTargetSerial or 0)
			if e and e!=b:
				a=dV(e)
				if a is not None and safe(lambda:int(a.Distance)>10,True):a=None
				if a is not None and safe(lambda:bool(a.IsDead),False):d["target"]={"serial":int(a.Serial),"dead":True,"name":""};return d
			if a is None:a=g4(c)
			if a is not None:f,g=int(a.Serial),bool(a.IsDead);d["target"]={"serial":f,"dead":g,"name":str(safe(lambda:a.Name,"")or "")or "foe"}
			return d
		except Exception:return
	def ev(dur):c=i["comp"];i["hop"].append(aH(b5,c["x"],c["y"],c["z"],0,dur))
	def bg():
		a=i["hop"]
		if not a:return
		i["hop"]=[]
		for f in a:
			try:f()
			except Exception:pass
	def aH(graphic,x,y,z,hue=0,dur=None):dur=cT+.1 if dur is None else dur;return lambda:API.CreateEffect(graphic,type=API.EffectType.FixedXYZ,hue=hue,sourceX=x,sourceY=y,sourceZ=max(-128,min(127,z)),duration=dur)
	def cV(graphic,hue,src=None,dst=None,sxyz=None,txyz=None):
		a={"type":API.EffectType.Moving,"hue":hue,"duration":0}
		if src:a["source"]=src
		if dst:a["target"]=dst
		if sxyz:a["sourceX"],a["sourceY"],a["sourceZ"]=sxyz
		if txyz:a["targetX"],a["targetY"],a["targetZ"]=txyz
		return lambda:API.CreateEffect(graphic,**a)
	def g6(cmd,t):
		c=i["comp"]
		if cmd=="home":bZ(False);L("*waves goodbye and flies home*",True);return
		if not c["on"]:
			if cmd=="follow"and af("u_companion")and not j["feral"]:bZ(True);q("%s flutters out to join you."%m(),D)
			return
		c["nap"]=False
		if cmd=="follow":c["mode"],c["stay"]="follow",None;L("*flaps after you*",True)
		elif cmd=="stay":c["mode"],c["stay"]="stay",(c["x"],c["y"]);L("*hovers in place*",True)
		elif cmd=="speak":aZ();L(random.choice(ax["idle"]+am("lines",[])),True)
		elif cmd=="dance":
			if t-c["trick_at"]<20:L("*is dizzy from the last one*",True);return
			c["trick_at"]=t;c["trick_until"]=t+2.;K("joy",2);T("pet");aZ();ev(1.5);L(random.choice(["*does a barrel roll*","*loop-de-loop!*","*spins in the air*"]),True)
		elif cmd=="kill":c["help_at"]=0.;L("*SCREEEECH!*",True,E)
		elif cmd=="good":K("joy",3);L("*preens proudly*",True)
		elif cmd=="sleep":c["nap"]=True;L("*curls up for a nap*",True)
		elif cmd=="fetch":c["fetch_until"]=t+3.;L("*zooms off*",True)
	g7=[(re.compile(r"\b%s\b"%iC),iD)for iC,iD in gV];g8=re.compile(r"your skill in (.+?) has increased");bF={}
	def g9(t,c):
		d=i["comp"]
		if not i["jcmds"]:return
		b,i["jcmds"]=i["jcmds"],[]
		if len(b)>1:b.sort(key=lambda e:e[2])
		for l,f,g,a,g in b:
			if a.startswith("your skill in")and "increased"in a:
				m=g8.search(a);h=T("skill",3)
				if d["on"]:ev(1.2);L("*cheers for your %s!* (+%d squeaks)"%(m.group(1)if m else "skill",int(h)),True)
				continue
			if f!=c:continue
			for j,k in g7:
				if j.search(a):g6(k,t);break
	ha=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)];hb={"sick":"*coughs pitifully*","hungry":"*tugs your sleeve: hungry*","dirty":"*sniffs itself... needs a bath*","bored":"*pokes you: play with me?*"}
	def hc(t):
		c=i["comp"]
		if t<c["next"]or i["read_at"]<=c.get("read_seen",-1.):return
		c["next"],c["read_seen"]=t+cT,i["read_at"];a=i.get("player")if(cU()or af("u_companion"))else None
		if a is None:c["on"]=False;return
		c["serial"]=a["serial"];g9(t,a.get("name")or str(safe(lambda:API.Player.Name,"")or ""))
		if not cU()or a.get("lite"):c["on"]=False;return
		e,f,n=a["x"],a["y"],a["z"]
		if not c["on"]or c["map"]!=a["map"]or max(abs(c["x"]-e),abs(c["y"]-f))>18:
			c.update({"on":True,"x":e,"y":f+1,"map":a["map"],"last_p":(e,f),"mode":"follow"if c["mode"]!="stay"or c["map"]!=a["map"]else c["mode"]})
			if c["mode"]=="follow":c["stay"]=None
			c["hp"],c["gold"]=a["hits"],a["gold"];L(random.choice(["*flutters onto your shoulder*","*squeaks hello*","*circles you happily*"]),True)
		b=[];v=c["last_p"]!=(e,f)
		if v:
			o,p=c["last_p"];w,x=(e>o)-(e<o),(f>p)-(f<p)
			if w or x:c["dir"]=(w,x)
			c["tiles"]+=max(abs(e-o),abs(f-p));c["last_p"]=(e,f);c["still_since"]=t
			if c["nap"]:c["nap"]=False;L("*yawns and catches up*")
		if c["mode"]=="stay"and c["stay"]:
			y,A=c["stay"]
			if max(abs(y-e),abs(A-f))>16:c["mode"],c["stay"]="follow",None;L("*got lonely and flies after you*",True)
			elif t>=c["hover_at"]:c["hover_at"]=t+random.uniform(2,4);c["x"],c["y"]=y+random.randint(-1,1),A+random.randint(-1,1)
		q=ha
		if t<c.get("trick_until",0.):B=int((t-c["trick_at"])/cT)*2%8;c["x"],c["y"]=e+q[B][0],f+q[B][1];b.append(aH(b5,c["x"],c["y"],n+es,0,.8))
		elif c["mode"]=="follow":
			if v:c["x"],c["y"]=e-c["dir"][0],f-c["dir"][1]
			elif t-c["still_since"]>3 and t>=c["hover_at"]:c["hover_at"]=t+random.uniform(3,6);G,I=random.choice(q);c["x"],c["y"]=e+G,f+I
		if not c["nap"]and t-c["still_since"]>120 and(j["energy"]<60 or j["asleep"]):c["nap"]=True;L("*lands and dozes off*")
		c["bob"]=1-c["bob"];c["z"]=z=n+(0 if c["nap"]or j["asleep"]else es+c["bob"])
		if a["dead"]!=c["dead"]:
			c["dead"]=a["dead"]
			if a["dead"]:K("joy",-10);L("*wails mournfully*",True,E)
			else:L("*happy flutter! You're back!*",True)
		if a["hidden"]!=c["hidden"]:
			c["hidden"]=a["hidden"]
			if a["hidden"]:L("*hides with you*",True)
		r,C=a["hits"],max(1,a["hmax"])
		if c["hp"]is not None and not a["dead"]:
			if c["hp"]-r>=C*.1:L(random.choice(["*worried squeak*","*hisses at your attacker*","*flaps anxiously*"]))
			if r<C*.3 and t-c["panic_at"]>fF-U["com_heal_secs"]*H("com"):c["panic_at"]=t;b.append(aH(gS,e,f,n,0,1.5));L("*licks your wounds* (it's the thought that counts)",True)
		c["hp"]=r
		if a["casting"]and not c["casting"]and random.random()<fG+U["spi_copy"]*H("spi"):b.append(aH(b5,c["x"],c["y"],z,0,1.));L(random.choice(["*wiggles its wings mystically*","*squeaks along: Kal Ort*","*copies your spell, badly*"]))
		c["casting"]=a["casting"]
		if c["gold"]is not None and a["gold"]>c["gold"]and random.random()<.3:L("*eyes your gold* Shiny!")
		c["gold"]=a["gold"]
		if c["tiles"]>=60:
			c["tiles"]-=60;K("joy",1);K("energy",-1);T("walk",1);M=.06*(2 if af("u_shiny")else 1)
			if random.random()<M:s=T("shiny",random.randint(5,15));b.append(aH(b5,c["x"],c["y"],z,0,1.));L("*found something shiny!* (+%d squeaks)"%int(s),True);S(a8)
		g=a["target"]
		if a["war"]!=c["war"]:c["war"]=a["war"];L("*bares its tiny fangs*"if a["war"]else "*settles down*")
		if c["target"]and(g is None or g["serial"]!=c["target"]["serial"]or g["dead"]):
			if g is not None and g["serial"]==c["target"]["serial"]and g["dead"]:T("victory",2);K("joy",2);L("*victory squeak!*",True)
			c["target"]=None
		if g is not None and not g["dead"]and a["war"]and J["comp_help"]and not a["dead"]and not j["asleep"]and c["dive"]is None:
			c["target"]=g
			if t>=c["help_at"]:
				N,O=(4,8)if af("u_war")else(8,15);c["help_at"]=t+random.uniform(N,O)*(1.-U["val_dive"]*H("val"));c["dive"]={"t":t,"serial":g["serial"],"back":False};d=bD();b.append(cV(b8(d["stage"]),d["hue"],dst=g["serial"],sxyz=(c["x"],c["y"],z)))
				if af("u_war")and random.random()<.5:b.append(cV(gT,0,dst=g["serial"],sxyz=(c["x"],c["y"],z)))
				P=random.choice(["*bonk!*","*nibble!*","*SCREECH*","*wing slap!*","*dive-bomb!*"]);b.append(lambda:API.HeadMsg(P,g["serial"],E))
		k=c["dive"]
		if k is not None:
			if not k["back"]and t-k["t"]>=.7:k["back"]=True;d=bD();b.append(cV(b8(d["stage"]),d["hue"],src=k["serial"],txyz=(c["x"],c["y"],z)))
			if t-k["t"]>=1.4:c["dive"]=None
		D=[Z for Z in cR()if Z!="grem"]
		if D and t-c["need_at"]>300:c["need_at"]=t;Q=hb.get(D[0],"*squeaks*");L(Q,True,E)
		elif t>=c["chat_at"]:
			c["chat_at"]=t+random.uniform(40,90)/max(.2,am("chat",1.))
			if not c["nap"]and not j["asleep"]:L(random.choice(ax["idle"]+am("lines",[])*2))
		F=t<c["fetch_until"]
		if c["fetch_until"]and not F:
			c["fetch_until"]=0.
			if random.random()<.25:s=T("shiny",random.randint(3,10));L("*brings you something shiny!* (+%d squeaks)"%int(s),True)
			else:L(random.choice(["*brings you a stick*","*brings you a bone*","*brings back... a gremlin's sock?*"]),True)
		if a["hidden"]or F or c["dive"]is not None:i["hop"].extend(b);return
		d=bD()
		if a["dead"]:d=dict(d);d["hue"]=bq
		l,m=c["x"],c["y"];h=ac.get(d["aura"]or "")
		if h:
			if h.get("seq"):
				if t>=c["aura_at"]:c["aura_at"]=t+1.;R=random.choice(bv)if h.get("rainbow")else h["hue"];b.append(aH(h["seq"][0],l,m,z-1,R,1.05))
			else:b.append(aH(h["gfx"],l,m,z-1,h["hue"]))
		b.append(aH(b8(d["stage"]),l,m,z,d["hue"]))
		for V,W in(("neck",gR),("hat",gQ)):
			u=ac.get(d[V]or "")
			if u:b.append(aH(u["gfx"],l,m,z+W[d["stage"]],u["hue"]))
		i["hop"].extend(b)
	def ew():i["redraw"]=True
	def hd(a,g):
		def b(*b):
			w=ad[a]
			if w["g"]is g and not i["shutting"]:
				w["g"]=None
				if a=="main":HOST.disable(aq)
				else:i[a+"_open"]=False
		return b
	def ak(g,v,graphic,x,y,w,h,hue=0,shown=True):
		p=G.CreateGumpItemPic(graphic,w,h);p.SetPos(x,y)
		if hue:p.Hue=hue
		if not shown:p.IsVisible=False
		p.SetAcceptMouseInput(False);g.Add(p);v.reg(p,gfx=graphic,hue=hue,vis=shown,pos=(int(x),int(y)),size=(int(w),int(h)));return p
	ex=[(25,0,3,3),(24,2,1,2),(21,3,1,4),(22,3,1,3),(23,3,1,2),(20,4,1,4),(18,5,4,2),(15,6,7,1),(14,7,2,2),(19,7,1,11),(12,8,4,1),(10,9,3,1),(10,10,2,1),(9,11,2,1),(7,12,1,4),(8,12,2,1),(8,13,1,1),(6,14,2,2),(4,15,16,1),(4,16,2,1),(20,16,1,2),(3,17,1,4),(4,17,1,1),(21,17,1,4),(7,18,1,1),(16,18,1,1),(2,19,2,2),(1,20,1,4),(22,20,1,4),(2,22,1,2),(3,23,1,2),(7,23,10,1),(21,23,1,2),(4,24,1,3),(19,24,1,3),(20,24,1,2),(5,25,1,2),(6,26,14,1),(6,27,1,3),(7,27,1,1),(16,27,3,1),(5,28,2,2),(17,28,2,1),(4,29,1,2),(18,29,2,1),(0,30,5,1),(19,30,6,1)]
	def he(g,v,c,x,y):
		a=G.CreateGumpColorBox(0.,"#000000");a.SetRect(int(x),int(y),au,aR);a.SetAcceptMouseInput(False);a.IsVisible=False;g.Add(a);d=[]
		for e,f,h,i in ex:b=G.CreateGumpColorBox(1.,e3);b.SetRect(e*aQ,f*aQ,h*aQ,i*aQ);a.Add(b);d.append(b)
		v.reg(a,vis=False,pos=(int(x),int(y)),size=(au,aR));c["grem_kids"],c["grem_k"]=d,1.;return a
	def cW(c,k):
		k=round(k,2)
		if c.get("grem_k")==k:return
		c["grem_k"]=k;s=aQ*k*c.get("pen_k",1.)
		for f,(a,b,g,h)in zip(c.get("grem_kids",[]),ex):
			d,e=int(round(a*s)),int(round(b*s));i,j=int(round((a+g)*s)),int(round((b+h)*s))
			try:f.SetRect(d,e,max(1,i-d),max(1,j-e))
			except Exception:pass
	def W(g,v,text,x,y,hue=None):a=P(g,text,x,y,hue);v.reg(a,text=text,thue=hue,pos=(int(x),int(y)));return a
	ey="Close"
	def bh(g,store,b,w,title,extra=None,dock=False,close_tip=ey):
		ah(g,M,M,w-2*M,30);x=w-M-84-(Kit.DOCK_DX if dock else 0);k=x-(M+30+u(title.upper())+6);l=sum(35+u(p)+6 for n,n,p,n in(extra or[]));d=l>k;h=(x-sum((30 if d else 35+u(t))+6 for s,s,t,s in(extra or[])));c=title.upper()
		if u(c)>h-6-(M+30):c=Kit.fit(c,max(8,h-6-(M+30)))
		P(g,c,M+30,M+7,ab)
		for i,m,e,j in reversed(extra or[]):x-=30 if d else 35+u(e);an(g,store,i,m,x,M+4,None if d else e,Kit.caption_tip(e,j)if d else j,on_click=aa((b,i)));x-=6
		if cm(bi(b)):
			f=bn(g,M,M,max(20,x-M-6),30,lambda*a:None,None,movable=True)
			if c!=title.upper():cl(f,title)
			return
		f=Kit.title_catcher(g,M,M,max(20,x-M-6),30,aa((b,"toggle_min")),key=aq+b)
		if c!=title.upper():cl(f,"%s. %s"%(title,Kit.DOUBLE_TIP))
		if dock:Kit.dock_button(g,store,w-M-74,M+7,on_click=aa((b,"to_bar")))
		an(g,store,"min",Kit.ART_MIN,w-M-74,M+7,None,Kit.MIN_TIP,on_click=aa((b,"toggle_min")));an(g,store,"close",a3,w-M-54,M+4,None,close_tip)
	def cX(g,store,a,title,close_tip=ey,w=None):return Kit.mini_bar(g,store,w or aC,bT,title,aq+a,aa((a,"toggle_min")),close_tip=close_tip)
	def bi(a):return aq if a=="main"else aq+"."+a
	def ez(a):
		if a=="shop":return SW,M+30+X+30+X+cZ(b3())[1]+X+8+3*38+30+M
		return{"pen":(cy,cC),"quest":(JW,JH),"ach":(dE,eY)}[a]
	def b6(a,nw,nh):
		z=cb.get(a);b,c=ez(a)
		if z is None or not cm(bi(a))or i[a+"_min"]or z[0]<b or z[1]<c:return nw,nh
		return z
	def hf(a):
		b=ad[a]
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
			if b!=cb.get(a)or(mode=="again"and b is not None):cb[a]=b;c()
		return{"title":ae+" "+cx[a],"icon":du,"state":d,"show":e,"minimize":f,"gump":lambda:b["g"],"redraw":c,"fit":g,"min":lambda:ez(a),"exact":True}
	def bj(a,build,w,h,max_h=None,hidden=False):
		b=ad[a];d=bi(a);x,y=Kit.load_pos(ds[a],fP[a],(w,h))
		if Kit.is_open(b["g"]):x,y=b["g"].GetX(),b["g"].GetY()
		c=LAYOUT.placed.get(d)if HOST.layout_holds(d)else None
		if c is not None:x,y=int(c[0]),int(c[1])
		j,b["g"]=b["g"],None;e,f,v=({},{}),{},View();g=G.CreateGump(True,True);build(g,e,f,v);i=Kit.show_window(g,x,y,w,h,d,hidden,hd(a,g),lambda:cI(a),b,{"g":g,"c":f,"store":e,"v":v},max_h)
		if c is not None and i is not None and tuple(i)!=(x,y):g.SetPos(x,y);Kit.note_rect(g,x,y);Kit.moved_by_code(g)
		if c is not None:LAYOUT.fit_now(d,g)
		ci(j)
	def b7(a,title,build,w,h):
		if not i[a+"_min"]:return bj(a,build,w,h)
		def b(g,store,c,v):c["mini"]=cX(g,store,a,title)
		bj(a,b,aC,bT)
	def eA(a):b=ad[a];cI(a);g,b["g"]=b["g"],None;ci(g);i[a+"_open"]=False
	hg={539:(7,7),2416:(17,11),2427:(12,8),2430:(16,17),2496:(14,15),2504:(12,14),2505:(18,14),2512:(7,9),2513:(9,10),2537:(23,25),2538:(9,9),2540:(13,17),2544:(13,17),2546:(18,16),2581:(13,26),2586:(13,26),2845:(21,39),3164:(17,15),3178:(16,15),3188:(10,10),3191:(24,25),3203:(42,55),3231:(60,51),3340:(15,24),3365:(36,52),3546:(37,88),3613:(14,14),3629:(13,20),3699:(10,10),3740:(33,32),3741:(16,14),3762:(22,29),3763:(22,18),3847:(9,17),3899:(22,19),3948:(37,88),3971:(9,15),4007:(12,17),4155:(17,15),4167:(21,39),4229:(11,11),4232:(9,10),4233:(10,20),4235:(20,12),4343:(19,23),4554:(38,62),4586:(36,34),4979:(16,17),5063:(15,12),5139:(17,11),5439:(15,9),5443:(11,15),5449:(20,21),5907:(19,17),5908:(17,13),5909:(12,12),5910:(21,22),5911:(20,17),5912:(18,17),5913:(12,13),5914:(17,16),5915:(16,17),5916:(23,11),5919:(15,13),5934:(30,26),7121:(8,8),7946:(10,20),8483:(21,11),8441:(19,42),9638:(51,44),9767:(38,40),10245:(24,25),10290:(15,45),10291:(24,42),11119:(14,12),11120:(12,10),4161:(21,13),11233:(14,18),11229:(10,22),8061:(7,13),5147:(18,19),5445:(21,22),5447:(22,26)};hh={0:-.1,1:.14,2:.14};hj={0:.31,1:.61,2:.61};bG=(14186,15);eB=(14138,16);hk=(14120,13);bk=(14170,16);hl=(14202,15);eC,eD=8,3
	def eE(gfx):return hg.get(gfx,(40,40))
	def b8(stage):return c6 if stage==0 else aP
	def O(kind,dur):i["anims"][kind]={"t0":time.time(),"dur":dur}
	def a2(kind,t):
		a=i["anims"].get(kind)
		if a is not None and t-a["t0"]<a["dur"]:return a,(t-a["t0"])/a["dur"]
		return None,0.
	def ao(text,hue,x,y,vx=0.,vy=-20.,dur=1.6,view="main"):
		a=i["parts"][view]
		if len(a)>=eC:a.pop(0)
		a.append({"text":text,"hue":hue,"x":float(x),"y":float(y),"vx":vx,"vy":vy,"t0":time.time(),"dur":dur,"w":Kit.text_px(text)})
	def aO(seq,x,y,dur=1.,hue=0,size=56,view="main"):
		a=i["sprites"][view]
		if len(a)>=eD:a.pop(0)
		a.append({"seq":seq,"x":float(x),"y":float(y),"t0":time.time(),"dur":dur,"hue":hue,"size":size})
	def bH():return i["px"]+N/2.,i["py"]+4
	def bI(text,hue,dx,dy,vx,vy,dur):x,y=bH();ao(text,hue,x+dx,y+dy,vx,vy,dur)
	def bl(text,hue,dx=0,vy=-20.,dur=1.6):x,y=bH();ao(text,hue,x+dx,y,random.uniform(-6,6),vy,dur)
	def eF(v,c,view,t,j,k,w,h):
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
			if d<len(a):p=a[d];o=t-p["t0"];x=V(p["x"]+p["vx"]*o+2*math.sin(o*6+d)-p["w"]/2.,j+4,j+w-4-p["w"]);y=V(p["y"]+p["vy"]*o,k+20,k+h-16);v.text(l,p["text"],p["hue"]);v.move(l,x,y);v.show(l,True)
			else:v.show(l,False)
		n=max(len(b),m[1])
		for d,g in enumerate(c["spr"]):
			if d>=n:break
			if d<len(b):s=b[d];r,q=s["seq"];u=min(q-1,int((t-s["t0"])/s["dur"]*q));e=s["size"];v.look(g,r+u,s["hue"]);v.size(g,e,e);v.move(g,V(s["x"]-e/2.,j+2,j+w-2-e),V(s["y"]-e/2.,k+2,k+h-2-e));v.show(g,True)
			else:v.show(g,False)
	def eG(g,v,a,b):
		e=[ak(g,v,bG[0]+1,a,b,56,56,shown=False)for h in range(eD)];d=[]
		for f in range(eC):c=W(g,v,"",a+8,b+24,ag);c.IsVisible=False;v.reg(c,text="",vis=False,pos=(a+8,b+24));d.append(c)
		return e,d
	def bJ(c,ctrl,gfx,d,e,k,f):
		if k>=.999:a,b=f
		else:g,h=eE(gfx);a,b=max(1,int(g*k)),max(1,int(h*k))
		c.size(ctrl,a,b);c.move(ctrl,d-a/2.,e-b/2.)
	def eH(g,v,x,y):return{"aura":ak(g,v,14144,x-10,y-8,N+20,ai+14,shown=False),"pet":ak(g,v,aP,x,y,N,ai),"neck":ak(g,v,4232,x,y+22,N,14,shown=False),"hat":ak(g,v,5912,x,y-3,N,22,shown=False)}
	def eI(t,b,phase=0.,stage=1,a=1.):
		s=abs(math.cos(t*b+phase))
		if stage==0:return{"sx":1.,"sy":.94+.06*s,"ox":0.,"oy":2.-4.*s}
		return{"sx":1.-.3*a*(1-s),"sy":1.,"ox":0.,"oy":2.5-5.*s*a}
	def eJ(t,phase=0.):return{"sx":.62,"sy":.93+.05*math.sin(t*1.7+phase),"ox":0.,"oy":0.}
	hn={"sx":1.,"sy":1.,"ox":0.,"oy":0.};ho=(("neck",hj,(N,14)),("hat",hh,(N,22)))
	def b9(v,d,c,e,g,t,a=None,shown=True):
		if not shown:
			for k in("aura","pet","neck","hat"):v.show(d[k],False)
			return
		a=a or hn;c,e=c+a.get("ox",0.),e+a.get("oy",0.);k=a.get("k",1.);j,l=a["sx"]*k,a["sy"]*k;p=g["stage"];q=b8(p);r,m=eE(q);s=a.get("hue");v.look(d["pet"],q,g["hue"]if s is None else s)
		if j>=.999 and l>=.999:n,h=N,ai;o=m
		else:n=r if j>=.999 else max(1,int(r*j));h=m if l>=.999 else max(1,int(m*l));o=h
		v.size(d["pet"],n,h);v.move(d["pet"],c-n/2.,e-h/2.);v.show(d["pet"],True);b=ac.get(g["aura"]or "")
		if b:
			if b.get("seq"):y,z=b["seq"];u=y+int(t*6)%z
			else:u=b["gfx"]
			A=bv[int(t*2.5)%len(bv)]if b.get("rainbow")else b["hue"];v.look(d["aura"],u,A);w,x=int((N+20)*min(1.,k)),int((ai+14)*min(1.,k));v.size(d["aura"],max(1,w),max(1,x));v.move(d["aura"],c-w/2.,e-x/2.)
		v.show(d["aura"],b is not None);B=e-o/2.
		for i,C,D in ho:
			f=ac.get(g[i]or "")
			if f:v.look(d[i],f["gfx"],f["hue"]);bJ(v,d[i],f["gfx"],c,B+C[p]*o,k,D)
			v.show(d[i],f is not None and k>.25)
	def eK(g,c,v):
		c["decor"]=ak(g,v,4554,r+F-50,C+Q-58,46,56,shown=False);c["hang"]=ak(g,v,2581,r+F-48,C+20,44,40,shown=False);c["pantry"]=[]
		for a in range(dG):e=az[a%len(az)][0];c["pantry"].append(ak(g,v,e,r+4+a*11,C+Q-38+(a%2)*3,44,34,shown=a<j["pantry"]))
		c["mess"]=[ak(g,v,c7,r+84+f*44,C+Q-28,44,24,shown=f<j["messes"])for f in range(cr)];b=i.get("night_a",.55 if j["asleep"]else 0.);c["night"]=ch(g,r,C,F,Q,max(0.,b),"#000010")
		if c["night"]is not None:v.reg(c["night"],vis=True,alpha=round(b,2),pos=(r,C),size=(F,Q))
		c["doll"]=eH(g,v,int(i["px"]),int(i["py"]));c["prop"]=ak(g,v,3613,r,aA,44,34,shown=False);c["grem"]=he(g,v,c,aM,aD);c["prop2"]=ak(g,v,2512,r,aA,44,34,shown=False)
		if "winter"in(i["seasons"]or()):hx(g,v,c)
		c["spr"],c["plbl"]=eG(g,v,r,C);c["say"]=W(g,v,"",r+8,C+24,ag);c["pet_hit"]=bn(g,int(i["px"]),int(i["py"]),N,ai,aa("pet"),"Pet "+m());v.reg(c["pet_hit"],vis=True,pos=(int(i["px"]),int(i["py"])),size=(N,ai));c["grem_hit"]=d=bn(g,aM,aD,au,aR,aa("swat"),"Swat it before it reaches the pantry (it takes half the food)");d.IsVisible=False;v.reg(d,vis=False,pos=(aM,aD),size=(au,aR))
	eL=.5;hp=26;bK=[("feed",ap,"Feed","Give one food from the pantry"),("play",ap,"Play","Play with its toy: happier, a bit tired"),("brush",ap,"Brush","Brush it: happier, cleaner, a few squeaks"),("clean",ap,"Clean","Tidy the pen and its heaps"),("lights",aI,"Lights","Put it to bed, or wake it up"),("cure",ap,"Cure","Give a Cure potion when it is sick"),("forage",ap,"Forage","Send it to find food (leaves the pantry unguarded)"),("shop",aI,"Shop","Spend squeaks on treats, clothes and more"),("playpen",aI,"Playpen","Open the pen for other players' mongotchis"),("journey",aI,"Journeys","Open treasure hunts and meditation"),("ach",aI,"Achievements","Open milestones that pay squeaks once")]
	def eM():return max(35+u(b)for a,a,b,a in bK)+12
	def cY():return 2*M+24-12+2*eM()
	def ca(w,h):
		b=w-2*M;Z={"w":w,"IW":b,"top":M+30+X};i=max(u(p)for s,p in bt);Z["bar_w"]=max(40,b-24-i-10-8-u("100%"));j=u("Age 99h 59m");d=u("Wonderfully Happy  (sick)")+6+j<=b-24;e=u("Squeaks 99999")+6+u("Mischievous")<=b-24;Z["pair1"],Z["pair2"]=d,e;l=(1 if d else 2)+(1 if e else 2);Z["sh"]=8+4*18+2+l*18+4;f=eM();n=max(1,min(len(bK),(b-24+12)//f));Z["ncols"],Z["col_w"]=n,f;m=(len(bK)+n-1)//n;Z["ah"]=8+m*26+4;o=Z["top"]+X+Z["sh"]+X+Z["ah"]+M;a=hp
		if h is None:k=min(1.,b/float(F));c=int(round(a+(Q-a)*k))
		else:c=h-o;k=min(1.,b/float(F),(c-a)/float(Q-a))
		g=k<eL-.001
		if g:k=eL;c=int(round(a+(Q-a)*k))
		Z["pen_h"],Z["k"],Z["scroll"]=c,k,g;Z["sy"]=Z["top"]+c+X;Z["ay"]=Z["sy"]+Z["sh"]+X;Z["h"]=Z["ay"]+Z["ah"]+M;Z["ox"]=M+(b-F*k)/2.;Z["oy"]=Z["top"]+a*(1.-k)+(c-a-(Q-a)*k)/2.;return Z
	def hq(w,h):
		d=cY();a=1.;b,c=w,h
		if w<d:e=ca(d,None)["h"];a=min(w/float(d),h/float(e));b,c=int(round(w/a)),int(round(h/a))
		Z=ca(b,c)
		if Z["scroll"]and a==1.:b=w-Kit.SCROLL_BAND;Z=ca(b,c);return b,c,a,Z,Z["h"]
		return b,c,a,Z,None
	def eN(g,store,x,y,w,h,c):
		d=Kit.wrap("%s decided it is better off without a master and flew away."%m(),w-40)
		for i,a in enumerate(d[:c]):P(g,a,x+(w-u(a))//2,y+32+i*18,o)
		b="Adopt a new pup";an(g,store,"adopt",ap,x+(w-35-u(b))//2,y+h-36,b,"Start again; squeaks, wardrobe, virtues and relics stay",on_click=aa("adopt"))
	def eO(g,c,v,sy,iw,sh,bw,pair1=True,pair2=True):
		ah(g,M,sy,iw,sh);d=M+12+max(u(k)for n,k in bt)+10;c["bars"]={}
		for i,(e,j)in enumerate(bt):b=sy+8+i*18;c["nl_"+e]=W(g,v,j,M+12,b,ag);bP(g,Kit.LINE_RED,d,b+3,bw,11);c["bars"][e]=bP(g,Kit.LINE_BLUE,d,b+3,bw,11);c["nv_"+e]=W(g,v,"",d+bw+8,b,o)
		h=u("Age 99h 59m");a=sy+82;c["loyal"]=W(g,v,"",M+12,a,ag)
		if pair1:c["age"]=W(g,v,"",M+iw-12-h,a,o);c["loyal_w"]=iw-24-h-6
		else:a+=18;c["age"]=W(g,v,"",M+12,a,o);c["loyal_w"]=iw-24
		f=a+18;c["sq"]=W(g,v,"",M+12,f,ab)
		if pair2:c["pers"]=W(g,v,"",M+iw-12-u("Mischievous"),f,o)
		else:c["pers"]=W(g,v,"",M+12,f+18,o)
	def hr(g,store,c,v,lw,x,d,Z):
		b=Z["IW"];a4(g,lw,Z["h"]if Z["scroll"]else x);bh(g,store,"main",lw,ae,[("settings",aI,"Settings",c3%ae)],dock=True,close_tip=bO%ae);e,h,k=Z["top"],Z["pen_h"],Z["k"];ah(g,M,e,b,h);c["pen_w"],c["iw"],c["bar_w"]=b,b,Z["bar_w"];c["pen_title"]=W(g,v,"",M+8,e+6,ab);c["pantry_lbl"]=W(g,v,"",M+b-8-u("Pantry 20"),e+6,o)
		if j["feral"]:eN(g,store,M,e,b,h,max(1,(h-70)//18))
		else:
			v.made=[];eK(g,c,v);i,l=[],set()
			for a in v.made:
				if id(a)not in l:l.add(id(a));i.append(a)
			v.made=None;v.pen=l;v.xf=(r,C,Z["ox"],Z["oy"],k);c["pen_ctrls"]=i;c["pen_k"]=k
			for a in i:
				f=v.cache.get(id(a))or{};m,n=f.get("pos"),f.get("size")
				with Kit.quiet:
					if m is not None:y,z=v.tr(m[0],m[1]);a.SetPos(int(round(y)),int(round(z)))
					if n is not None:a.SetWidth(max(1,int(round(n[0]*k))));a.SetHeight(max(1,int(round(n[1]*k))))
			c["grem_k"]=None;cW(c,1.)
		eO(g,c,v,Z["sy"],b,Z["sh"],Z["bar_w"],Z["pair1"],Z["pair2"]);p=Z["ay"];ah(g,M,p,b,Z["ah"]);q,A=Z["ncols"],Z["col_w"]
		for s,(t,B,D,E)in enumerate(bK):an(g,store,t,B,M+12+(s%q)*A,p+8+(s//q)*26,D,E,on_click=aa(t))
		if d!=1.:
			Kit.scale_window(g,d)
			if v.xf is not None:v.xf=(r,C,Z["ox"]*d,Z["oy"]*d,k*d);c["pen_k"]=k*d;c["grem_k"]=None;cW(c,1.)
		if v.xf is not None:
			for a in c.get("pen_ctrls")or():
				f=v.cache.get(id(a))or{}
				if "text"in f:
					w=Kit.client_control(a)
					if w is not None:safe(lambda a=w:a.SetInternalScale(v.xf[4]))
	def hs(w,h,mode):
		a=(int(w),int(h))if(w is not None and h is not None)else None
		if a!=i.get("fit")or(mode=="again"and a is not None):i["fit"]=a;i["redraw"]=True
	def ht():return i.get("zone_k")or(1.,None)
	def eP():
		def h(g,store,c,v):
			if i["minimized"]:c["mini"]=cX(g,store,"main",ae,bO%ae);return
			a4(g,bS,dt);bh(g,store,"main",bS,ae,[("settings",aI,"Settings",c3%ae)],dock=True,close_tip=bO%ae);ah(g,r,C,F,Q);c["pen_title"]=W(g,v,"",r+8,C+6,ab);c["pantry_lbl"]=W(g,v,"",r+F-8-u("Pantry 20"),C+6,o)
			if j["feral"]:eN(g,store,r,C,F,Q,3)
			else:eK(g,c,v)
			eO(g,c,v,SY,IW,SH,dH);ah(g,M,AY,IW,AH);b=0
			for d,(k,f,e,h)in enumerate(bK):
				a=M+12+(d%3)*88
				if d%3 and a<b:a=b
				l=AY+8+(d//3)*26;an(g,store,k,f,a,l,e,h,on_click=aa(k));b=a+35+u(e)+6
		a=i.get("fit");i["zone_k"]=None
		if a is not None and not i["minimized"]:
			d,k,b,Z,e=hq(a[0],a[1])
			if b!=1.:i["zone_k"]=(b,(cY(),ca(cY(),None)["h"]))
			def f(g,store,c,v):hr(g,store,c,v,d,k,b,Z)
			if e is not None:bj("main",f,d,e,a[1])
			else:bj("main",f,a[0],a[1])
		elif a is not None:
			def l(g,store,c,v):c["mini"]=cX(g,store,"main",ae,bO%ae,w=max(aC,a[0]));c["mini_w"]=max(aC,a[0])
			bj("main",l,max(aC,a[0]),bT,None,i["docked"])
		else:w,m=(aC,bT)if i["minimized"]else(bS,dt);bj("main",h,w,m,None,i["minimized"]and i["docked"])
		eQ(time.time(),True);bg()
	h1=None;ad=dict((iE,cF if iE=="main"else{"g":None,"c":{},"store":({},{}),"v":None})for iE in bR);cb={}
	def hu():
		b=d1(m().upper(),l["eq"].get("title","")).upper();a=["pup","mongotchi","greater"][j["stage"]]
		if b0(ar):a="avatar"
		return "%s  (%s)"%(b,"gone wild"if j["feral"]else a)
	def eQ(t,texts):
		c,v=ad["main"]["c"],ad["main"]["v"]
		if v is None:return
		if c.get("mini")is not None:
			if i["docked"]:return
			y=cR()
			if texts or y:
				if j["feral"]:m,e="gone wild",E
				elif y:m=gB[y[0]];e=E if int(t*2)%2==0 else ag
				elif j["away"]:m,e=d_(),o
				elif j["asleep"]:m,e="asleep",o
				else:m,e=d0()
				z,A="%s: %s"%(ae,m),c.get("mini_w",aC)-90;n=c.get("mini_fit")
				if n is None or n[0]!=z or n[1]!=A:n=c["mini_fit"]=(z,A,R(z,A))
				v.text(c["mini"],n[2],e)
			return
		for k,ac in bt:a=c.get("bar_w",dH)*j[k]/100.;f=i["bar_w"].get(k,a);K=max(1.,abs(a-f)*.25);f=a if abs(a-f)<=K else f+K*(1 if a>f else-1);i["bar_w"][k]=f;v.width(c["bars"].get(k),int(round(f)))
		a=int(l["sq"]);d=i.get("sq_shown",a)
		if d!=a:d+=max(1,abs(a-d)//5)*(1 if a>d else-1);i["sq_shown"]=d;v.text(c["sq"],"Squeaks %d"%d,D if a>d or i.get("sq_up")else ab);i["sq_up"]=a>d
		elif texts:i["sq_shown"]=a;v.text(c["sq"],"Squeaks %d"%a,ab)
		if texts:
			S=u("Pantry 20");L=eq("ncol");v.text(c["pen_title"],R(hu(),c.get("pen_w",F)-16-S-6),L["hue"]if L else ab);v.text(c["pantry_lbl"],"Pantry %d"%j["pantry"],E if j["pantry"]==0 else o)
			for k,T in bt:M=int(round(j[k]));v.text(c["nv_"+k],"%d%%"%M);v.text(c["nl_"+k],T,E if M<25 else ag)
			U,e=d0();V="  (sick)"if j["sick"]else "";v.text(c["loyal"],R(U+V,c.get("loyal_w",IW-24-u("Age 99h 59m")-6)),E if j["sick"]else e);v.text(c["age"],"Age "+hm(j["age"]));v.text(c["pers"],eq("pers")["name"])
		if c.get("doll")is None:return
		g=i["anims"]
		if g:
			for W in[dx for dx,bw in g.items()if t-bw["t0"]>=bw["dur"]]:del g[W]
		N=l["eq"];B=(N.get("decor"),N.get("hang"))
		if c.get("worn")!=B:
			c["worn"]=B
			for k in("decor","hang"):
				q=eq(k)
				if q:v.look(c[k],q["gfx"],q["hue"])
				v.show(c[k],q is not None)
		if B[1]and eq("hang"):v.move(c["hang"],r+F-48+2*math.sin(t*1.3),C+20)
		G,O=a2("pantry_pop",t)if g else(None,0.);s=min(j["pantry"],dG)
		if G is not None or c.get("pantry_n")!=s:
			c["pantry_n"]=None if G is not None else s
			for b,p in enumerate(c["pantry"]):
				v.show(p,b<s);X=az[b%len(az)][0];H,w=r+4+b*11+22,C+Q-38+(b%2)*3+17;k=1.
				if G is not None and b==s-1:k=.3+.7*O;w-=6*math.sin(O*math.pi)
				bJ(v,p,X,H,w,k,(44,34))
		I,Y=a2("clean",t)if g else(None,0.);J=max(j["messes"],i.get("mess_was",0)if I else 0);x=I is not None
		if g and not x:
			for k in cs:
				if k in g:x=True;break
		if x or c.get("mess_n")!=(J,j["messes"]):
			c["mess_n"]=None if x else(J,j["messes"])
			for b,p in enumerate(c["mess"]):
				P=b<J;v.show(p,P)
				if not P:continue
				H,w=r+84+b*44+22,C+Q-28+12;k=1.;Z,aa=a2(cs[b]if b<len(cs)else "mess%d"%b,t)
				if I is not None and b>=j["messes"]:k=max(.05,1.-Y)
				elif Z is not None:k=.2+.8*aa
				bJ(v,p,c7,H,w+(1-k)*8,k,(44,24))
		a=.55 if j["asleep"]and not j["feral"]else 0.;h=i.get("night_a",a);h=a if abs(a-h)<.06 else h+.06*(1 if a>h else-1);i["night_a"]=h;v.alpha(c["night"],h);hC(t,c,v)
		if c.get("snow"):hy(t,c,v)
		if i["seasons"]and "newyear"in i["seasons"]and not i["fw_at"]-cA[1]<=t<i["fw_at"]:hz(t)
		eF(v,c,"main",t,r,C,F,Q)
	def hv(t,a,toy):
		y=i["toy"];m=toy.get("motion","bounce");b,c=r+6,r+F-50
		if m in("bounce","bouncy","dice"):
			y[3]+=320.*a;y[0]+=y[2]*a;y[1]+=y[3]*a
			if y[1]>=aA:y[1]=float(aA);y[3]=-random.uniform(220,300)if m=="bouncy"else-random.uniform(80,120)if m=="dice"else-random.uniform(140,220)
		elif m=="float":y[0]+=y[2]*.5*a;y[1]=aA-50+30*math.sin(t*1.7)
		elif m=="scurry":
			y[1]=float(aA);y[0]+=y[2]*1.6*a
			if random.random()<a*.8:y[2]=-y[2]
		elif m=="hover":y[0]=r+F/2.-22+60*math.sin(t*1.3);y[1]=C+50+12*math.sin(t*2.6)
		elif m=="music":
			if t>=i["music_at"]:i["music_at"]=t+2.5;S(toy.get("snd"))
			d=r+F/2.-N/2.;return d+40*math.sin(t*3.),aw+20+10*math.sin(t*6.)
		if y[0]<=b or y[0]>=c:y[0]=V(y[0],b,c);y[2]=-y[2]
		return y[0]-6,y[1]-ai+22
	def hw(t,gone):
		if t<i.get("amb_at",0.)or gone or j["feral"]:return
		i["amb_at"]=t+random.uniform(1.2,2.2);x,y=bH()
		if j["asleep"]:ao(random.choice(["z","z","Z"]),e6,x+14,y+4,8.,-14.,2.4);return
		if j["clean"]<35 or j["messes"]>=2:
			ao("~",c8,x+random.uniform(-14,14),y+18,0.,-12.,1.8)
			for a in range(j["messes"]):
				if random.random()<.5:ao("~",c8,r+84+a*44+22,C+Q-30,0.,-10.,1.6)
		if j["sick"]and random.random()<.6:ao("o",co,x+random.uniform(-8,8),y+10,0.,-16.,1.6)
		elif j["food"]<25 and random.random()<.3:ao("?",o,x+16,y,0.,-10.,1.4)
		elif j["joy"]<25 and random.random()<.3:ao("...",o,x+16,y,0.,-8.,1.8)
		elif be()>=85 and random.random()<.15:aO(hl,x,y+18,1.2,0,64)
	eR,eS=C+22,C+Q-7
	def hx(g,v,c):
		a=i["snow"]
		if len(a)!=dA:i["snow"]=a=[[random.uniform(r+6,r+F-9),random.uniform(eR,eS),random.uniform(dB[0],dB[1]),random.uniform(0.,6.28),random.choice((2,2,3))]for h in range(dA)]
		b=ch(g,r+2,C+Q-5,F-4,3,.85,"#FFFFFF")
		if b is not None:v.reg(b,pos=(r+2,C+Q-5),size=(F-4,3))
		e=[]
		for f in a:
			d=ch(g,int(f[0]),int(f[1]),f[4],f[4],.9,"#FFFFFF")
			if d is not None:v.reg(d,pos=(int(f[0]),int(f[1])),size=(f[4],f[4]));e.append((d,f))
		c["snow"],c["snow_ground"]=e,b
	def hy(t,c,v):
		a=max(0.,min(.5,t-i.get("snow_t",t)));i["snow_t"]=t
		for b,f in c["snow"]:
			f[1]+=f[2]*a
			if f[1]>=eS:f[0]=random.uniform(r+6,r+F-9);f[1]=float(eR)
			v.move(b,f[0]+3.*math.sin(t*1.3+f[3]),f[1])
	def hz(t):
		i["fw_at"]=t+random.uniform(cA[0],cA[1]);a=random.choice(bv);x=random.uniform(r+40,r+F-40);y=random.uniform(C+36,C+60);aO(bk,x,y,1.,a,48)
		for b in(-14,14):ao("*",a,x+b,y,b*1.6,-8.,.9)
	hA=("loop","rumble","yawn","hop","shake","stretch","cough","flash","spooky","grow","arrive");hB=dict((iG,iF)for iF,iG in enumerate(hA))
	def hC(t,c,v):
		k=max(0.,min(.5,t-i.get("anim_t",t)));i["anim_t"]=t;f,l=i["px"],i["py"];Z=j["stage"];g=35.*am("speed",1.);m=4.;d=None;e=i["grem"];x=j["away"]and t>=i["leave_until"];aa,ag=a2("zoom",t)
		if aa:g*=2.5;m*=2.
		K=t<i["eat_until"]and i["eat_food"]is not None;B=False
		if j["away"]:
			if not x:i["tx"],i["ty"],g,m=a9+30.,float(aw),140.,10.
		elif j["feral"]:pass
		elif j["asleep"]:i["tx"],i["ty"],g=float(r+F//2-N//2),float(aL),30.
		elif e is not None and e["phase"]=="walk"and e["guard_at"]and t>=e["guard_at"]:i["tx"],i["ty"],g,m=e["x"]-6,float(aL),170.,11.
		elif K:
			L=float(i["eat_x"]-6);i["tx"],i["ty"],g,m=L,float(aL-4),110.,7.;B=abs(f-L)<6 and abs(l-(aL-4))<6;y=1.
			if B:
				i.setdefault("eat_t0",t);y=max(0.,1.-int((t-i["eat_t0"])/.45)*.25)
				if y<i.get("eat_bites",1.):bI(".",e7,random.uniform(-10,10),34,random.uniform(-15,15),10.,.8)
				i["eat_bites"]=y
			d=(i["eat_food"][0],i["eat_x"]+16,aA+17,0,max(.05,y))
		elif t<i["play_until"]and i["play_toy"]is not None:
			z=i["play_toy"];i["tx"],i["ty"]=hv(t,k,z);g,m=95.*am("speed",1.),8.;d=(z["gfx"],i["toy"][0]+22,i["toy"][1]+17,z["hue"],1.)
			if z.get("motion")=="music"and random.random()<k*1.5:bI(random.choice(["~","*","+"]),random.choice(bv),random.uniform(-20,20),6,random.uniform(-10,10),-18.,1.4)
			elif abs(i["toy"][0]+22-(f+N/2.))<14 and random.random()<k*2:bI("!",D,0,-4,0.,-24.,.8)
		else:
			if j["food"]<25 or j["energy"]<15:m=2.6;g*=.6
			if abs(i["tx"]-f)<2 and abs(i["ty"]-l)<2 or i["tx"]==0:
				if t>=i["hover_until"]:
					ab=aw+30 if(j["food"]<25 or j["joy"]<25)else aw;i["tx"]=float(random.randint(dF,a9));i["ty"]=float(random.randint(min(ab,aL),aL));i["hover_until"]=t+random.uniform(.5,2.5)/am("speed",1.);E=random.random()
					if be()>=80 and E<.12:O("loop",1.)
					elif j["food"]<25 and E<.25:O("rumble",.5)
					elif j["energy"]<20 and E<.25:O("yawn",1.4)
		if t<i["cure_until"]:p=1.-(i["cure_until"]-t)/1.5;d=(e4,f+N/2.+26*(1-p),l+18+6*(1-p),0,max(.1,1-p))
		elif t<i["brush_until"]:
			d=(e5,f+N/2.+14*math.sin(t*12),l+14+4*math.cos(t*12),0,1.)
			if random.random()<k*4:bI("*",bq,random.uniform(-18,18),random.uniform(4,24),0.,-14.,.7)
		M=c["doll"];P,G=a2("farewell",t)
		if not x and not j["feral"]:
			if t<i["dizzy_until"]and not j["asleep"]:i["tx"]+=30*math.sin(t*4.)*k*10
			i["tx"]=V(i["tx"],dF,a9+(40 if j["away"]else 0));i["ty"]=V(i["ty"],aw,aL);f,l=i["px"],i["py"]=dW(f,l,i["tx"],i["ty"],g*k)
		if j["asleep"]:a=eJ(t)
		elif K and B:a={"sx":.72,"sy":.86+.14*abs(math.sin(t*14)),"ox":0.,"oy":2.}
		else:ac=.6 if(j["joy"]<25 or j["sick"])else 1.;a=eI(t,m,0.,Z,ac)
		if j["sick"]and not j["asleep"]:a["ox"]+=random.uniform(-1.,1.)
		ad=i["play_toy"]is not None and t<i["play_until"]and i["play_toy"].get("motion")=="music"
		if ad:a["ox"]+=6*math.sin(t*3.);a["oy"]+=3*math.sin(t*12.)
		if t<i["dizzy_until"]and not j["asleep"]:
			a["ox"]+=6*math.sin(t*5.);a["oy"]+=4*math.cos(t*5.)
			if random.random()<k:bI("@",e8,10,-2,4.,-12.,1.)
		if t<i["brush_until"]:a["ox"]+=2*math.sin(t*25)
		R=i["anims"]
		if R:
			n=None
			for ae,q in R.items():
				o=hB.get(ae)
				if o is not None:
					S=t-q["t0"]
					if S<q["dur"]:
						if n is None:n=[]
						n.append((o,S/q["dur"]))
			if n is not None:
				if len(n)>1:n.sort()
				for o,p in n:
					if o==0:a["ox"]+=12*math.sin(p*2*math.pi);a["oy"]+=-12*(1-math.cos(p*2*math.pi))/2.
					elif o==1:a["ox"]+=2*math.sin(t*60)
					elif o==2:a["sy"]*=1.-.12*math.sin(p*math.pi);a["oy"]+=3*math.sin(p*math.pi)
					elif o==3:
						if p<.3:a["sy"]*=1.-.22*math.sin(p/.3*math.pi)
						else:a["oy"]-=9*math.sin((p-.3)/.7*math.pi)
					elif o==4:a["ox"]+=3*math.sin(t*40)*(1-p)
					elif o==5:a["sy"]*=.75+.25*p;a["oy"]-=6*math.sin(p*math.pi)
					elif o==6:a["sy"]*=1.-.15*math.sin(p*math.pi);a["oy"]+=2*math.sin(p*math.pi)
					elif o==7:a["hue"]=co if int(t*10)%2==0 else 0
					elif o==8:a["hue"]=bq if int(t*8)%2==0 else cp
					elif o==9:a["hue"]=bq if int(t*8)%2==0 else None;a["k"]=.8+.2*abs(math.sin(t*10))
					else:
						a["oy"]-=70*(1-p)**2
						if p>.8:a["sy"]*=1.-.25*math.sin((p-.8)/.2*math.pi)
		if P:a["oy"]-=70*G;a["ox"]+=30*G;a["k"]=max(.05,1.-.9*G)
		H=x or(j["away"]and f>=a9)or(j["feral"]and not P);w,s=min(f,a9)+N/2.,V(l,aw-3,aL)+ai/2.
		if H:b9(v,M,0,0,None,t,shown=False);v.show(c["pet_hit"],False)
		else:b9(v,M,w,s,bD(),t,a);v.move(c["pet_hit"],w-N/2.,s-ai/2.);v.show(c["pet_hit"],not j["feral"])
		if d is not None:v.look(c["prop"],d[0],d[3]);bJ(v,c["prop"],d[0],V(d[1],r+14,r+F-14),V(d[2],C+30,aA+17),d[4],(44,34));v.show(c["prop"],True)
		else:v.show(c["prop"],False)
		b=i.get("carry");h=None
		if b is not None:
			if b["who"]=="pet"and not H:h=(w,s+20,1.)
			elif b["who"]=="grem"and e is not None:h=(e["x"]+au/2.+14,aD+34+2*math.sin(t*10),1.)
			elif b["who"]=="drop":
				p=(t-b["t0"])/.8
				if p>=1.:i["carry"]=None;O("pantry_pop",.4)
				else:h=(b["x"]+(r+34-b["x"])*p,b["y"]+(C+Q-20-b["y"])*p-30*math.sin(p*math.pi),1.-.5*p)
			if h is not None:v.look(c["prop2"],b["gfx"],0);bJ(v,c["prop2"],b["gfx"],h[0],h[1],h[2],(44,34))
			if b["who"]=="pet"and not j["away"]and t-b.get("t0",t)>=1.8:i["carry"]={"who":"drop","gfx":b["gfx"],"t0":t,"x":w,"y":s+20}
		v.show(c["prop2"],h is not None)
		if e is not None:
			af=abs(math.sin(t*10));T=V(e["x"],r+4,aM)+au/2.;U=aD+aR-2*af;A=1.;W=True;q,p=a2("gswat",t)
			if q:W=int(t*12)%2==0;U-=10*math.sin(p*math.pi)
			q,p=a2("gtrap",t)
			if q:A=max(.05,1.-p)
			cW(c,A);bw,bh=au*A,aR*A;v.move(c["grem"],T-bw/2.,U-bh);v.move(c["grem_hit"],T-au/2.,aD);v.show(c["grem"],W);v.show(c["grem_hit"],e["phase"]=="walk")
		else:v.show(c["grem"],False);v.show(c["grem_hit"],False)
		I=i["say"]if not j["asleep"]and t<i["say_until"]and not x else "";v.text(c["say"],I)
		if I:
			X=u(I);sx=V(w-X/2.,r+6,r+F-6-X);Y=(a or{}).get("oy",0.);J=s+min(0.,Y)-ai/2.-22
			if J<C+24:J=s+max(0.,Y)+ai/2.+6
			v.move(c["say"],sx,V(J,C+24,C+Q-18))
		hw(t,H)
	def cZ(cats,sw=SW):
		a,x,y=M+10,M+10,0;b=[]
		for n,(e,d,f)in enumerate(cats):
			c=u(d)
			if x+c>sw-M-10 and x>a:x,y=a,y+20
			b.append((n,x,y));x+=c+14
		return b,y+20+14
	def hD():
		a=b3();i["shop_cat"]=min(i["shop_cat"],len(a)-1);e=M+30+X;b=e+30+X;d,j=b6("shop",SW,b+cZ(a)[1]+X+8+dv*38+30+M);n,m=cZ(a,d);f=b+m+X;k=j-f-M;h=i["shop_n"]=max(1,(k-38)//38)
		def p(g,store,c,v):
			q=d-2*M;a4(g,d,j);bh(g,store,"shop",d,ae+" Shop");ah(g,M,e,q,30);c["sq"]=W(g,v,"",M+10,e+7,ab);F="+%d an hour, even when away"%int(cv);P(g,R(F,q-130),M+q-10-min(u(F),q-130),e+7,o);ah(g,M,b,q,m)
			for r,x,G in n:A=a[r][1];T=ab if r==i["shop_cat"]else ag;P(g,A,x,b+7+G,T);bn(g,x-3,b+5+G,u(A)+6,18,aa(("shop","cat",r)),"Show the %s tab"%A.lower())
			ah(g,M,f,q,k);H=en();I=max(1,(len(H)+h-1)//h);i["shop_page"]=min(i["shop_page"],I-1);J=i["shop_page"]*h
			for K,p in enumerate(H[J:J+h]):
				s=f+8+K*38
				if p["cat"]=="ncol":P(g,"Abc",M+14,s+9,p["hue"])
				elif p["gfx"]:ak(g,v,p["gfx"],M+6,s,44,34,p["hue"])
				x=M+q-10
				for U,(L,N,V)in enumerate(em(p)):x-=35+u(N);an(g,store,"r%d_%d"%(K,U),gI[L],x,s+6,N,gK(L,p),on_click=aa(("shop","act",p["id"],V)));x-=8
				w=af(p["id"])and not aF(p);O=bC(p);Q=p["name"]
				if w:B=a1.get(p["cat"]);t="owned"if not B or l["eq"].get(B)!=p["id"]else "worn"if B in("hat","neck")else "in use"
				else:t=("%s only"%dN[p["season"]])if not O else "%d sq"%bA(p);r=l["cnt"].get(p["id"],0)if aF(p)else 0;Q+="  x%d"%r if r else ""
				X=u(t);x-=X;Y=w or l["sq"]>=bA(p);P(g,t,x,s+9,o if w or not O else D if Y else E);S=x-6-(M+56);P(g,R(Q,S),M+56,s+1,ag);y=ej(p)if not w else None;z=p["desc"]
				if "season"in p:z="%s: %s"%(dN[p["season"]],z[:1].lower()+z[1:])
				P(g,R(y[:1].upper()+y[1:]if y else z,S),M+56,s+18,E if y else o)
			C=f+k-28;an(g,store,"prev",fS,M+10,C,None,"Previous page",on_click=aa(("shop","prev")));an(g,store,"next",ap,M+q-40,C,None,"Next page",on_click=aa(("shop","next")));t="%s: page %d of %d"%(a[i["shop_cat"]][1],i["shop_page"]+1,I);P(g,t,M+(q-u(t))//2,C+3,o)
		b7("shop","Shop",p,d,j);eT(0.,True);bg()
	def eT(t,texts):
		c,v=ad["shop"]["c"],ad["shop"]["v"]
		if v is None or not texts:return
		if c.get("mini")is not None:v.text(c["mini"],"Shop: %d squeaks"%int(l["sq"]))
		elif c.get("sq")is not None:v.text(c["sq"],"Squeaks %d"%int(l["sq"]))
	def hE():
		a=cS();b,e=b6("pen",cy,cC);d=e-cC
		def n(g,store,c,v):
			h=b-2*M;a4(g,b,e);bh(g,store,"pen",b,ae+" Playpen",[("share",ap,"Share","Post %s's code in chat for friends' playpens"%m())]);ah(g,aj,al,h,QH+d);c["head"]=W(g,v,"",aj+8,al+6,ab);c["toy"]=ak(g,v,3613,aj+20,al+QH-40,44,34,shown=False);c["dolls"]=[]
			for n in range(aJ):x=aS+n*(aT-aS)//max(1,aJ-1);j=eH(g,v,x,aU+20);j["name"]=W(g,v,"",x,al+QH-18,ab);j["say"]=W(g,v,"",x,aU,ag);c["dolls"].append(j)
			c["spr"],c["plbl"]=eG(g,v,aj,al)
			if len(a)<=1:
				s="Nobody else here yet. Share your code, or paste a friend's below."
				for t,k in enumerate(Kit.wrap(s,QW-60)[:2]):P(g,k,aj+(QW-u(k))//2,al+QH//2-40+t*18,o)
			ah(g,M,cB+d,h,dI);l=h//2
			for n in range(aJ):
				x=M+10+(n%2)*l;y=cB+d+8+(n//2)*25
				if n>=len(a):P(g,"Free slot",x+34,y+3,o);continue
				f=a[n]
				if not f["mine"]:an(g,store,"rm%d"%n,a3,x,y,None,"Send %s home"%f["name"],on_click=aa(("pen","rm",n)))
				w="%s (yours)"%f["name"]if f["mine"]else "%s (%s)"%(f["name"],f["owner"]);P(g,R(w,l-50),x+34,y+3,D if f["mine"]else ag)
			i=dJ+d;ah(g,M,i,h,dK);P(g,"Code:",M+10,i+12);p="Add";q=M+h-10-35-u(p);r=M+10+u("Code:")+10;c["code"]=cl(Kit.add_textbox(g,"",r,i+9,q-r-12,numbers=False),"A friend's Mongotchi code (64 characters)");an(g,store,"add",cg,q,i+8,p,"Add that mongotchi to your playpen",on_click=aa(("pen","add")))
		b7("pen","Playpen",n,b,e);j={}
		for k in a:
			l=(k["uid"],k["owner"]);f=i["pals"].get(l)
			if f is None:
				h=float(random.randint(aU,bU));f={"x":float(aT),"y":h,"tx":float(aS+random.randint(0,aT-aS)),"ty":h,"until":0.,"say":"","say_until":0.,"chase":None,"chase_until":0.,"phase":random.uniform(0,6.28)}
				if i["pals"]:aO(bG,aT+N/2.,h+ai/2.,1.2,0,64,"pen")
			j[l]=f
		i["pals"]=j;eV(time.time(),True);bg()
	def eU(p,text,t,secs=3.):p["say"],p["say_until"]=text,t+secs
	def eV(t,texts):
		c,v=ad["pen"]["c"],ad["pen"]["v"]
		if v is None:return
		e=cS()
		if c.get("mini")is not None:
			if texts:v.text(c["mini"],"Playpen: %s"%a5(len(e),"mongotchi"))
			return
		f=max(0.,min(.5,t-i.get("pen_t",t)));i["pen_t"]=t
		if texts:v.text(c["head"],R("PLAYPEN  (%d of %d)"%(len(e),aJ),QW-16))
		g=bE["keys"];a=i.get("pen_game")
		if a is None and len(e)>1 and random.random()<f/25.:
			s=eq("toy")
			if s.get("motion")!="music":i["pen_game"]=a={"until":t+8.,"toy":s,"b":[float(aj+20),float(al+QH-60),random.uniform(80,120),-80.]}
		if a is not None and t>=a["until"]:i["pen_game"]=a=None
		if a is not None:
			b=a["b"];b[3]+=300.*f;b[0]+=b[2]*f;b[1]+=b[3]*f
			if b[1]>=al+QH-40:b[1]=float(al+QH-40);b[3]=-random.uniform(150,230)
			if b[0]<=aj+6 or b[0]>=aj+QW-50:b[0]=V(b[0],aj+6,aj+QW-50);b[2]=-b[2]
			v.look(c["toy"],a["toy"]["gfx"],a["toy"]["hue"]);v.move(c["toy"],b[0],b[1])
		v.show(c["toy"],a is not None)
		for n,d in enumerate(c["dolls"]):
			if n>=len(e):b9(v,d,0,0,None,t,shown=False);v.show(d["name"],False);v.show(d["say"],False);continue
			l=e[n];p=i["pals"].get(g[n])
			if p is None:continue
			h=gP(n,l);o=h["spd"]
			if p["chase"]is not None and t<p["chase_until"]and p["chase"]in i["pals"]:
				q=i["pals"][p["chase"]];p["tx"],p["ty"],o=q["x"],q["y"],90.
				if abs(q["x"]-p["x"])<20 and abs(q["y"]-p["y"])<16:C=(e[g.index(p["chase"])]["name"]if p["chase"]in g else "a friend");eU(p,random.choice(fV)%C,t);ao(random.choice(["<3","!","*boop*"]),random.choice([c9,fa,D]),q["x"]+N/2.,q["y"],0.,-20.,1.2,"pen");q["hop"]=t;p["chase"]=None;q["tx"],q["ty"]=float(random.randint(aS,aT)),float(aU);q["until"]=t+1.5
			elif a is not None:p["tx"],p["ty"],o=a["b"][0]-6,a["b"][1]-ai+22,80.
			else:
				p["chase"]=None
				if(abs(p["tx"]-p["x"])<2 and abs(p["ty"]-p["y"])<2)or p["tx"]==0:
					if t>=p["until"]:
						if len(e)>1 and random.random()<.25:p["chase"]=random.choice([Z for Z in g if Z!=g[n]]);p["chase_until"]=t+4.
						p["tx"]=float(random.randint(aS,aT));p["ty"]=float(random.randint(aU,bU));p["until"]=t+random.uniform(.5,3.)
						if random.random()<.08:E=ac.get(l["pers"]or "",{}).get("lines")or ax["idle"];eU(p,random.choice(E),t)
			p["tx"],p["ty"]=V(p["tx"],aS,aT),V(p["ty"],aU,bU);p["x"],p["y"]=dW(p["x"],p["y"],p["tx"],p["ty"],o*f);x,y=int(p["x"]),int(V(p["y"],aU-3,bU));k=bD()if l["mine"]else h["look"];w=p.get("phase",n*1.3)
			if l["mine"]and j["asleep"]:k=dict(k);k["hue"]=cp;r=eJ(t,w)
			else:F=(p["chase"]is not None and t<p["chase_until"])or a is not None;r=eI(t,8. if F else 4.,w,k["stage"])
			z=t-p.get("hop",-9.)
			if z<.5:r["oy"]-=8*math.sin(z/.5*math.pi)
			b9(v,d,x+N/2.,y+ai/2.,k,t,r);G=h["nm"];v.text(d["name"],G,h["hue"]);A=h["nw"];v.move(d["name"],V(x+N/2.-A/2.,aj+6,aj+QW-6-A),min(y+ai+2,al+QH-18));v.show(d["name"],True);m=p["say"]if t<p["say_until"]else "";v.text(d["say"],m);v.show(d["say"],bool(m))
			if m:B=u(m);v.move(d["say"],V(x+N/2.-B/2.,aj+6,aj+QW-6-B),max(al+24,y-18))
		eF(v,c,"pen",t,aj,al,QW,QH)
	bL=M+30+X;eW=48;bM=bL+eW+X;bm=bM+30+X;hF=8+bs*38+8;JH=bm+hF+M;cc=100
	def hG():
		a,b=b6("quest",JW,JH)
		def d(g,store,c,v):
			d=c["iw"]=a-2*M;a4(g,a,b);bh(g,store,"quest",a,ae+" Journeys");ah(g,M,bL,d,eW);c["status"]=W(g,v,"",M+10,bL+7,ab);c["status2"]=W(g,v,"",M+10,bL+26,o);f="Call home";h=M+d-10-35-u(f);c["home_x"]=h;c["home_lbl"]=an(g,store,"home",a3,h,bL+12,f,"Bring it back now with a share of the reward",on_click=aa(("quest","home")));c["home_btn"]=store[0].get("home");c["was_away"]=j["away"];ah(g,M,bM,d,30);x=M+12
			for n,e in enumerate(dS):k=ab if n==A["tab"]else ag;P(g,e,x,bM+7,k);bn(g,x-3,bM+4,u(e)+6,22,aa(("quest","tab",n)),"Show the %s tab"%e.lower());x+=u(e)+24
			i="%s, %s"%(a5(A["hunts"],"hunt"),a5(A["med"],"meditation"));P(g,R(i,d-(x-M)-10),M+d-10-min(u(i),d-(x-M)-10),bM+7,o);ah(g,M,bm,d,b-bm-M);c["rows"]=[];e=A["tab"]
			if e==0:hH(g,store,v,d)
			elif e==1:hI(g,store,d)
			else:hJ(g,v,d)
		b7("quest","Journeys",d,a,b);eX(time.time(),True);bg()
	def hH(g,store,v,l):
		n=j["away"]
		for i,a in enumerate(ay[:bs]):
			c=bm+8+i*38;d=bW[[s for s in a["loot"]if s[1]=="relic"][0][2]];ak(g,v,d[2],M+6,c,44,34,d[3]);b=dY(a["req"]);x=M+l-10
			if not n and not j["feral"]and b is None:e="Go";x-=35+u(e);an(g,store,"go%d"%i,ap,x,c+6,e,"Send %s hunting at %s (%d min)"%(m(),a["name"],a["mins"]),on_click=aa(("quest","hunt",i)));x-=8
			p="safe"if a["danger"]<=.05 else "a little risky"if a["danger"]<=.15 else "risky"if a["danger"]<=.3 else "dangerous";f="%d min, %s"%(a["mins"],p);q=u(f);x-=q;P(g,f,x,c+9,o if b is None else E);h=x-6-(M+56);k=A["visits"].get(a["id"],0);r=a["name"]+("  (x%d)"%k if k else "");P(g,R(r,h),M+56,c+1,ag if b is None else o);P(g,R(b[:1].upper()+b[1:]if b else a["hint"],h),M+56,c+18,E if b else o)
	def hI(g,store,m):
		n=j["away"]
		for i,c in enumerate(av[:bs]):
			k=c[0];b=bm+8+i*38;a=H(k);x=M+m-10
			if not n and not j["feral"]and a<ar:h="Meditate";x-=35+u(h);d,e=cK(k);an(g,store,"med%d"%i,ap,x,b+6,h,"Meditate at the Shrine of %s for %d min (%d/%d to level %d)"%(c[1],int(ct),int(d),int(e),a+1),on_click=aa(("quest","med",i)));x-=8
			f=x-cc;bP(g,Kit.LINE_RED,f,b+12,cc,11);d,e=cK(k);p=cc if a>=ar else int(cc*d/max(1.,e));bP(g,Kit.LINE_BLUE,f,b+12,max(0,p),11);l=f-6-(M+12);q="%s  Lv %d"%(c[1],a);P(g,R(q,l),M+12,b+1,ab if a>=ar else ag);r=(cL(k,a)if a else "Not yet felt: "+cL(k,1).lower()+" at level 1");P(g,R(r,l),M+12,b+18,o)
	def hJ(g,v,h):
		d=h//2
		for i,a in enumerate(bb):
			j,k=i//bs,i%bs;b=M+j*d;c=bm+8+k*38;n=A["relics"].get(a[0],0);e=next((p for p in ay if any(s[1]=="relic"and s[2]==a[0]for s in p["loot"])),None);f=e["name"]if e else ""
			if n:ak(g,v,a[2],b+6,c,44,34,a[3]);l=a[1][0].upper()+a[1][1:]+("  x%d"%n if n>1 else "");P(g,R(l,d-60),b+56,c+1,ag);P(g,R(f,d-60),b+56,c+18,o)
			else:P(g,"?",b+24,c+9,o);P(g,"Not found yet",b+56,c+1,o);P(g,R("Somewhere at "+f,d-60),b+56,c+18,o)
	def eX(t,texts):
		c,v=ad["quest"]["c"],ad["quest"]["v"]
		if v is None or not texts:return
		if j["feral"]:b,a="%s has gone wild"%m(),"Adopt a new pup in the pen first"
		elif j["away"]:d=eb(t);b="%s is %s"%(m(),dZ());a="Back in about %s (%d%% done)"%(hm(d+59)if d>=60 else "%d seconds"%int(d),int(ec(t)*100))
		else:
			b="%s is at home"%m()
			if A["tab"]==2:a="%d of %d relics found: +%d%% squeaks"%(len(A["relics"]),len(bb),int(round(cM()*100)))
			elif A["tab"]==1:a="Meditation earns experience; each level adds an effect"
			else:a="Far places are slower and riskier (Valor helps)"
		if c.get("mini")is not None:v.text(c["mini"],R("Journeys: %s"%("gone wild"if j["feral"]else d_()if j["away"]else "at home"),aC-90));return
		e=c.get("home_x",M+300)-(M+10)-8 if j["away"]else c["iw"]-20;v.text(c["status"],R(b,e));v.text(c["status2"],R(a,e));f=bool(j["away"])and j["away_kind"]!=0;v.show(c.get("home_btn"),f);v.show(c.get("home_lbl"),f)
		if j["away"]!=c.get("was_away"):c["was_away"]=j["away"];i["quest_redraw"]=True
	c_=M+30+X;cd=c_+30+X;hK=8+bX*38+8;eY=cd+hK+M
	def hL(a,done):
		if done or a[6]is None or a[6]=="stage"or a[7]<=1:return a[2]
		b="{:,}".format(int(min(ef[a[6]](),a[7])));return "%s (%s)"%(a[2],b)if a[7]>=1000 else "%s (%s/%d)"%(a[2],b,a[7])
	def hM():
		a,b=b6("ach",dE,eY)
		def d(g,store,c,v):
			i=c["iw"]=a-2*M;a4(g,a,b);bh(g,store,"ach",a,ae+" Achievements");ah(g,M,c_,i,30);c["status"]=W(g,v,"",M+10,c_+7,ab);ah(g,M,cd,i,b-cd-M);e=i//2;j=[]
			for k,d in enumerate(aW[:2*bX]):f=M+(k//bX)*e;h=cd+8+(k%bX)*38;n=d[0]in Y["got"];l="+%d"%d[3];m=u(l);j.append({"a":d,"raw":None,"nw":e-66-m-6,"hw":e-66,"pic":ak(g,v,d[4],f+6,h,44,34,d[5]if n else dD),"nm":W(g,v,"",f+56,h+1,ag),"rew":W(g,v,l,f+e-10-m,h+1,ab),"how":W(g,v,"",f+56,h+18,o)})
			c["rows"]=j
		b7("ach","Achievements",d,a,b);eZ(0.,True);bg()
	def eZ(t,texts):
		c,v=ad["ach"]["c"],ad["ach"]["v"]
		if v is None or not texts:return
		d=Y["got"];n=sum(1 for g in aW if g[0]in d);f=sum(h[3]for h in aW if h[0]in d)
		if c.get("mini")is not None:v.text(c["mini"],R("Achievements: %d of %d"%(n,len(aW)),aC-90));return
		v.text(c["status"],R("%d of %d earned: +%d squeaks"%(n,len(aW),f),c["iw"]-20))
		for r in c.get("rows",()):
			a=r["a"];b=a[0]in d;e=hL(a,b)
			if r["raw"]==(b,e):continue
			r["raw"]=(b,e);v.look(r["pic"],a[4],a[5]if b else dD);v.text(r["nm"],R(a[1],r["nw"]),D if b else ag);v.text(r["rew"],"+%d"%a[3],o if b else ab);v.text(r["how"],R(e,r["hw"]),o)
	def hN(action,t):
		b,a=action[0],action[1]
		if b=="main":Kit.win_action(a,i,aq,ae,ew,aK["main"])
		elif a=="toggle_min":k=b+"_min";i[k]=not i[k];c4(aK[b],i[k]);i[b+"_redraw"]=True
		elif b=="shop":
			if a=="cat":i["shop_cat"],i["shop_page"]=action[2],0
			elif a=="prev":i["shop_page"]=max(0,i["shop_page"]-1)
			elif a=="next":n=len(en());i["shop_page"]=min(max(0,(n-1)//i["shop_n"]),i["shop_page"]+1)
			elif a=="act":gM(action[2],action[3])
			i["shop_redraw"]=True
		elif b=="quest":
			if a=="tab":A["tab"]=action[2];i["quest_dirty"]=True
			elif a=="hunt":gr(action[2],t)
			elif a=="med":gu(action[2],t)
			elif a=="home":gw(t)
			i["quest_redraw"]=True
		elif b=="pen":
			if a=="share":ep()
			elif a=="rm":
				d=cS();n=action[2]
				if n<len(d)and not d[n]["mine"]:e=d[n];i["guests"]=[f for f in i["guests"]if not(f["uid"]==e["uid"]and f["owner"]==e["owner"])];cH();q("%s went home."%e["name"],o);i["pen_redraw"]=True
			elif a=="add":
				m=d3.search(str(safe(lambda:ad["pen"]["c"]["code"].Text,"")or ""));c=cO(m.group(1))if m else None
				if c is None:q("that isn't a Mongotchi code (64 characters).",E)
				elif not er(c)and c["uid"]==j["uid"]and c["owner"]==b1():q("that's your own mongotchi's code.",o)
	def ce(action,t):
		w=hQ[action]
		if i[w+"_open"]:
			if not cm(bi(w)):eA(w)
		else:
			i[w+"_open"],i[w+"_redraw"]=True,True
			if w=="pen"and not j["feral"]and J["share_open"]and J["share_min"]>0:ep()
			elif w=="pen":i["shared_at"]=t
	def hO(action,t):
		if j["feral"]:cN();i["redraw"]=True
	def hP(action,t):
		if t-i["confirm"]<6.:i["confirm"]=0.;q("%s released; a new pup arrives."%m(),o);cN();i["redraw"]=True
		else:i["confirm"]=t
		bN(aq)
	hQ={"shop":"shop","playpen":"pen","journey":"quest","ach":"ach"};e_={"feed":gg,"play":gj,"brush":gl,"cure":go,"forage":gp,"pet":gx,"clean":gm,"lights":gn,"swat":gz,"window":hN,"shop":ce,"playpen":ce,"journey":ce,"ach":ce,"adopt":hO,"refresh_page":lambda action,t:bN(aq),"release":hP};hR={"fw":60,"ugap":14};e0={"gremlins":("Gremlins raid the pantry","A gremlin that reaches the pantry takes half the food"),"sounds":("Play sounds","Squeaks, munching, gremlins and music"),"remind":("Remind me in the journal of its needs","At most every %d min per need"%int(dj/60)),"offline":("Keep living while the module is off (up to %d hours)"%cu,"Off: time stops while the module is off (squeaks still trickle in)"),"listen":("Add shared mongotchis to my playpen","Picks up \"%s\" lines from the journal"%cw),"share_open":("Share my code when I open the Playpen","Only while re-share reminders are on; off: only Share posts it"),"comp":("Follows me in the world","Only you see it; \"<name> go home\" or \"<name> come\" work too"),"comp_talk":("Talks over my head","Head messages only you see"),"comp_help":("Joins my fights (just for show)","Dives at your war-mode target; no damage")}
	def hS(w):
		def a(*keys):return[("check",c,R(e0[c][0],w-40),e0[c][1])for c in keys]
		b="Click again to confirm"if time.time()-i["confirm"]<6. else "Release %s"%m();return(("PET",[("text","name","Name:","Up to %d letters (; = | , are dropped)"%dk,{"tw":130}),("num","pace","Pace:","Need speed: 100 = normal, 200 = double","%")+aX["pace"],("num","grem_min","Gremlins every:","Average minutes between raids (%d-%d; the Scarecrow doubles it)"%aX["grem_min"],"min")+aX["grem_min"]]+a("gremlins","sounds","remind","offline")+[("buttons",(("release",a3,R(b,w-70),"Start over with a new pup (squeaks, wardrobe, virtues and relics stay); click twice within 6 s"),),{"bdy":0})],{"align":True}),("PLAYPEN",[("num","share_min","Remind to re-share every:","Minutes between Share reminders while the Playpen is open (%d-%d, 0 = never, and no post on opening)"%aX["share_min"],"min")+aX["share_min"]]+a("listen","share_open")+[("buttons",(("channel",aI,"Share in: %s"%bQ[J["share_ch"]][0],"Next chat for Share: Say, Party, Guild, Alliance or Whisper"),),{"bdy":0})]),("COMPANION  (needs the Companion Charm)",a("comp","comp_talk","comp_help")))
	def hT(f):
		if ck(f.store,"release"):aa("release")()
		if ck(f.store,"channel"):J["share_ch"]=(J["share_ch"]+1)%len(bQ);bY();aa("refresh_page")()
	def hU(f,new):new["name"]=cG(new["name"])
	def hV(a,new):
		if new["name"]!=a["name"]:i["redraw_at"]=time.time()+1.5
		i["texts_at"]=0.
	cf=Kit.Page(J,hS,bY,hV,hR,empty=J,adjust=hU,clicks=hT);dU()
	def hW():
		t=time.time();i.update({"shutting":False,"docked":False,"queue":[],"grem":None,"minimized":bp(aK["main"])or bool(HOST.dock_wanted(aq)),"redraw":False,"shop_redraw":False,"pen_redraw":False,"fit":None,"eat_until":0.,"play_until":0.,"cure_until":0.,"brush_until":0.,"leave_until":0.,"next_grem_ok":t+60.,"texts_at":0.,"next_chat":t+10.,"shop_open":False,"pen_open":False,"quest_open":False,"quest_redraw":False,"listen_at":0.,"sleep_after":0.,"pen_game":None,"comp":gW(),"hop":[],"read_at":0.,"jcodes":[],"jcmds":[],"jcodes_due":False,"player":None,"close_at":0.,"full_told":{},"shop_dirty":False,"quest_dirty":False,"ach_open":False,"ach_redraw":False,"ach_due":False,"ach_at":0.,"seasons":None,"season_at":0.,"fw_at":0.,"sim_acc":0.,"shop_n":dv});dU();f2();f6();f7();f4();ee(t,force=True)
		if f1():gf()
		else:l["last"]=t;i["shop_dirty"]=True;cN()
		eg(t);i["last_t"]=t;eP();a=Kit.dock_hooks(ae,du,i,ad["main"],ew,fit=hs);a.update({"exact":True,"verify":True,"drawn_at":ht});c1(aq,a);cb.clear()
		for b in cx:c1(bi(b),hf(b))
	def hX():
		if cF["g"]is None:return
		t=time.time()
		if t-i["close_at"]>=.25:
			i["close_at"]=t
			if Kit.closed(cF):return
			for a in bR:
				w=ad[a]
				if a!="main"and w["g"]is not None and ck(w["store"],"close"):eA(a)
		g0(t)
		if i["queue"]:c0();i["texts_at"]=0.;i["ach_due"]=True
		while i["queue"]:
			b=i["queue"].pop(0);g="window"if isinstance(b,tuple)else b
			if g in e_:e_[g](b,t)
		if i["confirm"]and not 0.<=t-i["confirm"]<6.:i["confirm"]=0.;bN(aq)
		h=max(0.,min(5.,t-i["last_t"]));i["last_t"]=t;ee(t);c=i["sim_acc"]+h;k=c>=hY
		if k:i["sim_acc"]=0.;e1(c)
		else:i["sim_acc"]=c
		p=not i["minimized"]
		if i["eat_food"]is not None and t>=i["eat_until"]:
			if i["eat_food"][2]:gh()
			else:i["eat_food"]=None
		if i.get("sleep_after")and t>=i["sleep_after"]:
			i["sleep_after"]=0.
			if a_():j["asleep"]=True;i["say"]=""
		if i["play_until"]and t>=i["play_until"]:i["play_until"]=0.;gk();i["play_toy"]=None
		if j["away"]and t>=i["away_until"]and t>=i["leave_until"]:cQ()
		gy(t,h,p);f9(t);gD(t)
		if k:gC(t)
		gN();hc(t)
		if i["ach_due"]or not i["ach_at"]-dC<=t<i["ach_at"]:eg(t)
		if i["pen_open"]:
			if J["share_open"]and J["share_min"]and t-i["shared_at"]>=J["share_min"]*60 and not j["feral"]:i["shared_at"]=t;q("time to Share %s's code again."%m(),o)
			if len(i["guests"])and t-i["social_at"]>=60.:
				i["social_at"]=t;T("social",min(3,len(i["guests"])))
				if not j["asleep"]and not j["feral"]:K("joy",2)
		if i.get("redraw_at")and t>=i["redraw_at"]:i["redraw_at"]=0.;i["redraw"]=i["quest_redraw"]=True
		if i.get("redraw"):
			i["redraw"]=False;eP()
			if i["pen_open"]:i["pen_redraw"]=True
		for a,l,n,d,e in e2:
			if i.get(d):
				i[d]=False
				if i[e]:l()
		f=t-i.get("texts_at",0.)>=1.
		if f:i["texts_at"]=t
		eQ(t,f)
		for a,l,n,d,e in e2:
			if i[e]:n(t,f)
		bg()
		if t-i["saved_at"]>=fH:c0();aY()
	hY=1.
	def e1(secs):
		a=[];d7(secs,a);T("passive",cv*secs/3600.)
		if a:d9(a);i["ach_due"]=True
	def c0():
		if i.get("sim_acc",0.)>0.:a,i["sim_acc"]=i["sim_acc"],0.;e1(a)
	e2=tuple((iH,iI,iJ,iH+"_redraw",iH+"_open")for iH,iI,iJ in(("shop",hD,eT),("pen",hE,eV),("quest",hG,eX),("ach",hM,eZ)))
	def hZ():return.1 if not i["minimized"]or(i["pen_open"]and not i["pen_min"])else.5
	def h_():
		i["shutting"]=True;c2(aq)
		for a in cx:c2(bi(a))
		for a in bR:cI(a)
		for k,b in aK.items():c4(b,i["minimized"if k=="main"else k+"_min"])
		bY();c0();aY(final=True)
		for a in bR:g,ad[a]["g"]=ad[a]["g"],None;ci(g)
		i["shop_open"]=i["pen_open"]=i["quest_open"]=i["ach_open"]=False
	return{"start":hW,"tick":hX,"stop":h_,"client_tick":True,"config_height":cf.height,"build_config":cf.build,"poll_config":cf.poll,"config_closed":cf.closed,"interval":hZ}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("mongotchi","Mongotchi","A pet mongbat to raise and dress up",_module_mongotchi,.1,category="Extras")
