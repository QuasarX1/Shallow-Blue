from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    usernameTextBox = StringField("Username", validators = [DataRequired(message = "This is a required field.")])
    passwordPasswordBox = PasswordField("Password", validators = [DataRequired(message = "This is a required field.")])
    submitButton = SubmitField("Login")

class SignupForm(FlaskForm):
    firstNameTextBox = StringField("Username", validators = [DataRequired(message = "This is a required field.")])
    lastNameTextBox = StringField("Username", validators = [DataRequired(message = "This is a required field.")])
    usernameTextBox = StringField("Username", validators = [DataRequired(message = "This is a required field.")])
    emailTextBox = StringField("Username", validators = [DataRequired(message = "This is a required field."), Email("This field must contain a valid email adress.")])
    dobDayIntegerBox = IntegerField("Day")
    dobMonthIntegerBox = IntegerField("Month")
    dobYearIntegerBox = IntegerField("Year")    
    passwordPasswordBox = PasswordField("Password", validators = [DataRequired(message = "This is a required field.")])
    repeatPasswordPasswordBox = PasswordField("Password", validators = [DataRequired(message = "This is a required field."), EqualTo(passwordPasswordBox, "Your passwords don't match. Please try entering them again.")])
    submitButton = SubmitField("Signup")