

class Item(object):
    def __init__(self, name, price, promoGroup=""):
        """
        Initializes an instance of the class.

        Args:
            name (str): Name of the item.
            price (float): Price of the item.
            promoGroup (str): Name of the item's promo group. (Optional)
        """
        self.__name = name
        self.__price = price
        self.__promoGroup = promoGroup

    def name(self):
        return self.__name

    def price(self):
        return self.__price

    def promoGroup(self):
        return self.__promoGroup

    def __eq__(self, other):
        """
        Returns:
            bool. True if the other item has the same attributes as this item,
                otherwise False.

        Raises:
            NotImplementedError: If the other object is not an Item instance.
        """
        if not isinstance(other, Item):
            raise NotImplementedError("Can't compare item with %r" % other)

        return (self.__name == other.name()
                    and self.__price == other.price()
                    and self.__promoGroup == other.promoGroup())

    def __repr__(self):
        """
        Returns:
            str. A string representation of the item.
        """
        return ("Item <name=%r, price=%r, promoGroup=%r"
                % (self.__name, self.__price, self.__promoGroup))