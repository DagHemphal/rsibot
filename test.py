import yfinance as yf
import datetime 
start = datetime.datetime(2020, 12, 18)
print(start)
end = start + datetime.timedelta(days=1)
print(end)
data = yf.download(tickers="TSLA", 
			start=start.strftime("%Y-%m-%d"), 
			end=end.strftime("%Y-%m-%d"), 
			interval="1m")

print(data)