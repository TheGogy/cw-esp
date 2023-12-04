import yaml
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QPushButton,QDialog,QFormLayout,QHBoxLayout,QCompleter,QLineEdit,QSlider,QLabel,QComboBox
from PyQt5.QtCore import  pyqtSignal, QObject,QRect,QEvent,Qt
from PyQt5.QtGui import QFontDatabase,QDoubleValidator
import sys
import os
from Profiles import Profiles


class Communicate(QObject):
    closed = pyqtSignal(str) 

class SettingsWindow(QDialog):

    def __init__(self,userProfiles):
        super().__init__()
        self.setGeometry(100,100,400,200)
        self.setWindowTitle("User Selection")
        self.userProfiles = userProfiles
        self.currentUserSettings = Profiles.getUserSettingDictionary(self.userProfiles)
        self.initLayout()
        self.resetCurrentUserSettings()
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
        self.DropDownMenu = QComboBox()
        self.fillDropDownMenu()
        self.DropDownMenu.activated.connect(self.activedDropDownMenu)
        self.DropDownMenu.currentIndexChanged.connect(self.changedUser)
        self.layout.addWidget(self.DropDownMenu)
        self.DropDownMenu.installEventFilter(self) 
        
    def fillDropDownMenu(self):
        self.DropDownMenu.clear()
        users =  self.userProfiles['Users'].keys()
        if self.userProfiles['Current'] is not None:
            self.DropDownMenu.addItem(self.userProfiles['Current'])
            users = list(self.userProfiles['Users'].keys())
            users.remove(self.userProfiles['Current'])
        for user in users:
            self.DropDownMenu.addItem(user)
        self.DropDownMenu.addItem("Create New User")
        self.DropDownMenu.setEditable(False)
        if self.DropDownMenu.count() == 1:
            self.DropDownMenu.setEditable(True)
            self.DropDownMenu.setCurrentText("")
        if self.DropDownMenu.count() > 1:
            self.userProfiles['Current'] = self.DropDownMenu.itemText(0)

    def activedDropDownMenu(self):
        if self.DropDownMenu.currentIndex() + 1 == self.DropDownMenu.count():
            self.DropDownMenu.setEditable(True)
            self.DropDownMenu.setCurrentText("")
            self.resetCurrentUserSettings()
                        
    def changedUser(self):
        if self.DropDownMenu.count() == 0:
            return
        self.DropDownMenu.setEditable(False)
        if self.DropDownMenu.currentText() == "Create New User":
            self.userProfiles['Current'] = None
            self.DropDownMenu.setEditable(True)
            self.DropDownMenu.setCurrentText("")
            self.resetCurrentUserSettings()
        else:
            self.userProfiles['Current'] = self.DropDownMenu.currentText()
            self.resetCurrentUserSettings()

        

    ################ Deals with font colour ################ 

    def initFontrgba(self):
         #adding fontrgba slider
        fontrgbSlidersBox = QHBoxLayout()
        self.fontrgbSliders  = {} #(r,g,b) sliders
        self.fontrgbIndicators = {}
        for colour in ("red","green","blue"):
            slider, indicator = self.generateSlider(0,255)
            slider.valueChanged.connect(self.updateSliderIndicators)
            self.fontrgbSliders[colour] = slider
            self.fontrgbIndicators[colour] = indicator
            fontrgbSlidersBox.addWidget(indicator,6)
            fontrgbSlidersBox.addWidget(slider,10)
        self.layout.addRow("Colour:",fontrgbSlidersBox)
        #adding font opacity slider
        self.fontOpacitySlider, self.fontOpacityIndicator = self.generateSlider(0,100)
        self.fontOpacityIndicator.setText(str(self.fontOpacitySlider.value() /100))
        opacityLayout = QHBoxLayout()
        opacityLayout.addWidget(self.fontOpacitySlider)
        opacityLayout.addWidget(self.fontOpacityIndicator)
        self.layout.addRow("Font Opacity: ",opacityLayout)
        self.fontOpacitySlider.valueChanged.connect(self.updateSliderIndicators)
        self.currentUserSettings['color'] = "rgba(0,0,0,0)"
    
    def updateSliderIndicators(self):
        self.fontOpacityIndicator.setText(str(self.fontOpacitySlider.value() /100))
        for colour in self.fontrgbIndicators.keys():
            self.fontrgbIndicators[colour].setText(str(self.fontrgbSliders[colour].value()))
        self.fontrgbaDictionary()
        self.saveQuitOff()

    def fontrgbaDictionary(self):
        rgba  =  "rgba(" + str(self.fontrgbSliders["red"].value())
        rgba += "," + str(self.fontrgbSliders["green"].value()) 
        rgba += "," + str(self.fontrgbSliders["blue"].value()) 
        rgba += "," + str(self.fontOpacitySlider.value() /100) + ")"
        self.currentUserSettings['color']  = rgba

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

    ################ Deals with buttons ################

    def buttonInit(self):
        '''Initializes the buttons and connects functions'''
        self.saveButton = QPushButton("Save",self)
        self.deleteUserButton = QPushButton("Delete User",self)
        self.deleteUserButton.clicked.connect(self.deleteUser)
        self.saveButton.clicked.connect(self.saveButtonFunction)
        buttonLayout  = QHBoxLayout()
        buttonLayout.setGeometry(self.layout.geometry())
        buttonLayout.addWidget(self.deleteUserButton,2)
        buttonLayout.addStretch(6)
        buttonLayout.addWidget(self.saveButton,2)
        self.layout.addRow(buttonLayout)
        self.saveQuit = False

    def saveButtonFunction(self):
        if self.validProfile():
            if self.userProfiles['Current'] is None:
                self.userProfiles['Users'][self.DropDownMenu.currentText()] = self.userProfiles['DefaultPath'] + "/" + self.DropDownMenu.currentText() + ".css"
                self.userProfiles['Current'] = self.DropDownMenu.currentText()
            else:
                oldText = self.userProfiles['Current']
                path = self.userProfiles['Users'][oldText]
                del self.userProfiles['Users'][oldText]
                self.userProfiles['Current'] = self.DropDownMenu.currentText()
                self.userProfiles['Users'][self.userProfiles['Current']] = path
            Profiles.saveUserProfile(self.userProfiles, self.currentUserSettings)
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
        elif self.currentUserSettings['font-family'] is None:
            return False
        return True
    
    def deleteUser(self):
        '''If there is a user to delete it deletes updating the file system accordingly'''
        if self.userProfiles['Current'] is not None:
            os.remove(self.userProfiles['Users'][self.userProfiles['Current']])
            del self.userProfiles['Users'][self.userProfiles['Current']]
            self.userProfiles['Current'] = None
            Profiles.saveProfilesFile(self.userProfiles)
            self.resetCurrentUserSettings()
            self.fillDropDownMenu()

    ################ Utitily Functions ################

    def resetCurrentUserSettings(self):
        '''Sets the values of the sliders to the current user settings'''
        self.currentUserSettings = Profiles.getUserSettingDictionary(self.userProfiles)
        if self.currentUserSettings['font-size'] != None:
            self.fontSizeSelector.setText(self.currentUserSettings['font-size'][:-2])
        else:
            self.fontSizeSelector.setText("")
        if self.currentUserSettings['font-family'] != None:
            self.fontSelector.setText(self.currentUserSettings['font-family'])
        else:
            self.fontSelector.setText("")
        rgbaSplit = (self.currentUserSettings['color'][5:-1]).split(",")
        rgbaDict = {}
        for index, colour in enumerate(("red","green","blue")):
            rgbaDict[colour] = rgbaSplit[index]
        for colour in ("red","green","blue"):    
            self.fontrgbSliders[colour].setValue(int(rgbaDict[colour]))
        self.fontOpacitySlider.setValue(int(float(rgbaSplit[3]) * 100))

    def generateSlider(self,min: int, max: int):
        '''Generates a slider (to avoid code duplicaions)'''
        slider = QSlider()
        slider.setOrientation(1)
        slider.setRange(min,max)
        indicator = QLabel()
        indicator.setText(str(slider.value()))
        return slider, indicator

    
    
    ################ Window Wide Events ################

    def resizeEvent(self,event):
        super().resizeEvent(event)

    def eventFilter(self, source, event):
        '''Enables editing of the name of a already made profile'''
        if event.type() == event.MouseButtonDblClick and source is self.DropDownMenu:
            self.DropDownMenu.setEditable(True)
            if self.DropDownMenu.currentText() == "Create New User":
                self.DropDownMenu.setCurrentText("")
        return super().eventFilter(source, event)
    
    def mousePressEvent(self, event):
        self.saveQuitOff()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SettingsWindow(Profiles.getUserProfiles())
    window.show()
    sys.exit(app.exec_())