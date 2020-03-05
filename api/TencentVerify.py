#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    腾讯通用印刷体识别接口(高精度版)
    documents   https://cloud.tencent.com/document/product/866/34937
"""

__author__ = 'Van23qf'


import base64
import json

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.faceid.v20180301 import faceid_client, models

from config import config
from system import global_dict


def check(idcard_name, idcard_number):
    try:
        #api_config = global_dict.get_value("api_config")
        cred = credential.Credential("AKID96rMeho9uQiqjRvCI8C3f6esstjMjFZi", "3toZ7RmtlSv9EA0f8LNJ6i6MOYXHoQr5")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "faceid.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = faceid_client.FaceidClient(cred, "ap-guangzhou", clientProfile)

        req = models.IdCardOCRVerificationRequest()
        params = {
            "IdCard": idcard_number,
            "Name": idcard_name,
        }
        params_json = json.dumps(params)
        req.from_json_string(params_json)

        resp = client.IdCardOCRVerification(req)
        resp = resp.to_json_string()
        return resp
    except FileNotFoundError as err_file:
        return {'status': False, 'msg': err_file.strerror}
    except TencentCloudSDKException as err:
        return {'status': False, 'msg': err.get_message()}


if __name__ == '__main__':
    print(check('秦凡', '421122199206231036'))

"""

"""