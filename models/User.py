class User:
    def __init__(self, userName, hashedPassword, creation_date):
        self._id = None
        self._userName = userName
        self._hashedPassword = hashedPassword
        self._creation_date = creation_date

    #Getter
    @property
    def id(self):
        return self._id

    @property
    def userName(self):
        return self._userName

    @property
    def hashedPassword(self):
        return self._hashedPassword

    @property
    def creation_date(self):
        return self._creation_date




