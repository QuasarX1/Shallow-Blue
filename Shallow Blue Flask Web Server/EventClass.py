import datetime

class Event(object):
    """A class representation of the current event in use."""

    __id: int = None
    id = property(fget = lambda self: self.__id)

    __name: str = None
    name = property(fget = lambda self: self.__name)

    __info: str = None
    info = property(fget = lambda self: self.__info)

    __creatorID: float = None
    creatorID = property(fget = lambda self: self.__creatorID)

    __eventType: str = None
    eventType = property(fget = lambda self: self.__eventType)

    __startDateTime: datetime.datetime = None
    startDateTime = property(fget = lambda self: self.__startDateTime)

    __status: str = None
    status = property(fget = lambda self: self.__status)

    __scoring: list = []
    startDateTime = property(fget = lambda self: self.__startDateTime)

    __players: list = []
    players = property(fget = lambda self: self.__players)

    def __init__(self):
        pass

    def getPlayers(self):
        pass

    def addPlayer(self, database, userID):
        pass

    def createPairings(self):
        raise NotImplementedError

    def addPairing(self):
        raise NotImplementedError