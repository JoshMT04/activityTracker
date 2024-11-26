# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 18:08:12 2024

@author: joshm
"""

from fitparse import FitFile
import pandas as pd

def FIT_process(file_path):
    
    fit_file = FitFile(f"workout_files/{file_path}")
    
    data_type_list = []
    for record in fit_file.get_messages('record'):
        for data in record:
            if data.name not in data_type_list:
                data_type_list.append(data.name)
            
    df = pd.DataFrame(columns=data_type_list)

    for record in fit_file.get_messages('record'):
        for data in record:
            df.loc[record.get('timestamp'), data.name] = data.value
        
    df.reset_index(inplace=True)
    df = df.drop(['index', 'battery_soc', 'enhanced_altitude', 'enhanced_speed'], axis=1)

    elapsed_times = []
    for time in df["timestamp"]:
        new_time = (time - df["timestamp"].iloc[0]).total_seconds()
        elapsed_times.append(new_time)

    df["elapsed_time"] = elapsed_times
    df["elapsed_time_min"] = df["elapsed_time"].apply(lambda x: x / 60)

    df['power'] = pd.to_numeric(df['power'], errors='coerce')
    
    pd.set_option('future.no_silent_downcasting', True)
    df = df.fillna(0)

    df = df.infer_objects()
    if 'heart_rate' in df.columns:
        df = df[df['heart_rate'] != 0]
    
    gps_scale_factor = 2**31 / 180
    df['latitude'] = df['position_lat'] / gps_scale_factor
    df['longitude'] = df['position_long'] / gps_scale_factor

    return df