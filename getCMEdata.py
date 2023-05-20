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
# from sunpy.net import Fido
# from sunpy.net import attrs as a
import matplotlib.pyplot as plt

import sunpy.coordinates
import sunpy.data.sample
from sunpy.io.special import srs

import datetime as dt
from datetime import date
from datetime import datetime
import json
import csv

import requests
import ssl
from urllib.request import urlopen
import netCDF4 as nc # https://towardsdatascience.com/read-netcdf-data-with-python-901f7ff61648

import calendar

from dateutil import parser

months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


#time, position angle, cme angular width, velocity 
def sortList(l):
    return sorted(l, key=lambda x: x['DATE'])

def getEvents(eventType):
    with open(f'{eventType}evs.csv') as f:
        csvcontent = pd.read_csv(f)#csv.reader(f)
        # rows = []
        # for row in csvcontent:
        #     rows.append(row)
        return csvcontent

def findLocation(eventDF, date):
    for i in range(len(eventDF["DATE"])):
        # print(str("%04d" % (eventDF["START"][i]))[0:2])
        
        start = parser.parse(eventDF["DATE"][i] + " " + str("%04d" % (eventDF["START"][i]))[0:2] + ":" + str("%04d" % (eventDF["START"][i]))[2:4])
        # print(start)
        end = parser.parse(eventDF["DATE"][i] + " " + str("%04d" % (eventDF["END"][i]))[0:2] + ":" + str("%04d" % (eventDF["END"][i]))[2:4])
        if(start <= date and end >= date):
            return eventDF["LOCATION"][i]
    return ""
    
def parseTxtFile(r, catalog):
    r = str(r)
    
    cmedict = {}
    eventDF = getEvents("her")
    if catalog == "cdaw":
        r = [word for word in r.split(" ") if word != ""]
        if (len(r)>1):
            # print(r[1][0])
            if (r[1][0] !="=" and r[1] != "Date" and r[1] != "PA"):
                # print(r)
                # print(r[0])
                cmedict["DATE"] = dt.datetime(int(r[0][2:6]), int(r[0][7:9]), int(r[0][10:12]), int(r[1][0:2]), int(r[1][3:5]))#, int(r[1][6:8]))
                cmedict["POS_ANG"] = int(r[2]) if (r[2] != "Halo") else r[2]
                cmedict["ANG_WIDTH"] = int(r[3])
                cmedict["VELOCITY"] = int(r[4])
                loc = findLocation(eventDF, cmedict["DATE"]) 
                print(loc)
                cmedict["LOCATION"] = loc
                print(cmedict)
            # else:
            #     print(r)
        
        return cmedict
    
    elif catalog == "seeds": #MAKE SURE THESE R RIGHT
        r = [word for word in r.split(" ") if word != ""]
        # print(r)
        # print(r[0])
        cmedict["DATE"] = dt.datetime(int(r[0][2:6]), int(r[0][7:9]), int(r[0][10:12]), int(r[1][0:2]), int(r[1][3:5]))#, int(r[1][6:8]))
        cmedict["POS_ANG"] = int(r[3])
        cmedict["ANG_WIDTH"] = int(r[4])
        cmedict["VELOCITY"] = int(r[5])
        loc = findLocation(eventDF, cmedict["DATE"]) 
        print(loc)
        cmedict["LOCATION"] = loc
        print(cmedict)
        return cmedict
    
    elif catalog == "cactus":
        # print("hi")
        # if (r[0] != ":" and r[0] != " " and r[0] != "#"):
        r = [word for word in r.split(" ") if word != ""]
        # print(r)
        cmedict["DATE"] = dt.datetime(int(r[0][5:9]), int(r[0][10:12]), int(r[0][13:15]), int(r[1][0:2]), int(r[1][3:5]))
        # print(r[4][:-1])
        cmedict["POS_ANG"] = int(r[4][:-1])
        cmedict["ANG_WIDTH"] = int(r[5][:-1])
        cmedict["VELOCITY"] = int(r[6][:-1])
        loc = findLocation(eventDF, cmedict["DATE"]) 
        print(loc)
        cmedict["LOCATION"] = loc
        print(cmedict)
        return cmedict
        
    else:
        print("Invalid catalog")
print(parseTxtFile("  0047|2022/07/10 02:24| 02 | 355| 044| 0277| 0039| 0200| 0347|    ", "cactus"))
        
def getTxtFiles(catalog):
    cmelist = []
    if catalog == "cdaw":
        root = "https://cdaw.gsfc.nasa.gov/CME_list/UNIVERSAL/text_ver/"
        
        for i in range(2010, 2023):
            last = 13 if (i!=2022) else (date.today().month)+1
            for x in range(1, last):
                strx = "0"+str(x) if (x//10==0) else str(x)
                fn = f"univ{i}_{strx}.txt"
                try:
                    r = urlopen(root+fn)#requests.get(root+fn, allow_redirects = True)
                    for line in r.readlines():
                        parseddict = parseTxtFile(line, catalog)
                        # print(parseddict)
                        io = True
                        if parseddict != {}:
                            cmelist.append(parseddict) 
                except:
                    pass
        return cmelist
    elif catalog == "seeds":
        root = "http://spaceweather.gmu.edu/seeds/detection/monthly/"
        for i in range(2010, 2023):
            last = 13 if (i!=2022) else (date.today().month)+1
            for x in range(1, last):
                strx = "%02d" % (x)
                fn = f"{i}_{strx}_monthly.txt"
                try:
                    r = urlopen(root+fn)
                    for line in r.readlines():
                        cmelist.append(parseTxtFile(line, catalog))
                except:
                    pass
        return cmelist
    elif catalog == "cactus": 
        for i in range(2010, 2023):
            first = 1 if (i!=2010) else 7
            last = 13 if (i!=2022) else (date.today().month)+1
            for x in range(first, last):
                strx = "0"+str(x) if (x//10==0) else str(x)
                fn = f"./cactus/{i}_{strx}.txt"
                # context = ssl._create_unverified_context()
                try:
                    with open(fn) as r:
                        lines = r.readlines()
                        count = 0
                        for line in lines:
                            if("# Flow|" in line):
                                break
                            else:
                                count+=1
                        # print(count)
                        for z in range(27, count-1):
                            # print(lines[z])
                            # parseTxtFile(lines[z], catalog)
                            cmelist.append(parseTxtFile(lines[z], catalog))
                except:
                    pass
        return cmelist
    else:
        print("Invalid catalog")
        return True
    # return True

# getTxtFiles("cactus")



def getDFs(evlist):
    dfs = []
    for ev in evlist:
        dfs.append(pd.DataFrame(ev, index = [0]))
    return pd.concat(dfs)

# cmelist1 = getTxtFiles("cdaw")
# sortedlist1 = sortList(cmelist1)
# print(cmelist1)
# cdawDF = getDFs(sortedlist1)
# print(cdawDF)

# cmelist2 = getTxtFiles("seeds")
# sortedlist2 = sortList(cmelist2)
# print(cmelist2)
# seedsDF = getDFs(sortedlist2)
# print(seedsDF)

# cmelist3 = getTxtFiles("cactus")
# sortedlist3 = sortList(cmelist3)
# print(cmelist3)
# cactusDF = getDFs(sortedlist3)
# print(cactusDF)

def mergeLists(list1, list2): # for each item in list 1, compare the DATE and the PEAK time to that in list 2      if there is match, compare items in each list, add a new column in df for new mag if it exists
    newlist = []
    uniquelist = []
    print(len(list2) + len(list2))
    for cme2 in list2:
        match = False
        for cme1 in list1:
            # print(event1)
            if(cme1["DATE"] == cme2["DATE"]):# and cme1["POS_ANG"] == cme2["POS_ANG"] and cme1["ANG_WIDTH"] == cme2["ANG_WIDTH"]):
                match = True
                newevent = cme2
                
                newlist.append(newevent)
                break
                
        if not match:
            # print("type3")
            # print(event2)
            newevent = cme2
            # magnitudes1 = []
            # magnitudes1.append(event2["MAGNITUDE"])
            
            newlist.append(newevent) #3
            
    for cme1 in list1:
        match2 = False
        # print(event1) 
        for cme2 in list2:
            if(cme1["DATE"] == cme2["DATE"]):# and cme1["POS_ANG"] == cme2["POS_ANG"] and cme1["ANG_WIDTH"] == cme2["ANG_WIDTH"]):
                match2 = True
                break
        if not match2:
            # print("type4")
            # print(event1)
            
            newevent = cme1
            
            newlist.append(newevent) #4
    return newlist



        
def getCMEs(cmecatalog):
    with open(f'{cmecatalog}CMEs.csv') as f:
        csvcontent = pd.read_csv(f)#csv.reader(f)
        # rows = []
        # for row in csvcontent:
        #     rows.append(row)
        print(csvcontent)
        return csvcontent.to_dict("records")

def getData():
    
    cdaw = getCMEs("cdaw")
    seeds = getCMEs("seeds")
    cactus = getCMEs("cactus")
    return cdaw, seeds, cactus    

# def
cdaw, seeds, cactus = getData()

cmelist4 = mergeLists(cdaw, seeds)
cmelist5 = mergeLists(cmelist4, cactus)
sortedMerged = sortList(cmelist5)

mergedDF = getDFs(sortedMerged)

# print(cdawDF)
# print(seedsDF)
# print(mergedDF)



# cdawDF.to_csv("cdawCMEs.csv", index=False)
# seedsDF.to_csv("seedsCMEs.csv", index=False)
# cactusDF.to_csv("cactusCMEs.csv", index=False)
mergedDF.to_csv("mergedCMEs.csv", index=False)