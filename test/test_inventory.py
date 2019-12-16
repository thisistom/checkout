import unittest
import os

from utils import captureOutput

from python.Inventory import Inventory
from python.Item import Item

# Define some test items
beans = Item("beans", 1.0, "canned")
beans2 = Item("beans", 2.0, "frozen")
chickpeas = Item("chickpeas", 0.75, "canned")

items = (beans, beans2, chickpeas)

# Get the path to this file, to find test resources
testDirectory = os.path.dirname(os.path.abspath(__file__))


class TestInventory(unittest.TestCase):

    def test_addItem(self):
        """ Test that we can add and retrieve an item. """
        inventory = Inventory()
        inventory.addItems((beans, chickpeas))

        item = inventory.getItem("beans")
        self.assertEqual(item, beans)

    def test_overwriteItem(self):
        """ Test that adding an item with a duplicate name silently overwrites the old item. """
        inventory = Inventory()
        inventory.addItems((beans, chickpeas))
        inventory.addItems((beans2, ))

        item = inventory.getItem("beans")
        self.assertEqual(item, beans2)
        self.assertNotEqual(item, beans)

    def test_readFromDisk(self):
        """ Test that we can read an inventory file from disk. """
        inventory = Inventory()
        inventory.readFromDisk(os.path.join(testDirectory, "resources", "testInventory.csv"))

        # Test a known item from the inventory on disk
        item = inventory.getItem("lettuce")
        testItem = Item("lettuce", 0.5, "vegetables")

        self.assertEqual(item, testItem)

    def test_readMissingInventory(self):
        """ Test that we can handle being given a missing inventory file. """
        inventory = Inventory()
        with self.assertRaises(IOError):
            inventory.readFromDisk("madeUpFile.csv")

    def test_readBadInventory(self):
        """ Test that we can handle reading bad inventory files from disk. """
        inventory = Inventory()

        # Test that an error is printed if the header row is wrong
        with captureOutput() as (out, err):
            inventory.readFromDisk(os.path.join(testDirectory, "resources", "badInventory1.csv"))

        output = out.getvalue().strip()
        self.assertIn('bad header row', output)

        # Test that errors are printed for malformed inventory entries
        with captureOutput() as (out, err):
            inventory.readFromDisk(os.path.join(testDirectory, "resources", "badInventory2.csv"))

        output = out.getvalue().strip()
        self.assertIn('bad inventory entry', output)
        self.assertIn('bad price for inventory entry', output)


if __name__ == '__main__':
    unittest.main()
