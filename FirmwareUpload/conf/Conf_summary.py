# -*- coding: utf-8 -*-
#
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
#
import os
import logging
import logging.config
from modules import Mod_common


def __merge_path(relative_path):
    """Merge relative file path.

    :param relative_path: relative file path
    """
    return os.path.join(os.getcwd(),relative_path)

# -------------------------------------------------------------------
__curpardir = os.path.abspath(os.path.dirname(__file__))
# svn yaml   configure dict
__yaml_file = os.path.join(
    __curpardir,'Conf_svnlogin.yaml',
)
# -------------------------------------------------------------------
yaml_dict = Mod_common.yaml_parse(__yaml_file)

# svn logging instance
# -------------------------------------------------------------------
__ipc_logger = Mod_common.Logger(
    'ipc-detect',
    __merge_path(yaml_dict['IPC']['logfile']),
)
__dvr_logger = Mod_common.Logger(
    'dvr-detect',
    __merge_path(yaml_dict['DVR']['logfile']),
)
__xmjp_logger = Mod_common.Logger(
    'xmjp-detect',
    __merge_path(yaml_dict['XMJP']['logfile']),
)
__jvfeng_logger = Mod_common.Logger(
    'jvfeng-detect',
    __merge_path(yaml_dict['JvFeng']['logfile']),
)
# ------------------------------------------------------------------
logg_dict = {
    'IPC'   : getattr(__ipc_logger,'logger'),
    'DVR'   : getattr(__dvr_logger,'logger'),
    'XMJP'  : getattr(__xmjp_logger,'logger'),
    'JvFeng': getattr(__jvfeng_logger,'logger'),
}

# download dirs
# ------------------------------------------------------------------
__ipc_dir = os.path.join(os.getcwd(),'download','IPC')
__dvr_dir = os.path.join(os.getcwd(),'download','DVR')
__xmjp_dir = os.path.join(os.getcwd(),'download','XMJP')
__jvfeng_dir = os.path.join(os.getcwd(),'download','JvFeng')
# -------------------------------------------------------------------
dest_dict = {
    'IPC': __ipc_dir,
    'DVR': __dvr_dir,
    'XMJP': __xmjp_dir,
    'JvFeng': __jvfeng_dir
}

# rsync dirs
#--------------------------------------------------------------------
__ipc_dst = os.path.join(os.getcwd(),'upgrade_files','IPC')
__dvr_dst = os.path.join(os.getcwd(),'upgrade_files','DVR')
__xmjp_dst = os.path.join(os.getcwd(),'upgrade_files','XMJP')
__jvfeng_dst = os.path.join(os.getcwd(),'upgrade_files','JvFeng')
#--------------------------------------------------------------------
sync_dict = {
    'IPC': __ipc_dst,
    'DVR': __dvr_dst,
    'XMJP': __xmjp_dst,
    'JvFeng': __jvfeng_dst
}

# rsync server
sync_info = {
    'rsync_sdir': None,
    'rsync_path': '/usr/bin/rsync',
    'rsync_user': 'rsync_limanman',
    'rsync_addr': '120.132.75.75',
    'rsync_ddir': 'upgrade_server',
    'rsync_pass': '/etc/rsync.password'
}
#--------------------------------------------------------------------

# auto create dirname
#--------------------------------------------------------------------
for cur_dir in dest_dict.itervalues():
    if not os.path.exists(cur_dir):
        os.makedirs(cur_dir)
for cur_dir in sync_dict.itervalues():
    if not os.path.exists(cur_dir):
        os.makedirs(cur_dir)
#--------------------------------------------------------------------
