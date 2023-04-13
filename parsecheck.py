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

def getSatellites(date):
    if(dt.datetime(2010,9,1,0,0,0) <= date and date < dt.datetime(2010,10,28,0,0,0)):
        return ["14", "15"] # not sure about 13
    elif(dt.datetime(2010,10,28,0,0,0) <= date and date < dt.datetime(2011,9,1,0,0,0)):
        return ["15", "14"]
    elif(dt.datetime(2011,9,1,0,0,0) <= date and date < dt.datetime(2012,10,23,16,0,0)):
        return ["14", "15"]
    elif(dt.datetime(2012,10,23,16,0,0) <= date and date < dt.datetime(2012,11,19,16,31,0)):
        return ["15", "14"]
    elif(dt.datetime(2012,11,19,16,31,0) <= date and date < dt.datetime(2015,1,26,16,1,0)):
        return ["15", "13"]
    elif(dt.datetime(2015,1,26,16,1,0) <= date and date < dt.datetime(2015,5,21,18,0,0)):
        return ["14", "13"]
    elif(dt.datetime(2015,5,21,18,0,0) <= date and date < dt.datetime(2015,6,9,16,25,0)):
        return ["15", "13"]
    elif(dt.datetime(2015,6,9,16,25,0) <= date and date < dt.datetime(2016,5,3,13,0,0)):
        return ["13", "14"]
    elif(dt.datetime(2016,5,3,13,0,0) <= date and date < dt.datetime(2016,5,12,17,30,0)):
        return ["14", "13"]
    elif(dt.datetime(2016,5,12,17,30,0) <= date and date < dt.datetime(2016,5,16,17,0,0)):
        return ["14", "15"]
    elif(dt.datetime(2016,5,16,17,0,0) <= date and date < dt.datetime(2016,6,9,17,30,0)):
        return ["15", "13"]
    elif(dt.datetime(2016,6,9,17,30,0) <= date and date < dt.datetime(2017,2,7,0,0,0)):
        return ["16", "15"]
    elif(dt.datetime(2017,2,7,0,0,0) <= date and date < dt.datetime(2017,5,30,20,0,0)):
        return ["16", "15", "13"]
    elif(dt.datetime(2017,5,30,20,0,0) <= date and date < dt.datetime(2017,8,16,19,15,0)):
        return ["16", "13", "14"]
    elif(dt.datetime(2017,8,16,19,15,0) <= date and date < dt.datetime(2017,8,23,21,20,0)):
        return ["16", "15", "13"]
    elif(dt.datetime(2017,8,23,21,20,0) <= date and date < dt.datetime(2017,12,12,16,30,0)):
        return ["16", "15", "14"]
    else:
        return ["17", "16", "15"]
    

    
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



# goestype = number, 
def getRawFluxes(goestypes, calibrated, startdate, enddate = dt.datetime.today()):
    
    fluxes = []
    timess = []
    flagss = []
    # print(startdate )
    # print(sat_life[goestypes][0])
    # print(startdate - sat_life[goestypes][0])
    # length1 = (startdate - sat_life[goestypes][0]).days #int(dateToUnix(startdate) - dateToUnix(sat_life[goestype][0]))
    
    if not calibrated:
        with open(f"./oldg{goestype}_1minxrs.json") as fn:
            f = json.load(fn)
            if enddate == dt.datetime(2000, 1, 1, 0, 0):
                # print(length1)
                # print(len(f))
                # print(f[2])
                # print(f[length1], "hi")
                fluxes.append(f[length1]["flux"])
                times.append(f[length1]["time"])
            else:
                length2 = int(dateToUnix(enddate) - dateToUnix(sat_life[goestype][0]))
                [fluxes.append(f[length1]["flux"]) for i in range(length1, length2)]
                # getFluxGraphs(fluxes, length1, length2, 0, 1/60)

    else:
        xrs = []
        times = []
        flags = []
        data = []
        dates = 0
        # length1 = []
        # length2 = []
        print("here")
        for i in range(len(goestypes)):
            ds = nc.Dataset(f"./goes{goestypes[i]}onemin.nc") # 4320000 4320060
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
            print(xrs)
            times.append(pd.DataFrame([float(t.data) for t in ds['time']], datetime0))
            flags.append(pd.DataFrame([float(f.data) for f in ds['xrsb_flag']], datetime0))
            
            # length1.append(getIndex(datetime0, 0, len(datetime0)-1, startdate))
            # length2.append(getIndex(datetime0, 0, len(datetime0)-1, enddate))
        
        
        # length1 = getIndex(datetime0, 0, len(datetime0)-1, startdate)
        # length2 = getIndex(datetime0, 0, len(datetime0)-1, enddate)#(enddate - sat_life[goestype][0]).days
        print(len(data[2]["xrsb_flag"]))

        # print(length1, length2)
        delta = dt.timedelta(minutes=1)
        
        while (startdate<=enddate):
            whichgoes = 0
            for j in range(len(goestypes)):
                if float(data[j]["xrsb_flag"][i].data) == 16.0:
                    whichgoes = j
                    break
            fluxes.append(xrs[whichgoes].loc[[startdate]][0][0])
            flags.append(flags[whichgoes].loc[[startdate]][0][0])
            times.append(startdate)
            startdate += delta
        
        
        
#         for i in range(length1, length2+1):
#             whichgoes = 0
#             for j in range(len(goestypes)):
#                 if float(data[j]["xrsb_flag"][i].data) == 16.0:
#                     whichgoes = j
#                     break

#             fluxes.append(xrs[whichgoes][i])
#             flagss.append(flags[whichgoes][i])

        # [fluxes.append(float(xrs[i].data)) for i in range(length1, length2+1)] # NEED TO FIND THE UNIX TIME FROM BEFORE AND AFTER AND VERIFY WHAT THOSE TIMES ARE
        # print(goestype)
        # print(unixToDate(float(times[length1].data)/60), "LKDSJLFJSLKDJFLKSDJF:")
        # print(unixToDate(float(times[length2].data)/60), "LKDSJLFJSLKDJFLKSDJF:")

        # [timess.append(datetime0[i]) for i in range(length1, length2)]

        # print(fluxes, len(xrs1))
        # print(timess, len(datetime0))
        # getFluxGraphs(fluxes, length1, length2, 0, 1/60)
        print("-------------------------")
            
#         ds1 = nc.Dataset(f"./goes{goestypes[0]}onemin.nc")
#         datetime0 = cftime.num2pydate(ds1.variables["time"][:], ds1["time"].units)
        
#         xrs1 = ds1['xrsb_flux']
#         times1 = ds1['time']
#         flags1 = [float(flag.data) for flag in ds1['xrsb_flag']]
        
        
        
#         ds2 = nc.Dataset(f"./goes{goestypes[1]}onemin.nc")
        
#         xrs2 = ds2['xrsb_flux']
#         times2 = ds2['time']
#         flags2 = [float(flag.data) for flag in ds2['xrsb_flag']]
        
#         if len(goestypes)==3:
#             ds3 = nc.Dataset(f"./goes{goestypes[2]}onemin.nc")

#             xrs3 = ds3['xrsb_flux']
#             times3 = ds3['time']
#             flags3 = [float(flag.data) for flag in ds3['xrsb_flag']]

#         if enddate == dt.datetime(2000, 1, 1, 0, 0):
#             fluxes.append(float(xrs1[length1].data))
#         else:
#             # print(enddate, dateToUnix(enddate), unixToDate(dateToUnix(enddate)))
#             # print(sat_life[goestype][0], dateToUnix(sat_life[goestype][0]), unixToDate(dateToUnix(enddate)))
#             length1 = getIndex(datetime0, 0, len(datetime0)-1, startdate)
#             length2 = getIndex(datetime0, 0, len(datetime0)-1, enddate)#(enddate - sat_life[goestype][0]).days
            
#             print(length1, length2)
#             for i in range(length1, length2+1):
#                 whichgoes = 0
#                 for j in range(len(goestypes)):
#                     if flags[j][i] == 16.0:
#                         whichgoes = j
#                         break
                
#                 fluxes.append(float(xrs[whichgoes][i].data))
                
#             # [fluxes.append(float(xrs[i].data)) for i in range(length1, length2+1)] # NEED TO FIND THE UNIX TIME FROM BEFORE AND AFTER AND VERIFY WHAT THOSE TIMES ARE
#             print(goestype)
#             # print(unixToDate(float(times[length1].data)/60), "LKDSJLFJSLKDJFLKSDJF:")
#             # print(unixToDate(float(times[length2].data)/60), "LKDSJLFJSLKDJFLKSDJF:")
            
#             [timess.append(datetime0[i]) for i in range(length1, length2)]
            
#             print(fluxes, len(xrs1))
#             print(timess, len(datetime0))
#             # getFluxGraphs(fluxes, length1, length2, 0, 1/60)
#             print("-------------------------")
    
    # datetime1 = cftime.num2pydate(timess.variables["time"][:], ds3["time"].units)
    print("FLUXES:____________________________", fluxes)
    print("TIMES:____________________________", times)
    print("FLAGS:____________________________", flags)
    return fluxes, times, flags

getRawFluxes(["17", "16", "15"], True, dt.datetime(2019, 1, 1, 0, 0), dt.datetime(2019, 1, 1, 1, 0))