import unittest

from utils import captureOutput
from python.Item import Item

# Define some test items
beans = Item("beans", 1.0, "canned")
beans_same = Item("beans", 1.0, "canned")

beans_frozen = Item("beans", 1.0, "frozen")
beans_expensive = Item("beans", 10.0, "canned")
not_beans = Item("chickpeas", 1.0, "canned")


class TestItem(unittest.TestCase):

    def test_equality(self):
        """ Test that equality comparison between items works. """
        self.assertEqual(beans, beans_same)
        self.assertNotEqual(beans, beans_frozen)
        self.assertNotEqual(beans, beans_expensive)
        self.assertNotEqual(beans, not_beans)

    def test_repr(self):
        """ Test that string representations of items works. """
        beans_repr = repr(beans)

        self.assertIn("beans", beans_repr)
        self.assertIn("1.0", beans_repr)
        self.assertIn("canned", beans_repr)

if __name__ == '__main__':
    unittest.main()
