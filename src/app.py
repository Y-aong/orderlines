# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : app.py
# Time       ：2023/1/14 22:34
# Author     ：Y-aong
# version    ：python 3.7
# Description：flask enter point
"""

from apis import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=15900)
