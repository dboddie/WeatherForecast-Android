"""
forecastparser.py - An XML parser for the Weather Forecast application.

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

from java.io import InputStream
from java.lang import Object, String
from java.text import DateFormat, ParsePosition, SimpleDateFormat
from java.util import Date, List, TimeZone
from android.content.res import Resources
from android.view import View
from org.xmlpull.v1 import XmlPullParser, XmlPullParserFactory

from app_resources import R

class ForecastParser(Object):

    @args(void, [Resources])
    def __init__(self, resources):
    
        Object.__init__(self)
        
        symbols = resources.getStringArray(R.array.symbols)
        resourceIDs = resources.getIntArray(R.array.resourceIDs)
        
        self.symbols = {}
        
        for i in range(len(symbols)):
            self.symbols[symbols[i]] = resourceIDs[i]
    
    @args(List(Forecast), [InputStream])
    def parse(self, stream):
    
        factory = XmlPullParserFactory.newInstance()
        parser = factory.newPullParser()
        parser.setInput(stream, None)
        
        eventType = parser.getEventType()
        section = ""
        sections = {"location", "credit", "tabular"}
        
        dateFormat = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
        dateFormat.setTimeZone(TimeZone.getTimeZone("UTC"))
        sunrise = Date()
        sunset = Date()
        
        place = ""
        credit = ""
        forecasts = []
        forecast = Forecast()
        
        while eventType != XmlPullParser.END_DOCUMENT:
        
            eventType = parser.next()
            
            if eventType == XmlPullParser.START_TAG:
            
                name = parser.getName()
                
                if name in sections:
                    section = name
                
                elif section != "":
                
                    if name == "name":
                        while eventType != XmlPullParser.TEXT:
                            eventType = parser.next()
                        
                        place = parser.getText()
                    
                    elif name == "link":
                        credit = parser.getAttributeValue(None, "text")
                    
                    elif name == "time":
                    
                        forecast = Forecast()
                        forecast.place = place
                        forecast.credit = credit
                        
                        from_ = parser.getAttributeValue(None, "from")
                        to_ = parser.getAttributeValue(None, "to")
                        forecast.from_ = dateFormat.parse(from_, ParsePosition(0))
                        forecast.to_ = dateFormat.parse(to_, ParsePosition(0))
                    
                    elif name == "symbol":
                    
                        forecast.description = parser.getAttributeValue(None, "name")
                        symbol = parser.getAttributeValue(None, "numberEx")
                        
                        try:
                            forecast.symbol = self.symbols[symbol]
                            continue
                        except KeyError:
                            pass
                        
                        if forecast.from_.after(sunrise) and \
                            forecast.from_.before(sunset):
                            symbol += "d"
                        else:
                            symbol += "n"
                        
                        try:
                            forecast.symbol = self.symbols[symbol]
                        except KeyError:
                            forecast.symbol = -1
                    
                    elif name == "windSpeed":
                        forecast.windSpeed = parser.getAttributeValue(None, "name")
                    
                    elif name == "temperature":
                        forecast.temperature = parser.getAttributeValue(None, "value")
                        forecast.temperatureUnit = parser.getAttributeValue(None, "unit")
                
                elif name == "sun":
                    rise = parser.getAttributeValue(None, "rise")
                    sset = parser.getAttributeValue(None, "set")
                    sunrise = dateFormat.parse(rise, ParsePosition(0))
                    sunset = dateFormat.parse(sset, ParsePosition(0))
            
            elif eventType == XmlPullParser.END_TAG:
            
                name = parser.getName()
                
                if name == section and name in sections:
                    section = ""
                
                elif section == "tabular" and name == "time":
                    forecasts.add(forecast)
        
        return forecasts


class Forecast(Object):

    __fields__ = {
        "place": String,
        "credit": String,
        "from_": Date, "to_": Date,
        "symbol": int,
        "description": String,
        "windSpeed": String,
        "temperature": String,
        "temperatureUnit": String,
        }
    
    def __init__(self):
        Object.__init__(self)
