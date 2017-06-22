from java.io import InputStream
from java.lang import Iterable, Object, String
from java.util import Iterator, Stack
from org.xmlpull.v1 import XmlPullParser, XmlPullParserFactory

class ForecastParser(Object):

    __interfaces__ = [Iterable, Iterator]
    __item_types__ = [ForecastObject]
    
    @args(void, [InputStream])
    def __init__(self, stream):
    
        Object.__init__(self)
        
        factory = XmlPullParserFactory.newInstance()
        self.parser = factory.newPullParser()
        self.parser.setInput(stream, None)
        
        self.eventType = self.parser.getEventType()
        self.section = ""
        self.sections = {
            "location": ["name"],
            "credit": ["link"],
            "forecast": ["time", "symbol", "windSpeed", "temperature"]
            }
    
    @args(Iterator(ForecastObject), [])
    def iterator(self):
        return self
    
    def hasNext(self):
    
        while self.eventType != XmlPullParser.END_DOCUMENT:
        
            self.eventType = self.parser.next()
            
            if self.eventType == XmlPullParser.START_TAG:
            
                name = self.parser.getName()
                
                if name in self.sections.keySet():
                    self.section = name
                
                elif self.section != "":
                    tags = self.sections[self.section]
                    if name in tags:
                        return True
            
            elif self.eventType == XmlPullParser.END_TAG:
            
                name = self.parser.getName()
                
                if name in self.sections.keySet():
                    self.section = ""
        
        return False
    
    def next(self):
    
        name = self.parser.getName()
        
        if name == "name":
        
            while self.eventType != XmlPullParser.TEXT:
                self.eventType = self.parser.next()
            
            return ForecastObject("text", self.parser.getText())
        
        elif name == "link":
            return ForecastObject("text", self.parser.getAttributeValue(None, "text"))
        
        elif name == "time":
            from_ = self.parser.getAttributeValue(None, "from")
            to_ = self.parser.getAttributeValue(None, "to")
            return ForecastObject("text", from_ + " to " + to_)
        
        elif name == "symbol":
            return ForecastObject("text", self.parser.getAttributeValue(None, "name"))
        
        elif name == "windSpeed":
            return ForecastObject("text", self.parser.getAttributeValue(None, "name"))
        
        elif name == "temperature":
            value = self.parser.getAttributeValue(None, "value")
            unit = self.parser.getAttributeValue(None, "unit")
            return ForecastObject("text", value + " " + unit)
        
        return ForecastObject("text", self.parser.getName())
    
    def remove(self):
        pass


class ForecastObject(Object):

    __fields__ = {"type": String, "value": String}
    
    @args(void, [String, String])
    def __init__(self, type, value):
    
        Object.__init__(self)
        
        self.type = type
        self.value = value
