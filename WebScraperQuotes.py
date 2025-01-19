import requests
from random import randint
from bs4 import BeautifulSoup

URL = 'https://www.goodreads.com/quotes/tag/physics'
NuURL = URL + '?page='

def getQuotes(URL):
    out = []
    page = requests.get(URL)
    # page range 2-72
    soup = BeautifulSoup(page.content, 'html.parser')

    res = soup.find_all(class_='quoteText')
    for a in res:
        if isNormal(a.text):
            out.append(a.text)
    return out



def getRandQuote():
    temp = randint(1,25)
    if temp == 1:
        url = URL
    else:
        url = NuURL + str(temp)
    quotes = getQuotes(url)
    quote = quotes[randint(0,len(quotes))]
    return quote

def isNormal(s):
    forbiddenAsciiNums = [35,36,37,28,29,43,60,61,62,64,91,93,94,123,124,125,126]
    for a in s:
        temp = ord(a)
        try:
            forbiddenAsciiNums.index(temp)
            return False
        except Exception:
            continue
    return True
def allQuotes():

    n = 1
    quotesList = []
    while n < 25:
        if n == 1:
            quotesList.append(getQuotes(URL))
        else:
            quotesList.append(getQuotes(NuURL+str(n)))
        n+=1
    return quotesList
