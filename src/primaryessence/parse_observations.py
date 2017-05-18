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
    # # Get script used to get video file
    # scripts = soup.findAll("script")
    # for script in scripts:
    #     for script_attr in script.attrs:
    #         if script_attr[0] == 'src':
    #             script_src = script_attr[1]
    #
    # IMAGES
    divs = soup.findAll("div", {"class": "LJItemPrintWrapper"})
    for div in divs:
        id = div.parent.attrMap['id'].replace('ljPrintItemWrapper_', '')
        #
        if not check_history(child_id, id):
            # title
            title = div.contents[1].contents[0]
            title = trimStrings(title)
            #
            img = []
            imgs = div.findAll("img")
            if len(imgs) > 0:
                for i in imgs:
                    #
                    src = False
                    onclick = False
                    #
                    for img_attr in i.attrs:
                        #
                        if img_attr[0] == 'src':
                            src = img_attr[1]
                        #
                        r = s.get(src)
                        if r.ok:
                            img.append(r.content)
            #
            # comment
            comment = div.findAll("div", {"class": "LjItemPrintableCommentWrapper"})
            comment = comment[0].contents[0]
            #
            # Create observation object and add to list
            o.append(ObjObservation(id, title, comment, imgs=img))
    #
    #
    # VIDEOS
    v_imgs = soup.findAll("img", {"src": "/Content/Images/Master/video-placeholder.png"})
    for v_img in v_imgs:
        #
        onclick = False
        #
        for img_attr in v_img.attrs:
            if img_attr[0] == 'onclick':
                onclick = img_attr[1]
        #
        if onclick:
            id = onclick.replace("GetPresignedVideoToPlay('/Observations/GetVideoForBrowserPlay/", "")
            id = id.replace("/{child_id}');".format(child_id=child_id), "")
            #
            if not check_history(child_id, id):
                # title
                # title = v_img.parent.parent.parent.parent.findAll("h4")[0].contents[0]
                title = v_img.parent.parent.parent.parent.contents[1].contents[1].contents[0]
                title = trimStrings(title)
                #
                vid = []
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
                # comment
                comment = v_img.parent.parent.parent.findAll("div", {"class": "ess-comment"})[0].contents[0]
                comment = trimStrings(comment)
                #
                # Create observation object and add to list
                o.append(ObjObservation(id, title, comment, vids=vid))
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