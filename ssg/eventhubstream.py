import asyncio
from asyncio.events import AbstractEventLoop
import websockets
import colorama
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import json 

async def _JSON(data:dict):
    json_object = json.dumps(data)
    print(json_object)
    return json_object

async def stream_data():
    
    producer = EventHubProducerClient.from_connection_string(
                                conn_str="",
                                eventhub_name="")

    async with websockets.connect('wss://stream.binance.com:9443/ws/btcgbp@kline_1m') as websocket: # create a WS connection to binance API.
        print(colorama.Fore.YELLOW +'ws connection established')
        async with producer: #open azure EH connection.
            print(colorama.Fore.YELLOW +'EH connection established')
            while True:
                event_data_batch = await producer.create_batch()
                print(colorama.Fore.BLUE +'EDB created',flush=True)
                
                data  = await websocket.recv()
                item = await _JSON(data)
                print(colorama.Fore.BLUE +'BTCGB item recieved',flush=True)

                event_data_batch.add(EventData(item)) 
                await producer.send_batch(event_data_batch)
                print(colorama.Fore.GREEN +'Event batch sent!',flush=True)
                
def main():
    if asyncio.get_event_loop().is_closed:
        asyncio.set_event_loop(asyncio.new_event_loop())
        
    loop: AbstractEventLoop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(stream_data())
    except KeyboardInterrupt:
        loop.close()
        print(colorama.Fore.RED,'Loop Ended.')

    
if __name__ == '__main__':
    main()
