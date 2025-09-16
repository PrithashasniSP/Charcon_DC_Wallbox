import requests

res = requests.get("https://keri7fkpkb32ujueqedomh5gla0pigve.lambda-url.ap-south-1.on.aws/?total_area=25.6&lat=22.9&lon=77.5")

print(res.json())
