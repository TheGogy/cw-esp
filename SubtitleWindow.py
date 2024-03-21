import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMenu, QAction, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from Profiles import Profiles
from SettingsWindow import SettingsWindow


class SubtitleWindow(QMainWindow):
    ################ Initialation ###############

    def __init__(self):
        super().__init__()
        self.initWindowStyling()
        self.initLabel()
        self.initMouseTracking()

    ################ Window Styling ###############

    def initWindowStyling(self):
        """Initializes window logic"""
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(2)  # allows resizing
        self.setGeometry(300, 100, 1000, 100)

    def updateWindowStyling(self):
        self.label.setStyleSheet(Profiles.getCurrentUserCSS())
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.update()

    ################ Subtitle text ###############

    def initLabel(self):
        self.label = QLabel("[Subtitles]",self)
        if Profiles.getCurrentUser() is None:
            self.openSettingsMenu()
        self.updateWindowStyling()
        
    def setSubtitleText(self, text):
        """
        updates subtitles to ensure they do not run of the screen
        needs updating to accomdate multiple lines of text
        """
        size = QFontMetrics(self.label.font())
        text_split = text.split(" ")
        while size.width(text) > self.width() and len(text_split) > 1:
            # removes the oldest word until it fits
            text_split = text.split(" ")
            text_split = text_split[1:]
            text = " ".join(text_split)
        self.label.setText(text)
        self.update()

    ################ MouseTracking (Move and Resize Window) ###############

    def initMouseTracking(self):
        self.setMouseTracking(True)
        self.dragging = False
        self.oldPosition = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            newPosition = event.globalPos()
            if self.oldPosition:
                difference = newPosition - self.oldPosition
                self.move(self.pos() + difference)
            self.oldPosition = newPosition

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.oldPosition = None

    ################ ContextMenu ###############

    def contextMenuEvent(self, event):
        """
        Create the context menu that allows user to switch between Transparency mode
        """
        contextMenu = QMenu()
        settingsAction = QAction("Settings")
        settingsAction.triggered.connect(self.openSettingsMenu)
        contextMenu.addAction(settingsAction)
        quit = QAction("Quit")
        contextMenu.addAction(quit)
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == quit:
            self.close()

    ################ ContextMenu ###############

    def openSettingsMenu(self):
        self.hide()
        self.userSelector = SettingsWindow("profile")
        self.userSelector.exec_()
        if Profiles.getCurrentUser() is None:
            sys.exit()
        self.updateWindowStyling()
        self.show()

    def resizeEvent(self, event):
        """Resizes the window ensure the label with the text stays the same"""
        super().resizeEvent(event)
        self.updateWindowStyling()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubtitleWindow()
    window.show()
    sys.exit(app.exec_())
