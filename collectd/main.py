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
import time
from core import core_run
from modules.CommUtils import daemonize, pid_writting


basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(basedir)

if __name__ == '__main__':
    std_err = os.path.join(basedir, 'logs', 'collectd_srv_err.log')
    daemonize(stdin=os.devnull, stdout=sys.stdout, stderr=std_err)
    # use scripts/collectd start|stop|restart control service
    pid_writting(os.getpid(), '/var/run/collectd.pid')
    # redis write rate, default 5 seconds
    # redis key expire, default 30 seconds
    core_run.main(5, 30)
