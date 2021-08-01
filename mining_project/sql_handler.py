import logging

import pymysql.cursors


def cast(val, to_type, default=None):
    """
    Safely cast variable to a type
    :param val: value
    :param to_type: type to cast to
    :param default: default value if cast fails
    :return: casted value
    """
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


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


def setup_table(database, sql_sentence):
    """
    Create a table in not exist
    :param database: database name
    :param sql_sentence: the sql sentence
    :return: nothing
    """
    try:
        if isinstance(sql_sentence, list):
            run_sql(database, sql_sentence[0])
            run_sql(database, sql_sentence[1])
            run_sql(database, sql_sentence[2])

        else:
            run_sql(database, sql_sentence)
    except database.IntegrityError as ex:
        print(f"Error {ex}")


def setup_sql_database(database, sql_sentence):
    """
    Setup sql database if not exist
    and then create all tables
    :return: nothing
    """
    logging.info('Setting UP Database')
    # Create database in not exist
    run_sql(None, sql_sentence[0])

    logging.info('Setting UP Tables')

    # Setup coins table
    setup_table(database, sql_sentence[1])
    # Setup coin_information table
    setup_table(database, sql_sentence[2])
    # Setup coin_price_today table
    setup_table(database, sql_sentence[3])
    # Setup coin_price_yesterday table
    setup_table(database, sql_sentence[4])
    # Setup coin_price_history table
    setup_table(database, sql_sentence[5])
    # Setup coin_google table
    setup_table(database, sql_sentence[6])


def update_coins_table(database, coin_id, coin_name, sql_sentence):
    """
    Insert a record to coins table
    :param database: the database
    :param coin_id: coin id
    :param coin_name: coin name
    :param sql_sentence: sql sentence to execute
    :return: nothing
    """
    logging.info('Updating coins table')

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
        logging.debug('duplicate record at coins table')
        # print("Coin Duplicate error!")
        pass


def update_coin_price_today_table(database, current_data, conf, sql_sentence):
    """
    Insert a record to today's coin price table
    :param database: the database
    :param current_data: data to insert
    :param conf: settings file
    :param sql_sentence: sql sentence to execute
    :return: nothing
    """
    logging.info('Updating price_today table')
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database=database,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_sentence, (current_data[conf.table_key.coin_id],
                                              cast(current_data[conf.table_key.today_price], float),
                                              cast(current_data[conf.table_key.today_price_change], float),
                                              cast(current_data[conf.table_key.today_low], float),
                                              cast(current_data[conf.table_key.today_high], float),
                                              cast(current_data[conf.table_key.today_volume], float),
                                              cast(current_data[conf.table_key.today_volume_market_cap], float),
                                              cast(current_data[conf.table_key.today_market_dominance], float),
                                              cast(current_data[conf.table_key.today_market_cap], float),
                                              cast(current_data[conf.table_key.today_fully_diluted_market_cap], float),
                                              cast(current_data[conf.table_key.today_market_rank], float),
                                              current_data[conf.table_key.today_data_summary]))
                connection.commit()
                return cursor.fetchall()
    except pymysql.err.IntegrityError:
        logging.debug('duplicate record at price_today table')
        # print("Coin price today Duplicate error!")
        pass


def update_coin_price_yesterday_table(database, current_data, conf, sql_sentence):
    """
    Insert a record to yesterday's coin price table
    :param database: the database
    :param current_data: data to insert
    :param conf: settings file
    :param sql_sentence: sql sentence to execute
    :return: nothing
    """
    logging.info('Updating yesterday price table')

    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database=database,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_sentence, (current_data[conf.table_key.coin_id],
                                              cast(current_data[conf.table_key.yesterday_low], float),
                                              cast(current_data[conf.table_key.yesterday_high], float),
                                              cast(current_data[conf.table_key.yesterday_open], float),
                                              cast(current_data[conf.table_key.yesterday_close], float),
                                              cast(current_data[conf.table_key.yesterday_change], float),
                                              cast(current_data[conf.table_key.yesterday_volume], float)
                                              ))
                connection.commit()
                return cursor.fetchall()
    except pymysql.err.IntegrityError:
        logging.debug('duplicate record at yesterday price table')
        # print("Coin price yesterday Duplicate error!")
        pass


def update_coin_price_history_table(database, current_data, conf, sql_sentence):
    """
    Insert a record to coin's history price table
    :param database: the database
    :param current_data: data to insert
    :param conf: settings file
    :param sql_sentence: sql sentence to execute
    :return: nothing
    """
    logging.info('Updating price history table')

    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database=database,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_sentence, (current_data[conf.table_key.coin_id],
                                              cast(current_data[conf.table_key.history_7d_low], float),
                                              cast(current_data[conf.table_key.history_7d_high], float),
                                              cast(current_data[conf.table_key.history_30d_low], float),
                                              cast(current_data[conf.table_key.history_30d_high], float),
                                              cast(current_data[conf.table_key.history_90d_low], float),
                                              cast(current_data[conf.table_key.history_90d_high], float),
                                              cast(current_data[conf.table_key.history_52w_low], float),
                                              cast(current_data[conf.table_key.history_52w_high], float),
                                              cast(current_data[conf.table_key.history_roi], float)))
                connection.commit()
                return cursor.fetchall()
    except pymysql.err.IntegrityError:
        logging.debug('duplicate record at price history table')
        # print("Coin price history Duplicate error!")
        pass


def update_coin_information_table(database, current_data, conf, sql_sentence):
    """
    Insert a record to coin's information table
    :param database: the database
    :param current_data: data to insert
    :param conf: settings file
    :param sql_sentence: sql sentence to execute
    :return: nothing
    """
    logging.info('Updating coin information table')

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
        logging.debug('duplicate record at coin information table')
        # print("Coin information Duplicate error!")
        pass


def update_coin_google_table(database, current_data, conf, sql_sentence):
    """
    Insert a record to coin's google table
    :param database: the database
    :param current_data: data to insert
    :param conf: settings file
    :param sql_sentence: sql sentence to execute
    :return: nothing
    """
    logging.info('Updating coin google information table')

    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database=database,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_sentence, (current_data[conf.table_key.coin_id],
                                              cast(current_data[conf.table_key.google_popularity], int),
                                              current_data[conf.table_key.google_sites]))
                connection.commit()
                return cursor.fetchall()
    except pymysql.err.IntegrityError:
        logging.debug('duplicate record at google information table')
        # print("Coin information Duplicate error!")
        pass


def update_sql_tables(database, coin_data, conf, sql_sentence):
    """
    Update all Sql tables with all information
    :return: Nothing
    """

    for coin in conf.coins:
        update_coins_table(database, conf.coins[coin], coin, sql_sentence[5])
    update_coin_price_today_table(database, coin_data, conf, sql_sentence[0])
    update_coin_price_yesterday_table(database, coin_data, conf, sql_sentence[1])
    update_coin_price_history_table(database, coin_data, conf, sql_sentence[2])
    update_coin_information_table(database, coin_data, conf, sql_sentence[3])
    update_coin_google_table(database, coin_data, conf, sql_sentence[4])
