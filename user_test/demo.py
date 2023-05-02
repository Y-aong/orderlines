# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : demo.py
# Time       ：2023/4/8 10:19
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
import json

from bs4 import BeautifulSoup

with open(r'E:\mongo_db\demo.html', mode='r', encoding='utf-8') as f:
    content = f.read()

b = BeautifulSoup(content, "html.parser")
data = list()
for i in b.text.split('\n'):

    if "MySQL" in i:
        data.append(i.strip().replace('2023Java面试题300集：', ''))
print(json.dumps(data))

