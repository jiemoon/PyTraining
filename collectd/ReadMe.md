# python version
    2.6.6

# environmental install:
    yum -y install python python-devel python-setuptools
    easy_install redis psutil


# daemon control
    mv scripts/collectd /etc/init.d/
    chmod +x /etc/init.d/collectd