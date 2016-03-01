#Python File
"""
This is going to be a web scraper. Particularly made for scraping wikipedia.
The purpose of this crawler is to be given a start article and a list of 
articles already found. Then, for the first article we are going to make sure
it has not already been found, and then if it hasn't grab the body. Then, we will 
perform the following. We will start grabbing links (in order), for the first
link we have not already got the article for, we will jump to that page and grab
the body and repeat (but with the links now on that page). For each body that we
grab we will strip it from a text document into a container and then will save
the container as a file in Containers with the same name as its article. We will
also append the name of the article to a file which contains the list of all 
articles found. We shall run our spider for a PREDEFINED number of times. This
number will be specified at the launch of the program. 

So inputs are: articlesFound file, first_article_name, number of times to run
(all of this called if we are in __main__) 
"""

import re
from bs4 import BeautifulSoup
from urllib import urlopen # urlopen opens url's as if they are a filehandle

# the following function takes an article name and returns a the wikipedia
# url for that article
def createUrl(articleName):
	# wikipedia articles are in urls like 
	# https://en.wikipedia.org/wiki/articleName
	stnd_articleName = ''
	for letter in articleName:
		if letter == ' ':
			stnd_articleName = stnd_articleName + '%20'
		else:
			stnd_articleName = stnd_articleName + letter
	return 'https://en.wikipedia.org/wiki/' + stnd_articleName


def getAllContent(wikisoup):
	# the content of a wiki article is found in its <p> tags
	# I am also going to signal the start of a new paragraph with <p>
	paragraphs = wikisoup.find_all('p')
	content = ''
	for paragraph in paragraphs:
		content = content + '<p>' +  paragraph.get_text()
	return content

def getNextArticle(wikisoup, foundArticles):
	links = wikisoup.find_all(href=re.compile('^/wiki/[^:]*$')) # article
		# links follow this pattern
	for link in links:
		if not (link['href'][6:] in foundArticles):
			return link['href'][6:]	# return the first one not
				# in foundArticles

def getArticleSoup(articleName):
	# this just converts the articleName to a url, fetches the page
	# and turns it into soup, using lxml and beautifulsoup
	url = createUrl(articleName)
	html = urlopen(url)
	wikisoup = BeautifulSoup(html, 'lxml')
	return wikisoup, html

def writeFile(text, fileName, directory):
	file = open(directory + '/' + fileName + '.txt', 'w')
	file.write(text.encode('utf-8'))
	file.close()

def copyArticle(articleName, foundArticles, ARTICLE_DIR):
	# this will copy the articles content into a text document
	# and return the next link
	soup, conn = getArticleSoup(articleName)
	next_article = getNextArticle(soup, foundArticles)
	content = getAllContent(soup)
	writeFile(content, articleName, ARTICLE_DIR)
	conn.close()
	return next_article 

def addToArticleDirectory(articleName, articleDirectory):
	# this will append a new line to the end of the directory
	file = open(articleDirectory, 'a')
	file.write((articleName+'\n').encode('utf-8'))
	file.close()

def createFoundArticleList(articleDirectory):
	foundArticles = []
	file = open(articleDirectory, 'r')
	for line in file:
		foundArticles.append(line[:-1])	# don't want to grab the /n
	return foundArticles

# NOW WE PUT EVERYTHING TOGETHER!
import sys
if __name__ == '__main__':
	arguments = sys.argv
	# arguments should come as articleDirectory, directory for Articles,
	# and then the first article name, and finally the number of iterations
	# to run
	articleDirectory = arguments[1] # file with names of articles found
	ARTICLE_DIR = arguments[2] # directory where articles are stored
	articleName = arguments[3] # article to begin your search
	num_iterations = int(arguments[4]) # number of articles to find

	# first we get our foundArticles list
	foundArticles = createFoundArticleList(articleDirectory)
	
	# now we check to see if articleName is in found articles and act 
	# accordingly
	if articleName in foundArticles:
		print('selecting different first article')
		soup, conn = getArticleSoup(articleName)
		articleName = getNextArticle(soup, foundArticles)
		conn.close()
		print('article chosen: ' + articleName)
	
	# now we go ahead and run our iterations
	for i in range(0, num_iterations):
		print(articleName)
		next_articleName = copyArticle(articleName, foundArticles, ARTICLE_DIR)
		foundArticles.append(articleName)
		addToArticleDirectory(articleName, articleDirectory)
		articleName = next_articleName

