#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from flask import Flask, request
from system import func
from system import global_dict
from config import config

app = Flask(__name__, static_folder='uploads')
app.config['ENV'] = 'development'


global_dict.init()


@app.route('/idcard', methods=['POST'])
def idcard():
    from controller import Idcard
    try:
        func.check_api_access('idcard')
        return Idcard.index()
    except Exception as e:
        return {'status': False, 'msg': str(e)}


@app.route('/invoice', methods=['POST'])
def invoice():
    from controller import Invoice
    try:
        func.check_api_access('invoice')
        return Invoice.index()
    except Exception as e:
        return {'status': False, 'msg': str(e)}


@app.route('/liveness/url', methods=['POST'])
def liveness_url():
    from controller import Liveness
    try:
        func.check_api_access('liveness')
        return Liveness.url()
    except Exception as e:
        return {'status': False, 'msg': str(e)}


@app.route('/liveness/result_check', methods=['POST'])
def liveness_result_check():
    from controller import Liveness
    try:
        return Liveness.result_check()
    except Exception as e:
        return {'status': False, 'msg': str(e)}


@app.route('/liveness/faceid/callback', methods=['GET', 'POST'])
def liveness_faceid_callback():
    from controller import Liveness
    try:
        return Liveness.faceid_callback()
    except Exception as e:
        return {'status': False, 'msg': str(e)}


@app.route('/liveness/faceid/return', methods=['GET', 'POST'])
def liveness_faceid_return():
    return "success"


@app.route('/test', methods=['GET', 'POST'])
def test():
    return str(request.headers)


if __name__ == '__main__':
    app.run(port=config.port)

