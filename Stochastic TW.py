import itertools
import datetime
import gantt
import math
import random
import pandas as pd
import numpy as np
import pyprind

number_of_MC_runs = 100000
method_mode = 0 # "0" for Monte Carlo
         # "1" for Enumerated
         # "2" for Deterministic
TW_mode = 1 # "0" for Deterministic TW
            # "1" for Stochastic TW
data_mode = 1 # "0" for short memory
              # "1" for long memory

# EMPTY LISTS FOR DATA MANAGEMENT
a1_alternative_list, a1_duration_list, a1_cost_list, a1_crews_list = [], [], [], []
a2_alternative_list, a2_duration_list, a2_cost_list, a2_crews_list = [], [], [], []
a3_alternative_list, a3_duration_list, a3_cost_list, a3_crews_list = [], [], [], []
a4_alternative_list, a4_duration_list, a4_cost_list, a4_crews_list = [], [], [], []
a5_alternative_list, a5_duration_list, a5_cost_list, a5_crews_list = [], [], [], []
a6_alternative_list, a6_duration_list, a6_cost_list, a6_crews_list = [], [], [], []
a7_alternative_list, a7_duration_list, a7_cost_list, a7_crews_list = [], [], [], []
a8_alternative_list, a8_duration_list, a8_cost_list, a8_crews_list = [], [], [], []
a9_alternative_list, a9_duration_list, a9_cost_list, a9_crews_list = [], [], [], []
a10_alternative_list, a10_duration_list, a10_cost_list, a10_crews_list = [], [], [], []
a11_alternative_list, a11_duration_list, a11_cost_list, a11_crews_list = [], [], [], []
a12_alternative_list, a12_duration_list, a12_cost_list, a12_crews_list = [], [], [], []
a13_alternative_list, a13_duration_list, a13_cost_list, a13_crews_list = [], [], [], []
a14_alternative_list, a14_duration_list, a14_cost_list, a14_crews_list = [], [], [], []
a15_alternative_list, a15_duration_list, a15_cost_list, a15_crews_list = [], [], [], []
tw0_duration_list, tw1_duration_list, tw3_duration_list, tw4_duration_list  = [], [], [], []
tw0_st_list, tw1_st_list, tw3_st_list, tw4_st_list = [], [], [], []
tw0_sp_list, tw1_sp_list, tw3_sp_list, tw4_sp_list = [], [], [], []
work_duration_list = []
total_cost_list = []
schedules_to_print = 9
pd.set_option('display.max_columns', None)

# Formatting
gantt.define_font_attributes(fill='black',
                             stroke='black',
                             stroke_width=0,
                             font_family="Verdana")
gantt.define_not_worked_days([])  # list_of_days -- list of integer (0: Monday ... 6: Sunday) - default [5, 6]

# CREWS
# Berm and abutment base
# Excavate (p. 603, added 15% to cost for loading onto trucks)
# [output/hr BCY, cost $/hr, workers, equipment weight lb, excavator capacity, CAT model]
B12B = [125, 316, 2, 49600, '1.5 CY', '320 4F excavator']  # line 31 23 16.42 0250
B12C = [165, 339, 2, 67900, '2 CY', '330 GC excavator']  # line 31 23 16.42 0260
B12D = [260, 539, 2, 83100, '3.5 CY', '340 excavator']  # line 31 23 16.42 0300
# Haul
# [output/hr LCY (calculated), cost $/hr, workers, total equipment weight lb, truck heaped capacity, CAT model]
B34E = [32.7, 238, 1, 50975, '19.6 CY', '725 truck']
B34F = [43.8, 259, 1, 70548, '26.2 CY', '735 truck']
B34G = [68.1, 303, 1, 76529, '40.8 CY', '772G truck']
# Spread
# [output/hr BCY, cost $/hr, workers, total equipment weight lb, dozer power, CAT model]
B10W = [87.5, 184, 1.5, 20640, '104 HP', 'D3 dozer']
B10B = [237.5, 285, 1.5, 50733, '215 HP', 'D6 dozer']
B10X = [241.3, 434, 1.5, 110225, '452 HP', 'D9 dozer']
# Define alternative methods for a1_build_berm
a1_alternative_0 = [B12B, B34E, B10W]
a1_alternative_1 = [B12C, B34F, B10B]
a1_alternative_2 = [B12D, B34G, B10X]
a1_alternatives = [a1_alternative_0, a1_alternative_1, a1_alternative_2]
a9_alternatives = [a1_alternative_0, a1_alternative_1, a1_alternative_2]
a10_alternatives = [a1_alternative_0, a1_alternative_1, a1_alternative_2]
a14_alternatives = [a1_alternative_0, a1_alternative_1, a1_alternative_2]
# Abutment base (berm crews plus compaction crew)
# Compact
# [output/hr CCY, cost $/hr, workers, total equipment weight lb]
B10G = [162.5, 269.9, 1.5, 49652, '815 sheep-foot roller'] # line 32 23 23.24 0300 (p. 619)
# Define alternative methods for a4_abutment_base
a4_alternative_0 = [B12B, B34E, B10W, B10G]
a4_alternative_1 = [B12C, B34F, B10B, B10G]
a4_alternative_2 = [B12D, B34G, B10X, B10G]
a4_alternatives = [a4_alternative_0, a4_alternative_1, a4_alternative_2]
a7_alternatives = [a4_alternative_0, a4_alternative_1, a4_alternative_2]
# Piles
# Driven prestressed, precast concrete piles 50' long, 12" diameter, 2-3/8" wall
# [output/hr VLF, cost $/hr, workers, total equipment weight: 1 crawler crane 40 ton, 1 lead 90' high, 1 diesel hammer 22k ft-lb]
B19_CONCRETE = [90, 827, 8, 96000+8055, 'SCC400TB 40 Ton crane, I-12V2 diesel hummer with lead'] # line 31 62 13.23 2200 (p.624)
#  Fixed end caisson piles 50' long, 18" diameter
#  Open style; machine drilled in wet ground; productivity includes excavation, concrete, 50 lb/CY reinforcing;
#  not includes boulder removal
# [output/hr VLF, cost $/hr, workers, equipment: 6" water pump, 1 truck-mounted drill rig, 1 suction and 1 discharge hoses]
B48_CAST_IN = [20, 843, 7, 44000, 'CAT-50 drill'] # line 31 63 26.13 1300 (p. 626)
# Off-road, mobile self-loading concrete mixer
# [output/hr CY of ready mix concrete (5 per truck), cost $/hr, operators, CARMIX 3500 truck weight]
CARMIX_3500 = [10, 400, 2, 2*16300, 'CARMIX 3500 self-loading concrete truck']
# Steel driven piles "H" section 50' long, HP 12x53 (53 lb/ft, width = 12", depth = 11.8")
# [output/hr VLF, cost $/hr, workers, equipment: 1 crawler crane 40 ton, 1 lead 90' high, 1 diesel hammer 22k ft-lb]
B19_STEEL = [74, 827, 8, 96000+8055, 'SCC400TB 40 Ton crane, I-12V2 diesel hummer with lead']
# Define alternative methods for a2_install_piles
a2_alternative_0 = [B19_CONCRETE]
a2_alternative_1 = [B48_CAST_IN, CARMIX_3500]
a2_alternative_2 = [B19_STEEL]
a2_alternatives = [a2_alternative_0, a2_alternative_1, a2_alternative_2]
a11_alternatives = [a2_alternative_0, a2_alternative_1, a2_alternative_2]
# Cast-in-place pier and abutment
# Pile cap and pier wall
# [output/hr CY, cost $/hr, workers, total pump weight lb, pump output 45 CY/hr]
C14A = [2.91, 1287, 25, 7300, 'Schwing SP 500 concrete pump']
# [output/hr SFCA, cost $/hr, workers, wall, job-built plywood, over 16 feet high, 2 use]
C2 = [36.25, 413, 6, 0] # line 03 11 13.85 2750 (p. 57)
# [output/hr Ton, cost $/hr, workers, columns reiforc. #8 to #18, potentially add unloading crew C5]
C4A = [0.15, 165, 2, 0]  # line 03 21 11.60 2750 (p. 71)
C4A_x8 = list(np.array(C4A) * 8) # 8 number of C4A crews
# [output/hr CY, cost $/hr, workers, total pump weight lb, place concrete with pump, output 45 CY/hr]
C20 = [110, 588, 8, 7300, 'Schwing SP 500 concrete pump']  # line 03 31 13.70 5100 (p. 79)
# [output/hr CY, cost $/hr, workers, total crane weight lb, place concrete with crane]
C7 = [90, 716, 9, 77000, 'Challenger 3160 55 Ton crane']  # line 03 31 13.70 5200 (p. 79)
# Define alternative methods for a3_cast_in_place_piers
a3_alternative_0 = [C14A, CARMIX_3500]
a3_alternative_1 = [C2, C4A_x8, C20, CARMIX_3500]
a3_alternative_2 = [C2, C4A_x8, C7, CARMIX_3500]
a3_alternatives = [a3_alternative_0, a3_alternative_1, a3_alternative_2]
# Define alternative methods for a5_cast_in_place_abutment
a5_alternative_0 = [C14A, CARMIX_3500]
a5_alternative_1 = [C2, C4A_x8, C20, CARMIX_3500]
a5_alternative_2 = [C2, C4A_x8, C7, CARMIX_3500]
a5_alternatives = [a5_alternative_0, a5_alternative_1, a5_alternative_2]
a8_alternatives = [a5_alternative_0, a5_alternative_1, a5_alternative_2]
a12_alternatives = [a5_alternative_0, a5_alternative_1, a5_alternative_2]
# Girder installation
# Crane method
# [output/hr Ton, cost $/hr, workers, total crane weight lb]
E5 = [1.61, 1101, 10, 115919, 'TEREX RT 100 90 ton crane']
# Incremental Launching method
# [output/hr Ton, cost $/hr, workers, total crane and lunging equipment weight lb] output calculated as 450m bridge/2 =
# = 225/(25m lunging per week cycle) x 1.152 ton/m weight of girders
E6 = [1.26, 1653 + 125, 16, 30000 + 115919, 'TEREX RT 100 90 ton crane'] # added $1000 per day for lunging equipment rental cost, and 30k of weight to account for lunging equipment
# Define alternative methods for a6_install_girders
a6_alternative_0 = [E5]
a6_alternative_1 = [E6]
a6_alternatives = [a6_alternative_0, a6_alternative_1]
# Cast-in-place pier and abutment
# [output/hr SF, cost $/hr, workers, equipment weight]
C14F = [342, 568, 9, 0,] # line 03 30 53.4900 (p. 89)
C4A_x5 = list(np.array(C4A) * 5) # 5 number of C4A crews
C4A_x10 = list(np.array(C4A) * 10) # 10 number of C4A crews
C2_x3 = list(np.array(C2) * 3) # 3 number of C2 crews
C2_x6 = list(np.array(C2) * 6) # 6 number of C2 crews
a15_alternative_0 = [C2_x3, C4A_x5, C14F, CARMIX_3500]
a15_alternative_1 = [C2_x6, C4A_x10, C14F, CARMIX_3500]
a15_alternatives = [a15_alternative_0, a15_alternative_1]

# NOTES
# Cost of moving equipment from Hay River to Tulita by Winter road (max speed - 50km/hr, distance 900 km, total of 4.5 days there and back assuming 8 hr/day travel time)
mobilize_duration = 4.5
B34N_cost = 1084.52 # $/hr
B34K_cost = 1516.82 # $/hr
# Ticket from Hay River to Tulita one way - $1255 (Hay River - Yellowknife - Tulita)
air_ticket_cost = 1255

# SIMULATION SETTINGS
alt_3 = [0,1,2]
alt_2 = [0,1]
combinations = list(itertools.product(alt_3,alt_3,alt_3,alt_3,alt_3,alt_2,alt_3,alt_3,alt_3,alt_3,alt_3,alt_3,alt_3,alt_2))
run = 0
number_of_runs = 0
if method_mode == 0:
    number_of_runs = number_of_MC_runs
    print('Monte Carlo')
elif method_mode == 1:
    number_of_runs = len(combinations)
    print('Enumerated')
elif method_mode == 2:
    print('Deterministic')
    number_of_runs = number_of_MC_runs#int(input())
print('Running', format(number_of_runs, ',d'), 'combinations')
bar = pyprind.ProgBar(number_of_runs, monitor=True, bar_char='■')
a1_r1, a1_o1, a1_r2, a1_o2, a1_r3, a1_o3 = 0,0,0,0,0,0
a2_r1, a2_o1, a2_r2, a2_o2, a2_r3, a2_o3 = 0,0,0,0,0,0
a3_r1, a3_o1, a3_r2, a3_o2, a3_r3, a3_o3 = 0,0,0,0,0,0
a4_r1, a4_o1, a4_r2, a4_o2, a4_r3, a4_o3 = 0,0,0,0,0,0
a5_r1, a5_o1, a5_r2, a5_o2, a5_r3, a5_o3 = 0,0,0,0,0,0
a6_r1, a6_o1, a6_r2, a6_o2, a6_r3, a6_o3 = 0,0,0,0,0,0
a7_r1, a7_o1, a7_r2, a7_o2, a7_r3, a7_o3 = 0,0,0,0,0,0
a8_r1, a8_o1, a8_r2, a8_o2, a8_r3, a8_o3 = 0,0,0,0,0,0
a9_r1, a9_o1, a9_r2, a9_o2, a9_r3, a9_o3 = 0,0,0,0,0,0
a10_r1, a10_o1, a10_r2, a10_o2, a10_r3, a10_o3 = 0,0,0,0,0,0
a11_r1, a11_o1, a11_r2, a11_o2, a11_r3, a11_o3 = 0,0,0,0,0,0
a12_r1, a12_o1, a12_r2, a12_o2, a12_r3, a12_o3 = 0,0,0,0,0,0
a13_r1, a13_o1, a13_r2, a13_o2, a13_r3, a13_o3 = 0,0,0,0,0,0
a14_r1, a14_o1, a14_r2, a14_o2, a14_r3, a14_o3 = 0,0,0,0,0,0
a15_r1, a15_o1, a15_r2, a15_o2, a15_r3, a15_o3 = 0,0,0,0,0,0

for iter in range(number_of_runs):
    bar.update()  # progress update
    # TIME-WINDOWS
    if TW_mode == 0:
        tw0_start = datetime.date(2022, 12, 21)
        tw0_stop = datetime.date(2023, 3, 31)
        # TIME-WINDOW TEMPERATURE ABOVE ZERO 2023
        tw1_start = datetime.date(2023, 4, 28)
        tw1_stop = datetime.date(2023, 10, 5)

        # TIME-WINDOW IN-RIVER ACTIVITY 2023
        tw2_start = datetime.date(2023, 7, 16)
        tw2_stop = datetime.date(2023, 9, 14)
        # TIME-WINDOW WINTER ROAD 2023-2024
        tw3_start = datetime.date(2023, 12, 21)
        tw3_stop = datetime.date(2024, 3, 31)

        # TIME-WINDOW TEMPERATURE ABOVE ZERO 2024
        tw4_start = datetime.date(2024, 4, 28)
        tw4_stop = datetime.date(2024, 10, 5)

        # TIME-WINDOW IN-RIVER ACTIVITY 2024
        tw5_start = datetime.date(2024, 7, 16)
        tw5_stop = datetime.date(2024, 9, 14)
    elif TW_mode == 1:
        # TIME-WINDOW WINTER ROAD 2022-2023
        # start (logistic)
        loc = 20.63; scale = 3.40
        sampled_day = int(np.random.logistic(loc, scale))
        while sampled_day <= 0 or sampled_day > 62:
            sampled_day = int(np.random.logistic(loc, scale))
        if sampled_day <= 31: day = sampled_day; month = 12; year = 2022
        else: day = sampled_day - 31; month = 1; year = 2023
        tw0_start = datetime.date(year, month, day)
        # stop (normal)
        mu = 30.633; sigma = 10.471
        sampled_day = int(np.random.normal(mu, sigma))
        while sampled_day <= 0 or sampled_day > 61:
            sampled_day = int(np.random.normal(mu, sigma))
        if sampled_day <= 31: day = sampled_day; month = 3; year = 2023
        else: day = sampled_day - 31; month = 4; year = 2023
        tw0_stop = datetime.date(year, month, day)

        # TIME-WINDOW TEMPERATURE ABOVE ZERO 2023
        # start (gamma)
        kay = 20.63; beta = 3.40
        while True:
            sampled_day = int(np.random.gamma(kay, beta))
            while sampled_day <= 0 or sampled_day > 61:
                sampled_day = int(np.random.gamma(kay, beta))
            if sampled_day <= 30:
                day = sampled_day; month = 4; year = 2023
            else:
                day = sampled_day - 30; month = 5; year = 2023
            tw1_start = datetime.date(year, month, day)
            if (tw1_start - tw0_stop).days >= 6: break # makes sure that a minimum of 6 days gap is maintained between the two time windows (based on 20 years of historical data)
        # stop (logistic)
        loc = 35.39; scale = 3.99
        sampled_day = int(np.random.logistic(loc, scale))
        while sampled_day <= 0 or sampled_day > 61:
            sampled_day = int(np.random.logistic(loc, scale))
        if sampled_day <= 30:
            day = sampled_day; month = 9; year = 2023
        else:
            day = sampled_day - 30; month = 10; year = 2023
        tw1_stop = datetime.date(year, month, day)

        # TIME-WINDOW IN-RIVER ACTIVITY 2023
        tw2_start = datetime.date(2023, 7, 16)
        tw2_stop = datetime.date(2023, 9, 14)

        # TIME-WINDOW WINTER ROAD 2023-2024
        # start (logistic)
        loc = 20.63; scale = 3.40
        sampled_day = int(np.random.logistic(loc, scale))
        while sampled_day <= 0 or sampled_day > 62:
            sampled_day = int(np.random.logistic(loc, scale))
        if sampled_day <= 31:
            day = sampled_day; month = 12; year = 2023
        else:
            day = sampled_day - 31; month = 1; year = 2024
        tw3_start = datetime.date(year, month, day)
        # stop (normal)
        mu = 30.633; sigma = 10.471
        sampled_day = int(np.random.normal(mu, sigma))
        while sampled_day <= 0 or sampled_day > 61:
            sampled_day = int(np.random.normal(mu, sigma))
        if sampled_day <= 31:
            day = sampled_day; month = 3; year = 2024
        else:
            day = sampled_day - 31; month = 4; year = 2024
        tw3_stop = datetime.date(year, month, day)

        # TIME-WINDOW TEMPERATURE ABOVE ZERO 2024
        # start (gamma)
        kay = 20.63; beta = 3.40
        while True:
            sampled_day = int(np.random.gamma(kay, beta))
            while sampled_day <= 0 or sampled_day > 61:
                sampled_day = int(np.random.logistic(loc, scale))
            if sampled_day <= 30:
                day = sampled_day; month = 4; year = 2024
            else:
                day = sampled_day - 30; month = 5; year = 2024
            tw4_start = datetime.date(year, month, day)
            if (tw4_start - tw3_stop).days >= 6: break # makes sure that a minimum of 6 days gap is maintained between the two time windows (based on 20 years of historical data)
        # stop (logistic)
        loc = 35.39; scale = 3.99
        sampled_day = int(np.random.logistic(loc, scale))
        while sampled_day <= 0 or sampled_day > 61:
            sampled_day = int(np.random.logistic(loc, scale))
        if sampled_day <= 30:
            day = sampled_day; month = 9; year = 2024
        else:
            day = sampled_day - 30; month = 10; year = 2024
        tw4_stop = datetime.date(year, month, day)

        # TIME-WINDOW IN-RIVER ACTIVITY 2024
        tw5_start = datetime.date(2024, 7, 16)
        tw5_stop = datetime.date(2024, 9, 14)
    tw0_duration = tw0_stop - tw0_start
    tw1_duration = tw1_stop - tw1_start
    tw2_duration = tw2_stop - tw2_start
    tw3_duration = tw3_stop - tw3_start
    tw4_duration = tw4_stop - tw4_start
    tw5_duration = tw5_stop - tw5_start

    if method_mode == 0:
        a1_x = random.randint(0, len(a1_alternatives) - 1)
        a2_x = random.randint(0, len(a2_alternatives) - 1)
        a3_x = random.randint(0, len(a3_alternatives) - 1)
        a4_x = random.randint(0, len(a4_alternatives) - 1)
        a5_x = random.randint(0, len(a5_alternatives) - 1)
        a6_x = random.randint(0, len(a6_alternatives) - 1)
        a7_x = random.randint(0, len(a7_alternatives) - 1)
        a8_x = random.randint(0, len(a8_alternatives) - 1)
        a9_x = random.randint(0, len(a9_alternatives) - 1)
        a10_x = random.randint(0, len(a10_alternatives) - 1)
        a11_x = random.randint(0, len(a11_alternatives) - 1)
        a12_x = random.randint(0, len(a12_alternatives) - 1)
        a14_x = random.randint(0, len(a14_alternatives) - 1)
        a15_x = random.randint(0, len(a15_alternatives) - 1)
    elif method_mode == 1:
        a1_x = combinations[iter][0]
        a2_x = combinations[iter][1]
        a3_x = combinations[iter][2]
        a4_x = combinations[iter][3]
        a5_x = combinations[iter][4]
        a6_x = combinations[iter][5]
        a7_x = combinations[iter][6]
        a8_x = combinations[iter][7]
        a9_x = combinations[iter][8]
        a10_x = combinations[iter][9]
        a11_x = combinations[iter][10]
        a12_x = combinations[iter][11]
        #a13_x = combinations[iter][12]
        a14_x = combinations[iter][12]
        a15_x = combinations[iter][13]
    elif method_mode == 2:
        a1_x = 0
        a2_x = 0
        a3_x = 0
        a4_x = 0
        a5_x = 0
        a6_x = 0
        a7_x = 0
        a8_x = 0
        a9_x = 0
        a10_x = 0
        a11_x = 0
        a12_x = 0
        a14_x = 0
        a15_x = 0

    # MOBILIZE JOB SITE
    a0_start = tw0_start
    a0_stop = None
    a0_duration = random.randint(30,30)#tw0_2023_duration.days/2

    # BUILD BERM 1
    a1_working_hours = 8
    a1_quantity = 88752  # BCY
    a1_allowable_duration = tw0_duration.days - a0_duration
    a1_productivity = min(a1_alternatives[a1_x][0][0], a1_alternatives[a1_x][2][0])
    a1_truck_crews = math.ceil(a1_productivity / (a1_alternatives[a1_x][1][0] / 1.25)) # 1.25 - bank to loose conversion factor
    a1_hourly_cost = (a1_alternatives[a1_x][0][1] + a1_truck_crews * a1_alternatives[a1_x][1][1] + a1_alternatives[a1_x][2][1])
    a1_initial_duration = a1_quantity / a1_productivity / a1_working_hours
    if a1_initial_duration < a1_allowable_duration:
        a1_crews = 1
        a1_duration = math.ceil(a1_initial_duration)
    else:
        a1_crews = math.ceil(a1_initial_duration/a1_allowable_duration)
        a1_duration = math.ceil(a1_quantity / a1_productivity / a1_working_hours / a1_crews)
    a1_ppl = math.ceil(a1_alternatives[a1_x][0][2] + a1_alternatives[a1_x][1][2] * a1_truck_crews + a1_alternatives[a1_x][2][2]) * a1_crews
    a1_ticket_cost = a1_ppl * air_ticket_cost * 2
    a1_equip_weight = math.ceil(a1_alternatives[a1_x][0][3] + a1_alternatives[a1_x][1][3] * a1_truck_crews + a1_alternatives[a1_x][2][3]) * a1_crews
    if a1_equip_weight <= 80000: a1_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a1_equip_weight <= 150000: a1_weight_cost = mobilize_duration * B34K_cost
    else: a1_weight_cost = mobilize_duration * B34K_cost * math.ceil(a1_equip_weight/150000)
    a1_cost = a1_crews * a1_duration * a1_working_hours * a1_hourly_cost + a1_ticket_cost + a1_weight_cost
    a1_start = a0_start + datetime.timedelta(a0_duration)
    a1_stop = None

    # INSTALL PILES 1
    a2_working_hours = 8
    a2_quantity = 6200  # VLF (64 piles x 50')
    a2_allowable_duration = (tw1_stop - tw0_stop).days
    a2_productivity = a2_alternatives[a2_x][0][0]
    a2_hourly_cost = 0
    for i in range(len(a2_alternatives[a2_x])):
        a2_hourly_cost += a2_alternatives[a2_x][i][1]
    a2_initial_duration = a2_quantity / a2_productivity / a2_working_hours
    if a2_initial_duration < a2_allowable_duration:
        a2_crews = 1
        a2_duration = math.ceil(a2_initial_duration)
    else:
        a2_crews = math.ceil(a2_initial_duration / a2_allowable_duration)
        a2_duration = math.ceil(a2_quantity / a2_productivity / a2_working_hours / a2_crews)
    a2_ppl = 0
    for n in range(len(a2_alternatives[a2_x])):
        a2_ppl += a2_crews * math.ceil(a2_alternatives[a2_x][n][2])
    a2_ticket_cost = a2_ppl * air_ticket_cost * 2
    a2_equip_weight = 0
    for m in range(len(a2_alternatives[a2_x])):
        a2_equip_weight += a2_crews * a2_alternatives[a2_x][m][3]
    if a2_equip_weight <= 80000: a2_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a2_equip_weight <= 150000: a2_weight_cost = mobilize_duration * B34K_cost
    else: a2_weight_cost = mobilize_duration * B34K_cost * math.ceil(a2_equip_weight/150000)
    a2_cost = a2_crews * a2_duration * a2_working_hours * a2_hourly_cost + a2_ticket_cost + a2_weight_cost
    a2_start = tw0_stop
    a2_stop = None

    # CAST-IN-PLACE PIERS 1
    a3_working_hours = 8
    a3_quantity = 2*1674.18  # CY
    a3_quantity_SFCA = 2*10979.19 # SFCA
    a3_quantity_Ton = 2*219.8 # Ton
    if a6_x == 0: a3_allowable_duration = tw1_duration.days
    else: a3_allowable_duration = (tw2_start - tw1_start).days
    # Productivity
    if len(a3_alternatives[a3_x]) == 2: a3_productivity = a3_alternatives[a3_x][0][0]
    else: a3_productivity = a3_quantity/(a3_quantity_SFCA/a3_alternatives[a3_x][0][0] + a3_quantity_Ton/a3_alternatives[a3_x][1][0] + a3_quantity/a3_alternatives[a3_x][2][0])
    a3_hourly_cost = 0
    for i in range(len(a3_alternatives[a3_x])):
        a3_hourly_cost += a3_alternatives[a3_x][i][1]
    a3_initial_duration = a3_quantity / a3_productivity / a3_working_hours
    if a3_initial_duration < a3_allowable_duration:
        a3_crews = 1
        a3_duration = math.ceil(a3_initial_duration)
    else:
        a3_crews = math.ceil(a3_initial_duration / a3_allowable_duration)
        a3_duration = math.ceil(a3_quantity / a3_productivity / a3_working_hours / a3_crews)
    a3_ppl = 0
    for n in range(len(a3_alternatives[a3_x])):
        a3_ppl += a3_crews * math.ceil(a3_alternatives[a3_x][n][2])
    a3_ticket_cost = a3_ppl * air_ticket_cost * 2
    a3_equip_weight = 0
    for m in range(len(a3_alternatives[a3_x])):
        a3_equip_weight += a3_crews * a3_alternatives[a3_x][m][3]
    if a3_equip_weight <= 80000: a3_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a3_equip_weight <= 150000: a3_weight_cost = mobilize_duration * B34K_cost
    else: a3_weight_cost = mobilize_duration * B34K_cost * math.ceil(a3_equip_weight/150000)
    a3_cost = a3_crews * a3_duration * a3_working_hours * a3_hourly_cost + a3_ticket_cost + a3_weight_cost
    a3_start = tw1_start
    a3_stop = None

    # ABUTMENT BASE 1
    a4_working_hours = 8
    a4_quantity = 20631  # BCY
    a4_allowable_duration = tw1_duration.days/2
    a4_productivity = min(a4_alternatives[a4_x][0][0], a4_alternatives[a4_x][2][0])
    a4_truck_crews = math.ceil(a4_productivity / (a4_alternatives[a4_x][1][0] / 1.25))
    a4_roller_crews = math.ceil(a4_productivity / (a4_alternatives[a4_x][3][0] / 0.9))
    a4_hourly_cost = ((a4_alternatives[a4_x][0][1] + a4_truck_crews * a4_alternatives[a4_x][1][1] + a4_alternatives[a4_x][2][1]) +
                      a4_roller_crews * a4_alternatives[a4_x][3][1]) # 0.9 - compacted to bank conversion factor; 1.25 -  bank to loose conversion factor
    a4_initial_duration = a4_quantity / a4_productivity / a4_working_hours
    if a4_initial_duration < a4_allowable_duration:
        a4_crews = 1
        a4_duration = math.ceil(a4_initial_duration)
    else:
        a4_crews = math.ceil(a4_initial_duration / a4_allowable_duration)
        a4_duration = math.ceil(a4_quantity / a4_productivity / a4_working_hours / a4_crews)
    a4_ppl = math.ceil(a4_alternatives[a4_x][0][2]+a4_alternatives[a4_x][1][2]*a4_truck_crews + a4_alternatives[a4_x][2][2] + a4_alternatives[a4_x][3][2]*a4_roller_crews) * a4_crews
    a4_ticket_cost = a4_ppl * air_ticket_cost * 2
    a4_equip_weight = math.ceil(a4_alternatives[a4_x][0][3]+a4_alternatives[a4_x][1][3]*a4_truck_crews + a4_alternatives[a4_x][2][3] + a4_alternatives[a4_x][3][3]*a4_roller_crews) * a4_crews
    if a4_equip_weight <= 80000: a4_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a4_equip_weight <= 150000: a4_weight_cost = mobilize_duration * B34K_cost
    else: a4_weight_cost = mobilize_duration * B34K_cost * math.ceil(a4_equip_weight / 150000)
    a4_cost = a1_crews * a4_duration * a4_working_hours * a4_hourly_cost + a4_ticket_cost + a4_weight_cost
    a4_start = tw1_start
    a4_stop = a4_start + datetime.timedelta(a4_duration)

    # CAST-IN-PLACE ABUTMENT 1
    a5_working_hours = 8
    a5_quantity = 978.21  # CY
    a5_quantity_SFCA = 3790.17  # SFCA
    a5_quantity_Ton = 75  # Ton
    a5_allowable_duration = (tw2_start - a4_stop).days
    # Productivity
    if len(a5_alternatives[a5_x]) == 2: a5_productivity = a5_alternatives[a5_x][0][0]
    else: a5_productivity = a5_quantity / (a5_quantity_SFCA / a5_alternatives[a5_x][0][0] + a5_quantity_Ton / a5_alternatives[a5_x][1][0] +
                                            a5_quantity / a5_alternatives[a5_x][2][0])
    a5_hourly_cost = 0
    for i in range(len(a5_alternatives[a5_x])):
        a5_hourly_cost += a5_alternatives[a5_x][i][1]
    a5_initial_duration = a5_quantity / a5_productivity / a5_working_hours
    if a5_initial_duration < a5_allowable_duration:
        a5_crews = 1
        a5_duration = math.ceil(a5_initial_duration)
    else:
        a5_crews = math.ceil(a5_initial_duration / a5_allowable_duration)
        a5_duration = math.ceil(a5_quantity / a5_productivity / a5_working_hours / a5_crews)
    a5_ppl = 0
    for n in range(len(a5_alternatives[a5_x])):
        a5_ppl += a5_crews * math.ceil(a5_alternatives[a5_x][n][2])
    a5_ticket_cost = a5_ppl * air_ticket_cost * 2
    a5_equip_weight = 0
    for m in range(len(a5_alternatives[a5_x])):
        a5_equip_weight += a5_crews * a5_alternatives[a5_x][m][3]
    if a5_equip_weight <= 80000: a5_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a5_equip_weight <= 150000: a5_weight_cost = mobilize_duration * B34K_cost
    else: a5_weight_cost = mobilize_duration * B34K_cost * math.ceil(a5_equip_weight / 150000)
    a5_cost = a5_crews * a5_duration * a5_working_hours * a5_hourly_cost + a5_ticket_cost + a5_weight_cost
    a5_start = a4_start + datetime.timedelta(a4_duration)
    a5_stop = a5_start + datetime.timedelta(a5_duration)

    # INSTALL GIRDERS 1
    a6_working_hours = 8
    if a6_x == 0:
        a6_quantity = 1296 # Imperial ton (half of the bridge)
        a6_crews = 2 # Need minimum 2 crews to install girders with cranes
        a6_name = 'a6_install_girders_depends_on_[a3, a5]'
    else:
        a6_quantity = 1296 * 2 # Full bridge in case of incremental launching
        a6_crews = 1
        a6_name = 'a6_install_girders_start_depends_on_[a3, a5]_stop_depends_on_[8, 12]'
    a6_productivity = a6_alternatives[a6_x][0][0]
    a6_hourly_cost = 0
    for i in range(len(a6_alternatives[a6_x])):
        a6_hourly_cost += a6_alternatives[a6_x][i][1]
    a6_duration = a6_quantity / a6_productivity /a6_crews / a6_working_hours
    a6_ppl = 0
    for n in range(len(a6_alternatives[a6_x])):
        a6_ppl += a6_crews * math.ceil(a6_alternatives[a6_x][n][2])
    a6_ticket_cost = a6_ppl * air_ticket_cost * 2
    a6_equip_weight = 0
    for m in range(len(a6_alternatives[a6_x])):
        a6_equip_weight += a6_crews * a6_alternatives[a6_x][m][3]
    if a6_equip_weight <= 80000: a6_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a6_equip_weight <= 150000: a6_weight_cost = mobilize_duration * B34K_cost
    else: a6_weight_cost = mobilize_duration * B34K_cost * math.ceil(a6_equip_weight/150000)
    a6_cost = a6_crews * a6_duration * a6_working_hours * a6_hourly_cost + a6_ticket_cost + a6_weight_cost
    a6_start = None
    a6_stop = None

    # ABUTMENT BASE 2
    a7_working_hours = 8
    a7_quantity = 20631  # BCY
    a7_allowable_duration = (tw1_stop - a5_stop).days / 2
    a7_productivity = min(a7_alternatives[a7_x][0][0], a7_alternatives[a7_x][2][0])
    a7_truck_crews = math.ceil(a7_productivity / (a7_alternatives[a7_x][1][0] / 1.25))
    a7_roller_crews = math.ceil(a7_productivity / (a7_alternatives[a7_x][3][0] / 0.9))
    a7_hourly_cost = ((a7_alternatives[a7_x][0][1] + a7_truck_crews * a7_alternatives[a7_x][1][1] +
                        a7_alternatives[a7_x][2][1]) +
                       a7_roller_crews * a7_alternatives[a7_x][3][
                           1])  # 0.9 - compacted to bank conversion factor; 1.25 -  bank to loose conversion factor
    a7_initial_duration = a7_quantity / a7_productivity / a7_working_hours
    if a7_initial_duration < a7_allowable_duration:
        a7_crews = 1
        a7_duration = math.ceil(a7_initial_duration)
    else:
        a7_crews = math.ceil(a7_initial_duration / a7_allowable_duration)
        a7_duration = math.ceil(a7_quantity / a7_productivity / a7_working_hours / a7_crews)
    a7_ppl = math.ceil(
        a7_alternatives[a7_x][0][2] + a7_alternatives[a7_x][1][2] * a7_truck_crews + a7_alternatives[a7_x][2][
            2] +
        a7_alternatives[a7_x][3][2] * a7_roller_crews) * a7_crews
    a7_ticket_cost = a7_ppl * air_ticket_cost * 2
    a7_equip_weight = math.ceil(
        a7_alternatives[a7_x][0][3] + a7_alternatives[a7_x][1][3] * a7_truck_crews + a7_alternatives[a7_x][2][
            3] +
        a7_alternatives[a7_x][3][3] * a7_roller_crews) * a7_crews
    if a7_equip_weight <= 80000:
        a7_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a7_equip_weight <= 150000:
        a7_weight_cost = mobilize_duration * B34K_cost
    else:
        a7_weight_cost = mobilize_duration * B34K_cost * math.ceil(a7_equip_weight / 150000)
    a7_cost = a1_crews * a7_duration * a7_working_hours * a7_hourly_cost + a7_ticket_cost + a7_weight_cost
    a7_start = a5_stop
    a7_stop = a7_start + datetime.timedelta(a7_duration)

    # CAST-IN-PLACE ABUTMENT 1
    a8_working_hours = 8
    a8_quantity = 978.21  # CY
    a8_quantity_SFCA = 3790.17  # SFCA
    a8_quantity_Ton = 75  # Ton
    a8_allowable_duration = (tw1_stop - a7_stop).days  # tw1_duration.days - a4_duration
    # Productivity
    if len(a8_alternatives[a8_x]) == 2:
        a8_productivity = a8_alternatives[a8_x][0][0]
    else:
        a8_productivity = a8_quantity / (
                (a8_quantity_SFCA / a8_alternatives[a8_x][0][0] + a8_quantity_Ton / a8_alternatives[a8_x][1][0] +
                 a8_quantity / a8_alternatives[a8_x][2][0]) / a8_working_hours) / a8_working_hours
    a8_hourly_cost = 0
    for i in range(len(a8_alternatives[a8_x])):
        a8_hourly_cost += a8_alternatives[a8_x][i][1]
    a8_initial_duration = a8_quantity / a8_productivity / a8_working_hours
    if a8_initial_duration < a8_allowable_duration:
        a8_crews = 1
        a8_duration = math.ceil(a8_initial_duration)
    else:
        a8_crews = math.ceil(a8_initial_duration / a8_allowable_duration)
        a8_duration = math.ceil(a8_quantity / a8_productivity / a8_working_hours / a8_crews)
    a8_ppl = 0
    for n in range(len(a8_alternatives[a8_x])):
        a8_ppl += a8_crews * math.ceil(a8_alternatives[a8_x][n][2])
    a8_ticket_cost = a8_ppl * air_ticket_cost * 2
    a8_equip_weight = 0
    for m in range(len(a8_alternatives[a8_x])):
        a8_equip_weight += a8_crews * a8_alternatives[a8_x][m][3]
    if a8_equip_weight <= 80000:
        a8_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a8_equip_weight <= 150000:
        a8_weight_cost = mobilize_duration * B34K_cost
    else:
        a8_weight_cost = mobilize_duration * B34K_cost * math.ceil(a8_equip_weight / 150000)
    a8_cost = a8_crews * a8_duration * a8_working_hours * a8_hourly_cost + a8_ticket_cost + a8_weight_cost
    a8_start = a7_stop
    a8_stop = a8_start + datetime.timedelta(a8_duration)

    # REMOVE BERM 1
    a9_working_hours = 8
    a9_quantity = 88752  # BCY
    if a6_x == 1:  # In case of incremental launching
        a9_name = 'a9_remove_berm_depends_on_[a3]'
        a9_allowable_duration = tw2_duration.days/3 # should be divided by 2 but dividing by 3 because often there is not enough time for activities a11 and a12
        a9_start = tw2_start
    else:
        a9_name = 'a9_remove_berm_depends_on_[a6]'
        a9_allowable_duration = tw3_duration.days/2
        a9_start = tw3_start
    a9_productivity = min(a9_alternatives[a9_x][0][0], a9_alternatives[a9_x][2][0])
    a9_truck_crews = math.ceil(a9_productivity / (a9_alternatives[a9_x][1][0] / 1.25)) # 1.25 - bank to loose conversion factor
    a9_hourly_cost = (a9_alternatives[a9_x][0][1] + a9_truck_crews * a9_alternatives[a9_x][1][1] + a9_alternatives[a9_x][2][1])
    a9_initial_duration = a9_quantity / a9_productivity / a9_working_hours
    if a9_initial_duration < a9_allowable_duration:
        a9_crews = 1
        a9_duration = math.ceil(a9_initial_duration)
    else:
        a9_crews = math.ceil(a9_initial_duration / a9_allowable_duration)
        a9_duration = math.ceil(a9_quantity / a9_productivity / a9_working_hours / a9_crews)
    a9_ppl = math.ceil(a9_alternatives[a9_x][0][2] + a9_alternatives[a9_x][1][2] * a9_truck_crews + a9_alternatives[a9_x][2][2]) * a9_crews
    a9_ticket_cost = a9_ppl * air_ticket_cost * 2
    a9_equip_weight = math.ceil(
        a9_alternatives[a9_x][0][3] + a9_alternatives[a9_x][1][3] * a9_truck_crews + a9_alternatives[a9_x][2][3]) * a9_crews
    if a9_equip_weight <= 80000:  # Crew B-34N
        a9_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a9_equip_weight <= 150000:  # Crew B-34K
        a9_weight_cost = mobilize_duration * B34K_cost
    else:
        a9_weight_cost = mobilize_duration * B34K_cost * math.ceil(a9_equip_weight / 150000)
    a9_cost = a9_crews * a9_duration * a9_working_hours * a9_hourly_cost + a9_ticket_cost + a9_weight_cost
    a9_stop = a9_start + datetime.timedelta(a9_duration)

    # BUILD BERM 2
    a10_working_hours = 8
    a10_quantity = 88752  # BCY
    if a6_x == 1: a10_allowable_duration = tw2_duration.days/3# should be - a9_duration but dividing by 3 to allovefor a11 and a12 to happen (In case of incremental launching)
    else: a10_allowable_duration = tw3_duration.days - a9_duration
    a10_productivity = min(a10_alternatives[a10_x][0][0], a10_alternatives[a10_x][2][0])
    a10_truck_crews = math.ceil(a10_productivity / (a10_alternatives[a10_x][1][0] / 1.25))  # 1.25 - bank to loose conversion factor
    a10_hourly_cost = (a10_alternatives[a10_x][0][1] + a10_truck_crews * a10_alternatives[a10_x][1][1] + a10_alternatives[a10_x][2][1])
    a10_initial_duration = a10_quantity / a10_productivity / a10_working_hours
    if a10_initial_duration < a10_allowable_duration:
        a10_crews = 1
        a10_duration = math.ceil(a10_initial_duration)
    else:
        a10_crews = math.ceil(a10_initial_duration / a10_allowable_duration)
        a10_duration = math.ceil(a10_quantity / a10_productivity / a10_working_hours / a10_crews)
    a10_ppl = math.ceil(
        a10_alternatives[a10_x][0][2] + a10_alternatives[a10_x][1][2] * a10_truck_crews + a10_alternatives[a10_x][2][2]) * a10_crews
    a10_ticket_cost = a10_ppl * air_ticket_cost * 2
    a10_equip_weight = math.ceil(a10_alternatives[a10_x][0][3] + a10_alternatives[a10_x][1][3] * a10_truck_crews + a10_alternatives[a10_x][2][3]) * a10_crews
    if a10_equip_weight <= 80000:  # Crew B-34N
        a10_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a10_equip_weight <= 150000:  # Crew B-34K
        a10_weight_cost = mobilize_duration * B34K_cost
    else:
        a10_weight_cost = mobilize_duration * B34K_cost * math.ceil(a10_equip_weight / 150000)
    a10_cost = a10_crews * a10_duration * a10_working_hours * a10_hourly_cost + a10_ticket_cost + a10_weight_cost
    a10_start = a9_stop
    a10_stop = a10_start + datetime.timedelta(a10_duration)

    # INSTALL PILES 2
    a11_working_hours = 8
    a11_quantity = 6200  # VLF (64 piles x 50')
    if a6_x == 1: a11_allowable_duration = (tw1_stop - a10_stop).days/2 # In case of incremental launching
    else: a11_allowable_duration = (tw5_start - a10_stop).days
    a11_productivity = a11_alternatives[a11_x][0][0]
    a11_hourly_cost = 0
    for i in range(len(a11_alternatives[a11_x])):
        a11_hourly_cost += a11_alternatives[a11_x][i][1]
    a11_initial_duration = a11_quantity / a11_productivity / a11_working_hours
    if a11_initial_duration < a11_allowable_duration:
        a11_crews = 1
        a11_duration = math.ceil(a11_initial_duration)
    else:
        a11_crews = math.ceil(a11_initial_duration / a11_allowable_duration)
        a11_duration = math.ceil(a11_quantity / a11_productivity / a11_working_hours / a11_crews)
    a11_ppl = 0
    for n in range(len(a11_alternatives[a11_x])):
        a11_ppl += a11_crews * math.ceil(a11_alternatives[a11_x][n][2])
    a11_ticket_cost = a11_ppl * air_ticket_cost * 2
    a11_equip_weight = 0
    for m in range(len(a11_alternatives[a11_x])):
        a11_equip_weight += a11_crews * a11_alternatives[a11_x][m][3]
    if a11_equip_weight <= 80000:
        a11_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a11_equip_weight <= 150000:
        a11_weight_cost = mobilize_duration * B34K_cost
    else:
        a11_weight_cost = mobilize_duration * B34K_cost * math.ceil(a11_equip_weight / 150000)
    a11_cost = a11_crews * a11_duration * a11_working_hours * a11_hourly_cost + a11_ticket_cost + a11_weight_cost
    a11_start = a10_stop
    a11_stop = a11_start + datetime.timedelta(a11_duration)
    # CAST-IN-PLACE PIERS 2
    a12_working_hours = 8
    a12_quantity = 2 * 1674.18  # CY
    a12_quantity_SFCA = 2 * 10979.19  # SFCA
    a12_quantity_Ton = 2 * 219.8  # Ton
    if a6_x == 0:
        a12_allowable_duration = (tw5_start - tw4_start).days/2
        a12_start = tw4_start
    else:
        a12_allowable_duration = (tw1_stop - a11_stop).days
        a12_start = a11_stop
    # Productivity
    if len(a12_alternatives[a12_x]) == 2:
        a12_productivity = a12_alternatives[a12_x][0][0]
    else:
        a12_productivity = a12_quantity / ((a12_quantity_SFCA / a12_alternatives[a12_x][0][0] + a12_quantity_Ton /
                                          a12_alternatives[a12_x][1][0] + a12_quantity / a12_alternatives[a12_x][2][
                                              0]) / a12_working_hours) / a12_working_hours
    a12_hourly_cost = 0
    for i in range(len(a12_alternatives[a12_x])):
        a12_hourly_cost += a12_alternatives[a12_x][i][1]
    a12_initial_duration = a12_quantity / a12_productivity / a12_working_hours
    if a12_initial_duration < a12_allowable_duration:
        a12_crews = 1
        a12_duration = math.ceil(a12_initial_duration)
    else:
        a12_crews = math.ceil(a12_initial_duration / a12_allowable_duration)
        a12_duration = math.ceil(a12_quantity / a12_productivity / a12_working_hours / a12_crews)
    a12_ppl = 0
    for n in range(len(a12_alternatives[a12_x])):
        a12_ppl += a12_crews * math.ceil(a12_alternatives[a12_x][n][2])
    a12_ticket_cost = a12_ppl * air_ticket_cost * 2
    a12_equip_weight = 0
    for m in range(len(a12_alternatives[a12_x])):
        a12_equip_weight += a12_crews * a12_alternatives[a12_x][m][3]
    if a12_equip_weight <= 80000:
        a12_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a12_equip_weight <= 150000:
        a12_weight_cost = mobilize_duration * B34K_cost
    else:
        a12_weight_cost = mobilize_duration * B34K_cost * math.ceil(a12_equip_weight / 150000)
    a12_cost = a12_crews * a12_duration * a12_working_hours * a12_hourly_cost + a12_ticket_cost + a12_weight_cost
    a12_stop = a12_start + datetime.timedelta(a12_duration)

    # INSTALL GIRDERS 1
    a13_working_hours = 8
    if a6_x == 0:
        a13_x = 0
        a13_quantity = 1296  # Imperial ton (half of the bridge)
        a13_allowable_duration = (tw5_stop - a12_stop).days/2
        a13_productivity = a6_alternatives[a6_x][0][0]
        a13_initial_duration = a13_quantity / a13_productivity / a13_working_hours
        if a13_initial_duration < a13_allowable_duration:
            a13_crews = 2
            a13_duration = math.ceil(a13_initial_duration)
        else:
            a13_crews = math.ceil(a13_initial_duration / a13_allowable_duration)
            a13_duration = math.ceil(a13_quantity / a13_productivity / a13_working_hours / a13_crews)
        a13_name = 'a13_install_girders_depends_on_[8, 12]'
        a13_hourly_cost = 0
        for i in range(len(a6_alternatives[a6_x])):
            a13_hourly_cost += a6_alternatives[a6_x][i][1]
        a13_duration = a13_quantity / a13_productivity / a13_crews / a13_working_hours
        a13_ppl = 0
        for n in range(len(a6_alternatives[a6_x])):
            a13_ppl += a13_crews * math.ceil(a6_alternatives[a6_x][n][2])
        a13_ticket_cost = a13_ppl * air_ticket_cost * 2
        a13_equip_weight = 0
        for m in range(len(a6_alternatives[a6_x])):
            a13_equip_weight += a13_crews * a6_alternatives[a6_x][m][3]
        if a13_equip_weight <= 80000:
            a13_weight_cost = mobilize_duration * B34N_cost
        elif 80000 < a13_equip_weight <= 150000:
            a13_weight_cost = mobilize_duration * B34K_cost
        else:
            a13_weight_cost = mobilize_duration * B34K_cost * math.ceil(a13_equip_weight / 150000)
        a13_cost = a13_crews * a13_duration * a13_working_hours * a13_hourly_cost + a13_ticket_cost + a13_weight_cost
        a13_start = a12_stop
        a13_stop = a13_start + datetime.timedelta(a13_duration)
    else:
        a13_duration, a13_cost, a13_productivity, a13_crews, a13_x, a13_ppl = 0, 0, 0, 0, 1, 0

    # REMOVE BERM 2
    a14_working_hours = 8
    a14_quantity = 88752  # BCY
    a14_name = 'a14_remove_berm'
    if a6_x == 1:  # In case of incremental launching
        a14_allowable_duration = tw3_duration.days
        a14_start = tw3_start
    else:
        a14_allowable_duration = (tw5_stop - a13_stop).days
        a14_start = a13_stop + datetime.timedelta(1)
    a14_productivity = min(a14_alternatives[a14_x][0][0], a14_alternatives[a14_x][2][0])
    a14_truck_crews = math.ceil(
        a14_productivity / (a14_alternatives[a14_x][1][0] / 1.25))  # 1.25 - bank to loose conversion factor
    a14_hourly_cost = (a14_alternatives[a14_x][0][1] + a14_truck_crews * a14_alternatives[a14_x][1][1] +
                      a14_alternatives[a14_x][2][1])
    a14_initial_duration = a14_quantity / a14_productivity / a14_working_hours
    if a14_initial_duration < a14_allowable_duration:
        a14_crews = 1
        a14_duration = math.ceil(a14_initial_duration)
    else:
        a14_crews = math.ceil(a14_initial_duration / a14_allowable_duration)
        a14_duration = math.ceil(a14_quantity / a14_productivity / a14_working_hours / a14_crews)
    a14_ppl = math.ceil(
        a14_alternatives[a14_x][0][2] + a14_alternatives[a14_x][1][2] * a14_truck_crews + a14_alternatives[a14_x][2][
            2]) * a14_crews
    a14_ticket_cost = a14_ppl * air_ticket_cost * 2
    a14_equip_weight = math.ceil(
        a14_alternatives[a14_x][0][3] + a14_alternatives[a14_x][1][3] * a14_truck_crews + a14_alternatives[a14_x][2][
            3]) * a14_crews
    if a14_equip_weight <= 80000:  # Crew B-34N
        a14_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a14_equip_weight <= 150000:  # Crew B-34K
        a14_weight_cost = mobilize_duration * B34K_cost
    else:
        a14_weight_cost = mobilize_duration * B34K_cost * math.ceil(a14_equip_weight / 150000)
    a14_cost = a14_crews * a14_duration * a14_working_hours * a14_hourly_cost + a14_ticket_cost + a14_weight_cost
    a14_stop = a14_start + datetime.timedelta(a14_duration)

    # CAST-IN-PLACE DECK
    a15_working_hours = 8
    a15_quantity = 72656  # SF
    a15_quantity_SFCA = 72656 + 2940 + 98  # SFCA of slab bottom plus edges
    a15_quantity_Ton = 625.9  # Ton
    if a6_x == 0:
        a15_allowable_duration = (tw4_stop - a13_stop).days
        a15_start = a13_stop + datetime.timedelta(1)
    else:
        a15_allowable_duration = tw4_duration.days
        a15_start = tw4_start
    # Productivity
    if len(a15_alternatives[a15_x]) == 2:
        a15_productivity = a15_alternatives[a15_x][0][0]
    else:
        a15_productivity = a15_quantity / (a15_quantity_SFCA / a15_alternatives[a15_x][0][0] + a15_quantity_Ton /
                                           a15_alternatives[a15_x][1][0] + a15_quantity / a15_alternatives[a15_x][2][0])
    a15_hourly_cost = 0
    for i in range(len(a15_alternatives[a15_x])):
        a15_hourly_cost += a15_alternatives[a15_x][i][1]
    a15_initial_duration = a15_quantity / a15_productivity / a15_working_hours
    if a15_initial_duration < a15_allowable_duration:
        a15_crews = 1
        a15_duration = math.ceil(a15_initial_duration)
    else:
        a15_crews = math.ceil(a15_initial_duration / a15_allowable_duration)
        a15_duration = math.ceil(a15_quantity / a15_productivity / a15_working_hours / a15_crews)
    a15_ppl = 0
    for n in range(len(a15_alternatives[a15_x])):
        a15_ppl += a15_crews * math.ceil(a15_alternatives[a15_x][n][2])
    a15_ticket_cost = a15_ppl * air_ticket_cost * 2
    a15_equip_weight = 0
    for m in range(len(a15_alternatives[a15_x])):
        a15_equip_weight += a15_crews * a15_alternatives[a15_x][m][3]
    if a15_equip_weight <= 80000:
        a15_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a15_equip_weight <= 150000:
        a15_weight_cost = mobilize_duration * B34K_cost
    else:
        a15_weight_cost = mobilize_duration * B34K_cost * math.ceil(a15_equip_weight / 150000)
    a15_cost = a15_crews * a15_duration * a15_working_hours * a15_hourly_cost + a15_ticket_cost + a15_weight_cost
    a15_stop = a15_start + datetime.timedelta(a15_duration)

   # Total duration estimation
    work_duration = (a15_stop - a0_start).days

    # Draw schedule
    if iter <= schedules_to_print:
        tw0 = gantt.Task(name='tw0_winter_road',
                         start=tw0_start,
                         stop=tw0_stop,
                         duration=None,
                         percent_done=None,
                         resources=None,
                         color="#ADD8E6",
                         depends_of=None)
        tw1 = gantt.Task(name='tw1_thawing',
                         start=tw1_start,
                         stop=tw1_stop,
                         duration=None,
                         percent_done=None,
                         resources=None,
                         color="#ADD8E6",
                         depends_of=None)
        tw2 = gantt.Task(name='tw2_in_river_activity',
                         start=tw2_start,
                         stop=tw2_stop,
                         duration=None,
                         percent_done=None,
                         resources=None,
                         color="#ADD8E6",
                         depends_of=None)
        tw3 = gantt.Task(name='tw3_winter_road',
                         start=tw3_start,
                         stop=tw3_stop,
                         duration=None,
                         percent_done=None,
                         resources=None,
                         color="#ADD8E6",
                         depends_of=None)
        tw4 = gantt.Task(name='tw4_thawing',
                         start=tw4_start,
                         stop=tw4_stop,
                         duration=None,
                         percent_done=None,
                         resources=None,
                         color="#ADD8E6",
                         depends_of=None)
        tw5 = gantt.Task(name='tw5_in_river_activity',
                         start=tw5_start,
                         stop=tw5_stop,
                         duration=None,
                         percent_done=None,
                         resources=None,
                         color="#ADD8E6",
                         depends_of=None)
        a0 = gantt.Task(name='a0_mobilize_job_site',
                        start=a0_start,
                        stop=a0_stop,
                        duration=a0_duration,
                        percent_done=None,
                        resources=None,
                        color="#FF8080",
                        depends_of=None)
        a1 = gantt.Task(name='a1_build_berm',
                        start=a1_start,
                        stop=a1_stop,
                        duration=a1_duration,
                        percent_done=None,
                        resources=None,
                        color="#FF8080",
                        depends_of=a0)
        a2 = gantt.Task(name='a2_install_piles',
                        start=a2_start,
                        stop=a2_stop,
                        duration=a2_duration,
                        percent_done=None,
                        resources=None,
                        color="#FF8080",
                        depends_of=a1)
        a3 = gantt.Task(name='a3_cast-in-place_piers',
                        start=a3_start,
                        stop=a3_stop,
                        duration=a3_duration,
                        percent_done=None,
                        resources=None,
                        color="#FF8080",
                        depends_of=a2)
        a4 = gantt.Task(name='a4_abutment_base',
                        start=a4_start,
                        stop=None,
                        duration=a4_duration,
                        percent_done=None,
                        resources=None,
                        color="#FF8080",
                        depends_of=a1)
        a5 = gantt.Task(name='a5_cast-in-place_abutment',
                        start=a5_start,
                        stop=None,
                        duration=a5_duration,
                        percent_done=None,
                        resources=None,
                        color="#FF8080",
                        depends_of=a4)
        a6 = gantt.Task(name=a6_name,
                        start=a6_start,
                        stop=None,
                        duration=a6_duration,
                        percent_done=None,
                        resources=None,
                        color="#FF8080",
                        depends_of=[a3, a5])
        a7 = gantt.Task(name='a7_abutment_base',
                        start=a7_start,
                        stop=None,
                        duration=a7_duration,
                        percent_done=None,
                        resources=None,
                        color="#f4aa80",
                        depends_of=a5)
        a8 = gantt.Task(name='a8_cast-in-place_abutment',
                        start=a8_start,
                        stop=None,
                        duration=a8_duration,
                        percent_done=None,
                        resources=None,
                        color="#f4aa80",
                        depends_of=a7)
        if a6_x == 1:  # In case of incremental launching
            a9_dependence = a3
        else:
            a9_dependence = a6
        a9 = gantt.Task(name=a9_name,
                        start=a9_start,
                        stop=None,
                        duration=a9_duration,
                        percent_done=None,
                        resources=None,
                        color="#f4aa80",
                        depends_of=a9_dependence)
        a10 = gantt.Task(name='a10_build_berm',
                         start=a10_start,
                         stop=None,
                         duration=a10_duration,
                         percent_done=None,
                         resources=None,
                         color="#f4aa80",
                         depends_of=a9)
        a11 = gantt.Task(name='a11_install_piles',
                         start=a11_start,
                         stop=None,
                         duration=a11_duration,
                         percent_done=None,
                         resources=None,
                         color="#f4aa80",
                         depends_of=a10)
        a12 = gantt.Task(name='a12_cast-in-place_piers',
                         start=a12_start,
                         stop=None,
                         duration=a12_duration,
                         percent_done=None,
                         resources=None,
                         color="#f4aa80",
                         depends_of=a11)
        if a6_x == 0:
            a13 = gantt.Task(name=a13_name,
                             start=a13_start,
                             stop=None,
                             duration=a13_duration,
                             percent_done=None,
                             resources=None,
                             color="#f4aa80",
                             depends_of=[a8, a12])
        else:
            a13 = gantt.Task(name=' ',
                             start=tw0_start,
                             stop=None,
                             duration=1,
                             percent_done=None,
                             resources=None,
                             color="#FFFFFF")
        if a6_x == 1:  # In case of incremental launching
            a14_dependence = a12
        else:
            a14_dependence = a13
        a14 = gantt.Task(name=a14_name,
                         start=a14_start,
                         stop=None,
                         duration=a14_duration,
                         percent_done=None,
                         resources=None,
                         color="#f4aa80",
                         depends_of=a14_dependence)
        if a6_x == 0:
            a15_dependence = a13
        else:
            a15_dependence = a6
        a15 = gantt.Task(name='a15_cast-in-place_deck',
                         start=a15_start,
                         stop=None,
                         duration=a15_duration,
                         percent_done=None,
                         resources=None,
                         color="#f4aa80",
                         depends_of=a15_dependence)
        # Add time-windows to schedule
        time_windows = gantt.Project(name='Time windows')
        time_windows.add_task(tw0)
        time_windows.add_task(tw1)
        time_windows.add_task(tw2)
        time_windows.add_task(tw3)
        time_windows.add_task(tw4)
        time_windows.add_task(tw5)
        # Add activities to schedule
        bridge_side_1 = gantt.Project(name='Side 1')
        bridge_side_1.add_task(a0),
        bridge_side_1.add_task(a1)
        bridge_side_1.add_task(a4)
        bridge_side_1.add_task(a5)
        bridge_side_1.add_task(a2)
        bridge_side_1.add_task(a3)
        bridge_side_1.add_task(a6)
        bridge_side_2 = gantt.Project(name='Side 2')
        bridge_side_2.add_task(a7)
        bridge_side_2.add_task(a8)
        bridge_side_2.add_task(a9)
        bridge_side_2.add_task(a10)
        bridge_side_2.add_task(a11)
        bridge_side_2.add_task(a12)
        bridge_side_2.add_task(a13)
        bridge_side_2.add_task(a14)
        bridge_side_2.add_task(a15)
        # Create schedule
        schedule = gantt.Project(name='Bridge')
        schedule.add_task(time_windows)
        schedule.add_task(bridge_side_1)
        schedule.add_task(bridge_side_2)
        schedule.make_svg_for_tasks(filename='run ' + str(iter+1) + '.svg',
                                today=None,
                                start=datetime.date(2022, 10, 1),
                                end=datetime.date(2025, 1, 2),
                                scale=gantt.DRAW_WITH_WEEKLY_SCALE)

    # Cost of temporary facilities
    if a6_x == 0:
        max_ppl = max(a1_ppl, a2_ppl, a3_ppl + a4_ppl, a3_ppl + a5_ppl, a3_ppl + a7_ppl, a3_ppl + a8_ppl, a14_ppl + a15_ppl,
            a6_ppl, a9_ppl, a10_ppl, a11_ppl, a12_ppl, a13_ppl)
    else:
        max_ppl = max(a1_ppl, a2_ppl, a3_ppl + a4_ppl, a3_ppl + a5_ppl, a3_ppl + a7_ppl, a6_ppl + a8_ppl, a15_ppl,
                      a6_ppl + a9_ppl, a6_ppl + a10_ppl, a6_ppl + a11_ppl, a6_ppl + a12_ppl, a6_ppl + a13_ppl, a6_ppl + a14_ppl)
    if max_ppl <= 9:  # 9 man bunk house trailer $42,900 to buy (p. 17 line 015213.200910)
        temp_cost = 42900
    else:  # 18 man bunk house trailer $55,000 to buy
        temp_cost = round(max_ppl/ 18* 55000, 0)
    # Indirect costs
    indirect_cost = work_duration * 10000
    bonus = (work_duration - 634) * 10000
    total_cost = round((a1_cost + a2_cost + a3_cost + a4_cost + a5_cost + a6_cost + a7_cost + a8_cost + a9_cost +
                        a10_cost + a11_cost + a12_cost + a13_cost + a14_cost + a15_cost + temp_cost + indirect_cost +
                        bonus), 0)

    # Data collection
    if data_mode == 1:
        a1_alternative_list.append(a1_x), a1_duration_list.append(a1_duration), a1_cost_list.append(round(a1_cost, 0)), a1_crews_list.append(a1_crews)
        a2_alternative_list.append(a2_x), a2_duration_list.append(a2_duration), a2_cost_list.append(round(a2_cost, 0)), a2_crews_list.append(a2_crews)
        a3_alternative_list.append(a3_x), a3_duration_list.append(a3_duration), a3_cost_list.append(round(a3_cost, 0)), a3_crews_list.append(a3_crews)
        a4_alternative_list.append(a4_x), a4_duration_list.append(a4_duration), a4_cost_list.append(round(a4_cost, 0)), a4_crews_list.append(a4_crews)
        a5_alternative_list.append(a5_x), a5_duration_list.append(a5_duration), a5_cost_list.append(round(a5_cost, 0)), a5_crews_list.append(a5_crews)
        a6_alternative_list.append(a6_x), a6_duration_list.append(a6_duration), a6_cost_list.append(round(a6_cost, 0)), a6_crews_list.append(a6_crews)
        a7_alternative_list.append(a7_x), a7_duration_list.append(a7_duration), a7_cost_list.append(round(a7_cost, 0)), a7_crews_list.append(a7_crews)
        a8_alternative_list.append(a8_x), a8_duration_list.append(a8_duration), a8_cost_list.append(round(a8_cost, 0)), a8_crews_list.append(a8_crews)
        a9_alternative_list.append(a9_x), a9_duration_list.append(a9_duration), a9_cost_list.append(round(a9_cost, 0)), a9_crews_list.append(a9_crews)
        a10_alternative_list.append(a10_x), a10_duration_list.append(a10_duration), a10_cost_list.append(round(a10_cost, 0)), a10_crews_list.append(a10_crews)
        a11_alternative_list.append(a11_x), a11_duration_list.append(a11_duration), a11_cost_list.append(round(a11_cost, 0)), a11_crews_list.append(a11_crews)
        a12_alternative_list.append(a12_x), a12_duration_list.append(a12_duration), a12_cost_list.append(round(a12_cost, 0)), a12_crews_list.append(a12_crews)
        a13_alternative_list.append(a13_x), a13_duration_list.append(a13_duration), a13_cost_list.append(round(a13_cost, 0)), a13_crews_list.append(a13_crews)
        a14_alternative_list.append(a14_x), a14_duration_list.append(a14_duration), a14_cost_list.append(round(a14_cost, 0)), a14_crews_list.append(a14_crews)
        a15_alternative_list.append(a15_x), a15_duration_list.append(a15_duration), a15_cost_list.append(round(a15_cost, 0)), a15_crews_list.append(a15_crews)
        work_duration_list.append(work_duration)
        total_cost_list.append(total_cost)
        tw0_duration_list.append(tw0_duration.days), tw1_duration_list.append(tw1_duration.days), tw3_duration_list.append(tw3_duration.days), tw4_duration_list.append(tw4_duration.days)
        tw0_st_list.append(tw0_start.timetuple().tm_yday), tw0_sp_list.append(tw0_stop.timetuple().tm_yday), tw1_st_list.append(tw1_start.timetuple().tm_yday), tw1_sp_list.append(tw1_stop.timetuple().tm_yday)
        tw3_st_list.append(tw3_start.timetuple().tm_yday), tw3_sp_list.append(tw3_stop.timetuple().tm_yday), tw4_st_list.append(tw4_start.timetuple().tm_yday), tw4_sp_list.append(tw4_stop.timetuple().tm_yday)

    # REWARD VALUES FOR EACH ALTERNATIVE
    if a1_x == 0: a1_r1 += total_cost/1000000; a1_o1 += 1
    elif a1_x == 1: a1_r2 += total_cost / 1000000; a1_o2 += 1
    else: a1_r3 += total_cost / 1000000; a1_o3 += 1
    if a2_x == 0: a2_r1 += total_cost/1000000; a2_o1 += 1
    elif a2_x == 1: a2_r2 += total_cost / 1000000; a2_o2 += 1
    else: a2_r3 += total_cost / 1000000; a2_o3 += 1
    if a3_x == 0: a3_r1 += total_cost/1000000; a3_o1 += 1
    elif a3_x == 1: a3_r2 += total_cost / 1000000; a3_o2 += 1
    else: a3_r3 += total_cost / 1000000; a3_o3 += 1
    if a4_x == 0: a4_r1 += total_cost/1000000; a4_o1 += 1
    elif a4_x == 1: a4_r2 += total_cost / 1000000; a4_o2 += 1
    else: a4_r3 += total_cost / 1000000; a4_o3 += 1
    if a5_x == 0: a5_r1 += total_cost/1000000; a5_o1 += 1
    elif a5_x == 1: a5_r2 += total_cost / 1000000; a5_o2 += 1
    else: a5_r3 += total_cost / 1000000; a5_o3 += 1
    if a6_x == 0: a6_r1 += total_cost/1000000; a6_o1 += 1
    elif a6_x == 1: a6_r2 += total_cost / 1000000; a6_o2 += 1
    if a7_x == 0: a7_r1 += total_cost/1000000; a7_o1 += 1
    elif a7_x == 1: a7_r2 += total_cost / 1000000; a7_o2 += 1
    else: a7_r3 += total_cost / 1000000; a7_o3 += 1
    if a8_x == 0: a8_r1 += total_cost/1000000; a8_o1 += 1
    elif a8_x == 1: a8_r2 += total_cost / 1000000; a8_o2 += 1
    else: a8_r3 += total_cost / 1000000; a8_o3 += 1
    if a9_x == 0: a9_r1 += total_cost/1000000; a9_o1 += 1
    elif a9_x == 1: a9_r2 += total_cost / 1000000; a9_o2 += 1
    else: a9_r3 += total_cost / 1000000; a9_o3 += 1
    if a10_x == 0: a10_r1 += total_cost/1000000; a10_o1 += 1
    elif a10_x == 1: a10_r2 += total_cost / 1000000; a10_o2 += 1
    else: a10_r3 += total_cost / 1000000; a10_o3 += 1
    if a11_x == 0: a11_r1 += total_cost/1000000; a11_o1 += 1
    elif a11_x == 1: a11_r2 += total_cost / 1000000; a11_o2 += 1
    else: a11_r3 += total_cost / 1000000; a11_o3 += 1
    if a12_x == 0: a12_r1 += total_cost/1000000; a12_o1 += 1
    elif a12_x == 1: a12_r2 += total_cost / 1000000; a12_o2 += 1
    else: a12_r3 += total_cost / 1000000; a12_o3 += 1
    if a13_x == 0: a13_r1 += total_cost/1000000; a13_o1 += 1
    elif a13_x == 1: a13_r2 += total_cost / 1000000; a13_o2 += 1
    if a14_x == 0: a14_r1 += total_cost/1000000; a14_o1 += 1
    elif a14_x == 1: a14_r2 += total_cost / 1000000; a14_o2 += 1
    else: a14_r3 += total_cost / 1000000; a14_o3 += 1
    if a15_x == 0: a15_r1 += total_cost/1000000; a15_o1 += 1
    elif a15_x == 1: a15_r2 += total_cost / 1000000; a15_o2 += 1

    if iter == 0:
        min_total_cost = total_cost
        max_total_cost = total_cost
    if total_cost < min_total_cost: min_total_cost = total_cost
    if total_cost > max_total_cost: max_total_cost = total_cost

try:
    a1_R1 = a1_r1/a1_o1; a1_R2 = a1_r2/a1_o2; a1_R3 = a1_r3/a1_o3
    a2_R1 = a2_r1/a2_o1; a2_R2 = a2_r2/a2_o2; a2_R3 = a2_r3/a2_o3
    a3_R1 = a3_r1/a3_o1; a3_R2 = a3_r2/a3_o2; a3_R3 = a3_r3/a3_o3
    a4_R1 = a4_r1/a4_o1; a4_R2 = a4_r2/a4_o2; a4_R3 = a4_r3/a4_o3
    a5_R1 = a5_r1/a5_o1; a5_R2 = a5_r2/a5_o2; a5_R3 = a5_r3/a5_o3
    a6_R1 = a6_r1/a6_o1; a6_R2 = a6_r2/a6_o2
    a7_R1 = a7_r1/a7_o1; a7_R2 = a7_r2/a7_o2; a7_R3 = a7_r3/a7_o3
    a8_R1 = a8_r1/a8_o1; a8_R2 = a8_r2/a8_o2; a8_R3 = a8_r3/a8_o3
    a9_R1 = a9_r1/a9_o1; a9_R2 = a9_r2/a9_o2; a9_R3 = a9_r3/a9_o3
    a10_R1 = a10_r1/a10_o1; a10_R2 = a10_r2/a10_o2; a10_R3 = a10_r3/a10_o3
    a11_R1 = a11_r1/a11_o1; a11_R2 = a11_r2/a11_o2; a11_R3 = a11_r3/a11_o3
    a12_R1 = a12_r1/a12_o1; a12_R2 = a12_r2/a12_o2; a12_R3 = a12_r3/a12_o3
    a13_R1 = a13_r1/a13_o1; a13_R2 = a13_r2/a13_o2
    a14_R1 = a14_r1/a14_o1; a14_R2 = a14_r2/a14_o2; a14_R3 = a14_r3/a14_o3
    a15_R1 = a15_r1/a15_o1; a15_R2 = a15_r2/a15_o2

    R = [a1_R1, a1_R2, a1_R3, a2_R1, a2_R2, a2_R3, a3_R1, a3_R2, a3_R3, a4_R1, a4_R2, a4_R3, a5_R1, a5_R2, a5_R3,
     a6_R1, a6_R2, a7_R1, a7_R2, a7_R3, a8_R1, a8_R2, a8_R3, a9_R1, a9_R2, a9_R3, a10_R1, a10_R2, a10_R3, 
     a11_R1, a11_R2, a11_R3, a12_R1, a12_R2, a12_R3, a13_R1, a13_R2, a14_R1, a14_R2, a14_R3, a15_R1, a15_R2]

    output = list(zip(R))
    df = pd.DataFrame(output, index=["a1_berm_0", "a1_berm_1", "a1_berm_2", "a2_piles_0", "a2_piles_1", "a2_piles_2", "a3_piers_0", "a3_piers_1", "a3_piers_2", "a4_abutment_base_0", "a4_abutment_base_1", "a4_abutment_base_2", "a5_abutment_0", "a5_abutment_1",
    "a5_abutment_2", "a6_girders_0", "a6_girders_1", "a7_abutment_base2_0", "a7_abutment_base2_1", "a7_abutment_base2_2", "a8_abutment2_0", "a8_abutment2_1", "a8_abutment2_2", "a9_remove_berm_0", "a9_remove_berm_1",
    "a9_remove_berm_2", "a10_berm2_0", "a10_berm2_1", "a10_berm2_2", "a11_piles2_0", "a11_piles2_1", "a11_piles2_2", "a12_piers2_0", "a12_piers2_1", "a12_piers2_2", "a13_girders2_0", "a13_girders2_1", "a14_remove_berm2_0", "a14_remove_berm2_1", "a14_remove_berm2_2",
    "a15_deck_0", "a15_deck_1"], columns=["total_$ (m)"])
    df["reward"] = round(1 + ((df["total_$ (m)"] - df["total_$ (m)"].min()) * (-1))/(df["total_$ (m)"].max()-df["total_$ (m)"].min()), 3)
    print(df.to_string())
    df.to_csv('algo3.csv')
    print('Simulation is complete')
except:
    print('Not all the scenarios executed. Simulation is terminated. Increase number of runs.')
    print('Limited results:')
if data_mode == 1:
    list = list(zip(a1_alternative_list, a1_duration_list, a1_cost_list, a1_crews_list, a2_alternative_list,
                    a2_duration_list, a2_cost_list, a2_crews_list, a3_alternative_list, a3_duration_list,
                    a3_cost_list, a3_crews_list, a4_alternative_list, a4_duration_list, a4_cost_list, a4_crews_list,
                    a5_alternative_list, a5_duration_list, a5_cost_list, a5_crews_list, a6_alternative_list,
                    a6_duration_list, a6_cost_list, a6_crews_list, a7_alternative_list, a7_duration_list,
                    a7_cost_list, a7_crews_list, a8_alternative_list, a8_duration_list, a8_cost_list, a8_crews_list,
                    a9_alternative_list, a9_duration_list, a9_cost_list, a9_crews_list, a10_alternative_list,
                    a10_duration_list, a10_cost_list, a10_crews_list, a11_alternative_list, a11_duration_list,
                    a11_cost_list, a11_crews_list, a12_alternative_list, a12_duration_list, a12_cost_list,
                    a12_crews_list, a13_alternative_list, a13_duration_list, a13_cost_list, a13_crews_list,
                    a14_alternative_list, a14_duration_list, a14_cost_list, a14_crews_list, a15_alternative_list,
                    a15_duration_list, a15_cost_list, a15_crews_list, work_duration_list, total_cost_list,
                    tw0_duration_list, tw1_duration_list, tw3_duration_list, tw4_duration_list, tw0_st_list, tw0_sp_list,
                    tw1_st_list, tw1_sp_list, tw3_st_list, tw3_sp_list, tw4_st_list, tw4_sp_list,))
    df = pd.DataFrame(list, columns=["a1_berm", "a1_t", "a1_$", "a1_c",
                                     "a2_piles", "a2_t", "a2_$", "a2_c",
                                     "a3_piers", "a3_t", "a3_$", "a3_c",
                                     "a4_abutment_base", "a4_t", "a4_$", "a4_c",
                                     "a5_abutment", "a5_t", "a5_$", "a5_c",
                                     "a6_girders", "a6_t", "a6_$", "a6_c",
                                     "a7_abutment_base2", "a7_t", "a7_$", "a7_c",
                                     "a8_abutment2", "a8_t", "a8_$", "a8_c",
                                     "a9_remove_berm", "a9_t", "a9_$", "a9_c",
                                     "a10_berm2", "a10_t", "a10_$", "a10_c",
                                     "a11_piles2", "a11_t", "a11_$", "a11_c",
                                     "a12_piers2", "a12_t", "a12_$", "a12_c",
                                     "a13_girders2", "a13_t", "a13_$", "a13_c",
                                     "a14_remove_berm2", "a14_t", "a14_$", "a14_c",
                                     "a15_deck", "a15_t", "a15_$", "a15_c",
                                     "total_t", "total_$", "tw0", "tw1", "tw3", "tw4", "tw0_st", "tw0_sp",
                                     "tw1_st", "tw1_sp", "tw3_st", "tw3_sp", "tw4_st", "tw4_sp"])
    print('Encountered', format(df.shape[0] - df.drop_duplicates(subset=['total_$']).shape[0], ',d'), 'cost duplicates')
    print('and', format(df.shape[0] - df.drop_duplicates().shape[0], ',d'), 'tw duplicates')
    print('Simulation efficiency is', round(100 - 100 / number_of_runs * (df.shape[0] - df.drop_duplicates(subset=['total_$']).shape[0]), 3), '%')
    df = df.drop_duplicates(subset=['total_$'])
    print('Duplicates dropped')
    if number_of_runs <= 100:
        print(df.to_string())
    df.to_csv('data.csv')
print('Maximum cost', round(max_total_cost/1000000, 3), 'm $')
print('Minimum cost', round(min_total_cost/1000000, 3), 'm $')
print('-----------------------------------------------------------------------')
print(bar)
