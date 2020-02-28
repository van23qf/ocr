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

