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
from datetime import date
import json
import csv

from astropy.time import TimeDelta

from sunpy.physics.differential_rotation import diff_rot, solar_rotate_coordinate
from sunpy.time import parse_time
from sunpy.coordinates import Helioprojective, HeliographicStonyhurst #USE STONYHURST solarmonitor.org SEND NABIL AN EMAIL ABT ERROR
from astropy.coordinates import SkyCoord

from sunpy.coordinates import RotatedSunFrame

import math
import sunpy.data.sample


lis = []
tfiscale = {"X": 10000, "M": 100000, "C": 1000000, "B": 10000000, "A": 100000000}

def getData(p):
    import pickle
    with open(f"{p}/AREventAssignment.pickle", 'rb') as handle:
        # {"XRS": [DF of goes13 data with date as index and flux, DF of goes14, ..., DF of GOES17], "TIMES": [...], "FLAGS": [...]}
        data = pickle.load(handle)
    return data

def getTFIsOnly(version):
    data = getData("/Users/jhou/LMSALDataSetupTaskOriginal/testdata619")
    tfilist = []
    lis = []
    arnums = []
    
    for i in range(len(data)):
        key = list(data[i].keys())[0]
        # data[i][key]["DATE"] = convertDate(data[i][key]["DATE"])
        arnums.append(key)
        
        
    for i in range(len(data)):
        tfi = 0
        for event in data[i][f"{arnums[i]}_EVENTS"]:
            # print(event["NEW_CALIB_MAG"])
            if type(event[f"{version}_CALIB_MAG"]) == type("HI"):
                # print(event[f"{version}_CALIB_MAG"], tfiscale[event[f"{version}_CALIB_MAG"][0]])
                print(event[f"{version}_CALIB_MAG"], event[f"{version}_CALIB_FLUX"], event[f"{version}_CALIB_FLUX"]*tfiscale[event[f"{version}_CALIB_MAG"][0]], tfiscale[event[f"{version}_CALIB_MAG"][0]])
                tfi+=event[f"{version}_CALIB_FLUX"]*tfiscale["C"]#event[f"{version}_CALIB_MAG"][0]]
        tfilist.append(["1"+arnums[i], tfi])
        lis.append(tfi)
    return tfilist

tfis = getTFIsOnly("NEW")

def getTFIs(version, data, arnums): # return tfi and ar
    # data = getData("/Users/jhou/LMSALDataSetupTaskOriginal/testdata612")
    tfilist = []
    lis = []
    
        
        
    for i in range(len(data)):
        tfi = 0
        # mags = [[ev[f"{version}_CALIB_FLUX"], ev["MAGNITUDE_NOAA"], ev["MAGNITUDE_HER"]] for ev in data[i][f"{arnums[i]}_EVENTS"]]
        # print(mags)
        # # tfi = 0
        # for mag in mags:
        #     if not np.isnan(mag[0]):
        #         tfi+=1000000*mag[0]
        #     elif not np.isnan(mag[1]):
        #         tfi+=tfiscale[mag[1][0]]*float(mag[1][1:])
        #     elif not np.isnan(mag[2]):
        #         tfi+=tfiscale[mag[2][0]]*float(mag[2][1:])
        #     else:
        #         pass
        # print(arnums[0],tfi)
        for event in data[i][f"{arnums[i]}_EVENTS"]:
            # print(event["NEW_CALIB_MAG"])
            if type(event[f"{version}_CALIB_MAG"]) == type("HI"):
                # print(event[f"{version}_CALIB_MAG"], tfiscale[event[f"{version}_CALIB_MAG"][0]])
                print(event[f"{version}_CALIB_MAG"], event[f"{version}_CALIB_FLUX"], event[f"{version}_CALIB_FLUX"]*tfiscale[event[f"{version}_CALIB_MAG"][0]], tfiscale[event[f"{version}_CALIB_MAG"][0]])
                tfi+=event[f"{version}_CALIB_FLUX"]*tfiscale["C"]#event[f"{version}_CALIB_MAG"][0]]
        data[i][f"TFI"] = tfi#{arnums[i]}_
        tfilist.append([arnums[i], tfi])
        lis.append(tfi)
    # print(data)
    return tfilist, data

# tfis = getTFIs("NEW")



# print(tfis)

# def getDFIs(): # {} return given dfi, date, and AR
#     data = getData()
#     dfilist = []
#     lis = []
#     arnums = []
    
#     for i in range(len(data)):
#         key = list(data[i].keys())[0]
#         # data[i][key]["DATE"] = convertDate(data[i][key]["DATE"])
#         arnums.append(key)
        
        
#     for i in range(len(data)):
#         tfi = 0
#         for event in data[i][f"{arnums[i]}_EVENTS"]:
            
#             if type(event[f"{version}_CALIB_MAG"]) == type("HI"):
#                 # print(event[f"{version}_CALIB_MAG"], tfiscale[event[f"{version}_CALIB_MAG"][0]])
                
#                 tfi+=event[f"{version}_CALIB_FLUX"]*tfiscale["C"]#event[f"{version}_CALIB_MAG"][0]]
#         tfilist.append(["1"+arnums[i], tfi])
#         lis.append(tfi)
#     return tfilist
    

def getSortedTFIs(fis):
    from operator import itemgetter
    sfis = sorted(fis, key=itemgetter(1), reverse=True)
    # print(stfis)
    return sfis#[s for s in sfis[:10]]
# print("\n", getTop10(tfis))

def sortList(l, attr, rev):
    return sorted(l, key=lambda x: x[attr], reverse=rev)

def restructureAssignments(data, arnums):
    # structure like such: [{12673}, {"12673_EVENTS":[{date1: [{event1},{event2}...], DFI: 1212}, {date2: ....}]}]
    # define new array
    newArr = []
    # looping through each day of SRS data available (sorted) attribute of each ar, group the events on same days
    for i in range(len(data)):
        
        ardays = sortList([arday for arday in data[i][f"{arnums[i]}"]], "DATE", False)
        
        eventsPerDay = []
        
        for a in ardays:
            l = []
            for e in data[i][f"{arnums[i]}_EVENTS"]:
                # print(type(a["DATE"]), type(e["DATE"]))
                if a["DATE"] == dt.datetime.strptime(e["DATE"], "%Y-%m-%d"):
                    # print(a["DATE"], e["DATE"])
                    l.append(e)
            eventsPerDay.append({a["DATE"]: l})
        
        data[i][f"{arnums[i]}_EVENTS_BY_DAY"] = eventsPerDay
        ardates = [arday["DATE"] for arday in ardays]
        data[i][f"{arnums[i]}_DATES"] = ardates
    
    # print(data)
    return data

def getDFIs(version, data, arnums):
    for i in range(len(data)):
        ardates = data[i][f"{arnums[i]}_DATES"]
        # print(ardates)
        # print(data[i][f"{arnums[i]}_EVENTS_BY_DAY"])
        for j in range(len(data[i][f"{arnums[i]}_EVENTS_BY_DAY"])):
            # for j in range(len(ardates)):
            day = data[i][f"{arnums[i]}_EVENTS_BY_DAY"][j]
            dfi = 0
            print(day, "dslafjalsdf;a", type(ardates[j]), ardates[j])
            print(day[ardates[j]])
            # if len(day[ardates[j]])==0:
            for val in day[ardates[j]]:
                dfi = dfi + val[f"{version}_CALIB_FLUX"]*tfiscale["C"]
            print("\n","asdklfj", day, day[ardates[j]], data[i][f"{arnums[i]}_EVENTS_BY_DAY"][j], "SDLFJLS") 
            data[i][f"{arnums[i]}_EVENTS_BY_DAY"][j]["DFI"] = dfi
    # print(data)
    return data


def saveFile(d1, p):
    import pickle
    with open(f'{p}/AREventAssignmentWithFIs.pickle', 'wb') as handle:
        pickle.dump(d1, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def injectFIassignments(p, version = "NEW"):
    data = getData(p)
    arnums = []
    
    for i in range(len(data)):
        key = list(data[i].keys())[0]
        # data[i][key]["DATE"] = convertDate(data[i][key]["DATE"])
        arnums.append(key)
    
    reAssignments = restructureAssignments(data, arnums)
    assignmentsWithDFIs = getDFIs(version, reAssignments, arnums)
    print(assignmentsWithDFIs)
    
    tfilist, assignmentsFinal = getTFIs(version, assignmentsWithDFIs, arnums)
    print(assignmentsFinal)
    sortedAssignmentsFinal = sortList(assignmentsFinal, "TFI", True)
    print(sortedAssignmentsFinal)
    
    stfilist = getSortedTFIs(tfilist)
    print(stfilist)
    
#     sortedAssignmentsFinal = []
    
#     for i in range(len(data)):
#         for tfi in sortedTFIs:
#             flux = tfi[1]
#             if flux == data[i][f"{arnums[i]}_TFI"]:
#                 print("found sorted event", data[i])
#                 sortedAssignmentsFinal.append(data[i])
    
#     print(sortedAssignmentsFinal)
    saveFile(sortedAssignmentsFinal, p)
    return assignmentsFinal, sortedAssignmentsFinal


    #loop through the first item in the TFI lists and add as separate attribute for each version of flux
    
    #
    
    
injectFIassignments("/Users/jhou/LMSALDataSetupTaskOriginal/testdata612")


