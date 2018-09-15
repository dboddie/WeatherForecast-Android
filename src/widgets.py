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
from java.util import Calendar, List, Locale, Map
from android.content import Context
from android.graphics import Color, Typeface
from android.os import Environment
from android.view import Gravity, View, ViewGroup
from android.widget import AdapterView, AutoCompleteTextView, Button, \
    EditText, ImageView, LinearLayout, ListView, RelativeLayout, ScrollView, \
    Space, TextView

import android.R

from serpentine.files import Files
from serpentine.adapters import FilterStringArrayAdapter, StringListAdapter
from serpentine.widgets import HBox

from app_resources import R

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
    
    def addLocation(self, name, spec):
    
        if self.locations.containsKey(name):
            return
        
        self.locations[name] = spec
        self.order.add(name)
        
        self.adapter.items.add(name)
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

    @args(void, [String, String])
    def addLocation(self, name, spec):
        pass


class AddWidget(HBox):

    __interfaces__ = [View.OnClickListener]
    
    @args(void, [Context, AddLocationListener])
    def __init__(self, context, handler):
    
        HBox.__init__(self, context)
        self.handler = handler
        
        # Read the lists of place names and place specifications from the
        # application's resources, creating a dictionary from the two lists.
        self.places = {}
        resources = context.getResources()
        place_names = resources.getStringArray(R.array.place_names)
        
        for name, place in zip(place_names,
                               resources.getStringArray(R.array.places)):
            self.places[name] = place
        
        # Use a specialised adapter to provide filtered lists of data for an
        # auto-complete-enabled text view.
        adapter = FilterStringArrayAdapter(context,
            android.R.layout.simple_dropdown_item_1line, place_names)
        
        self.locationEdit = AutoCompleteTextView(context)
        self.locationEdit.setAdapter(adapter)
        
        self.addButton = Button(context)
        self.addButton.setText("Add")
        self.addButton.setOnClickListener(self)
        
        self.addWeightedView(self.locationEdit, 2)
        self.addWeightedView(self.addButton, 0)
    
    def onClick(self, view):
    
        text = str(CAST(self.locationEdit, TextView).getText())
        
        name = text.trim()
        
        try:
            spec = self.places[name]
        except KeyError:
            return
        
        # Remove the country from the name.
        name = name[:name.indexOf(", ")]
        
        self.handler.addLocation(name, spec)
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
        
        # This getColor call deprecated in API level 23.
        lightBackground = context.getResources().getColor(android.R.color.background_light)
        
        # Header
        header = LinearLayout(context)
        header.setOrientation(LinearLayout.VERTICAL)
        header.setId(1)
        
        self.placeLabel = TextView(context)
        self.placeLabel.setTextSize(self.placeLabel.getTextSize() * 1.5)
        self.placeLabel.setGravity(Gravity.CENTER)
        
        headerLine = View(context)
        headerLine.setBackgroundColor(lightBackground)
        headerLineParams = LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, 1) # 1 pixel in height
        
        header.addView(self.placeLabel)
        header.addView(headerLine, headerLineParams)
        
        # Middle - containing the forecast layout
        self.scrollView = ScrollView(context)
        self.scrollView.setId(2)
        
        # Footer
        footer = LinearLayout(context)
        footer.setOrientation(LinearLayout.VERTICAL)
        footer.setId(3)
        
        footerLine = View(context)
        footerLine.setBackgroundColor(lightBackground)
        footerLineParams = LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, 1) # 1 pixel in height
        
        self.creditLabel = TextView(context)
        
        footer.addView(footerLine, footerLineParams)
        footer.addView(self.creditLabel)
        
        # The forecast layout
        self.forecastLayout = LinearLayout(context)
        self.forecastLayout.setOrientation(LinearLayout.VERTICAL)
        self.scrollView.addView(self.forecastLayout)
        
        # Layout parameters
        headerParams = RelativeLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT)
        headerParams.addRule(RelativeLayout.ALIGN_PARENT_TOP)
        headerParams.addRule(RelativeLayout.CENTER_HORIZONTAL)
        
        scrollParams = RelativeLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT)
        scrollParams.addRule(RelativeLayout.CENTER_HORIZONTAL)
        scrollParams.addRule(RelativeLayout.BELOW, 1)
        scrollParams.addRule(RelativeLayout.ABOVE, 3)
        
        footerParams = RelativeLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT)
        footerParams.addRule(RelativeLayout.ALIGN_PARENT_BOTTOM)
        
        self.addView(header, headerParams)
        self.addView(self.scrollView, scrollParams)
        self.addView(footer, footerParams)
    
    @args(void, [List(Forecast)])
    def addForecasts(self, forecasts):
    
        self.forecastLayout.removeAllViews()
        self.scrollView.scrollTo(0, 0)
        
        if len(forecasts) == 0:
            return
        
        self.placeLabel.setText(forecasts[0].place)
        self.creditLabel.setText(forecasts[0].credit)
        
        firstDate = forecasts[0].from_
        calendar = Calendar.getInstance()
        calendar.setTime(firstDate)
        
        currentDay = calendar.get(Calendar.DAY_OF_MONTH)
        
        context = self.getContext()
        
        for forecast in forecasts:
        
            #             Date
            # Temperature Symbol Description
            #                    Wind
            
            # Get the day of the month.
            date = forecast.from_
            calendar.setTime(date)
            day = calendar.get(Calendar.DAY_OF_MONTH)
            
            # Add an item for the date for the first item and any item
            # following a day change.
            if date == firstDate or day != currentDay:
                dateView = TextView(context)
                dateView.setText(
                    calendar.getDisplayName(Calendar.DAY_OF_WEEK,
                        Calendar.LONG, Locale.getDefault()) + " " + \
                    str(day) + " " + \
                    calendar.getDisplayName(Calendar.MONTH,
                        Calendar.LONG, Locale.getDefault()) + " " + \
                    str(calendar.get(Calendar.YEAR)))
                
                dateView.setGravity(Gravity.CENTER)
                dateView.setTypeface(Typeface.create(None, Typeface.BOLD))
                
                self.forecastLayout.addView(dateView, self.rowLayout())
            
            currentDay = day
            
            # Time
            timeString = String.format("%02d:%02d:%02d - ",
                array([calendar.get(Calendar.HOUR_OF_DAY),
                       calendar.get(Calendar.MINUTE),
                       calendar.get(Calendar.SECOND)]))
            
            date = forecast.to_
            calendar.setTime(date)
            
            timeString += String.format("%02d:%02d:%02d",
                array([calendar.get(Calendar.HOUR_OF_DAY),
                       calendar.get(Calendar.MINUTE),
                       calendar.get(Calendar.SECOND)]))
            
            timeView = TextView(context)
            timeView.setText(timeString)
            
            timeView.setGravity(Gravity.CENTER)
            timeView.setTypeface(Typeface.create(None, Typeface.BOLD))
            
            self.forecastLayout.addView(timeView, self.rowLayout())
            
            # Symbol, temperature, description and wind
            row = RelativeLayout(context)
            
            # Symbol
            lp = self.itemLayout()
            lp.addRule(RelativeLayout.CENTER_IN_PARENT)
            
            if forecast.symbol != -1:
                imageView = ImageView(context)
                imageView.setImageResource(forecast.symbol)
                row.addView(imageView, lp)
            else:
                spacer = Space(context)
                row.addView(spacer, lp)
            
            # Temperature
            tempView = TextView(context)
            tempView.setTextSize(tempView.getTextSize() * 2)
            
            if forecast.temperatureUnit == "celsius":
                tempView.setText(forecast.temperature + u"\u2103")
            else:
                tempView.setText(forecast.temperature + " " + forecast.temperatureUnit)
            
            lp = self.itemLayout()
            lp.addRule(RelativeLayout.CENTER_VERTICAL)
            lp.addRule(RelativeLayout.ALIGN_PARENT_LEFT)
            row.addView(tempView, lp)
            
            # Description and wind speed
            descLayout = LinearLayout(context)
            descLayout.setOrientation(LinearLayout.VERTICAL)
            
            descView = TextView(context)
            descView.setText(forecast.description)
            descLayout.addView(descView, lp)
            
            windView = TextView(context)
            windView.setText(forecast.windSpeed)
            descLayout.addView(windView, lp)
            
            lp = self.itemLayout()
            lp.addRule(RelativeLayout.CENTER_VERTICAL)
            lp.addRule(RelativeLayout.ALIGN_PARENT_RIGHT)
            row.addView(descLayout, lp)
            
            self.forecastLayout.addView(row, self.rowLayout())
    
    @args(LinearLayout.LayoutParams, [])
    def rowLayout(self):
    
        return LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                                         ViewGroup.LayoutParams.WRAP_CONTENT)
    
    @args(RelativeLayout.LayoutParams, [])
    def itemLayout(self):
    
        return RelativeLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT,
                                           ViewGroup.LayoutParams.WRAP_CONTENT)
