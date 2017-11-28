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
    LinearLayout, ListView, RelativeLayout, ScrollView, Space, \
    TextView

from serpentine.files import Files
from serpentine.adapters import StringListAdapter
from serpentine.widgets import HBox

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


class LocationWidget(RelativeLayout):

    __interfaces__ = [AdapterView.OnItemClickListener,
                      AdapterView.OnItemLongClickListener,
                      AddLocationListener, RemoveLocationListener]
    
    @args(void, [Context, LocationListener])
    def __init__(self, context, locationHandler):
    
        RelativeLayout.__init__(self, context)
        
        self.currentItem = -1
        self.mode = "normal"
        
        self.locationHandler = locationHandler
        self.adapter = self.getAdapter()
        
        self.listView = ListView(context)
        self.listView.setAdapter(self.adapter)
        self.listView.setOnItemClickListener(self)
        self.listView.setOnItemLongClickListener(self)
        
        self.addWidget = AddWidget(context, self)
        self.addWidget.setId(1)
        self.removeWidget = RemoveWidget(context, self)
        
        listParams = RelativeLayout.LayoutParams(
            ViewGroup.LayoutParams.WRAP_CONTENT,
            ViewGroup.LayoutParams.WRAP_CONTENT)
        listParams.addRule(RelativeLayout.ALIGN_PARENT_TOP)
        listParams.addRule(RelativeLayout.ABOVE, 1)
        
        self.addView(self.listView, listParams)
        self.addView(self.addWidget, self.getAddParams())
    
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
    
        if self.mode == "normal":
            self.currentItem = position
            self.enterRemoveMode()
        
        return True
    
    def enterRemoveMode(self):
    
        self.removeView(self.addWidget)
        self.addWidget.setId(2)
        
        removeParams = RelativeLayout.LayoutParams(
            ViewGroup.LayoutParams.WRAP_CONTENT,
            ViewGroup.LayoutParams.WRAP_CONTENT)
        removeParams.addRule(RelativeLayout.ALIGN_PARENT_BOTTOM)
        removeParams.addRule(RelativeLayout.ALIGN_PARENT_LEFT)
        removeParams.addRule(RelativeLayout.ALIGN_PARENT_RIGHT)
        
        self.addView(self.removeWidget, removeParams)
        self.removeWidget.setId(1)
        self.mode = "remove"
    
    def leaveRemoveMode(self):
    
        self.removeView(self.removeWidget)
        self.removeWidget.setId(2)
        self.addView(self.addWidget, self.getAddParams())
        self.addWidget.setId(1)
        self.mode = "normal"
    
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
    
    @args(RelativeLayout.LayoutParams, [])
    def getAddParams(self):
    
        addParams = RelativeLayout.LayoutParams(
            ViewGroup.LayoutParams.WRAP_CONTENT,
            ViewGroup.LayoutParams.WRAP_CONTENT)
        addParams.addRule(RelativeLayout.ALIGN_PARENT_BOTTOM)
        addParams.addRule(RelativeLayout.ALIGN_PARENT_LEFT)
        addParams.addRule(RelativeLayout.ALIGN_PARENT_RIGHT)
        return addParams


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


class ForecastWidget(RelativeLayout):

    def __init__(self, context):
    
        RelativeLayout.__init__(self, context)
        
        self.placeLabel = TextView(context)
        self.placeLabel.setTextSize(self.placeLabel.getTextSize() * 1.5)
        self.placeLabel.setGravity(Gravity.CENTER)
        self.placeLabel.setId(1)
        
        self.scrollView = ScrollView(context)
        self.creditLabel = TextView(context)
        self.creditLabel.setId(2)
        
        self.forecastLayout = RelativeLayout(context)
        self.scrollView.addView(self.forecastLayout)
        
        placeParams = RelativeLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT)
        placeParams.addRule(RelativeLayout.ALIGN_PARENT_TOP)
        placeParams.addRule(RelativeLayout.CENTER_HORIZONTAL)
        
        scrollParams = RelativeLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT)
        scrollParams.addRule(RelativeLayout.BELOW, 1)
        scrollParams.addRule(RelativeLayout.ABOVE, 2)
        scrollParams.addRule(RelativeLayout.CENTER_HORIZONTAL)
        
        creditParams = RelativeLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT)
        creditParams.addRule(RelativeLayout.ALIGN_PARENT_BOTTOM)
        
        self.addView(self.placeLabel, placeParams)
        self.addView(self.scrollView, scrollParams)
        self.addView(self.creditLabel, creditParams)
    
    @args(void, [List(Forecast)])
    def addForecasts(self, forecasts):
    
        self.forecastLayout.removeAllViews()
        self.scrollView.scrollTo(0, 0)
        
        if len(forecasts) == 0:
            return
        
        self.placeLabel.setText(forecasts[0].place)
        self.creditLabel.setText(forecasts[0].credit)
        
        context = self.getContext()
        previousId = 0
        nextId = 0x100
        
        last_forecast = forecasts[len(forecasts) - 1]
        
        for forecast in forecasts:
        
            is_last = forecast == last_forecast
            
            #             Date
            # Temperature Symbol Description
            #                    Wind
            
            # Date
            dateId = nextId
            
            dateView = TextView(context)
            dateView.setText(str(forecast.midDate))
            dateView.setGravity(Gravity.CENTER)
            dateView.setTypeface(Typeface.create(None, Typeface.BOLD))
            dateView.setId(dateId)
            
            lp = RelativeLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT)
            
            if previousId == 0:
                lp.addRule(RelativeLayout.ALIGN_PARENT_TOP)
            else:
                lp.addRule(RelativeLayout.BELOW, previousId)
            
            lp.addRule(RelativeLayout.CENTER_HORIZONTAL)
            
            self.forecastLayout.addView(dateView, lp)
            
            # Symbol
            symbolId = dateId + 1
            
            lp = RelativeLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT)
            
            lp.addRule(RelativeLayout.BELOW, dateId)
            lp.addRule(RelativeLayout.CENTER_HORIZONTAL)
            
            if forecast.symbol != -1:
                imageView = ImageView(context)
                imageView.setImageResource(forecast.symbol)
                imageView.setId(symbolId)
                self.forecastLayout.addView(imageView, lp)
            else:
                spacer = Space(context)
                spacer.setId(symbolId)
                self.forecastLayout.addView(spacer, lp)
            
            # Temperature
            tempId = symbolId + 1
            
            tempView = TextView(context)
            tempView.setTextSize(tempView.getTextSize() * 2)
            tempView.setId(tempId)
            
            if forecast.temperatureUnit == "celsius":
                tempView.setText(forecast.temperature + u"\u2103")
            else:
                tempView.setText(forecast.temperature + " " + forecast.temperatureUnit)
            
            lp = RelativeLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT)
            
            lp.addRule(RelativeLayout.ALIGN_BOTTOM, symbolId)
            lp.addRule(RelativeLayout.ALIGN_PARENT_LEFT)
            
            self.forecastLayout.addView(tempView, lp)
            
            # Description and wind speed
            descId = tempId + 1
            
            descView = TextView(context)
            descView.setText(forecast.description)
            descView.setId(descId)
            
            lp = RelativeLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT)
            
            lp.addRule(RelativeLayout.ALIGN_TOP, tempId)
            lp.addRule(RelativeLayout.ALIGN_PARENT_RIGHT)
            self.forecastLayout.addView(descView, lp)
            
            windView = TextView(context)
            windView.setText(forecast.windSpeed)
            
            lp = RelativeLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT)
            
            lp.addRule(RelativeLayout.BELOW, descId)
            lp.addRule(RelativeLayout.ALIGN_PARENT_RIGHT)
            if is_last:
                lp.addRule(RelativeLayout.ALIGN_PARENT_BOTTOM)
            
            self.forecastLayout.addView(windView, lp)
            
            previousId = symbolId
            nextId = descId + 1
