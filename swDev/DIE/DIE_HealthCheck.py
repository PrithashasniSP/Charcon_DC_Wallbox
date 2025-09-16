import Signals
import MQTT_publish
import time
import subprocess

#Define Health Check State -> ["init", "CableCheck", "vSECC_Check","CCon_Check", "Good", "Failure"]
HealthCheckStateEnum = {
       "init"           : 0,
       "CableCheck"     : 1,
       "vSECC_Check"    : 2,
       "CCon_Check"     : 3,
       "Good"           : 4,
       "Failure"        : 5,
       
    }

HealthCheckState = HealthCheckStateEnum["init"]
oldtime = time.perf_counter()

#How long to check Cable and CAN
CableCheckTime = 10
CAN_CheckTime = 5

enum = {
    "CableCheckStatus" : {
        "No Check"  : 0,
        "Checking"  : 1,
        "Good"      : 2,
    },
    "PowerBoardStatus" : {
        "No Check"  : 0,
        "Checking"  : 1,
        "Good"      : 2,
    },
    "HeartBeatMsg" : {
        "Checking"  : 0,
        "Good"      : 1,
    },  
}

def sendMqttMsg(client, CableChk, PwrBoard, HrtBeat): 
    
    topic = "DCWallbox/HMI/PageName/HealthCheck"
    MsgSent = False
        
    if topic in MQTT_publish.Topics:
        
        Msg = f"{CableChk}:{PwrBoard}:{HrtBeat}"
        
        MqttStatus = MQTT_publish.publish(client,topic, Msg)
        
        if MqttStatus == 0:
            MsgSent = True
            #print(f"Sent `{Msg}` to topic `{topic}`")
    
    # if not MsgSent:
    #     print(f"Failed to send message to topic {topic}")

    return MsgSent

def HealthCheck(client):    
    global oldtime,HealthCheckState
    #print(f"Health State: {HealthCheckState}")
    
    if HealthCheckState == HealthCheckStateEnum["Failure"]:
        return
    
    elif HealthCheckState == HealthCheckStateEnum["init"]:
        #Change Health Icon Status
        Signals.HMI_Signals["HealthIcon"] = "No icon"
            
        # Go to Cable Check
        HealthCheckState = HealthCheckStateEnum["CableCheck"]
        print("Cable Check Started...")
        oldtime = time.perf_counter()
        
    elif HealthCheckState == HealthCheckStateEnum["CableCheck"]:
        #Send MQTT Messages:
        sendMqttMsg(client, enum["CableCheckStatus"]["Checking"], enum["PowerBoardStatus"]["No Check"], enum["HeartBeatMsg"]["Checking"])
        
        #Close Contractor for Cable Check
        Signals.Contractor_op = 1
        subprocess.run("echo 1 > /sys/class/gpio/gpio141/value", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        Signals.CAN_Signals["contactorsStatus"] = "closed"
        Signals.CAN_Signals["HV_HVIL_Sts"] = "HVIL Closed"
        
        if(Signals.IMD_ip == False):
            print("Cable Check Failure!")
            HealthCheckState = HealthCheckStateEnum["Failure"]
            return
        
        elif(time.perf_counter() > (oldtime + CableCheckTime)):
            #Open Contractor After Cable Check
            Signals.Contractor_op = 0
            subprocess.run("echo 0 > /sys/class/gpio/gpio141/value", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            Signals.CAN_Signals["contactorsStatus"] = "open"
            Signals.CAN_Signals["HV_HVIL_Sts"] = "HVIL Open"
            
            HealthCheckState = HealthCheckStateEnum["vSECC_Check"]
            print("Cable Check Complete! Checking v.SECC CAN...")
            oldtime = time.perf_counter()
    
    elif HealthCheckState == HealthCheckStateEnum["vSECC_Check"]:
        #Send MQTT Messages:
        sendMqttMsg(client, enum["CableCheckStatus"]["Good"], enum["PowerBoardStatus"]["Checking"], enum["HeartBeatMsg"]["Checking"])
        
        if(Signals.CntrVseccFrameRecv > 10):
            print("vSECC CAN Failure!")
            HealthCheckState = HealthCheckStateEnum["Failure"]
            return
        
        elif(time.perf_counter() > (oldtime + CAN_CheckTime)):            
            HealthCheckState = HealthCheckStateEnum["CCon_Check"]
            print("v.SECC CAN Check Complete! Checking CharCon CAN...")
            oldtime = time.perf_counter()
    
    elif HealthCheckState == HealthCheckStateEnum["CCon_Check"]:
        #Send MQTT Messages:
        sendMqttMsg(client, enum["CableCheckStatus"]["Good"], enum["PowerBoardStatus"]["Checking"], enum["HeartBeatMsg"]["Checking"])
        
        if(Signals.CntrCharConFrameRecv > 10):
            print("CharCon CAN Failure!")
            HealthCheckState = HealthCheckStateEnum["Failure"]
            return
        
        elif(time.perf_counter() > (oldtime + CAN_CheckTime)):            
            HealthCheckState = HealthCheckStateEnum["Good"]
            
            print("CharCon CAN Check Complete!")
            print("Health Status is Good!")
            
            #Change Health Icon Status
            Signals.HMI_Signals["HealthIcon"] = "Green icon"
            
            #Send MQTT Messages:
            sendMqttMsg(client, enum["CableCheckStatus"]["Good"], enum["PowerBoardStatus"]["Good"], enum["HeartBeatMsg"]["Good"])


