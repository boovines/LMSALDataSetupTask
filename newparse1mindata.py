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

def getData(x):
    if(x==0):
        return dt.datetime(2010,9,1,0,0,0), dt.datetime(2010,10,28,0,0,0), ["14", "15"] # not sure about 13
    elif(x==1):
        return dt.datetime(2010,10,28,0,0,0), dt.datetime(2011,9,1,0,0,0), ["15", "14"]
    elif(x==2):
        return dt.datetime(2011,9,1,0,0,0), dt.datetime(2012,10,23,16,0,0)["14", "15"]
    elif(x==3):
        return dt.datetime(2012,10,23,16,0,0), dt.datetime(2012,11,19,16,31,0)["15", "14"]
    elif(x==4):
        return dt.datetime(2012,11,19,16,31,0), dt.datetime(2015,1,26,16,1,0)["15", "13"]
    elif(x==5):
        return dt.datetime(2015,1,26,16,1,0), dt.datetime(2015,5,21,18,0,0)["14", "13"]
    elif(x==6):
        return dt.datetime(2015,5,21,18,0,0), dt.datetime(2015,6,9,16,25,0)["15", "13"]
    elif(x==7):
        return dt.datetime(2015,6,9,16,25,0), dt.datetime(2016,5,3,13,0,0)["13", "14"]
    elif(x==8):
        return dt.datetime(2016,5,3,13,0,0), dt.datetime(2016,5,12,17,30,0)["14", "13"]
    elif(x==9):
        return dt.datetime(2016,5,12,17,30,0), dt.datetime(2016,5,16,17,0,0), ["14", "15"]
    elif(x==10): 
        return dt.datetime(2016,5,16,17,0,0), dt.datetime(2016,6,9,17,30,0), ["15", "13"]
    elif(x==11):
        return dt.datetime(2016,6,9,17,30,0), dt.datetime(2017,2,7,0,0,0), ["16", "15"]
    elif(x==12):
        return dt.datetime(2017,2,7,0,0,0), dt.datetime(2017,5,30,20,0,0), ["16", "15", "13"]
    elif(x==13):
        return dt.datetime(2017,5,30,20,0,0), dt.datetime(2017,8,16,19,15,0)["16", "13", "14"]
    elif(x==14):
        return dt.datetime(2017,8,16,19,15,0), dt.datetime(2017,8,23,21,20,0), ["16", "15", "13"]
    elif(x==15):
        return dt.datetime(2017,8,23,21,20,0), dt.datetime(2017,12,12,16,30,0), ["16", "15", "14"]
    else:
        return dt.datetime(2017,12,12,16,30,0), dt.datetime.today(), ["17", "16", "15"]
    

    
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
def getRawFluxes(goestypes, calibrated, startdate, enddate = dt.datetime(2000, 1, 1, 0, 0)):
    
    fluxes = []
    timess = []
    flagss = []
    length1 = (startdate - sat_life[goestype][0]).days #int(dateToUnix(startdate) - dateToUnix(sat_life[goestype][0]))
    
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
        datetime0 = 0
        for i in range(len(goestypes)):
            ds = nc.Dataset(f"./goes{goestypes[i]}onemin.nc")
            xrs.append([float(x.data) for x in ds['xrsb_flux']])
            times.append([float(t.data) for t in ds['time']])
            flags.append([float(f.data) for f in ds['xrsb_flag']])
            datetime0 = cftime.num2pydate(ds.variables["time"][:], ds["time"].units)
            
        length1 = getIndex(datetime0, 0, len(datetime0)-1, startdate)
        length2 = getIndex(datetime0, 0, len(datetime0)-1, enddate)#(enddate - sat_life[goestype][0]).days

        print(length1, length2)
        for i in range(length1, length2+1):
            whichgoes = 0
            for j in range(len(goestypes)):
                if flags[j][i] == 16.0:
                    whichgoes = j
                    break

            fluxes.append(xrs[whichgoes][i])
            flagss.append(flags[whichgoes][i])

        # [fluxes.append(float(xrs[i].data)) for i in range(length1, length2+1)] # NEED TO FIND THE UNIX TIME FROM BEFORE AND AFTER AND VERIFY WHAT THOSE TIMES ARE
        print(goestype)
        # print(unixToDate(float(times[length1].data)/60), "LKDSJLFJSLKDJFLKSDJF:")
        # print(unixToDate(float(times[length2].data)/60), "LKDSJLFJSLKDJFLKSDJF:")

        [timess.append(datetime0[i]) for i in range(length1, length2)]

        print(fluxes, len(xrs1))
        print(timess, len(datetime0))
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
    return fluxes, timess, flagss

def getFluxGraphs(fluxes, length1, length2, starthr, scale):
    # Get time values of the signal
    # scale = 1/60
    time   = np.arange(starthr, scale*(length2-length1)+starthr, scale)#, 1);
    # print(fluxes[100])
    # print(time[10])
    signalAmplitude = fluxes

    d = pd.DataFrame(
        dict(x=time,
        y=signalAmplitude)
    )
    print("here")
    sns.scatterplot(data=d, x='x', y='y')
    
# fluxes = getRawFluxes("14", True, dt.datetime(2010, 3, 4, 23, 32), dt.datetime(2010, 3, 5, 23, 32))
# print(fluxes)


    
# print(fluxes_new)

def coverEclipses(fluxes): 
    fluxes_new = []
    
    for i in range(1, len(fluxes[0])):
        diff = fluxes[0][i] - fluxes[0][i-1]
        
        upper = 1#.0000001
        lower = .00000001
        print(len(fluxes[1]))
        if len(fluxes[1]) > 0:
            fluxes_new.append(fluxes[1][i]) if (diff == 0.0 or diff > upper or diff < lower) else fluxes_new.append(fluxes[0][i])
    
    return fluxes_new
 
def stitchTogether(startdate, starttime, enddate, endtime, calibrated=True):
    y1 = startdate.year
    m1 = startdate.month
    d1 = startdate.day
    
    y2 = enddate.year
    m2 = enddate.month
    d2 = enddate.day
    
    start = dt.datetime(y1, m1, d1, int(starttime[0:2]), int(starttime[2:4]))
    end = dt.datetime(y2, m2, d2, int(endtime[0:2]), int(endtime[2:4]))
    
    # satellites = getSatellites(start) # this should return a 2D list: [[start, end, satellite], [start, end, satellite]] 
    
    delta = end-start
    fluxes_new = []
    
    goestypes = getSatellites(start)
    
    day1 = start
    day2 = end
    
    allBestSats = {}
    
    fluxes_total_new = []
    times_total_new = []
    flags_total_new = []
    
    fluxes_total_old = []
    times_total_old = []
    flags_total_old = []

    
    for i in range(17):
        startdate, enddate, goestypes = getData(i)
        fluxes, times, flags = getRawFluxes(goestypes, True, startdate, enddate)
        fluxes_total_new.append(fluxes)
        times_total_new.append(times)
        flags_total_new.append(flags)
        
    for i in range(17):
        startdate, enddate, goestypes = getData(i)
        fluxes, times, flags = getRawFluxes(goestypes, False, startdate, enddate)
        fluxes_total_old.append(fluxes)
        times_total_old.append(times)
        flags_total_old.append(flags)
        
    
    # gets sats for each time range
#     for i in range(delta.days+1):
#         day = startdate + timedelta(days=i)
#         satellites = getSatellites(start)
        
#         if satellites != bestsats: # if best sat switches
#             print(satellites, bestsats)
#             day2 = day
#             rawfluxes = []
#             dates = []
#             for satellite in bestsats:
#                 rawflux, date, flags = getRawFluxes(satellite, calibrated, day1, day2)
#                 rawfluxes.append(rawflux)
#                 dates.append(date)
#             # rawfluxes = [r for raw in rawfluxes for r in raw]
#             patched_fluxes = coverEclipses(rawfluxes)
#             # converted_fluxes = convertFluxes(patched_fluxes)
            
#             fluxes_new.append(patched_fluxes)
#             day1 = day
#             bestsats = satellites
#         elif i == delta.days: # last day condition
#             day2 = end
#             rawfluxes = []
#             dates = []
#             for satellite in bestsats:
#                 rawflux, date = getRawFluxes(satellite, calibrated, day1, day2)
#                 rawfluxes.append(rawflux)
#                 dates.append(date)
#             # rawfluxes = [r for raw in rawfluxes for r in raw]
#             patched_fluxes = coverEclipses(rawfluxes)
#             # converted_fluxes = convertFluxes(patched_fluxes)
            
#             fluxes_new.append(patched_fluxes)
#         else:
#             pass
#     print(len(dates[0]), len(dates[1]), len(fluxes_new[0]))   
#     print(dates, fluxes_new)
    fluxes_total_new = [f for flux in fluxes_total_new for f in flux]
    times_total_new = [f for time in times_total_new for f in time]
    flags_total_new = [f for flag in flags_total_new for f in flag]
    
    fluxes_total_old = [f for flux in fluxes_total_old for f in flux]
    times_total_old = [f for time in times_total_old for f in time]
    flags_total_old = [f for flag in flags_total_old for f in flag]
    
    df1 = pd.DataFrame({'dates': times_total_new,
                       'fluxes': fluxes_total_new, 'flags': flags_total_new})
    df1.to_pickle("newfluxes.pkl")
    
    df2 = pd.DataFrame({'dates': times_total_old,
                       'fluxes': fluxes_total_old, 'flags': flags_total_old})
    df2.to_pickle("oldfluxes.pkl")
    
    
    return fluxes_new, dates
            
# fluxes = stitchTogether(dt.datetime(2021,7,3), "1418", dt.datetime(2021,7,3), "1434")
fluxes = stitchTogether(dt.datetime(2010,3,31), "0000", dt.datetime(2020,3,4), "2359")
# fluxes = stitchTogether(dt.datetime(2010,3,31), "0000", dt.datetime(2010,3,31), "0050")
# fluxes = stitchTogether(dt.datetime(2017,9,10), "1605", dt.datetime(2017,9,10), "1607")
# fluxes = stitchTogether(dt.datetime(2017,9,25), "0757", dt.datetime(2017,9,25), "0808")

print(len(fluxes))

# def convertFluxes(fluxes): # x = s*((detected-bkg)*gain/conversion_factor) # maybe not necessary
#     return True

def getFluxes():
    return True

# basically use the pkl file and replace 0 or close to 0 values
# use sharp data stuff