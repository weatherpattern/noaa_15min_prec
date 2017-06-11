# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

#TODO:
import scraperwiki
import requests
import json
from datetime import datetime
import hashlib

### Add your own imports
from bs4 import BeautifulSoup


def initialize(url,UUID):
    """
    Should be called at the beginning of every scrape run (TODO: perhaps turn this into a decorator pattern)
    Creates the table for the runs metadata, and stores a timestamp, the http response headers, response body, and a SHA-256 hash of the body
    """
    makeTable()
    currentTime = str(datetime.now())
    r = requests.get(url)
    headers = json.dumps(dict(r.headers)) #json-serialized headers
    content = r.content #response body, TODO: may need to handle binary data differently vs html
    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest() #SHA-256 hash of body - text is first encoded as utf-8 b/c sha256 expects binary; output is then converted back as a hexadecimal string representation for storage
    payload = {'url':url,\
            'UUID':UUID,\
            'timestamp':currentTime,\
            'body_content':content,\
            'body_SHA256':content_hash,\
            'headers':headers}
    scraperwiki.sqlite.save(unique_keys=[],data=payload,table_name='runs_metadata') #saves to sqlite
    current_run_id = scraperwiki.sqlite.execute("""
            SELECT seq FROM sqlite_sequence WHERE NAME="runs_metadata"
            """) #Gets the most recent run_id associated w/ the entry we just added
    return current_run_id

def makeTable():
    """
    Creates a table in the sqlite db for keeping track of runs
    """
    scraperwiki.sqlite.execute("""
                    CREATE TABLE IF NOT EXISTS runs_metadata (
                    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    UUID TEXT,
                    timestamp TEXT,
                    body_content TEXT,
                    body_SHA256 TEXT,
                    headers TEXT
                    )""")
### Add your methods
def geturl(url):
    try:
        ## Access url
        page = requests.get(url)
        return page
    except:
        print ('Error accessing url')
        return

def getsouppage(page):
    # Create beautifulsoup object from page
    # Requests URL object -> BeautifulSoup page object
    souppage = BeautifulSoup(page.content,"html.parser")
    return souppage

def getlinks(souppage,url):
    # Get today's date
    todays_date = str(datetime.now())
    # Loop through lines of the html with an 'a' tag
    datadict={"name": url, "from": "NOAA"}
    #scraperwiki.sqlite.save(unique_keys=['name'],data={"name": url, "from": "NOAA"}, table_name="metadata")
    for item in souppage.find_all('a'):
        # Create the url, and save to the database
        link = url + '/' + item.get('href')
        scraperwiki.sqlite.save(unique_keys=['l'], data={"l": link, "d": todays_date })
        print(link)

def scrape(url,UUID):
    """
    This is the function that users should modify: they should make sure to store the run_id along with their data. Data should be saved to the sqlite table "data".
    Data can be saved using scraperwiki module via:
    scraperwiki.sqlite.save(unique_keys,data=dictionary_of_data,table_name='data')
    or any other connection capable of writing to the local sqlite db named data.sqlite
    """
    run_id = initialize(url,UUID)
    page = geturl(url)
    souppage = getsouppage(page)
    getlinks(souppage,url)


    return

if __name__ == '__main__':
    url = 'https://www1.ncdc.noaa.gov/pub/data/15min_precip-3260'
    UUID = '0000'
    scrape(url,UUID)
