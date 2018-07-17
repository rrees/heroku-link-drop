import uuid

import pg8000
from pypika import Table, Query

from .connection import connect

links_table = Table('links')

def add_link(collection_id, url, name=None, description=None):

	q = Query.into(links_table)\
		.columns('collection_id', 'url', 'name', 'description')\
		.insert(collection_id, url, name, description)

	conn = connect()
	cursor = conn.cursor()
	cursor.execute(str(q) + 'RETURNING id')
	link_id = cursor.fetchone()

	cursor.close()

	conn.commit()
	conn.close()

	return link_id
