#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    腾讯身份证OCR接口
    documents   https://cloud.tencent.com/document/product/866/33524#API-Explorer
    APPID:1252569649
    SecretId:AKID96rMeho9uQiqjRvCI8C3f6esstjMjFZi
    SecretKey:3toZ7RmtlSv9EA0f8LNJ6i6MOYXHoQr5


    目前支持的扩展字段为：
    IdCard，身份证照片，请求 CropIdCard 时返回；
    Portrait，人像照片，请求 CropPortrait 时返回；
    WarnInfos，告警信息（Code - 告警码），识别出以下告警内容时返回。

    Code 告警码列表和释义：
    -9100 身份证有效日期不合法告警，
    -9101 身份证边框不完整告警，
    -9102 身份证复印件告警，
    -9103 身份证翻拍告警，
    -9105 身份证框内遮挡告警，
    -9104 临时身份证告警，
    -9106 身份证PS告警。
"""

__author__ = 'Van23qf'


from datetime import datetime
import base64
import json

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

from api import Config

WarnInfosDict = {
    -9100: '身份证有效日期不合法告警',
    -9101: '身份证边框不完整告警',
    -9102: '身份证复印件告警',
    -9103: '身份证翻拍告警',
    -9104: '临时身份证告警',
    -9105: '身份证框内遮挡告警',
    -9106: '身份证 PS 告警',
}


def get_warns(resp):
    err_msg = []
    if resp.get('AdvancedInfo'):
        AdvancedInfo = json.loads(resp['AdvancedInfo'])
        for v in AdvancedInfo.get('WarnInfos', []):
            if WarnInfosDict.get(v):
                err_msg.append(WarnInfosDict[v])
    if resp.get('ValidDate'):
        validity = resp['ValidDate'].split("-")
        validity_start = datetime.strptime(validity[0] + " 00:00:00", "%Y.%m.%d %H:%M:%S").timestamp()
        validity_end = datetime.strptime(validity[1] + " 23:59:59", "%Y.%m.%d %H:%M:%S").timestamp()
        now_time = datetime.now().timestamp()
        if now_time > validity_end:
            err_msg.append("身份证过期告警")
        if now_time < validity_start:
            err_msg.append("身份证还未生效告警")
    return err_msg


def ocr(file, side='front'):
    idcardfile_base64 = str(base64.b64encode(file), 'utf-8')
    try:
        cred = credential.Credential(Config.tencent['idcard']['secretid'], Config.tencent['idcard']['secretkey'])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile('TC3-HMAC-SHA256')
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)

        req = models.IDCardOCRRequest()
        params = {
            'ImageBase64': idcardfile_base64,
            'CardSide': 'FRONT' if side == 'front' else 'BACK',
            'Config': '{"CopyWarn":true,"BorderCheckWarn":true,"ReshootWarn":true,"DetectPsWarn":true,"TempIdWarn":true,"InvalidDateWarn":true}'
        }
        params_json = json.dumps(params)
        req.from_json_string(params_json)

        resp = client.IDCardOCR(req)
        resp = json.loads(resp.to_json_string())
        warns = ";".join(get_warns(resp))
        if not resp.get('Name') and not resp.get('Authority'):
            err_msg = "身份证识别错误;" + warns
            return {'status': False, 'msg': err_msg}
        msg = '读取成功;' + warns
        if side == 'front':
            return {
                'status': True,
                'msg': msg,
                'data': {
                    'name': resp['Name'],
                    'gender': resp['Sex'],
                    'nation': resp['Nation'],
                    'birth': resp['Birth'],
                    'address': resp['Address'],
                    'idnum': resp['IdNum'],
                }
            }
        else:
            return {
                'status': True,
                'msg': msg,
                'data': {
                    'authority': resp['Authority'],
                    'validity': resp['ValidDate'],
                }
            }
    except TencentCloudSDKException as err:
        return {'status': False, 'msg': err.get_message()}


if __name__ == '__main__':
    result = ocr('../uploads/idcard_front.jpg', 'front')
    print(result)

"""
{"Name": "陈莲", "Sex": "女", "Nation": "汉", "Birth": "1964/5/5", "Address": "南宁市青秀区古城路9号1栋1单元1094号房", "IdNum": "450103196405052163", "Authority": "", "ValidDate": "", "AdvancedInfo": "{\"WarnInfos\":[-9102,-9101,-9106]}", "RequestId": "2f4d807b-7ba0-4c4d-8993-1cbac19da1f9"}
{"Name": "", "Sex": "", "Nation": "", "Birth": "", "Address": "", "IdNum": "", "Authority": "", "ValidDate": "", "AdvancedInfo": "{\"WarnInfos\":[-9101,-9105,-9106]}", "RequestId": "0d995bd1-c428-4f0c-b48d-bf3487e01802"}

"""