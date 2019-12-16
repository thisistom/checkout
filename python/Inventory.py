import csv
import os

from Item import Item

class Inventory(object):

    # Initializer -------------------------------------------------------------

    def __init__(self):
        """
        Initializes an instance of the class.
        """
        self.__items = {}

    # Public Instance Methods -------------------------------------------------

    def addItem(self, item):
        """
        Adds the given item to the inventory.

        Will silently override an item already in the inventory which has the
        same name as the given item.

        Args:
            item (Item): The item to add.
        """
        itemName = item.name()
        self.__items[item.name()] = item

    def addItems(self, items):
        """
        Adds the given items to the inventory.

        Silently overwrites any items already in the inventory which have the
        same name as one of the given items.

        Args:
            items (list of Item): The items to add.
        """
        for item in items:
            self.addItem(item)

    def readFromDisk(self, filePath):
        """
        Replaces the inventory with the contents of the given CSV file.

        Args:
            filePath (str): Path to the file to read.

        Raises:
            IOError: If a readable file doesn't exist at the given path.
        """
        # Clear the existing contents
        self.__items = {}

        # This will raise IOError if the file can't be opened for reading
        with open(filePath) as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            lineCount = 0

            for row in csvReader:
                rowLength = len(row)
                if lineCount == 0:
                    # Check the header row
                    if (rowLength < 3):
                        print("[WARNING] : bad header row: %r" % row)
                    else:
                        if (row[0] != "name"
                                or row[1] != "price"
                                or row[2] != "promoGroup"):
                            print("[WARNING] : bad header row: %r - expected "
                                  "'name,price,promoGroup'")

                elif rowLength > 0:
                    if rowLength < 2:
                        print("[WARNING] : bad inventory entry: %r" % row)
                    else:
                        name = row[0]

                        # Be cautious about the price - might not like being
                        # converted to a float
                        try:
                            price = float(row[1])
                        except ValueError as exception:
                            print("[WARNING] : bad price for inventory entry: %r" % row)
                            continue

                        if rowLength > 2:
                            promoGroup = row[2]
                        else:
                            promoGroup = ""

                        item = Item(name, price, promoGroup)
                        self.addItem(item)

                lineCount += 1

    def getItem(self, itemName):
        """
        Returns:
            Item or None. The item in our inventory with the given name, or
                None if no such item was found.
        """
        return self.__items.get(itemName)

    def getItems(self):
        """
        Returns:
            list of Item. The items in our inventory.
        """
        return list(self.__items.values())

    def getItemsPretty(self):
        """
        Returns:
            str. A nicely formatted string representing the items in our inventory.
        """
        # Get the longest entry in each field
        maxNameLength = 0
        maxPriceLength = 0

        for item in self.__items.itervalues():
            maxNameLength = max(maxNameLength, len(item.name()))
            maxPriceLength = max(maxPriceLength, len("%.2f" % item.price()))

        lines = []
        for item in self.__items.itervalues():
            name = item.name().ljust(maxNameLength)
            price = ("%.2f" % item.price()).rjust(maxPriceLength)
            promoGroup = item.promoGroup()

            line = "%s @ %s - %s" % (name, price, promoGroup)
            lines.append(line)

        return "\n".join(lines)

