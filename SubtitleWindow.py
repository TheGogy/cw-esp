import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMenu, QAction, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from Profiles import Profiles
from SettingsWindow import SettingsWindow

class SubtitleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #recieves userProfiles if unsuccessful then quits the application
        currentUser = Profiles.getCurrentUser()
        if currentUser is None:
            self.openSettingsMenu()
        else:
            self.css = Profiles.getCurrentUserCSS()
        # Set window properties
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(2) # allows resizing
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setGeometry(300, 100, 1000, 100)
        self.setMouseTracking(True)
        # variable for clicking / translucent mode 
        self.dragging = False
        self.oldPosition = None
        self.translucentMode = True
        # set label which contains the subtitles
        self.label = QLabel(self)
        self.label.setText("[Subtitles]")
        self.label.setStyleSheet(self.css)
        self.label.setGeometry(0, 0, self.width(), self.height())

        # load the style sheet 
        # self.loadStylesheet("cw-esp-1/styles /css_file.css")

    #MouseEvents implement window movement without having to have a window with a frame 
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

    def resizeEvent(self, event):
        '''Resizes the window ensure the label with the text stays the same'''
        super().resizeEvent(event)
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.update()
    
    def contextMenuEvent(self, event):
        '''
        Create the context menu that allows user to switch between Transparency mode
        
        '''
        contextMenu = QMenu(self)
        #transpancy
        translucent = QAction("",self)
        translucent.triggered.connect(self.switchTransparencyMode)
        if self.translucentMode:
            translucent.setText("Enable Translucent Background")
        else:
            translucent.setText("Disable Translucent Background")
        contextMenu.addAction(translucent)
        settingsAction = QAction("Settings",self)
        settingsAction.triggered.connect(self.openSettingsMenu)
        contextMenu.addAction(settingsAction)
        #quit
        quit = QAction("Quit")
        contextMenu.addAction(quit)
        
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == quit:
            self.close()
            
    def switchTransparencyMode(self):
        '''Transparency mode works on windows not make not sure why'''
        self.translucentMode = not self.translucentMode
        self.setAttribute(Qt.WA_TranslucentBackground,self.translucentMode)
        self.update()
    
    def openSettingsMenu(self):
        self.hide()
        self.userSelector = SettingsWindow()
        self.userSelector.exec_()
        if Profiles.getCurrentUser() is None:
            sys.exit()
        else:
            self.css = Profiles.getCurrentUserCSS()
        self.label.setText("[Subtitles]")
        self.label.setStyleSheet(self.css)
        self.show()

    # if window is resized ensures that the label will stay the same size
    def resizeEvent(self, event):
        self.label.setGeometry(0,0,self.width(),self.height())
        self.update()
        
    def setSubtitleText(self, text):
        '''
        updates subtitles to ensure they do not run of the screen\n
        needs updating to accomdate multiple lines of text
        '''
        if self.label.text() == "[Subtitles]":
            pass
        size = QFontMetrics(self.label.font())
        text_split = text.split(" ")
        while size.width(text) > self.width() and len(text_split) > 1: #removes the oldest word until it fits
            text_split = text.split(" ")
            text_split = text_split[1:]
            text = " ".join(text_split)
        self.label.setText(text)
        self.update()
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubtitleWindow()
    window.show()
    sys.exit(app.exec_())

