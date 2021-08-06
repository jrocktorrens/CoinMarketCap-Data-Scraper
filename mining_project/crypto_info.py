"""
Data mining Project


Contributors:
Aviad Haviv (rikicodes@gmail.com)
Yossi Golan (yossigolan@gmail.com)

"""
import decimal
import logging
import requests
import json
import google

import urllib3.exceptions
from bs4 import BeautifulSoup
import settings_handler
import sql_handler
from decimal import Decimal
from re import sub

# coin_data is a global variable to store coin data
coin_data = {}
# conf is a global variable of the configuration file
conf = None


def init_program():
    """
    function for initializing program:
    load settings file
    create sql tables
    :return: nothing
    """
    logging.basicConfig(filename="crypto.log", level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Initializing program...')
    global conf
    try:
        with open('crypto_settings.json', 'r') as f:
            conf_json = settings_handler.Configuration(json.loads(f.read()))
            f.close()
            conf = settings_handler.Configuration(conf_json)
    except FileNotFoundError as ex:
        logging.error('Settings file was not found!')
        print(f"Error! Can't find settings file! \n{ex}")
        exit(0)

    sql_handler.setup_sql_database(conf.sql.database, [conf.sql_create.cypto_database,
                                                       conf.sql_create.coins_table,
                                                       conf.sql_create.coin_information_table,
                                                       conf.sql_create.coin_price_today_table,
                                                       conf.sql_create.coin_price_yesterday_table,
                                                       conf.sql_create.coin_price_history_table,
                                                       conf.sql_create.coin_google_table
                                                       ])


def print_coin_headline(pre_message, post_message, coin_name):
    """
    Prints a headline with an underline
    :param pre_message: first part of message
    :param post_message: last part of message
    :param coin_name: coin name
    :return: nothing
    """
    print("\n", pre_message + ' ' + coin_name + ' ' + post_message)
    print("-" * (len(pre_message) + len(post_message)) + '-' * (len(coin_name) + 1))


def clean_value(value):
    """
    Remove $ and % signs from values
    :param value: the original value
    :return: the value after cleaning
    """
    try:
        new_value = Decimal(sub(r'[^\d.]', '', value))
        return new_value
    except (ValueError, TypeError, decimal.InvalidOperation):
        logging.debug('Cleaning process failed')
        return None


def parse_two_words(titles, data):
    """
    Parse data with two words and get two keys with related values
    :param titles: the Keys
    :param data: the values
    :return: nothing
    """
    table_key = titles[0].lower().strip()
    table_value = data[0].contents[0]
    coin_data[table_key] = clean_value(table_value)
    # print(table_key, table_value)
    table_key = titles[1].lower().strip()
    table_value = data[1].contents[0]
    coin_data[table_key] = clean_value(table_value)
    # print(table_key, table_value)


def parse_span(row):
    """
    Parse data with span and get only first data
    :param row: row of information
    :return: nothing
    """
    table_key = row.contents[0].text.lower().strip()
    table_value = row.contents[1].find('span').contents[0]
    coin_data[table_key] = clean_value(table_value)
    # print(table_key, table_value)


def parse_word(row, coin_name):
    """
    Parse one key with one value
    :param row: row of informationdatabase
    :param coin_name: coin name
    :return: nothing
    """
    table_key = row.contents[0].text.lower().replace(coin_name.replace('-', ' '), '').strip()
    table_value = row.contents[1].text
    coin_data[table_key] = clean_value(table_value)
    # print(table_key, table_value)


def get_coin_information(coin_text):
    """
    Get coin summery for today
    :param coin_text: coin html
    :return: nothing
    """
    coin_data[conf.table_key.today_data_summary] = \
        coin_text.find('div', class_=conf.mining_tag.coin_info_second).div.div.p.text
    # print(coin_data[conf.table_key.today_data_summary])


def get_coin_about(coin_text):
    """
    Get the 'About coin' information
    :param coin_text: coin html
    :return: nothing
    """
    # print_coin_headline("\nWhat is", "?", coin_name)
    coin_data[conf.table_key.coin_about] = ''
    coin_text = coin_text.find('div', class_=conf.mining_tag.coin_about).div
    for paragraph in coin_text.find_all('p'):
        coin_data[conf.table_key.coin_about] += paragraph.text + '\n\n '
        # print(about_info.text)


def get_coin_price_data(soup, coin_name):
    """
    Get price data (today, yesterday, history)
    :param soup: soup html
    :param coin_name: name of coin
    :return: nothing
    """
    logging.info('Coin price processing begins...')

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


def get_coin_info(coin_name):
    """
    Scrap all the information of a crypto coin
    :param coin_name: the name of the coin out of the following list:
    'bitcoin', 'ethereum', 'tether', 'binance-coin', 'cardano', 'dogecoin', 'xrp', 'usd-coin',
    'polkadot-new', 'uniswap', 'litecoin', 'solana', 'theta'
    :return: None. just prints the information to the screen
    """
    if coin_name not in conf.coins:
        print(conf.error_msg.err_coin_not_supported + f" ({coin_name})")
        exit(0)

    try:
        r = requests.get(conf.settings.SITE_URL + coin_name + "/")
        soup = BeautifulSoup(r.text, 'html.parser')
        # Get coin price data
        get_coin_price_data(soup, coin_name)

        # Get updated coin information summary
        coin_text = soup.find('div', class_=conf.mining_tag.coin_info_main)
        get_coin_information(coin_text)

        # Get 'What is' coin information that includes coin history and all related information.
        get_coin_about(coin_text)

        # Get google information
        coin_data[conf.table_key.google_popularity], \
            coin_data[conf.table_key.google_sites] = \
            google.search_google(coin_name,
                                 conf.google.akp_yek,
                                 conf.google.search_engine_id)

        # Update sql tables with new information
        sql_handler.update_sql_tables(conf.sql.database,
                                      coin_data,
                                      conf,
                                      [conf.sql_update.coin_price_today_table,
                                       conf.sql_update.coin_price_yesterday_table,
                                       conf.sql_update.coin_price_history_table,
                                       conf.sql_update.coin_information_table,
                                       conf.sql_update.coin_google_table,
                                       conf.sql_update.coin_table])
        logging.info('Coin price processing finished...')
    except ConnectionError as err:
        logging.error('Coin price processing Connection error')
        print(conf.error_msg.err_web_connection + f"\n({err})")
    except urllib3.exceptions.NewConnectionError as err:
        logging.error('Coin price processing Connection issue...')
        print(conf.error_msg.err_web_connection + f"\n({err})")
