import pymysql
from os import environ
import time
from extract import Extract
from transform import Transform
from load import Load
from log import logger
         
# logger = logging.getLogger(__name__) 

if __name__ == "__main__":
    logger.info("application ran")
    start = time.time()
    app = Extract()
    # raw_data_list = app.load_yesterdays_data() # extract output from yesterday
    raw_data_list = app.load_all_data()  # extract output from all time
    end_extract = time.time()
    extract_time = round(end_extract - start, 4)
    print(f"Extract time: {extract_time}")
    logger.info(f"Extract time: {extract_time}")
    apple = Transform()
    # transformed_data, transformed_drink_menu_data, location_list, basket = apple.transform(raw_data_list) # raw data into transform returns transformed data and drinks dic
    transformed_data, basket = apple.transform(raw_data_list) # raw data into transform returns transformed data and drinks dic

    end_transform = time.time()
    transform_time = round(end_transform - end_extract,4)
    logger.info(f"Transform time: {transform_time}")
    print(f"Transform time: {transform_time}")
    appley = Load()

    # appley.save_transaction(transformed_data) # populate RDS instance with cleaned data.
    # appley.save_drink_menu(transformed_drink_menu_data) # generate drinks menu
    # appley.save_location_menu(location_list) # generate drinks menu
    appley.save_basket(basket) # generate drinks menu


    end_load = time.time()
    load_time = round(end_load - end_transform, 4)
    logger.info(f"Loading time: {load_time}")
    total_time = extract_time + transform_time + load_time
    logger.info(f"total time: {total_time}")
    print(f"Load time: {load_time}\nTotal time: {total_time}")

