import os

import dsnparse
import pg8000


DATABASE_URI = os.environ['DATABASE_URL']

r = dsnparse.parse(DATABASE_URI)

def connect():
    return pg8000.connect(r.username,
        host=r.host,
        password=r.password,
        database=r.paths[0],
        ssl=True)