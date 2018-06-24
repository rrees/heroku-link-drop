import os
import uuid

import dsnparse
import pg8000
from pypika import Table, Query

from . import models

DATABASE_URI = os.environ['DATABASE_URI']

collections_table = Table('collections')
r = dsnparse.parse(DATABASE_URI)

def map_to_collection(result):
    return models.Collection(
        key = result[0],
        name = result[1],
        public = result[2]
    )

def connect():
    return pg8000.connect(r.username,
        host=r.host,
        password=r.password,
        database=r.paths[0],
        ssl=True)

def all():
    q = Query.from_(collections_table).select('key', 'name', 'public')

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(str(q))
    results = [map_to_collection(r) for r in cursor.fetchall()]
    cursor.close()
    conn.close()
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