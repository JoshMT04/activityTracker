# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 12:35:19 2024

@author: joshm
"""

import os
os.chdir("C:/Users/joshm/OneDrive/activity_tracker")
from modules.activity_processing_functions import *
from modules.activity_plot_functions import *
import statistics as stats

class activity:
    
    def __init__(self, df=None, activity_athlete=None):
        # activity components
        self.df = df
        self.activity_athlete = activity_athlete
        self.plots = {}
        self.time = activityTime(self.df['elapsed_time'].max())
        
        # key power metrics
        if 'power' in self.df.columns:
            self.pwrZoneTimes = pwrZonesDict(self.df, self.activity_athlete)
            self.pwrAVG = stats.mean(self.df['power'])
            self.npwr = np_calc(self.df)
            self.int_fact = if_calc(self.df, self.activity_athlete)
            self.tss = TSS_calc(self.df, self.activity_athlete)
            self.pwrVI = pwrVI_calc(self.df, self.activity_athlete)
            # Plots
            self.plots["pwrDist"] = pwrZonesBar(self.df, self.activity_athlete)
            self.plots["pwrLine"] = statVStime(self.df, self.activity_athlete, "power")
       
        # key hr metrics
        if 'heart_rate' in self.df.columns:
            self.hrZoneTimes = hrZonesDict(self.df, self.activity_athlete)
            self.hrAVG = stats.mean(self.df['heart_rate'])
            self.nhr = nhr_calc(self.df)
            if self.activity_athlete.lthr_hr:
                self.hrTSS = hrTSS_calc(self.df, self.activity_athlete)
            self.TRIMP = TRIMP_calc(self.df, self.activity_athlete)
            self.hrVI = hrVI_calc(self.df, self.activity_athlete)
            # Plots
            self.plots["hrDist"] = hrZonesBar(self.df, self.activity_athlete)
            self.plots["hrLine"] = statVStime(self.df, self.activity_athlete, "heart_rate")
        
    def __repr__(self):
        
        return (f"Your Ride Report:\nActivity Time: {self.time}\n"
                f"Average Power | Normalised Power | VI: {self.pwrAVG} | {self.npwr} | {self.pwrVI}\n"
                f"Average HR | Normalised HR | VI: {self.hrAVG} | {self.nhr} | {self.hrVI}\n"
                f"TSS | IF | TRIMP: {self.tss} | {self.int_fact} | {self.TRIMP}")















            