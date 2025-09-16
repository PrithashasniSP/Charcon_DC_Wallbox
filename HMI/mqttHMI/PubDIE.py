import paho.mqtt.client as mqtt
import time
import numpy as np
import threading
from datetime import datetime

# MQTT Broker Settings
broker_address = "localhost"
port = 1883

# Create a unique client ID
client_id = "DIE"

# Create an MQTT client
client = mqtt.Client(client_id)

# Connect to the MQTT broker
client.connect(broker_address, port)

# Set the loop_start to start the MQTT client's internal loop
client.loop_start()

parentTopic = "/DCWallbox/HMI"
# Function to publish AllPage
def publish_AllPage():
    # PageName
    pageName = parentTopic + "/AllPage"
    # Messages
    msgHealthIcon = "/HealthIcon/"
    msgPlugStatus = "/PlugStatus/"
    msgCloudConnection = "/CloudConnection/"

    while True:
        # Message Payloads
        message_payload_HealthIcon = str(np.random.randint(0,4))
        message_payload_PlugStatus = str(np.random.randint(0,3))
        message_payload_CloudConnection = str(np.random.randint(0,3))

        # Publishing Each message
        client.publish(pageName + msgHealthIcon, message_payload_HealthIcon)
        client.publish(pageName + msgPlugStatus, message_payload_PlugStatus)
        client.publish(pageName + msgCloudConnection, message_payload_CloudConnection)
        time.sleep(1)

# Function to publish HealthCheck
def publish_HealthCheck():
    # PageName
    pageName = parentTopic + "/HealthCheck"
    # Messages
    CableCheckStatus = "/CableCheckStatus/"
    PowerBoardStatus = "/PowerBoardStatus/"
    HeartBeatMsg = "/HeartBeatMsg/"

    while True:
        # Message Payloads
        message_payload_CableCheckStatus = str(np.random.randint(0,3))
        message_payload_PowerBoardStatus = str(np.random.randint(0,3))
        message_payload_HeartBeatMsg = str(np.random.randint(0,2))

        # Publishing Each message
        client.publish(pageName + CableCheckStatus, message_payload_CableCheckStatus)
        client.publish(pageName + PowerBoardStatus, message_payload_PowerBoardStatus)
        client.publish(pageName + HeartBeatMsg, message_payload_HeartBeatMsg)
        time.sleep(2)



# Function to publish ChargingProgressPage

def publish_ChargingProgressPage():
    # PageName
    pageName = parentTopic + "/ChargingProgressPage"
    # Messages
    SolarEnergy = "/SolarEnergy/"
    GridEnergy = "/GridEnergy/"
    ySolarPwr = "/ySolarPwr/"
    xTime = "/xTime/"
    TotCost = "/TotCost/"
    TimeHr = "/TimeHr/"
    TimeMin = "/TimeMin/"
    TimeSec = "/TimeSec/"
    StopEventAck = "/StopEventAck/"
    ChargingState = "/ChargingState/"
    StopEvent = "/StopEvent/"

    while True:

        # Message Payloads
        message_payload_SolarEnergy = str(np.random.randint(0,1500))
        message_payload_GridEnergy = str(np.random.randint(0,1500))
        message_payload_ySolarPwr = str(np.random.randint(0,1500))
        message_payload_xTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        message_payload_TotCost = str(np.random.randint(0,100))
        message_payload_TimeHr = str(np.random.randint(0,24))
        message_payload_TimeMin = str(np.random.randint(0,60))
        message_payload_TimeSec = str(np.random.randint(0,60))
        message_payload_StopEventAck = str(np.random.randint(0,2))
        message_payload_ChargingState = str(np.random.randint(0,4))
        message_payload_StopEvent = str(np.random.randint(0,2))

        # Publishing Each message
        client.publish(pageName + SolarEnergy,message_payload_SolarEnergy)
        client.publish(pageName + GridEnergy,message_payload_GridEnergy)
        client.publish(pageName + ySolarPwr,message_payload_ySolarPwr)
        client.publish(pageName + xTime,message_payload_xTime)
        client.publish(pageName + TotCost,message_payload_TotCost)
        client.publish(pageName + TimeHr,message_payload_TimeHr)
        client.publish(pageName + TimeMin,message_payload_TimeMin)
        client.publish(pageName + TimeSec,message_payload_TimeSec)
        client.publish(pageName + StopEventAck,message_payload_StopEventAck)
        client.publish(pageName + ChargingState,message_payload_ChargingState)
        client.publish(pageName + StopEvent,message_payload_StopEvent)
        time.sleep(3)

    
###
# Executing the functions in endless loop

try:
    # Start the topic publishing loops in separate threads
    thread_publish_AllPage = threading.Thread(target=publish_AllPage)
    thread_publish_HealthCheck = threading.Thread(target=publish_HealthCheck)
    thread_publish_publish_ChargingProgressPage = threading.Thread(target=publish_ChargingProgressPage)

    thread_publish_AllPage.start()
    thread_publish_HealthCheck.start()
    thread_publish_publish_ChargingProgressPage.start()

    # Keep the main thread running
    while True:
        pass

except KeyboardInterrupt:
    # Stop the topic publishing loops when Ctrl+C is pressed
    thread_publish_AllPage.join()
    thread_publish_HealthCheck.join()
    thread_publish_publish_ChargingProgressPage.join()

    # Disconnect from the MQTT broker
    client.disconnect()

    # Stop the MQTT client's internal loop
    client.loop_stop()



