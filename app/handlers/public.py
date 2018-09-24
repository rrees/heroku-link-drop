import re
import flask

from app.repositories import collections, links

def collection(collection_id):
	if re.fullmatch('^\d+$', collection_id):
		collection = collections.read(collection_id)
	else:
		collection = collections.read_public(collection_id)

	if not collection or not collection.public:
		flask.abort(404)

	collection_links = links.for_collection(collection.key, default_orderby='name')

	return flask.render_template('public/list.html',
		collection=collection,
		links=collection_links)