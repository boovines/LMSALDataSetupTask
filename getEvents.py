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

# directory = f'/sanhome/jhou/{reportName}/goes_xray_event_list_{year}.txt'
months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

# directory = f'/sanhome/jhou/{reportName}/goes_xray_event_list_{year}.txt'


def parseEventData(directory, skippedLines): # parse text file
    # print(directory)
    count = skippedLines
    
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
        
def getEventData(p, reportType, startyear=2010, endyear = dt.date.today().year):
    if 'goes-xrs-reports-HER' in reportType:
        root = f"https://hesperia.gsfc.nasa.gov/goes/goes_event_listings_HER"
    else:
        root = f"https://hesperia.gsfc.nasa.gov/goes/goes_event_listings"
    
    if not os.path.exists(f"{p}/{reportType}"):
        os.mkdir(f"{p}/{reportType}")
        

        for i in range(startyear, endyear+1):
            url = f"{root}/goes_xray_event_list_{i}.txt" 
            r = requests.get(url, allow_redirects=True)

            open(f"{p}/{reportType}/goes_xray_event_list_{i}.txt", 'wb').write(r.content)
    elif os.path.exists(f"{p}/{reportType}") and endyear == dt.date.today().year:
        # try:
        os.remove(f"{p}/{reportType}/goes_xray_event_list_{dt.date.today().year}.txt")
        url = f"{root}/goes_xray_event_list_{dt.date.today().year}.txt" 
        r = requests.get(url, allow_redirects=True)

        open(f"{p}/{reportType}/goes_xray_event_list_{dt.date.today().year}.txt", 'wb').write(r.content)
        # except:
        #     pass
    else:
        pass
    


    
def extractEventData(p, reportType, year, file, sanhome=False):
    if not sanhome: #file != '':
        skippedLines = 6 #if ('goes-xrs-reports' == reportType or 'goes-xrs-reports-HER' in reportType) else 0
        # print(file)
        directory = f'{p}/{reportType}/{file}'
        
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
    return dt.datetime(year, month, day)


def organizeDatav2(listtype, data): # organize data downloaded from Kim's email
    newdata = []
    for record in data:
        event = {}
        date = convertDatev2(record[0])
        event["DATE"] = date
        event["START"] = dt.datetime(date.year, date.month, date.day, int(record[1][0:2]), int(record[1][3:5]))
        event["PEAK"] = dt.datetime(date.year, date.month, date.day, int(record[2][0:2]), int(record[2][3:5]))#record[2][0:2]+record[2][3:5]
        event["END"] = dt.datetime(date.year, date.month, date.day, int(record[3][0:2]), int(record[3][3:5]))#record[3][0:2]+record[3][3:5]
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
                event["ARNUMBER"] = int(record[5])
            else:
                # event["LOCATION"] = record[5]
                event["ARNUMBER"] = ""
        elif(len(record) == 7):
            # event["LOCATION"] = record[5]
            event["ARNUMBER"] = int(record[6])
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
        # if list2
        for event2 in list2:
            # print(event1)
            # print(event2["MAGNITUDE_HER"][1:])
            
            # print("Hi", event1)
            # print("hi", event2)
            # print(event2["MAGNITUDE_HER"])
            # print(event2["MAGNITUDE_HER"][0])
            # print("hola", type(event2["MAGNITUDE_HER"][0]),event2["MAGNITUDE_HER"][0])
            
            # print(type(event1["DATE"]), event2["DATE"])
            
            mag1 = float(event1["MAGNITUDE_NOAA"][1:]) if event1["MAGNITUDE_NOAA"] != "" else 2100
            class1 = event1["MAGNITUDE_NOAA"][0] if event1["MAGNITUDE_NOAA"] != "" else 100 # maybe this is wrong? "MAGNITUDE"
            
            mag2 = float(event2["MAGNITUDE_HER"][1:]) if event2["MAGNITUDE_HER"] != "" else 2100
            class2 = event2["MAGNITUDE_HER"][0] if event2["MAGNITUDE_HER"] != "" else 2100 # maybe this is wrong?
            if(event1["DATE"] == event2["DATE"] and event1["PEAK"] == event2["PEAK"] and class1==class2 and abs(mag1-mag2)<=0.2):
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
            newevent = event1   
            # print(newevent)
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
            
            if(event1["DATE"] == event2["DATE"] and event1["PEAK"] == event2["PEAK"] and abs(mag1-mag2)<=0.2):
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
            newevent["LOCATION_NOAA"] = ""
            newlist.append(newevent) #4
    return newlist

def getDFs(evlist):
    dfs = []
    for ev in evlist:
        dfs.append(pd.DataFrame(ev, index = [0]))
    DF = pd.concat(dfs)
    
    return DF.loc[:,~DF.columns.str.match("Unnamed")]


def sortList(l):
    return sorted(l, key=lambda x: x['PEAK'])

def notSameDay(p, fn):
    if os.path.exists(f"{p}/{fn}"):
        return not dt.datetime.fromtimestamp(os.path.getmtime(f"{p}/{fn}")).replace(hour =0, minute=0,second=0,microsecond=0) == dt.datetime.now().replace(hour =0, minute=0,second=0,microsecond=0)
    else:
        return False



def makeFinalList(p, splitByYear=False, year=''):
    
    
    if splitByYear:
        # temp1 = extractEventData('old-goes-xrs-reports', str(year))
        temp2 = extractEventData('goes-xrs-reports', str(year))
        temp3 = extractEventData('goes-xrs-reports-HER', str(year))
        
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
            path = f"{p}/{reportTypes[i]}" #f"/sanhome/jhou/{reportTypes[i]}"
            getEventData(p, reportTypes[i])
            report = []
            files = [item for item in os.listdir(path) if item[0:2]!="._"]
            # print(files[len(files)-1:])
            print(files)
            # files = [item for item in files if not "2023" in item]
            # print(files)
            for file in files:#[:len(files)-1]:
                # print([item for item in os.listdir(path) if item[0:2]!="._"])
                if not ".ipynb_checkpoints" in file:
                    temp1 = extractEventData(p, reportTypes[i], str(year), file)
                    temp2 = organizeDatav2(reportTypes[i], temp1)#organizeDatav1(temp1) if (i==0) else organizeData2(temp1)


                    report.append(temp2)
            reports.append(report)
        
        noaa = [item for years in reports[0] for item in years]
        her = [item for years in reports[1] for item in years]
        # print(noaa)
        print(len(noaa), len(her))
        
        snoaa = sortList(noaa)
        noaaDF = getDFs(snoaa)
        
        
        sher = sortList(her)
        herDF = getDFs(sher)
        
        print(snoaa[0], sher[0])
        
        f1 = f"{p}/noaaevs.csv"
        f2 = f"{p}/herevs.csv"
        # print(noaa)
        if os.path.exists(f1) and os.path.exists(f2): # TEST THIS PARTTTTTTTTT
            if notSameDay(p, "mergedevs.csv"):
                print("entered test part")
                with open(f1, "rb") as f:
                    oldnoaaevs = pd.read_csv(f)
                    oldnoaalen = len(oldnoaaevs.index)
                unmergednoaa = snoaa[oldnoaalen:]

                with open(f2, "rb") as f:
                    oldherevs = pd.read_csv(f)
                    oldherlen = len(oldherevs.index)
                unmergedher = sher[oldherlen:]

                # print(unmergednoaa, unmergedher)

                # print(snoaa, noaaDF)



                mergedend = mergeLists(unmergednoaa, unmergedher)

                # print(mergedend)
                # print(oldnoaaevs[-1:])

                with open(f'{p}/mergedevs.csv', "rb") as f:
                    oldmergedevs = pd.read_csv(f)
                    twolistsmerged = oldmergedevs.to_dict("records")
                    [entry.pop('Unnamed: 0') for entry in twolistsmerged]
                    for i in range(len(twolistsmerged)):
                        twolistsmerged[i]["DATE"] = dt.datetime.strptime(twolistsmerged[i]["DATE"], "%Y-%m-%d")
                        print(type(twolistsmerged[i]["DATE"]))
                    # print(twolistsmerged[:3], "hihihihihihihih")
                # oldmergeddict.append(mergedend)
                # print(oldmergeddict)
                for event in mergedend:
                    twolistsmerged.append(event)
                # twolistsmerged = [item for sublist in oldmergeddict for item in sublist]
                # print(twolistsmerged, "hi here2")

                # print(len(twolistsmerged))

                for ev in twolistsmerged:
                    # print(ev)
                    if type(ev["DATE"]) == type(dt.datetime(2010,1,1,0,0)):
                        pass
                    else:
                        print(ev['DATE'])
                # twolistsmerged = [oldmergeddict.append(ev) for ev in mergedend]

                # print(twolistsmerged)



                smerged = sortList(twolistsmerged)
                mergedDF = getDFs(smerged)
                noaaDF.to_csv(f"{p}/noaaevs.csv")#{str(dt.date.today())}
                herDF.to_csv(f"{p}/herevs.csv")#{str(dt.date.today())}
                mergedDF.to_csv(f"{p}/mergedevs.csv")#{str(dt.date.today())}
            else:
                return "","",""
        else:
            noaaDF.to_csv(f"{p}/noaaevs.csv")#{str(dt.date.today())}
            herDF.to_csv(f"{p}/herevs.csv")#{str(dt.date.today())}

            twolistsmerged = mergeLists(snoaa, sher)
            # newlist = mergeLists(twolistsmerged, reports[2])
            smerged = sortList(twolistsmerged)
            mergedDF = getDFs(smerged)

            # noaaDF.to_csv("noaaevs0519.csv")
            # herDF.to_csv("herevs0519.csv")
            mergedDF.to_csv(f"{p}/mergedevs.csv")#{str(dt.date.today())}
        
        return noaa, her, twolistsmerged #newlist
        
# noaa, her, merged = makeFinalList("/Users/jhou/LMSALDataSetupTaskOriginal/testdata619")  
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

