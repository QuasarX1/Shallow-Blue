import os
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

        elif tableNames != [('user',), ('sqlite_sequence',), ('event',), ('player',), ('sr_pairing',), ('ladder_pairing',)]:# If the list of tables is incorrect
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
        if tableNames == []:# If the database is blank
            makeTables = True

        elif tableNames != [('user',), ('sqlite_sequence',), ('event',), ('player',), ('sr_pairing',), ('ladder_pairing',)]:# If the list of tables is incorrect
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
                dob datetime
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
                user_id int,
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
                result varchar(255),
                PRIMARY KEY (match_number, player_id),
                FOREIGN KEY (event_id) REFERENCES event(event_id),
                FOREIGN KEY (player_id) REFERENCES player(player_id)
            )"""
        )

        # Add admin user
        self._cursor.execute("SELECT user_id FROM user WHERE user_name = 'admin'")
        if self._cursor.fetchall() == []:# If the admin user dosen't allready exist
            self._cursor.execute(
                """INSERT INTO user (
                    user_name,
                    password
                )
                VALUES (
                    'admin',
                    'admin'
                )"""
            )

        # Save the changes to the database
        self._connection.commit()

    @connect
    def getUser(self, userName, password):
        """
        Retrives a user's id and names from the database.
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

    #def __del__(self):
    #    """
    #    Safely closes the database connection at the end of the program or in the event of an unexpected termination.
    #    """
    #    if self._cursor != None:# Checks that _cursor has been assigned a value
    #        self._cursor.close()# Closes the cursor used to manipulate the database
    #        print("Database cursor closed")
    #    if self._connection != None:# Checks that _connection has been assigned a value
    #        self._connection.close()# Closes the connection to the database
    #        print("Database connection closed")