#! /usr/bin/python
from BeautifulSoup import BeautifulSoup

import sys

class webscraper:
    def extractcomics(self):
        soup    = BeautifulSoup(sys.stdin.read()
        results = soup.findAll('tr')

        for result in results:
            atag    = result.first('a', attrs={'class' : 'searchlink'})
            print atag['href']
            print atag['title']

            print result.first('td', attrs={'align' : 'left'}).contents[0]


if __name__ == '__main__':
    ws  = webscraper()
    ws.extractcomics()
