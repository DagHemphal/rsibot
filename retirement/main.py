import avanza
import numpy as np
import random
import time
import atexit

# Q-learning variables
ALPHA = 0.5
GAMMA = 0.3
EPSILON = 0.03

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
			self.initial_price = price
			self.log = []
			self.log.append({action, price})
		elif action == 2 and self.shares > 0: #sell
			self.capital += (self.shares * price) * 0.9975
			self.shares = 0
			self.log.append({action, price})

	def print(self, price):
		print("bitcoins: " + str(self.shares))
		print("cash: $" + str(self.capital))
		print("portfolio: $" + str(self.shares * price + self.capital))
		print(portfolio.log)
		print("")

portfolio = portfolio(10000, 0, first_price)

#reward system
def reward(state, action):
	cash = portfolio.capital
	shares = portfolio.shares
	init_price = portfolio.initial_price
	if action == 0: #buy
		if cash > 0:
			return 1 - (state + 10)/200
	elif action == 2: #sell
		if shares > 0:
			return (state - 10)/200 
	elif action == 1:
		return ((state - 10)/200) * 0.9
	return -1
		
# Initialize q-table values to 0
state_size = 200
action_size = 3
#Q = np.zeros((state_size, action_size))
Q = np.load('test.pkl.npy')

old_state = 100

def exit_handler():
	np.save('test.pkl', Q)
	np.savetxt("foo.csv", Q, delimiter=",")
	print(portfolio.log)

atexit.register(exit_handler)
portfolio.print(old_state)

while True:
	time.sleep(3)
	stock = avanza.Ticker(1002234)
	last_price = stock.last_price
	print ("bitcoin price: " + str(last_price))
	init_price = portfolio.initial_price
	state = int(((last_price/init_price) - 0.9) * 1000)
	print(state)

	if random.uniform(0, 1) < EPSILON:
		action = random.randint(0, 2)
		print("random action: " + str(action))
	else:
		action = np.argmax(Q[int(state), :])
		print("best action: " + str(action))

	r = reward(state, action)
	# Update q values
	Q[old_state, action] = Q[old_state, action] + ALPHA * (r + GAMMA * np.max(Q[state, :]) - Q[old_state, action])

	print (r)
	portfolio.action(action)
	portfolio.print(last_price)
	old_state = state
