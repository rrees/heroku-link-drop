import os

import dsnparse
import pg8000
from pypika import Table, Query

DATABASE_URI = os.environ['DATABASE_URI']

collections_table = Table('collections')
r = dsnparse.parse(DATABASE_URI)

def connect():
    return pg8000.connect(r.username,
        host=r.host,
        password=r.password,
        database=r.paths[0],
        ssl=True)

def all():
    q = Query.from_(collections_table).select("*")

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(str(q))
    results = [r for r in cursor.fetchall()]
    cursor.close()
    conn.close()
    return results

def create_collection(name):
    pass