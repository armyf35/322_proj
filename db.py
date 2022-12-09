import sqlite3
import click
from flask import current_app, g


conn = sqlite3.connect('database.sqlite3')

with open('schema.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()
cur.execute("SELECT * FROM sqlite_master;")

conn.commit()
conn.close()
