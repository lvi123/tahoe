import ConfigParser
import time
import unittest

import mysql.connector
from mysql.connector import errorcode

class TestDB(unittest.TestCase):
    
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('test/test.conf')

        self.db_config = {
            'user' : config.get('db', 'user'),
            'password' : config.get('db', 'password'),
            'host' : config.get('db', 'host'),
            'database' : config.get('db', 'database')
            }

        self.bogus_user = 'foo'
        self.bogus_password = 'bar'

        self.debug_serial = config.get('db', 'debug_serial')

        self.delete_obs = ('DELETE FROM obs where serial = %(serial)s')

        self.insert_obs = ('INSERT INTO obs '
                           '(serial, timestamp, temp, temp2, rh, lowbatt, linkquality) '
                           'VALUES (%(serial)s, FROM_UNIXTIME(%(timestamp)s), %(temp)s, %(temp2)s, %(rh)s, %(lowbatt)s, %(linkquality)s)')

    def testLogin(self):
        cnx = mysql.connector.connect(**self.db_config);
        cnx.close

    def testLoginFailWrongCredentials(self):
        try:
            cnx = mysql.connector.connect(user = self.bogus_user,
                                          password = self.bogus_password,
                                          host = self.db_config['host'],
                                          database = self.db_config['database'])
            self.fail("DB connection for user '%s' should have failed!" % self.bogus_user)
        except mysql.connector.Error as err:
            self.assertEqual(err.errno, errorcode.ER_ACCESS_DENIED_ERROR)
            print "DB connection for user '%s' failed as expected" % self.bogus_user

    def deleteDebugObs(self, cnx):
        cursor = cnx.cursor()
        cursor.execute(self.delete_obs, {'serial' : self.debug_serial})
        cnx.commit()

    def makeDebugObs(self, timestamp):
        obs = {
            'serial' : self.debug_serial,
            'timestamp' : timestamp,
            'temp' : '60',
            'temp2' : '70',
            'rh' : '50',
            'lowbatt' : 0,
            'linkquality' : 100
            }
        return obs

    def testInsert(self):
        cnx = mysql.connector.connect(**self.db_config);
        try:
            self.deleteDebugObs(cnx)
            cursor = cnx.cursor()
            timestamp = int(time.time())
            for i in range (0,500):
                obs_data = []
                for j in range (0,100):
                    obs_data.append(self.makeDebugObs(timestamp))
                    timestamp += 1
                cursor.executemany(self.insert_obs, obs_data)
            cnx.commit()
        finally:
            cnx.close()

    def executemany_safe(self, cursor, stmt, data):
        try:
            cursor.executemany(stmt, data)
        except mysql.connector.Error as err:
            if err.errno != errorcode.ER_DUP_ENTRY:
                raise err
            print 'Encountered a dup while executing %d statements: %s' % (len(data), err)
            for datum in data:
                try:
                    cursor.execute(stmt, datum)
                except mysql.connector.Error as err:
                    if err.errno != errorcode.ER_DUP_ENTRY:
                        raise err
                    print 'Encountered a dup while executing a statement: %s' % err

    def testInsertDuplicates(self):
        cnx = mysql.connector.connect(**self.db_config);
        try:
            self.deleteDebugObs(cnx)
            cursor = cnx.cursor()
            timestamp = int(time.time())
            for i in range (0,5000):
                obs_data = []
                for j in range (0,10):
                    obs_data.append(self.makeDebugObs(timestamp))
                    if not (i == 10 and j == 5):
                        timestamp += 1            
                self.executemany_safe(cursor, self.insert_obs, obs_data)
            cnx.commit()
        finally:
            cnx.close()

if __name__ == '__main__':
    unittest.main()
