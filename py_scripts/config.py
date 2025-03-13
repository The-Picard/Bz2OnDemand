#!/usr/bin/env python

#These files need to be downloaded first. Scripts need read permissions.
#https://dumps.wikimedia.org/
index_filename = '/var/lib/mediawiki/extensions/Bz2OnDemand/py_scripts/enwiki-20250301-pages-articles-multistream-index.txt'
content_filename = '/var/lib/mediawiki/extensions/Bz2OnDemand/py_scripts/enwiki-20250301-pages-articles-multistream.xml.bz2'

#These files will be created by the extension. Scripts need read and write permissions for these paths.
sqlite_db = '/var/lib/mediawiki/extensions/Bz2OnDemand/py_scripts/bz2_search_index.db'
temp_filename = '/tmp/chunk-multistream.xml.bz2'
decomp_filename = '/tmp/chunk-multistream.xml'
article_filename = '/tmp/article.xml'
importdump_path = '/var/lib/mediawiki/maintenance/importDump.php'

