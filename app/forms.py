from wtforms import Form, validators
from wtforms.fields import StringField, BooleanField

class NewCollection(Form):
    name = StringField('Name', [validators.required()])
    description = StringField('Description')
    public = BooleanField('Public', default=False)