#!/usr/bin/env python
# coding=utf-8

from bs4 import BeautifulSoup as soup
from urllib import request as urlre
import requests
import os
import re 
def getHtml(url):
    user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
    header={"User-Agent":user_agent}
    return requests.get(url,headers=header).text

def parseDom(html):
    return soup(html,'html.parser')

def extraAnswers(url):
    html=getHtml(url)
    dom=parseDom(html)

    cwd = os.getcwd()
    count=0
    for answer in dom.find_all('div',tabindex="-1"):
        author=answer.find(class_="author-link")
        if author:
            author=author.text
        else:
           count+=1
           author='匿名用户'+str(count)
        path=os.path.join(cwd,author)
        if not os.path.exists(path):
            os.mkdir(path)

        content = answer.find(class_='zm-editable-content clearfix')
        fout = open(os.path.join(path,'text.txt'),'w')
        fout.write(content.text)
        fout.close()


        num=0
        imgPath=os.path.join(path,'pic')
        if not os.path.exists(imgPath):
            os.mkdir(imgPath)
        for img in content.find_all('img',src=re.compile('^https://')):
            src=img['src']
            num+=1
            urlre.urlretrieve(src,os.path.join(imgPath,'%s.%s' % (num,src.split('.')[-1])))
        
        fout=open(os.path.join(path,'summary.txt'),'w')
        agree=answer.find(class_="count").text
        print('赞同数:'+agree,file=fout)

        comment=answer.find(class_=re.compile("^meta-item toggle-comment")).text
        m=re.match('\d+',comment)
        if m:
            comment=m.group()
        else:
            comment=str(0)
        print('评论数:'+comment,file=fout)
        print('图片数:'+str(num),file=fout)
        fout.close()

    print('Done!')

   
extraAnswers('https://www.zhihu.com/question/36196026')
