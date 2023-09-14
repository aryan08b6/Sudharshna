import win32evtlog


def getLog(log, num):
    hlog = win32evtlog.OpenEventLog(None, log)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    L = []
    events = win32evtlog.ReadEventLog(hlog, flags, 0)
    while len(events) < num:
        batch = win32evtlog.ReadEventLog(hlog, flags, 0)
        if len(batch) > 0:
            events.extend(batch)
        else:
            print("No of logs Asked exceeds the amount of total no of logs")
    for i in range(num):
        event = events[i]
        L.append({"eventID": event.EventID,
                  "event_time": event.TimeGenerated.Format(),
                  "event_level": event.EventType,
                  "event_category": event.EventCategory,
                  "event_data": event.StringInserts,
                  "CompName": event.ComputerName,
                  "ReservedFlags": event.ReservedFlags}
                 )
    win32evtlog.CloseEventLog(hlog)
    return L


