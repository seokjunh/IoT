from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import serial
import asyncio

app = FastAPI()

connected_websockets = set()

ser = serial.Serial("/dev/ttyUSB0",9600)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)

    try:
        while True:
            value = ser.readline().decode().rstrip()
            values = value.split(',')
            if len(values) == 4:
                val0 = int(values[0])
                val1 = int(values[1])
                val2 = int(values[2])
                val3 = int(values[3])
                response = {}
                if val0 > 20:
                    response["A0"] = val0
                if val1 > 20:
                    response["A1"] = val1
                if val2 > 20:
                    response["A2"] = val2
                if val3 > 20:
                    response["A3"] = val3
                for connected_ws in connected_websockets:
                    await connected_ws.send_json(response)

            await asyncio.sleep(0.1)
    except Exception as e:
        print("Error:", e)
    finally:
        connected_websockets.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    import serial

    ser = serial.Serial("/dev/ttyUSB0", 9600)

    try:
        uvicorn.run(app, host="0.0.0.0", port=8001)
    finally:
        ser.close()