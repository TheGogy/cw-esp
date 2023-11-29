import yaml
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QPushButton,QDialog,QFormLayout,QHBoxLayout,QCompleter,QLineEdit,QSlider,QLabel,QComboBox
from PyQt5.QtCore import  pyqtSignal, QObject,QRect
from PyQt5.QtGui import QFontDatabase,QDoubleValidator
import sys
import os

''' Profiles.yml
Current: currentUsername
Users: dictionary key = username, value = path/to/user
DefaultPath: default path new users will be saved to
'''
def generateProfilesFile():
    data = {
    'Current': None,
    'Users': {},
    'DefaultPath': None,
    }
    profilesPath = str(Path(__file__).resolve().parent) + "/Profiles.yml"
    defaultPath = str(Path(__file__).resolve().parent) + "/Users"
    if not os.path.exists(defaultPath):
        os.mkdir(defaultPath)
    data['DefaultPath'] = defaultPath
    with open(profilesPath, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def getUserProfiles():
    profilesPath = str(Path(__file__).resolve().parent) + "/Profiles.yml"
    if not os.path.exists(profilesPath):
        generateProfilesFile()
    try:
        with open(profilesPath, "r") as profilesFile:
            profiles = yaml.safe_load(profilesFile)
    except (FileNotFoundError, yaml.YAMLError):
        generateProfilesFile()
    with open(profilesPath, "r") as profilesFile:
            profiles = yaml.safe_load(profilesFile)
    return profiles

class Communicate(QObject):
    closed = pyqtSignal(str) 

class UserSelector(QDialog):

    def __init__(self,userProfiles):
        super().__init__()
        self.setGeometry(100,100,400,200)
        self.setWindowTitle("User Selection")
        self.userProfiles = userProfiles
        self.currentUserSettings = self.getUserSettingDictionary()
        
        self.initLayout()
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
        
        #adding done and delete button
        

    ################ Drop down menu ################

    def initUserDropdownMenu(self):
        self.DropDownMenu = QComboBox()
        self.DropDownMenu.setEditable(True)
        for user in self.userProfiles['Users'].keys():
            self.DropDownMenu.addItem(user)
        self.DropDownMenu.addItem("Create New User")
        print(self.DropDownMenu.count())
        if self.DropDownMenu.count() == 1:
            self.DropDownMenu.setCurrentText("")
        self.DropDownMenu.activated.connect(self.changeCurrentUser)
        self.layout.addWidget(self.DropDownMenu)
        

    def changeCurrentUser(self):
        for x in range(self.DropDownMenu.count() - 2,-1,-1):
            if self.DropDownMenu.itemText(x) == "" or self.DropDownMenu.itemText(x) == "Create New User":
                self.DropDownMenu.removeItem(x)
        if self.DropDownMenu.currentIndex() + 1 == self.DropDownMenu.count():
            self.DropDownMenu.setCurrentText("")
        
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
        self.currentUserSettings['color'] = "rgba(0,0,0)"
    
    def updateSliderIndicators(self):
        self.fontOpacityIndicator.setText(str(self.fontOpacitySlider.value() /100))
        for colour in self.fontrgbIndicators.keys():
            self.fontrgbIndicators[colour].setText(str(self.fontrgbSliders[colour].value()))
        self.fontrgbaDictionary()

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
        fontSizeValidator.setNotation(QDoubleValidator.StandardNotation) #to be fix must stop , accepted as well as . (europian way of writing float)
        self.fontSizeSelector = QLineEdit("")
        self.fontSizeSelector.setValidator(fontSizeValidator)
        self.fontSizeSelector.textChanged.connect(self.fontSizeSelectorDictionary)
        self.layout.addRow("Font Size:",self.fontSizeSelector)

    def fontSizeSelectorDictionary(self):
        self.currentUserSettings['font-size'] = self.fontSizeSelector.text() + "px"

    ################ Deals with buttons ################

    def buttonInit(self):
        '''Initializes the buttons and connects functions'''
        self.doneButton = QPushButton("Done",self)
        self.deleteUserButton = QPushButton("Delete User",self)
        self.deleteUserButton.clicked.connect(self.deleteUser)
        self.doneButton.clicked.connect(self.doneButtonFunction)
        buttonLayout  = QHBoxLayout()
        buttonLayout.setGeometry(self.layout.geometry())
        buttonLayout.addWidget(self.deleteUserButton,2)
        buttonLayout.addStretch(6)
        buttonLayout.addWidget(self.doneButton,2)
        self.layout.addRow(buttonLayout)


    def doneButtonFunction(self):
        self.userProfiles['Current'] = self.DropDownMenu.currentText()
        self.userProfiles['Users'][self.DropDownMenu.currentText()] = self.userProfiles['DefaultPath'] + "/" + self.DropDownMenu.currentText() + ".css"
        self.saveUserProfile()
        self.close()
    
    def saveUserProfile(self):
        if self.userProfiles['Current'] is None:
            userFilePath = self.userProfiles['DefaultPath'] + "/" + self.DropDownMenu.currentText() + ".css"
        else:
            userFilePath = self.userProfiles['Users'][self.userProfiles['Current']]
        css_string = "QLabel {\n"
        #adding rgba font colour
        for element in self.currentUserSettings.keys():
            css_string += element + ": " + self.currentUserSettings[element] + ";\n"
        css_string += "}"
        with open(userFilePath, 'w') as userFile:
            userFile.write(css_string)
        
    def deleteUser(self):
        os.remove(self.userProfiles['Users'][self.userProfiles['Current']])
        del self.userProfiles['Users'][self.userProfiles['Current']]
        self.userProfiles['Current'] = None

    ################ Utitily Functions ################

    def generateSlider(self,min: int, max: int):
        slider = QSlider()
        slider.setOrientation(1)
        slider.setRange(min,max)
        indicator = QLabel()
        indicator.setText(str(slider.value()))
        return slider, indicator

    def getUserSettingDictionary(self):
        if self.userProfiles['Current'] is None:
            userSettings = {}
            userSettings['color'] = "rgba(0,0,0,0)"
            userSettings['font-family'] = None
            userSettings['font-size'] = None
        else:
            userSettings = {}
            # add code to generate dictionary from css file
        return userSettings
    
    ################ Window Wide Events ################

    def closeEvent(self,event):
        with open(str(Path(__file__).resolve().parent) + "/Profiles.yml", 'w') as file:
            yaml.dump(self.userProfiles, file)

    def resizeEvent(self,event):
        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserSelector(getUserProfiles())
    window.show()
    sys.exit(app.exec_())