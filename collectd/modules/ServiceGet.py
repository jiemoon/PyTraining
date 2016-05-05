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
import psutil
import operator


def get_cpu_status(interval=1):
    """Get local cpu status.

    :param interval: called interval, default 1
    :return:
    """
    cup_percent = psutil.cpu_percent(interval, False)
    return '%s%%' % (cup_percent)


def __bytes2human(n):
    """Convert bytes to human.

    :param n: bytes
    :return:
    """
    symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols, start=1):
        prefix[s] = 1 << i*10
    for s in reversed(symbols):
        value = float(n) / prefix[s]
        if value > 1:
            return '%.2f%s' % (value, s)
    return '%.2fB' % (n)


def get_memory_status():
    phy_mem = psutil.virtual_memory()
    freemem = int(phy_mem.total) - int(phy_mem.used)
    return __bytes2human(freemem)


def __dev2flow():
    for cur_line in open('/proc/net/dev', 'r'):
        pass
    interface, totaldata = cur_line.split(':')
    (recv_bytes, recv_packets, recv_errs, recv_drop,
     recv_fifo, recv_frame, recv_compressed, recv_multicast,
     send_bytes, send_packets, send_errs, send_drop, send_fifo,
     send_colls, send_carrier, send_compressed) = totaldata.split()

    recv_bytes = int(recv_bytes)*8
    send_bytes = int(send_bytes)*8
    return interface.strip(), recv_bytes, send_bytes


def get_network_status(interval=1):
    net_res = {
        'in_flow': [],
        'ou_flow': [],
    }
    for _ in xrange(2):
        curflow = __dev2flow()
        net_res['in_flow'].append(curflow[1])
        net_res['ou_flow'].append(curflow[2])
        time.sleep(interval)
    in_flow = __bytes2human(abs(operator.sub(*net_res['in_flow'])))
    ou_flow = __bytes2human(abs(operator.sub(*net_res['ou_flow'])))
    in_flow = '%s/s' % (in_flow)
    ou_flow = '%s/s' % (ou_flow)

    return curflow[0], in_flow, ou_flow



