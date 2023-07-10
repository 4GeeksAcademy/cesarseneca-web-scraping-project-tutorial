# your app code here
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

html_data = requests.get(" https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue").text

soup = BeautifulSoup(html_data, "html.parser")
tables = soup.find_all("table")
for table in tables:
    if "Tesla Quarterly Revenue" in table.text:
        revenue_table = table
        break
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in revenue_table.find_all("tr"):
    columns = row.find_all("td")
    if columns != [] :
        date = columns[0].text
        revenue = columns[1].text.replace(",", "").replace("$", "")
        tesla_revenue = tesla_revenue.append({"Date": date, "Revenue": revenue}, ignore_index=True)

tesla_revenue = tesla_revenue.loc[tesla_revenue['Revenue'] != ""]
tesla_revenue.reset_index(drop=True, inplace=True)

data = list(tesla_revenue.itertuples(index=False, name=None))

conn = sqlite3.connect('Tesla.db')

c = conn.cursor() 

c.execute('DROP TABLE IF EXISTS tesla_revenue')

c.execute('''
    CREATE TABLE IF NOT EXISTS tesla_revenue (
        Date TEXT,
        Revenue INTEGER
    )
''')
c.executemany('''
    INSERT INTO tesla_revenue (Date, Revenue)
    VALUES (?, ?)
''', data)

conn.commit()

dates = tesla_revenue["Date"]
revenue = tesla_revenue["Revenue"]
dates = dates[::-1]
revenue = revenue[::-1]
plt.figure(figsize=(14, 11))
plt.plot(dates, revenue)
plt.title("Tesla Quarterly Revenue")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.xticks(rotation=90)
plt.savefig("tesla.png")