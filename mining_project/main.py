"""
Data mining Project


Contributors:
Aviad Haviv (rikicodes@gmail.com)
Yossi Golan (yossigolan@gmail.com)

"""

import requests
from bs4 import BeautifulSoup

SITE_URL = "https://coinmarketcap.com/currencies/"


def get_coin_info(coin_name):
    """
    Scrap all the information of a crypto coin
    :param coin_name: the name of the coin out of the following list:
    'bitcoin', 'ethereum', 'tether', 'binance-coin', 'cardano', 'dogecoin', 'xrp', 'usd-coin',
    'polkadot-new', 'uniswap', 'litecoin', 'solana', 'theta'
    :return: None. just prints the information to the screen
    """
    if coin_name not in ['bitcoin', 'ethereum', 'tether', 'binance-coin', 'cardano',
                         'dogecoin', 'xrp', 'usd-coin', 'polkadot-new', 'uniswap', 'litecoin',
                         'solana', 'theta']:
        raise ValueError(f"Error! Coin {coin_name} is not supported!")

    try:
        r = requests.get(SITE_URL + coin_name + "/")
        soup = BeautifulSoup(r.text, 'html.parser')
    except ConnectionError:
        print(f"Something on the website went wrong reading {coin_name} information.")
        print("Please try again later...")

    print("\n", f"Here is the latest price statistics of {coin_name}:")
    print(f"---------------------------------------" + '-' * (len(coin_name) + 1))

    # Get all divs that contain coin statistics
    try:
        price_statistics = soup.find_all('div', class_='sc-16r8icm-0 dxttqv')
        div_counter = 0
        for div in price_statistics:
            # Get first 4 tables
            if div_counter <= 4:
                for table in div:
                    for tr in table.tbody:
                        table_key = tr.th.text
                        table_value = tr.td.text
                        print(table_key, table_value)
                div_counter += 1

        print("\n", f"Here is a live data summery of {coin_name}:")
        print(f"-------------------------------------" + '-' * (len(coin_name) + 1))

        # Get updated coin information summary
        coin_text = soup.find('div', class_='sc-16r8icm-0 coDTMj')
        print(coin_text.find('div', class_='about___1OuKY').div.div.p.text)

        print("\n", f"What is {coin_name}?")
        print(f"--------------" + '-' * (len(coin_name) + 1))

        # Get 'What is' coin information that includes coin history and all related information.
        for p in coin_text.find('div', class_='about___1OuKY').div.div.div.div:
            print(p.text)
    except ConnectionError:
        print(f"Can't read {coin_name} information.")
        print("Please try again later...")


if __name__ == '__main__':
    get_coin_info('bitcoin')
