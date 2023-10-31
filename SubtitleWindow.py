import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMenu, QAction, QWidget, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
class SubtitleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        # set label which contains the subtitlese
        self.label = QLabel(self)
        self.label.setText("")
        self.label.setStyleSheet("font-size: 40px; color: Pink;")
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
        return super().resizeEvent(event)
    
    def contextMenuEvent(self, event):
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
        self.translucentMode = not self.translucentMode
        self.setAttribute(Qt.WA_TranslucentBackground,self.translucentMode)
        self.update()
        
    # if window is resized ensures that the label will stay the same size
    def resizeEvent(self, event):
        self.label.setGeometry(0,0,self.width(),self.height())
        self.update()
        
    # updates subtitles requires updating to accomdate multiple lines of text
    def setSubtitleText(self, text):
        text = self.label.text() +" " + text
        size = QFontMetrics(self.label.font())
        text_split = text.split(" ")
        while size.width(text) > self.width() and len(text_split) > 1:
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