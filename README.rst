checkout
========

This project computes the cost of a shopping basket full of items,
given an inventory describing the items, their prices and the promotional
group of which they are part.

Quick Start
-----------

To try out the tool using the provided example files, run::

 ./checkout resources/inventory.csv --itemsFile resources/items.txt

You should expect to see output which looks something like this:

::

 =========================
 1 x lettuce        @ 0.50
 1 x carrots        @ 1.75
 2 x chickpeas      @ 0.75
 3 x potato waffles @ 2.50
 =========================
 TOTAL   = 8.75
 SAVINGS = 2.50

Inventory
---------

The inventory should be specified in CSV format, with a single header row and
three columns representing each item's name, price and promo group respectively.

For example:

::

 name,price,promoGroup
 "beans",1.0,"canned"
 "potato waffles",2.5,"frozen"
 "lettuce",0.5,"vegetables"

An example inventory is also provided at `resources/inventory.csv`.

To see the contents of the inventory, use the `--list` flag::

 ./checkout resources/inventory.csv --list

Items
-----

To compute the contents of a shopping cart, you must specify some items, using
the `--items` or `--itemsFile` flags. For example::

 ./checkout resources/inventory.csv --items lettuce peas

Note that item names which contain spaces must be enclosed in quotes::

 ./checkout resources/inventory.csv --items beans 'potato waffles' cabbage

Items can also be specified in a text file containing one item per line::

 ./checkout resources/inventory.csv --itemsFile resources/items.txt

An example items file is provided at `resources/items.txt`.

Unit Tests
----------

To run the unit tests, run::

 ./run_tests
