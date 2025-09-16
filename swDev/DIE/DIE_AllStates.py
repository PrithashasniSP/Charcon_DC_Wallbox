import Signals
import MQTT_publish
import DIE_HealthCheck
import subprocess

#Global Error Flag
flgError = False

#Global Variables
HealthIcon = None
PlugState = None
CloudState = None

EnergyTransferStopCounter = 0
    
enum = {
    "HealthIcon" : {
        "No icon"                       : 0,
        "Red icon with exclamation"     : 1,
        "White icon with exclamation"   : 2,
        "Green icon"                    : 3,
    },
    "PlugStatus" : {
        "Not Plugged"   : 0,
        "Connected"     : 1,
        "Charging"      : 2,
        "Error"         : 3,
    },
    "CloudConnectionStatus" : {
        "Not Connected"   : 0,
        "Connected"     : 1,
    },  
}

def getConnectionState(evConnectionState, chargingState):
    global flgError
    
    PlugState = None
    
    if (DIE_HealthCheck.HealthCheckState < DIE_HealthCheck.HealthCheckStateEnum["vSECC_Check"]):
        PlugState = "Not Plugged"
        return PlugState
    
    if(evConnectionState == "disconnected"):
        PlugState = "Not Plugged"
    elif(evConnectionState == "connected" or evConnectionState == "energyTransferAllowed"):
        if(chargingState == "charge"):
            PlugState = "Charging"
        else:
            PlugState = "Connected"
    else:
        PlugState = "Error"
        flgError = True
        print("Plug Connection Error!")
        
    return PlugState

def update():
    global HealthIcon, PlugState, CloudState
    
    #For MQTT to All HMI Pages
    HealthIcon = Signals.HMI_Signals["HealthIcon"]
    PlugState = getConnectionState(Signals.CAN_Signals["evConnectionState"], Signals.CAN_Signals["chargingState"])
    CloudState = "Connected"
    
    result = subprocess.run("cat /sys/class/gpio/gpio139/value", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # For monitoring IMD Status (not used for test with button. To be removed in actual code)
    Signals.IMD_ip = not bool(int(result.stdout))
    
    # Test Code to simulate IMD digital output via CAN
    # if(Signals.CAN_Signals["DC1_bReqMIL"] == "MIL On"):
    #     Signals.IMD_ip = False
    # else:
    #     Signals.IMD_ip = True
    
    # Update CharCon measured values to v.SECC
    Signals.CAN_Signals["measuredVoltage"] = Signals.CAN_Signals["CHRGR_uDcAct"] if isinstance(Signals.CAN_Signals["CHRGR_uDcAct"], (int, float)) else 0
    Signals.CAN_Signals["measuredCurrent"] = Signals.CAN_Signals["CHRGR_iDcAct"] if isinstance(Signals.CAN_Signals["CHRGR_iDcAct"], (int, float)) else 0
    
    # Update driven values of Charcon to v.SECC
    if Signals.CAN_Signals["VCU_OBCMode_Cmd"] == "charging":
        Signals.CAN_Signals["drivenVoltage"] = Signals.CAN_Signals["VCU_uDcReqChrgr"] if isinstance(Signals.CAN_Signals["VCU_uDcReqChrgr"], (int, float)) else 0
        Signals.CAN_Signals["drivenCurrent"] = Signals.CAN_Signals["VCU_iDcLimChrgr"] if isinstance(Signals.CAN_Signals["VCU_iDcLimChrgr"], (int, float)) else 0
    else:
        Signals.CAN_Signals["drivenVoltage"] = 0
        Signals.CAN_Signals["drivenCurrent"] = 0
        
    # Update temperature of Charcon to v.SECC
    Signals.CAN_Signals["temperature"] = Signals.CAN_Signals["DC1_Temp"] if isinstance(Signals.CAN_Signals["DC1_Temp"], (int, float)) else 0

def PassiveHealthCheck():
    global flgError, PlugState, EnergyTransferStopCounter
    
    if DIE_HealthCheck.HealthCheckState == DIE_HealthCheck.HealthCheckStateEnum["Good"]:
        # IMD Check:
        if (Signals.IMD_ip == False):
            print("IMD Error")
            flgError = True
            return
        
        # v.SECC CAN Check:
        if (Signals.CntrVseccFrameRecv > 20):
            print("vSECC CAN Failure!")
            flgError = True
            return
        
        # CharCon CAN Check:
        if (Signals.CntrCharConFrameRecv > 10):
            print("CharCon CAN Failure!")
            flgError = True
            return
        
        # Abrupt Vehicle Communication Termination
        if (Signals.EnergyTransferActive):
            if(Signals.CAN_Signals["evConnectionState"] == "connected"):
                EnergyTransferStopCounter += 1
                
            if(EnergyTransferStopCounter >= 10):
                print("Communication to vehicle Terminated Abruptly!")
                flgError = True
                EnergyTransferStopCounter = 0
                Signals.EnergyTransferActive = False
                return
        
    

def sendMqttMsg(client): 
    global flgError, HealthIcon, PlugState, CloudState, enum
    
    topic = "DCWallbox/HMI/PageName/AllPage"
    MsgSent = False
        
    if topic in MQTT_publish.Topics:
        # ConnectionState = PlugState
        # print(f"Connection State: {ConnectionState}")
        
        Msg = str(enum["HealthIcon"][HealthIcon])+":"+str(enum["PlugStatus"][PlugState])+":"+str(enum["CloudConnectionStatus"][CloudState])
        
        if Msg is not None:
            MqttStatus = MQTT_publish.publish(client,topic, Msg)
            if MqttStatus == 0:
                MsgSent = True
                #print(f"Sent `{Msg}` to topic `{topic}`")
            
        # if not MsgSent:
        #     print(f"Failed to send message to topic {topic}")
    
    return MsgSent

def AllStates(client):
    # Update All Real time Signals
    update()
    
    #Debug Code to check CAN signals reception from v.SECC and CharCon
    
    # if(Signals.CntrVseccFrameRecv > 10): 
    #     print(f"v.SECC frame Warning!!!! Counter: {Signals.CntrVseccFrameRecv}")
    # if(Signals.CntrCharConFrameRecv > 10): 
    #     print(f"charCon frame Warning!!!! Counter: {Signals.CntrCharConFrameRecv}")
       
    # Do Passive Health Check!
    if not flgError:
        PassiveHealthCheck()
    
    # SendMqttMsg for All HMI Pages
    sendMqttMsg(client)

#Test Code:
"""
Signals.CAN_Signals.update({
    "evConnectionState": "connected",
	"chargingState": "charge",
 })

# Set up MQTT Client
client = MQTT_publish.connect_mqtt()
client.loop_start()  
Signals.HMI_Signals["HealthIcon"] = "Green icon"
sendMqttMsg(client)
client.loop_stop()

"""