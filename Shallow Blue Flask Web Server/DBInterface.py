import datetime
import hashlib
import os
import shutil
import sqlite3
import sys

class DBInterface(object):
    """
    Creates an object for interfacing with the application's database.
    """

    # Atributes------------------------------------------------------------------------------------------------------------
    _location = None
    _connection = None
    _cursor = None

    # Decorator to handel the connection-----------------------------------------------------------------------------------
    def connect(method):
        def wrapper(*args, **kwargs):
            args[0]._connection = sqlite3.connect(args[0]._location)
            args[0]._cursor = args[0]._connection.cursor()

            result = method(*args, **kwargs)

            args[0]._cursor.close()
            args[0]._connection.close()

            return result

        return wrapper

    # Methods--------------------------------------------------------------------------------------------------------------
    def __init__(self, pathToLocationFile, applicationRootDirectory):
        """
        Paramiters:
            pathToLocationFile - string - the relitive path to the database location file
        """
        # Read in the db location------------------------------------------------------------------------------------------
        deafultPath = "Data"
        deafultName = "ShallowBlueDatabase.db"
        alternatePath = None
        alternateName = None

        try:
            file = open(pathToLocationFile, "r")
            alternatePath = file.readline()[0:-1]
            alternateName = file.readline()
            file.close()

        # Handle any error with the reading of the file--------------------------------------------------------------------
        except IOError as e:
            choice = ""

            while True:
                choice = input("""The location file for the database can't be found or is corrupt.\n
If you wish a replacement file to be created, please return \"y\".\n
If you wish to close the application and deal with the issue yourself, please return \"n\".\n
---> """)

                if choice == "y" or choice == "n":
                    break

                else:
                    print("You muse enter \"y\" or \"n\"!")

            if choice == "n":
                print(e)
                sys.exit()

            else:
                file = None

                if os.path.exists(pathToLocationFile):
                    file = open(pathToLocationFile, "w")

                else:
                    file = open(pathToLocationFile, "a")

                alternatePath = ""
                alternateName = ""

                file.write(alternatePath + "\n")
                file.write(alternateName)
                file.close()

        # Set the value of the db path-------------------------------------------------------------------------------------
        pathToDB = None
        nameOfDB = None

        if alternatePath == "":
            pathToDB = os.path.join(applicationRootDirectory, deafultPath)
            nameOfDB = deafultName

        elif not os.path.exists(alternatePath):
            while True:
                choice = input("""The alternate location of the database can't be found.\n
If you wish to atempt to connect to/create a database in the deafult location, please return \"y\".\n
If you wish to close the application and deal with the issue yourself, please return \"n\".\n
---> """)

                if choice == "y" or choice == "n":
                    break

                else:
                    print("You muse enter \"y\" or \"n\"!")

            if choice == "n":
                print("Alternate database location not found. Path provided was: " + alternatePath)
                sys.exit()

            else:
                pathToDB = os.path.join(applicationRootDirectory, deafultPath)
                nameOfDB = deafultName

        else:
            pathToDB = alternatePath
            nameOfDB = alternateName
        
        # Connect to the db file-------------------------------------------------------------------------------------------
        makeTables = False

        if not os.path.exists(os.path.join(pathToDB, nameOfDB)):
            makeTables = True

        self._location = os.path.join(pathToDB, nameOfDB)

        self._connection = sqlite3.connect(self._location)# Connects to the database specified by the path in the variable "pathToDB"
        print("Database connection created to " + self._location)
        self._cursor = self._connection.cursor()# Creates a cursor object that is used to manipulate the database
        print("Database cursor created")

        self._cursor.execute("PRAGMA foreign_keys = ON")# Force referential integrity when creating, modifying and deleting records

        self._cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        tableNames = self._cursor.fetchall()# Retrives a list of all the tables in the database

        if tableNames == []:# If the database is blank
            makeTables = True

        elif tableNames != [('user',), ('sqlite_sequence',), ('event',), ('player',), ('sr_pairing',), ('ladder_pairing',), ("join_event_requests",)]:# If the list of tables is incorrect
            while True:
                choice = input("""The database """ + nameOfDB + """ contained a list of tables that is either missing nessessary tables or has other tables. This could mean that the database location specified is wrong and this database doesn't belong to this application.\n
If you wish to continue with this database, please return \"y\". Please note that any nessessary tables that currently don't exist will be created if you chose to do so.\n
If you wish to close the application and deal with the issue yourself, please return \"n\".\n
---> """)

                if choice == "y" or choice == "n":
                    break

                else:
                    print("You muse enter \"y\" or \"n\"!")

            if choice == "n":
                print("The list of tables in the database was incorrect. The tables located were: " + str(tableNames))
                sys.exit()

            else:
                makeTables = True

        if makeTables == True:
            self.createTables()# Create the tables in the database
#        if tableNames == []:# If the database is blank
#            makeTables = True

#        elif tableNames != [('user',), ('sqlite_sequence',), ('event',), ('player',), ('sr_pairing',), ('ladder_pairing',)]:# If the list of tables is incorrect
#            while True:
#                choice = input("""The database """ + nameOfDB + """ contained a list of tables that is either missing nessessary tables or has other tables. This could mean that the database location specified is wrong and this database doesn't belong to this application.\n
#If you wish to continue with this database, please return \"y\". Please note that any nessessary tables that currently don't exist will be created if you chose to do so.\n
#If you wish to close the application and deal with the issue yourself, please return \"n\".\n
#---> """)

#                if choice == "y" or choice == "n":
#                    break

#                else:
#                    print("You muse enter \"y\" or \"n\"!")

#            if choice == "n":
#                print("The list of tables in the database was incorrect. The tables located were: " + str(tableNames))
#                sys.exit()

#            else:
#                makeTables = True

#        if makeTables == True:
#            self.createTables()# Create the tables in the database

        self._cursor.close()
        self._connection.close()

    def createTables(self):
        # user table
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name varchar(255) NOT NULL UNIQUE,
                first_name varchar(255),
                last_name varchar(255),
                password varchar(255),
                email varchar(255),
                dob datetime,
                raiting int
            )"""
        )

        # event table
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS event (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name varchar(255) NOT NULL,
                event_info text NOT NULL,
                event_creator_id int NOT NULL,
                event_type varchar(255) NOT NULL,
                event_start_datetime datetime NOT NULL,
                event_status varchar(255) NOT NULL,
                round_number int NOT NULL,
                total_rounds int,
                win_score real NOT NULL,
                draw_score real NOT NULL,
                lose_score real NOT NULL,
                no_show_score real NOT NULL,
                FOREIGN KEY (event_creator_id) REFERENCES user(user_id)
            )"""
        )

        # player table
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS player (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id int NOT NULL,
                event_id int NOT NULL,
                score real NOT NULL DEFAULT 0,
                position int NOT NULl DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES user(user_id),
                FOREIGN KEY (event_id) REFERENCES event(event_id)
            )"""
        )

        # sr_pairing table
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS sr_pairing (
                event_id int NOT NULL,
                round_number int NOT NULL,
                board_id int NOT NULL,
                player_id int NOT NULL,
                colour varchar(255) NOT NULL,
                expected_result real NOT NULL,
                result varchar(255),
                PRIMARY KEY (round_number, board_id, player_id),
                FOREIGN KEY (event_id) REFERENCES event(event_id),
                FOREIGN KEY (player_id) REFERENCES player(player_id)
            )"""
        )

        # ladder_pairing table
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS ladder_pairing (
                event_id int NOT NULL,
                match_number int NOT NULL,
                player_id int NOT NULL,
                colour varchar(255) NOT NULL,
                expected_result real NOT NULL,
                result varchar(255),
                PRIMARY KEY (match_number, player_id),
                FOREIGN KEY (event_id) REFERENCES event(event_id),
                FOREIGN KEY (player_id) REFERENCES player(player_id)
            )"""
        )

        # join_event_requests table
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS join_event_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id int NOT NULL,
                user_id int NOT NULL,
                status varchar(255) NOT NULL,
                FOREIGN KEY (event_id) REFERENCES event(event_id),
                FOREIGN KEY (user_id) REFERENCES user(user_id)
            )"""
        )

        # Add admin user
        self._cursor.execute("SELECT user_id FROM user WHERE user_name = 'admin'")
        if self._cursor.fetchall() == []:# If the admin user dosen't allready exist
            self._cursor.execute(
                """INSERT INTO user (
                    user_name,
                    password,
                    raiting
                )
                VALUES (
                    'admin',
                    '%s',
                    '1200'
                )"""
                %(hashlib.sha512("admin".encode('utf8')).hexdigest())
            )

        # Add bye user
        self._cursor.execute("SELECT user_id FROM user WHERE user_name = 'bye'")
        if self._cursor.fetchall() == []:# If the bye user dosen't allready exist
            self._cursor.execute(
                """INSERT INTO user (
                    user_name,
                    raiting
                )
                VALUES (
                    'bye',
                    '0'
                )"""
            )

        # Save the changes to the database
        self._connection.commit()

    @connect
    def addUser(self, userName, firstName, lastName, password, email, dob):
        self._cursor.execute(
            """INSERT INTO user(
                user_name, first_name, last_name, password, email, dob, raiting
            )
            VALUES(
                '%s', '%s', '%s', '%s', '%s', '%s', '1200'
            )"""
            %(userName, firstName, lastName, password, email, dob)
        )

        self._connection.commit()

    @connect
    def addEvent(self, name, info, creatorID, type, startDateTime, totalRounds, winScore, drawScore, loseScore, noShowScore):
        self._cursor.execute(
            """
                INSERT INTO event(
                    event_name,
                    event_info,
                    event_creator_id,
                    event_type,
                    event_start_datetime,
                    event_status,
                    round_number,
                    total_rounds,
                    win_score,
                    draw_score,
                    lose_score,
                    no_show_score
                )
                VALUES(
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    'registration',
                    '0',
                    '%s',
                    '%s',
                    '%s',
                    '%s',
                    '%s'
                )
            """
            %(name, info, creatorID, type, startDateTime, totalRounds, winScore, drawScore, loseScore, noShowScore)
        )

        self._connection.commit()

    @connect
    def addPlayer(self, userID, eventID):
        self._cursor.execute(
            """
                INSERT INTO player(
                    user_id, event_id, score, position
                )
                VALUES(
                    '%s', '%s', '0', '10000'
                )
            """
            %(userID, eventID)
        )

        self._connection.commit()

    @connect
    def addNoUserPlayer(self, userName):
        self._cursor.execute(
            """
                INSERT INTO user(user_name, raiting)
                VALUES('%s', '1200')
            """
            %(userName)
        )

        self._connection.commit()

    @connect
    def addSRPairing(self, eventID, round, board, bPlayer, wPlayer, bExpectedResult, wExpectedResult):
        self._cursor.execute(
            """
                INSERT INTO 'sr_pairing'(
                    event_id, round_number, board_id, player_id, expected_result, colour
                )
                VALUES(
                    '%s', '%s', '%s', '%s', '%s', 'black'
                )
            """
            %(eventID, round, board, bPlayer.id, bExpectedResult)
        )

        self._cursor.execute(
            """
                INSERT INTO 'sr_pairing'(
                    event_id, round_number, board_id, player_id, expected_result, colour
                )
                VALUES(
                    '%s', '%s', '%s', '%s', '%s', 'white'
                )
            """
            %(eventID, round, board, wPlayer.id, wExpectedResult)
        )

        self._connection.commit()

    @connect
    def addLadderPairing(self, eventID, match, bPlayer, wPlayer, bExpectedResult, wExpectedResult):
        self._cursor.execute(
            """
                INSERT INTO 'ladder_pairing'(
                    event_id, match_number, player_id, expected_result, colour
                )
                VALUES(
                    '%s', '%s', '%s', '%s', 'black'
                )
            """
            %(eventID, match, bPlayer.id, bExpectedResult)
        )

        self._cursor.execute(
            """
                INSERT INTO 'ladder_pairing'(
                    event_id, match_number, player_id, expected_result, colour
                )
                VALUES(
                    '%s', '%s', '%s', '%s', 'white'
                )
            """
            %(eventID, match, wPlayer.id, wExpectedResult)
        )

        self._connection.commit()

    @connect
    def addJoinRequest(self, event_id, user_id):
        self._cursor.execute(
            """
                INSERT INTO join_event_requests(
                    event_id, user_id, status
                )
                VALUES(
                    '%s', '%s', 'Request Sent'
                )
            """
            %(event_id, user_id)
        )
        
        self._connection.commit()

    @connect
    def getUser(self, userName):
        """
        Retrives a user's data from the database.
        Paramiters:
            userName - the user's username
        """
        self._cursor.execute(
            """
                SELECT *
                FROM user 
                WHERE user_name = '%s'
            """
            % (userName)
        )

        return self._cursor.fetchone()

    @connect
    def getUserLogin(self, userName, password):
        """
        Retrives a user's id and names from the database if their login details are correct.
        Paramiters:
            userName - the user's username
            password - the user's password
        """
        self._cursor.execute(
            """SELECT user_id, user_name, first_name, last_name 
            FROM user 
            WHERE user_name = '%s' AND password = '%s'"""
            % (userName, password)
        )

        return self._cursor.fetchone()

    @connect
    def getUsernames(self):
        """
        Retrives all of the usernames from the user table.
        """
        self._cursor.execute(
            """SELECT user_name
            FROM user"""
        )

        results = self._cursor.fetchall()

        for i in range(0, len(results)):
            results[i] = results[i][0]

        return results

    @connect
    def getEvent(self, eventID):
        self._cursor.execute(
            """
                SELECT *
                FROM event
                WHERE event_id = '%s'
            """
            %(eventID)
        )

        return self._cursor.fetchone()

    @connect
    def getEventListings(self):
        self._cursor.execute(
            """SELECT event_id, event_name, event_start_datetime, event_info, event_status, event_type
            FROM event"""
        )

        return self._cursor.fetchall()

    @connect
    def getPlayer(self, userID, eventID):
        """
        Retrives a player from the player table using their user id and the event id.
        """
        self._cursor.execute(
            """
                SELECT player_id, user_name, score, position, raiting
                FROM user AS u OUTER LEFT JOIN player AS p
                ON u.user_id = p.user_id
                WHERE p.user_id = '%s' AND p.event_id = '%s'
            """
            %(userID, eventID)
        )

        return self._cursor.fetchone()

    @connect
    def getPlayers(self, eventID):
        """
        Retrives all of the players in an event from the player table.
        """
        self._cursor.execute(
            """SELECT player_id, user_name, score, position, raiting
            FROM user AS u OUTER LEFT JOIN player AS p
            ON u.user_id = p.user_id
            WHERE event_id = '%s'"""
            %(eventID)
        )

        return self._cursor.fetchall()

    @connect
    def getPlayerResults(self, playerID):
        self._cursor.execute(
            """
                SELECT round_number, result
                FROM sr_pairing
                WHERE player_id = '%s'
            """
            %(playerID)
        )

        results = self._cursor.fetchall()
        results.sort(key = lambda round: round[0], reverse = True)

        return results

    @connect
    def getAdvancedPlayerResults(playerID):
        self._cursor.execute(
            """
                SELECT 1.round_number, 1.result, 2.player_id
                FROM sr_pairing AS 1 SELF JOIN  sr_pairing AS 2
                ON 1.board_id = 2.board_id
                WHERE 1.player_id = '%s'
            """
            %(playerID)
        )

        results = self._cursor.fetchall()
        results.sort(key = lambda round: round[0], reverse = True)

        return results    

    @connect
    def getSR_Pairings(self, eventID, roundNumber):
        self._cursor.execute(
            """
                SELECT t1.board_id, t1.player_id, t2.player_id, t1.user_name, t2.user_name, t1.colour, t2.colour, t1.expected_result, t1.result, t2.expected_result, t2.result
                FROM (
                    SELECT *
                    FROM sr_pairing AS sr
                    JOIN (
                        SELECT player_id, user_name
                        FROM player AS p JOIN user AS u
                        ON p.user_id = u.user_id
                    ) AS pu
                    ON sr.player_id = pu.player_id
                ) As t1
                JOIN (
                    SELECT *
                    FROM sr_pairing AS sr
                    JOIN (
                        SELECT player_id, user_name
                        FROM player AS p JOIN user AS u
                        ON p.user_id = u.user_id
                    ) AS pu
                    ON sr.player_id = pu.player_id
                ) As t2
                ON t1.event_id = t2.event_id AND t1.round_number = t2.round_number AND t1.board_id = t2.board_id
                WHERE t1.event_id = '%s' AND t1.round_number = '%s' AND t1.player_id <> t2.player_id AND t1.colour = 'black'
            """
            %(eventID, roundNumber)
        )

        return self._cursor.fetchall()

    @connect
    def getLadder_Pairings(self, eventID):
        self._cursor.execute(
            """
                SELECT t1.match_number, t1.player_id, t2.player_id, t1.user_name, t2.user_name, t1.colour, t2.colour, t1.expected_result, t1.result, t2.expected_result, t2.result
                FROM (
                    SELECT *
                    FROM ladder_pairing AS l
                    JOIN (
                        SELECT player_id, user_name
                        FROM player AS p JOIN user AS u
                        ON p.user_id = u.user_id
                    ) AS pu
                    ON l.player_id = pu.player_id
                ) As t1
                JOIN (
                    SELECT *
                    FROM ladder_pairing AS l
                    JOIN (
                        SELECT player_id, user_name
                        FROM player AS p JOIN user AS u
                        ON p.user_id = u.user_id
                    ) AS pu
                    ON l.player_id = pu.player_id
                ) As t2
                ON t1.event_id = t2.event_id AND t1.match_number = t2.match_number
                WHERE t1.event_id = '%s' AND t1.result IS NULL AND t1.player_id <> t2.player_id AND t1.colour = 'black'
            """
            %(eventID)
        )

        return self._cursor.fetchall()

    @connect
    def getUnfinishedPairings(self, event):
        if event.eventType == "ladder":
            self._cursor.execute(
                """
                    SELECT *
                    FROM ladder_pairing
                    WHERE event_id = '%s' AND result IS NULL
                """
                %(event.id)
            )

        else:
            self._cursor.execute(
                """
                    SELECT *
                    FROM sr_pairing
                    WHERE event_id = '%s' AND result IS NULL
                """
                %(event.id)
            )

        return self._cursor.fetchall()

    @connect
    def getJoinRequestByID(self, request_id):
        self._cursor.execute(
            """SELECT event_id, user_id, status
            FROM join_event_requests
            WHERE request_id = '%s'"""
            %(request_id)
        )

        return self._cursor.fetchone()

    @connect
    def getJoinRequest(self, event_id, user_id):
        self._cursor.execute(
            """SELECT request_id, event_id, user_id, status
            FROM join_event_requests
            WHERE event_id = '%s' AND user_id = '%s'"""
            %(event_id, user_id)
        )

        return self._cursor.fetchone()

    @connect
    def getJoinRequests(self, event_id):
        self._cursor.execute(
            """SELECT event_id, user_id, status
            FROM join_event_requests
            WHERE event_id = '%s'"""
            %(event_id)
        )

        return self._cursor.fetchall()

    @connect
    def getPendingJoinRequestsInfo(self, event_id):
        self._cursor.execute(
            """SELECT requestTable.request_id, requestTable.event_id, requestTable.user_id, userTable.user_name, userTable.first_name, userTable.last_name, userTable.dob, userTable.raiting
            FROM join_event_requests AS requestTable
            JOIN user AS userTable
            ON requestTable.user_id = userTable.user_id
            WHERE event_id = '%s' AND status = 'Request Sent'"""
            %(event_id)
        )

        return self._cursor.fetchall()

    @connect
    def updateUser(self, userData):
        self._cursor.execute(
            """
                UPDATE user
                SET user_name = '%s', first_name = '%s', last_name = '%s', password = '%s', email = '%s', dob = '%s'
                WHERE user_name = '%s'
            """
            % (userData[1], userData[2], userData[3], userData[4], userData[5], userData[6], userData[1])
        )

        self._connection.commit()

    @connect
    def updateUserPassword(self, userName, password):
        self._cursor.execute(
            """
                UPDATE user
                SET password = '%s'
                WHERE user_name = '%s';
            """
            % (password, userName)
        )

        self._connection.commit()

    @connect
    def updateEvent(self, event):
        self._cursor.execute(
            """
                UPDATE event
                SET event_status = '%s', round_number = '%s'
                WHERE event_id = '%s';
            """
            %(event.status, event.round, event.id)
        )

        self._connection.commit()

    @connect
    def updatePlayer(self, player):
        if player.name != "bye":
            self._cursor.execute(
                """
                    UPDATE player
                    SET score = '%s', position = '%s'
                    WHERE player_id = '%s'
                """
                %(player.score, player.position, player.id)
            )

        self._connection.commit()

    @connect
    def updateSR_Pairing(self, roundNumber, bPlayer, bResult, wPlayer, wResult):
        self._cursor.execute(
            """
                UPDATE sr_pairing
                SET result = '%s'
                WHERE round_number = '%s' AND player_id = '%s'
            """
            %(bResult, roundNumber, bPlayer.id)
        )

        if bPlayer.name != "bye":
            self._cursor.execute(
                """
                    SELECT expected_result
                    FROM sr_pairing
                    WHERE round_number = '%s' AND player_id = '%s'
                """
                %(roundNumber, bPlayer.id)
            )

            newRaiting = bPlayer.updateRaiting(self._cursor.fetchone()[0], bResult)

            self._cursor.execute(
                """
                    UPDATE user
                    SET raiting = '%s'
                    WHERE user_name = '%s'
                """
                %(newRaiting, bPlayer.name)
            )
        else:
            pass

        self._cursor.execute(
            """
                UPDATE sr_pairing
                SET result = '%s'
                WHERE round_number = '%s' AND player_id = '%s'
            """
            %(wResult, roundNumber, wPlayer.id)
        )

        if wPlayer.name != "bye":
            self._cursor.execute(
                """
                    SELECT expected_result
                    FROM sr_pairing
                    WHERE round_number = '%s' AND player_id = '%s'
                """
                %(roundNumber, wPlayer.id)
            )

            newRaiting = wPlayer.updateRaiting(self._cursor.fetchone()[0], wResult)

            self._cursor.execute(
                """
                    UPDATE user
                    SET raiting = '%s'
                    WHERE user_name = '%s'
                """
                %(newRaiting, wPlayer.name)
            )
        else:
            pass
        
        self._connection.commit()
    
    @connect
    def updateLadder_Pairing(self, match, bPlayer, bResult, wPlayer, wResult):
        # Update black
        self._cursor.execute(
            """
                UPDATE ladder_pairing
                SET result = '%s'
                WHERE match_number = '%s' AND player_id = '%s';
            """
            %(bResult, match, bPlayer.id)
        )

        self._cursor.execute(
            """
                SELECT expected_result
                FROM ladder_pairing
                WHERE match_number = '%s' AND player_id = '%s'
            """
            %(match, bPlayer.id)
        )

        newRaiting = bPlayer.updateRaiting(self._cursor.fetchone()[0], bResult)

        self._cursor.execute(
            """
                UPDATE user
                SET raiting = '%s'
                WHERE user_name = '%s'
            """
            %(newRaiting, bPlayer.name)
        )

        # Update white
        self._cursor.execute(
            """
                UPDATE ladder_pairing
                SET result = '%s'
                WHERE match_number = '%s' AND player_id = '%s';
            """
            %(wResult, match, wPlayer.id)
        )

        self._cursor.execute(
            """
                SELECT expected_result
                FROM ladder_pairing
                WHERE match_number = '%s' AND player_id = '%s'
            """
            %(match, wPlayer.id)
        )

        newRaiting = wPlayer.updateRaiting(self._cursor.fetchone()[0], wResult)

        self._cursor.execute(
            """
                UPDATE user
                SET raiting = '%s'
                WHERE user_name = '%s'
            """
            %(newRaiting, wPlayer.name)
        )
        
        self._connection.commit()

    @connect
    def updateJoinRequest(self, request_id, newStatus):
        self._cursor.execute(
            """
                UPDATE join_event_requests
                SET status = '%s'
                WHERE request_id = '%s';
            """
            %(newStatus, request_id)
        )
        
        self._connection.commit()

    @connect
    def deleteUser(self, username):
        now = datetime.datetime.now()

        self._cursor.execute(
            """
                UPDATE user
                SET user_name = '%s', first_name = NULL, last_name = NULL, password = NULL, email = NULL, dob = NULL
                WHERE user_name = '%s'
            """
            % (now.timestamp(), username)
        )

        self._connection.commit()

    @connect
    def deleteEvent(self, eventID, eventType):
        pairingTable = None
        if eventType == "ladder":
            pairingTable = "ladder_pairing"
        else:
            pairingTable = "sr_pairing"

        self._cursor.execute(
            """
                DELETE FROM %s
                WHERE event_id = %s
            """
            %(pairingTable ,eventID)
        )

        self._cursor.execute(
            """
                DELETE FROM player
                WHERE event_id = %s
            """
            %(eventID)
        )

        self._cursor.execute(
            """
                DELETE FROM event
                WHERE event_id = %s
            """
            %(eventID)
        )

        self._connection.commit()

    def backup(self, filename):
        shutil.copy(self._location, "Data\\Backups\\" + filename + ".db")
        print("Created a database backup called " + filename)