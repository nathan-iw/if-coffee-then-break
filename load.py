# Load
import pymysql
from os import environ
from extract import Extract
from transform import Transform
from Secrets import get_secret
import logging


logger = logging.getLogger(__name__) 

class Load():
    def get_connection(self):  # function to get the connection string using: pymysql.connect(host, username, password, database)
        host, username, password, db_name = get_secret()[0:5]
        try:
            db_connection = pymysql.connect(
                host,
                username,
                password,
                db_name
            )
            print("Got connection")
            return db_connection
        except Exception as error:
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
        logger.info(f"The number of transactions processed:{len(transformed_list)}")
        index = 0
        for t in transformed_list:
            args = t[0:9]
            str1 = ''.join(t[5])
            sql_query = "INSERT INTO clean_transactions (date, transaction_time, location, firstname, lastname, drink_order, total_price, method, ccn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor = self.update_sql(sql_query, args, connection)
            if index %50 == 0:
                print(f"Progress [{round(index*100/len(transformed_list),2)}/100%]", end="\r")
            index += 1
        connection.commit()
        cursor.close()

    def save_drink_menu(self, drink_dict):
        connection = self.get_connection()
        logger.info(f"The number of unique drinks processed:{len(drink_dict)}")
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

       


