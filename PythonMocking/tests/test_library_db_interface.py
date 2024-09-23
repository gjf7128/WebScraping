import unittest
from unittest.mock import MagicMock, patch
# from PythonMocking.library.library_db_interface import Library_DB
from library.library_db_interface import Library_DB
from library.patron import Patron


class TestLibraryDbInterface(unittest.TestCase):
    def test_constructor(self):
        library_db_interface = Library_DB()
        self.assertIsNotNone(library_db_interface)
        self.assertEqual(library_db_interface.DATABASE_FILE, 'db.json')

    def test_get_patron_count(self):
        library_db = Library_DB()
        mock = MagicMock(return_value=[{'fname': 'jeff', 'lname': 'smith', 'age': 20, 'memberID': 1}])
        library_db.db.all = mock
        actual = library_db.get_patron_count()

        self.assertEqual(actual, 1)
        mock.assert_called()

    def test_insert_patron(self):
        library_db = Library_DB()
        patron_mock = MagicMock(return_value=[{'fname': 'jeff', 'lname': 'smith', 'age': 20,
                                               'memberID': 1, 'borrowed_books': []}])
        result_mock = MagicMock(return_value=1)
        library_db.db.insert = result_mock
        data_mock = MagicMock(return_value=patron_mock.return_value)
        library_db.convert_patron_to_db_format = data_mock
        actual = library_db.insert_patron(patron_mock)

        self.assertEqual(actual, 1)
        result_mock.assert_called()
        data_mock.assert_called()

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
        data_mock = MagicMock(return_value=[{'fname': 'jeff', 'lname': 'smith',
                                             'age': 20, 'memberID': 1, 'borrowed_books': []}])
        library_db.convert_patron_to_db_format = data_mock

        db_mock = MagicMock(return_value=None)
        library_db.db.update = db_mock

        actual = library_db.update_patron(db_mock)
        data_mock.assert_called()
        db_mock.assert_called()
        self.assertIsNone(actual)

    def test_retrieve_patron(self):
        # I tried to kill the mutant: results = self.db.search(query.memberID != memberID)
        # by I guess ensuring that results was of size 1, but MagicMock forces a return value of what
        # I want anyways... I am so incredibly confused on this whole mutations testing assignment.
        library_db = Library_DB()
        results_mock = MagicMock(return_value=[{'fname': 'jeff', 'lname': 'smith', 'age': 20, 'memberID': 1, 'borrowed_books': []}])
        library_db.db.search = results_mock
        actual = library_db.retrieve_patron(1)

        self.assertEqual(actual.__dict__, results_mock.return_value[0])
        self.assertEqual(actual.__dict__['fname'], 'jeff')
        self.assertEqual(len(results_mock.return_value), 1)

    def test_close_db(self):
        library_db = Library_DB()
        mock = MagicMock(return_value=None)
        library_db.db.close = mock
        actual = library_db.close_db()

        self.assertEqual(actual, mock.return_value)
        mock.assert_called()

    def test_convert_patron_to_db_format(self):
        library_db = Library_DB()

        patron_mock = MagicMock()

        patron_mock.get_fname = MagicMock(return_value='jeff')
        patron_mock.get_lname = MagicMock(return_value='smith')
        patron_mock.get_age = MagicMock(return_value=20)
        patron_mock.get_memberID = MagicMock(return_value=1)
        patron_mock.get_borrowed_books = MagicMock(return_value=[])

        actual = library_db.convert_patron_to_db_format(patron_mock)

        self.assertEqual(actual['fname'], 'jeff')
        self.assertEqual(actual['lname'], 'smith')
        self.assertEqual(actual['age'], 20)
        self.assertEqual(actual['memberID'], 1)
        self.assertEqual(actual['borrowed_books'], [])


if __name__ == '__main__':
    unittest.main()
