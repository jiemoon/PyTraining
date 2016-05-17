# -*- coding: utf-8 -*-
#
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
#
import os
import re
import time
import pysvn
import urllib
import pprint
import datetime
import urlparse
from conf import Conf_summary


class SvnChecker(object):
    def __init__(self,svn_username,svn_password,svn_day,svn_url,svn_key):
        self.svn_day = svn_day
        self.svn_url = svn_url
        self.svn_key = svn_key

        self.svn_username = svn_username
        self.svn_password = svn_password

        self.svn_client = pysvn.Client()
        self.svn_client.set_default_username(self.svn_username)
        self.svn_client.set_default_password(self.svn_password)
        # 开启命令执行回显
        self.svn_client.callback_notify = self.__svn_debugbotify
        # 开启远程登录验证
        self.svn_client.callback_get_login = self.__svn_credentials

    @staticmethod
    def __svn_debugbotify(event_dict):
        pprint.pprint(event_dict)
    @staticmethod
    def __svn_credentials(realm,svn_user,svn_pass,svn_save):
        return True,None,None,False

    def svn_changed(self):
        """For multithread get svn changed and handler
        
        find few days before the current time, update the firmware.
        """
        change_files = []
        sta_timestamp = datetime.datetime.now() - datetime.timedelta(days=int(self.svn_day))
        sta_timestamp = time.mktime(sta_timestamp.timetuple())
        end_timestamp = time.time()
        revision_min = pysvn.Revision(pysvn.opt_revision_kind.date,sta_timestamp)
        revision_max = pysvn.Revision(pysvn.opt_revision_kind.date,end_timestamp)
        svn_summary = self.svn_client.diff_summarize(self.svn_url,revision_min,self.svn_url,revision_max)
        for cur_item in svn_summary:
            file_kind = pysvn.node_kind.file
            file_path = cur_item['path']
            node_kind = cur_item['node_kind']

            firmware_name = os.path.basename(file_path)
            if not self.svn_key in firmware_name:
                continue
            if firmware_name.startswith('upall_'):
                continue
            if not firmware_name.endswith('.bin'):
                continue
            if not file_kind == node_kind:
                continue

            svn_fullurl = urlparse.urljoin(self.svn_url,file_path)
            svn_matches = re.search(r'(.*/)(\d{4}-\d{1,2}-\d{1,2}[^/]+)(/.*)',svn_fullurl)
            if not svn_matches:
                message = 'could not match date with %s' % (svn_fullurl)
                Conf_summary.logg_dict[self.svn_key](message)
                continue
            svn_releasenote = urlparse.urljoin(svn_matches.group(1),'ReleaseNote')
            svn_fullurl = urllib.quote(svn_fullurl.encode('utf-8'),safe=':/')
            svn_releasenote = urllib.quote(svn_releasenote.encode('utf-8'),safe=':/')
            change_files.append((self.svn_key,svn_fullurl,svn_releasenote))
        return change_files


