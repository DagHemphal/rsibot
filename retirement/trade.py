import avanza
import time

stock = avanza.Ticker(1002234)
first_price = stock.last_price

class portfolio:
	def __init__(self, capital, shares, initial_price): 
		""" Inits a Portfolio object """
		#todo add multiple shares
		self.capital = capital
		self.shares = shares
		self.initial_price = initial_price
		self.log = []

	#todo add courtage
	def action(self, action):
		stock = avanza.Ticker(1002234)
		price = stock.last_price
		if action == 0 and self.capital > 0: #buy
			self.shares += (self.capital * 0.9975)/price  
			self.capital = 0
			self.log = []
			self.log.append({action, price})
		elif action == 2 and self.shares > 0: #sell
			self.capital += (self.shares * price) * 0.9975
			self.shares = 0
			self.log.append({action, price})
		self.initial_price = price

	def print(self, price):
		print("bitcoins: " + str(self.shares))
		print("cash: $" + str(self.capital))
		print("portfolio: $" + str(self.shares * price + self.capital))
		print(portfolio.log)
		print("")

portfolio = portfolio(10000, 0, first_price)

while True:
	time.sleep(3)
	stock = avanza.Ticker(1002234)
	price = stock.last_price

	init_price = portfolio.initial_price
	capital = portfolio.capital
	shares = portfolio.shares

	print ("bitcoin price: " + str(price))
	print ("bitcoin change: " + str(price/init_price))


	if capital > 0:
		if price/init_price < 0.995:
			portfolio.action(0)
		elif price/init_price >= 1.01:
			portfolio.action(0)
	elif shares > 0:
		if price/init_price > 1.005:
			portfolio.action(2)
		elif price/init_price < 0.99:
			portfolio.action(2)


	portfolio.print(price)
