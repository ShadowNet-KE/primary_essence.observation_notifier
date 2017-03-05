import login_creds


def get_learningJournal(s):
    #
    url_learning_journal = 'https://www.primaryessence.co.uk/LearningJourney/GetLJ/{child_id}'.format(child_id=login_creds.CHILD_ID)
    #
    ################################################################
    #
    # Get learning journal html
    r = s.post(url_learning_journal)
    #
    ################################################################
    #
    return r.text
