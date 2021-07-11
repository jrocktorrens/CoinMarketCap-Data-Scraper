import argparse


def is_coin_exist(coin_name):
    result = main_file.sql_exist(coin_name)  #True\False
    return result


def information(coin_name, attribute):
    return main_file.sql_information(coin_name, attribute)


def general(coin_name, attribute):
    return main_file.sql_general(coin_name, attribute)


def today(coin_name, attribute):
    attribute_list = ['price', 'price_change', 'low', 'high', 'volume', 'volume_market_cap',
                      'market_dominance', 'market_cap', 'fully_diluted_market_cap', 'rank', 'data_summery']
    if attribute not in attribute_list:
        raise Exception(f'{attribute} not in the list of options')
    return main_file.sql_online(coin_name, attribute)


def yesterday(coin_name, attribute):
    attribute_list = ['price', 'low', 'high', 'open', 'close', 'change', 'volume']
    if attribute not in attribute_list:
        raise Exception(f'{attribute} not in the list of options')
    return main_file.sql_yesterday(coin_name, attribute)


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
                              choices=['general', 'online', 'yesterday', 'history'])
    cmp_scraping.add_argument('attribute', type=str, metavar='<attribute>', help='wanted attribute to be shown')
    # cmp_scraping.add_argument('-w', help='display good morning message', action='store_true')

    args = cmp_scraping.parse_args()

    coin_name = str(args.coin_name)
    tables = str(args.table)
    attribute = str(args.attribute)
    # if args.w:
    #     print('good morning :)')

    if not is_coin_exist(coin_name):
        raise Exception(f'{coin_name} is not in a valid coin in coin market cap')

    table_map = {'information': information,
                 'general': general,
                 'today': today,
                 'yesterday': yesterday,
                 'history': history}

    print(table_map[tables](coin_name, attribute))


if __name__ == "__main__":
    main()
