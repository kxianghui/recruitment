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
import time
import random
import requests
import traceback

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}

# root_url
# root_url = 'https://www.lagou.com/jobs/list_java/p-city_7' # 南昌
root_url = 'https://www.lagou.com/jobs/list_java/p-city_213'  # 广州
# ajax_url
# url = "https://www.lagou.com/jobs/positionAjax.json?city=%E5%8D%97%E6%98%8C&needAddtionalResult=false"  # 南昌
url = "https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false"  # 广州
keyword = 'java'
file_name = 'lagou_gz.csv'
csv_path = file_name
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


def get(dict_args, keys):
    """
    get value by key
    if per key have ['.'], value will be wrong

    For example:
    like this, sys_args = {'a':{'b':'c'}}
    if you want to get 'c', just get('a.b', sys_args), then you can get it.
    :param keys: like 'a.b.c.d...'
    :param dict_args: not only sys_args, it could be other args, if it's type of dict
    :return:
    """
    key_list = keys.split('.')
    value = None
    if len(key_list) > 1:
        for key in key_list:
            assert isinstance(dict_args, dict), 'not found keys like {}'.format(keys)
            if dict_args:
                value = dict_args.get(key)
                dict_args = value
    else:
        value = dict_args.get(key_list[0])
    return value


def pause_random(integer=1, decimal_scale=1, offset=0.5, tip=None):
    """
    range 1.5 - 2.4
    :param integer:
    :param decimal_scale:
    :param offset:
    :param tip:
    :return:
    """
    decimal = round(random.random(), decimal_scale)
    sleep_time = integer + decimal + offset
    time.sleep(sleep_time)
    if tip:
        print("{}, wait {}s".format(tip, sleep_time))
    else:
        print("wait {}s".format(sleep_time))


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
    job_info_list = get(json_body, 'content.positionResult.result')
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
    pause_random()


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
