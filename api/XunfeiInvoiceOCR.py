#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    讯飞OCR发票识别模块
    documents https://www.xfyun.cn/doc/words/VAT-invoice-recg/API.html
"""

__author__ = 'qinfan'

import requests
import time
import json
import hashlib
import base64

from api import Config


OCR_API_CONFIG = {
    'appid': Config.xunfei['invoice']['appid'],
    'api_key': Config.xunfei['invoice']['api_key']
}

# 发票字段名称
INVOICE_FIELDS = {
    'vat_invoice_correct_code': '校验码',
    'vat_invoice_daima': '发票代码',
    'vat_invoice_haoma': '发票号码',
    'vat_invoice_issue_date': '开票日期',
    'vat_invoice_rate_payer_id': '纳税人识别号',
    'vat_invoice_total': '合计',
    'vat_invoice_tax_rate': '税率',
    'vat_invoice_jida_haoma': '机打号码',
    'vat_invoice_seller_name': '销售方名称',
    'vat_invoice_seller_bank_account': '销售方开户行及帐号',
    'vat_invoice_seller_id': '销售方纳税人识别号',
    'vat_invoice_seller_addr_tell': '销售方地址电话',
    'vat_invoice_payer_name': '购买方名称',
    'vat_invoice_payer_bank_account': '购买方开户行及账号',
    'vat_invoice_payer_addr_tell': '购买方地址电话',
    'vat_invoice_total_cover_tax': '价税合计大写',
    'vat_invoice_total_cover_tax_digits': '价税合计小写',
    'vat_invoice_electrans_unit_price': '单价',
    'vat_invoice_electrans_quantity': '数量',
    'vat_invoice_tax_total': '税额合计',
    'vat_invoice_goods_list': '货物或服务名称',
    'vat_invoice_price_list': '金额明细',
    'vat_invoice_tax_rate_list': '税率明细',
    'vat_invoice_tax_list': '税额明细',
    'vat_invoice_zhuan_yong_flag': '专票/普票',
    'vat_invoice_dai_kai_flag': '代开',
    'vat_invoice_note': '备注',
    'vat_invoice_daima_right_side': '右侧打印发票代码',
    'vat_invoice_haoma_right_side': '右侧打印发票号码	',
}


class InvoiceOCR(object):

    def __init__(self):
        self.appid = OCR_API_CONFIG['appid']
        self.api_key = OCR_API_CONFIG['api_key']
        self.api_url = 'http://webapi.xfyun.cn/v1/service/v1/ocr/invoice'
        self.set_header()

    def set_header(self):
        cur_time = str(int(time.time()))
        param = {"engine_type": "invoice"}
        param = json.dumps(param)
        param_base64 = base64.b64encode(param.encode('utf-8'))

        m2 = hashlib.md5()
        str1 = self.api_key + cur_time + str(param_base64,'utf-8')
        m2.update(str1.encode('utf-8'))
        check_sum = m2.hexdigest()

        self.header = {
            'X-CurTime': cur_time,
            'X-Param': param_base64,
            'X-Appid': self.appid,
            'X-CheckSum': check_sum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }

    def ocr(self, file):
        invoice_file_base64 = str(base64.b64encode(file), 'utf-8')
        self.data = {
            'image': invoice_file_base64
        }
        response_data = requests.post(self.api_url, data=self.data, headers=self.header)
        result = json.loads(str(response_data.content, 'utf-8'))
        if result['code'] != '0':
            return {'status': False, 'msg': '发票识别失败'}
        return {
            'status': True,
            'data': {
                'drug_name': result['data']['vat_invoice_goods_list'],  # 药品名称
                'patient_name': result['data']['vat_invoice_payer_name'],  # 购药人
                'drug_unit': '',  # 药品单位
                'drug_num': result['data']['vat_invoice_electrans_quantity'],  # 药品数量
                'invoice_date': result['data']['vat_invoice_issue_date'],  # 结算日期
                'invoice_sn': result['data']['vat_invoice_haoma'],  # 发票号码
                'invoice_amount': result['data']['vat_invoice_total'],  # 金额
                'invoice_unit_price': result['data']['vat_invoice_electrans_unit_price'],  # 单价
            }
        }


if __name__ == '__main__':
    invoice = InvoiceOCR()
    result = invoice.ocr('../uploads/222222.jpg')
    print(result)
