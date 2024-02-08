import yaml
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QPushButton,QDialog,QFormLayout,QHBoxLayout,QVBoxLayout,QCompleter,QLineEdit,QSlider,QLabel,QComboBox
from PyQt5.QtCore import  pyqtSignal, QObject,QRect,QEvent,Qt
from PyQt5.QtGui import QFontDatabase,QDoubleValidator
import sys
import re
from Profiles import Profiles


class Communicate(QObject):
    closed = pyqtSignal(str) 

class SettingsWindow(QDialog):
   
    ################ Constants ################

    NEW_USER_MESSAGE = "Create New User"
  
    ################ Initialization ################
    
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,400,200)
        self.setWindowTitle("User Selection")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.leftColumnLayout = QFormLayout()
        self.RightColumnLayout = QFormLayout()
        self.layout.addLayout(self.leftColumnLayout,1)
        self.layout.addLayout(self.RightColumnLayout,9)
        self.initLeftColumnLayout()
        self.initProfilesLayout()
        self.communicate = Communicate()

    def emptyFormLayout(self,layout: QFormLayout):
        while self.RightColumnLayout.rowCount() > 0:
            self.RightColumnLayout.removeRow(0)

    def initProfilesLayout(self):
        self.emptyFormLayout(self.RightColumnLayout)
        self.currentUserSettings = Profiles.getCurrentUserSettings()
        self.initUserDropdownMenu()
        self.initErrorMessage()
        self.initFontrgba()
        self.initFontSelector()
        self.initFontSizeSelector()
        self.buttonInit()
        self.resetUserSettings()

    def initModelSelector(self):
        self.emptyFormLayout(self.RightColumnLayout)
        self.RightColumnLayout.addRow(QLabel("Model place holder"))

    def initLeftColumnLayout(self):
        self.leftColumnExpanded = False
        collapseButton = QPushButton("",self)
        collapseButton.clicked.connect(self.collapsebuttonFunction)
        self.leftColumnLayout.addRow(collapseButton)
        profilesButton = QPushButton("Profiles",self)
        profilesButton.clicked.connect(self.initProfilesLayout)
        self.leftColumnLayout.addRow(profilesButton)
        modelsButton = QPushButton("Models",self)
        modelsButton.clicked.connect(self.initModelSelector)
        self.leftColumnLayout.addRow(modelsButton)

    def collapsebuttonFunction(self):
        if not self.leftColumnExpanded:
            self.layout.setStretch(1,3)
        else:
            self.layout.setStretch(1,9)
        self.leftColumnExpanded = not self.leftColumnExpanded
    
    def initTextPromptLayout(self):
        self.textPromptLayout = QFormLayout()
    
   ################ Drop down menu ################
 
    def initUserDropdownMenu(self):
        '''Creates the user DropDownMenu, adds it to form layout and connects it to the required functions'''
        self.DropDownMenu = QComboBox()
        self.fillDropDownMenu()
        self.DropDownMenu.activated.connect(self.changedUser)
        self.RightColumnLayout.addWidget(self.DropDownMenu)
        self.DropDownMenu.installEventFilter(self) 
        
    def fillDropDownMenu(self):
        '''Re-populates the DropDownMenu'''
        self.DropDownMenu.clear()
        users = sorted(Profiles.getUserList())
        currentUser = Profiles.getCurrentUser()
        if currentUser is not None:
            self.DropDownMenu.addItem(currentUser)
            users.remove(currentUser)
        for user in users:
            self.DropDownMenu.addItem(user)
        self.DropDownMenu.addItem(SettingsWindow.NEW_USER_MESSAGE)
        self.DropDownMenu.setEditable(True)
        self.updateText()

    def changedUser(self):
        '''Updates entire settings menu if user is changed'''
        self.updateText()
        self.resetUserSettings()
 
    def updateText(self):
        '''if create new user is selected enter editable mode'''
        self.DropDownMenu.setEditable(False)
        if self.DropDownMenu.currentText() == SettingsWindow.NEW_USER_MESSAGE:
            self.DropDownMenu.setEditable(True)
            self.DropDownMenu.setCurrentText("")
    
    ################ Error Message ################
    
    def initErrorMessage(self):
        '''Initializes error Message (not valid settings)'''
        self.errorMessage = QLabel()
        self.errorMessage.setText("")
        self.errorMessage.setStyleSheet("color: red")
        self.RightColumnLayout.addWidget(self.errorMessage)

    ################ Deals with font colour ################ 

    def initFontrgba(self):
        '''Initializes font rgba sliders and adds them to form'''
         #adding fontrgba slider
        fontrgbSlidersBox = QHBoxLayout()
        self.fontRedSliderBox = self.generateSliderBox(0,255,self.updateSliderIndicators)
        fontrgbSlidersBox.addLayout(self.fontRedSliderBox)
        self.fontGreenSliderBox = self.generateSliderBox(0,255,self.updateSliderIndicators)
        fontrgbSlidersBox.addLayout(self.fontGreenSliderBox)
        self.fontBlueSliderBox = self.generateSliderBox(0,255,self.updateSliderIndicators)
        fontrgbSlidersBox.addLayout(self.fontBlueSliderBox)
        self.RightColumnLayout.addRow("Colour:",fontrgbSlidersBox)
        #adding font opacity slider
        self.fontOpacityBox = self.generateSliderBox(0,100,self.updateSliderIndicators)
        self.RightColumnLayout.addRow("Font Opacity: ",self.fontOpacityBox)
    
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
        '''Initializes font fontSelector and adds it to the form'''
        availableFonts = QFontDatabase().families()
        fontCompleter = QCompleter(availableFonts)
        fontCompleter.setCaseSensitivity(False)
        self.fontSelector = QLineEdit("")
        self.fontSelector.setCompleter(fontCompleter)
        self.fontSelector.textChanged.connect(self.fontSelectorDictionary)
        self.RightColumnLayout.addRow("Font:" ,self.fontSelector)

    def fontSelectorDictionary(self):
        '''Updates the form selector dictionary'''
        self.currentUserSettings['font-family'] = self.fontSelector.text()
        self.saveQuitOff()
    
    ################ Font Size Selector ################

    def initFontSizeSelector(self):
        fontSizeValidator = QDoubleValidator()
        fontSizeValidator.setNotation(QDoubleValidator.StandardNotation) #to fix: must stop ',' accepted as well as '.' (europian way of writing float)
        self.fontSizeSelector = QLineEdit("")
        self.fontSizeSelector.setValidator(fontSizeValidator)
        self.fontSizeSelector.textChanged.connect(self.fontSizeSelectorDictionary)
        self.RightColumnLayout.addRow("Font Size:",self.fontSizeSelector)

    def fontSizeSelectorDictionary(self):
        if self.fontSizeSelector.text() == "":
            self.currentUserSettings['font-size'] = None
        else:
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
        self.RightColumnLayout.addRow(buttonLayout)
        self.saveQuit = False

    def saveButtonFunction(self): #Bug: if repeatly clicked fast it break as it is unable the first run finish breaking the logic 
        '''Save the updated information when called'''
        if not self.validProfile():
            return
        # Remove old username from database if name has changed
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
        self.errorMessage.setText("")
        # Checking if no name was entered
        if self.getEditedUsername() == "":
            self.errorMessage.setText("Please enter a profile name")
            return False
        # Checking if name is already taken
        if self.getOriginalUsername() is None and self.getEditedUsername() in Profiles.getUserList():
            self.errorMessage.setText("Profile name already taken.")
            return False
        # Checking for valid font
        if not self.currentUserSettings['font-family'] in QFontDatabase().families():
            self.errorMessage.setText("Please enter a valid font.")
            return False
        # Checking for valid font size
        if self.currentUserSettings['font-size'] is None:
            self.errorMessage.setText("Please enter a font size")
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
        if self.DropDownMenu.itemText(self.DropDownMenu.currentIndex()) == SettingsWindow.NEW_USER_MESSAGE:
            return None
        return self.DropDownMenu.itemText(self.DropDownMenu.currentIndex())
    
    def resetUserSettings(self):
        '''Sets the values of the sliders to the current user settings'''
        self.currentUserSettings = Profiles.getUserSettings(self.getOriginalUsername())
        #Rgba font slider reset
        self.setFontRgbaSliders(self.currentUserSettings['color'])
        #font reset
        if self.currentUserSettings['font-size'] is not None:
            self.fontSizeSelector.setText(re.search(r'\d+[.]?\d*',self.currentUserSettings['font-size']).group())
        else:
            self.fontSizeSelector.setText("")
        #font size reset
        if self.currentUserSettings['font-family'] is not None:
            self.fontSelector.setText(self.currentUserSettings['font-family'])
        else:
            self.fontSelector.setText("")


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
