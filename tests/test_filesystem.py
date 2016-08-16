#!/usr/bin/env python

import collections
import os
import unittest

from cohesion import filesystem

from pyfakefs import fake_filesystem_unittest


CONTENTS = """
class Cls(object):
    pass
"""


class TestFilesystem(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def tearDown(self):
        # It is no longer necessary to add self.tearDownPyfakefs()
        pass

    def assertCountEqual(self, first, second):
        """
        Test whether two sequences contain the same elements.

        This exists in Python 3, but not Python 2.
        """
        self.assertEqual(
            collections.Counter(list(first)),
            collections.Counter(list(second))
        )

    def test_get_file_contents(self):
        filename = os.path.join("directory", "filename.py")

        self.fs.CreateFile(
            filename,
            contents=CONTENTS
        )
        result = filesystem.get_file_contents(filename)

        self.assertEqual(result, CONTENTS)

    def test_recursively_get_files_from_directory(self):
        filenames = [
            os.path.join(".", "filename.txt"),
            os.path.join("directory", "inner_file.txt"),
            os.path.join("directory", "nested", "deep_file.py"),
        ]

        for filename in filenames:
            self.fs.CreateFile(filename, contents='')

        result = filesystem.recursively_get_files_from_directory('.')

        self.assertCountEqual(result, filenames)

    def test_recursively_get_python_files_from_directory(self):
        filenames = [
            os.path.join(".", "filename.txt"),
            os.path.join(".", "upper.py"),
            os.path.join("directory", "inner_file.txt"),
            os.path.join("directory", "nested", "deep_file.py"),
        ]

        for filename in filenames:
            self.fs.CreateFile(filename, contents='')

        result = filesystem.recursively_get_python_files_from_directory('.')
        expected = [
            os.path.join(".", "upper.py"),
            os.path.join("directory", "nested", "deep_file.py"),
        ]

        self.assertCountEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
