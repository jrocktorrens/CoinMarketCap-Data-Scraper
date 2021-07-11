import argparse
import crypto_info


def general(attribute):
    if attribute not in crypto_info.conf.attribute_general:
        raise Exception(f'{attribute} not in the list of options')
    return crypto_info.coin_data[crypto_info.conf.attribute_general[attribute]]


def today(attribute):
    if attribute not in crypto_info.conf.attribute_today:
        raise Exception(f'{attribute} not in the list of options')
    return crypto_info.coin_data[crypto_info.conf.attribute_today[attribute]]


def yesterday(attribute):
    if attribute not in crypto_info.conf.attribute_yesterday:
        raise Exception(f'{attribute} not in the list of options')
    return crypto_info.coin_data[crypto_info.conf.attribute_yesterday[attribute]]


def history(attribute):
    if attribute not in crypto_info.conf.attribute_history:
        raise Exception(f'{attribute} not in the list of options')
    return crypto_info.coin_data[crypto_info.conf.attribute_history[attribute]]


def main():
    cmp_scraping = argparse.ArgumentParser()
    cmp_scraping.add_argument('coin_name', type=str, metavar='<coin_name>',
                              help='in which coin are you interested?', )
    cmp_scraping.add_argument('table', type=str, metavar='<data table>', help='specify the table you are looking for '
                                                                              'from the options:',
                              choices=['general', 'today', 'yesterday', 'history'])
    cmp_scraping.add_argument('attribute', type=str, metavar='<attribute>', help='wanted attribute to be shown')


    args = cmp_scraping.parse_args()

    coin_name = str(args.coin_name)
    tables = str(args.table)
    attribute = str(args.attribute)

    crypto_info.get_coin_info(coin_name)

    table_map = {'general': general,
                 'today': today,
                 'yesterday': yesterday,
                 'history': history}

    print(table_map[tables](attribute))


if __name__ == "__main__":
    main()
