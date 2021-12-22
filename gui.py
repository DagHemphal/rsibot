import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from rsitest import tradebot
from portfolio import Portfolio

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.edit_view = tk.Canvas(self, width = 600, height = 200)
		self.edit_view.pack()

		self.trade_bt = tk.Button(self)
		self.trade_bt["text"] = "Start trading"
		self.trade_bt["command"] = self.trade

		self.balance_content = tk.StringVar(self, value="Balance: $10000")
		self.balance_label = tk.Label(self, textvariable=self.balance_content)

		#input
		self.start_date = tk.Entry(self, textvariable=tk.StringVar(self, '2021-10-01'))
		self.rsi_period = tk.Entry(self, textvariable=tk.StringVar(self, 14))
		self.rsi_top = tk.Entry(self, textvariable=tk.StringVar(self, 70))
		self.rsi_bot = tk.Entry(self, textvariable=tk.StringVar(self, 30))
		self.trade_days = tk.Entry(self, textvariable=tk.StringVar(self, 7))
		self.ticker = tk.Entry(self, textvariable=tk.StringVar(self, "BTC-USD"))
		self.stopprofit = tk.Entry(self, textvariable=tk.StringVar(self, 1.04))
		self.stoploss = tk.Entry(self, textvariable=tk.StringVar(self, 0.99))

		#input labels
		self.start_label = tk.Label(self, textvariable=tk.StringVar(self, value="Start date: "))
		self.rsi_period_label = tk.Label(self, textvariable=tk.StringVar(self, value="Rsi period: "))
		self.rsi_top_label = tk.Label(self, textvariable=tk.StringVar(self, value="Rsi top: "))
		self.rsi_bot_label = tk.Label(self, textvariable=tk.StringVar(self, value="Rsi bot: "))
		self.trade_days_label = tk.Label(self, textvariable=tk.StringVar(self, value="Trade days: "))
		self.ticker_label = tk.Label(self, textvariable=tk.StringVar(self, value="Ticker: "))
		self.stopprofit_label  = tk.Label(self, textvariable=tk.StringVar(self, value="Stop profit: "))
		self.stoploss_label  = tk.Label(self, textvariable=tk.StringVar(self, value="Stop loss: "))

		#place labels
		self.edit_view.create_window(50, 20, window=self.balance_label)

		self.edit_view.create_window(200, 30, window=self.start_label)
		self.edit_view.create_window(200, 60, window=self.rsi_period_label)
		self.edit_view.create_window(200, 90, window=self.rsi_top_label)
		self.edit_view.create_window(200, 120, window=self.rsi_bot_label)
		self.edit_view.create_window(200, 150, window=self.trade_days_label)
		self.edit_view.create_window(200, 180, window=self.ticker_label)

		self.edit_view.create_window(400, 30, window=self.stopprofit_label)
		self.edit_view.create_window(400, 60, window=self.stoploss_label)


		#place entrys
		self.edit_view.create_window(300, 30, window=self.start_date)
		self.edit_view.create_window(300, 60, window=self.rsi_period)
		self.edit_view.create_window(300, 90, window=self.rsi_top)
		self.edit_view.create_window(300, 120, window=self.rsi_bot)
		self.edit_view.create_window(300, 150, window=self.trade_days)
		self.edit_view.create_window(300, 180, window=self.ticker)

		self.edit_view.create_window(500, 30, window=self.stopprofit)
		self.edit_view.create_window(500, 60, window=self.stoploss)



		#place button
		self.edit_view.create_window(550, 120, window=self.trade_bt)
		
		self.fig, (self.axs1, self.axs2, self.axs3) = plt.subplots(3)
		self.fig.suptitle('price for ' + self.ticker.get())
		self.plot = FigureCanvasTkAgg(self.fig, self)
		self.plot.get_tk_widget().pack()
		self.plot.draw()   
	

	def trade(self):
		self.wallet = Portfolio(10000, {})
		self.fig.suptitle('price for ' + self.ticker.get())
		print("Starting to trade!")
		tradebot(self)

if __name__ == "__main__":
	root = tk.Tk()
	app = Application(master=root)
	app.mainloop()