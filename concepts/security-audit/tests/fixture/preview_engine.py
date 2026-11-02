import sys


def render(expression):
    value = expression.strip()
    if value.startswith("size:"):
        count = int(value.split(":", 1)[1])
        return len(bytearray(count))
    if value == "version":
        return sys.version_info.major
    return value.upper()
