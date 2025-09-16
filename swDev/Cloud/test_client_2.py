import websocket
import ssl
import json
import time

voltage_data = {
    "voltage": 120,
    "current": 20
}
 
 
# Convert dictionary to JSON string
json_data = json.dumps(voltage_data)
 
def on_message(ws, msg):
    print(msg)
 
def on_error(ws, err):
    print(err)
 
def on_close(ws, close_status_code, close_msg):
    print("Closed")
 
def on_open(ws):
    print("Connected")
    previous_time = time.perf_counter()
    try:
        while(True):
            if(time.perf_counter() > previous_time + 10):
                print("10s has elapsed!!!")
                ws.send(json_data)
                previous_time=time.perf_counter()
    except Exception as e:
        print(e)
 

ws = websocket.WebSocketApp("ws://websocket-nlb-c97a21e5ed5384fd.elb.ap-south-1.amazonaws.com/ws",
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
