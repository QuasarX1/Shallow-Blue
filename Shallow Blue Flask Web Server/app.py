# General Library Imports
import sqlite3
import datetime

con = sqlite3.connect("test.db")

cur = con.cursor()

# Creating the Flask object------------------------------------------------------------------------------------------------
from flask import Flask, render_template
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it
wsgi_app = app.wsgi_app

# View functions to handele web requests and generate responces-------------------------------------------------------------
@app.route('/')
@app.route('/home')
def home():
    """Splash Page"""
    return render_template("SplashPage.html")

@app.route('/join')
def join():
    """Join Page"""
    return render_template("JoinPage.html", pageTitle = "Join", eventData = [["Event 1", datetime.datetime(2018, 1, 1), "Event info."], ["Event 2", datetime.datetime(2018, 12, 31), "Event info."], ["Event 3", datetime.datetime(2018, 5, 9), "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent ipsum leo, gravida vel nisi lacinia, gravida fringilla felis. Maecenas sit amet maximus lorem, ut dapibus ipsum. Aliquam erat volutpat. Vivamus gravida non metus eleifend rhoncus. Praesent quis enim ut urna mollis auctor et volutpat est. Sed quis est accumsan, laoreet felis sit amet, interdum arcu. Duis quis risus at dui eleifend aliquam. Nulla facilisi. Nulla ut tincidunt quam. Aliquam erat volutpat. Fusce convallis magna non nunc vehicula, ut hendrerit odio accumsan. Mauris nec viverra arcu."]])

@app.route('/watch')
def spectate():
    """Spectate Page"""
    return render_template("JoinPage.html", pageTitle = "Spectate", eventData = [["Event 1", datetime.datetime(2018, 1, 1), "Event info."], ["Event 2", datetime.datetime(2018, 12, 31), "Event info."], ["Event 3", datetime.datetime(2018, 5, 9), "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent ipsum leo, gravida vel nisi lacinia, gravida fringilla felis. Maecenas sit amet maximus lorem, ut dapibus ipsum. Aliquam erat volutpat. Vivamus gravida non metus eleifend rhoncus. Praesent quis enim ut urna mollis auctor et volutpat est. Sed quis est accumsan, laoreet felis sit amet, interdum arcu. Duis quis risus at dui eleifend aliquam. Nulla facilisi. Nulla ut tincidunt quam. Aliquam erat volutpat. Fusce convallis magna non nunc vehicula, ut hendrerit odio accumsan. Mauris nec viverra arcu."]])

#@app.route('/test')
#def test():
#    """Template Test Page"""
#    return render_template("TemplateTestPage.html", eventName = "Test Event", pageTitle = "Test Page", splashClass = "active")

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
    app.run(HOST, PORT, threaded = True)
