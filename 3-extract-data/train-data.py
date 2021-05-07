TRAIN_DATA = [
    ("FM AMEMBASSY ANKARA \nTO SECSTATE WASHDC PRIORITY 9745 \nINFO AMCONSUL " +
    "ISTANBUL \nAMCONSUL ADANA ",
    {"entities": [
        (3, 19, "ORG"),
        (24, 48, "ORG"),
        (55, 77, "ORG"),
        (79, 93, "ORG")
    ]}),
    ("TAGS: PTER TU",
    {"entities": [
        (6, 10, "TAG"),
        (11, 13, "TAG")
    ]}),
    ("THE BEST-KNOWN TRANSNATIONAL TERRORIST GROUPS IN TURKEY ARE THE KURDISTAN " +
    "WORKERS' PARTY (PKK) AND THE REVOLUTIONARY PEOPLE'S LIBERATION PARTYLEFTIST " +
    "TERROR ORGANIZATIONS",
    {"entities": [
        (64, 88, "ORG"),
        (11, 13, "TAG")
    ]}),

    #09MOSCOW2542
    ("R 080612Z OCT 09\nFM AMEMBASSY MOSCOW\nTO RUEHC/SECSTATE WASHDC 5027\n" +
    "INFO RUCNCIS/CIS COLLECTIVE\nRUEHXD/MOSCOW POLITICAL COLLECTIVE\n" +
    "RHEHNSC/NSC WASHDC\nRUEAIIA/CIA WASHDC",
    {"entities": [
        (10, 16, "DATE"),
        (20, 36, "ORG"),
        (46, 61, "ORG"),
        (80, 94, "ORG"),
        (102, 129, "ORG"),
        (138, 148, "ORG"),
        (157, 167, "ORG")
    ]}),
    ("TAGS: PGOV KDEM PREL PHUM PINR KCOR RS\nSUBJECT: BELYKH FACES ROUGH YEAR " +
    "AHEAD IN KIROV",
    {"entities": [
        (6, 10, "TAG"),
        (11, 15, "TAG"),
        (16, 20, "TAG"),
        (21, 25, "TAG"),
        (26, 30, "TAG"),
        (31, 35, "TAG"),
        (36, 38, "TAG"),
        (49, 55, "PERSON"),
        (82, 87, "GPE")
    ]}),
    ("1. (C) Summary: Our September 23-25 visit to Kirov revealed a newly-settled" +
    " government slowly expanding its influence within the region.",
    {"entities": [
        (20, 32, "DATE"),
        (45, 50, "PERSON")
    ]}),
    ("Strict limitations placed on Governor Belykh and his staff by local" +
    " security services six months ago appear to have eased significantly, " +
    "and the new government remains moderately popular despite friction between " +
    "its youthful, moderate image and the conservative, paternalistic nature of " +
    "the general population.",
    {"entities": [
        (38, 44, "PERSON"),
        (86, 96, "DATE")
    ]}),
    ("Belykh must now make good on his promises to fight corruption, improve " +
    "efficiency in government and attract investment and economic growth over " +
    "the last nine months.",
    {"entities": [
        (0, 6, "PERSON"),
        (153, 164, "DATE")
    ]}),
    ("Despite being a former opposition figure, it appears that the priority" +
    " of Belykh's long-term agenda is delivering at least 60 percent of the " +
    "vote to United Russia in local elections 18 months from now. ",
    {"entities": [
        (74, 80, "PERSON"),
        (123, 133, "PERCENT"),
        (149, 162, "GPE"),
        (182, 191, "DATE")
    ]}),

    #06RIYADH5947
    ("P 261123Z JUL 06\nFM AMEMBASSY RIYADH\nTO RUEHC/SECSTATE WASHDC PRIORITY " +
    "0013\nINFO RUEHZM/GULF COOPERATION COUNCIL COLLECTIVE\nRUEHLO/AMEMBASSY " +
    "LONDON 2711\nRUEHFR/AMEMBASSY PARIS 0644",
    {"entities": [
        (10, 16, "DATE"),
        (20, 36, "ORG"),
        (46, 70, "ORG"),
        (88, 123, "ORG"),
        (131, 147, "ORG"),
        (160, 175, "ORG")
    ]}),
    ("TAGS: PGOVPHUM KIRF SA\nSUBJECT: SAG REMOVES SHI'A JUDGE IN QATIF",
    {"entities": [
        (6, 14, "TAG"),
        (15, 19, "TAG"),
        (20, 22, "TAG"),
        (59, 64, "GPE")
    ]}),
    ("The SAG removed Ghalib Al-Hammad as judge of the\nShi'a court in Qatif, " +
    "replacing him with associate judge\nSulaiman Abu Al-Makarem effective July 19.",
    {"entities": [
        (4, 7, "ORG"),
        (16, 32, "PERSON"),
        (49, 60, "NORP"),
        (64, 69, "GPE"),
        (106, 129, "PERSON"),
        (140, 147, "DATE")
    ]}),
    ("A third Shi'a contact, who is\ncloser to the SAG, said that the Vice Emir " +
    "of the Eastern\nProvince (EP) had made the decision to remove Al-Hammad\n" +
    "because he could not accept having a subordinate.",
    {"entities": [
        (8, 13, "NORP"),
        (44, 47, "ORG"),
        (63, 72, "PERSON"),
        (80, 96, "LOC"),
        (134, 143, "PERSON")
    ]}),

    # 09STATE82558
    ("O 072103Z AUG 09\nFM SECSTATE WASHDC\nTO RUEHON/AMCONSUL TORONTO IMMEDIATE" +
    " 0000\nINFO RUEHOT/AMEMBASSY OTTAWA IMMEDIATE 0000\nRUEHUNV/USMISSION " +
    "UNVIE VIENNA IMMEDIATE 0000\nRUEKJCS/SECDEF WASHINGTON DC IMMEDIATE\n" +
    "RUEAORC/US CUSTOMS AND BORDER PROTECTION WASHINGTON DC IMMEDIATE\n" +
    "RHMFIUU/NRC WASHINGTON DC IMMEDIATE\nRHMFISS/JOINT STAFF WASHINGTON DC " +
    "IMMEDIATE\nRHMCSUU/FBI WASHINGTON DC IMMEDIATE 0000\nRUETIAA/DIRNSA FT " +
    "GEORGE G MEADE MD IMMEDIATE\nRHMCSUU/DEPT OF ENERGY WASHINGTON DC " +
    "IMMEDIATE\nRUEAIIA/CIA WASHINGTON DC IMMEDIATE",
    {"entities": [
        (10, 16, "DATE"),
        (20, 35, "ORG"),
        (46, 62, "ORG"),
        (86, 106, "ORG"),
        (130, 152, "ORG"),
        (176, 196, "ORG"),
        (215, 261, "ORG"),
        (280, 297, "ORG"),
        (316, 341, "ORG"),
        (360, 377, "ORG"),
        (401, 428, "ORG"),
        (447, 485, "ORG"),
        (494, 511, "ORG"),
        (, , "ORG"),
        (, , "")
    ]}),
    ("REF: A. TORONTO 000173\nB. STATE 078415\nC. TORONTO 000163\nD. STATE " +
    "075002\nE. OTTAWA 000522\nF. STATE 69767",
    {"entities": [
        (8, 15, "GPE"),
        (42, 49, "GPE"),
        (76, 82, "GPE")
    ]}),
    ("Washington requests that ConGen\nToronto provide the Request for " +
    "Information in paragraph 4 to\nappropriate OPG officials for their " +
    "review by Monday, August\n10, 2009.",
    {"entities": [
        (0, 10, "GPE"),
        (25, 31, "ORG"),
        (32, 39, "GPE"),
        (106, 109, "ORG"),
        (140, 163, "DATE")
    ]}),
    ("The United States anticipates a current and ongoing\nneed of He-3 along with future He-3 OPG production.",
    {"entities": [
        (4, 17, "GPE"),
        (88, 91, "ORG")
    ]}),
]


The United States anticipates a current and ongoing\need of He-3 along with future He-3 OPG production.

#
