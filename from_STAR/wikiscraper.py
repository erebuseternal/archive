#Python File wikiscraper.py

"""
Hello, so I am going to start messing around with Solr to learn what there is to
be learned. But of course in order to do so, I need to have a data set to play
around with (and one I create to get the full feel for Solr stuff). Anywho,
Wikipedia is free and full of info so I'm going to go with that.

After looking through a number of wiki articles and their HTML I have decided
on the following way of storing them after processing with a spider.

<Title>title of page</Title>
<InfoBox>
    <first table header>value</first table header>
    <second table header>value</second table header>
    ...
</InfoBox>
<Intro>
    text
</Intro>
<First Major Heading Name>
        text
    <First Minor Heading Name>
        text
    </First Minor Heading Name>
    <Second Minor Heading Name>
        text
    </Second Minor Heading Name>
    ...
</First Major Heading Name>
<Second Major Heading Name>
    ...
</Second Major Heading Name>

Now the title's value can be found in the one <h1> tag on the page

Next comes the infobox who's values can be found in the table with
the class name 'infobox something something something'. Each header
comes in the tag th, and each value comes in the tag td

Then the Intro is imply the text after the <h1> tag and before the
first <h2> tag. The text involved is of course paragraphs and lists
from which we will just extract text and then place in individual
<div> tags (one per paragraph or list)

The Major headings are found in <h2> tags and the minor headings in
<h3> tags. The text will be treated the same as for the intro, except
that the first bit of text for the major heading is all that which
comes before the first minor heading in the html.

NOTES:  * I will be ignoring the final heading called References
        * I will ignore all those headers which have no text in
        them.
"""
import markupcreator
import re
from urllib2 import urlopen
from bs4 import BeautifulSoup

class WikiScraper:
    """
    This class will hold all of the goodies for our wikipedia scraper.
    It will take a first page when you want to initiate a crawl and will
    then optionally take a file that will tell it which articles have
    already been looked at so it can skip those links. Then it will crawl
    through wikipedia by reaching out to the first link that is not in its
    already-visited-list and then using a HTMLExtractor of our creation
    (I will set a default one) to extract the page. Finally it will write
    out the structured document that results to a directory we specify and
    then call the file the title of the article. And we simply set how many
    iterations we want.
    """

    def __init__(self, foundArticlesFile, documentDirectory):
        # directory should not be relative
        self.foundArticlesFile = foundArticlesFile
        self.documentDirectory = documentDirectory
        self.foundArticles = []
        self.newFoundArticles = [] # to keep track of what not to hit later
        self.htmlextractor = markupcreator.HTMLExtractor(documentDirectory)


        # note, this will do everything in the introduction besides the infobox
        self.Initiate()

    def Initiate(self):
        # one should recreate this function for an class inheriting from htmlextractor
        # with the self.htmlextractor.AddExtractor(...) functions you need to set up
        # your specific extractor.

        p = markupcreator.DocumentNode('p')
        ul = markupcreator.DocumentNode('ul')
        ol = markupcreator.DocumentNode('ol')
        body = markupcreator.DocumentNode('body')
        h1 = markupcreator.DocumentNode('h1')
        h2 = markupcreator.DocumentNode('h2')
        h3 = markupcreator.DocumentNode('h3')
        div = markupcreator.DocumentNode('div')

        self.htmlextractor.AddExtractor(p, self.htmlextractor.plainTextExtractor)
        self.htmlextractor.AddExtractor(ul, self.htmlextractor.plainTextExtractor)
        self.htmlextractor.AddExtractor(ol, self.htmlextractor.plainTextExtractor)
        self.htmlextractor.AddExtractor(body, self.htmlextractor.extractChildren)
        self.htmlextractor.AddExtractor(h1, self.htmlextractor.titleExtractor)
        self.htmlextractor.AddExtractor(h2, self.htmlextractor.rollingExtractor, [p, ul, ol, h3], [h2])
        self.htmlextractor.AddExtractor(h3, self.htmlextractor.rollingExtractor, [p, ul, ol], [h2, h3])
        self.htmlextractor.AddExtractor(div, self.htmlextractor.extractChildren)

    def Scrape(self, articleName, num_iterations):
        # this will handle our scraping. The first thing it does
        # is load in the foundLinks data. Then it makes sure our
        # article name is good and if not finds a good one
        # then it runs a loop num_iterations times that handles
        # articles in turn and finally once its done adds
        # the new article names to the file on found articles
        # and resets everything
        self.createFoundArticleList()
        if articleName in self.foundArticles:
            print 'article already scraped, choosing different start point'
            soup, conn = self.getArticleSoup(articleName)
            articleName = self.getNextArticle(soup)
            conn.close()
            print 'new start point is: %s' % articleName
        for i in range(0, num_iterations):
            print 'scraping: %s' % articleName
            articleName = self.handleArticle(articleName)
            print 'article scrape complete'
        # now we update our found articles file
        self.addToArticleDirectory()
        # and reset
        self.newFoundArticles = []
        self.foundArticles = []
        print 'Scraping Complete! :D'


    def handleArticle(self, articleName):
        # this will take an article name, handle it and send out another
        # article name. Does not check input article name itself,
        # but does check that the returned name is good

        # first we get the soup and the connection
        soup, conn = self.getArticleSoup(articleName)
        # next we add the soup to our extractor
        self.htmlextractor.AddSoup(soup)
        # now we extract
        self.htmlextractor.ExtractHTML()
        # now noting that h1 tag will come first we get the title
        title = self.htmlextractor.document.nodes[0].content
        # now we export
        file_name = title
        self.htmlextractor.document.Export(file_name)
        # now we set it as one of the newbies
        self.newFoundArticles.append(articleName)
        self.foundArticles.append(articleName)
        # now we get the next article
        nextArticleName = self.getNextArticle(soup)
        # finally we close the connection
        conn.close()
        self.htmlextractor.initializeState() # reset the state
        return nextArticleName

    # the following function takes an article name and returns a the wikipedia
    # url for that article
    def createUrl(self, articleName):
    	# wikipedia articles are in urls like
    	# https://en.wikipedia.org/wiki/articleName
    	stnd_articleName = ''
    	for letter in articleName:
    		if letter == ' ':
    			stnd_articleName = stnd_articleName + '%20'
    		else:
    			stnd_articleName = stnd_articleName + letter
    	return 'https://en.wikipedia.org/wiki/' + stnd_articleName

    def getArticleSoup(self, articleName):
    	# this just converts the articleName to a url, fetches the page
    	# and turns it into soup, using lxml and beautifulsoup
    	url = self.createUrl(articleName)
    	html = urlopen(url)
    	wikisoup = BeautifulSoup(html, 'lxml')
    	return wikisoup, html  # note we return both the soup and the connection

    def getNextArticle(self, wikisoup):
    	links = wikisoup.find_all(href=re.compile('^/wiki/[^:]*$')) # article
    		# links follow this pattern
    	for link in links:
    		if not (link['href'][6:] in self.foundArticles):
    			return link['href'][6:]	# return the first one not
    				# in foundArticles

    def addToArticleDirectory(self):
    	# this will append a new line to the end of the directory
    	file = open(self.foundArticlesFile, 'a')
        for name in self.newFoundArticles:
    	       file.write((name+'\n').encode('utf-8'))
    	file.close()

    def createFoundArticleList(self):
    	file = open(self.foundArticlesFile, 'r')
    	for line in file:
    		self.foundArticles.append(line[:-1])	# don't want to grab the /n
