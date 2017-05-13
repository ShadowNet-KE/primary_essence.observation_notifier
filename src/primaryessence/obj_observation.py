

class ObjObservation:

    def __init__(self, id, title, comment, imgs):
        self._id = id
        self._title = title
        self._comment = comment
        self._imgs = imgs

    def id(self):
        return self._id

    def title(self):
        return self._title

    def comment(self):
        return self._comment

    def imgs(self):
        return self._imgs