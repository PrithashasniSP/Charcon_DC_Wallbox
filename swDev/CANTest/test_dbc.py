import can
import canmatrix

# Load the DBC file
db = canmatrix.formats.loadp('DCWB-PEP-CAN-v1.4.1.dbc')

# Create a CAN bus interface
bus = can.interface.Bus(channel='can0', bustype='socketcan')

try:
    while True:
        # Receive a CAN message
        msg = bus.recv()

        # Find the message definition in the DBC database
        msg_def = db.frame_by_id(msg.arbitration_id)

        if msg_def:
            # Decode the CAN message using the message definition
            decoded_msg = canmatrix.DecodedMessage(msg_def).decode(msg.data)

            # Print the decoded message
            print(decoded_msg)

except KeyboardInterrupt:
    # Clean up when Ctrl+C is pressed
    bus.shutdown()