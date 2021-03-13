from gcsa.google_calendar import GoogleCalendar
import datetime
from tzlocal import get_localzone

tz = get_localzone()


def getCalendar():
    return GoogleCalendar("qhoj79fkhg5m4mdfle097kd3q8@group.calendar.google.com", credentials_path=".credentials/credentials.json")

def fetchEvents():
    calendar = getCalendar()
    out = []
    for i in calendar.get_events(time_min=datetime.datetime.now(tz), order_by="startTime", single_events=True):
        out.append(i)
    return out

def nextEvent(events):
    for event in events:
        print("HALLO")
        print(event.start.timestamp() < datetime.datetime.now(tz).timestamp())
        if event.start.timestamp() < datetime.datetime.now(tz).timestamp():
            continue
        else:
            return event

