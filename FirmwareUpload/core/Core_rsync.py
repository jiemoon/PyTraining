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
import tempfile
import subprocess
from conf import Conf_summary


def push_local_firmwares(svn_key,rsync_path,rsync_pass,rsync_sdir,rsync_user,rsync_addr,rsync_ddir):
    '''Push local firmware to remote rsync server.

    :param:   svn_key: svn key
    :param:rsync_path: rsync bin file path
    :param:rsync_pass: rsync pass
    :param:rsync_sdir: rsync sou dirname
    :param:rsync_user: rsync user
    :param:rsync_addr: rsync server
    :param:rsync_ddir: rsync dst dirname
    '''
    level = 'info'
    message = 'succ rsync %s to %s::%s' % (Conf_summary.sync_dict[svn_key],rsync_addr,rsync_ddir)
    if not rsync_sdir.endswith(os.sep):
        rsync_sdir = rsync_sdir + os.sep
    rsync_cmd = []
    rsync_cmd.append(rsync_path)
    rsync_cmd.append('-avzut')
    rsync_cmd.append('--progress')
    rsync_cmd.append('--password-file={0}'.format(rsync_pass))
    rsync_cmd.append(rsync_sdir)
    rsync_cmd.append('{0}@{1}::{2}'.format(rsync_user,rsync_addr,rsync_ddir))
    whandle = tempfile.NamedTemporaryFile(mode='a+b')
    try:
        processer = subprocess.Popen(rsync_cmd,stdout=whandle,stderr=subprocess.PIPE)
        position = 0
        rhandle = open(whandle.name,'r+b')
        while True:
            whandle.file.flush()
            rhandle.seek(position)
            cur_line = rhandle.readline()
            res_line = cur_line.strip()
            if res_line:
                print res_line.strip()
                position = rhandle.tell()
            if processer.poll() != None:
                break
        whandle.close()
    except Exception as Err:
        level = 'error'
        message = 'fail rsync %s to %s::%s' % (Conf_summary.sync_dict[svn_key],rsync_addr,rsync_ddir)
    # Conf_summary.logg_dict[svn_key](message, level)
