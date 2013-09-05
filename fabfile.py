from fabric.api import *

## 
## Proof of concept script for redmine 1.4.7 on CentOS / RHEL
##
	
def passenger():
	# Installing the needed repos
	run("rpm --import http://passenger.stealthymonkeys.com/RPM-GPG-KEY-stealthymonkeys.asc")
	run("yum install -y http://passenger.stealthymonkeys.com/rhel/6/passenger-release.noarch.rpm")
	run("rpm --import http://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-6")
	run("yum install -y http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm")
	# Installing Passenger
	run("yum install -y httpd apr-util-devel apr-devel httpd-devel zlib-devel openssl-devel curl-devel gcc-c++")
	run("yum install -y mod_passenger")
	run("passenger-install-apache2-module -a")		
	run("chkconfig httpd on")
	run("service httpd restart")
	#chould probably disable repos after this point to be somewhat safer
	
	
def redmine():
	#DEFINE INSTALL DIR No trailing slash
	install_dir = '/var/www/'
	# Let's install some deps
	run("yum install -y mercurial mysql-server mysql-devel")
	#cononfiguring our mysql server
	run("chkconfig mysqld on")
	put("create_redmine.sql", "/tmp/create_redmine.sql")
	run("mysql -u root < /tmp/create_redmine.sql")
	#Let's get the stable redmine release we are using
	run("hg clone --updaterev 1.4-stable https://bitbucket.org/redmine/redmine-all %s/redmine-1.4.7" % install_dir)
	run("ln -s %s/redmine-1.4.7 /var/www/redmine" % install_dir)
	run("cd /var/www/redmine ")
	run("chown -R apache:apache %s/redmine/{files,log,tmp}" % install_dir)
	#Let's get those gems running
	run("gem install bundler")	
	run("bundle install --without development test rmagick sqlite postgresql")
	


def migration():
	run("")
	run("")
