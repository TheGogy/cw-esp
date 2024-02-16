from zipfile import ZipFile
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from pathlib import Path
import requests
import yaml
import os
import re
class Profiles:
    ################ Database Queries ################

    ###PUBLIC###

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

    ###PRIVATE###

    def getUserPath(user = None):
        defaultPath = Profiles.getUserProfiles()["DefaultPath"] 
        return f"{defaultPath}/Users/{user}.css"

    def getUserProfiles():
        print("hello")
        appDirectory =  Path(str(Path(__file__).resolve().parent))
        profilesPath = f"{appDirectory}/Profiles.yml"
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
        appDirectory = str(Path(__file__).resolve().parent)
        with open(f"{appDirectory}/Profiles.yml", 'w') as file:
            yaml.dump(userProfiles, file)
    
    def addUser(user):
        userProfiles = Profiles.getUserProfiles()
        userProfiles['Users'].add(user)
        Profiles.saveProfilesFile(userProfiles)

    def generateDefaultSettings():
        userSettings = {}
        userSettings['color'] = "rgba(255,255,255,1)"
        userSettings['font-family'] = None
        userSettings['font-size'] = None
        return userSettings

    def saveUserProfile(user: str,currentUserSettings: dict):
        userProfilePath = Profiles.getUserPath(user)
        css_string = "QLabel {\n"
        for element in currentUserSettings.keys():
            css_string += f"{element}: {currentUserSettings[element]};\n"
        css_string += "}"
        with open(userProfilePath, 'w') as userFile:
            userFile.write(css_string)
        if not Profiles.userExists(user):
            Profiles.addUser(user)
        Profiles.setCurrentUser(user)

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
        print("hello")
        defaultPath = str(Path(__file__).resolve().parent) 
        data = {
            'Current': None,
            'Users': set(),
            'DefaultPath': None,
            'availableModels': {},
            'installedModels': set(),
            'CurrentModel': None,
        }
        userPath =  f"{defaultPath}/Users"
        if not os.path.exists(userPath):
            os.mkdir(userPath)
        data['DefaultPath'] = defaultPath
        modelPath = f"{defaultPath}/Models"
        if not os.path.exists(modelPath):
            os.mkdir(modelPath)
        data['availableModels'] = Profiles.generateAvailableModels()
        profilesPath = f"{defaultPath}/Profiles.yml"
        with open(profilesPath, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    def setCurrentUser(user):
        userProfiles = Profiles.getUserProfiles()
        userProfiles['Current'] = user
        Profiles.saveProfilesFile(userProfiles)

    def generateAvailableModels():
        availableModels = {}
        modelsUrl = "https://alphacephei.com/vosk/models"
        response = requests.get(modelsUrl)
        soup = BeautifulSoup(response.text,"html.parser")
        links = soup.select('a')
        for link in links:
            href = link.get('href')
            if re.match('\S*vosk-model\S*.zip',href):
                availableModels[link.get_text()] = href
        return availableModels
 
 
    def getModelUrls():
        return Profiles.getUserProfiles()['availableModels']

    def getAvailableModels():
        return list(Profiles.getUserProfiles()['availableModels'].keys())

    def getInstalledModels():
        return list(Profiles.getUserProfiles()['installedModels'])

    def installModel(modelName):
        try:
            modelUrl = Profiles.getModelUrls()[modelName]
        except KeyError:
            raise ValueError("Model not available.")
        filename = "Models/temp.zip"
        urlretrieve(modelUrl,filename)
        with ZipFile("Models/temp.zip", "r") as zObject:
            zObject.extractall("Models")
        os.remove("Models/temp.zip")
        profiles = Profiles.getUserProfiles()
        profiles['CurrentModel'] = modelName
        profiles['installedModels'].add(modelName)
        Profiles.saveProfilesFile(profiles)

    def getCurrentModelPath():
        profiles = Profiles.getUserProfiles()
        defaultPath = profiles["DefaultPath"]
        currentModel = profiles["CurrentModel"]
        if currentModel is not None:
            return f"{defaultPath}/Models/{currentModel}"
        else:
            return None

if __name__ == '__main__':
    Profiles.generateProfilesFile()
