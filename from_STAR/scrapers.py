# Python File scrapers.py
"""
This file will contain the various scrapers and their HTMLExtractors that I use
in this project.
"""

from wikiscraper import WikiScraper
from markupcreator import HTMLExtractor, DocumentNode
import re

"""
So the first scraper is going to be a ridiculously simple one. It will grab
the title from the h1 tag, then it will grab the first table (which will be
the infobox), and finally it will grab the the first paragraphs before the first
h2 tag. All of this will be thrown into text as Title, InfoBox, and then
Introduction
"""

class SimpleExtractor(HTMLExtractor):
    # all we need to do is define the right extractors herein that take advantage
    # of self.state

    def initializeState(self):
        self.state = [False, False, False] # the first entry is for title
                                            # the second for infobox
                                            # the third for intro

    def introductionExtractor(self, tag):
        if self.state[2] == True:
            return tag.next_sibling
        # we should have the infobox by now, so just going to check for it
        if self.state[1] == False:
            self.document.CreateNode('InfoBox')
            self.document.FinishNode()

        # okay so this is the first paragraph we are seeing
        content = ''

        while tag.name != 'h2':
            if tag.name == 'p':
                content = content + tag.get_text() + '\n'
            tag = tag.next_sibling
            if isinstance(tag, str):
                tag = tag.next_sibling

        self.document.CreateNode('Introduction')
        self.document.AddContent(content)
        self.document.FinishNode()

        self.state[2] = True
        return tag

    def infoBoxExtractor(self, tag):
        if self.state[1] == True:
            return tag.next_sibling
        if not 'class' in tag.attrs:
            return tag.next_sibling
        ex = re.compile('infobox')
        if not ex.match(tag.attrs['class'][0]):
            return tag.next_sibling

        # this is thus the first table we are seeing
        content = ''

        # so we are going to want to go through the children of
        # the table body and grab their children. we will thus
        # end up seeing td tags and we will extract the text from
        # these
        children = tag.children

        for child in children:
            if not child.name:
                continue
            for baby in child.children:
                # now we are at the td level
                if baby.name == 'td':
                    content = content + baby.get_text() + '\n'

        self.document.CreateNode('InfoBox')
        self.document.AddContent(content)
        self.document.FinishNode()

        self.state[1] = True
        return tag.next_sibling

class SimpleScraper(WikiScraper):

    def Initiate(self):
        self.htmlextractor = SimpleExtractor(self.documentDirectory)

        body = DocumentNode('body')
        div = DocumentNode('div')
        p = DocumentNode('p')
        h1 = DocumentNode('h1')
        table = DocumentNode('table')

        self.htmlextractor.AddExtractor(body, self.htmlextractor.extractChildren)
        self.htmlextractor.AddExtractor(div, self.htmlextractor.extractChildren)
        self.htmlextractor.AddExtractor(h1, self.htmlextractor.titleExtractor)
        self.htmlextractor.AddExtractor(p, self.htmlextractor.introductionExtractor)
        self.htmlextractor.AddExtractor(table, self.htmlextractor.infoBoxExtractor)
