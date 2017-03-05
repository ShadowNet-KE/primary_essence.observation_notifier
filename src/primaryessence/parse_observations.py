from BeautifulSoup import BeautifulSoup
from obj_observation import ObjObservation


def find_observations(s, data):
    #
    soup = BeautifulSoup(data)
    #
    title_replace = ['\r\n',
                     '                                        ',
                     '&nbsp;']
    #
    o = []
    #
    divs = soup.findAll("div", {"class": "LJItemPrintWrapper"})
    for div in divs:
        id = div.parent.attrMap['id'].replace('ljPrintItemWrapper_', '')
        #
        # title
        title = div.contents[1].contents[0]
        for rep in title_replace:
            title = title.replace(rep, '')
        #
        # img
        img = ''
        for img_attr in div.findAll("img")[0].attrs:
            if img_attr[0] == 'src':
                r = s.get(img_attr[1])
                if r.ok:
                    img = r.content
                break
        #
        # comment
        comment = div.findAll("div", {"class": "LjItemPrintableCommentWrapper"})
        comment = comment[0].contents[0]
        #
        # Create observation object and add to list
        o.append(ObjObservation(id, title, comment, img))
    #
    return o
