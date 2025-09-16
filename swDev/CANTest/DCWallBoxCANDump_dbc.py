import canmatrix

# Load the DBC file with the 'dbc' import type
db = canmatrix.formats.load('DCWB_OCDC_v1.dbc', 'dbc')

# Check if loading the DBC file was successful
if isinstance(db, canmatrix.CanMatrix):
    # Create a CAN bus interface object (adjust the channel name as needed)
    bus = can.interface.Bus(channel='can0', bustype='socketcan')

    # Receive and decode CAN messages in a loop
    while True:
        try:
            received_message = bus.recv(timeout=1.0)  # Set a timeout (in seconds) for receiving messages
            if received_message is not None:
                # Get the message name from the DBC
                message_id = received_message.arbitration_id
                message = db.frame_by_id(message_id)

                if message is not None:
                    # Decode signals using the DBC definition
                    decoded_signals = message.decode(received_message.data)
                    # Print the decoded message and signals
                    print(f"Message Name: {message.name}")
                    print(f"Received Message: {received_message}")
                    print(f"Decoded Signals: {decoded_signals}")
        except KeyboardInterrupt:
            break

    # Close the CAN bus interface
    bus.shutdown()
else:
    print("Failed to load the DBC file.")


