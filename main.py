import os

print("=" * 50)
print("      AI TRADING MANAGER")
print("=" * 50)

print("\n1. Downloading latest stock data...")
os.system("py data_collector.py")

print("\n2. Saving data to PostgreSQL...")
os.system("py database/save_stock_data.py")

print("\n3. Running technical analysis...")
os.system("py ai/predictor.py")

print("\n4. Running machine learning prediction...")
os.system("py ai/price_predictor.py")

print("\n" + "=" * 50)
print("AI Trading Manager Finished!")
print("=" * 50) 