from SubHMIv2a import *
import time
'''
1. create client for HMI and login
2. Subscribe Messages Save the last 100 values in txt
3. Logout when asked (Create a timed logout for test)

'''
######################################################
# 1. create client for HMI and login
######################################################
# MQTT Broker Settings
broker_address = "localhost"
port = 1883

# Create a unique client ID
client_id = "clientHMI"

# Create an MQTT client
client = create_mqtt_client(client_id, broker_address, port)

######################################################
# 2. Subscribe Messages and save in txt file
######################################################
csv_filename = "E:\MQTT\mqttHMI\last_20_messages.csv"

topics_to_subscribe = [#"/DCWallbox/HMI/AllPage/HealthIcon/", 
                          # "/DCWallbox/HMI/ChargingProgressPage/SolarEnergy/", 
                           #"/DCWallbox/HMI/ChargingProgressPage/TotCost/",
                           "/DCWallbox/HMI/ChargingProgressPage/#"]  # Replace with your desired MQTT topics

subscribe_to_topics(client,broker_address,port,topics_to_subscribe)


######################################################
# 3.Logout when asked (Create a timed logout for test)
######################################################

abort_after = 20
start = time.time()

subStatus = True
while subStatus:


    delta = time.time() - start
    if delta >= abort_after:
        subStatus = False
        logout_mqtt_client(client)
        #print("timeout_start : ",start)
        #print("Session Completed : ",delta)
        break

    time.sleep(1)
    
