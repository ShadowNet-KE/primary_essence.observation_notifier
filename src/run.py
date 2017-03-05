from time import sleep
from datetime import datetime
from primaryessence.get_data import get_learningJournal
from primaryessence.session import create_session
from primaryessence.parse_observations import find_observations
from primaryessence import creds
from notifications.notify_email import send_notifications_all

s = create_session(creds.NURSERY, creds.PREFIX, creds.USERNAME, creds.PASSWORD)

while True:
    #
    r = {}
    o = {}
    for child_id in creds.CHILD_ID:
        r[child_id] = get_learningJournal(s, child_id)
        o[child_id] = find_observations(s, r[child_id])
        #
        send_notifications_all(child_id, o[child_id])
    #
    print('Operation run at {time}'.format(time=datetime.now().strftime('%YYYY-%mm-%dd %HH:%MM:%ss')))
    #
    sleep(3600000) # hourly
    #
