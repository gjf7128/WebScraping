import unittest
from library.patron import *

class TestPatron(unittest.TestCase):
    def test_constructor(self):
        # Expected Values
        expected_fname = "Johanthon"
        expected_lname = "Johnson"
        expected_age = 20
        expected_id = 100001
        patron = Patron(expected_fname, expected_lname, expected_age, expected_id)

        # Actual Values
        actual_fname = patron.fname
        actual_lname = patron.lname
        actual_age = patron.age
        actual_id = patron.memberID

        # Asserts   
        self.assertEqual(actual_fname, expected_fname)
        self.assertEqual(actual_lname, expected_lname)
        self.assertEqual(actual_age, expected_age)
        self.assertEqual(actual_id, expected_id)

    @unittest.expectedFailure
    def test_constructor_fname_fails(self):
        # Expected Values
        expected_fname = "Johanth0n"
        expected_lname = "Johnson"
        expected_age = 20
        expected_id = 100001
        
        patron = Patron(expected_fname, expected_lname, expected_age, expected_id)

    @unittest.expectedFailure
    def test_constructor_lname_fails(self):
        # Expected Values
        expected_fname = "Johanthon"
        expected_lname = "J0hnson"
        expected_age = 20
        expected_id = 100001
        
        patron = Patron(expected_fname, expected_lname, expected_age, expected_id)




if __name__ == '__main__':
    unittest.main()
