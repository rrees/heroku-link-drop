import os

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

cur = connection.cursor();

cur.execute('SELECT * FROM collections')

results = cur.fetchall()

print(results)