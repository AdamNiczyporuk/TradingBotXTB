import pandas as pd 
import requests 
import conf 
import matplotlib.pyplot as plt
import DbManagement 



def intraday_data(ticker,interval='1min'):
    url=f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={interval}&outputsize=full&apikey={conf.DataChartApi}"
    response = requests.get(url)
    data =response.json()
    # print(data)

    time_series =data.get(f'Time Series ({interval})',{})
    if not time_series:
        print(f"No data returned for {ticker}")
        return None
     
    df = pd.DataFrame(time_series).T
    df.index.name='timestamp'
    df.columns=['open','high','low','close','volume']
    df= df.sort_index()
    df.reset_index(inplace=True)
    df['ticker']=ticker
    return df     





def main(): 
    ticker='IBM'
    # latest_timestamp = DbManagement.get_last_timestamp(ticker)
    data = intraday_data(ticker)
    DbManagement.insert_data(data)
    
if __name__ == '__main__':
    main()