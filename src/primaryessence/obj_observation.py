

class ObjObservation:

    def __init__(self, id, title, notes, imgs=False, vids=False):
        self._id = id
        self._title = title
        self._notes = notes
        self._imgs = imgs
        self._vids = vids

    def id(self):
        return self._id

    def title(self):
        return self._title

    def notes(self):
        return self._notes

    def imgs(self):
        return self._imgs

    def vids(self):
        return self._vids