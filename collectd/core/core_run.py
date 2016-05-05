#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
"""
import time
from modules import RedisPool
from modules import CommUtils
from modules import ServiceGet


def parse_motd(conf='/etc/motd'):
    """Parse motd configure file.

    :param conf: conf file.
    :return: dict
    """
    conf_dict = {}
    try:
        with open(conf, 'r') as rhandler:
            for cur_line in rhandler:
                key, val = cur_line.split(':', 1)
                key = key.strip()
                val = val.strip()
                conf_dict.update({key: val})
    except Exception, e:
        CommUtils.exit_print(e, 'errors', True)
    return conf_dict


def main(redis_write_rate, redis_key_expire):
    """ Write basic server info to redis.

    :param redis_write_rate: redis write interval
    :param redis_key_expire: redis key expire time
    :return: None
    """
    conf_dict = parse_motd()
    # pprint.pprint(conf_dict)
    if not conf_dict.get('DataIP', None) or not conf_dict.get('Wan_IP', None):
        exit_msg = 'could not found defined ip, check /etc/motd define.'
        CommUtils.exit_print(exit_msg, 'errors', True)
    redis_conn = RedisPool.Redis(conf_dict['DataIP'])

    # later changed to multi thread
    while True:
        # write to redis
        cpu_str = ServiceGet.get_cpu_status(1)
        mem_str = ServiceGet.get_memory_status()
        net_str = ServiceGet.get_network_status(1)

        redis_key = 'Collectd_%s' % (conf_dict['Wan_IP'])
        redis_fields = ['ServerCpu', 'ServerMem', 'ServerFlow']
        redis_values = [cpu_str, mem_str, net_str[1]]
        # print 'write => redis_values: %s' % (redis_values)
        redis_conn.redis_hset(redis_key, redis_fields, redis_values, redis_key_expire)

        time.sleep(redis_write_rate)


