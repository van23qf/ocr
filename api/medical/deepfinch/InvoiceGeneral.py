#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from api.medical.deepfinch import common
import env
import json


URL = 'https://cloudapi.deepfinch.com/ocr/medical_invoice'


def ocr(file):
    files = {'file': file}
    result_json = json.loads(common.post(URL, files=files, data={'auto_rotate': True}))
    if result_json['status'] != 'OK':
        raise Exception(result_json['status'] + ": " + result_json['reason'])
    return {
        'status': True,
        'data': common.format_result(result_json['medical_result'], 'general')
    }


if __name__ == '__main__':
    file = open(env.root_path + '/uploads/shanxi.jpg', 'rb')
    print(ocr(file))

"""

"""
