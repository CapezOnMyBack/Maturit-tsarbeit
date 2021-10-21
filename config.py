from pathlib import Path

amount = int(input("How many?"))

ai_control_ask = input("AI controlled?")
if ai_control_ask == "y" or "Y" or "yes" or "Yes":
    ai_control = True
else:
    ai_control = False

root_path = Path(__file__).parent
asset_path = root_path.joinpath("assets")

def get_Asset(name):
    return str(asset_path.joinpath(name))

def nutte():
    return "lol"