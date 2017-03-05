import login_creds
import requests
import requests.cookies


def create_session():
    #
    url_login = 'https://www.primaryessence.co.uk/{nursery}'.format(nursery=login_creds.NURSERY)
    url_login_post = 'https://www.primaryessence.co.uk/Login/General'

    with requests.Session() as s:
        #
        ################################################################
        #
        # Get login page to get sessionId
        r = s.get(url_login)
        #
        ################################################################
        #
        # Get the session cookie and set to the requests session
        c = r.cookies._cookies['www.primaryessence.co.uk']['/']['ASP.NET_SessionId']
        new_cookie = {'name': 'ASP.NET_SessionId',
                      'value': c.value,
                      'domain': 'www.primaryessence.co.uk',
                      'path': '/'}
        #
        s.cookies.set(**new_cookie)
        #
        ################################################################
        #
        # Set the cookie for nursery
        new_cookie = {'name': 'PEEELoginUrl',
                      'value': login_creds.NURSERY,
                      'domain': 'www.primaryessence.co.uk',
                      'path': '/'}
        #
        s.cookies.set(**new_cookie)
        #
        ################################################################
        #
        r = s.post(url_login_post,
                   files=(('prefix', (None, login_creds.PREFIX)), ('txtGeneralUsername', (None, login_creds.USERNAME)), ('txtGeneralPassword', (None, login_creds.PASSWORD))),
                   allow_redirects=False)
        #
        ################################################################
        #
        return s
