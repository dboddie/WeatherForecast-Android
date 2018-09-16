#!/usr/bin/env python

"""
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

import codecs, os, sys

import DUCK
from DUCK.Tools import buildhelper

def read_places():

    lines = codecs.open("data/noreg.txt", "r", "utf8").readlines()
    lines.pop(0)
    
    places = {}
    
    for line in lines:

        pieces = line.strip().split("\t")
        place_type = pieces[3]
        if place_type == "By":
            name = pieces[1] + u", Norway"
            url = pieces[-1]
            place = url[len("http://www.yr.no/place/"):-len("/forecast.xml")]
            places[name] = place

    lines = codecs.open("data/verda.txt", "r", "utf8").readlines()
    lines.pop(0)
    include_places = ['administration centre', 'airport', 'capital', 'city',
        'island', 'locality', 'populated locality', 'populated place',
        'regional capital', 'seat of government', 'town']
    
    for line in lines:
    
        pieces = line.strip().split("\t")
        place_type = pieces[7]
        if place_type in include_places:
            name = pieces[3] + u", %s" % pieces[10]
            url = pieces[-1]
            place = url[len("http://www.yr.no/place/"):-len("/forecast.xml")]
            places[name] = place
    
    return places.keys(), places.values()


app_name = "Weather Forecast"
package_name = "uk.org.boddie.android.weatherforecast"
symbols = [
    "1d", "1m", "1n", "2d", "2m", "2n", "3d", "3m", "3n",
    "4", "5d", "5m", "5n", "6d", "6m", "6n", "7d", "7m",
    "7n", "8d", "8m", "8n", "9", "10", "11", "12", "13",
    "14", "15", "20d", "20m", "20n", "21d", "21m", "21n",
    "22", "23", "24d", "24m", "24n", "25d", "25m", "25n",
    "26d", "26m", "26n", "27d", "27m", "27n", "28d", "28m",
    "28n", "29d", "29m", "29n", "30", "31", "32", "33", "34",
    "40d", "40m", "40n", "41d", "41m", "41n", "42d", "42m",
    "42n", "43d", "43m", "43n", "44d", "44m", "44n", "45d",
    "45m", "45n", "46", "47", "48", "49", "50"
    ]

place_names, places = read_places()

res_files = {
    "drawable": {
        "ic_launcher": "images/svg/27d.svg",
        "s01d": "images/png/01d.png",
        "s01m": "images/png/01m.png",
        "s01n": "images/png/01n.png",
        "s02d": "images/png/02d.png",
        "s02m": "images/png/02m.png",
        "s02n": "images/png/02n.png",
        "s03d": "images/png/03d.png",
        "s03m": "images/png/03m.png",
        "s03n": "images/png/03n.png",
        "s04": "images/png/04.png",
        "s05d": "images/png/05d.png",
        "s05m": "images/png/05m.png",
        "s05n": "images/png/05n.png",
        "s06d": "images/png/06d.png",
        "s06m": "images/png/06m.png",
        "s06n": "images/png/06n.png",
        "s07d": "images/png/07d.png",
        "s07m": "images/png/07m.png",
        "s07n": "images/png/07n.png",
        "s08d": "images/png/08d.png",
        "s08m": "images/png/08m.png",
        "s08n": "images/png/08n.png",
        "s09": "images/png/09.png",
        "s10": "images/png/10.png",
        "s11": "images/png/11.png",
        "s12": "images/png/12.png",
        "s13": "images/png/13.png",
        "s14": "images/png/14.png",
        "s15": "images/png/15.png",
        "s20d": "images/png/20d.png",
        "s20m": "images/png/20m.png",
        "s20n": "images/png/20n.png",
        "s21d": "images/png/21d.png",
        "s21m": "images/png/21m.png",
        "s21n": "images/png/21n.png",
        "s22": "images/png/22.png",
        "s23": "images/png/23.png",
        "s24d": "images/png/24d.png",
        "s24m": "images/png/24m.png",
        "s24n": "images/png/24n.png",
        "s25d": "images/png/25d.png",
        "s25m": "images/png/25m.png",
        "s25n": "images/png/25n.png",
        "s26d": "images/png/26d.png",
        "s26m": "images/png/26m.png",
        "s26n": "images/png/26n.png",
        "s27d": "images/png/27d.png",
        "s27m": "images/png/27m.png",
        "s27n": "images/png/27n.png",
        "s28d": "images/png/28d.png",
        "s28m": "images/png/28m.png",
        "s28n": "images/png/28n.png",
        "s29d": "images/png/29d.png",
        "s29m": "images/png/29m.png",
        "s29n": "images/png/29n.png",
        "s30": "images/png/30.png",
        "s31": "images/png/31.png",
        "s32": "images/png/32.png",
        "s33": "images/png/33.png",
        "s34": "images/png/34.png",
        "s40d": "images/png/40d.png",
        "s40m": "images/png/40m.png",
        "s40n": "images/png/40n.png",
        "s41d": "images/png/41d.png",
        "s41m": "images/png/41m.png",
        "s41n": "images/png/41n.png",
        "s42d": "images/png/42d.png",
        "s42m": "images/png/42m.png",
        "s42n": "images/png/42n.png",
        "s43d": "images/png/43d.png",
        "s43m": "images/png/43m.png",
        "s43n": "images/png/43n.png",
        "s44d": "images/png/44d.png",
        "s44m": "images/png/44m.png",
        "s44n": "images/png/44n.png",
        "s45d": "images/png/45d.png",
        "s45m": "images/png/45m.png",
        "s45n": "images/png/45n.png",
        "s46": "images/png/46.png",
        "s47": "images/png/47.png",
        "s48": "images/png/48.png",
        "s49": "images/png/49.png",
        "s50": "images/png/50.png"
        },
    "raw": {
        "sample": "tests/oslo.xml"
        },
    "string": {
        "version": "1.0.0"
        },
    "values": {
        "symbols": symbols,
        "place_names": place_names,
        "places": places,
        # Store the resource IDs that will be allocated for each of the above
        # images in a list that can be accessed at run time. This can be
        # cross-referenced with the symbols list because resources are sorted
        # by their keys before being encoded in the application's resources.
        "resourceIDs": map(lambda x: 0x7f010000 | (x + 1), range(len(symbols)))
        }
    }

code_file = "src/weatherforecast.py"
include_paths = []
layout = None
features = []
permissions = ["android.permission.INTERNET",
               "android.permission.READ_EXTERNAL_STORAGE",
               "android.permission.WRITE_EXTERNAL_STORAGE"]
options = {"pngquant": "-f 32"}

if __name__ == "__main__":

    args = sys.argv[:]
    
    result = buildhelper.main(__file__, app_name, package_name, res_files,
        layout, code_file, include_paths, features, permissions, args,
        include_sources = False, options = options)
    
    sys.exit(result)
