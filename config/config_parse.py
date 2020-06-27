#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : config_parse.py
@Author: hkhl
@Date  : 2020/6/27 14:49
@Desc  : 
@Python Version: 3.6.2
"""

from configparser import ConfigParser


class MyConfigParser(object):

    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read("config.ini")

    def get(self, section, key):
        return self.parser.get(section, key)

o = MyConfigParser()
a = o.get("word_cloud", 'picturePath')
print(a)