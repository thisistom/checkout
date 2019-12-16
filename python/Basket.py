from collections import defaultdict

from Promos import (
    ThreeForTwoPromo,
    CheapestFreePromo
)

class BasketEntry(object):
    """
    Class representing a single entry in a basket - an item and a counter.
    """

    # Initializer -------------------------------------------------------------

    def __init__(self, item):
        """
        Initializes an instance of the class.

        Args:
            item (Item): The item which this basket entry represents.
        """
        self.__item = item
        self.__count = 0

    # Public Instance Methods -------------------------------------------------

    def increment(self, count=1):
        """
        Increments the count for this item by the given amount.

        Args:
            count (int): The number of instances of the item to add. (Default: 1)

        Raises:
            ValueError: If the given count is < 0.

        Returns:
            int. The new count.
        """
        if count < 0:
            raise ValueError("Count must be > 0")

        self.__count += count

        return self.__count

    def decrement(self, count=1):
        """
        Decrements the count for this item by the given amount.

        Args:
            count (int): The number of instances of the item to remove. (Default: 1)

        Raises:
            ValueError: If the given count is < 0, or if too many items are being removed.

        Returns:
            int. The new count.
        """
        if count < 0:
            raise ValueError("Count must be > 0 - got %r" % count)

        if count > self.__count:
            raise ValueError("Removing too many items - got %r, only have %r items"
                             % (count, self.__count))

        self.__count -= count

        return self.__count

    def item(self):
        """
        Returns:
            Item. The item for this basket entry.
        """
        return self.__item

    def count(self):
        """
        Returns:
            int. The count for this basket entry.
        """
        return self.__count


class Basket(object):
    """
    Class representing the contents of a basket.
    """

    # Initializer -------------------------------------------------------------

    def __init__(self, inventory):
        """
        Initializes an instance of the class.

        Args:
            inventory (Inventory): The inventory to use with this basket.
        """
        self.__inventory = inventory

        # Dictionary mapping item name -> BasketEntry
        self._entriesByName = {}

        # Dictionary mapping promo group -> set of item names
        self._itemsByPromoGroup = defaultdict(set)

        # Flag indicating whether the cost + savings need computing
        self.__dirty = False

        # The cost + savings once computed
        self.__total = 0.0
        self.__savings = 0.0
        self.__promos = []

    # Public Instance Methods -------------------------------------------------

    def addItem(self, itemName, count=1):
        """
        Adds an item to the basket.

        Args:
            itemName (str): The name of the item to add.
            count (int): The number of instances of the item to add. (Default: 1)

        Raises:
            KeyError: If the given item name isn't found in our inventory.
        """
        # Increment the number of this item in our dict of items
        entry = self._entriesByName.get(itemName)
        if entry is None:
            item = self.__inventory.getItem(itemName)
            if item is None:
                raise KeyError("Item %r not found in inventory" % itemName)

            entry = BasketEntry(item)
            self._entriesByName[itemName] = entry

        # Add this item to the set of items for its promo group
        item = entry.item()
        promoGroup = item.promoGroup()
        if promoGroup:
            self._itemsByPromoGroup[promoGroup].add(item.name())

        entry.increment(count)

        # Set the flag so that we know to recompute the cost of the basket
        self.__dirty = True

    def total(self):
        """
        Returns:
            float. The cost of the basket, taking offers into account.
        """
        if self.__dirty:
            self.__compute()

        return self.__total

    def savings(self):
        """
        Returns:
            float. The total savings in this basket from offers.
        """
        if self.__dirty:
            self.__compute()

        return self.__savings

    def promos(self):
        """
        Returns:
            list of _PromoEntry. The promotional offers in this basket.
        """
        if self.__dirty:
            self.__compute()

        return list(self.__promos)

    def numItems(self):
        """
        Returns:
            int. The number of items in this basket.
        """
        numItems = 0
        for entry in self._entriesByName.itervalues():
            count = entry.count()
            numItems += count

        return numItems

    def entries(self):
        """
        Returns:
            list of BasketEntry. A list of the entries in this basket.
        """
        return list(self._entriesByName.values())

    def clear(self):
        """
        Empties the basket.
        """
        self._entriesByName = {}
        self._itemsByPromoGroup = defaultdict(set)

        self.__dirty = True

    def copyFrom(self, other):
        """
        Copies the contents of the other basket to this basket.

        Args:
            other (Basket): The basket to copy to.
        """
        self.clear()
        for itemName, entry in other._entriesByName.iteritems():
            self.addItem(itemName, entry.count())

    # Private Instance Methods ------------------------------------------------

    def __compute(self):
        """
        Computes the cost + savings of the basket.
        """
        self.__total = 0.0
        self.__savings = 0.0
        self.__promos = []

        # Make a duplicate basket to save our state
        originalBasket = Basket(self.__inventory)
        originalBasket.copyFrom(self)

        # First look for three-for-twos
        self.__processThreeForTwos()

        # Then handle promo groups
        self.__processPromoGroups()

        # Then add whatever's left
        for itemName, entry in self._entriesByName.iteritems():
            item = entry.item()
            count = entry.count()
            self.__total += count * item.price()

        # Restore the original contents of the basket
        self.copyFrom(originalBasket)

        # Set the flag so that we don't recompute unless we need to
        self.__dirty = False

    def __processThreeForTwos(self):
        """
        Processes all three-for-two offers found in the basket, and removes the
        processed items.
        """
        for itemName, entry in self._entriesByName.iteritems():
            count = entry.count()
            numThreeForTwos = count / 3
            if numThreeForTwos > 0:
                item = entry.item()
                price = item.price()

                promo = ThreeForTwoPromo(item, numThreeForTwos)
                self.__promos.append(promo)

                self.__total += promo.cost()
                self.__savings += promo.savings()

                # Take 3 off the counter for this entry
                entry.decrement(numThreeForTwos * 3)

    def __processPromoGroups(self):
        """
        Processes all promo group offers found in the basket, and removes the
        processed items.
        """
        for promoGroup, itemNames in self._itemsByPromoGroup.iteritems():
            # Build a list of entries for this promo group
            entries = []
            numItems = 0
            for itemName in itemNames:
                entry = self._entriesByName.get(itemName)
                if entry.count() > 0:
                    entries.append(entry)
                    numItems += entry.count()

            while numItems >= 3:
                # Sort the entries by increasing price of the item
                entries.sort(key=lambda entry: entry.item().price())

                # Take the last three items from the end - we charge for the
                # first two, and give the third for free.

                # NOTE: this is where we could be stingy if we wanted to, and
                # charge for the most expensive + give the cheapest for free.
                # Instead we're being nice and giving the best discount we can.
                items = []
                for x in xrange(3):
                    lastEntry = entries[-1]
                    items.append(lastEntry.item())

                    # Decrement the counter for this entry, and remove it if 0
                    newCount = lastEntry.decrement()
                    if newCount == 0:
                        entries.pop()

                promo = CheapestFreePromo(items)
                self.__promos.append(promo)

                self.__total += promo.cost()
                self.__savings += promo.savings()


                numItems -= 3


