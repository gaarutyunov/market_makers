import requests
from main import MOEX
example = '2-01-00206-A'


def get_data(code):
    cd = str(code)
    r = requests.get(MOEX + cd)
    json = r.json()
    data = json['securities']['data']
    return data[0]


def get_code(data):
    code = data[1]
    return code


def get_board(data):
    board = data[-1]
    return board


def get_engine(data):
    engine = data[-3].split('_')[0]
    return engine


def get_market(data):
    market = data[-3].split('_')[1]
    return market
