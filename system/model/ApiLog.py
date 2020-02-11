#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from system import db

Base = db.Base
engine = db.engine
DBSession = db.DBSession


class Model(Base):
    # 表的名字:
    __tablename__ = 'api_log'
    db_session = DBSession()

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(String(16))
    api_provider = Column(String(16))
    api_name = Column(String(16))
    result = Column(Text())
    created = Column(DateTime())

    def insert(self):
        self.db_session.add(self)
        self.db_session.commit()
        self.db_session.close()

