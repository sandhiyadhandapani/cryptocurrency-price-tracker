from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime

# Open Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open CoinMarketCap
driver.get("https://coinmarketcap.com/")

# Wait for page to load
time.sleep(10)

# Get all rows
rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

data = []

for row in rows:
    try:
        cols = row.find_elements(By.TAG_NAME, "td")

        if len(cols) < 8:
            continue

        coin_name = cols[2].find_element(By.TAG_NAME, "p").text.strip()

        # Skip non-cryptocurrency index rows
        if "Index" in coin_name or "DTF" in coin_name:
            continue

        price = cols[3].text.strip()
        change_24h = cols[5].text.strip()
        market_cap = cols[7].text.strip()

        data.append([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            coin_name,
            price,
            change_24h,
            market_cap
        ])

        # Stop after Top 10 cryptocurrencies
        if len(data) == 10:
            break

    except Exception:
        continue

# Close browser
driver.quit()

# Create DataFrame
df = pd.DataFrame(
    data,
    columns=[
        "Timestamp",
        "Coin Name",
        "Price (USD)",
        "24h Change",
        "Market Cap"
    ]
)

# Save fresh CSV
df.to_csv("crypto_prices.csv", index=False)

print("\nTop 10 Cryptocurrencies")
print(df)

print("\nCSV File Saved Successfully!")