# ***************************************************************************
# *   Copyright (c) 2021 David Carter <dcarter@davidcarter.ca>              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************
"""Rocket Workbench Constants"""

__title__ = "FreeCAD Rocket Workbench Constants"
__author__ = "David Carter"
__url__ = "https://www.davesrocketshop.com"
    
# Part styles
STYLE_SOLID = "solid"
STYLE_SOLID_CORE = "solid core" # Used by transitions, not nose cones
STYLE_HOLLOW = "hollow"
STYLE_CAPPED = "capped"

# Part shapes
TYPE_CONE = "cone"
TYPE_ELLIPTICAL = "elliptical"
TYPE_OGIVE = "ogive"
TYPE_PARABOLA = "parabola"
TYPE_VON_KARMAN = "Von Karman"
TYPE_PARABOLIC = "parabolic series"
TYPE_POWER = "power series"
TYPE_HAACK = "Haack series"

# Fin types
FIN_TYPE_TRAPEZOID = "trapezoid"
FIN_TYPE_ELLIPSE = "elliptical"
FIN_TYPE_TUBE = "tube"
FIN_TYPE_SKETCH = "custom"

# Fin cross sections
FIN_CROSS_SAME = "Same as root"
FIN_CROSS_SQUARE = "square"
FIN_CROSS_ROUND = "round"
FIN_CROSS_AIRFOIL = "airfoil"
FIN_CROSS_WEDGE = "wedge"
FIN_CROSS_DIAMOND = "diamond"
FIN_CROSS_TAPER_LE = "LE taper"
FIN_CROSS_TAPER_TE = "TE taper"
FIN_CROSS_TAPER_LETE = "taper"

# Part material types
MATERIAL_TYPE_BULK = "BULK"
MATERIAL_TYPE_SURFACE = "SURFACE"
MATERIAL_TYPE_LINE = "LINE"

# Components in the database
COMPONENT_TYPE_ANY = "Any"
COMPONENT_TYPE_BODYTUBE = "Body Tube"
COMPONENT_TYPE_BULKHEAD = "Bulkhead"
COMPONENT_TYPE_CENTERINGRING = "Centering Ring"
COMPONENT_TYPE_COUPLER = "Tube Coupler"
COMPONENT_TYPE_ENGINEBLOCK = "Engine Block"
COMPONENT_TYPE_LAUNCHLUG = "Launch Lug"
COMPONENT_TYPE_NOSECONE = "Nose Cone"
COMPONENT_TYPE_PARACHUTE = "Parachute"
COMPONENT_TYPE_STREAMER = "Streamer"
COMPONENT_TYPE_TRANSITION = "Transition"
