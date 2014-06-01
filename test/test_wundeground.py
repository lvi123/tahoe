import ConfigParser
import datetime
import unittest

from wunderground import WeatherUndegroundConnection

class TestWundeground(unittest.TestCase):
    
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('test/test.conf')

        self.url = config.get('wunderground', 'url')
        self.station_id = config.get('wunderground', 'station_id')
        self.day = datetime.datetime.strptime(config.get('wunderground', 'day'), '%m/%d/%Y')
        self.year = config.getint('wunderground', 'year')
    
    def test_get_observations_for_day(self):
        conn = WeatherUndegroundConnection(self.url)
        result = conn.get_observations_for_day(self.station_id, self.day)
        print result

    def test_get_observations_for_year(self):
        conn = WeatherUndegroundConnection(self.url)
        result = conn.get_observations_for_year(self.station_id, self.year)
        print result

if __name__ == '__main__':
    unittest.main()


