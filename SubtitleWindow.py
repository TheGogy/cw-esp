import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMenu, QAction, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from pathlib import Path
import Profiles
import yaml
import os

class SubtitleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #recieves userProfiles if unsuccessful then quits the application
        self.profiles = Profiles.getUserProfiles()
        if self.profiles['Current'] is None:
            self.userSelector = Profiles.UserSelector(self.profiles)
            self.userSelector.exec_()
        self.profiles = Profiles.getUserProfiles()
        if self.profiles['Current'] is None:
            sys.exit()
        else:
            with open(self.profiles['Users'][self.profiles['Current']],"r") as userFile: #Opens Current User File I know its cursed plz somebody fix
                self.css = userFile.read()
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
        self.label.setStyleSheet(self.css)
        self.label.setGeometry(0, 0, self.width(), self.height())

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
        
    # if window is resized ensures that the label will stay the same size
    def resizeEvent(self, event):
        self.label.setGeometry(0,0,self.width(),self.height())
        self.update()
        
    def setSubtitleText(self, text):
        '''
        updates subtitles ensure they do not run of the screen\n
        needs updating to accomdate multiple lines of text
        '''
        if self.label.text() == "[Subtitles]":
            pass
        else:
            text = self.label.text() + " " + text
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