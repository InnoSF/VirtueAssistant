def _module_ultima():
	ae=Client.key_held;L=Follow.alt_held;I=Follow.current;S=Follow.toggle;T=HOST.alert;U=HOST.alert_kind;af=HOST.dock_add;A=HOST.dock_forget;ag=HOST.dock_remove;ah=HOST.dock_to_bar;V=HOST.harm_ok;p=HOST.layout_holds;B=HOST.me;X=HOST.mobile;M=HOST.mobiles;Y=HOST.refresh_settings;Z=HOST.show_settings;N=HOST.stopping;O=Journal.reader;ar="ultima";at="Ultima Tracker";ai=re.compile(r"\bthe\s+[a-z]",re.IGNORECASE);J={"murderer":"red","criminal":"grey","gray":"grey","enemy":"orange","innocent":"blue","ally":"green","invulnerable":"yellow"};aa={"murderer":34,"criminal":946,"gray":946,"enemy":144,"innocent":89,"ally":63,"invulnerable":53};aj=3.;ab=2000;f={};z={};u={};C={};P=set();Q=set();ac={};D={"party":set(),"scan_at":0.};ak=("lord ","lady ")
	def l(name):
		n=(name or "").strip().lower()
		for p in ak:
			if n.startswith(p):n=n[len(p):]
		return n
	def E(cache):
		if len(cache)>ab:cache.clear()
	F={};al=1.;am=[0.]
	def K(serial):
		v=F.get(serial)
		if v is None:
			v=bool(API.IsFriend(serial))
			if len(F)>500:F.clear()
			F[serial]=v
		return v
	def an(now):
		if not 0.<am[0]-now<=al:F.clear();am[0]=now+al
	def j(m,a):
		try:return bool(getattr(m,a))
		except Exception:return False
	def au(mob,serial,name,low):
		if low.startswith(ak)or l(name)in f or low in u or serial in D["party"]:return True
		if j(mob,"IsRunning")or j(mob,"IsMounted")or j(mob,"InWarMode"):return True
		return K(serial)
	def av(mob,serial,name):
		if serial in P:return False
		b=name.strip().lower()
		if au(mob,serial,name,b):E(P);P.add(serial);C.pop(serial,None);return False
		if b in ay()or b in Q:return True
		c=time.time();a=C.get(serial)
		if a is not None and(a[0]or c-a[1]<aj):return a[0]
		e=ao(mob);d=bool(ai.search(e.split("\n")[0]+" "+name));E(C);C[serial]=(d,c);return d
	def ao(mob):
		try:return str(mob.NameAndProps(False)or "")
		except Exception:return ""
	def aw(mob,serial,name):
		if serial in P:return False
		b=name.strip().lower()
		if not b:return False
		a=b in Q
		if not a:
			d=time.time();c=ac.get(serial)
			if c is not None and(c[0]or d-c[1]<aj):a=c[0]
			else:e=ao(mob).split("\n")[0].strip().lower();a=e.startswith(b+" the ");E(ac);ac[serial]=(a,d)
		if not a:return False
		if b in u or l(name)in f or serial in D["party"]or K(serial):return False
		return True
	def ad(mob,serial):
		a=j(mob,"IsDead")
		if not a and not(j(mob,"IsHuman")or j(mob,"IsGargoyle")):return
		if j(mob,"IsRenamable"):return
		b=Kit.noto_name(mob)
		if b=="invulnerable":return
		try:c=str(mob.Name or "")
		except Exception:return
		if b=="innocent":
			if av(mob,serial,c):return
		elif not a and aw(mob,serial,c):return
		return(b,a,c)
	def R(m,a):
		try:return getattr(m,a)or 0
		except Exception:return 0
	ax=("0aaron2sin1ba2bott3y2del3iel2el4la3y2igail3jah3na3ona3ra2ner2ra4h5am4n2sinthe1cacia3nit4tha2calia2e3lin2hen3illes2kerley1da3ir3lia3m3ra2di4son2eben3laide4e4ia5ne4le3m3na3res3sina2ie3mina3ran3va2lai3er4y2mon2olph3n4cia4ia5s3ra2rian4el5nne1elina2neas1fina2ra3ika2ton1gate4ha2nes2ustin1hara3ve2earn2imsa2mik2ren1ida4n2ella2ken3o2la3een3sa2mee4ry2n3a3hoa3sley3tzane2rlia2sling6n2tan3hne2yana1jara3y4i2inora1kako3la3ndo4ke3sma2baar2ela4lo2il4ah4i5na3na2shay1laina3ke3la3manada3n4a4d4i4na4o3qua3ric3stair3vda3zne2ben4rt6a3inka2cander3ina3ott2dea4n4r5cy3rick2ec3k4a4sy3nne3ron3ser4ia4sa3thea3x4a5nder7ra8ia9na4is2fred2ger2i3a3ce4ia3da3ke3m4a3na3son4tair3ta3x3z4a2laard4n4rd3ele4n3igra4nora4son3yn2ma2odie3nzo3ysia2phonse7o2ston2tair3hea3on2ula3mit2vin5a4ta2ysa4sa6nd2zena1ma3bel3deo4i5ka5s4o3ia3la4ia3nda5ine3ra5nde6te4is3ta2bar3er3ika4s3rose2eerah3lia5na3thyst2ie4l5la3na4ta3ssa3ta4y2mon2oke3s2sden2y1nanda3stasia2celin2ders3i3ra5ianna5s4e5a5us5w5y4ies4omeda2eida3lla3mone3zka2gela5ica6ne6que5o4ni3us2i3ca3eli3sa3ta2ke4r2n3a4bel7le4marie3e4tte3ikka3ora2oki3rah3ush2sel5me3ley3on3reana2teia3hea4ony3je3oinette4nia6o2war1olani1para2irka2olline5oina3ni2ril5le1qua3ene1ra3bella7e3celi3minta3xie2cadia3her4ibald2dath3elia4n3is4th3on2eiela3lla3n3s3tha4ina2gus2i3adne4na3cia5n3el4ne3on3sta5o6tle2kin2len5e4y3in5da3o2man3en3ina5da3on3strong2ne3old4n2on2piar2sen5io2temisia3hur2una2ziki1saria2enka2h3a3by3er3ford3lan4eigh5y4in3on3ur2ia3sa2linda2pasia2ta3er5a3ra4ea4id1talanta3ra2enne3ri2halia4n3ena4ron3la2ifa2man2ta1ubrey2da3ny3rey4ianna5c3un2gustin8a6us2ra3e4k4lia3ilia4na3kene3ora2stin2tumn1va3na3sa2ella3na3rill4y2ie3s3va1xel4la1ya3luna3me3na3sha2dee2ela2iana3la3sha3ta2la2nora2una1zaleah4ia3rael2era2ha2ilea3na3ze2ora2ura0babette2cia2e2iley3ngana2ka4ri5ne2layna3bo3der4win3e4a4ndin3i4a4n5t2mbi2nan3croft3dele3e4lla3ning2ra4n3bara3clay3den4o5n3ika3nabas6y4ett5y3on3rett4y3se3t4h5olomew4on2sha3ia4l4mah3tiaan2takah3hsheba3ya2ul2vol2xter2y3ana5i4rd3lor3o3ta2zyli1ea3can3gan3man3trice6x3u4ina4mont4regard2cca3k4y2delia2l3ana3don3en3ina5da4ta3lanca4e3ora2m3an2n3edict4n3jamin3nett3son3t4e4ley4on2radine3enger3gren3illa4t3k4eley3nadette5rd4ice3sh3t4hold4on4ram3yl2ss4ine2ta3h4ana6y3ony3ty2ulah2val4n3erly3in1ialy3n4ca2lal3lie2na3dy3ti2rdie3kita2shop2talo2xenta1jorn1lade3ine4r4se3ke3nche4da3z2enda2iss2orn2y3the1o2den2gart2hdan6a2lton2namy3d3ita3nie4y2oker3ne2rden3gny3is2tan2wie3man2yce3d4en1rad4en4ford4ney4y3ina3m3n4d5eis5i5on5y4t3xton3y3z4il2en4cis4da6n5on4na6n4t5an3t4t5a3wster2iac4n5d3ce3dget3e4g4r4tta3git6te3na4ley3ona5y3shen3tes4ta6ny2ock3derick4ny4y3nson4t4wyn3oke2uce3no3tus2yan5t3ce3nn3son1ucia3k2d3o2rgess3han3ian3ke3l3r3ton1yran3on0cadence4o3or2edmon2ilan3mile3n4e3tlin4rin2la4ndia6ra3der4well3eb4ndonia4y3ida4sta3la5n4ia5dora5e3tha3vin3ypso2m3den3elia4ron3ilia5le2nace3dace5n4ida6e4ra3tara4on3ute2oimhe2pri5ce2ra4doc3den3esse4y3i4na5e4ssa4ta3l4a4een5n4in6g4o5s5ta4ton4y3ma4el6ina5n3na4elian3ol5ina7e5yn4n3r4ick5e4ocio5ll3son3ter3ver3yn2sey3ilda3per3sandra4ia5dy5us3ta5lia4el2talina4va3erina3herine4leen4y3o4n3riona2van2yla1eara3sar2cania3il5ia2dric2landine3este3ia4na3lia2mal2relia1had4wick3im4tra3l4e4mers3nah4da5er5i5ler5ra4e5l5y4na5ing4tal3pin4man3ris6sa5ty4les5otte5ton4maine3se4tity3tha3uncy3va4iva3y4a4ton2elsea3n4ey4oa3rica6e5e4yl3sna4ter3t3valier2iara3ka4e3lali3mlis3n3po2loe4ris2o2rista7ble6ian7na8e6oph9er7s6y2uck2you1ia3nnait3r2cely4ron2ndy2ro1laire3ra4ence4inda5ssa4k3ude6tte5ia6ne3y4ton2ement7ina9e3veland2iantha3fford4ton3nt5on3ve2orinda3ver2yde1ochiti2dy2lby3e4ene4man4tte3in3lin3on3ton2man2ndon3nie4or3rad3stance7za4uela3way2ra4lie4zon3bett5y4in3coran3deali5ll3etta4y3i4nna4s3liss3nelius3rine3t4ney2ty2urtland1raig3ndall2eighton3scent4sida2ispin2osby2ystal1ullen4in3ver2rran3tis1ybele3il2nric3thia2prien2rano3ene3il5la3us2theria0dabria2cey3ia4e4o2e2g3an3mar3na2i3ly3sel4y2karai3ota2le3ila5ia3lin3ton3y2mara3ek4n3ian4en4on4tri3on2na3e4tt3ia4el6la4or3nik3te3yelle2phene4ne5ie2r3a4lis3by3en3ia4en4o3la4ene3nell3rel6l5n3yl2sha2vene3id4n5e4s4ta2wn2ya3na1eacon3n4a4dra2b3ra2cker2de2e3dee2ianira3ene3rdre2lana5ey5o3bert4in3ia4cia4lia3la5n3more3phina3sin2man3be3i4tria3psey5ter2na3by3ice3nis4ys3ton3ver2r3ek3rick4y2va4ki4l3erell3i4n3lin3net3on2wey1iamanta3ne4the2ederik4re3go3lla3ter2llian4on4y3ys2mitri2nah2onne2rk2sa2ta3i2xie1obry2die2lores2minic7k6que2na4ld4ta5ien5o3ielle3nelley7y5r3ovan2oriya2phina2ra3een3inda4s4thy3on3y2ugie4las7s2v2yle1rake2ew2ina2ucilla1uane2gan3las2lcie5nea2ncan3stan2rand3riken2san3tin4y2tch1wayne2ight1yami3n4i3stro2lan2mas3phna2na0eamon2rl4e3tha2ster2ton1bony1cho1dan4a2gan4r2ie3son3th2lyn2mund2na2olie2ria4n2ward3in5a1fia1gan1ileen2nar2rene1lad3ine3na2den3roth2ek3ora2i3anor4s3jah3na3sa4e4ka4sa3ta3za5beeth2kan3e2la3e4n4ry3iot6t4s3sworth3y2mer3o2odie3ise2sa3ie3ton2ton2wood2ynor3se4ia1ma3jane3lia3nuel2ber2elie4yne2il4io4y2ma3ett2o1ndora2gracia2id2och3la2rico4que2ye1phraim1rasma2ek2ianthe3c4a3k3n2lina2nest2ol2rol2skine2wand3in2yx1skarne2merelda2peranza2sien2ta3eban4lle3her3u1tain5a3nthe2han2ta1udocia2gene5ia2lalia2stacia1va3csa3dine4ne3n4der4geline4the2e3lyn3rett2ita2onne2zen1yota1zekial2ra0fabienne4o2ifuza3nche3rfax3th3zah2llon2ntine2rha3ima3ley3rah4ell2tin2wne2xon2y3e3ina3me1elcia3icite7y4x2mi2nn3ton2rgus3idwyn3n3onia3ran4is1ielding2lbert3inda3more2na3lay4ey3n4igan3ola2ona3renza2sk2tzgerald1lavia2eta4cher2indo4t2ora4ence3yd2ynn1orbes3rest3sythe2ster1rances7ca5ine6s7ca4ek4k5lin3sier3zer4ier2ed4a4erica8k3mont3ya2ida3eda3tz1uller3ton2scienne0gabe3riel7la8e2ge2ia3l2latea3en5o3i4na3vin3ya2mble2na3esa3non2reth3field3gan3ner3rett4ick5dan5son5tt3th3vin3y2spar3ton2uri2vin3rie2ye3le4ord3nor1elasia2mma2nevieve2off5rey6y3gia3rge6anne6tta8e5iana2radline4ldine4rd3da3ik3main3ri4y3trude2va1hislaine1iacinta3nina2deon2gi2lana3berto3da3en4s3lian2n3a3ger3ton2selle2tana3ha2von2zane1leda3n4n5a5o5ys1odfrey2lda4ie2rdon4y3man2tzone1race4ie3dy3ham3inne3m3nger4t4ville3yson3zia2ear3g4er4or6y3sham3ta4chen4te2iffen5ith1uilhem2nnar3ther2s3tave2thrie2y1wen4dolyn4eth2ynne1ytha0hackett2dara4ssa3den3i4ya3ley3rian2gan2idee3ley3mi2l3den4is3e4y3i4an4ma3le4ie3sey2milton3lin2na4n3k3nah4e3s2rden4y3ith3lan3man4oni3old3per3riet5son4y3t4ley3vey2sna3san3tin6gs2va2ya3den3es3lee3nes2zel1ea3th5er2ctor2i3di2laku3degarde3en5a5e3ki2nka3ning3rietta4y2rbert3man3schel2sper3ter1ilary3da3liard3ton2nda2roshi2sa1obart2gan2lden3ly3t2mes2pe2race3ton2shi2uston2ward3rence2yt1ugh3o2mphrey2nter4ley1yacinth2e2man2patia0iain1da2ola3nia1lene2ias2ona1man2ogene1ndia4ra3ra2es3z2ga3mar3ram4id1olana5the2na1ra3tze2ena4e2is2ma2vin5g2win1saac3beau5l6la3dora3iah3ura2is2leta2obel3ke2rael2tas1tzak1van4a3r2ory2y0jabari3ir2celyn3inda5the3k3ob5e3ques3son3y2da2el3n2far2gger2imie3one2ke3inda2l3a3eel2mal3es3ie4la6h4son2n3a3e4lle4t3ice4s3na4elle2rdena3ed4k3man3on3rod3via5nia5s2smine3on3per2van3ier2y3a3ne1ean4ette4ine2bidiah2d3idiah3rek2ff4rey2lani3ena2na4y3dayi4yose3ica3nettia4ifer3sine2remiah5y3olin4me5y3rilyn3zy2sse5e4ica2thro2wel2zebel1ibril2han2llian2n3a3ny3x2ro2vin1oakima3n4ne2bey3ihna2casa3elyn2di3y2el4le5iane2hann6a3n2ia2lan5ta3ene3ie4ne3on2nah4than6on3ina2ra3dan6e4on3gen3vin2seph6ine3hua3ie2tha2y3ce3e1uanita2dd3e3ith6a2lia5n6a6e4e5tta4nka4us2ma3oke2n3e3g2stin6e0kaatje2chine3lyn2din2ede3the2i3a3e3kara3li3mi3ros3ya2kra2la4din4ma4nit4re3b3e4a3i4ka4l5a4nda3kin3le4i3man3onice3yca2ma4l5a5i4ria3bo3eko3ilah5ia2nda3e4ne3iel4ka3tha3ya2pera2ra4n4yan3dal3el4n3ida4mah4sa3ka3l4a4enne4i4yn3mina3ol3sten3ylin4n2sa3ch3en3ia4nda3par3sia2te4b3herine4leen3ja3oka3rien5na2ula2veri3indra2y3a3e3in3la3sa2zia1eane3ra4ney2dar2efe3lan4in4y3nan2fira2gan2hinde2i3ko3r3sha3th2lby3da3eman3ia3l4en5y4i5e4y3sey3vin2n3an3dall4ra5ick3elm3ley3nard4edy5th4is3t4on3yangi4on2ona2pa2r3ani3by3ensa3n3ry3s4en4tan3win2sare3i4a3sie3ter2turah3zia2vin1halida5l2oury1ichi2efer3le3ran4nan2llian2m3berly3mie4y2n3eta3nel3sey3tan2ona2p2ra4n3by3ima3k3sten3ti2sa3ka3met3sa2ta2yoshi1liftin2og1ohana2lina2mor2ntar2ren4ssa1rischan4ten6r1urt1yle4r3y2na3thia2oko0lacey3ie2ethan2ila4ie3rd2keisha2la4sa2mar3ont2n3a3ce3der4on4ra3e3g3i2ra4ine4lee3i4ssa3k3ry3s2tika3onia2ura5na4el4ie5nda4yn2veda4rn6e3inia2wler3rence2zarus1ea3h3la3ndra3r2ba2dah2e2if3gh5ton3ko3la5na2land2n3a3e3non5r5x3or5a5e3sar2o3n4a5rd3ra2ron4y2slie3ter2tha3itia2v3ana3i2wis2xine1i2a3dan3m3n4a4e2bby2en2ke2la3ith3lian5e3y2mber2na3coln3da4say5ey3ette3nae4ea2onel2sa3ette2tsa2v2za1lewellyn2oyd1ogan2is2kelani2la2ni2ra3e4lei5le4n5zo4tta3i3ne3raine2tus2uis5e2well1ucas3ian4lle4ne3retia3y2dia2ela2is4a2ke4ne3ina3yan2lu2na3t2ther1ydia2le2nda4on3elle3n4da4ette2ris2sander3el3nadra0mabel2c3aria3er3hi3k4enzie2ddy3elaine5ina7e5on5yn3y2e2gan4ra3dalen8a6ine3ena5ta3gie3nus2hala5ia2i3a3da3sie3tane3zah2j2laya3colm3ik4la4na5da3ka3lory3u2mie2nco3da5ra4ek5r4isa4y3fred3gena3ning3on3si4ur3uel3ya2ra3c4ella4ia4os4us4y3den3ek4n3garet6ita4o5t4uirte3ia5h5m6a5n6a6na7e4bel4e5l5tta4ly6n4na4o4s5a5ha5sa3jani4eta4orie3k4ham4os3lene4in4o5n3mara3nie5na3sha6l7l4ten3ta4ha4i5n6a6go3vin3y4ann4beth4lou3zia2son2tai4na3eo3hea5r3ilda3rika3thew5ias2ud3ra4een4ice5ta2vis2x3ine3well2y3a3nard3on1ead3ra2da3ea2g3an4ra3han2i3ra2ka2la4nie5tha3ba3ia5n4na5da4senda5sa3linio3odie5y4sa3va2rcedes5r3edith4le3ill3le3rick5k2sha2ta2yer1ia3koda2cael3hael7a4ele6le2dori2gina3non3on3uel2ka3e3kel3os2les3licent5e3o3ton2n3a3da4el4y3er5va3ka3na4ie2ra4nda3em5ba4ya3iam4elle2ssy3ty2tchell3ena4xi3zi1oira2llie4y2na3ique3roe3te2on2rena3gan6a6ce3ia5h3ley3ris3timer4on3ven3z2tega1ukasa2rdoch6k3iel3phy1yles2ra3on0nada3ia4ne3ya2eem2ia3lah3mah2lini3ren2mazzi3i2n3a3cy3ette3tale5n2omi2pea2ra3da3mada2siche3tassia2talie4ne4sha3esa3han6iel2ysa2zirqah1eal4a4e2ci2diva2ely2il2kane2lek3l3son2ola3ma3na2ria4ne4ssa3on2stor2tti2va4da4n3ille4n2ysa1icanor3holas3ia3ola5e6tte2gel2ka3ki3olos2ls2mah2na2obe3la2ra3velli2ssa2ta4ra2xie1oah2din2e3l4ani4la2lan3ita2na2ra4h3bert3een3i4ko3ma5n3ris3ton1uri1ydia2le2rna2ssa0oakes3ley1belia1chen2tavia6us1delia4l3ra3ssa3tta5e2ile3n3on2on1gden1hanna1kelani1laf3the3yinka2esia2ga2iana3n4da3ver5tte4ia1mar1na2ida1pal2helia1ralie3ne2dano2en4da2iana5na3el3ole4n2lantha2man5d2nidaa2rin2son2ville1scar2good2mond1tis2to1wen0paco2ige2kuna2lmer4iera3oma2mela2ndita4ora3thea4zike3ya4in2olo2ris3ker3nell2scal6e2tamon3ia4ence3ricia6k3sy3terson4on2ul4a4ette4in6e2vel3la2xton2yton2zia1earce4l2der2g3gy2lagia2mba4roke2nda3elope3inna3n4y3thea2ony2rcival3dita3ouze3ry3sis2ter3ra2yton1haedra2earcy3dra2ilip4lip7pe4omena2oebe4nix2ylis4lis1ia2er4ce4re4son2la4n2per1laton1olly3oma2rche3ter4ia1rentice3scot7t4ton2iscilla2udence4y1yrena2thia0qamra1ueena3lla3nby4tin5on2illan3ncy4lan4n4tina3terie0rachel2d3cliffe3ella3inka3man2e2fael3ferty2gnar2i3don3zel2leigh3ph2miro3la3on5a3say4ey3ya2nard3ce3dall4ie4olph3e4e4n3ger3i3kin2oul2phael2quel2shida3ine2tri2ul2ven3i4d2wnie2y3mond3na4ell4or2ziya1eade2ba3ecca2dford3mond2ed3se3ve2gan3ina6ld4s2idun2mington3y2na4ldo4ta3dor3e4e3fry3ny2uben2x2yhan1hea3tt2iamon4nne6on2oda5nthe3nda4na2ys4sa1ia3ne2ca4rdo3hard4ter3o2der3gley2gby2hana2kki2ley2mon2ngo2o3dan3rdan2sa2ta2va1oanna3rke2bert6a6o3i4n3yn2chelle3kwell2d3erick3man3ney3rigo2ger2hanna2i2land3dan3f2na4ld4n2oney2rie3y2sa4lind8a8e7e4nne3coe3e4anne4marie7y3s2th2wan3ena3land2xana5ne2y3ce1uben3y2dd3i3yard2fus2mer2nako2skin3s4ell3ty2th4ann4erford3ledge1yan4n5e2ba2der2lan2ssa0saba3ina5y4rah3ra4ina2cha4i2de3ira2ffi3iya2gara2hale3en2idah2kari3inah3ti3ura2lihah4m5ah4na3ly3oman5e2m3antha4ra3ien4rah3mon3son3uel2ncia3ders4ia4on5r4ra5ine4ya3ford2ra4h4i5d3ee4na3gent3i4sha3ngin3ojin2sha4enka2tinka2ul3nders2vanna2wyer2xon1chuyler2otia4t1ean3rlait3son2basten6ian7en2ema2if2la3by3ena3ina3ma2mele2non3ta2rafina3gio3ilda2sha2th2ung2verin3ilin2ward2ymour1haine3kira4o3mmara3na5ta4dra5y4e4i4ley4na5on4tay5ha3rman4on4ri3shi3wn3yndel2ea3ba3ena3ffield3ila3la4by4don4ley5y3n3ridan4man4ri4win5ood2ika3n4a4g3ra4ley2obi3shana2unnar1ibley3ongile3yl2dney3onia3ra2egfried3rra2gourney2ham2las3eas3va4ia2mba3on5e2ne4ad2obhan2ran3ena3oun2tara3embile2v3an3e1kip2yler1lade2evin1mith1ofi2lana5ge3edad3ita3omon2ndra3ia3ja3ya2phia5e4ronia2rgan2terios1palding2encer4ser2ica1tacey4ia4y3ndford4ley4ton3sio2efan6ia3lla3phan7i8e5en3r4ling3sha3van4e5n3wart2ockard3ke3rm3yan2rom2uart1ubrey2katai3i2laiman3lican2mi3mer3ner2n2san5na2therland3ton2zanne1ven3tlana1ybil2delle3ney2eira2lvester4ia2na3ia0tab3ari3itha2ci4ta2d3i2ffy2hirah2i3ma3nn3pa3te2jo2ka4ra3iyah3oda2lasi3bart4ot3e3ia4tha3lulah3man3os2m3a4ra5y3ma4y2naka3ek3i3ner3o3sy3ya2o2ra3o2te3yana2urin2wnie4y2yce3lor1eague2hya2kla2m3ina2rence5tia4se3rence4ill6yn4y3tia3yn2sia3s4a1haddeus4ea3i4s3lassa4ia3man3n4a4e4os3ra2ea3kla3lma3obald4dore6sia4ne3ra4on2ierry3rza2omas3ra4pe2urston2yra1ia3ra2balt2enette3rnan5ey4ra2ffany2lda2mandra3othy2na2ponya2rza2tus2vona1obey3ias3y2d3d2la2mas2ng2r3a3i4n3rance3y2sia2ve2wnsend1racey4y3vers4is2easa3main7e3nt3sa3va4or3y2ianon3cia3lby3na4d3sh5a4tan2oy2udy2yne3on3phena1ucker2lly1yee2ler2mon2ne2rone0ula3ni2tima1ma1na2dine1pton1rania2iah4n5a2sula1ta0vala3entina4ria6e4ska3onia4ra2n3ce3da3essa3ora3ya2shti2ughn1eda2lika3ma2nesssa2ra3ena3ity3n4on3onica2sta2vila1ictor6ia2donia2ncent3son2olet6ta2rgil5nia3idis2to2veka3ian1lad4imir1okes2leta3f1rinda0wade2gner2kanda2lden4o3ker3lace4y3ter2nda3eta2rd3ner3ren2tson2ylan6d4on3ne1ebb3ster2ndell4y2sley3ton2ylin1hilhelmina3taker4ney1ijdan2lfen3l4ard4em4iam4ow3ma3ona3son2nda3ema3ifred3na3ona3ston3throp1lby1oody1yatt2nee3n3ona0xanthe2veria3ier6a1ena3ia3os2rxes1imen5a1ylia3ona0yachne2kecan2le2ncey3ice2rdley3in3milla2smeen4in1elinda2nene2rik3o3vant2smina2tta2va1okiko2landa3ie2nina2rk2vela1usuf1vella3s3tte2onne0zachariah6y3kery2da2hara3irah3ra2id4e2kia2lea3ika3tana2ndra3e3iel3n2ra4h3ed4k2za1ehava2ke2lda3enka3ia3la2na4ide3ia3on2rlinda2va3ida1ia3zan2gana2la2na3nia2on2ta2ven1oe2la2na2ra4h3da3n2sia1uleika4ma2za4nny");ap=[None]
	def ay():
		a=ap[0]
		if a is None:
			a,b=set(),""
			for d,c in re.findall(r"(\d)([a-z]*)",ax):b=b[:int(d)]+c;a.add(b)
			ap[0]=a
		return a
	def aq(name):return Kit.checksum(name.lower().encode("utf-8"))if Kit.streamer and name else 0
	def o(name,serial=0):return Kit.veil("name",name,serial or aq(name))
	def H(name,serial,noto):a=Kit.noto_mark(noto);return(a+" "if a else "")+Kit.veil("name",name,serial or aq(name))
	def az():
		eM="ultima";aD="Ultima Tracker";eN=aD+":";bo=.25;eO=.15;eP=.05;eQ=.45;aS=85;cm,cn=50,200;co,cp=1,24;eR=32;cq=210;cr=90;eS=200;eT=18;eU=12;c5=14;eV=8;c6=220;eW=16;eX=11;a1=170;bJ=600;bK=1;cs=10;ct=5.;cu=12;c7=18;eY=20.;eZ=12;e_=2;e0=("invulnerable",);e1=("innocent","ally");e2=[API.Notoriety.Gray,API.Notoriety.Criminal,API.Notoriety.Enemy,API.Notoriety.Murderer];c8="ultima.foe";e3=743;cv,cw=1,60;bL=2000;e4=200;cx=60.;c9=30.;bM=12;da=30.;e5=5365;cy=60.;e6=60.;e7=6;e8=40;db=30.;dc=160;e9={0:"Fel",1:"Tram",2:"Ilsh",3:"Malas",4:"Tok",5:"TerM"};cz=(("All players",None),("Red only",("murderer",)),("Grey only",("gray","criminal")),("Orange only",("enemy",)),("Blue only",("innocent",)),("Foe list","foe"));cA=(("Last hour",3600.),("Today","today"),("All time",None));cB="UltimaTracker_sight_pos";bN="UltimaTracker_sight_min";bO="UltimaTracker_sight_open";cC="UltimaTracker_killer_pos";cD="UltimaTracker_killer_min";fa=.5;bP=6;bQ=("friend","foe","neutral","combat","panel");fb=4;fc=10;cE=5000;fd=4000;dd=4000;fe=1.;am=6;ff=24;de=13;fg=20;bp="#3A3A3A";bR="#5E4E24";df="#DDDDDD";fh="#F0C850";fi="#A8A8A8";bS="#DDDDDD";bT="#999999";fj="#7D6E52";dg={"friend":"Friends","foe":"Foes","neutral":"Neutral","combat":"Combat"};dh={"friend":"#5CE65C","foe":"#FF5050","neutral":"#9EC8FF","combat":"#FFB050","panel":"#FFD966"};bq={"friend":"#3AA0D4","foe":"#D93030","neutral":"#B8B8B8","combat":"#B32D2D"};bU="#2E9E3A";di="#FF2020";fk=50;fl=1.2;dj,fm=.1,.55;dk=32;fo=.1;dl="#B8902A";dm="#2A8C9E";dn="#D8CCB0";do=3617;fp=1;fq=3.;fr=3.5;bV="#3A6FD8";dp="#21A39A";cF="#555555";fs={"innocent":"#4FA3FF","ally":"#40E040","gray":"#B0B0B0","criminal":"#B0B0B0","enemy":"#FF9A2E","murderer":"#FF4040","invulnerable":"#FFE14D","unknown":"#DDDDDD",};ft,fu=10,18;fv=Kit.WINDOW_BG;fw=Kit.SECTION_TILE;fx=Kit.SECTION_TILE;br=3;fy=Kit.STONE_TILE;dq=2092;fz=.6;fA=(Kit.ART_MIN[0],Kit.ART_RESTORE[0]);fB=(2103,2104);cG=1153;fC={bp:0,bR:53,dl:53,dm:89,dn:0,bU:63,bV:1152};fD=[((235,235,235),1153),((150,150,150),946),((225,55,55),34),((70,220,70),63),((90,150,255),89),((255,155,45),144),((255,220,80),53),((25,25,25),0)];aO=Kit.data_path("_ultima_tracker_data.txt");dr=os.path.join(Kit.script_dir(),"_player_tracker_data.txt");aE=["friend","foe","neutral"];ds={"scale":(cm,cn),"opacity":(0,100),"range":(co,cp),"alert_minutes":(cv,cw),"sort":(0,2)};dt=("scale","opacity","range","alert_minutes","sort");du=("name","distance","HP");dv=("sync","magery","combat_shown","combat_only","healing","borders","alert_red","alert_foes","alert_orange","alert_gray","sightings","killer");cH={"friend":[40,140,240,220,False,False,aS],"foe":[290,140,240,220,False,False,aS],"neutral":[540,140,240,220,False,False,aS],"combat":[300,200,c6,0,False,False,aS],"panel":[40,380,0,0,False,False,aS],};ac={hr:list(hs)for hr,hs in cH.items()};P={"scale":100,"opacity":aS,"range":18,"sync":False,"magery":False,"combat_shown":True,"combat_only":True,"healing":False,"borders":True,"alert_red":True,"alert_foes":True,"alert_orange":False,"alert_gray":False,"alert_minutes":5,"sightings":True,"killer":True,"sort":0};dw=dict(P);fE={"dirty_save":False,"foe_ver":0,"combat_loaded":False,"shutting":False,"started":False,"loaded":False};ai={"minimized":False,"shutting":False,"docked":False,"queue":[],"dirty_save":False,"foe_ver":0,"combat_loaded":False,"started":False,"loaded":False,"party":set()};hn={"g":None,"c":{},"store":({},{})};ba,ho,aj=Kit.basics(ai,aD);au={};bs=[];cI=[];bW=Kit.MARGIN+30+Kit.GAP;dz=2*Kit.MARGIN+30
		def fF(*a):cI.append(True)
		aT={};aw={};aF=[];ax={};ao={};ap={"ver":0,"seen_ver":0,"dirty":False,"save_at":0.};bb={};bt={};bu={};bX=set();ay={};aU=[None]
		def sc(v,scale=None):s=P["scale"]if scale is None else scale;return max(1,int(round(v*s/100.)))
		fG=13;cJ=20
		def bY(s):return s if s>1. else 1.
		def bZ(v):return Kit.tsize(sc(v)if P["scale"]>100 else int(v))
		def dA(text,width):width=max(20,int(width));return[Kit.fit(a,width)for a in Kit.wrap(text,width)]
		def dB(parent,lines,x,y):a=b2(bT);return[Kit.inert(Kit.add_label(parent,c,x,y+b*cJ,a))for b,c in enumerate(lines)]
		al={"req":False,"size":{},"own_size":{},"force":set(),"made":{}};fH=3
		def dC():
			for k,v in cH.items():ac[k]=list(v)
		def dD():at.clear();P.update(dw);al["req"]=False;ar["serial"]=None;dC()
		def aP(v,lo,hi):return max(lo,min(hi,v))
		def bv():return API.StopRequested
		def cK(text,n):return text if len(text)<=n else text[:max(1,n-2)]+".."
		def bx(text,size,color,**a):return Kit.inert(G.CreateGumpTTFLabel(text,size,color,**a))
		def a2(opacity,color):return Kit.inert(G.CreateGumpColorBox(opacity,color))
		def aV(b,a):
			try:b.SetAlpha(a)
			except Exception:pass
		def aM(c):aG.pop(id(c),None);Kit.dispose(c)
		b_=[];fI=.15;bc={}
		class RowClick(object):
			__slots__=("row","make")
			def __init__(self,row,make):self.row,self.make=row,make
			def bind(self):
				r=self.row;b,c=r.serial,r.name;a=r.prev
				if a is not None and time.time()-a[2]<fI:b,c=a[0],a[1]
				if b is None:return
				return self.make(b,c)
		def fJ():return{"alt":L(),"shift":bool(ae("shift"))}
		def av(fn):
			def a(*a):
				f=fn.bind()if type(fn)is RowClick else fn
				if f is not None:b_.append((f,fJ()))
			return a
		def dE(c,fn):Kit.on_click(c,av(fn))
		def fK():
			while b_:
				a,b=b_.pop(0);bc.clear();bc.update(b)
				try:a()
				except Exception as c:
					if N():return
					bd(c)
				finally:bc.clear()
		def bd(b):
			a=str(b)
			if a not in aC["errors"]:aC["errors"].add(a);aj("error (still running): "+a,Kit.HUE_BAD)
		be=[False];bz=[];bf=[]
		def dF(q):
			while q:
				a=q.pop(0)
				try:a()
				except Exception as b:
					if N():return True
					bd(b)
		def aQ(x,y,w,h,fn,tip=None):c=G.CreateGumpColorBox(.01,"#000000");c.SetRect(x,y,w,h);dE(c,fn);return Kit.with_tip(c,tip)
		def b0(graphic,x=0,y=0,hue=0):return Kit.inert(G.CreateGumpPic(graphic,x,y,Kit.look_hue(graphic,hue)))
		def aK(graphic,w,h,hue=0):return Kit.inert(G.CreateTiledGumpPic(graphic,max(0,w),max(0,h),Kit.look_hue(graphic,hue)))
		def fL():
			aw.clear();e=aw["icons"]={}
			for f,b in(("lock",(dq,dq)),("min",fA),("opacity",fB)):
				c=[Kit.pic_size(i)for i in b]
				if all(g and k for g,k in c):e[f]=list(zip(b,c))
			d="Name the 75% PSN 12y Foes (3)";a=G.CreateGumpLabel(d,cG);w,h=int(a.GetWidth()),int(a.GetHeight());a.Dispose()
			if w>0 and h>0:aw["char_w"]=w/float(len(d));aw["font_h"]=h
		cL={};dG=dict(("#%02X%02X%02X"%Kit.CB_RGB[ht],Kit.CB_HUE[ht])for ht in Kit.CB_RGB)
		def b1(noto,default):return Kit.cb_hex(noto,fs.get(noto,default))
		def b2(color):
			if Kit.cblind and color in dG:return dG[color]
			h=cL.get(color)
			if h is not None:return h
			c=color.lstrip("#");r,g,e=int(c[0:2],16),int(c[2:4],16),int(c[4:6],16);a,b=cG,None
			for(f,i,j),k in fD:
				d=(f-r)**2+(i-g)**2+(j-e)**2
				if b is None or d<b:a,b=k,d
			if len(cL)<256:cL[color]=a
			return a
		dH={}
		def fM(color):
			v=dH.get(color)
			if v is None:c=color.lstrip("#");v=dH[color]=(int(c[0:2],16),int(c[2:4],16),int(c[4:6],16))
			return v
		def b3(size):return "char_w"in aw and ft<=size<=fu
		def fN(size):return aw["char_w"]if b3(size)else size*.58
		aG={};dI=[dd]
		def aH(text,size,color,aligned="left",maxWidth=0,applyStroke=False):
			if applyStroke or not b3(size):a=bx(text,size,color,aligned=aligned,maxWidth=maxWidth,applyStroke=applyStroke);aG.pop(id(a),None);return a
			if len(aG)>dI[0]:
				for k,v in list(aG.items()):
					if v[0].IsDisposed:del aG[k]
				dI[0]=max(dd,2*len(aG))
			text=dJ(text,maxWidth);a=Kit.inert(G.CreateGumpLabel(text,b2(color)));aG[id(a)]=[a,aligned,maxWidth,size,0,0,text];return a
		def cM(a):m=aG.get(id(a));return m if m is not None and m[0]is a else None
		def dJ(text,a):
			if a and len(text)*aw.get("char_w",7)>a:return cK(text,max(2,int(a/aw.get("char_w",7))))
			return text
		def az(b,x,y,text=None):
			m=cM(b)
			if m is None:b.SetPos(x,y);return
			m[4],m[5]=x,y;d,a,f=m[1],m[2],m[3]
			if text is None:text=m[6]
			e=int(len(text)*aw["char_w"]);c=0
			if a and d=="right":c=max(0,a-e)
			elif a and d=="center":c=max(0,(a-e)//2)
			g=int(round((f*1.35-aw["font_h"])/2.));b.SetPos(int(x+c),int(y+g))
		def aR(a,text):
			m=cM(a)
			if m is None:a.SetText(text);return
			text=dJ(text,m[2])
			if text==m[6]:return
			m[6]=text;a.Text=text
			if m[1]!="left"and m[2]:az(a,m[4],m[5],text)
		def dK(a,color):
			if cM(a)is None:return False
			a.Hue=b2(color);return True
		def dL():return bool(bc.get("shift")or ae("shift"))
		def aN():return bc.get("alt")or L()
		def fO():return[a for a in aE+["combat","panel"]if p("hub"if a=="panel"else "ultima."+a)]
		def b4():return bool(SNAP.drag)or SNAP.pressed()is True
		b5={};fP=2000
		def b6(text,px,size,smooth=False):
			if size>fG and(smooth or not b3(size)):b=size*.6 if smooth else fN(size);return cK(text,max(4,int(px/b)))
			k=(text,px);a=b5.get(k)
			if a is None:
				if len(b5)>fP:b5.clear()
				a=b5[k]=Kit.fit(text,max(10,int(px)))
			return a
		def bg(top,h,font):return top+max(0,int((h-font*1.35)/2))
		def a3(parent,x,y,w,h,text,fn,tip=None,face=bp,color=bS,font=12,store=None):
			f=aK(fy,w,h,fC.get(face,b2(face)));f.SetPos(x,y);color="#141414";parent.Add(f);a=aH(text,font,color,aligned="center",maxWidth=w);az(a,x,bg(y,h,font));parent.Add(a);c=aQ(x,y,w,h,fn,tip);parent.Add(c)
			if store is not None:store.extend([f,a,c])
			return a
		def b7():return(2 if P["magery"]else 0)+(1 if P["healing"]else 0)
		aW="Alt+click: auto-follow (again to stop)";fQ=("Cast Heal on %s (Shift+click: Greater Heal). Alt+click: auto-follow (again to stop)");fR=("Cast Cure on %s (Shift+click: Arch Cure). Alt+click: auto-follow (again to stop)");fS="Bandage %s when adjacent; farther away, follow them (again to stop). "+aW
		def dM(parent,x,y,w,h,serial,name,store=None,row=None):
			j=max(7,int(h*.7/min(1.,P["scale"]/100.)));e,b,f=[],[],[]if store is None else store
			if P["magery"]:
				for c,g,i,a,d in(("H","Heal","Greater Heal",fQ,dl),("C","Cure","Arch Cure",fR,dm)):b.append((c,ey(serial,g,i)if row is None else RowClick(row,(lambda a,st:lambda s,n:ey(s,a,st))(g,i)),a,d,"#FFFFFF"))
			if P["healing"]:b.append(("B",dP(serial,name)if row is None else RowClick(row,dP),fS,dn,"#202020"))
			for c,k,a,d,l in b:a3(parent,x,y,w,h,c,k,a%o(name,serial),face=d,color=l,font=j,store=f);e.append((f[-1],a));x+=w+2
			return e
		def dN(s):return max(16,int(round(ff*s)))
		def dO(s):return max(16,int(round(fg*s)))
		def fT(serial):
			if safe(I)==serial:return True
			return Follow.start(serial,aD)
		def bi(serial):S(serial,aD)
		def bA(serial,fn):
			def a(*a):
				if aN():bi(serial)
				else:fn()
			return a
		ar={"serial":None,"name":"","state":None,"until":0.,"follow":None}
		def bB(serial):
			if serial is None or ar["follow"]!=serial:return
			ar["follow"]=None
			if safe(I)==serial:Follow.stop(aD)
		def dP(serial,name):
			def a(*f):
				if ar["serial"]==serial:ar["serial"]=None;aX("bandage");bB(serial);aj("stopped bandaging %s; cursor released."%name,Kit.HUE_GOOD);return
				try:
					a=API.FindMobile(serial)
					if a is None or bool(a.IsDead):a=None
					else:b=API.Player;d=max(abs(int(a.X)-int(b.X)),abs(int(a.Y)-int(b.Y)))
				except Exception:a=None
				if a is None:aj("can't bandage %s (out of sight or dead)."%name,Kit.HUE_BAD);return
				if d>fp:
					if ar["follow"]==serial and safe(I)==serial:bB(serial);aj("stopped following %s."%name,Kit.HUE_GOOD);return
					e=safe(I)!=serial
					if not fT(serial):return
					if e:ar["follow"]=serial
					aj("following %s; press B again when adjacent."%name,Kit.HUE_INFO);return
				c=API.FindType(do,API.Backpack)or API.FindType(do)
				if not c:aj("no bandages in your backpack.",Kit.HUE_BAD);return
				if ar["serial"]is not None or b9()is not None or API.HasTarget("any"):aj("a target cursor is up; clear it, then press B.",Kit.HUE_BAD);return
				API.UseObject(c);ar.update(serial=serial,name=name,state="cursor",until=time.time()+fq);dQ("bandage",fr)
			return Kit.once(bA(serial,a),("ultima.bandage",serial),Kit.TWICE)
		b8="ultima";a4={"bandage":False,"spell":False}
		def dQ(what,a):a4[what]=True;HOST.claim_cursor(b8,a)
		def aX(what):
			if not a4.get(what):return
			a4[what]=False
			if not any(a4.values()):HOST.release_cursor(b8)
		def b9():return HOST.cursor_busy(b8)
		def dR():
			a=b9()
			if a is not None and a!="pick":return False
			return bool(API.HasTarget("any"))
		def fU():
			s=ar["serial"]
			if s is None:aX("bandage");return
			c=ar["name"]
			try:b=API.FindMobile(s);a=b is None or bool(b.IsDead)
			except Exception:a=True
			if a or time.time()>ar["until"]:ar["serial"]=None;bB(s);aj(("can't bandage %s (out of sight or dead)."if a else "no target cursor for bandaging %s.")%c,Kit.HUE_BAD);return
			if ar["state"]=="cursor"and a4["bandage"]and HOST.cursor_ok(b8,"beneficial"):API.Target(s);ar["serial"]=None;aX("bandage");bB(s)
		def fV():
			safe(I);s=Follow.serial
			if s is not None and X(s)is None:Follow.serial=None
			if ar["follow"]is not None and Follow.serial!=ar["follow"]:ar["follow"]=None
		dS=((3,4,3,8,"#FFFFFF"),(6,4,3,8,"#A0A0A0"),(9,4,3,8,"#5A5A5A"));fW={("lock",True):((3,8,10,6,None),(7,10,2,2,bR),(4,2,8,2,None),(4,2,2,6,None),(10,2,2,6,None)),("lock",False):((3,8,10,6,None),(7,10,2,2,bp),(4,0,8,2,None),(4,0,2,8,None),(10,0,2,3,None)),("min",True):((4,4,8,2,None),(4,4,1,8,None),(11,4,1,8,None),(4,11,8,1,None)),("min",False):((4,10,8,2,None),),("opacity",True):dS,("opacity",False):dS}
		def fX(add,d,x,y,a,kind,on):
			u=a/16.
			def R(v):return int(round(v*u))
			def S(v):return max(1,int(round(v*u)))
			e=(fh if on else fi)if kind=="lock"else df
			for f,g,h,i,j in fW.get((kind,bool(on)),()):add(x+R(f),y+R(g),S(h),S(i),j or e)
			if kind=="close":b=max(8,int(a*.8));c=bx("x",b,df,aligned="center",maxWidth=a);c.SetPos(x,y+max(0,int((a-b*1.35)/2)));d(c)
		bC={};aY=[]
		def dT():
			for c in list(aY):
				if c.gump.IsDisposed:aY.remove(c)
				else:c.frame.apply_borders()
		class Frame(object):
			def __init__(self,gump):
				self.size=(0,0);self.center=aK(fw,1,1);gump.Add(self.center);self.edges=[aK(fv+(1 if a in(0,1)else 3),1,1)for a in range(4)]
				for b in self.edges:gump.Add(b)
			def layout(self,w,h):
				self.size=(w,h);a=[(0,0,w,am),(0,h-am,w,am),(0,0,am,h),(w-am,0,am,h)]
				for b,r in zip(self.edges,a):b.SetRect(*r)
				self.apply_borders()
			def apply_borders(self):
				a=P["borders"]
				for p in self.edges:aV(p,1. if a else 0.)
				w,h=self.size
				if a:self.center.SetRect(am,am,max(0,w-2*am),max(0,h-2*am))
				else:self.center.SetRect(0,0,w,h)
			def set_alpha(self,a):aV(self.center,a)
		class KitFrame(object):
			def __init__(self,gump,key=None):
				self.gump,self.key=gump,key;self.top=0;a=Kit.WINDOW_BG;self.s=[Kit.pic_size(a+b)for b in range(9)];self.kw,self.kh=Kit.pic_size(Kit.CORNER_ART);self.fill=aK(a+4,1,1);self.center=aK(Kit.SECTION_TILE,1,1);self.edges=[aK(a+d,1,1)for d in(1,7,3,5)];self.corners=[b0(a+e,0,0)for e in(0,2,6,8)];self.knots=[b0(Kit.CORNER_ART,0,0)for g in range(4)];self.parts=[self.fill]+self.edges+self.corners+self.knots
				for c in[self.fill,self.center]+self.parts[1:]:gump.Add(c)
				Kit._frame_parts[gump]=self.parts
			def layout(self,w,h,top=None):
				if top is not None:self.top=top
				M=Kit.MARGIN;a,t,b,l,n,r,c,f,d=self.s;self.fill.SetRect(l[0],t[1],max(0,w-l[0]-r[0]),max(0,h-t[1]-f[1]))
				for j,e in zip(self.edges,((a[0],0,w-a[0]-b[0],t[1]),(c[0],h-f[1],w-c[0]-d[0],f[1]),(0,a[1],l[0],h-a[1]-c[1]),(w-r[0],b[1],r[0],h-b[1]-d[1]))):j.SetRect(e[0],e[1],max(0,e[2]),max(0,e[3]))
				for k,g in zip(self.corners,((0,0),(w-b[0],0),(0,h-c[1]),(w-d[0],h-d[1]))):k.SetPos(*g)
				for m,g in zip(self.knots,((0,0),(w-self.kw,0),(0,h-self.kh),(w-self.kw,h-self.kh))):m.SetPos(*g)
				i=h-self.top-M;self.center.SetRect(M,self.top,max(0,w-2*M),max(0,i));Kit.set(self.center,"IsVisible",i>4)
			def apply_borders(self):pass
			def set_alpha(self,a):aV(self.center,a)
			def drop_all(self):
				for c in[self.center]+self.parts:aM(c)
				if Kit._frame_parts.get(self.gump)is self.parts:Kit._frame_parts.pop(self.gump,None)
		class Chrome(object):
			def __init__(self,gump,kit=False,key=None):self.gump=gump;self.kit,self.key=kit,key;self.frame=KitFrame(gump,key)if kit else Frame(gump);aY[:]=[a for a in aY if a.gump is not gump and not a.gump.IsDisposed];aY.append(self);self.strip=[];self.title_bg=self.title_lbl=self.slider=self.pct_lbl=None;self.title_text=self.title_color=self.title_raw=self.status_x=None;self.status_lbl=self.status_text=None;self.title_max,self.title_pos,self.font=40,(0,0),de;self.opacity,self.content_top=aS,am;self.on_title_alt,self.alt_key=None,None
			def _add(self,ctrl):self.gump.Add(ctrl);self.strip.append(ctrl);return ctrl
			def _clear_strip(self):
				for c in self.strip:aM(c)
				self.strip=[];self.title_bg=self.title_lbl=self.slider=self.pct_lbl=None;self.status_lbl,self.status_text=None,None
			def dispose(self):
				self._clear_strip();self.frame.drop_all()
				if self in aY:aY.remove(self)
			def layout(self,w,h,s,opacity,title,color,buttons,l,m,o,p):
				self.opacity=opacity;g=opacity/100.;self.frame.layout(w,h);self.frame.set_alpha(g);self._clear_strip();a=dN(s);self.title_bg=self._add(aK(fx,w-2*am,a));self.title_bg.SetPos(am,am);aV(self.title_bg,g);q=self._add(aK(Kit.STONE_TILE,w-2*am,br));q.SetPos(am,am+a-br);b=max(12,a-6-br);i=max(2,int(round(2*s)));n=len(buttons);e=w-am-4-n*b-max(0,n-1)*i;j=e;self.on_title_dbl=m;self.on_title_alt,self.alt_key=o,p;self._title_catch(am,max(10,j-am-2),a,Kit.DOUBLE_TIP+". "+aW);r=am+(a-br-b)//2
				for t,u,v,x in buttons:self._button(e,r,b,t,u,v,x);e+=b+i
				self.font=max(9,int(round(de*bY(s))));self.title_max=max(20,j-am-10);self.title_pos=(am+5,bg(am,a-br,self.font));self.title_color=color;self.title_text=None;self.set_title(title);y=am+a
				if l:c=dO(s);d=max(8,int(round(11*bY(s))));z=self._add(aH("Opacity",d,bT));az(z,am+5,bg(y,c,d));f=int(round(34*s));k=am+int(round(54*s));A=max(40,w-am-8-f-k);self.slider=G.CreateSlider(A,0,100,opacity,k,y+max(2,(c-10)//2),True);self._add(self.slider);self.pct_lbl=self._add(aH("%d%%"%opacity,d,bS,aligned="right",maxWidth=f));az(self.pct_lbl,w-am-4-f,bg(y,c,d));y+=c
				self.content_top=y
			def _title_catch(self,xy,w,h,tip):
				a=aQ(xy,xy,w,h,self._title_clicked,tip);Kit.set(a,"CanMove",True)
				if Client.mouse is None:Kit.hook_double(a,self._dbl_once())
				self._add(a)
			def _dbl_once(self):return Kit.once(lambda:self.on_title_dbl(),("utitle",id(self)))
			def layout_kit(self,w,h,opacity,title,color,mini,d,i):
				M=Kit.MARGIN;self._clear_strip();self.content_top=bW;self.frame.layout(w,h,bW);self.frame.set_alpha(opacity/100.);e=self._add(aK(Kit.SECTION_TILE,w-2*M,30));e.SetPos(M,M);aV(e,Kit.SECTION_ALPHA)
				if not mini:self._add(a2(1.,color)).SetRect(M,M+30,w-2*M,3)
				a=w-M-54
				if not Kit.zone_up(self.key):
					self._art((Kit.ART_RESTORE if mini else Kit.ART_MIN)[0],a,M+7,d,Kit.RESTORE_TIP if mini else Kit.MIN_TIP);a-=Kit.DOCK_DX
					if not mini:self._art(Kit.ART_DOCK[0],a,M+7+Kit.DOCK_DY,i,Kit.DOCK_TIP);a-=10
				b=a
				if not mini:
					f="Settings";c=a-35-Kit.text_w(f)
					if c>M+30+Kit.text_w("COMBAT")+40:self._art(Kit.ART_PAGE[0],c,M+4,fF,Kit.SETTINGS_TIP%aD,f);b=c
				g=Kit.zone_up(self.key);self.on_title_dbl=(lambda:None)if g else d;self._title_catch(M,max(10,b-M-6),30,None if g else Kit.DOUBLE_TIP);self.title_max=max(20,b-M-30-10);self.title_pos=(M+30,M+7);self.title_color=color;self.title_text=None;self.set_title(title)
			def _art(self,graphic,x,y,fn,tip,cap=None):
				p=self._add(b0(graphic,x,y));a,b=Kit.pic_size(graphic);a,b=a or 20,b or 20
				if cap:c=Kit.add_label(self.gump,cap,x+a+5,y+3,Kit.HUE_TEXT);self.strip.append(c);a+=5+Kit.text_w(cap)
				self._add(aQ(x,y,a,b,fn,tip));return p
			def set_status(self,text):
				if not self.kit or self.title_lbl is None:return
				text=text or ""
				if text==self.status_text:return
				self.status_text=text;x=self.title_pos[0]+Kit.text_w(self.title_text or "")+12;b=self.title_pos[0]+self.title_max-x;c=Kit.fit(text,b)if b>20 else "";a=(x,self.title_pos[1])
				if self.status_lbl is None:self.status_lbl=Kit.add_label(self.gump,c,x,self.title_pos[1],Kit.HUE_INFO);self.strip.append(self.status_lbl);self.status_x=a
				else:
					if a!=self.status_x:self.status_x=a;self.status_lbl.SetPos(x,self.title_pos[1])
					Kit.set_text(self.status_lbl,c)
			def _title_clicked(self,*h):
				f=time.time();d=id(self.gump);a=(self.gump.GetX(),self.gump.GetY())
				if self.on_title_alt is not None and aN():
					b=self.alt_key;e=at.pos.get(b)if b is not None else None;g=(b is not None and at.moving==b)or SNAP.drag or(e is not None and(abs(a[0]-e[0])>bP or abs(a[1]-e[1])>bP))
					if not g:self.on_title_alt()
					return
				c=bC.get(d)
				if c and f-c[0]<=fa and abs(a[0]-c[1][0])<=bP and abs(a[1]-c[1][1])<=bP:bC.pop(d,None);self._dbl_once()()
				else:
					if len(bC)>ab:bC.clear()
					bC[d]=(f,a)
			def _button(self,x,y,a,kind,on,fn,tip):
				b=aw.get("icons",{}).get(kind)
				if b:
					e,(c,d)=b[1 if on else 0]
					if c<=a+6 and d<=a+6:
						f=34 if kind=="lock"and on else 0;p=self._add(b0(e,x+(a-c)//2,y+(a-d)//2,f))
						if kind=="lock"and not on:aV(p,fz)
						self._add(aQ(x,y,a,a,fn,tip));return
				if kind=="close"and "char_w"in aw:g=Kit.inert(self._add(G.CreateGumpLabel("x",cG)));g.SetPos(x+max(0,(a-int(aw["char_w"]))//2),y+(a-aw["font_h"])//2);self._add(aQ(x,y,a,a,fn,tip));return
				h=on and kind in("lock","opacity");i=self._add(a2(1.,bR if h else bp));i.SetRect(x,y,a,a)
				def j(a,by,bw,bh,col):p=self._add(a2(1.,col));p.SetRect(a,by,bw,bh)
				fX(j,self._add,x,y,a,kind,on);self._add(aQ(x,y,a,a,fn,tip))
			def set_title(self,text,color=None):
				if self.kit:
					b=(text,self.title_max)
					if self.title_lbl is not None and b==self.title_raw:return
					self.title_raw=b;text=Kit.fit(str(text).upper(),self.title_max)
					if self.title_lbl is None:self.title_lbl=Kit.add_label(self.gump,text,self.title_pos[0],self.title_pos[1],Kit.HUE_TITLE);self.strip.append(self.title_lbl);self.title_text=text
					elif text!=self.title_text:
						self.title_text=text;Kit.set_text(self.title_lbl,text)
						if self.status_text is not None:c,self.status_text=self.status_text,None;self.set_status(c)
					return
				if color is not None and color!=self.title_color:
					self.title_color=color;a=self.title_lbl
					if a is not None and not dK(a,color):
						self.title_text=None
						if a in self.strip:self.strip.remove(a)
						aM(a);self.title_lbl=None
				text=b6(text,self.title_max,self.font)
				if self.title_lbl is None:self.title_lbl=self._add(aH(text,self.font,self.title_color or bS));az(self.title_lbl,*self.title_pos);self.title_text=text
				elif text!=self.title_text:self.title_text=text;aR(self.title_lbl,text)
			def set_opacity(self,v):
				self.opacity=v;a=v/100.;self.frame.set_alpha(a)
				if self.kit:return
				if self.title_bg is not None:aV(self.title_bg,a)
				if self.pct_lbl is not None:aR(self.pct_lbl,"%d%%"%v)
			def poll(self):
				if self.slider is None:return
				v=aP(int(self.slider.Value),0,100)
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
					if k in bQ:a.setdefault(g,[]).append(k)
				return[sorted(b)for b in a.values()if len(b)>1]
			def groups_changed(self):
				if not self.touched:return False
				self.touched=False;a=self.saved_groups()
				if a==self.saved:return False
				self.saved=a;return True
			@staticmethod
			def shift(m,dx,dy,a,wins):x,y,w,h=a[m];g=wins[m][0];b,c=Kit.place(g,x+dx,y+dy,w,h);Kit.moved_by_code(g);a[m]=(b,c,w,h)
			def tick(self,g):
				if self.moving is None and not self.pending and self.linger<=0 and not SNAP.drag:
					for k in list(self.gid):
						if k not in bQ and not fY(k):self.detach(k)
					return
				self.pending=False
				if self.linger>0:self.linger-=1
				c=g()
				for k in list(self.gid):
					if k not in c and k not in bQ:self.detach(k)
				a={s:(int(n.GetX()),int(n.GetY()),int(n.GetWidth())or q[0],int(n.GetHeight())or q[1])for s,(n,q)in c.items()if Kit.is_open(n)};d=fO();e=HOST.layout_arranging();b=[t for t,v in a.items()if t in self.pos and(v[0],v[1])!=self.pos[t]and t not in d]
				if b:
					k=self.moving if self.moving in b else None
					if k is None:
						for m in b:
							if c[m][0]in SNAP.drag:k=m;break
					if k is None:k=b[0]
					h=a[k][0]-self.pos[k][0];i=a[k][1]-self.pos[k][1];f=self.dims.get(k,a[k][2:])!=a[k][2:]
					if f:b=[]
					elif k in self.gid and aN():
						self.detach(k)
						if not self.alt_used:self.alt_used=True;aj("window unanchored.",Kit.HUE_GOOD)
					j=self.host_follows(c[k][0])if b and not e else()
					for m in(self.members(k)if b and not e else[]):
						if m!=k and m not in b and m in a and m not in d and c[m][0]not in j:self.shift(m,h,i,a,c)
					if not f:self.moving=k;self.still=0
				elif self.moving is not None:
					if not SNAP.drag:self.still+=1
					if self.still>=fb:
						k,self.moving=self.moving,None
						if k in a and k not in d and not e:self.snap(k,a,c,d)
						self.linger=fc
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
		at=Anchors()
		def fY(k):return k.startswith("pop:")and int(k[4:])in au
		import _thread;cN=_thread.allocate_lock();bD=[0];ca=[None];cb=[False];a5={};a6=[None];cO=[0.];bE=[0];bj=[0.]
		def dU(fn):_thread.start_new_thread(fn,())
		def dV():
			a=aO if os.path.exists(aO)else f9()or dr
			if not os.path.exists(a):return None,[]
			with cN:
				with open(a,"r")as f:b=f.readlines()
				if a==aO:a6[0]=cP()
			return a,b
		def fZ():
			try:a,b=dV()
			except Exception as c:aj("couldn't read the save file (%s); saving is off this session."%c,Kit.HUE_BAD);return
			dX(a,b)
		def aI():
			if ak["windows"]is not None and not ai.get("shutting"):be[0]=True
			else:cd(background=True)
		def f_(line,links):f[l(line)]=line
		def f0(line,links):z[line.lower()]=line
		def f1(line,links):u[line.lower()]=line;bH[0]+=1
		def f2(line,links):
			if "="not in line:return
			a,b=[c.strip().lower()for c in line.split("=",1)]
			if a in ds:P[a]=aP(int(b),*ds[a])
			elif a in dv:P[a]=b=="true"
		def f3(line,links):
			if "="not in line:return
			a=[b.strip().lower()for b in line.split("=",1)[1].split(",")];a=[c for c in a if c in bQ]
			if len(a)>1:at.add_group(a)
		def f4(line,links):
			if "="not in line:return
			b,c=line.split("=",1);b=b.strip().lower();a=[d.strip()for d in c.split(",")]
			if b not in ac or len(a)<5:return
			ac[b]=[int(a[0]),int(a[1]),int(a[2]),int(a[3]),a[4].lower()=="true",len(a)>5 and a[5].lower()=="true",aP(int(a[6]),0,100)if len(a)>6 else P["opacity"]]
			if b=="combat":ai["combat_loaded"]=True
		def f5(line,links):
			e=gg(line)
			if e is not None:aF.append(e);cR(e)
		def f6(line,links):
			if "|"in line:a,b=line.split("|",1);links.append((l(a),l(b)))
		def f7(line,links):
			if "|"not in line:return
			p=line.split("|",5);a=(float(p[0]),int(p[1]),int(p[2]),int(p[3]),{"1":True,"0":False}.get(p[4]));k=l(p[5]);b=ax.get(k)
			if k and(b is None or b[0]<a[0]):ax[k]=a
		dW={"foes":f_,"ignore":f0,"players":f1,"settings":f2,"anchors":f3,"layout":f4,"sightings":f5,"links":f6,"foe_seen":f7}
		def dX(path,lines):
			if path is None:cb[0]=True;return
			b=None;e=[]
			try:
				for g in lines:
					try:
						a=g.strip()
						if not a or a.startswith("#"):continue
						if a.startswith("[")and a.endswith("]"):b=a[1:-1].strip().lower();continue
						if b in dW:dW[b](a,e)
					except Exception:continue
				d4();ea()
				for c,d in e:
					if c!=d and c in f and d in f:ao[c]=d
				d7()
				for h in ac:L=ac[h];L[0],L[1]=Kit.adapt(L[0],L[1],L[2],L[3])
				cb[0]=True
			except Exception as i:aj("couldn't read the save file (%s); saving is off this session."%i,Kit.HUE_BAD)
			if path==dr:
				for k in("friend","foe","neutral"):ac[k][6]=P["opacity"]
		def f8():
			if ai["combat_loaded"]:return
			def a(key,default):
				try:return int(API.GetPersistentVar(key,str(default),API.PersistentVar.Char))
				except Exception:return default
			L=ac["combat"];L[0],L[1]=a("CombatBars_X",L[0]),a("CombatBars_Y",L[1]);L[2]=aP(a("CombatBars_W",L[2]),a1,bJ);L[6]=aP(a("CombatBars_Opacity",L[6]),0,100);L[4]=a("CombatBars_Locked",0)==1;L[5]=a("CombatBars_Minimized",0)==1;P["magery"]=a("CombatBars_Magery",0)==1;ai["dirty_save"]=True
		def f9():
			try:d=os.path.dirname(aO)or ".";c=os.path.basename(aO)+".";e=[os.path.join(d,g)for g in os.listdir(d)if g.startswith(c)and g.endswith(".tmp")]
			except Exception:return
			b,a=None,None
			for t in e:
				try:m=os.path.getmtime(t)
				except Exception:continue
				if a is None or m>a:b,a=t,m
			return b
		def ga(text):Kit.write_safe(aO,text,None)
		def cP():return safe(lambda:(os.path.getmtime(aO),os.path.getsize(aO)))
		def gb():
			b=cP();c=time.time()
			if b is None:
				if a6[0]is None:return True
				if not bj[0]:bj[0]=c
				if c-bj[0]<5.:return False
				a6[0]=None;bj[0]=0.;return True
			bj[0]=0.
			if b==a6[0]:return True
			e=Client.on_client_thread()
			if(bE[0]and not e)or c<cO[0]:return False
			try:
				with cN:
					with open(aO,"r")as g:h=g.readlines()
			except Exception as i:cO[0]=c+30.;aj("couldn't read the save file to merge it (%s); saving waits."%i,Kit.HUE_BAD);return False
			f,d=None,[]
			for j in h:
				a=j.strip()
				if a.startswith("[")and a.endswith("]"):f=a[1:-1].strip().lower()
				elif f=="foes"and a and not a.startswith("#"):d.append(a)
			if e:dY(d,b,0);return True
			k=bE[0]=id(d);bf.append(lambda:dY(d,b,k));return False
		def dY(got,c,a):
			if a and a!=bE[0]:return
			bE[0]=0;d=Kit.merge_text("\n".join(got),dict(a5),l)[1];b=dict((l(e),e)for e in d)
			for k in[g for g in f if g not in b]:del f[k]
			f.update(b);a6[0]=c;ai["foe_ver"]+=1
			if a:aI()
		def cc():
			a,ca[0]=ca[0],None
			if a:aj("couldn't save (%s)."%a,Kit.HUE_BAD)
		def dZ():
			if not cb[0]or not gb():return
			def c(b):return "true"if b else "false"
			try:
				a=["# UltimaTracker save file - one name per line"]
				for e,g in(("foes",f),("ignore",z)):a+=["[%s]"%e]+sorted(g.values(),key=lambda s:s.lower())+[""]
				d=bH[0]
				if bI[0]!=d or bI[1]is None:bI[1]=sorted(u.values(),key=lambda s:s.lower());bI[0]=d
				a+=["[players]"]+bI[1]+[""];a+=["[settings]"]+["%s=%d"%(i,P[i])for i in dt];a+=["%s=%s"%(n,c(P[n]))for n in dv]+["","[anchors]"];a+=["group=%s"%",".join(q)for q in at.saved_groups()];a+=["","[layout]"]+["%s=%d,%d,%d,%d,%s,%s,%d"%(t,r[0],r[1],r[2],r[3],c(r[4]),c(r[5]),r[6])for t,r in ac.items()];a+=["","[links]"]+["%s|%s"%(f[v],f[w])for v,w in sorted(ao.items())if v in f and w in f and "|"not in f[v]+f[w]];a+=["","[foe_seen]"]+[gh(m)for m in sorted(f)if m in ax];a+=["","[sightings]"]+[k[gd]for k in aF];return "\n".join(a)+"\n"
			except Exception as h:aj("couldn't save (%s)."%h,Kit.HUE_BAD);return
		def d_(text,seq=None):
			with cN:
				if seq is not None and seq!=bD[0]:return
				try:ga(text);a6[0]=cP();return True
				except Exception as a:ca[0]=str(a)
		def cd(background=False):
			a=dZ()
			if a is None:return
			ai["dirty_save"]=False;ap["dirty"]=False;bD[0]+=1;c=bD[0];d=dict(a5)
			def b():
				if d_(a,c):
					for k,v in d.items():
						if a5.get(k,0)==v:a5.pop(k,None)
			if background:dU(b)
			else:b();cc()
		def gc():
			b={d:CategoryGump(d)for d in aE};a=CombatWindow();ak.update({"windows":b,"combat":a})
			if P["combat_shown"]:a.show()
			ak["panel"]=ControlPanel(b,a);he(b,a);ai["foe_ver"]+=1;aC.update({"last_layout":eG(),"tick":0,"next_scan":0.,"next_combat":0.,"next_glow":0.})
			if Kit.get_var(bO)=="1":a0.show()
		hp=None;ak={"windows":None,"combat":None,"panel":None};bk,ce,bF,d0,d1,d2,cQ,cf,bl,gd=range(10);d3={True:"1",False:"0",None:"-"};ge={"1":True,"0":False}
		def gf(t,serial,noto,facet,x,y,guard,name):return "%d|%d|%s|%d|%d|%d|%s|%s"%(int(t),int(serial),noto,int(facet),int(x),int(y),d3.get(guard,"-"),name)
		def gg(line):
			p=line.split("|",7)
			if len(p)<8 or not p[7]:return
			return[float(p[0]),int(p[1]),p[2]or "unknown",int(p[3]),int(p[4]),int(p[5]),ge.get(p[6]),p[7],l(p[7]),line]
		def cR(e):
			k=e[bl];a=ax.get(k)
			if a is not None and a[0]>e[bk]:return False
			ax[k]=(e[bk],e[d0],e[d1],e[d2],e[cQ]);return k in f
		def gh(k):t,a,x,y,b=ax[k];return "%d|%d|%d|%d|%s|%s"%(int(t),a,x,y,d3.get(b,"-"),f[k])
		def d4():
			n=len(aF)
			if n>bL+e4:del aF[:n-bL]
			if len(ax)>2*bL:
				a=dict((b,c)for b,c in ax.items()if b in f);ax.clear();ax.update(a)
				for e in aF:cR(e)
		def gi(t,serial,name,noto,facet,x,y,guard):
			a=gf(t,serial,noto,facet,x,y,guard,name);e=[float(int(t)),serial,noto,facet,x,y,guard,name,l(name),a];aF.append(e);d4()
			if cR(e):ap["seen_ver"]+=1
			ap["ver"]+=1
			if not ap["dirty"]:ap["dirty"]=True;ap["save_at"]=t+c9
		def d5(noto):return J.get(noto,noto or "unknown")
		def d6(facet,x,y):
			f=e9.get(facet)
			if f is None:f="map %d"%facet if facet>=0 else "?"
			return "%s %d,%d"%(f,x,y)
		def cS(now):a=time.localtime(now);return now-(a.tm_hour*3600+a.tm_min*60+a.tm_sec)
		def cT(t,a):
			try:return time.strftime("%H:%M"if t>=a else "%m/%d %H:%M",time.localtime(t))
			except Exception:return "?"
		def gj(k,now):
			s=ax.get(k)
			if s is None:return "not seen yet"
			t,a,x,y,b=s;return "seen %s, %s%s"%(Kit.ago(now-t,Kit.AGO_WORDS),Kit.veil("place",d6(a,x,y))," (guarded)"if b else "")
		def d7():
			for a in list(ao):
				m,n=ao.get(a),0
				while m in ao and n<10:m,n=ao[m],n+1
				if m is None or m==a or m in ao:ao.pop(a,None)
				else:ao[a]=m
		def d8(main):return sorted(b for b,c in ao.items()if c==main)
		def cU(k):
			m=ao.get(k)
			if m is not None:return "alt of "+o(f.get(m,m))
			a=d8(k)
			if a:return "alts: "+", ".join(o(f.get(b,b))for b in a)
			return ""
		def gk(a,b):
			c=ao.get(a,a)
			if b==c or ao.get(b)==c:return "%s and %s are already linked."%(f.get(a,a),f.get(b,b))
			d=ao.get(b,b)
			for k in list(ao):
				if ao[k]==d:ao[k]=c
			if d!=c:ao[d]=c
			ao[b]=c;ao.pop(c,None);d7();return "linked %s as an alt of %s."%(f.get(b,b),f.get(c,c))
		def d9(k):
			if k in ao:del ao[k];return True
			a=d8(k)
			if not a:return False
			b=a[0];del ao[b]
			for c in a[1:]:ao[c]=b
			return True
		bG={};gl=10.
		def gm(name):
			b=HOST.services.get("social.note")
			if b is None or not name:return ""
			c=time.time();a=bG.get(name)
			if a is not None and 0.<=c-a[0]<gl:return a[1]
			try:n=str(b(name)or "").strip()
			except Exception:return ""
			n=n if len(n)<=dc else n[:dc-2]+".."
			if len(bG)>500:bG.clear()
			bG[name]=(c,n);return n
		def aZ(tip,name,extra=""):
			a=[tip]
			if extra:a.insert(0,extra)
			b=cU(l(name))if name else ""
			if b:a.insert(0,b[0].upper()+b[1:])
			n=gm(name)
			if n:a.append("Note: "+n)
			return "\n".join(a)
		def cV(name):f[l(name)]=a5[l(name)]=name;ai["foe_ver"]+=1;aI()
		def gn(key):a5[key]=None;ai["foe_ver"]+=1;aI();return f.pop(key)
		def go(serial=None,name=None):
			if name:
				k=l(str(name))
				if k and k in f:return True
			if serial is None:return False
			try:s=int(serial)
			except Exception:return False
			k=bu.get(s)
			if k is not None and k in f:return True
			if not name:
				try:m=API.FindMobile(s);k=l(str(m.Name or ""))if m is not None else ""
				except Exception:k=""
				return bool(k)and k in f
			return False
		bH=[0];bI=[None,None];gp=re.compile(r"^\s*\[[^\]]+\]\s*$")
		def ea(c=None):
			if len(u)<=(cE if c is None else c):return
			b=len(u)-fd;d=[]
			for a,e in list(u.items()):
				if b<=0:break
				if a in z or l(e)in f:d.append(a);continue
				del u[a];b-=1
			for a in d:
				if b<=0:break
				del u[a];b-=1
			bH[0]+=1;C.clear();ai["dirty_save"]=True
		eb=[0.];aL={"learn":None,"attack":None,"killer":None}
		def gq():
			e=time.time()
			if e<eb[0]:return
			eb[0]=e+1.;d=aL["learn"]
			if d is None:d=aL["learn"]=O()
			for f in d.new():
				b=f.name.strip();a=f.text.strip()
				if not b and ": "in a:b,a=[g.strip()for g in a.split(": ",1)]
				if not b or not a:continue
				c=b.lower()
				if gp.match(a):
					if c not in u:
						if len(u)>=cE:ea(cE-1)
						u[c]=b;bH[0]+=1;ai["dirty_save"]=True;C.clear()
				elif a.lower().startswith(c+" the "):E(Q);Q.add(c)
		def cW(serial,name,noto,party):
			a=l(name)
			if a and a in f:return "foe","L"
			if serial in party:return "friend","P"
			if K(serial):return "friend","F"
			if noto=="ally":return "friend","G"
			if noto=="murderer":return "foe",""
			if noto=="enemy":return "foe","W"
			return "neutral",""
		def gr(mob,party):
			try:
				b=mob.Serial;c=ad(mob,b)
				if c is None:return
				d,e,a=c
				if a and a.lower()in z:return
				return cW(b,a,d,party)+(d,e)
			except Exception:return
		def cX():return M(max(P["range"],c7))
		def gs(e):return e["name"].lower()
		def gt(e):return e["dist"],e["name"].lower()
		def gu(e):return(e["hits"]/float(e["hmax"])if e["hmax"]>0 else 2.),e["name"].lower()
		gv=(gs,gt,gu);cg={};cY=[None]
		def gw(serial):
			if cY[0]is None or not HOST.in_hop or HOST.pass_id!=cY[0]:return
			return cg.get(serial)
		def gx():
			k={W:[]for W in aE};cg.clear();cY[0]=HOST.pass_id if HOST.in_hop else None;c=time.time();an(c);e=B();aA["me"]=e
			if e is None:return k
			J=P["range"];K=cX();y=set(API.GetPartyMemberSerials()or[]);ai["party"]=D["party"]=y;D["scan_at"]=c;gq();L=e.Serial;A,C=int(e.X),int(e.Y);M=(P["alert_red"]or P["alert_foes"]or P["alert_orange"]or P["alert_gray"]);f=g=h=i=None;N=P["sightings"];O=ak["windows"]or{};F={};Q=P["sort"]==2
			for j in aE:G=O.get(j);F[j]=Q or G is None or not(G.minimized and ac[j][5])
			for m in K:
				try:
					if m is None:continue
					a=m.Serial
					if a==L:continue
					n,o=int(m.X),int(m.Y);p=max(abs(n-A),abs(o-C))
					if p>J:continue
					H=ad(m,a)
					if H is None:continue
					d,s,b=H
					if b and b.lower()in z:continue
					q,r=cW(a,b,d,y)
					if q!="friend"and b:
						if r=="L":
							t=l(b)
							if bu.get(a)!=t:E(bu);bu[a]=t
							if i is None:i=[]
							i.append((t,n,o))
						if N:
							I=bb.get(a)
							if I is None or c-I>cx:
								if h is None:h=[]
								h.append((a,b,d,n,o))
							bb[a]=c
						if M and not s and gy(r,d)is not None:
							if f is None:f=set()
							f.add(a)
							if a not in bX:
								if g is None:g=[]
								g.append((a,b,d,r,p,n-A,o-C))
					if F[q]:
						u,v=m.Hits or 0,m.HitsMax or 0;w,x=bool(m.IsPoisoned),bool(m.IsParalyzed)
						if len(cg)<ab:cg[a]=(b,d,q,s,w,x,u,v,p)
					else:u=v=0;w=x=False
					k[q].append({"serial":a,"name":b or "(unknown)","tag":r,"noto":d,"hits":u,"hmax":v,"dist":p,"poisoned":w,"paralyzed":x,"dead":s,"mob":m.raw})
				except Exception:continue
			R=gv[P["sort"]]
			for j in aE:k[j].sort(key=R)
			bX.clear()
			if f is not None:bX.update(f)
			try:
				if i:gC(i,c)
				if g:gz(g,c)
				if h:gB(h,c)
			except Exception as S:bd(S)
			return k
		def gy(tag,noto):
			if tag=="L"and P["alert_foes"]:return "foe"
			if noto=="murderer"and P["alert_red"]:return "red"
			if noto=="enemy"and P["alert_orange"]:return "orange"
			if(noto=="gray"or noto=="criminal")and P["alert_gray"]:return "gray"
			return
		def gz(fresh,now):
			c=P["alert_minutes"]*60.
			for a,b,d,e,f,g,h in fresh:
				t=bt.get(a)
				if t is not None and now-t<c:continue
				bt[a]=now;T(c8,gA(b,d,e,f,g,h),level="warn",who=a,name=b)
		def gA(name,noto,tag,dist,dx,dy):a=cU(l(name))if tag=="L"else "";b="%s (%s)"%(name,a)if a else name;c=d5(noto)+(", on your Foe list"if tag=="L"else "");return "%s: %s, %s"%(b,c,Kit.where_text(dx,dy,"right here"))
		def ec():return int(API.GetMap())
		def ed():return safe(HOST.guarded)
		def cZ(key,serial,again,now=None):return not V(serial,key,aD,True,again,now=now)
		def gB(a,now):
			b,c=ec(),ed()
			for d,e,f,x,y in a:gi(now,d,e,f,b,x,y,c)
		ee=[-10.,-1,None]
		def gC(here,now):
			b=c=None
			for k,x,y in here:
				d=ax.get(k)
				if b is None:
					a=ee;f=ec()
					if f!=a[1]or not 0.<=now-a[0]<1.:a[0],a[1],a[2]=now,f,ed()
					b,c=a[1],a[2]
				ax[k]=(now,b,x,y,c)
				if d is None or now-d[0]>cx:
					ap["seen_ver"]+=1
					if not ap["dirty"]:ap["dirty"]=True;ap["save_at"]=now+c9
		aA={"dead":None,"prune_at":0.,"me":None,"att_at":0.,"died_at":0.}
		def gD(now):
			if now>=aA["prune_at"]:aA["prune_at"]=now+10.;gH(now)
			c=aA["me"];a=j(c,"IsDead")if c is not None else aA["dead"];b,aA["dead"]=aA["dead"],a
			if P["killer"]and(now>=aA["att_at"]or(a and b is False)):aA["att_at"]=now+1.;gE(now)
			if b is None or a is None or a==b:return
			if a:gG(now)
			else:a8.end()
		def gE(now):
			f=aL["killer"]
			if f is None:aL["killer"]=O();return
			g,c=[],set()
			for b in f.new():
				if b.text.startswith(eN)or "is attacking you"not in b.low:continue
				h=er.search(b.text);a=h.group(1).strip().strip("*").strip()if h is not None else ""
				if a:g.append((b,a));c.add(a.lower())
			i=ef(c)if c else None
			for b,a in g:
				k,l=eg(a,i)
				if l is not False:eh(a,b.at,k)
			for s,e in aJ.items():
				m=cj.get(s)
				if m is None:continue
				d=e.get("player")
				if d is None:d=e["player"]=not j(m,"IsRenamable")and(j(m,"IsHuman")or j(m,"IsGargoyle"))
				if d:
					try:a=str(m.Name or "")
					except Exception:a=""
					if a:eh(a,e["last"],s)
		def ef(c):
			a={}
			for m in cX():
				try:
					n=m.Name
					if not n:continue
					b=n.strip().lower()
					if b not in c or b in a:continue
					if j(m,"IsRenamable"):a[b]=(m.Serial,False)
					else:a[b]=(m.Serial,j(m,"IsHuman")or j(m,"IsGargoyle"))
					if len(a)>=len(c):break
				except Exception:continue
			return a
		def eg(name,b=None):
			a=name.lower()
			if b is None:b=ef((a,))
			c=b.get(a)
			if c is not None:return c
			if a.startswith("a ")or a.startswith("an "):return None,False
			return None,None
		def eh(name,t,serial):
			if t<=aA["died_at"]:return False
			if serial is not None and(serial in ai["party"]or K(serial)):return False
			c=name.lower();a=ay.get(c)
			if a is None:
				if len(ay)>=e8:
					b=None
					for k,v in ay.items():
						if b is None or v[1]<ay[b][1]:b=k
					ay.pop(b,None)
				ay[c]=[name,t,serial];return True
			if t>a[1]:a[1]=t
			if serial is not None:a[2]=serial
			return False
		def gF(a):return-a[1]
		def gG(now):
			aA["died_at"]=now
			if not P["killer"]:ay.clear();return
			b=now-cy;a=sorted([c for c in ay.values()if c[1]>=b],key=gF);ay.clear()
			if a:a8.open(a[:e7],now,len(a))
		def gH(now):
			a=now-cx
			for s in[b for b,c in bb.items()if c<a]:del bb[s]
			if bt:
				a=now-P["alert_minutes"]*60.
				for s in[d for d,e in bt.items()if e<a]:del bt[s]
			if ay:
				a=now-cy
				for k in[g for g,h in ay.items()if h[1]<a]:del ay[k]
		def ei(serial,name,a=None):
			def b(*e):
				b=time.time();d=aT.get(serial,0);E(aT);aT[serial]=b
				if aN():aT[serial]=0;bi(serial);return
				if dR():
					aT[serial]=0
					if V(serial,"ultima.aim",aD):API.Target(serial)
					return
				if a is not None and dL():c0(serial,name,a);aT[serial]=0;return
				c=b-d<=eQ
				if c:aT[serial]=0
				API.SetLastTarget(serial=serial)
				if c:
					if cZ("ultima.attack",serial,"double-click again to attack"):return
					API.Attack(serial);API.HeadMsg("* attacking *",serial,34)
				else:API.HeadMsg("* last target *",serial,53)
			return b
		def ch(cat,poisoned,dead,paralyzed=False):
			if dead:return cF
			if cat in("friend","combat"):
				if poisoned and paralyzed:return dp
				if paralyzed:return bV
			if poisoned:return bU
			return bq[cat]
		def ej(dead,hits,hmax):return not dead and hmax>0 and hits*100./hmax<=fk
		def ek():a=dj+(fm-dj)*(.5+.5*math.sin(2*math.pi*time.time()/fl));return int(a*dk+.5)/float(dk)
		ci={}
		def c_(b,low,a=None):
			if b is None:return
			if not low:a=0.
			elif a is None:a=ek()
			k=id(b)
			if ci.get(k)==a:return
			if len(ci)>400:ci.clear()
			ci[k]=a;aV(b,a)
		def el(dead,hits,hmax,poisoned,paralyzed,dist):
			if dead:return "DEAD  %dy"%dist,0,1
			if hmax>0:a=Kit.hp_mark(poisoned,paralyzed);b=" "+a if a else(" PSN"if poisoned else "")+(" PAR"if paralyzed else "");return "%d%%%s  %dy"%(int(round(100.*hits/hmax)),b,dist),hits,hmax
			return "--  %dy"%dist,0,1
		gI={bq["friend"]:("#3A86BF","#13283A"),bq["neutral"]:("#7E868F","#26292C"),bq["foe"]:("#B23C3C","#3A1616"),bq["combat"]:("#B23C3C","#3A1616"),bU:("#4A9A55","#16301A"),bV:("#5A7FCC","#1A2640"),dp:("#2E9A90","#0F302D"),cF:("#4C4C4C","#1C1C1C")};gJ=.85;gK=.9;gL=.95;gM=.16;gN=.3
		def em(color):return gI.get(color,(color,"#202020"))
		class HealthBar(object):
			def __init__(self,parent,x,y,w,h,color,cur=0,mx=1):
				self.fw=None;self.parts=[];self.color=color;c,d=em(color);a=1 if h>=5 and w>=8 else 0;self.ix,self.iy=x+a,y+a;self.iw,self.ih=max(1,w-2*a),max(1,h-2*a)
				if a:self._add(parent,gJ,"#000000",x,y,w,h)
				self.track=self._add(parent,gK,d,self.ix,self.iy,self.iw,self.ih);self.fill=self._add(parent,gL,c,self.ix,self.iy,0,self.ih);self.sheen=self.shade=None
				if self.ih>=6:self.sheen=self._add(parent,gM,"#FFFFFF",self.ix,self.iy,0,max(1,self.ih*2//5));b=max(1,self.ih//5);self.shade=self._add(parent,gN,"#000000",self.ix,self.iy+self.ih-b,0,b)
				self.SetProgress(cur,mx)
			def _add(self,parent,alpha,color,x,y,w,h):b=a2(alpha,color);b.SetRect(x,y,w,h);parent.Add(b);self.parts.append(b);return b
			def SetProgress(self,cur,mx):
				a=int(round(self.iw*aP(float(cur)/mx,0.,1.)))if mx>0 else 0
				if a==self.fw:return
				self.fw=a
				for b in(self.fill,self.sheen,self.shade):
					if b is not None:b.SetWidth(a)
			def set_color(self,color):
				if color==self.color:return
				a,b=em(color)
				for c,d in((self.fill,a),(self.track,b)):r,g,e=fM(d);c.SetBaseColor(r,g,e,255)
				self.color=color
			def set_visible(self,on):
				for c in self.parts:Kit.set(c,"IsVisible",on)
			def Dispose(self):
				for c in self.parts:aM(c)
				self.parts=[]
		class PopBar(object):
			def __init__(self,serial,name,x,y):self.serial,self.name,self.x,self.y=serial,name,x,y;self.gump=None;self.locked=self.minimized=self.opacity_open=False;self.opacity,self.name_color=P["opacity"],bS;self.shown=o(name,serial);self.create()
			def create(self):
				s=P["scale"]/100.;w=sc(eS);self.row_h=max(10,sc(16));self.pad=max(2,sc(5));h=2*am+dN(s)
				if self.opacity_open:h+=dO(s)
				if not self.minimized:h+=self.row_h+2*self.pad
				self.size=(w,h);self.x,self.y=Kit.clamp(self.x,self.y,w,h);g=G.CreateModernGump(self.x,self.y,w,h,False,w,h);self.gump=g;g.SetAlpha(0.);self.chrome=Chrome(g);self.bar=self.info=self.hit=self.glow=None;self.low,self.spell_ctrls,self.bar_key,self.last=False,[],None,None;self.layout_chrome();Kit.add_front(g);Kit.on_moved(g,self.moved);at.placed(self.anchor_key);Kit.set(g,"CanMove",not self.locked)
			@property
			def anchor_key(self):return "pop:%d"%self.serial
			def moved(self):at.pending=True
			def layout_chrome(self):
				w,h=self.size;a,b=self.minimized,self.opacity_open;c=[("lock",self.locked,self.toggle_lock,"Unlock (move and resize again)"if self.locked else "Lock in place (no moving or resizing)"),("min",a,self.toggle_minimize,"Restore"if a else Kit.MIN_TIP)]
				if not a:c.append(("opacity",b,self.toggle_opacity,"Hide the opacity slider"if b else "Show the opacity slider (frame and bars stay solid)"))
				c.append(("close",False,self.close,"Close this bar"));self.chrome.layout(w,h,P["scale"]/100.,self.opacity,self.shown,self.name_color,c,b and not a,self.toggle_minimize,lambda:bi(self.serial),self.anchor_key)
			def destroy(self):g,self.gump=self.gump,None;Kit.dispose(g)
			def close(self,*a):au.pop(self.serial,None);self.destroy()
			def snapshot(self):
				if Kit.is_open(self.gump):self.x,self.y=self.gump.GetX(),self.gump.GetY()
			def rebuild(self):self.snapshot();self.destroy();self.create()
			def set_locked(self,locked):
				self.locked=locked
				if self.gump is not None:Kit.set(self.gump,"CanMove",not locked);self.layout_chrome()
			def toggle_lock(self,*a):self.set_locked(not self.locked)
			def toggle_minimize(self,*a):self.minimized=not self.minimized;self.opacity_open=False;self.rebuild()
			def toggle_opacity(self,*a):self.opacity_open=not self.opacity_open;self.rebuild()
			def apply_opacity(self,v):
				self.opacity=v
				if self.gump is not None:self.chrome.set_opacity(v)
			def update(self):
				if not Kit.is_open(self.gump):au.pop(self.serial,None);return
				try:
					v=self.chrome.poll()
					if v is not None:self.opacity=v
					self._refresh()
				except Exception as a:aj("closed the health bar for %s (%s)."%(self.name,a),Kit.HUE_BAD);self.close()
			def _draw_row(self,key):
				f,h,c=key
				if self.bar is not None:self.bar.Dispose()
				for g in[self.info,self.hit,self.glow]+self.spell_ctrls:aM(g)
				self.spell_ctrls=[];w=self.size[0];s=P["scale"]/100.;y=self.chrome.content_top+self.pad;a=w-2*am-2*self.pad;x=am+self.pad
				if c and b7():d=self.row_h;a-=b7()*(d+2);dM(self.gump,x+a+2,y,d,self.row_h,self.serial,self.name,self.spell_ctrls)
				self.glow=None
				if c:b=max(2,self.pad-1);self.glow=a2(0.,di);self.glow.SetRect(x-b,y-b,a+2*b,self.row_h+2*b);self.gump.Add(self.glow)
				self.bar=HealthBar(self.gump,x,y,a,self.row_h,f);e=max(8,int(round(12*bY(s))));self.info=bx("",e,"#FFFFFF",aligned="right",maxWidth=a-6,applyStroke=True);self.info.SetPos(x+3,bg(y,self.row_h,e));self.gump.Add(self.info);self.hit=aQ(x,y,a,self.row_h,ei(self.serial,self.name),aZ(c1,self.name));self.gump.Add(self.hit);self.bar_key=key;self.last=None
			def pulse(self,a=None):
				if self.gump is not None and not self.minimized:c_(self.glow,self.low,a)
			def _refresh(self):
				e=B();d=gw(self.serial)if e is not None else None
				if d is not None and d[0]:a=True
				else:d=None;a=X(self.serial)
				if a is None or e is None:b,f,g,c,h=("out of range",0,1,(cF,False,False),"#888888");self.low=False;self.shown=o(self.name,self.serial)
				else:
					if d is not None:m,i,k,l,n,p,q,r,s=d
					else:
						try:m=a.Name or self.name
						except Exception:m=self.name
						i=Kit.noto_name(a);k,u=cW(self.serial,m,i,ai["party"]);l,n=j(a,"IsDead"),j(a,"IsPoisoned");p,q,r=j(a,"IsParalyzed"),R(a,"Hits"),R(a,"HitsMax")
						try:s=max(abs(int(a.X)-int(e.X)),abs(int(a.Y)-int(e.Y)))
						except Exception:s=0
					c=(ch(k,n,l,p),(P["magery"],P["healing"]),k=="friend");self.low=k=="friend"and ej(l,q,r);h=b1(i,"#DDDDDD");self.shown=H(self.name,self.serial,i);b,f,g=el(l,q,r,n,p,s)
				if Follow.serial==self.serial:b="FOL "+b
				self.name_color=h
				if self.minimized:self.chrome.set_title("%s  %s"%(self.shown,b.split("  ")[0]),h);return
				self.chrome.set_title(self.shown,h)
				if c!=self.bar_key:
					t=self.bar_key
					if t is not None and t[1:]==c[1:]and self.bar is not None:self.bar.set_color(c[0]);self.bar_key=c
					else:self._draw_row(c)
				if self.last!=(b,f,g):self.last=(b,f,g);aR(self.info,b);self.bar.SetProgress(float(f),float(g))
		def gO(serial,name):
			def a(*b):
				if not name or name=="(unknown)":aj("no name yet; try again in a moment.",Kit.HUE_BAD);return
				z[name.lower()]=name;aI();a=au.get(serial)
				if a is not None:a.close()
				aj("%s marked as an NPC and hidden; Unignore the name to undo."%name,Kit.HUE_GOOD)
			return bA(serial,a)
		def gP(serial,name,a):return bA(serial,lambda:c0(serial,name,a))
		def gQ(serial,name,a):HOST.enable("unitframes");bf.append(lambda:c0(serial,name,a,False))
		def c0(serial,name,a,d=True):
			b=HOST.services.get("unitframes.add")
			if b is None and d and "unitframes"in HOST.by_key:bz.append(lambda:gQ(serial,name,a));return
			if b is not None:b(serial);aj("%s gets a frame in Character HUD > Frames."%name,Kit.HUE_GOOD);return
			c=au.get(serial)
			if c is not None and Kit.is_open(c.gump):aj("a health bar for %s is already open."%name,Kit.HUE_BAD);return
			e=safe(lambda:a.gump.GetX(),300);f=safe(lambda:a.gump.GetY(),300);x=e+a.size[0]+6;y=f+len(au)*(sc(52)+4);g=au[serial]=PopBar(serial,name,x,y);g.update();aj("popped out a health bar for %s."%name,Kit.HUE_GOOD)
		c1=("Click: target; double-click: attack (blue or green in guards: twice). Alt+click: auto-follow (again to stop)");gR="Click: put the name in the box. Alt+click: auto-follow (again to stop)";en=("Click: show only this player (again for everyone). Alt+click: auto-follow (again to stop)")
		class PoolRow(object):
			glow=None;e=None;prev=None
			def parts(self):return self.ctrls
			def set_shown(self,on):
				for c in self.parts():Kit.set(c,"IsVisible",on)
				self.bar.set_visible(on);self.shown=on
			def hide(self):
				if self.serial is not None:self.prev=(self.serial,self.name,time.time())
				self.serial,self.name=None,"";self.low=False;self.last=None
				if self.glow is not None:c_(self.glow,False)
				self.set_shown(False)
		class TrackerRow(PoolRow):
			def __init__(self,view,i,geo,e):
				self.win=view;self.serial,self.name=e["serial"],e["name"];self.y=y=i*geo["row_h"];self.shown,self.low,self.ctrls=True,False,[];self.last=self.raw=self.name_raw=None;a,b=view.sa,geo["rw"];c=G.CreateGumpColorBox(.35,"#000000");c.SetRect(0,y,b,geo["row_h"]-2);dE(c,RowClick(self,lambda s,n:ei(s,n,view)));Kit.with_tip(c,aZ(c1,self.name));self.bg=c;self.glow=None
				if view.cat=="friend":self.glow=a2(0.,di);self.glow.SetRect(0,y,b,geo["row_h"]-2)
				h,j=eo(e,geo);self.name_lbl=aH(h,geo["name_fs"],j);az(self.name_lbl,4,y+geo["name_dy"]);self.name_key=(h,j);d,f=geo["pbw"],geo["nbw"];self.info=aH("",geo["info_fs"],"#DDDDDD",aligned="right",maxWidth=b-16-d-f);az(self.info,4,y+geo["info_dy"])
				for g in(c,self.glow,self.name_lbl,self.info):
					if g is not None:a.Add(g);self.ctrls.append(g)
				a3(a,b-8-d-f,y+geo["npc_dy"],f,f,"N",RowClick(self,gO),"Mark as an NPC and hide (Unignore the name to undo). "+aW,font=geo["npc_fs"],store=self.ctrls);a3(a,b-4-d,y+geo["pop_dy"],d,geo["pop_h"],">",RowClick(self,lambda s,n:gP(s,n,view)),"Pop out a health bar (or Shift+click the row). "+aW,font=geo["pop_fs"],store=self.ctrls);self.tips=[]
				if geo["fbtn"]:self.tips=dM(a,4+geo["bar_w"]+2,y+geo["fbtn_dy"],geo["sb"],geo["sb"],self.serial,self.name,store=self.ctrls,row=self)
				self.bar=HealthBar(a,4,y+geo["bar_dy"],geo["bar_w"],geo["bar_h"],ep(view.cat,e))
			def assign(self,e,geo):
				a,b=e["serial"],e["name"]
				if a!=self.serial or b!=self.name:
					if a!=self.serial:self.prev=(self.serial,self.name,time.time())
					self.serial,self.name=a,b;self.last=None
					for g,h in self.tips:Kit.with_tip(g,h%o(b,a))
					Kit.with_tip(self.bg,aZ(c1,b))
				if not self.shown:self.set_shown(True)
				c=(e["name"],e["tag"],e["noto"],geo["name_px"],geo["name_fs"])
				if c!=self.name_raw:
					d,f=eo(e,geo)
					if(d,f)!=self.name_key:self.set_name(d,f,geo)
					self.name_raw=c
				self.bar.set_color(ep(self.win.cat,e))
			def set_name(self,text,color,geo):
				a=self.name_lbl
				if color==self.name_key[1]or dK(a,color):aR(a,text)
				else:b=self.ctrls.index(a);aM(a);a=aH(text,geo["name_fs"],color);az(a,4,self.y+geo["name_dy"]);self.win.sa.Add(a);self.ctrls[b]=a;self.name_lbl=a
				self.name_key=(text,color)
			def values(self,e):
				self.e=e;d=Follow.serial==e["serial"];f=(e["dead"],e["hits"],e["hmax"],e["poisoned"],e["paralyzed"],e["dist"],d)
				if self.last is not None and f==self.raw:return
				self.raw=f;a,b,c=el(e["dead"],e["hits"],e["hmax"],e["poisoned"],e["paralyzed"],e["dist"])
				if d:a="FOL "+a
				self.low=ej(e["dead"],e["hits"],e["hmax"])
				if self.last!=(a,b,c):self.last=(a,b,c);aR(self.info,a);self.bar.SetProgress(float(b),float(c))
			def forget(self):
				for c in self.ctrls:aG.pop(id(c),None)
				self.ctrls=[];self.serial=None
		def eo(e,geo):
			a=b6(H(e["name"],e["serial"],e["noto"]),geo["name_px"],geo["name_fs"])
			if e["tag"]:a+="  ["+e["tag"]+"]"
			return a,b1(e["noto"],"#DDDDDD")
		def ep(cat,e):return ch(cat,e["poisoned"],e["dead"],e["paralyzed"])
		class PoolWin(object):
			def show_empty(self,on):
				if on and self.empty is None:self.empty=self.make_empty();self.empty_shown=True
				elif self.empty is not None and on!=self.empty_shown:
					for a in self.empty:Kit.set(a,"IsVisible",on)
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
			def destroy(self):g,self.gump=self.gump,None;Kit.dispose(g)
			def moved(self):at.pending=True;self.snapshot();aI()
			@property
			def dock_key(self):return "ultima."+self.cat
			def user_minimize(self,*a):A(self.dock_key);self.toggle_minimize()
			def apply_opacity(self,v):
				ac[self.cat][6]=v
				if Kit.is_open(self.gump)and self.chrome is not None:self.chrome.set_opacity(v)
		class CategoryGump(PoolWin):
			Row=TrackerRow
			def __init__(self,cat):self.cat,self.rows=cat,[];self.gump=self.chrome=self.sa=self.made_min=None;self.locked=self.minimized=self.docked=False;self.create()
			def create(self):
				x,y,w,h,i,e,k=ac[self.cat];self.minimized=e;b,c=sc(cq),sc(cr);a=al["size"].get(self.cat);j=p(self.dock_key)
				if a is not None:
					b=min(b,a[0]);c=min(c,a[1]);w=a[0]
					if not e:h=a[1]
				w=max(w,b)
				if e:d=dz;f,g=d,False
				else:d=max(h,c);f,g=c,a is None
				self.made_min=(b,c);self.resized_flag=self.user_resize_pending=False;self.sync_target,self.user_resize_ticks=None,0
				if not j:x,y=Kit.clamp(x,y,w,d);ac[self.cat][0],ac[self.cat][1]=x,y
				self.gump=G.CreateModernGump(x,y,w,d,g,b,f,self._on_resized);self.gump.SetAlpha(0.);self.chrome=Chrome(self.gump,kit=True,key=self.dock_key);self._forget_body();self.size=(w,d);self.count_n=0;self.locked=i;self.layout_chrome();Kit.add_front(self.gump,bool(self.docked and e));Kit.on_moved(self.gump,self.moved);at.placed(self.cat);self._apply_lock()
			def layout_fit(self,w,h,mode):
				a=self.cat
				if w is None or h is None:
					if a in al["size"]:al["size"][a]=None
					al["force"].discard(a)
				else:
					al["size"][a]=(int(w),int(h))
					if mode=="again":al["force"].add(a)
				al["req"]=True
			def _forget_body(self):
				for r in self.rows:r.forget()
				self.rows=[];self.sa=self.empty=self.geo=self.body_key=None
			def layout_chrome(self):w,h=self.size;c=self.cat;self.chrome.layout_kit(w,h,ac[c][6],dg[c],dh[c],self.minimized,self.user_minimize,lambda*a:bs.append(self.dock_key));self.chrome.set_status(str(max(0,self.count_n)))
			def zone_chrome(self):
				if Kit.is_open(self.gump)and self.chrome is not None:self.layout_chrome()
			def _on_resized(self,*a):self.resized_flag=True
			def set_count(self,n):
				if n==self.count_n:return
				self.count_n=n;self.chrome.set_status(str(max(0,n)))
			def _apply_lock(self):
				a=self.locked;b=al["size"].get(self.cat)is not None;c=p(self.dock_key)
				if not c:Kit.set(self.gump,"CanMove",not a)
				self.gump.SetResizable(not a and not self.minimized and not b);ac[self.cat][4]=a;ai["dirty_save"]=True
			def set_locked(self,locked):self.locked=locked;self._apply_lock()
			def toggle_minimize(self,*a):
				self.snapshot();ac[self.cat][5]=not self.minimized
				if not ac[self.cat][5]:self.docked=False
				self.destroy();self.create();ai["dirty_save"]=True
			def geometry(self):
				w,h=self.size;a=Kit.MARGIN+4;c=max(40,w-2*a);b=max(60,c-c5);e=bZ(13);g={"sa":(a,self.chrome.content_top+sc(4),c,max(20,h-self.chrome.content_top-sc(4)-a)),"rw":b,"row_h":sc(Kit.pitch(eR)),"name_fs":e,"info_fs":bZ(12),"name_px":max(30,int(b/1.2)),"name_dy":sc(1),"info_dy":sc(2),"pbw":sc(eT),"nbw":sc(eU),"npc_dy":sc(3),"npc_fs":bZ(10),"pop_dy":sc(1),"pop_h":sc(16),"pop_fs":bZ(12),"fbtn":self.cat=="friend"and b7()>0,"sb":sc(13),"fbtn_dy":sc(16)};d=b-8
				if g["fbtn"]:d-=b7()*(g["sb"]+2)
				g["bar_w"],g["bar_dy"],g["bar_h"]=d,sc(18),max(3,sc(10));return g
			def build_body(self):Kit.dispose(self.sa);self._forget_body();self.geo=a=self.geometry();x,y,w,h=a["sa"];self.sa=G.CreateGumpScrollArea(x,y,w,h);self.gump.Add(self.sa)
			def make_empty(self):a=dA("No players in range.",self.geo["rw"]-8);return dB(self.sa,a,4,4)
			def update(self,entries):
				if not Kit.is_open(self.gump):self.create()
				if not self.minimized:
					w,h=int(self.gump.GetWidth()),int(self.gump.GetHeight())
					if(w<=0 or h<=0)and self.size:w,h=self.size
					if(w,h)!=self.size or self.resized_flag:
						self.resized_flag=False;self.size=(w,h);at.placed(self.cat,self.gump.GetX(),self.gump.GetY(),w,h);self.layout_chrome();self.body_key=None
						if self.sync_target==(w,h)or al["size"].get(self.cat)is not None:self.sync_target=None
						else:self.user_resize_pending=True;self.user_resize_ticks=0
					elif self.user_resize_pending:self.user_resize_ticks+=1
					a=al["size"].get(self.cat)
					if a is not None and(w,h)!=a:al["req"]=True
				self.set_count(len(entries))
				if self.minimized:return
				b=(self.size,self.chrome.content_top,P["scale"],P["magery"],P["healing"])
				if b!=self.body_key:self.build_body();self.body_key=b
				self.fill(entries)
			def pulse(self,a=None):
				if self.cat!="friend"or self.minimized:return
				for b in self.rows:
					if b.shown:c_(b.glow,b.low,a)
			def resize_to(self,w,h):
				if not self.minimized:
					if self.size==(w,h):return
					self.sync_target=(w,h);self.gump.SetWidth(w);self.gump.SetHeight(h)
					if(self.gump.GetWidth(),self.gump.GetHeight())==(w,h):return
				self.snapshot();ac[self.cat][2],ac[self.cat][3]=w,h;self.destroy();self.create()
			def snapshot(self):
				if not Kit.is_open(self.gump):return
				L=ac[self.cat];L[0],L[1],L[2]=self.gump.GetX(),self.gump.GetY(),self.size[0]
				if not self.minimized:L[3]=self.size[1]
		def c2(windows):
			for w in windows.values():w.destroy()
			for w in windows.values():w.create()
			for p in list(au.values()):p.rebuild()
		def gS():
			if ak["windows"]is not None:
				for w in ak["windows"].values():w.snapshot()
				c2(ak["windows"])
			if ak["combat"]is not None:ak["combat"].relayout=True
			if ak["panel"]is not None:ak["panel"].rebuild_foe_list()
			a0.ask_redraw();a8.ask_redraw()
		def eq(windows,source):
			if source.minimized:w,h=ac[source.cat][2],ac[source.cat][3]
			else:w,h=source.size
			for t in windows.values():
				if t is source or t.locked or al["size"].get(t.cat)is not None:continue
				t.resize_to(w,h)
			ai["dirty_save"]=True
		def gT(windows):
			for w in windows.values():
				if not P["sync"]:w.user_resize_pending=False
				elif w.user_resize_pending and w.user_resize_ticks>=2:
					if b4():return
					w.user_resize_pending=False;eq(windows,w);return
		def gU(a,windows):
			b=P["scale"]
			if a==b:return
			c=float(a)/b
			for w in windows.values():w.snapshot();L=ac[w.cat];L[2]=max(sc(cq,a),int(round(L[2]*c)));L[3]=max(sc(cr,a),int(round(L[3]*c)))
			P["scale"]=a;c2(windows);ai["dirty_save"]=True
		def gV(windows):
			if not al["req"]:return
			al["req"]=False;e=b4()
			for a,i in list(al["size"].items()):
				b=windows.get(a)
				if b is None or b.gump is None:continue
				if i is None:
					if e:al["req"]=True;continue
					al["size"].pop(a,None);c=al["own_size"].pop(a,None)
					if b.made_min is not None and b.made_min!=(sc(cq),sc(cr)):
						b.snapshot()
						if c is not None:ac[a][2],ac[a][3]=c
						b.destroy();b.create()
					elif c is not None and c!=(ac[a][2],ac[a][3]):b.resize_to(c[0],c[1])
					al["made"].pop(a,None)
					if b.gump is not None:b._apply_lock()
					continue
				if a not in al["own_size"]:al["own_size"][a]=(ac[a][2],ac[a][3])
				w,h=i;j=a in al["force"]
				if b.minimized:
					if ac[a][2]!=w or(b.size and b.size[0]!=w):
						if e:al["req"]=True;continue
						b.resize_to(w,ac[a][3])
					al["force"].discard(a);continue
				d=(int(b.gump.GetWidth()),int(b.gump.GetHeight()))
				if d[0]<=0 or d[1]<=0:al["force"].discard(a);continue
				f=al["made"].get(a);g=f[1]if f is not None and f[0]==(w,h)else 0
				if d==(w,h)and b.size==(w,h):g=0;al["made"].pop(a,None)
				if(j or b.size!=(w,h)or d!=(w,h)or b.made_min[0]>w or b.made_min[1]>h)and(j or g<fH):
					if e:al["req"]=True;continue
					al["force"].discard(a);al["made"][a]=((w,h),g+1);b.snapshot();ac[a][2],ac[a][3]=w,h;b.destroy();b.create()
				else:al["force"].discard(a)
		er=Journal.ATTACK_RE;es=[int(hu)for hu in e2];aJ={};et=[0];bm=[];cj={};a7=[];aB={"serial":None,"until":0.,"harmful":True,"stale":False}
		def eu(m):
			try:return m is not None and not m.IsDead
			except Exception:return False
		def c3(m):
			try:return int(m.Distance)
			except Exception:return 0
		def c4(m,attacked_me=False):
			if j(m,"IsRenamable"):return False
			a=Kit.noto_name(m);return a not in e0 and(attacked_me or a not in e1)
		def bn(serial,t=None):
			e=aJ.get(serial)
			if not e:
				a=B()
				if a is None or serial==a.Serial:return
			if serial in ai["party"]or K(serial):return
			t=t or time.time()
			if e:e["last"]=t
			elif len(aJ)<eZ:et[0]+=1;aJ[serial]={"last":t,"hits":None,"order":et[0]}
		gW=5.
		def gX():
			d=aL["attack"]
			if d is None:aL["attack"]=O();return
			g,b=time.time()-gW,set()
			for c in d.new():
				if c.at>=g and "is attacking you"in c.low:
					m=er.search(c.text)
					if m:b.add(m.group(1).strip().lower())
			if not b:return
			e={}
			for m in cX():
				try:
					n=m.Name
					if n:
						f=n.strip().lower()
						if f in b and c4(m,attacked_me=True):e.setdefault(f,[]).append(m)
				except Exception:pass
			for a in e.values():
				if len(a)==1:bn(a[0].Serial);continue
				h=[i for i in a if c4(i)or j(i,"InWarMode")]or[min(a,key=c3)]
				for m in h:bn(m.Serial)
		ev=.5;ew={"serial":None,"until":0.}
		def gY():
			s=API.LastTargetSerial;b=B()
			if not s or b is None or s==b.Serial or s in aJ:return
			if P["combat_only"]and not b.InWarMode:return
			c=time.time();a=ew
			if a["serial"]==s and 0.<=a["until"]-c<=ev:return
			m=API.FindMobile(s)
			if eu(m)and c3(m)<=cu and c4(m):a["serial"]=None;bn(s)
			else:a["serial"],a["until"]=s,c+ev
		def gZ():
			a=e_ if P["combat_only"]else cu
			for m in M(a):
				try:
					if int(m.Notoriety)in es and m.InWarMode and not m.IsDead and not j(m,"IsRenamable"):bn(m.Serial)
				except Exception:pass
		def ex():
			t=time.time();cj.clear();a=[]
			for s in list(aJ.keys()):
				e=aJ[s];m=API.FindMobile(s)
				if not eu(m):del aJ[s];continue
				d=c3(m)
				if d>c7:del aJ[s];continue
				try:h=m.Hits
				except Exception:del aJ[s];continue
				if e["hits"]is not None and h<e["hits"]:e["last"]=t
				e["hits"]=h;n=None
				try:
					if d<=cu and m.InWarMode:
						n=m.Notoriety
						if int(n)in es:e["last"]=t
				except Exception:pass
				if t-e["last"]>eY:del aJ[s];continue
				cj[s]=m
				try:b,c=m.Name or "???",m.HitsMax;f,g=bool(m.IsPoisoned),bool(m.IsParalyzed);a.append((e["order"],s,b,Kit.noto_name(m)if n is None else Kit.noto_of(n),h,c,f,g))
				except Exception:continue
			a.sort();return[i[1:]for i in a]
		def g_(serial):
			def a(*a):bm.append((serial,aN(),time.time()))
			return a
		def g0():
			while bm:
				s,b,a=bm.pop(0);m=API.FindMobile(s)
				if not m:continue
				if b:bi(s);continue
				if dR():
					if not V(s,"ultima.aim",aD,now=a):continue
					API.Target(s)
				else:
					if cZ("ultima.attack",s,"click the bar again to attack",a):continue
					API.Attack(s)
				bn(s)
		def g1(spell,serial):
			def a(*a):
				if aN():bm.append((serial,True,time.time()));return
				a7.append((spell,serial,True,time.time()))
			return a
		def ey(serial,spell,a):return bA(serial,lambda:a7.append((a if dL()else spell,serial,False,time.time())))
		def g2():
			if a7:
				c,s,a,d=a7[-1]
				if b9()is not None:
					if time.time()-d>ct:del a7[:];aj("target cursor busy; %s not cast."%c,Kit.HUE_BAD)
				else:
					del a7[:];m=API.FindMobile(s)
					if m and a and cZ("ultima.cast",s,"click the button again to cast",d):m=None
					if m:
						b=bool(API.HasTarget("any"))
						if b and aB["serial"]is not None and not aB["stale"]and API.HasTarget("harmful"if aB["harmful"]else "beneficial"):API.CancelTarget();b=False
						API.CastSpell(c);aB.update(serial=s,harmful=a,stale=b,until=time.time()+ct);dQ("spell",ct)
						if a:bn(s)
			if aB["serial"]is None:aX("spell");return
			if time.time()>aB["until"]:aB["serial"]=None;aX("spell");return
			if aB["stale"]:
				if not API.HasTarget("any"):aB["stale"]=False
				return
			if b9()is not None:return
			if API.HasTarget("harmful"if aB["harmful"]else "beneficial"):
				s=aB["serial"];aB["serial"]=None;aX("spell")
				if API.FindMobile(s):API.Target(s)
				else:API.CancelTarget()
		def ez(serial,hits,a,c,d):
			f="?"if not a or a<=1 else str(int(round(hits*100./a)))+"%";b="FOL "if Follow.serial==serial else "";e=Kit.hp_mark(c,d)
			if e:b+=e+" "
			else:b+=("PSN "if c else "")+("PAR "if d else "")
			return b+f
		eA="Attack or aim at %s (blue or green in guards: twice). "+aW;g3=(("Poison","P",bU,"Cast Poison on %s. Alt+click: auto-follow (again to stop)"),("Paralyze","Z",bV,"Cast Paralyze on %s. Alt+click: auto-follow (again to stop)"));a_=Kit.MARGIN+4
		class CombatSlot(PoolRow):
			def __init__(self,view,i,geo,d):
				self.win=view;g=view.gump;b,a,u,l,h,m,p=d;self.serial,self.name=b,a;self.y=c=geo["y"]+i*(geo["rh"]+bK);self.shown,self.ctrls,self.tips=True,[],[];self.bar=HealthBar(g,a_,c,geo["bar_w"],geo["rh"],ch("combat",m,False,p),l,h if h else 1);self.name_lbl=self.info=self.name_key=self.info_text=self.name_raw=self.info_raw=None;self._texts(d,geo);e=aQ(a_,c,geo["bar_w"],geo["rh"],RowClick(self,lambda s,n:g_(s)),aZ(eA%o(a,b),a));g.Add(e);self.ctrls.append(e);self.tips.append((e,eA))
				if P["magery"]:
					j=a_+geo["bar_w"]+1
					for q,r,t,k in g3:f=[];a3(g,j,c,geo["spell_w"],geo["rh"],r,RowClick(self,(lambda a:lambda s,n:g1(a,s))(q)),k%o(a,b),face=t,color="#FFFFFF",font=max(7.,geo["font"]-1),store=f);self.ctrls.extend(f);self.tips.append((f[-1],k));j+=geo["spell_w"]+1
			def _texts(self,d,geo):
				g=self.win.gump;h,i,c,m,j,n,o=d;a=geo["font"];k=bg(self.y,geo["rh"],a)
				if self.name_lbl is None:b=b6(H(i,h,c),geo["name_w"],a,True);l=b1(c,"#FFFFFF");e=bx(b,a,l,applyStroke=True);e.SetPos(a_+3,k);g.Add(e);self.name_lbl,self.name_key=e,(b,l);self.name_raw=(i,c,geo["name_w"],a)
				if self.info is None:b=ez(h,m,j if j else 1,n,o);f=bx(b,a,"#FFFFFF",aligned="right",maxWidth=geo["info_w"],applyStroke=True);f.SetPos(a_+geo["bar_w"]-geo["info_w"]-3,k);g.Add(f);self.info,self.info_text=f,b
			def assign(self,d,geo):
				b,a,e,m,n,i,j=d
				if b!=self.serial or a!=self.name:
					if b!=self.serial:self.prev=(self.serial,self.name,time.time())
					self.serial,self.name=b,a
					for k,(l,f)in enumerate(self.tips):Kit.with_tip(l,aZ(f%o(a,b),a)if k==0 else f%o(a,b))
				if not self.shown:self.set_shown(True)
				self.bar.set_color(ch("combat",i,False,j));g=geo["font"];h=(a,e,geo["name_w"],g)
				if self.name_lbl is not None and h!=self.name_raw:
					c=(b6(H(a,b,e),geo["name_w"],g,True),b1(e,"#FFFFFF"))
					if c!=self.name_key:
						if c[1]==self.name_key[1]:aR(self.name_lbl,c[0]);self.name_key=c
						else:aM(self.name_lbl);self.name_lbl=None
					self.name_raw=h
				self._texts(d,geo)
			def values(self,d):
				self.e=d;a,j,k,b,f,g,h=d;c=f if f else 1;self.bar.SetProgress(b,c);i=(a,b,c,g,h,Follow.serial==a)
				if i!=self.info_raw:
					self.info_raw=i;e=ez(a,b,c,g,h)
					if e!=self.info_text:self.info_text=e;aR(self.info,e)
			def parts(self):return[self.name_lbl,self.info]+self.ctrls
			def dispose(self):
				for c in self.parts():aM(c)
				self.bar.Dispose()
		class CombatWindow(PoolWin):
			Row=CombatSlot
			def __init__(self):self.gump=self.chrome=self.slot=None;self.relayout=self.zone_redraw=self.docked=False;self.made_min=a1;self.cat="combat";self._forget()
			def layout_fit(self,w,h,mode):
				a=(int(w),int(h))if w and h else None
				if a!=self.slot or mode=="again":self.slot=a;self.relayout=self.zone_redraw=True
			def width(self):return self.slot[0]if self.slot is not None else ac["combat"][2]
			def zone_chrome(self):self.relayout=True
			def _forget(self):self.rows,self.grip,self.empty_lines=[],[],[];self.empty=self.frame_key=self.geo=self.fit_n=None;self.empty_shown=False
			@property
			def minimized(self):return bool(ac["combat"][5])
			def is_open(self):return Kit.is_open(self.gump)
			def show(self):
				if self.is_open():return
				L=ac["combat"];L[2]=aP(L[2],a1,bJ);a=p(self.dock_key)
				if not a:L[0],L[1]=Kit.clamp(L[0],L[1],self.width(),self.height(0))
				self.made_min=min(a1,self.width());g=G.CreateModernGump(L[0],L[1],self.width(),self.height(0),True,self.made_min,16,self._on_resized);g.SetAlpha(0.);self.gump=g;self._forget();Kit.add_front(g);Kit.on_moved(g,self.moved);at.placed("combat")
				if not a:P["combat_shown"]=True;ai["dirty_save"]=True
				self.apply_lock();self.draw(ex())
			def hide(self):
				self.snapshot();Kit.dispose(self.gump);self.gump=None;self._drop_notes();P["combat_shown"]=False;ai["dirty_save"]=True
				if self.docked:self.docked=False;A(self.dock_key)
			def _drop_notes(self):
				for a in self.rows:aG.pop(id(a.name_lbl),None);aG.pop(id(a.info),None)
				self._forget()
			def snapshot(self):
				if self.is_open():L=ac["combat"];L[0],L[1]=self.gump.GetX(),self.gump.GetY()
			def reset(self):
				ac["combat"]=list(cH["combat"])
				if self.is_open():L=ac["combat"];g=self.gump;g.SetPos(L[0],L[1]);Kit.moved_by_code(g);at.placed("combat");self.apply_lock();self.relayout=True
				else:self.show()
			def metrics(self):s=aP(self.width(),a1,bJ)/float(c6);return s,max(10,int(round(eW*s))),eX*bY(s)
			def height(self,n):
				if self.slot is not None and not ac["combat"][5]:return self.slot[1]
				b,a,b=self.metrics()
				if ac["combat"][5]:return dz
				h=bW+Kit.MARGIN
				if n<=0 and self.empty_lines:return h+max(a+bK,2+cJ*len(self.empty_lines))+cs
				return h+max(n,1)*(a+bK)+cs
			def _empty_text(self,W):
				c=max(20,W-2*a_-4);a=dA("No one is fighting you.",c)
				if self.slot is not None:
					b=max(1,(self.slot[1]-Kit.MARGIN-bW-2)//cJ)
					if len(a)>b:a=a[:b-1]+[Kit.fit(" ".join(a[b-1:]),c)]
				return a
			def _on_resized(self,*a):
				if not self.is_open()or self.slot is not None:return
				w=aP(int(self.gump.GetWidth()),a1,bJ)
				if w==ac["combat"][2]:return
				ac["combat"][2]=w;self.relayout=True
			def apply_lock(self):
				if not self.is_open():return
				g,a=self.gump,ac["combat"][4];b=p(self.dock_key)
				if not b:Kit.set(g,"CanMove",not a)
				g.SetResizable(not a and not b)
			def set_locked(self,locked):
				if ac["combat"][4]!=locked:ac["combat"][4]=locked;self.apply_lock();self.relayout=True;ai["dirty_save"]=True
			def toggle_minimize(self,*a):
				ac["combat"][5]=not ac["combat"][5]
				if not ac["combat"][5]:self.docked=False
				self.relayout=True;ai["dirty_save"]=True
			def status_text(self,data):
				n=len(data)
				if not ac["combat"][5]or n==0:return "%d"%n
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
				for c in self.grip:aM(c)
				for c in self.empty or():aM(c)
				g.Clear();self._forget();L=ac["combat"];b=L[5];s,e,k=self.metrics();W=self.width();n=len(data)
				if not b:self.empty_lines=self._empty_text(W)
				H=self.height(n);g.SetWidth(W);g.SetHeight(H);self.fit_n=n;at.sized("combat",W,H);self.chrome=Chrome(g,kit=True,key="ultima.combat");self.chrome.layout_kit(W,H,L[6],"Combat",dh["combat"],b,self.user_minimize,lambda*a:bs.append("ultima.combat"));self.chrome.set_status(self.status_text(data))
				if b:return
				l=W-2*a_;f=int(round(80*s));h=max(14,e)if P["magery"]else 0;i=l-(2*(h+1)if P["magery"]else 0);self.geo={"y":self.chrome.content_top,"rh":e,"font":k,"info_w":f,"spell_w":h,"bar_w":i,"name_w":i-f-6,"W":W}
				if L[4]:return
				m,o=W-Kit.MARGIN-9,H-Kit.MARGIN-9
				for p,q in eB:d=a2(1.,fj);d.SetRect(m+p,o+q,2,2);g.Add(d);self.grip.append(d)
			def fit(self,n):
				n=max(n,0)
				if n==self.fit_n:return
				self.fit_n=n;W,H=self.geo["W"],self.height(n);self.gump.SetHeight(H);at.sized("combat",W,H);self.chrome.frame.layout(W,H);a,b=W-Kit.MARGIN-9,H-Kit.MARGIN-9
				for(c,d),e in zip(eB,self.grip):e.SetRect(a+c,b+d,2,2)
			def make_empty(self):return dB(self.gump,self.empty_lines or[""],a_+4,self.geo["y"]+2)
			def fill(self,data):
				if self.slot is not None:
					a=self.geo;c=self.slot[1]-a["y"]-Kit.MARGIN-cs;b=max(1,c//max(1,a["rh"]+bK))
					if len(data)>b:data=data[:b]
				self.fit(len(data));PoolWin.fill(self,data)
			def draw(self,data):
				L=ac["combat"];a=(L[2],L[5],L[4],P["magery"],self.slot)
				if self.zone_redraw and self.frame_key is not None and b4():
					if self.chrome is not None:self.chrome.set_status(self.status_text(data))
					if a==self.frame_key and not L[5]and self.geo is not None:self.fill(data)
					return
				if self.relayout or a!=self.frame_key:self.relayout=self.zone_redraw=False;self.build_frame(data);self.frame_key=a
				elif self.chrome is not None:self.chrome.set_title("Combat");self.chrome.set_status(self.status_text(data))
				if not L[5]:self.fill(data)
			def tick(self):
				g=self.gump
				if g is None:del bm[:];return
				if bv():return
				if not Kit.is_open(g):
					self.gump=None;self._drop_notes()
					if p(self.dock_key):return
					P["combat_shown"]=False;ai["dirty_save"]=True;aj("combat bars hidden; Show combat in the %s window brings them back."%aD,Kit.HUE_INFO);return
				if((self.made_min>self.slot[0])if self.slot is not None else(self.made_min<a1))and not b4():
					self.snapshot();self.gump=None;self._drop_notes();Kit.dispose(g);self.show()
					if self.docked:Kit.set(self.gump,"IsVisible",False)
					return
				g0();gX();gY();gZ();self.draw(ex())
		eB=((6,6),(6,3),(3,6),(6,0),(0,6),(3,3))
		class ControlPanel(object):
			BODY_H=420;FOE_ROW_H=32
			def __init__(self,windows,combat):
				self.windows,self.combat=windows,combat;self.g=self.list_sa=self.input=self.lock_all_lbl=self.combat_lbl=self.foe_title=None;self.store,self.x0,self.w=({},{}),0,0;self.foe_ver=self.seen_ver=-1;self.foe_rows,self.seen_at=[],0.;self.list_top=self.list_h=0;self.list_lbls=();a=HOST.hub
				if a is not None:a.add("ultima",aD,{"height":self.height,"build":self.build_section,"closed":self.section_closed})
				else:aj("couldn't show the Foe list panel (no shared window).",Kit.HUE_BAD)
			@property
			def gump(self):return self.g if Kit.is_open(self.g)else None
			@property
			def size(self):a=HOST.hub;return(a.W,a.H)if a is not None else(0,0)
			def height(self,w):return self.BODY_H+16
			def build_section(self,g,x,y,w,store):self.g,self.store=g,store;self.x0,self.w=x+8,w-16;self.list_sa,self.foe_ver=None,-1;Kit.add_section(g,x,y,w,self.height(w));self.build_body(y+8);at.pending=True
			def section_closed(self):self.g=self.list_sa=self.input=None;self.foe_rows=[]
			def _heading(self,text,y):a=aH(text,13,"#FFD966");az(a,self.x0+2,y);self.g.Add(a);return a
			def _divider(self,y):d=aK(Kit.STONE_TILE,self.w,4);d.SetPos(self.x0,y);self.g.Add(d)
			def build_body(self,b):g,X,W=self.g,self.x0,self.w;c=int(W/3);self._heading("FOES & IGNORE LIST",b);f=aK(Kit.FIELD_TILE,W,24);f.SetPos(X,b+21);g.Add(f);self.input=G.CreateGumpTextBox("",W-4,22,False,16);self.input.SetPos(X+2,b+22);self.input.SetPlaceholder("Player name");Kit.with_tip(self.input,"Player name for the buttons below");g.Add(self.input);j="Hide combat"if self.combat.is_open()else "Show combat";k=(("Add foe",0,52,self.add_foe,Kit.ART_OK,"Put the typed name on your Foe list"),("Remove foe",1,52,self.remove_foe,Kit.ART_CLOSE,"Take the typed name off your Foe list"),("Target...",2,52,self.target_foe,Kit.ART_PLAY,"Target a player to put them on your Foe list"),("Ignore",0,80,self.ignore_name,Kit.ART_CLOSE,"Hide the typed name from the trackers (an NPC)"),("Unignore",1,80,self.unignore_name,Kit.ART_OK,"Show the typed name in the trackers again"),("Lock all",2,80,self.lock_all,Kit.ART_PLAY,"Lock or unlock every tracker, the combat bars and pop-outs"),(j,0,144,self.toggle_combat,Kit.ART_PLAY,"Show or hide the combat bars"),("Settings",1,144,lambda*a:Z("ultima"),Kit.ART_PAGE,Kit.SETTINGS_TIP%aD),("Sightings",2,144,lambda*a:a0.toggle(),Kit.ART_PAGE,"Open or close the Sightings window"));d=[self._button(m,X+n*c,b+q,c,r,s,v)for m,n,q,r,s,v in k];self.lock_all_lbl,self.combat_lbl=d[5],d[6];self._divider(b+110);self._heading("WINDOWS",b+120);self._divider(b+176);self.foe_title=self._heading("SAVED FOES (0)",b+186);self.list_top=b+210;e=b+self.BODY_H;h=max(16,aw.get("font_h",0)if b3(11)else 0);self.list_h=e-h-14-self.list_top;i=aH("Alt+click any bar: auto-follow (again to stop).",11,bT);az(i,X+2,e-h-6);g.Add(i);self.foe_ver=ai["foe_ver"];self.rebuild_foe_list()
			def _button(self,text,x,y,w,fn,art,tip=None):a=Kit.pic_size(art[0])[0]or 30;b="ut:"+text.lower().replace(" ","_").rstrip(".");return Kit.art_button(self.g,self.store,b,art,x,y,Kit.fit(text,max(10,w-a-6)),tip,on_click=av(fn))
			def _typed(self):return(safe(lambda:self.input.Text,"")or "").strip()
			def _clear_input(self):safe(lambda:self.input.SetText(""))
			def add_foe(self,*a):
				n=self._typed()
				if not n:aj("type a name first.",Kit.HUE_BAD);return
				cV(n);self._clear_input();aj("added %s to the Foe list."%n,Kit.HUE_GOOD)
			def remove_foe(self,*a):
				n=self._typed()
				if n:self._remove(l(n));self._clear_input()
			def _remove(self,key):
				if key in f:
					d9(key)
					if aU[0]==key:aU[0]=None
					a=gn(key);aj("removed %s from the Foe list."%a,Kit.HUE_GOOD)
				else:aj("%s isn't on the Foe list."%key,Kit.HUE_BAD)
			def target_foe(self,*a):aj("target a player for your Foe list.",Kit.HUE_INFO);HOST.pick_target(10,self._foe_targeted)
			def _foe_targeted(self,serial):
				a=API.FindMobile(serial)if serial else None
				if not a or not a.Name:aj("no player targeted.",Kit.HUE_BAD);return
				cV(a.Name);aj("added %s to the Foe list."%a.Name,Kit.HUE_GOOD)
			def ignore_name(self,*a):
				n=self._typed()
				if n:z[n.lower()]=n;aI();self._clear_input();aj("ignoring %s from now on."%n,Kit.HUE_GOOD)
			def unignore_name(self,*a):
				n=self._typed()
				if n and n.lower()in z:z.pop(n.lower());aI();self._clear_input();aj("no longer ignoring %s."%n,Kit.HUE_GOOD)
			def _all_locked(self):
				a=[b.locked for b in self.windows.values()]
				if self.combat.is_open():a.append(ac["combat"][4])
				a.extend(c.locked for c in au.values());return all(a)
			def lock_all(self,*b):
				a=not self._all_locked()
				for w in self.windows.values():w.set_locked(a)
				self.combat.set_locked(a)
				for p in list(au.values()):p.set_locked(a)
				self.refresh_labels()
			def toggle_combat(self,*b):
				a=self.combat
				if a.is_open()and p(a.dock_key):return
				(a.hide if a.is_open()else a.show)();self.refresh_labels()
			def refresh_labels(self):
				if self.gump is None or self.lock_all_lbl is None:return
				Kit.set_text(self.lock_all_lbl,"Unlock all"if self._all_locked()else "Lock all");Kit.set_text(self.combat_lbl,"Hide combat"if self.combat.is_open()else "Show combat")
			def reset_defaults(self,*b):
				dD()
				for p in au.values():p.opacity,p.locked=aS,False
				for w in self.windows.values():
					if w.docked:w.docked=False;A(w.dock_key)
				a=self.combat.docked
				if a:self.combat.docked=False;A(self.combat.dock_key)
				c2(self.windows);self.combat.reset()
				if a and self.combat.is_open():Kit.set(self.combat.gump,"IsVisible",True)
				if HOST.hub is not None:HOST.hub.refresh()
				dT();aI();aj("settings and windows reset to the defaults.",Kit.HUE_GOOD)
			def set_all_opacity(self,v):
				P["opacity"]=v
				for w in self.windows.values():w.apply_opacity(v)
				for a in au.values():a.apply_opacity(v)
				self.combat.apply_opacity(v);ac["panel"][6]=v;ai["dirty_save"]=True
			def rebuild_foe_list(self):
				if self.gump is None:return
				Kit.dispose(self.list_sa)
				for b in self.list_lbls:aG.pop(id(b),None)
				self.list_lbls=i=[];self.list_sa=G.CreateGumpScrollArea(self.x0,self.list_top,self.w,self.list_h);self.g.Add(self.list_sa);self.foe_rows=[];j=sorted(f.items(),key=lambda a:a[1].lower());aR(self.foe_title,"SAVED FOES (%d)"%len(j))
				if not j:b=aH("No foes yet. Type a name and press Add foe.",12,"#888888");i.append(b);az(b,2,2);self.list_sa.Add(b);return
				m=time.time();p=self.w-c5;q=set(ao.values());e=self.list_sa
				for r,(c,d)in enumerate(j):
					y=r*self.FOE_ROW_H;b=aH(cK(o(d),24),13,"#FF9090");i.append(b);az(b,2,y+2);e.Add(b);g=p-22;a3(e,g,y,18,18,"x",self._foe_btn(c,d,self._remove),"Take %s off your Foe list. %s"%(o(d),aW));g-=22;l=aU[0]==c;a3(e,g,y,18,18,"L*"if l else "L",self._foe_btn(c,d,self.link_click),("Press L on the other entry (L here again: cancel). "if l else "Link as one person: L here, then L on the other entry. ")+aW,face=bR if l else bp)
					if c in ao or c in q:g-=22;a3(e,g,y,18,18,"U",self._foe_btn(c,d,self.unlink_click),"Unlink from its group. "+aW)
					e.Add(aQ(0,y,max(20,g-6),18,(lambda k,n:(lambda*a:self.foe_name_click(k,n)))(c,d),aZ(gR,d)));h=aH(self.foe_info(c,m),11,bT,maxWidth=p-6);i.append(h);az(h,2,y+17);e.Add(h);self.foe_rows.append((c,h))
				self.seen_ver=ap["seen_ver"];self.seen_at=m+db
			def _foe_btn(self,k,n,fn):return lambda*a:self.foe_name_click(k,n)if aN()else fn(k)
			@staticmethod
			def foe_info(key,now):a=cU(key);b=gj(key,now);return a+"; "+b if a else b
			def link_click(self,key):
				if key not in f:return
				a=aU[0]
				if a is None or a not in f:aU[0]=key;aj("press L on the entry to link with %s."%f[key],Kit.HUE_INFO)
				elif a==key:aU[0]=None;aj("linking cancelled.",Kit.HUE_INFO)
				else:aU[0]=None;aj(gk(a,key),Kit.HUE_GOOD);aI()
				ai["foe_ver"]+=1
			def unlink_click(self,key):
				if key in f and d9(key):aj("%s is no longer linked."%f[key],Kit.HUE_GOOD);aI();ai["foe_ver"]+=1
			def foe_name_click(self,key,name):
				if aN():
					a,b=None,-1.
					for s,k in bu.items():
						if k==key and API.FindMobile(s)is not None:
							t=bb.get(s,0.)
							if t>b:a,b=s,t
					if a is not None:bi(a)
					else:aj("%s isn't in range."%name,Kit.HUE_BAD)
					return
				safe(lambda:self.input.SetText(name))
			def update(self):
				if self.gump is None:return
				if self.foe_ver!=ai["foe_ver"]:self.foe_ver=ai["foe_ver"];self.rebuild_foe_list()
				elif self.foe_rows:
					a=time.time()
					if self.seen_ver!=ap["seen_ver"]or a>=self.seen_at:
						self.seen_ver=ap["seen_ver"];self.seen_at=a+db
						for b,c in self.foe_rows:aR(c,self.foe_info(b,a))
				self.refresh_labels()
		class SightRow(object):
			__slots__=("serial","name","prev","e","c","nm","here")
			def __init__(self):self.serial,self.name,self.prev,self.e=None,"",None,None;self.c,self.nm,self.here={},"",None
		def g4(serial,name):return bA(serial,lambda:a0.filter_name(name,serial))
		eC=26+bM*22+6;ck=2*Kit.MARGIN+30+36+eC+36+3*Kit.GAP;eD=ck-(bM-1)*22
		def eE(obj,w,h,mode):
			a=(int(w),int(h))if(w is not None and h is not None)else None
			if a!=obj.slot or(mode=="again"and a is not None):obj.slot=a;obj.redraw=True
		def eF(obj,a,b):
			z=obj.slot
			if z is None or obj.st["minimized"]or not p(obj.KEY)or z[0]<a or z[1]<b:return
			return z
		class SightingsWindow(object):
			KEY="ultima.sightings";TITLE="Sightings";W=480;MINI_W,MINI_H=300,46;COLS=(8,92,230,278,404)
			def __init__(self):self.st={"minimized":False,"docked":False,"shutting":True};self.win={"g":None};self.slot,self.want,self.n,self.w=None,False,bM,self.W;self.hooks=Kit.dock_hooks(self.TITLE,e5,self.st,self.win,self.ask_redraw,self.fit);self.hooks.update(show=self.zone_show,min=(self.W,eD));self.flt={"text":"","noto":0,"time":0};self.fser,self.fshow=None,"";self.forget()
			def fit(self,w,h,mode):eE(self,w,h,mode)
			def zone_show(self):self.want=True
			def forget(self):self.c,self.store,self.rows={},({},{}),[];self.page,self.matches,self.counts=0,[],{};self.ver,self.ver_at,self.dirty,self.redraw=None,0.,True,False;self.full_at=self.here_at=self.poll_at=0.
			def is_open(self):return self.win["g"]is not None
			def ask_redraw(self):self.redraw=True
			def toggle(self):
				if not self.is_open():self.show()
				elif self.st["minimized"]or self.st["docked"]:self.bring()
				elif not p(self.KEY):self.close()
			def bring(self):
				if not self.is_open():self.show()
				if self.st["minimized"]or self.st["docked"]:A(self.KEY);self.st["minimized"]=self.st["docked"]=False;Kit.save_min(bN,False);self.build()
			def show(self):
				if self.is_open():return
				a=p(self.KEY);self.st.update(shutting=False,docked=HOST.dock_soon(self.KEY),minimized=not a and bool(Kit.load_min(bN)or HOST.dock_wanted(self.KEY)));self.build();Kit.put_var(bO,"1")
			def save_pos(self):
				if not p(self.KEY):Kit.save_pos(cB,self.win["g"])
			def close(self,stopping=False):
				g=self.win["g"]
				if g is None:return
				self.st["shutting"]=True
				if not stopping:A(self.KEY);Kit.put_var(bO,"0")
				if not p(self.KEY):Kit.save_pos(cB,g);Kit.save_min(bN,self.st["minimized"])
				self.win["g"]=None;self.forget();Kit.dispose(g)
			def lost(self):self.win["g"]=None;self.st["shutting"]=True;Kit.put_var(bO,"0");self.forget()
			def build(self):
				self.redraw=False;d=self.win["g"];x,y=Kit.load_pos(cB,(320,160),(self.W,ck))
				if Kit.is_open(d):x,y=d.GetX(),d.GetY()
				self.win["g"]=None;self.forget();a,c,n=self.store,self.c,self.rows;M,j=Kit.MARGIN,Kit.GAP;g=G.CreateGump(True,True);self.n,self.w=bM,self.W
				if self.st["minimized"]:w,h=self.MINI_W,self.MINI_H;c["status"]=Kit.mini_bar(g,a,w,h,self.TITLE,self.KEY,av(self.toggle_min),close_tip="Close Sightings")
				else:
					z=eF(self,self.W,eD);w,h=z if z else(self.W,ck);k=h-ck+eC;self.n=max(1,(k-32)//22);self.w=w;e=w-2*M;Kit.add_window_frame(g,w,h);Kit.title_bar(g,a,w,self.TITLE,self.KEY,av(self.toggle_min),av(lambda:ah(self.KEY,self.TITLE)),av(lambda:Z("ultima")),close_tip="Close Sightings");b=M+30+j;Kit.add_section(g,M,b,e,36);Kit.add_label(g,"Find:",M+10,b+9);c["find"]=Kit.with_tip(Kit.add_textbox(g,self.find_view(),M+52,b+7,128,numbers=False),"Part of a name: list only that player");c["noto"]=Kit.art_button(g,a,"noto",Kit.ART_PAGE,M+196,b+7,cz[self.flt["noto"]][0],"Which players to list (click to cycle)",on_click=av(lambda:self.cycle("noto",cz)));c["time"]=Kit.art_button(g,a,"time",Kit.ART_PAGE,M+326,b+7,cA[self.flt["time"]][0],"How far back to list (click to cycle)",on_click=av(lambda:self.cycle("time",cA)));f=b+36+j;Kit.add_section(g,M,f,e,k)
					for l,o in zip(self.COLS,("Time","Player","Colour","Where","Count")):Kit.add_label(g,o,M+l,f+6,Kit.HUE_TITLE)
					for p in range(self.n):
						m=f+26+p*22;r=SightRow()
						for q,l,s in(("t",0,Kit.HUE_INFO),("n",1,Kit.HUE_TEXT),("o",2,Kit.HUE_TEXT),("p",3,Kit.HUE_INFO),("k",4,Kit.HUE_INFO)):r.c[q]=Kit.add_label(g,"",M+self.COLS[l],m+2,s)
						r.c["hit"]=Kit.catcher(g,M+4,m,e-8,22,av(RowClick(r,g4)),en);n.append(r)
					i=f+k+j;Kit.add_section(g,M,i,e,36);Kit.art_button(g,a,"newer",Kit.ART_PAGE,M+10,i+7,"Prev","Newer sightings",on_click=av(self.newer));Kit.art_button(g,a,"older",Kit.ART_PAGE,M+120,i+7,"Next","Older sightings",on_click=av(self.older));c["status"]=Kit.add_label(g,"",M+230,i+10,Kit.HUE_INFO)
				Kit.show_window(g,x,y,w,h,self.KEY,self.st["minimized"]and self.st["docked"],None,self.save_pos,self.win,{"g":g});Kit.dispose(d);self.refresh(time.time(),True)
			def toggle_min(self,*a):Kit.win_action("toggle_min",self.st,self.KEY,self.TITLE,self.build,bN)
			def cycle(self,k,table):
				self.flt[k]=(self.flt[k]+1)%len(table)
				if k in self.c:Kit.set_text(self.c[k],table[self.flt[k]][0])
				self.page,self.dirty=0,True
			def newer(self,*a):
				if self.page>0:self.page-=1;self.dirty=True
			def older(self,*a):
				if(self.page+1)*self.n<len(self.matches):self.page+=1;self.dirty=True
			def find_view(self):a=self.flt["text"];self.fshow=Kit.veil("name",a,self.fser)if a and self.fser else a;return self.fshow
			def filter_name(self,name,serial=None):
				a=""if self.flt["text"].lower()==name.lower()else name;b=self.c.get("find");self.flt["text"],self.fser=a,(serial if a else None);c=self.find_view()
				if b is not None:safe(lambda:b.SetText(c))
				self.page,self.dirty=0,True
			def tick(self,now):
				if self.want:
					self.want=False
					if p(self.KEY):
						if not self.is_open():self.show()
						elif self.st["minimized"]or self.st["docked"]:self.st["minimized"]=self.st["docked"]=False;self.build()
				if self.win["g"]is None:return
				if Kit.was_clicked(self.store,"close"):self.close();return
				if self.redraw:self.build();return
				if now<self.poll_at<=now+bo:return
				self.poll_at=now+bo
				if not Kit.is_open(self.win["g"]):self.lost();return
				if self.st["minimized"]and self.st["docked"]:return
				self.refresh(now)
			def refresh(self,now,force=False):
				c=self.c
				if self.st["minimized"]:
					if force or ap["ver"]!=self.ver or now>=self.full_at:
						self.ver,self.full_at=ap["ver"],now+da;n=len(aF);a="%s: %d"%(self.TITLE,n)
						if n:e=aF[-1];a+=", last %s %s"%(o(e[cf],e[ce]),cT(e[bk],cS(now)))
						else:a="%s: none yet"%self.TITLE
						Kit.set_text(c["status"],Kit.fit(a,self.MINI_W-90))
					return
				b=c.get("find")
				if b is not None:
					d=str(b.Text or "").strip()
					if d!=self.fshow:self.flt["text"]=self.fshow=d;self.fser=None;self.page,self.dirty=0,True
				if force or self.dirty or now>=self.full_at or(ap["ver"]!=self.ver and not 0.<=self.ver_at-now<=1.):self.ver_at=now+1.;self.work_out(now);self.fill(now)
				elif now>=self.here_at:self.mark_here(now)
			def work_out(self,now):
				self.dirty=False;self.ver,self.full_at=ap["ver"],now+da;a=cA[self.flt["time"]][1];g=None if a is None else(cS(now)if a=="today"else now-a);b=cz[self.flt["noto"]][1];h=l(self.flt["text"]);c,d=[],{}
				for j in range(len(aF)-1,-1,-1):
					e=aF[j]
					if g is not None and e[bk]<g:break
					if h and h not in e[bl]:continue
					if b is not None and(e[bl]not in f if b=="foe"else e[bF]not in b):continue
					c.append(e);d[e[bl]]=d.get(e[bl],0)+1
				self.matches,self.counts=c,d;i=max(0,(len(c)-1)//self.n)
				if self.page>i:self.page=i
			def fill(self,now):
				c=cS(now);a=self.page*self.n;m=self.matches
				for i,r in enumerate(self.rows):j=a+i;self.assign(r,m[j]if j<len(m)else None,c)
				self.mark_here(now);n=len(m)
				if n:b="%d-%d of %d, %s"%(a+1,min(n,a+self.n),n,Kit.count(len(self.counts),"name"))
				elif aF:b="No sightings match the filters"
				else:b="No sightings yet"if P["sightings"]else "Logging is off (settings page)"
				Kit.set_text(self.c["status"],Kit.fit(b,self.w-2*Kit.MARGIN-236))
			def assign(self,r,e,a):
				c=r.c
				if e is None:
					if r.e is not None:
						r.prev=(r.serial,r.name,time.time());r.e,r.serial,r.name,r.nm,r.here=None,None,"","",None
						for k in("t","n","o","p","k"):Kit.set_text(c[k],"")
					return
				if e is not r.e:
					if r.serial is not None and r.serial!=e[ce]:r.prev=(r.serial,r.name,time.time())
					r.e,r.serial,r.name=e,e[ce],e[cf];r.here=None;r.nm=Kit.fit(H(e[cf],e[ce],e[bF]),124);Kit.set_text(c["o"],d5(e[bF]),Kit.cb_hue(e[bF],aa.get(e[bF],Kit.HUE_TEXT)));b=Kit.veil("place",d6(e[d0],e[d1],e[d2]));Kit.set_text(c["p"],Kit.fit(b+(" G"if e[cQ]else ""),118));g=e[cQ];d="Seen %s at %s%s"%(cT(e[bk],a),b,", in a guard zone (G)"if g else(", outside the guards"if g is False else ""));Kit.with_tip(c["hit"],aZ(en,e[cf],d))
				Kit.set_text(c["t"],cT(e[bk],a));Kit.set_text(c["k"],"x%d"%self.counts.get(e[bl],1))
			def mark_here(self,now):
				self.here_at=now+1.
				for r in self.rows:
					if r.e is None:continue
					t=bb.get(r.serial);a=t is not None and now-t<=2*bo+.05
					if a!=r.here:r.here=a;Kit.set_text(r.c["n"],r.nm,Kit.HUE_GOOD if a else Kit.HUE_TEXT)
		class KillerWindow(object):
			KEY="ultima.killer";TITLE="Add my killer";W=340;MINI_W,MINI_H=260,46;ROW_H=26
			def __init__(self):self.st={"minimized":False,"docked":False,"shutting":True};self.win={"g":None};self.store,self.c,self.cands=({},{}),{},[];self.until,self.slot=0.,None;self.redraw=self.want=False;self.hooks=Kit.dock_hooks(self.TITLE,0,self.st,self.win,self.ask_redraw,self.fit);self.hooks.update(show=self.zone_show,min=(self.W,self.height(1)))
			def ask_redraw(self):self.redraw=True
			def zone_show(self):self.want=True
			def fit(self,w,h,mode):eE(self,w,h,mode)
			def held(self):return p(self.KEY)
			def height(self,n):return 2*Kit.MARGIN+30+Kit.GAP+8+n*self.ROW_H+26
			def open(self,got,now,total=None):self.cands=[{"name":b[0],"serial":b[2]}for b in got];self.until=now+e6;self.st.update(shutting=False,docked=False,minimized=not self.held()and Kit.load_min(cD));self.build();n=len(got)if total is None else total;aj("you died; %s attacked you (see %s)."%(Kit.count(n,"player"),self.TITLE),Kit.HUE_BAD)
			def save_pos(self):
				if not self.held():Kit.save_pos(cC,self.win["g"])
			def close(self):
				g=self.win["g"]
				if g is None:return
				if not self.held():Kit.save_pos(cC,g);Kit.save_min(cD,self.st["minimized"])
				self.st["shutting"]=True;self.win["g"],self.c,self.cands=None,{},[];Kit.dispose(g)
			def end(self):
				if not self.held():self.close()
				elif self.cands:self.cands=[];self.build()
			def build(self):
				d=self.win["g"];p=self.st["minimized"];z=eF(self,self.W,self.height(1));W,H=z if z else(self.W,self.height(max(1,len(self.cands))));s,t=Kit.screen();j=self.cands[:max(1,(H-self.height(0))//self.ROW_H)]if z else self.cands;x,y=Kit.load_pos(cC,(max(0,((s or 1024)-W)//2),max(0,((t or 768)-H)//3)),(W,H))
				if Kit.is_open(d):x,y=d.GetX(),d.GetY()
				self.win["g"]=None;c,k=({},{}),{};M=Kit.MARGIN;g=G.CreateGump(True,True)
				if p:W,H=self.MINI_W,self.MINI_H;u=len(self.cands);k["status"]=Kit.mini_bar(g,c,W,H,self.TITLE,self.KEY,av(self.toggle_min),"%s: %s"%(self.TITLE,Kit.count(u,"attacker")),close_tip="Close the attacker list")
				else:
					e=W-2*M;Kit.add_window_frame(g,W,H);Kit.add_section(g,M,M,e,30);Kit.add_label(g,self.TITLE.upper(),M+30,M+7,Kit.HUE_TITLE)
					if Kit.zone_up(self.KEY):Kit.catcher(g,M,M,e,30,lambda*a:None,None,movable=True)
					else:Kit.title_catcher(g,M,M,W-M-80-M,30,av(self.toggle_min),key=self.KEY);Kit.art_button(g,c,"min",Kit.ART_MIN,W-M-74,M+7,None,Kit.MIN_TIP,on_click=av(self.toggle_min));Kit.art_button(g,c,"close",Kit.ART_CLOSE,W-M-54,M+4,None,"Close the attacker list")
					h=M+30+Kit.GAP;Kit.add_section(g,M,h,e,H-h-M);q="Add to foes";m=W-M-10-(35+Kit.text_w(q))
					for i,b in enumerate(j):n=h+8+i*self.ROW_H;v=l(b["name"])in f;r=Kit.noto_mark(Kit.noto_name(X(b["serial"])))if Kit.cblind and b["serial"]else "";Kit.add_label(g,Kit.fit((r+" "if r else "")+o(b["name"],b["serial"]or 0),m-M-30),M+10,n+3,Kit.HUE_BAD);Kit.catcher(g,M+6,n,m-M-14,22,av(self.make_follow(i)),aZ("Alt+click: auto-follow (again to stop)",b["name"]));k["add%d"%i]=Kit.art_button(g,c,"add%d"%i,Kit.ART_OK,m,n,"On Foe list"if v else q,"Put %s on your Foe list. Alt+click: auto-follow (again to stop)"%o(b["name"],b["serial"]or 0),on_click=av(self.make_add(i)))
					w="Closes on resurrection."if j else Kit.fit("Lists your attackers when you die."if P["killer"]else "Off (settings page)",e-20);Kit.add_label(g,w,M+10,h+8+len(j)*self.ROW_H+2,Kit.HUE_INFO)
				Kit.show_window(g,x,y,W,H,self.KEY,p and self.st["docked"],None,self.save_pos);self.win["g"],self.store,self.c=g,c,k;self.redraw=False;Kit.dispose(d)
			def make_add(self,i):
				def a(*c):
					if i>=len(self.cands):return
					if aN():self.make_follow(i)();return
					a=self.cands[i]
					if l(a["name"])in f:aj("%s is already on the Foe list."%a["name"],Kit.HUE_INFO)
					else:cV(a["name"]);aj("added %s to the Foe list."%a["name"],Kit.HUE_GOOD)
					b=self.c.get("add%d"%i)
					if b is not None:Kit.set_text(b,"On Foe list")
				return a
			def make_follow(self,i):
				def a(*b):
					if i>=len(self.cands)or not aN():return
					a=self.cands[i];s=a["serial"]
					if s is None:s,c=eg(a["name"])
					if s is None:aj("%s isn't in sight."%a["name"],Kit.HUE_BAD)
					else:bi(s)
				return a
			def toggle_min(self,*b):a=self.st;a["minimized"]=not a["minimized"];Kit.save_min(cD,a["minimized"]);self.build()
			def tick(self,now):
				if self.want:
					self.want=False;a=self.st
					if self.held()and(self.win["g"]is None or a["minimized"]or a["docked"]):a.update(shutting=False,minimized=False,docked=False);self.build()
				g=self.win["g"]
				if g is None:return
				if Kit.was_clicked(self.store,"close"):self.close()
				elif not Kit.is_open(g):self.win["g"],self.c,self.cands=None,{},[];self.st["shutting"]=True
				elif not self.cands and not self.held():self.close()
				elif self.redraw:self.build()
				elif self.cands and now>=self.until:self.end()
		a0=SightingsWindow();a8=KillerWindow()
		def eG():return tuple(tuple(a)for b,a in sorted(ac.items()))
		aq={"f":None,"seen":None,"stable":0,"loaded":False,"lines":None,"save_at":0.}
		def g5():
			if ai["started"]or aq["loaded"]:return
			eL();aq["loaded"]=True
			def a():
				try:aq["lines"]=dV()
				except Exception as a:ca[0]="could not read the save file: "+str(a);aq["lines"]=()
			dU(a)
		def g6():
			a=aq["lines"]
			if a is None:return False
			aq["lines"]=None
			if ai["started"]or not a:return False
			dX(a[0],a[1]);return True
		def a9():
			if ai["started"]:ai["dirty_save"]=True
			else:aq["save_at"]=time.time()+fe
		def eH(background):
			if aq["save_at"]:aq["save_at"]=0.;cd(background=background)
		def g7():return all(bool(ac[a][4])for a in aE+["combat"])
		hq={};eI={"top":32,"pad":6,"ldy":0,"sdy":4,"fh":26,"lw":110,"ugap":6}
		def eJ(w):a={"dx":320,"bdy":0,"h":26};b="Sort: "+du[P["sort"]];return(("WINDOWS",(("slider","scale","Scale:","Size of the trackers and pop-out bars (%d-%d)"%(cm,cn),cm,cn,{"unit":"%"}),("slider","opacity","Opacity:","Background opacity of every window (0-100)",0,100,{"unit":"%"}),("slider","range","Range:","Tracker range in tiles (%d-%d)"%(co,cp),co,cp,{"unit":"tiles"}),("gap",-78),("check","sync","Sync tracker sizes","Resizing one tracker resizes the others",a),("buttons",(("unanchor",Kit.ART_CLOSE,"Unanchor all","Undo every anchor between windows"),),a),("buttons",(("reset",Kit.ART_CLOSE,"Reset to defaults","Reset scale, opacity, range, options and window places"),),a),("check","lock","Lock the windows in place","Free windows can't be moved or resized (zoned windows stay put anyway)"))),("OPTIONS",(("check","combat_only","Combat bars: only once fighting","Only add a mobile once it attacks you, you attack it in war mode, or it fights you up close",{"stay":True}),("check","borders","Show a border on the pop-out bars","Stone border round the pop-out bars (the other windows always have one)",{"dx":320,"h":28}),("check","magery","Magery buttons","P (Poison) and Z (Paralyze) on the combat bars; H (Heal) and C (Cure) on friends, Shift+click for the greater spell",{"stay":True}),("check","healing","Bandage button","B on friends' bars: bandage when adjacent, else follow them",{"dx":320}),("buttons",(("sort",Kit.ART_PAGE,b,"Order of the tracker lists (name, distance or HP)"),)))),("SIGHTINGS AND DEATHS",(("check","sightings","Log players who come into range","Each non-friend player goes in the Sightings log once per visit (last %d kept)"%bL,{"stay":True}),("buttons",(("sightings",Kit.ART_PAGE,"Open Sightings","Open the Sightings window"),),{"dx":320}),("check","killer","On death: list your attackers","A window lists players who attacked you in the last %d s, each with Add to foes"%int(cy)))),("FOE ALERT  (sound: Settings > Alerts)",(("check","alert_red","Red","Alert on a red (murderer) in range",{"stay":True}),("check","alert_foes","Foe list","Alert on a Foe list player in range (linked alts too)",{"stay":True,"dx":110}),("check","alert_orange","Orange","Alert on an orange (enemy) in range",{"stay":True,"dx":230}),("check","alert_gray","Grey","Alert on a grey (criminal) in range",{"dx":340,"h":28}),("slider","alert_minutes","Same player again after:","Minutes before the same player alerts again (%d-%d)"%(cv,cw),cv,cw,{"lw":178,"sw":150,"ugap":12,"unit":"%d min"%P["alert_minutes"]}))))
		g8=Kit.Page(P,eJ,opts=eI)
		def g9(g,x,y,w):g5();aq.update({"f":Kit.Form(g,x,y,w,dict(P,lock=g7()),eJ(w),**eI),"stable":0,"seen":{a:P[a]for a in dt}})
		def ha():
			f=aq["f"]
			if f is None:return
			if g6():aq["f"]=None;Y("ultima");return
			cc();l=time.time()
			if aq["save_at"]and l>=aq["save_at"]:eH(True)
			h,a=f.store,aq["seen"];b=ak["windows"]
			if Kit.was_clicked(h,"unanchor"):at.clear();a9();aj("every window unanchored.",Kit.HUE_GOOD)
			if Kit.was_clicked(h,"reset"):
				if ak["panel"]is not None:ak["panel"].reset_defaults()
				else:dD();a9();aj("settings and windows reset to the defaults.",Kit.HUE_GOOD)
				Y("ultima");return
			f.vals=dict(P,**a);c=f.read();g=c["scale"]
			if g!=a["scale"]:a["scale"]=g;aq["stable"]=0
			elif g!=P["scale"]:
				aq["stable"]+=1
				if aq["stable"]>=2:
					if b is not None:gU(g,b)
					else:P["scale"]=g;a9()
			i=c["opacity"]
			if i!=a["opacity"]:
				a["opacity"]=i
				if ak["panel"]is not None:ak["panel"].set_all_opacity(i)
				else:P["opacity"]=i;a9()
			for k in("range","alert_minutes"):
				if c[k]==a[k]:continue
				a[k]=P[k]=c[k];a9()
				if k=="alert_minutes":Kit.set_text(f.c["alert_minutes_lbl"],"%d min"%c[k])
			if Kit.was_clicked(h,"sort"):P["sort"]=(P["sort"]+1)%len(du);a9();Y("ultima");return
			if Kit.was_clicked(h,"sightings"):
				if ak["windows"]is not None:aC["sight_req"]=True
				else:aj("the trackers aren't up yet; try again in a moment.",Kit.HUE_INFO)
			d=bool(c.get("lock"))
			if a.get("lock")is None:a["lock"]=d
			elif d!=a["lock"]:
				a["lock"]=d
				if b is not None:
					for k in aE:b[k].set_locked(d)
				if ak["panel"]is not None:ak["panel"].combat.set_locked(d)
				else:
					for k in aE+["combat"]:ac[k][4]=d
				aI()
			for e in("borders","healing","magery","combat_only","sync","alert_red","alert_foes","alert_orange","alert_gray","sightings","killer"):
				v=c[e]
				if v==P[e]:continue
				P[e]=v;a9()
				if e=="borders":dT()
				elif e=="healing"and not v:ar["serial"]=None
				elif e=="sync"and v and b is not None:j=[b[m]for m in aE if not b[m].minimized];eq(b,j[0]if j else b[aE[0]]);aj("tracker sizes synced.",Kit.HUE_GOOD)
		def hb():aq["f"]=None;eH(True)
		aC={"last_layout":None,"tick":0,"errors":set(),"next_scan":0.,"next_combat":0.,"next_glow":0.,"sight_req":False,"next_hp":0.}
		def cl(key,step,now):
			t=aC[key]
			if now<t<=now+step:return False
			aC[key]=t+step if 0<=now-t<step else now+step;return True
		def hc():
			c,d,b=ak["windows"],ak["combat"],ak["panel"];a={g:(c[g].gump,c[g].size)for g in aE}
			if d.is_open():a["combat"]=(d.gump,(ac["combat"][2],0))
			if b.gump is not None:a["panel"]=(b.gump,b.size)
			for s,e in au.items():a["pop:%d"%s]=(e.gump,e.size)
			return a
		def eK():
			for w in(ak["windows"]or{}).values():w.snapshot()
			if ak["combat"]is not None:ak["combat"].snapshot()
		def hd(view,title,fit):
			def c():
				if view.gump is None or ai.get("shutting"):return
				return "docked"if view.docked else("minimized"if view.minimized else "open")
			def b(on):Kit.set(view.gump,"IsVisible",on)
			def a(docked,mini):
				def f():
					if view.minimized!=mini:view.toggle_minimize()
					view.docked=docked;b(not docked)
				return f
			def d():view.docked=False;b(True)
			def e():
				if view.gump is None and view is ak["combat"]:bf.append(view.show)
				else:a(False,False)()
			return{"title":title,"icon":0,"state":c,"show":e,"dock":a(True,True),"undock":d,"minimize":a(False,True),"gump":lambda:view.gump,"fit":fit,"exact":True,"verify":True,"redraw":view.zone_chrome}
		def he(windows,combat):
			for c,w in list(windows.items())+[("combat",combat)]:af("ultima."+c,hd(w,dg[c],w.layout_fit));ba.add(ag,"ultima."+c)
			for a,b in(("ultima.sightings",a0.hooks),(a8.KEY,a8.hooks)):af(a,b);ba.add(ag,a)
		def eL():
			for d in(f,z,u,au,aT,aJ,bc,F,bG,ax,ao,bX,ay,a5):d.clear()
			a6[0]=None;cO[0]=bj[0]=0.;bE[0]=0
			for q in(bs,bm,a7,aY,b_,bz,bf,aF):del q[:]
			bH[0]+=1;dC();P.update(dw);al.update(req=False,size={},own_size={},force=set(),made={});ai.update(fE,party=set());ar.update(serial=None,follow=None);at.__init__();aB.update(serial=None,stale=False);be[0]=cb[0]=False;aq.update({"loaded":False,"lines":None,"save_at":0.});aL["learn"]=aL["attack"]=aL["killer"]=None;ew.update(serial=None,until=0.);ee[0]=-10.
			for a in list(a4):aX(a)
			ap.update(dirty=False,save_at=0.);ap["ver"]+=1;ap["seen_ver"]+=1;aU[0]=None;aA["dead"]=aA["me"]=None
		def hf():
			a=None
			if aq["save_at"]:aq["save_at"]=0.;a=dZ()
			eL();ai["started"]=True
			for k in aL:aL[k]=O()
			fL();aC["errors"]=set();U(c8,"Foe in range",e3);ba.service("ultima.is_foe",go);ba.service("ultima.classify",gr);ba.service("look.ultima",lambda:bf.append(gS));bz.append(lambda:hg(a))
		def hg(a=None):
			if ai["shutting"]:return
			if a is not None:bD[0]+=1;d_(a,bD[0]);cc()
			fZ();at.saved=at.saved_groups();f8();ai["loaded"]=True
		def hh():
			if ak["windows"]is None:
				if ai["loaded"]and not ai["shutting"]:gc()
				return
			cc();fK();dF(bf)
			while bs:ah(bs.pop(0))
			if cI:del cI[:];Z(eM)
			b,d,i=ak["windows"],ak["combat"],ak["panel"]
			if b is None:return
			gV(b);a=time.time()
			try:
				try:
					if aC["sight_req"]:aC["sight_req"]=False;a0.bring()
					a0.tick(a);a8.tick(a)
				except Exception as c:
					if N():return
					bd(c)
				g2();fU();at.tick(hc)
				if at.groups_changed():ai["dirty_save"]=True
				if cl("next_glow",fo,a):
					f=ek();b["friend"].pulse(f)
					for e in list(au.values()):e.pulse(f)
				if cl("next_scan",bo,a):
					j=gx()
					try:gD(a)
					except Exception as c:bd(c)
					if bv():return
					for g in aE:b[g].update(j[g])
					for e in list(au.values()):e.update()
					if bv():return
					gT(b);i.update();fV();aC["tick"]+=1
					if aC["tick"]%eV==0:
						eK();h=eG()
						if h!=aC["last_layout"]or ai["dirty_save"]or(ap["dirty"]and a>=ap["save_at"]):aC["last_layout"]=h;aI()
				if cl("next_combat",bo if d.docked else eO,a)and not bv():d.tick()
				if cl("next_hp",eP,a)and not bv():hj(b,d)
			except Exception as c:
				if N():return
				bd(c)
		def hj(windows,combat):
			for w in windows.values():
				if w.minimized or w.docked or not Kit.is_open(w.gump):continue
				for r in w.rows:
					e=r.e
					if not r.shown or not e or not e["hmax"]or e.get("mob")is None:continue
					try:c,b=e["mob"].Hits or 0,e["mob"].HitsMax or 0
					except Exception:continue
					if b>0:e["hits"],e["hmax"]=c,b;r.values(e)
			if combat is None or combat.docked or combat.minimized or not Kit.is_open(combat.gump):return
			for r in combat.rows:
				d=r.e
				if not r.shown or d is None:continue
				m=cj.get(d[0])
				if m is None:continue
				try:a=(m.Hits or 0,m.HitsMax or 0)
				except Exception:continue
				if a[1]>0 and a!=d[3:5]:r.values(d[:3]+a+d[5:])
		def hk():
			if dF(bz):return
			if be[0]:be[0]=False;cd(background=True)
		def hl():return bool(bz)or bool(be[0])
		def hm():
			ai["shutting"]=True;ai["started"]=False;a0.close(stopping=True);a8.close();ba.close()
			for c in list(a4):aX(c)
			if ak["windows"]is None:return
			safe(lambda:Kit.on_client(eK));be[0]=False;cd();a=[]
			for w in ak["windows"].values():a.append(w.gump);w.gump=None
			if ak["combat"]is not None:a.append(ak["combat"].gump);ak["combat"].gump=None
			if HOST.hub is not None:HOST.hub.remove("ultima")
			for b in list(au.values()):a.append(b.gump);b.gump=None
			au.clear()
			for g in a:Kit.dispose(g)
			bB(ar["follow"]);ak.update({"windows":None,"combat":None,"panel":None})
		return{"start":hf,"tick":hh,"stop":hm,"client_tick":True,"config_height":g8.height,"build_config":g9,"poll_config":ha,"config_closed":hb,"thread_tick":hk,"thread_wanted":hl}
	def aA():
		az="lookout";l="Lookout";K="Lookout_settings";aA="Lookout_pos";aB="Lookout_min";aC="_lookout_feed.txt";W=370;N,aD=280,46;aE=2597;z=5;aF=30;p=22;A,C=3,24;aG=.25;O=30.;P=5.;q=20.;aH=.1;Q=15.;R=32768;V=60;f=65536;aI=30.;aJ=120.;X=10.;Y=200;D=1.;E=400;aK=1000;Z=8;ab=10.;ac=.25;ad="lookout.alarm";aL=824;ae="lookout.lost";aM=74;af=60.;s=0x4C4F4F4B;aN=("Click: tracking arrow to where they were seen (again to clear). Alt+click: auto-follow (again to stop)");c={"watch":False,"listen":True,"range":18,"ping":True,"lost":True};bd=dict(c)
		def ag():return{"shutting":False,"minimized":False,"docked":False,"queue":[],"me":0,"path":None,"facet":-1,"next_scan":0.,"present":{},"in_range":0,"hb_next":0.,"outbox":[],"write_next":0.,"pings":[],"ping_next":0.,"listeners":{},"listeners_next":0.,"offset":0,"listen_next":0.,"announce_next":0.,"seen":{},"inbox":[],"watchers":{},"file":"none","recent":[],"arrow":None,"own_alarm":None,"dirty":True,"refresh_at":0.}
		b={"minimized":False,"shutting":False,"docked":False,"queue":[]};b.update(ag());d={"g":None,"c":{},"store":({},{}),"rows":[]};ah,F,aj=Kit.basics(b,l);ak,aO={"range":(A,C)},("watch","listen","range","ping","lost")
		def al():Kit.kv_load(K,";",c,ak)
		def am():Kit.kv_save(K,";",c,aO,ak)
		def t():
			p=b["path"]
			if p is None:p=b["path"]=Kit.data_path(aC)
			return p
		def g(now,key,step):
			t=b[key]
			if now>=t or t-now>step:b[key]=now+step;return True
			return False
		def an(text):return str(text or "").replace("|","/").replace("\n"," ").replace("\r"," ").strip()
		def ao(ev,short=False):
			c,d=ev["lx"],ev["ly"]
			if not(c or d):return "at "+Kit.veil("xy","%d,%d"%(ev["x"],ev["y"]))
			a,b=ev["x"]-c,ev["y"]-d;e=max(abs(a),abs(b))
			if e==0:return "at the lookout"
			if short:return "%d %s"%(e,Kit.compass(a,b))
			return Kit.where_text(a,b)+" of the lookout"
		def h(serial,name,noto,x,y,facet,count,lx,ly,pinged=False):s="%.2f|%d|%s|%s|%d|%d|%d|%d|%d|%d|%d|%d\n"%(time.time(),serial,an(name),an(noto),x,y,facet,count,lx,ly,b["me"],1 if pinged else 0);return s.encode("utf-8")
		def j(data):
			a=b["outbox"];a.append(data)
			if len(a)>Y:del a[:-Y]
		def G(raw):
			try:
				s=raw.decode("utf-8","replace").strip()
				if not s:return
				p=s.split("|")
				if len(p)<8:return
				a={"t":float(p[0]),"key":p[0],"serial":int(p[1]),"name":p[2],"noto":p[3],"x":int(p[4]),"y":int(p[5]),"facet":int(p[6]),"count":int(p[7]),"lx":int(p[8])if len(p)>8 else 0,"ly":int(p[9])if len(p)>9 else 0,"from":int(p[10])if len(p)>10 else 0,"pinged":len(p)>11 and p[11]=="1"}
				if not 0.<a["t"]<1e11:return
				return a
			except Exception:return
		def ap():
			a=b["outbox"];n=len(a);d=t()
			try:
				with open(d,"ab")as f:f.write(b"".join(a[:n]))
			except Exception:b["write_next"]=time.time()+D;return
			del a[:n]
			try:e=os.path.getsize(d)
			except Exception:return
			if e>(R if c["watch"]else 4*R):aP(d)
		def aP(path):
			with Kit.quiet:
				with open(path,"rb")as h:a=h.read()
				f=a.rfind(b"\n")+1;a=a[:f];g=[k for k in a.split(b"\n")if k.strip()];b=g[-V:];c=set()
				for d in reversed(g[:-V]):
					if b"|listen|"in d and len(c)<Z:
						e=G(d)
						if e is not None and e["from"]not in c:c.add(e["from"]);b.insert(0,d)
				def i():
					with open(path,"rb")as a:a.seek(f);return a.read()
				Kit.write_safe(path,b"\n".join(b)+(b"\n"if b else b""),tail=i)
		def aQ(path):
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
		def aR(now):
			e=aQ(t())
			if not e:return
			g=b["me"];c=b["seen"];d=b["inbox"]
			for h in e:
				a=G(h)
				if a is None or a["from"]==g or a["noto"]=="listen":continue
				k=(a["key"],a["serial"],a["from"])
				if k in c:continue
				f=now-a["t"]
				if f<-5. or(a["serial"]and f>Q):continue
				c[k]=a["t"];d.append(a)
			if len(c)>E:
				i=now-4*Q
				for k in[m for m,n in c.items()if n<i]:del c[k]
				if len(c)>E:j=sorted(c.items(),key=lambda a:a[1])[-(E//2):];c.clear();c.update(j)
			if len(d)>100:del d[:-100]
		def aS(now):
			c=t()
			try:
				d=os.path.getsize(c)
				with open(c,"rb")as e:
					if d>f:e.seek(d-f)
					i=e.read(f)
			except Exception:return
			g={}
			for h in i.split(b"\n"):
				if b"|listen|"not in h:continue
				a=G(h)
				if a is not None and a["noto"]=="listen"and a["from"]and-5.<=now-a["t"]<=aJ:g[a["from"]]=a["t"]
			b["listeners"]=g
		def aT(m,serial):
			if m.IsRenamable:return
			a=Kit.noto_name(m)
			if a in("invulnerable","ally"):return
			if not(m.IsHuman or m.IsGargoyle):return
			if API.IsFriend(serial):return
			if ai.search(str(m.Name or "")):return
			return a
		def aU(now):
			p=B()
			if p is None:return
			t=int(p.Serial);k,l=int(p.X),int(p.Y);f=int(API.GetMap());b["me"],b["facet"]=t,f;A=M(c["range"]);u=set(int(be)for be in(API.GetPartyMemberSerials()or()));v=HOST.services.get("ultima.classify");C=b["listeners"];o=[]
			for m in A:
				try:
					if m is None:continue
					a=int(m.Serial)
					if a==t or a in u or a in C:continue
					if v is not None:
						r=v(m,u)
						if r is None or r[0]=="friend"or r[3]:continue
						d=r[2]
					else:
						if m.IsDead:continue
						d=aT(m,a)
						if d is None:continue
					if API.OnIgnoreList(a):continue
					o.append((a,m,d))
				except Exception:continue
			e=b["present"];s=[]
			for a,m,d in o:
				w=e.get(a)
				if w is None or now-w>O:s.append((a,m,d))
				e[a]=now
			if len(e)>len(o):
				for D in[bf for bf,bg in e.items()if not 0<=now-bg<=O]:del e[D]
				if len(e)>aK:e.clear()
			n=len(o)
			if n!=b["in_range"]:b["in_range"]=n;b["dirty"]=True
			E=c["ping"]and HOST.services.get("pings.send")is not None;i=[]
			for a,m,d in s:
				try:q,x,y=str(m.Name or "")or "(unknown)",int(m.X),int(m.Y)
				except Exception:continue
				z=E and len(b["pings"])<8;j(h(a,q,d,x,y,f,n,k,l,z))
				if z:b["pings"].append([x,y,f,"Lookout: "+q,now+ab])
				F={"t":now,"serial":a,"name":q,"noto":d,"x":x,"y":y,"facet":f,"count":n,"lx":k,"ly":l,"src":"here"};aq(F);i.append("%s (%s)"%(q,J.get(d,d)))
			if i:aj("spotted %s, %s in range."%(", ".join(i[:4])+(" and %d more"%(len(i)-4)if len(i)>4 else ""),Kit.count(n,"player")))
			if s or g(now,"hb_next",P):b["hb_next"]=now+P;j(h(0,"","watch",k,l,f,n,k,l))
		def aV(now):
			a=b["pings"]
			if not a or(now<b["ping_next"]and b["ping_next"]-now<=ac):return
			d=HOST.services.get("pings.send")
			if d is None or not c["ping"]:del a[:];return
			x,y,m,f,g=a[0]
			if not 0<=g-now<=ab:a.pop(0);return
			try:e=d(x,y,m,"danger",f)
			except Exception:e=True
			if e:a.pop(0)
			else:b["ping_next"]=now+ac
		def aW():
			b["present"].clear();b["in_range"]=0;del b["pings"][:]
			if b["me"]:j(h(0,"","off",0,0,b["facet"],0,0,0))
			b["dirty"]=True
		def aq(ev):a=b["recent"];a.insert(0,ev);del a[aF:];b["dirty"]=True
		def aX(ev,now):
			a=b["watchers"];w=a.get(ev["from"])
			if w is None:
				if len(a)>=Z:del a[min(a,key=lambda k:a[k]["t"])]
				w=a[ev["from"]]={"t":0.,"told":False}
			if ev["t"]<w["t"]:return
			w.update({"t":ev["t"],"state":ev["noto"],"x":ev["x"],"y":ev["y"],"facet":ev["facet"],"count":ev["count"]});w["told"]=ev["noto"]!="watch"or not-5.<=now-ev["t"]<=q;b["dirty"]=True
		def ar(ev,name,here):
			a=ev["noto"];b="%s (%s)%s, %s"%(name,J.get(a,a),(", %d players"%ev["count"])if ev["count"]>1 else "",ao(ev))
			if ev["facet"]!=here and here>=0:b+=" in "+Kit.facet_name(ev["facet"])
			return b
		def at(a):return ar(a[0],o(a[0]["name"],a[0]["serial"]),a[2])
		def aY(ev):
			d=ar(ev,ev["name"],b["facet"]);a=None
			if c["ping"]and not ev["pinged"]and ev["facet"]==b["facet"]and HOST.services.get("pings.send")is not None:a=(ev["x"],ev["y"])
			T(ad,d,level="alarm",ping=a,who=ev["serial"],name=ev["name"]);b["own_alarm"]=(ev,time.time(),b["facet"]);ev["src"]="lookout";aq(ev)
		def aZ(now):
			d=b["inbox"]
			if d:
				f,b["inbox"]=d,[]
				for a in f:
					if a["serial"]:aY(a)
					else:aX(a,now)
			if not c["lost"]:return
			for g,w in b["watchers"].items():
				if w["told"]or w.get("state")!="watch":continue
				e=now-w["t"]
				if e>q:w["told"]=True;b["dirty"]=True;T(ae,"Lookout quiet for %d s"%int(e),level="warn",who=g)
		def a_(i):
			def a():
				b=d["rows"]
				if i>=len(b):return
				r=b[i];a=r["ev"]
				if r["prev"]is not None and time.time()-r["at"]<=.15:a=r["prev"]
				if a is None:return
				if L():F(("follow",a["serial"]))();return
				F(("arrow",a["x"],a["y"],a["facet"]))()
			return a
		def au():return Kit.MARGIN+30+Kit.GAP
		I=58
		def u(n=z):return au()+I+Kit.GAP+30+n*p+6+Kit.MARGIN
		def av():
			f=e.zone_slot(W,u(1));w,j=f if f else(W,u());n=e.rows(p,u(0),z)if f else z;g,o,d=e.begin(w,j);M=Kit.MARGIN;k=[]
			if not b["minimized"]:
				a=w-2*M;e.frame(g);d["info_w"]=a-196;c=au();Kit.add_section(g,M,c,a,I);l=w-M-12-35-Kit.text_w("Clear");Kit.art_button(g,o,"clear",Kit.ART_CLOSE,l,c+28,"Clear","Clear the list, alarm line and tracking arrow",on_click=F("clear"));d["watch"]=Kit.add_label(g,"",M+12,c+9,Kit.HUE_INFO);d["listen"]=Kit.add_label(g,"",M+12,c+32,Kit.HUE_INFO);d["tw"]=(a-24,l-8-(M+12));h=c+I+Kit.GAP;Kit.add_section(g,M,h,a,j-h-M,"SPOTTED  (newest first)")
				for m in range(n):i=h+28+m*p;r={"name":Kit.add_label(g,"",M+12,i+2,Kit.HUE_TEXT),"info":Kit.add_label(g,"",M+12+180,i+2,Kit.HUE_INFO),"ev":None,"prev":None,"at":0.,"tip":None,"shown":True};r["hit"]=Kit.catcher(g,M+6,i,a-12,p,a_(m),"");k.append(r)
			e.end(g,{"rows":k});b["dirty"]=True;ay(time.time())
		e=Kit.Window(az,l,b,d,av,aA,aB,(220,220),(N,aD),aE,ah,lock=True,clear={"rows":[]})
		def aw():
			if not c["watch"]:return "off",Kit.HUE_INFO
			n=b["in_range"]
			if n:return "%d tiles, %s in range"%(c["range"],Kit.count(n,"player")),Kit.HUE_BAD
			return "%d tiles, all clear"%c["range"],Kit.HUE_GOOD
		def ax(now):
			if not c["listen"]:return "off",Kit.HUE_INFO
			a=None
			for w in b["watchers"].values():
				if a is None or w["t"]>a["t"]:a=w
			if a is None:
				if b["file"]=="busy":return "the feed is busy, trying again",Kit.HUE_INFO
				return "no lookout heard yet",Kit.HUE_INFO
			d=Kit.ago(now-a["t"],Kit.AGO_SHORT)
			if a.get("state")=="off":return "the lookout stopped %s ago"%d,Kit.HUE_INFO
			if not-5.<=now-a["t"]<=q:return "the lookout has been quiet for %s"%d,Kit.HUE_BAD
			n=a.get("count",0);e=Kit.veil("xy","%d,%d"%(a.get("x",0),a.get("y",0)))
			if n:return "the lookout at %s sees %s"%(e,Kit.count(n,"player")),Kit.HUE_BAD
			return "the lookout at %s, all clear"%e,Kit.HUE_GOOD
		def a0(now):
			a=b["own_alarm"]
			if a is not None and 0<=now-a[1]<=af:d,e=at(a),Kit.HUE_BAD
			elif c["listen"]:d,e=ax(now)
			else:d,e=aw()
			return "%s: %s"%(l,d),e
		def a1(r,ev,now):
			if ev is not r["ev"]:r["prev"],r["ev"],r["at"]=r["ev"],ev,now
			if ev is None:
				if r["shown"]:Kit.set_text(r["name"],"");Kit.set_text(r["info"],"");Kit.set(r["hit"],"IsVisible",False);r["shown"]=False
				return
			if not r["shown"]:Kit.set(r["hit"],"IsVisible",True);r["shown"]=True
			a=ev["noto"];Kit.set_text(r["name"],Kit.fit("%s (%s)"%(H(ev["name"],ev["serial"],a),J.get(a,a)),172),Kit.cb_hue(a,aa.get(a,Kit.HUE_TEXT)));c="lookout"if ev.get("src")=="lookout"else "here";f=Kit.veil("place",ao(ev,True)if c=="lookout"else "%d,%d"%(ev["x"],ev["y"]));Kit.set_text(r["info"],Kit.fit("%s, %s ago (%s)"%(f,Kit.ago(now-ev["t"],Kit.AGO_SHORT),c),d["c"]["info_w"]));e="%s (%s), seen %s at %s%s. %s"%(o(ev["name"],ev["serial"]),J.get(a,a),"by the lookout"if c=="lookout"else "here",Kit.veil("xy","%d,%d"%(ev["x"],ev["y"])),""if ev["facet"]==b["facet"]else " in "+Kit.facet_name(ev["facet"]),aN)
			if e!=r["tip"]:r["tip"]=e;Kit.with_tip(r["hit"],e)
		def ay(now):
			k=d["g"]
			if k is None or(b["minimized"]and b["docked"]):return
			e=d["c"]
			if b["minimized"]:a,c=a0(now);Kit.set_text(e["status"],Kit.fit(a,N-90),c);return
			i=e["tw"];a,c=aw();Kit.set_text(e["watch"],Kit.fit("Watch: "+a,i[0]),c);a,c=ax(now);f=b["own_alarm"]
			if f is not None and 0<=now-f[1]<=af:a,c=at(f),Kit.HUE_BAD
			else:a="Listen: "+a
			Kit.set_text(e["listen"],Kit.fit(a,i[1]),c);g=b["recent"];h=d["rows"]
			for j,r in enumerate(h):a1(r,g[j]if j<len(g)else None,now)
			if not g and h:Kit.set_text(h[0]["name"],"No one spotted yet.",Kit.HUE_INFO)
		def a2(x,y,m):
			a=b["facet"];c=b["arrow"];API.TrackingArrow(-1,-1,s);b["arrow"]=None
			if c==(x,y,m):return
			if a>=0 and m!=a:aj("that spot is in %s."%Kit.facet_name(m));return
			API.TrackingArrow(x,y,s);b["arrow"]=(x,y,m)
		def a3(action):b["recent"]=[];b["own_alarm"]=None;Kit.drop_arrow(b,s);b["dirty"]=True
		a4={"clear":a3,"follow":lambda action:S(action[1],l),"arrow":lambda action:a2(action[1],action[2],action[3])}
		def a5(w):return(("WATCH AND LISTEN  (two clients, one TazUO folder)",(("check","watch","Watch: this client is the lookout","Park it hidden and still; it reports every player in range to the other client (not party, friends or guild)"),("check","listen","Listen: this client gets the alarms","Alarm for each player a lookout reports (sound: Settings > Alerts)"),("slider","range","Watch range:","Watch range in tiles (%d-%d)"%(A,C),A,C,{"ldy":6,"sdy":4,"lw":98,"sw":160,"ugap":10,"vfmt":"%d tiles","h":32}),("check","ping","Danger ping on the map where a player is spotted","Needs World Map > Map Pings; guildmates see it too"),("check","lost","Warn when the lookout is quiet for %d s"%int(q),"Its client closed, crashed or lost the connection")),{"top":32,"pad":4}),)
		def a6(old,new):
			for k in("watch","listen","ping","lost"):
				if new[k]!=old[k]:a7(k,new[k])
			b["dirty"]=True
		def a7(k,on):
			if k=="watch":
				if on:b["next_scan"]=b["hb_next"]=b["listeners_next"]=0.
				else:aW()
			elif k=="listen":
				if on:b["listen_next"]=b["announce_next"]=0.
				else:b["inbox"]=[]
			elif k=="ping"and not on:del b["pings"][:]
			b["refresh_at"]=time.time()
		v=Kit.Page(c,a5,am,a6);al()
		def a8():b.update(ag(),minimized=e.start_min());al();p=API.Player;b["me"]=int(p.Serial)if p is not None else 0;b["facet"]=int(API.GetMap());t();U(ad,"Lookout spotted a player",aL);U(ae,"Lookout went quiet",aM);av();e.dock(fit=True,min=(W,u(1)))
		def a9():
			if d["g"]is None:return
			if Kit.closed(d):return
			while b["queue"]:
				f=b["queue"].pop(0)
				if e.action(f):continue
				h=a4.get(f[0]if isinstance(f,tuple)else f)
				if h is not None:h(f)
			a=time.time()
			if c["watch"]:
				if g(a,"next_scan",aG):aU(a)
				aV(a)
			elif c["listen"]and g(a,"next_scan",1.):
				p=API.Player
				if p is not None:b["me"]=int(p.Serial);b["facet"]=int(API.GetMap())
			if c["listen"]:aZ(a)
			if b["dirty"]or g(a,"refresh_at",1.):b["dirty"]=False;ay(a)
		def ba():
			if b["shutting"]:return
			a=time.time()
			if c["listen"]and b["me"]and g(a,"announce_next",aI):j(h(0,"","listen",0,0,b["facet"],0,0,0))
			if b["outbox"]and(a>=b["write_next"]or b["write_next"]-a>D):ap()
			if c["watch"]and g(a,"listeners_next",X):aS(a)
			if c["listen"]and b["me"]and g(a,"listen_next",aH):aR(a)
		def bb():
			if b["shutting"]:return False
			a=time.time()
			if c["listen"]and b["me"]:return True
			if b["outbox"]and not 0<b["write_next"]-a<=D:return True
			return bool(c["watch"])and not 0<b["listeners_next"]-a<=X
		def bc():
			b["shutting"]=True
			if c["watch"]and b["me"]:j(h(0,"","off",0,0,b["facet"],0,0,0));ap()
			Kit.drop_arrow(b,s);am();ah.close()
		return{"start":a8,"tick":a9,"stop":bc,"client_tick":True,"config_height":v.height,"build_config":v.build,"poll_config":v.poll,"config_closed":v.closed,"thread_tick":ba,"thread_wanted":bb}
	def aB():
		J="ultima.overview";g="Overview";q="UltimaTracker_overview";K="UltimaTracker_overview_pos";N="UltimaTracker_overview_min";W=390;O=(260,46);P=5365;Q=24;n=66;s=60;t=.5;u=1.;T=1.;U=8198;o=50;V="#3AB04A";X="#202020";Y="Alt+click: auto-follow (again to stop)";f=(("players","Players","player"),("monsters","Monsters","monster"),("pets","Pets","pet"),("corpses","Corpses","corpse"));Z=("distance","HP","name");ab=("distance","name");v={"tab":(0,3),"players":(0,2),"monsters":(0,2),"pets":(0,2),"corpses":(0,1),"range":(4,24),"rows":(3,20)};b={"tab":0,"players":0,"monsters":0,"pets":0,"corpses":0,"range":18,"rows":8};ac=dict(b);a={"minimized":False,"shutting":False,"docked":False,"queue":[],"lists":{},"data_at":0.,"corpse_at":0.,"corpses":[]};c={"g":None,"c":{},"store":({},{}),"rows":[]};x,h,aw=Kit.basics(a,g)
		def ae():Kit.kv_load(q,"|",b,v)
		def k():Kit.kv_save(q,"|",b,sorted(ac),v)
		def y(tab):return ab if tab==3 else Z
		def l(tab):o=y(tab);return o[min(b[f[tab][0]],len(o)-1)]
		def A():return Kit.pitch(Q)
		def C():return Kit.MARGIN+30+Kit.GAP+n+Kit.GAP+16+Kit.MARGIN
		def E():return W,C()+A()
		def af(i):
			def a(*b):
				a=c["rows"]
				if i>=len(a)or not L():return
				r=a[i];v=r["prev"]if r["prev"]and time.time()-r["changed"]<Kit.TWICE else r["val"]
				if v and v[1]:h(("follow",v[0]))()
			return a
		def p():
			c,q=A(),C();z=d.zone_slot(*E());s=d.rows(c,q,b["rows"])if z else b["rows"];w,t=z if z else(W,q+s*c);g,u,i=d.begin(w,t);v=[]
			if not a["minimized"]:
				d.frame(g);M=Kit.MARGIN;e=w-2*M;y=M+30+Kit.GAP;x=b["tab"];Kit.add_section(g,M,y,e,n);Kit.buttons(g,u,M+8,y+6,[("tab%d"%aD,Kit.ART_PAGE,aE[1],"Show %s in range"%aE[1].lower(),h(("tab",aD)),Kit.HUE_TITLE if aD==x else None)for aD,aE in enumerate(f)],6);i["sort"]=Kit.art_button(g,u,"sort",Kit.ART_PAGE,M+8,y+36,"Sort: "+l(x),"Order of this list (again for the next)",on_click=h("sort"));i["count"]=Kit.add_label(g,"",M+e-12-Kit.text_w("60 in range"),y+40,Kit.HUE_INFO);j=y+n+Kit.GAP;Kit.add_section(g,M,j,e,t-j-M);B=M+e-10-Kit.text_w("24 tiles");k=B-8-o;D=k-6-Kit.text_w("100%");i["nw"]=D-6-(M+10)
				for H in range(s):m=j+8+H*c;p=m+max(2,(c-16)//2);I=m+c//2-3;r={"name":Kit.add_label(g,"",M+10,p,Kit.HUE_TEXT),"hp":Kit.add_label(g,"",D,p,Kit.HUE_INFO),"back":Kit.inert(G.CreateGumpColorBox(.8,X)),"fill":Kit.inert(G.CreateGumpColorBox(.95,V)),"dist":Kit.add_label(g,"",B,p,Kit.HUE_INFO),"val":None,"prev":None,"changed":0.,"fw":-1,"bar":True,"on":True};r["back"].SetRect(k,I,o,6);r["fill"].SetRect(k,I,0,6);g.Add(r["back"]);g.Add(r["fill"]);r["hit"]=Kit.catcher(g,M+6,m,e-12,c,af(H),Y);v.append(r)
			d.end(g,{"rows":v});F()
		d=Kit.Window(J,g,a,c,p,K,N,(W,300),O,P,x,clear={"rows":[]})
		def F():
			d=c["c"];e=b["tab"]
			if "status"in d:Kit.set_text(d["status"],"%s: %s"%(g,f[e][1]));return
			if "count"not in d:return
			h=a["lists"].get(f[e][0],());j=f[e][2];k="%s in range"%Kit.count(len(h),j);Kit.set_text(d["count"],k);l=c["rows"];m=time.time();n=d["nw"]
			for i,r in enumerate(l):o=""if i or h else "No %ss in range."%j;ag(r,h[i]if i<len(h)else None,e,n,m,o)
		def H(r,pct):
			a=pct>=0
			if a!=r["bar"]:r["bar"]=a;Kit.set(r["back"],"IsVisible",a);Kit.set(r["fill"],"IsVisible",a)
			b=int(round(o*min(100,pct)/100.))if a else 0
			if b!=r["fw"]:r["fw"]=b;r["fill"].SetWidth(b)
		def ag(r,e,tab,nw,now,blank):
			Kit.row_set(r,(e[0],tab!=3)if e else None,now);c=e is not None and tab!=3
			if c!=r["on"]:r["on"]=c;Kit.set(r["hit"],"IsVisible",c)
			if e is None:Kit.set_text(r["name"],blank,Kit.HUE_INFO);Kit.set_text(r["hp"],"");Kit.set_text(r["dist"],"");H(r,-1);return
			i,a,d,j,b,k,l,m,f=e
			if tab==0:a=Kit.veil("name",a,i)
			elif tab==3 and Kit.streamer:a="Corpse"
			g=Kit.noto_mark(d)if tab<3 else "";h=Kit.hp_mark(k,l,m)if tab<3 else "";n=(g+" "if g else "")+a+("  "+h if h else "");o=Kit.cb_hue(d,aa.get(d,Kit.HUE_TEXT))if tab<3 else Kit.HUE_TEXT;Kit.set_text(r["name"],Kit.fit(n,nw),o);Kit.set_text(r["hp"],""if tab==3 else("dead"if f else("--"if b is None else "%d%%"%b)));Kit.set_text(r["dist"],Kit.count(j,"tile"));H(r,-1 if tab==3 or b is None or f else b)
		def ah(e):return e[3],e[1].lower()
		def ai(e):return(101 if e[4]is None else e[4]),e[1].lower()
		def aj(e):return e[1].lower(),e[3]
		I={"distance":ah,"HP":ai,"name":aj}
		def ak(now):
			n=B()
			if n is None or b["tab"]==3:a["lists"]={"corpses":a["corpses"]};return
			if not 0.<=now-D["scan_at"]<=u:D["party"]=set(API.GetPartyMemberSerials()or())
			an(now);o=b["range"];w=n.Serial;d=None;e={"players":[],"monsters":[],"pets":[]};p=HOST.services.get("pets.list")
			if p is not None:
				try:
					q=p(distance=o)
					if q is not None:d=set(int(G)for G in q)
				except Exception:d=None
			for m in M(o):
				try:
					g=m.Serial
					if g==w:continue
					x,r=R(m,"Hits"),R(m,"HitsMax");i=j(m,"IsDead")
					if j(m,"IsRenamable")if d is None else int(g)in d:k,h,c="pets",Kit.noto_name(m),str(m.Name or "")
					else:
						t=ad(m,g)
						if t is not None:
							h,i,c=t;k="players"
							if c and c.lower()in z:continue
						else:
							h=Kit.noto_name(m)
							if h=="invulnerable":continue
							k,c="monsters",str(m.Name or "")
					e[k].append((g,c or "(unknown)",h,int(m.Distance),int(round(100.*x/r))if r>0 else None,j(m,"IsPoisoned"),j(m,"IsParalyzed"),j(m,"IsYellowHits")and not i,i))
				except Exception:continue
			for y,A in enumerate(f[:3]):v=e[A[0]];v.sort(key=I[l(y)]);del v[s:]
			e["corpses"]=a["corpses"];a["lists"]=e
		def al(now):
			a["corpse_at"]=now;c=[]
			try:e=API.GetItemsOnGround(b["range"],U)or()
			except Exception:e=()
			for d in e:
				try:c.append((int(d.Serial),str(d.Name or "")or "a corpse",None,int(d.Distance),None,False,False,False,False))
				except Exception:continue
			c.sort(key=I[l(3)]);del c[s:];a["corpses"]=c
		def am(action):
			if action[1]==b["tab"]:return
			b["tab"]=action[1];k();a["data_at"]=a["corpse_at"]=0.;p()
		def ao(action):
			d=b["tab"];e=f[d][0];o=y(d);b[e]=(min(b[e],len(o)-1)+1)%len(o);k();a["data_at"]=0.
			if d==3:a["corpse_at"]=0.
			if "sort"in c["c"]:Kit.set_text(c["c"]["sort"],"Sort: "+l(d))
		ap={"tab":am,"sort":ao,"follow":lambda action:S(action[1],g)}
		def aq(w):return(("LIST",(("slider","range","Range:","Overview range in tiles (4-24)",4,24,{"unit":"tiles"}),("num","rows","Rows:","Rows shown outside a zone (3-20)",None,3,20))),)
		def ar(old,new):
			a["data_at"]=a["corpse_at"]=0.
			if new["rows"]!=old["rows"]and c["g"]is not None:h.add("redraw")
		m=Kit.Page(b,aq,k,ar)
		def at():a.update({"shutting":False,"docked":False,"queue":[],"lists":{},"data_at":0.,"corpse_at":0.,"corpses":[],"minimized":d.start_min()});ae();p();d.dock(fit=True,min=E)
		def au():
			q=a["queue"]
			while q:
				f=q.pop(0)
				if not d.action(f):ap[f[0]if isinstance(f,tuple)else f](f)
			if c["g"]is None or Kit.closed(c)or a["minimized"]or a["docked"]:return
			e=time.time()
			if b["tab"]==3 and not 0.<=e-a["corpse_at"]<T:al(e)
			g=e-a["data_at"]
			if 0.<=g<t or(0.<=g<u and HOST._mob_pid!=HOST.pass_id and 0.<=e-HOST._mob_at<t):return
			a["data_at"]=e;ak(e);F()
		def av():a["shutting"]=True;k();x.close()
		return{"start":at,"tick":au,"stop":av,"client_tick":True,"config_height":m.height,"build_config":m.build,"poll_config":m.poll,"config_closed":m.closed}
	aC=(("tracker",az,.05,"ultima"),("lookout",aA,.1,"lookout"),("overview",aB,.1));return PartSet(ar,at,aC).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("ultima","Ultima Tracker","Friends, foes and neutrals near you",_module_ultima,.05,category="The world",parts=(("tracker","Tracker","Trackers and combat bars",True,("ultima",)),("lookout","Lookout","A second client keeps watch",False,("lookout",)),("overview","Overview","Players, monsters, pets and corpses in tabs",False,(),True),),aliases=('Combat Bars','Lookout','foe','sightings','trackers','second client'))
