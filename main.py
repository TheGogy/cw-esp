#!/usr/bin/env python3
import os
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread
import json
from pathlib import Path
import SubtitleWindow
'''This script processes audio input from the microphone and displays the transcribed text.'''


class MicrophoneThread(QThread):
    def __init__(self, window):
        super().__init__()
        self.window = window
    def run(self):
        # list all audio devices known to your system
        print("Display input/output devices")
        print(sd.query_devices())


        # get the samplerate - this is needed by the Kaldi recognizer
        device_info = sd.query_devices(sd.default.device[0], 'input')
        samplerate = int(device_info['default_samplerate'])

        # display the default input device
        print("===> Initial Default Device Number:{} Description: {}".format(sd.default.device[0], device_info))

        # setup queue and callback function
        q = queue.Queue()

        def recordCallback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))

        # build the model and recognizer objects.
        print("===> Build the model and recognizer objects.  This will take a few minutes.")
        modelPath = os.getcwd() +  "/models/vosk-model-small-en-us-0.15"
        model = Model(modelPath)
        recognizer = KaldiRecognizer(model, samplerate)
        recognizer.SetWords(False)

        print("===> Begin recording. Press Ctrl+C to stop the recording ")
        try:
            with sd.RawInputStream(dtype='int16',
                                channels=1,

                                callback=recordCallback):
                while True:
                    data = q.get()
                    if recognizer.AcceptWaveform(data):
                        recognizerResult = recognizer.Result()
                        resultDict = json.loads(recognizerResult)
                        if not resultDict.get("text", "") == "":
                            print(resultDict["text"])
                            self.window.setSubtitleText(resultDict["text"])
                        else:
                            print("no input sound")

        except KeyboardInterrupt:
            print('===> Finished Recording')
        except Exception as e:
            print(str(e))

app = QApplication(sys.argv)
window = SubtitleWindow.SubtitleWindow()
window.show()
microphoneThread = MicrophoneThread(window)
microphoneThread.start()
sys.exit(app.exec_())