import paho.mqtt.client as mqtt

# Maximum number of messages to keep in the text file
max_messages = 100

# Text file to save the received messages
output_file = r"C:\Users\XDX1COB\XDX1COB\Charcon\mqttHMI\received_messages.txt"

def create_mqtt_client(client_id, broker_address, port=1883):
    """
    Create and configure an MQTT client.

    Parameters:
    - client_id (str): The client ID for the MQTT client.
    - broker_address (str): The MQTT broker's address.
    - port (int, optional): The port to connect to on the broker. Default is 1883.

    Returns:
    - mqtt.Client: An MQTT client configured with the provided client ID and broker address.
    """
    client = mqtt.Client(client_id)
    client.connect(broker_address, port)
    return client

def logout_mqtt_client(client):
    """
    Log out (disconnect) an MQTT client based on its client passed.

    Parameters:
    - client : MQTT client to log out.
    """
    client.disconnect()
    client.loop_stop()

    print("Subscriber stopped.")

# Callback when a message is received on the subscribed topic
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()

    
    print(f"Received message on topic '{topic}': {payload}")
    # Save the received message to the text file
    with open(output_file,'a+') as f:
         f.write("Message Topic: " + topic + " : "  + payload + "\n")
        
    # Check the number of lines in the file
    num_lines = sum(1 for line in open(output_file))

    # If the number of lines exceeds max_messages, truncate the file to keep only the latest messages
    if num_lines > max_messages:
        lines_to_keep = num_lines - max_messages
        with open(output_file, 'r') as f:
            lines = f.readlines()
        with open(output_file, 'w') as f:
            f.writelines(lines[lines_to_keep:])

# Function to subscribe to multiple MQTT topics
def subscribe_to_topics(client,broker_address,port,topics):
    try:
        # Set the message callback
        client.on_message = on_message

        # Connect to the MQTT broker
        client.connect(broker_address, port)

        # Subscribe to each specified topic
        for topic in topics:
            client.subscribe(topic)
            print(f"Subscribed to topic '{topic}'...")

        # Start the MQTT client's internal loop to handle incoming messages
        client.loop_start()


    except KeyboardInterrupt:
        # Disconnect and stop the MQTT client when Ctrl+C is pressed
        client.disconnect()
        client.loop_stop()
        print("Subscriber stopped.")


# Example usage of the function
if __name__ == "__main__":
    
    # MQTT Broker Settings
    broker_address = "localhost"
    port = 1883

    # Create a unique client ID
    client_id = "clientHMI"

    # Create an MQTT client
    client = create_mqtt_client(client_id, broker_address, port)
    topics_to_subscribe = ["/DCWallbox/HMI/AllPage/HealthIcon/", 
                           "/DCWallbox/HMI/ChargingProgressPage/SolarEnergy/", 
                           "/DCWallbox/HMI/ChargingProgressPage/TotCost/"]  # Replace with your desired MQTT topics
    subscribe_to_topics(client,broker_address,port,topics_to_subscribe)
