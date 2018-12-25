from helpers.ranking import *
import asyncio


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous('ofz2'))
    loop.run_until_complete(future)


programs = ['bbo', 'eq', 'ofz1', 'ofz2']


for x in programs:
    create_graph(x)
