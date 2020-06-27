#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : my_driver.py
@Author: hkhl
@Date  : 2020/6/9 22:32
@Desc  : 
@Python Version: 3.6.2
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class MyDriver(object):

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        # 无窗口模式，参数
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # default 10s
        self.default_wait = WebDriverWait(self.driver, 10)

    def get(self, url):
        self.driver.get(url)

    def page_source(self):
        return self.driver.page_source

    def wait_by_css(self, expected_condition, wait=None):
        wait.until(expected_condition) if wait else self.default_wait.until(expected_condition)

    def wait_located_by_css(self, css_select, wait=None):
        self.wait_by_css(EC.presence_of_element_located((By.CSS_SELECTOR, css_select)), wait)

    def wait_click_able_by_css(self, css_select, wait=None):
        self.wait_by_css(EC.element_to_be_clickable((By.CSS_SELECTOR, css_select)), wait)

    def find_by_css(self, css_select):
        return self.driver.find_element_by_css_selector(css_select)

    def finds_by_css(self, css_select):
        return self.driver.find_elements_by_css_selector(css_select)

    def element_exist_by_css(self, css_select):
        try:
            self.find_by_css(css_select)
            return True
        except NoSuchElementException:
            return False

    def get_cookie(self, name):
        return self.driver.get_cookie(name)

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()
