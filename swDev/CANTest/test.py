DataBase = {
    "0x301": {
        "targetContactorsStatus": {
            "start_bit": 0,
            "length": 1,
            "byte_order": 'intel',
            "value_type": 'unsigned',
            "factor": 1,
            "offset": 0,
            "min": 0,
            "max": 1,
            "value_table" : {
                0: "open",
                1: "closed",                
            }
        },
        "evConnectionState": {
            "start_bit": 1,
            "length": 2,
            "byte_order": 'intel',
            "value_type": 'unsigned',
            "factor": 1,
            "offset": 0,
            "min": 0,
            "max": 3,
            "value_table" : {
                0: "disconnected",
                1: "connected",    
                2: "energyTransferAllowed",   
                3: "error",              
            }
        },
        "chargingState": {
            "start_bit": 3, 
            "length": 3,
            "byte_order": 'intel',
            "value_type": 'unsigned',
            "factor": 1,
            "offset": 0,
            "min": 0,
            "max": 7,
            "value_table" : {
                0: "standby",
                1: "cableCheck",    
                2: "preCharge",   
                3: "charge",
                4: "postCharge",             
            }
        },
        "targetVoltage": {
            "start_bit": 8, 
            "length": 16,
            "byte_order": 'intel',
            "value_type": 'unsigned',
            "factor": 0.1,
            "offset": 0,
            "min": 0,
            "max": 6553.5,
            "value_table" : None,
            
        },
        "targetCurrent": {
            "start_bit": 24,
            "length": 16,
            "byte_order": 'intel',
            "value_type": 'signed',
            "factor": 0.1,
            "offset": 0,
            "min": -3276.8,
            "max": 3276.7,
            "value_table" : None,
        },
        "batteryStateOfCharge": {
            "start_bit": 40, 
            "length": 7,
            "byte_order": 'intel',
            "value_type": 'unsigned',
            "factor": 1,
            "offset": 0,
            "min": 0,
            "max": 100,
            "value_table" : None,
        },
        "cableCheckVoltage ": {
            "start_bit": 48, 
            "length": 16,
            "byte_order": 'intel',
            "value_type": 'unsigned',
            "factor": 1,
            "offset": 0,
            "min": 0,
            "max": 65535,
            "value_table" : None,
            },        
    },
}

CanSignals = {
	"targetContactorsStatus": "closed",
	"evConnectionState": "energyTransferAllowed",
	"chargingState": "postCharge",
	"targetVoltage": 200,
	"targetCurrent": -10.47,
	"batteryStateOfCharge": 45,
	"cableCheckVoltage ": 400,
}

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
        signal_value = convert_to_raw(CanSignals[signal_name],signal_info) 

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


frame = Create_Frame("0x301", DataBase)
frameStr = ' '.join(['{:02x}'.format(byte) for byte in frame])

frame_id = int("0x301", 16)

print(frame_id)
print(frame)
print(frameStr)