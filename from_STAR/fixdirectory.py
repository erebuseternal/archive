#Python File fixdirectory.py
def formatString(string):
    # replaces spaces with %20's
    words = string.split(' ')
    string = words[0]
    for i in range(1, len(words)):
        string = string + '%20' + words[i]
    words = string.split('(')
    string = words[0]
    for i in range(1, len(words)):
        string = string + '%28' + words[i]
    words = string.split(')')
    string = words[0]
    for i in range(1, len(words)):
        string = string + '%29' + words[i]
    return string

import os
def fixDirectory(directory):
    for filename in os.listdir(directory):
        new_filename = formatString(filename)
        os.rename(directory + '/' + filename, directory + '/' + new_filename)
