import unittest

from shopkit.ledger import InsufficientFunds, Ledger


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.ledger = Ledger()
        self.ledger.open("ann", 1000)
        self.ledger.open("bob", 0)

    def test_unknown_balance_is_zero(self):
        self.assertEqual(self.ledger.balance("zed"), 0)

    def test_transfer(self):
        self.ledger.transfer("ann", "bob", 300)
        self.assertEqual(self.ledger.balance("ann"), 700)
        self.assertEqual(self.ledger.balance("bob"), 300)

    def test_transfer_insufficient(self):
        with self.assertRaises(InsufficientFunds):
            self.ledger.transfer("bob", "ann", 1)
        self.assertEqual(self.ledger.total(), 1000)

    def test_transfer_positive(self):
        with self.assertRaises(ValueError):
            self.ledger.transfer("ann", "bob", 0)
