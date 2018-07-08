from flask import redirect, request, url_for

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