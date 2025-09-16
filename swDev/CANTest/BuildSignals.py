import CAN_Matrix
import os

# Get the directory of the current Python script
script_directory = os.path.dirname(os.path.abspath(__file__))
print("Directory of the current Python script:", script_directory)

sigFileName = os.path.join(script_directory, "CAN_Signals.py")

#Create CanSignals.py
sigFile = open(sigFileName, "w")

sigFile.write("CAN_Signals = {\n")

for FrameID in CAN_Matrix.DataBase.values():
    for signal in FrameID.keys():
        sigFile.write("\t\""+signal+"\": None,\n")

sigFile.write("}")

sigFile.close()

print(f"Successfully Created \'{sigFileName}\'")