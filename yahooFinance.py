import yfinance as yf 
import datetime

''' Scrapes historical IB01 data from Yahoo Finance '''

def get_yahoo_data():
  ib01 = yf.Ticker('IB01.L')

  # all historical data
  history = ib01.history(period='6mo')

  # we only need Date, Close and Volume
  filtered_history = history[['Close', 'Volume']] 
  filtered_final = filtered_history.reset_index()

  # cast to numeric types 
  filtered_final['Close'] = filtered_final['Close'].astype(float)
  filtered_final['Volume'] = filtered_final['Volume'].astype(int)

  # find average trading volume over the period 
  filtered_final['Daily_Trading_Volume'] = filtered_final['Close'] * filtered_final['Volume']

  average_trading_volume = filtered_final['Daily_Trading_Volume'].mean()

  # save history backup for needed cols 
  current_date = datetime.datetime.now().strftime("%Y-%m-%d")
  filtered_final.to_csv(f'data/ib01_data_{current_date}.csv', index=False)

  return average_trading_volume

def filtered_yahoo_data():
  
  trade_volume = get_yahoo_data()
  avg_volume = round(trade_volume, 2)
  avg_volume = ('{:,}'.format(avg_volume))
  
  print(f"Average trading volume over the lsat 6 months: ${avg_volume}")
  return avg_volume




