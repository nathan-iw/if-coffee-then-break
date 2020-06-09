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
            string = "id_dict[row[1:4]] = row[0]"
        elif table_name == "locations":
            string = "id_dict[row[1]] = row[0]"
        elif table_name == "pii":
            string = "id_dict[row[1]] = row[0]"
        return(string)
    
    def load_ids(self, table_name):
        id_dict = {}
        string = self.table_unique_getter(table_name)
        sql_string = f"SELECT * FROM {table_name} ORDER BY id"
        data = self.sql_load_all(sql_string)
        for row in data:
            exec(string)
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