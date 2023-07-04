import sunpy.coordinates
from astropy.coordinates import SkyCoord
import math
import astropy.units as u
import sunpy.data.sample
import sunpy.map
from sunpy.net import Fido
from sunpy.net import attrs as a

from sunpy.physics.differential_rotation import diff_rot, solar_rotate_coordinate
from sunpy.time import parse_time
# import astropy.units as u

from sunpy.coordinates import Helioprojective, HeliographicStonyhurst #USE STONYHURST solarmonitor.org 
# from astropy.coordinates import SkyCoord
from sunpy.coordinates import RotatedSunFrame

import datetime as dt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from astropy.coordinates import SkyCoord
from astropy.io import fits
import drms

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def set_proxy(proxy):
    import os
    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
    os.environ['ftp_proxy'] = proxy
    os.environ['FTP_PROXY'] = proxy
set_proxy("http://proxy-zsgov.external.lmco.com:80")

def rotate2(point, starttime, duration):
    lat = int(point[1:3]) if point[0] == "N" else int(point[1:3]) * -1
    long = int(point[4:6]) if point[3] == "W" else int(point[4:6]) * -1
    hrs = duration*u.hour#(int(duration[0:2])+int(duration[2:4])/60)*u.hour
    if hrs == 0:
        return point
    
    start_time = starttime
    point = SkyCoord(long*u.deg, lat*u.deg, obstime = start_time, frame=HeliographicStonyhurst)
    # print(point)
    durations = [hrs]*u.hour#np.concatenate([range(-5, 0), range(1, 6)]) * u.day
    diffrot_point = RotatedSunFrame(base=point, duration=durations)
    # print(diffrot_point)
    transformed_diffrot_point = diffrot_point.transform_to(HeliographicStonyhurst)
    # print(transformed_diffrot_point[0])
    return transformed_diffrot_point.lon.degree, transformed_diffrot_point.lat.degree

def hmiQuery():
    import drms
    jsoc = drms.Client()
    ds = jsoc.series(r"aia.lev1_euv_12s") # Level 1.0
    si = jsoc.info(ds[0])
    print(si.segments)
    #Choose wavelnth
    wavelnth = 94 
    k, s = jsoc.query('{0:s}[2018-02-01T00:00/12s][WAVELNTH = {1:03d}]'.format(ds[0],wavelnth), 
                      key='DATE, T_OBS, FSN, DATAMEAN, TEMPCCD, EXPTIME',seg=['image','spikes'])
    # s.head() if you want to look at contents of s
    dummy, spikes = fits.open('http://jsoc.stanford.edu'+s['spikes'][0])
    dummy, image = fits.open('http://jsoc.stanford.edu'+s['image'][0])
    image.verify('fix')
    print(spikes.data.shape)
    

def getFromLocal():
    files = []
    for i in range(times):
        yr = date.year
        mnth = date.month
        day = date.day
        hr = date.hour
        mn = date.minute
        with open(f'/sunpy/data/hmi_m_45s_{yr}_{mnth}_{day}_{hr}_{mn}_30_tai_magnetogram.fits') as f:
            files.append(f)
        td = timedelta(hours=intvl)
        # your calculated date
        print(date, td)
        date = date + td
        # day += 1
    return sorted(files)
    
def downloadFitsFido(times, date, intvl):
    files = []
    for i in range(times):
        yr = date.year
        mnth = date.month
        day = date.day
        hr = date.hour
        mn = date.minute
        print(yr, mnth, day, hr, mn,int(mn)+1)
        result2 = Fido.search(a.Time(f'{yr}/{mnth}/{day} {hr}:{mn}:00', f'{yr}/{mnth}/{day} {hr}:{int(mn)+1}:00'), 
                     a.Instrument.hmi, a.Physobs.los_magnetic_field) # doesn't work if min is 59
        downloaded_file = Fido.fetch(result2)
        files.append(downloaded_file)
        
        td = timedelta(hours=intvl)
        # your calculated date
        print(date, td)
        date = date + td
        # day += 1
    return sorted(files)

def downloadFitsJsoc(times, date, intvl):
    files = []
    jsoc = drms.Client(email="jhou@lmsal.com")
    
    yr1 = str(date.year).zfill(2)
    mnth1 = str(date.month).zfill(2)
    day1 = str(date.day).zfill(2)
    hr1 = str(date.hour).zfill(2)
    
    td = timedelta(hours=intvl*times)
    # your calculated date
    print(date, td)
    date = date + td
    
    yr2 = str(date.year).zfill(2)
    mnth2 = str(date.month).zfill(2)
    day2 = str(date.day).zfill(2)
    hr2 = str(date.hour).zfill(2)
    
    
    ds = f'hmi.sharp_720s[][{yr1}.{mnth1}.{day1}_{hr1}:12:00_TAI-{yr1}.{mnth1}.{day1}_{hr1}:12:00_TAI]' + '{magnetogram}'    # Level 1.0
    #hmi.sharp_720s[1449][2012.03.07_00:12:00_TAI-2012.03.10_00:12:00_TAI]{magnetogram}
    sharpnum = "1449"
    d1 = "2012.03.07_00:12:00"
    d2 = "2012.03.10_00:12:00"


    query, s = jsoc.query(ds, key='NOAA_AR, DATE, DATE-OBS, T_REC, T_OBS,  CRPIX1, CRPIX2, CRVAL1, CRVAL2, CDELT1, CDELT2, CROTA2,RSUN_OBS, DSUN_OBS, DSUN_REF,RSUN_REF,CRLN_OBS,CRLT_OBS', seg=['magnetogram'])
    
    for i in range(times):
        yr = date.year
        mnth = date.month
        day = date.day
        hr = date.hour
        mn = date.minute
        print(yr, mnth, day, hr, mn,int(mn)+1)
        result2 = Fido.search(a.Time(f'{yr}/{mnth}/{day} {hr}:{mn}:00', f'{yr}/{mnth}/{day} {hr}:{int(mn)+1}:00'), 
                     a.Instrument.hmi, a.Physobs.los_magnetic_field) # doesn't work if min is 59
        downloaded_file = Fido.fetch(result2)
        files.append(downloaded_file)
        
        td = timedelta(hours=intvl)
        # your calculated date
        print(date, td)
        date = date + td
        # day += 1
    return sorted(files)


def downloadHeliographicFrames(date, time, location, intvl, times, mag, version = "fido"): #interval in hours, convert into helioprojective or cartesian heliographic
    time = time.zfill(4)
    hrinit = time[0:2]
    mninit = time[2:4]
    hrs = (int(time[0:2])+int(time[2:4])/60)
    
    date = dt.datetime(date.year, date.month, date.day, int(hrinit), int(mninit))
    
    try:
        sorted_files = getFromLocal(times, date, intvl)
    except:
        if version == "fido":
            sorted_files = downloadFitsFido(times, date, intvl)
        else:
            sorted_files = downloadFitsJsoc(times, date, intvl)
    
    for i in range(times):
        lon, lat = rotate2(location, date, hrs+intvl*i)
        print(lon, lat)
        hmi_map = sunpy.map.Map(sorted_files[i][0])
        hmi_rotated = hmi_map.rotate(order=3)
        top_right = SkyCoord((lon+10) * u.deg, (lat+10) * u.deg, frame=HeliographicStonyhurst)
        bottom_left = SkyCoord((lon-10) * u.deg, (lat-10) * u.deg, frame=HeliographicStonyhurst)
        swap_submap = hmi_rotated.submap(bottom_left, top_right=top_right)
        plt.figure()
        swap_submap.plot()
        swap_submap.draw_limb()
        swap_submap.draw_grid()
        output_dir = "hmiIMGs"
        fn = f"{location}_{mag}_{i}.png"
        plt.savefig(("{}/"+fn).format(output_dir)) #eventually change to save in certain directory
        plt.show()

downloadFrames(dt.datetime(2012, 3, 7), "0024", "N18E31", .2, 600, "X54")


def downloadCEAFrames(date, time, location, intvl, times, mag, version = "fido"):
    time = time.zfill(4)
    hrinit = time[0:2]
    mninit = time[2:4]
    hrs = (int(time[0:2])+int(time[2:4])/60)
    
    date = dt.datetime(date.year, date.month, date.day, int(hrinit), int(mninit))
    
    try:
        sorted_files = getFromLocal(times, date, intvl)
    except:
        if version == "fido":
            sorted_files = downloadFitsFido(times, date, intvl)
        else:
            sorted_files = downloadFitsJsoc(times, date, intvl)
    
    for i in range(times):
        lon, lat = rotate2(location, date, hrs+intvl*i)
        hmi_map = sunpy.map.Map(f'/Users/jhou/sunpy/data/hmi_m_45s_2012_03_07_01_13_30_tai_magnetogram.fits')#sorted_files[i][0])
        hmi_rotated = hmi_map.rotate(order=3)
        top_right = SkyCoord((lon+20) * u.deg, (lat+20) * u.deg, frame=HeliographicStonyhurst)
        bottom_left = SkyCoord((lon-20) * u.deg, (lat-20) * u.deg, frame=HeliographicStonyhurst)
        swap_submap = hmi_rotated.submap(bottom_left, top_right=top_right)
        plt.figure()
        swap_submap.plot()
        swap_submap.draw_limb()
        swap_submap.draw_grid()
        output_dir = "hmiIMGs"
        plt.show()

        # aia_map = sunpy.map.Map(sunpy.data.sample.AIA_193_IMAGE)

        # plt.figure()
        # aia_map.plot()
        # plt.show()


        shape_out = (720, 720)
        frame_out = SkyCoord(lon, lat, unit=u.deg,
                             frame="heliographic_stonyhurst",
                             obstime=swap_submap.date,
                             rsun=swap_submap.coordinate_frame.rsun)
        header = sunpy.map.make_fitswcs_header(shape_out,
                                               frame_out,
                                               scale=(20 / shape_out[1],
                                                      20 / shape_out[0]) * u.deg / u.pix,
                                               projection_code="CEA")



        outmap = swap_submap.reproject_to(header)



        plt.figure()
        outmap.plot()
        outmap.draw_limb(color='blue')

        plt.show()
        output_dir = "hmiIMGs"
        fn = f"{location}_{mag}_{i}.png"
        plt.savefig(("{}/"+fn).format(output_dir)) #eventually change to save in certain directory
        plt.show()
# makeMovie(dt.datetime(2012, 3, 7), "0024", "N18E31", 12, 10, "X54") # 3hr cadence or 12 min cadenc, use drms, add symbol of flare
# '2012/03/10 17:44:00'
        
# aia 171 channel aia and hmi sun size not necessarily same size, think about overlaying them
#cylindrical equal area (heliographic)
# https://docs.sunpy.org/en/stable/generated/gallery/map_transformations/autoalign_aia_hmi.html?highlight=2d%20projection#auto-aligning-aia-and-hmi-data-during-plotting

# from sunpy.net.jsoc.jsoc import drms
# client = drms.Client()
# import numpy
# from datetime import date
# d = date.today()
# print(str(d.day).zfill(2))
# # harp = client.query(f'hmi.sharp_720s[][2010.05.31_00:00_TAI-2010.06.03_00:00_TAI]', key = ['HARPNUM','T_REC','NOAA_ARS'])

# harp = client.query(f'hmi.sharp_720s[][2010.05.01_00:00_TAI-{str(d.year).zfill(2)}.{str(d.month).zfill(2)}.{str(d.day).zfill(2)}_00:00_TAI]', key = ['HARPNUM','T_REC','NOAA_ARS'])
# harp.to_csv("harpnums.csv")
def aiaQuery():
    import drms
    jsoc = drms.Client()
    ds = jsoc.series(r"aia.lev1_euv_12s") # Level 1.0
    si = jsoc.info(ds[0])
    print(si.segments)
    #Choose wavelnth
    wavelnth = 94 
    k, s = jsoc.query('{0:s}[2018-02-01T00:00/12s][WAVELNTH = {1:03d}]'.format(ds[0],wavelnth), 
                      key='DATE, T_OBS, FSN, DATAMEAN, TEMPCCD, EXPTIME',seg=['image','spikes'])
    # s.head() if you want to look at contents of s
    dummy, spikes = fits.open('http://jsoc.stanford.edu'+s['spikes'][0])
    dummy, image = fits.open('http://jsoc.stanford.edu'+s['image'][0])
    image.verify('fix')
    print(spikes.data.shape)