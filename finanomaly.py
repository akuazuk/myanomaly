from google.oauth2.service_account import Credentials
import gspread
import json 
import pandas as pd
from datetime import datetime, timezone, timedelta
import datetime
from datetime import date

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file('credentials_t.json', scopes=scopes)

gc = gspread.authorize(credentials)

sh = gc.open("Stock_Finance")


class Anomaly:
    
    def __init__ (self, company):
        
        self.company = company
        
    def stock (self):
        
        for i in self.company:
            
            df = pd.DataFrame(sh.worksheet(i).get('A2:1000'))
            df.columns = ['timestamp', 'value']
            df["timestamp"] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            pd.to_datetime(pd.Series(df['timestamp'], dtype = 'int32'), format="%Y-%m-%dT%H:%M:%SZ")
            df["value"]=df["value"].str.replace(',','.').astype(float)
            df["timestamp"]=df["timestamp"].str.replace('13:00:00','16:00:00')
            
            df2 = df.to_dict('records')
            dict = {"period": 24, "series": df2 }

            with open('{}.json'.format(i), 'w', encoding='utf-8') as jsonf:
                json.dump(dict, jsonf)

#company = ["DJI", "AAPL", "NFLX", "META", "GOOG", "AMZN", "SP500", "NASDAQ"]
#fin_files = Anomaly(company)
#fin_files.stock()
