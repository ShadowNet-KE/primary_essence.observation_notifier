import json
from BeautifulSoup import BeautifulSoup
from obj_observation import ObjObservation
from src.history.notification_history import check_history


def find_observations(s, data, child_id):
    #
    soup = BeautifulSoup(data)
    #
    o = []
    #
    div_items = soup.findAll("div", {"class": ["item", "item active"]})
    for item in div_items:
        #
        for div in item.contents:
            #
            try:
                #
                if div.attrMap['id'].startswith('ljPrintItemWrapper_'):
                    #
                    id = div.attrMap['id'].replace('ljPrintItemWrapper_', '')
                    #
                    if not check_history(child_id, id):
                        # title
                        title = div.contents[1].contents[1].contents[0]
                        title = trimStrings(title)
                        #
                        img = []
                        vid = []
                        #
                        imgs = div.findAll("img")
                        if len(imgs) > 0:
                            for i in imgs:
                                #
                                src = False
                                onclick = False
                                #
                                for img_attr in i.attrs:
                                    if img_attr[0] == 'src':
                                        src = img_attr[1]
                                #
                                if bool(src):
                                    r = s.get(src)
                                    if r.ok:
                                        img.append(r.content)
                        else:
                            v_imgs = div.parent.findAll("img", {"src": "/Content/Images/Master/video-placeholder.png"})
                            for v_img in v_imgs:
                                #
                                onclick = False
                                #
                                for img_attr in v_img.attrs:
                                    if img_attr[0] == 'onclick':
                                        onclick = img_attr[1]
                                #
                                if bool(onclick):
                                    # id = onclick.replace("GetPresignedVideoToPlay('/Observations/GetVideoForBrowserPlay/", "")
                                    # id = id.replace("/{child_id}');".format(child_id=child_id), "")
                                    #
                                    if not check_history(child_id, id):
                                        #
                                        url = onclick.replace("GetPresignedVideoToPlay('", "")
                                        url = url.replace("');", "")
                                        url = 'https://www.primaryessence.co.uk' + url
                                        #
                                        r_vid = s.post(url)
                                        #
                                        url_vid = r_vid.content
                                        url_vid = json.loads(url_vid)['preSignedUrl']
                                        #
                                        r = s.get(url_vid)
                                        if r.ok:
                                            vid.append(r.content)
                        #
                        #
                        notes = ''
                        div_othernotes = div.findAll(["h4", "h5", "p"])
                        if len(div_othernotes) > 0:
                            comment = div.findAll("div", {"class": "LjItemPrintableCommentWrapper"})[0]
                            div_othernotes.insert(1, comment)
                            #
                            for item in div_othernotes:
                                if item.name == 'div':
                                    name = 'p'
                                else:
                                    name = item.name
                                notes += '<{tag}>{content}</{tag}>'.format(tag=name,
                                                                           content=item.text)
                        #
                        date_observation = title[-10:]
                        #
                        # Create observation object and add to list
                        o.append(ObjObservation(id, title, notes, img, vid, date_observation))
            except Exception as e:
                pass
    #
    return o


def trimStrings(str):
    #
    to_replace = ['\r\n',
                  '                                        ',
                  '                    ',
                  '                ',
                  '&nbsp;']
    #
    for rep in to_replace:
        str = str.replace(rep, '')
    #
    return str