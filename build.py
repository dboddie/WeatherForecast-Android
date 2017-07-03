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

import os, sys

from Tools import buildhelper

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

res_files = {
    "drawable": {
        "ic_launcher": "icon.svg",
        "s01d": "images/01d.svg",
        "s01m": "images/01m.svg",
        "s01n": "images/01n.svg",
        "s02d": "images/02d.svg",
        "s02m": "images/02m.svg",
        "s02n": "images/02n.svg",
        "s03d": "images/03d.svg",
        "s03m": "images/03m.svg",
        "s03n": "images/03n.svg",
        "s04": "images/04.svg",
        "s05d": "images/05d.svg",
        "s05m": "images/05m.svg",
        "s05n": "images/05n.svg",
        "s06d": "images/06d.svg",
        "s06m": "images/06m.svg",
        "s06n": "images/06n.svg",
        "s07d": "images/07d.svg",
        "s07m": "images/07m.svg",
        "s07n": "images/07n.svg",
        "s08d": "images/08d.svg",
        "s08m": "images/08m.svg",
        "s08n": "images/08n.svg",
        "s09": "images/09.svg",
        "s10": "images/10.svg",
        "s11": "images/11.svg",
        "s12": "images/12.svg",
        "s13": "images/13.svg",
        "s14": "images/14.svg",
        "s15": "images/15.svg",
        "s20d": "images/20d.svg",
        "s20m": "images/20m.svg",
        "s20n": "images/20n.svg",
        "s21d": "images/21d.svg",
        "s21m": "images/21m.svg",
        "s21n": "images/21n.svg",
        "s22": "images/22.svg",
        "s23": "images/23.svg",
        "s24d": "images/24d.svg",
        "s24m": "images/24m.svg",
        "s24n": "images/24n.svg",
        "s25d": "images/25d.svg",
        "s25m": "images/25m.svg",
        "s25n": "images/25n.svg",
        "s26d": "images/26d.svg",
        "s26m": "images/26m.svg",
        "s26n": "images/26n.svg",
        "s27d": "images/27d.svg",
        "s27m": "images/27m.svg",
        "s27n": "images/27n.svg",
        "s28d": "images/28d.svg",
        "s28m": "images/28m.svg",
        "s28n": "images/28n.svg",
        "s29d": "images/29d.svg",
        "s29m": "images/29m.svg",
        "s29n": "images/29n.svg",
        "s30": "images/30.svg",
        "s31": "images/31.svg",
        "s32": "images/32.svg",
        "s33": "images/33.svg",
        "s34": "images/34.svg",
        "s40d": "images/40d.svg",
        "s40m": "images/40m.svg",
        "s40n": "images/40n.svg",
        "s41d": "images/41d.svg",
        "s41m": "images/41m.svg",
        "s41n": "images/41n.svg",
        "s42d": "images/42d.svg",
        "s42m": "images/42m.svg",
        "s42n": "images/42n.svg",
        "s43d": "images/43d.svg",
        "s43m": "images/43m.svg",
        "s43n": "images/43n.svg",
        "s44d": "images/44d.svg",
        "s44m": "images/44m.svg",
        "s44n": "images/44n.svg",
        "s45d": "images/45d.svg",
        "s45m": "images/45m.svg",
        "s45n": "images/45n.svg",
        "s46": "images/46.svg",
        "s47": "images/47.svg",
        "s48": "images/48.svg",
        "s49": "images/49.svg",
        "s50": "images/50.svg"
        },
    "raw": {
        "sample": "oslo.xml"
        },
    "values": {
        "symbols": symbols,
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
               "android.permission.READ_EXTERNAL_STORAGE"]

if __name__ == "__main__":

    args = sys.argv[:]
    
    result = buildhelper.main(__file__, app_name, package_name, res_files,
        layout, code_file, include_paths, features, permissions, args,
        include_sources = False)
    
    sys.exit(result)
