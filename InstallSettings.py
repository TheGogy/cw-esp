from PyQt5.QtWidgets import QPushButton,QGridLayout,QVBoxLayout,QHBoxLayout,QComboBox,QLabel, QFormLayout
from PyQt5.QtCore import  pyqtSignal, QObject, pyqtSlot, QThread,Qt
import os
import re
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

class InstallSettings(QVBoxLayout):
    def __init__(self,installWorker):
        super().__init__()
        self.availableModels = Profiles.getAvailableModels()
        self.initInstallWorker(installWorker)
        self.formLayout = QFormLayout()
        self.initDropdownMenu()
        self.initNotes()
        self.addLayout(self.formLayout)
        self.addStretch(10)
        self.initButtons()

    def initInstallWorker(self,installWorker):
        self.installWorker = installWorker
        self.installWorker.signals.began.connect(self.modelChanged)
        self.installWorker.signals.finished.connect(self.modelChanged)
        self.installWorker.signals.interrupted.connect(self.modelChanged)

    def initDropdownMenu(self):
        currentModel = Profiles.getCurrentModel()
        self.modelSelector = QComboBox()
        self.modelSelector.setDuplicatesEnabled(False)
        if self.installWorker.isRunning():
            self.modelSelector.addItem(f"[{self.availableModels[self.installWorker.modelName][1]}] {self.installWorker.modelName}")
        elif currentModel in self.availableModels:
            self.modelSelector.addItem(f"[{self.availableModels[currentModel][1]}] {currentModel}")
        for model in sorted(self.availableModels.keys()):
            self.modelSelector.addItem(f"[{self.availableModels[model][1]}] {model}") 
        self.modelSelector.activated.connect(self.modelChanged)
        self.formLayout.addRow("Models:",self.modelSelector)
        self.formLayout.addRow(" ",None)

    def initNotes(self):
        availableModels = Profiles.getAvailableModels()
        gridLayout = QGridLayout()
        self.notes = QLabel(f"Notes:\n{availableModels[self.getCurrentModelText()][3]}")
        self.notes.setStyleSheet("font-size: 15px;background:rgba(0,0,0,0.2)")
        self.notes.setMinimumHeight(200)
        self.notes.setAlignment(Qt.AlignTop)
        self.license = QLabel(f"License: {availableModels[self.getCurrentModelText()][4]}")
        self.license.setStyleSheet("font-size: 18px;background:rgba(0,0,0,0.3)")
        self.license.setMaximumHeight(50)
        gridLayout.addWidget(self.notes,0,0,3,5,alignment=Qt.AlignTop)
        gridLayout.addWidget(self.license,2,4)
        self.formLayout.addRow(gridLayout)
        
    
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
        self.addLayout(buttonLayout)

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
    
    def updateNotesText(self):
        availableModels = Profiles.getAvailableModels()
        self.notes.setText(f"Notes:\n{availableModels[self.getCurrentModelText()][3]}")
        self.license.setText(f"License: {availableModels[self.getCurrentModelText()][4]}")

    def modelChanged(self):
        self.updateButtonText()
        self.updateNotesText()

    def getCurrentModelText(self):
        return re.findall(r'\[.*\] (.*)',self.modelSelector.currentText())[0]
