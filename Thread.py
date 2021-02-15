from wtforms import Form, StringField, TextAreaField, validators

class CreateThreadForm(Form):
    title = StringField('Add Title', [validators.Length(min=1, max=150), validators.DataRequired()])
    body = TextAreaField('Add Body', [validators.Length(min=1, max=150), validators.DataRequired()])

class CreateCommentForm(Form):
    comment = TextAreaField('Add Comment', [validators.Length(min=1, max=150), validators.DataRequired()])

