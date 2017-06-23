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
from android.view import Gravity, View, ViewGroup
from android.widget import Button, EditText, ImageView, LinearLayout, \
                           ScrollView, Space, TextView
from serpentine.widgets import HBox, VBox

from forecastparser import Forecast

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
    
    @args(void, [Forecast])
    def addForecast(self, forecast):
    
        context = self.getContext()
        
        # Date
        dateView = TextView(context)
        dateView.setText(forecast.from_.toString())
        dateView.setGravity(Gravity.CENTER)
        
        # Symbol and description
        symbolBox = VBox(context)
        symbolBox.setGravity(Gravity.LEFT)
        symbolBox.setBackgroundColor(0x80f08080)
        
        descView = TextView(context)
        descView.setText(forecast.description)
        symbolBox.addView(descView)
        
        if forecast.symbol != -1:
            imageView = ImageView(context)
            imageView.setImageResource(forecast.symbol)
            symbolBox.addView(imageView)
        
        # Temperature and wind speed
        tempBox = VBox(context)
        tempBox.setGravity(Gravity.RIGHT)
        tempBox.setBackgroundColor(0x8080f080)
        
        tempView = TextView(context)
        tempView.setTextSize(tempView.getTextSize() * 2)
        if forecast.temperatureUnit == "celsius":
            tempView.setText(forecast.temperature + u"\u2103")
        else:
            tempView.setText(forecast.temperature + " " + forecast.temperatureUnit)
        
        windView = TextView(context)
        windView.setText(forecast.windSpeed)
        
        tempBox.addView(windView)
        tempBox.addView(tempView)
        
        # Arrange the two boxes.
        hbox = HBox(context)
        hbox.setBackgroundColor(0x80808080)
        hbox.setHorizontalGravity(Gravity.CENTER_HORIZONTAL)
        hbox.addView(symbolBox)
        hbox.addView(tempBox)
        
        self.vbox.addView(dateView)
        self.vbox.addView(hbox)
