from googleCalendarHandeling import *
import asyncio
import datetime
from copy import deepcopy
from notifypy import Notify
from pytz import timezone
from tzlocal import get_localzone

tz = get_localzone()

events = None
nextEventTask = None

def notify(title, text):
    a = Notify(
        default_notification_application_name="ToDo",
        default_notification_icon="images/to-do.png"
    )
    a.title = title
    a.message = text
    return a.send()

def strfTimedelta(td: datetime.timedelta):
    out = []
    minutes, seconds = divmod(td.total_seconds(), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    if days > 0:
        out.append(f"{days} days")
    if hours > 0:
        out.append(f"{hours} hours")
    if minutes > 0:
        out.append(f"{minutes} minutes")
    if seconds > 0:
        out.append(f"{seconds} seonds")

    return " ".join(out)

def roundTime(dt=None, roundTo=60):
    """Round a datetime object to any time lapse in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if dt == None:
        dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + datetime.timedelta(0,rounding-seconds, -dt.microseconds)


async def fetchEventsLoop():
    global events, nextEventTask
    firstRun = True
    while True:
        oldEvents = deepcopy(events)
        events = fetchEvents()
        if len(events) == 0:
            events = None
        if firstRun and events is not None:
            asyncio.create_task(notifyWhenDue(nextEvent(events)))
            firstRun = False
        if events is not None and oldEvents is not None:
            if events[0] != oldEvents[0]:
                if nextEventTask is not None:
                    nextEventTask.cancel()
                nextEventTask = asyncio.create_task(notifyWhenDue(nextEvent(events)))
        print(events)
        await asyncio.sleep(10)


async def notifyWhenDue(event):
    print(event)
    toWait = roundTime(event.start - datetime.datetime.now(tz))
    print(toWait)
    notify(event.summary, f"Už za {strfTimedelta(toWait)}")

    await asyncio.sleep(toWait.total_seconds()-600)
    toWait = roundTime(event.start - datetime.datetime.now(tz))
    notify(event.summary, f"Už za {strfTimedelta(toWait)}")

    await asyncio.sleep(toWait.total_seconds()-60)
    toWait = roundTime(event.start - datetime.datetime.now(tz))
    notify(event.summary, f"Už za {strfTimedelta(toWait)}")

    await asyncio.sleep(toWait.total_seconds())
    notify(event.summary,"Pracuj!")


asyncio.run(fetchEventsLoop())

