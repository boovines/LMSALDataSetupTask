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

# from ftplib import FTP
# import tarfile

# ftp = FTP('ftp.swpc.noaa.gov')
# ftp.login()
# ftp.cwd('pub/warehouse/1996')

# print(ftp.nlst())

# with open('./test.tar.gz', 'wb') as fp:
#     ftp.retrbinary("RETR" + '2017_SRS.tar.gz', fp.write)
    
# with tarfile.open('./test.tar.gz') as fp:
#     fp.extractall('./')

months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def extractData(path):
    # return path
    with open(path, "r") as fp:
        date = ''
        data = []
        nextline = False
        for line in fp.readlines():
            line = line.rstrip("\n")
            if line[0:8] == ":Issued:":
                date = line[len(line)-20:len(line)-38]
                # print(date.split(" "))

                # print(line[0:10])
            if line[0:3] == "IA.":
                nextline = False
                # break
            if nextline:
                # print(line)
                data.append([word for word in line.split(" ") if word != ""])
            if line[0:4] == "Nmbr" and "Area  Z   LL   NN Mag Type" in line:
                nextline = True
                
    # print(data)
    return date, data
            
# print(fp)
# txt = fp.read()

# fp.close()
# print(txt)

years = []
for i in range(2010, 2022):
    years.append(i)

#[{arnum1: {dates:[], location:[], classification:[] ...}}, {arnum2: {dates:[], location:[], classification:[] ...}} ...]

def convertDate(date):
    dlist = date.split(' ')
    dlist[1] = months[dlist[1]]
    dlist = [int(d) for d in dlist]
    
    return dt.date(dlist[0], dlist[1], dlist[2])
    
def sortList(l):
    return sorted(l, key=lambda x: convertDate(x[8]))
    
def getData():
    # dates = []
    # dataall = []
    # arnumraw = []
    # arnums = []
    
    finallist = []
    finallist2 = []
    for year in years:
        dates = []
        dataall = []
        arnumraw = []
        arnums = []
        path = f"/sanhome/jhou/srs-data/{year}_SRS"
        count1125 = 0
        for file in os.listdir(path):
            # print(f"{path}/{file}")
            date, data = extractData(f"{path}/{file}")
            # print()
            count1125+=len([ins[0] for ins in data if ins[0] == "1125"])
            try:
                if data[0][0] != 'None':

                    temparnums = [num[0] for num in data]
                    arnumraw.append(temparnums)

                    # newdate = convertDate(date)


                    for ar in temparnums:
                        temp = []
                        temp.append(ar)
                        temp.append(date)
                        dates.append(temp)

                    dataall.append(data)
            except:
                print("exception", date)
        
        print(count1125)
        arnumraw = [item for sublist in arnumraw for item in sublist]
        # print(dates)
        [arnums.append(x) for x in arnumraw if x not in arnums]
        # print(arnums)
        # print(dataall)

        for arnum in arnums:
            ardict = {}
            
            arnumdata = [a for day in dataall for a in day if a[0] == arnum]
            # print(dates)
            reordereddates = [date[1] for date in dates if date[0] == arnum]
            # print(reordereddates)
            for i in range(len(reordereddates)):
                # arnumdata[i].pop(0)
                arnumdata[i].append(reordereddates[i])
            
            arnumdata = [instance for instance in arnumdata if len(instance)==9]
            # print(arnumdata)
            arnumdata = sortList(arnumdata)
            # print(arnumdata, "LJDLKJSLFJSDL")
            for instance in arnumdata:
                if len(instance) == 9:
                    # print(instance, "dklfhlaksdhflajhdsflk")
                    subdict = {}
                    subdict["ARNUM"] = arnum
                    subdict["DATE"] = instance[8]
                    subdict["LOCATION"] = instance[1]
                    subdict["MAG_TYPE"] = instance[7]
                    subdict["LONGITUDE"] = instance[2]
                    subdict["AREA"] = instance[3]
                    subdict["ZURICH_CLASSIFICATION"] = instance[4]
                    subdict["LONG_EXTENT"] = instance[5]
                    subdict["NUM_SUNSPOTS"] = instance[6]
                    # print(subdict)
                    finallist2.append(subdict)
                    # print(finallist2)
            ardict[arnum] = subdict
            # print(finallist2)


            # for arnumdata 
            # ardict[arnum] = arnumdata
            finallist.append(ardict)
            # print(arnumdata)

        # print(finallist) 
    # print(data)
    # print(finallist2)
    return date, finallist, finallist2
date, data2, data3 = getData()
# print(h)
import json

# with open('srs-data-by-AR.json', 'w') as f:
#     json.dump(data2, f)
    
with open('srs-data-test.json', 'w') as f:
    json.dump(data3, f)
    
    
  
            
            
#             ardict = {}
            
#             arnumdata = [a for day in dataall for a in day if a[0] == arnum]
#             # print(dates)
#             reordereddates = [date[1] for date in dates if date[0] == arnum]
#             # print(reordereddates)
#             for i in range(len(reordereddates)):
#                 # arnumdata[i].pop(0)
#                 arnumdata[i].append(reordereddates[i])
            
#             arnumdata = [instance for instance in arnumdata if len(instance)==9]
#             # print(arnumdata)
#             arnumdata = sortList(arnumdata)
#             # print(arnumdata, "LJDLKJSLFJSDL")
#             for instance in arnumdata:
#                 if len(instance) == 9:
#                     # print(instance, "dklfhlaksdhflajhdsflk")
                    # subdict = {}
                    # subdict["ARNUM"] = arnum
                    # subdict["DATE"] = instance[8]
                    # subdict["LOCATION"] = instance[1]
                    # subdict["MAG_TYPE"] = instance[7]
                    # subdict["LONGITUDE"] = instance[2]
                    # subdict["AREA"] = instance[3]
                    # subdict["ZURICH_CLASSIFICATION"] = instance[4]
                    # subdict["LONG_EXTENT"] = instance[5]
                    # subdict["NUM_SUNSPOTS"] = instance[6]
#                     # print(subdict)
#                     finallist2.append(subdict)
#                     # print(finallist2)
#             ardict[arnum] = subdict
#             # print(finallist2)


#             # for arnumdata 
#             # ardict[arnum] = arnumdata
#             finallist.append(ardict)
#             # print(arnumdata)

        # print(finallist) 
    # print(data)
    # print(finallist2)
    # return date, finallist, finallist2