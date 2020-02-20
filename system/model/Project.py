#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError

from system import db, func

Base = db.Base
engine = db.engine
DBSession = db.DBSession


class Model(Base):
    # 表的名字:
    __tablename__ = 'project'
    db_session = DBSession()

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_name = Column(String(16))
    secret = Column(String(32))
    api_access = Column(String(128))

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

    def get_by_project(self, project_name):
        try:
            result = self.db_session.query(Model).filter(Model.project_name == project_name).one()
            self.db_session.close()
            return result
        except InvalidRequestError:
            self.db_session.rollback()
            return None

    def get_access_list(self, project_name):
        result = self.get_by_project(project_name)
        if not result or not result.api_access:
            return None
        return result.api_access.split(',')

    def check_api_access(self, project_name, api_name):
        access_list = self.get_access_list(project_name)
        if not access_list:
            return False
        if api_name not in access_list:
            return False
        return True

    def check_project_verify(self, project_name, ts, out_signature):
        project_data = self.get_by_project(project_name)
        if not project_data:
            return False
        signature = func.md5(project_data.project_name + project_data.secret + ts)
        if out_signature != signature:
            return False
        return True

