from wtforms import Form, validators, widgets
from wtforms import fields

class NewCollection(Form):
    name = fields.StringField('Name', [validators.DataRequired()])
    description = fields.StringField('Description')
    public = fields.BooleanField('Public', default=False)

class NewLink(Form):
    collection_id = fields.HiddenField('Collection ID', [validators.DataRequired()])
    url = fields.StringField('URL', [validators.DataRequired()])
    name = fields.StringField('Name')
    description = fields.StringField('Description')

class EditLink(Form):
    url = fields.StringField('URL', [validators.DataRequired()])
    name = fields.StringField('Name')
    description = fields.StringField('Description')

class DeleteItem(Form):
    item_id = fields.HiddenField('Item Id', [validators.DataRequired()])

class CollectionChange(Form):
	collection_id = fields.HiddenField('Collection ID', [validators.DataRequired()])

class CollectionEdit(Form):
	name = fields.StringField('Name', [validators.DataRequired()])
	description = fields.StringField('Description')

class CollectionDelete(Form):
    item_id = fields.IntegerField('Collection ID',
        widget=widgets.HiddenInput(),
        validators=[validators.DataRequired(), validators.NumberRange(min=0)])