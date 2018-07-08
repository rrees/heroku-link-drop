import uuid

import pg8000
from pypika import Table, Query

from .connection import connect

collections_table = Table('collections')

def add_link(collection_id, url, name=None, description=None):

    return None
