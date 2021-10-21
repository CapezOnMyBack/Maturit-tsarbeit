from pathlib import Path

ai_control = True

root_path = Path(__file__).parent
asset_path = root_path.joinpath("assets")

def get_Asset(name):
    return str(asset_path.joinpath(name))

def nutte():
    return "lol"