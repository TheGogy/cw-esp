# Universal Subtitle Program 
A simple tool that allows users to generate subtitles from spoken language.

![screenshot](ExImage.jpg?raw=true "Screenshot of application")

- [Overview](#overview)
- [Compiling from source](#compiling)
- [Features](#features)

## Overview
We aim to bridge the gap by providing customisable subtitles for all types of video content. The system works to accurately interpret audio and generate subtitles on the user's device, aiming to support full comprehension of video content for individuals with diverse needs.

## Compiling from source
We recommend compiling from source for speed, efficiency and download size.
After cloning the repository, you can generate an exacutable by running:
```sh
pyinstaller main.py SettingsWindow.py Profiles.py SubtitleWindow.py --noconsole --collect-all vosk --onefile --icon=Cabbage.ico
```

## Features
- [x] Detect audio from microphone and render subtitles
- [x] Full customisability, including:
  - [x] - Colours (text + background)
  - [x] - Fonts + sizes
  - [x] - Rounding
- [x] - Fully built-in model downloader + selecter
- [x] - Support for multiple profiles 
  
- [ ] - Transcribe audio from files
- [ ] - Render subtitles from computer audio
