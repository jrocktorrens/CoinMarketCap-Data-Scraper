import argparse
import crypto_info


def is_coin_exist(coin_name):
    result = coin_name in crypto_info.conf.coins  #True\False
    return result


def information(coin_name, attribute):
    return main_file.sql_information(coin_name, attribute)


def general(coin_name, attribute):
    return main_file.sql_general(coin_name, attribute)


def today(attribute):
    if attribute not in crypto_info.conf.attribute[1:11]:
        raise Exception(f'{attribute} not in the list of options')
    return crypto_info.conf.attribute[attribute]
#
def yesterday(coin_name, attribute):
    attribute_list = ['price', 'low', 'high', 'open', 'close', 'change', 'volume']
    if attribute not in attribute_list:
        raise Exception(f'{attribute} not in the list of options')
    # return conf.value_sign.{attribute} + coin_data[conf.table_key.attribute]


def history(coin_name, attribute):
    attribute_list = ['7d_low', '7d_high', '30d_low', '30d_high', '90d_low', '90d_high', '52w_low', '52w_high',
                      'all_time_low', 'all_time_high', 'roi', 'circulating_supply', 'total_supply', 'max_supply']
    if attribute not in attribute_list:
        raise Exception(f'{attribute} not in the list of options')
    return main_file.sql_yesterday(coin_name, attribute)


def main():
    cmp_scraping = argparse.ArgumentParser()
    cmp_scraping.add_argument('coin_name', type=str, metavar='<coin_name>',
                              help='in which coin are you interested?', )
    cmp_scraping.add_argument('table', type=str, metavar='<data table>', help='specify the table you are looking for '
                                                                              'from the options:',
                              choices=['general', 'today', 'yesterday', 'history'])
    cmp_scraping.add_argument('attribute', type=str, metavar='<attribute>', help='wanted attribute to be shown')
    # cmp_scraping.add_argument('-w', help='display good morning message', action='store_true')

    args = cmp_scraping.parse_args()

    coin_name = str(args.coin_name)
    tables = str(args.table)
    attribute = str(args.attribute)
    # if args.w:
    #     print('good morning :)')

    # if not is_coin_exist(coin_name):
    #     raise Exception(f'{coin_name} is not in a valid coin in coin market cap')

    crypto_info.get_coin_info(coin_name)

    table_map = {'information': information,
                 'general': general,
                 'today': today,
                 'yesterday': yesterday,
                 'history': history}

    print(table_map[tables](attribute))


if __name__ == "__main__":
    main()
