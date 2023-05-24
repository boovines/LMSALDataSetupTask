import getData
import saveSRS2
import getEvents
import get1mindata
import parsecheck3
import newparsemindata2
import appendNewFluxes2
import groupARandEventFinal
import getFIs

def main():
    getData.getAll()
    saveSRS2.getData()
    noaa, herr, merged = getEvents.makeFinalList()
    # stitchTogether(startdate, starttime, enddate, endtime, calibrated=True)
    newfluxes = newparsemindata2.stitchTogether(dt.datetime(2016,11,4), "1800", dt.datetime(2023,1,5), "2359", True)
    oldfluxes = newparsemindata2.stitchTogether(dt.datetime(2016,11,4), "1800", dt.datetime(2023,1,5), "2359", False)
    appendNewFluxes2.appendData()
    groupARandEventFinal
    groupARandEventFinal.compileEvents()
    tfilist = getFIs.getTFIs()
    top10TFIs = getFIs.getTop10(tfilist)
    return top10TFIs
print(main())
