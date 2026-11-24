import unittest

from shopkit.inventory import Inventory, OutOfStock


def sample():
    inv = Inventory()
    inv.add("apple", 10, 120)
    inv.add("pear", 5, 200)
    return inv


class InventoryTest(unittest.TestCase):
    def test_find(self):
        inv = sample()
        self.assertEqual(inv.find("pear"), 1)
        self.assertIsNone(inv.find("plum"))

    def test_price(self):
        self.assertEqual(sample().price("pear"), 200)

    def test_set_price_unknown(self):
        with self.assertRaises(KeyError):
            sample().set_price("plum", 1)

    def test_reserve_and_release(self):
        inv = sample()
        inv.reserve("apple", 4)
        self.assertEqual(inv.stock("apple"), 6)
        inv.release("apple", 4)
        self.assertEqual(inv.stock("apple"), 10)

    def test_reserve_too_many(self):
        inv = sample()
        with self.assertRaises(OutOfStock):
            inv.reserve("pear", 6)
        self.assertEqual(inv.stock("pear"), 5)

    def test_duplicate_sku(self):
        with self.assertRaises(ValueError):
            sample().add("apple", 1, 1)
