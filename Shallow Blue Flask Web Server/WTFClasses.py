from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    usernameTextBox = StringField("Username", validators = [DataRequired(message = "This is a required field.")])
    passwordPasswordBox = PasswordField("Password", validators = [DataRequired(message = "This is a required field.")])
    submitButton = SubmitField("Login")