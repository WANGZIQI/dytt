#!/usr/bin/python
# coding: UTF-8
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup as bsp
import urllib3
import re
import urllib.request

site = 'http://www.dytt8.net'
lineNo = 1


class Movie:
    def __init__(self, name, url, score, link):
        self.name = name
        self.url = url
        self.score = score
        self.link = link

    def __str__(self):
        return '%s,\t%s分,\t%s' % (self.name, self.score, self.link)

    __repr__ = __str__


def getSoup(url):
    r = requests.get(url)
    r.encoding = 'gb18030'
    return bsp(r.text, "html.parser")


def filterMovie(url):
    resultList = []
    soup = getSoup(url)
    tables = soup.find_all('table', class_='tbspan')
    for table in tables:
        nameA = table.find('a', text=re.compile("《"))
        td = table.find('td', text=re.compile("IMD"))
        if td is not None:
            scoreStr = re.findall(r"评分 (.+?)/10", td.text)
            if (len(scoreStr) > 0):
                try:
                    ##正则niubi的同学可以用正则表达式搞定
                    scoreStr[0]=scoreStr[0].replace(',','.')
                    scoreStr[0] = scoreStr[0].replace('Ratings:', '')
                    score = float(scoreStr[0])
                    if (score > 9):
                        name = nameA.text
                        url = site + nameA['href']
                        print('url:', url)
                        print('title:', name)
                        print('score:', score)
                        downloadLink = getDownloadLink(url)
                        movie = Movie(name, url, score, downloadLink)
                        resultList.append(movie)
                except:
                    print(scoreStr)
                    print('error !!')
    return resultList


def getDownloadLink(url):
    soup = getSoup(url)
    downloadTd = soup.find('td', attrs={"style": "WORD-WRAP: break-word"})
    downloadA = downloadTd.find('a')
    return downloadA['href']


def saveInfo(movieList):
    fileObj = open('data.txt', 'a',encoding='utf-8')
    for movie in movieList:
        movie_str = str(movie)
       ## downloadMovice(movie.link,movie.name)
        print('movie info:', movie_str)
        global lineNo
        fileObj.write('(' + str(lineNo) + ') ' + movie_str)
        fileObj.write('\n')
        fileObj.write(
            '————————————————————————————————————————————————————————————————————————————————————————————————')
        fileObj.write('\n')
        lineNo += 1
    fileObj.close()


def getPageResource(url):
    resultList = filterMovie(url)
    if len(resultList) > 0:
        saveInfo(resultList)
## 只能下http打头的 在线视频
def downloadMovice(url,fileName):
    urllib.request.urlretrieve(url,fileName);

if __name__ == '__main__':
    for index in range(165):
        index += 1
        url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_' + \
              str(index) + '.html'
        getPageResource(url)
