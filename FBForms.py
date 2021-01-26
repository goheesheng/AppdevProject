from wtforms import Form, StringField, TextAreaField, validators, RadioField


class CreateFeedbackForm(Form):
    thoughts = RadioField('Do you think our Customer Support was helpful?*', [validators.DataRequired()],
                          choices=[('Yes', 'Yes'), ('Partially', 'Partially'), ('No', 'No')])
    reason = StringField('What was your reason for visiting the website?*',
                         [validators.Length(min=1, max=100), validators.DataRequired()])
    suggestions = TextAreaField('Do you have any suggestions for us to improve on?', [validators.Optional()])



