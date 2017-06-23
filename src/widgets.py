"""
widgets.py - Widgets for the Weather Forecast application.

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

from java.lang import String
from android.content import Context
from android.view import View
from android.widget import Button, EditText, LinearLayout, ScrollView, TextView
from serpentine.widgets import VBox

class LocationListener:

    @args(void, [String])
    def locationEntered(self, location):
        pass


class LocationWidget(VBox):

    __interfaces__ = [View.OnClickListener]
    
    @args(void, [Context, LocationListener])
    def __init__(self, context, locationHandler):
    
        VBox.__init__(self, context)
        self.locationHandler = locationHandler
        
        button = Button(context)
        button.setText("Fetch forecast")
        button.setOnClickListener(self)
        
        self.addView(button)
    
    def onClick(self, view):
    
        self.locationHandler.locationEntered("Hello")


class ForecastWidget(ScrollView):

    def __init__(self, context):
    
        ScrollView.__init__(self, context)
        
        self.vbox = VBox(context)
        self.addView(self.vbox)
    
    @args(void, [View])
    def addChildView(self, view):
    
        self.vbox.addView(view)
