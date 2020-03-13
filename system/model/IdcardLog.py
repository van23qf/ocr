#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError

from system import db

Base = db.Base
engine = db.engine
DBSession = db.DBSession


class Model(Base):
    # 表的名字:
    __tablename__ = 'idcard_log'
    db_session = DBSession()

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    idcard = Column(String(20))
    realname = Column(String(16))

    def insert(self):
        try:
            self.db_session.add(self)
            self.db_session.flush()
            insert_id = self.id
            self.db_session.commit()
            self.db_session.close()
            return insert_id
        except InvalidRequestError:
            self.db_session.rollback()
            raise Exception(str(InvalidRequestError))
