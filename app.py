#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from flask import Flask, request
from api import call, func
import global_dict

app = Flask(__name__, static_folder='uploads')
app.config['ENV'] = 'development'


global_dict.init()


@app.route('/idcard', methods=['POST'])
def idcard():
    side = request.form.get('side')
    project = request.form.get('project')
    file_name = request.form.get('file_name')
    api_provider = request.form.get('api_provider')
    api_config = func.get_api_config('idcard', project, api_provider)
    if not api_config:
        return json.dumps({'status': False, 'msg': '配置错误'})
    global_dict.set_value("api_config", api_config)
    result = json.dumps(call.idcard_ocr(file_name, side, api_provider))
    func.save_api_log('idcard', result, project, api_provider)
    return result


if __name__ == '__main__':
    app.run(port=5000)

