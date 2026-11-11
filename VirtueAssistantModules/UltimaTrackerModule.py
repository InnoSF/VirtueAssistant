def _module_ultima():
	aX=Client.key_held;al=Follow.alt_held;ag=Follow.current;ax=Follow.toggle;ay=HOST.alert;az=HOST.alert_kind;aY=HOST.dock_add;X=HOST.dock_forget;aZ=HOST.dock_remove;a_=HOST.dock_to_bar;aA=HOST.harm_ok;H=HOST.layout_holds;Y=HOST.me;aB=HOST.mobile;am=HOST.mobiles;aC=HOST.refresh_settings;aD=HOST.show_settings;an=HOST.stopping;ao=Journal.reader;a0=Kit.AGO_SHORT;Z=Kit.ART_CLOSE;aE=Kit.ART_MIN;aF=Kit.ART_OK;L=Kit.ART_PAGE;aG=Kit.ART_PLAY;a1=Kit.ART_RESTORE;a2=Kit.CB_RGB;a3=Kit.CORNER_ART;a4=Kit.DOUBLE_TIP;J=Kit.GAP;l=Kit.HUE_BAD;A=Kit.HUE_GOOD;o=Kit.HUE_INFO;N=Kit.HUE_TEXT;ap=Kit.HUE_TITLE;u=Kit.MARGIN;aH=Kit.MIN_TIP;aq=Kit.SECTION_TILE;a5=Kit.SETTINGS_TIP;aI=Kit.STONE_TILE;a6=Kit.WINDOW_BG;B=Kit.add_label;O=Kit.add_section;a7=Kit.add_window_frame;aJ=Kit.ago;P=Kit.art_button;aK=Kit.basics;ah=Kit.catcher;aL=Kit.cb_hue;aM=Kit.clamp;a8=Kit.closed;R=Kit.count;a9=Kit.data_path;K=Kit.dispose;ba=Kit.dock_hooks;bb=Kit.drop_arrow;aN=Kit.facet_name;C=Kit.fit;aO=Kit.hp_mark;S=Kit.inert;E=Kit.is_open;bc=Kit.kv_load;bd=Kit.kv_save;be=Kit.load_min;bf=Kit.load_pos;bg=Kit.look_hue;bi=Kit.mini_bar;bj=Kit.moved_by_code;aP=Kit.noto_mark;V=Kit.noto_name;aQ=Kit.on_moved;ai=Kit.pic_size;aR=Kit.put_var;ar=Kit.save_min;at=Kit.save_pos;D=Kit.set;j=Kit.set_text;bk=Kit.show_window;T=Kit.text_w;Q=Kit.veil;aa=Kit.was_clicked;bl=Kit.where_text;U=Kit.with_tip;bm=Kit.write_safe;aS=Kit.zone_up;bx="ultima";bz="Ultima Tracker";bn=re.compile(r"\bthe\s+[a-z]",re.IGNORECASE);aj={"murderer":"red","criminal":"grey","gray":"grey","enemy":"orange","innocent":"blue","ally":"green","invulnerable":"yellow"};aT={"murderer":34,"criminal":946,"gray":946,"enemy":144,"innocent":89,"ally":63,"invulnerable":53};bo=3.;aU=2000;f={};M={};I={};ab={};au=set();av=set();aV={};ac={"party":set(),"scan_at":0.};bp=("lord ","lady ")
	def z(name):
		n=(name or "").strip().lower()
		for p in bp:
			if n.startswith(p):n=n[len(p):]
		return n
	def ad(cache):
		if len(cache)>aU:cache.clear()
	ae={};bq=1.;br=[0.]
	def ak(serial):
		v=ae.get(serial)
		if v is None:
			v=bool(API.IsFriend(serial))
			if len(ae)>500:ae.clear()
			ae[serial]=v
		return v
	def bs(now):
		if not 0.<br[0]-now<=bq:ae.clear();br[0]=now+bq
	def p(m,a):
		try:return bool(getattr(m,a))
		except Exception:return False
	def bA(mob,serial,name,low):
		if low.startswith(bp)or z(name)in f or low in I or serial in ac["party"]:return True
		if p(mob,"IsRunning")or p(mob,"IsMounted")or p(mob,"InWarMode"):return True
		return ak(serial)
	def bB(mob,serial,name):
		if serial in au:return False
		b=name.strip().lower()
		if bA(mob,serial,name,b):ad(au);au.add(serial);ab.pop(serial,None);return False
		if b in bE()or b in av:return True
		c=time.time();a=ab.get(serial)
		if a is not None and(a[0]or c-a[1]<bo):return a[0]
		e=bt(mob);d=bool(bn.search(e.split("\n")[0]+" "+name));ad(ab);ab[serial]=(d,c);return d
	def bt(mob):
		try:return str(mob.NameAndProps(False)or "")
		except Exception:return ""
	def bC(mob,serial,name):
		if serial in au:return False
		b=name.strip().lower()
		if not b:return False
		a=b in av
		if not a:
			d=time.time();c=aV.get(serial)
			if c is not None and(c[0]or d-c[1]<bo):a=c[0]
			else:e=bt(mob).split("\n")[0].strip().lower();a=e.startswith(b+" the ");ad(aV);aV[serial]=(a,d)
		if not a:return False
		if b in I or z(name)in f or serial in ac["party"]or ak(serial):return False
		return True
	def aW(mob,serial):
		a=p(mob,"IsDead")
		if not a and not(p(mob,"IsHuman")or p(mob,"IsGargoyle")):return
		if p(mob,"IsRenamable"):return
		b=V(mob)
		if b=="invulnerable":return
		try:c=str(mob.Name or "")
		except Exception:return
		if b=="innocent":
			if bB(mob,serial,c):return
		elif not a and bC(mob,serial,c):return
		return(b,a,c)
	def aw(m,a):
		try:return getattr(m,a)or 0
		except Exception:return 0
	bD=("0aaron2sin1ba2bott3y2del3iel2el4la3y2igail3jah3na3ona3ra2ner2ra4h5am4n2sinthe1cacia3nit4tha2calia2e3lin2hen3illes2kerley1da3ir3lia3m3ra2di4son2eben3laide4e4ia5ne4le3m3na3res3sina2ie3mina3ran3va2lai3er4y2mon2olph3n4cia4ia5s3ra2rian4el5nne1elina2neas1fina2ra3ika2ton1gate4ha2nes2ustin1hara3ve2earn2imsa2mik2ren1ida4n2ella2ken3o2la3een3sa2mee4ry2n3a3hoa3sley3tzane2rlia2sling6n2tan3hne2yana1jara3y4i2inora1kako3la3ndo4ke3sma2baar2ela4lo2il4ah4i5na3na2shay1laina3ke3la3manada3n4a4d4i4na4o3qua3ric3stair3vda3zne2ben4rt6a3inka2cander3ina3ott2dea4n4r5cy3rick2ec3k4a4sy3nne3ron3ser4ia4sa3thea3x4a5nder7ra8ia9na4is2fred2ger2i3a3ce4ia3da3ke3m4a3na3son4tair3ta3x3z4a2laard4n4rd3ele4n3igra4nora4son3yn2ma2odie3nzo3ysia2phonse7o2ston2tair3hea3on2ula3mit2vin5a4ta2ysa4sa6nd2zena1ma3bel3deo4i5ka5s4o3ia3la4ia3nda5ine3ra5nde6te4is3ta2bar3er3ika4s3rose2eerah3lia5na3thyst2ie4l5la3na4ta3ssa3ta4y2mon2oke3s2sden2y1nanda3stasia2celin2ders3i3ra5ianna5s4e5a5us5w5y4ies4omeda2eida3lla3mone3zka2gela5ica6ne6que5o4ni3us2i3ca3eli3sa3ta2ke4r2n3a4bel7le4marie3e4tte3ikka3ora2oki3rah3ush2sel5me3ley3on3reana2teia3hea4ony3je3oinette4nia6o2war1olani1para2irka2olline5oina3ni2ril5le1qua3ene1ra3bella7e3celi3minta3xie2cadia3her4ibald2dath3elia4n3is4th3on2eiela3lla3n3s3tha4ina2gus2i3adne4na3cia5n3el4ne3on3sta5o6tle2kin2len5e4y3in5da3o2man3en3ina5da3on3strong2ne3old4n2on2piar2sen5io2temisia3hur2una2ziki1saria2enka2h3a3by3er3ford3lan4eigh5y4in3on3ur2ia3sa2linda2pasia2ta3er5a3ra4ea4id1talanta3ra2enne3ri2halia4n3ena4ron3la2ifa2man2ta1ubrey2da3ny3rey4ianna5c3un2gustin8a6us2ra3e4k4lia3ilia4na3kene3ora2stin2tumn1va3na3sa2ella3na3rill4y2ie3s3va1xel4la1ya3luna3me3na3sha2dee2ela2iana3la3sha3ta2la2nora2una1zaleah4ia3rael2era2ha2ilea3na3ze2ora2ura0babette2cia2e2iley3ngana2ka4ri5ne2layna3bo3der4win3e4a4ndin3i4a4n5t2mbi2nan3croft3dele3e4lla3ning2ra4n3bara3clay3den4o5n3ika3nabas6y4ett5y3on3rett4y3se3t4h5olomew4on2sha3ia4l4mah3tiaan2takah3hsheba3ya2ul2vol2xter2y3ana5i4rd3lor3o3ta2zyli1ea3can3gan3man3trice6x3u4ina4mont4regard2cca3k4y2delia2l3ana3don3en3ina5da4ta3lanca4e3ora2m3an2n3edict4n3jamin3nett3son3t4e4ley4on2radine3enger3gren3illa4t3k4eley3nadette5rd4ice3sh3t4hold4on4ram3yl2ss4ine2ta3h4ana6y3ony3ty2ulah2val4n3erly3in1ialy3n4ca2lal3lie2na3dy3ti2rdie3kita2shop2talo2xenta1jorn1lade3ine4r4se3ke3nche4da3z2enda2iss2orn2y3the1o2den2gart2hdan6a2lton2namy3d3ita3nie4y2oker3ne2rden3gny3is2tan2wie3man2yce3d4en1rad4en4ford4ney4y3ina3m3n4d5eis5i5on5y4t3xton3y3z4il2en4cis4da6n5on4na6n4t5an3t4t5a3wster2iac4n5d3ce3dget3e4g4r4tta3git6te3na4ley3ona5y3shen3tes4ta6ny2ock3derick4ny4y3nson4t4wyn3oke2uce3no3tus2yan5t3ce3nn3son1ucia3k2d3o2rgess3han3ian3ke3l3r3ton1yran3on0cadence4o3or2edmon2ilan3mile3n4e3tlin4rin2la4ndia6ra3der4well3eb4ndonia4y3ida4sta3la5n4ia5dora5e3tha3vin3ypso2m3den3elia4ron3ilia5le2nace3dace5n4ida6e4ra3tara4on3ute2oimhe2pri5ce2ra4doc3den3esse4y3i4na5e4ssa4ta3l4a4een5n4in6g4o5s5ta4ton4y3ma4el6ina5n3na4elian3ol5ina7e5yn4n3r4ick5e4ocio5ll3son3ter3ver3yn2sey3ilda3per3sandra4ia5dy5us3ta5lia4el2talina4va3erina3herine4leen4y3o4n3riona2van2yla1eara3sar2cania3il5ia2dric2landine3este3ia4na3lia2mal2relia1had4wick3im4tra3l4e4mers3nah4da5er5i5ler5ra4e5l5y4na5ing4tal3pin4man3ris6sa5ty4les5otte5ton4maine3se4tity3tha3uncy3va4iva3y4a4ton2elsea3n4ey4oa3rica6e5e4yl3sna4ter3t3valier2iara3ka4e3lali3mlis3n3po2loe4ris2o2rista7ble6ian7na8e6oph9er7s6y2uck2you1ia3nnait3r2cely4ron2ndy2ro1laire3ra4ence4inda5ssa4k3ude6tte5ia6ne3y4ton2ement7ina9e3veland2iantha3fford4ton3nt5on3ve2orinda3ver2yde1ochiti2dy2lby3e4ene4man4tte3in3lin3on3ton2man2ndon3nie4or3rad3stance7za4uela3way2ra4lie4zon3bett5y4in3coran3deali5ll3etta4y3i4nna4s3liss3nelius3rine3t4ney2ty2urtland1raig3ndall2eighton3scent4sida2ispin2osby2ystal1ullen4in3ver2rran3tis1ybele3il2nric3thia2prien2rano3ene3il5la3us2theria0dabria2cey3ia4e4o2e2g3an3mar3na2i3ly3sel4y2karai3ota2le3ila5ia3lin3ton3y2mara3ek4n3ian4en4on4tri3on2na3e4tt3ia4el6la4or3nik3te3yelle2phene4ne5ie2r3a4lis3by3en3ia4en4o3la4ene3nell3rel6l5n3yl2sha2vene3id4n5e4s4ta2wn2ya3na1eacon3n4a4dra2b3ra2cker2de2e3dee2ianira3ene3rdre2lana5ey5o3bert4in3ia4cia4lia3la5n3more3phina3sin2man3be3i4tria3psey5ter2na3by3ice3nis4ys3ton3ver2r3ek3rick4y2va4ki4l3erell3i4n3lin3net3on2wey1iamanta3ne4the2ederik4re3go3lla3ter2llian4on4y3ys2mitri2nah2onne2rk2sa2ta3i2xie1obry2die2lores2minic7k6que2na4ld4ta5ien5o3ielle3nelley7y5r3ovan2oriya2phina2ra3een3inda4s4thy3on3y2ugie4las7s2v2yle1rake2ew2ina2ucilla1uane2gan3las2lcie5nea2ncan3stan2rand3riken2san3tin4y2tch1wayne2ight1yami3n4i3stro2lan2mas3phna2na0eamon2rl4e3tha2ster2ton1bony1cho1dan4a2gan4r2ie3son3th2lyn2mund2na2olie2ria4n2ward3in5a1fia1gan1ileen2nar2rene1lad3ine3na2den3roth2ek3ora2i3anor4s3jah3na3sa4e4ka4sa3ta3za5beeth2kan3e2la3e4n4ry3iot6t4s3sworth3y2mer3o2odie3ise2sa3ie3ton2ton2wood2ynor3se4ia1ma3jane3lia3nuel2ber2elie4yne2il4io4y2ma3ett2o1ndora2gracia2id2och3la2rico4que2ye1phraim1rasma2ek2ianthe3c4a3k3n2lina2nest2ol2rol2skine2wand3in2yx1skarne2merelda2peranza2sien2ta3eban4lle3her3u1tain5a3nthe2han2ta1udocia2gene5ia2lalia2stacia1va3csa3dine4ne3n4der4geline4the2e3lyn3rett2ita2onne2zen1yota1zekial2ra0fabienne4o2ifuza3nche3rfax3th3zah2llon2ntine2rha3ima3ley3rah4ell2tin2wne2xon2y3e3ina3me1elcia3icite7y4x2mi2nn3ton2rgus3idwyn3n3onia3ran4is1ielding2lbert3inda3more2na3lay4ey3n4igan3ola2ona3renza2sk2tzgerald1lavia2eta4cher2indo4t2ora4ence3yd2ynn1orbes3rest3sythe2ster1rances7ca5ine6s7ca4ek4k5lin3sier3zer4ier2ed4a4erica8k3mont3ya2ida3eda3tz1uller3ton2scienne0gabe3riel7la8e2ge2ia3l2latea3en5o3i4na3vin3ya2mble2na3esa3non2reth3field3gan3ner3rett4ick5dan5son5tt3th3vin3y2spar3ton2uri2vin3rie2ye3le4ord3nor1elasia2mma2nevieve2off5rey6y3gia3rge6anne6tta8e5iana2radline4ldine4rd3da3ik3main3ri4y3trude2va1hislaine1iacinta3nina2deon2gi2lana3berto3da3en4s3lian2n3a3ger3ton2selle2tana3ha2von2zane1leda3n4n5a5o5ys1odfrey2lda4ie2rdon4y3man2tzone1race4ie3dy3ham3inne3m3nger4t4ville3yson3zia2ear3g4er4or6y3sham3ta4chen4te2iffen5ith1uilhem2nnar3ther2s3tave2thrie2y1wen4dolyn4eth2ynne1ytha0hackett2dara4ssa3den3i4ya3ley3rian2gan2idee3ley3mi2l3den4is3e4y3i4an4ma3le4ie3sey2milton3lin2na4n3k3nah4e3s2rden4y3ith3lan3man4oni3old3per3riet5son4y3t4ley3vey2sna3san3tin6gs2va2ya3den3es3lee3nes2zel1ea3th5er2ctor2i3di2laku3degarde3en5a5e3ki2nka3ning3rietta4y2rbert3man3schel2sper3ter1ilary3da3liard3ton2nda2roshi2sa1obart2gan2lden3ly3t2mes2pe2race3ton2shi2uston2ward3rence2yt1ugh3o2mphrey2nter4ley1yacinth2e2man2patia0iain1da2ola3nia1lene2ias2ona1man2ogene1ndia4ra3ra2es3z2ga3mar3ram4id1olana5the2na1ra3tze2ena4e2is2ma2vin5g2win1saac3beau5l6la3dora3iah3ura2is2leta2obel3ke2rael2tas1tzak1van4a3r2ory2y0jabari3ir2celyn3inda5the3k3ob5e3ques3son3y2da2el3n2far2gger2imie3one2ke3inda2l3a3eel2mal3es3ie4la6h4son2n3a3e4lle4t3ice4s3na4elle2rdena3ed4k3man3on3rod3via5nia5s2smine3on3per2van3ier2y3a3ne1ean4ette4ine2bidiah2d3idiah3rek2ff4rey2lani3ena2na4y3dayi4yose3ica3nettia4ifer3sine2remiah5y3olin4me5y3rilyn3zy2sse5e4ica2thro2wel2zebel1ibril2han2llian2n3a3ny3x2ro2vin1oakima3n4ne2bey3ihna2casa3elyn2di3y2el4le5iane2hann6a3n2ia2lan5ta3ene3ie4ne3on2nah4than6on3ina2ra3dan6e4on3gen3vin2seph6ine3hua3ie2tha2y3ce3e1uanita2dd3e3ith6a2lia5n6a6e4e5tta4nka4us2ma3oke2n3e3g2stin6e0kaatje2chine3lyn2din2ede3the2i3a3e3kara3li3mi3ros3ya2kra2la4din4ma4nit4re3b3e4a3i4ka4l5a4nda3kin3le4i3man3onice3yca2ma4l5a5i4ria3bo3eko3ilah5ia2nda3e4ne3iel4ka3tha3ya2pera2ra4n4yan3dal3el4n3ida4mah4sa3ka3l4a4enne4i4yn3mina3ol3sten3ylin4n2sa3ch3en3ia4nda3par3sia2te4b3herine4leen3ja3oka3rien5na2ula2veri3indra2y3a3e3in3la3sa2zia1eane3ra4ney2dar2efe3lan4in4y3nan2fira2gan2hinde2i3ko3r3sha3th2lby3da3eman3ia3l4en5y4i5e4y3sey3vin2n3an3dall4ra5ick3elm3ley3nard4edy5th4is3t4on3yangi4on2ona2pa2r3ani3by3ensa3n3ry3s4en4tan3win2sare3i4a3sie3ter2turah3zia2vin1halida5l2oury1ichi2efer3le3ran4nan2llian2m3berly3mie4y2n3eta3nel3sey3tan2ona2p2ra4n3by3ima3k3sten3ti2sa3ka3met3sa2ta2yoshi1liftin2og1ohana2lina2mor2ntar2ren4ssa1rischan4ten6r1urt1yle4r3y2na3thia2oko0lacey3ie2ethan2ila4ie3rd2keisha2la4sa2mar3ont2n3a3ce3der4on4ra3e3g3i2ra4ine4lee3i4ssa3k3ry3s2tika3onia2ura5na4el4ie5nda4yn2veda4rn6e3inia2wler3rence2zarus1ea3h3la3ndra3r2ba2dah2e2if3gh5ton3ko3la5na2land2n3a3e3non5r5x3or5a5e3sar2o3n4a5rd3ra2ron4y2slie3ter2tha3itia2v3ana3i2wis2xine1i2a3dan3m3n4a4e2bby2en2ke2la3ith3lian5e3y2mber2na3coln3da4say5ey3ette3nae4ea2onel2sa3ette2tsa2v2za1lewellyn2oyd1ogan2is2kelani2la2ni2ra3e4lei5le4n5zo4tta3i3ne3raine2tus2uis5e2well1ucas3ian4lle4ne3retia3y2dia2ela2is4a2ke4ne3ina3yan2lu2na3t2ther1ydia2le2nda4on3elle3n4da4ette2ris2sander3el3nadra0mabel2c3aria3er3hi3k4enzie2ddy3elaine5ina7e5on5yn3y2e2gan4ra3dalen8a6ine3ena5ta3gie3nus2hala5ia2i3a3da3sie3tane3zah2j2laya3colm3ik4la4na5da3ka3lory3u2mie2nco3da5ra4ek5r4isa4y3fred3gena3ning3on3si4ur3uel3ya2ra3c4ella4ia4os4us4y3den3ek4n3garet6ita4o5t4uirte3ia5h5m6a5n6a6na7e4bel4e5l5tta4ly6n4na4o4s5a5ha5sa3jani4eta4orie3k4ham4os3lene4in4o5n3mara3nie5na3sha6l7l4ten3ta4ha4i5n6a6go3vin3y4ann4beth4lou3zia2son2tai4na3eo3hea5r3ilda3rika3thew5ias2ud3ra4een4ice5ta2vis2x3ine3well2y3a3nard3on1ead3ra2da3ea2g3an4ra3han2i3ra2ka2la4nie5tha3ba3ia5n4na5da4senda5sa3linio3odie5y4sa3va2rcedes5r3edith4le3ill3le3rick5k2sha2ta2yer1ia3koda2cael3hael7a4ele6le2dori2gina3non3on3uel2ka3e3kel3os2les3licent5e3o3ton2n3a3da4el4y3er5va3ka3na4ie2ra4nda3em5ba4ya3iam4elle2ssy3ty2tchell3ena4xi3zi1oira2llie4y2na3ique3roe3te2on2rena3gan6a6ce3ia5h3ley3ris3timer4on3ven3z2tega1ukasa2rdoch6k3iel3phy1yles2ra3on0nada3ia4ne3ya2eem2ia3lah3mah2lini3ren2mazzi3i2n3a3cy3ette3tale5n2omi2pea2ra3da3mada2siche3tassia2talie4ne4sha3esa3han6iel2ysa2zirqah1eal4a4e2ci2diva2ely2il2kane2lek3l3son2ola3ma3na2ria4ne4ssa3on2stor2tti2va4da4n3ille4n2ysa1icanor3holas3ia3ola5e6tte2gel2ka3ki3olos2ls2mah2na2obe3la2ra3velli2ssa2ta4ra2xie1oah2din2e3l4ani4la2lan3ita2na2ra4h3bert3een3i4ko3ma5n3ris3ton1uri1ydia2le2rna2ssa0oakes3ley1belia1chen2tavia6us1delia4l3ra3ssa3tta5e2ile3n3on2on1gden1hanna1kelani1laf3the3yinka2esia2ga2iana3n4da3ver5tte4ia1mar1na2ida1pal2helia1ralie3ne2dano2en4da2iana5na3el3ole4n2lantha2man5d2nidaa2rin2son2ville1scar2good2mond1tis2to1wen0paco2ige2kuna2lmer4iera3oma2mela2ndita4ora3thea4zike3ya4in2olo2ris3ker3nell2scal6e2tamon3ia4ence3ricia6k3sy3terson4on2ul4a4ette4in6e2vel3la2xton2yton2zia1earce4l2der2g3gy2lagia2mba4roke2nda3elope3inna3n4y3thea2ony2rcival3dita3ouze3ry3sis2ter3ra2yton1haedra2earcy3dra2ilip4lip7pe4omena2oebe4nix2ylis4lis1ia2er4ce4re4son2la4n2per1laton1olly3oma2rche3ter4ia1rentice3scot7t4ton2iscilla2udence4y1yrena2thia0qamra1ueena3lla3nby4tin5on2illan3ncy4lan4n4tina3terie0rachel2d3cliffe3ella3inka3man2e2fael3ferty2gnar2i3don3zel2leigh3ph2miro3la3on5a3say4ey3ya2nard3ce3dall4ie4olph3e4e4n3ger3i3kin2oul2phael2quel2shida3ine2tri2ul2ven3i4d2wnie2y3mond3na4ell4or2ziya1eade2ba3ecca2dford3mond2ed3se3ve2gan3ina6ld4s2idun2mington3y2na4ldo4ta3dor3e4e3fry3ny2uben2x2yhan1hea3tt2iamon4nne6on2oda5nthe3nda4na2ys4sa1ia3ne2ca4rdo3hard4ter3o2der3gley2gby2hana2kki2ley2mon2ngo2o3dan3rdan2sa2ta2va1oanna3rke2bert6a6o3i4n3yn2chelle3kwell2d3erick3man3ney3rigo2ger2hanna2i2land3dan3f2na4ld4n2oney2rie3y2sa4lind8a8e7e4nne3coe3e4anne4marie7y3s2th2wan3ena3land2xana5ne2y3ce1uben3y2dd3i3yard2fus2mer2nako2skin3s4ell3ty2th4ann4erford3ledge1yan4n5e2ba2der2lan2ssa0saba3ina5y4rah3ra4ina2cha4i2de3ira2ffi3iya2gara2hale3en2idah2kari3inah3ti3ura2lihah4m5ah4na3ly3oman5e2m3antha4ra3ien4rah3mon3son3uel2ncia3ders4ia4on5r4ra5ine4ya3ford2ra4h4i5d3ee4na3gent3i4sha3ngin3ojin2sha4enka2tinka2ul3nders2vanna2wyer2xon1chuyler2otia4t1ean3rlait3son2basten6ian7en2ema2if2la3by3ena3ina3ma2mele2non3ta2rafina3gio3ilda2sha2th2ung2verin3ilin2ward2ymour1haine3kira4o3mmara3na5ta4dra5y4e4i4ley4na5on4tay5ha3rman4on4ri3shi3wn3yndel2ea3ba3ena3ffield3ila3la4by4don4ley5y3n3ridan4man4ri4win5ood2ika3n4a4g3ra4ley2obi3shana2unnar1ibley3ongile3yl2dney3onia3ra2egfried3rra2gourney2ham2las3eas3va4ia2mba3on5e2ne4ad2obhan2ran3ena3oun2tara3embile2v3an3e1kip2yler1lade2evin1mith1ofi2lana5ge3edad3ita3omon2ndra3ia3ja3ya2phia5e4ronia2rgan2terios1palding2encer4ser2ica1tacey4ia4y3ndford4ley4ton3sio2efan6ia3lla3phan7i8e5en3r4ling3sha3van4e5n3wart2ockard3ke3rm3yan2rom2uart1ubrey2katai3i2laiman3lican2mi3mer3ner2n2san5na2therland3ton2zanne1ven3tlana1ybil2delle3ney2eira2lvester4ia2na3ia0tab3ari3itha2ci4ta2d3i2ffy2hirah2i3ma3nn3pa3te2jo2ka4ra3iyah3oda2lasi3bart4ot3e3ia4tha3lulah3man3os2m3a4ra5y3ma4y2naka3ek3i3ner3o3sy3ya2o2ra3o2te3yana2urin2wnie4y2yce3lor1eague2hya2kla2m3ina2rence5tia4se3rence4ill6yn4y3tia3yn2sia3s4a1haddeus4ea3i4s3lassa4ia3man3n4a4e4os3ra2ea3kla3lma3obald4dore6sia4ne3ra4on2ierry3rza2omas3ra4pe2urston2yra1ia3ra2balt2enette3rnan5ey4ra2ffany2lda2mandra3othy2na2ponya2rza2tus2vona1obey3ias3y2d3d2la2mas2ng2r3a3i4n3rance3y2sia2ve2wnsend1racey4y3vers4is2easa3main7e3nt3sa3va4or3y2ianon3cia3lby3na4d3sh5a4tan2oy2udy2yne3on3phena1ucker2lly1yee2ler2mon2ne2rone0ula3ni2tima1ma1na2dine1pton1rania2iah4n5a2sula1ta0vala3entina4ria6e4ska3onia4ra2n3ce3da3essa3ora3ya2shti2ughn1eda2lika3ma2nesssa2ra3ena3ity3n4on3onica2sta2vila1ictor6ia2donia2ncent3son2olet6ta2rgil5nia3idis2to2veka3ian1lad4imir1okes2leta3f1rinda0wade2gner2kanda2lden4o3ker3lace4y3ter2nda3eta2rd3ner3ren2tson2ylan6d4on3ne1ebb3ster2ndell4y2sley3ton2ylin1hilhelmina3taker4ney1ijdan2lfen3l4ard4em4iam4ow3ma3ona3son2nda3ema3ifred3na3ona3ston3throp1lby1oody1yatt2nee3n3ona0xanthe2veria3ier6a1ena3ia3os2rxes1imen5a1ylia3ona0yachne2kecan2le2ncey3ice2rdley3in3milla2smeen4in1elinda2nene2rik3o3vant2smina2tta2va1okiko2landa3ie2nina2rk2vela1usuf1vella3s3tte2onne0zachariah6y3kery2da2hara3irah3ra2id4e2kia2lea3ika3tana2ndra3e3iel3n2ra4h3ed4k2za1ehava2ke2lda3enka3ia3la2na4ide3ia3on2rlinda2va3ida1ia3zan2gana2la2na3nia2on2ta2ven1oe2la2na2ra4h3da3n2sia1uleika4ma2za4nny");bu=[None]
	def bE():
		a=bu[0]
		if a is None:
			a,b=set(),""
			for d,c in re.findall(r"(\d)([a-z]*)",bD):b=b[:int(d)]+c;a.add(b)
			bu[0]=a
		return a
	def bv(name):return Kit.checksum(name.lower().encode("utf-8"))if Kit.streamer and name else 0
	def F(name,serial=0):return Q("name",name,serial or bv(name))
	def af(name,serial,noto):a=aP(noto);return(a+" "if a else "")+Q("name",name,serial or bv(name))
	def bF():
		fK="ultima";bD="Ultima Tracker";fL=bD+":";cn=.25;fM=.15;fN=.05;fO=.45;bS=85;dj,dk=50,200;dl,dm=1,24;fP=32;dn=210;do=90;fQ=200;fR=18;fS=12;d4=14;fT=8;d5=220;fU=16;fV=11;b1=170;cG=600;cH=1;dp=10;dq=5.;dr=12;d6=18;fW=20.;fX=12;fY=2;fZ=("invulnerable",);f_=("innocent","ally");f0=[API.Notoriety.Gray,API.Notoriety.Criminal,API.Notoriety.Enemy,API.Notoriety.Murderer];d7="ultima.foe";f1=743;ds,dt=1,60;cI=2000;f2=200;du=60.;d8=30.;cJ=12;d9=30.;f3=5365;dv=60.;f4=60.;f5=6;f6=40;ea=30.;eb=160;f7={0:"Fel",1:"Tram",2:"Ilsh",3:"Malas",4:"Tok",5:"TerM"};dw=(("All players",None),("Red only",("murderer",)),("Grey only",("gray","criminal")),("Orange only",("enemy",)),("Blue only",("innocent",)),("Foe list","foe"));dz=(("Last hour",3600.),("Today","today"),("All time",None));dA="UltimaTracker_sight_pos";cK="UltimaTracker_sight_min";cL="UltimaTracker_sight_open";dB="UltimaTracker_killer_pos";dC="UltimaTracker_killer_min";f8=.5;cM=6;cN=("friend","foe","neutral","combat","panel");f9=4;ga=10;dD=5000;gb=4000;ec=4000;gc=1.;bc=6;gd=24;ed=13;ge=20;co="#3A3A3A";cO="#5E4E24";ee="#DDDDDD";gf="#F0C850";gg="#A8A8A8";cP="#DDDDDD";cQ="#999999";gh="#7D6E52";ef={"friend":"Friends","foe":"Foes","neutral":"Neutral","combat":"Combat"};eg={"friend":"#5CE65C","foe":"#FF5050","neutral":"#9EC8FF","combat":"#FFB050","panel":"#FFD966"};cp={"friend":"#3AA0D4","foe":"#D93030","neutral":"#B8B8B8","combat":"#B32D2D"};cR="#2E9E3A";eh="#FF2020";gi=50;gj=1.2;ei,gk=.1,.55;ej=32;gl=.1;ek="#B8902A";el="#2A8C9E";em="#D8CCB0";en=3617;gm=1;gn=3.;go=3.5;cS="#3A6FD8";eo="#21A39A";dE="#555555";gp={"innocent":"#4FA3FF","ally":"#40E040","gray":"#B0B0B0","criminal":"#B0B0B0","enemy":"#FF9A2E","murderer":"#FF4040","invulnerable":"#FFE14D","unknown":"#DDDDDD",};gq,gr=10,18;gs=a6;gt=aq;gu=aq;cq=3;gv=aI;ep=2092;gw=.6;gx=(aE[0],a1[0]);gy=(2103,2104);dF=1153;gz={co:0,cO:53,ek:53,el:89,em:0,cR:63,cS:1152};gA=[((235,235,235),1153),((150,150,150),946),((225,55,55),34),((70,220,70),63),((90,150,255),89),((255,155,45),144),((255,220,80),53),((25,25,25),0)];bO=a9("_ultima_tracker_data.txt");eq=os.path.join(Kit.script_dir(),"_player_tracker_data.txt");bE=["friend","foe","neutral"];er={"scale":(dj,dk),"opacity":(0,100),"range":(dl,dm),"alert_minutes":(ds,dt),"sort":(0,2)};es=("scale","opacity","range","alert_minutes","sort");et=("name","distance","HP");eu=("sync","magery","combat_shown","combat_only","healing","borders","alert_red","alert_foes","alert_orange","alert_gray","sightings","killer");dG={"friend":[40,140,240,220,False,False,bS],"foe":[290,140,240,220,False,False,bS],"neutral":[540,140,240,220,False,False,bS],"combat":[300,200,d5,0,False,False,bS],"panel":[40,380,0,0,False,False,bS],};aN={ir:list(it)for ir,it in dG.items()};au={"scale":100,"opacity":bS,"range":18,"sync":False,"magery":False,"combat_shown":True,"combat_only":True,"healing":False,"borders":True,"alert_red":True,"alert_foes":True,"alert_orange":False,"alert_gray":False,"alert_minutes":5,"sightings":True,"killer":True,"sort":0};ev=dict(au);gB={"dirty_save":False,"foe_ver":0,"combat_loaded":False,"shutting":False,"started":False,"loaded":False};a0={"minimized":False,"shutting":False,"docked":False,"queue":[],"dirty_save":False,"foe_ver":0,"combat_loaded":False,"started":False,"loaded":False,"party":set()};im={"g":None,"c":{},"store":({},{})};ca,io,aV=aK(a0,bD);br={};cr=[];dH=[];cT=u+30+J;ew=2*u+30
		def gC(*a):dH.append(True)
		bT={};bu={};bF=[];bv={};bd={};bn={"ver":0,"seen_ver":0,"dirty":False,"save_at":0.};cb={};cs={};ct={};cU=set();bx={};bU=[None]
		def sc(v,scale=None):s=au["scale"]if scale is None else scale;return max(1,int(round(v*s/100.)))
		gD=13;dI=20
		def cV(s):return s if s>1. else 1.
		def cW(v):return Kit.tsize(sc(v)if au["scale"]>100 else int(v))
		def ex(text,width):width=max(20,int(width));return[C(a,width)for a in Kit.wrap(text,width)]
		def ey(parent,lines,x,y):a=c_(cQ);return[S(B(parent,c,x,y+b*dI,a))for b,c in enumerate(lines)]
		bb={"req":False,"size":{},"own_size":{},"force":set(),"made":{}};gE=3
		def ez():
			for k,v in dG.items():aN[k]=list(v)
		def eA():bq.clear();au.update(ev);bb["req"]=False;bp["serial"]=None;ez()
		def bP(v,lo,hi):return max(lo,min(hi,v))
		def cu():return API.StopRequested
		def dJ(text,n):return text if len(text)<=n else text[:max(1,n-2)]+".."
		def cv(text,size,color,**a):return S(API.Gumps.CreateGumpTTFLabel(text,size,color,**a))
		def b2(opacity,color):return S(API.Gumps.CreateGumpColorBox(opacity,color))
		def bV(b,a):
			try:b.SetAlpha(a)
			except Exception:pass
		def bM(c):bG.pop(id(c),None);K(c)
		cX=[];gF=.15;cc={}
		class RowClick(object):
			__slots__=("row","make")
			def __init__(self,row,make):self.row,self.make=row,make
			def bind(self):
				r=self.row;b,c=r.serial,r.name;a=r.prev
				if a is not None and time.time()-a[2]<gF:b,c=a[0],a[1]
				if b is None:return
				return self.make(b,c)
		def gG():return{"alt":al(),"shift":bool(aX("shift"))}
		def bt(fn):
			def a(*a):
				f=fn.bind()if type(fn)is RowClick else fn
				if f is not None:cX.append((f,gG()))
			return a
		def eB(c,fn):Kit.on_click(c,bt(fn))
		def gH():
			while cX:
				a,b=cX.pop(0);cc.clear();cc.update(b)
				try:a()
				except Exception as c:
					if an():return
					cd(c)
				finally:cc.clear()
		def cd(b):
			a=str(b)
			if a not in bC["errors"]:bC["errors"].add(a);aV("error (still running): "+a,l)
		ce=[False];cw=[];cf=[]
		def eC(q):
			while q:
				a=q.pop(0)
				try:a()
				except Exception as b:
					if an():return True
					cd(b)
		def bQ(x,y,w,h,fn,tip=None):c=API.Gumps.CreateGumpColorBox(.01,"#000000");c.SetRect(x,y,w,h);eB(c,fn);return U(c,tip)
		def cY(graphic,x=0,y=0,hue=0):return S(API.Gumps.CreateGumpPic(graphic,x,y,bg(graphic,hue)))
		def bK(graphic,w,h,hue=0):return S(API.Gumps.CreateTiledGumpPic(graphic,max(0,w),max(0,h),bg(graphic,hue)))
		def gI():
			bu.clear();e=bu["icons"]={}
			for f,b in(("lock",(ep,ep)),("min",gx),("opacity",gy)):
				c=[ai(i)for i in b]
				if all(g and k for g,k in c):e[f]=list(zip(b,c))
			d="Name the 75% PSN 12y Foes (3)";a=API.Gumps.CreateGumpLabel(d,dF);w,h=int(a.GetWidth()),int(a.GetHeight());a.Dispose()
			if w>0 and h>0:bu["char_w"]=w/float(len(d));bu["font_h"]=h
		dK={};eD=dict(("#%02X%02X%02X"%a2[iu],Kit.CB_HUE[iu])for iu in a2)
		def cZ(noto,default):return Kit.cb_hex(noto,gp.get(noto,default))
		def c_(color):
			if Kit.cblind and color in eD:return eD[color]
			h=dK.get(color)
			if h is not None:return h
			c=color.lstrip("#");r,g,e=int(c[0:2],16),int(c[2:4],16),int(c[4:6],16);a,b=dF,None
			for(f,i,j),k in gA:
				d=(f-r)**2+(i-g)**2+(j-e)**2
				if b is None or d<b:a,b=k,d
			if len(dK)<256:dK[color]=a
			return a
		eE={}
		def gJ(color):
			v=eE.get(color)
			if v is None:c=color.lstrip("#");v=eE[color]=(int(c[0:2],16),int(c[2:4],16),int(c[4:6],16))
			return v
		def c0(size):return "char_w"in bu and gq<=size<=gr
		def gK(size):return bu["char_w"]if c0(size)else size*.58
		bG={};eF=[ec]
		def bH(text,size,color,aligned="left",maxWidth=0,applyStroke=False):
			if applyStroke or not c0(size):a=cv(text,size,color,aligned=aligned,maxWidth=maxWidth,applyStroke=applyStroke);bG.pop(id(a),None);return a
			if len(bG)>eF[0]:
				for k,v in list(bG.items()):
					if v[0].IsDisposed:del bG[k]
				eF[0]=max(ec,2*len(bG))
			text=eG(text,maxWidth);a=S(API.Gumps.CreateGumpLabel(text,c_(color)));bG[id(a)]=[a,aligned,maxWidth,size,0,0,text];return a
		def dL(a):m=bG.get(id(a));return m if m is not None and m[0]is a else None
		def eG(text,a):
			if a and len(text)*bu.get("char_w",7)>a:return dJ(text,max(2,int(a/bu.get("char_w",7))))
			return text
		def bz(b,x,y,text=None):
			m=dL(b)
			if m is None:b.SetPos(x,y);return
			m[4],m[5]=x,y;d,a,f=m[1],m[2],m[3]
			if text is None:text=m[6]
			e=int(len(text)*bu["char_w"]);c=0
			if a and d=="right":c=max(0,a-e)
			elif a and d=="center":c=max(0,(a-e)//2)
			g=int(round((f*1.35-bu["font_h"])/2.));b.SetPos(int(x+c),int(y+g))
		def bR(a,text):
			m=dL(a)
			if m is None:a.SetText(text);return
			text=eG(text,m[2])
			if text==m[6]:return
			m[6]=text;a.Text=text
			if m[1]!="left"and m[2]:bz(a,m[4],m[5],text)
		def eH(a,color):
			if dL(a)is None:return False
			a.Hue=c_(color);return True
		def eI():return bool(cc.get("shift")or aX("shift"))
		def bN():return cc.get("alt")or al()
		def gL():return[a for a in bE+["combat","panel"]if H("hub"if a=="panel"else "ultima."+a)]
		def c1():return bool(SNAP.drag)or SNAP.pressed()is True
		c2={};gM=2000
		def c3(text,px,size,smooth=False):
			if size>gD and(smooth or not c0(size)):b=size*.6 if smooth else gK(size);return dJ(text,max(4,int(px/b)))
			k=(text,px);a=c2.get(k)
			if a is None:
				if len(c2)>gM:c2.clear()
				a=c2[k]=C(text,max(10,int(px)))
			return a
		def cg(top,h,font):return top+max(0,int((h-font*1.35)/2))
		def b3(parent,x,y,w,h,text,fn,tip=None,face=co,color=cP,font=12,store=None):
			f=bK(gv,w,h,gz.get(face,c_(face)));f.SetPos(x,y);color="#141414";parent.Add(f);a=bH(text,font,color,aligned="center",maxWidth=w);bz(a,x,cg(y,h,font));parent.Add(a);c=bQ(x,y,w,h,fn,tip);parent.Add(c)
			if store is not None:store.extend([f,a,c])
			return a
		def c4():return(2 if au["magery"]else 0)+(1 if au["healing"]else 0)
		bW="Alt+click: auto-follow (again to stop)";gN=("Cast Heal on %s (Shift+click: Greater Heal). Alt+click: auto-follow (again to stop)");gO=("Cast Cure on %s (Shift+click: Arch Cure). Alt+click: auto-follow (again to stop)");gP="Bandage %s when adjacent; farther away, follow them (again to stop). "+bW
		def eJ(parent,x,y,w,h,serial,name,store=None,row=None):
			j=max(7,int(h*.7/min(1.,au["scale"]/100.)));e,b,f=[],[],[]if store is None else store
			if au["magery"]:
				for c,g,i,a,d in(("H","Heal","Greater Heal",gN,ek),("C","Cure","Arch Cure",gO,el)):b.append((c,fw(serial,g,i)if row is None else RowClick(row,(lambda a,st:lambda s,n:fw(s,a,st))(g,i)),a,d,"#FFFFFF"))
			if au["healing"]:b.append(("B",eM(serial,name)if row is None else RowClick(row,eM),gP,em,"#202020"))
			for c,k,a,d,l in b:b3(parent,x,y,w,h,c,k,a%F(name,serial),face=d,color=l,font=j,store=f);e.append((f[-1],a));x+=w+2
			return e
		def eK(s):return max(16,int(round(gd*s)))
		def eL(s):return max(16,int(round(ge*s)))
		def gQ(serial):
			if safe(ag)==serial:return True
			return Follow.start(serial,bD)
		def ch(serial):ax(serial,bD)
		def cx(serial,fn):
			def a(*a):
				if bN():ch(serial)
				else:fn()
			return a
		bp={"serial":None,"name":"","state":None,"until":0.,"follow":None}
		def cy(serial):
			if serial is None or bp["follow"]!=serial:return
			bp["follow"]=None
			if safe(ag)==serial:Follow.stop(bD)
		def eM(serial,name):
			def a(*f):
				if bp["serial"]==serial:bp["serial"]=None;bX("bandage");cy(serial);aV("stopped bandaging %s; cursor released."%name,A);return
				try:
					a=API.FindMobile(serial)
					if a is None or bool(a.IsDead):a=None
					else:b=API.Player;d=max(abs(int(a.X)-int(b.X)),abs(int(a.Y)-int(b.Y)))
				except Exception:a=None
				if a is None:aV("can't bandage %s (out of sight or dead)."%name,l);return
				if d>gm:
					if bp["follow"]==serial and safe(ag)==serial:cy(serial);aV("stopped following %s."%name,A);return
					e=safe(ag)!=serial
					if not gQ(serial):return
					if e:bp["follow"]=serial
					aV("following %s; press B again when adjacent."%name,o);return
				c=API.FindType(en,API.Backpack)or API.FindType(en)
				if not c:aV("no bandages in your backpack.",l);return
				if bp["serial"]is not None or c6()is not None or API.HasTarget("any"):aV("a target cursor is up; clear it, then press B.",l);return
				API.UseObject(c);bp.update(serial=serial,name=name,state="cursor",until=time.time()+gn);eN("bandage",go)
			return Kit.once(cx(serial,a),("ultima.bandage",serial),Kit.TWICE)
		c5="ultima";b4={"bandage":False,"spell":False}
		def eN(what,a):b4[what]=True;HOST.claim_cursor(c5,a)
		def bX(what):
			if not b4.get(what):return
			b4[what]=False
			if not any(b4.values()):HOST.release_cursor(c5)
		def c6():return HOST.cursor_busy(c5)
		def eO():
			a=c6()
			if a is not None and a!="pick":return False
			return bool(API.HasTarget("any"))
		def gR():
			s=bp["serial"]
			if s is None:bX("bandage");return
			c=bp["name"]
			try:b=API.FindMobile(s);a=b is None or bool(b.IsDead)
			except Exception:a=True
			if a or time.time()>bp["until"]:bp["serial"]=None;cy(s);aV(("can't bandage %s (out of sight or dead)."if a else "no target cursor for bandaging %s.")%c,l);return
			if bp["state"]=="cursor"and b4["bandage"]and HOST.cursor_ok(c5,"beneficial"):API.Target(s);bp["serial"]=None;bX("bandage");cy(s)
		def gS():
			safe(ag);s=Follow.serial
			if s is not None and aB(s)is None:Follow.serial=None
			if bp["follow"]is not None and Follow.serial!=bp["follow"]:bp["follow"]=None
		eP=((3,4,3,8,"#FFFFFF"),(6,4,3,8,"#A0A0A0"),(9,4,3,8,"#5A5A5A"));gT={("lock",True):((3,8,10,6,None),(7,10,2,2,cO),(4,2,8,2,None),(4,2,2,6,None),(10,2,2,6,None)),("lock",False):((3,8,10,6,None),(7,10,2,2,co),(4,0,8,2,None),(4,0,2,8,None),(10,0,2,3,None)),("min",True):((4,4,8,2,None),(4,4,1,8,None),(11,4,1,8,None),(4,11,8,1,None)),("min",False):((4,10,8,2,None),),("opacity",True):eP,("opacity",False):eP}
		def gU(add,d,x,y,a,kind,on):
			u=a/16.
			def R(v):return int(round(v*u))
			def S(v):return max(1,int(round(v*u)))
			e=(gf if on else gg)if kind=="lock"else ee
			for f,g,h,i,j in gT.get((kind,bool(on)),()):add(x+R(f),y+R(g),S(h),S(i),j or e)
			if kind=="close":b=max(8,int(a*.8));c=cv("x",b,ee,aligned="center",maxWidth=a);c.SetPos(x,y+max(0,int((a-b*1.35)/2)));d(c)
		cz={};bY=[]
		def eQ():
			for c in list(bY):
				if c.gump.IsDisposed:bY.remove(c)
				else:c.frame.apply_borders()
		class Frame(object):
			def __init__(self,gump):
				self.size=(0,0);self.center=bK(gt,1,1);gump.Add(self.center);self.edges=[bK(gs+(1 if a in(0,1)else 3),1,1)for a in range(4)]
				for b in self.edges:gump.Add(b)
			def layout(self,w,h):
				self.size=(w,h);a=[(0,0,w,bc),(0,h-bc,w,bc),(0,0,bc,h),(w-bc,0,bc,h)]
				for b,r in zip(self.edges,a):b.SetRect(*r)
				self.apply_borders()
			def apply_borders(self):
				a=au["borders"]
				for p in self.edges:bV(p,1. if a else 0.)
				w,h=self.size
				if a:self.center.SetRect(bc,bc,max(0,w-2*bc),max(0,h-2*bc))
				else:self.center.SetRect(0,0,w,h)
			def set_alpha(self,a):bV(self.center,a)
		class KitFrame(object):
			def __init__(self,gump,key=None):
				self.gump,self.key=gump,key;self.top=0;a=a6;self.s=[ai(a+b)for b in range(9)];self.kw,self.kh=ai(a3);self.fill=bK(a+4,1,1);self.center=bK(aq,1,1);self.edges=[bK(a+d,1,1)for d in(1,7,3,5)];self.corners=[cY(a+e,0,0)for e in(0,2,6,8)];self.knots=[cY(a3,0,0)for g in range(4)];self.parts=[self.fill]+self.edges+self.corners+self.knots
				for c in[self.fill,self.center]+self.parts[1:]:gump.Add(c)
				Kit._frame_parts[gump]=self.parts
			def layout(self,w,h,top=None):
				if top is not None:self.top=top
				M=u;a,t,b,l,n,r,c,f,d=self.s;self.fill.SetRect(l[0],t[1],max(0,w-l[0]-r[0]),max(0,h-t[1]-f[1]))
				for j,e in zip(self.edges,((a[0],0,w-a[0]-b[0],t[1]),(c[0],h-f[1],w-c[0]-d[0],f[1]),(0,a[1],l[0],h-a[1]-c[1]),(w-r[0],b[1],r[0],h-b[1]-d[1]))):j.SetRect(e[0],e[1],max(0,e[2]),max(0,e[3]))
				for k,g in zip(self.corners,((0,0),(w-b[0],0),(0,h-c[1]),(w-d[0],h-d[1]))):k.SetPos(*g)
				for m,g in zip(self.knots,((0,0),(w-self.kw,0),(0,h-self.kh),(w-self.kw,h-self.kh))):m.SetPos(*g)
				i=h-self.top-M;self.center.SetRect(M,self.top,max(0,w-2*M),max(0,i));D(self.center,"IsVisible",i>4)
			def apply_borders(self):pass
			def set_alpha(self,a):bV(self.center,a)
			def drop_all(self):
				for c in[self.center]+self.parts:bM(c)
				if Kit._frame_parts.get(self.gump)is self.parts:Kit._frame_parts.pop(self.gump,None)
		class Chrome(object):
			def __init__(self,gump,kit=False,key=None):self.gump=gump;self.kit,self.key=kit,key;self.frame=KitFrame(gump,key)if kit else Frame(gump);bY[:]=[a for a in bY if a.gump is not gump and not a.gump.IsDisposed];bY.append(self);self.strip=[];self.title_bg=self.title_lbl=self.slider=self.pct_lbl=None;self.title_text=self.title_color=self.title_raw=self.status_x=None;self.status_lbl=self.status_text=None;self.title_max,self.title_pos,self.font=40,(0,0),ed;self.opacity,self.content_top=bS,bc;self.on_title_alt,self.alt_key=None,None
			def _add(self,ctrl):self.gump.Add(ctrl);self.strip.append(ctrl);return ctrl
			def _clear_strip(self):
				for c in self.strip:bM(c)
				self.strip=[];self.title_bg=self.title_lbl=self.slider=self.pct_lbl=None;self.status_lbl,self.status_text=None,None
			def dispose(self):
				self._clear_strip();self.frame.drop_all()
				if self in bY:bY.remove(self)
			def layout(self,w,h,s,opacity,title,color,buttons,l,m,o,p):
				self.opacity=opacity;g=opacity/100.;self.frame.layout(w,h);self.frame.set_alpha(g);self._clear_strip();a=eK(s);self.title_bg=self._add(bK(gu,w-2*bc,a));self.title_bg.SetPos(bc,bc);bV(self.title_bg,g);q=self._add(bK(aI,w-2*bc,cq));q.SetPos(bc,bc+a-cq);b=max(12,a-6-cq);i=max(2,int(round(2*s)));n=len(buttons);e=w-bc-4-n*b-max(0,n-1)*i;j=e;self.on_title_dbl=m;self.on_title_alt,self.alt_key=o,p;self._title_catch(bc,max(10,j-bc-2),a,a4+". "+bW);r=bc+(a-cq-b)//2
				for t,u,v,x in buttons:self._button(e,r,b,t,u,v,x);e+=b+i
				self.font=max(9,int(round(ed*cV(s))));self.title_max=max(20,j-bc-10);self.title_pos=(bc+5,cg(bc,a-cq,self.font));self.title_color=color;self.title_text=None;self.set_title(title);y=bc+a
				if l:c=eL(s);d=max(8,int(round(11*cV(s))));z=self._add(bH("Opacity",d,cQ));bz(z,bc+5,cg(y,c,d));f=int(round(34*s));k=bc+int(round(54*s));A=max(40,w-bc-8-f-k);self.slider=API.Gumps.CreateSlider(A,0,100,opacity,k,y+max(2,(c-10)//2),True);self._add(self.slider);self.pct_lbl=self._add(bH("%d%%"%opacity,d,cP,aligned="right",maxWidth=f));bz(self.pct_lbl,w-bc-4-f,cg(y,c,d));y+=c
				self.content_top=y
			def _title_catch(self,xy,w,h,tip):
				a=bQ(xy,xy,w,h,self._title_clicked,tip);D(a,"CanMove",True)
				if Client.mouse is None:Kit.hook_double(a,self._dbl_once())
				self._add(a)
			def _dbl_once(self):return Kit.once(lambda:self.on_title_dbl(),("utitle",id(self)))
			def layout_kit(self,w,h,opacity,title,color,mini,d,i):
				M=u;self._clear_strip();self.content_top=cT;self.frame.layout(w,h,cT);self.frame.set_alpha(opacity/100.);e=self._add(bK(aq,w-2*M,30));e.SetPos(M,M);bV(e,Kit.SECTION_ALPHA)
				if not mini:self._add(b2(1.,color)).SetRect(M,M+30,w-2*M,3)
				a=w-M-54
				if not aS(self.key):
					self._art((a1 if mini else aE)[0],a,M+7,d,Kit.RESTORE_TIP if mini else aH);a-=Kit.DOCK_DX
					if not mini:self._art(Kit.ART_DOCK[0],a,M+7+Kit.DOCK_DY,i,Kit.DOCK_TIP);a-=10
				b=a
				if not mini:
					f="Settings";c=a-35-T(f)
					if c>M+30+T("COMBAT")+40:self._art(L[0],c,M+4,gC,a5%bD,f);b=c
				g=aS(self.key);self.on_title_dbl=(lambda:None)if g else d;self._title_catch(M,max(10,b-M-6),30,None if g else a4);self.title_max=max(20,b-M-30-10);self.title_pos=(M+30,M+7);self.title_color=color;self.title_text=None;self.set_title(title)
			def _art(self,graphic,x,y,fn,tip,cap=None):
				p=self._add(cY(graphic,x,y));a,b=ai(graphic);a,b=a or 20,b or 20
				if cap:c=B(self.gump,cap,x+a+5,y+3,N);self.strip.append(c);a+=5+T(cap)
				self._add(bQ(x,y,a,b,fn,tip));return p
			def set_status(self,text):
				if not self.kit or self.title_lbl is None:return
				text=text or ""
				if text==self.status_text:return
				self.status_text=text;x=self.title_pos[0]+T(self.title_text or "")+12;b=self.title_pos[0]+self.title_max-x;c=C(text,b)if b>20 else "";a=(x,self.title_pos[1])
				if self.status_lbl is None:self.status_lbl=B(self.gump,c,x,self.title_pos[1],o);self.strip.append(self.status_lbl);self.status_x=a
				else:
					if a!=self.status_x:self.status_x=a;self.status_lbl.SetPos(x,self.title_pos[1])
					j(self.status_lbl,c)
			def _title_clicked(self,*h):
				f=time.time();d=id(self.gump);a=(self.gump.GetX(),self.gump.GetY())
				if self.on_title_alt is not None and bN():
					b=self.alt_key;e=bq.pos.get(b)if b is not None else None;g=(b is not None and bq.moving==b)or SNAP.drag or(e is not None and(abs(a[0]-e[0])>cM or abs(a[1]-e[1])>cM))
					if not g:self.on_title_alt()
					return
				c=cz.get(d)
				if c and f-c[0]<=f8 and abs(a[0]-c[1][0])<=cM and abs(a[1]-c[1][1])<=cM:cz.pop(d,None);self._dbl_once()()
				else:
					if len(cz)>aU:cz.clear()
					cz[d]=(f,a)
			def _button(self,x,y,a,kind,on,fn,tip):
				b=bu.get("icons",{}).get(kind)
				if b:
					e,(c,d)=b[1 if on else 0]
					if c<=a+6 and d<=a+6:
						f=34 if kind=="lock"and on else 0;p=self._add(cY(e,x+(a-c)//2,y+(a-d)//2,f))
						if kind=="lock"and not on:bV(p,gw)
						self._add(bQ(x,y,a,a,fn,tip));return
				if kind=="close"and "char_w"in bu:g=S(self._add(API.Gumps.CreateGumpLabel("x",dF)));g.SetPos(x+max(0,(a-int(bu["char_w"]))//2),y+(a-bu["font_h"])//2);self._add(bQ(x,y,a,a,fn,tip));return
				h=on and kind in("lock","opacity");i=self._add(b2(1.,cO if h else co));i.SetRect(x,y,a,a)
				def j(a,by,bw,bh,col):p=self._add(b2(1.,col));p.SetRect(a,by,bw,bh)
				gU(j,self._add,x,y,a,kind,on);self._add(bQ(x,y,a,a,fn,tip))
			def set_title(self,text,color=None):
				if self.kit:
					b=(text,self.title_max)
					if self.title_lbl is not None and b==self.title_raw:return
					self.title_raw=b;text=C(str(text).upper(),self.title_max)
					if self.title_lbl is None:self.title_lbl=B(self.gump,text,self.title_pos[0],self.title_pos[1],ap);self.strip.append(self.title_lbl);self.title_text=text
					elif text!=self.title_text:
						self.title_text=text;j(self.title_lbl,text)
						if self.status_text is not None:c,self.status_text=self.status_text,None;self.set_status(c)
					return
				if color is not None and color!=self.title_color:
					self.title_color=color;a=self.title_lbl
					if a is not None and not eH(a,color):
						self.title_text=None
						if a in self.strip:self.strip.remove(a)
						bM(a);self.title_lbl=None
				text=c3(text,self.title_max,self.font)
				if self.title_lbl is None:self.title_lbl=self._add(bH(text,self.font,self.title_color or cP));bz(self.title_lbl,*self.title_pos);self.title_text=text
				elif text!=self.title_text:self.title_text=text;bR(self.title_lbl,text)
			def set_opacity(self,v):
				self.opacity=v;a=v/100.;self.frame.set_alpha(a)
				if self.kit:return
				if self.title_bg is not None:bV(self.title_bg,a)
				if self.pct_lbl is not None:bR(self.pct_lbl,"%d%%"%v)
			def poll(self):
				if self.slider is None:return
				v=bP(int(self.slider.Value),0,100)
				if v!=self.opacity:self.set_opacity(v);return v
				return
		class Anchors(object):
			def __init__(self):self.gid,self.next_gid,self.pos,self.dims={},1,{},{};self.moving,self.still,self.linger,self.saved=None,0,0,[];self.pending=self.alt_used=self.touched=False
			def placed(self,key,x=None,y=None,w=None,h=None):
				if x is None:self.pos.pop(key,None)
				else:self.pos[key]=(int(x),int(y))
				if w is None:self.dims.pop(key,None)
				else:self.dims[key]=(int(w),int(h))
				self.pending=True
			def sized(self,key,w,h):self.dims[key]=(int(w),int(h))
			@staticmethod
			def host_follows(g):
				a=set()
				if not SNAP.enabled or g in SNAP.no_snap:return a
				c,d=SNAP.links,SNAP.members;b=[g]
				while b:
					e=b.pop()
					for f,l in list(c.items()):
						if l is e and f is not g and f not in a and f in d:a.add(f);b.append(f)
				return a
			def add_group(self,keys):
				g=self.next_gid;self.next_gid+=1
				for k in keys:self.gid[k]=g
			def members(self,key):
				g=self.gid.get(key)
				if g is None:return[key]
				return[a for a,b in self.gid.items()if b==g]
			def join(self,a,b):
				c,d=self.gid.get(a),self.gid.get(b)
				if c is None and d is None:self.add_group([a,b])
				elif c is None:self.gid[a]=d
				elif d is None:self.gid[b]=c
				elif c!=d:
					for k,v in list(self.gid.items()):
						if v==d:self.gid[k]=c
				self.touched=True
			def detach(self,key):
				g=self.gid.pop(key,None)
				if g is not None:
					self.touched=True;a=[b for b,c in self.gid.items()if c==g]
					if len(a)==1:self.gid.pop(a[0],None)
			def clear(self):self.gid={};self.touched=True
			def saved_groups(self):
				a={}
				for k,g in self.gid.items():
					if k in cN:a.setdefault(g,[]).append(k)
				return[sorted(b)for b in a.values()if len(b)>1]
			def groups_changed(self):
				if not self.touched:return False
				self.touched=False;a=self.saved_groups()
				if a==self.saved:return False
				self.saved=a;return True
			@staticmethod
			def shift(m,dx,dy,a,wins):x,y,w,h=a[m];g=wins[m][0];b,c=Kit.place(g,x+dx,y+dy,w,h);bj(g);a[m]=(b,c,w,h)
			def tick(self,g):
				if self.moving is None and not self.pending and self.linger<=0 and not SNAP.drag:
					for k in list(self.gid):
						if k not in cN and not gV(k):self.detach(k)
					return
				self.pending=False
				if self.linger>0:self.linger-=1
				c=g()
				for k in list(self.gid):
					if k not in c and k not in cN:self.detach(k)
				a={s:(int(n.GetX()),int(n.GetY()),int(n.GetWidth())or q[0],int(n.GetHeight())or q[1])for s,(n,q)in c.items()if E(n)};d=gL();e=HOST.layout_arranging();b=[t for t,v in a.items()if t in self.pos and(v[0],v[1])!=self.pos[t]and t not in d]
				if b:
					k=self.moving if self.moving in b else None
					if k is None:
						for m in b:
							if c[m][0]in SNAP.drag:k=m;break
					if k is None:k=b[0]
					h=a[k][0]-self.pos[k][0];i=a[k][1]-self.pos[k][1];f=self.dims.get(k,a[k][2:])!=a[k][2:]
					if f:b=[]
					elif k in self.gid and bN():
						self.detach(k)
						if not self.alt_used:self.alt_used=True;aV("window unanchored.",A)
					j=self.host_follows(c[k][0])if b and not e else()
					for m in(self.members(k)if b and not e else[]):
						if m!=k and m not in b and m in a and m not in d and c[m][0]not in j:self.shift(m,h,i,a,c)
					if not f:self.moving=k;self.still=0
				elif self.moving is not None:
					if not SNAP.drag:self.still+=1
					if self.still>=f9:
						k,self.moving=self.moving,None
						if k in a and k not in d and not e:self.snap(k,a,c,d)
						self.linger=ga
				self.pos={w:x[:2]for w,x in a.items()};self.dims={y:G[2:]for y,G in a.items()}
			def snap(self,k,h,wins,held):
				a,b,i,j=h[k];l=set(self.members(k))
				if any(t in held for t in l):return
				e=None
				for o,(c,d,m,n)in h.items():
					if o in l or o in held:continue
					p=[]
					if b<d+n and d<b+j:p+=[(abs(a-(c+m)),c+m-a,0),(abs(a+i-c),c-i-a,0)]
					if a<c+m and c<a+i:p+=[(abs(b-(d+n)),0,d+n-b),(abs(b+j-d),0,d-j-b)]
					for q,f,g in p:
						if q<=SNAP_DIST and(e is None or q<e[0]):
							if f and abs(b-d)<=SNAP_DIST:g=d-b
							if g and abs(a-c)<=SNAP_DIST:f=c-a
							e=(q,f,g,o)
				if e is None:return
				s,f,g,o=e
				for r in l:
					if r in h:self.shift(r,f,g,h,wins)
				self.join(k,o)
		bq=Anchors()
		def gV(k):return k.startswith("pop:")and int(k[4:])in br
		import threading;dM=threading.Lock();cA=[0];c7=[None];c8=[False];b5={};b6=[None];dN=[0.];cB=[0];ci=[0.]
		def eR(fn):t=threading.Thread(target=fn);t.daemon=True;t.start()
		def eS():
			a=bO if os.path.exists(bO)else g6()or eq
			if not os.path.exists(a):return None,[]
			with dM:
				with open(a,"r")as f:b=f.readlines()
				if a==bO:b6[0]=dO()
			return a,b
		def gW():
			try:a,b=eS()
			except Exception as c:aV("couldn't read the save file (%s); saving is off this session."%c,l);return
			eU(a,b)
		def bI():
			if a8["windows"]is not None and not a0.get("shutting"):ce[0]=True
			else:da(background=True)
		def gX(line,links):f[z(line)]=line
		def gY(line,links):M[line.lower()]=line
		def gZ(line,links):I[line.lower()]=line;cE[0]+=1
		def g_(line,links):
			if "="not in line:return
			a,b=[c.strip().lower()for c in line.split("=",1)]
			if a in er:au[a]=bP(int(b),*er[a])
			elif a in eu:au[a]=b=="true"
		def g0(line,links):
			if "="not in line:return
			a=[b.strip().lower()for b in line.split("=",1)[1].split(",")];a=[c for c in a if c in cN]
			if len(a)>1:bq.add_group(a)
		def g1(line,links):
			if "="not in line:return
			b,c=line.split("=",1);b=b.strip().lower();a=[d.strip()for d in c.split(",")]
			if b not in aN or len(a)<5:return
			aN[b]=[int(a[0]),int(a[1]),int(a[2]),int(a[3]),a[4].lower()=="true",len(a)>5 and a[5].lower()=="true",bP(int(a[6]),0,100)if len(a)>6 else au["opacity"]]
			if b=="combat":a0["combat_loaded"]=True
		def g2(line,links):
			e=hd(line)
			if e is not None:bF.append(e);dQ(e)
		def g3(line,links):
			if "|"in line:a,b=line.split("|",1);links.append((z(a),z(b)))
		def g4(line,links):
			if "|"not in line:return
			p=line.split("|",5);a=(float(p[0]),int(p[1]),int(p[2]),int(p[3]),{"1":True,"0":False}.get(p[4]));k=z(p[5]);b=bv.get(k)
			if k and(b is None or b[0]<a[0]):bv[k]=a
		eT={"foes":gX,"ignore":gY,"players":gZ,"settings":g_,"anchors":g0,"layout":g1,"sightings":g2,"links":g3,"foe_seen":g4}
		def eU(path,lines):
			if path is None:c8[0]=True;return
			b=None;e=[]
			try:
				for g in lines:
					try:
						a=g.strip()
						if not a or a.startswith("#"):continue
						if a.startswith("[")and a.endswith("]"):b=a[1:-1].strip().lower();continue
						if b in eT:eT[b](a,e)
					except Exception:continue
				e1();e7()
				for c,d in e:
					if c!=d and c in f and d in f:bd[c]=d
				e4()
				for h in aN:L=aN[h];L[0],L[1]=Kit.adapt(L[0],L[1],L[2],L[3])
				c8[0]=True
			except Exception as i:aV("couldn't read the save file (%s); saving is off this session."%i,l)
			if path==eq:
				for k in("friend","foe","neutral"):aN[k][6]=au["opacity"]
		def g5():
			if a0["combat_loaded"]:return
			def a(key,default):
				try:return int(API.GetPersistentVar(key,str(default),API.PersistentVar.Char))
				except Exception:return default
			L=aN["combat"];L[0],L[1]=a("CombatBars_X",L[0]),a("CombatBars_Y",L[1]);L[2]=bP(a("CombatBars_W",L[2]),b1,cG);L[6]=bP(a("CombatBars_Opacity",L[6]),0,100);L[4]=a("CombatBars_Locked",0)==1;L[5]=a("CombatBars_Minimized",0)==1;au["magery"]=a("CombatBars_Magery",0)==1;a0["dirty_save"]=True
		def g6():
			try:d=os.path.dirname(bO)or ".";c=os.path.basename(bO)+".";e=[os.path.join(d,g)for g in os.listdir(d)if g.startswith(c)and g.endswith(".tmp")]
			except Exception:return
			b,a=None,None
			for t in e:
				try:m=os.path.getmtime(t)
				except Exception:continue
				if a is None or m>a:b,a=t,m
			return b
		def g7(text):bm(bO,text,None)
		def dO():return safe(lambda:(os.path.getmtime(bO),os.path.getsize(bO)))
		def g8():
			b=dO();c=time.time()
			if b is None:
				if b6[0]is None:return True
				if not ci[0]:ci[0]=c
				if c-ci[0]<5.:return False
				b6[0]=None;ci[0]=0.;return True
			ci[0]=0.
			if b==b6[0]:return True
			e=Client.on_client_thread()
			if(cB[0]and not e)or c<dN[0]:return False
			try:
				with dM:
					with open(bO,"r")as g:h=g.readlines()
			except Exception as i:dN[0]=c+30.;aV("couldn't read the save file to merge it (%s); saving waits."%i,l);return False
			f,d=None,[]
			for j in h:
				a=j.strip()
				if a.startswith("[")and a.endswith("]"):f=a[1:-1].strip().lower()
				elif f=="foes"and a and not a.startswith("#"):d.append(a)
			if e:eV(d,b,0);return True
			k=cB[0]=id(d);cf.append(lambda:eV(d,b,k));return False
		def eV(got,c,a):
			if a and a!=cB[0]:return
			cB[0]=0;d=Kit.merge_text("\n".join(got),dict(b5),z)[1];b=dict((z(e),e)for e in d)
			for k in[g for g in f if g not in b]:del f[k]
			f.update(b);b6[0]=c;a0["foe_ver"]+=1
			if a:bI()
		def c9():
			a,c7[0]=c7[0],None
			if a:aV("couldn't save (%s)."%a,l)
		def eW():
			if not c8[0]or not g8():return
			def c(b):return "true"if b else "false"
			try:
				a=["# UltimaTracker save file - one name per line"]
				for e,g in(("foes",f),("ignore",M)):a+=["[%s]"%e]+sorted(g.values(),key=lambda s:s.lower())+[""]
				d=cE[0]
				if cF[0]!=d or cF[1]is None:cF[1]=sorted(I.values(),key=lambda s:s.lower());cF[0]=d
				a+=["[players]"]+cF[1]+[""];a+=["[settings]"]+["%s=%d"%(i,au[i])for i in es];a+=["%s=%s"%(n,c(au[n]))for n in eu]+["","[anchors]"];a+=["group=%s"%",".join(q)for q in bq.saved_groups()];a+=["","[layout]"]+["%s=%d,%d,%d,%d,%s,%s,%d"%(t,r[0],r[1],r[2],r[3],c(r[4]),c(r[5]),r[6])for t,r in aN.items()];a+=["","[links]"]+["%s|%s"%(f[v],f[w])for v,w in sorted(bd.items())if v in f and w in f and "|"not in f[v]+f[w]];a+=["","[foe_seen]"]+[he(m)for m in sorted(f)if m in bv];a+=["","[sightings]"]+[k[ha]for k in bF];return "\n".join(a)+"\n"
			except Exception as h:aV("couldn't save (%s)."%h,l);return
		def eX(text,seq=None):
			with dM:
				if seq is not None and seq!=cA[0]:return
				try:g7(text);b6[0]=dO();return True
				except Exception as a:c7[0]=str(a)
		def da(background=False):
			a=eW()
			if a is None:return
			a0["dirty_save"]=False;bn["dirty"]=False;cA[0]+=1;c=cA[0];d=dict(b5)
			def b():
				if eX(a,c):
					for k,v in d.items():
						if b5.get(k,0)==v:b5.pop(k,None)
			if background:eR(b)
			else:b();c9()
		def g9():
			b={d:CategoryGump(d)for d in bE};a=CombatWindow();a8.update({"windows":b,"combat":a})
			if au["combat_shown"]:a.show()
			a8["panel"]=ControlPanel(b,a);ic(b,a);a0["foe_ver"]+=1;n=len(f);aV("on, %s."%R(n,"saved foe"),A);bC.update({"last_layout":fE(),"tick":0,"next_scan":0.,"next_combat":0.,"next_glow":0.})
			if Kit.get_var(cL)=="1":b0.show()
		ip=None;a8={"windows":None,"combat":None,"panel":None};cj,db,cC,eY,eZ,e_,dP,dc,ck,ha=range(10);e0={True:"1",False:"0",None:"-"};hb={"1":True,"0":False}
		def hc(t,serial,noto,facet,x,y,guard,name):return "%d|%d|%s|%d|%d|%d|%s|%s"%(int(t),int(serial),noto,int(facet),int(x),int(y),e0.get(guard,"-"),name)
		def hd(line):
			p=line.split("|",7)
			if len(p)<8 or not p[7]:return
			return[float(p[0]),int(p[1]),p[2]or "unknown",int(p[3]),int(p[4]),int(p[5]),hb.get(p[6]),p[7],z(p[7]),line]
		def dQ(e):
			k=e[ck];a=bv.get(k)
			if a is not None and a[0]>e[cj]:return False
			bv[k]=(e[cj],e[eY],e[eZ],e[e_],e[dP]);return k in f
		def he(k):t,a,x,y,b=bv[k];return "%d|%d|%d|%d|%s|%s"%(int(t),a,x,y,e0.get(b,"-"),f[k])
		def e1():
			n=len(bF)
			if n>cI+f2:del bF[:n-cI]
			if len(bv)>2*cI:
				a=dict((b,c)for b,c in bv.items()if b in f);bv.clear();bv.update(a)
				for e in bF:dQ(e)
		def hf(t,serial,name,noto,facet,x,y,guard):
			a=hc(t,serial,noto,facet,x,y,guard,name);e=[float(int(t)),serial,noto,facet,x,y,guard,name,z(name),a];bF.append(e);e1()
			if dQ(e):bn["seen_ver"]+=1
			bn["ver"]+=1
			if not bn["dirty"]:bn["dirty"]=True;bn["save_at"]=t+d8
		def e2(noto):return aj.get(noto,noto or "unknown")
		def e3(facet,x,y):
			f=f7.get(facet)
			if f is None:f="map %d"%facet if facet>=0 else "?"
			return "%s %d,%d"%(f,x,y)
		def dR(now):a=time.localtime(now);return now-(a.tm_hour*3600+a.tm_min*60+a.tm_sec)
		def dS(t,a):
			try:return time.strftime("%H:%M"if t>=a else "%m/%d %H:%M",time.localtime(t))
			except Exception:return "?"
		def hg(k,now):
			s=bv.get(k)
			if s is None:return "not seen yet"
			t,a,x,y,b=s;return "seen %s, %s%s"%(aJ(now-t,Kit.AGO_WORDS),Q("place",e3(a,x,y))," (guarded)"if b else "")
		def e4():
			for a in list(bd):
				m,n=bd.get(a),0
				while m in bd and n<10:m,n=bd[m],n+1
				if m is None or m==a or m in bd:bd.pop(a,None)
				else:bd[a]=m
		def e5(main):return sorted(b for b,c in bd.items()if c==main)
		def dT(k):
			m=bd.get(k)
			if m is not None:return "alt of "+F(f.get(m,m))
			a=e5(k)
			if a:return "alts: "+", ".join(F(f.get(b,b))for b in a)
			return ""
		def hh(a,b):
			c=bd.get(a,a)
			if b==c or bd.get(b)==c:return "%s and %s are already linked."%(f.get(a,a),f.get(b,b))
			d=bd.get(b,b)
			for k in list(bd):
				if bd[k]==d:bd[k]=c
			if d!=c:bd[d]=c
			bd[b]=c;bd.pop(c,None);e4();return "linked %s as an alt of %s."%(f.get(b,b),f.get(c,c))
		def e6(k):
			if k in bd:del bd[k];return True
			a=e5(k)
			if not a:return False
			b=a[0];del bd[b]
			for c in a[1:]:bd[c]=b
			return True
		cD={};hj=10.
		def hk(name):
			b=HOST.services.get("social.note")
			if b is None or not name:return ""
			c=time.time();a=cD.get(name)
			if a is not None and 0.<=c-a[0]<hj:return a[1]
			try:n=str(b(name)or "").strip()
			except Exception:return ""
			n=n if len(n)<=eb else n[:eb-2]+".."
			if len(cD)>500:cD.clear()
			cD[name]=(c,n);return n
		def bZ(tip,name,extra=""):
			a=[tip]
			if extra:a.insert(0,extra)
			b=dT(z(name))if name else ""
			if b:a.insert(0,b[0].upper()+b[1:])
			n=hk(name)
			if n:a.append("Note: "+n)
			return "\n".join(a)
		def dU(name):f[z(name)]=b5[z(name)]=name;a0["foe_ver"]+=1;bI()
		def hl(key):b5[key]=None;a0["foe_ver"]+=1;bI();return f.pop(key)
		def hm(serial=None,name=None):
			if name:
				k=z(str(name))
				if k and k in f:return True
			if serial is None:return False
			try:s=int(serial)
			except Exception:return False
			k=ct.get(s)
			if k is not None and k in f:return True
			if not name:
				try:m=API.FindMobile(s);k=z(str(m.Name or ""))if m is not None else ""
				except Exception:k=""
				return bool(k)and k in f
			return False
		cE=[0];cF=[None,None];hn=re.compile(r"^\s*\[[^\]]+\]\s*$")
		def e7(c=None):
			if len(I)<=(dD if c is None else c):return
			b=len(I)-gb;d=[]
			for a,e in list(I.items()):
				if b<=0:break
				if a in M or z(e)in f:d.append(a);continue
				del I[a];b-=1
			for a in d:
				if b<=0:break
				del I[a];b-=1
			cE[0]+=1;ab.clear();a0["dirty_save"]=True
		e8=[0.];bL={"learn":None,"attack":None,"killer":None}
		def ho():
			e=time.time()
			if e<e8[0]:return
			e8[0]=e+1.;d=bL["learn"]
			if d is None:d=bL["learn"]=ao()
			for f in d.new():
				b=f.name.strip();a=f.text.strip()
				if not b and ": "in a:b,a=[g.strip()for g in a.split(": ",1)]
				if not b or not a:continue
				c=b.lower()
				if hn.match(a):
					if c not in I:
						if len(I)>=dD:e7(dD-1)
						I[c]=b;cE[0]+=1;a0["dirty_save"]=True;ab.clear()
				elif a.lower().startswith(c+" the "):ad(av);av.add(c)
		def dV(serial,name,noto,party):
			a=z(name)
			if a and a in f:return "foe","L"
			if serial in party:return "friend","P"
			if ak(serial):return "friend","F"
			if noto=="ally":return "friend","G"
			if noto=="murderer":return "foe",""
			if noto=="enemy":return "foe","W"
			return "neutral",""
		def hp(mob,party):
			try:
				b=mob.Serial;c=aW(mob,b)
				if c is None:return
				d,e,a=c
				if a and a.lower()in M:return
				return dV(b,a,d,party)+(d,e)
			except Exception:return
		def dW():return am(max(au["range"],d6))
		def hq(e):return e["name"].lower()
		def hr(e):return e["dist"],e["name"].lower()
		def hs(e):return(e["hits"]/float(e["hmax"])if e["hmax"]>0 else 2.),e["name"].lower()
		ht=(hq,hr,hs);dd={};dX=[None]
		def hu(serial):
			if dX[0]is None or not HOST.in_hop or HOST.pass_id!=dX[0]:return
			return dd.get(serial)
		def hv():
			k={W:[]for W in bE};dd.clear();dX[0]=HOST.pass_id if HOST.in_hop else None;c=time.time();bs(c);e=Y();bA["me"]=e
			if e is None:return k
			F=au["range"];G=dW();x=set(API.GetPartyMemberSerials()or[]);a0["party"]=ac["party"]=x;ac["scan_at"]=c;ho();H=e.Serial;y,A=int(e.X),int(e.Y);I=(au["alert_red"]or au["alert_foes"]or au["alert_orange"]or au["alert_gray"]);f=g=h=i=None;J=au["sightings"];K=a8["windows"]or{};B={};L=au["sort"]==2
			for j in bE:C=K.get(j);B[j]=L or C is None or not(C.minimized and aN[j][5])
			for m in G:
				try:
					if m is None:continue
					a=m.Serial
					if a==H:continue
					l,n=int(m.X),int(m.Y);o=max(abs(l-y),abs(n-A))
					if o>F:continue
					D=aW(m,a)
					if D is None:continue
					d,r,b=D
					if b and b.lower()in M:continue
					p,q=dV(a,b,d,x)
					if p!="friend"and b:
						if q=="L":
							s=z(b)
							if ct.get(a)!=s:ad(ct);ct[a]=s
							if i is None:i=[]
							i.append((s,l,n))
						if J:
							E=cb.get(a)
							if E is None or c-E>du:
								if h is None:h=[]
								h.append((a,b,d,l,n))
							cb[a]=c
						if I and not r and hw(q,d)is not None:
							if f is None:f=set()
							f.add(a)
							if a not in cU:
								if g is None:g=[]
								g.append((a,b,d,q,o,l-y,n-A))
					if B[p]:
						t,u=m.Hits or 0,m.HitsMax or 0;v,w=bool(m.IsPoisoned),bool(m.IsParalyzed)
						if len(dd)<aU:dd[a]=(b,d,p,r,v,w,t,u,o)
					else:t=u=0;v=w=False
					k[p].append({"serial":a,"name":b or "(unknown)","tag":q,"noto":d,"hits":t,"hmax":u,"dist":o,"poisoned":v,"paralyzed":w,"dead":r,"mob":m.raw})
				except Exception:continue
			N=ht[au["sort"]]
			for j in bE:k[j].sort(key=N)
			cU.clear()
			if f is not None:cU.update(f)
			try:
				if i:hA(i,c)
				if g:hx(g,c)
				if h:hz(h,c)
			except Exception as O:cd(O)
			return k
		def hw(tag,noto):
			if tag=="L"and au["alert_foes"]:return "foe"
			if noto=="murderer"and au["alert_red"]:return "red"
			if noto=="enemy"and au["alert_orange"]:return "orange"
			if(noto=="gray"or noto=="criminal")and au["alert_gray"]:return "gray"
			return
		def hx(fresh,now):
			c=au["alert_minutes"]*60.
			for a,b,d,e,f,g,h in fresh:
				t=cs.get(a)
				if t is not None and now-t<c:continue
				cs[a]=now;ay(d7,hy(b,d,e,f,g,h),level="warn",who=a,name=b)
		def hy(name,noto,tag,dist,dx,dy):a=dT(z(name))if tag=="L"else "";b="%s (%s)"%(name,a)if a else name;c=e2(noto)+(", on your Foe list"if tag=="L"else "");return "%s: %s, %s"%(b,c,bl(dx,dy,"right here"))
		def e9():return int(API.GetMap())
		def fa():return safe(HOST.guarded)
		def dY(key,serial,again,now=None):return not aA(serial,key,bD,True,again,now=now)
		def hz(a,now):
			b,c=e9(),fa()
			for d,e,f,x,y in a:hf(now,d,e,f,b,x,y,c)
		fb=[-10.,-1,None]
		def hA(here,now):
			b=c=None
			for k,x,y in here:
				d=bv.get(k)
				if b is None:
					a=fb;f=e9()
					if f!=a[1]or not 0.<=now-a[0]<1.:a[0],a[1],a[2]=now,f,fa()
					b,c=a[1],a[2]
				bv[k]=(now,b,x,y,c)
				if d is None or now-d[0]>du:
					bn["seen_ver"]+=1
					if not bn["dirty"]:bn["dirty"]=True;bn["save_at"]=now+d8
		bA={"dead":None,"prune_at":0.,"me":None,"att_at":0.,"died_at":0.}
		def hB(now):
			if now>=bA["prune_at"]:bA["prune_at"]=now+10.;hF(now)
			c=bA["me"];a=p(c,"IsDead")if c is not None else bA["dead"];b,bA["dead"]=bA["dead"],a
			if au["killer"]and(now>=bA["att_at"]or(a and b is False)):bA["att_at"]=now+1.;hC(now)
			if b is None or a is None or a==b:return
			if a:hE(now)
			else:b8.end()
		def hC(now):
			f=bL["killer"]
			if f is None:bL["killer"]=ao();return
			g,c=[],set()
			for b in f.new():
				if b.text.startswith(fL)or "is attacking you"not in b.low:continue
				h=fp.search(b.text);a=h.group(1).strip().strip("*").strip()if h is not None else ""
				if a:g.append((b,a));c.add(a.lower())
			i=fc(c)if c else None
			for b,a in g:
				j,k=fd(a,i)
				if k is not False:fe(a,b.at,j)
			for s,e in bJ.items():
				m=dg.get(s)
				if m is None:continue
				d=e.get("player")
				if d is None:d=e["player"]=not p(m,"IsRenamable")and(p(m,"IsHuman")or p(m,"IsGargoyle"))
				if d:
					try:a=str(m.Name or "")
					except Exception:a=""
					if a:fe(a,e["last"],s)
		def fc(c):
			a={}
			for m in dW():
				try:
					n=m.Name
					if not n:continue
					b=n.strip().lower()
					if b not in c or b in a:continue
					if p(m,"IsRenamable"):a[b]=(m.Serial,False)
					else:a[b]=(m.Serial,p(m,"IsHuman")or p(m,"IsGargoyle"))
					if len(a)>=len(c):break
				except Exception:continue
			return a
		def fd(name,b=None):
			a=name.lower()
			if b is None:b=fc((a,))
			c=b.get(a)
			if c is not None:return c
			if a.startswith("a ")or a.startswith("an "):return None,False
			return None,None
		def fe(name,t,serial):
			if t<=bA["died_at"]:return False
			if serial is not None and(serial in a0["party"]or ak(serial)):return False
			c=name.lower();a=bx.get(c)
			if a is None:
				if len(bx)>=f6:
					b=None
					for k,v in bx.items():
						if b is None or v[1]<bx[b][1]:b=k
					bx.pop(b,None)
				bx[c]=[name,t,serial];return True
			if t>a[1]:a[1]=t
			if serial is not None:a[2]=serial
			return False
		def hD(a):return-a[1]
		def hE(now):
			bA["died_at"]=now
			if not au["killer"]:bx.clear();return
			b=now-dv;a=sorted([c for c in bx.values()if c[1]>=b],key=hD);bx.clear()
			if a:b8.open(a[:f5],now,len(a))
		def hF(now):
			a=now-du
			for s in[b for b,c in cb.items()if c<a]:del cb[s]
			if cs:
				a=now-au["alert_minutes"]*60.
				for s in[d for d,e in cs.items()if e<a]:del cs[s]
			if bx:
				a=now-dv
				for k in[g for g,h in bx.items()if h[1]<a]:del bx[k]
		def ff(serial,name,a=None):
			def b(*e):
				b=time.time();d=bT.get(serial,0);ad(bT);bT[serial]=b
				if bN():bT[serial]=0;ch(serial);return
				if eO():
					bT[serial]=0
					if aA(serial,"ultima.aim",bD):API.Target(serial)
					return
				if a is not None and eI():d_(serial,name,a);bT[serial]=0;return
				c=b-d<=fO
				if c:bT[serial]=0
				API.SetLastTarget(serial=serial)
				if c:
					if dY("ultima.attack",serial,"double-click again to attack"):return
					API.Attack(serial);API.HeadMsg("* attacking *",serial,34)
				else:API.HeadMsg("* last target *",serial,53)
			return b
		def de(cat,poisoned,dead,paralyzed=False):
			if dead:return dE
			if cat in("friend","combat"):
				if poisoned and paralyzed:return eo
				if paralyzed:return cS
			if poisoned:return cR
			return cp[cat]
		def fg(dead,hits,hmax):return not dead and hmax>0 and hits*100./hmax<=gi
		def fh():a=ei+(gk-ei)*(.5+.5*math.sin(2*math.pi*time.time()/gj));return int(a*ej+.5)/float(ej)
		df={}
		def dZ(b,low,a=None):
			if b is None:return
			if not low:a=0.
			elif a is None:a=fh()
			k=id(b)
			if df.get(k)==a:return
			if len(df)>400:df.clear()
			df[k]=a;bV(b,a)
		def fi(dead,hits,hmax,poisoned,paralyzed,dist):
			if dead:return "DEAD  %dy"%dist,0,1
			if hmax>0:a=aO(poisoned,paralyzed);b=" "+a if a else(" PSN"if poisoned else "")+(" PAR"if paralyzed else "");return "%d%%%s  %dy"%(int(round(100.*hits/hmax)),b,dist),hits,hmax
			return "--  %dy"%dist,0,1
		hG={cp["friend"]:("#3A86BF","#13283A"),cp["neutral"]:("#7E868F","#26292C"),cp["foe"]:("#B23C3C","#3A1616"),cp["combat"]:("#B23C3C","#3A1616"),cR:("#4A9A55","#16301A"),cS:("#5A7FCC","#1A2640"),eo:("#2E9A90","#0F302D"),dE:("#4C4C4C","#1C1C1C")};hH=.85;hI=.9;hJ=.95;hK=.16;hL=.3
		def fj(color):return hG.get(color,(color,"#202020"))
		class HealthBar(object):
			def __init__(self,parent,x,y,w,h,color,cur=0,mx=1):
				self.fw=None;self.parts=[];self.color=color;c,d=fj(color);a=1 if h>=5 and w>=8 else 0;self.ix,self.iy=x+a,y+a;self.iw,self.ih=max(1,w-2*a),max(1,h-2*a)
				if a:self._add(parent,hH,"#000000",x,y,w,h)
				self.track=self._add(parent,hI,d,self.ix,self.iy,self.iw,self.ih);self.fill=self._add(parent,hJ,c,self.ix,self.iy,0,self.ih);self.sheen=self.shade=None
				if self.ih>=6:self.sheen=self._add(parent,hK,"#FFFFFF",self.ix,self.iy,0,max(1,self.ih*2//5));b=max(1,self.ih//5);self.shade=self._add(parent,hL,"#000000",self.ix,self.iy+self.ih-b,0,b)
				self.SetProgress(cur,mx)
			def _add(self,parent,alpha,color,x,y,w,h):b=b2(alpha,color);b.SetRect(x,y,w,h);parent.Add(b);self.parts.append(b);return b
			def SetProgress(self,cur,mx):
				a=int(round(self.iw*bP(float(cur)/mx,0.,1.)))if mx>0 else 0
				if a==self.fw:return
				self.fw=a
				for b in(self.fill,self.sheen,self.shade):
					if b is not None:b.SetWidth(a)
			def set_color(self,color):
				if color==self.color:return
				a,b=fj(color)
				for c,d in((self.fill,a),(self.track,b)):r,g,e=gJ(d);c.SetBaseColor(r,g,e,255)
				self.color=color
			def set_visible(self,on):
				for c in self.parts:D(c,"IsVisible",on)
			def Dispose(self):
				for c in self.parts:bM(c)
				self.parts=[]
		class PopBar(object):
			def __init__(self,serial,name,x,y):self.serial,self.name,self.x,self.y=serial,name,x,y;self.gump=None;self.locked=self.minimized=self.opacity_open=False;self.opacity,self.name_color=au["opacity"],cP;self.shown=F(name,serial);self.create()
			def create(self):
				s=au["scale"]/100.;w=sc(fQ);self.row_h=max(10,sc(16));self.pad=max(2,sc(5));h=2*bc+eK(s)
				if self.opacity_open:h+=eL(s)
				if not self.minimized:h+=self.row_h+2*self.pad
				self.size=(w,h);self.x,self.y=aM(self.x,self.y,w,h);g=API.Gumps.CreateModernGump(self.x,self.y,w,h,False,w,h);self.gump=g;g.SetAlpha(0.);self.chrome=Chrome(g);self.bar=self.info=self.hit=self.glow=None;self.low,self.spell_ctrls,self.bar_key,self.last=False,[],None,None;self.layout_chrome();G.AddGump(g);aQ(g,self.moved);bq.placed(self.anchor_key);D(g,"CanMove",not self.locked)
			@property
			def anchor_key(self):return "pop:%d"%self.serial
			def moved(self):bq.pending=True
			def layout_chrome(self):
				w,h=self.size;a,b=self.minimized,self.opacity_open;c=[("lock",self.locked,self.toggle_lock,"Unlock (move and resize again)"if self.locked else "Lock in place (no moving or resizing)"),("min",a,self.toggle_minimize,"Restore"if a else aH)]
				if not a:c.append(("opacity",b,self.toggle_opacity,"Hide the opacity slider"if b else "Show the opacity slider (frame and bars stay solid)"))
				c.append(("close",False,self.close,"Close this bar"));self.chrome.layout(w,h,au["scale"]/100.,self.opacity,self.shown,self.name_color,c,b and not a,self.toggle_minimize,lambda:ch(self.serial),self.anchor_key)
			def destroy(self):g,self.gump=self.gump,None;K(g)
			def close(self,*a):br.pop(self.serial,None);self.destroy()
			def snapshot(self):
				if E(self.gump):self.x,self.y=self.gump.GetX(),self.gump.GetY()
			def rebuild(self):self.snapshot();self.destroy();self.create()
			def set_locked(self,locked):
				self.locked=locked
				if self.gump is not None:D(self.gump,"CanMove",not locked);self.layout_chrome()
			def toggle_lock(self,*a):self.set_locked(not self.locked)
			def toggle_minimize(self,*a):self.minimized=not self.minimized;self.opacity_open=False;self.rebuild()
			def toggle_opacity(self,*a):self.opacity_open=not self.opacity_open;self.rebuild()
			def apply_opacity(self,v):
				self.opacity=v
				if self.gump is not None:self.chrome.set_opacity(v)
			def update(self):
				if not E(self.gump):br.pop(self.serial,None);return
				try:
					v=self.chrome.poll()
					if v is not None:self.opacity=v
					self._refresh()
				except Exception as a:aV("closed the health bar for %s (%s)."%(self.name,a),l);self.close()
			def _draw_row(self,key):
				f,h,c=key
				if self.bar is not None:self.bar.Dispose()
				for g in[self.info,self.hit,self.glow]+self.spell_ctrls:bM(g)
				self.spell_ctrls=[];w=self.size[0];s=au["scale"]/100.;y=self.chrome.content_top+self.pad;a=w-2*bc-2*self.pad;x=bc+self.pad
				if c and c4():d=self.row_h;a-=c4()*(d+2);eJ(self.gump,x+a+2,y,d,self.row_h,self.serial,self.name,self.spell_ctrls)
				self.glow=None
				if c:b=max(2,self.pad-1);self.glow=b2(0.,eh);self.glow.SetRect(x-b,y-b,a+2*b,self.row_h+2*b);self.gump.Add(self.glow)
				self.bar=HealthBar(self.gump,x,y,a,self.row_h,f);e=max(8,int(round(12*cV(s))));self.info=cv("",e,"#FFFFFF",aligned="right",maxWidth=a-6,applyStroke=True);self.info.SetPos(x+3,cg(y,self.row_h,e));self.gump.Add(self.info);self.hit=bQ(x,y,a,self.row_h,ff(self.serial,self.name),bZ(d0,self.name));self.gump.Add(self.hit);self.bar_key=key;self.last=None
			def pulse(self,a=None):
				if self.gump is not None and not self.minimized:dZ(self.glow,self.low,a)
			def _refresh(self):
				e=Y();d=hu(self.serial)if e is not None else None
				if d is not None and d[0]:a=True
				else:d=None;a=aB(self.serial)
				if a is None or e is None:b,f,g,c,h=("out of range",0,1,(dE,False,False),"#888888");self.low=False;self.shown=F(self.name,self.serial)
				else:
					if d is not None:l,i,j,k,m,n,o,q,r=d
					else:
						try:l=a.Name or self.name
						except Exception:l=self.name
						i=V(a);j,t=dV(self.serial,l,i,a0["party"]);k,m=p(a,"IsDead"),p(a,"IsPoisoned");n,o,q=p(a,"IsParalyzed"),aw(a,"Hits"),aw(a,"HitsMax")
						try:r=max(abs(int(a.X)-int(e.X)),abs(int(a.Y)-int(e.Y)))
						except Exception:r=0
					c=(de(j,m,k,n),(au["magery"],au["healing"]),j=="friend");self.low=j=="friend"and fg(k,o,q);h=cZ(i,"#DDDDDD");self.shown=af(self.name,self.serial,i);b,f,g=fi(k,o,q,m,n,r)
				if Follow.serial==self.serial:b="FOL "+b
				self.name_color=h
				if self.minimized:self.chrome.set_title("%s  %s"%(self.shown,b.split("  ")[0]),h);return
				self.chrome.set_title(self.shown,h)
				if c!=self.bar_key:
					s=self.bar_key
					if s is not None and s[1:]==c[1:]and self.bar is not None:self.bar.set_color(c[0]);self.bar_key=c
					else:self._draw_row(c)
				if self.last!=(b,f,g):self.last=(b,f,g);bR(self.info,b);self.bar.SetProgress(float(f),float(g))
		def hM(serial,name):
			def a(*b):
				if not name or name=="(unknown)":aV("no name yet; try again in a moment.",l);return
				M[name.lower()]=name;bI();a=br.get(serial)
				if a is not None:a.close()
				aV("%s marked as an NPC and hidden; Unignore the name to undo."%name,A)
			return cx(serial,a)
		def hN(serial,name,a):return cx(serial,lambda:d_(serial,name,a))
		def hO(serial,name,a):HOST.enable("unitframes");cf.append(lambda:d_(serial,name,a,False))
		def d_(serial,name,a,d=True):
			b=HOST.services.get("unitframes.add")
			if b is None and d and "unitframes"in HOST.by_key:cw.append(lambda:hO(serial,name,a));return
			if b is not None:b(serial);aV("%s gets a frame in Character HUD > Frames."%name,A);return
			c=br.get(serial)
			if c is not None and E(c.gump):aV("a health bar for %s is already open."%name,l);return
			e=safe(lambda:a.gump.GetX(),300);f=safe(lambda:a.gump.GetY(),300);x=e+a.size[0]+6;y=f+len(br)*(sc(52)+4);g=br[serial]=PopBar(serial,name,x,y);g.update();aV("popped out a health bar for %s."%name,A)
		d0=("Click: target; double-click: attack (blue or green in guards: twice). Alt+click: auto-follow (again to stop)");hP="Click: put the name in the box. Alt+click: auto-follow (again to stop)";fk=("Click: show only this player (again for everyone). Alt+click: auto-follow (again to stop)")
		class PoolRow(object):
			glow=None;e=None;prev=None
			def parts(self):return self.ctrls
			def set_shown(self,on):
				for c in self.parts():D(c,"IsVisible",on)
				self.bar.set_visible(on);self.shown=on
			def hide(self):
				if self.serial is not None:self.prev=(self.serial,self.name,time.time())
				self.serial,self.name=None,"";self.low=False;self.last=None
				if self.glow is not None:dZ(self.glow,False)
				self.set_shown(False)
		class TrackerRow(PoolRow):
			def __init__(self,view,i,geo,e):
				self.win=view;self.serial,self.name=e["serial"],e["name"];self.y=y=i*geo["row_h"];self.shown,self.low,self.ctrls=True,False,[];self.last=self.raw=self.name_raw=None;a,b=view.sa,geo["rw"];c=API.Gumps.CreateGumpColorBox(.35,"#000000");c.SetRect(0,y,b,geo["row_h"]-2);eB(c,RowClick(self,lambda s,n:ff(s,n,view)));U(c,bZ(d0,self.name));self.bg=c;self.glow=None
				if view.cat=="friend":self.glow=b2(0.,eh);self.glow.SetRect(0,y,b,geo["row_h"]-2)
				h,j=fl(e,geo);self.name_lbl=bH(h,geo["name_fs"],j);bz(self.name_lbl,4,y+geo["name_dy"]);self.name_key=(h,j);d,f=geo["pbw"],geo["nbw"];self.info=bH("",geo["info_fs"],"#DDDDDD",aligned="right",maxWidth=b-16-d-f);bz(self.info,4,y+geo["info_dy"])
				for g in(c,self.glow,self.name_lbl,self.info):
					if g is not None:a.Add(g);self.ctrls.append(g)
				b3(a,b-8-d-f,y+geo["npc_dy"],f,f,"N",RowClick(self,hM),"Mark as an NPC and hide (Unignore the name to undo). "+bW,font=geo["npc_fs"],store=self.ctrls);b3(a,b-4-d,y+geo["pop_dy"],d,geo["pop_h"],">",RowClick(self,lambda s,n:hN(s,n,view)),"Pop out a health bar (or Shift+click the row). "+bW,font=geo["pop_fs"],store=self.ctrls);self.tips=[]
				if geo["fbtn"]:self.tips=eJ(a,4+geo["bar_w"]+2,y+geo["fbtn_dy"],geo["sb"],geo["sb"],self.serial,self.name,store=self.ctrls,row=self)
				self.bar=HealthBar(a,4,y+geo["bar_dy"],geo["bar_w"],geo["bar_h"],fm(view.cat,e))
			def assign(self,e,geo):
				a,b=e["serial"],e["name"]
				if a!=self.serial or b!=self.name:
					if a!=self.serial:self.prev=(self.serial,self.name,time.time())
					self.serial,self.name=a,b;self.last=None
					for g,h in self.tips:U(g,h%F(b,a))
					U(self.bg,bZ(d0,b))
				if not self.shown:self.set_shown(True)
				c=(e["name"],e["tag"],e["noto"],geo["name_px"],geo["name_fs"])
				if c!=self.name_raw:
					d,f=fl(e,geo)
					if(d,f)!=self.name_key:self.set_name(d,f,geo)
					self.name_raw=c
				self.bar.set_color(fm(self.win.cat,e))
			def set_name(self,text,color,geo):
				a=self.name_lbl
				if color==self.name_key[1]or eH(a,color):bR(a,text)
				else:b=self.ctrls.index(a);bM(a);a=bH(text,geo["name_fs"],color);bz(a,4,self.y+geo["name_dy"]);self.win.sa.Add(a);self.ctrls[b]=a;self.name_lbl=a
				self.name_key=(text,color)
			def values(self,e):
				self.e=e;d=Follow.serial==e["serial"];f=(e["dead"],e["hits"],e["hmax"],e["poisoned"],e["paralyzed"],e["dist"],d)
				if self.last is not None and f==self.raw:return
				self.raw=f;a,b,c=fi(e["dead"],e["hits"],e["hmax"],e["poisoned"],e["paralyzed"],e["dist"])
				if d:a="FOL "+a
				self.low=fg(e["dead"],e["hits"],e["hmax"])
				if self.last!=(a,b,c):self.last=(a,b,c);bR(self.info,a);self.bar.SetProgress(float(b),float(c))
			def forget(self):
				for c in self.ctrls:bG.pop(id(c),None)
				self.ctrls=[];self.serial=None
		def fl(e,geo):
			a=c3(af(e["name"],e["serial"],e["noto"]),geo["name_px"],geo["name_fs"])
			if e["tag"]:a+="  ["+e["tag"]+"]"
			return a,cZ(e["noto"],"#DDDDDD")
		def fm(cat,e):return de(cat,e["poisoned"],e["dead"],e["paralyzed"])
		class PoolWin(object):
			def show_empty(self,on):
				if on and self.empty is None:self.empty=self.make_empty();self.empty_shown=True
				elif self.empty is not None and on!=self.empty_shown:
					for a in self.empty:D(a,"IsVisible",on)
					self.empty_shown=on
			def fill(self,data):
				a,b,n=self.rows,self.geo,len(data)
				for i,e in enumerate(data):
					if i<len(a):a[i].assign(e,b)
					else:a.append(self.Row(self,i,b,e))
				for r in a[n:]:
					if r.shown:r.hide()
				self.show_empty(n==0)
				for r,e in zip(a,data):r.values(e)
			def destroy(self):g,self.gump=self.gump,None;K(g)
			def moved(self):bq.pending=True;self.snapshot();bI()
			@property
			def dock_key(self):return "ultima."+self.cat
			def user_minimize(self,*a):X(self.dock_key);self.toggle_minimize()
			def apply_opacity(self,v):
				aN[self.cat][6]=v
				if E(self.gump)and self.chrome is not None:self.chrome.set_opacity(v)
		class CategoryGump(PoolWin):
			Row=TrackerRow
			def __init__(self,cat):self.cat,self.rows=cat,[];self.gump=self.chrome=self.sa=self.made_min=None;self.locked=self.minimized=self.docked=False;self.create()
			def create(self):
				x,y,w,h,i,e,k=aN[self.cat];self.minimized=e;b,c=sc(dn),sc(do);a=bb["size"].get(self.cat);j=H(self.dock_key)
				if a is not None:
					b=min(b,a[0]);c=min(c,a[1]);w=a[0]
					if not e:h=a[1]
				w=max(w,b)
				if e:d=ew;f,g=d,False
				else:d=max(h,c);f,g=c,a is None
				self.made_min=(b,c);self.resized_flag=self.user_resize_pending=False;self.sync_target,self.user_resize_ticks=None,0
				if not j:x,y=aM(x,y,w,d);aN[self.cat][0],aN[self.cat][1]=x,y
				self.gump=API.Gumps.CreateModernGump(x,y,w,d,g,b,f,self._on_resized);self.gump.SetAlpha(0.);self.chrome=Chrome(self.gump,kit=True,key=self.dock_key);self._forget_body();self.size=(w,d);self.count_n=0;self.locked=i;self.layout_chrome();G.AddGump(self.gump);aQ(self.gump,self.moved);bq.placed(self.cat);self._apply_lock()
				if self.docked and e:D(self.gump,"IsVisible",False)
			def layout_fit(self,w,h,mode):
				a=self.cat
				if w is None or h is None:
					if a in bb["size"]:bb["size"][a]=None
					bb["force"].discard(a)
				else:
					bb["size"][a]=(int(w),int(h))
					if mode=="again":bb["force"].add(a)
				bb["req"]=True
			def _forget_body(self):
				for r in self.rows:r.forget()
				self.rows=[];self.sa=self.empty=self.geo=self.body_key=None
			def layout_chrome(self):w,h=self.size;c=self.cat;self.chrome.layout_kit(w,h,aN[c][6],ef[c],eg[c],self.minimized,self.user_minimize,lambda*a:cr.append(self.dock_key));self.chrome.set_status(str(max(0,self.count_n)))
			def zone_chrome(self):
				if E(self.gump)and self.chrome is not None:self.layout_chrome()
			def _on_resized(self,*a):self.resized_flag=True
			def set_count(self,n):
				if n==self.count_n:return
				self.count_n=n;self.chrome.set_status(str(max(0,n)))
			def _apply_lock(self):
				a=self.locked;b=bb["size"].get(self.cat)is not None;c=H(self.dock_key)
				if not c:D(self.gump,"CanMove",not a)
				self.gump.SetResizable(not a and not self.minimized and not b);aN[self.cat][4]=a;a0["dirty_save"]=True
			def set_locked(self,locked):self.locked=locked;self._apply_lock()
			def toggle_minimize(self,*a):
				self.snapshot();aN[self.cat][5]=not self.minimized
				if not aN[self.cat][5]:self.docked=False
				self.destroy();self.create();a0["dirty_save"]=True
			def geometry(self):
				w,h=self.size;a=u+4;c=max(40,w-2*a);b=max(60,c-d4);e=cW(13);g={"sa":(a,self.chrome.content_top+sc(4),c,max(20,h-self.chrome.content_top-sc(4)-a)),"rw":b,"row_h":sc(Kit.pitch(fP)),"name_fs":e,"info_fs":cW(12),"name_px":max(30,int(b/1.2)),"name_dy":sc(1),"info_dy":sc(2),"pbw":sc(fR),"nbw":sc(fS),"npc_dy":sc(3),"npc_fs":cW(10),"pop_dy":sc(1),"pop_h":sc(16),"pop_fs":cW(12),"fbtn":self.cat=="friend"and c4()>0,"sb":sc(13),"fbtn_dy":sc(16)};d=b-8
				if g["fbtn"]:d-=c4()*(g["sb"]+2)
				g["bar_w"],g["bar_dy"],g["bar_h"]=d,sc(18),max(3,sc(10));return g
			def build_body(self):K(self.sa);self._forget_body();self.geo=a=self.geometry();x,y,w,h=a["sa"];self.sa=API.Gumps.CreateGumpScrollArea(x,y,w,h);self.gump.Add(self.sa)
			def make_empty(self):a=ex("No players in range.",self.geo["rw"]-8);return ey(self.sa,a,4,4)
			def update(self,entries):
				if not E(self.gump):self.create()
				if not self.minimized:
					w,h=int(self.gump.GetWidth()),int(self.gump.GetHeight())
					if(w<=0 or h<=0)and self.size:w,h=self.size
					if(w,h)!=self.size or self.resized_flag:
						self.resized_flag=False;self.size=(w,h);bq.placed(self.cat,self.gump.GetX(),self.gump.GetY(),w,h);self.layout_chrome();self.body_key=None
						if self.sync_target==(w,h)or bb["size"].get(self.cat)is not None:self.sync_target=None
						else:self.user_resize_pending=True;self.user_resize_ticks=0
					elif self.user_resize_pending:self.user_resize_ticks+=1
					a=bb["size"].get(self.cat)
					if a is not None and(w,h)!=a:bb["req"]=True
				self.set_count(len(entries))
				if self.minimized:return
				b=(self.size,self.chrome.content_top,au["scale"],au["magery"],au["healing"])
				if b!=self.body_key:self.build_body();self.body_key=b
				self.fill(entries)
			def pulse(self,a=None):
				if self.cat!="friend"or self.minimized:return
				for b in self.rows:
					if b.shown:dZ(b.glow,b.low,a)
			def resize_to(self,w,h):
				if not self.minimized:
					if self.size==(w,h):return
					self.sync_target=(w,h);self.gump.SetWidth(w);self.gump.SetHeight(h)
					if(self.gump.GetWidth(),self.gump.GetHeight())==(w,h):return
				self.snapshot();aN[self.cat][2],aN[self.cat][3]=w,h;self.destroy();self.create()
			def snapshot(self):
				if not E(self.gump):return
				L=aN[self.cat];L[0],L[1],L[2]=self.gump.GetX(),self.gump.GetY(),self.size[0]
				if not self.minimized:L[3]=self.size[1]
		def d1(windows):
			for w in windows.values():w.destroy()
			for w in windows.values():w.create()
			for p in list(br.values()):p.rebuild()
		def hQ():
			if a8["windows"]is not None:
				for w in a8["windows"].values():w.snapshot()
				d1(a8["windows"])
			if a8["combat"]is not None:a8["combat"].relayout=True
			if a8["panel"]is not None:a8["panel"].rebuild_foe_list()
			b0.ask_redraw();b8.ask_redraw()
		def fo(windows,source):
			if source.minimized:w,h=aN[source.cat][2],aN[source.cat][3]
			else:w,h=source.size
			for t in windows.values():
				if t is source or t.locked or bb["size"].get(t.cat)is not None:continue
				t.resize_to(w,h)
			a0["dirty_save"]=True
		def hR(windows):
			for w in windows.values():
				if not au["sync"]:w.user_resize_pending=False
				elif w.user_resize_pending and w.user_resize_ticks>=2:
					if c1():return
					w.user_resize_pending=False;fo(windows,w);return
		def hS(a,windows):
			b=au["scale"]
			if a==b:return
			c=float(a)/b
			for w in windows.values():w.snapshot();L=aN[w.cat];L[2]=max(sc(dn,a),int(round(L[2]*c)));L[3]=max(sc(do,a),int(round(L[3]*c)))
			au["scale"]=a;d1(windows);a0["dirty_save"]=True
		def hT(windows):
			if not bb["req"]:return
			bb["req"]=False;e=c1()
			for a,i in list(bb["size"].items()):
				b=windows.get(a)
				if b is None or b.gump is None:continue
				if i is None:
					if e:bb["req"]=True;continue
					bb["size"].pop(a,None);c=bb["own_size"].pop(a,None)
					if b.made_min is not None and b.made_min!=(sc(dn),sc(do)):
						b.snapshot()
						if c is not None:aN[a][2],aN[a][3]=c
						b.destroy();b.create()
					elif c is not None and c!=(aN[a][2],aN[a][3]):b.resize_to(c[0],c[1])
					bb["made"].pop(a,None)
					if b.gump is not None:b._apply_lock()
					continue
				if a not in bb["own_size"]:bb["own_size"][a]=(aN[a][2],aN[a][3])
				w,h=i;j=a in bb["force"]
				if b.minimized:
					if aN[a][2]!=w or(b.size and b.size[0]!=w):
						if e:bb["req"]=True;continue
						b.resize_to(w,aN[a][3])
					bb["force"].discard(a);continue
				d=(int(b.gump.GetWidth()),int(b.gump.GetHeight()))
				if d[0]<=0 or d[1]<=0:bb["force"].discard(a);continue
				f=bb["made"].get(a);g=f[1]if f is not None and f[0]==(w,h)else 0
				if d==(w,h)and b.size==(w,h):g=0;bb["made"].pop(a,None)
				if(j or b.size!=(w,h)or d!=(w,h)or b.made_min[0]>w or b.made_min[1]>h)and(j or g<gE):
					if e:bb["req"]=True;continue
					bb["force"].discard(a);bb["made"][a]=((w,h),g+1);b.snapshot();aN[a][2],aN[a][3]=w,h;b.destroy();b.create()
				else:bb["force"].discard(a)
		fp=Journal.ATTACK_RE;fq=[int(iv)for iv in f0];bJ={};fr=[0];cl=[];dg={};b7=[];bB={"serial":None,"until":0.,"harmful":True,"stale":False}
		def fs(m):
			try:return m is not None and not m.IsDead
			except Exception:return False
		def d2(m):
			try:return int(m.Distance)
			except Exception:return 0
		def d3(m,attacked_me=False):
			if p(m,"IsRenamable"):return False
			a=V(m);return a not in fZ and(attacked_me or a not in f_)
		def cm(serial,t=None):
			e=bJ.get(serial)
			if not e:
				a=Y()
				if a is None or serial==a.Serial:return
			if serial in a0["party"]or ak(serial):return
			t=t or time.time()
			if e:e["last"]=t
			elif len(bJ)<fX:fr[0]+=1;bJ[serial]={"last":t,"hits":None,"order":fr[0]}
		hU=5.
		def hV():
			d=bL["attack"]
			if d is None:bL["attack"]=ao();return
			g,b=time.time()-hU,set()
			for c in d.new():
				if c.at>=g and "is attacking you"in c.low:
					m=fp.search(c.text)
					if m:b.add(m.group(1).strip().lower())
			if not b:return
			e={}
			for m in dW():
				try:
					n=m.Name
					if n:
						f=n.strip().lower()
						if f in b and d3(m,attacked_me=True):e.setdefault(f,[]).append(m)
				except Exception:pass
			for a in e.values():
				if len(a)==1:cm(a[0].Serial);continue
				h=[i for i in a if d3(i)or p(i,"InWarMode")]or[min(a,key=d2)]
				for m in h:cm(m.Serial)
		ft=.5;fu={"serial":None,"until":0.}
		def hW():
			s=API.LastTargetSerial;b=Y()
			if not s or b is None or s==b.Serial or s in bJ:return
			if au["combat_only"]and not b.InWarMode:return
			c=time.time();a=fu
			if a["serial"]==s and 0.<=a["until"]-c<=ft:return
			m=API.FindMobile(s)
			if fs(m)and d2(m)<=dr and d3(m):a["serial"]=None;cm(s)
			else:a["serial"],a["until"]=s,c+ft
		def hX():
			a=fY if au["combat_only"]else dr
			for m in am(a):
				try:
					if int(m.Notoriety)in fq and m.InWarMode and not m.IsDead and not p(m,"IsRenamable"):cm(m.Serial)
				except Exception:pass
		def fv():
			t=time.time();dg.clear();a=[]
			for s in list(bJ.keys()):
				e=bJ[s];m=API.FindMobile(s)
				if not fs(m):del bJ[s];continue
				d=d2(m)
				if d>d6:del bJ[s];continue
				try:h=m.Hits
				except Exception:del bJ[s];continue
				if e["hits"]is not None and h<e["hits"]:e["last"]=t
				e["hits"]=h;n=None
				try:
					if d<=dr and m.InWarMode:
						n=m.Notoriety
						if int(n)in fq:e["last"]=t
				except Exception:pass
				if t-e["last"]>fW:del bJ[s];continue
				dg[s]=m
				try:b,c=m.Name or "???",m.HitsMax;f,g=bool(m.IsPoisoned),bool(m.IsParalyzed);a.append((e["order"],s,b,V(m)if n is None else Kit.noto_of(n),h,c,f,g))
				except Exception:continue
			a.sort();return[i[1:]for i in a]
		def hY(serial):
			def a(*a):cl.append((serial,bN(),time.time()))
			return a
		def hZ():
			while cl:
				s,b,a=cl.pop(0);m=API.FindMobile(s)
				if not m:continue
				if b:ch(s);continue
				if eO():
					if not aA(s,"ultima.aim",bD,now=a):continue
					API.Target(s)
				else:
					if dY("ultima.attack",s,"click the bar again to attack",a):continue
					API.Attack(s)
				cm(s)
		def h_(spell,serial):
			def a(*a):
				if bN():cl.append((serial,True,time.time()));return
				b7.append((spell,serial,True,time.time()))
			return a
		def fw(serial,spell,a):return cx(serial,lambda:b7.append((a if eI()else spell,serial,False,time.time())))
		def h0():
			if b7:
				c,s,a,d=b7[-1]
				if c6()is not None:
					if time.time()-d>dq:del b7[:];aV("target cursor busy; %s not cast."%c,l)
				else:
					del b7[:];m=API.FindMobile(s)
					if m and a and dY("ultima.cast",s,"click the button again to cast",d):m=None
					if m:
						b=bool(API.HasTarget("any"))
						if b and bB["serial"]is not None and not bB["stale"]and API.HasTarget("harmful"if bB["harmful"]else "beneficial"):API.CancelTarget();b=False
						API.CastSpell(c);bB.update(serial=s,harmful=a,stale=b,until=time.time()+dq);eN("spell",dq)
						if a:cm(s)
			if bB["serial"]is None:bX("spell");return
			if time.time()>bB["until"]:bB["serial"]=None;bX("spell");return
			if bB["stale"]:
				if not API.HasTarget("any"):bB["stale"]=False
				return
			if c6()is not None:return
			if API.HasTarget("harmful"if bB["harmful"]else "beneficial"):
				s=bB["serial"];bB["serial"]=None;bX("spell")
				if API.FindMobile(s):API.Target(s)
				else:API.CancelTarget()
		def fx(serial,hits,a,c,d):
			f="?"if not a or a<=1 else str(int(round(hits*100./a)))+"%";b="FOL "if Follow.serial==serial else "";e=aO(c,d)
			if e:b+=e+" "
			else:b+=("PSN "if c else "")+("PAR "if d else "")
			return b+f
		fy="Attack or aim at %s (blue or green in guards: twice). "+bW;h1=(("Poison","P",cR,"Cast Poison on %s. Alt+click: auto-follow (again to stop)"),("Paralyze","Z",cS,"Cast Paralyze on %s. Alt+click: auto-follow (again to stop)"));b_=u+4
		class CombatSlot(PoolRow):
			def __init__(self,view,i,geo,d):
				self.win=view;g=view.gump;b,a,t,l,h,m,o=d;self.serial,self.name=b,a;self.y=c=geo["y"]+i*(geo["rh"]+cH);self.shown,self.ctrls,self.tips=True,[],[];self.bar=HealthBar(g,b_,c,geo["bar_w"],geo["rh"],de("combat",m,False,o),l,h if h else 1);self.name_lbl=self.info=self.name_key=self.info_text=self.name_raw=self.info_raw=None;self._texts(d,geo);e=bQ(b_,c,geo["bar_w"],geo["rh"],RowClick(self,lambda s,n:hY(s)),bZ(fy%F(a,b),a));g.Add(e);self.ctrls.append(e);self.tips.append((e,fy))
				if au["magery"]:
					j=b_+geo["bar_w"]+1
					for p,q,r,k in h1:f=[];b3(g,j,c,geo["spell_w"],geo["rh"],q,RowClick(self,(lambda a:lambda s,n:h_(a,s))(p)),k%F(a,b),face=r,color="#FFFFFF",font=max(7.,geo["font"]-1),store=f);self.ctrls.extend(f);self.tips.append((f[-1],k));j+=geo["spell_w"]+1
			def _texts(self,d,geo):
				g=self.win.gump;h,i,c,m,j,n,o=d;a=geo["font"];k=cg(self.y,geo["rh"],a)
				if self.name_lbl is None:b=c3(af(i,h,c),geo["name_w"],a,True);l=cZ(c,"#FFFFFF");e=cv(b,a,l,applyStroke=True);e.SetPos(b_+3,k);g.Add(e);self.name_lbl,self.name_key=e,(b,l);self.name_raw=(i,c,geo["name_w"],a)
				if self.info is None:b=fx(h,m,j if j else 1,n,o);f=cv(b,a,"#FFFFFF",aligned="right",maxWidth=geo["info_w"],applyStroke=True);f.SetPos(b_+geo["bar_w"]-geo["info_w"]-3,k);g.Add(f);self.info,self.info_text=f,b
			def assign(self,d,geo):
				b,a,e,m,n,i,j=d
				if b!=self.serial or a!=self.name:
					if b!=self.serial:self.prev=(self.serial,self.name,time.time())
					self.serial,self.name=b,a
					for k,(l,f)in enumerate(self.tips):U(l,bZ(f%F(a,b),a)if k==0 else f%F(a,b))
				if not self.shown:self.set_shown(True)
				self.bar.set_color(de("combat",i,False,j));g=geo["font"];h=(a,e,geo["name_w"],g)
				if self.name_lbl is not None and h!=self.name_raw:
					c=(c3(af(a,b,e),geo["name_w"],g,True),cZ(e,"#FFFFFF"))
					if c!=self.name_key:
						if c[1]==self.name_key[1]:bR(self.name_lbl,c[0]);self.name_key=c
						else:bM(self.name_lbl);self.name_lbl=None
					self.name_raw=h
				self._texts(d,geo)
			def values(self,d):
				self.e=d;a,j,k,b,f,g,h=d;c=f if f else 1;self.bar.SetProgress(b,c);i=(a,b,c,g,h,Follow.serial==a)
				if i!=self.info_raw:
					self.info_raw=i;e=fx(a,b,c,g,h)
					if e!=self.info_text:self.info_text=e;bR(self.info,e)
			def parts(self):return[self.name_lbl,self.info]+self.ctrls
			def dispose(self):
				for c in self.parts():bM(c)
				self.bar.Dispose()
		class CombatWindow(PoolWin):
			Row=CombatSlot
			def __init__(self):self.gump=self.chrome=self.slot=None;self.relayout=self.zone_redraw=self.docked=False;self.made_min=b1;self.cat="combat";self._forget()
			def layout_fit(self,w,h,mode):
				a=(int(w),int(h))if w and h else None
				if a!=self.slot or mode=="again":self.slot=a;self.relayout=self.zone_redraw=True
			def width(self):return self.slot[0]if self.slot is not None else aN["combat"][2]
			def zone_chrome(self):self.relayout=True
			def _forget(self):self.rows,self.grip,self.empty_lines=[],[],[];self.empty=self.frame_key=self.geo=self.fit_n=None;self.empty_shown=False
			@property
			def minimized(self):return bool(aN["combat"][5])
			def is_open(self):return E(self.gump)
			def show(self):
				if self.is_open():return
				L=aN["combat"];L[2]=bP(L[2],b1,cG);a=H(self.dock_key)
				if not a:L[0],L[1]=aM(L[0],L[1],self.width(),self.height(0))
				self.made_min=min(b1,self.width());g=API.Gumps.CreateModernGump(L[0],L[1],self.width(),self.height(0),True,self.made_min,16,self._on_resized);g.SetAlpha(0.);self.gump=g;self._forget();G.AddGump(g);aQ(g,self.moved);bq.placed("combat")
				if not a:au["combat_shown"]=True;a0["dirty_save"]=True
				self.apply_lock();self.draw(fv())
			def hide(self):
				self.snapshot();K(self.gump);self.gump=None;self._drop_notes();au["combat_shown"]=False;a0["dirty_save"]=True
				if self.docked:self.docked=False;X(self.dock_key)
			def _drop_notes(self):
				for a in self.rows:bG.pop(id(a.name_lbl),None);bG.pop(id(a.info),None)
				self._forget()
			def snapshot(self):
				if self.is_open():L=aN["combat"];L[0],L[1]=self.gump.GetX(),self.gump.GetY()
			def reset(self):
				aN["combat"]=list(dG["combat"])
				if self.is_open():L=aN["combat"];g=self.gump;g.SetPos(L[0],L[1]);bj(g);bq.placed("combat");self.apply_lock();self.relayout=True
				else:self.show()
			def metrics(self):s=bP(self.width(),b1,cG)/float(d5);return s,max(10,int(round(fU*s))),fV*cV(s)
			def height(self,n):
				if self.slot is not None and not aN["combat"][5]:return self.slot[1]
				b,a,b=self.metrics()
				if aN["combat"][5]:return ew
				h=cT+u
				if n<=0 and self.empty_lines:return h+max(a+cH,2+dI*len(self.empty_lines))+dp
				return h+max(n,1)*(a+cH)+dp
			def _empty_text(self,W):
				c=max(20,W-2*b_-4);a=ex("No one is fighting you.",c)
				if self.slot is not None:
					b=max(1,(self.slot[1]-u-cT-2)//dI)
					if len(a)>b:a=a[:b-1]+[C(" ".join(a[b-1:]),c)]
				return a
			def _on_resized(self,*a):
				if not self.is_open()or self.slot is not None:return
				w=bP(int(self.gump.GetWidth()),b1,cG)
				if w==aN["combat"][2]:return
				aN["combat"][2]=w;self.relayout=True
			def apply_lock(self):
				if not self.is_open():return
				g,a=self.gump,aN["combat"][4];b=H(self.dock_key)
				if not b:D(g,"CanMove",not a)
				g.SetResizable(not a and not b)
			def set_locked(self,locked):
				if aN["combat"][4]!=locked:aN["combat"][4]=locked;self.apply_lock();self.relayout=True;a0["dirty_save"]=True
			def toggle_minimize(self,*a):
				aN["combat"][5]=not aN["combat"][5]
				if not aN["combat"][5]:self.docked=False
				self.relayout=True;a0["dirty_save"]=True
			def status_text(self,data):
				n=len(data)
				if not aN["combat"][5]or n==0:return "%d"%n
				a,c,d=None,0,0
				for j,k,l,h,e,g,i in data:
					c+=g;d+=i
					if e:f=int(round(h*100./e));a=f if a is None else min(a,f)
				b=["%d"%n]
				if a is not None:b.append("low %d%%"%a)
				if c:b.append("PSN %d"%c)
				if d:b.append("PAR %d"%d)
				return "  ".join(b)
			def build_frame(self,data):
				g=self.gump
				if self.chrome is not None and self.chrome.gump is g:self.chrome.dispose()
				for j in self.rows:j.dispose()
				for c in self.grip:bM(c)
				for c in self.empty or():bM(c)
				g.Clear();self._forget();L=aN["combat"];b=L[5];s,e,k=self.metrics();W=self.width();n=len(data)
				if not b:self.empty_lines=self._empty_text(W)
				H=self.height(n);g.SetWidth(W);g.SetHeight(H);self.fit_n=n;bq.sized("combat",W,H);self.chrome=Chrome(g,kit=True,key="ultima.combat");self.chrome.layout_kit(W,H,L[6],"Combat",eg["combat"],b,self.user_minimize,lambda*a:cr.append("ultima.combat"));self.chrome.set_status(self.status_text(data))
				if b:return
				l=W-2*b_;f=int(round(80*s));h=max(14,e)if au["magery"]else 0;i=l-(2*(h+1)if au["magery"]else 0);self.geo={"y":self.chrome.content_top,"rh":e,"font":k,"info_w":f,"spell_w":h,"bar_w":i,"name_w":i-f-6,"W":W}
				if L[4]:return
				m,o=W-u-9,H-u-9
				for p,q in fz:d=b2(1.,gh);d.SetRect(m+p,o+q,2,2);g.Add(d);self.grip.append(d)
			def fit(self,n):
				n=max(n,0)
				if n==self.fit_n:return
				self.fit_n=n;W,H=self.geo["W"],self.height(n);self.gump.SetHeight(H);bq.sized("combat",W,H);self.chrome.frame.layout(W,H);a,b=W-u-9,H-u-9
				for(c,d),e in zip(fz,self.grip):e.SetRect(a+c,b+d,2,2)
			def make_empty(self):return ey(self.gump,self.empty_lines or[""],b_+4,self.geo["y"]+2)
			def fill(self,data):
				if self.slot is not None:
					a=self.geo;c=self.slot[1]-a["y"]-u-dp;b=max(1,c//max(1,a["rh"]+cH))
					if len(data)>b:data=data[:b]
				self.fit(len(data));PoolWin.fill(self,data)
			def draw(self,data):
				L=aN["combat"];a=(L[2],L[5],L[4],au["magery"],self.slot)
				if self.zone_redraw and self.frame_key is not None and c1():
					if self.chrome is not None:self.chrome.set_status(self.status_text(data))
					if a==self.frame_key and not L[5]and self.geo is not None:self.fill(data)
					return
				if self.relayout or a!=self.frame_key:self.relayout=self.zone_redraw=False;self.build_frame(data);self.frame_key=a
				elif self.chrome is not None:self.chrome.set_title("Combat");self.chrome.set_status(self.status_text(data))
				if not L[5]:self.fill(data)
			def tick(self):
				g=self.gump
				if g is None:del cl[:];return
				if cu():return
				if not E(g):
					self.gump=None;self._drop_notes()
					if H(self.dock_key):return
					au["combat_shown"]=False;a0["dirty_save"]=True;aV("combat bars hidden; Show combat in the %s window brings them back."%bD,o);return
				if((self.made_min>self.slot[0])if self.slot is not None else(self.made_min<b1))and not c1():
					self.snapshot();self.gump=None;self._drop_notes();K(g);self.show()
					if self.docked:D(self.gump,"IsVisible",False)
					return
				hZ();hV();hW();hX();self.draw(fv())
		fz=((6,6),(6,3),(3,6),(6,0),(0,6),(3,3))
		class ControlPanel(object):
			BODY_H=420;FOE_ROW_H=32
			def __init__(self,windows,combat):
				self.windows,self.combat=windows,combat;self.g=self.list_sa=self.input=self.lock_all_lbl=self.combat_lbl=self.foe_title=None;self.store,self.x0,self.w=({},{}),0,0;self.foe_ver=self.seen_ver=-1;self.foe_rows,self.seen_at=[],0.;self.list_top=self.list_h=0;self.list_lbls=();a=HOST.hub
				if a is not None:a.add("ultima",bD,{"height":self.height,"build":self.build_section,"closed":self.section_closed})
				else:aV("couldn't show the Foe list panel (no shared window).",l)
			@property
			def gump(self):return self.g if E(self.g)else None
			@property
			def size(self):a=HOST.hub;return(a.W,a.H)if a is not None else(0,0)
			def height(self,w):return self.BODY_H+16
			def build_section(self,g,x,y,w,store):self.g,self.store=g,store;self.x0,self.w=x+8,w-16;self.list_sa,self.foe_ver=None,-1;O(g,x,y,w,self.height(w));self.build_body(y+8);bq.pending=True
			def section_closed(self):self.g=self.list_sa=self.input=None;self.foe_rows=[]
			def _heading(self,text,y):a=bH(text,13,"#FFD966");bz(a,self.x0+2,y);self.g.Add(a);return a
			def _divider(self,y):d=bK(aI,self.w,4);d.SetPos(self.x0,y);self.g.Add(d)
			def build_body(self,b):g,X,W=self.g,self.x0,self.w;c=int(W/3);self._heading("FOES & IGNORE LIST",b);f=bK(Kit.FIELD_TILE,W,24);f.SetPos(X,b+21);g.Add(f);self.input=API.Gumps.CreateGumpTextBox("",W-4,22,False,16);self.input.SetPos(X+2,b+22);self.input.SetPlaceholder("Player name");U(self.input,"Player name for the buttons below");g.Add(self.input);j="Hide combat"if self.combat.is_open()else "Show combat";k=(("Add foe",0,52,self.add_foe,aF,"Put the typed name on your Foe list"),("Remove foe",1,52,self.remove_foe,Z,"Take the typed name off your Foe list"),("Target...",2,52,self.target_foe,aG,"Target a player to put them on your Foe list"),("Ignore",0,80,self.ignore_name,Z,"Hide the typed name from the trackers (an NPC)"),("Unignore",1,80,self.unignore_name,aF,"Show the typed name in the trackers again"),("Lock all",2,80,self.lock_all,aG,"Lock or unlock every tracker, the combat bars and pop-outs"),(j,0,144,self.toggle_combat,aG,"Show or hide the combat bars"),("Settings",1,144,lambda*a:aD("ultima"),L,a5%bD),("Sightings",2,144,lambda*a:b0.toggle(),L,"Open or close the Sightings window"));d=[self._button(m,X+n*c,b+q,c,r,s,v)for m,n,q,r,s,v in k];self.lock_all_lbl,self.combat_lbl=d[5],d[6];self._divider(b+110);self._heading("WINDOWS",b+120);self._divider(b+176);self.foe_title=self._heading("SAVED FOES (0)",b+186);self.list_top=b+210;e=b+self.BODY_H;h=max(16,bu.get("font_h",0)if c0(11)else 0);self.list_h=e-h-14-self.list_top;i=bH("Alt+click any bar: auto-follow (again to stop).",11,cQ);bz(i,X+2,e-h-6);g.Add(i);self.foe_ver=a0["foe_ver"];self.rebuild_foe_list()
			def _button(self,text,x,y,w,fn,art,tip=None):a=ai(art[0])[0]or 30;b="ut:"+text.lower().replace(" ","_").rstrip(".");return P(self.g,self.store,b,art,x,y,C(text,max(10,w-a-6)),tip,on_click=bt(fn))
			def _typed(self):return(safe(lambda:self.input.Text,"")or "").strip()
			def _clear_input(self):safe(lambda:self.input.SetText(""))
			def add_foe(self,*a):
				n=self._typed()
				if not n:aV("type a name first.",l);return
				dU(n);self._clear_input();aV("added %s to the Foe list."%n,A)
			def remove_foe(self,*a):
				n=self._typed()
				if n:self._remove(z(n));self._clear_input()
			def _remove(self,key):
				if key in f:
					e6(key)
					if bU[0]==key:bU[0]=None
					a=hl(key);aV("removed %s from the Foe list."%a,A)
				else:aV("%s isn't on the Foe list."%key,l)
			def target_foe(self,*a):aV("target a player for your Foe list.",o);HOST.pick_target(10,self._foe_targeted)
			def _foe_targeted(self,serial):
				a=API.FindMobile(serial)if serial else None
				if not a or not a.Name:aV("no player targeted.",l);return
				dU(a.Name);aV("added %s to the Foe list."%a.Name,A)
			def ignore_name(self,*a):
				n=self._typed()
				if n:M[n.lower()]=n;bI();self._clear_input();aV("ignoring %s from now on."%n,A)
			def unignore_name(self,*a):
				n=self._typed()
				if n and n.lower()in M:M.pop(n.lower());bI();self._clear_input();aV("no longer ignoring %s."%n,A)
			def _all_locked(self):
				a=[b.locked for b in self.windows.values()]
				if self.combat.is_open():a.append(aN["combat"][4])
				a.extend(c.locked for c in br.values());return all(a)
			def lock_all(self,*b):
				a=not self._all_locked()
				for w in self.windows.values():w.set_locked(a)
				self.combat.set_locked(a)
				for p in list(br.values()):p.set_locked(a)
				self.refresh_labels()
			def toggle_combat(self,*b):
				a=self.combat
				if a.is_open()and H(a.dock_key):return
				(a.hide if a.is_open()else a.show)();self.refresh_labels()
			def refresh_labels(self):
				if self.gump is None or self.lock_all_lbl is None:return
				j(self.lock_all_lbl,"Unlock all"if self._all_locked()else "Lock all");j(self.combat_lbl,"Hide combat"if self.combat.is_open()else "Show combat")
			def reset_defaults(self,*b):
				eA()
				for p in br.values():p.opacity,p.locked=bS,False
				for w in self.windows.values():
					if w.docked:w.docked=False;X(w.dock_key)
				a=self.combat.docked
				if a:self.combat.docked=False;X(self.combat.dock_key)
				d1(self.windows);self.combat.reset()
				if a and self.combat.is_open():D(self.combat.gump,"IsVisible",True)
				if HOST.hub is not None:HOST.hub.refresh()
				eQ();bI();aV("settings and windows reset to the defaults.",A)
			def set_all_opacity(self,v):
				au["opacity"]=v
				for w in self.windows.values():w.apply_opacity(v)
				for a in br.values():a.apply_opacity(v)
				self.combat.apply_opacity(v);aN["panel"][6]=v;a0["dirty_save"]=True
			def rebuild_foe_list(self):
				if self.gump is None:return
				K(self.list_sa)
				for b in self.list_lbls:bG.pop(id(b),None)
				self.list_lbls=i=[];self.list_sa=API.Gumps.CreateGumpScrollArea(self.x0,self.list_top,self.w,self.list_h);self.g.Add(self.list_sa);self.foe_rows=[];j=sorted(f.items(),key=lambda a:a[1].lower());bR(self.foe_title,"SAVED FOES (%d)"%len(j))
				if not j:b=bH("No foes yet. Type a name and press Add foe.",12,"#888888");i.append(b);bz(b,2,2);self.list_sa.Add(b);return
				m=time.time();o=self.w-d4;p=set(bd.values());e=self.list_sa
				for q,(c,d)in enumerate(j):
					y=q*self.FOE_ROW_H;b=bH(dJ(F(d),24),13,"#FF9090");i.append(b);bz(b,2,y+2);e.Add(b);g=o-22;b3(e,g,y,18,18,"x",self._foe_btn(c,d,self._remove),"Take %s off your Foe list. %s"%(F(d),bW));g-=22;l=bU[0]==c;b3(e,g,y,18,18,"L*"if l else "L",self._foe_btn(c,d,self.link_click),("Press L on the other entry (L here again: cancel). "if l else "Link as one person: L here, then L on the other entry. ")+bW,face=cO if l else co)
					if c in bd or c in p:g-=22;b3(e,g,y,18,18,"U",self._foe_btn(c,d,self.unlink_click),"Unlink from its group. "+bW)
					e.Add(bQ(0,y,max(20,g-6),18,(lambda k,n:(lambda*a:self.foe_name_click(k,n)))(c,d),bZ(hP,d)));h=bH(self.foe_info(c,m),11,cQ,maxWidth=o-6);i.append(h);bz(h,2,y+17);e.Add(h);self.foe_rows.append((c,h))
				self.seen_ver=bn["seen_ver"];self.seen_at=m+ea
			def _foe_btn(self,k,n,fn):return lambda*a:self.foe_name_click(k,n)if bN()else fn(k)
			@staticmethod
			def foe_info(key,now):a=dT(key);b=hg(key,now);return a+"; "+b if a else b
			def link_click(self,key):
				if key not in f:return
				a=bU[0]
				if a is None or a not in f:bU[0]=key;aV("press L on the entry to link with %s."%f[key],o)
				elif a==key:bU[0]=None;aV("linking cancelled.",o)
				else:bU[0]=None;aV(hh(a,key),A);bI()
				a0["foe_ver"]+=1
			def unlink_click(self,key):
				if key in f and e6(key):aV("%s is no longer linked."%f[key],A);bI();a0["foe_ver"]+=1
			def foe_name_click(self,key,name):
				if bN():
					a,b=None,-1.
					for s,k in ct.items():
						if k==key and API.FindMobile(s)is not None:
							t=cb.get(s,0.)
							if t>b:a,b=s,t
					if a is not None:ch(a)
					else:aV("%s isn't in range."%name,l)
					return
				safe(lambda:self.input.SetText(name))
			def update(self):
				if self.gump is None:return
				if self.foe_ver!=a0["foe_ver"]:self.foe_ver=a0["foe_ver"];self.rebuild_foe_list()
				elif self.foe_rows:
					a=time.time()
					if self.seen_ver!=bn["seen_ver"]or a>=self.seen_at:
						self.seen_ver=bn["seen_ver"];self.seen_at=a+ea
						for b,c in self.foe_rows:bR(c,self.foe_info(b,a))
				self.refresh_labels()
		class SightRow(object):
			__slots__=("serial","name","prev","e","c","nm","here")
			def __init__(self):self.serial,self.name,self.prev,self.e=None,"",None,None;self.c,self.nm,self.here={},"",None
		def h2(serial,name):return cx(serial,lambda:b0.filter_name(name,serial))
		fA=26+cJ*22+6;dh=2*u+30+36+fA+36+3*J;fB=dh-(cJ-1)*22
		def fC(obj,w,h,mode):
			a=(int(w),int(h))if(w is not None and h is not None)else None
			if a!=obj.slot or(mode=="again"and a is not None):obj.slot=a;obj.redraw=True
		def fD(obj,a,b):
			z=obj.slot
			if z is None or obj.st["minimized"]or not H(obj.KEY)or z[0]<a or z[1]<b:return
			return z
		class SightingsWindow(object):
			KEY="ultima.sightings";TITLE="Sightings";W=480;MINI_W,MINI_H=300,46;COLS=(8,92,230,278,404)
			def __init__(self):self.st={"minimized":False,"docked":False,"shutting":True};self.win={"g":None};self.slot,self.want,self.n,self.w=None,False,cJ,self.W;self.hooks=ba(self.TITLE,f3,self.st,self.win,self.ask_redraw,self.fit);self.hooks.update(show=self.zone_show,min=(self.W,fB));self.flt={"text":"","noto":0,"time":0};self.fser,self.fshow=None,"";self.forget()
			def fit(self,w,h,mode):fC(self,w,h,mode)
			def zone_show(self):self.want=True
			def forget(self):self.c,self.store,self.rows={},({},{}),[];self.page,self.matches,self.counts=0,[],{};self.ver,self.ver_at,self.dirty,self.redraw=None,0.,True,False;self.full_at=self.here_at=self.poll_at=0.
			def is_open(self):return self.win["g"]is not None
			def ask_redraw(self):self.redraw=True
			def toggle(self):
				if not self.is_open():self.show()
				elif self.st["minimized"]or self.st["docked"]:self.bring()
				elif not H(self.KEY):self.close()
			def bring(self):
				if not self.is_open():self.show()
				if self.st["minimized"]or self.st["docked"]:X(self.KEY);self.st["minimized"]=self.st["docked"]=False;ar(cK,False);self.build()
			def show(self):
				if self.is_open():return
				a=H(self.KEY);self.st.update(shutting=False,docked=False,minimized=not a and bool(be(cK)or HOST.dock_wanted(self.KEY)));self.build();aR(cL,"1")
			def save_pos(self):
				if not H(self.KEY):at(dA,self.win["g"])
			def close(self,stopping=False):
				g=self.win["g"]
				if g is None:return
				self.st["shutting"]=True
				if not stopping:X(self.KEY);aR(cL,"0")
				if not H(self.KEY):at(dA,g);ar(cK,self.st["minimized"])
				self.win["g"]=None;self.forget();K(g)
			def lost(self):self.win["g"]=None;self.st["shutting"]=True;aR(cL,"0");self.forget()
			def build(self):
				self.redraw=False;d=self.win["g"];x,y=bf(dA,(320,160),(self.W,dh))
				if E(d):x,y=d.GetX(),d.GetY()
				self.win["g"]=None;self.forget();a,c,n=self.store,self.c,self.rows;M,j=u,J;g=G.CreateGump(True,True);self.n,self.w=cJ,self.W
				if self.st["minimized"]:w,h=self.MINI_W,self.MINI_H;c["status"]=bi(g,a,w,h,self.TITLE,self.KEY,bt(self.toggle_min),close_tip="Close Sightings")
				else:
					z=fD(self,self.W,fB);w,h=z if z else(self.W,dh);k=h-dh+fA;self.n=max(1,(k-32)//22);self.w=w;e=w-2*M;a7(g,w,h);Kit.title_bar(g,a,w,self.TITLE,self.KEY,bt(self.toggle_min),bt(lambda:a_(self.KEY,self.TITLE)),bt(lambda:aD("ultima")),close_tip="Close Sightings");b=M+30+j;O(g,M,b,e,36);B(g,"Find:",M+10,b+9);c["find"]=U(Kit.add_textbox(g,self.find_view(),M+52,b+7,128,numbers=False),"Part of a name: list only that player");c["noto"]=P(g,a,"noto",L,M+196,b+7,dw[self.flt["noto"]][0],"Which players to list (click to cycle)",on_click=bt(lambda:self.cycle("noto",dw)));c["time"]=P(g,a,"time",L,M+326,b+7,dz[self.flt["time"]][0],"How far back to list (click to cycle)",on_click=bt(lambda:self.cycle("time",dz)));f=b+36+j;O(g,M,f,e,k)
					for l,p in zip(self.COLS,("Time","Player","Colour","Where","Count")):B(g,p,M+l,f+6,ap)
					for q in range(self.n):
						m=f+26+q*22;r=SightRow()
						for s,l,t in(("t",0,o),("n",1,N),("o",2,N),("p",3,o),("k",4,o)):r.c[s]=B(g,"",M+self.COLS[l],m+2,t)
						r.c["hit"]=ah(g,M+4,m,e-8,22,bt(RowClick(r,h2)),fk);n.append(r)
					i=f+k+j;O(g,M,i,e,36);P(g,a,"newer",L,M+10,i+7,"Prev","Newer sightings",on_click=bt(self.newer));P(g,a,"older",L,M+120,i+7,"Next","Older sightings",on_click=bt(self.older));c["status"]=B(g,"",M+230,i+10,o)
				bk(g,x,y,w,h,self.KEY,self.st["minimized"]and self.st["docked"],None,self.save_pos,self.win,{"g":g});K(d);self.refresh(time.time(),True)
			def toggle_min(self,*a):Kit.win_action("toggle_min",self.st,self.KEY,self.TITLE,self.build,cK)
			def cycle(self,k,table):
				self.flt[k]=(self.flt[k]+1)%len(table)
				if k in self.c:j(self.c[k],table[self.flt[k]][0])
				self.page,self.dirty=0,True
			def newer(self,*a):
				if self.page>0:self.page-=1;self.dirty=True
			def older(self,*a):
				if(self.page+1)*self.n<len(self.matches):self.page+=1;self.dirty=True
			def find_view(self):a=self.flt["text"];self.fshow=Q("name",a,self.fser)if a and self.fser else a;return self.fshow
			def filter_name(self,name,serial=None):
				a=""if self.flt["text"].lower()==name.lower()else name;b=self.c.get("find");self.flt["text"],self.fser=a,(serial if a else None);c=self.find_view()
				if b is not None:safe(lambda:b.SetText(c))
				self.page,self.dirty=0,True
			def tick(self,now):
				if self.want:
					self.want=False
					if H(self.KEY):
						if not self.is_open():self.show()
						elif self.st["minimized"]or self.st["docked"]:self.st["minimized"]=self.st["docked"]=False;self.build()
				if self.win["g"]is None:return
				if aa(self.store,"close"):self.close();return
				if self.redraw:self.build();return
				if now<self.poll_at<=now+cn:return
				self.poll_at=now+cn
				if not E(self.win["g"]):self.lost();return
				if self.st["minimized"]and self.st["docked"]:return
				self.refresh(now)
			def refresh(self,now,force=False):
				c=self.c
				if self.st["minimized"]:
					if force or bn["ver"]!=self.ver or now>=self.full_at:
						self.ver,self.full_at=bn["ver"],now+d9;n=len(bF);a="%s: %d"%(self.TITLE,n)
						if n:e=bF[-1];a+=", last %s %s"%(F(e[dc],e[db]),dS(e[cj],dR(now)))
						else:a="%s: none yet"%self.TITLE
						j(c["status"],C(a,self.MINI_W-90))
					return
				b=c.get("find")
				if b is not None:
					d=str(b.Text or "").strip()
					if d!=self.fshow:self.flt["text"]=self.fshow=d;self.fser=None;self.page,self.dirty=0,True
				if force or self.dirty or now>=self.full_at or(bn["ver"]!=self.ver and not 0.<=self.ver_at-now<=1.):self.ver_at=now+1.;self.work_out(now);self.fill(now)
				elif now>=self.here_at:self.mark_here(now)
			def work_out(self,now):
				self.dirty=False;self.ver,self.full_at=bn["ver"],now+d9;a=dz[self.flt["time"]][1];g=None if a is None else(dR(now)if a=="today"else now-a);b=dw[self.flt["noto"]][1];h=z(self.flt["text"]);c,d=[],{}
				for j in range(len(bF)-1,-1,-1):
					e=bF[j]
					if g is not None and e[cj]<g:break
					if h and h not in e[ck]:continue
					if b is not None and(e[ck]not in f if b=="foe"else e[cC]not in b):continue
					c.append(e);d[e[ck]]=d.get(e[ck],0)+1
				self.matches,self.counts=c,d;i=max(0,(len(c)-1)//self.n)
				if self.page>i:self.page=i
			def fill(self,now):
				d=dR(now);a=self.page*self.n;m=self.matches
				for i,r in enumerate(self.rows):c=a+i;self.assign(r,m[c]if c<len(m)else None,d)
				self.mark_here(now);n=len(m)
				if n:b="%d-%d of %d, %s"%(a+1,min(n,a+self.n),n,R(len(self.counts),"name"))
				elif bF:b="No sightings match the filters"
				else:b="No sightings yet"if au["sightings"]else "Logging is off (settings page)"
				j(self.c["status"],C(b,self.w-2*u-236))
			def assign(self,r,e,a):
				c=r.c
				if e is None:
					if r.e is not None:
						r.prev=(r.serial,r.name,time.time());r.e,r.serial,r.name,r.nm,r.here=None,None,"","",None
						for k in("t","n","o","p","k"):j(c[k],"")
					return
				if e is not r.e:
					if r.serial is not None and r.serial!=e[db]:r.prev=(r.serial,r.name,time.time())
					r.e,r.serial,r.name=e,e[db],e[dc];r.here=None;r.nm=C(af(e[dc],e[db],e[cC]),124);j(c["o"],e2(e[cC]),aL(e[cC],aT.get(e[cC],N)));b=Q("place",e3(e[eY],e[eZ],e[e_]));j(c["p"],C(b+(" G"if e[dP]else ""),118));g=e[dP];d="Seen %s at %s%s"%(dS(e[cj],a),b,", in a guard zone (G)"if g else(", outside the guards"if g is False else ""));U(c["hit"],bZ(fk,e[dc],d))
				j(c["t"],dS(e[cj],a));j(c["k"],"x%d"%self.counts.get(e[ck],1))
			def mark_here(self,now):
				self.here_at=now+1.
				for r in self.rows:
					if r.e is None:continue
					t=cb.get(r.serial);a=t is not None and now-t<=2*cn+.05
					if a!=r.here:r.here=a;j(r.c["n"],r.nm,A if a else N)
		class KillerWindow(object):
			KEY="ultima.killer";TITLE="Add my killer";W=340;MINI_W,MINI_H=260,46;ROW_H=26
			def __init__(self):self.st={"minimized":False,"docked":False,"shutting":True};self.win={"g":None};self.store,self.c,self.cands=({},{}),{},[];self.until,self.slot=0.,None;self.redraw=self.want=False;self.hooks=ba(self.TITLE,0,self.st,self.win,self.ask_redraw,self.fit);self.hooks.update(show=self.zone_show,min=(self.W,self.height(1)))
			def ask_redraw(self):self.redraw=True
			def zone_show(self):self.want=True
			def fit(self,w,h,mode):fC(self,w,h,mode)
			def held(self):return H(self.KEY)
			def height(self,n):return 2*u+30+J+8+n*self.ROW_H+26
			def open(self,got,now,total=None):self.cands=[{"name":b[0],"serial":b[2]}for b in got];self.until=now+f4;self.st.update(shutting=False,docked=False,minimized=not self.held()and be(dC));self.build();n=len(got)if total is None else total;aV("you died; %s attacked you (see %s)."%(R(n,"player"),self.TITLE),l)
			def save_pos(self):
				if not self.held():at(dB,self.win["g"])
			def close(self):
				g=self.win["g"]
				if g is None:return
				if not self.held():at(dB,g);ar(dC,self.st["minimized"])
				self.st["shutting"]=True;self.win["g"],self.c,self.cands=None,{},[];K(g)
			def end(self):
				if not self.held():self.close()
				elif self.cands:self.cands=[];self.build()
			def build(self):
				d=self.win["g"];q=self.st["minimized"];j=fD(self,self.W,self.height(1));W,H=j if j else(self.W,self.height(max(1,len(self.cands))));t,v=Kit.screen();k=self.cands[:max(1,(H-self.height(0))//self.ROW_H)]if j else self.cands;x,y=bf(dB,(max(0,((t or 1024)-W)//2),max(0,((v or 768)-H)//3)),(W,H))
				if E(d):x,y=d.GetX(),d.GetY()
				self.win["g"]=None;c,m=({},{}),{};M=u;g=G.CreateGump(True,True)
				if q:W,H=self.MINI_W,self.MINI_H;w=len(self.cands);m["status"]=bi(g,c,W,H,self.TITLE,self.KEY,bt(self.toggle_min),"%s: %s"%(self.TITLE,R(w,"attacker")),close_tip="Close the attacker list")
				else:
					e=W-2*M;a7(g,W,H);O(g,M,M,e,30);B(g,self.TITLE.upper(),M+30,M+7,ap)
					if aS(self.KEY):ah(g,M,M,e,30,lambda*a:None,None,movable=True)
					else:Kit.title_catcher(g,M,M,W-M-80-M,30,bt(self.toggle_min),key=self.KEY);P(g,c,"min",aE,W-M-74,M+7,None,aH,on_click=bt(self.toggle_min));P(g,c,"close",Z,W-M-54,M+4,None,"Close the attacker list")
					h=M+30+J;O(g,M,h,e,H-h-M);r="Add to foes";n=W-M-10-(35+T(r))
					for i,b in enumerate(k):p=h+8+i*self.ROW_H;A=z(b["name"])in f;s=aP(V(aB(b["serial"])))if Kit.cblind and b["serial"]else "";B(g,C((s+" "if s else "")+F(b["name"],b["serial"]or 0),n-M-30),M+10,p+3,l);ah(g,M+6,p,n-M-14,22,bt(self.make_follow(i)),bZ("Alt+click: auto-follow (again to stop)",b["name"]));m["add%d"%i]=P(g,c,"add%d"%i,aF,n,p,"On Foe list"if A else r,"Put %s on your Foe list. Alt+click: auto-follow (again to stop)"%F(b["name"],b["serial"]or 0),on_click=bt(self.make_add(i)))
					D="Closes on resurrection."if k else C("Lists your attackers when you die."if au["killer"]else "Off (settings page)",e-20);B(g,D,M+10,h+8+len(k)*self.ROW_H+2,o)
				bk(g,x,y,W,H,self.KEY,q and self.st["docked"],None,self.save_pos);self.win["g"],self.store,self.c=g,c,m;self.redraw=False;K(d)
			def make_add(self,i):
				def a(*c):
					if i>=len(self.cands):return
					if bN():self.make_follow(i)();return
					a=self.cands[i]
					if z(a["name"])in f:aV("%s is already on the Foe list."%a["name"],o)
					else:dU(a["name"]);aV("added %s to the Foe list."%a["name"],A)
					b=self.c.get("add%d"%i)
					if b is not None:j(b,"On Foe list")
				return a
			def make_follow(self,i):
				def a(*b):
					if i>=len(self.cands)or not bN():return
					a=self.cands[i];s=a["serial"]
					if s is None:s,c=fd(a["name"])
					if s is None:aV("%s isn't in sight."%a["name"],l)
					else:ch(s)
				return a
			def toggle_min(self,*b):a=self.st;a["minimized"]=not a["minimized"];ar(dC,a["minimized"]);self.build()
			def tick(self,now):
				if self.want:
					self.want=False;a=self.st
					if self.held()and(self.win["g"]is None or a["minimized"]or a["docked"]):a.update(shutting=False,minimized=False,docked=False);self.build()
				g=self.win["g"]
				if g is None:return
				if aa(self.store,"close"):self.close()
				elif not E(g):self.win["g"],self.c,self.cands=None,{},[];self.st["shutting"]=True
				elif not self.cands and not self.held():self.close()
				elif self.redraw:self.build()
				elif self.cands and now>=self.until:self.end()
		b0=SightingsWindow();b8=KillerWindow()
		def fE():return tuple(tuple(a)for b,a in sorted(aN.items()))
		bo={"f":None,"seen":None,"stable":0,"loaded":False,"lines":None,"save_at":0.}
		def h3():
			if a0["started"]or bo["loaded"]:return
			fJ();bo["loaded"]=True
			def a():
				try:bo["lines"]=eS()
				except Exception as a:c7[0]="could not read the save file: "+str(a);bo["lines"]=()
			eR(a)
		def h4():
			a=bo["lines"]
			if a is None:return False
			bo["lines"]=None
			if a0["started"]or not a:return False
			eU(a[0],a[1]);return True
		def b9():
			if a0["started"]:a0["dirty_save"]=True
			else:bo["save_at"]=time.time()+gc
		def fF(background):
			if bo["save_at"]:bo["save_at"]=0.;da(background=background)
		def h5():return all(bool(aN[a][4])for a in bE+["combat"])
		iq={};fG={"top":32,"pad":6,"ldy":0,"sdy":4,"fh":26,"lw":110,"ugap":6}
		def fH(w):a={"dx":320,"bdy":0,"h":26};b="Sort: "+et[au["sort"]];return(("WINDOWS",(("slider","scale","Scale:","Size of the trackers and pop-out bars (%d-%d)"%(dj,dk),dj,dk,{"unit":"%"}),("slider","opacity","Opacity:","Background opacity of every window (0-100)",0,100,{"unit":"%"}),("slider","range","Range:","Tracker range in tiles (%d-%d)"%(dl,dm),dl,dm,{"unit":"tiles"}),("gap",-78),("check","sync","Sync tracker sizes","Resizing one tracker resizes the others",a),("buttons",(("unanchor",Z,"Unanchor all","Undo every anchor between windows"),),a),("buttons",(("reset",Z,"Reset to defaults","Reset scale, opacity, range, options and window places"),),a),("check","lock","Lock the windows in place","Free windows can't be moved or resized (zoned windows stay put anyway)"))),("OPTIONS",(("check","combat_only","Combat bars: only once fighting","Only add a mobile once it attacks you, you attack it in war mode, or it fights you up close",{"stay":True}),("check","borders","Show a border on the pop-out bars","Stone border round the pop-out bars (the other windows always have one)",{"dx":320,"h":28}),("check","magery","Magery buttons","P (Poison) and Z (Paralyze) on the combat bars; H (Heal) and C (Cure) on friends, Shift+click for the greater spell",{"stay":True}),("check","healing","Bandage button","B on friends' bars: bandage when adjacent, else follow them",{"dx":320}),("buttons",(("sort",L,b,"Order of the tracker lists (name, distance or HP)"),)))),("SIGHTINGS AND DEATHS",(("check","sightings","Log players who come into range","Each non-friend player goes in the Sightings log once per visit (last %d kept)"%cI,{"stay":True}),("buttons",(("sightings",L,"Open Sightings","Open the Sightings window"),),{"dx":320}),("check","killer","On death: list your attackers","A window lists players who attacked you in the last %d s, each with Add to foes"%int(dv)))),("FOE ALERT  (sound: Settings > Alerts)",(("check","alert_red","Red","Alert on a red (murderer) in range",{"stay":True}),("check","alert_foes","Foe list","Alert on a Foe list player in range (linked alts too)",{"stay":True,"dx":110}),("check","alert_orange","Orange","Alert on an orange (enemy) in range",{"stay":True,"dx":230}),("check","alert_gray","Grey","Alert on a grey (criminal) in range",{"dx":340,"h":28}),("slider","alert_minutes","Same player again after:","Minutes before the same player alerts again (%d-%d)"%(ds,dt),ds,dt,{"lw":178,"sw":150,"ugap":12,"unit":"%d min"%au["alert_minutes"]}))))
		h6=Kit.Page(au,fH,opts=fG)
		def h7(g,x,y,w):h3();bo.update({"f":Kit.Form(g,x,y,w,dict(au,lock=h5()),fH(w),**fG),"stable":0,"seen":{a:au[a]for a in es}})
		def h8():
			f=bo["f"]
			if f is None:return
			if h4():bo["f"]=None;aC("ultima");return
			c9();m=time.time()
			if bo["save_at"]and m>=bo["save_at"]:fF(True)
			h,a=f.store,bo["seen"];b=a8["windows"]
			if aa(h,"unanchor"):bq.clear();b9();aV("every window unanchored.",A)
			if aa(h,"reset"):
				if a8["panel"]is not None:a8["panel"].reset_defaults()
				else:eA();b9();aV("settings and windows reset to the defaults.",A)
				aC("ultima");return
			f.vals=dict(au,**a);c=f.read();g=c["scale"]
			if g!=a["scale"]:a["scale"]=g;bo["stable"]=0
			elif g!=au["scale"]:
				bo["stable"]+=1
				if bo["stable"]>=2:
					if b is not None:hS(g,b)
					else:au["scale"]=g;b9()
			i=c["opacity"]
			if i!=a["opacity"]:
				a["opacity"]=i
				if a8["panel"]is not None:a8["panel"].set_all_opacity(i)
				else:au["opacity"]=i;b9()
			for k in("range","alert_minutes"):
				if c[k]==a[k]:continue
				a[k]=au[k]=c[k];b9()
				if k=="alert_minutes":j(f.c["alert_minutes_lbl"],"%d min"%c[k])
			if aa(h,"sort"):au["sort"]=(au["sort"]+1)%len(et);b9();aC("ultima");return
			if aa(h,"sightings"):
				if a8["windows"]is not None:bC["sight_req"]=True
				else:aV("the trackers aren't up yet; try again in a moment.",o)
			d=bool(c.get("lock"))
			if a.get("lock")is None:a["lock"]=d
			elif d!=a["lock"]:
				a["lock"]=d
				if b is not None:
					for k in bE:b[k].set_locked(d)
				if a8["panel"]is not None:a8["panel"].combat.set_locked(d)
				else:
					for k in bE+["combat"]:aN[k][4]=d
				bI()
			for e in("borders","healing","magery","combat_only","sync","alert_red","alert_foes","alert_orange","alert_gray","sightings","killer"):
				v=c[e]
				if v==au[e]:continue
				au[e]=v;b9()
				if e=="borders":eQ()
				elif e=="healing"and not v:bp["serial"]=None
				elif e=="sync"and v and b is not None:l=[b[n]for n in bE if not b[n].minimized];fo(b,l[0]if l else b[bE[0]]);aV("tracker sizes synced.",A)
		def h9():bo["f"]=None;fF(True)
		bC={"last_layout":None,"tick":0,"errors":set(),"next_scan":0.,"next_combat":0.,"next_glow":0.,"sight_req":False,"next_hp":0.}
		def di(key,step,now):
			t=bC[key]
			if now<t<=now+step:return False
			bC[key]=t+step if 0<=now-t<step else now+step;return True
		def ia():
			c,d,b=a8["windows"],a8["combat"],a8["panel"];a={g:(c[g].gump,c[g].size)for g in bE}
			if d.is_open():a["combat"]=(d.gump,(aN["combat"][2],0))
			if b.gump is not None:a["panel"]=(b.gump,b.size)
			for s,e in br.items():a["pop:%d"%s]=(e.gump,e.size)
			return a
		def fI():
			for w in(a8["windows"]or{}).values():w.snapshot()
			if a8["combat"]is not None:a8["combat"].snapshot()
		def ib(view,title,fit):
			def c():
				if view.gump is None or a0.get("shutting"):return
				return "docked"if view.docked else("minimized"if view.minimized else "open")
			def b(on):D(view.gump,"IsVisible",on)
			def a(docked,mini):
				def f():
					if view.minimized!=mini:view.toggle_minimize()
					view.docked=docked;b(not docked)
				return f
			def d():view.docked=False;b(True)
			def e():
				if view.gump is None and view is a8["combat"]:cf.append(view.show)
				else:a(False,False)()
			return{"title":title,"icon":0,"state":c,"show":e,"dock":a(True,True),"undock":d,"minimize":a(False,True),"gump":lambda:view.gump,"fit":fit,"exact":True,"verify":True,"redraw":view.zone_chrome}
		def ic(windows,combat):
			for c,w in list(windows.items())+[("combat",combat)]:aY("ultima."+c,ib(w,ef[c],w.layout_fit));ca.add(aZ,"ultima."+c)
			for a,b in(("ultima.sightings",b0.hooks),(b8.KEY,b8.hooks)):aY(a,b);ca.add(aZ,a)
		def fJ():
			for d in(f,M,I,br,bT,bJ,cc,ae,cD,bv,bd,cU,bx,b5):d.clear()
			b6[0]=None;dN[0]=ci[0]=0.;cB[0]=0
			for q in(cr,cl,b7,bY,cX,cw,cf,bF):del q[:]
			cE[0]+=1;ez();au.update(ev);bb.update(req=False,size={},own_size={},force=set(),made={});a0.update(gB,party=set());bp.update(serial=None,follow=None);bq.__init__();bB.update(serial=None,stale=False);ce[0]=c8[0]=False;bo.update({"loaded":False,"lines":None,"save_at":0.});bL["learn"]=bL["attack"]=bL["killer"]=None;fu.update(serial=None,until=0.);fb[0]=-10.
			for a in list(b4):bX(a)
			bn.update(dirty=False,save_at=0.);bn["ver"]+=1;bn["seen_ver"]+=1;bU[0]=None;bA["dead"]=bA["me"]=None
		def ie():
			a=None
			if bo["save_at"]:bo["save_at"]=0.;a=eW()
			fJ();a0["started"]=True
			for k in bL:bL[k]=ao()
			gI();bC["errors"]=set();az(d7,"Foe in range",f1);ca.service("ultima.is_foe",hm);ca.service("ultima.classify",hp);ca.service("look.ultima",lambda:cf.append(hQ));cw.append(lambda:ig(a))
		def ig(a=None):
			if a0["shutting"]:return
			if a is not None:cA[0]+=1;eX(a,cA[0]);c9()
			gW();bq.saved=bq.saved_groups();g5();a0["loaded"]=True
		def ih():
			if a8["windows"]is None:
				if a0["loaded"]and not a0["shutting"]:g9()
				return
			c9();gH();eC(cf)
			while cr:a_(cr.pop(0))
			if dH:del dH[:];aD(fK)
			b,d,i=a8["windows"],a8["combat"],a8["panel"]
			if b is None:return
			hT(b);a=time.time()
			try:
				try:
					if bC["sight_req"]:bC["sight_req"]=False;b0.bring()
					b0.tick(a);b8.tick(a)
				except Exception as c:
					if an():return
					cd(c)
				h0();gR();bq.tick(ia)
				if bq.groups_changed():a0["dirty_save"]=True
				if di("next_glow",gl,a):
					f=fh();b["friend"].pulse(f)
					for e in list(br.values()):e.pulse(f)
				if di("next_scan",cn,a):
					j=hv()
					try:hB(a)
					except Exception as c:cd(c)
					if cu():return
					for g in bE:b[g].update(j[g])
					for e in list(br.values()):e.update()
					if cu():return
					hR(b);i.update();gS();bC["tick"]+=1
					if bC["tick"]%fT==0:
						fI();h=fE()
						if h!=bC["last_layout"]or a0["dirty_save"]or(bn["dirty"]and a>=bn["save_at"]):bC["last_layout"]=h;bI()
				if di("next_combat",cn if d.docked else fM,a)and not cu():d.tick()
				if di("next_hp",fN,a)and not cu():ii(b,d)
			except Exception as c:
				if an():return
				cd(c)
		def ii(windows,combat):
			for w in windows.values():
				if w.minimized or w.docked or not E(w.gump):continue
				for r in w.rows:
					e=r.e
					if not r.shown or not e or not e["hmax"]or e.get("mob")is None:continue
					try:c,b=e["mob"].Hits or 0,e["mob"].HitsMax or 0
					except Exception:continue
					if b>0:e["hits"],e["hmax"]=c,b;r.values(e)
			if combat is None or combat.docked or combat.minimized or not E(combat.gump):return
			for r in combat.rows:
				d=r.e
				if not r.shown or d is None:continue
				m=dg.get(d[0])
				if m is None:continue
				try:a=(m.Hits or 0,m.HitsMax or 0)
				except Exception:continue
				if a[1]>0 and a!=d[3:5]:r.values(d[:3]+a+d[5:])
		def ij():
			if eC(cw):return
			if ce[0]:ce[0]=False;da(background=True)
		def ik():return bool(cw)or bool(ce[0])
		def il():
			a0["shutting"]=True;a0["started"]=False;b0.close(stopping=True);b8.close();ca.close()
			for c in list(b4):bX(c)
			if a8["windows"]is None:return
			safe(lambda:Kit.on_client(fI));ce[0]=False;da();a=[]
			for w in a8["windows"].values():a.append(w.gump);w.gump=None
			if a8["combat"]is not None:a.append(a8["combat"].gump);a8["combat"].gump=None
			if HOST.hub is not None:HOST.hub.remove("ultima")
			for b in list(br.values()):a.append(b.gump);b.gump=None
			br.clear()
			for g in a:K(g)
			cy(bp["follow"]);a8.update({"windows":None,"combat":None,"panel":None})
		return{"start":ie,"tick":ih,"stop":il,"client_tick":True,"config_height":h6.height,"build_config":h7,"poll_config":h8,"config_closed":h9,"thread_tick":ij,"thread_wanted":ik}
	def bG():
		aV="lookout";q="Lookout";ab="Lookout_settings";aW="Lookout_pos";aX="Lookout_min";aY="_lookout_feed.txt";W=370;ac,aZ=280,46;a_=2597;H=5;a1=30;s=22;I,K=3,24;a2=.25;ad=30.;ae=5.;t=20.;a3=.1;ag=15.;ai=32768;ak=60;f=65536;a4=30.;a5=120.;an=10.;ao=200;L=1.;M=400;a6=1000;ap=8;aq=10.;ar=.25;at="lookout.alarm";a7=824;au="lookout.lost";ba=74;av=60.;v=0x4C4F4F4B;be=("Click: tracking arrow to where they were seen (again to clear). Alt+click: auto-follow (again to stop)");c={"watch":False,"listen":True,"range":18,"ping":True,"lost":True};bI=dict(c)
		def aw():return{"shutting":False,"minimized":False,"docked":False,"queue":[],"me":0,"path":None,"facet":-1,"next_scan":0.,"present":{},"in_range":0,"hb_next":0.,"outbox":[],"write_next":0.,"pings":[],"ping_next":0.,"listeners":{},"listeners_next":0.,"offset":0,"listen_next":0.,"announce_next":0.,"seen":{},"inbox":[],"watchers":{},"file":"none","recent":[],"arrow":None,"own_alarm":None,"dirty":True,"refresh_at":0.}
		b={"minimized":False,"shutting":False,"docked":False,"queue":[]};b.update(aw());d={"g":None,"c":{},"store":({},{}),"rows":[]};aA,S,aB=aK(b,q);aC,bf={"range":(I,K)},("watch","listen","range","ping","lost")
		def aD():bc(ab,";",c,aC)
		def aE():bd(ab,";",c,bf,aC)
		def z():
			p=b["path"]
			if p is None:p=b["path"]=a9(aY)
			return p
		def g(now,key,step):
			t=b[key]
			if now>=t or t-now>step:b[key]=now+step;return True
			return False
		def aF(text):return str(text or "").replace("|","/").replace("\n"," ").replace("\r"," ").strip()
		def aG(ev,short=False):
			c,d=ev["lx"],ev["ly"]
			if not(c or d):return "at "+Q("xy","%d,%d"%(ev["x"],ev["y"]))
			a,b=ev["x"]-c,ev["y"]-d;e=max(abs(a),abs(b))
			if e==0:return "at the lookout"
			if short:return "%d %s"%(e,Kit.compass(a,b))
			return bl(a,b)+" of the lookout"
		def h(serial,name,noto,x,y,facet,count,lx,ly,pinged=False):s="%.2f|%d|%s|%s|%d|%d|%d|%d|%d|%d|%d|%d\n"%(time.time(),serial,aF(name),aF(noto),x,y,facet,count,lx,ly,b["me"],1 if pinged else 0);return s.encode("utf-8")
		def p(data):
			a=b["outbox"];a.append(data)
			if len(a)>ao:del a[:-ao]
		def X(raw):
			try:
				s=raw.decode("utf-8","replace").strip()
				if not s:return
				p=s.split("|")
				if len(p)<8:return
				a={"t":float(p[0]),"key":p[0],"serial":int(p[1]),"name":p[2],"noto":p[3],"x":int(p[4]),"y":int(p[5]),"facet":int(p[6]),"count":int(p[7]),"lx":int(p[8])if len(p)>8 else 0,"ly":int(p[9])if len(p)>9 else 0,"from":int(p[10])if len(p)>10 else 0,"pinged":len(p)>11 and p[11]=="1"}
				if not 0.<a["t"]<1e11:return
				return a
			except Exception:return
		def aH():
			a=b["outbox"];n=len(a);d=z()
			try:
				with open(d,"ab")as f:f.write(b"".join(a[:n]))
			except Exception:b["write_next"]=time.time()+L;return
			del a[:n]
			try:e=os.path.getsize(d)
			except Exception:return
			if e>(ai if c["watch"]else 4*ai):bg(d)
		def bg(path):
			with Kit.quiet:
				with open(path,"rb")as h:a=h.read()
				f=a.rfind(b"\n")+1;a=a[:f];g=[k for k in a.split(b"\n")if k.strip()];b=g[-ak:];c=set()
				for d in reversed(g[:-ak]):
					if b"|listen|"in d and len(c)<ap:
						e=X(d)
						if e is not None and e["from"]not in c:c.add(e["from"]);b.insert(0,d)
				def i():
					with open(path,"rb")as a:a.seek(f);return a.read()
				bm(path,b"\n".join(b)+(b"\n"if b else b""),tail=i)
		def bh(path):
			try:c=os.path.getsize(path)
			except Exception:b["file"]="none";return
			a=b["offset"]
			if c<a:a=0
			if c-a>f:a=c-f;h=True
			else:h=a>0 and a!=b["offset"]
			if c==a:b["offset"]=a;b["file"]="ok";return
			try:
				with open(path,"rb")as i:i.seek(a);d=i.read(min(c-a,f))
			except Exception:b["file"]="busy";return
			b["file"]="ok";g=d.rfind(b"\n")
			if g<0:b["offset"]=a+len(d)if len(d)>=f else a;return
			b["offset"]=a+g+1;e=d[:g].split(b"\n")
			if h and e:e=e[1:]
			return e
		def bi(now):
			e=bh(z())
			if not e:return
			g=b["me"];c=b["seen"];d=b["inbox"]
			for h in e:
				a=X(h)
				if a is None or a["from"]==g or a["noto"]=="listen":continue
				k=(a["key"],a["serial"],a["from"])
				if k in c:continue
				f=now-a["t"]
				if f<-5. or(a["serial"]and f>ag):continue
				c[k]=a["t"];d.append(a)
			if len(c)>M:
				i=now-4*ag
				for k in[m for m,n in c.items()if n<i]:del c[k]
				if len(c)>M:j=sorted(c.items(),key=lambda a:a[1])[-(M//2):];c.clear();c.update(j)
			if len(d)>100:del d[:-100]
		def bj(now):
			c=z()
			try:
				d=os.path.getsize(c)
				with open(c,"rb")as e:
					if d>f:e.seek(d-f)
					i=e.read(f)
			except Exception:return
			g={}
			for h in i.split(b"\n"):
				if b"|listen|"not in h:continue
				a=X(h)
				if a is not None and a["noto"]=="listen"and a["from"]and-5.<=now-a["t"]<=a5:g[a["from"]]=a["t"]
			b["listeners"]=g
		def bk(m,serial):
			if m.IsRenamable:return
			a=V(m)
			if a in("invulnerable","ally"):return
			if not(m.IsHuman or m.IsGargoyle):return
			if API.IsFriend(serial):return
			if bn.search(str(m.Name or "")):return
			return a
		def bo(now):
			j=Y()
			if j is None:return
			t=int(j.Serial);k,l=int(j.X),int(j.Y);f=int(API.GetMap());b["me"],b["facet"]=t,f;A=am(c["range"]);u=set(int(bJ)for bJ in(API.GetPartyMemberSerials()or()));v=HOST.services.get("ultima.classify");B=b["listeners"];o=[]
			for m in A:
				try:
					if m is None:continue
					a=int(m.Serial)
					if a==t or a in u or a in B:continue
					if v is not None:
						r=v(m,u)
						if r is None or r[0]=="friend"or r[3]:continue
						d=r[2]
					else:
						if m.IsDead:continue
						d=bk(m,a)
						if d is None:continue
					if API.OnIgnoreList(a):continue
					o.append((a,m,d))
				except Exception:continue
			e=b["present"];s=[]
			for a,m,d in o:
				w=e.get(a)
				if w is None or now-w>ad:s.append((a,m,d))
				e[a]=now
			if len(e)>len(o):
				for C in[bK for bK,bL in e.items()if not 0<=now-bL<=ad]:del e[C]
				if len(e)>a6:e.clear()
			n=len(o)
			if n!=b["in_range"]:b["in_range"]=n;b["dirty"]=True
			D=c["ping"]and HOST.services.get("pings.send")is not None;i=[]
			for a,m,d in s:
				try:q,x,y=str(m.Name or "")or "(unknown)",int(m.X),int(m.Y)
				except Exception:continue
				z=D and len(b["pings"])<8;p(h(a,q,d,x,y,f,n,k,l,z))
				if z:b["pings"].append([x,y,f,"Lookout: "+q,now+aq])
				E={"t":now,"serial":a,"name":q,"noto":d,"x":x,"y":y,"facet":f,"count":n,"lx":k,"ly":l,"src":"here"};aI(E);i.append("%s (%s)"%(q,aj.get(d,d)))
			if i:aB("spotted %s, %s in range."%(", ".join(i[:4])+(" and %d more"%(len(i)-4)if len(i)>4 else ""),R(n,"player")))
			if s or g(now,"hb_next",ae):b["hb_next"]=now+ae;p(h(0,"","watch",k,l,f,n,k,l))
		def bp(now):
			a=b["pings"]
			if not a or(now<b["ping_next"]and b["ping_next"]-now<=ar):return
			d=HOST.services.get("pings.send")
			if d is None or not c["ping"]:del a[:];return
			x,y,m,f,g=a[0]
			if not 0<=g-now<=aq:a.pop(0);return
			try:e=d(x,y,m,"danger",f)
			except Exception:e=True
			if e:a.pop(0)
			else:b["ping_next"]=now+ar
		def bq():
			b["present"].clear();b["in_range"]=0;del b["pings"][:]
			if b["me"]:p(h(0,"","off",0,0,b["facet"],0,0,0))
			b["dirty"]=True
		def aI(ev):a=b["recent"];a.insert(0,ev);del a[a1:];b["dirty"]=True
		def br(ev,now):
			a=b["watchers"];w=a.get(ev["from"])
			if w is None:
				if len(a)>=ap:del a[min(a,key=lambda k:a[k]["t"])]
				w=a[ev["from"]]={"t":0.,"told":False}
			if ev["t"]<w["t"]:return
			w.update({"t":ev["t"],"state":ev["noto"],"x":ev["x"],"y":ev["y"],"facet":ev["facet"],"count":ev["count"]});w["told"]=ev["noto"]!="watch"or not-5.<=now-ev["t"]<=t;b["dirty"]=True
		def aM(ev,name,here):
			a=ev["noto"];b="%s (%s)%s, %s"%(name,aj.get(a,a),(", %d players"%ev["count"])if ev["count"]>1 else "",aG(ev))
			if ev["facet"]!=here and here>=0:b+=" in "+aN(ev["facet"])
			return b
		def aO(a):return aM(a[0],F(a[0]["name"],a[0]["serial"]),a[2])
		def bs(ev):
			d=aM(ev,ev["name"],b["facet"]);a=None
			if c["ping"]and not ev["pinged"]and ev["facet"]==b["facet"]and HOST.services.get("pings.send")is not None:a=(ev["x"],ev["y"])
			ay(at,d,level="alarm",ping=a,who=ev["serial"],name=ev["name"]);b["own_alarm"]=(ev,time.time(),b["facet"]);ev["src"]="lookout";aI(ev)
		def bt(now):
			d=b["inbox"]
			if d:
				f,b["inbox"]=d,[]
				for a in f:
					if a["serial"]:bs(a)
					else:br(a,now)
			if not c["lost"]:return
			for g,w in b["watchers"].items():
				if w["told"]or w.get("state")!="watch":continue
				e=now-w["t"]
				if e>t:w["told"]=True;b["dirty"]=True;ay(au,"Lookout quiet for %d s"%int(e),level="warn",who=g)
		def bu(i):
			def a():
				b=d["rows"]
				if i>=len(b):return
				r=b[i];a=r["ev"]
				if r["prev"]is not None and time.time()-r["at"]<=.15:a=r["prev"]
				if a is None:return
				if al():S(("follow",a["serial"]))();return
				S(("arrow",a["x"],a["y"],a["facet"]))()
			return a
		def aP():return u+30+J
		aa=58
		def E(n=H):return aP()+aa+J+30+n*s+6+u
		def aQ():
			z=e.zone_slot(W,E(1));w,i=z if z else(W,E());n=e.rows(s,E(0),H)if z else H;g,m,d=e.begin(w,i);M=u;j=[]
			if not b["minimized"]:
				a=w-2*M;e.frame(g);d["info_w"]=a-196;c=aP();O(g,M,c,a,aa);k=w-M-12-35-T("Clear");P(g,m,"clear",Z,k,c+28,"Clear","Clear the list, alarm line and tracking arrow",on_click=S("clear"));d["watch"]=B(g,"",M+12,c+9,o);d["listen"]=B(g,"",M+12,c+32,o);d["tw"]=(a-24,k-8-(M+12));f=c+aa+J;O(g,M,f,a,i-f-M,"SPOTTED  (newest first)")
				for l in range(n):h=f+28+l*s;r={"name":B(g,"",M+12,h+2,N),"info":B(g,"",M+12+180,h+2,o),"ev":None,"prev":None,"at":0.,"tip":None,"shown":True};r["hit"]=ah(g,M+6,h,a-12,s,bu(l),"");j.append(r)
			e.end(g,{"rows":j});b["dirty"]=True;aU(time.time())
		e=Kit.Window(aV,q,b,d,aQ,aW,aX,(220,220),(ac,aZ),a_,aA,lock=True,clear={"rows":[]})
		def aR():
			if not c["watch"]:return "off",o
			n=b["in_range"]
			if n:return "%d tiles, %s in range"%(c["range"],R(n,"player")),l
			return "%d tiles, all clear"%c["range"],A
		def aS(now):
			if not c["listen"]:return "off",o
			a=None
			for w in b["watchers"].values():
				if a is None or w["t"]>a["t"]:a=w
			if a is None:
				if b["file"]=="busy":return "the feed is busy, trying again",o
				return "no lookout heard yet",o
			d=aJ(now-a["t"],a0)
			if a.get("state")=="off":return "the lookout stopped %s ago"%d,o
			if not-5.<=now-a["t"]<=t:return "the lookout has been quiet for %s"%d,l
			n=a.get("count",0);e=Q("xy","%d,%d"%(a.get("x",0),a.get("y",0)))
			if n:return "the lookout at %s sees %s"%(e,R(n,"player")),l
			return "the lookout at %s, all clear"%e,A
		def bv(now):
			a=b["own_alarm"]
			if a is not None and 0<=now-a[1]<=av:d,e=aO(a),l
			elif c["listen"]:d,e=aS(now)
			else:d,e=aR()
			return "%s: %s"%(q,d),e
		def bw(r,ev,now):
			if ev is not r["ev"]:r["prev"],r["ev"],r["at"]=r["ev"],ev,now
			if ev is None:
				if r["shown"]:j(r["name"],"");j(r["info"],"");D(r["hit"],"IsVisible",False);r["shown"]=False
				return
			if not r["shown"]:D(r["hit"],"IsVisible",True);r["shown"]=True
			a=ev["noto"];j(r["name"],C("%s (%s)"%(af(ev["name"],ev["serial"],a),aj.get(a,a)),172),aL(a,aT.get(a,N)));c="lookout"if ev.get("src")=="lookout"else "here";f=Q("place",aG(ev,True)if c=="lookout"else "%d,%d"%(ev["x"],ev["y"]));j(r["info"],C("%s, %s ago (%s)"%(f,aJ(now-ev["t"],a0),c),d["c"]["info_w"]));e="%s (%s), seen %s at %s%s. %s"%(F(ev["name"],ev["serial"]),aj.get(a,a),"by the lookout"if c=="lookout"else "here",Q("xy","%d,%d"%(ev["x"],ev["y"])),""if ev["facet"]==b["facet"]else " in "+aN(ev["facet"]),be)
			if e!=r["tip"]:r["tip"]=e;U(r["hit"],e)
		def aU(now):
			m=d["g"]
			if m is None or(b["minimized"]and b["docked"]):return
			e=d["c"]
			if b["minimized"]:a,c=bv(now);j(e["status"],C(a,ac-90),c);return
			i=e["tw"];a,c=aR();j(e["watch"],C("Watch: "+a,i[0]),c);a,c=aS(now);f=b["own_alarm"]
			if f is not None and 0<=now-f[1]<=av:a,c=aO(f),l
			else:a="Listen: "+a
			j(e["listen"],C(a,i[1]),c);g=b["recent"];h=d["rows"]
			for k,r in enumerate(h):bw(r,g[k]if k<len(g)else None,now)
			if not g and h:j(h[0]["name"],"No one spotted yet.",o)
		def bx(x,y,m):
			a=b["facet"];c=b["arrow"];API.TrackingArrow(-1,-1,v);b["arrow"]=None
			if c==(x,y,m):return
			if a>=0 and m!=a:aB("that spot is in %s."%aN(m));return
			API.TrackingArrow(x,y,v);b["arrow"]=(x,y,m)
		def by(action):b["recent"]=[];b["own_alarm"]=None;bb(b,v);b["dirty"]=True
		bz={"clear":by,"follow":lambda action:ax(action[1],q),"arrow":lambda action:bx(action[1],action[2],action[3])}
		def bA(w):return(("WATCH AND LISTEN  (two clients, one TazUO folder)",(("check","watch","Watch: this client is the lookout","Park it hidden and still; it reports every player in range to the other client (not party, friends or guild)"),("check","listen","Listen: this client gets the alarms","Alarm for each player a lookout reports (sound: Settings > Alerts)"),("slider","range","Watch range:","Watch range in tiles (%d-%d)"%(I,K),I,K,{"ldy":6,"sdy":4,"lw":98,"sw":160,"ugap":10,"vfmt":"%d tiles","h":32}),("check","ping","Danger ping on the map where a player is spotted","Needs World Map > Map Pings; guildmates see it too"),("check","lost","Warn when the lookout is quiet for %d s"%int(t),"Its client closed, crashed or lost the connection")),{"top":32,"pad":4}),)
		def bB(a,new):
			for k in("watch","listen","ping","lost"):
				if new[k]!=a[k]:bC(k,new[k])
			b["dirty"]=True
		def bC(k,on):
			if k=="watch":
				if on:b["next_scan"]=b["hb_next"]=b["listeners_next"]=0.
				else:bq()
			elif k=="listen":
				if on:b["listen_next"]=b["announce_next"]=0.
				else:b["inbox"]=[]
			elif k=="ping"and not on:del b["pings"][:]
			b["refresh_at"]=time.time()
		G=Kit.Page(c,bA,aE,bB);aD()
		def bD():b.update(aw(),minimized=e.start_min());aD();p=API.Player;b["me"]=int(p.Serial)if p is not None else 0;b["facet"]=int(API.GetMap());z();az(at,"Lookout spotted a player",a7);az(au,"Lookout went quiet",ba);aQ();e.dock(fit=True,min=(W,E(1)))
		def bE():
			if d["g"]is None:return
			if a8(d):return
			while b["queue"]:
				f=b["queue"].pop(0)
				if e.action(f):continue
				h=bz.get(f[0]if isinstance(f,tuple)else f)
				if h is not None:h(f)
			a=time.time()
			if c["watch"]:
				if g(a,"next_scan",a2):bo(a)
				bp(a)
			elif c["listen"]and g(a,"next_scan",1.):
				p=API.Player
				if p is not None:b["me"]=int(p.Serial);b["facet"]=int(API.GetMap())
			if c["listen"]:bt(a)
			if b["dirty"]or g(a,"refresh_at",1.):b["dirty"]=False;aU(a)
		def bF():
			if b["shutting"]:return
			a=time.time()
			if c["listen"]and b["me"]and g(a,"announce_next",a4):p(h(0,"","listen",0,0,b["facet"],0,0,0))
			if b["outbox"]and(a>=b["write_next"]or b["write_next"]-a>L):aH()
			if c["watch"]and g(a,"listeners_next",an):bj(a)
			if c["listen"]and b["me"]and g(a,"listen_next",a3):bi(a)
		def bG():
			if b["shutting"]:return False
			a=time.time()
			if c["listen"]and b["me"]:return True
			if b["outbox"]and not 0<b["write_next"]-a<=L:return True
			return bool(c["watch"])and not 0<b["listeners_next"]-a<=an
		def bH():
			b["shutting"]=True
			if c["watch"]and b["me"]:p(h(0,"","off",0,0,b["facet"],0,0,0));aH()
			bb(b,v);aE();aA.close()
		return{"start":bD,"tick":bE,"stop":bH,"client_tick":True,"config_height":G.height,"build_config":G.build,"poll_config":G.poll,"config_closed":G.closed,"thread_tick":bF,"thread_wanted":bG}
	def bH():
		Z="ultima.overview";g="Overview";t="UltimaTracker_overview";aa="UltimaTracker_overview_pos";ab="UltimaTracker_overview_min";W=390;ad=(260,46);ae=5365;af=24;n=66;v=60;x=.5;y=1.;ag=1.;ai=8198;q=50;aj="#3AB04A";ak="#202020";an="Alt+click: auto-follow (again to stop)";f=(("players","Players","player"),("monsters","Monsters","monster"),("pets","Pets","pet"),("corpses","Corpses","corpse"));ao=("distance","HP","name");aq=("distance","name");z={"tab":(0,3),"players":(0,2),"monsters":(0,2),"pets":(0,2),"corpses":(0,1),"range":(4,24),"rows":(3,20)};b={"tab":0,"players":0,"monsters":0,"pets":0,"corpses":0,"range":18,"rows":8};ar=dict(b);a={"minimized":False,"shutting":False,"docked":False,"queue":[],"lists":{},"data_at":0.,"corpse_at":0.,"corpses":[]};c={"g":None,"c":{},"store":({},{}),"rows":[]};A,h,aN=aK(a,g)
		def at():bc(t,"|",b,z)
		def k():bd(t,"|",b,sorted(ar),z)
		def E(tab):return aq if tab==3 else ao
		def l(tab):o=E(tab);return o[min(b[f[tab][0]],len(o)-1)]
		def F():return Kit.pitch(af)
		def H():return u+30+J+n+J+16+u
		def I():return W,H()+F()
		def au(i):
			def a(*b):
				a=c["rows"]
				if i>=len(a)or not al():return
				r=a[i];v=r["prev"]if r["prev"]and time.time()-r["changed"]<Kit.TWICE else r["val"]
				if v and v[1]:h(("follow",v[0]))()
			return a
		def s():
			c,s=F(),H();z=d.zone_slot(*I());t=d.rows(c,s,b["rows"])if z else b["rows"];w,v=z if z else(W,s+t*c);g,x,i=d.begin(w,v);A=[]
			if not a["minimized"]:
				d.frame(g);M=u;e=w-2*M;y=M+30+J;C=b["tab"];O(g,M,y,e,n);Kit.buttons(g,x,M+8,y+6,[("tab%d"%bh,L,bw[1],"Show %s in range"%bw[1].lower(),h(("tab",bh)),ap if bh==C else None)for bh,bw in enumerate(f)],6);i["sort"]=P(g,x,"sort",L,M+8,y+36,"Sort: "+l(C),"Order of this list (again for the next)",on_click=h("sort"));i["count"]=B(g,"",M+e-12-T("60 in range"),y+40,o);j=y+n+J;O(g,M,j,e,v-j-M);D=M+e-10-T("24 tiles");k=D-8-q;E=k-6-T("100%");i["nw"]=E-6-(M+10)
				for Q in range(t):m=j+8+Q*c;p=m+max(2,(c-16)//2);R=m+c//2-3;r={"name":B(g,"",M+10,p,N),"hp":B(g,"",E,p,o),"back":S(G.CreateGumpColorBox(.8,ak)),"fill":S(G.CreateGumpColorBox(.95,aj)),"dist":B(g,"",D,p,o),"val":None,"prev":None,"changed":0.,"fw":-1,"bar":True,"on":True};r["back"].SetRect(k,R,q,6);r["fill"].SetRect(k,R,0,6);g.Add(r["back"]);g.Add(r["fill"]);r["hit"]=ah(g,M+6,m,e-12,c,au(Q),an);A.append(r)
			d.end(g,{"rows":A});K()
		d=Kit.Window(Z,g,a,c,s,aa,ab,(W,300),ad,ae,A,clear={"rows":[]})
		def K():
			d=c["c"];e=b["tab"]
			if "status"in d:j(d["status"],"%s: %s"%(g,f[e][1]));return
			if "count"not in d:return
			h=a["lists"].get(f[e][0],());k=f[e][2];l="%s in range"%R(len(h),k);j(d["count"],l);m=c["rows"];n=time.time();o=d["nw"]
			for i,r in enumerate(m):p=""if i or h else "No %ss in range."%k;av(r,h[i]if i<len(h)else None,e,o,n,p)
		def U(r,pct):
			a=pct>=0
			if a!=r["bar"]:r["bar"]=a;D(r["back"],"IsVisible",a);D(r["fill"],"IsVisible",a)
			b=int(round(q*min(100,pct)/100.))if a else 0
			if b!=r["fw"]:r["fw"]=b;r["fill"].SetWidth(b)
		def av(r,e,tab,nw,now,blank):
			Kit.row_set(r,(e[0],tab!=3)if e else None,now);c=e is not None and tab!=3
			if c!=r["on"]:r["on"]=c;D(r["hit"],"IsVisible",c)
			if e is None:j(r["name"],blank,o);j(r["hp"],"");j(r["dist"],"");U(r,-1);return
			i,a,d,k,b,l,m,n,f=e
			if tab==0:a=Q("name",a,i)
			elif tab==3 and Kit.streamer:a="Corpse"
			g=aP(d)if tab<3 else "";h=aO(l,m,n)if tab<3 else "";p=(g+" "if g else "")+a+("  "+h if h else "");q=aL(d,aT.get(d,N))if tab<3 else N;j(r["name"],C(p,nw),q);j(r["hp"],""if tab==3 else("dead"if f else("--"if b is None else "%d%%"%b)));j(r["dist"],R(k,"tile"));U(r,-1 if tab==3 or b is None or f else b)
		def ay(e):return e[3],e[1].lower()
		def az(e):return(101 if e[4]is None else e[4]),e[1].lower()
		def aA(e):return e[1].lower(),e[3]
		X={"distance":ay,"HP":az,"name":aA}
		def aB(now):
			k=Y()
			if k is None or b["tab"]==3:a["lists"]={"corpses":a["corpses"]};return
			if not 0.<=now-ac["scan_at"]<=y:ac["party"]=set(API.GetPartyMemberSerials()or())
			bs(now);n=b["range"];u=k.Serial;d=None;e={"players":[],"monsters":[],"pets":[]};o=HOST.services.get("pets.list")
			if o is not None:
				try:
					q=o(distance=n)
					if q is not None:d=set(int(G)for G in q)
				except Exception:d=None
			for m in am(n):
				try:
					g=m.Serial
					if g==u:continue
					w,r=aw(m,"Hits"),aw(m,"HitsMax");i=p(m,"IsDead")
					if p(m,"IsRenamable")if d is None else int(g)in d:j,h,c="pets",V(m),str(m.Name or "")
					else:
						s=aW(m,g)
						if s is not None:
							h,i,c=s;j="players"
							if c and c.lower()in M:continue
						else:
							h=V(m)
							if h=="invulnerable":continue
							j,c="monsters",str(m.Name or "")
					e[j].append((g,c or "(unknown)",h,int(m.Distance),int(round(100.*w/r))if r>0 else None,p(m,"IsPoisoned"),p(m,"IsParalyzed"),p(m,"IsYellowHits")and not i,i))
				except Exception:continue
			for x,z in enumerate(f[:3]):t=e[z[0]];t.sort(key=X[l(x)]);del t[v:]
			e["corpses"]=a["corpses"];a["lists"]=e
		def aC(now):
			a["corpse_at"]=now;c=[]
			try:e=API.GetItemsOnGround(b["range"],ai)or()
			except Exception:e=()
			for d in e:
				try:c.append((int(d.Serial),str(d.Name or "")or "a corpse",None,int(d.Distance),None,False,False,False,False))
				except Exception:continue
			c.sort(key=X[l(3)]);del c[v:];a["corpses"]=c
		def aD(action):
			if action[1]==b["tab"]:return
			b["tab"]=action[1];k();a["data_at"]=a["corpse_at"]=0.;s()
		def aE(action):
			d=b["tab"];e=f[d][0];o=E(d);b[e]=(min(b[e],len(o)-1)+1)%len(o);k();a["data_at"]=0.
			if d==3:a["corpse_at"]=0.
			if "sort"in c["c"]:j(c["c"]["sort"],"Sort: "+l(d))
		aF={"tab":aD,"sort":aE,"follow":lambda action:ax(action[1],g)}
		def aG(w):return(("LIST",(("slider","range","Range:","Overview range in tiles (4-24)",4,24,{"unit":"tiles"}),("num","rows","Rows:","Rows shown outside a zone (3-20)",None,3,20))),)
		def aH(b,new):
			a["data_at"]=a["corpse_at"]=0.
			if new["rows"]!=b["rows"]and c["g"]is not None:h.add("redraw")
		m=Kit.Page(b,aG,k,aH)
		def aI():a.update({"shutting":False,"docked":False,"queue":[],"lists":{},"data_at":0.,"corpse_at":0.,"corpses":[],"minimized":d.start_min()});at();s();d.dock(fit=True,min=I)
		def aJ():
			q=a["queue"]
			while q:
				f=q.pop(0)
				if not d.action(f):aF[f[0]if isinstance(f,tuple)else f](f)
			if c["g"]is None or a8(c)or a["minimized"]or a["docked"]:return
			e=time.time()
			if b["tab"]==3 and not 0.<=e-a["corpse_at"]<ag:aC(e)
			g=e-a["data_at"]
			if 0.<=g<x or(0.<=g<y and HOST._mob_pid!=HOST.pass_id and 0.<=e-HOST._mob_at<x):return
			a["data_at"]=e;aB(e);K()
		def aM():a["shutting"]=True;k();A.close()
		return{"start":aI,"tick":aJ,"stop":aM,"client_tick":True,"config_height":m.height,"build_config":m.build,"poll_config":m.poll,"config_closed":m.closed}
	bI=(("tracker",bF,.05,"ultima"),("lookout",bG,.1,"lookout"),("overview",bH,.1));return PartSet(bx,bz,bI).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("ultima","Ultima Tracker","Friends, foes and neutrals near you",_module_ultima,.05,category="The world",parts=(("tracker","Tracker","Trackers and combat bars",True,("ultima",)),("lookout","Lookout","A second client keeps watch",False,("lookout",)),("overview","Overview","Players, monsters, pets and corpses in tabs",False,(),True),),aliases=('Combat Bars','Lookout','foe','sightings','trackers','second client'))
