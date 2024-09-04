import pymysql
import conf

# query = """
#         CREATE TABLE IF NOT EXISTS intraday_price(
#         ticker VARCHAR(10),
#         timestamp VARCHAR(50),
#         open REAL,
#         high REAL,
#         low REAL,
#         close REAL,
#         volume INTEGER);"""
def create_table(query):
    try: 
        connection = pymysql.connect( 
                    host='127.0.0.1',
                    user=conf.Dbuser,
                    password=conf.Dbpassword,
                    database='BinanceDB',
                    port= 3306
                )
        cursor = connection.cursor()  
        
        cursor.execute(query)
        print("Table Created")
        connection.commit()
    except pymysql.MySQLError as error:
        print(f"Error: {error}")
    
    finally:
       if connection: 
           cursor.close()
           connection.close()
           print("Połączenie zostało zamknięte.")
           
# create_table(query)

def insert_data(data):
    if data is not None: 
        if not data.empty:
            
            connection = pymysql.connect( 
                        host='127.0.0.1',
                        user=conf.Dbuser,
                        password=conf.Dbpassword,
                        database='BinanceDB',
                        port= 3306
                    )
            cursor = connection.cursor()
            InserQuery = "INSERT INTO intraday_price (ticker,timestamp,open,high,low,close,volume) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            for row in data.itertuples(index=False):
                cursor.execute(InserQuery, (row.ticker, row.timestamp, row.open, row.high, row.low, row.close, row.volume))
                
                
            connection.commit()
        else: 
            print('No new data to insert')
   
        
def get_last_timestamp():
    connection = pymysql.connect( 
                        host='127.0.0.1',
                        user=conf.Dbuser,
                        password=conf.Dbpassword,
                        database='BinanceDB',
                        port= 3306
                    )
    cursor = connection.cursor()
    query= """SELECT MAX(timestamp) FROM intraday_price WHERE ticker = IBM"""
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result
    