#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : lagou_spider.py
@Author: hkhl
@Date  : 2020/5/31 11:23
@Desc  : 
@Python Version: 3.6.2
"""

import re
import json
import csv
import requests
import traceback
from common import util
from config import config_parse

config_parser = config_parse.MyConfigParser()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
section_name = "lagou_nc"  # 切换
keyword = config_parser.get("lagou", "keyword")
# root_url
root_url = config_parser.get(section_name, "url")
# ajax_url
url = config_parser.get(section_name, "ajaxUrl")
csv_path = config_parser.get(section_name, "filePath")

title_dict = {
        "companyFullName": "公司全称",
        "companySize": "公司规模",
        "industryField": "公司领域",
        "positionName": "职位名称",
        "createTime": "职位创建时间",
        "district": "区域",
        "salary": "工资水平",
        "workYear": "工作年限",
        "education": "学历要求",
        "positionAdvantage": "职位优势",
    }


def create_row(job_info_dict):
    row = dict()
    for key in title_dict:
        value = job_info_dict.get(key)
        name = title_dict.get(key)
        row[name] = value
    return row


def save_to_csv(rows, write_header=True):
    if not rows:
        print('rows is null...')
        return
    with open(csv_path, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=title_dict.values())
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def parse_page_job_json(text):
    json_body = json.loads(text)
    job_info_list = util.get(json_body, 'content.positionResult.result')
    rows = []
    for job_info in job_info_list:
        rows.append(create_row(job_info))
    return rows


def build_request_data(page_no, keyword):
    first = 'true' if page_no == 1 else 'false'
    request_data = dict()
    request_data['first'] = first
    request_data['pn'] = page_no
    request_data['kd'] = keyword
    return request_data


def execute_on_page(session, page_no):
    print('request page {}'.format(page_no))
    data = build_request_data(page_no, keyword)
    res = session.post(url, data=data, headers=headers)
    rows = parse_page_job_json(res.text)
    write_header = True if page_no == 1 else False
    save_to_csv(rows, write_header=write_header)
    util.pause_random()


def normal_gather():
    session = requests.session()
    res = session.get(root_url, headers=headers)
    page_total = int(re.search('<span class="span totalNum">(\\d+)</span>', res.text).group(1))
    headers['referer'] = root_url
    for page_no in range(1, page_total + 1):
        try:
            execute_on_page(session, page_no)
            # 已知问题，路人访问好像10页就开始采集不到了，重新拿下连接
            if page_no % 9 == 0:
                session.close()
                session = requests.session()
                session.get(root_url, headers=headers)
        except Exception:
            print(traceback.format_exc())


normal_gather()
