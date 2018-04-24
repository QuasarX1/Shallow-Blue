import datetime
import PlayerClass

class Event(object):
    """A class representation of the current event in use."""

    def __init__(self, database, eventData):
        self.id: int = None

        self.name: str = None

        self.info: str = None

        self.creatorID: int = None

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
        self.scoring = {"W": float(eventData[9]), "D": float(eventData[10]), "L": float(eventData[11]), "NS": float(eventData[12])}
        
        playersData = database.getPlayers(self.id)

        for playerData in playersData:
            self.players.append(PlayerClass.Player(playerData))

        self.players.sort(key = lambda player: player.position)

    def addPlayer(self, database, userID):
        player = database.getPlayer(userID, self.id)

        if player == None:
            database.addPlayer(userID, self.id)
        else:
            raise ValueError("This user has allready joined this event.")

        self.players.append(PlayerClass.Player(database.getPlayer(userID, self.id)))

        self.sortPlayers()

        self.updatePositions(database)

    def getPlayer(self, playerID):
        for player in self.players:
            if player.id == playerID:
                return player

    def updatePlayers(self, database):
        for player in self.players:
            player.updatePlayer(database)

    def updatePositions(self, database):
        for position in range(1, len(self.players) + 1):
            self.players[position - 1].position = position

        self.updatePlayers(database)

    @staticmethod
    def predictResult(player, oponent):
        return 1 / (1 + float(10) ** ( (player.raiting - oponent.raiting) / 400) )