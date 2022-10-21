import asyncio
from asyncio.events import AbstractEventLoop
from datetime import datetime
import websockets
import colorama
from colorama import init
from pathlib import Path

init(autoreset=True)

class BinaceWebsocket:

    def __init__(self,address):
        self.address = address 


    async def open_connection(self,parser):
        await self._stream(self.address,parser)

    @staticmethod
    async def _stream(address,parser):
        async with websockets.connect(address) as websocket: # create a WS connection to binance API.
            print(colorama.Fore.GREEN +'Websocket stream established with Binance.')
            while True:

                data  = await websocket.recv()
                record = parser.parse(path=Path('recorded'),dest ='',data =str(data),filename =timestamp())
                
def timestamp():
     
    #order =['year','hour','minute','second']
    #p represents the smallest time period you want 
    #eval 
    return datetime.utcnow().date().__str__() + 'T'+datetime.utcnow().hour.__str__() 