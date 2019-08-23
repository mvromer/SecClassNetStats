import matplotlib.pyplot as plt

packet = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

avg_packet_size = {
    "Wikipedia Cat (Standard Connection)": [ 1041.06, 1074.57, 1048.34, 1044.15, 1040.46, 1049.29, 1041.64, 1014.90, 1048.28, 1047.83 ],
    "Wikipedia Dog (Standard Connection)": [ 1034.28, 1050.95, 1070.87, 1062.96, 1084.95, 1069.40, 1065.31, 1063.77, 1060.95, 1066.20 ],
    "Wikipedia Egress (Standard Connection)": [ 1027.30, 1037.99, 978.26, 1016.57, 1005.72, 1046.33, 1050.48, 1036.98, 948.28, 1022.61 ],
    "MIT (Standard Connection)": [ 1271.13, 1303.48, 1315.24, 1302.46, 1296.75, 1281.85, 1310.76, 1300.64, 1283.65, 1290.54 ],
    "UNM (Standard Connection)": [ 1074.04, 1111.63, 1109.38, 1087.41, 1122.29, 1123.46, 1121.97, 1115.18, 1101.56, 1109.02 ],
    "CMU (Standard Connection)": [ 1062.87, 1056.62, 1088.40, 1100.30, 1088.84, 1071.32, 1095.37, 1068.06, 1085.86, 1092.50 ],
    "Berkeley (Standard Connection)": [ 986.91, 1025.75, 999.87, 1018.62, 1018.43, 1018.34, 1022.46, 1018.80, 1003.66, 1006.32 ],
    "UT Austin (Standard Connection)": [ 1299.64, 1309.04, 1300.72, 1298.36, 1286.16, 1290.18, 1298.75, 1310.13, 1296.29, 1295.05 ],
    "ASU (Standard Connection)": [ 1011.48, 1026.76, 1031.72, 1027.37, 1035.16, 1017.34, 1019.16, 1018.76, 1032.49, 1029.53 ],
    "UT Dallas (Standard Connection)": [ 1290.33, 1253.34, 1274.90, 1261.00, 1264.06, 1291.74, 1226.46, 1228.14, 1248.08, 1211.41 ],

    "Wikipedia Cat (VPN Connection)": [ 578.04, 602.32, 549.24, 582.62, 580.18, 525.32, 482.41, 592.65, 591.70, 580.20 ],
    "Wikipedia Dog (VPN Connection)": [ 595.25, 603.33, 617.22, 621.11, 610.49, 627.39, 628.08, 590.64, 589.95, 600.61 ],
    "Wikipedia Egress (VPN Connection)": [ 487.24, 614.82, 558.33, 408.68, 558.18, 518.01, 494.82, 431.59, 533.94, 538.77 ],
    "MIT (VPN Connection)": [ 686.06, 691.26, 697.72, 693.50, 691.62, 655.59, 620.09, 640.88, 701.62, 688.31 ],
    "UNM (VPN Connection)": [ 694.91, 707.52, 687.60, 655.64, 665.56, 668.75, 664.42, 737.55, 660.06, 677.23 ],
    "CMU (VPN Connection)": [ 584.30, 582.36, 660.06, 679.35, 582.25, 595.97, 633.79, 481.39, 652.30, 606.19 ],
    "Berkeley (VPN Connection)": [ 649.29, 648.11, 645.35, 661.91, 658.80, 661.41, 646.27, 660.79, 676.03, 664.50 ],
    "UT Austin (VPN Connection)": [ 675.07, 748.28, 626.98, 700.67, 671.27, 645.93, 689.36, 694.56, 700.81, 720.31 ],
    "ASU (VPN Connection)": [ 534.85, 597.44, 601.58, 597.32, 720.34, 603.54, 616.24, 559.24, 533.63, 542.72 ],
    "UT Dallas (VPN Connection)": [ 689.47, 641.26, 654.69, 687.27, 685.35, 693.46, 703.57, 720.38, 596.38, 686.85 ],

    "Wikipedia Cat (Tor Connection)": [ 1120.21, 999.61, 1116.28, 1050.42, 1011.52, 1123.05, 1146.38, 1092.53, 1152.97, 1049.94 ],
    "Wikipedia Dog (Tor Connection)": [ 1134.44, 1134.15, 1142.41, 1165.12, 1136.11, 1058.39, 1011.00, 1074.86, 1130.40, 1122.12 ],
    "Wikipedia Egress (Tor Connection)": [ 948.96, 815.17, 986.00, 1024.25, 1067.33, 963.91, 841.42, 954.35, 1024.88, 1011.82 ],
    "MIT (Tor Connection)": [ 1197.11, 1118.68, 1127.66, 1118.70, 1180.56, 1162.65, 1105.54, 1147.95, 1119.63, 1158.77 ],
    "UNM (Tor Connection)": [ 1189.51, 1154.49, 1149.10, 1137.80, 1124.71, 1148.01, 1155.40, 1130.56, 1136.29, 1127.99 ],
    "CMU (Tor Connection)": [ 1081.02, 1084.25, 1054.54, 1101.93, 940.60, 1038.01, 1042.06, 1057.75, 1041.02, 1002.67 ],
    "Berkeley (Tor Connection)": [ 1016.50, 925.03, 1061.31, 1011.80, 1013.53, 1046.88, 1034.74, 1037.31, 1063.00, 1049.15 ],
    "UT Austin (Tor Connection)": [ 1138.82, 1080.03, 1098.57, 1103.73, 1005.21, 1129.61, 1043.16, 1144.53, 1092.53, 1128.01 ],
    "ASU (Tor Connection)": [ 1087.29, 1082.49, 1105.46, 1112.09, 1103.50, 1048.61, 1112.09, 1107.63, 1051.41, 1112.88 ],
    "UT Dallas (Tor Connection)": [ 1149.72, 1138.74, 1152.62, 1108.05, 1057.93, 1118.90, 1130.08, 1145.25, 1127.99, 695.91 ]
}

avg_packet_rate = {
    "Wikipedia Cat (Standard Connection)": [ 418, 352, 276, 401, 434, 407, 435, 451, 431, 290 ],
    "Wikipedia Dog (Standard Connection)": [ 362, 493, 452, 441, 381, 341, 467, 301, 283, 453 ],
    "Wikipedia Egress (Standard Connection)": [ 230, 191, 126, 185, 158, 294, 279, 300, 115, 290 ],
    "MIT (Standard Connection)": [ 2137, 2244, 1766, 2004, 2341, 1906, 2021, 1618, 1910, 2138 ],
    "UNM (Standard Connection)": [ 1142, 1136, 1297, 1247, 1150, 1233, 1284, 1329, 1232, 1224 ],
    "CMU (Standard Connection)": [ 445, 445, 447, 463, 447, 460, 444, 679, 476, 480 ],
    "Berkeley (Standard Connection)": [ 449, 554, 554, 563, 503, 534, 534, 604, 581, 593 ],
    "UT Austin (Standard Connection)": [ 3014, 2369, 2764, 2243, 3037, 2053, 2195, 2888, 2484, 2296 ],
    "ASU (Standard Connection)": [ 708, 775, 959, 670, 747, 727, 681, 690, 995, 739 ],
    "UT Dallas (Standard Connection)": [ 4272, 4396, 4295, 4428, 2494, 4307, 2482, 2526, 4311, 2519 ],

    "Wikipedia Cat (VPN Connection)": [ 316, 393, 414, 309, 451, 394, 449, 307, 271, 434 ],
    "Wikipedia Dog (VPN Connection)": [ 378, 357, 401, 614, 381, 329, 418, 277, 362, 324 ],
    "Wikipedia Egress (VPN Connection)": [ 201, 267, 130, 257, 184, 128, 170, 192, 144, 194 ],
    "MIT (VPN Connection)": [ 1907, 3700, 3208, 2671, 3050, 2604, 1694, 1403, 3277, 2893 ],
    "UNM (VPN Connection)": [ 1414, 2012, 2253, 2504, 2495, 1914, 2043, 1860, 2109, 2775 ],
    "CMU (VPN Connection)": [ 138, 137, 733, 750, 143, 138, 135, 84, 726, 137 ],
    "Berkeley (VPN Connection)": [ 621, 770, 646, 716, 701, 617, 730, 644, 719, 817 ],
    "UT Austin (VPN Connection)": [ 1937, 3884, 1452, 1971, 1930, 1366, 3669, 2300, 3381, 4744 ],
    "ASU (VPN Connection)": [ 223, 1126, 1007, 1161, 869, 938, 861, 216, 223, 223 ],
    "UT Dallas (VPN Connection)": [ 960, 1037, 1111, 999, 1129, 1090, 1098, 1020, 1010, 1027 ],

    "Wikipedia Cat (Tor Connection)": [ 145, 153, 248, 193, 139, 146, 150, 188, 61, 147 ],
    "Wikipedia Dog (Tor Connection)": [ 169, 164, 190, 181, 167, 137, 128, 191, 261, 207 ],
    "Wikipedia Egress (Tor Connection)": [ 62, 64, 39, 69, 53, 67, 27, 52, 37, 62 ],
    "MIT (Tor Connection)": [ 452, 209, 397, 409, 509, 521, 196, 408, 278, 370 ],
    "UNM (Tor Connection)": [ 578, 443, 445, 407, 376, 423, 471, 464, 408, 493 ],
    "CMU (Tor Connection)": [ 143, 219, 70, 152, 49, 145, 112, 132, 219, 125 ],
    "Berkeley (Tor Connection)": [ 130, 135, 221, 126, 163, 190, 123, 143, 194, 206 ],
    "UT Austin (Tor Connection)": [ 542, 417, 695, 368, 152, 562, 96, 591, 527, 568 ],
    "ASU (Tor Connection)": [ 164, 273, 320, 280, 264, 309, 278, 258, 91, 313 ],
    "UT Dallas (Tor Connection)": [ 611, 417, 398, 495, 384, 486, 369, 543, 330, 10 ]
}

num_packets_sent = {
    "Wikipedia Cat (Standard Connection)": [ 1612, 1538, 1600, 1603, 1609, 1596, 1607, 1659, 1596, 1598 ],
    "Wikipedia Dog (Standard Connection)": [ 1848, 1694, 1664, 1674, 1646, 1664, 1678, 1679, 1672, 1669 ],
    "Wikipedia Egress (Standard Connection)": [ 896, 886, 487, 914, 917, 878, 876, 886, 512, 900 ],
    "MIT (Standard Connection)": [ 10, 9957, 10, 10, 10, 10, 10, 10, 10, 10 ],
    "UNM (Standard Connection)": [ 11, 10, 10, 11, 10, 10, 10, 10, 10, 10 ],
    "CMU (Standard Connection)": [ 4237, 4072, 4132, 4105, 4178, 4225, 4103, 4225, 4138, 4109 ],
    "Berkeley (Standard Connection)": [ 3355, 3218, 3315, 3179, 3298, 3244, 3232, 3251, 3290, 3284 ],
    "UT Austin (Standard Connection)": [ 18, 18, 18, 18, 18, 18, 18, 18, 18, 18 ],
    "ASU (Standard Connection)": [ 6316, 6210, 6174, 6221, 6126, 6288, 6251, 6262, 6171, 6174 ],
    "UT Dallas (Standard Connection)": [ 31, 32, 31, 32, 18, 31, 18, 18, 32, 19 ],

    "Wikipedia Cat (VPN Connection)": [ 2496, 3147, 2612, 2286, 2634, 2660, 2930, 2259, 2277, 2275 ],
    "Wikipedia Dog (VPN Connection)": [ 2574, 2396, 2324, 3050, 1952, 2032, 3222, 2524, 2470, 2491 ],
    "Wikipedia Egress (VPN Connection)": [ 935, 1320, 754, 1557, 684, 847, 899, 1063, 814, 782 ],
    "MIT (VPN Connection)": [ 12, 20, 20, 12, 17, 15, 10, 9457, 20, 12 ],
    "UNM (VPN Connection)": [ 16, 18, 18, 19, 19, 19, 19, 17, 19, 18 ],
    "CMU (VPN Connection)": [ 7957, 8028, 6773, 6545, 8481, 8204, 8093, 10, 6917, 8224 ],
    "Berkeley (VPN Connection)": [ 6146, 5354, 5434, 5250, 5258, 5268, 5379, 5291, 5098, 5215 ],
    "UT Austin (VPN Connection)": [ 16, 34, 11, 17, 16, 12, 33, 17, 25, 36 ],
    "ASU (VPN Connection)": [ 13, 12, 11, 11, 8824, 11, 10, 12, 13, 13 ],
    "UT Dallas (VPN Connection)": [ 57, 62, 65, 59, 63, 64, 64, 60, 59, 61 ],

    "Wikipedia Cat (Tor Connection)": [ 1137, 1285, 1145, 1225, 1270, 1131, 1125, 1159, 1104, 1250 ],
    "Wikipedia Dog (Tor Connection)": [ 1169, 1202, 1190, 1186, 1216, 1320, 1363, 1290, 1212, 1255 ],
    "Wikipedia Egress (Tor Connection)": [ 434, 510, 394, 379, 352, 417, 520, 423, 383, 399 ],
    "MIT (Tor Connection)": [ 5283, 4761, 5778, 6299, 5456, 6008, 4365, 6218, 4048, 5109 ],
    "UNM (Tor Connection)": [ 11, 11, 11, 11, 11, 11, 11, 11, 11, 11 ],
    "CMU (Tor Connection)": [ 3966, 3922, 4131, 3937, 4668, 4150, 4146, 4059, 4179, 4427 ],
    "Berkeley (Tor Connection)": [ 3410, 3731, 3232, 3412, 3402, 3265, 3309, 3318, 3212, 3314 ],
    "UT Austin (Tor Connection)": [ 8751, 9572, 8903, 6677, 6905, 8603, 5017, 9023, 7650, 8851 ],
    "ASU (Tor Connection)": [ 5879, 5846, 5745, 5723, 5749, 6029, 5658, 5641, 5971, 5592 ],
    "UT Dallas (Tor Connection)": [ 9036, 10, 9069, 8620, 8373, 8732, 9308, 9184, 9253, 859 ]
}

avg_tcp_window = {
    "Wikipedia Cat (Standard Connection)": [ 76194, 76520, 76932, 85413, 72574, 72501, 75226, 78341, 76043, 79462 ],
    "Wikipedia Dog (Standard Connection)": [ 72730, 88335, 91683, 83664, 71687, 73865, 78505, 77618, 62241, 89122 ],
    "Wikipedia Egress (Standard Connection)": [ 71534, 77356, 49012, 74130, 71147, 66932, 67769, 69913, 50313, 76607 ],
    "MIT (Standard Connection)": [ 410672, 416558, 362332, 255696, 348629, 355752, 179494, 162570, 255701, 231874 ],
    "UNM (Standard Connection)": [ 49657, 49135, 46052, 40408, 46369, 47115, 49162, 53194, 49089, 52991 ],
    "CMU (Standard Connection)": [ 33000, 34332, 35577, 33360, 31457, 34422, 33263, 33334, 33190, 33300 ],
    "Berkeley (Standard Connection)": [ 137699, 111209, 117804, 101692, 124720, 136985, 107304, 98934, 109713, 124991 ],
    "UT Austin (Standard Connection)": [ 382337, 385266, 422650, 334955, 440336, 450875, 345736, 299055, 410952, 409214 ],
    "ASU (Standard Connection)": [ 240365, 255629, 228539, 190998, 280607, 252535, 260634, 190826, 214060, 247221 ],
    "UT Dallas (Standard Connection)": [ 443789, 414983, 436196, 443302, 376932, 417961, 360069, 464410, 370016, 593237 ],

    "Wikipedia Cat (VPN Connection)": [ 20164, 20682, 20136, 20229, 20335, 20883, 19923, 20420, 20666, 20028 ],
    "Wikipedia Dog (VPN Connection)": [ 20391, 20587, 20648, 20247, 20460, 20975, 20496, 20584, 20293, 20422 ],
    "Wikipedia Egress (VPN Connection)": [ 19362, 20457, 20381, 20131, 19925, 20043, 19953, 21786, 20353, 20337 ],
    "MIT (VPN Connection)": [ 20774, 20086, 21121, 20621, 20647, 20346, 20147, 20196, 20366, 20789 ],
    "UNM (VPN Connection)": [ 21067, 21040, 20673, 20300, 20261, 20509, 20380, 21357, 20473, 20615 ],
    "CMU (VPN Connection)": [ 20309, 20075, 20299, 20732, 20399, 20014, 21379, 122.8, 20052, 20103 ],
    "Berkeley (VPN Connection)": [ 20477, 20190, 20420, 20386, 20581, 20550, 20237, 20738, 20746, 20550 ],
    "UT Austin (VPN Connection)": [ 20291, 21074, 19892, 20767, 20290, 19991, 20248, 20372, 20703, 20466 ],
    "ASU (VPN Connection)": [ 19627, 19727, 19743, 19854, 22210, 19811, 19839, 20206, 19774, 19986 ],
    "UT Dallas (VPN Connection)": [ 20685, 20389, 20514, 20858, 20920, 20748, 20915, 21299, 20219, 20604 ],

    "Wikipedia Cat (Tor Connection)": [ 1172, 2169, 9541, 4347, 1866, 1874, 1852, 4522, 3919, 24722 ],
    "Wikipedia Dog (Tor Connection)": [ 1879, 1866, 2318, 1843, 5617, 2034, 2149, 1991, 4333, 4048 ],
    "Wikipedia Egress (Tor Connection)": [ 16595, 11864, 2845, 2041, 1956, 16089, 28277, 8733, 1980, 2010 ],
    "MIT (Tor Connection)": [ 1743, 4253, 1899, 1909, 3218, 1817, 1903, 1850, 4495, 1810 ],
    "UNM (Tor Connection)": [ 2231, 2331, 1864, 2497, 2743, 2236, 1848, 1906, 1889, 1909 ],
    "CMU (Tor Connection)": [ 2690, 1977, 7009, 1929, 9552, 1930, 1971, 3069, 2681, 7839 ],
    "Berkeley (Tor Connection)": [ 2037, 2127, 2892, 2913, 2071, 2065, 2030, 2080, 2034, 2057 ],
    "UT Austin (Tor Connection)": [ 2184, 2261, 1970, 1934, 2924, 1898, 3008, 2516, 1975, 2468 ],
    "ASU (Tor Connection)": [ 5039, 2174, 2876, 2606, 4355, 3124, 2552, 2678, 3440, 3054 ],
    "UT Dallas (Tor Connection)": [ 2046, 2056, 2022, 2461, 2883, 3083, 6468, 2583, 3631, 52768 ]
}

avg_ack_rtt = {
    "Wikipedia Cat (Standard Connection)": [ 0.006838, 0.005767, 0.007658, 0.007273, 0.007060, 0.006623, 0.006469, 0.006294, 0.006614, 0.007072 ],
    "Wikipedia Dog (Standard Connection)": [ 0.008102, 0.005458, 0.009092, 0.006607, 0.006944, 0.006397, 0.006815, 0.006904, 0.005129, 0.006047 ],
    "Wikipedia Egress (Standard Connection)": [ 0.007412, 0.006806, 0.005386, 0.007107, 0.013445, 0.006649, 0.007706, 0.006864, 0.004876, 0.007346 ],
    "MIT (Standard Connection)": [ 0.002134, 0.002039, 0.004301, 0.002987, 0.003076, 0.002648, 0.003580, 0.001959, 0.001848, 0.003207 ],
    "UNM (Standard Connection)": [ 0.009088, 0.010124, 0.010985, 0.010114, 0.013040, 0.010965, 0.011107, 0.010668, 0.010808, 0.010189 ],
    "CMU (Standard Connection)": [ 0.011313, 0.013905, 0.011104, 0.013058, 0.012469, 0.011261, 0.012490, 0.010192, 0.011410, 0.013669 ],
    "Berkeley (Standard Connection)": [ 0.010365, 0.010495, 0.014508, 0.010687, 0.011338, 0.011695, 0.012399, 0.012332, 0.010462, 0.011036 ],
    "UT Austin (Standard Connection)": [ 0.006826, 0.005890, 0.004811, 0.005316, 0.005029, 0.005507, 0.005737, 0.006272, 0.005413, 0.006454 ],
    "ASU (Standard Connection)": [ 0.015145, 0.015234, 0.016097, 0.016573, 0.015159, 0.017132, 0.016168, 0.015423, 0.015464, 0.015012 ],
    "UT Dallas (Standard Connection)": [ 0.002599, 0.002499, 0.002520, 0.002499, 0.003113, 0.002880, 0.003254, 0.002940, 0.002452, 0.003048 ],

    "Wikipedia Cat (VPN Connection)": [ 0.012980, 0.014479, 0.014851, 0.013607, 0.013587, 0.015064, 0.014727, 0.013978, 0.014640, 0.013312 ],
    "Wikipedia Dog (VPN Connection)": [ 0.013500, 0.013937, 0.013825, 0.012324, 0.012603, 0.017686, 0.015881, 0.025364, 0.015666, 0.029102 ],
    "Wikipedia Egress (VPN Connection)": [ 0.016949, 0.014746, 0.019869, 0.018464, 0.013047, 0.016626, 0.016157, 0.017813, 0.019419, 0.015351 ],
    "MIT (VPN Connection)": [ 0.011253, 0.009549, 0.019604, 0.009523, 0.010318, 0.011340, 0.011623, 0.010962, 0.009246, 0.011216 ],
    "UNM (VPN Connection)": [ 0.010045, 0.009469, 0.008924, 0.009530, 0.009116, 0.009213, 0.009446, 0.009164, 0.009546, 0.009578 ],
    "CMU (VPN Connection)": [ 0.013861, 0.013758, 0.010376, 0.010220, 0.026297, 0.013399, 0.016267, 0.016591, 0.010152, 0.019343 ],
    "Berkeley (VPN Connection)": [ 0.011906, 0.010861, 0.011372, 0.010800, 0.010547, 0.010870, 0.010920, 0.011240, 0.010470, 0.010701 ],
    "UT Austin (VPN Connection)": [ 0.010532, 0.009764, 0.010953, 0.010124, 0.011018, 0.010917, 0.010614, 0.009930, 0.010546, 0.009975 ],
    "ASU (VPN Connection)": [ 0.015534, 0.011986, 0.012144, 0.011715, 0.012688, 0.011343, 0.014772, 0.015977, 0.015384, 0.014764 ],
    "UT Dallas (VPN Connection)": [ 0.011189, 0.012197, 0.012275, 0.012074, 0.011716, 0.011413, 0.011177, 0.011821, 0.012797, 0.011524 ],

    "Wikipedia Cat (Tor Connection)": [ 0.018117, 0.014939, 0.019241, 0.016168, 0.019894, 0.019212, 0.020840, 0.017972, 0.022328, 0.023991 ],
    "Wikipedia Dog (Tor Connection)": [ 0.025439, 0.019213, 0.016278, 0.019868, 0.019463, 0.017301, 0.014648, 0.015660, 0.019427, 0.017180 ],
    "Wikipedia Egress (Tor Connection)": [ 0.028084, 0.020865, 0.031871, 0.023017, 0.027678, 0.026285, 0.031107, 0.025197, 0.026893, 0.027697 ],
    "MIT (Tor Connection)": [ 0.012384, 0.013832, 0.012107, 0.010959, 0.013072, 0.011375, 0.013105, 0.010971, 0.013477, 0.011752 ],
    "UNM (Tor Connection)": [ 0.014140, 0.015628, 0.013638, 0.013810, 0.012906, 0.013723, 0.014095, 0.013353, 0.013491, 0.013092 ],
    "CMU (Tor Connection)": [ 0.016032, 0.015163, 0.018029, 0.017068, 0.018774, 0.015699, 0.015487, 0.015739, 0.015002, 0.015546 ],
    "Berkeley (Tor Connection)": [ 0.016090, 0.015640, 0.016163, 0.015665, 0.015716, 0.014888, 0.015915, 0.015748, 0.015542, 0.015178 ],
    "UT Austin (Tor Connection)": [ 0.011656, 0.010535, 0.010431, 0.010871, 0.013350, 0.011586, 0.014294, 0.012258, 0.011022, 0.011956 ],
    "ASU (Tor Connection)": [ 0.016630, 0.017051, 0.014534, 0.016967, 0.015864, 0.013342, 0.015881, 0.015469, 0.019431, 0.015932 ],
    "UT Dallas (Tor Connection)": [ 0.012489, 0.011377, 0.011653, 0.011115, 0.010500, 0.011312, 0.025649, 0.012254, 0.013093, 0.052341 ]
}

labels = ["Standard", "VPN", "Tor"]
plot_type = [
    "Wikipedia Cat",
    "Wikipedia Dog",
    "Wikipedia Egress",
    "MIT",
    "UNM",
    "CMU",
    "Berkeley",
    "UT Austin",
    "ASU",
    "UT Dallas"
]

for t in plot_type:
    fig, ax = plt.subplots( figsize=(6, 5) )
    data = [
        avg_packet_size[f"{t} (Standard Connection)"],
        avg_packet_size[f"{t} (VPN Connection)"],
        avg_packet_size[f"{t} (Tor Connection)"]
    ]

    ax.plot( packet, data[0], label=labels[0], marker="s" )
    ax.plot( packet, data[1], label=labels[1], marker="o" )
    ax.plot( packet, data[2], label=labels[2], marker="x" )
    ax.set_xlabel( "Run No." )
    ax.set_ylabel( "Average Packet Size (bytes)" )
    ax.set_title( f"{t} - Average Packet Size" )
    ax.legend()
    fig.savefig( f"AvgPacketSize-{t}.png" )
    plt.close( fig )

for t in plot_type:
    fig, ax = plt.subplots( figsize=(6, 5) )
    data = [
        avg_packet_rate[f"{t} (Standard Connection)"],
        avg_packet_rate[f"{t} (VPN Connection)"],
        avg_packet_rate[f"{t} (Tor Connection)"]
    ]

    ax.plot( packet, data[0], label=labels[0], marker="s" )
    ax.plot( packet, data[1], label=labels[1], marker="o" )
    ax.plot( packet, data[2], label=labels[2], marker="x" )
    ax.set_xlabel( "Run No." )
    ax.set_ylabel( "Average Packet Rate (packets per second)" )
    ax.set_title( f"{t} - Average Packet Rate" )
    ax.legend()
    fig.savefig( f"AvgPacketRate-{t}.png" )
    plt.close( fig )

for t in plot_type:
    fig, ax = plt.subplots( figsize=(6, 5) )
    data = [
        num_packets_sent[f"{t} (Standard Connection)"],
        num_packets_sent[f"{t} (VPN Connection)"],
        num_packets_sent[f"{t} (Tor Connection)"]
    ]

    ax.plot( packet, data[0], label=labels[0], marker="s" )
    ax.plot( packet, data[1], label=labels[1], marker="o" )
    ax.plot( packet, data[2], label=labels[2], marker="x" )
    ax.set_xlabel( "Run No." )
    ax.set_ylabel( "Number Packets Sent" )
    ax.set_title( f"{t} - Number Packets Sent" )
    ax.legend()
    fig.savefig( f"NumPacketsSent-{t}.png" )
    plt.close( fig )

for t in plot_type:
    fig, ax = plt.subplots( figsize=(6, 5) )
    data = [
        avg_tcp_window[f"{t} (Standard Connection)"],
        avg_tcp_window[f"{t} (VPN Connection)"],
        avg_tcp_window[f"{t} (Tor Connection)"]
    ]

    ax.plot( packet, data[0], label=labels[0], marker="s" )
    ax.plot( packet, data[1], label=labels[1], marker="o" )
    ax.plot( packet, data[2], label=labels[2], marker="x" )
    ax.set_xlabel( "Run No." )
    ax.set_ylabel( "Average TCP Window Size (bytes)" )
    ax.set_title( f"{t} - Average TCP Window Size" )
    ax.legend()
    fig.savefig( f"TcpWindow-{t}.png" )
    plt.close( fig )

for t in plot_type:
    fig, ax = plt.subplots( figsize=(6, 5) )
    data = [
        avg_ack_rtt[f"{t} (Standard Connection)"],
        avg_ack_rtt[f"{t} (VPN Connection)"],
        avg_ack_rtt[f"{t} (Tor Connection)"]
    ]

    ax.plot( packet, data[0], label=labels[0], marker="s" )
    ax.plot( packet, data[1], label=labels[1], marker="o" )
    ax.plot( packet, data[2], label=labels[2], marker="x" )
    ax.set_xlabel( "Run No." )
    ax.set_ylabel( "Average TCP ACK Round Trip Time (seconds)" )
    ax.set_title( f"{t} - TCP ACK Round Trip Time" )
    ax.legend()
    fig.savefig( f"TcpAckRtt-{t}.png" )
    plt.close( fig )
