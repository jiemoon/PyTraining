# -*- coding: utf-8 -*-
#
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
#
import os
import Queue
import pprint
import threading
import Core_rsync
import Core_mulitask
from modules import Mod_firmware
from conf import Conf_summary
from modules import Mod_common
from modules import Mod_svncheck


def main():
    """Main function
    """
    # write svn_yaml_key, svn_full_url, svn_release_note to queue with blocking
    yaml_file = os.path.join(os.getcwd(),'conf','Conf_svnlogin.yaml')
    yaml_dict = Mod_common.yaml_parse(yaml_file)

    thread_list = []
    thread_lock = threading.Lock()
    thread_queue = Queue.Queue()
    for cur_key,cur_val in yaml_dict.iteritems():
        thread_name = cur_key.strip()
        thread_rate = int(cur_val['uprate'])

        svn_username = cur_val['user']
        svn_password = cur_val['passwd']

        svn_day = int(cur_val['update'])
        svn_url = cur_val['baseurl']
        cur_thread = Core_mulitask.SvnSummaryDiff(thread_queue,
                                                  thread_lock,
                                                  thread_name,
                                                  thread_rate,
                                                  svn_username,
                                                  svn_password,
                                                  svn_day,svn_url,cur_key)
        thread_list.append(cur_thread)
        cur_thread.start()

    # read svn_yaml_key, svn_full_url, svn_release_note from queue with blocking
    while True:
        svn_key,svn_url,svn_note = thread_queue.get(block=True)
        print '=>#############################################################'
        print 'svn_key',svn_key
        print 'svn_url',svn_url
        print 'svn_note',svn_note
        print '=>#############################################################'
        # start download firmware from svn.
        Mod_firmware.f_download(svn_key,svn_url,svn_note)
        Conf_summary.sync_info['rsync_sdir'] = Conf_summary.sync_dict[svn_key]
        # start upload firmware with rsync
        Core_rsync.push_local_firmwares(svn_key,
                                        Conf_summary.sync_info['rsync_path'],
                                        Conf_summary.sync_info['rsync_pass'],
                                        Conf_summary.sync_info['rsync_sdir'],
                                        Conf_summary.sync_info['rsync_user'],
                                        Conf_summary.sync_info['rsync_addr'],
                                        Conf_summary.sync_info['rsync_ddir'])
        # start check and email notice somebody.
        # ...

