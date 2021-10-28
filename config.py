from pathlib import Path

amount = 1

ai_control = True

wr = 1.0

architecture = [7, 11, 3]

# Mutation margin in %:
margin = 0

root_path = Path(__file__).parent
asset_path = root_path.joinpath("assets")


def get_Asset(name):
    return str(asset_path.joinpath(name))
