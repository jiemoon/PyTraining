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
from core import Core_run

basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(basedir)

if __name__ == '__main__':
    # called core main handler
    Core_run.main(sys.argv)
