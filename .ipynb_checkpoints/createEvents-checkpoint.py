from sunpy.net import Fido
from sunpy.net import attrs as a
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from astropy.io import fits
import datetime as dt
import os
import pandas as pd

def remTime(d):
    return dt.datetime(d.year, d.month, d.day)

def set_proxy(proxy):
    import os
    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
    os.environ['ftp_proxy'] = proxy
    os.environ['FTP_PROXY'] = proxy
    os.environ['PARFIVE_TOTAL_TIMEOUT'] = '10.0'
    
set_proxy("http://proxy-zsgov.external.lmco.com:80")

def getFido(tstart, tend, obstype, event_type = "FL"):
    set_proxy("http://proxy-zsgov.external.lmco.com:80")
    result = Fido.search(a.Time(tstart, tend),
                         a.hek.EventType(event_type),
                         # a.hek.FL.GOESCls > "M1.0",
                         a.hek.OBS.Observatory == obstype)

    # print(result.show("hpc_bbox", "refs"))
    print("searched")
    hek_results = result["hek"]
    # We only print every 10th key to avoid the output being too long.
    # print(hek_results.colnames[::10])

    filtered_results = hek_results["event_starttime", "event_peaktime",
                                   "event_endtime", "fl_goescls", "ar_noaanum", "hgs_y", "hgs_x", "noposition"] #DATE, START PEAK END CLASS POSITION ACTIVE_REGION
    return filtered_results

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
def sortList(l):
    return sorted(l, key=lambda x: x['PEAK'])

def organizeDatav2(listtype, data): # organize data downloaded from Kim's email
    newdata = []
    for record in data:
        event = {}
        date = dt.datetime.strptime(record[0], "%Y-%m-%d")
        event["DATE"] = date
        event["START"] = dt.datetime(date.year, date.month, date.day, int(record[1][0:2]), int(record[1][3:5]))
        
        peak = dt.datetime(date.year, date.month, date.day, int(record[2][0:2]), int(record[2][3:5])) 
        if int(record[1][0:2]) > int(record[2][0:2]):
            peak += dt.timedelta(days=1)
        event["PEAK"] = peak#record[2][0:2]+record[2][3:5]
        
        end = dt.datetime(date.year, date.month, date.day, int(record[3][0:2]), int(record[3][3:5]))
        if int(record[2][0:2]) > int(record[3][0:2]):
            end += dt.timedelta(days=1)
        # if int(record[2][0:2]) < int(record[3][0:2]) else dt.datetime(date.year, date.month, date.day+1, int(record[2][0:2]), int(record[2][3:5])) 
        event["END"] = end#record[3][0:2]+record[3][3:5]
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

def getDFs(evlist):
    dfs = []
    for ev in evlist:
        dfs.append(pd.DataFrame(ev, index = [0]))
    DF = pd.concat(dfs)
    
    return DF.loc[:,~DF.columns.str.match("Unnamed")]

def makeFinalList(p, folder, year=''):
    report = []
    for year in range(2010, dt.datetime.now().year+1):
        temp1 = parseEventData(f"{p}/event_text_files/{year}_events.txt", 6)
        
        temp2 = organizeDatav2('goes-xrs-reports-her', temp1)#organizeDatav1(temp1) if (i==0) else organizeData2(temp1)


        report.append(temp2)
        # reports.append(report)

    her = [item for years in report for item in years]
    # her = [item for years in reports[1] for item in years]
    # print(noaa)
    print(len(her))

    sher = sortList(her)
    print(sher)
    herDF = getDFs(sher)
    print(herDF)
    herDF.to_csv(f"{p}/{folder}/mergedevs.csv")
# makeFinalList("/Users/jhou/LMSALDataSetupTaskOriginal/testdata623")


def createEvents(path, folder, event_type = "FL"):
    currentyear = dt.datetime.now().year
    if not os.path.exists(f"{path}/event_text_files"):
        os.mkdir(f"{path}/event_text_files")
    for year in range(2010, currentyear+1):
        if not os.path.exists(f"{path}/event_text_files/{year}_events.txt"):
            print("YEAR:", year)
            today = remTime(dt.datetime.now())
            tstart = f"{year}/1/1"
            tend = f"{year}/{remTime(dt.datetime.now()).month}/{remTime(dt.datetime.now()).day}" if year==currentyear else f"{year+1}/1/1"

            filtered_results = getFido(tstart, tend, "GOES")
            other_results = getFido(tstart, tend, "SDO")

            file_content = f"GOES XRAY events for {year} \nWritten {today}, Justin Hou, justinhou2005@gmail.com \n{len(filtered_results)} events were retrieved from the Heliophysics Event Registry (HER) \n\nColumns:Date, Start, Peak, End Time, Class, Position (if available), Active Region (if available) \n"

            # print(str(flare["event_starttime"].hour).zfill(2))
            priorev = "2010-12-29   21:04   21:10   21:15   B4.3   "
            for flare in filtered_results:
                s = dt.datetime.strptime(str(flare["event_starttime"])[:16], "%Y-%m-%d %H:%M")
                p = dt.datetime.strptime(str(flare["event_peaktime"])[:16], "%Y-%m-%d %H:%M")
                e = dt.datetime.strptime(str(flare["event_endtime"])[:16], "%Y-%m-%d %H:%M")

                start = f"{str(s.hour).zfill(2)}:{str(s.minute).zfill(2)}"
                peak = f"{str(p.hour).zfill(2)}:{str(p.minute).zfill(2)}"
                end = f"{str(e.hour).zfill(2)}:{str(e.minute).zfill(2)}"
                date = str(remTime(s))[:10]
                arnum = ""

                priorsplit = [word for word in priorev.split(" ") if word != ""]
                print(priorsplit, date, start, peak, end)
                if priorsplit[0] == date and priorsplit[1] == start and priorsplit[2] == peak and priorsplit[3] == end:
                    print("inskip--------------------------------------------------------------", priorev)
                    continue
                else:

                    if flare["noposition"]=="false":#flare["hgs_x"]!=0.0 and flare["hgs_y"]!=0.0:
                        loc1 = f"   N"+str(int(flare["hgs_y"])).zfill(2) if flare["hgs_y"]>0 else f"   S"+str(-int(flare["hgs_y"])).zfill(2)
                        loc2 = f"W"+str(int(flare["hgs_x"])).zfill(2) if flare["hgs_x"]>0 else f"E"+str(-int(flare["hgs_x"])).zfill(2)
                    else:
                        loc1 = ""
                        loc2 = ""
                        s2s = other_results["event_starttime"]
                        p2s = other_results["event_peaktime"]
                        e2s = other_results["event_endtime"]
                        z = 0
                        for i in range(len(s2s)):
                            s2 = dt.datetime.strptime(str(s2s[i])[:16], "%Y-%m-%d %H:%M")
                            p2 = dt.datetime.strptime(str(p2s[i])[:16], "%Y-%m-%d %H:%M")
                            e2 = dt.datetime.strptime(str(e2s[i])[:16], "%Y-%m-%d %H:%M")
                            if s==s2 and p==p2 and e==e2:
                                z = other_results[i]
                                break
                        if z != 0:
                            loc1 = f"   N"+str(int(z["hgs_y"])).zfill(2) if z["hgs_y"]>0 else f"   S"+str(-int(z["hgs_y"])).zfill(2)
                            loc2 = f"W"+str(int(z["hgs_x"])).zfill(2) if z["hgs_x"]>0 else f"E"+str(-int(z["hgs_x"])).zfill(2)
                            arnum = z["ar_noaanum"] if z["ar_noaanum"]!=0 and type(z["ar_noaanum"])!=type(None) else ""
                            print(loc1, loc2, arnum)
                            if type(arnum) != type("hi"):
                                print("here", arnum, type(arnum))
                                arnum = arnum+10000 if arnum<10000 else arnum

                    mag = flare["fl_goescls"]
                    if type(arnum) == type("hi"):
                        print("inarnum assignment")
                        arnum = flare["ar_noaanum"] if flare["ar_noaanum"]!=0 else ""
                        if type(arnum) != type("hi"):
                            # print("here", arnum)
                            arnum = arnum+10000 if arnum<10000 else arnum
                    print(arnum)
                    newstr = f"{date}   {start}   {peak}   {end}   {mag}{loc1}{loc2}   {arnum}"
                    file_content += f"\n{newstr}"
                    priorev = newstr
                    print(priorev)


            directory = "event_text_files"
            if not os.path.exists(f'{path}/{directory}'):
                os.mkdir(f'{path}/{directory}')
            with open(f'{path}/{directory}/{year}_events.txt', 'w') as f:
                f.write(file_content)
    
    now = dt.datetime.now()
    if dt.datetime.fromtimestamp(os.path.getmtime(f"{path}/event_text_files/{currentyear}_events.txt"))<dt.datetime(now.year, now.month, now.day, now.hour, 0):
        print("in update")
        directory = "event_text_files"
        with open(f'{path}/{directory}/{dt.datetime.now().year}_events.txt', 'r') as f:
            allevents = f.read()
        with open(f'{path}/{directory}/{dt.datetime.now().year}_events.txt', 'r') as f:
            latest = f.readlines()[-1]
        lsplit = [word for word in latest.split(" ") if word != ""]
        latestdate = dt.datetime.strptime(lsplit[0], "%Y-%m-%d")
        tstart = f"{latestdate.year}/{latestdate.month}/{latestdate.day}"
        tend = f"{dt.datetime.now().year}/{remTime(dt.datetime.now()).month}/{remTime(dt.datetime.now()).day}" 

        filtered_results = getFido(tstart, tend, "GOES")
        other_results = getFido(tstart, tend, "SDO")
        
        date = dt.datetime.strptime(lsplit[0], "%Y-%m-%d")
        laststart = dt.datetime(date.year, date.month, date.day, int(lsplit[1][0:2]), int(lsplit[1][3:5]))
        
        lastpeak = dt.datetime(date.year, date.month, date.day, int(lsplit[2][0:2]), int(lsplit[2][3:5])) 
        if int(lsplit[1][0:2]) > int(lsplit[2][0:2]):
            lastpeak += dt.timedelta(days=1)
        
        lastend = dt.datetime(date.year, date.month, date.day, int(lsplit[3][0:2]), int(lsplit[3][3:5]))
        if int(lsplit[2][0:2]) > int(lsplit[3][0:2]):
            lastend += dt.timedelta(days=1)
        
        priorev = "2010-12-29   21:04   21:10   21:15   B4.3   "
        for flare in filtered_results:
            s = dt.datetime.strptime(str(flare["event_starttime"])[:16], "%Y-%m-%d %H:%M")
            p = dt.datetime.strptime(str(flare["event_peaktime"])[:16], "%Y-%m-%d %H:%M")
            e = dt.datetime.strptime(str(flare["event_endtime"])[:16], "%Y-%m-%d %H:%M")
            
            
            start = f"{str(s.hour).zfill(2)}:{str(s.minute).zfill(2)}"
            peak = f"{str(p.hour).zfill(2)}:{str(p.minute).zfill(2)}"
            end = f"{str(e.hour).zfill(2)}:{str(e.minute).zfill(2)}"
            
            

            if s <= laststart and p <= lastpeak and e <= lastend:
                continue
            else:
                

            
                date = str(remTime(s))[:10]
                arnum = ""

                priorsplit = [word for word in priorev.split(" ") if word != ""]
                print(priorsplit, date, start, peak, end)
                # print(priorsplit, date, start, peak, end)
                if priorsplit[0] == date and priorsplit[1] == start and priorsplit[2] == peak and priorsplit[3] == end:
                    print("inskip--------------------------------------------------------------", priorev)
                    continue
                else:

                    if flare["noposition"]=="false":#flare["hgs_x"]!=0.0 and flare["hgs_y"]!=0.0:
                        loc1 = f"   N"+str(int(flare["hgs_y"])).zfill(2) if flare["hgs_y"]>0 else f"   S"+str(-int(flare["hgs_y"])).zfill(2)
                        loc2 = f"W"+str(int(flare["hgs_x"])).zfill(2) if flare["hgs_x"]>0 else f"E"+str(-int(flare["hgs_x"])).zfill(2)
                    else:
                        loc1 = ""
                        loc2 = ""
                        s2s = other_results["event_starttime"]
                        p2s = other_results["event_peaktime"]
                        e2s = other_results["event_endtime"]
                        z = 0
                        for i in range(len(s2s)):
                            s2 = dt.datetime.strptime(str(s2s[i])[:16], "%Y-%m-%d %H:%M")
                            p2 = dt.datetime.strptime(str(p2s[i])[:16], "%Y-%m-%d %H:%M")
                            e2 = dt.datetime.strptime(str(e2s[i])[:16], "%Y-%m-%d %H:%M")
                            if s==s2 and p==p2 and e==e2:
                                z = other_results[i]
                                break
                        if z != 0:
                            loc1 = f"   N"+str(int(z["hgs_y"])).zfill(2) if z["hgs_y"]>0 else f"   S"+str(-int(z["hgs_y"])).zfill(2)
                            loc2 = f"W"+str(int(z["hgs_x"])).zfill(2) if z["hgs_x"]>0 else f"E"+str(-int(z["hgs_x"])).zfill(2)
                            arnum = z["ar_noaanum"] if z["ar_noaanum"]!=0 and type(z["ar_noaanum"])!=type(None) else ""
                            print(loc1, loc2, arnum)
                            if type(arnum) != type("hi"):
                                print("here", arnum, type(arnum))
                                arnum = arnum+10000 if arnum<10000 else arnum

                    mag = flare["fl_goescls"]
                    if type(arnum) == type("hi"):
                        print("inarnum assignment")
                        arnum = flare["ar_noaanum"] if flare["ar_noaanum"]!=0 else ""
                        if type(arnum) != type("hi"):
                            # print("here", arnum)
                            arnum = arnum+10000 if arnum<10000 else arnum
                    print(arnum)
                    newstr = f"{date}   {start}   {peak}   {end}   {mag}{loc1}{loc2}   {arnum}"
                    allevents += f"\n{newstr}"
                    priorev = newstr
                    print(priorev)
            with open(f'{path}/{directory}/{dt.datetime.now().year}_events.txt', 'w') as f:
                f.write(allevents)
    makeFinalList(path, folder)

                                              

    
# createEvents("/Users/jhou/LMSALDataSetupTaskOriginal", "testfinal")