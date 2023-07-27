# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : generate_html_report_utils.py
# Time       ：2023/7/27 15:37
# Author     ：YangYong
# version    ：python 3.10
# Description：
    生成html报告
    generate html report
"""

import pandas as pd
from jinja2 import Environment, FileSystemLoader

df = pd.read_excel('demo.xlsx')
df['消耗本金'] = df['消耗本金'].astype(str) + ' 元'
df['最大回报率'] = df['最大回报率'].astype(str) + '%'
df['总收益率'] = df['总收益率'].astype(str) + '%'
data = df.to_dict('records')

results = {}
results.update({'strategy_name': '第一个策略',
                'start_time': '2020-01-01',
                'end_time': '2021-06-01',
                'money': 20000,
                'items': data})

env = Environment(loader=FileSystemLoader('./'))

template = env.get_template('template.html')

with open("out.html", 'w+', encoding='utf-8') as f:
    out = template.render(strategy_name=results['strategy_name'],
                          start_time=results['start_time'],
                          end_time=results['end_time'],
                          money=results['money'],
                          items=results['items'])
    f.write(out)
    f.close()
