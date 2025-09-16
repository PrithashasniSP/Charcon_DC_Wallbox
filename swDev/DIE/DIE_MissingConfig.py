import Signals
import MQTT_publish
import json
import os
import subprocess

def sendMqttMsg(client): 
    
    topic = "DCWallbox/HMI/PageName/MissingConfig"
    MsgSent = False
        
    if topic in MQTT_publish.Topics:
        
        Msg = "configuration_missing"
        
        MqttStatus = MQTT_publish.publish(client,topic, Msg)
        
        if MqttStatus == 0:
            MsgSent = True
            #print(f"Sent `{Msg}` to topic `{topic}`")
    
    # if not MsgSent:
    #     print(f"Failed to send message to topic {topic}")

    return MsgSent

def MissingConfig(client):
    print(f"Missing Configurations")
    
    #Open Contractor
    Signals.Contractor_op = 0
    subprocess.run("echo 0 > /sys/class/gpio/gpio141/value", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    #Notify v.SECC
    Signals.CAN_Signals["operationalStatus"] = "inoperative"
    Signals.CAN_Signals["contactorsStatus"] = "open"
    Signals.CAN_Signals["HV_HVIL_Sts"] = "HVIL Open"
    
    #Change Health Icon Status
    Signals.HMI_Signals["HealthIcon"] = "White icon with exclamation"
    
    #Send MQTT Messages:
    sendMqttMsg(client)
    
    
def CheckConfigAvl():
    
    ConfigAvl = False
    
    # Get the directory of the current Python script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the Config file path
    file_path = os.path.join(script_directory, "DCWB_Config.json")

    try:
        # Open the JSON file for reading
        with open(file_path, "r") as json_file:
            # Read and parse the JSON data
            DCWB_config = json.load(json_file)
            
            # Check if the values in the Configuration are numbers
            if isinstance(DCWB_config["CostPerKwh"], (int,float)) and isinstance(DCWB_config["MaxGridCurrent"], (int,float)):
                Signals.HMI_Signals["CostPerKwh"] = DCWB_config["CostPerKwh"]
                Signals.HMI_Signals["MaxGridCurrent"] = DCWB_config["MaxGridCurrent"]
                ConfigAvl = True
            
    except FileNotFoundError:
        pass

    except json.JSONDecodeError as e:
        # Error Parsing JSON
        pass
    
    except KeyError:
        # MissingKeys
        pass
    
    return ConfigAvl
        
        
#Test Code:
'''
# Set up MQTT Client
client = MQTT_publish.connect_mqtt()
client.loop_start()  
MissingConfig(client)
print(CheckConfigAvl())
client.loop_stop()
'''