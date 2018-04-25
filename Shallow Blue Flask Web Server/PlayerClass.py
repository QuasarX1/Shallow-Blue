class Player(object):
    """
        A class representation of player data.
    """

    def __init__(self, playerData):
        self.id: int = None

        self.name: int = None

        self.score: float = None

        self.position: int = None

        self.raiting: int = None

        self.id = playerData[0]
        self.name = playerData[1]
        self.score = playerData[2]
        self.position = playerData[3]
        self.raiting = playerData[4]

    def updatePlayer(self, database):
        """
            Updates the player record in the database
        """
        database.updatePlayer(self)

    def updateScore(self, database, result, scoringValues):
        """
            Ajusts the player's score dependant on the outcome of their pairing result
        """
        self.score += scoringValues[result]

        self.updatePlayer(database)

    def updateRaiting(self, expectedResult, result):
        """
            Calculates the player's new raiting
        """
        score: float = None

        if result == "W": score = 1.0
        elif result == "D": score = 0.5
        elif result == "L": score = 0.0
        else: score = 0.0

        scoreDifference = score - expectedResult

        k: int = None

        if self.raiting < 2400: k = 20
        else: k = 10

        self.raiting = self.raiting + (k * scoreDifference)

        return self.raiting