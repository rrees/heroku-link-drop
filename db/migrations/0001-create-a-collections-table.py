"""
Create a collections table
"""

from yoyo import step

__depends__ = {}

create_collection_table = """
CREATE TABLE collections (
    key BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    public BOOLEAN NOT NULL,
    public_id UUID NOT NULL,
    created_timestamp timestamp NOT NULL DEFAULT current_timestamp,
    updated_timestamp timestamp NOT NULL DEFAULT current_timestamp
)
"""

steps = [
    step(create_collection_table, "DROP TABLE collections"),
]
