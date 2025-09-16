from Signals import OCPP_Signals
import websocket
import ssl
import json
import time
 
CloseReq = False
 

 
 
def on_close(ws, close_status_code, close_msg):
    global CloseReq
    print("OCPP Client Closed")
    CloseReq = False
 
def on_open(ws):
    global CloseReq
    print("Connected to OCPP Client")
    previous_time = time.perf_counter()
    try:
        while(not CloseReq):
            if(time.perf_counter() > previous_time + 10):
                #print("10s has elapsed!!!")
                
                # Convert dictionary to JSON string
                json_data = json.dumps(OCPP_Signals)
                
                print(f"OCPP data: {OCPP_Signals}")
                print(f"json data: {json_data}")
                ws.send(json_data)
                previous_time=time.perf_counter()
    except Exception as e:
        #print(e)
        ws.close()
 
def closeWebsocket(ws):
    global CloseReq
    CloseReq = True
    ws.close()
 
def websocket_establishement():
    ws = websocket.WebSocketApp("ws://websocket-nlb-c97a21e5ed5384fd.elb.ap-south-1.amazonaws.com/ws",
                            on_open=on_open,
                            on_close=on_close)
    return ws
 
def ws_start(ws):
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})