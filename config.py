from pathlib import Path
import numpy as np

amount = 1

ai_control = True

wr = 1.0

architecture = [5, 11, 2]

time_margin = 1000 * 0.2

root_path = Path(__file__).parent
asset_path = root_path.joinpath("assets")


def get_Asset(name):
    return str(asset_path.joinpath(name))

w = [np.array([
	[ 0.47494262, -0.12016689, -0.88666953,  0.11499479, -0.37652255, 0.1103896 ,  0.77735131,  0.52087761,  0.78514752, -0.09134888, -0.81937992],
	[ 0.87126703,  0.2777362 , -0.94585573, -0.15091362, -0.12377629, 0.84072775, -0.56870273,  0.76835568,  0.63052854,  0.87237407, -0.99463463],
	[ 0.5464498 , -0.71347865,  0.48862159, -0.60091429,  0.13780168, 0.09787205, -0.7883506 , -0.77914407, -0.66475353, -0.0648421 , 0.20358428],
	[-0.92766611,  0.61164272,  0.36448712,  0.39662648, -0.98585054, 0.76803145, -0.47735177, -0.32386471, -0.30974872, -0.58010933, 0.61847111],
	[-0.32515973, -0.47976359, -0.36581991,  0.01949015, 0.52176795, -0.9448777 , -0.73144583, -0.07926249,  0.45686065, -0.67572577, 0.68333331]]),
    np.array([[ 0.79128182,  0.5152681 ],
       [ 0.38660448, -0.4443949 ],
       [ 0.98937894, -0.71393645],
       [-0.28586552,  0.8841968 ],
       [ 0.93939359, -0.66422221],
       [-0.29792749,  0.4289103 ],
       [ 0.2315714 , -0.7841884 ],
       [ 0.16189559, -0.52217191],
       [ 0.96407618,  0.95310395],
       [ 0.43770542,  0.70517814],
       [ 0.40123568, -0.88902646]])]

b = [np.array([-0.90112815, -0.1343994 , -0.24228076, -0.28174044,  0.18392742, 0.48686646, -0.11077757, -0.58085882,  0.89212028, -0.8501021 , -0.42431702]),
     np.array([-0.25104167,  0.85554095])]