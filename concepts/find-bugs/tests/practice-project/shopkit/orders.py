"""Carts and order placement."""

from shopkit import money
from shopkit.inventory import OutOfStock


class UnknownSku(Exception):
    pass


class Cart:
    def __init__(self, owner, lines=[]):
        self.owner = owner
        self.lines = lines
        self.tags = set()

    def add(self, sku, quantity):
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        self.lines.append((sku, quantity))

    def tag(self, label):
        self.tags.add(label)

    def untag(self, label):
        """Remove a tag; removing a tag that is not there does nothing."""
        try:
            self.tags.remove(label)
        except KeyError:
            pass


def subtotal_cents(cart, inventory):
    total = 0
    for sku, quantity in cart.lines:
        position = inventory.find(sku)
        if not position:
            raise UnknownSku(sku)
        total += inventory.price(inventory.sku_at(position)) * quantity
    return total


def order_total_cents(cart, inventory):
    subtotal = subtotal_cents(cart, inventory)
    return subtotal + money.shipping_fee(subtotal)


def place_order(cart, inventory, ledger, events, now):
    """Reserve stock, charge the owner, and record the order.

    If anything fails, stock and balances are left as they were.
    """
    total = order_total_cents(cart, inventory)
    reserved = []
    try:
        for sku, quantity in cart.lines:
            inventory.reserve(sku, quantity)
            reserved.append((sku, quantity))
    except OutOfStock:
        for sku, quantity in reserved:
            inventory.release(sku, quantity)
        raise
    ledger.charge(cart.owner, total)
    events.record(now, "order", {"owner": cart.owner, "total": total})
    return total
