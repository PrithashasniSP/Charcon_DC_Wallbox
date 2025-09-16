import Signals
import MQTT_publish
from DIE_HealthCheck import enum
import time

oldtime = time.perf_counter()

def sendMqttMsg(client, prevState): 
    
    if(prevState == "HealthCheck"):
        topic = "DCWallbox/HMI/PageName/HealthCheck"
        CableChk = enum["CableCheckStatus"]["Good"]
        PwrBoard = enum["PowerBoardStatus"]["Good"]
        HrtBeat = enum["HeartBeatMsg"]["Good"]        
        Msg = f"{CableChk}:{PwrBoard}:{HrtBeat}"
    
    elif(prevState == "Charging" and time.perf_counter() <= oldtime + 10) :
        topic = "DCWallbox/HMI/PageName/ChargingProgressPage"
        SolarEnergy = Signals.HMI_Signals["SolarEnergy"]
        GridEnergy = Signals.HMI_Signals["GridEnergy"]
        ySolarPwr = Signals.HMI_Signals["ySolarPwr"]
        yGridPwr = Signals.HMI_Signals["yGridPwr"]
        xTime = Signals.HMI_Signals["xTime"]
        TotCost = Signals.HMI_Signals["TotCost"]
        PauseTimer = Signals.HMI_Signals["PauseTimer"]
        StopEventAck = Signals.HMI_Signals["StopEventAck"]
        ChargingState = Signals.HMI_Signals["ChargingState"]
        
        Msg = f"{SolarEnergy}:{GridEnergy}:{ySolarPwr}:{yGridPwr}:{xTime}:{TotCost}:{PauseTimer}:{StopEventAck}:{ChargingState}"
        
    else:
        topic = "DCWallbox/HMI/PageName/ReadyToCharge"
        Msg = "wallbox_ready_to_charge"
        
    MsgSent = False
        
    if topic in MQTT_publish.Topics:
        
        MqttStatus = MQTT_publish.publish(client,topic, Msg)
        
        if MqttStatus == 0:
            MsgSent = True
            #print(f"Sent `{Msg}` to topic `{topic}`")
    
    # if not MsgSent:
    #     print(f"Failed to send message to topic {topic}")

    return MsgSent

# Check if New connection detected
def ConnectionDetected():
    evConnectionState = Signals.CAN_Signals["evConnectionState"]
    if(evConnectionState == "connected" or evConnectionState == "energyTransferAllowed"):
        return True
    else:
        return False

def Ready(client, prevState):
        
    #Send MQTT Messages:
    sendMqttMsg(client, prevState)
    

#Test Code:
'''
Signals.CAN_Signals.update({
    "evConnectionState": "connected",
	"chargingState": "charge",
 })
'''

# Set up MQTT Client
'''
client = MQTT_publish.connect_mqtt()
client.loop_start()  
Ready(client,"Charging")
client.loop_stop()
'''