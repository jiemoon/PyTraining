# -*- coding: utf-8 -*-
#
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
#
import os
import sys
from core import Core_run
from modules.Mod_common import (daemonize,)

basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(basedir)

if __name__ == '__main__':
    # create firmwareupload running log dir
    if not os.path.exists('/var/log/firmwareupload'):
        os.makedirs('/var/log/firmwareupload')
    # daemon running ~
    std_err = '/var/log/firmwareupload/firmwareupload.log'
    daemonize(stdin=os.devnull, stdout=sys.stdout, stderr=std_err)
    # control by shell script
    pid_writting(os.getpid(), '/var/run/firmwareupload.pid')
    
    
    Core_run.main()
