# stock_tool.py


class StockLookup:
    """A tool that knows about product stock. It knows nothing about chatting."""

    def __init__(self, stock_data):
        """Store the inventory this tool can look up."""
        self.stock_data = stock_data

    def find_product(self, text):
        """Return the first known product named in the text, or None."""
        text_lower = text.lower()
        for product in self.stock_data:
            if product in text_lower:
                return product
        return None

    def count_for(self, product):
        """Return the stock count of one product, or None if unknown."""
        if product in self.stock_data:
            return self.stock_data[product]
        return None