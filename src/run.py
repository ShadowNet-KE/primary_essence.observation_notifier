from primaryessence.get_data import get_learningJournal
from primaryessence.session import create_session
from primaryessence.parse_observations import find_observations
from primaryessence import creds

s = create_session(creds.NURSERY, creds.PREFIX, creds.USERNAME, creds.PASSWORD)

r = {}
o = {}
for child_id in creds.CHILD_ID:
    r[child_id] = get_learningJournal(s, child_id)
    o[child_id] = find_observations(s, r[child_id])
    #
    print(o[child_id])
