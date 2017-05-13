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
        img = []
        imgs = div.findAll("img")
        if len(imgs) > 0:
            for i in imgs:
                for img_attr in i.attrs:
                    if img_attr[0] == 'src':
                        r = s.get(img_attr[1])
                        if r.ok:
                            img.append(r.content)
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
