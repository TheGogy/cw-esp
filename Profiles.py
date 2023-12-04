from pathlib import Path
import yaml
import os
class Profiles:
    def saveUserProfile(userProfiles,currentUserSettings):
        if userProfiles['Current'] is None:
            raise TypeError("There must be a current user Current user is None")
        userFilePath = userProfiles['Users'][userProfiles['Current']]
        css_string = "QLabel {\n"
        for element in currentUserSettings.keys():
            css_string += element + ": " + currentUserSettings[element] + ";\n"
        css_string += "}"
        with open(userFilePath, 'w') as userFile:
            userFile.write(css_string)
        Profiles.saveProfilesFile(userProfiles)
        

    ''' Profiles.yml
    Current: currentUsername
    Users: dictionary key = username, value = path/to/user
    DefaultPath: default path new users will be saved to
    '''
    def generateProfilesFile():
        data = {
        'Current': None,
        'Users': {},
        'DefaultPath': None,
        }
        profilesPath = str(Path(__file__).resolve().parent) + "/Profiles.yml"
        defaultPath = str(Path(__file__).resolve().parent) + "/Users"
        if not os.path.exists(defaultPath):
            os.mkdir(defaultPath)
        data['DefaultPath'] = defaultPath
        with open(profilesPath, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    def getUserProfiles():
        profilesPath = Path(str(Path(__file__).resolve().parent) + "/Profiles.yml")
        if not profilesPath.exists():
            Profiles.generateProfilesFile()
        try:
            with open(profilesPath, "r") as profilesFile:
                profiles = yaml.safe_load(profilesFile)
        except (FileNotFoundError, yaml.YAMLError):
            Profiles.generateProfilesFile()
        with open(profilesPath, "r") as profilesFile:
                profiles = yaml.safe_load(profilesFile)
        return profiles
    
    def getUserSettingDictionary(userProfiles,user = None):
        if user is None:
            user = userProfiles['Current']
        if user is None or user not in userProfiles['Users']:
            userSettings = {}
            userSettings['color'] = "rgba(0,0,0,0)"
            userSettings['font-family'] = None
            userSettings['font-size'] = None
        else:
            userSettings = {}
            with open(userProfiles['Users'][user],"r") as cssFile:
                cssLines = cssFile.readlines()[1:-1]
                for line in cssLines:
                    entry = (line.strip()).split(": ")
                    userSettings[entry[0]] = entry[1][:-1]
        return userSettings
    
    def saveProfilesFile(userProfiles):
        with open(str(Path(__file__).resolve().parent) + "/Profiles.yml", 'w') as file:
            yaml.dump(userProfiles, file)
    
    def getUserSettings(userProfiles, user = None):
        if user is None:
            user = userProfiles['Current']
        with open(userProfiles['Users'][user],"r") as cssFile:
            return "".join(cssFile.readlines())