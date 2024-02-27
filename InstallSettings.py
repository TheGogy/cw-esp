from pathlib import Path
from PyQt5.QtWidgets import QApplication, QPushButton,QDialog,QFormLayout,QHBoxLayout,QVBoxLayout,QCompleter,QLineEdit,QSlider,QLabel,QComboBox
from PyQt5.QtCore import  pyqtSignal, QObject,QRect,QEvent,Qt,QRunnable,pyqtSlot,QThread
import sys
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
        self.kwargs = kwargs
        self.signals = InstallWorkerSignals()
        self.modelName = None

    @pyqtSlot()
    def run(self):
        self.signals.began.emit()
        Profiles.installModel(self.modelName)
        self.signals.finished.emit()

    def terminate(self):
        super().terminate()
        if os.path.exists("Models/temp.zip"):
            os.remove("Models/temp.zip")
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
        installedModels = Profiles.getInstalledModels()
        availableModels = Profiles.getAvailableModels()
        currentModel = Profiles.getCurrentModel()
        self.modelSelector = QComboBox()
        if self.installWorker.isRunning():
            availableModels.remove(self.installWorker.modelName)
            self.modelSelector.addItem(self.installWorker.modelName)
        elif currentModel in availableModels:
            availableModels.remove(currentModel)
            self.modelSelector.addItem(currentModel)
        for model in sorted(availableModels):
           self.modelSelector.addItem(model) 
        self.modelSelector.activated.connect(self.updateButtonText)
        self.addRow(self.modelSelector)

    def initButtons(self):
        self.installButton = QPushButton("")
        self.deleteButton = QPushButton("")
        self.installButton.clicked.connect(self.installFunction)
        self.deleteButton.clicked.connect(self.deleteButtonFunction)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.deleteButton,2)
        buttonLayout.addStretch(6)
        buttonLayout.addWidget(self.installButton,2)
        self.updateButtonText()
        self.addRow(buttonLayout)

    def installFunction(self):
        if self.modelSelector.currentText() in Profiles.getInstalledModels():
            return
        self.installWorker.modelName = self.modelSelector.currentText()
        self.installWorker.start()

    def deleteButtonFunction(self):
        if self.installWorker.isRunning():
            self.installWorker.terminate()
        elif self.modelSelector.currentText() in Profiles.getInstalledModels():   
            Profiles.deleteModel(self.modelSelector.currentText())
        self.updateButtonText()

    def updateButtonText(self):
        installedModels = Profiles.getInstalledModels()
        if self.installWorker.isRunning():
            self.deleteButton.setText("Cancel")
            self.installButton.setText("Installing")
            return
        if self.modelSelector.currentText() in installedModels:
            self.deleteButton.setText("Delete")
            self.installButton.setText("Installed")
            return
        if self.modelSelector.currentText() not in installedModels:
            self.deleteButton.setText("Delete")
            self.installButton.setText("Install")
            return



