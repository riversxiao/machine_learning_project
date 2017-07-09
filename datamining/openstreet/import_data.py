
# coding: utf-8

import sqlite3
import csv
from pprint import pprint


sqlite_file = 'mydb.db'    # name of the sqlite database file

# Connect to the database
conn = sqlite3.connect(sqlite_file)

#create the curosr for delete table and create table
cur = conn.cursor()

# flush the database
cur.execute('''DROP TABLE IF EXISTS nodes_tags''')
cur.execute('''DROP TABLE IF EXISTS nodes''')
cur.execute('''DROP TABLE IF EXISTS ways_tags''')
cur.execute('''DROP TABLE IF EXISTS ways_nodes''')
cur.execute('''DROP TABLE IF EXISTS ways''')
conn.commit()

# Create the table, specifying the column names and data types
cur.execute('''
    CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT,category TEXT)
''')
cur.execute('''
    CREATE TABLE nodes(id INTEGER,lat REAL,lon REAL,user TEXT,uid INTEGER,version INTEGER,changeset INTEGER,timestamp TEXT)
''')
cur.execute('''
    CREATE TABLE ways_nodes(id INTEGER,node_id INTEGER,position INTEGER)
''')
cur.execute('''
    CREATE TABLE ways_tags(id INTEGER, key TEXT, value TEXT,category TEXT)
''')
cur.execute('''
    CREATE TABLE ways(id INTEGER,user TEXT,uid INTEGER,version INTEGER,changeset INTEGER,timestamp TEXT)
''')

# commit the changes
conn.commit()

# import nodes_tags.csv to sqlite

with open('nodes_tags.csv','r') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['key'],i['value'], i['category']) for i in dr]
# insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value,category) VALUES (?, ?, ?, ?);", to_db)

with open('nodes.csv','r') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'],i['lat'],i['lon'],i['user'],i['uid'],i['version'], i['changeset'],i['timestamp']) for i in dr]
cur.executemany("INSERT INTO nodes(id, lat, lon,user,uid,version,changeset,timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)


with open('ways_tags.csv','r') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['key'],i['value'], i['category']) for i in dr]
cur.executemany("INSERT INTO ways_tags(id, key, value, category) VALUES (?, ?, ?, ?);", to_db)


with open('ways_nodes.csv','r') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['node_id'],i['position']) for i in dr]
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_db)


with open('ways.csv','r') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['user'],i['uid'], i['version'],i['changeset'],i['timestamp']) for i in dr]
    
cur.executemany("INSERT INTO ways(id, user, uid,version,changeset,timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)


# commit the changes to the database
conn.commit()


# close the connection
conn.close()





