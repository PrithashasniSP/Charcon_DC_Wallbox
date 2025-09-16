import can
import CAN_Matrix
import Signals
import threading
import time
from collections import OrderedDict

sendFrames_100ms = OrderedDict({
    0x5D0:None,
    0x5C0:None,
    0x5C1:None,
    0x5C2:None,
    0x5C3:None,
    })
sendFrames_250ms = OrderedDict({
    0x301:None,
    0x308:None,
    0x30A:None,
    0x30B:None,
    0x30D:None,
    })

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

# Create a function to convert physical value into raw signal data 
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
            Signals.CAN_Signals[signal_name] = PhysVal
                        
        return extracted_data
    else:
        return None

# Create a function to Build CAN frame based on the frame ID and CAN Matrix passed
def Create_Frame(frame_id, matrix):
    signals = matrix[frame_id]
    # Determine the required data length based on the CAN matrix
    data_length = max((signal_info["start_bit"] + signal_info["length"] - 1) // 8 + 1 for signal_info in signals.values())
    
    frame = [0]*data_length
    for signal_name, signal_info in signals.items():
        start_bit = signal_info["start_bit"]
        length = signal_info["length"]

        # if any of the signals in the frame are not defined, make frame as empty so not frames are sent.
        if(Signals.CAN_Signals[signal_name] is None):
            return None
        
        # Get the signal value from the signal_values dictionary            
        signal_value = convert_to_raw(Signals.CAN_Signals[signal_name],signal_info) 

        # Calculate the mask for the signal
        mask = (1 << length) - 1

        # Calculate the byte offset and bit offset within the byte
        byte_offset = start_bit // 8
        bit_offset = start_bit % 8

        # Check if the signal spans multiple bytes
        if bit_offset + length > 8:
            # Calculate how many bits can be placed in the first byte
            bits_filled = 8 - bit_offset

            # Update the first byte
            frame[byte_offset] |= (signal_value & ((1 << bits_filled) - 1)) << bit_offset

            # Calculate how many bits are left for the next byte
            bits_remaining = length - bits_filled

            # Update the remaining bytes
            i = byte_offset + 1
            while bits_remaining > 0:
                frame[i] |= (signal_value >> bits_filled) & 0xFF
                bits_filled += 8
                bits_remaining -= 8
                i+=1

        else:
            # The signal fits entirely within a single byte
            frame[byte_offset] |= (signal_value & mask) << bit_offset
   
    return frame
    
# Create a function to send CAN messages every 100ms
def send_can_messages_100ms():
    global sendFrames_100ms
    
    # Create a CAN bus interface object (adjust the channel name as needed)
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    
    # LastFrameTime = [startTime]*numFrames
    FrameCycleTime = 0.1
    
    while True:
        try:                                       
            begin = time.perf_counter()
            
            # Send a CAN message
            for data in sendFrames_100ms.values():
                # Check if CAN data available to be transmitted
                if(data is not None):
                    bus.send(data) 
            
            while ((time.perf_counter() - begin) < FrameCycleTime):
                pass
            
            # Debug code to see the cycle time
            # end = time.perf_counter()
            # print(f"Cycle Time = {end - begin}")
            
        except KeyboardInterrupt:
            break
        
def send_can_messages_250ms():
    global sendFrames_250ms
    
    # Create a CAN bus interface object (adjust the channel name as needed)
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    
    # LastFrameTime = [startTime]*numFrames
    FrameCycleTime = 0.25
    
    while True:
        try:                                       
            begin = time.perf_counter()
            
            # Send a CAN message
            for data in sendFrames_250ms.values():
                # Check if CAN data available to be transmitted
                if(data is not None):
                    bus.send(data) 
            
            while ((time.perf_counter() - begin) < FrameCycleTime):
                pass
            
            # Debug code to see the cycle time
            # end = time.perf_counter()
            # print(f"Cycle Time = {end - begin}")
            
        except KeyboardInterrupt:
            break

def ProcessCAN():
    
    # Create a thread for Sending 100ms CAN messages
    send100_can_thread = threading.Thread(target=send_can_messages_100ms)
    send100_can_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits

    # Start the CAN thread
    send100_can_thread.start()
    
    # Create a thread for Sending 100ms CAN messages
    send250_can_thread = threading.Thread(target=send_can_messages_250ms)
    send250_can_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits

    # Start the CAN thread
    send250_can_thread.start()

    # Main program
    try:
        while True:            
            
            for frame in sendFrames_100ms.keys():
                frame_id = "0x{:X}".format(frame)
                data = Create_Frame(frame_id,CAN_Matrix.DataBase)
                if data is not None:
                    sendFrames_100ms[frame] = can.Message(arbitration_id=frame, data=data, is_extended_id=False)
                    #sendFrames_100ms[frame] = can.Message(arbitration_id=frame, data=data)
                else:
                    sendFrames_100ms[frame] = None
                    #print("Data is None")      #Debug Code
                
            for frame in sendFrames_250ms.keys():
                frame_id = "0x{:X}".format(frame)
                data = Create_Frame(frame_id,CAN_Matrix.DataBase)
                if data is not None:
                    sendFrames_250ms[frame] = can.Message(arbitration_id=frame, data=data, is_extended_id=False)
                    #sendFrames_250ms[frame] = can.Message(arbitration_id=frame, data=data)
                else:
                    sendFrames_250ms[frame] = None
                    #print("Data is None")      #Debug Code

    except KeyboardInterrupt:
        pass
