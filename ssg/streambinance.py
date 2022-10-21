from ._parser import JsonParser
from .collector import BinaceWebsocket
import asyncio
from asyncio.events import AbstractEventLoop
import colorama
import sys
def main(address ='wss://stream.binance.com:9443/ws/btcgbp@kline_1m',
        parser =JsonParser()
            ):
    config ={'address':address}
    
    if asyncio.get_event_loop().is_closed:
        asyncio.set_event_loop(asyncio.new_event_loop())
    loop: AbstractEventLoop = asyncio.get_event_loop()

    #try:
    #    loop.run_until_complete(
    #                        BinaceWebsocket(**config).open_connection(parser= parser)
    #                          )
    #except KeyboardInterrupt as e:
    #    print(colorama.Fore.RED,'Closing Stream.')
    #    
    #    loop.close()

    try:
        loop.set_debug(False)
        loop.run_until_complete(BinaceWebsocket(**config).open_connection(parser= parser))
    except KeyboardInterrupt as e:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


    
 





if __name__ =='__main__':
    main()
