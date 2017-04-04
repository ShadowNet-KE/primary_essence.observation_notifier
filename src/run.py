from time import sleep
import datetime
from primaryessence.get_data import get_learningJournal
from primaryessence.session import create_session
from primaryessence.parse_observations import find_observations
from primaryessence import creds
from notifications.notify_email import send_notifications_all


while True:
    #
    s = create_session(creds.NURSERY, creds.PREFIX, creds.USERNAME, creds.PASSWORD)
    #
    r = {}
    o = {}
    for child_id in creds.CHILD_ID:
        r[child_id] = get_learningJournal(s, child_id)
        o[child_id] = find_observations(s, r[child_id])
        #
        send_notifications_all(child_id, o[child_id])
    #
    now = datetime.datetime.now()
    nxt = now + datetime.timedelta(hours=1)
    #
    s = 7    # opening time of nursery in 24 hours
    e = 18   # closing time of nursery in 24 hours
    #
    if nxt.time() >= datetime.time(e):
        nxt = datetime.datetime(now.year, now.month, now.day+1, datetime.time(s).hour, 0, 0, 0)
    elif nxt.time() < datetime.time(s):
        nxt = datetime.datetime(now.year, now.month, now.day, datetime.time(s).hour, 0, 0, 0)
    #
    print('****************************************************************')
    print('Operation run at:            {dt}'.format(dt=now.strftime('%Y-%m-%d %H:%M')))
    print('Next scheduled run will be:  {dt}'.format(dt=nxt.strftime('%Y-%m-%d %H:%M')))
    print('****************************************************************')
    #
    slp = (nxt - now).seconds
    #
    sleep(slp)
    #
