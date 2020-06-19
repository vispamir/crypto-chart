import requests
import logging
import time
import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from var_dump import var_dump
from datetime import datetime
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')


def fetch_data(symbol):
  # api-endpoint 
  URL = "https://min-api.cryptocompare.com/data/exchange/histohour"

  # defining a params dict for the parameters to be sent to the API 
  PARAMS = {
    'tsym': symbol,
    'limit': 10,
    'api_key': '1e97a81afd70b50e88ed1d8eea0a4a92f1ef8f771885e2a1e215054b32f847d1'
  }

  try:
      import http.client as http_client
  except ImportError:
      # Python 2
      import httplib as http_client
  http_client.HTTPConnection.debuglevel = 1

  # You must initialize logging, otherwise you'll not see debug output.
  # logging.basicConfig()
  # logging.getLogger().setLevel(logging.DEBUG)
  # requests_log = logging.getLogger("requests.packages.urllib3")
  # requests_log.setLevel(logging.DEBUG)
  # requests_log.propagate = True

  # sending get request and saving the response as response object 
  r = requests.get(url = URL, params = PARAMS) 

  # extracting data in json format 
  data = r.json()

  var_dump(data)

  return data 

def update_chart(i):

  symbols = [
    {
      'name': 'LINK', 
      'color': 'skyblue',
      'markerfacecolor': 'blue',
    },
    {
      'name': 'ETC', 
      'color': 'plum',
      'markerfacecolor': 'purple',
    },
    {
      'name': 'EOS', 
      'color': 'moccasin',
      'markerfacecolor': 'darkorange',
    },
  ]

  prices = {
    'Hour': [],
    'LINK': [],
    'ETC': [],
    'EOS': [],
  }

  for key, symbol in enumerate(symbols, start=0):
    data = fetch_data(symbol['name'])
    for index, item in enumerate(data['Data'], start=0):

      prices[symbol['name']].append(item['volume'])

      if key == 0:
        updatedAt = datetime.fromtimestamp(item['time'])
        item['time'] = updatedAt.strftime("%H:%M")
        prices['Hour'].append(item['time'])


  # var_dump(prices)

  prices = DataFrame(prices)


  plt.cla()

  for symbol in symbols:
    plt.plot( 'Hour', symbol['name'], data=prices, marker='o', markerfacecolor=symbol['markerfacecolor'], markersize=12, color=symbol['color'], linewidth=4)

  plt.legend()

  time.sleep(5)



ani = FuncAnimation(plt.gcf(), update_chart, 1000)


plt.tight_layout()
plt.show()

# root = tk.Tk()

# OPTIONS = [
#   "Jan",
#   "Feb",
#   "Mar"
# ] #etc

# variable = tk.StringVar(root)
# variable.set(OPTIONS[0]) # default value

# w = tk.OptionMenu(root, variable, *OPTIONS)
# w.pack()

# def ok():
#     print ("value is:" + variable.get())

# button = tk.Button(root, text="OK", command=ok)
# button.pack()

# root.mainloop()
