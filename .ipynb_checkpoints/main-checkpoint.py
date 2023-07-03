# import getData
import saveSRS2
import getEvents
import createEvents
import get1mindata
import parsecheck3
import newparsemindata3
import appendNewFluxes2
# import groupARandEventFinal
import groupARandEventFinal
import time
import datetime as dt
import getFIs

def remTime(d):
    return dt.datetime(d.year, d.month, d.day)

def updatedToday(fp):
    if os.path.exists(fp):
        if remTime(dt.datetime.now())>dt.datetime.fromtimestamp(os.path.getmtime(fp)):
            return False
    return True
    
#unresolved portions: SRS download on proxy, make events quicker, find cloud storage
def main(path):
    
    # getData.getAll(path)
    # time.sleep(20)
    saveSRS2.getData(path)
    print("FINISHED SAVING SRS")
    time.sleep(10)
    
    if not updatedToday(f"{path}/mergedevs.csv"):
        # noaa, herr, merged = getEvents.makeFinalList(path)
        createEvents.createEvents(path)
        print("FINISHED SAVING EVENTS")
        # time.sleep(10)
    
    if not updatedToday(f"{path}/goes16onemin.nc"):
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
    
    if not updatedToday(f"{path}/newmergedevs.csv"):
        appendNewFluxes2.appendData(path)
        print("FINISHED FINAL EVENT LISTS")
        time.sleep(10)


        # groupARandEventFinal
        groupARandEventFinal.compileEvents(path, "HER")
        print("FINISHED FLARE ASSIGNMENT")
        time.sleep(10)
    
    assignmentsFinal, sortedAssignmentsFinal = getFIs.injectFIassignments(path)
    # top10TFIs = getFIs.getTop10(tfilist)
    print("FINISHED TFI PRODUCTS")
    return sortedAssignmentsFinal
print(main("/Users/jhou/LMSALDataSetupTaskOriginal/testdata623"))
