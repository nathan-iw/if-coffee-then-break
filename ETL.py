import pymysql
from os import environ
import time
from extract import Extract
from transform import Transform
from load import Load


if __name__ == "__main__":
    start = time.time()
    app = Extract()
    app.load_data()
    end_extract = time.time()
    print(f"Extract time:")
    print(round(end_extract - start, 4))
    apple = Load()
    transformed_data, transformed_drink_menu_data = apple.get_transformed_data()

    end_transform = time.time()
    print(f"Transform time:")
    print(round(end_transform - end_extract, 4))


    # apple.save_transaction(transformed_data) # populate RDS instance with cleaned data.
    apple.save_drink_menu(transformed_drink_menu_data) # generate drinks menu

    end_load = time.time()
    print(f"Load time:")
    print(round(end_load - end_transform, 4))