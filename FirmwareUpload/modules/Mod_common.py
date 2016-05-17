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
import yaml
import pprint
import logging


def exit_print(exit_msg,level='notice',is_exit='False'):
    """Is exit with print?
    
    :param exit_msg: exit message
    :param level: exit level, notice/errors
    :param is_exit: bool, true/false
    
    :return: None
    """
    exit_message = 'found %s: %s' % (level,exit_msg)
    pprint.pprint(exit_message)
    if is_exit:
        sys.exit()


def yaml_parse(yaml_file):
    """Parse yaml file to python struct.
    
    :param yaml_file: yaml file absolute path
    :return: dict
    """
    if not os.path.exists(yaml_file):
        exit_message = 'yaml file %s not exists, exit.' % (yaml_file)
        exit_print(exit_message,'errors',True)
    with open(yaml_file,'r+b') as rhandler:
        try:
            res_dict = yaml.load(rhandler)
        except Exception,e:
            exit_print(e,'errors',True)
    return res_dict


class Logger(object):
    def __init__(self,log_name,log_file):
        self.__logger = logging.getLogger(log_name)
        self.__handler = logging.handlers.RotatingFileHandler(filename=log_file,mode='a',maxBytes=100 * 1024,backupCount=5)
        self.__formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)s]')
        self.__handler.setFormatter(self.__formater)
        self.__logger.addHandler(self.__handler)
        # 默认日志级别设置,self.logger中超出默认日志级别才会被记录
        self.__logger.setLevel(logging.DEBUG)

    def logger(self,msg,level='info'):
        """RotatingFileHandler Logger message.
        
        :param level: debug,info,warning,error,critical
        :param msg: message.
        :return: None
        """
        getattr(self.__logger,level)(msg)


def daemonize(stdin=os.devnull,stdout=os.devnull,stderr=os.devnull):
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
    except OSError,e:
        exit_print(e,'errors',True)

    # change working space
    # os.chdir('/')
    os.umask(0)
    os.setsid()

    # fork again.
    try:
        nxt_pid = os.fork()
        if nxt_pid > 0:
            sys.exit(0)

    except OSError,e:
        exit_print(e,'errors',True)

    # flush stdin, stdout, stderr
    for f in (sys.stdin,sys.stdout,sys.stderr):
        f.flush()

    # redirect stdin, stdout, stderr to other file
    f_stdin = open(stdin,'r')
    # f_stdout = open(stdout, 'a+')
    f_stderr = open(stderr,'a+',0)
    os.dup2(f_stdin.fileno(),sys.stdin.fileno())
    # os.dup2(f_stdout.fileno(), sys.stdout.fileno())
    os.dup2(f_stderr.fileno(),sys.stderr.fileno())


def pid_writting(daemon_pid,pid_file='/var/run/collectd.pid'):
    """Write pid to pid file

    :param daemon_pid: daemon pid
    :param pid_file: pid file, default /var/run/collectd.pid
    :return:
    """
    with open(pid_file,'w') as whandler:
        whandler.write(str(daemon_pid))
