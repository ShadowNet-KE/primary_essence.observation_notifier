import json
from bs4 import BeautifulSoup
from obj_observation import ObjObservation
from history.notification_history import check_history


def find_observations(s, data, child_id):
    #
    soup = BeautifulSoup(data, "html.parser")
    #
    o = []
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
                                src = i.attrs['src']
                                r = s.get(src)
                                if r.ok:
                                    img.append(r.content)
                            except:
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
                    commentby = div_item_body_notes.find("div", {"class": "ess-comment-by"})
                    #
                    aspects_of_learning = div_item_body_notes[1].find("div", {"class": "ibox-content"})
                    #
################################################################
# TODO - get details of observations held in dict seperately
#
#   <div class ="ibox-content">
#       <h4>Understanding</h4>
#       <ul class ="typical-list">
#           <li>16 - 26 Months - Understands ... </li>
#           <li>8 - 20 Months - Understanding ...</li>
#       </ul>
#       <h4> Shape, space and measure</h4>
#       <ul class ="typical-list">
#           <li>16 - 26 Months - Beginning to understand ...</li>
#       </ul>
#   </div>
################################################################
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
            pass
    #
    return o


def trimStrings(str):
    #
    str = str.replace('\r\n', '')
    str = str.strip()
    #
    return str