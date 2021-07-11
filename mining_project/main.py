"""
Data mining Project


Contributors:
Aviad Haviv (rikicodes@gmail.com)
Yossi Golan (yossigolan@gmail.com)

"""

import requests
import json
from bs4 import BeautifulSoup
import settings_handler
import sql_handler
from decimal import Decimal
from re import sub

try:
    with open('crypto_settings.json', 'r') as f:
        conf_json = settings_handler.Configuration(json.loads(f.read()))
        f.close()
except Exception as ex:
    print(f"Error reading settings file! {ex}")


conf = settings_handler.Configuration(conf_json)
sql_handler.setup_sql_database()
coin_data = {}


def print_coin_headline(pre_message, post_message, coin_name):
    print("\n", pre_message + ' ' + coin_name + ' ' + post_message)
    print("-" * (len(pre_message) + len(post_message)) + '-' * (len(coin_name) + 1))


def clean_value(value):
    return Decimal(sub(r'[^\d.]', '', value))


def parse_two_words(titles, data):
    table_key = titles[0].lower().strip()
    table_value = data[0].contents[0]
    coin_data[table_key] = clean_value(table_value)
    print(table_key, table_value)
    table_key = titles[1].lower().strip()
    table_value = data[1].contents[0]
    coin_data[table_key] = clean_value(table_value)
    print(table_key, table_value)


def parse_span(row):
    table_key = row.contents[0].text.lower().strip()
    table_value = row.contents[1].find('span').contents[0]
    coin_data[table_key] = clean_value(table_value)
    print(table_key, table_value)


def parse_word(row, coin_name):
    table_key = row.contents[0].text.lower().replace(coin_name.replace('-', ' '), '').strip()
    table_value = row.contents[1].text
    coin_data[table_key] = clean_value(table_value)
    print(table_key, table_value)


def get_coin_information(coin_text):
    coin_data[conf.table_key.today_data_summary] = \
        coin_text.find('div', class_=conf.mining_tag.coin_info_second).div.div.p.text
    print(coin_data[conf.table_key.today_data_summary])


def get_coin_about(coin_text, coin_name):
    print_coin_headline("\nWhat is", "?", coin_name)
    coin_data[conf.table_key.coin_about] = ''
    for about_info in coin_text.find('div', class_=conf.mining_tag.coin_about).div.div.div.div:
        coin_data[conf.table_key.coin_about] += about_info.text + '\n'
        print(about_info.text)


def update_sql_tables():
    sql_handler.update_coin_price_today_table(coin_data, conf)
    sql_handler.update_coin_price_yesterday_table(coin_data, conf)
    for coin in conf.coins:
        sql_handler.update_coins_table(conf.coins[coin], coin)
    sql_handler.update_coin_price_history_table(coin_data, conf)
    sql_handler.update_coin_information_table(coin_data, conf)


def get_coin_info(coin_name):
    """
    Scrap all the information of a crypto coin
    :param coin_name: the name of the coin out of the following list:
    'bitcoin', 'ethereum', 'tether', 'binance-coin', 'cardano', 'dogecoin', 'xrp', 'usd-coin',
    'polkadot-new', 'uniswap', 'litecoin', 'solana', 'theta'
    :return: None. just prints the information to the screen
    """
    if coin_name not in conf.coins:
        raise ValueError(f"Error! Coin {coin_name} is not supported!")

    try:
        r = requests.get(conf.settings.SITE_URL + coin_name + "/")
        soup = BeautifulSoup(r.text, 'html.parser')

        print_coin_headline("\nHere is the latest price statistics of", ":", coin_name)

        # Get all divs that contain coin statistics
        coin_data[conf.table_key.coin_id] = conf.coins[coin_name]
        # Get first 4 tables
        price_statistics = soup.find_all('div', class_=conf.mining_tag.main_div)
        div_counter = 0
        for item in price_statistics:
            coin_info = item.find('table').find('tbody').find_all('tr')
            for row in coin_info:
                table_key = row.contents[0].text.lower().strip()
                split_titles = table_key.split('/')
                two_data = row.contents[1].find_all('div')
                if len(two_data) > 1:
                    parse_two_words(split_titles, two_data)
                elif row.contents[1].find('span') is not None:
                    parse_span(row)
                else:
                    parse_word(row, coin_name)
            div_counter += 1
            if div_counter == 4:
                break

        print_coin_headline("\nHere is a live data summery of", ":", coin_name)

        # Get updated coin information summary
        coin_text = soup.find('div', class_=conf.mining_tag.coin_info_main)
        get_coin_information(coin_text)

        # Get 'What is' coin information that includes coin history and all related information.
        get_coin_about(coin_text, coin_name)
        update_sql_tables()

    except ConnectionError as err:
        print(f"Something on the website went wrong reading {coin_name} information. {err}")
        print("Please try again later...")


def main():
    pass


if __name__ == '__main__':
    get_coin_info('bitcoin')
