#!/usr/bin/env python
"""
This script will find, decompress, extract, and import an XML article for the
search_term that is provided from the PHP extension as sys.argv[1].

If the sqlite db exists, then it will be searched. Otherwise the script will
default to searching the multistream-index.txt file. The script returns "success"
to the PHP extension after the article is imported.
"""

from itertools import islice
import os
import bz2
import shutil
import sys
import csv
import random
import sqlite3
from config import *

search_term = sys.argv[1] #.replace('%27', "'")
temp_file_suffix = str(random.randint(100000, 999999))
temp_filename += temp_file_suffix
decomp_filename += temp_file_suffix
article_filename += temp_file_suffix


def search_database(search_term, sqlite_db):
    data_length = start_byte = article_id = 0
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    cursor.execute('SELECT start_byte, end_byte, article_id FROM mediawiki_articles WHERE name=? limit 1', (search_term,))
    results = cursor.fetchall()
    print(results)
    if len(results) > 0:
        article_id = str(results[0][2])
        start_byte = results[0][0]
        data_length = results[0][1] - start_byte
    return start_byte, data_length, article_id

def search_textfile(search_term, index_filename):
    byte_flag = False
    data_length = start_byte = article_id = 0
    index_file = open(index_filename, 'r')
    csv_reader = csv.reader(index_file, delimiter=':')
    for line in csv_reader:
        if not byte_flag and search_term == line[2]:
            start_byte = int(line[0])
            article_id = line[1]
            byte_flag = True
        elif byte_flag and int(line[0]) != start_byte:
            data_length = int(line[0]) - start_byte
            break
    index_file.close()
    return start_byte, data_length, article_id
        

def decompress_chunk(content_filename, start_byte, data_length):
    with open(content_filename, 'rb') as wiki_file:
        wiki_file.seek(start_byte)
        data = wiki_file.read(data_length)
    with open(temp_filename, 'wb') as temp_file:
        temp_file.write(data)
    with bz2.BZ2File(temp_filename) as fr, open(decomp_filename,"wb") as fw:
        shutil.copyfileobj(fr,fw)
    return decomp_filename

    #alternate way to slice file. faster?
    #os.system('dd if="{content_filename}" of="{temp_filename}" iflag=skip_bytes,count_bytes,fullblock bs="4096" skip="{str(start_byte)}" count="{str(data_length)}"')
       

def extract_atricle(article_id):
    #find <page>...</page> tags containing desired article_id
    counter = 0
    page_line_num = None
    id_line_num = None
    end_line_num = None
    with open(decomp_filename, 'r') as decomp_file:
        for line in decomp_file:
            if '<page>' in line:
                page_line_num = counter
            if '<id>' + article_id + '</id>' in line:
                id_line_num = counter
            if page_line_num is not None and id_line_num is not None and '</page>' in line:
                end_line_num = counter
                break
            counter += 1

    #slice file between <page>...</page> tags
    article_string = ''
    with open(decomp_filename, 'r') as decomp_file:
        decomp_slice = islice(decomp_file, page_line_num, end_line_num+1)
        for i, line in enumerate(decomp_slice, page_line_num+1):
            article_string += line
    article_string = f"""<mediawiki>{article_string}</mediawiki>"""

    with open(article_filename, 'w') as result_file:
        result_file.write(article_string)


if __name__ == '__main__':
    if os.path.isfile(sqlite_db):
        start_byte, data_length, article_id = search_database(search_term, sqlite_db)
    else:
        start_byte, data_length, article_id = search_textfile(search_term, index_filename)
    
    if data_length > 0:
        decompress_chunk(content_filename, start_byte, data_length)
        extract_atricle(article_id)
        os.system(f"""php {importdump_path} < {article_filename}""")
        print('success')

    for file_to_remove in [temp_filename, decomp_filename, article_filename]:
        if os.path.isfile(file_to_remove):
            os.remove(file_to_remove)
    
