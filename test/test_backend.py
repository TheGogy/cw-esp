import sys
import pytest
import os
from pathlib import Path
import shutil
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QPoint, QRect
from src.SubtitleWindow import SubtitleWindow
from src.backend import MicrophoneThread
from src import Profiles
pytest.RUNTIME_DIR = Path(__file__).parent / "BackendTest"

@pytest.fixture(scope="module")
def profiles():
    profiles = Profiles(pytest.RUNTIME_DIR)
    profiles.saveUserProfile("test",Profiles.generateDefaultSettings())
    profiles.installModel("vosk-model-small-de-0.15")
    yield profiles 


def setup_module():
    if not os.path.exists(pytest.RUNTIME_DIR):
        os.mkdir(pytest.RUNTIME_DIR)
    profiles = Profiles(pytest.RUNTIME_DIR)

def teardown_module():
    if os.path.isdir(pytest.RUNTIME_DIR):
        shutil.rmtree(pytest.RUNTIME_DIR)
 
@pytest.fixture
def window(qtbot,profiles):
    window = SubtitleWindow(profiles)
    yield window

@pytest.fixture
def thread(qtbot,profiles,window):
    thread = MicrophoneThread(profiles,window)
    yield thread

#passes when run alone not otherwise no clue why
@pytest.mark.order(1)
def testInit(thread,qtbot):
    thread.start()
    assert thread.isRunning() 
