#Python File indexdocs.py

"""
This is just a shortcut for me so I can do this really easily.
"""

import os
import subprocess

def formatString(string):
    # replaces spaces with %20's
    words = string.split(' ')
    final_string = words[0]
    for i in range(1, len(words)):
        final_string = final_string + '%20' + words[i]
    return final_string

command_preface = 'curl http://localhost:8983/solr/core1/update -H "Content-Type: text/xml" --data-binary @'
directory = 'ArticlesSolr'
for filename in os.listdir(directory):
    filename = formatString(filename)
    print(command_preface + directory + '/' + filename)
    os.system(command_preface + directory + '/' + filename)
# now we commit
print(command_preface[:-1] + "'<commit waitSearcher=\"false\" />'")
os.system(command_preface[:-1] + "'<commit waitSearcher=\"false\" />'")
