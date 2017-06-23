from time import sleep
import datetime
from primaryessence.get_data import get_learningJournal
from primaryessence.session import create_session
from primaryessence.parse_observations import find_observations
from primaryessence import creds
from notifications.notify_email import send_notifications_all


while True:
    #
    err_count = 0
    #
    now = datetime.datetime.now()
    #
    s = 7    # opening time of nursery in 24 hours
    e = 18   # closing time of nursery in 24 hours
    #
    if now.hour >= datetime.time(e).hour:
        nxt = datetime.datetime(now.year, now.month, now.day, datetime.time(s).hour, 0, 0, 0) + datetime.timedelta(days=1)
    elif now.hour < datetime.time(s).hour:
        nxt = datetime.datetime(now.year, now.month, now.day, datetime.time(s).hour, 0, 0, 0)
    else:
        nxt = now + datetime.timedelta(hours=1)
    #
    print('****************************************************************')
    print('Operation started at:              {dt}'.format(dt=now.strftime('%Y-%m-%d %H:%M')))
    #
    try:
        s = create_session(creds.NURSERY, creds.PREFIX, creds.USERNAME, creds.PASSWORD)
        #
        count = 0
        #
        r = {}
        o = {}
        for child_id in creds.CHILD_ID:
            r[child_id] = get_learningJournal(s, child_id)
            o[child_id] = find_observations(s, r[child_id], child_id)
            #
            count += send_notifications_all(child_id, o[child_id])
        #
        print('Operation completed successfully:  {count} email(s) updates found'.format(count=count))
        err_count = 0
        #
    except Exception as e:
        err_count =+ 1
        print('Error running operation:           Attempt {err_count} - {error}'.format(err_count=err_count,
                                                                                        error=e))
    #
    print('Next scheduled run will be:        {dt}'.format(dt=nxt.strftime('%Y-%m-%d %H:%M')))
    print('****************************************************************')
    #
    slp = (nxt - now).seconds
    #
    sleep(slp)
    #
