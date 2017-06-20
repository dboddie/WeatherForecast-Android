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
from android.widget import TextView
from org.xmlpull.v1 import XmlPullParser, XmlPullParserFactory
from serpentine.activities import Activity

from app_resources import R

from exceptions import WeatherException
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
    
        stream = self.getSampleStream()
        s = self.parseData(stream)
        self.forecastWidget.addText(s)
        self.setContentView(self.forecastWidget)
    
    @args(InputStream, [])
    def getSampleStream(self):
    
        resources = self.getResources()
        return resources.openRawResource(R.raw.sample)
    
    @args(InputStream, [String])
    def fetchData(self, place):
    
        url = URL("https://www.yr.no/place/david/www-repo/Personal/Updates/2016/images/duck-small.png")
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
    
    @args(String, [InputStream])
    def parseData(self, stream):
    
        factory = XmlPullParserFactory.newInstance()
        parser = factory.newPullParser()
        parser.setInput(stream, None)
        
        eventType = parser.getEventType()
        s = ""
        
        while eventType != XmlPullParser.END_DOCUMENT:
        
            if eventType == XmlPullParser.START_DOCUMENT:
                s += "Start document\n"
            elif eventType == XmlPullParser.START_TAG:
                s += "Start tag: " + parser.getName() + "\n"
            elif eventType == XmlPullParser.END_TAG:
                s += "End tag: " + parser.getName() + "\n"
            
            eventType = parser.next()
        
        s += "End document"
        
        return s
