from wtforms import Form, StringField,validators,PasswordField

class PWReset(Form):
    email = StringField('Enter email', [validators.DataRequired(),validators.Email(),validators.Length(max=50)],render_kw={"placeholder": "E.g you@example.com"})
    email_validCode = StringField('Validation Code',render_kw={"placeholder": "Enter email validation code: "})
    password = PasswordField('Password',[validators.DataRequired(), validators.Length(min=8, max = 20, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password', message='Both password fields must be equal!')])

class PWConfirm(Form):
    password = PasswordField('Password',[validators.DataRequired(), validators.Length(min=8, max = 20, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.EqualTo('password', message='Both password fields must be equal!')])
