from wtforms import StringField, validators, SelectField
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
# from wtforms.fields.html5 import TimeField

class CreateUserFormBooking(FlaskForm):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=1, max=150), validators.DataRequired()])
    jobs = SelectField('Jobs', [validators.DataRequired()], choices=[('', 'Select Job'), ('A/F', 'Accounting/Finance'), ('Admin', 'Administrative'), ('B&W', ' Beauty & Wellness'),
                                                                     ('B/C', 'Building/Construction'), ('C/T', 'Call Centres/Telemarketing'),
                                                                     ('C/H', 'Cleaning/Housekeeping'), ('C/D', 'Creative/Design'),
                                                                     ('C/R', 'Customer Service/Receptionists'), ('Drivers', 'Drivers/Riders/Delivery'), ('E/T', 'Education/Training'),
                                                                     ('F&B', 'Hospitality/F&B'), ('HR', 'Human Resources'), ('IT', 'IT/Techincal/Engineers'), ('M', 'Manufacturing'),
                                                                     ('N/H', 'Nursing/Health Care'), ('Sales', 'Sales/Retail/Manufacturing'), ('S', 'Security'), ('Events','Temporary/Events'),
                                                                     ('W&L', 'Warehousing & Logistics')], default='')
    date = DateField('Date ', [validators.DataRequired()])
    # time = TimeField('Time',format='%H:%M')
