#!/usr/bin/env python
# coding=utf-8
import os
import jieba

cwd=os.getcwd()
path=os.path.join(cwd,'answers')
for sub in os.listdir(path):
    text=open(os.path.join(path,sub,'text.txt')).read()
    print(','.join(jieba.cut(text)))
