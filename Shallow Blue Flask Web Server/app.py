# General Library Imports--------------------------------------------------------------------------------------------------
import datetime
import DBInterface
import hashlib
import Ladder_EventClass
import os
import random
import sqlite3
import SR_EventClass
import string
import WTFClasses

# Specific Imports---------------------------------------------------------------------------------------------------------
from flask import Flask, render_template, redirect, url_for, session, flash
from functools import wraps

# Creating the Flask object------------------------------------------------------------------------------------------------
app = Flask(__name__)

# Adding the app config data
app.config["SECRET_KEY"] = ""
for i in range(0, 10):
    app.config["SECRET_KEY"] += string.printable[random.SystemRandom().randint(0, len(string.printable))]

# Creating the database object---------------------------------------------------------------------------------------------
rootDirectory = os.path.dirname(__file__)
database = DBInterface.DBInterface(os.path.join(rootDirectory, "Data/DatabaseLocation.txt"), rootDirectory)

# Make the WSGI interface available at the top level so wfastcgi can get it
wsgi_app = app.wsgi_app

# Custom Decorators---------------------------------------------------------------------------------------------------------
def testLogin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        loggedIn = False

        if "userID" in session:
            loggedIn = True

        return func(loggedIn)

    return wrapper

# View functions to handele web requests and generate responces-------------------------------------------------------------
@app.route('/')
@app.route('/home')
@testLogin
def home(loggedIn):
    """Splash Page"""
    return render_template("SplashPage.html", loggedIn = loggedIn)

@app.route('/login', methods = ["GET", "POST"])
def login():
    """Login Page"""
    form = WTFClasses.LoginForm()

    if form.validate_on_submit():
        userName = form.usernameTextBox.data
        password = hashlib.sha512(form.passwordPasswordBox.data.encode('utf8')).hexdigest()
        
        userData = database.getUser(userName, password)

        if userData != None:
            session["userID"] = userData[0]
            session["userName"] = userData[1]
            session["firstName"] = userData[2]
            session["lastName"] = userData[3]

            return redirect(url_for("home"))

        else:
            flash("Credentials were incorrect. Please try again.")

    return render_template("LoginPage.html", pageTitle = "Login", form = form)

@app.route('/logout')
def logout():
    del session["userID"]
    del session["userName"]
    del session["firstName"]
    del session["lastName"]

    flash("You have sucessfully logged out.")

    return redirect(url_for("home"))

@app.route('/signup', methods = ["GET", "POST"])
def signup():
    """Signup Page"""
    form = WTFClasses.SignupForm()

    if form.validate_on_submit():
        year = form.dobYearIntegerBox.data
        month = form.dobMonthIntegerBox.data
        day = form.dobDayIntegerBox.data

        # Validate username and date fields---------------------------------------------------------------------------------
        valid = True

        # Retrive a list of usernames from the database
        userNames = database.getUsernames()

        # Check username is unique
        if form.usernameTextBox.data in userNames:
            form.usernameTextBox.errors.append("This username is allready being used. Please try another")
            valid = False

        try:
            # Check the date is in a sutable range
            datetime.timedelta()
            if datetime.date(year, month, day) > datetime.date.today() or datetime.date(year, month, day) -  datetime.date(1, 1, 1) < datetime.date.today() - datetime.date(120, 1, 1):
                form.dobDayIntegerBox.errors.append("The date provided was not posible as a date of birth. Please try again.")
                valid = False

        except ValueError:
            valid = False

            # Check that day and month values are valid
            if month in [1, 3, 5, 7, 8, 10, 12] and (day < 1 or day > 31):
                form.dobDayIntegerBox.errors.append("The day of the month provided dosen't exist.")

            elif month in [4, 6, 9, 11] and (day < 1 or day > 31):
                form.dobDayIntegerBox.errors.append("The day of the month provided dosen't exist.")
            
            elif month == 2:
                if int(year/4) == int(float(year/4.0)) and (day < 1 or day > 29):
                    form.dobDayIntegerBox.errors.append("The day of the month provided dosen't exist.")

                elif day < 1 or day > 28:
                    form.dobDayIntegerBox.errors.append("The day of the month provided dosen't exist.")

            else:
                form.dobMonthIntegerBox.errors.append("The month provided dosen't exist.")

        # Add the user to the database-------------------------------------------------------------------------------------
        if valid == True:# If the username and date fields are valid
            # In case the username has been taken by another user after the check
            try:
                database.addUser(form.usernameTextBox.data, form.firstNameTextBox.data, form.lastNameTextBox.data, hashlib.sha512(form.passwordPasswordBox.data.encode('utf8')).hexdigest(), form.emailTextBox.data, datetime.date(year, month, day).strftime("%Y-%m-%d"))

            except sqlite3.IntegrityError:
                 form.usernameTextBox.errors.append("This username is allready being used. Please try another")

                 return render_template("SignupPage.html", pageTitle = "Signup", form = form)

            flash("Welcome %s." %(form.usernameTextBox.data))

            return redirect(url_for("home"))

    return render_template("SignupPage.html", pageTitle = "Signup", form = form)

@app.route('/join')
def join():
    """Join Page"""
    events = database.getEventListings()

    listings = []

    for event in events:
        if event[4] == "registration" and datetime.datetime.fromtimestamp(event[2]) > datetime.datetime.now() or event[5] == "ladder" and event[4] != "finnished":
            listings.append([event[0], event[1], datetime.datetime.fromtimestamp(event[2]), event[3]])

    listings.sort(key = lambda event: event[2])

    return render_template("JoinPage.html", pageTitle = "Join", eventData = listings)

@app.route('/watch')
def spectate():
    """Spectate Page"""
    events = database.getEventListings()

    listings = []

    for event in events:
        if event[4] != "finnished":
            listings.append([event[0], event[1], datetime.datetime.fromtimestamp(event[2]), event[3]])

    listings.sort(key = lambda event: event[2])

    return render_template("JoinPage.html", pageTitle = "Spectate", eventData = listings)

@app.route('/<eventID>/home')
def homepage(eventID):
    event = None

    #Create the event object
    eventData = database.getEvent(eventID)
    if eventData[4] == "ladder":
        event = Ladder_EventClass.Ladder_Event(database, eventData)
    else:
        event = SR_EventClass.SR_Event(database, eventData)

    #event.addPlayer(database, 1)

    return render_template("EventHomePage.html", event = event, pageTitle = "Home", homeClass = "active")

@app.route('/<eventID>/pairings', methods = ["GET", "POST"])
def pairings(eventID):
    event = None

    #Create the event object
    eventData = database.getEvent( eventID)
    if eventData[4] == "ladder":
        event = Ladder_EventClass.Ladder_Eventdatabase, (eventData)
    else:
        event = SR_EventClass.SR_Event(database, eventData)

    currentPairings = event.getPairings(database)

@app.route('/<eventID>/scores')
def scores(eventID):
    event = None

    #Create the event object
    eventData = database.getEvent(eventID)
    if eventData[4] == "ladder":
        event = Ladder_EventClass.Ladder_Event(database, eventData)
    else:
        event = SR_EventClass.SR_Event(database, eventData)

    event.sortPlayers()
    return event.players

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

    # Clearup Operations---------------------------------------------------------------------------------------------------
    #del database