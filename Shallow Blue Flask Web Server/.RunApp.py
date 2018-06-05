import os
import socket
import sys

try:
    ip = socket.gethostbyname(socket.gethostname())

    location = os.getcwd()

    command = r'"%s\env\Scripts\python.exe" app.py %s'% (location, ip)

    result = os.system(command)

    if result == 1:
        print("Failed to start server.")

finally:
    input("Press enter to close...")
    sys.exit()
