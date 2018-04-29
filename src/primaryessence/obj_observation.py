

class ObjObservation:

    def __init__(self, id, title, comment, commentby, aol, imgs, vids, date_observation):
        self._id = id
        self._title = title
        self._comment = comment
        self._commentby = commentby
        self._aol = aol
        self._imgs = imgs
        self._vids = vids
        self._date_observation = date_observation

    def id(self):
        return self._id

    def title(self):
        return self._title

    def comment(self):
        return self._comment

    def commentby(self):
        return self._commentby

    def aol(self):
        return self._aol

    def imgs(self):
        return self._imgs

    def vids(self):
        return self._vids

    def date_observation(self):
        return self._date_observation
