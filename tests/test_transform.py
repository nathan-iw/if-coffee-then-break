import unittest
from transform import Transform
from unittest.mock import Mock, patch, call, MagicMock
import time
import datetime


class TransformTests(unittest.TestCase):

    def setUp(self):
        self.app = Transform()
        
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
        
    def test_card_masker_long(self):
        expected_outcome = "****5678"
        mock_ccn = "12345678"
        actual_outcome = self.app.card_masker(mock_ccn)
        self.assertEqual(expected_outcome, actual_outcome)
        
    def test_card_masker_short(self):
        expected_outcome = "1234"
        mock_ccn = "1234"
        actual_outcome = self.app.card_masker(mock_ccn)
        self.assertEqual(expected_outcome, actual_outcome)

    def test_card_masker_null(self):
        expected_outcome = None
        mock_ccn = None
        actual_outcome = self.app.card_masker(mock_ccn)
        self.assertEqual(expected_outcome, actual_outcome)

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

    def test_get_drink_list(self):
        mock_drink_dict = {}
        mock_raw_orders = ["Frappes - Chocolate Cookie: 2.90", "Americano", "Herbal Tea: 1.40", "Americano: 1.40"]
        expected = {"Frappes - Chocolate Cookie": "2.90", "Americano": "1.40", "Herbal Tea": "1.40" }
        actual = self.app.get_drink_list(mock_raw_orders, mock_drink_dict)
        self.assertEqual(actual, expected)
    

    def test_date_breaker(self):
        # mock_date_time.return_value = "2020-05-19 16:25.33" 
        expected = (datetime.date(2020,5,19),datetime.time(11,11,11))
        actual = self.app.date_breaker(datetime.datetime(2020,5,19,11,11,11))
        self.assertEqual(expected,actual)

# , mock_card_masker, mock_pay_method, mock_drink_breaker, mock_person_breaker, 
    @patch("transform.Transform.date_breaker", return_value=unittest.mock)
    @patch("transform.Transform.person_breaker", return_value=unittest.mock)
    @patch("transform.Transform.drink_breaker", return_value=unittest.mock)
    @patch("transform.Transform.pay_method", return_value=unittest.mock)
    @patch("transform.Transform.card_masker", return_value=unittest.mock)
    def test_transform(self, mock_card_masker, mock_pay_method, mock_drink_breaker, mock_person_breaker, mock_date_breaker):
        mock_transformed_data = []
        mock_person_breaker.return_value = "Oscar", "Ohara"
        mock_date_breaker.return_value = datetime.date(2020, 5, 18), datetime.time(15, 46, 1)
        mock_location = "Isle of Wight"
        mock_drink_breaker.return_value = "Frappes - Chocolate Cookie"
        mock_price = "2.75"
        mock_pay_method.return_value = "CASH"
        mock_card_masker.return_value = None
        mock_entry = [(633, datetime.datetime(2020, 5, 18, 15, 46, 1), 'Isle of Wight', 'Oscar Ohara', ' Frappes - Chocolate Cookie', 2.75, 'CASH', None)]
        expected = [[datetime.date(2020, 5, 18), datetime.time(15, 46, 1), 'Isle of Wight', 'Oscar', 'Ohara', 'Frappes - Chocolate Cookie', 2.75, 'CASH', None]]
        actual = self.app.transform(mock_entry)
        self.assertEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()