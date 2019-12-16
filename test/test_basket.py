import unittest

from python.Basket import Basket
from python.Inventory import Inventory
from python.Item import Item


# Define some test items
beans = Item("beans", 1.0, "canned")
spaghettiHoops = Item("spaghetti hoops", 1.5, "canned")
chickpeas = Item("chickpeas", 0.75, "canned")
peas = Item("peas", 1.5, "frozen")
potatoWaffles = Item("potato waffles", 2.5, "frozen")
iceCream = Item("ice cream", 4.0, "frozen")

items = (beans, spaghettiHoops, chickpeas, peas, potatoWaffles, iceCream)


class _BaseTestCase(unittest.TestCase):
    """
    Base class for Basket test cases.

    Creates an inventory from the items defined in this module, and provides a
    method for creating a basket.
    """

    @classmethod
    def setUpClass(cls):
        cls._inventory = Inventory()
        cls._inventory.addItems(items)

    def createBasket(self):
        return Basket(self.__class__._inventory)


class TestSimpleBasket(_BaseTestCase):

    def test_emptyBasket(self):
        """ Test that an empty basket costs nothing. """
        basket = self.createBasket()
        self.assertEqual(basket.total(), 0.0)
        self.assertEqual(basket.savings(), 0.0)

    def test_copyBasket(self):
        """ Test that we can copy one basket to another. """
        basket1 = self.createBasket()
        basket1.addItem("beans")
        basket1.addItem("spaghetti hoops")

        basket2 = self.createBasket()
        basket2.copyFrom(basket1)

        self.assertEqual(basket1.total(), basket2.total())
        self.assertEqual(basket2.total(), beans.price() + spaghettiHoops.price())
        self.assertEqual(basket1.savings(), basket2.savings())

    def test_badItem(self):
        """ Test that adding a bad item raises an exception. """
        basket = self.createBasket()
        with self.assertRaises(KeyError):
            basket.addItem("ferrari")

    def test_singleItem(self):
        """ Test that adding a single item produces the expected total. """
        basket = self.createBasket()
        basket.addItem("beans")
        self.assertEqual(basket.total(), beans.price())
        self.assertEqual(basket.numItems(), 1)

    def test_twoItems(self):
        """ Test that adding two items produces the expected total. """
        basket = self.createBasket()
        basket.addItem("beans")
        basket.addItem("spaghetti hoops")
        self.assertEqual(basket.total(), beans.price() + spaghettiHoops.price())
        self.assertEqual(basket.numItems(), 2)

    def test_threeItemsNoOffer(self):
        """ Test that adding three items which aren't in an offer produces the expected total. """
        basket = self.createBasket()
        basket.addItem("beans")
        basket.addItem("spaghetti hoops")
        basket.addItem("ice cream")
        self.assertEqual(basket.total(), beans.price() + spaghettiHoops.price() + iceCream.price())
        self.assertEqual(basket.numItems(), 3)


class TestThreeForTwoBasket(_BaseTestCase):

    def test_threeItems(self):
        """ Test that three of the same item costs the same as two. """
        basket1 = self.createBasket()
        basket2 = self.createBasket()

        basket1.addItem("beans")
        basket1.addItem("beans")
        basket1.addItem("beans")

        basket2.addItem("beans")
        basket2.addItem("beans")

        self.assertEqual(basket1.total(), 2 * beans.price())
        self.assertEqual(basket1.total(), basket2.total())
        self.assertEqual(basket1.savings(), beans.price())
        self.assertEqual(basket2.savings(), 0.0)

    def test_fourItems(self):
        """ Test that four of the same item costs the same as three. """
        basket = self.createBasket()

        basket.addItem("beans")
        basket.addItem("beans")
        basket.addItem("beans")
        basket.addItem("beans")

        self.assertEqual(basket.total(), 3 * beans.price())
        self.assertEqual(basket.savings(), beans.price())
        self.assertEqual(basket.numItems(), 4)

    def test_loadsOfItems(self):
        """ Test that the offer is applied correctly to loads of the same item. """
        basket = self.createBasket()

        numBeans = 302
        for x in xrange(numBeans):
            basket.addItem("beans")

        # Work out how many tins of beans we expect to be charged for
        expectedPrice = 2 * (numBeans / 3) + numBeans % 3
        expectedSavings = numBeans / 3

        self.assertEqual(basket.total(), expectedPrice * beans.price())
        self.assertEqual(basket.savings(), expectedSavings * beans.price())
        self.assertEqual(basket.numItems(), numBeans)


class TestCheapestFreeBasket(_BaseTestCase):

    def test_threeItems(self):
        """ Test that the cheapest of three items in the same promo group is free. """
        basket = self.createBasket()
        basket.addItem("beans")
        basket.addItem("spaghetti hoops")
        basket.addItem("chickpeas")

        # Chickpeas are cheapest so should be free
        self.assertEqual(basket.total(), beans.price() + spaghettiHoops.price())
        self.assertEqual(basket.savings(), chickpeas.price())
        self.assertEqual(basket.numItems(), 3)

    def test_fourItems(self):
        """ Test that the "cheapest free" promo still works as expected with four items. """
        basket = self.createBasket()

        basket.addItem("peas")
        basket.addItem("potato waffles")
        basket.addItem("ice cream")
        basket.addItem("peas")

        # One of the peas should be free
        self.assertEqual(basket.total(), peas.price() + potatoWaffles.price() + iceCream.price())
        self.assertEqual(basket.savings(), peas.price())
        self.assertEqual(basket.numItems(), 4)

    def test_multipleDeals(self):
        """ Test that two "cheapest free" promos work as expected. """
        basket = self.createBasket()

        # Add two of each frozen item
        for x in xrange(2):
            basket.addItem("peas")
            basket.addItem("potato waffles")
            basket.addItem("ice cream")

        # By our generous lgoic, we should try and give as big a discount as
        # possible, so there should be one free potato waffle and one free peas
        self.assertEqual(basket.total(), 2 * iceCream.price() + potatoWaffles.price() + peas.price())
        self.assertEqual(basket.savings(), potatoWaffles.price() + peas.price())


class TestComboBasket(_BaseTestCase):

    def test_threeForTwoWins(self):
        """ Test that a three-for-two offer beats a cheapest free offer. """
        basket = self.createBasket()
        basket.addItem("beans")
        basket.addItem("spaghetti hoops")
        basket.addItem("spaghetti hoops")
        basket.addItem("spaghetti hoops")

        # Check that the spaghetti hoops were free
        self.assertEqual(basket.total(), 2 * spaghettiHoops.price() + beans.price())
        self.assertEqual(basket.savings(), spaghettiHoops.price())

    def test_bothOffers(self):
        """ Test that a combination of the two offers is computed correctly. """
        basket = self.createBasket()

        basket.addItem("beans")
        basket.addItem("beans")
        basket.addItem("beans")
        basket.addItem("chickpeas")
        basket.addItem("chickpeas")
        basket.addItem("spaghetti hoops")

        # Basket contains one of each offer
        self.assertEqual(basket.total(), 2 * beans.price() + chickpeas.price() + spaghettiHoops.price())
        self.assertEqual(basket.savings(), beans.price() + chickpeas.price())

    def test_dontCountItemsInMultipleOffers(self):
        """ Test that items aren't counted for more than one offer. """
        basket = self.createBasket()

        basket.addItem("beans")
        basket.addItem("beans")
        basket.addItem("beans")
        basket.addItem("chickpeas")
        basket.addItem("spaghetti hoops")

        # Three-for-two should win, so no cheapest-free savings should happen here
        self.assertEqual(basket.total(), 2 * beans.price() + chickpeas.price() + spaghettiHoops.price())
        self.assertEqual(basket.savings(), beans.price())


if __name__ == '__main__':
    unittest.main()
