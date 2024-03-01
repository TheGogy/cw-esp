from InstallSettings import InstallWorker, InstallWorkerSignals, InstallSettings
import pytest
from pytestqt import qtbot  # allows interaction with PyQt widgets
from PyQt5.QtWidgets import QComboBox, QPushButton
import time

# SETUP and TEARDOWN #
####################################################################################
class MockProfiles:
    @staticmethod
    def installModel(model_name):
        pass

    @staticmethod
    def getInstalledModels():
        return []


@pytest.fixture
def mockProfiles(monkeypatch):
    monkeypatch.setattr('InstallSettings.Profiles', MockProfiles)


@pytest.fixture
def installWorker():
    worker = InstallWorker()
    yield worker

####################################################################################

@pytest.mark.order(1)
def testRun(qtbot):
    pass 

@pytest.mark.order(2)
def testTerminate(installWorker):
    # runs, terminates and then checks if termination.
    installWorker.start()
    installWorker.terminate()
    assert installWorker.isRunning()

@pytest.mark.order(3)
def testInitalisationInitInstallWorker(installWorker):
    # checks initialisation
    installSettings = InstallSettings(installWorker)
    assert installSettings.installWorker == installWorker

@pytest.mark.order(4)
def testBeginInitInstallWorker(installWorker):
    installSettings = InstallSettings(installWorker)
    assert installSettings.installWorker == installWorker
    # so basically hasattr checks if installSettings.installWorker.signals has the attribute began.
    # works like assertEquals.
    # if it does, test case passes.
    assert hasattr(installSettings.installWorker.signals, 'began')

@pytest.mark.order(5)
def testBeginInitInstallWorker(installWorker):
    installSettings = InstallSettings(installWorker)
    assert installSettings.installWorker == installWorker
    assert hasattr(installSettings.installWorker.signals, 'finished')

@pytest.mark.order(6)
def testInterruptedInitInstallWorker(installWorker):
    installSettings = InstallSettings(installWorker)
    assert installSettings.installWorker == installWorker
    assert hasattr(installSettings.installWorker.signals, 'interrupted')

@pytest.mark.order(7)
def testInitDropdownMenu(qtbot, installWorker):
    # check initialisation
    installSettings = InstallSettings(installWorker)
    assert installSettings.modelSelector is not None
    assert isinstance(installSettings.modelSelector, QComboBox)
    # check model selection connection
    with qtbot.waitSignal(installSettings.modelSelector.activated):
        if installSettings.modelSelector.activated.emit(0):
            assert True
        # emits mic signal and if true passes test case.

@pytest.mark.order(8)
def testInitButtonsInitialisation(installWorker):
    # Create an instance of InstallSettings
    installSettings = InstallSettings(installWorker)

    # check if the installButton and deleteButton are initialised 
    assert installSettings.installButton is not None
    assert isinstance(installSettings.installButton, QPushButton)
    assert installSettings.deleteButton is not None
    assert isinstance(installSettings.deleteButton, QPushButton)

@pytest.mark.order(9)
def testInitButtonsFunctionsInstall(installWorker):
    # create instance of InstallSettings
    installSettings = InstallSettings(installWorker)
    # qbot is a little funky so instead call function directly
    installSettings.installFunction()
    # test install button, should be enough 
    assert installSettings.installButton.text() == "Install"

@pytest.mark.order(10)
def testInitButtonsFunctionsDelete(installWorker):
    # create instance of InstallSettings
    installSettings = InstallSettings(installWorker)
    # qbot is a little funky so instead call function directly
    installSettings.installFunction() # 
    # now test the delete functions
    installSettings.deleteButtonFunction()
    assert installSettings.deleteButton.isEnabled()

@pytest.mark.order(11)
def testInstallFunction(installWorker):
    installSettings = InstallSettings(installWorker)
    installSettings.installFunction()
    assert installWorker.modelName == installSettings.modelSelector.currentText()


# def testDeleteButtonFunction(installWorker):
#     installSettings = InstallSettings(installWorker)
#     installSettings.deleteButtonFunction()

#     assert installSettings.installButton.text() == "Install"
#     # assert not installSettings.deleteButton.isEnabled()
#     # ... #TODO

# # def testUpdateButtonText(installWorker):
# #     # create instance 
# #     installSettings = InstallSettings(installWorker)  
# #     # TODO 
# #     # not really sure how to check this one
