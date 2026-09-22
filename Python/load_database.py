import pandas as pd
import sqlite3

df = pd.read_csv('Data\\retail_price.csv')  

conn = sqlite3.connect('pricing_analytics.db')

df.to_sql('retail_price', conn, if_exists='replace', index=False)

print("Data Loaded Successfully into SQLite Database.")

conn.close()