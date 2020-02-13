#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from flask import Flask, request
from system import func
import global_dict

app = Flask(__name__, static_folder='uploads')
app.config['ENV'] = 'development'


global_dict.init()


@app.route('/idcard', methods=['POST'])
def idcard():
    from controller import Idcard
    try:
        return Idcard.index()
    except Exception as e:
        return {'status': False, 'msg': str(e)}


@app.route('/invoice', methods=['POST'])
def invoice():
    from controller import Invoice
    try:
        return Invoice.index()
    except Exception as e:
        return {'status': False, 'msg': str(e)}


@app.route('/liveness/url', methods=['POST'])
def liveness_url():
    from controller import Liveness
    try:
        return Liveness.url()
    except Exception as e:
        return {'status': False, 'msg': str(e)}


@app.route('/liveness/faceid/callback', methods=['POST'])
def liveness_faceid_callback():
    from controller import Liveness
    try:
        return Liveness.faceid_callback()
    except Exception as e:
        return {'status': False, 'msg': str(e)}


if __name__ == '__main__':
    app.run(port=5000)

