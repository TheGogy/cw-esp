from PyQt5.QtWidgets import QApplication, QPushButton,QDialog,QFormLayout,QHBoxLayout
from PyQt5.QtCore import  pyqtSignal, QObject, QTextStream, QFile

import sys
from pathlib import Path
from Profiles import Profiles
from ProfileSettings import ProfileSettings
from InstallSettings import InstallSettings,InstallWorker 


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
        self.installWorker = InstallWorker()
        self.cssPath = Path(__file__).parent / "Styles/css_file.qss"
        self.loadStylesheet(self.cssPath)


    def initLeftColumnLayout(self):
        self.leftColumnExpanded = False
        self.collapseButton = QPushButton("",self)
        self.textPromptLayout = QFormLayout()
        self.setMinimumWidth(1)
        self.collapseButton.clicked.connect(self.collapsebuttonFunction)
        self.leftColumnLayout.addRow(self.collapseButton)
        self.profilesButton = QPushButton("P",self)
        self.profilesButton.setMinimumWidth(1)
        self.profilesButton.clicked.connect(self.initProfileSettings)
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
        if isinstance(self.RightColumnLayout,InstallSettings):
            return
        self.deleteLayout(self.RightColumnLayout)
        self.RightColumnLayout = InstallSettings(self.installWorker)
        if self.leftColumnExpanded:
            self.layout.addLayout(self.RightColumnLayout,3)
        else:
            self.layout.addLayout(self.RightColumnLayout,9)

    def initProfileSettings(self):
        if isinstance(self.RightColumnLayout,ProfileSettings):
            return
        self.deleteLayout(self.RightColumnLayout)
        self.RightColumnLayout = ProfileSettings()
        if self.leftColumnExpanded:
            self.layout.addLayout(self.RightColumnLayout,3)
        else:
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

    def loadStylesheet(self, filename):
        '''Opening and Reading Stylesheet'''
        style_file = QFile(str(filename))
        if not style_file.open(QFile.ReadOnly | QFile.Text):
            print("error - can't open css_file :", filename)
            return
        else:
            print("opened successfully:", filename)

        stream = QTextStream(style_file)
        stylesheet_content = stream.readAll()
        self.setStyleSheet(stylesheet_content)


    def closeEvent(self,event):
        self.installWorker.terminate()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())
