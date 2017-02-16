#!/usr/bin/env python
# coding=utf-8
from httpmock import requestByGet,requestByPost
from bs4 import BeautifulSoup as soup
from urllib import request as urlre
from bs4.element import NavigableString
import os
import re 
import json


def geneDom(html):
    return soup(html,'html.parser')

def parseAnswer(html,num):
    answer=geneDom(html)

    cwd = os.getcwd()
    result=0
    #获取答主用户名，并按照用户名生成目录
    author=answer.find(class_="author-link")
    if author:
        author=author.text
    else:
        result=1
        author='匿名用户'+str(num)
    
    print('正在解析<%s>的答案' % author)

    path=os.path.join(cwd,'answers',author)
    if not os.path.exists(path):
        os.makedirs(path)

    content = answer.find(class_='zm-editable-content clearfix')

    
    #讲答案文字内容写入text.txt 
    fout = open(os.path.join(path,'text.txt'),'w')
    fout.write(extraAnswer(content))
    fout.close()
     
    #讲答案中嵌入的图片下载到答主目录的pic子目录下,按照1,2,3……编号
    picnum=0
    imgPath=os.path.join(path,'pic')
    if not os.path.exists(imgPath):
        os.mkdir(imgPath)

    for img in content.find_all('img',src=re.compile('^https://')):
        src=img['src']
        picnum+=1
        urlre.urlretrieve(src,os.path.join(imgPath,'%s.%s' % (picnum,src.split('.')[-1])))
    
    #统计赞同数、评论数、图片数，并将结果写入summary.txt
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
    print('图片数:'+str(picnum),file=fout)
    fout.close()

    print('Done!')
    return result,picnum



def extraAnswer(tag):
    text_list=[]
    extraRecurAnswer(tag,text_list)
    return '\n'.join(text_list)

def extraRecurAnswer(tag,list):
    if isinstance(tag,NavigableString):
        if tag.string not in list:
            list.append(tag.string)
    else:
        for child in tag.children:
            extraRecurAnswer(child,list)

        

def parseAllAnswers(que_id):
    url='https://www.zhihu.com/node/QuestionAnswerListV2'
    offset=0
    pagesize=10
    num=0
    count=0
    picCount=0
    while True:
        params=json.dumps({'url_token':que_id,'pagesize':pagesize,'offset':offset,'method':'next'})
        data={
            '_xsrf':'',
            'method':'next',
            'params':params
        }
        answers=requestByPost(url,isJson=True,data=data)['msg']
        if not answers:
            break
        for answer in answers:
            result=parseAnswer(answer,num)
            num+= result[0]
            count+=1
            picCount+=result[1]
        offset+=pagesize
    print('完成,共解析%d个答案,下载%d张图片' % (count,picCount))

