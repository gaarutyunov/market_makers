import os
MAIN = os.path.dirname(os.path.abspath(__file__))
MOEX = 'http://iss.moex.com/iss/securities.json?q='
API = 'https://iss.moex.com/iss/'
DATE = '2018-10-01'
INPUT = os.path.join(MAIN, 'input')
OUTPUT = os.path.join(MAIN, 'output')
STAT = os.path.join(OUTPUT, 'statistics')
GRAPH_PATH = os.path.join(MAIN, 'graphs')

