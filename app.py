#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from flask import Flask, request
from api import call, func

app = Flask(__name__, static_folder='uploads')
app.config['ENV'] = 'development'


@app.route('/idcard', methods=['POST'])
def idcard():
    side = request.form.get('side')
    project = request.form.get('project')
    file_name = request.form.get('file_name')
    api_provider = request.form.get('api_provider')
    result = json.dumps(call.idcard_ocr(file_name, side, api_provider))
    func.save_api_log('idcard', result, project, api_provider)
    return result


if __name__ == '__main__':
    app.run(port=5000)

