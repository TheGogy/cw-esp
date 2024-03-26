# Import modules
from Profiles import Profiles
from pathlib import Path
import pytest
import yaml
import unittest

# Set up test environment
RUNTIME_DIR = Path(__file__).parent

# Create test user css
with open(RUNTIME_DIR / "Users/test_user_1.css", "w") as f:
    f.write("""
QLabel {
color: rgba(195,78,92,0.85);
font-family: Fira Code;
font-size: 20px;
background-color: rgba(0, 0, 0, 0);
border-radius: 10px;
}
"""
)

with open(RUNTIME_DIR / "Users/test_user_2.css", "w") as f:
    f.write("""
QLabel {
color: rgba(43,43,43,1);
font-family: Arial;
font-size: 12px;
background-color: rgba(10, 10, 10, 0);
border-radius: 10px;
}
"""
)
    
with open(RUNTIME_DIR / "Users/test_user_3.css", "w") as f:
    f.write("""
QLabel {
color: rgba(13,6,6,1);
font-family: Arial;
font-size: 12px;
background-color: rgba(20, 20, 20, 0);
border-radius: 10px;
}
"""
)

with open(RUNTIME_DIR / "Users/test_user_delete.css", "w") as f:
    f.write("""
QLabel {
color: rgba(13,6,6,1);
font-family: Arial;
font-size: 12px;
background-color: rgba(0, 0, 0, 0);
border-radius: 10px;
}
"""
)

# Set current user to test user
with open(RUNTIME_DIR / "Profiles.yml", "w") as f:
    f.write(f"""
Current: test_user_1
DefaultPath: {str(RUNTIME_DIR)}
Users: !!set
  test_user_1: null
  test_user_2: null
  test_user_3: null
  test_user_delete: null
"""
)

# Profiles test class
class test_Profiles(unittest.TestCase):

    @pytest.mark.order(1)
    # Test Profiles.getCurrentUserCSS()
    def test_getCurrentUserCSS(self):
        test_user_1_cssData = """
QLabel {
color: rgba(195,78,92,0.85);
font-family: Fira Code;
font-size: 20px;
background-color: rgba(0, 0, 0, 0);
border-radius: 10px;
}
"""
        self.assertEqual(Profiles.getCurrentUserCSS(), test_user_1_cssData)

    @pytest.mark.order(2)
    # Test Profiles.getUserList()
    def test_getUserList(self):
        self.assertEqual(sorted(Profiles.getUserList()), ["test_user_1", "test_user_2", "test_user_3", "test_user_delete"])

    @pytest.mark.order(3)
    # Test Profiles.getCurrentUser()
    def test_getCurrentUser(self):
        self.assertEqual(Profiles.getCurrentUser(), "test_user_1")

    # Test Profiles.getCurrentUserSettings()
    @pytest.mark.order(4)
    def test_getCurrentUserSettings(self):
        test_user_1_cssData = """
QLabel {
color: rgba(195,78,92,0.85);
font-family: Fira Code;
font-size: 20px;
background-color: rgba(0, 0, 0, 0);
border-radius: 10px;
}
"""
        self.assertEqual(Profiles.getCurrentUserCSS(), test_user_1_cssData)

    @pytest.mark.order(5)
    # Test Profiles.userExists(user)
    def test_userExists(self):
        self.assertEqual(Profiles.userExists("test_user_1"), True)
        self.assertEqual(Profiles.userExists("test_user_2"), True)
        self.assertEqual(Profiles.userExists("fake_user"), False)

    # Test Profiles.getUserSettings(user)
    @pytest.mark.order(6)
    def test_getUserSettings(self):
        test_user_settings = {
            "color": "rgba(255,255,255,1)",
            "font-family": "Arial",
            "font-size": "14px"
        }
        file_name = "test_user_get_settings"
        Profiles.saveUserProfile(file_name, test_user_settings)
        retrieved_settings = Profiles.getUserSettings(file_name)

        self.assertEqual(retrieved_settings, test_user_settings)

    # Test Profiles.getUserPath(user)
    @pytest.mark.order(7)
    def test_getUserPath(self):
        self.assertEqual(RUNTIME_DIR / "Users/test_user_1.css", Profiles.getUserPath("test_user_1"))
        self.assertEqual(RUNTIME_DIR / "Users/test_user_2.css", Profiles.getUserPath("test_user_2"))

    # Test Profiles.getUserProfiles()
    @pytest.mark.order(8)
    def test_getUserProfiles(self):
        self.assertEqual({
            "Current": "test_user_get_settings",
            "DefaultPath": str(RUNTIME_DIR),
            "Users": {"test_user_1", "test_user_2", "test_user_3", "test_user_delete", "test_user_get_settings"}
        },
        Profiles.getUserProfiles())

    # Test Profiles.generateDefaultSettings()
    @pytest.mark.order(9)
    def test_generateDefaultSettings(self):
        userSettings = {
            'color'            : "rgba(255,255,255,1)",
            'font-family'      : "Arial",
            'font-size'        : "12px",
            'background-color' : "rgba(0,0,0,0.2)",
            'border-radius'    : "0px"
        }
        self.assertEqual(Profiles.generateDefaultSettings(), userSettings)

    @pytest.mark.order(10)
    def test_deleteUser(self):
        Profiles.deleteUser("test_user_delete")
        self.assertFalse(Profiles.userExists("test_user_delete"))
        self.assertFalse("test_user_delete" in list(Profiles.getUserProfiles()['Users']))

    # Test Profiles.saveUserProfile(user, currentUserSettings)
    @pytest.mark.order(11)
    def test_saveUserProfile(self):
        newUserSettings = {
            "color": "rgba(255,255,255,1)",
            "font-family": "Helvetica",
            "font-size": '28'
        }
        Profiles.saveUserProfile("test_user_3", newUserSettings)
        userSettings = {}
        with open(Profiles.getUserPath("test_user_3"), "r") as cssFile:
            cssLines = cssFile.readlines()[1:-1]
            for line in cssLines:
                entry = (line.strip()).split(": ")
                userSettings[entry[0]] = entry[1][:-1]

        self.assertEqual(newUserSettings, userSettings)

    @pytest.mark.order(12)
    def test_generateProfilesFile(self):
        Profiles.generateProfilesFile()
        self.assertTrue(Path("Profiles.yml").exists())

    @pytest.mark.order(13)
    def test_saveProfilesFile(self):
        test_data = {
            "Current": "test_user_1",
            "DefaultPath": "default/path",
            "Users": {"test_user_1"}
        }
        Profiles.saveProfilesFile(test_data)
        with open("Profiles.yml", "r") as f:
            saved_data = yaml.safe_load(f)
        self.assertEqual(test_data, saved_data)

    @pytest.mark.order(14)
    def test_addUser(self):
        Profiles.addUser("test_user_3")
        self.assertTrue(Profiles.userExists("test_user_3"))

    @pytest.mark.order(15)
    def test_setCurrentUser(self):
        Profiles.setCurrentUser("test_user_2")
        self.assertEqual(Profiles.getCurrentUser(), "test_user_2")
