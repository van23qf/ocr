#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from flask import Flask, request
from api import call
from system import func
import global_dict

app = Flask(__name__, static_folder='uploads')
app.config['ENV'] = 'development'


global_dict.init()


@app.route('/idcard', methods=['POST'])
def idcard():
    from controller import Idcard
    try:
        return json.dumps(Idcard.index())
    except Exception as e:
        return json.dumps({'status': False, 'msg': str(e)})


@app.route('/invoice', methods=['POST'])
def invoice():
    from controller import Invoice
    try:
        return json.dumps(Invoice.index())
    except Exception as e:
        return json.dumps({'status': False, 'msg': str(e)})


if __name__ == '__main__':
    app.run(port=5000)

