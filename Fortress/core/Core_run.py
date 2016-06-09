#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
"""
from modules import Mod_commutils
from Core_register import action_dict
from conf.Conf_database import database_info
from modules.Mod_sqlconnect import (sql_engine,sqlsession)


def check_database(sql_command='show databases'):
    """Check database whither exists ?
    
    :param: sql_command: show databases
    :return: bool
    """
    res_list = sqlsession.execute(sql_command).fetchall()
    database = database_info['sql_database']
    if (database,) in res_list:
        return database
    return None


def main(argv):
    """Main function.
    """
    action_type = None
    action_args = []
    if argv[1:]:
        action_type = argv[1]
    action_args = argv[2:]
    # invalid action_type
    if not action_type in action_dict:
        Mod_commutils.show_usage(argv[0])
    # check database is exists ?
    check_res = check_database()
    if check_res:
        exit_msg = ('database %s is exists, table structure changed, '
                    'should reconstruction.') % (check_res)
        Mod_commutils.exit_print(exit_msg,'notice',False)

    # called register to view handler, mayby load slow
    action_dict[action_type](sql_engine,sqlsession,argv[2:])
