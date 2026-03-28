from src.__version__ import __version__

def test_version_exists():
    assert isinstance(__version__, str)
    