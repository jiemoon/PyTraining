#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose: 
#
# should be loaded after fortress user login.
#
#
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf.Conf_database import (database_info,sqlconnect_str)


# max 10 connections
sql_engine = create_engine(sqlconnect_str,echo=True,max_overflow=10)

# create session class, bind sql_engine
SqlSession = sessionmaker(bind=sql_engine)

# for execute sql command
sqlsession = SqlSession()
