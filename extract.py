# Extract
import pymysql
from os import environ
import datetime
from log import logger

# logger = logging.getLogger(__name__) 

class Extract():

    def get_connection(self):  # function to get the connection string using: pymysql.connect(host, username, password, database)
        try:
            db_connection = pymysql.connect(
                environ.get("DB_HOST_SAINS"),  # host
                environ.get("DB_USER_SAINS"),  # username
                environ.get("DB_PW_SAINS"),  # password
                environ.get("DB_NAME_SAINS")  # database
            )
            logger.info("Connection successful LOL")
            return db_connection
        except Exception as error:
            logger.critical(f"Connection failed lol {error}")
            (f"didn't work lol {error}")
    
    def load_all_data(self):
        raw_data = []

        sql_string = f"SELECT * FROM transactions ORDER BY Date DESC LIMIT 1000"
        data = self.sql_load_all(sql_string)
        for row in data:
            raw_entry = row[0:8]
            raw_data.append(raw_entry)
        return raw_data

    def load_yesterdays_data(self):
        raw_data = []
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        print(yesterday)
        sql_string = f"SELECT * FROM transactions WHERE Date >= '{yesterday} 00:00:01'  and Date <= '{yesterday} 23:59:59' LIMIT 50"
        data = self.sql_load(sql_string)
        for row in data:
            raw_entry = row[0:8]
            raw_data.append(raw_entry)
        return raw_data
    
    def sql_load(self, sql_string):
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
            (f"Unable to return all: \n{error}")
        finally:
            connection.close()