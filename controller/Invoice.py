#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, request
import base64, json
from api import TencentInvoiceOCR, XunfeiInvoiceOCR

from system import func
from system import global_dict


def index():
    project = request.headers.get('Project-Name')
    file = base64.b64decode(request.form.get('file'))
    api_provider = request.form.get('api_provider')
    if not api_provider:
        raise Exception('接口参数错误')
    if not file:
        raise Exception('文件缺失')
    if not project:
        raise Exception('项目名称缺失')
    api_config = func.get_api_config('invoice', project, api_provider)
    if not api_config:
        raise Exception('配置错误')
    global_dict.set_value("api_config", api_config)
    # file = func.read_file(file_name)
    # if not file:
    #     raise Exception('文件读取失败')
    if api_provider == 'tencent':
        result = TencentInvoiceOCR.ocr(file)
    elif api_provider == 'xunfei':
        xunfei = XunfeiInvoiceOCR.InvoiceOCR()
        result = xunfei.ocr(file)
    else:
        raise Exception('接口未知')
    func.save_api_log('invoice', json.dumps(result), project, api_provider)
    return result