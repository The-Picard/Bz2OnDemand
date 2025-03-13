#!/usr/bin/env python
"""
Creates a sqlite database from multistream-index.txt
"""

import sqlite3
import csv
from config import sqlite_db, index_filename

def process_queue(article_queue, end_byte):
    for article in article_queue:
        cursor.execute('INSERT INTO mediawiki_articles (article_id, name, start_byte, end_byte) VALUES (?, ?, ?, ?)', (article['article_id'], article['name'], article['start_byte'], end_byte))

# Connect to the database (or create it if it doesn't exist)
connection = sqlite3.connect(sqlite_db)
cursor = connection.cursor()

# Create a table (if it doesn't exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mediawiki_articles (
        id INTEGER PRIMARY KEY,
        article_id INTEGER,
        name TEXT,
        start_byte INTEGER,
        end_byte INTEGER
    )
''')

# Insert data into the table
with open(index_filename, 'r') as file:
    reader = csv.reader(file, delimiter=':')
    article_queue = []
    start_byte_flag = None
    for row in reader:
        if start_byte_flag != row[0]:
            process_queue(article_queue, row[0])
            article_queue = []
            start_byte_flag = row[0]
        article_queue.append({'article_id':row[1], 'name':':'.join(row[2:]), 'start_byte':row[0]})
    process_queue(article_queue, None)
        
# Commit the changes and close the connection
connection.commit()
connection.close()

