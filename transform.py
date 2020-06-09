import pymysql
from os import environ
import time
from extract import Extract
import datetime
from log import logger
from check_ids import Check_IDs
import uuid
# Ahoy

class Transform():

    def transform(self, raw_data): # needs test
        id_instance = Check_IDs()
        location_list = []
        basket_dict = {}
        drink_dict = id_instance.load_ids("drink_menu")
        location_dict = id_instance.load_ids("locations")
        transformed_data = [] # Clean list to populate with transformed data
        for row in raw_data:
            trans_id = self.id_generator()
            t_date, t_time = self.date_breaker(row[1])  # defines variables for split date and time from date breaker
            # t_location = row[2] # taken directly from raw_data
            location_id = self.get_id(row[2], location_dict)
            # self.location_adder(row[2], location_list)
            t_first_name, t_last_name = self.person_breaker(row[3]) # splits first name from customer name.
            # t_order = row[4] # taken directly from raw_data
            drink_ids = self.order_loop(row[4], drink_dict)
            self.drink_splitter(self.drink_breaker(row[4]))
            # t_brok_flavour = self.flavour_breaker(self.drink_breaker(row[4]), drink_dict)
            t_price = int(float(row[5])*100)
            t_method = self.pay_method(row[6])
            t_card = self.card_masker(row[7])
            filled_basket = self.basket_generator(trans_id, drink_ids, basket_dict)
            transformed_data.append([trans_id, t_date, t_time, location_id, t_first_name, t_last_name, t_price, t_method, t_card])
        # return (transformed_data, drink_dict, location_dict, filled_basket)
        return (transformed_data, filled_basket)

    def id_generator(self):
        return str(uuid.uuid1())

    def basket_generator(self, trans_id, drink_id_list, basket_dict):
        basket_dict[trans_id] = drink_id_list
        return basket_dict

    def location_adder(self, location, location_list):
        location_list.append(location)
        return(location_list)
        
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
        
    def order_loop(self, raw_orders, drink_dict):
        basket = raw_orders.split(", ")
        drinks_per_order = []
        # basket = ["large armicano - Hazelnut: 1.40", "large armicano - Hazelnut: 1.40", "large armicano - Hazelnut: 1.40"]
        for drink in basket:
            split_drink = self.drink_splitter(drink)
            drink_id = self.get_id(split_drink[0:3], drink_dict)
            # self.drink_2_dict(split_drink, drink_dict) # add drink to menu
            # check drink in dictionary to get ID - then append the ID in the next line
            drinks_per_order.append(drink_id)
        return(drinks_per_order)
        
    def get_id(self, split_item, item_dict): # functions for drink OR location
        try:
            found_id = item_dict[split_item]
            return (found_id)
        except Exception as err:
            pass
            
    def drink_splitter(self, raw_drink): # tested ... Raw order is a list of strings
        # "large armicano - Hazelnut: 1.40"
        # If order contains ":" then contains a price, needs splitting.
        drink_flav = self.flavour_breaker(raw_drink) # drink_flav = [large americano, hazlenut: 1.40]
        if ": " in str(drink_flav[1]):
            drink = drink_flav[0].strip()
            flavour_price = drink_flav[1].split(": ")
            flavour = flavour_price[0]
            drink_price = int(100*float(flavour_price[1]))
        else:
            drink = drink_flav[0]
            flavour = drink_flav[1]
            # if flavour == None:
            # flavour = "Orginal"
            # print(flavour)
            drink_price = 0
        drink = self.get_name(drink)
        split_drink = (drink[1], drink[0], flavour, drink_price)

        return split_drink

    def get_name(self, drink):
        name_broken = []
        drink_size = "N/A"
        if "Large" in drink:
            drink_size = "Large"
            drink_name = drink.split("Large ")[1]
        else:
            try:
                drink_name = drink.split("Regular ")[1]
                drink_size = "Regular"
            except:
                drink_name = drink
                drink_size = "N/A"
        return (drink_size, drink_name)

    def drink_2_dict(self, split_drink, drink_dict):
        x = {(split_drink[0:3]): split_drink[3]}
        drink_dict.update(x)
        return drink_dict
        # (Drink name, drink size, drink flava): price

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
 
