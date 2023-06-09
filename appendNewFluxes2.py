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



def getData(p):
    lmsal = True
    evData = 0
    newFluxData = 0
    oldFluxData = 0
    
    # direc = "/Users/jhou/LMSALDataSetupTaskOriginal/testdata/" if lmsal else "Users/justinhou/Documents/data/"
    with open(f'{p}/mergedevs.csv') as f:
        evData = pd.read_csv(f)#csv.reader(f)
    
    
    import pickle
    
    route = f'{p}/newfluxes.pkl'
    with open(route, 'rb') as handle:
        # {"XRS": [DF of goes13 data with date as index and flux, DF of goes14, ..., DF of GOES17], "TIMES": [...], "FLAGS": [...]}
        newFluxData = pickle.load(handle)
        # df_new = data[data['DATE'] == dt.datetime(2011,9,6,22,20)]
        # print(df_new)
        # print(data[data.GOES == '13'].shape[0])
        # for i in range(100):
        #     print(data[i])
        
    route = f'{p}/oldfluxes.pkl'
    with open(route, 'rb') as handle:
        # {"XRS": [DF of goes13 data with date as index and flux, DF of goes14, ..., DF of GOES17], "TIMES": [...], "FLAGS": [...]}
        oldFluxData = pickle.load(handle)
        # df_new = data[data['DATE'] == dt.datetime(2011,9,6,22,20)]
        # print(df_new)
        # print(data[data.GOES == '13'].shape[0])
        # for i in range(100):
        #     print(data[i])
    return evData, newFluxData, oldFluxData

def changeDates(evData, i):
    y1 = int(evData["DATE"][i][0:4])
    m1 = int(evData["DATE"][i][5:7])
    d1 = int(evData["DATE"][i][8:])
    
    h1 = int(evData["START"][i])//100
    mi1 = int(evData["START"][i])%100
    
    h2 = int(evData["PEAK"][i])//100
    mi2 = int(evData["PEAK"][i])%100
    
    h3 = int(evData["END"][i])//100
    mi3 = int(evData["END"][i])%100
    
    return dt.datetime(y1, m1, d1, h1, mi1), dt.datetime(y1, m1, d1, h2, mi2), dt.datetime(y1, m1, d1, h3, mi3)

def getMatchingFluxes(evData, newFluxData, oldFluxData):
    oldEventFluxes = []
    newEventFluxes = []
    count = 0
    count2 = 0
    for i in range(len(evData["DATE"])):
        # print(evData["DATE"][i])
        # y1 = int(evData["DATE"][i][0:4])
        # m1 = int(evData["DATE"][i][5:7])
        # d1 = int(evData["DATE"][i][8:])
        # h1 = int(evData["PEAK"][i])//100
        # mi1 = int(evData["PEAK"][i])%100
        # print(h1, mi1)

        # start, d, peak = changeDates(evData, i)# dt.datetime(y1, m1, d1, h1, mi1)
        print(evData)
        # print(evData["PEAK"][28225])
        start = evData["START"][evData.index[i]]
        peak = evData["PEAK"][evData.index[i]]
        end = evData["END"][evData.index[i]]


        # evData["START"][i] = start
        # evData["PEAK"][i] = d
        # evData["END"][i] = peak

        print(peak)
        d = dt.datetime.strptime(peak, "%Y-%m-%d %H:%M:%S")
        # print( np.isnan(float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"])))# or not np.isnan(float(newFluxData[newFluxData['DATE'] == d]["FLUX"])))
        if d>=dt.datetime(2010, 1, 1, 0, 0):# or not np.isnan(float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"])) or notnp.isnan(float(newFluxData[newFluxData['DATE'] == d]["FLUX"])):
            # print("hih")
            if d<=dt.datetime(2020, 3, 6, 0, 0) and d>=dt.datetime(2010, 9, 1, 0, 0):
                try:
                    # print(d)
                    # print(float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"]))
                    oldFlux = float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"])
                    newFlux = float(newFluxData[newFluxData['DATE'] == d]["FLUX"])
                    oldEventFluxes.append(oldFlux)
                    newEventFluxes.append(newFlux)
                    # try:

                    # except:
                    #     # print("error occurred")
                    #     count+=1
                    #     oldEventClassif.append("")
                    #     newEventClassif.append("")

                except:
                    count2+=1


                    oldEventFluxes.append(np.nan)
                    newEventFluxes.append(np.nan)
            else:
                # try:
                print("here", d, newFluxData[newFluxData['DATE'] == d]["FLUX"])
                try:
                    newFlux = float(newFluxData[newFluxData['DATE'] == d]["FLUX"])
                except:
                    newFlux = np.nan
                oldEventFluxes.append(np.nan)
                newEventFluxes.append(newFlux)
                    # try:

                    # except:
                    #     # print("error occurred")
                    #     count+=1
                    #     oldEventClassif.append("")
                    #     newEventClassif.append("")

#                     except:
#                         count2+=1


#                         oldEventFluxes.append(np.nan) 
#                         newEventFluxes.append(np.nan)

        else:
            oldEventFluxes.append(np.nan)
            newEventFluxes.append(np.nan)
    # print(count)#,count2)
    return oldEventFluxes, newEventFluxes

def appendData(p):
    lmsal = False
    # direc = direc = "/Users/jhou/Documents/data/" if lmsal else "Users/justinhou/Documents/data/"
    evData, newFluxData, oldFluxData = getData(p)
    oldEventFluxes = []
    newEventFluxes = []
    
    import math
    # print(evData["DATE"][-1])
    classes = {1: "X", 2: "X", 3: "X", 4:"X", 5: "M", 6:"C", 7: "B", 8: "A", 9: "A", 10: "A", 11: "A"}
    
    if not os.path.exists(f"{p}/newmergedevs.csv"):
        print(evData.iloc[(len(evData["DATE"])-1000):])
        # test = evData.iloc[:(len(evData["DATE"])-1000)]
        oldEventFluxes, newEventFluxes = getMatchingFluxes(evData, newFluxData, oldFluxData)
    else:
        
        
        # date = dt.datetime.now()
        mergedevDate = dt.datetime.fromtimestamp(os.path.getmtime(f"{p}/mergedevs.csv"))
        fluxDate = dt.datetime.fromtimestamp(os.path.getmtime(f"{p}/newfluxes.pkl"))
        delta = dt.timedelta(days=3)
        priorDate = mergedevDate - delta if mergedevDate<fluxDate else fluxDate - delta
        today = dt.datetime.now()

        endEvData = evData.loc[evData["PEAK"].between(str(priorDate),str(today))]
        print(endEvData)
        
         # = newEvData.iloc[len(newEventFluxes):]
        if not endEvData.empty:
            oldEventFluxes, newEventFluxes = getMatchingFluxes(endEvData, newFluxData, oldFluxData)
            # for index, ev in endEvData.iterrows():
            #     endEvData[]
        else:
            print("Nothing to Update")
            return "Nothing to Update"
        
        # float(data[data['DATE'] == dt.datetime(2011,9,8,15,46)]["FLUX"])
#     oldEventFluxes = [float(oldFluxData[oldFluxData['DATE'] == date]["FLUX"]) for date in evData["DATE"]]
#     newEventFluxes = [float(newFluxData[newFluxData['DATE'] == date]["FLUX"]) for date in evData["DATE"]]
    oldEventClassif = []
    newEventClassif = []
    herecount = 0
    for i in range(len(oldEventFluxes)):
        # try:
        # print(np.nan, np.isnan(oldEventFluxes[i]))
        if not np.isnan(oldEventFluxes[i]) and not np.isnan(newEventFluxes[i]):
            
            # print(oldEventFluxes[i])
            # print(f"{classes[(math.log(oldEventFluxes[i],10)-1)//-1]}{str(oldEventFluxes[i])[0:4]}")
            # f"{classes[(math.log(f,10)-1)//-1]}{round(f*10**(-(math.floor(math.log(f,10)))), 1)}"
            # f"{classes[(math.log(newEventFluxes[i],10)-1)//-1]}{math.floor(newEventFluxes[i]*10**(-(math.floor(math.log(newEventFluxes[i],10))))*10)/10}"
            oldEventClassif.append(f"{classes[(math.log(oldEventFluxes[i],10)-1)//-1]}{round(oldEventFluxes[i]*10**(-(math.floor(math.log(oldEventFluxes[i],10)))), 1)}")
            newEventClassif.append(f"{classes[(math.log(newEventFluxes[i],10)-1)//-1]}{round(newEventFluxes[i]*10**(-(math.floor(math.log(newEventFluxes[i],10)))), 1)}")
            
        elif np.isnan(oldEventFluxes[i]) and not np.isnan(newEventFluxes[i]):
            oldEventClassif.append(np.nan)
            # print(newEventFluxes*10**(-(math.floor(math.log(newEventFluxes,10)))))
            newEventClassif.append(f"{classes[(math.log(newEventFluxes[i],10)-1)//-1]}{round(newEventFluxes[i]*10**(-(math.floor(math.log(newEventFluxes[i],10)))), 1)}")
            # newEventClassif.append(f"{classes[(math.log(newEventFluxes[i],10)-1)//-1]}{str(newEventFluxes[i])[0:4]}")
            
        elif not np.isnan(oldEventFluxes[i]) and np.isnan(newEventFluxes[i]):
            # oldEventClassif.append(f"{classes[(math.log(oldEventFluxes[i],10)-1)//-1]}{str(oldEventFluxes[i])[0:4]}")
            oldEventClassif.append(f"{classes[(math.log(oldEventFluxes[i],10)-1)//-1]}{round(oldEventFluxes[i]*10**(-(math.floor(math.log(oldEventFluxes[i],10)))), 1)}")
            newEventClassif.append(np.nan)
        else:
            oldEventClassif.append(np.nan)
            newEventClassif.append(np.nan)
        
        
        # oldEventClassif.append(f"{classes[(math.log(oldEventFluxes[i],10)-1)//-1]}{str(oldEventFluxes[i])[0:4]}") if np.isnan(oldEventFluxes[i]) else oldEventClassif.append(np.nan)
        # newEventClassif.append(f"{classes[(math.log(newEventFluxes[i],10)-1)//-1]}{str(newEventFluxes[i])[0:4]}") if np.isnan(newEventFluxes[i]) else newEventClassif.append(np.nan)
        # except:
        #     herecount+=1
        #     print("here")
        #     oldEventClassif.append(np.nan)
        #     newEventClassif.append(np.nan)
    # print(herecount)
    
    if not os.path.exists(f"{p}/newmergedevs.csv"): 
        evData["OLD_CALIB_FLUX"] = oldEventFluxes
        evData["NEW_CALIB_FLUX"] = newEventFluxes
        evData["OLD_CALIB_MAG"] = oldEventClassif
        evData["NEW_CALIB_MAG"] = newEventClassif
        print(evData[:3])
        evData.to_csv(f"{p}/newmergedevs.csv")
    else:
        endEvData["OLD_CALIB_FLUX"] = oldEventFluxes
        endEvData["NEW_CALIB_FLUX"] = newEventFluxes
        endEvData["OLD_CALIB_MAG"] = oldEventClassif
        endEvData["NEW_CALIB_MAG"] = newEventClassif
        
        with open(f'{p}/newmergedevs.csv') as f:
            evData2 = pd.read_csv(f)#csv.reader(f)
            # print(endEvData["PEAK"][0], "HDSJFHDLSF")
            fixedEvData2 = evData2.loc[evData["PEAK"].between(str(dt.datetime(2010,1,1,12,2)),str(endEvData["PEAK"][endEvData.index[0]]))]
            # oldEventFluxes = evData["OLD_CALIB_FLUX"]
            # newEventFluxes = evData["NEW_CALIB_FLUX"]
            # peakDates = evData["PEAK"]
            
        fixedEvData2.append(endEvData, ignore_index = True)
        print(fixedEvData2[:3])
        fixedEvData2.to_csv(f"{p}/newmergedevs.csv")
    
    
        
# appendData("/Users/jhou/LMSALDataSetupTaskOriginal/testdata623")