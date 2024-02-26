from yahooFinance import filtered_yahoo_data
from iShares import filtered_iShares_data

def main(): 
  trade_volume = filtered_yahoo_data()
  print('--------------------------')
  iShares = filtered_iShares_data()
  
if __name__ == "__main__": 
  main() 