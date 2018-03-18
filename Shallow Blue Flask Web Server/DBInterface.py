import os
import sqlite3

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
        deafultPath = None
        alternatePath = None

        try:
            file = open(pathToLocationFile, "r")
            deafultPath = os.path.join(applicationRootDirectory, file.readline()[0:-1])
            alternatePath = file.readline()
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
                exit()

            else:
                file = None

                if os.path.exists(pathToLocationFile):
                    file = open(pathToLocationFile, "w")

                else:
                    file = open(pathToLocationFile, "a")

                deafultPath = "Data/ShallowBlueDatabase.db"
                alternatePath = ""

                file.write(deafultPath)
                file.write(alternatePath)
                file.close()

                deafultPath = os.path.join(applicationRootDirectory, deafultPath)

        # Set the value of the db path-------------------------------------------------------------------------------------
        pathToDB = None

        if alternatePath == "":
            pathToDB = os.path.join(applicationRootDirectory, deafultPath)

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
                exit()

            else:
                pathToDB = os.path.join(applicationRootDirectory, deafultPath)

        else:
            pathToDB = alternatePath
        
        # Connect to the db file-------------------------------------------------------------------------------------------
        self._connection = sqlite3.connect(pathToDB)# Connects to the database specified by the path in the variable "pathToDB"
        print("Database connection created to " + pathToDB)
        self._cursor = self._connection.cursor()# Creates a cursor object that is used to manipulate the database
        print("Database cursor created")

    def __del__(self):
        """
        Safely closes the database connection at the end of the programm or in the event of an unexpected termination.
        """
        self._cursor.close()# Closes the cursor used to manipulate the database
        print("Database cursor closed")
        self._connection.close()# Closes the connection to the database
        print("Database connection closed")