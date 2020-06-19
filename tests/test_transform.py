import unittest
from transform import Transform
from unittest.mock import Mock, patch, call, MagicMock
import time
import datetime
from check_ids import Check_IDs


class TransformTests(unittest.TestCase):

    def setUp(self):
        self.app = Transform()
        self.id = Mock(Check_IDs)
        
        
    def test_drink_breaker(self):
        #Arrange
        mock_drink = " Frappes - Chocolate Cookie: 2.29"
        expected = ["Frappes - Chocolate Cookie: 2.29"]
        #Act
        actual = self.app.drink_breaker(mock_drink)
        #Assert
        self.assertEqual(expected, actual)

    def test_drinks_breaker(self):
        #Arrange
        mock_drinks_list = " Frappes - Chocolate Cookie: 2.29,  Large Americano: 3.29"
        expected = ["Frappes - Chocolate Cookie: 2.29", "Large Americano: 3.29"]
        #Act
        actual = self.app.drink_breaker(mock_drinks_list)
        #Assert
        self.assertEqual(expected, actual)

    def test_pay_method_lower(self):
        #Arrange
        dummy_method = "blah"
        expected = "Blah"
        #Act
        actual = self.app.pay_method(dummy_method)
        #Assert
        self.assertEqual(expected, actual)
    
    def test_pay_method_upper(self):
        #Arrange
        dummy_method = "BLAH"
        expected = "Blah"
        #Act
        actual = self.app.pay_method(dummy_method)
        self.assertEqual(expected, actual)

    def test_pay_method_cap(self):
        #Arrange
        dummy_method = "Blah"
        expected = "Blah"
        #Act
        actual = self.app.pay_method(dummy_method)
        #Assert
        self.assertEqual(expected, actual)
        
    # def test_card_masker_long(self):
    #     expected_outcome = "****5678"
    #     mock_ccn = "12345678"
    #     actual_outcome = self.app.card_masker(mock_ccn)
    #     self.assertEqual(expected_outcome, actual_outcome)
        
    # def test_card_masker_short(self):
    #     expected_outcome = "1234"
    #     mock_ccn = "1234"
    #     actual_outcome = self.app.card_masker(mock_ccn)
    #     self.assertEqual(expected_outcome, actual_outcome)

    # def test_card_masker_null(self):
    #     expected_outcome = None
    #     mock_ccn = None
    #     actual_outcome = self.app.card_masker(mock_ccn)
    #     self.assertEqual(expected_outcome, actual_outcome)

    def test_person_breaker(self):
        expected_outcome = ("Gary", "McTest")
        mock_name = "Gary McTest"
        actual_outcome = self.app.person_breaker(mock_name)
        self.assertEqual(actual_outcome, expected_outcome)

    def test_person_breaker_no_last(self):
        expected_outcome = ("Gary", "")
        mock_name = "Gary "
        actual_outcome = self.app.person_breaker(mock_name)
        self.assertEqual(actual_outcome, expected_outcome)

    # def test_get_drink_list(self):
    #     mock_drink_dict = {}
    #     mock_raw_orders = ["Frappes - Chocolate Cookie: 2.90", "Americano", "Herbal Tea: 1.40", "Americano: 1.40"]
    #     expected = {"Frappes - Chocolate Cookie": 290, "Americano": 140, "Herbal Tea": 140}
    #     actual = self.app.get_drink_list(mock_raw_orders, mock_drink_dict)
    #     self.assertEqual(actual, expected)
    

    def test_date_breaker(self):
        expected = (datetime.date(2020,5,19),datetime.time(11,11,11))
        actual = self.app.date_breaker(datetime.datetime(2020,5,19,11,11,11))
        self.assertEqual(expected,actual)

    def test_csv_date_breaker(self):
        expected = ("2020,5,19", "11,11,11")
        actual = self.app.csv_date_breaker(("2020,5,19 11,11,11"))
        self.assertEqual(expected,actual)


    @patch("transform.Transform.date_breaker", return_value=unittest.mock)
    @patch("transform.Transform.person_breaker", return_value=unittest.mock)
    @patch("transform.Transform.drink_breaker", return_value=unittest.mock)
    @patch("transform.Transform.pay_method", return_value=unittest.mock)
    @patch("transform.Transform.id_generator", return_value=unittest.mock)
    @patch("transform.Transform.get_id", return_value=unittest.mock)
    def test_transform(self, mock_location_id, mock_id_generator, mock_pay_method, mock_drink_breaker, mock_person_breaker, mock_date_breaker):
        mock_transformed_data = []
        mock_person_breaker.return_value = "Oscar", "Ohara"
        mock_date_breaker.return_value = datetime.date(2020, 5, 18), datetime.time(15, 46, 1)
        mock_location_id.return_value = 1
        mock_drink_breaker.return_value = "Frappes - Chocolate Cookie"
        mock_price = "2.75"
        mock_pay_method.return_value = "CASH"
        mock_id_generator.return_value = 1
        mock_entry = [[1, datetime.datetime(2020, 5, 18, 15, 46, 1), "Isle of Wight", 'Oscar Ohara', 'Frappes - Chocolate Cookie', 2.75, 'CASH', None]]
        expected = ([[1, datetime.date(2020, 5, 18), datetime.time(15, 46, 1), 1, 'Oscar', 'Ohara', 275, 'CASH']],{},{},{1: [1]})
        actual = self.app.transform(mock_entry)
        self.assertEqual(actual, expected)

    def test_get_id_drink(self):
        #arrange
        data = ('Speciality Tea', 'N/A', 'English breakfast')
        expected_outcome = 1
        #act
        actual_outcome = self.app.get_id(data)
        #assert
        self.assertEqual(expected_outcome, actual_outcome)

    def test_get_id_location(self):
        #arrange
        mock_location_dict = {('Chesterfield'): 10}
        self.id.load_ids("locations").return_value = mock_location_dict
        data = ('Chesterfield')
        expected_outcome = 1004
        #act
        actual_outcome = self.app.get_id(data)
        #assert
        self.assertEqual(expected_outcome, actual_outcome)

    def test_get_split_drink_no_flavour(self):
    #     mock_drink = 'Large Espresso: 1.8', 'Frappes - Coffee: 2.75', 'Large Espresso: 1.8', 'Frappes - Chocolate Cookie: 2.75']
        mock_raw_drink = 'Large Espresso: 1.8'
        expected_outcome = ('Espresso', 'Large', 'Original', 180)
        # , 'Frappes - Coffee: 2.75', 'Large Espresso: 1.8', 'Frappes - Chocolate Cookie: 2.75'])
        actual_outcome = self.app.get_split_drink(mock_raw_drink)
        self.assertEqual(expected_outcome, actual_outcome)

    def test_get_split_drink_flavour(self):
    #     mock_drink = 'Large Espresso: 1.8', 'Frappes - Coffee: 2.75', 'Large Espresso: 1.8', 'Frappes - Chocolate Cookie: 2.75']
        mock_raw_drink = 'Frappes - Coffee: 2.75'
        expected_outcome = ('Frappes', 'N/A', 'Coffee', 275)
        # , 'Frappes - Coffee: 2.75', 'Large Espresso: 1.8', 'Frappes - Chocolate Cookie: 2.75'])
        actual_outcome = self.app.get_split_drink(mock_raw_drink)
        self.assertEqual(expected_outcome, actual_outcome)
    
    def test_item_adder(self): 
        mock_item_dict = {'apple': 2, 'orange': 3, 'grapes': 4}
        nothing = "0"
        expected_outcome = 5
        actual_outcome = self.app.item_adder(nothing ,mock_item_dict)
        self.assertEqual(expected_outcome, actual_outcome)

    def test_location_adder(self):
        mock_location_list = ["Uppingham", "Oakham"]
        mock_location = "Lyddington"
        expected_outcome = ["Uppingham", "Oakham", "Lyddington"]
        actual_outcome = self.app.location_adder(mock_location, mock_location_list)
        self.assertEqual(expected_outcome, actual_outcome)

    def test_drink_name_size_breaker_large(self):
        mock_drink = "Large Espresso"
        expected_outcome = "Large", "Espresso"
        actual_outcome = self.app.drink_name_size_breaker(mock_drink)
        self.assertEqual(expected_outcome, actual_outcome)

    def test_drink_name_size_breaker_regular(self):
        mock_drink = "Regular Espresso"
        expected_outcome = "Regular", "Espresso"
        actual_outcome = self.app.drink_name_size_breaker(mock_drink)
        self.assertEqual(expected_outcome, actual_outcome)

    def test_drink_name_size_breaker_none(self):
        mock_drink = "Espresso"
        expected_outcome = "N/A", "Espresso"
        actual_outcome = self.app.drink_name_size_breaker(mock_drink)
        self.assertEqual(expected_outcome, actual_outcome)

    def test_get_price_and_flavour_with_price(self):
        mock_drink = "large americano, hazlenut: 1.40"
        expected_outcome = "large americano, hazlenut", "Original", 140
        actual_outcome = self.app.get_price_and_flavour(mock_drink)
        self.assertEqual(expected_outcome, actual_outcome)

    def test_get_price_and_flavour_without_price(self):
        mock_drink = "large americano, hazlenut"
        expected_outcome = "large americano, hazlenut", "Original", 0
        actual_outcome = self.app.get_price_and_flavour(mock_drink)
        self.assertEqual(expected_outcome, actual_outcome)




    
    



if __name__ == '__main__':
    unittest.main()