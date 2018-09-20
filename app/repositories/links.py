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
	'id',
	'collection_id'])

def map_to_link(row):
	return Link(
		url=row[0],
		name=row[1],
		description=row[2],
		id=row[3],
		collection_id=row[4]
	)

def read_link_columns():
	return Query.from_(links_table)\
		.select('url', 'name', 'description', 'id', 'collection_id')

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

	q = read_link_columns()\
		.where(links_table.collection_id == collection_id)\
		.orderby(order_by)

	conn = connect()
	cursor = conn.cursor()
	cursor.execute(str(q))
	results = [map_to_link(r) for r in cursor.fetchall()]
	cursor.close()
	conn.close()
	return results

def read(link_id):
	q = read_link_columns().where(links_table.id == link_id)

	conn = connect()
	cursor = conn.cursor()
	cursor.execute(str(q))
	link_data = cursor.fetchone()
	cursor.close()
	conn.close()

	if link_data:
		return map_to_link(link_data)

	return None

def update_link(link_id, url, name=None, description=None):

	q = Query.update(links_table)\
		.set('url', url)\
		.set('name', name)\
		.set('description', description)\
		.where(links_table.id == link_id)

	conn = connect()
	cursor = conn.cursor()
	cursor.execute(str(q))

	cursor.close()

	conn.commit()
	conn.close()

	return read(link_id)
