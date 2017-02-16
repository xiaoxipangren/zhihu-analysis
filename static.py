#!/usr/bin/env python
# coding=utf-8
from collections import Counter
import os
import jieba

class Role():
    def __init__(self,name_zh,name_en):
        self.name_zh=name_zh
        self.name_en=name_en
        self.nicks=[name_zh.replace('·',''),name_zh.replace('·',' ')]
    def singleName(self,name_zhs,name_ens):
        name=self.name_zh.split('·')[0]
        if name_zhs[name]==1:
            self.nicks.append(name)
        name=self.name_en.split(' ')[0]
        if name_ens[name]==1:
            self.nicks.append(name)
    def isSame(self,name):
        en=self.name_en.lower()
        name=name.lower()
        result= (name == self.name_zh) or (name == en)
        if result:
            return result
        else:
            for nick in self.nicks:
                result = (result) or (name==nick)
            return result

    def __str__(self):
        return '%s %s %s'  % (self.name_zh,self.name_en,','.join(self.nicks))



def geneNickDict():
    dict={}
    fin=open('nickname.txt','rt')
    for line in fin:
        if line:
            index=line.index(' ')
            name=line[0:index]
            nicks=line[index+1:-1].split(',')
            dict[name]=nicks
    return dict

def geneAllRoles():
    roles=[]
    fin=open('allroles.txt','rt')
    for line in fin:
        index=line.index(' ')
        name_zh=line[0:index]
        name_en=line[index+1:-1]
        roles.append(Role(name_zh,name_en))

    nicks=geneNickDict()
    for role in roles:
        for name in nicks.keys():
            if role.name_zh==name:
                role.nicks+=nicks[name]
        
    zhs=[role.name_zh.split('·')[0] for role in roles]
    zhs=Counter(zhs)
    ens=[role.name_en.split(' ')[0] for role in roles]
    ens=Counter(ens)
    for role in roles:
        role.singleName(zhs,ens)
        return roles


def static():
    cwd=os.getcwd()
    path=os.path.join(cwd,'answers')
    allroles=geneAllRoles()
    for sub in os.listdir(path):
        print(sub,end=':')
        text=open(os.path.join(path,sub,'text.txt')).read()
        words=jieba.cut(text)
        roles=[]
        for word in words:
            for role in allroles:
                if(role.isSame(word)):
                    roles.append(role)
                    break

        for role in roles:
            print(role,end=';')
        print('')
static()
