import pandas as pd

file_path = 'data/EUR_USD Historical Data.csv'
df = pd.read_csv(file_path, parse_dates=['time'])


print(df.head())
