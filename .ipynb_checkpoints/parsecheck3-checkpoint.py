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

from ncflag import FlagWrap


num_vars = 2
make_plot = 1
# ds = nc.Dataset("./2010/g14_xrs_1m_20100101_20100131.nc")
# ds2 = nc.Dataset("./goes14onemin.nc")

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
def fillGap1(p, xrs, isNew):
    # fill in 2010s
    with nc.Dataset(f"{p}/goes14onemin.nc") as nc_in: #"sci_xrsf-l2-avg1m_g14_s20090901_e20200304_v1-0-0.nc") as nc_in:
        times = cftime.num2pydate(nc_in.variables["time"][:], nc_in.variables["time"].units)
        xrsb_flux = np.ma.filled(nc_in.variables["xrsb_flux"][:], fill_value=np.nan)
    if isNew:
        a = pd.DataFrame(xrsb_flux, times)
        new = a.loc[:dt.datetime(2010,8,31,23,59)]
        print(new)
        df = pd.DataFrame(new,times )
    else:
        a = pd.DataFrame(xrsb_flux, times)
        old = a.loc[:dt.datetime(2010,8,31,23,59)]*.7
        df = pd.DataFrame(old, times)
    print(xrs[1])
    xrs[1] = pd.concat([df, xrs[1]])
    return xrs
    # df.loc[[dt.datetime(2010,1,1,12,9)]][0][0]*.7
    #fill in 2011-3-1 ---- 2011-3-31
    
    
def makeNewData(p):
    xrs = []
    times = []
    flags = []
    data = []
    # length1 = []
    # length2 = []
    print("here")
    
    # filenames = ["sci_xrsf-l2-avg1m_g13_s20130601_e20171214_v1-0-0.nc", "sci_xrsf-l2-avg1m_g14_s20090901_e20200304_v1-0-0.nc", "sci_xrsf-l2-avg1m_g15_s20100331_e20200304_v1-0-0.nc"]
    
    for i in range(13,18):
        fn = f"{p}/goes{i}onemin.nc"#filenames[i-13]
#         if not os.path.exists(fn):
#             with open(fn, "wb") as f:
#                 url_path = f"https://www.ncei.noaa.gov/data/goes-space-environment-monitor/access/science/xrs/goes{i}/xrsf-l2-avg1m_science/"
                
#                 r = requests.get(url_path + fn)
#                 f.write(r.content)
        ds = nc.Dataset(fn) # 4320000 4320060
        data.append(ds)
        
        with nc.Dataset(fn) as nc_in:
            times = cftime.num2pydate(nc_in.variables["time"][:], nc_in.variables["time"].units)
            # print(nc_in.variables)
            xrsb_flags = FlagWrap.init_from_netcdf(nc_in.variables["xrsb_flag"])
            print(nc_in.variables["xrsb_flag"])
            xrsb_flux = np.ma.filled(nc_in.variables["xrsb_flux"][:], fill_value=np.nan)
            print(xrsb_flags)
        good_data = xrsb_flags.get_flag("good_data")
        xrsb_flux[~good_data] = np.nan
        
        xrs.append(pd.DataFrame(xrsb_flux, times))
        print(xrsb_flux)
        
    
#     #g16
#     d = dt.datetime.today()
#     day = str(d.day-3).zfill(2) if d.weekday()==0 else str(d.day-1).zfill(2)
#     month = str(d.month).zfill(2)
#     filename = f"sci_xrsf-l2-avg1m_g16_s20170207_e20230204_v2-1-0.nc"#{month}{day}_v2-1-0.nc"
#     if not os.path.exists(filename):
#         with open(filename, "wb") as f:
#             url_path = f"https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/goes16/l2/data/xrsf-l2-avg1m_science/"
#             r = requests.get(url_path + filename)
#             f.write(r.content)
    
#     with nc.Dataset(filename) as nc_in:
#         times = cftime.num2pydate(nc_in.variables["time"][:], nc_in.variables["time"].units)
#         # print(nc_in.variables)
#         xrsb_flags = FlagWrap.init_from_netcdf(nc_in.variables["xrsb_flag"])
#         print(nc_in.variables["xrsb_flag"])
#         xrsb_flux = np.ma.filled(nc_in.variables["xrsb_flux"][:], fill_value=np.nan)
#         print(xrsb_flags)
#     good_data = xrsb_flags.get_flag("good_data")
#     xrsb_flux[~good_data] = np.nan 
#     print(xrsb_flux)
    
#     xrs.append(pd.DataFrame(xrsb_flux, times))
    

#     #do the same for GOES 17
#     xrs17 = pd.DataFrame({})
#     times17 = pd.DataFrame({})
#     flags17 = pd.DataFrame({})
#     for j in range(18, 24):
#         filename = f"sci_xrsf-l2-avg1m_g17_y20{j}_v2-1-0.nc"
#         if not os.path.exists(filename):
#             with open(filename, "wb") as f:
#                 url_path = f"https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/goes17/l2/data/xrsf-l2-avg1m_science/"
#                 r = requests.get(url_path + filename)
#                 f.write(r.content)

#         with nc.Dataset(filename) as nc_in:
#             times = cftime.num2pydate(nc_in.variables["time"][:], nc_in.variables["time"].units)
#             # print(nc_in.variables)
#             xrsb_flags = FlagWrap.init_from_netcdf(nc_in.variables["xrsb_flag"])
#             print(nc_in.variables["xrsb_flag"])
#             xrsb_flux = np.ma.filled(nc_in.variables["xrsb_flux"][:], fill_value=np.nan)
#             print(xrsb_flags)
#         good_data = xrsb_flags.get_flag("good_data")
#         xrsb_flux[~good_data] = np.nan
#         print(xrsb_flux)
#         print("EJLKRJLKJSDLKFJLKSDJFLKSDJFKLJSDLKFJSLDKFJLKSDJFLDKSJFLKDSJFLSDJFLSDJFL", xrs17)
#         xrs17 = pd.concat([xrs17, pd.DataFrame(xrsb_flux, times)])
#         # xrs17.append(pd.DataFrame(xrsb_flux, times))
    
#     xrs.append(xrs17)
    # times.append(times17)
    # flags.append(flags17)
    
    finalxrs = fillGap1(p, xrs, True)

    import pickle

    data = {'XRS': finalxrs}#, 'TIMES': times, 'FLAGS': flags}

    # Store data (serialize)
    with open(f'{p}/new1mindata.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

# makeNewData("/Users/jhou/LMSALDataSetupTaskOriginal/newfoldertest")




def makeOldData(p):
    # "https://satdat.ngdc.noaa.gov/sem/goes/data/avg/2019/12/goes15/netcdf/g15_xrs_1m_20191201_20191231.nc"
    # open(f"./20{stri}/g14_xrs_1m_20{stri}{strx}01_20{stri}{strx}{lastday}.nc", "wb").write(r.content)
    goespaths = [] #[[]]
    xrs = []
    for j in range(13,16):
        gpaths = []
        for i in range(10,21): # SWITCH BACK EV
            path = f"{p}/20{i}/"
            direc = os.listdir(path)
            # with open(path):
            for file in direc:
                if f"g{j}" in file:
                    gpaths.append(f'{path}{file}')
        goespaths.append(gpaths)
    goespaths = [sorted(goespaths[0]), sorted(goespaths[1]), sorted(goespaths[2])]

    
    for x in range(len(goespaths)):
        xrsinstance = pd.DataFrame({})
        for goespath in goespaths[x]:
            try:
                with nc.Dataset(goespath) as nc_in:
                    times = cftime.num2pydate(nc_in.variables["time_tag"][:], nc_in.variables["time_tag"].units)
                    # print(nc_in.variables)

                    xrsb_flux = np.ma.filled(nc_in.variables["B_AVG"][:], fill_value=np.nan)



                    xrsb_flags = np.ma.filled(nc_in.variables["B_QUAL_FLAG"][:], fill_value=np.nan)

                    xrsb_numpts = np.ma.filled(nc_in.variables["B_NUM_PTS"][:], fill_value=np.nan)
                    # print(nc_in.variables["xrsb_flag"])
                xrsmonth = []
                timesmonth = []

                print(times, xrsb_flux)
                for c in range(len(xrsb_flux)):
                    if xrsb_flags[c] == 0 and xrsb_numpts[c] >= 29:
                        xrsmonth.append(xrsb_flux[c])
                        # print("SLDKFJLSDJFLKSDJFLKJSDKLFLSDJFLKJSDLKFJSDLJFLDSJF", xrsmonth)
                        timesmonth.append(times[c])
                    else:
                        xrsmonth.append(np.nan)
                        timesmonth.append(times[c])
                print(pd.DataFrame(xrsmonth, timesmonth))
                # good_data = xrsb_flags.get_flag("good_data")
                # xrsb_flux[~good_data] = np.nan
                xrsinstance = pd.concat([xrsinstance, pd.DataFrame(xrsmonth, timesmonth)])
            except:
                pass
        
        print(xrsinstance)
        xrs.append(xrsinstance)
    
    # print(xrs)
    import pickle
    finalxrs = fillGap1(p, xrs, False)
    data = {'XRS': finalxrs}#, 'TIMES': times, 'FLAGS': flags}

    # Store data (serialize)
    with open(f'{p}/old1mindata.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

# makeOldData("/Users/jhou/LMSALDataSetupTaskOriginal/testdata")
    #     xrs.append(pd.DataFrame(xrsb_flux, times))
# ff = nc.Dataset(dir0 + file0)
# from ncflag import FlagWrap

# nc_in = nc.Dataset("./2015/g13_xrs_1m_20150101_20150131.nc")
# # nc_in.variables["B_AVG"][:]
# # datetime0 = cftime.num2pydate(nc_in.variables["time_tag"][:], nc_in["time_tag"].units)
# # xrsb_flux = np.ma.filled(nc_in.variables["B_AVG"][:], fill_value=np.nan)

# # print(len([float(item.data) for item in nc_in.variables["B_QUAL_FLAG"]]))
# # xrsb_flags = FlagWrap.init_from_netcdf(nc_in.variables["B_QUAL_FLAG"])#xrsb_flag

# # # print("Filename:  ", file0)
# # # print("start time in file [{}]: {}".format(ff["time_tag"].units, ff.variables["time_tag"][0]))
# # # print("start and end times:", datetime0[0], datetime0[-1])
    
    
    
#     xrs = []
#     times = []
#     flags = []
#     for j in range(13,18):
#         xrsEx = pd.DataFrame({})
#         timesEx = pd.DataFrame({})
#         flagsEx = pd.DataFrame({})
#         for i in range (10,24):
#             for filename in os.listdir(f"20{i}"):
#                 if(f"g{j}" in filename):
#                     ds = nc.Dataset(f"./20{i}/{filename}")
#                     datetime0=cftime.num2pydate(ds.variables["time"][:], ds["time"].units)
#                     print(datetime0)
#                     flux = [float(x.data) for x in ds['xrsb_flux']]
#                     print(len(flux), len(datetime0), flux)
#                     xrsEx.append(pd.DataFrame(flux, datetime0))
#                     print("flux done", xrs)
#                     timesEx.append(pd.DataFrame([float(t.data) for t in ds['time']], datetime0))
#                     print("time done")
#                     flagsEx.append(pd.DataFrame([float(f.data) for f in ds['xrsb_flag']], datetime0))
#                     print("flags done")
#     xrs.append(xrsEx)
#     times.append(timesEx)
#     flags.append(flagsEx)
    
#     import pickle

#     data = {'XRS': xrs}#, 'TIMES': times, 'FLAGS': flags}

#     # Store data (serialize)
#     with open('old1mindata.pickle', 'wb') as handle:
#         pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
#     # go through each year 2010-2023
#     # check every file in the folder; loop for i in range (goestypes); if it starts with g{goestype[i]}, 
#         # get the datetime0, overall copy-paste the g17 code, save to pickle
        
        
        
# def makeOldData():
#     # "https://satdat.ngdc.noaa.gov/sem/goes/data/avg/2019/12/goes15/netcdf/g15_xrs_1m_20191201_20191231.nc"
#     # open(f"./20{stri}/g14_xrs_1m_20{stri}{strx}01_20{stri}{strx}{lastday}.nc", "wb").write(r.content)
#     xrs = []
#     times = []
#     flags = []
#     for j in range(13,18):
#         xrsEx = pd.DataFrame({})
#         timesEx = pd.DataFrame({})
#         flagsEx = pd.DataFrame({})
#         for i in range (10,24):
#             for filename in os.listdir(f"20{i}"):
#                 if(f"g{j}" in filename):
#                     ds = nc.Dataset(f"./20{i}/{filename}")
#                     datetime0=cftime.num2pydate(ds.variables["time"][:], ds["time"].units)
#                     print(datetime0)
#                     flux = [float(x.data) for x in ds['xrsb_flux']]
#                     print(len(flux), len(datetime0), flux)
#                     xrsEx.append(pd.DataFrame(flux, datetime0))
#                     print("flux done", xrs)
#                     timesEx.append(pd.DataFrame([float(t.data) for t in ds['time']], datetime0))
#                     print("time done")
#                     flagsEx.append(pd.DataFrame([float(f.data) for f in ds['xrsb_flag']], datetime0))
#                     print("flags done")
#     xrs.append(xrsEx)
#     times.append(timesEx)
#     flags.append(flagsEx)
    
#     import pickle

#     data = {'XRS': xrs}#, 'TIMES': times, 'FLAGS': flags}

#     # Store data (serialize)
#     with open('old1mindata.pickle', 'wb') as handle:
#         pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
#     # go through each year 2010-2023
#     # check every file in the folder; loop for i in range (goestypes); if it starts with g{goestype[i]}, 
#         # get the datetime0, overall copy-paste the g17 code, save to pickle

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
            # times.append(data["TIMES"][int(goestypes[i])-13])
            # flags.append(data["FLAGS"][int(goestypes[i])-13])

    
    

    delta = dt.timedelta(minutes=1)
    date1 = startdate
    # go through each minute in range
    while (date1<=enddate):
        whichgoes = 0

        # Finds the first available good GOES data
        for j in range(len(goestypes)):
            if not np.isnan(xrs[j].loc[[date1]][0][0]): # MAKE SURE THIS IS THE FLAG THROUGHOUT ALL TYPES
                whichgoes = j
                break
        bestfluxes.append(xrs[whichgoes].loc[[date1]][0][0])

        date1 += delta
      
    print("FLUXES:____________________________", bestfluxes)
    return bestfluxes#, besttimes, bestflags

# getRawFluxes(["16", "15", "13"], True, dt.datetime(2017,2,7,0,0,0), dt.datetime(2017,5,30,20,0,0))