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


def getData():
    evData = 0
    newFluxData = 0
    oldFluxData = 0
    
    with open(f'mergedevs.csv') as f:
        evData = pd.read_csv(f)#csv.reader(f)
    
    
    import pickle
    
    route = 'newfluxes3.pkl'
    with open(route, 'rb') as handle:
        # {"XRS": [DF of goes13 data with date as index and flux, DF of goes14, ..., DF of GOES17], "TIMES": [...], "FLAGS": [...]}
        newFluxData = pickle.load(handle)
        # df_new = data[data['DATE'] == dt.datetime(2011,9,6,22,20)]
        # print(df_new)
        # print(data[data.GOES == '13'].shape[0])
        # for i in range(100):
        #     print(data[i])
        
    route = 'oldfluxes.pkl'
    with open(route, 'rb') as handle:
        # {"XRS": [DF of goes13 data with date as index and flux, DF of goes14, ..., DF of GOES17], "TIMES": [...], "FLAGS": [...]}
        oldFluxData = pickle.load(handle)
        # df_new = data[data['DATE'] == dt.datetime(2011,9,6,22,20)]
        # print(df_new)
        # print(data[data.GOES == '13'].shape[0])
        # for i in range(100):
        #     print(data[i])
    return evData, newFluxData, oldFluxData

def appendData():
    evData, newFluxData, oldFluxData = getData()
    oldEventFluxes = []
    newEventFluxes = []
    oldEventClassif = []
    newEventClassif = []
    import math
    
    classes = {1: "X", 2: "X", 3: "X", 4:"X", 5: "M", 6:"C", 7: "B", 8: "A", 9: "A", 10: "A", 11: "A"}
    count = 0
    count2 = 0
    for i in range(len(evData["DATE"])):
        # print(evData["DATE"][i])
        y1 = int(evData["DATE"][i][0:4])
        m1 = int(evData["DATE"][i][5:7])
        d1 = int(evData["DATE"][i][8:])
        h1 = int(evData["PEAK"][i])//100
        mi1 = int(evData["PEAK"][i])%100
        # print(h1, mi1)

        d = dt.datetime(y1, m1, d1, h1, mi1)
        # print( np.isnan(float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"])))# or not np.isnan(float(newFluxData[newFluxData['DATE'] == d]["FLUX"])))
        if d>=dt.datetime(2010, 9, 1, 0, 0):# or not np.isnan(float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"])) or notnp.isnan(float(newFluxData[newFluxData['DATE'] == d]["FLUX"])):
            try:
                # print(d)
                # print(float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"]))
                oldFlux = float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"])
                newFlux = float(newFluxData[newFluxData['DATE'] == d]["FLUX"])
                oldEventClassif.append(f"{classes[(math.log(oldFlux,10)-1)//-1]}{math.floor(f*10**(-(math.floor(math.log(oldFlux,10))))*10)/10}")
                newEventClassif.append(f"{classes[(math.log(newFlux,10)-1)//-1]}{math.floor(f*10**(-(math.floor(math.log(newFlux,10))))*10)/10}")
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
                # FIX THE AND THING 
                
                
                
                
                
                if not np.isnan(float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"])) and not np.isnan(float(newFluxData[newFluxData['DATE'] == d]["FLUX"])):
                     
                    oldFlux = float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"])
                    newFlux = float(newFluxData[newFluxData['DATE'] == d]["FLUX"])
                    print("here2", oldFlux, newFlux)
                    oldEventClassif.append(f"{classes[(math.log(oldFlux,10)-1)//-1]}{math.floor(f*10**(-(math.floor(math.log(oldFlux,10))))*10)/10}")
                    newEventClassif.append(f"{classes[(math.log(newFlux,10)-1)//-1]}{math.floor(f*10**(-(math.floor(math.log(newFlux,10))))*10)/10}")
                    oldEventFluxes.append(float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"]))
                    newEventFluxes.append(float(newFluxData[newFluxData['DATE'] == d]["FLUX"]))
                    
                # print("ERROR:", float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"]), np.isnan(float(oldFluxData[oldFluxData['DATE'] == d]["FLUX"])))
                # print(f"{classes[(math.log(oldFlux,10)-1)//-1]}{str(oldFlux)[0:4]}")
                else:
                    oldEventFluxes.append(np.nan)
                    newEventFluxes.append(np.nan)
                    oldEventClassif.append("")
                    newEventClassif.append("")
        else:
            oldEventFluxes.append(np.nan)
            newEventFluxes.append(np.nan)
            oldEventClassif.append("")
            newEventClassif.append("")
    print(count,count2)
        # float(data[data['DATE'] == dt.datetime(2011,9,8,15,46)]["FLUX"])
#     oldEventFluxes = [float(oldFluxData[oldFluxData['DATE'] == date]["FLUX"]) for date in evData["DATE"]]
#     newEventFluxes = [float(newFluxData[newFluxData['DATE'] == date]["FLUX"]) for date in evData["DATE"]]
    
    evData["OLD_CALIB_FLUX"] = oldEventFluxes
    evData["NEW_CALIB_FLUX"] = newEventFluxes
    evData["OLD_CALIB_MAG"] = oldEventClassif
    evData["NEW_CALIB_MAG"] = newEventClassif
    
    evData.to_csv("newmergedevstest.csv")
        
appendData()