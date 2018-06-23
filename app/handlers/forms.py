from flask import redirect, request, url_for

from app import forms

def new_collection():
    collection_form = forms.NewCollection(request.form)

    assert collection_form.validate(), "Form data was not valid"
    return redirect(url_for('home'))