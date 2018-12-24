from helpers.ranking import get_data_asynchronous
import asyncio


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous('eq'))
    loop.run_until_complete(future)


main()
