from pathlib import Path
import yaml
import os
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
        defaultProfilePath = Profiles.getUserProfiles()["DefaultPath"] 
        return f"{defaultProfilePath}/{user}.css"

    def getUserProfiles():
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
        Profiles.setCurrentUser(user) #WHY ? 

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
        appDirectory = str(Path(__file__).resolve().parent) 
        data = {
            'Current': None,
            'Users': set(),
            'DefaultPath': None,
        }
        profilesPath = f"{appDirectory}/Profiles.yml"
        defaultPath =  f"{appDirectory}/Users"
        if not os.path.exists(defaultPath):
            os.mkdir(defaultPath)
        data['DefaultPath'] = defaultPath
        with open(profilesPath, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    def saveProfilesFile(userProfiles):
        appDirectory = str(Path(__file__).resolve().parent)
        with open(f"{appDirectory}/Profiles.yml", 'w') as file:
            yaml.dump(userProfiles, file)
    
    def addUser(user):
        userProfiles = Profiles.getUserProfiles()
        userProfiles['Users'].add(user)
        Profiles.saveProfilesFile(userProfiles)

    def setCurrentUser(user):
        userProfiles = Profiles.getUserProfiles()
        userProfiles['Current'] = user
        Profiles.saveProfilesFile(userProfiles)
