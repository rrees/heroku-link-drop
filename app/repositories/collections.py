import datetime
import uuid

from pypika import Table, Query, Order

from . import models
from .connection import connect

collections_table = Table('collections')

def map_to_collection(result):
    if not result:
        return None

    return models.Collection(
        key = result[0],
        name = result[1],
        public = result[2],
        public_id = result[3],
    )

def execute_and_commit(statement):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(str(statement))
        cursor.close()
        conn.commit()


def query_collection():
    return Query.from_(collections_table)\
        .select('key', 'name', 'public', 'public_id')

def all(order_column=None, sort_descending=False, filter_by_name=None):

    if not order_column:
        order_column = 'updated_timestamp'

    sort_order = Order.desc if sort_descending else Order.asc

    
    q = query_collection().orderby(order_column, order=sort_order)

    if filter_by_name:
        q = q.where(collections_table.name.ilike(f'%{filter_by_name}%'))

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(str(q))
        results = [map_to_collection(r) for r in cursor.fetchall()]
        cursor.close()
    
    return results

def create(name, description=None, public=False):

    public_id = str(uuid.uuid4())
    insert_statement = Query.into(collections_table)\
        .columns('name', 'description', 'public', 'public_id')\
        .insert(name, description, public, public_id)
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(str(insert_statement) + 'RETURNING key')
    collection_id = cursor.fetchone()

    cursor.close()

    conn.commit()
    conn.close()

    return collection_id

def read(key):
    q = query_collection()\
        .where(collections_table.key == key)

    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(str(q))
            result = cursor.fetchone()

    return map_to_collection(result)

def read_public(identifer):
    q = query_collection()\
        .where(collections_table.public_id == identifer)

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(str(q))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return map_to_collection(result)

def public(public_flag):
    q = Query.update(collections_table).set(collections_table.public, public_flag)
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(str(q))
    cursor.close()
    conn.commit()
    conn.close()
    return public_flag

def update(key, name, description=None):
    q = Query.update(collections_table).set(collections_table.name, name).set(collections_table.updated_timestamp, datetime.datetime.now())

    if description:
        q = q.set(collections_table.description, description)

    q = q.where(collections_table.key == key)

    execute_and_commit(q)

def touch_collection(key):
    q = Query.update(collections_table).set(collections_table.updated_timestamp, datetime.datetime.now()).where(collections_table.key == key)

    execute_and_commit(q)


def delete(key):
    q = Query.from_(collections_table).where(collections_table.key == key).delete()

    execute_and_commit(q)