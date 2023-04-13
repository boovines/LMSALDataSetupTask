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
    with open(f'{eventType}evs.csv') as f:
        csvcontent = pd.read_csv(f)#csv.reader(f)
        # rows = []
        # for row in csvcontent:
        #     rows.append(row)
        return csvcontent.to_dict("records")

def getSRS():
    with open('srs-data.json') as f:
        data = json.load(f)
        for i in range(len(data)):
            data[i]["DATE"] = convertDate(data[i]["DATE"])
            
        return data

def getSRSbyAR():
    with open('srs-data-by-AR.json') as f:
        data = json.load(f)
        arnums = []
        for i in range(len(data)):
            key = list(data[i].keys())[0]
            data[i][key]["DATE"] = convertDate(data[i][key]["DATE"])
            arnums.append(key)
        return data, arnums

    
def getData():
    srsbyAR, arnums = getSRSbyAR()
    srs = getSRS()
    mergedevs = getEvents("merged")
    # herevs = getEvents("her")
    # noaaevs = getEvents("noaa")
    return arnums, srs, srsbyAR, mergedevs#, herevs, noaaevs
# print(getEvents("her"))





def findARregion(lon, lat): # find boundary area of each AR using diffrot
    bl = [lon-5, lat-5]
    tr = [lon+5, lat+5]
    c = [lon, lat]
    return bl, tr, c

# https://docs.sunpy.org/en/stable/generated/gallery/differential_rotation/differentially_rotated_coordinate.html#sphx-glr-generated-gallery-differential-rotation-differentially-rotated-coordinate-py
# https://github.com/sunpy/sunpy/blob/main/docs/whatsnew/1.0.rst
def diffRot(point, starttime, duration):
    lat = int(point[1:3]) if point[0] == "N" else int(point[1:3]) * -1
    long = int(point[4:6]) if point[3] == "W" else int(point[4:6]) * -1
    hrs = (int(duration[0:2])+int(duration[2:4])/60)*u.hour
    # hrs = duration*u.hour#(int(duration[0:2])+int(duration[2:4])/60)*u.hour
    if hrs == 0:
        return point
    
    start_time = starttime
    point = SkyCoord(long*u.deg, lat*u.deg, obstime = start_time, frame=HeliographicStonyhurst)
    # print(point)
    durations = [hrs]*u.hour#np.concatenate([range(-5, 0), range(1, 6)]) * u.day
    diffrot_point = RotatedSunFrame(base=point, duration=durations)
    # print(diffrot_point)
    transformed_diffrot_point = diffrot_point.transform_to(HeliographicStonyhurst)
    # print(transformed_diffrot_point)
    return transformed_diffrot_point.lon.degree, transformed_diffrot_point.lat.degree



def inbounds(bl, tr, loc):
    try:
        long = int(loc[1:3]) if loc[0] == "N" else int(loc[1:3]) * -1
        lat = int(loc[4:6]) if loc[3] == "W" else int(loc[4:6]) * -1
        return (bl[0] < long and tr[0] > long) and (bl[1] < lat and tr[1] > lat)
    except:
        return False

import time

def findMatches(ar, allevs): # use bottomleft topright to create array of ars that are valid, find ar that is closest to event region, if none, return none
    loc = ar["LOCATION"]
    date = ar["DATE"]
    matchedevs = []
    count = 0
    evlist = []
    for ev in allevs:
        evdate = ev["DATE"] #dt.datetime.strptime("2010-11-13", "%Y-%m-%d")
        # print(evdate)
        # print(str(evdate)[:-9], type(evdate), "\n", str(date), type(evdate2), "\n", str(evdate)[:-9]==str(date)) # FIX THIS THSLGL:HJGNSF:LJNGL:JSFH"LGHSFKL"KL:FS?GJ:SFJGKF:GNz
        # print(evdate, date) if evdate==date else print(".")
        evnum = int(ev["ARNUMBER"] % 10000) if (not np.isnan(ev["ARNUMBER"])) else 0
        # print(evnum, int(ar["ARNUM"]), evnum == int(ar["ARNUM"]))
        # if (evnum == int(ar["ARNUM"])):
        #     print("here1")
        #     matchedevs.append(ev)
        # el
        if (evdate==str(date)):
            count+=1
            evlist.append(ev)
            # print("here2")
            duration = f"{ev['PEAK']:04d}"
            # print(date, type(date), "hereherehere")
            # print(duration, type(duration), loc, type(loc))
            # try:
            lon, lat = diffRot(loc, str(date), duration)
            bl, tr, c = findARregion(lon, lat)
            # print(evdate, str(date))
            # print(bl, tr, ev["LOCATION"])
            if(inbounds(bl, tr, ev["LOCATION"])):
                print(str(evdate)[:-9], str(date))
                print(bl, tr, ev["LOCATION"])
                print("IWIWIWIIWWJTIWEOIGJOIWRJGOIJD:GJ:LDWJ:OIFJ:OHPEFIHBOEFH:BFH:BJHFKJBHLEFJKHLKJFHELKJHEFBG")
                # print(ev["LOCATION"])
                matchedevs.append(ev)
            # except:
            #     pass
        else:
            # print("here3")
            # time.sleep(1)
            pass
    # print(evlist, count)
    return matchedevs
    
    # find the ar with smallest dist, return

def saveFile(d1, d2):
    import pickle
    with open('oldAREventAssignment.pickle', 'wb') as handle:
        pickle.dump(d1, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
def compileEvents():
    arnums, old_srs, srsbyAR, mergedevs = getData()
    srsandevents = []
    srsandeventsbyAR = []
    
    matchedARs = []
    
    
    
    testsrs = []
    numtests = 100
    print(len(old_srs))
    srs = []
    for i in range(len(old_srs)):
        if old_srs[i] not in old_srs[i + 1:]:
            srs.append(old_srs[i])
    print(len(srs))
    
    for i in range(numtests):
        # print(srs[i])
        testsrs.append(srs[i])
    
    for ar in srs:
        matchedEvs = findMatches(ar, mergedevs)
        count = 0
        # for match in matchedEvs:
        #     print(ar, match)
        #     if(ar==match):
        #         count+=1
        # print(count/len(matchedEvs))
        # print(matchedEvs)
        matchdict = ar
        matchdict["EVENTS"] = matchedEvs
        
        if len(matchedEvs)>0:
            matchedARs.append(ar["ARNUM"])
        
        srsandevents.append(matchdict)
        
        matchdictbyAR = {ar["ARNUM"]: matchdict}
        srsandeventsbyAR.append(matchdictbyAR)
    print(matchedARs)
    # print(srsandevents)
    
    saveFile(srsandevents, srsandeventsbyAR)

compileEvents()








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
