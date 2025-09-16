import asyncio
import websockets
import json
import subprocess
import threading
import os
import time


def exeCFunc(inputarg1,inputarg2,inputarg3):
    global exe_starttime
    global exe_endtime 
    global result_obtained
    arg1 = inputarg1.replace(',', ' ')
    arg2 = inputarg2.replace(',', ' ')
    arg3 = inputarg3.replace(',', ' ')
    # Concatenate the strings
    inputargs = f'{arg1} {arg2} {arg3}'
    try:
        elements1 = inputarg1.strip('()').split(',') 
        elements2 = inputarg2.strip('()').split(',') 
        elements3 = inputarg3.strip('()').split(',') 
        formatted_elements1 = [f"'{e.strip()}'" for e in elements1]
        formatted_elements2 = [f"'{e.strip()}'" for e in elements2]     
        formatted_elements3 = [f"'{e.strip()}'" for e in elements3]        
        cmdargs = ','.join(formatted_elements1+formatted_elements2+formatted_elements3)
        split_values = cmdargs.split(',')
        string_list = [value.strip("'") for value in split_values]


        execute_command= ['./MTSolver'] + string_list
        print(execute_command)
        exe_starttime= time.time_ns()
        execute_result = subprocess.run(execute_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        #print("Exe executed successfully")
        exe_endtime=  time.time_ns()
        if execute_result.returncode == 0:
             print("execution successful.")
             print("standard output:")
             print(execute_result.stdout)
             result_obtained= execute_result.stdout
        else:
             print("execution failed with error code:", execute_result.returncode)
             print("standard error:")
             print(execute_result.stderr)
    except Exception as e:
        print("An error occurred:", str(e))
    
latency_dict = {}
# Define a function to handle incoming WebSocket messages
# Define a function to handle incoming WebSocket messages
async def websocket_handler(websocket, path):
    print("Stage 2")

    try:
        connection_time = asyncio.get_event_loop().time()
        latency_dict[id(websocket)] = connection_time
        while True:
            print("Stage 4")
            
            # Wait for messages from the client and await the message
            message = await websocket.recv()
            
            connection_time = latency_dict.get(id(websocket), 0)
            current_time = asyncio.get_event_loop().time()
            latency = current_time - connection_time
            
            
            # Print the received message
            print(f"Received message: {message}")

            try:
                # Attempt to parse the received message as JSON
                received_time= time.time_ns()
                data = json.loads(message)
                jsonformatted_time= time.time_ns()
                # Check if the JSON data contains specific fields
                if "function" in data and "input" in data:
                    function = data["function"]
                    inputs = data["input"]

                    # Process the JSON data based on the action
                    if function == "rba_SrvMT_gauss_rpiv_straight":
                        # Example: Process the data and send a response
                        #response_data = {"result": "Called rba_SrvMT_gauss_rpiv_straight Data processed successfully"}
                        inputarg1 = inputs["arg1"]
                        inputarg2 = inputs["arg2"]
                        inputarg3 = inputs["arg3"]
                        print(f"arg1: {inputarg1}")
                        #createCFunc(function, inputs)
                        exeCFunc(inputarg1,inputarg2,inputarg3)

                        # Read JSON data from the file
                        file_starttime= time.time_ns()
                        # with open("output.json", "r") as file:
                        #     json_data = json.load(file)
                        # Convert the JSON data to a JSON string
                        json_request = result_obtained

                        # Send the JSON response to the client
                        await websocket.send(json_request)
                        #file_endtime=time.time_ns()
                        # OutputpreparationTime = (file_endtime-file_starttime)/pow(10,9)
                        # ExecutionTime = (exe_endtime-exe_starttime)/pow(10,9)
                        # JsonHandlingTime = (jsonformatted_time-received_time)/pow(10,9)
                        # print("Time taken output preparation and send the response to client:" ,OutputpreparationTime, "seconds")
                        # print("Time to execute the result:",ExecutionTime , "seconds")
                        # print("json handling time:" ,JsonHandlingTime, "seconds")
                        # print(f"Latency for message: {latency:.4f} seconds")
                        # totalTime = OutputpreparationTime+ExecutionTime+JsonHandlingTime+latency
                        # print("total time: ", totalTime)

                    else:
                        # Send an "Unknown action" response
                        await websocket.send("Unknown action")

                else:
                    # Send an "Invalid JSON format" response
                    await websocket.send("Invalid JSON format")

            except json.JSONDecodeError:
                # Send an "Invalid JSON format" response
                await websocket.send("Invalid JSON format")

    except websockets.exceptions.ConnectionClosedOK:
        print("WebSocket connection closed")

# Create a WebSocket server
start_server = websockets.serve(websocket_handler, "0.0.0.0", 8765)
print("Starting server")

# Start the WebSocket server in a non-blocking way
asyncio.get_event_loop().run_until_complete(start_server)
print("Stage 3")
# Run the WebSocket server indefinitely
try:
    asyncio.get_event_loop().run_forever()
except Exception as e:
    print(e)
    
    