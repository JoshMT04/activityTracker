# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 20:26:00 2024

@author: joshm
"""

class Athlete:
    
    def __init__(self, ftp=None, palette=None, max_hr=None, 
                 rest_hr=None, lthr_hr=None, sex=None):
        # power zones
        self.ftp = ftp
        self.pwr_zone1 = (0, self.ftp * 0.55)
        self.pwr_zone2 = (self.ftp * 0.56, self.ftp * 0.75) 
        self.pwr_zone3 = (self.ftp * 0.76, self.ftp * 0.9)
        self.pwr_zone4 = (self.ftp * 0.91, self.ftp * 1.05)
        self.pwr_zone5 = (self.ftp * 1.06, self.ftp * 1.2)
        self.pwr_zone6 = (self.ftp * 1.21, self.ftp * 1.5)
        self.pwr_zone7 = (self.ftp * 1.51)
        # customisation
        self.palette = palette
        self.sex = sex
        # hr zones
        self.max_hr = max_hr
        self.rest_hr = rest_hr
        self.lthr_hr = lthr_hr
        if not self.lthr_hr:
            self.hr_zone0 = (self.rest_hr, self.max_hr * 0.54)
            self.hr_zone1 = (self.max_hr * 0.50, self.max_hr *0.59)
            self.hr_zone2 = (self.max_hr * 0.60, self.max_hr * 0.69)
            self.hr_zone3 = (self.max_hr * 0.70, self.max_hr * 0.79)
            self.hr_zone4 = (self.max_hr * 0.80, self.max_hr * 0.89)
            self.hr_zone5 = (self.max_hr * 0.90, self.max_hr)
        elif self.lthr_hr:
            self.hr_zone1 = (self.rest_hr, self.lthr_hr * 0.81)
            self.hr_zone2 = (self.lthr_hr * 0.82, self.lthr_hr * 0.89)
            self.hr_zone3 = (self.lthr_hr * 0.90, self.lthr_hr * 0.93)
            self.hr_zone4 = (self.lthr_hr * 0.94, self.lthr_hr * 0.99)
            self.hr_zone5a = (self.lthr_hr, self.lthr_hr * 1.02)
            self.hr_zone5b = (self.lthr_hr * 1.03, self.lthr_hr * 1.06)
            self.hr_zone5c = (self.lthr_hr * 1.07)
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         