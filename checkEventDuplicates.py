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

import datetime as dt

import requests

def getEvents():
    with open(f'herevs524.csv') as f:
        csvcontent = pd.read_csv(f)#csv.reader(f)
        # rows = []
        # for row in csvcontent:
        #     rows.append(row)
        return csvcontent#.to_dict("records")

def isCenteringDup(ev1, ev2):
    c1 = ev1["LOCATION_HER"] if (type(ev1["LOCATION_HER"]) == type("hi")) else 0
    c2 = ev2["LOCATION_HER"] if (type(ev2["LOCATION_HER"]) == type("hi")) else 1
    return c1==c2

def isARDup(ev1, ev2):
    ar1 = int(ev1["ARNUMBER"] % 10000) if (not np.isnan(ev1["ARNUMBER"])) else 0
    ar2 = int(ev2["ARNUMBER"] % 10000) if (not np.isnan(ev2["ARNUMBER"])) else 1
    return ar1==ar2

def isPeakDup(ev1, ev2):
    p1 = ev1["PEAK"] if (not np.isnan(ev1["PEAK"])) else 0
    p2 = ev2["PEAK"] if (not np.isnan(ev2["PEAK"])) else 1
    return p1==p2


def isClassMagDup(ev1, ev2):
    c1 = ev1["MAGNITUDE_HER"] if (type(ev1["MAGNITUDE_HER"]) == type("hi")) else 0
    c2 = ev2["MAGNITUDE_HER"] if (type(ev2["MAGNITUDE_HER"]) == type("hi")) else 1
    return c1==c2

def getDupType(ev1, ev2):
    duptypes = []
    peak = 0
    cmag = 0
    centering = 0
    ar = 0
    if isPeakDup(ev1,ev2):
        duptypes.append("PEAK")
        peak = 1
    if isClassMagDup(ev1, ev2):
        duptypes.append("CLASS/MAG")
        cmag = 1
    if isCenteringDup(ev1, ev2):
        duptypes.append("CENTERING")
        centering = 0
    if isARDup(ev1,ev2):
        duptypes.append("AR")
        ar = 0
    return duptypes, peak, cmag, centering, ar

def detectDups():
    evlist = getEvents()
    # count = 0
    alldups = []
    classdupcount = 0
    ardupcount = 0
    centeringdupcount = 0
    peakdupcount = 0
    atleast1 = 0
    edict = evlist.to_dict()
    for i in range(len(edict)-1):
        # evdups = []
        #print(df.loc[i, "Fee"], df.loc[i, "Courses"])
        ev = edict[i]
        ev2 = edict[i+1]
        # date = ev["DATE"]
        count = 0
        # today = date #- dt.timedelta(days=1)
        # tomorrow = date + dt.timedelta(days=2)
        # evsInRange = evlist.loc[evlist["DATE"].between(str(today),str(tomorrow))]
        # for index2, ev2 in evsInRange.iterrows():
        inside1 = ev["PEAK"]>ev2["START"] and ev["PEAK"]<ev2["END"]
        inside2 = ev2["PEAK"]>ev["START"] and ev2["PEAK"]<ev["END"]
        if inside1 or inside2:
            duptypes, peak, cmag, centering, ar = getDupType(ev,ev2)
            # evdups.append(duptypes)
            peakdupcount += peak
            centeringdupcount += centering
            ardupcount += ar
            classdupcount += cmag
            atleast1 += 1
        alldups.append([i, duptypes])
        print("Class/Mag Related Duplicates:", classdupcount, " ", classdupcount/atleast1*100, "%")
        print("Centering Related Duplicates:", centeringdupcount, " ", centeringdupcount/atleast1*100, "%")
        print("AR Related Duplicates:", ardupcount, " ", ardupcount/atleast1*100, "%")
        print("Peak Time Related Duplicates:", peakdupcount, " ", peakdupcount/atleast1*100, "%")
    # for index, ev in evlist.iterrows():
    #     # evdups = []
    #     date = ev["DATE"]
    #     count = 0
    #     # today = date #- dt.timedelta(days=1)
    #     # tomorrow = date + dt.timedelta(days=2)
    #     # evsInRange = evlist.loc[evlist["DATE"].between(str(today),str(tomorrow))]
    #     # for index2, ev2 in evsInRange.iterrows():
    #     inside1 = ev["PEAK"]>ev2["START"] and ev["PEAK"]<ev2["END"]
    #     inside2 = ev2["PEAK"]>ev["START"] and ev2["PEAK"]<ev["END"]
    #     if inside1 or inside2:
    #         duptypes, peak, cmag, centering, ar = getDupType(ev,ev2)
    #         # evdups.append(duptypes)
    #         peakdupcount += peak
    #         centeringdupcount += centering
    #         ardupcount += ar
    #         classdupcount += cmag
    #         atleast1 += 1
    #     alldups.append([index, duptypes])
