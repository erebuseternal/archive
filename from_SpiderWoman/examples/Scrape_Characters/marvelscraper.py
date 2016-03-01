import sys
from SpiderWoman import WikiSpider

num = int(sys.argv[1])

# our scraping function
def text(tag):
    return tag.get_text().strip()

# our name -> function dictionary
weapons = {'text' : text}

# the function that will evaluate whether we record the page or not
def is_worth(fields):
    if 'Real Name' in fields:
        return True
    return False

# our function to store (or in this case diplay) our page
def store(fields):
    print(fields['Real Name'])

# create the spider
spider = WikiSpider('https://marvel.wikia.com', 'http://marvel.wikia.com/wiki/Jessica_Jones_%28Earth-616%29', 'marvel.css', weapons)
# run the spider
spider.Go(num, store, is_worth)
