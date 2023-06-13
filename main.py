import getData
import saveSRS2
import getEvents
import get1mindata
import parsecheck3
import newparsemindata3
import appendNewFluxes2
import groupARandEventFinal
import time


    
def main(path):
    # getData.getAll(path)
    # time.sleep(20)
    saveSRS2.getData(path)
    print("FINISHED SAVING SRS")
    time.sleep(10)
    noaa, herr, merged = getEvents.makeFinalList(path)
    print("FINISHED SAVING EVENTS")
    time.sleep(10)
    
    get1mindata.getLatest(path, "16")
    print("FINISHED GETTING XRS")
    time.sleep(10)
    parsecheck3.makeNewData(path)
    print("FINISHED PREPARING XRS")
    time.sleep(10)
    parsecheck3.makeOldData(path)
    
    time.sleep(10)
    # stitchTogether(startdate, starttime, enddate, endtime, calibrated=True)
    newfluxes = newparsemindata3.stitchTogether(path, True)
    time.sleep(10)
    oldfluxes = newparsemindata3.stitchTogether(path, False)
    print("FINISHED FINAL XRS LISTS")
    time.sleep(10)
    
    appendNewFluxes2.appendData(path)
    print("FINISHED FINAL EVENT LISTS")
    time.sleep(10)
    # groupARandEventFinal
    groupARandEventFinal.compileEvents(path, "HER")
    print("FINISHED FLARE ASSIGNMENT")
    time.sleep(10)
    import getFIs
    tfilist = getFIs.getTFIs("NEW")
    top10TFIs = getFIs.getTop10(tfilist)
    print("FINISHED TFI PRODUCTS")
    return top10TFIs
print(main("/Users/jhou/LMSALDataSetupTaskOriginal/testdata612"))
