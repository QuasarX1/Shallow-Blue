import EventClass

class Ladder_Event(EventClass.Event):
    """
        Inherits "Event"

        Used to interact with ladder events
    """
    def __init__(self, database, eventData):
        EventClass.Event.__init__(self, database, eventData)

    def startEvent(self, database):
        """
            Sets up the event to allow pairings
        """
        self.status = "in progress"
        self.round = 1

        # Sorts the players on decending raiting
        self.players.sort(key = lambda player: player.raiting, reverse = True)

        self.updatePositions(database)

        database.updateEvent(self)

    def sortPlayers(self):
        """
            Sorts the players on their position
        """
        self.players.sort(key = lambda player: player.position, reverse = True)

    def addPairing(self, database, bPlayer, wPlayer):
        """
            Attempts to add a pairing to the database
        """
        activePairings = database.getUnfinishedPairings(self)

        valid = True

        # Check that neithr of the players is allready paired
        for pairing in activePairings:
            if bPlayer.id == pairing[2] or wPlayer.id == pairing[2]:
                valid = False
                break

        if valid:
            database.addLadderPairing(self.id, self.round, bPlayer, wPlayer, EventClass.Event.predictResult(bPlayer, wPlayer), EventClass.Event.predictResult(wPlayer, bPlayer))
        else:
            raise ValueError("One of the players is currently paired.")

        self.round += 1

        database.updateEvent(self)

    def getPairings(self, database):
        """
            Returns all unfinished pairings
        """
        return database.getLadder_Pairings(self.id)

    def updatePairing(self, database, match, bPlayer, bResult, wPlayer, wResult):
        """
            Updates the players and the database with the result of a pairing and its implications
        """
        # Swap positions of the players if nessessary
        if bPlayer.position > wPlayer.position and bResult == "W" or wPlayer.position > bPlayer.position and wResult == "W":
            storePosition = bPlayer.position
            bPlayer.position = wPlayer.position
            wPlayer.position = storePosition

            bPlayer.updatePlayer(database)
            wPlayer.updatePlayer(database)

        # Update the pairing and the user's raitings
        database.updateLadder_Pairing(match, bPlayer, bResult, wPlayer, wResult)

    def endEvent(self, database):
        """
            Ends the ladder event
            Not currently implemented
        """
        self.status = "finished"

        database.updateEvent(self)