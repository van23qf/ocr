#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import config


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


def get_all(sql):
    return engine.execute(sql)


def get_one(sql):
    return engine.execute(sql).first()

