from wtforms import Form, StringField, SelectField, TextAreaField, validators

class CreateTicketForm(Form):
    category = SelectField('Category', [validators.DataRequired()], choices=[('', 'Select a Problem Type'), ('Technical Issues', 'Technical Issues'), ('General Enquiries', 'General Enquiries'),('Account Management', 'Account Management')], default='')
    subject = StringField('Subject (30 chars max)', [validators.Length(min=1, max=30), validators.DataRequired()])
    message = TextAreaField('Message', [validators.Optional()])
