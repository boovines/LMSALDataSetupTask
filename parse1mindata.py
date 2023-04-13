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

def dateToUnix(time): 
    start = dt.datetime(2000, 1, 1, 12, 0)
    delta = time-start
    minutes = (delta.total_seconds()/60)
    return minutes

def unixToDate(time):
    return dt.datetime.fromtimestamp(time*60 + 946753200)#946756800)

def getSatellites(date):
    if(dt.datetime(2010,10,28,0,0,0) > date):
        return ["14", "15"]
    elif(dt.datetime(2010,10,28,0,0,0) <= date and date < dt.datetime(2011,9,1,0,0,0)):
        return ["15", "13"] # not sure about 13
    elif(dt.datetime(2011,9,1,0,0,0) <= date and date < dt.datetime(2012,10,23,16,0,0)):
        return ["15", "14"]
    elif(dt.datetime(2012,10,23,16,0,0) <= date and date < dt.datetime(2012,11,19,16,31,0)):
        return ["14", "15"]
    elif(dt.datetime(2012,11,19,16,31,0) <= date and date < dt.datetime(2015,1,26,16,1,0)):
        return ["15", ""]
    elif(dt.datetime(2015,1,26,16,1,0) <= date and date < dt.datetime(2015,5,21,18,0,0)):
        return ["15", "13"]
    elif(dt.datetime(2015,5,21,18,0,0) <= date and date < dt.datetime(2015,6,9,16,25,0)):
        return ["14", "13"]
    elif(dt.datetime(2015,6,9,16,25,0) <= date and date < dt.datetime(2016,5,3,13,0,0)):
        return ["15", "13"]
    elif(dt.datetime(2016,5,3,13,0,0) <= date and date < dt.datetime(2016,5,12,17,30,0)):
        return ["13", "14"]
    elif(dt.datetime(2016,5,12,17,30,0) <= date and date < dt.datetime(2016,5,16,17,0,0)):
        return ["14", "13"]
    elif(dt.datetime(2016,5,16,17,0,0) <= date and date < dt.datetime(2016,6,9,0,0,0)):
        return ["14", "15"]
    elif(dt.datetime(2016,6,9,0,0,0) <= date and date < dt.datetime(2017,12,15,0,0,0)):
        return ["15", "13"]
    elif(dt.datetime(2017,12,15,0,0,0) <= date and date < dt.datetime(2019,11,31,0,0,0)):
        return ["15", "14", "16"]
    elif(dt.datetime(2019,11,31,0,0,0) <= date and date < dt.datetime(2020,3,15,0,0,0)):
        return ["16", "15", "17"]
    else:
        return ["16", "17"]



# goestype = number, 
def getRawFluxes(goestype, calibrated, startdate, enddate = dt.datetime(2000, 1, 1, 0, 0)):
    
    fluxes = []
    timess = []
    length1 = int(dateToUnix(startdate) - dateToUnix(sat_life[goestype][0]))
    
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
        ds3 = nc.Dataset(f"./goes{goestype}onemin.nc")
        xrs = ds3['xrsb_flux']
        times = ds3['time']
        

        if enddate == dt.datetime(2000, 1, 1, 0, 0):
            fluxes.append(float(xrs[length1].data))
        else:
            print(enddate, dateToUnix(enddate), unixToDate(dateToUnix(enddate)))
            print(sat_life[goestype][0], dateToUnix(sat_life[goestype][0]), unixToDate(dateToUnix(enddate)))

            length2 = int(dateToUnix(enddate) - dateToUnix(sat_life[goestype][0]))
            
            print(length1, length2)
            [fluxes.append(float(xrs[i].data)) for i in range(length1, length2)] # NEED TO FIND THE UNIX TIME FROM BEFORE AND AFTER AND VERIFY WHAT THOSE TIMES ARE
            print(goestype)
            print(unixToDate(float(times[length1].data)/60), "LKDSJLFJSLKDJFLKSDJF:")
            print(unixToDate(float(times[length2].data)/60), "LKDSJLFJSLKDJFLKSDJF:")
            
            [timess.append(float(times[i].data)) for i in range(length1, length2)]
            
            print(fluxes)
            # getFluxGraphs(fluxes, length1, length2, 0, 1/60)
            print("-------------------------")
    
    
    return fluxes

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

def coverEclipses(fluxes): # THIS IS OLD.        USE FLAGS INSTEAD AND REVISE THE LIST
    
#     fluxes_new = []
    
#     for i in range(1, len(fluxes[0])):
#         diff = fluxes[0][i] - fluxes[0][i-1]
        
#         upper = 1#.0000001
#         lower = .00000001
        
#         fluxes_new.append(fluxes[1][i]) if (diff == 0.0 or diff > upper or diff < lower) else fluxes_new.append(fluxes[0][i])
    
#     return fluxes_new

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
    
    bestsats = getSatellites(start)
    
    day1 = start
    day2 = end
    
    allBestSats = {}
    # gets sats for each time range
    for i in range(delta.days+1):
        day = startdate + timedelta(days=i)
        satellites = getSatellites(start)
        
        if satellites != bestsats: # if best sat switches
            print(satellites, bestsats)
            day2 = day
            rawfluxes = []
            for satellite in bestsats:
                rawflux = getRawFluxes(satellite, calibrated, day1, day2)
                rawfluxes.append(rawflux)
            # rawfluxes = [r for raw in rawfluxes for r in raw]
            patched_fluxes = coverEclipses(rawfluxes)
            # converted_fluxes = convertFluxes(patched_fluxes)
            
            fluxes_new.append(patched_fluxes)
            day1 = day
            bestsats = satellites
        elif i == delta.days: # last day condition
            day2 = end
            rawfluxes = []
            for satellite in bestsats:
                rawflux = getRawFluxes(satellite, calibrated, day1, day2)
                rawfluxes.append(rawflux)
            # rawfluxes = [r for raw in rawfluxes for r in raw]
            patched_fluxes = coverEclipses(rawfluxes)
            # converted_fluxes = convertFluxes(patched_fluxes)
            
            fluxes_new.append(patched_fluxes)
        else:
            pass
        
    fluxes_new = [f for flux in fluxes_new for f in flux]
    
    return fluxes_new
            
fluxes = stitchTogether(dt.datetime(2021,7,3), "1418", dt.datetime(2021,7,3), "1434")
# fluxes = stitchTogether(dt.datetime(2011,8,9), "0748", dt.datetime(2011,8,9), "0808")
# fluxes = stitchTogether(dt.datetime(2017,9,10), "1605", dt.datetime(2017,9,10), "1607")
# fluxes = stitchTogether(dt.datetime(2017,9,25), "0757", dt.datetime(2017,9,25), "0808")

print(len(fluxes))

# def convertFluxes(fluxes): # x = s*((detected-bkg)*gain/conversion_factor) # maybe not necessary
#     return True

def getFluxes():
    return True
