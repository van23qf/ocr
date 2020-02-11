#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import base64
from datetime import datetime
from system.model import ApiLog
from system import db


def read_file(file_path):
    """
    读取文件
    :param file_path:
    :return:
    """
    try:
        with open(file_path, 'rb') as f:
            f1 = f.read()
        return f1
    except Exception as e:
        return False


def save_api_log(api_name, result, project, api_provider):
    """
    记录api调用日志
    :param api_name:
    :param result:
    :param project:
    :param api_provider:
    """
    apilog = ApiLog.Model()
    apilog.project = project
    apilog.api_provider = api_provider
    apilog.api_name = api_name
    apilog.result = result
    apilog.created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    apilog.insert()


def get_api_config(api_name, project, api_provider):
    """
    获取api配置
    :param api_name:
    :param project:
    :param api_provider:
    :return:
    """
    sql = "select * from api_config where api_name='{api_name}' and project='{project}' and api_provider='{api_provider}'"
    return db.get_one(sql.format(api_name=api_name, project=project, api_provider=api_provider))
