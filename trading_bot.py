import requests
import json
import pandas as pd
import numpy as np
import websockets
import asyncio
import tkinter as tk
import conf 
#Konfiguracja API


Id_User = conf.Id_User
password = conf.password

ws_url = "wss://ws.xtb.com/demo"
ws_stream_url = "wss://ws.xtb.com/demoStream"


session_id= None

#logowanie

async def login(ws):
    payload = {
        "command": "login",
        "arguments": {
            "userId": Id_User,
            "password": password
        }
    }
    await ws.send(json.dumps(payload))  # Wysłanie danych do serwera
    response = await ws.recv()  # Odbiór odpowiedzi z serwera
    data = json.loads(response)  # Konwersja odpowiedzi do formatu JSON
    if data['status']:
        print("Login successful!")
        return data["streamSessionId"]
    else:
        print("Login failed!")
        print(data)
        return None

#Balans Konta
async def get_Balance(ws_stream,streamSessionId):
        payload = {
            "command": "getBalance",
	        "streamSessionId": streamSessionId
        }
        await ws_stream.send(json.dumps(payload))  # Wysłanie danych do serwera
        response = await ws_stream.recv()  # Odbiór odpowiedzi z serwera
        data = json.loads(response)  # Konwersja odpowiedzi do formatu JSON
        if data['data']['balance']:
            print(f"Saldo Konta: {data['data']['balance']}")
        else:
            print("Błąd Get_balance")
            print(data)
            return None


# Tick Price
async def get_Tick_Price(ws_stream,streamSessionId):
    symbol = input("Podaj Symbol: ")
    payload={
            "command": "getTickPrices", 
            "streamSessionId": streamSessionId,
            "symbol": symbol,
            "minArrivalTime": 0,
            "maxLevel": 2,
             }
    await ws_stream.send(json.dumps(payload))  # Wysłanie danych do serwera
    response = await ws_stream.recv()  # Odbiór odpowiedzi z serwera
    data = json.loads(response)  # Konwersja odpowiedzi do formatu JSON
    if data['data']:
        print("Cena Tick:")
        for key, value in data['data'].items():
            print(f"{key}: {value}")
    else: 
        print("Błąd Tick_Price")
        print(data)
        return None
async def get_Candles(ws_stream,streamSessionId):
    symbol = input("Podaj Symbol: ")
    payload={
	"command": "getCandles",
	"streamSessionId": streamSessionId,
	"symbol": symbol
             }
    await ws_stream.send(json.dumps(payload))  # Wysłanie danych do serwera
    response = await ws_stream.recv()  # Odbiór odpowiedzi z serwera
    data = json.loads(response)  # Konwersja odpowiedzi do formatu JSON
    if data['data']:
        for key, value in data['data'].items():
            print(f"{key}: {value}")
    else:
        print("failed getting Candles!")
        print(data)
        return None


# def retrieve_input():
#     input_value = entry.get()  # Get the current text in the entry
#     print(f"Input received: {input_value}")


# # Okno Sterowania
# def on_button_click(number):
#     print(f"Wybrano numer: {number}")
#     if number ==1:
#         root.title("Input Example")
#         root = tk.Tk()
#         entry = tk.Entry(root)
#         entry.pack()
#         input_value = entry.get()  
#         submit_button = tk.Button(root, text="Submit", command=get_Tick_Price(ws_stream,stream_session_id,input_value))
#         submit_button.pack()
#         TickPrice =get_Tick_Price()
#         print(f"Cena Tick: {TickPrice}") 
    

    
# root = tk.Tk()
# root.title("Panel Sterowania") 
# buttons_info = {
#     1: "Get Tick Prices",
#     2: "Nazwa 2",
#     3: "Nazwa 3",
#     4: "Nazwa 4",
#     5: "Nazwa 5",
# }


# for number, name in buttons_info.items():
#     button = tk.Button(root, text=name, command=lambda n=number: on_button_click(n))
#     button.pack(side=tk.TOP, padx=50, pady=10)


   
    


async def main():
    async with websockets.connect(ws_url) as ws:
        async with websockets.connect(ws_stream_url) as ws_stream:
            stream_session_id = await login(ws)
            if stream_session_id:
                print(stream_session_id)
                # Pobieranie wszystkich symboli
                await get_Balance(ws_stream,stream_session_id)
                # await get_Tick_Price(ws_stream,stream_session_id)
                await get_Candles(ws_stream,stream_session_id)
            else:
                print("brak SessionID")
            
       
# Uruchomienie głównej funkcji
if __name__ == "__main__":
    asyncio.run(main())
    # root.mainloop()