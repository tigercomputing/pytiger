import unittest
import os
from mock import patch
from .filesystem import get_file_age, touch
from tempfile import mkdtemp, mkstemp
from shutil import rmtree


class Test_get_file_age(unittest.TestCase):

    def setUp(self):
        self.tempfile, self.tempfile_name = mkstemp()

    def tearDown(self):
        try:
            os.remove(self.tempfile_name)
        except OSError:  # pragma: no cover
            pass

    def test_without_filename(self):
        self.assertRaises(TypeError, get_file_age)

    def test_invalid_filename(self):
        self.assertRaises(OSError, get_file_age, '')

    @patch('time.time')
    def test_age(self, stable_time):
        touch(self.tempfile_name, timestamp=100)
        stable_time.return_value = 150
        self.assertEqual(get_file_age(self.tempfile_name), 50)


class Test_touch(unittest.TestCase):

    def setUp(self):
        self.tempdir = mkdtemp()

    def tearDown(self):
        rmtree(self.tempdir)

    def test_create_single_file(self):
        """Create a file"""
        test_file_name = self.tempdir+'test_file'
        touch(test_file_name)
        self.assertTrue(os.path.isfile(test_file_name))

    def test_fail_on_no_dirs(self):
        """Raise exception without create_dirs"""
        # Deliberately call touch() with a nested file
        # but not create_dirs
        # We should get an exception
        test_file_name = self.tempdir+'/test_dir/test_file'
        self.assertRaises(IOError, touch, test_file_name)

    def test_create_file_in_new_dir(self):
        """Create a file in a directory with create_dirs"""
        test_file_name = self.tempdir+'/test_dir/test_file'
        touch(test_file_name, create_dirs=True)
        self.assertTrue(os.path.isfile(test_file_name))

    def test_create_file_in_existing_dir(self):
        test_file_name = self.tempdir+'/test_dir/test_file'
        os.makedirs(self.tempdir+'/test_dir')
        touch(test_file_name, create_dirs=True)
        self.assertTrue(os.path.isfile(test_file_name))

    def test_set_timestamp(self):
        """Set a file timestamp"""
        test_file_name = self.tempdir+'test_file'
        stamp = 100
        touch(test_file_name, timestamp=stamp)
        s = os.stat(test_file_name)
        self.assertEqual(stamp, s.st_atime)
        self.assertEqual(stamp, s.st_mtime)
