import  websocket
import ssl
import json

headers = {}
#### have also tried with headers = Authorization : Bearer + token ####

# uri = "wss://localhost:5001/ws"
voltage_data = {
        "voltage": 120,
        "current":20
    }

# Convert dictionary to JSON string
json_data = json.dumps(voltage_data)
# Print the JSON string
print(json_data)

def on_message(ws,msg):
    print(msg)

def on_error(ws,err):
    print(err)

def on_close(ws,close_status_code, close_msg):
    print("Closed")

def on_open(ws):
    ws.send(json_data)


ws = websocket.WebSocketApp("ws://websocket-nlb-c97a21e5ed5384fd.elb.ap-south-1.amazonaws.com/ws",
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})