#!/bin/bash
############################################
#           �Ʒ�����������ű�         
#
#2013-12-16 by ����Զ���
#version:1.1
#ʹ�÷�����
#����./vmnetcheck.sh [eth0|eth1]
#
#����˵����
#��д����ʱ��Ĭ�ϼ����������eth1
# eth0  :����������� 
# eth1  :�����������
#������
#�ű���Ҫ��q���˳����޷�ʹ��ctrl+cֹͣ       
############################################
#v1.1:
#curr_conn_net()��������15�У���ֹ������Ļ


##ʹ�÷���
usage()
{
	echo -e "usage:\n$0 [eth0|eth1]"
	exit
}
##��ʾ����
show_net()
{
	recv1=$(cat /sys/class/net/${vm_interface}/statistics/rx_bytes)
	send1=$(cat /sys/class/net/${vm_interface}/statistics/tx_bytes)
	sleep 1
	recv2=$(cat /sys/class/net/${vm_interface}/statistics/rx_bytes)
	send2=$(cat /sys/class/net/${vm_interface}/statistics/tx_bytes)
	recv_Bps=$(($recv2-$recv1))
	send_Bps=$(($send2-$send1))
	recv_KBps=$(echo "${recv_Bps} 1024" |awk '{printf("%0.2f\n",$1/$2)}')
	send_KBps=$(echo "${send_Bps} 1024" |awk '{printf("%0.2f\n",$1/$2)}')
	recv_Mbps=$(echo "${recv_KBps} 1024 8" |awk '{printf("%0.2f\n",$1/$2*$3)}')
	send_Mbps=$(echo "${send_KBps} 1024 8" |awk '{printf("%0.2f\n",$1/$2*$3)}')
	echo -e "\033[5;1H����:${vm_interface}\t�����: ${recv_KBps} KB/s (${recv_Mbps} Mb/s) \t������: ${send_KBps} KB/s (${send_Mbps} Mb/s)"
}
##���ssh����״̬
check_sshd()
{
	sshd_port_tmp=$(grep -i ^port /etc/ssh/sshd_config|awk '{print $2}')
	sshd_port=${sshd_port_tmp:-22}
	sshd_root_state_tmp=$(grep ^PermitRootLogin /etc/ssh/sshd_config|tail -1|awk '{print $2}'|tr [A-Z] [a-z])
	sshd_root_state=${sshd_root_state_tmp:-yes}
	sshd_passwd_state_tmp=$(grep ^PasswordAuthentication /etc/ssh/sshd_config|tail -1|awk '{print $2}'|tr [A-Z] [a-z])
	sshd_passwd_state=${sshd_passwd_state_tmp:-yes}
	echo -e "\033[2;1Hssh�˿�Ϊ:"${sshd_port}
	echo -e "\033[2;60Hssh����root��½:${sshd_root_state}"
	echo -e "\033[2;120Hssh����������֤:${sshd_passwd_state}"
}
##���IP
check_ip()
{
	internal_ip=$(ifconfig |grep -A 1 eth0|grep inet|awk -F: '{print $2}'|awk '{print $1}')
	internat_ip=$(ifconfig |grep -A 1 eth1|grep inet|awk -F: '{print $2}'|awk '{print $1}')
	if [ -n "${internal_ip}" ];then
		echo -ne "\033[1;1H����IP:"${internal_ip}
	else
		echo -ne "\033[1;1H����IP:none"
	fi
	if [ -n "${internat_ip}" ];then
                echo -ne "\033[1;60H����IP:"${internat_ip}
        else
                echo -ne "\033[1;60H����IP:none"
        fi
	is_icmp=$(cat /proc/sys/net/ipv4/icmp_echo_ignore_all)
	if [ "${is_icmp}x" == "1"x ];then
	echo -ne "\033[1;120Hicmp:�ѽ�ping"
	fi
}
##netstat״̬
curr_conn_net()
{
	curr_conn_tcp=$(netstat -anp|grep ^tcp|grep -v :::|grep ESTABLISHED |sort -rn -k 3|awk '{print $1,"\t�����:",$2,"\t������:",$3,"\t  ����IP:",$4,"\t\tԶ��IP:",$5,"\tPID/����:",$NF}')
	if [ -n "${curr_conn_tcp}" ];then
		echo -e "\r\033[K${curr_conn_tcp}\n\n"|grep -v 132|head -15
	fi
	curr_conn_udp=$(netstat -anp|grep ^udp|grep -v ::|grep ESTABLISHED |sort -rn -k 3|awk '{print $1,"\t�����:",$2,"\t������:",$3,"\t  ����IP:",$4,"\t\tԶ��IP:",$5,"\tPID/����:",$NF}')
	if [ -n "$curr_conn_udp" ];then
		echo -ne "\r\033[K${curr_conn_udp}"|grep -v 132|head -15
	fi
}

##�ű��������
if [ $# -gt 1 ];then
	usage
elif [ $# -eq 0 ];then
	:
else
	if [ "$1"x != "eth0"x ] && [ "$1"x != "eth1"x ];then
	usage
	fi
fi
##�趨�������
vm_interface=${1:-eth1}
##�����ļ����
if [ ! -e /sys/class/net/${vm_interface} ];then
	echo "����:${vm_interface}�����ڣ����ʵ!"
	usage
	exit
fi
clear
##��q�˳�
stty intr q
echo -ne "\033[4;1H��\033[31mq\033[0m���˳�"
##��ʼִ��
check_sshd
check_ip

##ѭ����ʾ
while true
do
##������ʾ��
#echo -ne "\033[?25l"
show_net ${vm_interface}
curr_conn_net
#echo -e "\033[?25h"
done