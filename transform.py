import pymysql
from os import environ
import time
from extract import Extract
import datetime


 # loads the raw data list from extract.

# Input:
# (633, datetime.datetime(2020, 5, 18, 15, 46, 1), 'Isle of Wight', 'Oscar Ohara', ' Frappes - Chocolate Cookie', Decimal('2.75'), 'CASH', None)]

class Transform():

    def transform(self):
        transformed_data = []
        app = Extract()
        raw_data = app.load_data()
        for row in raw_data:
            t_location = row[2]
            t_price = row[5]
            t_method = self.pay_method(row[6])
            t_card = self.card_masker(row[7])
            t_first_name, t_last_name = self.person_breaker(row[3]) # splits first name from customer name.
            t_date, t_time = self.date_breaker(row[1])  # append transformed data
            t_drink_order = self.drink_breaker(row[4])

    def drink_breaker(self, raw_order):
        split_drink = raw_order.split(", ")
        print(split_drink)
        # for i in split_drink:

        

    def date_breaker(self, date):
        print(f"{date.date()} {date.time()}")
        return date.date(), date.time() 

    def pay_method(self, raw_method):
        pay_method = raw_method.capitalize()
        print (pay_method)
        return pay_method

    def card_masker(self, ccn):
        if ccn == None:
            return None
        digits = ccn.replace(ccn[:-4], (len(ccn)-4) * "*") # X out everything other than the last 4 digits
        print(digits)
        return digits # returns the disguised ccn

    def person_breaker(self, person):
        broken_person = person.split(" ")
        first_name = broken_person[0]
        last_name = broken_person[1]
        name = (first_name, last_name)
        print(name)
        return name
 
  
