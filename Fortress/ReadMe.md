# python version
> 2.7.x

# environmental install:
> yum -y install python python-devel python-setuptools
> pip install paramiko

# for more help
> python main.py

# sequential execution
##初始数据
> python main.py initdatabase
##创建主机
> python main.py ssh_host_add -f srcs\ssh_host_add.yaml
##堡垒用户
> python main.py fts_user_add -f srcs\fts_user_add.yaml
##登录用户
> python main.py ssh_grup_add -f srcs\ssh_grup_add.yaml
##创建属组
> python main.py ssh_user_add -f srcs\ssh_user_add.yaml

# start session
> python main.py sta_sessions

# 未完待续
> 1.支持多线程/多进程命令执行
> 2.支持多线程/多进程文件分发
> 3.支持密钥或密码验证(ChoiceType好像有点儿问题,再看看)
> 4.目标服务器交互日志审计记录,满足指定条数再记录,记录中正则过滤特殊字符,参考jumpserver
> ............................................................