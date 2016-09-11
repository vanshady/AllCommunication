import re, sys
from AslVideoScraper import getVideoUrl

# gets ASL video URLs to all words in the given sentence in order
# if a word is not found, its corresponding URL will be None
# returns all the URLs as a single string, separated by spaces
def getVideoUrls(sentence):
    words = re.sub("[^\w]", " ",  sentence).split()

    if (len(words) == 0):
        return None

    urls = []
    for word in words:
        url = getVideoUrl(word)
        if (url == None):
            url = "None"
        urls.append(url)

    assert(len(urls) == len(words))
    return " ".join(urls)

print(getVideoUrls(sys.argv[1]))