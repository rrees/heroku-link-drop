import os
import logging
import itertools
import sys

import flask

from flask_sslify import SSLify

from . import filters
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

app.jinja_env.filters['name_or_url'] = filters.name_or_url

routes = [
	('/', 'index', handlers.pages.front_page, ['GET']),
    ('/home', 'home', handlers.pages.home_page, ['GET']),
    ('/collection/<collection_id>', 'collection', handlers.pages.collection, ['GET']),
    ('/collection/<collection_id>/edit', 'collection_edit', handlers.pages.edit_collection, ['GET']),
    ('/collection/<collection_id>/delete', 'collection_delete', handlers.pages.delete_collection, ['GET']),
    ('/forms/collections/new', 'new_collection_form', handlers.forms.new_collection, ['POST']),
    ('/forms/link/add', 'new_link_form', handlers.forms.add_link, ['POST']),
    ('/forms/link/edit/<link_id>', 'edit_link_form', handlers.forms.edit_link, ['POST']),
    ('/forms/link/delete/<link_id>', 'delete_link_form', handlers.forms.delete_link, ['POST']),
    ('/forms/collection/<collection_id>/public', 'collection_public_form', handlers.forms.make_public, ['POST']),
    ('/forms/collection/<collection_id>/private', 'collection_private_form', handlers.forms.make_private, ['POST']),
    ('/forms/collection/<collection_id>/edit', 'collection_edit_form', handlers.forms.edit, ['POST']),
    ('/forms/collection/<collection_id>/delete', 'collection_deletion_form', handlers.forms.delete_collection, ['POST']),
    ('/public/collection/<collection_id>', 'public_collection', handlers.public.collection, ['GET']),
    ('/collections', 'collections', handlers.pages.all_collections, ['GET']),
    ('/collection/<collection_id>/link/<link_id>', 'link', handlers.pages.link, ['GET']),
    ('/link/<link_id>/delete', 'delete_link', handlers.pages.delete_link, ['GET']),
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