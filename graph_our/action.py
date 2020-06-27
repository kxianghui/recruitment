#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : action.py
@Author: hkhl
@Date  : 2020/6/27 16:11
@Desc  : 
@Python Version: 3.6.2
"""

import csv
import jieba
import configparser
from graph_our import word_cloud

cp = configparser.ConfigParser()
cp.read("../config/config.ini")
file_path = cp.get("boss", "filePath")
font_path = cp.get("word_cloud", "fontPath")
picture_path = cp.get("word_cloud", "picturePath")


def create_word_cloud_pic():
    # 1-3 3-5
    final_tag_list = []
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            work_year = row[6]
            tags = row[8]
            if "1-3" in work_year or "3-5" in work_year:
                tag_list = jieba.cut(tags)
                final_tag_list.extend(tag_list)
    words = ['java', '后端开发']
    stopwords = word_cloud.get_stopwords(words)
    wc = word_cloud.MyWordCloud(" ".join(final_tag_list), picture_path, font_path=font_path, width=1500, height=1000,
                                background_color="white", stopwords=stopwords)
    wc.show()

create_word_cloud_pic()