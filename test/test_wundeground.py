import ConfigParser
import datetime
import unittest

from wunderground import WeatherUndegroundConnection

class TestLaCrosseAlerts(unittest.TestCase):
    
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('test/test.conf')

        self.url = config.get('wunderground', 'url')
        self.station_id = config.get('wunderground', 'station_id')
        self.day = datetime.datetime.strptime(config.get('wunderground', 'day'), '%m/%d/%Y')
        self.year = config.getint('wunderground', 'year')
    
    def testGetObservationsForDay(self):
        conn = WeatherUndegroundConnection(self.url)
        result = conn.getObservationsForDay(self.station_id, self.date)
        print result

    def testGetObservationsForYear(self):
        conn = WeatherUndegroundConnection(self.url)
        result = conn.getObservationsForYear(self.station_id, self.year)
        print result

if __name__ == '__main__':
    unittest.main()


