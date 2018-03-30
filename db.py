import os
import uuid

import dsnparse

import pg8000

db_env = os.environ.get('DATABASE_URI', None)

r = dsnparse.parse_environ('DATABASE_URI')

connection = pg8000.connect(
    r.user,
    host=r.host,
    database=r.database,
    password=r.password,
    ssl=True,
    )

def show_table_contents():
    cur = connection.cursor();

    cur.execute('SELECT * FROM collections')

    results = cur.fetchall()

    print(results)

    cur.execute('SELECT * FROM links')

    results = cur.fetchall()

    print(results)

def create_collection(name, description=None, public=False):
    public_id = uuid.uuid4()

    insert = """
    INSERT INTO collections (
        name,
        description,
        public,
        public_id)
    VALUES (
        %s,
        %s,
        %s,
        %s
    )
    """

    cursor = connection.cursor()
    cursor.execute(insert, (
        name,
        description,
        public,
        public_id
        ))
    connection.commit()
    cursor.close()

def add_link(collection_id, url, name=None, description=None):
    insert = """
    INSERT INTO links (
        url,
        name,
        description,
        collection_id
    ) VALUES (
        %s,
        %s,
        %s,
        %s
    ) RETURNING id
    """

    cursor = connection.cursor()
    cursor.execute(insert,(
        url,
        name,
        description,
        collection_id,
    ))

    result = cursor.fetchone()

    print(result)

    print(result.pop())

    connection.commit()
    cursor.close()

show_table_contents()
create_collection("Test")
show_table_contents()
add_link(7, "https://www.example.com")
show_table_contents()