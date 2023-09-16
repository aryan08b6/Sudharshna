import requests 
from datetime import datetime, timedelta 
from time import sleep
import win32evtlog
import json


def getSysId():
    return 1

def getLocalID():
    return 1

def getTimeThreshold():
    return int(requests.get(url=serverURL+"/params", params= {"PARAM": "TimeGap", "LOCATIONID": LOCATIONID}).json())


def getLog(log_type, timeRange):
    event_log_handle = win32evtlog.EvtOpenLog(log_type, win32evtlog.EVENTLOG_READONLY)
    query = """<QueryList><Query Id="0" Path="/System"><Select Path="/System">*[System[TimeCreated[@SystemTime>='{start_time}'] and System[TimeCreated[@SystemTime<='{end_time}']]]</Select></Query></QueryList>""".format(start_time=range[0], end_time=range[1])

    query_handle = win32evtlog.EvtQuery(event_log_handle, win32evtlog.EvtQueryForwardDirection, query, None)

    events = []
    while True:
        event = win32evtlog.EvtNext(query_handle, 1, 1, 0)
        if event is None:
            break
        events.append(event)

    win32evtlog.EvtClose(event_log_handle)
    return events

timeGap = getTimeThreshold()
SYSTEMID = getSysId()
LOCATIONID = getLocalID
serverURL = ""

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
        jsonData = json.dumps({"Application": appLogs, "Security": secLogs, "Setup": setLogs, "System": sysLogs, "Forwarded Events": forLogs})
        requests.post(serverURL + "/logPush", json=jsonData)
        print("Updating The LastUp")
        requests.post(url=serverURL + "/timeUpdate", json=json.dumps({"SYSTEMID": SYSTEMID, "LOCATIONID": LOCATIONID, "Time": datetime.now()}))
        
    else:
        sleepSecs = dayGap.total_seconds() - timeDiff.total_seconds()
        print("Sleeping")
        sleep(sleepSecs)

