import Signals
import MQTT_publish
import time
import subprocess

#Define Health Check State -> ["standby","CableCheckWait", "CableCheck", "preChargeWait", "preCharge","charge", "Failure"]
chargeInitState = "standby"
oldtime = time.perf_counter()

#How long to check Cable
CableCheckTime = 10
TimeOutTime = 30

def sendMqttMsg(client): 
    
    topic = "DCWallbox/HMI/PageName/ChargingInitPage"
    MsgSent = False
        
    if topic in MQTT_publish.Topics:
        
        Msg = "initializing_charging"
        
        MqttStatus = MQTT_publish.publish(client,topic, Msg)
        
        if MqttStatus == 0:
            MsgSent = True
            #print(f"Sent `{Msg}` to topic `{topic}`")
    
    # if not MsgSent:
    #     print(f"Failed to send message to topic {topic}")

    return MsgSent

def ChargingInit(client):    
    global oldtime,chargeInitState
    
    sendMqttMsg(client)
    
    if chargeInitState == "Failure":
        return
    
    elif chargeInitState == "standby":   
        # Go to Cable Check Waiting
        chargeInitState = "CableCheckWait"
        oldtime = time.perf_counter()
    
    elif chargeInitState == "CableCheckWait":
        #Wait for Cable check charging State
        if Signals.CAN_Signals["chargingState"] == "cableCheck":
            # Go to Cable Check
            chargeInitState = "CableCheck"
            Signals.EnergyTransferActive = True            
            print("Cable Check Started!")
            
            oldtime = time.perf_counter()
            
        elif(time.perf_counter() > (oldtime + TimeOutTime)):
            print("Time Out Error! CableCheck not requested")
            chargeInitState = "Failure"
        
    elif chargeInitState == "CableCheck":
        
        # Check if target contractor status is closed
        if Signals.CAN_Signals["targetContactorsStatus"] == "closed":
            #Close Contractor for Cable Check
            Signals.Contractor_op = 1
            subprocess.run("echo 1 > /sys/class/gpio/gpio141/value", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            Signals.CAN_Signals["contactorsStatus"] = "closed"
            Signals.CAN_Signals["HV_HVIL_Sts"] = "HVIL Closed"
            
            # Setpoints for Charcon            
            Signals.CAN_Signals["VCU_uDcReqChrgr"] = Signals.CAN_Signals["cableCheckVoltage"]
            Signals.CAN_Signals["VCU_iDcLimChrgr"] = Signals.CAN_Signals["targetCurrent"]
            Signals.CAN_Signals["VCU_OBCMode_Cmd"] = "charging"
        
            if(Signals.IMD_ip == False):
                print("Cable Check Failure!")
                
                chargeInitState = "Failure"
                return
            
            elif(time.perf_counter() > (oldtime + CableCheckTime)):
                #Set isolation status to valid                
                Signals.CAN_Signals["isolationStatus"] = "valid"
                chargeInitState = "preChargeWait"
                
                #Set CharCon to safe state while we wait for preCharge request
                Signals.CAN_Signals["VCU_OBCMode_Cmd"] = "standby"
                                
                print("Cable Check Complete! All OK")
                oldtime = time.perf_counter()
                
        # Set a timeout if Target Contractor status is not set to closed
        elif(time.perf_counter() > (oldtime + TimeOutTime)):
            print("Time Out Error! Target Contractor Status not closed")
            chargeInitState = "Failure"
    
    elif chargeInitState == "preChargeWait":
        
        #Wait for Cable check charging State
        if Signals.CAN_Signals["chargingState"] == "preCharge":
            # Go to preCharge
            chargeInitState = "preCharge"
            print("Pre-Charging DC output...")
            oldtime = time.perf_counter()
                
        elif(time.perf_counter() > (oldtime + TimeOutTime)):
            print("Time Out Error! preCharge not requested")
            chargeInitState = "Failure"
    
    elif chargeInitState == "preCharge":
        # Setpoints for Charcon            
        Signals.CAN_Signals["VCU_uDcReqChrgr"] = Signals.CAN_Signals["targetVoltage"]
        Signals.CAN_Signals["VCU_iDcLimChrgr"] = Signals.CAN_Signals["targetCurrent"]
        Signals.CAN_Signals["VCU_OBCMode_Cmd"] = "charging"
        
        if Signals.CAN_Signals["chargingState"] == "charge":
            # Go to Charging State
            chargeInitState = "charge"
            
            


