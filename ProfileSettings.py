### Pyqt imports
from PyQt5.QtWidgets import QPushButton, QFormLayout,QHBoxLayout,QCompleter,QLineEdit,QSlider,QLabel,QComboBox
from PyQt5.QtCore import  pyqtSignal, QObject,QRect,QEvent 
from PyQt5.QtGui import QFontDatabase,QDoubleValidator
### General Library imports
import sys
import re
### Project Imports
from Profiles import Profiles

class ProfileSettings(QFormLayout):
    
    ################ Constants ################

    NEW_USER_MESSAGE = "Create New User"
  
    ################ Signals ################

    closed = pyqtSignal()

    ################ Initialation ###############

    def __init__(self):
        super().__init__()
        self.currentUserSettings = Profiles.getCurrentUserSettings()
        self.initUserDropdownMenu()
        self.initErrorMessage()
        self.initFontrgba()
        self.initFontSelector()
        self.initFontSizeSelector()
        self.initBackgroundrgba()
        self.initBorderRadius()
        self.buttonInit()
        self.resetUserSettings()

    def initUserDropdownMenu(self):
        '''Creates the user DropDownMenu, adds it to form layout and connects it to the required functions'''
        self.DropDownMenu = QComboBox()
        self.fillDropDownMenu()
        self.DropDownMenu.activated.connect(self.changedUser)
        self.addWidget(self.DropDownMenu)
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
        self.DropDownMenu.addItem(ProfileSettings.NEW_USER_MESSAGE)
        self.DropDownMenu.setEditable(True)
        self.updateText()

    def changedUser(self):
        '''Updates entire settings menu if user is changed'''
        self.updateText()
        self.resetUserSettings()
 
    def updateText(self):
        '''if create new user is selected enter editable mode'''
        self.DropDownMenu.setEditable(False)
        if self.DropDownMenu.currentText() == ProfileSettings.NEW_USER_MESSAGE:
            self.DropDownMenu.setEditable(True)
            self.DropDownMenu.setCurrentText("")
    
    ################ Error Message ################
    
    def initErrorMessage(self):
        '''Initializes error Message (not valid settings)'''
        self.errorMessage = QLabel()
        self.errorMessage.setText("")
        self.errorMessage.setStyleSheet("color: red")
        self.addWidget(self.errorMessage)

    ################ Deals with font colour ################ 

    def initFontrgba(self):
        '''Initializes font rgba sliders and adds them to form'''
        #adding fontrgba slider
        fontrgbSlidersBox = QHBoxLayout()

        # Styling Red Slider 
        self.fontRedSliderBox = self.generateSliderBox(0,255,self.updateSliderIndicators)
        fontrgbSlidersBox.addLayout(self.fontRedSliderBox)
        self.fontRedSliderBox.itemAt(1).widget().setStyleSheet(self.generate_slider_style(self.generateGradient("white", "red")))
        
        # Styling for Green Slider
        self.fontGreenSliderBox = self.generateSliderBox(0, 255, self.updateSliderIndicators)
        fontrgbSlidersBox.addLayout(self.fontGreenSliderBox)
        self.fontGreenSliderBox.itemAt(1).widget().setStyleSheet(self.generate_slider_style(self.generateGradient("white", "green")))

        # Styling for blue slider
        self.fontBlueSliderBox = self.generateSliderBox(0, 255, self.updateSliderIndicators)
        fontrgbSlidersBox.addLayout(self.fontBlueSliderBox)
        self.fontBlueSliderBox.itemAt(1).widget().setStyleSheet(self.generate_slider_style(self.generateGradient("white", "blue")))

        self.addRow("Colour:",fontrgbSlidersBox)
        # add the font opacity slider
        self.fontOpacityBox = self.generateSliderBox(0,100,self.updateSliderIndicators)
        self.fontOpacityBox.itemAt(1).widget().setStyleSheet(self.generate_slider_style(self.generateGradient("white", "black")))
        self.addRow("Font Opacity: ",self.fontOpacityBox)

    def updateSliderIndicators(self):
        '''Updates the slider indicator and dictionary when a slider is moved'''
        r = self.fontRedSliderBox.itemAt(1).widget().value()
        g = self.fontGreenSliderBox.itemAt(1).widget().value()
        b = self.fontBlueSliderBox.itemAt(1).widget().value()
        a = self.fontOpacityBox.itemAt(1).widget().value() / 100

        self.fontrgbaDictionary(f"rgba({r},{g},{b},{a})")
        self.setFontRgbaSliders()
        self.saveQuitOff()

    def fontrgbaDictionary(self,value: str):
        '''Updates dictionary'''
        self.currentUserSettings['color']  = value
        self.saveQuitOff()

    def setFontRgbaSliders(self):
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
        self.addRow("Font:" ,self.fontSelector)

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
        self.addRow("Font Size:",self.fontSizeSelector)

    def fontSizeSelectorDictionary(self):
        if self.fontSizeSelector.text() == "":
            self.currentUserSettings['font-size'] = None
        else:
            self.currentUserSettings['font-size'] = self.fontSizeSelector.text() + "px"    
        self.saveQuitOff()

    ################ Background Colour ################

    def initBackgroundrgba(self):
        '''Initializes font rgba sliders and adds them to form'''
        #adding fontrgba slider
        backgroundRgbSlidersBox = QHBoxLayout()

        # Styling Red Slider 
        self.backgroundRedSliderBox = self.generateSliderBox(0,255,self.updateBackgroundSliderIndicators)
        backgroundRgbSlidersBox.addLayout(self.backgroundRedSliderBox)
        self.backgroundRedSliderBox.itemAt(1).widget().setStyleSheet(self.generate_slider_style(self.generateGradient("white", "red")))
        
        # Styling for Green Slider
        self.backgroundGreenSliderBox = self.generateSliderBox(0, 255, self.updateBackgroundSliderIndicators)
        backgroundRgbSlidersBox.addLayout(self.backgroundGreenSliderBox)
        self.backgroundGreenSliderBox.itemAt(1).widget().setStyleSheet(self.generate_slider_style(self.generateGradient("white", "green")))

        # Styling for blue slider
        self.backgroundBlueSliderBox = self.generateSliderBox(0, 255, self.updateBackgroundSliderIndicators)
        backgroundRgbSlidersBox.addLayout(self.backgroundBlueSliderBox)
        self.backgroundBlueSliderBox.itemAt(1).widget().setStyleSheet(self.generate_slider_style(self.generateGradient("white", "blue")))

        self.addRow("Background Colour:",backgroundRgbSlidersBox)
        # add the font opacity slider
        self.backgroundOpacityBox = self.generateSliderBox(0,100,self.updateSliderIndicators)
        self.backgroundOpacityBox.itemAt(1).widget().setStyleSheet(self.generate_slider_style(self.generateGradient("white", "black")))
        self.addRow("Background Opacity: ",self.backgroundOpacityBox)

    def updateBackgroundSliderIndicators(self):
        '''Updates the slider indicator and dictionary when a slider is moved'''
        r = self.backgroundRedSliderBox.itemAt(1).widget().value()
        g = self.backgroundGreenSliderBox.itemAt(1).widget().value()
        b = self.backgroundBlueSliderBox.itemAt(1).widget().value()
        a = self.backgroundOpacityBox.itemAt(1).widget().value() / 100

        self.backgroundrgbaDictionary(f"rgba({r},{g},{b},{a})")
        self.setBackgroundRgbaSliders()
        self.saveQuitOff()

    def backgroundrgbaDictionary(self,value: str):
        '''Updates dictionary'''
        self.currentUserSettings['background-color']  = value
        self.saveQuitOff()

    def setBackgroundRgbaSliders(self):
        '''sets fonts and and indicator to a given rgba value'''
        rgbaValues = re.findall(r'\d+[.]?\d*',self.currentUserSettings['background-color'])
        self.backgroundRedSliderBox.itemAt(1).widget().setValue(int(rgbaValues[0]))
        self.backgroundRedSliderBox.itemAt(0).widget().setText(rgbaValues[0])
        self.backgroundGreenSliderBox.itemAt(1).widget().setValue(int(rgbaValues[1]))
        self.backgroundGreenSliderBox.itemAt(0).widget().setText(rgbaValues[1])
        self.backgroundBlueSliderBox.itemAt(1).widget().setValue(int(rgbaValues[2]))
        self.backgroundBlueSliderBox.itemAt(0).widget().setText(rgbaValues[2])
        self.backgroundOpacityBox.itemAt(1).widget().setValue(int(float(rgbaValues[3]) * 100))
        self.backgroundOpacityBox.itemAt(0).widget().setText(rgbaValues[3])

    def initBorderRadius(self):
        self.borderRadiusSliderBox = self.generateSliderBox(0,25,self.updateBorderRadiusIndicator)
        self.borderRadiusSliderBox.itemAt(1).widget().setStyleSheet(self.generate_slider_style("red"))
        self.addRow("Border Radius:",self.borderRadiusSliderBox)

    def updateBorderRadiusIndicator(self):
        self.borderRadiusSliderBox.itemAt(0).widget().setText(str(self.borderRadiusSliderBox.itemAt(1).widget().value()))
        self.borderRadiusDictionary()

    def borderRadiusDictionary(self):
        self.currentUserSettings['border-radius'] = str(self.borderRadiusSliderBox.itemAt(1).widget().value()) + "px"

    def setBorderRadiusSlider(self):
        value = self.currentUserSettings['border-radius'][:-2]
        self.borderRadiusSliderBox.itemAt(0).widget().setText(str(value))

    ################ Deals with buttons ################

    def buttonInit(self):
        '''Initializes the buttons and connects functions'''
        self.saveButton = QPushButton("Save")
        self.deleteUserButton = QPushButton("Delete User")
        self.deleteUserButton.clicked.connect(self.deleteUser)
        self.saveButton.clicked.connect(self.saveButtonFunction)
        buttonLayout  = QHBoxLayout()
        buttonLayout.addWidget(self.deleteUserButton,2)
        buttonLayout.addStretch(6)
        buttonLayout.addWidget(self.saveButton,2)
        self.addRow(buttonLayout)
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
            self.closed.emit()
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
        if self.DropDownMenu.itemText(self.DropDownMenu.currentIndex()) == ProfileSettings.NEW_USER_MESSAGE:
            return None
        return self.DropDownMenu.itemText(self.DropDownMenu.currentIndex())
    
    def resetUserSettings(self):
        '''Sets the values of the sliders to the current user settings'''
        self.currentUserSettings = Profiles.getUserSettings(self.getOriginalUsername())
        #Rgba font slider reset
        self.setFontRgbaSliders()

        self.setBackgroundRgbaSliders()

        self.setBorderRadiusSlider()
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

    def generateGradient(self, start, end):
        return f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {start}, stop:1 {end})"

    def generate_slider_style(self, color):
        '''Returns a string containing the QSlider CSS'''
        return f"""
            QSlider::groove:horizontal {{
                background: {color};
                border: 1px solid #D8DEE9;
                height: 7.5px;
                margin: 0px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: #D8DEE9;
                border: 1px solid #D8DEE9;
                width: 4px;
                height: 4px;
                margin: -4px 0;
                border-radius: 2px;
            }}
            QSlider::sub-page:horizontal {{
                background: {color};
            }}
            QSlider::add-page:horizontal {{
                background: #D8DEE9;
            }}
        """

    
    
    ################ Window Wide Events ################

    def resizeEvent(self,event):
        super().resizeEvent(event)

    def eventFilter(self, source, event):
        '''Enables editing of the name of a already made profile'''
        if event.type() == event.MouseButtonDblClick and source is self.DropDownMenu:
            self.DropDownMenu.setEditable(True)
        return super().eventFilter(source, event)



