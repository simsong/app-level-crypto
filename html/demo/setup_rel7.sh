#!/bin/bash
#
# setup 
cp /etc/yum.conf /etc/yum.conf.DIST
sed < /etc/yum.conf.DIST 's/exclude=/#exclude=' > /tmp/yum.conf
sudo yum -y install gcc 
sudo yum -y install emacs git httpd python34 python34-setuptools python34-devel
sudo yum -y install mariadb
sudo yum -y install mariadb-server
sudo yum -y install mariadb-devel
sudo easy_install-3.4 pip
sudo pip3.4 install ipython
sudo pip3.4 install python-jose rsa
sudo pip3.4 install mysqlclient

# make sure firewall is open
firewall-cmd --add-service=http               2>&1 | grep -v 'Warning: ALREADY_ENABLED'
firewall-cmd --permanent --add-service=http   2>&1 | grep -v 'Warning: ALREADY_ENABLED'
firewall-cmd --add-service=https              2>&1 | grep -v 'Warning: ALREADY_ENABLED'
firewall-cmd --permanent --add-service=https  2>&1 | grep -v 'Warning: ALREADY_ENABLED'

if test ! -d /var/www/html/demo ; then
  mkdir /var/www/html/demo
  chown $USER /var/www/html/demo
  ln -s /var/www/html/demo
fi

# Make sure .cgi is enabled in httpd.conf
CONF=/etc/httpd/conf/httpd.conf
sed 's/#AddHandler cgi-script .cgi/AddHandler cgi-script .cgi/' < $CONF \|
sed 's/Options Indexes FollowSymLinks$/Options Indexes FollowSymLinks ExecCGI' > $CONF.new
mv -f $CONF $CONF.dist
mv $CONF.new $CONF
apachectl graceful
