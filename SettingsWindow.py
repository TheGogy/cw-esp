from PyQt5.QtWidgets import QApplication, QPushButton,QDialog,QFormLayout,QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import  pyqtSignal, QObject, QTextStream, QFile

from Profiles import Profiles
from ProfileSettings import ProfileSettings
from InstallSettings import InstallSettings,InstallWorker 


class Communicate(QObject):
    closed = pyqtSignal(str) 

class SettingsWindow(QDialog):

    ################ Initialization ################

    def __init__(self, name=None):
        super().__init__()
        self.setGeometry(100,100,600,300)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.initLeftColumnLayout()
        self.leftColumnLayout = QFormLayout()
        self.installWorker = InstallWorker()
        if name == None:
            self.RightColumnLayout = ProfileSettings()
            self.RightColumnLayout.closed.connect(self.close)
            self.setWindowTitle("Settings Window")
        if name == "profile":
            self.RightColumnLayout = ProfileSettings()
            self.setWindowTitle("Create User.")
            self.RightColumnLayout.closed.connect(self.close)
        if name == "model":
            self.RightColumnLayout = InstallSettings(self.installWorker)
            self.setWindowTitle("Download a model.")
        self.layout.addLayout(self.leftColumnLayout,1)
        self.layout.addLayout(self.RightColumnLayout,9)
        self.communicate = Communicate()
        self.cssPath = Profiles.getAppDirectory() / "Styles" / "CssFile.qss"
        self.loadStylesheet(self.cssPath)


    def initLeftColumnLayout(self):
        self.leftColumnLayout = QHBoxLayout()
        self.profilesButton = QPushButton("Profiles",self)
        self.profilesButton.clicked.connect(self.initProfileSettings)
        self.leftColumnLayout.addWidget(self.profilesButton,2)
        self.modelsButton = QPushButton("Models",self)
        self.modelsButton.clicked.connect(self.initInstallSettings)
        self.leftColumnLayout.addWidget(self.modelsButton,2)
        self.leftColumnLayout.addStretch(6)
        self.layout.addLayout(self.leftColumnLayout)

    def initInstallSettings(self):
        if isinstance(self.RightColumnLayout,InstallSettings):
            return
        self.deleteLayout(self.RightColumnLayout)
        self.RightColumnLayout = InstallSettings(self.installWorker)
        self.layout.addLayout(self.RightColumnLayout,9)

    def initProfileSettings(self):
        if isinstance(self.RightColumnLayout,ProfileSettings):
            return
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
    import sys
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())
