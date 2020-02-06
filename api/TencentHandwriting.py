#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    腾讯手写体识别
"""

__author__ = 'Van23qf'


import base64
import json

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models


def ocr(pic):
    try:
        with open(pic, 'rb') as f:
            f1 = f.read()
        pic_base64 = str(base64.b64encode(f1), 'utf-8')
        cred = credential.Credential("AKID96rMeho9uQiqjRvCI8C3f6esstjMjFZi", "3toZ7RmtlSv9EA0f8LNJ6i6MOYXHoQr5")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile('TC3-HMAC-SHA256')
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)

        req = models.GeneralHandwritingOCRRequest()
        params = '{"ImageBase64":"' + pic_base64 + '"}'
        req.from_json_string(params)

        resp = client.GeneralHandwritingOCR(req)
        resp = json.loads(resp.to_json_string())
        if not resp.get('TextDetections'):
            return {'status': False, 'msg': '识别失败'}
        data = []
        for v in resp['TextDetections']:
            data.append(v['DetectedText'])
        return {'status': True, 'msg': 'success', 'data': data}
    except FileNotFoundError as err_file:
        return {'status': False, 'msg': err_file.strerror}
    except TencentCloudSDKException as err:
        return {'status': False, 'msg': err.get_message()}


if __name__ == '__main__':
    result = ocr('../uploads/jibing.png')
    print(result)
