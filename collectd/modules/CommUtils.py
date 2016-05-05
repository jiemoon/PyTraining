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
import time


def exit_print(message, logevel='notice', is_exit=False):
    """Print message at exit.

    :param message: message info.
    :param logevel: notice/errors.
    :param is_exit: is exit ?
    :return: None
    """
    exit_msg = 'found %s: %s' % (logevel, message)
    if is_exit:
        sys.exit(exit_msg)
    print exit_msg


def daemonize(stdin=os.devnull, stdout=os.devnull, stderr=os.devnull):
    """Fork current process as daemon process.

    :param stdin: stand input
    :param stdout: stand output
    :param stderr: stand stderr
    :return: None
    """
    # fork a pid
    try:
        cur_pid = os.fork()
        if cur_pid > 0:
            sys.exit(0)
    except OSError, e:
        exit_print(e, 'errors', True)

    # change working space
    os.chdir('/')
    os.umask(0)
    os.setsid()

    # fork again.
    try:
        nxt_pid = os.fork()
        if nxt_pid > 0:
            sys.exit(0)

    except OSError, e:
        exit_print(e, 'errors', True)

    # flush stdin, stdout, stderr
    for f in (sys.stdin, sys.stdout, sys.stderr):
        f.flush()

    # redirect stdin, stdout, stderr to other file
    f_stdin = open(stdin, 'r')
    # f_stdout = open(stdout, 'a+')
    f_stderr = open(stderr, 'a+', 0)
    os.dup2(f_stdin.fileno(), sys.stdin.fileno())
    # os.dup2(f_stdout.fileno(), sys.stdout.fileno())
    os.dup2(f_stderr.fileno(), sys.stderr.fileno())


def pid_writting(daemon_pid, pid_file='/var/run/collectd.pid'):
    """Write pid to pid file

    :param daemon_pid: daemon pid
    :param pid_file: pid file, default /var/run/collectd.pid
    :return:
    """
    with open(pid_file, 'w') as whandler:
        whandler.write(str(daemon_pid))