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
        self.setWindowFlag(Qt.WindowStaysOnTopHint) # window to always be on top
        self.setGeometry(300, 100, 1000, 100)  # (x,y,width,height)
        self.setMouseTracking(True)
        
        
        # variable for clicking
        self.dragging = False
        self.oldPosition = None
        self.translucentMode = True
        # set up fonts
        self.label = QLabel(self)
        self.label.setText("Your subtitle text")
        self.label.setStyleSheet("font-size: 40px; color: Pink;")
        self.label.setGeometry(0, 0, self.width(), self.height())

    #Button events 
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
        transparency = QAction("",self)
        transparency.triggered.connect(self.switchTransparencyMode)
        if self.translucentMode:
            transparency.setText("Enter Transparency Mode")
        else:
            transparency.setText("Exit Transparency Mode")
        contextMenu.addAction(transparency)
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
             
    def resizeEvent(self, event):
        self.label.setGeometry(0,0,self.width(),self.height())
        
   

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