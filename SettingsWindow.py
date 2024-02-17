from pathlib import Path
from PyQt5.QtWidgets import QApplication, QPushButton,QDialog,QFormLayout,QHBoxLayout,QVBoxLayout,QCompleter,QLineEdit,QSlider,QLabel,QComboBox
from PyQt5.QtCore import  pyqtSignal, QObject,QRect,QEvent,Qt,QRunnable,pyqtSlot,QThreadPool
from PyQt5.QtGui import QFontDatabase,QDoubleValidator
import sys
import re
from Profiles import Profiles
from ProfileSettings import ProfileSettings
from InstallSettings import InstallSettings 

class Communicate(QObject):
    closed = pyqtSignal(str) 

class SettingsWindow(QDialog):
   
   ################ Initialization ################

    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,400,200)
        self.setWindowTitle("User Selection")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.leftColumnLayout = QFormLayout()
        self.RightColumnLayout = ProfileSettings()
        self.RightColumnLayout.closed.connect(self.close)
        self.layout.addLayout(self.leftColumnLayout,1)
        self.layout.addLayout(self.RightColumnLayout,9)
        self.initLeftColumnLayout()
        self.communicate = Communicate()
        self.threadpool = QThreadPool()

    def initLeftColumnLayout(self):
        self.leftColumnExpanded = False
        self.collapseButton = QPushButton("",self)
        self.textPromptLayout = QFormLayout()
        self.setMinimumWidth(1)
        self.collapseButton.clicked.connect(self.collapsebuttonFunction)
        self.leftColumnLayout.addRow(self.collapseButton)
        self.profilesButton = QPushButton("P",self)
        self.profilesButton.setMinimumWidth(1)
        self.profilesButton.clicked.connect(self.initProfileSttings)
        self.leftColumnLayout.addRow(self.profilesButton)
        self.modelsButton = QPushButton("M",self)
        self.modelsButton.setMinimumWidth(1)
        self.modelsButton.clicked.connect(self.initInstallSettings)
        self.leftColumnLayout.addRow(self.modelsButton)

    def collapsebuttonFunction(self):
        if not self.leftColumnExpanded:
            self.layout.setStretch(1,3)
            self.modelsButton.setText("Models")
            self.profilesButton.setText("Profiles")
        else:
            self.layout.setStretch(1,9)
            self.modelsButton.setText("M")
            self.profilesButton.setText("P")
        self.leftColumnExpanded = not self.leftColumnExpanded
 
    def initInstallSettings(self):
        self.deleteLayout(self.RightColumnLayout)
        self.RightColumnLayout = InstallSettings(self.threadpool)
        self.layout.addLayout(self.RightColumnLayout,9)

    def initProfileSttings(self):
        self.deleteLayout(self.RightColumnLayout)
        self.RightColumnLayout = ProfileSettings()
        self.layout.addLayout(self.RightColumnLayout,9)

    def deleteLayout(self, layout):
        for i in reversed(range(layout.count())):
            if layout.itemAt(i).layout() is not None:
                childLayout = layout.itemAt(i)
                self.deleteLayout(childLayout.layout())
                childLayout.setParent(None)
                childLayout.layout().deleteLater()
            elif layout.itemAt(i).widget() is not None:
                widget = layout.itemAt(i).widget()
                widget.setParent(None)
                widget.deleteLater()
        layout.deleteLater()

    def closeEvent(self,event):
        print("Test")
        self.threadpool.clear()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())
