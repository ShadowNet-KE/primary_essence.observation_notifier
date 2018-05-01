# primary_essence.update_checker

Application to run and check on regular basis (currently set to hourly) for new observations on the Primary Essence website for child(ren).

A history of the observations are maintained against each child ID in the history.json file, and at each scheduled run the observation IDs are checked against this list.

Details from any new observations are extracted, along with the image or video, and emailed to the email addresses in the config.json module.