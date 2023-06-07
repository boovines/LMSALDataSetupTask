import os

import numpy as np
import pandas as pd

import astropy
import astropy.units as u
from astropy.coordinates import SkyCoord
# from sunpy.data.sample import AIA_193_IMAGE, HMI_LOS_IMAGE

import astropy.time
from astropy.visualization import ImageNormalize, SqrtStretch

import matplotlib.pyplot as plt


import sunpy.map
from sunpy.net import Fido
from sunpy.net import attrs as a
import matplotlib.pyplot as plt

import sunpy.coordinates
import sunpy.data.sample
from sunpy.io.special import srs

import datetime as dt
from datetime import datetime
import json
import csv

import requests
import netCDF4 as nc # https://towardsdatascience.com/read-netcdf-data-with-python-901f7ff61648

import calendar

months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

def getLatest(path, version): # check if already saved latest. else, get latest from https server
    # if(not latest):
    date = datetime.now()
    y = date.strftime("%y")
    m = date.strftime("%m")
    if not os.path.exists(f'{path}/goes13onemin.nc'):
        url13 = f"https://www.ncei.noaa.gov/data/goes-space-environment-monitor/access/science/xrs/goes13/xrsf-l2-avg1m_science/sci_xrsf-l2-avg1m_g13_s20130601_e20171214_v1-0-0.nc" 
        r = requests.get(url13, allow_redirects = True)
        open(f'{path}/goes13onemin.nc', "wb").write(r.content)
        
    if not os.path.exists(f'{path}/goes14onemin.nc'):
        url14 = f"https://www.ncei.noaa.gov/data/goes-space-environment-monitor/access/science/xrs/goes14/xrsf-l2-avg1m_science/sci_xrsf-l2-avg1m_g14_s20090901_e20200304_v1-0-0.nc" 
        r = requests.get(url14, allow_redirects = True)
        open(f'{path}/goes14onemin.nc', "wb").write(r.content)

    if not os.path.exists(f'{path}/goes15onemin.nc'):
        url15 = f"https://www.ncei.noaa.gov/data/goes-space-environment-monitor/access/science/xrs/goes15/xrsf-l2-avg1m_science/sci_xrsf-l2-avg1m_g15_s20100331_e20200304_v1-0-0.nc"
        r = requests.get(url15, allow_redirects = True)
        open(f'{path}/goes15onemin.nc', "wb").write(r.content)


    lastday = "0"+str(int(date.strftime("%d"))-3) if ((int(date.strftime("%d"))-3)//10==0) else str(int(date.strftime("%d"))-3)
    print(lastday)

    if os.path.exists(f'{path}/goes16onemin.nc'):
        os.remove(f'{path}/goes16onemin.nc')
    
    url16 = f"https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/goes16/l2/data/xrsf-l2-avg1m_science/sci_xrsf-l2-avg1m_g16_s20170207_e20{y}{m}{lastday}_v2-2-0.nc"
    r = requests.get(url16, allow_redirects = True)
    open(f'{path}/goes16onemin.nc', "wb").write(r.content)



    if os.path.exists(f'{path}/goes17onemin.nc'):
        os.remove(f'{path}/goes17onemin.nc')
    url17 = "https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/goes17/l2/data/xrsf-l2-avg1m_science/sci_xrsf-l2-avg1m_g17_s20180601_e20230110_v2-2-0.nc" #f"https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/goes17/l2/data/xrsf-l2-avg1m_science/sci_xrsf-l2-avg1m_g17_s20180601_e20{y}{m}{lastday}_v2-2-0.nc"
    r = requests.get(url17, allow_redirects = True)
    open(f'{path}/goes17onemin.nc', "wb").write(r.content)
    print("UPDATED")
    # else:
    #     ds = nc.Dataset(f"./goes{version}onemin.nc")
    #     # for var in ds.variables.values():
    #     #     print(var)
    #     xrs = ds["xrsb_flux"]
    #     print(xrs)
#         for mint in xrs:
#             if int(str(mint)[-1])<7:
#                 pass# print(mint)
    
    

# getLatest("/Users/jhou/LMSALDataSetupTaskOriginal/testdata", "16")
sat_life = {
        "goes13": [dt.datetime(2013, 6, 1, 0, 0), dt.datetime(2017, 12, 31, 0, 0)], 
        "goes14": [dt.datetime(2009, 9, 1, 0, 0), dt.datetime(2020, 3, 31, 0, 0)], 
        "goes15": [dt.datetime(2010, 3, 31, 0, 0), dt.datetime(2020, 3, 31, 0, 0)], 
        "goes16": [dt.datetime(2017, 2, 7, 0, 0), datetime.now()], 
        "goes17": [dt.datetime(2018, 6, 1, 0, 0), datetime.now()]
    }
def getOldCalib():
    # "https://satdat.ngdc.noaa.gov/sem/goes/data/avg/2019/12/goes15/netcdf/g15_xrs_1m_20191201_20191231.nc"
    root = "https://satdat.ngdc.noaa.gov/sem/goes/data/avg"
    for i in range(9, 21):
        for x in range(1, 13):
            first = dt.datetime(2000+i, x, 1, 0, 0)
            last = dt.datetime(2000+i, x, calendar.monthrange(2000+i, x)[1])
            lastday = last.day
            stri = "0"+str(i) if ((i)//10==0) else str(i)
            strx = "0"+str(x) if ((x)//10==0) else str(x)
            
            if(x==2):
                if(i==12 or i==16):
                    lastday = 29#dt.datetime(2000+i, x, 29, 0, 0)
            if sat_life["goes13"][0] <= first and sat_life["goes13"][1] >= last:
                url = f"/20{stri}/{strx}/goes13/netcdf/g13_xrs_1m_20{stri}{strx}01_20{stri}{strx}{lastday}.nc"
                print(root+url)
                r = requests.get(root+url, allow_redirects = True)
                open(f"./20{stri}/g13_xrs_1m_20{stri}{strx}01_20{stri}{strx}{lastday}.nc", "wb").write(r.content)
                
            if sat_life["goes14"][0] <= first and sat_life["goes14"][1] >= last:
                url = f"/20{stri}/{strx}/goes14/netcdf/g14_xrs_1m_20{stri}{strx}01_20{stri}{strx}{lastday}.nc"
                print(root+url)
                r = requests.get(root+url, allow_redirects = True)
                open(f"./20{stri}/g14_xrs_1m_20{stri}{strx}01_20{stri}{strx}{lastday}.nc", "wb").write(r.content)
                
            if sat_life["goes15"][0] <= first and sat_life["goes15"][1] >= last:
                url = f"/20{stri}/{strx}/goes15/netcdf/g15_xrs_1m_20{stri}{strx}01_20{stri}{strx}{lastday}.nc"
                print(root+url)
                r = requests.get(root+url, allow_redirects = True)
                open(f"./20{stri}/g15_xrs_1m_20{stri}{strx}01_20{stri}{strx}{lastday}.nc", "wb").write(r.content)
    print("DONE")

# getOldCalib()

def stitchUncalibMonthsTogether(goestype): #stitch old together
    xrslist = []
    for i in range(9, 21):
        stri = "0"+str(i) if ((i)//10==0) else str(i)
        path = f"/Users/jhou/20{stri}"
        files = []
        for file in os.listdir(path):
            if f"g{goestype}_xrs" in f:
                files.append(file)
        sortedlist = []
        for n in range(1,13):
            strn = "0"+str(n) if ((n)//10==0) else str(n)
            for fn in files:
                if f"g14_xrs_1m_20{strn}" in fn:
                    sortedlist.append(fn)
        
        for f in files:
            
            print(path+"/"+f)
            print("here")
            try:
                ds = nc.Dataset(path+"/"+f)
                xrs = ds['B_AVG']
                times = ds['time_tag']
                initial_time = float(times[0].data)+28740000
                for i in range(1, len(xrs)):
                    xrsdict = {}
                    current = float(times[i].data+28740000)
                    if current == initial_time+60000:
                        # print("yes!")
                        xrsdict['time'] = str(dt.datetime.fromtimestamp(current/1000))
                        xrsdict['flux'] = float(xrs[i].data)
                        # print(xrsdict)
                        xrslist.append(xrsdict)
                        initial_time = current
                    else:
                        print("no")
                        temp = initial_time
                        print("not cont", current-initial_time)
                        print(current, initial_time)
                        while(temp<= current):
                            xrsdict['time'] = str(dt.datetime.fromtimestamp((temp+60000)/1000))
                            xrsdict['flux'] = 0
                            # print(xrsdict)

                            xrslist.append(xrsdict)
                            temp += 60000
                        initial_time = current
            except:
                month = int(f[15:17])
                lastday = int(f[26:28])
                for d in range(1, lastday+1):
                    for h in range(1,25):
                        for m in range(1,61):
                            xrsdict = {}
                            xrsdict['time'] = str(dt.datetime(2000+i, month, d, h, m))
                            xrsdict['flux'] = 0
                            xrslist.append(xrsdict)
                
    with open(f'oldg{goestype}_1minxrs.json', 'w') as f:
        json.dump(xrslist, f)
                
# stitchUncalibMonthsTogether("14")    

# def getEvents():
#     return True

# def stitchData(): # create ultimate list of 1-min cadence
#     return True

# def findFlux():