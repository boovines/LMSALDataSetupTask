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

def getData():
    import pickle
    with open("AREventAssignment2.pickle", 'rb') as handle:
        # {"XRS": [DF of goes13 data with date as index and flux, DF of goes14, ..., DF of GOES17], "TIMES": [...], "FLAGS": [...]}
        data = pickle.load(handle)
    return data


def getTFIs(version):
    data = getData()
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

tfis = getTFIs("NEW")



# print(tfis)

def getDFIs(): # {}
    data = getData()
    dfilist = []
    lis = []
    arnums = []
    
    for i in range(len(data)):
        key = list(data[i].keys())[0]
        # data[i][key]["DATE"] = convertDate(data[i][key]["DATE"])
        arnums.append(key)
        
        
    for i in range(len(data)):
        tfi = 0
        for event in data[i][f"{arnums[i]}_EVENTS"]:
            
            if type(event[f"{version}_CALIB_MAG"]) == type("HI"):
                # print(event[f"{version}_CALIB_MAG"], tfiscale[event[f"{version}_CALIB_MAG"][0]])
                
                tfi+=event[f"{version}_CALIB_FLUX"]*tfiscale["C"]#event[f"{version}_CALIB_MAG"][0]]
        tfilist.append(["1"+arnums[i], tfi])
        lis.append(tfi)
    return tfilist
    

def getTop10(fis):
    from operator import itemgetter
    sfis = sorted(fis, key=itemgetter(1), reverse=True)
    # print(stfis)
    return [s for s in sfis[:10]]


def appendData():
    data = getData()
    # get tfis and dfis and top 10s
    # reformat ar assigned list
    


