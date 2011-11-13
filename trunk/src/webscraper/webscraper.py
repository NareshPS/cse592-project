#! /usr/bin/python
from BeautifulSoup import BeautifulSoup

import sys

class webscraper:
    def extractcomics(self):
        soup    = BeautifulSoup(sys.stdin.read())
        results = soup.findAll('tr')

        for result in results:
            if str(result) == '<tr><td>&nbsp;</td></tr>':
                continue
            atag    = result.first('a', attrs={'class' : 'searchlink'})
            if atag is None:
                continue
            print atag['title']
            print result.first('td', attrs={'align' : 'left'}).contents[0]
            print atag['href']


if __name__ == '__main__':
    ws  = webscraper()
    ws.extractcomics()
