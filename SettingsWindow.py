import yaml
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QPushButton,QDialog,QFormLayout,QHBoxLayout,QCompleter,QLineEdit,QSlider,QLabel,QComboBox
from PyQt5.QtCore import  pyqtSignal, QObject,QRect,QEvent,Qt
from PyQt5.QtGui import QFontDatabase,QDoubleValidator
import sys
import os
import re
from Profiles import Profiles


class Communicate(QObject):
    closed = pyqtSignal(str) 

class SettingsWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,400,200)
        self.setWindowTitle("User Selection")
        self.currentUserSettings = Profiles.getCurrentUserSettings()
        self.initLayout()
        self.resetUserSettings()
        self.communicate = Communicate()
        
    ################ Initialization ################

    def initLayout(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.initUserDropdownMenu()
        self.initFontrgba()
        self.initFontSelector()
        self.initFontSizeSelector()
        self.buttonInit()      

    ################ Drop down menu ################
 
    def initUserDropdownMenu(self):
        '''Creates the user DropDownMenu, adds it to form layout and connects it to the required functions'''
        self.DropDownMenu = QComboBox()
        self.fillDropDownMenu()
        if Profiles.getCurrentUser() is not None:
            self.DropDownMenu.setCurrentText(Profiles.getCurrentUser())
        self.DropDownMenu.activated.connect(self.changedUser)
        self.layout.addWidget(self.DropDownMenu)
        self.DropDownMenu.installEventFilter(self) 
        
    def fillDropDownMenu(self):
        '''Populates the DropDownMenu'''
        self.DropDownMenu.clear()
        users = sorted(Profiles.getUserList())
        for user in users:
            self.DropDownMenu.addItem(user)
        self.DropDownMenu.addItem("Create New User")
        self.DropDownMenu.setEditable(True)
        if Profiles.getCurrentUser() is not None:
            self.DropDownMenu.setCurrentText(Profiles.getCurrentUser())
        self.updateText()

    def changedUser(self):
        '''Updates entire settings menu if user is changed'''
        self.updateText()
        self.resetUserSettings()
 
    def updateText(self):
        '''if create new user is selected enter editable mode'''
        self.DropDownMenu.setEditable(False)
        if self.DropDownMenu.currentText() == "Create New User":
            self.DropDownMenu.setEditable(True)
            self.DropDownMenu.setCurrentText("")
         
    ################ Deals with font colour ################ 

    def initFontrgba(self):
        '''Initializes font rgba sliders'''
         #adding fontrgba slider
        fontrgbSlidersBox = QHBoxLayout()
        self.fontRedSliderBox = self.generateSliderBox(0,255,self.updateSliderIndicators)
        fontrgbSlidersBox.addLayout(self.fontRedSliderBox)
        self.fontGreenSliderBox = self.generateSliderBox(0,255,self.updateSliderIndicators)
        fontrgbSlidersBox.addLayout(self.fontGreenSliderBox)
        self.fontBlueSliderBox = self.generateSliderBox(0,255,self.updateSliderIndicators)
        fontrgbSlidersBox.addLayout(self.fontBlueSliderBox)
        self.layout.addRow("Colour:",fontrgbSlidersBox)
        #adding font opacity slider
        self.fontOpacityBox = self.generateSliderBox(0,100,self.updateSliderIndicators)
        self.layout.addRow("Font Opacity: ",self.fontOpacityBox)
    
    def updateSliderIndicators(self):
        '''Updates the slider indicator and dictionary when a slider is moved'''
        r = self.fontRedSliderBox.itemAt(1).widget().value()
        g = self.fontGreenSliderBox.itemAt(1).widget().value()
        b = self.fontBlueSliderBox.itemAt(1).widget().value()
        a = self.fontOpacityBox.itemAt(1).widget().value() / 100
        self.fontrgbaDictionary(f"rgba({r},{g},{b},{a})")
        self.setFontRgbaSliders(f"rgba({r},{g},{b},{a})")
        self.saveQuitOff()

    def fontrgbaDictionary(self,value: str):
        '''Updates dictionary'''
        self.currentUserSettings['color']  = value
        self.saveQuitOff()

    def setFontRgbaSliders(self,value: str):
        '''sets fonts and and indicator to a given rgba value'''
        rgbaValues = re.findall(r'\d+[.]?\d*',self.currentUserSettings['color'])
        self.fontRedSliderBox.itemAt(1).widget().setValue(int(rgbaValues[0]))
        self.fontRedSliderBox.itemAt(0).widget().setText(rgbaValues[0])
        self.fontGreenSliderBox.itemAt(1).widget().setValue(int(rgbaValues[1]))
        self.fontGreenSliderBox.itemAt(0).widget().setText(rgbaValues[1])
        self.fontBlueSliderBox.itemAt(1).widget().setValue(int(rgbaValues[2]))
        self.fontBlueSliderBox.itemAt(0).widget().setText(rgbaValues[2])
        self.fontOpacityBox.itemAt(1).widget().setValue(int(float(rgbaValues[3]) * 100))
        self.fontOpacityBox.itemAt(0).widget().setText(rgbaValues[3])


    ################ Font Selector ################

    def initFontSelector(self):
        availableFonts = QFontDatabase().families()
        fontCompleter = QCompleter(availableFonts)
        fontCompleter.setCaseSensitivity(False)
        self.fontSelector = QLineEdit("")
        self.fontSelector.setCompleter(fontCompleter)
        self.fontSelector.textChanged.connect(self.fontSelectorDictionary)
        self.layout.addRow("Font:" ,self.fontSelector)

    def fontSelectorDictionary(self):
        if self.fontSelector.text() in QFontDatabase().families():
            self.currentUserSettings['font-family'] = self.fontSelector.text()
        self.saveQuitOff()
    
    ################ Font Size Selector ################
    
    def initFontSizeSelector(self):
        fontSizeValidator = QDoubleValidator()
        fontSizeValidator.setNotation(QDoubleValidator.StandardNotation) #to fix: must stop ',' accepted as well as '.' (europian way of writing float)
        self.fontSizeSelector = QLineEdit("")
        self.fontSizeSelector.setValidator(fontSizeValidator)
        self.fontSizeSelector.textChanged.connect(self.fontSizeSelectorDictionary)
        self.layout.addRow("Font Size:",self.fontSizeSelector)

    def fontSizeSelectorDictionary(self):
        self.currentUserSettings['font-size'] = self.fontSizeSelector.text() + "px"
        self.saveQuitOff()

    ################ Deals with buttons ################

    def buttonInit(self):
        '''Initializes the buttons and connects functions'''
        self.saveButton = QPushButton("Save",self)
        self.deleteUserButton = QPushButton("Delete User",self)
        self.deleteUserButton.clicked.connect(self.deleteUser)
        self.saveButton.clicked.connect(self.saveButtonFunction)
        buttonLayout  = QHBoxLayout()
        buttonLayout.addWidget(self.deleteUserButton,2)
        buttonLayout.addStretch(6)
        buttonLayout.addWidget(self.saveButton,2)
        self.layout.addRow(buttonLayout)
        self.saveQuit = False

    def saveButtonFunction(self): #Bug: if repeatly clicked fast it break as it is unable the first run finish breaking the logic 
        '''Save the updated information when called'''
        if self.validProfile():
            if self.getEditedUsername() != self.getOriginalUsername():
                Profiles.deleteUser(self.getOriginalUsername())
            Profiles.saveUserProfile(self.getEditedUsername(), self.currentUserSettings)
            self.fillDropDownMenu()
        if self.saveQuit: 
            self.close()
        else:
            self.saveButton.setText("Save and Exit")
            self.saveQuit = True
     
    def saveQuitOff(self):
        '''Disables the save and quit for use whenever anything else is clicked'''
        self.saveQuit = False
        self.saveButton.setText("Save")
    
    def validProfile(self):
        '''Checks validity of the Profile so that it doesnt save a no functioning file'''
        if self.currentUserSettings['font-size'] is None:
            return False
        if self.currentUserSettings['font-family'] is None:
            return False
        return True
    
    def deleteUser(self):
        '''If there is a user to delete it deletes updating the file system accordingly''' 
        Profiles.deleteUser(self.getOriginalUsername())
        self.fillDropDownMenu()
        self.resetUserSettings()


    ################ Utitily Functions ################
    
    def getEditedUsername(self):
        return self.DropDownMenu.currentText()

    def getOriginalUsername(self):
        if self.DropDownMenu.itemText(self.DropDownMenu.currentIndex()) != "Create New User":
            return self.DropDownMenu.itemText(self.DropDownMenu.currentIndex())
        else:
            return None
    
    def resetUserSettings(self):
        '''Sets the values of the sliders to the current user settings'''
        self.currentUserSettings = Profiles.getUserSettings(self.getOriginalUsername())
        if self.currentUserSettings['font-size'] != None:
            self.fontSizeSelector.setText(re.search(r'\d+[.]?\d*',self.currentUserSettings['font-size']).group())
        else:
            self.fontSizeSelector.setText("")
        if self.currentUserSettings['font-family'] != None:
            self.fontSelector.setText(self.currentUserSettings['font-family'])
        else:
            self.fontSelector.setText("")
        self.setFontRgbaSliders(self.currentUserSettings['color'])


    def generateSliderBox(self,min: int, max: int,function):
        '''Generates a slider (to avoid code duplicaions)'''
        sliderBox = QHBoxLayout()
        slider = QSlider()
        slider.setOrientation(1)
        slider.setRange(min,max)
        indicator = QLabel()
        indicator.setFixedSize(25,20)
        indicator.setText(str(slider.value()))
        sliderBox.addWidget(indicator)
        sliderBox.addWidget(slider)
        slider.valueChanged.connect(function)
        return sliderBox
    
    
    ################ Window Wide Events ################

    def resizeEvent(self,event):
        super().resizeEvent(event)

    def eventFilter(self, source, event):
        '''Enables editing of the name of a already made profile'''
        if event.type() == event.MouseButtonDblClick and source is self.DropDownMenu:
            self.DropDownMenu.setEditable(True)
        return super().eventFilter(source, event)
    
    def mousePressEvent(self, event):
        self.saveQuitOff()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())
