from wtforms import Form, StringField, SelectField, validators

class CreateJobForm(Form):
    name = StringField('Job Title', [validators.Length(min=1, max=150),validators.DataRequired()])
    location = StringField('Location', [validators.Length(min=1, max=150),validators.DataRequired()])
    timing = StringField('Timing/Shifts', [validators.Length(min=1, max=150), validators.DataRequired()])
    job_type = SelectField('Job Type', choices=[('pt','Part Time'), ('ft','Full Time'),('c','Contract'),('si','Student Internship')],default='pt')
    salary = StringField('Salary', [validators.Length(min=1, max=150), validators.DataRequired()])
