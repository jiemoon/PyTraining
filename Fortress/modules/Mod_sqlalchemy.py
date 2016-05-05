#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose:
#
"""
import pprint
# 创建基类
from sqlalchemy.ext.declarative import declarative_base
# 创建会话类
from sqlalchemy.orm import sessionmaker, aliased, relationship, backref
# 创建表结构
from sqlalchemy import (Text, Integer, String, Table, DateTime ,ForeignKey,
                        Column, create_engine, func, UniqueConstraint)
# 增加列类型
from sqlalchemy_utils import ChoiceType, PasswordType

Base = declarative_base()

# hostuser2hostgroup - 中间表
hostuser2hostgroup = Table('hostuser2hostgroup', Base.metadata,
                           Column('hostuser_id', ForeignKey('hostuser.id'),
                                  primary_key=True),
                           Column('hostgroup_id', ForeignKey('hostgroup.id'),
                                  primary_key=True),
                           )
# fortress2hostgroup - 中间表
fortress2hostgroup = Table('fortress2hostgroup', Base.metadata,
                           Column('hostgroup_id',
                                  ForeignKey('hostgroup.id'),
                                  primary_key=True),
                           Column('FortressAccount_id',
                                  ForeignKey('fortressaccount.id'),
                                  primary_key=True),
                           )
"""
附加需求: 分配堡垒机指定账户 - 服务器.账户 (给特定用户零时使用), 略 M-M
"""

# sshhost - 主机表
class SshHost(Base):
    __tablename__ = 'sshhost'
    id = Column(Integer,
                unique=True,
                nullable=False,
                autoincrement=True,
                primary_key=True)
    hostname = Column(String(64),
                      unique=True,
                      nullable=False)
    haddress = Column(String(128),
                      unique=True,
                      nullable=False)
    hostport = Column(Integer,
                      nullable=False)
    # 规范打印
    def __repr__(self):
        return ('<SshHost(id: %s hostname: %s haddress: %s password: %s'
                'hostport: %s auth_key: %s)>') % ( self.id, self.hostname,
                                                   self.haddress, self.hostport,
                                                   self.password, self.auth_key)

# hostuser - 主机账户表
class HostUser(Base):
    __tablename__ = 'hostuser'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sshhost_id = Column(Integer, ForeignKey('sshhost.id'))

    # 验证方式
    Authtype = [
        (u'ssh-pass', u'ssh-auth-pass'),
        (u'ssh-keys', u'ssh-auth_keys'),
    ]
    authtype = Column(ChoiceType(Authtype))
    username = Column(String(64),
                      unique=True,
                      nullable=False)
    password = Column(String(64),
                      nullable=True)
    # 保证主机,账户联合唯一,防止记录重复
    __table_args__ = (UniqueConstraint('sshhost_id', 'username',
                                       name='sshhost_username_uc'),)

# hostgroup - 主机组表
class HostGroup(Base):
    __tablename__ = 'hostgroup'
    id = Column(Integer,
                unique=True,
                nullable=False,
                autoincrement=True,
                primary_key=True)
    groupname = Column(String(64),
                       unique=True,
                       nullable=False)
    # 双向引用,获取主机组内的主机+账户
    hostusers = relationship('HostUser', secondary=hostuser2hostgroup,
                             backref='hostgroups')
    # 规范打印
    def __repr__(self):
        return '<HostGroup(id: %s groupname: %s)>' % (self.id, self.groupname)


# fortressaccount - 堡垒进机账户表
class FortressAccount(Base):
    __tablename__ = 'fortressaccount'
    id = Column(Integer,
                unique=True,
                nullable=True,
                autoincrement=True,
                primary_key=True)
    username = Column(String(64),
                      unique=True,
                      nullable=False)
    password = Column(String(64),
                      nullable=False)
    # 双向引用,获取用户所属主机组
    hostgroups = relationship('HostGroup', secondary=fortress2hostgroup,
                              backref='fortressaccounts')

    # 规范打印
    def __repr__(self):
        return ('<FortressAccount(username: %s password: %s') % (self.username,
                                                                 self.password,
                                                                 self.auth_key)

# auditlogs - 日志审计表
class AuditLog(Base):
    __tablename__ = 'auditlogs'
    id = Column(Integer, primary_key=True)
    # 关联的SSH账户
    hostuser_id = Column(Integer, ForeignKey('hostuser.id'))
    # 关联的堡垒账户
    fortressaccount_id = Column(Integer, ForeignKey('fortressaccount.id'))

    # 操作类型
    ActionType = [
        (u'cmd', u'CMD'),
        (u'login', u'Login'),
        (u'logout', u'Logout'),
        (u'getfile', u'GetFile'),
        (u'sendfile', u'SendFile'),
        (u'exception', u'Exception'),
    ]
    actiontype = Column(ChoiceType(ActionType))
    actcontent = Column(String(255))
    actiondate = Column(DateTime)

    # 关联主机用户表和堡垒机账户表,加入精确审计日志
    hostuser = relationship('HostUser')
    fortressaccount = relationship('FortressAccount')

    # 规范打印
    def __repr__(self):
        return ('<AuditLog(fortressaccount_id: %s hostuser_id: %s'
                'actiondate: %s actiontype %s actcontent: %s)>') % (
                    self.fortressaccount_id, self.hostuser_id,
                    self.actiondate, self.actiontype, self.actcontent,
                )