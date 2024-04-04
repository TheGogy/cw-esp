from PyQt5.QtWidgets import QApplication
import sys
import src.backend as backend

if __name__ == "__main__":
    app = QApplication(sys.argv)
    microphoneThread = backend.MicrophoneThread()
    microphoneThread.start()
    sys.exit(app.exec_())
