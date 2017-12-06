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
from java.lang import Object, String, System
from java.net import HttpURLConnection, URL
from java.util import List, Map
from android.widget import Toast
from serpentine.activities import Activity

from app_resources import R

from exceptions import WeatherException
from forecastparser import Forecast, ForecastParser
from widgets import ForecastWidget, LocationListener, LocationWidget

class WeatherForecastActivity(Activity):

    __interfaces__ = [LocationListener]
    
    __fields__ = {"cache": Map(String, CacheItem)}
    
    def __init__(self):
    
        Activity.__init__(self)
        self.state = "entry"
        self.cache = {}
    
    def onCreate(self, bundle):
    
        Activity.onCreate(self, bundle)
        
        self.entryWidget = LocationWidget(self, self)
        self.forecastWidget = ForecastWidget(self)
        self.setContentView(self.entryWidget)
        self.parser = ForecastParser(self.getResources())
    
    def onPause(self):
    
        Activity.onPause(self)
        self.entryWidget.writeLocations()
    
    def locationEntered(self, location):
    
        try:
            forecasts = self.fetchData(location)
        except WeatherException, e:
            Toast.makeText(self, e.getMessage(), Toast.LENGTH_SHORT).show()
            return
        
        try:
            self.forecastWidget.addForecasts(forecasts)
            
            self.state = "forecast"
            self.setContentView(self.forecastWidget)
        
        except:
            Toast.makeText(self, "Failed to read weather forecast,",
                           Toast.LENGTH_SHORT).show()
    
    @args(InputStream, [])
    def getSampleStream(self):
    
        resources = self.getResources()
        return resources.openRawResource(R.raw.sample)
    
    @args(List(Forecast), [String])
    def fetchData(self, place):
    
        current_time = System.currentTimeMillis()
        
        try:
            item = self.cache[place]
            if current_time - item.time < 600000: # 10 minutes
                return item.forecasts
        
        except KeyError:
            pass
        
        url = URL("https://www.yr.no/place/" + place + "/forecast.xml")
        connection = CAST(url.openConnection(), HttpURLConnection)
        connection.setInstanceFollowRedirects(True)
        
        length = connection.getContentLength()
        if length <= 0:
            raise WeatherException("No connection")
        
        try:
            stream = BufferedInputStream(connection.getInputStream())
        except FileNotFoundException:
            raise WeatherException("Resource not found")
        
        #stream = self.getSampleStream()
        forecasts = self.parser.parse(stream)
        stream.close()
        
        self.cache[place] = CacheItem(current_time, forecasts)
        
        return forecasts
    
    def onBackPressed(self):
    
        if self.state == "forecast":
            # Return to the entry widget.
            self.state = "entry"
            self.setContentView(self.entryWidget)
        else:
            # If already showing the entry widget then exit.
            Activity.onBackPressed(self)


class CacheItem(Object):

    __fields__ = {"time": long, "forecasts": List(Forecast)}
    
    @args(void, [long, List(Forecast)])
    def __init__(self, time, forecasts):
    
        Object.__init__(self)
        
        self.time = time
        self.forecasts = forecasts
