from pathlib import Path

#amount = int(input("How many?"))
amount = 150
#ai_control_ask = input("AI controlled?")
#if ai_control_ask == "y" or "Y" or "yes" or "Yes":
#    ai_control = True
#else:
#    ai_control = False
ai_control = True

root_path = Path(__file__).parent
asset_path = root_path.joinpath("assets")

def get_Asset(name):
    return str(asset_path.joinpath(name))