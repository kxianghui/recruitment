#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : util.py
@Author: hkhl
@Date  : 2020/6/9 22:23
@Desc  : 公共方法
@Python Version: 3.6.2
"""

import os
import time
import random
import codecs
import csv


def save_file(content, path, check_null=False, mode='w', encoding='utf-8'):
    """
    save content to file
    :param content:
    :param path:
    :param check_null:
    :param mode:
    :param encoding:
    :return:
    """
    if not path:
        raise Exception('path must be not null.')
    if check_null and not content:
        print('null content, not to save it.')
        return
    # if parent dir not exist, then create it
    parent_dir, file_name = os.path.split(path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    # write it
    with open(path, mode, encoding=encoding) as f:
        f.write(content)


def append_file(content, path, check_null=False):
    """
    append content to origin file
    :param content:
    :param path:
    :param check_null:
    :return:
    """
    save_file(content, path, check_null, 'a')


def save_binary_file(content, path, check_null=False, encoding=None):
    """
    save binary data to file
    :param content:
    :param path:
    :param check_null:
    :param encoding:
    :return:
    """
    save_file(content, path, check_null, 'wb', encoding)


def read_file(path):
    """
    read file, get file content
    :param path:
    :return:
    """
    with open(path, encoding='utf-8') as f:
        content = f.read()
    return content


def transfer_encoding_file(before_en, after_en, path):
    """
    transfer file encoding, like 'ANSI' transfer to 'UTF-8'
    :param before_en: before file encoding
    :param after_en: after file encoding
    :param path: file path
    :return:
    """
    if not path:
        raise Exception('path must be not null')
    # before encoding
    before_f = codecs.open(path, 'r', before_en)
    content = before_f.read()
    # after encoding
    file_obj = codecs.open(path, 'w', after_en)
    file_obj.write(content)


def save_csv_file(rows, path, header, mode='w', write_header=True):
    if not path:
        raise Exception('path must be not null.')
    if not rows:
        print('null content, not to save it.')
        return
    # if parent dir not exist, then create it
    parent_dir, filename = os.path.split(path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    # write it
    with open(path, mode, newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def append_csv_file(rows, path, header, write_header=True):
    save_csv_file(rows, path, header, 'a', write_header)


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
