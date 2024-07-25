import pandas as pd

original_file_path = '/home/anthony/Downloads/EURUSD=X (1).csv'

fixed_file_path = 'data/fixed_EUR_USD_Historical_Data.csv'

df = pd.read_csv(original_file_path)

print(df.head())

df.to_csv(fixed_file_path, index=False)  

print(f"Data saved to {fixed_file_path}")
