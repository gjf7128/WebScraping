import unittest
from unittest.mock import MagicMock
from PythonMocking.library.library_db_interface import Library_DB


class TestLibraryDbInterface(unittest.TestCase):
    def test_constructor(self):
        library_db_interface = Library_DB()
        self.assertIsNotNone(library_db_interface)

    def test_get_patron_count(self):
        library_db = Library_DB()
        mock = MagicMock(return_value=[{'fname': 'jeff', 'lname': 'smith', 'age': 20, 'memberID': 1}])
        library_db.db.all = mock
        actual = library_db.get_patron_count()

        self.assertEqual(actual, 1)
        mock.assert_called()

    def test_insert_patron(self):
        library_db = Library_DB()
        patron_mock = MagicMock(return_value=[{'fname': 'jeff', 'lname': 'smith', 'age': 20, 'memberID': 1, 'borrowed_books': []}])
        result_mock = MagicMock(return_value=1)
        library_db.db.insert = result_mock
        actual = library_db.insert_patron(patron_mock)

        self.assertEqual(actual, 1)
        result_mock.assert_called()

    def test_insert_patron_already_in_db(self):
        library_db = Library_DB()
        retrieve_patron_mock = MagicMock(return_value=[{'fname': 'jeff', 'lname': 'smith', 'age': 20, 'memberID': 1}])
        library_db.retrieve_patron = retrieve_patron_mock

        self.assertIsNone(library_db.insert_patron(retrieve_patron_mock))

    def test_get_all_patrons(self):
        library_db = Library_DB()
        mock = MagicMock(return_value=[{'fname': 'jeff', 'lname': 'smith', 'age': 20, 'memberID': 1}])
        library_db.db.all = mock

        actual = library_db.get_all_patrons()
        self.assertEqual(actual, mock.return_value)

    def test_update_patron(self):
        library_db = Library_DB()
        data_mock = MagicMock(return_value=[{'fname': 'jeff', 'lname': 'smith', 'age': 20, 'memberID': 1, 'borrowed_books': []}])
        library_db.convert_patron_to_db_format = data_mock

        db_mock = MagicMock(return_value=None)
        library_db.db.update = db_mock

        actual = library_db.update_patron(db_mock)
        data_mock.assert_called()
        db_mock.assert_called()
        self.assertIsNone(actual)

    def test_retrieve_patron(self):
        library_db = Library_DB()
        results_mock = MagicMock(return_value=[{'fname': 'jeff', 'lname': 'smith', 'age': 20, 'memberID': 1, 'borrowed_books': []}])
        library_db.db.search = results_mock
        actual = library_db.retrieve_patron(1)
        print(actual)
        print(results_mock.return_value)

        self.assertEqual(actual.__dict__, results_mock.return_value[0])

    def test_close_db(self):
        library_db = Library_DB()
        mock = MagicMock(return_value=None)
        library_db.db.close = mock
        actual = library_db.close_db()

        self.assertEqual(actual, mock.return_value)
        mock.assert_called()

    # Been spending hours on this and I can't figure this out without creating a Patron Object.
    # We aren't allowed to use modules not within the module we are testing :(
    # Therefor I don't know what to use for the 'actual' variable.
    def test_convert_patron_to_db_format(self):
        library_db = Library_DB()
        mock = MagicMock(return_value={'fname': 'jeff', 'lname': 'smith', 'age': 20, 'memberID': 1, 'borrowed_books': []})

        # fname_mock = MagicMock()
        # lname_mock = MagicMock()
        # age_mock = MagicMock()
        # memberID_mock = MagicMock()
        # borrowed_mock = MagicMock()
        #
        # mock.fname_mock = fname_mock
        # mock.lname_mock = lname_mock
        # mock.age_mock = age_mock
        # mock.memberID_mock = memberID_mock
        # mock.borrowed_mcok = borrowed_mock

        actual = library_db.convert_patron_to_db_format(mock)

        self.assertEqual(mock.return_value, actual.items())
        # fname_mock.assert_called()



if __name__ == '__main__':
    unittest.main()
