import argparse

from Basket import Basket
from Inventory import Inventory
from Receipt import Receipt


def readInventory(inventoryFile):
    """
    Reads the given inventory file and returns a populated Inventory instance.

    Args:
        inventoryFile (str): The file from which to read the inventory.

    Returns:
        Inventory or None. The inventory file read from disk, or None if the
            file couldn't be read.
    """
    # Read the inventory from disk
    inventory = Inventory()
    try:
        inventory.readFromDisk(inventoryFile)

    except IOError as exception:
        print("[ERROR] : couldn't read inventory from file: %r - %s"
              % (args.inventoryFile, exception))
        return None

    return inventory


def readItems(itemsFile):
    """
    Reads the given items file and returns a list of the items.

    Args:
        itemsFile (str): The file from which to read the items.

    Returns:
        list of str. The items found in the file.
    """
    result = []

    try:
        with open(itemsFile) as itemsFile:
           for item in itemsFile:
                # Strip leading/trailing whitespace
                strippedItem = item.strip()
                if strippedItem:
                    result.append(strippedItem)

    except IOError as exception:
        print("[ERROR] : couldn't read items from file: %r - %s"
              % (itemsFile, exception))
        return []

    return result


def printInventory(inventoryFile):
    """
    Prints the contents of the given inventory file.

    Args:
        inventoryFile (str): The file from which to read the inventory.
    """
    # Read the inventory from disk
    inventory = readInventory(inventoryFile)
    if inventory is None:
        return

    items = inventory.getItemsPretty()
    print("Contents of inventory:\n\n%s" % items)


def printShoppingBasket(inventoryFile, itemNames):
    """
    Prints a receipt of the total cost and savings for the given list of items,
    using the given inventory.

    Args:
        inventoryFile (str): The file from which to read the inventory.
        itemNames (list of str): The names of the items for which to calculate
            and print the cost and savings.
    """
    # Exit early if we haven't been given any items
    if not itemNames:
        print("[WARNING] : no items found.")
        return

    # Read the inventory from disk
    inventory = readInventory(inventoryFile)
    if inventory is None:
        return

    # Create a basket from the given items
    basket = Basket(inventory)
    for itemName in itemNames:
        try:
            basket.addItem(itemName)
        except KeyError as exception:
            print("[WARNING] : couldn't find item %r in inventory" % itemName)

    # Create a receipt from the basket
    receipt = Receipt.GetReceipt(basket)
    print(receipt)


def main():
    """
    Parses arguments + performs the appropriate actions.
    """
    # Parse arguments
    parser = argparse.ArgumentParser(prog="checkout.sh")

    # First argument must be the inventory file
    parser.add_argument("inventoryFile", action="store")

    # Optional flag to list the contents of the inventory - in this case we
    # ignore any supplied items and don't print a receipt
    parser.add_argument("--list", action="store_true",
                        help="List the contents of the inventory file")

    # Items can either be given as arguments or supplied in a text file
    itemsGroup = parser.add_mutually_exclusive_group()
    itemsGroup.add_argument('--itemsFile', action='store')
    itemsGroup.add_argument('--items', action='store',
                            nargs=argparse.REMAINDER)

    args = parser.parse_args()

    # List the contents of the inventory if we've been asked to
    if args.list:
        printInventory(args.inventoryFile)
        exit()

    # Read the shopping list from disk if a file was provided
    itemNames = []
    if args.itemsFile:
        itemNames = readItems(args.itemsFile)
    else:
        itemNames = args.items

    # Compute and print the shopping basket
    printShoppingBasket(args.inventoryFile, itemNames)

