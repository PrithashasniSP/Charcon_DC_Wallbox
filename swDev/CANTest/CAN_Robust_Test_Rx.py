import can
import time

#Get start time for reference
startTime = time.time()

# Create a CAN bus interface object (adjust the channel name as needed)
bus = can.interface.Bus(channel='can0', bustype='socketcan')

print("Waiting for CAN Frames...")
# Receive CAN messages in a loop
while True:
    try:
        received_message = bus.recv(timeout=1.0)  # Set a timeout (in seconds) for receiving messages
        if received_message is not None:
            frame_id = "0x{:X}".format(received_message.arbitration_id)
            data_str = ' '.join(['{:02x}'.format(byte) for byte in received_message.data])
            #print(f"RX\tTimestamp: {(received_message.timestamp - startTime):.6f}\tFrame ID={frame_id}\tData= [{data_str}]")
            
            Rx_int = [int(byte) for byte in received_message.data]
            Tx_int = [(x + 1)%256 for x in Rx_int]
            
            #Wait for 10ms before returning the frame
            #time.sleep(0.01)
            
            TimeStamp = time.time()
            # Send a CAN message
            message = can.Message(timestamp = TimeStamp, arbitration_id=(received_message.arbitration_id + 0x300), data=Tx_int)
            bus.send(message)
            
            frame_id = "0x{:X}".format(message.arbitration_id)
            data_str = ' '.join(['{:02x}'.format(byte) for byte in message.data])
            
            # Print the CAN frame info with timestamp to standard output
            print(f"TX\tTimestamp: {(message.timestamp - startTime):.6f}\tFrame ID={frame_id}\tData= [{data_str}]\n")
            
            # Set received_message back to None to clear it for the next message
            received_message = None
            
    except KeyboardInterrupt:
        break

# Close the CAN bus interface
bus.shutdown()
