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
# import datetime

months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def convertDate(date):
    # print(date)
    dlist = date.split(' ')
    dlist[1] = months[dlist[1]]
    dlist = [int(d) for d in dlist]
    
    return dt.date(dlist[0], dlist[1], dlist[2])

#get data
def getEvents(eventType):
    with open(f'new{eventType}evs5.csv') as f:
        csvcontent = pd.read_csv(f)#csv.reader(f)
        # rows = []
        # for row in csvcontent:
        #     rows.append(row)
        return csvcontent#.to_dict("records")

def getSRS():
    with open('srs-data.json') as f:
        data = json.load(f)
        for i in range(len(data)):
            data[i]["DATE"] = convertDate(data[i]["DATE"])
            
        return data

def getSRSbyAR():
    import pickle
    with open("srsdata.pkl", 'rb') as handle:
        # {"XRS": [DF of goes13 data with date as index and flux, DF of goes14, ..., DF of GOES17], "TIMES": [...], "FLAGS": [...]}
        data = pickle.load(handle)
        arnums = []
        for i in range(len(data)):
            key = list(data[i].keys())[0]
            # data[i][key]["DATE"] = convertDate(data[i][key]["DATE"])
            arnums.append(key)
        return data, arnums

    
def getData():
    srsbyAR, arnums = getSRSbyAR()
    # srs = getSRS()
    mergedevs = getEvents("merged")
    # herevs = getEvents("her")
    # noaaevs = getEvents("noaa")
    return arnums, srsbyAR, mergedevs#, herevs, noaaevs
# print(getEvents("her"))





def findARregion(lon, lat): # find boundary area of each AR using diffrot
    bl = [lon-5, lat-5]
    tr = [lon+5, lat+5]
    c = [lon, lat]
    return bl, tr, c

# https://docs.sunpy.org/en/stable/generated/gallery/differential_rotation/differentially_rotated_coordinate.html#sphx-glr-generated-gallery-differential-rotation-differentially-rotated-coordinate-py
# https://github.com/sunpy/sunpy/blob/main/docs/whatsnew/1.0.rst
def diffRot(point, starttime, duration):
    # print(point, starttime, duration)
    lat = int(point[1:3]) if point[0] == "N" else int(point[1:3]) * -1
    long = int(point[4:6]) if point[3] == "W" else int(point[4:6]) * -1
    
    if dt.datetime(duration.year, duration.month, duration.day) == starttime:
        hrs = (duration.hour+duration.minute/60)*u.hour
        durations = [hrs]*u.hour
    elif dt.datetime(duration.year, duration.month, duration.day) == dt.datetime(starttime.year, starttime.month, starttime.day)- dt.timedelta(days=1):
        hrs = (24-(duration.hour+duration.minute/60))*u.hour
        durations = [hrs]*u.hour
        durations = -durations
    else:
        hrs = (24+duration.hour+duration.minute/60)*u.hour
        durations = [hrs]*u.hour
    
    
    # hrs = duration*u.hour#(int(duration[0:2])+int(duration[2:4])/60)*u.hour
    if hrs == 0:
        return point
    
    start_time = str(starttime)
    point = SkyCoord(long*u.deg, lat*u.deg, obstime = start_time, frame=HeliographicStonyhurst)
    # print(point)
    
    diffrot_point = RotatedSunFrame(base=point, duration=durations)
    # print(diffrot_point)
    transformed_diffrot_point = diffrot_point.transform_to(HeliographicStonyhurst)
    # print(transformed_diffrot_point)
    return transformed_diffrot_point.lon.degree, transformed_diffrot_point.lat.degree



def inbounds(bl, tr, loc):
    try:
        long = int(loc[1:3]) if loc[0] == "N" else int(loc[1:3]) * -1
        lat = int(loc[4:6]) if loc[3] == "W" else int(loc[4:6]) * -1
        return (bl[0] < lat and tr[0] > lat) and (bl[1] < long and tr[1] > long)
    except:
        return False
    # try:
    #     long = int(loc[1:3]) if loc[0] == "N" else int(loc[1:3]) * -1
    #     lat = int(loc[4:6]) if loc[3] == "W" else int(loc[4:6]) * -1
    #     return (bl[0] < long and tr[0] > long) and (bl[1] < lat and tr[1] > lat)
    # except:
    #     return False

import time

def findMatches(ar, allevs): # use bottomleft topright to create array of ars that are valid, find ar that is closest to event region, if none, return none
    loc = ar["LOCATION"]
    date = ar["DATE"]
    matchedevs = []
    count = 0
    today = date #- dt.timedelta(days=1)
    tomorrow = date + dt.timedelta(days=2)
    evsInRange = allevs.loc[allevs["PEAK"].between(str(today),str(tomorrow))]
    # print(evsInRange)
    evlist = []
    mms = []
    for index, ev in evsInRange.iterrows():
        # evdate = ev["DATE"]
        
        evnum = int(ev["ARNUMBER"] % 10000) if (not np.isnan(ev["ARNUMBER"])) else 0 # do this if not new
        
        if evnum != ar["ARNUM"]: # if !=, check for arnum after diff rot if no other choice, if ==, check arnum
            print("found arnummmmmmmmmmmm")
            matchedevs.append(ev)
        else:
            # print(evdate, date)
            # if (evdate==date):
            count+=1
            evlist.append(ev)
            # print("here2")
            duration = ev['PEAK']
            duration2 = dt.datetime.strptime(duration, '%Y-%m-%d %H:%M:%S')
            # print(date, type(date), "hereherehere")
            # print(duration, type(duration), loc, type(loc))
            # try:
            # print(duration)
            lon, lat = diffRot(loc, date, duration2)
            print(lon,lat)
            bl, tr, c = findARregion(lon, lat)
            # print(evdate, str(date))
            # print(bl, tr, ev["LOCATION"])
            if (type(ev["LOCATION"]) == type("hi")): # and type(ev["LOCATION"]) == type("hi")
                la = int(ev["LOCATION"][1:3]) if ev["LOCATION"][0] == "N" else int(ev["LOCATION"][1:3]) * -1
                lo = int(ev["LOCATION"][4:6]) if ev["LOCATION"][3] == "W" else int(ev["LOCATION"][4:6]) * -1
                print(bl, tr, la, lo, ev["LOCATION"])
            
            
                if(inbounds(bl, tr, ev["LOCATION"])):
                    # print(str(evdate)[:-9], str(date))

                    print("ASSIGNEDASSIGNEDASSIGNEDASSIGNEDASSIGNEDASSIGNEDASSIGNEDASSIGNEDASSIGNEDASSIGNEDASSIGNEDASSIGNEDASSIGNED")
                    # print(ev["LOCATION"])
                    matchedevs.append(ev)
                    if evnum != ar['ARNUM'] and ev not in mms:
                        mms.append(ev)
            else:
                if evnum != ar["ARNUM"]: # if !=, don't check arnum first, if ==, check arnum
                    print("No LOCATION, only ARNUM available")
                    matchedevs.append(ev)
        # except:
        #     pass
        
    # print(evlist, count)
    return matchedevs, mms
    
    # find the ar with smallest dist, return

def saveFile(d1):
    import pickle
    with open('AREventAssignment3.pickle', 'wb') as handle:
        pickle.dump(d1, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
def compileEvents():
    arnums, srsbyAR, mergedevs = getData()
    srsandevents = []
    srsandeventsbyAR = []
    
    matchedARs = []
    
    
    
    testsrs = []
    numtests = 100
    
    newSRSbyAR = []
    mismatches = []
    for i in range(len(srsbyAR)):
        allMatchedEvs = []
        # print(srsbyAR[i][arnums[i]])
        mmsall = []
        for day in srsbyAR[i][arnums[i]]:
            matchedEvs, mms = findMatches(day, mergedevs)
            allMatchedEvs.append(matchedEvs)
            mmsall.append(mms)
        mmsall = [item for sublist in mmsall for item in sublist]
        mismatches.append([arnums[i], mmsall])
        allMatchedEvs = [item for sublist in allMatchedEvs for item in sublist]
        
        newdict = srsbyAR[i]
        newdict[f"{arnums[i]}_EVENTS"] = allMatchedEvs
        
        newSRSbyAR.append(newdict)
    
    bothcount = 0
    for index, ev in mergedevs.iterrows(): 
        if (not np.isnan(ev["ARNUMBER"])) and type(ev["LOCATION"]) == type("hi"):
            bothcount+=1
    falsecount = len([item for sublist in mismatches for item in sublist])
    print(falsecount/bothcount)


    
    # newsrsby ar get rid of repitition
    
    # get arnum list and use that to loop through events
    
    # save the differentially rotated result
    # make 3xlen(assigned events) with each item [event_data, differentially_rotated, arnum]
    
    # if two event_datas match, evaluate the distance. whichever has the greater distance is added to the "remove list"
    
    
     
    saveFile(newSRSbyAR)
    
#     print(len(old_srs))
    
    
#     srs = []
#     for i in range(len(old_srs)):
#         if old_srs[i] not in old_srs[i + 1:]:
#             srs.append(old_srs[i])
#     print(len(srs))
    
#     for i in range(numtests):
#         # print(srs[i])
#         testsrs.append(srs[i])
    
#     for ar in srs:
#         matchedEvs = findMatches(ar, mergedevs)
#         count = 0
#         # for match in matchedEvs:
#         #     print(ar, match)
#         #     if(ar==match):
#         #         count+=1
#         # print(count/len(matchedEvs))
#         # print(matchedEvs)
#         matchdict = ar
#         matchdict["EVENTS"] = matchedEvs
        
#         if len(matchedEvs)>0:
#             matchedARs.append(ar["ARNUM"])
        
#         srsandevents.append(matchdict)
        
#         matchdictbyAR = {ar["ARNUM"]: matchdict}
#         srsandeventsbyAR.append(matchdictbyAR)
#     print(matchedARs)
#     # print(srsandevents)
    
#     saveFile(srsandevents)

# compileEvents()








# import netCDF4 as nc


# loop through each event in input csv
# for each, grab date and time of peak and location

# if time of peak exceeds 1200, move date up one; else, keep it as is 
# search for srs that matches date and save it to var
# plug in srs location and date and time into the differential rotation eq, let it give new location
# define 10x10 heliographic degree area of tolerance
# if event falls within, add it to srs list; else, add it to unassigned list

def diffRot2(point, starttime, duration):
    #sunpy method is stupid, so try rotating with astropy
    aia_map = sunpy.map.Map(sunpy.data.sample.AIA_193_IMAGE)
    
    # print(duration)
    mins = (int(duration[0:2])+int(duration[2:4])/60)*u.hour
    if mins == 0:
        return point
    long = int(point[1:3]) if point[0] == "N" else int(point[1:3]) * -1
    lat = int(point[4:6]) if point[3] == "W" else int(point[4:6]) * -1
    # print(long, lat, u.deg, starttime)
    startpoint = SkyCoord(long, lat, unit=u.deg,
                     frame="heliographic_stonyhurst",
                     obstime=dt.datetime(starttime.year, starttime.month, starttime.day),
                     rsun=aia_map.coordinate_frame.rsun)
    transformed = startpoint # point.transform_to(sunpy.coordinates.HeliographicStonyhurst) #1: get heliographic coordinates
    w = (14.713 + -2.396*(math.sin(transformed.lat.degree)**2) + -1.787*(math.sin(transformed.lat.degree)**4)) * u.degree/u.day #2: get angular velocity at longitude (https://en.wikipedia.org/wiki/Solar_rotation)
    new = SkyCoord(transformed.lon.degree*u.degree + w*mins, transformed.lat.degree*u.degree, frame=sunpy.coordinates.HeliographicStonyhurst) #3: create new coordinate using w
    return new.lon.degree, new.lat.degree
