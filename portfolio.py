class Portfolio:
	def __init__(self, capital, stocks): 
		""" Inits a Portfolio object """
		self.start_capital = capital
		self.capital = capital
		self.stocks = stocks #{"tsla": {"buy_price": 500, "shares": 10}, "pltr": {"buy_price": 10, "share": 200}}
		self.transactions = []
		self.profit = 1
		'''
		{"tsl": 
			{"time": "",
			"action": "sold",
			"amount": 100,
			"price": 560
			}
		}
		'''

	def buy_all(self, ticket, price):
		if self.capital > 0:
			amount = (self.capital * 0.9975)/price
			self.action([ticket, amount], price, 0)
	def sell_all(self, ticket, price):
		if ticket in self.stocks:
			self.action([ticket, self.stocks[ticket]["shares"]], price, 2)


	#todo add courtage
	def action(self, share, price, action): #share ["tsla", 10]
		cost = price * share[1] * 1.0025
		if share[1] == 0:
			print("Cant buy/sell 0 shares")
			return
		if action == 0 and self.capital >= cost: #buy
			new_share = share[1]
			if share[0] in self.stocks:
				new_share += self.stocks[share[0]]["shares"]
				
			self.stocks[share[0]] = {"buy_price": cost/share[1], "shares":  new_share}
			self.stocks[share[0]] = self.stocks[share[0]]
			self.capital -= cost
			#self.transactions.append({})
		elif action == 2 and share[0] in self.stocks  and self.stocks[share[0]]["shares"] >= share[1]: #sell
			self.capital += (share[1] * price) * 0.9975
			self.stocks[share[0]]["shares"] -= share[1]
			self.profit = self.capital/self.start_capital
			if self.stocks[share[0]]["shares"] == 0:
				del self.stocks[share[0]]
			#self.transactions.append({})
		else:
			print(action)
			print(share)
			print(self.stocks)
			print("Error not enough capital or dont own stock")
			
	def print(self):
		print("cash: $" + str(self.capital))

		for stock in self.stocks:
			if self.stocks[stock]:
				print(stock + ": " + str(self.stocks[stock]["shares"]))

		#print("portfolio: $" + str(self.shares * price + self.capital))

		#print(self.transactions)
		print("")