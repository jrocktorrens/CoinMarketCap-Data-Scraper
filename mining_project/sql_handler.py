import pymysql.cursors


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


def setup_coins_table(database):
    """
    Create the coins table if not exist
    :return: nothing
    """
    sql_sentence = "CREATE TABLE IF NOT EXISTS coins (" \
                   "coin_id INT PRIMARY KEY," \
                   "name TEXT" \
                   ");"
    run_sql(database, sql_sentence)


def setup_coin_price_today_table(database):
    """
    Create today's coin price table
    :return: nothing
    """
    sql_sentence = "CREATE TABLE IF NOT EXISTS coin_price_today (" \
                   "id INT AUTO_INCREMENT PRIMARY KEY," \
                   "coin_id INT," \
                   "price FLOAT," \
                   "price_change FLOAT," \
                   "low FLOAT," \
                   "high FLOAT," \
                   "volume FLOAT," \
                   "volume_market_cap FLOAT," \
                   "market_dominance FLOAT," \
                   "market_cap FLOAT," \
                   "fully_diluted_market_cap FLOAT," \
                   "market_rank INT," \
                   "data_summery TEXT" \
                   ");"
    run_sql(database, sql_sentence)
    sql_sentence = "ALTER TABLE `coin_price_today` " \
                   "ADD FOREIGN KEY (`coin_id`) REFERENCES" \
                   " `coins` (`coin_id`);"
    run_sql('crypto', sql_sentence)
    sql_sentence = "ALTER TABLE coin_price_today ADD UNIQUE (" \
                   "coin_id," \
                   "price," \
                   "price_change," \
                   "low," \
                   "high," \
                   "volume," \
                   "volume_market_cap," \
                   "market_dominance," \
                   "market_cap," \
                   "fully_diluted_market_cap," \
                   "market_rank);"
    run_sql('crypto', sql_sentence)


def setup_coin_price_yesterday_table(database):
    """
    Create yesterday's coin price table
    :return: nothing
    """
    try:
        sql_sentence = "CREATE TABLE IF NOT EXISTS coin_price_yesterday (" \
                       "id INT AUTO_INCREMENT PRIMARY KEY," \
                       "coin_id INT UNIQUE," \
                       "low FLOAT UNIQUE," \
                       "high FLOAT UNIQUE," \
                       "open FLOAT UNIQUE," \
                       "close FLOAT UNIQUE," \
                       "coin_change FLOAT UNIQUE," \
                       "volume FLOAT UNIQUE" \
                       ");"
        run_sql(database, sql_sentence)
        sql_sentence = "ALTER TABLE `coin_price_yesterday` " \
                       "ADD FOREIGN KEY (`coin_id`) REFERENCES" \
                       " `coins` (`coin_id`);"
        run_sql(database, sql_sentence)
        sql_sentence = "ALTER TABLE coin_price_yesterday ADD UNIQUE ("\
                       "coin_id," \
                       "low," \
                       "high," \
                       "open," \
                       "close," \
                       "coin_change," \
                       "volume" \
                       ");"
        run_sql(database, sql_sentence)
    except Exception as ex:
        print(f"Error")


def setup_coin_price_history_table(database):
    """
    Create price history table
    :return: nothing
    """
    sql_sentence = "CREATE TABLE IF NOT EXISTS coin_price_history (" \
                   "id INT AUTO_INCREMENT PRIMARY KEY," \
                   "coin_id INT," \
                   "7d_low FLOAT," \
                   "7d_high FLOAT," \
                   "30d_low FLOAT," \
                   "30d_high FLOAT," \
                   "90d_low FLOAT," \
                   "90d_high FLOAT," \
                   "52w_low FLOAT," \
                   "52w_high FLOAT," \
                   "roi FLOAT" \
                   ");"
    run_sql(database, sql_sentence)
    sql_sentence = "ALTER TABLE `coin_price_history` " \
                   "ADD FOREIGN KEY (`coin_id`) REFERENCES" \
                   " `coins` (`coin_id`);"
    run_sql(database, sql_sentence)
    sql_sentence = "ALTER TABLE coin_price_history ADD UNIQUE (" \
                   "coin_id," \
                   "7d_low," \
                   "7d_high," \
                   "30d_low," \
                   "30d_high," \
                   "90d_low," \
                   "90d_high," \
                   "52w_low," \
                   "52w_high," \
                   "roi" \
                   ");"
    run_sql(database, sql_sentence)


def setup_coin_information(database):
    """
    Create coin information table
    :return: nothing
    """
    sql_sentence = "CREATE TABLE IF NOT EXISTS coin_information (" \
                   "coin_id INT AUTO_INCREMENT PRIMARY KEY," \
                   "info TEXT" \
                   ");"
    run_sql(database, sql_sentence)
    sql_sentence = "ALTER TABLE `coin_information` " \
                   "ADD FOREIGN KEY (`coin_id`) REFERENCES" \
                   " `coins` (`coin_id`);"
    run_sql(database, sql_sentence)
    sql_sentence = "ALTER TABLE coin_information ADD UNIQUE (" \
                   "coin_id" \
                   ");"
    run_sql(database, sql_sentence)


def setup_sql_database(database):
    """
    Setup sql database if not exist
    and then create all tables
    :return: nothing
    """
    sql_sentence = "CREATE DATABASE IF NOT EXISTS crypto;"
    run_sql(None, sql_sentence)

    setup_coins_table(database)
    setup_coin_information(database)
    setup_coin_price_today_table(database)
    setup_coin_price_yesterday_table(database)
    setup_coin_price_history_table(database)


def update_coins_table(coin_id, coin_name):
    """
    Insert a record to coins table
    :param coin_id: coin id
    :param coin_name: coin name
    :return: nothing
    """
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database='crypto',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql_statement = "INSERT INTO coins (" \
                                    "coin_id," \
                                    "name" \
                                    ") VALUES (%s, %s);"
                    # Write a single record
                cursor.execute(sql_statement, (coin_id, coin_name))
                connection.commit()
                return cursor.fetchall()
    except pymysql.err.IntegrityError as ex:
        print("Coin Duplicate error!")


def update_coin_price_today_table(current_data, conf):
    """
    Insert a record to today's coin price table
    :param current_data: data to insert
    :param conf: settings file
    :return: nothing
    """
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database='crypto',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql_statement = "INSERT INTO coin_price_today (" \
                                "coin_id," \
                                "price," \
                                "price_change," \
                                "low," \
                                "high," \
                                "volume," \
                                "volume_market_cap," \
                                "market_dominance," \
                                "market_cap," \
                                "fully_diluted_market_cap," \
                                "market_rank," \
                                "data_summery" \
                                ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

                cursor.execute(sql_statement, (current_data[conf.table_key.coin_id],
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
    except pymysql.err.IntegrityError as ex:
        print("Coin price today Duplicate error!")


def update_coin_price_yesterday_table(current_data, conf):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database='crypto',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql_statement = "INSERT INTO coin_price_yesterday (" \
                                "coin_id," \
                                "low," \
                                "high," \
                                "open," \
                                "close," \
                                "coin_change," \
                                "volume" \
                                ") VALUES (%s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(sql_statement, (current_data[conf.table_key.coin_id],
                                               current_data[conf.table_key.yesterday_low],
                                               current_data[conf.table_key.yesterday_high],
                                               current_data[conf.table_key.yesterday_open],
                                               current_data[conf.table_key.yesterday_close],
                                               current_data[conf.table_key.yesterday_change],
                                               current_data[conf.table_key.yesterday_volume]
                                               ))
                connection.commit()
                return cursor.fetchall()
    except pymysql.err.IntegrityError as ex:
        print("Coin price yesterday Duplicate error!")


def update_coin_price_history_table(current_data, conf):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database='crypto',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql_statement = "INSERT INTO coin_price_history (" \
                                "coin_id," \
                                "7d_low," \
                                "7d_high," \
                                "30d_low," \
                                "30d_high," \
                                "90d_low," \
                                "90d_high," \
                                "52w_low," \
                                "52w_high," \
                                "roi" \
                                ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(sql_statement, (current_data[conf.table_key.coin_id],
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
    except pymysql.err.IntegrityError as ex:
        print("Coin price history Duplicate error!")


def update_coin_information_table(current_data, conf):
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     database='crypto',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql_statement = "INSERT INTO coin_information (" \
                                "coin_id," \
                                "info" \
                                ") VALUES (%s, %s);"
                cursor.execute(sql_statement, (current_data[conf.table_key.coin_id],
                                               current_data[conf.table_key.coin_about]))
                connection.commit()
                return cursor.fetchall()
    except pymysql.err.IntegrityError as ex:
        print("Coin information Duplicate error!")
