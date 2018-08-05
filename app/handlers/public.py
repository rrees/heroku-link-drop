import flask

from app.repositories import collections, links

def collection(collection_id):
	collection = collections.read(collection_id)

	if not collection.public:
		flask.abort(404)

	collection_links = links.for_collection(collection_id, default_orderby='name')

	return flask.render_template('public/list.html',
		collection=collection,
		links=collection_links)