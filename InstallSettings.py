import yaml
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QPushButton,QDialog,QFormLayout,QHBoxLayout,QVBoxLayout,QCompleter,QLineEdit,QSlider,QLabel,QComboBox
from PyQt5.QtCore import  pyqtSignal, QObject,QRect,QEvent,Qt,QRunnable,pyqtSlot,QThreadPool
from PyQt5.QtGui import QFontDatabase,QDoubleValidator
import sys
import re
from Profiles import Profiles

class installWorkerSignals(QObject):
    finished = pyqtSignal()
    began = pyqtSignal()

class installWorker(QRunnable):
    def __init__(self, *args,**kwargs):
        super(installWorker,self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals =installWorkerSignals()

    @pyqtSlot()
    def run(self):
        self.signals.began.emit()
        Profiles.installModel(self.args[0])
        self.signals.finished.emit()


class InstallSettings(QFormLayout):
    def __init__(self,threadpool):
        super().__init__()
        self.threadpool = threadpool
        installedModels = Profiles.getInstalledModels()
        availableModels = Profiles.getAvailableModels()
        self.modelSelector = QComboBox()
        for model in sorted(availableModels):
           self.modelSelector.addItem(model) 
        self.addRow(self.modelSelector)
        installButton = QPushButton("install")
        installButton.clicked.connect(self.installFunction)
        self.addRow(installButton)

    def installFunction(self):
        worker = installWorker(self.modelSelector.currentText())
        worker.signals.began.connect(self.installStarted)
        worker.signals.finished.connect(self.installCompleted)
        self.threadpool.start(worker)

    def installStarted(self):
        print("BEGANNN")

    def installCompleted(self):
        print("FIIIINNNNNNIIIIISSSSSSHEEEEDDD")
