#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from api.medical.deepfinch import common
import env
import json


URL = 'https://cloudapi.deepfinch.com/ocr/medical_invoice/jiangsu'


def ocr(file):
    files = {'file': file}
    result_json = json.loads(common.post(URL, files=files, data={'auto_rotate': True}))
    if result_json['status'] != 'OK':
        raise Exception(result_json['status'] + ": " + result_json['reason'])
    return {
        'status': True,
        'data': result_json['medical_result']
    }


if __name__ == '__main__':
    file = open(env.root_path + '/uploads/jiangsu1.jpg', 'rb')
    print(ocr(file))

"""
{'status': True, 'data': {'billing_date': None, 'charging_units': None, 'checksum': {'cost_categories': 0, 'total_cost': 1}, 'cost_categories': [], 'cost_detail_list': [{'amount': 14.0, 'check_info': 0, 'check_info_price': 0, 'check_name_info': 0, 'class': None, 'level': None, 'medical_type': None, 'name': None, 'ocr_name': '替格瑞洛片-倍林达>', 'origin_ocr_name': '替格瑞洛片-倍林达>', 'price': 795.5, 'selfpay': None, 'selfpay_ratio': None, 'spec': None, 'unit_price': None}], 'hospital_dates': [], 'hospital_days': None, 'hospital_name': '江苏省人民医院', 'hospital_no': None, 'medical_insurance_type': '普通自费', 'medical_organization_type': '综合医院', 'note_no': None, 'patient_gender': 1, 'patient_name': '吴英', 'payee': None, 'payments_info': [{'amount': 705.5, 'check_info': 0, 'name': '个人支付金额'}], 'service_serial_number': '0006138627', 'social_security_card_number': None, 'total_cost': 795.5, 'type': 1}}
{'status': True, 'data': {'billing_date': None, 'charging_units': None, 'checksum': {'cost_categories': 0, 'total_cost': 1}, 'cost_categories': [], 'cost_detail_list': [], 'hospital_dates': [], 'hospital_days': None, 'hospital_name': None, 'hospital_no': None, 'medical_insurance_type': None, 'medical_organization_type': None, 'note_no': None, 'patient_gender': 0, 'patient_name': '李六萍', 'payee': None, 'payments_info': [], 'service_serial_number': None, 'social_security_card_number': None, 'total_cost': None, 'type': 1}}
{'status': True, 'data': {'billing_date': None, 'charging_units': None, 'checksum': {'cost_categories': 0, 'total_cost': 0}, 'cost_categories': [], 'cost_detail_list': [{'amount': 32.0, 'check_info': 0, 'check_info_price': 0, 'check_name_info': 0, 'class': None, 'level': None, 'medical_type': None, 'name': None, 'ocr_name': '替格瑞洛片*信林达>', 'origin_ocr_name': '替格瑞洛片*信林达>', 'price': 14.0, 'selfpay': 5.0, 'selfpay_ratio': 0.3571, 'spec': None, 'unit_price': None}], 'hospital_dates': [], 'hospital_days': None, 'hospital_name': '江苏省人民医院', 'hospital_no': None, 'medical_insurance_type': '普通自费', 'medical_organization_type': '综合医院', 'note_no': None, 'patient_gender': 1, 'patient_name': '吴英', 'payee': None, 'payments_info': [{'amount': 705.5, 'check_info': 0, 'name': '个人支付金额'}], 'service_serial_number': '0006138627', 'social_security_card_number': None, 'total_cost': 795.5, 'type': 1}}

"""
