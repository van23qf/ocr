#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from api.medical.deepfinch import common
import env
import json


URL = 'https://cloudapi.deepfinch.com/ocr/medical_invoice/tianjin'


def ocr(file):
    files = {'file': file}
    result_json = json.loads(common.post(URL, files=files, data={'auto_rotate': True}))
    if result_json['status'] != 'OK':
        raise Exception(result_json['status'] + ": " + result_json['reason'])
    return {
        'status': True,
        'data': common.format_result(result_json['medical_result'], 'tianjin')
    }


if __name__ == '__main__':
    file = open(env.root_path + '/uploads/tianjin.jpg', 'rb')
    print(ocr(file))

"""
{"request_id":"TID93cb475755d341ee84480b92c6c4ce1d","status":"OK","image_id":"1fcdf86b0c4e462e82036eb03b66db39","degree":0,"medical_result":{"billing_date":"2007-06-14","charging_units":null,"checksum":{"cost_categories":1,"total_cost":1},"cost_categories":[{"cost":727.77,"name":"西药"},{"cost":0.03,"name":"舍入费"}],"cost_detail_list":[{"amount":20.0,"check_info":0,"check_info_price":0,"check_name_info":0,"class":null,"level":null,"medical_type":1,"name":"法莫替丁","ocr_name":"法莫替丁(合资)","origin_ocr_name":"法莫替丁(合资)","price":null,"selfpay":null,"selfpay_ratio":0,"spec":null,"unit_price":null},{"amount":90.0,"check_info":0,"check_info_price":0,"check_name_info":0,"class":null,"level":null,"medical_type":null,"name":null,"ocr_name":"替格瑞洛","origin_ocr_name":"替格瑞洛","price":1.0,"selfpay":null,"selfpay_ratio":null,"spec":null,"unit_price":null}],"hospital_dates":[],"hospital_days":null,"hospital_name":null,"hospital_no":null,"medical_insurance_type":"现金","medical_organization_type":null,"note_no":null,"patient_gender":0,"patient_name":"陈方升","payee":"收款人","payments_info":[{"amount":727.77,"check_info":0,"name":"个人支付金额"}],"service_serial_number":"97582668","social_security_card_number":null,"total_cost":727.8,"type":1}}

"""
