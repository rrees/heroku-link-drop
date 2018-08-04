import flask

def collection(collection_id):
	collection = collections.read(collection_id)

	if not collection.public:
		flask.abort(404)

	links = links.for_collection(collection_id)

	return flask.render_template('public/list.html',
		collection=collection,
		links=links)