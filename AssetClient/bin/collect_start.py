#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os,sys,platform
print(platform.system())
if platform.system() == "Windows":
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
    print(BASE_DIR)
else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
    print(BASE_DIR)

sys.path.append((BASE_DIR))
from core import argvhandler

if __name__ == '__main__':

    argvhandler.ArgvHandler(sys.argv)