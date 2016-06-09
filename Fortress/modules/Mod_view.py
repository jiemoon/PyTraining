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
import getpass
import pprint
from sqlalchemy import and_
from modules import Mod_commutils
from modules import Mod_sshcontrol
from Mod_sqlalchemy import Base,SshHost,HostUser,HostGroup,FortressAccount,AuditLog


def check_params(func):
    def decorator(sql_engine,sqlsession,args):
        if len(args) == 2:
            option = args[0]
            yamlfs = os.path.abspath(args[1])
            if option == '-f' and os.path.exists(yamlfs):
                # for succ action
                exit_msg = 'start load yaml %s for %s.' % (yamlfs,func.__name__)
                Mod_commutils.exit_print(exit_msg,'notice',False)
                func(sql_engine,sqlsession,args)
            else:
                exit_msg = 'no yaml is specified, please special.'
                Mod_commutils.exit_print(exit_msg,'errors',True)
        else:
            exit_msg = 'invalid number of the parameter.'
            Mod_commutils.exit_print(exit_msg,'errors',True)
    return decorator


def initdatabase(sql_engine,sqlsession,args):
    """Create database table structure.
    
    :param: sql_engine: sql engine  for called
    :param: sqlsession: sql session for execute sql command
    :param: args: some args
    :return: None
    """
    Base.metadata.create_all(sql_engine)


def fortress_auth(sql_engine,sqlsession,args):
    count = 3
    flags = False
    while count > 0:
        user_name = raw_input('username: ').strip()
        user_pass = getpass.getpass('userpass: ').strip()

        query_usr = sqlsession.query(FortressAccount).filter(and_(FortressAccount.username == user_name,
                                                                  FortressAccount.password == user_pass)).first()
        if query_usr:
            flags = True
            break
        count -= 1
    if flags:
        return query_usr
    else:
        exit_msg = 'three times wrong username or userpass, exit.'
        Mod_commutils.exit_print(exit_msg,'errors',True)


def sta_sessions(sql_engine,sqlsession,args):
    """Start ssh session with paramiko.
    
    :param: sql_engine: sql engine  for called
    :param: sqlsession: sql session for execute sql command
    :param: args: some args
    :return: None
    """
    user_choice = {
        'hostgrup': {},
        'hostuser': {},
    }
    fortress_user = fortress_auth(sql_engine,sqlsession,args)
    print 'auth success.'
    for cur_index,cur_group in enumerate(fortress_user.hostgroups):
        user_choice['hostgrup'].update({cur_index:cur_group})
        print '%s. %s' % (cur_index,cur_group.groupname)
    while True:
        choice = raw_input('group_id: ').strip()
        if choice.isdigit():
            choice = int(choice)
        if not user_choice['hostgrup'].has_key(choice):
            exit_msg = 'invalid choice number, try again.'
            Mod_commutils.exit_print(exit_msg,'notice',False)
            continue
        else:
            break
    for cur_index,cur_hosts in enumerate(user_choice['hostgrup'][choice].hostusers):
        ssh_host = sqlsession.query(SshHost).filter(SshHost.id == cur_hosts.sshhost_id).first()
        if not user_choice['hostuser'].has_key(cur_index):
            user_choice['hostuser'].update({cur_index: {}})
        user_choice['hostuser'][cur_index].update({
            'haddress': ssh_host.haddress,
            'hostname': ssh_host.hostname,
            'hostport': ssh_host.hostport,
            'username': cur_hosts.username,
            'password': cur_hosts.password,
            'authtype': cur_hosts.authtype,
        })
        print '%s. %s' % (cur_index,ssh_host.haddress)
    while True:
        choice = raw_input('hosts_id: ').strip()
        if choice.isdigit():
            choice = int(choice)
        if not user_choice['hostuser'].has_key(choice):
            exit_msg = 'invalid choice number, try again.'
            Mod_commutils.exit_print(exit_msg,'notice',False)
            continue
        else:
            break
    pprint.pprint(user_choice['hostuser'][choice])
    # 零时密码验证,密码验证调用另一个函数
    Mod_sshcontrol.ssh_authpass_login(user_choice['hostuser'][choice]['haddress'],
                                      user_choice['hostuser'][choice]['hostport'],
                                      user_choice['hostuser'][choice]['username'],
                                      user_choice['hostuser'][choice]['password'],)

@check_params
def ssh_host_add(sql_engine,sqlsession,args):
    """Create host.
    
    hostname
    haddress
    hostport
    
    :param: sql_engine: sql engine  for called
    :param: sqlsession: sql session for execute sql command
    :param: args: some args
    :return: None
    """
    host_list = []
    yaml_file = os.path.abspath(args[-1])
    parse_res = Mod_commutils.load_yamls(yaml_file)
    for cur_key,cur_val in parse_res.iteritems():
        print  cur_key,cur_val
        cur_sshhost = SshHost(hostname=cur_val['name'],haddress=cur_val['host'],hostport=cur_val['port'])
        host_list.append(cur_sshhost)
    # add session and execute
    sqlsession.add_all(host_list)
    sqlsession.commit()


@check_params
def fts_user_add(sql_engine,sqlsession,args):
    """Create fortress login account.
    
    username
    password
    
    :param: sql_engine: sql engine  for called
    :param: sqlsession: sql session for execute sql command
    :param: args: some args
    :return: None
    """
    user_list = []
    yaml_file = os.path.abspath(args[-1])
    parse_res = Mod_commutils.load_yamls(yaml_file)
    for cur_key,cur_val in parse_res.iteritems():
        print cur_key,cur_val
        cur_ftsuser = FortressAccount(username=cur_val['user'],password=cur_val['pass'])
        user_list.append(cur_ftsuser)
    # add session and execute
    sqlsession.add_all(user_list)
    sqlsession.commit()


@check_params
def ssh_user_add(sql_engine,sqlsession,args):
    """Create ssh account.
    
    sshhost_id
    authtype
    username
    password
    
    :param: sql_engine: sql engine  for called
    :param: sqlsession: sql session for execute sql command
    :param: args: some args
    :return: None
    """
    user_list = []
    yaml_file = os.path.abspath(args[-1])
    parse_res = Mod_commutils.load_yamls(yaml_file)
    for cur_key,cur_val in parse_res.iteritems():
        # print  cur_key,cur_val
        username = cur_val['user']
        authtype = cur_val['auth']
        password = cur_val['pass']
        if cur_val.has_key('grup'):
            hostgroups = sqlsession.query(HostGroup).filter(HostGroup.groupname.in_(cur_val.get('grup'))).all()
            print hostgroups
            if cur_val.has_key('host'):
                for cur_host in cur_val.get('host'):
                    cur_sshhost = sqlsession.query(SshHost).filter_by(hostname=cur_host).first()
                    cur_sshuser = HostUser(sshhost_id=int(cur_sshhost.id),authtype=authtype,username=username,password=password)
                    cur_sshuser.hostgroups = hostgroups
                    user_list.append(cur_sshuser)
    # add session and execute
    sqlsession.add_all(user_list)
    sqlsession.commit()


@check_params
def ssh_grup_add(sql_engine,sqlsession,args):
    """Create server group.
    
    groupname
    
    :param: sql_engine: sql engine  for called
    :param: sqlsession: sql session for execute sql command
    :param: args: some args
    :return: None
    """
    grup_list = []
    yaml_file = os.path.abspath(args[-1])
    parse_res = Mod_commutils.load_yamls(yaml_file)
    for cur_key,cur_val in parse_res.iteritems():
        print cur_key,cur_val
        cur_sshgrup = HostGroup(groupname=cur_val['name'])
        # 关联主机的账户
        if cur_val.has_key('host'):
            hostusers = sqlsession.query(HostUser).filter(SshHost.hostname.in_(cur_val.get('host'))).all()
            cur_sshgrup.hostusers = hostusers
        # 关联堡垒机账户
        if cur_val.has_key('user'):
            fortressaccounts = sqlsession.query(FortressAccount).filter(FortressAccount.username.in_(cur_val.get('user'))).all()
            cur_sshgrup.fortressaccounts = fortressaccounts
        grup_list.append(cur_sshgrup)
    # add session and execute
    sqlsession.add_all(grup_list)
    sqlsession.commit()
