#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api import call, func
from system import db
from system import Redis

import json
#import sqlalchemy.engine.result.ResultProxy


r = Redis.Redis()
r.set('name', 'qinfan')
print(r.get('name'))

