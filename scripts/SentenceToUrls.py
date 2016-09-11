import re
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
        urls.append(getVideoUrl(word))

    assert(len(urls) == len(words))
    return " ".join(urls)
