#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : boss_spider.py
@Author: hkhl
@Date  : 2020/6/25 17:31
@Desc  : 
@Python Version: 3.6.2
"""

import time
from pyquery import PyQuery as pq
from common import util
from driver import my_driver
from config import config_parse

browser = my_driver.MyDriver()
config_parser = config_parse.MyConfigParser()
# tip
null_tip = '-'
title_dict = {
    "company_name": "公司全称",
    "company_size": "公司规模",
    "industry_field": "公司领域",
    "position_name": "职位名称",
    "job_area": "区域",
    "salary": "工资水平",
    "work_year": "工作年限",
    "education": "学历要求",
    "tags": "标签",
    "position_advantage": "职位优势",
}
section_name = "boss"  # 切换
url = config_parser.get(section_name, "url")
file_path = config_parser.get(section_name, "filePath")


def parse_job_body(doc):
    li_list = doc('#main > .job-box > .job-list > ul > li').items()
    rows = []
    for li in li_list:
        rows.append(parse_li_body(li))
    return rows


def transfer_row_key_name_2_cn(row):
    cn_row = dict()
    for key in row:
        cn_key = title_dict.get(key)
        value = row[key]
        cn_row[cn_key] = value
    return cn_row


def parse_li_body(li):
    row = dict()
    row['company_name'] = li.find('.company-text > h3 > a').text()
    sizes = li.find('.company-text > p').html().split('<em class="vline"/>')
    row['company_size'] = sizes[-1] if sizes else null_tip
    row['industry_field'] = li.find('.company-text > p > a').text()
    row['position_name'] = li.find('span.job-name > a').text()
    row['job_area'] = li.find('span.job-area').text()
    row['salary'] = li.find('.job-limit > span:first-child').text()
    work_year_education = li.find('.job-limit > p').html()
    work_year_educations = work_year_education.split('<em class="vline"/>')
    row['work_year'] = work_year_educations[0] if work_year_educations else null_tip
    row['education'] = work_year_educations[-1] if work_year_educations else null_tip
    tags = li.find('.info-append span').text()
    row['tags'] = tags.replace(' ', ',') if tags else null_tip
    row['position_advantage'] = li.find('.info-desc').text()
    return transfer_row_key_name_2_cn(row)


def check_next_page_ok(doc):
    """
    if next button is enabled, return True, otherwise return False
    :param doc:
    :return:
    """
    next_page = doc('#main .job-list > .page > a:last-child')
    return 'disabled' not in next_page.attr('class')


def parse_page(page_source):
    doc = pq(page_source)
    rows = parse_job_body(doc)
    next_state = check_next_page_ok(doc)
    return rows, next_state


def save_2_csv(rows, writer_header):
    if not rows:
        print('rows is null, return')
    util.append_csv_file(rows, file_path, title_dict.values(), write_header=writer_header)


def click_next_page():
    # click next page
    next_a = browser.find_by_css("#main > div > div.job-list > div.page > a.next")
    browser.driver.execute_script('arguments[0].scrollIntoView();', next_a)
    next_a.click()


def main():
    browser.get(url)
    browser.driver.maximize_window()
    browser.wait_located_by_css('#main > div > div.job-list > ul')
    browser.wait_located_by_css('#main > div > div.job-list > div.page')
    page_no = 1
    while True:
        print("request page no {}".format(page_no))
        rows, next_state = parse_page(browser.page_source)
        write_header = True if page_no == 1 else False
        save_2_csv(rows, write_header)
        if not next_state:
            break
        click_next_page()
        time.sleep(2)
        page_no += 1


main()
