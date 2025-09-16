import time
import can

def send_can_frame(channel="can0"):
    # Create a CAN bus instance
    bus = can.interface.Bus(channel=channel, bustype='socketcan')

    # Create a CAN message with 8 DLC and an empty payload
    can_frame = can.Message(arbitration_id=0x630, data=[0] * 8, is_extended_id=False)
    print("Transmitting Frame...")

    try:
        while True:
            begin = time.perf_counter()
            
            # Send the CAN frame
            bus.send(can_frame)
            
            # Wait for 100ms
            while ((time.perf_counter() - begin) < 0.1):
                pass

    except KeyboardInterrupt:
        # Clean up when the script is interrupted
        bus.shutdown()

if __name__ == "__main__":
    send_can_frame()