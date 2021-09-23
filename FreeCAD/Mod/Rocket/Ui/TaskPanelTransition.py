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
"""Class for drawing transitions"""

__title__ = "FreeCAD Transitions"
__author__ = "David Carter"
__url__ = "https://www.davesrocketshop.com"
    

import FreeCAD
import FreeCADGui

from PySide import QtGui, QtCore
from PySide2.QtWidgets import QDialog, QGridLayout

from DraftTools import translate

from Ui.TaskPanelDatabase import TaskPanelDatabase
from App.Constants import TYPE_CONE, TYPE_ELLIPTICAL, TYPE_HAACK, TYPE_OGIVE, TYPE_VON_KARMAN, TYPE_PARABOLA, TYPE_PARABOLIC, TYPE_POWER
from App.Constants import STYLE_CAPPED, STYLE_HOLLOW, STYLE_SOLID, STYLE_SOLID_CORE
from App.Constants import COMPONENT_TYPE_TRANSITION

from App.Utilities import _toFloat, _valueWithUnits

class _TransitionDialog(QDialog):

    def __init__(self, parent=None):
        super(_TransitionDialog, self).__init__(parent)

        ui = FreeCADGui.UiLoader()

        # define our window
        self.setGeometry(250, 250, 400, 350)
        self.setWindowTitle(translate('Rocket', "Transition Parameter"))

        # Select the type of transition
        self.transitionTypeLabel = QtGui.QLabel(translate('Rocket', "Transition type"), self)

        self.transitionTypes = (TYPE_CONE,
                                TYPE_ELLIPTICAL,
                                TYPE_OGIVE,
                                TYPE_PARABOLA,
                                TYPE_PARABOLIC,
                                TYPE_POWER,
                                TYPE_VON_KARMAN,
                                TYPE_HAACK
                                )
        self.transitionTypesCombo = QtGui.QComboBox(self)
        self.transitionTypesCombo.addItems(self.transitionTypes)

        self.clippedLabel = QtGui.QLabel(translate('Rocket', "Clipped"), self)

        self.clippedCheckbox = QtGui.QCheckBox(self)
        self.clippedCheckbox.setCheckState(QtCore.Qt.Checked)
        # self.clippedCheckbox.setEnabled(False) # Not supported yet

        # Select the type of sketch
        self.transitionStyleLabel = QtGui.QLabel(translate('Rocket', "Transition Style"), self)

        self.transitionStyles = (STYLE_SOLID,
                                STYLE_SOLID_CORE,
                                STYLE_HOLLOW,
                                STYLE_CAPPED)
        self.transitionStylesCombo = QtGui.QComboBox(self)
        self.transitionStylesCombo.addItems(self.transitionStyles)

        # Get the transition parameters: length, width, etc...
        self.lengthLabel = QtGui.QLabel(translate('Rocket', "Length"), self)

        self.lengthInput = ui.createWidget("Gui::InputField")
        self.lengthInput.unit = 'mm'
        self.lengthInput.setFixedWidth(80)

        self.foreDiameterLabel = QtGui.QLabel(translate('Rocket', "Forward Diameter"), self)

        self.foreDiameterInput = ui.createWidget("Gui::InputField")
        self.foreDiameterInput.unit = 'mm'
        self.foreDiameterInput.setFixedWidth(80)

        self.aftDiameterLabel = QtGui.QLabel(translate('Rocket', "Aft Diameter"), self)

        self.aftDiameterInput = ui.createWidget("Gui::InputField")
        self.aftDiameterInput.unit = 'mm'
        self.aftDiameterInput.setFixedWidth(80)

        self.coreDiameterLabel = QtGui.QLabel(translate('Rocket', "Core Diameter"), self)

        self.coreDiameterInput = ui.createWidget("Gui::InputField")
        self.coreDiameterInput.unit = 'mm'
        self.coreDiameterInput.setFixedWidth(80)

        self.thicknessLabel = QtGui.QLabel(translate('Rocket', "Thickness"), self)

        self.thicknessInput = ui.createWidget("Gui::InputField")
        self.thicknessInput.unit = 'mm'
        self.thicknessInput.setFixedWidth(80)

        self.coefficientLabel = QtGui.QLabel(translate('Rocket', "Coefficient"), self)

        self.coefficientValidator = QtGui.QDoubleValidator(self)
        self.coefficientValidator.setBottom(0.0)

        self.coefficientInput = QtGui.QLineEdit(self)
        self.coefficientInput.setFixedWidth(100)
        self.coefficientInput.setValidator(self.coefficientValidator)
        self.coefficientInput.setEnabled(False)

        self.foreShoulderLabel = QtGui.QLabel(translate('Rocket', "Forward Shoulder"), self)

        self.foreShoulderCheckbox = QtGui.QCheckBox(self)
        self.foreShoulderCheckbox.setCheckState(QtCore.Qt.Checked)

        self.foreShoulderDiameterLabel = QtGui.QLabel(translate('Rocket', "Diameter"), self)

        self.foreShoulderDiameterInput = ui.createWidget("Gui::InputField")
        self.foreShoulderDiameterInput.unit = 'mm'
        self.foreShoulderDiameterInput.setFixedWidth(80)

        self.foreShoulderLengthLabel = QtGui.QLabel(translate('Rocket', "Length"), self)

        self.foreShoulderLengthInput = ui.createWidget("Gui::InputField")
        self.foreShoulderLengthInput.unit = 'mm'
        self.foreShoulderLengthInput.setFixedWidth(80)

        self.foreShoulderThicknessLabel = QtGui.QLabel(translate('Rocket', "Thickness"), self)

        self.foreShoulderThicknessInput = ui.createWidget("Gui::InputField")
        self.foreShoulderThicknessInput.unit = 'mm'
        self.foreShoulderThicknessInput.setFixedWidth(80)

        self.aftShoulderLabel = QtGui.QLabel(translate('Rocket', "Aft Shoulder"), self)

        self.aftShoulderCheckbox = QtGui.QCheckBox(self)
        self.aftShoulderCheckbox.setCheckState(QtCore.Qt.Checked)

        self.aftShoulderDiameterLabel = QtGui.QLabel(translate('Rocket', "Diameter"), self)

        self.aftShoulderDiameterInput = ui.createWidget("Gui::InputField")
        self.aftShoulderDiameterInput.unit = 'mm'
        self.aftShoulderDiameterInput.setFixedWidth(80)

        self.aftShoulderLengthLabel = QtGui.QLabel(translate('Rocket', "Length"), self)

        self.aftShoulderLengthInput = ui.createWidget("Gui::InputField")
        self.aftShoulderLengthInput.unit = 'mm'
        self.aftShoulderLengthInput.setFixedWidth(80)

        self.aftShoulderThicknessLabel = QtGui.QLabel(translate('Rocket', "Thickness"), self)

        self.aftShoulderThicknessInput = ui.createWidget("Gui::InputField")
        self.aftShoulderThicknessInput.unit = 'mm'
        self.aftShoulderThicknessInput.setFixedWidth(80)

        row = 0
        layout = QGridLayout()

        layout.addWidget(self.transitionTypeLabel, row, 0, 1, 2)
        layout.addWidget(self.transitionTypesCombo, row, 1)
        row += 1

        layout.addWidget(self.transitionStyleLabel, row, 0)
        layout.addWidget(self.transitionStylesCombo, row, 1)
        row += 1

        layout.addWidget(self.lengthLabel, row, 0)
        layout.addWidget(self.lengthInput, row, 1)
        row += 1

        layout.addWidget(self.clippedLabel, row, 0)
        layout.addWidget(self.clippedCheckbox, row, 1)
        row += 1

        layout.addWidget(self.foreDiameterLabel, row, 0)
        layout.addWidget(self.foreDiameterInput, row, 1)
        row += 1

        layout.addWidget(self.aftDiameterLabel, row, 0)
        layout.addWidget(self.aftDiameterInput, row, 1)
        row += 1

        layout.addWidget(self.coreDiameterLabel, row, 0)
        layout.addWidget(self.coreDiameterInput, row, 1)
        row += 1

        layout.addWidget(self.thicknessLabel, row, 0)
        layout.addWidget(self.thicknessInput, row, 1)
        row += 1

        layout.addWidget(self.coefficientLabel, row, 0)
        layout.addWidget(self.coefficientInput, row, 1)
        row += 1

        layout.addWidget(self.foreShoulderLabel, row, 0)
        layout.addWidget(self.foreShoulderCheckbox, row, 1)
        row += 1

        layout.addWidget(self.foreShoulderLengthLabel, row, 1)
        layout.addWidget(self.foreShoulderLengthInput, row, 2)
        row += 1

        layout.addWidget(self.foreShoulderDiameterLabel, row, 1)
        layout.addWidget(self.foreShoulderDiameterInput, row, 2)
        row += 1

        layout.addWidget(self.foreShoulderThicknessLabel, row, 1)
        layout.addWidget(self.foreShoulderThicknessInput, row, 2)
        row += 1

        layout.addWidget(self.aftShoulderLabel, row, 0)
        layout.addWidget(self.aftShoulderCheckbox, row, 1)
        row += 1

        layout.addWidget(self.aftShoulderLengthLabel, row, 1)
        layout.addWidget(self.aftShoulderLengthInput, row, 2)
        row += 1

        layout.addWidget(self.aftShoulderDiameterLabel, row, 1)
        layout.addWidget(self.aftShoulderDiameterInput, row, 2)
        row += 1

        layout.addWidget(self.aftShoulderThicknessLabel, row, 1)
        layout.addWidget(self.aftShoulderThicknessInput, row, 2)
        row += 1

        self.setLayout(layout)


class TaskPanelTransition:

    def __init__(self,obj,mode):
        self._obj = obj
        
        self._tranForm = _TransitionDialog()
        self._db = TaskPanelDatabase(obj, COMPONENT_TYPE_TRANSITION)
        self._dbForm = self._db.getForm()

        self.form = [self._tranForm, self._dbForm]
        self._tranForm.setWindowIcon(QtGui.QIcon(FreeCAD.getUserAppDataDir() + "Mod/Rocket/Resources/icons/Rocket_Transition.svg"))
        
        self._tranForm.transitionTypesCombo.currentTextChanged.connect(self.onTransitionType)
        self._tranForm.transitionStylesCombo.currentTextChanged.connect(self.onTransitionStyle)
        self._tranForm.lengthInput.textEdited.connect(self.onLength)
        self._tranForm.foreDiameterInput.textEdited.connect(self.onForeDiameter)
        self._tranForm.aftDiameterInput.textEdited.connect(self.onAftDiameter)
        self._tranForm.coreDiameterInput.textEdited.connect(self.onCoreDiameter)
        self._tranForm.thicknessInput.textEdited.connect(self.onThickness)
        self._tranForm.coefficientInput.textEdited.connect(self.onCoefficient)
        self._tranForm.clippedCheckbox.stateChanged.connect(self.onClipped)
        self._tranForm.foreShoulderCheckbox.stateChanged.connect(self.onForeShoulder)
        self._tranForm.foreShoulderDiameterInput.textEdited.connect(self.onForeShoulderDiameter)
        self._tranForm.foreShoulderLengthInput.textEdited.connect(self.onForeShoulderLength)
        self._tranForm.foreShoulderThicknessInput.textEdited.connect(self.onForeShoulderThickness)
        self._tranForm.aftShoulderCheckbox.stateChanged.connect(self.onAftShoulder)
        self._tranForm.aftShoulderDiameterInput.textEdited.connect(self.onAftShoulderDiameter)
        self._tranForm.aftShoulderLengthInput.textEdited.connect(self.onAftShoulderLength)
        self._tranForm.aftShoulderThicknessInput.textEdited.connect(self.onAftShoulderThickness)

        self._db.dbLoad.connect(self.onLookup)
        
        self.update()
        
        if mode == 0: # fresh created
            self._obj.Proxy.execute(self._obj)  # calculate once 
            FreeCAD.Gui.SendMsgToActiveView("ViewFit")
        
    def transferTo(self):
        "Transfer from the dialog to the object" 
        self._obj.TransitionType = str(self._tranForm.transitionTypesCombo.currentText())
        self._obj.TransitionStyle = str(self._tranForm.transitionStylesCombo.currentText())
        self._obj.Length = self._tranForm.lengthInput.text()
        self._obj.ForeDiameter = self._tranForm.foreDiameterInput.text()
        self._obj.AftDiameter = self._tranForm.aftDiameterInput.text()
        self._obj.CoreDiameter = self._tranForm.coreDiameterInput.text()
        self._obj.Thickness = self._tranForm.thicknessInput.text()
        self._obj.Coefficient = _toFloat(self._tranForm.coefficientInput.text())
        self._obj.Clipped = self._tranForm.clippedCheckbox.isChecked()
        self._obj.ForeShoulder = self._tranForm.foreShoulderCheckbox.isChecked()
        self._obj.ForeShoulderDiameter = self._tranForm.foreShoulderDiameterInput.text()
        self._obj.ForeShoulderLength =self._tranForm.foreShoulderLengthInput.text()
        self._obj.ForeShoulderThickness = self._tranForm.foreShoulderThicknessInput.text()
        self._obj.AftShoulder = self._tranForm.aftShoulderCheckbox.isChecked()
        self._obj.AftShoulderDiameter = self._tranForm.aftShoulderDiameterInput.text()
        self._obj.AftShoulderLength = self._tranForm.aftShoulderLengthInput.text()
        self._obj.AftShoulderThickness =self._tranForm.aftShoulderThicknessInput.text()

    def transferFrom(self):
        "Transfer from the object to the dialog"
        self._tranForm.transitionTypesCombo.setCurrentText(self._obj.TransitionType)
        self._tranForm.transitionStylesCombo.setCurrentText(self._obj.TransitionStyle)
        self._tranForm.lengthInput.setText(self._obj.Length.UserString)
        self._tranForm.foreDiameterInput.setText(self._obj.ForeDiameter.UserString)
        self._tranForm.aftDiameterInput.setText(self._obj.AftDiameter.UserString)
        self._tranForm.coreDiameterInput.setText(self._obj.CoreDiameter.UserString)
        self._tranForm.thicknessInput.setText(self._obj.Thickness.UserString)
        self._tranForm.coefficientInput.setText("%f" % self._obj.Coefficient)
        self._tranForm.clippedCheckbox.setChecked(self._obj.Clipped)
        self._tranForm.foreShoulderCheckbox.setChecked(self._obj.ForeShoulder)
        self._tranForm.foreShoulderDiameterInput.setText(self._obj.ForeShoulderDiameter.UserString)
        self._tranForm.foreShoulderLengthInput.setText(self._obj.ForeShoulderLength.UserString)
        self._tranForm.foreShoulderThicknessInput.setText(self._obj.ForeShoulderThickness.UserString)
        self._tranForm.aftShoulderCheckbox.setChecked(self._obj.AftShoulder)
        self._tranForm.aftShoulderDiameterInput.setText(self._obj.AftShoulderDiameter.UserString)
        self._tranForm.aftShoulderLengthInput.setText(self._obj.AftShoulderLength.UserString)
        self._tranForm.aftShoulderThicknessInput.setText(self._obj.AftShoulderThickness.UserString)

        self._showTransitionType()
        self._showClippable()
        self._showTransitionStyle()

    def _showClippable(self):
        if str(self._obj.TransitionType) in [TYPE_CONE, TYPE_OGIVE]:
            # These types aren't clippable
            self._obj.Clipped = False
            self._tranForm.clippedCheckbox.setChecked(self._obj.Clipped)
            self._tranForm.clippedCheckbox.setEnabled(False)
        else:
            self._tranForm.clippedCheckbox.setEnabled(True)
        
        
    def _showTransitionType(self):
        value = self._obj.TransitionType
        if value == TYPE_HAACK or value == TYPE_PARABOLIC:
            self._tranForm.coefficientInput.setEnabled(True)
        elif value == TYPE_POWER:
            self._tranForm.coefficientInput.setEnabled(True)
        elif value == TYPE_PARABOLA:
            # Set the coefficient, but don't enable it
            self._obj.Coefficient = 0.5
            self._tranForm.coefficientInput.setText("%f" % self._obj.Coefficient)
            self._tranForm.coefficientInput.setEnabled(False)
        elif value == TYPE_VON_KARMAN:
            # Set the coefficient, but don't enable it
            self._obj.Coefficient = 0.0
            self._tranForm.coefficientInput.setText("%f" % self._obj.Coefficient)
            self._tranForm.coefficientInput.setEnabled(False)
        else:
            self._tranForm.coefficientInput.setEnabled(False)
        
    def onTransitionType(self, value):
        self._obj.TransitionType = value

        self._showTransitionType()
        self._showClippable()

        self._obj.Proxy.execute(self._obj)
        
    def _showTransitionStyle(self):
        value = self._obj.TransitionStyle
        if value == STYLE_HOLLOW or value == STYLE_CAPPED:
            self._tranForm.thicknessInput.setEnabled(True)
            self._tranForm.coreDiameterInput.setEnabled(False)

            if self._tranForm.foreShoulderCheckbox.isChecked():
                self._tranForm.foreShoulderThicknessInput.setEnabled(True)
            else:
                self._tranForm.foreShoulderThicknessInput.setEnabled(False)

            if self._tranForm.aftShoulderCheckbox.isChecked():
                self._tranForm.aftShoulderThicknessInput.setEnabled(True)
            else:
                self._tranForm.aftShoulderThicknessInput.setEnabled(False)
        elif value == STYLE_SOLID_CORE:
            self._tranForm.thicknessInput.setEnabled(False)
            self._tranForm.coreDiameterInput.setEnabled(True)

            self._tranForm.foreShoulderThicknessInput.setEnabled(False)
            self._tranForm.aftShoulderThicknessInput.setEnabled(False)
        else:
            self._tranForm.thicknessInput.setEnabled(False)
            self._tranForm.coreDiameterInput.setEnabled(False)

            self._tranForm.foreShoulderThicknessInput.setEnabled(False)
            self._tranForm.aftShoulderThicknessInput.setEnabled(False)

        
    def onTransitionStyle(self, value):
        self._obj.TransitionStyle = value

        self._showTransitionStyle()
        self._obj.Proxy.execute(self._obj)
        
    def onLength(self, value):
        try:
            self._obj.Length = FreeCAD.Units.Quantity(value).Value
            self._obj.Proxy.execute(self._obj)
        except ValueError:
            pass
        
    def onForeDiameter(self, value):
        try:
            self._obj.ForeDiameter = FreeCAD.Units.Quantity(value).Value
            self._obj.Proxy.execute(self._obj)
        except ValueError:
            pass
        
    def onAftDiameter(self, value):
        try:
            self._obj.AftDiameter = FreeCAD.Units.Quantity(value).Value
            self._obj.Proxy.execute(self._obj)
        except ValueError:
            pass
        
    def onCoreDiameter(self, value):
        try:
            self._obj.CoreDiameter = FreeCAD.Units.Quantity(value).Value
            self._obj.Proxy.execute(self._obj)
        except ValueError:
            pass
        
    def onThickness(self, value):
        try:
            self._obj.Thickness = FreeCAD.Units.Quantity(value).Value
            self._obj.Proxy.execute(self._obj)
        except ValueError:
            pass
        
    def onCoefficient(self, value):
        self._obj.Coefficient = _toFloat(value)
        self._obj.Proxy.execute(self._obj)
        
    def onClipped(self, value):
        self._obj.Clipped = self._tranForm.clippedCheckbox.isChecked()
        self._obj.Proxy.execute(self._obj)
        
    def onForeShoulder(self, value):
        self._obj.ForeShoulder = self._tranForm.foreShoulderCheckbox.isChecked()
        if self._obj.ForeShoulder:
            self._tranForm.foreShoulderDiameterInput.setEnabled(True)
            self._tranForm.foreShoulderLengthInput.setEnabled(True)

            selectedText = self._tranForm.transitionStylesCombo.currentText()
            if selectedText == STYLE_HOLLOW or selectedText == STYLE_CAPPED:
                self._tranForm.foreShoulderThicknessInput.setEnabled(True)
            else:
                self._tranForm.foreShoulderThicknessInput.setEnabled(False)
        else:
            self._tranForm.foreShoulderDiameterInput.setEnabled(False)
            self._tranForm.foreShoulderLengthInput.setEnabled(False)
            self._tranForm.foreShoulderThicknessInput.setEnabled(False)

        self._obj.Proxy.execute(self._obj)
        
    def onForeShoulderDiameter(self, value):
        try:
            self._obj.ForeShoulderDiameter = FreeCAD.Units.Quantity(value).Value
            self._obj.Proxy.execute(self._obj)
        except ValueError:
            pass
        
    def onForeShoulderLength(self, value):
        try:
            self._obj.ForeShoulderLength = FreeCAD.Units.Quantity(value).Value
            self._obj.Proxy.execute(self._obj)
        except ValueError:
            pass
        
    def onForeShoulderThickness(self, value):
        try:
            self._obj.ForeShoulderThickness = FreeCAD.Units.Quantity(value).Value
            self._obj.Proxy.execute(self._obj)
        except ValueError:
            pass
        
    def onAftShoulder(self, value):
        self._obj.AftShoulder = self._tranForm.aftShoulderCheckbox.isChecked()
        if self._obj.AftShoulder:
            self._tranForm.aftShoulderDiameterInput.setEnabled(True)
            self._tranForm.aftShoulderLengthInput.setEnabled(True)

            selectedText = self._tranForm.transitionStylesCombo.currentText()
            if selectedText == STYLE_HOLLOW or selectedText == STYLE_CAPPED:
                self._tranForm.aftShoulderThicknessInput.setEnabled(True)
            else:
                self._tranForm.aftShoulderThicknessInput.setEnabled(False)
        else:
            self._tranForm.aftShoulderDiameterInput.setEnabled(False)
            self._tranForm.aftShoulderLengthInput.setEnabled(False)
            self._tranForm.aftShoulderThicknessInput.setEnabled(False)

        self._obj.Proxy.execute(self._obj)
        
    def onAftShoulderDiameter(self, value):
        try:
            self._obj.AftShoulderDiameter = FreeCAD.Units.Quantity(value).Value
            self._obj.Proxy.execute(self._obj)
        except ValueError:
            pass
        
    def onAftShoulderLength(self, value):
        try:
            self._obj.AftShoulderLength = FreeCAD.Units.Quantity(value).Value
            self._obj.Proxy.execute(self._obj)
        except ValueError:
            pass
        
    def onAftShoulderThickness(self, value):
        try:
            self._obj.AftShoulderThickness = FreeCAD.Units.Quantity(value).Value
            self._obj.Proxy.execute(self._obj)
        except ValueError:
            pass
        
    def onLookup(self):
        result = self._db.getLookupResult()

        self._obj.TransitionType = str(result["shape"])
        self._obj.TransitionStyle = str(result["style"])
        self._obj.Length = _valueWithUnits(result["length"], result["length_units"])
        self._obj.ForeDiameter = _valueWithUnits(result["fore_outside_diameter"], result["fore_outside_diameter_units"])
        self._obj.AftDiameter = _valueWithUnits(result["aft_outside_diameter"], result["aft_outside_diameter_units"])
        self._obj.CoreDiameter = 0.0
        self._obj.Thickness = _valueWithUnits(result["thickness"], result["thickness_units"])
        self._obj.Coefficient = 0.0
        self._obj.Clipped = True
        self._obj.ForeShoulderDiameter = _valueWithUnits(result["fore_shoulder_diameter"], result["fore_shoulder_diameter_units"])
        self._obj.ForeShoulderLength = _valueWithUnits(result["fore_shoulder_length"], result["fore_shoulder_length_units"])
        self._obj.ForeShoulderThickness = self._obj.Thickness
        self._obj.AftShoulderDiameter = _valueWithUnits(result["aft_shoulder_diameter"], result["aft_shoulder_diameter_units"])
        self._obj.AftShoulderLength = _valueWithUnits(result["aft_shoulder_length"], result["aft_shoulder_length_units"])
        self._obj.AftShoulderThickness = self._obj.Thickness

        self._obj.ForeShoulder = (self._obj.ForeShoulderDiameter > 0.0) and (self._obj.ForeShoulderLength >= 0)
        self._obj.AftShoulder = (self._obj.AftShoulderDiameter > 0.0) and (self._obj.AftShoulderLength >= 0)

        self.update()
        self._obj.Proxy.execute(self._obj) 
        
    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok) | int(QtGui.QDialogButtonBox.Cancel)| int(QtGui.QDialogButtonBox.Apply)

    def clicked(self,button):
        if button == QtGui.QDialogButtonBox.Apply:
            #print "Apply"
            self.transferTo()
            self._obj.Proxy.execute(self._obj) 
        
    def update(self):
        'fills the widgets'
        self.transferFrom()
                
    def accept(self):
        self.transferTo()
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.ActiveDocument.resetEdit()
        
                    
    def reject(self):
        FreeCAD.ActiveDocument.abortTransaction()
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.ActiveDocument.resetEdit()
