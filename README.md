# primaryessence_update-checker

Application to run and check on regular basis (currently set to hourly) for new observations on the primary essence website for child(ren).

A history of the observation IDs are maintained against each child ID in json format, and each scheduled run is checked against this list. Any new observations are emailed, along with the image embedded in the email, to the email addresses in the notifications.creds.py module.

<hr>

<h3>Required python packages</h3>
<p>The following python packages require installation on the target system:
<br>
requests: <code>http://docs.python-requests.org/en/master/</code>
<br>
Beautiful Soup: <code>https://pypi.python.org/pypi/beautifulsoup4</code>
</p>
