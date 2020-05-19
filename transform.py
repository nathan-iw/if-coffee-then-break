import pymysql
from os import environ
import time
from extract import Extract
import datetime


 # loads the raw data list from extract.

# Input:
# (633, datetime.datetime(2020, 5, 18, 15, 46, 1), 'Isle of Wight', 'Oscar Ohara', ' Frappes - Chocolate Cookie', Decimal('2.75'), 'CASH', None)]

class Transform():

    def get_raw_data(self):
        app = Extract()
        return app.load_data()

    def transform(self, raw_data): # needs test
        transformed_data = []
        drink_dict = {}
        for row in raw_data:
            t_date, t_time = self.date_breaker(row[1])  # append transformed data
            t_location = row[2]
            t_first_name, t_last_name = self.person_breaker(row[3]) # splits first name from customer name.
            t_order = self.drink_breaker(row[4])
            t_drink_menu = self.get_drink_list(t_order, drink_dict)
            t_price = row[5]
            t_method = self.pay_method(row[6])
            t_card = self.card_masker(row[7])
            transformed_data.append([t_date, t_time, t_location, t_first_name, t_last_name, t_order, t_price, t_method, t_card])
        for line in transformed_data:
            print(line)
            print("")
        print(f"Drink list: {drink_dict}")
        return transformed_data

    def drink_breaker(self, raw_order): # tested
        dirty_order = raw_order.split(", ")
        clean_order = []
        for i in dirty_order:
            clean_order.append(i.strip())
        return clean_order
    
    def get_drink_list(self, raw_orders, drink_dict): # tested
        for drink in raw_orders:
            if ":" in str(drink):
                split_drink = drink.split(": ")
                drink = split_drink[0]
                drink_price = split_drink[1]
            else:
                drink_price = "Unassigned price"
            x = {drink.strip():drink_price}
            drink_dict.update(x)
        return drink_dict
                      
    def date_breaker(self, date): # not tested
        split_date = date.date()
        split_time = date.time()
        return (split_date, split_time) 

    def pay_method(self, raw_method): # tested
        pay_method = raw_method.capitalize()
        return pay_method

    def card_masker(self, ccn): # tested
        if ccn == None:
            return None
        digits = ccn.replace(ccn[:-4], (len(ccn)-4) * "*") # X out everything other than the last 4 digits
        return digits # returns the disguised ccn

    def person_breaker(self, person): # tested
        broken_person = person.split(" ")
        first_name = broken_person[0]
        last_name = broken_person[1]
        name = (first_name, last_name)
        return name
 
