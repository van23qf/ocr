#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api import call, func
from system import db

import json
#import sqlalchemy.engine.result.ResultProxy

result = db.get_one("select * from api_log where id=3")
print(result)
