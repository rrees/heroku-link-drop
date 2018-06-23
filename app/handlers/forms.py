from flask import redirect, request, url_for

from app import forms
from app.repositories import collections

def new_collection():
    collection_form = forms.NewCollection(request.form)

    assert collection_form.validate(), "Form data was not valid"

    collections.create(**collection_form.data)
    return redirect(url_for('home'))