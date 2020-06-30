import requests
import logging
import time
from tkinter import *
from pandas import DataFrame
import matplotlib.pyplot as plt
from var_dump import var_dump
from datetime import datetime
from matplotlib.animation import FuncAnimation


class Checkbar(Frame):

  def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
    Frame.__init__(self, parent)
    self.vars = []
    for pick in picks:
      var = IntVar()
      chk = Checkbutton(self, text=pick, variable=var)
      chk.pack(side=side)
      self.vars.append(var)

  def state(self):
    return map((lambda var: var.get()), self.vars)

app = Tk()

app.title('Crypto Currencies')
app.geometry("500x200")

OPTIONS = {
  'LINK': 'LINK',
  'ETC': 'ETC',
  'EOS': 'EOS',
}

currecies = Checkbar(app, OPTIONS)
currecies.pack()


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

  # var_dump(data)

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
  }

  selected_currencies = list(currecies.state())

  row = 0

  for key, symbol in enumerate(symbols, start=0):

    if selected_currencies[key] == 1:
      prices[symbol['name']] = []

      row = row + 1

      data = fetch_data(symbol['name'])

      for index, item in enumerate(data['Data'], start=0):

        prices[symbol['name']].append(item['volume'])

        if row == 1:
          updatedAt = datetime.fromtimestamp(item['time'])
          item['time'] = updatedAt.strftime("%H:%M")
          prices['Hour'].append(item['time'])
  
  prices = DataFrame(prices)

  plt.cla()

  for key, symbol in enumerate(symbols, start=0):
    if selected_currencies[key] == 1:
      plt.plot( 'Hour', symbol['name'], data=prices, marker='o', markerfacecolor=symbol['markerfacecolor'], markersize=12, color=symbol['color'], linewidth=4)

  plt.legend()

  if i != 0:
    time.sleep(5)


def display_chart():
  plt.style.use('fivethirtyeight')

  plt.rcParams["figure.figsize"] = [16,9]

  figure = plt.gcf()
  figure.canvas.set_window_title('Crypto Currencies')

  ani = FuncAnimation(figure, update_chart, 1000)

  plt.tight_layout()
  plt.show()


button = Button(app, text="Create Chart", command=display_chart)
button.pack()

app.mainloop()