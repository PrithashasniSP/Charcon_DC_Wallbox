import Signals
import MQTT_publish
import subprocess

def sendMqttMsg(client): 
    
    topic = "DCWallbox/HMI/PageName/DeviceFailure"
    MsgSent = False
        
    if topic in MQTT_publish.Topics:
        
        Msg = "failure_has_occured"
        
        MqttStatus = MQTT_publish.publish(client,topic, Msg)
        
        if MqttStatus == 0:
            MsgSent = True
            #print(f"Sent `{Msg}` to topic `{topic}`")
    
    # if not MsgSent:
    #     print(f"Failed to send message to topic {topic}")

    return MsgSent

def WallBoxFailure(client):
        
    #Open Contractor
    Signals.Contractor_op = 0
    subprocess.run("echo 0 > /sys/class/gpio/gpio141/value", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    #Notify v.SECC
    Signals.CAN_Signals["operationalStatus"] = "inoperative"
    Signals.CAN_Signals["contactorsStatus"] = "open"
    
    #Get CharCon to Standby
    Signals.CAN_Signals["VCU_OBCMode_Cmd"] = "standby"
    Signals.CAN_Signals["HV_HVIL_Sts"] = "HVIL Open"
    
    #Change Health Icon Status
    Signals.HMI_Signals["HealthIcon"] = "Red icon with exclamation"
    
    #Send MQTT Messages:
    sendMqttMsg(client)
    

#Test Code:
'''
Signals.CAN_Signals.update({
    "evConnectionState": "connected",
	"chargingState": "charge",
 })

# Set up MQTT Client
client = MQTT_publish.connect_mqtt()
client.loop_start()  
WallBoxFailure(client)
client.loop_stop()
'''