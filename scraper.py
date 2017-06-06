# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful


import requests
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime

# Open page
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
    scraperwiki.sqlite.save(unique_keys=['name'],data={"name": url, "from": "NOAA"}, table_name="metadata")
    for item in souppage.find_all('a'):
        # Create the url, and save to the database
        link = url + '/' + item.get('href')
        scraperwiki.sqlite.save(unique_keys=['l'], data={"l": link, "d": todays_date })
        print(link)

if __name__ == '__main__':
    url = 'https://www1.ncdc.noaa.gov/pub/data/15min_precip-3260'
    page = geturl(url)
    souppage = getsouppage(page)
    getlinks(souppage,url)

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
