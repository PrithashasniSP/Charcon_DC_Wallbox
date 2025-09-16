import Signals
import MQTT_publish
import time
import random
import can
import subprocess
import DIE_OcppClient
import threading

enum = {
    "StopEventAck" : {
        "Event message NOT Received"  : 0,
        "Event message Received and Acknowledged"  : 1,
    },
    "ChargingState" : {
        "Charging"          : 0,
        "Terminating"       : 1,
        "Charging Complete" : 2,
        "Charger Unplugged" : 3,
    },
}

#Define Health Check State -> ["standby", "charging","UserStop", "evStop", "ReadyDisconnect", "Disconnect", "Failure"]
chargeState = "standby"
oldtime = time.perf_counter()

TimeOutTime = 30

usedSolarEnergy = 0
usedGridEnergy = 0

ws_instance = None

def sendMqttMsg(client): 
    
    topic = "DCWallbox/HMI/PageName/ChargingProgressPage"
    MsgSent = False
        
    if topic in MQTT_publish.Topics:
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
        
        MqttStatus = MQTT_publish.publish(client,topic, Msg)
        
        if MqttStatus == 0:
            MsgSent = True
            #print(f"Sent `{Msg}` to topic `{topic}`")
    
    # if not MsgSent:
    #     print(f"Failed to send message to topic {topic}")

    return MsgSent

def Charging(client,startTime):    
    global oldtime,chargeState,usedGridEnergy,usedSolarEnergy,ws_instance
    
    if chargeState == "standby":
        
        # Create a thread for Sending Voltage and current data to OCPP
        ws_instance = DIE_OcppClient.websocket_establishement()
        
        OCPP_thread = threading.Thread(target=DIE_OcppClient.ws_start, args=(ws_instance,))
        OCPP_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits
        OCPP_thread.start() # Start the CAN thread
        
        chargeState = "charging"
        Signals.OCPP_Signals.update({
            "Voltage": 0,
            "Current": 0,
        })
        
    elif chargeState == "charging":
        
        usedSolarPwr = 0
        usedGridPwr = 0

        #Get requested output:
        targetVoltage = Signals.CAN_Signals["targetVoltage"]
        targetCurrent = Signals.CAN_Signals["targetCurrent"]
        
        requestedPower = targetCurrent * targetVoltage
        
        uReq = targetVoltage
        
        if requestedPower < Signals.MaxOutPwr:
            iReq = targetCurrent
        else:
            iReq = Signals.MaxOutPwr/targetVoltage
        
        # Setpoints for Charcon            
        Signals.CAN_Signals["VCU_uDcReqChrgr"] = uReq
        Signals.CAN_Signals["VCU_iDcLimChrgr"] = iReq
        Signals.CAN_Signals["VCU_OBCMode_Cmd"] = "charging"
        
        uAct = Signals.CAN_Signals["CHRGR_uDcAct"] if isinstance(Signals.CAN_Signals["CHRGR_uDcAct"], (int, float)) else 0
        iAct = Signals.CAN_Signals["CHRGR_iDcAct"] if isinstance(Signals.CAN_Signals["CHRGR_uDcAct"], (int, float)) else 0
        
        #print(f"V = {uAct}, I = {iAct}")
        
        Signals.OCPP_Signals.update({
            "Voltage": uAct,
            "Current": iAct,
        })
        
        # Calculate input Grid power
        inputAcCurrents =[val if isinstance(val, (int, float)) else 0 for val in  [Signals.CAN_Signals["CHRGR_iAcAct"], Signals.CAN_Signals["CHRGR_iAcAct2"], Signals.CAN_Signals["CHRGR_iAcAct3"]]]
        inputAcVoltages = [val if isinstance(val, (int, float)) else 0 for val in  [Signals.CAN_Signals["CHRGR_uAcActPha1"], Signals.CAN_Signals["CHRGR_uAcActPha2"], Signals.CAN_Signals["CHRGR_uAcActPha3"]]]
        
        inputAcPwr = 0
        for i in range(0,3): 
            inputAcPwr += inputAcCurrents[i]*inputAcVoltages[i]
        
        
        # Calculation based on Avl Solar Power
        # AvlSolarPwr = random.randrange(1000,1500)
        # #AvlSolarPwr = 1200
        
        # usedSolarPwr = min(inputAcPwr,AvlSolarPwr)
        # usedGridPwr = inputAcPwr - usedSolarPwr
        
        # Calculation Based on Power derived from Energy meter reading
        EnergyMeterPower = random.randrange(-100,1000)
        usedGridPwr = max(EnergyMeterPower,0)
        usedSolarPwr = inputAcPwr - usedGridPwr
        
        # usedGridEnergy += (usedGridPwr/1000) * (time.perf_counter() - oldtime)/3600
        # usedSolarEnergy += (usedSolarPwr/1000) * (time.perf_counter() - oldtime)/3600
        
        # removing the division by 1000 to have faster changing of the energy on display
        usedGridEnergy += (usedGridPwr) * (time.perf_counter() - oldtime)/3600
        usedSolarEnergy += (usedSolarPwr) * (time.perf_counter() - oldtime)/3600
        
        TotCost = usedGridEnergy*Signals.HMI_Signals["CostPerKwh"]
        
        oldtime = time.perf_counter()
        
        elapsedtime = time.perf_counter() - startTime
        
        Signals.HMI_Signals.update({
        "SolarEnergy": "{:.3f}".format(usedSolarEnergy),
        "GridEnergy": "{:.3f}".format(usedGridEnergy),
        "ySolarPwr": "{:.3f}".format(usedSolarPwr),
        "yGridPwr": "{:.3f}".format(usedGridPwr),
        "xTime": "{:.3f}".format(elapsedtime),
        "TotCost": "{:.3f}".format(TotCost),
        "PauseTimer": 1,
        "StopEventAck": enum["StopEventAck"]["Event message NOT Received"],
        "ChargingState": enum["ChargingState"]["Charging"],
        })
        
        sendMqttMsg(client)
        
        if(Signals.CAN_Signals["chargingState"] == "postCharge"):
            print("Terminating Charging Session")
            chargeState = "evStop"
            Signals.EnergyTransferActive = False
            DIE_OcppClient.closeWebsocket(ws_instance)
            
        elif(Signals.StopChargingHMI):
            print("Stop Charging Request from HMI")
            Signals.StopChargingHMI = False
            chargeState = "UserStop"
            DIE_OcppClient.closeWebsocket(ws_instance)
            oldtime = time.perf_counter()
    
    elif chargeState == "UserStop":
        # Setpoints for Charcon            
        Signals.CAN_Signals["VCU_OBCMode_Cmd"] = "standby"  
        Signals.CAN_Signals["VCU_uDcReqChrgr"] = 0
        Signals.CAN_Signals["VCU_iDcLimChrgr"] = 0
        
        TotCost = usedGridEnergy*Signals.HMI_Signals["CostPerKwh"]
        
        Signals.HMI_Signals.update({
        "SolarEnergy": "{:.3f}".format(usedSolarEnergy),
        "GridEnergy": "{:.3f}".format(usedGridEnergy),
        "ySolarPwr": 0,
        "yGridPwr": 0,
        "xTime": 0,
        "TotCost": "{:.3f}".format(TotCost),
        "PauseTimer": 0,
        "StopEventAck": enum["StopEventAck"]["Event message Received and Acknowledged"],
        "ChargingState": enum["ChargingState"]["Terminating"],
        })
        
        sendMqttMsg(client)
        
        # Send Stop Charging Request to v.SECC
        bus = can.interface.Bus(channel='can0', bustype='socketcan')
        message = can.Message(arbitration_id=0x309, data=[], dlc=0, is_extended_id=False)
        bus.send(message)
        bus.shutdown()
        
        if(Signals.CAN_Signals["chargingState"] == "postCharge"):
            print("Terminating Charging Session")
            chargeState = "evStop"
            Signals.EnergyTransferActive = False
            
        elif(time.perf_counter() > oldtime + 10):
            print("Did not receive EV Stop Request")
            Signals.CAN_Signals["operationalStatus"] = "inoperative"
            chargeState = "Failure"
        
        
    
    elif chargeState == "evStop":
        
        # Setpoints for Charcon            
        Signals.CAN_Signals["VCU_OBCMode_Cmd"] = "standby"  
        Signals.CAN_Signals["VCU_uDcReqChrgr"] = 0
        Signals.CAN_Signals["VCU_iDcLimChrgr"] = 0
        
        TotCost = usedGridEnergy*Signals.HMI_Signals["CostPerKwh"]
        
        Signals.HMI_Signals.update({
        "SolarEnergy": "{:.3f}".format(usedSolarEnergy),
        "GridEnergy": "{:.3f}".format(usedGridEnergy),
        "ySolarPwr": 0,
        "yGridPwr": 0,
        "xTime": 0,
        "TotCost": "{:.3f}".format(TotCost),
        "PauseTimer": 0,
        "StopEventAck": enum["StopEventAck"]["Event message NOT Received"],
        "ChargingState": enum["ChargingState"]["Terminating"],
        })
        
        sendMqttMsg(client)
        
        if(Signals.StopChargingEv):
            print("Charger Ready to Disconnect")
            chargeState = "ReadyDisconnect"
            Signals.StopChargingEv = False
    
    elif chargeState == "ReadyDisconnect":
        # Setpoints for Charcon          
        Signals.CAN_Signals["VCU_OBCMode_Cmd"] = "standby"  
        Signals.CAN_Signals["VCU_uDcReqChrgr"] = 0
        Signals.CAN_Signals["VCU_iDcLimChrgr"] = 0
        
        #Open Contractor After Reset
        Signals.Contractor_op = 0
        subprocess.run("echo 0 > /sys/class/gpio/gpio141/value", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        Signals.CAN_Signals["contactorsStatus"] = "open"
        Signals.CAN_Signals["HV_HVIL_Sts"] = "HVIL Open"
        
        TotCost = usedGridEnergy*Signals.HMI_Signals["CostPerKwh"]
        
        Signals.HMI_Signals.update({
        "SolarEnergy": "{:.3f}".format(usedSolarEnergy),
        "GridEnergy": "{:.3f}".format(usedGridEnergy),
        "ySolarPwr": 0,
        "yGridPwr": 0,
        "xTime": 0,
        "TotCost": "{:.3f}".format(TotCost),
        "PauseTimer": 0,
        "StopEventAck": enum["StopEventAck"]["Event message NOT Received"],
        "ChargingState": enum["ChargingState"]["Charging Complete"],
        })
        
        sendMqttMsg(client)
        
        if(Signals.CAN_Signals["evConnectionState"] == "disconnected"):
            print("Charger Unplugged")
            chargeState = "Disconnect"
            Signals.HMI_Signals["ChargingState"] = enum["ChargingState"]["Charger Unplugged"]
            sendMqttMsg(client)
    
    elif chargeState == "Disconnect" or chargeState == "Failure":
        pass
    
    else:
        print(f"Undefined Charging State {chargeState}")
        chargeState = "Failure"
        
        
        
        
            
            


