

class ObjObservation:

    def __init__(self, id, title, comment, img):
        self._id = id
        self._title = title
        self._comment = comment
        self._img = img

    def id(self):
        return self._id

    def title(self):
        return self._title

    def comment(self):
        return self._comment

    def img(self):
        return self._img