tahoe
=====
stuff

DB:
sudo /Library/StartupItems/MySQLCOM/MySQLCOM start
alias mysql=/usr/local/mysql/bin/mysql
alias mysqladmin=/usr/local/mysql/bin/mysqladmin

sudo pip install mysql-connector-python --allow-external mysql-connector-python

mysql -u root <db/create.sql 


testing:
nosetests -s -v test/test_lacrossealerts.py:TestLaCrosseAlerts.test_login
nosetests -s -v test/test_db.py