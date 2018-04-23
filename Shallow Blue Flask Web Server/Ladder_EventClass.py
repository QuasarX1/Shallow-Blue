import EventClass

class Ladder_Event(EventClass.Event):
    def __init__(self, database, eventData):
        EventClass.Event.__init__(self, database, eventData)

    def startEvent(self, database):
        self.status = "in progress"
        self.round = 1

        self.players.sort(key = lambda player: player.raiting, reverse = True)

        self.updatePositions(database)

        database.updateEvent(self)

    def sortPlayers(self):
        self.players.sort(key = lambda player: player.position, reverse = True)

    def addPairing(self, database, bPlayer, wPlayer):
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
        return database.getLadder_Pairings(self.id)

    def updatePairing(self, database, match, bPlayer, bResult, wPlayer, wResult):
        # Swap positions of the players if nessessary
        if bPlayer.position > wPlayer.position and bResult == "W" or wPlayer.position > bPlayer.position and wResult == "W":
            storePosition = bPlayer.position
            bPlayer.position = wPlayer.position
            wPlayer.position = storePosition

            bPlayer.updatePlayer(database)
            wPlayer.updatePlayer(database)

        # Update the pairing and the user's raitings
        database.updateLadder_Pairing(match, bPlayer, bResult, wPlayer, wResult)

    def endEvent():
        self.status = "finished"