from wtforms import Form, StringField, SelectField, TextAreaField, validators, BooleanField

#Basically removed the confirm_password and change password to Stringfield so admin can view the password and change it if they want

class Admin_UpdateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=30),validators.DataRequired()],render_kw={"placeholder": "E.g Samuel"})  # can edit length,validators.DataRequired() means data required
    last_name = StringField('Last Name', [validators.Length(min=1, max=30), validators.DataRequired()],render_kw={"placeholder": "E.g Goh"})
    race = SelectField("Race", [validators.DataRequired()], choices=[('', 'Select'), ('C','Chinese'), ('M','Malay'), ('I','Indian'), ('O','Others')],default='')
    phone_no = StringField('Phone Number', [validators.Length(min=8, max=15), validators.DataRequired()],render_kw={"placeholder": "E.g 8898 2898"})
    email = StringField('Email', [validators.DataRequired(),validators.Email(),validators.Length(max=50)],render_kw={"placeholder": "E.g you@example.com"})
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    password = StringField('Password',[validators.DataRequired(), validators.Length(min=8, max = 20, message='Password should be at least %(min)d characters long')])
    address_1 = TextAreaField('Address (First)', [validators.DataRequired()],render_kw={"placeholder": "E.g 898 Yishun Ring Road"})
    address_2 = TextAreaField('Address (Second) (Optional)', [validators.Optional()],render_kw={"placeholder": "#08-1899"})
    postal_code = StringField('Postal Code', [validators.Length(min=6, max=6), validators.DataRequired()], render_kw={"placeholder": "889906"})
    receive_emails = BooleanField("I want to receive Angel's Email")
    become_admin = BooleanField("Admin Staff")
