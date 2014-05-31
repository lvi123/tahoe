import cookielib
import json
import urllib
import urllib2

class RequestError(Exception):
    def __init__(self, url):
        self.url = url
    def __str__(self):
        return repr(self.url)

class NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response
    https_response = http_response

class LaCrosseAlertsConnection:

    def __init__(self, url = "https://www.lacrossealerts.com"):
        self.url = url
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(NoRedirection,
                                           urllib2.HTTPCookieProcessor(cj))

    def login(self, username, password):
        form = {
            "username" : username,
            "password" : password
            }
        url = self.url + "/login"
        self.opener.open(url, urllib.urlencode(form))

    def logout(self):
        url = self.url + "/logout"
        self.opener.open(url)

    def makeObservationQueryURL(self, sensor_id):
        return self.url + "/v1/observations/%d?format=json" % sensor_id

    def getAllObservationsJSON(self, sensor_id):
        url = self.makeObservationQueryURL(sensor_id) + "&from=-100years"
        return self.getObservationsJSON(url)

    def getLatestObservationJSON(self, sensor_id):
        url = self.makeObservationQueryURL(sensor_id)
        return self.getObservationsJSON(url)
        
    def getObservationsJSON(self, url):
        jdata = json.load(self.opener.open(url))
        return self.validateAndTransform(url, jdata)

    def validateAndTransform(self, url, jdata):
        if not ("success" in jdata and jdata["success"]):
            raise RequestError(url)
        response = jdata["response"]
        serial = response["serial"];
        observations = []
        for item in response["obs"]:
            values = item["values"]
            observation = {
                "serial": serial,
                "timeStamp": item["timeStamp"],
                "rh": values["rh"],
                "temp": values["temp"],
                "temp2": values["temp2"],
                "linkquality": values["linkquality"],
                "lowbatt": values["lowbatt"]
                }
            observations.append(observation)
        return observations