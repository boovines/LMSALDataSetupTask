from sunpy.net.jsoc.jsoc import drms
client = drms.Client()
import numpy

d = date.today()
print(str(d.day).zfill(2))
harp = client.query(f'hmi.sharp_720s[][2010.05.31_00:00_TAI-2010.06.03_00:00_TAI]', key = ['HARPNUM','T_REC','NOAA_ARS'])

# harp = client.query(f'hmi.sharp_720s[][2010.05.01_00:00_TAI-{str(d.year).zfill(2)}.{str(d.month).zfill(2)}.{str(d.day).zfill(2)}_00:00_TAI]', key = ['HARPNUM','T_REC','NOAA_ARS'])
harp.to_csv("harpnums.csv")