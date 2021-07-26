import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dfKS200 = pd.read_csv('./kospi200_20090601_20090710.csv', header=0, encoding= 'unicode_escape',
                      names=['일자', '종가', '대비', '등락율','시가', '고가', '저가', '거래량', '거래대금', '상장시가총액'], index_col='일자')
print(dfKS200['종가'].describe())

plt.hist(dfKS200['종가'], density=True, alpha=0.5)
print(dfKS200['등락율'].describe())

dfKS200['log_return'] = np.log(dfKS200['종가']) - np.log(dfKS200['종가'].shift(1))
print(dfKS200.log_return.describe())

r = (1+dfKS200.log_return.describe()['mean']) ** 27
K = 426.36 * r
spot_price = 426.36
# Short put
strike_price_short_put = spot_price * r
premium_short_put = 9.60
# Short call
strike_price_short_call = strike_price_short_put
premium_short_call = 7.81
# Stock price range at expiration of the put
sT = np.arange(300, 500, 1)

def short_call_payoff(sT, strike_price, premium):
    return np.where(sT > strike_price, strike_price - sT, 0) + premium

payoff_short_call = short_call_payoff (sT, strike_price_short_call, premium_short_call)
fig, ax = plt.subplots()
ax.spines['top'].set_visible(False) # Top border removed
ax.spines['right'].set_visible(False) # Right border removed
ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center
ax.plot(sT, payoff_short_call,label='Short Call',color='r')
plt.xlabel('Stock Price')
plt.ylabel('Profit and loss')
plt.legend()
plt.show()

def short_put_payoff(sT, strike_price, premium):
    return np.where(sT < strike_price, sT - strike_price, 0) + premium

payoff_short_put = short_put_payoff(sT, strike_price_short_put, premium_short_put)
# Plot
fig, ax = plt.subplots()
ax.spines['top'].set_visible(False) # Top border removed
ax.spines['right'].set_visible(False) # Right border removed
ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center
ax.plot(sT,payoff_short_put,label='Short Put',color='g')
plt.xlabel('Stock Price')
plt.ylabel('Profit and loss')
plt.legend()
plt.show()

payoff_straddle = payoff_short_call + payoff_short_put

print (f'Max Profit: {payoff_straddle.max()}')
print ("Max Loss:", "Unlimited")
# Plot
fig, ax = plt.subplots()
ax.spines['top'].set_visible(False) # Top border removed
ax.spines['right'].set_visible(False) # Right border removed
ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center

ax.plot(sT,payoff_short_call,'--',label='Short Call',color='r')
ax.plot(sT,payoff_short_put,'--',label='Short Put',color='g')

ax.plot(sT,payoff_straddle,label='Straddle')
plt.xlabel('Stock Price', ha='left')
plt.ylabel('Profit and loss')
plt.legend()
plt.show()


