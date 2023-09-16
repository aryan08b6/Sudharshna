import requests 
from datetime import datetime, timedelta 
from time import sleep
import win32evtlog
import json

serverURL = "http://localhost:5000"


def getSysId():
    return 1

def getLocalID():
    return 1

SYSTEMID = getSysId()
LOCATIONID = getLocalID()

def getTimeThreshold():
    return int(requests.get(url=serverURL+"/timeGap", params= {"LOCATIONID": LOCATIONID}).json())


def getLog(log_type, timeRange):
    event_log_handle = win32evtlog.EvtOpenLog(log_type, win32evtlog.EVENTLOG_READONLY)
    query = """<QueryList><Query Id="0" Path="/System"><Select Path="/System">*[System[TimeCreated[@SystemTime>='{start_time}'] and System[TimeCreated[@SystemTime<='{end_time}']]]</Select></Query></QueryList>""".format(start_time=range[0], end_time=range[1])

    query_handle = win32evtlog.EvtQuery(event_log_handle, win32evtlog.EvtQueryForwardDirection, query, None)

    events = []
    while True:
        event = win32evtlog.EvtNext(query_handle, 1, 1, 0)
        if event is None:
            break
        data = {"EventID": event.EventID, "EventMessage": event.Message, "EventType": event.EventType, "EventTime": event.TimeGenerated}
        events.append(data)

    win32evtlog.EvtClose(event_log_handle)
    return events

timeGap = getTimeThreshold()

schedule = requests.get(url=serverURL+"/time", params= {"SYSTEMID": SYSTEMID, "LOCATIONID": LOCATIONID}).json()
lastUpdate = json.loads(schedule["LastUp"])

dayGap = timedelta(days=timeGap)

while True:
    timeDiff = datetime.now() - lastUpdate
    if timeDiff > dayGap:
        print("Updating Logs.....")
        tRange = lastUpdate.strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Applications Logs")
        appLogs = getLog(log="Application", timeRange=tRange)
        print("System Logs")
        sysLogs = getLog(log="System", timeRange=tRange)
        print("Security Logs")
        secLogs = getLog(log="Security", timeRange=tRange)
        print("Setup Logs")
        setLogs = getLog(log="Setup", timeRange=tRange)
        print("Forwarded Events Logs")
        forLogs = getLog(log="Forwarded Events", timeRange=tRange)
        jsonData = json.dumps({"Application": json.dumps(appLogs), "Security": json.dumps(secLogs), "Setup": json.dumps(setLogs), "System": json.dumps(sysLogs), "Forwarded Events": json.dumps(forLogs)})
        requests.post(serverURL + "/logPush", json=jsonData)
        print("Updating The LastUp")
        requests.post(url=serverURL + "/timeUpdate", json={"SYSTEMID": SYSTEMID, "LOCATIONID": LOCATIONID, "Time": json.dumps(datetime.now())})
        
    else:
        sleepSecs = dayGap.total_seconds() - timeDiff.total_seconds()
        print("Sleeping")
        sleep(sleepSecs)


