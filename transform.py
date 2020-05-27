import pymysql
from os import environ
import time
from extract import Extract
import datetime
from log import logger


class Transform():

    def get_raw_data(self):
        app = Extract()
        return app.load_data() # Loads data from DB, returns "raw_data"

    def transform(self, raw_data): # needs test
        transformed_data = [] # Clean list to populate with transformed data
        drink_dict = {} # Clean dictionary to populate with split drink, size and flavour
        for row in raw_data:
            t_date, t_time = self.date_breaker(row[1])  # defines variables for split date and time from date breaker
            t_location = row[2] # taken directly from raw_data
            t_first_name, t_last_name = self.person_breaker(row[3]) # splits first name from customer name.
            t_order = row[4] # taken directly from raw_data
            t_drink_menu = self.get_drink_list(self.drink_breaker(row[4]), drink_dict)
            # t_brok_flavour = self.flavour_breaker(self.drink_breaker(row[4]), drink_dict)
            t_price = int(float(row[5])*100)
            t_method = self.pay_method(row[6])
            t_card = self.card_masker(row[7])
            transformed_data.append([t_date, t_time, t_location, t_first_name, t_last_name, t_order, t_price, t_method, t_card])
        return (transformed_data, drink_dict)

    def drink_breaker(self, raw_order): # tested
        dirty_order = raw_order.split(", ") # 
        clean_order = []
        for i in dirty_order:
            clean_order.append(i.strip())
        return clean_order

    def flavour_breaker(self, drink):
        broken_flavour = []
        flavour = None
        if " - " in drink:
            split_order = drink.split(" - ")
            drink = split_order[0] # drink = large americano
            flavour = split_order[1] # flavour = hazlenut: 1.40
        elif ": " in drink:
            split_order = drink.split(": ")
            drink = split_order[0]
            flavour = f"Original: {split_order[1]}"
        else:
            flavour = "Original"
        broken_flavour.append(drink) 
        broken_flavour.append(flavour) # broken flavour = [large americano, hazlenut: 1.40]
        return broken_flavour

    def get_name(self, drink):
        name_broken = []
        drink_size = None
        if "Large" in drink:
            drink_size = "Large"
            drink_name = drink.split("Large ")[1]
        else:
            try:
                drink_name = drink.split("Regular ")[1]
                drink_size = "Regular"
            except:
                drink_name = drink
                drink_size = None
        return (drink_size,drink_name)
            
    def get_drink_list(self, raw_orders, drink_dict): # tested ... Raw order is a list of strings
        for drink in raw_orders: # raw_orders = ["large armicano - Hazelnut: 1.40", "large armicano - Hazelnut: 1.40", "large armicano - Hazelnut: 1.40"]
    # If order contains ":" then contains a price, needs splitting.
            drink_flav = self.flavour_breaker(drink) # drink_flav = [large americano, hazlenut: 1.40]
            if ": " in str(drink_flav[1]):
                drink = drink_flav[0]
                flavour_price = drink_flav[1].split(": ")
                flavour = flavour_price[0]
                drink_price = int(100*float(flavour_price[1]))
            else:
                drink = drink_flav[0]
                flavour = drink_flav[1]
                # if flavour == None:
                #     flavour = "Orginal"
                # print(flavour)
                drink_price = None
            drink = self.get_name(drink)
            x = {(drink[1].strip(), drink[0], flavour):drink_price}
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
 
