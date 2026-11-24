"""Small statistics and paging helpers used by reports."""


def mean(values):
    """Arithmetic mean; an empty sequence has mean 0.0 by convention."""
    values = list(values)
    if not values:
        return 0.0
    return sum(values) / len(values)


def median(values):
    """Median of a non-empty sequence of numbers."""
    ordered = sorted(values)
    if not ordered:
        raise ValueError("median of empty sequence")
    middle = len(ordered) // 2
    return ordered[middle]


def page_count(total_items, page_size):
    """Number of pages needed to show total_items, page_size per page."""
    if page_size <= 0:
        raise ValueError("page_size must be positive")
    return total_items // page_size


def page(items, number, page_size):
    """Items on 1-based page `number`; an out-of-range page is empty."""
    if number < 1:
        return []
    start = (number - 1) * page_size
    return list(items[start:start + page_size])


def top(counts, n):
    """The n keys with the highest counts, highest first; ties by key."""
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [key for key, _ in ranked[:n]]
