import unittest
from transform import Transform
from unittest.mock import Mock, patch, call, MagicMock


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


if __name__ == '__main__':
    unittest.main()