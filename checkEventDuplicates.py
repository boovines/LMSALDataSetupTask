import os
from webbrowser import get

import numpy as np
import pandas as pd

# import astropy
# import astropy.units as u
# from astropy.coordinates import SkyCoord
# # from sunpy.data.sample import AIA_193_IMAGE, HMI_LOS_IMAGE

# import astropy.time
# from astropy.visualization import ImageNormalize, SqrtStretch

import matplotlib.pyplot as plt


import sunpy.map
# from sunpy.net import Fido
# from sunpy.net import attrs as a

import datetime as dt

import requests
import pickle

def getHist(l):
    import matplotlib.pyplot as plt
    print("in get hist")

    # data = [1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5]

    plt.hist(l, bins=5, edgecolor='black')

    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram')

    plt.show()
def getEvents():
    with open(f'/Users/justinhou/Documents/data/herevs524.csv') as f:
        csvcontent = pd.read_csv(f)#csv.reader(f)
        # rows = []
        # for row in csvcontent:
        #     rows.append(row)
        for index, ev in csvcontent.iterrows():
            csvcontent.at[index,'DATE'] = dt.datetime(int(ev["DATE"][0:4]), int(ev["DATE"][5:7]), int(ev["DATE"][8:]))
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
        centering = 1
    if isARDup(ev1,ev2):
        duptypes.append("AR")
        ar = 1
    return duptypes, peak, cmag, centering, ar

def generatePairs(lst):
    pairs = []
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            pairs.append([lst[i], lst[j]])
    return pairs


def detectDups():
    evlist = getEvents()
    # count = 0
    alldups = []
    classdupcount = 0
    ardupcount = 0
    centeringdupcount = 0
    peakdupcount = 0
    exactdup = 0
    atleast1 = 0
    NSdif = []
    WEdif = []
    edict = evlist.to_dict('records')
    print(edict[:5])

    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime.today()-dt.timedelta(days=1)#(2023, 1, 10)

    current_date = start_date
    num = 0
    denom = 0
    while current_date <= end_date:
        # evdups = []
        today = current_date #- dt.timedelta(days=1)
        tomorrow = current_date + dt.timedelta(days=1)
        evsInRange = evlist.loc[evlist["DATE"].between(today,tomorrow)]
        inRangeDict = evsInRange.to_dict('records')
        pairs = generatePairs(inRangeDict)
        denom+=len(pairs)
        for pair in pairs:
            ev=pair[0]
            ev2=pair[1]
            inside1 = int(ev["PEAK"])>int(ev2["START"]) and int(ev["PEAK"])<int(ev2["END"])
            inside2 = int(ev2["PEAK"])>int(ev["START"]) and int(ev2["PEAK"])<int(ev["END"])
            # print(inside1)
            
            if inside1: num+=1
            # else: denom+=1
            # inside2 = ev2["PEAK"]>ev["START"] and ev2["PEAK"]<ev["END"]
            if inside1 or inside2:
                duptypes, peak, cmag, centering, ar = getDupType(ev,ev2)
                alldups.append([pair, duptypes])
                peakdupcount += peak
                centeringdupcount += centering
                ardupcount += ar
                classdupcount += cmag
                if ev==ev2: exactdup+=1 
                atleast1 += 1
                loctype = "LOCATION_HER"
                if type(ev[loctype])==type("hi") and type(ev2[loctype])==type("hi"):
                    NS1 = int(ev[loctype][1:3]) if ev[loctype][0] == "N" else -int(ev[loctype][1:3])
                    WE1 = int(ev[loctype][5:]) if ev[loctype][3] == "W" else -int(ev[loctype][5:])
                    NS2 = int(ev2[loctype][1:3]) if ev2[loctype][0] == "N" else -int(ev2[loctype][1:3])
                    WE2 = int(ev2[loctype][5:]) if ev2[loctype][3] == "W" else -int(ev2[loctype][5:])
                    NSdif.append(abs(NS1-NS2))
                    WEdif.append(abs(WE1-WE2))
                print("class dups:", classdupcount/atleast1*100)
                print("center dups:", centeringdupcount/atleast1*100)
                print("ar dups:",ardupcount/atleast1*100)
                print("peak dups:",peakdupcount/atleast1*100)
                # print((atleast1)/(i+1))
                print("percent dups", num/denom*100)
        
        
        current_date += dt.timedelta(days=1)

    # for i in range(len(edict)):
    #     evdups = []
    #     #print(df.loc[i, "Fee"], df.loc[i, "Courses"])
    #     # print(edict)
    #     ev = edict[i]
        
    #     # ev2 = edict[i+1]
    #     date = ev["DATE"]
    #     count = 0
    #     today = date #- dt.timedelta(days=1)
    #     tomorrow = date + dt.timedelta(days=2)
    #     evsInRange = evlist.loc[evlist["DATE"].between(today,tomorrow)]
    #     inRangeDict = evsInRange.to_dict('records')
    #     num = 1
    #     denom = 1
    #     for j in range(len(inRangeDict)):
    #         ev2 = inRangeDict[j]
    #         # print(type(int(ev["PEAK"])),ev2["START"], ev2["END"])
    #         # print(int(ev["PEAK"])>int(ev2["START"]), int(ev["PEAK"]), int(ev2["START"]))
    #         # print(int(ev["PEAK"])>int(ev2["START"]), int(ev["PEAK"]), int(ev2["START"]))
    #         inside1 = int(ev["PEAK"])>int(ev2["START"]) and int(ev["PEAK"])<int(ev2["END"])
    #         inside2 = int(ev2["PEAK"])>int(ev["START"]) and int(ev2["PEAK"])<int(ev["END"])
    #         # print(inside1)
            
    #         if inside1: num+=1
    #         else: denom+=1
    #         # inside2 = ev2["PEAK"]>ev["START"] and ev2["PEAK"]<ev["END"]
    #         if inside1:# or inside2:
    #             duptypes, peak, cmag, centering, ar = getDupType(ev,ev2)
    #             evdups.append(duptypes)
    #             peakdupcount += peak
    #             centeringdupcount += centering
    #             ardupcount += ar
    #             classdupcount += cmag
    #             if ev==ev2: exactdup+=1 
    #             atleast1 += 1
    #             loctype = "LOCATION_HER"
    #             NS1 = int(ev[loctype][1:3]) if ev[loctype][0] == "N" else -int(ev[loctype][1:3])
    #             WE1 = int(ev[loctype][5:]) if ev[loctype][3] == "W" else -int(ev[loctype][5:])
    #             NS2 = int(ev2[loctype][1:3]) if ev2[loctype][0] == "N" else -int(ev2[loctype][1:3])
    #             WE2 = int(ev2[loctype][5:]) if ev2[loctype][3] == "W" else -int(ev2[loctype][5:])
    #             NSdif.append(abs(NS1-NS2))
    #             WEdif.append(abs(WE1-WE2))
    #             print(i)
    #             print(classdupcount/atleast1*100)
    #             print(centeringdupcount/atleast1*100)
    #             print(ardupcount/atleast1*100)
    #             print(peakdupcount/atleast1*100)
    #             # print((atleast1)/(i+1))
    #             print(atleast1/len(edict))
    #         print("dup rate:", num/denom)
                
    #     alldups.append([i, evdups])
    print(alldups)
    print(num/denom)
    print("Class/Mag Related Duplicates:", classdupcount, " ", classdupcount/atleast1*100, "%")
    print("Centering Related Duplicates:", centeringdupcount, " ", centeringdupcount/atleast1*100, "%")
    print("AR Related Duplicates:", ardupcount, " ", ardupcount/atleast1*100, "%")
    print("Peak Time Related Duplicates:", peakdupcount, " ", peakdupcount/atleast1*100, "%")
    getHist(NSdif)
    getHist(WEdif)
    with open("duplicateStats.pkl") as fh:
        pickle.dump({
            "allDuplicatePairs": alldups, 
            "cmagDups": [classdupcount, classdupcount/atleast1*100],
            "centeringDups": [classdupcount, classdupcount/atleast1*100],
            "ARDups": [ardupcount, ardupcount/atleast1*100],
            "peakDups": [peakdupcount, peakdupcount/atleast1*100]
            })
    # for i in range(len(edict)-1):
    #     # evdups = []
    #     #print(df.loc[i, "Fee"], df.loc[i, "Courses"])
    #     # print(edict)
    #     ev = edict[i]
        
    #     ev2 = edict[i+1]
    #     # date = ev["DATE"]
    #     count = 0
    #     # today = date #- dt.timedelta(days=1)
    #     # tomorrow = date + dt.timedelta(days=2)
    #     # evsInRange = evlist.loc[evlist["DATE"].between(str(today),str(tomorrow))]
    #     # for index2, ev2 in evsInRange.iterrows():
    #     # print(type(int(ev["PEAK"])),ev2["START"], ev2["END"])
    #     # print(int(ev["PEAK"])>int(ev2["START"]), int(ev["PEAK"]), int(ev2["START"]))
    #     # print(int(ev["PEAK"])>int(ev2["START"]), int(ev["PEAK"]), int(ev2["START"]))
    #     inside1 = int(ev["PEAK"])>int(ev2["START"]) and int(ev["PEAK"])<int(ev2["END"])
    #     # inside2 = int(ev2["PEAK"])>int(ev["START"]) and int(ev2["PEAK"])<int(ev["END"])
    #     print(inside1)
    #     # inside2 = ev2["PEAK"]>ev["START"] and ev2["PEAK"]<ev["END"]
    #     if inside1 or inside2:
    #         print("in if")
    #         duptypes, peak, cmag, centering, ar = getDupType(ev,ev2)
    #         # evdups.append(duptypes)
    #         peakdupcount += peak
    #         centeringdupcount += centering
    #         ardupcount += ar
    #         classdupcount += cmag
    #         atleast1 += 1
    #         alldups.append([i, duptypes])
    #     print(alldups)
    #     print("Class/Mag Related Duplicates:", classdupcount, " ", classdupcount/atleast1*100, "%")
    #     print("Centering Related Duplicates:", centeringdupcount, " ", centeringdupcount/atleast1*100, "%")
    #     print("AR Related Duplicates:", ardupcount, " ", ardupcount/atleast1*100, "%")
    #     print("Peak Time Related Duplicates:", peakdupcount, " ", peakdupcount/atleast1*100, "%")
    
    
    
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
detectDups()