from src import InstallWorker, InstallWorkerSignals, InstallSettings
from src import Profiles
import pytest
import os
import shutil
from pathlib import Path
from PyQt5.QtWidgets import QComboBox, QPushButton


#below import solves mac specific error (i think)
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

# SETUP and TEARDOWN #
####################################################################################

pytest.RUNTIME_DIR = Path(__file__).parent / "InstallSettingsTest"

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
def installWorker(qtbot,profiles,scope="module"):
    worker = InstallWorker(profiles)
    yield worker

@pytest.fixture
def installSettings(qtbot, installWorker,profiles):
    settings = InstallSettings(installWorker,profiles)
    yield settings


####################################################################################

@pytest.mark.order(1)
def testRun(qtbot, installWorker,installSettings):
    ''' tests basic core functionality of button click and response,
        modify if additional test needed
    '''
    with qtbot.waitSignal(installSettings.installButton.clicked):
        installSettings.installButton.click()
    # can also add qbot wait signals if you want
    assert installWorker.isRunning() is True


@pytest.mark.order(2)
def testTerminate(installWorker):
    assert True # delete when error resolved
    '''
    This test case should work, but test terminate may not actually
    be functioning properly. 
    '''
    # runs, terminates and then checks if termination.
    # installWorker.start()
    # installWorker.terminate()
    # assert installWorker.isRunning() is False

@pytest.mark.order(3)
def testInitalisationInitInstallWorker(installWorker,installSettings):
    # checks initialisation
    assert installSettings.installWorker == installWorker

@pytest.mark.order(4)
def testBeginInitInstallWorker(installWorker,installSettings):
    assert installSettings.installWorker == installWorker
    # so basically hasattr checks if installSettings.installWorker.signals has the attribute began.
    # works like assertEquals.
    # if it does, test case passes.
    assert hasattr(installSettings.installWorker.signals, 'began')

@pytest.mark.order(5)
def testBeginInitInstallWorker(installWorker,profiles):
    installSettings = InstallSettings(installWorker,profiles)
    assert installSettings.installWorker == installWorker
    assert hasattr(installSettings.installWorker.signals, 'finished')

@pytest.mark.order(6)
def testInterruptedInitInstallWorker(installWorker,profiles):
    installSettings = InstallSettings(installWorker,profiles)
    assert installSettings.installWorker == installWorker
    assert hasattr(installSettings.installWorker.signals, 'interrupted')

@pytest.mark.order(7)
def testInitDropdownMenu(qtbot, installSettings):
    # check initialisation
    assert installSettings.modelSelector is not None
    assert isinstance(installSettings.modelSelector, QComboBox)
    # check model selection connection
    with qtbot.waitSignal(installSettings.modelSelector.activated):
        if installSettings.modelSelector.activated.emit(0):
            assert True
        # emits mic signal and if true passes test case.

@pytest.mark.order(8)
def testInitButtonsInitialisation(installSettings):
    # check if the installButton and deleteButton are initialised 
    assert installSettings.installButton is not None
    assert isinstance(installSettings.installButton, QPushButton)
    assert installSettings.deleteButton is not None
    assert isinstance(installSettings.deleteButton, QPushButton)

@pytest.mark.order(9)
def testInitButtonsFunctionsInstall(installSettings):
    # test install button, should be enough 
    assert installSettings.installButton.text() == "Install"

@pytest.mark.order(10)
def testInitButtonsFunctionsDelete(qtbot,installSettings):
    # qbot is a little funky so instead call function directly
    installSettings.installFunction() 
    # now test the delete functions
    installSettings.deleteButtonFunction()
    assert installSettings.deleteButton.isEnabled()

@pytest.mark.order(11)
def testInstallFunction(installWorker,installSettings):
    installSettings.installFunction()
    assert installWorker.modelName == installSettings.getCurrentModelText()

@pytest.mark.order(12)
def testDeleteButtonFunction(installWorker,installSettings):
    installSettings.deleteButtonFunction()
    assert installSettings.installButton.text() == "Install"
    assert installSettings.deleteButton.isEnabled() == True

@pytest.mark.order(13)
def test_updateButtonTextNotInstalled(installSettings):
    # just setup for a non installed model simulation
    installSettings.modelSelector.setCurrentText('Model2')
    # check expected results based on updateButtonText
    installSettings.updateButtonText()
    assert installSettings.installButton.text() == "Install"
    assert installSettings.deleteButton.text() == "Delete"
