import pandas as pd 
import pymysql
import requests 
import conf 



def intreaday_data(ticker,interval='1min'):
    url=f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=1min&outputsize=full&apikey={conf.DataChartApi}"
    response = requests.get(url)
    data =response.json()
    print(data)

    time_series =data.get(f'TimeSeries({interval})',{})
    if not time_series:
        print(f"No dataa returned for {ticker}")
        return None 
    df = pd.DataFrame(time_series).T
    df.index.name='timestamp'
    df.columns=['open','high','low','close','volume']
    df.resert_index(inplace=True)
    df= df.sort_index()
    df['ticker']=ticker
    return df     


