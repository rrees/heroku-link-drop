from collections import namedtuple
import uuid

import pg8000
from pypika import Table, Query

from .connection import connect

links_table = Table('links')

Link = namedtuple('Link', [
	'url',
	'name',
	'description',
	'id'])

def map_to_link(row):
	return Link(
		url=row[0],
		name=row[1],
		description=row[2],
		id=row[3],
	)

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

def for_collection(collection_id, default_orderby=None):

	order_by = default_orderby if default_orderby else 'updated_timestamp'

	q = Query.from_(links_table)\
		.select('url', 'name', 'description', 'id')\
		.where(links_table.collection_id == collection_id)\
		.orderby(order_by)

	conn = connect()
	cursor = conn.cursor()
	cursor.execute(str(q))
	results = [map_to_link(r) for r in cursor.fetchall()]
	cursor.close()
	conn.close()
	return results