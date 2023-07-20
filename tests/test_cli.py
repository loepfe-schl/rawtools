# -*- coding: utf-8 -*-

"""
test command-line tool
"""

import unittest
from rawtools import cli


class Test_CLI(unittest.TestCase):
    """Test CLI"""

    def setUp(self):
        """Code that will be run before each test in this class"""
        pass

    def test_system_exit(self):
        try:
            cli.main()
        except SystemExit:
            pass
        else:
            self.fail('Expected System Exit')


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    unittest.main()
