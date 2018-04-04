import os
import sqlite3
import sys

class DBInterface(object):
    """
    Creates an object for interfacing with the application's database.
    """

    # Atributes------------------------------------------------------------------------------------------------------------
    _connection = None
    _cursor = None

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

        if alternatePath == "":
            pathToDB = os.path.join(applicationRootDirectory, os.path.join(deafultPath, deafultName))

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
                pathToDB = os.path.join(applicationRootDirectory, os.path.join(deafultPath, deafultName))

        else:
            pathToDB = os.path.join(alternatePath, alternateName)
        
        # Connect to the db file-------------------------------------------------------------------------------------------
        self._connection = sqlite3.connect(pathToDB)# Connects to the database specified by the path in the variable "pathToDB"
        print("Database connection created to " + pathToDB)
        self._cursor = self._connection.cursor()# Creates a cursor object that is used to manipulate the database
        print("Database cursor created")
        self._cursor.execute("PRAGMA foreign_keys = ON;")

    def createTables(self):
        # user table
        self._cursor.execute(
            """CREATE TABLE user (
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
            """CREATE TABLE event (
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
            """CREATE TABLE player (
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
            """CREATE TABLE sr_pairing (
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
            """CREATE TABLE ladder_pairing (
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

    def __del__(self):
        """
        Safely closes the database connection at the end of the program or in the event of an unexpected termination.
        """
        if self._cursor != None:# Checks that _cursor has been assigned a value
            self._cursor.close()# Closes the cursor used to manipulate the database
            print("Database cursor closed")
        if self._connection != None:# Checks that _connection has been assigned a value
            self._connection.close()# Closes the connection to the database
            print("Database connection closed")