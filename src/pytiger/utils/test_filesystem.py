import unittest
import os
from mock import patch
from filesystem import get_file_age, touch

@unittest.skip('expected failures')
class Testget_file_age(unittest.TestCase):

    def test_run_without_filename(self):
        self.assertRaises(TypeError, get_file_age())

    def test_run_incorrect_filename(self):
        self.assertRaises(TypeError, get_file_age('////'))
        self.assertRaises(TypeError, get_file_age(''))

    def test_run_incorrect_timestamp(self):
        pass

    def test_run_future_timestamp(self):
        pass

    def test_run_unowned_location(self):
        pass
    

    def test_run_correct_timestamp(self):
        pass

