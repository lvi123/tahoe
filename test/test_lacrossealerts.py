import ConfigParser
import json
import unittest

from lacrossealerts import *

#httplib.HTTPConnection.debuglevel = 1

class TestLaCrosseAlerts(unittest.TestCase):
    
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('test/test.conf')

        self.url = config.get('lacrossealerts', 'url')
        self.username = config.get('lacrossealerts', 'username')
        self.password = config.get('lacrossealerts', 'password')
        self.sensor_id = config.getint('lacrossealerts', 'sensor_id')

        self.bogus_sensor_id = 123456
        self.bogus_username = 'foo'
        self.bogus_password = 'bar'

    def testLogin(self):
        conn = LaCrosseAlertsConnection(self.url)
        conn.login(self.username, self.password)
        conn.logout()

    def testLoginFail(self):
        conn = LaCrosseAlertsConnection(self.url)
        conn.login(self.bogus_username, self.bogus_password)
        conn.logout()

    def testGetLatestObservation(self):
        conn = LaCrosseAlertsConnection(self.url)
        conn.login(self.username, self.password)
        try:
            jdata = conn.getLatestObservationJSON(self.sensor_id)
            print(json.dumps(jdata, indent=4))
        finally:
            conn.logout()

    def testGetAllObservations(self):
        conn = LaCrosseAlertsConnection(self.url)
        conn.login(self.username, self.password)
        try:
            jdata = conn.getAllObservationsJSON(self.sensor_id)
            print(json.dumps(jdata, indent=4))
        finally:
            conn.logout()

    def testGetObservationsFailedWrongSensorId(self):
        conn = LaCrosseAlertsConnection(self.url)
        conn.login(self.username, self.password)
        try:
            jdata = conn.getLatestObservationJSON(self.bogus_sensor_id)
            self.fail('Request for observations for sensor %d should have failed!' % self.bogus_sensor_id)
        except RequestError:
            print('Request for observations for sensor %d failed as expected' % self.bogus_sensor_id)
        finally:
            conn.logout()

    def testGetObservationsFailedWrongCredentials(self):
        conn = LaCrosseAlertsConnection(self.url)
        conn.login(self.bogus_username, self.bogus_password)
        try:
            jdata = conn.getLatestObservationJSON(self.sensor_id)
            self.fail("Request for observations using username '%s' should have failed!" % self.bogus_username )
        except RequestError:
            print("Request for observations using username '%s' failed as expected" % self.bogus_username )
        finally:
            conn.logout()

if __name__ == '__main__':
    unittest.main()
