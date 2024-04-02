from zipfile import ZipFile
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from pathlib import Path
import yaml
import sys
import os
import shutil
import requests

def getDownloadLinks(availableModels, url):
    content = requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
    rows = soup.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        if columns:
            link = columns[0].a
            if not link or len(columns) < 4:
                continue

            size = columns[1].text.strip()
            errorRate = columns[2].text.strip()
            notes = columns[3].text.strip()
            modelLicense = columns[4].text.strip()

            availableModels[link.get_text()] = [
                link.get("href"),
                size,
                errorRate,
                notes,
                modelLicense,
            ]

class Profiles:
    ################ Database Queries ################

    ###PUBLIC###
    def getAppDirectory():
        if hasattr(sys,'_MEIPASS'):
            return Path(os.path.dirname(sys.executable))
        else:
            return Path(__file__).resolve().parent

    def getStyleSheet():
        '''Opening and Reading Stylesheet'''
        filename =  Profiles.getAppDirectory() / "Styles" / "CssFile.qss"
        with open(str(filename),"r") as file:
            return file.read()


    def getCurrentUserCSS():
        with open(Profiles.getUserPath(Profiles.getCurrentUser()), "r") as file:
            return "".join(file.readlines())

    def getUserList():
        return list(Profiles.getUserProfiles()['Users'])

    def getCurrentUser():
        return Profiles.getUserProfiles()['Current']

    def getCurrentUserSettings():
        return Profiles.getUserSettings(Profiles.getCurrentUser())

    def userExists(user = None):
        return user in Profiles.getUserList()

    def getUserSettings(user = None):
        userProfiles = Profiles.getUserProfiles()
        if not Profiles.userExists(user):
            userSettings = Profiles.generateDefaultSettings()
        else:
            userSettings = {}
            with open(Profiles.getUserPath(user),"r") as cssFile:
                cssLines = cssFile.readlines()[1:-1]
                for line in cssLines:
                    entry = (line.strip()).split(": ")
                    userSettings[entry[0]] = entry[1][:-1]
        return userSettings

    def getDefaultPath():
        return Path(Profiles.getUserProfiles()["DefaultPath"])

    ###PRIVATE###

    def getUserPath(user = None):
        defaultPath = Path(Profiles.getUserProfiles()["DefaultPath"])
        return defaultPath / "Users" / f"{user}.css"

    def getUserProfiles():
        profilesPath =  Profiles.getAppDirectory() / "Profiles.yml"
        if not Path(profilesPath).exists():
            Profiles.generateProfilesFile()
        try:
            with open(profilesPath, "r") as profilesFile:
                profiles = yaml.safe_load(profilesFile)
        except (FileNotFoundError, yaml.YAMLError):
            Profiles.generateProfilesFile()
        with open(profilesPath, "r") as profilesFile:
            profiles = yaml.safe_load(profilesFile)
        return profiles

    ################ Data Editor  ################

    ###PUBLIC###

    def saveProfilesFile(userProfiles):
        profilesPath = Profiles.getAppDirectory() / "Profiles.yml"
        with open(profilesPath, 'w') as file:
            yaml.dump(userProfiles, file)

    def addUser(user):
        userProfiles = Profiles.getUserProfiles()
        userProfiles['Users'].add(user)
        Profiles.saveProfilesFile(userProfiles)

    def generateDefaultSettings():
        userSettings = {
            'color'            : "rgba(255,255,255,1)",
            'font-family'      : "Arial",
            'font-size'        : "12px",
            'background-color' : "rgba(0,0,0,0.2)",
            'border-radius'    : "0px"
        }
        return userSettings

    def saveUserProfile(user: str,currentUserSettings: dict):
        userProfilePath = Profiles.getUserPath(user)
        cssString = Profiles.convertToCSS(currentUserSettings)
        with open(userProfilePath, 'w') as userFile:
            userFile.write(cssString)
        if not Profiles.userExists(user):
            Profiles.addUser(user)
        Profiles.setCurrentUser(user)

    def convertToCSS(userSettings: dict):
        cssString = "QLabel {\n"
        for element in userSettings.keys():
            cssString += f"{element}: {userSettings[element]};\n"
        cssString += "}"
        return cssString

    def deleteUser(user: str):
        userProfiles = Profiles.getUserProfiles()
        if Profiles.userExists(user):
            os.remove(Profiles.getUserPath(user))
            userProfiles['Users'].remove(user)
            userProfiles['Current'] = None
            Profiles.saveProfilesFile(userProfiles)


    ''' Profiles.yml
    Current: currentUsername
    Users: set of current users
    DefaultPath: default path new users will be saved to
    '''
    def generateProfilesFile():
        defaultPath = Profiles.getAppDirectory()
        data = {
            'Current': None,
            'Users': set(),
            'DefaultPath': None,
            'availableModels': {},
            'installedModels': set(),
            'CurrentModel': None,
        }
        userPath =  defaultPath / "Users"
        if not os.path.exists(userPath):
            os.mkdir(userPath)
        data['DefaultPath'] = str(defaultPath)
        modelPath = defaultPath / "Models"
        if not os.path.exists(modelPath):
            os.mkdir(modelPath)
        data['availableModels'] = Profiles.generateAvailableModels()
        profilesPath = defaultPath / "Profiles.yml"
        with open(profilesPath, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    def setCurrentUser(user: str):
        userProfiles = Profiles.getUserProfiles()
        userProfiles['Current'] = user
        Profiles.saveProfilesFile(userProfiles)

    def generateAvailableModels():
        availableModels = {}
        modelsUrl = "https://alphacephei.com/vosk/models"
        getDownloadLinks(availableModels, modelsUrl)
        return availableModels


    def getModelUrls():
        return Profiles.getUserProfiles()['availableModels']

    def getAvailableModels():
        return Profiles.getUserProfiles()['availableModels']

    def getInstalledModels():
        return list(Profiles.getUserProfiles()['installedModels'])

    def getCurrentModel():
        return Profiles.getUserProfiles()['CurrentModel']

    def installModel(modelName: str):
        try:
            modelUrl = Profiles.getModelUrls()[modelName][0]
        except KeyError:
            raise ValueError("Model not available.")
        defaultPath = Profiles.getDefaultPath()
        filename = defaultPath / "Models" / "temp.zip"
        urlretrieve(modelUrl,filename)
        with ZipFile(filename, "r") as zObject:
            zObject.extractall("Models")
        os.remove(filename)
        profiles = Profiles.getUserProfiles()
        profiles['CurrentModel'] = modelName
        profiles['installedModels'].add(modelName)
        Profiles.saveProfilesFile(profiles)

    def getCurrentModelPath():
        profiles = Profiles.getUserProfiles()
        defaultPath = Path(profiles["DefaultPath"])
        currentModel = profiles["CurrentModel"]
        if currentModel is not None:
            return  defaultPath / "Models" / currentModel
        else:
            return None

    def deleteModel(modelName: str): 
        modelsFolder = Profiles.getDefaultPath() / "Models"
        profiles = Profiles.getUserProfiles()
        profiles['installedModels'].remove(modelName)
        profiles['CurrentModel'] = None
        Profiles.saveProfilesFile(profiles)
        shutil.rmtree(modelsFolder / modelName)

    def selectModel(modelName: str):
        profiles = Profiles.getUserProfiles()
        profiles['CurrentModel'] = modelName
        Profiles.saveProfilesFile(profiles)

    def emptyDatabase():
        if os.path.isfile("Profiles.yml"):
            os.remove("Profiles.yml")
        if os.path.isdir("Models"):
            shutil.rmtree("Models")
        if os.path.isdir("Users"):
            shutil.rmtree("Users")
if __name__ == '__main__':
    Profiles.generateProfilesFile()
