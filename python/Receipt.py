
def formatPrice(price):
    """
    Returns a formatted price string.

    Args:
        price (float): The price to format.

    Returns:
        str. The formatted price.
    """
    return "%.2f" % price


def formatName(name, maxWidth):
    """
    Formats the given item name.

    Args:
        name (str): The name to format.
        maxWidth (str): The maximum width to crop the name to.

    Returns:
        str. The formatted name.
    """
    if len(name) > maxWidth:
        name = "%s..." % name[:maxWidth-3]

    return name.ljust(maxWidth)


class Receipt(object):
    """
    Class to print out the receipt for a given shopping basket.
    """

    # Dimensions for the printed output
    LeftMarginWidth = 2
    NameColumnWidth = 40
    PriceColumnWidth = 15
    CountColumnWidth = 10

    # There's a space between the columns, so separators need one extra char
    SeparatorWidth = NameColumnWidth + PriceColumnWidth + 1

    @classmethod
    def GetReceipt(cls, basket):
        """
        Generates a receipt for the given basket.

        Args:
            basket (Basket): The basket for which to generate a receipt.

        Returns:
            str. A string representing the receipt for our basket.
        """
        # Store a list of pairs of strings, to format into two columns
        lines = []
        separator = ("-" * cls.SeparatorWidth, "")
        separator2 = ("=" * cls.SeparatorWidth, "")

        # First just list all the entries
        totalBeforePromos = 0.0
        for entry in basket.entries():
            count = entry.count()
            if count <= 0:
                continue

            item = entry.item()
            name = item.name()
            price = item.price()
            totalPrice = count * price

            nameWidth = cls.NameColumnWidth
            if count == 1:
                # Format the name to the width of the column
                lines.append((formatName(name, nameWidth), "%.2f" % price))
            else:
                # Use the extra space for the name if we have multiples - we
                # put the count and price on a separate line
                nameWidth += cls.PriceColumnWidth
                lines.append((formatName(name, nameWidth), ""))
                formattedCount = "%s @ %s" % (str(count).rjust(cls.PriceColumnWidth), formatPrice(price))
                lines.append((formattedCount, formatPrice(totalPrice)))

            totalBeforePromos += totalPrice

        # Add a sub-total for the amount before promos
        lines.append(separator)
        lines.append(("SUB-TOTAL:", formatPrice(totalBeforePromos)))

        # Now give details of promos
        lines.append(separator)
        lines.append(("OFFERS:", ""))
        for promo in basket.promos():
            lines.append(("%s%s" % (cls.LeftMarginWidth * " ", promo.name()),
                                    formatPrice(-promo.savings())))

        # Then total savings
        lines.append(separator)
        lines.append(("TOTAL SAVINGS:", formatPrice(basket.savings())))

        # Then add the total to pay
        lines.append(separator2)
        lines.append(("TOTAL TO PAY:", formatPrice(basket.total())))
        lines.append(separator2)

        # Add a left-hand margin and justify the columns
        outputLines = []
        for name, price in lines:
            formattedName = name.ljust(cls.NameColumnWidth)
            formattedPrice = price.rjust(cls.PriceColumnWidth)
            outputLines.append(
                "%s %s %s" % (cls.LeftMarginWidth * " ", formattedName, formattedPrice))

        # Join the output with newlines + return
        return "\n".join(outputLines)
