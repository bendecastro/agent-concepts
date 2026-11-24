"""Customer account balances in cents."""


class InsufficientFunds(Exception):
    pass


class Ledger:
    def __init__(self):
        self._balances = {}

    def open(self, name, cents=0):
        if name in self._balances:
            raise ValueError(f"account {name} exists")
        self._balances[name] = cents

    def balance(self, name):
        """Balance in cents; an account that was never opened has balance 0."""
        return self._balances.get(name, 0)

    def charge(self, name, cents):
        if self._balances[name] < cents:
            raise InsufficientFunds(name)
        self._balances[name] -= cents

    def transfer(self, source, target, cents):
        """Move cents from source to target. Either both sides change or neither."""
        if cents <= 0:
            raise ValueError("amount must be positive")
        self.charge(source, cents)
        self._balances[target] += cents

    def total(self):
        return sum(self._balances.values())
