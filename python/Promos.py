


class _PromoEntry(object):
    """
    Base class for promotional groupings of items.
    """

    def __init__(self, items):
        """
        Initializes an instance of the class.

        Args:
            items (list of Item): The items for this promo.
        """
        self._items = items

    def cost(self):
        raise NotImplementedError("Must be defined in derived class")

    def savings(self):
        raise NotImplementedError("Must be defined in derived class")

    def name(self):
        raise NotImplementedError("Must be defined in derived class")


class ThreeForTwoPromo(_PromoEntry):

    def __init__(self, item, numPromos=1):
        """
        Initializes an instance of the class.

        Args:
            item (Item): The item for this promo.
            numPromos (int): The number of 3-for-2 promos. (Default: 1)
        """
        _PromoEntry.__init__(self, [item])
        self.__count = numPromos

    def cost(self):
        """
        Returns:
            float. The cost for this promotion.
        """
        return 2 * self._items[0].price() * self.__count

    def savings(self):
        """
        Returns:
            float. The savings from this promotion.
        """
        return self._items[0].price() * self.__count

    def name(self):
        """
        Returns:
            str. The name of this promotion.
        """
        return "%s - 3 for 2" % self._items[0].name()

class CheapestFreePromo(_PromoEntry):

    def __init__(self, items):
        """
        Initializes an instance of the class.

        Args:
            items (list of Item): The items for this promo.

        Raises:
            ValueError: If fewer than three items are provided.
        """
        _PromoEntry.__init__(self, items)

        if len(items) < 3:
            raise ValueError("Not enough items provided")

        self._items.sort(key=lambda item: item.price(), reverse=True)

    def cost(self):
        """
        Returns:
            float. The cost for this promotion.
        """
        return sum(item.price() for item in self._items[:-1])

    def savings(self):
        """
        Returns:
            float. The savings from this promotion.
        """
        return self._items[-1].price()

    def name(self):
        """
        Returns:
            str. The name of this promotion.
        """
        return "%s - buy 3 get cheapest free" % self._items[0].promoGroup()


class NoPromo(_PromoEntry):

    def __init__(self, item):
        """
        Initializes an instance of the class.

        Args:
            item (Item): The item for this promo.
        """
        _PromoEntry.__init__(self, [item])

    def cost(self):
        """
        Returns:
            float. The cost for this promotion.
        """
        return sum(item.price() for item in self._items)

    def savings(self):
        """
        Returns:
            float. The savings from this promotion.
        """
        return 0.0

    def name(self):
        """
        Returns:
            str. The name of this promotion.
        """
        return ""
