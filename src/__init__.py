from primaryessence.get_data import get_learningJournal
from primaryessence.session import create_session

s = create_session()
r = get_learningJournal(s)

print(r)