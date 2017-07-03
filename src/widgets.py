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

from java.io import BufferedReader, File, FileNotFoundException, FileReader
from java.lang import String
from java.util import List, Map
from android.content import Context
from android.graphics import Color, Typeface
from android.os import Environment
from android.view import Gravity, View, ViewGroup
from android.widget import AdapterView, Button, EditText, ImageView, \
    GridLayout, LinearLayout, ListView, ScrollView, Space, TextView

from serpentine.adapters import StringListAdapter
from serpentine.widgets import HBox, VBox

from forecastparser import Forecast

class LocationListener:

    @args(void, [String])
    def locationEntered(self, location):
        pass


class LocationAdapter(StringListAdapter):

    def __init__(self, strings):
    
        StringListAdapter.__init__(self, strings)
    
    def getView(self, position, convertView, parent):
    
        # If convertView is not None then reuse it.
        if convertView != None:
            return convertView
        
        view = TextView(parent.getContext())
        view.setText(self.items[position])
        view.setTextSize(view.getTextSize() * 1.25)
        return view


class LocationWidget(VBox):

    __interfaces__ = [AdapterView.OnItemClickListener]
    
    @args(void, [Context, LocationListener])
    def __init__(self, context, locationHandler):
    
        VBox.__init__(self, context)
        
        self.locationHandler = locationHandler
        
        self.locations = self.readLocations()
        
        keys = []
        for location in self.locations.keySet():
            keys.add(location)
        
        listView = ListView(context)
        self.adapter = LocationAdapter(keys)
        listView.setAdapter(self.adapter)
        listView.setOnItemClickListener(self)
        
        self.addView(listView)
    
    def onItemClick(self, parent, view, position, id):
    
        try:
            location = self.adapter.items[int(id)]
            self.locationHandler.locationEntered(self.locations[location])
        except IndexError:
            pass
    
    @args(Map(String, String), [])
    def readLocations(self):
    
        locations = {}
        
        if Environment.getExternalStorageState() != Environment.MEDIA_MOUNTED:
            return locations
        
        storageDir = Environment.getExternalStoragePublicDirectory(
            Environment.DIRECTORY_DOWNLOADS)
        
        subdir = File(storageDir, "WeatherForecast")
        if not subdir.exists():
            return locations
        
        f = File(subdir, "locations.txt")
        
        try:
            stream = BufferedReader(FileReader(f))
            while True:
            
                line = stream.readLine()
                if line == None:
                    break
                
                index = line.indexOf(":")
                if index == -1:
                    continue
                
                place = line[:index]
                spec = line[index + 1:].trim()
                locations[place] = spec
            
            stream.close()
        
        except FileNotFoundException:
            pass
        
        return locations


class ForecastWidget(VBox):

    def __init__(self, context):
    
        VBox.__init__(self, context)
        
        self.placeLabel = TextView(context)
        self.placeLabel.setTextSize(self.placeLabel.getTextSize() * 1.5)
        self.placeLabel.setGravity(Gravity.CENTER)
        
        self.scrollView = ScrollView(context)
        self.creditLabel = TextView(context)
        
        self.grid = GridLayout(context)
        self.grid.setColumnCount(2)
        #self.grid.setUseDefaultMargins(True)
        self.scrollView.addView(self.grid)
        
        self.addView(self.creditLabel)
        self.addView(self.placeLabel)
        self.addView(self.scrollView)
    
    @args(void, [List(Forecast)])
    def addForecasts(self, forecasts):
    
        self.grid.removeAllViews()
        self.scrollView.scrollTo(0, 0)
        
        if len(forecasts) > 0:
            self.placeLabel.setText(forecasts[0].place)
            self.creditLabel.setText(forecasts[0].credit)
        
        for forecast in forecasts:
            self.addForecast(forecast)
    
    @args(void, [Forecast])
    def addForecast(self, forecast):
    
        context = self.getContext()
        
        # Date
        dateView = TextView(context)
        dateView.setText(str(forecast.midDate))
        dateView.setTypeface(Typeface.create(None, Typeface.BOLD))
        
        lp = GridLayout.LayoutParams(self.grid.spec(self.grid.getRowCount()),
                                     self.grid.spec(0, 2))
        lp.setGravity(Gravity.CENTER)
        lp.topMargin = 12
        dateView.setLayoutParams(lp)
        self.grid.addView(dateView)
        
        # Symbol and temperature
        row = self.grid.getRowCount()
        
        lp = GridLayout.LayoutParams(self.grid.spec(row), self.grid.spec(0))
        lp.setGravity(Gravity.CENTER)
        
        if forecast.symbol != -1:
            imageView = ImageView(context)
            imageView.setImageResource(forecast.symbol)
            imageView.setLayoutParams(lp)
            self.grid.addView(imageView)
        else:
            spacer = Space(context)
            spacer.setLayoutParams(lp)
            self.grid.addView(spacer)
        
        lp = GridLayout.LayoutParams(self.grid.spec(row), self.grid.spec(1))
        lp.setGravity(Gravity.CENTER)
        
        tempView = TextView(context)
        tempView.setTextSize(tempView.getTextSize() * 2)
        if forecast.temperatureUnit == "celsius":
            tempView.setText(forecast.temperature + u"\u2103")
        else:
            tempView.setText(forecast.temperature + " " + forecast.temperatureUnit)
        
        tempView.setLayoutParams(lp)
        self.grid.addView(tempView)
        
        # Description and wind speed
        row = self.grid.getRowCount()
        
        descView = TextView(context)
        descView.setText(forecast.description)
        lp = GridLayout.LayoutParams(self.grid.spec(row), self.grid.spec(0))
        lp.setGravity(Gravity.CENTER)
        descView.setLayoutParams(lp)
        self.grid.addView(descView)
        
        windView = TextView(context)
        windView.setText(forecast.windSpeed)
        lp = GridLayout.LayoutParams(self.grid.spec(row), self.grid.spec(1))
        lp.setGravity(Gravity.CENTER)
        windView.setLayoutParams(lp)
        self.grid.addView(windView)
