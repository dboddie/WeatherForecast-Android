from java.io import InputStream
from java.lang import Iterable, Object, String
from java.util import Iterator, NoSuchElementException
from org.xmlpull.v1 import XmlPullParser, XmlPullParserFactory

class ForecastParser(Object):

    __interfaces__ = [Iterable, Iterator]
    __item_types__ = [String]
    
    @args(void, [InputStream])
    def __init__(self, stream):
    
        Object.__init__(self)
        
        factory = XmlPullParserFactory.newInstance()
        self.parser = factory.newPullParser()
        self.parser.setInput(stream, None)
        
        self.eventType = self.parser.getEventType()
    
    @args(Iterator(String), [])
    def iterator(self):
        return self
    
    def hasNext(self):
        while self.eventType != XmlPullParser.END_DOCUMENT:
        
            lastEventType = self.eventType
            self.eventType = self.parser.next()
            
            if lastEventType == XmlPullParser.START_TAG:
                return True
        
        return False
    
    def next(self):
        return self.parser.getName()
    
    def remove(self):
        pass
