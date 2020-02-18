#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import base64, json, os, hashlib
from datetime import datetime
from system.model import ApiLog, Project
from system import db, Redis

from flask import Flask, request


def md5(str):
    """
    字符串md5加密
    :param str:
    :return:
    """
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


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


def save_api_log(api_name, result, project, api_provider, nonce_str=''):
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
    apilog.nonce_str = nonce_str
    apilog.created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return apilog.insert()


def get_api_config(api_name, project, api_provider):
    """
    获取api配置
    :param api_name:
    :param project:
    :param api_provider:
    :return:
    """
    sql = "select * from api_config where api_name='{api_name}' and project='{project}' and api_provider='{api_provider}'"
    api_config = db.get_one(sql.format(api_name=api_name, project=project, api_provider=api_provider))
    return api_config
    # r = Redis.Redis()
    # api_config_key = project + ':api_config:' + api_name + ':' + api_name
    # api_config_json = r.get(api_config_key)
    # if not api_config_json:
    #     sql = "select * from api_config where api_name='{api_name}' and project='{project}' and api_provider='{api_provider}'"
    #     api_config = db.get_one(sql.format(api_name=api_name, project=project, api_provider=api_provider))
    #     r.set(api_config_key, json.dumps(api_config))
    # else:
    #     api_config = json.loads(api_config_json)
    # return api_config


def save_file_log(file_name, content, mode='a'):
    """
    记录文本
    :param file_name:
    :param content:
    :param mode:
    """
    file_path = os.path.dirname(file_name)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_name, mode) as f:
        f.write(content)


def check_api_access(api_name):
    """
    检测api权限
    :param project_name:
    :param api_name:
    """
    project_name = request.headers.get('project_name')
    ts = request.headers.get('ts')
    out_signature = request.headers.get('signature')
    if not project_name or not ts or not out_signature:
        raise Exception("签名参数不全")
    project = Project.Model()
    if not project.check_project_verify(project_name, ts, out_signature):
        raise Exception("签名错误")
    if not project.check_api_access(project_name, api_name):
        raise Exception("项目没有API权限")