#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api.medical.deepfinch import InvoiceGeneral
from system import global_dict

def ocr(file):
    try:
        result = InvoiceGeneral.ocr(file)
        if not result['status']:
            return result
        return {
            'status': True,
            'data': {
                'goods_name': result['data']['vat_invoice_goods_list'],  # 药品名称
                'payer_name': result['data']['vat_invoice_payer_name'],  # 购药人
                'goods_unit': '',  # 药品单位
                'goods_num': result['data']['vat_invoice_electrans_quantity'],  # 药品数量
                'issue_date': result['data']['vat_invoice_issue_date'],  # 结算日期
                'invoice_number': result['data']['vat_invoice_haoma'],  # 发票号码
                'invoice_amount': result['data']['vat_invoice_total'],  # 金额
                'invoice_unit_price': result['data']['vat_invoice_electrans_unit_price'],  # 单价
            }
        }
    except Exception as err:
        return {'status': False, 'msg': str(err)}
