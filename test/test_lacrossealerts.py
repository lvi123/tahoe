import ConfigParser
import json
import unittest

from lacrossealerts import *

class TestLaCrosseAlerts(unittest.TestCase):
    
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('test/test.conf')

        self.url = config.get('lacrossealerts', 'url')
        self.username = config.get('lacrossealerts', 'username')
        self.password = config.get('lacrossealerts', 'password')
        self.sensor_id = config.getint('lacrossealerts', 'sensor_id')
        self.debuglevel = config.getint('lacrossealerts', 'debuglevel')

        self.bogus_sensor_id = 123456
        self.bogus_username = 'foo'
        self.bogus_password = 'bar'

    def test_login(self):
        conn = LaCrosseAlertsConnection(self.url, self.debuglevel)
        conn.login(self.username, self.password)
        conn.logout()

    def test_login_fail(self):
        conn = LaCrosseAlertsConnection(self.url, self.debuglevel)
        conn.login(self.bogus_username, self.bogus_password)
        conn.logout()

    def test_get_latest_observation(self):
        conn = LaCrosseAlertsConnection(self.url, self.debuglevel)
        conn.login(self.username, self.password)
        try:
            jdata = conn.get_latest_observation_JSON(self.sensor_id)
            print(json.dumps(jdata, indent=4))
        finally:
            conn.logout()

    def test_get_all_observations(self):
        conn = LaCrosseAlertsConnection(self.url, self.debuglevel)
        conn.login(self.username, self.password)
        try:
            jdata = conn.get_all_observations_JSON(self.sensor_id)
#            print(json.dumps(jdata, indent=4))
        finally:
            conn.logout()

    def test_get_observations_failed_wrong_sensor_id(self):
        conn = LaCrosseAlertsConnection(self.url, self.debuglevel)
        conn.login(self.username, self.password)
        try:
            jdata = conn.get_latest_observation_JSON(self.bogus_sensor_id)
            self.fail('Request for observations for sensor %d should have failed!' % self.bogus_sensor_id)
        except RequestError:
            print('Request for observations for sensor %d failed as expected' % self.bogus_sensor_id)
        finally:
            conn.logout()

    def test_get_observations_failed_wrong_credentials(self):
        conn = LaCrosseAlertsConnection(self.url, self.debuglevel)
        conn.login(self.bogus_username, self.bogus_password)
        try:
            jdata = conn.get_latest_observation_JSON(self.sensor_id)
            self.fail("Request for observations using username '%s' should have failed!" % self.bogus_username )
        except RequestError:
            print("Request for observations using username '%s' failed as expected" % self.bogus_username )
        finally:
            conn.logout()

if __name__ == '__main__':
    unittest.main()
