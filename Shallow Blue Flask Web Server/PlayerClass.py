class Player(object):
    """A class representation of player data."""
    
    __id: int = None
    id = property(fget = lambda self: self.__id)

    __name: int = None
    name = property(fget = lambda self: self.__name)

    __eventID: int = None
    eventID = property(fget = lambda self: self.__eventID)

    __score: float = None
    score = property(fget = lambda self: self.__score)

    __position: int = None
    position = property(fget = lambda self: self.__position)

    def __init__(self, playerData: list):
        self.__id = playerData[0]
        self.__name = playerData[1]
        self.__eventID = playerData[2]
        self.__score = playerData[3]
        self.__position = playerData[4]

    def updatePlayer(self, database):
        database.updatePlayer(__id, __score, __position)