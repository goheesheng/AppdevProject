from wtforms import Form, StringField,validators, PasswordField, BooleanField

class LoginForm(Form):
    nric = StringField("NRIC", [validators.Length(min=1), validators.DataRequired()])
    password = PasswordField('Password',[validators.DataRequired(), validators.Length(max = 20)])
    remember = BooleanField("Remember me")
