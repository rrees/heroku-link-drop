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
	collection = collections.read(collection_id)

	public_toggle_label = "Make private" if collection.public else "Make public"
	toggle_action = (flask.url_for('collection_public_form', collection_id=collection_id)
		if not collection.public else flask.url_for('collection_private_form', collection_id=collection_id))

	return flask.render_template('collection.html',
		collection=collection,
		links=links.for_collection(collection_id),
		public_toggle_label=public_toggle_label,
		visibility_action=toggle_action,
	)

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

@login_required
def delete_link(link_id):
	link = links.read(link_id)

	return flask.render_template('delete.html',
		item='link',
		identity=link.name or link.url,
		item_id=link_id,
		delete_action_url=flask.url_for('delete_link_form', link_id=link_id)
	)

@login_required
def edit_collection(collection_id):
	collection = collections.read(collection_id)

	return flask.render_template('collection/edit.html',
		collection=collection,
		links=links.for_collection(collection_id),
	)