#!/usr/bin/env python
# coding=utf-8

from httpmock import requestByGet,requestByPost
from bs4 import BeautifulSoup as soup
from bs4.element import NavigableString
import os
import re 

def geneDomFromUrl(url):
    html=requestByGet(url)
    return geneDom(html)

def geneDom(html):
    return soup(html,'html.parser')

def allRoles():
    prefix='http://zh.asoiaf.wikia.com'
    url=prefix+'/wiki/Category:%E4%BA%BA%E7%89%A9'
    fout=open('allroles.txt','wt')
    count=0
    while(url):
        print('Handling',url)
        dom=geneDomFromUrl(url)
        div=dom.find('div',id='mw-pages')
        for li in div.find_all('li'):
            if li.a:
                role= roleInfo(prefix+li.a['href'])
                print(role)
                if role:
                    print(role[0],role[1],file=fout)
                else:
                    continue

        next=list(div.find_all('a',title=re.compile('^Category')))
        next=list(filter(lambda  a:a.text=='后200个',next))
        if next:
            url=prefix+next[0]['href']
        else:
            url=None
    fout.close()
    print('Done,',str(count),'roles in total.')


def roleInfo(url):
    dom=geneDomFromUrl(url)
    div=dom.find_all('div',id='mw-content-text')
    b=dom.find_all('b')
    pattern=re.compile('.*（')
    b=list(filter(lambda b:b.next_sibling and b.next_sibling.string and  pattern.match( b.next_sibling.string),list(b)))
    if b:
        b=b[0]
    else:
        return None
    name_zh=b.text
    name_en=b.next_sibling.next_sibling.text
    return name_zh,name_en

allRoles()
