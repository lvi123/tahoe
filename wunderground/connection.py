import cookielib
import urllib
import urllib2

from datetime import date
from dateutil.rrule import rrule, DAILY

class WeatherUndegroundConnection:

    def __init__(self, url = 'http://www.wunderground.com'):
        self.url = url
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    def get_observations_for_day(self, station_id, day):
        url = self.url + '/weatherstation/WXDailyHistory.asp?ID=%s&day=%d&year=%d&month=%d&graphspan=day&format=1' % \
            (station_id, day.day, day.year, day.month)
        print url
        return self.opener.open(url).read()

    def get_observations_for_year(self, station_id, year):
        start = date(year, 1, 1)
        end = date(year, 12, 31)
        for day in rrule(DAILY, dtstart=start, until=end):
            self.get_observations_for_day(station_id, day)


