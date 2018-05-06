import flask

def login_form():
    return flask.redirect(flask.url_for('home'))