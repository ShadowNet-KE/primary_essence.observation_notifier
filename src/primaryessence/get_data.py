def get_learningJournal(s, child_id):
    #
    url_learning_journal = 'https://www.primaryessence.co.uk/LearningJourney/GetLJ/{child_id}'.format(child_id=child_id)
    #
    ################################################################
    #
    # Get learning journal html
    r = s.post(url_learning_journal)
    #
    ################################################################
    #
    return r.text
