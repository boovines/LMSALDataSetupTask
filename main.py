import getData
import saveSRS2
import getEvents
import get1mindata
import parsecheck3
import newparsemindata2
import appendNewFluxes2
import groupARandEventFinal
import getFIs
import time

def main(path):
    getData.getAll(path)
    time.sleep(20)
    saveSRS2.getData(path)
    time.sleep(20)
    noaa, herr, merged = getEvents.makeFinalList(path)
    time.sleep(20)
    
    get1mindata.getLatest(path, "16")
    time.sleep(20)
    parsecheck3.makeNewData(path)
    time.sleep(20)
    parsecheck3.makeOldData(path)
    time.sleep(20)
    # stitchTogether(startdate, starttime, enddate, endtime, calibrated=True)
    newfluxes = newparsemindata2.stitchTogether(path, True)
    time.sleep(20)
    oldfluxes = newparsemindata2.stitchTogether(path, False)
    time.sleep(20)
    appendNewFluxes2.appendData(path)
    time.sleep(20)
    # groupARandEventFinal
    groupARandEventFinal.compileEvents("/Users/jhou/LMSALDataSetupTaskOriginal/testdata", "HER")
    time.sleep(20)
    tfilist = getFIs.getTFIs("NEW")
    top10TFIs = getFIs.getTop10(tfilist)
    return top10TFIs
print(main("/Users/jhou/LMSALDataSetupTaskOriginal/newfoldertest"))
