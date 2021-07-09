import pymysql.cursors


def run_sql(database, mysql_statement):
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


def setup_coins_table():
    sql_sentence = "CREATE TABLE IF NOT EXISTS coins (" \
                   "id INT AUTO_INCREMENT PRIMARY KEY," \
                   "name VARCHAR(20)" \
                   ");"
    run_sql('crypto', sql_sentence)


def setup_coin_price_today_table():
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
                   "coin_rank INT," \
                   "data_summery VARCHAR(256)" \
                   ");"
    run_sql('crypto', sql_sentence)
    sql_sentence = "ALTER TABLE `coin_price_today` " \
                   "ADD FOREIGN KEY (`coin_id`) REFERENCES" \
                   " `coins` (`id`);"
    run_sql('crypto', sql_sentence)


def setup_coin_price_yesterday_table():
    sql_sentence = "CREATE TABLE IF NOT EXISTS coin_price_yesterday (" \
                   "id INT AUTO_INCREMENT PRIMARY KEY," \
                   "coin_id INT," \
                   "price FLOAT," \
                   "low FLOAT," \
                   "high FLOAT," \
                   "open FLOAT," \
                   "close FLOAT," \
                   "coin_change FLOAT," \
                   "volume FLOAT" \
                   ");"
    run_sql('crypto', sql_sentence)
    sql_sentence = "ALTER TABLE `coin_price_yesterday` " \
                   "ADD FOREIGN KEY (`coin_id`) REFERENCES" \
                   " `coins` (`id`);"
    run_sql('crypto', sql_sentence)


def setup_coin_price_history_table():
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
                   "all_time_low FLOAT," \
                   "all_time_high FLOAT," \
                   "roi FLOAT," \
                   "circulating_supply INT," \
                   "total_supply INT," \
                   "max_supply INT" \
                   ");"
    run_sql('crypto', sql_sentence)
    sql_sentence = "ALTER TABLE `coin_price_history` " \
                   "ADD FOREIGN KEY (`coin_id`) REFERENCES" \
                   " `coins` (`id`);"
    run_sql('crypto', sql_sentence)


def setup_coin_information():
    sql_sentence = "CREATE TABLE IF NOT EXISTS coin_information (" \
                   "coin_id INT AUTO_INCREMENT PRIMARY KEY," \
                   "info VARCHAR(1000)" \
                   ");"
    run_sql('crypto', sql_sentence)
    sql_sentence = "ALTER TABLE `coin_information` " \
                   "ADD FOREIGN KEY (`coin_id`) REFERENCES" \
                   " `coins` (`id`);"
    run_sql('crypto', sql_sentence)


def setup_sql_database():
    """
    Setup sql database on first run
    :return: nothing
    """
    sql_sentence = "CREATE DATABASE IF NOT EXISTS crypto;"
    run_sql(None, sql_sentence)

    setup_coins_table()
    setup_coin_information()
    setup_coin_price_today_table()
    setup_coin_price_yesterday_table()
    setup_coin_price_history_table()


def update_coins_table(coins_list):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='crypto',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            for coin in coins_list:
                sql_statement = "INSERT INTO coins (" \
                                "name" \
                                ") VALUES (%s);"
            # Read a single record
            cursor.execute(sql_statement)
            connection.commit()
            return cursor.fetchall()


def update_coin_price_today_table(info_list):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='crypto',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql_statement = "INSERT INTO coin_price (" \
                            "coin_id" \
                            "price" \
                            "price_change" \
                            "low" \
                            "high" \
                            "volume" \
                            "volume_market_cap" \
                            "market_dominance" \
                            "market_cap" \
                            "fully_diluted_market_cap" \
                            "coin_rank" \
                            "data_summery" \
                            ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql_statement, (info_list[0], info_list[1], info_list[2], info_list[3],
                                           info_list[4], info_list[5], info_list[6], info_list[7],
                                           info_list[8], info_list[9], info_list[10], info_list[11]))
            connection.commit()
            return cursor.fetchall()


def update_coin_price_yesterday_table(info_list):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='crypto',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql_statement = "INSERT INTO coin_price_yesterday (" \
                            "coin_id" \
                            "price" \
                            "low" \
                            "high" \
                            "open" \
                            "close" \
                            "coin_change" \
                            "volume" \
                            ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql_statement, (info_list[0], info_list[1], info_list[2], info_list[3],
                                           info_list[4], info_list[5], info_list[6], info_list[7],
                                           ))
            connection.commit()
            return cursor.fetchall()


def update_coin_price_history_table(info_list):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='crypto',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql_statement = "INSERT INTO coin_price_history (" \
                            "coin_id" \
                            "7d_low" \
                            "7d_high" \
                            "30d_low" \
                            "30d_high" \
                            "90d_low" \
                            "90d_high" \
                            "52w_low" \
                            "52w_high" \
                            "all_time_low" \
                            "all_time_high" \
                            "roi" \
                            "circulating_supply" \
                            "total_supply" \
                            "max_supply" \
                            ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql_statement, (info_list[0], info_list[1], info_list[2], info_list[3],
                                           info_list[4], info_list[5], info_list[6], info_list[7],
                                           info_list[8], info_list[9], info_list[10], info_list[11],
                                           info_list[12], info_list[13], info_list[14]))
            connection.commit()
            return cursor.fetchall()


def update_coin_information_table(info_list):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='crypto',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql_statement = "INSERT INTO coin_information (" \
                            "coin_id" \
                            "info" \
                            ") VALUES (%s, %s);"
            cursor.execute(sql_statement, (info_list[0], info_list[1]))
            connection.commit()
            return cursor.fetchall()
