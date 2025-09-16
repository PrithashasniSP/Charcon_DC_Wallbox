import requests
from datetime import datetime

print("Requesting Solar Data")

current_time = datetime.now()
Date = current_time.strftime("%Y-%m-%d")

res = requests.get(f"https://keri7fkpkb32ujueqedomh5gla0pigve.lambda-url.ap-south-1.on.aws/?total_area=25.6&lat=22.9&lon=77.5&date={Date}")

print(res.json())
