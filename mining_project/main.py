"""
Data mining Project


Contributors:
Aviad Haviv (rikicodes@gmail.com)
Yossi Golan (yossigolan@gmail.com)

"""

import requests
from bs4 import BeautifulSoup

SITE_URL = "https://coinmarketcap.com/currencies/"


def print_coin_headline(pre_message, post_message, coin_name):
    print("\n", pre_message + ' ' + coin_name + ' ' + post_message)
    print("-"*(len(pre_message) + len(post_message)) + '-' * (len(coin_name) + 1))


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

    print_coin_headline("\nHere is the latest price statistics of", ":", coin_name)

    # Get all divs that contain coin statistics
    try:
        # Get first 4 tables
        price_statistics = soup.find_all('div', class_='sc-16r8icm-0 dxttqv')
        div_counter = 0
        for item in price_statistics:
            coin_info = item.find('table').find('tbody').find_all('tr')
            for row in coin_info:
                table_key = row.contents[0].text
                table_value = row.contents[1].text
                print(table_key, table_value)
            div_counter += 1
            if div_counter == 4:
                break

        print_coin_headline("\nHere is a live data summery of", ":", coin_name)

        # Get updated coin information summary
        coin_text = soup.find('div', class_='sc-16r8icm-0 coDTMj')
        print(coin_text.find('div', class_='sc-16r8icm-0 sc-19zk94m-3 bmiOME').div.div.p.text)

        print_coin_headline("\nWhat is", "?", coin_name)

        # Get 'What is' coin information that includes coin history and all related information.
        for p in coin_text.find('div', class_='sc-16r8icm-0 sc-19zk94m-3 bmiOME').div.div.div.div:
            print(p.text)
    except ConnectionError:
        print(f"Can't read {coin_name} information.")
        print("Please try again later...")


def main():
    pass


if __name__ == '__main__':
    get_coin_info('bitcoin')
