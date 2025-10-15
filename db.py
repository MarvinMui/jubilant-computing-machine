import duckdb
import os
import pandas as pd

SCHEMA_PATH = os.path.join('db', 'schema.sql')
DB_PATH = os.path.join('db', 'cmdb.db')
def init_db():
    if os.path.exists(SCHEMA_PATH):
        with duckdb.connect(DB_PATH) as con:
            with open(SCHEMA_PATH, "r") as f:
                # Create the DB schema
                con.sql(f.read())
                # # Import data
                # con.sql("COPY inspections from ")
    else:
        print("You must create a file named schema.sql as described above.")

# def get_connection():
#     """Return a DuckDB connection object."""
#     return duckdb.connect(os.path.join('db', 'schema.sql'))