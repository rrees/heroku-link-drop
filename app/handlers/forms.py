from flask import abort, redirect, request, url_for

from app import forms
from app.repositories import collections, links
from app.decorators import login_required

import logging

@login_required
def new_collection():
    collection_form = forms.NewCollection(request.form)

    assert collection_form.validate(), "Form data was not valid"

    collections.create(**collection_form.data)
    return redirect(url_for('home'))

@login_required
def add_link():
    link_form = forms.NewLink(request.form)
    logging.info(request.form)
    assert link_form.validate(), "Link data in the form was incomplete"
    logging.info(link_form.data)
    links.add_link(**link_form.data)

    return redirect(url_for('collection', collection_id=link_form.collection_id.data))


@login_required
def edit_link(link_id):
    link_form = forms.EditLink(request.form)
    assert link_form.validate(), "Link data in the form was incomplete"
    logging.info(link_form.data)
    updated_link = links.update_link(link_id, **link_form.data)

    return redirect(url_for('collection', collection_id=updated_link.collection_id))

@login_required
def delete_link(link_id):
    link_form = forms.DeleteItem(request.form)
    assert link_form.validate(), "Link data in the form was incomplete"
    logging.info(link_form.data)

    link_id = link_form.item_id.data

    link = links.read(link_id)

    links.delete(link_id)

    return redirect(url_for('collection', collection_id=link.collection_id))

@login_required
def make_public(collection_id):
    collection_form = forms.CollectionChange(request.form)
    assert collection_form.validate(), "Link data in the form was incomplete"

    collections.public(True)

    return redirect(url_for('collection', collection_id=collection_id))


@login_required
def make_private(collection_id):
    collection_form = forms.CollectionChange(request.form)
    assert collection_form.validate(), "Link data in the form was incomplete"

    collections.public(False)

    return redirect(url_for('collection', collection_id=collection_id))

@login_required
def edit(collection_id):
    collection_form = forms.CollectionEdit(request.form)
    assert collection_form.validate(), "Collection data was incomplete for the edit"

    collections.update(collection_id, **collection_form.data)

    return redirect(url_for('collection', collection_id=collection_id))

@login_required
def delete_collection(collection_id):
    collection_form = forms.CollectionDelete(request.form)

    if collections.validate():
        return redirect(url_for('collections'))
    
    abort(400, "Form information was invalid")