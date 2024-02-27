import unittest
from unittest.mock import MagicMock

from library import *


class TestLibrary(unittest.TestCase):
    def test_constructor(self):
        library = Library()
        self.assertIsNotNone(library)

    def test_is_ebook_true(self):
        library = Library()
        mock = MagicMock(return_value=[{'title': 'true', 'ebook_count': 2}])
        library.api.get_ebooks = mock

        actual = library.is_ebook("True")
        self.assertTrue(actual)
        mock.assert_called()

    def test_is_ebook_false(self):
        library = Library()
        mock = MagicMock(return_value=[{'title': 'true', 'ebook_count': 2}])
        library.api.get_ebooks = mock

        actual = library.is_ebook("False")
        self.assertFalse(actual)
        mock.assert_called()

    def test_get_ebook_count(self):
        library = Library()
        mock = MagicMock(return_value=[{'title': 'true', 'ebook_count': 2}])
        library.api.get_ebooks = mock

        actual = library.get_ebooks_count("True")
        expected = 2
        self.assertEqual(actual, expected)
        mock.assert_called()

    def test_get_books_by_author_true(self):
        library = Library()
        mock = MagicMock(return_value=["true", "indeed", "certainly"])
        library.api.books_by_author = mock

        actual = library.is_book_by_author("steven", "true")
        self.assertTrue(actual)
        mock.assert_called()

    def test_get_books_by_author_false(self):
        library = Library()
        mock = MagicMock(return_value=["true", "indeed", "certainly"])
        library.api.books_by_author = mock

        actual = library.is_book_by_author("steven", "false")
        self.assertFalse(actual)
        mock.assert_called()

    def test_get_book_languages(self):
        library = Library()
        book_info = [{"language" : "E"}, {"language" : "S"}, {"language" : "F"}]
        mock = MagicMock(return_value=book_info)
        library.api.get_book_info = mock

        actual = library.get_languages_for_book("test")
        expected = {"E", "S", "F"}

        self.assertSetEqual(actual, expected)
        mock.assert_called_once_with("test")

    def test_add_patron(self):
        library = Library()
        mock = MagicMock(return_value=1001)
        library.db.insert_patron = mock
        actual = library.register_patron("John", "Johnson", 42, 1001)
        expected = 1001

        self.assertEqual(expected, actual)
        mock.assert_called_once()

    def test_patron_registered_true(self):
        library = Library()
        mock = MagicMock(return_value=True)
        library.db.retrieve_patron = mock
        patron = MagicMock()
        actual = library.is_patron_registered(patron)

        self.assertTrue(actual)
        mock.assert_called_once()

    def test_patron_registered_false(self):
        library = Library()
        mock = MagicMock(return_value=False)
        library.db.retrieve_patron = mock
        patron = MagicMock()
        actual = library.is_patron_registered(patron)

        self.assertFalse(actual)
        mock.assert_called_once()

    def test_borrow_book(self):
        library = Library()
        patron = MagicMock()
        mock = MagicMock()
        library.db.update_patron = mock

        library.borrow_book("The Odyssey", patron)

        mock.assert_called_once_with(patron)

    def test_return_book(self):
        library = Library()
        patron = MagicMock()
        mock = MagicMock()
        library.db.update_patron = mock

        library.return_borrowed_book("The Odyssey", patron)

        mock.assert_called_once_with(patron)

    def test_patron_borrowed_book_true(self):
        library = Library()
        patron_mock = MagicMock()
        method_mock = MagicMock(return_value={"the odyssey"})
        patron_mock.get_borrowed_books = method_mock
        actual = library.is_book_borrowed("the odyssey", patron_mock)

        self.assertTrue(actual)



if __name__ == '__main__':
    unittest.main()
