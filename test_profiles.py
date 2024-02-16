# Import modules
from Profiles import Profiles
from pathlib import Path
import pytest
import yaml 
import unittest


# Set up test environment
print("[ + ] Setting up environment for testing")
RUNTIME_DIR = Path(__file__).parent



# Create test user css
with open(RUNTIME_DIR / "Users/test_user_1.css", "w") as f:
    f.write("""
QLabel {
color: rgba(195,78,92,0.85);
font-family: Fira Code;
font-size: 20px;
}
"""
)
with open(RUNTIME_DIR / "Users/test_user_2.css", "w") as f:
    f.write("""
QLabel {
color: rgba(43,43,43,1);
font-family: Arial;
font-size: 12px;
}
"""
)

with open(RUNTIME_DIR / "Users/test_user_delete.css", "w") as f:
    f.write("""
QLabel {
color: rgba(13,6,6,1);
font-family: Arial;
font-size: 12px;
}
"""
)

with open(RUNTIME_DIR / "Users/test_user_3.css", "w") as f:
    f.write("""
QLabel {
color: rgba(13,6,6,1);
font-family: Arial;
font-size: 12px;
}
"""
)


# Set current user to test user
with open(RUNTIME_DIR / "Profiles.yml", "w") as f:
    f.write(f"""
Current: test_user_1
DefaultPath: {str(RUNTIME_DIR / "Users")}
Users: !!set
  test_user_1: null
  test_user_2: null
  test_user_3: null 
  test_user_delete: null 
""")


# Profiles test class
class test_Profiles(unittest.TestCase):

    # Test Profiles.getCurrentUserCSS()
    def test_getCurrentUserCSS(self):
        test_user_1_cssData = """
QLabel {
color: rgba(195,78,92,0.85);
font-family: Fira Code;
font-size: 20px;
}
"""
        
        self.assertEqual(Profiles.getCurrentUserCSS(), test_user_1_cssData)



    # Test Profiles.getUserList()
    def test_getUserList(self):
        self.assertEqual(sorted(Profiles.getUserList()), ["test_user_1", "test_user_2","test_user_3","test_user_delete"])


    # Test Profiles.getCurrentUser()
    def test_getCurrentUser(self):
        self.assertEqual(Profiles.getCurrentUser(), "test_user_1")



    # Test Profiles.getCurrentUserSettings()
    def test_getCurrentUserSettings(self):
        test_user_1_cssData = """
QLabel {
color: rgba(195,78,92,0.85);
font-family: Fira Code;
font-size: 20px;
}
"""
        self.assertEqual(Profiles.getCurrentUserCSS(), test_user_1_cssData)


    # Test Profiles.userExists(user)
    def test_userExists(self):
        self.assertEqual(Profiles.userExists("test_user_1"), True)
        self.assertEqual(Profiles.userExists("test_user_2"), True)
        self.assertEqual(Profiles.userExists("fake_user"), False)

    

    # Test Profiles.getUserSettings(user)
    def test_getUserSettings(self):
        pass
        # Uncomment the test body once implemented
#         test_user_1_cssData = """
# QLabel {
# color: rgba(195,78,92,0.85);
# font-family: Fira Code;
# font-size: 20px;
# }
# """
#         test_user_2_cssData = """
# QLabel {
# color: rgba(43,43,43,1);
# font-family: Arial;
# font-size: 12px;
# }
# """
#         self.assertEqual(Profiles.getUserSettings("test_user_1"), test_user_1_cssData)
#         self.assertEqualp(Profiles.getUserSettings("test_user_2"), test_user_2_cssData)



    # Test Profiles.getUserPath(user)
    def test_getUserPath(self):
        self.assertEqual(str(RUNTIME_DIR / "Users/test_user_1.css"), Profiles.getUserPath("test_user_1"))
        self.assertEqual(str(RUNTIME_DIR / "Users/test_user_2.css"), Profiles.getUserPath("test_user_2"))



    # Test Profiles.getUserProfiles()
    def test_getUserProfiles(self):
        self.assertEqual({
            "Current": "test_user_1",
            "DefaultPath": str(RUNTIME_DIR / "Users"),
            "Users": {"test_user_1", "test_user_2","test_user_3", "test_user_delete"}
            },
        Profiles.getUserProfiles())

##############################################################################################

    # Test Profiles.generateDefaultSettings()
    def test_generateDefaultSettings(self):
        userSettings = {
            "color" : "rgba(255,255,255,1)",
            "font-family" : None,
            "font-size" : None
        }
        self.assertEqual(Profiles.generateDefaultSettings(), userSettings)


    # When we save a user profile why is it currently set to the current user.
    # Asynchronous? 
    # Functions Don't Contain Profile Functions.
    # Overwriting is currently causing conflicts.
    # Test Profiles.saveUserProfile(user, currentUserSettings)
    # def test_saveUserProfile(self):
    #     newUserSettings = {
    #         "color" : "rgba(255,255,255,1)",
    #         "font-family" : "Helvetica",
    #         "font-size" : 28
    #     }
    #     Profiles.saveUserProfile("test_user_3", newUserSettings)
    #     # savedUserSettings = Profiles.getUserSettings("test_user_3")
    #     userSettings = {}
    #     with open(Profiles.getUserPath("test_user_3"),"r") as cssFile:
    #         cssLines = cssFile.readlines()[1:-1]
    #         for line in cssLines:
    #             entry = (line.strip()).split(": ")
    #             userSettings[entry[0]] = entry[1][:-1]

    #     self.assertEqual(newUserSettings, userSettings)

    # def test_deleteUser(self):
    #     Profiles.deleteUser("test_user_delete")
    #     self.assertFalse(Profiles.userExists("test_user_delete"))
    #     #self.assertFalse("test_user_delete" in list(Profiles.getUserProfiles()['Users']))

    # def test_generateProfilesFile(self):
    #     Profiles.generateProfilesFile()
    #     self.assertTrue(Path("Profiles.yml").exists())

    # def test_saveProfilesFile(self):
    #     test_data = {
    #      "Current": "test_user_1",
    #      "DefaultPath": "default/path", 
    #      "Users": {"test_user_1"}
    #      }
    #     Profiles.saveProfilesFile(test_data)
    #     with open("Profiles.yml", "r") as f:
    #         saved_data = yaml.safe_load(f)
    #         print(saved_data)
    #     self.assertEqual(test_data, saved_data)

    # def test_addUser(self):
    #     Profiles.addUser("test_user_3")
    #     #self.assertTrue("test_user_3" in list(Profiles.getUserProfiles()['Users']))
    #     self.assertTrue(Profiles.userExists("test_user_3"))

    # def test_setCurrentUser(self):
    #     Profiles.setCurrentUser("test_user_2")
    #     self.assertEqual(Profiles.getCurrentUser(), "test_user_2")





















    # def test_deleteUser(self):
    #     pass


    # def test_generateProfilesFile(self):
    #     pass


    # def test_saveProfilesFile(self):
    #     pass


    # def test_addUser(self):
    #     pass


    # def test_setCurrentUser(self):
    #     pass