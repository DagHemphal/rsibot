#import avanza
import yfinance as yf
import datetime
from rsi import RSI
from portfolio import Portfolio
import matplotlib.pyplot as plt
import tkinter as tk
import pandas as pd

def tradebot(gui):
	#convert to datetime
	ticker = gui.ticker.get()
	wallet = gui.wallet
	stopprofit = float(gui.stopprofit.get())
	stoploss = float(gui.stoploss.get())
	stock = yf.Ticker(ticker)

	a = []
	prices = []
	dates = []
	buy = False
	sell = False
	bought_x = []
	bought_y = []
	sold_x = []
	sold_y = []

	profit = []

	rsi_period = int(gui.rsi_period.get())

	rsi_top = int(gui.rsi_top.get())
	rsi_bottom = int(gui.rsi_bot.get())

	trade_days = int(gui.trade_days.get())

	start_date = (datetime.datetime.strptime(gui.start_date.get(), "%Y-%m-%d")) - (datetime.timedelta(days=rsi_period)) #get period
	end_date = datetime.datetime.strptime(gui.start_date.get(), "%Y-%m-%d")

	day_index = 0

	for i in range(trade_days):
		hist = stock.history(start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
		rsi_stock = RSI(ticker, hist["Close"], rsi_period)

		start_date += datetime.timedelta(days=1)
		end_date += datetime.timedelta(days=1)

		data = yf.download(tickers=ticker, 
			start=end_date.strftime("%Y-%m-%d"), 
			end=(end_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d"), 
			interval="1m")

		

		changes = []
		# Print the data
		if data.empty:
			continue
		open_price = data["Open"][0]
		for date, price in data.iterrows():
			change = price["Open"]/open_price
			date = date.strftime("%H-%M")

			rsi = rsi_stock.get_rsi(change)
			changes.append(change)
			if not buy and ticker not in wallet.stocks and rsi < rsi_bottom:
				buy = True
			elif buy and ticker not in wallet.stocks and rsi > rsi_bottom:
				buy = False
				wallet.buy_all(ticker, price["Open"])
				wallet.print()
				if ticker in wallet.stocks:
					bought_y.append(price)
					bought_x.append(date)
			elif not sell and ticker in wallet.stocks and rsi > rsi_top:
				sell = True
			elif sell and ticker in wallet.stocks and rsi < rsi_top:
				sell = False
				wallet.sell_all(ticker, price["Open"])
				wallet.print()
				if ticker not in wallet.stocks:
					sold_y.append(price["Open"])
					sold_x.append(date)
			#stopProfit
			elif ticker in wallet.stocks and price/wallet.stocks[ticker]["buy_price"] >= stopprofit:
				print("sell profit")
				wallet.sell_all(ticker, price["Open"])
				wallet.print()
				if ticker not in wallet.stocks:
					sold_y.append(price["Open"])
					sold_x.append(date)
			#stopploss
			elif ticker in wallet.stocks and price/wallet.stocks[ticker]["buy_price"] <= stoploss:
				print("sell loss")
				wallet.sell_all(ticker, price["Open"])
				wallet.print()
				if ticker not in wallet.stocks:
					sold_y.append(price["Open"])
					sold_x.append(date)
				
			prices.append(price["Open"])
			dates.append(date)
			profit.append(wallet.profit)
			a.append(rsi)
	gui.axs1.clear()
	gui.axs2.clear()
	gui.axs3.clear()
	gui.axs1.plot(dates, prices, "b")
	gui.axs2.plot(dates, a,"b")
	gui.axs1.plot(sold_x, sold_y, "or")
	gui.axs1.plot(bought_x, bought_y, "og")

	if (profit[len(profit) - 1] >= 1):
		gui.axs3.plot(dates, profit, "g")
	else:
		gui.axs3.plot(dates, profit, "r")
	plt.draw()

	wallet.print()
	gui.balance_content.set("Balance: $" + str(round(wallet.capital, 4)))
