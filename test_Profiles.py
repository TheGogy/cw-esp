# Import modules
from Profiles import Profiles
from pathlib import Path
import pytest
import yaml

pytest.RUNTIME_DIR = Path(__file__).parent
@pytest.fixture 
def setup():
    # Set up test environment
    Profiles.generateProfilesFile()
    # Create test user css
    with open(pytest.RUNTIME_DIR / "Users/test_user_1.css", "w") as f:
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

    with open(pytest.RUNTIME_DIR / "Users/test_user_2.css", "w") as f:
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
        
    with open(pytest.RUNTIME_DIR / "Users/test_user_3.css", "w") as f:
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

    with open(pytest.RUNTIME_DIR / "Users/test_user_delete.css", "w") as f:
        f.write("""
    QLabel {
    color: rgba(13,6,6,1);
    font-family: Arial;
    font-size: 12px;
    background-color: rgba(0, 0, 0, 0);
    border-radius: 10px
    }
    """
    )

    # Set current user to test user
    with open(pytest.RUNTIME_DIR / "Profiles.yml", "w") as f:
        f.write(f"""
    Current: test_user_1
    DefaultPath: {str(pytest.RUNTIME_DIR)}
    Users: !!set
      test_user_1: null
      test_user_2: null
      test_user_3: null
      test_user_delete: null
    """
    )

@pytest.fixture
def teardown():
    Profiles.emptyDatabase()

@pytest.mark.order(1)
# Test Profiles.getCurrentUserCSS()
def test_getCurrentUserCSS(setup):
    test_user_1_cssData = """
QLabel {
color: rgba(195,78,92,0.85);
font-family: Fira Code;
font-size: 20px;
background-color: rgba(0, 0, 0, 0);
border-radius: 10px;
}
"""
    assert Profiles.getCurrentUserCSS() == test_user_1_cssData

@pytest.mark.order(2)
# Test Profiles.getUserList()
def test_getUserList():
    assert sorted(Profiles.getUserList()) == ["test_user_1", "test_user_2", "test_user_3", "test_user_delete"]

@pytest.mark.order(3)
# Test Profiles.getCurrentUser()
def test_getCurrentUser():
    assert Profiles.getCurrentUser() == "test_user_1"

# Test Profiles.getCurrentUserSettings()
@pytest.mark.order(4)
def test_getCurrentUserSettings():
    test_user_1_cssData = """
QLabel {
color: rgba(195,78,92,0.85);
font-family: Fira Code;
font-size: 20px;
background-color: rgba(0, 0, 0, 0);
border-radius: 10px;
}
"""
    assert Profiles.getCurrentUserCSS() == test_user_1_cssData

@pytest.mark.order(5)
# Test Profiles.userExists(user)
def test_userExists():
    assert Profiles.userExists("test_user_1") == True
    assert Profiles.userExists("test_user_2") == True
    assert Profiles.userExists("fake_user") ==  False

# Test Profiles.getUserSettings(user)
@pytest.mark.order(6)
def test_getUserSettings():
    test_user_settings = {
        "color": "rgba(255,255,255,1)",
        "font-family": "Arial",
        "font-size": "14px"
    }
    file_name = "test_user_get_settings"
    Profiles.saveUserProfile(file_name, test_user_settings)
    retrieved_settings = Profiles.getUserSettings(file_name)
    assert retrieved_settings == test_user_settings

# Test Profiles.getUserPath(user)
@pytest.mark.order(7)
def test_getUserPath():
    assert pytest.RUNTIME_DIR / "Users/test_user_1.css" == Profiles.getUserPath("test_user_1")
    assert pytest.RUNTIME_DIR / "Users/test_user_2.css" == Profiles.getUserPath("test_user_2")

# Test Profiles.getUserProfiles()
@pytest.mark.order(8)
def test_getUserProfiles():
    curretUserProfiles = {
            "Current": "test_user_get_settings",
            "DefaultPath": str(pytest.RUNTIME_DIR),
            "Users": {"test_user_1", "test_user_2", "test_user_3", "test_user_delete", "test_user_get_settings"}
    } 
    assert  curretUserProfiles == Profiles.getUserProfiles()

# Test Profiles.generateDefaultSettings()
@pytest.mark.order(9)
def test_generateDefaultSettings():
    userSettings = {
        'color'            : "rgba(255,255,255,1)",
        'font-family'      : "Arial",
        'font-size'        : "12px",
        'background-color' : "rgba(0,0,0,0.2)",
        'border-radius'    : "0px"
    }
    assert Profiles.generateDefaultSettings() == userSettings

@pytest.mark.order(10)
def test_deleteUser():
    Profiles.deleteUser("test_user_delete")
    assert not Profiles.userExists("test_user_delete")
    assert not "test_user_delete" in list(Profiles.getUserProfiles()['Users'])

# Test Profiles.saveUserProfile(user, currentUserSettings)
@pytest.mark.order(11)
def test_saveUserProfile():
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

    assert newUserSettings ==  userSettings

@pytest.mark.order(12)
def test_generateProfilesFile():
    Profiles.generateProfilesFile()
    assert Path("Profiles.yml").exists()

@pytest.mark.order(13)
def test_saveProfilesFile():
    test_data = {
        "Current": "test_user_1",
        "DefaultPath": "default/path",
        "Users": {"test_user_1"}
    }
    Profiles.saveProfilesFile(test_data)
    with open("Profiles.yml", "r") as f:
        saved_data = yaml.safe_load(f)
    assert test_data == saved_data

@pytest.mark.order(14)
def test_addUser():
    Profiles.addUser("test_user_3")
    assert Profiles.userExists("test_user_3")

@pytest.mark.order(15)
def test_setCurrentUser(teardown):
    Profiles.setCurrentUser("test_user_2")
    assert Profiles.getCurrentUser() == "test_user_2"

