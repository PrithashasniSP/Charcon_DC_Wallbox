import can
import time
import threading
import sys
import random

#Get start time for reference
startTime = time.perf_counter()
stopTime = 15

TimerExpired = False

numValid = 0
numSent = 0
numRecv = 0
numChecked = 0


Can_Data_Tx = {}
Can_Data_Rx = {}

#Check_Dict = {}
unCheckedRx = {}

# Create a CAN bus interface object (adjust the channel name as needed)
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Create File for recording the sent and recieved data
log = open("RobustTestLog.txt", "w")
#logDbg = open("RobustTestDebugLog.txt", "w")

# Create a function to send CAN messages
def send_CAN():
    global numSent, Can_Data_Tx

    cntr = 0
    numFrames = 10
    send_message = None
    
    
    LastFrameTime = [startTime]*numFrames
    FrameCycleTime = 0.1
    
    OldCycleTime = startTime
    
    while not TimerExpired:
        try:                       
            #Clear Unchecked data
            #Check_Dict.clear()
                    
            # Send a CAN message
            for i in range(0,numFrames):
                # CAN data
                CanFrameTx = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
                #CanFrameTx = [x%256 for x in CanFrameTx]
                
                Timestamp = time.perf_counter()
                send_message = can.Message(timestamp = Timestamp, arbitration_id=0x101+i, data=CanFrameTx)
                bus.send(send_message)
                numSent += 1
                
                frame_id = "0x{:X}".format(send_message.arbitration_id)                
                cycleTime = (Timestamp - LastFrameTime[i])
                # Store the CAN frame info with timestamp to standard output
                Can_Data_Tx.update({Timestamp : {"direction" : "Tx", "frameID" : frame_id, "data": send_message.data, "DataInt" : CanFrameTx, "cycleTime":cycleTime}})
                
                #GetLog (debug only)
                # logDbg.write(f"Tx\tTimestamp: {(Timestamp - startTime)}\tFrame ID:{frame_id}\tData: [{CanFrameTx}]\n")
                # logDbg.flush()
                
                LastFrameTime[i] = Timestamp
                # increment counter to update the CAN data
                cntr += 1
            
            while ((time.perf_counter() - OldCycleTime) < FrameCycleTime):
                pass
            
            OldCycleTime = time.perf_counter()

            
            
        except KeyboardInterrupt:
            break

# Create a function to receive CAN messages
def recv_CAN():
    global recv_message, numRecv, Can_Data_Rx

    while not TimerExpired:
        try:
            recv_message = bus.recv(timeout=0.1)  # Set a timeout (in seconds) for receiving messages
            
            if recv_message is not None:
                numRecv += 1
                Timestamp = recv_message.timestamp
                
                frame_id = "0x{:X}".format(recv_message.arbitration_id)
                Rx_int = [int(byte) for byte in recv_message.data]
                
                # Store the CAN frame info with timestamp to standard output
                Can_Data_Rx.update({Timestamp : {"direction" : "Rx" ,"frameID" : frame_id, "data": recv_message.data, "DataInt" : Rx_int}})
                                                
                #GetLog (debug only)
                # logDbg.write(f"Rx\tTimestamp: {(Timestamp - startTime)}\tFrame ID:{frame_id}\tData: [{Rx_int}]\n")
                # logDbg.flush()
                
                #set message back to None to clear it for the next message
                recv_message = None
                
        except KeyboardInterrupt:
            break
    
# Create a thread for Sending CAN messages
sendCan_thread = threading.Thread(target=send_CAN)
sendCan_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits

# Start the CAN thread
sendCan_thread.start()

# Create a thread for receiving CAN messages
recvCan_thread = threading.Thread(target=recv_CAN)
recvCan_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits

# Start the CAN thread
recvCan_thread.start()


# Set a timer thread to stop the entire program after 10 seconds
def stop_program_Timer():
    global TimerExpired
    
    time.sleep(stopTime)  # Wait for 10 seconds
    TimerExpired = True
    
    # Wait for sometime for all the running threads and main program to complete
    time.sleep(0.5)
    
    # Optionally, you can add cleanup or finalization code here before exiting
    
    numInvalid = numChecked - numValid
    logOut = f"\n\nNumber of Frames Sent: {numSent}\tNumber of Frames Recieved: {numRecv}\tNumber of Checks: {numChecked}\t Number of Valid Checks: {numValid}\tNumber of Invalid Checks: {numInvalid}\n\n"
    print(logOut)
    log.write(logOut+"\n")
    log.flush()
    
    log.close()
    #logDbg.close()
    
    print("Unchecked Rx Messages: \n")
    for key, value in unCheckedRx.items():
        print(f"{key - startTime}: {value}")  
    
    print("\nUnchecked Tx Messages: ")
    for key, value in Can_Data_Tx.items():
        dataInt = value["DataInt"]
        print(f"{key - startTime}: {dataInt}")  
    
    # Exit the entire program
    sys.exit(0)

# Create and start the timer thread
timer_thread = threading.Thread(target=stop_program_Timer)
timer_thread.start()


# Main Program
try:      
    while not TimerExpired:            
        
        # begin = time.perf_counter()    #Debug Code to check time to run 1 loop
        
        # Make a copy of the Can_Data to get the available data
        avlDataTx = Can_Data_Tx.copy()
        avlDataRx = Can_Data_Rx.copy()
        
        # Sort the timestamps in ascending order
        timestampsTx = sorted(avlDataTx.keys())
        timestampsRx = sorted(avlDataRx.keys())
        
        timestampsRx = [x for x in timestampsRx if x < max(timestampsTx)]
                         
        for RxTime in timestampsRx:
            Rx_frameId = avlDataRx[RxTime]["frameID"]
            Rx_data = avlDataRx[RxTime]["DataInt"]
            Rx_data_str = ' '.join(['{:02x}'.format(byte) for byte in avlDataRx[RxTime]["data"]])
            
            numChecked += 1
            
            Check_data = [(x - 1)%256 for x in Rx_data]
            MatchFound = False
            
            for TxTime in timestampsTx:
                if avlDataTx[TxTime]["DataInt"] == Check_data:
                    numValid += 1
                    Tx_frameId = avlDataTx[TxTime]["frameID"]
                    Tx_data_str = ' '.join(['{:02x}'.format(byte) for byte in avlDataTx[TxTime]["data"]])
                    Tx_cycleTime = avlDataTx[TxTime]["cycleTime"]
                    logOut = f"Tx Time: {(TxTime - startTime):.6f}\tRx Time: {(RxTime - startTime):.6f}\tTx Cycle Time: {Tx_cycleTime:.6f}\t\tTx Frame ID: {Tx_frameId}\tTx Data: [{Tx_data_str}]\tRx Frame ID: {Rx_frameId}\tRx Data: [{Rx_data_str}]"
                    #print(logOut)
                    log.write(logOut + "\n")
                    log.flush()
                    MatchFound = True
                    Can_Data_Tx.pop(TxTime)
                    break
                
            if(MatchFound == False):
                unCheckedRx.update({RxTime: Rx_data})
            
            Can_Data_Rx.pop(RxTime)         
                                       
        # totTime = time.perf_counter() - begin         #Debug Code to check time to run 1 loop
        # print(f"TotTime: {totTime}")          #Debug Code to check time to run 1 loop
                   
except KeyboardInterrupt:
    
    numInvalid = numChecked - numValid
    logOut = f"\n\nNumber of Frames Sent: {numSent}\tNumber of Frames Recieved: {numRecv}\tNumber of Checks: {numChecked}\t Number of Valid Checks: {numValid}\tNumber of Invalid Checks: {numInvalid}\n\n"
    print(logOut)
    log.write(logOut+"\n")
    log.flush()
    
    log.close()
    sys.exit(1)


# Wait for the CAN thread to finish (if necessary)
sendCan_thread.join()
recvCan_thread.join()

# Close the CAN bus interface
bus.shutdown()