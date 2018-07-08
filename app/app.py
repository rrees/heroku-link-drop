import os
import logging
import itertools
import sys

import flask

from flask_sslify import SSLify

from . import handlers
from . import redis_utils
from .auth.routes import auth_routes

ENV = os.environ.get("ENV", "PROD")

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    level=logging.DEBUG,
    stream=sys.stderr,
)

redis_url = os.environ.get("REDIS_URL", None)

redis = redis_utils.setup_redis(redis_url) if redis_url else None

app = flask.Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

if not ENV == "DEV":
    sslify = SSLify(app)

logger = app.logger

routes = [
	('/', 'index', handlers.pages.front_page, ['GET']),
    ('/home', 'home', handlers.pages.home_page, ['GET']),
    ('/collection/<collection_id>', 'collection', handlers.pages.collection, ['GET']),
    ('/forms/collections/new', 'new_collection_form', handlers.forms.new_collection, ['POST']),
]

all_routes = itertools.chain(
    routes,
    auth_routes,
)

for path, endpoint, handler, methods in all_routes:
	app.add_url_rule(path, endpoint, handler, methods=methods)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500