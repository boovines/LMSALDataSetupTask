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

# import sunpy
# import sunpy.map
# from sunpy.net import Fido
# from sunpy.net import attrs as a

import datetime as dt

from getFTP import getFTPtar
from sunpy.net import Fido
from sunpy.net import attrs as a
# import getCMEdata
# directory = "/Users/justinhou/Documents/data"

def getHEK(directory):
    event_type = "FL"
    tstart = "2013/10/28"
    tend = "2013/10/29"
    result = Fido.search(a.Time(tstart, tend),
                        a.hek.EventType(event_type),
                        # a.hek.FL.GOESCls > "M1.0",
                        a.hek.OBS.Observatory == "GOES")
    new_table = hek_results["event_starttime", "event_peaktime",
                        "event_endtime", "fl_goescls", "ar_noaanum"]
    new_table.write("october_M1_flares.csv", format="csv")


def getAll(directory):
    getFTPtar(2022, "SRS", directory) # write code to replace existing file if not downloaded within the same day prior

    # getFTPtar(2022, "events", directory)

    # getHEK(directory)
    # getCMEdata.getData()



