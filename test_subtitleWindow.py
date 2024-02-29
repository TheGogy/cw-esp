import sys
import unittest
import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QPoint,QRect 
import SubtitleWindow
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtTest import QTest


class TestSubtitleWindow(unittest.TestCase):

    @pytest.mark.order(1)
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.window = SubtitleWindow.SubtitleWindow()
        self.window.hide()

    @pytest.mark.order(2)
    def tearDown(self):
        self.window.close()

    @pytest.mark.order(3)
    def test_mousePressEvent(self):     
        # current default mouse position is 300, 100
        # move it 101, 101 
        QTest.mousePress(self.window, Qt.LeftButton, Qt.NoModifier, QPoint(101, 101))
        # check if dragging is set to True after mouse press
        self.assertTrue(self.window.dragging)
        # Check if the old position is set correctly after mouse press
        # expected result:
        # 300 + 101 = 401
        # 100 + 101 = 201 
        self.assertEqual(self.window.oldPosition, QPoint(401, 201))

    @pytest.mark.order(4)
    def test_mouseMoveEvent(self):
        QTest.mousePress(self.window, Qt.LeftButton, Qt.NoModifier, QPoint(100, 0))
        QTest.mouseMove(self.window, QPoint(200, 100))
        self.assertEqual(self.window.pos(), QPoint(300, 100))
    
    @pytest.mark.order(5)
    def test_mouseReleaseEvent(self):
        QTest.mousePress(self.window, Qt.LeftButton, Qt.NoModifier, QPoint(100, 100))
        QTest.mouseRelease(self.window, Qt.LeftButton, Qt.NoModifier)
        # check if dragging is set to false once mouse released
        self.assertFalse(self.window.dragging)
        # check if the position is reset to none
        self.assertEqual(self.window.oldPosition, None)

    @pytest.mark.order(6)
    def test_resizeEvent(self):
        # set to a new size
        self.window.resize(1000, 100)
        # set the expected size 
        expect_size = QRect(0, 0, 1000, 100)
        self.assertEqual(self.window.label.geometry(), expect_size)

    @pytest.mark.order(7)
    def test_switchTransparencyMode(self):

        # transparent mode is true
        self.assertTrue(self.window.translucentMode)
        # transparent mode intally on 
        self.assertTrue(self.window.testAttribute(Qt.WA_TranslucentBackground))

        # toggle the transparent mode to false 
        self.window.switchTransparencyMode()
        # check after the toggle is set to false 
        self.assertFalse(self.window.translucentMode)
        # now check the background actually is false. 
        self.assertFalse(self.window.testAttribute(Qt.WA_TranslucentBackground))

    @pytest.mark.order(8)
    def test_setSubtitleText(self):
        # set a long subtitle text
        long_text = "this is a very long message that won't fit on the screen, this is a very long message that won't fit on the screen "
        
        # set the subtitle text
        self.window.setSubtitleText(long_text, window_width=500)
        print(self.window.label.text())

        expect_text = "won't fit on the screen, this is a very long message that won't fit on the screen "
        self.assertEqual(self.window.label.text(), expect_text)
        


    # #TODO
    # @pytest.mark.order(9)
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
    # @pytest.mark.order(9)
    # def test_openSettingsMenu(self):
    #     self.window.openSettingsMenu()

    #     # userSelector
    #     settings_window = self.window.userSelector
    #     self.assertIsNotNone(settings_window)
    #     settings_window.close()

    #     self.assertTrue(self.window.isVisible())


    


if __name__ == '__main__':
    unittest.main()
