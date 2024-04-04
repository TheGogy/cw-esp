import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton, QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from src.SettingsWindow import SettingsWindow
from src.Profiles import Profiles
import os
from pathlib import Path
import shutil
pytest.RUNTIME_DIR = Path(__file__).parent / "ProfileSettingsTest"

@pytest.fixture(scope="module")
def profiles():
    profiles = Profiles(pytest.RUNTIME_DIR)
    yield profiles 

def setup_module():
    if not os.path.exists(pytest.RUNTIME_DIR):
        os.mkdir(pytest.RUNTIME_DIR)
    profiles = Profiles(pytest.RUNTIME_DIR)

def teardown_module():
    if os.path.isdir(pytest.RUNTIME_DIR):
        shutil.rmtree(pytest.RUNTIME_DIR)

@pytest.fixture
def ProfileSettings(qtbot):
    '''Create instance of SettingsProfileSettings'''
    test_ProfileSettings = SettingsWindow()
    yield test_ProfileSettings.RightColumnLayout

    

@pytest.mark.order(1)
def test_initLayout(ProfileSettings):
    '''Test layout instantiated'''
    assert ProfileSettings is not None

@pytest.mark.order(2)
def test_DropDownMenu(ProfileSettings):
    '''Test DropDownMenu instantiated and message added'''
    assert ProfileSettings.DropDownMenu is not None
    assert ProfileSettings.DropDownMenu.count() > 0
    assert ProfileSettings.DropDownMenu.itemText(ProfileSettings.DropDownMenu.count() - 1) == ProfileSettings.NEW_USER_MESSAGE

@pytest.mark.order(3)
def test_fillDropDownMenu(ProfileSettings,profiles):
    '''Test ddmenu filled with correct users'''
    dropDownMenu = ProfileSettings.DropDownMenu
    currentUser = profiles.getCurrentUser()
    allItems = [dropDownMenu.itemText(i) for i in range(dropDownMenu.count())]
    profiles = sorted(profiles.getUserList())
    for x in range(len(profiles)):
        assert allItems[x] == profiles[x]

@pytest.mark.order(4)
def test_ButtonInit(ProfileSettings):
    '''Test Buttons instantiated and display correct message'''
    assert ProfileSettings.saveButton is not None
    assert ProfileSettings.saveButton.text() == "Save"
    assert ProfileSettings.deleteUserButton is not None
    assert ProfileSettings.deleteUserButton.text()== "Delete User"
    ProfileSettings.buttonInit()
    assert ProfileSettings.saveQuit == False

@pytest.mark.order(5)
def test_SaveButton(ProfileSettings):
    '''Test when SaveButton is called, it calls function'''
    # Dictionary to track function calls
    function_calls = {'saveButtonFunction': 0}
    def count_calls():
        function_calls['saveButtonFunction'] += 1
    ProfileSettings.saveButtonFunction = count_calls()
    save_button = ProfileSettings.saveButton
    QTest.mouseClick(save_button, Qt.LeftButton)
    assert function_calls['saveButtonFunction'] == 1

@pytest.mark.order(6)
def test_DeleteUserButton(ProfileSettings):
    '''Test when SaveButton is called, it calls function'''
    # Dictionary to track function calls
    myfunction_calls = {'deleteUser': 0}
    def count_call():
        myfunction_calls['deleteUser'] += 1
    ProfileSettings.deleteUser = count_call()
    delete_user_button = ProfileSettings.deleteUserButton
    QTest.mouseClick(delete_user_button, Qt.LeftButton)
    assert myfunction_calls['deleteUser'] == 1

@pytest.mark.order(7)
def test_SliderColour(ProfileSettings):
    '''Test slider instantiated and slider values same as dictionary'''
    assert ProfileSettings.setFontRgbaSliders is not None
    # Check slider value is same as dictionary value
    ProfileSettings.fontRedSliderBox.itemAt(1).widget().value = 255
    ProfileSettings.fontGreenSliderBox.itemAt(1).widget().value = 255
    ProfileSettings.fontBlueSliderBox.itemAt(1).widget().value = 255
    ProfileSettings.fontOpacityBox.itemAt(1).widget().value = 1
    assert ProfileSettings.currentUserSettings['color']  == 'rgba(255,255,255,1.0)'

@pytest.mark.order(8)
def test_fontSizeSelectorDictionary(ProfileSettings):
    '''Test slider font size is same as dictionary'''
    ProfileSettings.fontSizeSelector.setText('100')
    ProfileSettings.fontSizeSelectorDictionary()
    assert ProfileSettings.currentUserSettings['font-size'] == '100px'

if __name__ == '__main__':
    pytest.main()
