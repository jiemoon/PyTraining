#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
"""
from Mod_sqlalchemy import Base
from modules import Mod_commutils


def check_params(args):
    """Check command args.
    
    :param: args: command args
    """
     if not '-f' in args:


def initdatabase(sql_engine,sqlsession,args):
    """Create database table structure.
    
    :param: sql_engine: sql engine  for called
    :param: sqlsession: sql session for execute sql command
    :param: args: some args
    :return: None
    """
    Base.metadata.create_all(sql_engine)


def ssh_host_add(sql_engine,sqlsession,args):
    """Create database table structure.
    
    :param: sql_engine: sql engine  for called
    :param: sqlsession: sql session for execute sql command
    :param: args: some args
    :return: None
    """
    if not '-f' in args:
        exit_msg


def ssh_user_add(sql_engine,sqlsession,args):
    print 'ssh_user_add'


def ssh_grup_add(sql_engine,sqlsession,args):
    print 'ssh_grup_add'


def fts_user_add(sql_engine,sqlsession,args):
    print 'fts_user_add'
