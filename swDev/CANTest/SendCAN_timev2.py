import can
import CAN_Matrix
from CAN_Signals import CAN_Signals
import threading
import time

numFrames = 1
sendFrames = {
    0x301:[],
    }
start_time = time.perf_counter()

# Create a function to convert raw signal data into physical value
def convert_to_raw(PhyVal, sigInfo):
      
    rawVal = None
    
    # endian translation
    endTra = {
        'intel':'little',
        'motorola': 'big',
    }
    
    # Apply value table if available
    if ("value_table" in sigInfo) and (sigInfo["value_table"] is not None) and (PhyVal in sigInfo["value_table"].values()):
        if PhyVal in sigInfo["value_table"].values():
            for key, value in sigInfo["value_table"].items():
                if value == PhyVal:
                    rawVal = key
                    break    
    else:
        # Ensure the physical value is within the defined min and max values
        if "min" in sigInfo:
            rawVal = max(PhyVal, sigInfo["min"])
        if "max" in sigInfo:
            rawVal = min(PhyVal, sigInfo["max"])
            
        # Apply offset if available
        if "offset" in sigInfo:
            rawVal = PhyVal - sigInfo["offset"]
        
        # Apply conversion factor if available
        if "factor" in sigInfo:
            rawVal = round(rawVal/sigInfo["factor"])
        
        #if negative, convert to 2's compliment:
        if rawVal < 0:
            rawVal = (1<<sigInfo["length"]) + rawVal
        
    # modify byte order if more that 1 byte:
    byteSize = (sigInfo["length"]+7)//8 # 7 is added to ensure rounding off happens
    if byteSize > 1:
        rawBytes = rawVal.to_bytes(byteSize, byteorder='little')
        rawVal = int.from_bytes(rawBytes, byteorder=endTra[sigInfo["byte_order"]])
        
    return rawVal 

def Create_Frame(frame_id, matrix):
    signals = matrix[frame_id]
    # Determine the required data length based on the CAN matrix
    data_length = max((signal_info["start_bit"] + signal_info["length"] - 1) // 8 + 1 for signal_info in signals.values())
    
    frame = [0]*data_length
    for signal_name, signal_info in signals.items():
        start_bit = signal_info["start_bit"]
        length = signal_info["length"]

        # Get the signal value from the signal_values dictionary
        signal_value = convert_to_raw(CAN_Signals[signal_name],signal_info) 

        # Calculate the mask for the signal
        mask = (1 << length) - 1

        # Calculate the byte offset and bit offset within the byte
        byte_offset = start_bit // 8
        bit_offset = start_bit % 8

        # Check if the signal spans multiple bytes
        if bit_offset + length > 8:
            # Calculate how many bits can be placed in the first byte
            bits_in_first_byte = 8 - bit_offset

            # Update the first byte
            frame[byte_offset] |= (signal_value & ((1 << bits_in_first_byte) - 1)) << bit_offset

            # Calculate how many bits are left for the next byte
            bits_remaining = length - bits_in_first_byte

            # Update the remaining bytes
            for i in range(byte_offset + 1, byte_offset + (bits_remaining // 8) + 1):
                frame[i] |= (signal_value >> bits_in_first_byte) & 0xFF
                bits_remaining -= 8

        else:
            # The signal fits entirely within a single byte
            frame[byte_offset] |= (signal_value & mask) << bit_offset
   
    return frame
    
    
# Create a function to send CAN messages
def send_CAN():
    global sendFrames
    
    # Create a CAN bus interface object (adjust the channel name as needed)
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    
    # LastFrameTime = [startTime]*numFrames
    FrameCycleTime = 0.25
    nextCall = time.perf_counter()
    while True:
        try:                       
            
            nextCall += FrameCycleTime
            #print(f"SendFrames: {sendFrames}")                   
            # Send a CAN message
            for frame_id, data in sendFrames.items():
                # CAN data
                #print(f"frameID: {frame_id}     date: {data}")
                if(len(data) != 0):
                    send_message = can.Message(arbitration_id=frame_id, data=data)
                    bus.send(send_message)
                    print(f"frame {frame_id} sent with data {data}")
                else:
                    print(f"no data in frame {frame_id}. Frame not sent!")
            
            while (time.perf_counter() < nextCall):
                pass
            
            #OldCycleTime = time.perf_counter()
            
        except KeyboardInterrupt:
            break

# Create a thread for receiving CAN messages
can_thread = threading.Thread(target=send_CAN)
can_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits

# Start the CAN thread
can_thread.start()

# Main program
try:
    while True:
        # if received_message is not None:
        #     # Extract the CAN data from CAN frame
        #     extracted_data = extract_signals(received_message, CAN_Matrix.DataBase)
        #     # Generate the CAN Dump Message
        #     frame_id = "0x{:X}".format(received_message.arbitration_id)
        #     data_str = ' '.join(['{:02x}'.format(byte) for byte in received_message.data])
        #     DumpMsg = "TimeStamp: "+str(received_message.timestamp)+ "\tID: "+ frame_id + "\tData: "+ data_str + " "*(30 - len(data_str)) + "DLC: " + str(received_message.dlc)
            
        #     # f.write(DumpMsg+"\n")
        #     # f.flush()
        #     print("\n",DumpMsg)
            
        #     if extracted_data is not None:
        #         # f.write(str(extracted_data)+"\n\n")
        #         # f.flush()
        #         print(str(extracted_data))
            
        #     #Print All signals
        #     #print(str(CanSignals) + "\n")

        #     # Set received_message back to None to clear it for the next message
        #     received_message = None
        
        CAN_Signals.update({
            "targetContactorsStatus": "open",
            "evConnectionState": "connected",
            "chargingState": "charge",
            "targetVoltage": 200,
            "targetCurrent": -10.7,
            "batteryStateOfCharge": 45,
            "cableCheckVoltage ": 400,
        })
        
        for frame in sendFrames.keys():
            frame_id = "0x{:X}".format(frame)
            sendFrames[frame] = Create_Frame(frame_id,CAN_Matrix.DataBase)
        
        # print(f"SendFrames: {sendFrames}")
        

        # Other main program logic can go here
        # ...
except KeyboardInterrupt:
    pass

# Wait for the CAN thread to finish (if necessary)
can_thread.join()

# Optionally, perform cleanup or other tasks before exiting the program
# f.close()