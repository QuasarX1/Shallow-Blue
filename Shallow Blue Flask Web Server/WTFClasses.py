from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, HiddenField, FloatField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Optional

class AddPlayerForm(FlaskForm):
    usernameTextBox = StringField("Name", validators = [DataRequired(message = "This is a required field.")])
    submitButton = SubmitField("Add Player")

class CreateEventForm(FlaskForm):
    typeSelector = SelectField("Event Type", choices = [["", ""], ["swiss", "Swiss"], ["round robin", "Round Robin"], ["ladder", "Ladder"]], validators = [DataRequired()])
    maxRoundsIntegerBox = IntegerField("Number of Rounds",  validators = [Optional()])
    playersIntegerBox = IntegerField("Estimated Number of Players",  validators = [Optional()])
    eventNameTextBox = StringField("Event Name", validators = [DataRequired(message = "This is a required field.")])
    infoTextBox = TextAreaField("Event Infomation", validators = [DataRequired(message = "This is a required field.")])
    startDayIntegerBox = IntegerField("Day",  validators = [Optional()])
    startMonthIntegerBox = IntegerField("Month",  validators = [Optional()])
    startYearIntegerBox = IntegerField("Year",  validators = [Optional()])
    startHourIntegerBox = IntegerField("Hour",  validators = [Optional()])
    startMinuteIntegerBox = IntegerField("Minute",  validators = [Optional()])
    winScoreFloatBox = StringField("Win Score", validators = [DataRequired(message = "This is a required field.")])
    drawScoreFloatBox = StringField("Draw Score", validators = [DataRequired(message = "This is a required field.")])
    loseScoreFloatBox = StringField("Lose Score", validators = [DataRequired(message = "This is a required field.")])
    noShowScoreFloatBox = StringField("No Show Score", validators = [DataRequired(message = "This is a required field.")])
    adminPasswordBox = PasswordField("Admin Password",  validators = [Optional()])
    submitButton = SubmitField("Create Event")

class DeleteEventForm(FlaskForm):
    passwordPasswordBox = PasswordField("Re-enter your password to confirm:", validators = [DataRequired(message = "This is a required field.")])
    submitButton = SubmitField("Delete Event")

class LoginForm(FlaskForm):
    usernameTextBox = StringField("Username", validators = [DataRequired(message = "This is a required field.")])
    passwordPasswordBox = PasswordField("Password", validators = [DataRequired(message = "This is a required field.")])
    submitButton = SubmitField("Login")

class ResultForm(FlaskForm):
    pairingIdentifier = HiddenField()
    matchNumber = HiddenField()
    blackResultSelector = SelectField("Black Result", choices = [["", ""], ["W", "Win"], ["D", "Draw"], ["L", "Lose"], ["NS", "No Show"]], validators = [DataRequired(message = "This is a required field.")])
    whiteResultSelector = SelectField("White Result", choices = [["", ""], ["W", "Win"], ["D", "Draw"], ["L", "Lose"], ["NS", "No Show"]], validators = [DataRequired(message = "This is a required field.")])
    submitButton = SubmitField("Submit")

class SignupForm(FlaskForm):
    firstNameTextBox = StringField("First Name", validators = [DataRequired(message = "This is a required field.")])
    lastNameTextBox = StringField("Last name", validators = [DataRequired(message = "This is a required field.")])
    usernameTextBox = StringField("Username", validators = [DataRequired(message = "This is a required field.")])
    emailTextBox = StringField("Email", validators = [DataRequired(message = "This is a required field."), Email("This field must contain a valid email adress.")])
    dobDayIntegerBox = IntegerField("Day")
    dobMonthIntegerBox = IntegerField("Month")
    dobYearIntegerBox = IntegerField("Year")    
    passwordPasswordBox = PasswordField("Password", validators = [DataRequired(message = "This is a required field.")])
    repeatPasswordBox = PasswordField("Repeat Password", validators = [DataRequired(message = "This is a required field."), EqualTo("passwordPasswordBox", "Your passwords don't match. Please try entering them again.")])
    submitButton = SubmitField("Signup")

class PairingForm(FlaskForm):
    blackNameSelector = SelectField("Player playing Black", coerce = int, validators = [DataRequired(message = "This is a required field.")])
    whiteNameSelector = SelectField("Player playing White", coerce = int, validators = [DataRequired(message = "This is a required field.")])
    submitButton = SubmitField("Submit")

class ViewOldEventsForm(FlaskForm):
    viewCheckBox = BooleanField("View Finnished Events")
    submitButton = SubmitField("Submit")