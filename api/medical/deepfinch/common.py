#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests


headers = {
    'X-DF-API-ID': "dcf0d8845a4b43d8b5bc2380e795804d",
    'X-DF-API-SECRET': "0dd1e375185d4c719972f7e83d44f3d9",
}


def post(url, **kw):
    response = requests.post(url, headers=headers, files=kw.get('files'), data=kw.get('data'))
    return response.text


def format_result(medical_result, type='general'):
    data = {}
    if type == 'general':
        # 患者基本信息
        data['姓名'] = medical_result['patient_name']
        data['性别'] = '男' if medical_result['patient_gender'] == 1 else '女'
        data['社会保障卡号码'] = medical_result['social_security_card_number']
        data['医院名称'] = medical_result['hospital_name']
        data['医疗机构类型'] = medical_result['medical_organization_type']
        data['医保类型'] = medical_result['medical_insurance_type']
        # 票据信息
        data['发票号'] = medical_result['note_no']
        data['交易流水号'] = medical_result['service_serial_number']
        data['开票时间'] = medical_result['billing_date']
        data['收款人'] = medical_result['payee']
        data['收款单位'] = medical_result['charging_units']
        # 金额信息
        data['总金额'] = medical_result['total_cost']
        data['门诊大额支付'] = medical_result['total_cost']
    else:
        pass

