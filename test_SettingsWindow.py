import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton, QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from SettingsWindow import SettingsWindow
from Profiles import Profiles


@pytest.fixture
def app():
    '''Create QApplication to test'''
    test_app = QApplication([])
    yield test_app
    test_app.quit()

@pytest.fixture
def window(app):
    '''Create instance of SettingsWindow'''
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
    AllItems = [dropDownMenu.itemText(i) for i in range(dropDownMenu.count())]
    assert AllItems[0] == Profiles.getCurrentUser()
    #pytest.assertCountEqual(AllItems, sorted(Profiles.getUserList()))


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

def test_ValidProfiles(window):
    '''Check that valid profiles return true'''
    window.currentUserSettings =  Profiles.getCurrentUser()

def test_SliderColour(window):
    '''Test slider instantiated and slider values same as dictionary'''
    assert window.setFontRgbaSliders is not None
    # Check slider value is same as dictionary value
    window.fontRedSliderBox.itemAt(1).widget().value = 255
    window.fontGreenSliderBox.itemAt(1).widget().value = 255
    window.fontBlueSliderBox.itemAt(1).widget().value = 255
    window.fontOpacityBox.itemAt(1).widget().value = 1
    assert window.currentUserSettings['color']  == 'rgba(255,255,255,1.0)'

def test_SliderFont(window):
    '''Test slider font is same as dictionary'''
    window.fontSelector.text = 'Arial'
    assert window.currentUserSettings['font-family'] == 'Arial'


if __name__ == '__main__':
    pytest.main()
