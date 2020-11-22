from wtforms import Form, validators
from wtforms import fields

class NewCollection(Form):
    name = fields.StringField('Name', [validators.required()])
    description = fields.StringField('Description')
    public = fields.BooleanField('Public', default=False)

class NewLink(Form):
    collection_id = fields.HiddenField('Collection ID', [validators.required()])
    url = fields.StringField('URL', [validators.required()])
    name = fields.StringField('Name')
    description = fields.StringField('Description')

class EditLink(Form):
    url = fields.StringField('URL', [validators.required()])
    name = fields.StringField('Name')
    description = fields.StringField('Description')

class DeleteItem(Form):
    item_id = fields.HiddenField('Item Id', [validators.required()])

class CollectionChange(Form):
	collection_id = fields.HiddenField('Collection ID', [validators.required()])

class CollectionEdit(Form):
	name = fields.StringField('Name', [validators.required()])
	description = fields.StringField('Description')

class CollectionDelete(Form):
    collection_id = fields.HiddenField('Collection ID', [validators.required(), validators.NumberRange(min=0)])