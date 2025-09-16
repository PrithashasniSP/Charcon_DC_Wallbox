import can
import time

# Create a CAN bus interface object (adjust the channel name as needed)
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Send a CAN message
message = can.Message(arbitration_id=0x123, data=[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])
bus.send(message)

# Receive CAN messages in a loop
while True:
    try:
        received_message = bus.recv(timeout=1.0)  # Set a timeout (in seconds) for receiving messages
        if received_message is not None:
            print(f"Received message: {received_message}")
    except KeyboardInterrupt:
        break

# Close the CAN bus interface
bus.shutdown()
