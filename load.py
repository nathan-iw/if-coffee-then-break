# Load
import pymysql
from os import environ
from extract import Extract
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

    # def get_transformed_data(self):
    #     app = Transform()
    #     t_data = app.transform(app.get_raw_data()) # to be fixed, gets inital connection for extract twice currently. 
    #     return t_data

    def update_sql(self, sql_string, args, connection):
        with connection.cursor() as cursor:
            cursor.execute(sql_string, args)
        return cursor

    def save_transaction(self, transformed_list):
        connection = self.get_connection()
        start = time.time()
        logger.info(f"The number of transactions processed:{len(transformed_list)}")
        print(f"The number of transactions processed:{len(transformed_list)}")
        index = 0
        for t in transformed_list:
            args = t[0:9]
            sql_query = "INSERT INTO clean_transactions (date, transaction_time, location, firstname, lastname, drink_order, total_price, method, ccn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor = self.update_sql(sql_query, args, connection)
            if index %10 == 0 and index != 0:
                t2 = time.time()
                current_load_time = t2 - start
                percentage = round(index*100/len(transformed_list),2)
                total_time_estimate = current_load_time / percentage * 100
                time_remaining = total_time_estimate - current_load_time
                print(f"Progress: {progress(percentage)} [{percentage}%] Estimated time remaining: {round(time_remaining,2)} seconds", end="\r")
            index += 1
        connection.commit()
        cursor.close()

    def save_drink_menu(self, drink_dict):
        connection = self.get_connection()
        logger.info(f"The number of unique drinks processed: {len(drink_dict)}")
        for key in drink_dict.items():
            args = (key[0][0], key[0][1], key[0][2], key[1])
            print(args)
            sql_query = "INSERT INTO drink_menu (drink_name, drink_size, drink_flavour, price) VALUES (%s, %s, %s, %s)"
            try:
                cursor = self.update_sql(sql_query, args, connection)
            except Exception as error:
                print(f"DOOP! {error}")
        connection.commit()
        cursor.close()

    def save_location_menu(self, location_list):
        connection = self.get_connection()
        logger.info(f"The number of unique drinks processed: {len(location_list)}")
        for place in location_list:
            args = (place)
            print(args)
            sql_query = "INSERT INTO locations (location) VALUES (%s)"
            try:
                cursor = self.update_sql(sql_query, args, connection)
            except Exception as error:
                print(f"DOOP! {error}")
        connection.commit()
        cursor.close()
       
def progress(percentage_progress):
    progress_bar = int(round(percentage_progress,0)) * "#"
    remaining_bar = (100 - int(round(percentage_progress,0))) * "-"
    return f"{progress_bar}{remaining_bar}"


