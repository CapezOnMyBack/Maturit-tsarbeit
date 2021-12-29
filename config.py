from pathlib import Path

ai_control = True
amount = 1
architecture = [7, 2, 3]
wr = 2.0
margin = 0

root_path = Path(__file__).parent
asset_path = root_path.joinpath("assets")


def get_Asset(name):
    return str(asset_path.joinpath(name))
