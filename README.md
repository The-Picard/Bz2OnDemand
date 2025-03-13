**Bz2OnDemand** is an extension for MediaWiki that can decompress articles from `multistream.xml.bz2` Wikipedia dumps, for example `enwiki-20250301-pages-articles-multistream.xml.bz2`, and import them into the MediaWiki database on demand, as they are requested by users. This allows MediaWiki to serve articles from large data dumps without the time consuming process of importing them all into the MediaWiki database.

Instead of one long time comsuming process to import the entire database, **Bz2OnDemand** adds a small amount of latency when a new article is loaded. Most of this latency is from seraching the `multistream-index.txt` file to find the byte positions of the requested article. This serach latency can be reduced by indexing the `multistream-index.txt` data into a sqlite database using the `create_index_db.py` script.

1. **Python is required.** Use this command to check your python installation:
   ```bash
   python3 --version
   ``` 


2. **Download the compressed XML dump and index files,** for example: `enwiki-20250301-pages-articles-multistream.xml.bz2` and also the corresponding index file: `enwiki-20250301-pages-articles-multistream-index.txt.bz2`.
https://meta.wikimedia.org/wiki/Data_dump_torrents
https://dumps.wikimedia.org/backup-index.html

3. **Decompress the `index.txt.bz2` file into plain text:**
   ```bash
   bzip2 -d enwiki-20250301-pages-articles-multistream-index.txt.bz2
   ``` 

4. **Clone the repo into your extensions folder.** For this example, I have mediawiki installed at `/var/lib/mediawiki/`. Use the correct path to your mediawiki installation.
   ```bash
   cd /var/lib/mediawiki/extensions/
   git clone https://github.com/The-Picard/Bz2OnDemand
   ``` 

5. **Move the dump file `multistream.xml.bz2` and text file `multistream-index.txt`** into the `extensions/Bz2OnDemand/py_scripts` folder
   ```bash
   mv enwiki-20250301-pages-articles-multistream-index.txt /var/lib/mediawiki/extensions/Bz2OnDemand/py_scripts/enwiki-20250301-pages-articles-multistream-index.txt
   mv enwiki-20250301-pages-articles-multistream.xml.bz2 /var/lib/mediawiki/extensions/Bz2OnDemand/py_scripts/enwiki-20250301-pages-articles-multistream.xml.bz2
   ``` 

6. **Change the file paths used by python scripts in `config.py`**
   ```bash
   cd /var/lib/mediawiki/extensions/Bz2OnDemand/py_scripts
   nano config.py
   ``` 
   
7. **Register the extension in MediaWiki's LocalSettings.php file** and remove the option to create new articles, so that the hook `ShowMissingArticle` is triggered.
   ```bash
   cd /var/lib/mediawiki/
   nano LocalSettings.php
   ``` 
   Add these two lines to the end of the file:
   ```bash
   $wgGroupPermissions['*']['createpage'] = false;
   wfLoadExtension('Bz2OnDemand');
   ``` 

8. **Create sqlite database from `multistream-index.txt` to improve performance (optional)** This script should take <5 minutes to run, and it will create a .db file that is about the same size as the file `multistream-index.txt`. After the database is created, the file `multistream-index.txt` can be removed.
   ```bash
   cd /var/lib/mediawiki/extensions/Bz2OnDemand/py_scripts/
   python3 create_index_db.py
   ```
   
9. **Log out** so that you do not have the option to create new articles, and instead you will trigger the `ShowMissingArticle` hook. There is probably a better hook to use so that this is not necessary, and `$wgGroupPermissions['*']['createpage'] = false;` is not needed.

