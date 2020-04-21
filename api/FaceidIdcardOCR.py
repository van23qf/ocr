#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
        身份证OCR模块
    documents https://faceid.com/pages/documents/10881005

    legality 返回身份证照片的合法性检查结果。它为一个结构体，里面包含身份证的五种分类及真实身份证判定阈值。结构体是按照key-value pair类型进行设计。其中身份证五种分类的概率值（取［0，1］区间实数，取3位有效数字，总和等于1）。
    * ID_Photo：分类1 - 真实身份证照片
    * Temporary_ID_Photo：分类2 - 临时身份证照片
    * Photocopy：分类3 - 身份证的复印件
    * Screen：分类4 - 手机或电脑屏幕翻拍的照片
    * Edited：分类5 - 用工具合成或者编辑过的身份证图片
    * ID_Photo_Threshold：表示判断为真实身份证照片的阈值，通常来说，如果ID_Photo的值不低于该阈值，则可以认定为真实拍摄的；
    注：随产品迭代，未来会增加新的分类，因此在集成此API时请留意兼容性。
"""

__author__ = 'Van23qf'


import requests
import json
import base64

from system import global_dict, func


# 判断为真实身份证照片的阈值
ID_Photo_Threshold = 0.5


def ocr(file, side='front'):
    api_config = global_dict.get_value("api_config")
    data = {
        'api_key': api_config['appid'],
        'api_secret': api_config['appsecret'],
        # 传1时返回头像
        'return_portrait': '0',
    }
    image_file = {'image': file}
    response = requests.post('https://api.megvii.com/faceid/v3/ocridcard', data=data, files=image_file)
    result = json.loads(response.text)
    if not result.get('result'):
        #return {'status': False, 'msg': result['error']}
        return {'status': False, 'msg': '当前身份证照片非法'}
    if result['result'] != 1001 and result['result'] != 1002:
        return {'status': False, 'msg': '身份证照片非法'}
    if result['legality']['Edited'] > 0:
        msg = '该身份证照片为PS合成'
    else:
        if result['result'] == 1001:
            msg = '该身份证照片完全合法'
        else:
            if result['legality']['ID_Photo'] >= ID_Photo_Threshold:
                msg = '该身份证照片为真实拍摄的合法照片'
            else:
                msg = '该身份证照片不合法，请确认照片是否完整或PS'
    if result['side'] == 0:
        return {
            'status': True,
            'msg': msg,
            'data': {
                'side': 'front',
                'name': result['name']['result'],
                'gender': result['gender']['result'],
                'nation': result['nationality']['result'],
                'birth': result['birth_year']['result'] + '-' + result['birth_month']['result'] + '-' + result['birth_day']['result'],
                'address': result['address']['result'],
                'idnum': result['idcard_number']['result'],
            }
        }
    else:
        return {
            'status': True,
            'msg': msg,
            'data': {
                'side': 'back',
                'authority': result['issued_by']['result'],
                'validity': func.insert_str(result['valid_date_start']['result'], '.', [4, 7]) + '-' + func.insert_str(result['valid_date_end']['result'], '.', [4, 7]),
            }
        }


if __name__ == '__main__':
    #result = ocr('../uploads/idcard_front.jpg')
    #print(result)
    str1 = '20100617'
    print(str1)
    # if result['result'] != 1001 and result['result'] != 1002:
    #     print('识别失败')
    # else:
    #     if result['side'] == 1:
    #         print('当前图片为国徽面')
    #         print('签发机关：' + result['issued_by']['result'])
    #         print('有效日期的起始时间：' + result['valid_date_start']['result'])
    #         print('有效日期的结束时间：' + result['valid_date_end']['result'])
    #     else:
    #         print('当前图片为人像面')
    #         print('姓名：' + result['name']['result'])
    #         print('性别：' + result['gender']['result'])
    #         print('民族：' + result['nationality']['result'])
    #         print('出生年份：' + result['birth_year']['result'])
    #         print('出生月份：' + result['birth_month']['result'])
    #         print('出生日：' + result['birth_day']['result'])
    #         print('身份证号：' + result['idcard_number']['result'])
    #         print('住址：' + result['address']['result'])
    #     if result['legality']['Edited'] > 0:
    #         print('该身份证照片为PS合成')
    #     else:
    #         if result['result'] == 1001:
    #             print('该身份证照片完全合法')
    #         else:
    #             if result['legality']['ID_Photo'] >= idcard_ocr.ID_Photo_Threshold:
    #                 print('该身份证照片为真实拍摄的合法照片')
    #             else:
    #                 print('该身份证照片不合法')
