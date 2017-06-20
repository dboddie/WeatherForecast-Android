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
res_files = {"drawable": {"ic_launcher": "icon.svg"},
             "raw": {"sample": "forecast.xml"}}
code_file = "weatherforecast.py"
include_paths = []
layout = None
features = []
permissions = []

if __name__ == "__main__":

    args = sys.argv[:]
    
    result = buildhelper.main(__file__, app_name, package_name, res_files,
        layout, code_file, include_paths, features, permissions, args,
        include_sources = False)
    
    sys.exit(result)
