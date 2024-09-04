import conf 
from binance import Client 
import pandas as pd 
import matplotlib.pyplot as plt


client = Client(conf.Test_api_key_biance,conf.Test_secret_key_biance,testnet=True)


data = client.get_account() #Sporawdzenie Konta
#Przekształcanie danych z Api do DataFarme
balances_df=pd.DataFrame(data['balances'])
print(balances_df)
#balances_df.to_csv('dane.csv',index=False)

#dataStream przez websocekt ale na razie nie 

symbol="BTCUSDT"
interval="1m"
lookback="30"

# klinesTable=pd.DataFrame(client.get_historical_klines('BTCUSDT','1m','1 day ago UTC'))
# print(klinesTable)


def getMinuteData(symbol,interval,lookback): 
    frame = pd.DataFrame(client.get_historical_klines(symbol,interval,lookback+' min ago UTC'))
    frame= frame.iloc[:,:6]
    frame.columns=['Time','Open','High','Low','Close','Volume']
    frame=frame.set_index('Time')
    frame.index=pd.to_datetime(frame.index ,unit='ms')
    frame.index = frame.index + pd.to_timedelta(2, unit='h') # Ustawiamy czas na Polski
    frame =frame.astype(float) # wszystko jest stringiem więc zamieniamy na floata do działań
    return frame

test = getMinuteData(symbol,interval,lookback)
#test.Open.plot()


#Strategy 
#but if asset fell by more then 0.2% withnt the las 30 min 
# sell if asset rises by more than 0.15% or falls furhter by 0.15 %



def strategyTest(symbol,qty,entried=False): 
    df = getMinuteData(symbol,'1m','15')
    cumulret = (df.Open.pct_change()+1).cumprod()-1
    print("Cumulative Return:\n", cumulret)
    if not entried: 
        if cumulret.iloc[-1] < -0.002:
            order = client.create_order(symbol=symbol,side='BUY',type='MARKET',quantity=qty)
            print(order)
            entried=True
        else: 
            print("Nie było Trade")
    if entried:
        while True: 
            df = getMinuteData(symbol,'1m','15')
            sinceBuy= df.loc[df.index > pd.to_datetime(order['transactTime'],unit='ms')]
            if len(sinceBuy) > 0:
                sinceBuyRet = cumulret = (sinceBuy.Open.pct_change()+1).cumprod()-1
                if sinceBuyRet.iloc[-1] > 0.0015 or sinceBuyRet[-1] < -0.0015:
                    order = client.create_order(symbol=symbol,side='SELL',type='MARKET',quantity=qty)
                    print(order)
                    break
                
strategyTest('BTCUSDT',0.03)