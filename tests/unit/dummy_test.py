"""tests/unit/dummy_test.py"""

import unittest

from protaskinate.utils.dummy import dummy


class TestDummy(unittest.TestCase):
    """Dummy test class"""

    def test_dummy(self):
        """Dummy test method"""
        self.assertTrue(dummy())
