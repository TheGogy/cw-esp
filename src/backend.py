#!/usr/bin/env python3
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
from PyQt5.QtCore import QThread
import json
from src.SubtitleWindow import SubtitleWindow
from src.Profiles import Profiles
from src.SettingsWindow import SettingsWindow

"""This script processes audio input from the microphone and displays the transcribed text."""


class MicrophoneThread(QThread):
    def __init__(self):
        super().__init__()
        self.profiles = Profiles()
        if self.profiles.getCurrentModelPath() is None:
            settings = SettingsWindow("model",self.profiles)
            settings.exec_()
        if self.profiles.getCurrentModelPath() is None:
            sys.exit()
        self.window = SubtitleWindow(self.profiles)
        self.window.show()

    def run(self):
        # get the samplerate - this is needed by the Kaldi recognizer
        device_info = sd.query_devices(sd.default.device[0], "input")
        samplerate = int(device_info["default_samplerate"])

        # display the default input device

        # setup queue and callback function
        q = queue.Queue()

        def recordCallback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))

        # build the model and recognizer objects.
        model = Model(str(self.profiles.getCurrentModelPath()))
        recognizer = KaldiRecognizer(model, samplerate)
        recognizer.SetWords(False)

        try:
            with sd.RawInputStream(
                dtype="int16",
                channels=1,
                blocksize=8000,
                callback=recordCallback,
                samplerate=samplerate,
            ):
                while True:
                    data = q.get()
                    if not recognizer.AcceptWaveform(data):
                        partialResultDict = json.loads(recognizer.PartialResult())
                        if not partialResultDict.get("partial", "") == "":
                            self.window.setSubtitleText(partialResultDict["partial"])
                    else:
                        recognizer.Reset()

        except KeyboardInterrupt:
            print("===> Finished Recording")
        except Exception as e:
            print(str(e))

