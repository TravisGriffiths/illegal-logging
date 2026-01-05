from .tables import ORIGINS

rm_table_sql = f"""DROP TABLE IF EXISTS {ORIGINS};"""

create_table_sql = f"""CREATE TABLE {ORIGINS} (
    id INTEGER PRIMARY KEY,
    city TEXT,
    state TEXT,
    name TEXT,
    longitude REAL,
    latitude REAL
)"""