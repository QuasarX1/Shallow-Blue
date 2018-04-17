# General Library Imports--------------------------------------------------------------------------------------------------
import datetime
import DBInterface
import os
import random
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
        password = form.passwordPasswordBox.data

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
            if datetime.date(year, month, day) > datetime.date.today() or datetime.date(year, month, day) -  datetime.date(0, 0, 0) < datetime.date.today() - datetime.date(120, 1, 1):
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

        

        if valid == True:# If the username and date fields are valid
            try:# In case the username has been taken by another user after the check
                database.addUser(form.usernameTextBox.data, form.firstNameTextBox.data, form.lastNameTextBox.data, form.passwordPasswordBox.data, form.emailTextBox.data, datetime.date(year, month, day).strftime())

            except sqlite3.IntegrityError:
                 form.usernameTextBox.errors.append("This username is allready being used. Please try another")

                 return render_template("SignupPage.html", pageTitle = "Signup", form = form)

            flash("Welcome %s." %(form.usernameTextBox.data))

            return redirect(url_for("home"))

    return render_template("SignupPage.html", pageTitle = "Signup", form = form)

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

    # Clearup Operations---------------------------------------------------------------------------------------------------
    #del database