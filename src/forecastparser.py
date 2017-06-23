from java.io import InputStream
from java.lang import Object, String
from java.text import DateFormat, ParsePosition, SimpleDateFormat
from java.util import Date, List, TimeZone
from android.view import View
from org.xmlpull.v1 import XmlPullParser, XmlPullParserFactory

from app_resources import R

class ForecastParser(Object):

    @static
    @args(List(Forecast), [InputStream])
    def parse(stream):
    
        symbols = {
            "s1d": R.drawable.s01d, "s1m": R.drawable.s01m,
            "s1n": R.drawable.s01n, "s2d": R.drawable.s02d,
            "s2m": R.drawable.s02m, "s2n": R.drawable.s02n,
            "s3d": R.drawable.s03d, "s3m": R.drawable.s03m,
            "s3n": R.drawable.s03n, "s4": R.drawable.s04,
            "s5d": R.drawable.s05d, "s5m": R.drawable.s05m,
            "s5n": R.drawable.s05n, "s6d": R.drawable.s06d,
            "s6m": R.drawable.s06m, "s6n": R.drawable.s06n,
            "s7d": R.drawable.s07d, "s7m": R.drawable.s07m,
            "s7n": R.drawable.s07n, "s8d": R.drawable.s08d,
            "s8m": R.drawable.s08m, "s8n": R.drawable.s08n,
            "s9": R.drawable.s09, "s10": R.drawable.s10,
            "s11": R.drawable.s11, "s12": R.drawable.s12,
            "s13": R.drawable.s13, "s14": R.drawable.s14,
            "s15": R.drawable.s15, "s20d": R.drawable.s20d,
            "s20m": R.drawable.s20m, "s20n": R.drawable.s20n,
            "s21d": R.drawable.s21d, "s21m": R.drawable.s21m,
            "s21n": R.drawable.s21n, "s22": R.drawable.s22,
            "s23": R.drawable.s23, "s24d": R.drawable.s24d,
            "s24m": R.drawable.s24m, "s24n": R.drawable.s24n,
            "s25d": R.drawable.s25d, "s25m": R.drawable.s25m,
            "s25n": R.drawable.s25n, "s26d": R.drawable.s26d,
            "s26m": R.drawable.s26m, "s26n": R.drawable.s26n,
            "s27d": R.drawable.s27d, "s27m": R.drawable.s27m,
            "s27n": R.drawable.s27n, "s28d": R.drawable.s28d,
            "s28m": R.drawable.s28m, "s28n": R.drawable.s28n,
            "s29d": R.drawable.s29d, "s29m": R.drawable.s29m,
            "s29n": R.drawable.s29n, "s30": R.drawable.s30,
            "s31": R.drawable.s31, "s32": R.drawable.s32,
            "s33": R.drawable.s33, "s34": R.drawable.s34,
            "s40d": R.drawable.s40d, "s40m": R.drawable.s40m,
            "s40n": R.drawable.s40n, "s41d": R.drawable.s41d,
            "s41m": R.drawable.s41m, "s41n": R.drawable.s41n,
            "s42d": R.drawable.s42d, "s42m": R.drawable.s42m,
            "s42n": R.drawable.s42n, "s43d": R.drawable.s43d,
            "s43m": R.drawable.s43m, "s43n": R.drawable.s43n,
            "s44d": R.drawable.s44d, "s44m": R.drawable.s44m,
            "s44n": R.drawable.s44n, "s45d": R.drawable.s45d,
            "s45m": R.drawable.s45m, "s45n": R.drawable.s45n,
            "s46": R.drawable.s46, "s47": R.drawable.s47,
            "s48": R.drawable.s48, "s49": R.drawable.s49,
            "s50": R.drawable.s50
            }
        
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
                        symbol = "s" + parser.getAttributeValue(None, "numberEx")
                        
                        try:
                            forecast.symbol = symbols[symbol]
                            continue
                        except KeyError:
                            pass
                        
                        if forecast.from_.after(sunrise) and \
                            forecast.from_.before(sunset):
                            symbol += "d"
                        else:
                            symbol += "n"
                        
                        try:
                            forecast.symbol = symbols[symbol]
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
