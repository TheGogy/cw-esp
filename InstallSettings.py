import yaml
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

class InstallWorker(QThread):
    def __init__(self, *args,**kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = InstallWorkerSignals()
        self.modelName = None

    @pyqtSlot()
    def run(self):
        self.signals.began.emit()
        Profiles.installModel(self.modelName)
        self.signals.finished.emit()

    def terminate(self):
        if os.path.exists("Models/temp.zip"):
            os.remove("Models/temp.zip") 
        super().terminate()

class InstallSettings(QFormLayout):
    def __init__(self,installWorker):
        super().__init__()
        self.installWorker = installWorker
        installedModels = Profiles.getInstalledModels()
        availableModels = Profiles.getAvailableModels()
        self.modelSelector = QComboBox()
        for model in sorted(availableModels):
           self.modelSelector.addItem(model) 
        self.addRow(self.modelSelector)
        if self.installWorker.isRunning():
            self.installButton = QPushButton("Installing")
        else:
            self.installButton = QPushButton("Install")
        self.installButton.clicked.connect(self.installFunction)
        self.addRow(self.installButton)

    def installFunction(self):
        self.installWorker.modelName = self.modelSelector.currentText()
        self.installWorker.signals.began.connect(self.installStarted)
        self.installWorker.signals.finished.connect(self.installCompleted)
        self.installWorker.start()

    def installStarted(self):
        self.installButton.setText("Installing")

    def installCompleted(self):
        self.installButton.setText("Installed")
