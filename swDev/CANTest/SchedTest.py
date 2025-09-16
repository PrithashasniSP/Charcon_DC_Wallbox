import can
import threading
import sched
import time

# Create a CAN bus object for your specific interface (e.g., SocketCAN, virtual, etc.)
# Replace 'socketcan' with your specific interface type and channel (e.g., 'can0')
bus = can.interface.Bus(channel='socketcan0', bustype='socketcan')

# Define your CAN frame data
can_data = [0x01, 0x02, 0x03, 0x04]  # Replace with your actual data

# Create a scheduler
scheduler = sched.scheduler(time.time, time.sleep)

# Function to send CAN messages
def send_can_message():
    # Create a CAN message with your data
    message = can.Message(arbitration_id=0x123, data=can_data, is_extended_id=False)

    # Send the CAN message
    bus.send(message)

    # Reschedule the function to run after 100ms
    scheduler.enter(0.1, 1, send_can_message, ())

# Create a thread for sending CAN messages
can_thread = threading.Thread(target=scheduler.run)

try:
    # Start the CAN thread
    can_thread.start()

    # You can perform other tasks in the main thread concurrently

except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C) to gracefully exit
    pass

# Close the CAN bus when done
bus.shutdown()