from PyQt5.QtWidgets import QPushButton,QFormLayout,QHBoxLayout,QComboBox
from PyQt5.QtCore import  pyqtSignal, QObject, pyqtSlot, QThread
import os
from Profiles import Profiles

class InstallWorkerSignals(QObject):
    finished = pyqtSignal()
    began = pyqtSignal()
    interrupted = pyqtSignal()

class InstallWorker(QThread):
    def __init__(self):
        super().__init__()
        self.signals = InstallWorkerSignals()
        self.modelName = None

    @pyqtSlot()
    def run(self):
        self.signals.began.emit()
        Profiles.installModel(self.modelName)
        self.signals.finished.emit()

    def terminate(self):
        super().terminate()
        if os.path.exists(Profiles.getAppDirectory() / "Models"/ "temp.zip"):
            os.remove(Profiles.getAppDirectory()/ "Models" / "temp.zip")
        self.signals.interrupted.emit()

class InstallSettings(QFormLayout):
    def __init__(self,installWorker):
        super().__init__()
        self.initInstallWorker(installWorker)
        self.initDropdownMenu()
        self.initButtons()

    def initInstallWorker(self,installWorker):
        self.installWorker = installWorker
        self.installWorker.signals.began.connect(self.updateButtonText)
        self.installWorker.signals.finished.connect(self.updateButtonText)
        self.installWorker.signals.interrupted.connect(self.updateButtonText)

    def initDropdownMenu(self):
        availableModels = Profiles.getAvailableModels()
        print(availableModels)
        currentModel = Profiles.getCurrentModel()
        self.modelSelector = QComboBox()
        self.modelSelector.setDuplicatesEnabled(False)
        if self.installWorker.isRunning():
            self.modelSelector.addItem(f"[{availableModels[self.installWorker.modelName][1]}] {self.installWorker.modelName}")
        elif currentModel in availableModels:
            self.modelSelector.addItem(f"[{availableModels[currentModel][1]}] {currentModel}")
        for model in sorted(availableModels.keys()):
            self.modelSelector.addItem(f"[{availableModels[model][1]}] {model}") 
        self.modelSelector.activated.connect(self.updateButtonText)
        self.addRow(self.modelSelector)

    def initButtons(self):
        self.installButton = QPushButton()
        self.deleteButton = QPushButton()
        self.installButton.clicked.connect(self.installFunction)
        self.deleteButton.clicked.connect(self.deleteButtonFunction)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.deleteButton,2)
        buttonLayout.addStretch(6)
        buttonLayout.addWidget(self.installButton,2)
        self.updateButtonText()
        self.addRow(buttonLayout)

    def installFunction(self):
        if self.getCurrentModelText() in Profiles.getInstalledModels():
            Profiles.selectModel(self.getCurrentModelText())
            return
        self.installWorker.modelName = self.getCurrentModelText()
        self.installWorker.start()

    def deleteButtonFunction(self):
        if self.installWorker.isRunning():
            self.installWorker.terminate()
        elif self.getCurrentModelText() in Profiles.getInstalledModels():   
            Profiles.deleteModel(self.getCurrentModelText())
        self.updateButtonText()

    def updateButtonText(self):
        installedModels = Profiles.getInstalledModels()
        if self.installWorker.isRunning():
            self.deleteButton.setText("Cancel")
            self.installButton.setText("Installing")
            return
        if self.getCurrentModelText() in installedModels:
            self.deleteButton.setText("Delete")
            self.installButton.setText("Select")
            return
        if self.getCurrentModelText() not in installedModels:
            self.deleteButton.setText("Delete")
            self.installButton.setText("Install")
            return

    def getCurrentModelText(self):
        return re.findall(r'\[.*\] (.*)',self.modelSelector.currentText())[0]
