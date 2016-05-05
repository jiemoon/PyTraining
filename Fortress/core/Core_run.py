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
    # called register to view handler
    action_dict[action_type](argv[2:])
