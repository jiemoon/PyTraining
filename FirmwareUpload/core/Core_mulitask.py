# -*- coding: utf-8 -*-
#
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
#
import time
import pprint
import threading
from modules import Mod_svncheck


class SvnSummaryDiff(threading.Thread):
    def __init__(self,thread_queue,thread_lock,thread_name,sleep_time,*args):
        self.sleep_time = sleep_time
        self.thread_lock = thread_lock
        self.thread_name = thread_name
        self.thread_queue = thread_queue
        super(SvnSummaryDiff,self).__init__()
        # svn_check instance
        self.svn_checker = Mod_svncheck.SvnChecker(*args)

    def run(self):
        while True:
            self.thread_lock.acquire()
            # every sleep_time flush
            svn_changed = self.svn_checker.svn_changed()
            for cur_item in svn_changed:
                self.thread_queue.put((self.thread_name,cur_item[1],cur_item[2]),block=True)
            self.thread_lock.release()
            time.sleep(self.sleep_time)

