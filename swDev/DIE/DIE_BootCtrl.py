import json
import os
from Signals import HMI_Signals
from datetime import datetime
import requests

StateEnum  =   {
    "Not Checked": 0,
    "Valid": 1,
    "Missing Config": 2,
    "Failure": 3,
    }

ConfigParameters = [
    "CostPerKwh",
    "MaxGridCurrent",
    "SolarPanelArea"
    ]

State = StateEnum["Not Checked"]

# Get the directory of the current Python script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the Config file path
Config_file_path = os.path.join(script_directory, "DCWB_Config.json")

# Specify Solar data JSON file
Solar_file_path = os.path.join(script_directory, "Solar_Data.json")

def writeSolarData(Date):
    print("Solar data for the day not available. Creating new data")
    response = requests.get(f"https://keri7fkpkb32ujueqedomh5gla0pigve.lambda-url.ap-south-1.on.aws/?total_area=25.6&lat=22.9&lon=77.5&date={Date}")
    print(response.json())
    data = {
        'Date': Date,
        'ApiData': response.json(),
        }
    with open(Solar_file_path, 'w') as file:
        json.dump(data, file)

def BootCtrl(CAN_Avl, GSM_Avl, MQTT_Avl):
    global State,StateEnum
    
    print("Booting Data Interface Engine...")
    
    if CAN_Avl and GSM_Avl and MQTT_Avl:
        # Check if Config File not available / File could not be parsed
        try:
            # Open the JSON file for reading
            with open(Config_file_path, "r") as json_file:
                # Read and parse the JSON data
                DCWB_config = json.load(json_file)
            # Check if the values in the Configuration are numbers
            
            for x in ConfigParameters:
                if isinstance(DCWB_config[x], (int,float)):
                    HMI_Signals[x] = DCWB_config[x]
                    State = StateEnum["Valid"]
                else:
                    State = StateEnum["Missing Config"]
                    break
        except FileNotFoundError:
            State = StateEnum["Missing Config"]

        except json.JSONDecodeError as e:
            # Error Parsing JSON
            State = StateEnum["Missing Config"]
        
        except KeyError:
            # MissingKeys
            State = StateEnum["Missing Config"]
            
        try:
            # Get current Date
            current_time = datetime.now()
            Date = current_time.strftime("%Y-%m-%d")
            
            # Check if Solar Data jSON exists
            if os.path.exists(Solar_file_path):
                
                with open(Solar_file_path, 'r') as file:
                    data = json.load(file)
                
                if(data["Date"] == Date):
                    print("Solar data for the day available already")
                else:
                    # If the file doesn't exist, create it with new data
                    writeSolarData(Date)
            
            else:
                # If the file doesn't exist, create it with new data
                writeSolarData(Date)
                
        except:
            pass
        
    else:
        State = StateEnum["Failure"]
        
    return State

#Test Code
#print(BootCtrl(1,1,1))