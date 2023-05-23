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



# directory = f'/sanhome/jhou/{reportName}/goes_xray_event_list_{year}.txt'
months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

# directory = f'/sanhome/jhou/{reportName}/goes_xray_event_list_{year}.txt'


def parseEventData(directory, skippedLines): # parse text file
    count = skippedLines
    # if (reportName == ")
    with open(directory) as fp3:
        data = []
        for line in fp3.readlines():
            if count <= 0:
                line = line.rstrip("\n")
                data.append([word for word in line.split(" ") if word != ""])

            else:
                count -= 1
        # print(data)
        return data
        
        

def getEventData(reportType, year, file=''):
    if file != '':
        skippedLines = 6 #if ('goes-xrs-reports' == reportType or 'goes-xrs-reports-HER' in reportType) else 0
        # print(file)
        directory = f'{reportType}/{file}'
        data = parseEventData(directory, skippedLines)
        
    else:
        if 'goes-xrs-reports' == reportType:
            skippedLines = 6
            directory = f'/sanhome/jhou/{reportType}/goes_xray_event_list_{year}.txt'
            data = parseEventData(directory, skippedLines)
        elif 'goes-xrs-reports-HER' in reportType:
            skippedLines = 6
            directory = f'/sanhome/jhou/{reportType}/goes_xray_event_list_{year}_HER.txt'
            data = parseEventData(directory, skippedLines)
        else:
            skippedLines = 0
            if year == '2017':
                directory = f'/sanhome/jhou/{reportType}/goes-xrs-report_{year}-ytd.txt'
                data = parseEventData(directory, skippedLines)
            elif year == '2015':
                directory = f'/sanhome/jhou/{reportType}/goes-xrs-report_{year}_modifiedreplacedmissingrows.txt'
                data = parseEventData(directory, skippedLines)
            else:
                directory = f'/sanhome/jhou/{reportType}/goes-xrs-report_{year}.txt'
                data = parseEventData(directory, skippedLines)
    return data

def convertDatev2(date):
    # tempyr = date[5:7]
    times = date.split("-")
    year = int(times[2])
    month = int(months[times[1]])
    day = int(times[0])
    return dt.date(year, month, day)


def organizeDatav2(listtype, data): # organize data downloaded from Kim's email
    newdata = []
    for record in data:
        event = {}
        event["DATE"] = convertDatev2(record[0])
        event["START"] = record[1][0:2]+record[1][3:5]
        event["PEAK"] = record[2][0:2]+record[2][3:5]
        event["END"] = record[3][0:2]+record[3][3:5]
        # if listtype == 'goes-xrs-reports':
        #     event["MAGNITUDE_NOAA"] = record[4]
        # else:
        #     event["MAGNITUDE_HER"] = record[4]
        
        if(len(record) == 5):
            # event["LOCATION"] = ""
            event["ARNUMBER"] = ""
        elif(len(record) == 6):
            if(record[5].isnumeric()):
                # event["LOCATION"] = ""
                event["ARNUMBER"] = record[5]
            else:
                # event["LOCATION"] = record[5]
                event["ARNUMBER"] = ""
        elif(len(record) == 7):
            # event["LOCATION"] = record[5]
            event["ARNUMBER"] = record[6]
        else:
            pass
        
        if listtype == 'goes-xrs-reports':
            if(len(record) == 5):
                event["LOCATION_NOAA"] = ""
            elif(len(record) == 6):
                if(record[5].isnumeric()):
                    event["LOCATION_NOAA"] = ""
                else:
                    event["LOCATION_NOAA"] = record[5]
            elif(len(record) == 7):
                event["LOCATION_NOAA"] = record[5]
            else:
                pass
            event["MAGNITUDE_NOAA"] = record[4]
        else:
            if(len(record) == 5):
                event["LOCATION_HER"] = ""
            elif(len(record) == 6):
                if(record[5].isnumeric()):
                    event["LOCATION_HER"] = ""
                else:
                    event["LOCATION_HER"] = record[5]
            elif(len(record) == 7):
                event["LOCATION_HER"] = record[5]
            else:
                pass
            event["MAGNITUDE_HER"] = record[4]
        
        newdata.append(event)
    return newdata

def flatten(l):
    return l

def mergeLists(list1, list2): # for each item in list 1, compare the DATE and the PEAK time to that in list 2      if there is match, compare items in each list, add a new column in df for new mag if it exists
    newlist = []
    uniquelist = []
    print(len(list2) + len(list2))
    for event1 in list1:
        match = False
        for event2 in list2:
            # print(event1)
            # print(event2["MAGNITUDE_HER"][1:])
            
            # print("Hi", event1)
            # print("hi", event2)
            # print(event2["MAGNITUDE_HER"])
            # print(event2["MAGNITUDE_HER"][0])
            # print("hola", type(event2["MAGNITUDE_HER"][0]),event2["MAGNITUDE_HER"][0])
            
            mag1 = float(event1["MAGNITUDE_NOAA"][1:]) if event1["MAGNITUDE_NOAA"] != "" else 2100
            class1 = event1["MAGNITUDE_NOAA"][0] if event1["MAGNITUDE_NOAA"] != "" else 100 # maybe this is wrong? "MAGNITUDE"
            
            mag2 = float(event2["MAGNITUDE_HER"][1:]) if event2["MAGNITUDE_HER"] != "" else 2100
            class2 = event2["MAGNITUDE_HER"][0] if event2["MAGNITUDE_HER"] != "" else 2100 # maybe this is wrong?
            if(event1["DATE"] == event2["DATE"] and event1["PEAK"] == event2["PEAK"] and class1==class2 and abs(mag1-mag2)<0.2):
                match = True
                newevent = event1
#                 # magnitudes = []
#                 if(event1["MAGNITUDE_NOAA"] == event2["MAGNITUDE_HER"]): #1
                  
#                     # magnitudes.append(event2["MAGNITUDE"])
                newevent["LOCATION_HER"] = event2["LOCATION_HER"]
                newevent["LOCATION_NOAA"] = event1["LOCATION_NOAA"]
                newevent["MAGNITUDE_HER"] = event2["MAGNITUDE_HER"]
                newevent["MAGNITUDE_NOAA"] = event1["MAGNITUDE_NOAA"] # also remove newevent["LOCATION/MAGNITUDE"]
                
                # print(event1["LOCATION_NOAA"], event1["MAGNITUDE_NOAA"])
                # print(event2["LOCATION_HER"], event2["MAGNITUDE_HER"])
                # print(newevent)
                # print("type1")
                # print(event1)
                # print(event2)
                # print(magnitudes)
                newlist.append(newevent)
                break
                # else: #2
                #     magnitudes.append(event1["MAGNITUDE"])
                #     magnitudes.append(event2["MAGNITUDE"])
                #     # flatmag = flatten(magnitudes) # WRITE THIS FUNCTION
                #     # print("type2")
                #     # print(event1)
                #     # print(event2)
                #     # print(magnitudes)
                #     newevent["MAGNITUDE"] = magnitudes
                #     newlist.append(newevent)
                #     break
        if not match:
            # print("type3")
            # print(event2)
            newevent = event2
            # magnitudes1 = []
            # magnitudes1.append(event2["MAGNITUDE"])
            newevent["MAGNITUDE_NOAA"] = event1["MAGNITUDE_NOAA"] # SAME POTENTIAL ERROR HERE?
            newevent["MAGNITUDE_HER"] = ""
            newevent["LOCATION_NOAA"] = event1["LOCATION_NOAA"]
            newevent["LOCATION_HER"] = ""
            newlist.append(newevent) #3
            
    for event2 in list2:
        match2 = False
        # print(event1)
        for event1 in list1:
            mag1 = float(event1["MAGNITUDE_NOAA"][1:]) if event1["MAGNITUDE_NOAA"] != "" else 2100
            class1 = event1["MAGNITUDE_NOAA"][0] if event1["MAGNITUDE_NOAA"] != "" else 100 # maybe this is wrong? "MAGNITUDE"
            
            mag2 = float(event2["MAGNITUDE_HER"][1:]) if event2["MAGNITUDE_HER"] != "" else 2100
            class2 = event2["MAGNITUDE_HER"][0] if event2["MAGNITUDE_HER"] != "" else 2100 # maybe this is wrong?
            
            if(event1["DATE"] == event2["DATE"] and event1["PEAK"] == event2["PEAK"] and abs(mag1-mag2)<0.2):
                match2 = True
                break
        if not match2:
            # print("type4")
            # print(event1)
            
            newevent = event2
            # magnitudes1 = []
            # magnitudes1.append(event1["MAGNITUDE_NOAA"])
            newevent["MAGNITUDE_HER"] = event2["MAGNITUDE_HER"]
            newevent["MAGNITUDE_NOAA"] = ""
            newlist.append(newevent) #4
    return newlist

def getDFs(evlist):
    dfs = []
    for ev in evlist:
        dfs.append(pd.DataFrame(ev, index = [0]))
    return pd.concat(dfs)
def sortList(l):
    return sorted(l, key=lambda x: x['DATE'])
def makeFinalList(splitByYear=False, year=''):
    if splitByYear:
        # temp1 = getEventData('old-goes-xrs-reports', str(year))
        temp2 = getEventData('goes-xrs-reports', str(year))
        temp3 = getEventData('goes-xrs-reports-HER', str(year))
        
        # report1 = organizeDatav1(temp1)
        report2 = organizeDatav2('goes-xrs-reports', temp2)
        report3 = organizeDatav2('goes-xrs-reports-HER', temp3)
        
        twolistsmerged = mergeLists(report2, report3)
        
        # newlist = mergeLists(twolistsmerged, report3)
        return report2, report3, twolistsmerged #newlist
        
    else:
        reportTypes = ['goes-xrs-reports', 'goes-xrs-reports-HER']#['old-goes-xrs-reports', 'goes-xrs-reports', 'goes-xrs-reports-HER']
        reports = []
        for i in range(len(reportTypes)):
            path = f"/sanhome/jhou/{reportTypes[i]}"
            report = []
            files = [item for item in os.listdir(path) if item[0:2]!="._"]
            for file in files:
                # print([item for item in os.listdir(path) if item[0:2]!="._"])
                temp1 = getEventData(path, str(year), file)
                temp2 = organizeDatav2(reportTypes[i], temp1)#organizeDatav1(temp1) if (i==0) else organizeData2(temp1)
                
                    
                report.append(temp2)
            reports.append(report)
        
        noaa = [item for years in reports[0] for item in years]
        her = [item for years in reports[1] for item in years]
        print(noaa)
        print(len(noaa), len(her))
        
        snoaa = sortList(noaa)
        noaaDF = getDFs(snoaa)
        noaaDF.to_csv("noaaevs.csv")
        
        sher = sortList(her)
        herDF = getDFs(sher)
        herDF.to_csv("herevs.csv")
        twolistsmerged = mergeLists(noaa, her)
        
        # newlist = mergeLists(twolistsmerged, reports[2])
        smerged = sortList(twolistsmerged)
        mergedDF = getDFs(smerged)

        # noaaDF.to_csv("noaaevs0519.csv")
        # herDF.to_csv("herevs0519.csv")
        mergedDF.to_csv("mergedevs.csv")
        
        return noaa, her, twolistsmerged #newlist
        
noaa, her, merged = makeFinalList()  
# print(merged)

# noaaline1 = pd.DataFrame(noaa[0])
# herline1 = pd.DataFrame(her[0])
# mergedline1 = pd.DataFrame(merged[0])


    
    # if len(evlist) == 0:
    #     return df
    # else:
    #     df2 = pd.DataFrame(evlist[0], index=[0])
    #     df3 = pd.concat([df, df2])
    #     return getDFs(df3, evlist[1:])

# emptyDF = pd.DataFrame({'DATE': date.today(), 'START': '', 'PEAK': '', 'END': '', 'MAGNITUDE': [], 'LOCATION': '', 'ARNUMBER': ''})

    
# noaaDF = getDFs(noaa)
# herDF = getDFs(her)

