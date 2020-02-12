#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    腾讯发票识别OCR接口
    documents   https://cloud.tencent.com/document/product/866/36210
"""

__author__ = 'Van23qf'


import base64
import json


from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

import global_dict

def ocr(file):
    try:
        api_config = global_dict.get_value("api_config")
        invoicefile_base64 = str(base64.b64encode(file), 'utf-8')
        cred = credential.Credential(api_config['appid'], api_config['appsecret'])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile('TC3-HMAC-SHA256')
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)

        req = models.VatInvoiceOCRRequest()
        params = {
            'ImageBase64': invoicefile_base64,
        }
        params_json = json.dumps(params)
        req.from_json_string(params_json)

        resp = client.VatInvoiceOCR(req)
        resp = json.loads(resp.to_json_string())
        if not resp.get('VatInvoiceInfos'):
            return {'status': False, 'msg': '发票识别失败'}
        data = {}
        for v in resp['VatInvoiceInfos']:
            if v['Name'] == '货物或应税劳务、服务名称':
                data['goods_name'] = v['Value']
            if v['Name'] == '购买方名称':
                data['payer_name'] = v['Value']
            if v['Name'] == '数量':
                data['goods_num'] = v['Value']
            if v['Name'] == '单位':
                data['goods_unit'] = v['Value']
            if v['Name'] == '开票日期':
                data['issue_date'] = v['Value']
            if v['Name'] == '发票号码':
                data['invoice_number'] = v['Value']
            if v['Name'] == '金额':
                data['invoice_amount'] = v['Value']
            if v['Name'] == '单价':
                data['invoice_unit_price'] = v['Value']
        return {'status': True, 'data': data}
    except TencentCloudSDKException as err:
        return {'status': False, 'msg': str(err)}


if __name__ == '__main__':
    result = ocr('./uploads/invoice.jpg')
    print(result)

"""
{"VatInvoiceInfos": [{"Name": "货物或应税劳务、服务名称", "Value": "通信服务费"}, {"Name": "数量", "Value": "1"}, {"Name": "单价", "Value": "6.10"}, {"Name": "金额", "Value": "6.10"}, {"Name": "税率", "Value": "*"}, {"Name": "税额", "Value": "*"}, {"Name": "密码区1", "Value": "5-01692*30394-*7+*6*-41/881"}, {"Name": "密码区2", "Value": "3<+74+68>-39<<>+>83363<2<+1"}, {"Name": "密码区3", "Value": "*06183084*-8/>344-80/*74354"}, {"Name": "密码区4", "Value": "/80/1*574+68>-39<<>+>835>2+"}, {"Name": "发票名称", "Value": "宁波增值税电子普通发票"}, {"Name": "购买方名称", "Value": "王彩萍"}, {"Name": "销售方名称", "Value": "中国移动通信集团浙江有限公司宁波分公司"}, {"Name": "销售方识别号", "Value": "91330000717612522B"}, {"Name": "销售方地址、电话", "Value": "浙江省宁波市国家高新技术开发区光华路2号057455123456-8815"}, {"Name": "销售方开户行及账号", "Value": "中国建设银行宁波市分行营业部-33101983679050502016"}, {"Name": "发票代码", "Value": "033021600111"}, {"Name": "校验码", "Value": "72934467024267954935"}, {"Name": "发票号码", "Value": "No00163217"}, {"Name": "开票日期", "Value": "2016年06月08日"}, {"Name": "合计金额", "Value": "¥6.10"}, {"Name": "合计税额", "Value": "¥*"}, {"Name": "复核", "Value": "叶敏颖"}, {"Name": "开票人", "Value": "叶敏颖"}, {"Name": "小写金额", "Value": "¥6.10"}, {"Name": "备注", "Value": "计费月份:201507"}, {"Name": "收款人", "Value": "叶敏颖"}, {"Name": "省", "Value": "浙江省"}, {"Name": "市", "Value": "宁波市"}, {"Name": "机器编号", "Value": "661565722666"}, {"Name": "发票消费类型", "Value": "服务"}, {"Name": "车船税", "Value": ""}, {"Name": "价税合计(大写)", "Value": ""}, {"Name": "单位", "Value": ""}, {"Name": "规格型号", "Value": ""}, {"Name": "购买方开户行及账号", "Value": ""}, {"Name": "购买方地址、电话", "Value": ""}, {"Name": "购买方识别号", "Value": ""}, {"Name": "通行费标志", "Value": ""}, {"Name": "是否代开", "Value": ""}, {"Name": "是否收购", "Value": ""}, {"Name": "成品油标志", "Value": ""}, {"Name": "校验码备选", "Value": ""}, {"Name": "校验码后六位备选", "Value": ""}, {"Name": "发票号码备选", "Value": ""}, {"Name": "服务类型", "Value": ""}, {"Name": "联次", "Value": ""}, {"Name": "联次名称", "Value": ""}, {"Name": "是否有公司印章", "Value": "1"}], "RequestId": "a23a1d17-d774-4fca-8e69-47879203c6a9"}

{'VatInvoiceInfos': [{'Name': '货物或应税劳务、服务名称', 'Value': '24:'}, {'Name': '规格型号', 'Value': '3号A'}, {'Name': '单位', 'Value': '只'}, {'Name': '单价', 'Value': '6.37808376'}, {'Name': '金额', 'Value': '13675.21'}, {'Name': '税额', 'Value': '2324.75'}, {'Name': '联次', 'Value': '二'}, {'Name': '密码区1', 'Value': '/*/63717<*/13722/+607'}, {'Name': '密码区2', 'Value': '7*02**1/0*2*43+1/5569'}, {'Name': '密码区3', 'Value': '-80<>37>>2**8>/<683+>'}, {'Name': '密码区4', 'Value': '5*//13>+27>//<6/*>>75'}, {'Name': '发票名称', 'Value': '山东增值税普通发票'}, {'Name': '购买方名称', 'Value': '华电虎林民力发电有限公司'}, {'Name': '销售方名称', 'Value': '山东阳谷玻瑞工艺制品厂'}, {'Name': '销售方识别号', 'Value': '372522168018036'}, {'Name': '销售方地址、电话', 'Value': '阳谷城岗高商王688396'}, {'Name': '销售方开户行及账号', 'Value': '中国银行阳谷县支365860609100'}, {'Name': '发票代码', 'Value': '3700081650'}, {'Name': '发票号码', 'Value': 'No01599485'}, {'Name': '开票日期', 'Value': '2009年04月24日'}, {'Name': '税率', 'Value': '17%'}, {'Name': '合计金额', 'Value': '¥13675.21'}, {'Name': '合计税额', 'Value': '¥2324.79'}, {'Name': '价税合计(大写)', 'Value': '壹万陆仟圆整'}, {'Name': '复核', 'Value': '开票人'}, {'Name': '开票人', 'Value': '31216'}, {'Name': '小写金额', 'Value': '¥16000.00'}, {'Name': '备注', 'Value': '31216'}, {'Name': '收款人', 'Value': '香广启'}, {'Name': '省', 'Value': '山东省'}, {'Name': '发票消费类型', 'Value': '服务'}, {'Name': '联次名称', 'Value': '发票联'}, {'Name': '车船税', 'Value': ''}, {'Name': '购买方识别号', 'Value': ''}, {'Name': '购买方地址、电话', 'Value': ''}, {'Name': '购买方开户行及账号', 'Value': ''}, {'Name': '校验码', 'Value': ''}, {'Name': '数量', 'Value': ''}, {'Name': '通行费标志', 'Value': ''}, {'Name': '是否代开', 'Value': ''}, {'Name': '是否收购', 'Value': ''}, {'Name': '机器编号', 'Value': ''}, {'Name': '成品油标志', 'Value': ''}, {'Name': '校验码备选', 'Value': ''}, {'Name': '校验码后六位备选', 'Value': ''}, {'Name': '发票号码备选', 'Value': ''}, {'Name': '服务类型', 'Value': ''}, {'Name': '市', 'Value': ''}, {'Name': '是否有公司印章', 'Value': '1'}], 'RequestId': '18543de3-9659-4e9c-a333-41090a184265'}


"""
