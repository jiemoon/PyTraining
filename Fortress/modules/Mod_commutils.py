#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
"""
import os
import sys
import datetime


def exit_print(exit_msg, exit_level, is_exit=False):
    """Is exit with print ?
    
    :param exit_msg: exit message
    :param exit_level: notice/errors
    :param is_exit: bool
    :return: None
    """
    message = 'found %s: %s' % (exit_level, exit_msg)
    if is_exit:
        sys.exit(message)
    else:
        print message
        

def show_usage(execute_file):
    """Show usage of fortress.
    
    action type:
    
    initdatabase    init database
    ssh_host_add    add ssh host info
    ssh_user_add    add ssh user info
    ssh_grup_add    add ssh grup info
    fts_user_add    add fortress info
    """
    copyright = os.linesep.join([
        '%s version 0.0.1' % (execute_file),
        'Copyright (C) 2016-%s by limanman and others.' % (datetime.datetime.now().year),
        'Web site: http://my.oschina.net/pydevops/',
    ])
    
    all_usage='''
    Usage: %s <action-type> [option] [yaml-file]
    
    action-types
        initdatabase   use sqlalchemy init database
        ssh_host_add   use sqlalchemy add sshhosts
        ssh_user_add   use sqlalchemy add sshusers
        ssh_grup_add   use sqlalchemy add sshgroup
        fts_user_add   use sqlalchemy add fortress users
    
    options
        -f             yaml file for action types''' % (execute_file)

    exit_msg = os.linesep.join([
        copyright,
        all_usage,
    ])
    sys.exit(exit_msg)
