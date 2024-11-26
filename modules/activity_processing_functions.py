# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 17:00:21 2024

@author: joshm
"""
import os
os.chdir("C:/Users/joshm/OneDrive/activity_tracker")


import statistics as stats
import numpy as np

# Create dictionary with time(s) spent in each zone
def pwrZonesDict(df, athlete):
    
    dic = {"z1": 0, "z2": 0, "z3": 0, "z4": 0, "z5": 0, "z6": 0, "z7": 0}

    for i in range(len(df["power"]) - 1):
        
        power = df["power"].iloc[i]
        time_spent = df["elapsed_time"].iloc[i + 1] - df["elapsed_time"].iloc[i]

        if power < athlete.pwr_zone1[1]:
            dic["z1"] += time_spent
        elif athlete.pwr_zone2[0] <= power <= athlete.pwr_zone2[1]:
            dic["z2"] += time_spent
        elif athlete.pwr_zone3[0] <= power <= athlete.pwr_zone3[1]:
            dic["z3"] += time_spent
        elif athlete.pwr_zone4[0] <= power <= athlete.pwr_zone4[1]:
            dic["z4"] += time_spent
        elif athlete.pwr_zone5[0] <= power <= athlete.pwr_zone5[1]:
            dic["z5"] += time_spent
        elif athlete.pwr_zone6[0] <= power <= athlete.pwr_zone6[1]:
            dic["z6"] += time_spent
        elif power > athlete.pwr_zone6[1]:
            dic["z7"] += time_spent
    
    return dic

# Create dictionary with time(s) spent in hr zones
# Zones change depending on lthr data
def hrZonesDict(df, athlete):
    
    if not athlete.lthr_hr:
        dic = {"z0": 0, "z1": 0, "z2": 0, "z3": 0, "z4": 0, "z5": 0}
        
        for i in range(len(df["heart_rate"]) - 1):
            
            hr = df["heart_rate"].iloc[i]
            time_spent = df["elapsed_time"].iloc[i + 1] - df["elapsed_time"].iloc[i]
    
            if hr < athlete.hr_zone1[0]:
                dic["z0"] += time_spent
            elif athlete.hr_zone1[0] <= hr <= athlete.hr_zone1[1]:
                dic["z1"] += time_spent
            elif athlete.hr_zone2[0] <= hr <= athlete.hr_zone2[1]:
                dic["z2"] += time_spent
            elif athlete.hr_zone3[0] <= hr <= athlete.hr_zone3[1]:
                dic["z3"] += time_spent
            elif athlete.hr_zone4[0] <= hr <= athlete.hr_zone4[1]:
                dic["z4"] += time_spent
            elif athlete.hr_zone5[0] <= hr <= athlete.hr_zone5[1]:
                dic["z5"] += time_spent
        
    elif athlete.lthr_hr:
        
        dic = {"z1": 0, "z2": 0, "z3": 0, "z4": 0, "z5a": 0, "z5b": 0, "z5c": 0}
        
        for i in range(len(df["heart_rate"]) - 1):
            
            hr = df["heart_rate"].iloc[i]
            time_spent = df["elapsed_time"].iloc[i + 1] - df["elapsed_time"].iloc[i]
    
            if hr < athlete.hr_zone1[0]:
                dic["z1"] += time_spent
            elif athlete.hr_zone1[0] <= hr <= athlete.hr_zone2[1]:
                dic["z2"] += time_spent
            elif athlete.hr_zone2[0] <= hr <= athlete.hr_zone3[1]:
                dic["z3"] += time_spent
            elif athlete.hr_zone3[0] <= hr <= athlete.hr_zone4[1]:
                dic["z4"] += time_spent
            elif athlete.hr_zone4[0] <= hr <= athlete.hr_zone5a[1]:
                dic["z5a"] += time_spent
            elif athlete.hr_zone5a[0] <= hr <= athlete.hr_zone5b[1]:
                dic["z5b"] += time_spent
            elif athlete.hr_zone5b[0] <= hr <= athlete.hr_zone5c[1]:
                dic["z5c"] += time_spent
    return dic
    
# Calculates normalised power (uses formula available on training speaks documentation)
def np_calc(df):
    
    power_series = df['power']
    ave_list = []
    
    n = 0
    while n < len(power_series)-30:
        
        window = power_series[n:n+30]
        window_ave = stats.mean(window)
        ave_list.append(window_ave)
        n += 1
        
    ave_array = np.array(ave_list)
    fourth_power = ave_array ** 4
    mean_fourth_power = stats.mean(fourth_power)
    norm_power = mean_fourth_power ** (1/4)
    
    return norm_power

# Calculates a normalised hr value using the same approach as power
def nhr_calc(df):
    
    hr_series = df['heart_rate']
    ave_list = []
    
    n = 0
    while n < len(hr_series)-30:
        
        window = hr_series[n:n+30]
        window_ave = stats.mean(window)
        ave_list.append(window_ave)
        n += 1
        
    ave_array = np.array(ave_list)
    fourth_hr = ave_array ** 4
    mean_fourth_hr = stats.mean(fourth_hr)
    norm_hr = mean_fourth_hr ** (1/4)
    
    return norm_hr

# Calculates intensity factor as described in training peaks documentation
def if_calc(df, athlete):
    
    norm_power = np_calc(df)
    if_score = norm_power/athlete.ftp
    
    return if_score

# Calculates TSS as described in training peaks documentation
# Formula could be simplified but TP does not for clarity
def TSS_calc(df, athlete):
    
    if_score = if_calc(df, athlete)
    np_score = np_calc(df)
    duration = df['elapsed_time'].max(skipna=True)
    
    tss = ((duration * np_score * if_score) / (athlete.ftp * 3600)) * 100
    
    return tss

#Calculates hrTSS as described in TP documentation
def hrTSS_calc(df, athlete):
    
    zoneTimeDict = hrZonesDict(df, athlete)
    zoneTSShourDict = {"z1": 30, "z2": 55, "z3": 70, 
                       "z4": 80, "z5a": 100, "z5b": 120, "z5c": 140}
    totalTSS = 0
    for key, value in zoneTimeDict.items():
        time_hrs = value / 3600
        zoneTSS = zoneTSShourDict[key]
        zonehrTSS = time_hrs * zoneTSS
        totalTSS += zonehrTSS
    
    return totalTSS

# Calculates Training Impulse score using the Bannister Method as 
# described in Polar documentation
def TRIMP_calc(df, athlete):
    
    if athlete.sex == 'male':
        multiplier = 0.64
        expo = 1.92
    elif athlete.sex == 'female':
        multiplier = 0.86
        expo = 1.67
    else:
        raise ValueError("Sex must be 'male' or 'female'.")
    max_hr = float(athlete.max_hr)
    rest_hr = float(athlete.rest_hr)
    core = (df['heart_rate'] - rest_hr)/(max_hr - rest_hr)
    W = np.sum(core * multiplier * np.exp(expo * core))
    W_min_adj = W/60
    
    return W_min_adj

# Calculates the variability index for power
def pwrVI_calc(df, athlete):
    
    norm_power = np_calc(df)
    power_series = df['power']
    vi = norm_power/stats.mean(power_series)
    
    return vi

# Calculates the variability index for hr
def hrVI_calc(df, athlete):
    
    norm_hr = nhr_calc(df)
    hr_series = df['heart_rate']
    vi = norm_hr/stats.mean(hr_series)
    
    return vi

def activityTime(total_seconds):
    
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"







