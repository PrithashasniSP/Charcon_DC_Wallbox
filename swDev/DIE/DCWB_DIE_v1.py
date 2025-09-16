from CAN_Interface import ProcessCAN
from init import init
import Signals
import MQTT_publish
from MQTT_subscribe import MQTT_Sub_Start
import DIE_AllStates
import DIE_BootCtrl
import DIE_Failure
import DIE_MissingConfig
import DIE_HealthCheck
import DIE_Ready
import DIE_ChargeInit
import DIE_Charging
import threading
import time
import sys
import subprocess

#Access Command Line Arguments
""" 
Format: python3 <filename.py> <CAN_Avl> <GSM_Avl> <MQTT_Avl>
"""
args = sys.argv

if len(args) < 4:
    print("Insufficient arguments Passed to the program")
    sys.exit(1)
    
elif len(args) > 4:
    print("Too many arguments Passed to the program")
    sys.exit(1)

for arg in args[3:]:
    if arg not in ('0', '1'):
        print(f"Error: Argument '{arg}' is not a valid boolean value (use '0' or '1').")
        sys.exit(1)
        
CAN_Avl = bool(int(args[1]))
GSM_Avl = bool(int(args[2]))
MQTT_Avl = bool(int(args[3]))

#Define Current and Previous States of the DIE
'''
valid States: ["BootCtrl", "MissingConfig", "Failure", "HealthCheck", "Ready", "ChargeInit", "Charging"]
'''
CurrentState = "BootCtrl"
PrevState = CurrentState

Time = time.perf_counter()

# Configure GPIO Pins of iMx
result = subprocess.run("echo 141 > /sys/class/gpio/export", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result = subprocess.run("echo out > /sys/class/gpio/gpio141/direction", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result = subprocess.run("echo 139 > /sys/class/gpio/export", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result = subprocess.run("echo in > /sys/class/gpio/gpio139/direction", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Create a thread for Sending and receiving CAN messages
getCAN_thread = threading.Thread(target=ProcessCAN)
getCAN_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits
getCAN_thread.start() # Start the CAN thread

# Set up MQTT Client for Publishing
client = MQTT_publish.connect_mqtt()
client.loop_start()  

# Set up MQTT Client for Subscribing in a thread
MQTT_Sub_Thread = threading.Thread(target=MQTT_Sub_Start)
MQTT_Sub_Thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits
MQTT_Sub_Thread.start() # Start the CAN thread
        
# Main Program
try:
    #print("Booting!")
    BootStatus = DIE_BootCtrl.BootCtrl(CAN_Avl,GSM_Avl,MQTT_Avl)
    
    if BootStatus == DIE_BootCtrl.StateEnum["Failure"]:
        # Go to Wallbox Failure
        PrevState = CurrentState
        CurrentState = "Failure"
        print("Wall Box Failure Has Occured!")
    
    elif BootStatus == DIE_BootCtrl.StateEnum["Missing Config"]:
        # Go to Missing Configuration State
        PrevState = CurrentState
        CurrentState = "MissingConfig"
    
    elif BootStatus == DIE_BootCtrl.StateEnum["Valid"]:
        # Boot Successful        
        # Initialize signals
        init()
        
        DIE_AllStates.AllStates(client)
        
        if(DIE_AllStates.flgError):
            # Go to Wallbox Failure
            PrevState = CurrentState
            CurrentState = "Failure"
            print("Wall Box Failure Has Occured!")
        
        #print("Boot Successful!")
        PrevState = CurrentState
        CurrentState = "HealthCheck"
        print("Health Check Started!")
    
    else:
        print("BootControl Code not executed properly")
        sys.exit(1)
      
    while True: 
         
        # WALLBOX FAILURE STATE
        while CurrentState == "Failure":
            DIE_Failure.WallBoxFailure(client)
            DIE_AllStates.AllStates(client)
            #time.sleep(1)
        
        # MISSING CONFIGURATION STATE
        while CurrentState == "MissingConfig":
            DIE_MissingConfig.MissingConfig(client)
            
            if DIE_MissingConfig.CheckConfigAvl():
                # Go to Health Check
                PrevState = CurrentState
                CurrentState = "HealthCheck"
                print("Health Check Started!")
                
            DIE_AllStates.AllStates(client)
            
            if(DIE_AllStates.flgError):
                # Go to Wallbox Failure
                PrevState = CurrentState
                CurrentState = "Failure"
                print("Wall Box Failure Has Occured!")
                
            #time.sleep(1)
        
        # HEALTH CHECK STATE
        while CurrentState == "HealthCheck":
            DIE_HealthCheck.HealthCheck(client)
            
            if(DIE_HealthCheck.HealthCheckState == DIE_HealthCheck.HealthCheckStateEnum["Failure"]):
                # Go to Wallbox Failure
                PrevState = CurrentState
                CurrentState = "Failure"
                print("Wall Box Failure Has Occured!")
                
            elif(DIE_HealthCheck.HealthCheckState == DIE_HealthCheck.HealthCheckStateEnum["Good"]):
                # Go to Ready to Charge State
                PrevState = CurrentState
                CurrentState = "Ready"
                print("Ready to Charge!")
            
            
            DIE_AllStates.AllStates(client)
        
            if(DIE_AllStates.flgError):
                # Go to Wallbox Failure
                PrevState = CurrentState
                CurrentState = "Failure"
                print("Wall Box Failure Has Occured!")
                
            #time.sleep(1)
        
        # READY TO CHARGE STATE
        while CurrentState == "Ready":
            DIE_Ready.Ready(client, PrevState)
            
            if(DIE_Ready.ConnectionDetected()):
                # Go to Charging Initialization state
                PrevState = CurrentState
                CurrentState = "ChargeInit"
                DIE_ChargeInit.chargeInitState = "standby"
                print("Connection Detected! Initializing Device...")
                             
            DIE_AllStates.AllStates(client)
        
            if(DIE_AllStates.flgError):
                # Go to Wallbox Failure
                PrevState = CurrentState
                CurrentState = "Failure"
                print("Wall Box Failure Has Occured!")
                
            #time.sleep(1)
            
        # CHARGING INITIALIZATION STATE
        while CurrentState == "ChargeInit":                  
            DIE_ChargeInit.ChargingInit(client)
            
            if(DIE_ChargeInit.chargeInitState == "Failure"):
                # Go to Wallbox Failure
                PrevState = CurrentState
                CurrentState = "Failure"
                print("Wall Box Failure Has Occured!")
                
            elif(DIE_ChargeInit.chargeInitState == "charge"):
                # Go to Ready to Charging State
                PrevState = CurrentState
                CurrentState = "Charging"
                DIE_Charging.chargeState = "standby"
                DIE_Charging.usedGridEnergy = 0
                DIE_Charging.usedSolarEnergy = 0
                
                Time = time.perf_counter()
                print("Charging")
                DIE_Charging.oldtime = time.perf_counter()
                
            DIE_AllStates.AllStates(client)
        
            if(DIE_AllStates.flgError):
                # Go to Wallbox Failure
                PrevState = CurrentState
                CurrentState = "Failure"
                print("Wall Box Failure Has Occured!")
                
            #time.sleep(1)
        
        # CHARGINGING STATE
        while CurrentState == "Charging":                  
            DIE_Charging.Charging(client,Time)
            
            if(DIE_Charging.chargeState == "Failure"):
                # Go to Wallbox Failure
                PrevState = CurrentState
                CurrentState = "Failure"
                print("Wall Box Failure Has Occured!")
                
            elif(DIE_Charging.chargeState == "Disconnect"):
                # Go to Ready to Charging State
                PrevState = CurrentState
                CurrentState = "Ready"
                
                print("Ready to Charge!")
                DIE_Ready.oldtime = time.perf_counter()
                
            DIE_AllStates.AllStates(client)
        
            if(DIE_AllStates.flgError):
                # Go to Wallbox Failure
                PrevState = CurrentState
                CurrentState = "Failure"
                print("Wall Box Failure Has Occured!")
                
            #time.sleep(1)
        
except KeyboardInterrupt:
    # Stop MQTT Client
    client.loop_stop()

# Wait for the CAN thread to finish (if necessary)
getCAN_thread.join()

# Wait for the MQTT Subscribe thread to finish (if necessary)
MQTT_Sub_Thread.join()