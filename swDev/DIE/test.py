from datetime import datetime
 
current_time = datetime.now()
print("Current time:", current_time)
 
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
Date = current_time.strftime("%Y-%m-%d")
Hour = current_time.strftime("%H")
print("Formatted time:", formatted_time)
print("Date:", Date)
print("Hour:", Hour)