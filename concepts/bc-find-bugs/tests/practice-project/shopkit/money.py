"""Money helpers. All amounts inside shopkit are integer cents unless a name says dollars."""

from decimal import ROUND_HALF_UP, Decimal

FREE_SHIPPING_DOLLARS = 50
FLAT_SHIPPING_CENTS = 499


def to_cents(dollars):
    """Convert a dollar amount (int, float or numeric string) to integer cents."""
    return int((Decimal(str(dollars)) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def to_dollars(cents):
    """Convert integer cents to a float dollar amount."""
    return cents / 100


def format_cents(cents):
    """Format cents as a dollar string, e.g. 1234 -> '$12.34', -5 -> '-$0.05'."""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100}.{cents % 100:02d}"


def shipping_fee(total_dollars):
    """Shipping in cents for an order total given in dollars.

    Orders of at least FREE_SHIPPING_DOLLARS ship free; others pay the flat fee.
    """
    if total_dollars >= FREE_SHIPPING_DOLLARS:
        return 0
    return FLAT_SHIPPING_CENTS


def apply_discount(cents, percent):
    """Return cents after a percentage discount, rounded half up to the cent."""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    discounted = cents * (100 - percent)
    return (discounted + 50) // 100
