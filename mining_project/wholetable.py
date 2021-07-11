import requests
from bs4 import BeautifulSoup
COUNTER = 4

url = requests.get("https://coinmarketcap.com/currencies/bitcoin/")
soup = BeautifulSoup(url.text, 'html.parser')
counter = 0

price_statistics = soup.find_all('div', class_='sc-16r8icm-0 dxttqv')
for div in price_statistics:
    if counter <= COUNTER:
        for table in div:
            try:
                for tr in table.tbody:
                    table_key = tr.th.text
                    table_value = tr.td.text
                    print(table_key, table_value)
            except TypeError:
                print(f'{tr} gives {TypeError}')
                pass
        counter += 1



