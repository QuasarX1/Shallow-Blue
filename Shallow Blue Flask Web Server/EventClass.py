import datetime
import PlayerClass
import math

class Event(object):
    """A class representation of the current event in use."""

    def __init__(self, database, eventData):
        self.id: int = None

        self.name: str = None

        self.info: str = None

        self.creatorID: float = None

        self.eventType: str = None

        self.startDateTime: datetime.datetime = None
        
        self.status: str = None

        self.round: int = None

        self.totalRounds: int = None
        
        self.scoring: dict = {}
        
        self.players: list = []

        self.id = eventData[0]
        self.name = eventData[1]
        self.info = eventData[2]
        self.creatorID = eventData[3]
        self.eventType = eventData[4]
        self.startDateTime = datetime.datetime.fromtimestamp(eventData[5])
        self.status = eventData[6]
        self.round = eventData[7]
        self.totalRounds = eventData[8]
        self.scoring = {"W": int(eventData[9]), "D": int(eventData[10]), "L": int(eventData[11]), "NS": int(eventData[12])}
        
        playersData = database.getPlayers(self.id)

        for playerData in playersData:
            self.players.append(PlayerClass.Player(playerData))

    def addPlayer(self, database, userID):
        player = database.getPlayer(self.id, userID)

        if player == None:
            database.addPlayer(self.id, userID)
        else:
            raise ValueError("This user has allready joined this event.")

        self.players.append(PlayerClass.Player(database.getPlayer(self.id, userID)))

        self.sortPlayers()

    def updatePlayers(self, database):
        for player in self.players:
            player.updatePlayer(database)

    @staticmethod
    def predictResult(player, oponent):
        return 1 / (1 + 10 ^ ( (player.raiting - oponent.raiting) / 400) )