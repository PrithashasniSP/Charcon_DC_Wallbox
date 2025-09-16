import json
import matplotlib.pyplot as plt
import requests
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
import numpy as np
import math
import time
# # The API endpoint
# url = "https://api.openweathermap.org/energy/1.0/solar/data?lat=22.9&lon=77.5&date=2023-11-14&tz=+05:30&appid=b2c5a021282ac8d3bc74b9e27fc72239"

# # A GET request to the API
# response = requests.get(url)

# # Print the response
# response_json = response.json()
# print(response_json)

def lambda_handler(event,context):
    json_string2 ={'lat': 22.9, 'lon': 77.5, 'date': '2023-11-14', 'tz': '+05:30', 'sunrise': '2023-11-14T06:31:58', 'sunset': '2023-11-14T17:36:29', 'irradiance': {'daily': [{'clear_sky': {'ghi': 5305.65, 'dni': 8114.12, 'dhi': 977.62}, 'cloudy_sky': {'ghi': 3747.58, 'dni': 2619.38, 'dhi': 2277.85}}], 'hourly': [{'hour': 0, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}}, {'hour': 1, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 
    0.0}}, {'hour': 2, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}}, {'hour': 3, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}}, {'hour': 4, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}}, {'hour': 5, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}}, {'hour': 6, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}}, {'hour': 7, 'clear_sky': {'ghi': 54.43, 'dni': 311.83, 'dhi': 35.94}, 'cloudy_sky': {'ghi': 27.44, 'dni': 56.81, 'dhi': 22.15}}, {'hour': 8, 'clear_sky': {'ghi': 264.54, 'dni': 655.64, 'dhi': 73.52}, 'cloudy_sky': {'ghi': 178.19, 'dni': 198.39, 'dhi': 117.9}}, {'hour': 9, 'clear_sky': {'ghi': 474.05, 'dni': 795.04, 'dhi': 94.02}, 'cloudy_sky': {'ghi': 270.07, 'dni': 111.92, 'dhi': 215.5}}, {'hour': 10, 'clear_sky': {'ghi': 644.99, 'dni': 867.35, 'dhi': 
    106.53}, 'cloudy_sky': {'ghi': 501.15, 'dni': 343.39, 'dhi': 285.18}}, {'hour': 11, 'clear_sky': {'ghi': 757.39, 'dni': 904.35, 'dhi': 113.52}, 'cloudy_sky': {'ghi': 587.2, 'dni': 352.45, 'dhi': 333.33}}, {'hour': 12, 'clear_sky': {'ghi': 799.72, 'dni': 916.79, 'dhi': 115.94}, 'cloudy_sky': {'ghi': 585.68, 'dni': 295.03, 'dhi': 363.11}}, {'hour': 13, 'clear_sky': {'ghi': 767.86, 'dni': 907.68, 'dhi': 114.07}, 'cloudy_sky': {'ghi': 367.69, 'dni': 80.12, 'dhi': 309.43}}, {'hour': 14, 'clear_sky': {'ghi': 664.88, 'dni': 874.75, 'dhi': 107.72}, 'cloudy_sky': {'ghi': 555.68, 'dni': 474.51, 'dhi': 249.5}}, {'hour': 15, 'clear_sky': {'ghi': 501.21, 'dni': 808.73, 'dhi': 96.07}, 'cloudy_sky': {'ghi': 406.98, 'dni': 404.07, 'dhi': 201.04}}, {'hour': 16, 'clear_sky': {'ghi': 295.44, 'dni': 682.52, 'dhi': 77.01}, 'cloudy_sky': {'ghi': 214.13, 'dni': 237.62, 'dhi': 135.37}}, {'hour': 17, 'clear_sky': {'ghi': 81.14, 'dni': 389.44, 'dhi': 43.28}, 'cloudy_sky': {'ghi': 53.37, 'dni': 65.07, 'dhi': 45.34}}, {'hour': 18, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}}, {'hour': 19, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}}, {'hour': 20, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}}, {'hour': 21, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}}, {'hour': 22, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}}, {'hour': 23, 'clear_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}, 'cloudy_sky': {'ghi': 0.0, 'dni': 0.0, 'dhi': 0.0}}]}}

    ###################################   Panel Configuration assumptions   #####################################################
    configuration_panel ={}
    configuration_panel['module'] = {
        'power': 4,  # in Kw
        'total_area': 25.6,  # in meter square
        'eachmodule_area': 1.6, # in meter square
        'num_modules': 16
    }
    assumed_paneleff= 0.2
    #######################################################################################################################

    # get the hourly values from json response and save to an array
    array_ghi = [entry["clear_sky"]["ghi"] for entry in json_string2["irradiance"]["hourly"]]
    array_hour= [entry["hour"] for entry in json_string2["irradiance"]["hourly"]]
    print(array_ghi)
    print(array_hour)

    # power calculation
    float_ghi = np.array([float(value) for value in array_ghi])
    power_array= float_ghi * assumed_paneleff*float(configuration_panel['module']['total_area']/1000)

    peak_sun_hours= (sum(float_ghi)/1000)

    total_power = (sum(power_array))

    # Get the corresponding hour for max ghi
    max_ghi_index = array_ghi.index(max(float_ghi))
    max_ghi_hour = array_hour[max_ghi_index]
    print("Max GHI Hour:", max_ghi_hour)

    # Get the corresponding hour for approximating peak sun hours
    min_hour = array_hour[math.floor(max_ghi_hour-peak_sun_hours/2)]
    print("min Hour:", min_hour)
    max_hour = array_hour[math.ceil(max_ghi_hour+peak_sun_hours/2)]
    print("max Hour:", max_hour)
    # you have different irradiations at different hours. so multiply that with only that hour, not the total time becoz it is not same during all hours. since
    # data is received for evrey hour, keep at hour constant GHI(W/m2)*1h /1000  is how many KWh/m2 aka peak sun hours
    print(f"Peak Sun Hours: {peak_sun_hours:.1f} KWh/m2")
    print(f"Energy available: {total_power:.2f} KWh")

    ############################################################   Put in JSON   ###################################################
    # a Python object (dict):
    JSON_solardata = {
      # "MaxIrrAt": f"Max Irradiation: {max(float_ghi):.2f} @ {corresponding_hour} ",
      "PeakSunHours": float("{:.1f}".format(peak_sun_hours)),
      "DurationPSH": f"{min_hour} to {max_hour}",
      "EnergyPerDay": float("{:.2f}".format(total_power))
    }
    # the result is a JSON string:
    print(json.dumps(JSON_solardata))
    return (json.dumps(JSON_solardata))

###########################################################################################################################
