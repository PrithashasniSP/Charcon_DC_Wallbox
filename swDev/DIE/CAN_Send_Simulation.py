from CAN_Send_Simulation_CAN_Interface import ProcessCAN
from init import init
import threading
import sys

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

# Create a thread for Sending and receiving CAN messages
getCAN_thread = threading.Thread(target=ProcessCAN)
getCAN_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits
getCAN_thread.start() # Start the CAN thread 

        
# Main Program
try:
    print("Initializing CAN Signals to be sent...")
    init()
    print("Initialization complete!")
        
except KeyboardInterrupt:
    print("Ending Program!")
    pass

# Wait for the CAN thread to finish (if necessary)
getCAN_thread.join()