from string import ascii_letters
import requests
import sys
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sys

# only call this method from outside
# gets link to an ASL video of the given word, or None if word not found
def getVideoUrl(word):
    wordPage = querySigningsavvy(word)
    
    if (wordPage == None):
        return None
    
    return scrapeVideoUrl(wordPage)

# queries https://www.signingsavvy.com for the given word
# and returns the URL to this word's page, or None if word not found
def querySigningsavvy(word):
    assert(isWord(word))

    word = word.upper()
    domain = "https://www.signingsavvy.com/"
    queryUrl = domain + "search/" + word
    soup = getWebpageSource(queryUrl)
    queryResults = soup.findAll("div", {"class": "search_results"})

    wordTags = []
    for queryResult in queryResults:
        wordTag = queryResult.find("a", text = word)
        if (wordTag != None):
            wordTags.append(wordTag)

    if (len(wordTags) == 0):
        return None
    # TODO:
    # there may be multiple entries for the same word if it has more than
    # one meaning: we'll need to select one; but for now, use the first result

    wordTag = wordTags[0]
    wordRelativeUrl = wordTag["href"]
    result = domain + wordRelativeUrl

    assert(word in result)
    return result

# gets link to the ASL video on wordPageUrl
def scrapeVideoUrl(wordPageUrl):
    domain = "https://www.signingsavvy.com/"
    assert(wordPageUrl.startswith(domain))

    soup = getWebpageSource(wordPageUrl)

    videoTag = soup.find("video", {"id": "player1Video"})
    videoRelativeUrl = videoTag.find("source")["src"]
    result = domain + videoRelativeUrl

    assert(result.endswith(".mp4"))
    return result

# gets a BeautifulSoup object of the given url's source
def getWebpageSource(url):
    ua = UserAgent()
    headers = { "Connection": "close", "User-Agent": ua.random }
    r = requests.get(url, headers = headers)
    return BeautifulSoup(r.text, "html.parser")

# checks if a given string contains only letters or apostrophes
def isWord(word):
    return not any(c for c in word if c not in ascii_letters + "'")

print(getVideoUrl(sys.argv[1]))
