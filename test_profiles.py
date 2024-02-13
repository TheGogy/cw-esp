from Profiles import Profiles
from pathlib import Path
import pytest

# @pytest.fixture(scope="session")
# def setup_test_environment():
print("[ + ] Setting up environment for testing")
RUNTIME_DIR = Path(__file__).parent

with open(RUNTIME_DIR / "Users/test.css", "w") as f:
    f.write("""
QLabel {
color: rgba(195,78,92,0.85);
font-family: Fira Code;
font-size: 20px;
}
    """)
with open(RUNTIME_DIR / "Profiles.yml", "w") as f:
    f.write(f"""
Current: test
DefaultPath: {str(RUNTIME_DIR / "Users")}
Users: !!set
  test: null
""")



def test_getCurrentUserCSS():
    with open("Users/test.css", "r") as f:
        cssData = f.read()
    assert Profiles.getCurrentUserCSS() == cssData

