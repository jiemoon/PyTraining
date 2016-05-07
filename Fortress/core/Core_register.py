#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
"""
from modules import Mod_view


action_dict = {
    'initdatabase': Mod_view.initdatabase,
    'ssh_host_add': Mod_view.ssh_host_add,
    'ssh_user_add': Mod_view.ssh_user_add,
    'ssh_grup_add': Mod_view.ssh_grup_add,
    'fts_user_add': Mod_view.fts_user_add,
    'sta_sessions': Mod_view.sta_sessions,
}
