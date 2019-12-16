"""
Module providing some helpful utility functions.
"""
import random
import sys
from contextlib import contextmanager
from StringIO import StringIO

@contextmanager
def captureOutput():
    """
    Context manager to temporarily override stdout + stderr, to capture output.

    Use like this:

        with captureOutput() as (out, err):
            foo()

        output = out.getvalue().strip()
        self.assertEqual(output, 'my expected output')
    """
    newOut, newErr = StringIO(), StringIO()
    oldOut, oldErr = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = newOut, newErr
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = oldOut, oldErr

# Random words to use as promotional groups
promoGroups = [
    "leather",
    "flagrant",
    "agreement",
    "coach",
    "cannon",
    "hand",
    "rock",
    "quick",
    "violet",
    "victorious",
    "bounce",
    "noxious",
]
numPromoGroups = len(promoGroups)

def _randomGroup():
    ix = random.randint(0, numPromoGroups - 1)
    return promoGroups[ix]

def _randomPrice():
    price = random.random() * 1000.0
    return price

def generateRandomInventory(wordsFileIn, inventoryFileOut, numEntries=-1):
    """
    From a list of words, generate an inventory with random prices and promo
    groups. Intended for constructing very large inventories for testing.

    Args:
        wordsFileIn (str): Path to a file containing loads of words.
        inventoryFileOut (str): Path to the file to write to.
        numEntries (int): The number of entries to generate, or -1 to use all
            words in the input file. (Default: -1)

    Returns:
        int. The number of entries generated in the inventory.
    """
    numWords = 0

    with open(wordsFileIn, 'rt') as fileIn:
        with open(inventoryFileOut, 'w') as fileOut:
            # Write the header
            fileOut.write("name,price,promoGroup\n")

            for line in fileIn:
                name = line.strip()
                if not name:
                    continue

                price = _randomPrice()
                promoGroup = _randomGroup()

                outputLine = "%s,%.2f,%s\n" % (name, price, promoGroup)

                fileOut.write(outputLine)
                numWords += 1

                if numEntries > 0 and numWords > numEntries:
                    return numWords

    return numWords

def generateRandomItems(wordsFileIn, itemsFileOut, numItems=50):
    """
    From a list of words, choose a subset to use as an items list. Intended for
    use with very large inventories for testing.

    Args:
        wordsFileIn (str): Path to a file containing loads of words.
        inventoryFileOut (str): Path to the file to write to.
        numItems (int): The number of items to generate, or -1 to use all
            words in the input file. (Default: 50)

    Returns:
        int. The number of entries generated in the inventory.
    """
    with open(wordsFileIn, 'rt') as fileIn:
        # This reads the whole file into memory, which isn't great but will do for now.
        lines = fileIn.read().splitlines()

        with open(itemsFileOut, 'w') as fileOut:
            for ix in xrange(numItems):
                line = random.choice(lines)
                fileOut.write("%s\n" % line)
