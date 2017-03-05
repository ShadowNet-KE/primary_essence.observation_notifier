from primaryessence.get_data import get_learningJournal
from primaryessence.session import create_session
from primaryessence import creds

s = create_session(creds.NURSERY, creds.PREFIX, creds.USERNAME, creds.PASSWORD)

r = {}
for child_id in creds.CHILD_ID:
    r[child_id] = get_learningJournal(s, child_id)
    print(r[child_id])
