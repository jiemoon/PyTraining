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
import redis
import pprint
import threading
from pylsy import pylsytable


def exit_print(message, level='notice', is_exit=False):
    """Is exit with print ?

    :param message: exit or print message.
    :param level: notice or errors.
    :param is_exit: bool
    :return: None
    """
    exit_msg = 'found %s: %s' % (level, message)
    if is_exit:
        sys.exit(exit_msg)
    else:
        print exit_msg


def draw_asciitab(area_name, data_source):
    """Draw ascii table with data source.

    :param data_source: dict data
    :return: None
    """
    headers = ['ServerIP', 'ServerPort',
               'ServerCpu', 'ServerMem',
               'ServerFlow', 'ServerRole',
               'AreaName', 'Status',
               'RunSeconds',
               ]
               #'UpdateDate', 'VendorName'
    pytab = pylsytable(headers)
    for cur_dict in data_source:
        for cur_head in headers:
            pytab.append_data(cur_head, cur_dict.get(cur_head, None))
    print pytab


class MultiReader(threading.Thread):
    def __init__(self, thread_lock, redis_area, redis_key, server_ips):
        self.redis_key = redis_key
        self.redis_area = redis_area
        self.server_ips = server_ips
        self.thread_lock = thread_lock
        super(MultiReader, self).__init__()

    def run(self):
        # thread direct data is not shared by default
        res_list = []
        self.thread_lock.acquire()
        for cur_ip in self.server_ips:
            collectd_key = '_'.join(['Collectd', cur_ip])
            srvtypes_key = self.redis_key.rstrip('Map')
            srvtypes_key = '_'.join([srvtypes_key, cur_ip])
            rds_report.redis_pipeadd(self.redis_area, srvtypes_key)
            rds_report.redis_pipeadd(self.redis_area, collectd_key)
        exec_res = rds_report.redis_execute(self.redis_area)
        for i in xrange(0, len(exec_res), 2):
            exec_res[i].update(exec_res[i+1])
            res_list.append(exec_res[i])
        print '%s %s => (total: %s)' % (self.redis_area, self.redis_key, len(res_list))
        draw_asciitab(self.redis_area, res_list)
        # pprint.pprint(res_list)
        self.thread_lock.release()


class RedisReport(object):
    # create redis connection pool
    def __init__(self, port, redis_hosts, redis_keys):
        self.port = port
        self.redis_conns = {}
        self.redis_keys = redis_keys
        self.redis_hosts = redis_hosts
        for redis_area, redis_host in self.redis_hosts.iteritems():
            __conns_pool = redis.ConnectionPool()
            __redis_conn = redis.Redis(host=redis_host,
                                       port=self.port,
                                       connection_pool=__conns_pool)
            __redis_pipe = __redis_conn.pipeline()
            self.redis_conns[redis_area] = __redis_pipe

    def redis_pipeadd(self, area, redis_key):
        self.redis_conns[area].hgetall(redis_key)

    def redis_execute(self, area):
        exec_res = self.redis_conns[area].execute()
        return exec_res


def show_usage(excute_file):
    versions = os.linesep.join([
        'redis-report version 0.0.1',
        'Copyright (C) 2016-%s by limanman and others.',
        'Web site: http://my.oschina.net/pydevops/'
    ])
    allusage = '''\
    Usage: %s <area-like> [redis-key-like]
    area-like     : area name, China_China
                               Asia_Oceania
                               Europe_Africa
                               America_Antarctica
    redis-key-like: redis key, DnsServerMap
                               NatServerMap
                               StatusHelperMap
                               ProxyServerMap


    example:
        %s china, will print domestic all server.
        %s china nat, will print domestic natserver.
    ''' % (excute_file, excute_file, excute_file)
    exit_msg = os.linesep.join([versions, allusage])
    sys.exit(exit_msg)


def main(argv):
    excute_file = None
    excute_area = None
    excute_keys = None
    thread_lock = threading.Lock()

    if argv[0:]:
        excute_file = os.path.basename(argv[0])
    if argv[1:]:
        if argv[1] in redis_host:
            excute_area = argv[1]
    else:
        show_usage(excute_file)
    if argv[2:]:
        if argv[2] in redis_keys:
            excute_keys = argv[2]
    else:
        pass
    thread_list = []
    # multi thread read from redis and handler
    if not excute_keys:
        for cur_redis_key in redis_keys:
            rds_report.redis_pipeadd(excute_area, cur_redis_key)
    else:
        rds_report.redis_pipeadd(excute_area, excute_keys)
    srv_ips = rds_report.redis_execute(excute_area)

    for i in xrange(len(srv_ips)):
        cur_thread = MultiReader(thread_lock, excute_area,
                                 excute_keys or redis_keys[i],
                                 srv_ips[i].iterkeys())
        thread_list.append(cur_thread)
        cur_thread.start()
    for cur_thread in thread_list:
        cur_thread.join()

if __name__ == '__main__':
    redis_host = {
        'China_China': '123.59.14.61',
        'Asia_Oceania': '54.254.159.106',
        'Europe_Africa': '54.72.86.70',
        'America_Antarctica': '54.67.91.181',
    }
    redis_port = 5123
    redis_keys = ['DnsServerMap', 'NatServerMap', 'StatusHelperMap', 'ProxyServerMap']
    rds_report = RedisReport(redis_port, redis_host, redis_keys)
    # main func called.
    main(sys.argv)
