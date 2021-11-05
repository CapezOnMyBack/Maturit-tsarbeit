from pathlib import Path

amount = 200

ai_control = True

wr = 1.0

architecture = [7, 6, 3]

# Mutation margin in %:
margin = 30

root_path = Path(__file__).parent
asset_path = root_path.joinpath("assets")


def get_Asset(name):
    return str(asset_path.joinpath(name))
