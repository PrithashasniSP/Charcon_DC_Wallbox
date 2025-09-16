import CAN_Matrix
import os

# Get the directory of the current Python script
script_directory = os.path.dirname(os.path.abspath(__file__))
print("Directory of the current Python script:", script_directory)

sigFileName = os.path.join(script_directory, "Signals.py")

#Create CanSignals.py
sigFile = open(sigFileName, "w")

sigFile.write("CAN_Signals = {\n")

for FrameID in CAN_Matrix.DataBase.values():
    for signal in FrameID.keys():
        sigFile.write("\t\""+signal+"\": None,\n")

sigFile.write("}\n\n")

sigFile.write('''
HMI_Signals = {
    "HealthIcon": None,
    "SolarEnergy": None,
    "GridEnergy": None,
    "ySolarPwr": None,
    "yGridPwr": None,
    "xTime": None,
    "TotCost": None,
    "PauseTimer": None,
    "StopEventAck": None,
    "ChargingState": None,
    "CostPerKwh": None,
    "MaxGridCurrent": None,
    "SolarPanelArea": None,
    "StopEvent": None,
    }
    
OCPP_Signals = {
    "Voltage": 0,
    "Current": 0,
}
    
IMD_ip = None
Contractor_op = 0 #{0: open, 1: Closed}

CntrCharConFrameRecv = 0
CntrVseccFrameRecv = 0

MaxOutPwr = None

StopChargingEv = False
StopChargingHMI = False

EnergyTransferActive = False
''')

sigFile.close()

print(f"Successfully Created \'{sigFileName}\'")