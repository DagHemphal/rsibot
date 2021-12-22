
class RSI:
	def __init__(self, ticker, data, period): 
		self.rsi_period = period
		gain = 0.00001
		loss = 0.00001
		for i in range(len(data)-1):
			gain_loss = data[i+1]/data[i]
			if gain_loss > 1:
				gain += gain_loss - 1
			elif gain_loss < 1:
				loss += 1 - gain_loss

		self.first_average_gain = gain/self.rsi_period
		self.first_average_loss = loss/self.rsi_period

	def get_rsi(self, change):
		current_gain = 0
		current_loss = 0

		if change > 1:
			current_gain = change - 1
			current_loss = 0
		elif change < 1:
			current_loss = 1 - change
			current_gain = 0

		average_gain = ((self.first_average_gain * (self.rsi_period-1)) + current_gain)/self.rsi_period
		average_loss = ((self.first_average_loss * (self.rsi_period-1)) + current_loss)/self.rsi_period
		rs = average_gain/average_loss
		rsi = 100 - (100/(1+rs))


		return rsi