import sys
import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QPoint, QRect
import SubtitleWindow

@pytest.mark.order(1)
def test_mousePressEvent():
    app = QApplication(sys.argv)
    window = SubtitleWindow.SubtitleWindow()
    window.hide()

    QTest.mousePress(window, Qt.LeftButton, Qt.NoModifier, QPoint(101, 101))
    assert window.dragging
    assert window.oldPosition == QPoint(401, 201)
    window.close()

@pytest.mark.order(2)
def test_mouseMoveEvent():
    app = QApplication(sys.argv)
    window = SubtitleWindow.SubtitleWindow()
    window.hide()

    QTest.mousePress(window, Qt.LeftButton, Qt.NoModifier, QPoint(100, 0))
    QTest.mouseMove(window, QPoint(200, 100))
    assert window.pos() == QPoint(300, 100)
    window.close()

@pytest.mark.order(3)
def test_mouseReleaseEvent():
    app = QApplication(sys.argv)
    window = SubtitleWindow.SubtitleWindow()
    window.hide()

    QTest.mousePress(window, Qt.LeftButton, Qt.NoModifier, QPoint(100, 100))
    QTest.mouseRelease(window, Qt.LeftButton, Qt.NoModifier)
    assert not window.dragging
    assert window.oldPosition is None
    window.close()

@pytest.mark.order(4)
def test_resizeEvent():
    app = QApplication(sys.argv)
    window = SubtitleWindow.SubtitleWindow()
    window.hide()

    window.resize(1000, 100)
    expect_size = QRect(0, 0, 1000, 100)
    assert window.label.geometry() == expect_size
    window.close()

@pytest.mark.order(5)
def test_switchTransparencyMode():
    app = QApplication(sys.argv)
    window = SubtitleWindow.SubtitleWindow()
    window.hide()

    assert window.translucentMode
    assert window.testAttribute(Qt.WA_TranslucentBackground)
    
    window.switchTransparencyMode()
    assert not window.translucentMode
    assert not window.testAttribute(Qt.WA_TranslucentBackground)
    window.close()

@pytest.mark.order(6)
def test_setSubtitleText():
    app = QApplication(sys.argv)
    window = SubtitleWindow.SubtitleWindow()
    window.hide()

    long_text = "this is a very long message that won't fit on the screen, this is a very long message that won't fit on the screen "
    window.setSubtitleText(long_text, window_width=500)
    expect_text = "won't fit on the screen, this is a very long message that won't fit on the screen "
    assert window.label.text() == expect_text
    window.close()

# #TODO
# @pytest.mark.order(7)
# def test_contextMenuEvent(self):
#     QTest.mouseClick(self.window, Qt.RightButton)
#     context_menu = self.window.childAt(QPoint(0, 0))
#     self.assertIsNotNone(context_menu)

#     # # check enable translusent 
#     # enable_action = context_menu.findChild(
#     #     QAction, ""
#     # )
#     # self.assertEqual(enable_action,context_menu)

#TODO 
# @pytest.mark.order(8)
# def test_openSettingsMenu(self):
#     self.window.openSettingsMenu()

#     # userSelector
#     settings_window = self.window.userSelector
#     self.assertIsNotNone(settings_window)
#     settings_window.close()

#     self.assertTrue(self.window.isVisible())