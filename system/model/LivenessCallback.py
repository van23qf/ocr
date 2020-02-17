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
    __tablename__ = 'liveness_callback'
    db_session = DBSession()

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    nonce_str = Column(String(32))
    result = Column(Text())
    check_status = Column(Integer)
    created = Column(DateTime())

    def insert(self):
        self.db_session.add(self)
        self.db_session.flush()
        insert_id = self.id
        self.db_session.commit()
        self.db_session.close()
        return insert_id

