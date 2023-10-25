import yaml
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
import sys
''' Profiles.yml
Current: currentUserName
Users: dictionary key = username, value = path/to/user
'''
def generateProfilesFile():
    pass

def userFileGenerator(path):
    pass
class UserSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,300,130)
        self.setWindowTitle("User Selection")
        self.selectUserButton = QPushButton("Select User",self)
        self.createUserButton = QPushButton("New User",self)
        self.deleteUserButton = QPushButton("Delete User",self)
        self.updateGeometry()
        
    def resizeEvent(self,event):
        super().resizeEvent(event)
        self.updateGeometry()
    
    def updateGeometry(self):
        self.selectUserButton.setGeometry(int(self.width() * 1/6),int(self.height() * 2/13),int(self.width() * 2 / 3),int(self.height()* 4/13))
        self.createUserButton.setGeometry(int(self.width() * 7.75/15),int(self.height() * 7/13),int(self.width() * 2/5),int(self.height() * 4/13))
        self.deleteUserButton.setGeometry(int(self.width() * 1.25/15),int(self.height() * 7/13),int(self.width() * 2/5),int(self.height() * 4/13))
        self.update()
    
    def selectUser(self):
        pass
    
    def createUser(self):
        pass
    
    def deleteUser(self):
        pass
    
def getUserPreferences():
    profilesPath = Path.cwd() + "/Profiles.yml"
    try:
        with open(profilesPath, "r") as profilesFile:
            profiles = yaml.safe_load(profilesFile)
    except (FileNotFoundError, yaml.YAMLError):
        generateProfilesFile()
    if profiles['Current'] is None:
        user = UserSelector(profiles)    
    user = profiles[profiles['Current']]
    with open(user,"wr") as userPreferences:
        userPreferences = yaml.safe_load(userPreferences)
        # add something to update usersPath to current dir
        return userPreferences
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserSelector()
    window.show()
    sys.exit(app.exec_())