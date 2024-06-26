from PyQt5.QtWidgets import QApplication, QPushButton,QDialog,QFormLayout,QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import  pyqtSignal, QObject, QTextStream, QFile

from src.Profiles import Profiles
from src.ProfileSettings import ProfileSettings
from src.InstallSettings import InstallSettings,InstallWorker 


class Communicate(QObject):
    closed = pyqtSignal(str) 

class SettingsWindow(QDialog):

    ################ Initialization ################

    def __init__(self, name=None,profiles = None):
        super().__init__()
        if profiles is not None:
            self.profiles = profiles
        else:
            self.profiles = Profiles()
        self.setGeometry(100,100,835,560)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.initLeftColumnLayout()
        self.leftColumnLayout = QFormLayout()
        self.installWorker = InstallWorker(self.profiles)
        if name == None:
            self.RightColumnLayout = ProfileSettings(self.profiles)
            self.RightColumnLayout.closed.connect(self.close)
            self.setWindowTitle("Settings Window")
        if name == "profile":
            self.RightColumnLayout = ProfileSettings(self.profiles)
            self.setWindowTitle("Create User.")
            self.RightColumnLayout.closed.connect(self.close)
        if name == "model":
            self.RightColumnLayout = InstallSettings(self.installWorker,self.profiles)
            self.setWindowTitle("Download a model.")

        self.layout.addLayout(self.leftColumnLayout,1)
        self.layout.addLayout(self.RightColumnLayout,100)
        self.communicate = Communicate()
        self.setStyleSheet(self.profiles.getStyleSheet())

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
        self.RightColumnLayout = InstallSettings(self.installWorker,self.profiles)
        self.layout.addLayout(self.RightColumnLayout,100)

    def initProfileSettings(self):
        if isinstance(self.RightColumnLayout,ProfileSettings):
            return
        self.deleteLayout(self.RightColumnLayout)
        self.RightColumnLayout = ProfileSettings(self.profiles)
        self.RightColumnLayout.closed.connect(self.close)
        self.layout.addLayout(self.RightColumnLayout,100)


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
        self.installWorker.terminate()
        event.accept()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())
