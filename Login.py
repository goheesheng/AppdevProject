from wtforms import Form, StringField,validators, PasswordField, BooleanField
from flask_wtf import RecaptchaField




class LoginForm(Form):
    nric = StringField("NRIC", [validators.Length(min=1), validators.DataRequired()])
    password = PasswordField('Password',[validators.DataRequired(), validators.Length(max = 20)])
    remember = BooleanField("Remember me")
    recaptcha = RecaptchaField()

class LoginVerify(Form):
    phone_token = StringField('Token', [validators.DataRequired(), validators.Length(min = 6, max = 6)],render_kw={"placeholder": "Enter phone validation code: "})

class LoginEmailVerify(Form):
    email_validCode = StringField('Validation Code',render_kw={"placeholder": "Enter email validation code: "})
