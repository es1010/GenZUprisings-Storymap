# -*- coding: utf-8 -*-
"""
Paragraphes d'explication de la StoryMap v2 (3 phrases au plus : déclencheur, déroulement, issue), FR puis EN court.
Clé = colonne « ville » de power/mouvements_genz.csv.
Sources : power/liste_gen_z_protests.xlsx (notes d'Estelle) et faits largement documentés.
INCERTAINS = textes qui reposent surtout sur les notes d'Estelle (faits postérieurs à mi-2026 ou peu couverts) : à relire.
"""

EXPLICATIONS = {
    # ---------------------------------------------------------------- précurseurs
    "Taipei": (
        "Le Kuomintang fait passer sans vrai débat un accord de libre-échange des services avec la Chine. "
        "Des étudiants occupent le Parlement pendant 24 jours, soutenus par des centaines de milliers de manifestants. "
        "L'accord n'a jamais été ratifié.",
        "Students occupied parliament for 24 days; the trade pact with China was never ratified."),
    "Hong Kong": (
        "Pékin impose un filtrage des candidats à l'élection du chef de l'exécutif au lieu d'un vrai suffrage universel. "
        "Étudiants et lycéens occupent les grands carrefours pendant 79 jours, en se protégeant des gaz lacrymogènes avec des parapluies. "
        "Les campements sont évacués en décembre 2014 sans aucune concession.",
        "A 79-day occupation for universal suffrage, cleared without concessions."),
    "Addis-Abeba": (
        "En 2014, le plan d'extension d'Addis-Abeba sur les terres oromo lance une contestation portée par la jeunesse oromo, les Qeerroo. "
        "Malgré une répression meurtrière et l'état d'urgence, grèves et boycotts durent jusqu'en 2018. "
        "Le Premier ministre Hailemariam Desalegn démissionne en février 2018 et Abiy Ahmed lui succède.",
        "Years of Oromo youth protests forced the prime minister out in 2018."),
    "Stockholm": (
        "En août 2018, Greta Thunberg, 15 ans, fait grève de l'école devant le Parlement suédois contre l'inaction climatique. "
        "Le mouvement devient mondial, avec des millions de jeunes dans la rue le 20 septembre 2019. "
        "Il a pesé sur l'agenda politique, sans obtenir de changement à la hauteur de ses demandes.",
        "A one-girl school strike became a global youth climate movement."),
    "Khartoum": (
        "Le triplement du prix du pain, en décembre 2018, lance une révolte contre le régime d'Omar el-Béchir. "
        "Après des mois de manifestations et un sit-in devant le QG de l'armée, Béchir est renversé en avril 2019 et un accord de partage du pouvoir est signé en août. "
        "La transition est interrompue par le coup d'État militaire d'octobre 2021.",
        "Bread-price protests toppled al-Bashir in 2019; a 2021 coup ended the transition."),
    # ---------------------------------------------------------------- 1re vague numérique
    "Hong Kong 2019": (
        "Un projet de loi permettant les extraditions vers la Chine continentale fait descendre des foules immenses dans la rue en juin 2019. "
        "Le mouvement, sans leader, invente la tactique « Be water » ; le projet de loi est retiré en septembre 2019. "
        "La loi de sécurité nationale imposée par Pékin en juin 2020 met fin au mouvement.",
        "The extradition bill was withdrawn, but the 2020 national security law crushed the movement."),
    "Santiago": (
        "En octobre 2019, la hausse de 30 pesos du ticket de métro pousse des lycéens à sauter les tourniquets, puis tout le pays à se révolter contre les inégalités. "
        "Après des semaines de manifestations massives et une forte répression, le gouvernement accepte d'écrire une nouvelle constitution. "
        "Les deux projets de constitution sont ensuite rejetés par référendum, en 2022 et en 2023.",
        "Metro-fare protests won a constitutional process, but both drafts were rejected."),
    "Lagos": (
        "En octobre 2020, des vidéos de violences de l'unité policière SARS déclenchent une mobilisation organisée en ligne par de jeunes Nigérians. "
        "Le gouvernement annonce la dissolution de la SARS, mais le 20 octobre des soldats tirent sur les manifestants au péage de Lekki. "
        "Le mouvement s'arrête après cette fusillade.",
        "SARS was disbanded, but soldiers fired on protesters at the Lekki toll gate."),
    "Bangkok": (
        "En 2020, la dissolution d'un parti d'opposition populaire chez les jeunes lance des manifestations étudiantes contre le gouvernement issu de l'armée. "
        "Le mouvement ose réclamer une réforme de la monarchie, un tabou en Thaïlande. "
        "Les meneurs sont poursuivis, notamment pour lèse-majesté, et la mobilisation s'éteint fin 2021.",
        "Student protests demanding monarchy reform were stifled by prosecutions."),
    "Yangon": (
        "Le coup d'État militaire du 1er février 2021 déclenche une désobéissance civile massive, largement menée par la jeunesse. "
        "L'armée réprime dans le sang ; Kyal Sin, 19 ans, tuée avec son t-shirt « Everything will be OK », devient un symbole. "
        "Beaucoup de jeunes rejoignent ensuite la résistance armée et le pays bascule dans la guerre civile.",
        "Mass protests against the 2021 coup were crushed and turned into civil war."),
    "Téhéran": (
        "En septembre 2022, la mort de Mahsa Amini, 22 ans, après son arrestation par la police des mœurs, déclenche un soulèvement mené par des jeunes femmes. "
        "Les manifestantes coupent leurs cheveux et brûlent leur voile au cri de « Femme, Vie, Liberté ». "
        "La répression fait des centaines de morts et plusieurs manifestants sont exécutés.",
        "The uprising after Mahsa Amini's death was crushed, with executions."),
    "Colombo": (
        "En 2022, la faillite du Sri Lanka entraîne pénuries de carburant et de médicaments et coupures de courant. "
        "Le campement « GotaGoGama » réclame le départ du clan Rajapaksa ; en juillet, la foule envahit le palais présidentiel et se baigne dans sa piscine. "
        "Le président Gotabaya Rajapaksa fuit le pays et démissionne.",
        "Economic collapse led protesters to storm the palace; the president fled and resigned."),
    "Tbilissi 2023": (
        "En mars 2023, le parti au pouvoir fait voter en première lecture une loi sur les « agents de l'étranger » calquée sur la loi russe. "
        "Des milliers de jeunes manifestent devant le Parlement, drapeau européen à la main face aux canons à eau. "
        "Le gouvernement retire la loi au bout de quelques jours.",
        "Protests forced the withdrawal of the 'foreign agents' bill within days."),
    # ---------------------------------------------------------------- vague Gen Z
    "Nairobi": (
        "Le projet de loi de finances 2024 prévoit de nouvelles taxes alors que le chômage des jeunes est élevé. "
        "Organisés sur X et TikTok, sans parti ni leader, de jeunes Kényans manifestent et envahissent le Parlement le 25 juin 2024. "
        "Le président Ruto retire la loi, mais la répression fait des dizaines de morts.",
        "The finance bill was withdrawn after parliament was stormed; dozens were killed."),
    "Dacca": (
        "En juillet 2024, le rétablissement des quotas dans la fonction publique lance un mouvement étudiant. "
        "La répression, qui fait des centaines de morts dont Abu Sayed abattu bras en croix, transforme la contestation en soulèvement contre Sheikh Hasina. "
        "Hasina fuit en Inde le 5 août 2024 et Muhammad Yunus prend la tête d'un gouvernement intérimaire.",
        "Quota protests became an uprising; Sheikh Hasina fled on 5 August 2024."),
    "Belgrade": (
        "Le 1er novembre 2024, l'effondrement de l'auvent de la gare de Novi Sad (16 morts) est imputé à la corruption. "
        "Les étudiants occupent les universités et marchent dans tout le pays, avec 16 minutes de silence et la main rouge. "
        "En 2026, Aleksandar Vučić démissionne et la Liste étudiante arrive en tête des législatives anticipées du 25 octobre (résultats provisoires).",
        "Two years of student protests after the Novi Sad disaster ended with Vučić's resignation in 2026."),
    "Tbilissi": (
        "Fin novembre 2024, après des élections contestées, le gouvernement du Rêve géorgien suspend les négociations d'adhésion à l'Union européenne. "
        "Des manifestations ont lieu chaque soir devant le Parlement, avec drapeaux européens et feux d'artifice contre la police. "
        "Le pouvoir répond par des arrestations et des lois répressives ; le mouvement continue.",
        "Nightly pro-EU protests since November 2024 face arrests and repressive laws."),
    "Jakarta": (
        "Fin août 2025, les indemnités de logement accordées aux députés provoquent la colère d'une jeunesse confrontée à la vie chère. "
        "La mort d'un livreur, écrasé par un véhicule de police, embrase la contestation ; le drapeau One Piece en devient l'emblème. "
        "Le Parlement revient sur une partie des avantages des députés.",
        "Anger at MPs' perks, then a delivery rider's death, won partial concessions."),
    "Katmandou": (
        "Début septembre 2025, le gouvernement bloque 26 réseaux sociaux, sur fond de colère contre les « nepo kids », enfants de dirigeants qui étalent leur luxe. "
        "Le 8 septembre, la police tire sur la foule ; le lendemain, le Parlement est incendié et le Premier ministre K. P. Sharma Oli démissionne. "
        "Sushila Karki devient Première ministre intérimaire après une consultation des manifestants sur Discord.",
        "A social-media ban led to deadly protests; PM Oli resigned and an interim PM was picked via Discord."),
    "Manille": (
        "En 2025, des scandales de corruption dans les projets de lutte contre les inondations indignent les Philippins. "
        "La « Trillion Peso March » du 21 septembre rassemble des foules à Manille sous le drapeau One Piece, et certaines manifestations tournent à l'affrontement. "
        "Enquêtes et démissions suivent, sans régler le fond du problème.",
        "Flood-control corruption scandals brought mass protests, inquiries and resignations."),
    "Dili": (
        "En septembre 2025, des étudiants protestent contre l'achat de voitures neuves pour les députés et contre leurs pensions à vie. "
        "Après trois jours de manifestations, le Parlement renonce aux voitures et vote la fin des pensions à vie. "
        "C'est la victoire la plus rapide de la vague Gen Z.",
        "In three days students made MPs drop new cars and lifetime pensions."),
    "Antananarivo": (
        "Fin septembre 2025, les coupures d'eau et d'électricité à répétition mobilisent la jeunesse malgache. "
        "Le président Andry Rajoelina limoge son gouvernement, puis quitte le pays quand une unité d'élite de l'armée, le CAPSAT, se range du côté des manifestants. "
        "L'armée prend le pouvoir en octobre 2025, ce qui rend la victoire ambiguë.",
        "Water and power cuts sparked protests; Rajoelina fled and the army took over."),
    "Rabat": (
        "Fin septembre 2025, le collectif GenZ 212, né sur Discord, dénonce les milliards dépensés pour les stades du Mondial 2030 alors que les hôpitaux manquent de tout. "
        "Les manifestations sont réprimées : 3 morts et des centaines de personnes arrêtées. "
        "Le budget 2026 augmente nettement les crédits de la santé.",
        "Discord-organised protests over hospitals vs stadiums won a bigger health budget."),
    "Lima": (
        "À partir de septembre 2025, une réforme des retraites, l'insécurité et la corruption mobilisent la jeunesse péruvienne. "
        "La présidente Dina Boluarte est destituée par le Congrès en octobre 2025. "
        "Les manifestations continuent ensuite contre son successeur.",
        "Gen Z protests helped bring down President Boluarte in October 2025."),
    "Leh": (
        "Au Ladakh, la jeunesse réclame le statut d'État et des protections constitutionnelles, sur fond de chômage. "
        "Le 24 septembre 2025, la manifestation dégénère : le bureau local du BJP est incendié et la police tire, faisant 4 morts. "
        "Le militant Sonam Wangchuk est arrêté peu après.",
        "A statehood protest ended with four killed and activist Sonam Wangchuk arrested."),
    "Dar es Salaam": (
        "L'élection présidentielle du 29 octobre 2025, dont les principaux opposants sont écartés, fait descendre des jeunes dans la rue. "
        "Le pouvoir coupe Internet et réprime très durement ; le bilan, très lourd, reste contesté. "
        "Samia Suluhu Hassan est déclarée réélue avec près de 98 % des voix.",
        "Protests over a closed election met an internet blackout and a heavy, disputed toll."),
    "Mexico": (
        "L'assassinat de Carlos Manzo, maire d'Uruapan, et l'insécurité provoquent une « Marche de la génération Z » le 15 novembre 2025. "
        "La marche se termine par des affrontements devant le Palais national. "
        "La présidente Claudia Sheinbaum accuse l'opposition de l'avoir organisée et la mobilisation s'essouffle.",
        "A Gen Z march against insecurity ended in clashes and soon faded."),
    "Sofia": (
        "Fin novembre 2025, le projet de budget 2026, accusé de servir les réseaux de corruption, fait descendre la jeunesse dans la rue. "
        "Le gouvernement retire le budget, puis démissionne en décembre face à l'ampleur des manifestations.",
        "Budget protests made the government withdraw it, then resign."),
    # ---------------------------------------------------------------- 2026
    "Kampala": (
        "L'élection présidentielle de janvier 2026, organisée sous coupure d'Internet, provoque des manifestations de jeunes. "
        "Yoweri Museveni est déclaré réélu et la contestation est réprimée. "
        "Le principal opposant, Bobi Wine, part en exil.",
        "Protests over a disputed election were crushed; Museveni stayed in power."),
    "La Paz": (
        "En mai 2026, une grave pénurie de carburant entraîne des blocages routiers dans toute la Bolivie. "
        "La mobilisation se termine par un accord avec la centrale syndicale, la COB, et les blocages sont levés.",
        "Fuel-shortage blockades ended with a deal with the main union federation."),
    "Tirana": (
        "En mai 2026, un projet de complexe de luxe dans une lagune protégée, associé à Jared Kushner, lance la « révolution des flamants roses ». "
        "La contestation vise ensuite le Premier ministre Edi Rama et s'intensifie en octobre avec l'entrée des lycéens et des étudiants. "
        "Le mouvement est toujours en cours.",
        "Protests against a luxury resort in a protected lagoon grew into a movement against Edi Rama."),
    "New Delhi": (
        "En juin 2026, la fuite des sujets du concours de médecine NEET (environ 2 millions de candidats) indigne la jeunesse, d'autant qu'un juge traite les jeunes chômeurs de « cafards ». "
        "Les manifestants reprennent le cafard comme emblème et tapent sur des assiettes à Jantar Mantar. "
        "Le ministre de l'Éducation démissionne fin juillet et les revendications sont acceptées.",
        "A leaked medical entrance exam led to protests; the education minister resigned."),
    "Créteil": (
        "À la rentrée 2026, lycées délabrés, manque de professeurs et Parcoursup font naître un mouvement lycéen, parti de Mayotte puis de Créteil. "
        "Blocus et manifestations gagnent toute la France, au son de « The Hanging Tree » et sous le drapeau One Piece ; la répression entraîne des milliers de gardes à vue, surtout de mineurs. "
        "Le gouvernement envoie des remplaçants, mais le mouvement continue.",
        "A high-school movement over run-down schools spread across France; it is still ongoing."),
    "Bruxelles": (
        "En octobre 2026, des lycéens belges reprennent les blocus du modèle français pour dénoncer leurs conditions d'études et le coût des études. "
        "Les manifestations de Bruxelles et de Liège sont dispersées au gaz lacrymogène et aux canons à eau. "
        "Le mouvement est en cours.",
        "Belgian pupils copied the French school blockades; police dispersed them."),
    "Rome": (
        "Le « No Meloni Day » du 16 octobre 2026 réunit des lycéens contre la politique éducative du gouvernement Meloni. "
        "Des lycées sont occupés et des cortèges défilent à Rome, Turin, Milan et Bologne ; la police charge. "
        "Le mouvement continue, alors qu'un décret sécurité durcit les peines pour émeute.",
        "Italian pupils occupied schools against Meloni's education policy."),
    "Berlin": (
        "Le retour du service militaire, l'éducation et la vie chère mobilisent la jeunesse allemande, explicitement « sur le modèle français ». "
        "La journée nationale du 31 octobre 2026 rassemble des jeunes dans 23 villes et se termine par des affrontements et des centaines d'arrestations. "
        "Le mouvement est en cours.",
        "German youth protested against conscription, 'on the French model'."),
    "Athènes": (
        "À partir du 13 octobre 2026, des étudiants grecs campent devant le Parlement, place Syntagma, contre la hausse des loyers étudiants et le sous-financement des universités. "
        "Le mouvement est en cours.",
        "Greek students camp outside parliament over rents and university funding."),
    "Madrid": (
        "En septembre 2026, l'expulsion de Maricarmen, 87 ans, morte peu après, déclenche un mouvement pour le droit au logement. "
        "Un campement d'environ 1 250 tentes s'installe à la Puerta del Sol, en écho au 15-M de 2011. "
        "Le gouvernement adopte des décrets anti-expulsion et convoque des élections anticipées ; le mouvement est intergénérationnel.",
        "An elderly woman's eviction sparked a housing camp at Puerta del Sol."),
    # ---------------------------------------------------------------- cas limites
    "Paris": (
        "Lancé sur les réseaux sociaux, l'appel « Bloquons tout » du 10 septembre 2025 dénonce les économies budgétaires du gouvernement. "
        "Blocages et manifestations rassemblent toutes les générations, pas seulement la Gen Z. "
        "Le gouvernement Bayrou était tombé deux jours plus tôt, après avoir perdu un vote de confiance.",
        "An intergenerational 'block everything' day against budget cuts."),
    "Milan": (
        "En septembre et octobre 2025, des grèves générales pour Gaza, lancées par les syndicats, paralysent l'Italie. "
        "Elles rassemblent jusqu'à 2 millions de personnes selon les organisateurs. "
        "Les jeunes y sont nombreux, mais le mouvement est syndical.",
        "Union-led general strikes for Gaza, with many young people."),
    "New York": (
        "Au printemps 2024, des étudiants installent des campements sur les campus pour protester contre la guerre à Gaza, à partir de Columbia le 17 avril. "
        "Le mouvement gagne des dizaines d'universités aux États-Unis et ailleurs. "
        "Les campements sont démantelés par la police, avec des milliers d'arrestations.",
        "Campus encampments for Gaza were cleared, with thousands of arrests."),
    "Séoul": (
        "Le 3 décembre 2024, le président Yoon Suk-yeol proclame la loi martiale. "
        "Des foules, où les jeunes femmes sont très présentes, manifestent avec des bâtons lumineux de K-pop pour exiger sa destitution. "
        "Yoon est destitué par le Parlement, puis démis par la Cour constitutionnelle le 4 avril 2025.",
        "K-pop lightstick protests helped remove President Yoon after martial law."),
    "Téhéran 2025": (
        "Fin décembre 2025, l'effondrement du rial et la vie chère déclenchent des manifestations dans tout l'Iran. "
        "La contestation, durement réprimée, se poursuit ensuite dans un contexte de guerre. "
        "Elle touche toute la société et n'est pas spécifiquement générationnelle.",
        "Economic protests across Iran, harshly repressed and not specifically generational."),
    "Lomé": (
        "En juin 2025, des appels lancés en ligne dénoncent la réforme constitutionnelle qui permet à Faure Gnassingbé de rester au pouvoir sans limite de mandat, ainsi que la vie chère. "
        "Les manifestations de Lomé sont réprimées. "
        "Mouvement de moindre ampleur, d'où son classement en cas limite.",
        "Online-organised protests against Faure Gnassingbé's grip on power were repressed."),
    "Asunción": (
        "Le 28 septembre 2025, une « marche de la génération Z » dénonce la corruption et le népotisme au Paraguay. "
        "Elle est dispersée par la police, avec des arrestations. "
        "Mouvement de moindre ampleur, d'où son classement en cas limite.",
        "A Gen Z march against corruption was dispersed by police."),
    "Malé": (
        "En 2025, des manifestations aux Maldives visent le gouvernement et ses atteintes aux libertés. "
        "La mobilisation reste limitée. "
        "Mouvement de moindre ampleur, d'où son classement en cas limite.",
        "Small protests against the government; a borderline case."),
    "Douala": (
        "Après la présidentielle d'octobre 2025, qui donne un huitième mandat à Paul Biya, 92 ans, des partisans de l'opposant Issa Tchiroma contestent les résultats. "
        "Les manifestations, à Douala et ailleurs, sont réprimées et font plusieurs morts. "
        "La jeunesse y est très présente, mais le mouvement suit un leader d'opposition.",
        "Post-election protests behind an opposition leader were repressed."),
    "Muzaffarabad": (
        "Fin septembre 2025, le Comité d'action populaire lance une grève générale au Cachemire administré par le Pakistan, pour des revendications économiques et politiques. "
        "Les affrontements font plusieurs morts. "
        "Un accord avec le gouvernement pakistanais met fin au mouvement début octobre.",
        "A general strike in Pakistan-administered Kashmir ended with a deal."),
    "Dakar 2023": (
        "En juin 2023, la condamnation de l'opposant Ousmane Sonko à deux ans de prison déclenche des émeutes à Dakar et en Casamance. "
        "Les jeunes sont très présents et nombreux parmi les morts, mais ils suivent un parti d'opposition, le Pastef. "
        "Sonko devient Premier ministre en 2024, après la victoire de son camp à la présidentielle.",
        "Riots after Sonko's conviction, led by an opposition party rather than a youth movement."),
    "Nanterre 2023": (
        "Le 27 juin 2023, Nahel, 17 ans, est tué par un policier lors d'un contrôle routier à Nanterre. "
        "Plusieurs nuits d'émeutes touchent les banlieues de toute la France, avec des milliers d'interpellations, souvent de très jeunes. "
        "Ces émeutes, sans revendication organisée, sont classées en cas limite.",
        "Riots after a teenager was killed by police, without organised demands."),
}

# Textes qui reposent surtout sur les notes d'Estelle (xlsx) ou sur des faits peu couverts : à relire avant publication.
INCERTAINS = ["Belgrade", "Kampala", "La Paz", "Tirana", "New Delhi", "Créteil", "Bruxelles", "Rome", "Berlin",
              "Athènes", "Madrid", "Téhéran 2025", "Lomé", "Asunción", "Malé", "Manille", "Jakarta"]
