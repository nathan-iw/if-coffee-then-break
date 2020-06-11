# Load
import pymysql
from os import environ
from csv_extract import Extract
from transform import Transform
from Secrets import get_secret
from log import logger
import time

class Load():

    def get_connection(self):  # function to get the connection string using: pymysql.connect(host, username, password, database)
        if environ.get("ENVIRONMENT") == "prod":
            host, username, password, db_name = get_secret()[0:5]
        else:
            host, username, password, db_name = environ.get("DB_HOST2"), environ.get("DB_USER2"), environ.get("DB_PW2"), environ.get("DB_NAME2")  
        try:      
            db_connection = pymysql.connect(
                host,
                username,
                password,
                db_name
            )
            print("Got connection")
            logger.info("Load connection successful LOL")
            return db_connection
        except Exception as error:
            logger.critical("Load connection failed LOL")
            print(f"didn't work lol {error}")


    def update_sql(self, sql_string, args, connection):
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql_string, args)
            except Exception as error:
                print(f"didn't work lol doopy mcdoo {error}")
        return cursor

    def save_transaction(self, transformed_list):
        connection = self.get_connection()
        start = time.time()
        logger.info(f"The number of transactions processed:{len(transformed_list)}")
        print(f"The number of transactions processed:{len(transformed_list)}")
        index = 0
        for t in transformed_list:
            args = t[0:8]
            sql_query = "INSERT INTO clean_transactions (id, date, transaction_time, location, firstname, lastname, total_price, method) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor = self.update_sql(sql_query, args, connection)
            if index %10 == 0 and index != 0:
                t2 = time.time()
                current_load_time = t2 - start
                percentage = round(index*100/len(transformed_list),2)
                total_time_estimate = current_load_time / percentage * 100
                time_remaining = total_time_estimate - current_load_time
                print(f"Progress: {progress(percentage)} [{percentage}%] Estimated time remaining: {round(time_remaining,2)} seconds", end="\r")
            index += 1
        print(f"Progress: {progress(100)} [100%] Load transactions complete! You are king d00p!", end="\r")
        connection.commit()
        cursor.close()

    def save_drink_menu(self, drink_dict):
        connection = self.get_connection()
        logger.info(f"The number of unique drinks processed: {len(drink_dict)}")
        print(drink_dict)
        for drink_features, drink_id in drink_dict.items():
            args = (drink_id, drink_features[0], drink_features[1], drink_features[2], drink_features[3])
            sql_query = "INSERT INTO drink_menu (id, drink_name, drink_size, drink_flavour, price) VALUES (%s, %s, %s, %s, %s)"
            cursor = self.update_sql(sql_query, args, connection)
        connection.commit()
        try:
            cursor.close()
        except Exception as error:
            print("no new drinks lol")

    def save_basket(self, basket_dict):
        connection = self.get_connection()
        for trans_id, drink_order in basket_dict.items():
            for drink in drink_order:
                args = (trans_id, drink)
                sql_query = "INSERT INTO basket (trans_id, drink_id) VALUES (%s, %s)"
                try:
                    cursor = self.update_sql(sql_query, args, connection)
                except Exception as error:
                    logger.critical(f"DOOP! {error}")
        connection.commit()
        cursor.close()

    def save_location_menu(self, new_locations):
        connection = self.get_connection()
        logger.info(f"The number of unique locations processed: {len(new_locations)}")
        for location, location_id in new_locations.items():
            args = (location_id, location)
            sql_query = "INSERT INTO locations (id, location) VALUES (%s, %s)"
            try:
                cursor = self.update_sql(sql_query, args, connection)
            except Exception as error:
                logger.critical(f"DOOP! {error}")
        connection.commit()
        try:
            cursor.close()
        except Exception as error:
            print("no new locals lmao, where's ches??????")
        
def progress(percentage_progress):
    progress_bar = int(round(percentage_progress,0)) * "#"
    remaining_bar = (100 - int(round(percentage_progress,0))) * "-"
    return f"{progress_bar}{remaining_bar}"


