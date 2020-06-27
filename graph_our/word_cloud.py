#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : word_cloud.py
@Author: hkhl
@Date  : 2020/6/27 13:37
@Desc  : 
@Python Version: 3.6.2
"""

import jieba
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import PIL.Image as Image


def get_stopwords(words):
    stopwords = set(STOPWORDS)
    for word in words:
        stopwords.add(word)
    return stopwords


class MyWordCloud(object):

    def __init__(self, text, picture_path, mask_img_path=None, font_path=None,
                 background_color=None, stopwords=None, width=None, height=None):
        self.text = text
        self.picture_path = picture_path
        self.mask_img_path = mask_img_path
        self.font_path = font_path
        self.background_color = background_color
        self.stopwords = stopwords
        self.width = width
        self.height = height
        self.wc = None
        self.__create_word_cloud()

    def __get_mask(self):
        return np.array(Image.open(self.mask_img_path)) if self.mask_img_path else None

    def __create_word_cloud(self):
        mask = self.__get_mask()
        self.wc = WordCloud(mask=mask, font_path=self.font_path, background_color=self.background_color,
                            stopwords=self.stopwords, width=self.width, height=self.height)

    def render(self):
        self.wc.generate(self.text)
        self.wc.to_file(self.picture_path)

    def show(self):
        self.wc.generate(self.text)
        image = self.wc.to_image()
        image.show()

