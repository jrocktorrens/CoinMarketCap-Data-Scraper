"""
Data mining Project


"""

import requests
from bs4 import BeautifulSoup


r = requests.get("https://coinmarketcap.com/currencies/Bitcoin/")

soup = BeautifulSoup(r.text,'html.parser')
# price_statistics = soup.find('div', class_='sc-16r8icm-0 dxttqv')
# for tr in price_statistics.table.tbody:
#     table_key = tr.th.text
#     table_value = tr.td.text
#     print(table_key, table_value)
# print(price_statistics.prettify())

price_statistics = soup.find_all('div', class_='sc-16r8icm-0 dxttqv')
div_counter = 0
for div in price_statistics:
    if div_counter <= 4:
        for table in div:
            for tr in table.tbody:
                table_key = tr.th.text
                table_value = tr.td.text
                print(table_key, table_value)
        div_counter += 1
coin_text = soup.find('div', class_='sc-16r8icm-0 coDTMj')
print(coin_text.find('div', class_='about___1OuKY').div.div.p.text)

for p in coin_text.find('div', class_='about___1OuKY').div.div.div.div:
    print(p.text)
#print(coin_text.find('div', class_='about___1OuKY').div.div.div.div.p.text)

"""
article = soup.find('div', class='article')
print(article)
headline = article.h2.a.text
print(headline)
summary = article.p.text
print(summary)

for article in soup.find('div', class='article')
    headline = article.h2.a.text
    print(headline)
    summary = article.p.text
    print(summary)
"""