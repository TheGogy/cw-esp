import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton, QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from SettingsWindow import SettingsWindow
from Profiles import Profiles
#import main


@pytest.fixture
def window():
    '''Create instance of SettingsWindow'''
    app = QApplication([]) 
    test_window = SettingsWindow()
    yield test_window
    test_window.close()


def test_initLayout(window):
    '''Test layout instantiated'''
    assert window.layout is not None

def test_DropDownMenu(window):
    '''Test DropDownMenu instantiated and message added'''
    assert window.DropDownMenu is not None
    assert window.DropDownMenu.count() > 0
    assert window.DropDownMenu.itemText(window.DropDownMenu.count() - 1) == SettingsWindow.NEW_USER_MESSAGE

def test_fillDropDownMenu(window):
    '''Test ddmenu filled with correct users'''
    dropDownMenu = window.DropDownMenu
    currentUser = Profiles.getCurrentUser()
    assert currentUser == None
    AllItems = [dropDownMenu.itemText(i) for i in range(dropDownMenu.count())]
    profiles = sorted(Profiles.getUserList())
    currentUser = Profiles.getCurrentUser()
    profiles.remove(currentUser)
    assert AllItems[0] == Profiles.getCurrentUser()
    for x in range(len(profiles)):
        assert AllItems[x + 1] = profiles[x]


def test_ButtonInit(window):
    '''Test Buttons instantiated and display correct message'''
    assert window.saveButton is not None
    assert window.saveButton.text() == "Save"
    assert window.deleteUserButton is not None
    assert window.deleteUserButton.text()== "Delete User"
    window.buttonInit()
    assert window.saveQuit == False

def test_SaveButton(window):
    '''Test when SaveButton is called, it calls function'''
    # Dictionary to track function calls
    function_calls = {'saveButtonFunction': 0}
    def count_calls():
        function_calls['saveButtonFunction'] += 1
    window.saveButtonFunction = count_calls()
    save_button = window.saveButton
    QTest.mouseClick(save_button, Qt.LeftButton)
    assert function_calls['saveButtonFunction'] == 1

def test_DeleteUserButton(window):
    '''Test when SaveButton is called, it calls function'''
    # Dictionary to track function calls
    myfunction_calls = {'deleteUser': 0}
    def count_call():
        myfunction_calls['deleteUser'] += 1
    window.deleteUser = count_call()
    delete_user_button = window.deleteUserButton
    QTest.mouseClick(delete_user_button, Qt.LeftButton)
    assert myfunction_calls['deleteUser'] == 1

def test_SliderColour(window):
    '''Test slider instantiated and slider values same as dictionary'''
    assert window.setFontRgbaSliders is not None
    # Check slider value is same as dictionary value
    window.fontRedSliderBox.itemAt(1).widget().value = 255
    window.fontGreenSliderBox.itemAt(1).widget().value = 255
    window.fontBlueSliderBox.itemAt(1).widget().value = 255
    window.fontOpacityBox.itemAt(1).widget().value = 1
    assert window.currentUserSettings['color']  == 'rgba(255,255,255,1.0)'


def test_fontSizeSelectorDictionary(window):
    '''Test slider font size is same as dictionary'''
    window.__init__()
    window.fontSizeSelector.setText('100')
    window.fontSizeSelectorDictionary()
    assert window.currentUserSettings['font-size'] == '100px'

if __name__ == '__main__':
    pytest.main()
