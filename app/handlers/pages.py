import flask

from app.repositories import collections, links

from app.decorators import login_required

def front_page():
	return flask.render_template('index.html')

@login_required
def home_page():
	return flask.render_template('home.html',
		collections=collections.all(sort_descending=True),)

@login_required
def collection(collection_id):
	return flask.render_template('collection.html',
		collection=collections.read(collection_id),
		links=links.for_collection(collection_id))

@login_required
def all_collections():
	return flask.render_template('collections.html',
		collections=collections.all(order_column='name'),
	)

@login_required
def link(collection_id, link_id):
	return flask.render_template('link.html',
		collection=collections.read(collection_id),
		link=links.read(link_id),
	)