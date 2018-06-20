from flask import redirect, url_for

def new_collection():
    return redirect(url_for('home'))