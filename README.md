# Binance ALTrader
 
Primary idea was to scan all alt coins and buy volume spikes on low 
timeframes when higher timeframes RSI still isn't oversold.
Advantage of Binance is that it's API limits are virtually non-existent.

Note: the bot is designed mainly for trading alt coins in btc parings,
there are less USDT pairings and they tend to follow btc a lot

## quickstart

install the required packages via
    
    pip install -r requirements

run 

    python <one of below>
#### balances.py

quick balances tool, on running it prints assets and balances of binance wallet
 with a possibility of diplaying charts   
it is convenient to use from terminal using an alias to monitor live performance

#### main.py

main strategy loop
  
- algo looks for Money Flow Index bounces in an uptrend

- trader gets to see the chart and decides manually whether wants to buy

- if btc in uptrend - trade btc pairings, hold btc

- if btc is falling - trade usdt pairings, hold tether

#### confluence.py
    
I got an idea that is inspired by a very succesful forex trader.
He mentioned that he only entered once there is confluence among all
timeframes. This tries that.
    
The trend is told in one of the two: 
- pct chg since candle open  
- price over moving averages

#### sell_all.py 
tool to get rid of all assets in case of emergency
    
## some ideas and initial changelog 
consider fibonacci an awesome strategy, peaks from codewars

add volume param and whenever volume is significantly higher on 1 min -
trigger a buy signal
(lets say average of the day for the given interval)

v1.1
-
- purpose is to automate the process of finding and executing buys among altcoins
- added script to display currently held assets
- before entering now the chart can be analysed and based on that, 
a choice is made
- atm support only for btc pairings

v1.2
- 
- new strategy that checks whether a given condition is satisfied among
 all timeframes
- idea: that strategy can also be used along with another oscillator-based strategy
- introduced a bit of utility in form of a tool for checking balances and 
instantly selling all currently held assets
