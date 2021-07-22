"""
Handle the user command line interface
"""

import argparse
import crypto_info


def general(attribute):
    """
    Print general type value
    :param attribute: attribute to print
    :return: value for print
    """
    if attribute not in crypto_info.conf.attribute_general:
        print(f"{crypto_info.conf.error_msg.err_arguments} ({attribute})")
        exit(0)
    return crypto_info.coin_data[crypto_info.conf.attribute_general[attribute]]


def today(attribute):
    """
    Print today type value
    :param attribute: attribute to print
    :return: value for print
    """
    if attribute not in crypto_info.conf.attribute_today:
        print(f"{crypto_info.conf.error_msg.err_arguments} ({attribute})")
        exit(0)
    return crypto_info.conf.today_value_sign[attribute] + str(
        crypto_info.coin_data[crypto_info.conf.attribute_today[attribute]])


def yesterday(attribute):
    """
    Print yesterday type value
    :param attribute: attribute to print
    :return: value for print
    """
    if attribute not in crypto_info.conf.attribute_yesterday:
        print(f"{crypto_info.conf.error_msg.err_arguments} ({attribute})")
        exit(0)
    return crypto_info.conf.yesterday_value_sign[attribute] + str(
        crypto_info.coin_data[crypto_info.conf.attribute_yesterday[attribute]])


def history(attribute):
    """
    Print history type value
    :param attribute: attribute to print
    :return: value for print
    """
    if attribute not in crypto_info.conf.attribute_history:
        print(f"{crypto_info.conf.error_msg.err_arguments} ({attribute})")
        exit(0)
    return crypto_info.conf.history_value_sign[attribute] + str(
        crypto_info.coin_data[crypto_info.conf.attribute_history[attribute]])


def main():
    """
    Get user command line parameters
    :return: nothing
    """
    cmp_scraping = argparse.ArgumentParser()
    cmp_scraping.add_argument('coin_name', type=str, metavar='<coin_name>',
                              help='in which coin are you interested?', )
    cmp_scraping.add_argument('type', type=str, metavar='<data type>', help='specify the table you are looking for '
                                                                            'from the options:',
                              choices=['general', 'today', 'yesterday', 'history'])
    cmp_scraping.add_argument('attribute', type=str, metavar='<attribute>', help='wanted attribute to be shown')

    args = cmp_scraping.parse_args()

    coin_name = str(args.coin_name)
    types = str(args.type)
    attribute = str(args.attribute)

    crypto_info.get_coin_info(coin_name)

    type_map = {'general': general,
                'today': today,
                'yesterday': yesterday,
                'history': history}

    print(f"{coin_name} {types} {attribute}: {type_map[types](attribute)}")


if __name__ == "__main__":
    main()
