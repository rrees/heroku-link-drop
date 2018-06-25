import flask

from app.repositories import collections

def front_page():
	return flask.render_template('index.html')

def home_page():
	return flask.render_template('home.html',
		collections=collections.all(),)

def collection(collection_id):
	return flask.render_template('collection.html',
		collection=collections.read(collection_id))