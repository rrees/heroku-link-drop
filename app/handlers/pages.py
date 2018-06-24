import flask

from app.repositories import collections

def front_page():
	return flask.render_template('index.html')

def home_page():
	return flask.render_template('home.html',
		collections=collections.all(),)