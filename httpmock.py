#!/usr/bin/env python
# coding=utf-8

import requests
import json

def geneHeader():
    user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
    header={"User-Agent":user_agent}
    return header

def requestByGet(url,isJson=False,params=None):
    header=geneHeader()
    r=requests.get(url,headers=header,params=params)
    if(isJson):
        return r.json()
    else:
        return r.text

def requestByPost(url,isJson=False,data=None):
    header=geneHeader()
    r=requests.post(url,headers=header,data=data)
    if(isJson):
        return r.json()
    else:
        return r.text
