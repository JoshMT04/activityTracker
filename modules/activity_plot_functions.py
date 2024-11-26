# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 18:17:35 2024

@author: joshm
"""
from modules.activity_processing_functions import *
import matplotlib.pyplot as plt
import gmplot
import pandas as pd
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
import matplotlib.cm as cmx

def pwrZonesBar(df, athlete):
    
    power_zone_dict = pwrZonesDict(df, athlete)
    
    power_zones_df = pd.DataFrame.from_dict(power_zone_dict, orient="index", columns=["Time"])
    power_zones_df.reset_index(inplace=True)
    power_zones_df.columns = ["Zone", "Time"]
    power_zones_df['Time'] = power_zones_df['Time'].apply(lambda x: x/60)
    total_time_s = (df['elapsed_time'].max())/60
    power_zones_df['% Time in Zone'] = power_zones_df['Time'].apply(lambda x: 
                                                                    (x/total_time_s)*100)
    fig, ax = plt.subplots(figsize=(10,6))  
    sns.barplot(data=power_zones_df, x="Zone", y="% Time in Zone", hue="Zone",
                                   palette=athlete.palette)
    plt.ioff()
    
    return fig

def hrZonesBar(df, athlete):
    
    hr_zone_times = hrZonesDict(df, athlete)
    
    hr_zones_df = pd.DataFrame.from_dict(hr_zone_times, orient="index", columns=["Time"])
    hr_zones_df.reset_index(inplace=True)
    hr_zones_df.columns = ["Zone", "Time"]
    hr_zones_df['Time'] = hr_zones_df['Time'].apply(lambda x: x/60)
    total_time_s = (df['elapsed_time'].max())/60
    hr_zones_df['% Time in Zone'] = hr_zones_df['Time'].apply(lambda x: (x/total_time_s)*100)
    
    fig, ax = plt.subplots(figsize=(10,6))
    zone_plot = sns.barplot(data=hr_zones_df, x="Zone", y="% Time in Zone", hue="Zone",
                                   palette=athlete.palette)
    plt.ioff()
    
    return fig

def statVStime(df, athlete, plot_type):
    
    time = df['elapsed_time']
    stat = df[plot_type]

    norm = mcolors.Normalize(vmin=stat.min(), vmax=stat.max())
    cmap = plt.get_cmap('coolwarm')  # Choose a colormap
    scalar_map = cmx.ScalarMappable(norm=norm, cmap=cmap)

    # Create the figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each segment of the line with a different color
    for i in range(len(time) - 1):
        x = [time.iloc[i], time.iloc[i + 1]]
        y = [stat.iloc[i], stat.iloc[i + 1]]
        ax.plot(x, y, color=scalar_map.to_rgba(stat.iloc[i]), linewidth=2)

    # Add a colorbar to indicate stat values
    cbar = fig.colorbar(scalar_map, ax=ax)
    cbar.set_label(plot_type.capitalize())

    # Add labels and title
    ax.set_xlabel("Elapsed Time (s)")
    ax.set_ylabel(plot_type.capitalize())
    ax.set_title(f"{plot_type.capitalize()} vs. Time with Gradient Colors")
    
    return fig

def geoMap(df):
    
    latitudes = df['latitude']
    longitudes = df['longitude']

    gmap = gmplot.GoogleMapPlotter(latitudes.iloc[1000], longitudes.iloc[1000], 12)

    gmap.polygon(latitudes, longitudes, color='pink', edge_width=10)

    gmap.draw('map.html')

def elevMap(df):
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    z = df['altitude']

    ax.scatter(df['longitude'], df['latitude'], z, marker='o')
    ax.plot(df['longitude'], df['latitude'], z, linestyle='-', color='blue') 

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Altitude')

    return fig