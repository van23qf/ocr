#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import result
from sqlalchemy.exc import InvalidRequestError

from config import config


engine = create_engine('mysql+mysqlconnector://'
                       + config.db['default']['dbuser'] + ':'
                       + config.db['default']['dbpass'] + '@'
                       + config.db['default']['host'] + ':'
                       + config.db['default']['port'] + '/'
                       + config.db['default']['dbname'] + '?charset=utf8')
DBSession = sessionmaker(bind=engine)
db_session = scoped_session(DBSession)

Base = declarative_base()
Base.query = db_session.query_property()


def get_result(sql):
    return engine.execute(sql)


def result_keys(fetch_result):
    return fetch_result.keys()


def to_dict(keys, fetch_list):
    all_dict = []
    for v in fetch_list:
        rows = dict(zip(keys, v))
        all_dict.append(rows)
    return all_dict


def get_all(sql):
    fetch_result = get_result(sql)
    keys = result_keys(fetch_result)
    fetch_list = fetch_result.fetchall()
    return to_dict(keys, fetch_list)


def get_one(sql):
    all_dict = get_all(sql)
    if not all_dict:
        return None
    return all_dict[0]

