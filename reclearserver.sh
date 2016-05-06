#!/usr/bin/env bash

# remove zabbix
/etc/init.d/zabbix-agent stop
yum -y remove zabbix*
rm -rf /etc/zabbix

# install rpm
yum -y install unzip

# replace repo
cd /etc/yum.repos.d
rm -rf *
wget http://52.69.247.24:8080/app/srv_tools/yum.repos.d.zip
unzip -o yum.repos.d.zip
yum -y remove epel-release
yum -y install epel-release
rm -rf yum.repos.d.zip

# open ip forward.
sed -i 's/\(net.ipv4.ip_forward = \).*/\11/g' /etc/sysctl.conf
sysctl -p
sysctl -p

# remove dir
rm -rf  /xm-scripts /AuthService  /p2p_svn /OEMManager
rm -rf /root/OEMManager /root/StatusHelper