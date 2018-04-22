import EventClass

class Ladder_Event(EventClass.Event):
    def __init__(self, eventData):
        EventClass.Event.__init__(self, eventData)

    def startEvent(self, database):
        self.status = "in progress"

    def sortPlayers(self):
        self.players.sort(key = lambda player: player.position, reverse = True)

    def addPairing(self, database, match, bPlayer, wPlayer):
        activePairings = database.getUnfinnishedPairings(self)

        valid = True

        # Check that neithr of the players is allready paired
        for pairing in activePairings:
            if bPlayer.id in pairing or wPlayer.id in pairing:
                valid = False
                break

        if valid:
            database.addLadder_Pairing(self.id, match, bPlayer, wPlayer)
        else:
            raise ValueError("One of the players is currently paired.")

        self.round += 1

        database.updateEvent(self)

    def getPairings(self, database):
        return database.getLadder_Pairings(self.id, self.round)

    def updatePairing(self, database, match, bPlayer, bResult, wPlayer, wResult):
        # Swap positions of the players if nessessary
        if bPlayer.position < wPlayer.raitipositionng and bResult == "W" or wPlayer.position < bPlayer.raitipositionng and wResult == "W":
            storePosition = bPlayer.position
            bPlayer.position = wPlayer.position
            wPlayre.position = storePosition

            bPlayer.updatePlayer()
            wPlayer.updatePlayer()

        # Update the pairing and the user's raitings
        database.updateLadder_Pairing(match, bPlayer, bResult, wPlayer, wResult)

    def endEvent():
        self.status = "finnished"