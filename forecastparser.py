from java.io import InputStream
from java.lang import Iterable, Object, String
from java.util import Iterator, Stack
from org.xmlpull.v1 import XmlPullParser, XmlPullParserFactory

class NameStack(Stack):

    __item_types__ = [String]
    
    def __init__(self):
        Stack.__init__(self)


class ForecastParser(Object):

    __interfaces__ = [Iterable, Iterator]
    __item_types__ = [String]
    
    @args(void, [InputStream])
    def __init__(self, stream):
    
        Object.__init__(self)
        
        factory = XmlPullParserFactory.newInstance()
        self.parser = factory.newPullParser()
        self.parser.setInput(stream, None)
        
        self.name_stack = NameStack()
        
        self.eventType = self.parser.getEventType()
    
    @args(Iterator(String), [])
    def iterator(self):
        return self
    
    def hasNext(self):
    
        while self.eventType != XmlPullParser.END_DOCUMENT:
        
            self.eventType = self.parser.next()
            
            if self.eventType == XmlPullParser.START_TAG:
                self.name_stack.push(self.parser.getName())
                return True
            elif self.eventType == XmlPullParser.END_TAG:
                self.name_stack.pop()
        
        return False
    
    def next(self):
    
        return self.name_stack.peek()
    
    def remove(self):
        pass
