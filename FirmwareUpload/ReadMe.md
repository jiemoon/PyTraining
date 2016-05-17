# python version
    2.6.6

# environmental install:
    yum -y install epel-release
    yum -y install subversion subversion-devel pysvn
    yum -y install python python-devel python-setuptools
    easy_install wget

# daemon control
    mv scripts/firmwareupload /etc/init.d/
    chmod +x /etc/init.d/firmwareupload
    /etc/init.d/firmwareupload restart