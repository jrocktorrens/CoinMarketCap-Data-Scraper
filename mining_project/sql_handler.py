import pymysql.cursors

import crypto_info


def run_sql(database, mysql_statement):
    """
    Run sql statement
    :param database: database name
    :param mysql_statement: the sql statement to run
    :return: sql statement output
    """
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database=database,
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(mysql_statement)
            connection.commit()
            return cursor.fetchall()


def setup_coins_table(database, sql_sentence):
    """
    Create the coins table if not exist
    :return: nothing
    """
    run_sql(database, sql_sentence)


def setup_coin_price_today_table(database, sql_sentence):
    """
    Create today's coin price table
    :return: nothing
    """
    run_sql(database, sql_sentence[0])
    run_sql(database, sql_sentence[1])
    run_sql(database, sql_sentence[2])


def setup_coin_price_yesterday_table(database, sql_sentence):
    """
    Create yesterday's coin price table
    :return: nothing
    """
    try:
        run_sql(database, sql_sentence[0])
        run_sql(database, sql_sentence[1])
        run_sql(database, sql_sentence[2])
    except database.IntegrityError as ex:
        print(f"Error {ex}")


def setup_coin_price_history_table(database, sql_sentence):
    """
    Create price history table
    :return: nothing
    """
    run_sql(database, sql_sentence[0])
    run_sql(database, sql_sentence[1])
    run_sql(database, sql_sentence[2])


def setup_coin_information(database, sql_sentence):
    """
    Create coin information table
    :return: nothing
    """
    run_sql(database, sql_sentence[0])
    run_sql(database, sql_sentence[1])
    run_sql(database, sql_sentence[2])


def setup_sql_database(database, sql_sentence):
    """
    Setup sql database if not exist
    and then create all tables
    :return: nothing
    """
    run_sql(None, sql_sentence[0])

    setup_coins_table(database, sql_sentence[1])
    setup_coin_information(database, sql_sentence[2])
    setup_coin_price_today_table(database, sql_sentence[3])
    setup_coin_price_yesterday_table(database, sql_sentence[4])
    setup_coin_price_history_table(database, sql_sentence[5])


def update_coins_table(database, coin_id, coin_name, sql_sentence):
    """
    Insert a record to coins table
    :param sql_sentence: sql sentence to execute
    :param database: the database
    :param coin_id: coin id
    :param coin_name: coin name
    :return: nothing
    """
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database=database,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_sentence, (coin_id, coin_name))
                connection.commit()
                return cursor.fetchall()
    except pymysql.err.IntegrityError:
        # print("Coin Duplicate error!")
        pass


def update_coin_price_today_table(database, current_data, conf, sql_sentence):
    """
    Insert a record to today's coin price table
    :param sql_sentence: sql sentence to execute
    :param database: the database
    :param current_data: data to insert
    :param conf: settings file
    :return: nothing
    """
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database=database,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_sentence, (current_data[conf.table_key.coin_id],
                                              current_data[conf.table_key.today_price],
                                              current_data[conf.table_key.today_price_change],
                                              current_data[conf.table_key.today_low],
                                              current_data[conf.table_key.today_high],
                                              current_data[conf.table_key.today_volume],
                                              current_data[conf.table_key.today_volume_market_cap],
                                              current_data[conf.table_key.today_market_dominance],
                                              current_data[conf.table_key.today_market_cap],
                                              current_data[conf.table_key.today_fully_diluted_market_cap],
                                              current_data[conf.table_key.today_market_rank],
                                              current_data[conf.table_key.today_data_summary]))
                connection.commit()
                return cursor.fetchall()
    except pymysql.err.IntegrityError:
        # print("Coin price today Duplicate error!")
        pass


def update_coin_price_yesterday_table(database, current_data, conf, sql_sentence):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database=database,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_sentence, (current_data[conf.table_key.coin_id],
                                              current_data[conf.table_key.yesterday_low],
                                              current_data[conf.table_key.yesterday_high],
                                              current_data[conf.table_key.yesterday_open],
                                              current_data[conf.table_key.yesterday_close],
                                              current_data[conf.table_key.yesterday_change],
                                              current_data[conf.table_key.yesterday_volume]
                                              ))
                connection.commit()
                return cursor.fetchall()
    except pymysql.err.IntegrityError:
        # print("Coin price yesterday Duplicate error!")
        pass


def update_coin_price_history_table(database, current_data, conf, sql_sentence):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database=database,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_sentence, (current_data[conf.table_key.coin_id],
                                              current_data[conf.table_key.history_7d_low],
                                              current_data[conf.table_key.history_7d_high],
                                              current_data[conf.table_key.history_30d_low],
                                              current_data[conf.table_key.history_30d_high],
                                              current_data[conf.table_key.history_90d_low],
                                              current_data[conf.table_key.history_90d_high],
                                              current_data[conf.table_key.history_52w_low],
                                              current_data[conf.table_key.history_52w_high],
                                              current_data[conf.table_key.history_roi]))
                connection.commit()
                return cursor.fetchall()
    except pymysql.err.IntegrityError:
        # print("Coin price history Duplicate error!")
        pass


def update_coin_information_table(database, current_data, conf, sql_sentence):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database=database,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_sentence, (current_data[conf.table_key.coin_id],
                                              current_data[conf.table_key.coin_about]))
                connection.commit()
                return cursor.fetchall()
    except pymysql.err.IntegrityError:
        # print("Coin information Duplicate error!")
        pass


def update_sql_tables(database, coin_data, conf, sql_sentence):
    """
    Update all Sql tables with all information
    :return: Nothing
    """

    for coin in conf.coins:
        update_coins_table(database, conf.coins[coin], coin, sql_sentence[4])
    update_coin_price_today_table(database, coin_data, conf, sql_sentence[0])
    update_coin_price_yesterday_table(database, coin_data, conf, sql_sentence[1])
    update_coin_price_history_table(database, coin_data, conf, sql_sentence[2])
    update_coin_information_table(database, coin_data, conf, sql_sentence[3])

