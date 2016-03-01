"""
Our Superhero can now defeat the villains. Now she must be able to find villains
in the first place and not repeat herself. So we are going to make a VillainTracker!
This is going to take the soup for the current page and do a couple of things
(in theory, you yourself will have to program in the actual implementation).

The first thing is that it will assign a unique id to the page based off of its
soup. The easiest way of doing this is of course a hash over the page text. So
that's what I will do. Then it will save these hashes to make sure that you don't
repeat yourself (or at least make it very unlikely).

The main method for this class is the FindVillain, which will use an input function
for getting the next batch of soup from the current one to go ahead and find
the next 'villain'. Note that to find the first one, the VillainTracker needs
to be seeded.

Finally you can call GetFinishedVillains() to retrieve the hashes found
You can upload hashes with LoadFinishedVillains(hashes)
"""

from copy import copy

class VillainTracker:

    def __init__(self, tracking_device, seed, get_unique=True):
        self.hasher = hash  # we set it to the built in hash funtion
                            # this way you can reset things if you like
        self.get_unique = get_unique    # this allows us to turn off page
                                        # uniqueness if we are interested
                                        # in other kinds of data
        self.hashes = []
        self.tracking_device = tracking_device          # this is a function that takes
                                        # only the soup and returns the soup
                                        # for a new page (the next one)
        self.soup = seed                # our seed is our first soup
        self.max_tries = 1000           # this is how many tries to find a unique
                                        # villain the VillainTracker will make
                                        # before quitting

    def FindVillain(self):
        # this is what the VillainTracker calls. If get_unique is true it
        # will keep calling the user's function until a unique hash is found
        # otherwise it just calls the user's function once and returns
        if not self.get_unique:
            return self.getNextLink(self.soup)
        else:
            link = self.getNextLink(self.soup)
            link_hash = self.hashLink(link)
            count = 0
            while link_hash in self.hashes:
                print("Link already found, will try for new one.")
                link = self.getNextLink(self.soup)
                link_hash = self.hashLink(link)
                count += 1
                if count == self.max_tries:
                    return None
            self.hashes.append(link_hash)
            try:
                new_soup = self.tracking_device.CreateSoup(link)
                self.soup = new_soup
            except:
                print('Could not connect, trying for new link')
                new_soup = self.FindVillain()
            return new_soup


    def hashLink(self, link):
        return self.hasher(link)

    def getNextLink(self, soup):
        return self.tracking_device.NextLink(soup)

    def GetFinishedVillains(self):
        return copy(self.hashes)

    def LoadFinishedVillains(self, hashes):
        self.hashes.extend(copy(hashes))

from random import randint
from urllib2 import urlopen
from bs4 import BeautifulSoup
import re

class TrackingDevice:

    def CreateSoup(self, url):
        # should take an absolute url and return soup
        pass

    def NextLink(self, soup):
        # should take soup and return an absolute url
        pass

# example of a tracking device
class WikiTrackingDevice(TrackingDevice):

    def __init__(self, base_url):
        self.base = base_url

    def CreateSoup(self, url):
        response = urlopen(url)
        html = response.read()
        seed = BeautifulSoup(html, 'lxml')
        return seed

    def NextLink(self, soup):
        links = soup.find_all('a', href=re.compile('^\/wiki\/[^:?#]{1,}$'))
        index = randint(0, len(links) - 1)
        link = links[index]
        href = link['href']
        print("Trying link: " + self.base + href)
        return self.base + href
