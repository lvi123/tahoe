tahoe
=====
stuff

Git:
git config --global user.name lvi123
git config --global user.email lvi123@xxx.com
git config --global credential.helper store
#git config --global credential.helper osxkeychain

git clone https://github.com/lvi123/tahoe.git

MAC:
sudo /Library/StartupItems/MySQLCOM/MySQLCOM start
alias mysql=/usr/local/mysql/bin/mysql
alias mysqladmin=/usr/local/mysql/bin/mysqladmin

sudo pip install mysql-connector-python --allow-external mysql-connector-python

Ubuntu:
sudo apt-get install git
sudo apt-get install mysql-client mysql-server
sudo apt-get install python-pip 
sudo apt-get install python-nose

alias mysql=/usr/bin/mysql
alias mysqladmin=/usr/bin/mysqladmin  

sudo pip install mysql-connector-python --allow-external mysql-connector-python 

DB:
mysql -u root <db/create.sql 

Testing:
nosetests -s -v test/test_lacrossealerts.py:TestLaCrosseAlerts.test_login
nosetests -s -v test/test_db.py
