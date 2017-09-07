# coding=utf-8
#dytt.py
import sys
import urllib
import urllib3
import os
import chardet
import requests
from bs4 import BeautifulSoup
import time



#从html页面中获取视频下载地址
def get_download_url(broken_html):
    soup=BeautifulSoup(broken_html,'html.parser')
    fixed_html=soup.prettify()
    td=soup.find('td',attrs={'style':'WORD-WRAP: break-word'})
    url_a=td.find('a')
    url_a=url_a.string
    return url_a

#从html页面中获取电影标题
def get_title(broken_html):
    soup=BeautifulSoup(broken_html,'html.parser')
    fixed_html=soup.prettify()
    title=soup.find('h1')
    title=title.string
    return title

#访问url，返回html页面
def url_open(url):
    req=requests.get(url)
   # req.add_header('User-Agent','Mozilla/5.0')
   # response=urllib3.urlopen(url)
    html=req.text
    return html

#主要逻辑就是爬取列表页面，从列表页面中找到每个下载页的连接，拼接好之后再访问，获得标题和下载地址
def add_index_url(url,num,file_object):
    for i in range(1,num):
        new_url=url+str(i)+".html"
        print("----------------------当前爬取第"+str(i)+"页---------------------")
        html=url_open(new_url)
        time.sleep(1)
        soup=BeautifulSoup(html,'html.parser')
        fixed_html=soup.prettify()
        a_urls=soup.find_all('a',attrs={'class':'ulink'})
        host="http://www.ygdy8.net"
        for a_url in a_urls:
            a_url=a_url.get('href')
            a_url=host+a_url
            print(a_url)
            html=url_open(a_url)
            #html=unicode(html,'GBK').encode("utf-8")
            html=html.encode('utf-8')
            write_title=get_title(html)
            write_url=get_download_url(html)
            file_object.write(write_title+"\n")
            file_object.write(write_url+"\n")

if __name__=='__main__':
    url="http://www.ygdy8.net/html/gndy/dyzz/list_23_"
    filename="down_load_url.txt"
    num=int(input("please input the page num you want to download:"))
    num=num+1
    if os.path.exists(filename):
        file_object=open(filename,'w+',encoding='UTF-8')
    else:
        file_object=open(filename,'w+',encoding='UTF-8')
    add_index_url(url,num,file_object)
    print("----------------------爬取完成--------------------------")
    file_object.close()