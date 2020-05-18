# Load
import pymysql
from os import environ


def save_sql(sql_query, args):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql_query, args)
    connection.commit()
    cursor.close()
    connection.close()