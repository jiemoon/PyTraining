#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
"""
from sqlalchemy import create_engine


database_info = {
    'sql_type': 'mysql',
    'sql_engine': 'mysqldb',
    'sql_user': 'root',
    'sql_pass': 'root',
    'sql_port': 3306,
    'sql_server': '172.24.10.1',
    'sql_database': 'fortress',
    'sql_charset': 'utf8',
}

sqlconnect_str = '%s+%s://%s:%s@%s:%s/%s?charset=%s' % (
    database_info['sql_type'],
    database_info['sql_engine'],
    database_info['sql_user'],
    database_info['sql_pass'],
    database_info['sql_server'],
    database_info['sql_port'],
    database_info['sql_database'],
    database_info['sql_charset'],

)

# print sql connect string
if __name__ == '__main__':
   print  sqlconnect_str
