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

num_vars = 2
make_plot = 1
ds = nc.Dataset("./2010/g14_xrs_1m_20100101_20100131.nc")
ds2 = nc.Dataset("./goes14onemin.nc")

sat_life = {
        "13": [dt.datetime(2013, 6, 1, 0, 0), dt.datetime(2017, 12, 14, 22, 59)], 
        "14": [dt.datetime(2009, 9, 1, 0, 0), dt.datetime(2020, 3, 4, 22, 59)], 
        "15": [dt.datetime(2010, 9, 28, 0, 0), dt.datetime(2020, 3, 4, 22, 59)],#[dt.datetime(2010, 3, 31, 0, 0), dt.datetime(2020, 3, 4, 22, 59)], 
        "16": [dt.datetime(2017, 2, 7, 0, 0), datetime.now()], 
        "17": [dt.datetime(2018, 6, 1, 0, 0), datetime.now()]
    }
# for var in ds.variables.values():
#     print(var)

def getIndex(arr, low, high, x):
 
    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        if arr[mid] == x:
            print(mid, "sLSJDFSFKJ")
            return mid
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return getIndex(arr, low, mid - 1, x)
 
        # Else the element can only be present in right subarray
        else:
            return getIndex(arr, mid + 1, high, x)
 
    else:
        # Element is not present in the array
        return -1  

# def getSatellites(date):
#     if(dt.datetime(2010,9,1,0,0,0) <= date and date < dt.datetime(2010,10,28,0,0,0)):
#         return ["14", "15"] # not sure about 13
#     elif(dt.datetime(2010,10,28,0,0,0) <= date and date < dt.datetime(2011,9,1,0,0,0)):
#         return ["15", "14"]
#     elif(dt.datetime(2011,9,1,0,0,0) <= date and date < dt.datetime(2012,10,23,16,0,0)):
#         return ["14", "15"]
#     elif(dt.datetime(2012,10,23,16,0,0) <= date and date < dt.datetime(2012,11,19,16,31,0)):
#         return ["15", "14"]
#     elif(dt.datetime(2012,11,19,16,31,0) <= date and date < dt.datetime(2015,1,26,16,1,0)):
#         return ["15", "13"]
#     elif(dt.datetime(2015,1,26,16,1,0) <= date and date < dt.datetime(2015,5,21,18,0,0)):
#         return ["14", "13"]
#     elif(dt.datetime(2015,5,21,18,0,0) <= date and date < dt.datetime(2015,6,9,16,25,0)):
#         return ["15", "13"]
#     elif(dt.datetime(2015,6,9,16,25,0) <= date and date < dt.datetime(2016,5,3,13,0,0)):
#         return ["13", "14"]
#     elif(dt.datetime(2016,5,3,13,0,0) <= date and date < dt.datetime(2016,5,12,17,30,0)):
#         return ["14", "13"]
#     elif(dt.datetime(2016,5,12,17,30,0) <= date and date < dt.datetime(2016,5,16,17,0,0)):
#         return ["14", "15"]
#     elif(dt.datetime(2016,5,16,17,0,0) <= date and date < dt.datetime(2016,6,9,17,30,0)):
#         return ["15", "13"]
#     elif(dt.datetime(2016,6,9,17,30,0) <= date and date < dt.datetime(2017,2,7,0,0,0)):
#         return ["16", "15"]
#     elif(dt.datetime(2017,2,7,0,0,0) <= date and date < dt.datetime(2017,5,30,20,0,0)):
#         return ["16", "15", "13"]
#     elif(dt.datetime(2017,5,30,20,0,0) <= date and date < dt.datetime(2017,8,16,19,15,0)):
#         return ["16", "13", "14"]
#     elif(dt.datetime(2017,8,16,19,15,0) <= date and date < dt.datetime(2017,8,23,21,20,0)):
#         return ["16", "15", "13"]
#     elif(dt.datetime(2017,8,23,21,20,0) <= date and date < dt.datetime(2017,12,12,16,30,0)):
#         return ["16", "15", "14"]
#     else:
#         return ["17", "16", "15"]
    

    
# def getPrimSecList():
#     start = dt.datetime(2010,9,1,0,0,0)
#     end = dt.now()
#     delta = end-start
#     fluxes_new = []
    
#     bestsats = getSatellites(start)
    
#     day1 = start
#     day2 = end
#     for i in range(delta.days+1):
#         day = startdate + timedelta(days=i) 

def makeNewData():
    xrs = []
    times = []
    flags = []
    data = []
    # length1 = []
    # length2 = []
    print("here")
    for i in range(13,17):
        ds = nc.Dataset(f"./goes{i}onemin.nc") # 4320000 4320060
        data.append(ds)
        print("here2")
        # xrs.append([float(x.data) for x in ds['xrsb_flux']])
        # times.append([float(t.data) for t in ds['time']])
        # flags.append([float(f.data) for f in ds['xrsb_flag']])
        datetime0=cftime.num2pydate(ds.variables["time"][:], ds["time"].units)
        print(datetime0)
        flux = [float(x.data) for x in ds['xrsb_flux']]
        print(len(flux), len(datetime0), flux)
        xrs.append(pd.DataFrame(flux, datetime0))
        print("flux done", xrs)
        times.append(pd.DataFrame([float(t.data) for t in ds['time']], datetime0))
        print("time done")
        flags.append(pd.DataFrame([float(f.data) for f in ds['xrsb_flag']], datetime0))
        print("flags done")

    #do the same for GOES 17
    xrs17 = pd.DataFrame({})
    times17 = pd.DataFrame({})
    flags17 = pd.DataFrame({})
    for j in range(18, 24):
        ds = nc.Dataset(f"sci_xrsf-l2-avg1m_g17_y20{j}_v2-1-0.nc")
        datetime0=cftime.num2pydate(ds.variables["time"][:], ds["time"].units)
        print(datetime0)
        flux = [float(x.data) for x in ds['xrsb_flux']]
        print(len(flux), len(datetime0), flux)
        xrs17.append(pd.DataFrame(flux, datetime0))
        print("flux done", xrs)
        times17.append(pd.DataFrame([float(t.data) for t in ds['time']], datetime0))
        print("time done")
        flags17.append(pd.DataFrame([float(f.data) for f in ds['xrsb_flag']], datetime0))
        print("flags done")
    
    xrs.append(xrs17)
    times.append(times17)
    flags.append(flags17)

    import pickle

    data = {'XRS': xrs, 'TIMES': times, 'FLAGS': flags}

    # Store data (serialize)
    with open('new1mindata.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

makeNewData()

def makeOldData():
    # "https://satdat.ngdc.noaa.gov/sem/goes/data/avg/2019/12/goes15/netcdf/g15_xrs_1m_20191201_20191231.nc"
    # open(f"./20{stri}/g14_xrs_1m_20{stri}{strx}01_20{stri}{strx}{lastday}.nc", "wb").write(r.content)
    xrs = []
    times = []
    flags = []
    for j in range(13,18):
        xrsEx = pd.DataFrame({})
        timesEx = pd.DataFrame({})
        flagsEx = pd.DataFrame({})
        for i in range (10,24):
            for filename in os.listdir(f"20{i}"):
                if(f"g{j}" in filename):
                    ds = nc.Dataset(f"./20{i}/{filename}")
                    datetime0=cftime.num2pydate(ds.variables["time"][:], ds["time"].units)
                    print(datetime0)
                    flux = [float(x.data) for x in ds['xrsb_flux']]
                    print(len(flux), len(datetime0), flux)
                    xrsEx.append(pd.DataFrame(flux, datetime0))
                    print("flux done", xrs)
                    timesEx.append(pd.DataFrame([float(t.data) for t in ds['time']], datetime0))
                    print("time done")
                    flagsEx.append(pd.DataFrame([float(f.data) for f in ds['xrsb_flag']], datetime0))
                    print("flags done")
    xrs.append(xrsEx)
    times.append(timesEx)
    flags.append(flagsEx)
    
    import pickle

    data = {'XRS': xrs, 'TIMES': times, 'FLAGS': flags}

    # Store data (serialize)
    with open('old1mindata.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # go through each year 2010-2023
    # check every file in the folder; loop for i in range (goestypes); if it starts with g{goestype[i]}, 
        # get the datetime0, overall copy-paste the g17 code, save to pickle

# goestype = number, 
def getRawFluxes(goestypes, calibrated, startdate, enddate = dt.datetime.today()):
    # REVISE GOES EVENT LISTS AND MAKE FLARE INDICES
    bestfluxes = []
    besttimes = []
    bestflags = []

    # which data preferred
    route = "new1mindata.pickle" if calibrated else "old1mindata.pickle"
    

    xrs = []
    times = []
    flags = []
    # data = []
    print("here")
    import pickle
    with open(route, 'rb') as handle:
        # {"XRS": [DF of goes13 data with date as index and flux, DF of goes14, ..., DF of GOES17], "TIMES": [...], "FLAGS": [...]}
        data = pickle.load(handle)

        # get the specific goestypes' data in the order specified by the goestype parameter
        for i in range(len(goestypes)): 
            xrs.append(data["XRS"][int(goestypes[i])-13])
            times.append(data["TIMES"][int(goestypes[i])-13])
            flags.append(data["FLAGS"][int(goestypes[i])-13])

    
    

    delta = dt.timedelta(minutes=1)
    date1 = startdate
    # go through each minute in range
    while (date1<=enddate):
        whichgoes = 0

        # Finds the first available good GOES data
        for j in range(len(goestypes)):
            if flags[j].loc[[date1]][0][0] == 16.0: # MAKE SURE THIS IS THE FLAG THROUGHOUT ALL TYPES
                whichgoes = j
                break
        bestfluxes.append(xrs[whichgoes].loc[[date1]][0][0])
        bestflags.append(flags[whichgoes].loc[[date1]][0][0])
        besttimes.append(date1)
        date1 += delta
      
    print("FLUXES:____________________________", bestfluxes)
    print("TIMES:____________________________", bestflags)
    print("FLAGS:____________________________", besttimes)
    return bestfluxes, besttimes, bestflags

# getRawFluxes(["16", "15", "13"], True, dt.datetime(2017,2,18,0,0,0), dt.datetime(2017,2,19,0,0,0))