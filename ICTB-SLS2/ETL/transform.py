import pymysql
from os import environ
import time
from ETL.csv_extract import Extract
import datetime
from ETL.log import logger
from ETL.check_ids import Check_IDs


class Transform():
    def __init__(self):
        self.id_instance = Check_IDs()
        self.location_dict = self.id_instance.load_ids("locations")
        self.drink_dict = self.id_instance.load_ids("drink_menu")
        self.basket_dict = {}
        self.new_locations = {} # add locations that aren't in the clean dictionary to here
        self.new_drinks = {} # add drinks that aren't in the clean dictionary to here
        self.transformed_data = []

    def transform(self, raw_data): # needs test
        print(raw_data)
        for row in raw_data: # row: ['2020-06-11 13:26:25.441651', 'Uppingham', 'James Williams', ' Glass of milk: 0.7', 0.7, 'CARD', 'Type: mastercard\nCCN: 5439844399567818']
            if len(row) != 7:
                continue 
            # trans_id = self.id_generator()
            t_date, t_time = self.csv_date_breaker(row[0])  # defines variables for split date and time from date breaker
            # t_date, t_time = self.date_breaker(row[1])  # defines variables for split date and time from date breaker
            location_id = self.get_id(row[1])
            trans_id = self.id_maker(row[0],location_id)
            t_first_name, t_last_name = self.person_breaker(row[2]) # splits first name from customer name.            
            drink_ids = self.order_to_drink_ids(row[3])            
            filled_basket = self.basket_generator(trans_id, drink_ids)
            t_price = int(float(row[4])*100)
            t_method = self.pay_method(row[5])

            self.transformed_data.append([trans_id, t_date, t_time, location_id, t_first_name, t_last_name, t_price, t_method])
        print(self.transformed_data)
        return (self.transformed_data, self.new_drinks, self.new_locations, filled_basket)

    def id_maker(self, date_string, location_id):
        characters_to_remove = "- :"
        new_string = date_string
        for character in characters_to_remove:
            new_string = new_string.replace(character, "")
        noo_id = new_string+'.'+str(location_id)
        return(noo_id)

    def basket_generator(self, trans_id, drink_id_list):
        self.basket_dict[trans_id] = drink_id_list
        return self.basket_dict

    def location_adder(self, location, location_list):
        location_list.append(location)
        return(location_list)
        
    def drink_breaker(self, raw_order): # tested
        dirty_order = raw_order.split(", ") # 
        clean_order = []
        for i in dirty_order:
            clean_order.append(i.strip())
        return clean_order

    def drink_flav_breaker(self, drink):
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
        
    def order_to_drink_ids(self, raw_orders):
        basket = raw_orders.split(", ") # basket = ["large armicano - Hazelnut: 1.40", "large armicano - Hazelnut: 1.40", "large armicano - Hazelnut: 1.40"]
        drink_ids_in_trans = []
        for drink in basket:
            split_drink = self.get_split_drink(drink)
            drink_id = self.get_id(split_drink)
            drink_ids_in_trans.append(drink_id)
        return(drink_ids_in_trans)
        
    def get_id(self, split_item): # functions for drink OR location
        if type(split_item) == tuple: # == drink
            try:
                found_id = self.drink_dict[split_item[0:3]]
                return (found_id)
            except:
                generated_id = self.item_adder(split_item, self.drink_dict)
                self.drink_dict[split_item[0:3]] = generated_id
                self.new_drinks[split_item]=generated_id
                return (generated_id)
        else: # == location 
            try:
                found_id = self.location_dict[split_item]
                return (found_id)
            except:
                generated_id = self.item_adder(split_item, self.location_dict)
                self.location_dict[split_item]=generated_id 
                self.new_locations[split_item]=generated_id 
                return (generated_id)
                
    def item_adder(self, split_item, item_dict):
        max_id = max(item_dict.values())
        new_id = max_id + 1
        return(new_id)
        
    def get_split_drink(self, raw_drink): 
        # "large armicano - Hazelnut: 1.40"
        drink_name_size, flavour, drink_price = self.get_price_and_flavour(raw_drink)
        size, name = self.drink_name_size_breaker(drink_name_size)
        split_drink = (name, size, flavour, drink_price)
        return split_drink

    def get_price_and_flavour(self, drink_string):
        drink_flav = self.drink_flav_breaker(drink_string) # drink_flav = [large americano, hazlenut: 1.40]
        if ": " in str(drink_flav[1]): # if it has a price
            drink = drink_flav[0].strip()
            flavour_price = drink_flav[1].split(": ")
            flavour = flavour_price[0]
            drink_price = int(100*float(flavour_price[1]))
        else: # if it doesn't have a price
            drink = drink_flav[0]
            flavour = drink_flav[1]
            drink_price = 0
        return drink, flavour, drink_price

    def drink_name_size_breaker(self, drink):
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

    def date_breaker(self, date): # not tested
        split_date = date.date()
        split_time = date.time()
        return (split_date, split_time) 

    def csv_date_breaker(self, date): # not tested
        split_date = date.split(" ")
        clean_date = split_date[0]
        clean_time = split_date[1]
        return (clean_date, clean_time)

    def pay_method(self, raw_method): # tested
        pay_method = raw_method.capitalize()
        return pay_method

    def person_breaker(self, person): # tested
        broken_person = person.split(" ")
        first_name = broken_person[0]
        last_name = broken_person[1]
        name = (first_name, last_name)
        return name
 
