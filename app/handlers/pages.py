import flask

from app.repositories import collections

from app.decorators import login_required

def front_page():
	return flask.render_template('index.html')

@login_required
def home_page():
	return flask.render_template('home.html',
		collections=collections.all(),)

@login_required
def collection(collection_id):
	return flask.render_template('collection.html',
		collection=collections.read(collection_id))