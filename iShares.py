import pandas as pd
import requests
from bs4 import BeautifulSoup
import re 

'''  Scrapes data from BlackRock's iShares page '''

def get_iShares_data():
  link_list = [
    'https://www.ishares.com/uk/individual/en/products/307243/ishares-treasury-bond-0-1yr-ucits-etf?switchLocale=y&siteEntryPassthrough=true'
    # 'https://www.ishares.com/uk/individual/en/products/287352/ishares-high-yield-corp-bond-ucits-etf#/'
    # add more in needed
  ]

  for link in link_list: 
    req = requests.get(link).text
    soup = BeautifulSoup(req, 'html.parser')
    
    list_data = {'caption': [], 'data': []} 
    
    # span category
    captions = soup.find_all('span', class_='caption')
    # span value'
    data = soup.find_all('span', class_='data')
    
    # parse and clean table titles and values
    for caption, d in zip(captions, data):
        cleaned_caption = caption.text.strip().replace('\n', ' ').replace('\r', '').replace('   ', ' ')
        cleaned_data = d.text.strip().replace('\n', '').replace('\r', '').replace('   ', ' ')
        list_data['caption'].append(cleaned_caption)
        list_data['data'].append(cleaned_data)


    # find the treasury and cash/derivatives values
    treasury_td = soup.find('td', class_='colIssuePercentage col2 holdings.issuers.issuePercentage')
    if treasury_td:
        us_treasury_value = float(treasury_td.text.strip().replace('%', ''))
        cash_derivatives_value = 100.0 - us_treasury_value
        # append new rows 
        list_data['caption'].extend(['United States Treasury', 'Cash and/or Derivatives'])
        list_data['data'].extend([f'{us_treasury_value}%', f'{cash_derivatives_value}%'])

    df = pd.DataFrame(list_data)
    return df


needed_captions = [
  'Net Assets of Fund', 'Weighted Average YTM', 
  'Weighted Avg Maturity', 'Standard Deviation (3y)',
  'United States Treasury', 'Cash and/or Derivatives'
  ]

def filter_data(df, captions):
    # match the needed captions
    pattern = '|'.join([re.escape(caption) for caption in captions]) 
    mask = df['caption'].str.contains(pattern, case=False, na=False) 
    filtered_df = df[mask]
    return filtered_df
    
    
def filtered_iShares_data(): 
    # grab data 
    data = get_iShares_data()

    # Filter the DataFrame
    filtered_data = filter_data(data, needed_captions)
    print(filtered_data)

      
  
  
  