#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api import call, func

result = call.general_ocr(func.read_file('../uploads/table.jpg'), 'tencent')
print(result)
