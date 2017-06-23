"""
weatherforecast.py - Application code for the Weather Forecast application.

Copyright (C) 2017 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from java.io import BufferedInputStream, FileNotFoundException, InputStream
from java.lang import String
from java.net import HttpURLConnection, URL
from serpentine.activities import Activity

from app_resources import R

from exceptions import WeatherException
from forecastparser import ForecastParser
from widgets import ForecastWidget, LocationListener, LocationWidget

class WeatherForecastActivity(Activity):

    __interfaces__ = [LocationListener]
    
    def __init__(self):
    
        Activity.__init__(self)
    
    def onCreate(self, bundle):
    
        Activity.onCreate(self, bundle)
        
        self.entryWidget = LocationWidget(self, self)
        self.forecastWidget = ForecastWidget(self)
        self.setContentView(self.entryWidget)
    
    def locationEntered(self, location):
    
        #stream = self.getSampleStream()
        stream = self.fetchData("Norway/Oslo/Oslo/Oslo")
        parser = ForecastParser(stream, self)
        for obj in parser:
            self.forecastWidget.addChildView(obj)
        
        self.setContentView(self.forecastWidget)
        stream.close()
    
    @args(InputStream, [])
    def getSampleStream(self):
    
        resources = self.getResources()
        return resources.openRawResource(R.raw.sample)
    
    @args(InputStream, [String])
    def fetchData(self, place):
    
        url = URL("http://www.yr.no/place/" + place + "/forecast.xml")
        connection = CAST(url.openConnection(), HttpURLConnection)
        connection.setInstanceFollowRedirects(True)
        
        length = connection.getContentLength()
        if length <= 0:
            raise WeatherException("Zero length content")
        
        try:
            stream = BufferedInputStream(connection.getInputStream())
        except FileNotFoundException:
            raise WeatherException("Resource not found")
        
        return stream
