import CAN_Matrix
from CAN_Signals import CAN_Signals

sendFrames = {
    0x186:[],
    0x304:[],
    0x305:[],
    0x302:[],
    0x303:[],
    }

CAN_Signals.update({
            "mc_VCU_OBCControl": 9,
            "VCU_OBCMode_Cmd": "charging",
            "VCU_uDcReqChrgr": 256.5,
            "VCU_iDcLimChrgr": 18.6,
            "VCU_iAcMaxAllwdChrgr": 14.9,
            "CRC_VCU_OBCControl": 24,
            "limitVoltageMin": 0.1,
            "limitVoltageMax": 600,
            "limitPowerMax": 0.5,
            "limitPowerMin": 11000,
            "limitCurrentMin": 0.6,
            "limitCurrentMax": 25,
            "contactorsStatus": "closed",
            "operationalStatus": "inoperative",
            "isolationStatus": "valid",
            "drivenVoltage": 365.2,
            "drivenCurrent": 16.7,
            "temperature": 37.6,
            "measuredVoltage": 366.5,
            "measuredCurrent": 15.8,
        })

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


frame = Create_Frame("0x186", CAN_Matrix.DataBase)


for frame in sendFrames.keys():
    frame_id = "0x{:X}".format(frame)
    sendFrames[frame] = Create_Frame(frame_id,CAN_Matrix.DataBase)
    frameStr = ' '.join(['{:02x}'.format(byte) for byte in sendFrames[frame]])
    print(f"{frame_id} : {frameStr}")


