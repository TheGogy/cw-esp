import sys
import pytest
import os
from pathlib import Path
import shutil
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QPoint, QRect
from src.SubtitleWindow import SubtitleWindow
from src import Profiles
pytest.RUNTIME_DIR = Path(__file__).parent / "SubtitleWindowTest"

@pytest.fixture(scope="module")
def profiles():
    profiles = Profiles(pytest.RUNTIME_DIR)
    profiles.saveUserProfile("dumb bastard",Profiles.generateDefaultSettings())
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

@pytest.mark.order(1)
def test_mousePressEvent(window):
    QTest.mousePress(window, Qt.LeftButton, Qt.NoModifier, QPoint(101, 101))
    assert window.dragging
    assert window.oldPosition == QPoint(401, 201)
    window.close()

@pytest.mark.order(2)
def test_mouseMoveEvent(window):
    QTest.mousePress(window, Qt.LeftButton, Qt.NoModifier, QPoint(100, 0))
    QTest.mouseMove(window, QPoint(200, 100))
    assert window.pos() == QPoint(300, 100)

@pytest.mark.order(3)
def test_mouseReleaseEvent(window):
    QTest.mousePress(window, Qt.LeftButton, Qt.NoModifier, QPoint(100, 100))
    QTest.mouseRelease(window, Qt.LeftButton, Qt.NoModifier)
    assert not window.dragging
    assert window.oldPosition is None

@pytest.mark.order(4)
def test_resizeEvent(window):
    window.resize(1000, 100)
    expect_size = QRect(0, 0, 1000, 100)
    assert window.label.geometry() == expect_size


@pytest.mark.order(6)
def test_setSubtitleText(window):
    long_text = "this is a very long message that won't fit on the screen, this is a very long message that won't fit on the screen"
    window.setSubtitleText(long_text, windowWidth=500)
    assert len(window.label.text()) < len(long_text)

