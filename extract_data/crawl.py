import urllib.request
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from urllib.request import Request, urlopen

from random import randint
from time import sleep

from socket import error as SocketError
import errno


def handle_starttag(soup, uur):
    a_tags = soup.findAll('a')
    for tag in a_tags:
        if 'walmart' in tag['href']:
            url1 = tag['href']
            url2 = parse.urljoin(uur, url1)
            url2 = Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
            return url2


def print_id(soup2, idd, lis, ki, num):
    for div in soup2.findAll('div', {'class': 'content'}):
        for ultag in div.find_all('ul', {'class': 'quot'}):
            num.append(0)
            ki[0] = ki[0] + 1
            for litag in ultag.find_all('li'):
                lis.append(litag.text)
                num[ki[0]] = num[ki[0]] + 1
                # print("gotcha",ki[0],num[ki[0]])
                # print(litag.text)

        for tag1 in div.find_all('a'):
            if 'Publication' in tag1['href']:
                url = tag1['href']
                # print(tag1['href'],"hello")
                idd.append(urlparse(tag1['href']).path.lstrip(
                    '/').split("/")[1])

url = Request('http://www.metrolyrics.com/taylor-swift-alpage-4.html',
              headers={'User-Agent': 'Mozilla/5.0'})
sleep(randint(2, 4))
page = urllib.request.urlopen(url).read()
soup = BeautifulSoup(page)

for div in soup.findAll('a', {'class': 'title '}):
    url = (div['href'])

    file_name = url.split('/')[3][:-5]
    url1 = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    sleep(randint(2, 4))
    page1 = urllib.request.urlopen(url1).read()
    soup1 = BeautifulSoup(page1)
    with open("Taylor_Swift/" + file_name + ".txt", "w") as f:
        for div in soup1.findAll('div', {'class': 'lyrics-body'}):
            for p in div.find_all('p'):
                f.write(p.text)
