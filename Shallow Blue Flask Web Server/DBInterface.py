import sqlite3

class DBInterface(object):
    """
    Creates an object for interfacing with the application's database.
    """

    # Atributes------------------------------------------------------------------------------------------------------------
    _connection = None
    _cursor = None

    # Methods--------------------------------------------------------------------------------------------------------------
    def __init__(self, pathToDB):
        """
        Paramiters:
            pathToDB - string - the absolute path to the database
        """
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