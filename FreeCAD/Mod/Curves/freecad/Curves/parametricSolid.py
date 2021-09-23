# -*- coding: utf-8 -*-

__title__ = "Parametric solid"
__author__ = "Christophe Grellier (Chris_G)"
__license__ = "LGPL 2.1"
__doc__ = "Make a parametric solid from selected faces."
__usage__ = """Select some faces in the 3D View, or select objects in the Tree View.
Activate tool.
It will try to build a solid from selected faces.
If not possible, it falls back to a shell, then to a compound.
The ShapeStatus property (and the color of the icon) give the type of shape."""

import os
import FreeCAD
import FreeCADGui
import Part
import tempfile

from PySide import QtGui

from freecad.Curves import _utils
from freecad.Curves import ICONPATH

TOOL_ICON = os.path.join(ICONPATH, 'solid.svg')


def get_svg(shape_type):
    colors = {"": "ffffff",
              "Compound": "ff0000",
              "Shell": "ff7b00",
              "Solid": "00ff00"}
    return '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   version="1.1"
   height="51.200001"
   width="51.200001">
  <path
     id="ColorBackground"
     style="fill:#{};fill-rule:evenodd;stroke:none;stroke-width:1.05624831px;stroke-linecap:butt;stroke-linejoin:bevel;stroke-opacity:1;fill-opacity:1"
     d="M 27.7265 3.543 L 5.3847656 16.525391 L 5.3847656 36.689453 L 24.490234 47.876953 L 46.832031 34.894531 L 46.832031 14.730469 L 27.726562 3.543 z " />
  <path
     style="fill:#000000;fill-rule:evenodd;stroke:#000000;stroke-width:1.05624831px;stroke-linecap:butt;stroke-linejoin:bevel;stroke-opacity:1;fill-opacity:0.50"
     d="M 5.3848898,16.525959 V 36.689551 L 24.490848,47.876201 L 24.490847,27.7126 Z"
     id="Face1" />
  <path
     style="fill:#000000;fill-rule:evenodd;stroke:#000000;stroke-width:1.05624831px;stroke-linecap:butt;stroke-linejoin:bevel;stroke-opacity:1;fill-opacity:0.64"
     d="M 46.832491,14.73057 L 24.490847,27.7126 L 24.490848,47.876201 L 46.832492,34.894162 L 46.832491,14.73057"
     id="Face2" />
  <path
     style="fill:#000000;fill-rule:evenodd;stroke:#000000;stroke-width:1.05624831px;stroke-linecap:butt;stroke-linejoin:bevel;stroke-opacity:1;fill-opacity:0.26"
     d="M 5.3848898,16.525959 L 27.7265,3.5439198 L 46.832491,14.73057 L 24.490847,27.7126 Z"
     id="Face3" />
</svg>'''.format(colors[shape_type])


class solid:
    """Make a parametric solid from selected faces"""
    def __init__(self, obj):
        obj.addProperty("App::PropertyLinkSubList",
                        "Faces",
                        "Solid",
                        "List of faces to build the solid")
        obj.addProperty("App::PropertyString",
                        "ShapeStatus",
                        "Solid",
                        "Status of the created shape")
        obj.ShapeStatus = ""
        obj.setEditorMode("ShapeStatus", 1)
        obj.Proxy = self

    def execute(self, obj):
        faces = _utils.getShape(obj, "Faces", "Face")
        shape = Part.Compound(faces)
        try:
            shell = Part.Shell(shape.Faces)
            if shell.isValid():
                shape = shell
        except Part.OCCError:
            pass
        try:
            solid = Part.Solid(shape)
            if solid.isValid():
                shape = solid
        except Part.OCCError:
            pass
        if isinstance(shape, Part.Solid):  # and shape.isValid():
            obj.ShapeStatus = "Solid"
        elif isinstance(shape, Part.Shell):  # and shape.isValid():
            obj.ShapeStatus = "Shell"
        else:
            obj.ShapeStatus = "Compound"
        obj.Shape = shape

    def onDocumentRestored(self, fp):
        fp.setEditorMode("ShapeStatus", 1)


class solidVP:
    def __init__(self, vobj):
        vobj.Proxy = self

    def getIcon(self):
        if not hasattr(self, "icons"):
            self.icons = dict()
            for sht in ["", "Compound", "Shell", "Solid"]:
                iconFile = tempfile.NamedTemporaryFile(suffix=".svg", delete=False)
                iconFile.write(bytes(get_svg(sht), "utf8"))
                iconFile.close()
                self.icons[sht] = QtGui.QIcon(iconFile.name)
        return self.icons[self.Object.ShapeStatus]

    def attach(self, vobj):
        self.Object = vobj.Object

    def updateData(self, fp, prop):
        if prop == "ShapeStatus":
            fp.ViewObject.signalChangeIcon()

    def __getstate__(self):
        return {"name": self.Object.Name}

    def __setstate__(self, state):
        self.Object = FreeCAD.ActiveDocument.getObject(state["name"])
        return None


class solidCommand:
    """Make a parametric solid from selected faces"""
    def makeSolidFeature(self, source):
        solidFP = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",
                                                   "Solid")
        solid(solidFP)
        solidVP(solidFP.ViewObject)
        solidFP.Faces = source
        FreeCAD.ActiveDocument.recompute()

    def Activated(self):
        faces = []
        sel = FreeCADGui.Selection.getSelectionEx()
        if sel == []:
            FreeCAD.Console.PrintError("{} :\n{}\n".format(__title__, __usage__))
        for selobj in sel:
            if selobj.HasSubObjects:
                for i in range(len(selobj.SubObjects)):
                    if isinstance(selobj.SubObjects[i], Part.Face):
                        faces.append((selobj.Object,
                                      selobj.SubElementNames[i]))
            elif selobj.Object.Shape.Faces:
                for i in range(len(selobj.Object.Shape.Faces)):
                    faces.append((selobj.Object, "Face{}".format(i + 1)))
                selobj.Object.ViewObject.Visibility = False
        if faces:
            self.makeSolidFeature(faces)

    def IsActive(self):
        if FreeCAD.ActiveDocument:
            return True
        else:
            return False

    def GetResources(self):
        return {'Pixmap': TOOL_ICON,
                'MenuText': __title__,
                'ToolTip': "{}\n\n{}\n\n{}".format(__title__, __doc__, __usage__)}


FreeCADGui.addCommand('solid', solidCommand())
