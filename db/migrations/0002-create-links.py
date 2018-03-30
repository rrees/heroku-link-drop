"""
Create a links table
"""

from yoyo import step

__depends__ = ['0001-create-a-collections-table']

create_collection_table = """
CREATE TABLE links (
    id BIGSERIAL PRIMARY KEY,
    collection_id BIGSERIAL REFERENCES collections(key),
    name TEXT NOT NULL,
    description TEXT,
    url TEXT,
    created_timestamp timestamp NOT NULL DEFAULT current_timestamp,
    updated_timestamp timestamp NOT NULL DEFAULT current_timestamp
)
"""

steps = [
    step(create_collection_table, "DROP TABLE links"),
]
