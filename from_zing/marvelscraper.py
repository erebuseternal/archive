from SpiderWoman.action import Action

def bold(tag):
    return tag.b.get_text().strip()

def unmarkedtext(tag):
    string = ''
    count = 0
    for child in tag.children:
        if count > 1:
            try:
                string = string + child.get_text()
            except:
                string = string + child
        count += 1
    return string

def text(tag):
    return tag.get_text().strip()

def width(tag):
    return tag.attrs['style']

def content(tag):
    return 'Content'

weapons = {'bold': bold, 'unmarkedtext': unmarkedtext, 'text': text, 'width': width, 'content': content}

from urllib2 import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://marvel.com/universe/Scarlet_Witch_%28Wanda_Maximoff%29').read()
soup = BeautifulSoup(html, 'lxml')

action = Action()
action.SetWeapons(weapons)
action.SetVillain(soup)
action.LoadPlan('marvelscraper.css')
action.Act()
beaten = action.DumpVillain()
print(beaten)

import re

expre = re.compile('width:([0-9]{1,})px;')
for key in beaten:
    if key == 'Content':
        values = beaten[key]
        content = ''
        for value in values:
            content = content + value
        beaten[key] = content
        continue
    match = re.search(expre, beaten[key][0])
    if match:
        if match.group(1) == '21':
            beaten[key] = 1
        elif match.group(1) == '42':
            beaten[key] = 2
        elif match.group(1) == '63':
            beaten[key] = 3
        elif match.group(1) == '84':
            beaten[key] = 4
        elif match.group(1) == '105':
            beaten[key] = 5
        elif match.group(1) == '126':
            beaten[key] = 6
        else:
            beaten[key] = 7
    else:
        value = beaten[key][0]
        values = value.split(',')
        new_values = []
        for value in values:
            value = value.strip()
            new_values.append(value)
        beaten[key] = new_values
print(beaten)
