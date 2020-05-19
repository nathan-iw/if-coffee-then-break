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

def save_transaction(list, drink_type):
    for drink in list:
        if drink_type == "Hot":
            args = (drink.drink_choice, drink.milk_choice, drink.strength_choice, drink.sugar_choice)
            sql_query = "INSERT INTO hot_drinks (hot_drink, milk, drink_strength, sugar) VALUES (%s, %s, %s, %s)"
            save_sql(sql_query, args)
            print(f"{drink.drink_choice}, with {drink.milk_choice} milk, {drink.strength_choice} with "
                  f"{drink.sugar_choice} sugar(s) has been saved to BrIW.")