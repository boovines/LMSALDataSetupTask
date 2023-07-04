import getData
import saveSRS2
import getEvents
import createEvents
import get1mindata
import parsecheck3
import newparsemindata3
import appendNewFluxes2
import groupARandEventFinal
import time
import datetime as dt
import getFIs
import os

def remTime(d):
    return dt.datetime(d.year, d.month, d.day)

def updatedToday(fp):
    if os.path.exists(fp):
        if remTime(dt.datetime.now())>dt.datetime.fromtimestamp(os.path.getmtime(fp)):
            return False
        else: return True
    else: return False


def main(path, folder):
    # Create the data-containing folder if it does not already exist
    if not os.path.exists(f"{path}/{folder}"):
        os.mkdir(f"{path}/{folder}")
    
    # Get daily active region text file data from ftp.swpc.noaa.gov
    getData.getAll(path)
    time.sleep(10)
    
    # Parse the downloaded text files into a data structure containing all active region data by day
    saveSRS2.getData(f"{path}/{folder}")
    print("FINISHED SAVING SRS")
    time.sleep(10)
    
    # Create text file event lists if saved ones are deleted, parse them into event list csv
    if not updatedToday(f"{path}/{folder}/mergedevs.csv"):
        # noaa, herr, merged = getEvents.makeFinalList(path)
        createEvents.createEvents(path, folder)
        print("FINISHED SAVING EVENTS")
        time.sleep(10)
    
    # Get all 1-minute cadence XRS flux data 
    if not updatedToday(f"{path}/{folder}/goes16onemin.nc"):
        print("hereher")
        get1mindata.getLatest(f"{path}/{folder}", "16")
        print("FINISHED GETTING XRS")
        time.sleep(10)
        parsecheck3.makeNewData(f"{path}/{folder}")
        print("FINISHED PREPARING XRS")
        time.sleep(10)
        parsecheck3.makeOldData(f"{path}/{folder}")

        time.sleep(10)
        # stitchTogether(startdate, starttime, enddate, endtime, calibrated=True)
        newfluxes = newparsemindata3.stitchTogether(f"{path}/{folder}", True)
        time.sleep(10)
        oldfluxes = newparsemindata3.stitchTogether(f"{path}/{folder}", False)
        print("FINISHED FINAL XRS LISTS")
        time.sleep(10)
    # Append flux data to event data and group the events with active regions
    if not updatedToday(f"{path}/{folder}/newmergedevs.csv"):
        appendNewFluxes2.appendData(f"{path}/{folder}")
        print("FINISHED FINAL EVENT LISTS")
        time.sleep(10)


        # This is producing occasional duplicates still for some reason
        groupARandEventFinal.compileEvents(f"{path}/{folder}", "HER")
        print("FINISHED FLARE ASSIGNMENT")
        time.sleep(10)
    
    # Create final data structure and corresponding DFIs and TFIs for each day/active region
    assignmentsFinal, sortedAssignmentsFinal = getFIs.injectFIassignments(f"{path}/{folder}")
    print("FINISHED TFI PRODUCTS")
    return sortedAssignmentsFinal
