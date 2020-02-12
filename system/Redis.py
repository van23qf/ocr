#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
import config


class Redis():
    def __init__(self):
        self.__redis = redis.StrictRedis(host=config.redis['default']['host'], port=config.redis['default']['port'], password=config.redis['default']['password'])

    def set(self, key, value):
        return self.__redis.set(key, value)

    def get(self, key):
        if self.__redis.exists(key):
            return self.__redis.get(key)
        else:
            return None
