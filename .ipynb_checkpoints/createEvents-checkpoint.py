from sunpy.net import Fido
from sunpy.net import attrs as a
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from astropy.io import fits
import datetime as dt

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


def createEvents(p, event_type = "FL"):
    for year in range(2010,2024):
        today = remTime(dt.datetime.now())
        tstart = f"{year}/1/1"
        tend = f"{year}/{remTime(dt.datetime.now()).month}/{remTime(dt.datetime.now()).day}" if year==2023 else f"{year}/12/31"

        filtered_results = getFido(tstart, tend, "GOES")
        other_results = getFido(tstart, tend, "SDO")
        
        file_content = f"GOES XRAY events for {year} \nWritten {today}, Justin Hou, justinhou2005@gmail.com \n{len(filtered_results)} events were retrieved from the Heliophysics Event Registry (HER) \n\nColumns:Date, Start, Peak, End Time, Class, Position (if available), Active Region (if available) \n"

        # print(str(flare["event_starttime"].hour).zfill(2))
        for flare in filtered_results:
            s = dt.datetime.strptime(str(flare["event_starttime"])[:16], "%Y-%m-%d %H:%M")
            p = dt.datetime.strptime(str(flare["event_peaktime"])[:16], "%Y-%m-%d %H:%M")
            e = dt.datetime.strptime(str(flare["event_endtime"])[:16], "%Y-%m-%d %H:%M")

            start = f"{str(s.hour).zfill(2)}:{str(s.minute).zfill(2)}"
            peak = f"{str(p.hour).zfill(2)}:{str(p.minute).zfill(2)}"
            end = f"{str(e.hour).zfill(2)}:{str(e.minute).zfill(2)}"
            arnum = ""

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
                    arnum = z["ar_noaanum"] if z["ar_noaanum"]!=0 else ""
                    if type(arnum) != type("hi"):
                        # print("here", arnum)
                        arnum = arnum+10000 if arnum<10000 else arnum

            mag = flare["fl_goescls"]
            
            if arnum == type("hi"):
                arnum = flare["ar_noaanum"] if flare["ar_noaanum"]!=0 else ""
                if type(arnum) != type("hi"):
                    # print("here", arnum)
                    arnum = arnum+10000 if arnum<10000 else arnum
            # print(arnum)

            file_content+=f"\n{str(remTime(s))[:10]}   {start}   {peak}   {end}   {mag}{loc1}{loc2}   {arnum}"
        
        directory = "event_text_files"
        if not os.path.exists(f'{p}/{directory}'):
            os.mkdir(f'{p}/{directory}')
        with open(f'{p}/{directory}/{year}_events.txt', 'w') as f:
            f.write(file_content)

    # Sorting is done by using the flare class from "fl_goescls"
    # By converting the flare class to a number using ord()
    # and adding the flare strength, we can sort by value
    by_magnitude = sorted(filtered_results, key=lambda x: ord(x['fl_goescls'][0]) + float(x['fl_goescls'][1:]), reverse=True)

    # for flare in filtered_results:
    #     print(f"Class {flare['fl_goescls']} occurred on {flare['event_starttime']}")

    # with open('docs/readme.txt', 'w') as f:
    #     f.write('Create a new text file!')

    # print(result.errors)
createEvents("/Users/jhou/LMSALDataSetupTaskOriginal/testdata623")