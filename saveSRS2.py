import os

import numpy as np
import pandas as pd

import astropy
import astropy.units as u
from astropy.coordinates import SkyCoord
# from sunpy.data.sample import AIA_193_IMAGE, HMI_LOS_IMAGE

import astropy.time
from astropy.visualization import ImageNormalize, SqrtStretch

import datetime as dt

from getFTP import extractFromTar

months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def extractData(path): # parse the SRS text files for date and SRS data attributes
    with open(path, "r") as fp:
        date = ''
        data = []
        nextline = False
        for line in fp.readlines():
            line = line.rstrip("\n")
            if line[0:8] == ":Issued:":
                date = line[len(line)-20:len(line)-38]
                
            if line[0:3] == "IA.":
                nextline = False
                
            if nextline:
                data.append([word for word in line.split(" ") if word != ""])
            if line[0:4] == "Nmbr" and "Area  Z   LL   NN Mag Type" in line:
                nextline = True
                
    return date, data




# DATA STRUCTURE: [{arnum1: {dates:[], location:[], classification:[] ...}}, {arnum2: {dates:[], location:[], classification:[] ...}} ...]

def convertDate(date): # Convert String to datetime type
    dlist = date.split(' ')
    dlist[1] = months[dlist[1]]
    dlist = [int(d) for d in dlist]
    
    return dt.date(dlist[0], dlist[1], dlist[2])
    
# def sortList(l):
#     return sorted(l, key=lambda x: convertDate(x[8]))

def dictify(ardata): # Append all SRS data for that day to the respective ARNUM
    dictlist = []
    # print(ardata)
    for day in ardata:
        subdict = {}
        if len(day)==8:
            subdict["ARNUM"] = day[0] # add 10000 here
            subdict["DATE"] = day[1]
            subdict["LOCATION"] = day[2]
            subdict["MAG_TYPE"] = day[7]
            subdict["LONGITUDE"] = day[3]
            subdict["AREA"] = day[4]
            subdict["ZURICH_CLASSIFICATION"] = day[5]
            subdict["LONG_EXTENT"] = day[6]
        else:
            subdict["ARNUM"] = day[0] # add 10000 here
            subdict["DATE"] = day[1]
            subdict["LOCATION"] = day[2]
            subdict["MAG_TYPE"] = day[8]
            subdict["LONGITUDE"] = day[3]
            subdict["AREA"] = day[4]
            subdict["ZURICH_CLASSIFICATION"] = day[5]
            subdict["LONG_EXTENT"] = day[6]
            subdict["NUM_SUNSPOTS"] = day[7]
        
        dictlist.append(subdict)
    return dictlist


def saveData(path, finaldata, versionDate):
    import pickle

    # Store data (serialize)
    fn = f'srsdata{versionDate}.pkl'
    # path = "/Users/jhou/Documents/data"
    if not os.path.exists(fn):
        with open(f'{path}/{fn}', 'wb') as handle:
            pickle.dump(finaldata, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("saved")
        
    else:
        print("Not Saved: rename version")

def getData(p):
    years = []
    for i in range(2010, 2022):
        years.append(i)
    
    finallist = []
    # extractFromTar("/Users/jhou/LMSALDataSetupTaskOriginal/testdata", "SRS")
    
    extractFromTar(p, "SRS")
        
    for year in years:
        print(year)
        dates = []
        dataall = []
        arnumraw = []
        arnums = []
        path = f"{p}/ftp_download_SRS/{year}_SRS"#f"/sanhome/jhou/srs-data/{year}_SRS"
        # path = f"{year}_SRS"
        print(path)
        count1125 = 0
        # print(path)
        print(len(os.listdir(path)))
        
        for file in os.listdir(path): # 
            print(file)
            
            date, data = extractData(f"{path}/{file}")
            
            
            count1125+=len([ins[0] for ins in data if ins[0] == "1125"])
            try:
                if data[0][0] != 'None':

                    temparnums = [("1"+num[0]) for num in data] # add 10000 here
                    arnumraw.append(temparnums)

                    for ar in temparnums:
                        temp = []
                        temp.append(ar)
                        temp.append(date)
                        dates.append(temp)
                    [d.insert(1, "1"+d[0]) for d in data]
                    [d.remove(d[0]) for d in data]
                    [d.insert(1,convertDate(date)) for d in data]

                    dataall.append(data)
            except:
                pass
        
        arnumraw = [item for sublist in arnumraw for item in sublist] #flatten ARNUM list

        [arnums.append(x) for x in arnumraw if x not in arnums] # get rid of duplicates
        
        flatteneddata = [item for sublist in dataall for item in sublist] # flatten AR features list
        
        print(len(flatteneddata))
        
        
        
        finaldata = []
        for arnum in arnums:
            templist = []
            for instance in flatteneddata:
                if instance[0] == arnum:
                    templist.append(instance)
            finaldata.append({arnum: templist})
            
        for i in range(len(finaldata)):
            instancedata = finaldata[i][arnums[i]]
            instancedictlist = dictify(instancedata)
            finaldata[i][arnums[i]] = instancedictlist
        finallist.append(finaldata)
    flattenedfinallist = [item for sublist in finallist for item in sublist]
    
    print(flattenedfinallist)
    
    saveData(p, flattenedfinallist, "")

getData("/Users/jhou/LMSALDataSetupTaskOriginal/testdata")




