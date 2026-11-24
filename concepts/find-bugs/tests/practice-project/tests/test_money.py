import unittest

from shopkit import money


class MoneyTest(unittest.TestCase):
    def test_to_cents_rounds(self):
        self.assertEqual(money.to_cents("12.345"), 1235)
        self.assertEqual(money.to_cents(3), 300)

    def test_format_cents(self):
        self.assertEqual(money.format_cents(1234), "$12.34")
        self.assertEqual(money.format_cents(-5), "-$0.05")
        self.assertEqual(money.format_cents(0), "$0.00")

    def test_shipping_threshold(self):
        self.assertEqual(money.shipping_fee(50), 0)
        self.assertEqual(money.shipping_fee(49.99), money.FLAT_SHIPPING_CENTS)

    def test_discount(self):
        self.assertEqual(money.apply_discount(1000, 10), 900)
        self.assertEqual(money.apply_discount(999, 50), 500)
        with self.assertRaises(ValueError):
            money.apply_discount(100, 101)
