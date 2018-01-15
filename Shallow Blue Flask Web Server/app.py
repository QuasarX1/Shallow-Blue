# Creating the Flask object------------------------------------------------------------------------------------------------
from flask import Flask
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it
wsgi_app = app.wsgi_app

# View functions to handel web requests and generate responces-------------------------------------------------------------
@app.route('/')
def blank():
    """Blank Page"""
    return "This page intentionaly left almost blank."

if __name__ == '__main__':
    # Visual Studio Code For Debugging-------------------------------------------------------------------------------------
    #TODO: Comment out this section before relice
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    # Run the web server---------------------------------------------------------------------------------------------------
    app.run(HOST, PORT)
