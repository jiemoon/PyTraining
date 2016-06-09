#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://my.oschina.net/pydevops/
# Purpose: just for pass or keys auth
#
"""
import base64
from binascii import hexlify
import getpass
import os
import socket
import sys
import time
import traceback
from paramiko.py3compat import input

import paramiko
try:
    import Mod_interactive
except ImportError:
    from . import Mod_interactive


def agent_auth(transport,username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent.
    """

    agent = paramiko.Agent()
    agent_keys = agent.get_keys()
    if len(agent_keys) == 0:
        return

    for key in agent_keys:
        print('Trying ssh-agent key %s' % hexlify(key.get_fingerprint()))
        try:
            transport.auth_publickey(username,key)
            print('... success!')
            return
        except paramiko.SSHException:
            print('... nope.')


def manual_auth(username,hostname):
    default_auth = 'p'
    auth = input('Auth by (p)assword, (r)sa key, or (d)ss key? [%s] ' % default_auth)
    if len(auth) == 0:
        auth = default_auth

    if auth == 'r':
        default_path = os.path.join(os.environ['HOME'],'.ssh','id_rsa')
        path = input('RSA key [%s]: ' % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.RSAKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass('RSA key password: ')
            key = paramiko.RSAKey.from_private_key_file(path,password)
        t.auth_publickey(username,key)
    elif auth == 'd':
        default_path = os.path.join(os.environ['HOME'],'.ssh','id_dsa')
        path = input('DSS key [%s]: ' % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.DSSKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass('DSS key password: ')
            key = paramiko.DSSKey.from_private_key_file(path,password)
        t.auth_publickey(username,key)
    else:
        pw = getpass.getpass('Password for %s@%s: ' % (username,hostname))
        t.auth_password(username,pw)


def ssh_authkeys_login(haddress,hostport,username):
    # now connect
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((haddress,hostport))
    except Exception as e:
        print('*** Connect failed: ' + str(e))
        traceback.print_exc()
        sys.exit(1)

    try:
        t = paramiko.Transport(sock)
        try:
            t.start_client()
        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            sys.exit(1)

        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                print('*** Unable to open host keys file')
                keys = {}

        # check server's host key -- this is important.
        key = t.get_remote_server_key()
        if haddress not in keys:
            print('*** WARNING: Unknown host key!')
        elif key.get_name() not in keys[haddress]:
            print('*** WARNING: Unknown host key!')
        elif keys[haddress][key.get_name()] != key:
            print('*** WARNING: Host key has changed!!!')
            sys.exit(1)
        else:
            print('*** Host key OK.')

        # get username
        if username == '':
            default_username = getpass.getuser()
            username = input('Username [%s]: ' % default_username)
            if len(username) == 0:
                username = default_username

        agent_auth(t,username)
        if not t.is_authenticated():
            manual_auth(username,haddress)
        if not t.is_authenticated():
            print('*** Authentication failed. :(')
            t.close()
            sys.exit(1)

        chan = t.open_session()
        chan.get_pty()
        chan.invoke_shell()
        print('*** Here we go!\n')
        Mod_interactive.interactive_shell(chan)
        chan.close()
        t.close()

    except Exception as e:
        print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)


def ssh_authpass_login(haddress,hostport,username,password):
    # enable GSS-API / SSPI authentication
    UseGSSAPI = False
    DoGSSAPIKeyExchange = False

    # now, connect and use paramiko Client to negotiate SSH2 across the connection
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        print('*** Connecting...')
        if not UseGSSAPI or (not UseGSSAPI and not DoGSSAPIKeyExchange):
            client.connect(haddress,hostport,username,password)
        else:
            # SSPI works only with the FQDN of the target host
            hostname = socket.getfqdn(haddress)
            try:
                client.connect(haddress,hostport,username,gss_auth=UseGSSAPI,
                               gss_kex=DoGSSAPIKeyExchange)
            except Exception:
                password = getpass.getpass('Password for %s@%s: ' % (username,haddress))
                client.connect(hostname,hostport,username,password)
        # interactive shell
        chan = client.invoke_shell()
        print(repr(client.get_transport()))
        print('*** Here we go!\n')
        Mod_interactive.interactive_shell(chan)
        chan.close()
        client.close()
    except Exception as e:
        print('*** Caught exception: %s: %s' % (e.__class__,e))
        traceback.print_exc()
        try:
            client.close()
        except:
            pass
        sys.exit(1)
