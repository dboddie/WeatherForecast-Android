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

from java.io import BufferedReader, File, FileNotFoundException, FileReader, \
                    FileWriter
from java.lang import String
from java.util import List, Map
from android.content import Context
from android.graphics import Color, Typeface
from android.os import Environment
from android.view import Gravity, View, ViewGroup
from android.widget import AdapterView, Button, EditText, ImageView, \
    GridLayout, LinearLayout, ListView, ScrollView, Space, TextView

from serpentine.files import Files
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

    __interfaces__ = [AdapterView.OnItemClickListener,
                      AdapterView.OnItemLongClickListener,
                      AddLocationListener, RemoveLocationListener]
    
    @args(void, [Context, LocationListener])
    def __init__(self, context, locationHandler):
    
        VBox.__init__(self, context)
        
        self.currentItem = -1
        
        self.locationHandler = locationHandler
        self.adapter = self.getAdapter()
        
        self.listView = ListView(context)
        self.listView.setAdapter(self.adapter)
        self.listView.setOnItemClickListener(self)
        self.listView.setOnItemLongClickListener(self)
        
        self.addWidget = AddWidget(context, self)
        self.removeWidget = RemoveWidget(context, self)
        
        self.addView(self.listView)
        self.addWeightedView(Space(context), 1)
        self.addView(self.addWidget)
    
    def readLocations(self):
    
        self.locations = {}
        self.order = []
        
        if Environment.getExternalStorageState() != Environment.MEDIA_MOUNTED:
            return
        
        storageDir = Environment.getExternalStoragePublicDirectory(
            Environment.DIRECTORY_DOWNLOADS)
        
        subdir = File(storageDir, "WeatherForecast")
        if subdir.exists():
        
            f = File(subdir, "locations.txt")
            
            try:
                stream = BufferedReader(FileReader(f))
                while True:
                
                    line = stream.readLine()
                    if line == None:
                        break
                    
                    spec = line.trim()
                    pieces = spec.split("/")
                    
                    if len(pieces) < 3:
                        continue
                    
                    place = pieces[len(pieces) - 1]
                    self.locations[place] = spec
                    self.order.add(place)
                
                stream.close()
            
            except FileNotFoundException:
                pass
    
    def writeLocations(self):
    
        f = Files.createExternalFile(Environment.DIRECTORY_DOWNLOADS,
            "WeatherForecast", "locations.txt", None, None)
        
        try:
            stream = FileWriter(f)
            
            for key in self.order:
                stream.write(self.locations[key] + "\n")
            
            stream.flush()
            stream.close()
        
        except FileNotFoundException:
            pass
    
    @args(LocationAdapter, [])
    def getAdapter(self):
    
        self.readLocations()
        
        keys = []
        for location in self.order:
            keys.add(location)
        
        return LocationAdapter(keys)
    
    def onItemClick(self, parent, view, position, id):
    
        try:
            location = self.adapter.items[int(id)]
            self.locationHandler.locationEntered(self.locations[location])
        except IndexError:
            pass
        
        if self.currentItem != -1:
            self.leaveRemoveMode()
    
    def addLocation(self, location):
    
        spec = location.trim()
        pieces = spec.split("/")
        
        if len(pieces) < 3:
            return
        
        place = pieces[len(pieces) - 1]
        
        if self.locations.containsKey(place):
            return
        
        self.locations[place] = spec
        self.order.add(place)
        
        self.adapter.items.add(place)
        self.listView.setAdapter(self.adapter)
    
    def onItemLongClick(self, parent, view, position, id):
    
        self.currentItem = position
        self.enterRemoveMode()
        return True
    
    def enterRemoveMode(self):
    
        self.removeView(self.addWidget)
        self.addView(self.removeWidget)
    
    def leaveRemoveMode(self):
    
        self.removeView(self.removeWidget)
        self.addView(self.addWidget)
    
    def removeLocation(self):
    
        place = self.order.remove(self.currentItem)
        self.locations.remove(place)
        
        self.adapter.items.remove(place)
        self.listView.setAdapter(self.adapter)
        
        self.currentItem = -1
        self.leaveRemoveMode()
    
    def cancelRemove(self):
    
        self.currentItem = -1
        self.leaveRemoveMode()


class AddLocationListener:

    @args(void, [String])
    def addLocation(self, location):
        pass


class AddWidget(HBox):

    __interfaces__ = [View.OnClickListener]
    
    @args(void, [Context, AddLocationListener])
    def __init__(self, context, handler):
    
        HBox.__init__(self, context)
        self.handler = handler
        
        self.locationEdit = EditText(context)
        
        self.addButton = Button(context)
        self.addButton.setText("Add")
        self.addButton.setOnClickListener(self)
        
        self.addWeightedView(self.locationEdit, 2)
        self.addWeightedView(self.addButton, 0)
    
    def onClick(self, view):
    
        text = str(CAST(self.locationEdit, TextView).getText())
        self.handler.addLocation(text)
        self.locationEdit.setText("")


class RemoveLocationListener:

    def removeLocation(self):
        pass
    
    def cancelRemove(self):
        pass


class RemoveWidget(HBox):

    __interfaces__ = [View.OnClickListener]
    
    @args(void, [Context, RemoveLocationListener])
    def __init__(self, context, handler):
    
        HBox.__init__(self, context)
        self.handler = handler
        
        self.removeButton = Button(context)
        self.removeButton.setText("Remove")
        self.removeButton.setOnClickListener(self)
        
        self.cancelButton = Button(context)
        self.cancelButton.setText("Cancel")
        self.cancelButton.setOnClickListener(self)
        
        self.addWeightedView(self.removeButton, 1)
        self.addWeightedView(self.cancelButton, 1)
    
    def onClick(self, view):
    
        if view == self.removeButton:
            self.handler.removeLocation()
        else:
            self.handler.cancelRemove()


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
