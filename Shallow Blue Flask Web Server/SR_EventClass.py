import EventClass
import PlayerClass

class SR_Event(EventClass.Event):
    def __init__(self, database, eventData):
        EventClass.Event.__init__(self, database, eventData)

    def startEvent(self, database):
        self.status = "in progress"

        self.round = 1

        self.sortPlayers()

        if float(int(len(self.players)/2)) != float(len(self.players)/2.0):
            self.addPlayer(database, database.getUser("bye")[0])

        self.updatePositions(database)

        if self.totalRounds == "None":
            if self.eventType == "round robin":
                self.totalRounds = len(self.players) - 1
            else:
                rounds = 1
                counter = 2
                while counter < len(self.players) and rounds <= 7:
                    counter *= 2
                    rounds += 1

                self.totalRounds = rounds

        database.updateEvent(self)

    def sortPlayers(self):
        self.players.sort(key = lambda player: player.raiting, reverse = True)

        self.players.sort(key = lambda player: player.score, reverse = True)

    def createPairings(self, database):
        if self.eventType == "swiss":
            self.sortPlayers()

            scoreBands = []
            currentScoreBand = None

            for player in self.players:
                if player.score != currentScoreBand:# If the current player is in a different score band
                    scoreBands.append([])# Add a new band
                    currentScoreBand = player.score# Update the current score band

                scoreBands[len(scoreBands) - 1].append(player)# Add the current player to the last avalable score band

            pairings = []
            carry = None# Used to store an unpaired player from the last band

            for band in scoreBands:# For each score band
                if carry!= None:# If there is a carried player, add them to the top of the band
                    band.insert(0, carry)

                if len(band) != 1:
                    for i in range(0, int(len(band)/2)):
                        pairings.append((band[i], band[i + int(len(band)/2)]))

                if float(int(len(band)/2)) != len(band)/2.0:# If the band has an odd number of players
                    carry = band[len(band) - 1]# Make the remaining player the carried player
                else:
                    carry = None# Otherwise, ensure the carry is empty

            # Add each pairing to the database
            for i in range(0, len(pairings)):
                self.addPairing(database, i, pairings[i][0], pairings[i][1])

        else:# Round Robin
            self.players.sort(key = lambda player: player.id)# Sort players into same order each time

            # Get players into known starting positions-------------------------------------------------------------------------
            stationaryPlayer = None
            set1 = []
            set2 = []

            for i in range(0, len(self.players)):
                if i == 0:
                    stationaryPlayer = self.players[i]
                elif i/2 == float(int(i/2)):
                    set1.append(self.players[i])
                else:
                    set2.append(self.players[i])

            # Modify positions to match round----------------------------------------------------------------------------------
            for i in range(0, self.round - 1):
                temp1 = []
                temp2 = []

                for item in set1:
                    temp1.append(item)
                for item in set2:
                    temp2.append(item)

                for i in range(0, len(temp2)):
                    if i != 0:
                        set2[i - 1] = temp2[i]
                    else:
                        set1[0] = temp2[0]

                for i in range(0, len(temp1)):
                    if i != len(temp1) - 1:
                        set1[i + 1] = temp1[i]
                    else:
                        set2[len(set2) - 1] = temp1[i]

            # Create pairings----------------------------------------------------------------------------------------------------
            pairings = []

            for counter in range(0, len(set2)):
                if counter != 0:
                    pairings.append((set1[counter - 1], set2[counter]))
                else:
                    pairings.append((stationaryPlayer, set2[counter]))

            # Add each pairing to the database----------------------------------------------------------------------------------
            for i in range(0, len(pairings)):
                self.addPairing(database, i, pairings[i][0], pairings[i][1])

    def addPairing(self, database, board, bPlayer, wPlayer):
        database.addSRPairing(self.id, self.round, board, bPlayer, wPlayer, EventClass.Event.predictResult(bPlayer, wPlayer), EventClass.Event.predictResult(wPlayer, bPlayer))

    def getPairings(self, database):
        return database.getSR_Pairings(self.id, self.round)

    def updatePairing(self, database, boardNumber, bPlayer, bResult, wPlayer, wResult):
        bPlayer.updateScore(database, bResult, self.scoring)
        wPlayer.updateScore(database, wResult, self.scoring)
        
        database.updateSR_Pairing(self.round, bPlayer, bResult, wPlayer, wResult)

        if len(database.getUnfinishedPairings(self)) == 0:
            isEndOfEvent = self.endRound(database)

            if isEndOfEvent == True: return "End of event"
            else: return "End of round"

        else: return None

    #def updatePositions(self, database):
    #    for position in range(1, len(self.players) + 1):
    #        self.players[position - 1].position = position

    #    self.updatePlayers(database)

    def endRound(self, database):
        self.sortPlayers()

        self.updatePositions(database)

        if self.round != self.totalRounds:
            self.round += 1

            database.updateEvent(self)
        else:
            try:
                self.endEvent(database, False)
            except ValueError:
                self.endEvent(database, True)

            return True

    def endEvent(self, database, useOponentsScores):
        self.sortPlayers()

        while True:
            changed = False

            for counter in range(0, len(self.players)):
                if counter != len(self.players) - 1:
                    if self.players[counter].score == self.players[counter + 1].score:
                        if useOponentsScores == False:
                            sum1 = self.sumOfProgressiveScores(database, self.players[counter])
                            sum2 = self.sumOfProgressiveScores(database, self.players[counter + 1])
                        else:
                            sum1 = self.sumOfOponentsScores(self.players[counter])
                            sum2 = self.sumOfOponentsScores(self.players[counter + 1])

                        if sum2 > sum1:
                            carry = self.players.pop(counter + 1)
                            self.players.insert(counter, carry)

                            changed = True

            if changed == False: break

        #If SoPS is used and the top 2 have the same SoPS, use SoOS
        if useOponentsScores == False and self.sumOfProgressiveScores(database, self.players[0]) == self.sumOfProgressiveScores(database, self.players[1]):
            raise ValueError("Sum of Progressive Scores didn't produce a clear winner.")

        self.status = "finished"

        self.updatePositions(database)

        database.updateEvent(self)

    def sumOfProgressiveScores(self, database, player):
        results = database.getPlayerResults(player.id)

        SoPS = 0.0
        score = 0.0

        for round in results:
            if round[1] == "W":
                score = score + 1.0

            elif round[1] == "D":
                score = score + 0.5

            SoPS = SoPS + score

        return SoPS


    def sumOfOponentsScores(self, database, player):

        def sumOpponentsScores(database, opponentID):
            results = database.getPlayerResults(opponentID)

            score = 0.0
            
            for round in results:
                if round[1] == "W":
                    score = score + 1.0
                   
                if round[1] == "D":
                    score = score + 0.5

        results = database.getAdvancedPlayerResults(player.id)

        SoOS = 0.0

        for round in results:
            if round[1] == "W":
                SoOS = SoOS + sumOpponentsScores(database, round[2])
            
            elif round[1] == "D":
                SoOS = SoOS + 0.5 * sumOpponentsScores(database, round[2])

        return SoOS