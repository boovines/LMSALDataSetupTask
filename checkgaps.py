import netCDF4 as nc # https://towardsdatascience.com/read-netcdf-data-with-python-901f7ff61648
# https://www.ngdc.noaa.gov/stp/satellite/goes/doc/GOES_XRS_readme.pdf
# with open("./test2.nc", 'rb') as fp:
from datetime import datetime
import numpy as np
import datetime as dt

import requests
from datetime import date


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plot
import json
from datetime import timedelta


import netCDF4 as nc
import numpy as np
import cftime
import matplotlib.pyplot as plt
from datetime import datetime
import os
import requests
import matplotlib.ticker as ticker


from ncflag import FlagWrap
import math

# fix dates
# count number of same class/mags
#make plot of when discrepancies happen, contact kim tolbert a.01

# create movie making script
# get FIs of top 10 and FIs of 10 random sample avg

# fix srs scrape and make better pkls of SRS data
# fix ar assignment to account for
def getCSV():
    with open(f'newmergedevs5.csv') as f:
        evData = pd.read_csv(f)#csv.reader(f)
    return evData

def convert(f):
    classes = {1: "X", 2: "X", 3: "X", 4:"X", 5: "M", 6:"C", 7: "B", 8: "A", 9: "A", 10: "A", 11: "A"}
    if np.isnan(f):
        return np.nan
    else:
        return f"{classes[(math.log(f,10)-1)//-1]}{round(f*10**(-(math.floor(math.log(f,10)))), 1)}"

def makePlots(d, yher, ynoaa, z1, z2):
    s = [.1 for i in z1]
    fig, ax = plt.subplots(1,1)
    ax.scatter(d, z1, s=s)
    ax.scatter(d, z2, s=s)
    
    tick_spacing = 3000
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    fig.autofmt_xdate()
    plt.show()
    
    # plt.plot(d, yher)
    # plt.plot(d, ynoaa)
    # plt.clos()
    
def getUnaligned():
    df = getCSV()
    count = 0
    count2 = 0
    d = []
    evs1 = []
    evs2 = []
    z1 = []
    z2 = []
    yher = []
    ynoaa = []
    
    for index, ev in df.iterrows():
        d.append(ev["PEAK"])
        try:
            herclass = float(ev["MAGNITUDE_HER"][1:])
        except:
            herclass = 2
        try:
            noaaclass = float(ev["MAGNITUDE_NOAA"][1:])
        except:
            noaaclass = 2
        try:
            newclass = float(convert(ev["NEW_CALIB_FLUX"]*.7)[1:])
        except:
            newclass = 52
        try:
            oldclass = float(ev["OLD_CALIB_MAG"][1:])
        except:
            oldclass = 52
        # print(ev)
        isSameAsOld = ev["MAGNITUDE_HER"] == ev["OLD_CALIB_MAG"] or ev["MAGNITUDE_NOAA"] == ev["OLD_CALIB_MAG"]
        # print(round(float(ev["NEW_CALIB_MAG"][1:])*.7, 1))
        # try:
        isSameAsNew = ev["MAGNITUDE_HER"] == convert(ev["NEW_CALIB_FLUX"]*.7) or ev["MAGNITUDE_NOAA"] == convert(ev["NEW_CALIB_FLUX"]*.7)
        # except:
        #     isSameAsNew=False
        
        if isSameAsOld or isSameAsNew:
            # if np.isnan(ev["OLD_CALIB_MAG"]) and np.isnan(ev["NEW_CALIB_MAG"]):
            #     count2+=1
            # else:
            count+=1
            evs1.append(ev)
            z1.append(1)
            yher.append(0)
            ynoaa.append(0)
        else:
            z1.append(0)
            try:
                yher.append(oldclass-herclass)
                ynoaa.append(oldclass-noaaclass)
            except:
                yher.append(newclass-herclass)
                ynoaa.append(newclass-noaaclass)
        
        
        
        isSameAsOld2 = abs(herclass - oldclass) <= .1 or abs(noaaclass - oldclass) <= .1001
        
        isSameAsNew2 = abs(herclass - newclass) <= .1 or abs(noaaclass - newclass) <= .1001
        
        if isSameAsOld2 or isSameAsNew2:
            # if np.isnan(ev["OLD_CALIB_MAG"]) and np.isnan(ev["NEW_CALIB_MAG"]):
            #     count2+=1
            # else:
            # print("here")
            count2+=1
            evs2.append(ev)
            z2.append(2)
        else:
            z2.append(0)
    
    
    makePlots(d, yher, ynoaa, z1, z2)
    return count, count2

print(getUnaligned())


#         # print(ev["MAGNITUDE_HER"], ev["OLD_CALIB_MAG"] == np.nan)
#         # print(np.isnan(ev["MAGNITUDE_HER"]))
        
#         # print( ev["OLD_CALIB_MAG"] != np.nan, type(ev["OLD_CALIB_MAG"]), type(np.nan))
#         # herclass = float(ev["MAGNITUDE_HER"][1:]) if not ev["MAGNITUDE_HER"] == np.nan else 2
#         # noaaclass = float(ev["MAGNITUDE_NOAA"][1:]) if not ev["MAGNITUDE_NOAA"] == np.nan else 2
#         # newclass = float(convert(ev["NEW_CALIB_FLUX"]*.7)[1:]) if not ev["NEW_CALIB_FLUX"] == np.nan else 6
#         # oldclass = float(ev["OLD_CALIB_MAG"][1:]) if not ev["OLD_CALIB_MAG"] == np.nan else 6
        
#         print(abs(herclass - oldclass))