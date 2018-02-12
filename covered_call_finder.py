from wallstreet import Stock, Call, Put
import numpy as np
from datetime import datetime
import ast 

EXP_LOWER = 5.0 #days
EXP_HIGH = 45.0 #days
VOL_LOWER = 20 #number
MAX_UNDERLYING = 20.0 # Max price per share of the underlying stock
PROFIT_MIN = 5.0 

def get_symbols():
    symbols=[]
    with open('russel2000.txt','r') as f:
        symbols = [line.strip() for line in f]
    return symbols


tickers = ['AMD','F']

with open('Under17.txt','r') as f:
    t_str = f.read()

tickers = ast.literal_eval(t_str)
# tickers = get_symbols()

#This will become the master list of options that fit our criteria. 
candidates = []
tickers_17 = []

for symb in tickers:
    print(symb)

    try:
        call = Call(symb, source='yahoo')
    except Exception as e:
        continue

    c_expires = call.expirations
    c_strikes = call.strikes

    under_price = float(call.underlying.price)

    if under_price>MAX_UNDERLYING:
        continue

    tickers_17.append(symb)

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
            if strike < under_price:
                # We are in the money
                1+1

            else:
                # We are out of the money
                # Ignore for now. 
                continue


            # Assign our call the desired strike.   
            c_iter.set_strike(strike)

            # How far is this option from being OTM? 
            otm_percent = (1 - strike/under_price)*100
            # print(atm_percent)

            volume = c_iter.volume
            last_price = c_iter.price
            last_price = c_iter.bid


            # Calculate extrinsic value -> how much if it expired at the current price. 
            extrinsic = last_price - (under_price-strike)
            profit_potential = extrinsic / under_price * 100

            if profit_potential<PROFIT_MIN:
                continue

            # if the volume is below thres, toss. 
            if volume < VOL_LOWER:
                continue


            print("Found One!  Profit: %.4f percent. Strike: %.2f, Last: %.2f, Under: %.2f, EX: %.2f" %(profit_potential, strike, last_price, under_price, extrinsic))

            # If we get here, we have a candidate. 
            # Create a dictionary with the desired information.
            option = {}
            option['type']          = 'Call'
            option['expiration_dt'] = exp_dt
            option['days']          = dt
            option['symb']          = symb
            option['underlying']    = under_price
            option['last_price']    = c_iter.price
            option['bid']           = c_iter.bid
            option['ask']           = c_iter.ask
            option['volume']        = c_iter.volume
            option['strike']        = c_iter.strike
            option['extrinsic']     = extrinsic
            option['percent']       = profit_potential
            option['otm_percent']   = otm_percent

            candidates.append(option)


#Use this block for saving stock lists. 
# with open('Under20_russel.txt','w') as w:
#     w.write(str(tickers_17))
            
print('\n\n\n\n\n\n\n')

for i in candidates:
    print("Symb: %s Underlying: %.2f Days: %i  Price: %.2f Bid: %.2f Strike: %.1f  Extrinsic: %.2f OTM: %.1f Percent: %.2f" %(i['symb'],i['underlying'],i['days'],i['last_price'],i['bid'],i['strike'],i['extrinsic'],i['otm_percent'],i['percent']))



