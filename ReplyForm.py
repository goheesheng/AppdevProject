from wtforms import Form, TextAreaField, validators

class CreateReplyForm(Form):
    reply = TextAreaField('Reply', [validators.DataRequired()])
