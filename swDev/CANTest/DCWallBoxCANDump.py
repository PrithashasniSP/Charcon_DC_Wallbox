import can
import CAN_Matrix
from CanSignals import CanSignals
import threading


f = open("candump.txt", "w")

# Global variable to store the received CAN message
received_message = None

# Create a function to convert raw signal data into physical value
def convert_to_Phys(rawVal, sigInfo):
      
    # endian translation
    endTra = {
        'intel':'little',
        'motorola': 'big',
    }
    
    # value Type translation
    valTypeTra = {
        'unsigned' : False,
        'signed' : True,
    }
    
    # Convert raw value to integer value
    byteSize = (sigInfo["length"]+7)//8 # 7 is added to ensure rounding off happens
    rawBytes = rawVal.to_bytes(byteSize, byteorder='little')
    PhyVal = int.from_bytes(rawBytes, byteorder=endTra[sigInfo["byte_order"]], signed=valTypeTra[sigInfo["value_type"]])
    
    # Apply value table if available
    if "value_table" in sigInfo and sigInfo["value_table"] is not None:
        if PhyVal in sigInfo["value_table"]:
            return sigInfo["value_table"][PhyVal]
    
    # Apply conversion factor if available
    if "factor" in sigInfo:
        PhyVal *= sigInfo["factor"]
        
    # Apply offset if available
    if "offset" in sigInfo:
        PhyVal += sigInfo["offset"]
        
    # Ensure the scaled value is within the defined min and max values
    if "min" in sigInfo:
        PhyVal = max(PhyVal, sigInfo["min"])
    if "max" in sigInfo:
        PhyVal = min(PhyVal, sigInfo["max"])
    
    return PhyVal

# Create a function to extract the signals based on the can matrix
def extract_signals(frame, matrix):
    frame_id = "0x{:X}".format(frame.arbitration_id)
    if frame_id in matrix:
        signals = matrix[frame_id]
        extracted_data = {}
        for signal_name, signal_info in signals.items():
            start_bit = signal_info["start_bit"]
            length = signal_info["length"]
            data_int = int.from_bytes(frame.data, byteorder='little', signed=False)
            raw_signal_data = (data_int >> start_bit) & ((1 << length) - 1)
            PhysVal = convert_to_Phys(raw_signal_data, signal_info)
            extracted_data[signal_name] = PhysVal
            
            #Also update the Global signal values:
            CanSignals[signal_name] = PhysVal
                        
        return extracted_data
    else:
        return None

# Create a function to receive CAN messages
def receive_can_messages():
    global received_message

    # Create a CAN bus interface object (adjust the channel name as needed)
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    while True:
        try:
            received_message = bus.recv(timeout=1.0)  # Set a timeout (in seconds) for receiving messages
        except KeyboardInterrupt:
            break

    # Close the CAN bus interface
    bus.shutdown()

# Create a thread for receiving CAN messages
can_thread = threading.Thread(target=receive_can_messages)
can_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits

# Start the CAN thread
can_thread.start()

# Main program
try:
    print("Waiting for CAN Frames...")
    while True:
        if received_message is not None:
            # Extract the CAN data from CAN frame
            extracted_data = extract_signals(received_message, CAN_Matrix.DataBase)
            # Generate the CAN Dump Message
            frame_id = "0x{:X}".format(received_message.arbitration_id)
            data_str = ' '.join(['{:02x}'.format(byte) for byte in received_message.data])
            DumpMsg = "TimeStamp: "+str(received_message.timestamp)+ "\tID: "+ frame_id + "\tData: "+ data_str + " "*(30 - len(data_str)) + "DLC: " + str(received_message.dlc)
            
            f.write(DumpMsg+"\n")
            f.flush()
            print("\n",DumpMsg)
            
            if extracted_data is not None:
                f.write(str(extracted_data)+"\n\n")
                f.flush()
                print(str(extracted_data))
            
            #Print All signals
            #print(str(CanSignals) + "\n")

            # Set received_message back to None to clear it for the next message
            received_message = None

        # Other main program logic can go here
        # ...
except KeyboardInterrupt:
    pass

# Wait for the CAN thread to finish (if necessary)
can_thread.join()

# Optionally, perform cleanup or other tasks before exiting the program
f.close()