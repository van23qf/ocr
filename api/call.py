#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
from api import FaceidIdcardOCR, TencentIdcardOCR, XunfeiIdcardOCR
from api import TencentInvoiceOCR, XunfeiInvoiceOCR
from api import XunfeiGeneralOCR, TencentGeneralOCR

from api import func


def idcard_ocr(file_path, side='front', api='faceid'):
    """
    调用身份证ocr
    :param file_path:
    :param side:
    :param api:
    :return:
    """
    file = func.read_file(file_path)
    if not file:
        raise Exception('文件读取失败')
    if api == 'faceid':
        result = FaceidIdcardOCR.ocr(file, side)
    elif api == 'tencent':
        result = TencentIdcardOCR.ocr(file, side)
    elif api == 'xunfei':
        result = XunfeiIdcardOCR.ocr(file, side)
    else:
        raise Exception('接口未知')
    return result


def invoice_ocr(file_path, api='tencent'):
    """
    调用发票识别
    :param file_path:
    :param api:
    :return:
    """
    file = func.read_file(file_path)
    if not file:
        raise Exception('文件读取失败')
    if api == 'tencent':
        result = TencentInvoiceOCR.ocr(file)
    elif api == 'xunfei':
        xunfei = XunfeiInvoiceOCR.InvoiceOCR()
        result = xunfei.ocr(file)
    else:
        raise Exception('接口未知')
    return result


def general_ocr(file_path, api='xunfei'):
    """
    通用文字识别
    :param file_path:
    :param api:
    :return:
    """
    file = func.read_file(file_path)
    if not file:
        raise Exception('文件读取失败')
    if api == 'xunfei':
        result = XunfeiGeneralOCR.ocr(file)
    elif api == 'tencent':
        result = TencentGeneralOCR.ocr(file)
    else:
        raise Exception('接口未知')
    return result


if __name__ == '__main__':
    print(general_ocr('../uploads/table.jpg', 'xunfei'))
