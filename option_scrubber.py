from wallstreet import Stock, Call, Put
import numpy as np
from datetime import datetime

EXP_LOWER = 30.0 #days
EXP_HIGH = 200.0 #days
PRICE_MAX = 1.0 # dollars per share
VOL_LOWER = 100 #number




tickers = ['SPY']

#This will become the master list of options that fit our criteria. 
candidates = []

for symb in tickers:
	print(symb)

	# call = Call(symb, source='yahoo')
	call = Call(symb, source="google")
	c_expires = call.expirations
	c_strikes = call.strikes

	under_price = float(call.underlying.price)

	#Set the expiration date first
	# Start at least EXP_LOWER and end EXP_HIGH
	now = datetime.now()
	for exp in c_expires:

		#Make a date-time object for the expiration date. 
		exp_dt = datetime.strptime(exp,'%d-%m-%Y')

		# Determine how far into the future (in day) the option expires
		dt = (exp_dt-now).total_seconds()/3600/24

		# If this expiration date is too soon or too far away, move on. 
		if EXP_LOWER > dt:
			continue
		if EXP_HIGH < dt:
			continue



		print(exp)
		# Create the call object for this desired expiration date. 
		c_iter = Call(symb, source="yahoo", d=exp_dt.day, m=exp_dt.month, y=exp_dt.year)

		#Now circle through the strikes.
		c_strikes = c_iter.strikes
		for strike in c_strikes:


			# If this call is in the money, we arent interested. 
			if strike < under_price:
				continue

			if strike % 1 != 0:
				continue	

			print(strike)

			# Assign our call the desired strike. 	
			c_iter.set_strike(strike)

			# How far is this option from being ATM? 
			atm_percent = (strike/under_price-1.0)*100
			# print(atm_percent)

			volume = c_iter.volume
			last_price = c_iter.price

			# if the volume is below thres, toss. 
			if volume < VOL_LOWER:
				continue

			# If the price is above our thres, toss. 
			if last_price > PRICE_MAX:
				continue

			print("Found One!")

			# If we get here, we have a candidate. 
			# Create a dictionary with the desired information.
			option = {}
			option['type']			= 'Call'
			option['expiration_dt']	= exp_dt
			option['symb']			= symb
			option['underlying']	= under_price
			option['last_price']	= last_price
			option['volume']		= volume
			option['atm_percent']	= atm_percent
			option['strike']		= strike

			candidates.append(option)

			break

	# Same process but for puts. 
	put = Put(sumb, source='yahoo')
	p_expires = put.expirations
	print("PUTS")
	under_price = float(put.underlying.price)

	now = datetime.now()
	for exp in p_expires:

		#Make a date-time object for the expiration date. 
		exp_dt = datetime.strptime(exp,'%d-%m-%Y')

		# Determine how far into the future (in day) the option expires
		dt = (exp_dt-now).total_seconds()/3600/24

		# If this expiration date is too soon or too far away, move on.  
		if EXP_LOWER < dt and dt < EXP_HIGH:
			continue

		print(exp)

		# Create the put object for this desired expiration date. 
		p_iter = Put(symb, source="yahoo", d=exp_dt.day, m=exp_dt.month, y=exp_dt.year)

		#Now circle through the strikes.
		p_strikes = p_iter.strikes
		for strike in p_strikes:

			# If this put is in the money, we arent interested. 
			if strike > under_price:
				continue

			# Assign our putl the desired strike. 	
			p_iter.set_strike(strike)

			# How far is this option from being ATM? 
			# Positive is negative price movement here. 
			atm_percent = -(strike/under_price-1.0)*100
			# print(atm_percent)

			volume = c_iter.volume
			last_price = c_iter.price

			# if the volume is below thres, toss. 
			if volume < VOL_LOWER:
				continue

			# If the price is above our thres, toss. 
			if last_price > PRICE_MAX:
				continue

			# If we get here, we have a candidate. 
			# Create a dictionary with the desired information.
			option = {}
			option['type']			= 'Put'
			option['expiration_dt']	= exp_dt
			option['symb']			= symb
			option['underlying']	= under_price
			option['last_price']	= last_price
			option['volume']		= volume
			option['atm_percent']	= atm_percent
			option['strike']		= strike

			candidates.append(option)

