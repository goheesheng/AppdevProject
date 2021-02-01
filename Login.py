from wtforms import Form, StringField,validators, PasswordField, BooleanField
from flask_wtf import RecaptchaField
from flask import Flask

app = Flask('__init__')

class LoginForm(Form):
    nric = StringField("NRIC", [validators.Length(min=1), validators.DataRequired()])
    password = PasswordField('Password',[validators.DataRequired(), validators.Length(max = 20)])
    remember = BooleanField("Remember me")
    recaptcha = RecaptchaField()
