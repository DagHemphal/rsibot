import avanza
from rsi import RSI
from portfolio import Portfolio
import matplotlib.pyplot as plt

ticket = "BTC-USD"
wallet = Portfolio(10000, {})

rsi_stock = RSI(ticket, "20d")

rsi_bottom = 20
rsi_top = 90

a = []
prices = []
buy = False
sell = False
bought_x = []
bought_y = []
sold_x = []
sold_y = []

plt.ion()
fig, (axs1, axs2) = plt.subplots(2, sharex=True)
fig.suptitle('price for ' + ticket)
index = 0
while True:
	index += 1
	stock = avanza.Ticker(1002234)
	price = stock.last_price
	change = stock.change_percent

	rsi = rsi_stock.get_rsi(change)

	if rsi < rsi_bottom:
		buy = True
	elif ticket not in wallet.stocks and buy and rsi > rsi_bottom:
		wallet.buy_all(ticket, price)
		wallet.print()
		if ticket in wallet.stocks:
			bought_y.append(price)
			bought_x.append(index)
			axs1.plot(bought_x, bought_y, "og")
		buy = False
	if rsi > rsi_top:
		sell = True
	elif ticket in wallet.stocks and sell and rsi < rsi_top:
		wallet.sell_all(ticket, price)
		wallet.print()
		if ticket not in wallet.stocks:
			sold_y.append(price)
			sold_x.append(index)
			axs1.plot(sold_x, sold_y, "or")
		sell = False

	prices.append(price)
	a.append(rsi)
	
	axs1.plot(prices, "b")
	axs2.plot(a,"b")

	fig.tight_layout()
	plt.pause(5)
