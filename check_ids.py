import pymysql
from os import environ
from log import logger

class Check_IDs():

    def get_connection(self):  # function to get the connection string using: pymysql.connect(host, username, password, database)
        try:
            db_connection = pymysql.connect(
                environ.get("DB_HOST2"),  # host
                environ.get("DB_USER2"),  # username
                environ.get("DB_PW2"),  # password
                environ.get("DB_NAME2")  # database
            )
            logger.info("Connection successful LOL")
            return db_connection
        except Exception as error:
            logger.critical(f"Connection failed lol {error}")
            print(f"didn't work lol {error}")

    def table_unique_getter(self, table_name):
        if table_name == "drink_menu":
            rows_start = 1 # drink name, size, flava, price
            row_end = 4
            unique_id = 0
        elif table_name == "locations":
            rows_start = 1
            row_end = 2 # whatever makes the unique criteria
            unique_id = 0
        return(unique_id, rows_start, row_end)
    
    def load_ids(self, table_name):
        id_dict = {}
        unique_id, row_start, row_end = self.table_unique_getter(table_name)
        sql_string = f"SELECT * FROM {table_name}"
        data = self.sql_load_all(sql_string)
        for row in data:
            id_dict[row[row_start:row_end]] = row[unique_id]
        return id_dict

    def sql_load_all(self, sql_string):
        connection = self.get_connection()
        sql_load_list = []
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_string)
            connection.commit()
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                else:
                    sql_load_list.append(row)
            return(sql_load_list)
        except Exception as error:
            print(f"Unable to return all: \n{error}")
        finally:
            connection.close()