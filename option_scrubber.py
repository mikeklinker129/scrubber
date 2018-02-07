from wallstreet import Stock, Call, Put
import numpy as np
from datetime import datetime

EXP_LOWER = 30 #days
EXP_HIGH = 180 #days




tickers = ['GOOG','AAPL','SPY']



for symb in tickers:
	print(symb)

	call = Call(symb, source='yahoo')
	c_expires = call.expirations
	c_strikes = call.strikes

	price = call.underlying.price

	#Set the expiration date first
	# Start at least EXP_LOWER and end EXP_HIGH
	now = datetime.now()
	for exp in c_expires:
		exp_dt = datetime.strptime(exp,'%d-%m-%Y')
		dt = (exp_dt-now).total_seconds()/3600/24
		print(exp,dt)
		if EXP_LOWER < dt and dt < EXP_HIGH:
			continue

		# Create the call object
		c_iter = Call(symb, source="yahoo", d=exp_dt.day, m=exp_dt.month, y=exp_dt.year)

		#Now circle through the strikes
		for strike in c_strikes:
			if strike < price:
				continue

			atm_percent = (strike/price-1.0)*100

			# print(atm_percent)


