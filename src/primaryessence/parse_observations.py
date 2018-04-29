import json
from bs4 import BeautifulSoup
from obj_observation import ObjObservation
from history.notification_history import check_history
from log.log import log_internal
from resources.global_resources.logs import logException

def find_observations(s, data, child_id):
    #
    soup = BeautifulSoup(data, "html.parser")
    #
    o = []
    #
    title = ''
    #
    data = soup.find("div", {"id": "ljCarousel"})  # Get carousel div that contains all observations
    div_items = data.findAll("div", {"class": ["item", "item active"]})
    #
    for item in div_items:
        #
        div_item_title = item.contents[1]
        div_item_body = item.contents[3]
        div_item_printwrapper = item.contents[5]
        #
        try:
            #
            if div_item_printwrapper.get('id').startswith('ljPrintItemWrapper_'):
                #
                id = div_item_printwrapper.get('id').replace('ljPrintItemWrapper_', '')
                #
                if not check_history(child_id, id):
                    # title
                    title = div_item_title.find("h4")
                    title = title.contents[0]
                    title = trimStrings(title)
                    #
                    div_item_body_media = div_item_body.contents[1]
                    div_item_body_notes = div_item_body.contents[3]
                    #
                    img = []
                    vid = []
                    #
                    imgs = div_item_body_media.findAll("img")
                    if len(imgs) > 0:
                        for i in imgs:
                            #
                            try:
                                onclick = i.attrs['onclick']
                                src = onclick.replace("ShowInnerLJItemImage('innerLJItemImgHolder_{id}', '".format(id=id), "")
                                src = src.replace("');", "")
                                r = s.get(src)
                                if r.ok:
                                    img.append(r.content)
                            except Exception as e:
                                pass
                    else:
                        v_imgs = div_item_body_media.parent.findAll("img", {"src": "/Content/Images/Master/video-placeholder.png"})
                        for v_img in v_imgs:
                            #
                            try:
                                onclick = v_img.attrs['onclick']
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
                            except:
                                pass
                    #
                    #
                    comment = div_item_body_notes.find("div", {"class": "ess-comment"})
                    if comment is None:
                        comment = ''
                    else:
                        comment = trimStrings(comment.contents[0])
                    #
                    commentby = div_item_body_notes.find("div", {"class": "ess-comment-by"})
                    if commentby is None:
                        commentby = ''
                    else:
                        commentby = trimStrings(commentby.contents[0]).replace('Comment by: ', '')
                    #
                    try:
                        _aol = div_item_body_notes.contents[3].find("div", {"class": "ibox-content"})
                        _aol_header = _aol.findAll("h4")
                        _aol_desc = _aol.findAll("ul")
                        #
                        aspects_of_learning = {}
                        #
                        a = 0
                        while a < len(_aol_header):
                            _aol_desc_tags = _aol_desc[a].findAll("li")
                            _aol_desc_list = []
                            for l in _aol_desc_tags:
                                _aol_desc_list.append(trimStrings(l.getText()))
                            #
                            aspects_of_learning[_aol_header[a].contents[0]] = _aol_desc_list
                            #
                            a += 1
                        #
                    except:
                        aspects_of_learning = {}
                    #
                    date_observation = title[-10:]
                    #
                    # Create observation object and add to list
                    o.append(ObjObservation(id, title,
                                            comment, commentby,
                                            aspects_of_learning,
                                            img, vid,
                                            date_observation))
        except Exception as e:
            log_internal(logException, 'parsing of observation',
                         description='Error running operation - {title}'.format(title=title),
                         exception=e)
    #
    return o


def trimStrings(str):
    #
    str = str.replace('\r\n', '')
    str = str.strip()
    #
    return str