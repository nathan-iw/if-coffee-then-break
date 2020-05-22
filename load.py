# Load
import pymysql
from os import environ
from extract import Extract
from transform import Transform

class Load():

    def get_connection(self):  # function to get the connection string using: pymysql.connect(host, username, password, database)
        try:
            db_connection = pymysql.connect(
                environ.get("DB_HOST2"),  # host
                environ.get("DB_USER2"),  # username
                environ.get("DB_PW2"),  # password
                environ.get("DB_NAME2")  # database
            )
            return db_connection
            print("worked")
        except Exception as error:
            print(f"didn't work lol {error}")

    def get_transformed_data(self):
        app = Transform()
        t_data = app.transform(app.get_raw_data())
        return t_data

    def update_sql(self, sql_string, args):
        connection = self.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(sql_string, args)
        connection.commit()
        cursor.close()
        connection.close()

    def save_transaction(self, transformed_list):
        for t in transformed_list:
            args = t[0:9]
            str1 = ''.join(t[5])
            sql_query = "INSERT INTO clean_transactions (date, transaction_time, location, firstname, lastname, drink_order, total_price, method, ccn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.update_sql(sql_query, args)

    def save_drink_menu(self, drink_dict):
        for key in drink_dict.items():
            args = (key[0][0], key[0][1], key[0][2], key[1])
            print(args)
            sql_query = "INSERT INTO drink_menu (drink_name, drink_size, drink_flavour, price) VALUES (%s, %s, %s, %s)"
            try:
                self.update_sql(sql_query, args)
            except Exception as error:
                print(f"DOOP! {error}")

       


