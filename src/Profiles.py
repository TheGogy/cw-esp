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
    def __init__(self,databaseDirectory = None):
        if databaseDirectory == None:
            self.databaseDirectory = Profiles.getAppDirectory()
        else:   
            self.databaseDirectory = Path(databaseDirectory)
        self.generateProfilesFile()

    def getAppDirectory():
        if hasattr(sys,'_MEIPASS'):
            return Path(os.path.dirname(sys.executable))
        else:
            return Path(__file__).resolve().parent

    def getDatabaseDirectory(self):
        return self.databaseDirectory
    def getStyleSheet(self):
        '''Opening and Reading Stylesheet'''
        filename = self.databaseDirectory / "Styles" / "CssFile.qss"
        with open(str(filename),"r") as file:
            return file.read()


    def getCurrentUserCSS(self):
        with open(self.getUserPath(self.getCurrentUser()), "r") as file:
            return "".join(file.readlines())

    def getUserList(self):
        return list(self.getUserProfiles()['Users'])

    def getCurrentUser(self):
        return self.getUserProfiles()['Current']

    def getCurrentUserSettings(self):
        return self.getUserSettings(self.getCurrentUser())

    def userExists(self,user = None):
        return user in self.getUserList()

    def getUserSettings(self,user = None):
        userProfiles = self.getUserProfiles()
        if not self.userExists(user):
            userSettings = Profiles.generateDefaultSettings()
        else:
            userSettings = {}
            with open(self.getUserPath(user),"r") as cssFile:
                cssLines = cssFile.readlines()[1:-1]
                for line in cssLines:
                    entry = (line.strip()).split(": ")
                    userSettings[entry[0]] = entry[1][:-1]
        return userSettings

    def getDefaultPath(self):
        return Path(self.getUserProfiles()["DefaultPath"])

    ###PRIVATE###

    def getUserPath(self,user = None):
        defaultPath = Path(self.getUserProfiles()["DefaultPath"])
        return defaultPath / "Users" / f"{user}.css"

    def getUserProfiles(self):
        profilesPath =  self.databaseDirectory / "Profiles.yml"
        if not Path(profilesPath).exists():
            Profiles.generateProfilesFile()
        try:
            with open(profilesPath, "r") as profilesFile:
                profiles = yaml.safe_load(profilesFile)
        except (FileNotFoundError, yaml.YAMLError):
            self.generateProfilesFile()
        with open(profilesPath, "r") as profilesFile:
            profiles = yaml.safe_load(profilesFile)
        return profiles

    ################ Data Editor  ################

    ###PUBLIC###

    def saveProfilesFile(self,userProfiles):
        profilesPath = self.databaseDirectory / "Profiles.yml"
        with open(profilesPath, 'w') as file:
            yaml.dump(userProfiles, file)

    def addUser(self,user):
        userProfiles = self.getUserProfiles()
        userProfiles['Users'].add(user)
        self.saveProfilesFile(userProfiles)

    def generateDefaultSettings():
        userSettings = {
            'color'            : "rgba(255,255,255,1)",
            'font-family'      : "Arial",
            'font-size'        : "12px",
            'background-color' : "rgba(0,0,0,0.2)",
            'border-radius'    : "0px"
        }
        return userSettings

    def saveUserProfile(self,user: str,currentUserSettings: dict):
        userProfilePath = self.getUserPath(user)
        cssString = self.convertToCSS(currentUserSettings)
        with open(userProfilePath, 'w') as userFile:
            userFile.write(cssString)
        if not self.userExists(user):
            self.addUser(user)
        self.setCurrentUser(user)

    def convertToCSS(self,userSettings: dict):
        cssString = "QLabel {\n"
        for element in userSettings.keys():
            cssString += f"{element}: {userSettings[element]};\n"
        cssString += "}"
        return cssString

    def deleteUser(self,user: str):
        userProfiles = self.getUserProfiles()
        if self.userExists(user):
            os.remove(self.getUserPath(user))
            userProfiles['Users'].remove(user)
            userProfiles['Current'] = None
            self.saveProfilesFile(userProfiles)


    ''' Profiles.yml
    Current: currentUsername
    Users: set of current users
    DefaultPath: default path new users will be saved to
    '''
    def generateProfilesFile(self):
        defaultPath = self.databaseDirectory
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
        if not os.path.exists(profilesPath):
            with open(profilesPath, 'w') as file:
                yaml.dump(data, file, default_flow_style=False)

    def setCurrentUser(self,user: str):
        userProfiles = self.getUserProfiles()
        userProfiles['Current'] = user
        self.saveProfilesFile(userProfiles)

    def generateAvailableModels():
        availableModels = {}
        modelsUrl = "https://alphacephei.com/vosk/models"
        getDownloadLinks(availableModels, modelsUrl)
        return availableModels


    def getModelUrls(self):
        return self.getUserProfiles()['availableModels']

    def getAvailableModels(self):
        return self.getUserProfiles()['availableModels']

    def getInstalledModels(self):
        return list(self.getUserProfiles()['installedModels'])

    def getCurrentModel(self):
        return self.getUserProfiles()['CurrentModel']

    def installModel(self,modelName):
        try:
            modelUrl = self.getModelUrls()[modelName][0]
        except KeyError:
            raise ValueError("Model not available.")
        defaultPath = self.getDatabaseDirectory()
        filename = defaultPath / "Models" / "temp.zip"
        urlretrieve(modelUrl,filename)
        with ZipFile(filename, "r") as zObject:
            zObject.extractall(defaultPath / "Models")
        os.remove(filename)
        profiles = self.getUserProfiles()
        profiles['CurrentModel'] = modelName
        profiles['installedModels'].add(modelName)
        self.saveProfilesFile(profiles)

    def getCurrentModelPath(self):
        profiles = self.getUserProfiles()
        defaultPath = Path(profiles["DefaultPath"])
        currentModel = profiles["CurrentModel"]
        if currentModel is not None:
            return  defaultPath / "Models" / currentModel
        else:
            return None

    def deleteModel(self,modelName: str): 
        modelsFolder = self.getDefaultPath() / "Models"
        profiles = self.getUserProfiles()
        profiles['installedModels'].remove(modelName)
        profiles['CurrentModel'] = None
        self.saveProfilesFile(profiles)
        shutil.rmtree(modelsFolder / modelName)

    def selectModel(self,modelName: str):
        profiles = self.getUserProfiles()
        profiles['CurrentModel'] = modelName
        self.saveProfilesFile(profiles)

if __name__ == '__main__':
    Profiles.generateProfilesFile()
